import os
import sys
import hashlib
import tempfile
import subprocess
from pathlib import Path


def _hash_file(filepath: Path) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def test_generator_skill_parity():
    """Verify that .agents/skills/pixel-readme/generator has full parity with root generator/."""
    repo_root = Path(__file__).resolve().parent.parent
    root_gen = repo_root / "generator"
    skill_gen = repo_root / ".agents" / "skills" / "pixel-readme" / "generator"

    assert root_gen.is_dir(), f"Root generator dir missing: {root_gen}"
    assert skill_gen.is_dir(), f"Skill generator dir missing: {skill_gen}"

    root_py_files = {
        p.relative_to(root_gen): p
        for p in root_gen.rglob("*.py")
        if "__pycache__" not in p.parts
    }

    skill_py_files = {
        p.relative_to(skill_gen): p
        for p in skill_gen.rglob("*.py")
        if "__pycache__" not in p.parts
    }

    diff_keys = set(root_py_files.keys()) ^ set(skill_py_files.keys())
    assert not diff_keys, (
        f"Skill generator is out of sync! File set difference: {diff_keys}. "
        "Run: python scripts/sync_skill.py"
    )

    mismatches = []
    for rel_path, root_file in root_py_files.items():
        skill_file = skill_py_files[rel_path]
        if _hash_file(root_file) != _hash_file(skill_file):
            mismatches.append(str(rel_path))

    assert not mismatches, (
        f"Skill generator is out of sync! Content mismatch in: {mismatches}. "
        "Run: python scripts/sync_skill.py"
    )


def test_skill_generator_standalone_isolation():
    """Verify that skill cli executes cleanly in an isolated environment outside the repo."""
    repo_root = Path(__file__).resolve().parent.parent
    skill_cli_path = repo_root / ".agents" / "skills" / "pixel-readme" / "generator" / "cli.py"

    assert skill_cli_path.is_file(), f"Skill cli.py missing: {skill_cli_path}"

    isolated_env = os.environ.copy()
    isolated_env.pop("PYTHONPATH", None)

    res = subprocess.run(
        [sys.executable, str(skill_cli_path), "--help"],
        cwd=tempfile.gettempdir(),
        env=isolated_env,
        capture_output=True,
        text=True,
    )

    assert res.returncode == 0, (
        f"Standalone skill execution failed with returncode {res.returncode}:\n"
        f"Stdout: {res.stdout}\nStderr: {res.stderr}"
    )
    assert "ReadmeKit" in res.stdout or "usage:" in res.stdout
