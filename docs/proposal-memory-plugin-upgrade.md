# 方案：@dsh-cbw/memory 记忆插件升级建议

> 状态：P0+P1+P2+P3 已实施（4.15 FTS5 暂缓）
> 日期：2026-10-31（初版），2026-10-31（修订：通用助手定位 + 4.7/4.8 调整 + task1 整合 + P3 实施）
> 分析对象：dsh-mnemon（最新源码）+ 社区记忆插件综合评估
> 目标：为 @dsh-cbw/memory 提出可操作的升级建议，做减法不做加法
> 历史背景：原 task1（桌宠记忆下沉）已整合至 §七

> **定位澄清（2026-10-31）**：桌宠正朝通用前端/助手角色发展，未来会触发 DSH 的各种工作
> （含工程类）。记忆插件不能只考虑闲聊场景，还需支持工程类工作的记忆需求——记忆分类、
> 不同半衰期策略、更高信息密度对话的沉淀。当前以闲聊为主，但设计需为工程场景预留扩展空间。

---

## 一、当前 @dsh-cbw/memory 现状

### 1.1 核心机制

| 维度 | 实现 |
|---|---|
| 存储 | 每会话独立 JSON 文件（`memory<sessionId>.json`） |
| 打分公式 | `P = C × (baseline + activation×A + importance×I + emotion×E)` |
| 鲜活度 | `A = A0 × 2^(-daysA / H)`，H = `baseHalfLifeDays` × (1 + 2×I) |
| 情绪衰减 | 独立半衰期 `emotionHalfLifeDays`（默认 7 天） |
| 稀有度饱和 | `C = s / (s + rarityK)`，控制命中词稀有度饱和点 |
| 注入 | `systemPrompt.context()` order=900，每条带时间戳 |
| 门槛 | `threshold=0.3`（卡 C），`maxItems=6`，`maxChars=800`，`dailyQuota=8` |
| 长期事实 | `factsMax=2`，每轮固定带，不占 maxItems |
| 问句门槛 | `queryGate=0.5`，过滤低信息量查询 |
| 工具 | 1 个（`remember`） |
| 版本 | v0.2（按会话分开） |

### 1.2 优势（不应丢弃）

1. **半衰期遗忘**：重要度调节半衰期（H = base × (1 + 2×I)），重要记忆忘得慢
2. **情绪衰减**：独立情绪半衰期，情绪记忆比事实记忆衰减快
3. **稀有度饱和**：rarityK 控制命中词稀有度，避免高频词主导
4. **问句信息量门槛**：queryGate 过滤"你好"这类低信息查询
5. **长期事实常驻层**：factsMax 每轮固定带，不看当前查询
6. **每日配额**：dailyQuota 限制每天记录条数，防过度记录
7. **时区自动适配**：TZ_OFFSET 自动认机器时区
8. **权重自动凑 100%**：fitWeights 函数
9. **会话独立**：每个 agent 挂自己的记忆文件

### 1.3 不足（升级方向）

1. **无按需召回**：每轮全量注入 maxItems=6 条，模型不能自己决定何时召回更多
2. **无容量管理**：记忆文件无限增长，无自动归档/压缩
3. **无安全模型**：模型可以凭空捏造 id 删除记忆
4. **无隐式拒绝检测**：用户说"不要记住"时仍可能自动记录
5. **单工具**：只有 `remember`，无 `recall`/`forget`/`link` 等
6. **无图遍历**：记忆之间无关联关系
7. **无空闲复盘**：记忆维护只发生在每轮注入时
8. **注入预算固定**：maxChars=800 不随上下文余量动态调整
9. **无记忆分类**：所有记忆混存，无法区分用户偏好/工程上下文/任务状态等不同类型
10. **无自动沉淀**：工程类对话信息密度高，但当前只靠模型主动调 remember 工具，有价值信息容易丢失

---

## 二、dsh-mnemon 可借鉴部分（重点分析）

### 2.1 Composable View 模式（⭐ 最值得借鉴）

