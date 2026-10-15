"""
Pixel Vector Icon Repository for Pixel Readme Kit v4.0.
Contains clean, lightweight, 16x16 / 20x20 pixel-perfect SVG path definitions
for popular developer technologies, programming languages, and tools.
"""

# Normalized viewBox="0 0 20 20"
ICONS_20x20 = {
    "python": (
        '<path d="M10 2C6.5 2 6.5 3.5 6.5 3.5V5H10.5V6H4.5C3 6 3 8 3 8V11C3 12.5 4.5 12.5 4.5 12.5H6V11C6 9.5 7.5 9.5 7.5 9.5H11.5C13 9.5 13 8 13 8V5C13 3.5 11.5 2 10 2ZM8 3.5C8.4 3.5 8.7 3.8 8.7 4.2C8.7 4.6 8.4 4.9 8 4.9C7.6 4.9 7.3 4.6 7.3 4.2C7.3 3.8 7.6 3.5 8 3.5Z" fill="currentColor"/>'
        '<path d="M10 18C13.5 18 13.5 16.5 13.5 16.5V15H9.5V14H15.5C17 14 17 12 17 12V9C17 7.5 15.5 7.5 15.5 7.5H14V9C14 10.5 12.5 10.5 12.5 10.5H8.5C7 10.5 7 12 7 12V15C7 16.5 8.5 18 10 18ZM12 16.5C11.6 16.5 11.3 16.2 11.3 15.8C11.3 15.4 11.6 15.1 12 15.1C12.4 15.1 12.7 15.4 12.7 15.8C12.7 16.2 12.4 16.5 12 16.5Z" fill="currentColor"/>'
    ),
    "cpp": (
        '<path d="M3 6L8 3L8 6L5 8L5 12L8 14L8 17L3 14Z" fill="currentColor"/>'
        '<rect x="9" y="8" width="2" height="4" fill="currentColor"/>'
        '<rect x="8" y="9" width="4" height="2" fill="currentColor"/>'
        '<rect x="14" y="8" width="2" height="4" fill="currentColor"/>'
        '<rect x="13" y="9" width="4" height="2" fill="currentColor"/>'
    ),
    "c": (
        '<path d="M15 5L7 5C4.8 5 3 6.8 3 9L3 11C3 13.2 4.8 15 7 15L15 15L15 12L7 12C6.4 12 6 11.6 6 11L6 9C6 8.4 6.4 8 7 8L15 8Z" fill="currentColor"/>'
    ),
    "rust": (
        '<circle cx="10" cy="10" r="7" stroke="currentColor" stroke-width="2" fill="none"/>'
        '<path d="M7 7H11C12.5 7 13 8 13 9C13 10 12.2 10.5 11 10.5L13 13H11L9.5 11H8.5V13H7V7ZM8.5 8.2V9.8H10.5C11.2 9.8 11.5 9.5 11.5 9C11.5 8.5 11.2 8.2 10.5 8.2H8.5Z" fill="currentColor"/>'
    ),
    "go": (
        '<path d="M3 8C3 6.5 4.5 5 7 5C9 5 10 6 10 7L8 7C8 6.5 7.5 6 7 6C5.5 6 4.5 7 4.5 8C4.5 9 5.5 10 7 10C8 10 8.5 9.5 8.5 9L7 9V8H10V10C9.5 11 8.5 11.5 7 11.5C4.5 11.5 3 10 3 8Z" fill="currentColor"/>'
        '<path d="M11 8C11 6.5 12.5 5 15 5C17.5 5 19 6.5 19 8C19 9.5 17.5 11 15 11C12.5 11 11 9.5 11 8ZM17.5 8C17.5 7 16.5 6 15 6C13.5 6 12.5 7 12.5 8C12.5 9 13.5 10 15 10C16.5 10 17.5 9 17.5 8Z" fill="currentColor"/>'
    ),
    "js": (
        '<rect x="3" y="3" width="14" height="14" rx="2" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="1.5"/>'
        '<path d="M8 10V13C8 14 7 14 6 13.5L5.5 14.5C6.5 15.2 8.5 15.2 9.5 14C10 13.2 9.8 11 9.8 10H8ZM11 14C12 14.5 13 14.7 14 14C14.8 13.5 14.8 12.5 14 12C13.2 11.5 12 11.2 12 10.5C12 10 12.5 9.5 13.2 9.5C14 9.5 14.5 9.8 15 10.2L15.5 9.2C14.8 8.7 14 8.5 13.2 8.5C11.8 8.5 10.8 9.5 10.8 10.5C10.8 11.8 12 12.2 12.8 12.6C13.5 13 13.5 13.5 13 13.8C12.5 14.1 11.8 13.8 11.3 13.2L11 14Z" fill="currentColor"/>'
    ),
    "ts": (
        '<rect x="3" y="3" width="14" height="14" rx="2" fill="currentColor" fill-opacity="0.2" stroke="currentColor" stroke-width="1.5"/>'
        '<path d="M6 7H11V8.5H9.3V14H7.7V8.5H6V7ZM12 14C13 14.5 14 14.7 15 14C15.8 13.5 15.8 12.5 15 12C14.2 11.5 13 11.2 13 10.5C13 10 13.5 9.5 14.2 9.5C15 9.5 15.5 9.8 16 10.2L16.5 9.2C15.8 8.7 15 8.5 14.2 8.5C12.8 8.5 11.8 9.5 11.8 10.5C11.8 11.8 13 12.2 13.8 12.6C14.5 13 14.5 13.5 14 13.8C13.5 14.1 12.8 13.8 12.3 13.2L12 14Z" fill="currentColor"/>'
    ),
    "docker": (
        '<rect x="4" y="9" width="2" height="2" fill="currentColor"/>'
        '<rect x="7" y="9" width="2" height="2" fill="currentColor"/>'
        '<rect x="10" y="9" width="2" height="2" fill="currentColor"/>'
        '<rect x="7" y="6" width="2" height="2" fill="currentColor"/>'
        '<rect x="10" y="6" width="2" height="2" fill="currentColor"/>'
        '<path d="M2 12C3 15 6 16 10 16C15 16 18 14 18 12C16 11.5 14 12 12 12C12 11 10 11 8 12C5 12 3 11.5 2 12Z" fill="currentColor"/>'
    ),
    "git": (
        '<path d="M17.5 9.2L10.8 2.5C10.4 2.1 9.6 2.1 9.2 2.5L2.5 9.2C2.1 9.6 2.1 10.4 2.5 10.8L9.2 17.5C9.6 17.9 10.4 17.9 10.8 17.5L17.5 10.8C17.9 10.4 17.9 9.6 17.5 9.2ZM9.5 14.2C8.7 14.2 8.2 13.6 8.2 13C8.2 12.6 8.4 12.2 8.7 12V8.5L7.5 9.7C7.4 10.2 7 10.5 6.5 10.5C5.7 10.5 5.2 10 5.2 9.2C5.2 8.5 5.7 8 6.5 8C6.9 8 7.2 8.2 7.4 8.4L9.2 6.6V5.8C8.9 5.6 8.7 5.2 8.7 4.8C8.7 4 9.3 3.5 10 3.5C10.7 3.5 11.3 4 11.3 4.8C11.3 5.2 11.1 5.6 10.8 5.8V12C11.1 12.2 11.3 12.6 11.3 13C11.3 13.6 10.8 14.2 9.5 14.2Z" fill="currentColor"/>'
    ),
    "linux": (
        '<ellipse cx="10" cy="9" rx="4" ry="5" fill="currentColor" fill-opacity="0.3"/>'
        '<circle cx="8.5" cy="7" r="0.8" fill="currentColor"/>'
        '<circle cx="11.5" cy="7" r="0.8" fill="currentColor"/>'
        '<polygon points="9,9 11,9 10,10.5" fill="currentColor"/>'
        '<ellipse cx="6" cy="15" rx="2" ry="1" fill="currentColor"/>'
        '<ellipse cx="14" cy="15" rx="2" ry="1" fill="currentColor"/>'
    ),
    "opengl": (
        '<polygon points="10,3 17,7 17,14 10,18 3,14 3,7" fill="none" stroke="currentColor" stroke-width="1.5"/>'
        '<polygon points="10,6 14,8.5 14,12.5 10,15 6,12.5 6,8.5" fill="currentColor" fill-opacity="0.3"/>'
    ),
    "delphi": (
        '<rect x="4" y="4" width="12" height="12" rx="1" fill="none" stroke="currentColor" stroke-width="1.5"/>'
        '<path d="M7 6H10.5C12.5 6 13.5 7.5 13.5 10C13.5 12.5 12.5 14 10.5 14H7V6ZM8.5 7.5V12.5H10.2C11.4 12.5 12 11.5 12 10C12 8.5 11.4 7.5 10.2 7.5H8.5Z" fill="currentColor"/>'
    ),
    "react": (
        '<ellipse cx="10" cy="10" rx="8" ry="3" fill="none" stroke="currentColor" stroke-width="1.2"/>'
        '<ellipse cx="10" cy="10" rx="8" ry="3" transform="rotate(60 10 10)" fill="none" stroke="currentColor" stroke-width="1.2"/>'
        '<ellipse cx="10" cy="10" rx="8" ry="3" transform="rotate(120 10 10)" fill="none" stroke="currentColor" stroke-width="1.2"/>'
        '<circle cx="10" cy="10" r="1.5" fill="currentColor"/>'
    ),
    "database": (
        '<ellipse cx="10" cy="5" rx="6" ry="2" fill="none" stroke="currentColor" stroke-width="1.5"/>'
        '<path d="M4 5V10C4 11 6.7 12 10 12C13.3 12 16 11 16 10V5" fill="none" stroke="currentColor" stroke-width="1.5"/>'
        '<path d="M4 10V15C4 16 6.7 17 10 17C13.3 17 16 16 16 15V10" fill="none" stroke="currentColor" stroke-width="1.5"/>'
    ),
    "terminal": (
        '<rect x="3" y="4" width="14" height="12" rx="1.5" fill="none" stroke="currentColor" stroke-width="1.5"/>'
        '<path d="M6 7.5L8.5 10L6 12.5" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>'
        '<line x1="10" y1="12.5" x2="13" y2="12.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>'
    ),
    "cpu": (
        '<rect x="5" y="5" width="10" height="10" rx="1" fill="none" stroke="currentColor" stroke-width="1.5"/>'
        '<rect x="8" y="8" width="4" height="4" fill="currentColor"/>'
        '<path d="M7 2V5M10 2V5M13 2V5M7 15V18M10 15V18M13 15V18M2 7H5M2 10H5M2 13H5M15 7H18M15 10H18M15 13H18" stroke="currentColor" stroke-width="1.2"/>'
    ),
    "generic": (
        '<rect x="4" y="4" width="12" height="12" fill="none" stroke="currentColor" stroke-width="1.5"/>'
        '<circle cx="10" cy="10" r="2.5" fill="currentColor"/>'
        '<path d="M4 4L16 16M16 4L4 16" stroke="currentColor" stroke-width="0.8" stroke-dasharray="2,2"/>'
    )
}

ALIASES = {
    "c++": "cpp",
    "c#": "generic",
    "csharp": "generic",
    "javascript": "js",
    "typescript": "ts",
    "py": "python",
    "golang": "go",
    "rs": "rust",
    "sh": "terminal",
    "bash": "terminal",
    "zsh": "terminal",
    "shell": "terminal",
    "sql": "database",
    "postgres": "database",
    "postgresql": "database",
    "mysql": "database",
    "sqlite": "database",
    "gl": "opengl",
    "pascal": "delphi",
    "k8s": "docker",
    "kubernetes": "docker",
    "hardware": "cpu",
    "embedded": "cpu"
}

def get_icon(name: str):
    """Returns SVG snippet for a given technology name, or None if unknown."""
    clean = str(name).strip().lower()
    key = ALIASES.get(clean, clean)
    return ICONS_20x20.get(key, None)

def list_available_icons() -> list:
    """Returns sorted list of registered icon names and aliases."""
    names = set(ICONS_20x20.keys()) | set(ALIASES.keys())
    return sorted(list(names))

def get_tech_icon_svg(name: str) -> str:
    """Returns SVG snippet for a given technology name, fallback to generic."""
    icon = get_icon(name)
    return icon if icon is not None else ICONS_20x20["generic"]
