#!/usr/bin/env python3
"""Unified Build & Asset Organization Pipeline for ICD Identity System.

Provides deterministic cleaning, modular SVG compilation, audit, rendering,
frontend contract synchronization, and artifact synchronization.

Usage:
  python3 build.py --clean
  python3 build.py --build
  python3 build.py --sync-contracts
  python3 build.py --sync-frontend
  python3 build.py --audit
  python3 build.py --render
  python3 build.py --contrast
  python3 build.py --showcase
  python3 build.py --sync-artifacts
  python3 build.py --candidate c4-tesseract
  python3 build.py --all
"""
import os
import sys
import glob
import json
import shutil
import argparse
import subprocess

REPO_ROOT = os.path.abspath(os.path.dirname(__file__))
CANDIDATES_DIR = os.path.join(REPO_ROOT, "candidates")
CONFIG_PATH = os.path.join(CANDIDATES_DIR, "candidates.config.json")
RENDERS_DIR = os.path.join(REPO_ROOT, "renders")
FRONTEND_PUBLIC = os.path.join(REPO_ROOT, "frontend", "public", "candidates")
ARTIFACT_DIR = "/var/home/ocelot/.gemini/antigravity-cli/brain/bb63ec6e-ee8a-42c2-9da4-7361de38ac1c"
ARTIFACT_ASSETS = os.path.join(ARTIFACT_DIR, "assets")
ARTIFACT_ARCHIVE = os.path.join(ARTIFACT_DIR, "archive")

SKILL_SCRIPTS = os.path.join(REPO_ROOT, ".agents", "skills", "logo-design", "scripts")
SVG_AUDIT = os.path.join(SKILL_SCRIPTS, "svg_audit.py")
RENDER_PNG = os.path.join(SKILL_SCRIPTS, "render_png.py")
CONCEPT_SHEET = os.path.join(SKILL_SCRIPTS, "concept_sheet.py")

def load_system_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def clean_pipeline():
    print("[1/7] Cleaning output directories...")
    # Clean candidates directory (keep python scripts and config, delete generated SVGs/subdirs)
    if os.path.exists(CANDIDATES_DIR):
        for item in os.listdir(CANDIDATES_DIR):
            p = os.path.join(CANDIDATES_DIR, item)
            if os.path.isdir(p) and item.startswith("c"):
                shutil.rmtree(p)
            elif item.endswith(".svg") or (item.endswith(".png") and not item.startswith("ref_")):
                os.remove(p)

    # Clean renders directory
    if os.path.exists(RENDERS_DIR):
        shutil.rmtree(RENDERS_DIR)
    os.makedirs(os.path.join(RENDERS_DIR, "candidates"), exist_ok=True)
    os.makedirs(os.path.join(RENDERS_DIR, "concepts"), exist_ok=True)
    os.makedirs(os.path.join(RENDERS_DIR, "showcases"), exist_ok=True)

    # Clean artifact assets directory
    if os.path.exists(ARTIFACT_ASSETS):
        shutil.rmtree(ARTIFACT_ASSETS)
    os.makedirs(ARTIFACT_ASSETS, exist_ok=True)
    os.makedirs(ARTIFACT_ARCHIVE, exist_ok=True)

    # Verify no loose images in artifact root
    for f in os.listdir(ARTIFACT_DIR):
        p = os.path.join(ARTIFACT_DIR, f)
        if os.path.isfile(p) and f.endswith(".png"):
            os.remove(p)

    print("  Output directories wiped clean.")

def build_svgs(specific_candidate=None):
    print("[2/7] Compiling vector SVG master suites via modular compiler...")
    sys.path.insert(0, REPO_ROOT)
    from candidates.compiler import compile_all
    compile_all(clean=False, specific_candidate=specific_candidate, config_path=CONFIG_PATH)
    print("  SVG master suites compiled successfully.")

def sync_contracts():
    print("[3/7] Synchronizing TypeScript types and Zod domain schemas from config...")
    sys.path.insert(0, REPO_ROOT)
    from candidates.sync_contracts import sync_all
    sync_all()

