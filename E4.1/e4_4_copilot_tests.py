"""
E4.4 — Copilot: Generación Automática de Tests
=================================================
Clase Calculator que el alumno da a Copilot para que genere tests.
Incluye tests de referencia para comparar con los generados.

Prompt para Copilot: "Genera tests unitarios completos para esta clase
Calculator usando unittest. Cubre: happy path, edge cases, errores."

Uso: python e4_4_copilot_tests.py

Dependencias: Solo librería estándar.
"""

import math
from typing import Union

__version__ = "1.0.0"

Number = Union[int, float]


class Calculator:
    """Calculadora con historial y memoria.

    El alumno pega esta clase en VS Code y pide a Copilot:
    "Genera tests unitarios completos para Calculator."
    """

    def __init__(self) -> None:
        self.history: list[str] = []
        self.memory: float = 0.0

    def add(self, a: Number, b: Number) -> Number:
        """Suma dos números."""
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result

    def subtract(self, a: Number, b: Number) -> Number:
        """Resta b de a."""
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result

    def multiply(self, a: Number, b: Number) -> Number:
        """Multiplica dos números."""
        result = a * b
        self.history.append(f"{a} * {b} = {result}")
        return result

    def divide(self, a: Number, b: Number) -> float:
        """Divide a entre b. Lanza ZeroDivisionError si b=0."""
        if b == 0:
            raise ZeroDivisionError("No se puede dividir por cero")
        result = a / b
        self.history.append(f"{a} / {b} = {result}")
        return result

    def power(self, base: Number, exp: Number) -> Number:
        """Potencia: base^exp."""
        result = base ** exp
        self.history.append(f"{base} ^ {exp} = {result}")
        return result

    def sqrt(self, n: Number) -> float:
        """Raíz cuadrada. ValueError si n < 0."""
        if n < 0:
            raise ValueError("No se puede calcular raíz de número negativo")
        result = math.sqrt(n)
        self.history.append(f"√{n} = {result}")
        return result

    def modulo(self, a: Number, b: Number) -> Number:
        """Módulo (resto). ZeroDivisionError si b=0."""
        if b == 0:
            raise ZeroDivisionError("No se puede calcular módulo con divisor cero")
        result = a % b
        self.history.append(f"{a} % {b} = {result}")
        return result

    def memory_store(self, value: Number) -> None:
        """Almacena valor en memoria."""
        self.memory = float(value)

    def memory_recall(self) -> float:
        """Recupera valor de memoria."""
        return self.memory

    def memory_clear(self) -> None:
        """Limpia la memoria."""
        self.memory = 0.0

    def clear_history(self) -> None:
        """Limpia el historial."""
        self.history.clear()

    def get_history(self) -> list[str]:
        """Devuelve el historial de operaciones."""
        return self.history.copy()


# ═══════════════════════════════════════════════════════════════
# TESTS DE REFERENCIA (para comparar con los generados por Copilot)
# ═══════════════════════════════════════════════════════════════

def ejecutar_demo_y_tests() -> None:
    """Tests de referencia: lo que Copilot DEBERÍA generar."""

    print("=" * 70)
    print("E4.4 — TESTS DE REFERENCIA PARA CALCULATOR")
    print("=" * 70)
    print("\nEl alumno pega la clase Calculator en VS Code y pide:")
    print('"Genera tests unitarios completos para Calculator."')
    print("Luego compara los tests generados con estos de referencia.\n")

    c = Calculator()

    # Operaciones básicas
    assert c.add(2, 3) == 5
    assert c.add(-1, 1) == 0
    assert c.add(0.1, 0.2) == pytest_approx(0.3)
    print("  [PASS] Test 1-3: add() — positivos, negativos, decimales")

    assert c.subtract(10, 3) == 7
    assert c.subtract(0, 5) == -5
    print("  [PASS] Test 4-5: subtract()")

    assert c.multiply(3, 4) == 12
    assert c.multiply(-2, 3) == -6
    assert c.multiply(0, 999) == 0
    print("  [PASS] Test 6-8: multiply()")

    assert c.divide(10, 2) == 5.0
    assert c.divide(7, 3) == pytest_approx(2.333, 0.01)
    print("  [PASS] Test 9-10: divide()")

    try:
        c.divide(1, 0)
        assert False
    except ZeroDivisionError:
        pass
    print("  [PASS] Test 11: divide(1, 0) → ZeroDivisionError")

    assert c.power(2, 10) == 1024
    assert c.power(5, 0) == 1
    print("  [PASS] Test 12-13: power()")

    assert c.sqrt(16) == 4.0
    assert c.sqrt(0) == 0.0
    print("  [PASS] Test 14-15: sqrt()")

    try:
        c.sqrt(-4)
        assert False
    except ValueError:
        pass
    print("  [PASS] Test 16: sqrt(-4) → ValueError")

    assert c.modulo(10, 3) == 1
    print("  [PASS] Test 17: modulo()")

    # Historial
    c2 = Calculator()
    c2.add(1, 2)
    c2.multiply(3, 4)
    h = c2.get_history()
    assert len(h) == 2
    assert "1 + 2 = 3" in h[0]
    print("  [PASS] Test 18: Historial registra operaciones")

    c2.clear_history()
    assert len(c2.get_history()) == 0
    print("  [PASS] Test 19: clear_history()")

    # Memoria
    c3 = Calculator()
    c3.memory_store(42)
    assert c3.memory_recall() == 42.0
    c3.memory_clear()
    assert c3.memory_recall() == 0.0
    print("  [PASS] Test 20: memory_store/recall/clear")

    print(f"\n  Todos los tests pasaron correctamente.")
    print(f"\n  Comparar con los tests que genera Copilot:")
    print(f"  - ¿Cuántos tests genera? (referencia: 20)")
    print(f"  - ¿Cubre edge cases? (0, negativos, decimales)")
    print(f"  - ¿Verifica excepciones? (ZeroDivisionError, ValueError)")
    print(f"  - ¿Testea historial y memoria?")


def pytest_approx(expected: float, tolerance: float = 0.001) -> bool:
    """Pseudo-approx para comparación de floats sin pytest."""
    class Approx:
        def __init__(self, val, tol):
            self.val = val
            self.tol = tol
        def __eq__(self, other):
            return abs(other - self.val) < self.tol
    return Approx(expected, tolerance)


if __name__ == "__main__":
    ejecutar_demo_y_tests()
