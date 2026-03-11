# Guia: Secciones de un archivo CLAUDE.md

## Que es CLAUDE.md

Es el archivo de instrucciones que Claude Code lee automaticamente al iniciar una sesion. Define el contexto del proyecto, convenciones y reglas que Claude debe seguir. Se carga completo en el contexto de cada conversacion, por lo que debe ser conciso (idealmente < 200 lineas).

---

## Ubicaciones y Alcance

| Alcance | Ubicacion | Uso |
|---------|-----------|-----|
| **Proyecto** | `./CLAUDE.md` o `./.claude/CLAUDE.md` | Estandares compartidos del equipo (se commitea) |
| **Usuario** | `~/.claude/CLAUDE.md` | Preferencias personales globales |
| **Local** | `./CLAUDE.local.md` | Preferencias personales por proyecto (no se commitea) |
| **Subdirectorios** | `src/CLAUDE.md`, `tests/CLAUDE.md` | Instrucciones contextuales que se cargan bajo demanda |
| **Reglas** | `.claude/rules/*.md` | Archivos tematicos (uno por topico) |

---

## Secciones Tipicas (recomendadas en todo proyecto)

### 1. Descripcion del Proyecto
- Que es, para que sirve (1-2 frases).
- Contexto minimo para orientar a Claude.

### 2. Stack Tecnologico
- Lenguaje, framework, base de datos, dependencias clave y versiones.
- Ejemplo: "Next.js 14, TypeScript, PostgreSQL, Prisma ORM"

### 3. Estructura de Directorios
- Mapa de carpetas principales con su proposito.
- No hace falta el arbol completo, solo las rutas clave.

### 4. Comandos de Build, Test y Ejecucion
- Comandos exactos tal como se usan en el dia a dia.
- Incluir flags y variantes habituales.
- Ejemplo: `npm run test -- --coverage`, `dotnet build src/Api/Api.csproj`

### 5. Convenciones de Codigo
- Formato: indentacion, comillas, punto y coma.
- Naming: PascalCase, camelCase, snake_case segun contexto.
- Patrones: async/await vs callbacks, manejo de errores, imports.
- Estilo: "No usar `any` en TypeScript", "Preferir funciones puras".

### 6. Arquitectura y Organizacion del Codigo
- Capas (controladores, servicios, repositorios).
- Como interactuan los modulos entre si.
- Patrones de diseno usados (CQRS, Clean Architecture, etc.).

### 7. Flujo de Trabajo con Git
- Convencion de ramas: `feature/`, `fix/`, `chore/`.
- Formato de commits: Conventional Commits, mensajes en ingles/espanol.
- Politica de PRs: revisar antes de merge, squash, etc.

### 8. Flujos de Trabajo Comunes
- Procedimientos repetibles que Claude debe seguir.
- Ejemplo: "Al crear un endpoint: definir DTO, crear servicio, agregar controller, escribir test".

---

## Secciones Adicionales (segun el proyecto)

### 9. Modelo de Datos / Schema de BD
- Entidades principales y sus relaciones.
- Constraints importantes (unique, not null, cascadas).

### 10. Gotchas y Problemas Conocidos
- Trampas especificas del proyecto que Claude no puede deducir solo.
- Ejemplo: "Los tests de integracion requieren Docker corriendo", "No usar `Date.now()` en tests, usar el mock de reloj".

### 11. Seguridad
- Reglas de manejo de credenciales y datos sensibles.
- Validacion de inputs, sanitizacion, politicas de autenticacion/autorizacion.

### 12. Rendimiento
- Restricciones conocidas y directrices.
- Ejemplo: "Paginar siempre las consultas", "No cargar mas de 1000 registros en memoria".

### 13. Dependencias y Servicios Externos
- APIs de terceros, webhooks, colas de mensajes.
- Como se configuran y donde estan documentados.

### 14. Calidad de Codigo
- Umbrales de cobertura de tests.
- Reglas de linting obligatorias.
- Requisitos de documentacion (JSDoc, XML comments, etc.).

### 15. Entornos y Despliegue
- Ambientes: dev, staging, produccion.
- Pipeline CI/CD y particularidades.
- Variables de entorno necesarias (sin valores reales).

### 16. Documentacion y Referencias
- Links a wikis, ADRs, diseños de referencia.
- Uso de `@path/to/file` para importar archivos relacionados.

### 17. Estructura Monorepo (si aplica)
- Paquetes y sus dependencias internas.
- Comandos por paquete vs globales.

---

## Buenas Practicas

### Que hacer
- Ser concreto y verificable: "Usar 2 espacios de indentacion" en vez de "formatear bien".
- Usar comandos exactos, no genericos.
- Mantenerlo corto: < 200 lineas (lo que exceda, moverlo a `.claude/rules/`).
- Usar listas y headers en Markdown para estructura clara.
- Evolucionar el archivo segun la friccion real del proyecto.

### Que NO hacer
- No incluir secretos, API keys ni credenciales.
- No poner instrucciones que Claude ya cumple por defecto.
- No crear reglas contradictorias entre multiples CLAUDE.md.
- No convertirlo en documentacion exhaustiva; es una guia operativa.

---

## Checklist Rapido

- [ ] Descripcion del proyecto (1-2 frases)
- [ ] Stack tecnologico con versiones
- [ ] Estructura de directorios
- [ ] Comandos exactos de build/test/run
- [ ] Convenciones de codigo
- [ ] Arquitectura general
- [ ] Flujo de Git
- [ ] Gotchas (si los hay)
- [ ] < 200 lineas
- [ ] Sin secretos ni credenciales

---

## Generacion Automatica

Usa el comando `/init` de Claude Code para generar un CLAUDE.md inicial basado en el analisis automatico del repositorio, y luego refinalo con las instrucciones que Claude no podria descubrir por si mismo.

---

*Referencias: [Documentacion oficial de Claude Code](https://docs.anthropic.com/en/docs/claude-code), [Blog: Using CLAUDE.md files](https://www.anthropic.com/engineering/claude-code-best-practices)*
