"""
E4.6 — Sphinx + JSDoc: Documentación Automática
==================================================
Módulo Python documentado con docstrings Sphinx-compatible.
El alumno genera docs HTML con: sphinx-quickstart + make html.
Incluye ejemplo JSDoc equivalente en JavaScript.

Uso: python e4_6_sphinx_jsdoc.py

Dependencias: Solo librería estándar. Sphinx para generar docs.
"""

__version__ = "1.0.0"


class ShoppingCart:
    """Carrito de compras con descuentos y impuestos.

    Ejemplo de documentación lista para Sphinx (reStructuredText).
    El alumno ejecuta ``sphinx-apidoc`` sobre este módulo.

    :param tax_rate: Tasa de impuesto (0.0 a 1.0), por defecto 0.21 (IVA España).
    :type tax_rate: float

    Example:
        .. code-block:: python

            cart = ShoppingCart(tax_rate=0.21)
            cart.add_item("Laptop", 999.99, quantity=1)
            cart.add_item("Mouse", 29.99, quantity=2)
            print(cart.get_total())  # Total con IVA

    .. note::
        Este módulo es educativo. No usar en producción sin validación adicional.
    """

    def __init__(self, tax_rate: float = 0.21) -> None:
        self.tax_rate: float = tax_rate
        self._items: list[dict] = []
        self._discount_code: str | None = None
        self._discount_pct: float = 0.0

    def add_item(self, name: str, price: float, quantity: int = 1) -> dict:
        """Añade un producto al carrito.

        :param name: Nombre del producto.
        :param price: Precio unitario en euros.
        :param quantity: Cantidad (mínimo 1).
        :returns: Diccionario con los datos del item añadido.
        :rtype: dict
        :raises ValueError: Si el precio es negativo o la cantidad < 1.

        Example:
            >>> cart = ShoppingCart()
            >>> item = cart.add_item("Teclado", 49.99, quantity=2)
            >>> item['subtotal']
            99.98
        """
        if price < 0:
            raise ValueError(f"Precio no puede ser negativo: {price}")
        if quantity < 1:
            raise ValueError(f"Cantidad debe ser al menos 1: {quantity}")

        item: dict = {
            "name": name,
            "price": round(price, 2),
            "quantity": quantity,
            "subtotal": round(price * quantity, 2),
        }
        self._items.append(item)
        return item

    def remove_item(self, name: str) -> bool:
        """Elimina un producto del carrito por nombre.

        :param name: Nombre del producto a eliminar.
        :returns: True si se eliminó, False si no existía.
        :rtype: bool
        """
        before = len(self._items)
        self._items = [i for i in self._items if i["name"] != name]
        return len(self._items) < before

    def apply_discount(self, code: str, percentage: float) -> None:
        """Aplica un código de descuento.

        :param code: Código de descuento (ej: "SAVE10").
        :param percentage: Porcentaje de descuento (0-100).
        :raises ValueError: Si el porcentaje no está en [0, 100].
        """
        if not 0 <= percentage <= 100:
            raise ValueError(f"Porcentaje debe estar entre 0 y 100: {percentage}")
        self._discount_code = code
        self._discount_pct = percentage / 100

    def get_subtotal(self) -> float:
        """Calcula el subtotal (sin impuestos ni descuentos).

        :returns: Suma de todos los subtotales de items.
        :rtype: float
        """
        return round(sum(i["subtotal"] for i in self._items), 2)

    def get_discount_amount(self) -> float:
        """Calcula la cantidad de descuento aplicada.

        :returns: Cantidad de descuento en euros.
        :rtype: float
        """
        return round(self.get_subtotal() * self._discount_pct, 2)

    def get_tax_amount(self) -> float:
        """Calcula el impuesto sobre el total con descuento.

        :returns: Cantidad de impuesto en euros.
        :rtype: float
        """
        taxable = self.get_subtotal() - self.get_discount_amount()
        return round(taxable * self.tax_rate, 2)

    def get_total(self) -> float:
        """Calcula el total final (subtotal - descuento + impuesto).

        :returns: Total a pagar en euros.
        :rtype: float
        """
        subtotal = self.get_subtotal()
        discount = self.get_discount_amount()
        tax = self.get_tax_amount()
        return round(subtotal - discount + tax, 2)

    def get_summary(self) -> dict:
        """Genera resumen completo del carrito.

        :returns: Diccionario con items, subtotal, discount, tax, total.
        :rtype: dict
        """
        return {
            "items": [i.copy() for i in self._items],
            "item_count": sum(i["quantity"] for i in self._items),
            "subtotal": self.get_subtotal(),
            "discount_code": self._discount_code,
            "discount_amount": self.get_discount_amount(),
            "tax_rate": self.tax_rate,
            "tax_amount": self.get_tax_amount(),
            "total": self.get_total(),
        }


# ═══════════════════════════════════════════════════════════════
# EJEMPLO JSDoc EQUIVALENTE (para referencia)
# ═══════════════════════════════════════════════════════════════

