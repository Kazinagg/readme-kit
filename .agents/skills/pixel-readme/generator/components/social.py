"""Social, starchart and profile card components for Pixel Readme Kit."""
from typing import Optional, Any, List
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
    render_rough_circle,
    coord_jitter,
)
from generator.font_engine import render_3d_text, calculate_smart_layout, calculate_px_size

def _generate_modern_social(style_name, theme_name, c, css_vars,
                            title="PIXEL-KIT", subtitle="TRANSLUCENT RETRO HUD READMES",
                            repo="Kazinagg/pixel-readme-kit", tags="PYTHON,SVG,HUD,RETRO",
                            width=1280, height=640):
    """Renders a flagship modern SaaS/DevTools OpenGraph preview card (1280x640)."""
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
    repo_clean = escape_xml(repo)

    # Parse tags
    if not tags:
        tag_list = ["GITHUB", "OPEN-SOURCE", "v6.0"]
    elif isinstance(tags, str):
        tag_list = [t.strip().upper() for t in tags.split(",") if t.strip()]
    else:
        tag_list = [str(t).strip().upper() for t in tags if t]

    # Repository top pill
    repo_header_str = f"repo // {repo_clean}"
    repo_disp = clamp_sans_text_to_width(repo_header_str, 420, 14)
    repo_pill_w = max(200, int(measure_sans_text_width(repo_disp, 14) + 48))

    # Title sizing
    title_fs = 54 if len(title) <= 24 else (44 if len(title) <= 36 else 36)
    title_disp = clamp_sans_text_to_width(title_clean, width - 160, title_fs)

    # Subtitle sizing
    sub_disp = clamp_sans_text_to_width(sub_clean, width - 160, 20)

    # Tag pills row
    tag_pills = []
    curr_x = 80
    for tag in tag_list[:6]:
        tag_disp = clamp_sans_text_to_width(tag, 160, 13)
        pill_w = max(80, int(measure_sans_text_width(tag_disp, 13) + 36))
        if curr_x + pill_w > width - 80:
            break
        tag_pills.append(f"""    <g transform="translate({curr_x}, 370)">
      <rect x="0" y="0" width="{pill_w}" height="32" rx="16" fill="{panel}" stroke="{border}" stroke-width="1"/>
      <circle cx="14" cy="16" r="3.5" fill="{acc}"/>
      <text x="26" y="21" fill="{text_main}" font-size="13" font-weight="600" class="font-sans">{tag_disp}</text>
    </g>""")
        curr_x += pill_w + 12

    # Bottom feature highlight cards (3 cards)
    col_w = (width - 160 - 2 * 20) // 3
    features = [
        ("DETERMINISTIC SVG", "Zero-drift layout & verified pixel accuracy"),
        ("HIGH PERFORMANCE", "Pure browser-native rendering, 0 dependencies"),
        ("DYNAMIC MODES", "Automated system dark/light sync support"),
    ]
    feat_cards = []
    for i, (f_title, f_desc) in enumerate(features):
        fx = 80 + i * (col_w + 20)
        f_t_disp = escape_xml(clamp_sans_text_to_width(f_title, col_w - 32, 12))
        f_d_disp = escape_xml(clamp_sans_text_to_width(f_desc, col_w - 32, 11))
        feat_cards.append(f"""    <g transform="translate({fx}, 470)">
      <rect x="0" y="0" width="{col_w}" height="90" rx="12" fill="{panel}" stroke="{border}" stroke-width="1"/>
      <circle cx="20" cy="28" r="4" fill="{prim}"/>
      <text x="32" y="32" fill="{acc}" font-size="12" font-weight="700" letter-spacing="0.05em" class="font-sans">{f_t_disp}</text>
      <text x="20" y="60" fill="{text_dim}" font-size="11" class="font-sans">{f_d_disp}</text>
    </g>""")

    defs_markup = render_modern_defs(c, "modern-social")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">
  <defs>
    {defs_markup}
    <style>
      {css_vars}
      {MODERN_BASE_STYLES}
    </style>
    <radialGradient id="modern-social-glow" cx="50%" cy="30%" r="60%">
      <stop offset="0%" stop-color="{prim}" stop-opacity="0.12"/>
      <stop offset="60%" stop-color="{acc}" stop-opacity="0.03"/>
      <stop offset="100%" stop-color="{bg}" stop-opacity="0"/>
    </radialGradient>
  </defs>

  <!-- BACKGROUND & CHASSIS -->
  <rect x="2" y="2" width="{width-4}" height="{height-4}" rx="20" fill="{bg}" stroke="url(#modern-social-border-grad)" stroke-width="1.5"/>
  <rect x="2" y="2" width="{width-4}" height="{height-4}" rx="20" fill="url(#modern-social-glow)"/>
  <path d="M 28 2 L {width-28} 2" stroke="url(#modern-social-accent-grad)" stroke-width="2.5" stroke-linecap="round"/>

  <!-- REPO PILL & STATUS BADGE -->
  <g transform="translate(80, 68)">
    <rect x="0" y="0" width="{repo_pill_w}" height="36" rx="18" fill="{panel}" stroke="{border}" stroke-width="1"/>
    <circle cx="18" cy="18" r="4.5" fill="{prim}"/>
    <text x="32" y="23" fill="{text_main}" font-size="14" font-weight="600" class="font-sans">{repo_disp}</text>
  </g>

  <g transform="translate({width-230}, 68)">
    <rect x="0" y="0" width="150" height="36" rx="18" fill="{panel}" stroke="{border}" stroke-width="1"/>
    <circle cx="20" cy="18" r="4" fill="{success}"/>
    <text x="34" y="23" fill="{success}" font-size="13" font-weight="700" class="font-sans">ACTIVE // v6.0</text>
  </g>

  <!-- TITLE & SUBTITLE -->
  <text x="80" y="230" fill="url(#modern-social-accent-grad)" font-size="{title_fs}" font-weight="800" letter-spacing="-0.02em" class="font-sans">{title_disp}</text>
  <text x="80" y="285" fill="{text_dim}" font-size="20" font-weight="400" class="font-sans">{sub_disp}</text>

  <!-- TAG PILLS -->
  {"".join(tag_pills)}

  <!-- FEATURE CARDS -->
  {"".join(feat_cards)}
</svg>"""

    validate_svg(svg)
    return svg

def _generate_sketch_social(style_name, theme_name, c, css_vars,
                            title="PIXEL-KIT", subtitle="TRANSLUCENT RETRO HUD READMES",
                            repo="Kazinagg/pixel-readme-kit", tags="PYTHON,SVG,HUD,RETRO",
                            width=1280, height=640):
    """Renders a flagship hand-drawn sketch OpenGraph preview card (1280x640) on Excalidraw board."""
    prim = c["primary"]
    acc = c["accent"]
    tertiary_col = c.get("tertiary", "#FDE047")
    bg = c["bg"]
    panel = c["panel"]
    border = c["border"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]
    success = c["success"]

    title_clean = escape_xml(title)
    sub_clean = escape_xml(subtitle)
    repo_clean = escape_xml(repo)

    if not tags:
        tag_list = ["GITHUB", "OPEN-SOURCE", "v6.1"]
    elif isinstance(tags, str):
        tag_list = [t.strip().upper() for t in tags.split(",") if t.strip()]
    else:
        tag_list = [str(t).strip().upper() for t in tags if t]

    repo_header_str = f"repo // {repo_clean}"
    repo_disp = clamp_sans_text_to_width(repo_header_str, 420, 14)
    repo_pill_w = max(200, int(measure_sans_text_width(repo_disp, 14) + 48))

    title_fs = 54 if len(title) <= 24 else (44 if len(title) <= 36 else 36)
    title_disp = clamp_sans_text_to_width(title_clean, width - 160, title_fs)
    sub_disp = clamp_sans_text_to_width(sub_clean, width - 160, 20)

    # Tag pills row
    tag_pills = []
    curr_x = 80
    for i, tag in enumerate(tag_list[:6]):
        tag_disp = clamp_sans_text_to_width(tag, 160, 13)
        pill_w = max(80, int(measure_sans_text_width(tag_disp, 13) + 36))
        if curr_x + pill_w > width - 80:
            break
        box = render_rough_rect(x=curr_x, y=360, w=pill_w, h=32, stroke=acc, stroke_width=1.1, fill=panel, rx=8, seed=470 + i)
        tag_pills.append(f"""    <g>
      {box}
      <text x="{curr_x + pill_w//2}" y="381" fill="{text_main}" font-size="13" font-weight="600" text-anchor="middle" class="font-sketch">{tag_disp}</text>
    </g>""")
        curr_x += pill_w + 14

    # Feature cards (3 cards)
    col_w = (width - 160 - 2 * 20) // 3
    features = [
        ("DETERMINISTIC PHYSICS", "No randomized jitter drifts in git diffs"),
        ("AUTHENTIC ROUGH LOOK", "Double strokes, corner overshoots & hatching"),
        ("ZERO DEPENDENCIES", "Pure SVG math, 100% vector, instant loading"),
    ]
    feat_cards = []
    for i, (f_title, f_desc) in enumerate(features):
        fx = 80 + i * (col_w + 20)
        f_t_disp = escape_xml(clamp_sans_text_to_width(f_title, col_w - 32, 12))
        f_d_disp = escape_xml(clamp_sans_text_to_width(f_desc, col_w - 32, 11))
        f_box = render_rough_rect(x=fx, y=450, w=col_w, h=110, stroke=border, stroke_width=1.3, fill=panel, rx=6, seed=480 + i * 5)
        f_star = render_rough_star(cx=fx + 24, cy=476, r=5.0, fill=acc, stroke=acc, seed=485 + i)
        tape = f'<polygon points="{fx+col_w//2-22} 444, {fx+col_w//2+22} 444, {fx+col_w//2+16} 456, {fx+col_w//2-28} 456" fill="url(#socialSketch-tape)" stroke="{tertiary_col}" stroke-width="0.6" opacity="0.8"/>'
        feat_cards.append(f"""    <g>
      {tape}
      {f_box}
      {f_star}
      <text x="{fx+38}" y="480" fill="{prim}" font-size="12" font-weight="700" class="font-sketch">{f_t_disp}</text>
      <text x="{fx+20}" y="520" fill="{text_dim}" font-size="11" class="font-sketch">{f_d_disp}</text>
    </g>""")

    chassis = render_rough_rect(x=6, y=6, w=width-12, h=height-12, stroke=border, stroke_width=1.8, fill=bg, rx=12, seed=450)
    washi_tape = f'<polygon points="60 0, 160 0, 140 24, 40 24" fill="url(#socialSketch-tape)" stroke="{tertiary_col}" stroke-width="0.9" opacity="0.8"/>'
    repo_box = render_rough_rect(x=80, y=60, w=repo_pill_w, h=36, stroke=acc, stroke_width=1.2, fill=panel, rx=6, seed=455)
    status_box = render_rough_rect(x=width-260, y=60, w=180, h=36, stroke=success, stroke_width=1.2, fill=panel, rx=6, seed=460)
    title_w_est = min(width - 160, int(measure_sans_text_width(title_disp, title_fs) * 1.05))
    wavy_title_line = render_rough_line(80, 240, 80 + title_w_est, 240, stroke=acc, stroke_width=2.5, jitter=1.4, seed=465)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">
  <defs>
    <style>
      {css_vars}
{SKETCH_BASE_STYLES}
    </style>
{render_sketch_defs(c, "socialSketch")}
  </defs>

  <!-- Sketch Canvas Chassis -->
  {chassis}
  {washi_tape}

  <!-- Header Pills -->
  <g>
    {repo_box}
    <text x="96" y="83" fill="{text_main}" font-size="14" font-weight="600" class="font-sketch">📁 {repo_disp}</text>
  </g>
  <g>
    {status_box}
    <text x="{width-170}" y="83" fill="{success}" font-size="13" font-weight="700" text-anchor="middle" class="font-sketch">★ ACTIVE // v6.1 DRAFT</text>
  </g>

  <!-- Title & Underline -->
  <text x="80" y="220" fill="{prim}" font-size="{title_fs}" font-weight="700" class="font-sketch">{title_disp}</text>
  {wavy_title_line}

  <!-- Subtitle Marker -->
  <rect x="80" y="260" width="{min(width-160, int(measure_sans_text_width(sub_disp, 20) + 40))}" height="32" rx="4" fill="{tertiary_col}" fill-opacity="0.18"/>
  <text x="92" y="283" fill="{text_main}" font-size="20" font-weight="600" class="font-sketch">✏️ {sub_disp}</text>

  <!-- Tag Pills -->
{"".join(tag_pills)}

  <!-- Feature Cards -->
{"".join(feat_cards)}
</svg>"""

    validate_svg(svg)
    return svg


