"""
E3.5 — Cadena de Prompts: Sistema de Biblioteca en 5 Pasos
=============================================================
Cada sección fue generada por un prompt encadenado que construye
sobre el output del anterior. Demuestra Prompt Chaining.

Uso: python e3_5_library_system.py

Dependencias: Solo librería estándar.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Optional
import json

__version__ = "1.0.0"


# ═══════════════════════════════════════════════════════════════
# PROMPT 1/5 — MODELO DE DATOS
# ═══════════════════════════════════════════════════════════════

@dataclass
class Book:
    """Libro de la biblioteca."""
    isbn: str
    title: str
    author: str
    year: int
    available: bool = True

    def __str__(self) -> str:
        status = "✅" if self.available else "❌"
        return f"{status} [{self.isbn}] {self.title} — {self.author} ({self.year})"


@dataclass
class Member:
    """Miembro de la biblioteca."""
    id: str
    name: str
    email: str
    active: bool = True

    def __str__(self) -> str:
        return f"[{self.id}] {self.name} ({self.email})"


@dataclass
class Loan:
    """Préstamo de un libro."""
    id: str
    book_isbn: str
    member_id: str
    loan_date: str
    return_date: Optional[str] = None
    returned: bool = False

    def __str__(self) -> str:
        status = "Devuelto" if self.returned else "Activo"
        return f"[{self.id}] {self.book_isbn} → {self.member_id} ({status})"


# ═══════════════════════════════════════════════════════════════
# PROMPT 2/5 — REPOSITORIO (CRUD)
# ═══════════════════════════════════════════════════════════════
# PROMPT 3/5 — LÓGICA DE PRÉSTAMOS
# PROMPT 4/5 — ESTADÍSTICAS
# ═══════════════════════════════════════════════════════════════

class Library:
    """Sistema de biblioteca completo.

    Construido en 3 prompts encadenados:
    - Prompt 2: CRUD básico (add, find, get)
    - Prompt 3: Préstamos (loan, return, overdue)
    - Prompt 4: Estadísticas (get_stats)
    """

    def __init__(self) -> None:
        self.books: dict[str, Book] = {}
        self.members: dict[str, Member] = {}
        self.loans: list[Loan] = []
        self._loan_counter: int = 0

    # ── Prompt 2: CRUD ──

    def add_book(self, isbn: str, title: str, author: str, year: int) -> Book:
        """Añade un libro a la biblioteca."""
        book = Book(isbn=isbn, title=title, author=author, year=year)
        self.books[isbn] = book
        return book

    def add_member(self, id: str, name: str, email: str) -> Member:
        """Registra un nuevo miembro."""
        member = Member(id=id, name=name, email=email)
        self.members[id] = member
        return member

    def find_book(self, query: str) -> list[Book]:
        """Busca libros por título, autor o ISBN (case-insensitive)."""
        q = query.lower()
        return [b for b in self.books.values()
                if q in b.title.lower() or q in b.author.lower() or q in b.isbn.lower()]

    def find_member(self, query: str) -> list[Member]:
        """Busca miembros por nombre, email o ID."""
        q = query.lower()
        return [m for m in self.members.values()
                if q in m.name.lower() or q in m.email.lower() or q in m.id.lower()]

    def get_available_books(self) -> list[Book]:
        """Devuelve libros disponibles."""
        return [b for b in self.books.values() if b.available]

    def get_all_books(self) -> list[Book]:
        """Devuelve todos los libros."""
        return list(self.books.values())

    def get_all_members(self) -> list[Member]:
        """Devuelve todos los miembros."""
        return list(self.members.values())

    # ── Prompt 3: Préstamos ──

    def loan_book(self, isbn: str, member_id: str) -> Optional[Loan]:
        """Presta un libro a un miembro.

        Args:
            isbn: ISBN del libro.
            member_id: ID del miembro.

        Returns:
            Loan creado, o None si el libro no está disponible.
        """
        book = self.books.get(isbn)
        member = self.members.get(member_id)
        if not book or not member or not book.available or not member.active:
            return None

        self._loan_counter += 1
        loan = Loan(
            id=f"L{self._loan_counter:04d}",
            book_isbn=isbn,
            member_id=member_id,
            loan_date=datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        )
        book.available = False
        self.loans.append(loan)
        return loan

    def return_book(self, loan_id: str) -> bool:
        """Devuelve un libro prestado.

        Args:
            loan_id: ID del préstamo.

        Returns:
            True si se devolvió correctamente.
        """
        for loan in self.loans:
            if loan.id == loan_id and not loan.returned:
                loan.returned = True
                loan.return_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
                book = self.books.get(loan.book_isbn)
                if book:
                    book.available = True
                return True
        return False

    def get_active_loans(self) -> list[Loan]:
        """Devuelve préstamos activos (no devueltos)."""
        return [l for l in self.loans if not l.returned]

    def get_member_loans(self, member_id: str) -> list[Loan]:
        """Devuelve préstamos de un miembro."""
        return [l for l in self.loans if l.member_id == member_id]

    def get_overdue_loans(self, days: int = 14) -> list[Loan]:
        """Devuelve préstamos vencidos (más de N días sin devolver)."""
        cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
        return [l for l in self.loans if not l.returned and l.loan_date < cutoff]

    # ── Prompt 4: Estadísticas ──

    def get_stats(self) -> dict:
        """Devuelve estadísticas completas de la biblioteca.

        Returns:
            Dict con total_books, available_books, total_members,
            active_loans, overdue_loans, most_loaned_books, most_active_members.
        """
        # Conteo de préstamos por libro
        book_loan_count: dict[str, int] = {}
        member_loan_count: dict[str, int] = {}

        for loan in self.loans:
            book_loan_count[loan.book_isbn] = book_loan_count.get(loan.book_isbn, 0) + 1
            member_loan_count[loan.member_id] = member_loan_count.get(loan.member_id, 0) + 1

        # Top 3 libros más prestados
        top_books = sorted(book_loan_count.items(), key=lambda x: x[1], reverse=True)[:3]
        most_loaned = []
        for isbn, count in top_books:
            book = self.books.get(isbn)
            most_loaned.append({"isbn": isbn, "title": book.title if book else "?", "loans": count})

        # Top 3 miembros más activos
        top_members = sorted(member_loan_count.items(), key=lambda x: x[1], reverse=True)[:3]
        most_active = []
        for mid, count in top_members:
            member = self.members.get(mid)
            most_active.append({"id": mid, "name": member.name if member else "?", "loans": count})

        return {
            "total_books": len(self.books),
            "available_books": len(self.get_available_books()),
            "total_members": len(self.members),
            "active_loans": len(self.get_active_loans()),
            "overdue_loans": len(self.get_overdue_loans()),
            "total_loans_ever": len(self.loans),
            "most_loaned_books": most_loaned,
            "most_active_members": most_active,
        }


# ═══════════════════════════════════════════════════════════════
# PROMPT 5/5 — DEMO + TESTS
# ═══════════════════════════════════════════════════════════════

def ejecutar_demo_y_tests() -> None:
    """Demo completa del sistema + 10 tests."""

    print("=" * 70)
    print("E3.5 — DEMO: SISTEMA DE BIBLIOTECA (5 prompts encadenados)")
    print("=" * 70)

    lib = Library()

    # ── Paso 1: Datos ──
    print(f"\n{'─' * 50}")
    print("Prompt 1/5: Modelo de datos ✅")
    print("Prompt 2/5: Añadiendo libros y miembros...")
    print(f"{'─' * 50}")

    books_data = [
        ("978-0-13-468599-1", "Clean Code", "Robert C. Martin", 2008),
        ("978-0-20-161622-4", "The Pragmatic Programmer", "David Thomas", 2019),
        ("978-0-59-651798-2", "JavaScript: The Good Parts", "Douglas Crockford", 2008),
        ("978-0-13-235088-4", "Clean Architecture", "Robert C. Martin", 2017),
        ("978-1-49-195016-0", "Fluent Python", "Luciano Ramalho", 2022),
        ("978-0-59-680948-5", "Learning Python", "Mark Lutz", 2013),
        ("978-1-09-813611-5", "The Rust Programming Language", "Steve Klabnik", 2022),
        ("978-0-13-711006-3", "Design Patterns", "Gang of Four", 1994),
    ]
    for isbn, title, author, year in books_data:
        lib.add_book(isbn, title, author, year)

    members_data = [
        ("M001", "Ana García", "ana@mail.com"),
        ("M002", "Carlos López", "carlos@mail.com"),
        ("M003", "María Ruiz", "maria@mail.com"),
        ("M004", "Pedro Martín", "pedro@mail.com"),
    ]
    for mid, name, email in members_data:
        lib.add_member(mid, name, email)

    print(f"  📚 {len(lib.get_all_books())} libros añadidos")
    print(f"  👤 {len(lib.get_all_members())} miembros registrados")

    # ── Paso 3: Préstamos ──
    print(f"\n{'─' * 50}")
    print("Prompt 3/5: Realizando préstamos...")
    print(f"{'─' * 50}")

    loans = [
        ("978-0-13-468599-1", "M001"),  # Clean Code → Ana
        ("978-0-20-161622-4", "M001"),  # Pragmatic → Ana
        ("978-0-59-651798-2", "M002"),  # JS Good Parts → Carlos
        ("978-0-13-235088-4", "M003"),  # Clean Arch → María
        ("978-1-49-195016-0", "M002"),  # Fluent Python → Carlos
    ]
    loan_ids: list[str] = []
    for isbn, mid in loans:
        loan = lib.loan_book(isbn, mid)
        if loan:
            book = lib.books[isbn]
            member = lib.members[mid]
            print(f"  📖 {book.title} → {member.name} [{loan.id}]")
            loan_ids.append(loan.id)

    # Devolver 2
    print(f"\n  Devolviendo 2 libros:")
    for lid in loan_ids[:2]:
        lib.return_book(lid)
        loan = next(l for l in lib.loans if l.id == lid)
        book = lib.books[loan.book_isbn]
        print(f"  ↩️  {book.title} devuelto [{lid}]")

    # ── Paso 4: Estadísticas ──
    print(f"\n{'─' * 50}")
    print("Prompt 4/5: Estadísticas ✅")
    print(f"{'─' * 50}")

    stats = lib.get_stats()
    print(f"  📚 Total libros:     {stats['total_books']}")
    print(f"  📗 Disponibles:      {stats['available_books']}")
    print(f"  👤 Miembros:         {stats['total_members']}")
    print(f"  📖 Préstamos activos: {stats['active_loans']}")
    print(f"  📊 Total histórico:   {stats['total_loans_ever']}")

    print(f"\n  📈 Libros más prestados:")
    for b in stats["most_loaned_books"]:
        print(f"     {b['title']}: {b['loans']} préstamo(s)")

    print(f"\n  🏆 Miembros más activos:")
    for m in stats["most_active_members"]:
        print(f"     {m['name']}: {m['loans']} préstamo(s)")

    # ── Búsqueda ──
    print(f"\n{'─' * 50}")
    print("Prompt 5/5: Búsqueda y tests...")
    print(f"{'─' * 50}")

    results = lib.find_book("python")
    print(f'\n  Búsqueda "python": {len(results)} resultados')
    for b in results:
        print(f"    {b}")

    # ═══════════════════════════════════════════════════════
    # TESTS
    # ═══════════════════════════════════════════════════════
    print(f"\n{'=' * 70}")
    print("TESTS:")
    print(f"{'=' * 70}")

    lib2 = Library()

    # Test 1: Modelo de datos
    b = Book("123", "Test", "Author", 2024)
    assert b.isbn == "123" and b.available is True
    print("  [PASS] Test 1: Dataclass Book funciona")

    # Test 2: Add book y member
    lib2.add_book("ISBN1", "Libro 1", "Autor 1", 2020)
    lib2.add_member("M01", "Test User", "test@mail.com")
    assert len(lib2.get_all_books()) == 1
    assert len(lib2.get_all_members()) == 1
    print("  [PASS] Test 2: add_book + add_member")

    # Test 3: Find book
    lib2.add_book("ISBN2", "Python Master", "Author X", 2023)
    results = lib2.find_book("python")
    assert len(results) == 1 and results[0].title == "Python Master"
    print("  [PASS] Test 3: find_book('python') encuentra 1 libro")

    # Test 4: Loan book
    loan = lib2.loan_book("ISBN1", "M01")
    assert loan is not None
    assert loan.book_isbn == "ISBN1"
    assert lib2.books["ISBN1"].available is False
    print("  [PASS] Test 4: loan_book marca libro como no disponible")

    # Test 5: No prestar libro no disponible
    loan2 = lib2.loan_book("ISBN1", "M01")
    assert loan2 is None
    print("  [PASS] Test 5: No presta libro ya prestado")

    # Test 6: Return book
    success = lib2.return_book(loan.id)
    assert success is True
    assert lib2.books["ISBN1"].available is True
    print("  [PASS] Test 6: return_book devuelve libro y lo marca disponible")

    # Test 7: Active loans
    lib2.loan_book("ISBN2", "M01")
    active = lib2.get_active_loans()
    assert len(active) == 1
    assert active[0].book_isbn == "ISBN2"
    print("  [PASS] Test 7: get_active_loans devuelve 1 préstamo activo")

    # Test 8: Member loans
    member_loans = lib2.get_member_loans("M01")
    assert len(member_loans) == 2  # ISBN1 (devuelto) + ISBN2 (activo)
    print("  [PASS] Test 8: get_member_loans devuelve historial completo")

    # Test 9: Stats
    stats = lib2.get_stats()
    assert stats["total_books"] == 2
    assert stats["active_loans"] == 1
    assert stats["total_loans_ever"] == 2
    assert len(stats["most_loaned_books"]) > 0
    print(f"  [PASS] Test 9: get_stats: {stats['total_books']} libros, {stats['active_loans']} activos")

    # Test 10: Cadena completa — los 5 prompts integrados
    lib3 = Library()
    lib3.add_book("A", "Book A", "Auth", 2020)
    lib3.add_member("U1", "User", "u@m.com")
    loan = lib3.loan_book("A", "U1")
    assert loan is not None
    st = lib3.get_stats()
    assert st["active_loans"] == 1
    lib3.return_book(loan.id)
    st2 = lib3.get_stats()
    assert st2["active_loans"] == 0 and st2["available_books"] == 1
    print("  [PASS] Test 10: Cadena completa: add→loan→stats→return→stats ✅")

    print(f"\n  Todos los tests pasaron correctamente.")


if __name__ == "__main__":
    ejecutar_demo_y_tests()
