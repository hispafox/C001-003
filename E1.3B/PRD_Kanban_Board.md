# PRD — Tablero Kanban Interactivo

**Aplicación web single-file HTML**

| Campo | Valor |
|-------|-------|
| **Proyecto** | IA Generativa para el Desarrollo: Herramientas |
| **Versión** | 1.0 |
| **Fecha** | 09/03/2026 |
| **Autor** | Pedro |
| **Estado** | Borrador |

---

## 1. Resumen Ejecutivo

Este documento define los requisitos del producto para un **Tablero Kanban interactivo** implementado como aplicación web en un único archivo HTML. El tablero servirá como ejercicio práctico dentro del módulo 4 del curso «IA Generativa para el Desarrollo: Herramientas», demostrando cómo las herramientas de IA generativa (GitHub Copilot, Claude, ChatGPT) pueden asistir en la creación rápida de aplicaciones funcionales sin dependencias externas de backend.

---

## 2. Objetivos del Producto

### 2.1 Objetivo Principal

Proporcionar una herramienta de gestión visual de tareas tipo Kanban, completamente funcional en el navegador, con persistencia local y diseño profesional.

### 2.2 Objetivos Específicos

- Demostrar la capacidad de generar aplicaciones completas con asistencia de IA en un solo archivo.
- Ofrecer interactividad avanzada: drag & drop, edición in-line, filtrado dinámico.
- Garantizar persistencia de datos entre sesiones mediante localStorage.
- Implementar un diseño oscuro moderno, responsive y accesible, inspirado en Trello.
- Servir como ejemplo de código limpio y buenas prácticas de desarrollo frontend.

---

## 3. Alcance

### 3.1 Dentro del Alcance

- Aplicación single-file HTML (HTML + CSS + JavaScript incrustados).
- Funcionalidad completa de gestión de tarjetas Kanban.
- Dependencia externa única: SortableJS vía CDN.
- Compatibilidad con navegadores modernos (Chrome, Firefox, Edge, Safari).
- Diseño responsive (desktop y tablet).

### 3.2 Fuera del Alcance

- Backend o base de datos remota.
- Autenticación de usuarios o múltiples tableros.
- Sincronización entre dispositivos.
- Exportación/importación de datos.
- Tests automatizados.

---

## 4. Arquitectura Técnica

### 4.1 Stack Tecnológico

| Capa | Tecnología | Versión / Notas |
|------|-----------|-----------------|
| Estructura | HTML5 semántico | Elementos nativos |
| Estilos | CSS3 (variables + grid/flexbox) | Theme oscuro con custom properties |
| Lógica | JavaScript ES6+ (vanilla) | Sin frameworks |
| Drag & Drop | SortableJS | CDN (cdnjs.cloudflare.com) |
| Persistencia | localStorage API | JSON serializado |

### 4.2 Estructura del Archivo

El archivo HTML contendrá tres secciones claramente delimitadas:

- `<style>`: Variables CSS, layout, componentes, responsive breakpoints, animaciones.
- `<body>`: Estructura semántica del tablero, formulario, filtros y columnas.
- `<script>`: Lógica de aplicación, gestión de estado, eventos y persistencia.

---

## 5. Requisitos Funcionales

### 5.1 Estructura del Tablero

| ID | Requisito | Prioridad | Estado |
|----|-----------|-----------|--------|
| RF-01 | El tablero debe contener exactamente 3 columnas: «Por Hacer», «En Progreso» y «Completado». | 🔴 Alta | Pendiente |
| RF-02 | Cada columna debe mostrar un contador dinámico del número de tarjetas que contiene. | 🔴 Alta | Pendiente |
| RF-03 | El tablero debe cargar con 6 tarjetas iniciales predefinidas (2 por columna) con temática de desarrollo de software. | 🟡 Media | Pendiente |

### 5.2 Tarjetas

| ID | Requisito | Prioridad | Estado |
|----|-----------|-----------|--------|
| RF-04 | Cada tarjeta debe mostrar: título, descripción, badge de prioridad (alta/media/baja) con código de color, y fecha de creación. | 🔴 Alta | Pendiente |
| RF-05 | El título de la tarjeta debe ser editable mediante doble clic (inline editing). | 🔴 Alta | Pendiente |
| RF-06 | Cada tarjeta debe incluir un botón de eliminar con confirmación visual. | 🔴 Alta | Pendiente |
| RF-07 | Los badges de prioridad deben usar colores diferenciados: rojo (alta), naranja (media) y verde (baja). | 🟡 Media | Pendiente |

### 5.3 Interacción y Navegación

| ID | Requisito | Prioridad | Estado |
|----|-----------|-----------|--------|
| RF-08 | Las tarjetas deben poder moverse entre columnas y reordenarse dentro de cada columna mediante drag & drop (SortableJS). | 🔴 Alta | Pendiente |
| RF-09 | Debe existir un formulario para añadir nuevas tarjetas con campos: título (obligatorio), descripción y prioridad. | 🔴 Alta | Pendiente |
| RF-10 | Debe existir un filtro por prioridad con opciones: Todas, Alta, Media, Baja. | 🔴 Alta | Pendiente |
| RF-11 | Debe existir un botón «Reiniciar tablero» que restaure las 6 tarjetas iniciales. | 🟡 Media | Pendiente |

### 5.4 Persistencia

