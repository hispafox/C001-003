"""
E4.5 — Ruff: Análisis Estático y Formateo de Código
======================================================
Código Python con 15 problemas que Ruff detecta y corrige.
El alumno ejecuta: ruff check e4_5_ruff_before.py
y luego: ruff format e4_5_ruff_before.py

Este archivo es la versión CORREGIDA (after). El archivo _before
tiene los problemas intencionados.

Uso: python e4_5_ruff_demo.py

Dependencias: Solo librería estándar. Ruff para la demo.
"""

__version__ = "1.0.0"

# ═══════════════════════════════════════════════════════════════
# CÓDIGO "BEFORE" — 15 problemas que Ruff detecta
# ═══════════════════════════════════════════════════════════════

BEFORE_CODE = '''
import os, sys, json  # E401: multiple imports on one line
import math  # F401: imported but unused
from typing import *  # F403: wildcard import

x=1  # E225: missing whitespace around operator
y = [1,2,3]  # E231: missing whitespace after comma

def bad_function( a,b,c ):  # E251: unexpected spaces around keyword / parameter equals
    """No docstring consistency."""
    if a == True:  # E712: comparison to True should be 'if a:'
        pass
    if b == None:  # E711: comparison to None should be 'if b is None:'
        pass
    l = []  # E741: ambiguous variable name 'l' (looks like 1)
    for i in range(0,10):
        l.append(i)
    
    unused_var = 42  # F841: local variable assigned but never used
    
    try:
        result = 1/0
    except:  # E722: do not use bare except
        pass
    
    return a + b

class myClass:  # N801: class names should use CapWords convention
    def __init__(self):
        self.data = dict()  # C408: unnecessary dict() call, use {}
    
    def method(self):
        return(self.data)  # unnecessary parentheses in return

# Trailing whitespace and missing newline at end
x = 1   
'''

# ═══════════════════════════════════════════════════════════════
# CÓDIGO "AFTER" — Corregido por Ruff
# ═══════════════════════════════════════════════════════════════

AFTER_CODE = '''
import json
import os
import sys


x = 1
y = [1, 2, 3]


def good_function(a, b, c):
    """Función corregida siguiendo las reglas de Ruff."""
    if a:
        pass
    if b is None:
        pass
    items = []
    for i in range(10):
        items.append(i)

    try:
        result = 1 / 0
    except ZeroDivisionError:
        pass

    return a + b


class MyClass:
    """Clase con nombre CapWords."""

    def __init__(self):
        self.data = {}

    def method(self):
        return self.data
'''

# ═══════════════════════════════════════════════════════════════
# CATÁLOGO DE REGLAS
# ═══════════════════════════════════════════════════════════════

RUFF_RULES: list[dict] = [
    {"code": "E401", "desc": "Multiple imports on one line", "fix": "Un import por línea"},
    {"code": "F401", "desc": "Module imported but unused", "fix": "Eliminar import no usado"},
    {"code": "F403", "desc": "Wildcard import", "fix": "Importar solo lo necesario"},
    {"code": "E225", "desc": "Missing whitespace around operator", "fix": "Espacios alrededor de ="},
    {"code": "E231", "desc": "Missing whitespace after comma", "fix": "Espacio después de ,"},
    {"code": "E712", "desc": "Comparison to True", "fix": "Usar 'if x:' en vez de 'if x == True'"},
    {"code": "E711", "desc": "Comparison to None", "fix": "Usar 'is None' en vez de '== None'"},
    {"code": "E741", "desc": "Ambiguous variable name", "fix": "Renombrar 'l' a 'items'"},
    {"code": "F841", "desc": "Local variable assigned but never used", "fix": "Eliminar variable"},
    {"code": "E722", "desc": "Bare except clause", "fix": "Especificar la excepción"},
    {"code": "N801", "desc": "Class name not CapWords", "fix": "myClass → MyClass"},
    {"code": "C408", "desc": "Unnecessary dict() call", "fix": "Usar {} en vez de dict()"},
]


def ejecutar_demo_y_tests() -> None:
    """Demo de las 15 reglas de Ruff."""

    print("=" * 70)
    print("E4.5 — DEMO: RUFF — ANÁLISIS ESTÁTICO Y FORMATEO")
    print("=" * 70)

    print(f"\n{'─' * 50}")
    print("Código BEFORE (con 15 problemas):")
    print(f"{'─' * 50}")
    for i, line in enumerate(BEFORE_CODE.strip().split("\n"), 1):
        print(f"  {i:3d} | {line}")

    print(f"\n{'─' * 50}")
    print("Reglas Ruff que se violan:")
    print(f"{'─' * 50}")
    for r in RUFF_RULES:
        print(f"  {r['code']:6s} {r['desc']:<40s} → {r['fix']}")

    print(f"\n{'─' * 50}")
    print("Código AFTER (corregido):")
    print(f"{'─' * 50}")
    for i, line in enumerate(AFTER_CODE.strip().split("\n"), 1):
        print(f"  {i:3d} | {line}")

    print(f"\n{'─' * 50}")
    print("Comandos Ruff para el alumno:")
    print(f"{'─' * 50}")
    print("  1. ruff check e4_5_ruff_before.py        → muestra errores")
    print("  2. ruff check --fix e4_5_ruff_before.py   → corrige automáticamente")
    print("  3. ruff format e4_5_ruff_before.py        → formatea el código")
    print("  4. ruff check --select ALL archivo.py     → todas las reglas")

    # Tests
    print(f"\n{'=' * 70}")
    print("TESTS:")
    print(f"{'=' * 70}")

    assert len(RUFF_RULES) >= 10
    print(f"  [PASS] Test 1: {len(RUFF_RULES)} reglas documentadas")

    assert "import os, sys" in BEFORE_CODE
    assert "import os" in AFTER_CODE and "import sys" in AFTER_CODE
    print("  [PASS] Test 2: E401 corregido (imports separados)")

    assert "import math" in BEFORE_CODE and "import math" not in AFTER_CODE
    print("  [PASS] Test 3: F401 corregido (import no usado eliminado)")

    assert "== True" in BEFORE_CODE and "== True" not in AFTER_CODE
    print("  [PASS] Test 4: E712 corregido (if a: en vez de if a == True)")

    assert "== None" in BEFORE_CODE and "is None" in AFTER_CODE
    print("  [PASS] Test 5: E711 corregido (is None)")

    assert "except:" in BEFORE_CODE and "except ZeroDivisionError" in AFTER_CODE
    print("  [PASS] Test 6: E722 corregido (bare except → ZeroDivisionError)")

    assert "myClass" in BEFORE_CODE and "MyClass" in AFTER_CODE
    print("  [PASS] Test 7: N801 corregido (MyClass)")

    assert "dict()" in BEFORE_CODE and "{}" in AFTER_CODE
    print("  [PASS] Test 8: C408 corregido (dict() → {})")

    print(f"\n  Todos los tests pasaron correctamente.")


if __name__ == "__main__":
    ejecutar_demo_y_tests()
