"""
Native MCP (Model Context Protocol) Server for ReadmeKit v5.1.
Provides structured tools for AI assistants (Claude, Cursor, Antigravity, Copilot)
to compile, render, validate, and scaffold retro-cyberpunk README layouts.

Supports both:
1. FastMCP if 'mcp' package is installed.
2. Zero-dependency native JSON-RPC 2.0 stdio protocol fallback.
"""

import os
import sys
import json
import traceback

# Add project root to sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from generator.compiler import MarkdownCompiler, parse_directive_attrs
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
    normalize_style_and_theme,
    validate_svg
)
from generator.scaffolder import scaffold_readme, get_available_templates

# ==============================================================================
# TOOL IMPLEMENTATIONS
# ==============================================================================

def tool_compile_readme(
    template_path: str = "README.template.md",
    output_path: str = "README.md",
    assets_dir: str = "assets/generated",
    clean_assets: bool = False,
    dry_run: bool = False,
    no_cache: bool = False,
    bust_cache: bool = False
) -> dict:
    """Compiles a template markdown with pixel-kit directives into GitHub-ready README.md."""
    if not os.path.exists(template_path):
        return {"status": "error", "message": f"Template file not found: {template_path}"}

    compiler = MarkdownCompiler(assets_dir=assets_dir, use_cache=not no_cache, bust_cache=bust_cache)
    compiler.compile_file(template_path, output_path, clean_assets=clean_assets, dry_run_clean=dry_run)

    return {
        "status": "success",
        "template": template_path,
        "output": output_path,
        "assets_dir": assets_dir,
        "stats": compiler.stats,
        "orphans": compiler.orphans if (clean_assets or dry_run) else []
    }

