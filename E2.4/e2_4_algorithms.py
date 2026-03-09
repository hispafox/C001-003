"""
E2.4 — Razonamiento: 3 Problemas Algorítmicos Resueltos por IA
================================================================
Tres clases que resuelven problemas algorítmicos clásicos, demostrando
dónde la IA acierta y dónde puede fallar en razonamiento.

Uso: python e2_4_algorithms.py

Dependencias: Solo librería estándar.
"""

import sys
from typing import Optional

__version__ = "1.0.0"


# ═══════════════════════════════════════════════════════════════
# PROBLEMA 1: LAS N REINAS (Backtracking)
# ═══════════════════════════════════════════════════════════════

class EightQueens:
    """Resuelve el problema de las N Reinas con backtracking.

    Encuentra todas las formas de colocar N reinas en un tablero NxN
    de forma que ninguna reina ataque a otra.

    Examples:
        >>> eq = EightQueens()
        >>> eq.count_solutions(4)
        2
    """

    def solve(self, n: int = 8) -> list[list[int]]:
        """Encuentra todas las soluciones para N reinas.

        Args:
            n: Tamaño del tablero (por defecto 8).

        Returns:
            Lista de soluciones. Cada solución es una lista de N enteros
            donde el índice es la fila y el valor es la columna.

        Raises:
            ValueError: Si n < 1.
        """
        if n < 1:
            raise ValueError("n debe ser al menos 1")

        solutions: list[list[int]] = []
        self._backtrack([], n, solutions)
        return solutions

    def _backtrack(self, current: list[int], n: int, solutions: list[list[int]]) -> None:
        """Backtracking recursivo para encontrar soluciones."""
        if len(current) == n:
            solutions.append(current[:])
            return

        row: int = len(current)
        for col in range(n):
            if self._is_safe(current, row, col):
                current.append(col)
                self._backtrack(current, n, solutions)
                current.pop()

    def _is_safe(self, current: list[int], row: int, col: int) -> bool:
        """Verifica si es seguro colocar una reina en (row, col)."""
        for r, c in enumerate(current):
            if c == col:
                return False
            if abs(r - row) == abs(c - col):
                return False
        return True

    def count_solutions(self, n: int = 8) -> int:
        """Cuenta el número total de soluciones para N reinas.

        Args:
            n: Tamaño del tablero.

        Returns:
            Número de soluciones.
        """
        return len(self.solve(n))

    def is_valid(self, solution: list[int]) -> bool:
        """Verifica si una solución es válida.

        Args:
            solution: Lista de columnas por fila.

        Returns:
            True si ninguna reina ataca a otra.
        """
        n: int = len(solution)
        for i in range(n):
            for j in range(i + 1, n):
                if solution[i] == solution[j]:
                    return False
                if abs(i - j) == abs(solution[i] - solution[j]):
                    return False
        return True

    def print_board(self, solution: list[int]) -> str:
        """Genera representación visual del tablero.

        Args:
            solution: Lista de columnas por fila.

        Returns:
            String con el tablero usando ♛ y ·
        """
        n: int = len(solution)
        lines: list[str] = []
        for row in range(n):
            line: str = ""
            for col in range(n):
                if solution[row] == col:
                    line += "♛ "
                else:
                    line += "· "
            lines.append(line.rstrip())
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
# PROBLEMA 2: EVALUADOR DE EXPRESIONES (Shunting-Yard)
# ═══════════════════════════════════════════════════════════════

