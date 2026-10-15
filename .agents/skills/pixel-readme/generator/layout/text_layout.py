"""
Text layout, measurement, and formatting utilities for Pixel Readme Kit.
"""

from typing import List, Tuple, Optional, Any


def measure_mono_text_width(text: Any, font_size: float = 11.0) -> float:
    """
    Estimates the pixel width of text rendered with monospace font (JetBrains Mono, Fira Code, etc.).
    Standard monospace character pitch is approx 0.60 to 0.62 * font_size.
    Wide/Unicode symbols (such as arrows, stars, blocks) are approx 1.1 to 1.35 * font_size.
    """
    if not text:
        return 0.0
    w = 0.0
    char_pitch = font_size * 0.61
    for ch in str(text):
        code = ord(ch)
        if code > 0x2000 or ch in "★⚡●▲▼■◆▶◀ℹ✓✗🏛️🧬":
            w += font_size * 1.25
        else:
            w += char_pitch
    return w


def clamp_text_to_width(
    text: Any,
    max_width: float,
    font_size: float = 11.0,
    suffix: str = "...",
) -> str:
    """
    Clamps/truncates text with a suffix if its rendered width exceeds max_width.
    """
    if not text:
        return ""
    text_str = str(text)
    if measure_mono_text_width(text_str, font_size) <= max_width:
        return text_str

    suffix_w = measure_mono_text_width(suffix, font_size)
    target_w = max(0.0, max_width - suffix_w)

    clamped = text_str
    while clamped and measure_mono_text_width(clamped, font_size) > target_w:
        clamped = clamped[:-1]

    return (clamped.rstrip() + suffix) if clamped else text_str[:1]


def wrap_text_to_lines(
    text: Any,
    max_width: float,
    font_size: float = 11.0,
    max_lines: int = 2,
    suffix: str = "...",
) -> List[str]:
    """
    Splits text across lines based on word boundaries, respecting max_width and max_lines.
    The final line is truncated with suffix if there is remaining overflow.
    """
    if not text:
        return []
    words = str(text).strip().split()
    if not words:
        return []

    lines: List[str] = []
    curr_line: List[str] = []

    for i, w in enumerate(words):
        test_line = " ".join(curr_line + [w])
        if measure_mono_text_width(test_line, font_size) <= max_width or not curr_line:
            curr_line.append(w)
        else:
            lines.append(" ".join(curr_line))
            curr_line = [w]
            if len(lines) == max_lines - 1:
                # Last allowed line, accumulate rest
                remaining_words = words[i:]
                last_line = " ".join(remaining_words)
                lines.append(clamp_text_to_width(last_line, max_width, font_size, suffix=suffix))
                curr_line = []
                break

    if curr_line and len(lines) < max_lines:
        line_str = " ".join(curr_line)
        if measure_mono_text_width(line_str, font_size) > max_width:
            line_str = clamp_text_to_width(line_str, max_width, font_size, suffix=suffix)
        lines.append(line_str)
    elif curr_line and lines:
        lines[-1] = clamp_text_to_width(lines[-1] + " " + " ".join(curr_line), max_width, font_size, suffix=suffix)

    return lines


def normalize_specs(
    specs: Any = None,
    spec1: Optional[str] = None,
    spec2: Optional[str] = None,
    spec3: Optional[str] = None,
    default_color: Optional[str] = None,
) -> List[Tuple[str, str, str]]:
    """
    Normalizes specifications (level-3 header telemetry tags).
    Accepts:
    - spec1, spec2, spec3 strings
    - specs: list of tuples/strings, or pipe/semicolon/newline-delimited string
    Returns list of tuples: [(label, value, color), ...] with at most 3 items.
    If nothing is specified, returns an empty list [].
    """
    items = []
    def _parse_spec_item(item, idx):
        if isinstance(item, (list, tuple)):
            lbl = str(item[0]) if len(item) > 0 else f"SPEC.{idx+1}"
            val = str(item[1]) if len(item) > 1 else "NOMINAL"
            col = str(item[2]) if len(item) > 2 and item[2] else (default_color or "var(--accent)")
            return lbl, val, col
        elif isinstance(item, str):
            s = item.strip()
            if not s:
                return None
            parts = s.split(":")
            if len(parts) >= 2:
                lbl = parts[0].strip()
                val = parts[1].strip()
                col = parts[2].strip() if len(parts) > 2 and parts[2].strip() else (default_color or "var(--accent)")
            else:
                lbl = f"SPEC.{idx+1}"
                val = s
                col = default_color or "var(--accent)"
            return lbl, val, col
        return None

    if specs:
        if isinstance(specs, (list, tuple)):
            for i, it in enumerate(specs):
                parsed = _parse_spec_item(it, i)
                if parsed:
                    items.append(parsed)
        elif isinstance(specs, str):
            delim = "\n" if "\n" in specs else ("|" if "|" in specs else ";")
            for i, it in enumerate(specs.split(delim)):
                parsed = _parse_spec_item(it, i)
                if parsed:
                    items.append(parsed)

    if not items:
        for i, sp in enumerate([spec1, spec2, spec3]):
            if sp:
                parsed = _parse_spec_item(sp, i)
                if parsed:
                    items.append(parsed)

    return items[:3]