**核心思想**：Strategy 决定"用什么"，Source 决定"怎么给"，Core 验证"给的对不对"。

```
请求 → Strategy.compose() → ViewSpec
     → Source.project(spec) → fragments + routes + actions
     → 模型看到 projection + route/action 描述
     → 模型按需调用 mnemon_view_route(routeId) → Evidence
```

**两种模式**：
- **eager**：直接注入文本（适合常驻记忆，如长期事实）
- **routed**：暴露 route 描述给模型，模型按需调用（适合按需召回）

**借鉴建议**：@dsh-cbw/memory 当前是纯 eager 模式（每轮注入 6 条）。可以增加 routed 模式：注入 2 条事实 + 暴露一个 `recall` route，让模型在需要时自己召回更多记忆。这不需要重构整个架构，只需在 `remember` 工具旁加一个 `recall` 工具。

### 2.2 双重预算控制（⭐ 实用）

```typescript
// 数量预算 + 字符预算，超限标记 truncated
if (items.length >= resultLimit) break
if (characters + text.length > characterLimit) { truncated = true; continue }
```

**借鉴建议**：@dsh-cbw/memory 的 maxChars=800 是硬截断。改为双重预算：maxItems=6 + maxChars=800，超限时标记 truncated 并在注入末尾加"还有 N 条记忆未显示，可用 recall 工具查看"。

### 2.3 显式/隐式记忆请求检测（⭐ 低成本高收益）

```typescript
EXPLICIT_MEMORY_CANDIDATE = [
  /(?:记住|记下来|保存到记忆|写入记忆|长期记录)/u,
  /\b(?:please\s+)?remember\b/iu,
]
NO_MEMORY_MAINTENANCE = [
  /(?:不要|不必|无需|请勿|禁止|别)(?:再|主动|自动|在后台|替我)?(?:记住|记忆)/u,
  /\b(?:do not|don't|never)\s+remember\b/iu,
]
```

**借鉴建议**：在注入前检测用户最近消息。如果匹配 NO_MEMORY_MAINTENANCE，跳过自动记录（仍允许显式 remember 工具调用）。如果匹配 EXPLICIT_MEMORY_CANDIDATE，提高该轮的记录优先级。实现成本极低（几行正则），但用户体验提升明显。

### 2.4 LRU 式缓存边界

```typescript
while (map.size > 128) map.delete(map.keys().next().value!)
```

**借鉴建议**：@dsh-cbw/memory 的记忆 JSON 文件无限增长。加一个 LRU 式容量管理：当记忆条数 > maxMemories（如 200）时，按 score 从低到高归档到 `archive-<sessionId>-<date>.json`，主文件只保留高分记忆。归档不删除，可手动恢复。

### 2.5 idle review 机制

```
对话结束 → 空闲 N 秒 → 回顾对话 → 提取值得记住的内容 → 调 remember
```

**触发条件**：用户文本 ≥ 320 字符 || 助手文本 ≥ 600 字符 || 非记忆工具调用

**借鉴建议**：@dsh-cbw/memory 当前只在用户显式调 `remember` 工具时记录。可以加一个 idle review：对话结束后空闲 30 秒，让模型回顾对话，自动提取值得记住的内容。但这需要注入权限和额外 token 消耗，建议作为可选配置项（默认关），不作为核心升级。

### 2.6 ReadGrant 安全模型

**思想**：写入必须证明证据来自当前 View 的 ReadGrant，防止模型捏造 id。

**借鉴建议**：@dsh-cbw/memory 的 `remember` 工具无安全模型，模型可以写入任意内容。加一个轻量安全检查：remember 工具的 `source` 参数必须是 "user_explicit" 或 "model_observed"，且 "model_observed" 的记忆在注入时标记来源。不需要完整的 ReadGrant 体系，只需区分"用户明确要求记住"和"模型自己觉得该记住"。

### 2.7 容量自动归档

