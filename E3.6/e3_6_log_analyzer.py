"""
E3.6 — Integración: Analizador de Logs con Todas las Técnicas
================================================================
Combina las 5 técnicas del Módulo 3 en un solo proyecto:
- Elementos del prompt (contexto SRE, rol, restricciones)
- Zero-shot (parser sin ejemplos de código)
- Few-shot (reglas de alerta siguiendo patrón)
- Chain of Thought (pensar métricas antes de implementar)
- Cadena de prompts (4 módulos secuenciales)

Uso: python e3_6_log_analyzer.py

Dependencias: Solo librería estándar.
"""

import re
from collections import Counter
from datetime import datetime, timedelta, timezone
from typing import Callable, Optional

__version__ = "1.0.0"


# ═══════════════════════════════════════════════════════════════
# PROMPT 1/4 — LOG PARSER (zero-shot + elementos del prompt)
# ═══════════════════════════════════════════════════════════════

class LogParser:
    """Parser de logs multi-formato para monitorización de servidores.

    Soporta: Apache combined, Nginx, JSON-like, Syslog.
    Generado con zero-shot + contexto SRE + restricciones.
    """

    LEVELS = {"DEBUG", "INFO", "WARNING", "WARN", "ERROR", "CRITICAL", "FATAL"}
    LEVEL_MAP = {"WARN": "WARNING", "FATAL": "CRITICAL"}

    # Patterns
    _RE_APACHE = re.compile(
        r'(?P<ip>[\d.]+)\s+\S+\s+\S+\s+\[(?P<ts>[^\]]+)\]\s+'
        r'"(?:\w+)\s+\S+\s+\S+"\s+(?P<status>\d{3})\s+\d+'
    )
    _RE_LEVEL = re.compile(r'\b(' + '|'.join(LEVELS) + r')\b', re.IGNORECASE)
    _RE_TS_ISO = re.compile(r'\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2}')
    _RE_IP = re.compile(r'\b(\d{1,3}\.){3}\d{1,3}\b')
    _RE_SOURCE = re.compile(r'\[(web|api|db|auth|cache|app|server|nginx|apache)\]', re.IGNORECASE)

    def parse_line(self, line: str) -> Optional[dict]:
        """Parsea una línea de log en un dict normalizado.

        Args:
            line: Línea de log en cualquier formato soportado.

        Returns:
            Dict con timestamp, level, source, message, ip, status_code.
            None si la línea es malformada.
        """
        line = line.strip()
        if not line or len(line) < 10:
            return None

        entry: dict = {
            "timestamp": None, "level": "INFO", "source": "unknown",
            "message": line, "ip": None, "status_code": None,
        }

        # Extract timestamp
        ts_match = self._RE_TS_ISO.search(line)
        if ts_match:
            entry["timestamp"] = ts_match.group()

        # Apache format
        apache = self._RE_APACHE.match(line)
        if apache:
            entry["ip"] = apache.group("ip")
            entry["status_code"] = int(apache.group("status"))
            entry["source"] = "apache"
            entry["timestamp"] = entry["timestamp"] or apache.group("ts")
            sc = entry["status_code"]
            if sc >= 500:
                entry["level"] = "ERROR"
            elif sc >= 400:
                entry["level"] = "WARNING"
            return entry

        # Extract level
        lvl_match = self._RE_LEVEL.search(line)
        if lvl_match:
            lvl = lvl_match.group().upper()
            entry["level"] = self.LEVEL_MAP.get(lvl, lvl)

        # Extract IP
        ip_match = self._RE_IP.search(line)
        if ip_match:
            entry["ip"] = ip_match.group()

        # Extract source
        src_match = self._RE_SOURCE.search(line)
        if src_match:
            entry["source"] = src_match.group(1).lower()

        # Must have at least level or timestamp
        if not ts_match and not lvl_match:
            return None

        return entry

    def parse_lines(self, lines: list[str]) -> list[dict]:
        """Parsea múltiples líneas, descartando malformadas."""
        results: list[dict] = []
        for line in lines:
            parsed = self.parse_line(line)
            if parsed:
                results.append(parsed)
        return results


