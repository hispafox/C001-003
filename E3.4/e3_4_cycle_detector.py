"""
E3.4 — Cadena de Pensamiento: Detector de Ciclos en Grafos
=============================================================
Compara un prompt directo vs Chain of Thought para detectar ciclos.
El prompt CoT produce una solución más completa y robusta.

Uso: python e3_4_cycle_detector.py

Dependencias: Solo librería estándar.
"""

from typing import Optional

__version__ = "1.0.0"


# ═══════════════════════════════════════════════════════════════
# CLASE GRAPH
# ═══════════════════════════════════════════════════════════════

class Graph:
    """Grafo dirigido representado como lista de adyacencia.

    Examples:
        >>> g = Graph()
        >>> g.add_edge("A", "B")
        >>> g.get_neighbors("A")
        ['B']
    """

    def __init__(self) -> None:
        self._adj: dict[str, list[str]] = {}

    def add_node(self, node: str) -> None:
        """Añade un nodo al grafo."""
        if node not in self._adj:
            self._adj[node] = []

    def add_edge(self, from_node: str, to_node: str) -> None:
        """Añade una arista dirigida."""
        self.add_node(from_node)
        self.add_node(to_node)
        if to_node not in self._adj[from_node]:
            self._adj[from_node].append(to_node)

    def get_neighbors(self, node: str) -> list[str]:
        """Devuelve los vecinos de un nodo."""
        return self._adj.get(node, [])

    def get_all_nodes(self) -> set[str]:
        """Devuelve todos los nodos."""
        return set(self._adj.keys())

    @classmethod
    def from_dict(cls, adj_dict: dict[str, list[str]]) -> "Graph":
        """Crea un grafo desde un diccionario de adyacencia."""
        g = cls()
        for node, neighbors in adj_dict.items():
            g.add_node(node)
            for neighbor in neighbors:
                g.add_edge(node, neighbor)
        return g

    def visualize(self) -> str:
        """Representación ASCII del grafo."""
        lines: list[str] = []
        for node in sorted(self._adj.keys()):
            neighbors = self._adj[node]
            if neighbors:
                arrows = ", ".join(f"{node}→{n}" for n in neighbors)
                lines.append(f"  {node}: {arrows}")
            else:
                lines.append(f"  {node}: (sin aristas)")
        return "\n".join(lines) if lines else "  (grafo vacío)"


# ═══════════════════════════════════════════════════════════════
# VERSIÓN A: PROMPT DIRECTO (sin CoT)
# "Detecta ciclos en un grafo dirigido"
# ═══════════════════════════════════════════════════════════════

def detect_cycle_direct(graph: Graph) -> bool:
    """Detecta si hay ciclo en un grafo dirigido (versión directa).

    Generada con prompt simple sin Chain of Thought.
    Solo devuelve True/False, sin información adicional.

    Args:
        graph: Grafo dirigido.

    Returns:
        True si hay al menos un ciclo.
    """
    visited: set[str] = set()
    rec_stack: set[str] = set()

    def _dfs(node: str) -> bool:
        visited.add(node)
        rec_stack.add(node)
        for neighbor in graph.get_neighbors(node):
            if neighbor not in visited:
                if _dfs(neighbor):
                    return True
            elif neighbor in rec_stack:
                return True
        rec_stack.discard(node)
        return False

    for node in graph.get_all_nodes():
        if node not in visited:
            if _dfs(node):
                return True
    return False


# ═══════════════════════════════════════════════════════════════
# VERSIÓN B: PROMPT CON CHAIN OF THOUGHT
# "Piensa paso a paso: algoritmo, estados, edge cases, info extra"
# ═══════════════════════════════════════════════════════════════

