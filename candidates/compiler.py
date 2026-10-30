"""Master compiler that reads candidates.config.json and generates vector SVG assets.

Generates:
- symbols/symbol-{palette}.svg & symbol.svg
- lockups/lockup-{palette}.svg & lockup-{palette}-light.svg
- stacked/stacked-{palette}.svg & stacked-{palette}-light.svg
- monochrome/symbol-mono-black.svg & symbol-mono-white.svg
"""
import os
import json
import shutil
import argparse
from .figures import get_symbol_drawer
from .lockups import save_svg_file, make_horizontal_lockup, make_stacked_lockup

CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "candidates.config.json"))
CANDIDATES_DIR = os.path.abspath(os.path.dirname(__file__))

def load_config(config_path: str = CONFIG_PATH) -> dict:
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)

def build_candidate_suite(candidate: dict, palettes: list[dict], out_base_dir: str = CANDIDATES_DIR):
    """Build all SVG variants for a single candidate."""
    cand_id = candidate["id"]
    cand_name = candidate["name"]
    module_name = candidate["module"]
    drawer = get_symbol_drawer(module_name)

    cand_dir = os.path.join(out_base_dir, cand_id)
    sym_dir = os.path.join(cand_dir, "symbols")
    lock_dir = os.path.join(cand_dir, "lockups")
    stack_dir = os.path.join(cand_dir, "stacked")
    mono_dir = os.path.join(cand_dir, "monochrome")

    for d in [sym_dir, lock_dir, stack_dir, mono_dir]:
        os.makedirs(d, exist_ok=True)

    for p in palettes:
        p_id = p["id"]
        tokens = p["tokens"]
        p_name = p["fullName"]

        sym_file = os.path.join(sym_dir, f"symbol-{p_id}.svg")
        lock_file = os.path.join(lock_dir, f"lockup-{p_id}.svg")
        stack_file = os.path.join(stack_dir, f"stacked-{p_id}.svg")

        save_svg_file(sym_file, f"{cand_name} Symbol ({p_name})", 256, 256, lambda ctx, d=drawer, tok=tokens: d(ctx, pal=tok))
        make_horizontal_lockup(lock_file, f"{cand_name} Lockup ({p_name})", drawer, pal=tokens)
        make_stacked_lockup(stack_file, f"{cand_name} Stacked Lockup ({p_name})", drawer, pal=tokens)

        # Light apparel lockups
        lock_light = os.path.join(lock_dir, f"lockup-{p_id}-light.svg")
        stack_light = os.path.join(stack_dir, f"stacked-{p_id}-light.svg")
        make_horizontal_lockup(lock_light, f"{cand_name} Light Lockup ({p_name})", drawer, pal=tokens, light_bg=True)
        make_stacked_lockup(stack_light, f"{cand_name} Light Stacked Lockup ({p_name})", drawer, pal=tokens, light_bg=True)

        # Cobalt is primary default
        if p_id == "cobalt":
            save_svg_file(os.path.join(sym_dir, "symbol.svg"), f"{cand_name} Symbol", 256, 256, lambda ctx, d=drawer, tok=tokens: d(ctx, pal=tok))
            make_horizontal_lockup(os.path.join(lock_dir, "lockup.svg"), f"{cand_name} Lockup", drawer, pal=tokens)
            make_stacked_lockup(os.path.join(stack_dir, "stacked.svg"), f"{cand_name} Stacked Lockup", drawer, pal=tokens)
            make_horizontal_lockup(os.path.join(lock_dir, "lockup-light.svg"), f"{cand_name} Light Lockup", drawer, pal=tokens, light_bg=True)
            make_stacked_lockup(os.path.join(stack_dir, "stacked-light.svg"), f"{cand_name} Light Stacked Lockup", drawer, pal=tokens, light_bg=True)

    # 1-Color Monochrome Masters
    mono_black = os.path.join(mono_dir, "symbol-mono-black.svg")
    mono_white = os.path.join(mono_dir, "symbol-mono-white.svg")
    save_svg_file(mono_black, f"{cand_name} 1-Color Black", 256, 256, lambda ctx, d=drawer: d(ctx, mono="#000000"))
    save_svg_file(mono_white, f"{cand_name} 1-Color White", 256, 256, lambda ctx, d=drawer: d(ctx, mono="#FFFFFF"))

    print(f"  ✓ Compiled SVG suite for {cand_id} ({cand_name})")

def compile_all(clean: bool = False, specific_candidate: str | None = None, config_path: str = CONFIG_PATH):
    """Compile all active candidates from configuration."""
    config = load_config(config_path)
    palettes = config["palettes"]
    candidates = config["candidates"]

    if specific_candidate:
        candidates = [c for c in candidates if c["id"] == specific_candidate or c["module"] == specific_candidate]
        if not candidates:
            raise ValueError(f"Candidate '{specific_candidate}' not found in configuration.")

    print(f"[SVG Compiler] Generating suites for {len(candidates)} candidate(s) across {len(palettes)} palettes...")
    for c in candidates:
        if c.get("status") == "active" or specific_candidate:
            build_candidate_suite(c, palettes)

def main():
    parser = argparse.ArgumentParser(description="Modular SVG Master Compiler")
    parser.add_argument("--candidate", "-c", help="Compile only a specific candidate ID (e.g. c1-neural)")
    parser.add_argument("--clean", action="store_true", help="Clean candidate directory before compiling")
    args = parser.parse_args()

    compile_all(clean=args.clean, specific_candidate=args.candidate)

if __name__ == "__main__":
    main()
