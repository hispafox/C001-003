"""
E4.1 — TaskFlow: Gestor de Tareas CLI Completo
=================================================
Mini-proyecto generado por agente de IA. Demuestra generación
de código a escala de proyecto con Copilot Agente.

Uso demo + tests: python e4_1_taskflow.py
CLI: python e4_1_taskflow.py add "Tarea" -p high -t tag1,tag2
     python e4_1_taskflow.py list --status todo --sort priority
     python e4_1_taskflow.py done 1
     python e4_1_taskflow.py stats

Dependencias: Solo librería estándar.
"""

import argparse
import json
import os
import sys
import tempfile
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

__version__ = "1.0.0"

# ═══════════════════════════════════════════════════════════════
# CONSTANTES Y COLORES ANSI
# ═══════════════════════════════════════════════════════════════

PRIORITIES = ("low", "medium", "high", "urgent")
STATUSES = ("todo", "in_progress", "done", "cancelled")

PRIORITY_ICONS = {"urgent": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}
STATUS_ICONS = {"todo": "📋", "in_progress": "🔄", "done": "✅", "cancelled": "❌"}

ANSI_BOLD = "\033[1m"
ANSI_DIM = "\033[2m"
ANSI_RESET = "\033[0m"
ANSI_RED = "\033[91m"
ANSI_GREEN = "\033[92m"
ANSI_YELLOW = "\033[93m"
ANSI_BLUE = "\033[94m"
ANSI_CYAN = "\033[96m"


# ═══════════════════════════════════════════════════════════════
# MODELO
# ═══════════════════════════════════════════════════════════════

@dataclass
class Task:
    """Tarea del gestor TaskFlow."""
    id: int
    title: str
    description: str = ""
    priority: str = "medium"
    status: str = "todo"
    created_at: str = ""
    updated_at: str = ""
    due_date: Optional[str] = None
    tags: list[str] = field(default_factory=list)
    project: str = "default"

    def __post_init__(self) -> None:
        now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
        if not self.created_at:
            self.created_at = now
        if not self.updated_at:
            self.updated_at = now

    def format_row(self) -> str:
        """Formato tabla para CLI."""
        p_icon = PRIORITY_ICONS.get(self.priority, "·")
        s_icon = STATUS_ICONS.get(self.status, "·")
        title = self.title[:30] + ("…" if len(self.title) > 30 else "")
        tags_str = ",".join(self.tags[:3]) if self.tags else "—"
        due = self.due_date or "—"
        return f"  {self.id:<4d} {s_icon} {title:<32s} {p_icon} {self.priority:<8s} {self.project:<12s} {tags_str:<15s} {due}"

    @property
    def is_overdue(self) -> bool:
        """True si tiene due_date pasada y no está completada."""
        if not self.due_date or self.status in ("done", "cancelled"):
            return False
        return self.due_date < datetime.now(timezone.utc).strftime("%Y-%m-%d")


# ═══════════════════════════════════════════════════════════════
# TASK MANAGER
# ═══════════════════════════════════════════════════════════════

