# GitHub 操作注意事项

> 最后更新：2026-11-01 | 已纳入 git 追踪

## 1. 仓库清单

| 仓库 | 本地路径 | 远程地址 | 分支 | 用途 |
| --- | --- | --- | --- | --- |
| dsh-selfuse-index | `D:\DSH-Dev` | `github.com/Scorpioflz/dsh-selfuse-index` | `main` | 索引仓库，统一入口 |
| dsh-pet-chubby_blue_whale | `D:\DSH-Dev\dsh-pet-chubby_blue_whale` | `github.com/Scorpioflz/dsh-pet-chubby_blue_whale` | `main` | 桌宠前端 |
| dsh-cbw-memory | `D:\DSH-Dev\dsh-cbw-memory` | `github.com/Scorpioflz/dsh-cbw-memory` | `main` | DSH 记忆插件（独立仓库） |

> `D:\DSH-Dev` 下每个子文件夹是独立项目 + 独立 git 仓库，非 monorepo。
> `deepseek-harness/` 和 `_plugin-references/` 是只读参考，不在 index 仓库追踪范围内（.gitignore 排除）。

## 2. 认证

- **git 作者**：`Scorpioflz` / `fanlinze@petalmail.com`
- **GitHub 认证**：通过 Git Credential Manager (GCM) 自动管理，已配置好无需手动输入
- **获取 token**（如需 API 操作）：`git credential fill`，输入 `protocol=https` + `host=github.com`，返回的 password 字段即 token（`gho_...` 格式）。**token 只放 shell 变量，禁止打印**
- **fgit 认证**：`D:\Tool\fgit\fgit.exe` 已内置认证配置，直接 push 即可

## 3. 克隆（拉取）

国内无法稳定连接 `github.com:443`，直连会超时。**必须使用镜像代理**：

```bash
# 主选：gh-proxy.com 镜像前缀（已验证可用）
git clone --depth 1 https://gh-proxy.com/https://github.com/<user>/<repo>.git

# 备选：kkgithub.com（可能有 SNI/证书问题）
git clone --depth 1 https://kkgithub.com/<user>/<repo>.git
```

- 先试 gh-proxy.com，失败再问用户是否有 VPN/代理可开
- 浅克隆 `--depth 1` 足够参考用途，节省时间和空间
- 已克隆的仓库更新用 `git pull`（本地已有 remote 缓存，通常不需要代理）

## 4. 推送

国内推送 `git push` 到 github.com 会超时。**必须用 fgit 加速**：

```bash
# 优先用不带参数的 fgit push（用户实测更稳定）
D:/Tool/fgit/fgit.exe push

# 也可带参数
D:/Tool/fgit/fgit.exe push origin main
```

- **fgit 路径**：`D:\Tool\fgit\fgit.exe`（不在 PATH 中，需完整路径）
- **版本**：v1.2.0，基于 git 2.56.0.windows.2
- 克隆（拉取）仍用镜像代理，fgit 只用于推送
- fgit 无输出或超时时**不要假设失败**，先 `git ls-remote origin` 验证远程状态

## 5. 提交规范

- **提交信息**：用中英文均可，建议 `type(scope): subject` 格式（`feat:` / `fix:` / `docs:` / `chore:` / `refactor:`）
- **暂存**：只 `git add` 相关文件，**不要 `git add -A`**——工作区常有多个无关的未提交改动
- **作者**：`Scorpioflz <fanlinze@petalmail.com>`（git config 已配置）
- **禁止**：force push 到 main、跳过 hooks（`--no-verify`）、修改 git config
- **个人自用项目**：不设 Issue/PR，直接提交到 main

## 6. README 双语化

推送到 GitHub 的项目 README 必须：
- **英文** `README.md` + **中文** `README_ZH.md`，内容对照
- 顶部加语言切换互链：`English · [简体中文](README_ZH.md)` / `[English](README.md) · 简体中文`
- 含 mermaid 整体架构图（GitHub 自动渲染）
- 含各插件职责表（插件名 / 职责 / 状态 / 来源）
- 注明引用的插件及源地址

## 7. 常见操作速查

```bash
# --- index 仓库 ---
# 提交推送
cd D:\DSH-Dev
git add <files>
git commit -m "docs: ..."
D:/Tool/fgit/fgit.exe push origin main

# --- 桌宠仓库 ---
cd D:\DSH-Dev\dsh-pet-chubby_blue_whale
git add <files>
git commit -m "fix: ..."
git push origin main  # 桌宠仓库直连通常可以，不行就用 fgit

# --- 克隆插件参考源码 ---
cd D:\DSH-Dev\_plugin-references
git clone --depth 1 https://gh-proxy.com/https://github.com/<user>/<repo>.git

# --- 查看状态 ---
git status --short
git log -3 --format="%h %s"
git diff --stat
```

## 8. 并行开发冲突避免

多会话并行开发多个子项目时，子项目更新常涉及根项目文档/README 同步。冲突避免策略：

**文档分片（主要手段）**
- 各子项目详细描述放在 `docs/sub-projects/<name>.md`（分片文件）
- 子项目会话：改子项目仓库 + 改自己的分片文件 — **不碰 README 主体或其他分片**
- README 主体只放全局架构图 + 插件职责表概览 + 子项目表（含分片链接）
- 不同会话改不同分片文件 → 零冲突

**插件职责表（共享区）**
- 保留在 README（全局视角），每个会话只改自己子项目对应的行
- 不同行的修改 git 能自动合并

**push 前 rebase（兜底）**
```bash
git pull --rebase origin main && D:/Tool/fgit/fgit.exe push origin main
```
- 不同文件/不同行的修改 rebase 能自动合并
- 同行冲突需手动解决后再 push

**操作约定**
- 子项目会话完成后：先提交推送子项目仓库，再改根项目分片文件
- 根项目 README 主体更新（架构图、插件表全局变更）由当前会话直接做，push 前 rebase
- 如果频繁冲突：把待同步变更写到 `docs/.pending-root-updates.md`，由专门会话串行处理

## 9. 注意事项

- **工作区多仓库**：`D:\DSH-Dev` 本身是 index 仓库，`dsh-pet-chubby_blue_whale/` 是独立仓库（.gitignore 排除），操作时注意当前所在仓库
- **只读目录**：`deepseek-harness/`（可 `git pull` 但禁止修改）、`_plugin-references/`（禁止修改任何文件）
- **同步更新**：改动后同步更新所有相关文档（README、docs/、记忆文件），不能只改一处
- **桌宠 README 变更记录**：改桌宠文件后同步更新其 README 的"修改文件/删除文件"部分