class ExpressionEvaluator:
    """Evaluador de expresiones matemáticas con algoritmo Shunting-Yard.

    Soporta: +, -, *, /, paréntesis, números decimales y negativos.
    NO usa eval() ni compile().

    Examples:
        >>> ev = ExpressionEvaluator()
        >>> ev.evaluate("2 + 3")
        5.0
    """

    PRECEDENCE: dict[str, int] = {"+": 1, "-": 1, "*": 2, "/": 2}

    def tokenize(self, expression: str) -> list:
        """Divide una expresión en tokens numéricos y operadores.

        Args:
            expression: Expresión matemática como string.

        Returns:
            Lista de tokens (float para números, str para operadores/paréntesis).

        Raises:
            ValueError: Si la expresión está vacía o tiene caracteres inválidos.
        """
        expression = expression.strip()
        if not expression:
            raise ValueError("La expresión no puede estar vacía")

        tokens: list = []
        i: int = 0
        prev_token = None

        while i < len(expression):
            ch: str = expression[i]

            if ch == " ":
                i += 1
                continue

            # Número (incluyendo negativos al inicio o después de operador/paréntesis)
            if (ch.isdigit() or ch == "." or
                    (ch == "-" and (prev_token is None or prev_token in "(-+*/"))):
                num_str: str = ""
                if ch == "-":
                    num_str = "-"
                    i += 1
                while i < len(expression) and (expression[i].isdigit() or expression[i] == "."):
                    num_str += expression[i]
                    i += 1
                if num_str == "-" or num_str == "." or num_str == "-.":
                    raise ValueError(f"Número inválido en posición {i}")
                tokens.append(float(num_str))
                prev_token = "num"
                continue

            if ch in "+-*/":
                tokens.append(ch)
                prev_token = ch
                i += 1
                continue

            if ch == "(":
                tokens.append("(")
                prev_token = "("
                i += 1
                continue

            if ch == ")":
                tokens.append(")")
                prev_token = ")"
                i += 1
                continue

            raise ValueError(f"Carácter inválido '{ch}' en posición {i}")

        return tokens

    def evaluate(self, expression: str) -> float:
        """Evalúa una expresión matemática con Shunting-Yard.

        Args:
            expression: Expresión como "3 + 4 * 2 / (1 - 5)".

        Returns:
            Resultado como float.

        Raises:
            ValueError: Si la expresión es inválida.
            ZeroDivisionError: Si hay división por cero.
        """
        tokens: list = self.tokenize(expression)
        output_queue: list[float] = []
        operator_stack: list[str] = []

        for token in tokens:
            if isinstance(token, float):
                output_queue.append(token)

            elif token in self.PRECEDENCE:
                while (operator_stack and
                       operator_stack[-1] != "(" and
                       operator_stack[-1] in self.PRECEDENCE and
                       self.PRECEDENCE[operator_stack[-1]] >= self.PRECEDENCE[token]):
                    self._apply_operator(output_queue, operator_stack.pop())
                operator_stack.append(token)

            elif token == "(":
                operator_stack.append(token)

            elif token == ")":
                while operator_stack and operator_stack[-1] != "(":
                    self._apply_operator(output_queue, operator_stack.pop())
                if not operator_stack:
                    raise ValueError("Paréntesis no balanceados: ) sin ( correspondiente")
                operator_stack.pop()  # Remove "("

        while operator_stack:
            op: str = operator_stack.pop()
            if op == "(":
                raise ValueError("Paréntesis no balanceados: ( sin ) correspondiente")
            self._apply_operator(output_queue, op)

        if len(output_queue) != 1:
            raise ValueError("Expresión malformada")

        return output_queue[0]

    def _apply_operator(self, stack: list[float], op: str) -> None:
        """Aplica un operador a los dos valores superiores del stack."""
        if len(stack) < 2:
            raise ValueError("Expresión malformada: operador sin operandos suficientes")
        b: float = stack.pop()
        a: float = stack.pop()
        if op == "+":
            stack.append(a + b)
        elif op == "-":
            stack.append(a - b)
        elif op == "*":
            stack.append(a * b)
        elif op == "/":
            if b == 0:
                raise ZeroDivisionError("División por cero")
            stack.append(a / b)


# ═══════════════════════════════════════════════════════════════
# PROBLEMA 3: CALCULADORA BAYESIANA
# ═══════════════════════════════════════════════════════════════

