# DSH 插件更新跟踪

本文件由定时任务（每小时）自动维护，记录 `_plugin-references/` 下各已安装 DSH 插件
上游仓库的更新情况与整合建议。每次检查的结果快照见 `docs/.plugin_updates_last.json`。

检查脚本：`scripts/check_plugin_updates.py`（遍历每个插件浅克隆，`git fetch` 比较远程
HEAD，有更新则 `git pull --ff-only` 并记录 commit 列表与文件变动）。

## 状态图例

- `updated` — 远程有新提交，已拉取
- `up_to_date` — 已是最新
- `fetch_error` / `pull_failed` — 网络或非快进更新，需人工介入
- `not_a_repo` / `no_head` — 目录非 git 仓库

## 更新记录

> 最新的更新记录追加在下方。无更新的检查轮次不在此记录。

### 2026-10-31 13:14 检查轮次

本轮 7 个插件有更新，13 个已最新。

- **billion-context**: `226c33893d33` → `fb5b91611a07`
  - 提交: 7294 个（v0.1.209 发布；主要含存储完整性 refuse-to-start、index.db quarantine、event-loop watchdog、session-resident 内存封顶、schema v10 + message timestamps 默认关闭、subagent lane token、prompt_cache_key 默认关闭等）
  - 变动文件: 270 个（`.claude-plugin/plugin.json`、`marketplace.json`、CI workflows、storage kernel 等）
  - 整合建议: 此为 DSH 存储/长上下文核心 fork，更新极频繁。本次引入 **schema v10 迁移**（messages.ts 列）与多项存储稳定性修复。升级后需**重启 DSH** 并观察 sessions 目录迁移；schema 迁移为 probe-first ALTER、不回填，对桌宠无直接前端影响，但 DSH 重启后应确认桌宠会话能正常加载。建议关注 v0.1.209 release notes 中 `promptCache.routing` 默认关闭的升级提示。

- **cc-safety-net**: `a84eb80e5e93` → `24b5e018d20f`
  - 提交: 23 个（v2.7.1；`fix(gate): retry Remove-Item and cmd deletes past a disabled home-cwd rule` 等）
  - 变动文件: 43 个（`plugin.json`、`dist/amp/cc-safety-net/` 等）
  - 整合建议: 安全网/命令门控插件。本次修复 workdir anchor 与删除重试逻辑。若 DSH 已安装此插件，需**重新 pnpm 安装**（`--config.package-import-method=copy`）以更新；变更涉及 gate 判定，建议复查桌宠经 DSH 执行的命令门控规则是否仍符合预期。

- **dsh-chat-manager**: `bbec76df9878` → `f9840bf66ef9`
  - 提交: 2 个（仅 CI/文档：`ci: maintain stable compatibility independently of next`）
  - 变动文件: 10 个（`.github/workflows/`、`AGENTS.md` 等）
  - 整合建议: 纯 CI/兼容性维护，**无功能变更**，无需跟进改造桌宠前端；本地参考源码已自动拉取，择机重启 DSH 即可。

- **dsh-fish-memory**: `2bb9be7b83ba` → `edc723d63809`
  - 提交: 8 个（**许可证变更**：改用 Yuuyuko-uu 插件许可 1.2，要求署名、禁止声称原创、违约须删除衍生作品）
  - 变动文件: 8 个（`LICENSE`、`CHANGELOG.md`、`README.md`、`lib/client.js`、`lib/index.js`、`package.json`）
  - 整合建议: ⚠️ **许可证从 MIT 改为自定义 Yuuyuko-uu 许可 1.2**。若在桌宠/DSH 集成中 redistribute 此插件或其衍生作品，须更新许可证声明并保留署名。功能层面无破坏性变更，记忆打分/半衰期逻辑未动；建议同步更新 README 中对该插件的许可证引用说明。

- **dsh-mnemon**: `fa4950616f8c` → `7cbdefc64c01`
  - 提交: 8 个（v0.5.37；`fix-516-evolution-scroll-boundary` 等）
  - 变动文件: 73 个（`.changeset/`、`docs/en/`、release-notes 等）
  - 整合建议: 助记记忆插件 v0.5.37。若 DSH 启用 mnemon，更新版本即可；注意与 **dsh-fish-memory 二选一**，避免双记忆后端造成注入冲突。

- **dsh-skills-manager**: `b69e64296ead` → `93f0c49acf33`
  - 提交: 10 个（1.2.23；`fix(core): harden error translation and verify dryRun` 等）
  - 变动文件: 29 个（`CHANGELOG.md`、`lib/core.js`、`lib/client.js`、`README.md` 等）
  - 整合建议: 技能管理插件 1.2.23，修复错误翻译与 dryRun。若 DSH 启用技能管理，更新版本并**重启 DSH** 生效；对桌宠无前端影响。

- **dsh-univer-office**: `8f85ce4074fd` → `c59332186fbd`
  - 提交: 15 个（0.3.9；`fix(client): folded floating window point/resize/move`、`remove duplicated Univer SDK copies`）
  - 变动文件: 304 个（多为构建产物；`README.md`、`docs/architecture.md` 等）
  - 整合建议: Univer 办公插件 0.3.9，修复浮动窗口交互与构建去重。若桌宠/DSH 使用 Univer 办公功能，**重新 pnpm 安装**更新版本；304 文件多为 dist 产物，源码逻辑变更较小。

<!-- NEW_ENTRIES_BELOW -->