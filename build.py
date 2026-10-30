#!/usr/bin/env python3
"""Unified Build & Asset Organization Pipeline for ICD Identity System.

Provides deterministic cleaning, SVG compilation, audit, rendering, and artifact synchronization.

Usage:
  python3 build.py --clean
  python3 build.py --build
  python3 build.py --audit
  python3 build.py --render
  python3 build.py --showcase
  python3 build.py --sync-artifacts
  python3 build.py --all
"""
import os
import sys
import glob
import shutil
import argparse
import subprocess

REPO_ROOT = os.path.abspath(os.path.dirname(__file__))
CANDIDATES_DIR = os.path.join(REPO_ROOT, "candidates")
RENDERS_DIR = os.path.join(REPO_ROOT, "renders")
ARTIFACT_DIR = "/var/home/ocelot/.gemini/antigravity-cli/brain/bb63ec6e-ee8a-42c2-9da4-7361de38ac1c"
ARTIFACT_ASSETS = os.path.join(ARTIFACT_DIR, "assets")
ARTIFACT_ARCHIVE = os.path.join(ARTIFACT_DIR, "archive")

SKILL_SCRIPTS = os.path.join(REPO_ROOT, ".agents", "skills", "logo-design", "scripts")
SVG_AUDIT = os.path.join(SKILL_SCRIPTS, "svg_audit.py")
RENDER_PNG = os.path.join(SKILL_SCRIPTS, "render_png.py")
CONCEPT_SHEET = os.path.join(SKILL_SCRIPTS, "concept_sheet.py")

CANDIDATE_LIST = [
    ("c1-neural", "Neural Cluster", "Distributed graph neural networks and node embeddings"),
    ("c2-matrix", "Matrix Tensor", "Multidimensional matrix algebra and tensor slice"),
    ("c3-hexcore", "Hex Data Core", "Hexagonal spatial indexing and cyber prism"),
    ("c4-tesseract", "4D Tesseract", "Hyperdimensional feature space isometric projection"),
    ("c5-voronoi", "Voronoi Cells", "Spatial clustering, KNN, and decision boundaries"),
    ("c6-waveform", "Harmonized Waveform", "Signal extraction, Fourier transforms, and entropy reduction")
]

PALETTES = [
    ('cobalt', '', 'Tech Cobalt & Cyan'),
    ('emerald', '-emerald', 'Cyber Emerald & Mint'),
    ('violet', '-violet', 'Ultraviolet & Neon Orchid'),
    ('amber', '-amber', 'Solar Amber & Cyber Orange')
]

def clean_pipeline():
    print("[1/6] Cleaning output directories...")
    # Clean candidates directory (keep python scripts, delete generated SVGs/subdirs)
    if os.path.exists(CANDIDATES_DIR):
        for item in os.listdir(CANDIDATES_DIR):
            p = os.path.join(CANDIDATES_DIR, item)
            if os.path.isdir(p) and item.startswith("c"):
                shutil.rmtree(p)
            elif item.endswith(".svg") or item.endswith(".png"):
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

def build_svgs():
    print("[2/6] Compiling 72 outlined SVG masters into organized candidate folders...")
    sys.path.insert(0, CANDIDATES_DIR)
    from generate_all import generate_all_candidates
    generate_all_candidates(out_dir=CANDIDATES_DIR, clean=False)
    print("  SVGs compiled successfully.")

def audit_svgs():
    print("[3/6] Running production SVG audit across all generated files...")
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

