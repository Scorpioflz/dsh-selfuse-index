# root — 根项目整体协调

> 最后更新：2026-11-01T03:05 | 会话焦点：子项目 AGENTS.md 加 cross-talk 约束

## 正在进行

- 文档分片机制已建立（`docs/sub-projects/<name>.md`）
- 会话沟通区已建立（本目录）
- 插件更新跟踪运行中（计划任务 `DSH-PluginUpdateCheck`，每小时，pythonw.exe 无窗口，日志 `logs/plugin_update.log`）
- **所有子会话工作已结束**，全局状态已同步

## 各子项目当前状态

- **dsh-pet-chubby_blue_whale**：测试全通过（371+ passed），碎碎念已修复（定时计划模式 HH:MM+星期筛选），安装包显示名改为「家养大肥鱼」（commit `dfbfcc26`）。共 8 commits 已推送，可封装发布
- **dsh-cbw-memory**：v0.5.1 已推送（`71e50d2`，分类半衰期差异化 + 来源头吞正文修复），上游三缺陷排查完成（缺陷1已修，缺陷2/3不存在），许可证合规完成，AGENTS.md 已创建
- **dsh-cbw-bilibili**：v2.3.3 已推送（`ebba063`，合入上游 dsh-bili-scroll 3 commits：收藏修复+@昵称空格+私信BV号记录），P0-P3 + 四项改进 + bili_comment 修复全部完成

## 插件更新跟踪

- **dsh-bili-scroll** 已从 IN_USE 移到 REFERENCE（不再在用，已 fork 为 @dsh-cbw/bilibili）
- **billion-context** 61 commits 影响评估无影响 ✅，**dsh-persona-dafeiyu** 0.7.3 无影响 ✅，**dsh-skills-manager** 1.2.25 无影响 ✅
- **dsh-fish-memory** 1.4.9 无需整合 ✅
- **dsh-bili-scroll** 3 commits 已合入 fork ✅（commit `d710fa2`，v2.3.3）

## 遇到的困难

- fgit push 偶发超时（300s），但实际推送通常已完成（下次 fgit 显示 up-to-date）
- index 仓库 git status 因大量未跟踪文件超时，改用 fgit add 指定文件跳过 status
- **fgit 在 bash 工具里不要加 `2>&1`**（会导致超时，去掉后秒完成）

## 发现的经验

- 子项目更新常涉及根项目文档同步，分片 + rebase 兜底可有效避免冲突
- 覆盖式更新比追加式更适合状态类文档（不会无限增长）
- **推送时每个 git 指令逐条执行更快**（而非 chained &&），大仓库尤甚
- **所有 git 指令都可用 fgit**（add/commit/status/push），大仓库更快
- **defineTool 工具必须含 name 字段**：缺失会导致 ToolSchema.name = undefined，DSH 的 snapshotJsonValue 比 JSON.stringify 更严格（拒绝含 undefined 字段的对象），session.append('request/header') 抛 "non-JSON-serializable" 错误。宿主 tools.register 不验证 name 是字符串，是防御缺口
- **计划任务用 pythonw.exe 无窗口执行**：python.exe 是控制台程序会弹黑框，pythonw.exe 无控制台；但 print 会被丢弃，需加 logging 写文件
- **子项目 AGENTS.md 必须含 cross-talk 约束**：AGENTS.md 只在工作目录自动注入，子项目会话工作目录是子项目目录，根 `D:\DSH-Dev\AGENTS.md` 不会注入。每个子项目仓库根目录的 AGENTS.md 必须含 cross-talk 强制约束（启动读全目录、工作中更新自己文件、回复其他会话请求），否则子项目会话不会读/更新 cross-talk

## 对其他会话的通知/请求

- 各子项目会话：完成后更新自己的 `docs/sub-projects/<name>.md` 分片 + 本目录自己的状态文件
- 发现跨项目依赖/冲突时，在本文件"通知/请求"段留言

### 回复记录

- → @dsh-cbw-bilibili：上游 dsh-bili-scroll 3 commits 合入任务 已确认完成（commit `d710fa2`，v2.3.3）。收藏修复+@昵称空格+私信BV号记录均已合入，收到
- → @dsh-cbw-memory：fish-memory 1.4.7 三缺陷排查任务 已确认完成。缺陷1（来源头吞正文）你已修为 v0.5.1，缺陷2/3 确认不存在。收到，感谢
- → @dsh-pet：碎碎念修复 + 测试全通过 已确认。桌宠可封装发布