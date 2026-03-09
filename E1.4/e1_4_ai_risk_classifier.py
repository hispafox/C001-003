"""
E1.4 — Clasificador de Nivel de Riesgo según el AI Act Europeo
================================================================
Aplicación CLI que clasifica sistemas de IA según su nivel de riesgo
bajo la Ley de IA Europea (AI Act).

Uso como CLI:
    python e1_4_ai_risk_classifier.py "chatbot de atención al cliente"
    python e1_4_ai_risk_classifier.py --interactive
    python e1_4_ai_risk_classifier.py --file descripciones.txt
    python e1_4_ai_risk_classifier.py --file descripciones.txt --format json

Uso como demo/tests (sin argumentos):
    python e1_4_ai_risk_classifier.py

Dependencias: Solo librería estándar de Python.
"""

import argparse
import json
import re
import sys
from typing import Optional

__version__ = "1.0.0"

# ═══════════════════════════════════════════════════════════════
# REGLAS DE CLASIFICACIÓN (basadas en el AI Act)
# ═══════════════════════════════════════════════════════════════

REGLAS_RIESGO: dict[str, dict] = {
    "inaceptable": {
        "keywords": [
            "manipulación subliminal", "scoring social", "puntuación social",
            "control social", "vigilancia biométrica masiva", "vigilancia masiva",
            "explotación vulnerabilidades", "manipulación comportamiento",
            "clasificación social gobierno", "reconocimiento facial masivo",
        ],
        "descripcion": "Prácticas de IA prohibidas por suponer un riesgo inaceptable para los derechos fundamentales",
    },
    "alto": {
        "keywords": [
            "selección candidatos", "selección de personal", "contratación", "despido",
            "empleo", "recursos humanos",
            "educación", "admisión", "evaluación exámenes", "calificación alumnos",
            "crédito", "scoring crediticio", "préstamo", "seguros", "solvencia",
            "justicia", "evidencia judicial", "sentencia", "libertad condicional",
            "migración", "visados", "asilo", "fronteras",
            "infraestructura crítica", "transporte autónomo", "energía", "suministro agua",
            "identificación biométrica", "reconocimiento facial",
        ],
        "descripcion": "Sistemas de alto riesgo sujetos a requisitos estrictos de conformidad",
    },
    "limitado": {
        "keywords": [
            "chatbot", "asistente virtual", "bot conversacional",
            "deepfake", "contenido sintético", "generación contenido",
            "generación imágenes", "generación de imágenes", "generador de imágenes",
            "generador de texto", "generador de vídeo", "generador",
            "reconocimiento emociones", "detección emociones",
            "atención al cliente", "soporte automatizado",
        ],
        "descripcion": "Sistemas con obligaciones específicas de transparencia",
    },
    "minimo": {
        "keywords": [
            "spam", "filtro correo", "antispam",
            "videojuego", "npc", "juego",
            "recomendación", "sugerencia contenido", "playlist",
            "productividad", "autocompletado", "corrector ortográfico",
            "optimización inventario", "búsqueda interna",
        ],
        "descripcion": "Sistemas de riesgo mínimo o nulo, sin obligaciones adicionales",
    },
}

# Orden de prioridad (más restrictivo primero)
ORDEN_PRIORIDAD: list[str] = ["inaceptable", "alto", "limitado", "minimo"]


# ═══════════════════════════════════════════════════════════════
# CLASIFICADOR
# ═══════════════════════════════════════════════════════════════