def generate_social(style=None, primary=None, accent=None,
                    title="PIXEL-KIT", subtitle="TRANSLUCENT RETRO HUD READMES",
                    repo="Kazinagg/pixel-readme-kit", tags="PYTHON,SVG,HUD,RETRO",
                    width=1280, height=640, mode="auto", preset=None, tertiary=None, theme=None):
    """
    Renders an OpenGraph Social Preview Card (1280x640) for GitHub repositories.
    """
    style_name, theme_name = normalize_style_and_theme(style=style, theme=theme)
    c, css_vars = resolve_theme(style=style_name, theme=theme_name, mode=mode, primary=primary, accent=accent, preset=preset, tertiary=tertiary)
    if style_name == "modern":
        return _generate_modern_social(
            style_name=style_name, theme_name=theme_name, c=c, css_vars=css_vars,
            title=title, subtitle=subtitle, repo=repo, tags=tags,
            width=width, height=height
        )
    elif style_name == "sketch":
        return _generate_sketch_social(
            style_name=style_name, theme_name=theme_name, c=c, css_vars=css_vars,
            title=title, subtitle=subtitle, repo=repo, tags=tags,
            width=width, height=height
        )
    prim = c["primary"]
    acc = c["accent"]
    bg = c["bg"]
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

    title_clean = escape_xml(title)
    sub_clean = escape_xml(subtitle)
    repo_clean = escape_xml(repo.upper())

    # Repository header bar
    repo_header_str = f"■ REPOSITORY // {repo_clean}"
    repo_box_w = min(540, max(360, int(measure_mono_text_width(repo_header_str, 13) + 32)))
    repo_disp = clamp_text_to_width(repo_header_str, repo_box_w - 28, 13)
    badge2_x = 80 + repo_box_w + 14

    # 3D Pixel Title at px_size=7 (or 6 if long)
    px_size = 6 if len(title) > 14 else 7
    pixel_markup, t_w, t_h = render_3d_text(
        title, x=80, y=170, px_size=px_size,
        front_color=c["title_front"], mid_shadow=c["title_mid"], dark_shadow=c["title_dark"],
        spacing=2, max_width=750, allow_wrap=True
    )

    y_sub = 170 + t_h + 24
    max_sub_w = 740
    sub_disp = clamp_text_to_width(sub_clean, max_sub_w - 50, 15)
    sub_w = min(max_sub_w, max(320, int(measure_mono_text_width(f"▶ {sub_disp}", 15) + 40)))

    # Parse technology/feature tags
    if not tags:
        tag_list = ["GITHUB", "OPEN-SOURCE", "v5.0"]
    elif isinstance(tags, str):
        tag_list = [t.strip().upper() for t in tags.split(",") if t.strip()]
    else:
        tag_list = [str(t).strip().upper() for t in tags if t]
    tag_chips = []
    curr_x = 80
    for t_item in tag_list[:5]:
        t_clean = escape_xml(t_item)
        tw = int(measure_mono_text_width(t_clean, 12) + 28)
        if curr_x + tw > 860:
            break
        tag_chips.append(f"""
    <g transform="translate({curr_x}, 530)">
      <rect x="0" y="0" width="{tw}" height="34" fill="{panel}" stroke="{prim}" stroke-width="1.2"/>
      <rect x="0" y="0" width="4" height="34" fill="{prim}"/>
      <text x="{tw//2 + 2}" y="22" fill="{acc}" font-size="12" font-weight="bold" text-anchor="middle" class="font-mono">{t_clean}</text>
    </g>
""")
        curr_x += tw + 16
    chips_markup = "".join(tag_chips)

    # Chassis styling
    if st == "tactical":
        chassis = f"""
  <polygon points="24 6, {width-24} 6, {width-6} 24, {width-6} {height-24}, {width-24} {height-6}, 24 {height-6}, 6 {height-24}, 6 24"
           fill="{bg}" stroke="{border}" stroke-width="2.5"/>
  <polygon points="32 14, {width-32} 14, {width-14} 32, {width-14} {height-32}, {width-32} {height-14}, 32 {height-14}, 14 {height-32}, 14 32"
           fill="none" stroke="{prim}" stroke-width="1.5" opacity="0.6"/>
  <!-- Corner Hazard Chevrons -->
  <polygon points="40 18, 54 18, 36 36, 22 36" fill="{prim}"/>
  <polygon points="62 18, 76 18, 58 36, 44 36" fill="{prim}"/>
"""
        reticle = f"""
  <g transform="translate(1020, 320)">
    <circle cx="0" cy="0" r="140" fill="none" stroke="{border}" stroke-width="2"/>
    <circle cx="0" cy="0" r="90" fill="none" stroke="{prim}" stroke-width="1.5" stroke-dasharray="6 4"/>
    <circle cx="0" cy="0" r="40" fill="{panel}" stroke="{acc}" stroke-width="1.5"/>
    <line x1="-160" y1="0" x2="160" y2="0" stroke="{prim}" stroke-width="1.5" stroke-dasharray="8 4"/>
    <line x1="0" y1="-160" x2="0" y2="160" stroke="{prim}" stroke-width="1.5" stroke-dasharray="8 4"/>
    <text x="0" y="5" fill="{prim}" font-size="12" font-weight="bold" text-anchor="middle" class="font-mono">LOCK-ON</text>
  </g>
"""
    elif st == "minimal":
        chassis = f"""
  <rect x="8" y="8" width="{width-16}" height="{height-16}" fill="{bg}" stroke="{border}" stroke-width="2"/>
  <line x1="8" y1="8" x2="{width-8}" y2="8" stroke="{prim}" stroke-width="4"/>
  <rect x="14" y="14" width="8" height="8" fill="{prim}"/>
  <rect x="{width-22}" y="14" width="8" height="8" fill="{acc}"/>
  <rect x="14" y="{height-22}" width="8" height="8" fill="{acc}"/>
  <rect x="{width-22}" y="{height-22}" width="8" height="8" fill="{prim}"/>
"""
        reticle = f"""
  <g transform="translate(1020, 320)">
    <rect x="-110" y="-110" width="220" height="220" fill="none" stroke="{border}" stroke-width="1.5"/>
    <rect x="-80" y="-80" width="160" height="160" fill="{panel}" stroke="{prim}" stroke-width="1.5"/>
    <line x1="-110" y1="0" x2="110" y2="0" stroke="{acc}" stroke-width="2"/>
    <line x1="0" y1="-110" x2="0" y2="110" stroke="{acc}" stroke-width="2"/>
    <circle cx="0" cy="0" r="6" fill="{prim}"/>
  </g>
"""
    else:  # cyberpunk
        chassis = f"""
  <rect x="8" y="8" width="{width-16}" height="{height-16}" fill="{bg}" stroke="{border}" stroke-width="2"/>
  <rect x="8" y="8" width="16" height="16" fill="{prim}"/>
  <rect x="{width-24}" y="8" width="16" height="16" fill="{acc}"/>
  <rect x="8" y="{height-24}" width="16" height="16" fill="{acc}"/>
  <rect x="{width-24}" y="{height-24}" width="16" height="16" fill="{prim}"/>
  <line x1="8" y1="48" x2="24" y2="48" stroke="{prim}" stroke-width="2"/>
  <line x1="{width-24}" y1="{height-48}" x2="{width-8}" y2="{height-48}" stroke="{acc}" stroke-width="2"/>
"""
        reticle = f"""
  <g transform="translate(1020, 320)">
    <circle cx="0" cy="0" r="140" fill="none" stroke="{border}" stroke-width="2"/>
    <circle cx="0" cy="0" r="100" fill="none" stroke="{prim}" stroke-width="2" stroke-dasharray="10 6"/>
    <circle cx="0" cy="0" r="60" fill="{panel}" stroke="{acc}" stroke-width="2"/>
    <line x1="-150" y1="0" x2="150" y2="0" stroke="{prim}" stroke-width="1.5"/>
    <line x1="0" y1="-150" x2="0" y2="150" stroke="{prim}" stroke-width="1.5"/>
    <circle cx="45" cy="-45" r="5" fill="{prim}"/>
    <circle cx="-55" cy="35" r="4" fill="{acc}"/>
  </g>
"""

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
    </style>
  </defs>

  {chassis}

  <!-- TOP REPOSITORY HEADER -->
  <rect x="80" y="56" width="{repo_box_w}" height="34" fill="{panel}" stroke="{border}" stroke-width="1.2"/>
  <text x="96" y="78" fill="{prim}" font-size="13" font-weight="bold" letter-spacing="1px" class="font-mono">{repo_disp}</text>
  <rect x="{badge2_x}" y="56" width="140" height="34" fill="{panel}" stroke="{acc}" stroke-width="1.2"/>
  <text x="{badge2_x + 70}" y="78" fill="{acc}" font-size="12" font-weight="bold" text-anchor="middle" class="font-mono">PUBLIC // v5.0</text>

  <!-- 3D PIXEL TITLE -->
  {pixel_markup}

  <!-- SUBTITLE CALLOUT -->
  <rect x="80" y="{y_sub}" width="{sub_w}" height="42" fill="{panel}" stroke="{acc}" stroke-width="1.5"/>
  <text x="100" y="{y_sub + 27}" fill="{text_main}" font-size="15" font-weight="bold" class="font-mono">▶ {sub_disp}</text>

  <!-- TECH / FEATURE TAGS ROW -->
  {chips_markup}

  <!-- RIGHT SIDE RETICLE -->
  {reticle}

  <!-- WATERMARK -->
  <text x="{width-80}" y="{height-40}" fill="{text_dim}" font-size="12" font-weight="bold" text-anchor="end" class="font-mono">PIXEL-README-KIT // 1280x640 OPENGRAPH</text>
