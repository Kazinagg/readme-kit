"""Header components for Pixel Readme Kit."""
import html
from typing import Optional, Any
from generator.themes import resolve_theme, normalize_style_and_theme
from generator.layout import (
    measure_mono_text_width,
    clamp_text_to_width,
    normalize_specs,
    format_tag,
    measure_sans_text_width,
    clamp_sans_text_to_width,
)
from generator.components.base import (
    escape_xml,
    validate_svg,
    MODERN_BASE_STYLES,
    render_modern_defs,
    SKETCH_BASE_STYLES,
    render_sketch_defs,
    render_rough_line,
    render_rough_rect,
    render_rough_arrow,
    render_rough_star,
    coord_jitter,
)
from generator.font_engine import render_3d_text



def _generate_modern_compact_header(style_name, theme_name, c, css_vars,
                                     title="PIXEL-KIT", subtitle="CLEAN VECTOR DESIGN SYSTEM",
                                     tag="SYSTEM_ACTIVE", width=850, height=None,
                                     tag_url=None, close_url=None):
    """Renders a modern low-profile vector compact banner (~76px height)."""
    prim = c["primary"]
    acc = c["accent"]
    tertiary_col = c["tertiary"]
    bg = c["bg"]
    panel = c["panel"]
    border = c["border"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]
    success = c["success"]
    h = height if height else 76

    title_clean = escape_xml(title)
    sub_clean = escape_xml(subtitle)
    tag_clean = escape_xml(tag)

    tag_w = min(220, max(110, int(measure_sans_text_width(tag_clean, 11) + 36)))
    tag_x = width - tag_w - 24
    avail_title_w = max(100, tag_x - 64)
    title_disp = clamp_sans_text_to_width(title_clean, avail_title_w, 20)
    sub_disp = clamp_sans_text_to_width(sub_clean, avail_title_w - 20, 11)

    tag_link_open = f'<a href="{escape_xml(tag_url)}" target="_blank" rel="noopener noreferrer" class="btn-hover">' if tag_url else ''
    tag_link_close = '</a>' if tag_url else ''

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%">
  <defs>
    <style>
      {css_vars}
{MODERN_BASE_STYLES}
      @keyframes pulseLiveDot {{
        0%, 100% {{ opacity: 1; transform: scale(1); }}
        50% {{ opacity: 0.35; transform: scale(0.8); }}
      }}
      .live-dot {{ animation: pulseLiveDot 2.2s infinite ease-in-out; }}
    </style>
{render_modern_defs("headerGrad", prim, acc, tertiary_col)}
  </defs>

  <!-- Modern Card Background with rounded corners & top glow highlight -->
  <rect x="2" y="2" width="{width-4}" height="{h-4}" rx="12" fill="{bg}" stroke="{border}" stroke-width="1.2"/>
  <path d="M 16 2 L {width-16} 2" stroke="url(#headerGrad)" stroke-width="1.5" stroke-linecap="round" opacity="0.8"/>

  <!-- Clean Vector Typography -->
  <text x="32" y="34" font-size="20" font-weight="700" fill="url(#headerGrad)" class="font-sans" letter-spacing="-0.3">{title_disp}</text>
  <g transform="translate(32, 52)">
    <circle cx="4" cy="-3" r="3.5" fill="{success}" class="live-dot"/>
    <text x="14" y="0" fill="{text_dim}" font-size="11" font-weight="500" class="font-sans">{sub_disp}</text>
  </g>

  <!-- Modern Pill Tag Badge -->
  {tag_link_open}<g transform="translate({tag_x}, 24)">
    <rect x="0" y="0" width="{tag_w}" height="28" rx="14" fill="{panel}" stroke="{border}" stroke-width="1"/>
    <circle cx="14" cy="14" r="3" fill="{prim}"/>
    <text x="{tag_w//2 + 4}" y="18" fill="{text_main}" font-size="11" font-weight="600" text-anchor="middle" class="font-sans">{tag_clean}</text>
  </g>{tag_link_close}
</svg>"""

    validate_svg(svg)
    return svg


def _generate_modern_header(style_name, theme_name, c, css_vars,
                            title="PIXEL-KIT", subtitle="CLEAN VECTOR DESIGN SYSTEM",
                            specs=None, spec1=None, spec2=None, spec3=None,
                            tag="SYSTEM_ACTIVE", width=850, height=None,
                            tag_url=None, close_url=None):
    """Renders a flagship modern vector banner with clean typography and smooth cards."""
    prim = c["primary"]
    acc = c["accent"]
    tertiary_col = c["tertiary"]
    bg = c["bg"]
    panel = c["panel"]
    border = c["border"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]
    success = c["success"]

    title_clean = escape_xml(title)
    sub_clean = escape_xml(subtitle)
    tag_clean = escape_xml(tag)
    norm_specs = normalize_specs(specs=specs, spec1=spec1, spec2=spec2, spec3=spec3, default_color=None)

    tag_w = min(240, max(120, int(measure_sans_text_width(tag_clean, 12) + 40)))
    tag_x = width - tag_w - 32

    avail_title_w = max(160, tag_x - 70)
    title_disp = clamp_sans_text_to_width(title_clean, avail_title_w, 32)
    sub_disp = clamp_sans_text_to_width(sub_clean, avail_title_w - 24, 13)

    y_title = 68
    y_sub = 98
    h = height if height else (200 if norm_specs else 160)

    tag_link_open = f'<a href="{escape_xml(tag_url)}" target="_blank" rel="noopener noreferrer" class="btn-hover">' if tag_url else ''
    tag_link_close = '</a>' if tag_url else ''

    specs_svg = []
    if norm_specs:
        cur_x = 36
        spec_y = 132
        for spec in norm_specs[:3]:
            lbl = escape_xml(spec[0])
            val = escape_xml(spec[1])
            val_col = spec[2] if (len(spec) > 2 and spec[2]) else prim
            lbl_w = measure_sans_text_width(lbl, 11)
            val_w = measure_sans_text_width(val, 11)
            pill_w = int(lbl_w + val_w + 32)
            if cur_x + pill_w > width - 36:
                break
            specs_svg.append(f"""    <g transform="translate({cur_x}, {spec_y})">
      <rect x="0" y="0" width="{pill_w}" height="28" rx="14" fill="{panel}" stroke="{border}" stroke-width="1"/>
      <text x="14" y="18" fill="{text_dim}" font-size="11" font-weight="500" class="font-sans">{lbl}:</text>
      <text x="{14 + int(lbl_w) + 6}" y="18" fill="{val_col}" font-size="11" font-weight="600" class="font-sans">{val}</text>
    </g>""")
            cur_x += pill_w + 12

    specs_markup = "\n".join(specs_svg)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%">
  <defs>
    <style>
      {css_vars}
{MODERN_BASE_STYLES}
      @keyframes pulseLiveDot {{
        0%, 100% {{ opacity: 1; transform: scale(1); }}
        50% {{ opacity: 0.35; transform: scale(0.85); }}
      }}
      .live-dot {{ animation: pulseLiveDot 2.2s infinite ease-in-out; }}
    </style>
{render_modern_defs("modernHeaderGrad", prim, acc, tertiary_col)}
  </defs>

  <!-- Modern Card Background with rounded corners & top gradient highlight -->
  <rect x="2" y="2" width="{width-4}" height="{h-4}" rx="16" fill="{bg}" stroke="{border}" stroke-width="1.2"/>
  <path d="M 24 2 L {width-24} 2" stroke="url(#modernHeaderGrad)" stroke-width="2" stroke-linecap="round" opacity="0.9"/>

  <!-- Clean Vector Typography Header -->
  <text x="36" y="{y_title}" font-size="32" font-weight="700" fill="url(#modernHeaderGrad)" class="font-sans" letter-spacing="-0.5">{title_disp}</text>
  
  <!-- Subtitle with Pulse Live Dot -->
  <g transform="translate(36, {y_sub})">
    <circle cx="5" cy="-4" r="4" fill="{success}" class="live-dot"/>
    <text x="18" y="0" fill="{text_dim}" font-size="13" font-weight="500" class="font-sans">{sub_disp}</text>
  </g>

  <!-- Modern Specs Pills -->
{specs_markup}

  <!-- Modern Upper-Right Tag Badge -->
  {tag_link_open}<g transform="translate({tag_x}, 32)">
    <rect x="0" y="0" width="{tag_w}" height="32" rx="16" fill="{panel}" stroke="{border}" stroke-width="1"/>
    <circle cx="16" cy="16" r="3.5" fill="{prim}"/>
    <text x="{tag_w//2 + 6}" y="20" fill="{text_main}" font-size="11" font-weight="600" text-anchor="middle" class="font-sans">{tag_clean}</text>
  </g>{tag_link_close}
</svg>"""

    validate_svg(svg)
    return svg


