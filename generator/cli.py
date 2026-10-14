"""
CLI Generator & Compiler for Pixel Readme Kit v3.0
Usage modes:
1. Generate individual SVG blocks (supports --mode auto|dark|light|transparent|gh|picture):
   python -m generator.cli header --help
   python -m generator.cli footer --help
   python -m generator.cli callout --help
   python -m generator.cli frame --help
   python -m generator.cli chip --help
   python -m generator.cli divider --help
   python -m generator.cli splitter --help

2. Compile README markdown template with pixel-kit directives:
   python -m generator.cli compile --input README.template.md --output README.md --assets-dir assets/generated
"""

import os
import sys
import argparse

# Add parent directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

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
    validate_svg
)
from generator.themes import normalize_style_and_theme, VALID_STYLES
from generator.compiler import MarkdownCompiler
from generator.scaffolder import scaffold_readme, get_available_templates

def save_output(svg_content, output_path, default_path):
    target = output_path if output_path else default_path
    os.makedirs(os.path.dirname(os.path.abspath(target)), exist_ok=True)
    validate_svg(svg_content)
    with open(target, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"[+] Generated SVG successfully: {target}")

def handle_cli_output(args, generator_fn, gen_kwargs, default_name):
    mode = getattr(args, "mode", "auto")
    if mode in ("gh", "github"):
        out = args.output if args.output else f"assets/{default_name}.svg"
        base, ext = os.path.splitext(out)
        out_dark = f"{base}-dark{ext}"
        out_light = f"{base}-light{ext}"
        svg_dark = generator_fn(**dict(gen_kwargs, mode="dark"))
        svg_light = generator_fn(**dict(gen_kwargs, mode="light"))
        save_output(svg_dark, out_dark, out_dark)
        save_output(svg_light, out_light, out_light)
        print("\n[i] GitHub Dark/Light Markdown syntax:")
        print(f"![{default_name}]({out_dark}#gh-dark-mode-only)")
        print(f"![{default_name}]({out_light}#gh-light-mode-only)")
    elif mode == "picture":
        out = args.output if args.output else f"assets/{default_name}.svg"
        base, ext = os.path.splitext(out)
        out_dark = f"{base}-dark{ext}"
        out_light = f"{base}-light{ext}"
        svg_dark = generator_fn(**dict(gen_kwargs, mode="dark"))
        svg_light = generator_fn(**dict(gen_kwargs, mode="light"))
        save_output(svg_dark, out_dark, out_dark)
        save_output(svg_light, out_light, out_light)
        print("\n[i] HTML5 <picture> syntax:")
        print(f'<picture>\n  <source media="(prefers-color-scheme: dark)" srcset="{out_dark}">\n  <source media="(prefers-color-scheme: light)" srcset="{out_light}">\n  <img src="{out_dark}">\n</picture>')
    else:
        svg = generator_fn(**dict(gen_kwargs, mode=mode))
        save_output(svg, args.output, f"assets/{default_name}.svg")

def cmd_header(args):
    style, theme = normalize_style_and_theme(getattr(args, "style", None), getattr(args, "theme", None))
    handle_cli_output(args, generate_header, {
        "style": style,
        "theme": theme,
        "primary": args.primary,
        "accent": args.accent,
        "preset": args.preset,
        "title": args.title,
        "subtitle": args.subtitle,
        "tag": args.tag,
        "tag_url": getattr(args, "tag_url", None),
        "close_url": getattr(args, "close_url", None),
        "spec1": args.spec1,
        "spec2": args.spec2,
        "spec3": args.spec3,
        "specs": args.specs,
        "compact": getattr(args, "compact", False)
    }, f"header-{theme}")

def cmd_social(args):
    style, theme = normalize_style_and_theme(getattr(args, "style", None), getattr(args, "theme", None))
    tags = [x.strip() for x in args.tags.split(",") if x.strip()] if getattr(args, "tags", None) else None
    handle_cli_output(args, generate_social, {
        "style": style,
        "theme": theme,
        "primary": args.primary,
        "accent": args.accent,
        "preset": args.preset,
        "title": args.title,
        "subtitle": args.subtitle,
        "repo": getattr(args, "repo", "pixel-readme-kit"),
        "tags": tags
    }, f"social-{theme}")

def cmd_footer(args):
    style, theme = normalize_style_and_theme(getattr(args, "style", None), getattr(args, "theme", None))
    handle_cli_output(args, generate_footer, {
        "style": style,
        "theme": theme,
        "primary": args.primary,
        "accent": args.accent,
        "preset": args.preset,
        "status": args.status,
        "nav_text": args.nav,
        "sub_text": args.sub
    }, f"footer-{theme}")

def cmd_callout(args):
    style, theme = normalize_style_and_theme(getattr(args, "style", None), getattr(args, "theme", None))
    prefix = "callout-quote" if args.quote else "callout"
    handle_cli_output(args, generate_callout, {
        "style": style,
        "theme": theme,
        "primary": args.primary,
        "accent": args.accent,
        "preset": args.preset,
        "callout_type": args.type,
        "title": args.title,
        "subtitle": args.subtitle,
        "is_quote": args.quote,
        "badge_color": getattr(args, "badge_color", None)
    }, f"{prefix}-{theme}-{args.type}")