**借鉴建议**：runtime memory 超限时先压缩（合并相似条目），再归档到单独文件。@dsh-cbw/memory 可以在记忆条数 > maxMemories 时：
1. 按 score 排序
2. 合并 content 相似度 > 0.8 的条目（简单 bigram 相似度）
3. 仍超限则将最低分的 N 条移到归档文件

### 2.8 不建议借鉴的部分

| 特性 | 原因 |
|---|---|
| 三层架构（runtime/documents/durable） | 过度工程化，@dsh-cbw/memory 的单层 + 长期事实已够用 |
| 9 个 Provider 插件化 | @dsh-cbw/memory 用 JSON 文件足够轻量，不需要 SQLite/远程服务 |
| Skill Evolution | 完全不同的职责（技能进化 vs 记忆管理） |
| 13 个工具 | @dsh-cbw/memory 只需 2-3 个（remember + recall + 可选 forget） |
| Composable View 完整架构 | 过重，只借鉴 eager/routed 思路即可 |
| 图遍历（mnemon_related + mnemon_link） | 记忆关联图对桌宠场景过重 |

---

## 三、社区记忆插件综合评估

### 3.1 评估矩阵

| 插件 | 存储 | 检索 | 特色 | 适合 @dsh-cbw/memory 借鉴 |
|---|---|---|---|---|
| **dsh-mnemon** | 三层分离 | Provider 可插拔 | Composable View, 13 工具 | ⭐⭐⭐ View 模式（✅ recall 已实施）、预算控制（✅ 已实施）、idle review（4.7 待实施） |
| **@restregular/dsh-memory** | JSONL | 本地向量检索 BGE-M3 | 5 工具 + 管理面板 | ⭐⭐ JSONL 存储（✅ 4.8 已实施）、管理面板（4.9 待实施） |
| **@furongjun1999/dsh-memory** (灵枢) | md 认知图 | 递归反思 | 知识飞轮、自我认知 | ⭐ 认知图思路（但过重） |
| **@tr1v3r/dsh-ltm** | — | CJK-aware 分词 + 混合重排 | 去重、过期审查 | ⭐⭐ CJK 分词（4.10 待实施）、去重（✅ 已实施） |
| **dsh-memory** | SQLite FTS5 | 全文检索 | 3 工具，无 embedding | ⭐⭐ FTS5 全文检索（4.12 重新评估中） |
| **dsh-memory-palace** | Markdown 文件 | 文件搜索 | 人类可读 Markdown | ⭐ 人类可读性（但 JSONL 已有 UI） |
| **dsh-memory-core** | 5 轨隔离 | — | memory/user/project/key/daily | ⭐ 多轨思路（✅ category 字段已替代） |
| **DWJZ/dsh-reflection** | $DSH_HOME/memory | 紧凑索引注入 | 持久化 + 新会话注入 | ⭐ 紧凑索引（类似当前 systemPrompt.context） |
| **jli517166-gif/love-suite** | — | — | 记忆星图、心情、人格 | ⭐ 心情/情绪维度（@dsh-cbw/memory 已有 emotion） |

### 3.2 关键发现

1. **JSONL 存储**（@restregular/dsh-memory）：JSONL 比 JSON 更适合记忆追加写入——每条记忆一行，追加不需要读全文件再写回。@dsh-cbw/memory 当前是 read-modify-write 整个 JSON，记忆条数多时 IO 开销大。

2. **CJK-aware 分词**（@tr1v3r/dsh-ltm）：@dsh-cbw/memory 的检索是线性扫描 + 词频统计，对中文分词不友好。@tr1v3r/dsh-ltm 用 CJK-aware tokenized search，对中文记忆的召回质量更高。但引入分词库会增加依赖，可以用简单的 bigram 分词代替。

3. **SQLite FTS5**（dsh-memory）：全文检索比线性扫描快得多。但 @dsh-cbw/memory 的记忆量级（单会话 < 200 条）用线性扫描完全够用，引入 SQLite 是过度工程化。

