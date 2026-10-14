"""
HUD Studio HTTP Server for ReadmeKit v5.1.
Handles live browser preview, template editing API, theme creation, and asset compilation.
"""

import os
import sys
import json
import time
import re
import threading
import urllib.parse
from http.server import SimpleHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

from generator.compiler import MarkdownCompiler
from generator.studio.handlers import (
    handle_render_request,
    handle_github_fetch,
    extract_template_blocks,
    apply_global_theme_to_content,
    render_preview_html,
    markdown_to_html,
    handle_presets_list,
    handle_themes_list,
    handle_theme_generate,
    handle_theme_save,
    handle_git_push,
)

STUDIO_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(STUDIO_DIR, "..", ".."))
STATIC_DIR = os.path.join(STUDIO_DIR, "static")

def is_protected_template(path: str) -> bool:
    """Checks whether the template path points to canonical starter templates inside generator/templates."""
    if not path:
        return False
    full = os.path.abspath(os.path.join(PROJECT_ROOT, path)) if not os.path.isabs(path) else os.path.abspath(path)
    tpl_dir = os.path.abspath(os.path.join(PROJECT_ROOT, "generator", "templates"))
    return full == tpl_dir or full.startswith(tpl_dir + os.sep)

# Load STUDIO_HTML from static/index.html (inlining CSS and JS for 100% standalone reliability)
def _load_studio_html() -> str:
    html_path = os.path.join(STATIC_DIR, "index.html")
    css_path = os.path.join(STATIC_DIR, "css", "studio.css")
    js_path = os.path.join(STATIC_DIR, "js", "app.js")
    ts_js_path = os.path.join(STATIC_DIR, "js", "theme_studio.js")

    if os.path.isfile(html_path) and os.path.isfile(css_path) and os.path.isfile(js_path):
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()
        with open(css_path, "r", encoding="utf-8") as f:
            css = f.read()
        with open(js_path, "r", encoding="utf-8") as f:
            js = f.read()
        ts_js = ""
        if os.path.isfile(ts_js_path):
            with open(ts_js_path, "r", encoding="utf-8") as f:
                ts_js = f.read()

        # Inline stylesheet and script so the studio HTML is completely self-contained
        html = html.replace('<link rel="stylesheet" href="/static/css/studio.css">', f"<style>\n{css}\n</style>")
        html = html.replace('<script src="/static/js/app.js"></script>', f"<script>\n{js}\n</script>")
        if ts_js:
            html = html.replace('<script src="/static/js/theme_studio.js"></script>', f"<script>\n{ts_js}\n</script>")
        return html
    return "<html><body>HUD Studio static assets not found</body></html>"

STUDIO_HTML = _load_studio_html()


def _extract_media_block(css_or_svg: str, media_pattern: str):
    """
    Finds a media block matching media_pattern, returns (inner_content, text_without_media_block).
    Uses brace-depth counting to handle arbitrary nesting safely.
    """
    m = re.search(media_pattern, css_or_svg, re.IGNORECASE)
    if not m:
        return None, css_or_svg

    start_idx = css_or_svg.find('{', m.end())
    if start_idx == -1:
        return None, css_or_svg

    depth = 0
    end_idx = -1
    for i in range(start_idx, len(css_or_svg)):
        if css_or_svg[i] == '{':
            depth += 1
        elif css_or_svg[i] == '}':
            depth -= 1
            if depth == 0:
                end_idx = i + 1
                break

    if end_idx == -1:
        return None, css_or_svg

    inner_content = css_or_svg[start_idx + 1:end_idx - 1]
    new_text = css_or_svg[:m.start()] + css_or_svg[end_idx:]
    return inner_content, new_text


