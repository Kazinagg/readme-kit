"""Frame window cap components for Pixel Readme Kit."""
from typing import Optional, Any
from generator.themes import resolve_theme, normalize_style_and_theme
from generator.layout import (
    format_tag,
    format_bottom_tag,
    clamp_text_to_width,
    measure_mono_text_width,
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
)


def _generate_modern_frame(style_name, theme_name, c, css_vars,
                           frame_type="top", title="SYSTEM.CORE // RUNTIME.SYS",
                           tag="[OPEN]", width=850, height=None,
                           tag_url=None, close_url=None):
    """Renders clean vector frame caps with rounded corners and traffic lights."""
    prim = c["primary"]
    acc = c["accent"]
    tertiary_col = c["tertiary"]
    bg = c["bg"]
    border = c["border"]
    panel = c["panel"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]

    title_clean = escape_xml(title).lstrip("╔═ ").strip()
    ft = str(frame_type).lower().replace("-", "_")
    is_top = ft in ("top", "term_top", "terminal_top", "window_top")
    is_term = "term" in ft

    if is_top:
        h = height if height else 36
        tag_link_open = f'<a href="{escape_xml(tag_url)}" target="_blank" rel="noopener noreferrer" class="btn-hover">' if tag_url else ''
        tag_link_close = '</a>' if tag_url else ''

        clean_tag_raw = str(tag).strip().strip("[]")
        tag_clean = escape_xml(clean_tag_raw if (clean_tag_raw and clean_tag_raw != "OPEN_HUD") else ("TTY:01" if is_term else "OPEN"))
        tag_w = min(160, max(80, int(measure_sans_text_width(tag_clean, 10) + 28)))
        tag_x = width - tag_w - 20

        avail_title_w = max(100, tag_x - 80)
        title_disp = clamp_sans_text_to_width(title_clean, avail_title_w, 12)

        if is_term:
            title_markup = f'<text x="68" y="{h//2 + 4}" fill="{prim}" font-size="12" font-weight="700" class="font-mono">❯ <tspan fill="{text_main}">{title_disp}</tspan> <tspan fill="{acc}">_</tspan></text>'
        else:
            title_markup = f'<text x="68" y="{h//2 + 4}" fill="{text_main}" font-size="12" font-weight="600" class="font-sans">{title_disp}</text>'

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%">
  <defs>
    <style>
      {css_vars}
{MODERN_BASE_STYLES}
    </style>
  </defs>

  <!-- Modern Top Cap: Rounded Top (rx=10) & Flat Bottom (Flush to table) -->
  <path d="M 1 {h} L 1 10 Q 1 1 10 1 L {width-10} 1 Q {width-1} 1 {width-1} 10 L {width-1} {h} Z"
        fill="{bg}" stroke="{border}" stroke-width="1.2"/>
  <line x1="1" y1="{h}" x2="{width-1}" y2="{h}" stroke="{border}" stroke-width="1"/>

  <!-- macOS / SaaS Window Traffic Lights -->
  <circle cx="20" cy="{h//2}" r="4" fill="#EF4444" opacity="0.85"/>
  <circle cx="34" cy="{h//2}" r="4" fill="#F59E0B" opacity="0.85"/>
  <circle cx="48" cy="{h//2}" r="4" fill="#10B981" opacity="0.85"/>

  <!-- Clean Title -->
  {title_markup}

  <!-- Modern Pill Tag Button -->
  {tag_link_open}<g transform="translate({tag_x}, {(h-22)//2})">
    <rect x="0" y="0" width="{tag_w}" height="22" rx="11" fill="{panel}" stroke="{border}" stroke-width="1"/>
    <text x="{tag_w//2}" y="15" fill="{prim}" font-size="10" font-weight="600" text-anchor="middle" class="font-sans">{tag_clean}</text>
  </g>{tag_link_close}
