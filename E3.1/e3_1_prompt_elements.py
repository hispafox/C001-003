"""
E3.1 — Elementos del Prompt: Validador de Emails en 8 Iteraciones
===================================================================
Demuestra que cada elemento de un buen prompt mejora el resultado.
8 funciones de validación de email, cada una generada con un prompt
progresivamente mejor.

Uso: python e3_1_prompt_elements.py

Dependencias: Solo librería estándar.
"""

import re
import sys
from typing import Optional

__version__ = "1.0.0"

# ═══════════════════════════════════════════════════════════════
# LOS 8 PROMPTS Y SUS RESULTADOS
# ═══════════════════════════════════════════════════════════════

PROMPTS: dict[int, dict] = {
    1: {
        "elemento": "Solo acción",
        "prompt": "Valida un email.",
        "mejora": "Implementación mínima: solo comprueba que haya @",
    },
    2: {
        "elemento": "+ Contexto",
        "prompt": "En un sistema de registro de usuarios, valida un email.",
        "mejora": "Añade verificación de que hay dominio después del @",
    },
    3: {
        "elemento": "+ Rol",
        "prompt": "Eres un desarrollador senior backend. En un sistema de registro de usuarios, valida un email.",
        "mejora": "Regex más completa, separa local part y dominio",
    },
    4: {
        "elemento": "+ Público",
        "prompt": "...para un equipo de juniors que mantendrá el código.",
        "mejora": "Misma lógica pero con comentarios explicativos",
    },
    5: {
        "elemento": "+ Restricciones",
        "prompt": "...sin dependencias externas, solo re. Máximo 30 líneas.",
        "mejora": "Código más conciso, sin imports innecesarios",
    },
    6: {
        "elemento": "+ Ejemplos",
        "prompt": "...válidos: user@domain.com, name+tag@sub.domain.org. Inválidos: @domain.com, user@, user@.com",
        "mejora": "Cubre todos los edge cases de los ejemplos dados",
    },
    7: {
        "elemento": "+ Tono",
        "prompt": "...docstrings Google Style, nombres descriptivos en español.",
        "mejora": "Documentación profesional, misma lógica que v6",
    },
    8: {
        "elemento": "Prompt completo (8 elementos)",
        "prompt": "Todos los elementos combinados en un prompt perfecto.",
        "mejora": "Versión production-ready: dict con valid, errors, checks_passed",
    },
}


# ═══════════════════════════════════════════════════════════════
# V1: SOLO ACCIÓN — "Valida un email"
# ═══════════════════════════════════════════════════════════════

def validate_v1(email: str) -> bool:
    """Validación mínima: solo comprueba que hay @."""
    return "@" in email


# ═══════════════════════════════════════════════════════════════
# V2: + CONTEXTO — "En un sistema de registro..."
# ═══════════════════════════════════════════════════════════════

def validate_v2(email: str) -> bool:
    """Validación con contexto: @ + dominio con punto."""
    if "@" not in email:
        return False
    parts = email.split("@")
    if len(parts) != 2:
        return False
    return "." in parts[1]


# ═══════════════════════════════════════════════════════════════
# V3: + ROL — "Eres un desarrollador senior..."
# ═══════════════════════════════════════════════════════════════

