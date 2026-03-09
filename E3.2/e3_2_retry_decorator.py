"""
E3.2 — Zero-shot: Decorador @retry con Espera Exponencial
============================================================
Generado con un solo prompt sin ejemplos de código (zero-shot).
Demuestra que un prompt descriptivo produce código funcional.

Uso: python e3_2_retry_decorator.py

Dependencias: Solo librería estándar.
"""

import functools
import logging
import random
import time
from typing import Any, Callable, Optional, Type

__version__ = "1.0.0"

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger("retry")


# ═══════════════════════════════════════════════════════════════
# RETRY CONFIG
# ═══════════════════════════════════════════════════════════════

class RetryConfig:
    """Configuración para el mecanismo de retry.

    Attributes:
        max_retries: Número máximo de reintentos.
        base_delay: Delay base en segundos.
        max_delay: Delay máximo en segundos (cap).
        exceptions: Tupla de excepciones a capturar.
        jitter: Si True, añade variación ±25% al delay.
    """

    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        exceptions: tuple[Type[Exception], ...] = (Exception,),
        jitter: bool = True,
    ) -> None:
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exceptions = exceptions
        self.jitter = jitter

    def calculate_delay(self, attempt: int) -> float:
        """Calcula el delay para un intento dado.

        Fórmula: delay = min(base_delay * 2^attempt, max_delay)
        Si jitter: delay *= random(0.75, 1.25)

        Args:
            attempt: Número de intento (0-indexed).

        Returns:
            Delay en segundos.
        """
        delay: float = min(self.base_delay * (2 ** attempt), self.max_delay)
        if self.jitter:
            delay *= random.uniform(0.75, 1.25)
        return round(delay, 4)


# ═══════════════════════════════════════════════════════════════
# DECORADOR @retry
# ═══════════════════════════════════════════════════════════════

