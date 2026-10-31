# dsh-pet — 桌宠前端开发

> 最后更新：2026-10-31 | 会话焦点：非 DSH backend 移除后的测试修复 + 碎碎念调查

## 正在进行

- 无进行中任务。桌宠子项目 `dsh-pet-chubby_blue_whale` 测试全部通过，碎碎念问题已解决，可封装发布

## 已完成

- 今日共 5 个 commit 已推送到 GitHub（fade273d / 5f9c15bc / ed9822d3 / be51fa51 / 698cb53f）
- 修复 15 个 bug（含 2 个功能 bug + 13 个测试对齐），371+ tests passed, 0 failed
- 碎碎念不触发问题：根因是配置开关关闭（`self_talk_enabled = False` + `dsh_self_talk_enabled = False`），非代码 bug。已帮用户开启两个开关，下次启动碎碎念会正常触发

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