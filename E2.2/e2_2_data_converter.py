"""
E2.2 — Conversor Multiformato: CSV → JSON + Markdown + HTML
=============================================================
Transforma datos CSV de empleados en tres formatos de salida
distintos, demostrando la capacidad de los LLMs para generar
código de manipulación de datos complejo.

Uso demo + tests:
    python e2_2_data_converter.py

Uso con archivo CSV:
    python e2_2_data_converter.py --input datos.csv --output-dir ./output

Solo validación:
    python e2_2_data_converter.py --input datos.csv --validate

Dependencias: Solo librería estándar.
"""

import argparse
import csv
import io
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from statistics import mean
from typing import Optional

__version__ = "1.0.0"

# ═══════════════════════════════════════════════════════════════
# DATOS DE EJEMPLO (con anomalías intencionadas)
# ═══════════════════════════════════════════════════════════════

SAMPLE_CSV = """nombre,email,departamento,salario,fecha_ingreso
Ana López,ana.lopez@empresa.com,Ingeniería,65000,2023-03-15
Carlos Ruiz,carlos.ruiz@empresa.com,Ingeniería,72000,2022-01-10
María García,maria.garcia@empresa.com,Marketing,48000,2023-06-20
Pedro Sánchez,pedro.sanchez@empresa.com,Marketing,52000,2021-09-01
Juan Torres,juan.torres.invalid,Ventas,45000,2023-11-05
Laura Martín,laura.martin@empresa.com,Ventas,38000,2024-01-15
Roberto Díaz,roberto.diaz@empresa.com,Ingeniería,80000,2020-05-20
Elena Fernández,elena.fernandez@empresa.com,RRHH,-5000,2023-08-10
Pablo Moreno,pablo.moreno@empresa.com,RRHH,42000,2022-04-12
Sofía Navarro,sofia.navarro@empresa.com,Marketing,55000,2021-11-30
,vacio@empresa.com,Ventas,35000,2024-02-01
Diego Romero,diego.romero@empresa.com,Ingeniería,85000,2019-07-22"""


# ═══════════════════════════════════════════════════════════════
# CLASE PRINCIPAL
# ═══════════════════════════════════════════════════════════════

