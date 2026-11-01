# DSH 插件更新跟踪

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

## 当前待处理建议

> 最后检查：2026-11-01T10:17:21 | 4 个有更新，15 个已最新

### 在用插件 · 影响评估

- **billion-context**: `1876186c9912` → `7578e8184f91`（61 commits，最近: Merge pull request #5389 from ranxianglei/2026-11-01_blog-frequent-compression）
  - 影响评估: 无影响（对自研代码）。billion-context 是 DSH 平台层上下文压缩代理（npm `bili` CLI），自研部分（@dsh-pet/bridge、@dsh-cbw/memory、桌宠前端、人设模板）不直接调用其 API/CLI/配置面（grep 确认三个自研仓库均无 `billion-context` 引用）。57 commits 均为插件内部改进（pack editor #5345、estimate safety clamp #5291、CI runner queue optimize #5333、foreign block sweep #5343、cost USD restore #5338、zod bump #4880、launcher test xdg isolation #4960 等），不触及自研部分依赖的对外契约。
- **dsh-bili-scroll**: `a093f559e08d` → `398e4724a481`（3 commits，最近: fix: 合入社区 PR #150 + #162）
  - 影响评估: **需合入**——已 fork 为 `@dsh-cbw/bilibili`（`D:\DSH-Dev\dsh-cbw-bilibili`，v2.3.2 已发布到插件市场）。fork 基于 `a093f559e08d`，上游新增 3 commits 需评估合入：
    - `aadcdf7` fix(fav): 自动收藏连续四天全失败——`FavoriteList` 参数错位 + `FavoriteListResource` 已移除，改用 `Video.set_favorite`。fork 有 `lib/favops.py`，**需合入**
    - `398e472` #150 @ 昵称空格修复——B站只认紧挨着的 @，带空格对方收不到通知。fork index.js 有 mention 逻辑（29 处），**需合入**
    - `398e472` #162 私信 BV 号记录——私信发送后记下实际 BV 号让筛选能认出。fork 有私信投递逻辑，**需合入**
    - `a4941cb` chore(2.4.0) 版本 bump——fork 有独立版本号，**无需合入**
  - fork 当前状态：v2.3.2，已实现画像深度增强（时间权重+视频Tag+UP主签名）+ UP主偏好时间权重 + 画像兴趣词修复 + bili_comment 修复 + 四项功能改进。fork 仓库：github.com/Scorpioflz/dsh-cbw-bilibili
- **dsh-persona-dafeiyu**: `d939e74de288` → `fb81f4c366ee`（1 commits，最近: Release 0.7.3: hover feedback, and long text that no longer breaks the layout）
  - 影响评估: **无影响**。Release 0.7.3 纯前端 UI 改动（人设卡片 hover 反馈 + 长文本布局修复），不触及 API/契约/配置面。人设模板（`docs/大肥鱼_蓝鲸女仆人设模板.md`）是纯文本文件，不受插件 UI 改动影响。用户直接更新插件即可 ✅
- **dsh-skills-manager**: `3e7dc3a6e7cc` → `0cf5fb60ebcc`（14 commits，最近: chore(release): 1.2.25）
  - 影响评估: **无影响**。dsh-skills-manager 是 DSH 平台层技能管理插件，自研部分（@dsh-pet/bridge、@dsh-cbw/memory、桌宠前端、人设模板）不直接调用其 API/CLI/配置面。14 commits 均为版本发布相关（chore release 1.2.25），内部改进。用户直接更新插件即可 ✅

### 参考插件 · 整合建议

- **dsh-fish-memory**: `44f3db3b1c43` → `2a25e04a3d19`（2 commits，最近: 1.4.9：检查更新改成多源取最大、能一键装，命令行那套删了）
  - 整合建议: **无需整合**。1.4.9 是上游的更新检查机制（多源取最大）+ 安装流程（一键装）+ CLI 删除改动。@dsh-cbw/memory 有独立的安装/更新流程（已发布到插件市场，用 gh-proxy tarball URL 安装），不依赖上游的更新检查机制。@dsh-cbw/memory 无命令行接口，"命令行那套删了"不影响 ✅
