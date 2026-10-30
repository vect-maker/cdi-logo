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

# Copy example environment variables (optional for local SQLite development)
cp .env.example .env

# Start development server on http://localhost:8000
just backend-dev

# Test /health endpoint
just backend-test
```

## Production Image & Docker Hub Deployment

Build, tag, and publish the production server container image using Podman:

```bash
# Build the production image and tag locally (latest, prod, and custom tag)
just backend-prod-build [tag="latest"]

# Build, tag, and upload directly to Docker Hub (haterofvectors/icd-logo-votes)
just backend-prod-push [tag="latest"]

# Convenience aliases:
just backend-push
just push-prod
```
When running `just backend-prod-push`, the recipe automatically guarantees that the latest build is created with Podman, tagged (`latest`, `prod`, and any specified tag), and pushed to `docker.io/haterofvectors/icd-logo-votes`.
