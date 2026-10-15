"""
Theme API handler for HUD Studio.
Handles listing presets, querying active design tokens, and creating/saving custom themes.
"""

import json
from typing import Dict, Any
from generator.themes import theme_registry, theme_creator, BASE_THEME_PALETTES, VALID_STYLES, CANONICAL_THEMES
from generator.icons import list_available_icons


def handle_presets_list(handler) -> None:
    """GET /api/presets - Lists available presets and icons."""
    data = {
        "presets": theme_registry.list_presets(),
        "icons": list_available_icons(),
    }
    handler.send_response(200)
    handler.send_header("Content-Type", "application/json")
    handler.end_headers()
    handler.wfile.write(json.dumps(data).encode("utf-8"))


def handle_themes_list(handler) -> None:
    """GET /api/themes - Full dictionary of available themes with dark/light tokens and style mapping."""
    data = {
        "themes": theme_registry.theme_palettes,
        "presets": theme_registry.list_presets(),
        "styles": [s for s in VALID_STYLES if s != "corporate"],
        "style_themes": {s: theme_registry.get_canonical_themes_for_style(s) for s in VALID_STYLES},
        "all_style_themes": {s: theme_registry.get_themes_for_style(s) for s in VALID_STYLES},
        "canonical_themes": list(CANONICAL_THEMES),
        "theme_presets": {t: theme_registry.get_presets_for_theme(t) for t in CANONICAL_THEMES},
    }
    handler.send_response(200)
    handler.send_header("Content-Type", "application/json")
    handler.end_headers()
    handler.wfile.write(json.dumps(data).encode("utf-8"))


def handle_theme_generate(handler, body: Dict[str, Any]) -> None:
    """POST /api/themes/generate - Derives harmonious palette from a primary color."""
    prim = body.get("primary", "#00C8D7")
    name = body.get("name", "Custom Theme")
    strategy = body.get("strategy", "triadic")

    result = theme_creator.generate_theme(
        primary_hex=prim,
        name=name,
        accent_strategy=strategy,
    )
    handler.send_response(200)
    handler.send_header("Content-Type", "application/json")
    handler.end_headers()
    handler.wfile.write(json.dumps({"status": "success", "theme": result}).encode("utf-8"))


def handle_theme_save(handler, body: Dict[str, Any]) -> None:
    """POST /api/themes/save - Saves custom preset to presets/{slug}.json."""
    slug = body.get("slug") or body.get("name") or "custom-theme"
    preset_data = body.get("preset") or body

    path = theme_creator.save_preset(slug, preset_data)
    # Refresh registry
    theme_registry._palettes[slug] = {
        "dark": preset_data.get("dark", {}),
        "light": preset_data.get("light", {}),
    }

    handler.send_response(200)
    handler.send_header("Content-Type", "application/json")
    handler.end_headers()
    handler.wfile.write(json.dumps({
        "status": "saved",
        "slug": slug,
        "path": path,
        "presets": theme_registry.list_presets()
    }).encode("utf-8"))
