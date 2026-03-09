"""
E1.1 — Generación de Texto: Mi Primer Prompt
Función que genera un resumen de 3 líneas a partir de un texto largo.
Incluye docstring, type hints y manejo de errores.

Código generado como respuesta real de Claude al prompt del ejercicio.
"""


def generar_resumen(texto: str, num_lineas: int = 3) -> str:
    """Genera un resumen extraactivo de un texto seleccionando las oraciones más relevantes.

    El algoritmo puntúa cada oración según la frecuencia de sus palabras
    en el texto completo, priorizando oraciones con vocabulario representativo.
    Las oraciones seleccionadas se devuelven en su orden original.

    Args:
        texto: El texto largo del que se desea obtener un resumen.
        num_lineas: Número de oraciones a incluir en el resumen (por defecto 3).

    Returns:
        Un string con las oraciones más relevantes separadas por espacios.

    Raises:
        ValueError: Si el texto está vacío o num_lineas es menor que 1.
        TypeError: Si los argumentos no son del tipo esperado.

    Examples:
        >>> texto = "Python es un lenguaje versátil. Se usa en ciencia de datos. También en web."
        >>> resultado = generar_resumen(texto, num_lineas=2)
        >>> isinstance(resultado, str)
        True
    """
    # Validación de entrada
    if not isinstance(texto, str):
        raise TypeError(f"Se esperaba str, se recibió {type(texto).__name__}")
    if not isinstance(num_lineas, int):
        raise TypeError(f"num_lineas debe ser int, se recibió {type(num_lineas).__name__}")
    if num_lineas < 1:
        raise ValueError("num_lineas debe ser al menos 1")

    texto = texto.strip()
    if not texto:
        raise ValueError("El texto no puede estar vacío")

    # Paso 1: Dividir el texto en oraciones
    oraciones: list[str] = _dividir_en_oraciones(texto)

    # Si hay menos oraciones que las solicitadas, devolver todo
    if len(oraciones) <= num_lineas:
        return " ".join(oraciones)

    # Paso 2: Calcular frecuencia de palabras
    frecuencias: dict[str, int] = _calcular_frecuencias(texto)

    # Paso 3: Puntuar cada oración
    puntuaciones: list[tuple[int, float]] = []
    for indice, oracion in enumerate(oraciones):
        palabras = _normalizar_palabras(oracion)
        if palabras:
            puntaje = sum(frecuencias.get(p, 0) for p in palabras) / len(palabras)
        else:
            puntaje = 0.0
        puntuaciones.append((indice, puntaje))

    # Paso 4: Seleccionar las mejores oraciones manteniendo orden original
    puntuaciones.sort(key=lambda x: x[1], reverse=True)
    indices_seleccionados: list[int] = sorted(
        [idx for idx, _ in puntuaciones[:num_lineas]]
    )

    # Paso 5: Construir el resumen
    resumen: str = " ".join(oraciones[i] for i in indices_seleccionados)
    return resumen


def _dividir_en_oraciones(texto: str) -> list[str]:
    """Divide un texto en oraciones usando delimitadores comunes.

    Args:
        texto: Texto a dividir.

    Returns:
        Lista de oraciones no vacías.
    """
    import re
    # Dividir por punto, signo de exclamación o interrogación seguido de espacio
    oraciones_raw = re.split(r'(?<=[.!?])\s+', texto)
    return [o.strip() for o in oraciones_raw if o.strip()]


def _normalizar_palabras(texto: str) -> list[str]:
    """Extrae palabras normalizadas (minúsculas, sin puntuación) de un texto.

    Args:
        texto: Texto del que extraer palabras.

    Returns:
        Lista de palabras normalizadas.
    """
    import re
    palabras = re.findall(r'\b[a-záéíóúñü]+\b', texto.lower())
    # Filtrar palabras vacías comunes en español
    palabras_vacias = {
        'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas',
        'de', 'del', 'al', 'a', 'en', 'y', 'o', 'que', 'es',
        'se', 'no', 'por', 'con', 'para', 'su', 'sus', 'como',
        'más', 'pero', 'lo', 'le', 'ya', 'son', 'este', 'ha',
        'muy', 'también', 'fue', 'ser', 'tiene', 'esto', 'entre',
    }
    return [p for p in palabras if p not in palabras_vacias and len(p) > 2]


