"""
Unit tests for v5.0 Components, Multi-Style Themes, and Repo/Profile Templates.
"""

import os
import tempfile
import unittest
import xml.etree.ElementTree as ET

from generator.engine import (
    generate_starchart,
    generate_profile_card,
    resolve_theme,
    THEME_PALETTES,
    validate_svg
)
from generator.palettes import THEMES
from generator.compiler import MarkdownCompiler
from generator.scaffolder import scaffold_readme, TEMPLATE_REGISTRY


class TestV5Starchart(unittest.TestCase):
    def test_generate_starchart_xml_validity(self):
        """Verify generate_starchart generates valid XML in all modes and styles."""
        styles = ["cyberpunk", "tactical", "minimal", "clean-mono", "corporate-blue"]
        modes = ["auto", "dark", "light", "transparent"]

        for style in styles:
            for mode in modes:
                with self.subTest(style=style, mode=mode):
                    svg = generate_starchart(
                        style=style,
                        mode=mode,
                        repo="owner/test-repo",
                        points="5,20,55,140,420,980",
                        current="980",
                        delta="+120% 6m",
                        title="STARS TRAJECTORY"
                    )
                    root = ET.fromstring(svg)
                    self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")
                    self.assertIn("viewBox", root.attrib)

    def test_generate_starchart_custom_points_and_defaults(self):
        """Verify handling of default points, flat points, single point, and presets."""
        svg_default = generate_starchart()
        ET.fromstring(svg_default)

        # Single point
        svg_single = generate_starchart(points="100")
        ET.fromstring(svg_single)

        # Flat points
        svg_flat = generate_starchart(points="50,50,50,50")
        ET.fromstring(svg_flat)

        # Preset usage
        svg_preset = generate_starchart(preset="corporate-blue", style="corporate-blue")
        ET.fromstring(svg_preset)


class TestV5ProfileCard(unittest.TestCase):
    def test_generate_profile_card_xml_validity(self):
        """Verify generate_profile_card generates valid XML in all modes and styles."""
        styles = ["cyberpunk", "tactical", "minimal", "clean-mono", "academic-paper"]
        modes = ["auto", "dark", "light", "transparent"]

        for style in styles:
            for mode in modes:
                with self.subTest(style=style, mode=mode):
                    svg = generate_profile_card(
                        style=style,
                        mode=mode,
                        name="SARAH CONNOR",
                        role="DEFENSE SYSTEMS ARCHITECT",
                        bio="Building unstoppable resilient systems.",
                        status="ACTIVE",
                        location="LOS ANGELES",
                        badge="SYS_ADMIN"
                    )
                    root = ET.fromstring(svg)
                    self.assertEqual(root.tag, "{http://www.w3.org/2000/svg}svg")
                    self.assertIn("viewBox", root.attrib)

    def test_profile_card_long_names(self):
        """Verify that long names are handled gracefully without XML errors."""
        svg = generate_profile_card(
            name="ALEXANDER VON HUMBOLDT",
            role="CHIEF GEOGRAPHICAL EXPLORATION ARCHITECT",
            bio="Exploring deep algorithmic jungles and microkernel runtimes."
        )
        ET.fromstring(svg)

    def test_profile_card_no_text_overlap(self):
        """Verify that 3D name does not vertically collide with Role Pill (y=116) or Bio (y=166)."""
        test_names = ["ALEX DEVELOPER", "SARAH CONNOR", "ALEXANDER VON HUMBOLDT", "JOHN"]
        for name in test_names:
            with self.subTest(name=name):
                svg = generate_profile_card(name=name)
                root = ET.fromstring(svg)

                # Find all rects inside <g class="pixel-text-3d">
                # None of them should have y + height >= 116 (where Role Pill starts)
                for g in root.iter("{http://www.w3.org/2000/svg}g"):
                    if g.attrib.get("class") == "pixel-text-3d":
                        for rect in g.iter("{http://www.w3.org/2000/svg}rect"):
                            y_val = float(rect.attrib.get("y", 0))
                            h_val = float(rect.attrib.get("height", 0))
                            bottom_y = y_val + h_val
                            self.assertLess(
                                bottom_y, 116,
                                f"Name '{name}' glyph rect at y={y_val}, bottom={bottom_y} collides with Role Pill at y=116"
                            )


