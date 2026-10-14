"""Metrics, progress and techstack components for Pixel Readme Kit."""
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
)


def _generate_modern_metrics(style_name, theme_name, c, css_vars, metrics=None, width=850):
    """Renders sleek vector KPI cards with large typography, pill badges and smooth sparklines."""
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

    if not metrics:
        metrics = [{"label": "SYSTEM METRIC", "value": "100%", "delta": "+0%", "trend": "neutral"}]

    card_list = metrics[:4]
    n = len(card_list)
    usable_w = width - 4
    gap = 14
    card_w = (usable_w - (n - 1) * gap) // n
    h = 96
    y = 3

    cards_svg = []
    for i, m in enumerate(card_list):
        x = 2 + i * (card_w + gap)
        label = escape_xml(m.get("label", f"METRIC {i+1}").upper())
        val = escape_xml(m.get("value") or m.get("val") or "--")
        delta = m.get("delta")
        trend = str(m.get("trend", "")).lower()
        status = m.get("status")

        if trend == "up":
            trend_col = success
            trend_icon = "↑ "
        elif trend == "down":
            trend_col = warning
            trend_icon = "↓ "
        else:
            trend_col = text_dim
            trend_icon = ""

        label_disp = clamp_sans_text_to_width(label, card_w - 32, 11)
        val_fs = 26 if len(val) <= 6 else (22 if len(val) <= 9 else 18)
        val_disp = clamp_sans_text_to_width(val, card_w - 32, val_fs)

        status_markup = ""
        if status:
            st_clean = escape_xml(status.upper())
            sw = min(card_w - 30, int(measure_sans_text_width(st_clean, 9) + 20))
            status_markup = f"""<g transform="translate({x + card_w - sw - 12}, {y + 12})">
      <rect x="0" y="0" width="{sw}" height="18" rx="9" fill="{panel}" stroke="{border}" stroke-width="1"/>
      <text x="{sw//2}" y="12" fill="{prim}" font-size="9" font-weight="600" text-anchor="middle" class="font-sans">{st_clean}</text>
    </g>"""

        delta_markup = ""
        if delta:
            d_clean = escape_xml(delta)
            d_disp = clamp_sans_text_to_width(f"{trend_icon}{d_clean}", card_w - 75, 10.5)
            delta_markup = f'<text x="{x+16}" y="{y+80}" fill="{trend_col}" font-size="10.5" font-weight="600" class="font-sans">{d_disp}</text>'

        sp_x = x + card_w - 56
        sp_y = y + 74
        sparkline = f"""<path d="M {sp_x} {sp_y+4} Q {sp_x+12} {sp_y-4} {sp_x+24} {sp_y} T {sp_x+44} {sp_y-6}" fill="none" stroke="{prim}" stroke-width="1.8" stroke-linecap="round" opacity="0.65"/>
    <circle cx="{sp_x+44}" cy="{sp_y-6}" r="2.5" fill="{acc}"/>"""

        cards_svg.append(f"""  <g id="metric-card-{i}">
    <rect x="{x}" y="{y}" width="{card_w}" height="{h}" rx="12" fill="{bg}" stroke="{border}" stroke-width="1.2"/>
    <text x="{x+16}" y="{y+25}" fill="{text_dim}" font-size="11" font-weight="600" class="font-sans">{label_disp}</text>
    {status_markup}
    <text x="{x+16}" y="{y+56}" fill="{text_main}" font-size="{val_fs}" font-weight="700" class="font-sans" letter-spacing="-0.5">{val_disp}</text>
    {delta_markup}
    {sparkline}
  </g>""")

    joined_cards = "\n".join(cards_svg)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h+6}" width="100%" height="100%">
  <defs>
    <style>
      {css_vars}
{MODERN_BASE_STYLES}
    </style>
  </defs>
{joined_cards}
</svg>"""

    validate_svg(svg)
    return svg


def _generate_modern_progress(style_name, theme_name, c, css_vars,
                              value=50, label="SYSTEM PROGRESS", sub=None, width=850):
    """Renders sleek continuous progress bar with gradient fill and pill badge."""
    prim = c["primary"]
    acc = c["accent"]
    tertiary_col = c["tertiary"]
    bg = c["bg"]
    panel = c["panel"]
    border = c["border"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]

    try:
        val_clean = max(0, min(100, int(round(float(value)))))
    except Exception:
        val_clean = 50

    lbl_clean = escape_xml(label)
    sub_raw = sub if sub is not None else f"RUNTIME PROGRESS // {val_clean}% COMPLETE"
    sub_clean = escape_xml(sub_raw)

    lbl_disp = clamp_sans_text_to_width(lbl_clean, width - 120, 12)
    sub_disp = clamp_sans_text_to_width(sub_clean, width - 200, 11)

    h = 72
    track_x = 18
    track_y = 34
    track_w = width - 36
    track_h = 10
    filled_w = max(0.0, track_w * (val_clean / 100.0))

    filled_bar = ""
    if filled_w > 0:
        filled_bar = f'<rect x="{track_x}" y="{track_y}" width="{filled_w:.1f}" height="{track_h}" rx="5" fill="url(#progGrad)"/>'

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%">
  <defs>
    <style>
      {css_vars}
{MODERN_BASE_STYLES}
    </style>
{render_modern_defs("progGrad", prim, acc, tertiary_col)}
  </defs>

  <!-- Modern Card Background -->
  <rect x="2" y="2" width="{width-4}" height="{h-4}" rx="12" fill="{bg}" stroke="{border}" stroke-width="1.2"/>

  <!-- Label & Percentage Pill -->
  <text x="18" y="22" fill="{text_main}" font-size="12" font-weight="600" class="font-sans">{lbl_disp}</text>
  <g transform="translate({width-76}, 9)">
    <rect x="0" y="0" width="58" height="20" rx="10" fill="{panel}" stroke="{border}" stroke-width="1"/>
    <text x="29" y="14" fill="{prim}" font-size="11" font-weight="700" text-anchor="middle" class="font-sans">{val_clean}%</text>
  </g>

  <!-- Continuous Track & Filled Bar -->
  <rect x="{track_x}" y="{track_y}" width="{track_w}" height="{track_h}" rx="5" fill="{panel}" stroke="{border}" stroke-width="1"/>
  {filled_bar}

  <!-- Subtext & Milestone Indicators -->
  <text x="18" y="58" fill="{text_dim}" font-size="11" font-weight="500" class="font-sans">{sub_disp}</text>
  <text x="{width-18}" y="58" fill="{text_dim}" font-size="11" font-weight="500" text-anchor="end" class="font-sans">0% • 50% • 100%</text>
</svg>"""

    validate_svg(svg)
    return svg


