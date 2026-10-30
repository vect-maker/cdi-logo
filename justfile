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
test:
    {{python}} build.py --audit
    @{{python}} -c "import re, os; doc = open('{{artifact_dir}}/walkthrough.md').read(); links = re.findall(r'\((file:///[^)]+)\)', doc); missing = [l for l in links if not os.path.exists(l.replace('file://', ''))]; assert not missing, f'Missing links: {missing}'; print('  Documentation links: 100% PASS (all targets exist on disk)')"
    @{{python}} -c "import re, os; doc = open('{{artifact_dir}}/walkthrough.md').read(); imgs = re.findall(r'!\[[^\]]*\]\((/[^)]+)\)', doc); missing = [i for i in imgs if not os.path.exists(i)]; assert not missing, f'Missing images: {missing}'; print('  Embedded markdown images: 100% PASS (all assets exist on disk)')"

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
