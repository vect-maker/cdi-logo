#!/usr/bin/env python3
"""Generate complete master SVG suite for all 6 candidates across 4 palettes + monochrome.

Candidate Roster:
1. Candidate 1: Neural Cluster & Distributed Nodes (Advanced from Round 1)
2. Candidate 2: Multidimensional Matrix Tensor (Advanced from Round 1)
3. Candidate 3: Hexagonal Data Core & Cyber Prism (Advanced from Round 1)
4. Candidate 4: 4D Hypercube / Tesseract (Feature Space Projection) [NEW]
5. Candidate 5: Voronoi Decision Cells (Spatial Classification & Clustering) [NEW]
6. Candidate 6: Harmonized Signal & Quantized Waveform (Entropy to Order) [NEW]

Curated Palettes:
1. Tech Cobalt & Cyan ('Cloud Computing & Precision Logic')
2. Cyber Emerald & Mint ('Neural Streams & Matrix Cybernetics')
3. Ultraviolet & Neon Orchid ('Deep Learning & AI Research')
4. Solar Amber & Cyber Orange ('High-Performance Compute & Spark')

Outputs for each candidate:
- Symbol only (256x256) in 4 palettes + 1-color black + 1-color white
- Horizontal 3-tier lockup (920x256) in 4 palettes
- Centered stacked 3-tier lockup (512x512) in 4 palettes
"""
import os
import math
import cairo

OUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "candidates"))
os.makedirs(OUT_DIR, exist_ok=True)

# The 4 Curated Palettes
PALETTES = {
    'cobalt': {
        'name':    "Tech Cobalt and Cyan",
        'dark':    "#1E40AF",   # Luminous Royal Cobalt (3.8:1 on black, distinct blue hue)
        'mid':     "#3B82F6",   # Electric Azure (5.8:1 on black)
        'bright':  "#60A5FA",   # Sky Highlight (8.2:1 on black)
        'accent':  "#00F0FF",   # Neon Cyan (13.2:1 on black)
        'sub':     "#E2E8F0",
        'white':   "#FFFFFF"
    },
    'emerald': {
        'name':    "Cyber Emerald and Mint",
        'dark':    "#065F46",   # Deep Luminous Emerald (4.1:1 on black, vibrant green hue)
        'mid':     "#10B981",   # Cyber Mint (7.0:1 on black)
        'bright':  "#34D399",   # Spring Glow (9.5:1 on black)
        'accent':  "#00F5D4",   # Neo Mint (12.7:1 on black)
        'sub':     "#E2E8F0",
        'white':   "#FFFFFF"
    },
    'violet': {
        'name':    "Ultraviolet and Neon Orchid",
        'dark':    "#5B21B6",   # Royal Violet (3.5:1 on black, rich purple hue)
        'mid':     "#8B5CF6",   # Vivid Purple (5.2:1 on black)
        'bright':  "#A78BFA",   # Orchid Glow (7.6:1 on black)
        'accent':  "#FF2A85",   # Neon Orchid (8.5:1 on black)
        'sub':     "#E2E8F0",
        'white':   "#FFFFFF"
    },
    'amber': {
        'name':    "Solar Amber and Cyber Orange",
        'dark':    "#9A3412",   # Deep Rust Amber (4.2:1 on black, warm terracotta hue)
        'mid':     "#D97706",   # Amber Mid (5.6:1 on black)
        'bright':  "#F59E0B",   # Solar Gold (8.3:1 on black)
        'accent':  "#FF5400",   # Cyber Orange (6.5:1 on black)
        'sub':     "#E2E8F0",
        'white':   "#FFFFFF"
    }
}

PALETTE_COBALT = PALETTES['cobalt']
PALETTE_EMERALD = PALETTES['emerald']
PALETTE_VIOLET = PALETTES['violet']
PALETTE_AMBER = PALETTES['amber']

def hex_to_rgb(hex_str):
    h = hex_str.lstrip('#')
    return tuple(int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4))