class StudioRequestHandler(SimpleHTTPRequestHandler):
    """Handles HUD Studio API, static asset requests, and interactive editing."""

    template_file = "README.template.md"
    output_file = "README.md"
    assets_dir = "assets/generated"
    is_starter = False
    subscribers = set()
    subscribers_lock = threading.Lock()
    _known_mtimes = {}
    _mtime_lock = threading.Lock()

    @classmethod
    def record_mtime(cls, file_path: str):
        """Records file mtime into _known_mtimes under lock to prevent redundant watcher compiles."""
        if not file_path:
            return
        abs_p = os.path.abspath(file_path)
        if os.path.exists(abs_p):
            try:
                mt = os.path.getmtime(abs_p)
                with cls._mtime_lock:
                    cls._known_mtimes[abs_p] = mt
            except OSError:
                pass

    def end_headers(self):
        """Ensure no browser or proxy caching for any studio assets or endpoints."""
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def do_GET(self):
        url = urllib.parse.urlparse(self.path)
        path = url.path
        query = urllib.parse.parse_qs(url.query)

        # 1. Main Studio UI
        if path == "/" or path == "/studio":
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(_load_studio_html().encode("utf-8"))
            return

        # 2. Static Assets Serving (/static/*)
        if path.startswith("/static/"):
            rel_path = path[len("/static/"):].lstrip("/")
            file_path = os.path.abspath(os.path.join(STATIC_DIR, rel_path))
            if not file_path.startswith(os.path.abspath(STATIC_DIR)):
                self.send_error(403, "Access denied")
                return
            if os.path.isfile(file_path):
                content_type = "text/plain"
                if file_path.endswith(".css"):
                    content_type = "text/css; charset=utf-8"
                elif file_path.endswith(".js"):
                    content_type = "application/javascript; charset=utf-8"
                elif file_path.endswith(".html"):
                    content_type = "text/html; charset=utf-8"
                with open(file_path, "rb") as f:
                    data = f.read()
                self.send_response(200)
                self.send_header("Content-Type", content_type)
                self.end_headers()
                self.wfile.write(data)
                return

        # 3. Server-Sent Events (SSE) Live Reload channel
        if path == "/events":
            self.send_response(200)
            self.send_header("Content-Type", "text/event-stream")
            self.send_header("Connection", "keep-alive")
            self.end_headers()

            with self.subscribers_lock:
                self.subscribers.add(self)

            try:
                self.wfile.write(b"data: {\"status\": \"connected\"}\n\n")
                self.wfile.flush()
                while True:
                    time.sleep(1.0)
                    self.wfile.write(b": keepalive\n\n")
                    self.wfile.flush()
            except (ConnectionError, BrokenPipeError, ConnectionResetError, ConnectionAbortedError, OSError):
                pass
            finally:
                with self.subscribers_lock:
                    self.subscribers.discard(self)
            return

        # 4. Dynamic SVG Render API (/api/render)
        if path == "/api/render":
            handle_render_request(self, query)
            return

        # 4.5 GitHub Live Data Fetch API (/api/github/fetch)
        if path == "/api/github/fetch":
            handle_github_fetch(self, query)
            return

        # 5. Preview Compiled Content (/api/preview)
        if path == "/api/preview":
            req_theme = query.get("theme", ["dark"])[0]
            edit_html = self.render_template_to_preview_html(preview_theme=req_theme, view_mode=False)
            view_html = self.render_template_to_preview_html(preview_theme=req_theme, view_mode=True)
            line_count = 0
            byte_size = 0
            if os.path.exists(self.template_file):
                try:
                    with open(self.template_file, "r", encoding="utf-8") as f:
                        f_data = f.read()
                        line_count = len(f_data.splitlines())
                        byte_size = len(f_data.encode("utf-8"))
                except Exception:
                    pass
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            resp = {
                "status": "success",
                "filename": self.template_file,
                "lines": line_count,
                "bytes": byte_size,
                "html": edit_html,
                "view_html": view_html
            }
            self.wfile.write(json.dumps(resp).encode("utf-8"))
            return

        # 6. List Presets and Icons (/api/presets)
        if path == "/api/presets":
            handle_presets_list(self)
            return

        # 7. List Detailed Themes (/api/themes)
        if path == "/api/themes":
            handle_themes_list(self)
            return

        # 8. Extract Blocks from Template (/api/template/blocks)
        if path == "/api/template/blocks":
            if not os.path.exists(self.template_file):
                self.send_error(404, "Template file not found")
                return
            with open(self.template_file, "r", encoding="utf-8") as f:
                content = f.read()
            blocks = extract_template_blocks(content)
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            resp = {
                "status": "success",
                "filename": self.template_file,
                "count": len(blocks),
                "blocks": blocks
            }
            self.wfile.write(json.dumps(resp).encode("utf-8"))
            return

        # 8.5 List Available Templates and Readmes (/api/templates)
        if path == "/api/templates":
            items = []
            seen = set()

            # Scan root workspace directory
            root_dir = PROJECT_ROOT if os.path.exists(PROJECT_ROOT) else "."
            for f in sorted(os.listdir(root_dir)):
                if f.endswith(".template.md"):
                    items.append({"name": f, "path": f, "is_template": True, "is_starter": False})
                    seen.add(f)
                elif f.endswith(".md") and not f.endswith(".template.md") and f in ("README.md", "CATALOG.md", "EXAMPLES.md"):
                    items.append({"name": f, "path": f, "is_template": False, "is_starter": False})
                    seen.add(f)

            # Check generator/templates for starter templates
            gen_tpl_dir = os.path.join(PROJECT_ROOT, "generator", "templates")
            if os.path.isdir(gen_tpl_dir):
                for root, _, files in os.walk(gen_tpl_dir):
                    for f in sorted(files):
                        if f.endswith(".template.md"):
                            rel_p = os.path.relpath(os.path.join(root, f), PROJECT_ROOT).replace("\\", "/")
                            if rel_p not in seen:
                                items.append({"name": rel_p, "path": rel_p, "is_template": True, "is_starter": True})
                                seen.add(rel_p)

            cur = getattr(self, "template_file", "README.template.md")
            for item in items:
                item["is_active"] = (item["path"] == cur)
            resp = {
                "status": "success",
                "current": cur,
                "is_starter": is_protected_template(cur),
                "templates": items
            }
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(resp).encode("utf-8"))
            return

        # 9. Static SVG File Serving with Theme Adaptability
        if path.lower().endswith(".svg"):
            local_path = path.lstrip("/")
            if not os.path.exists(local_path) and hasattr(self, "assets_dir") and self.assets_dir:
                candidate = os.path.join(self.assets_dir, os.path.basename(path))
                if os.path.exists(candidate):
                    local_path = candidate

            local_full = os.path.abspath(local_path)
            if not local_full.startswith(PROJECT_ROOT):
                self.send_error(403, "Access denied")
                return

            if os.path.exists(local_full) and os.path.isfile(local_full):
                try:
                    with open(local_full, "r", encoding="utf-8", errors="replace") as f:
                        svg_data = f.read()
                    req_theme = query.get("theme", [None])[0]
                    if req_theme == "light":
                        _, svg_data = _extract_media_block(svg_data, r'@media\s*\(\s*prefers-color-scheme\s*:\s*dark\s*\)')
                    elif req_theme == "dark":
                        dark_content, svg_data_no_dark = _extract_media_block(svg_data, r'@media\s*\(\s*prefers-color-scheme\s*:\s*dark\s*\)')
                        if dark_content:
                            m_dark = re.search(r':root\s*\{([\s\S]*?)\}', dark_content)
                            if m_dark:
                                dark_vars = m_dark.group(1)
                                svg_data = re.sub(r':root\s*\{[\s\S]*?\}', f':root {{{dark_vars}}}', svg_data_no_dark, count=1)
                            else:
                                svg_data = svg_data_no_dark

                    self.send_response(200)
                    self.send_header("Content-Type", "image/svg+xml; charset=utf-8")
                    self.end_headers()
                    self.wfile.write(svg_data.encode("utf-8"))
                    return
                except Exception:
                    pass

        # 10. Restricted static file serving fallback (assets/ and docs/ directories only)
        safe_exts = {
            ".svg": "image/svg+xml; charset=utf-8",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".gif": "image/gif",
            ".webp": "image/webp",
            ".ico": "image/x-icon",
            ".html": "text/html; charset=utf-8",
            ".css": "text/css; charset=utf-8",
            ".js": "application/javascript; charset=utf-8",
            ".json": "application/json; charset=utf-8",
            ".md": "text/markdown; charset=utf-8",
        }
        clean_rel = path.lstrip("/\\").replace("\\", "/")
        allowed_dirs = ("assets/", "docs/")
        if any(clean_rel.startswith(pfx) for pfx in allowed_dirs):
            target_path = os.path.abspath(os.path.join(PROJECT_ROOT, clean_rel))
            if target_path.startswith(PROJECT_ROOT) and os.path.isfile(target_path):
                ext = os.path.splitext(target_path)[1].lower()
                if ext in safe_exts:
                    try:
                        with open(target_path, "rb") as f:
                            data = f.read()
                        self.send_response(200)
                        self.send_header("Content-Type", safe_exts[ext])
                        self.send_header("Content-Length", str(len(data)))
                        self.end_headers()
                        self.wfile.write(data)
                        return
                    except Exception:
                        pass

        self.send_error(404, "File not found")

    def do_POST(self):
        url = urllib.parse.urlparse(self.path)
        path = url.path

        if path == "/api/recompile":
            self.trigger_compile()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b"{\"status\": \"recompiled\"}")
            return

        if path == "/api/template/apply_global_theme":
            if is_protected_template(self.template_file):
                self.send_error(403, "Starter templates in generator/templates/ are read-only. Copy to project root to edit.")
                return
            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
            try:
                req = json.loads(raw_body)
            except (json.JSONDecodeError, ValueError) as e:
                self.send_error(400, f"Invalid JSON payload: {e}")
                return
            try:
                if not os.path.exists(self.template_file):
                    self.send_error(404, "Template file not found")
                    return
                with open(self.template_file, "r", encoding="utf-8") as f:
                    content = f.read()

                updated_content = apply_global_theme_to_content(content, req)
                with open(self.template_file, "w", encoding="utf-8") as f:
                    f.write(updated_content)

                self.record_mtime(self.template_file)
                self.trigger_compile()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(b"{\"status\": \"applied\"}")
                return
            except Exception as e:
                self.send_error(500, f"Apply global theme error: {e}")
                return

        if path == "/api/insert":
            if is_protected_template(self.template_file):
                self.send_error(403, "Starter templates in generator/templates/ are read-only. Copy to project root to edit.")
                return
            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
            try:
                req = json.loads(raw_body)
            except (json.JSONDecodeError, ValueError) as e:
                self.send_error(400, f"Invalid JSON payload: {e}")
                return
            try:
                directive = req.get("directive", "")
                if os.path.exists(self.template_file):
                    with open(self.template_file, "a", encoding="utf-8") as f:
                        f.write(f"\n{directive}\n")
                    self.record_mtime(self.template_file)
                    self.trigger_compile()
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(b"{\"status\": \"inserted\"}")
                    return
                else:
                    self.send_error(404, "Template file not found")
                    return
            except Exception as e:
                self.send_error(500, f"Insert error: {e}")
                return

        if path == "/api/template/update_block":
            if is_protected_template(self.template_file):
                self.send_error(403, "Starter templates in generator/templates/ are read-only. Copy to project root to edit.")
                return
            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
            try:
                req = json.loads(raw_body)
            except (json.JSONDecodeError, ValueError) as e:
                self.send_error(400, f"Invalid JSON payload: {e}")
                return
            try:
                blk_id = int(req.get("id", -1))
                new_raw = req.get("directive_raw", "")
                if not os.path.exists(self.template_file):
                    self.send_error(404, "Template file not found")
                    return
                with open(self.template_file, "r", encoding="utf-8") as f:
                    content = f.read()
                blocks = extract_template_blocks(content)
                if blk_id < 0 or blk_id >= len(blocks):
                    self.send_error(400, f"Invalid block index: {blk_id}")
                    return
                target = blocks[blk_id]
                new_content = content[:target["start"]] + new_raw + content[target["end"]:]
                with open(self.template_file, "w", encoding="utf-8") as f:
                    f.write(new_content)
                self.record_mtime(self.template_file)
                self.trigger_compile()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "updated", "id": blk_id}).encode("utf-8"))
                return
            except Exception as e:
                self.send_error(500, f"Update block error: {e}")
                return

        if path == "/api/template/delete_block":
            if is_protected_template(self.template_file):
                self.send_error(403, "Starter templates in generator/templates/ are read-only. Copy to project root to edit.")
                return
            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
            try:
                req = json.loads(raw_body)
            except (json.JSONDecodeError, ValueError) as e:
                self.send_error(400, f"Invalid JSON payload: {e}")
                return
            try:
                blk_id = int(req.get("id", -1))
                if not os.path.exists(self.template_file):
                    self.send_error(404, "Template file not found")
                    return
                with open(self.template_file, "r", encoding="utf-8") as f:
                    content = f.read()
                blocks = extract_template_blocks(content)
                if blk_id < 0 or blk_id >= len(blocks):
                    self.send_error(400, f"Invalid block index: {blk_id}")
                    return
                target = blocks[blk_id]
                start = target["start"]
                end = target["end"]
                if start > 0 and content[start-1] == '\n':
                    start -= 1
                new_content = content[:start] + content[end:]
                with open(self.template_file, "w", encoding="utf-8") as f:
                    f.write(new_content)
                self.record_mtime(self.template_file)
                self.trigger_compile()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "deleted"}).encode("utf-8"))
                return
            except Exception as e:
                self.send_error(500, f"Delete block error: {e}")
                return

        if path == "/api/template/insert_block":
            if is_protected_template(self.template_file):
                self.send_error(403, "Starter templates in generator/templates/ are read-only. Copy to project root to edit.")
                return
            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
            try:
                req = json.loads(raw_body)
            except (json.JSONDecodeError, ValueError) as e:
                self.send_error(400, f"Invalid JSON payload: {e}")
                return
            try:
                after_id = int(req.get("after_id", -1))
                directive_raw = req.get("directive_raw", "").strip()
                if not directive_raw:
                    self.send_error(400, "Empty directive_raw")
                    return
                if not os.path.exists(self.template_file):
                    self.send_error(404, "Template file not found")
                    return
                with open(self.template_file, "r", encoding="utf-8") as f:
                    content = f.read()

                blocks = extract_template_blocks(content)
                if after_id == -1 or not blocks:
                    new_content = f"{directive_raw}\n\n" + content
                elif 0 <= after_id < len(blocks):
                    target = blocks[after_id]
                    ins_pos = target["end"]
                    new_content = content[:ins_pos] + f"\n\n{directive_raw}\n" + content[ins_pos:]
                else:
                    new_content = content.rstrip() + f"\n\n{directive_raw}\n"

                with open(self.template_file, "w", encoding="utf-8") as f:
                    f.write(new_content)
                self.record_mtime(self.template_file)
                self.trigger_compile()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "inserted"}).encode("utf-8"))
                return
            except Exception as e:
                self.send_error(500, f"Insert block error: {e}")
                return

        # New Theme API routes
        if path == "/api/themes/generate":
            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
            try:
                body = json.loads(raw_body)
            except (json.JSONDecodeError, ValueError) as e:
                self.send_error(400, f"Invalid JSON payload: {e}")
                return
            handle_theme_generate(self, body)
            return

        if path == "/api/themes/save":
            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
            try:
                body = json.loads(raw_body)
            except (json.JSONDecodeError, ValueError) as e:
                self.send_error(400, f"Invalid JSON payload: {e}")
                return
            handle_theme_save(self, body)
            return

        if path == "/api/template/switch":
            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
            try:
                req = json.loads(raw_body)
            except (json.JSONDecodeError, ValueError) as e:
                self.send_error(400, f"Invalid JSON payload: {e}")
                return
            try:
                target_path = (req.get("path") or req.get("file") or "").strip()
                if not target_path:
                    self.send_error(400, "Missing path in request")
                    return
                # Normalize relative to workspace root if needed
                full_path = os.path.abspath(os.path.join(PROJECT_ROOT, target_path)) if not os.path.isabs(target_path) else os.path.abspath(target_path)
                if not full_path.startswith(PROJECT_ROOT):
                    self.send_error(403, "Access denied: outside project root")
                    return
                if not full_path.endswith(".md"):
                    self.send_error(400, "Invalid file type: must be a markdown file")
                    return
                if not os.path.exists(full_path):
                    self.send_error(404, f"File not found: {target_path}")
                    return

                rel_target = os.path.relpath(full_path, PROJECT_ROOT).replace("\\", "/")
                StudioRequestHandler.template_file = rel_target
                is_starter = is_protected_template(rel_target)
                StudioRequestHandler.is_starter = is_starter

                if is_starter:
                    # NEVER compile or write .md into generator/templates/!
                    preview_out = os.path.join(self.assets_dir, ".studio_preview.md")
                    StudioRequestHandler.output_file = preview_out
                elif rel_target.endswith(".template.md"):
                    StudioRequestHandler.output_file = rel_target[:-len(".template.md")] + ".md"
                elif rel_target.endswith(".md"):
                    StudioRequestHandler.output_file = rel_target

                # Trigger compile if template
                if (rel_target.endswith(".template.md")
                        and os.path.exists(StudioRequestHandler.template_file)
                        and StudioRequestHandler.template_file != StudioRequestHandler.output_file):
                    compiler = MarkdownCompiler(assets_dir=self.assets_dir, use_cache=True)
                    compiler.compile_file(StudioRequestHandler.template_file, StudioRequestHandler.output_file)
                    StudioRequestHandler.record_mtime(StudioRequestHandler.template_file)
                    StudioRequestHandler.record_mtime(StudioRequestHandler.output_file)

                # Broadcast reload to all connected clients
                self.trigger_compile()

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "switched",
                    "template": StudioRequestHandler.template_file,
                    "output": StudioRequestHandler.output_file,
                    "is_starter": is_starter
                }).encode("utf-8"))
                return
            except Exception as e:
                self.send_error(500, f"Switch template error: {e}")
                return

        if path == "/api/template/clone":
            content_length = int(self.headers.get("Content-Length", 0))
            raw_body = self.rfile.read(content_length).decode("utf-8") if content_length > 0 else "{}"
            try:
                req = json.loads(raw_body)
            except (json.JSONDecodeError, ValueError) as e:
                self.send_error(400, f"Invalid JSON payload: {e}")
                return
            try:
                src_path = (req.get("src") or req.get("source") or self.template_file or "").strip()
                dest_name = (req.get("dest") or req.get("target") or os.path.basename(src_path)).strip()
                if not dest_name.endswith(".template.md") and not dest_name.endswith(".md"):
                    dest_name += ".template.md"
                dest_full = os.path.abspath(os.path.join(PROJECT_ROOT, dest_name))
                if not dest_full.startswith(PROJECT_ROOT) or is_protected_template(dest_full):
                    self.send_error(403, "Access denied: destination cannot be in package templates")
                    return
                src_full = os.path.abspath(os.path.join(PROJECT_ROOT, src_path)) if not os.path.isabs(src_path) else os.path.abspath(src_path)
                if not os.path.exists(src_full):
                    self.send_error(404, f"Source template not found: {src_path}")
                    return
                import shutil
                shutil.copyfile(src_full, dest_full)
                rel_dest = os.path.relpath(dest_full, PROJECT_ROOT).replace("\\", "/")
                StudioRequestHandler.template_file = rel_dest
                StudioRequestHandler.is_starter = False
                if rel_dest.endswith(".template.md"):
                    StudioRequestHandler.output_file = rel_dest[:-len(".template.md")] + ".md"
                else:
                    StudioRequestHandler.output_file = rel_dest

                compiler = MarkdownCompiler(assets_dir=self.assets_dir, use_cache=True)
                compiler.compile_file(StudioRequestHandler.template_file, StudioRequestHandler.output_file)
                StudioRequestHandler.record_mtime(StudioRequestHandler.template_file)
                StudioRequestHandler.record_mtime(StudioRequestHandler.output_file)
                self.trigger_compile()

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "status": "cloned",
                    "template": StudioRequestHandler.template_file,
                    "output": StudioRequestHandler.output_file
                }).encode("utf-8"))
                return
            except Exception as e:
                self.send_error(500, f"Clone template error: {e}")
                return

        if path == "/api/git/push_readme":
            handle_git_push(self)
            return

        self.send_error(404, "Endpoint not found")

    def render_template_to_preview_html(self, preview_theme: str = "auto", view_mode: bool = False) -> str:
        """Compiles template and formats markdown into HTML for browser preview."""
        return render_preview_html(self.template_file, self.assets_dir, preview_theme, view_mode)

    @classmethod
    def markdown_to_html(cls, *args, **kwargs) -> str:
        """Converts Markdown text to HTML using GFM renderer."""
        return markdown_to_html(*args, **kwargs)

    @classmethod
    def _fallback_markdown_to_html(cls, md: str) -> str:
        from generator.studio.handlers.template_handler import _fallback_markdown_to_html
        return _fallback_markdown_to_html(md)

    @classmethod
    def _format_inline_md(cls, text: str) -> str:
        from generator.studio.handlers.template_handler import _format_inline_md
        return _format_inline_md(text)

    @classmethod
    def trigger_compile(cls):
        """Forces compilation and notifies all SSE clients."""
        # Only compile to disk if it is a template file and template != output to prevent circular rewrite loops
        if (os.path.exists(cls.template_file)
                and cls.template_file.endswith(".template.md")
                and cls.template_file != cls.output_file):
            try:
                compiler = MarkdownCompiler(assets_dir=cls.assets_dir, use_cache=False, bust_cache=True)
                compiler.compile_file(cls.template_file, cls.output_file)
                cls.record_mtime(cls.template_file)
                cls.record_mtime(cls.output_file)
            except Exception as e:
                print(f"[Studio] Compilation error: {e}", file=sys.stderr)

        with cls.subscribers_lock:
            dead = set()
            for s in cls.subscribers:
                try:
                    s.wfile.write(b"event: reload\ndata: {\"reloaded\": true}\n\n")
                    s.wfile.flush()
                except Exception:
                    dead.add(s)
            cls.subscribers.difference_update(dead)


