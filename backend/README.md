# ICD Logo Voting Platform — Backend API

FastAPI backend service for student identification, vote registry, and receipt verification for the **Ingeniería en Ciencias de Datos (ICD)** logo selection.

## Tech Stack
- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) with Uvicorn
- **Package & Environment Manager**: [`uv`](https://docs.astral.sh/uv/)
- **Database**: [Turso](https://turso.tech/) via official [`libsql`](https://github.com/tursodatabase/libsql-python)
- **Validation & Settings**: Pydantic v2 & Pydantic Settings

## Local Development
```bash
# Setup virtual environment and dependencies
just backend-setup

# Start development server on http://localhost:8000
just backend-dev

# Test /health endpoint
just backend-test
```