def _generate_modern_techstack(style_name, theme_name, c, css_vars, items=None, columns=5, width=850):
    """Renders sleek vector techstack card matrix with smooth rounded badges."""
    from generator.icons import get_tech_icon_svg
    prim = c["primary"]
    acc = c["accent"]
    bg = c["bg"]
    panel = c["panel"]
    border = c["border"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]

    if items is None:
        tech_list = ["python", "cpp", "rust", "docker", "git"]
    elif isinstance(items, str):
        tech_list = [x.strip() for x in items.split(",") if x.strip()]
    else:
        tech_list = list(items)

    cols = max(2, min(int(columns), 8))
    rows = (len(tech_list) + cols - 1) // cols

    usable_w = width - 4
    gap_x = 10
    gap_y = 10
    card_w = (usable_w - (cols - 1) * gap_x) // cols
    card_h = 42
    total_h = 12 + rows * (card_h + gap_y)

    items_svg = []
    for idx, item in enumerate(tech_list):
        r = idx // cols
        col = idx % cols
        x = 2 + col * (card_w + gap_x)
        y = 6 + r * (card_h + gap_y)

        if isinstance(item, dict):
            raw_name = str(item.get("name") or item.get("id") or item.get("icon") or "ITEM")
            icon_key = str(item.get("icon") or raw_name)
            sub_label = str(item.get("label", "")) if item.get("label") else None
        else:
            raw_name = str(item)
            icon_key = raw_name
            sub_label = None

        clean_name = escape_xml(raw_name.upper())
        icon_inner = get_tech_icon_svg(icon_key)

        label_markup = ""
        if sub_label:
            lbl_clean = escape_xml(sub_label.upper())
            lbl_disp = clamp_sans_text_to_width(lbl_clean, card_w // 2 - 10, 10)
            sub_w = measure_sans_text_width(lbl_disp, 10)
            max_name_w = max(40, card_w - 42 - int(sub_w) - 10)
            clean_disp = clamp_sans_text_to_width(clean_name, max_name_w, 11)
            label_markup = f'<text x="{x+card_w-10}" y="{y+26}" fill="{text_dim}" font-size="10" font-weight="500" text-anchor="end" class="font-sans">{lbl_disp}</text>'
        else:
            clean_disp = clamp_sans_text_to_width(clean_name, card_w - 44, 11)

        items_svg.append(f"""  <g id="tech-{idx}">
    <rect x="{x}" y="{y}" width="{card_w}" height="{card_h}" rx="8" fill="{panel}" stroke="{border}" stroke-width="1"/>
    <g transform="translate({x+10}, {y+11})" color="{prim}">
      {icon_inner}
    </g>
    <text x="{x+36}" y="{y+26}" fill="{text_main}" font-size="11" font-weight="600" class="font-sans">{clean_disp}</text>
    {label_markup}
  </g>""")

    joined_items = "\n".join(items_svg)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {total_h}" width="100%" height="100%">
  <defs>
    <style>
      {css_vars}
{MODERN_BASE_STYLES}
    </style>
  </defs>
{joined_items}
</svg>"""

    validate_svg(svg)
    return svg


def _generate_sketch_metrics(style_name, theme_name, c, css_vars, metrics=None, width=850):
    """Renders hand-drawn sketch KPI cards with wobbly borders and doodle sparklines."""
    prim = c["primary"]
    acc = c["accent"]
    tertiary_col = c.get("tertiary", "#FDE047")
    bg = c["bg"]
    panel = c["panel"]
    border = c["border"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]
    success = c["success"]
    warning = c["warning"]

    if not metrics:
        metrics = [{"label": "SYSTEM METRIC", "value": "100%", "delta": "+0%", "trend": "neutral"}]

    card_list = metrics[:4]
    n = len(card_list)
    usable_w = width - 4
    gap = 14
    card_w = (usable_w - (n - 1) * gap) // n
    h = 96
    y = 3

    cards_svg = []
    for i, m in enumerate(card_list):
        x = 2 + i * (card_w + gap)
        label = escape_xml(m.get("label", f"METRIC {i+1}").upper())
        val = escape_xml(m.get("value") or m.get("val") or "--")
        delta = m.get("delta")
        trend = str(m.get("trend", "")).lower()
        status = m.get("status")

        if trend == "up":
            trend_col = success
            trend_icon = "↑ "
        elif trend == "down":
            trend_col = warning
            trend_icon = "↓ "
        else:
            trend_col = text_dim
            trend_icon = ""

        label_disp = clamp_sans_text_to_width(label, card_w - 32, 11)
        val_fs = 26 if len(val) <= 6 else (22 if len(val) <= 9 else 18)
        val_disp = clamp_sans_text_to_width(val, card_w - 32, val_fs)

        card_hull = render_rough_rect(x=x, y=y, w=card_w, h=h, stroke=border, stroke_width=1.3, fill=bg, rx=6, seed=200 + i * 10)

        status_markup = ""
        if status:
            st_clean = escape_xml(status.upper())
            sw = min(card_w - 30, int(measure_sans_text_width(st_clean, 9) + 20))
            st_box = render_rough_rect(x=x + card_w - sw - 12, y=y + 10, w=sw, h=18, stroke=acc, stroke_width=1.0, fill=panel, rx=4, seed=220 + i)
            status_markup = f"""  {st_box}
  <text x="{x + card_w - sw//2 - 12}" y="{y + 22}" fill="{prim}" font-size="9" font-weight="600" text-anchor="middle" class="font-sketch">{st_clean}</text>"""

        delta_markup = ""
        if delta:
            d_clean = escape_xml(delta)
            d_disp = clamp_sans_text_to_width(f"{trend_icon}{d_clean}", card_w - 75, 10.5)
            delta_markup = f'<text x="{x+16}" y="{y+80}" fill="{trend_col}" font-size="10.5" font-weight="600" class="font-sketch">{d_disp}</text>'

        sp_x = x + card_w - 56
        sp_y = y + 74
        spark_l1 = render_rough_line(sp_x, sp_y + 4, sp_x + 18, sp_y - 2, stroke=prim, stroke_width=1.3, jitter=0.9, double_stroke=False, seed=230 + i)
        spark_l2 = render_rough_line(sp_x + 18, sp_y - 2, sp_x + 40, sp_y - 6, stroke=prim, stroke_width=1.3, jitter=0.9, double_stroke=False, seed=235 + i)
        spark_star = render_rough_star(cx=sp_x + 40, cy=sp_y - 6, r=3.0, fill=acc, stroke=acc, seed=240 + i)

        cards_svg.append(f"""  <g id="sketch-metric-{i}">
    {card_hull}
    <text x="{x+16}" y="{y+25}" fill="{text_dim}" font-size="11" font-weight="600" class="font-sketch">{label_disp}</text>
    {status_markup}
    <text x="{x+16}" y="{y+56}" fill="{text_main}" font-size="{val_fs}" font-weight="700" class="font-sketch">{val_disp}</text>
    {delta_markup}
    {spark_l1}
    {spark_l2}
    {spark_star}
  </g>""")

    joined_cards = "\n".join(cards_svg)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h+6}" width="100%" height="100%">
  <defs>
    <style>
      {css_vars}
{SKETCH_BASE_STYLES}
    </style>
{render_sketch_defs(c, "metricsSketch")}
  </defs>
{joined_cards}
</svg>"""

    validate_svg(svg)
    return svg


def _generate_sketch_progress(style_name, theme_name, c, css_vars,
                              value=50, label="SYSTEM PROGRESS", sub=None, width=850):
    """Renders hand-drawn sketch progress bar with pencil hatching ////// fill."""
    prim = c["primary"]
    acc = c["accent"]
    tertiary_col = c.get("tertiary", "#FDE047")
    bg = c["bg"]
    panel = c["panel"]
    border = c["border"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]

    try:
        val_clean = max(0, min(100, int(round(float(value)))))
    except Exception:
        val_clean = 50

    lbl_clean = escape_xml(label)
    sub_raw = sub if sub is not None else f"SKETCH RUNTIME // {val_clean}% COMPLETE"
    sub_clean = escape_xml(sub_raw)

    lbl_disp = clamp_sans_text_to_width(lbl_clean, width - 120, 12)
    sub_disp = clamp_sans_text_to_width(sub_clean, width - 200, 11)

    h = 76
    track_x = 18
    track_y = 34
    track_w = width - 36
    track_h = 12
    filled_w = max(0.0, track_w * (val_clean / 100.0))

    chassis = render_rough_rect(x=2, y=2, w=width-4, h=h-4, stroke=border, stroke_width=1.4, fill=bg, rx=6, seed=250)
    badge_box = render_rough_rect(x=width-76, y=10, w=58, h=20, stroke=acc, stroke_width=1.1, fill=panel, rx=4, seed=255)
    track_box = render_rough_rect(x=track_x, y=track_y, w=track_w, h=track_h, stroke=border, stroke_width=1.2, fill=panel, rx=4, seed=260)

    filled_bar = ""
    if filled_w > 0:
        edge_line = render_rough_line(track_x + filled_w, track_y, track_x + filled_w, track_y + track_h, stroke=prim, stroke_width=1.4, jitter=0.5, double_stroke=False, seed=265)
        filled_bar = f"""  <rect x="{track_x}" y="{track_y}" width="{filled_w:.1f}" height="{track_h}" rx="3" fill="url(#progSketch-hatch)"/>
  {edge_line}"""

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%">
  <defs>
    <style>
      {css_vars}
{SKETCH_BASE_STYLES}
    </style>
{render_sketch_defs(c, "progSketch")}
  </defs>

  <!-- Sketch Background Chassis -->
  {chassis}

  <!-- Label & Percentage Tag -->
  <text x="18" y="24" fill="{text_main}" font-size="12" font-weight="600" class="font-sketch">{lbl_disp}</text>
  <g>
    {badge_box}
    <text x="{width-47}" y="24" fill="{prim}" font-size="11" font-weight="700" text-anchor="middle" class="font-sketch">{val_clean}%</text>
  </g>

  <!-- Track & Hatch-Filled Bar -->
  {track_box}
{filled_bar}

  <!-- Subtext & Legend -->
  <text x="18" y="62" fill="{text_dim}" font-size="11" class="font-sketch">✏️ {sub_disp}</text>
  <text x="{width-18}" y="62" fill="{text_dim}" font-size="11" text-anchor="end" class="font-sketch">[0% — 100% draft]</text>
</svg>"""

    validate_svg(svg)
    return svg


def _generate_sketch_techstack(style_name, theme_name, c, css_vars, items=None, columns=5, width=850):
    """Renders hand-drawn sketch techstack matrix with rough card borders."""
    from generator.icons import get_tech_icon_svg
    prim = c["primary"]
    acc = c["accent"]
    bg = c["bg"]
    panel = c["panel"]
    border = c["border"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]

    if items is None:
        tech_list = ["python", "cpp", "rust", "docker", "git"]
    elif isinstance(items, str):
        tech_list = [x.strip() for x in items.split(",") if x.strip()]
    else:
        tech_list = list(items)

    cols = max(2, min(int(columns), 8))
    rows = (len(tech_list) + cols - 1) // cols

    usable_w = width - 4
    gap_x = 10
    gap_y = 10
    card_w = (usable_w - (cols - 1) * gap_x) // cols
    card_h = 42
    total_h = 12 + rows * (card_h + gap_y)

    items_svg = []
    for idx, item in enumerate(tech_list):
        r = idx // cols
        col = idx % cols
        x = 2 + col * (card_w + gap_x)
        y = 6 + r * (card_h + gap_y)

        if isinstance(item, dict):
            raw_name = str(item.get("name") or item.get("id") or item.get("icon") or "ITEM")
            icon_key = str(item.get("icon") or raw_name)
        else:
            raw_name = str(item)
            icon_key = raw_name

        icon_svg = get_tech_icon_svg(icon_key)
        box = render_rough_rect(x=x, y=y, w=card_w, h=card_h, stroke=border, stroke_width=1.2, fill=panel, rx=4, seed=280 + idx * 5)
        label = escape_xml(raw_name.upper())
        items_svg.append(f"""  <g id="tech-card-{idx}">
    {box}
    <g transform="translate({x+10}, {y+11})" color="{prim}">{icon_svg}</g>
    <text x="{x + 36}" y="{y + 26}" fill="{text_main}" font-size="11" font-weight="600" class="font-sketch">{label}</text>
  </g>""")

    joined_items = "\n".join(items_svg)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {total_h}" width="100%" height="100%">
  <defs>
    <style>
      {css_vars}
{SKETCH_BASE_STYLES}
    </style>
{render_sketch_defs(c, "techSketch")}
  </defs>
{joined_items}
</svg>"""

    validate_svg(svg)
    return svg


def generate_metrics(metrics=None, cards=None, style=None, primary=None, accent=None, mode="auto", preset=None, width=850, tertiary=None, theme=None):
    """
    Renders 1 to 4 metric KPI cards in a full-width SVG row.
    metrics / cards: list of dicts with: label, value, delta (optional), trend (optional), status (optional)
    """
    if metrics is None and cards is not None:
        metrics = cards
    style_name, theme_name = normalize_style_and_theme(style=style, theme=theme)
    c, css_vars = resolve_theme(style=style_name, theme=theme_name, mode=mode, primary=primary, accent=accent, preset=preset, tertiary=tertiary)
    if style_name == "modern":
        return _generate_modern_metrics(style_name=style_name, theme_name=theme_name, c=c, css_vars=css_vars, metrics=metrics, width=width)
    elif style_name == "sketch":
        return _generate_sketch_metrics(style_name=style_name, theme_name=theme_name, c=c, css_vars=css_vars, metrics=metrics, width=width)
    prim = c["primary"]
    acc = c["accent"]
    panel = c["panel"]
    border = c["border"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]
    title_front = c["title_front"]
    success = c["success"]
    warning = c["warning"]

    if theme_name in ("tactical", "amber", "amber_crt"):
        st = "tactical"
    elif theme_name in ("minimal", "clean-mono", "clean_mono", "academic-paper", "academic_paper", "corporate-blue", "corporate_blue", "tokyo", "tokyo_night", "swiss-mono", "swiss_mono", "executive-slate", "executive_slate"):
        st = "minimal"
    else:
        st = "cyberpunk"

    if not metrics:
        metrics = [{"label": "SYSTEM METRIC", "value": "100%", "delta": "+0%", "trend": "neutral"}]

    card_list = metrics[:4]
    n = len(card_list)
    usable_w = width - 2
    gap = 12
    card_w = (usable_w - (n - 1) * gap) // n
    h = 92
    y = 3

    cards_svg = []
    for i, m in enumerate(card_list):
        x = 1 + i * (card_w + gap)
        label = escape_xml(m.get("label", f"METRIC {i+1}").upper())
        val = escape_xml(m.get("value") or m.get("val") or "--")
        delta = m.get("delta")
        trend = str(m.get("trend", "")).lower()
        status = m.get("status")

        # Trend styling
        if trend == "up":
            trend_col = success
            trend_icon = "▲ "
        elif trend == "down":
            trend_col = warning
            trend_icon = "▼ "
        else:
            trend_col = text_dim
            trend_icon = "● " if delta else ""

        # Style-specific card hull
        if st == "tactical":
            hull = f"""
    <polygon points="{x+8},{y} {x+card_w},{y} {x+card_w},{y+h-8} {x+card_w-8},{y+h} {x},{y+h} {x},{y+8}" fill="{panel}" stroke="{border}" stroke-width="1.5"/>
    <polygon points="{x+card_w-12},{y+3} {x+card_w-3},{y+3} {x+card_w-3},{y+12}" fill="{acc}"/>
    <line x1="{x+10}" y1="{y+h-1}" x2="{x+card_w-10}" y2="{y+h-1}" stroke="{prim}" stroke-width="1.5" stroke-dasharray="4 2"/>
"""
        elif st == "minimal":
            hull = f"""
    <rect x="{x}" y="{y}" width="{card_w}" height="{h}" fill="{panel}" stroke="{border}" stroke-width="1"/>
    <line x1="{x}" y1="{y}" x2="{x+card_w}" y2="{y}" stroke="{prim}" stroke-width="2"/>
    <rect x="{x+card_w-6}" y="{y+6}" width="2" height="2" fill="{prim}"/>
"""
        else:  # cyberpunk
            hull = f"""
    <rect x="{x}" y="{y}" width="{card_w}" height="{h}" fill="{panel}" stroke="{border}" stroke-width="1.5"/>
    <line x1="{x}" y1="{y+8}" x2="{x}" y2="{y}" stroke="{prim}" stroke-width="2"/>
    <line x1="{x}" y1="{y}" x2="{x+8}" y2="{y}" stroke="{prim}" stroke-width="2"/>
    <line x1="{x+card_w-8}" y1="{y}" x2="{x+card_w}" y2="{y}" stroke="{prim}" stroke-width="2"/>
    <line x1="{x+card_w}" y1="{y}" x2="{x+card_w}" y2="{y+8}" stroke="{prim}" stroke-width="2"/>
    <line x1="{x}" y1="{y+h-8}" x2="{x}" y2="{y+h}" stroke="{prim}" stroke-width="2"/>
    <line x1="{x}" y1="{y+h}" x2="{x+8}" y2="{y+h}" stroke="{prim}" stroke-width="2"/>
    <line x1="{x+card_w-8}" y1="{y+h}" x2="{x+card_w}" y2="{y+h}" stroke="{prim}" stroke-width="2"/>
    <line x1="{x+card_w}" y1="{y+h-8}" x2="{x+card_w}" y2="{y+h}" stroke="{prim}" stroke-width="2"/>
    <rect x="{x+6}" y="{y+6}" width="2" height="2" fill="{acc}"/>
"""

        status_markup = ""
        if status:
            stat_clean = escape_xml(status.upper())
            stat_w = max(56, int(measure_mono_text_width(stat_clean, 10) + 16))
            status_markup = f"""<rect x="{x+card_w-stat_w-12}" y="{y+10}" width="{stat_w}" height="13" fill="{panel}" stroke="{acc}" stroke-width="1"/>
    <text x="{x+card_w-12-stat_w//2}" y="{y+20}" fill="{acc}" text-anchor="middle" class="font-mono-tag">{stat_clean}</text>"""
            label_disp = clamp_text_to_width(label, card_w - stat_w - 30, 11)
        else:
            label_disp = clamp_text_to_width(label, card_w - 28, 11)

        val_str = str(val)
        val_len = len(val_str)
        if val_len > 12:
            val_fs = 14
        elif val_len > 8:
            val_fs = 18
        elif val_len > 6:
            val_fs = 21
        else:
            val_fs = 26
        val_disp = clamp_text_to_width(val_str, card_w - 28, val_fs)

        delta_markup = ""
        if delta:
            d_clean = escape_xml(delta)
            d_disp = clamp_text_to_width(d_clean, card_w - 68, 11)
            delta_markup = f'<text x="{x+14}" y="{y+76}" fill="{trend_col}" class="font-mono-sub">{trend_icon}{d_disp}</text>'

        # Mini sparkline decoration in bottom right of card
        sp_x = x + card_w - 54
        sp_y = y + 74
        sparkline = f"""
    <path d="M {sp_x} {sp_y+4} L {sp_x+10} {sp_y-2} L {sp_x+20} {sp_y+6} L {sp_x+30} {sp_y-6} L {sp_x+40} {sp_y}" fill="none" stroke="{prim}" stroke-width="1.2" stroke-opacity="0.4"/>
    <circle cx="{sp_x+40}" cy="{sp_y}" r="2" fill="{acc}"/>
"""

        cards_svg.append(f"""  <g id="metric-card-{i}">
    {hull}
    <text x="{x+14}" y="{y+22}" fill="{text_dim}" class="font-mono-lbl">{label_disp}</text>
    {status_markup}
    <text x="{x+14}" y="{y+54}" fill="{title_front}" font-size="{val_fs}" class="font-mono-val">{val_disp}</text>
    {delta_markup}
    {sparkline}
  </g>""")

    joined_cards = "\n".join(cards_svg)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h+6}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono-lbl {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 11px; font-weight: bold; letter-spacing: 0.5px; }}
      .font-mono-val {{ font-family: 'JetBrains Mono', 'Courier New', monospace; font-size: 26px; font-weight: 900; letter-spacing: -0.5px; }}
      .font-mono-sub {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 11px; font-weight: bold; }}
      .font-mono-tag {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; }}
    </style>
  </defs>
{joined_cards}
</svg>"""

    validate_svg(svg)
    return svg

def generate_progress(value=50, label="SYSTEM PROGRESS", sub=None, style=None, primary=None, accent=None, mode="auto", preset=None, width=850, tertiary=None, theme=None):
    """
    Renders a segmented sci-fi HUD progress bar with dithering and status readout.
    """
    style_name, theme_name = normalize_style_and_theme(style=style, theme=theme)
    c, css_vars = resolve_theme(style=style_name, theme=theme_name, mode=mode, primary=primary, accent=accent, preset=preset, tertiary=tertiary)
    if style_name == "modern":
        return _generate_modern_progress(style_name=style_name, theme_name=theme_name, c=c, css_vars=css_vars, value=value, label=label, sub=sub, width=width)
    elif style_name == "sketch":
        return _generate_sketch_progress(style_name=style_name, theme_name=theme_name, c=c, css_vars=css_vars, value=value, label=label, sub=sub, width=width)
    prim = c["primary"]
    acc = c["accent"]
    panel = c["panel"]
    border = c["border"]
    text_dim = c["text_dim"]
    title_front = c["title_front"]
    if theme_name in ("tactical", "amber", "amber_crt"):
        st = "tactical"
    elif theme_name in ("minimal", "clean-mono", "clean_mono", "academic-paper", "academic_paper", "corporate-blue", "corporate_blue", "tokyo", "tokyo_night", "swiss-mono", "swiss_mono", "executive-slate", "executive_slate"):
        st = "minimal"
    else:
        st = "cyberpunk"

    try:
        val_clean = max(0, min(100, int(round(float(value)))))
    except Exception:
        val_clean = 50

    lbl_clean = escape_xml(label)
    sub_raw = sub if sub is not None else f"RUNTIME PROGRESS // {val_clean}% COMPLETE"
    sub_clean = escape_xml(sub_raw)

    lbl_disp = clamp_text_to_width(f"■ {lbl_clean}", width - 95, 11)
    sub_disp = clamp_text_to_width(sub_clean, width - 200, 11)

    total_segments = 32
    filled_segments = int(round(total_segments * (val_clean / 100)))

    h = 68
    track_x = 14
    track_y = 28
    track_w = width - 28
    track_h = 14

    seg_gap = 2
    seg_w = (track_w - (total_segments - 1) * seg_gap) / total_segments

    segments_svg = []
    for s in range(total_segments):
        sx = track_x + s * (seg_w + seg_gap)
        if s < filled_segments - 1:
            col = prim
            op = "1.0"
        elif s == filled_segments - 1:
            col = acc  # Active front block
            op = "1.0"
        else:
            col = border
            op = "0.2"

        segments_svg.append(f'<rect x="{sx:.1f}" y="{track_y}" width="{seg_w:.1f}" height="{track_h}" fill="{col}" fill-opacity="{op}"/>')

    joined_segments = "\n    ".join(segments_svg)

    # Style hull
    if st == "tactical":
        hull = f"""
  <polygon points="1,2 {width-1},2 {width-1},{h-10} {width-10},{h-1} 10,{h-1} 1,{h-10}" fill="{panel}" stroke="{border}" stroke-width="1.5"/>
  <polygon points="1,2 14,2 1,15" fill="{prim}"/>
  <polygon points="{width-1},2 {width-14},2 {width-1},15" fill="{acc}"/>
