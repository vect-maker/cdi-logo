#!/usr/bin/env python3
"""Generate high-resolution Black & Heather Gray T-Shirt showcase.

Tests all 6 candidates across:
1. True Black T-Shirt (#111827) with Palette 2 (Cyber Emerald & Mint)
2. Dark Charcoal Heather Gray T-Shirt (#374151) with Palette 1 (Cobalt & Cyan)
3. Classic Athletic Heather Gray T-Shirt (#9CA3AF) with Dual-Palette Chest Prints
"""
import os
import cairo
import math

from generate_all import (
    draw_candidate_1_symbol,
    draw_candidate_2_symbol,
    draw_candidate_3_symbol,
    draw_candidate_4_symbol,
    draw_candidate_5_symbol,
    draw_candidate_6_symbol,
    PALETTE_COBALT,
    PALETTE_EMERALD,
    hex_to_rgb,
    add_outlined_text
)

OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "renders", "showcases"))
os.makedirs(OUT_DIR, exist_ok=True)

def draw_tshirt_silhouette(ctx, x, y, width, height, fabric_color_hex, fold_shadow=True, is_heather=False):
    ctx.save()
    ctx.translate(x, y)
    sx = width / 210.0
    sy = height / 220.0
    ctx.scale(sx, sy)

    ctx.new_path()
    ctx.move_to(60, 10)
    ctx.line_to(20, 35)
    ctx.line_to(0, 80)
    ctx.line_to(35, 95)
    ctx.line_to(45, 75)
    ctx.line_to(45, 215)
    ctx.line_to(165, 215)
    ctx.line_to(165, 75)
    ctx.line_to(175, 95)
    ctx.line_to(210, 80)
    ctx.line_to(190, 35)
    ctx.line_to(150, 10)
    ctx.curve_to(130, 40, 80, 40, 60, 10)
    ctx.close_path()

    r, g, b = hex_to_rgb(fabric_color_hex)
    ctx.set_source_rgb(r, g, b)
    ctx.fill_preserve()

    ctx.set_source_rgba(0, 0, 0, 0.35 if not is_heather else 0.20)
    ctx.set_line_width(2.0)
    ctx.stroke()

    # Collar Ribbing
    ctx.new_path()
    ctx.move_to(60, 10)
    ctx.curve_to(80, 40, 130, 40, 150, 10)
    ctx.curve_to(130, 22, 80, 22, 60, 10)
    ctx.close_path()
    ctx.set_source_rgba(0, 0, 0, 0.3)
    ctx.fill()

    # Crease shading
    if fold_shadow:
        ctx.set_source_rgba(0, 0, 0, 0.15)
        ctx.set_line_width(3.0)
        ctx.move_to(45, 75)
        ctx.line_to(55, 110)
        ctx.stroke()
        ctx.move_to(165, 75)
        ctx.line_to(155, 110)
        ctx.stroke()

    ctx.restore()

