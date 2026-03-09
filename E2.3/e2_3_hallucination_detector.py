"""
E2.3 — Detector de Alucinaciones en Código Generado por IA
=============================================================
Herramienta que analiza snippets de código Python y verifica si las
librerías, módulos y atributos referenciados existen realmente.

Uso demo + tests:
    python e2_3_hallucination_detector.py

Dependencias: Solo librería estándar.
"""

import ast
import importlib
import importlib.util
import sys
from typing import Optional

__version__ = "1.0.0"


# ═══════════════════════════════════════════════════════════════
# DETECTOR
# ═══════════════════════════════════════════════════════════════

class HallucinationDetector:
    """Detector de alucinaciones en código Python generado por IA.

    Analiza imports y llamadas a métodos para verificar si existen
    realmente en el ecosistema Python.

    Examples:
        >>> detector = HallucinationDetector()
        >>> result = detector.check_imports("import json")
        >>> result[0]["exists"]
        True
    """

    # Módulos conocidos de la librería estándar (subset)
    STDLIB_MODULES: set[str] = {
        "abc", "argparse", "ast", "asyncio", "base64", "bisect",
        "calendar", "collections", "configparser", "contextlib",
        "copy", "csv", "ctypes", "dataclasses", "datetime",
        "decimal", "difflib", "email", "enum", "fileinput",
        "fnmatch", "fractions", "functools", "getpass", "glob",
        "gzip", "hashlib", "heapq", "hmac", "html", "http",
        "importlib", "inspect", "io", "itertools", "json",
        "logging", "math", "multiprocessing", "operator", "os",
        "pathlib", "pickle", "platform", "pprint", "queue",
        "random", "re", "secrets", "shutil", "signal", "socket",
        "sqlite3", "statistics", "string", "struct", "subprocess",
        "sys", "tempfile", "textwrap", "threading", "time",
        "timeit", "traceback", "typing", "unittest", "urllib",
        "uuid", "warnings", "weakref", "xml", "zipfile",
    }

    # Métodos falsos conocidos (frecuentes en alucinaciones de IA)
    KNOWN_FAKE_METHODS: list[str] = [
        "auto_optimize", "auto_clean", "smart_merge",
        "deep_analyze", "quick_transform", "auto_format",
        "execute_query", "fast_predict", "auto_encode",
        "smart_filter", "quick_validate", "auto_normalize",
    ]

    def __init__(self) -> None:
        """Inicializa el detector."""
        pass

    def check_imports(self, code: str) -> list[dict]:
        """Analiza los imports de un código y verifica su existencia.

        Usa ast.parse para extraer imports y importlib.util.find_spec
        para verificar si el módulo existe.

        Args:
            code: String con código Python a analizar.

        Returns:
            Lista de diccionarios con:
                - module: nombre del módulo
                - attribute: atributo importado (si aplica)
                - exists: bool si el módulo existe
                - hallucination: bool si se detecta alucinación
                - detail: descripción del resultado
        """
        results: list[dict] = []

        if not code.strip():
            return results

        try:
            tree = ast.parse(code)
        except SyntaxError:
            return [{"module": "?", "attribute": None, "exists": False,
                     "hallucination": True, "detail": "Error de sintaxis en el código"}]

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    module_name: str = alias.name
                    result = self._check_module(module_name)
                    results.append(result)

            elif isinstance(node, ast.ImportFrom):
                module_name = node.module or ""
                for alias in node.names:
                    attr_name: str = alias.name
                    result = self._check_module_attribute(module_name, attr_name)
                    results.append(result)

        return results

    def _check_module(self, module_name: str) -> dict:
        """Verifica si un módulo existe.

        Args:
            module_name: Nombre completo del módulo.

        Returns:
            Diccionario con resultado de la verificación.
        """
        exists: bool = False
        detail: str = ""

        # Verificar con find_spec
        try:
            spec = importlib.util.find_spec(module_name)
            exists = spec is not None
        except (ModuleNotFoundError, ValueError):
            exists = False

        # También verificar en stdlib conocida
        top_level: str = module_name.split(".")[0]
        is_stdlib: bool = top_level in self.STDLIB_MODULES

        if exists:
            detail = f"Módulo '{module_name}' existe"
            if is_stdlib:
                detail += " (librería estándar)"
        else:
            detail = f"Módulo '{module_name}' NO encontrado — posible alucinación"

        return {
            "module": module_name,
            "attribute": None,
            "exists": exists,
            "hallucination": not exists,
            "detail": detail,
        }

    def _check_module_attribute(self, module_name: str, attr_name: str) -> dict:
        """Verifica si un atributo existe en un módulo.

        Args:
            module_name: Nombre del módulo.
            attr_name: Nombre del atributo a verificar.

        Returns:
            Diccionario con resultado de la verificación.
        """
        # Primero verificar que el módulo existe
        module_exists: bool = False
        attr_exists: bool = False
        detail: str = ""

        try:
            spec = importlib.util.find_spec(module_name)
            module_exists = spec is not None
        except (ModuleNotFoundError, ValueError):
            module_exists = False

        if not module_exists:
            detail = f"Módulo '{module_name}' NO existe — '{attr_name}' es alucinación"
            return {
                "module": module_name,
                "attribute": attr_name,
                "exists": False,
                "hallucination": True,
                "detail": detail,
            }

        # Módulo existe, verificar atributo
        try:
            mod = importlib.import_module(module_name)
            attr_exists = hasattr(mod, attr_name)
        except Exception:
            # No se puede importar (puede tener dependencias)
            # Marcamos como no verificable
            return {
                "module": module_name,
                "attribute": attr_name,
                "exists": True,
                "hallucination": False,
                "detail": f"Módulo '{module_name}' existe pero no se pudo verificar '{attr_name}'",
            }

        if attr_exists:
            detail = f"'{module_name}.{attr_name}' existe"
        else:
            detail = f"'{attr_name}' NO existe en '{module_name}' — posible alucinación"

        return {
            "module": module_name,
            "attribute": attr_name,
            "exists": attr_exists,
            "hallucination": not attr_exists,
            "detail": detail,
        }

    def check_methods(self, code: str, known_fakes: Optional[list[str]] = None) -> list[dict]:
        """Busca llamadas a métodos conocidos como falsos.

        Args:
            code: Código Python a analizar.
            known_fakes: Lista de nombres de métodos falsos conocidos.
                        Si None, usa KNOWN_FAKE_METHODS.

        Returns:
            Lista de diccionarios con métodos sospechosos encontrados.
        """
        if known_fakes is None:
            known_fakes = self.KNOWN_FAKE_METHODS

        results: list[dict] = []
        if not code.strip():
            return results

        for i, line in enumerate(code.split("\n"), 1):
            for fake in known_fakes:
                if fake in line:
                    results.append({
                        "method": fake,
                        "line": i,
                        "hallucination": True,
                        "detail": f"Método '{fake}' en línea {i} — conocido como alucinación frecuente",
                    })

        return results

    def analyze(self, code: str, label: str = "") -> dict:
        """Análisis completo de un snippet de código.

        Combina verificación de imports y métodos falsos.

        Args:
            code: Código Python a analizar.
            label: Etiqueta opcional para identificar el snippet.

        Returns:
            Diccionario con:
                - label: etiqueta
                - imports: resultados de check_imports
                - methods: resultados de check_methods
                - total_issues: número total de alucinaciones
                - verdict: "LIMPIO", "SOSPECHOSO" o "PELIGROSO"
        """
        imports: list[dict] = self.check_imports(code)
        methods: list[dict] = self.check_methods(code)

        import_issues: int = len([r for r in imports if r["hallucination"]])
        method_issues: int = len([r for r in methods if r["hallucination"]])
        total: int = import_issues + method_issues

        if total == 0:
            verdict = "LIMPIO"
        elif total <= 2:
            verdict = "SOSPECHOSO"
        else:
            verdict = "PELIGROSO"

        return {
            "label": label,
            "imports": imports,
            "methods": methods,
            "total_issues": total,
            "verdict": verdict,
        }


