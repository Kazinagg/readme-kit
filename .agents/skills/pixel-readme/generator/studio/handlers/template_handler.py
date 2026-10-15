"""
Template management, block editing, and markdown preview handler for HUD Studio.
"""

import os
import re
import json
import time
from typing import Dict, Any, List
from generator.compiler import MarkdownCompiler, parse_directive_attrs


def extract_template_blocks(template_content: str) -> List[Dict[str, Any]]:
    """
    Parses all readme-kit and pixel-kit directives from markdown text with their exact span indices,
    attributes, and inner body contents.
    """
    block_pattern = re.compile(
        r'(<!--\s*(?:pixel-kit|readme-kit):(window|terminal|quote|metrics|timeline)\b(.*?)-->([\s\S]*?)<!--\s*/(?:pixel-kit|readme-kit):\2\s*-->)',
        re.IGNORECASE
    )
    single_pattern = re.compile(
        r'(<!--\s*(?:pixel-kit|readme-kit):(header|footer|callout|frame|chip|divider|splitter|progress|techstack|social|starchart|profile)\b(.*?)-->)',
        re.IGNORECASE
    )

    blocks = []
    for m in block_pattern.finditer(template_content):
        btype = m.group(2).lower()
        attrs = parse_directive_attrs(m.group(3))
        blocks.append({
            "id": 0,
            "type": btype,
            "attrs": attrs,
            "body": m.group(4).strip(),
            "is_container": True,
            "start": m.start(),
            "end": m.end(),
            "raw": m.group(1)
        })
    for m in single_pattern.finditer(template_content):
        btype = m.group(2).lower()
        attrs = parse_directive_attrs(m.group(3))
        blocks.append({
            "id": 0,
            "type": btype,
            "attrs": attrs,
            "body": "",
            "is_container": False,
            "start": m.start(),
            "end": m.end(),
            "raw": m.group(1)
        })

    blocks.sort(key=lambda x: x["start"])
    for i, b in enumerate(blocks):
        b["id"] = i
    return blocks


