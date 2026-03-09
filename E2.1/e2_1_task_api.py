"""
E2.1 — API REST Flask con CRUD de Tareas
==========================================
API REST completa para gestionar tareas, generada como ejemplo de
cómo un agente de IA produce aplicaciones funcionales desde una
especificación en lenguaje natural.

Uso como servidor:
    python e2_1_task_api.py

Uso como tests:
    python e2_1_task_api.py --test

Dependencias: pip install flask
"""

import json
import logging
import sys
from datetime import datetime, timezone
from typing import Optional

from flask import Flask, Response, jsonify, request

__version__ = "1.0.0"

# ═══════════════════════════════════════════════════════════════
# APP SETUP
# ═══════════════════════════════════════════════════════════════

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("task_api")

# ═══════════════════════════════════════════════════════════════
# DATA STORE (in-memory)
# ═══════════════════════════════════════════════════════════════

tasks: dict[int, dict] = {}
next_id: int = 1

VALID_STATUSES: set[str] = {"pending", "in_progress", "completed"}


def _now() -> str:
    """Devuelve la fecha/hora actual en formato ISO 8601."""
    return datetime.now(timezone.utc).isoformat()


def init_sample_data() -> None:
    """Carga 3 tareas de ejemplo en el almacén de datos.

    Se llama al iniciar la aplicación para tener datos de demostración.
    """
    global next_id
    tasks.clear()
    next_id = 1

    sample_tasks = [
        {"title": "Diseñar API REST", "description": "Definir endpoints, modelos y validaciones", "status": "pending"},
        {"title": "Implementar autenticación", "description": "JWT con login, registro y refresh token", "status": "in_progress"},
        {"title": "Escribir documentación", "description": "Swagger/OpenAPI + README con ejemplos", "status": "completed"},
    ]

    for t in sample_tasks:
        now = _now()
        tasks[next_id] = {
            "id": next_id,
            "title": t["title"],
            "description": t["description"],
            "status": t["status"],
            "created_at": now,
            "updated_at": now,
        }
        next_id += 1


# ═══════════════════════════════════════════════════════════════
# VALIDATION
# ═══════════════════════════════════════════════════════════════

def validate_task(data: dict, require_title: bool = True) -> tuple[bool, str]:
    """Valida los datos de una tarea.

    Args:
        data: Diccionario con los campos de la tarea.
        require_title: Si True, title es obligatorio (POST). Si False, es opcional (PUT).

    Returns:
        Tupla (es_valido, mensaje_error). Si es_valido es True, mensaje_error es "".
    """
    if not isinstance(data, dict):
        return False, "El body debe ser un objeto JSON"

    # Title validation
    if require_title:
        if "title" not in data or not data["title"]:
            return False, "El campo 'title' es obligatorio"

    if "title" in data:
        title = data["title"]
        if not isinstance(title, str) or len(title.strip()) == 0:
            return False, "El campo 'title' no puede estar vacío"
        if len(title) > 100:
            return False, "El campo 'title' no puede exceder 100 caracteres"

    # Description validation
    if "description" in data and data["description"] is not None:
        if not isinstance(data["description"], str):
            return False, "El campo 'description' debe ser un string"
        if len(data["description"]) > 500:
            return False, "El campo 'description' no puede exceder 500 caracteres"

    # Status validation
    if "status" in data:
        if data["status"] not in VALID_STATUSES:
            return False, f"El campo 'status' debe ser uno de: {', '.join(sorted(VALID_STATUSES))}"

    return True, ""


# ═══════════════════════════════════════════════════════════════
# CORS
# ═══════════════════════════════════════════════════════════════

@app.after_request
def add_cors_headers(response: Response) -> Response:
    """Añade headers CORS a todas las respuestas.

    Args:
        response: Respuesta Flask.

    Returns:
        Respuesta con headers CORS añadidos.
    """
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


# ═══════════════════════════════════════════════════════════════
# ENDPOINTS
# ═══════════════════════════════════════════════════════════════

@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    """Lista todas las tareas, con filtro opcional por status.

    Query params:
        status (optional): Filtrar por estado (pending, in_progress, completed).

    Returns:
        200: Lista de tareas en JSON.
    """
    status_filter: Optional[str] = request.args.get("status")
    result = list(tasks.values())

    if status_filter:
        if status_filter not in VALID_STATUSES:
            return jsonify({"error": f"Status inválido. Usa: {', '.join(sorted(VALID_STATUSES))}"}), 400
        result = [t for t in result if t["status"] == status_filter]

    logger.info(f"GET /api/tasks — {len(result)} tareas (filtro: {status_filter or 'ninguno'})")
    return jsonify(result), 200


