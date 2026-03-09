"""
E4.3 — Copilot: Depuración de Código con Bugs Intencionados
==============================================================
8 funciones con bugs intencionados. El alumno usa Copilot Agente
para detectar y corregir cada bug. Incluye versión corregida.

Uso: python e4_3_debug_challenge.py

Dependencias: Solo librería estándar.
"""

__version__ = "1.0.0"

# ═══════════════════════════════════════════════════════════════
# CÓDIGO CON BUGS (el alumno da esto a Copilot para depurar)
# ═══════════════════════════════════════════════════════════════

def buggy_fibonacci(n: int) -> list[int]:
    """Bug 1: Off-by-one error — genera n-1 números en vez de n."""
    if n <= 0:
        return []
    fib = [0, 1]
    for i in range(2, n):  # BUG: debería ser range(2, n) solo si n>2, y luego retornar fib[:n]
        fib.append(fib[i-1] + fib[i-2])
    return fib  # BUG: no trunca a n elementos si n==1

def buggy_binary_search(arr: list, target) -> int:
    """Bug 2: Bucle infinito cuando target no existe."""
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid  # BUG: debería ser mid + 1
        else:
            right = mid  # BUG: debería ser mid - 1
    return -1

def buggy_flatten(nested: list) -> list:
    """Bug 3: No maneja diccionarios dentro de la lista."""
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(buggy_flatten(item))
        # BUG: no maneja tuplas ni otros iterables
        else:
            result.append(item)
    return result

def buggy_remove_duplicates(lst: list) -> list:
    """Bug 4: Modifica la lista mientras itera (comportamiento impredecible)."""
    for i in range(len(lst)):
        for j in range(i + 1, len(lst)):
            if j < len(lst) and lst[i] == lst[j]:
                lst.pop(j)  # BUG: modifica lista durante iteración
    return lst

def buggy_celsius_to_fahrenheit(temps: list[float]) -> list[float]:
    """Bug 5: Fórmula incorrecta."""
    return [t * 9/5 + 23 for t in temps]  # BUG: debería ser +32, no +23

def buggy_word_count(text: str) -> dict[str, int]:
    """Bug 6: No maneja puntuación ni mayúsculas."""
    words = text.split()
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1  # BUG: "Hello" y "hello." cuentan como diferentes
    return counts

def buggy_matrix_multiply(a: list, b: list) -> list:
    """Bug 7: Índices invertidos en la multiplicación."""
    rows_a, cols_b = len(a), len(b[0])
    cols_a = len(a[0])
    result = [[0] * cols_b for _ in range(rows_a)]
    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):
                result[i][j] += a[i][k] * b[j][k]  # BUG: debería ser b[k][j]
    return result

def buggy_is_palindrome(s: str) -> bool:
    """Bug 8: No ignora espacios ni mayúsculas."""
    return s == s[::-1]  # BUG: "A man" != "nam A" pero debería limpiar primero


# ═══════════════════════════════════════════════════════════════
# CÓDIGO CORREGIDO (referencia del formador)
# ═══════════════════════════════════════════════════════════════

def fixed_fibonacci(n: int) -> list[int]:
    """Fibonacci corregido: genera exactamente n números."""
    if n <= 0:
        return []
    if n == 1:
        return [0]
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    return fib[:n]

def fixed_binary_search(arr: list, target) -> int:
    """Binary search corregido: mid±1 para evitar bucle infinito."""
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

def fixed_flatten(nested: list) -> list:
    """Flatten corregido: maneja listas y tuplas."""
    result = []
    for item in nested:
        if isinstance(item, (list, tuple)):
            result.extend(fixed_flatten(item))
        else:
            result.append(item)
    return result

def fixed_remove_duplicates(lst: list) -> list:
    """Remove duplicates corregido: no modifica durante iteración."""
    seen = []
    for item in lst:
        if item not in seen:
            seen.append(item)
    return seen

def fixed_celsius_to_fahrenheit(temps: list[float]) -> list[float]:
    """Conversión corregida: +32, no +23."""
    return [t * 9/5 + 32 for t in temps]

def fixed_word_count(text: str) -> dict[str, int]:
    """Word count corregido: normaliza a minúsculas y elimina puntuación."""
    import re
    words = re.findall(r'[a-záéíóúüñ]+', text.lower())
    counts: dict[str, int] = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    return counts

def fixed_matrix_multiply(a: list, b: list) -> list:
    """Matrix multiply corregido: b[k][j] en vez de b[j][k]."""
    rows_a, cols_b = len(a), len(b[0])
    cols_a = len(a[0])
    result = [[0] * cols_b for _ in range(rows_a)]
    for i in range(rows_a):
        for j in range(cols_b):
            for k in range(cols_a):
                result[i][j] += a[i][k] * b[k][j]
    return result