def add_outlined_text(ctx, text, x, y, font_size, font_family="Liberation Sans", bold=True, color_hex="#0B132B"):
    ctx.save()
    weight = cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL
    ctx.select_font_face(font_family, cairo.FONT_SLANT_NORMAL, weight)
    ctx.set_font_size(font_size)
    r, g, b = hex_to_rgb(color_hex)
    ctx.set_source_rgb(r, g, b)
    ctx.move_to(x, y)
    ctx.text_path(text)
    ctx.fill()
    ctx.restore()

def add_centered_outlined_text(ctx, text, center_x, y, font_size, font_family="Liberation Sans", bold=True, color_hex="#0B132B"):
    ctx.save()
    weight = cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL
    ctx.select_font_face(font_family, cairo.FONT_SLANT_NORMAL, weight)
    ctx.set_font_size(font_size)
    ext = ctx.text_extents(text)
    x = center_x - (ext.width / 2.0 + ext.x_bearing)
    r, g, b = hex_to_rgb(color_hex)
    ctx.set_source_rgb(r, g, b)
    ctx.move_to(x, y)
    ctx.text_path(text)
    ctx.fill()
    ctx.restore()

# ------------------------------------------------------------------------------
# Candidate 1: Neural Cluster & Distributed Nodes (Advanced Champion B)
# ------------------------------------------------------------------------------
def draw_candidate_1_symbol(ctx, offset_x=0, offset_y=0, scale=1.0, mono=None, pal=None):
    ctx.save()
    ctx.translate(offset_x, offset_y)
    ctx.scale(scale, scale)

    p = pal or PALETTE_COBALT
    c_dark   = mono or p['dark']
    c_mid    = mono or p['mid']
    c_accent = mono or p['accent']

    nodes = {
        'N1': (46, 48),
        'N2': (46, 128),
        'N3': (46, 208),
        'N4': (124, 70),
        'N5': (124, 186),
        'N6': (208, 128),
        'S1': (86, 98),
        'S2': (86, 158),
        'S3': (160, 128)
    }

    outer_edges = [
        ('N1', 'N2', 8, c_dark),
        ('N2', 'N3', 8, c_dark),
        ('N1', 'N4', 8, c_mid),
        ('N4', 'N6', 9, c_accent),
        ('N3', 'N5', 8, c_mid),
        ('N5', 'N6', 9, c_accent),
    ]
    for n_a, n_b, width, color in outer_edges:
        r, g, b = hex_to_rgb(color)
        ctx.set_source_rgb(r, g, b)
        ctx.set_line_width(width)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.move_to(*nodes[n_a])
        ctx.line_to(*nodes[n_b])
        ctx.stroke()

    inner_edges = [
        ('N2', 'S1', 4, c_dark),
        ('N2', 'S2', 4, c_dark),
        ('N1', 'S1', 4, c_dark),
        ('N3', 'S2', 4, c_dark),
        ('S1', 'N4', 5, c_mid),
        ('S2', 'N5', 5, c_mid),
        ('S1', 'S2', 4, c_dark),
        ('N4', 'N5', 5, c_mid),
        ('N4', 'S3', 4, c_accent),
        ('N5', 'S3', 4, c_accent),
        ('S3', 'N6', 6, c_accent),
    ]
    for n_a, n_b, width, color in inner_edges:
        r, g, b = hex_to_rgb(color)
        ctx.set_source_rgb(r, g, b)
        ctx.set_line_width(width)
        ctx.set_line_cap(cairo.LINE_CAP_ROUND)
        ctx.move_to(*nodes[n_a])
        ctx.line_to(*nodes[n_b])
        ctx.stroke()

    for n in ['N1', 'N2', 'N3']:
        r, g, b = hex_to_rgb(c_dark)
        ctx.set_source_rgb(r, g, b)
        ctx.arc(nodes[n][0], nodes[n][1], 14, 0, 2*math.pi)
        ctx.fill()

    for n in ['N4', 'N5']:
        r, g, b = hex_to_rgb(c_mid)
        ctx.set_source_rgb(r, g, b)
        ctx.arc(nodes[n][0], nodes[n][1], 15, 0, 2*math.pi)
        ctx.fill()

    for n in ['S1', 'S2', 'S3']:
        r, g, b = hex_to_rgb(c_accent)
        ctx.set_source_rgb(r, g, b)
        ctx.arc(nodes[n][0], nodes[n][1], 8, 0, 2*math.pi)
        ctx.fill()

    r, g, b = hex_to_rgb(c_accent)
    ctx.set_source_rgb(r, g, b)
    ctx.arc(nodes['N6'][0], nodes['N6'][1], 20, 0, 2*math.pi)
    ctx.fill()

    ctx.restore()