4. **去重 + 过期审查**（@tr1v3r/dsh-ltm）：@dsh-cbw/memory 无去重机制——模型可以反复记录相同内容。加一个 bigram 相似度去重（新记忆与最近 N 条比较，相似度 > 0.8 则合并而非新增）成本低收益高。

5. **管理面板**（@restregular/dsh-memory）：@dsh-cbw/memory 有设置页但无记忆管理面板（查看/编辑/删除单条记忆）。加一个简单的记忆列表页能大幅提升可操作性。

---

## 四、升级建议（按优先级排序）

### P0：低成本高收益 ✅ 已完成

#### 4.1 显式/隐式记忆请求检测 ✅
- **改动**：在注入前用正则检测用户最近消息
- **效果**：用户说"不要记住"时不再自动记录；用户说"记住这个"时提高记录优先级
- **成本**：~20 行正则 + 逻辑分支
- **来源**：dsh-mnemon `lifecycle.ts`

#### 4.2 记忆去重 ✅
- **改动**：新记忆写入前与最近 N 条做 bigram 相似度比较，> 0.8 则合并
- **效果**：避免模型反复记录相同内容
- **成本**：~30 行 bigram + 比较逻辑
- **来源**：@tr1v3r/dsh-ltm 去重思路

#### 4.3 双重预算 + truncated 标记 ✅
- **改动**：maxItems + maxChars 双重限制，超限标记 truncated 并提示"可用 recall 查看更多"
- **效果**：用户知道还有更多记忆，不是被硬截断了
- **成本**：~10 行
- **来源**：dsh-mnemon `composition.ts:normalizeEvidence`

### P1：中等成本 ✅ 已完成

#### 4.4 recall 工具（按需召回） ✅
- **改动**：在 `remember` 旁加一个 `recall` 工具，参数 `query` + `limit`，让模型在需要时主动召回更多记忆
- **效果**：从"每轮注入 6 条"变为"每轮注入 2 条事实 + 模型按需召回"，减少无关记忆注入
- **成本**：~50 行（工具定义 + 复用已有打分逻辑）
- **来源**：dsh-mnemon routed 模式

#### 4.5 容量管理 + 自动归档 ✅
- **改动**：记忆条数 > maxMemories（默认 200）时，按 score 排序，低分归档到 `archive-<sessionId>-<date>.jsonl`
- **效果**：主文件不无限增长，归档可恢复
- **成本**：~40 行
- **来源**：dsh-mnemon `runtime-capacity.ts`

#### 4.6 记忆来源标记 ✅
- **改动**：remember 工具加 `source` 参数（"user_explicit" / "model_observed"），注入时标记来源
- **效果**：区分"用户明确要求记住"和"模型自己觉得该记住"，前者优先级更高
- **成本**：~15 行
- **来源**：dsh-mnemon ReadGrant 思路（简化版）

### P2：较高成本（可选，按需做）

#### 4.7 增量定时沉淀（idle review 修订版）
- **改动**：定时检查（默认每 30 分钟）+ 增量处理 + 闲聊跳过
- **触发流程**：
  1. 定时触发（每 30 分钟，可配置 `idleReviewInterval`）
  2. 检查当前是否有活跃 SSE 流 → 有则跳过（不打断对话）
  3. 提取自上次沉淀后的增量对话内容
  4. 增量 < 500 字符 → 跳过（0 token）
  5. 闲聊检测（启发式，非 LLM）：无 tool_call + 无代码块 + 无文件路径 + < 1000 字符 → 跳过（0 token）
  6. 工程对话（有工具调用/代码块/文件路径）→ 增量摘要沉淀（只处理增量，非全量回顾）