class CycleDetector:
    """Detector de ciclos con DFS y colores (versión Chain of Thought).

    Razonamiento paso a paso (CoT):
    1. Algoritmo: DFS con 3 colores (WHITE/GRAY/BLACK)
    2. Estados: WHITE=no visitado, GRAY=en proceso, BLACK=completado
    3. Ciclo: cuando DFS encuentra nodo GRAY (ancestro en el camino)
    4. Edge cases: vacío, aislado, self-loop, múltiples componentes
    5. Info extra: nodos del ciclo, camino, topological sort
    """

    WHITE: int = 0  # No visitado
    GRAY: int = 1   # En la pila de recursión (en proceso)
    BLACK: int = 2  # Completado

    def detect(self, graph: Graph) -> dict:
        """Detecta ciclos con información detallada.

        Args:
            graph: Grafo dirigido.

        Returns:
            Dict con has_cycle, cycle_nodes, cycle_path, algorithm.
        """
        nodes = graph.get_all_nodes()
        if not nodes:
            return {
                "has_cycle": False, "cycle_nodes": [],
                "cycle_path": [], "algorithm": "DFS 3-color",
            }

        color: dict[str, int] = {n: self.WHITE for n in nodes}
        parent: dict[str, Optional[str]] = {n: None for n in nodes}
        cycle_path: list[str] = []

        def _dfs(node: str) -> bool:
            color[node] = self.GRAY
            for neighbor in graph.get_neighbors(node):
                if color.get(neighbor, self.WHITE) == self.GRAY:
                    # Ciclo encontrado: reconstruir camino
                    cycle_path.clear()
                    cycle_path.append(neighbor)
                    current = node
                    while current != neighbor:
                        cycle_path.append(current)
                        current = parent.get(current, neighbor)
                        if current is None:
                            break
                    cycle_path.append(neighbor)
                    cycle_path.reverse()
                    return True
                if color.get(neighbor, self.WHITE) == self.WHITE:
                    parent[neighbor] = node
                    if _dfs(neighbor):
                        return True
            color[node] = self.BLACK
            return False

        for node in sorted(nodes):
            if color[node] == self.WHITE:
                if _dfs(node):
                    return {
                        "has_cycle": True,
                        "cycle_nodes": list(set(cycle_path)),
                        "cycle_path": cycle_path,
                        "algorithm": "DFS 3-color (WHITE/GRAY/BLACK)",
                    }

        return {
            "has_cycle": False, "cycle_nodes": [],
            "cycle_path": [], "algorithm": "DFS 3-color (WHITE/GRAY/BLACK)",
        }

    def find_all_cycles(self, graph: Graph) -> list[list[str]]:
        """Encuentra todos los ciclos simples en el grafo.

        Args:
            graph: Grafo dirigido.

        Returns:
            Lista de ciclos, cada uno como lista de nodos.
        """
        nodes = sorted(graph.get_all_nodes())
        cycles: list[list[str]] = []
        visited_global: set[str] = set()

        for start in nodes:
            visited: set[str] = set()
            stack: list[tuple[str, list[str]]] = [(start, [start])]

            while stack:
                node, path = stack.pop()
                for neighbor in graph.get_neighbors(node):
                    if neighbor == start and len(path) > 1:
                        cycle = path + [start]
                        cycle_key = tuple(sorted(set(cycle)))
                        if cycle_key not in visited_global:
                            cycles.append(cycle)
                            visited_global.add(cycle_key)
                    elif neighbor not in visited and neighbor not in path:
                        visited.add(neighbor)
                        stack.append((neighbor, path + [neighbor]))

        return cycles

    def topological_sort(self, graph: Graph) -> Optional[list[str]]:
        """Ordenación topológica (Kahn's algorithm).

        Args:
            graph: Grafo dirigido.

        Returns:
            Lista ordenada topológicamente, o None si hay ciclo.
        """
        nodes = graph.get_all_nodes()
        if not nodes:
            return []

        # Calcular in-degree
        in_degree: dict[str, int] = {n: 0 for n in nodes}
        for node in nodes:
            for neighbor in graph.get_neighbors(node):
                in_degree[neighbor] = in_degree.get(neighbor, 0) + 1

        # Cola con nodos sin dependencias
        queue: list[str] = sorted([n for n in nodes if in_degree[n] == 0])
        result: list[str] = []

        while queue:
            node = queue.pop(0)
            result.append(node)
            for neighbor in graph.get_neighbors(node):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
                    queue.sort()

        if len(result) != len(nodes):
            return None  # Hay ciclo

        return result