class RiskClassifier:
    """Clasificador de nivel de riesgo de sistemas de IA según el AI Act.

    Analiza la descripción de un sistema de IA y determina su nivel
    de riesgo basándose en keywords del reglamento europeo.

    Attributes:
        reglas: Diccionario con las reglas de clasificación por nivel.

    Examples:
        >>> clf = RiskClassifier()
        >>> resultado = clf.clasificar("filtro de spam para email")
        >>> resultado["nivel"]
        'minimo'
    """

    def __init__(self, reglas: Optional[dict[str, dict]] = None) -> None:
        """Inicializa el clasificador con las reglas de riesgo.

        Args:
            reglas: Diccionario de reglas personalizado. Si None, usa las reglas
                    predefinidas basadas en el AI Act.
        """
        self.reglas: dict[str, dict] = reglas or REGLAS_RIESGO

    def clasificar(self, descripcion: str) -> dict:
        """Clasifica un sistema de IA según su nivel de riesgo.

        Busca keywords de cada nivel en la descripción (case-insensitive).
        El nivel con más matches gana. En caso de empate, gana el más
        restrictivo. La confianza se basa en el número de keywords:
        alta (3+), media (2), baja (1), ninguna → mínimo por defecto.

        Args:
            descripcion: Descripción del sistema de IA a clasificar.

        Returns:
            Diccionario con:
                - nivel: str ('inaceptable', 'alto', 'limitado', 'minimo')
                - confianza: str ('alta', 'media', 'baja', 'sin_match')
                - keywords_encontradas: list[str]
                - justificacion: str
                - scores: dict[str, int] (matches por nivel)

        Raises:
            ValueError: Si la descripción está vacía.
            TypeError: Si la descripción no es string.
        """
        if not isinstance(descripcion, str):
            raise TypeError(f"Se esperaba str, se recibió {type(descripcion).__name__}")
        if not descripcion.strip():
            raise ValueError("La descripción no puede estar vacía")

        desc_lower: str = descripcion.lower()

        # Contar matches por nivel
        scores: dict[str, int] = {}
        keywords_por_nivel: dict[str, list[str]] = {}

        for nivel, regla in self.reglas.items():
            keywords_encontradas: list[str] = []
            for keyword in regla["keywords"]:
                if keyword.lower() in desc_lower:
                    keywords_encontradas.append(keyword)
            scores[nivel] = len(keywords_encontradas)
            keywords_por_nivel[nivel] = keywords_encontradas

        # Determinar nivel ganador (más matches; en empate, más restrictivo)
        mejor_nivel: str = "minimo"
        mejor_score: int = 0

        for nivel in ORDEN_PRIORIDAD:
            if scores.get(nivel, 0) > mejor_score:
                mejor_score = scores[nivel]
                mejor_nivel = nivel
            elif scores.get(nivel, 0) == mejor_score and mejor_score > 0:
                # Empate: gana el más restrictivo (primero en ORDEN_PRIORIDAD)
                idx_actual = ORDEN_PRIORIDAD.index(mejor_nivel)
                idx_nuevo = ORDEN_PRIORIDAD.index(nivel)
                if idx_nuevo < idx_actual:
                    mejor_nivel = nivel

        # Calcular confianza
        if mejor_score >= 3:
            confianza = "alta"
        elif mejor_score == 2:
            confianza = "media"
        elif mejor_score == 1:
            confianza = "baja"
        else:
            confianza = "sin_match"

        # Justificación
        regla_ganadora = self.reglas.get(mejor_nivel, {})
        justificacion: str = regla_ganadora.get("descripcion", "Sin descripción")

        todas_keywords: list[str] = keywords_por_nivel.get(mejor_nivel, [])

        return {
            "nivel": mejor_nivel,
            "confianza": confianza,
            "keywords_encontradas": todas_keywords,
            "justificacion": justificacion,
            "scores": scores,
        }

    def clasificar_batch(self, descripciones: list[str]) -> list[dict]:
        """Clasifica múltiples sistemas de IA.

        Args:
            descripciones: Lista de descripciones a clasificar.

        Returns:
            Lista de diccionarios con la clasificación de cada descripción.
        """
        resultados: list[dict] = []
        for desc in descripciones:
            try:
                resultado = self.clasificar(desc)
                resultado["descripcion"] = desc
                resultados.append(resultado)
            except (ValueError, TypeError) as e:
                resultados.append({
                    "descripcion": desc,
                    "nivel": "error",
                    "error": str(e),
                })
        return resultados


# ═══════════════════════════════════════════════════════════════
# FORMATO DE SALIDA
# ═══════════════════════════════════════════════════════════════

ICONOS_NIVEL: dict[str, str] = {
    "inaceptable": "🚫",
    "alto": "⚠️",
    "limitado": "ℹ️",
    "minimo": "✅",
}

def formatear_resultado(resultado: dict, indice: Optional[int] = None) -> str:
    """Formatea un resultado de clasificación para mostrar en consola.

    Args:
        resultado: Diccionario con la clasificación.
        indice: Número opcional para listas.

    Returns:
        String formateado.
    """
    lineas: list[str] = []
    prefijo = f"  {indice:2d}. " if indice is not None else "  "

    desc = resultado.get("descripcion", "")
    if desc:
        # Truncar si es muy larga
        desc_display = desc[:70] + "..." if len(desc) > 70 else desc
        lineas.append(f'{prefijo}"{desc_display}"')

    nivel = resultado["nivel"].upper()
    icono = ICONOS_NIVEL.get(resultado["nivel"], "")
    confianza = resultado.get("confianza", "")
    lineas.append(f"      {icono} → {nivel} (confianza: {confianza})")

    keywords = resultado.get("keywords_encontradas", [])
    if keywords:
        lineas.append(f"      Keywords: {', '.join(keywords)}")

    justificacion = resultado.get("justificacion", "")
    if justificacion:
        lineas.append(f"      {justificacion}")

    return "\n".join(lineas)


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

