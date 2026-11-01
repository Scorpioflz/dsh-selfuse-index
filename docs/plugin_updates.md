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

> 最后检查：2026-11-01T22:03:51 | 2 个有更新，20 个已最新

### 在用插件 · 影响评估

- **billion-context**: `aeda157a0abc` → `760c24c55d02`（13 commits，最近: Merge pull request #5457 from ranxianglei/2026-11-01_fix-raw-sync-bookkeeping）
  - 影响评估: 无影响。v0.1.211 release，纯内部 storage/kernel 修复（async ingest drift-latch #5412、abort starvation #5415、frozen-envelope recovery #5408、golden test #5368）。billion-context 是寄生式压缩代理，自研部分不依赖其内部实现
- **dsh-persona-dafeiyu**: `fb81f4c366ee` → `ec706c087277`（1 commits，最近: Persist session picks so a restart stops wiping every session's persona）
  - 影响评估: [待分析]
- **dsh-skills-manager**: （无新更新，仍有未完成建议）
  - 影响评估: 无影响。纯 UI 响应式布局修复（`fix(ui): improve responsive layout on mobile and narrow viewports`），只改 client 端 `lib/client.js`/`src/client.ts`，不涉及自研部分依赖的 API/契约/配置面

### 参考插件 · 整合建议

- **dsh-fish-memory**: （无新更新，仍有未完成建议）
  - 整合建议: 无需整合。两变更（合并预览 UI 位置 #26、归档来源标记 ta.* + 管理接口鉴权）@dsh-cbw/memory 已有来源标记（P1 升级）和自管 client UI，无需借鉴
- **dsh-soul**: （无新更新，仍有未完成建议）
  - 整合建议: 暂不整合。2.0.0 大重构（+4341 行：独立记忆+图记忆 graph-memory.js+记忆动态 memory-dynamics.js+整合 consolidation.js）。核心评估不变：图记忆/经验编译对桌宠场景过重，@dsh-cbw/memory 的 bigram+半衰期更适合对话记忆。"独立记忆"思路 @dsh-cbw/memory 已具备
