import subprocess
import json
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
PLUGINS = ROOT / "_plugin-references"
OUT = ROOT / "docs" / ".plugin_updates_last.json"
TIMEOUT = 180


def git(args, cwd):
    try:
        return subprocess.run(
            ["git"] + args,
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=TIMEOUT,
            encoding="utf-8",
            errors="replace",
        )
    except subprocess.TimeoutExpired:
        return subprocess.CompletedProcess(args, 124, "", "timeout")


def remote_head(d):
    r = git(["rev-parse", "origin/HEAD"], d)
    if r.returncode == 0 and r.stdout.strip():
        return r.stdout.strip()
    r = git(["rev-parse", "FETCH_HEAD"], d)
    return r.stdout.strip() if r.returncode == 0 else ""


def check_one(d):
    name = d.name
    if not (d / ".git").exists():
        return {"name": name, "status": "not_a_repo"}
    head_old = git(["rev-parse", "HEAD"], d).stdout.strip()
    if not head_old:
        return {"name": name, "status": "no_head"}
    fetch = git(["fetch", "origin", "--quiet"], d)
    if fetch.returncode != 0:
        return {
            "name": name,
            "status": "fetch_error",
            "head": head_old[:12],
            "error": fetch.stderr.strip()[:500],
        }
    head_remote = remote_head(d)
    if not head_remote or head_remote == head_old:
        return {"name": name, "status": "up_to_date", "head": head_old[:12]}
    pull = git(["pull", "--ff-only", "--quiet"], d)
    if pull.returncode != 0:
        return {
            "name": name,
            "status": "pull_failed",
            "old": head_old[:12],
            "remote": head_remote[:12],
            "error": pull.stderr.strip()[:500],
        }
    head_new = git(["rev-parse", "HEAD"], d).stdout.strip()
    log = git(
        ["log", f"{head_old}..{head_new}", "--pretty=format:%h|%ci|%s"], d
    ).stdout
    diffstat = git(["diff", "--stat", head_old, head_new], d).stdout
    names = git(["diff", "--name-only", head_old, head_new], d).stdout
    return {
        "name": name,
        "status": "updated",
        "old": head_old[:12],
        "new": head_new[:12],
        "commits": [c for c in log.strip().splitlines() if c],
        "changed_files": [c for c in names.strip().splitlines() if c],
        "diffstat": diffstat.strip(),
    }


def main():
    results = []
    if PLUGINS.is_dir():
        for d in sorted(PLUGINS.iterdir()):
            if d.is_dir():
                results.append(check_one(d))
    payload = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "root": str(ROOT),
        "results": results,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()