</svg>"""

    validate_svg(svg)
    return svg

# ==============================================================================
def _generate_modern_starchart(style_name, theme_name, c, css_vars,
                              repo="Kazinagg/pixel-readme-kit", points=None,
                              current=None, delta="+78% past 6m", title="STAR GROWTH TRAJECTORY",
                              period="6M", width=850, height=230):
    """Renders a sleek vector star trend chart with smooth cubic Bezier spline and area gradient fill."""
    prim = c["primary"]
    acc = c["accent"]
    tertiary_col = c["tertiary"]
    bg = c["bg"]
    panel = c["panel"]
    border = c["border"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]
    success = c["success"]

    title_clean = escape_xml(title.upper())
    repo_clean = escape_xml(repo.strip())
    delta_clean = escape_xml(delta)

    # Parse points
    if points is None:
        pts = [15.0, 65.0, 190.0, 480.0, 950.0, 1650.0]
    elif isinstance(points, str):
        pts = []
        for x in points.split(","):
            x = x.strip()
            if x:
                try:
                    pts.append(float(x))
                except ValueError:
                    pass
        if not pts:
            pts = [15.0, 65.0, 190.0, 480.0, 950.0, 1650.0]
    elif isinstance(points, (list, tuple)):
        pts = []
        for x in points:
            if x is not None:
                try:
                    if isinstance(x, (list, tuple)):
                        pts.append(float(x[1] if len(x) > 1 else x[0]))
                    else:
                        pts.append(float(x))
                except (ValueError, TypeError):
                    pass
        if not pts:
            pts = [15.0, 65.0, 190.0, 480.0, 950.0, 1650.0]
    else:
        pts = [15.0, 65.0, 190.0, 480.0, 950.0, 1650.0]

    cur_val = current if current else (f"{int(pts[-1]):,}" if pts else "1,650")

    # Geometry bounds
    pad_left = 65
    pad_right = width - 40
    chart_w = pad_right - pad_left
    pad_top = 68
    pad_bot = height - 44
    chart_h = pad_bot - pad_top

    min_v = 0.0
    max_v = max(pts) if pts else 1000.0
    if max_v <= 0:
        max_v = 100.0

    n = len(pts)
    step_x = chart_w / (n - 1) if n > 1 else chart_w
    coords = []
    for i, val in enumerate(pts):
        cx = pad_left + i * step_x
        ratio = (val - min_v) / (max_v - min_v) if max_v > min_v else 0.5
        cy = pad_bot - ratio * chart_h
        coords.append((cx, cy, val))

    # Build smooth cubic Bezier spline
    first_x, first_y = coords[0][0], coords[0][1]
    last_x, last_y = coords[-1][0], coords[-1][1]

    if n == 1:
        curve_d = f"M {first_x:.1f} {first_y:.1f}"
        area_d = f"M {first_x:.1f} {pad_bot} L {first_x:.1f} {first_y:.1f} L {first_x:.1f} {pad_bot} Z"
    else:
        curve_segments = []
        for i in range(n - 1):
            p0 = coords[i]
            p1 = coords[i + 1]
            dx = (p1[0] - p0[0]) * 0.45
            cp1_x, cp1_y = p0[0] + dx, p0[1]
            cp2_x, cp2_y = p1[0] - dx, p1[1]
            curve_segments.append(f"C {cp1_x:.1f} {cp1_y:.1f}, {cp2_x:.1f} {cp2_y:.1f}, {p1[0]:.1f} {p1[1]:.1f}")
        spline_body = " ".join(curve_segments)
        curve_d = f"M {first_x:.1f} {first_y:.1f} {spline_body}"
        area_d = f"M {first_x:.1f} {pad_bot} L {first_x:.1f} {first_y:.1f} {spline_body} L {last_x:.1f} {pad_bot} Z"

    # Subtle horizontal grid lines (4 lines)
    grid_lines = []
    y_labels = []
    for step in range(4):
        gy = pad_bot - step * (chart_h / 3.0)
        g_val = int(min_v + step * (max_v - min_v) / 3.0)
        v_str = f"{g_val/1000.0:.1f}k" if g_val >= 1000 else str(g_val)
        grid_lines.append(f'<line x1="{pad_left}" y1="{gy:.1f}" x2="{pad_right}" y2="{gy:.1f}" stroke="{border}" stroke-width="1" stroke-dasharray="3 4" opacity="0.45"/>')
        y_labels.append(f'<text x="{pad_left - 10}" y="{gy + 3.5:.1f}" fill="{text_dim}" font-size="10" text-anchor="end" class="font-mono">{v_str}</text>')

    # Vertical ticks & X labels
    x_labels = []
    month_names = ["M-5", "M-4", "M-3", "M-2", "M-1", "NOW"]
    for i, (cx, cy, val) in enumerate(coords):
        lbl = month_names[i] if i < len(month_names) else f"T{i+1}"
        x_labels.append(f'<text x="{cx:.1f}" y="{pad_bot + 18}" fill="{text_dim}" font-size="10.5" font-weight="500" text-anchor="middle" class="font-sans">{lbl}</text>')

    # Data points and peak marker
    dots = []
    callout_text = f"★ {cur_val}"
    callout_w = max(76, int(measure_sans_text_width(callout_text, 11) + 22))

    for i, (cx, cy, val) in enumerate(coords):
        if i == len(coords) - 1:
            tag_y = cy + 12 if cy < 65 else cy - 30
            tag_x = max(pad_left, min(width - callout_w - 14, cx - callout_w // 2))
            dots.append(f"""
    <!-- Peak Milestone Marker -->
    <circle cx="{cx:.1f}" cy="{cy:.1f}" r="8" fill="{acc}" opacity="0.2"/>
    <circle cx="{cx:.1f}" cy="{cy:.1f}" r="5" fill="{bg}" stroke="{acc}" stroke-width="2"/>
    <circle cx="{cx:.1f}" cy="{cy:.1f}" r="2" fill="{prim}"/>
    <!-- Peak Callout Pill -->
    <g transform="translate({tag_x:.1f}, {tag_y:.1f})">
      <rect x="0" y="0" width="{callout_w}" height="22" rx="11" fill="{panel}" stroke="{acc}" stroke-width="1.2"/>
      <text x="{callout_w // 2}" y="15" fill="{acc}" font-size="11" font-weight="700" text-anchor="middle" class="font-sans">{callout_text}</text>
    </g>""")
        else:
            dots.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="3" fill="{panel}" stroke="{prim}" stroke-width="1.5"/>')

    # Modern header badges
    badge1_text = f"★ {cur_val}"
    badge1_w = max(86, int(measure_sans_text_width(badge1_text, 11) + 24))
    badge2_text = delta_clean
    badge2_w = max(86, int(measure_sans_text_width(badge2_text, 10.5) + 24))
    badges_total_w = badge1_w + 8 + badge2_w
    badges_x = width - badges_total_w - 20

    max_hdr_w = badges_x - 32
    title_disp = clamp_sans_text_to_width(title_clean, max_hdr_w - 180, 12)
    repo_disp = clamp_sans_text_to_width(repo_clean, 160, 11)

    defs_markup = render_modern_defs(c, "modern-starchart")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">
  <defs>
    {defs_markup}
    <style>
      {css_vars}
      {MODERN_BASE_STYLES}
    </style>
    <linearGradient id="modern-star-area" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{prim}" stop-opacity="0.25"/>
      <stop offset="100%" stop-color="{prim}" stop-opacity="0.0"/>
    </linearGradient>
  </defs>

  <!-- MODERN CHASSIS -->
  <rect x="2" y="2" width="{width-4}" height="{height-4}" rx="14" fill="{bg}" stroke="url(#modern-starchart-border-grad)" stroke-width="1.2"/>
  <path d="M 16 2 L {width-16} 2" stroke="url(#modern-starchart-accent-grad)" stroke-width="2" stroke-linecap="round"/>

  <!-- HEADER -->
  <g transform="translate(20, 18)">
    <circle cx="8" cy="14" r="3.5" fill="{success}"/>
    <text x="18" y="18" fill="{text_main}" font-size="12" font-weight="700" letter-spacing="0.03em" class="font-sans">{title_disp}</text>
    <text x="{22 + int(measure_sans_text_width(title_disp, 12)) + 6}" y="18" fill="{text_dim}" font-size="11" class="font-mono">/ {repo_disp}</text>
  </g>

  <!-- STATS PILLS -->
  <g transform="translate({badges_x}, 18)">
    <rect x="0" y="0" width="{badge1_w}" height="24" rx="12" fill="{panel}" stroke="{prim}" stroke-width="1"/>
    <text x="{badge1_w // 2}" y="16" fill="{prim}" font-size="11" font-weight="700" text-anchor="middle" class="font-sans">{badge1_text}</text>
    <rect x="{badge1_w + 8}" y="0" width="{badge2_w}" height="24" rx="12" fill="{panel}" stroke="{acc}" stroke-width="1"/>
    <text x="{badge1_w + 8 + badge2_w // 2}" y="16" fill="{acc}" font-size="10.5" font-weight="600" text-anchor="middle" class="font-sans">{badge2_text}</text>
  </g>

  <!-- GRID & AXES -->
  {"".join(grid_lines)}
  {"".join(y_labels)}
  {"".join(x_labels)}

  <!-- CHART AREA & BEZIER SPLINE -->
  <path d="{area_d}" fill="url(#modern-star-area)" shape-rendering="geometricPrecision"/>
  <path d="{curve_d}" fill="none" stroke="url(#modern-starchart-accent-grad)" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" shape-rendering="geometricPrecision"/>

  <!-- DATA VERTICES -->
  {"".join(dots)}
</svg>"""

    validate_svg(svg)
    return svg

