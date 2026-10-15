"""Chip badge components for Pixel Readme Kit."""
from typing import Optional, Any
from generator.themes import resolve_theme, normalize_style_and_theme
from generator.layout import (
    measure_mono_text_width,
    clamp_text_to_width,
    estimate_chip_width,
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


def _generate_modern_chip(style_name, theme_name, c, css_vars,
                          text="CHIP_LABEL", width=None, height=26):
    """Renders sleek vector pill badge for metadata and GitHub counters."""
    prim = c["primary"]
    acc = c["accent"]
    tertiary_col = c["tertiary"]
    bg = c["bg"]
    border = c["border"]
    panel = c["panel"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]

    raw_text = str(text).strip()
    h = height if height else 26
    rx = h // 2

    if ":" in raw_text:
        parts = raw_text.split(":", 1)
        lbl = escape_xml(parts[0].strip())
        val = escape_xml(parts[1].strip())
        lbl_w = measure_sans_text_width(lbl, 10)
        val_w = measure_sans_text_width(val, 10.5)
        calc_w = int(lbl_w + val_w + 38)
        w = width if width is not None else calc_w
        mid_sep = int(lbl_w + 20)

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <defs>
    <style>
      {css_vars}
{MODERN_BASE_STYLES}
    </style>
  </defs>

  <!-- Modern Dual-Segment Pill Badge -->
  <rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{rx-1}" fill="{bg}" stroke="{border}" stroke-width="1.2"/>
  <path d="M 1 {rx} Q 1 1 {rx} 1 L {mid_sep} 1 L {mid_sep} {h-1} L {rx} {h-1} Q 1 {h-1} 1 {h-rx} Z" fill="{panel}"/>
  <line x1="{mid_sep}" y1="1" x2="{mid_sep}" y2="{h-1}" stroke="{border}" stroke-width="1"/>

  <!-- Label & Value -->
  <text x="{mid_sep//2 + 1}" y="{h//2 + 4}" fill="{text_dim}" font-size="10" font-weight="600" text-anchor="middle" class="font-sans">{lbl}</text>
  <text x="{mid_sep + (w - mid_sep)//2}" y="{h//2 + 4}" fill="{prim}" font-size="10.5" font-weight="700" text-anchor="middle" class="font-sans">{val}</text>
</svg>"""

    else:
        text_clean = escape_xml(raw_text)
        text_w = measure_sans_text_width(text_clean, 10.5)
        calc_w = int(text_w + 36)
        w = width if width is not None else calc_w

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <defs>
    <style>
      {css_vars}
{MODERN_BASE_STYLES}
    </style>
  </defs>

  <!-- Modern Single Pill Badge with dot -->
  <rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{rx-1}" fill="{panel}" stroke="{border}" stroke-width="1.2"/>
  <circle cx="12" cy="{h//2}" r="3" fill="{prim}"/>
  <text x="{w//2 + 5}" y="{h//2 + 4}" fill="{text_main}" font-size="10.5" font-weight="600" text-anchor="middle" class="font-sans">{text_clean}</text>
</svg>"""

    validate_svg(svg)
    return svg


def _generate_sketch_chip(style_name, theme_name, c, css_vars,
                          text="CHIP_LABEL", width=None, height=26):
    """Renders hand-drawn sketch badge for metadata and GitHub counters."""
    prim = c["primary"]
    acc = c["accent"]
    tertiary_col = c.get("tertiary", "#FDE047")
    bg = c["bg"]
    border = c["border"]
    panel = c["panel"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]

    raw_text = str(text).strip()
    h = height if height else 26

    if ":" in raw_text:
        parts = raw_text.split(":", 1)
        lbl = escape_xml(parts[0].strip())
        val = escape_xml(parts[1].strip())
        lbl_w = measure_sans_text_width(lbl, 10)
        val_w = measure_sans_text_width(val, 10.5)
        calc_w = int(lbl_w + val_w + 38)
        w = width if width is not None else calc_w
        mid_sep = int(lbl_w + 20)

        outer_rect = render_rough_rect(x=1, y=1, w=w-2, h=h-2, stroke=border, stroke_width=1.3, fill=bg, rx=6, seed=190)
        divider_line = render_rough_line(mid_sep, 2, mid_sep, h-2, stroke=border, stroke_width=1.1, jitter=0.6, double_stroke=False, seed=192)

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <defs>
    <style>
      {css_vars}
{SKETCH_BASE_STYLES}
    </style>
{render_sketch_defs(c, "chipSketchDual")}
  </defs>

  <!-- Sketch Dual-Segment Badge -->
  {outer_rect}
  <rect x="2" y="2" width="{mid_sep-3}" height="{h-4}" rx="4" fill="{panel}" />
  {divider_line}

  <!-- Label & Value -->
  <text x="{mid_sep//2 + 1}" y="{h//2 + 4}" fill="{text_dim}" font-size="10" font-weight="600" text-anchor="middle" class="font-sketch">{lbl}</text>
  <text x="{mid_sep + (w - mid_sep)//2}" y="{h//2 + 4}" fill="{prim}" font-size="10.5" font-weight="700" text-anchor="middle" class="font-sketch">{val}</text>
</svg>"""

    else:
        text_clean = escape_xml(raw_text)
        text_w = measure_sans_text_width(text_clean, 10.5)
        calc_w = int(text_w + 36)
        w = width if width is not None else calc_w

        outer_rect = render_rough_rect(x=1, y=1, w=w-2, h=h-2, stroke=acc, stroke_width=1.3, fill=panel, rx=6, seed=195)
        doodle_icon = render_rough_star(cx=12, cy=h//2, r=3.2, fill=prim, stroke=prim, seed=197)

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
  <defs>
    <style>
      {css_vars}
{SKETCH_BASE_STYLES}
    </style>
{render_sketch_defs(c, "chipSketchSingle")}
  </defs>

  <!-- Sketch Single Badge -->
  {outer_rect}
  {doodle_icon}
  <text x="{w//2 + 5}" y="{h//2 + 4}" fill="{text_main}" font-size="10.5" font-weight="600" text-anchor="middle" class="font-sketch">{text_clean}</text>
</svg>"""

    validate_svg(svg)
    return svg


def generate_chip(style=None, primary=None, accent=None,
                  chip_type="closed", text="CHIP_LABEL", width=None, height=26, mode="auto", preset=None,
                  decay_dir="right", tertiary=None, theme=None):
    style_name, theme_name = normalize_style_and_theme(style=style, theme=theme)
    c, css_vars = resolve_theme(style=style_name, theme=theme_name, mode=mode, primary=primary, accent=accent, preset=preset, tertiary=tertiary)
    if style_name == "modern":
        return _generate_modern_chip(style_name=style_name, theme_name=theme_name, c=c, css_vars=css_vars, text=text, width=width, height=height)
    elif style_name == "sketch":
        return _generate_sketch_chip(style_name=style_name, theme_name=theme_name, c=c, css_vars=css_vars, text=text, width=width, height=height)
    prim = c["primary"]
    acc = c["accent"]
    bg = c["bg"]
    border = c["border"]
    panel = c["panel"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]


    text_clean = escape_xml(text)
    if theme_name in ("tactical", "amber", "amber_crt"):
        st = "tactical"
    elif theme_name in ("minimal", "clean-mono", "clean_mono", "academic-paper", "academic_paper", "corporate-blue", "corporate_blue", "tokyo", "tokyo_night", "swiss-mono", "swiss_mono", "executive-slate", "executive_slate"):
        st = "minimal"
    else:
        st = "cyberpunk"
    ct = chip_type.lower()
    dd = (decay_dir or "right").lower()
    if width is not None:
        text_clean = clamp_text_to_width(text_clean, max(20, width - 36), 10)
    text_w = estimate_chip_width(text_clean)

    if st == "tactical":
        if ct == "decay":
            if dd == "both":
                slash_zone = 26
                left_pad = slash_zone + 10
                right_pad = 10
                box_l = slash_zone + 2
                box_r = int(left_pad + text_w + right_pad)
                calc_w = box_r + slash_zone + 2
                w = width if width is not None else calc_w
                text_x = int(w / 2)
                l1_t, l1_b = 2, 2
                l2_t, l2_b = l1_t + 6, l1_b + 6
                l3_t, l3_b = l2_t + 6, l2_b + 6
                l4_t, l4_b = l3_t + 6, l3_b + 6
                r1_t, r1_b = box_r + 4, box_r + 4
                r2_t, r2_b = r1_t + 6, r1_b + 6
                r3_t, r3_b = r2_t + 6, r2_b + 6
                r4_t, r4_b = r3_t + 6, r3_b + 6
                svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {height}" width="{w}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
    </style>
  </defs>
  <polygon points="{box_l+5} 1, {box_r-5} 1, {box_r} 6, {box_r} 20, {box_r-5} 25, {box_l+5} 25, {box_l} 20, {box_l} 6" fill="{bg}"/>
  <polygon points="{box_l+5} 1, {box_r-5} 1, {box_r} 6, {box_r} 20, {box_r-5} 25, {box_l+5} 25, {box_l} 20, {box_l} 6" fill="{panel}" stroke="{prim}" stroke-width="1.5"/>
  <polygon points="{l1_t+3} 9, {l1_t+5} 9, {l1_b+3} 17, {l1_b+1} 17" fill="{prim}" opacity="0.2"/>
  <polygon points="{l2_t+2.5} 6, {l2_t+5} 6, {l2_b+2.5} 20, {l2_b} 20" fill="{prim}" opacity="0.4"/>
  <polygon points="{l3_t+3} 3, {l3_t+6} 3, {l3_b+3} 23, {l3_b} 23" fill="{prim}" opacity="0.65"/>
  <polygon points="{l4_t} 1, {l4_t+3.5} 1, {l4_b+3.5} 25, {l4_b} 25" fill="{prim}" opacity="0.9"/>
  <polygon points="{r1_t} 1, {r1_t+3.5} 1, {r1_b+3.5} 25, {r1_b} 25" fill="{prim}" opacity="0.9"/>
  <polygon points="{r2_t} 3, {r2_t+3} 3, {r2_b+3} 23, {r2_b} 23" fill="{prim}" opacity="0.65"/>
  <polygon points="{r3_t} 6, {r3_t+2.5} 6, {r3_b+2.5} 20, {r3_b} 20" fill="{prim}" opacity="0.4"/>
  <polygon points="{r4_t} 9, {r4_t+2} 9, {r4_b+2} 17, {r4_b} 17" fill="{prim}" opacity="0.2"/>
  <text x="{text_x}" y="17" fill="{prim}" text-anchor="middle" class="chip-text">{text_clean}</text>
</svg>"""
            elif dd == "left":
                slash_zone = 26
                left_pad = slash_zone + 14
                right_pad = 16
                box_l = slash_zone + 2
                calc_w = int(left_pad + text_w + right_pad)
                w = width if width is not None else calc_w
                text_x = left_pad + int(text_w / 2)
                l1_t, l1_b = 2, 2
                l2_t, l2_b = l1_t + 6, l1_b + 6
                l3_t, l3_b = l2_t + 6, l2_b + 6
                l4_t, l4_b = l3_t + 6, l3_b + 6
                svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {height}" width="{w}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
    </style>
  </defs>
  <polygon points="{box_l+5} 1, {w-8} 1, {w-2} 7, {w-2} 19, {w-8} 25, {box_l+5} 25, {box_l} 20, {box_l} 6" fill="{bg}"/>
  <polygon points="{box_l+5} 1, {w-8} 1, {w-2} 7, {w-2} 19, {w-8} 25, {box_l+5} 25, {box_l} 20, {box_l} 6" fill="{panel}" stroke="{prim}" stroke-width="1.5"/>
  <polygon points="{l1_t+3} 9, {l1_t+5} 9, {l1_b+3} 17, {l1_b+1} 17" fill="{prim}" opacity="0.2"/>
  <polygon points="{l2_t+2.5} 6, {l2_t+5} 6, {l2_b+2.5} 20, {l2_b} 20" fill="{prim}" opacity="0.4"/>
  <polygon points="{l3_t+3} 3, {l3_t+6} 3, {l3_b+3} 23, {l3_b} 23" fill="{prim}" opacity="0.65"/>
  <polygon points="{l4_t} 1, {l4_t+3.5} 1, {l4_b+3.5} 25, {l4_b} 25" fill="{prim}" opacity="0.9"/>
  <text x="{text_x}" y="17" fill="{prim}" text-anchor="middle" class="chip-text">{text_clean}</text>
</svg>"""
            elif dd == "left":
                # Tactical Hazard Slash Decay Left
                slash_zone = 26
                left_pad = slash_zone + 12
                right_pad = 16
                box_l = slash_zone + 2
                box_r = int(left_pad + text_w + right_pad)
                calc_w = box_r + 4
                w = width if width is not None else calc_w
                text_x = left_pad + int(text_w / 2)
                l1_t, l1_b = 2, 2
                l2_t, l2_b = l1_t + 6, l1_b + 6
                l3_t, l3_b = l2_t + 6, l2_b + 6
                l4_t, l4_b = l3_t + 6, l3_b + 6
                svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {height}" width="{w}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
    </style>
  </defs>
  <polygon points="{box_l+5} 1, {w-8} 1, {w-2} 7, {w-2} 19, {w-8} 25, {box_l+5} 25, {box_l} 20, {box_l} 6" fill="{bg}"/>
  <polygon points="{box_l+5} 1, {w-8} 1, {w-2} 7, {w-2} 19, {w-8} 25, {box_l+5} 25, {box_l} 20, {box_l} 6" fill="{panel}" stroke="{prim}" stroke-width="1.5"/>
  <polygon points="{l1_t+3} 9, {l1_t+5} 9, {l1_b+3} 17, {l1_b+1} 17" fill="{prim}" opacity="0.2"/>
  <polygon points="{l2_t+2.5} 6, {l2_t+5} 6, {l2_b+2.5} 20, {l2_b} 20" fill="{prim}" opacity="0.4"/>
  <polygon points="{l3_t+3} 3, {l3_t+6} 3, {l3_b+3} 23, {l3_b} 23" fill="{prim}" opacity="0.65"/>
  <polygon points="{l4_t} 1, {l4_t+3.5} 1, {l4_b+3.5} 25, {l4_b} 25" fill="{prim}" opacity="0.9"/>
  <polygon points="{w-14} 9, {w-9} 13, {w-14} 17" fill="{prim}"/>
  <text x="{text_x}" y="17" fill="{prim}" text-anchor="middle" class="chip-text">{text_clean}</text>
</svg>"""
            else:
                # Tactical Hazard Slash Decay Right (default)
                left_pad = 22  # Chamfer (7px) + arrow (8..13px) + padding
                right_pad = 14 # Padding before 45° slant
                box_bot_r = int(left_pad + text_w + right_pad)
                box_top_r = box_bot_r + 14
                s1_t, s1_b = box_top_r + 5, box_bot_r + 5
                s2_t, s2_b = s1_t + 9, s1_b + 9
                s3_t, s3_b = s2_t + 8, s2_b + 8
                s4_t, s4_b = s3_t + 8, s3_b + 8
                calc_w = s4_t + 6
                w = width if width is not None else calc_w
                text_x = left_pad + int(text_w / 2)

                svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {height}" width="{w}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
    </style>
  </defs>
  <polygon points="7 1, {box_top_r} 1, {box_bot_r} 25, 7 25, 1 19, 1 7" fill="{bg}"/>
  <polygon points="7 1, {box_top_r} 1, {box_bot_r} 25, 7 25, 1 19, 1 7" fill="{panel}" stroke="{prim}" stroke-width="1.5"/>
  <polygon points="8 13, 13 9, 13 17" fill="{prim}"/>
  <polygon points="{s1_t} 1, {s1_t+4} 1, {s1_b+4} 25, {s1_b} 25" fill="{prim}" opacity="0.9"/>
  <polygon points="{s2_t} 3, {s2_t+3.5} 3, {s2_b+3.5} 23, {s2_b} 23" fill="{prim}" opacity="0.65"/>
  <polygon points="{s3_t} 6, {s3_t+3} 6, {s3_b+3} 20, {s3_b} 20" fill="{prim}" opacity="0.4"/>
  <polygon points="{s4_t} 9, {s4_t+2} 9, {s4_b+2} 17, {s4_b} 17" fill="{prim}" opacity="0.2"/>
  <text x="{text_x}" y="17" fill="{prim}" text-anchor="middle" class="chip-text">{text_clean}</text>
</svg>"""
        elif ct == "pulse":
            # Tactical Targeting Reticle Pulse
            left_pad = 26  # Chamfer (7px) + reticle (cx=14, r=4.5) + padding
            right_pad = 16
            calc_w = int(left_pad + text_w + right_pad)
            w = width if width is not None else calc_w
            text_x = left_pad + int(text_w / 2)

            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {height}" width="{w}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
      @keyframes targetPulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.25; }} }}
      .laser {{ animation: targetPulse 1.2s infinite ease-in-out; }}
    </style>
  </defs>
  <polygon points="7 1, {w-8} 1, {w-2} 7, {w-2} 19, {w-8} 25, 7 25, 1 19, 1 7" fill="{bg}"/>
  <polygon points="7 1, {w-8} 1, {w-2} 7, {w-2} 19, {w-8} 25, 7 25, 1 19, 1 7" fill="{panel}" stroke="{prim}" stroke-width="1.5"/>
  <circle cx="14" cy="13" r="4.5" fill="none" stroke="{prim}" stroke-width="1"/>
  <circle cx="14" cy="13" r="2.5" fill="{prim}" class="laser"/>
  <text x="{text_x}" y="17" fill="{prim}" text-anchor="middle" class="chip-text">{text_clean}</text>
