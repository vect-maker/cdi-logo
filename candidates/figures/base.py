"""Base utilities and helper functions for modular candidate geometry generators."""
import cairo

def hex_to_rgb(hex_str: str) -> tuple[float, float, float]:
    """Convert hex color string (#RRGGBB) to Cairo float RGB (0.0-1.0)."""
    h = hex_str.lstrip('#')
    return tuple(int(h[i:i+2], 16) / 255.0 for i in (0, 2, 4))  # type: ignore

def draw_polygon(ctx: cairo.Context, points: list[tuple[float, float]], color_hex: str) -> None:
    """Draw a closed polygon path filled with color_hex."""
    if not points:
        return
    r, g, b = hex_to_rgb(color_hex)
    ctx.set_source_rgb(r, g, b)
    ctx.new_path()
    ctx.move_to(points[0][0], points[0][1])
    for pt in points[1:]:
        ctx.line_to(pt[0], pt[1])
    ctx.close_path()
    ctx.fill()