def crear_parser() -> argparse.ArgumentParser:
    """Crea el parser de argumentos CLI.

    Returns:
        ArgumentParser configurado.
    """
    parser = argparse.ArgumentParser(
        prog="ai_risk_classifier",
        description="Clasifica sistemas de IA según su nivel de riesgo (AI Act europeo).",
        epilog='Ejemplo: python e1_4_ai_risk_classifier.py "chatbot de atención al cliente"',
    )
    parser.add_argument(
        "descripcion", nargs="?", default=None,
        help="Descripción del sistema de IA a clasificar",
    )
    parser.add_argument(
        "-i", "--interactive", action="store_true",
        help="Modo interactivo: pide descripciones por teclado",
    )
    parser.add_argument(
        "-f", "--file",
        help="Archivo con descripciones (una por línea)",
    )
    parser.add_argument(
        "--format", choices=["text", "json"], default="text",
        help="Formato de salida (default: text)",
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}",
    )
    return parser


def main() -> int:
    """Punto de entrada CLI.

    Returns:
        Código de salida (0 = éxito).
    """
    parser = crear_parser()
    args = parser.parse_args()

    clf = RiskClassifier()

    # Modo archivo
    if args.file:
        try:
            with open(args.file, "r", encoding="utf-8") as f:
                descripciones = [l.strip() for l in f if l.strip()]
        except FileNotFoundError:
            print(f"Error: archivo no encontrado: {args.file}", file=sys.stderr)
            return 1

        resultados = clf.clasificar_batch(descripciones)
        if args.format == "json":
            print(json.dumps(resultados, ensure_ascii=False, indent=2))
        else:
            for i, r in enumerate(resultados, 1):
                print(formatear_resultado(r, indice=i))
                print()
        return 0

    # Modo interactivo
    if args.interactive:
        print("Clasificador de Riesgo AI Act — Modo Interactivo")
        print("Escribe una descripción (o 'salir' para terminar):\n")
        while True:
            try:
                desc = input("  > ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n\nSaliendo.")
                break
            if desc.lower() in ("salir", "exit", "quit", "q"):
                break
            if not desc:
                continue
            resultado = clf.clasificar(desc)
            resultado["descripcion"] = desc
            print(formatear_resultado(resultado))
            print()
        return 0

    # Modo directo
    if args.descripcion:
        resultado = clf.clasificar(args.descripcion)
        resultado["descripcion"] = args.descripcion
        if args.format == "json":
            print(json.dumps(resultado, ensure_ascii=False, indent=2))
        else:
            print(formatear_resultado(resultado))
        return 0

    # Sin argumentos → demo y tests
    ejecutar_demo_y_tests()
    return 0


# ═══════════════════════════════════════════════════════════════
# DEMO Y TESTS
# ═══════════════════════════════════════════════════════════════

EJEMPLOS_DEMO: list[tuple[str, str]] = [
    ("Sistema de scoring social usado por el gobierno para evaluar ciudadanos", "inaceptable"),
    ("Cámara de vigilancia con reconocimiento facial masivo en tiempo real en la vía pública", "inaceptable"),
    ("IA para selección automática de candidatos en procesos de empleo", "alto"),
    ("Sistema de evaluación automática de exámenes universitarios en educación", "alto"),
    ("IA para decisiones de concesión de créditos bancarios y scoring crediticio", "alto"),
    ("Chatbot de atención al cliente en una tienda online", "limitado"),
    ("Generador de imágenes por IA para campañas de marketing", "limitado"),
    ("Filtro de spam en correo electrónico", "minimo"),
    ("Sistema de recomendación de películas en plataforma de streaming", "minimo"),
    ("IA en NPCs de un videojuego de aventuras", "minimo"),
]