</svg>"""
        else:
            # Tactical Closed 45° Chamfer
            left_pad = 24  # Chamfer + arrow (10..15) + padding
            right_pad = 16
            calc_w = int(left_pad + text_w + right_pad)
            w = width if width is not None else calc_w
            text_x = left_pad + int(text_w / 2)
            mid_x = int(w / 2)

            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {height}" width="{w}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
    </style>
  </defs>
  <polygon points="7 1, {w-8} 1, {w-2} 7, {w-2} 19, {w-8} 25, 7 25, 1 19, 1 7" fill="{bg}"/>
  <polygon points="7 1, {w-8} 1, {w-2} 7, {w-2} 19, {w-8} 25, 7 25, 1 19, 1 7" fill="{panel}" stroke="{prim}" stroke-width="1.5"/>
  <polygon points="{mid_x-2} 1, {mid_x+2} 1, {mid_x} 4" fill="{prim}"/>
  <polygon points="{mid_x-2} 25, {mid_x+2} 25, {mid_x} 22" fill="{prim}"/>
  <polygon points="10 13, 15 9, 15 17" fill="{prim}"/>
  <text x="{text_x}" y="17" fill="{prim}" text-anchor="middle" class="chip-text">{text_clean}</text>
</svg>"""

    elif st == "minimal":
        if ct == "decay":
            if dd == "both":
                dissolve_zone = 32
                box_l = dissolve_zone + 2
                left_pad = dissolve_zone + 14
                right_pad = 14
                box_r = int(left_pad + text_w + right_pad)
                calc_w = box_r + dissolve_zone + 4
                w = width if width is not None else calc_w
                text_x = int(w / 2)
                dash_start = box_l - 16
                dash_end = box_r + 16

                cl1, cl2, cl3, cl4 = box_l - 7, box_l - 14, box_l - 21, box_l - 28
                cr1, cr2, cr3, cr4 = box_r + 7, box_r + 14, box_r + 21, box_r + 28

                svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {height}" width="{w}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
    </style>
  </defs>
  <path d="M {box_r} 1 L {box_l} 1 L {box_l} 25 L {box_r} 25" fill="{bg}"/>
  <path d="M {box_r} 1 L {box_l} 1 L {box_l} 25 L {box_r} 25" fill="{panel}" stroke="{prim}" stroke-width="1"/>
  <line x1="{dash_start}" y1="1" x2="{box_l}" y2="1" stroke="{prim}" stroke-width="1" stroke-dasharray="2,3" opacity="0.6"/>
  <line x1="{dash_start}" y1="25" x2="{box_l}" y2="25" stroke="{prim}" stroke-width="1" stroke-dasharray="2,3" opacity="0.6"/>
  <line x1="{box_r}" y1="1" x2="{dash_end}" y2="1" stroke="{prim}" stroke-width="1" stroke-dasharray="2,3" opacity="0.6"/>
  <line x1="{box_r}" y1="25" x2="{dash_end}" y2="25" stroke="{prim}" stroke-width="1" stroke-dasharray="2,3" opacity="0.6"/>
  <g fill="{prim}">
    <circle cx="{cl1}" cy="6" r="1.2" opacity="0.8"/><circle cx="{cl1}" cy="11" r="1.2" opacity="0.8"/><circle cx="{cl1}" cy="15" r="1.2" opacity="0.8"/><circle cx="{cl1}" cy="20" r="1.2" opacity="0.8"/>
    <circle cx="{cl2}" cy="8" r="1.1" opacity="0.55"/><circle cx="{cl2}" cy="13" r="1.1" opacity="0.55"/><circle cx="{cl2}" cy="18" r="1.1" opacity="0.55"/>
    <circle cx="{cl3}" cy="10" r="1" opacity="0.35"/><circle cx="{cl3}" cy="16" r="1" opacity="0.35"/>
    <circle cx="{cl4}" cy="7" r="0.8" opacity="0.2"/><circle cx="{cl4}" cy="14" r="0.8" opacity="0.2"/>
    <circle cx="{cr1}" cy="6" r="1.2" opacity="0.8"/><circle cx="{cr1}" cy="11" r="1.2" opacity="0.8"/><circle cx="{cr1}" cy="15" r="1.2" opacity="0.8"/><circle cx="{cr1}" cy="20" r="1.2" opacity="0.8"/>
    <circle cx="{cr2}" cy="8" r="1.1" opacity="0.55"/><circle cx="{cr2}" cy="13" r="1.1" opacity="0.55"/><circle cx="{cr2}" cy="18" r="1.1" opacity="0.55"/>
    <circle cx="{cr3}" cy="10" r="1" opacity="0.35"/><circle cx="{cr3}" cy="16" r="1" opacity="0.35"/>
    <circle cx="{cr4}" cy="7" r="0.8" opacity="0.2"/><circle cx="{cr4}" cy="14" r="0.8" opacity="0.2"/>
  </g>
  <text x="{text_x}" y="17" fill="{prim}" text-anchor="middle" class="chip-text">{text_clean}</text>