def apply_global_theme_to_content(content: str, req: Dict[str, Any]) -> str:
    """Batch-updates style, theme, preset, mode, primary, accent, tertiary across all directives."""
    g_style = req.get("style", "pixel")
    g_theme = req.get("theme", "")
    g_preset = req.get("preset", "cyberpunk")
    g_mode = req.get("mode", "auto")
    g_prim = req.get("primary", "")
    g_acc = req.get("accent", "")
    g_tert = req.get("tertiary", "")
    is_force = bool(req.get("force", False))

    def update_dir(m):
        tag_content = m.group(0)
        tag_type = m.group(1).lower()
        if tag_type.startswith("/"):
            return tag_content

        # 1. Update style
        if re.search(r'\bstyle="[^"]*"', tag_content):
            tag_content = re.sub(r'\bstyle="[^"]*"', f'style="{g_style}"', tag_content)
        else:
            tag_content = re.sub(r'<!--\s*(pixel-kit|readme-kit):([a-zA-Z0-9_\-]+)', rf'<!-- \1:\2 style="{g_style}"', tag_content)

        # 1.1 Update theme if provided
        if g_theme:
            if re.search(r'\btheme="[^"]*"', tag_content):
                tag_content = re.sub(r'\btheme="[^"]*"', f'theme="{g_theme}"', tag_content)
            else:
                tag_content = re.sub(r'(style="[^"]*")', rf'\1 theme="{g_theme}"', tag_content)

        # 2. Preset and Colors
        if g_preset == "custom":
            tag_content = re.sub(r'\s*\bpreset="[^"]*"', '', tag_content)
            if g_prim:
                if re.search(r'\bprimary="[^"]*"', tag_content):
                    tag_content = re.sub(r'\bprimary="[^"]*"', f'primary="{g_prim}"', tag_content)
                else:
                    tag_content = re.sub(r'(style="[^"]*")', rf'\1 primary="{g_prim}"', tag_content)

            if is_force:
                if g_acc:
                    if re.search(r'\baccent="[^"]*"', tag_content):
                        tag_content = re.sub(r'\baccent="[^"]*"', f'accent="{g_acc}"', tag_content)
                    else:
                        tag_content = re.sub(r'(style="[^"]*")', rf'\1 accent="{g_acc}"', tag_content)
                else:
                    tag_content = re.sub(r'\s*\baccent="[^"]*"', '', tag_content)
                tag_content = re.sub(r'\s*\bbadge_color="[^"]*"', '', tag_content)
            else:
                if not re.search(r'\baccent="[^"]*"', tag_content) and g_acc:
                    tag_content = re.sub(r'(style="[^"]*")', rf'\1 accent="{g_acc}"', tag_content)

            if is_force:
                if g_tert:
                    if re.search(r'\btertiary="[^"]*"', tag_content):
                        tag_content = re.sub(r'\btertiary="[^"]*"', f'tertiary="{g_tert}"', tag_content)
                    else:
                        tag_content = re.sub(r'(style="[^"]*")', rf'\1 tertiary="{g_tert}"', tag_content)
                else:
                    tag_content = re.sub(r'\s*\btertiary="[^"]*"', '', tag_content)
            else:
                if not re.search(r'\btertiary="[^"]*"', tag_content) and g_tert:
                    tag_content = re.sub(r'(style="[^"]*")', rf'\1 tertiary="{g_tert}"', tag_content)
        else:
            if re.search(r'\bpreset="[^"]*"', tag_content):
                tag_content = re.sub(r'\bpreset="[^"]*"', f'preset="{g_preset}"', tag_content)
            else:
                tag_content = re.sub(r'(style="[^"]*")', rf'\1 preset="{g_preset}"', tag_content)

            tag_content = re.sub(r'\s*\bprimary="[^"]*"', '', tag_content)
            if is_force:
                tag_content = re.sub(r'\s*\baccent="[^"]*"', '', tag_content)
                tag_content = re.sub(r'\s*\btertiary="[^"]*"', '', tag_content)
                tag_content = re.sub(r'\s*\bbadge_color="[^"]*"', '', tag_content)

        # 3. Update mode if not auto
        if g_mode and g_mode != "auto":
            if re.search(r'\bmode="[^"]*"', tag_content):
                tag_content = re.sub(r'\bmode="[^"]*"', f'mode="{g_mode}"', tag_content)
            else:
                tag_content = re.sub(r'(style="[^"]*")', rf'\1 mode="{g_mode}"', tag_content)
        else:
            tag_content = re.sub(r'\s*\bmode="[^"]*"', '', tag_content)

        return tag_content

    return re.sub(r'<!--\s*(?:pixel-kit|readme-kit):([a-zA-Z0-9_\-]+)\b[\s\S]*?-->', update_dir, content)