def fixed_is_palindrome(s: str) -> bool:
    """Palindrome corregido: ignora espacios, puntuación y mayúsculas."""
    cleaned = ''.join(c.lower() for c in s if c.isalnum())
    return cleaned == cleaned[::-1]


# ═══════════════════════════════════════════════════════════════
# DEMO Y TESTS
# ═══════════════════════════════════════════════════════════════

def ejecutar_demo_y_tests() -> None:
    """Compara versiones buggy vs fixed."""

    print("=" * 70)
    print("E4.3 — DEMO: 8 BUGS PARA DEPURAR CON COPILOT")
    print("=" * 70)

    bugs = [
        ("Fibonacci(5)", lambda: buggy_fibonacci(5), lambda: fixed_fibonacci(5), [0,1,1,2,3]),
        ("Fibonacci(1)", lambda: buggy_fibonacci(1), lambda: fixed_fibonacci(1), [0]),
        ("BinarySearch(7)", lambda: buggy_binary_search([1,3,5,7,9],7), lambda: fixed_binary_search([1,3,5,7,9],7), 3),
        ("Flatten([[1,[2]],3])", lambda: buggy_flatten([[1,[2]],3,(4,5)]), lambda: fixed_flatten([[1,[2]],3,(4,5)]), [1,2,3,4,5]),
        ("RemoveDups", lambda: buggy_remove_duplicates([1,2,2,3,3,3][:]), lambda: fixed_remove_duplicates([1,2,2,3,3,3]), [1,2,3]),
        ("Celsius(0,100)", lambda: buggy_celsius_to_fahrenheit([0,100]), lambda: fixed_celsius_to_fahrenheit([0,100]), [32.0,212.0]),
        ("WordCount", lambda: buggy_word_count("Hello hello world."), lambda: fixed_word_count("Hello hello world."), {"hello":2,"world":1}),
        ("Palindrome", lambda: buggy_is_palindrome("A man a plan a canal Panama"), lambda: fixed_is_palindrome("A man a plan a canal Panama"), True),
    ]

    for name, buggy_fn, fixed_fn, expected in bugs:
        try:
            buggy_result = buggy_fn()
        except Exception as e:
            buggy_result = f"ERROR: {e}"
        fixed_result = fixed_fn()

        buggy_ok = buggy_result == expected
        fixed_ok = fixed_result == expected
        b_icon = "✅" if buggy_ok else "❌"
        f_icon = "✅" if fixed_ok else "⚠️"

        print(f"\n  {name}:")
        print(f"    Buggy:    {b_icon} {buggy_result}")
        print(f"    Fixed:    {f_icon} {fixed_result}")
        print(f"    Expected: {expected}")

    # ═══════════════════════════════════════════════════════
    # TESTS (solo versiones corregidas)
    # ═══════════════════════════════════════════════════════
    print(f"\n{'=' * 70}")
    print("TESTS (versiones corregidas):")
    print(f"{'=' * 70}")

    assert fixed_fibonacci(5) == [0,1,1,2,3]
    assert fixed_fibonacci(1) == [0]
    assert fixed_fibonacci(0) == []
    print("  [PASS] Test 1-3: Fibonacci corregido")

    assert fixed_binary_search([1,3,5,7,9], 7) == 3
    assert fixed_binary_search([1,3,5,7,9], 4) == -1
    print("  [PASS] Test 4-5: BinarySearch corregido")

    assert fixed_flatten([[1,[2]],3,(4,5)]) == [1,2,3,4,5]
    print("  [PASS] Test 6: Flatten corregido")

    assert fixed_remove_duplicates([1,2,2,3,3,3]) == [1,2,3]
    print("  [PASS] Test 7: RemoveDups corregido")

    assert fixed_celsius_to_fahrenheit([0,100]) == [32.0, 212.0]
    print("  [PASS] Test 8: Celsius corregido")

    wc = fixed_word_count("Hello hello WORLD world.")
    assert wc["hello"] == 2 and wc["world"] == 2
    print("  [PASS] Test 9: WordCount corregido")

    assert fixed_matrix_multiply([[1,2],[3,4]], [[5,6],[7,8]]) == [[19,22],[43,50]]
    print("  [PASS] Test 10: MatrixMultiply corregido")

    assert fixed_is_palindrome("A man a plan a canal Panama") is True
    assert fixed_is_palindrome("hello") is False
    print("  [PASS] Test 11-12: Palindrome corregido")

    print(f"\n  Todos los tests pasaron correctamente.")


if __name__ == "__main__":
    ejecutar_demo_y_tests()
