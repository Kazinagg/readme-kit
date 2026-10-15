"""
SVG generation components package for Pixel Readme Kit.
"""

from generator.components.base import escape_xml, validate_svg
from generator.components.header import generate_header, _generate_compact_header, generate_compact_header
from generator.components.footer import generate_footer
from generator.components.callout import generate_callout, GITHUB_ALERT_COLORS
from generator.components.frame import generate_frame
from generator.components.chip import generate_chip
from generator.components.divider import generate_divider, generate_splitter
from generator.components.metrics import generate_metrics, generate_progress, generate_techstack
from generator.components.timeline import generate_timeline
from generator.components.social import generate_social, generate_starchart, generate_profile_card

__all__ = [
    "escape_xml",
    "validate_svg",
    "generate_header",
    "_generate_compact_header",
    "generate_compact_header",
    "generate_footer",
    "generate_callout",
    "GITHUB_ALERT_COLORS",
    "generate_frame",
    "generate_chip",
    "generate_divider",
    "generate_splitter",
    "generate_metrics",
    "generate_progress",
    "generate_techstack",
    "generate_timeline",
    "generate_social",
    "generate_starchart",
    "generate_profile_card",
]