- **沉淀 prompt**：`"以下是对话片段，提取值得长期记住的事实/偏好/工程上下文，没有则返回空数组"`（约 500-1000 token）
- **效果**：闲聊场景 0 token 消耗；工程场景每 30 分钟最多一次增量摘要
- **成本**：~100 行（定时器 + 增量提取 + 闲聊检测 + 摘要调用）
- **配置**：默认关，需手动开启；`idleReviewInterval=30`（分钟）、`idleReviewMinChars=500`、`idleReviewIdleChatThreshold=1000`
- **来源**：dsh-mnemon `skill-evolution.ts`（原版），修订为增量定时方案以节省 token
- **与原方案差异**：原方案"空闲 30 秒触发"在闲聊场景频繁浪费 token；修订版用定时 + 闲聊跳过，闲聊 0 token，工程场景按需沉淀

#### 4.8 JSONL 存储格式 + category 字段 ✅
- **改动**：从 JSON read-modify-write 改为 JSONL 追加写入；每条记忆加 `category` 字段
- **JSONL 效果**：追加写入不需要读全文件，IO 开销从 O(n) 降到 O(1)
- **category 字段**：
  - 默认 `"general"`，remember 工具加可选 `category` 参数
  - 预留分类：`"user_preference"`（用户偏好）、`"fact"`（长期事实）、`"project_context"`（工程上下文）、`"task_state"`（任务状态）、`"conversation"`（对话上下文）
  - 当前不实现分类逻辑，只打基础——将来需要按分类检索/差异化半衰期时不用再改存储格式
  - 与工程场景的关联：工程记忆（`project_context`/`task_state`）可用更长半衰期，闲聊记忆用默认半衰期
- **成本**：~80 行（存储层重写 + category 字段 + remember 工具参数）+ 数据迁移（当前记忆几乎为零，迁移成本忽略）
- **来源**：@restregular/dsh-memory（JSONL），通用助手定位需求（category）
- **注意**：当前记忆量级（< 200 条）JSON 性能足够，但开发阶段迁移成本接近零，现在改比将来有数据后改容易得多

#### 4.9 记忆管理面板 ✅
- **改动**：在设置页加一个记忆列表页，支持查看/编辑/删除单条记忆
- **效果**：用户可以直接管理记忆，不用手动编辑 JSONL
- **成本**：~100 行 UI + 后端 API
- **来源**：@restregular/dsh-memory 管理面板
- **注意**：实施时发现已有完整管理 UI（搜索/编辑/删除/批量操作/恢复/合并），无需新增

### P3：额外优化（用户提出，基于通用助手定位）

#### 4.10 CJK-aware bigram 分词 ✅
- **改动**：检索时对中文文本做 bigram 分词（相邻两字一组），替代当前的空格分词
- **效果**：中文记忆召回质量大幅提升（当前空格分词对中文几乎无效，整段中文被当作一个 token）
- **成本**：~20 行（bigram 函数 + 替换 tokenize 调用点）
- **来源**：@tr1v3r/dsh-ltm CJK-aware 分词
- **注意**：实施时发现已有 CJK-aware 分词（`分词()` 用词表切词 + `老分词()` bigram 兜底），无需新增

#### 4.11 remember 工具安全模型增强
- **改动**：`source` 参数从标记升级为验证——只接受 `"user_explicit"` / `"model_observed"` / `"idle_review"` 三个值，非法值拒绝写入
- **效果**：防止模型捏造来源；`idle_review` 来源的记忆在注入时降权（低于 user_explicit）
- **成本**：~10 行（参数校验 + 注入降权）
- **来源**：dsh-mnemon ReadGrant，4.6 来源标记的增强

#### 4.12 归档索引（Redis/SQL 模型）
- **改动**：记忆归档时，在主记忆文件留一条 `type: "archive_index"` 记录，指向归档文件路径 + 内容摘要
- **效果**：recall 查询命中 archive_index 时，自动从归档文件加载对应记忆——归档不再是死存储
- **架构模型**：主记忆 ≈ Redis（快速、常用、容量有限），归档 ≈ SQL（大量、可查、按需加载）
- **成本**：~40 行（归档时写 index + recall 时检查 index + 按需加载）
- **来源**：用户提出，借鉴 Redis/SQL 分层思路