def render_preview_html(template_file: str, assets_dir: str, preview_theme: str = "auto", view_mode: bool = False) -> str:
    """Compiles template and formats markdown into HTML for browser preview."""
    if not os.path.exists(template_file):
        return f"<div style='padding:20px;color:#f85149;'>Template file not found: <code>{template_file}</code></div>"

    try:
        with open(template_file, "r", encoding="utf-8") as f:
            raw_template = f.read()

        blocks = extract_template_blocks(raw_template)
        if not blocks or view_mode:
            compiler = MarkdownCompiler(assets_dir=assets_dir, use_cache=False, bust_cache=True)
            compiled_md = compiler.compile_string(raw_template)
            html = markdown_to_html(compiled_md)
            if preview_theme in ("light", "dark"):
                html = re.sub(
                    r'(<img\b[^>]*?\bsrc=")([^"]+)(\")',
                    lambda m: f'{m.group(1)}{m.group(2).split("?")[0]}?theme={preview_theme}&t={int(time.time()*1000)}{m.group(3)}',
                    html
                )
            return html

        wrapped_template = raw_template
        for b in reversed(blocks):
            b_id = b["id"]
            b_type = b["type"]
            start = b["start"]
            end = b["end"]
            wrapped_template = (
                wrapped_template[:start]
                + f"<!-- PK_BLOCK_START:{b_id}:{b_type} -->\n"
                + wrapped_template[start:end]
                + f"\n<!-- PK_BLOCK_END:{b_id}:{b_type} -->"
                + wrapped_template[end:]
            )

        compiler = MarkdownCompiler(assets_dir=assets_dir, use_cache=False, bust_cache=True)
        compiled_md = compiler.compile_string(wrapped_template)
        html = markdown_to_html(compiled_md)

        def start_repl(m):
            blk_id = int(m.group(1))
            blk_type = m.group(2).upper()
            top_divider = ""
            if blk_id == 0:
                top_divider = '<div class="pk-insert-divider" data-after-id="-1" ondragover="onDividerDragOver(event)" ondragleave="onDividerDragLeave(event)" ondrop="onDividerDrop(event, -1)"><button class="pk-insert-btn" onclick="openInsertAt(-1, event)">+ Add block at top</button></div>'
            return f"""{top_divider}
<div class="pk-block-wrapper" id="pk-block-{blk_id}" data-pk-id="{blk_id}" data-pk-type="{blk_type.lower()}" onclick="selectBlockFromPreview({blk_id}, event)">
  <div class="pk-block-hud-bar">
    <div class="pk-hud-badge"><span class="pk-hud-dot">●</span> {blk_type} <span class="pk-hud-num">#{blk_id}</span></div>
    <div class="pk-hud-actions">
      <button class="pk-hud-btn edit-btn" onclick="selectBlockFromPreview({blk_id}, event)">EDIT</button>
      <button class="pk-hud-btn del-btn" onclick="confirmDeleteBlock({blk_id}, event)">DEL</button>
    </div>
  </div>
  <div class="pk-block-content">"""

        def end_repl(m):
            blk_id = int(m.group(1))
            return f"""  </div>
</div>
<div class="pk-insert-divider" data-after-id="{blk_id}" ondragover="onDividerDragOver(event)" ondragleave="onDividerDragLeave(event)" ondrop="onDividerDrop(event, {blk_id})"><button class="pk-insert-btn" onclick="openInsertAt({blk_id}, event)">+ Add block here</button></div>"""

        html = re.sub(r'<!--\s*PK_BLOCK_START:(\d+):(\w+)\s*-->', start_repl, html)
        html = re.sub(r'<!--\s*PK_BLOCK_END:(\d+):(\w+)\s*-->', end_repl, html)

        if preview_theme in ("light", "dark"):
            html = re.sub(
                r'(<img\b[^>]*?\bsrc=")([^"]+)(\")',
                lambda m: f'{m.group(1)}{m.group(2).split("?")[0]}?theme={preview_theme}&t={int(time.time()*1000)}{m.group(3)}',
                html
            )

        return html
    except Exception as e:
        return f"<div style='padding:20px;color:#f85149;'>Compilation Error: {e}</div>"