def _generate_sketch_compact_header(style_name, theme_name, c, css_vars,
                                    title="PIXEL-KIT", subtitle="HAND-DRAWN SKETCH SYSTEM",
                                    tag="DRAFT_ACTIVE", width=850, height=None,
                                    tag_url=None, close_url=None):
    """Renders a hand-drawn sketch compact banner (~80px height)."""
    prim = c["primary"]
    acc = c["accent"]
    tertiary_col = c["tertiary"]
    bg = c["bg"]
    panel = c["panel"]
    border = c["border"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]
    success = c["success"]
    h = height if height else 80

    title_clean = escape_xml(title)
    sub_clean = escape_xml(subtitle)
    tag_clean = escape_xml(tag)

    tag_w = min(220, max(110, int(measure_sans_text_width(tag_clean, 11) + 36)))
    tag_x = width - tag_w - 24
    avail_title_w = max(100, tag_x - 64)
    title_disp = clamp_sans_text_to_width(title_clean, avail_title_w, 20)
    sub_disp = clamp_sans_text_to_width(sub_clean, avail_title_w - 20, 11)

    tag_link_open = f'<a href="{escape_xml(tag_url)}" target="_blank" rel="noopener noreferrer" class="sketch-hover">' if tag_url else ''
    tag_link_close = '</a>' if tag_url else ''

    chassis = render_rough_rect(x=4, y=4, w=width-8, h=h-8, stroke=border, stroke_width=1.4, fill=bg, rx=6, seed=12)
    tag_box = render_rough_rect(x=tag_x, y=24, w=tag_w, h=28, stroke=acc, stroke_width=1.2, fill=panel, rx=6, seed=22)
    star_badge = render_rough_star(cx=tag_x + 14, cy=38, r=4.5, fill=tertiary_col, stroke=tertiary_col, seed=23)
    underline_w = min(avail_title_w, int(measure_sans_text_width(title_disp, 20) * 1.05))
    wavy_underline = render_rough_line(32, 42, 32 + underline_w, 42, stroke=acc, stroke_width=1.5, jitter=1.1, seed=15)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%">
  <defs>
    <style>
      {css_vars}
{SKETCH_BASE_STYLES}
    </style>
{render_sketch_defs(c, "compactSketch")}
  </defs>

  <!-- Sketch Rough Card Chassis -->
  {chassis}

  <!-- Doodle Action Dots -->
  <circle cx="18" cy="18" r="3.5" fill="{prim}" opacity="0.8"/>
  <circle cx="28" cy="18" r="3.5" fill="{acc}" opacity="0.8"/>
  <circle cx="38" cy="18" r="3.5" fill="{tertiary_col}" opacity="0.8"/>

  <!-- Hand-Drawn Typography -->
  <text x="32" y="36" font-size="20" font-weight="700" fill="{prim}" class="font-sketch">{title_disp}</text>
  {wavy_underline}
  <text x="32" y="62" fill="{text_dim}" font-size="11" font-weight="500" class="font-sketch">✏️ {sub_disp}</text>

  <!-- Sketch Tag Badge -->
  {tag_link_open}<g>
    {tag_box}
    {star_badge}
    <text x="{tag_x + tag_w//2 + 6}" y="42" fill="{text_main}" font-size="11" font-weight="600" text-anchor="middle" class="font-sketch">{tag_clean}</text>
  </g>{tag_link_close}