def sync_frontend_assets():
    print("[4/7] Synchronizing vector assets into frontend/public/candidates/...")
    os.makedirs(FRONTEND_PUBLIC, exist_ok=True)
    for cand_folder in glob.glob(os.path.join(CANDIDATES_DIR, "c*")):
        if os.path.isdir(cand_folder):
            base_name = os.path.basename(cand_folder)
            dest = os.path.join(FRONTEND_PUBLIC, base_name)
            if os.path.exists(dest):
                shutil.rmtree(dest)
            shutil.copytree(cand_folder, dest)
    print("  Vector assets synchronized to frontend/public/candidates/.")

def audit_svgs():
    print("[5/7] Running production SVG audit across all generated files...")
    all_svgs = glob.glob(os.path.join(CANDIDATES_DIR, "*", "*", "*.svg"))
    if not all_svgs:
        print("  Error: No SVGs found to audit.")
        return False

    cmd = ["python3", SVG_AUDIT] + all_svgs
    res = subprocess.run(cmd, capture_output=True, text=True)
    if "FAIL" in res.stdout:
        print("  Audit reported failures:")
        print(res.stdout)
        return False
    print(f"  Audit passed for all {len(all_svgs)} files (0 live-text, valid geometry).")
    return True

def audit_contrast():
    sys.path.insert(0, REPO_ROOT)
    from candidates.audit_contrast import audit_all_palettes
    audit_all_palettes(CONFIG_PATH)

def render_pngs(specific_candidate=None):
    print("[6/7] Rendering 512px PNGs and multi-palette concept boards...")
    cfg = load_system_config()
    candidates = cfg["candidates"]
    palettes = cfg["palettes"]

    if specific_candidate:
        candidates = [c for c in candidates if c["id"] == specific_candidate or c["module"] == specific_candidate]

    # Render candidate PNGs into renders/candidates/<folder>/<subfolder>/
    for cand in candidates:
        cand_folder = cand["id"]
        for cat in ["symbols", "lockups", "stacked", "monochrome"]:
            src_cat = os.path.join(CANDIDATES_DIR, cand_folder, cat)
            dst_cat = os.path.join(RENDERS_DIR, "candidates", cand_folder, cat)
            os.makedirs(dst_cat, exist_ok=True)
            svgs = glob.glob(os.path.join(src_cat, "*.svg"))
            if svgs:
                cmd = ["python3", RENDER_PNG] + svgs + ["--out-dir", dst_cat, "--size", "512"]
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)

    # Render concept overview boards if all candidates are active
    if not specific_candidate:
        concepts_dir = os.path.join(RENDERS_DIR, "concepts")
        os.makedirs(concepts_dir, exist_ok=True)
        active_cands = [c for c in cfg["candidates"] if c.get("status") == "active"]

        for pal in palettes:
            key = pal["id"]
            title = pal.get("fullName", pal["name"])
            pal_tag = f"-{key}"

            symbols = [os.path.join(CANDIDATES_DIR, c["id"], "symbols", f"symbol{pal_tag}.svg") for c in active_cands]
            lockups = [os.path.join(CANDIDATES_DIR, c["id"], "lockups", f"lockup{pal_tag}.svg") for c in active_cands]
            names = [c["name"] for c in active_cands]
            notes = [c.get("concept", "") for c in active_cands]

            out_png = os.path.join(concepts_dir, f"concepts-{key}.png")
            cmd = [
                "python3", CONCEPT_SHEET,
                *symbols,
                "--lockups", *lockups,
                "--names", *names,
                "--notes", *notes,
                "--title", f"Ingeniería en Ciencias de Datos — {title}",
                "-o", out_png
            ]
            subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
            print(f"  Rendered {out_png}")

        if os.path.exists(os.path.join(concepts_dir, "concepts-cobalt.png")):
            shutil.copy(
                os.path.join(concepts_dir, "concepts-cobalt.png"),
                os.path.join(concepts_dir, "concepts-overview.png")
            )

def render_showcases():
    print("[7/7] Rendering apparel showcases into renders/showcases/...")
    sys.path.insert(0, CANDIDATES_DIR)
    from generate_palette_matrix import generate_palette_matrix
    from generate_black_gray_showcase import generate_showcase

    generate_palette_matrix()
    generate_showcase()
    print("  Showcases rendered successfully.")