"""
    elif st == "minimal":
        hull = f"""
  <rect x="1" y="2" width="{width-2}" height="{h-3}" fill="{panel}" stroke="{border}" stroke-width="1"/>
  <line x1="1" y1="2" x2="{width-1}" y2="2" stroke="{prim}" stroke-width="2"/>
"""
    else:  # cyberpunk
        hull = f"""
  <rect x="1" y="2" width="{width-2}" height="{h-3}" fill="{panel}" stroke="{border}" stroke-width="1.5"/>
  <rect x="1" y="2" width="6" height="6" fill="{prim}"/>
  <rect x="{width-7}" y="2" width="6" height="6" fill="{acc}"/>
  <rect x="1" y="{h-7}" width="6" height="6" fill="{acc}"/>
  <rect x="{width-7}" y="{h-7}" width="6" height="6" fill="{prim}"/>
"""

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-prog-lbl {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 11px; font-weight: bold; letter-spacing: 0.5px; }}
      .font-prog-val {{ font-family: 'JetBrains Mono', 'Courier New', monospace; font-size: 12px; font-weight: 900; }}
      .font-prog-sub {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 11px; font-weight: bold; }}
    </style>
  </defs>
  {hull}
  <!-- Label & Percentage Header -->
  <text x="14" y="19" fill="{title_front}" class="font-prog-lbl">{lbl_disp}</text>
  <rect x="{width-74}" y="7" width="60" height="15" fill="{panel}" stroke="{acc}" stroke-width="1"/>
  <text x="{width-44}" y="19" fill="{acc}" text-anchor="middle" class="font-prog-val">{val_clean}%</text>

  <!-- Track & Segments -->
  <rect x="{track_x-1}" y="{track_y-1}" width="{track_w+2}" height="{track_h+2}" fill="none" stroke="{border}" stroke-width="1"/>
  <g id="segments">
    {joined_segments}
  </g>

  <!-- Subtext & Milestone Ticks -->
  <text x="14" y="56" fill="{text_dim}" class="font-prog-sub">{sub_disp}</text>
  <text x="{width-14}" y="56" fill="{text_dim}" text-anchor="end" class="font-prog-sub">0% ── 50% ── 100%</text>
</svg>"""

    validate_svg(svg)
    return svg

