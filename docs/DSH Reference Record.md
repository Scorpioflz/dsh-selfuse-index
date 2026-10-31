# DSH Reference Record

> 所有 DSH 插件、参考源码、灵感来源的完整记录。
> 源码浅克隆于 `D:\DSH-Dev\_plugin-references\`（只读参考）。
> 更新方式：进对应目录 `git pull`。新增参考：把 GitHub 地址追加到本文件末尾并告知 AI，AI 会克隆+分析+回填。
> 官方约定判定：`@deepseek-ai/dsh-*` scope + function plugin 四件套(name/inject/Config/apply 无 default) + schemastery Config + `dsh.bundle.patch` + peerDependencies 声明 `@deepseek-ai/*` + `engines.dsh`。

---

## 一、已安装的 DSH 插件（桌宠依赖或日常使用）

### 1. dsh-web-service — `dsh-web-service`（仓库 dsh-webapi）⭐ 桌宠依赖

| 项 | 内容 |
|---|---|
| GitHub | toddpan/dsh-webapi |
| 用途 | 把 DSH 能力开放为 80+ REST + SSE 路由与 OpenAI 兼容 `/chat/completions`，附独立固定端口 API 服务与 API Key 管理 |
| 形式 | service plugin（REST/SSE + 独立 HTTP 服务）+ function plugin（工具 + 设置页） |
| 暴露 | 工具 `dsh_web_service_info`；80+ 路由（默认前缀 `/api/v1`）：system/workspaces/sessions/streaming/OpenAI `chat/completions`/models/settings/api-keys/docs(Swagger UI)；独立固定端口服务(31800-31899)；SKILL.md |
| 配置 | schemastery Config：`pathPrefix:'/api/v1'`/`apiKey:''`/`standalonePort:0`(自动)/`standaloneBindIp:'127.0.0.1'`/`cors:true`/`maxUploadBytes:2GiB`/`adminRemoteAccess:false` |
| 依赖 | peer: `@deepseek-ai/cordis^4.0.4`/`@deepseek-ai/schemastery^3.18.2`/`@deepseek-ai/dsh-host-webserver`/`@deepseek-ai/dsh-tools`（复杂 `\|\|` 范围覆盖 0.1.0–0.2.x）；BSD-3-Clause |
| 安装 | `dsh plugin --profile web add https://github.com/toddpan/dsh-webapi/releases/latest/download/dsh-web-service.tgz`（推荐）；探活 `curl -s http://127.0.0.1:3080/api/v1/system/status` |
| 约束 | 兼容 DSH 0.1.0–0.2.x；独立服务端口固定；API Key 落盘 sha256+AES-256-GCM；管理接口默认仅回环；流式用停滞看门狗(300s)非总时长上限 |
| 官方约定 | **是（最规范）**：有 Config schema、TypeScript、SKILL、peer 范围、name 一致 |
| 关键文件 | `src/index.ts`、`src/router.ts`、`src/sessions.ts`、`src/streaming.ts`、`src/api-keys.ts`、`skills/dsh-web-service/SKILL.md`、`cordis.patch.yml` |

### 2. dsh-fish-memory — `dsh-fish-memory`（记忆插件参考）

| 项 | 内容 |
|---|---|
| GitHub | Yuuyuko-uu/dsh-fish-memory |
| 用途 | 给每个会话一份会淡忘的长期记忆，每条带时间戳，按鲜活度/重要度/情绪排序择优注入 |
| 形式 | function plugin（host `lib/index.js` 6309 行 + client `lib/client.js` 4043 行）；**`name='memory'` 与包名不一致** |
| 暴露 | 工具 `remember`；`systemPrompt.section`/`context`（每轮注入）；30+ HTTP 路由 |
| 与桌宠关系 | **@dsh-pet/memory 基于此改造**（按工作区共享记忆，14 天半衰期） |
| 关键文件 | `lib/index.js`、`lib/client.js`、`lib/hostdeps.mjs`、`cordis.patch.yml` |

### 3. dsh-balance-panel — `@wycto/dsh-balance-panel` ⭐ 桌宠依赖

| 项 | 内容 |
|---|---|
| GitHub | wycto/dsh-balance-panel |
| 用途 | 侧边栏底部展示已配置模型 Provider 的余额/配额 |
| 关键文件 | `src/host.js`、`src/client.js`、`cordis.patch.yml` |

### 4. dsh-bili-scroll — `dsh-bili-scroll`

| 项 | 内容 |
|---|---|
| GitHub | c1overzz/dsh-bili-scroll |
| 用途 | 每天自动刷 B 站：搜视频、读字幕判断值不值得、写日报 |
| 关键文件 | `index.js`、`client.js`、`cordis.patch.yml` |

### 5. dsh-computer-use — `dsh-codex-style-computer-use`

| 项 | 内容 |
|---|---|
| GitHub | ltmroberthk915/dsh-computer-use |
| 用途 | 让 DSH 能"看见并操控" Windows 桌面——截图/UIA 树查询与操作 |
| 关键文件 | `lib/index.js`、`lib/tools.js`、`skills/computer-use/SKILL.md` |

### 6. dsh-skills-manager — `@michengai/dsh-skills-manager`

| 项 | 内容 |
|---|---|
| GitHub | MichengAI/dsh-skills-manager |
| 用途 | 统一加载并安全管理本机与项目的 Agent Skills |
| 关键文件 | `src/index.ts`、`src/client.ts`、`cordis.patch.yml` |

### 7. dsh-chat-manager — `dsh-chat-manager`

| 项 | 内容 |
|---|---|
| GitHub | WSL043/dsh-chat-manager |
| 用途 | 在官方归档之上增加「归档内容搜索」与「已归档且未加载会话的确认式永久删除」 |
| 关键文件 | `src/index.js`、`lib/client.js`、`cordis.patch.yml` |

### 8. dsh-custom-reasoning — `dsh-custom-reasoning`

| 项 | 内容 |
|---|---|
| GitHub | 3likofj/dsh-custom-reasoning |
| 用途 | 为官方未声明推理强度的第三方模型自动补上标准五档推理等级 |
| 关键文件 | `lib/index.js`（19 行 no-op）、`lib/client.js`（675 行手写 bundle） |

### 9. dsh-preset-bridge — `dsh-preset-bridge`

| 项 | 内容 |
|---|---|
| GitHub | Lyrissonare/dsh-preset-bridge |
| 用途 | 把 DSH 桌面版 0.2.x 移除的 `~/.dsh/.agent-presets/` 目录扫描通道补回来 |
| 关键文件 | `lib/index.js`（163 行）、`cordis.patch.yml` |

### 10. modsearch — `@liustack/modsearch`

| 项 | 内容 |
|---|---|
| GitHub | liustack/modsearch |
| 用途 | 为无原生联网能力的模型外挂网页搜索/X 搜索/单页抓取 |
| 关键文件 | `dsh/index.js`、`dsh/client.js`、`cordis.patch.yml` |

### 11. cc-safety-net — `cc-safety-net`

| 项 | 内容 |
|---|---|
| GitHub | kenryu42/cc-safety-net |
| 用途 | 工具调用执行前拦截破坏性命令和密钥文件访问 |
| 关键文件 | `src/entries/deepseek-harness/index.ts`、`assets/cc-safety-net.schema.json` |

### 12. billion-context — `billion-context`

| 项 | 内容 |
|---|---|
| GitHub | ranxianglei/billion-context |
| 用途 | 上下文压缩代理——架在编程助手与模型 API 之间，压缩重写流 |
| 注意 | **勿作为 DSH 插件编写参考**（寄生式 fetch 劫持，非官方模式） |

### 13. dsh-univer-office — `dsh-univer-office`

| 项 | 内容 |
|---|---|
| GitHub | dream-num/dsh-univer-office |
| 用途 | 真正的办公环境——Univer 电子表格/文档/幻灯片汇聚同一运行时 |
| 官方约定 | **是（最规范）**，开发新插件优先参考 |

---

## 二、人设/Persona 参考插件（未安装，供参考）

### 14. dsh-persona-dafeiyu — `dsh-persona-dafeiyu` ⭐ 推荐安装

| 项 | 内容 |
|---|---|
| GitHub | huaizhuanghub/dsh-persona-dafeiyu |
| Stars | 90（活跃维护，2026-10-31 更新） |
| 用途 | **人设库插件**：内置大肥鱼/阿茶/听澜，支持导入自定义人设，按全局/工作区/会话三档生效，切换后即时生效无需重启 |
| 形式 | function plugin（host `lib/index.js` 1177 行 + client `lib/client.js` 设置页） |
| 暴露 | `ctx.systemPrompt.section()`（动态 text 函数，即时切换）；HTTP 路由 `/api/dsh-persona-dafeiyu/status`/`/mutate`/`/persona`；设置页 UI |
| 三档生效 | `global` → `workspace`（按 cwd）→ `session`，越细越优先 |
| 持久化 | `<DSH_HOME>/storages/dsh-persona-dafeiyu/personas.json` |
| 人设上限 | 64,000 字符 |
| 依赖 | peer(optional): `@deepseek-ai/cordis^4.0.1`/`@deepseek-ai/dsh-system-prompt^0.2.0-rc.2`/`@deepseek-ai/schemastery^3.18.4`；node>=20 |
| inject | `['systemPrompt']`（host）+ `['@deepseek-ai/dsh-client-ui-renderer','@deepseek-ai/dsh-client-locale']`（client） |
| 与桌宠关系 | **推荐替代当前 prompt_sync 人设注入方式**。安装后桌宠前端删掉 `dsh_provider.py:305-315` 的 prompt_sync，人设改由插件通过 `systemPrompt.section()` 注入（可被 prompt caching 缓存） |
| 关键文件 | `lib/index.js`（1177 行）、`lib/client.js`、`cordis.patch.yml`、`README.md` |

### 15. dsh-whale-musume-persona — `dsh-whale-musume-persona`

| 项 | 内容 |
|---|---|
| GitHub | Kaalia0912/dsh-whale-musume-persona |
| Stars | 52 |
| 用途 | DeepSeek Harness 全局鲸鱼娘（大肥鱼）人设插件 |
| 与桌宠关系 | 鲸鱼娘专用人设，可作为灵感参考 |

### 16. dsh-prompt-persona — `@xilin3/dsh-prompt-persona`

| 项 | 内容 |
|---|---|
| GitHub | Xilin3/dsh-prompt-persona |
| Stars | 16 |
| 用途 | 从设置页可视化编辑系统提示词（deployment:persona-prefix），支持实时预览与保存 |
| 形式 | function plugin（host `lib/index.js` + `lib/config.js` + `lib/web.js` + client `lib/client.js`） |
| 特点 | 简单直接，只编辑 deployment persona，无工作区分档 |
| 关键文件 | `lib/index.js`、`lib/config.js`、`lib/web.js`、`lib/client.js`、`cordis.patch.yml` |

### 17. dsh-soul — `dsh-soul`（仅分析，未安装）

| 项 | 内容 |
|---|---|
| GitHub | icyaaaww/dsh-soul |
| 用途 | 记忆骨架 + 图压缩 + 经验编译 |
| 评估结论 | **暂不整合**。经验编译对桌宠无价值；图压缩是全局副作用。借鉴方向：未来可在 dsh-pet-memory 内部加"约束节点" |

---

## 三、桌宠上游与源码参考

### 18. dsh-pet-indesktop（桌宠上游）

| 项 | 内容 |
|---|---|
| GitHub | MerZlin/dsh-pet-indesktop |
| 用途 | 桌宠前端上游（MIT License），当前仓库基于此个人自用再开发 |
| 路径 | `_plugin-references/dsh-pet-indesktop-upstream/` |
| 合并策略 | `git remote add upstream https://github.com/MerZlin/dsh-pet-indesktop.git && git fetch upstream && git merge upstream/main` |

### 19. DSH 原生 persona 包 — `@deepseek-ai/dsh-persona`

| 项 | 内容 |
|---|---|
| 路径 | `D:\DSH-Dev\deepseek-harness\packages\preset\persona\` |
| 用途 | DSH 原生 persona 插件，通过 `ctx.systemPrompt.section()` 注册 `deployment:persona-prefix`/`deployment:persona-suffix` |
| 限制 | **配置驱动，无终端用户运行时编辑 API**（README 明确声明） |
| 与 dsh-persona-dafeiyu 关系 | dafeiyu 插件通过注册同名 section shadow 原生 persona，并增加了运行时编辑/导入/三档切换 |

### 20. DSH systemPrompt 核心包 — `@deepseek-ai/dsh-system-prompt`

| 项 | 内容 |
|---|---|
| 路径 | `D:\DSH-Dev\deepseek-harness\packages\core\system-prompt\` |
| 用途 | SystemPrompt 注册表 + 装配流水线。每 step 调用 `assemble()` 合并全局+scope 层、排序、插值、渲染 |
| 关键 API | `section()`（有序 prompt section）、`context()`（动态运行时上下文）、`variable()`（模板变量）、`getSectionOrder()` |
| Section 顺序 | `DEPLOYMENT_PERSONA_PREFIX=0` → `TOOL_BASH=1000` → ... → `DEPLOYMENT_PERSONA_SUFFIX=10200` |
| 缓存友好 | 固定 section 可被 DeepSeek prompt caching 缓存；动态 context 只在内容变化时追加 |

---

## 四、横向速查

| 插件 | 形式 | 工具数 | Config schema | 官方约定 | 平台 |
|---|---|---|---|---|---|
| modsearch | function | 2 | 无（自管） | 部分 | 跨平台 |
| cc-safety-net | function(guard) | 0 | JSON Schema | 部分 | 跨平台 |
| dsh-bili-scroll | function | 20+ | schemastery ✓ | **是** | 跨平台 |
| dsh-chat-manager | function(slot) | 0 | 无 | 部分 | 跨平台 |
| dsh-fish-memory | function | 1 | 无（自管） | 部分 | 跨平台 |
| dsh-web-service | service+function | 1 | schemastery ✓ | **是** | 跨平台 |
| dsh-skills-manager | service+UI | 1 | ✓ | **是** | 跨平台 |
| dsh-balance-panel | service+UI | 0 | 无 | 部分 | 跨平台 |
| dsh-custom-reasoning | surface(no-op) | 0 | 无 | 部分 | 跨平台 |
| dsh-computer-use | function+MCP | 19 | ✓ | **是** | **win32** |
| billion-context | 寄生式 | 4 | 自管 | 部分 | 跨平台 |
| dsh-univer-office | function | 14 | schemastery ✓ | **是** | 跨平台 |
| dsh-preset-bridge | function | 0 | schemastery ✓ | 部分 | 跨平台 |
| dsh-soul | function | 2+ | ✓ | 部分 | 跨平台 |
| **dsh-persona-dafeiyu** | function+UI | 0 | 无（自管） | 部分 | 跨平台 |
| dsh-whale-musume-persona | function | 0 | — | — | 跨平台 |
| dsh-prompt-persona | function+UI | 0 | — | 部分 | 跨平台 |

**最规范的范本**（开发新插件优先参考）：`dsh-univer-office`、`dsh-web-service`、`dsh-skills-manager`、`dsh-bili-scroll`。
**勿作为 DSH 插件编写参考**：`billion-context`（寄生式 fetch 劫持，非官方模式）。