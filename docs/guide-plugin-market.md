# DSH 插件市场发布指南

> 本文档记录将 DSH 插件发布到插件市场的完整流程。**仅适用于 DSH 插件**（声明 `dsh.bundle` 的 npm 包），不适用于桌宠等独立应用。

## 前提条件

- 插件已有 GitHub 仓库（公开）
- `package.json` 中声明了 `dsh.bundle`（含 `patch` 字段指向 `cordis.patch.yml`）
- `package.json` **不设** `"private": true`
- `cordis.patch.yml` 的 `id`/`name` 与 `package.json` 的 `name` 一致
- `client.js` 的 `id` 与 `package.json` 的 `name` 一致

## 第一步：完善 package.json

确保 `package.json` 包含以下字段：

```jsonc
{
  "name": "@your-scope/your-plugin",   // 包名，与 cordis.patch.yml name 一致
  "version": "x.y.z",                   // 语义化版本
  "description": "...",                 // 简短描述
  "repository": {                       // ⚠ 必填！版本检查依赖此字段
    "type": "git",
    "url": "https://github.com/<owner>/<repo>.git"
  },
  "homepage": "https://github.com/<owner>/<repo>",
  "dsh": {
    "bundle": { "patch": "./cordis.patch.yml" }
  }
}
```

> **常见坑**：缺 `repository` 字段会导致管理面板"检查更新"报"查不到（包里没写 GitHub 仓库地址，没法查）"。

## 第二步：创建索引文件

在仓库中创建 `docs/index.json`（格式 1）：

```jsonc
{
  "format": 1,
  "title": { "en": "Your Index Title", "zh": "你的索引标题" },
  "plugins": [
    {
      "name": "@your-scope/your-plugin",       // 与 package.json name 一致
      "title": { "en": "Plugin Name", "zh": "插件名" },
      "description": {
        "en": "English description",
        "zh": "中文描述"
      },
      "author": "<GitHub 用户名>",
      "homepage": "https://github.com/<owner>/<repo>",
      "repository": "https://github.com/<owner>/<repo>",
      "keywords": ["keyword1", "keyword2"],
      "versions": [
        {
          "version": "x.y.z",                  // 与 package.json version 一致
          "publishTimestamp": <Unix 秒级时间戳>,
          "source": {
            "type": "git",
            "url": "https://github.com/<owner>/<repo>",
            "commit": "<完整 commit hash>"      // 用 git rev-parse HEAD 获取
          },
          "engines": { "dsh": ">=0.2.0" }       // DSH 版本兼容范围
        }
      ]
    }
  ]
}
```

同时在 `docs/` 下创建空文件 `.nojekyll`，防止 GitHub Pages 忽略特殊文件。

## 第三步：启用 GitHub Pages

1. 打开 `https://github.com/<owner>/<repo>/settings/pages`
2. **Source** → `Deploy from a branch`
3. **Branch** → `main`，文件夹 → `/docs`
4. **Save**

等待 1-2 分钟，索引将在 `https://<owner>.github.io/<repo>/index.json` 可访问。

> **验证**：`curl -s -o /dev/null -w "%{http_code}" "https://<owner>.github.io/<repo>/index.json"` 应返回 `200`。

## 第四步：给仓库打上 `dsh-plugin` topic

在 GitHub 仓库上添加 `dsh-plugin` topic（`https://github.com/topics/dsh-plugin`），让插件可被按 topic 检索发现。

**方式 A（网页）**：仓库主页右上角齿轮 → Topics → 输入 `dsh-plugin` → Save。

**方式 B（API）**：
```bash
TOKEN=$(printf "protocol=https\nhost=github.com\n" | git credential fill 2>&1 | grep "^password=" | cut -d= -f2)
curl -s -X PUT "https://api.github.com/repos/<owner>/<repo>/topics" \
  -H "Authorization: token $TOKEN" \
  -H "Accept: application/vnd.github.mercy-preview+json" \
  -d '{"names":["dsh-plugin"]}'
```

## 第五步：在 DSH 中添加索引源

1. 打开 DSH → **Plugins** 页面
2. 找到 **Custom plugin indexes**（在 Experimental plugins 下，需先开启实验性功能）
3. 点 **Add index source**
4. 输入索引 URL：`https://<owner>.github.io/<repo>/index.json`
5. 确认后切换到 **Discover** 标签页，应能看到插件

## 第六步：通过市场安装

在 Discover 标签页找到插件后，点击安装。DSH 会通过 `pluginManager.installBundle` 安装，保留审批/兼容性检查。

## 发布新版本时的更新流程

1. 更新代码，bump `package.json` version
2. 提交并推送到 GitHub
3. 获取新 commit hash：`git rev-parse HEAD`
4. 更新 `docs/index.json`：在 `versions` 数组中**追加**新版本条目（保留旧版本）
5. 提交并推送 `docs/index.json`
6. GitHub Pages 自动更新，用户在 DSH 中会看到 `update-available`

## 索引格式要点

- **format**: 必须为 `1`
- **source.type**: `"git"`（GitHub 仓库）或 `"npm"`（npm 包）
- **publishTimestamp**: Unix 秒级时间戳（非毫秒）
- **engines.dsh**: DSH 版本兼容范围，缺失时由 `@deepseek-ai/dsh*` peerDependencies 推断
- **多语言**: `title`/`description` 支持对象形式 `{ "en": "...", "zh": "..." }`
- **keywords**: 用于搜索匹配
- **索引未签名**: title/author/label 都是声明值，DSH 只校验格式不校验真实性；安装时重新检查源 manifest

## 常见问题

| 问题 | 原因 | 解决 |
|---|---|---|
| 管理面板"查不到"更新 | package.json 缺 `repository` 字段 | 添加 `repository` + `homepage` |
| GitHub Pages 404 | 未启用 Pages 或分支/文件夹选错 | Settings → Pages → Branch: main, /docs |
| 插件不出现在 Discover | 索引 URL 错误或格式不合规 | 用 `curl` 验证返回 200 + 合法 JSON |
| 路由 404 | 插件路由在 web app 端口（3080）非 web service（31800） | 测试用 `curl http://127.0.0.1:3080/<plugin-id>/...` |
| `dsh plugin add` 后插件不加载 | 手动创建符号链接不被 pnpm/cordis 识别 | 用 `dsh plugin --profile <p> add "link:<path>"` 正式安装 |

## 参考

- DSH 插件市场是**去中心化**的，没有官方注册表
- 索引可托管在任意静态主机（GitHub Pages、对象存储 + https 等）
- 用户可添加多个索引源，DSH 会合并展示
- 详细机制见 `deepseek-harness/docs/user/guide/plugin-market.md`