@app.route("/api/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id: int):
    """Obtiene una tarea por su ID.

    Args:
        task_id: ID de la tarea.

    Returns:
        200: Tarea en JSON.
        404: Si no existe.
    """
    task = tasks.get(task_id)
    if not task:
        return jsonify({"error": f"Tarea con id={task_id} no encontrada"}), 404

    logger.info(f"GET /api/tasks/{task_id} — '{task['title']}'")
    return jsonify(task), 200


@app.route("/api/tasks", methods=["POST"])
def create_task():
    """Crea una nueva tarea.

    Body JSON:
        title (str, required): Título (1-100 chars).
        description (str, optional): Descripción (max 500 chars).
        status (str, optional): Estado (default: pending).

    Returns:
        201: Tarea creada en JSON.
        400: Si la validación falla.
    """
    global next_id

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Body debe ser JSON válido"}), 400

    valid, error = validate_task(data, require_title=True)
    if not valid:
        return jsonify({"error": error}), 400

    now = _now()
    task = {
        "id": next_id,
        "title": data["title"].strip(),
        "description": data.get("description", ""),
        "status": data.get("status", "pending"),
        "created_at": now,
        "updated_at": now,
    }

    tasks[next_id] = task
    logger.info(f"POST /api/tasks — Creada #{next_id}: '{task['title']}'")
    next_id += 1

    return jsonify(task), 201


@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id: int):
    """Actualiza una tarea existente (campos parciales permitidos).

    Args:
        task_id: ID de la tarea.

    Body JSON:
        title (str, optional): Nuevo título.
        description (str, optional): Nueva descripción.
        status (str, optional): Nuevo estado.

    Returns:
        200: Tarea actualizada en JSON.
        404: Si no existe.
        400: Si la validación falla.
    """
    task = tasks.get(task_id)
    if not task:
        return jsonify({"error": f"Tarea con id={task_id} no encontrada"}), 404

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "Body debe ser JSON válido"}), 400

    valid, error = validate_task(data, require_title=False)
    if not valid:
        return jsonify({"error": error}), 400

    # Update only provided fields
    if "title" in data:
        task["title"] = data["title"].strip()
    if "description" in data:
        task["description"] = data["description"]
    if "status" in data:
        task["status"] = data["status"]

    task["updated_at"] = _now()

    logger.info(f"PUT /api/tasks/{task_id} — Actualizada: '{task['title']}'")
    return jsonify(task), 200


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id: int):
    """Elimina una tarea por su ID.

    Args:
        task_id: ID de la tarea.

    Returns:
        204: Eliminada exitosamente (sin body).
        404: Si no existe.
    """
    if task_id not in tasks:
        return jsonify({"error": f"Tarea con id={task_id} no encontrada"}), 404

    title = tasks[task_id]["title"]
    del tasks[task_id]
    logger.info(f"DELETE /api/tasks/{task_id} — Eliminada: '{title}'")
    return "", 204


@app.route("/api/tasks/stats", methods=["GET"])
def get_stats():
    """Devuelve estadísticas de las tareas.

    Returns:
        200: JSON con total, conteo por estado y última tarea creada.
    """
    all_tasks = list(tasks.values())
    stats = {
        "total": len(all_tasks),
        "by_status": {
            "pending": len([t for t in all_tasks if t["status"] == "pending"]),
            "in_progress": len([t for t in all_tasks if t["status"] == "in_progress"]),
            "completed": len([t for t in all_tasks if t["status"] == "completed"]),
        },
        "last_created": max(all_tasks, key=lambda t: t["created_at"])["title"] if all_tasks else None,
    }

    logger.info(f"GET /api/tasks/stats — {stats['total']} tareas")
    return jsonify(stats), 200


# ═══════════════════════════════════════════════════════════════
# TESTS
# ═══════════════════════════════════════════════════════════════

