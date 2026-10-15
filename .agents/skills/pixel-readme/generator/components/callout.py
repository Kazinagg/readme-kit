"""Callout and GitHub alert components for Pixel Readme Kit."""
from typing import Optional, Any
from generator.themes import resolve_theme, normalize_style_and_theme
from generator.layout import (
    measure_mono_text_width,
    clamp_text_to_width,
    wrap_text_to_lines,
    measure_sans_text_width,
    clamp_sans_text_to_width,
    wrap_sans_text_to_lines,
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

GITHUB_ALERT_COLORS = {
    "NOTE": "#2f81f7",
    "TIP": "#238636",
    "IMPORTANT": "#8957e5",
    "WARNING": "#d29922",
    "CAUTION": "#f85149",
    "CRITICAL": "#f85149",
    "SUCCESS": "#238636",
    "INFO": "#8957e5",
}


def _generate_modern_callout(style_name, theme_name, c, css_vars,
                             callout_type="note", title="SYSTEM SPECIFICATION",
                             subtitle=None, is_quote=False, width=850, height=None,
                             badge_col="#38BDF8"):
    """Renders modern SaaS-style alert card with rounded corners and vertical accent bar."""
    bg = c["bg"]
    border = c["border"]
    panel = c["panel"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]

    title_clean = escape_xml(title)
    sub_raw = str(subtitle).strip() if subtitle else ""
    c_type_upper = str(callout_type).strip().upper() if callout_type else "NOTE"

    bw = max(70, min(140, int(measure_sans_text_width(c_type_upper, 10) + 24)))
    text_x = 18 + bw + 14
    avail_w = max(100, width - text_x - 24)

    title_disp = clamp_sans_text_to_width(title_clean, avail_w, 12)
    sub_lines = wrap_sans_text_to_lines(sub_raw, avail_w, 11, max_lines=2) if sub_raw else []

    if sub_lines:
        def_h = 68 if len(sub_lines) > 1 else 52
    else:
        def_h = 44
    h = height if height else def_h

    if not sub_lines:
        y_title = h // 2 + 4
        y_badge = (h - 22) // 2
    else:
        y_badge = 14
        y_title = 26

    sub_markup = ""
    if sub_lines:
        y_sub_start = 44
        lines_svg = []
        for i, sl in enumerate(sub_lines):
            lines_svg.append(f'<text x="{text_x}" y="{y_sub_start + i * 16}" fill="{text_dim}" font-size="11" font-weight="400" class="font-sans">{escape_xml(sl)}</text>')
        sub_markup = "\n  ".join(lines_svg)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%">
  <defs>
    <style>
      {css_vars}
{MODERN_BASE_STYLES}
    </style>
  </defs>

  <!-- Modern Card with rounded corners and left vertical accent pill -->
  <rect x="2" y="2" width="{width-4}" height="{h-4}" rx="10" fill="{bg}" stroke="{border}" stroke-width="1.2"/>
  <rect x="4" y="6" width="4" height="{h-12}" rx="2" fill="{badge_col}"/>

  <!-- Type Pill Badge -->
  <g transform="translate(18, {y_badge})">
    <rect x="0" y="0" width="{bw}" height="22" rx="11" fill="{panel}" stroke="{badge_col}" stroke-width="1"/>
    <text x="{bw//2}" y="15" fill="{badge_col}" font-size="10" font-weight="600" text-anchor="middle" class="font-sans">{escape_xml(c_type_upper)}</text>
  </g>

  <!-- Title & Subtitle -->
  <text x="{text_x}" y="{y_title}" fill="{text_main}" font-size="12" font-weight="600" class="font-sans">{title_disp}</text>
  {sub_markup}
</svg>"""

    validate_svg(svg)
    return svg


def _generate_sketch_callout(style_name, theme_name, c, css_vars,
                             callout_type="note", title="SYSTEM SPECIFICATION",
                             subtitle=None, is_quote=False, width=850, height=None,
                             badge_col="#38BDF8"):
    """Renders hand-drawn sketch callout / sticky note with washi tape and doodle badge."""
    bg = c["bg"]
    border = c["border"]
    panel = c["panel"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]
    tertiary_col = c.get("tertiary", "#FDE047")

    title_clean = escape_xml(title)
    sub_raw = str(subtitle).strip() if subtitle else ""
    c_type_upper = str(callout_type).strip().upper() if callout_type else "NOTE"

    bw = max(70, min(140, int(measure_sans_text_width(c_type_upper, 10) + 26)))
    text_x = 22 + bw + 14
    avail_w = max(100, width - text_x - 24)

    title_disp = clamp_sans_text_to_width(title_clean, avail_w, 12)
    sub_lines = wrap_sans_text_to_lines(sub_raw, avail_w, 11, max_lines=2) if sub_raw else []

    if sub_lines:
        def_h = 70 if len(sub_lines) > 1 else 54
    else:
        def_h = 46
    h = height if height else def_h

    if not sub_lines:
        y_title = h // 2 + 4
        y_badge = (h - 22) // 2
    else:
        y_badge = 14
        y_title = 26

    sub_markup = ""
    if sub_lines:
        y_sub_start = 44
        lines_svg = []
        for i, sl in enumerate(sub_lines):
            lines_svg.append(f'<text x="{text_x}" y="{y_sub_start + i * 16}" fill="{text_dim}" font-size="11" class="font-sketch">{escape_xml(sl)}</text>')
        sub_markup = "\n  ".join(lines_svg)

    chassis = render_rough_rect(x=4, y=4, w=width-8, h=h-8, stroke=border, stroke_width=1.4, fill=bg, rx=6, seed=140)
    accent_bar = render_rough_line(12, 8, 12, h-8, stroke=badge_col, stroke_width=3.2, jitter=0.8, double_stroke=False, seed=145)
    badge_box = render_rough_rect(x=22, y=y_badge, w=bw, h=22, stroke=badge_col, stroke_width=1.2, fill=panel, rx=4, seed=150)

    # Optional doodle star for TIP or SUCCESS
    star_markup = ""
    if c_type_upper in ("TIP", "SUCCESS"):
        star_markup = render_rough_star(cx=30, cy=y_badge + 11, r=3.8, fill=badge_col, stroke=badge_col, seed=152)

    quote_prefix = '“ ' if is_quote else ''

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%">
  <defs>
    <style>
      {css_vars}
{SKETCH_BASE_STYLES}
    </style>
{render_sketch_defs(c, "calloutSketch")}
  </defs>

  <!-- Sticky Note Rough Chassis -->
  {chassis}

  <!-- Washi Tape Strip -->
  <polygon points="20 1, 60 1, 52 13, 12 13" fill="url(#calloutSketch-tape)" stroke="{tertiary_col}" stroke-width="0.8" opacity="0.85" />

  <!-- Left Accent Marker Line -->
  {accent_bar}

  <!-- Type Badge -->
  <g>
    {badge_box}
    {star_markup}
    <text x="{22 + bw//2}" y="{y_badge + 15}" fill="{badge_col}" font-size="10" font-weight="600" text-anchor="middle" class="font-sketch">{escape_xml(c_type_upper)}</text>
  </g>

  <!-- Title & Subtitle in Handwriting -->
  <text x="{text_x}" y="{y_title}" fill="{text_main}" font-size="12" font-weight="600" class="font-sketch">{quote_prefix}{title_disp}</text>
  {sub_markup}
</svg>"""

    validate_svg(svg)
    return svg


def generate_callout(style=None, primary=None, accent=None,
                     callout_type="note", title="SYSTEM SPECIFICATION",
                     subtitle="Dual-theme contrast > 7:1 // Monospace typography",
                     is_quote=False, width=850, height=None, mode="auto", preset=None,
                     badge_color=None, tertiary=None, theme=None):
    style_name, theme_name = normalize_style_and_theme(style=style, theme=theme)
    c, css_vars = resolve_theme(style=style_name, theme=theme_name, mode=mode, primary=primary, accent=accent, preset=preset, tertiary=tertiary)
    prim = c["primary"]
    acc = c["accent"]
    bg = c["bg"]
    border = c["border"]
    panel = c["panel"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]

    c_type_upper = str(callout_type).strip().upper() if callout_type else "NOTE"
    if badge_color:
        b_str = str(badge_color).strip()
        if b_str.startswith("#"):
            badge_col = b_str
        elif b_str.lower() == "theme":
            badge_col = prim
        elif b_str.upper() in GITHUB_ALERT_COLORS:
            badge_col = GITHUB_ALERT_COLORS[b_str.upper()]
        else:
            badge_col = b_str
    elif primary is not None:
        badge_col = prim
    else:
        badge_col = GITHUB_ALERT_COLORS.get(c_type_upper, prim)

    if style_name == "modern":
        return _generate_modern_callout(
            style_name=style_name, theme_name=theme_name, c=c, css_vars=css_vars,
            callout_type=callout_type, title=title, subtitle=subtitle, is_quote=is_quote,
            width=width, height=height, badge_col=badge_col
        )
    elif style_name == "sketch":
        return _generate_sketch_callout(
            style_name=style_name, theme_name=theme_name, c=c, css_vars=css_vars,
            callout_type=callout_type, title=title, subtitle=subtitle, is_quote=is_quote,
            width=width, height=height, badge_col=badge_col
        )


    title_clean = escape_xml(title)
    sub_raw = str(subtitle).strip() if subtitle else ""
    tag_clean = escape_xml(callout_type.upper())
    if theme_name in ("tactical", "amber", "amber_crt") or style_name == "tactical":
        st = "tactical"
    elif theme_name in ("minimal", "clean-mono", "clean_mono", "academic-paper", "academic_paper", "corporate-blue", "corporate_blue", "tokyo", "tokyo_night", "swiss-mono", "swiss_mono", "executive-slate", "executive_slate") or style_name == "minimal":
        st = "minimal"
    else:
        st = "cyberpunk"
    has_sub = bool(sub_raw)

    if is_quote:
        if st == "tactical":
            dash_w = "8,4"
            tag_str = f"▲ {tag_clean} // HAZARD"
            bw = max(144, int(measure_mono_text_width(tag_str, 10) + 24))
            badge = f'<polygon points="6 6, 12 6, 4 18, 0 18" fill="{badge_col}" opacity="0.6"/><polygon points="16 6, 22 6, 14 18, 8 18" fill="{badge_col}" opacity="0.6"/><polygon points="28 8, {28+bw-7} 8, {28+bw} 15, {28+bw} 27, {28+bw-7} 34, 28 34" fill="{panel}" stroke="{badge_col}" stroke-width="1.5"/><text x="{28 + bw//2}" y="24" fill="{badge_col}" font-size="10" font-weight="bold" text-anchor="middle" class="font-mono">{tag_str}</text>'
            text_x = 28 + bw + 14
        elif st == "minimal":
            dash_w = "5,4"
            tag_str = f"{tag_clean} // MINIMAL"
            bw = max(115, int(measure_mono_text_width(tag_str, 9.5) + 20))
            badge = f'<rect x="8" y="8" width="{bw}" height="24" fill="{panel}" stroke="{badge_col}" stroke-width="1"/><text x="{8 + bw//2}" y="23" fill="{badge_col}" font-size="9.5" font-weight="bold" text-anchor="middle" class="font-mono">{tag_str}</text>'
            text_x = 8 + bw + 14
        else:
            dash_w = "6,4"
            tag_str = f"{tag_clean} // 0x01"
            bw = max(120, int(measure_mono_text_width(tag_str, 10) + 32))
            badge = f'<rect x="8" y="8" width="{bw}" height="24" fill="{panel}" stroke="{badge_col}" stroke-width="1.5"/><circle cx="20" cy="20" r="3.5" fill="{badge_col}"/><text x="{20 + (bw-12)//2}" y="24" fill="{badge_col}" font-size="10" font-weight="bold" text-anchor="middle" class="font-mono">{tag_str}</text>'
            text_x = 8 + bw + 14

        avail_w = max(100, width - text_x - 20)
        title_disp = clamp_text_to_width(title_clean, avail_w, 11)
        sub_lines = wrap_text_to_lines(sub_raw, avail_w, 11, max_lines=2) if has_sub else []

        def_h = 56 if len(sub_lines) > 1 else 42
        h = height if height else def_h

        if st == "tactical":
            top_rail = f'<line x1="0" y1="2" x2="{width-12}" y2="2" stroke="{prim}" stroke-width="2"/><line x1="{width-12}" y1="2" x2="{width-1}" y2="13" stroke="{prim}" stroke-width="2"/><line x1="{width-1}" y1="13" x2="{width-1}" y2="{h-4}" stroke="{prim}" stroke-width="2"/>'
            arrow_poly = f'<polygon points="{width-10} {h-5}, {width-2} {h-5}, {width-6} {h-1}" fill="{prim}"/>'
            bg_elem = f'<polygon points="0 0, {width-12} 0, {width-1} 12, {width-1} {h}, 0 {h}" fill="{bg}"/>'
        elif st == "minimal":
            top_rail = f'<line x1="0" y1="2" x2="{width-1}" y2="2" stroke="{border}" stroke-width="1.5"/><path d="M {width-1} 2 L {width-1} 14" fill="none" stroke="{border}" stroke-width="1.5"/><rect x="{width-4}" y="2" width="4" height="4" fill="{acc}"/>'
            arrow_poly = ""
            bg_elem = f'<rect x="0" y="0" width="{width}" height="{h}" fill="{bg}"/>'
        else:
            top_rail = f'<line x1="0" y1="2" x2="{width-1}" y2="2" stroke="{prim}" stroke-width="2"/><line x1="{width-1}" y1="2" x2="{width-1}" y2="{h-4}" stroke="{prim}" stroke-width="2"/><rect x="{width-6}" y="2" width="5" height="5" fill="{prim}"/>'
            arrow_poly = ""
            bg_elem = f'<rect x="0" y="0" width="{width}" height="{h}" fill="{bg}"/>'

        rail_bottom_col = prim if st != "minimal" else border

        if not has_sub:
            text_block = f'<text x="{text_x}" y="25" fill="{text_main}" font-size="11" font-weight="bold" letter-spacing="0.5" class="font-mono">{title_disp}</text>'
        elif len(sub_lines) == 1:
            text_block = f"""<text x="{text_x}" y="20" fill="{text_main}" font-size="11" font-weight="bold" letter-spacing="0.5" class="font-mono">{title_disp}</text>
  <text x="{text_x}" y="33" fill="{acc}" font-size="11" class="font-mono">{escape_xml(sub_lines[0])}</text>"""
        else:
            text_block = f"""<text x="{text_x}" y="19" fill="{text_main}" font-size="11" font-weight="bold" letter-spacing="0.5" class="font-mono">{title_disp}</text>
  <text x="{text_x}" y="32" fill="{acc}" font-size="11" class="font-mono">{escape_xml(sub_lines[0])}</text>
  <text x="{text_x}" y="45" fill="{acc}" font-size="11" class="font-mono">{escape_xml(sub_lines[1])}</text>"""

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
    </style>
  </defs>
  <!-- Background Glass (Flush left to connect with markdown quote border) -->
  {bg_elem}
  <!-- Top Rail -->
  {top_rail}
  <!-- Badge -->
  {badge}
  <!-- Title & Subtitle (Properly offset past badge edge) -->
  {text_block}
  <!-- DASHED BOTTOM LINE: Bridges into live markdown text -->
  <line x1="0" y1="{h-1}" x2="{width-5}" y2="{h-1}" stroke="{rail_bottom_col}" stroke-width="1.5" stroke-dasharray="{dash_w}" opacity="0.75"/>
  {arrow_poly}
</svg>"""

    else:
        # Autonomous Closed Callout (48px or 62px)
        if st == "tactical":
            tag_str = f"▲ {tag_clean} // HAZARD"
            bw = max(148, int(measure_mono_text_width(tag_str, 11) + 24))
            badge = f'<polygon points="34 10, {34+bw-7} 10, {34+bw} 17, {34+bw} 31, {34+bw-7} 38, 34 38" fill="{panel}" stroke="{badge_col}" stroke-width="1.5"/><text x="{34 + bw//2}" y="28" fill="{badge_col}" font-size="11" font-weight="bold" text-anchor="middle" class="font-mono">{tag_str}</text>'
            text_x = 34 + bw + 14
        elif st == "minimal":
            tag_str = f"{tag_clean} // MINIMAL"
            bw = max(130, int(measure_mono_text_width(tag_str, 11) + 20))
            badge = f'<rect x="16" y="11" width="{bw}" height="26" fill="{panel}" stroke="{badge_col}" stroke-width="1"/><text x="{16 + bw//2}" y="28" fill="{badge_col}" font-size="11" font-weight="bold" text-anchor="middle" class="font-mono">{tag_str}</text>'
            text_x = 16 + bw + 14
        else:
            tag_str = f"{tag_clean} // 0x01"
            bw = max(140, int(measure_mono_text_width(tag_str, 11) + 36))
            badge = f'<rect x="14" y="10" width="{bw}" height="28" fill="{panel}" stroke="{badge_col}" stroke-width="1.5"/><circle cx="26" cy="24" r="3.5" fill="{badge_col}"/><text x="{26 + (bw-12)//2}" y="28" fill="{badge_col}" font-size="11" font-weight="bold" text-anchor="middle" class="font-mono">{tag_str}</text>'
            text_x = 14 + bw + 14

        avail_w = max(100, width - text_x - 45)
        title_disp = clamp_text_to_width(title_clean, avail_w, 11)
        sub_lines = wrap_text_to_lines(sub_raw, avail_w, 11, max_lines=2) if has_sub else []

        def_h = 62 if len(sub_lines) > 1 else 48
        h = height if height else def_h
        mid_y = h // 2

        if st == "tactical":
            body = f'<polygon points="12 2, {width-12} 2, {width-2} 12, {width-2} {h-12}, {width-12} {h-2}, 12 {h-2}, 2 {h-12}, 2 12" fill="{bg}" stroke="{prim}" stroke-width="1.5"/>'
            accents = f'<polygon points="10 8, 16 8, 8 20, 2 20" fill="{prim}" opacity="0.6"/><polygon points="20 8, 26 8, 18 20, 12 20" fill="{prim}" opacity="0.6"/><circle cx="{width-25}" cy="{mid_y}" r="8" fill="none" stroke="{prim}" stroke-width="1.5"/><polygon points="{width-28} {mid_y}, {width-22} {mid_y-4}, {width-22} {mid_y+4}" fill="{prim}"/>'
        elif st == "minimal":
            body = f'<rect x="1" y="2" width="{width-2}" height="{h-4}" fill="{bg}" stroke="{border}" stroke-width="1.5"/>'
            accents = f'<path d="M 5 12 L 5 5 L 14 5" fill="none" stroke="{prim}" stroke-width="1.5"/><path d="M {width-5} 12 L {width-5} 5 L {width-14} 5" fill="none" stroke="{prim}" stroke-width="1.5"/>'
        else:
            body = f'<rect x="2" y="2" width="{width-4}" height="{h-4}" fill="{bg}" stroke="{prim}" stroke-width="1.5"/><rect x="2" y="2" width="5" height="5" fill="{prim}"/><rect x="{width-7}" y="2" width="5" height="5" fill="{prim}"/><rect x="2" y="{h-7}" width="5" height="5" fill="{prim}"/><rect x="{width-7}" y="{h-7}" width="5" height="5" fill="{prim}"/>'
            accents = f'<rect x="{width-35}" y="{mid_y - 10}" width="20" height="20" fill="{panel}" stroke="{border}"/><text x="{width-25}" y="{mid_y + 4}" fill="{prim}" font-size="11" font-weight="bold" text-anchor="middle" class="font-mono">ℹ</text>'

        if not has_sub:
            text_block = f'<text x="{text_x}" y="28" fill="{text_main}" font-size="11" font-weight="bold" letter-spacing="0.5" class="font-mono">{title_disp}</text>'
        elif len(sub_lines) == 1:
            text_block = f"""<text x="{text_x}" y="22" fill="{text_main}" font-size="11" font-weight="bold" letter-spacing="0.5" class="font-mono">{title_disp}</text>
  <text x="{text_x}" y="36" fill="{acc}" font-size="11" class="font-mono">{escape_xml(sub_lines[0])}</text>"""
        else:
            text_block = f"""<text x="{text_x}" y="20" fill="{text_main}" font-size="11" font-weight="bold" letter-spacing="0.5" class="font-mono">{title_disp}</text>
  <text x="{text_x}" y="34" fill="{acc}" font-size="11" class="font-mono">{escape_xml(sub_lines[0])}</text>
  <text x="{text_x}" y="48" fill="{acc}" font-size="11" class="font-mono">{escape_xml(sub_lines[1])}</text>"""

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
    </style>
  </defs>
  <!-- Body Chassis -->
  {body}
  <!-- Badges & Accents -->
  {badge}
  {accents}
  <!-- Text Content (Properly offset past badge edge) -->
  {text_block}
</svg>"""

    validate_svg(svg)
    return svg


