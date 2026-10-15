"""Timeline milestone components for Pixel Readme Kit."""
from typing import Optional, Any, List, Dict
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
    render_modern_defs,
    SKETCH_BASE_STYLES,
    render_sketch_defs,
    render_rough_line,
    render_rough_rect,
    render_rough_arrow,
    render_rough_star,
    coord_jitter,
)

def _generate_modern_timeline(style_name, theme_name, c, css_vars, items=None, milestones=None, width=850):
    """Renders a sleek vector milestone timeline with rounded cards, status pills, and continuous axis."""
    if items is None and milestones is not None:
        items = milestones
    if not items:
        items = [
            {"title": "PHASE 1: RESEARCH", "date": "2026-Q1", "status": "COMPLETED", "desc": "Initial prototype and vector specification"},
            {"title": "PHASE 2: CORE RUNTIME", "date": "2026-Q2", "status": "IN_PROGRESS", "desc": "Data visualization suite and multi-theming engine"},
            {"title": "PHASE 3: HUD STUDIO", "date": "2026-Q3", "status": "PLANNED", "desc": "Interactive web editor and production rollout"}
        ]

    prim = c["primary"]
    acc = c["accent"]
    panel = c["panel"]
    border = c["border"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]
    success = c["success"]

    step_h = 72
    k = len(items)
    total_h = 24 + k * step_h
    bus_x = 36
    bus_end_y = 38 + (k - 1) * step_h + 12

    milestones_svg = []
    for i, item in enumerate(items):
        node_y = 38 + i * step_h
        card_y = node_y - 24
        card_x = 64
        card_w = width - card_x - 12
        card_h = 54

        t = escape_xml(item.get("title", f"STAGE {i+1}"))
        d = escape_xml(item.get("date", "2026"))
        stat = str(item.get("status", "PLANNED")).upper()
        desc = escape_xml(item.get("desc", ""))

        if stat in ("COMPLETED", "DONE", "FINISHED"):
            stat_col = success
            stat_lbl = "COMPLETED"
            node_shape = f"""<circle cx="{bus_x}" cy="{node_y}" r="6.5" fill="{success}"/>
    <circle cx="{bus_x}" cy="{node_y}" r="9" fill="none" stroke="{success}" stroke-width="1.2" opacity="0.3"/>
    <path d="M {bus_x-2.5} {node_y} L {bus_x-0.5} {node_y+2} L {bus_x+3} {node_y-2}" fill="none" stroke="{c['bg']}" stroke-width="1.4" stroke-linecap="round"/>"""
        elif stat in ("IN_PROGRESS", "ACTIVE", "WIP"):
            stat_col = acc
            stat_lbl = "IN PROGRESS"
            node_shape = f"""<circle cx="{bus_x}" cy="{node_y}" r="6" fill="{acc}"/>
    <circle cx="{bus_x}" cy="{node_y}" r="10" fill="none" stroke="{acc}" stroke-width="1.2" stroke-dasharray="2 3"/>"""
        else:
            stat_col = text_dim
            stat_lbl = "PLANNED"
            node_shape = f'<circle cx="{bus_x}" cy="{node_y}" r="5" fill="{panel}" stroke="{border}" stroke-width="1.5"/>'

        # Connector trace
        conn = f'<line x1="{bus_x+10}" y1="{node_y}" x2="{card_x}" y2="{node_y}" stroke="{stat_col}" stroke-width="1.2" stroke-dasharray="2 2" opacity="0.6"/>'

        # Date pill badge
        d_disp = clamp_sans_text_to_width(d, 90, 10.5)
        dw = max(56, int(measure_sans_text_width(d_disp, 10.5) + 18))

        # Status badge pill
        stat_pill_w = max(74, int(measure_sans_text_width(stat_lbl, 10) + 24))

        # Title and description text
        avail_t_w = max(60, card_w - dw - stat_pill_w - 50)
        t_disp = clamp_sans_text_to_width(t, avail_t_w, 12.5)
        desc_disp = clamp_sans_text_to_width(desc, card_w - 28, 11)

        milestones_svg.append(f"""  <g id="modern-milestone-{i}">
    {conn}
    {node_shape}
    <rect x="{card_x}" y="{card_y}" width="{card_w}" height="{card_h}" rx="10" fill="{panel}" stroke="{border}" stroke-width="1"/>
    <rect x="{card_x}" y="{card_y+8}" width="3" height="{card_h-16}" rx="1.5" fill="{stat_col}"/>

    <!-- Date Pill -->
    <rect x="{card_x+12}" y="{card_y+9}" width="{dw}" height="18" rx="9" fill="{c['bg']}" stroke="{border}" stroke-width="0.8"/>
    <text x="{card_x+12+dw//2}" y="{card_y+22}" fill="{text_dim}" font-size="10.5" font-weight="600" text-anchor="middle" class="font-sans">{d_disp}</text>

    <!-- Title -->
    <text x="{card_x+12+dw+10}" y="{card_y+23}" fill="{text_main}" font-size="12.5" font-weight="700" class="font-sans">{t_disp}</text>

    <!-- Status Pill -->
    <rect x="{card_x+card_w-stat_pill_w-12}" y="{card_y+9}" width="{stat_pill_w}" height="18" rx="9" fill="{c['bg']}" stroke="{stat_col}" stroke-width="0.8"/>
    <circle cx="{card_x+card_w-stat_pill_w-2}" y="{card_y+18}" r="2.5" fill="{stat_col}"/>
    <text x="{card_x+card_w-stat_pill_w+6}" y="{card_y+22}" fill="{stat_col}" font-size="10" font-weight="700" class="font-sans">{stat_lbl}</text>

    <!-- Description -->
    <text x="{card_x+14}" y="{card_y+42}" fill="{text_dim}" font-size="11" class="font-sans">{desc_disp}</text>
  </g>""")

    defs_markup = render_modern_defs(c, "modern-timeline")
    joined_milestones = "\n".join(milestones_svg)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {total_h}" width="100%" height="100%">
  <defs>
    {defs_markup}
    <style>
      {css_vars}
      {MODERN_BASE_STYLES}
    </style>
  </defs>

  <!-- Vertical Continuous Axis -->
  <line x1="{bus_x}" y1="20" x2="{bus_x}" y2="{bus_end_y}" stroke="url(#modern-timeline-border-grad)" stroke-width="2"/>
  <circle cx="{bus_x}" cy="20" r="3.5" fill="{prim}"/>
  <circle cx="{bus_x}" cy="{bus_end_y}" r="3.5" fill="{acc}"/>