def run_tests() -> None:
    """Ejecuta 12 tests contra la API usando el test client de Flask."""

    print("=" * 70)
    print("E2.1 — TESTS: API REST Flask")
    print("=" * 70)

    # Reset data
    init_sample_data()

    with app.test_client() as client:

        # Test 1: GET all tasks
        resp = client.get("/api/tasks")
        assert resp.status_code == 200
        data = resp.get_json()
        assert len(data) == 3, f"Esperado 3 tareas iniciales, obtenido {len(data)}"
        print("  [PASS] Test 1: GET /api/tasks → 200, 3 tareas iniciales")

        # Test 2: GET one task
        resp = client.get("/api/tasks/1")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["id"] == 1
        assert data["title"] == "Diseñar API REST"
        print("  [PASS] Test 2: GET /api/tasks/1 → 200, tarea correcta")

        # Test 3: GET not found
        resp = client.get("/api/tasks/999")
        assert resp.status_code == 404
        data = resp.get_json()
        assert "error" in data
        print("  [PASS] Test 3: GET /api/tasks/999 → 404")

        # Test 4: POST valid
        resp = client.post("/api/tasks", json={
            "title": "Nueva tarea de test",
            "description": "Creada desde test",
            "status": "pending",
        })
        assert resp.status_code == 201
        data = resp.get_json()
        assert data["title"] == "Nueva tarea de test"
        assert "id" in data
        assert "created_at" in data
        new_id = data["id"]
        print("  [PASS] Test 4: POST /api/tasks → 201, tarea creada")

        # Test 5: POST without title
        resp = client.post("/api/tasks", json={"description": "Sin título"})
        assert resp.status_code == 400
        data = resp.get_json()
        assert "error" in data
        print("  [PASS] Test 5: POST sin title → 400")

        # Test 6: POST with empty title
        resp = client.post("/api/tasks", json={"title": ""})
        assert resp.status_code == 400
        print("  [PASS] Test 6: POST title vacío → 400")

        # Test 7: POST with invalid status
        resp = client.post("/api/tasks", json={"title": "Test", "status": "invalid_status"})
        assert resp.status_code == 400
        data = resp.get_json()
        assert "status" in data["error"].lower()
        print("  [PASS] Test 7: POST status inválido → 400")

        # Test 8: PUT valid
        resp = client.put(f"/api/tasks/{new_id}", json={"title": "Tarea actualizada"})
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["title"] == "Tarea actualizada"
        print(f"  [PASS] Test 8: PUT /api/tasks/{new_id} → 200, actualizada")

        # Test 9: PUT not found
        resp = client.put("/api/tasks/999", json={"title": "No existe"})
        assert resp.status_code == 404
        print("  [PASS] Test 9: PUT /api/tasks/999 → 404")

        # Test 10: DELETE valid
        resp = client.delete(f"/api/tasks/{new_id}")
        assert resp.status_code == 204
        # Verify it's gone
        resp2 = client.get(f"/api/tasks/{new_id}")
        assert resp2.status_code == 404
        print(f"  [PASS] Test 10: DELETE /api/tasks/{new_id} → 204, confirmado eliminado")

        # Test 11: DELETE not found
        resp = client.delete("/api/tasks/999")
        assert resp.status_code == 404
        print("  [PASS] Test 11: DELETE /api/tasks/999 → 404")

        # Test 12: GET stats
        resp = client.get("/api/tasks/stats")
        assert resp.status_code == 200
        data = resp.get_json()
        assert "total" in data
        assert "by_status" in data
        assert data["total"] == 3  # 3 iniciales (la creada en test 4 fue eliminada)
        assert data["by_status"]["pending"] >= 1
        print("  [PASS] Test 12: GET /api/tasks/stats → 200, estadísticas correctas")

        # Bonus: Filter by status
        resp = client.get("/api/tasks?status=pending")
        assert resp.status_code == 200
        data = resp.get_json()
        assert all(t["status"] == "pending" for t in data)
        print("  [PASS] Bonus: GET /api/tasks?status=pending → filtrado correcto")

    print("\n  Todos los tests pasaron correctamente.")


# ═══════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    if "--test" in sys.argv:
        run_tests()
    else:
        init_sample_data()
        print(f"\n  Task API v{__version__} — http://127.0.0.1:5000")
        print(f"  Endpoints:")
        print(f"    GET    /api/tasks          — Listar tareas")
        print(f"    GET    /api/tasks/<id>      — Obtener tarea")
        print(f"    POST   /api/tasks          — Crear tarea")
        print(f"    PUT    /api/tasks/<id>      — Actualizar tarea")
        print(f"    DELETE /api/tasks/<id>      — Eliminar tarea")
        print(f"    GET    /api/tasks/stats     — Estadísticas")
        print(f"\n  Tareas iniciales: {len(tasks)}")
        print(f"  Ctrl+C para detener\n")
        app.run(debug=True, port=5000)