# ═══════════════════════════════════════════════════════════════
# PROMPT 2/4 — LOG ANALYZER (few-shot + CoT)
# ═══════════════════════════════════════════════════════════════

class LogAnalyzer:
    """Analizador de métricas de logs para SRE.

    CoT: ¿Qué métricas son útiles? → conteos por nivel/fuente/hora,
    top IPs, top errores, tasa de error.
    """

    def __init__(self) -> None:
        self.entries: list[dict] = []

    def add_entries(self, entries: list[dict]) -> None:
        """Añade entradas parseadas al analyzer."""
        self.entries.extend(entries)

    def count_by_level(self) -> dict[str, int]:
        """Conteo de logs por nivel."""
        counter: Counter = Counter()
        for e in self.entries:
            counter[e.get("level", "UNKNOWN")] += 1
        return dict(counter.most_common())

    def count_by_source(self) -> dict[str, int]:
        """Conteo de logs por fuente."""
        counter: Counter = Counter()
        for e in self.entries:
            counter[e.get("source", "unknown")] += 1
        return dict(counter.most_common())

    def count_by_hour(self) -> dict[str, int]:
        """Distribución horaria de logs."""
        counter: Counter = Counter()
        for e in self.entries:
            ts = e.get("timestamp", "")
            if ts and len(ts) >= 13:
                hour = ts[11:13] if "T" in ts or " " in ts[10:11] else "??"
                counter[hour + ":00"] += 1
        return dict(sorted(counter.items()))

    def top_ips(self, n: int = 5) -> list[tuple[str, int]]:
        """Top N IPs con más logs."""
        counter: Counter = Counter()
        for e in self.entries:
            ip = e.get("ip")
            if ip:
                counter[ip] += 1
        return counter.most_common(n)

    def top_errors(self, n: int = 5) -> list[tuple[str, int]]:
        """Top N mensajes de error más frecuentes."""
        counter: Counter = Counter()
        for e in self.entries:
            if e.get("level") in ("ERROR", "CRITICAL"):
                msg = e.get("message", "")[:80]
                counter[msg] += 1
        return counter.most_common(n)

    def error_rate(self) -> float:
        """Porcentaje de ERROR + CRITICAL sobre el total."""
        if not self.entries:
            return 0.0
        errors = sum(1 for e in self.entries if e.get("level") in ("ERROR", "CRITICAL"))
        return round(errors / len(self.entries) * 100, 2)

    def total_errors(self) -> int:
        """Total de errores (ERROR + CRITICAL)."""
        return sum(1 for e in self.entries if e.get("level") in ("ERROR", "CRITICAL"))


# ═══════════════════════════════════════════════════════════════
# PROMPT 3/4 — ALERT ENGINE (few-shot: 2 ejemplos + 3 más)
# ═══════════════════════════════════════════════════════════════

class Alert:
    """Alerta generada por una regla."""
    def __init__(self, rule_name: str, severity: str, message: str) -> None:
        self.rule_name = rule_name
        self.severity = severity
        self.message = message

    def __str__(self) -> str:
        icon = "🔴" if self.severity == "CRITICAL" else "🟡"
        return f"{icon} [{self.severity}] {self.rule_name}: {self.message}"


class AlertRule:
    """Regla de alerta evaluable contra un LogAnalyzer."""
    def __init__(self, name: str, condition_fn: Callable, severity: str) -> None:
        self.name = name
        self.condition_fn = condition_fn
        self.severity = severity


class AlertEngine:
    """Motor de alertas que evalúa reglas contra métricas."""

    def __init__(self) -> None:
        self.rules: list[AlertRule] = []

    def add_rule(self, rule: AlertRule) -> None:
        """Añade una regla de alerta."""
        self.rules.append(rule)

    def evaluate(self, analyzer: LogAnalyzer) -> list[Alert]:
        """Evalúa todas las reglas contra el analyzer.

        Returns:
            Lista de alertas disparadas.
        """
        alerts: list[Alert] = []
        for rule in self.rules:
            result = rule.condition_fn(analyzer)
            if result:
                alerts.append(Alert(rule.name, rule.severity, result))
        return alerts


