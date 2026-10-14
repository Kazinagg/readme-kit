"""
Git push and staging handler for HUD Studio.
Carefully isolates stages to README and generated assets only.
"""

import os
import json
import subprocess


def handle_git_push(handler) -> None:
    """Handles POST /api/git/push_readme with strict file isolation."""
    try:
        handler.trigger_compile()

        work_dir = os.path.dirname(os.path.abspath(handler.template_file)) if handler.template_file else os.getcwd()
        res = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], cwd=work_dir, capture_output=True, text=True)
        if res.returncode != 0:
            handler.send_response(400)
            handler.send_header("Content-Type", "application/json")
            handler.end_headers()
            handler.wfile.write(json.dumps({"ok": False, "error": "Not a Git repository"}).encode("utf-8"))
            return

        files_to_add = []
        if handler.output_file and os.path.exists(handler.output_file):
            files_to_add.append(os.path.relpath(handler.output_file, work_dir))
        if handler.template_file and os.path.exists(handler.template_file):
            files_to_add.append(os.path.relpath(handler.template_file, work_dir))
        if handler.assets_dir and os.path.exists(handler.assets_dir):
            files_to_add.append(os.path.relpath(handler.assets_dir, work_dir))

        if not files_to_add:
            handler.send_response(400)
            handler.send_header("Content-Type", "application/json")
            handler.end_headers()
            handler.wfile.write(json.dumps({"ok": False, "error": "No README or assets found to stage"}).encode("utf-8"))
            return

        for target in files_to_add:
            subprocess.run(["git", "add", target], cwd=work_dir, check=True)

        diff_res = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=work_dir)
        has_staged_changes = (diff_res.returncode != 0)

        committed = False
        if has_staged_changes:
            commit_msg = "docs: update README via ReadmeKit Studio"
            c_res = subprocess.run(["git", "commit", "-m", commit_msg], cwd=work_dir, capture_output=True, text=True)
            if c_res.returncode != 0:
                handler.send_response(500)
                handler.send_header("Content-Type", "application/json")
                handler.end_headers()
                handler.wfile.write(json.dumps({"ok": False, "error": f"Git commit failed: {c_res.stderr.strip()}"}).encode("utf-8"))
                return
            committed = True

        p_res = subprocess.run(["git", "push"], cwd=work_dir, capture_output=True, text=True)
        if p_res.returncode != 0:
            handler.send_response(500)
            handler.send_header("Content-Type", "application/json")
            handler.end_headers()
            handler.wfile.write(json.dumps({
                "ok": False,
                "error": f"Git push failed: {p_res.stderr.strip() or p_res.stdout.strip()}",
                "committed": committed
            }).encode("utf-8"))
            return

        handler.send_response(200)
        handler.send_header("Content-Type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps({
            "ok": True,
            "committed": committed,
            "files": files_to_add,
            "message": "README and assets pushed to GitHub successfully!" if committed else "Already up to date. Pushed latest commits to GitHub."
        }).encode("utf-8"))
    except FileNotFoundError:
        handler.send_response(500)
        handler.send_header("Content-Type", "application/json")
        handler.end_headers()
        handler.wfile.write(json.dumps({"ok": False, "error": "Git command line tool not found on system PATH"}).encode("utf-8"))
    except Exception as e:
        handler.send_error(500, f"Git push error: {e}")