# ------------------------------------------------------------------------------
# Candidate 2: Multidimensional Matrix Tensor (Advanced Champion C)
# ------------------------------------------------------------------------------
def draw_candidate_2_symbol(ctx, offset_x=0, offset_y=0, scale=1.0, mono=None, pal=None):
    ctx.save()
    ctx.translate(offset_x, offset_y)
    ctx.scale(scale, scale)

    p = pal or PALETTE_COBALT
    c_dark   = mono or p['dark']
    c_mid    = mono or p['mid']
    c_accent = mono or p['accent']

    cx, cy = 128, 140
    cos30 = math.cos(math.radians(30))
    sin30 = math.sin(math.radians(30))
    L = 82.0

    def iso_pt(u, v, w):
        return (cx + (u - v) * cos30, cy + (u + v) * sin30 - w)

    def draw_quad(p1, p2, p3, p4, color):
        r, g, b = hex_to_rgb(color)
        ctx.set_source_rgb(r, g, b)
        ctx.new_path()
        ctx.move_to(*p1)
        ctx.line_to(*p2)
        ctx.line_to(*p3)
        ctx.line_to(*p4)
        ctx.close_path()
        ctx.fill()

    n = 3
    gap = 3.0
    for iv in range(n):
        for iw in range(n):
            v0 = iv * (L/n) + gap
            v1 = (iv + 1) * (L/n) - gap
            w0 = iw * (L/n) + gap
            w1 = (iw + 1) * (L/n) - gap
            col = c_dark if (iv + iw) % 2 == 0 else c_mid
            draw_quad(iso_pt(0, v0, w0), iso_pt(0, v1, w0), iso_pt(0, v1, w1), iso_pt(0, v0, w1), col)

    for iu in range(n):
        for iw in range(n):
            u0 = iu * (L/n) + gap
            u1 = (iu + 1) * (L/n) - gap
            w0 = iw * (L/n) + gap
            w1 = (iw + 1) * (L/n) - gap
            col = c_mid if (iu + iw) % 2 == 0 else c_dark
            draw_quad(iso_pt(u0, 0, w0), iso_pt(u1, 0, w0), iso_pt(u1, 0, w1), iso_pt(u0, 0, w1), col)

    for iu in range(n):
        for iv in range(n):
            u0 = iu * (L/n) + gap
            u1 = (iu + 1) * (L/n) - gap
            v0 = iv * (L/n) + gap
            v1 = (iv + 1) * (L/n) - gap
            col = c_accent if (iu + iv) % 2 == 0 else c_mid
            draw_quad(iso_pt(u0, v0, L), iso_pt(u1, v0, L), iso_pt(u1, v1, L), iso_pt(u0, v1, L), col)

    ext = 14.0
    u0 = 2 * (L/n) + gap + ext
    u1 = 3 * (L/n) - gap + ext
    v0 = 0 * (L/n) + gap
    v1 = 1 * (L/n) - gap
    w0 = 2 * (L/n) + gap + ext
    w1 = 3 * (L/n) - gap + ext

    draw_quad(iso_pt(u0, v1, w0), iso_pt(u0, v1, w1), iso_pt(u1, v1, w1), iso_pt(u1, v1, w0), c_mid)
    draw_quad(iso_pt(u0, v0, w0), iso_pt(u1, v0, w0), iso_pt(u1, v0, w1), iso_pt(u0, v0, w1), c_accent)
    draw_quad(iso_pt(u0, v0, w1), iso_pt(u1, v0, w1), iso_pt(u1, v1, w1), iso_pt(u0, v1, w1), c_accent)

    r, g, b = hex_to_rgb(c_accent)
    ctx.set_source_rgb(r, g, b)
    ctx.set_line_width(3.5)
    p_orig = iso_pt(0, 0, 0)
    for p_dest in [iso_pt(L + 18, 0, 0), iso_pt(0, L + 18, 0), iso_pt(0, 0, L + 18)]:
        ctx.move_to(*p_orig)
        ctx.line_to(*p_dest)
        ctx.stroke()
        ctx.arc(p_dest[0], p_dest[1], 4.5, 0, 2*math.pi)
        ctx.fill()

    ctx.restore()

