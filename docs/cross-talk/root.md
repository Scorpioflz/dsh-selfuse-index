# root — 根项目整体协调

> 最后更新：2026-10-31T23:30 | 会话焦点：全局审计 + 经验总结

## 正在进行

- 文档分片机制已建立（`docs/sub-projects/<name>.md`）
- 会话沟通区已建立（本目录）
- 插件更新跟踪运行中（cron `cac53447`，每小时，覆盖式 + keep-until TTL）

## 各子项目当前状态

- **dsh-pet-chubby_blue_whale**：测试全通过（371+ passed），碎碎念已修复，可封装发布。非 DSH backend 已全部移除（commit `cc881933`）
- **dsh-cbw-memory**：v0.5.1 已推送（分类半衰期差异化 + 来源头吞正文修复），上游三缺陷排查完成（缺陷1已修，缺陷2/3不存在），许可证合规完成
- **dsh-cbw-bilibili**：P0-P3 全部完成，bili_comment 工具 name 字段缺失已修复（commit `ec2ed73`），四项功能改进已推送（人设开关/兴趣整合/画像查看/数据路径分离）

## 遇到的困难

- fgit push 偶发超时（300s），但实际推送通常已完成（下次 fgit 显示 up-to-date）
- index 仓库 git status 因大量未跟踪文件超时，提交时直接 git add 指定文件跳过 status

## 发现的经验

- 子项目更新常涉及根项目文档同步，分片 + rebase 兜底可有效避免冲突
- 覆盖式更新比追加式更适合状态类文档（不会无限增长）
- **推送时每个 git 指令逐条在 cmd 中执行更快**（而非 chained && ），尤其在大仓库
- **defineTool 工具必须含 name 字段**：缺失会导致 ToolSchema.name = undefined，DSH 的 snapshotJsonValue 比 JSON.stringify 更严格（拒绝含 undefined 字段的对象），session.append('request/header') 抛 "non-JSON-serializable" 错误。宿主 tools.register 不验证 name 是字符串，是防御缺口

## 对其他会话的通知/请求

- 各子项目会话：完成后更新自己的 `docs/sub-projects/<name>.md` 分片 + 本目录自己的状态文件
- 发现跨项目依赖/冲突时，在本文件"通知/请求"段留言