def _generate_sketch_starchart(style_name, theme_name, c, css_vars,
                              repo="Kazinagg/pixel-readme-kit", points=None,
                              current=None, delta="+78% past 6m", title="STAR GROWTH TRAJECTORY",
                              period="6M", width=850, height=230):
    """Renders the authentic hand-drawn Star-History style star growth chart with pencil hatching and doodle star."""
    prim = c["primary"]
    acc = c["accent"]
    tertiary_col = c.get("tertiary", "#FDE047")
    bg = c["bg"]
    panel = c["panel"]
    border = c["border"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]
    success = c["success"]

    title_clean = escape_xml(title.upper())
    repo_clean = escape_xml(repo.strip())
    delta_clean = escape_xml(delta)

    # Parse points
    if points is None:
        pts = [15.0, 65.0, 190.0, 480.0, 950.0, 1650.0]
    elif isinstance(points, str):
        pts = []
        for x in points.split(","):
            x = x.strip()
            if x:
                try:
                    pts.append(float(x))
                except ValueError:
                    pass
        if not pts:
            pts = [15.0, 65.0, 190.0, 480.0, 950.0, 1650.0]
    elif isinstance(points, (list, tuple)):
        pts = []
        for x in points:
            if x is not None:
                try:
                    if isinstance(x, (list, tuple)):
                        pts.append(float(x[1] if len(x) > 1 else x[0]))
                    else:
                        pts.append(float(x))
                except (ValueError, TypeError):
                    pass
        if not pts:
            pts = [15.0, 65.0, 190.0, 480.0, 950.0, 1650.0]
    else:
        pts = [15.0, 65.0, 190.0, 480.0, 950.0, 1650.0]

    cur_val = current if current else (f"{int(pts[-1]):,}" if pts else "1,650")

    # Geometry bounds
    pad_left = 68
    pad_right = width - 42
    chart_w = pad_right - pad_left
    pad_top = 66
    pad_bot = height - 44
    chart_h = pad_bot - pad_top

    min_v = 0.0
    max_v = max(pts) if pts else 1000.0
    if max_v <= 0:
        max_v = 100.0

    n = len(pts)
    step_x = chart_w / (n - 1) if n > 1 else chart_w
    coords = []
    for i, val in enumerate(pts):
        cx = pad_left + i * step_x
        ratio = (val - min_v) / (max_v - min_v) if max_v > min_v else 0.5
        cy = pad_bot - ratio * chart_h
        coords.append((cx, cy, val))

    # Outer chassis
    chassis = render_rough_rect(x=2, y=2, w=width-4, h=height-4, stroke=border, stroke_width=1.4, fill=bg, rx=8, seed=360)

    # Top washi tape
    tape_x = width // 2
    washi_tape = f'<polygon points="{tape_x - 45} 0, {tape_x + 45} 0, {tape_x + 36} 13, {tape_x - 54} 13" fill="url(#starSketch-tape)" stroke="{tertiary_col}" stroke-width="0.8" opacity="0.8"/>'

    # Rough X and Y Axes with Arrows
    x_axis = render_rough_arrow(x1=pad_left - 8, y1=pad_bot, x2=pad_right + 16, y2=pad_bot, stroke=border, stroke_width=1.6, arrow_size=6.0, seed=300)
    y_axis = render_rough_arrow(x1=pad_left, y1=pad_bot + 8, x2=pad_left, y2=pad_top - 16, stroke=border, stroke_width=1.6, arrow_size=6.0, seed=305)

    # Y Grid ticks and labels (4 ticks)
    y_ticks = []
    for step in range(4):
        gy = pad_bot - step * (chart_h / 3.0)
        g_val = int(min_v + step * (max_v - min_v) / 3.0)
        v_str = f"{g_val/1000.0:.1f}k" if g_val >= 1000 else str(g_val)
        tick = render_rough_line(pad_left - 6, gy, pad_left, gy, stroke=border, stroke_width=1.2, jitter=0.5, double_stroke=False, seed=370 + step)
        lbl = f'<text x="{pad_left - 10}" y="{gy + 4:.1f}" fill="{text_dim}" font-size="10" text-anchor="end" class="font-sketch-mono">{v_str}</text>'
        if step > 0:
            dashed_grid = f'<line x1="{pad_left}" y1="{gy:.1f}" x2="{pad_right}" y2="{gy:.1f}" stroke="{border}" stroke-width="1" stroke-dasharray="3 4" opacity="0.25"/>'
            y_ticks.append(f"  {dashed_grid}\n  {tick}\n  {lbl}")
        else:
            y_ticks.append(f"  {tick}\n  {lbl}")

    # X Labels
    x_labels = []
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    for i, (cx, cy, val) in enumerate(coords):
        m_idx = (i * 2) % 12
        lbl_txt = months[m_idx] if n > 4 else f"T{i+1}"
        x_labels.append(f'<text x="{cx:.1f}" y="{pad_bot + 18}" fill="{text_dim}" font-size="10" text-anchor="middle" class="font-sketch-mono">{lbl_txt}</text>')

    # Area Hatch Fill Polygon under the line
    area_poly_points = [f"{pad_left:.1f},{pad_bot:.1f}"]
    for cx, cy, val in coords:
        area_poly_points.append(f"{cx:.1f},{cy:.1f}")
    area_poly_points.append(f"{coords[-1][0]:.1f},{pad_bot:.1f}")
    area_markup = f'<polygon points="{" ".join(area_poly_points)}" fill="url(#starSketch-hatch)" />'

    # Hand-drawn organic line segments with slight overshoot and double stroke
    line_segments = []
    for i in range(n - 1):
        p0 = coords[i]
        p1 = coords[i + 1]
        # Slight overshoot at endpoints for authentic sketch look
        dx = p1[0] - p0[0]
        dy = p1[1] - p0[1]
        dist = (dx*dx + dy*dy)**0.5
        ux = (dx / dist) if dist > 0 else 0
        uy = (dy / dist) if dist > 0 else 0
        ext0_x = p0[0] - (ux * 2.0 if i > 0 else 0)
        ext0_y = p0[1] - (uy * 2.0 if i > 0 else 0)
        ext1_x = p1[0] + (ux * 2.0 if i < n - 2 else 0)
        ext1_y = p1[1] + (uy * 2.0 if i < n - 2 else 0)
        line_seg = render_rough_line(ext0_x, ext0_y, ext1_x, ext1_y, stroke=prim, stroke_width=2.5, jitter=1.6, double_stroke=True, seed=320 + i * 7)
        line_segments.append(f"  {line_seg}")

    # Vertices (authentic rough doodle circle nodes)
    dots = []
    for i, (cx, cy, val) in enumerate(coords):
        if i == len(coords) - 1:
            dot_svg = render_rough_circle(cx, cy, r=5.0, stroke=acc, stroke_width=1.8, fill=panel, seed=400 + i * 9)
        else:
            dot_svg = render_rough_circle(cx, cy, r=3.8, stroke=prim, stroke_width=1.4, fill=acc, seed=400 + i * 9)
        dots.append(f"  {dot_svg}")

    # Peak Star Badge & Milestone
    last_x, last_y, _ = coords[-1]
    peak_star = render_rough_star(cx=last_x, cy=last_y - 14, r=7.0, fill=tertiary_col, stroke=tertiary_col, seed=350)
    peak_tag_box = render_rough_rect(x=last_x - 100, y=last_y - 36, w=92, h=20, stroke=acc, stroke_width=1.0, fill=panel, rx=4, seed=355)
    peak_label = f"""  <g>
    {peak_tag_box}
    <text x="{last_x - 54}" y="{last_y - 22}" fill="{tertiary_col}" font-size="10.5" font-weight="700" text-anchor="middle" class="font-sketch">★ {cur_val}</text>
  </g>"""

    joined_y_ticks = "\n".join(y_ticks)
    joined_x_labels = "\n  ".join(x_labels)
    joined_lines = "\n".join(line_segments)
    joined_dots = "\n  ".join(dots)

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">
  <defs>
    <style>
      {css_vars}
{SKETCH_BASE_STYLES}
    </style>
{render_sketch_defs(c, "starSketch")}
  </defs>

  <!-- Sketch Outer Hull -->
  {chassis}
  {washi_tape}

  <!-- Header Info -->
  <text x="24" y="32" fill="{prim}" font-size="14" font-weight="700" class="font-sketch">★ {title_clean} // {repo_clean}</text>
  <text x="{width-24}" y="32" fill="{success}" font-size="12" font-weight="600" text-anchor="end" class="font-sketch">↑ {delta_clean}</text>

  <!-- Axes & Ticks -->
  {x_axis}
  {y_axis}
{joined_y_ticks}
  {joined_x_labels}

  <!-- Pencil Hatching Area Fill -->
  {area_markup}

  <!-- Rough Hand-Drawn Trend Line -->
{joined_lines}

  <!-- Data Vertices & Peak Star -->
  {joined_dots}
  {peak_star}
{peak_label}
</svg>"""

    validate_svg(svg)
    return svg


def generate_starchart(style=None, primary=None, accent=None,
                       repo="Kazinagg/pixel-readme-kit", points=None,
                       current=None, delta="+78% past 6m", title="STAR GROWTH TRAJECTORY",
                       period="6M", width=850, height=230, mode="auto", preset=None, tertiary=None, theme=None):
    """
    Renders an authentic, vector SVG star trend chart / activity chart (850x230).
    Features:
    - Glowing polyline curve and area gradient fill
    - Dynamic coordinate grid with Y-value levels and X-period labels
    - Peak milestone marker with star count callout tag
    - Authentic HUD header plate with live/custom repository stats
    """
    style_name, theme_name = normalize_style_and_theme(style=style, theme=theme)
    c, css_vars = resolve_theme(style=style_name, theme=theme_name, mode=mode, primary=primary, accent=accent, preset=preset, tertiary=tertiary)
    if style_name == "modern":
        return _generate_modern_starchart(
            style_name=style_name, theme_name=theme_name, c=c, css_vars=css_vars,
            repo=repo, points=points, current=current, delta=delta,
            title=title, period=period, width=width, height=height
        )
    elif style_name == "sketch":
        return _generate_sketch_starchart(
            style_name=style_name, theme_name=theme_name, c=c, css_vars=css_vars,
            repo=repo, points=points, current=current, delta=delta,
            title=title, period=period, width=width, height=height
        )
    prim = c["primary"]
    acc = c["accent"]
    bg = c["bg"]
    panel = c["panel"]
    border = c["border"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]
    success = c["success"]
    if theme_name in ("tactical", "amber", "amber_crt"):
        st = "tactical"
    elif theme_name in ("minimal", "clean-mono", "clean_mono", "academic-paper", "academic_paper", "corporate-blue", "corporate_blue", "tokyo", "tokyo_night", "swiss-mono", "swiss_mono", "executive-slate", "executive_slate"):
        st = "minimal"
    else:
        st = "cyberpunk"

    title_clean = escape_xml(title.upper())
    repo_clean = escape_xml(repo.strip())
    delta_clean = escape_xml(delta)

    # Parse points
    if points is None:
        pts = [15.0, 65.0, 190.0, 480.0, 950.0, 1650.0]
    elif isinstance(points, str):
        pts = []
        for x in points.split(","):
            x = x.strip()
            if x:
                try:
                    pts.append(float(x))
                except ValueError:
                    pass
        if not pts:
            pts = [15.0, 65.0, 190.0, 480.0, 950.0, 1650.0]
    elif isinstance(points, (list, tuple)):
        pts = [float(x) for x in points if x is not None]
        if not pts:
            pts = [15.0, 65.0, 190.0, 480.0, 950.0, 1650.0]
    else:
        pts = [15.0, 65.0, 190.0, 480.0, 950.0, 1650.0]

    cur_val = current if current else (f"{int(pts[-1]):,}" if pts else "1,650")

    # Geometry bounds
    pad_left = 75
    pad_right = 800
    chart_w = pad_right - pad_left
    pad_top = 70
    pad_bot = 185
    chart_h = pad_bot - pad_top

    min_v = 0.0
    max_v = max(pts) if pts else 1000.0
    if max_v <= 0:
        max_v = 100.0

    # Calculate coordinates
    n = len(pts)
    step_x = chart_w / (n - 1) if n > 1 else chart_w
    coords = []
    for i, val in enumerate(pts):
        cx = pad_left + i * step_x
        ratio = (val - min_v) / (max_v - min_v) if max_v > min_v else 0.5
        cy = pad_bot - ratio * chart_h
        coords.append((cx, cy, val))

    # Polyline and area paths
    line_points_str = " ".join(f"{cx:.1f},{cy:.1f}" for cx, cy, _ in coords)
    first_x, first_y = coords[0][0], coords[0][1]
    last_x, last_y = coords[-1][0], coords[-1][1]
    area_path = f"M {first_x:.1f} {pad_bot} L " + " L ".join(f"{cx:.1f} {cy:.1f}" for cx, cy, _ in coords) + f" L {last_x:.1f} {pad_bot} Z"

    # Grid lines (4 horizontal)
    grid_lines = []
    y_labels = []
    for step in range(4):
        gy = pad_bot - step * (chart_h / 3.0)
        g_val = int(min_v + step * (max_v - min_v) / 3.0)
        v_str = f"{g_val/1000.0:.1f}k" if g_val >= 1000 else str(g_val)
        grid_lines.append(f'<line x1="{pad_left}" y1="{gy:.1f}" x2="{pad_right}" y2="{gy:.1f}" stroke="{border}" stroke-width="1" stroke-dasharray="4 4" opacity="0.6"/>')
        y_labels.append(f'<text x="{pad_left - 10}" y="{gy + 4:.1f}" fill="{text_dim}" font-size="10" text-anchor="end" class="font-mono">{v_str}</text>')

    # Vertical ticks & X labels
    x_ticks = []
    x_labels = []
    month_names = ["M-5", "M-4", "M-3", "M-2", "M-1", "NOW"]
    for i, (cx, cy, val) in enumerate(coords):
        lbl = month_names[i] if i < len(month_names) else f"T{i+1}"
        x_ticks.append(f'<line x1="{cx:.1f}" y1="{pad_top}" x2="{cx:.1f}" y2="{pad_bot}" stroke="{border}" stroke-width="0.8" stroke-dasharray="2 4" opacity="0.35"/>')
        x_labels.append(f'<text x="{cx:.1f}" y="{pad_bot + 18}" fill="{text_dim}" font-size="10.5" font-weight="bold" text-anchor="middle" class="font-mono">{lbl}</text>')

    # Peak Callout Tag & Data points circles
    dots = []
    callout_text = f"★ {cur_val}"
    callout_w = max(76, int(measure_mono_text_width(callout_text, 11) + 20))

    callout_rx = "0" if st == "minimal" else "3"
    for i, (cx, cy, val) in enumerate(coords):
        if i == len(coords) - 1:
            tag_y = cy + 12 if cy < 65 else cy - 30
            tag_x = max(pad_left, min(width - callout_w - 14, cx - callout_w // 2))
            dots.append(f"""
    <!-- Peak Milestone Marker -->
    <circle cx="{cx:.1f}" cy="{cy:.1f}" r="8" fill="{acc}" opacity="0.25"/>
    <circle cx="{cx:.1f}" cy="{cy:.1f}" r="5.5" fill="{bg}" stroke="{acc}" stroke-width="2"/>
    <circle cx="{cx:.1f}" cy="{cy:.1f}" r="2.5" fill="{prim}"/>
    <!-- Peak Callout Tag -->
    <g transform="translate({tag_x:.1f}, {tag_y:.1f})">
      <rect x="0" y="0" width="{callout_w}" height="22" rx="{callout_rx}" fill="{panel}" stroke="{acc}" stroke-width="1.2"/>
      <text x="{callout_w // 2}" y="15" fill="{acc}" font-size="11" font-weight="bold" text-anchor="middle" class="font-mono">{callout_text}</text>
    </g>""")
        else:
            dots.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="3.5" fill="{panel}" stroke="{prim}" stroke-width="1.8"/>')

    if st == "tactical":
        chassis = f"""
  <polygon points="12 1, {width-12} 1, {width-1} 12, {width-1} {height-12}, {width-12} {height-1}, 12 {height-1}, 1 {height-12}, 1 12"
           fill="{bg}" stroke="{border}" stroke-width="1.5"/>
  <rect x="1" y="1" width="12" height="12" fill="{prim}"/>
  <rect x="{width-13}" y="{height-13}" width="12" height="12" fill="{acc}"/>
  <line x1="20" y1="1" x2="60" y2="1" stroke="{prim}" stroke-width="2"/>
