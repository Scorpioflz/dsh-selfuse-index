# dsh-cbw-memory — 记忆插件开发

> 最后更新：2026-11-01 | 会话焦点：无进行中任务

## 正在进行

- 无进行中任务

## 已完成

- v0.5.1 修复来源头吞正文缺陷（上游 dsh-fish-memory 1.4.7 同款）：`清掉注入上下文()` 仅 `【你记得的事】` 整块跳，外部来源头只跳那一行
- v0.5.0 分类半衰期差异化：`project_context` ×3、`fact`/`user_preference`/`task_state` ×2、其余 ×1
- v0.5.0/v0.5.1 均已安装到 DSH web profile 并验证路由正常
- 上游三缺陷排查完成：缺陷1（来源头吞正文）存在并已修复；缺陷2（/mode GET/POST）不存在；缺陷3（提示词缺「写我」规则）不存在
- `docs/plugin_updates.md` 已标 ✅

## 遇到的困难

- Discover 标签页直装遇 `ERR_PNPM_TARBALL_DECODE_GZIP`，改用 gh-proxy tarball URL CLI 安装

## 发现的经验

### DSH 插件安装与部署

- **pnpm + NTFS os error 448**：所有 pnpm install 调用加 `--config.package-import-method=copy`，避免 NTFS 挂载点 reparse point 冲突
- **tarball 下载损坏 ERR_PNPM_TARBALL_DECODE_GZIP**：国内网络不稳致 pnpm 从 GitHub 拉 tarball gzip 数据损坏。解法：先 `pnpm store prune` 清缓存，反复失败改用 `https://gh-proxy.com/https://github.com/<owner>/<repo>/archive/refs/heads/main.tar.gz` 镜像 tarball URL
- **gh-proxy tarball URL 比 `github:` specifier 更可靠**：后者走 git ls-remote 直连 GitHub 必失败（国内网络），前者经镜像代理稳定可达
- **pnpm 12.11.2+ 能正确处理 gh-proxy tarball URL**：无需 integrity hash，直接 `dsh plugin --profile <p> add "<url>" --config.package-import-method=copy` 即可
- **插件热加载**：通过 CLI 安装后无需重启 DSH，插件自动热加载，路由立即生效

### DSH 插件市场发布

- **去中心化架构**：index.json 托管在 GitHub Pages，用户添加索引 URL 后可搜索安装
- **`dshmarket` 的 `installTargetFor` 只接受 `https://github.com/owner/repo` 格式**：不支持 tarball URL（但 CLI add 支持）
- **`accelerate.js` 区域代理**：有区域代理机制可代理 GitHub ref 解析，但 tarball 下载仍走 codeload.github.com 直连
- **完整发布流程**：① package.json 加 `repository` 字段 → ② `docs/index.json` 索引文件 → ③ GitHub Pages 启用 → ④ GitHub API 打 `dsh-plugin` topic（PUT /repos/.../topics）→ ⑤ 从 GitHub 安装验证
- **`git credential fill` 可获取 GitHub token**：做 API 操作（启用 Pages、打 topic），需 printf 管道方式避免超时

### DSH 插件架构要点

- **插件 HTTP 路由在端口 3080（web app）响应**，非 31800（web service）。测试插件路由用 `curl http://localhost:3080/<route>`
- **热重启不重载 bundle 层**：改插件后热重启不生效，必须完全重启 DSH（关进程再重开）才能让 bundle 层（cordis.patch.yml 等）重新加载
- **defineTool 工具必须含 name 字段**：缺失会导致 ToolSchema.name = undefined，DSH 的 snapshotJsonValue 比 JSON.stringify 更严格（拒绝含 undefined 字段的对象），session.append('request/header') 抛 "non-JSON-serializable" 错误。宿主 tools.register 不验证 name 是字符串，是防御缺口
- **YAML 中 scoped 包名必须加引号**：`@` 是 YAML 保留字符，`name: '@dsh-cbw/memory'` 而非 `name: @dsh-cbw/memory`，否则 DSH 静默跳过整个插件（仅日志 `skipping profile bundle` 警告，不报错）
- **client.js id 与 package.json name 必须完全一致**：`window.__ModuleLoader__.load({ id: ... })` 的 id 必须与 package.json 的 name 完全一致（如 `@dsh-cbw/memory`，非 `dsh-cbw-memory`），否则 DSH 报 `loaded without registering "<name>"`，插件不激活
- **三处名称关系**：cordis.patch.yml `id` == index.js `export const name`；cordis.patch.yml `name` == package.json `name`；client.js `id` == package.json `name`

### DSH 开发流程经验

- **DSH 启动由用户负责，AI 负责测试**：需 DSH 运行做验证时让用户手动启动，AI 用 browser/curl 工具测试，别自己 subprocess 启动（AI 启动反复崩溃）
- **上游派生作品需跟踪上游缺陷修复**：作为 fish-memory 派生作品，上游 dsh-fish-memory 修了缺陷需同步排查 @dsh-cbw/memory 是否有相同代码路径，存在则修复发版
- **Windows 上验证 JS 语法**：`node --check` 超时，直接用 esbuild
- **index 仓库 git status 超时**：D:\DSH-Dev 根仓库 git status 因大量未跟踪文件超时，提交时直接 git add 指定文件 + commit 跳过 status
- **git 推送逐条执行更快**：每个 git 指令逐条执行，不要 chained &&，大仓库更快
- **fgit 可用于所有 git 子命令**：`D:\Tool\fgit\fgit.exe` 不只 push，add/commit/status 等都可用，大仓库更快；fgit 超时不一定是失败，可能已推送完成

## 对其他会话的通知/请求

- → @dsh-pet：project_context/task_state 半衰期差异化 已完成（v0.5.0，project_context ×3、fact/user_preference/task_state ×2、其余 ×1）
- → @root：fish-memory 1.4.7 三缺陷排查任务 已完成（v0.5.1，缺陷1已修，缺陷2/3不存在，plugin_updates.md 已标 ✅）
- → @all：上方「发现的经验」段已系统整理 DSH 插件开发经验（安装部署/市场发布/架构要点/开发流程），供各会话参考