# ═══════════════════════════════════════════════════════════════
# GRAFOS DE TEST
# ═══════════════════════════════════════════════════════════════

GRAPHS: dict[str, dict] = {
    "lineal": {
        "desc": "Sin ciclo: A→B→C→D",
        "edges": {"A": ["B"], "B": ["C"], "C": ["D"], "D": []},
        "has_cycle": False,
    },
    "ciclo_simple": {
        "desc": "Ciclo simple: A→B→C→A",
        "edges": {"A": ["B"], "B": ["C"], "C": ["A"]},
        "has_cycle": True,
    },
    "self_loop": {
        "desc": "Self-loop: A→A",
        "edges": {"A": ["A"]},
        "has_cycle": True,
    },
    "multi_componente": {
        "desc": "2 componentes: {A→B→C} + {D→E→D}",
        "edges": {"A": ["B"], "B": ["C"], "C": [], "D": ["E"], "E": ["D"]},
        "has_cycle": True,
    },
    "complejo": {
        "desc": "6 nodos: A→B→C→D, B→E→F→C (ciclo C→D→...no, pero F→C crea C→D..F→C)",
        "edges": {"A": ["B"], "B": ["C", "E"], "C": ["D"], "D": [], "E": ["F"], "F": ["C"]},
        "has_cycle": False,
    },
}


# ═══════════════════════════════════════════════════════════════
# DEMO Y TESTS
# ═══════════════════════════════════════════════════════════════