#### 4.13 LRU 阈值上调
- **改动**：`maxMemories` 从 200 调到 500（配合归档索引，主记忆容量提升不影响查询效率）
- **效果**：更多记忆常驻主文件，减少归档/加载频率
- **成本**：配置项调整，~0 行代码
- **注意**：若 4.12 归档索引实施后查询效率不受影响，可考虑进一步调到 1000

#### 4.14 归档去重（防循环）
- **改动**：归档前检查归档文件中是否已有相似内容（bigram 相似度 > 0.8），有则跳过/合并
- **效果**：防止记忆被反复 记录→归档→再记录→再归档 的循环
- **成本**：~20 行（归档时对归档文件做去重检查）
- **来源**：用户提出，4.2 去重逻辑的归档层延伸

#### 4.15 SQLite FTS5 重新评估
- **原评估**：记忆量级 < 200 条，线性扫描足够，SQLite 过度工程化
- **重新评估**：通用助手定位下记忆量级可能 > 500 条（工程场景信息密度高），加上归档索引（4.12）后总可查记忆可能 > 2000 条
- **决策**：暂不实施。先实施 4.10 CJK bigram + 4.12 归档索引，若线性扫描 + bigram 在 1000+ 条时性能不足再引入 FTS5
- **理由**：FTS5 需要引入 SQLite 依赖 + 同步索引维护，当前 JSONL + bigram + 归档索引的方案更轻量

#### 4.16 路由前缀统一 ✅
- **改动**：所有 HTTP 路由前缀 `/dsh-pet-memory/` → `/dsh-cbw-memory/`，数据目录 `~/.dsh/dsh-pet-memory` → `~/.dsh/dsh-cbw-memory`，客户端前缀常量、plugin source 标识、桌宠 toggle URL 同步更新
- **效果**：插件从 `dsh-pet` 提取为独立 `@dsh-cbw/memory` 包后，路由前缀与包名一致
- **成本**：全局字符串替换（index.js 42 处 + client.js 1 处 + dsh_provider.py 1 处）
- **版本**：v0.4.1

#### 4.17 实机测试 + 插件市场安装 ✅
- **实机测试**：v0.4.1 通过 `dsh plugin add link:` 部署到 DSH web profile，全部通过（插件加载、32 路由、管理面板、记忆写入、跨对话召回、版本检查、策略配置）
- **repository 修复**：package.json 缺 `repository` 字段导致版本检查报"查不到"，已添加（commit `cd4d5b5`）
- **插件市场索引**：`docs/index.json` 已创建并托管在 GitHub Pages（`https://scorpioflz.github.io/dsh-cbw-memory/index.json`）
- **市场安装**：Discover 标签页直装遇 `ERR_PNPM_TARBALL_DECODE_GZIP`（GitHub tarball 下载损坏，国内网络不稳定）；改用 gh-proxy 镜像 tarball URL 通过 CLI 安装成功：`dsh plugin --profile web add "https://gh-proxy.com/https://github.com/Scorpioflz/dsh-cbw-memory/archive/refs/heads/main.tar.gz" --config.package-import-method=copy`，插件热加载后全部路由正常（list/page/policy 均 200）
- **版本**：v0.4.1（commit `4211c0b`）

---

## 五、不建议做的升级

| 升级 | 原因 |
|---|---|
| 三层记忆分离 | 过度工程化，单层 + 长期事实 + 归档索引（4.12）已够用 |
| SQLite/向量检索 | 暂不需要——先试 JSONL + bigram + 归档索引（见 4.15 重新评估） |
| 记忆关联图 | 桌宠/通用助手场景不需要记忆间的图遍历 |
| 9 个 Provider 插件化 | JSONL 文件足够轻量 |
| Composable View 完整架构 | 只借鉴 eager/routed 思路即可，不需要 Strategy/Source/Core 三层 |
| Skill Evolution | 完全不同的职责 |
| 13 个工具 | 2-3 个工具（remember + recall + 可选 forget）足够 |

---

## 六、实施路线图

