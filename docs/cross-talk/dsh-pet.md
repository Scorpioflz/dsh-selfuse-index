# dsh-pet — 桌宠前端开发

> 最后更新：2026-11-01 | 会话焦点：安装包快捷方式改名

## 正在进行

- 无进行中任务

## 已完成

- 今日共 5 个 commit 已推送到 GitHub（fade273d / 5f9c15bc / ed9822d3 / be51fa51 / 698cb53f）
- 修复 15 个 bug（含 2 个功能 bug + 13 个测试对齐），371+ tests passed, 0 failed
- 碎碎念不触发问题：根因是配置开关关闭，已帮用户开启
- 碎碎念定时计划模式：将 24h 滑动窗口改为 HH:MM + 星期筛选的定时计划，启动时回溯检查 (last_run, now] 间是否有计划点，错过多天合并为一次执行。新增 dsh_self_talk_schedule + dsh_self_talk_weekdays 配置键，30 个测试全部通过
- 安装包快捷方式改名：`packaging/dsh-pet-chubby_blue_whale.iss` 的 MyAppDisplay 从 "dsh-pet-chubby_blue_whale" 改为 "家养大肥鱼"，[Icons] 快捷方式名和 [Run] 启动描述改用 {#MyAppDisplay}。文件加 UTF-8 BOM 防止 Inno 按 ANSI 读取中文乱码。安装目录/安装包文件名保留英文 MyAppShortName 不变

## 遇到的困难

- 完整测试套件运行时 Qt segfault（既有问题，非本次变更引起）
- `test_low_priority_warm_interaction_yield.py` 线程 join 无超时（既有问题）

## 发现的经验

- `_gen_current(agent_key, gen)` 检查 `monitors.get(agent_key)`：非 DSH agent 无 monitor，`_on_agent_state` 直接 return。所有用 claude/cursor/opencode 调 `_on_agent_state` 的测试都是死代码路径
- cost tracking（`本轮消费 ¥X.XX`）只在 provider base_url 含 `deepseek.com` 时启用；dsh-webapi 默认指向 localhost，cost tracking 默认不激活
- pnpm install 命令现在带 `--config.package-import-method=copy` 参数
- 碎碎念有两套独立开关：`self_talk_enabled`（定时自动弹气泡，per-pet 键在 config-slot-N.json）+ `dsh_self_talk_enabled`（DSH API 每天生成候选词，全局键在 config.json）。`schedule_self_talk` 条件 `if not host._self_talk_enabled or not (host._self_talk_texts or host._self_talk_images): return`；`generate_self_talk` 还检查 `provider.provider_id == "dsh-webapi"`

## 对其他会话的通知/请求

- @dsh-cbw/memory：`project_context`/`task_state` 半衰期差异化待优化（目前与 `event` 同半衰期）
- dsh-cbw-bilibili P3（观看统计报告 + 收件箱分类）已有新会话实施