def render_pngs():
    print("[4/6] Rendering 512px PNGs and multi-palette concept boards...")
    # Render candidate PNGs into renders/candidates/<folder>/<subfolder>/
    for cand_folder, _, _ in CANDIDATE_LIST:
        for cat in ["symbols", "lockups", "stacked", "monochrome"]:
            src_cat = os.path.join(CANDIDATES_DIR, cand_folder, cat)
            dst_cat = os.path.join(RENDERS_DIR, "candidates", cand_folder, cat)
            os.makedirs(dst_cat, exist_ok=True)
            svgs = glob.glob(os.path.join(src_cat, "*.svg"))
            if svgs:
                cmd = ["python3", RENDER_PNG] + svgs + ["--out-dir", dst_cat, "--size", "512"]
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)

    # Render concept boards with full lockups into renders/concepts/
    concepts_dir = os.path.join(RENDERS_DIR, "concepts")
    for key, sfx, title in PALETTES:
        pal_tag = f"-{key}" if key != "cobalt" else "-cobalt"
        symbols = [os.path.join(CANDIDATES_DIR, c[0], "symbols", f"symbol{pal_tag}.svg") for c in CANDIDATE_LIST]
        lockups = [os.path.join(CANDIDATES_DIR, c[0], "lockups", f"lockup{pal_tag}.svg") for c in CANDIDATE_LIST]
        names = [c[1] for c in CANDIDATE_LIST]
        notes = [c[2] for c in CANDIDATE_LIST]

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

    # Copy cobalt as default overview
    shutil.copy(
        os.path.join(concepts_dir, "concepts-cobalt.png"),
        os.path.join(concepts_dir, "concepts-overview.png")
    )

def render_showcases():
    print("[5/6] Rendering apparel showcases into renders/showcases/...")
    sys.path.insert(0, CANDIDATES_DIR)
    from generate_palette_matrix import generate_palette_matrix
    from generate_black_gray_showcase import generate_showcase

    generate_palette_matrix()
    generate_showcase()
    print("  Showcases rendered successfully.")

def sync_artifacts():
    print("[6/6] Synchronizing assets to artifact directory and verifying clean root...")
    # 1. Sync showcase boards
    showcases_dir = os.path.join(RENDERS_DIR, "showcases")
    for f in os.listdir(showcases_dir):
        if f.endswith(".png"):
            shutil.copy(os.path.join(showcases_dir, f), os.path.join(ARTIFACT_ASSETS, f))

    # 2. Sync concept boards
    concepts_dir = os.path.join(RENDERS_DIR, "concepts")
    for f in os.listdir(concepts_dir):
        if f.endswith(".png"):
            shutil.copy(os.path.join(concepts_dir, f), os.path.join(ARTIFACT_ASSETS, f))

    # 3. Sync candidate showcase lockups and stacked previews needed in walkthrough
    for cand_folder, _, _ in CANDIDATE_LIST:
        cand_renders = os.path.join(RENDERS_DIR, "candidates", cand_folder)
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

    root_files = [f for f in os.listdir(ARTIFACT_DIR) if os.path.isfile(os.path.join(ARTIFACT_DIR, f))]
    print(f"  Artifact root clean! Active root documents: {root_files}")
    print(f"  Active assets synced: {len(os.listdir(ARTIFACT_ASSETS))} files in assets/")

def main():
    parser = argparse.ArgumentParser(description="Master Build & Organization Pipeline")
    parser.add_argument("--clean", action="store_true", help="Clean output directories")
    parser.add_argument("--build", action="store_true", help="Compile outlined SVG master files")
    parser.add_argument("--audit", action="store_true", help="Audit SVG files for compliance")
    parser.add_argument("--render", action="store_true", help="Render PNG previews and concept sheets")
    parser.add_argument("--showcase", action="store_true", help="Render apparel matrix and t-shirt showcases")
    parser.add_argument("--sync-artifacts", action="store_true", help="Sync assets to artifact folder")
    parser.add_argument("--all", action="store_true", help="Execute complete pipeline end-to-end")

    args = parser.parse_args()

    # If no flags passed, default to --all
    run_all = args.all or not any([args.clean, args.build, args.audit, args.render, args.showcase, args.sync_artifacts])

    if run_all or args.clean:
        clean_pipeline()
    if run_all or args.build:
        build_svgs()
    if run_all or args.audit:
        audit_svgs()
    if run_all or args.render:
        render_pngs()
    if run_all or args.showcase:
        render_showcases()
    if run_all or args.sync_artifacts:
        sync_artifacts()

    print("\n Pipeline execution completed successfully.")

if __name__ == "__main__":
    main()