def create_default_rules() -> list[AlertRule]:
    """Crea las 5 reglas predefinidas (2 few-shot + 3 nuevas)."""
    return [
        # Ejemplo A (few-shot): error_rate > 10%
        AlertRule("Error Rate Alto",
            lambda a: f"Error rate: {a.error_rate():.1f}%" if a.error_rate() > 10 else None,
            "CRITICAL"),
        # Ejemplo B (few-shot): >20 errores total
        AlertRule("Volumen de Errores",
            lambda a: f"{a.total_errors()} errores detectados" if a.total_errors() > 20 else None,
            "WARNING"),
        # Regla 3: IP dominante (>30% del tráfico)
        AlertRule("IP Dominante",
            lambda a: f"IP {a.top_ips(1)[0][0]} con {a.top_ips(1)[0][1]} logs" if a.top_ips(1) and a.top_ips(1)[0][1] > len(a.entries) * 0.3 else None,
            "WARNING"),
        # Regla 4: fuente "db" con errores
        AlertRule("Errores en Base de Datos",
            lambda a: f"{sum(1 for e in a.entries if e.get('source')=='db' and e.get('level') in ('ERROR','CRITICAL'))} errores en DB" if any(e.get("source") == "db" and e.get("level") in ("ERROR", "CRITICAL") for e in a.entries) else None,
            "CRITICAL"),
        # Regla 5: CRITICAL > 3
        AlertRule("Logs Críticos",
            lambda a: f"{a.count_by_level().get('CRITICAL',0)} logs CRITICAL" if a.count_by_level().get("CRITICAL", 0) > 3 else None,
            "CRITICAL"),
    ]


# ═══════════════════════════════════════════════════════════════
# PROMPT 4/4 — REPORT GENERATOR (cadena final)
# ═══════════════════════════════════════════════════════════════

class ReportGenerator:
    """Genera informes de texto a partir del análisis."""

    def generate(self, analyzer: LogAnalyzer, alerts: list[Alert]) -> str:
        """Genera informe completo en texto plano."""
        lines: list[str] = []
        lines.append("=" * 60)
        lines.append("INFORME DE ANÁLISIS DE LOGS")
        lines.append("=" * 60)

        # Resumen
        lines.append(f"\nTotal de entradas: {len(analyzer.entries)}")
        lines.append(f"Tasa de error: {analyzer.error_rate():.1f}%")
        lines.append(f"Errores totales: {analyzer.total_errors()}")

        # Por nivel
        lines.append(f"\nDistribución por nivel:")
        for level, count in analyzer.count_by_level().items():
            bar = "█" * min(count, 30)
            lines.append(f"  {level:10s} {count:4d}  {bar}")

        # Por fuente
        lines.append(f"\nDistribución por fuente:")
        for source, count in analyzer.count_by_source().items():
            lines.append(f"  {source:10s} {count:4d}")

        # Top IPs
        top = analyzer.top_ips(3)
        if top:
            lines.append(f"\nTop 3 IPs:")
            for ip, count in top:
                lines.append(f"  {ip:18s} {count} logs")

        # Alertas
        if alerts:
            lines.append(f"\n{'─' * 40}")
            lines.append(f"⚠️  ALERTAS ({len(alerts)}):")
            lines.append(f"{'─' * 40}")
            for alert in alerts:
                lines.append(f"  {alert}")
        else:
            lines.append(f"\n✅ Sin alertas activas")

        lines.append(f"\n{'=' * 60}")
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
# LOGS DE TEST (30 líneas multi-formato)
# ═══════════════════════════════════════════════════════════════

