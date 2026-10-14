"""
Markdown Compiler / Transpiler for ReadmeKit v5.1
Parses markdown files containing pixel-kit directives:
  <!-- pixel-kit:header ... -->
  <!-- pixel-kit:window ... --> ... <!-- /pixel-kit:window -->
  <!-- pixel-kit:terminal ... --> ... <!-- /pixel-kit:terminal -->
  <!-- pixel-kit:quote ... --> ... <!-- /pixel-kit:quote -->
  <!-- pixel-kit:footer ... -->
  <!-- pixel-kit:callout ... -->
  <!-- pixel-kit:divider ... -->
  <!-- pixel-kit:splitter ... -->
  <!-- pixel-kit:chip ... -->

Supports multi-mode theming:
  mode="auto"        (Default: Single adaptive SVG with CSS @media (prefers-color-scheme: dark))
  mode="dark"        (Always dark palette)
  mode="light"       (Always light palette)
  mode="transparent" (Dark palette with transparent background)
  mode="gh"          (GitHub syntax: generates -dark and -light files, #gh-*-mode-only markup)
  mode="picture"     (HTML5 <picture> tag: generates -dark and -light files)

Automatically generates all requested SVGs into --assets-dir, creates proper
100% full-width table wrappers, quote formats, and details/summary blocks,
and outputs the compiled README markdown.
"""

import os
import re
import json
import urllib.request
from generator.engine import (
    generate_header,
    generate_footer,
    generate_callout,
    generate_frame,
    generate_chip,
    generate_divider,
    generate_splitter,
    generate_metrics,
    generate_progress,
    generate_techstack,
    generate_timeline,
    generate_social,
    generate_starchart,
    generate_profile_card,
    validate_svg,
    escape_xml
)
from generator.themes import normalize_style_and_theme
from generator.cache import BuildCache
from generator.github_api import (
    fetch_repo_data,
    fetch_user_data,
    fetch_star_trajectory,
    fetch_github_stat,
    _GITHUB_CACHE
)


def parse_directive_attrs(attr_string):
    """Parses key="value" or key=value attributes from a directive string."""
    attrs = {}
    pattern = re.compile(r'(\w+)=(?:"([^"]*)"|\'([^\']*)\'|([^\s>]+))')
    for m in pattern.finditer(attr_string):
        key = m.group(1).lower()
        val = m.group(2) if m.group(2) is not None else (m.group(3) if m.group(3) is not None else m.group(4))
        attrs[key] = val
    return attrs