# ------------------------------------------------------------------------------
# Candidate 3: Hexagonal Data Core & Cyber Prism (Advanced Champion F)
# ------------------------------------------------------------------------------
def draw_candidate_3_symbol(ctx, offset_x=0, offset_y=0, scale=1.0, mono=None, pal=None):
    ctx.save()
    ctx.translate(offset_x, offset_y)
    ctx.scale(scale, scale)

    p = pal or PALETTE_COBALT
    c_dark   = mono or p['dark']
    c_mid    = mono or p['mid']
    c_accent = mono or p['accent']

    r, g, b = hex_to_rgb(c_dark)
    ctx.set_source_rgb(r, g, b)
    ctx.new_path()
    ctx.move_to(116, 46)
    ctx.line_to(48, 85)
    ctx.line_to(48, 171)
    ctx.line_to(116, 210)
    ctx.line_to(116, 168)
    ctx.line_to(82, 148)
    ctx.line_to(82, 108)
    ctx.line_to(116, 88)
    ctx.close_path()
    ctx.fill()

    r, g, b = hex_to_rgb(c_mid)
    ctx.set_source_rgb(r, g, b)
    ctx.new_path()
    ctx.move_to(138, 46)
    ctx.line_to(206, 85)
    ctx.line_to(176, 102)
    ctx.line_to(138, 80)
    ctx.close_path()
    ctx.fill()

    r, g, b = hex_to_rgb(c_accent)
    ctx.set_source_rgb(r, g, b)
    ctx.new_path()
    ctx.move_to(206, 100)
    ctx.line_to(206, 171)
    ctx.line_to(138, 210)
    ctx.line_to(138, 176)
    ctx.line_to(174, 155)
    ctx.line_to(174, 118)
    ctx.close_path()
    ctx.fill()

    r, g, b = hex_to_rgb(c_accent)
    ctx.set_source_rgb(r, g, b)
    ctx.new_path()
    ctx.move_to(128, 102)
    ctx.line_to(148, 114)
    ctx.line_to(148, 142)
    ctx.line_to(128, 154)
    ctx.line_to(108, 142)
    ctx.line_to(108, 114)
    ctx.close_path()
    ctx.fill()

    r, g, b = hex_to_rgb(c_mid)
    ctx.set_source_rgb(r, g, b)
    ctx.arc(128, 128, 7, 0, 2*math.pi)
    ctx.fill()

    ctx.restore()

