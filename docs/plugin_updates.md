# DSH 插件更新跟踪

本文件由定时任务（每天 22:00）**覆盖式**维护，只保留**尚未执行**的建议操作。
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

## 当前待处理建议

> 最后检查：2026-10-31T18:02:29 | 2 个有更新，17 个已最新

### 在用插件 · 影响评估


- **dsh-bili-scroll**: `2c7b3f14f525` → `a093f559e08d`（2 commits，最近: Merge pull request #111 from pentyum/feat/duty-model-scope-timeout）
  - 影响评估: 无影响（对自研代码）。核心 commit `3bd4868` 新增四项功能：(1) 值班轮可指定模型（`modelProvider`/`modelName` 配置字段 + `GET /api/bili-duty/models` 路由 + 设置页下拉）；(2) 「刷过的视频」按工作区显示（`GET /api/bili-duty/session-scope` + 隐藏探针）；(3) **会话归工作区 + 兜底归档**（`runDuty` 的 cwd 用设置里的 workspace，会话落在该工作区桶里；没配 workspace 时跑完归档）；(4) 超时看门狗（`runTimeoutMinutes` 默认 20，SIGTERM→5s→SIGKILL）。新增 Config 字段 `runTimeoutMinutes`/`modelProvider`/`modelName`（均 volatile，向后兼容），`bili_config` 工具描述扩展。自研部分（@dsh-pet/bridge、@dsh-cbw/memory、桌宠前端、人设模板）不调用 dsh-bili-scroll 的 HTTP API 或工具，不依赖其 Config/类型，不触及本次变更的任何表面对外契约。
  - ⚠️ **任务2方案已被上游解决**：`docs/task2-bili-scroll-fixed-session.md` 的方案 A（固定会话复用 sessionId + compaction 兜底）已被上游以"会话归工作区桶 + 归档兜底"方式实现。建议将该方案文档标记为「已由上游实现（commit 3bd4868，v2.3.x）」，避免重复自研；如需固定 sessionId 复用仍可向上游提 PR，但工作区归组已满足"避免工作区混乱"的原始诉求。

### 参考插件 · 整合建议

（无待处理项）