</svg>"""
            elif dd == "left":
                dissolve_zone = 32
                box_l = dissolve_zone + 2
                left_pad = dissolve_zone + 14
                right_pad = 16
                box_r = int(left_pad + text_w + right_pad)
                calc_w = box_r + 4
                w = width if width is not None else calc_w
                text_x = left_pad + int(text_w / 2)
                dash_start = box_l - 16
                cl1, cl2, cl3, cl4 = box_l - 7, box_l - 14, box_l - 21, box_l - 28

                svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {height}" width="{w}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
    </style>
  </defs>
  <path d="M {box_l} 1 L {w-2} 1 L {w-2} 25 L {box_l} 25" fill="{bg}"/>
  <path d="M {box_l} 1 L {w-2} 1 L {w-2} 25 L {box_l} 25" fill="{panel}" stroke="{prim}" stroke-width="1"/>
  <line x1="{dash_start}" y1="1" x2="{box_l}" y2="1" stroke="{prim}" stroke-width="1" stroke-dasharray="2,3" opacity="0.6"/>
  <line x1="{dash_start}" y1="25" x2="{box_l}" y2="25" stroke="{prim}" stroke-width="1" stroke-dasharray="2,3" opacity="0.6"/>
  <path d="M {w-5} 8 L {w-5} 4 L {w-9} 4" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <path d="M {w-5} 18 L {w-5} 22 L {w-9} 22" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <g fill="{prim}">
    <circle cx="{cl1}" cy="6" r="1.2" opacity="0.8"/><circle cx="{cl1}" cy="11" r="1.2" opacity="0.8"/><circle cx="{cl1}" cy="15" r="1.2" opacity="0.8"/><circle cx="{cl1}" cy="20" r="1.2" opacity="0.8"/>
    <circle cx="{cl2}" cy="8" r="1.1" opacity="0.55"/><circle cx="{cl2}" cy="13" r="1.1" opacity="0.55"/><circle cx="{cl2}" cy="18" r="1.1" opacity="0.55"/>
    <circle cx="{cl3}" cy="10" r="1" opacity="0.35"/><circle cx="{cl3}" cy="16" r="1" opacity="0.35"/>
    <circle cx="{cl4}" cy="7" r="0.8" opacity="0.2"/><circle cx="{cl4}" cy="14" r="0.8" opacity="0.2"/>
  </g>
  <text x="{text_x}" y="17" fill="{prim}" text-anchor="middle" class="chip-text">{text_clean}</text>
</svg>"""
            else:
                # Minimal Glass Micro-Stipple Dissolution Right (default)
                left_pad = 16  # Corner bracket (4..8) + padding
                right_pad = 14
                box_r = int(left_pad + text_w + right_pad)
                dash_end = box_r + 16
                c1, c2, c3, c4 = box_r + 7, box_r + 14, box_r + 21, box_r + 28
                calc_w = box_r + 34
                w = width if width is not None else calc_w
                text_x = left_pad + int(text_w / 2)

                svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {height}" width="{w}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
    </style>
  </defs>
  <path d="M {box_r} 1 L 1 1 L 1 25 L {box_r} 25" fill="{bg}"/>
  <path d="M {box_r} 1 L 1 1 L 1 25 L {box_r} 25" fill="{panel}" stroke="{prim}" stroke-width="1"/>
  <path d="M 4 8 L 4 4 L 8 4" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <path d="M 4 18 L 4 22 L 8 22" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <line x1="{box_r}" y1="1" x2="{dash_end}" y2="1" stroke="{prim}" stroke-width="1" stroke-dasharray="2,3" opacity="0.6"/>
  <line x1="{box_r}" y1="25" x2="{dash_end}" y2="25" stroke="{prim}" stroke-width="1" stroke-dasharray="2,3" opacity="0.6"/>
  <g fill="{prim}">
    <circle cx="{c1}" cy="6" r="1.2" opacity="0.8"/><circle cx="{c1}" cy="11" r="1.2" opacity="0.8"/><circle cx="{c1}" cy="15" r="1.2" opacity="0.8"/><circle cx="{c1}" cy="20" r="1.2" opacity="0.8"/>
    <circle cx="{c2}" cy="8" r="1.1" opacity="0.55"/><circle cx="{c2}" cy="13" r="1.1" opacity="0.55"/><circle cx="{c2}" cy="18" r="1.1" opacity="0.55"/>
    <circle cx="{c3}" cy="10" r="1" opacity="0.35"/><circle cx="{c3}" cy="16" r="1" opacity="0.35"/>
    <circle cx="{c4}" cy="7" r="0.8" opacity="0.2"/><circle cx="{c4}" cy="14" r="0.8" opacity="0.2"/>
  </g>
  <text x="{text_x}" y="17" fill="{prim}" text-anchor="middle" class="chip-text">{text_clean}</text>