</svg>"""

    else:
        h = height if height else 26
        tag_link_open = f'<a href="{escape_xml(close_url or tag_url)}" class="btn-hover">' if (close_url or tag_url) else ''
        tag_link_close = '</a>' if (close_url or tag_url) else ''

        clean_tag_raw = str(tag).strip()
        default_bot_label = "EXIT: 0 // TERMINAL DETACHED" if is_term else "▲ RETURN TO TOP"
        bot_tag_clean = escape_xml(clean_tag_raw if clean_tag_raw and clean_tag_raw not in ("[OPEN_HUD]", "[ONLINE]", "[SYS_LOG]") else default_bot_label)
        bot_w = max(160, min(width - 60, int(measure_sans_text_width(bot_tag_clean, 10) + 32)))
        bx = (width - bot_w) // 2

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%">
  <defs>
    <style>
      {css_vars}
{MODERN_BASE_STYLES}
    </style>
  </defs>

  <!-- Modern Bottom Cap: Flat Top & Rounded Bottom (rx=10) -->
  <path d="M 1 0 L {width-1} 0 L {width-1} {h-10} Q {width-1} {h-1} {width-10} {h-1} L 10 {h-1} Q 1 {h-1} 1 {h-10} Z"
        fill="{bg}" stroke="{border}" stroke-width="1.2"/>
  <line x1="1" y1="0" x2="{width-1}" y2="0" stroke="{border}" stroke-width="1"/>

  <!-- Center Nav / Readout Pill -->
  {tag_link_open}<g transform="translate({bx}, {(h-18)//2})">
    <rect x="0" y="0" width="{bot_w}" height="18" rx="9" fill="{panel}" stroke="{border}" stroke-width="1"/>
    <text x="{bot_w//2}" y="13" fill="{prim}" font-size="10" font-weight="500" text-anchor="middle" class="font-sans">{bot_tag_clean}</text>
  </g>{tag_link_close}
</svg>"""

    validate_svg(svg)
    return svg