def retry(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exceptions: tuple[Type[Exception], ...] = (Exception,),
    jitter: bool = True,
) -> Callable:
    """Decorador que reintenta funciones con espera exponencial.

    Args:
        max_retries: Máximo número de reintentos.
        base_delay: Delay base en segundos.
        max_delay: Delay máximo (cap).
        exceptions: Excepciones a capturar para reintentar.
        jitter: Añadir variación aleatoria al delay.

    Returns:
        Decorador que envuelve la función con lógica de retry.

    Examples:
        >>> @retry(max_retries=3, base_delay=0.01)
        ... def mi_funcion():
        ...     pass
    """
    config = RetryConfig(max_retries, base_delay, max_delay, exceptions, jitter)

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exception: Optional[Exception] = None

            for attempt in range(config.max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except config.exceptions as e:
                    last_exception = e
                    if attempt < config.max_retries:
                        delay = config.calculate_delay(attempt)
                        logger.info(
                            f"Retry {attempt + 1}/{config.max_retries}: "
                            f"{type(e).__name__}: {e}. Waiting {delay:.3f}s"
                        )
                        time.sleep(delay)
                    # Si no está en las excepciones configuradas, se propaga
                except Exception:
                    raise

            # Agotados todos los reintentos
            raise last_exception  # type: ignore

        return wrapper
    return decorator


# ═══════════════════════════════════════════════════════════════
# RETRY CON ESTADÍSTICAS
# ═══════════════════════════════════════════════════════════════

class RetryStats:
    """Estadísticas de uso del decorador retry.

    Attributes:
        total_calls: Total de llamadas a funciones decoradas.
        total_retries: Total de reintentos realizados.
        total_failures: Total de fallos definitivos.
    """

    def __init__(self) -> None:
        self.total_calls: int = 0
        self.total_retries: int = 0
        self.total_failures: int = 0

    @property
    def total_successes(self) -> int:
        """Número de llamadas exitosas."""
        return self.total_calls - self.total_failures

    @property
    def success_rate(self) -> float:
        """Tasa de éxito (0.0 a 1.0)."""
        return self.total_successes / self.total_calls if self.total_calls > 0 else 0.0

    def __repr__(self) -> str:
        return (f"RetryStats(calls={self.total_calls}, retries={self.total_retries}, "
                f"failures={self.total_failures}, success_rate={self.success_rate:.1%})")


def retry_with_stats(
    stats: RetryStats,
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exceptions: tuple[Type[Exception], ...] = (Exception,),
    jitter: bool = True,
) -> Callable:
    """Versión de retry que registra estadísticas.

    Args:
        stats: Objeto RetryStats para acumular estadísticas.
        max_retries: Máximo número de reintentos.
        base_delay: Delay base en segundos.
        max_delay: Delay máximo (cap).
        exceptions: Excepciones a capturar.
        jitter: Variación aleatoria.

    Returns:
        Decorador con tracking de estadísticas.
    """
    config = RetryConfig(max_retries, base_delay, max_delay, exceptions, jitter)

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            stats.total_calls += 1
            last_exception: Optional[Exception] = None

            for attempt in range(config.max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except config.exceptions as e:
                    last_exception = e
                    if attempt < config.max_retries:
                        stats.total_retries += 1
                        delay = config.calculate_delay(attempt)
                        time.sleep(delay)
                except Exception:
                    stats.total_failures += 1
                    raise

            stats.total_failures += 1
            raise last_exception  # type: ignore

        return wrapper
    return decorator


# ═══════════════════════════════════════════════════════════════
# DEMO Y TESTS
# ═══════════════════════════════════════════════════════════════

def ejecutar_demo_y_tests() -> None:
    """Demo y tests del decorador @retry."""

    print("=" * 70)
    print("E3.2 — DEMO: DECORADOR @retry (Zero-shot)")
    print("=" * 70)

    # ── Demo 1: Función inestable ──
    print(f"\n{'─' * 50}")
    print("Demo 1: Función que falla 2 veces y luego funciona")
    print(f"{'─' * 50}")

    call_count_1 = 0

    @retry(max_retries=5, base_delay=0.01, jitter=False)
    def servicio_inestable() -> str:
        nonlocal call_count_1
        call_count_1 += 1
        if call_count_1 <= 2:
            raise ConnectionError(f"Servicio no disponible (intento {call_count_1})")
        return "¡Éxito!"

    result = servicio_inestable()
    print(f"  Resultado: {result} (tras {call_count_1} intentos)")

    # ── Demo 2: Función que siempre falla ──
    print(f"\n{'─' * 50}")
    print("Demo 2: Función que siempre falla (max_retries=3)")
    print(f"{'─' * 50}")

    @retry(max_retries=3, base_delay=0.01, jitter=False)
    def siempre_falla() -> None:
        raise TimeoutError("Servidor no responde")

    try:
        siempre_falla()
    except TimeoutError as e:
        print(f"  Excepción final tras 3 retries: {e}")

    # ── Demo 3: Excepción no cubierta ──
    print(f"\n{'─' * 50}")
    print("Demo 3: Excepción no cubierta (solo captura ConnectionError)")
    print(f"{'─' * 50}")

    @retry(max_retries=5, base_delay=0.01, exceptions=(ConnectionError,))
    def error_inesperado() -> None:
        raise ValueError("Error de validación — no se reintenta")

    try:
        error_inesperado()
    except ValueError as e:
        print(f"  ValueError propagada sin retry: {e}")

    # ── Demo 4: Estadísticas ──
    print(f"\n{'─' * 50}")
    print("Demo 4: Retry con estadísticas")
    print(f"{'─' * 50}")

    stats = RetryStats()

    call_count_4 = 0

    @retry_with_stats(stats, max_retries=3, base_delay=0.01, jitter=False)
    def servicio_stats() -> str:
        nonlocal call_count_4
        call_count_4 += 1
        if call_count_4 % 3 != 0:  # Falla 2 de cada 3
            raise ConnectionError("Fallo")
        return "OK"

    for _ in range(6):
        call_count_4 = 0
        try:
            servicio_stats()
        except Exception:
            pass

    print(f"  {stats}")

    # ═══════════════════════════════════════════════════════
    # TESTS
    # ═══════════════════════════════════════════════════════
    print(f"\n{'=' * 70}")
    print("TESTS:")
    print(f"{'=' * 70}")

    # Test 1: Función OK no reintenta
    count = 0

    @retry(max_retries=3, base_delay=0.01)
    def ok_func() -> str:
        nonlocal count
        count += 1
        return "ok"

    count = 0
    assert ok_func() == "ok"
    assert count == 1
    print("  [PASS] Test 1: Función OK → 0 retries, 1 llamada")

    # Test 2: Falla 2, éxito al 3ro
    count = 0

    @retry(max_retries=5, base_delay=0.01, jitter=False)
    def falla_2() -> str:
        nonlocal count
        count += 1
        if count <= 2:
            raise RuntimeError("fail")
        return "ok"

    count = 0
    assert falla_2() == "ok"
    assert count == 3
    print("  [PASS] Test 2: Falla 2 veces → éxito al 3er intento")

    # Test 3: Siempre falla → lanza excepción
    @retry(max_retries=2, base_delay=0.01, jitter=False)
    def siempre_mal() -> None:
        raise RuntimeError("always fails")

    try:
        siempre_mal()
        assert False
    except RuntimeError:
        pass
    print("  [PASS] Test 3: Siempre falla → excepción tras max_retries")

    # Test 4: Solo captura excepciones especificadas
    @retry(max_retries=5, base_delay=0.01, exceptions=(ConnectionError,))
    def wrong_exc() -> None:
        raise TypeError("no capturada")

    try:
        wrong_exc()
        assert False
    except TypeError:
        pass
    print("  [PASS] Test 4: TypeError no capturada (solo ConnectionError)")

    # Test 5: max_retries=0
    count = 0

    @retry(max_retries=0, base_delay=0.01)
    def no_retry() -> None:
        nonlocal count
        count += 1
        raise RuntimeError("fail")

    count = 0
    try:
        no_retry()
    except RuntimeError:
        pass
    assert count == 1
    print("  [PASS] Test 5: max_retries=0 → no reintenta")

    # Test 6: Delay exponencial (sin jitter)
    cfg = RetryConfig(base_delay=1.0, jitter=False)
    assert cfg.calculate_delay(0) == 1.0
    assert cfg.calculate_delay(1) == 2.0
    assert cfg.calculate_delay(2) == 4.0
    assert cfg.calculate_delay(3) == 8.0
    print("  [PASS] Test 6: Delay exponencial: 1, 2, 4, 8")

    # Test 7: max_delay respetado
    cfg2 = RetryConfig(base_delay=1.0, max_delay=5.0, jitter=False)
    assert cfg2.calculate_delay(10) == 5.0
    print("  [PASS] Test 7: max_delay=5.0 respetado (2^10 capped)")

    # Test 8: functools.wraps preserva metadata
    @retry(max_retries=1, base_delay=0.01)
    def mi_funcion_documentada() -> None:
        """Docstring original."""
        pass

    assert mi_funcion_documentada.__name__ == "mi_funcion_documentada"
    assert "Docstring original" in (mi_funcion_documentada.__doc__ or "")
    print("  [PASS] Test 8: functools.wraps preserva __name__ y __doc__")

    # Test 9: Jitter añade variación
    cfg3 = RetryConfig(base_delay=1.0, jitter=True)
    delays = [cfg3.calculate_delay(2) for _ in range(20)]
    assert not all(d == delays[0] for d in delays), "Con jitter los delays deben variar"
    assert all(2.5 <= d <= 5.5 for d in delays), "Jitter ±25% de 4.0 → 3.0-5.0 aprox"
    print("  [PASS] Test 9: Jitter añade variación al delay")

    # Test 10: retry_with_stats
    st = RetryStats()
    call_c = 0

    @retry_with_stats(st, max_retries=2, base_delay=0.01, jitter=False)
    def stats_func() -> str:
        nonlocal call_c
        call_c += 1
        if call_c <= 1:
            raise RuntimeError("fail once")
        return "ok"

    call_c = 0
    stats_func()
    assert st.total_calls == 1
    assert st.total_retries == 1
    assert st.total_failures == 0
    assert st.success_rate == 1.0
    print(f"  [PASS] Test 10: retry_with_stats: {st}")

    print(f"\n  Todos los tests pasaron correctamente.")


if __name__ == "__main__":
    ejecutar_demo_y_tests()
