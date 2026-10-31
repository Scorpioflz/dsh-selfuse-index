# dsh-cbw-memory — 记忆插件开发

> 最后更新：2026-10-31 | 会话焦点：插件市场安装成功

## 正在进行

- v0.4.1 已通过 gh-proxy 镜像 tarball URL 安装到 DSH web profile，插件热加载正常
- 安装命令：`dsh plugin --profile web add "https://gh-proxy.com/https://github.com/Scorpioflz/dsh-cbw-memory/archive/refs/heads/main.tar.gz" --config.package-import-method=copy`
- 验证：list/page/policy 路由均返回 200，记忆数据正常捕获

## 遇到的困难

- Discover 标签页直装遇 `ERR_PNPM_TARBALL_DECODE_GZIP`（pnpm 从 GitHub 下载 tarball 时 gzip 数据损坏，国内网络不稳定）
- DSH 的 `accelerate.js` 有区域代理机制可代理 GitHub ref 解析，但 tarball 下载仍走 codeload.github.com 直连
- 旧版市场用镜像前缀 tarball URL 会导致 `ERR_PNPM_MISSING_TARBALL_INTEGRITY`（pnpm 无法识别为 GitHub 源），但 pnpm 12.11.2 已能处理

## 发现的经验

- DSH 插件市场去中心化：index.json 托管在 GitHub Pages，用户添加索引 URL 后可搜索安装
- `dshmarket` 的 `installTargetFor` 只接受 `https://github.com/owner/repo` 格式的 source URL
- `codeloadTarball(repo, sha, proxy)` 支持代理前缀，但仅用于区域加速内部
- pnpm 12.11.2 能正确处理 gh-proxy tarball URL 安装，无需 integrity hash
- 插件路由在端口 3080（web app）响应，非 31800（web service）

## 对其他会话的通知/请求

- 无