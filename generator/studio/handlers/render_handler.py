"""
Render request handler for HUD Studio /api/render endpoint.
Generates dynamic SVGs on the fly based on query parameters.
"""

from typing import Dict, Any
from generator.components.base import validate_svg
from generator.compiler import fetch_github_stat
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
)
from generator.themes import normalize_style_and_theme


def handle_render_request(handler, query: Dict[str, list]) -> None:
    """Dispatches /api/render query parameters to appropriate SVG generator."""
    btype = query.get("block_type", ["header"])[0].lower()
    raw_style = query.get("style", ["cyberpunk"])[0]
    raw_theme = query.get("theme", [None])[0] or None
    style, theme = normalize_style_and_theme(style=raw_style, theme=raw_theme)
    mode = query.get("mode", ["auto"])[0]
    preset = query.get("preset", [None])[0] or None
    primary = query.get("primary", [None])[0] or None
    accent = query.get("accent", [None])[0] or None
    tertiary = query.get("tertiary", [None])[0] or None

    title = query.get("title", [None])[0]
    subtitle = query.get("subtitle", [None])[0]
    tag = query.get("tag", [None])[0]
    compact = query.get("compact", ["false"])[0].lower() in ("true", "1", "yes")

    spec1 = query.get("spec1", [None])[0] or None
    spec2 = query.get("spec2", [None])[0] or None
    spec3 = query.get("spec3", [None])[0] or None
    specs = query.get("specs", [None])[0] or None
    tag_url = query.get("tag_url", [None])[0] or None
    close_url = query.get("close_url", [None])[0] or None

    chip_type = query.get("chip_type", [None])[0] or query.get("type", ["closed"])[0]
    decay_dir = query.get("decay_dir", [None])[0] or query.get("direction", ["right"])[0]
    gh_stat = query.get("github", [None])[0] or query.get("gh", [None])[0]
    repo = query.get("repo", [None])[0]
    width_str = query.get("width", [None])[0]
    width_val = int(width_str) if width_str and width_str.isdigit() else None

    items = query.get("items", [None])[0]
    body = query.get("body", [None])[0]
    delta = query.get("delta", [None])[0]
    status = query.get("status", [None])[0]
    trend = query.get("trend", [None])[0]

    value_str = query.get("value", [None])[0] or tag
    cols_str = query.get("columns", [None])[0]
    cols_val = int(cols_str) if cols_str and cols_str.isdigit() else (int(tag) if tag and tag.isdigit() else 5)

    callout_type = query.get("callout_type", [None])[0] or query.get("type", ["note"])[0]
    badge_color = query.get("badge_color", [None])[0] or None
    is_quote = query.get("quote", ["false"])[0].lower() in ("true", "1", "yes")
    frame_type = query.get("frame_type", [None])[0] or query.get("type", ["top"])[0]
    badge = query.get("badge", ["NOTE"])[0]
    label = query.get("label", [None])[0] or title or "[SUB_MODULE]"
    sub_text = query.get("sub", [None])[0] or subtitle
    nav_text = query.get("nav", [None])[0] or tag or "RETURN TO TOP"
    tags_str = query.get("tags", [None])[0] or tag or "PYTHON,SVG"

    try:
        if btype == "header":
            svg = generate_header(
                style=style, theme=theme, mode=mode, preset=preset, primary=primary, accent=accent, tertiary=tertiary,
                title=title or "PIXEL-KIT", subtitle=subtitle or "TRANSLUCENT HUD SYSTEM",
                tag=tag or "SYSTEM_ACTIVE", spec1=spec1, spec2=spec2, spec3=spec3, specs=specs,
                tag_url=tag_url, close_url=close_url, compact=compact
            )
        elif btype == "footer":
            svg = generate_footer(
                style=style, theme=theme, mode=mode, preset=preset, primary=primary, accent=accent, tertiary=tertiary,
                status=status or title or "SESSION_ACTIVE // STANDBY",
                nav_text=nav_text, sub_text=sub_text
            )
        elif btype in ("callout", "quote"):
            q_badge = badge if btype == "quote" else callout_type
            svg = generate_callout(
                style=style, theme=theme, mode=mode, preset=preset, primary=primary, accent=accent,
                callout_type=q_badge, title=title or "SYSTEM NOTICE",
                subtitle=subtitle or "", is_quote=(btype == "quote" or is_quote),
                badge_color=badge_color
            )
        elif btype in ("frame", "window", "terminal"):
            f_title = title or ("HUD.TERMINAL" if btype == "terminal" else "SYSTEM.CORE")
            if btype == "terminal":
                f_title = f"╔═ {f_title} // RUNTIME.SYS"
            svg = generate_frame(
                style=style, theme=theme, mode=mode, preset=preset, primary=primary, accent=accent, tertiary=tertiary,
                frame_type=frame_type, title=f_title,
                tag=tag or "[OPEN_HUD]", tag_url=tag_url, close_url=close_url
            )
        elif btype == "chip":
            text_val = title or "CHIP"
            if gh_stat:
                repo_name = repo or "Kazinagg/pixel-readme-kit"
                stat_text, _ = fetch_github_stat(repo_name, gh_stat)
                text_val = stat_text
            svg = generate_chip(
                style=style, theme=theme, mode=mode, preset=preset, primary=primary, accent=accent,
                chip_type=chip_type, text=text_val, width=width_val, decay_dir=decay_dir
            )
        elif btype == "divider":
            svg = generate_divider(style=style, theme=theme, mode=mode, preset=preset, primary=primary, accent=accent)
        elif btype == "splitter":
            svg = generate_splitter(style=style, theme=theme, mode=mode, preset=preset, primary=primary, accent=accent, label=label)
        elif btype == "metrics":
            cards = []
            raw_items = items or body or query.get("metrics", [None])[0] or query.get("cards", [None])[0]
            if raw_items:
                for line in raw_items.splitlines() if "\n" in raw_items else raw_items.split("|"):
                    item = line.strip()
                    if not item:
                        continue
                    if item.startswith("-"): item = item[1:].strip()
                    if item.startswith("milestone") or item.startswith("card"):
                        parts = item.split()
                        card_dict = {}
                        for p in parts[1:]:
                            if "=" in p:
                                k, v = p.split("=", 1)
                                card_dict[k] = v.strip('"\'')
                        if card_dict:
                            cards.append(card_dict)
                    elif ":" in item:
                        parts = item.split(":", 1)
                        cards.append({"label": parts[0].strip(), "value": parts[1].strip()})
                    else:
                        cards.append({"label": "METRIC", "value": item})
            svg = generate_metrics(cards=cards if cards else None, style=style, theme=theme, mode=mode, preset=preset, primary=primary, accent=accent)
        elif btype == "progress":
            val_int = int(value_str) if value_str and value_str.isdigit() else 75
            svg = generate_progress(value=val_int, label=title or label or "PROGRESS", sub=sub_text, style=style, theme=theme, mode=mode, preset=preset, primary=primary, accent=accent)
        elif btype == "techstack":
            item_list = [x.strip() for x in (items or subtitle or "python,cpp,docker,git").split(",") if x.strip()]
            svg = generate_techstack(items=item_list, columns=cols_val, style=style, theme=theme, mode=mode, preset=preset, primary=primary, accent=accent)
        elif btype == "timeline":
            from generator.compiler import parse_directive_attrs
            timeline_items = []
            raw_lines = (body or items or "").splitlines()
            for line in raw_lines:
                line = line.strip()
                if not line:
                    continue
                if line.startswith("-"): line = line[1:].strip()
                for prefix in ("milestone", "stage", "item"):
                    if line.lower().startswith(prefix):
                        line = line[len(prefix):].strip()
                        break
                item_attrs = parse_directive_attrs(line)
                if item_attrs:
                    timeline_items.append(item_attrs)
            svg = generate_timeline(items=timeline_items if timeline_items else None, style=style, theme=theme, mode=mode, preset=preset, primary=primary, accent=accent)
        elif btype == "social":
            tag_list = [x.strip() for x in tags_str.split(",") if x.strip()]
            svg = generate_social(title=title or "PIXEL README KIT", subtitle=subtitle or "HUD SYSTEM", repo=repo or "Kazinagg/pixel-readme-kit", tags=tag_list, style=style, theme=theme, mode=mode, preset=preset, primary=primary, accent=accent)
        elif btype == "starchart":
            pts = query.get("points", [None])[0]
            cur = query.get("current", [None])[0]
            dlt = query.get("delta", ["+78% past 6m"])[0]
            ttl = title or query.get("title", ["STAR GROWTH TRAJECTORY"])[0]
            per = query.get("period", ["6M"])[0]
            rep = repo or query.get("repo", ["Kazinagg/pixel-readme-kit"])[0]
            svg = generate_starchart(
                style=style, theme=theme, mode=mode, preset=preset, primary=primary, accent=accent,
                repo=rep, points=pts, current=cur, delta=dlt, title=ttl, period=per
            )
        elif btype == "profile":
            p_name = query.get("name", [title or "ALEX DEVELOPER"])[0]
            p_role = query.get("role", [subtitle or "FULLSTACK & SYSTEMS ARCHITECT"])[0]
            p_bio = query.get("bio", ["Building high-performance runtimes and resilient developer tooling."])[0]
            p_stat = query.get("status", ["AVAILABLE FOR HIRE"])[0]
            p_loc = query.get("location", ["REMOTE // UTC+3"])[0]
            p_bdg = tag or query.get("badge", ["LEVEL_99"])[0]
            svg = generate_profile_card(
                style=style, theme=theme, mode=mode, preset=preset, primary=primary, accent=accent,
                name=p_name, role=p_role, bio=p_bio, status=p_stat, location=p_loc, badge=p_bdg
            )
        else:
            handler.send_error(400, f"Unsupported block type: {btype}")
            return

        validate_svg(svg)
        handler.send_response(200)
        handler.send_header("Content-Type", "image/svg+xml; charset=utf-8")
        handler.send_header("Cache-Control", "no-cache, no-store, must-revalidate, max-age=0")
        handler.end_headers()
        handler.wfile.write(svg.encode("utf-8"))
    except Exception as e:
        handler.send_error(500, f"Render error: {e}")


def handle_github_fetch(handler, query):
    """Handles GET /api/github/fetch?repo=owner/repo or ?user=username for live data preview."""
    import json
    from generator.github_api import fetch_repo_data, fetch_user_data, fetch_star_trajectory

    repo = query.get("repo", [None])[0]
    user = query.get("user", [None])[0]

    resp = {"status": "success"}
    if repo:
        rdata, rerr = fetch_repo_data(repo)
        traj, _ = fetch_star_trajectory(repo)
        resp["repo"] = rdata
        resp["trajectory"] = traj
        if rerr:
            resp["repo_error"] = rerr

    if user:
        udata, uerr = fetch_user_data(user)
        resp["user"] = udata
        if uerr:
            resp["user_error"] = uerr

    handler.send_response(200)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Cache-Control", "no-cache, no-store, must-revalidate, max-age=0")
    handler.end_headers()
    handler.wfile.write(json.dumps(resp).encode("utf-8"))

