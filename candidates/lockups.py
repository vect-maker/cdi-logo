"""Standardized typography lockup and SVG compilation engine for ICD Identity System.

Generates:
- Symbol only: 256×256
- Horizontal 3-tier lockup: 920×256
- Centered stacked 3-tier lockup: 512×512
- Light and dark textile / background variants
- 1-color monochrome masters (Black and White)
"""
import cairo
from .figures.base import hex_to_rgb

def add_outlined_text(ctx: cairo.Context, text: str, x: float, y: float, font_size: float, font_family="Liberation Sans", bold=True, color_hex="#0B132B"):
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

def add_centered_outlined_text(ctx: cairo.Context, text: str, center_x: float, y: float, font_size: float, font_family="Liberation Sans", bold=True, color_hex="#0B132B"):
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

def save_svg_file(filename: str, title: str, width: int, height: int, draw_func):
    """Render to Cairo SVGSurface and ensure standard <title> tag insertion."""
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

def make_horizontal_lockup(filename: str, title: str, drawer, pal: dict, mono: str | None = None, light_bg: bool = False):
    """Build 920×256 horizontal lockup with precision text geometry."""
    c_mid    = mono or pal['mid']
    c_accent = mono or pal['accent']
    c_tier2  = "#0F172A" if light_bg else (mono or "#FFFFFF")
    c_tier3  = "#334155" if light_bg else (mono or "#E2E8F0")

    def draw(ctx):
        drawer(ctx, offset_x=26, offset_y=25, scale=0.80, mono=mono, pal=pal)

        # Tier 1: ICD Monogram
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

def make_stacked_lockup(filename: str, title: str, drawer, pal: dict, mono: str | None = None, light_bg: bool = False):
    """Build 512×512 centered stacked lockup."""
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