# ------------------------------------------------------------------------------
# Candidate 4: 4D Hypercube / Tesseract (Multi-Dimensional Space Projection) [NEW]
# ------------------------------------------------------------------------------
def draw_candidate_4_symbol(ctx, offset_x=0, offset_y=0, scale=1.0, mono=None, pal=None):
    ctx.save()
    ctx.translate(offset_x, offset_y)
    ctx.scale(scale, scale)

    p = pal or PALETTE_COBALT
    c_dark   = mono or p['dark']
    c_mid    = mono or p['mid']
    c_bright = mono or p['bright']
    c_accent = mono or p['accent']

    cx, cy = 128, 128
    R_out = 88.0
    cos30 = math.cos(math.radians(30))
    sin30 = math.sin(math.radians(30))

    V_out = [
        (cx, cy - R_out),                         # 0: Top
        (cx + R_out * cos30, cy - R_out * sin30), # 1: Top-Right
        (cx + R_out * cos30, cy + R_out * sin30), # 2: Bottom-Right
        (cx, cy + R_out),                         # 3: Bottom
        (cx - R_out * cos30, cy + R_out * sin30), # 4: Bottom-Left
        (cx - R_out * cos30, cy - R_out * sin30), # 5: Top-Left
    ]

    R_in = R_out * 0.44
    V_in = [
        (cx, cy - R_in),                         # 0: Top
        (cx + R_in * cos30, cy - R_in * sin30), # 1: Top-Right
        (cx + R_in * cos30, cy + R_in * sin30), # 2: Bottom-Right
        (cx, cy + R_in),                         # 3: Bottom
        (cx - R_in * cos30, cy + R_in * sin30), # 4: Bottom-Left
        (cx - R_in * cos30, cy - R_in * sin30), # 5: Top-Left
    ]

    def draw_quad(p1, p2, p3, p4, col_hex, gap=2.6):
        cen_x = (p1[0] + p2[0] + p3[0] + p4[0]) / 4.0
        cen_y = (p1[1] + p2[1] + p3[1] + p4[1]) / 4.0

        def inset(p):
            dx = p[0] - cen_x
            dy = p[1] - cen_y
            dist = math.hypot(dx, dy)
            if dist == 0:
                return p
            factor = max(0.0, (dist - gap) / dist)
            return (cen_x + dx * factor, cen_y + dy * factor)

        ip1 = inset(p1)
        ip2 = inset(p2)
        ip3 = inset(p3)
        ip4 = inset(p4)

        ctx.new_path()
        ctx.move_to(*ip1)
        ctx.line_to(*ip2)
        ctx.line_to(*ip3)
        ctx.line_to(*ip4)
        ctx.close_path()

        r, g, b = hex_to_rgb(col_hex)
        ctx.set_source_rgb(r, g, b)
        ctx.fill()

    # Outer 4D Projection Struts
    draw_quad(V_out[0], V_out[1], V_in[1], V_in[0], c_mid, gap=2.6)
    draw_quad(V_out[1], V_out[2], V_in[2], V_in[1], c_dark, gap=2.6)
    draw_quad(V_out[2], V_out[3], V_in[3], V_in[2], c_dark, gap=2.6)
    draw_quad(V_out[3], V_out[4], V_in[4], V_in[3], c_mid, gap=2.6)
    draw_quad(V_out[4], V_out[5], V_in[5], V_in[4], c_bright, gap=2.6)
    draw_quad(V_out[5], V_out[0], V_in[0], V_in[5], c_bright, gap=2.6)

    # Inner Hypercube Core
    C_in = (cx, cy)
    draw_quad(V_in[5], V_in[0], V_in[1], C_in, c_accent, gap=2.0)
    draw_quad(C_in, V_in[1], V_in[2], V_in[3], c_mid, gap=2.0)
    draw_quad(V_in[4], V_in[5], C_in, V_in[3], c_bright, gap=2.0)

    # Center glowing node (accent)
    ctx.new_path()
    ctx.arc(cx, cy, 5.0, 0, 2*math.pi)
    r, g, b = hex_to_rgb(c_accent)
    ctx.set_source_rgb(r, g, b)
    ctx.fill()

    ctx.restore()

