"""
Theme Creator and Color Harmonizer for Pixel Readme Kit.
Enables algorithmic creation of balanced HUD palettes from a brand primary color
and saving customized presets directly to presets/*.json.
"""

import os
import json
import re
from typing import Dict, Any, Optional
from generator.themes.color_utils import (
    hex_to_hsl,
    hsl_to_hex,
    darken_hex,
    lighten_hex,
    is_light_color,
    hex_to_rgb,
    rgb_to_hex,
)


def slugify(name: str) -> str:
    """Converts a theme name into a safe file slug (e.g., 'Cyber Neon' -> 'cyber-neon')."""
    s = str(name).strip().lower()
    s = re.sub(r'[^a-z0-9_\-]+', '-', s)
    s = re.sub(r'-+', '-', s)
    return s.strip('-') or 'custom-theme'


class ThemeCreator:
    """Algorithmic builder and exporter for Pixel Readme Kit themes."""

    def __init__(self, presets_dir: Optional[str] = None):
        if presets_dir:
            self.presets_dir = presets_dir
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            cand_pkg = os.path.abspath(os.path.join(base_dir, "..", "presets"))
            cand_root = os.path.abspath(os.path.join(base_dir, "..", "..", "presets"))
            if os.path.isdir(cand_pkg):
                self.presets_dir = cand_pkg
            elif os.path.isdir(cand_root):
                self.presets_dir = cand_root
            else:
                self.presets_dir = cand_pkg

    def generate_theme(
        self,
        primary_hex: str,
        name: str = "Custom Theme",
        accent_strategy: str = "triadic",
        theme_type: str = "cyberpunk",
    ) -> Dict[str, Any]:
        """
        Derives a harmonious palette from a primary brand color.
        accent_strategy options: 'triadic' (+120°/+240°), 'complementary' (+180°), 'analogous' (+30°/-30°).
        """
        prim = primary_hex.strip()
        h, s, l = hex_to_hsl(prim)

        if accent_strategy == "complementary":
            acc_h = (h + 180.0) % 360.0
            tert_h = (h + 90.0) % 360.0
        elif accent_strategy == "analogous":
            acc_h = (h + 35.0) % 360.0
            tert_h = (h - 35.0) % 360.0
        else:  # 'triadic'
            acc_h = (h + 120.0) % 360.0
            tert_h = (h + 240.0) % 360.0

        accent = hsl_to_hex(acc_h, max(0.65, s), max(0.45, min(0.65, l)))
        tertiary = hsl_to_hex(tert_h, max(0.70, s), max(0.50, min(0.60, l)))

        # Tinted glass backgrounds
        r_tint, g_tint, b_tint = hex_to_rgb(prim)
        bg_glass = f"rgba({max(8, int(r_tint * 0.08))}, {max(12, int(g_tint * 0.08))}, {max(20, int(b_tint * 0.12))}, 0.82)"
        border_subtle = f"rgba({max(25, int(r_tint * 0.20))}, {max(35, int(g_tint * 0.20))}, {max(55, int(b_tint * 0.30))}, 0.85)"

        slug = slugify(name)
        preset_dict = {
            "theme": slug,
            "name": name,
            "primary": prim,
            "secondary": accent,
            "accent": tertiary,
            "success": "#00D26A",
            "warning": "#F59E0B",
            "bg_glass": bg_glass,
            "border_subtle": border_subtle,
        }

        # Build complete adaptive dark/light dictionaries
        dark_palette = {
            "bg": bg_glass,
            "panel": f"rgba(15, 23, 38, 0.82)",
            "border": border_subtle,
            "primary": prim,
            "accent": accent,
            "tertiary": tertiary,
            "title_front": prim,
            "title_mid": darken_hex(prim, 0.45),
            "title_dark": darken_hex(prim, 0.15),
            "text_main": "#F8F8F2",
            "text_dim": "#94A3B8",
            "success": "#00D26A",
            "warning": "#F59E0B",
            "grid_op": "0.08",
        }

        light_prim = darken_hex(prim, 0.7) if is_light_color(prim) else prim
        light_palette = {
            "bg": "#F6F8FA",
            "panel": "#EAEFF5",
            "border": "#D0D7DE",
            "primary": light_prim,
            "accent": darken_hex(accent, 0.7) if is_light_color(accent) else accent,
            "tertiary": darken_hex(tertiary, 0.7) if is_light_color(tertiary) else tertiary,
            "title_front": light_prim,
            "title_mid": darken_hex(light_prim, 0.6),
            "title_dark": darken_hex(light_prim, 0.3),
            "text_main": "#1F2328",
            "text_dim": "#57606A",
            "success": "#1A7F37",
            "warning": "#9A6700",
            "grid_op": "0.10",
        }

        return {
            "preset": preset_dict,
            "dark": dark_palette,
            "light": light_palette,
        }

    def save_preset(self, name_or_slug: str, preset_dict: Dict[str, Any]) -> str:
        """Saves preset definition to presets/{slug}.json."""
        slug = slugify(name_or_slug)
        os.makedirs(self.presets_dir, exist_ok=True)
        target_path = os.path.join(self.presets_dir, f"{slug}.json")

        # Standardize structure
        clean_dict = {
            "theme": slug,
            "name": preset_dict.get("name", slug),
            "style": preset_dict.get("style", "pixel"),
            "primary": preset_dict.get("primary", "#00C8D7"),
            "secondary": preset_dict.get("secondary") or preset_dict.get("accent", "#A855F7"),
            "accent": preset_dict.get("accent") or preset_dict.get("tertiary", "#FF0055"),
            "success": preset_dict.get("success", "#00D26A"),
            "warning": preset_dict.get("warning", "#F59E0B"),
            "bg_glass": preset_dict.get("bg_glass", "rgba(10, 14, 23, 0.75)"),
            "border_subtle": preset_dict.get("border_subtle", "rgba(30, 41, 59, 0.85)"),
        }

        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(clean_dict, f, indent=2, ensure_ascii=False)

        return target_path


# Default singleton instance
theme_creator = ThemeCreator()