```
Phase 1 (P0): 显式/隐式检测 + 去重 + 双重预算 ✅ 已完成
  ↓
Phase 2 (P1): recall 工具 + 容量管理 + 来源标记 ✅ 已完成
  ↓
Phase 3 (P2): 4.8 JSONL+category ✅ | 4.7 增量定时沉淀 ✅ | 4.9 管理面板 ✅（已有）
  ↓
Phase 4 (P3): 4.10 CJK bigram ✅（已有）| 4.11 安全模型增强 ✅ | 4.12 归档索引 ✅ | 4.13 LRU 上调 ✅ | 4.14 归档去重 ✅ | 4.15 FTS5 暂缓
  ↓
Phase 5 (维护): 4.16 路由前缀统一 ✅（v0.4.1）| 4.17 实机测试 + 插件市场索引 ✅（v0.4.1）
```

每个 Phase 独立可交付，不依赖下一个 Phase。P3 各项也相互独立，可按需挑选实施。

---

## 七、历史背景：桌宠记忆下沉到 DSH 插件层

> 原 task1 方案已整合至此。task1 完成"桌宠前端记忆下沉到 DSH 后端"，@dsh-cbw/memory 即下沉后的记忆插件。本方案是其延续。

### 7.1 架构变化

```
变更前：
  桌宠 Python ──(自带 memory.py 读写本地 JSON)──> 本地记忆文件
  桌宠 Python ──(拼接 prompt.py)──> DSH webapi ──> 模型

变更后：
  桌宠 Python ──(纯 UI + 会话管理)──> DSH webapi ──(@dsh-cbw/memory 插件)──> 模型
                                          └──(记忆读写)──> DSH 会话目录下 JSONL
```

### 7.2 桌宠移除的代码（2026-10-29）

| 文件 | 行数 | 处理 |
|------|------|------|
| `pet/chat/memory.py` | 1104 | 删除（四层记忆：user/fact/lesson/topic） |
| `pet/chat/memory_recall.py` | 531 | 删除（BM25 打分、艾宾浩斯衰减） |
| `pet/chat/memory_extract.py` | 306 | 删除（每 5 轮自动提炼） |
| `pet/chat/prompt.py` | 148→~30 | 重写：移除 memory_text/recall_text 拼接 |
| 对应测试 | — | 删除 3 个测试文件 |

净减约 2000 行。保留 `pet/proactive/memory.py`（主动识屏）和 `pet/memory_trim.py`（Windows 内存修剪），与聊天记忆无关。

### 7.3 非 DSH 后端移除（2026-10-31，commit cc881933）

桌宠只保留 DSH 作为唯一后端。移除：非 DSH provider 支持、桌宠侧人设拼接、联网搜索、非 DSH agent 联动。人设改由 DSH persona 插件（`dsh-persona-dafeiyu`）通过 `systemPrompt.section()` 注入。净删除 683 行。

### 7.4 关键设计决策

| 决策 | 落实 |
|------|------|
| fish-memory vs 自研 | 直接用 fish-memory 改造为 @dsh-cbw/memory |
| 多角色记忆隔离 | 每角色一个工作区，工作区内共享记忆 |
| system prompt 边界 | 人设由 DSH persona 插件注入，桌宠不再首发 |
| 工作区映射 | `storePath(sid)` 有 workspace 映射时用 `ws-<workspaceId>.jsonl`，否则回退 `<sessionId>.jsonl` |
| `baseHalfLifeDays` | 30→14（对齐桌宠原艾宾浩斯半衰期） |

### 7.5 待完成（来自 task1）

- 旧记忆数据迁移脚本（桌宠旧四层记忆 → @dsh-cbw/memory 格式）
- 配置权重校准（需实际对话数据）
- system prompt 引导段（建议追加 remember 工具引导）

---

## 八、核心原则

做减法不做加法。每个升级建议都先问"当前或未来的使用场景真的需要这个吗？"，不需要的即使技术上有趣也不做。但需考虑桌宠作为通用前端的演进方向——未来会触发工程类工作，记忆需求会比纯闲聊更复杂。