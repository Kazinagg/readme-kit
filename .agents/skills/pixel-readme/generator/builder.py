"""
Legacy Builder Compatibility Adapter for Pixel Readme Kit
=========================================================
NOTE: This module is retained for backwards compatibility with v2.1 code.
All modern generation should use `generator.engine` and `generator.compiler`
which support multi-mode theming (auto, dark, light, transparent, gh, picture),
responsive callouts, JSON palette presets, and dynamic live GitHub stats.
"""

import warnings
from generator.engine import (
    escape_xml,
    generate_header,
    generate_footer,
    generate_callout,
    generate_frame,
    generate_chip,
    generate_divider,
    generate_splitter,
    validate_svg,
)

def _warn_legacy(old_name, new_name):
    warnings.warn(
        f"{old_name} is deprecated since v3.0. Use generator.engine.{new_name} instead.",
        DeprecationWarning,
        stacklevel=3
    )

def _extract_colors(theme):
    if not isinstance(theme, dict):
        return None, None
    prim = theme.get("primary")
    acc = theme.get("accent") or theme.get("secondary")
    return prim, acc

def _map_style(style_name):
    st = str(style_name).lower() if style_name else "cyberpunk"
    if "tactical" in st or "amber" in st:
        return "tactical"
    elif "minimal" in st or "tokyo" in st or "glass" in st:
        return "minimal"
    return "cyberpunk"

def build_header(title="PIXEL-KIT", subtitle="TRANSLUCENT HUD DESIGN SYSTEM", specs=None, theme=None, width=850, height=None, style="terminal"):
    _warn_legacy("build_header", "generate_header")
    prim, acc = _extract_colors(theme)
    mapped_style = _map_style(style)
    return generate_header(
        style=mapped_style,
        primary=prim,
        accent=acc,
        title=title,
        subtitle=subtitle,
        specs=specs,
        width=width,
        height=height,
        mode="auto"
    )

def build_header_terminal(title, subtitle, specs, theme, width=850, height=260):
    return build_header(title=title, subtitle=subtitle, specs=specs, theme=theme, width=width, height=height, style="cyberpunk")

def build_header_tactical(title, subtitle, specs, theme, width=850, height=220):
    return build_header(title=title, subtitle=subtitle, specs=specs, theme=theme, width=width, height=height, style="tactical")

def build_header_minimal(title, subtitle, specs, theme, width=850, height=135):
    return build_header(title=title, subtitle=subtitle, specs=specs, theme=theme, width=width, height=height, style="minimal")

def build_footer(style="terminal", status=None, theme=None, width=850, height=76):
    _warn_legacy("build_footer", "generate_footer")
    prim, acc = _extract_colors(theme)
    mapped_style = _map_style(style)
    return generate_footer(
        style=mapped_style,
        primary=prim,
        accent=acc,
        status=status or "SESSION_ACTIVE // STANDBY",
        width=width,
        height=height,
        mode="auto"
    )

def build_footer_terminal(status="SYSTEM_STANDBY // 0xDEADBEEF", theme=None, width=850, height=76):
    return build_footer(style="cyberpunk", status=status, theme=theme, width=width, height=height)

def build_footer_tactical(status="CLASSIFIED // SECTOR_CLEAR", theme=None, width=850, height=76):
    return build_footer(style="tactical", status=status, theme=theme, width=width, height=height)

def build_footer_minimal(status="TOKYO_VAPORWAVE // HUD v3.0", theme=None, width=850, height=76):
    return build_footer(style="minimal", status=status, theme=theme, width=width, height=height)

def build_footer_matrix(status="CONNECTION TERMINATED // BUFFER_FLUSHED", theme=None, width=850, height=76):
    return build_footer(style="cyberpunk", status=status, theme=theme, width=width, height=height)

def build_callout(callout_type="note", title="SYSTEM SPECIFICATION", message="", theme=None, width=850, height=None):
    _warn_legacy("build_callout", "generate_callout")
    prim, acc = _extract_colors(theme)
    return generate_callout(
        style="cyberpunk",
        primary=prim,
        accent=acc,
        callout_type=callout_type,
        title=title,
        subtitle=message,
        width=width,
        height=height,
        mode="auto"
    )

def build_frame_top(title="╔═ SYSTEM.CORE // RUNTIME.SYS", tag="[OPEN_HUD]", color=None, theme=None, width=850, height=None, style="brackets"):
    _warn_legacy("build_frame_top", "generate_frame")
    prim, acc = _extract_colors(theme)
    if color and not prim:
        prim = color
    mapped_style = _map_style(style)
    return generate_frame(
        style=mapped_style,
        primary=prim,
        accent=acc,
        frame_type="top",
        title=title,
        tag=tag,
        width=width,
        height=height,
        mode="auto"
    )

def build_frame_bottom(tag="╚═ [SYSTEM.CLOSED] ═╝", color=None, theme=None, width=850, height=None, style="brackets"):
    _warn_legacy("build_frame_bottom", "generate_frame")
    prim, acc = _extract_colors(theme)
    if color and not prim:
        prim = color
    mapped_style = _map_style(style)
    return generate_frame(
        style=mapped_style,
        primary=prim,
        accent=acc,
        frame_type="bottom",
        tag=tag,
        width=width,
        height=height,
        mode="auto"
    )

def build_chip(text="CHIP", color=None, theme=None, style="closed", width=None, height=26):
    _warn_legacy("build_chip", "generate_chip")
    prim, acc = _extract_colors(theme)
    if color and not prim:
        prim = color
    return generate_chip(
        style="cyberpunk",
        primary=prim,
        accent=acc,
        chip_type=style,
        text=text,
        width=width,
        height=height,
        mode="auto"
    )

def build_pcb_divider(theme=None, width=850, height=28):
    _warn_legacy("build_pcb_divider", "generate_divider")
    prim, acc = _extract_colors(theme)
    return generate_divider(style="cyberpunk", primary=prim, accent=acc, width=width, height=height, mode="auto")

def build_laser_divider(theme=None, width=850, height=28, color=None):
    _warn_legacy("build_laser_divider", "generate_divider")
    prim, acc = _extract_colors(theme)
    if color and not prim:
        prim = color
    return generate_divider(style="tactical", primary=prim, accent=acc, width=width, height=height, mode="auto")

def build_splitter_terminal(title="[MODULE: TERMINAL]", theme=None, width=850, height=22):
    _warn_legacy("build_splitter_terminal", "generate_splitter")
    prim, acc = _extract_colors(theme)
    return generate_splitter(style="cyberpunk", primary=prim, accent=acc, label=title, width=width, height=height, mode="auto")

def build_splitter_tactical(title="[MODULE: TACTICAL]", theme=None, width=850, height=22):
    _warn_legacy("build_splitter_tactical", "generate_splitter")
    prim, acc = _extract_colors(theme)
    return generate_splitter(style="tactical", primary=prim, accent=acc, label=title, width=width, height=height, mode="auto")

def build_splitter_decay(title="[MODULE: MINIMAL]", theme=None, width=850, height=22):
    _warn_legacy("build_splitter_decay", "generate_splitter")
    prim, acc = _extract_colors(theme)
    return generate_splitter(style="minimal", primary=prim, accent=acc, label=title, width=width, height=height, mode="auto")
