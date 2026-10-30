"""Registry of modular candidate geometry generators."""
from . import c1_neural, c2_matrix, c3_hexcore, c4_tesseract, c5_voronoi, c6_waveform

FIGURE_MODULES = {
    "c1_neural": c1_neural.draw_symbol,
    "c2_matrix": c2_matrix.draw_symbol,
    "c3_hexcore": c3_hexcore.draw_symbol,
    "c4_tesseract": c4_tesseract.draw_symbol,
    "c5_voronoi": c5_voronoi.draw_symbol,
    "c6_waveform": c6_waveform.draw_symbol,
}

def get_symbol_drawer(module_name: str):
    """Retrieve draw_symbol function for a candidate module."""
    if module_name not in FIGURE_MODULES:
        raise ValueError(f"Unknown figure module: '{module_name}'. Available: {list(FIGURE_MODULES.keys())}")
    return FIGURE_MODULES[module_name]
