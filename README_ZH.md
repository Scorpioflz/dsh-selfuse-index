# DSH 自用开发索引

本仓库是一套基于 [DeepSeek Harness (DSH)](https://github.com/deepseek-ai/deepseek-harness)
（all-plugin Cordis agent harness）的自用相关开发项目的**索引**。它**不包含**任何子项目的
源代码，而是指向各子项目各自的仓库，使其可以独立开发与版本管理。

## 用途

- 作为所有个人 DSH 相关开发工作的统一入口。
- 维护子项目清单，提供链接与简要说明。
- 跟踪跨子项目的项目级文档（位于 `docs/`）。

## 子项目

> 每个子项目位于工作区根目录下各自的文件夹中，是独立的 git 仓库。这些文件夹在本索引
> 仓库中被 git-ignore，仅本索引仓库与 `docs/` 被跟踪。

| 名称 | 说明 | 仓库 |
| --- | --- | --- |
| dsh-pet-chubby_blue_whale | DSH 桌宠前端（PySide6，Python 3.14+），通过 `dsh-web-service` 会话 API 接入 DSH。 | [Scorpioflz/dsh-pet-chubby_blue_whale](https://github.com/Scorpioflz/dsh-pet-chubby_blue_whale) |

> 新增子项目时，在上表追加一行，并将其文件夹加入 `.gitignore`。

## 工作区结构

```
DSH-Dev/                       # 本索引仓库
├── README.md                  # 英文说明
├── README_ZH.md               # 中文说明（本文件）
├── .gitignore
├── docs/                      # 跨子项目的设计与任务文档
├── _plugin-references/        # 已安装 DSH 插件的浅克隆源码（只读，已忽略）
├── deepseek-harness/          # DSH 上游源码（只读，已忽略）
└── dsh-pet-chubby_blue_whale/ # 桌宠前端（独立仓库，已忽略）
```

## 参考

- DSH 上游：[deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness)
- 作为参考的已安装插件源码清单见 `docs/plugin_installed.md`。