def cmd_frame(args):
    style, theme = normalize_style_and_theme(getattr(args, "style", None), getattr(args, "theme", None))
    handle_cli_output(args, generate_frame, {
        "style": style,
        "theme": theme,
        "primary": args.primary,
        "accent": args.accent,
        "preset": args.preset,
        "frame_type": args.type,
        "title": args.title,
        "tag": args.tag,
        "tag_url": getattr(args, "tag_url", None),
        "close_url": getattr(args, "close_url", None)
    }, f"frame-{args.type}-{theme}")

def cmd_chip(args):
    style, theme = normalize_style_and_theme(getattr(args, "style", None), getattr(args, "theme", None))
    chip_text = args.text
    if getattr(args, "github", None):
        repo = getattr(args, "repo", None) or "Kazinagg/pixel-readme-kit"
        from generator.compiler import fetch_github_stat
        stat_text, _ = fetch_github_stat(repo, args.github)
        chip_text = stat_text

    handle_cli_output(args, generate_chip, {
        "style": style,
        "theme": theme,
        "primary": args.primary,
        "accent": args.accent,
        "preset": args.preset,
        "chip_type": args.type,
        "text": chip_text,
        "width": args.width,
        "decay_dir": getattr(args, "decay_dir", "right")
    }, f"chip-{theme}-{args.type}")

def cmd_divider(args):
    style, theme = normalize_style_and_theme(getattr(args, "style", None), getattr(args, "theme", None))
    handle_cli_output(args, generate_divider, {
        "style": style,
        "theme": theme,
        "primary": args.primary,
        "accent": args.accent,
        "preset": args.preset
    }, f"divider-{theme}")

def cmd_splitter(args):
    style, theme = normalize_style_and_theme(getattr(args, "style", None), getattr(args, "theme", None))
    handle_cli_output(args, generate_splitter, {
        "style": style,
        "theme": theme,
        "primary": args.primary,
        "accent": args.accent,
        "preset": args.preset,
        "label": args.label
    }, f"splitter-{theme}")

def cmd_metrics(args):
    style, theme = normalize_style_and_theme(getattr(args, "style", None), getattr(args, "theme", None))
    items = []
    if getattr(args, "fetch_github", False) and getattr(args, "repo", None):
        from generator.github_api import fetch_repo_data
        rdata, err = fetch_repo_data(args.repo)
        if rdata:
            items = [
                {"label": "STARS", "value": f"{rdata['stars']:,}", "delta": "+growth", "trend": "up"},
                {"label": "FORKS", "value": f"{rdata['forks']:,}", "delta": "active", "trend": "up"},
                {"label": "WATCHERS", "value": f"{rdata['watchers']:,}", "trend": "neutral"},
                {"label": "LICENSE", "value": rdata["license"], "trend": "neutral"}
            ]
        elif err:
            print(f"[!] Warning: GitHub API error: {err}")

    if not items:
        if getattr(args, "items", None):
            from generator.compiler import parse_directive_attrs
            for chunk in args.items.split("|"):
                attrs = parse_directive_attrs(chunk.strip())
                if attrs:
                    items.append(attrs)
        else:
            items = [{
                "label": args.label or "FPS BENCHMARK",
                "value": args.value or "1,200+",
                "delta": args.delta or "+24% vs baseline",
                "trend": getattr(args, "trend", "up"),
                "status": getattr(args, "status", None)
            }]

    handle_cli_output(args, generate_metrics, {
        "metrics": items,
        "style": style,
        "theme": theme,
        "primary": args.primary,
        "accent": args.accent,
        "preset": args.preset
    }, f"metrics-{theme}")

def cmd_progress(args):
    style, theme = normalize_style_and_theme(getattr(args, "style", None), getattr(args, "theme", None))
    handle_cli_output(args, generate_progress, {
        "value": args.value,
        "label": args.label,
        "sub": args.sub,
        "style": style,
        "theme": theme,
        "primary": args.primary,
        "accent": args.accent,
        "preset": args.preset
    }, f"progress-{theme}")

def cmd_techstack(args):
    style, theme = normalize_style_and_theme(getattr(args, "style", None), getattr(args, "theme", None))
    items = [x.strip() for x in args.items.split(",") if x.strip()] if args.items else ["python", "cpp", "rust", "docker", "git"]
    handle_cli_output(args, generate_techstack, {
        "items": items,
        "columns": args.columns,
        "style": style,
        "theme": theme,
        "primary": args.primary,
        "accent": args.accent,
        "preset": args.preset
    }, f"techstack-{theme}")

def cmd_timeline(args):
    style, theme = normalize_style_and_theme(getattr(args, "style", None), getattr(args, "theme", None))
    handle_cli_output(args, generate_timeline, {
        "style": style,
        "theme": theme,
        "primary": args.primary,
        "accent": args.accent,
        "preset": args.preset
    }, f"timeline-{theme}")

