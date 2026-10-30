"""Candidate 5: Voronoi Decision Cells.

Concept: Spatial classification, K-Nearest Neighbors (KNN), and partitioned decision boundaries.
"""
import math
import cairo
from .base import hex_to_rgb

def draw_symbol(ctx: cairo.Context, offset_x=0.0, offset_y=0.0, scale=1.0, mono=None, pal=None):
    ctx.save()
    ctx.translate(offset_x, offset_y)
    ctx.scale(scale, scale)

    # Scale slightly around center (128, 128) to fill bounding box nicely
    ctx.translate(128, 128)
    ctx.scale(1.15, 1.15)
    ctx.translate(-128, -128)

    c_dark   = mono or pal['dark']
    c_mid    = mono or pal['mid']
    c_bright = mono or pal['bright']
    c_accent = mono or pal['accent']

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