</svg>"""
        elif ct == "pulse":
            # Minimal Glass Breathing Beacon
            left_pad = 26  # Beacon cx=15, r=3 + padding
            right_pad = 16
            calc_w = int(left_pad + text_w + right_pad)
            w = width if width is not None else calc_w
            text_x = left_pad + int(text_w / 2)

            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {height}" width="{w}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
      @keyframes breatheBeacon {{ 0%, 100% {{ opacity: 0.95; }} 50% {{ opacity: 0.25; }} }}
      .breathe {{ animation: breatheBeacon 2s infinite ease-in-out; }}
    </style>
  </defs>
  <rect x="1" y="1" width="{w-2}" height="{height-2}" fill="{bg}"/>
  <rect x="1" y="1" width="{w-2}" height="{height-2}" fill="{panel}" stroke="{prim}" stroke-width="1"/>
  <path d="M 4 8 L 4 4 L 8 4" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <path d="M {w-4} 8 L {w-4} 4 L {w-8} 4" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <path d="M 4 18 L 4 22 L 8 22" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <path d="M {w-4} 18 L {w-4} 22 L {w-8} 22" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <circle cx="15" cy="13" r="3" fill="{prim}" class="breathe"/>
  <text x="{text_x}" y="17" fill="{prim}" text-anchor="middle" class="chip-text">{text_clean}</text>
</svg>"""
        else:
            # Minimal Glass Closed Hairline
            left_pad = 24  # Dot cx=15 + padding
            right_pad = 16
            calc_w = int(left_pad + text_w + right_pad)
            w = width if width is not None else calc_w
            text_x = left_pad + int(text_w / 2)

            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {height}" width="{w}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
    </style>
  </defs>
  <rect x="1" y="1" width="{w-2}" height="{height-2}" fill="{bg}"/>
  <rect x="1" y="1" width="{w-2}" height="{height-2}" fill="{panel}" stroke="{prim}" stroke-width="1"/>
  <path d="M 4 8 L 4 4 L 8 4" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <path d="M {w-4} 8 L {w-4} 4 L {w-8} 4" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <path d="M 4 18 L 4 22 L 8 22" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <path d="M {w-4} 18 L {w-4} 22 L {w-8} 22" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <circle cx="15" cy="13" r="2" fill="{prim}"/>
  <text x="{text_x}" y="17" fill="{prim}" text-anchor="middle" class="chip-text">{text_clean}</text>
