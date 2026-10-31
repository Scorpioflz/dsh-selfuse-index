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

> 最后检查：2026-10-31T16:02:47 | 1 个有更新，18 个已最新

### 在用插件 · 影响评估

- **billion-context**: `afdf889cf701` → `2a499c1564bc`（30 commits，关键文件: src/fold-reconcile.ts、src/durable-message-guards.ts、src/chat-pack.ts、src/decompress-shared.ts、src/tunnel-guard.ts、CONFIGURATION.md）
  - 影响评估: 无影响。变更均为内部实现修复——折叠对账（#5142 fold-drift expected-rebase）、隧道 DNS 楔形诊断（#5224）、搜索折叠原文（#4154）、claude title sidecar 识别（#5135/#5136）、持久化消息守卫加固；唯一对外表面变化是 `compress.promptPack` 新增内置 `chat` 选项（#5319，向后兼容扩展，默认仍 `default`）。自研部分（@dsh-pet/bridge、@dsh-pet/memory、桌宠前端、人设模板）均不直接 import billion-context，也未在其配置中设置 compress.promptPack（使用默认值），不触及本次变更的任何对外表面。

### 参考插件 · 整合建议

（无待处理项）
