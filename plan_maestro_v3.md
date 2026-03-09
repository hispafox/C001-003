# Plan Maestro de Ejemplos Prácticos v3.0

## IA Generativa para el Desarrollo: Herramientas

---

## Principio Fundamental

> **La IA (Claude, Copilot Agente, Claude Code) es la HERRAMIENTA. Las aplicaciones son el PRODUCTO.**

- Cero API keys, cero dependencias de servicios de IA en el código
- Las 3 herramientas funcionan como agentes: prompt → código completo
- **Dos ejemplos por punto**: uno en Python, otro en HTML/JS (vanilla + CDN si aplica)
- 44 ejemplos totales (22 Python + 22 HTML/JS)

---

## Las 3 Herramientas como Agentes

| Herramienta | Dónde | Cómo |
|---|---|---|
| **Claude** | claude.ai (web) | Prompt en chat → código completo → copiar |
| **Copilot Agente** | VS Code | Prompt en modo agente → genera archivos en el proyecto |
| **Claude Code** | Terminal | Lee el .md → genera el proyecto completo |

---

## Resumen: 44 Ejemplos

| # | Módulo | Python | HTML/JS | Total |
|---|--------|--------|---------|-------|
| 1 | Introducción a la IA Generativa | 4 | 4 | 8 |
| 2 | Introducción a los LLMs | 5 | 5 | 10 |
| 3 | Ingeniería de Prompts | 6 | 6 | 12 |
| 4 | Herramientas Prácticas de IA | 7 | 7 | 14 |
| | **TOTAL** | **22** | **22** | **44** |

---

## Módulo 1 — Introducción a la IA Generativa

### E1.1 — Qué es la IA Generativa
- **Python**: Generador de resúmenes extractivos de texto ✅
- **HTML/JS**: Editor Markdown con vista previa en tiempo real ✅

### E1.2 — Tokens, Embeddings, Chunks, Contexto
- **Python**: Tokenizador BPE educativo + similitud TF-IDF ✅
- **HTML/JS**: Visualizador interactivo de tokenización ✅

### E1.3 — Tipologías de modelos generativos
- **Python**: Organizador de archivos CLI ✅
- **HTML/JS**: Kanban board con drag & drop ✅

### E1.4 — Ley de IA Europea
- **Python**: Clasificador de riesgo AI Act ✅
- **HTML/JS**: Formulario interactivo de evaluación de riesgo AI Act ✅

---

## Módulo 2 — Introducción a los Grandes Modelos de Lenguaje

### E2.1 — Generación
- **Python**: API REST Flask con CRUD de tareas
- **HTML/JS**: Generador de formularios dinámicos desde JSON

### E2.2 — Manipulación de lenguaje
- **Python**: Conversor multiformato CSV → JSON + Markdown + HTML
- **HTML/JS**: Conversor de unidades universal

### E2.3 — Alucinaciones
- **Python**: Detector de código con APIs inventadas
- **HTML/JS**: Quiz interactivo "¿Es real esta API?"

### E2.4 — Razonamiento básico
- **Python**: 3 problemas algorítmicos (8 reinas, silogismos, Bayes)
- **HTML/JS**: Visualizador de algoritmos de ordenación con animación

### E2.5 — Comparativa de LLMs
- **Python**: Gestor de contraseñas CLI
- **HTML/JS**: Dashboard comparativo de LLMs con Chart.js

---

## Módulo 3 — Ingeniería de Prompts

### E3.1 — Elementos del prompt
- **Python**: Validador de emails (8 iteraciones progresivas)
- **HTML/JS**: Validador de formularios con feedback en tiempo real

### E3.2 — Zero-shot
- **Python**: Decorador @retry con espera exponencial
- **HTML/JS**: Cronómetro con múltiples timers simultáneos

### E3.3 — Few-shot
- **Python**: Funciones de transformación de datos con patrón
- **HTML/JS**: Conversor de colores HEX ↔ RGB ↔ HSL con preview

### E3.4 — Cadena de pensamiento
- **Python**: Detector de ciclos en grafos dirigidos
- **HTML/JS**: Visualizador de grafos interactivo con nodos arrastrables

### E3.5 — Cadena de prompts
- **Python**: Sistema de gestión de biblioteca (5 módulos)
- **HTML/JS**: App de presupuesto personal con gráficos (Chart.js)

### E3.6 — Integración
- **Python**: Analizador de logs de servidor
- **HTML/JS**: Dashboard de analytics con Chart.js y filtros

---

## Módulo 4 — Herramientas Prácticas de IA

> Mini-proyecto Python: **TaskFlow** (CLI tareas)
> Mini-proyecto HTML/JS: **WebFlow** (app web tareas)

### E4.1 — Copilot: Generación
- **Python**: Estructura completa TaskFlow
- **HTML/JS**: Estructura completa WebFlow

### E4.2 — Copilot: Depuración
- **Python**: Bugs intencionados en TaskFlow
- **HTML/JS**: Bugs intencionados en WebFlow

### E4.3 — Copilot: Tests y documentación
- **Python**: Tests pytest + docstrings
- **HTML/JS**: Tests con assertions + JSDoc

### E4.4 — Ruff
- **Python**: Linting con Ruff
- **HTML/JS**: Linting con ESLint

### E4.5 — Sphinx
- **Python**: Documentación Sphinx
- **HTML/JS**: Documentación JSDoc de WebFlow

### E4.6 — JSDoc
- **Python**: Conversión models.py → JS + JSDoc
- **HTML/JS**: Módulo JS completo con JSDoc exhaustivo

### E4.7 — Doxygen
- **Python**: Conversión storage → C + Doxygen
- **HTML/JS**: Web component documentado + ejemplo Doxygen

---

## Estructura de Carpetas

```
curso-ia-generativa/
├── plan_maestro_v3.md
├── E1.1_Generacion_Texto/
│   ├── E1.1_python_instrucciones.md
│   ├── e1_1_generar_resumen.py
│   ├── E1.1_html_instrucciones.md
│   └── e1_1_markdown_editor.html
├── E1.2_Tokens_Embeddings/
│   ├── E1.2_python_instrucciones.md
│   ├── e1_2_tokens_embeddings.py
│   ├── E1.2_html_instrucciones.md
│   └── e1_2_token_visualizer.html
└── ...
```
