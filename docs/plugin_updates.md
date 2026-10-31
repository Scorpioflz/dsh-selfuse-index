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

> 最后检查：2026-10-31T22:02:19 | 3 个有更新，16 个已最新

### 在用插件 · 影响评估

- **billion-context**: `d108df320978` → `1876186c9912`（57 commits，最近: Merge pull request #5147 from ranxianglei/2026-10-29_5146-bili-upstreams-endpoin）
  - 影响评估: 无影响（对自研代码）。billion-context 是 DSH 平台层上下文压缩代理（npm `bili` CLI），自研部分（@dsh-pet/bridge、@dsh-cbw/memory、桌宠前端、人设模板）不直接调用其 API/CLI/配置面（grep 确认三个自研仓库均无 `billion-context` 引用）。57 commits 均为插件内部改进（pack editor #5345、estimate safety clamp #5291、CI runner queue optimize #5333、foreign block sweep #5343、cost USD restore #5338、zod bump #4880、launcher test xdg isolation #4960 等），不触及自研部分依赖的对外契约。
- **dsh-bili-scroll**: `a093f559e08d` → `398e4724a481`（3 commits，最近: fix: 合入社区 PR #150 + #162）
  - 影响评估: 无影响（对自研代码）。核心 commit `3bd4868` 新增四项功能：(1) 值班轮可指定模型（`modelProvider`/`modelName` 配置字段 + `GET /api/bili-duty/models` 路由 + 设置页下拉）；(2) 「刷过的视频」按工作区显示（`GET /api/bili-duty/session-scope` + 隐藏探针）；(3) **会话归工作区 + 兜底归档**（`runDuty` 的 cwd 用设置里的 workspace，会话落在该工作区桶里；没配 workspace 时跑完归档）；(4) 超时看门狗（`runTimeoutMinutes` 默认 20，SIGTERM→5s→SIGKILL）。新增 Config 字段 `runTimeoutMinutes`/`modelProvider`/`modelName`（均 volatile，向后兼容），`bili_config` 工具描述扩展。自研部分（@dsh-pet/bridge、@dsh-cbw/memory、桌宠前端、人设模板）不调用 dsh-bili-scroll 的 HTTP API 或工具，不依赖其 Config/类型，不触及本次变更的任何表面对外契约。

### 参考插件 · 整合建议

- **dsh-fish-memory**: `edc723d63809` → `44f3db3b1c43`（1 commits，最近: 1.4.7：来源头把正文吞掉（整条不召回）；「按工作区」切了又弹回去；助手条目被标成 ta.）
  - 整合建议: @dsh-cbw/memory 会话需确认三个缺陷是否同样存在：(1) **来源头吞正文**——【QQ私聊】等来源头后紧跟正文（无空行），若整块跳过会把正文一起跳掉导致 query 为空、不召回。dsh-fish-memory 修复：自己的【你记得的事】整块跳，别人的来源头只丢表头那一行。(2) **/mode 路由 GET/POST 不分**——界面读状态用 GET 无请求体，被当 POST 写回配置导致切到「按工作区」后一刷新就弹回去。修复：只有 POST 改配置。(3) **提示词缺「讲助手自己的要写『我』」规则**——补上此规则避免助手条目被标成 ta.。三个均为 bug 修复非新功能，@dsh-cbw/memory 作为独立重写版本需自行评估是否有相同代码路径。
