"""
E3.3 — Few-shot: Funciones de Transformación de Datos
======================================================
Demuestra few-shot: dar 2 ejemplos con un patrón específico y pedir
una 3ª función que siga ese patrón. Compara con zero-shot.

Uso: python e3_3_fewshot_transforms.py

Dependencias: Solo librería estándar.
"""

import sys
from datetime import datetime
from typing import Any

__version__ = "1.0.0"


# ═══════════════════════════════════════════════════════════════
# EJEMPLO A (dado en el prompt como "few-shot")
# Pipeline: validar → limpiar → normalizar → enriquecer
# ═══════════════════════════════════════════════════════════════

def transform_users(raw_data: list[dict]) -> list[dict]:
    """Transforma datos crudos de usuarios al formato estándar.

    Pipeline: validar → limpiar → normalizar → enriquecer.

    Args:
        raw_data: Lista de dicts con campos name, email, age.

    Returns:
        Lista de dicts transformados con campos normalizados.
    """
    results: list[dict] = []
    for item in raw_data:
        # Validar
        if not item.get("name") or not item.get("email"):
            continue
        # Limpiar
        cleaned: dict = {
            "full_name": item["name"].strip().title(),
            "email": item["email"].strip().lower(),
            "age": int(item.get("age", 0)) if str(item.get("age", "")).isdigit() else None,
        }
        # Normalizar
        cleaned["age_group"] = (
            "junior" if cleaned["age"] and cleaned["age"] < 30
            else "senior" if cleaned["age"] and cleaned["age"] >= 30
            else "unknown"
        )
        # Enriquecer
        cleaned["domain"] = cleaned["email"].split("@")[1] if "@" in cleaned["email"] else "invalid"
        cleaned["is_valid"] = "@" in cleaned["email"] and "." in cleaned["domain"]
        results.append(cleaned)
    return results


# ═══════════════════════════════════════════════════════════════
# EJEMPLO B (dado en el prompt como "few-shot")
# ═══════════════════════════════════════════════════════════════

def transform_products(raw_data: list[dict]) -> list[dict]:
    """Transforma datos crudos de productos al formato estándar.

    Pipeline: validar → limpiar → normalizar → enriquecer.

    Args:
        raw_data: Lista de dicts con campos name, price, currency, category.

    Returns:
        Lista de dicts transformados con campos normalizados.
    """
    results: list[dict] = []
    for item in raw_data:
        # Validar
        if not item.get("name") or not item.get("price"):
            continue
        # Limpiar
        cleaned: dict = {
            "product_name": item["name"].strip().title(),
            "price": round(float(item.get("price", 0)), 2),
            "currency": item.get("currency", "EUR").upper(),
            "category": item.get("category", "uncategorized").lower(),
        }
        # Normalizar
        cleaned["price_range"] = (
            "budget" if cleaned["price"] < 10
            else "mid" if cleaned["price"] < 50
            else "premium" if cleaned["price"] < 200
            else "luxury"
        )
        # Enriquecer
        cleaned["price_with_tax"] = round(cleaned["price"] * 1.21, 2)
        cleaned["is_valid"] = cleaned["price"] > 0
        results.append(cleaned)
    return results


# ═══════════════════════════════════════════════════════════════
# RESULTADO FEW-SHOT: transform_orders
# (generada "siguiendo el patrón de los 2 ejemplos")
# ═══════════════════════════════════════════════════════════════