def ejecutar_demo_y_tests() -> None:
    """Ejecuta demo y tests automáticos."""

    print("=" * 70)
    print("E1.4 — DEMO: CLASIFICADOR DE RIESGO AI ACT")
    print("=" * 70)

    clf = RiskClassifier()

    # ── Demo ──
    print(f"\nClasificando {len(EJEMPLOS_DEMO)} sistemas de IA:\n")

    conteo: dict[str, int] = {}
    aciertos: int = 0

    for i, (descripcion, nivel_esperado) in enumerate(EJEMPLOS_DEMO, 1):
        resultado = clf.clasificar(descripcion)
        resultado["descripcion"] = descripcion
        print(formatear_resultado(resultado, indice=i))
        print()

        nivel_obtenido = resultado["nivel"]
        conteo[nivel_obtenido] = conteo.get(nivel_obtenido, 0) + 1
        if nivel_obtenido == nivel_esperado:
            aciertos += 1

    print(f"{'─' * 50}")
    print(f"  Resumen: ", end="")
    print(", ".join(f"{count} {nivel}" for nivel, count in sorted(conteo.items())))
    print(f"  Precisión en ejemplos de demo: {aciertos}/{len(EJEMPLOS_DEMO)}")

    # ═══════════════════════════════════════════════════════
    # TESTS
    # ═══════════════════════════════════════════════════════
    print(f"\n{'=' * 70}")
    print("TESTS:")
    print(f"{'=' * 70}")

    # Test 1: scoring social → inaceptable
    r = clf.clasificar("scoring social gobierno para evaluar ciudadanos")
    assert r["nivel"] == "inaceptable", f"Esperado inaceptable, obtenido {r['nivel']}"
    print("  [PASS] Test 1: scoring social → inaceptable")

    # Test 2: vigilancia biométrica masiva → inaceptable
    r = clf.clasificar("sistema de vigilancia biométrica masiva en espacios públicos")
    assert r["nivel"] == "inaceptable", f"Esperado inaceptable, obtenido {r['nivel']}"
    print("  [PASS] Test 2: vigilancia biométrica masiva → inaceptable")

    # Test 3: selección candidatos empleo → alto
    r = clf.clasificar("IA para selección de candidatos en proceso de empleo y contratación")
    assert r["nivel"] == "alto", f"Esperado alto, obtenido {r['nivel']}"
    print("  [PASS] Test 3: selección candidatos empleo → alto")

    # Test 4: evaluación exámenes educación → alto
    r = clf.clasificar("evaluación automática de exámenes en educación universitaria")
    assert r["nivel"] == "alto", f"Esperado alto, obtenido {r['nivel']}"
    print("  [PASS] Test 4: evaluación exámenes educación → alto")

    # Test 5: créditos bancarios → alto
    r = clf.clasificar("sistema de scoring crediticio para decisiones de crédito")
    assert r["nivel"] == "alto", f"Esperado alto, obtenido {r['nivel']}"
    print("  [PASS] Test 5: créditos bancarios → alto")

    # Test 6: chatbot → limitado
    r = clf.clasificar("chatbot de atención al cliente automatizado")
    assert r["nivel"] == "limitado", f"Esperado limitado, obtenido {r['nivel']}"
    print("  [PASS] Test 6: chatbot → limitado")

    # Test 7: generación imágenes → limitado
    r = clf.clasificar("herramienta de generación de imágenes por IA")
    assert r["nivel"] == "limitado", f"Esperado limitado, obtenido {r['nivel']}"
    print("  [PASS] Test 7: generación imágenes → limitado")

    # Test 8: filtro spam → mínimo
    r = clf.clasificar("filtro de spam para correo electrónico")
    assert r["nivel"] == "minimo", f"Esperado minimo, obtenido {r['nivel']}"
    print("  [PASS] Test 8: filtro spam → mínimo")

    # Test 9: recomendación → mínimo
    r = clf.clasificar("sistema de recomendación de películas y series")
    assert r["nivel"] == "minimo", f"Esperado minimo, obtenido {r['nivel']}"
    print("  [PASS] Test 9: recomendación → mínimo")

    # Test 10: descripción vacía → ValueError
    try:
        clf.clasificar("")
        assert False, "Debería lanzar ValueError"
    except ValueError:
        pass
    print("  [PASS] Test 10: descripción vacía → ValueError")

    print(f"\n  Todos los tests pasaron correctamente.")


# ═══════════════════════════════════════════════════════════════
# PUNTO DE ENTRADA
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    if len(sys.argv) > 1:
        sys.exit(main())
    else:
        ejecutar_demo_y_tests()
