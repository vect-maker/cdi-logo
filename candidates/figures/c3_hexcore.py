"""Candidate 3: Hexagonal Data Core & Cyber Prism.

Concept: Hexagonal spatial indexing (H3), partitioned data core, and cyber prism.
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