| ID | Requisito | Prioridad | Estado |
|----|-----------|-----------|--------|
| RF-12 | El estado completo del tablero (tarjetas, posiciones, columnas) debe persistir en localStorage. | 🔴 Alta | Pendiente |
| RF-13 | Al cargar la página, debe restaurarse el último estado guardado. Si no existe, cargar las tarjetas iniciales. | 🔴 Alta | Pendiente |
| RF-14 | Cada cambio (mover, añadir, editar, eliminar) debe disparar auto-guardado inmediato. | 🔴 Alta | Pendiente |

---

## 6. Requisitos No Funcionales

| ID | Requisito | Prioridad | Estado |
|----|-----------|-----------|--------|
| RNF-01 | Diseño oscuro moderno inspirado en Trello: fondo oscuro, tarjetas con sombra, bordes redondeados, tipografía legible. | 🔴 Alta | Pendiente |
| RNF-02 | Responsive: adaptarse a pantallas de 768px o superior (desktop y tablet). | 🔴 Alta | Pendiente |
| RNF-03 | Rendimiento: la interfaz debe responder en menos de 100ms a cualquier interacción del usuario. | 🟡 Media | Pendiente |
| RNF-04 | Todo el código debe estar contenido en un único archivo .html (sin archivos externos salvo CDN de SortableJS). | 🔴 Alta | Pendiente |
| RNF-05 | Compatibilidad: Chrome 90+, Firefox 90+, Edge 90+, Safari 15+. | 🟡 Media | Pendiente |
| RNF-06 | Accesibilidad: contraste mínimo AA para texto sobre fondo oscuro. | 🟢 Baja | Pendiente |
| RNF-07 | Transiciones CSS suaves en las interacciones (hover, drag, filtro). | 🟢 Baja | Pendiente |

---

## 7. Datos Iniciales

El tablero se inicializará con las siguientes 6 tarjetas de temática de desarrollo:

| Columna | Título | Descripción | Prioridad | Fecha |
|---------|--------|-------------|-----------|-------|
| Por Hacer | Configurar ESLint | Añadir reglas de linting al proyecto | 🔴 Alta | Hoy |
| Por Hacer | Diseñar API REST | Definir endpoints y modelos de datos | 🟡 Media | Hoy |
| En Progreso | Implementar login | Autenticación con JWT y refresh tokens | 🔴 Alta | Hoy |
| En Progreso | Crear tests unitarios | Cobertura mínima del 80% con Jest | 🟡 Media | Hoy |
| Completado | Setup del repositorio | Inicializar repo con Git y estructura base | 🟢 Baja | Hoy |
| Completado | Documentar README | Instrucciones de instalación y uso | 🟢 Baja | Hoy |

---

## 8. Especificaciones de Diseño

### 8.1 Paleta de Colores

| Elemento | Color | Uso |
|----------|-------|-----|
| Fondo principal | `#0D1117` / `#161B22` | Background del body y columnas |
| Tarjetas | `#21262D` | Background de cada tarjeta |
| Texto principal | `#E6EDF3` | Títulos y contenido |
| Texto secundario | `#8B949E` | Descripciones y metadata |
| Prioridad Alta | `#F85149` | Badge de prioridad alta |
| Prioridad Media | `#D29922` | Badge de prioridad media |
| Prioridad Baja | `#3FB950` | Badge de prioridad baja |
| Acento / CTA | `#58A6FF` | Botones primarios y enlaces |

### 8.2 Layout

- **Header fijo:** título del tablero + filtro de prioridad + botón reiniciar.
- **Zona principal:** 3 columnas en CSS Grid o Flexbox con scroll horizontal en pantallas pequeñas.
- **Formulario:** modal o sección colapsable para añadir tareas.
- **Tarjetas:** border-radius 8px, sombra sutil, hover con elevación.

---

## 9. Criterios de Aceptación

El producto se considerará completo cuando se cumplan **todos** los criterios siguientes:

- [ ] El archivo HTML se abre correctamente en Chrome, Firefox y Edge sin errores en consola.
- [ ] Las 3 columnas se renderizan con sus 6 tarjetas iniciales al primer uso.
- [ ] Drag & drop funciona entre columnas y dentro de cada columna.
- [ ] Los contadores de columna se actualizan en tiempo real al mover/añadir/eliminar tarjetas.
- [ ] El filtro de prioridad oculta/muestra tarjetas correctamente sin perder estado.
- [ ] Doble clic en el título activa edición inline; Enter o blur confirma el cambio.
- [ ] localStorage persiste el estado: cerrar y reabrir el navegador mantiene los datos.
- [ ] El botón Reiniciar restaura las 6 tarjetas originales descartando cambios.
- [ ] El diseño es oscuro, moderno, y responsive en pantallas ≥768px.
- [ ] El formulario valida que el título no esté vacío antes de crear la tarjeta.

---

## 10. Riesgos y Mitigaciones

| Riesgo | Impacto | Mitigación |
|--------|---------|------------|
| CDN de SortableJS no disponible | 🔴 Alto | Incluir comentario con fallback: descargar sortable.min.js y embeber en el HTML. |
| Límite de localStorage (5-10MB) | 🟢 Bajo | Para uso académico el volumen de datos es mínimo. Documentar límite. |
| Incompatibilidad en Safari < 15 | 🟢 Bajo | Usar propiedades CSS con amplio soporte. Evitar APIs experimentales. |
| Pérdida de datos al limpiar navegador | 🟡 Medio | Documentar que los datos se pierden al limpiar caché. Botón reiniciar como backup. |

---

*Fin del documento*
