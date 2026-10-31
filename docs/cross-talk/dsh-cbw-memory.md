# dsh-cbw-memory — 记忆插件开发

> 最后更新：2026-10-31 | 会话焦点：上游缺陷排查修复（v0.5.1）

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

- DSH 插件市场去中心化：index.json 托管在 GitHub Pages
- `dshmarket` 的 `installTargetFor` 只接受 `https://github.com/owner/repo` 格式
- pnpm 12.11.2 能正确处理 gh-proxy tarball URL 安装
- 插件路由在端口 3080（web app）响应

## 对其他会话的通知/请求

- 无