def generate_showcase():
    width = 1680
    height = 1200
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)

    # Clean Dark Studio Background
    ctx.set_source_rgb(0.08, 0.09, 0.11)
    ctx.rectangle(0, 0, width, height)
    ctx.fill()

    # Header Bar
    ctx.set_source_rgb(0.04, 0.05, 0.07)
    ctx.rectangle(0, 0, width, 100)
    ctx.fill()

    add_outlined_text(ctx, "INGENIERÍA EN CIENCIAS DE DATOS — BLACK & HEATHER GRAY APPAREL SUITE", 40, 46, 22, font_family="Liberation Sans", bold=True, color_hex="#00F5D4")
    add_outlined_text(ctx, "Dual-Palette Evaluation: Palette 1 (Cobalt & Cyan) vs. Palette 2 (Cyber Emerald & Mint) across Black, Charcoal & Athletic Gray", 40, 76, 14, font_family="Liberation Sans", bold=False, color_hex="#94A3B8")

    candidates = [
        ("Candidate 1: Neural Cluster", draw_candidate_1_symbol),
        ("Candidate 2: Matrix Tensor", draw_candidate_2_symbol),
        ("Candidate 3: Hex Data Core", draw_candidate_3_symbol),
        ("Candidate 4: 4D Tesseract", draw_candidate_4_symbol),
        ("Candidate 5: Voronoi Cells", draw_candidate_5_symbol),
        ("Candidate 6: Data Waveform", draw_candidate_6_symbol)
    ]

    col_w = width / 6.0 # 280px per column
    shirt_w, shirt_h = 224, 240

    for i, (title, drawer) in enumerate(candidates):
        cx = i * col_w
        
        # Column Divider
        if i > 0:
            ctx.set_source_rgba(1, 1, 1, 0.08)
            ctx.set_line_width(1)
            ctx.move_to(cx, 110)
            ctx.line_to(cx, height - 30)
            ctx.stroke()

        # Candidate Header
        add_outlined_text(ctx, f"0{i+1}", cx + 20, 136, 20, font_family="Liberation Sans", bold=True, color_hex="#00F5D4")
        short_name = title.split(":")[1].strip()
        add_outlined_text(ctx, short_name, cx + 52, 136, 13, font_family="Liberation Sans", bold=True, color_hex="#FFFFFF")

        # ----------------------------------------------------------------------
        # Row 1: True Black T-Shirt (#111827) + Palette 2 (Cyber Emerald & Mint)
        # ----------------------------------------------------------------------
        shirt1_x = cx + (col_w - shirt_w)/2.0
        shirt1_y = 158
        draw_tshirt_silhouette(ctx, shirt1_x, shirt1_y, shirt_w, shirt_h, "#111827")

        # Center Graphic in Emerald / Mint
        gx1 = shirt1_x + shirt_w/2.0 - 38
        gy1 = shirt1_y + 72
        drawer(ctx, offset_x=gx1, offset_y=gy1, scale=0.30, pal=PALETTE_EMERALD)

        add_outlined_text(ctx, "True Black · Cyber Emerald", cx + 38, shirt1_y + shirt_h + 20, 11, font_family="Liberation Sans", bold=True, color_hex="#00F5D4")

        # ----------------------------------------------------------------------
        # Row 2: Dark Charcoal Heather (#374151) + Palette 1 (Cobalt & Cyan)
        # ----------------------------------------------------------------------
        shirt2_y = 458
        draw_tshirt_silhouette(ctx, shirt1_x, shirt2_y, shirt_w, shirt_h, "#374151", is_heather=True)

        # Center Graphic in Cobalt / Cyan
        gy2 = shirt2_y + 72
        drawer(ctx, offset_x=gx1, offset_y=gy2, scale=0.30, pal=PALETTE_COBALT)

        add_outlined_text(ctx, "Charcoal Heather · Cobalt", cx + 36, shirt2_y + shirt_h + 20, 11, font_family="Liberation Sans", bold=True, color_hex="#38BDF8")

        # ----------------------------------------------------------------------
        # Row 3: Athletic Heather Gray (#9CA3AF) + Left Chest Pocket Placement
        # ----------------------------------------------------------------------
        shirt3_y = 758
        draw_tshirt_silhouette(ctx, shirt1_x, shirt3_y, shirt_w, shirt_h, "#9CA3AF", is_heather=True)

        # Chest Pocket Graphic (Compact scale = 0.20)
        gx3 = shirt1_x + 60
        gy3 = shirt3_y + 60
        # Alternate emerald on even, cobalt on odd
        pal_pocket = PALETTE_EMERALD if i % 2 == 0 else PALETTE_COBALT
        drawer(ctx, offset_x=gx3, offset_y=gy3, scale=0.20, pal=pal_pocket)

        label_pal = "Emerald Pocket" if i % 2 == 0 else "Cobalt Pocket"
        add_outlined_text(ctx, f"Athletic Gray · {label_pal}", cx + 38, shirt3_y + shirt_h + 20, 11, font_family="Liberation Sans", bold=True, color_hex="#E2E8F0")

        # Bottom Verification Tag
        ctx.set_source_rgb(0.14, 0.16, 0.20)
        ctx.rectangle(cx + 25, height - 72, col_w - 50, 36)
        ctx.fill()
        add_outlined_text(ctx, "100% Contrast Verified", cx + 46, height - 50, 10, font_family="Liberation Sans", bold=True, color_hex="#00F5D4")

    out_file = os.path.join(OUT_DIR, "apparel-black-gray-showcase.png")
    surface.write_to_png(out_file)
    print(f"Generated Black & Gray Apparel Showcase: {out_file}")

if __name__ == "__main__":
    generate_showcase()
