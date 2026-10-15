"""
Core SVG Generation Engine Façade for Pixel Readme Kit.
======================================================
Re-exports theme resolvers, text layout tools, and modular SVG components
for complete 100% backwards compatibility with v2.x and v3.x code.

Modular packages:
- generator.themes      -> Theme definitions, palettes, and color utilities
- generator.layout      -> Monospace measurement, clamping, and spec parsing
- generator.components  -> Modular SVG generators for headers, chips, callouts, etc.
"""

# 1. Themes and Color Domain
from generator.themes import (
    THEME_PALETTES,
    STYLE_PALETTES,
    VALID_STYLES,
    STYLE_THEMES,
    load_preset,
    is_light_color,
    darken_hex,
    get_shadow_colors,
    resolve_theme,
    resolve_colors,
    normalize_style_and_theme,
    get_themes_for_style,
)

# 2. Text Layout and Typography
from generator.font_engine import (
    render_3d_text,
    calculate_px_size,
    calculate_smart_layout,
)
from generator.layout import (
    measure_mono_text_width,
    clamp_text_to_width,
    wrap_text_to_lines,
    normalize_specs,
    format_tag,
    format_bottom_tag,
    estimate_chip_width,
)

# 3. Base XML / SVG Utilities
from generator.components.base import (
    escape_xml,
    validate_svg,
)

# 4. Modular SVG Component Generators
from generator.components.header import (
    generate_header,
    _generate_compact_header,
)
from generator.components.footer import generate_footer
from generator.components.callout import (
    generate_callout,
    GITHUB_ALERT_COLORS,
)
from generator.components.frame import generate_frame
from generator.components.chip import generate_chip
from generator.components.divider import (
    generate_divider,
    generate_splitter,
)
from generator.components.metrics import (
    generate_metrics,
    generate_progress,
    generate_techstack,
)
from generator.components.timeline import generate_timeline
from generator.components.social import (
    generate_social,
    generate_starchart,
    generate_profile_card,
)

__all__ = [
    # Themes
    "THEME_PALETTES",
    "STYLE_PALETTES",
    "VALID_STYLES",
    "STYLE_THEMES",
    "load_preset",
    "is_light_color",
    "darken_hex",
    "get_shadow_colors",
    "resolve_theme",
    "resolve_colors",
    "normalize_style_and_theme",
    "get_themes_for_style",
    # Text Layout & Fonts
    "render_3d_text",
    "calculate_px_size",
    "calculate_smart_layout",
    "measure_mono_text_width",
    "clamp_text_to_width",
    "wrap_text_to_lines",
    "normalize_specs",
    "format_tag",
    "format_bottom_tag",
    "estimate_chip_width",
    # Base
    "escape_xml",
    "validate_svg",
    # Components
    "generate_header",
    "_generate_compact_header",
    "generate_footer",
    "generate_callout",
    "GITHUB_ALERT_COLORS",
    "generate_frame",
    "generate_chip",
    "generate_divider",
    "generate_splitter",
    "generate_metrics",
    "generate_progress",
    "generate_techstack",
    "generate_timeline",
    "generate_social",
    "generate_starchart",
    "generate_profile_card",
]
