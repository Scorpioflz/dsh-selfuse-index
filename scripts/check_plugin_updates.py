import subprocess
import json
import re
import logging
import sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
CREATEFLAGS = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
PLUGINS = ROOT / "_plugin-references"
OUT_JSON = ROOT / "docs" / ".plugin_updates_last.json"
OUT_MD = ROOT / "docs" / "plugin_updates.md"
TIMEOUT = 180

LOG_FILE = ROOT / "logs" / "plugin_update.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

IN_USE = {
    "dsh-webapi", "dsh-balance-panel", "dsh-chat-manager",
    "dsh-skills-manager", "dsh-custom-reasoning", "billion-context",
    "dsh-univer-office", "dsh-preset-bridge", "modsearch", "cc-safety-net",
    "dsh-persona-dafeiyu", "dsh-knowledge", "dsh-session-bridge",
}
REFERENCE = {
    "dsh-fish-memory", "dsh-bili-scroll", "dsh-computer-use", "dsh-prompt-persona",
    "dsh-whale-musume-persona", "dsh-soul", "dsh-pet-indesktop-upstream",
    "dsh-liketavern",
}

HEADER = """# DSH 插件更新跟踪

本文件由定时任务（每小时）**覆盖式**维护，只保留**尚未执行**的建议操作。
已实施的变更（建议行标记 ✅）在下次运行时自动清除，避免文件无限增长。
完整检查快照见 `docs/.plugin_updates_last.json`。

检查脚本：`scripts/check_plugin_updates.py`（遍历每个插件浅克隆，`git fetch` 比较
远程 HEAD，有更新则 `git pull --ff-only` 并记录 commit 列表与文件变动）。

## 分类处理规则

- **在用插件** → **影响评估**：只分析变更是否影响自研部分
  （`@dsh-pet/bridge`、`@dsh-cbw/memory`、桌宠前端、人设模板）依赖的 API/契约/配置面。
  无影响则写「无影响」。不写整合建议——直接安装的插件，更新即更新。
- **参考/已弃插件** → **整合建议**：分析上游变更中哪些有用部分可整合进对应自研插件
  （如 dsh-fish-memory → @dsh-cbw/memory、dsh-pet-indesktop-upstream → 桌宠前端等）。

## 状态图例

- `updated` — 远程有新提交，已拉取
- `up_to_date` — 已是最新
- `fetch_error` / `pull_failed` — 网络或非快进更新，需人工介入
- `not_a_repo` / `no_head` — 目录非 git 仓库
"""


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
            creationflags=CREATEFLAGS,
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


def parse_pending_advice(md_text):
    """从旧 plugin_updates.md 提取未完成建议，返回 {plugin_name: {advice, keep_until}}。
    - 含 <!-- keep-until: YYYY-MM-DD --> 且未过期 → 保留（即使含 ✅，长期参考记忆）
    - 含 keep-until 且已过期 → 丢弃
    - 无 keep-until：含 ✅ 或「无影响」→ 丢弃"""
    pending = {}
    today = datetime.now().strftime("%Y-%m-%d")
    blocks = re.split(r'(?=^- \*\*)', md_text, flags=re.MULTILINE)
    for block in blocks:
        m = re.match(r'- \*\*(.+?)\*\*', block)
        if not m:
            continue
        name = m.group(1)

        keep_until = None
        keep_match = re.search(r'<!-- keep-until: (\d{4}-\d{2}-\d{2}) -->', block)
        if keep_match:
            keep_until = keep_match.group(1)
            if today > keep_until:
                continue
        elif "✅" in block:
            continue

        advice_match = re.search(
            r'  - (?:影响评估|整合建议):\s*(.+)', block, re.DOTALL
        )
        if advice_match:
            advice = advice_match.group(1).strip()
            advice = advice.split("\n")[0].strip()
            if not advice or advice == "[待分析]":
                continue
            if not keep_until:
                if "✅" in advice or advice.startswith("**无影响**"):
                    continue
            pending[name] = {"advice": advice, "keep_until": keep_until}
    return pending


def summarize_commits(commits):
    if not commits:
        return ""
    n = len(commits)
    first = commits[0].split("|")
    last = commits[-1].split("|")
    subj_first = first[2] if len(first) > 2 else ""
    return f"{n} commits，最近: {subj_first[:80]}"


