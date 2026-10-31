# dsh-cbw-memory — DSH 记忆插件

> 本分片由记忆插件开发会话维护。更新记忆插件时改本文件，不碰根项目 README 主体。

## 基本信息

- **本地路径**：`D:\DSH-Dev\dsh-cbw-memory`（独立仓库）+ 桌宠 `integrations/dsh-pet-memory/`（打包目录）
- **仓库**：[Scorpioflz/dsh-cbw-memory](https://github.com/Scorpioflz/dsh-cbw-memory)
- **npm 包名**：`@dsh-cbw/memory`（注册名 `memory`）
- **许可证**：Yuuyuko-uu 插件许可 1.2（派生自 dsh-fish-memory）

## 定位

DSH 长期记忆后端，按工作区共享记忆（同一工作区多会话共用一份记忆），经 `systemPrompt.context` 注入。

## 派生关系

派生自 [Yuuyuko-uu/dsh-fish-memory](https://github.com/Yuuyuko-uu/dsh-fish-memory)，相对上游的改动：
- 记忆按工作区共享（上游按会话）
- `<system-reminder>` 等机器来源文本的检索过滤
- queryGate 小库保护门槛调整（0.8→0.5，记忆 <10 条时跳过打分归一化）
- 设置页「会话→工作区」归类入口
- 打包目录编码损坏修复
- 包名改为 `@dsh-cbw/memory`，注册名仍为 `memory`

## P0/P1 升级

请求检测、bigram 去重、recall 工具、自动归档、来源标记。

## 许可证合规

- `integrations/dsh-pet-memory/LICENSE`：逐字复制上游许可 + 派生声明附录
- `package.json`：license = `SEE LICENSE IN LICENSE`
- 桌宠 README 致谢段：含派生声明 + 改动清单
- `THIRD_PARTY_NOTICES.md`：第 0 节登记

## 参考源

- dsh-fish-memory（Yuuyuko-uu/dsh-fish-memory）— 参考源，未在 profile 安装
- dsh-mnemon（omdsh-dev/dsh-mnemon）— 已弃，与本插件冲突