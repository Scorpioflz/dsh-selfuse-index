# DSH 插件更新跟踪

本文件由定时任务（每小时）**覆盖式**维护，只保留**尚未执行**的建议操作。
已实施的变更（建议行标记 ✅）在下次运行时自动清除，避免文件无限增长。
完整检查快照见 `docs/.plugin_updates_last.json`。

检查脚本：`scripts/check_plugin_updates.py`（遍历每个插件浅克隆，`git fetch` 比较
远程 HEAD，有更新则 `git pull --ff-only` 并记录 commit 列表与文件变动）。

## 分类处理规则

- **在用插件** → **影响评估**：只分析变更是否影响自研部分
  （`@dsh-pet/bridge`、`@dsh-pet/memory`、桌宠前端、人设模板）依赖的 API/契约/配置面。
  无影响则写「无影响」。不写整合建议——直接安装的插件，更新即更新。
- **参考/已弃插件** → **整合建议**：分析上游变更中哪些有用部分可整合进对应自研插件
  （如 dsh-fish-memory → @dsh-pet/memory、dsh-pet-indesktop-upstream → 桌宠前端等）。

## 状态图例

- `updated` — 远程有新提交，已拉取
- `up_to_date` — 已是最新
- `fetch_error` / `pull_failed` — 网络或非快进更新，需人工介入
- `not_a_repo` / `no_head` — 目录非 git 仓库

## 当前待处理建议

> 最后检查：2026-10-31T15:02:52 | 1 个有更新，18 个已最新

### 在用插件 · 影响评估

- **billion-context**: `a34a65a931ce` → `afdf889cf701`（18 commits，最近: Merge pull request #5305 from ranxianglei/2026-10-31_codex-catalog-window）
  - 影响评估: **无影响**。本次 18 个提交均为 billion-context 内部代理管道优化与 bug 修复（codex 模型目录对齐 #5243/#5305、代理热路径性能优化 #5130、relay/loop 修复、孪生持久化门控 #4977/#5004、测试补齐），变更文件全部在 `src/` 和 `tests/` 下，未触及 `package.json` exports / `CONFIGURATION.md` / `dsh.bundle.patch.yml` 等对外 API/配置面/DSH 集成接口。自研部分（@dsh-pet/bridge、@dsh-pet/memory、桌宠前端、人设模板）不直接 import billion-context 内部模块，仅依赖其作为 DSH 插件的上下文压缩行为契约，该契约未变。

### 参考插件 · 整合建议

（无待处理项）
