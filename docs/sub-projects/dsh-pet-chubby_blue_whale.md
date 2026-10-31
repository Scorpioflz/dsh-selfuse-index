# dsh-pet-chubby_blue_whale — 桌宠前端

> 本分片由桌宠开发会话维护。更新桌宠时改本文件，不碰根项目 README 主体。
> 根项目 README 仅保留全局架构图 + 插件职责表概览。

## 基本信息

- **本地路径**：`D:\DSH-Dev\dsh-pet-chubby_blue_whale`
- **仓库**：[Scorpioflz/dsh-pet-chubby_blue_whale](https://github.com/Scorpioflz/dsh-pet-chubby_blue_whale)
- **分支**：`main`
- **技术栈**：PySide6，Python 3.14+，uv 管理依赖，入口 `python -m pet`
- **继承自**：[MerZLin/dsh-pet-indesktop](https://github.com/MerZLin/dsh-pet-indesktop)（MIT），仅 Windows 11 验证通过

## 定位

仅做视觉交互（精灵图、右键菜单、设置 UI）。不含记忆/人设/provider 逻辑，全部后端工作交由 DSH。正朝通用前端/助手方向发展。

## 涉及的插件

| 插件 | 职责 | 来源 |
| --- | --- | --- |
| @dsh-pet/bridge | 桌宠状态桥接（屏幕/窗口同步） | 继承自 MerZLin/dsh-pet-indesktop，本地 `integrations/dsh-pet-bridge/` |
| @dsh-cbw/memory | 记忆后端（自研，派生自 fish-memory） | 独立仓库 [Scorpioflz/dsh-cbw-memory](https://github.com/Scorpioflz/dsh-cbw-memory) |
| hermes-pet-bridge | 桌宠桥接变体，未启用 | 本地 `integrations/hermes-pet-bridge/` |

## 架构要点

- `pet/chat/dsh_provider.py`：`DshWebApiProvider`，每角色一个 DSH 工作区
- `pet/dsh_workspace.py`：按角色绑定工作区
- `pet/chat/prompt.py`：`PromptBuilder.build_messages`，仅拼接 system prompt
- `pet/memory_plugin_link.py`：记忆插件安装检查与一键安装
- `integrations/`：桌宠相关 DSH 插件目录
- `pet/features.py` + `pet/feature_activation.py`：功能模块激活层

## 接入 DSH

通过 `dsh-web-service` 插件的会话 API（`/sessions/:id/prompt-stream`、`POST /sessions/:id/files`）接入 DSH。

## 许可证合规

- @dsh-cbw/memory 派生自 Yuuyuko-uu/dsh-fish-memory（Yuuyuko-uu 插件许可 1.2），独立仓库内 LICENSE + README 致谢段已合规
- @dsh-pet/bridge 继承自 MerZLin/dsh-pet-indesktop（MIT）

## 变更记录约定

改桌宠文件后同步更新桌宠仓库 README 的"修改文件/删除文件"部分（见记忆 `feedback_pet_readme_changelog.md`）。