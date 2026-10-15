"""
Base utilities for SVG component generation in Pixel Readme Kit.
"""

import html
import xml.etree.ElementTree as ET
from typing import Any, Optional


def escape_xml(s: Any) -> str:
    """Escapes strings for safe inclusion in SVG attributes and text nodes."""
    if s is None:
        return ""
    return html.escape(str(s), quote=True)


def validate_svg(svg_content: str) -> bool:
    """Validates that SVG content parses cleanly as XML without errors."""
    try:
        ET.fromstring(svg_content)
        return True
    except ET.ParseError as e:
        raise ValueError(f"Generated SVG has invalid XML syntax: {e}\nSVG Content:\n{svg_content}")


MODERN_BASE_STYLES = """
    .font-sans { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif, 'Apple Color Emoji', 'Segoe UI Emoji'; }
    .font-mono { font-family: 'JetBrains Mono', 'SF Mono', 'Fira Code', Menlo, monospace; }
    .btn-hover { transition: opacity 0.2s ease, transform 0.2s ease; cursor: pointer; }
    .btn-hover:hover { opacity: 0.85; }
"""


def render_modern_defs(
    grad_id: Any = "modernGrad",
    prim: Any = "#38BDF8",
    acc: Any = "#818CF8",
    tert: Any = None,
    add_glow: bool = False,
    glow_id: str = "softGlow",
) -> str:
    """
    Renders SVG <defs> elements for modern linear gradients and subtle glow effects.
    Supports both:
      render_modern_defs("myGradId", prim, acc, tert)
      render_modern_defs(c, "myPrefix")
    """
    if isinstance(grad_id, dict):
        c = grad_id
        prefix = str(prim) if prim and isinstance(prim, str) else "modern"
        p = c.get("primary", "#38BDF8")
        a = c.get("accent", "#818CF8")
        b = c.get("border", "#334155")
        return f"""    <linearGradient id="{prefix}-accent-grad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{p}" />
      <stop offset="100%" stop-color="{a}" />
    </linearGradient>
    <linearGradient id="{prefix}-border-grad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{p}" stop-opacity="0.6" />
      <stop offset="100%" stop-color="{b}" stop-opacity="0.3" />
    </linearGradient>"""

    grad_markup = f"""    <linearGradient id="{grad_id}" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{prim}" />
      <stop offset="100%" stop-color="{acc}" />
    </linearGradient>"""

    glow_markup = ""
    if add_glow:
        glow_markup = f"""
    <filter id="{glow_id}" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>"""

    return f"{grad_markup}{glow_markup}"


SKETCH_BASE_STYLES = """
    .font-sketch { font-family: 'Virgil', 'Architects Daughter', 'Comic Shanns', 'Kalam', 'Chalkboard SE', 'Comic Sans MS', 'Casual', cursive, sans-serif; }
    .font-sketch-mono { font-family: 'SF Mono', 'JetBrains Mono', 'Fira Code', Menlo, monospace; }
    .sketch-hover { transition: opacity 0.2s ease, transform 0.2s ease; cursor: pointer; }
    .sketch-hover:hover { opacity: 0.85; transform: scale(1.01); }
"""


def coord_jitter(x: float, y: float, seed: int = 42, magnitude: float = 1.2) -> float:
    """Deterministic coordinate jitter based on position and seed."""
    n = int(abs(x) * 37.13 + abs(y) * 101.41 + (seed + 1) * 197.89) & 0xFFFF
    normalized = ((n % 1000) / 500.0) - 1.0
    return round(normalized * magnitude, 2)