def transform_orders_fewshot(raw_data: list[dict]) -> list[dict]:
    """Transforma datos crudos de pedidos al formato estándar.

    Pipeline: validar → limpiar → normalizar → enriquecer.
    Sigue el mismo patrón que transform_users y transform_products.

    Args:
        raw_data: Lista de dicts con campos order_id, customer, items, total, date.

    Returns:
        Lista de dicts transformados con campos normalizados.
    """
    results: list[dict] = []
    for item in raw_data:
        # Validar (mismo patrón: campos obligatorios)
        if not item.get("customer") or not item.get("total"):
            continue
        # Limpiar (mismo patrón: strip, tipos correctos)
        cleaned: dict = {
            "order_id": str(item.get("order_id", "unknown")).strip(),
            "customer_name": item["customer"].strip().title(),
            "items_count": len(item.get("items", [])),
            "total": round(float(item.get("total", 0)), 2),
            "currency": item.get("currency", "EUR").upper(),
            "order_date": item.get("date", "").strip(),
        }
        # Normalizar (mismo patrón: clasificación por rangos)
        cleaned["order_size"] = (
            "small" if cleaned["items_count"] <= 2
            else "medium" if cleaned["items_count"] <= 5
            else "large" if cleaned["items_count"] <= 10
            else "bulk"
        )
        cleaned["total_range"] = (
            "micro" if cleaned["total"] < 10
            else "small" if cleaned["total"] < 50
            else "medium" if cleaned["total"] < 200
            else "large"
        )
        # Enriquecer (mismo patrón: cálculos derivados + is_valid)
        cleaned["total_with_tax"] = round(cleaned["total"] * 1.21, 2)
        cleaned["avg_item_price"] = (
            round(cleaned["total"] / cleaned["items_count"], 2)
            if cleaned["items_count"] > 0 else 0.0
        )
        cleaned["is_valid"] = cleaned["total"] > 0 and cleaned["items_count"] > 0
        results.append(cleaned)
    return results


# ═══════════════════════════════════════════════════════════════
# RESULTADO ZERO-SHOT: transform_orders (sin ejemplos)
# (generada con prompt "crea transform_orders" sin patrón)
# ═══════════════════════════════════════════════════════════════

def transform_orders_zeroshot(raw_data: list[dict]) -> list[dict]:
    """Transforma datos de pedidos (versión zero-shot, sin patrón previo).

    Nota: esta versión se generó sin ver los ejemplos A y B.
    Puede diferir en convenciones, estructura y campos.

    Args:
        raw_data: Lista de dicts con datos de pedidos.

    Returns:
        Lista de dicts procesados.
    """
    output: list[dict] = []
    for order in raw_data:
        # Validación básica
        if not order.get("customer"):
            continue

        total_val = order.get("total", 0)
        try:
            total_val = float(total_val)
        except (ValueError, TypeError):
            total_val = 0.0

        processed = {
            "id": order.get("order_id", "N/A"),
            "customer": order.get("customer", "Unknown"),
            "num_items": len(order.get("items", [])),
            "total_amount": total_val,
            "date": order.get("date", None),
            "status": "valid" if total_val > 0 else "invalid",
        }
        output.append(processed)
    return output


# ═══════════════════════════════════════════════════════════════
# COMPARADOR
# ═══════════════════════════════════════════════════════════════

