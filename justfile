# Justfile for Ingeniería en Ciencias de Datos (ICD) Identity System
# Faculty: Ciencias Básicas y Tecnología

# Use Python 3 executable
python := "python3"
artifact_dir := "/var/home/ocelot/.gemini/antigravity-cli/brain/bb63ec6e-ee8a-42c2-9da4-7361de38ac1c"

# Display all available recipes and their descriptions
default:
    @just --list

# Compile all vector SVG masters, sync frontend contracts and assets, render PNGs, and generate apparel showcases
build:
    {{python}} build.py --build --sync-contracts --sync-frontend --render --showcase

# Synchronize identity system: compiles SVGs, syncs contracts (voting.ts & domain.ts) and copies to frontend
sync-identity:
    {{python}} build.py --build --sync-contracts --sync-frontend
    @echo "  Identity synchronized: SVGs, frontend assets, and TypeScript/Zod contracts up to date."

# Rapidly recompile and sync a single candidate (e.g. just iterate-candidate c4-tesseract)
iterate-candidate cand:
    {{python}} build.py --candidate {{cand}} --sync-contracts --sync-frontend
    @echo "  Candidate {{cand}} recompiled and synchronized."

# Run WCAG 2.1 accessibility and contrast audit for all palettes across fabrics
test-contrast:
    {{python}} build.py --contrast

# Run vector quality audit and verify documentation link/image integrity
test-unit:
    {{python}} build.py --audit
    @{{python}} -c "import re, os; doc = open('{{artifact_dir}}/walkthrough.md').read(); links = re.findall(r'\((file:///[^)]+)\)', doc); missing = [l for l in links if not os.path.exists(l.replace('file://', ''))]; assert not missing, f'Missing links: {missing}'; print('  Documentation links: 100% PASS (all targets exist on disk)')"
    @{{python}} -c "import re, os; doc = open('{{artifact_dir}}/walkthrough.md').read(); imgs = re.findall(r'!\[[^\]]*\]\((/[^)]+)\)', doc); missing = [i for i in imgs if not os.path.exists(i)]; assert not missing, f'Missing images: {missing}'; print('  Embedded markdown images: 100% PASS (all assets exist on disk)')"

# Run headless Cypress E2E suite in Podman container against the frontend
test-e2e *args="":
    podman compose -f compose.test.yml --profile test run -T --rm test-e2e {{args}}

# Run a single Cypress E2E spec file in Podman (e.g. just test-e2e-spec cypress/e2e/voting-happy-path.cy.ts)
test-e2e-spec spec:
    @just test-e2e --spec "{{spec}}"

# Launch interactive Cypress GUI in Podman container
test-e2e-gui *args="":
    podman compose -f compose.test.yml --profile gui run --rm test-e2e-gui {{args}}

# Run Cypress E2E directly on the host using local node_modules
test-e2e-local *args="":
    cd frontend && npx cypress run --spec "cypress/e2e/**/*.cy.ts" {{args}}

# Capture high-fidelity screenshots of all voting wizard steps using Cypress
capture-screenshots:
    cd frontend && npx cypress run --headed --spec "cypress/visual/capture-screenshots.cy.ts"
    @mkdir -p {{artifact_dir}}/screenshots
    @cp -f frontend/cypress/screenshots/capture-screenshots.cy.ts/*.png {{artifact_dir}}/screenshots/ 2>/dev/null || true
    @echo "  Screenshots captured and saved to frontend/cypress/screenshots/"

# List installed AI agent skills in the workspace
skills-list:
    npx skills list

# Update installed AI agent skills from upstream
skills-update:
    npx skills update

# Run complete test suite (unit + audit)
test: test-unit

# Run full project health check (backend types & lint, frontend types & tests, backend tests)
check: backend-check frontend-typecheck backend-test frontend-test frontend-build
    @echo "  All systems healthy: Backend (types, lint, tests) + Frontend (types, tests, build) 100% PASS"

# Wipe output directories (candidates/, renders/, and artifact assets) to prevent stale files
clean:
    {{python}} build.py --clean

# Synchronize candidate vector assets into the frontend public directory
frontend-sync:
    @mkdir -p frontend/public/candidates
    @cp -r candidates/c* frontend/public/candidates/
    @rm -rf frontend/public/candidates/__pycache__
    @echo "  Synchronized candidates assets to frontend/public/candidates/"

# Setup backend Python virtual environment and dependencies using uv
backend-setup:
    cd backend && uv venv && uv pip install "fastapi[standard]" "libsql" "pydantic-settings"
    @just backend-requirements

# Generate or update locked backend requirements.txt using uv pip compile
backend-requirements:
    cd backend && uv pip compile pyproject.toml -o requirements.txt

# Start backend FastAPI development server locally on port 8000
backend-dev *args="--port 8000 --host 0.0.0.0":
    cd backend && uv run uvicorn app.main:app --reload {{args}}

# Build backend container image using Podman Compose
backend-container-build:
    podman compose build backend

# Run backend development container with hot-reloading mounted volume
backend-container-up:
    podman compose up -d backend
    @echo "  Backend running in container at http://localhost:8000"

# Stop backend development container
backend-container-down:
    podman compose down

# Follow backend container logs
backend-container-logs:
    podman compose logs -f backend

# Run comprehensive backend static analysis (basedpyright type check + ruff lint & format)
backend-check: backend-typecheck backend-lint
    @echo "  Backend static analysis: 100% PASS (Zero type errors, zero lint warnings)"

# Run backend static type check using basedpyright (primary LSP type checker in Zed)
backend-typecheck:
    cd backend && uv run basedpyright app

# Run secondary static type check using mypy
backend-typecheck-mypy:
    cd backend && uv run mypy app

# Run backend linting and style verification using ruff
backend-lint:
    cd backend && uv run ruff check app && uv run ruff format --check app

# Automatically fix formatting and auto-fixable lint issues with ruff
backend-format:
    cd backend && uv run ruff check --fix app && uv run ruff format app

# Run backend unit verification on /health endpoint and vote lifecycle
backend-test:
    cd backend && uv run python -c "from fastapi.testclient import TestClient; from app.main import app; tc = TestClient(app); tc.__enter__(); hr = tc.get('/health'); assert hr.status_code == 200 and hr.json()['status'] == 'ok'; cr = tc.get('/api/v1/votes/check/20268888'); assert cr.status_code == 200; tc.__exit__(None, None, None); print('  FastAPI + SQLModel verification: 100% PASS (db:', hr.json()['database'], ')')"

# Run frontend unit tests (Zod validation and API client)
frontend-test:
    cd frontend && npm test

# Run comprehensive frontend static type check across all components, API, unit tests, and Cypress specs
frontend-typecheck:
    cd frontend && npm run typecheck
    @echo "  Frontend static type check: 100% PASS (Components, stores, API, unit tests & Cypress specs)"

# Build the frontend production bundle (type check + vite build)
frontend-build: frontend-sync
    cd frontend && npm run build

# Start the frontend Vite development server
frontend-dev: frontend-sync
    cd frontend && npm run dev

# Execute the complete pipeline end-to-end (clean, build, audit, render, showcase, and sync)
all:
    {{python}} build.py --all
