"""
E4.7 — Doxygen: Documentación Automática Multi-Lenguaje
==========================================================
Módulo documentado con estilo Doxygen (compatible con Python y C).
El alumno genera docs con: doxygen Doxyfile

Uso: python e4_7_doxygen_demo.py

Dependencias: Solo librería estándar. Doxygen para generar docs.
"""

__version__ = "1.0.0"


## @package e4_7_doxygen_demo
#  Módulo de ejemplo para documentación Doxygen.
#
#  Demuestra cómo documentar clases y funciones Python
#  con comentarios Doxygen para generación automática de docs HTML.


class TemperatureConverter:
    """Conversor de temperaturas entre Celsius, Fahrenheit y Kelvin.

    @brief Clase para conversión de temperaturas.
    @details Soporta 3 escalas: Celsius (°C), Fahrenheit (°F), Kelvin (K).
    Incluye historial de conversiones y validación de temperaturas imposibles.

    @note Kelvin no puede ser negativo (cero absoluto = 0K = -273.15°C).

    @code
    converter = TemperatureConverter()
    result = converter.celsius_to_fahrenheit(100)
    print(result)  # 212.0
    @endcode
    """

    ## Cero absoluto en Celsius
    ABSOLUTE_ZERO_C: float = -273.15

    ## Cero absoluto en Fahrenheit
    ABSOLUTE_ZERO_F: float = -459.67

    def __init__(self) -> None:
        """@brief Constructor. Inicializa historial vacío."""
        ## @var history
        #  Lista de conversiones realizadas
        self.history: list[dict] = []

    def celsius_to_fahrenheit(self, celsius: float) -> float:
        """Convierte Celsius a Fahrenheit.

        @brief Conversión °C → °F
        @param celsius Temperatura en grados Celsius.
        @return Temperatura en grados Fahrenheit.
        @exception ValueError Si la temperatura es inferior al cero absoluto.

        @par Fórmula:
        @f$ F = C \\times \\frac{9}{5} + 32 @f$
        """
        self._validate_celsius(celsius)
        result = celsius * 9 / 5 + 32
        self._log("C→F", celsius, result)
        return round(result, 2)

    def fahrenheit_to_celsius(self, fahrenheit: float) -> float:
        """Convierte Fahrenheit a Celsius.

        @brief Conversión °F → °C
        @param fahrenheit Temperatura en grados Fahrenheit.
        @return Temperatura en grados Celsius.
        @exception ValueError Si la temperatura es inferior al cero absoluto.

        @par Fórmula:
        @f$ C = (F - 32) \\times \\frac{5}{9} @f$
        """
        self._validate_fahrenheit(fahrenheit)
        result = (fahrenheit - 32) * 5 / 9
        self._log("F→C", fahrenheit, result)
        return round(result, 2)

    def celsius_to_kelvin(self, celsius: float) -> float:
        """Convierte Celsius a Kelvin.

        @brief Conversión °C → K
        @param celsius Temperatura en grados Celsius.
        @return Temperatura en Kelvin.

        @par Fórmula:
        @f$ K = C + 273.15 @f$
        """
        self._validate_celsius(celsius)
        result = celsius + 273.15
        self._log("C→K", celsius, result)
        return round(result, 2)

    def kelvin_to_celsius(self, kelvin: float) -> float:
        """Convierte Kelvin a Celsius.

        @brief Conversión K → °C
        @param kelvin Temperatura en Kelvin.
        @return Temperatura en grados Celsius.
        @exception ValueError Si Kelvin es negativo.
        """
        if kelvin < 0:
            raise ValueError(f"Kelvin no puede ser negativo: {kelvin}")
        result = kelvin - 273.15
        self._log("K→C", kelvin, result)
        return round(result, 2)

    def batch_convert(self, temps: list[float], from_scale: str, to_scale: str) -> list[float]:
        """Convierte una lista de temperaturas entre escalas.

        @brief Conversión por lotes.
        @param temps Lista de temperaturas a convertir.
        @param from_scale Escala origen: "C", "F" o "K".
        @param to_scale Escala destino: "C", "F" o "K".
        @return Lista de temperaturas convertidas.

        @see celsius_to_fahrenheit
        @see fahrenheit_to_celsius
        """
        converters = {
            ("C", "F"): self.celsius_to_fahrenheit,
            ("F", "C"): self.fahrenheit_to_celsius,
            ("C", "K"): self.celsius_to_kelvin,
            ("K", "C"): self.kelvin_to_celsius,
        }
        fn = converters.get((from_scale.upper(), to_scale.upper()))
        if not fn:
            raise ValueError(f"Conversión no soportada: {from_scale}→{to_scale}")
        return [fn(t) for t in temps]

    def get_history(self) -> list[dict]:
        """@brief Devuelve el historial de conversiones."""
        return self.history.copy()

    def _validate_celsius(self, temp: float) -> None:
        """@brief Valida que la temperatura no sea inferior al cero absoluto."""
        if temp < self.ABSOLUTE_ZERO_C:
            raise ValueError(f"Temperatura {temp}°C inferior al cero absoluto ({self.ABSOLUTE_ZERO_C}°C)")

    def _validate_fahrenheit(self, temp: float) -> None:
        """@brief Valida temperatura en Fahrenheit."""
        if temp < self.ABSOLUTE_ZERO_F:
            raise ValueError(f"Temperatura {temp}°F inferior al cero absoluto ({self.ABSOLUTE_ZERO_F}°F)")

    def _log(self, conversion: str, input_val: float, output_val: float) -> None:
        """@brief Registra una conversión en el historial."""
        self.history.append({"conversion": conversion, "input": input_val, "output": output_val})