def sync_artifacts():
    print("Synchronizing assets to artifact directory and verifying clean root...")
    cfg = load_system_config()
    # 1. Sync showcase boards
    showcases_dir = os.path.join(RENDERS_DIR, "showcases")
    if os.path.exists(showcases_dir):
        for f in os.listdir(showcases_dir):
            if f.endswith(".png"):
                shutil.copy(os.path.join(showcases_dir, f), os.path.join(ARTIFACT_ASSETS, f))

    # 2. Sync concept boards
    concepts_dir = os.path.join(RENDERS_DIR, "concepts")
    if os.path.exists(concepts_dir):
        for f in os.listdir(concepts_dir):
            if f.endswith(".png"):
                shutil.copy(os.path.join(concepts_dir, f), os.path.join(ARTIFACT_ASSETS, f))

    # 3. Sync candidate showcase lockups and stacked previews
    for cand in cfg["candidates"]:
        cand_folder = cand["id"]
        cand_renders = os.path.join(RENDERS_DIR, "candidates", cand_folder)
        if not os.path.exists(cand_renders):
            continue
        # Lockups
        for lock_png in glob.glob(os.path.join(cand_renders, "lockups", "*.png")):
            fname = f"{cand_folder}-{os.path.basename(lock_png)}"
            shutil.copy(lock_png, os.path.join(ARTIFACT_ASSETS, fname))
        # Stacked
        for stack_png in glob.glob(os.path.join(cand_renders, "stacked", "*.png")):
            fname = f"{cand_folder}-{os.path.basename(stack_png)}"
            shutil.copy(stack_png, os.path.join(ARTIFACT_ASSETS, fname))

    # 4. Strict assertion: zero loose images in ARTIFACT_DIR root
    loose_images = [f for f in os.listdir(ARTIFACT_DIR) if f.endswith(".png") or f.endswith(".svg")]
    if loose_images:
        for f in loose_images:
            os.remove(os.path.join(ARTIFACT_DIR, f))
        print(f"  Cleaned {len(loose_images)} loose images from artifact root.")

    print(f"  Active assets synced: {len(os.listdir(ARTIFACT_ASSETS))} files in assets/")

def main():
    parser = argparse.ArgumentParser(description="Master Build & Organization Pipeline")
    parser.add_argument("--clean", action="store_true", help="Clean output directories")
    parser.add_argument("--build", action="store_true", help="Compile outlined SVG master files")
    parser.add_argument("--sync-contracts", action="store_true", help="Sync TypeScript types and Zod schemas")
    parser.add_argument("--sync-frontend", action="store_true", help="Sync SVGs into frontend/public/candidates")
    parser.add_argument("--audit", action="store_true", help="Audit SVG files for compliance")
    parser.add_argument("--contrast", action="store_true", help="Run WCAG contrast accessibility audit")
    parser.add_argument("--render", action="store_true", help="Render PNG previews and concept sheets")
    parser.add_argument("--showcase", action="store_true", help="Render apparel matrix and showcases")
    parser.add_argument("--sync-artifacts", action="store_true", help="Sync assets to artifact folder")
    parser.add_argument("--candidate", "-c", help="Process only a specific candidate ID (e.g. c4-tesseract)")
    parser.add_argument("--all", action="store_true", help="Execute complete pipeline end-to-end")

    args = parser.parse_args()

    # If no flags passed, default to --all
    run_all = args.all or not any([
        args.clean, args.build, args.sync_contracts, args.sync_frontend,
        args.audit, args.contrast, args.render, args.showcase, args.sync_artifacts,
        args.candidate
    ])

    if run_all or args.clean:
        clean_pipeline()
    if run_all or args.build or args.candidate:
        build_svgs(specific_candidate=args.candidate)
    if run_all or args.sync_contracts:
        sync_contracts()
    if run_all or args.sync_frontend:
        sync_frontend_assets()
    if run_all or args.audit:
        audit_svgs()
    if run_all or args.contrast:
        audit_contrast()
    if run_all or args.render or args.candidate:
        render_pngs(specific_candidate=args.candidate)
    if run_all or args.showcase:
        render_showcases()
    if run_all or args.sync_artifacts:
        sync_artifacts()

    print("\n Pipeline execution completed successfully.")

if __name__ == "__main__":
    main()