def cmd_starchart(args):
    style, theme = normalize_style_and_theme(getattr(args, "style", None), getattr(args, "theme", None))
    pts = [float(x.strip()) for x in args.points.split(",") if x.strip()] if getattr(args, "points", None) else None
    cur = args.current
    delta = args.delta
    if getattr(args, "fetch_github", False) and getattr(args, "repo", None):
        from generator.github_api import fetch_star_trajectory
        traj, err = fetch_star_trajectory(args.repo)
        if traj:
            if not getattr(args, "points", None) or args.points == "15,65,190,480,950,1650":
                pts = traj.get("points")
            if not cur:
                cur = traj.get("current")
            if not getattr(args, "delta", None) or delta == "+78% past 6m":
                delta = traj.get("delta")
        elif err:
            print(f"[!] Warning: GitHub API error: {err}")

    handle_cli_output(args, generate_starchart, {
        "style": style,
        "theme": theme,
        "repo": args.repo,
        "points": pts,
        "current": cur,
        "delta": delta,
        "title": args.title,
        "period": args.period,
        "primary": args.primary,
        "accent": args.accent,
        "preset": args.preset
    }, f"starchart-{theme}")

def cmd_profile(args):
    style, theme = normalize_style_and_theme(getattr(args, "style", None), getattr(args, "theme", None))
    name = args.name
    role = args.role
    bio = args.bio
    status = args.status
    loc = args.location
    badge = args.badge
    username = getattr(args, "username", None)
    if getattr(args, "fetch_github", False) and (username or name):
        from generator.github_api import fetch_user_data
        uname = username or name
        udata, err = fetch_user_data(uname)
        if udata:
            if name == "ALEX DEVELOPER" and udata.get("name"):
                name = udata["name"]
            if "Building high-performance" in bio and udata.get("bio"):
                bio = udata["bio"]
            if loc == "REMOTE // UTC+3" and udata.get("location"):
                loc = udata["location"]
            if badge == "LEVEL_99" and udata.get("public_repos") is not None:
                badge = f"REPOS: {udata['public_repos']}"
        elif err:
            print(f"[!] Warning: GitHub API error: {err}")

    handle_cli_output(args, generate_profile_card, {
        "style": style,
        "theme": theme,
        "name": name,
        "role": role,
        "bio": bio,
        "status": status,
        "location": loc,
        "badge": badge,
        "primary": args.primary,
        "accent": args.accent,
        "preset": args.preset
    }, f"profile-{theme}")

def cmd_compile(args):
    inp = args.input if args.input else "README.template.md"
    if args.output:
        out = args.output
    else:
        out = "README.md" if inp == "README.template.md" else (inp.replace(".template.md", ".md") if ".template.md" in inp else "README.md")
    print(f"[*] Compiling Markdown template: {inp}")
    print(f"[*] Assets directory: {args.assets_dir}")
    print(f"[*] Output destination: {out}")
    use_cache = not getattr(args, "no_cache", False)
    clean_assets = getattr(args, "clean_assets", False)
    dry_run = getattr(args, "dry_run", False)
    bust_cache = getattr(args, "bust_cache", False)
    fetch_github = getattr(args, "fetch_github", False)

    compiler = MarkdownCompiler(assets_dir=args.assets_dir, use_cache=use_cache, bust_cache=bust_cache, fetch_github=fetch_github)
    compiler.compile_file(inp, out, clean_assets=clean_assets, dry_run_clean=dry_run)
    print(f"[+] Successfully compiled to: {out}")
    print(f"[i] Build stats: {compiler.stats['generated']} generated, {compiler.stats['cached']} cached")
    if clean_assets or dry_run:
        if compiler.orphans:
            action = "Orphan assets found (dry-run)" if dry_run else "Cleaned orphan assets"
            print(f"[i] {action} ({len(compiler.orphans)}):")
            for f in compiler.orphans:
                print(f"    - {f}")
        else:
            print("[i] Clean assets: no orphan files detected.")

def cmd_sync(args):
    """Auto-updates all stats from GitHub, cleans orphan assets and busts Camo cache."""
    print("[*] Syncing README with live GitHub data...")
    setattr(args, "fetch_github", True)
    setattr(args, "clean_assets", True)
    setattr(args, "bust_cache", True)
    setattr(args, "no_cache", False)
    setattr(args, "dry_run", False)
    cmd_compile(args)

def cmd_serve(args):
    from generator.server import run_studio_server
    inp = args.input if args.input else "README.template.md"
    if args.output:
        out = args.output
    else:
        out = "README.md" if inp == "README.template.md" else (inp.replace(".template.md", ".md") if ".template.md" in inp else "README.md")
    port = getattr(args, "port", 3000)
    open_browser = getattr(args, "open", False)
    run_studio_server(template_path=inp, output_path=out, assets_dir=args.assets_dir, port=port, open_browser=open_browser)