def markdown_to_html(*args, **kwargs) -> str:
    """Converts GFM text to HTML with tables, task lists, and alert callouts."""
    if len(args) == 1:
        md = args[0]
    elif len(args) >= 2:
        md = args[1]
    else:
        md = kwargs.get("md", "")

    try:
        from markdown_it import MarkdownIt
        md_parser = MarkdownIt().enable('table').enable('strikethrough')
        html = md_parser.render(md)

        html = re.sub(r'<li>\s*\[ \]\s+', r'<li class="task-list-item"><input type="checkbox" disabled class="task-list-item-checkbox"> ', html)
        html = re.sub(r'<li>\s*\[[xX]\]\s+', r'<li class="task-list-item"><input type="checkbox" checked disabled class="task-list-item-checkbox"> ', html)

        def alert_repl(m):
            alert_type = m.group(1).upper()
            body = m.group(2).strip()
            icons = {
                "NOTE": '<svg class="octicon octicon-info" viewBox="0 0 16 16" width="16" height="16"><path d="M0 8a8 8 0 1 1 16 0A8 8 0 0 1 0 8Zm8-6.5a6.5 6.5 0 1 0 0 13 6.5 6.5 0 0 0 0-13ZM6.5 7.75A.75.75 0 0 1 7.25 7h1a.75.75 0 0 1 .75.75v2.75h.25a.75.75 0 0 1 0 1.5h-2a.75.75 0 0 1 0-1.5h.25v-2h-.25a.75.75 0 0 1-.75-.75ZM8 6a1 1 0 1 1 0-2 1 1 0 0 1 0 2Z"></path></svg>',
                "TIP": '<svg class="octicon octicon-light-bulb" viewBox="0 0 16 16" width="16" height="16"><path d="M8 1.5c-2.363 0-4 1.69-4 3.75 0 .984.424 1.625.984 2.304l.214.253c.223.264.47.556.673.848.284.411.537.896.621 1.49a.75.75 0 0 1-1.484.211c-.04-.282-.163-.547-.37-.847a8.456 8.456 0 0 0-.542-.68c-.084-.1-.173-.205-.268-.32C3.201 7.75 2.5 6.666 2.5 5.25 2.5 2.31 4.863 0 8 0s5.5 2.31 5.5 5.25c0 1.416-.701 2.5-1.328 3.25-.095.115-.184.22-.268.319-.18.213-.362.43-.542.68-.207.3-.33.565-.37.847a.751.751 0 0 1-1.485-.212c.084-.593.337-1.078.621-1.489.203-.292.45-.584.673-.848.075-.088.147-.173.213-.253.561-.679.985-1.32.985-2.304 0-2.06-1.637-3.75-4-3.75ZM5.75 12h4.5a.75.75 0 0 1 0 1.5h-4.5a.75.75 0 0 1 0-1.5ZM6.25 15h3.5a.75.75 0 0 1 0 1.5h-3.5a.75.75 0 0 1 0-1.5Z"></path></svg>',
                "IMPORTANT": '<svg class="octicon octicon-report" viewBox="0 0 16 16" width="16" height="16"><path d="M0 1.75C0 .784.784 0 1.75 0h12.5C15.216 0 16 .784 16 1.75v9.5A1.75 1.75 0 0 1 14.25 13H8.06l-2.573 2.573A1.458 1.458 0 0 1 3 14.543V13H1.75A1.75 1.75 0 0 1 0 11.25Zm1.75-.25a.25.25 0 0 0-.25.25v9.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h6.5a.25.25 0 0 0 .25-.25v-9.5a.25.25 0 0 0-.25-.25Zm7 2.25v2.5a.75.75 0 0 1-1.5 0v-2.5a.75.75 0 0 1 1.5 0ZM9 9a1 1 0 1 1-2 0 1 1 0 0 1 2 0Z"></path></svg>',
                "WARNING": '<svg class="octicon octicon-alert" viewBox="0 0 16 16" width="16" height="16"><path d="M6.457 1.047c.659-1.234 2.427-1.234 3.086 0l6.082 11.378A1.75 1.75 0 0 1 14.082 15H1.918a1.75 1.75 0 0 1-1.543-2.575Zm1.763.707a.25.25 0 0 0-.44 0L1.698 13.132a.25.25 0 0 0 .22.368h12.164a.25.25 0 0 0 .22-.368Zm.53 3.996v2.5a.75.75 0 0 1-1.5 0v-2.5a.75.75 0 0 1 1.5 0ZM9 11a1 1 0 1 1-2 0 1 1 0 0 1 2 0Z"></path></svg>',
                "CAUTION": '<svg class="octicon octicon-stop" viewBox="0 0 16 16" width="16" height="16"><path d="M4.47.047A1.75 1.75 0 0 1 5.707 0h4.586c.464 0 .909.184 1.237.513l3.957 3.957c.328.328.513.773.513 1.237v4.586c0 .464-.185.909-.513 1.237l-3.957 3.957c-.328.328-.773.513-1.237.513H5.707c-.464 0-.91-.185-1.238-.513L.512 11.53A1.75 1.75 0 0 1 0 10.293V5.707c0-.464.184-.91.513-1.238ZM1.5 5.707v4.586c0 .066.026.13.073.177l3.957 3.957c.047.047.111.073.177.073h4.586c.066 0 .13-.026.177-.073l3.957-3.957c.047-.047.073-.111.073-.177V5.707a.25.25 0 0 0-.073-.177L10.464 1.573a.25.25 0 0 0-.177-.073H5.707a.25.25 0 0 0-.177.073L1.573 5.53a.25.25 0 0 0-.073.177Zm7.25 4.543v1.5a.75.75 0 0 1-1.5 0v-1.5a.75.75 0 0 1 1.5 0ZM8 3.5a.75.75 0 0 1 .75.75v3.5a.75.75 0 0 1-1.5 0v-3.5A.75.75 0 0 1 8 3.5Z"></path></svg>',
            }
            icon_svg = icons.get(alert_type, icons["NOTE"])
            title_text = alert_type.capitalize()
            return f"""<div class="markdown-alert markdown-alert-{alert_type.lower()}">
  <p class="markdown-alert-title">{icon_svg} {title_text}</p>
  <div>{body}</div>
</div>"""

        html = re.sub(
            r'<blockquote>\s*<p>\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\](?:\s*<br\s*/?>)?\s*([\s\S]*?)</p>\s*</blockquote>',
            alert_repl,
            html,
            flags=re.IGNORECASE
        )
        return html
    except Exception:
        return _fallback_markdown_to_html(md)