def generate_techstack(items=None, columns=5, style=None, primary=None, accent=None, mode="auto", preset=None, width=850, tertiary=None, theme=None):
    """
    Renders a sci-fi HUD matrix of technology cards with embedded 20x20 pixel vector icons.
    items: list of string names e.g. ["python", "cpp", "docker", "git", "linux"]
    """
    from generator.icons import get_tech_icon_svg

    style_name, theme_name = normalize_style_and_theme(style=style, theme=theme)
    c, css_vars = resolve_theme(style=style_name, theme=theme_name, mode=mode, primary=primary, accent=accent, preset=preset, tertiary=tertiary)
    if style_name == "modern":
        return _generate_modern_techstack(style_name=style_name, theme_name=theme_name, c=c, css_vars=css_vars, items=items, columns=columns, width=width)
    elif style_name == "sketch":
        return _generate_sketch_techstack(style_name=style_name, theme_name=theme_name, c=c, css_vars=css_vars, items=items, columns=columns, width=width)
    prim = c["primary"]
    acc = c["accent"]
    panel = c["panel"]
    border = c["border"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]
    if theme_name in ("tactical", "amber", "amber_crt"):
        st = "tactical"
    elif theme_name in ("minimal", "clean-mono", "clean_mono", "academic-paper", "academic_paper", "corporate-blue", "corporate_blue", "tokyo", "tokyo_night", "swiss-mono", "swiss_mono", "executive-slate", "executive_slate"):
        st = "minimal"
    else:
        st = "cyberpunk"

    if items is None:
        tech_list = ["python", "cpp", "rust", "docker", "git"]
    elif isinstance(items, str):
        tech_list = [x.strip() for x in items.split(",") if x.strip()]
    else:
        tech_list = list(items)

    cols = max(2, min(int(columns), 8))
    rows = (len(tech_list) + cols - 1) // cols

    usable_w = width - 2
    gap_x = 10
    gap_y = 10
    card_w = (usable_w - (cols - 1) * gap_x) // cols
    card_h = 40
    total_h = 10 + rows * (card_h + gap_y)

    items_svg = []
    for idx, item in enumerate(tech_list):
        r = idx // cols
        col = idx % cols
        x = 1 + col * (card_w + gap_x)
        y = 6 + r * (card_h + gap_y)

        if isinstance(item, dict):
            raw_name = str(item.get("name") or item.get("id") or item.get("icon") or "ITEM")
            icon_key = str(item.get("icon") or raw_name)
            sub_label = str(item.get("label", "")) if item.get("label") else None
        else:
            raw_name = str(item)
            icon_key = raw_name
            sub_label = None

        clean_name = escape_xml(raw_name.upper())
        icon_inner = get_tech_icon_svg(icon_key)

        label_markup = ""
        if sub_label:
            lbl_clean = escape_xml(sub_label.upper())
            lbl_disp = clamp_text_to_width(lbl_clean, card_w // 2 - 10, 10)
            sub_w = measure_mono_text_width(lbl_disp, 10)
            max_name_w = max(40, card_w - 42 - int(sub_w) - 10)
            clean_disp = clamp_text_to_width(clean_name, max_name_w, 11)
            label_markup = f'<text x="{x+card_w-8}" y="{y+25}" fill="{text_dim}" text-anchor="end" class="font-tech-sub">{lbl_disp}</text>'
        else:
            clean_disp = clamp_text_to_width(clean_name, card_w - 44, 11)

        if st == "tactical":
            card_bg = f"""<polygon points="{x+6},{y} {x+card_w},{y} {x+card_w},{y+card_h-6} {x+card_w-6},{y+card_h} {x},{y+card_h} {x},{y+6}" fill="{panel}" stroke="{border}" stroke-width="1.2"/>
    <line x1="{x+card_w-4}" y1="{y+2}" x2="{x+card_w-2}" y2="{y+4}" stroke="{acc}" stroke-width="1.5"/>"""
        elif st == "minimal":
            card_bg = f"""<rect x="{x}" y="{y}" width="{card_w}" height="{card_h}" fill="{panel}" stroke="{border}" stroke-width="1"/>
    <line x1="{x}" y1="{y}" x2="{x+card_w}" y2="{y}" stroke="{prim}" stroke-width="1.5"/>"""
        else:  # cyberpunk
            card_bg = f"""<rect x="{x}" y="{y}" width="{card_w}" height="{card_h}" fill="{panel}" stroke="{border}" stroke-width="1.2"/>
    <line x1="{x}" y1="{y+4}" x2="{x}" y2="{y}" stroke="{prim}" stroke-width="1.5"/>
    <line x1="{x}" y1="{y}" x2="{x+4}" y2="{y}" stroke="{prim}" stroke-width="1.5"/>
    <line x1="{x+card_w-4}" y1="{y+card_h}" x2="{x+card_w}" y2="{y+card_h}" stroke="{prim}" stroke-width="1.5"/>
    <line x1="{x+card_w}" y1="{y+card_h-4}" x2="{x+card_w}" y2="{y+card_h}" stroke="{prim}" stroke-width="1.5"/>"""

        items_svg.append(f"""  <g id="tech-{idx}">
    {card_bg}
    <g transform="translate({x+10}, {y+10})" color="{prim}">
      {icon_inner}
    </g>
    <text x="{x+36}" y="{y+25}" fill="{text_main}" class="font-tech-name">{clean_disp}</text>
    {label_markup}
  </g>""")

    joined_items = "\n".join(items_svg)
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {total_h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-tech-name {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 11px; font-weight: bold; letter-spacing: 0.5px; }}
      .font-tech-sub {{ font-family: 'JetBrains Mono', 'Fira Code', monospace; font-size: 10px; font-weight: bold; }}
    </style>
  </defs>
{joined_items}
</svg>"""

    validate_svg(svg)
    return svg

