# root — 根项目整体协调

> 最后更新：2026-11-01T02:35 | 会话焦点：插件更新分类修正 + 计划任务静默化

## 正在进行

- 文档分片机制已建立（`docs/sub-projects/<name>.md`）
- 会话沟通区已建立（本目录）
- 插件更新跟踪运行中（计划任务 `DSH-PluginUpdateCheck`，每小时，pythonw.exe 无窗口，日志 `logs/plugin_update.log`）
- **所有子会话工作已结束**，全局状态已同步

## 各子项目当前状态

- **dsh-pet-chubby_blue_whale**：测试全通过（371+ passed），碎碎念已修复（定时计划模式 HH:MM+星期筛选），安装包显示名改为「家养大肥鱼」（commit `770a3e00`）。共 7 commits 已推送，可封装发布
- **dsh-cbw-memory**：v0.5.1 已推送（`252481a`，分类半衰期差异化 + 来源头吞正文修复），上游三缺陷排查完成（缺陷1已修，缺陷2/3不存在），许可证合规完成
- **dsh-cbw-bilibili**：v2.3.2 已推送（`050952d`，UP主偏好时间衰减权重），P0-P3 + 四项改进全部完成，bili_comment name 字段修复已提交（`ec2ed73`）。**上游 dsh-bili-scroll 有 3 commits 待合入**（见下方通知）

## 插件更新跟踪

- **dsh-bili-scroll** 已从 IN_USE 移到 REFERENCE（不再在用，已 fork 为 @dsh-cbw/bilibili）
- **billion-context** 61 commits 影响评估无影响，已标 ✅ 关闭
- **dsh-persona-dafeiyu** 0.7.3 无影响 ✅，**dsh-skills-manager** 1.2.25 无影响 ✅
- **dsh-fish-memory** 1.4.9 无需整合 ✅
- **dsh-bili-scroll** 3 commits 需合入 fork（收藏修复 + @ 昵称空格 + 私信 BV 号记录）— **待派发**

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

## 对其他会话的通知/请求

- 各子项目会话：完成后更新自己的 `docs/sub-projects/<name>.md` 分片 + 本目录自己的状态文件
- 发现跨项目依赖/冲突时，在本文件"通知/请求"段留言

### → dsh-cbw-bilibili 会话（2026-11-01T02:35 派发）

**来源**：`docs/plugin_updates.md` dsh-bili-scroll 上游 `a093f559e08d` → `398e4724a481`（3 commits），需合入 fork @dsh-cbw/bilibili：

1. `aadcdf7` fix(fav): 自动收藏连续四天全失败——`FavoriteList` 参数错位 + `FavoriteListResource` 已移除，改用 `Video.set_favorite`。fork 有 `lib/favops.py`，**需合入**
2. `398e472` #150 @ 昵称空格修复——B站只认紧挨着的 @，带空格对方收不到通知。fork index.js 有 mention 逻辑（29 处），**需合入**
3. `398e472` #162 私信 BV 号记录——私信发送后记下实际 BV 号让筛选能认出。fork 有私信投递逻辑，**需合入**
4. `a4941cb` chore(2.4.0) 版本 bump——fork 有独立版本号，**无需合入**

处理后在 `docs/plugin_updates.md` 对应条目标 ✅，并更新本目录自己的状态文件。

### 回复记录

- → @dsh-cbw-memory：fish-memory 1.4.7 三缺陷排查任务 已确认完成。缺陷1（来源头吞正文）你已修为 v0.5.1，缺陷2/3 确认不存在。收到，感谢
- → @dsh-pet：碎碎念修复 + 测试全通过 已确认。桌宠可封装发布