def render_rough_line(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    stroke: str,
    stroke_width: float = 1.5,
    jitter: float = 1.2,
    double_stroke: bool = True,
    seed: int = 0,
    opacity: float = 1.0,
    extra_cls: str = "",
) -> str:
    """
    Renders deterministic hand-drawn SVG strokes between (x1, y1) and (x2, y2).
    Simulates rough hand drawing with slight curve deflection and optional double stroke.
    """
    mx = (x1 + x2) / 2.0
    my = (y1 + y2) / 2.0
    j1x = coord_jitter(x1, y1, seed + 1, jitter)
    j1y = coord_jitter(x1, y1, seed + 2, jitter)
    j2x = coord_jitter(x2, y2, seed + 3, jitter)
    j2y = coord_jitter(x2, y2, seed + 4, jitter)
    jmx = coord_jitter(mx, my, seed + 5, jitter * 1.5)
    jmy = coord_jitter(mx, my, seed + 6, jitter * 1.5)

    sx1, sy1 = round(x1 + j1x, 2), round(y1 + j1y, 2)
    sx2, sy2 = round(x2 + j2x, 2), round(y2 + j2y, 2)
    cx, cy = round(mx + jmx, 2), round(my + jmy, 2)

    cls_attr = f' class="{extra_cls}"' if extra_cls else ""
    p1 = f'<path d="M {sx1} {sy1} Q {cx} {cy} {sx2} {sy2}" stroke="{stroke}" stroke-width="{stroke_width}" stroke-linecap="round" fill="none" opacity="{opacity}"{cls_attr} />'

    if not double_stroke:
        return p1

    j3x = coord_jitter(x1, y1, seed + 7, jitter * 0.8)
    j3y = coord_jitter(x1, y1, seed + 8, jitter * 0.8)
    j4x = coord_jitter(x2, y2, seed + 9, jitter * 0.8)
    j4y = coord_jitter(x2, y2, seed + 10, jitter * 0.8)
    jmx2 = coord_jitter(mx, my, seed + 11, jitter * -1.2)
    jmy2 = coord_jitter(mx, my, seed + 12, jitter * -1.2)

    sx3, sy3 = round(x1 + j3x, 2), round(y1 + j3y, 2)
    sx4, sy4 = round(x2 + j4x, 2), round(y2 + j4y, 2)
    cx2, cy2 = round(mx + jmx2, 2), round(my + jmy2, 2)

    p2 = f'<path d="M {sx3} {sy3} Q {cx2} {cy2} {sx4} {sy4}" stroke="{stroke}" stroke-width="{round(stroke_width * 0.85, 2)}" stroke-linecap="round" fill="none" opacity="{round(opacity * 0.75, 2)}"{cls_attr} />'
    return f"{p1}\n    {p2}"


def render_rough_rect(
    x: float,
    y: float,
    w: float,
    h: float,
    stroke: str,
    stroke_width: float = 1.5,
    fill: str = "none",
    jitter: float = 1.2,
    overshoot: float = 3.0,
    rx: float = 4.0,
    seed: int = 0,
    fill_opacity: float = 1.0,
) -> str:
    """
    Renders a hand-drawn rough rectangle with corner overshoot lines and optional fill.
    """
    parts = []
    if fill != "none":
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" fill-opacity="{fill_opacity}" />')

    top = render_rough_line(x - overshoot, y, x + w + overshoot, y, stroke, stroke_width, jitter, True, seed + 10)
    right = render_rough_line(x + w, y - overshoot, x + w, y + h + overshoot, stroke, stroke_width, jitter, True, seed + 20)
    bottom = render_rough_line(x + w + overshoot, y + h, x - overshoot, y + h, stroke, stroke_width, jitter, True, seed + 30)
    left = render_rough_line(x, y + h + overshoot, x, y - overshoot, stroke, stroke_width, jitter, True, seed + 40)

    parts.extend([top, right, bottom, left])
    return "\n    ".join(parts)


def render_rough_arrow(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    stroke: str,
    stroke_width: float = 1.5,
    arrow_size: float = 8.0,
    seed: int = 0,
) -> str:
    """Renders a rough arrow line with a two-barb hand-drawn arrowhead pointing to (x2, y2)."""
    import math
    shaft = render_rough_line(x1, y1, x2, y2, stroke, stroke_width, jitter=1.2, double_stroke=True, seed=seed)
    angle = math.atan2(y2 - y1, x2 - x1)
    barb1_angle = angle + math.pi * 0.82
    barb2_angle = angle - math.pi * 0.82

    bx1 = x2 + arrow_size * math.cos(barb1_angle)
    by1 = y2 + arrow_size * math.sin(barb1_angle)
    bx2 = x2 + arrow_size * math.cos(barb2_angle)
    by2 = y2 + arrow_size * math.sin(barb2_angle)

    barb1 = render_rough_line(x2, y2, bx1, by1, stroke, stroke_width, jitter=0.8, double_stroke=False, seed=seed + 50)
    barb2 = render_rough_line(x2, y2, bx2, by2, stroke, stroke_width, jitter=0.8, double_stroke=False, seed=seed + 60)
    return f"{shaft}\n    {barb1}\n    {barb2}"