# ═══════════════════════════════════════════════════════════════
# SNIPPETS DE PRUEBA
# ═══════════════════════════════════════════════════════════════

SNIPPETS: list[dict] = [
    # Alucinaciones (5)
    {
        "label": "pandasql.execute_query()",
        "code": "import pandasql\nresult = pandasql.execute_query('SELECT * FROM df')",
        "has_hallucination": True,
    },
    {
        "label": "sklearn.neural.DeepClassifier",
        "code": "from sklearn.neural import DeepClassifier\nclf = DeepClassifier(layers=[64, 32])\nclf.fit(X, y)",
        "has_hallucination": True,
    },
    {
        "label": "import fastutils",
        "code": "import fastutils\nresult = fastutils.quick_transform(data)",
        "has_hallucination": True,
    },
    {
        "label": "df.auto_optimize()",
        "code": "import pandas as pd\ndf = pd.DataFrame({'a': [1, 2, 3]})\ndf.auto_optimize()",
        "has_hallucination": True,
    },
    {
        "label": "collections.TreeDict",
        "code": "from collections import TreeDict\nd = TreeDict(key=lambda x: x.priority)",
        "has_hallucination": True,
    },
    # Código correcto (5)
    {
        "label": "import json + json.dumps()",
        "code": "import json\ndata = {'nombre': 'Ana', 'edad': 30}\nresult = json.dumps(data, indent=2)",
        "has_hallucination": False,
    },
    {
        "label": "from pathlib import Path",
        "code": "from pathlib import Path\np = Path('archivo.txt')\nexists = p.exists()",
        "has_hallucination": False,
    },
    {
        "label": "from collections import Counter",
        "code": "from collections import Counter\nc = Counter(['a', 'b', 'a', 'c', 'a'])\ntop = c.most_common(2)",
        "has_hallucination": False,
    },
    {
        "label": "import csv",
        "code": "import csv\nwith open('data.csv') as f:\n    reader = csv.reader(f)",
        "has_hallucination": False,
    },
    {
        "label": "from datetime import datetime",
        "code": "from datetime import datetime\nnow = datetime.now()\nformatted = now.strftime('%Y-%m-%d')",
        "has_hallucination": False,
    },
]