def tool_render_block(
    block_type="header",
    style: str = "cyberpunk",
    theme: str = None,
    mode: str = "auto",
    preset: str = None,
    primary: str = None,
    accent: str = None,
    title: str = None,
    subtitle: str = None,
    tag: str = None,
    frame_type: str = "top",
    chip_type: str = "closed",
    callout_type: str = "note",
    compact: bool = False,
    output_path: str = None,
    params: dict = None,
    **kwargs
) -> dict:
    """Generates an individual SVG block (header, footer, callout, frame, chip, divider, splitter, metrics, progress, techstack, timeline, social, starchart, profile)."""
    if isinstance(block_type, dict):
        d = dict(block_type)
        return tool_render_block(**d)

    btype = str(block_type).lower()
    p = params or {}
    is_compact = compact or kwargs.get("compact", False) or p.get("compact", False)

    req_style = style or p.get("style", "cyberpunk")
    req_theme = theme or p.get("theme")
    style, theme = normalize_style_and_theme(req_style, req_theme)

    try:
        if btype == "header":
            svg = generate_header(
                style=style, theme=theme, mode=mode, preset=preset, primary=primary, accent=accent,
                title=title or p.get("title") or "READMEKIT",
                subtitle=subtitle or p.get("subtitle") or "TRANSLUCENT HUD SYSTEM",
                tag=tag or p.get("tag") or "SYSTEM_ACTIVE",
                compact=is_compact
            )
        elif btype == "footer":
            svg = generate_footer(
                style=style, theme=theme, mode=mode, preset=preset, primary=primary, accent=accent,
                status=title or p.get("status") or "SESSION_ACTIVE // STANDBY",
                nav_text=tag or p.get("tag") or "RETURN TO TOP",
                sub_text=subtitle or p.get("sub_text")
            )
        elif btype == "callout":
            svg = generate_callout(
                style=style, theme=theme, mode=mode, preset=preset, primary=primary, accent=accent,
                callout_type=callout_type or p.get("callout_type", "note"),
                title=title or p.get("title") or "SYSTEM NOTICE",
                subtitle=subtitle or p.get("subtitle", ""),
                badge_color=p.get("badge_color")
            )
        elif btype == "frame":
            svg = generate_frame(
                style=style, theme=theme, mode=mode, preset=preset, primary=primary, accent=accent,
                frame_type=frame_type or p.get("frame_type", "top"),
                title=title or p.get("title") or "╔═ SYSTEM.CORE // RUNTIME.SYS",
                tag=tag or p.get("tag") or "[OPEN_HUD]"
            )
        elif btype == "chip":
            svg = generate_chip(
                style=style, theme=theme, mode=mode, preset=preset, primary=primary, accent=accent,
                chip_type=chip_type or p.get("chip_type", "closed"),
                text=title or p.get("text") or "CHIP"
            )
        elif btype == "divider":
            svg = generate_divider(
                style=style, theme=theme, mode=mode, preset=preset, primary=primary, accent=accent
            )
        elif btype == "splitter":
            svg = generate_splitter(
                style=style, theme=theme, mode=mode, preset=preset, primary=primary, accent=accent,
                label=title or p.get("label") or "[MODULE: SUB_SYSTEM]"
            )
        elif btype == "metrics":
            cards = p.get("metrics") or p.get("cards")
            if not cards:
                if "label" in p:
                    cards = [p]
                else:
                    cards = [{"label": title or "SYSTEM METRIC", "value": subtitle or "100%", "delta": tag}]
            svg = generate_metrics(
                metrics=cards,
                style=style, theme=theme, mode=mode, preset=preset, primary=primary, accent=accent
            )
        elif btype == "progress":
            val = p.get("value")
            if val is None:
                val = int(tag) if tag and tag.isdigit() else 75
            svg = generate_progress(
                value=val,
                label=title or p.get("label") or "PROGRESS",
                sub=subtitle or p.get("sub"),
                style=style, theme=theme, mode=mode, preset=preset, primary=primary, accent=accent
            )
        elif btype == "techstack":
            items = p.get("items") or (subtitle.split(",") if subtitle else ["python", "cpp", "docker", "git"])
            cols = p.get("columns", 5)
            svg = generate_techstack(
                items=items, columns=cols,
                style=style, theme=theme, mode=mode, preset=preset, primary=primary, accent=accent
            )
        elif btype == "timeline":
            items = p.get("milestones") or p.get("items") or []
            svg = generate_timeline(
                items=items,
                style=style, theme=theme, mode=mode, preset=preset, primary=primary, accent=accent
            )
        elif btype == "social":
            tags = p.get("tags") or kwargs.get("tags")
            if isinstance(tags, str):
                tags = [t.strip() for t in tags.split(",") if t.strip()]
            repo = p.get("repo") or kwargs.get("repo") or "Kazinagg/readme-kit"
            svg = generate_social(
                title=title or p.get("title") or kwargs.get("title") or "READMEKIT",
                subtitle=subtitle or p.get("subtitle") or kwargs.get("subtitle") or "RETRO-FUTURISTIC HUD & SCI-FI INFOGRAPHICS",
                repo=repo,
                tags=tags,
                style=style, theme=theme, mode=mode, preset=preset, primary=primary, accent=accent
            )
        elif btype in ("starchart", "star_chart", "chart"):
            points = p.get("points") or kwargs.get("points")
            current = p.get("current") or kwargs.get("current")
            delta = p.get("delta") or kwargs.get("delta")
            repo = p.get("repo") or kwargs.get("repo") or "Kazinagg/readme-kit"
            svg = generate_starchart(
                style=style, theme=theme, mode=mode, preset=preset, primary=primary, accent=accent,
                repo=repo, points=points, current=current, delta=delta
            )
        elif btype in ("profile", "profile_card"):
            svg = generate_profile_card(
                style=style, theme=theme, mode=mode, preset=preset, primary=primary, accent=accent,
                name=title or p.get("name") or "DEVELOPER",
                role=subtitle or p.get("role") or "SYSTEM ARCHITECT",
                bio=p.get("bio") or "Building high-performance runtimes and tooling.",
                status=tag or p.get("status") or "AVAILABLE FOR HIRE",
                location=p.get("location") or "REMOTE // UTC",
                badge=p.get("badge") or "LEVEL_99"
            )
        else:
            return {"status": "error", "success": False, "message": f"Unsupported block type: '{block_type}'"}

        validate_svg(svg)

        if output_path:
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(svg)
            return {"status": "success", "success": True, "block_type": btype, "saved_to": output_path, "length": len(svg)}

        return {"status": "success", "success": True, "block_type": btype, "svg": svg, "length": len(svg)}
    except Exception as e:
        return {"status": "error", "success": False, "message": str(e)}