"""
    elif st in ("minimal", "clean-mono", "corporate-blue", "academic-paper", "modern-slate"):
        chassis = f"""
  <!-- TOKYO MINIMAL CHASSIS (Sharp 90° corners, 1px Swiss frame, bold accent top banner) -->
  <rect x="1" y="1" width="{width-2}" height="{height-2}" fill="{bg}" stroke="{border}" stroke-width="1.0"/>
  <rect x="1" y="1" width="{width-2}" height="5" fill="{prim}"/>
  <line x1="1" y1="{height-2}" x2="{width-1}" y2="{height-2}" stroke="{border}" stroke-width="1.0" stroke-dasharray="4,4" opacity="0.4"/>
"""
    else:  # cyberpunk
        chassis = f"""
  <rect x="1" y="1" width="{width-2}" height="{height-2}" fill="{bg}" stroke="{border}" stroke-width="1.5"/>
  <rect x="1" y="1" width="8" height="8" fill="{prim}"/>
  <rect x="{width-9}" y="1" width="8" height="8" fill="{acc}"/>
  <rect x="1" y="{height-9}" width="8" height="8" fill="{acc}"/>
  <rect x="{width-9}" y="{height-9}" width="8" height="8" fill="{prim}"/>
"""

    # Dynamic Stats Badges
    badge1_text = f"★ {cur_val}"
    badge1_w = max(90, int(measure_mono_text_width(badge1_text, 12) + 24))
    badge2_text = delta_clean
    badge2_w = max(90, int(measure_mono_text_width(badge2_text, 11) + 24))
    badges_total_w = badge1_w + 8 + badge2_w
    badges_x = width - badges_total_w - 20

    # Dynamic Header Bar and Title / Repo Positioning
    max_hdr_w = badges_x - 32
    title_disp = f"★ {title_clean}"
    title_w = measure_mono_text_width(title_disp, 11.5)

    if title_w > max_hdr_w - 30:
        title_disp = clamp_text_to_width(title_disp, max_hdr_w - 30, 11.5)
        title_w = measure_mono_text_width(title_disp, 11.5)
        repo_markup = ""
        bar_w = int(title_w + 26)
    else:
        repo_disp = f"// {repo_clean}"
        avail_repo_w = max_hdr_w - title_w - 35
        if avail_repo_w >= 40:
            repo_disp = clamp_text_to_width(repo_disp, avail_repo_w, 11)
            repo_x = int(32 + title_w + 14)
            repo_markup = f'<text x="{repo_x}" y="35" fill="{text_dim}" font-size="11" class="font-mono">{repo_disp}</text>'
            bar_w = int(repo_x + measure_mono_text_width(repo_disp, 11) + 14)
        else:
            repo_markup = ""
            bar_w = int(title_w + 26)

    bar_w = min(max_hdr_w, max(260, bar_w))

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
    </style>
    <linearGradient id="grad-star-area" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" stop-color="{prim}" stop-opacity="0.32"/>
      <stop offset="100%" stop-color="{prim}" stop-opacity="0.01"/>
    </linearGradient>
  </defs>

  {chassis}

  <!-- HEADER BAR -->
  <rect x="20" y="16" width="{bar_w}" height="28" fill="{panel}" stroke="{border}" stroke-width="1"/>
  <rect x="20" y="16" width="4" height="28" fill="{prim}"/>
  <text x="32" y="35" fill="{prim}" font-size="11.5" font-weight="bold" letter-spacing="0.5px" class="font-mono">{title_disp}</text>
  {repo_markup}

  <!-- STATS BADGES -->
  <g transform="translate({badges_x}, 16)">
    <rect x="0" y="0" width="{badge1_w}" height="28" fill="{panel}" stroke="{prim}" stroke-width="1"/>
    <text x="{badge1_w // 2}" y="19" fill="{prim}" font-size="12" font-weight="bold" text-anchor="middle" class="font-mono">{badge1_text}</text>
    <rect x="{badge1_w + 8}" y="0" width="{badge2_w}" height="28" fill="{panel}" stroke="{acc}" stroke-width="1"/>
    <text x="{badge1_w + 8 + badge2_w // 2}" y="19" fill="{acc}" font-size="11" font-weight="bold" text-anchor="middle" class="font-mono">{badge2_text}</text>
  </g>

  <!-- GRID & AXES -->
  {"".join(grid_lines)}
  {"".join(y_labels)}
  {"".join(x_ticks)}
  {"".join(x_labels)}

  <!-- CHART AREA & LINE -->
  <path d="{area_path}" fill="url(#grad-star-area)" shape-rendering="geometricPrecision"/>
  <path d="M {line_points_str.replace(' ', ' L ')}" fill="none" stroke="{prim}" stroke-width="2.5" shape-rendering="geometricPrecision"/>

  <!-- DATA VERTICES -->
  {"".join(dots)}
</svg>"""

    validate_svg(svg)
    return svg