class TaskManager:
    """Gestor de tareas con persistencia JSON.

    Args:
        filepath: Ruta al archivo JSON. ":memory:" para no persistir.
    """

    def __init__(self, filepath: str = "tasks.json") -> None:
        self.filepath = filepath
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1
        if filepath != ":memory:" and Path(filepath).exists():
            self._load()

    def _load(self) -> None:
        """Carga tareas desde JSON."""
        try:
            data = json.loads(Path(self.filepath).read_text(encoding="utf-8"))
            for t in data.get("tasks", []):
                task = Task(**t)
                self._tasks[task.id] = task
                if task.id >= self._next_id:
                    self._next_id = task.id + 1
        except (json.JSONDecodeError, OSError, TypeError):
            pass

    def _save(self) -> None:
        """Guarda tareas a JSON."""
        if self.filepath == ":memory:":
            return
        data = {"tasks": [asdict(t) for t in self._tasks.values()]}
        Path(self.filepath).write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def add(self, title: str, description: str = "", priority: str = "medium",
            due_date: Optional[str] = None, tags: Optional[list[str]] = None,
            project: str = "default") -> Task:
        """Añade una tarea nueva."""
        if priority not in PRIORITIES:
            raise ValueError(f"Prioridad inválida: {priority}")
        task = Task(
            id=self._next_id, title=title, description=description,
            priority=priority, due_date=due_date, tags=tags or [], project=project,
        )
        self._tasks[task.id] = task
        self._next_id += 1
        self._save()
        return task

    def update(self, task_id: int, **fields) -> Optional[Task]:
        """Actualiza campos de una tarea."""
        task = self._tasks.get(task_id)
        if not task:
            return None
        for key, value in fields.items():
            if hasattr(task, key) and key not in ("id", "created_at"):
                setattr(task, key, value)
        task.updated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")
        self._save()
        return task

    def delete(self, task_id: int) -> bool:
        """Elimina una tarea."""
        if task_id in self._tasks:
            del self._tasks[task_id]
            self._save()
            return True
        return False

    def get(self, task_id: int) -> Optional[Task]:
        """Obtiene una tarea por ID."""
        return self._tasks.get(task_id)

    def list_all(self, status: Optional[str] = None, priority: Optional[str] = None,
                 project: Optional[str] = None, tag: Optional[str] = None,
                 sort_by: str = "id") -> list[Task]:
        """Lista tareas con filtros opcionales."""
        tasks = list(self._tasks.values())
        if status:
            tasks = [t for t in tasks if t.status == status]
        if priority:
            tasks = [t for t in tasks if t.priority == priority]
        if project:
            tasks = [t for t in tasks if t.project == project]
        if tag:
            tasks = [t for t in tasks if tag in t.tags]

        sort_keys = {
            "id": lambda t: t.id,
            "priority": lambda t: PRIORITIES.index(t.priority) if t.priority in PRIORITIES else 99,
            "status": lambda t: STATUSES.index(t.status) if t.status in STATUSES else 99,
            "due_date": lambda t: t.due_date or "9999-99-99",
            "created_at": lambda t: t.created_at,
        }
        reverse = sort_by == "priority"  # urgent first
        tasks.sort(key=sort_keys.get(sort_by, sort_keys["id"]), reverse=reverse)
        return tasks

    def search(self, query: str) -> list[Task]:
        """Busca en título, descripción y tags."""
        q = query.lower()
        return [t for t in self._tasks.values()
                if q in t.title.lower() or q in t.description.lower()
                or any(q in tag.lower() for tag in t.tags)]

    def stats(self) -> dict:
        """Estadísticas completas."""
        tasks = list(self._tasks.values())
        by_status = {s: 0 for s in STATUSES}
        by_priority = {p: 0 for p in PRIORITIES}
        by_project: dict[str, int] = {}
        overdue = 0

        for t in tasks:
            by_status[t.status] = by_status.get(t.status, 0) + 1
            by_priority[t.priority] = by_priority.get(t.priority, 0) + 1
            by_project[t.project] = by_project.get(t.project, 0) + 1
            if t.is_overdue:
                overdue += 1

        return {
            "total": len(tasks),
            "by_status": by_status,
            "by_priority": by_priority,
            "by_project": by_project,
            "overdue": overdue,
        }


# ═══════════════════════════════════════════════════════════════
# DEMO Y TESTS
# ═══════════════════════════════════════════════════════════════

