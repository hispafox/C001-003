"""
E2.5 — Gestor de Contraseñas CLI
==================================
Genera, almacena y gestiona contraseñas desde la terminal.
Diseñado para ser el mismo prompt dado a Claude, Copilot Agente
y ChatGPT — comparar qué genera cada uno.

Uso demo + tests:
    python e2_5_password_manager.py

CLI:
    python e2_5_password_manager.py generate --length 20
    python e2_5_password_manager.py add --service GitHub --username user
    python e2_5_password_manager.py list
    python e2_5_password_manager.py search git
    python e2_5_password_manager.py get GitHub
    python e2_5_password_manager.py delete GitHub
    python e2_5_password_manager.py export --output passwords.csv

Dependencias: Solo librería estándar.
"""

import argparse
import base64
import json
import os
import secrets
import string
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

__version__ = "1.0.0"


# ═══════════════════════════════════════════════════════════════
# PASSWORD MANAGER
# ═══════════════════════════════════════════════════════════════

class PasswordManager:
    """Gestor de contraseñas con generación segura y almacenamiento JSON.

    Usa secrets (criptográficamente seguro) para generación y base64
    para codificación del almacenamiento (educativo, no producción).

    Attributes:
        filepath: Ruta al archivo JSON de almacenamiento.

    Examples:
        >>> pm = PasswordManager(":memory:")
        >>> pwd = pm.generate_password(16)
        >>> len(pwd) == 16
        True
    """

    def __init__(self, filepath: str = "passwords.json") -> None:
        """Inicializa el gestor.

        Args:
            filepath: Ruta al archivo JSON. Usa ":memory:" para no persistir.
        """
        self.filepath: str = filepath
        self._data: dict = {"entries": []}

        if filepath != ":memory:" and Path(filepath).exists():
            try:
                self._data = json.loads(Path(filepath).read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                self._data = {"entries": []}

    def _save(self) -> None:
        """Guarda datos al archivo JSON."""
        if self.filepath == ":memory:":
            return
        Path(self.filepath).write_text(
            json.dumps(self._data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    # ── Generación ──

    def generate_password(
        self,
        length: int = 16,
        uppercase: bool = True,
        lowercase: bool = True,
        digits: bool = True,
        symbols: bool = True,
    ) -> str:
        """Genera una contraseña criptográficamente segura.

        Usa secrets.choice() y garantiza al menos 1 carácter de cada
        tipo seleccionado.

        Args:
            length: Longitud de la contraseña (mínimo 4).
            uppercase: Incluir mayúsculas.
            lowercase: Incluir minúsculas.
            digits: Incluir dígitos.
            symbols: Incluir símbolos.

        Returns:
            String con la contraseña generada.

        Raises:
            ValueError: Si length < 4 o ningún tipo seleccionado.
        """
        if length < 4:
            raise ValueError("La longitud mínima es 4")

        pools: list[str] = []
        required: list[str] = []

        if uppercase:
            pools.append(string.ascii_uppercase)
            required.append(secrets.choice(string.ascii_uppercase))
        if lowercase:
            pools.append(string.ascii_lowercase)
            required.append(secrets.choice(string.ascii_lowercase))
        if digits:
            pools.append(string.digits)
            required.append(secrets.choice(string.digits))
        if symbols:
            pool = "!@#$%^&*()-_=+[]{}|;:,.<>?"
            pools.append(pool)
            required.append(secrets.choice(pool))

        if not pools:
            raise ValueError("Debe seleccionar al menos un tipo de carácter")

        all_chars: str = "".join(pools)
        remaining: int = length - len(required)
        password_chars: list[str] = required + [
            secrets.choice(all_chars) for _ in range(remaining)
        ]

        # Mezclar de forma segura
        result: list[str] = []
        temp = password_chars[:]
        while temp:
            idx = secrets.randbelow(len(temp))
            result.append(temp.pop(idx))

        return "".join(result)

    def evaluate_strength(self, password: str) -> dict:
        """Evalúa la fortaleza de una contraseña.

        Args:
            password: Contraseña a evaluar.

        Returns:
            Diccionario con score (0-100), level, feedback.
        """
        score: int = 0
        feedback: list[str] = []

        # Longitud
        n: int = len(password)
        if n >= 16:
            score += 30
        elif n >= 12:
            score += 25
        elif n >= 8:
            score += 15
        else:
            score += 5
            feedback.append("Demasiado corta (mínimo 8 recomendado)")

        # Variedad de tipos
        has_upper: bool = any(c in string.ascii_uppercase for c in password)
        has_lower: bool = any(c in string.ascii_lowercase for c in password)
        has_digit: bool = any(c in string.digits for c in password)
        has_symbol: bool = any(c in "!@#$%^&*()-_=+[]{}|;:,.<>?" for c in password)

        variety: int = sum([has_upper, has_lower, has_digit, has_symbol])

        if variety == 4:
            score += 40
        elif variety == 3:
            score += 30
        elif variety == 2:
            score += 15
            feedback.append("Añade más tipos de caracteres")
        else:
            score += 5
            feedback.append("Usa mayúsculas, minúsculas, números y símbolos")

        # Caracteres únicos
        unique_ratio: float = len(set(password)) / n if n > 0 else 0
        if unique_ratio > 0.8:
            score += 20
        elif unique_ratio > 0.6:
            score += 15
        elif unique_ratio > 0.4:
            score += 10
        else:
            score += 5
            feedback.append("Demasiados caracteres repetidos")

        # Bonus longitud extra
        if n >= 20:
            score += 10

        score = min(score, 100)

        if score >= 80:
            level = "Muy fuerte"
        elif score >= 60:
            level = "Fuerte"
        elif score >= 40:
            level = "Media"
        else:
            level = "Débil"

        if not feedback:
            feedback.append("¡Excelente contraseña!")

        return {"score": score, "level": level, "feedback": feedback}

    # ── CRUD ──

    def add_entry(
        self, service: str, username: str, password: str, notes: str = ""
    ) -> dict:
        """Añade una entrada al gestor.

        Args:
            service: Nombre del servicio.
            username: Nombre de usuario.
            password: Contraseña (se codifica en base64).
            notes: Notas opcionales.

        Returns:
            Diccionario con la entrada creada.
        """
        entry: dict = {
            "service": service,
            "username": username,
            "password_b64": base64.b64encode(password.encode()).decode(),
            "created_at": datetime.now(timezone.utc).isoformat(),
            "notes": notes,
        }
        self._data["entries"].append(entry)
        self._save()
        return entry

    def get_entry(self, service: str) -> Optional[dict]:
        """Obtiene una entrada por nombre de servicio.

        Args:
            service: Nombre del servicio (case-insensitive).

        Returns:
            Diccionario con la entrada (password decodificada) o None.
        """
        for entry in self._data["entries"]:
            if entry["service"].lower() == service.lower():
                result = entry.copy()
                result["password"] = base64.b64decode(entry["password_b64"]).decode()
                return result
        return None

    def list_entries(self) -> list[dict]:
        """Lista todas las entradas sin mostrar contraseñas.

        Returns:
            Lista de diccionarios con service, username, created_at, notes.
        """
        return [
            {
                "service": e["service"],
                "username": e["username"],
                "created_at": e["created_at"],
                "notes": e.get("notes", ""),
            }
            for e in self._data["entries"]
        ]

    def search(self, query: str) -> list[dict]:
        """Busca entradas por texto parcial en service o username.

        Args:
            query: Texto a buscar (case-insensitive).

        Returns:
            Lista de entradas que coinciden.
        """
        q: str = query.lower()
        return [
            {"service": e["service"], "username": e["username"],
             "created_at": e["created_at"], "notes": e.get("notes", "")}
            for e in self._data["entries"]
            if q in e["service"].lower() or q in e["username"].lower()
        ]

    def delete_entry(self, service: str) -> bool:
        """Elimina una entrada por servicio.

        Args:
            service: Nombre del servicio.

        Returns:
            True si se eliminó, False si no existía.
        """
        before: int = len(self._data["entries"])
        self._data["entries"] = [
            e for e in self._data["entries"]
            if e["service"].lower() != service.lower()
        ]
        deleted: bool = len(self._data["entries"]) < before
        if deleted:
            self._save()
        return deleted

    def export_csv(self, filepath: str) -> int:
        """Exporta entradas a CSV.

        Args:
            filepath: Ruta del archivo CSV.

        Returns:
            Número de entradas exportadas.
        """
        lines: list[str] = ["service,username,password,created_at,notes"]
        for e in self._data["entries"]:
            pwd: str = base64.b64decode(e["password_b64"]).decode()
            notes: str = e.get("notes", "").replace('"', '""')
            lines.append(f'{e["service"]},{e["username"]},{pwd},{e["created_at"]},"{notes}"')

        Path(filepath).write_text("\n".join(lines), encoding="utf-8")
        return len(self._data["entries"])


# ═══════════════════════════════════════════════════════════════
# DEMO Y TESTS
# ═══════════════════════════════════════════════════════════════

def ejecutar_demo_y_tests() -> None:
    """Ejecuta demo y tests."""

    print("=" * 70)
    print("E2.5 — DEMO: GESTOR DE CONTRASEÑAS")
    print("=" * 70)

    pm = PasswordManager(":memory:")

    # ── Generación ──
    print(f"\n{'─' * 50}")
    print("GENERACIÓN DE CONTRASEÑAS:")
    print(f"{'─' * 50}")

    for length in [8, 12, 16, 20, 24]:
        pwd: str = pm.generate_password(length)
        strength: dict = pm.evaluate_strength(pwd)
        bar: str = "█" * (strength["score"] // 5) + "░" * (20 - strength["score"] // 5)
        print(f"  {length:2d} chars: {pwd:28s} {bar} {strength['level']:12s} ({strength['score']})")

    # ── Almacenamiento ──
    print(f"\n{'─' * 50}")
    print("ALMACENAMIENTO:")
    print(f"{'─' * 50}")

    pm.add_entry("GitHub", "dev@mail.com", pm.generate_password(20), "Cuenta principal")
    pm.add_entry("Gmail", "user@gmail.com", pm.generate_password(16), "Email personal")
    pm.add_entry("AWS", "admin", pm.generate_password(24), "Producción")
    pm.add_entry("Netflix", "familia@mail.com", pm.generate_password(12), "Plan familiar")
    pm.add_entry("GitLab", "dev@mail.com", pm.generate_password(18), "Repositorios privados")

    entries = pm.list_entries()
    print(f"\n  Entradas almacenadas: {len(entries)}")
    for e in entries:
        print(f"    • {e['service']:12s} ({e['username']})")

    # ── Búsqueda ──
    print(f"\n{'─' * 50}")
    print("BÚSQUEDA:")
    print(f"{'─' * 50}")

    results = pm.search("git")
    print(f'  search("git") → {len(results)} resultado(s):')
    for r in results:
        print(f"    • {r['service']} ({r['username']})")

    # ── Obtener ──
    entry = pm.get_entry("GitHub")
    if entry:
        print(f"\n  get('GitHub'):")
        print(f"    Service:  {entry['service']}")
        print(f"    Username: {entry['username']}")
        print(f"    Password: {entry['password'][:4]}{'*' * 12} (parcial)")

    # ── Exportar ──
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        csv_path = f.name
    count = pm.export_csv(csv_path)
    print(f"\n  Exportado a CSV: {count} entradas → {csv_path}")
    os.unlink(csv_path)

    # ═══════════════════════════════════════════════════════
    # TESTS
    # ═══════════════════════════════════════════════════════
    print(f"\n{'=' * 70}")
    print("TESTS:")
    print(f"{'=' * 70}")

    pm = PasswordManager(":memory:")

    # Test 1: Generación de longitud correcta
    pwd = pm.generate_password(16)
    assert len(pwd) == 16, f"Esperado 16, obtenido {len(pwd)}"
    print("  [PASS] Test 1: Generación longitud=16 correcta")

    # Test 2: Contiene todos los tipos
    pwd = pm.generate_password(20)
    has_upper = any(c in string.ascii_uppercase for c in pwd)
    has_lower = any(c in string.ascii_lowercase for c in pwd)
    has_digit = any(c in string.digits for c in pwd)
    has_symbol = any(c in "!@#$%^&*()-_=+[]{}|;:,.<>?" for c in pwd)
    assert has_upper and has_lower and has_digit and has_symbol
    print("  [PASS] Test 2: Contiene mayúsculas, minúsculas, dígitos y símbolos")

    # Test 3: Longitud mínima
    try:
        pm.generate_password(2)
        assert False, "Debería lanzar ValueError"
    except ValueError:
        pass
    print("  [PASS] Test 3: Longitud < 4 → ValueError")

    # Test 4: Fortaleza — contraseña fuerte
    strength = pm.evaluate_strength("Xk9$mL2pQr7#Hn4j")
    assert strength["score"] >= 70
    assert strength["level"] in ("Fuerte", "Muy fuerte")
    print(f"  [PASS] Test 4: Contraseña fuerte → {strength['level']} ({strength['score']})")

    # Test 5: Fortaleza — contraseña débil
    strength = pm.evaluate_strength("1234")
    assert strength["score"] < 40
    assert strength["level"] == "Débil"
    print(f"  [PASS] Test 5: Contraseña débil → {strength['level']} ({strength['score']})")

    # Test 6: Añadir y obtener entrada
    pm.add_entry("TestService", "testuser", "MyP@ssw0rd!", "Notas test")
    entry = pm.get_entry("TestService")
    assert entry is not None
    assert entry["password"] == "MyP@ssw0rd!"
    assert entry["username"] == "testuser"
    print("  [PASS] Test 6: add_entry + get_entry funciona")

    # Test 7: Listar entradas (sin contraseña)
    entries = pm.list_entries()
    assert len(entries) == 1
    assert "password" not in entries[0]
    assert "password_b64" not in entries[0]
    print("  [PASS] Test 7: list_entries no muestra contraseñas")

    # Test 8: Búsqueda
    pm.add_entry("GitHub", "dev", "pass123")
    pm.add_entry("GitLab", "dev", "pass456")
    results = pm.search("git")
    assert len(results) == 2
    print("  [PASS] Test 8: search('git') encuentra 2 resultados")

    # Test 9: Eliminar entrada
    deleted = pm.delete_entry("TestService")
    assert deleted
    assert pm.get_entry("TestService") is None
    deleted2 = pm.delete_entry("NoExiste")
    assert not deleted2
    print("  [PASS] Test 9: delete_entry funciona (existente y no existente)")

    # Test 10: Exportar CSV
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        csv_path = f.name
    count = pm.export_csv(csv_path)
    assert count == 2  # GitHub + GitLab
    content = Path(csv_path).read_text()
    assert "GitHub" in content
    assert "GitLab" in content
    os.unlink(csv_path)
    print(f"  [PASS] Test 10: export_csv exporta {count} entradas")

    print(f"\n  Todos los tests pasaron correctamente.")


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

def crear_parser() -> argparse.ArgumentParser:
    """Crea el parser CLI con subcomandos."""
    parser = argparse.ArgumentParser(prog="password_manager", description="Gestor de contraseñas CLI")
    sub = parser.add_subparsers(dest="command")

    gen = sub.add_parser("generate", help="Genera una contraseña")
    gen.add_argument("--length", "-l", type=int, default=16)
    gen.add_argument("--no-symbols", action="store_true")

    add = sub.add_parser("add", help="Añade una entrada")
    add.add_argument("--service", "-s", required=True)
    add.add_argument("--username", "-u", required=True)
    add.add_argument("--password", "-p")
    add.add_argument("--notes", "-n", default="")

    sub.add_parser("list", help="Lista entradas")

    get = sub.add_parser("get", help="Obtiene una entrada")
    get.add_argument("service")

    srch = sub.add_parser("search", help="Busca entradas")
    srch.add_argument("query")

    dele = sub.add_parser("delete", help="Elimina una entrada")
    dele.add_argument("service")

    exp = sub.add_parser("export", help="Exporta a CSV")
    exp.add_argument("--output", "-o", default="passwords.csv")

    return parser


if __name__ == "__main__":
    if len(sys.argv) > 1:
        parser = crear_parser()
        args = parser.parse_args()
        pm = PasswordManager()

        if args.command == "generate":
            pwd = pm.generate_password(args.length, symbols=not args.no_symbols)
            s = pm.evaluate_strength(pwd)
            print(f"  Contraseña: {pwd}")
            print(f"  Fortaleza:  {s['level']} ({s['score']})")

        elif args.command == "add":
            pwd = args.password or pm.generate_password(16)
            pm.add_entry(args.service, args.username, pwd, args.notes)
            print(f"  Guardado: {args.service} ({args.username})")

        elif args.command == "list":
            for e in pm.list_entries():
                print(f"  {e['service']:20s} {e['username']}")

        elif args.command == "get":
            e = pm.get_entry(args.service)
            if e:
                print(f"  Service:  {e['service']}")
                print(f"  Username: {e['username']}")
                print(f"  Password: {e['password']}")
            else:
                print(f"  No encontrado: {args.service}")

        elif args.command == "search":
            for e in pm.search(args.query):
                print(f"  {e['service']:20s} {e['username']}")

        elif args.command == "delete":
            if pm.delete_entry(args.service):
                print(f"  Eliminado: {args.service}")
            else:
                print(f"  No encontrado: {args.service}")

        elif args.command == "export":
            n = pm.export_csv(args.output)
            print(f"  Exportadas {n} entradas → {args.output}")
        else:
            parser.print_help()
    else:
        ejecutar_demo_y_tests()