def render_md(timestamp, results, pending):
    updated = {r["name"]: r for r in results if r["status"] == "updated"}
    uptodate = sum(1 for r in results if r["status"] == "up_to_date")
    errors = [r for r in results if r["status"] not in ("updated", "up_to_date")]

    names_to_show = set(updated.keys()) | set(pending.keys())

    in_use_items = []
    ref_items = []
    for name in sorted(names_to_show):
        r = updated.get(name)
        is_in_use = name in IN_USE
        is_ref = name in REFERENCE
        if not is_in_use and not is_ref:
            continue
        entry = pending.get(name)
        if isinstance(entry, dict):
            advice_text = entry["advice"]
            keep_until = entry["keep_until"]
        else:
            advice_text = entry if entry else ""
            keep_until = None
        label = "影响评估" if is_in_use else "整合建议"
        if r:
            summary = summarize_commits(r.get("commits", []))
            head_line = f"- **{name}**: `{r['old']}` → `{r['new']}`（{summary}）"
        else:
            head_line = f"- **{name}**: （无新更新，仍有未完成建议）"
        advice_text = advice_text if advice_text else "[待分析]"
        item = f"{head_line}\n  - {label}: {advice_text}"
        if keep_until:
            item += f"\n  <!-- keep-until: {keep_until} -->"
        if is_in_use:
            in_use_items.append(item)
        else:
            ref_items.append(item)

    lines = [HEADER.rstrip(), ""]
    lines.append("## 当前待处理建议")
    lines.append("")
    lines.append(
        f"> 最后检查：{timestamp} | "
        f"{len(updated)} 个有更新，{uptodate} 个已最新"
        + (f"，{len(errors)} 个异常" if errors else "")
    )
    lines.append("")

    lines.append("### 在用插件 · 影响评估")
    lines.append("")
    if in_use_items:
        lines.extend(in_use_items)
    else:
        lines.append("（无待处理项）")
    lines.append("")

    lines.append("### 参考插件 · 整合建议")
    lines.append("")
    if ref_items:
        lines.extend(ref_items)
    else:
        lines.append("（无待处理项）")
    lines.append("")

    if errors:
        lines.append("### 异常")
        lines.append("")
        for r in errors:
            err = r.get("error", r["status"])
            lines.append(f"- **{r['name']}**: {err}")
        lines.append("")

    return "\n".join(lines)


def auto_commit_push():
    """git add + commit + push（用于 --commit 模式，系统定时任务调用）。"""
    r = git(["add", "docs/plugin_updates.md", "docs/.plugin_updates_last.json"], ROOT)
    if r.returncode != 0:
        logging.error(f"git add failed: {r.stderr}")
        return
    r = git(["diff", "--cached", "--quiet"], ROOT)
    if r.returncode == 0:
        logging.info("No changes to commit.")
        return
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    r = git(["commit", "-m", f"chore: plugin update check {timestamp}"], ROOT)
    if r.returncode != 0:
        logging.error(f"git commit failed: {r.stderr}")
        return
    fgit = ROOT / "D:" / "Tool" / "fgit" / "fgit.exe"
    fgit_path = r"D:\Tool\fgit\fgit.exe"
    push_cmd = subprocess.run(
        [fgit_path, "push"],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        timeout=120,
        encoding="utf-8",
        errors="replace",
        creationflags=CREATEFLAGS,
    )
    if push_cmd.returncode == 0:
        logging.info("Pushed via fgit.")
    else:
        logging.error(f"fgit push failed: {push_cmd.stderr[:200]}")


def main():
    import sys
    do_commit = "--commit" in sys.argv

    results = []
    if PLUGINS.is_dir():
        for d in sorted(PLUGINS.iterdir()):
            if d.is_dir():
                results.append(check_one(d))
    timestamp = datetime.now().isoformat(timespec="seconds")
    payload = {"timestamp": timestamp, "root": str(ROOT), "results": results}
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    pending = {}
    if OUT_MD.exists():
        pending = parse_pending_advice(OUT_MD.read_text(encoding="utf-8"))

    md = render_md(timestamp, results, pending)
    OUT_MD.write_text(md, encoding="utf-8")

    n_updated = len([r for r in results if r["status"] == "updated"])
    logging.info(f"Checked {len(results)} plugins, {n_updated} updated. md rewritten.")

    if do_commit:
        auto_commit_push()


if __name__ == "__main__":
    main()