class DataConverter:
    """Conversor multiformato de datos CSV.

    Parsea datos CSV y los transforma a JSON agrupado, informe Markdown
    y tabla HTML estilizada. Incluye validación de anomalías.

    Attributes:
        records: Lista de diccionarios con los datos parseados.
        headers: Lista de nombres de columnas.

    Examples:
        >>> converter = DataConverter(SAMPLE_CSV)
        >>> len(converter.records) > 0
        True
    """

    DEPT_COLORS: dict[str, str] = {
        "Ingeniería": "#3b82f6",
        "Marketing": "#22c55e",
        "Ventas": "#f97316",
        "RRHH": "#a855f7",
    }

    def __init__(self, csv_data: str) -> None:
        """Inicializa el conversor parseando datos CSV.

        Args:
            csv_data: String con datos CSV (headers en primera línea).

        Raises:
            ValueError: Si el CSV está vacío o no tiene datos.
        """
        csv_data = csv_data.strip()
        if not csv_data:
            raise ValueError("Los datos CSV no pueden estar vacíos")

        reader = csv.DictReader(io.StringIO(csv_data))
        self.headers: list[str] = reader.fieldnames or []
        self.records: list[dict] = []

        for row in reader:
            record: dict = {}
            for key, value in row.items():
                if key == "salario":
                    try:
                        record[key] = int(value)
                    except (ValueError, TypeError):
                        record[key] = 0
                else:
                    record[key] = (value or "").strip()
            self.records.append(record)

        if not self.records:
            raise ValueError("El CSV no contiene datos")

    def to_json_grouped(self) -> str:
        """Genera JSON agrupado por departamento.

        Returns:
            String JSON con indentación de 2 espacios.
            Estructura: {"departamento": [{"nombre": ..., ...}, ...]}
        """
        grouped: dict[str, list[dict]] = {}

        for record in self.records:
            dept: str = record.get("departamento", "Sin departamento")
            if dept not in grouped:
                grouped[dept] = []
            grouped[dept].append(record)

        return json.dumps(grouped, ensure_ascii=False, indent=2)

    def to_markdown_report(self) -> str:
        """Genera un informe completo en formato Markdown.

        Returns:
            String con informe Markdown incluyendo tabla de empleados,
            estadísticas por departamento y resumen global.
        """
        lines: list[str] = []
        lines.append("# Informe de Empleados")
        lines.append("")
        lines.append(f"*Generado el {datetime.now().strftime('%Y-%m-%d %H:%M')}*")
        lines.append("")

        # Tabla de empleados
        lines.append("## Listado de Empleados")
        lines.append("")
        lines.append("| Nombre | Email | Departamento | Salario | Ingreso |")
        lines.append("|---|---|---|---|---|")

        for r in self.records:
            nombre: str = r.get("nombre", "") or "(vacío)"
            email: str = r.get("email", "")
            dept: str = r.get("departamento", "")
            salario: int = r.get("salario", 0)
            fecha: str = r.get("fecha_ingreso", "")
            lines.append(f"| {nombre} | {email} | {dept} | {salario:,} | {fecha} |")

        lines.append("")

        # Estadísticas por departamento
        lines.append("## Estadísticas por Departamento")
        lines.append("")

        dept_stats: dict[str, list[int]] = {}
        for r in self.records:
            dept = r.get("departamento", "Sin departamento")
            salario = r.get("salario", 0)
            if dept not in dept_stats:
                dept_stats[dept] = []
            dept_stats[dept].append(salario)

        lines.append("| Departamento | Empleados | Salario Medio | Mínimo | Máximo |")
        lines.append("|---|---|---|---|---|")

        for dept in sorted(dept_stats.keys()):
            salarios = dept_stats[dept]
            n: int = len(salarios)
            media: float = mean(salarios) if salarios else 0
            minimo: int = min(salarios) if salarios else 0
            maximo: int = max(salarios) if salarios else 0
            lines.append(f"| {dept} | {n} | {media:,.0f} | {minimo:,} | {maximo:,} |")

        lines.append("")

        # Resumen global
        lines.append("## Resumen Global")
        lines.append("")
        all_salarios: list[int] = [r.get("salario", 0) for r in self.records]
        lines.append(f"- **Total empleados**: {len(self.records)}")
        lines.append(f"- **Departamentos**: {len(dept_stats)}")
        lines.append(f"- **Salario medio global**: {mean(all_salarios):,.0f}")
        lines.append(f"- **Rango salarial**: {min(all_salarios):,} — {max(all_salarios):,}")
        lines.append("")

        return "\n".join(lines)

    def to_html_table(self) -> str:
        """Genera una tabla HTML completa y estilizada.

        Returns:
            String con documento HTML completo incluyendo DOCTYPE,
            CSS embebido con filas coloreadas por departamento y responsive.
        """
        dept_colors = self.DEPT_COLORS

        rows_html: list[str] = []
        for r in self.records:
            dept: str = r.get("departamento", "")
            color: str = dept_colors.get(dept, "#64748b")
            nombre: str = _escape_html(r.get("nombre", "") or "(vacío)")
            email: str = _escape_html(r.get("email", ""))
            salario: int = r.get("salario", 0)
            fecha: str = _escape_html(r.get("fecha_ingreso", ""))

            rows_html.append(
                f'        <tr style="border-left: 4px solid {color};">'
                f"<td>{nombre}</td><td>{email}</td>"
                f"<td><span class='dept' style='background:{color}20;color:{color};'>{_escape_html(dept)}</span></td>"
                f"<td class='num'>{salario:,}</td><td>{fecha}</td></tr>"
            )

        now: str = datetime.now().strftime("%Y-%m-%d %H:%M")

        return f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Informe de Empleados</title>