{joined_milestones}
</svg>"""

    validate_svg(svg)
    return svg

def _generate_sketch_timeline(style_name, theme_name, c, css_vars, items=None, milestones=None, width=850):
    """Renders a hand-drawn sketch milestone timeline with wobbly spine, doodle markers, and rough cards."""
    if items is None and milestones is not None:
        items = milestones
    if not items:
        items = [
            {"title": "PHASE 1: RESEARCH", "date": "2026-Q1", "status": "COMPLETED", "desc": "Initial prototype and vector specification"},
            {"title": "PHASE 2: CORE RUNTIME", "date": "2026-Q2", "status": "IN_PROGRESS", "desc": "Data visualization suite and multi-theming engine"},
            {"title": "PHASE 3: HUD STUDIO", "date": "2026-Q3", "status": "PLANNED", "desc": "Interactive web editor and production rollout"}
        ]

    prim = c["primary"]
    acc = c["accent"]
    tertiary_col = c["tertiary"]
    panel = c["panel"]
    border = c["border"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]
    success = c["success"]
    bg = c["bg"]

    step_h = 76
    k = len(items)
    total_h = 28 + k * step_h
    bus_x = 36
    bus_end_y = 38 + (k - 1) * step_h + 16

    # Spine line with wobbly jitter and arrow
    bus_line = render_rough_line(bus_x, 16, bus_x, bus_end_y, stroke=border, stroke_width=2.0, seed=15, jitter=1.0)
    bus_arrow = render_rough_arrow(bus_x, bus_end_y - 6, bus_x, bus_end_y + 8, stroke=prim, stroke_width=1.8, seed=17)

    milestones_svg = []
    for i, item in enumerate(items):
        node_y = 38 + i * step_h
        card_y = node_y - 25
        card_x = 64
        card_w = width - card_x - 14
        card_h = 56

        t = escape_xml(item.get("title", f"STAGE {i+1}"))
        d = escape_xml(item.get("date", "2026"))
        stat = str(item.get("status", "PLANNED")).upper()
        desc = escape_xml(item.get("desc", ""))

        if stat in ("COMPLETED", "DONE", "FINISHED"):
            stat_col = success
            stat_lbl = "COMPLETED"
            node_shape = f"""<circle cx="{bus_x}" cy="{node_y}" r="6.5" fill="{success}"/>
    <circle cx="{bus_x}" cy="{node_y}" r="9.5" fill="none" stroke="{success}" stroke-width="1.2" opacity="0.4"/>
    <path d="M {bus_x-3} {node_y} L {bus_x-0.5} {node_y+2.5} L {bus_x+3.5} {node_y-2.5}" fill="none" stroke="{bg}" stroke-width="1.6" stroke-linecap="round"/>"""
        elif stat in ("IN_PROGRESS", "ACTIVE", "WIP"):
            stat_col = acc
            stat_lbl = "IN PROGRESS"
            node_shape = render_rough_star(bus_x, node_y, r=8, fill=acc, stroke=acc, seed=i*13 + 5)
        else:
            stat_col = text_dim
            stat_lbl = "PLANNED"
            node_shape = f'<circle cx="{bus_x}" cy="{node_y}" r="5" fill="{panel}" stroke="{border}" stroke-width="1.5"/>'

        # Connector trace from bus to card
        conn = render_rough_line(bus_x + 9, node_y, card_x, node_y, stroke=stat_col, stroke_width=1.2, seed=i*29 + 1, jitter=0.8)

        # Card rough box
        card_box = render_rough_rect(card_x, card_y, card_w, card_h, stroke=border, fill=panel, stroke_width=1.4, seed=i*41 + 9, overshoot=2)

        # Card left marker strip (highlighter stroke)
        strip = render_rough_line(card_x + 3, card_y + 4, card_x + 3, card_y + card_h - 4, stroke=stat_col, stroke_width=2.5, seed=i*53 + 3, jitter=0.6)

        # Date pill
        d_disp = clamp_sans_text_to_width(d, 90, 11)
        dw = max(58, int(measure_sans_text_width(d_disp, 11) + 20))
        date_box = render_rough_rect(card_x + 12, card_y + 8, dw, 18, stroke=border, fill=bg, stroke_width=1.0, seed=i*67 + 2, overshoot=1)

        # Status pill
        stat_pill_w = max(78, int(measure_sans_text_width(stat_lbl, 10.5) + 22))
        stat_box = render_rough_rect(card_x + card_w - stat_pill_w - 14, card_y + 8, stat_pill_w, 18, stroke=stat_col, fill=bg, stroke_width=1.0, seed=i*71 + 4, overshoot=1)

        # Title & desc
        avail_t_w = max(60, card_w - dw - stat_pill_w - 52)
        t_disp = clamp_sans_text_to_width(t, avail_t_w, 12.5)
        desc_disp = clamp_sans_text_to_width(desc, card_w - 28, 11.5)

        tape_markup = ""
        if i == 0:
            tape_markup = f'<polygon points="{card_x + 28} {card_y - 5}, {card_x + 58} {card_y - 5}, {card_x + 54} {card_y + 8}, {card_x + 24} {card_y + 8}" fill="url(#timelineSketch-tape)"/>'

        milestones_svg.append(f"""  <g id="sketch-milestone-{i}">
    {conn}
    {node_shape}
    {card_box}
    {strip}
    {tape_markup}

    <!-- Date Pill -->
    {date_box}
    <text x="{card_x + 12 + dw//2}" y="{card_y + 21}" fill="{text_dim}" font-size="10.5" font-weight="600" text-anchor="middle" class="font-sketch">{d_disp}</text>

    <!-- Title -->
    <text x="{card_x + 12 + dw + 10}" y="{card_y + 22}" fill="{prim}" font-size="12.5" font-weight="700" class="font-sketch">{t_disp}</text>

    <!-- Status Pill -->
    {stat_box}
    <text x="{card_x + card_w - stat_pill_w//2 - 14}" y="{card_y + 21}" fill="{stat_col}" font-size="10" font-weight="700" text-anchor="middle" class="font-sketch">{stat_lbl}</text>

    <!-- Description -->
    <text x="{card_x + 14}" y="{card_y + 43}" fill="{text_dim}" font-size="11.5" class="font-sketch">{desc_disp}</text>
  </g>""")

    joined_milestones = "\n".join(milestones_svg)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {total_h}" width="100%" height="100%">
  <defs>
    {render_sketch_defs(c, "timelineSketch")}
    <style>
      {css_vars}
      {SKETCH_BASE_STYLES}
    </style>
  </defs>

  <!-- Vertical Continuous Sketch Axis -->
  {bus_line}
  {bus_arrow}

{joined_milestones}
</svg>"""

    validate_svg(svg)
    return svg

