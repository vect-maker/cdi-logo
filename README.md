# ICD Logo Identity & Voting Platform
**Carrera:** *Ingeniería en Ciencias de Datos* (ICD)  
**Facultad:** *Ciencias Básicas y Tecnología*  

---

## 1. Visión y Proceso Electoral Iterativo

La elección del logotipo oficial de la carrera se rige por un **enfoque iterativo en múltiples rondas**:

1. **Ronda 1 (Selección de Conceptos Base)**:
   - Presentación de 6 isotipos geométricos con fundamentos matemáticos de Ciencias de Datos (Tesseract, Matriz Tensor, Red Neuronal, Circuito, Binario y Forma de Onda).
   - Exploración interactiva de paletas cromáticas y composiciones en prendas de vestir.
   - Cada estudiante universitario dispone estrictamente de **1 voto único e intransferible** verificado por su número de carné institucional (8 dígitos).

2. **Rondas Subsecuentes (Refinamiento Estético y Finalistas)**:
   - Las opciones más votadas avanzan a rondas de optimización visual, ajustes tipográficos de precisión y aplicaciones de marca corporativa.
   - Votaciones definitorias sobre combinaciones finalistas.

> **Nota de Diseño UI**: Toda la información referente al enfoque de desarrollo y al número de rondas pertenece a la documentación del proyecto y no se expone innecesariamente en la interfaz pública del estudiante, manteniendo la experiencia de votación limpia, enfocada y directa.

---

## 2. Arquitectura del Sistema

```
                          ┌─────────────────────────────┐
                          │   Frontend (Vue 3 + Vite)   │
                          │   • Pinia, Tailwind CSS v4  │
                          │   • VueUse (useApiFetch)    │
                          │   • Zod Schema Validation   │
                          └──────────────┬──────────────┘
                                         │ HTTP /api/v1
                                         ▼
                          ┌─────────────────────────────┐
                          │   Backend (FastAPI dev)     │
                          │   • SQLModel ORM            │
                          │   • Turso Database (libSQL) │
                          │   • SQLite Local Fallback   │
                          │   • Podman/Docker Compose   │
                          └─────────────────────────────┘
```

- **Frontend**: SPA construida en Vue 3 con TypeScript estricto, Tailwind CSS v4, Reka UI y Lucide. La comunicación con la API sigue el patrón de abstracción desacoplada de `mercanto` mediante `@vueuse/core` y esquemas de validación en tiempo de ejecución con **Zod**.
- **Backend**: API REST en FastAPI que utiliza **SQLModel** para definir esquemas y modelos de persistencia. Soporta tanto bases de datos remotas en la nube con **Turso (`libsql`)** como un fallback sin conexión a SQLite local.
- **Seguridad Electoral**: Garantiza unicidad del voto por carné a nivel de base de datos (`UNIQUE index`), generando un recibo digital con hash criptográfico SHA-256.

---

## 3. Comandos de Desarrollo (`just`)

El proyecto cuenta con un conjunto integral de recetas automatizadas a través de `just`:

### Verificación y Calidad
- **`just check`**: Ejecuta el chequeo integral de salud del proyecto (análisis estático y linteo del backend, chequeo estricto de tipos del frontend con Cypress, pruebas unitarias y build de producción).
- **`just backend-check`**: Chequeo estático del backend con `basedpyright` y verificación de estilo con `ruff`.
- **`just backend-format`**: Formateo automático y corrección de reglas de estilo con `ruff`.
- **`just frontend-typecheck`**: Chequeo estático de tipos TypeScript en Vue, API, tests unitarios y specs de Cypress (`vue-tsc --noEmit && tsc -p cypress/tsconfig.json --noEmit`).
- **`just test`**: Auditoría de calidad vectorial de los 162 archivos SVG maestros (cero texto en vivo) y verificación de enlaces.
- **`just test-e2e-local`**: Ejecución de la suite completa de pruebas funcionales E2E con Cypress (10/10 pruebas pasando).

### Ejecución de Servicios
- **`just backend-container-up`**: Inicia el backend containerizado con Podman Compose en `http://localhost:8000` con hot-reloading (`./backend/app:/app/app:z`).
- **`just backend-container-down`**: Detiene el contenedor del backend.
- **`just frontend-dev`**: Inicia el servidor de desarrollo Vite con soporte para HMR y proxy reverso hacia el backend.