<style>
  body {{ font-family: 'Segoe UI', system-ui, sans-serif; background: #f8fafc; color: #1e293b; padding: 24px; }}
  .container {{ max-width: 960px; margin: 0 auto; }}
  h1 {{ color: #1e293b; margin-bottom: 4px; }}
  .date {{ color: #64748b; font-size: 14px; margin-bottom: 24px; }}
  .table-wrapper {{ overflow-x: auto; border-radius: 12px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
  table {{ width: 100%; border-collapse: collapse; background: white; }}
  th {{ background: #1e293b; color: white; padding: 12px 16px; text-align: left; font-size: 13px; text-transform: uppercase; letter-spacing: 0.5px; }}
  td {{ padding: 10px 16px; border-bottom: 1px solid #e2e8f0; font-size: 14px; }}
  tr:hover {{ background: #f1f5f9; }}
  .num {{ text-align: right; font-family: monospace; }}
  .dept {{ padding: 3px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; }}
  .footer {{ margin-top: 16px; color: #94a3b8; font-size: 12px; text-align: center; }}
</style>
</head>
<body>
<div class="container">
  <h1>Informe de Empleados</h1>
  <p class="date">Generado el {now}</p>
  <div class="table-wrapper">
    <table>
      <thead>
        <tr><th>Nombre</th><th>Email</th><th>Departamento</th><th>Salario</th><th>Ingreso</th></tr>
      </thead>
      <tbody>
{chr(10).join(rows_html)}
      </tbody>
    </table>
  </div>
  <p class="footer">Total: {len(self.records)} empleados | Generado automáticamente</p>
</div>
</body>
</html>"""

    def validate(self) -> list[str]:
        """Detecta anomalías en los datos.

        Revisa:
        - Emails sin @
        - Salarios negativos o > 200000
        - Nombres vacíos

        Returns:
            Lista de strings describiendo cada anomalía encontrada.
        """
        issues: list[str] = []

        for i, r in enumerate(self.records, 1):
            nombre: str = r.get("nombre", "")
            email: str = r.get("email", "")
            salario: int = r.get("salario", 0)

            if not nombre or not nombre.strip():
                issues.append(f"⚠ Nombre vacío (fila {i})")

            if email and "@" not in email:
                issues.append(f"⚠ Email inválido: {email} (fila {i})")

            if salario < 0:
                issues.append(f"⚠ Salario negativo: {salario:,} (fila {i})")
            elif salario > 200000:
                issues.append(f"⚠ Salario inusualmente alto: {salario:,} (fila {i})")

        return issues

    def summary(self) -> dict:
        """Genera un resumen compacto de los datos.

        Returns:
            Diccionario con total_empleados, departamentos, salario_medio,
            y anomalías encontradas.
        """
        salarios: list[int] = [r.get("salario", 0) for r in self.records]
        depts: set[str] = {r.get("departamento", "") for r in self.records}

        return {
            "total_empleados": len(self.records),
            "departamentos": sorted(depts),
            "salario_medio": round(mean(salarios), 2) if salarios else 0,
            "anomalias": self.validate(),
        }


def _escape_html(text: str) -> str:
    """Escapa caracteres especiales HTML."""
    return (text.replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

def crear_parser() -> argparse.ArgumentParser:
    """Crea el parser CLI."""
    parser = argparse.ArgumentParser(
        prog="data_converter",
        description="Convierte CSV a JSON, Markdown y HTML.",
    )
    parser.add_argument("--input", "-i", help="Archivo CSV de entrada")
    parser.add_argument("--output-dir", "-o", help="Directorio para guardar los archivos generados")
    parser.add_argument("--validate", "-V", action="store_true", help="Solo mostrar anomalías")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main() -> int:
    """Punto de entrada CLI."""
    parser = crear_parser()
    args = parser.parse_args()

    # Cargar datos
    if args.input:
        try:
            csv_data = Path(args.input).read_text(encoding="utf-8")
        except FileNotFoundError:
            print(f"Error: archivo no encontrado: {args.input}", file=sys.stderr)
            return 1
    else:
        csv_data = SAMPLE_CSV

    converter = DataConverter(csv_data)

    # Solo validación
    if args.validate:
        issues = converter.validate()
        if issues:
            print("Anomalías encontradas:")
            for issue in issues:
                print(f"  {issue}")
        else:
            print("No se encontraron anomalías.")
        return 0

    # Guardar archivos
    if args.output_dir:
        out = Path(args.output_dir)
        out.mkdir(parents=True, exist_ok=True)
        (out / "datos.json").write_text(converter.to_json_grouped(), encoding="utf-8")
        (out / "informe.md").write_text(converter.to_markdown_report(), encoding="utf-8")
        (out / "tabla.html").write_text(converter.to_html_table(), encoding="utf-8")
        print(f"Archivos generados en {out}/:")
        print(f"  datos.json  ({len(converter.to_json_grouped())} bytes)")
        print(f"  informe.md  ({len(converter.to_markdown_report())} bytes)")
        print(f"  tabla.html  ({len(converter.to_html_table())} bytes)")
        return 0

    # Demo (sin argumentos con datos de ejemplo se maneja en __main__)
    return 0


# ═══════════════════════════════════════════════════════════════
# DEMO Y TESTS
# ═══════════════════════════════════════════════════════════════

def ejecutar_demo_y_tests() -> None:
    """Ejecuta demo de los 3 formatos + validación + 10 tests."""

    print("=" * 70)
    print("E2.2 — DEMO: CONVERSOR MULTIFORMATO")
    print("=" * 70)

    converter = DataConverter(SAMPLE_CSV)

    # ── JSON ──
    json_output: str = converter.to_json_grouped()
    print(f"\n{'─' * 50}")
    print("JSON AGRUPADO POR DEPARTAMENTO (extracto):")
    print(f"{'─' * 50}")
    # Mostrar primeras 20 líneas
    json_lines = json_output.split("\n")
    for line in json_lines[:20]:
        print(f"  {line}")
    if len(json_lines) > 20:
        print(f"  ... ({len(json_lines) - 20} líneas más)")

    # ── Markdown ──
    md_output: str = converter.to_markdown_report()
    print(f"\n{'─' * 50}")
    print("INFORME MARKDOWN (extracto):")
    print(f"{'─' * 50}")
    md_lines = md_output.split("\n")
    for line in md_lines[:25]:
        print(f"  {line}")
    if len(md_lines) > 25:
        print(f"  ... ({len(md_lines) - 25} líneas más)")

    # ── HTML ──
    html_output: str = converter.to_html_table()
    print(f"\n{'─' * 50}")
    print("TABLA HTML:")
    print(f"{'─' * 50}")
    print(f"  Documento HTML generado: {len(html_output)} caracteres")
    print(f"  Contiene <table>: {'Sí' if '<table>' in html_output else 'No'}")
    print(f"  Contiene <!DOCTYPE>: {'Sí' if '<!DOCTYPE' in html_output else 'No'}")
    print(f"  Contiene CSS: {'Sí' if '<style>' in html_output else 'No'}")

    # ── Validación ──
    issues: list[str] = converter.validate()
    print(f"\n{'─' * 50}")
    print("VALIDACIÓN DE ANOMALÍAS:")
    print(f"{'─' * 50}")
    if issues:
        for issue in issues:
            print(f"  {issue}")
    else:
        print("  Sin anomalías")

    # ── Summary ──
    summ: dict = converter.summary()
    print(f"\n{'─' * 50}")
    print("RESUMEN:")
    print(f"{'─' * 50}")
    print(f"  Total empleados: {summ['total_empleados']}")
    print(f"  Departamentos: {', '.join(summ['departamentos'])}")
    print(f"  Salario medio: {summ['salario_medio']:,.2f}")
    print(f"  Anomalías: {len(summ['anomalias'])}")

    # ═══════════════════════════════════════════════════════
    # TESTS
    # ═══════════════════════════════════════════════════════
    print(f"\n{'=' * 70}")
    print("TESTS:")
    print(f"{'=' * 70}")

    c = DataConverter(SAMPLE_CSV)

    # Test 1: Parseo correcto
    assert len(c.records) == 12, f"Esperado 12 registros, obtenido {len(c.records)}"
    print("  [PASS] Test 1: Parseo CSV → 12 registros")

    # Test 2: JSON agrupado tiene 4 departamentos
    json_data = json.loads(c.to_json_grouped())
    assert len(json_data) == 4, f"Esperado 4 departamentos, obtenido {len(json_data)}"
    print("  [PASS] Test 2: JSON agrupado → 4 departamentos")

    # Test 3: JSON es parseable
    try:
        json.loads(c.to_json_grouped())
        print("  [PASS] Test 3: JSON es parseable")
    except json.JSONDecodeError:
        assert False, "JSON no es parseable"

    # Test 4: Markdown contiene tabla
    md = c.to_markdown_report()
    pipe_lines = [l for l in md.split("\n") if "|" in l]
    assert len(pipe_lines) >= 14, f"Esperado ≥14 líneas con |, obtenido {len(pipe_lines)}"
    print("  [PASS] Test 4: Markdown contiene tabla")

    # Test 5: Markdown contiene estadísticas
    assert "Estadísticas por Departamento" in md
    assert "Resumen Global" in md
    print("  [PASS] Test 5: Markdown contiene estadísticas")

    # Test 6: HTML contiene <table>
    html = c.to_html_table()
    assert "<table>" in html and "<th>" in html
    print("  [PASS] Test 6: HTML contiene <table> y <th>")

    # Test 7: HTML es documento completo
    assert "<!DOCTYPE html>" in html
    assert "</html>" in html
    print("  [PASS] Test 7: HTML es documento completo")

    # Test 8: Validación detecta email inválido
    issues = c.validate()
    email_issues = [i for i in issues if "Email" in i]
    assert len(email_issues) >= 1, "Debe detectar al menos 1 email inválido"
    print("  [PASS] Test 8: Validación detecta email inválido")

    # Test 9: Validación detecta salario negativo
    salary_issues = [i for i in issues if "negativo" in i.lower()]
    assert len(salary_issues) >= 1, "Debe detectar al menos 1 salario negativo"
    print("  [PASS] Test 9: Validación detecta salario negativo")

    # Test 10: Summary tiene claves correctas
    s = c.summary()
    assert "total_empleados" in s
    assert "departamentos" in s
    assert "salario_medio" in s
    assert "anomalias" in s
    assert s["total_empleados"] == 12
    print("  [PASS] Test 10: Summary tiene claves correctas")

    print(f"\n  Todos los tests pasaron correctamente.")


# ═══════════════════════════════════════════════════════════════
# PUNTO DE ENTRADA
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    if len(sys.argv) > 1:
        sys.exit(main())
    else:
        ejecutar_demo_y_tests()
