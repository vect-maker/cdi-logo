"""Candidate 4: 4D Hypercube / Tesseract.

Concept: Multi-dimensional feature space isometric 4D projection, dimension reduction.
"""
import math
import cairo
from .base import hex_to_rgb

def draw_symbol(ctx: cairo.Context, offset_x=0.0, offset_y=0.0, scale=1.0, mono=None, pal=None):
    ctx.save()
    ctx.translate(offset_x, offset_y)
    ctx.scale(scale, scale)

    c_dark   = mono or pal['dark']
    c_mid    = mono or pal['mid']
    c_bright = mono or pal['bright']
    c_accent = mono or pal['accent']

    cx, cy = 128.0, 128.0
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
