"""
Data models representing color tokens, palettes, and themes for Pixel Readme Kit.
"""

from dataclasses import dataclass, field, asdict
from typing import Dict, Any, Optional


@dataclass
class ModePalette:
    """Represents a specific display mode palette (dark or light)."""
    bg: str
    panel: str
    border: str
    primary: str
    accent: str
    tertiary: str
    title_front: str
    title_mid: str
    title_dark: str
    text_main: str
    text_dim: str
    success: str
    warning: str
    grid_op: str = "0.08"

    def to_dict(self) -> Dict[str, str]:
        return asdict(self)


@dataclass
class ThemeDefinition:
    """Represents a complete theme with dark and light adaptive palettes."""
    slug: str
    name: str
    dark: Dict[str, Any]
    light: Dict[str, Any]
    description: str = ""
    is_custom: bool = False
    aliases: list = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "slug": self.slug,
            "name": self.name,
            "dark": dict(self.dark),
            "light": dict(self.light),
            "description": self.description,
            "is_custom": self.is_custom,
            "aliases": list(self.aliases),
        }

    def get_palette(self, mode: str = "dark") -> Dict[str, Any]:
        """Returns the dictionary for mode 'dark' or 'light'."""
        if mode == "light":
            return dict(self.light)
        return dict(self.dark)