class BayesCalculator:
    """Calculadora de probabilidad bayesiana.

    Aplica el teorema de Bayes: P(A|B) = P(B|A) * P(A) / P(B)

    Examples:
        >>> bc = BayesCalculator()
        >>> bc.calculate(0.5, 0.8, 0.5)
        0.8
    """

    def calculate(self, prior: float, likelihood: float, evidence: float) -> float:
        """Aplica el teorema de Bayes básico.

        Args:
            prior: P(A) - probabilidad a priori.
            likelihood: P(B|A) - verosimilitud.
            evidence: P(B) - evidencia.

        Returns:
            P(A|B) - probabilidad posterior.

        Raises:
            ValueError: Si las probabilidades no están en [0, 1] o evidence es 0.
        """
        self._validate_probability(prior, "prior")
        self._validate_probability(likelihood, "likelihood")
        self._validate_probability(evidence, "evidence")

        if evidence == 0:
            raise ValueError("evidence (P(B)) no puede ser 0")

        posterior: float = (likelihood * prior) / evidence
        return round(posterior, 6)

    def calculate_with_complement(
        self, prior: float, true_positive: float, false_positive: float
    ) -> float:
        """Calcula probabilidad posterior usando sensibilidad y falsos positivos.

        Caso típico: ¿Probabilidad de enfermedad dado test positivo?
        P(enfermo|test+) = P(test+|enfermo) * P(enfermo) /
                           [P(test+|enfermo) * P(enfermo) + P(test+|sano) * P(sano)]

        Args:
            prior: Prevalencia P(enfermo).
            true_positive: Sensibilidad P(test+|enfermo).
            false_positive: Tasa de falsos positivos P(test+|sano).

        Returns:
            Probabilidad posterior P(enfermo|test+).
        """
        self._validate_probability(prior, "prior")
        self._validate_probability(true_positive, "true_positive")
        self._validate_probability(false_positive, "false_positive")

        # P(B) = P(B|A)*P(A) + P(B|¬A)*P(¬A)
        evidence: float = true_positive * prior + false_positive * (1 - prior)

        if evidence == 0:
            return 0.0

        posterior: float = (true_positive * prior) / evidence
        return round(posterior, 6)

    def explain(self, prior: float, likelihood: float, evidence: float) -> str:
        """Devuelve explicación paso a paso del cálculo.

        Args:
            prior: P(A).
            likelihood: P(B|A).
            evidence: P(B).

        Returns:
            String con explicación en español.
        """
        posterior: float = self.calculate(prior, likelihood, evidence)

        lines: list[str] = [
            "Teorema de Bayes: P(A|B) = P(B|A) × P(A) / P(B)",
            "",
            f"  P(A)   = {prior}     (probabilidad a priori)",
            f"  P(B|A) = {likelihood}     (verosimilitud)",
            f"  P(B)   = {evidence}     (evidencia)",
            "",
            f"  P(A|B) = {likelihood} × {prior} / {evidence}",
            f"         = {likelihood * prior} / {evidence}",
            f"         = {posterior}",
            f"         = {posterior * 100:.2f}%",
        ]
        return "\n".join(lines)

    def _validate_probability(self, value: float, name: str) -> None:
        """Valida que un valor sea una probabilidad válida [0, 1]."""
        if not isinstance(value, (int, float)):
            raise TypeError(f"{name} debe ser un número")
        if value < 0 or value > 1:
            raise ValueError(f"{name} debe estar entre 0 y 1, recibido: {value}")


# ═══════════════════════════════════════════════════════════════
# DEMO Y TESTS
# ═══════════════════════════════════════════════════════════════