class TestV5Presets(unittest.TestCase):
    def test_v5_presets_exist_and_resolve(self):
        """Verify all new v5 presets exist in presets/ and resolve properly in engine."""
        v5_presets = ["clean-mono", "corporate-blue", "academic-paper", "modern-slate"]
        for p in v5_presets:
            with self.subTest(preset=p):
                preset_path = os.path.join(os.path.dirname(__file__), "..", "generator", "presets", f"{p}.json")
                if not os.path.exists(preset_path):
                    preset_path = os.path.join(os.path.dirname(__file__), "..", "presets", f"{p}.json")
                self.assertTrue(os.path.exists(preset_path), f"Preset file {preset_path} missing")
                self.assertIn(p, THEMES, f"Theme {p} not registered in palettes.THEMES")
                self.assertIn(p, THEME_PALETTES, f"Theme {p} not registered in engine.THEME_PALETTES")

                c, css = resolve_theme(style=p, mode="dark")
                self.assertIn("primary", c)
                self.assertIn("accent", c)


class TestV5CompilerDirectives(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.compiler = MarkdownCompiler(assets_dir=self.tmp_dir)

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_compiler_starchart_directive(self):
        """Verify that <!-- pixel-kit:starchart ... --> compiles and produces output."""
        chart_file = os.path.join(self.tmp_dir, "chart.svg")
        chart_out = chart_file.replace("\\", "/")
        md = f'<!-- pixel-kit:starchart style="corporate-blue" repo="octocat/Hello-World" points="10,50,200" title="GROWTH" out="{chart_out}" -->'
        compiled = self.compiler.compile_text(md)
        self.assertIn("chart.svg", compiled)
        self.assertTrue(os.path.exists(chart_file))
        with open(chart_file, "r", encoding="utf-8") as f:
            content = f.read()
        ET.fromstring(content)

    def test_compiler_profile_directive(self):
        """Verify that <!-- pixel-kit:profile ... --> compiles and produces output."""
        profile_file = os.path.join(self.tmp_dir, "profile.svg")
        profile_out = profile_file.replace("\\", "/")
        md = f'<!-- pixel-kit:profile style="clean-mono" name="DEV MASTER" role="BACKEND LEAD" out="{profile_out}" -->'
        compiled = self.compiler.compile_text(md)
        self.assertIn("profile.svg", compiled)
        self.assertTrue(os.path.exists(profile_file))
        with open(profile_file, "r", encoding="utf-8") as f:
            content = f.read()
        ET.fromstring(content)


class TestV5Scaffolder(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_scaffolder_all_registered_templates(self):
        """Verify that all templates in TEMPLATE_REGISTRY can be scaffolded cleanly."""
        for key in TEMPLATE_REGISTRY.keys():
            with self.subTest(template=key):
                out_path = os.path.join(self.tmp_dir, f"{key.replace('/', '_')}.md")
                scaffold_readme(project_type=key, title="Test Project", output_path=out_path)
                self.assertTrue(os.path.exists(out_path))
                with open(out_path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.assertTrue(len(content) > 50)
                self.assertIn("<!-- pixel-kit:", content)

    def test_scaffolder_categories(self):
        """Verify scaffolding by category repo and profile."""
        out_repo = os.path.join(self.tmp_dir, "repo.md")
        scaffold_readme(category="repo", project_type="library", title="My Lib", output_path=out_repo)
        with open(out_repo, "r", encoding="utf-8") as f:
            repo_content = f.read()
        self.assertIn("pixel-kit:header", repo_content)

        out_prof = os.path.join(self.tmp_dir, "profile.md")
        scaffold_readme(category="profile", project_type="developer", title="John Doe", output_path=out_prof)
        with open(out_prof, "r", encoding="utf-8") as f:
            prof_content = f.read()
        self.assertIn("pixel-kit:profile", prof_content)


if __name__ == "__main__":
    unittest.main()
