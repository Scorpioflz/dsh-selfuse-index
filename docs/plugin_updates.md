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

> 最后检查：2026-10-31T17:02:49 | 2 个有更新，17 个已最新 | 均无影响，无需操作

### 在用插件 · 影响评估

- **billion-context**: `2a499c1564bc` → `f6e69aee195c`（8 commits，关键: #4954/#4952 zcode 项目记忆提取会话隔离）
  - 影响评估: 无影响。核心改动 `aa479bc2` 在 `src/server/handle.ts` + `src/session-id.ts` 新增 `zcodeMemoryConversation()`，通过特定 header（`x-zcode-query-source: project_memory_extract` + `x-zcode-session-type: other` + `x-query-id`）识别 zcode 工具的记忆提取请求，为其生成隔离会话 ID（`${parent}|aux:zcode-memory:${query}`），并在会话路由中跳过 plugin binding/prompt-cache-key/pluginMode 等逻辑，使记忆提取 worker 不继承父会话的工具绑定。其余 7 个 commits 均为 merge commits。自研部分（@dsh-pet/bridge、@dsh-pet/memory、桌宠前端、人设模板）不发送 zcode 专用 header，不经由 zcode 记忆提取通道，不触及本次变更的任何表面对外契约。

- **dsh-skills-manager**: `93f0c49acf33` → `3e7dc3a6e7cc`（6 commits，关键: #73 自定义技能笔记 + 4 个 bug fix + release 1.2.24）
  - 影响评估: 无影响。`03496d1` (feat) 新增 `setSkillNote()` 及 `POST /skill-note` 路由，`ManagerState.customNotes` + `SkillView.customNote` 字段（均可选，旧状态文件可缺省，向后兼容）；`c7150a9`/`bda8036`/`12b0ced`/`df7b6de` 修复活跃笔记被 trash purge 误删、历史自定义源 fail-closed、清理逻辑直接操作 raw document 等内部缺陷。自研部分不调用 dsh-skills-manager 的 HTTP API（桌宠前端经 dsh-web-service 会话 API 接入，不直接集成技能管理），不依赖其 ManagerState/SkillView 类型，不触及本次变更的任何表面对外契约。

### 参考插件 · 整合建议

（无待处理项）