class ThreadedStudioServer(ThreadingMixIn, HTTPServer):
    daemon_threads = True

    def handle_error(self, request, client_address):
        """Suppress noisy tracebacks for normal browser disconnects / tab reloads."""
        exc_type, exc_val, _ = sys.exc_info()
        if exc_type and issubclass(exc_type, (ConnectionError, ConnectionResetError, ConnectionAbortedError, BrokenPipeError)):
            return
        if exc_type and issubclass(exc_type, OSError) and getattr(exc_val, "winerror", None) in (10053, 10054):
            return
        super().handle_error(request, client_address)


def start_file_watcher(template_path: str, handler_class, poll_interval: float = 0.5):
    """Background thread watching active template file mtime to trigger auto-reloads safely."""
    def watcher_loop():
        last_tracked_path = None

        while True:
            time.sleep(poll_interval)
            active_path = getattr(handler_class, "template_file", template_path)
            if not os.path.exists(active_path):
                continue

            abs_active = os.path.abspath(active_path)
            try:
                mtime = os.path.getmtime(abs_active)
            except OSError:
                continue

            # If active template changed, initialize its mtime baseline without triggering reload
            if abs_active != last_tracked_path:
                last_tracked_path = abs_active
                with handler_class._mtime_lock:
                    handler_class._known_mtimes[abs_active] = mtime
                continue

            # Check if current active template was modified externally
            with handler_class._mtime_lock:
                prev_mtime = handler_class._known_mtimes.get(abs_active, 0)
                if mtime > prev_mtime:
                    handler_class._known_mtimes[abs_active] = mtime
                    is_new = True
                else:
                    is_new = False

            if is_new:
                handler_class.trigger_compile()

    t = threading.Thread(target=watcher_loop, daemon=True)
    t.start()
    return t