# ------------------------------------------------------------------------------
# Candidate 5: Voronoi Decision Cells (Spatial Classification & Clustering) [NEW]
# ------------------------------------------------------------------------------
def draw_candidate_5_symbol(ctx, offset_x=0, offset_y=0, scale=1.0, mono=None, pal=None):
    ctx.save()
    ctx.translate(offset_x, offset_y)
    ctx.scale(scale, scale)

    # Scale slightly around center (128, 128) to fill bounding box nicely
    ctx.translate(128, 128)
    ctx.scale(1.15, 1.15)
    ctx.translate(-128, -128)

    p = pal or PALETTE_COBALT
    c_dark   = mono or p['dark']
    c_mid    = mono or p['mid']
    c_bright = mono or p['bright']
    c_accent = mono or p['accent']

    cells = [
        # Focal Center Cell (Accent)
        ([(112, 106), (150, 98), (164, 130), (144, 156), (108, 144)], c_accent, True),
        # Top-North Cell (Bright)
        ([(96, 52), (160, 52), (150, 94), (112, 102)], c_bright, False),
        # North-East Cell (Mid)
        ([(164, 56), (208, 92), (196, 138), (166, 128), (154, 96)], c_mid, False),
        # South-East Cell (Dark)
        ([(198, 142), (192, 196), (144, 204), (146, 160), (166, 132)], c_dark, False),
        # South-West Cell (Bright)
        ([(140, 204), (88, 198), (64, 156), (106, 146), (142, 158)], c_bright, False),
        # North-West Cell (Mid)
        ([(60, 150), (48, 98), (92, 56), (110, 102), (106, 142)], c_mid, False)
    ]

    def draw_poly(pts, col_hex, is_focal=False, gap=3.2):
        cen_x = sum(p[0] for p in pts) / len(pts)
        cen_y = sum(p[1] for p in pts) / len(pts)

        def inset(p):
            dx = p[0] - cen_x
            dy = p[1] - cen_y
            dist = math.hypot(dx, dy)
            if dist == 0:
                return p
            factor = max(0.0, (dist - gap) / dist)
            return (cen_x + dx * factor, cen_y + dy * factor)

        in_pts = [inset(p) for p in pts]
        ctx.new_path()
        ctx.move_to(*in_pts[0])
        for p in in_pts[1:]:
            ctx.line_to(*p)
        ctx.close_path()

        r, g, b = hex_to_rgb(col_hex)
        ctx.set_source_rgb(r, g, b)
        ctx.fill()

    for pts, col, focal in cells:
        draw_poly(pts, col, focal)

    ctx.restore()

# ------------------------------------------------------------------------------
# Candidate 6: Harmonized Signal & Quantized Waveform (Entropy to Order) [NEW]
# ------------------------------------------------------------------------------
def draw_candidate_6_symbol(ctx, offset_x=0, offset_y=0, scale=1.0, mono=None, pal=None):
    ctx.save()
    ctx.translate(offset_x, offset_y)
    ctx.scale(scale, scale)

    p = pal or PALETTE_COBALT
    c_dark   = mono or p['dark']
    c_mid    = mono or p['mid']
    c_bright = mono or p['bright']
    c_accent = mono or p['accent']

    cx, cy = 128, 128

    bars = [
        (56,  9, 36,  c_dark),
        (80,  9, 64,  c_mid),
        (104, 9, 108, c_bright),
        (128, 11, 168, c_accent),
        (152, 9, 108, c_bright),
        (176, 9, 64,  c_mid),
        (200, 9, 36,  c_dark),
    ]

    for bx, hw, h, col in bars:
        top_y = cy - h / 2.0
        bot_y = cy + h / 2.0
        r, g, b = hex_to_rgb(col)
        ctx.set_source_rgb(r, g, b)

        cap_h = min(14.0, hw * 1.4)
        ctx.new_path()
        ctx.move_to(bx, top_y)
        ctx.line_to(bx + hw, top_y + cap_h)
        ctx.line_to(bx + hw, bot_y - cap_h)
        ctx.line_to(bx, bot_y)
        ctx.line_to(bx - hw, bot_y - cap_h)
        ctx.line_to(bx - hw, top_y + cap_h)
        ctx.close_path()
        ctx.fill()

    # Outlined horizontal carrier equilibrium bars (solid filled rectangles)
    r, g, b = hex_to_rgb(c_accent)
    ctx.set_source_rgb(r, g, b)
    ctx.rectangle(30, cy - 2, 14, 4)
    ctx.fill()
    ctx.rectangle(212, cy - 2, 14, 4)
    ctx.fill()

    ctx.restore()

