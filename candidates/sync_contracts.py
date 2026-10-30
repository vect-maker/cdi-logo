"""Synchronize design tokens, candidate catalog, and palettes from candidates.config.json

Directly updates:
1. frontend/src/types/voting.ts (TypeScript constants & interfaces)
2. frontend/src/api/modules/voting/domain.ts (Zod validation enums)
"""
import os
import json
import re

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONFIG_PATH = os.path.join(REPO_ROOT, "candidates", "candidates.config.json")
VOTING_TS_PATH = os.path.join(REPO_ROOT, "frontend", "src", "types", "voting.ts")
DOMAIN_TS_PATH = os.path.join(REPO_ROOT, "frontend", "src", "api", "modules", "voting", "domain.ts")

def load_config() -> dict:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def generate_voting_types(config: dict) -> str:
    """Generate clean, strongly-typed TypeScript source for voting.ts."""
    candidates = config["candidates"]
    palettes = config["palettes"]
    compositions = config["compositions"]
    fabrics = config["fabrics"]

    lines = [
        "// THIS FILE IS AUTO-GENERATED FROM candidates/candidates.config.json",
        "// Run `just sync-identity` or `python3 build.py --sync-contracts` to regenerate.",
        "",
        "export interface CandidateFigure {",
        "  id: string",
        "  slot: string",
        "  name: string",
        "  subtitle: string",
        "  concept?: string",
        "  svgPath: (palette: string) => string",
        "}",
        "",
        "export interface ColorPalette {",
        "  id: string",
        "  name: string",
        "  fullName?: string",
        "  primaryHex: string",
        "  secondaryHex: string",
        "  tokens?: Record<string, string>",
        "}",
        "",
        "export interface CompositionType {",
        "  id: 'symbols' | 'lockups' | 'stacked'",
        "  name: string",
        "  subtitle: string",
        "  getAssetFilename: (palette: string) => string",
        "}",
        "",
        "export interface FabricColor {",
        "  id: 'black' | 'charcoal' | 'gray'",
        "  name: string",
        "  hex: string",
        "}",
        "",
        "export interface StudentVote {",
        "  round: string",
        "  studentCode: string",
        "  figureId: string",
        "  paletteId: string",
        "  compositionId: 'symbols' | 'lockups' | 'stacked'",
        "  recommendations: string",
        "  timestamp: number",
        "  isoDate: string",
        "}",
        "",
        "export const CANDIDATE_FIGURES: CandidateFigure[] = ["
    ]

    for c in candidates:
        if c.get("status") == "active":
            lines.extend([
                "  {",
                f"    id: '{c['id']}',",
                f"    slot: '{c['slot']}',",
                f"    name: '{c['name']}',",
                f"    subtitle: '{c['subtitle']}',",
                f"    concept: '{c.get('concept', '')}',",
                f"    svgPath: (palette) => `/candidates/{c['id']}/symbols/symbol-${{palette}}.svg`,",
                "  },"
            ])
    lines.append("]")
    lines.append("")

    lines.append("export const COLOR_PALETTES: ColorPalette[] = [")
    for p in palettes:
        lines.extend([
            "  {",
            f"    id: '{p['id']}',",
            f"    name: '{p['name']}',",
            f"    fullName: '{p.get('fullName', '')}',",
            f"    primaryHex: '{p['primaryHex']}',",
            f"    secondaryHex: '{p['secondaryHex']}',",
            "  },"
        ])
    lines.append("]")
    lines.append("")

    lines.append("export const COMPOSITION_TYPES: CompositionType[] = [")
    comp_asset_map = {
        "symbols": "symbols/symbol-${palette}.svg",
        "lockups": "lockups/lockup-${palette}.svg",
        "stacked": "stacked/stacked-${palette}.svg",
    }
    for comp in compositions:
        asset_fn = comp_asset_map.get(comp["id"], "symbols/symbol-${palette}.svg")
        lines.extend([
            "  {",
            f"    id: '{comp['id']}',",
            f"    name: '{comp['name']}',",
            f"    subtitle: '{comp['subtitle']}',",
            f"    getAssetFilename: (palette) => `{asset_fn}`,",
            "  },"
        ])
    lines.append("]")
    lines.append("")

    lines.append("export const FABRIC_COLORS: FabricColor[] = [")
    for f in fabrics:
        lines.extend([
            "  {",
            f"    id: '{f['id']}',",
            f"    name: '{f['name']}',",
            f"    hex: '{f['hex']}',",
            "  },"
        ])
    lines.append("]")
    lines.append("")

    return "\n".join(lines)

def update_domain_schemas(config: dict) -> None:
    """Update Zod enums in domain.ts without affecting other validation logic."""
    if not os.path.exists(DOMAIN_TS_PATH):
        return

    with open(DOMAIN_TS_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    fig_ids = [f"  \"{c['id']}\"" for c in config["candidates"] if c.get("status") == "active"]
    fig_replacement = "export const FigureIdSchema = z.enum([\n" + ",\n".join(fig_ids) + ",\n]);"

    pal_ids = [f"  \"{p['id']}\"" for p in config["palettes"]] + ["  \"light\"", "  \"dark\""]
    pal_replacement = "export const PaletteIdSchema = z.enum([\n" + ",\n".join(pal_ids) + ",\n]);"

    comp_ids = [f"  \"{c['id']}\"" for c in config["compositions"]] + ["  \"chest-center\"", "  \"chest-left\"", "  \"sleeve-left\"", "  \"back-collar\""]
    comp_replacement = "export const PositionIdSchema = z.enum([\n" + ",\n".join(comp_ids) + ",\n]);"

    content = re.sub(r"export const FigureIdSchema = z\.enum\(\[[^\]]*\]\);", fig_replacement, content)
    content = re.sub(r"export const PaletteIdSchema = z\.enum\(\[[^\]]*\]\);", pal_replacement, content)
    content = re.sub(r"export const PositionIdSchema = z\.enum\(\[[^\]]*\]\);", comp_replacement, content)

    with open(DOMAIN_TS_PATH, "w", encoding="utf-8") as f:
        f.write(content)

def sync_all():
    print("[Contract Sync] Reading candidates.config.json...")
    config = load_config()

    voting_ts_content = generate_voting_types(config)
    with open(VOTING_TS_PATH, "w", encoding="utf-8") as f:
        f.write(voting_ts_content)
    print(f"  ✓ Updated {os.path.relpath(VOTING_TS_PATH, REPO_ROOT)}")

    update_domain_schemas(config)
    print(f"  ✓ Updated {os.path.relpath(DOMAIN_TS_PATH, REPO_ROOT)}")

if __name__ == "__main__":
    sync_all()
