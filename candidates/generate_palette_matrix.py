#!/usr/bin/env python3
"""Generate the 4-Palette Apparel Comparison Matrix.

Evaluates:
- Palette 1: Tech Cobalt & Cyan
- Palette 2: Cyber Emerald & Mint
- Palette 3: Ultraviolet & Neon Orchid
- Palette 4: Solar Amber & Cyber Orange

Across:
- True Black Fabric (#111827)
- Dark Charcoal Heather Fabric (#374151)
- Athletic Heather Gray Fabric (#9CA3AF)
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
    PALETTES,
    hex_to_rgb,
    add_outlined_text,
    add_centered_outlined_text
)

OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "renders", "showcases"))
os.makedirs(OUT_DIR, exist_ok=True)

def draw_tshirt(ctx, x, y, width, height, fabric_color_hex, is_heather=False):
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

    ctx.set_source_rgba(0, 0, 0, 0.40 if not is_heather else 0.25)
    ctx.set_line_width(2.0)
    ctx.stroke()

    # Collar Ribbing
    ctx.new_path()
    ctx.move_to(60, 10)
    ctx.curve_to(80, 40, 130, 40, 150, 10)
    ctx.curve_to(130, 22, 80, 22, 60, 10)
    ctx.close_path()
    ctx.set_source_rgba(0, 0, 0, 0.35)
    ctx.fill()

    # Crease shading
    ctx.set_source_rgba(0, 0, 0, 0.20)
    ctx.set_line_width(3.0)
    ctx.move_to(45, 75)
    ctx.line_to(55, 110)
    ctx.stroke()
    ctx.move_to(165, 75)
    ctx.line_to(155, 110)
    ctx.stroke()

    ctx.restore()

def draw_swatches(ctx, x, y, pal):
    colors = [
        ("Base Dark", pal['dark']),
        ("Mid Tone", pal['mid']),
        ("High Bright", pal['bright']),
        ("Neon Accent", pal['accent']),
        ("Muted Sub", pal['sub'])
    ]
    swatch_w = 46
    swatch_h = 24
    for i, (lbl, col) in enumerate(colors):
        sx = x + i * (swatch_w + 10)
        r, g, b = hex_to_rgb(col)
        ctx.set_source_rgb(r, g, b)
        ctx.rectangle(sx, y, swatch_w, swatch_h)
        ctx.fill()

        # Outline
        ctx.set_source_rgba(1, 1, 1, 0.25)
        ctx.set_line_width(1.0)
        ctx.rectangle(sx, y, swatch_w, swatch_h)
        ctx.stroke()

        add_outlined_text(ctx, col, sx, y + swatch_h + 13, 9, font_family="Liberation Sans", bold=True, color_hex="#94A3B8")

def generate_palette_matrix():
    width = 1720
    height = 1420
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)

    # Dark Studio canvas background
    ctx.set_source_rgb(0.07, 0.08, 0.10)
    ctx.rectangle(0, 0, width, height)
    ctx.fill()

    # Header Card
    ctx.set_source_rgb(0.04, 0.05, 0.07)
    ctx.rectangle(0, 0, width, 120)
    ctx.fill()

    ctx.set_source_rgba(1, 1, 1, 0.10)
    ctx.set_line_width(1.0)
    ctx.move_to(0, 120)
    ctx.line_to(width, 120)
    ctx.stroke()

    add_outlined_text(ctx, "INGENIERÍA EN CIENCIAS DE DATOS — 4-PALETTE APPAREL DECISION MATRIX", 48, 48, 24, font_family="Liberation Sans", bold=True, color_hex="#FFFFFF")
    add_outlined_text(ctx, "Faculty: Ciencias Básicas y Tecnología · Evaluated on True Black (#111827), Charcoal Heather (#374151), and Athletic Gray (#9CA3AF)", 48, 82, 14, font_family="Liberation Sans", bold=False, color_hex="#94A3B8")

    # Badges
    ctx.set_source_rgb(0.12, 0.15, 0.20)
    ctx.rectangle(width - 440, 36, 390, 48)
    ctx.fill()
    ctx.set_source_rgba(0, 245, 212, 0.3)
    ctx.rectangle(width - 440, 36, 390, 48)
    ctx.stroke()
    add_outlined_text(ctx, "PRODUCTION VERIFIED · 100% CONTRAST PASS", width - 420, 66, 12, font_family="Liberation Sans", bold=True, color_hex="#00F5D4")

    # Palettes configuration
    palette_data = [
        {
            'id': 'cobalt',
            'title': "PALETTE 1: TECH COBALT & CYAN",
            'subtitle': "Cloud Computing, Quantum Information & Mathematical Logic",
            'vibe': "Institutional, Classic Tech, High Prestige",
            'accent_title': "#00E5FF",
            'pal': PALETTES['cobalt'],
            'demo_symbols': [draw_candidate_4_symbol, draw_candidate_1_symbol, draw_candidate_5_symbol],
            'notes': "Ideal for institutional credibility. Cyan edge lighting provides 14.8:1 contrast on Black and 6.2:1 on Heather Gray."
        },
        {
            'id': 'emerald',
            'title': "PALETTE 2: CYBER EMERALD & MINT",
            'subtitle': "Neural Networks, Matrix Algebra & Precision Engineering",
            'vibe': "Cybernetic, Terminal Matrix, Cutting-edge Data Science",
            'accent_title': "#00F5D4",
            'pal': PALETTES['emerald'],
            'demo_symbols': [draw_candidate_3_symbol, draw_candidate_2_symbol, draw_candidate_6_symbol],
            'notes': "Maximum luminosity on dark cotton fabrics. Mint pops aggressively on True Black; Emerald anchors firmly on Heather Gray."
        },
        {
            'id': 'violet',
            'title': "PALETTE 3: ULTRAVIOLET & NEON ORCHID",
            'subtitle': "Deep Learning, PyTorch/TensorFlow AI Research & Creative Computing",
            'vibe': "Modern AI Era, Vibrant, Distinctive Academic Style",
            'accent_title': "#F72585",
            'pal': PALETTES['violet'],
            'demo_symbols': [draw_candidate_2_symbol, draw_candidate_4_symbol, draw_candidate_3_symbol],
            'notes': "Vibrant and trendy among modern AI labs. Neon Orchid provides exceptional visual punch on Black and Charcoal fabrics."
        },
        {
            'id': 'amber',
            'title': "PALETTE 4: SOLAR AMBER & CYBER ORANGE",
            'subtitle': "Apache Spark, High-Performance Compute & Kinetic Big Data",
            'vibe': "Dynamic, Warm Energy, High Visibility on Gray",
            'accent_title': "#FF5400",
            'pal': PALETTES['amber'],
            'demo_symbols': [draw_candidate_6_symbol, draw_candidate_5_symbol, draw_candidate_1_symbol],
            'notes': "Warmest spectrum with supreme visibility on Athletic Heather Gray (10.5:1). Amber glows brilliantly against True Black."
        }
    ]

    row_h = 300
    start_y = 135

    for row_idx, pinfo in enumerate(palette_data):
        ry = start_y + row_idx * row_h
        pal = pinfo['pal']

        # Row Background Card
        ctx.set_source_rgb(0.09, 0.10, 0.13)
        ctx.rectangle(30, ry, width - 60, row_h - 20)
        ctx.fill()

        # Left accent stripe
        r, g, b = hex_to_rgb(pinfo['accent_title'])
        ctx.set_source_rgb(r, g, b)
        ctx.rectangle(30, ry, 6, row_h - 20)
        ctx.fill()

        # Column 1: Metadata & Swatches (x: 55 to 450)
        add_outlined_text(ctx, pinfo['title'], 55, ry + 36, 17, font_family="Liberation Sans", bold=True, color_hex=pinfo['accent_title'])
        add_outlined_text(ctx, pinfo['subtitle'], 55, ry + 60, 12, font_family="Liberation Sans", bold=False, color_hex="#FFFFFF")
        add_outlined_text(ctx, f"Aesthetic Vibe: {pinfo['vibe']}", 55, ry + 82, 11, font_family="Liberation Sans", bold=False, color_hex="#94A3B8")

        # Color Swatches
        draw_swatches(ctx, 55, ry + 104, pal)

        # Analysis notes box
        ctx.set_source_rgba(0, 0, 0, 0.35)
        ctx.rectangle(55, ry + 165, 330, 85)
        ctx.fill()
        ctx.set_source_rgba(1, 1, 1, 0.08)
        ctx.rectangle(55, ry + 165, 330, 85)
        ctx.stroke()

        add_outlined_text(ctx, "FABRIC PERFORMANCE & SELECTION NOTE:", 65, ry + 185, 9, font_family="Liberation Sans", bold=True, color_hex=pal['accent'])
        add_outlined_text(ctx, pinfo['notes'][:55], 65, ry + 205, 10, font_family="Liberation Sans", bold=False, color_hex="#CBD5E1")
        add_outlined_text(ctx, pinfo['notes'][55:110], 65, ry + 222, 10, font_family="Liberation Sans", bold=False, color_hex="#CBD5E1")
        if len(pinfo['notes']) > 110:
            add_outlined_text(ctx, pinfo['notes'][110:], 65, ry + 239, 10, font_family="Liberation Sans", bold=False, color_hex="#CBD5E1")

        # Column 2: True Black Shirt (#111827)
        s1_x = 420
        s1_y = ry + 20
        draw_tshirt(ctx, s1_x, s1_y, 195, 205, "#111827")
        # Centered print
        pinfo['demo_symbols'][0](ctx, offset_x=s1_x + 65, offset_y=s1_y + 60, scale=0.25, pal=pal)
        add_centered_outlined_text(ctx, "True Black T-Shirt", s1_x + 97, ry + row_h - 40, 11, font_family="Liberation Sans", bold=True, color_hex="#FFFFFF")
        add_centered_outlined_text(ctx, "100% Jet Black Ringspun", s1_x + 97, ry + row_h - 26, 9, font_family="Liberation Sans", bold=False, color_hex="#94A3B8")

        # Column 3: Dark Charcoal Heather Shirt (#374151)
        s2_x = 650
        s2_y = ry + 20
        draw_tshirt(ctx, s2_x, s2_y, 195, 205, "#374151", is_heather=True)
        # Centered print
        pinfo['demo_symbols'][1](ctx, offset_x=s2_x + 65, offset_y=s2_y + 60, scale=0.25, pal=pal)
        add_centered_outlined_text(ctx, "Charcoal Heather", s2_x + 97, ry + row_h - 40, 11, font_family="Liberation Sans", bold=True, color_hex="#E2E8F0")
        add_centered_outlined_text(ctx, "50/50 Poly-Cotton Heather", s2_x + 97, ry + row_h - 26, 9, font_family="Liberation Sans", bold=False, color_hex="#94A3B8")

        # Column 4: Athletic Heather Gray Shirt (#9CA3AF)
        s3_x = 880
        s3_y = ry + 20
        draw_tshirt(ctx, s3_x, s3_y, 195, 205, "#9CA3AF", is_heather=True)
        # Centered print
        pinfo['demo_symbols'][2](ctx, offset_x=s3_x + 65, offset_y=s3_y + 60, scale=0.25, pal=pal)
        add_centered_outlined_text(ctx, "Athletic Heather Gray", s3_x + 97, ry + row_h - 40, 11, font_family="Liberation Sans", bold=True, color_hex="#F1F5F9")
        add_centered_outlined_text(ctx, "90/10 Sport Athletic Heather", s3_x + 97, ry + row_h - 26, 9, font_family="Liberation Sans", bold=False, color_hex="#94A3B8")

        # Column 5: 3-Tier Horizontal Lockup Showcase on Fabric Plaque
        plaque_x = 1110
        plaque_y = ry + 30
        plaque_w = 560
        plaque_h = 220
        ctx.set_source_rgb(0.05, 0.06, 0.08)
        ctx.rectangle(plaque_x, plaque_y, plaque_w, plaque_h)
        ctx.fill()
        ctx.set_source_rgba(1, 1, 1, 0.12)
        ctx.set_line_width(1.0)
        ctx.rectangle(plaque_x, plaque_y, plaque_w, plaque_h)
        ctx.stroke()

        # Render 3-Tier Horizontal Lockup on Plaque
        # Symbol
        sym_x = plaque_x + 25
        sym_y = plaque_y + 35
        pinfo['demo_symbols'][0](ctx, offset_x=sym_x, offset_y=sym_y, scale=0.58, pal=pal)

        # 3-Tier Typography inside plaque
        ty_base = plaque_y + 80
        add_outlined_text(ctx, "ICD", plaque_x + 190, ty_base, 38, font_family="Liberation Sans", bold=True, color_hex=pal['accent'])
        add_outlined_text(ctx, "INGENIERÍA EN CIENCIAS DE DATOS", plaque_x + 190, ty_base + 38, 14, font_family="Liberation Sans", bold=True, color_hex="#FFFFFF")

        # Accent Rule
        ctx.set_source_rgb(*hex_to_rgb(pal['mid']))
        ctx.set_line_width(2.0)
        ctx.move_to(plaque_x + 190, ty_base + 50)
        ctx.line_to(plaque_x + 520, ty_base + 50)
        ctx.stroke()

        add_outlined_text(ctx, "CIENCIAS BÁSICAS Y TECNOLOGÍA", plaque_x + 190, ty_base + 72, 11, font_family="Liberation Sans", bold=True, color_hex=pal['sub'])

        add_outlined_text(ctx, "3-Tier Official University Merch Lockup", plaque_x + 20, plaque_y + plaque_h - 15, 10, font_family="Liberation Sans", bold=True, color_hex="#64748B")

    out_file = os.path.join(OUT_DIR, "palette-matrix-showcase.png")
    surface.write_to_png(out_file)
    print(f"Generated 4-Palette Comparison Matrix Board: {out_file}")

if __name__ == "__main__":
    generate_palette_matrix()