SAMPLE_LOGS: list[str] = [
    '2026-03-09T08:01:12 [web] INFO Request processed successfully from 192.168.1.10',
    '2026-03-09T08:02:30 [api] INFO GET /users returned 200 from 10.0.0.5',
    '2026-03-09T08:03:45 [db] WARNING Slow query detected: 2.3s on users table',
    '2026-03-09T08:04:01 [auth] ERROR Failed login attempt from 203.0.113.50',
    '2026-03-09T08:05:22 [web] INFO Static file served from 192.168.1.10',
    '2026-03-09T08:06:10 [api] ERROR Timeout connecting to payment service from 10.0.0.5',
    '2026-03-09T08:07:33 [db] CRITICAL Connection pool exhausted on primary replica',
    '2026-03-09T08:08:45 [cache] INFO Cache hit ratio: 94.2%',
    '2026-03-09T08:09:01 [web] WARNING High memory usage: 87% on worker-3',
    '2026-03-09T08:10:15 [auth] INFO User admin@empresa.com logged in from 192.168.1.20',
    '2026-03-09T09:01:00 [api] INFO Health check OK',
    '2026-03-09T09:02:30 [web] ERROR 503 Service Unavailable from 10.0.0.15',
    '2026-03-09T09:03:12 [db] ERROR Deadlock detected on transactions table',
    '2026-03-09T09:04:45 [api] INFO POST /orders created successfully from 172.16.0.8',
    '2026-03-09T09:05:30 [auth] WARNING Multiple failed attempts from 203.0.113.50',
    '2026-03-09T09:06:01 [web] INFO Request processed from 192.168.1.10',
    '2026-03-09T09:07:22 [cache] WARNING Cache miss on session store',
    '2026-03-09T09:08:10 [db] CRITICAL Replication lag: 15 seconds',
    '2026-03-09T09:09:33 [api] ERROR Rate limit exceeded from 203.0.113.50',
    '2026-03-09T09:10:45 [web] INFO CSS bundle served from 10.0.0.5',
    '2026-03-09T10:01:00 [api] DEBUG Query plan analysis for /reports',
    '2026-03-09T10:02:12 [db] WARNING Lock wait timeout on orders table',
    '2026-03-09T10:03:30 [auth] ERROR Token expired for user session-4829',
    '2026-03-09T10:04:45 [web] INFO Image optimized and served from 192.168.1.10',
    '2026-03-09T10:05:01 [api] INFO Webhook delivered to partner-api from 10.0.0.5',
    '2026-03-09T10:06:22 [db] CRITICAL Primary database failover initiated',
    '2026-03-09T10:07:30 [cache] INFO Redis cluster rebalanced successfully',
    '2026-03-09T10:08:45 [web] ERROR Connection reset by peer from 203.0.113.50',
    # Malformadas
    'this is just random garbage text',
    '',
]


# ═══════════════════════════════════════════════════════════════
# DEMO Y TESTS
# ═══════════════════════════════════════════════════════════════