</svg>"""

    else:
        # Cyberpunk Chips
        if ct == "decay":
            if dd == "both":
                dither_zone = 26
                box_l = dither_zone + 2
                left_pad = dither_zone + 12
                right_pad = 12
                box_r = int(left_pad + text_w + right_pad)
                calc_w = box_r + dither_zone + 4
                w = width if width is not None else calc_w
                text_x = int(w / 2)

                dl1, dl2, dl3, dl4, dl5 = box_l - 2, box_l - 8, box_l - 14, box_l - 20, box_l - 24
                dr1, dr2, dr3, dr4, dr5 = box_r + 2, box_r + 8, box_r + 14, box_r + 20, box_r + 24

                svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {height}" width="{w}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
    </style>
  </defs>
  <path d="M {box_r} 1 L {box_l} 1 L {box_l} 25 L {box_r} 25" fill="{bg}"/>
  <path d="M {box_r} 1 L {box_l} 1 L {box_l} 25 L {box_r} 25" fill="{panel}" stroke="{prim}" stroke-width="1.5"/>
  <g fill="{prim}">
    <!-- Left Dither -->
    <rect x="{dl1-3}" y="3" width="3" height="3"/><rect x="{dl1-3}" y="9" width="3" height="3"/><rect x="{dl1-3}" y="15" width="3" height="3"/><rect x="{dl1-3}" y="20" width="3" height="3"/>
    <rect x="{dl2-2}" y="5" width="2" height="2"/><rect x="{dl2-2}" y="12" width="2" height="2"/><rect x="{dl2-2}" y="18" width="2" height="2"/>
    <rect x="{dl3-2}" y="7" width="2" height="2" opacity="0.7"/><rect x="{dl3-2}" y="15" width="2" height="2" opacity="0.7"/>
    <rect x="{dl4-1.5}" y="10" width="1.5" height="1.5" opacity="0.45"/><rect x="{dl5-1}" y="6" width="1" height="1" opacity="0.3"/>
    <!-- Right Dither -->
    <rect x="{dr1}" y="3" width="3" height="3"/><rect x="{dr1}" y="9" width="3" height="3"/><rect x="{dr1}" y="15" width="3" height="3"/><rect x="{dr1}" y="20" width="3" height="3"/>
    <rect x="{dr2}" y="5" width="2" height="2"/><rect x="{dr2}" y="12" width="2" height="2"/><rect x="{dr2}" y="18" width="2" height="2"/>
    <rect x="{dr3}" y="7" width="2" height="2" opacity="0.7"/><rect x="{dr3}" y="15" width="2" height="2" opacity="0.7"/>
    <rect x="{dr4}" y="10" width="1.5" height="1.5" opacity="0.45"/><rect x="{dr5}" y="6" width="1" height="1" opacity="0.3"/>
  </g>
  <text x="{text_x}" y="17" fill="{prim}" text-anchor="middle" class="chip-text">{text_clean}</text>
</svg>"""
            elif dd == "left":
                dither_zone = 26
                box_l = dither_zone + 2
                left_pad = dither_zone + 12
                right_pad = 18
                box_r = int(left_pad + text_w + right_pad)
                calc_w = box_r + 4
                w = width if width is not None else calc_w
                text_x = left_pad + int(text_w / 2)
                dl1, dl2, dl3, dl4, dl5 = box_l - 2, box_l - 8, box_l - 14, box_l - 20, box_l - 24

                svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {height}" width="{w}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
    </style>
  </defs>
  <path d="M {box_l} 1 L {w-2} 1 L {w-2} 25 L {box_l} 25" fill="{bg}"/>
  <path d="M {box_l} 1 L {w-2} 1 L {w-2} 25 L {box_l} 25" fill="{panel}" stroke="{prim}" stroke-width="1.5"/>
  <rect x="{w-4}" y="1" width="3" height="3" fill="{prim}"/>
  <rect x="{w-4}" y="22" width="3" height="3" fill="{prim}"/>
  <rect x="{w-10}" y="8" width="3" height="10" fill="{prim}"/>
  <g fill="{prim}">
    <rect x="{dl1-3}" y="3" width="3" height="3"/><rect x="{dl1-3}" y="9" width="3" height="3"/><rect x="{dl1-3}" y="15" width="3" height="3"/><rect x="{dl1-3}" y="20" width="3" height="3"/>
    <rect x="{dl2-2}" y="5" width="2" height="2"/><rect x="{dl2-2}" y="12" width="2" height="2"/><rect x="{dl2-2}" y="18" width="2" height="2"/>
    <rect x="{dl3-2}" y="7" width="2" height="2" opacity="0.7"/><rect x="{dl3-2}" y="15" width="2" height="2" opacity="0.7"/>
    <rect x="{dl4-1.5}" y="10" width="1.5" height="1.5" opacity="0.45"/><rect x="{dl5-1}" y="6" width="1" height="1" opacity="0.3"/>
  </g>
  <text x="{text_x}" y="17" fill="{prim}" text-anchor="middle" class="chip-text">{text_clean}</text>