def cmd_init(args):
    ptype = args.type
    category = getattr(args, "category", None)
    title = args.title
    if not ptype:
        print("\n=== README KIT SCAFFOLDER v5.1 ===")
        print("Select template type:")
        print("--- REPOSITORIES (repo/) ---")
        print("1. repo/library   (Open Source package / SDK / modular component)")
        print("2. repo/cli       (Command-line utility / terminal tool)")
        print("3. repo/study     (Laboratory report / student dossier / coursework)")
        print("4. repo/minimal   (Clean corporate / minimal repository)")
        print("5. repo/modern    (Modern clean SaaS / WebApp repository)")
        print("6. repo/sketch    (Hand-drawn Excalidraw sketch repository)")
        print("--- PROFILES (profile/) ---")
        print("7. profile/dev    (Comprehensive developer profile / username/username)")
        print("8. profile/min    (Clean minimalist developer profile)")
        print("9. profile/cyber  (Futuristic HUD / cyber developer profile)")
        choice = input("Enter choice [1-9] (default: 1): ").strip()
        mapping = {
            "1": "repo/library",
            "2": "repo/cli",
            "3": "repo/study",
            "4": "repo/minimal",
            "5": "repo/modern",
            "6": "repo/sketch",
            "7": "profile/developer",
            "8": "profile/minimal",
            "9": "profile/cyberpunk",
        }
        ptype = mapping.get(choice, "repo/library")

    if not title:
        try:
            default_title = os.path.basename(os.getcwd()).upper()
        except Exception:
            default_title = "MY-PROJECT"
        user_title = input(f"Project Title (default: {default_title}): ").strip()
        title = user_title if user_title else default_title

    out = args.output if args.output else "README.template.md"
    if os.path.exists(out) and not getattr(args, "force", False):
        print(f"[!] Warning: {out} already exists.")
        confirm = input("Overwrite? (y/N): ").strip().lower()
        if confirm != "y":
            print("[-] Scaffolding cancelled.")
            return

    scaffold_readme(
        project_type=ptype,
        category=category,
        title=title,
        subtitle=args.subtitle,
        author=args.author if args.author else "DEVELOPER",
        group=args.group if args.group else "SE-01",
        discipline=args.discipline if args.discipline else "COMPUTER SCIENCE",
        repo=args.repo,
        style=getattr(args, "style", "pixel"),
        theme=getattr(args, "theme", None),
        output_path=out
    )
    print(f"[+] Initialized template: {out} (type: {ptype})")
    print(f"[*] Next step: customize {out} and run:")
    print(f"    python -m generator.cli compile --input {out}")