# ------------------------------------------------------------------------------
# SVG Exporters
# ------------------------------------------------------------------------------
def save_svg_file(filename, title, width, height, draw_func):
    surface = cairo.SVGSurface(filename, width, height)
    ctx = cairo.Context(surface)
    draw_func(ctx)
    surface.finish()

    with open(filename, 'r', encoding='utf-8') as f:
        svg_content = f.read()

    svg_idx = svg_content.find('<svg')
    if svg_idx != -1:
        close_tag_idx = svg_content.find('>', svg_idx)
        if close_tag_idx != -1:
            clean_title = title.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            title_tag = f'\n  <title>{clean_title}</title>'
            svg_content = svg_content[:close_tag_idx+1] + title_tag + svg_content[close_tag_idx+1:]

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(svg_content)

def make_horizontal_lockup(filename, title, drawer, pal, mono=None, light_bg=False):
    c_mid    = mono or pal['mid']
    c_accent = mono or pal['accent']
    c_tier2  = "#0F172A" if light_bg else (mono or "#FFFFFF")
    c_tier3  = "#334155" if light_bg else (mono or "#E2E8F0")

    def draw(ctx):
        drawer(ctx, offset_x=26, offset_y=25, scale=0.80, mono=mono, pal=pal)

        # Tier 1: ICD
        add_outlined_text(ctx, "ICD", 280, 114, 76, font_family="Liberation Sans", bold=True, color_hex=c_accent)

        # Tier 2: INGENIERÍA EN CIENCIAS DE DATOS
        add_outlined_text(ctx, "INGENIERÍA EN CIENCIAS DE DATOS", 284, 150, 19, font_family="Liberation Sans", bold=True, color_hex=c_tier2)

        # Accent Rule Divider
        r, g, b = hex_to_rgb(c_mid)
        ctx.set_source_rgb(r, g, b)
        ctx.set_line_width(2.5)
        ctx.move_to(284, 166)
        ctx.line_to(680, 166)
        ctx.stroke()

        # Tier 3: CIENCIAS BÁSICAS Y TECNOLOGÍA
        add_outlined_text(ctx, "CIENCIAS BÁSICAS Y TECNOLOGÍA", 284, 192, 15, font_family="Liberation Sans", bold=True, color_hex=c_tier3)

    save_svg_file(filename, title, 920, 256, draw)

def make_stacked_lockup(filename, title, drawer, pal, mono=None, light_bg=False):
    c_mid    = mono or pal['mid']
    c_accent = mono or pal['accent']
    c_tier2  = "#0F172A" if light_bg else (mono or "#FFFFFF")
    c_tier3  = "#334155" if light_bg else (mono or "#E2E8F0")

    def draw(ctx):
        # Symbol centered at top
        drawer(ctx, offset_x=146, offset_y=30, scale=0.86, mono=mono, pal=pal)

        # Tier 1: Centered ICD
        add_centered_outlined_text(ctx, "ICD", 256, 320, 68, font_family="Liberation Sans", bold=True, color_hex=c_accent)

        # Tier 2: Centered INGENIERÍA EN CIENCIAS DE DATOS
        add_centered_outlined_text(ctx, "INGENIERÍA EN CIENCIAS DE DATOS", 256, 380, 18, font_family="Liberation Sans", bold=True, color_hex=c_tier2)

        # Centered Accent Rule
        r, g, b = hex_to_rgb(c_mid)
        ctx.set_source_rgb(r, g, b)
        ctx.set_line_width(2.5)
        ctx.move_to(216, 404)
        ctx.line_to(296, 404)
        ctx.stroke()

        # Tier 3: Centered CIENCIAS BÁSICAS Y TECNOLOGÍA
        add_centered_outlined_text(ctx, "CIENCIAS BÁSICAS Y TECNOLOGÍA", 256, 432, 14, font_family="Liberation Sans", bold=True, color_hex=c_tier3)

    save_svg_file(filename, title, 512, 512, draw)