</svg>"""

    validate_svg(svg)
    return svg


def _generate_sketch_header(style_name, theme_name, c, css_vars,
                            title="PIXEL-KIT", subtitle="HAND-DRAWN SKETCH SYSTEM",
                            specs=None, spec1=None, spec2=None, spec3=None,
                            tag="DRAFT_ACTIVE", width=850, height=None,
                            tag_url=None, close_url=None):
    """Renders a flagship hand-drawn sketch banner with rough borders, pencil hatching, and doodle annotations."""
    prim = c["primary"]
    acc = c["accent"]
    tertiary_col = c["tertiary"]
    bg = c["bg"]
    panel = c["panel"]
    border = c["border"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]
    success = c["success"]

    title_clean = escape_xml(title)
    sub_clean = escape_xml(subtitle)
    tag_clean = escape_xml(tag)

    norm_specs = normalize_specs(specs=specs, spec1=spec1, spec2=spec2, spec3=spec3, default_color=None)

    # Dynamic height calculation
    specs_count = len(norm_specs[:3]) if norm_specs else 0
    needed_h = 190 + (specs_count * 24)
    h = max(height or 0, max(230, needed_h))

    title_disp = clamp_sans_text_to_width(title_clean, 480, 26)
    sub_disp = clamp_sans_text_to_width(sub_clean, 460, 12)

    tag_w = min(220, max(120, int(measure_sans_text_width(tag_clean, 11) + 40)))
    tag_x = width - tag_w - 24
    tag_link_open = f'<a href="{escape_xml(tag_url)}" target="_blank" rel="noopener noreferrer" class="sketch-hover">' if tag_url else ''
    tag_link_close = '</a>' if tag_url else ''

    chassis = render_rough_rect(x=4, y=4, w=width-8, h=h-8, stroke=border, stroke_width=1.5, fill=bg, rx=6, seed=42)
    tag_box = render_rough_rect(x=tag_x, y=14, w=tag_w, h=26, stroke=acc, stroke_width=1.2, fill=panel, rx=6, seed=63)
    tag_star = render_rough_star(cx=tag_x + 14, cy=27, r=4.0, fill=tertiary_col, stroke=tertiary_col, seed=64)

    title_w_est = min(480, int(measure_sans_text_width(title_disp, 26) * 1.05))
    wavy_title_line = render_rough_line(40, 84, 40 + title_w_est, 84, stroke=acc, stroke_width=2.0, jitter=1.4, seed=70)

    sub_highlight_w = min(480, int(measure_sans_text_width(sub_disp, 12) + 32))

    # Spec bullet lines
    spec_lines = []
    if norm_specs:
        y_specs_start = 138
        for i, spec in enumerate(norm_specs[:3]):
            lbl = escape_xml(spec[0])
            val = escape_xml(spec[1])
            val_col = spec[2] if (len(spec) > 2 and spec[2]) else text_main
            y = y_specs_start + i * 22
            arrow = render_rough_arrow(42, y - 4, 52, y - 4, stroke=acc, stroke_width=1.2, arrow_size=4.5, seed=80 + i * 7)
            spec_lines.append(f"""  {arrow}
  <text x="60" y="{y}" fill="{text_dim}" font-size="11" class="font-sketch">{lbl}: <tspan fill="{val_col}" font-weight="600">{val}</tspan></text>""")

    specs_markup = "\n".join(spec_lines)

    # Right side: Hand-drawn sticky note / architectural doodle card
    note_w = 190
    note_h = 136
    note_x = width - note_w - 24
    note_y = 52
    note_rect = render_rough_rect(x=note_x, y=note_y, w=note_w, h=note_h, stroke=prim, stroke_width=1.4, fill=panel, rx=4, seed=90)
    note_star = render_rough_star(cx=note_x + note_w // 2, cy=note_y + 44, r=22, fill=f"url(#headerSketch-hatch)", stroke=tertiary_col, stroke_width=1.8, seed=92)
    note_line = render_rough_line(note_x + 20, note_y + 82, note_x + note_w - 20, note_y + 82, stroke=border, stroke_width=1.0, jitter=1.2, seed=94)

    bottom_divider = render_rough_line(16, h - 26, width - 16, h - 26, stroke=border, stroke_width=1.0, jitter=0.8, seed=99)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%">
  <defs>
    <style>
      {css_vars}
{SKETCH_BASE_STYLES}
    </style>
{render_sketch_defs(c, "headerSketch")}
  </defs>

  <!-- Sketch Hull Chassis -->
  {chassis}

  <!-- Header Meta Bar -->
  <text x="24" y="28" fill="{text_dim}" font-size="11" font-weight="600" class="font-sketch">// ARCHITECTURE DRAFT • EXCALIDRAW CANVAS</text>

  <!-- Tag Pill -->
  {tag_link_open}<g>
    {tag_box}
    {tag_star}
    <text x="{tag_x + tag_w//2 + 5}" y="31" fill="{text_main}" font-size="11" font-weight="600" text-anchor="middle" class="font-sketch">{tag_clean}</text>
  </g>{tag_link_close}

  <!-- Title & Underline -->
  <text x="40" y="74" font-size="26" font-weight="700" fill="{prim}" class="font-sketch">{title_disp}</text>
  {wavy_title_line}

  <!-- Subtitle with Marker Highlighter -->
  <rect x="40" y="98" width="{sub_highlight_w}" height="20" rx="3" fill="{tertiary_col}" fill-opacity="0.2" />
  <text x="48" y="112" fill="{text_main}" font-size="12" font-weight="600" class="font-sketch">✏️ {sub_disp}</text>

  <!-- Specs Checklist -->
  {specs_markup}

  <!-- Right Side Sticky Note with Washi Tape -->
  <g>
    <polygon points="{note_x + 65} {note_y - 8}, {note_x + 125} {note_y - 8}, {note_x + 117} {note_y + 6}, {note_x + 57} {note_y + 6}"
             fill="url(#headerSketch-tape)" stroke="{tertiary_col}" stroke-width="0.8" opacity="0.85" />
    {note_rect}
    {note_star}
    {note_line}
    <text x="{note_x + note_w//2}" y="{note_y + 102}" fill="{text_main}" font-size="11" font-weight="600" text-anchor="middle" class="font-sketch">★ HANDMADE IN SVG</text>
    <text x="{note_x + note_w//2}" y="{note_y + 118}" fill="{text_dim}" font-size="9" text-anchor="middle" class="font-sketch">deterministic physics</text>
  </g>

  <!-- Bottom Draft Notes Line -->
  {bottom_divider}
  <text x="24" y="{h-13}" fill="{text_dim}" font-size="10" class="font-sketch">STYLE // HAND-DRAWN SKETCH • ZERO-DEPENDENCY • NO EXTERNAL IMAGES</text>
  <text x="{width-24}" y="{h-13}" fill="{prim}" font-size="10" font-weight="600" text-anchor="end" class="font-sketch">STATUS: DRAFT OK ✎</text>
</svg>"""

    validate_svg(svg)
    return svg