def ejecutar_demo_y_tests() -> None:
    """Demo y tests."""

    print("=" * 70)
    print("E3.4 — DEMO: CHAIN OF THOUGHT (Detector de Ciclos)")
    print("=" * 70)

    detector = CycleDetector()

    # ── Demo: cada grafo ──
    for name, info in GRAPHS.items():
        graph = Graph.from_dict(info["edges"])

        print(f"\n{'─' * 50}")
        print(f"Grafo '{name}': {info['desc']}")
        print(f"{'─' * 50}")
        print(graph.visualize())

        # Versión directa
        direct = detect_cycle_direct(graph)
        print(f"\n  Directo (bool):  has_cycle = {direct}")

        # Versión CoT
        cot = detector.detect(graph)
        print(f"  CoT (detalle):   has_cycle = {cot['has_cycle']}")
        if cot["cycle_path"]:
            print(f"                   cycle_path = {'→'.join(cot['cycle_path'])}")
        print(f"                   algorithm = {cot['algorithm']}")

        # Topological sort
        topo = detector.topological_sort(graph)
        if topo is not None:
            print(f"  Topo sort:       {' → '.join(topo)}")
        else:
            print(f"  Topo sort:       None (hay ciclo)")

    # ── Comparativa ──
    print(f"\n{'─' * 50}")
    print("COMPARATIVA: Prompt Directo vs Chain of Thought")
    print(f"{'─' * 50}")
    print(f"\n  {'Aspecto':<30s} {'Directo':>10s} {'CoT':>10s}")
    print(f"  {'─' * 52}")
    print(f"  {'Tipo de retorno':<30s} {'bool':>10s} {'dict':>10s}")
    print(f"  {'Info del ciclo':<30s} {'No':>10s} {'Sí':>10s}")
    print(f"  {'Camino del ciclo':<30s} {'No':>10s} {'Sí':>10s}")
    print(f"  {'Topological sort':<30s} {'No':>10s} {'Sí':>10s}")
    print(f"  {'Visualización':<30s} {'No':>10s} {'Sí':>10s}")
    print(f"  {'Edge cases docs':<30s} {'No':>10s} {'Sí':>10s}")

    # ═══════════════════════════════════════════════════════
    # TESTS
    # ═══════════════════════════════════════════════════════
    print(f"\n{'=' * 70}")
    print("TESTS:")
    print(f"{'=' * 70}")

    det = CycleDetector()

    # Test 1: Directo - sin ciclo
    g1 = Graph.from_dict(GRAPHS["lineal"]["edges"])
    assert detect_cycle_direct(g1) is False
    print("  [PASS] Test 1: Directo — grafo lineal → False")

    # Test 2: Directo - con ciclo
    g2 = Graph.from_dict(GRAPHS["ciclo_simple"]["edges"])
    assert detect_cycle_direct(g2) is True
    print("  [PASS] Test 2: Directo — ciclo simple → True")

    # Test 3: CoT - sin ciclo
    r3 = det.detect(g1)
    assert r3["has_cycle"] is False
    assert r3["cycle_nodes"] == []
    print("  [PASS] Test 3: CoT — sin ciclo, cycle_nodes vacío")

    # Test 4: CoT - con ciclo, devuelve nodos
    r4 = det.detect(g2)
    assert r4["has_cycle"] is True
    assert len(r4["cycle_nodes"]) > 0
    assert len(r4["cycle_path"]) > 0
    print(f"  [PASS] Test 4: CoT — ciclo detectado: {'→'.join(r4['cycle_path'])}")

    # Test 5: Self-loop
    g5 = Graph.from_dict(GRAPHS["self_loop"]["edges"])
    r5 = det.detect(g5)
    assert r5["has_cycle"] is True
    print("  [PASS] Test 5: CoT — self-loop detectado")

    # Test 6: Múltiples componentes
    g6 = Graph.from_dict(GRAPHS["multi_componente"]["edges"])
    r6 = det.detect(g6)
    assert r6["has_cycle"] is True
    print(f"  [PASS] Test 6: CoT — multi-componente, ciclo en {'→'.join(r6['cycle_path'])}")

    # Test 7: Topological sort sin ciclo
    t7 = det.topological_sort(g1)
    assert t7 is not None
    assert len(t7) == 4
    # A debe ir antes de B, B antes de C, etc.
    assert t7.index("A") < t7.index("B") < t7.index("C") < t7.index("D")
    print(f"  [PASS] Test 7: Topo sort sin ciclo: {' → '.join(t7)}")

    # Test 8: Topological sort con ciclo
    t8 = det.topological_sort(g2)
    assert t8 is None
    print("  [PASS] Test 8: Topo sort con ciclo → None")

    # Test 9: Grafo vacío
    g9 = Graph()
    r9 = det.detect(g9)
    assert r9["has_cycle"] is False
    assert detect_cycle_direct(g9) is False
    print("  [PASS] Test 9: Grafo vacío → sin error, sin ciclo")

    # Test 10: Directo solo devuelve bool
    assert isinstance(detect_cycle_direct(g1), bool)
    assert isinstance(detect_cycle_direct(g2), bool)
    print("  [PASS] Test 10: Directo devuelve bool (sin info extra)")

    # Test 11: CoT devuelve dict completo
    r11 = det.detect(g2)
    assert isinstance(r11, dict)
    assert "has_cycle" in r11 and "cycle_nodes" in r11 and "cycle_path" in r11 and "algorithm" in r11
    print("  [PASS] Test 11: CoT devuelve dict con 4+ campos")

    # Test 12: Visualize genera output
    v12 = g2.visualize()
    assert "→" in v12
    assert "A" in v12
    print(f"  [PASS] Test 12: Visualize genera representación del grafo")

    print(f"\n  Todos los tests pasaron correctamente.")


if __name__ == "__main__":
    ejecutar_demo_y_tests()
