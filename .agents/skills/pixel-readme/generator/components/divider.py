"""Divider and splitter components for Pixel Readme Kit."""
from typing import Optional, Any
from generator.themes import resolve_theme, normalize_style_and_theme
from generator.layout import (
    measure_mono_text_width,
    clamp_text_to_width,
    measure_sans_text_width,
    clamp_sans_text_to_width,
)
from generator.components.base import (
    escape_xml,
    validate_svg,
    MODERN_BASE_STYLES,
    SKETCH_BASE_STYLES,
    render_sketch_defs,
    render_rough_line,
    render_rough_rect,
    render_rough_star,
)


def _generate_modern_divider(style_name, theme_name, c, css_vars, width=850, height=28):
    """Renders sleek vector gradient divider with center diamond."""
    prim = c["primary"]
    acc = c["accent"]
    tertiary_col = c["tertiary"]
    cy = height // 2

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">
  <defs>
    <style>
      {css_vars}
{MODERN_BASE_STYLES}
    </style>
    <linearGradient id="modernDivGrad" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{prim}" stop-opacity="0"/>
      <stop offset="35%" stop-color="{prim}" stop-opacity="0.8"/>
      <stop offset="50%" stop-color="{acc}" stop-opacity="1"/>
      <stop offset="65%" stop-color="{prim}" stop-opacity="0.8"/>
      <stop offset="100%" stop-color="{acc}" stop-opacity="0"/>
    </linearGradient>
  </defs>

  <!-- Smooth Gradient Vector Line -->
  <line x1="24" y1="{cy}" x2="{width-24}" y2="{cy}" stroke="url(#modernDivGrad)" stroke-width="1.5" stroke-linecap="round"/>

  <!-- Center Accent Geometry -->
  <circle cx="{width//2}" cy="{cy}" r="4" fill="{acc}"/>
  <circle cx="{width//2}" cy="{cy}" r="7" fill="none" stroke="{prim}" stroke-width="1" opacity="0.6"/>
</svg>"""

    validate_svg(svg)
    return svg


def _generate_modern_splitter(style_name, theme_name, c, css_vars,
                              label="[MODULE: SUB_SYSTEM]", width=850, height=22):
    """Renders modern sub-block splitter with centered pill badge."""
    prim = c["primary"]
    acc = c["accent"]
    bg = c["bg"]
    border = c["border"]
    panel = c["panel"]
    text_main = c["text_main"]

    lbl_clean = escape_xml(str(label).strip().strip("[]"))
    mid_x = width // 2
    max_lbl_w = width - 80
    lbl_disp = clamp_sans_text_to_width(lbl_clean, max_lbl_w - 40, 10)
    text_w = measure_sans_text_width(lbl_disp, 10) + 36
    box_w = max(100, min(max_lbl_w, int(text_w)))
    x1 = mid_x - box_w // 2
    x2 = mid_x + box_w // 2
    l_end = max(10, x1 - 12)
    r_start = min(width - 10, x2 + 12)
    cy = height // 2

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">
  <defs>
    <style>
      {css_vars}
{MODERN_BASE_STYLES}
    </style>
  </defs>

  <!-- Subtle Connecting 1px Line -->
  <line x1="12" y1="{cy}" x2="{l_end}" y2="{cy}" stroke="{border}" stroke-width="1"/>
  <line x1="{r_start}" y1="{cy}" x2="{width-12}" y2="{cy}" stroke="{border}" stroke-width="1"/>

  <!-- Center Pill Badge -->
  <g transform="translate({x1}, {(height-20)//2})">
    <rect x="0" y="0" width="{box_w}" height="20" rx="10" fill="{panel}" stroke="{border}" stroke-width="1"/>
    <circle cx="10" cy="10" r="2.5" fill="{prim}"/>
    <text x="{box_w//2 + 4}" y="14" fill="{text_main}" font-size="10" font-weight="600" text-anchor="middle" class="font-sans">{lbl_disp}</text>
  </g>
</svg>"""

    validate_svg(svg)
    return svg


