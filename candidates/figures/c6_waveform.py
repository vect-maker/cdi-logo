"""Candidate 6: Harmonized Signal & Quantized Waveform.

Concept: Signal extraction, Fourier transform, entropy reduction from noise to structured order.
"""
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

    bars = [
        (56.0,  9.0, 36.0,  c_dark),
        (80.0,  9.0, 64.0,  c_mid),
        (104.0, 9.0, 108.0, c_bright),
        (128.0, 11.0, 168.0, c_accent),
        (152.0, 9.0, 108.0, c_bright),
        (176.0, 9.0, 64.0,  c_mid),
        (200.0, 9.0, 36.0,  c_dark),
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
