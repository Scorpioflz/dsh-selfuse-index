# AGENTS.md — DSH-Dev 工作区约定

> 本文件是项目级强制约定，所有在此工作区启动的 AI 对话**必须遵守**。

## 启动时必须执行（强制）

1. **读取 `docs/cross-talk/` 全目录**：了解其他会话在做什么、有无对自己的通知/请求
2. **读取自己的 `docs/cross-talk/<sub-project>.md`**：确认上次状态，准备更新
3. **读取 `docs/github-operations.md`**：GitHub 操作规范（认证/克隆/推送/提交）
4. **检查 `docs/plugin_updates.md` 有无 `[待分析]` 条目**：系统定时任务（每天 22:00）自动检查插件更新并生成待分析占位，会话启动时若有 `[待分析]` 条目需主动分析填写（影响评估/整合建议），填写后提交推送

## 工作中必须执行（强制）

1. **更新自己的 `docs/cross-talk/<sub-project>.md`**：有进展/困难/经验/跨会话通知时覆盖式更新
2. **只改自己的文件**：
   - 子项目会话：改子项目仓库 + `docs/sub-projects/<自己的分片>` + `docs/cross-talk/<自己的文件>`
   - **不碰 README 主体、其他分片、其他 cross-talk 文件**
3. **根项目协调会话**：负责 README 主体 + 跨项目文档 + 插件更新跟踪，不碰子项目代码
4. **回复其他会话的请求**：启动时读全目录后，逐个检查其他会话文件的"对其他会话的通知/请求"段有无给自己派的任务；确认已完成后，**在自己的 cross-talk 文件"对其他会话的通知/请求"段留回复**（格式：`→ @<对方会话>：<事项> 已完成/已处理`）。对方下次启动读全目录时能看到回复

## 提交推送

- **所有 git 指令可用 fgit**：`D:/Tool/fgit/fgit.exe <子命令>` 替代普通 git（add/commit/status/push 等），大仓库更快；**bash 工具里不要加 `2>&1`**（会导致超时，去掉后秒完成）
- **逐条执行**：不要 chained `&&`，逐条 add → commit → push，每步确认成功
- **暂存**：只 `git add` 相关文件，**不要 `git add -A`**
- **push 前 rebase**：`git pull --rebase origin main` 后再 push，避免并行冲突
- **克隆**：用 `https://gh-proxy.com/https://github.com/...` 镜像前缀
- **fgit 超时不一定是失败**：可能已推送完成，下次 fgit 同命令显示 up-to-date 即可确认

## 文档结构

```
docs/
  cross-talk/          ← 会话沟通区（动态状态，各会话只改自己的文件）
  sub-projects/        ← 子项目分片（静态描述，各会话只改自己的分片）
  plugin_updates.md    ← 插件更新跟踪（系统定时任务自动生成，覆盖式）
  github-operations.md ← GitHub 操作指南（本地不追踪）
```

## 定时任务

- **插件更新检查**：Windows 定时任务 `DSH-PluginUpdateCheck`，每天 22:00 运行 `python scripts/check_plugin_updates.py --commit`（纯脚本，不创建 AI 对话）
- 脚本自动 git 检查 + 生成 `plugin_updates.md` + commit + fgit push
- 有更新时留 `[待分析]` 占位，会话启动时 AI 主动分析填写

## 仓库

- **index 仓库** `D:\DSH-Dev` → `github.com/Scorpioflz/dsh-selfuse-index`（main）
- **桌宠仓库** `D:\DSH-Dev\dsh-pet-chubby_blue_whale` → `github.com/Scorpioflz/dsh-pet-chubby_blue_whale`（main）
- **记忆插件仓库** `D:\DSH-Dev\dsh-cbw-memory` → `github.com/Scorpioflz/dsh-cbw-memory`（main）
- git 作者：`Scorpioflz / fanlinze@petalmail.com`