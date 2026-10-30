"""Candidate 2: Multidimensional Matrix Tensor.

Concept: Isometric 3D tensor slice, multidimensional matrix algebra and data cubes.
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
    c_accent = mono or pal['accent']

    cx, cy = 128.0, 140.0
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