def ejecutar_demo_y_tests() -> None:
    """Ejecuta demos y tests de los 3 problemas."""

    print("=" * 70)
    print("E2.4 — DEMO: 3 PROBLEMAS ALGORÍTMICOS")
    print("=" * 70)

    # ── Problema 1: 8 Reinas ──
    print(f"\n{'─' * 50}")
    print("PROBLEMA 1: LAS N REINAS (Backtracking)")
    print(f"{'─' * 50}")

    eq = EightQueens()
    solutions_4 = eq.solve(4)
    solutions_8 = eq.solve(8)

    print(f"\n  N=4: {len(solutions_4)} soluciones")
    print(f"  N=8: {len(solutions_8)} soluciones")

    print(f"\n  Primera solución para N=8:")
    board: str = eq.print_board(solutions_8[0])
    for line in board.split("\n"):
        print(f"    {line}")

    # ── Problema 2: Expresiones ──
    print(f"\n{'─' * 50}")
    print("PROBLEMA 2: EVALUADOR DE EXPRESIONES (Shunting-Yard)")
    print(f"{'─' * 50}")

    ev = ExpressionEvaluator()
    expressions = [
        "2 + 3",
        "3 + 4 * 2 / (1 - 5)",
        "(2 + 3) * (4 - 1)",
        "10 / 3",
        "3.5 * 2 + 1.5",
    ]

    print()
    for expr in expressions:
        result: float = ev.evaluate(expr)
        print(f"  {expr:30s} = {result}")

    # ── Problema 3: Bayes ──
    print(f"\n{'─' * 50}")
    print("PROBLEMA 3: CALCULADORA BAYESIANA")
    print(f"{'─' * 50}")

    bc = BayesCalculator()

    print(f"\n  Ejemplo médico:")
    print(f"  Enfermedad con prevalencia del 1%")
    print(f"  Test con sensibilidad del 99% (true positive)")
    print(f"  Tasa de falsos positivos del 5%")

    prob = bc.calculate_with_complement(
        prior=0.01,
        true_positive=0.99,
        false_positive=0.05,
    )
    print(f"\n  P(enfermo | test positivo) = {prob:.4f} = {prob * 100:.2f}%")
    print(f"\n  ¡Sorpresa! Solo ~{prob * 100:.0f}% de los test positivos están")
    print(f"  realmente enfermos. La intuición humana falla aquí.")

    print(f"\n  Explicación paso a paso:")
    explanation = bc.explain(prior=0.5, likelihood=0.8, evidence=0.5)
    for line in explanation.split("\n"):
        print(f"    {line}")

    # ═══════════════════════════════════════════════════════
    # TESTS
    # ═══════════════════════════════════════════════════════
    print(f"\n{'=' * 70}")
    print("TESTS:")
    print(f"{'=' * 70}")

    eq = EightQueens()
    ev = ExpressionEvaluator()
    bc = BayesCalculator()

    # Test 1
    assert eq.count_solutions(4) == 2
    print("  [PASS] Test 1: N=4 tiene 2 soluciones")

    # Test 2
    assert eq.count_solutions(8) == 92
    print("  [PASS] Test 2: N=8 tiene 92 soluciones")

    # Test 3
    valid_sol = eq.solve(8)[0]
    assert eq.is_valid(valid_sol)
    print("  [PASS] Test 3: is_valid confirma solución correcta")

    # Test 4
    assert not eq.is_valid([0, 0, 0, 0, 0, 0, 0, 0])  # Todas en misma columna
    print("  [PASS] Test 4: is_valid rechaza solución inválida")

    # Test 5
    assert ev.evaluate("2 + 3") == 5.0
    print("  [PASS] Test 5: 2 + 3 = 5.0")

    # Test 6
    assert ev.evaluate("3 + 4 * 2 / (1 - 5)") == 1.0
    print("  [PASS] Test 6: 3 + 4 * 2 / (1 - 5) = 1.0")

    # Test 7
    assert ev.evaluate("3.5 * 2") == 7.0
    print("  [PASS] Test 7: 3.5 * 2 = 7.0")

    # Test 8
    try:
        ev.evaluate("(2 + 3")
        assert False
    except ValueError:
        pass
    print("  [PASS] Test 8: Paréntesis no balanceados → ValueError")

    # Test 9
    assert bc.calculate(0.5, 0.8, 0.5) == 0.8
    print("  [PASS] Test 9: Bayes básico P(A|B) = 0.8")

    # Test 10
    result = bc.calculate_with_complement(0.01, 0.99, 0.05)
    assert abs(result - 0.1667) < 0.01, f"Esperado ~0.167, obtenido {result}"
    print(f"  [PASS] Test 10: Bayes médico ≈ 16.7% (obtenido {result * 100:.1f}%)")

    # Test 11
    try:
        bc.calculate(1.5, 0.8, 0.5)
        assert False
    except ValueError:
        pass
    print("  [PASS] Test 11: Probabilidad > 1 → ValueError")

    # Test 12
    try:
        ev.evaluate("")
        assert False
    except ValueError:
        pass
    print("  [PASS] Test 12: Expresión vacía → ValueError")

    print(f"\n  Todos los tests pasaron correctamente.")


if __name__ == "__main__":
    ejecutar_demo_y_tests()
