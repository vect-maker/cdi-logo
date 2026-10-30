"""Contrast and Accessibility Evaluator for ICD Identity System Palettes.

Calculates relative luminance and WCAG 2.1 contrast ratios for every color token
against all standard fabric backgrounds (Black, Charcoal, Gray).
"""
import json
import os

CONFIG_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "candidates.config.json"))

def hex_to_rgb(hex_str: str) -> tuple[float, float, float]:
    h = hex_str.lstrip('#')
    return tuple(int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4))  # type: ignore

def relative_luminance(rgb: tuple[float, float, float]) -> float:
    def channel_lum(c: float) -> float:
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (channel_lum(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast_ratio(hex1: str, hex2: str) -> float:
    l1 = relative_luminance(hex_to_rgb(hex1))
    l2 = relative_luminance(hex_to_rgb(hex2))
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)

def audit_all_palettes(config_path: str = CONFIG_PATH):
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    fabrics = config["fabrics"]
    palettes = config["palettes"]

    print("=" * 80)
    print(" ICD IDENTITY SYSTEM — WCAG 2.1 CONTRAST & ACCESSIBILITY AUDIT")
    print("=" * 80)

    for p in palettes:
        p_id = p["id"]
        p_name = p.get("fullName", p["name"])
        tokens = p["tokens"]
        print(f"\n▶ Palette: {p_name} ({p_id})")

        for f in fabrics:
            f_id = f["id"]
            f_name = f["name"]
            f_hex = f["hex"]

            accent_ratio = contrast_ratio(tokens["accent"], f_hex)
            bright_ratio = contrast_ratio(tokens["bright"], f_hex)
            mid_ratio = contrast_ratio(tokens["mid"], f_hex)

            def badge(ratio: float) -> str:
                if ratio >= 7.0:
                    return f"{ratio:4.1f}:1 [AAA]"
                elif ratio >= 4.5:
                    return f"{ratio:4.1f}:1 [AA ]"
                elif ratio >= 3.0:
                    return f"{ratio:4.1f}:1 [AA-Large]"
                else:
                    return f"{ratio:4.1f}:1 [FAIL]"

            print(f"  Background: {f_name:15} ({f_hex}) | Accent: {badge(accent_ratio)} | Bright: {badge(bright_ratio)} | Mid: {badge(mid_ratio)}")

    print("\n" + "=" * 80)
    print("  Contrast Audit complete.")

if __name__ == "__main__":
    audit_all_palettes()