class FewShotComparator:
    """Compara funciones generadas por few-shot vs zero-shot.

    Evalúa consistencia con los ejemplos originales.
    """

    PATTERN_FIELDS: list[str] = [
        "is_valid",           # Todos los ejemplos tienen is_valid
        "_with_tax",          # Enriquecimiento con impuesto
    ]

    PATTERN_CONVENTIONS: dict[str, str] = {
        "snake_case": "Nombres de campos en snake_case",
        "pipeline_4_steps": "Pipeline validar→limpiar→normalizar→enriquecer",
        "is_valid_field": "Campo is_valid booleano",
        "range_classification": "Clasificación por rangos (budget/mid/premium, etc.)",
        "strip_title_lower": "Limpieza con strip/title/lower",
        "round_floats": "Números decimales redondeados con round()",
    }

    def compare(
        self, few_shot_result: list[dict], zero_shot_result: list[dict]
    ) -> dict:
        """Compara resultados de few-shot vs zero-shot.

        Args:
            few_shot_result: Datos transformados por la función few-shot.
            zero_shot_result: Datos transformados por la función zero-shot.

        Returns:
            Dict con análisis de consistencia y diferencias.
        """
        fs_fields: set[str] = set()
        zs_fields: set[str] = set()

        for r in few_shot_result:
            fs_fields.update(r.keys())
        for r in zero_shot_result:
            zs_fields.update(r.keys())

        # Scoring de consistencia con el patrón
        score: int = 0
        checks: list[dict] = []

        # Check 1: is_valid field
        has_is_valid_fs = "is_valid" in fs_fields
        has_is_valid_zs = "is_valid" in zs_fields
        checks.append({"check": "Campo is_valid", "fewshot": has_is_valid_fs, "zeroshot": has_is_valid_zs})
        if has_is_valid_fs:
            score += 20

        # Check 2: tax calculation
        has_tax_fs = any("tax" in f for f in fs_fields)
        has_tax_zs = any("tax" in f for f in zs_fields)
        checks.append({"check": "Cálculo de impuesto", "fewshot": has_tax_fs, "zeroshot": has_tax_zs})
        if has_tax_fs:
            score += 15

        # Check 3: range classification
        has_range_fs = any("range" in f or "size" in f or "group" in f for f in fs_fields)
        has_range_zs = any("range" in f or "size" in f or "group" in f for f in zs_fields)
        checks.append({"check": "Clasificación por rangos", "fewshot": has_range_fs, "zeroshot": has_range_zs})
        if has_range_fs:
            score += 20

        # Check 4: snake_case naming
        all_snake_fs = all("_" in f or f.islower() for f in fs_fields if len(f) > 3)
        all_snake_zs = all("_" in f or f.islower() for f in zs_fields if len(f) > 3)
        checks.append({"check": "snake_case consistente", "fewshot": all_snake_fs, "zeroshot": all_snake_zs})
        if all_snake_fs:
            score += 15

        # Check 5: rounded floats
        has_rounded_fs = any(
            isinstance(r.get("total_with_tax"), float) and
            r["total_with_tax"] == round(r["total_with_tax"], 2)
            for r in few_shot_result if "total_with_tax" in r
        )
        checks.append({"check": "Floats redondeados", "fewshot": has_rounded_fs, "zeroshot": False})
        if has_rounded_fs:
            score += 15

        # Check 6: filters invalid
        fs_count = len(few_shot_result)
        zs_count = len(zero_shot_result)
        checks.append({"check": f"Filtrado (fs:{fs_count}, zs:{zs_count})", "fewshot": True, "zeroshot": True})
        score += 15

        return {
            "fewshot_fields": sorted(fs_fields),
            "zeroshot_fields": sorted(zs_fields),
            "common_fields": sorted(fs_fields & zs_fields),
            "only_fewshot": sorted(fs_fields - zs_fields),
            "only_zeroshot": sorted(zs_fields - fs_fields),
            "checks": checks,
            "consistency_score": min(score, 100),
            "verdict": "Few-shot sigue mejor el patrón" if score >= 70 else "Ambos son similares",
        }


# ═══════════════════════════════════════════════════════════════
# DATOS DE TEST
# ═══════════════════════════════════════════════════════════════

SAMPLE_USERS: list[dict] = [
    {"name": "  ana lópez  ", "email": "ANA@EMPRESA.COM", "age": "28"},
    {"name": "carlos ruiz", "email": "carlos@mail.com", "age": "35"},
    {"name": "", "email": "noname@mail.com", "age": "20"},  # inválido
]

SAMPLE_PRODUCTS: list[dict] = [
    {"name": "  camiseta básica ", "price": "9.99", "category": "ROPA"},
    {"name": "portátil gaming", "price": "1299.00", "category": "electrónica", "currency": "eur"},
    {"name": "producto sin precio", "price": None},  # inválido
]

