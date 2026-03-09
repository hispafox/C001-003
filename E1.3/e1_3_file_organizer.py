"""
E1.3 — Construyendo una App Real: Organizador de Archivos
==========================================================
Aplicación CLI que organiza archivos de un directorio por tipo/extensión.

Uso como CLI:
    python e1_3_file_organizer.py ~/Descargas
    python e1_3_file_organizer.py ~/Descargas --dry-run
    python e1_3_file_organizer.py ~/Descargas --dry-run --verbose

Uso como demo/tests (sin argumentos):
    python e1_3_file_organizer.py

Dependencias: Solo librería estándar de Python.
"""

import argparse
import logging
import shutil
import sys
import tempfile
from pathlib import Path

__version__ = "1.0.0"

# ═══════════════════════════════════════════════════════════════
# CONFIGURACIÓN DE CATEGORÍAS
# ═══════════════════════════════════════════════════════════════

CATEGORIAS: dict[str, set[str]] = {
    "images": {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico", ".tiff"},
    "documents": {
        ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
        ".odt", ".ods", ".odp", ".txt", ".rtf",
    },
    "code": {
        ".py", ".js", ".ts", ".html", ".css", ".java", ".c", ".cpp", ".h",
        ".rb", ".go", ".rs", ".php", ".sql", ".sh", ".bat",
    },
    "data": {".csv", ".json", ".xml", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".env", ".db", ".sqlite"},
    "media": {".mp3", ".wav", ".flac", ".mp4", ".avi", ".mkv", ".mov", ".wmv", ".ogg", ".m4a"},
    "archives": {".zip", ".tar", ".gz", ".rar", ".7z", ".bz2", ".xz"},
    "fonts": {".ttf", ".otf", ".woff", ".woff2", ".eot"},
}


# ═══════════════════════════════════════════════════════════════
# LOGGING
# ═══════════════════════════════════════════════════════════════

def configurar_logging(log_file: Path, nivel: int = logging.INFO) -> logging.Logger:
    """Configura logging con salida a archivo y consola.

    Args:
        log_file: Ruta del archivo de log.
        nivel: Nivel de logging (por defecto INFO).

    Returns:
        Logger configurado.
    """
    logger = logging.getLogger("file_organizer")
    logger.setLevel(nivel)

    # Limpiar handlers previos (por si se ejecuta múltiples veces)
    logger.handlers.clear()

    formato = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s",
                                datefmt="%Y-%m-%d %H:%M:%S")

    # Handler de archivo
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formato)
    logger.addHandler(file_handler)

    # Handler de consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formato)
    logger.addHandler(console_handler)

    return logger


# ═══════════════════════════════════════════════════════════════
# CLASE PRINCIPAL
# ═══════════════════════════════════════════════════════════════

