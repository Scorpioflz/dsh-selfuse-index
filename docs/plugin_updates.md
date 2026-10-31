# DSH 插件更新跟踪

本文件由定时任务（每小时）自动维护，记录 `_plugin-references/` 下各 DSH 插件上游仓库的
更新情况。每次检查的结果快照见 `docs/.plugin_updates_last.json`。

检查脚本：`scripts/check_plugin_updates.py`（遍历每个插件浅克隆，`git fetch` 比较远程
HEAD，有更新则 `git pull --ff-only` 并记录 commit 列表与文件变动）。

## 分类处理规则

更新记录按插件状态（见 README.md 插件职责表「状态」列）分两类，**处理目的不同**：

- **在用插件**（状态 = 在用 / in use）→ **影响评估**：只分析变更是否影响自研部分
  （`@dsh-pet/bridge`、`@dsh-pet/memory`、桌宠前端、人设模板）依赖的 API/契约/配置面。
  无影响则写「无影响」。**不写整合建议**——直接安装的插件，更新即更新。
- **参考/已弃插件**（状态含 ref / superseded / 参考 / 已弃）→ **整合建议**：分析上游
  变更中哪些有用部分可整合进对应自研插件（如 dsh-fish-memory → @dsh-pet/memory、
  dsh-pet-indesktop-upstream → 桌宠前端/@dsh-pet/bridge 等）。

## 状态图例

- `updated` — 远程有新提交，已拉取
- `up_to_date` — 已是最新
- `fetch_error` / `pull_failed` — 网络或非快进更新，需人工介入
- `not_a_repo` / `no_head` — 目录非 git 仓库

## 更新记录

> 最新的更新记录追加在下方。无更新的检查轮次不在此记录。

<!-- NEW_ENTRIES_BELOW -->

### 2026-10-31 13:14 检查轮次

本轮 7 个插件有更新，13 个已最新。按状态分两组处理。

#### 在用插件 · 影响评估

- **billion-context**: `226c33893d33` → `fb5b91611a07`（7294 commits，v0.1.209；schema v10 迁移 + 存储稳定性 + event-loop watchdog + promptCache 默认关闭）
  - 影响评估: ⚠️ **可能影响**。schema v10 引入 `messages.ts` 列（probe-first ALTER、不回填、timestamps 默认关闭）。`@dsh-pet/memory` 经 `systemPrompt.context` 注入记忆，不直接依赖存储 schema，但 DSH 重启后 sessions 迁移若失败会影响桌宠会话加载。`promptCache.routing` 默认关闭不影响自研。建议：重启 DSH 后确认桌宠会话正常加载、记忆注入未异常。
- **cc-safety-net**: `a84eb80e5e93` → `24b5e018d20f`（23 commits，v2.7.1；gate 删除重试 + workdir anchor 修复）
  - 影响评估: **无影响**。自研部分不依赖 cc-safety-net 的 gate 内部逻辑；它只做命令门控，桌宠/自研插件不直接调用其 API。重新 pnpm 安装即可。
- **dsh-chat-manager**: `bbec76df9878` → `f9840bf66ef9`（2 commits，仅 CI/文档：stable compatibility）
  - 影响评估: **无影响**。纯 CI/兼容性维护，无功能变更。
- **dsh-skills-manager**: `b69e64296ead` → `93f0c49acf33`（10 commits，1.2.23；error translation + dryRun 修复）
  - 影响评估: **无影响**。自研部分不依赖 skills-manager 的内部 API；变更在 core/client 错误翻译，不影响外部契约。重启 DSH 生效。
- **dsh-univer-office**: `8f85ce4074fd` → `c59332186fbd`（15 commits，0.3.9；浮动窗口修复 + Univer SDK 构建去重）
  - 影响评估: **无影响**。自研部分不使用 Univer 办公功能；变更多为构建产物 + 浮动窗口交互。重新 pnpm 安装即可。

#### 参考插件 · 整合建议

- **dsh-fish-memory**: `2bb9be7b83ba` → `edc723d63809`（8 commits；**许可证变更 MIT → Yuuyuko-uu 1.2**：要求署名、禁止声称原创、违约须删除衍生作品）
  - 整合建议: `@dsh-pet/memory` 借鉴了 fish-memory 的打分公式思路，本次许可证变更需**同步更新 @dsh-pet/memory 的许可证声明**（若 redistribute，保留 fish-memory 署名引用）。功能层面无新可整合思路；后续持续关注 fish-memory 的打分公式/半衰期算法变更，若有优化可同步到 @dsh-pet/memory。
- **dsh-mnemon**: `fa4950616f8c` → `7cbdefc64c01`（8 commits，v0.5.37；evolution scroll boundary 修复）
  - 整合建议: dsh-mnemon 与 @dsh-pet/memory 职责重叠但未启用。本次修复 evolution scroll boundary——可**对比 dsh-mnemon 的 evolution/scroll 边界处理**，评估 @dsh-pet/memory 是否需要类似机制（若 @dsh-pet/memory 有记忆演化/滚动逻辑）。低优先，仅思路参考。