def _generate_sketch_divider(style_name, theme_name, c, css_vars, width=850, height=28):
    """Renders hand-drawn sketch divider with wobbly double stroke and doodle star."""
    prim = c["primary"]
    acc = c["accent"]
    tertiary_col = c.get("tertiary", "#FDE047")
    border = c["border"]
    cy = height // 2

    # Double rough pencil line across
    line_markup = render_rough_line(x1=24, y1=cy, x2=width-24, y2=cy, stroke=prim, stroke_width=1.5, jitter=1.3, double_stroke=True, seed=160)
    center_star = render_rough_star(cx=width//2, cy=cy, r=6.5, fill=acc, stroke=tertiary_col, stroke_width=1.3, seed=165)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">
  <defs>
    <style>
      {css_vars}
{SKETCH_BASE_STYLES}
    </style>
{render_sketch_defs(c, "dividerSketch")}
  </defs>

  <!-- Wobbly Sketch Divider Stroke -->
  {line_markup}

  <!-- Center Doodle Star -->
  <circle cx="{width//2}" cy="{cy}" r="11" fill="none" stroke="{border}" stroke-width="1" stroke-dasharray="2,3" opacity="0.6"/>
  {center_star}
</svg>"""

    validate_svg(svg)
    return svg


def _generate_sketch_splitter(style_name, theme_name, c, css_vars,
                              label="[MODULE: SUB_SYSTEM]", width=850, height=22):
    """Renders hand-drawn sketch splitter with rough lines and centered doodle tag."""
    prim = c["primary"]
    acc = c["accent"]
    bg = c["bg"]
    border = c["border"]
    panel = c["panel"]
    text_main = c["text_main"]

    lbl_clean = escape_xml(str(label).strip().strip("[]"))
    mid_x = width // 2
    max_lbl_w = width - 80
    lbl_disp = clamp_sans_text_to_width(lbl_clean, max_lbl_w - 40, 10)
    text_w = measure_sans_text_width(lbl_disp, 10) + 38
    box_w = max(110, min(max_lbl_w, int(text_w)))
    x1 = mid_x - box_w // 2
    x2 = mid_x + box_w // 2
    l_end = max(10, x1 - 10)
    r_start = min(width - 10, x2 + 10)
    cy = height // 2

    left_line = render_rough_line(12, cy, l_end, cy, stroke=border, stroke_width=1.3, jitter=0.9, double_stroke=False, seed=170)
    right_line = render_rough_line(r_start, cy, width - 12, cy, stroke=border, stroke_width=1.3, jitter=0.9, double_stroke=False, seed=175)
    box_rect = render_rough_rect(x1, (height - 20) // 2, box_w, 20, stroke=acc, stroke_width=1.2, fill=panel, rx=6, seed=180)
    doodle_icon = render_rough_star(cx=x1 + 12, cy=cy, r=3.5, fill=prim, stroke=prim, seed=182)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">
  <defs>
    <style>
      {css_vars}
{SKETCH_BASE_STYLES}
    </style>
{render_sketch_defs(c, "splitterSketch")}
  </defs>

  <!-- Side Rough Lines -->
  {left_line}
  {right_line}

  <!-- Center Hand-drawn Tag Box -->
  <g>
    {box_rect}
    {doodle_icon}
    <text x="{x1 + box_w//2 + 5}" y="{cy + 4}" fill="{text_main}" font-size="10" font-weight="600" text-anchor="middle" class="font-sketch">{lbl_disp}</text>
  </g>
</svg>"""

    validate_svg(svg)
    return svg


def generate_divider(style=None, primary=None, accent=None, width=850, height=28, mode="auto", preset=None, tertiary=None, theme=None):
    style_name, theme_name = normalize_style_and_theme(style=style, theme=theme)
    c, css_vars = resolve_theme(style=style_name, theme=theme_name, mode=mode, primary=primary, accent=accent, preset=preset, tertiary=tertiary)
    if style_name == "modern":
        return _generate_modern_divider(style_name=style_name, theme_name=theme_name, c=c, css_vars=css_vars, width=width, height=height)
    elif style_name == "sketch":
        return _generate_sketch_divider(style_name=style_name, theme_name=theme_name, c=c, css_vars=css_vars, width=width, height=height)
    prim = c["primary"]
    acc = c["accent"]
    bg = c["bg"]
    border = c["border"]

    if theme_name in ("tactical", "amber", "amber_crt"):
        st = "tactical"
    elif theme_name in ("minimal", "clean-mono", "clean_mono", "academic-paper", "academic_paper", "corporate-blue", "corporate_blue", "tokyo", "tokyo_night", "swiss-mono", "swiss_mono", "executive-slate", "executive_slate"):
        st = "minimal"
    else:
        st = "cyberpunk"

    if st == "tactical":
        # Pulsing Aiming Laser Divider
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 9px; font-weight: bold; }}
      @keyframes laserPulse {{ 0%, 100% {{ opacity: 0.95; }} 50% {{ opacity: 0.35; }} }}
      .laser {{ animation: laserPulse 1.4s infinite ease-in-out; }}
    </style>
  </defs>
  <line x1="20" y1="14" x2="350" y2="14" stroke="{prim}" stroke-width="1.5"/>
  <line x1="500" y1="14" x2="{width-20}" y2="14" stroke="{prim}" stroke-width="1.5"/>
  <polygon points="12 14, 20 8, 20 20" fill="{prim}"/>
  <polygon points="{width-12} 14, {width-20} 8, {width-20} 20" fill="{prim}"/>
  <polygon points="360 4, 490 4, 498 14, 490 24, 360 24, 352 14" fill="{bg}" stroke="{prim}" stroke-width="1.5"/>
  <text x="425" y="17" fill="{prim}" text-anchor="middle" class="font-mono laser">▲ TACTICAL // LASER ▲</text>