def _generate_compact_header(style=None, primary=None, accent=None,
                             title="PIXEL-KIT", subtitle="TRANSLUCENT HUD DESIGN SYSTEM",
                             tag="SYSTEM_ACTIVE", width=850, height=None, mode="auto", preset=None,
                             tag_url=None, close_url=None, tertiary=None, theme=None):
    """
    Renders a low-profile compact banner (~84px height) optimized for mobile viewports.
    """
    style_name, theme_name = normalize_style_and_theme(style=style, theme=theme)
    c, css_vars = resolve_theme(style=style_name, theme=theme_name, mode=mode, primary=primary, accent=accent, preset=preset, tertiary=tertiary)
    if style_name == "modern":
        return _generate_modern_compact_header(
            style_name=style_name, theme_name=theme_name, c=c, css_vars=css_vars,
            title=title, subtitle=subtitle, tag=tag, width=width, height=height,
            tag_url=tag_url, close_url=close_url
        )
    elif style_name == "sketch":
        return _generate_sketch_compact_header(
            style_name=style_name, theme_name=theme_name, c=c, css_vars=css_vars,
            title=title, subtitle=subtitle, tag=tag, width=width, height=height,
            tag_url=tag_url, close_url=close_url
        )
    prim = c["primary"]
    acc = c["accent"]
    tertiary_col = c["tertiary"]
    bg = c["bg"]
    panel = c["panel"]
    border = c["border"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]
    st = theme_name
    h = height if height else 84


    title_clean = escape_xml(title)
    sub_clean = escape_xml(subtitle)
    tag_clean = escape_xml(tag)

    pixel_markup, t_w, t_h = render_3d_text(
        title, x=32, y=14, px_size=3,
        front_color=c["title_front"], mid_shadow=c["title_mid"], dark_shadow=c["title_dark"],
        spacing=2, max_width=width - 240, allow_wrap=False
    )

    y_sub = 14 + t_h + 6
    if y_sub > h - 18:
        h = y_sub + 22

    tag_w = min(200, max(120, int(measure_mono_text_width(tag_clean, 11) + 24)))
    tag_x = width - tag_w - 24
    status_widget = f"""  <rect x="{tag_x}" y="24" width="{tag_w}" height="32" fill="{panel}" stroke="{prim}" stroke-width="1.2"/>
  <text x="{tag_x + tag_w//2}" y="44" fill="{acc}" font-size="11" font-weight="bold" text-anchor="middle" class="font-mono">{tag_clean}</text>"""

    avail_sub_w = max(60, tag_x - 46)
    sub_disp = clamp_text_to_width(f"■ {sub_clean}", avail_sub_w, 11)

    if st == "tactical":
        hull = f"""  <polygon points="12 2, {width-12} 2, {width-2} 12, {width-2} {h-12}, {width-12} {h-2}, 12 {h-2}, 2 {h-12}, 2 12" fill="{bg}" stroke="{border}" stroke-width="1.5"/>
  <polygon points="2 12, 14 2, 2 2" fill="{prim}"/>
  <polygon points="{width-2} {h-12}, {width-14} {h-2}, {width-2} {h-2}" fill="{acc}"/>
  <g fill="{prim}" opacity="0.6">
    <polygon points="20 6, 26 6, 18 14, 12 14"/>
    <polygon points="30 6, 36 6, 28 14, 22 14"/>
  </g>"""
    elif st == "minimal":
        hull = f"""  <rect x="2" y="2" width="{width-4}" height="{h-4}" fill="{bg}" stroke="{border}" stroke-width="1"/>
  <line x1="2" y1="2" x2="{width-2}" y2="2" stroke="{prim}" stroke-width="2"/>
  <rect x="6" y="6" width="3" height="3" fill="{prim}"/>
  <rect x="{width-9}" y="6" width="3" height="3" fill="{acc}"/>"""
    else:  # cyberpunk
        hull = f"""  <rect x="2" y="2" width="{width-4}" height="{h-4}" fill="{bg}" stroke="{border}" stroke-width="1.5"/>
  <rect x="2" y="2" width="6" height="6" fill="{prim}"/>
  <rect x="{width-8}" y="2" width="6" height="6" fill="{acc}"/>
  <rect x="2" y="{h-8}" width="6" height="6" fill="{acc}"/>
  <rect x="{width-8}" y="{h-8}" width="6" height="6" fill="{prim}"/>
  <line x1="2" y1="18" x2="8" y2="18" stroke="{prim}" stroke-width="1"/>
  <line x1="{width-8}" y1="{h-18}" x2="{width-2}" y2="{h-18}" stroke="{acc}" stroke-width="1"/>"""

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
    </style>
  </defs>
{hull}
  {pixel_markup}
  <text x="34" y="{y_sub + 12}" fill="{text_dim}" font-size="11" font-weight="bold" class="font-mono">{sub_disp}</text>
{status_widget}
</svg>"""

    validate_svg(svg)
    return svg

def generate_header(style=None, primary=None, accent=None,
                    title="PIXEL-KIT", subtitle="TRANSLUCENT HUD DESIGN SYSTEM",
                    specs=None, spec1=None, spec2=None, spec3=None,
                    tag="SYSTEM_ACTIVE", width=850, height=None, mode="auto", preset=None,
                    tag_url=None, close_url=None, compact=False, tertiary=None, theme=None):
    if compact and str(compact).lower() in ("true", "1", "yes", "compact"):
        return _generate_compact_header(
            style=style, primary=primary, accent=accent, title=title, subtitle=subtitle,
            tag=tag, width=width, height=height, mode=mode, preset=preset,
            tag_url=tag_url, close_url=close_url, tertiary=tertiary, theme=theme
        )

    style_name, theme_name = normalize_style_and_theme(style=style, theme=theme)
    c, css_vars = resolve_theme(style=style_name, theme=theme_name, mode=mode, primary=primary, accent=accent, preset=preset, tertiary=tertiary)
    if style_name == "modern":
        return _generate_modern_header(
            style_name=style_name, theme_name=theme_name, c=c, css_vars=css_vars,
            title=title, subtitle=subtitle, specs=specs, spec1=spec1, spec2=spec2, spec3=spec3,
            tag=tag, width=width, height=height, tag_url=tag_url, close_url=close_url
        )
    elif style_name == "sketch":
        return _generate_sketch_header(
            style_name=style_name, theme_name=theme_name, c=c, css_vars=css_vars,
            title=title, subtitle=subtitle, specs=specs, spec1=spec1, spec2=spec2, spec3=spec3,
            tag=tag, width=width, height=height, tag_url=tag_url, close_url=close_url
        )
    prim = c["primary"]
    acc = c["accent"]
    tertiary_col = c["tertiary"]
    bg = c["bg"]
    panel = c["panel"]
    border = c["border"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]
    success = c["success"]
    warning = c["warning"]
    grid_op = c["grid_op"]
    front_color = c["title_front"]
    mid_shadow = c["title_mid"]
    dark_shadow = c["title_dark"]

    title_clean = escape_xml(title)
    sub_clean = escape_xml(subtitle)
    tag_clean = escape_xml(tag)
    if theme_name in ("tactical", "amber", "amber_crt"):
        st = "tactical"
    elif theme_name in ("minimal", "clean-mono", "clean_mono", "academic-paper", "academic_paper", "corporate-blue", "corporate_blue", "tokyo", "tokyo_night", "swiss-mono", "swiss_mono", "executive-slate", "executive_slate"):
        st = "minimal"
    else:
        st = "cyberpunk"

    # Dynamic subtitle box width and safe clamp
    sub_w = min(480, max(260, int(measure_mono_text_width(subtitle, 11) + 40)))
    sub_tactical = clamp_text_to_width(f"[TARGET] {sub_clean}", sub_w - 24, 11)
    sub_minimal = clamp_text_to_width(f"⚡ {sub_clean}", sub_w - 24, 11)
    sub_cyberpunk = clamp_text_to_width(f"⚡ {sub_clean}", sub_w - 24, 11)

    # Normalize specs (max 3 items, [] if omitted)
    norm_specs = normalize_specs(specs=specs, spec1=spec1, spec2=spec2, spec3=spec3, default_color=None)

    if st == "tactical":
        y_title = 50
        pixel_markup, t_w, t_h = render_3d_text(
            title, x=42, y=y_title, px_size=None,
            front_color=front_color, mid_shadow=mid_shadow, dark_shadow=dark_shadow,
            spacing=2, max_width=480, allow_wrap=True
        )
        y_sub = y_title + t_h + 8
        sub_bottom = y_sub + 24

        spec_lines = []
        if norm_specs:
            y_specs_start = sub_bottom + 25
            for i, spec in enumerate(norm_specs[:3]):
                lbl = spec[0]
                val = spec[1]
                val_col = spec[2] if (len(spec) > 2 and spec[2]) else text_main
                y = y_specs_start + i * 20
                lbl_disp = clamp_text_to_width(lbl, 140, 11)
                prefix = f"&gt; {lbl_disp}: "
                avail_val_w = max(40, 480 - int(measure_mono_text_width(prefix, 11)))
                val_disp = clamp_text_to_width(val, avail_val_w, 11)
                spec_lines.append(f"""
  <text x="42" y="{y}" fill="{prim}" font-size="11" class="font-mono">&gt; {escape_xml(lbl_disp)}: <tspan fill="{val_col}">{escape_xml(val_disp)}</tspan></text>