class MarkdownCompiler:
    def __init__(self, assets_dir="assets/generated", base_url="", use_cache=True, cache_file=None, bust_cache=False, fetch_github=False):
        self.assets_dir = assets_dir
        self.base_url = base_url
        self.counters = {}
        if cache_file is None:
            cache_file = os.path.join(assets_dir, ".pixel-cache.json") if assets_dir else ".pixel-cache.json"
        self.cache = BuildCache(cache_file=cache_file, enabled=use_cache)
        self.active_files = set()
        self.orphans = []
        self.stats = {"generated": 0, "cached": 0, "cleaned": 0}
        self.bust_cache = bust_cache
        self.fetch_github = fetch_github

    def _apply_cache_bust(self, url: str) -> str:
        """Appends ?v=<hash> cache-busting query parameter for GitHub Camo proxy."""
        if not self.bust_cache or not url:
            return url
        clean_url = url.split("#")[0].split("?")[0]
        norm_path = os.path.normpath(clean_url).replace("\\", "/")
        cached_entry = self.cache.entries.get(norm_path)
        if not cached_entry:
            for k, v in self.cache.entries.items():
                if os.path.basename(k) == os.path.basename(clean_url):
                    cached_entry = v
                    break
        content_hash = cached_entry.get("hash") if cached_entry else None
        short_v = content_hash[:8] if content_hash else "v4"

        if "#" in url:
            base, fragment = url.split("#", 1)
            sep = "&" if "?" in base else "?"
            return f"{base}{sep}v={short_v}#{fragment}"
        else:
            sep = "&" if "?" in url else "?"
            return f"{url}{sep}v={short_v}"

    def _next_file(self, prefix, ext="svg"):
        count = self.counters.get(prefix, 0) + 1
        self.counters[prefix] = count
        filename = f"{prefix}-{count}.{ext}"
        filepath = os.path.join(self.assets_dir, filename)
        try:
            rel_url = os.path.relpath(filepath, ".").replace("\\", "/")
        except ValueError:
            rel_url = filepath.replace("\\", "/")
        return filepath, rel_url

    def _save_asset(self, generator_fn, gen_kwargs, custom_out, default_prefix):
        """
        Saves or retrieves SVG asset using incremental caching.
        Skips generator_fn execution and disk writing if cache is valid.
        """
        if custom_out:
            filepath = custom_out
            rel_url = custom_out.replace("\\", "/")
        else:
            filepath, rel_url = self._next_file(default_prefix)

        norm_path = os.path.normpath(filepath).replace("\\", "/")
        self.active_files.add(norm_path)

        cache_key = {
            "fn": generator_fn.__name__,
            "kwargs": gen_kwargs
        }
        content_hash = self.cache.compute_hash(cache_key)

        if self.cache.is_valid(filepath, content_hash):
            self.stats["cached"] += 1
            return rel_url

        svg_content = generator_fn(**gen_kwargs)
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        validate_svg(svg_content)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(svg_content)

        self.cache.record(filepath, content_hash)
        self.stats["generated"] += 1
        return rel_url

    def _save_svg(self, svg_content, custom_out, default_prefix):
        """Direct SVG saving with cache recording for raw content."""
        if custom_out:
            filepath = custom_out
            rel_url = custom_out.replace("\\", "/")
        else:
            filepath, rel_url = self._next_file(default_prefix)

        norm_path = os.path.normpath(filepath).replace("\\", "/")
        self.active_files.add(norm_path)

        content_hash = self.cache.compute_hash(svg_content)
        if self.cache.is_valid(filepath, content_hash):
            self.stats["cached"] += 1
            return rel_url

        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        validate_svg(svg_content)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(svg_content)

        self.cache.record(filepath, content_hash)
        self.stats["generated"] += 1
        return rel_url

    def clean_assets(self, dry_run=False) -> list:
        """
        Scans assets_dir and identifies orphan SVG files not referenced
        during the compilation run. Removes them unless dry_run is True.
        """
        orphans = []
        if not os.path.exists(self.assets_dir):
            return orphans

        active_normalized = {os.path.normpath(f).replace("\\", "/") for f in self.active_files}

        for root, _, files in os.walk(self.assets_dir):
            for file in files:
                if not file.lower().endswith(".svg"):
                    continue
                full_path = os.path.join(root, file)
                norm_path = os.path.normpath(full_path).replace("\\", "/")
                if norm_path not in active_normalized:
                    orphans.append(full_path)

        if not dry_run:
            for f in orphans:
                try:
                    os.remove(f)
                    self.cache.remove(f)
                    self.stats["cleaned"] += 1
                except OSError:
                    pass

        return orphans

    def _render_asset_markup(self, generator_fn, kwargs, attrs, default_prefix, alt="", is_full_width=True, link=None):
        mode = attrs.get("mode", "auto").lower()
        custom_out = attrs.get("out")

        width_attr = ' width="100%"' if is_full_width else ""
        alt_attr = f' alt="{escape_xml(alt)}"' if alt else ""

        def _format_url(busted_url: str) -> str:
            if self.base_url:
                return f"{self.base_url.rstrip('/')}/{busted_url.lstrip('/')}"
            return busted_url

        if mode in ("gh", "github"):
            kwargs_dark = dict(kwargs, mode="dark")
            kwargs_light = dict(kwargs, mode="light")

            if custom_out:
                base, ext = os.path.splitext(custom_out)
                out_dark = f"{base}-dark{ext}"
                out_light = f"{base}-light{ext}"
            else:
                out_dark = None
                out_light = None

            url_dark = self._save_asset(generator_fn, kwargs_dark, out_dark, f"{default_prefix}-dark")
            url_light = self._save_asset(generator_fn, kwargs_light, out_light, f"{default_prefix}-light")

            url_dark_busted = _format_url(self._apply_cache_bust(f"{url_dark}#gh-dark-mode-only"))
            url_light_busted = _format_url(self._apply_cache_bust(f"{url_light}#gh-light-mode-only"))

            img_dark = f'<img src="{url_dark_busted}"{width_attr}{alt_attr} />'
            img_light = f'<img src="{url_light_busted}"{width_attr}{alt_attr} />'

            if link:
                escaped_link = escape_xml(link)
                img_dark = f'<a href="{escaped_link}">{img_dark}</a>'
                img_light = f'<a href="{escaped_link}">{img_light}</a>'

            return f"{img_dark}\n{img_light}"

        elif mode == "picture":
            kwargs_dark = dict(kwargs, mode="dark")
            kwargs_light = dict(kwargs, mode="light")

            if custom_out:
                base, ext = os.path.splitext(custom_out)
                out_dark = f"{base}-dark{ext}"
                out_light = f"{base}-light{ext}"
            else:
                out_dark = None
                out_light = None

            url_dark = self._save_asset(generator_fn, kwargs_dark, out_dark, f"{default_prefix}-dark")
            url_light = self._save_asset(generator_fn, kwargs_light, out_light, f"{default_prefix}-light")

            url_dark_busted = _format_url(self._apply_cache_bust(url_dark))
            url_light_busted = _format_url(self._apply_cache_bust(url_light))

            pic = f"""<picture>
  <source media="(prefers-color-scheme: dark)" srcset="{url_dark_busted}">
  <source media="(prefers-color-scheme: light)" srcset="{url_light_busted}">
  <img src="{url_dark_busted}"{width_attr}{alt_attr} />
</picture>"""
            if link:
                escaped_link = escape_xml(link)
                pic = f'<a href="{escaped_link}">\n{pic}\n</a>'
            return pic

        else:
            # "auto" (default adaptive), "dark", "light", "transparent"
            kwargs_single = dict(kwargs, mode=mode)
            url = self._save_asset(generator_fn, kwargs_single, custom_out, default_prefix)
            url_busted = _format_url(self._apply_cache_bust(url))
            img = f'<img src="{url_busted}"{width_attr}{alt_attr} />'
            if link:
                escaped_link = escape_xml(link)
                img = f'<a href="{escaped_link}">{img}</a>'
            return img

    def compile_text(self, markdown_text, template_dir=None):
        """Compiles template markdown string into full GitHub markdown with SVGs."""
        os.makedirs(self.assets_dir, exist_ok=True)
        self.counters = {}
        self.active_files = set()
        self.stats = {"generated": 0, "cached": 0, "cleaned": 0}
        text = markdown_text

        # ---------------------------------------------------------------
        # 1. CONTAINERS: WINDOW
        # <!-- pixel-kit:window style="..." title="..." [tag="..."] [primary="..."] [accent="..."] [mode="..."] [out_top="..."] [out_bottom="..."] -->
        # ...
        # <!-- /pixel-kit:window -->
        # ---------------------------------------------------------------
        window_regex = re.compile(
            r'<!--\s*(?:pixel-kit|readme-kit):window\s+(.*?)\s*-->((?:(?!<!--\s*/?(?:pixel-kit|readme-kit):window)[\s\S])*?)<!--\s*/(?:pixel-kit|readme-kit):window\s*-->',
            re.IGNORECASE
        )

        def repl_window(m):
            attrs = parse_directive_attrs(m.group(1))
            inner_content = m.group(2).strip()
            style, theme = normalize_style_and_theme(attrs.get("style"), attrs.get("theme"))
            title = attrs.get("title", "╔═ SYSTEM.CORE // WINDOW.SYS")
            tag = attrs.get("tag", "[OPEN_HUD]")
            prim = attrs.get("primary", None)
            acc = attrs.get("accent", None)
            tert = attrs.get("tertiary", None)
            preset = attrs.get("preset", None)

            attrs_top = dict(attrs)
            if "out_top" in attrs:
                attrs_top["out"] = attrs["out_top"]
            elif "out" in attrs:
                del attrs_top["out"]

            attrs_bot = dict(attrs)
            if "out_bottom" in attrs:
                attrs_bot["out"] = attrs["out_bottom"]
            elif "out" in attrs:
                del attrs_bot["out"]

            tag_url = attrs.get("tag_url") or attrs.get("tag_href")
            close_url = attrs.get("close_url") or attrs.get("close_href")

            rendered_top = self._render_asset_markup(
                generate_frame,
                {"style": style, "theme": theme, "primary": prim, "accent": acc, "tertiary": tert, "frame_type": "top", "title": title, "tag": tag, "preset": preset, "tag_url": tag_url, "close_url": close_url},
                attrs_top,
                f"frame-top-{theme}",
                is_full_width=True
            )
            rendered_bot = self._render_asset_markup(
                generate_frame,
                {"style": style, "theme": theme, "primary": prim, "accent": acc, "tertiary": tert, "frame_type": "bottom", "title": title, "tag": tag, "preset": preset},
                attrs_bot,
                f"frame-bottom-{theme}",
                is_full_width=True
            )

            if style.lower() in ("minimal", "modern", "sketch") or theme.lower() in ("minimal", "clean-mono", "academic-paper", "corporate-blue", "swiss-mono", "executive-slate", "slate-dark", "nordic-frost", "linear-violet", "emerald-clean", "modern-slate", "excali-dark", "whiteboard", "notebook-graph", "blueprint-sketch"):
                # Integrated 3-row single table monolith
                return f"""<table width="100%">
<tr>
<td width="100%" align="center">
{rendered_top}
</td>
</tr>
<tr>
<td width="2000">

{inner_content}

</td>
</tr>
<tr>
<td width="100%" align="center">
{rendered_bot}
</td>
</tr>
</table>"""
            else:
                # Direct capping 1-cell table
                return f"""{rendered_top}

<table width="100%">
<tr>
<td width="2000">

{inner_content}

</td>
</tr>
</table>

{rendered_bot}"""

        text = window_regex.sub(repl_window, text)

        # ---------------------------------------------------------------
        # 2. CONTAINERS: TERMINAL (Details/Summary)
        # <!-- pixel-kit:terminal style="..." title="..." [state="open|closed"] [primary="..."] [accent="..."] [preset="..."] [mode="..."] -->
        # ...
        # <!-- /pixel-kit:terminal -->
        # ---------------------------------------------------------------
        terminal_regex = re.compile(
            r'<!--\s*(?:pixel-kit|readme-kit):terminal\s+(.*?)\s*-->((?:(?!<!--\s*/?(?:pixel-kit|readme-kit):terminal)[\s\S])*?)<!--\s*/(?:pixel-kit|readme-kit):terminal\s*-->',
            re.IGNORECASE
        )

        def repl_terminal(m):
            attrs = parse_directive_attrs(m.group(1))
            inner_content = m.group(2).strip()
            style, theme = normalize_style_and_theme(attrs.get("style"), attrs.get("theme"))
            title = attrs.get("title", "HUD.TERMINAL")
            state = attrs.get("state", "open").lower()
            prim = attrs.get("primary", None)
            acc = attrs.get("accent", None)
            tert = attrs.get("tertiary", None)
            preset = attrs.get("preset", None)

            attrs_top = dict(attrs)
            if "out_top" in attrs:
                attrs_top["out"] = attrs["out_top"]
            elif "out" in attrs:
                del attrs_top["out"]

            attrs_bot = dict(attrs)
            if "out_bottom" in attrs:
                attrs_bot["out"] = attrs["out_bottom"]
            elif "out" in attrs:
                del attrs_bot["out"]

            rendered_top = self._render_asset_markup(
                generate_frame,
                {"style": style, "theme": theme, "primary": prim, "accent": acc, "tertiary": tert, "frame_type": "top", "title": f"╔═ {title} // RUNTIME.SYS", "preset": preset},
                attrs_top,
                f"terminal-top-{theme}",
                is_full_width=True
            )
            rendered_bot = self._render_asset_markup(
                generate_frame,
                {"style": style, "theme": theme, "primary": prim, "accent": acc, "tertiary": tert, "frame_type": "bottom", "preset": preset},
                attrs_bot,
                f"terminal-bottom-{theme}",
                is_full_width=True
            )

            open_attr = "open" if state == "open" else ""
            status_text = "STATE: EXPANDED" if state == "open" else "CLICK TO EXPAND"

            return f"""<details {open_attr}>
<summary><kbd>▶ {title}</kbd> <b>[ НАЖМИТЕ ДЛЯ СВОРАЧИВАНИЯ / РАЗВОРАЧИВАНИЯ ]</b> <code>[{status_text}]</code></summary>

<br/>

{rendered_top}

<table width="100%">
<tr>
<td width="2000">

{inner_content}

</td>
</tr>
</table>

{rendered_bot}

</details>"""

        text = terminal_regex.sub(repl_terminal, text)

        # ---------------------------------------------------------------
        # 3. CONTAINERS: QUOTE CALLOUT
        # <!-- pixel-kit:quote style="..." title="..." [subtitle="..."] [badge="..."] [primary="..."] [accent="..."] [preset="..."] [mode="..."] -->
        # ...
        # <!-- /pixel-kit:quote -->
        # ---------------------------------------------------------------
        quote_regex = re.compile(
            r'<!--\s*(?:pixel-kit|readme-kit):quote\s+(.*?)\s*-->((?:(?!<!--\s*/?(?:pixel-kit|readme-kit):quote)[\s\S])*?)<!--\s*/(?:pixel-kit|readme-kit):quote\s*-->',
            re.IGNORECASE
        )

        def repl_quote(m):
            attrs = parse_directive_attrs(m.group(1))
            inner_content = m.group(2).strip()
            style, theme = normalize_style_and_theme(attrs.get("style"), attrs.get("theme"))
            title = attrs.get("title", "SPECIFICATION NOTICE")
            sub = attrs.get("subtitle", "Content flows into live blockquote text")
            badge = attrs.get("badge", "NOTE")
            badge_color = attrs.get("badge_color", None)
            prim = attrs.get("primary", None)
            acc = attrs.get("accent", None)
            preset = attrs.get("preset", None)

            rendered_q = self._render_asset_markup(
                generate_callout,
                {"style": style, "theme": theme, "primary": prim, "accent": acc, "callout_type": badge, "title": title, "subtitle": sub, "is_quote": True, "preset": preset, "badge_color": badge_color},
                attrs,
                f"callout-quote-{theme}",
                alt=title,
                is_full_width=True
            )

            quote_header_lines = "\n".join([f"> {line}" for line in rendered_q.splitlines()])
            prefixed_lines = "\n".join([f"> {line}" if line.strip() else ">" for line in inner_content.splitlines()])

            return f"""{quote_header_lines}
>
{prefixed_lines}"""

        text = quote_regex.sub(repl_quote, text)

        # ---------------------------------------------------------------
        # 3B. CONTAINERS: METRICS / KPI
        # <!-- pixel-kit:metrics style="..." [primary="..."] [accent="..."] [preset="..."] [mode="..."] [out="..."] -->
        # - label="FPS BENCHMARK" value="1,200+" delta="+24% vs baseline" trend="up"
        # - label="CONTAINER POINTS" value="100K" status="OPTIMAL"
        # <!-- /pixel-kit:metrics -->
        # ---------------------------------------------------------------
        metrics_regex = re.compile(
            r'<!--\s*(?:pixel-kit|readme-kit):metrics\s*(.*?)\s*-->((?:(?!<!--\s*/?(?:pixel-kit|readme-kit):metrics)[\s\S])*?)<!--\s*/(?:pixel-kit|readme-kit):metrics\s*-->',
            re.IGNORECASE
        )

        def repl_metrics(m):
            attrs = parse_directive_attrs(m.group(1))
            inner_content = m.group(2).strip()
            style, theme = normalize_style_and_theme(attrs.get("style"), attrs.get("theme"))
            prim = attrs.get("primary", None)
            acc = attrs.get("accent", None)
            preset = attrs.get("preset", None)

            metric_items = []
            for line in inner_content.splitlines():
                line = line.strip()
                if not line:
                    continue
                if line.startswith("<!--") and line.endswith("-->"):
                    line = line[4:-3].strip()
                if line.startswith(("-", "*")):
                    line = line[1:].strip()
                for prefix in ("card", "metric", "item"):
                    if line.lower().startswith(prefix):
                        line = line[len(prefix):].strip()
                        break
                item_attrs = parse_directive_attrs(line)
                if item_attrs:
                    metric_items.append(item_attrs)

            return self._render_asset_markup(
                generate_metrics,
                {"metrics": metric_items, "style": style, "theme": theme, "primary": prim, "accent": acc, "preset": preset},
                attrs,
                f"metrics-{theme}",
                alt="Metrics",
                is_full_width=True
            )

        text = metrics_regex.sub(repl_metrics, text)

        # ---------------------------------------------------------------
        # 3C. CONTAINERS: TIMELINE / ROADMAP
        # <!-- pixel-kit:timeline style="..." [primary="..."] [accent="..."] [preset="..."] [mode="..."] [out="..."] -->
        # - title="PHASE 1" date="2026-Q1" status="COMPLETED" desc="Architecture"
        # - title="PHASE 2" date="2026-Q2" status="IN_PROGRESS" desc="Widgets"
        # <!-- /pixel-kit:timeline -->
        # ---------------------------------------------------------------
        timeline_regex = re.compile(
            r'<!--\s*(?:pixel-kit|readme-kit):timeline\s*(.*?)\s*-->((?:(?!<!--\s*/?(?:pixel-kit|readme-kit):timeline)[\s\S])*?)<!--\s*/(?:pixel-kit|readme-kit):timeline\s*-->',
            re.IGNORECASE
        )

        def repl_timeline(m):
            attrs = parse_directive_attrs(m.group(1))
            inner_content = m.group(2).strip()
            style, theme = normalize_style_and_theme(attrs.get("style"), attrs.get("theme"))
            prim = attrs.get("primary", None)
            acc = attrs.get("accent", None)
            preset = attrs.get("preset", None)

            timeline_items = []
            for line in inner_content.splitlines():
                line = line.strip()
                if not line:
                    continue
                if line.startswith("<!--") and line.endswith("-->"):
                    line = line[4:-3].strip()
                if line.startswith(("-", "*")):
                    line = line[1:].strip()
                for prefix in ("milestone", "stage", "item"):
                    if line.lower().startswith(prefix):
                        line = line[len(prefix):].strip()
                        break
                item_attrs = parse_directive_attrs(line)
                if item_attrs:
                    timeline_items.append(item_attrs)

            return self._render_asset_markup(
                generate_timeline,
                {"items": timeline_items, "style": style, "theme": theme, "primary": prim, "accent": acc, "preset": preset},
                attrs,
                f"timeline-{theme}",
                alt="Timeline",
                is_full_width=True
            )

        text = timeline_regex.sub(repl_timeline, text)

        # ---------------------------------------------------------------
        # 4. STANDALONE: HEADER
        # <!-- pixel-kit:header style="..." title="..." subtitle="..." [tag="..."] [primary="..."] [accent="..."] [preset="..."] [mode="..."] [out="..."] -->
        # ---------------------------------------------------------------
        header_regex = re.compile(r'<!--\s*(?:pixel-kit|readme-kit):header\s+(.*?)\s*-->', re.IGNORECASE)

        def repl_header(m):
            attrs = parse_directive_attrs(m.group(1))
            style, theme = normalize_style_and_theme(attrs.get("style"), attrs.get("theme"))
            title = attrs.get("title", "PIXEL-KIT")
            sub = attrs.get("subtitle", "TRANSLUCENT HUD DESIGN SYSTEM")
            tag = attrs.get("tag", "SYSTEM_ACTIVE")
            prim = attrs.get("primary", None)
            acc = attrs.get("accent", None)
            preset = attrs.get("preset", None)
            tert = attrs.get("tertiary", None)

            spec1 = attrs.get("spec1", None)
            spec2 = attrs.get("spec2", None)
            spec3 = attrs.get("spec3", None)
            specs = attrs.get("specs", None)

            tag_url = attrs.get("tag_url") or attrs.get("tag_href")
            close_url = attrs.get("close_url") or attrs.get("close_href")
            raw_compact = attrs.get("compact", False)
            compact = raw_compact if isinstance(raw_compact, bool) else str(raw_compact).lower() in ("true", "1", "yes")

            return self._render_asset_markup(
                generate_header,
                {
                    "style": style, "theme": theme, "primary": prim, "accent": acc, "tertiary": tert, "title": title,
                    "subtitle": sub, "tag": tag, "spec1": spec1, "spec2": spec2,
                    "spec3": spec3, "specs": specs, "preset": preset,
                    "tag_url": tag_url, "close_url": close_url, "compact": compact
                },
                attrs,
                f"header-{theme}",
                alt=title,
                is_full_width=True
            )

        text = header_regex.sub(repl_header, text)

        # ---------------------------------------------------------------
        # 5. STANDALONE: FOOTER
        # <!-- pixel-kit:footer style="..." status="..." [nav="..."] [primary="..."] [accent="..."] [preset="..."] [mode="..."] [out="..."] -->
        # ---------------------------------------------------------------
        footer_regex = re.compile(r'<!--\s*(?:pixel-kit|readme-kit):footer\s+(.*?)\s*-->', re.IGNORECASE)

        def repl_footer(m):
            attrs = parse_directive_attrs(m.group(1))
            style, theme = normalize_style_and_theme(attrs.get("style"), attrs.get("theme"))
            status = attrs.get("status", "SYSTEM_ACTIVE // STANDBY")
            nav = attrs.get("nav", "RETURN TO TOP")
            sub = attrs.get("sub") or attrs.get("sub_text") or None
            prim = attrs.get("primary", None)
            acc = attrs.get("accent", None)
            tert = attrs.get("tertiary", None)
            preset = attrs.get("preset", None)

            return self._render_asset_markup(
                generate_footer,
                {"style": style, "theme": theme, "primary": prim, "accent": acc, "tertiary": tert, "status": status, "nav_text": nav, "sub_text": sub, "preset": preset},
                attrs,
                f"footer-{theme}",
                alt=nav,
                is_full_width=True,
                link="#top"
            )

        text = footer_regex.sub(repl_footer, text)

        # ---------------------------------------------------------------
        # 6. STANDALONE: CALLOUT (Autonomous)
        # <!-- pixel-kit:callout style="..." type="..." title="..." [subtitle="..."] [primary="..."] [accent="..."] [preset="..."] [mode="..."] [out="..."] -->
        # ---------------------------------------------------------------
        callout_regex = re.compile(r'<!--\s*(?:pixel-kit|readme-kit):callout\s+(.*?)\s*-->', re.IGNORECASE)

        def repl_callout(m):
            attrs = parse_directive_attrs(m.group(1))
            style, theme = normalize_style_and_theme(attrs.get("style"), attrs.get("theme"))
            ctype = attrs.get("type", "note")
            badge_color = attrs.get("badge_color", None)
            title = attrs.get("title", "SYSTEM SPECIFICATION")
            sub = attrs.get("subtitle", "")
            prim = attrs.get("primary", None)
            acc = attrs.get("accent", None)
            preset = attrs.get("preset", None)

            return self._render_asset_markup(
                generate_callout,
                {"style": style, "theme": theme, "primary": prim, "accent": acc, "callout_type": ctype, "title": title, "subtitle": sub, "is_quote": False, "preset": preset, "badge_color": badge_color},
                attrs,
                f"callout-{theme}-{ctype}",
                alt=title,
                is_full_width=True
            )

        text = callout_regex.sub(repl_callout, text)

        # ---------------------------------------------------------------
        # 7. STANDALONE: DIVIDER
        # <!-- pixel-kit:divider style="..." [primary="..."] [accent="..."] [preset="..."] [mode="..."] [out="..."] -->
        # ---------------------------------------------------------------
        divider_regex = re.compile(r'<!--\s*(?:pixel-kit|readme-kit):divider\s+(.*?)\s*-->', re.IGNORECASE)

        def repl_divider(m):
            attrs = parse_directive_attrs(m.group(1))
            style, theme = normalize_style_and_theme(attrs.get("style"), attrs.get("theme"))
            prim = attrs.get("primary", None)
            acc = attrs.get("accent", None)
            preset = attrs.get("preset", None)

            return self._render_asset_markup(
                generate_divider,
                {"style": style, "theme": theme, "primary": prim, "accent": acc, "preset": preset},
                attrs,
                f"divider-{theme}",
                alt=f"Divider {theme}",
                is_full_width=True
            )

        text = divider_regex.sub(repl_divider, text)

        # ---------------------------------------------------------------
        # 8. STANDALONE: SPLITTER
        # <!-- pixel-kit:splitter style="..." label="..." [primary="..."] [accent="..."] [preset="..."] [mode="..."] [out="..."] -->
        # ---------------------------------------------------------------
        splitter_regex = re.compile(r'<!--\s*(?:pixel-kit|readme-kit):splitter\s+(.*?)\s*-->', re.IGNORECASE)

        def repl_splitter(m):
            attrs = parse_directive_attrs(m.group(1))
            style, theme = normalize_style_and_theme(attrs.get("style"), attrs.get("theme"))
            label = attrs.get("label", "[MODULE: SUB_SYSTEM]")
            prim = attrs.get("primary", None)
            acc = attrs.get("accent", None)
            preset = attrs.get("preset", None)

            return self._render_asset_markup(
                generate_splitter,
                {"style": style, "theme": theme, "primary": prim, "accent": acc, "label": label, "preset": preset},
                attrs,
                f"splitter-{theme}",
                alt=label,
                is_full_width=True
            )

        text = splitter_regex.sub(repl_splitter, text)

        # ---------------------------------------------------------------
        # 9. STANDALONE: CHIP
        # <!-- pixel-kit:chip style="..." [type="closed|decay|pulse"] [text="..."] [github="stars|forks|issues|license|watchers|version|release"] [repo="owner/repo"] [primary="..."] [accent="..."] [preset="..."] [mode="..."] [out="..."] -->
        # ---------------------------------------------------------------
        chip_regex = re.compile(r'<!--\s*(?:pixel-kit|readme-kit):chip\s+(.*?)\s*-->', re.IGNORECASE)

        def repl_chip(m):
            attrs = parse_directive_attrs(m.group(1))
            style, theme = normalize_style_and_theme(attrs.get("style"), attrs.get("theme"))
            ctype = attrs.get("type", "closed")
            text_val = attrs.get("text", "CHIP")
            prim = attrs.get("primary", None)
            acc = attrs.get("accent", None)
            preset = attrs.get("preset", None)

            w_val = int(attrs["width"]) if "width" in attrs and attrs["width"].isdigit() else None
            link_url = attrs.get("url") or attrs.get("href") or attrs.get("link")

            gh_stat = attrs.get("github") or attrs.get("gh")
            if not gh_stat and "repo" in attrs and text_val.lower() in ("stars", "forks", "issues", "watchers", "license", "version", "release"):
                gh_stat = text_val.lower()

            if gh_stat:
                repo_name = attrs.get("repo", "Kazinagg/readme-kit")
                raw_af = attrs.get("auto_fetch")
                if raw_af is not None:
                    auto_fetch = raw_af if isinstance(raw_af, bool) else str(raw_af).lower() not in ("false", "0", "no")
                else:
                    auto_fetch = True
                stat_text, stat_link = fetch_github_stat(repo_name, gh_stat, auto_fetch=auto_fetch)
                text_val = stat_text
                if not link_url:
                    link_url = stat_link

            decay_dir = attrs.get("decay_dir") or attrs.get("direction", "right")

            return self._render_asset_markup(
                generate_chip,
                {"style": style, "theme": theme, "primary": prim, "accent": acc, "chip_type": ctype, "text": text_val, "width": w_val, "preset": preset, "decay_dir": decay_dir},
                attrs,
                f"chip-{theme}-{ctype}",
                alt=text_val,
                is_full_width=False,
                link=link_url
            )

        text = chip_regex.sub(repl_chip, text)

        # ---------------------------------------------------------------
        # 9.5 STANDALONE: METRICS
        # <!-- pixel-kit:metrics style="..." [items="..."] [repo="..."] [auto_fetch="true"] [primary="..."] [accent="..."] [preset="..."] [mode="..."] [out="..."] -->
        # ---------------------------------------------------------------
        metrics_regex = re.compile(r'<!--\s*(?:pixel-kit|readme-kit):metrics\s+(.*?)\s*-->', re.IGNORECASE)

        def repl_metrics(m):
            attrs = parse_directive_attrs(m.group(1))
            style, theme = normalize_style_and_theme(attrs.get("style"), attrs.get("theme"))
            repo = attrs.get("repo")
            prim = attrs.get("primary", None)
            acc = attrs.get("accent", None)
            preset = attrs.get("preset", None)
            auto_fetch = attrs.get("auto_fetch", "").lower() in ("true", "1", "yes") or (self.fetch_github and bool(repo))

            card_items = []
            if auto_fetch and repo:
                rdata, _ = fetch_repo_data(repo)
                if rdata:
                    card_items = [
                        {"label": "STARS", "value": f"{rdata['stars']:,}", "delta": "+growth", "trend": "up"},
                        {"label": "FORKS", "value": f"{rdata['forks']:,}", "delta": "active", "trend": "up"},
                        {"label": "WATCHERS", "value": f"{rdata['watchers']:,}", "trend": "neutral"},
                        {"label": "LICENSE", "value": rdata["license"], "trend": "neutral"}
                    ]

            if not card_items:
                raw_items = attrs.get("items")
                if raw_items:
                    for chunk in raw_items.split("|"):
                        parsed_chunk = parse_directive_attrs(chunk.strip())
                        if parsed_chunk:
                            card_items.append(parsed_chunk)
                        elif ":" in chunk:
                            k, v = chunk.split(":", 1)
                            card_items.append({"label": k.strip(), "value": v.strip()})

            if not card_items:
                card_items = [
                    {"label": "ACTIVE REPOS", "value": "12", "delta": "+2", "trend": "up"},
                    {"label": "CONTRIBUTIONS", "value": "1,420", "delta": "+18%", "trend": "up"},
                    {"label": "STARS", "value": "350", "delta": "+45", "trend": "up"}
                ]

            return self._render_asset_markup(
                generate_metrics,
                {"metrics": card_items, "style": style, "theme": theme, "primary": prim, "accent": acc, "preset": preset},
                attrs,
                f"metrics-{theme}",
                alt="Metrics",
                is_full_width=True
            )

        text = metrics_regex.sub(repl_metrics, text)

        # ---------------------------------------------------------------
        # 10. STANDALONE: PROGRESS
        # <!-- pixel-kit:progress style="..." value="80" label="..." [sub="..."] [primary="..."] [accent="..."] [preset="..."] [mode="..."] [out="..."] -->
        # ---------------------------------------------------------------
        progress_regex = re.compile(r'<!--\s*(?:pixel-kit|readme-kit):progress\s+(.*?)\s*-->', re.IGNORECASE)

        def repl_progress(m):
            attrs = parse_directive_attrs(m.group(1))
            style, theme = normalize_style_and_theme(attrs.get("style"), attrs.get("theme"))
            val = attrs.get("value", 50)
            label = attrs.get("label", "PROGRESS")
            sub = attrs.get("sub") or attrs.get("subtitle")
            prim = attrs.get("primary", None)
            acc = attrs.get("accent", None)
            preset = attrs.get("preset", None)

            return self._render_asset_markup(
                generate_progress,
                {"value": val, "label": label, "sub": sub, "style": style, "theme": theme, "primary": prim, "accent": acc, "preset": preset},
                attrs,
                f"progress-{theme}",
                alt=label,
                is_full_width=True
            )

        text = progress_regex.sub(repl_progress, text)

        # ---------------------------------------------------------------
        # 11. STANDALONE: TECHSTACK
        # <!-- pixel-kit:techstack style="..." items="cpp,opengl,delphi,git,docker" [columns="5"] [primary="..."] [accent="..."] [preset="..."] [mode="..."] [out="..."] -->
        # ---------------------------------------------------------------
        techstack_regex = re.compile(r'<!--\s*(?:pixel-kit|readme-kit):techstack\s+(.*?)\s*-->', re.IGNORECASE)

        def repl_techstack(m):
            attrs = parse_directive_attrs(m.group(1))
            style, theme = normalize_style_and_theme(attrs.get("style"), attrs.get("theme"))
            items = attrs.get("items", "python,cpp,rust,docker,git")
            cols = int(attrs.get("columns", 5)) if "columns" in attrs and attrs["columns"].isdigit() else 5
            prim = attrs.get("primary", None)
            acc = attrs.get("accent", None)
            preset = attrs.get("preset", None)

            return self._render_asset_markup(
                generate_techstack,
                {"items": items, "columns": cols, "style": style, "theme": theme, "primary": prim, "accent": acc, "preset": preset},
                attrs,
                f"techstack-{theme}",
                alt="Tech Stack",
                is_full_width=True
            )

        text = techstack_regex.sub(repl_techstack, text)

        # ---------------------------------------------------------------
        # 12. STANDALONE: SOCIAL PREVIEW (OpenGraph 1280x640)
        # <!-- pixel-kit:social style="..." title="..." subtitle="..." repo="..." tags="..." [primary="..."] [accent="..."] [preset="..."] [mode="..."] [out="..."] -->
        # ---------------------------------------------------------------
        social_regex = re.compile(r'<!--\s*(?:pixel-kit|readme-kit):social\s+(.*?)\s*-->', re.IGNORECASE)

        def repl_social(m):
            attrs = parse_directive_attrs(m.group(1))
            style, theme = normalize_style_and_theme(attrs.get("style"), attrs.get("theme"))
            title = attrs.get("title", "PIXEL-KIT")
            sub = attrs.get("subtitle", "TRANSLUCENT RETRO HUD READMES")
            repo = attrs.get("repo", "Kazinagg/pixel-readme-kit")
            tags = attrs.get("tags", "PYTHON,SVG,HUD,RETRO")
            prim = attrs.get("primary", None)
            acc = attrs.get("accent", None)
            preset = attrs.get("preset", None)

            return self._render_asset_markup(
                generate_social,
                {"style": style, "theme": theme, "title": title, "subtitle": sub, "repo": repo, "tags": tags, "primary": prim, "accent": acc, "preset": preset},
                attrs,
                f"social-{theme}",
                alt=title,
                is_full_width=True
            )

        text = social_regex.sub(repl_social, text)

        # ---------------------------------------------------------------
        # 13. STANDALONE: STARCHART (Star Growth Trend)
        # <!-- pixel-kit:starchart style="..." repo="..." points="..." [current="..."] [delta="..."] [title="..."] [primary="..."] [accent="..."] [preset="..."] [mode="..."] [out="..."] -->
        # ---------------------------------------------------------------
        starchart_regex = re.compile(r'<!--\s*(?:pixel-kit|readme-kit):starchart\s+(.*?)\s*-->', re.IGNORECASE)

        def repl_starchart(m):
            attrs = parse_directive_attrs(m.group(1))
            style, theme = normalize_style_and_theme(attrs.get("style"), attrs.get("theme"))
            repo = attrs.get("repo", "Kazinagg/pixel-readme-kit")
            points = attrs.get("points", None)
            current = attrs.get("current", None)
            delta = attrs.get("delta", "+78% past 6m")
            title = attrs.get("title", "STAR GROWTH TRAJECTORY")
            period = attrs.get("period", "6M")
            prim = attrs.get("primary", None)
            acc = attrs.get("accent", None)
            preset = attrs.get("preset", None)

            auto_fetch = attrs.get("auto_fetch", "").lower() in ("true", "1", "yes") or attrs.get("auto", "").lower() in ("true", "1", "yes") or self.fetch_github
            if auto_fetch and repo:
                traj, _ = fetch_star_trajectory(repo)
                if traj:
                    if points is None:
                        points = traj.get("points")
                    if current is None:
                        current = traj.get("current")
                    if delta == "+78% past 6m" or "delta" not in attrs:
                        delta = traj.get("delta", delta)

            return self._render_asset_markup(
                generate_starchart,
                {
                    "style": style, "theme": theme, "repo": repo, "points": points, "current": current,
                    "delta": delta, "title": title, "period": period,
                    "primary": prim, "accent": acc, "preset": preset
                },
                attrs,
                f"starchart-{theme}",
                alt=title,
                is_full_width=True
            )

        text = starchart_regex.sub(repl_starchart, text)

        # ---------------------------------------------------------------
        # 14. STANDALONE: PROFILE (Developer Dossier Card)
        # <!-- pixel-kit:profile style="..." name="..." role="..." bio="..." [status="..."] [location="..."] [badge="..."] [primary="..."] [accent="..."] [preset="..."] [mode="..."] [out="..."] -->
        # ---------------------------------------------------------------
        profile_regex = re.compile(r'<!--\s*(?:pixel-kit|readme-kit):profile\s+(.*?)\s*-->', re.IGNORECASE)

        def repl_profile(m):
            attrs = parse_directive_attrs(m.group(1))
            style, theme = normalize_style_and_theme(attrs.get("style"), attrs.get("theme"))
            name = attrs.get("name", "ALEX DEVELOPER")
            role = attrs.get("role", "FULLSTACK & SYSTEMS ARCHITECT")
            bio = attrs.get("bio", "Building high-performance runtimes and resilient developer tooling.")
            status = attrs.get("status", "AVAILABLE FOR HIRE")
            location = attrs.get("location", "REMOTE // UTC+3")
            badge = attrs.get("badge", "LEVEL_99")
            prim = attrs.get("primary", None)
            acc = attrs.get("accent", None)
            preset = attrs.get("preset", None)

            username = attrs.get("username") or attrs.get("user")
            auto_fetch = attrs.get("auto_fetch", "").lower() in ("true", "1", "yes") or (self.fetch_github and bool(username))
            if auto_fetch and username:
                udata, _ = fetch_user_data(username)
                if udata:
                    if "name" not in attrs and udata.get("name"):
                        name = udata["name"]
                    if "bio" not in attrs and udata.get("bio"):
                        bio = udata["bio"]
                    if "location" not in attrs and udata.get("location"):
                        location = udata["location"]
                    if "badge" not in attrs and udata.get("public_repos") is not None:
                        badge = f"REPOS: {udata['public_repos']}"

            return self._render_asset_markup(
                generate_profile_card,
                {
                    "style": style, "theme": theme, "name": name, "role": role, "bio": bio,
                    "status": status, "location": location, "badge": badge,
                    "primary": prim, "accent": acc, "preset": preset
                },
                attrs,
                f"profile-{theme}",
                alt=name,
                is_full_width=True
            )

        text = profile_regex.sub(repl_profile, text)

        self.cache.save()
        return text

    def compile_string(self, text):
        """Alias for compile_text."""
        return self.compile_text(text)

    def compile_file(self, input_filepath, output_filepath=None, clean_assets=False, dry_run_clean=False, bust_cache=None):
        """Reads input file, compiles all directives, and writes output file."""
        if bust_cache is not None:
            self.bust_cache = bust_cache

        if output_filepath is None:
            if input_filepath.endswith(".template.md"):
                output_filepath = input_filepath.replace(".template.md", ".md")
            else:
                base, ext = os.path.splitext(input_filepath)
                output_filepath = f"{base}.compiled{ext}"

        with open(input_filepath, "r", encoding="utf-8") as f:
            template_content = f.read()

        compiled_content = self.compile_text(template_content)

        os.makedirs(os.path.dirname(os.path.abspath(output_filepath)), exist_ok=True)
        with open(output_filepath, "w", encoding="utf-8") as f:
            f.write(compiled_content)

        if clean_assets or dry_run_clean:
            self.orphans = self.clean_assets(dry_run=dry_run_clean)

        self.cache.save()
        return output_filepath