def format_tag(
    tag: Optional[str],
    tag_url: Optional[str] = None,
    default_label: str = "[SYSTEM.ACTIVE]",
) -> str:
    """Formats header/frame upper tag, wrapping into <a> if tag_url provided."""
    raw = tag if tag is not None and str(tag).strip() != "" else default_label
    lbl = str(raw).strip()
    if not lbl.startswith("["):
        lbl = f"[{lbl}]"
    if tag_url:
        import html
        esc_url = html.escape(tag_url, quote=True)
        return f'<a href="{esc_url}" target="_blank" rel="noopener noreferrer" class="btn-hover">{lbl}</a>'
    return lbl


def format_bottom_tag(
    tag: Optional[str],
    tag_url: Optional[str] = None,
    close_url: Optional[str] = None,
    default_label: str = "▲ RETURN TO TOP",
) -> str:
    """Formats frame bottom navigation tag, wrapping into <a> if link provided."""
    raw = tag if tag is not None and str(tag).strip() != "" else default_label
    lbl = str(raw).strip()
    target = close_url or tag_url
    if target:
        import html
        esc_url = html.escape(target, quote=True)
        return f'<a href="{esc_url}" class="btn-hover">{lbl}</a>'
    return lbl


def estimate_chip_width(
    text: Any,
    font_size: float = 10.0,
    min_width: int = 120,
    max_width: int = 450,
) -> int:
    """Calculates adaptive chip width based on character count and margins."""
    tw = measure_mono_text_width(str(text), font_size)
    total = int(tw + 48)  # 24px padding on both sides
    return max(min_width, min(max_width, total))


def measure_sans_text_width(text: Any, font_size: float = 13.0) -> float:
    """
    Estimates the pixel width of text rendered with proportional Sans-Serif font
    (system-ui, -apple-system, Inter, Segoe UI, Roboto, Helvetica, sans-serif).
    Accounts for narrow characters (i, l, t, .), wide characters (M, W, m, w),
    and Unicode symbols.
    """
    if not text:
        return 0.0
    w = 0.0
    for ch in str(text):
        code = ord(ch)
        if code > 0x2000 or ch in "★⚡●▲▼■◆▶◀ℹ✓✗🏛️🧬":
            w += font_size * 1.25
        elif ch in "ijl|!.,:; '`()[]{}":
            w += font_size * 0.30
        elif ch in "frt-":
            w += font_size * 0.38
        elif ch in "mwMW@%&Q":
            w += font_size * 0.88
        elif ch.isupper() or ch in "0123456789":
            w += font_size * 0.62
        else:
            w += font_size * 0.52
    return w


def clamp_sans_text_to_width(
    text: Any,
    max_width: float,
    font_size: float = 13.0,
    suffix: str = "...",
) -> str:
    """
    Clamps proportional Sans-Serif text with a suffix if width exceeds max_width.
    """
    if not text:
        return ""
    text_str = str(text)
    if measure_sans_text_width(text_str, font_size) <= max_width:
        return text_str

    suffix_w = measure_sans_text_width(suffix, font_size)
    target_w = max(0.0, max_width - suffix_w)

    clamped = text_str
    while clamped and measure_sans_text_width(clamped, font_size) > target_w:
        clamped = clamped[:-1]

    return (clamped.rstrip() + suffix) if clamped else text_str[:1]


def wrap_sans_text_to_lines(
    text: Any,
    max_width: float,
    font_size: float = 13.0,
    max_lines: int = 2,
    suffix: str = "...",
) -> List[str]:
    """
    Splits Sans-Serif text across lines based on word boundaries.
    """
    if not text:
        return []
    words = str(text).strip().split()
    if not words:
        return []

    lines: List[str] = []
    curr_line: List[str] = []

    for i, w in enumerate(words):
        test_line = " ".join(curr_line + [w])
        if measure_sans_text_width(test_line, font_size) <= max_width or not curr_line:
            curr_line.append(w)
        else:
            lines.append(" ".join(curr_line))
            curr_line = [w]
            if len(lines) == max_lines - 1:
                remaining_words = words[i:]
                last_line = " ".join(remaining_words)
                lines.append(clamp_sans_text_to_width(last_line, max_width, font_size, suffix=suffix))
                curr_line = []
                break

    if curr_line and len(lines) < max_lines:
        line_str = " ".join(curr_line)
        if measure_sans_text_width(line_str, font_size) > max_width:
            line_str = clamp_sans_text_to_width(line_str, max_width, font_size, suffix=suffix)
        lines.append(line_str)
    elif curr_line and lines:
        lines[-1] = clamp_sans_text_to_width(lines[-1] + " " + " ".join(curr_line), max_width, font_size, suffix=suffix)

    return lines

