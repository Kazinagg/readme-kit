"""
Project Scaffolder for Readme Kit v5.0
Generates initial README.template.md from predefined templates:

Repositories (repo/):
- library (or repo-library): Open Source libraries and packages
- cli (or repo-cli): Command-line utilities and system tools
- study (or repo-study): Laboratory reports and academic work
- minimal (or repo-minimal): Clean corporate and minimal repository

Profiles (profile/):
- developer (or profile-developer): Comprehensive developer profile (username/username)
- minimal (or profile-minimal): Clean minimalist developer profile
- cyberpunk (or profile-cyberpunk): Futuristic HUD / cyber developer profile
"""

import os
import re

TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")

TEMPLATE_REGISTRY = {
    # Repositories
    "repo/library": os.path.join("repo", "library.template.md"),
    "repo/cli": os.path.join("repo", "cli.template.md"),
    "repo/study": os.path.join("repo", "study.template.md"),
    "repo/minimal": os.path.join("repo", "minimal.template.md"),
    "repo/modern": os.path.join("repo", "modern.template.md"),
    "repo/sketch": os.path.join("repo", "sketch.template.md"),
    # Profiles
    "profile/developer": os.path.join("profile", "developer.template.md"),
    "profile/minimal": os.path.join("profile", "minimal.template.md"),
    "profile/cyberpunk": os.path.join("profile", "cyberpunk.template.md"),
    "profile/modern": os.path.join("profile", "modern.template.md"),
    "profile/sketch": os.path.join("profile", "sketch.template.md"),
}

# Aliases for convenience and backward compatibility
ALIASES = {
    # Legacy aliases
    "library": "repo/library",
    "cli": "repo/cli",
    "study": "repo/study",
    "minimal": "repo/minimal",
    "modern": "repo/modern",
    "sketch": "repo/sketch",
    # Dash-separated aliases
    "repo-library": "repo/library",
    "repo-cli": "repo/cli",
    "repo-study": "repo/study",
    "repo-minimal": "repo/minimal",
    "repo-modern": "repo/modern",
    "repo-sketch": "repo/sketch",
    "profile": "profile/developer",
    "profile-developer": "profile/developer",
    "profile-minimal": "profile/minimal",
    "profile-cyberpunk": "profile/cyberpunk",
    "profile-modern": "profile/modern",
    "profile-sketch": "profile/sketch",
}

def get_available_templates(category=None):
    """
    Returns a list of available template identifiers.
    If category is 'repo' or 'profile', filters templates by that category.
    """
    keys = list(TEMPLATE_REGISTRY.keys())
    if category:
        cat_prefix = f"{category.lower().strip()}/"
        return [k for k in keys if k.startswith(cat_prefix)]
    return keys + list(ALIASES.keys())

def resolve_template_path(template_name: str) -> str:
    """
    Resolves the absolute filepath for a given template name or alias.
    """
    normalized = template_name.lower().strip().replace("\\", "/")
    resolved_key = ALIASES.get(normalized, normalized)

    if resolved_key in TEMPLATE_REGISTRY:
        rel_path = TEMPLATE_REGISTRY[resolved_key]
        full_path = os.path.join(TEMPLATE_DIR, rel_path)
        if os.path.exists(full_path):
            return full_path

    # Direct filename check in TEMPLATE_DIR or subdirs
    cand1 = os.path.join(TEMPLATE_DIR, f"{normalized}.template.md")
    if os.path.exists(cand1):
        return cand1

    cand2 = os.path.join(TEMPLATE_DIR, "repo", f"{normalized}.template.md")
    if os.path.exists(cand2):
        return cand2

    cand3 = os.path.join(TEMPLATE_DIR, "profile", f"{normalized}.template.md")
    if os.path.exists(cand3):
        return cand3

    raise ValueError(
        f"Unknown template type '{template_name}'. "
        f"Available: {sorted(list(TEMPLATE_REGISTRY.keys()) + ['library', 'cli', 'study'])}"
    )

from generator.themes import normalize_style_and_theme

def scaffold_readme(
    project_type="library",
    category=None,
    title="MY PROJECT",
    subtitle=None,
    author="DEVELOPER",
    group="SE-01",
    discipline="COMPUTER SCIENCE",
    repo=None,
    style="pixel",
    theme=None,
    output_path="README.template.md"
) -> str:
    """
    Creates a customized README.template.md from a built-in template.
    Supports both Repositories (repo/*) and Profiles (profile/*).
    """
    ptype = project_type.lower().strip()
    if category and "/" not in ptype and not ptype.startswith(f"{category}/"):
        ptype = f"{category}/{ptype}"

    tpl_path = resolve_template_path(ptype)

    with open(tpl_path, "r", encoding="utf-8") as f:
        content = f.read()

    slug = re.sub(r'[^a-zA-Z0-9_\-]+', '-', title.lower()).strip('-') or "my-project"
    repo_val = repo if repo else f"username/{slug}"
    sub_val = subtitle if subtitle else f"{title.upper()} // SYSTEM ARCHITECTURE"

    replacements = {
        "{PROJECT_TITLE}": title,
        "{PROJECT_SUBTITLE}": sub_val,
        "{PROJECT_SLUG}": slug,
        "{AUTHOR}": author,
        "{GROUP}": group,
        "{DISCIPLINE}": discipline,
        "{REPO}": repo_val,
    }

    for key, val in replacements.items():
        content = content.replace(key, str(val))

    if theme or (style and style != "pixel"):
        norm_style, norm_theme = normalize_style_and_theme(style, theme)
        if norm_theme:
            content = re.sub(r'style="[^"]*"', f'style="{norm_style}" theme="{norm_theme}"', content)

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    return output_path