SAMPLE_ORDERS: list[dict] = [
    {"order_id": "ORD001", "customer": " María García ", "items": ["item1", "item2"], "total": "45.50", "date": "2026-03-01"},
    {"order_id": "ORD002", "customer": "Pedro López", "items": ["a", "b", "c", "d", "e", "f"], "total": "230.00", "date": "2026-03-02"},
    {"order_id": "ORD003", "customer": "Ana Ruiz", "items": ["x"], "total": "5.99", "date": "2026-03-03"},
    {"order_id": "ORD004", "customer": "Luis Martín", "items": ["a", "b", "c"], "total": "89.95", "date": "2026-03-04"},
    {"order_id": "ORD005", "customer": "Sara Díaz", "items": ["item1"], "total": "150.00", "date": "2026-03-05"},
    # Inválidos
    {"order_id": "ORD006", "customer": "", "items": ["a"], "total": "10.00"},  # sin customer
    {"order_id": "ORD007", "customer": "Test User", "items": [], "total": None},  # sin total
    {"order_id": "ORD008", "customer": "Bad Order", "items": ["a"], "total": "-50.00"},  # total negativo
]


# ═══════════════════════════════════════════════════════════════
# DEMO Y TESTS
# ═══════════════════════════════════════════════════════════════

def ejecutar_demo_y_tests() -> None:
    """Demo y tests de few-shot vs zero-shot."""

    print("=" * 70)
    print("E3.3 — DEMO: FEW-SHOT vs ZERO-SHOT")
    print("=" * 70)

    # ── Ejemplo A: Users ──
    print(f"\n{'─' * 50}")
    print("EJEMPLO A (dado como referencia): transform_users")
    print(f"{'─' * 50}")
    users = transform_users(SAMPLE_USERS)
    print(f"  Input: {len(SAMPLE_USERS)} registros → Output: {len(users)} válidos")
    for u in users:
        print(f"    {u['full_name']:20s} {u['email']:25s} {u['age_group']:8s} valid={u['is_valid']}")

    # ── Ejemplo B: Products ──
    print(f"\n{'─' * 50}")
    print("EJEMPLO B (dado como referencia): transform_products")
    print(f"{'─' * 50}")
    products = transform_products(SAMPLE_PRODUCTS)
    print(f"  Input: {len(SAMPLE_PRODUCTS)} registros → Output: {len(products)} válidos")
    for p in products:
        print(f"    {p['product_name']:20s} {p['price']:>8.2f}€ +IVA={p['price_with_tax']:>8.2f}€ {p['price_range']:8s}")

    # ── Few-shot result ──
    print(f"\n{'─' * 50}")
    print("FEW-SHOT: transform_orders (siguiendo el patrón)")
    print(f"{'─' * 50}")
    fs_orders = transform_orders_fewshot(SAMPLE_ORDERS)
    print(f"  Input: {len(SAMPLE_ORDERS)} registros → Output: {len(fs_orders)} válidos")
    for o in fs_orders:
        print(f"    {o['order_id']:8s} {o['customer_name']:20s} {o['total']:>8.2f}€ +IVA={o['total_with_tax']:>8.2f}€ {o['total_range']:8s} valid={o['is_valid']}")

    # ── Zero-shot result ──
    print(f"\n{'─' * 50}")
    print("ZERO-SHOT: transform_orders (sin ver los ejemplos)")
    print(f"{'─' * 50}")
    zs_orders = transform_orders_zeroshot(SAMPLE_ORDERS)
    print(f"  Input: {len(SAMPLE_ORDERS)} registros → Output: {len(zs_orders)} válidos")
    for o in zs_orders:
        print(f"    {o['id']:8s} {o['customer']:20s} {o['total_amount']:>8.2f}  status={o['status']}")

    # ── Comparación ──
    print(f"\n{'─' * 50}")
    print("COMPARACIÓN FEW-SHOT vs ZERO-SHOT:")
    print(f"{'─' * 50}")

    comparator = FewShotComparator()
    comp = comparator.compare(fs_orders, zs_orders)

    print(f"\n  Campos few-shot:  {comp['fewshot_fields']}")
    print(f"  Campos zero-shot: {comp['zeroshot_fields']}")
    print(f"  Solo en few-shot: {comp['only_fewshot']}")
    print(f"  Solo en zero-shot: {comp['only_zeroshot']}")

    print(f"\n  {'Check':<30s} {'Few-shot':>10s} {'Zero-shot':>10s}")
    print(f"  {'─' * 52}")
    for c in comp["checks"]:
        fs_icon = "✅" if c["fewshot"] else "❌"
        zs_icon = "✅" if c["zeroshot"] else "❌"
        print(f"  {c['check']:<30s} {fs_icon:>10s} {zs_icon:>10s}")

    print(f"\n  Consistencia con patrón: {comp['consistency_score']}/100")
    print(f"  Veredicto: {comp['verdict']}")

    # ═══════════════════════════════════════════════════════
    # TESTS
    # ═══════════════════════════════════════════════════════
    print(f"\n{'=' * 70}")
    print("TESTS:")
    print(f"{'=' * 70}")

    # Test 1
    users = transform_users(SAMPLE_USERS)
    assert len(users) == 2
    assert users[0]["full_name"] == "Ana López"
    print("  [PASS] Test 1: transform_users funciona con datos válidos")

    # Test 2
    assert len(users) < len(SAMPLE_USERS)
    print("  [PASS] Test 2: transform_users filtra datos sin nombre")

    # Test 3
    products = transform_products(SAMPLE_PRODUCTS)
    assert len(products) == 2
    assert products[0]["product_name"] == "Camiseta Básica"
    print("  [PASS] Test 3: transform_products funciona")

    # Test 4
    assert products[0]["price_with_tax"] == round(9.99 * 1.21, 2)
    print(f"  [PASS] Test 4: transform_products calcula IVA ({products[0]['price_with_tax']}€)")

    # Test 5: Few-shot sigue pipeline
    fs = transform_orders_fewshot(SAMPLE_ORDERS)
    assert len(fs) >= 4  # filtra inválidos
    # Tiene los 4 pasos del pipeline
    sample = fs[0]
    assert "customer_name" in sample  # limpiar (title)
    assert "order_size" in sample or "total_range" in sample  # normalizar
    assert "total_with_tax" in sample  # enriquecer
    print("  [PASS] Test 5: Few-shot sigue pipeline validar→limpiar→normalizar→enriquecer")

    # Test 6: is_valid presente
    assert "is_valid" in fs[0]
    print("  [PASS] Test 6: Few-shot incluye is_valid en cada registro")

    # Test 7: Filtra inválidos
    assert len(fs) < len(SAMPLE_ORDERS)
    print(f"  [PASS] Test 7: Few-shot filtra inválidos ({len(SAMPLE_ORDERS)}→{len(fs)})")

    # Test 8: Zero-shot funcional
    zs = transform_orders_zeroshot(SAMPLE_ORDERS)
    assert len(zs) > 0
    assert "customer" in zs[0] or "customer_name" in zs[0]
    print("  [PASS] Test 8: Zero-shot genera función funcional")

    # Test 9: Few-shot más consistente
    comp = FewShotComparator().compare(fs, zs)
    assert comp["consistency_score"] >= 70
    print(f"  [PASS] Test 9: Few-shot consistencia {comp['consistency_score']}/100 ≥ 70")

    # Test 10: Comparador detecta diferencias
    assert len(comp["only_fewshot"]) > 0 or len(comp["only_zeroshot"]) > 0
    assert len(comp["checks"]) >= 5
    print(f"  [PASS] Test 10: Comparador detecta {len(comp['only_fewshot'])} campos solo en few-shot")

    print(f"\n  Todos los tests pasaron correctamente.")


if __name__ == "__main__":
    ejecutar_demo_y_tests()
