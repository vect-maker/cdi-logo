"""Candidate 1: Neural Cluster & Distributed Nodes.

Concept: Distributed graph neural networks, node embeddings, and synaptic connections.
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

    nodes = {
        'N1': (46.0, 48.0),
        'N2': (46.0, 128.0),
        'N3': (46.0, 208.0),
        'N4': (124.0, 70.0),
        'N5': (124.0, 186.0),
        'N6': (208.0, 128.0),
        'S1': (86.0, 98.0),
        'S2': (86.0, 158.0),
        'S3': (160.0, 128.0)
    }

    outer_edges = [
        ('N1', 'N2', 8.0, c_dark),
        ('N2', 'N3', 8.0, c_dark),
        ('N1', 'N4', 8.0, c_mid),
        ('N4', 'N6', 9.0, c_accent),
        ('N3', 'N5', 8.0, c_mid),
        ('N5', 'N6', 9.0, c_accent),
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
        ('N2', 'S1', 4.0, c_dark),
        ('N2', 'S2', 4.0, c_dark),
        ('N1', 'S1', 4.0, c_dark),
        ('N3', 'S2', 4.0, c_dark),
        ('S1', 'N4', 5.0, c_mid),
        ('S2', 'N5', 5.0, c_mid),
        ('S1', 'S2', 4.0, c_dark),
        ('N4', 'N5', 5.0, c_mid),
        ('N4', 'S3', 4.0, c_accent),
        ('N5', 'S3', 4.0, c_accent),
        ('S3', 'N6', 6.0, c_accent),
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