# ==============================================================================
def _generate_modern_profile_card(style_name, theme_name, c, css_vars,
                                   name="ALEX DEVELOPER", role="FULLSTACK & SYSTEMS ARCHITECT",
                                   bio="Building high-performance runtimes and resilient developer tooling.",
                                   status="AVAILABLE FOR HIRE", location="REMOTE // UTC+3",
                                   badge="LEVEL_99", width=850, height=190):
    """Renders a flagship modern developer dossier / profile header card (850x190)."""
    prim = c["primary"]
    acc = c["accent"]
    tertiary_col = c["tertiary"]
    bg = c["bg"]
    panel = c["panel"]
    border = c["border"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]
    success = c["success"]

    name_clean = escape_xml(name)
    role_clean = escape_xml(role)
    bio_clean = escape_xml(bio)
    status_clean = escape_xml(status.upper())
    loc_clean = escape_xml(location)
    badge_clean = escape_xml(badge)

    av_x, av_y, av_size = 28, 28, 134
    av_cx, av_cy = av_x + av_size // 2, av_y + av_size // 2 - 8

    # Pills top right
    badge_disp = clamp_sans_text_to_width(badge_clean, 120, 10.5)
    badge_w = max(68, int(measure_sans_text_width(badge_disp, 10.5) + 24))
    loc_disp = clamp_sans_text_to_width(loc_clean, 160, 10.5)
    loc_w = max(90, int(measure_sans_text_width(loc_disp, 10.5) + 24))
    pills_gap = 8
    pills_total_w = badge_w + pills_gap + loc_w
    pills_x = width - pills_total_w - 24

    # Name and role sizing
    content_x = 180
    max_name_w = pills_x - content_x - 16
    name_fs = 26 if len(name) <= 20 else (22 if len(name) <= 28 else 18)
    name_disp = clamp_sans_text_to_width(name_clean, max_name_w, name_fs)

    role_disp = clamp_sans_text_to_width(role_clean, width - content_x - 40, 12)
    role_w = max(120, int(measure_sans_text_width(role_disp, 12) + 24))

    bio_disp = clamp_sans_text_to_width(bio_clean, width - content_x - 40, 12.5)

    status_short = "AVAILABLE" if "AVAILABLE" in status_clean else ("ACTIVE" if "ACTIVE" in status_clean else status_clean[:12])
    status_disp = clamp_sans_text_to_width(status_short, 80, 9.5)
    status_pill_w = max(84, int(measure_sans_text_width(status_disp, 9.5) + 32))
    status_pill_x = av_cx - status_pill_w // 2

    defs_markup = render_modern_defs(c, "modern-profile")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">
  <defs>
    {defs_markup}
    <style>
      {css_vars}
      {MODERN_BASE_STYLES}
    </style>
  </defs>

  <!-- CHASSIS -->
  <rect x="2" y="2" width="{width-4}" height="{height-4}" rx="14" fill="{bg}" stroke="url(#modern-profile-border-grad)" stroke-width="1.2"/>
  <path d="M 16 2 L {width-16} 2" stroke="url(#modern-profile-accent-grad)" stroke-width="2" stroke-linecap="round"/>

  <!-- CIRCULAR AVATAR WITH GRADIENT RING -->
  <g>
    <!-- Outer halo ring -->
    <circle cx="{av_cx}" cy="{av_cy}" r="46" fill="none" stroke="url(#modern-profile-accent-grad)" stroke-width="2"/>
    <!-- Inner panel circle -->
    <circle cx="{av_cx}" cy="{av_cy}" r="43" fill="{panel}"/>
    <!-- Vector User Silhouette -->
    <circle cx="{av_cx}" cy="{av_cy-10}" r="15" fill="{bg}" stroke="{prim}" stroke-width="1.8"/>
    <path d="M {av_cx-24} {av_cy+26} C {av_cx-24} {av_cy+8}, {av_cx+24} {av_cy+8}, {av_cx+24} {av_cy+26} Z" fill="{bg}" stroke="{prim}" stroke-width="1.8"/>
    <circle cx="{av_cx}" cy="{av_cy-10}" r="5" fill="{acc}"/>
  </g>

  <!-- STATUS PILL (UNDER AVATAR) -->
  <g transform="translate({status_pill_x}, {av_y + av_size - 18})">
    <rect x="0" y="0" width="{status_pill_w}" height="20" rx="10" fill="{panel}" stroke="{border}" stroke-width="1"/>
    <circle cx="12" cy="10" r="3" fill="{success}"/>
    <text x="20" y="13.5" fill="{success}" font-size="9.5" font-weight="700" class="font-sans">{status_disp}</text>
  </g>

  <!-- BADGE AND LOCATION PILLS (TOP RIGHT) -->
  <g transform="translate({pills_x}, 24)">
    <rect x="0" y="0" width="{badge_w}" height="24" rx="12" fill="{panel}" stroke="{acc}" stroke-width="1"/>
    <text x="{badge_w // 2}" y="16" fill="{acc}" font-size="10.5" font-weight="700" text-anchor="middle" class="font-sans">{badge_disp}</text>
    <rect x="{badge_w + pills_gap}" y="0" width="{loc_w}" height="24" rx="12" fill="{panel}" stroke="{border}" stroke-width="1"/>
    <text x="{badge_w + pills_gap + loc_w // 2}" y="16" fill="{text_dim}" font-size="10.5" font-weight="500" text-anchor="middle" class="font-sans">{loc_disp}</text>
  </g>

  <!-- NAME TYPOGRAPHY -->
  <text x="{content_x}" y="56" fill="url(#modern-profile-accent-grad)" font-size="{name_fs}" font-weight="800" letter-spacing="-0.02em" class="font-sans">{name_disp}</text>

  <!-- ROLE PILL -->
  <g transform="translate({content_x}, 72)">
    <rect x="0" y="0" width="{role_w}" height="24" rx="12" fill="{panel}" stroke="{border}" stroke-width="1"/>
    <text x="12" y="16" fill="{acc}" font-size="11.5" font-weight="600" class="font-sans">{role_disp}</text>
  </g>

  <!-- BIO SUMMARY -->
  <text x="{content_x}" y="128" fill="{text_main}" font-size="12.5" font-weight="400" class="font-sans">{bio_disp}</text>
</svg>"""

    validate_svg(svg)
    return svg

def _generate_sketch_profile_card(style_name, theme_name, c, css_vars,
                                   name="ALEX DEVELOPER", role="FULLSTACK & SYSTEMS ARCHITECT",
                                   bio="Building high-performance runtimes and resilient developer tooling.",
                                   status="AVAILABLE FOR HIRE", location="REMOTE // UTC+3",
                                   badge="LEVEL_99", width=850, height=190):
    """Renders a flagship hand-drawn sketch developer dossier card (850x190) with washi tape and doodle details."""
    prim = c["primary"]
    acc = c["accent"]
    tertiary_col = c["tertiary"]
    bg = c["bg"]
    panel = c["panel"]
    border = c["border"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]
    success = c["success"]

    name_clean = escape_xml(name)
    role_clean = escape_xml(role)
    bio_clean = escape_xml(bio)
    status_clean = escape_xml(status.upper())
    loc_clean = escape_xml(location)
    badge_clean = escape_xml(badge)

    # Outer hull
    hull = render_rough_rect(4, 4, width - 8, height - 8, stroke=border, fill=bg, stroke_width=1.6, seed=89, overshoot=3)

    # Polaroid photo frame on left
    av_x, av_y, av_w, av_h = 24, 20, 116, 148
    photo_hull = render_rough_rect(av_x, av_y, av_w, av_h, stroke=border, fill=panel, stroke_width=1.4, seed=37, overshoot=2)
    photo_tape = f'<polygon points="{av_x + av_w//2 - 24} {av_y - 6}, {av_x + av_w//2 + 24} {av_y - 6}, {av_x + av_w//2 + 20} {av_y + 10}, {av_x + av_w//2 - 28} {av_y + 10}" fill="url(#profileSketch-tape)"/>'
    photo_box = render_rough_rect(av_x + 8, av_y + 12, av_w - 16, 96, stroke=border, fill=bg, stroke_width=1.0, seed=42, overshoot=1)

    # Hand-drawn developer avatar doodle
    av_cx = av_x + av_w // 2
    av_head_cy = av_y + 46
    doodle_avatar = f"""  <g>
    <circle cx="{av_cx}" cy="{av_head_cy}" r="17" fill="none" stroke="{prim}" stroke-width="1.8"/>
    <circle cx="{av_cx - 5}" cy="{av_head_cy - 1}" r="1.5" fill="{prim}"/>
    <circle cx="{av_cx + 5}" cy="{av_head_cy - 1}" r="1.5" fill="{prim}"/>
    <path d="M {av_cx - 6} {av_head_cy + 7} Q {av_cx} {av_head_cy + 12} {av_cx + 6} {av_head_cy + 7}" fill="none" stroke="{prim}" stroke-width="1.6" stroke-linecap="round"/>
    <path d="M {av_x + 18} {av_y + 98} Q {av_cx} {av_y + 72} {av_x + av_w - 18} {av_y + 98}" fill="none" stroke="{prim}" stroke-width="1.8" stroke-linecap="round"/>
  </g>"""

    # Status text under photo
    status_short = "AVAILABLE" if "AVAILABLE" in status_clean else ("ACTIVE" if "ACTIVE" in status_clean else status_clean[:12])
    status_markup = f'<text x="{av_cx}" y="{av_y + 130}" fill="{success}" font-size="10.5" font-weight="700" text-anchor="middle" class="font-sketch">● {status_short}</text>'

    # Top-right badge and location pills
    badge_disp = clamp_sans_text_to_width(badge_clean, 120, 11)
    badge_w = max(70, int(measure_sans_text_width(badge_disp, 11) + 24))
    loc_disp = clamp_sans_text_to_width(loc_clean, 160, 11)
    loc_w = max(90, int(measure_sans_text_width(loc_disp, 11) + 24))
    pills_gap = 12
    pills_total_w = badge_w + pills_gap + loc_w
    pills_x = width - pills_total_w - 24

    badge_box = render_rough_rect(pills_x, 20, badge_w, 24, stroke=acc, fill=panel, stroke_width=1.2, seed=61, overshoot=2)
    loc_box = render_rough_rect(pills_x + badge_w + pills_gap, 20, loc_w, 24, stroke=border, fill=panel, stroke_width=1.2, seed=62, overshoot=2)

    # Name, underline and typography
    content_x = 162
    max_name_w = pills_x - content_x - 16
    name_fs = 26 if len(name) <= 20 else (22 if len(name) <= 28 else 18)
    name_disp = clamp_sans_text_to_width(name_clean, max_name_w, name_fs)
    name_w = int(measure_sans_text_width(name_disp, name_fs))
    name_underline = render_rough_line(content_x, 60, content_x + min(name_w + 14, max_name_w), 60, stroke=acc, stroke_width=2.4, seed=73, jitter=1.2)

    # Role sticker
    role_disp = clamp_sans_text_to_width(role_clean, width - content_x - 40, 12)
    role_w = max(120, int(measure_sans_text_width(role_disp, 12) + 26))
    role_box = render_rough_rect(content_x, 74, role_w, 24, stroke=tertiary_col, fill=panel, stroke_width=1.2, seed=84, overshoot=2)

    # Bio
    bio_disp = clamp_sans_text_to_width(bio_clean, width - content_x - 30, 13)

    # Sign-off doodle star
    star_doodle = render_rough_star(width - 130, height - 23, r=7, fill="none", stroke=acc, stroke_width=1.2, seed=99)

    defs_markup = render_sketch_defs(c, "profileSketch")

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%">
  <defs>
    {defs_markup}
    <style>
      {css_vars}
      {SKETCH_BASE_STYLES}
    </style>
  </defs>

  <!-- Chassis -->
  {hull}

  <!-- Polaroid Avatar -->
  {photo_hull}
  {photo_tape}
  {photo_box}
{doodle_avatar}
  {status_markup}

  <!-- Top Right Pills -->
  {badge_box}
  <text x="{pills_x + badge_w // 2}" y="36" fill="{acc}" font-size="11" font-weight="700" text-anchor="middle" class="font-sketch">★ {badge_disp}</text>
  {loc_box}
  <text x="{pills_x + badge_w + pills_gap + loc_w // 2}" y="36" fill="{text_dim}" font-size="11" font-weight="500" text-anchor="middle" class="font-sketch">{loc_disp}</text>

  <!-- Name & Underline -->
  <text x="{content_x}" y="52" fill="{prim}" font-size="{name_fs}" font-weight="700" class="font-sketch">{name_disp}</text>
  {name_underline}

  <!-- Role Sticker -->
  {role_box}
  <text x="{content_x + 10}" y="90" fill="{tertiary_col}" font-size="12" font-weight="600" class="font-sketch">{role_disp}</text>

  <!-- Bio -->
  <text x="{content_x}" y="128" fill="{text_main}" font-size="13" font-weight="500" class="font-sketch">{bio_disp}</text>

  <!-- Draft Note & Star -->
  {star_doodle}
  <text x="{width - 28}" y="{height - 20}" fill="{text_dim}" font-size="10.5" font-weight="600" text-anchor="end" class="font-sketch">// signed profile</text>
</svg>"""

    validate_svg(svg)
    return svg

