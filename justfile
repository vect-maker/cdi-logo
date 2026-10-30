# Justfile for Ingeniería en Ciencias de Datos (ICD) Identity System
# Faculty: Ciencias Básicas y Tecnología

# Use Python 3 executable
python := "python3"
artifact_dir := "/var/home/ocelot/.gemini/antigravity-cli/brain/bb63ec6e-ee8a-42c2-9da4-7361de38ac1c"

# Display all available recipes and their descriptions
default:
    @just --list

# Compile all vector SVG masters, render 512px PNGs, and generate apparel showcases
build:
    {{python}} build.py --build --render --showcase

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
    cd frontend && npx cypress run {{args}}

# Capture high-fidelity screenshots of all voting wizard steps using Cypress
capture-screenshots:
    cd frontend && npx cypress run --headed --spec cypress/e2e/capture-screenshots.cy.ts
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

# Wipe output directories (candidates/, renders/, and artifact assets) to prevent stale files
clean:
    {{python}} build.py --clean

# Synchronize candidate vector assets into the frontend public directory
frontend-sync:
    @mkdir -p frontend/public/candidates
    @cp -r candidates/c* frontend/public/candidates/
    @rm -rf frontend/public/candidates/__pycache__
    @echo "  Synchronized candidates assets to frontend/public/candidates/"

# Build the frontend production bundle (type check + vite build)
frontend-build: frontend-sync
    cd frontend && npm run build

# Start the frontend Vite development server
frontend-dev: frontend-sync
    cd frontend && npm run dev

# Execute the complete pipeline end-to-end (clean, build, audit, render, showcase, and sync)
all:
    {{python}} build.py --all