def generate_all_candidates(out_dir=OUT_DIR, clean=False):
    import shutil
    if clean and os.path.exists(out_dir):
        # Clean existing subdirectories
        for item in os.listdir(out_dir):
            item_path = os.path.join(out_dir, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
            elif item.endswith('.svg') or item.endswith('.png'):
                os.remove(item_path)

    candidates = [
        ("c1-neural", "ICD Neural Cluster and Distributed Graph", draw_candidate_1_symbol),
        ("c2-matrix", "ICD Multidimensional Matrix Tensor", draw_candidate_2_symbol),
        ("c3-hexcore", "ICD Hexagonal Data Core and Cyber Prism", draw_candidate_3_symbol),
        ("c4-tesseract", "ICD 4D Hypercube Tesseract Projection", draw_candidate_4_symbol),
        ("c5-voronoi", "ICD Voronoi Decision Cells and Clustering", draw_candidate_5_symbol),
        ("c6-waveform", "ICD Harmonized Signal and Quantized Waveform", draw_candidate_6_symbol)
    ]

    for folder_name, name, drawer in candidates:
        cand_base = os.path.join(out_dir, folder_name)
        sym_dir = os.path.join(cand_base, "symbols")
        lock_dir = os.path.join(cand_base, "lockups")
        stack_dir = os.path.join(cand_base, "stacked")
        mono_dir = os.path.join(cand_base, "monochrome")

        for d in [sym_dir, lock_dir, stack_dir, mono_dir]:
            os.makedirs(d, exist_ok=True)

        for p_key, p_val in PALETTES.items():
            sym_file = os.path.join(sym_dir, f"symbol-{p_key}.svg")
            lock_file = os.path.join(lock_dir, f"lockup-{p_key}.svg")
            stack_file = os.path.join(stack_dir, f"stacked-{p_key}.svg")

            save_svg_file(sym_file, f"{name} Symbol ({p_val['name']})", 256, 256, lambda ctx, d=drawer, p=p_val: d(ctx, pal=p))
            make_horizontal_lockup(lock_file, f"{name} Lockup ({p_val['name']})", drawer, pal=p_val)
            make_stacked_lockup(stack_file, f"{name} Stacked Lockup ({p_val['name']})", drawer, pal=p_val)

            # Also generate light-apparel lockups for Heather Gray / Light backgrounds
            lock_light = os.path.join(lock_dir, f"lockup-{p_key}-light.svg")
            stack_light = os.path.join(stack_dir, f"stacked-{p_key}-light.svg")
            make_horizontal_lockup(lock_light, f"{name} Light Lockup ({p_val['name']})", drawer, pal=p_val, light_bg=True)
            make_stacked_lockup(stack_light, f"{name} Light Stacked Lockup ({p_val['name']})", drawer, pal=p_val, light_bg=True)

            # Also provide default un-suffixed copy for cobalt
            if p_key == "cobalt":
                save_svg_file(os.path.join(sym_dir, "symbol.svg"), f"{name} Symbol", 256, 256, lambda ctx, d=drawer, p=p_val: d(ctx, pal=p))
                make_horizontal_lockup(os.path.join(lock_dir, "lockup.svg"), f"{name} Lockup", drawer, pal=p_val)
                make_stacked_lockup(os.path.join(stack_dir, "stacked.svg"), f"{name} Stacked Lockup", drawer, pal=p_val)
                make_horizontal_lockup(os.path.join(lock_dir, "lockup-light.svg"), f"{name} Light Lockup", drawer, pal=p_val, light_bg=True)
                make_stacked_lockup(os.path.join(stack_dir, "stacked-light.svg"), f"{name} Light Stacked Lockup", drawer, pal=p_val, light_bg=True)

        # 1-Color Monochrome Masters (Black & White)
        mono_black = os.path.join(mono_dir, "symbol-mono-black.svg")
        mono_white = os.path.join(mono_dir, "symbol-mono-white.svg")
        save_svg_file(mono_black, f"{name} 1-Color Black", 256, 256, lambda ctx, d=drawer: d(ctx, mono="#000000"))
        save_svg_file(mono_white, f"{name} 1-Color White", 256, 256, lambda ctx, d=drawer: d(ctx, mono="#FFFFFF"))

        print(f"Generated 4-palette master suite for {folder_name}")

def main():
    import sys
    clean_flag = "--clean" in sys.argv
    generate_all_candidates(clean=clean_flag)

if __name__ == "__main__":
    main()