</svg>"""

    elif st == "minimal":
        # Frequency Spectrum Equalizer Divider
        bars = []
        for i in range(15):
            bx = 365 + i * 8
            bh = 6 + (i * 7 % 18)
            by = 14 - bh // 2
            col = prim if i % 2 == 0 else acc
            bars.append(f'<rect x="{bx}" y="{by}" width="4" height="{bh}" fill="{col}" class="s-bar"/>')
        bars_markup = "".join(bars)

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 8px; font-weight: bold; letter-spacing: 1px; }}
      @keyframes barPulse {{ 0%, 100% {{ transform: scaleY(0.4); opacity: 0.5; }} 50% {{ transform: scaleY(1.2); opacity: 1; }} }}
      .s-bar {{ transform-origin: center; animation: barPulse 1.6s infinite ease-in-out; }}
    </style>
  </defs>
  <line x1="20" y1="14" x2="345" y2="14" stroke="{border}" stroke-width="1.5"/>
  <line x1="505" y1="14" x2="{width-20}" y2="14" stroke="{border}" stroke-width="1.5"/>
  <line x1="60" y1="14" x2="330" y2="14" stroke="{prim}" stroke-width="1" opacity="0.6" stroke-dasharray="12,4"/>
  <line x1="520" y1="14" x2="{width-60}" y2="14" stroke="{prim}" stroke-width="1" opacity="0.6" stroke-dasharray="12,4"/>
  <path d="M 20 8 L 20 14 L 32 14" fill="none" stroke="{prim}" stroke-width="1.5"/><rect x="20" y="12" width="4" height="4" fill="{acc}"/>
  <path d="M {width-20} 8 L {width-20} 14 L {width-32} 14" fill="none" stroke="{prim}" stroke-width="1.5"/><rect x="{width-24}" y="12" width="4" height="4" fill="{acc}"/>
  <text x="240" y="11" fill="{prim}" text-anchor="middle" opacity="0.7" class="font-mono">// 44.1 kHz //</text>
  <text x="610" y="11" fill="{prim}" text-anchor="middle" opacity="0.7" class="font-mono">// SPECTRUM_HUD //</text>
  <rect x="355" y="2" width="140" height="24" fill="{bg}" stroke="{border}" stroke-width="1"/>
  {bars_markup}
</svg>"""

    else:
        # Cyberpunk PCB Trace Flow Divider
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 9px; font-weight: bold; letter-spacing: 1px; }}
      @keyframes pcbTrace {{ 0% {{ stroke-dashoffset: 400; }} 100% {{ stroke-dashoffset: 0; }} }}
      .packet {{ stroke-dasharray: 40, 200; animation: pcbTrace 2.8s infinite linear; }}
    </style>
  </defs>
  <line x1="10" y1="14" x2="{width-10}" y2="14" stroke="{border}" stroke-width="2"/>
  <line x1="10" y1="14" x2="{width-10}" y2="14" stroke="{prim}" stroke-width="2" class="packet"/>
  <circle cx="20" cy="14" r="4" fill="{prim}"/><circle cx="{width-20}" cy="14" r="4" fill="{prim}"/>
  <rect x="{width//2 - 90}" y="4" width="180" height="20" fill="{bg}" stroke="{prim}" stroke-width="1.5"/>
  <text x="{width//2}" y="17" fill="{prim}" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">[PCB: DATA_PACKET_FLOW]</text>