def tool_validate_template(content: str = None, file_path: str = None) -> dict:
    """Validates directives syntax, character limits, and potential collisions in a markdown template."""
    text = content
    if file_path:
        if not os.path.exists(file_path):
            return {"status": "error", "message": f"File not found: {file_path}"}
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

    if not text:
        return {"status": "error", "message": "Neither content nor valid file_path was provided."}

    import re
    directives = []
    warnings = []

    pattern = re.compile(r'<!--\s*(/?)\s*(?:pixel-kit|readme-kit):([a-z_0-9-]+)\s*([\s\S]*?)\s*-->', re.IGNORECASE)
    paired_containers = ("window", "terminal", "quote", "timeline", "metrics")
    open_counts = {c: 0 for c in paired_containers}
    close_counts = {c: 0 for c in paired_containers}

    for m in pattern.finditer(text):
        is_close = bool(m.group(1))
        tag_name = m.group(2).lower().strip()
        attr_str = m.group(3).strip()

        if is_close:
            if tag_name in close_counts:
                close_counts[tag_name] += 1
            continue

        dtype = tag_name
        attrs = parse_directive_attrs(attr_str)
        directives.append({"type": dtype, "attrs": attrs})

        if dtype in open_counts:
            open_counts[dtype] += 1

        # Safe budget inspections
        if dtype == "header":
            t = attrs.get("title", "")
            sub = attrs.get("subtitle", "")
            if len(t) > 32:
                warnings.append(f"Header title '{t}' has {len(t)} chars. Recommended <= 32 (truncation risk).")
            elif len(t) > 16:
                warnings.append(f"Header title '{t}' has {len(t)} chars. Will automatically downscale font size.")
            if len(sub) > 60:
                warnings.append(f"Header subtitle exceeds 60 chars ({len(sub)} chars). May overlap visual boundaries.")
        elif dtype == "window":
            t = attrs.get("title", "")
            if len(t) > 40:
                warnings.append(f"Window title '{t}' is long ({len(t)} chars). Recommended <= 35 chars.")

    for container in ("window", "terminal", "quote", "timeline"):
        if open_counts[container] != close_counts[container]:
            warnings.append(f"Mismatched container tags for '{container}': {open_counts[container]} open vs {close_counts[container]} close.")

    if close_counts["metrics"] > open_counts["metrics"]:
        warnings.append(f"Mismatched container tags for 'metrics': {open_counts['metrics']} open vs {close_counts['metrics']} close.")

    return {
        "status": "success",
        "directives_found": len(directives),
        "directives": [d["type"] for d in directives],
        "warnings": warnings,
        "is_valid": len(warnings) == 0
    }

