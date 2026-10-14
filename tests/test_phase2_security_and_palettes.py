"""
Unit tests for Phase 2 hardening:
1. Template protection & static file serving security in studio/server.py
2. Palette differentiation: rough-doodle vs excali-dark
3. CLI style choices (sketch support) and scaffolder template resolution
"""

import os
import io
import json
import unittest
from unittest.mock import MagicMock, patch

from generator.themes import resolve_theme, normalize_style_and_theme
from generator.palettes import THEMES
from generator.components.social import generate_profile_card, generate_starchart
from generator.cli import build_parser
from generator.scaffolder import TEMPLATE_REGISTRY, resolve_template_path, ALIASES
from generator.studio.server import StudioRequestHandler, is_protected_template, PROJECT_ROOT


class TestPaletteDifferentiation(unittest.TestCase):
    def test_rough_doodle_vs_excali_dark_distinct(self):
        """rough-doodle and excali-dark must generate distinctly different SVGs."""
        prof_rough = generate_profile_card(style="sketch", theme="rough-doodle")
        prof_excali = generate_profile_card(style="sketch", theme="excali-dark")
        self.assertNotEqual(prof_rough, prof_excali)

        star_rough = generate_starchart(style="sketch", theme="rough-doodle")
        star_excali = generate_starchart(style="sketch", theme="excali-dark")
        self.assertNotEqual(star_rough, star_excali)

    def test_rough_doodle_in_palettes(self):
        """rough-doodle must be defined in generator.palettes THEMES with light paper defaults."""
        self.assertIn("rough-doodle", THEMES)
        doodle = THEMES["rough-doodle"]
        self.assertEqual(doodle["primary"], "#4F46E5")
        self.assertEqual(doodle["bg_glass"], "#FDFDFD")
        self.assertIn("doodle", THEMES)
        self.assertIn("sketch", THEMES)

    def test_rough_doodle_css_root_vars(self):
        """rough-doodle resolve_theme in auto mode must provide light-first root variables."""
        c, css = resolve_theme(style="sketch", theme="rough-doodle", mode="auto")
        self.assertIn("--bg-glass: #FDFDFD;", css)
        self.assertIn("--primary: #4F46E5;", css)


class TestCliSketchChoices(unittest.TestCase):
    def test_cli_accepts_sketch_style(self):
        """CLI parser must accept --style sketch without error."""
        parser = build_parser()
        args = parser.parse_args(["header", "--style", "sketch", "--theme", "rough-doodle"])
        self.assertEqual(args.style, "sketch")
        self.assertEqual(args.theme, "rough-doodle")

    def test_cli_accepts_doodle_style(self):
        """CLI parser must accept --style doodle without error."""
        parser = build_parser()
        args = parser.parse_args(["footer", "--style", "doodle"])
        self.assertEqual(args.style, "doodle")

    def test_scaffolder_all_templates_and_aliases(self):
        """All registered templates and aliases in scaffolder must resolve to existing files."""
        for key in TEMPLATE_REGISTRY:
            path = resolve_template_path(key)
            self.assertTrue(os.path.isfile(path), f"Template file does not exist: {path}")

        for alias in ALIASES:
            path = resolve_template_path(alias)
            self.assertTrue(os.path.isfile(path), f"Alias does not resolve to existing file: {alias} -> {path}")


class TestStudioSecurityAndProtection(unittest.TestCase):
    def test_is_protected_template(self):
        """Templates in generator/templates/ must be recognized as protected."""
        sample_tpl = os.path.join(PROJECT_ROOT, "generator", "templates", "repo", "library.template.md")
        self.assertTrue(is_protected_template(sample_tpl))
        self.assertTrue(is_protected_template("generator/templates/profile/modern.template.md"))

        # User workspace template must NOT be protected
        self.assertFalse(is_protected_template(os.path.join(PROJECT_ROOT, "README.template.md")))
        self.assertFalse(is_protected_template("README.template.md"))

    def test_protected_template_write_blocked(self):
        """Modifying endpoints must return HTTP 403 Forbidden for protected templates."""
        req = MagicMock(spec=StudioRequestHandler)
        req.path = "/api/template/apply_global_theme"
        req.template_file = os.path.join(PROJECT_ROOT, "generator", "templates", "repo", "library.template.md")
        req.assets_dir = os.path.join(PROJECT_ROOT, "assets")
        req.output_file = os.path.join(PROJECT_ROOT, "README.md")
        req.rfile = io.BytesIO(b'{"theme": "cyberpunk"}')
        req.headers = {"Content-Length": "22"}

        StudioRequestHandler.do_POST(req)
        req.send_error.assert_called_with(403, unittest.mock.ANY)

    def test_static_file_serving_whitelist(self):
        """do_GET must return 404 for python files, .git, and unauthorized directories."""
        req = MagicMock(spec=StudioRequestHandler)
        req.path = "/generator/cli.py"
        StudioRequestHandler.do_GET(req)
        req.send_error.assert_called_with(404, "File not found")

        req.reset_mock()
        req.path = "/.git/config"
        StudioRequestHandler.do_GET(req)
        req.send_error.assert_called_with(404, "File not found")

        req.reset_mock()
        req.path = "/pyproject.toml"
        StudioRequestHandler.do_GET(req)
        req.send_error.assert_called_with(404, "File not found")


if __name__ == "__main__":
    unittest.main()