""")
            last_spec_y = y_specs_start + (len(norm_specs[:3]) - 1) * 20
            content_bottom = last_spec_y + 6
        else:
            content_bottom = sub_bottom

        specs_markup = "".join(spec_lines)

        needed_h = content_bottom + 36
        calc_h = max(220, needed_h)
        h = max(height or 0, calc_h)

        reticle_cy = max(105, min(h - 80, (h // 2) - 5))

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      @keyframes targetScan {{
        0% {{ transform: translateX(0px); opacity: 0; }}
        15% {{ opacity: 0.85; }}
        85% {{ opacity: 0.85; }}
        100% {{ transform: translateX({width-120}px); opacity: 0; }}
      }}
      @keyframes pulseLock {{
        0%, 100% {{ opacity: 1; transform: scale(1); }}
        50% {{ opacity: 0.45; transform: scale(0.96); }}
      }}
      @keyframes chevronBlink {{
        0%, 100% {{ opacity: 0.95; }}
        50% {{ opacity: 0.35; }}
      }}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
      .laser-scan {{ animation: targetScan 4s ease-in-out infinite; }}
      .reticle-pulse {{ transform-origin: 750px {reticle_cy}px; animation: pulseLock 2s infinite ease-in-out; }}
      .chevron-pulse {{ animation: chevronBlink 1.6s infinite steps(1); }}
    </style>
  </defs>

  <!-- 1. 45° CHAMFERED CHASSIS -->
  <polygon points="20 4, {width-20} 4, {width-4} 20, {width-4} {h-20}, {width-20} {h-4}, 20 {h-4}, 4 {h-20}, 4 20"
           fill="{bg}" stroke="{border}" stroke-width="2"/>
  
  <polygon points="24 10, {width-24} 10, {width-10} 24, {width-10} {h-24}, {width-24} {h-10}, 24 {h-10}, 10 {h-24}, 10 24"
           fill="none" stroke="{prim}" stroke-width="1.5" opacity="0.75"/>

  <!-- HAZARD STRIPES TOP-LEFT -->
  <g fill="{prim}" class="chevron-pulse">
    <polygon points="30 14, 38 14, 26 26, 18 26"/>
    <polygon points="44 14, 52 14, 40 26, 32 26"/>
    <polygon points="58 14, 66 14, 54 26, 46 26"/>
  </g>

  <!-- TACTICAL TITLE BAR -->
  <text x="80" y="24" fill="{prim}" font-size="11" font-weight="bold" letter-spacing="1.5" class="font-mono">
    // TACTICAL.HUD // SEC_CLASS_ALPHA // SYSTEM_READY // {tag_clean}
  </text>

  <!-- 3D PIXEL TITLE -->
  {pixel_markup}

  <!-- SUBTITLE -->
  <rect x="42" y="{y_sub}" width="{sub_w}" height="24" fill="{panel}" stroke="{acc}" stroke-width="1"/>
  <text x="54" y="{y_sub+16}" fill="{text_main}" font-size="11" font-weight="bold" class="font-mono">
    {sub_tactical}
  </text>

  <!-- SPECS TELEMETRY -->
  {specs_markup}

  <!-- RIGHT SIDE: TARGET LOCK-ON CROSSHAIR RETICLE -->
  <g class="reticle-pulse">
    <circle cx="750" cy="{reticle_cy}" r="45" fill="none" stroke="{prim}" stroke-width="1.5" stroke-dasharray="8,4"/>
    <circle cx="750" cy="{reticle_cy}" r="24" fill="none" stroke="{acc}" stroke-width="1.5"/>
    <circle cx="750" cy="{reticle_cy}" r="4" fill="{acc}"/>
    <line x1="750" y1="{reticle_cy - 55}" x2="750" y2="{reticle_cy - 30}" stroke="{prim}" stroke-width="2"/>
    <line x1="750" y1="{reticle_cy + 30}" x2="750" y2="{reticle_cy + 55}" stroke="{prim}" stroke-width="2"/>
    <line x1="695" y1="{reticle_cy}" x2="720" y2="{reticle_cy}" stroke="{prim}" stroke-width="2"/>
    <line x1="780" y1="{reticle_cy}" x2="805" y2="{reticle_cy}" stroke="{prim}" stroke-width="2"/>
    <path d="M 725 {reticle_cy - 25} L 720 {reticle_cy - 25} L 720 {reticle_cy - 20}" fill="none" stroke="{prim}" stroke-width="2"/>
    <path d="M 775 {reticle_cy - 25} L 780 {reticle_cy - 25} L 780 {reticle_cy - 20}" fill="none" stroke="{prim}" stroke-width="2"/>
    <path d="M 725 {reticle_cy + 25} L 720 {reticle_cy + 25} L 720 {reticle_cy + 20}" fill="none" stroke="{prim}" stroke-width="2"/>
    <path d="M 775 {reticle_cy + 25} L 780 {reticle_cy + 25} L 780 {reticle_cy + 20}" fill="none" stroke="{prim}" stroke-width="2"/>
    <text x="750" y="{reticle_cy + 63}" fill="{prim}" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">TARGET LOCK</text>
  </g>

  <!-- SWEEPING TARGET LASER -->
  <g class="laser-scan">
    <line x1="50" y1="10" x2="50" y2="{h-10}" stroke="{acc}" stroke-width="1.5" opacity="0.8"/>
    <circle cx="50" cy="20" r="3" fill="{acc}"/>
    <circle cx="50" cy="{h-20}" r="3" fill="{acc}"/>
  </g>
</svg>"""

    elif st == "minimal":
        y_title = 36
        pixel_markup, t_w, t_h = render_3d_text(
            title, x=42, y=y_title, px_size=None,
            front_color=front_color, mid_shadow=mid_shadow, dark_shadow=dark_shadow,
            spacing=2, max_width=500, allow_wrap=True
        )
        y_sub = y_title + t_h + 8
        sub_bottom = y_sub + 22

        spec_lines = []
        if norm_specs:
            y_specs_start = sub_bottom + 22
            for i, spec in enumerate(norm_specs[:3]):
                lbl = spec[0]
                val = spec[1]
                val_col = spec[2] if (len(spec) > 2 and spec[2]) else text_main
                y = y_specs_start + i * 18
                lbl_disp = clamp_text_to_width(lbl, 140, 10)
                prefix = f"// {lbl_disp}: "
                avail_val_w = max(40, 480 - int(measure_mono_text_width(prefix, 10)))
                val_disp = clamp_text_to_width(val, avail_val_w, 10)
                spec_lines.append(f"""
  <text x="42" y="{y}" fill="{prim}" font-size="10" class="font-mono">// {escape_xml(lbl_disp)}: <tspan fill="{val_col}">{escape_xml(val_disp)}</tspan></text>
""")
            last_spec_y = y_specs_start + (len(norm_specs[:3]) - 1) * 18
            content_bottom = last_spec_y + 4
        else:
            content_bottom = sub_bottom

        specs_markup = "".join(spec_lines)

        min_default_h = 135 if not norm_specs else (140 + len(norm_specs[:3]) * 18)
        needed_h = content_bottom + 34
        calc_h = max(min_default_h, needed_h)
        h = max(height or 0, calc_h)

        eq_y = max(35, min(h - 75, (h // 2) - 25))

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      @keyframes eqBar1 {{ 0%, 100% {{ height: 12px; y: 28px; }} 50% {{ height: 32px; y: 8px; }} }}
      @keyframes eqBar2 {{ 0%, 100% {{ height: 28px; y: 12px; }} 50% {{ height: 10px; y: 30px; }} }}
      @keyframes eqBar3 {{ 0%, 100% {{ height: 18px; y: 22px; }} 50% {{ height: 36px; y: 4px; }} }}
      @keyframes eqBar4 {{ 0%, 100% {{ height: 34px; y: 6px; }} 50% {{ height: 14px; y: 26px; }} }}
      @keyframes eqBar5 {{ 0%, 100% {{ height: 22px; y: 18px; }} 50% {{ height: 8px; y: 32px; }} }}
      @keyframes neonBreath {{ 0%, 100% {{ opacity: 0.9; }} 50% {{ opacity: 0.45; }} }}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
      .eq1 {{ animation: eqBar1 1.2s infinite ease-in-out; }}
      .eq2 {{ animation: eqBar2 0.9s infinite ease-in-out; }}
      .eq3 {{ animation: eqBar3 1.4s infinite ease-in-out; }}
      .eq4 {{ animation: eqBar4 1.1s infinite ease-in-out; }}
      .eq5 {{ animation: eqBar5 1.5s infinite ease-in-out; }}
      .breath {{ animation: neonBreath 3s infinite ease-in-out; }}
    </style>
  </defs>

  <!-- BACKGROUND GLASS -->
  <rect x="4" y="4" width="{width-8}" height="{h-8}" fill="{bg}" stroke="{border}" stroke-width="2"/>
  <rect x="8" y="8" width="{width-16}" height="{h-16}" fill="none" stroke="{prim}" stroke-width="1.5" class="breath"/>

  <!-- CORNER PIXEL ACCENTS -->
  <rect x="4" y="4" width="8" height="3" fill="{prim}"/>
  <rect x="4" y="4" width="3" height="8" fill="{prim}"/>
  <rect x="{width-12}" y="4" width="8" height="3" fill="{prim}"/>
  <rect x="{width-7}" y="4" width="3" height="8" fill="{prim}"/>
  <rect x="4" y="{h-7}" width="8" height="3" fill="{prim}"/>
  <rect x="4" y="{h-12}" width="3" height="8" fill="{prim}"/>
  <rect x="{width-12}" y="{h-7}" width="8" height="3" fill="{prim}"/>
  <rect x="{width-7}" y="{h-12}" width="3" height="8" fill="{prim}"/>

  <!-- 3D PIXEL TITLE -->
  {pixel_markup}

  <!-- SUBTITLE CHIP -->
  <g transform="translate(42, {y_sub})">
    <rect x="0" y="0" width="{sub_w}" height="22" fill="{panel}" stroke="{acc}" stroke-width="1"/>
    <text x="12" y="15" fill="{text_main}" font-size="11" font-weight="bold" class="font-mono">{sub_minimal}</text>
  </g>

  <!-- SPECS TELEMETRY -->
  {specs_markup}

  <!-- EQUALIZER BARS (RIGHT SIDE) -->
  <g transform="translate({width-120}, {eq_y})">
    <rect x="0" y="28" width="8" height="12" fill="{prim}" class="eq1"/>
    <rect x="14" y="12" width="8" height="28" fill="{acc}" class="eq2"/>
    <rect x="28" y="22" width="8" height="18" fill="{tertiary_col}" class="eq3"/>
    <rect x="42" y="6" width="8" height="34" fill="{warning}" class="eq4"/>
    <rect x="56" y="18" width="8" height="22" fill="{success}" class="eq5"/>
    <text x="32" y="52" fill="{prim}" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">LIVE_AUDIO</text>
  </g>
</svg>"""

    else:
        # Cyberpunk Workstation (Default Flagship: 360° Animated Radar, CRT Scanline, 20px Grid, Equalizer)
        y_title = 60
        pixel_markup, t_w, t_h = render_3d_text(
            title, x=42, y=y_title, px_size=None,
            front_color=front_color, mid_shadow=mid_shadow, dark_shadow=dark_shadow,
            spacing=2, max_width=480, allow_wrap=True
        )
        y_sub = y_title + t_h + 8
        sub_bottom = y_sub + 28

        teletype_block = ""
        if norm_specs:
            teletype_svg = []
            y_teletype_start = max(182, sub_bottom + 28)
            default_colors = [prim, acc, success]
            for i, spec in enumerate(norm_specs[:3]):
                lbl = spec[0]
                val = spec[1]
                col = spec[2] if (len(spec) > 2 and spec[2]) else default_colors[i % 3]
                y_pos = y_teletype_start + i * 20
                lbl_disp = clamp_text_to_width(lbl, 130, 11)
                lbl_w = measure_mono_text_width(f"{lbl_disp}:", 11)
                val_x = max(200, int(60 + lbl_w + 12))
                avail_val_w = max(40, 480 - val_x)
                val_disp = clamp_text_to_width(val, avail_val_w, 11)
                teletype_svg.append(f"""
    <text x="42" y="{y_pos}" fill="{success}" font-size="12" font-weight="bold" class="font-mono">&gt;</text>
    <text x="60" y="{y_pos}" fill="{text_main}" font-size="11" class="font-mono">{escape_xml(lbl_disp)}:</text>
    <text x="{val_x}" y="{y_pos}" fill="{col}" font-size="11" font-weight="bold" class="font-mono">{escape_xml(val_disp)}</text>
""")

            last_y = y_teletype_start + (len(norm_specs[:3]) - 1) * 20
            eq_offset = last_y - 210
            content_bottom = last_y + 12
            teletype_block = f"""
  <!-- TELETYPE TELEMETRY LINES -->
  <g>
    {''.join(teletype_svg)}
    <rect x="500" y="{last_y - 10}" width="8" height="12" fill="{prim}" class="cursor-blink"/>
  </g>

  <!-- MINI SPECTRUM EQUALIZER -->
  <g transform="translate(525, {eq_offset})">
    <rect x="0" y="198" width="5" height="6" fill="{prim}" class="w1"/>
    <rect x="8" y="186" width="5" height="18" fill="{acc}" class="w2"/>
    <rect x="16" y="192" width="5" height="12" fill="{tertiary_col}" class="w3"/>
    <rect x="24" y="182" width="5" height="22" fill="{warning}" class="w4"/>
  </g>
"""
        else:
            content_bottom = sub_bottom

        min_default_h = 260
        needed_h = content_bottom + 48
        calc_h = max(min_default_h, needed_h)
        h = max(height or 0, calc_h)

        grid_lines = []
        for x in range(0, width + 1, 20):
            grid_lines.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{h}" stroke="{prim}" stroke-width="1"/>')
        for y in range(0, h + 1, 20):
            grid_lines.append(f'<line x1="0" y1="{y}" x2="{width}" y2="{y}" stroke="{prim}" stroke-width="1"/>')

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      @keyframes blink {{
        0%, 49% {{ opacity: 1; }}
        50%, 100% {{ opacity: 0; }}
      }}
      @keyframes ledFlicker {{
        0%, 100% {{ fill: {success}; opacity: 1; }}
        50% {{ fill: {success}; opacity: 0.2; }}
      }}
      @keyframes crtScanline {{
        0% {{ transform: translateY(0px); opacity: 0; }}
        20% {{ opacity: 0.35; }}
        80% {{ opacity: 0.35; }}
        100% {{ transform: translateY({h}px); opacity: 0; }}
      }}
      @keyframes waveBar1 {{ 0%, 100% {{ height: 6px; y: 198px; }} 50% {{ height: 20px; y: 184px; }} }}
      @keyframes waveBar2 {{ 0%, 100% {{ height: 18px; y: 186px; }} 50% {{ height: 8px; y: 196px; }} }}
      @keyframes waveBar3 {{ 0%, 100% {{ height: 12px; y: 192px; }} 50% {{ height: 22px; y: 182px; }} }}
      @keyframes waveBar4 {{ 0%, 100% {{ height: 22px; y: 182px; }} 50% {{ height: 10px; y: 194px; }} }}
      .font-mono {{
        font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace;
      }}
      .cursor-blink {{
        animation: blink 1s infinite steps(1);
      }}
      .status-led {{
        animation: ledFlicker 1.8s infinite steps(1);
      }}
      .scan-line {{
        animation: crtScanline 6s linear infinite;
      }}
      .w1 {{ animation: waveBar1 1.1s infinite ease-in-out; }}
      .w2 {{ animation: waveBar2 0.8s infinite ease-in-out; }}
      .w3 {{ animation: waveBar3 1.3s infinite ease-in-out; }}
      .w4 {{ animation: waveBar4 0.9s infinite ease-in-out; }}
    </style>
  </defs>

  <!-- 1. TRANSLUCENT GLASS BACKGROUND -->
  <rect x="0" y="0" width="{width}" height="{h}" fill="{bg}"/>

  <!-- 2. MATRIX RETRO GRID PATTERN -->
  <g opacity="{grid_op}">
    {''.join(grid_lines)}
  </g>

  <!-- 3. ANIMATED SCANLINE -->
  <line x1="0" y1="0" x2="{width}" y2="0" stroke="{prim}" stroke-width="2" class="scan-line"/>

  <!-- 4. OUTER CHASSIS / BORDER -->
  <rect x="6" y="6" width="{width-12}" height="{h-12}" fill="none" stroke="{border}" stroke-width="2"/>
  <rect x="12" y="12" width="{width-24}" height="{h-24}" fill="none" stroke="{prim}" stroke-width="2" opacity="0.85"/>

  <!-- CORNER ACCENT BRACKETS (PRIMARY + SECONDARY DUAL-TONE) -->
  <rect x="6" y="6" width="24" height="6" fill="{prim}"/>
  <rect x="6" y="6" width="6" height="24" fill="{prim}"/>
  <rect x="{width-30}" y="6" width="24" height="6" fill="{acc}"/>
  <rect x="{width-12}" y="6" width="6" height="24" fill="{acc}"/>
  <rect x="6" y="{h-12}" width="24" height="6" fill="{acc}"/>
  <rect x="6" y="{h-30}" width="6" height="24" fill="{acc}"/>
  <rect x="{width-30}" y="{h-12}" width="24" height="6" fill="{prim}"/>
  <rect x="{width-12}" y="{h-30}" width="6" height="24" fill="{prim}"/>

  <!-- TOP CONSOLE STATUS BAR -->
  <rect x="14" y="14" width="{width-28}" height="22" fill="{panel}"/>
  <line x1="14" y1="36" x2="260" y2="36" stroke="{prim}" stroke-width="1.5" opacity="0.8"/>
  <line x1="260" y1="36" x2="{width-14}" y2="36" stroke="{acc}" stroke-width="1.5" opacity="0.5"/>

  <circle cx="28" cy="25" r="4" fill="{success}" class="status-led"/>
  <text x="38" y="29" fill="{success}" font-size="11" font-weight="bold" class="font-mono">SYS: ONLINE // 0x00</text>

  <rect x="175" y="19" width="2" height="12" fill="{acc}" opacity="0.7"/>
  <text x="188" y="29" fill="{text_dim}" font-size="11" class="font-mono">HUD: ACTIVE_SYS</text>

  <rect x="360" y="19" width="2" height="12" fill="{acc}" opacity="0.7"/>
  <text x="372" y="29" fill="{text_dim}" font-size="11" class="font-mono">MODE: {st.upper()}_HUD</text>

  <!-- Tag right-anchored to never collide with window controls -->
  {f'<a href="{escape_xml(tag_url)}" target="_blank" class="btn-hover">' if tag_url else ''}<text x="{width-95}" y="29" fill="{warning}" font-size="11" font-weight="bold" text-anchor="end" class="font-mono">{tag_clean}</text>{'</a>' if tag_url else ''}

  <!-- Window controls [ _ ] [ □ ] [ × ] -->
  <rect x="{width-85}" y="19" width="16" height="12" fill="{border}"/>
  <text x="{width-80}" y="28" fill="{text_dim}" font-size="10" font-weight="bold" class="font-mono">_</text>
  <rect x="{width-63}" y="19" width="16" height="12" fill="{border}"/>
  <text x="{width-59}" y="29" fill="{text_dim}" font-size="11" font-weight="bold" class="font-mono">□</text>
  {f'<a href="{escape_xml(close_url)}" target="_blank" class="btn-hover">' if close_url else ''}<rect x="{width-41}" y="19" width="16" height="12" fill="{tertiary_col}"/><text x="{width-37}" y="29" fill="{text_main}" font-size="11" font-weight="bold" class="font-mono">×</text>{'</a>' if close_url else ''}

  <!-- 3D PIXEL TITLE -->
  {pixel_markup}

  <!-- SUB-BADGE: ROLE & SPECIALIZATION -->
  <g transform="translate(42, {y_sub})">
    <rect x="0" y="0" width="{sub_w}" height="26" fill="{panel}" stroke="{acc}" stroke-width="2"/>
    <rect x="-2" y="-2" width="6" height="6" fill="{acc}"/>
    <rect x="{sub_w-4}" y="-2" width="6" height="6" fill="{acc}"/>
    <rect x="-2" y="22" width="6" height="6" fill="{acc}"/>
    <rect x="{sub_w-4}" y="22" width="6" height="6" fill="{acc}"/>
    <text x="12" y="18" fill="{text_main}" font-size="11" font-weight="bold" letter-spacing="1" class="font-mono">
      {sub_cyberpunk}
    </text>
  </g>

  {teletype_block}

  <!-- RIGHT SIDE: RETRO SCI-FI WORKBENCH / MONITOR HUD (RADAR) -->
  <g transform="translate({width-220}, 60)">
    <rect x="0" y="0" width="170" height="140" fill="{panel}" stroke="{border}" stroke-width="2"/>
    <rect x="4" y="4" width="162" height="132" fill="none" stroke="{prim}" stroke-width="1" opacity="0.6"/>

    <!-- Radar Corner Accent Tabs in Secondary Accent -->
    <rect x="0" y="0" width="8" height="2" fill="{acc}"/>
    <rect x="0" y="0" width="2" height="8" fill="{acc}"/>
    <rect x="162" y="0" width="8" height="2" fill="{acc}"/>
    <rect x="168" y="0" width="2" height="8" fill="{acc}"/>
    <rect x="0" y="138" width="8" height="2" fill="{acc}"/>
    <rect x="0" y="132" width="2" height="8" fill="{acc}"/>
    <rect x="162" y="138" width="8" height="2" fill="{acc}"/>
    <rect x="168" y="132" width="2" height="8" fill="{acc}"/>

    <!-- Concentric Range Rings -->
    <circle cx="85" cy="70" r="50" fill="none" stroke="{prim}" stroke-width="1" stroke-dasharray="3,3" opacity="0.4"/>
    <circle cx="85" cy="70" r="35" fill="none" stroke="{prim}" stroke-width="1" opacity="0.3"/>
    <circle cx="85" cy="70" r="18" fill="none" stroke="{prim}" stroke-width="1" opacity="0.25"/>
    <line x1="85" y1="15" x2="85" y2="125" stroke="{prim}" stroke-width="1" opacity="0.3"/>
    <line x1="30" y1="70" x2="140" y2="70" stroke="{prim}" stroke-width="1" opacity="0.3"/>

    <!-- 360° Rotating Radar Beam -->
    <g>
      <line x1="85" y1="70" x2="85" y2="20" stroke="{success}" stroke-width="2.5" opacity="0.9"/>
      <circle cx="85" cy="35" r="3.5" fill="{warning}"/>
      <animateTransform attributeName="transform" type="rotate" from="0 85 70" to="360 85 70" dur="4s" repeatCount="indefinite"/>
    </g>

    <!-- Pulsing Radar Target Blips -->
    <circle cx="110" cy="50" r="3" fill="{tertiary_col}">
      <animate attributeName="opacity" values="0.2;1;0.2" dur="2s" repeatCount="indefinite"/>
    </circle>
    <circle cx="65" cy="85" r="2.5" fill="{success}">
      <animate attributeName="opacity" values="0.1;0.9;0.1" dur="3s" repeatCount="indefinite"/>
    </circle>

    <!-- Radar Telemetry Label -->
    <text x="85" y="132" fill="{success}" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">RADAR: ACTIVE (360°)</text>
  </g>

  <!-- BOTTOM STATUS LINE -->
  <line x1="14" y1="{h-26}" x2="{width-14}" y2="{h-26}" stroke="{border}" stroke-width="1"/>
  <text x="24" y="{h-15}" fill="{acc}" font-size="9" class="font-mono">HUD_ARCH: V4.3 <tspan fill="{text_dim}">//</tspan> DUAL_THEME: PASS <tspan fill="{text_dim}">//</tspan> SMART_LAYOUT</text>
  <text x="{width-24}" y="{h-15}" fill="{prim}" font-size="9" font-weight="bold" text-anchor="end" class="font-mono">READY // ID: 0xDEADBEEF</text>
</svg>"""

    validate_svg(svg)
    return svg


generate_compact_header = _generate_compact_header