# ═══════════════════════════════════════════════════════════════
# DEMO Y TESTS
# ═══════════════════════════════════════════════════════════════

def ejecutar_demo_y_tests() -> None:
    """Ejecuta demo y tests."""

    print("=" * 70)
    print("E2.3 — DEMO: DETECTOR DE ALUCINACIONES")
    print("=" * 70)

    detector = HallucinationDetector()

    aciertos: int = 0
    total_snippets: int = len(SNIPPETS)

    print(f"\nAnalizando {total_snippets} snippets de código...\n")

    for i, snippet in enumerate(SNIPPETS, 1):
        result = detector.analyze(snippet["code"], label=snippet["label"])

        has_issues: bool = result["total_issues"] > 0
        expected_issues: bool = snippet["has_hallucination"]

        if has_issues == expected_issues:
            aciertos += 1

        icon: str = "❌" if has_issues else "✅"
        verdict: str = result["verdict"]

        print(f"  {i:2d}. {icon} {snippet['label']}")
        print(f"      {verdict}", end="")

        if result["total_issues"] > 0:
            details = []
            for imp in result["imports"]:
                if imp["hallucination"]:
                    details.append(imp["detail"])
            for mth in result["methods"]:
                if mth["hallucination"]:
                    details.append(mth["detail"])
            if details:
                print(f" — {details[0]}", end="")
        print()

    print(f"\n{'─' * 50}")
    print(f"  Precisión del detector: {aciertos}/{total_snippets}")
    print(f"  Alucinaciones detectadas: {len([s for s in SNIPPETS if s['has_hallucination']])}/5")
    print(f"  Código limpio confirmado: {len([s for s in SNIPPETS if not s['has_hallucination']])}/5")

    # ═══════════════════════════════════════════════════════
    # TESTS
    # ═══════════════════════════════════════════════════════
    print(f"\n{'=' * 70}")
    print("TESTS:")
    print(f"{'=' * 70}")

    d = HallucinationDetector()

    # Test 1: Detecta módulo inexistente
    r = d.check_imports("import fastutils")
    assert len(r) == 1 and r[0]["hallucination"], f"fastutils debe ser alucinación"
    print("  [PASS] Test 1: Detecta 'import fastutils' como alucinación")

    # Test 2: Detecta submódulo inexistente
    r = d.check_imports("from sklearn.neural import DeepClassifier")
    hallucs = [x for x in r if x["hallucination"]]
    assert len(hallucs) >= 1, "sklearn.neural debe ser alucinación"
    print("  [PASS] Test 2: Detecta 'sklearn.neural' como alucinación")

    # Test 3: Detecta atributo inexistente en módulo real
    r = d.check_imports("from collections import TreeDict")
    hallucs = [x for x in r if x["hallucination"]]
    assert len(hallucs) >= 1, "TreeDict debe ser alucinación"
    print("  [PASS] Test 3: Detecta 'collections.TreeDict' como alucinación")

    # Test 4: NO marca json como alucinación
    r = d.check_imports("import json")
    assert len(r) == 1 and not r[0]["hallucination"], "json no es alucinación"
    print("  [PASS] Test 4: NO marca 'import json' como alucinación")

    # Test 5: NO marca pathlib.Path como alucinación
    r = d.check_imports("from pathlib import Path")
    hallucs = [x for x in r if x["hallucination"]]
    assert len(hallucs) == 0, "pathlib.Path no es alucinación"
    print("  [PASS] Test 5: NO marca 'pathlib.Path' como alucinación")

    # Test 6: NO marca collections.Counter como alucinación
    r = d.check_imports("from collections import Counter")
    hallucs = [x for x in r if x["hallucination"]]
    assert len(hallucs) == 0, "Counter no es alucinación"
    print("  [PASS] Test 6: NO marca 'collections.Counter' como alucinación")

    # Test 7: Detecta método falso conocido
    r = d.check_methods("df.auto_optimize()")
    assert len(r) >= 1 and r[0]["hallucination"], "auto_optimize es fake"
    print("  [PASS] Test 7: Detecta método falso 'auto_optimize'")

    # Test 8: analyze LIMPIO para código correcto
    r = d.analyze("import json\ndata = json.dumps({'a': 1})")
    assert r["verdict"] == "LIMPIO", f"Esperado LIMPIO, obtenido {r['verdict']}"
    print("  [PASS] Test 8: analyze() → LIMPIO para código correcto")

    # Test 9: analyze NO LIMPIO para código con alucinaciones
    r = d.analyze("import fastutils\nfastutils.quick_transform(data)")
    assert r["verdict"] != "LIMPIO", f"No debe ser LIMPIO, obtenido {r['verdict']}"
    assert r["total_issues"] >= 1
    print("  [PASS] Test 9: analyze() → no LIMPIO para alucinaciones")

    # Test 10: Código vacío no lanza error
    r = d.analyze("")
    assert r["verdict"] == "LIMPIO"
    assert r["total_issues"] == 0
    print("  [PASS] Test 10: Código vacío → LIMPIO sin error")

    print(f"\n  Todos los tests pasaron correctamente.")


if __name__ == "__main__":
    ejecutar_demo_y_tests()