# ═══════════════════════════════════════════════════════════════
# DOXYFILE EJEMPLO
# ═══════════════════════════════════════════════════════════════

DOXYFILE_CONTENT = """# Doxyfile para E4.7
PROJECT_NAME = "E4.7 Temperature Converter"
OUTPUT_DIRECTORY = docs_doxygen
INPUT = e4_7_doxygen_demo.py
RECURSIVE = NO
GENERATE_HTML = YES
GENERATE_LATEX = NO
EXTRACT_ALL = YES
OPTIMIZE_OUTPUT_JAVA = YES
PYTHON_DOCSTRING = YES
"""


def ejecutar_demo_y_tests() -> None:
    """Demo y tests del conversor documentado con Doxygen."""

    print("=" * 70)
    print("E4.7 — DEMO: DOXYGEN — DOCUMENTACIÓN AUTOMÁTICA")
    print("=" * 70)

    tc = TemperatureConverter()

    conversions = [
        ("0°C", tc.celsius_to_fahrenheit, 0, "32.0°F"),
        ("100°C", tc.celsius_to_fahrenheit, 100, "212.0°F"),
        ("212°F", tc.fahrenheit_to_celsius, 212, "100.0°C"),
        ("0°C", tc.celsius_to_kelvin, 0, "273.15K"),
        ("0K", tc.kelvin_to_celsius, 0, "-273.15°C"),
    ]

    print(f"\n  Conversiones de ejemplo:")
    for label, fn, val, expected in conversions:
        result = fn(val)
        print(f"    {label:10s} → {result} (esperado: {expected})")

    # Batch
    batch = tc.batch_convert([0, 25, 100], "C", "F")
    print(f"\n  Batch C→F [0, 25, 100]: {batch}")

    print(f"\n  Historial: {len(tc.get_history())} conversiones")

    print(f"\n{'─' * 50}")
    print("Comandos Doxygen:")
    print(f"{'─' * 50}")
    print("  1. Instalar: sudo apt install doxygen (o brew install doxygen)")
    print("  2. Crear Doxyfile con el contenido de ejemplo")
    print("  3. Ejecutar: doxygen Doxyfile")
    print("  4. Abrir docs_doxygen/html/index.html")

    print(f"\n{'─' * 50}")
    print("Tags Doxygen usados en este módulo:")
    print(f"{'─' * 50}")
    tags = ["@brief","@details","@param","@return","@exception","@note","@code/@endcode","@par","@f$...@f$","@see","@var","@package"]
    for t in tags:
        print(f"    {t}")

    # Tests
    print(f"\n{'=' * 70}")
    print("TESTS:")
    print(f"{'=' * 70}")

    t = TemperatureConverter()
    assert t.celsius_to_fahrenheit(0) == 32.0
    assert t.celsius_to_fahrenheit(100) == 212.0
    print("  [PASS] Test 1-2: C→F correcto")

    assert t.fahrenheit_to_celsius(32) == 0.0
    assert t.fahrenheit_to_celsius(212) == 100.0
    print("  [PASS] Test 3-4: F→C correcto")

    assert t.celsius_to_kelvin(0) == 273.15
    assert t.kelvin_to_celsius(273.15) == 0.0
    print("  [PASS] Test 5-6: C↔K correcto")

    try:
        t.celsius_to_fahrenheit(-300)
        assert False
    except ValueError:
        pass
    print("  [PASS] Test 7: Bajo cero absoluto → ValueError")

    try:
        t.kelvin_to_celsius(-1)
        assert False
    except ValueError:
        pass
    print("  [PASS] Test 8: Kelvin negativo → ValueError")

    batch = t.batch_convert([0, 100], "C", "F")
    assert batch == [32.0, 212.0]
    print("  [PASS] Test 9: batch_convert C→F")

    h = t.get_history()
    assert len(h) >= 8
    print(f"  [PASS] Test 10: Historial tiene {len(h)} entradas")

    print(f"\n  Todos los tests pasaron correctamente.")


if __name__ == "__main__":
    ejecutar_demo_y_tests()