class FileOrganizer:
    """Organizador de archivos por tipo/extensión.

    Escanea un directorio, clasifica archivos por extensión en categorías
    temáticas (images, documents, code, etc.) y los mueve a subcarpetas
    organizadas.

    Attributes:
        directorio: Path del directorio a organizar.
        dry_run: Si True, simula sin mover archivos.
        archivos_movidos: Contador de archivos movidos.
        archivos_omitidos: Contador de archivos omitidos.
        errores: Contador de errores.
        operaciones: Lista de operaciones realizadas.

    Examples:
        >>> organizer = FileOrganizer("/tmp/test", dry_run=True)
        >>> resultado = organizer.organizar()
        >>> isinstance(resultado, dict)
        True
    """

    def __init__(self, directorio: str, dry_run: bool = False) -> None:
        """Inicializa el organizador de archivos.

        Args:
            directorio: Ruta al directorio a organizar.
            dry_run: Si True, simula las operaciones sin mover archivos.

        Raises:
            ValueError: Si el directorio no existe o no es un directorio.
        """
        self.directorio: Path = Path(directorio).resolve()

        if not self.directorio.exists():
            raise ValueError(f"El directorio no existe: {self.directorio}")
        if not self.directorio.is_dir():
            raise ValueError(f"La ruta no es un directorio: {self.directorio}")

        self.dry_run: bool = dry_run
        self.archivos_movidos: int = 0
        self.archivos_omitidos: int = 0
        self.errores: int = 0
        self.operaciones: list[dict] = []

        # Configurar logging
        log_file = self.directorio / ".file_organizer.log"
        self.logger: logging.Logger = configurar_logging(log_file)

    def clasificar_archivo(self, archivo: Path) -> str:
        """Clasifica un archivo según su extensión.

        La extensión se compara en minúsculas para ser case-insensitive.

        Args:
            archivo: Path del archivo a clasificar.

        Returns:
            Nombre de la categoría ('images', 'code', 'other', etc.).
        """
        extension: str = archivo.suffix.lower()

        for categoria, extensiones in CATEGORIAS.items():
            if extension in extensiones:
                return categoria

        return "other"

    def resolver_conflicto(self, destino: Path) -> Path:
        """Resuelve conflictos de nombre añadiendo sufijo numérico.

        Si el archivo destino ya existe, genera un nuevo nombre con
        sufijo incremental: foto.jpg → foto_1.jpg → foto_2.jpg

        Args:
            destino: Path del archivo destino original.

        Returns:
            Path sin conflicto (el original si no existe, o con sufijo).
        """
        if not destino.exists():
            return destino

        stem: str = destino.stem
        suffix: str = destino.suffix
        parent: Path = destino.parent
        contador: int = 1

        while True:
            nuevo_nombre: str = f"{stem}_{contador}{suffix}"
            nuevo_destino: Path = parent / nuevo_nombre
            if not nuevo_destino.exists():
                return nuevo_destino
            contador += 1

    def organizar(self) -> dict:
        """Organiza los archivos del directorio por categoría.

        Escanea solo archivos del directorio raíz (no recursivo).
        Ignora archivos ocultos (nombre empieza por '.').
        En modo dry_run, registra las operaciones sin ejecutarlas.

        Returns:
            Diccionario con estadísticas:
                - total_archivos: archivos encontrados
                - archivos_movidos: archivos movidos/simulados
                - archivos_omitidos: archivos ignorados
                - errores: errores encontrados
                - por_categoria: dict con conteo por categoría
        """
        modo: str = "SIMULACIÓN (dry-run)" if self.dry_run else "EJECUCIÓN REAL"
        self.logger.info(f"Iniciando organización de {self.directorio}")
        self.logger.info(f"Modo: {modo}")

        por_categoria: dict[str, int] = {}
        archivos_encontrados: int = 0

        # Escanear archivos (solo directorio raíz, no recursivo)
        for item in sorted(self.directorio.iterdir()):
            # Ignorar directorios
            if item.is_dir():
                continue

            # Ignorar archivos ocultos
            if item.name.startswith("."):
                self.archivos_omitidos += 1
                self.logger.debug(f"Omitido (oculto): {item.name}")
                continue

            # Ignorar el propio script
            if item.name == Path(__file__).name:
                self.archivos_omitidos += 1
                continue

            archivos_encontrados += 1

            # Clasificar
            categoria: str = self.clasificar_archivo(item)

            # Preparar destino
            carpeta_destino: Path = self.directorio / categoria
            destino: Path = carpeta_destino / item.name

            # Resolver conflictos
            destino = self.resolver_conflicto(destino)

            # Registrar operación
            operacion: dict = {
                "archivo": item.name,
                "categoria": categoria,
                "origen": str(item),
                "destino": str(destino),
                "estado": "pendiente",
            }

            try:
                if self.dry_run:
                    operacion["estado"] = "simulado"
                    self.logger.info(f"[DRY-RUN] {item.name} → {categoria}/{destino.name}")
                else:
                    # Crear carpeta si no existe
                    carpeta_destino.mkdir(exist_ok=True)
                    # Mover archivo
                    shutil.move(str(item), str(destino))
                    operacion["estado"] = "movido"
                    self.logger.info(f"[MOVED] {item.name} → {categoria}/{destino.name}")

                self.archivos_movidos += 1
                por_categoria[categoria] = por_categoria.get(categoria, 0) + 1

            except PermissionError:
                operacion["estado"] = "error"
                operacion["error"] = "Sin permisos"
                self.errores += 1
                self.logger.error(f"Sin permisos para mover: {item.name}")
            except Exception as e:
                operacion["estado"] = "error"
                operacion["error"] = str(e)
                self.errores += 1
                self.logger.error(f"Error moviendo {item.name}: {e}")

            self.operaciones.append(operacion)

        self.logger.info(f"Organización completada: {self.archivos_movidos} archivos procesados")

        return {
            "total_archivos": archivos_encontrados,
            "archivos_movidos": self.archivos_movidos,
            "archivos_omitidos": self.archivos_omitidos,
            "errores": self.errores,
            "por_categoria": por_categoria,
        }

    def generar_informe(self) -> str:
        """Genera un informe legible de las operaciones realizadas.

        Returns:
            String con el informe formateado.
        """
        modo: str = "SIMULACIÓN (dry-run)" if self.dry_run else "EJECUCIÓN REAL"
        lineas: list[str] = []

        lineas.append(f"  Modo: {modo}")
        lineas.append(f"  Directorio: {self.directorio}")
        lineas.append(f"  Archivos procesados: {self.archivos_movidos}")
        lineas.append(f"  Archivos omitidos: {self.archivos_omitidos}")
        lineas.append(f"  Errores: {self.errores}")

        # Conteo por categoría
        categorias_usadas: dict[str, int] = {}
        for op in self.operaciones:
            if op["estado"] in ("movido", "simulado"):
                cat = op["categoria"]
                categorias_usadas[cat] = categorias_usadas.get(cat, 0) + 1

        if categorias_usadas:
            lineas.append(f"  Desglose por categoría:")
            for cat, count in sorted(categorias_usadas.items()):
                lineas.append(f"    {cat}: {count}")

        return "\n".join(lineas)


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

