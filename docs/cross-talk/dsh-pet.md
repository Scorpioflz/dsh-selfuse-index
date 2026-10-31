# dsh-pet — 桌宠前端开发

> 最后更新：2026-10-31 | 会话焦点：非 DSH backend 移除后的测试修复

## 正在进行

- 桌宠子项目 `dsh-pet-chubby_blue_whale` 的测试修复已全部完成
- 今日共 5 个 commit 已推送到 GitHub（fade273d / 5f9c15bc / ed9822d3 / be51fa51 + 本次待提交）

## 遇到的困难

- 完整测试套件运行时 Qt segfault（既有问题，非本次变更引起）
- `test_low_priority_warm_interaction_yield.py` 线程 join 无超时（既有问题）

## 发现的经验

- `_gen_current(agent_key, gen)` 检查 `monitors.get(agent_key)`：非 DSH agent 无 monitor，`_on_agent_state` 直接 return。所有用 claude/cursor/opencode 调 `_on_agent_state` 的测试都是死代码路径
- cost tracking（`本轮消费 ¥X.XX`）只在 provider base_url 含 `deepseek.com` 时启用；dsh-webapi 默认指向 localhost，cost tracking 默认不激活
- pnpm install 命令现在带 `--config.package-import-method=copy` 参数

## 对其他会话的通知/请求

- @dsh-cbw/memory：`project_context`/`task_state` 半衰期差异化待优化（目前与 `event` 同半衰期）
- dsh-cbw-bilibili P3（观看统计报告 + 收件箱分类）已有新会话实施