def tool_scaffold_project(
    project_type: str = "library",
    title: str = "MY PROJECT",
    subtitle: str = None,
    author: str = "DEVELOPER",
    group: str = "SE-01",
    discipline: str = "COMPUTER SCIENCE",
    repo: str = None,
    output_path: str = "README.template.md"
) -> dict:
    """Initializes a new README.template.md from predefined templates (study, library, cli)."""
    try:
        path = scaffold_readme(
            project_type=project_type,
            title=title,
            subtitle=subtitle,
            author=author,
            group=group,
            discipline=discipline,
            repo=repo,
            output_path=output_path
        )
        return {
            "status": "success",
            "project_type": project_type,
            "created_file": path,
            "next_steps": f"Customize {path} and compile using compile_readme tool."
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

def tool_inspect_safe_zones(element_type: str, title: str, subtitle: str = None) -> dict:
    """Inspects text lengths and returns character budgets, font downscaling predictions, and safety alerts."""
    el = element_type.lower()
    t_len = len(title) if title else 0
    sub_len = len(subtitle) if subtitle else 0

    analysis = {
        "element": el,
        "title_length": t_len,
        "subtitle_length": sub_len,
        "status": "optimal",
        "recommendations": []
    }

    if el == "header":
        if t_len <= 14:
            analysis["pixel_scale"] = 6
            analysis["lines"] = 1
        elif t_len <= 20:
            analysis["pixel_scale"] = 5
            analysis["lines"] = 1
            analysis["recommendations"].append("Title will downscale to px=5 to fit cleanly.")
        elif t_len <= 32:
            analysis["pixel_scale"] = 4
            analysis["lines"] = 2
            analysis["recommendations"].append("Title will wrap across 2 lines and downscale to px=4.")
        else:
            analysis["status"] = "danger"
            analysis["pixel_scale"] = 3
            analysis["lines"] = 2
            analysis["recommendations"].append("Title exceeds 32 characters! Risk of truncation or border collision.")

        if sub_len > 55:
            analysis["status"] = "warning" if analysis["status"] != "danger" else "danger"
            analysis["recommendations"].append(f"Subtitle has {sub_len} chars. Recommended max: 45.")
    elif el == "window":
        if t_len > 35:
            analysis["status"] = "warning"
            analysis["recommendations"].append(f"Window title length ({t_len}) exceeds recommended budget of 30 chars.")
    elif el == "chip":
        if t_len > 24:
            analysis["status"] = "warning"
            analysis["recommendations"].append(f"Chip label length ({t_len}) exceeds recommended budget of 20 chars.")

    return analysis

# ==============================================================================
# TOOL REGISTRY FOR MCP
# ==============================================================================

TOOLS_METADATA = [
    {
        "name": "compile_readme",
        "description": "Compiles a Markdown template with pixel-kit directives into GitHub-ready README.md and generates SVGs.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "template_path": {"type": "string", "default": "README.template.md", "description": "Source template file path"},
                "output_path": {"type": "string", "default": "README.md", "description": "Target compiled markdown file path"},
                "assets_dir": {"type": "string", "default": "assets/generated", "description": "Directory where generated SVGs will be stored"},
                "clean_assets": {"type": "boolean", "default": False, "description": "Remove orphan SVG assets not referenced in template"},
                "dry_run": {"type": "boolean", "default": False, "description": "Preview orphan files without deleting"},
                "no_cache": {"type": "boolean", "default": False, "description": "Force regeneration of all SVG assets"},
                "bust_cache": {"type": "boolean", "default": False, "description": "Append content hash query params to bypass Camo proxy caching"}
            }
        }
    },
    {
        "name": "render_block",
        "description": "Generates a standalone pixel-HUD SVG block (header, footer, callout, frame, chip, divider, splitter, metrics, progress, techstack, timeline, social, starchart, profile).",
        "inputSchema": {
            "type": "object",
            "required": ["block_type"],
            "properties": {
                "block_type": {"type": "string", "enum": ["header", "footer", "callout", "frame", "chip", "divider", "splitter", "metrics", "progress", "techstack", "timeline", "social", "starchart", "profile"]},
                "style": {"type": "string", "enum": ["pixel", "modern", "sketch", "cyberpunk", "tactical", "minimal"], "default": "cyberpunk"},
                "theme": {"type": "string", "description": "Theme name (e.g. slate-dark, tokyo, emerald-clean, notebook-graph)"},
                "mode": {"type": "string", "enum": ["auto", "dark", "light", "transparent", "gh", "picture"], "default": "auto"},
                "preset": {"type": "string", "description": "Preset name (cyberpunk, amber, matrix, tokyo) or JSON path"},
                "primary": {"type": "string", "description": "Hex primary color (e.g. #00C8D7)"},
                "accent": {"type": "string", "description": "Hex accent color (e.g. #A855F7)"},
                "title": {"type": "string", "description": "Main title / label text"},
                "subtitle": {"type": "string", "description": "Subtitle / secondary text"},
                "tag": {"type": "string", "description": "Status badge or button text"},
                "frame_type": {"type": "string", "enum": ["top", "bottom"], "default": "top"},
                "chip_type": {"type": "string", "enum": ["closed", "decay", "pulse"], "default": "closed"},
                "callout_type": {"type": "string", "enum": ["note", "warning", "critical", "success", "info"], "default": "note"},
                "compact": {"type": "boolean", "default": False, "description": "Compact mode for header (~84px height)"},
                "output_path": {"type": "string", "description": "Optional file path to save the generated SVG"}
            }
        }
    },
    {
        "name": "validate_template",
        "description": "Validates template directives, checks syntax, and identifies text length / layout collisions.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Path to template markdown file to validate"},
                "content": {"type": "string", "description": "Raw markdown template content string"}
            }
        }
    },
    {
        "name": "scaffold_project",
        "description": "Scaffolds a new README.template.md using predefined sci-fi HUD templates (study, library, cli).",
        "inputSchema": {
            "type": "object",
            "properties": {
                "project_type": {"type": "string", "enum": ["study", "library", "cli"], "default": "library"},
                "title": {"type": "string", "default": "MY PROJECT"},
                "subtitle": {"type": "string"},
                "author": {"type": "string", "default": "DEVELOPER"},
                "group": {"type": "string", "default": "SE-01"},
                "discipline": {"type": "string", "default": "COMPUTER SCIENCE"},
                "repo": {"type": "string"},
                "output_path": {"type": "string", "default": "README.template.md"}
            }
        }
    },
    {
        "name": "inspect_safe_zones",
        "description": "Calculates font downscaling, multi-line wrapping predictions, and collision risks for text elements.",
        "inputSchema": {
            "type": "object",
            "required": ["element_type", "title"],
            "properties": {
                "element_type": {"type": "string", "enum": ["header", "window", "callout", "chip"]},
                "title": {"type": "string", "description": "Candidate title or label string"},
                "subtitle": {"type": "string", "description": "Candidate subtitle or description string"}
            }
        }
    }
]

