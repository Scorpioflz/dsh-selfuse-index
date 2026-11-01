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

> 最后检查：2026-11-01T10:17:21 | 4 个有更新，15 个已最新

### 在用插件 · 影响评估

- **billion-context**: `1876186c9912` → `7578e8184f91`（61 commits，最近: Merge pull request #5389 from ranxianglei/2026-11-01_blog-frequent-compression）
  - 影响评估: 无影响（对自研代码）。billion-context 是 DSH 平台层上下文压缩代理（npm `bili` CLI），自研部分（@dsh-pet/bridge、@dsh-cbw/memory、桌宠前端、人设模板）不直接调用其 API/CLI/配置面（grep 确认三个自研仓库均无 `billion-context` 引用）。57 commits 均为插件内部改进（pack editor #5345、estimate safety clamp #5291、CI runner queue optimize #5333、foreign block sweep #5343、cost USD restore #5338、zod bump #4880、launcher test xdg isolation #4960 等），不触及自研部分依赖的对外契约。
- **dsh-bili-scroll**: （无新更新，仍有未完成建议）
  - 影响评估: **需关注**——已 fork 为 `@dsh-cbw/bilibili`（`D:\DSH-Dev\dsh-cbw-bilibili`，v2.3.1 已发布到插件市场）。上游 commit `3bd4868` 新增四项功能：(1) 值班轮可指定模型；(2) 「刷过的视频」按工作区显示；(3) 会话归工作区 + 兜底归档；(4) 超时看门狗。fork 已合入这些功能（基于 `a093f559e08d` fork），并额外实现四项改进（人设开关/兴趣整合/画像查看/数据路径分离）。**后续上游若有新提交，需评估是否值得 rebase 合入 fork**。fork 仓库：github.com/Scorpioflz/dsh-cbw-bilibili
- **dsh-persona-dafeiyu**: `d939e74de288` → `fb81f4c366ee`（1 commits，最近: Release 0.7.3: hover feedback, and long text that no longer breaks the layout）
  - 影响评估: [待分析]
- **dsh-skills-manager**: `3e7dc3a6e7cc` → `0cf5fb60ebcc`（14 commits，最近: chore(release): 1.2.25）
  - 影响评估: [待分析]

### 参考插件 · 整合建议

- **dsh-fish-memory**: `44f3db3b1c43` → `2a25e04a3d19`（2 commits，最近: 1.4.9：检查更新改成多源取最大、能一键装，命令行那套删了）
  - 整合建议: [待分析]
