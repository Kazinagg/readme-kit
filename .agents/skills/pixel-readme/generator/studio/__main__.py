"""
CLI entry point for running HUD Studio directly via python -m generator.studio
"""
import argparse
from generator.studio.server import run_studio_server


def main():
    parser = argparse.ArgumentParser(description="ReadmeKit HUD Studio Live Server")
    parser.add_argument("--template", "-t", default="README.template.md", help="Path to markdown template")
    parser.add_argument("--output", "-o", default="README.md", help="Path to output markdown file")
    parser.add_argument("--assets", "-a", default="assets/generated", help="Directory for generated assets")
    parser.add_argument("--port", "-p", type=int, default=3000, help="Port to listen on (default: 3000)")
    parser.add_argument("--open", action="store_true", help="Automatically open browser")
    args = parser.parse_args()

    run_studio_server(
        template_path=args.template,
        output_path=args.output,
        assets_dir=args.assets,
        port=args.port,
        open_browser=args.open,
    )


if __name__ == "__main__":
    main()
