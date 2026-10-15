"""
HUD Studio Server Façade for ReadmeKit.
==============================================
Provides 100% backwards compatibility for legacy and CLI callers.
Modular implementation is located in `generator.studio`.
"""

from generator.studio import (
    STUDIO_HTML,
    StudioRequestHandler,
    ThreadedStudioServer,
    start_file_watcher,
    run_studio_server,
    extract_template_blocks,
    apply_global_theme_to_content,
    render_preview_html,
    markdown_to_html,
)

__all__ = [
    "STUDIO_HTML",
    "StudioRequestHandler",
    "ThreadedStudioServer",
    "start_file_watcher",
    "run_studio_server",
    "extract_template_blocks",
    "apply_global_theme_to_content",
    "render_preview_html",
    "markdown_to_html",
]

if __name__ == "__main__":
    run_studio_server()