def _generate_sketch_frame(style_name, theme_name, c, css_vars,
                           frame_type="top", title="SYSTEM.CORE // RUNTIME.SYS",
                           tag="[OPEN]", width=850, height=None,
                           tag_url=None, close_url=None):
    """Renders hand-drawn sketch frame caps for markdown table monolith headers and footers."""
    prim = c["primary"]
    acc = c["accent"]
    tertiary_col = c["tertiary"]
    bg = c["bg"]
    border = c["border"]
    panel = c["panel"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]

    title_clean = escape_xml(title).lstrip("╔═ ").strip()
    ft = str(frame_type).lower().replace("-", "_")
    is_top = ft in ("top", "term_top", "terminal_top", "window_top")
    is_term = "term" in ft

    if is_top:
        h = height if height else 38
        tag_link_open = f'<a href="{escape_xml(tag_url)}" target="_blank" rel="noopener noreferrer" class="sketch-hover">' if tag_url else ''
        tag_link_close = '</a>' if tag_url else ''

        clean_tag_raw = str(tag).strip().strip("[]")
        tag_clean = escape_xml(clean_tag_raw if (clean_tag_raw and clean_tag_raw != "OPEN_HUD") else ("sh:exec" if is_term else "OPEN"))
        tag_w = min(160, max(80, int(measure_sans_text_width(tag_clean, 10) + 28)))
        tag_x = width - tag_w - 20

        avail_title_w = max(100, tag_x - 80)
        title_disp = clamp_sans_text_to_width(title_clean, avail_title_w, 12)

        # Top frame rests flat on the table bottom (y = h)
        body = render_rough_rect(x=2, y=2, w=width-4, h=h-2, stroke=border, stroke_width=1.4, fill=bg, rx=6, seed=101)
        bottom_flat_line = render_rough_line(1, h, width-1, h, stroke=border, stroke_width=1.5, seed=102)
        tag_box = render_rough_rect(x=tag_x, y=(h-22)//2, w=tag_w, h=22, stroke=acc, stroke_width=1.1, fill=panel, rx=6, seed=105)

        prefix = "$ " if is_term else ""

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%">
  <defs>
    <style>
      {css_vars}
{SKETCH_BASE_STYLES}
    </style>
{render_sketch_defs(c, "frameSketchTop")}
  </defs>

  <!-- Sketch Top Cap -->
  {body}
  {bottom_flat_line}

  <!-- Hand-drawn Doodle Dots -->
  <circle cx="20" cy="{h//2}" r="3.5" fill="{prim}" opacity="0.85"/>
  <circle cx="32" cy="{h//2}" r="3.5" fill="{acc}" opacity="0.85"/>
  <circle cx="44" cy="{h//2}" r="3.5" fill="{tertiary_col}" opacity="0.85"/>

  <!-- Title -->
  <text x="64" y="{h//2 + 4}" fill="{text_main}" font-size="12" font-weight="600" class="font-sketch">{prefix}{title_disp}</text>

  <!-- Tag Pill -->
  {tag_link_open}<g>
    {tag_box}
    <text x="{tag_x + tag_w//2}" y="{h//2 + 4}" fill="{prim}" font-size="10" font-weight="600" text-anchor="middle" class="font-sketch">{tag_clean}</text>
  </g>{tag_link_close}
</svg>"""

    else:
        h = height if height else 28
        tag_link_open = f'<a href="{escape_xml(close_url or tag_url)}" class="sketch-hover">' if (close_url or tag_url) else ''
        tag_link_close = '</a>' if (close_url or tag_url) else ''

        clean_tag_raw = str(tag).strip()
        default_bot_label = "// process completed (exit 0)" if is_term else "▲ RETURN TO TOP"
        bot_tag_clean = escape_xml(clean_tag_raw if clean_tag_raw and clean_tag_raw not in ("[OPEN_HUD]", "[ONLINE]", "[SYS_LOG]") else default_bot_label)
        bot_w = max(160, min(width - 60, int(measure_sans_text_width(bot_tag_clean, 10) + 32)))
        bx = (width - bot_w) // 2

        # Bottom frame rests flat on table top (y = 0)
        body = render_rough_rect(x=2, y=2, w=width-4, h=h-3, stroke=border, stroke_width=1.3, fill=bg, rx=6, seed=112)
        top_flat_line = render_rough_line(1, 1, width-1, 1, stroke=border, stroke_width=1.5, seed=110)
        bot_box = render_rough_rect(x=bx, y=(h-20)//2, w=bot_w, h=20, stroke=acc, stroke_width=1.1, fill=panel, rx=6, seed=115)

        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%">
  <defs>
    <style>
      {css_vars}
{SKETCH_BASE_STYLES}
    </style>
{render_sketch_defs(c, "frameSketchBot")}
  </defs>

  <!-- Sketch Bottom Cap -->
  {body}
  {top_flat_line}

  <!-- Center Status / Return Label -->
  {tag_link_open}<g>
    {bot_box}
    <text x="{bx + bot_w//2}" y="{h//2 + 3}" fill="{prim}" font-size="10" font-weight="600" text-anchor="middle" class="font-sketch">{bot_tag_clean}</text>
  </g>{tag_link_close}
</svg>"""

    validate_svg(svg)
    return svg


def generate_frame(style=None, primary=None, accent=None,
                   frame_type="top", title="╔═ SYSTEM.CORE // RUNTIME.SYS",
                   tag="[OPEN_HUD]", width=850, height=None, mode="auto", preset=None,
                   tag_url=None, close_url=None, tertiary=None, theme=None):
    style_name, theme_name = normalize_style_and_theme(style=style, theme=theme)
    c, css_vars = resolve_theme(style=style_name, theme=theme_name, mode=mode, primary=primary, accent=accent, preset=preset, tertiary=tertiary)
    if style_name == "modern":
        return _generate_modern_frame(
            style_name=style_name, theme_name=theme_name, c=c, css_vars=css_vars,
            frame_type=frame_type, title=title, tag=tag, width=width, height=height,
            tag_url=tag_url, close_url=close_url
        )
    elif style_name == "sketch":
        return _generate_sketch_frame(
            style_name=style_name, theme_name=theme_name, c=c, css_vars=css_vars,
            frame_type=frame_type, title=title, tag=tag, width=width, height=height,
            tag_url=tag_url, close_url=close_url
        )
    prim = c["primary"]
    acc = c["accent"]
    tertiary_col = c["tertiary"]
    bg = c["bg"]
    border = c["border"]
    panel = c["panel"]
    text_main = c["text_main"]
    text_dim = c["text_dim"]


    title_clean = escape_xml(title)
    tag_clean = format_tag(tag)
    bot_tag_clean = format_bottom_tag(tag)
    if theme_name in ("tactical", "amber", "amber_crt"):
        st = "tactical"
    elif theme_name in ("minimal", "clean-mono", "clean_mono", "academic-paper", "academic_paper", "corporate-blue", "corporate_blue", "tokyo", "tokyo_night", "swiss-mono", "swiss_mono", "executive-slate", "executive_slate"):
        st = "minimal"
    else:
        st = "cyberpunk"

    ft = str(frame_type).lower().replace("-", "_")
    is_top = ft in ("top", "term_top", "terminal_top", "window_top")
    is_term = "term" in ft

    title_disp = clamp_text_to_width(title_clean, width - 230, 12)
    tag_disp = clamp_text_to_width(tag_clean if tag_clean and tag_clean != "[OPEN_HUD]" else ("[TTY:01]" if is_term else "[OPEN]"), 95, 9)

    if is_term and bot_tag_clean in ("▲ RETURN TO TOP", "[OPEN_HUD]", "[ONLINE]", "[SYS_LOG]"):
        if st == "tactical":
            bot_tag_clean = "[ CMD_SESSION // EXIT_CODE: 0 // BUFFER: 100% ]"
        elif st == "minimal":
            bot_tag_clean = "[EXIT 0 // SESSION TERMINATED]"
        else:
            bot_tag_clean = "[ TTY // 0x00 OK // BUFFER RELEASED ]"

    bot_w = max(220, min(width - 60, int(measure_mono_text_width(bot_tag_clean, 9) + 28)))
    bx = (width - bot_w) // 2

    if is_top:
        h = height if height else 38
        tag_link_open = f'<a href="{escape_xml(tag_url)}" target="_blank" class="btn-hover">' if tag_url else ''
        tag_link_close = '</a>' if tag_url else ''
        close_link_open = f'<a href="{escape_xml(close_url)}" target="_blank" class="btn-hover">' if close_url else ''
        close_link_close = '</a>' if close_url else ''

        if st == "tactical":
            # Tactical Chamfer Top: Dual Hull, Tech Seam, Flush Downward Prongs x=1..849, LED, Buttons
            prefix_label = "[CLI] // " if is_term else "[//] "
            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
      @keyframes blinkLed {{ 0%, 100% {{ fill: {prim}; opacity: 1; }} 50% {{ fill: {border}; opacity: 0.3; }} }}
      .led {{ animation: blinkLed 1.8s infinite steps(1); }}
    </style>
  </defs>

  <!-- DUAL TACTICAL CHASSIS -->
  <polygon points="12 4, {width-12} 4, {width-1} 15, {width-1} 32, 1 32, 1 15"
           fill="{bg}" stroke="{border}" stroke-width="2"/>
  <polygon points="14 7, {width-14} 7, {width-4} 16, {width-4} 29, 4 29, 4 16"
           fill="none" stroke="{prim}" stroke-width="1.5" opacity="0.85"/>
  <line x1="20" y1="32" x2="{width-20}" y2="32" stroke="{acc}" stroke-width="1" stroke-dasharray="6,4" opacity="0.6"/>

  <!-- DOWNWARD PRONGS (FLUSH TO EDGES x=1..{width-1}) -->
  <line x1="1" y1="26" x2="1" y2="{h}" stroke="{prim}" stroke-width="2.5"/>
  <rect x="0" y="32" width="4" height="6" fill="{prim}"/>
  <line x1="{width-1}" y1="26" x2="{width-1}" y2="{h}" stroke="{prim}" stroke-width="2.5"/>
  <rect x="{width-4}" y="32" width="4" height="6" fill="{prim}"/>

  <!-- Status LED -->
  <circle cx="24" cy="18" r="4" fill="{prim}" class="led"/>

  <!-- Title Text -->
  <text x="36" y="22" fill="{prim}" font-size="12" font-weight="bold" letter-spacing="1" class="font-mono">
    <tspan fill="{acc}">{prefix_label}</tspan>{title_disp}
  </text>

  <!-- Right Status Tag -->
  {tag_link_open}<rect x="{width-180}" y="9" width="105" height="18" fill="{panel}" stroke="{prim}" stroke-width="1"/>
  <text x="{width-127}" y="22" fill="{prim}" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">{tag_disp}</text>{tag_link_close}

  <!-- Window controls [ _ ] [ □ ] [ × ] -->
  <rect x="{width-68}" y="11" width="14" height="14" fill="{panel}"/>
  <text x="{width-64}" y="21" fill="{text_dim}" font-size="10" font-weight="bold" class="font-mono">_</text>
  <rect x="{width-50}" y="11" width="14" height="14" fill="{panel}"/>
  <text x="{width-47}" y="22" fill="{text_dim}" font-size="10" font-weight="bold" class="font-mono">□</text>
  {close_link_open}<rect x="{width-32}" y="11" width="14" height="14" fill="{tertiary_col}"/>
  <text x="{width-28}" y="22" fill="{text_main}" font-size="10" font-weight="bold" class="font-mono">×</text>{close_link_close}
</svg>"""

        elif st == "minimal":
            # Minimal Glass Table Monolith Top (Hugging Ticks ┌ ┐)
            prefix_label = "> " if is_term else ""
            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
    </style>
  </defs>
  <rect x="0" y="0" width="{width}" height="{h}" fill="{bg}"/>
  <path d="M 4 14 L 4 4 L 14 4" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <path d="M {width-4} 14 L {width-4} 4 L {width-14} 4" fill="none" stroke="{acc}" stroke-width="1.5"/>
  <line x1="8" y1="{h-2}" x2="{width-8}" y2="{h-2}" stroke="{prim}" stroke-width="1" stroke-dasharray="4,4" opacity="0.35"/>
  <circle cx="24" cy="18" r="4" fill="{prim}"/>
  <text x="36" y="22" fill="{prim}" font-size="12" font-weight="bold" letter-spacing="1" class="font-mono">{prefix_label}{title_disp}</text>
  {tag_link_open}<rect x="{width-180}" y="9" width="105" height="18" fill="{panel}" stroke="{prim}" stroke-width="1"/>
  <text x="{width-128}" y="22" fill="{prim}" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">{tag_disp}</text>{tag_link_close}
  <rect x="{width-68}" y="11" width="14" height="14" fill="{panel}"/><text x="{width-64}" y="21" fill="{text_dim}" font-size="10" class="font-mono">_</text>
  <rect x="{width-50}" y="11" width="14" height="14" fill="{panel}"/><text x="{width-47}" y="22" fill="{text_dim}" font-size="10" class="font-mono">□</text>
  {close_link_open}<rect x="{width-32}" y="11" width="14" height="14" fill="{tertiary_col}"/><text x="{width-28}" y="22" fill="{text_main}" font-size="10" font-weight="bold" class="font-mono">×</text>{close_link_close}
</svg>"""

        else:
            # Cyberpunk Brackets Top (Downward prongs on x=1 and x=849)
            if is_term:
                title_svg = f'<tspan fill="{acc}">$</tspan> {title_disp} <tspan fill="{acc}">█</tspan>'
            else:
                title_svg = f'<tspan fill="{acc}">[//]</tspan> {title_disp}'

            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
      @keyframes blinkLed {{ 0%, 100% {{ fill: {prim}; opacity: 1; }} 50% {{ fill: {border}; opacity: 0.3; }} }}
      .led {{ animation: blinkLed 1.8s infinite steps(1); }}
    </style>
  </defs>
  <rect x="1" y="4" width="{width-2}" height="28" fill="{bg}" stroke="{border}" stroke-width="2"/>
  <rect x="3" y="6" width="{width-6}" height="24" fill="none" stroke="{prim}" stroke-width="1.5" opacity="0.85"/>
  <rect x="1" y="4" width="5" height="5" fill="{prim}"/>
  <rect x="{width-6}" y="4" width="5" height="5" fill="{acc}"/>
  <!-- Downward Embracing Prongs (Flush x=1 and x={width-1}) -->
  <line x1="1" y1="24" x2="1" y2="{h}" stroke="{prim}" stroke-width="2.5"/>
  <rect x="0" y="32" width="4" height="6" fill="{prim}"/>
  <line x1="{width-1}" y1="24" x2="{width-1}" y2="{h}" stroke="{prim}" stroke-width="2.5"/>
  <rect x="{width-4}" y="32" width="4" height="6" fill="{prim}"/>
  <circle cx="24" cy="18" r="4" fill="{prim}" class="led"/>
  <text x="36" y="22" fill="{prim}" font-size="12" font-weight="bold" letter-spacing="1" class="font-mono">{title_svg}</text>
  {tag_link_open}<rect x="{width-180}" y="9" width="105" height="18" fill="{panel}" stroke="{prim}" stroke-width="1"/>
  <text x="{width-128}" y="22" fill="{prim}" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">{tag_disp}</text>{tag_link_close}
  <rect x="{width-68}" y="11" width="14" height="14" fill="{panel}"/><text x="{width-64}" y="21" fill="{text_dim}" font-size="10" class="font-mono">_</text>
  <rect x="{width-50}" y="11" width="14" height="14" fill="{panel}"/><text x="{width-47}" y="22" fill="{text_dim}" font-size="10" class="font-mono">□</text>
  {close_link_open}<rect x="{width-32}" y="11" width="14" height="14" fill="{tertiary_col}"/><text x="{width-28}" y="22" fill="{text_main}" font-size="10" font-weight="bold" class="font-mono">×</text>{close_link_close}
</svg>"""

    else:
        # Bottom Frames
        h = height if height else 24
        if st == "tactical":
            # Tactical Chamfer Bottom: Upward Prongs Flush x=1..849, Chamfer Body, Center Buffer
            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
    </style>
  </defs>
  <!-- UPWARD PRONGS (FLUSH TO EDGES x=1..{width-1}) -->
  <line x1="1" y1="0" x2="1" y2="10" stroke="{prim}" stroke-width="2.5"/>
  <rect x="0" y="0" width="4" height="5" fill="{prim}"/>
  <line x1="{width-1}" y1="0" x2="{width-1}" y2="10" stroke="{prim}" stroke-width="2.5"/>
  <rect x="{width-4}" y="0" width="4" height="5" fill="{prim}"/>

  <polygon points="1 10, {width-1} 10, {width-12} 20, 12 20" fill="{bg}" stroke="{border}" stroke-width="1.5"/>
  <line x1="12" y1="20" x2="{width-12}" y2="20" stroke="{acc}" stroke-width="2"/>

  <!-- Center Status Buffer Readout -->
  <rect x="{bx}" y="4" width="{bot_w}" height="16" fill="{bg}" stroke="{acc}" stroke-width="1"/>
  <text x="{width//2}" y="15" fill="{prim}" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">
    {bot_tag_clean}
  </text>
</svg>"""

        elif st == "minimal":
            # Minimal Glass Table Monolith Bottom (Hugging Ticks └ ┘)
            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
    </style>
  </defs>
  <rect x="0" y="0" width="{width}" height="{h}" fill="{bg}"/>
  <path d="M 4 8 L 4 18 L 14 18" fill="none" stroke="{prim}" stroke-width="1.5"/>
  <path d="M {width-4} 8 L {width-4} 18 L {width-14} 18" fill="none" stroke="{acc}" stroke-width="1.5"/>
  <line x1="8" y1="2" x2="{width-8}" y2="2" stroke="{prim}" stroke-width="1" stroke-dasharray="4,4" opacity="0.35"/>
  <text x="{width//2}" y="15" fill="{prim}" font-size="9" font-weight="bold" letter-spacing="1.5" text-anchor="middle" class="font-mono">{bot_tag_clean}</text>
</svg>"""

        else:
            # Cyberpunk Brackets Bottom (Upward prongs on x=1 and x=849)
            svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" width="100%" height="100%" shape-rendering="crispEdges">
  <defs>
    <style>
      {css_vars}
      .font-mono {{ font-family: 'JetBrains Mono', 'Fira Code', 'Courier New', monospace; }}
    </style>
  </defs>
  <!-- UPWARD PRONGS (FLUSH TO EDGES x=1..{width-1}) -->
  <line x1="1" y1="0" x2="1" y2="12" stroke="{prim}" stroke-width="2.5"/><rect x="0" y="0" width="4" height="5" fill="{prim}"/>
  <line x1="{width-1}" y1="0" x2="{width-1}" y2="12" stroke="{prim}" stroke-width="2.5"/><rect x="{width-4}" y="0" width="4" height="5" fill="{prim}"/>
  <line x1="1" y1="12" x2="{width-1}" y2="12" stroke="{border}" stroke-width="3"/>
  <line x1="6" y1="12" x2="{width-6}" y2="12" stroke="{prim}" stroke-width="1.5" opacity="0.85"/>
  <path d="M 1 12 L 1 20 L 16 20" fill="none" stroke="{prim}" stroke-width="1.5"/><rect x="1" y="17" width="4" height="4" fill="{acc}"/>
  <path d="M {width-1} 12 L {width-1} 20 L {width-16} 20" fill="none" stroke="{prim}" stroke-width="1.5"/><rect x="{width-5}" y="17" width="4" height="4" fill="{acc}"/>
  <rect x="{bx}" y="4" width="{bot_w}" height="16" fill="{bg}" stroke="{acc}" stroke-width="1"/>
  <text x="{width//2}" y="15" fill="{prim}" font-size="9" font-weight="bold" text-anchor="middle" class="font-mono">{bot_tag_clean}</text>
</svg>"""

    validate_svg(svg)
    return svg