</svg>"""

    validate_svg(svg)
    return svg

def generate_splitter(style=None, primary=None, accent=None,
                      label="[MODULE: SUB_SYSTEM]", width=850, height=22, mode="auto", preset=None,
                      tertiary=None, theme=None):
    style_name, theme_name = normalize_style_and_theme(style=style, theme=theme)
    c, css_vars = resolve_theme(style=style_name, theme=theme_name, mode=mode, primary=primary, accent=accent, preset=preset, tertiary=tertiary)
    if style_name == "modern":
        return _generate_modern_splitter(style_name=style_name, theme_name=theme_name, c=c, css_vars=css_vars, label=label, width=width, height=height)
    elif style_name == "sketch":
        return _generate_sketch_splitter(style_name=style_name, theme_name=theme_name, c=c, css_vars=css_vars, label=label, width=width, height=height)
    prim = c["primary"]
    acc = c["accent"]
    bg = c["bg"]
    border = c["border"]
    lbl_clean = escape_xml(label)
    if theme_name in ("tactical", "amber", "amber_crt"):
        st = "tactical"
    elif theme_name in ("minimal", "clean-mono", "clean_mono", "academic-paper", "academic_paper", "corporate-blue", "corporate_blue", "tokyo", "tokyo_night", "swiss-mono", "swiss_mono", "executive-slate", "executive_slate"):
        st = "minimal"
    else:
        st = "cyberpunk"

    mid_x = width // 2
    max_lbl_w = width - 80
    lbl_disp = clamp_text_to_width(lbl_clean, max_lbl_w - 40, 9)
    text_w = measure_mono_text_width(lbl_disp, 9) + 40
    box_w = max(140, min(max_lbl_w, int(text_w)))
    x1 = mid_x - box_w // 2
    x2 = mid_x + box_w // 2
    l_end = max(1, x1 - 10)
    r_start = min(width - 1, x2 + 10)

    if st == "tactical":
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 9px; font-weight: bold; }}
    </style>
  </defs>
  <line x1="1" y1="11" x2="{l_end}" y2="11" stroke="{prim}" stroke-width="1.5"/>
  <line x1="{r_start}" y1="11" x2="{width-1}" y2="11" stroke="{prim}" stroke-width="1.5"/>
  <polygon points="1 11, 8 7, 8 15" fill="{prim}"/>
  <polygon points="{width-1} 11, {width-8} 7, {width-8} 15" fill="{prim}"/>
  <polygon points="{x1} 3, {x2} 3, {x2+6} 11, {x2} 19, {x1} 19, {x1-6} 11" fill="{bg}" stroke="{prim}" stroke-width="1"/>
  <text x="{mid_x}" y="14" fill="{prim}" text-anchor="middle" class="font-mono">▲ {lbl_disp} ▲</text>
</svg>"""

    elif st == "minimal":
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 9px; font-weight: bold; }}
    </style>
  </defs>
  <line x1="1" y1="11" x2="{l_end}" y2="11" stroke="{border}" stroke-width="1"/>
  <line x1="{r_start}" y1="11" x2="{width-1}" y2="11" stroke="{border}" stroke-width="1"/>
  <rect x="{x1}" y="2" width="{box_w}" height="18" fill="{bg}" stroke="{prim}" stroke-width="1"/>
  <text x="{mid_x}" y="14" fill="{prim}" text-anchor="middle" class="font-mono">{lbl_disp}</text>
</svg>"""

    else:
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 9px; font-weight: bold; }}
    </style>
  </defs>
  <line x1="1" y1="11" x2="{l_end}" y2="11" stroke="{prim}" stroke-width="1.5"/>
  <line x1="{r_start}" y1="11" x2="{width-1}" y2="11" stroke="{prim}" stroke-width="1.5"/>
  <rect x="1" y="8" width="6" height="6" fill="{acc}"/>
  <rect x="{width-7}" y="8" width="6" height="6" fill="{acc}"/>
  <rect x="{x1}" y="2" width="{box_w}" height="18" fill="{bg}" stroke="{prim}" stroke-width="1.5"/>
  <rect x="{x1}" y="2" width="4" height="4" fill="{acc}"/>
  <rect x="{x2-4}" y="2" width="4" height="4" fill="{acc}"/>
  <text x="{mid_x}" y="14" fill="{prim}" text-anchor="middle" class="font-mono"><tspan fill="{acc}">//</tspan> {lbl_disp} <tspan fill="{acc}">//</tspan></text>
</svg>"""

    validate_svg(svg)
    return svg

# ==============================================================================
# DATA VISUALIZATION WIDGETS (v4.0)
# ==============================================================================