def validate_v3(email: str) -> bool:
    """Validación con regex básica de desarrollador senior."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


# ═══════════════════════════════════════════════════════════════
# V4: + PÚBLICO — "...para juniors que mantendrán el código"
# ═══════════════════════════════════════════════════════════════

def validate_v4(email: str) -> bool:
    """Validación con comentarios para equipo junior.

    La regex se descompone en partes para facilitar su comprensión:
    - Parte local: letras, números, puntos, guiones, +, _, %
    - Símbolo @: exactamente uno
    - Dominio: letras, números, puntos, guiones
    - TLD: al menos 2 letras (com, org, es, etc.)
    """
    # Parte antes del @: al menos 1 carácter alfanumérico o especial permitido
    local_part = r'[a-zA-Z0-9._%+-]+'
    # Separador: exactamente un @
    separator = r'@'
    # Dominio: letras, números, puntos y guiones
    domain = r'[a-zA-Z0-9.-]+'
    # TLD: al menos 2 letras (com, org, es, etc.)
    tld = r'\.[a-zA-Z]{2,}'
    # Regex completa
    pattern = f'^{local_part}{separator}{domain}{tld}$'
    return bool(re.match(pattern, email))


# ═══════════════════════════════════════════════════════════════
# V5: + RESTRICCIONES — "solo re, máximo 30 líneas"
# ═══════════════════════════════════════════════════════════════

def validate_v5(email: str) -> bool:
    """Validación concisa cumpliendo restricción de brevedad."""
    if not email or len(email) > 254:
        return False
    return bool(re.match(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?'
        r'(\.[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}$',
        email
    ))


# ═══════════════════════════════════════════════════════════════
# V6: + EJEMPLOS — edge cases explícitos
# ═══════════════════════════════════════════════════════════════

def validate_v6(email: str) -> bool:
    """Validación que cubre todos los edge cases de los ejemplos.

    Válidos: user@domain.com, name+tag@sub.domain.org
    Inválidos: @domain.com, user@, user@.com, user@domain..com
    """
    if not email or len(email) > 254:
        return False
    if email.count("@") != 1:
        return False

    local, domain = email.split("@")

    # Local part checks
    if not local:
        return False
    if local.startswith(".") or local.endswith("."):
        return False
    if ".." in local:
        return False

    # Domain checks
    if not domain:
        return False
    if domain.startswith(".") or domain.startswith("-"):
        return False
    if ".." in domain:
        return False

    # Full regex
    return bool(re.match(
        r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?'
        r'(\.[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?)*\.[a-zA-Z]{2,}$',
        email
    ))


# ═══════════════════════════════════════════════════════════════
# V7: + TONO — docstrings Google Style, nombres descriptivos
# ═══════════════════════════════════════════════════════════════

def validate_v7(email: str) -> bool:
    """Valida una dirección de email según RFC 5321 simplificado.

    Implementa validación de formato de email sin dependencias externas.
    No verifica existencia del dominio ni del buzón.

    Args:
        email: Dirección de email a validar.

    Returns:
        True si el formato es válido, False en caso contrario.

    Examples:
        >>> validate_v7("usuario@dominio.com")
        True
        >>> validate_v7("@sinlocal.com")
        False
    """
    if not email or not isinstance(email, str) or len(email) > 254:
        return False
    if email.count("@") != 1:
        return False

    parte_local, dominio = email.split("@")

    if not parte_local or len(parte_local) > 64:
        return False
    if parte_local.startswith(".") or parte_local.endswith(".") or ".." in parte_local:
        return False

    if not dominio or dominio.startswith(".") or dominio.startswith("-") or ".." in dominio:
        return False

    patron_completo = (
        r'^[a-zA-Z0-9._%+-]+@'
        r'[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?'
        r'(\.[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?)*'
        r'\.[a-zA-Z]{2,}$'
    )
    return bool(re.match(patron_completo, email))


# ═══════════════════════════════════════════════════════════════
# V8: PROMPT COMPLETO — Production-ready
# ═══════════════════════════════════════════════════════════════

def validate_v8(email: str) -> dict:
    """Valida email con informe detallado (prompt completo, 8 elementos).

    Combina: contexto (registro), rol (senior), público (juniors),
    restricciones (solo re), ejemplos (edge cases), tono (Google Style),
    longitud (respuesta estructurada).

    Args:
        email: Dirección de email a validar.

    Returns:
        Diccionario con:
            - valid (bool): Si el email es válido.
            - email (str): El email evaluado.
            - errors (list[str]): Lista de errores encontrados.
            - checks_passed (list[str]): Verificaciones superadas.
    """
    errors: list[str] = []
    checks_passed: list[str] = []

    # Check 1: Tipo y longitud básica
    if not email or not isinstance(email, str):
        return {"valid": False, "email": str(email), "errors": ["Email vacío o tipo inválido"], "checks_passed": []}

    email = email.strip()

    if len(email) > 254:
        errors.append("Excede longitud máxima de 254 caracteres")
    else:
        checks_passed.append("Longitud válida")

    # Check 2: Exactamente un @
    if email.count("@") != 1:
        errors.append("Debe contener exactamente un símbolo @")
        return {"valid": False, "email": email, "errors": errors, "checks_passed": checks_passed}

    checks_passed.append("Contiene exactamente un @")

    parte_local, dominio = email.split("@")

    # Check 3: Parte local
    if not parte_local:
        errors.append("Falta la parte local (antes del @)")
    elif len(parte_local) > 64:
        errors.append("Parte local excede 64 caracteres")
    elif parte_local.startswith(".") or parte_local.endswith("."):
        errors.append("Parte local no puede empezar o terminar con punto")
    elif ".." in parte_local:
        errors.append("Parte local no puede contener puntos consecutivos")
    else:
        checks_passed.append("Parte local válida")

    # Check 4: Dominio
    if not dominio:
        errors.append("Falta el dominio (después del @)")
    elif dominio.startswith(".") or dominio.startswith("-"):
        errors.append("Dominio no puede empezar con punto o guión")
    elif ".." in dominio:
        errors.append("Dominio no puede contener puntos consecutivos")
    elif "." not in dominio:
        errors.append("Dominio debe contener al menos un punto (TLD)")
    else:
        checks_passed.append("Dominio válido")

    # Check 5: Regex completa
    patron = (
        r'^[a-zA-Z0-9._%+-]+@'
        r'[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?'
        r'(\.[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?)*'
        r'\.[a-zA-Z]{2,}$'
    )
    if not errors and not re.match(patron, email):
        errors.append("Formato general no coincide con el patrón RFC 5321")
    elif not errors:
        checks_passed.append("Formato RFC 5321 válido")

    return {
        "valid": len(errors) == 0,
        "email": email,
        "errors": errors,
        "checks_passed": checks_passed,
    }


# ═══════════════════════════════════════════════════════════════
# PROMPT ANALYZER
# ═══════════════════════════════════════════════════════════════

class PromptAnalyzer:
    """Analiza la progresión de las 8 versiones de validación."""

    VALIDATORS = [validate_v1, validate_v2, validate_v3, validate_v4,
                  validate_v5, validate_v6, validate_v7, validate_v8]

    TEST_EMAILS: list[tuple[str, bool]] = [
        # Válidos
        ("user@domain.com", True),
        ("name+tag@sub.domain.org", True),
        ("test.user@empresa.es", True),
        ("admin123@mail-server.com", True),
        ("a@b.co", True),
        # Inválidos
        ("@domain.com", False),
        ("user@", False),
        ("user@.com", False),
        ("user@domain..com", False),
        ("no-arroba.com", False),
    ]

    def compare_all(self) -> list[dict]:
        """Compara las 8 versiones con los 10 emails de test.

        Returns:
            Lista de dicts con version, elemento, aciertos, total, porcentaje.
        """
        results: list[dict] = []

        for i, validator in enumerate(self.VALIDATORS, 1):
            aciertos: int = 0
            for email, expected in self.TEST_EMAILS:
                if i == 8:
                    result = validator(email)
                    actual = result["valid"]
                else:
                    actual = validator(email)
                if actual == expected:
                    aciertos += 1

            results.append({
                "version": i,
                "elemento": PROMPTS[i]["elemento"],
                "aciertos": aciertos,
                "total": len(self.TEST_EMAILS),
                "porcentaje": round(aciertos / len(self.TEST_EMAILS) * 100),
            })

        return results

    def get_prompt_for_version(self, version: int) -> str:
        """Devuelve el prompt usado para una versión."""
        return PROMPTS.get(version, {}).get("prompt", "Versión no encontrada")


# ═══════════════════════════════════════════════════════════════
# DEMO Y TESTS
# ═══════════════════════════════════════════════════════════════

def ejecutar_demo_y_tests() -> None:
    """Ejecuta demo comparativa y tests."""

    print("=" * 70)
    print("E3.1 — DEMO: ELEMENTOS DEL PROMPT (8 iteraciones)")
    print("=" * 70)

    analyzer = PromptAnalyzer()
    results = analyzer.compare_all()

    print(f"\n{'─' * 60}")
    print(f"  {'Versión':<12} {'Elemento':<28} {'Aciertos':>10}")
    print(f"{'─' * 60}")

    for r in results:
        bar = "█" * (r["aciertos"]) + "░" * (r["total"] - r["aciertos"])
        marker = " ✅" if r["aciertos"] == r["total"] else ""
        print(f"  v{r['version']:<10} {r['elemento']:<28} {r['aciertos']:>2}/{r['total']} {bar}{marker}")

    print(f"{'─' * 60}")

    # Mostrar prompts
    print(f"\n{'─' * 60}")
    print("DETALLE DE CADA ELEMENTO:")
    print(f"{'─' * 60}")
    for i in range(1, 9):
        info = PROMPTS[i]
        print(f"\n  v{i} — {info['elemento']}:")
        print(f"    Prompt: \"{info['prompt'][:70]}{'...' if len(info['prompt']) > 70 else ''}\"")
        print(f"    Mejora: {info['mejora']}")

    # Ejemplo detallado v8
    print(f"\n{'─' * 60}")
    print("EJEMPLO DETALLADO v8 (prompt completo):")
    print(f"{'─' * 60}")

    for email, expected in [("user+tag@sub.domain.org", True), ("user@domain..com", False), ("@sinlocal.com", False)]:
        r = validate_v8(email)
        icon = "✅" if r["valid"] == expected else "❌"
        print(f"\n  {icon} {email}")
        print(f"    Válido: {r['valid']}")
        if r["checks_passed"]:
            print(f"    Checks: {', '.join(r['checks_passed'])}")
        if r["errors"]:
            print(f"    Errores: {', '.join(r['errors'])}")

    # ═══════════════════════════════════════════════════════
    # TESTS
    # ═══════════════════════════════════════════════════════
    print(f"\n{'=' * 70}")
    print("TESTS:")
    print(f"{'=' * 70}")

    # Test 1: v1 acepta básico
    assert validate_v1("user@domain.com") is True
    print("  [PASS] Test 1: v1 acepta 'user@domain.com'")

    # Test 2: v1 falla con edge case
    assert validate_v1("user@.com") is True  # v1 es demasiado simple, acepta todo con @
    print("  [PASS] Test 2: v1 acepta 'user@.com' (demasiado simple)")

    # Test 3: v6 rechaza user@.com
    assert validate_v6("user@.com") is False
    print("  [PASS] Test 3: v6 rechaza 'user@.com' (los ejemplos lo cubren)")

    # Test 4: v6 rechaza puntos consecutivos
    assert validate_v6("user@domain..com") is False
    print("  [PASS] Test 4: v6 rechaza 'user@domain..com'")

    # Test 5: v8 acepta email complejo válido
    r = validate_v8("user+tag@sub.domain.org")
    assert r["valid"] is True
    print("  [PASS] Test 5: v8 acepta 'user+tag@sub.domain.org'")

    # Test 6: v8 rechaza sin local part
    r = validate_v8("@domain.com")
    assert r["valid"] is False
    print("  [PASS] Test 6: v8 rechaza '@domain.com'")

    # Test 7: v8 devuelve dict con claves correctas
    r = validate_v8("test@test.com")
    assert "valid" in r and "email" in r and "errors" in r and "checks_passed" in r
    print("  [PASS] Test 7: v8 devuelve dict con claves correctas")

    # Test 8: errors vacía para email válido
    r = validate_v8("good@email.com")
    assert r["valid"] is True and len(r["errors"]) == 0
    print("  [PASS] Test 8: v8 errors vacía para email válido")

    # Test 9: errors con mensaje para inválido
    r = validate_v8("@bad.com")
    assert r["valid"] is False and len(r["errors"]) > 0
    print("  [PASS] Test 9: v8 errors contiene mensaje para inválido")

    # Test 10: compare_all devuelve 8 versiones
    analyzer = PromptAnalyzer()
    results = analyzer.compare_all()
    assert len(results) == 8
    assert all("version" in r and "aciertos" in r for r in results)
    print("  [PASS] Test 10: compare_all devuelve 8 versiones")

    print(f"\n  Todos los tests pasaron correctamente.")


if __name__ == "__main__":
    ejecutar_demo_y_tests()
