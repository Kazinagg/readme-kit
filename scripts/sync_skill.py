#!/usr/bin/env python3
"""
scripts/sync_skill.py
Synchronizes canonical generator/ package into .agents/skills/pixel-readme/generator/
ensuring that the distributed skill is 100% self-contained and free of split-brain drift.
"""
import os
import shutil
import sys

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_GENERATOR = os.path.join(REPO_ROOT, "generator")
DEST_GENERATOR = os.path.join(REPO_ROOT, ".agents", "skills", "pixel-readme", "generator")

IGNORE_PATTERNS = shutil.ignore_patterns(
    "__pycache__",
    "*.pyc",
    "*.pyo",
    "*.pyd",
    ".pytest_cache",
    ".pixel-cache.json",
    ".DS_Store",
)


def sync_skill() -> None:
    if not os.path.isdir(SRC_GENERATOR):
        print(f"Error: Source directory {SRC_GENERATOR} does not exist", file=sys.stderr)
        sys.exit(1)

    print(f"Syncing canonical {SRC_GENERATOR} -> {DEST_GENERATOR}...")
    if os.path.exists(DEST_GENERATOR):
        shutil.rmtree(DEST_GENERATOR)

    shutil.copytree(SRC_GENERATOR, DEST_GENERATOR, ignore=IGNORE_PATTERNS)
    print("[OK] Successfully synchronized generator package to skill bundle.")


if __name__ == "__main__":
    sync_skill()
