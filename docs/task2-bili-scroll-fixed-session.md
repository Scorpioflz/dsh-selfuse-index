# 任务2：dsh-bili-scroll 固定会话方案

> 状态：分析完成，待讨论
> 目标：让 dsh-bili-scroll 在固定对话中运行，有上下文，更好留存记忆，不让对话工作区混乱。

---

## 一、当前会话机制根因

### 1.1 调用方式

值班轮通过 `child_process.spawn` 起新 dsh CLI 进程（`index.js:1600-1632`）：

```js
spawn('dsh', ['-p', 'bili-duty', '--print', prompt], { cwd: pluginHome })
```

- **纯 CLI 一次性模式**：prompt 作为命令行参数传入，进程结束即会话结束
- **非 API 复用会话**：不调用 webapi，无 sessionId 复用
- **每轮独立会话**：无上下文延续

### 1.2 权限隔离

用 `bili-duty` 最小权限 profile（`cordis.patch.yml`）：
- 关掉 fs/shell/web/subagent/skill 等几乎所有工具
- 只留 B站 MCP + 5 个窄口 IO 工具
- cwd 钉在插件家 `$DSH_HOME/bili-duty/`

### 1.3 跨轮记忆（当前替代方案）

靠三个文件在插件家目录下：
- `seen.md` — 判重表（已处理视频 ID）
- `digest/` — 月归档（`YYYY-MM.md`）
- `out/` — 日报（`YYYY-MM-DD.md`）

**问题**：文件记忆无法提供对话上下文，模型每轮"失忆"，只能靠 prompt 重新注入摘要。

---

## 二、DSH webapi 能力

### 2.1 会话创建

`POST /sessions` 支持：
- 自带 `sessionId` — 可指定固定 ID
- 指定 `workspaceId` — 归组到工作区
- 指定 `cwd` — 钉工作目录
- 指定 `title` — 会话标题
- 指定 `systemPrompt` — 首发系统提示词

### 2.2 会话续写

`POST /sessions/:id/prompt-stream` 支持：
- 向**已有会话**发 SSE 流式消息
- 保留完整对话上下文
- 模型可调用 `remember` 等工具写入记忆

### 2.3 工作区查询

`GET /workspaces/:id/sessions` — 列工作区下所有会话

**结论**：DSH webapi 技术上完全支撑固定会话方案。

---

## 三、四个候选方案

### 方案 A：固定会话复用 sessionId

```
首次：POST /sessions { sessionId: "bili-duty-fixed", workspaceId: "bili-duty-ws", ... }
后续：POST /sessions/bili-duty-fixed/prompt-stream { prompt }
```

| 项 | 评估 |
|----|------|
| 上下文 | ✅ 最直接，完整对话历史 |
| 记忆 | ✅ 模型可调用 remember，记忆插件持久化 |
| 改动量 | 中：spawn CLI → 调 webapi HTTP |
| 风险 | ⚠️ 会话无限增长，需 compaction 兜底 |
| 适合 | 长期值班、需强上下文 |

### 方案 B：固定工作区 + 每天新会话 + 显式注入记忆

```
每天：POST /sessions { workspaceId: "bili-duty-ws", title: "值班-YYYY-MM-DD", systemPrompt: <含昨日摘要> }
```

| 项 | 评估 |
|----|------|
| 上下文 | ⚠️ 仅当日有上下文，跨日靠注入 |
| 记忆 | ⚠️ 需每轮从记忆文件读取并注入 prompt |
| 改动量 | 中：spawn CLI → 调 webapi HTTP + 注入逻辑 |
| 风险 | 低：会话不膨胀 |
| 适合 | 日报式值班、跨日上下文需求弱 |

### 方案 C：固定会话 + 超阈值归档换新会话

```
固定会话运行；当消息数 > N 或 token > M：
  1. 让模型生成当前会话摘要
  2. 归档旧会话
  3. 新建会话，systemPrompt 注入摘要
```

| 项 | 评估 |
|----|------|
| 上下文 | ✅ 强，且有归档兜底 |
| 记忆 | ✅ remember 持久化 + 摘要注入 |
| 改动量 | 高：webapi + 归档逻辑 + 阈值监控 + 摘要生成 |
| 风险 | 中：归档时机和摘要质量需调优 |
| 适合 | 长期运行、需兼顾上下文与性能 |

### 方案 D：CLI 不变仅加 workspace 归组

```
spawn 时加 --workspace bili-duty-ws（如 CLI 支持）
```

| 项 | 评估 |
|----|------|
| 上下文 | ❌ 仍无上下文 |
| 记忆 | ❌ 仍靠文件 |
| 改动量 | 极小 |
| 风险 | 极低 |
| 适合 | 仅想归组，不解决核心问题 |

---

## 四、推荐倾向

**推荐方案 A（固定会话复用 sessionId）**，理由：

1. 改动量适中（spawn → HTTP 调用），收益最大
2. 完整对话上下文最符合"有上下文、更好留存记忆"的目标
3. fish-memory 等记忆插件在固定会话下自然生效
4. compaction 兜底：DSH 有会话 compaction 机制（需验证 bili-duty profile 下是否自动生效）

**若验证发现 compaction 在 bili-duty profile 下不生效**，则退到方案 C。

---

## 五、待验证未知项

1. **bili-duty profile 下 compaction 是否自动生效**
   - bili-duty 关掉了多数工具，compaction 若依赖某工具可能被禁
   - 验证方法：查 DSH compaction 触发条件与依赖工具

2. **会话级 permission 与 profile disabled 的叠加语义**
   - 固定会话的权限是会话级还是 profile 级？
   - 若会话级可覆盖 profile，需确认固定会话不泄露权限
   - 验证方法：查 DSH 权限叠加逻辑

---

## 六、风险与注意事项

| 风险 | 影响 | 缓解 |
|------|------|------|
| 固定会话无限增长导致 token 爆炸 | 高 | compaction 兜底 / 方案 C 归档 |
| bili-duty profile 下 compaction 不生效 | 高 | 验证后选方案 C |
| webapi 不可用时值班中断 | 中 | 保留 CLI fallback；webapi 重试 |
| 固定 sessionId 被意外清除 | 低 | 会话不存在时自动重建 |
| 多值班轮并发写同一会话 | 中 | 加锁或每轮串行 |
| 权限泄露（固定会话权限叠加） | 高 | 验证叠加语义；保持 profile 级禁用 |

---

## 七、待讨论决策点

1. **方案选择**：A / B / C / D？倾向 A，但需先验证两个未知项
2. **固定 sessionId 命名**：`bili-duty-fixed`？还是带日期/版本？
3. **workspaceId 命名与是否新建**：复用现有 workspace 还是新建 `bili-duty-ws`？
4. **compaction 不生效时的降级策略**：自动转方案 C，还是告警人工介入？
5. **并发控制**：多值班轮是否允许并发写同一会话？还是强制串行？
6. **webapi 地址与认证**：bili-scroll 插件如何获知 webapi 的 host:port？是否需要新增配置项？
7. **CLI fallback 保留与否**：webapi 不可用时是否退回原 CLI 模式？