def generate_profile_card(style=None, primary=None, accent=None,
                          name="ALEX DEVELOPER", role="FULLSTACK & SYSTEMS ARCHITECT",
                          bio="Building high-performance runtimes and resilient developer tooling.",
                          status="AVAILABLE FOR HIRE", location="REMOTE // UTC+3",
                          badge="LEVEL_99", width=850, height=190, mode="auto", preset=None,
                          tertiary=None, theme=None):
    """
    Renders a flagship developer dossier / identity header card (850x190) for GitHub Profiles.
    Features:
    - Stylized cyber avatar frame with status LED ring
    - 3D Typography name header and role descriptor
    - Clean manifesto / bio summary section
    - Multi-mode theming and responsive vector geometry
    """
    style_name, theme_name = normalize_style_and_theme(style=style, theme=theme)
    c, css_vars = resolve_theme(style=style_name, theme=theme_name, mode=mode, primary=primary, accent=accent, preset=preset, tertiary=tertiary)
    if style_name == "modern":
        return _generate_modern_profile_card(
            style_name=style_name, theme_name=theme_name, c=c, css_vars=css_vars,
            name=name, role=role, bio=bio, status=status, location=location,
            badge=badge, width=width, height=height
        )
    elif style_name == "sketch":
        return _generate_sketch_profile_card(
            style_name=style_name, theme_name=theme_name, c=c, css_vars=css_vars,
            name=name, role=role, bio=bio, status=status, location=location,
            badge=badge, width=width, height=height
        )
    prim = c["primary"]
    acc = c["accent"]
    bg = c["bg"]
    panel = c["panel"]
    border = c["border"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]
    success = c["success"]
    if theme_name in ("tactical", "amber", "amber_crt") or style_name == "tactical":
        st = "tactical"
    elif theme_name in ("minimal", "tokyo", "tokyo_night", "clean-mono", "clean_mono", "swiss-mono", "swiss_mono") or style_name == "minimal":
        st = "minimal"
    elif theme_name in ("academic-paper", "academic_paper", "corporate-blue", "corporate_blue", "enterprise-navy", "enterprise_navy", "executive-slate", "executive_slate") or style_name == "corporate":
        st = "corporate"
    elif theme_name in ("slate-dark", "slate_dark", "nordic-frost", "nordic_frost", "linear-violet", "linear_violet", "emerald-clean", "emerald_clean", "modern-clean") or style_name == "modern":
        st = "modern"
    else:
        st = "cyberpunk"

    name_clean = escape_xml(name.upper())
    role_clean = escape_xml(role.upper())
    bio_clean = escape_xml(bio)
    status_clean = escape_xml(status.upper())
    loc_clean = escape_xml(location.upper())
    badge_clean = escape_xml(badge.upper())

    # Available width for name and header items
    av_x, av_y, av_size = 28, 28, 134
    max_name_w = width - 180 - 40

    # Dynamic badges and status pills (top right)
    badge_disp = clamp_text_to_width(badge_clean, 120, 10.5)
    badge_w = max(70, int(measure_mono_text_width(badge_disp, 10.5) + 20))
    status_disp = clamp_text_to_width(status_clean, 160, 10)
    status_w = max(90, int(measure_mono_text_width(status_disp, 10) + 32))
    pills_gap = 8
    pills_total_w = badge_w + pills_gap + status_w
    pills_x = width - pills_total_w - 20

    # Top breadcrumb dossier
    avail_dossier_w = max(60, pills_x - 180 - 15)
    if st == "tactical":
        dossier_prefix = "■ TAC_ID // "
    elif st == "minimal":
        dossier_prefix = "■ MINIMAL // "
    elif st in ("modern", "corporate"):
        dossier_prefix = "DOSSIER // "
    else:
        dossier_prefix = "■ CYBER_ID // "
    dossier_full = f"{dossier_prefix}{loc_clean}"
    dossier_disp = clamp_text_to_width(dossier_full, avail_dossier_w - 24, 11)
    dossier_w = max(120, min(avail_dossier_w, int(measure_mono_text_width(dossier_disp, 11) + 24)))

    # Role and Bio sizing
    max_role_w = width - 180 - 30
    role_disp = clamp_text_to_width(f"▶ {role_clean}", max_role_w - 28, 12)
    role_w = max(160, min(max_role_w, int(measure_mono_text_width(role_disp, 12) + 28)))
    bio_disp = clamp_text_to_width(bio_clean, width - 180 - 30, 12)

    # -------------------------------------------------------------
    # 1. TACTICAL HUD PARADIGM (MIL-SPEC armored casing & crosshairs)
    # -------------------------------------------------------------
    if st == "tactical":
        chassis = f"""
  <!-- TACTICAL ARMORED CHASSIS -->
  <polygon points="16 1, {width-16} 1, {width-1} 16, {width-1} {height-16}, {width-16} {height-1}, 16 {height-1}, 1 {height-16}, 1 16"
           fill="{bg}" stroke="{border}" stroke-width="1.8"/>
  <rect x="1" y="16" width="4" height="24" fill="{prim}"/>
  <rect x="{width-5}" y="{height-40}" width="4" height="24" fill="{acc}"/>
  <!-- Reticle Crosshair Marks -->
  <line x1="20" y1="10" x2="28" y2="10" stroke="{prim}" stroke-width="1.5"/>
  <line x1="24" y1="6" x2="24" y2="14" stroke="{prim}" stroke-width="1.5"/>
  <line x1="{width-28}" y1="10" x2="{width-20}" y2="10" stroke="{acc}" stroke-width="1.5"/>
  <line x1="{width-24}" y1="6" x2="{width-24}" y2="14" stroke="{acc}" stroke-width="1.5"/>
  <!-- Telemetry Grate (Bottom Right) -->
  <rect x="{width-80}" y="{height-12}" width="3" height="6" fill="{acc}"/>
  <rect x="{width-73}" y="{height-12}" width="3" height="6" fill="{acc}"/>
  <rect x="{width-66}" y="{height-12}" width="3" height="6" fill="{acc}"/>
  <rect x="{width-59}" y="{height-12}" width="3" height="6" fill="{acc}"/>
  <text x="24" y="{height-8}" fill="{text_dim}" font-size="8.5" class="font-mono">MIL-STD-810 // HUD_TELEMETRY // SYS_ID:0x884F</text>
"""
        avatar_markup = f"""
  <!-- TACTICAL AVATAR & RANGEFINDER RETICLE -->
  <g transform="translate({av_x}, {av_y})">
    <polygon points="10 0, {av_size-10} 0, {av_size} 10, {av_size} {av_size-10}, {av_size-10} {av_size}, 10 {av_size}, 0 {av_size-10}, 0 10"
             fill="{panel}" stroke="{border}" stroke-width="1.8"/>
    <!-- Azimuth Rangefinder Ring -->
    <circle cx="{av_size//2}" cy="54" r="38" fill="none" stroke="{prim}" stroke-width="1.2" stroke-dasharray="3 4"/>
    <circle cx="{av_size//2}" cy="54" r="46" fill="none" stroke="{border}" stroke-width="0.8"/>
    <!-- Reticle Crosshair Ticks -->
    <line x1="{av_size//2}" y1="10" x2="{av_size//2}" y2="22" stroke="{acc}" stroke-width="1.5"/>
    <line x1="{av_size//2}" y1="86" x2="{av_size//2}" y2="98" stroke="{acc}" stroke-width="1.5"/>
    <line x1="14" y1="54" x2="26" y2="54" stroke="{acc}" stroke-width="1.5"/>
    <line x1="{av_size-26}" y1="54" x2="{av_size-14}" y2="54" stroke="{acc}" stroke-width="1.5"/>
    <!-- Operator Silhouette -->
    <circle cx="{av_size//2}" cy="50" r="16" fill="{bg}" stroke="{prim}" stroke-width="2"/>
    <path d="M 32 94 L 46 78 L {av_size-46} 78 L {av_size-32} 94 Z" fill="{bg}" stroke="{prim}" stroke-width="2"/>
    <circle cx="{av_size//2}" cy="50" r="6" fill="{acc}"/>
    <!-- Tactical Readiness Status Bar -->
    <rect x="8" y="110" width="{av_size-16}" height="16" fill="{bg}" stroke="{acc}" stroke-width="1"/>
    <text x="{av_size//2}" y="122" fill="{acc}" font-size="8.5" font-weight="bold" text-anchor="middle" class="font-mono">HUD // ACTIVE</text>
  </g>
"""
        lines, calc_px = calculate_smart_layout(name, max_width=max_name_w, default_px_size=5, min_px_size=3, spacing=2, allow_wrap=False)
        single_name = lines[0] if lines else name
        name_markup, _, _ = render_3d_text(
            single_name, x=180, y=58, px_size=calc_px,
            front_color=c["title_front"], mid_shadow=c["title_mid"], dark_shadow=c["title_dark"],
            spacing=2, max_width=max_name_w, allow_wrap=False
        )
        role_markup = f"""
  <g transform="translate(180, 116)">
    <polygon points="0 0, {role_w-8} 0, {role_w} 8, {role_w} 26, 0 26" fill="{panel}" stroke="{prim}" stroke-width="1.2"/>
    <rect x="0" y="0" width="5" height="26" fill="{prim}"/>
    <text x="14" y="17" fill="{acc}" font-size="11.5" font-weight="bold" class="font-mono">{role_disp}</text>
  </g>
"""

    # -------------------------------------------------------------
    # 2. TOKYO MINIMAL PARADIGM (Sharp 90°, Swiss 1px grid, top accent banner)
    # -------------------------------------------------------------
    elif st == "minimal":
        chassis = f"""
  <!-- TOKYO MINIMAL CHASSIS (Sharp 90°, 1px Swiss frame, bold accent top banner) -->
  <rect x="1" y="1" width="{width-2}" height="{height-2}" fill="{bg}" stroke="{border}" stroke-width="1.0"/>
  <rect x="1" y="1" width="{width-2}" height="5" fill="{prim}"/>
  <line x1="8" y1="{height-2}" x2="{width-8}" y2="{height-2}" stroke="{prim}" stroke-width="1.0" stroke-dasharray="4,4" opacity="0.35"/>
  <text x="{width-18}" y="{height-10}" fill="{text_dim}" font-size="8.5" text-anchor="end" class="font-mono">MINIMAL SPEC // VERIFIED</text>
"""
        avatar_markup = f"""
  <!-- MINIMAL MATRIX AVATAR (Sharp 90°, Crosshair grid) -->
  <g transform="translate({av_x}, {av_y})">
    <rect x="0" y="0" width="{av_size}" height="{av_size}" fill="{panel}" stroke="{border}" stroke-width="1.0"/>
    <circle cx="{av_size//2}" cy="48" r="22" fill="{bg}" stroke="{prim}" stroke-width="1.5"/>
    <path d="M 28 98 C 28 76, {av_size-28} 76, {av_size-28} 98 Z" fill="{bg}" stroke="{prim}" stroke-width="1.5"/>
    <circle cx="{av_size//2}" cy="48" r="6" fill="{acc}"/>
    <!-- Sharp status bar -->
    <rect x="8" y="108" width="{av_size-16}" height="18" fill="{bg}" stroke="{border}" stroke-width="1.0"/>
    <circle cx="20" cy="117" r="3" fill="{success}"/>
    <text x="30" y="120" fill="{success}" font-size="8.5" font-weight="600" class="font-mono">ACTIVE</text>
  </g>
"""
        calc_font_size = 26
        while calc_font_size > 14 and measure_mono_text_width(name_clean, calc_font_size) > max_name_w:
            calc_font_size -= 2
        name_markup = f"""  <text x="180" y="78" fill="{c['title_front']}" font-size="{calc_font_size}" font-weight="700" letter-spacing="0.04em" class="font-mono">{name_clean}</text>"""

        role_markup = f"""
  <g transform="translate(180, 116)">
    <rect x="0" y="0" width="{role_w}" height="26" fill="{panel}" stroke="{border}" stroke-width="1.0"/>
    <rect x="0" y="0" width="3" height="26" fill="{prim}"/>
    <text x="12" y="17" fill="{acc}" font-size="11.5" font-weight="600" class="font-mono">{role_disp}</text>
  </g>
"""

    # -------------------------------------------------------------
    # 3. MODERN & CORPORATE & ACADEMIC PARADIGM (Pure Vector Cleanliness)
    # -------------------------------------------------------------
    elif st in ("modern", "corporate"):
        is_academic_corp = theme_name in ("academic-paper", "academic_paper", "corporate-blue", "corporate_blue",
                                          "enterprise-navy", "enterprise_navy", "swiss-mono", "swiss_mono", "clean-mono", "clean_mono") or style_name == "corporate"
        if is_academic_corp:
            chassis = f"""
  <!-- CORPORATE / ACADEMIC FORMAL SPECIFICATION DOSSIER -->
  <rect x="1" y="1" width="{width-2}" height="{height-2}" fill="{bg}" stroke="{border}" stroke-width="1.5"/>
  <rect x="5" y="5" width="{width-10}" height="{height-10}" fill="none" stroke="{border}" stroke-width="0.8" opacity="0.6"/>
  <line x1="5" y1="5" x2="{width-5}" y2="5" stroke="{prim}" stroke-width="2.5"/>
  <line x1="5" y1="{height-5}" x2="{width-5}" y2="{height-5}" stroke="{border}" stroke-width="1"/>
  <text x="{width-18}" y="{height-10}" fill="{text_dim}" font-size="8.5" text-anchor="end" class="font-mono">IDENTIFICATION PROTOCOL // VERIFIED</text>
"""
        else:
            chassis = f"""
  <!-- MODERN CLEAN VECTOR CARD -->
  <rect x="1" y="1" width="{width-2}" height="{height-2}" rx="10" fill="{bg}" stroke="{border}" stroke-width="1.2"/>
  <path d="M 12 1 L {width-12} 1" stroke="{prim}" stroke-width="2.5" stroke-linecap="round"/>
"""

        avatar_markup = f"""
  <!-- CLEAN MINIMALIST AVATAR -->
  <g transform="translate({av_x}, {av_y})">
    <rect x="0" y="0" width="{av_size}" height="{av_size}" rx="12" fill="{panel}" stroke="{border}" stroke-width="1.2"/>
    <!-- Smooth User Silhouette (Pure Vector) -->
    <circle cx="{av_size//2}" cy="48" r="22" fill="{bg}" stroke="{prim}" stroke-width="1.8"/>
    <path d="M 28 98 C 28 76, {av_size-28} 76, {av_size-28} 98 Z" fill="{bg}" stroke="{prim}" stroke-width="1.8"/>
    <circle cx="{av_size//2}" cy="48" r="8" fill="{acc}"/>
    <!-- Minimalist Status Indicator -->
    <rect x="16" y="108" width="{av_size-32}" height="18" rx="9" fill="{bg}" stroke="{success}" stroke-width="1"/>
    <circle cx="28" cy="117" r="3" fill="{success}"/>
    <text x="36" y="120" fill="{success}" font-size="8.5" font-weight="600" class="font-mono">ACTIVE</text>
  </g>
"""
        # PURE VECTOR NAME TYPOGRAPHY (No pixelated pseudo-3D block shadows)
        calc_font_size = 26
        while calc_font_size > 14 and measure_mono_text_width(name_clean, calc_font_size) > max_name_w:
            calc_font_size -= 2
        name_markup = f"""  <text x="180" y="78" fill="{c['title_front']}" font-size="{calc_font_size}" font-weight="700" letter-spacing="0.04em" class="font-mono">{name_clean}</text>"""

        role_markup = f"""
  <g transform="translate(180, 116)">
    <rect x="0" y="0" width="{role_w}" height="26" rx="4" fill="{panel}" stroke="{border}" stroke-width="1"/>
    <rect x="0" y="0" width="3" height="26" rx="1.5" fill="{prim}"/>
    <text x="12" y="17" fill="{acc}" font-size="11.5" font-weight="600" class="font-mono">{role_disp}</text>
  </g>
"""

    # -------------------------------------------------------------
    # 3. CYBERPUNK / RETRO-TECH PARADIGM (Asymmetrical cuts & neon beacons)
    # -------------------------------------------------------------
    else:
        chassis = f"""
  <!-- CYBERPUNK ASYMMETRICAL DECK -->
  <polygon points="20 1, {width-1} 1, {width-1} {height-20}, {width-20} {height-1}, 1 {height-1}, 1 20"
           fill="{bg}" stroke="{border}" stroke-width="1.8"/>
  <rect x="1" y="20" width="3" height="40" fill="{prim}"/>
  <rect x="{width-4}" y="{height-60}" width="3" height="40" fill="{acc}"/>
  <line x1="24" y1="{height-8}" x2="160" y2="{height-8}" stroke="{acc}" stroke-width="2" stroke-dasharray="8 4 2 4"/>
  <!-- Corner Beacons -->
  <rect x="20" y="1" width="12" height="3" fill="{prim}"/>
  <rect x="{width-32}" y="{height-4}" width="12" height="3" fill="{prim}"/>
"""
        avatar_markup = f"""
  <!-- CYBERPUNK HEXAGONAL AVATAR & SCANNER -->
  <g transform="translate({av_x}, {av_y})">
    <polygon points="16 0, {av_size-16} 0, {av_size} 16, {av_size} {av_size-16}, {av_size-16} {av_size}, 16 {av_size}, 0 {av_size-16}, 0 16"
             fill="{panel}" stroke="{prim}" stroke-width="1.8"/>
    <!-- Cyber Scanner Lines -->
    <line x1="10" y1="40" x2="{av_size-10}" y2="40" stroke="{border}" stroke-width="0.8"/>
    <line x1="10" y1="70" x2="{av_size-10}" y2="70" stroke="{border}" stroke-width="0.8"/>
    <!-- Netrunner Silhouette -->
    <circle cx="{av_size//2}" cy="50" r="22" fill="{bg}" stroke="{acc}" stroke-width="2"/>
    <polygon points="28 102, 42 78, {av_size-42} 78, {av_size-28} 102" fill="{bg}" stroke="{acc}" stroke-width="2"/>
    <circle cx="{av_size//2}" cy="50" r="8" fill="{prim}"/>
    <!-- Neon Status LED Pill -->
    <polygon points="10 110, {av_size-10} 110, {av_size-14} 126, 6 126" fill="{bg}" stroke="{success}" stroke-width="1.2"/>
    <text x="{av_size//2}" y="122" fill="{success}" font-size="8.5" font-weight="bold" text-anchor="middle" class="font-mono">NET // ONLINE</text>
  </g>
"""
        lines, calc_px = calculate_smart_layout(name, max_width=max_name_w, default_px_size=5, min_px_size=3, spacing=2, allow_wrap=False)
        single_name = lines[0] if lines else name
        name_markup, _, _ = render_3d_text(
            single_name, x=180, y=58, px_size=calc_px,
            front_color=c["title_front"], mid_shadow=c["title_mid"], dark_shadow=c["title_dark"],
            spacing=2, max_width=max_name_w, allow_wrap=False
        )
        role_markup = f"""
  <g transform="translate(180, 116)">
    <rect x="0" y="0" width="{role_w}" height="26" fill="{panel}" stroke="{prim}" stroke-width="1.2"/>
    <rect x="0" y="0" width="4" height="26" fill="{prim}"/>
    <text x="14" y="17" fill="{acc}" font-size="12" font-weight="bold" class="font-mono">{role_disp}</text>
  </g>
"""

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
    </style>
  </defs>

  {chassis}

  {avatar_markup}

  <!-- TOP BREADCRUMB -->
  <rect x="180" y="24" width="{dossier_w}" height="24" fill="{panel}" stroke="{border}" stroke-width="1"/>
  <text x="192" y="40" fill="{prim}" font-size="11" font-weight="bold" class="font-mono">{dossier_disp}</text>

  <!-- BADGE AND STATUS PILLS (TOP RIGHT) -->
  <g transform="translate({pills_x}, 24)">
    <rect x="0" y="0" width="{badge_w}" height="24" fill="{panel}" stroke="{acc}" stroke-width="1"/>
    <text x="{badge_w // 2}" y="16" fill="{acc}" font-size="10.5" font-weight="bold" text-anchor="middle" class="font-mono">{badge_disp}</text>
    <rect x="{badge_w + pills_gap}" y="0" width="{status_w}" height="24" fill="{panel}" stroke="{success}" stroke-width="1"/>
    <circle cx="{badge_w + pills_gap + 12}" y="12" r="3" fill="{success}"/>
    <text x="{badge_w + pills_gap + 12 + (status_w - 12) // 2}" y="16" fill="{success}" font-size="10" font-weight="bold" text-anchor="middle" class="font-mono">{status_disp}</text>
  </g>

  <!-- NAME TYPOGRAPHY -->
  {name_markup}

  <!-- ROLE PILL -->
  {role_markup}

  <!-- BIO SUMMARY -->
  <text x="182" y="166" fill="{text_main}" font-size="12" font-weight="normal" class="font-mono">{bio_disp}</text>
</svg>"""

    validate_svg(svg)
    return svg