</svg>"""
            else:
                # Pixel Matrix Dither Decay Right (default)
                left_pad = 18  # Corner pixels + vertical bar (7..10) + padding
                right_pad = 14
                box_r = int(left_pad + text_w + right_pad)
                d1, d2, d3, d4, d5 = box_r + 2, box_r + 8, box_r + 14, box_r + 20, box_r + 24
                calc_w = box_r + 28
                w = width if width is not None else calc_w
                text_x = left_pad + int(text_w / 2)

                svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {height}" width="{w}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
    </style>
  </defs>
  <path d="M {box_r} 1 L 1 1 L 1 25 L {box_r} 25" fill="{bg}"/>
  <path d="M {box_r} 1 L 1 1 L 1 25 L {box_r} 25" fill="{panel}" stroke="{prim}" stroke-width="1.5"/>
  <rect x="1" y="1" width="3" height="3" fill="{prim}"/>
  <rect x="1" y="22" width="3" height="3" fill="{prim}"/>
  <rect x="7" y="8" width="3" height="10" fill="{prim}"/>
  <g fill="{prim}">
    <rect x="{d1}" y="3" width="3" height="3"/><rect x="{d1}" y="9" width="3" height="3"/><rect x="{d1}" y="15" width="3" height="3"/><rect x="{d1}" y="20" width="3" height="3"/>
    <rect x="{d2}" y="5" width="2" height="2"/><rect x="{d2}" y="12" width="2" height="2"/><rect x="{d2}" y="18" width="2" height="2"/>
    <rect x="{d3}" y="7" width="2" height="2" opacity="0.7"/><rect x="{d3}" y="15" width="2" height="2" opacity="0.7"/>
    <rect x="{d4}" y="10" width="1.5" height="1.5" opacity="0.45"/><rect x="{d5}" y="6" width="1" height="1" opacity="0.3"/>
  </g>
  <text x="{text_x}" y="17" fill="{prim}" text-anchor="middle" class="chip-text">{text_clean}</text>
</svg>"""
        elif ct == "pulse":
            # Cyberpunk Blinking Square LED Beacon
            left_pad = 25  # LED cx=14, r=3.5 + padding
            right_pad = 16
            calc_w = int(left_pad + text_w + right_pad)
            w = width if width is not None else calc_w
            text_x = left_pad + int(text_w / 2)

            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {height}" width="{w}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
      @keyframes blinkLed {{ 0%, 100% {{ fill: {prim}; opacity: 1; }} 50% {{ fill: {border}; opacity: 0.3; }} }}
      .led {{ animation: blinkLed 1.4s infinite steps(1); }}
    </style>
  </defs>
  <rect x="1" y="1" width="{w-2}" height="{height-2}" fill="{bg}"/>
  <rect x="1" y="1" width="{w-2}" height="{height-2}" fill="{panel}" stroke="{prim}" stroke-width="1.5"/>
  <rect x="1" y="1" width="3" height="3" fill="{prim}"/>
  <rect x="{w-4}" y="1" width="3" height="3" fill="{acc}"/>
  <rect x="1" y="{height-4}" width="3" height="3" fill="{acc}"/>
  <rect x="{w-4}" y="{height-4}" width="3" height="3" fill="{prim}"/>
  <circle cx="14" cy="13" r="3.5" fill="{prim}" class="led"/>
  <text x="{text_x}" y="17" fill="{prim}" text-anchor="middle" class="chip-text">{text_clean}</text>