def dispatch_tool_call(name: str, arguments: dict) -> dict:
    if name == "compile_readme":
        return tool_compile_readme(**arguments)
    elif name == "render_block":
        return tool_render_block(**arguments)
    elif name == "validate_template":
        return tool_validate_template(**arguments)
    elif name == "scaffold_project":
        return tool_scaffold_project(**arguments)
    elif name == "inspect_safe_zones":
        return tool_inspect_safe_zones(**arguments)
    else:
        raise ValueError(f"Unknown tool: '{name}'")

# ==============================================================================
# NATIVE STDIO JSON-RPC 2.0 PROTOCOL ENGINE
# ==============================================================================

def run_native_stdio_server():
    """Runs zero-dependency standard MCP stdio JSON-RPC loop."""
    sys.stderr.write("[*] ReadmeKit MCP Server v5.1 running on STDIO...\n")
    sys.stderr.flush()

    while True:
        try:
            line = sys.stdin.readline()
            if not line:
                break
            line = line.strip()
            if not line:
                continue

            try:
                request = json.loads(line)
            except Exception:
                err_resp = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32700,
                        "message": "Parse error"
                    }
                }
                sys.stdout.write(json.dumps(err_resp, ensure_ascii=False) + "\n")
                sys.stdout.flush()
                continue

            if not isinstance(request, dict):
                continue

            req_id = request.get("id")
            method = request.get("method")
            params = request.get("params", {})

            # Per JSON-RPC 2.0: if "id" is absent, it is a notification and must not receive a response
            if "id" not in request:
                continue

            if method == "initialize":
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {
                            "tools": {}
                        },
                        "serverInfo": {
                            "name": "readme-kit",
                            "version": "5.1.0"
                        }
                    }
                }
            elif method == "notifications/initialized":
                continue  # No response needed for notifications
            elif method == "ping":
                response = {"jsonrpc": "2.0", "id": req_id, "result": {}}
            elif method == "tools/list":
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "result": {
                        "tools": TOOLS_METADATA
                    }
                }
            elif method == "tools/call":
                tool_name = params.get("name")
                tool_args = params.get("arguments", {})
                try:
                    tool_res = dispatch_tool_call(tool_name, tool_args)
                    response = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": json.dumps(tool_res, indent=2, ensure_ascii=False)
                                }
                            ]
                        }
                    }
                except Exception as e:
                    response = {
                        "jsonrpc": "2.0",
                        "id": req_id,
                        "result": {
                            "isError": True,
                            "content": [
                                {
                                    "type": "text",
                                    "text": f"Error executing tool '{tool_name}': {str(e)}"
                                }
                            ]
                        }
                    }
            else:
                response = {
                    "jsonrpc": "2.0",
                    "id": req_id,
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: '{method}'"
                    }
                }

            sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
            sys.stdout.flush()

        except Exception as e:
            sys.stderr.write(f"[!] Protocol error: {str(e)}\n{traceback.format_exc()}\n")
            sys.stderr.flush()

def main():
    # If FastMCP is available and requested, we can use it, else native stdio
    try:
        from mcp.server.fastmcp import FastMCP
        # If user explicitly wants FastMCP
        if "--fastmcp" in sys.argv:
            mcp = FastMCP("readme-kit")
            mcp.tool()(tool_compile_readme)
            mcp.tool()(tool_render_block)
            mcp.tool()(tool_validate_template)
            mcp.tool()(tool_scaffold_project)
            mcp.tool()(tool_inspect_safe_zones)
            mcp.run()
            return
    except ImportError:
        pass

    # Default to zero-dependency native stdio JSON-RPC server
    run_native_stdio_server()

if __name__ == "__main__":
    main()