def crear_parser() -> argparse.ArgumentParser:
    """Crea el parser de argumentos de línea de comandos.

    Returns:
        ArgumentParser configurado.
    """
    parser = argparse.ArgumentParser(
        prog="file_organizer",
        description="Organiza archivos de un directorio por tipo/extensión.",
        epilog="Ejemplo: python e1_3_file_organizer.py ~/Descargas --dry-run",
    )
    parser.add_argument(
        "directorio",
        help="Ruta al directorio a organizar",
    )
    parser.add_argument(
        "-n", "--dry-run",
        action="store_true",
        help="Simular sin mover archivos (muestra qué haría)",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Mostrar más detalle en consola",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def main() -> int:
    """Punto de entrada principal de la aplicación CLI.

    Returns:
        Código de salida (0 = éxito, 1 = errores).
    """
    parser = crear_parser()
    args = parser.parse_args()

    nivel = logging.DEBUG if args.verbose else logging.INFO

    try:
        organizer = FileOrganizer(args.directorio, dry_run=args.dry_run)
        organizer.logger.setLevel(nivel)
        resultado = organizer.organizar()
        print(f"\n{'─' * 50}")
        print("INFORME:")
        print(f"{'─' * 50}")
        print(organizer.generar_informe())
        return 0 if resultado["errores"] == 0 else 1

    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nOperación cancelada por el usuario.")
        return 1


# ═══════════════════════════════════════════════════════════════
# DEMO Y TESTS
# ═══════════════════════════════════════════════════════════════

def _crear_directorio_prueba() -> Path:
    """Crea un directorio temporal con archivos de prueba.

    Returns:
        Path al directorio temporal creado.
    """
    tmp_dir = Path(tempfile.mkdtemp(prefix="file_organizer_test_"))

    archivos_prueba = [
        "foto.jpg",
        "documento.pdf",
        "script.py",
        "datos.csv",
        "cancion.mp3",
        "comprimido.zip",
        "fuente.ttf",
        "desconocido.xyz",
        ".hidden_file",
        "README.txt",
    ]

    for nombre in archivos_prueba:
        (tmp_dir / nombre).touch()

    return tmp_dir


def ejecutar_demo_y_tests() -> None:
    """Ejecuta demo completa y tests automáticos."""

    print("=" * 70)
    print("E1.3 — DEMO: ORGANIZADOR DE ARCHIVOS")
    print("=" * 70)

    # ── Crear directorio de prueba ──
    print("\nCreando directorio de prueba con 10 archivos...")
    test_dir = _crear_directorio_prueba()
    for f in sorted(test_dir.iterdir()):
        print(f"  Creado: {f.name}")

    # ── DEMO 1: Dry-Run ──
    print(f"\n{'─' * 50}")
    print("DEMO 1: Modo Dry-Run")
    print(f"{'─' * 50}")

    # Suprimir logging en consola para demo limpia
    organizer_dry = FileOrganizer(str(test_dir), dry_run=True)
    # Quitar console handler para no duplicar output
    organizer_dry.logger.handlers = [
        h for h in organizer_dry.logger.handlers
        if not isinstance(h, logging.StreamHandler) or isinstance(h, logging.FileHandler)
    ]

    resultado_dry = organizer_dry.organizar()

    # Mostrar operaciones
    for op in organizer_dry.operaciones:
        print(f"  [DRY-RUN] {op['archivo']} → {op['categoria']}/{Path(op['destino']).name}")

    print(f"\nInforme:")
    print(organizer_dry.generar_informe())

    # ── DEMO 2: Ejecución real (nuevo directorio) ──
    print(f"\n{'─' * 50}")
    print("DEMO 2: Ejecución Real")
    print(f"{'─' * 50}")

    test_dir2 = _crear_directorio_prueba()
    organizer_real = FileOrganizer(str(test_dir2), dry_run=False)
    organizer_real.logger.handlers = [
        h for h in organizer_real.logger.handlers
        if not isinstance(h, logging.StreamHandler) or isinstance(h, logging.FileHandler)
    ]

    resultado_real = organizer_real.organizar()

    for op in organizer_real.operaciones:
        print(f"  [MOVED] {op['archivo']} → {op['categoria']}/{Path(op['destino']).name}")

    print(f"\nInforme:")
    print(organizer_real.generar_informe())

    # Verificar estructura creada
    print(f"\n  Estructura resultante:")
    for item in sorted(test_dir2.iterdir()):
        if item.is_dir() and not item.name.startswith("."):
            contenido = list(item.iterdir())
            print(f"    {item.name}/ ({len(contenido)} archivos)")
            for f in contenido:
                print(f"      └── {f.name}")

    # ═══════════════════════════════════════════════════════
    # TESTS
    # ═══════════════════════════════════════════════════════
    print(f"\n{'=' * 70}")
    print("TESTS:")
    print(f"{'=' * 70}")

    # Test 1: Clasificación de extensiones
    test_dir3 = _crear_directorio_prueba()
    org = FileOrganizer(str(test_dir3), dry_run=True)
    assert org.clasificar_archivo(Path("foto.jpg")) == "images"
    assert org.clasificar_archivo(Path("script.py")) == "code"
    assert org.clasificar_archivo(Path("datos.csv")) == "data"
    print("  [PASS] Test 1: Clasificación de extensiones")

    # Test 2: Clasificación case-insensitive
    assert org.clasificar_archivo(Path("FOTO.JPG")) == "images"
    assert org.clasificar_archivo(Path("Script.Py")) == "code"
    assert org.clasificar_archivo(Path("DATA.CSV")) == "data"
    print("  [PASS] Test 2: Clasificación case-insensitive")

    # Test 3: Extensión desconocida → other
    assert org.clasificar_archivo(Path("raro.xyz")) == "other"
    assert org.clasificar_archivo(Path("sin_extension")) == "other"
    print("  [PASS] Test 3: Extensión desconocida → other")

    # Test 4: Dry-run no mueve archivos
    archivos_antes = set(f.name for f in test_dir3.iterdir() if f.is_file())
    org_dry = FileOrganizer(str(test_dir3), dry_run=True)
    org_dry.logger.handlers = [h for h in org_dry.logger.handlers if isinstance(h, logging.FileHandler)]
    org_dry.organizar()
    archivos_despues = set(f.name for f in test_dir3.iterdir() if f.is_file())
    assert archivos_antes == archivos_despues, "Dry-run no debe mover archivos"
    print("  [PASS] Test 4: Dry-run no mueve archivos")

    # Test 5: Dry-run registra operaciones
    assert len(org_dry.operaciones) > 0, "Dry-run debe registrar operaciones"
    assert all(op["estado"] == "simulado" for op in org_dry.operaciones)
    print("  [PASS] Test 5: Dry-run registra operaciones")

    # Test 6: Ejecución real mueve archivos
    test_dir4 = _crear_directorio_prueba()
    org_real = FileOrganizer(str(test_dir4), dry_run=False)
    org_real.logger.handlers = [h for h in org_real.logger.handlers if isinstance(h, logging.FileHandler)]
    resultado = org_real.organizar()
    archivos_raiz = [f for f in test_dir4.iterdir() if f.is_file() and not f.name.startswith(".")]
    assert len(archivos_raiz) == 0, "Todos los archivos visibles deben moverse"
    assert resultado["archivos_movidos"] == 9, f"Esperado 9 movidos, obtenido {resultado['archivos_movidos']}"
    print("  [PASS] Test 6: Ejecución real mueve archivos")

    # Test 7: Se crean las carpetas correctas
    carpetas_creadas = {d.name for d in test_dir4.iterdir() if d.is_dir() and not d.name.startswith(".")}
    assert "images" in carpetas_creadas, "Debe existir carpeta images"
    assert "code" in carpetas_creadas, "Debe existir carpeta code"
    assert "documents" in carpetas_creadas, "Debe existir carpeta documents"
    print("  [PASS] Test 7: Se crean las carpetas correctas")

    # Test 8: Archivos ocultos se ignoran
    hidden_existe = (test_dir4 / ".hidden_file").exists()
    hidden_en_ops = any(op["archivo"] == ".hidden_file" for op in org_real.operaciones)
    assert hidden_existe, ".hidden_file debe permanecer en la raíz"
    assert not hidden_en_ops, ".hidden_file no debe estar en operaciones"
    print("  [PASS] Test 8: Archivos ocultos se ignoran")

    # Test 9: Resolución de conflictos
    test_dir5 = _crear_directorio_prueba()
    # Crear archivo duplicado manualmente
    (test_dir5 / "images").mkdir(exist_ok=True)
    (test_dir5 / "images" / "foto.jpg").touch()  # Ya existe en destino
    org_conflict = FileOrganizer(str(test_dir5), dry_run=False)
    org_conflict.logger.handlers = [h for h in org_conflict.logger.handlers if isinstance(h, logging.FileHandler)]
    org_conflict.organizar()
    fotos = list((test_dir5 / "images").glob("foto*.jpg"))
    assert len(fotos) == 2, f"Debe haber 2 fotos (original + renombrada), hay {len(fotos)}"
    nombres_fotos = {f.name for f in fotos}
    assert "foto_1.jpg" in nombres_fotos, f"Debe existir foto_1.jpg, encontrado: {nombres_fotos}"
    print("  [PASS] Test 9: Resolución de conflictos")

    # Test 10: Directorio inexistente lanza ValueError
    try:
        FileOrganizer("/ruta/que/no/existe/jamas")
        assert False, "Debería lanzar ValueError"
    except ValueError:
        pass
    print("  [PASS] Test 10: Directorio inexistente lanza ValueError")

    print(f"\n  Todos los tests pasaron correctamente.")

    # Limpieza
    for d in [test_dir, test_dir2, test_dir3, test_dir4, test_dir5]:
        try:
            shutil.rmtree(d)
        except Exception:
            pass
    print(f"\n  Limpieza: directorios temporales eliminados.")


# ═══════════════════════════════════════════════════════════════
# PUNTO DE ENTRADA
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Si se pasan argumentos → modo CLI
    if len(sys.argv) > 1:
        sys.exit(main())
    else:
        # Sin argumentos → demo y tests
        ejecutar_demo_y_tests()
