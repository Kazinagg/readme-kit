"""
HUD Studio Request Handlers.
"""

from generator.studio.handlers.render_handler import handle_render_request, handle_github_fetch
from generator.studio.handlers.template_handler import (
    extract_template_blocks,
    apply_global_theme_to_content,
    render_preview_html,
    markdown_to_html,
)
from generator.studio.handlers.theme_handler import (
    handle_presets_list,
    handle_themes_list,
    handle_theme_generate,
    handle_theme_save,
)
from generator.studio.handlers.git_handler import handle_git_push

__all__ = [
    "handle_render_request",
    "handle_github_fetch",
    "extract_template_blocks",
    "apply_global_theme_to_content",
    "render_preview_html",
    "markdown_to_html",
    "handle_presets_list",
    "handle_themes_list",
    "handle_theme_generate",
    "handle_theme_save",
    "handle_git_push",
]