def render_rough_star(
    cx: float,
    cy: float,
    r: float = 6.0,
    fill: str = "none",
    stroke: str = "#FDE047",
    stroke_width: float = 1.5,
    seed: int = 0,
    size: Optional[float] = None,
) -> str:
    """Renders a 5-pointed doodle star drawn as a continuous hand-drawn path."""
    import math
    if size is not None:
        r = size
    points = []
    order = [0, 2, 4, 1, 3, 0]
    for idx, i in enumerate(order):
        angle = -math.pi / 2 + (i * 2 * math.pi / 5)
        px = cx + r * math.cos(angle) + coord_jitter(cx + idx, cy, seed + idx, 0.7)
        py = cy + r * math.sin(angle) + coord_jitter(cx, cy + idx, seed + idx * 2, 0.7)
        points.append(f"{round(px, 1)},{round(py, 1)}")

    d_str = "M " + " L ".join(points)
    fill_attr = f' fill="{fill}"' if fill != "none" else ' fill="none"'
    return f'<path d="{d_str}" stroke="{stroke}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"{fill_attr} />'


def render_rough_circle(
    cx: float,
    cy: float,
    r: float = 4.0,
    stroke: str = "#A78BFA",
    stroke_width: float = 1.2,
    fill: str = "none",
    seed: int = 0,
) -> str:
    """Renders a hand-drawn circle / node marker with slight organic wobble and overlap."""
    import math
    steps = 8
    points = []
    for i in range(steps + 1):
        angle = (i * 2 * math.pi / steps)
        j_rad = coord_jitter(cx + i * 3, cy + i * 5, seed + i, magnitude=min(1.5, 0.35 * r))
        cur_r = max(1.0, r + j_rad)
        px = cx + cur_r * math.cos(angle)
        py = cy + cur_r * math.sin(angle)
        points.append((round(px, 1), round(py, 1)))

    # Extra slight overlap stroke at the end
    end_angle = 2 * math.pi + 0.35
    end_px = cx + r * math.cos(end_angle) + coord_jitter(cx, cy, seed + 15, 0.4)
    end_py = cy + r * math.sin(end_angle) + coord_jitter(cx, cy, seed + 16, 0.4)
    points.append((round(end_px, 1), round(end_py, 1)))

    d_parts = [f"M {points[0][0]} {points[0][1]}"]
    for i in range(1, len(points)):
        p_prev = points[i - 1]
        p_cur = points[i]
        mx = (p_prev[0] + p_cur[0]) / 2.0
        my = (p_prev[1] + p_cur[1]) / 2.0
        d_parts.append(f"Q {mx} {my} {p_cur[0]} {p_cur[1]}")

    d_str = " ".join(d_parts)
    fill_attr = f' fill="{fill}"' if fill != "none" else ' fill="none"'
    return f'<path d="{d_str}" stroke="{stroke}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"{fill_attr} />'


def render_sketch_defs(
    theme_or_id: Any = "sketch",
    prefix: str = "sketch",
    prim: str = "#A78BFA",
    stroke: str = "#E0E0E0",
) -> str:
    """
    Renders SVG <defs> elements for Sketch style:
    - 45° angled pencil hatch pattern
    - Cross-hatch pattern
    - Semi-transparent washi tape fill
    """
    if isinstance(theme_or_id, dict):
        c = theme_or_id
        pref = str(prefix) if prefix and isinstance(prefix, str) else "sketch"
        p = c.get("primary", "#A78BFA")
        a = c.get("accent", "#6EE7B7")
        s = c.get("border", "#E0E0E0")
        t = c.get("tertiary", "#FDE047")
    else:
        pref = str(prefix) if prefix else "sketch"
        p = prim
        a = "#6EE7B7"
        s = stroke
        t = "#FDE047"

    return f"""    <pattern id="{pref}-hatch" width="10" height="10" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">
      <line x1="0" y1="0" x2="0" y2="10" stroke="{p}" stroke-width="1.3" opacity="0.45" />
    </pattern>
    <pattern id="{pref}-crosshatch" width="12" height="12" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">
      <line x1="0" y1="0" x2="0" y2="12" stroke="{a}" stroke-width="1.2" opacity="0.4" />
      <line x1="0" y1="0" x2="12" y2="0" stroke="{a}" stroke-width="1.2" opacity="0.4" />
    </pattern>
    <pattern id="{pref}-hatch-accent" width="10" height="10" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">
      <line x1="0" y1="0" x2="0" y2="10" stroke="{a}" stroke-width="1.3" opacity="0.5" />
    </pattern>
    <linearGradient id="{pref}-tape" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#ffffff" stop-opacity="0.35" />
      <stop offset="100%" stop-color="#fef08a" stop-opacity="0.25" />
    </linearGradient>"""


