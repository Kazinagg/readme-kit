"""
Color manipulation and harmonization utilities for Pixel Readme Kit.
Includes conversion, contrast calculations, shading, and lighting analysis.
"""

from typing import Tuple, Optional
import colorsys


def hex_to_rgb(hex_str: str) -> Tuple[int, int, int]:
    """Parses a hex color string into (R, G, B) integer tuple [0..255]."""
    if not hex_str or not isinstance(hex_str, str):
        return (0, 0, 0)
    clean = hex_str.strip().lstrip('#')
    if len(clean) == 3:
        clean = "".join(c * 2 for c in clean)
    if len(clean) == 6:
        try:
            return (
                int(clean[0:2], 16),
                int(clean[2:4], 16),
                int(clean[4:6], 16),
            )
        except ValueError:
            return (0, 0, 0)
    return (0, 0, 0)


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """Formats RGB integer values [0..255] into lowercase #rrggbb hex string."""
    r_clamped = max(0, min(255, int(r)))
    g_clamped = max(0, min(255, int(g)))
    b_clamped = max(0, min(255, int(b)))
    return f"#{r_clamped:02x}{g_clamped:02x}{b_clamped:02x}"


def hex_to_hsl(hex_str: str) -> Tuple[float, float, float]:
    """Converts hex color to HSL tuple (h [0..360], s [0..1], l [0..1])."""
    r, g, b = hex_to_rgb(hex_str)
    h, l, s = colorsys.rgb_to_hls(r / 255.0, g / 255.0, b / 255.0)
    return (h * 360.0, s, l)


def hsl_to_hex(h: float, s: float, l: float) -> str:
    """Converts HSL (h [0..360], s [0..1], l [0..1]) to #rrggbb hex string."""
    h_norm = (h % 360.0) / 360.0
    s_clamped = max(0.0, min(1.0, float(s)))
    l_clamped = max(0.0, min(1.0, float(l)))
    r, g, b = colorsys.hls_to_rgb(h_norm, l_clamped, s_clamped)
    return rgb_to_hex(int(r * 255.0), int(g * 255.0), int(b * 255.0))


def is_light_color(hex_str: str) -> bool:
    """
    Determines if color brightness is above light threshold (> 150 / 255).
    Preserves exact backward compatibility with engine.is_light_color.
    """
    if not hex_str or not isinstance(hex_str, str):
        return False
    clean = hex_str.strip().lstrip('#')
    if len(clean) == 6:
        try:
            r, g, b = int(clean[0:2], 16), int(clean[2:4], 16), int(clean[4:6], 16)
            brightness = (r * 299 + g * 587 + b * 114) / 1000
            return brightness > 150
        except Exception:
            return False
    return False


def darken_hex(hex_str: str, factor: float = 0.4) -> str:
    """
    Multiplies RGB channels by factor [0.0..1.0] to darken.
    Preserves exact backward compatibility with engine.darken_hex.
    """
    if not hex_str or not isinstance(hex_str, str):
        return "#050B14"
    clean = hex_str.strip().lstrip('#')
    if len(clean) == 6:
        try:
            r, g, b = int(clean[0:2], 16), int(clean[2:4], 16), int(clean[4:6], 16)
            r = max(0, min(255, int(r * factor)))
            g = max(0, min(255, int(g * factor)))
            b = max(0, min(255, int(b * factor)))
            return f"#{r:02x}{g:02x}{b:02x}"
        except Exception:
            return "#050B14"
    return "#050B14"


def lighten_hex(hex_str: str, factor: float = 0.4) -> str:
    """Blends color towards white (#ffffff) by factor [0.0..1.0]."""
    r, g, b = hex_to_rgb(hex_str)
    new_r = r + (255 - r) * factor
    new_g = g + (255 - g) * factor
    new_b = b + (255 - b) * factor
    return rgb_to_hex(int(new_r), int(new_g), int(new_b))


def relative_luminance(hex_str: str) -> float:
    """Calculates WCAG 2.1 relative luminance for a color [0.0..1.0]."""
    r, g, b = hex_to_rgb(hex_str)
    def _channel_lum(c: int) -> float:
        val = c / 255.0
        return val / 12.92 if val <= 0.03928 else ((val + 0.055) / 1.055) ** 2.4

    rl = _channel_lum(r)
    gl = _channel_lum(g)
    bl = _channel_lum(b)
    return 0.2126 * rl + 0.7152 * gl + 0.0722 * bl


def contrast_ratio(hex1: str, hex2: str) -> float:
    """Calculates WCAG contrast ratio between two colors [1.0..21.0]."""
    l1 = relative_luminance(hex1)
    l2 = relative_luminance(hex2)
    lighter = max(l1, l2)
    darker = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)


def get_shadow_colors(
    primary_hex: Optional[str],
    default_mid: Optional[str] = None,
    default_dark: Optional[str] = None,
) -> Tuple[str, str]:
    """
    Computes title_mid and title_dark layered drop shadows from primary color.
    If primary_hex matches base style or is None, returns defaults.
    """
    if not primary_hex:
        return default_mid or "#006B74", default_dark or "#002B2F"
    return darken_hex(primary_hex, 0.45), darken_hex(primary_hex, 0.15)