def generate_timeline(items=None, milestones=None, style=None, primary=None, accent=None, mode="auto", preset=None, width=850, tertiary=None, theme=None):
    """
    Renders a vertical PCB data bus timeline with milestones and status nodes.
    items / milestones: list of dicts with: title, date, status ("COMPLETED"|"IN_PROGRESS"|"PLANNED"), desc
    """
    if items is None and milestones is not None:
        items = milestones
    style_name, theme_name = normalize_style_and_theme(style=style, theme=theme)
    c, css_vars = resolve_theme(style=style_name, theme=theme_name, mode=mode, primary=primary, accent=accent, preset=preset, tertiary=tertiary)
    if style_name == "modern":
        return _generate_modern_timeline(style_name=style_name, theme_name=theme_name, c=c, css_vars=css_vars, items=items, milestones=milestones, width=width)
    elif style_name == "sketch":
        return _generate_sketch_timeline(style_name=style_name, theme_name=theme_name, c=c, css_vars=css_vars, items=items, milestones=milestones, width=width)
    prim = c["primary"]
    acc = c["accent"]
    panel = c["panel"]
    border = c["border"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]
    title_front = c["title_front"]
    success = c["success"]
    if theme_name in ("tactical", "amber", "amber_crt"):
        st = "tactical"
    elif theme_name in ("minimal", "clean-mono", "clean_mono", "academic-paper", "academic_paper", "corporate-blue", "corporate_blue", "tokyo", "tokyo_night", "swiss-mono", "swiss_mono", "executive-slate", "executive_slate"):
        st = "minimal"
    else:
        st = "cyberpunk"

    if not items:
        items = [
            {"title": "PHASE 1: RESEARCH", "date": "2026-Q1", "status": "COMPLETED", "desc": "Initial prototype and vector specification"},
            {"title": "PHASE 2: CORE RUNTIME", "date": "2026-Q2", "status": "IN_PROGRESS", "desc": "Data visualization suite and multi-theming engine"},
            {"title": "PHASE 3: HUD STUDIO", "date": "2026-Q3", "status": "PLANNED", "desc": "Interactive web editor and production rollout"}
        ]

    step_h = 66
    k = len(items)
    total_h = 16 + k * step_h
    bus_x = 42

    milestones_svg = []
    for i, item in enumerate(items):
        node_y = 28 + i * step_h
        card_y = node_y - 18
        card_x = 70
        card_w = width - 72
        card_h = 52

        t = escape_xml(item.get("title", f"STAGE {i+1}").upper())
        d = escape_xml(item.get("date", "2026"))
        stat = str(item.get("status", "PLANNED")).upper()
        desc = escape_xml(item.get("desc", ""))

        if stat in ("COMPLETED", "DONE", "FINISHED"):
            node_col = success
            node_shape = f'<polygon points="{bus_x},{node_y-6} {bus_x+6},{node_y} {bus_x},{node_y+6} {bus_x-6},{node_y}" fill="{success}"/>'
            stat_lbl = "● COMPLETED"
        elif stat in ("IN_PROGRESS", "ACTIVE", "WIP"):
            node_col = acc
            node_shape = f"""<circle cx="{bus_x}" cy="{node_y}" r="6" fill="{acc}"/>
    <circle cx="{bus_x}" cy="{node_y}" r="10" fill="none" stroke="{acc}" stroke-width="1.2" stroke-dasharray="2 2"/>"""
            stat_lbl = "◉ IN_PROGRESS"
        else:
            node_col = text_dim
            node_shape = f'<circle cx="{bus_x}" cy="{node_y}" r="5" fill="{panel}" stroke="{border}" stroke-width="1.5"/>'
            stat_lbl = "○ PLANNED"

        # Connector trace from bus to card
        conn = f'<path d="M {bus_x+6} {node_y} L {card_x} {node_y}" stroke="{node_col}" stroke-width="1.5" stroke-dasharray="3 2"/>'

        # Card hull
        if st == "tactical":
            c_hull = f"""<polygon points="{card_x+6},{card_y} {card_x+card_w},{card_y} {card_x+card_w},{card_y+card_h-6} {card_x+card_w-6},{card_y+card_h} {card_x},{card_y+card_h} {card_x},{card_y+6}" fill="{panel}" stroke="{border}" stroke-width="1.2"/>
    <line x1="{card_x+1}" y1="{card_y+1}" x2="{card_x+1}" y2="{card_y+card_h-1}" stroke="{node_col}" stroke-width="2.5"/>"""
        elif st == "minimal":
            c_hull = f"""<rect x="{card_x}" y="{card_y}" width="{card_w}" height="{card_h}" fill="{panel}" stroke="{border}" stroke-width="1"/>
    <line x1="{card_x}" y1="{card_y}" x2="{card_x}" y2="{card_y+card_h}" stroke="{node_col}" stroke-width="2"/>"""
        else:  # cyberpunk
            c_hull = f"""<rect x="{card_x}" y="{card_y}" width="{card_w}" height="{card_h}" fill="{panel}" stroke="{border}" stroke-width="1.2"/>
    <line x1="{card_x}" y1="{card_y}" x2="{card_x+8}" y2="{card_y}" stroke="{node_col}" stroke-width="2"/>
    <line x1="{card_x}" y1="{card_y}" x2="{card_x}" y2="{card_y+8}" stroke="{node_col}" stroke-width="2"/>
    <rect x="{card_x+card_w-5}" y="{card_y+2}" width="3" height="3" fill="{node_col}"/>"""

        # Dynamic date width and text clamps
        dw = max(60, min(130, int(measure_mono_text_width(d, 11) + 18)))
        max_title_w = max(60, card_w - dw - 165)
        t_disp = clamp_text_to_width(t, max_title_w, 12)
        desc_disp = clamp_text_to_width(desc, card_w - 28, 11)

        milestones_svg.append(f"""  <g id="milestone-{i}">
    {conn}
    {node_shape}
    {c_hull}
    <!-- Milestone Header -->
    <rect x="{card_x+12}" y="{card_y+9}" width="{dw}" height="14" fill="{panel}" stroke="{border}" stroke-width="1"/>
    <text x="{card_x+12 + dw//2}" y="{card_y+20}" fill="{text_dim}" text-anchor="middle" class="font-time-date">{d}</text>
    <text x="{card_x+12 + dw + 10}" y="{card_y+20}" fill="{title_front}" class="font-time-title">{t_disp}</text>
    <text x="{card_x+card_w-14}" y="{card_y+20}" fill="{node_col}" text-anchor="end" class="font-time-stat">{stat_lbl}</text>
    <!-- Milestone Description -->
    <text x="{card_x+14}" y="{card_y+40}" fill="{text_dim}" class="font-time-desc">{desc_disp}</text>
  </g>""")

    joined_nodes = "\n".join(milestones_svg)
    bus_end_y = 28 + (k - 1) * step_h + 10

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {total_h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-time-date {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 11px; font-weight: bold; }}
      .font-time-title {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 12px; font-weight: bold; }}
      .font-time-stat {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 11px; font-weight: bold; }}
      .font-time-desc {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 11px; font-weight: normal; }}
    </style>
  </defs>
  <!-- Vertical Data PCB Bus -->
  <line x1="{bus_x}" y1="14" x2="{bus_x}" y2="{bus_end_y}" stroke="{border}" stroke-width="2"/>
  <circle cx="{bus_x}" cy="14" r="3" fill="{prim}"/>
  <polygon points="{bus_x},{bus_end_y+6} {bus_x+4},{bus_end_y} {bus_x-4},{bus_end_y}" fill="{prim}"/>
{joined_nodes}
</svg>"""

    validate_svg(svg)
    return svg

# ==============================================================================
# SOCIAL PREVIEW CARDS (v4.0 - 1280x640 OpenGraph)
# ==============================================================================