def _format_inline_md(text: str) -> str:
    """Formats inline markdown elements like bold, italic, code, links, images, strikethrough."""
    text = re.sub(r'`([^`]+)`', r'<code class="gh-inline-code">\1</code>', text)
    text = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1" class="gh-img" />', text)
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2" class="gh-link">\1</a>', text)
    text = re.sub(r'~~(.+?)~~', r'<del>\1</del>', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)
    return text


def _fallback_markdown_to_html(md: str) -> str:
    """Fallback GFM-compatible markdown converter."""
    lines = md.split("\n")
    out = []
    in_code_block = False
    in_list = False
    in_blockquote = False
    in_table = False
    table_headers = []
    table_rows = []

    def flush_table():
        nonlocal in_table, table_headers, table_rows
        if not in_table:
            return
        t_html = ["<table>"]
        if table_headers:
            t_html.append("<thead><tr>")
            for h in table_headers:
                t_html.append(f"<th>{_format_inline_md(h.strip())}</th>")
            t_html.append("</tr></thead>")
        if table_rows:
            t_html.append("<tbody>")
            for r in table_rows:
                t_html.append("<tr>")
                for c in r:
                    t_html.append(f"<td>{_format_inline_md(c.strip())}</td>")
                t_html.append("</tr>")
            t_html.append("</tbody>")
        t_html.append("</table>")
        out.append("".join(t_html))
        in_table = False
        table_headers = []
        table_rows = []

    i = 0
    while i < len(lines):
        line = lines[i]
        trimmed = line.strip()

        if trimmed.startswith("|") and trimmed.endswith("|"):
            if in_list:
                out.append("</ul>")
                in_list = False
            if in_blockquote:
                out.append("</blockquote>")
                in_blockquote = False

            cells = [c for c in trimmed.split("|")[1:-1]]
            if not in_table:
                if i + 1 < len(lines) and re.match(r'^\s*\|(?:\s*:?-+:?\s*\|)+\s*$', lines[i+1].strip()):
                    in_table = True
                    table_headers = cells
                    table_rows = []
                    i += 2
                    continue
                else:
                    flush_table()
            else:
                table_rows.append(cells)
                i += 1
                continue
        else:
            flush_table()

        if trimmed.startswith("```"):
            if in_list:
                out.append("</ul>")
                in_list = False
            if in_blockquote:
                out.append("</blockquote>")
                in_blockquote = False
            if not in_code_block:
                in_code_block = True
                lang = trimmed[3:].strip()
                out.append(f"<pre class='gh-code-block' data-lang='{lang}'><code>")
            else:
                in_code_block = False
                out.append("</code></pre>")
            i += 1
            continue

        if in_code_block:
            escaped = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            out.append(escaped)
            i += 1
            continue

        if trimmed.startswith("<") or trimmed.startswith("<!--") or trimmed.endswith(">"):
            if in_list:
                out.append("</ul>")
                in_list = False
            if in_blockquote:
                out.append("</blockquote>")
                in_blockquote = False
            out.append(line)
            i += 1
            continue

        if not trimmed:
            if in_list:
                out.append("</ul>")
                in_list = False
            if in_blockquote:
                out.append("</blockquote>")
                in_blockquote = False
            out.append("")
            i += 1
            continue

        m_h = re.match(r'^(#{1,6})\s+(.*)$', line)
        if m_h:
            if in_list:
                out.append("</ul>")
                in_list = False
            if in_blockquote:
                out.append("</blockquote>")
                in_blockquote = False
            level = len(m_h.group(1))
            h_text = m_h.group(2)
            out.append(f"<h{level} class='gh-h{level}'>{h_text}</h{level}>")
            i += 1
            continue

        if trimmed in ("---", "***", "___"):
            if in_list:
                out.append("</ul>")
                in_list = False
            if in_blockquote:
                out.append("</blockquote>")
                in_blockquote = False
            out.append("<hr class='gh-hr'>")
            i += 1
            continue

        m_alert = re.match(r'^>\s*\[!(NOTE|TIP|IMPORTANT|WARNING|CAUTION)\]\s*$', line, re.IGNORECASE)
        if m_alert:
            if in_list:
                out.append("</ul>")
                in_list = False
            if in_blockquote:
                out.append("</blockquote>")
                in_blockquote = False
            alert_type = m_alert.group(1).upper()
            alert_body_lines = []
            i += 1
            while i < len(lines) and lines[i].startswith(">"):
                alert_body_lines.append(lines[i].lstrip("> ").strip())
                i += 1
            body_html = "<br>".join([_format_inline_md(l) for l in alert_body_lines if l])
            out.append(f"""<div class="markdown-alert markdown-alert-{alert_type.lower()}"><p class="markdown-alert-title">{alert_type.capitalize()}</p><div>{body_html}</div></div>""")
            continue

        if trimmed.startswith(">"):
            if in_list:
                out.append("</ul>")
                in_list = False
            if not in_blockquote:
                in_blockquote = True
                out.append("<blockquote>")
            out.append(f"<p>{_format_inline_md(trimmed[1:].strip())}</p>")
            i += 1
            continue
        elif in_blockquote:
            out.append("</blockquote>")
            in_blockquote = False

        if trimmed.startswith(("- ", "* ", "+ ")):
            if not in_list:
                in_list = True
                out.append("<ul class='gh-ul'>")
            item_text = trimmed[2:]
            if item_text.startswith("[ ] "):
                out.append(f"<li class='task-list-item'><input type='checkbox' disabled class='task-list-item-checkbox'> {_format_inline_md(item_text[4:])}</li>")
            elif item_text.startswith(("[x] ", "[X] ")):
                out.append(f"<li class='task-list-item'><input type='checkbox' checked disabled class='task-list-item-checkbox'> {_format_inline_md(item_text[4:])}</li>")
            else:
                out.append(f"<li>{_format_inline_md(item_text)}</li>")
            i += 1
            continue
        elif in_list:
            out.append("</ul>")
            in_list = False

        out.append(f"<p>{_format_inline_md(line)}</p>")
        i += 1

    flush_table()
    if in_list:
        out.append("</ul>")
    if in_blockquote:
        out.append("</blockquote>")

    return "\n".join(out)