def ejecutar_demo_y_tests() -> None:
    """Demo completa: parser → analyzer → alertas → report."""

    print("=" * 70)
    print("E3.6 — DEMO: ANALIZADOR DE LOGS (Integración Módulo 3)")
    print("=" * 70)

    # ── Prompt 1: Parser ──
    print(f"\n{'─' * 50}")
    print("Prompt 1/4: LogParser (zero-shot)")
    print(f"{'─' * 50}")

    parser = LogParser()
    entries = parser.parse_lines(SAMPLE_LOGS)
    print(f"  Líneas totales:  {len(SAMPLE_LOGS)}")
    print(f"  Parseadas:       {len(entries)}")
    print(f"  Descartadas:     {len(SAMPLE_LOGS) - len(entries)}")

    # ── Prompt 2: Analyzer ──
    print(f"\n{'─' * 50}")
    print("Prompt 2/4: LogAnalyzer (CoT)")
    print(f"{'─' * 50}")

    analyzer = LogAnalyzer()
    analyzer.add_entries(entries)

    print(f"\n  Por nivel:")
    for lvl, count in analyzer.count_by_level().items():
        print(f"    {lvl:10s} {count}")

    print(f"\n  Error rate: {analyzer.error_rate():.1f}%")
    print(f"  Top IPs: {analyzer.top_ips(3)}")

    # ── Prompt 3: Alertas ──
    print(f"\n{'─' * 50}")
    print("Prompt 3/4: AlertEngine (few-shot)")
    print(f"{'─' * 50}")

    engine = AlertEngine()
    for rule in create_default_rules():
        engine.add_rule(rule)

    alerts = engine.evaluate(analyzer)
    for alert in alerts:
        print(f"  {alert}")
    if not alerts:
        print("  ✅ Sin alertas")

    # ── Prompt 4: Report ──
    print(f"\n{'─' * 50}")
    print("Prompt 4/4: ReportGenerator (cadena final)")
    print(f"{'─' * 50}")

    report = ReportGenerator()
    output = report.generate(analyzer, alerts)
    print(output)

    # ═══════════════════════════════════════════════════════
    # TESTS
    # ═══════════════════════════════════════════════════════
    print(f"\n{'=' * 70}")
    print("TESTS:")
    print(f"{'=' * 70}")

    # Test 1: Parser descarta malformadas
    p = LogParser()
    entries = p.parse_lines(SAMPLE_LOGS)
    assert len(entries) < len(SAMPLE_LOGS)
    assert len(entries) >= 25
    print(f"  [PASS] Test 1: Parser descarta malformadas ({len(SAMPLE_LOGS)}→{len(entries)})")

    # Test 2: Parser extrae niveles correctos
    levels = set(e["level"] for e in entries)
    assert "ERROR" in levels and "INFO" in levels and "CRITICAL" in levels
    print(f"  [PASS] Test 2: Parser extrae niveles: {sorted(levels)}")

    # Test 3: Parser extrae IPs
    ips = [e["ip"] for e in entries if e["ip"]]
    assert len(ips) > 10
    assert "192.168.1.10" in ips
    print(f"  [PASS] Test 3: Parser extrae {len(ips)} IPs")

    # Test 4: Parser extrae fuentes
    sources = set(e["source"] for e in entries)
    assert "web" in sources and "api" in sources and "db" in sources
    print(f"  [PASS] Test 4: Parser extrae fuentes: {sorted(sources)}")

    # Test 5: Analyzer count_by_level
    a = LogAnalyzer()
    a.add_entries(entries)
    by_level = a.count_by_level()
    assert sum(by_level.values()) == len(entries)
    print(f"  [PASS] Test 5: count_by_level suma total correcto")

    # Test 6: Analyzer error_rate
    rate = a.error_rate()
    assert 0 < rate < 100
    print(f"  [PASS] Test 6: error_rate = {rate:.1f}%")

    # Test 7: Analyzer top_ips
    top = a.top_ips(3)
    assert len(top) == 3
    assert all(isinstance(t, tuple) and len(t) == 2 for t in top)
    print(f"  [PASS] Test 7: top_ips(3) = {top}")

    # Test 8: AlertEngine evalúa reglas
    eng = AlertEngine()
    for r in create_default_rules():
        eng.add_rule(r)
    alerts = eng.evaluate(a)
    assert isinstance(alerts, list)
    print(f"  [PASS] Test 8: AlertEngine genera {len(alerts)} alerta(s)")

    # Test 9: ReportGenerator genera informe
    rpt = ReportGenerator()
    output = rpt.generate(a, alerts)
    assert "INFORME" in output
    assert "error" in output.lower() or "Error" in output
    assert len(output) > 200
    print(f"  [PASS] Test 9: Report genera {len(output)} chars")

    # Test 10: Cadena completa parser→analyzer→alerts→report
    p2 = LogParser()
    e2 = p2.parse_lines(["2026-03-09T12:00:00 [web] ERROR Server crash from 1.2.3.4"] * 30)
    a2 = LogAnalyzer()
    a2.add_entries(e2)
    assert a2.error_rate() == 100.0
    alerts2 = eng.evaluate(a2)
    assert len(alerts2) >= 2  # error rate + volumen
    r2 = rpt.generate(a2, alerts2)
    assert "ALERTAS" in r2
    print(f"  [PASS] Test 10: Cadena completa: 30 errores → rate=100% → {len(alerts2)} alertas ✅")

    print(f"\n  Todos los tests pasaron correctamente.")


if __name__ == "__main__":
    ejecutar_demo_y_tests()
