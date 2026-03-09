# Tablero Kanban Interactivo

## Descripción del Proyecto

Aplicación web single-file HTML: un tablero Kanban interactivo con tema oscuro inspirado en Trello.
Ejercicio práctico del módulo 4 del curso «IA Generativa para el Desarrollo: Herramientas».

## Arquitectura

- **Single-file**: Todo el código en un único archivo `.html` (HTML + CSS + JS incrustados).
- **Sin framework**: JavaScript ES6+ vanilla.
- **Única dependencia externa**: SortableJS vía CDN (`cdnjs.cloudflare.com`).
- **Persistencia**: `localStorage` con JSON serializado.

### Estructura del archivo HTML

1. `<style>`: Variables CSS, layout (grid/flexbox), componentes, responsive, animaciones.
2. `<body>`: Estructura semántica del tablero, formulario, filtros y columnas.
3. `<script>`: Lógica de aplicación, gestión de estado, eventos y persistencia.

## Requisitos Clave

### Tablero
- 3 columnas fijas: «Por Hacer», «En Progreso», «Completado».
- Contador dinámico de tarjetas por columna.
- 6 tarjetas iniciales predefinidas (2 por columna) con temática de desarrollo de software.

### Tarjetas
- Campos: título, descripción, badge de prioridad (alta/media/baja), fecha de creación.
- Título editable con doble clic (inline editing); confirmar con Enter o blur.
- Botón eliminar con confirmación visual.
- Drag & drop entre columnas y reordenamiento dentro de cada columna (SortableJS).

### Interacción
- Formulario para añadir tarjetas: título (obligatorio), descripción, prioridad.
- Filtro por prioridad: Todas, Alta, Media, Baja.
- Botón «Reiniciar tablero» que restaura las 6 tarjetas originales.

### Persistencia (localStorage)
- Auto-guardado inmediato en cada cambio (mover, añadir, editar, eliminar).
- Restaurar último estado al cargar la página; si no existe, cargar tarjetas iniciales.

## Datos Iniciales

| Columna      | Título                  | Descripción                                  | Prioridad |
|--------------|-------------------------|----------------------------------------------|-----------|
| Por Hacer    | Configurar ESLint       | Añadir reglas de linting al proyecto         | Alta      |
| Por Hacer    | Diseñar API REST        | Definir endpoints y modelos de datos         | Media     |
| En Progreso  | Implementar login       | Autenticación con JWT y refresh tokens       | Alta      |
| En Progreso  | Crear tests unitarios   | Cobertura mínima del 80% con Jest            | Media     |
| Completado   | Setup del repositorio   | Inicializar repo con Git y estructura base   | Baja      |
| Completado   | Documentar README       | Instrucciones de instalación y uso           | Baja      |

## Diseño

### Paleta de Colores (tema oscuro)
- Fondo principal: `#0D1117` / `#161B22`
- Tarjetas: `#21262D`
- Texto principal: `#E6EDF3`
- Texto secundario: `#8B949E`
- Prioridad Alta: `#F85149` (rojo)
- Prioridad Media: `#D29922` (naranja)
- Prioridad Baja: `#3FB950` (verde)
- Acento/CTA: `#58A6FF`

### Layout
- Header fijo: título + filtro de prioridad + botón reiniciar.
- 3 columnas en CSS Grid/Flexbox con scroll horizontal en pantallas pequeñas.
- Formulario: modal o sección colapsable.
- Tarjetas: `border-radius: 8px`, sombra sutil, hover con elevación.
- Responsive: pantallas >= 768px (desktop y tablet).

## Requisitos No Funcionales

- Rendimiento: respuesta < 100ms en cualquier interacción.
- Compatibilidad: Chrome 90+, Firefox 90+, Edge 90+, Safari 15+.
- Accesibilidad: contraste mínimo AA sobre fondo oscuro.
- Transiciones CSS suaves en hover, drag y filtro.

## Convenciones de Código

- Código limpio y bien organizado dentro de las 3 secciones del HTML.
- CSS con custom properties (variables) para colores y valores reutilizables.
- JavaScript modular con funciones bien nombradas.
- No usar APIs experimentales del navegador.

## Changelog Automático

**OBLIGATORIO**: Antes de cada commit, actualizar `CHANGELOG.md` con los cambios realizados.

### Formato del Changelog
- Seguir formato [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/).
- Agrupar entradas por fecha `[YYYY-MM-DD]`.
- Usar categorías: `Añadido`, `Cambiado`, `Corregido`, `Eliminado`.
- Cada entrada debe ser una línea concisa describiendo el cambio desde la perspectiva del usuario.
- Incluir `CHANGELOG.md` en el staging (`git add`) junto con los demás archivos del commit.

### Ejemplo
```markdown
## [2026-03-09]

### Añadido
- Filtro por prioridad en el header del tablero

### Corregido
- Tarjetas nuevas no se guardaban al crearlas desde el formulario
```