def ejecutar_demo_y_tests() -> None:
    """Demo completa + 12 tests."""

    print("=" * 70)
    print("E4.1 — DEMO: TASKFLOW CLI")
    print("=" * 70)

    tm = TaskManager(":memory:")

    # ── Añadir tareas ──
    print(f"\n{'─' * 50}")
    print("Añadiendo tareas:")
    print(f"{'─' * 50}")

    tasks_data = [
        ("Configurar CI/CD pipeline", "high", ["devops", "ci"], "infra", "2026-03-15"),
        ("Escribir tests unitarios", "urgent", ["testing"], "backend", "2026-03-10"),
        ("Diseñar landing page", "medium", ["diseño", "frontend"], "web", "2026-03-20"),
        ("Revisar PR de autenticación", "high", ["review", "security"], "backend", None),
        ("Actualizar dependencias", "low", ["maintenance"], "infra", "2026-04-01"),
        ("Implementar API de pagos", "urgent", ["api", "pagos"], "backend", "2026-03-12"),
        ("Documentar API REST", "medium", ["docs"], "backend", "2026-03-25"),
        ("Optimizar queries SQL", "high", ["performance", "db"], "backend", "2026-03-18"),
    ]
    for title, priority, tags, project, due in tasks_data:
        t = tm.add(title, priority=priority, tags=tags, project=project, due_date=due)
        icon = PRIORITY_ICONS[priority]
        print(f"  {icon} #{t.id} {t.title}")

    # ── Listar ──
    print(f"\n{'─' * 50}")
    print("Todas las tareas (ordenadas por prioridad):")
    print(f"{'─' * 50}")
    print(f"  {'ID':<4s}    {'Título':<32s}   {'Prioridad':<8s}  {'Proyecto':<12s} {'Tags':<15s} {'Due'}")
    print(f"  {'─' * 95}")
    for t in tm.list_all(sort_by="priority"):
        print(t.format_row())

    # ── Completar y actualizar ──
    tm.update(2, status="done")
    tm.update(6, status="in_progress")
    print(f"\n  ✅ Tarea #2 completada")
    print(f"  🔄 Tarea #6 en progreso")

    # ── Búsqueda ──
    results = tm.search("api")
    print(f'\n  Búsqueda "api": {len(results)} resultados')
    for t in results:
        print(f"    #{t.id} {t.title}")

    # ── Estadísticas ──
    print(f"\n{'─' * 50}")
    print("Estadísticas:")
    print(f"{'─' * 50}")
    s = tm.stats()
    print(f"  Total: {s['total']}")
    print(f"  Por estado: {s['by_status']}")
    print(f"  Por prioridad: {s['by_priority']}")
    print(f"  Proyectos: {s['by_project']}")
    print(f"  Vencidas: {s['overdue']}")

    # ═══════════════════════════════════════════════════════
    # TESTS
    # ═══════════════════════════════════════════════════════
    print(f"\n{'=' * 70}")
    print("TESTS:")
    print(f"{'=' * 70}")

    tm2 = TaskManager(":memory:")

    # Test 1: Add
    t = tm2.add("Test task", priority="high", tags=["test"])
    assert t.id == 1 and t.title == "Test task" and t.priority == "high"
    print("  [PASS] Test 1: add() crea tarea con campos correctos")

    # Test 2: Get
    got = tm2.get(1)
    assert got is not None and got.title == "Test task"
    print("  [PASS] Test 2: get() recupera tarea por ID")

    # Test 3: Update
    updated = tm2.update(1, status="done", priority="low")
    assert updated is not None and updated.status == "done" and updated.priority == "low"
    print("  [PASS] Test 3: update() cambia status y priority")

    # Test 4: Delete
    tm2.add("To delete")
    assert tm2.delete(2) is True
    assert tm2.get(2) is None
    assert tm2.delete(999) is False
    print("  [PASS] Test 4: delete() elimina y devuelve False si no existe")

    # Test 5: List con filtros
    tm2.add("Task A", priority="high", project="web")
    tm2.add("Task B", priority="low", project="api")
    tm2.add("Task C", priority="high", project="web", tags=["urgent"])
    high = tm2.list_all(priority="high")
    assert len(high) == 2
    web = tm2.list_all(project="web")
    assert len(web) == 2
    print("  [PASS] Test 5: list_all() filtra por priority y project")

    # Test 6: Sort
    sorted_p = tm2.list_all(sort_by="priority")
    assert sorted_p[0].priority == "high"  # urgent first → high
    print("  [PASS] Test 6: list_all(sort_by='priority') ordena correctamente")

    # Test 7: Search
    results = tm2.search("task")
    assert len(results) >= 2
    print(f"  [PASS] Test 7: search('task') encuentra {len(results)} resultados")

    # Test 8: Search en tags
    results = tm2.search("urgent")
    assert len(results) >= 1
    print("  [PASS] Test 8: search() busca en tags")

    # Test 9: Stats
    s = tm2.stats()
    assert s["total"] >= 4
    assert "by_status" in s and "by_priority" in s and "by_project" in s
    print(f"  [PASS] Test 9: stats() → total={s['total']}, projects={list(s['by_project'].keys())}")

    # Test 10: Prioridad inválida
    try:
        tm2.add("Bad", priority="super_high")
        assert False
    except ValueError:
        pass
    print("  [PASS] Test 10: Prioridad inválida → ValueError")

    # Test 11: Persistencia JSON
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        path = f.name
    tm3 = TaskManager(path)
    tm3.add("Persistent task", priority="high")
    tm3.add("Another task")
    # Reload
    tm4 = TaskManager(path)
    assert tm4.get(1) is not None and tm4.get(1).title == "Persistent task"
    assert len(tm4.list_all()) == 2
    os.unlink(path)
    print("  [PASS] Test 11: Persistencia JSON (save + reload)")

    # Test 12: Task format_row
    t = Task(id=1, title="Test", priority="urgent", status="in_progress", project="web")
    row = t.format_row()
    assert "🔴" in row and "🔄" in row
    print("  [PASS] Test 12: format_row() incluye iconos correctos")

    print(f"\n  Todos los tests pasaron correctamente.")


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

