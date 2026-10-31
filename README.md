# DSH Self-Use Index

This repository is an **index** for a set of self-use development projects built on top of
[DeepSeek Harness (DSH)](https://github.com/deepseek-ai/deepseek-harness) — an all-plugin
Cordis agent harness. It does **not** contain the source of any sub-project; instead it
points to each sub-project's own repository so they can be developed and versioned
independently.

## Purpose

- Serve as a single entry point for all personal DSH-related development work.
- Keep an up-to-date catalog of sub-projects with links and short descriptions.
- Track project-level documents (under `docs/`) that span multiple sub-projects.

## Sub-projects

> Each sub-project lives in its own folder under the workspace root and is an independent
> git repository. The folders themselves are git-ignored here — only this index repo and
> `docs/` are tracked.

| Name | Description | Repository |
| --- | --- | --- |
| dsh-pet-chubby_blue_whale | Desktop pet front-end for DSH (PySide6, Python 3.14+). Talks to DSH via the `dsh-web-service` session API. | [Scorpioflz/dsh-pet-chubby_blue_whale](https://github.com/Scorpioflz/dsh-pet-chubby_blue_whale) |

> When a new sub-project is added, append a row to the table above and add its folder
> to `.gitignore`.

## Workspace layout

```
DSH-Dev/                       # this index repo
├── README.md                  # this file (English)
├── README_ZH.md               # Chinese version
├── .gitignore
├── docs/                      # cross-project design notes and task docs
├── _plugin-references/        # shallow clones of installed DSH plugins (read-only, ignored)
├── deepseek-harness/          # upstream DSH source (read-only, ignored)
└── dsh-pet-chubby_blue_whale/ # desktop pet front-end (independent repo, ignored)
```

## References

- DSH upstream: [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness)
- Installed plugin sources used as reference are listed in `docs/plugin_installed.md`.