JSDOC_EXAMPLE = '''
/**
 * Carrito de compras con descuentos e impuestos.
 * Ejemplo de documentación JSDoc para generación automática.
 *
 * @example
 * const cart = new ShoppingCart(0.21);
 * cart.addItem("Laptop", 999.99, 1);
 * console.log(cart.getTotal());
 */
class ShoppingCart {
    /**
     * Crea una nueva instancia del carrito.
     * @param {number} [taxRate=0.21] - Tasa de impuesto (0.0 a 1.0).
     */
    constructor(taxRate = 0.21) {
        /** @type {number} */
        this.taxRate = taxRate;
        /** @type {Array<Object>} */
        this._items = [];
        /** @type {?string} */
        this._discountCode = null;
        /** @type {number} */
        this._discountPct = 0.0;
    }

    /**
     * Añade un producto al carrito.
     * @param {string} name - Nombre del producto.
     * @param {number} price - Precio unitario en euros.
     * @param {number} [quantity=1] - Cantidad (mínimo 1).
     * @returns {Object} Item añadido con subtotal calculado.
     * @throws {Error} Si precio < 0 o cantidad < 1.
     */
    addItem(name, price, quantity = 1) {
        if (price < 0) throw new Error(`Precio negativo: ${price}`);
        if (quantity < 1) throw new Error(`Cantidad inválida: ${quantity}`);
        const item = { name, price: +price.toFixed(2), quantity, subtotal: +(price * quantity).toFixed(2) };
        this._items.push(item);
        return item;
    }

    /**
     * Calcula el total final (subtotal - descuento + impuesto).
     * @returns {number} Total a pagar en euros.
     */
    getTotal() {
        const subtotal = this._items.reduce((s, i) => s + i.subtotal, 0);
        const discount = subtotal * this._discountPct;
        const tax = (subtotal - discount) * this.taxRate;
        return +(subtotal - discount + tax).toFixed(2);
    }
}
'''


# ═══════════════════════════════════════════════════════════════
# DEMO Y TESTS
# ═══════════════════════════════════════════════════════════════

def ejecutar_demo_y_tests() -> None:
    """Demo del carrito + comparación Sphinx vs JSDoc."""

    print("=" * 70)
    print("E4.6 — DEMO: SPHINX + JSDOC")
    print("=" * 70)

    cart = ShoppingCart(tax_rate=0.21)
    cart.add_item("Laptop", 999.99, quantity=1)
    cart.add_item("Mouse", 29.99, quantity=2)
    cart.add_item("Teclado", 49.99, quantity=1)
    cart.apply_discount("SAVE10", 10)

    summary = cart.get_summary()
    print(f"\n  Items: {summary['item_count']}")
    print(f"  Subtotal: €{summary['subtotal']}")
    print(f"  Descuento ({summary['discount_code']}): -€{summary['discount_amount']}")
    print(f"  IVA ({summary['tax_rate']*100:.0f}%): +€{summary['tax_amount']}")
    print(f"  Total: €{summary['total']}")

    print(f"\n{'─' * 50}")
    print("Comandos Sphinx para generar docs:")
    print(f"{'─' * 50}")
    print("  1. pip install sphinx")
    print("  2. sphinx-quickstart docs/")
    print("  3. Editar docs/conf.py: extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon']")
    print("  4. sphinx-apidoc -o docs/ .")
    print("  5. cd docs && make html")
    print("  6. Abrir docs/_build/html/index.html")

    print(f"\n{'─' * 50}")
    print("Comandos JSDoc para generar docs:")
    print(f"{'─' * 50}")
    print("  1. npm install -g jsdoc")
    print("  2. jsdoc shopping_cart.js -d docs/")
    print("  3. Abrir docs/index.html")

    print(f"\n{'─' * 50}")
    print("Ejemplo JSDoc equivalente:")
    print(f"{'─' * 50}")
    for line in JSDOC_EXAMPLE.strip().split("\n")[:20]:
        print(f"  {line}")
    print("  ...")

    # Tests
    print(f"\n{'=' * 70}")
    print("TESTS:")
    print(f"{'=' * 70}")

    c = ShoppingCart()
    c.add_item("A", 10.00, 2)
    assert c.get_subtotal() == 20.00
    print("  [PASS] Test 1: Subtotal correcto")

    c.apply_discount("TEST", 50)
    assert c.get_discount_amount() == 10.00
    print("  [PASS] Test 2: Descuento 50% = €10")

    assert c.get_tax_amount() == round(10.00 * 0.21, 2)
    print("  [PASS] Test 3: IVA sobre total con descuento")

    assert c.get_total() == round(20 - 10 + 10 * 0.21, 2)
    print(f"  [PASS] Test 4: Total = €{c.get_total()}")

    assert c.remove_item("A") is True
    assert c.remove_item("NoExiste") is False
    print("  [PASS] Test 5: remove_item()")

    try:
        c.add_item("Bad", -5)
        assert False
    except ValueError:
        pass
    print("  [PASS] Test 6: Precio negativo → ValueError")

    s = ShoppingCart().get_summary()
    assert "items" in s and "total" in s
    print("  [PASS] Test 7: get_summary() devuelve dict completo")

    assert "class ShoppingCart" in JSDOC_EXAMPLE
    assert "@param" in JSDOC_EXAMPLE
    assert "@returns" in JSDOC_EXAMPLE
    print("  [PASS] Test 8: JSDoc example contiene tags correctos")

    print(f"\n  Todos los tests pasaron correctamente.")


if __name__ == "__main__":
    ejecutar_demo_y_tests()