def crear_cli() -> argparse.ArgumentParser:
    """Crea el parser CLI."""
    parser = argparse.ArgumentParser(prog="taskflow", description="TaskFlow — Gestor de tareas CLI")
    sub = parser.add_subparsers(dest="command")

    a = sub.add_parser("add", help="Añade tarea")
    a.add_argument("title")
    a.add_argument("-d", "--description", default="")
    a.add_argument("-p", "--priority", default="medium", choices=PRIORITIES)
    a.add_argument("-t", "--tags", default="")
    a.add_argument("--project", default="default")
    a.add_argument("--due", default=None)

    l = sub.add_parser("list", help="Lista tareas")
    l.add_argument("--status", choices=STATUSES)
    l.add_argument("--priority", choices=PRIORITIES)
    l.add_argument("--project")
    l.add_argument("--tag")
    l.add_argument("--sort", default="id")

    sub.add_parser("stats", help="Estadísticas")

    d = sub.add_parser("done", help="Marca como completada")
    d.add_argument("task_id", type=int)

    u = sub.add_parser("update", help="Actualiza tarea")
    u.add_argument("task_id", type=int)
    u.add_argument("--status", choices=STATUSES)
    u.add_argument("--priority", choices=PRIORITIES)
    u.add_argument("--title")

    dl = sub.add_parser("delete", help="Elimina tarea")
    dl.add_argument("task_id", type=int)

    s = sub.add_parser("search", help="Busca tareas")
    s.add_argument("query")

    return parser


if __name__ == "__main__":
    if len(sys.argv) > 1:
        parser = crear_cli()
        args = parser.parse_args()
        tm = TaskManager()

        if args.command == "add":
            tags = [t.strip() for t in args.tags.split(",") if t.strip()] if args.tags else []
            t = tm.add(args.title, args.description, args.priority, args.due, tags, args.project)
            print(f"  ✅ Tarea #{t.id} creada: {t.title}")
        elif args.command == "list":
            tasks = tm.list_all(args.status, args.priority, args.project, args.tag, args.sort)
            for t in tasks:
                print(t.format_row())
        elif args.command == "done":
            if tm.update(args.task_id, status="done"):
                print(f"  ✅ Tarea #{args.task_id} completada")
            else:
                print(f"  ❌ Tarea #{args.task_id} no encontrada")
        elif args.command == "update":
            fields = {k: v for k, v in vars(args).items() if v is not None and k not in ("command", "task_id")}
            if tm.update(args.task_id, **fields):
                print(f"  ✅ Tarea #{args.task_id} actualizada")
        elif args.command == "delete":
            if tm.delete(args.task_id):
                print(f"  🗑️ Tarea #{args.task_id} eliminada")
        elif args.command == "search":
            for t in tm.search(args.query):
                print(t.format_row())
        elif args.command == "stats":
            s = tm.stats()
            print(f"  Total: {s['total']} | Vencidas: {s['overdue']}")
            print(f"  Estado: {s['by_status']}")
            print(f"  Prioridad: {s['by_priority']}")
        else:
            parser.print_help()
    else:
        ejecutar_demo_y_tests()
