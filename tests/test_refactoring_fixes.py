"""
Unit tests for ReadmeKit 5.1 refactoring and bugfixes:
- Header compact boolean parsing
- Negative lookahead in container directives to prevent tag collisions
- Base URL and cache bust ordering
- Link XML escaping
- MCP tool_render_block metrics cards/metrics arg, starchart, profile
- MCP tool_validate_template container tag balancing
- Support for 'val' alongside 'value' in metrics cards
- Studio CSS media block balanced brace extraction
- GitHub API token support and safe caching
"""

import os
import re
import tempfile
import unittest
import xml.etree.ElementTree as ET

from generator.compiler import MarkdownCompiler
from generator.engine import (
    generate_header,
    generate_metrics,
    validate_svg,
)
from generator.mcp_server import (
    tool_render_block,
    tool_validate_template,
)
from generator.studio.server import _extract_media_block, StudioRequestHandler
from generator.github_api import fetch_github_stat, _GITHUB_CACHE


class TestRefactoringFixes(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.assets_dir = os.path.join(self.temp_dir.name, "assets")
        os.makedirs(self.assets_dir, exist_ok=True)
        self.compiler = MarkdownCompiler(assets_dir=self.assets_dir, use_cache=True)

    def tearDown(self):
        self.temp_dir.cleanup()

    # --------------------------------------------------------------------------
    # 1. Header compact boolean parsing
    # --------------------------------------------------------------------------
    def test_header_compact_false_string(self):
        """Ensure compact='false' in markdown directive produces full-height header (~180px), not 84px."""
        md = '<!-- readme-kit:header title="FULL HEADER" subtitle="SUB" compact="false" -->'
        compiled = self.compiler.compile_text(md)
        self.assertIn("<img src=", compiled)

        # Find generated SVG asset and inspect its height
        svg_files = [f for f in os.listdir(self.assets_dir) if f.endswith(".svg")]
        self.assertTrue(len(svg_files) > 0)
        svg_path = os.path.join(self.assets_dir, svg_files[0])
        with open(svg_path, "r", encoding="utf-8") as f:
            svg_content = f.read()

        # Full cyberpunk/pixel header height is 260 (viewBox="0 0 850 260")
        self.assertIn('viewBox="0 0 850 260"', svg_content)
        self.assertNotIn('viewBox="0 0 850 84"', svg_content)

    def test_header_compact_true_string(self):
        """Ensure compact='true' in markdown directive produces compact header (~84px height)."""
        md = '<!-- readme-kit:header title="COMPACT HEADER" subtitle="SUB" compact="true" -->'
        compiled = self.compiler.compile_text(md)
        self.assertIn("<img src=", compiled)

        svg_files = [f for f in os.listdir(self.assets_dir) if f.endswith(".svg")]
        self.assertTrue(len(svg_files) > 0)
        svg_path = os.path.join(self.assets_dir, svg_files[0])
        with open(svg_path, "r", encoding="utf-8") as f:
            svg_content = f.read()

        self.assertIn('viewBox="0 0 850 84"', svg_content)

    # --------------------------------------------------------------------------
    # 2. Negative lookahead: metrics standalone followed by block container
    # --------------------------------------------------------------------------
    def test_metrics_standalone_followed_by_block_container(self):
        """
        Ensures standalone <!-- readme-kit:metrics repo='...' --> does not swallow
        intervening text when followed by a paired <!-- readme-kit:metrics --> block.
        """
        md = (
            '# Project Overview\n\n'
            '<!-- readme-kit:metrics auto_fetch="false" style="cyberpunk" -->\n\n'
            '### Middle Section Content\n'
            'This text MUST NOT be swallowed by the metrics container regex!\n\n'
            '<!-- readme-kit:metrics style="modern" -->\n'
            '- label="BENCHMARK" value="1,200+" delta="+24%" trend="up"\n'
            '- label="UPTIME" value="99.9%" status="STABLE"\n'
            '<!-- /readme-kit:metrics -->\n\n'
            'Final conclusion paragraph.\n'
        )
        compiled = self.compiler.compile_text(md)

        # Intervening text must remain intact
        self.assertIn("### Middle Section Content", compiled)
        self.assertIn("This text MUST NOT be swallowed by the metrics container regex!", compiled)
        self.assertIn("Final conclusion paragraph.", compiled)

        # Both metrics assets must be generated
        svg_files = [f for f in os.listdir(self.assets_dir) if f.endswith(".svg")]
        self.assertGreaterEqual(len(svg_files), 2)

    def test_paired_container_isolation_window_and_quote(self):
        """Sequential window and quote containers must not merge or swallow text between them."""
        md = (
            '<!-- readme-kit:window title="WINDOW 1" style="minimal" -->\n'
            'Inner content 1\n'
            '<!-- /readme-kit:window -->\n\n'
            'Divider Paragraph Between Containers\n\n'
            '<!-- readme-kit:quote title="QUOTE TITLE" style="minimal" -->\n'
            'Quote body text\n'
            '<!-- /readme-kit:quote -->\n'
        )
        compiled = self.compiler.compile_text(md)
        self.assertIn("Divider Paragraph Between Containers", compiled)
        self.assertIn("Inner content 1", compiled)
        self.assertIn("Quote body text", compiled)

    # --------------------------------------------------------------------------
    # 3. Base URL and cache bust ordering
    # --------------------------------------------------------------------------
    def test_base_url_applied_after_cache_bust(self):
        """
        self.base_url must be prepended AFTER _apply_cache_bust computes hash on relative path.
        Otherwise _apply_cache_bust fails to find entry and defaults to ?v=v4.
        """
        base_url = "https://raw.githubusercontent.com/Kazinagg/readme-kit/main"
        compiler = MarkdownCompiler(assets_dir=self.assets_dir, base_url=base_url, use_cache=True, bust_cache=True)

        md = '<!-- readme-kit:header title="BASE URL TEST" style="cyberpunk" -->'
        compiled = compiler.compile_text(md)

        self.assertIn(base_url, compiled)
        # Should contain ?v=<hash> with an 8-char hex content hash, NOT the fallback v4
        m = re.search(r'\?v=([a-f0-9]{8})', compiled)
        self.assertIsNotNone(m, f"Compiled output should contain an 8-char hex content hash: {compiled}")

    # --------------------------------------------------------------------------
    # 4. Link XML attribute escaping
    # --------------------------------------------------------------------------
    def test_link_xml_escaping_in_chip(self):
        """Ensure special characters in links (&, \", <, >) are XML-escaped to prevent XSS / markup corruption."""
        chip_url = "https://example.com/api?user=admin&token=123%22&val=456"
        md = f'<!-- readme-kit:chip text="SECURE_CHIP" href="{chip_url}" -->'
        compiled = self.compiler.compile_text(md)

        # & must be escaped to &amp;
        self.assertIn("https://example.com/api?user=admin&amp;token=123%22&amp;val=456", compiled)
        self.assertNotIn("user=admin&token", compiled)

    # --------------------------------------------------------------------------
    # 5. Metrics val support alongside value
    # --------------------------------------------------------------------------
    def test_metrics_val_support_in_all_styles(self):
        """Ensure metrics cards accepting 'val' properly render the metric number across all styles."""
        test_cards = [
            {"label": "TEST_VAL", "val": "8888", "delta": "+10%"},
            {"label": "TEST_VALUE", "value": "9999", "delta": "+20%"},
        ]
        # Modern style
        modern_svg = generate_metrics(metrics=test_cards, style="modern", theme="slate-dark")
        self.assertIn("8888", modern_svg)
        self.assertIn("9999", modern_svg)
        validate_svg(modern_svg)

        # Sketch style
        sketch_svg = generate_metrics(metrics=test_cards, style="sketch", theme="excali-dark")
        self.assertIn("8888", sketch_svg)
        self.assertIn("9999", sketch_svg)
        validate_svg(sketch_svg)

        # Pixel style
        pixel_svg = generate_metrics(metrics=test_cards, style="cyberpunk", theme="cyberpunk")
        self.assertIn("8888", pixel_svg)
        self.assertIn("9999", pixel_svg)
        validate_svg(pixel_svg)

    # --------------------------------------------------------------------------
    # 6. MCP Server: tool_render_block fixes
    # --------------------------------------------------------------------------
    def test_mcp_tool_render_block_metrics(self):
        """Verify tool_render_block executes generate_metrics using metrics= parameter without TypeError."""
        res = tool_render_block(
            block_type="metrics",
            style="modern",
            theme="slate-dark",
            params={
                "cards": [
                    {"label": "LATENCY", "value": "12ms"},
                    {"label": "THROUGHPUT", "val": "100k req/s"}
                ]
            }
        )
        self.assertTrue(res.get("success"), f"tool_render_block failed: {res}")
        self.assertIn("12ms", res["svg"])
        self.assertIn("100k req/s", res["svg"])

    def test_mcp_tool_render_block_starchart_and_profile(self):
        """Verify tool_render_block handles starchart and profile block types."""
        # Starchart
        res_star = tool_render_block(
            block_type="starchart",
            style="modern",
            theme="slate-dark",
            repo="Kazinagg/readme-kit"
        )
        self.assertTrue(res_star.get("success"), f"starchart failed: {res_star}")
        self.assertIn("svg", res_star)

        # Profile
        res_prof = tool_render_block(
            block_type="profile",
            style="modern",
            theme="slate-dark",
            title="LEAD DEVELOPER",
            subtitle="SYSTEMS ARCHITECT"
        )
        self.assertTrue(res_prof.get("success"), f"profile failed: {res_prof}")
        self.assertIn("LEAD DEVELOPER", res_prof["svg"])

    # --------------------------------------------------------------------------
    # 7. MCP Server: tool_validate_template container balancing
    # --------------------------------------------------------------------------
    def test_mcp_tool_validate_template_mismatched_container(self):
        """tool_validate_template must report warnings when container opening and closing tags are unbalanced."""
        bad_template = (
            '<!-- readme-kit:window title="OPEN WINDOW" -->\n'
            'Window body\n'
        )
        res_bad = tool_validate_template(content=bad_template)
        self.assertFalse(res_bad["is_valid"])
        self.assertTrue(any("Mismatched container tags for 'window'" in w for w in res_bad["warnings"]))

        good_template = (
            '<!-- readme-kit:window title="OPEN WINDOW" -->\n'
            'Window body\n'
            '<!-- /readme-kit:window -->\n'
        )
        res_good = tool_validate_template(content=good_template)
        self.assertTrue(res_good["is_valid"])
        self.assertEqual(len(res_good["warnings"]), 0)

    # --------------------------------------------------------------------------
    # 8. Studio balanced brace CSS media block extraction
    # --------------------------------------------------------------------------
    def test_studio_media_block_balanced_braces(self):
        """_extract_media_block must properly match closing brace across multiple nested rules."""
        sample_svg = (
            '<svg><style>\n'
            ':root { --bg: #ffffff; }\n'
            '@media (prefers-color-scheme: dark) {\n'
            '  :root {\n'
            '    --bg: #000000;\n'
            '  }\n'
            '  .nested-rule {\n'
            '    fill: #ff0000;\n'
            '  }\n'
            '}\n'
            '.after-rule { display: block; }\n'
            '</style></svg>'
        )
        inner, stripped = _extract_media_block(sample_svg, r'@media\s*\(\s*prefers-color-scheme\s*:\s*dark\s*\)')
        self.assertIsNotNone(inner)
        self.assertIn("--bg: #000000;", inner)
        self.assertIn(".nested-rule", inner)
        self.assertNotIn("@media", stripped)
        self.assertIn(".after-rule", stripped)
        self.assertIn(":root { --bg: #ffffff; }", stripped)

    # --------------------------------------------------------------------------
    # 9. GitHub API offline fallback and caching
    # --------------------------------------------------------------------------
    def test_github_api_offline_fallback(self):
        """fetch_github_stat returns expected fallback without network call when auto_fetch=False."""
        text, link = fetch_github_stat("owner/repo", "stars", auto_fetch=False)
        self.assertEqual(text, "★ STARS")
        self.assertEqual(link, "https://github.com/owner/repo/stargazers")


if __name__ == "__main__":
    unittest.main()