</svg>"""
        else:
            # Cyberpunk Closed Corner Pixels
            left_pad = 22  # Corner pixels + bar (8..12) + padding
            right_pad = 16
            calc_w = int(left_pad + text_w + right_pad)
            w = width if width is not None else calc_w
            text_x = left_pad + int(text_w / 2)

            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {height}" width="{w}" height="{height}" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .chip-text {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; letter-spacing: 0.5px; }}
    </style>
  </defs>
  <rect x="1" y="1" width="{w-2}" height="{height-2}" fill="{bg}"/>
  <rect x="1" y="1" width="{w-2}" height="{height-2}" fill="{panel}" stroke="{prim}" stroke-width="1.5"/>
  <rect x="1" y="1" width="3" height="3" fill="{prim}"/>
  <rect x="{w-4}" y="1" width="3" height="3" fill="{prim}"/>
  <rect x="1" y="{height-4}" width="3" height="3" fill="{prim}"/>
  <rect x="{w-4}" y="{height-4}" width="3" height="3" fill="{prim}"/>
  <rect x="8" y="8" width="4" height="10" fill="{prim}"/>
  <text x="{text_x}" y="17" fill="{prim}" text-anchor="middle" class="chip-text">{text_clean}</text>
</svg>"""

    validate_svg(svg)
    return svg