def build_parser():
    parser = argparse.ArgumentParser(
        prog="readme-kit",
        description="ReadmeKit v5.1.0 — Multi-Style Translucent HUD & Multi-Paradigm Markdown Compiler"
    )

    subparsers = parser.add_subparsers(dest="command", help="Block type or compiler action")
    mode_choices = ["auto", "dark", "light", "transparent", "gh", "picture"]
    style_choices = ["pixel", "modern", "corporate", "sketch", "doodle", "cyberpunk", "tactical", "minimal"]

    # 1. HEADER
    p_hdr = subparsers.add_parser("header", help="Generate flagship header banner")
    p_hdr.add_argument("--style", choices=style_choices, default="pixel", help="Geometry style (pixel, modern, corporate)")
    p_hdr.add_argument("--theme", help="Color palette theme (e.g. cyberpunk, tactical, minimal, tokyo, amber, slate-dark, nordic-frost)")
    p_hdr.add_argument("--mode", choices=mode_choices, default="auto", help="Theme mode: auto (default), dark, light, transparent, gh, picture")
    p_hdr.add_argument("--preset", help="Named palette preset (e.g. cyberpunk, amber, matrix, tokyo) or path to JSON")
    p_hdr.add_argument("--primary", help="Primary brand hex color (e.g. #00C8D7, #F59E0B, #4F8BFF)")
    p_hdr.add_argument("--accent", help="Secondary accent hex color (e.g. #A855F7, #EA580C)")
    p_hdr.add_argument("--title", default="PIXEL-KIT", help="Main title text")
    p_hdr.add_argument("--subtitle", default="TRANSLUCENT HUD DESIGN SYSTEM", help="Subtitle description text")
    p_hdr.add_argument("--tag", default="SYSTEM_ACTIVE", help="Top badge tag text")
    p_hdr.add_argument("--tag-url", help="Optional URL link for the top badge tag")
    p_hdr.add_argument("--close-url", help="Optional URL link for the close button [x]")
    p_hdr.add_argument("--spec1", help="Level 3 spec line 1 (e.g. 'HUD ARCHITECTURE: TRANSLUCENT GLASS')")
    p_hdr.add_argument("--spec2", help="Level 3 spec line 2 (e.g. 'TEXT INTEGRATION: 100%% COPYABLE MARKDOWN')")
    p_hdr.add_argument("--spec3", help="Level 3 spec line 3 (e.g. 'ANIMATION SUITE: RADAR // SCANLINE')")
    p_hdr.add_argument("--specs", help="Combined level 3 specs separated by '|' (max 3 items)")
    p_hdr.add_argument("--compact", action="store_true", help="Generate compact header (~84px height) optimized for mobile/minimal readmes")
    p_hdr.add_argument("--output", "-o", help="Target SVG destination path")
    p_hdr.set_defaults(func=cmd_header)

    # 2. FOOTER
    p_ftr = subparsers.add_parser("footer", help="Generate full-width closing footer plate")
    p_ftr.add_argument("--style", choices=style_choices, default="pixel", help="Geometry style (pixel, modern, corporate)")
    p_ftr.add_argument("--theme", help="Color palette theme")
    p_ftr.add_argument("--mode", choices=mode_choices, default="auto", help="Theme mode: auto (default), dark, light, transparent, gh, picture")
    p_ftr.add_argument("--preset", help="Named palette preset (e.g. cyberpunk, amber, matrix, tokyo) or path to JSON")
    p_ftr.add_argument("--primary", help="Primary brand hex color")
    p_ftr.add_argument("--accent", help="Secondary accent hex color")
    p_ftr.add_argument("--status", default="SESSION_ACTIVE // STANDBY", help="Status telemetry readout text")
    p_ftr.add_argument("--sub", help="Secondary diagnostic or telemetry readout line")
    p_ftr.add_argument("--nav", default="RETURN TO TOP", help="Navigation button text")
    p_ftr.add_argument("--output", "-o", help="Target SVG destination path")
    p_ftr.set_defaults(func=cmd_footer)

    # 3. CALLOUT
    p_clt = subparsers.add_parser("callout", help="Generate inline alert plate or quote header")
    p_clt.add_argument("--style", choices=style_choices, default="pixel", help="Geometry style (pixel, modern, corporate)")
    p_clt.add_argument("--theme", help="Color palette theme")
    p_clt.add_argument("--mode", choices=mode_choices, default="auto", help="Theme mode: auto (default), dark, light, transparent, gh, picture")
    p_clt.add_argument("--preset", help="Named palette preset (e.g. cyberpunk, amber, matrix, tokyo) or path to JSON")
    p_clt.add_argument("--type", choices=["note", "warning", "critical", "success", "info"], default="note", help="Callout type / badge")
    p_clt.add_argument("--primary", help="Primary brand hex color")
    p_clt.add_argument("--accent", help="Secondary accent hex color")
    p_clt.add_argument("--title", default="SYSTEM ARCHITECTURE NOTICE", help="Callout header title text")
    p_clt.add_argument("--subtitle", default="Dual-theme contrast > 7:1 // Monospace typography", help="Callout subtext message")
    p_clt.add_argument("--quote", action="store_true", help="Generate quote header sub-variant (open left edge + dashed bottom line)")
    p_clt.add_argument("--badge-color", help="Custom hex color or GitHub alert name for badge and strip")
    p_clt.add_argument("--output", "-o", help="Target SVG destination path")
    p_clt.set_defaults(func=cmd_callout)

    # 4. FRAME
    p_frm = subparsers.add_parser("frame", help="Generate window top cap or bottom plate")
    p_frm.add_argument("--style", choices=style_choices, default="pixel", help="Geometry style (pixel, modern, corporate)")
    p_frm.add_argument("--theme", help="Color palette theme")
    p_frm.add_argument("--mode", choices=mode_choices, default="auto", help="Theme mode: auto (default), dark, light, transparent, gh, picture")
    p_frm.add_argument("--preset", help="Named palette preset (e.g. cyberpunk, amber, matrix, tokyo) or path to JSON")
    p_frm.add_argument("--type", choices=["top", "bottom"], default="top", help="Frame position: top or bottom")
    p_frm.add_argument("--primary", help="Primary brand hex color")
    p_frm.add_argument("--accent", help="Secondary accent hex color")
    p_frm.add_argument("--title", default="╔═ SYSTEM.CORE // RUNTIME.SYS", help="Window title text (for top frame)")
    p_frm.add_argument("--tag", default="[OPEN_HUD]", help="Window tag text (for top frame)")
    p_frm.add_argument("--tag-url", help="Optional URL link for the top frame tag")
    p_frm.add_argument("--close-url", help="Optional URL link for the close button [x]")
    p_frm.add_argument("--output", "-o", help="Target SVG destination path")
    p_frm.set_defaults(func=cmd_frame)

    # 5. CHIP
    p_chp = subparsers.add_parser("chip", help="Generate holographic pill / chip badge")
    p_chp.add_argument("--style", choices=style_choices, default="pixel", help="Geometry style (pixel, modern, corporate)")
    p_chp.add_argument("--theme", help="Color palette theme")
    p_chp.add_argument("--mode", choices=mode_choices, default="auto", help="Theme mode: auto (default), dark, light, transparent, gh, picture")
    p_chp.add_argument("--preset", help="Named palette preset (e.g. cyberpunk, amber, matrix, tokyo) or path to JSON")
    p_chp.add_argument("--type", choices=["closed", "decay", "pulse"], default="closed", help="Form & decay mechanics: closed, decay, pulse")
    p_chp.add_argument("--primary", help="Primary brand hex color")
    p_chp.add_argument("--accent", help="Secondary accent hex color")
    p_chp.add_argument("--text", default="CHIP_TAG", help="Text label inside the chip")
    p_chp.add_argument("--github", choices=["stars", "forks", "issues", "license", "watchers", "version", "release"], help="Fetch live GitHub stat for label")
    p_chp.add_argument("--repo", default="Kazinagg/pixel-readme-kit", help="GitHub repo for live stats (e.g. Kazinagg/pixel-readme-kit)")
    p_chp.add_argument("--width", type=int, help="Optional manual width override in px (default: auto-calculated from text)")
    p_chp.add_argument("--decay-dir", choices=["right", "left", "both"], default="right", help="Decay direction: right, left, both (default: right)")
    p_chp.add_argument("--output", "-o", help="Target SVG destination path")
    p_chp.set_defaults(func=cmd_chip)

    # 6. DIVIDER
    p_div = subparsers.add_parser("divider", help="Generate chapter divider (PCB, Laser, or Spectrum)")
    p_div.add_argument("--style", choices=style_choices, default="pixel", help="Geometry style (pixel, modern, corporate)")
    p_div.add_argument("--theme", help="Color palette theme")
    p_div.add_argument("--mode", choices=mode_choices, default="auto", help="Theme mode: auto (default), dark, light, transparent, gh, picture")
    p_div.add_argument("--preset", help="Named palette preset (e.g. cyberpunk, amber, matrix, tokyo) or path to JSON")
    p_div.add_argument("--primary", help="Primary brand hex color")
    p_div.add_argument("--accent", help="Secondary accent hex color")
    p_div.add_argument("--output", "-o", help="Target SVG destination path")
    p_div.set_defaults(func=cmd_divider)

    # 7. SPLITTER
    p_spl = subparsers.add_parser("splitter", help="Generate sub-module splitter (flush x=1..849)")
    p_spl.add_argument("--style", choices=style_choices, default="pixel", help="Geometry style (pixel, modern, corporate)")
    p_spl.add_argument("--theme", help="Color palette theme")
    p_spl.add_argument("--mode", choices=mode_choices, default="auto", help="Theme mode: auto (default), dark, light, transparent, gh, picture")
    p_spl.add_argument("--preset", help="Named palette preset (e.g. cyberpunk, amber, matrix, tokyo) or path to JSON")
    p_spl.add_argument("--primary", help="Primary brand hex color")
    p_spl.add_argument("--accent", help="Secondary accent hex color")
    p_spl.add_argument("--label", default="[MODULE: SUB_SYSTEM]", help="Splitter center label text")
    p_spl.add_argument("--output", "-o", help="Target SVG destination path")
    p_spl.set_defaults(func=cmd_splitter)

    # 8. COMPILE
    p_cmp = subparsers.add_parser("compile", help="Compile README template markdown containing pixel-kit directives")
    p_cmp.add_argument("--input", "-i", "--template", default="README.template.md", help="Input Markdown template filepath (default: README.template.md)")
    p_cmp.add_argument("--output", "-o", default=None, help="Output compiled Markdown filepath (default: README.md or matching *.md)")
    p_cmp.add_argument("--assets-dir", default="assets/generated", help="Folder where generated SVGs will be stored")
    p_cmp.add_argument("--clean-assets", action="store_true", help="Remove unused/orphan SVG files from assets directory")
    p_cmp.add_argument("--dry-run", action="store_true", help="Preview orphan SVG files that would be cleaned without deleting")
    p_cmp.add_argument("--no-cache", action="store_true", help="Disable build cache and force regeneration of all assets")
    p_cmp.add_argument("--bust-cache", action="store_true", help="Append content hash query params (?v=<hash>) to asset URLs to bypass GitHub Camo proxy caching")
    p_cmp.add_argument("--fetch-github", action="store_true", help="Fetch live stats, profile info and star history from GitHub API")
    p_cmp.set_defaults(func=cmd_compile)

    # 8.5 SYNC (Auto-Update Cron Command)
    p_syn = subparsers.add_parser("sync", help="Auto-update README stats from GitHub, bust Camo cache, and clean orphan assets")
    p_syn.add_argument("--input", "-i", "--template", default="README.template.md", help="Input Markdown template filepath (default: README.template.md)")
    p_syn.add_argument("--output", "-o", default=None, help="Output compiled Markdown filepath (default: README.md or matching *.md)")
    p_syn.add_argument("--assets-dir", default="assets/generated", help="Folder where generated SVGs will be stored")
    p_syn.set_defaults(func=cmd_sync)

    # 9. INIT (Scaffolder)
    p_init = subparsers.add_parser("init", help="Scaffold a new README.template.md for a repository or developer profile")
    p_init.add_argument("--category", choices=["repo", "profile"], help="Template category: repo or profile")
    p_init.add_argument("--type", help="Template type (e.g. repo/library, repo/cli, repo/study, repo/minimal, profile/developer, profile/minimal, profile/cyberpunk)")
    p_init.add_argument("--style", choices=style_choices, default="pixel", help="Geometry style")
    p_init.add_argument("--theme", help="Color palette theme")
    p_init.add_argument("--title", help="Main project or profile title")
    p_init.add_argument("--subtitle", help="Project subtitle or profile bio")
    p_init.add_argument("--author", help="Author name (for study or profile template)")
    p_init.add_argument("--group", help="Student group (for study template)")
    p_init.add_argument("--discipline", help="Discipline / course name (for study template)")
    p_init.add_argument("--repo", help="GitHub repo in 'owner/repo' format")
    p_init.add_argument("--output", "-o", default="README.template.md", help="Destination template file path (default: README.template.md)")
    p_init.add_argument("--force", "-f", action="store_true", help="Overwrite existing template file without prompt")
    p_init.set_defaults(func=cmd_init)

    # 10. METRICS
    p_met = subparsers.add_parser("metrics", help="Generate full-width KPI metrics card row")
    p_met.add_argument("--style", choices=style_choices, default="pixel", help="Geometry style (pixel, modern, corporate)")
    p_met.add_argument("--theme", help="Color palette theme")
    p_met.add_argument("--mode", choices=mode_choices, default="auto", help="Theme mode: auto (default), dark, light, transparent, gh, picture")
    p_met.add_argument("--preset", help="Named palette preset or path to JSON")
    p_met.add_argument("--primary", help="Primary brand hex color")
    p_met.add_argument("--accent", help="Secondary accent hex color")
    p_met.add_argument("--label", default="BENCHMARK", help="Card label")
    p_met.add_argument("--value", default="1,200+", help="Metric value")
    p_met.add_argument("--delta", help="Delta text e.g. '+24%% vs baseline'")
    p_met.add_argument("--trend", choices=["up", "down", "neutral"], default="up", help="Trend direction")
    p_met.add_argument("--status", help="Status pill text e.g. OPTIMAL")
    p_met.add_argument("--items", help="Multiple items separated by '|' e.g. 'label=CPU value=42%% | label=RAM value=12GB'")
    p_met.add_argument("--repo", help="GitHub repo in 'owner/repo' format for live stats")
    p_met.add_argument("--fetch-github", action="store_true", help="Fetch live repo stats (stars, forks, watchers, license) from GitHub")
    p_met.add_argument("--output", "-o", help="Target SVG destination path")
    p_met.set_defaults(func=cmd_metrics)

    # 11. PROGRESS
    p_prg = subparsers.add_parser("progress", help="Generate segmented sci-fi HUD progress bar")
    p_prg.add_argument("--style", choices=style_choices, default="pixel", help="Geometry style (pixel, modern, corporate)")
    p_prg.add_argument("--theme", help="Color palette theme")
    p_prg.add_argument("--mode", choices=mode_choices, default="auto", help="Theme mode: auto (default), dark, light, transparent, gh, picture")
    p_prg.add_argument("--preset", help="Named palette preset or path to JSON")
    p_prg.add_argument("--primary", help="Primary brand hex color")
    p_prg.add_argument("--accent", help="Secondary accent hex color")
    p_prg.add_argument("--value", type=int, default=75, help="Progress percentage value (0-100)")
    p_prg.add_argument("--label", default="SYSTEM PROGRESS", help="Progress bar title label")
    p_prg.add_argument("--sub", help="Subtext readout message")
    p_prg.add_argument("--output", "-o", help="Target SVG destination path")
    p_prg.set_defaults(func=cmd_progress)

    # 12. TECHSTACK
    p_tch = subparsers.add_parser("techstack", help="Generate tech stack matrix with vector pixel icons")
    p_tch.add_argument("--style", choices=style_choices, default="pixel", help="Geometry style (pixel, modern, corporate)")
    p_tch.add_argument("--theme", help="Color palette theme")
    p_tch.add_argument("--mode", choices=mode_choices, default="auto", help="Theme mode: auto (default), dark, light, transparent, gh, picture")
    p_tch.add_argument("--preset", help="Named palette preset or path to JSON")
    p_tch.add_argument("--primary", help="Primary brand hex color")
    p_tch.add_argument("--accent", help="Secondary accent hex color")
    p_tch.add_argument("--items", default="python,cpp,rust,docker,git", help="Comma-separated technology names")
    p_tch.add_argument("--columns", type=int, default=5, help="Number of columns (default: 5)")
    p_tch.add_argument("--output", "-o", help="Target SVG destination path")
    p_tch.set_defaults(func=cmd_techstack)

    # 13. TIMELINE
    p_tml = subparsers.add_parser("timeline", help="Generate vertical PCB data bus timeline")
    p_tml.add_argument("--style", choices=style_choices, default="pixel", help="Geometry style (pixel, modern, corporate)")
    p_tml.add_argument("--theme", help="Color palette theme")
    p_tml.add_argument("--mode", choices=mode_choices, default="auto", help="Theme mode: auto (default), dark, light, transparent, gh, picture")
    p_tml.add_argument("--preset", help="Named palette preset or path to JSON")
    p_tml.add_argument("--primary", help="Primary brand hex color")
    p_tml.add_argument("--accent", help="Secondary accent hex color")
    p_tml.add_argument("--output", "-o", help="Target SVG destination path")
    p_tml.set_defaults(func=cmd_timeline)

    # 14. SOCIAL (OpenGraph 1280x640)
    p_soc = subparsers.add_parser("social", help="Generate 1280x640 OpenGraph social preview card")
    p_soc.add_argument("--style", choices=style_choices, default="pixel", help="Geometry style (pixel, modern, corporate)")
    p_soc.add_argument("--theme", help="Color palette theme")
    p_soc.add_argument("--mode", choices=mode_choices, default="auto", help="Theme mode: auto (default), dark, light, transparent, gh, picture")
    p_soc.add_argument("--preset", help="Named palette preset or path to JSON")
    p_soc.add_argument("--primary", help="Primary brand hex color")
    p_soc.add_argument("--accent", help="Secondary accent hex color")
    p_soc.add_argument("--title", default="PIXEL README KIT", help="Main card title text")
    p_soc.add_argument("--subtitle", default="RETRO-FUTURISTIC HUD & SCI-FI INFOGRAPHICS FOR GITHUB READMES", help="Card subtitle / description")
    p_soc.add_argument("--repo", default="Kazinagg/pixel-readme-kit", help="GitHub repo name or author tag")
    p_soc.add_argument("--tags", help="Comma-separated tech/topic tags (e.g. 'SVG,PYTHON,CYBERPUNK,DARK-MODE')")
    p_soc.add_argument("--output", "-o", help="Target SVG destination path")
    p_soc.set_defaults(func=cmd_social)

    # 15. SERVE / STUDIO (Live Preview & Interactive HUD Studio)
    p_srv = subparsers.add_parser("serve", help="Launch live preview HTTP server with SSE reload and HUD Studio")
    p_srv.add_argument("--input", "-i", "--template", default="README.template.md", help="Input Markdown template file to watch (default: README.template.md)")
    p_srv.add_argument("--output", "-o", default=None, help="Target compiled markdown file (default: README.md)")
    p_srv.add_argument("--assets-dir", default="assets/generated", help="Folder where generated SVGs are stored")
    p_srv.add_argument("--port", "-p", type=int, default=3000, help="HTTP server port (default: 3000)")
    p_srv.add_argument("--open", action="store_true", help="Automatically open browser upon launch")
    p_srv.set_defaults(func=cmd_serve)

    p_std = subparsers.add_parser("studio", help="Alias for serve: open HUD Studio in browser")
    p_std.add_argument("--input", "-i", "--template", default="README.template.md", help="Input Markdown template file to watch (default: README.template.md)")
    p_std.add_argument("--output", "-o", default=None, help="Target compiled markdown file (default: README.md)")
    p_std.add_argument("--assets-dir", default="assets/generated", help="Folder where generated SVGs are stored")
    p_std.add_argument("--port", "-p", type=int, default=3000, help="HTTP server port (default: 3000)")
    p_std.add_argument("--open", action="store_true", default=True, help="Automatically open browser upon launch")
    p_std.set_defaults(func=cmd_serve)

    # 16. STARCHART
    p_sta = subparsers.add_parser("starchart", help="Generate vector star growth trend / activity chart")
    p_sta.add_argument("--style", choices=style_choices, default="pixel", help="Geometry style (pixel, modern, corporate)")
    p_sta.add_argument("--theme", help="Color palette theme")
    p_sta.add_argument("--mode", choices=mode_choices, default="auto", help="Theme mode: auto (default), dark, light, transparent, gh, picture")
    p_sta.add_argument("--preset", help="Named palette preset or path to JSON")
    p_sta.add_argument("--primary", help="Primary brand hex color")
    p_sta.add_argument("--accent", help="Secondary accent hex color")
    p_sta.add_argument("--repo", default="Kazinagg/pixel-readme-kit", help="GitHub repo in 'owner/repo' format")
    p_sta.add_argument("--points", default="15,65,190,480,950,1650", help="Comma-separated historical star points")
    p_sta.add_argument("--current", help="Current star count label (e.g. '1,650')")
    p_sta.add_argument("--delta", default="+78% past 6m", help="Growth delta or period indicator")
    p_sta.add_argument("--title", default="STAR GROWTH TRAJECTORY", help="Chart title text")
    p_sta.add_argument("--period", default="6M", help="Timeline period tag")
    p_sta.add_argument("--fetch-github", action="store_true", help="Fetch real star count and trajectory curve from GitHub")
    p_sta.add_argument("--output", "-o", help="Target SVG destination path")
    p_sta.set_defaults(func=cmd_starchart)

    # 17. PROFILE CARD
    p_prf = subparsers.add_parser("profile", help="Generate flagship developer profile / dossier identity header card")
    p_prf.add_argument("--style", choices=style_choices, default="pixel", help="Geometry style (pixel, modern, corporate)")
    p_prf.add_argument("--theme", help="Color palette theme")
    p_prf.add_argument("--mode", choices=mode_choices, default="auto", help="Theme mode: auto (default), dark, light, transparent, gh, picture")
    p_prf.add_argument("--preset", help="Named palette preset or path to JSON")
    p_prf.add_argument("--primary", help="Primary brand hex color")
    p_prf.add_argument("--accent", help="Secondary accent hex color")
    p_prf.add_argument("--username", help="GitHub username to fetch profile details automatically")
    p_prf.add_argument("--name", default="ALEX DEVELOPER", help="Developer display name")
    p_prf.add_argument("--role", default="FULLSTACK & SYSTEMS ARCHITECT", help="Engineering role / specialty headline")
    p_prf.add_argument("--bio", default="Building high-performance runtimes and resilient developer tooling.", help="Bio or manifesto summary")
    p_prf.add_argument("--status", default="AVAILABLE FOR HIRE", help="Availability status")
    p_prf.add_argument("--location", default="REMOTE // UTC+3", help="Location indicator")
    p_prf.add_argument("--badge", default="LEVEL_99", help="Rank / experience badge")
    p_prf.add_argument("--fetch-github", action="store_true", help="Fetch bio, name, location and repos count from GitHub API")
    p_prf.add_argument("--output", "-o", help="Target SVG destination path")
    p_prf.set_defaults(func=cmd_profile)

    return parser

def main():
    parser = build_parser()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