def run_studio_server(template_path="README.template.md", output_path="README.md",
                      assets_dir="assets/generated", port=3000, open_browser=False):
    """Starts the HUD Studio server and watches the template."""
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    StudioRequestHandler.template_file = template_path
    StudioRequestHandler.output_file = output_path
    StudioRequestHandler.assets_dir = assets_dir

    if os.path.exists(template_path):
        compiler = MarkdownCompiler(assets_dir=assets_dir, use_cache=True)
        compiler.compile_file(template_path, output_path)

    start_file_watcher(template_path, StudioRequestHandler)

    server = ThreadedStudioServer(("127.0.0.1", port), StudioRequestHandler)
    url = f"http://localhost:{port}/"
    print(f"[*] ╔═══════════════════════════════════════════════════════════╗")
    print(f"[*] ║        READMEKIT // HUD STUDIO LIVE PREVIEW v6.5          ║")
    print(f"[*] ╚═══════════════════════════════════════════════════════════╝")
    print(f"[*] ▶ Studio Web UI:     {url}")
    print(f"[*] ▶ Active Template:   {template_path}")
    print(f"[*] ▶ Output Target:     {output_path}")
    print(f"[*] ▶ Live Reload:       ENABLED (300ms SSE sync)")
    print(f"[*] Press Ctrl+C to terminate.")

    if open_browser:
        try:
            import webbrowser
            webbrowser.open(url)
        except Exception:
            pass

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Shutting down HUD Studio server...")
    finally:
        server.server_close()