def _calcular_frecuencias(texto: str) -> dict[str, int]:
    """Calcula la frecuencia de cada palabra normalizada en el texto.

    Args:
        texto: Texto completo para análisis de frecuencia.

    Returns:
        Diccionario con cada palabra y su frecuencia.
    """
    from collections import Counter
    palabras = _normalizar_palabras(texto)
    return dict(Counter(palabras))


# ═══════════════════════════════════════════════════
# DEMO Y TESTS
# ═══════════════════════════════════════════════════

if __name__ == "__main__":
    # Texto de ejemplo sobre IA Generativa
    texto_ejemplo = (
        "La inteligencia artificial generativa ha revolucionado la forma en que "
        "interactuamos con la tecnología. Los modelos de lenguaje como GPT y Claude "
        "pueden generar texto coherente y útil a partir de instrucciones en lenguaje "
        "natural. Estas herramientas están transformando sectores como la programación, "
        "la educación y la creación de contenido. Los desarrolladores pueden usar estas "
        "herramientas para generar código, documentación y tests de forma automática. "
        "Sin embargo, es importante entender las limitaciones de estos modelos, como "
        "las alucinaciones y la dependencia de los datos de entrenamiento. La ingeniería "
        "de prompts se ha convertido en una habilidad fundamental para aprovechar al "
        "máximo el potencial de la IA generativa. Un buen prompt debe incluir contexto, "
        "restricciones y ejemplos para obtener resultados de calidad. Las empresas están "
        "adoptando estas tecnologías a un ritmo acelerado, creando nuevos roles como el "
        "de ingeniero de prompts. El futuro de la programación será una colaboración "
        "entre humanos y herramientas de IA cada vez más sofisticadas."
    )

    print("=" * 70)
    print("TEXTO ORIGINAL:")
    print("=" * 70)
    print(texto_ejemplo)
    print(f"\n(Longitud: {len(texto_ejemplo)} caracteres)")

    print("\n" + "=" * 70)
    print("RESUMEN (3 líneas):")
    print("=" * 70)
    resumen = generar_resumen(texto_ejemplo, num_lineas=3)
    print(resumen)

    print("\n" + "=" * 70)
    print("RESUMEN (1 línea):")
    print("=" * 70)
    resumen_corto = generar_resumen(texto_ejemplo, num_lineas=1)
    print(resumen_corto)

    # ── Tests básicos ──
    print("\n" + "=" * 70)
    print("TESTS:")
    print("=" * 70)

    # Test 1: Resultado no vacío
    assert len(resumen) > 0, "El resumen no debe estar vacío"
    print("  [PASS] Test 1: Resumen no vacío")

    # Test 2: Número correcto de oraciones
    oraciones_resumen = [o.strip() for o in resumen.split('.') if o.strip()]
    assert len(oraciones_resumen) <= 3, "No debe exceder num_lineas oraciones"
    print("  [PASS] Test 2: Número de oraciones correcto")

    # Test 3: Manejo de texto corto
    texto_corto = "Una sola oración."
    resultado_corto = generar_resumen(texto_corto, num_lineas=3)
    assert resultado_corto == texto_corto, "Con texto corto, devolver todo"
    print("  [PASS] Test 3: Texto más corto que num_lineas")

    # Test 4: Validación de entrada vacía
    try:
        generar_resumen("", num_lineas=3)
        assert False, "Debería lanzar ValueError"
    except ValueError:
        print("  [PASS] Test 4: ValueError con texto vacío")

    # Test 5: Validación de num_lineas inválido
    try:
        generar_resumen("Texto válido.", num_lineas=0)
        assert False, "Debería lanzar ValueError"
    except ValueError:
        print("  [PASS] Test 5: ValueError con num_lineas=0")

    # Test 6: Validación de tipo
    try:
        generar_resumen(123, num_lineas=3)  # type: ignore
        assert False, "Debería lanzar TypeError"
    except TypeError:
        print("  [PASS] Test 6: TypeError con argumento no-string")

    # Test 7: Las oraciones del resumen provienen del texto original
    oraciones_originales = _dividir_en_oraciones(texto_ejemplo)
    oraciones_res = _dividir_en_oraciones(resumen)
    for oracion in oraciones_res:
        assert oracion in oraciones_originales, f"Oración no encontrada: {oracion}"
    print("  [PASS] Test 7: Oraciones del resumen provienen del original")

    print("\n  Todos los tests pasaron correctamente.")
