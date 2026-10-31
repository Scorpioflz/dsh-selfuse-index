# 方案一：@dsh-pet/memory 记忆插件升级建议

> 状态：分析完成，待讨论
> 日期：2026-10-31
> 分析对象：dsh-mnemon（最新源码）+ 社区记忆插件综合评估
> 目标：为 @dsh-pet/memory 提出可操作的升级建议，做减法不做加法

---

## 一、当前 @dsh-pet/memory 现状

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

**借鉴建议**：@dsh-pet/memory 当前是纯 eager 模式（每轮注入 6 条）。可以增加 routed 模式：注入 2 条事实 + 暴露一个 `recall` route，让模型在需要时自己召回更多记忆。这不需要重构整个架构，只需在 `remember` 工具旁加一个 `recall` 工具。

### 2.2 双重预算控制（⭐ 实用）

```typescript
// 数量预算 + 字符预算，超限标记 truncated
if (items.length >= resultLimit) break
if (characters + text.length > characterLimit) { truncated = true; continue }
```

**借鉴建议**：@dsh-pet/memory 的 maxChars=800 是硬截断。改为双重预算：maxItems=6 + maxChars=800，超限时标记 truncated 并在注入末尾加"还有 N 条记忆未显示，可用 recall 工具查看"。

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

**借鉴建议**：@dsh-pet/memory 的记忆 JSON 文件无限增长。加一个 LRU 式容量管理：当记忆条数 > maxMemories（如 200）时，按 score 从低到高归档到 `archive-<sessionId>-<date>.json`，主文件只保留高分记忆。归档不删除，可手动恢复。

### 2.5 idle review 机制

```
对话结束 → 空闲 N 秒 → 回顾对话 → 提取值得记住的内容 → 调 remember
```

**触发条件**：用户文本 ≥ 320 字符 || 助手文本 ≥ 600 字符 || 非记忆工具调用

**借鉴建议**：@dsh-pet/memory 当前只在用户显式调 `remember` 工具时记录。可以加一个 idle review：对话结束后空闲 30 秒，让模型回顾对话，自动提取值得记住的内容。但这需要注入权限和额外 token 消耗，建议作为可选配置项（默认关），不作为核心升级。

### 2.6 ReadGrant 安全模型

**思想**：写入必须证明证据来自当前 View 的 ReadGrant，防止模型捏造 id。

**借鉴建议**：@dsh-pet/memory 的 `remember` 工具无安全模型，模型可以写入任意内容。加一个轻量安全检查：remember 工具的 `source` 参数必须是 "user_explicit" 或 "model_observed"，且 "model_observed" 的记忆在注入时标记来源。不需要完整的 ReadGrant 体系，只需区分"用户明确要求记住"和"模型自己觉得该记住"。

### 2.7 容量自动归档

**借鉴建议**：runtime memory 超限时先压缩（合并相似条目），再归档到单独文件。@dsh-pet/memory 可以在记忆条数 > maxMemories 时：
1. 按 score 排序
2. 合并 content 相似度 > 0.8 的条目（简单 bigram 相似度）
3. 仍超限则将最低分的 N 条移到归档文件

### 2.8 不建议借鉴的部分

| 特性 | 原因 |
|---|---|
| 三层架构（runtime/documents/durable） | 过度工程化，@dsh-pet/memory 的单层 + 长期事实已够用 |
| 9 个 Provider 插件化 | @dsh-pet/memory 用 JSON 文件足够轻量，不需要 SQLite/远程服务 |
| Skill Evolution | 完全不同的职责（技能进化 vs 记忆管理） |
| 13 个工具 | @dsh-pet/memory 只需 2-3 个（remember + recall + 可选 forget） |
| Composable View 完整架构 | 过重，只借鉴 eager/routed 思路即可 |
| 图遍历（mnemon_related + mnemon_link） | 记忆关联图对桌宠场景过重 |

---

## 三、社区记忆插件综合评估

### 3.1 评估矩阵

| 插件 | 存储 | 检索 | 特色 | 适合 @dsh-pet/memory 借鉴 |
|---|---|---|---|---|
| **dsh-mnemon** | 三层分离 | Provider 可插拔 | Composable View, 13 工具 | ⭐⭐⭐ View 模式、预算控制、idle review |
| **@restregular/dsh-memory** | JSONL | 本地向量检索 BGE-M3 | 5 工具 + 管理面板 | ⭐⭐ JSONL 存储（比 JSON 更适合追加）、管理面板 |
| **@furongjun1999/dsh-memory** (灵枢) | md 认知图 | 递归反思 | 知识飞轮、自我认知 | ⭐ 认知图思路（但过重） |
| **@tr1v3r/dsh-ltm** | — | CJK-aware 分词 + 混合重排 | 去重、过期审查 | ⭐⭐ CJK 分词（对中文记忆更友好）、去重 |
| **dsh-memory** | SQLite FTS5 | 全文检索 | 3 工具，无 embedding | ⭐⭐ FTS5 全文检索（比当前线性扫描快） |
| **dsh-memory-palace** | Markdown 文件 | 文件搜索 | 人类可读 Markdown | ⭐ 人类可读性（但 JSON 已有 UI） |
| **dsh-memory-core** | 5 轨隔离 | — | memory/user/project/key/daily | ⭐ 多轨思路（但会话隔离已够） |
| **DWJZ/dsh-reflection** | $DSH_HOME/memory | 紧凑索引注入 | 持久化 + 新会话注入 | ⭐ 紧凑索引（类似当前 systemPrompt.context） |
| **jli517166-gif/love-suite** | — | — | 记忆星图、心情、人格 | ⭐ 心情/情绪维度（@dsh-pet/memory 已有 emotion） |

### 3.2 关键发现

1. **JSONL 存储**（@restregular/dsh-memory）：JSONL 比 JSON 更适合记忆追加写入——每条记忆一行，追加不需要读全文件再写回。@dsh-pet/memory 当前是 read-modify-write 整个 JSON，记忆条数多时 IO 开销大。

2. **CJK-aware 分词**（@tr1v3r/dsh-ltm）：@dsh-pet/memory 的检索是线性扫描 + 词频统计，对中文分词不友好。@tr1v3r/dsh-ltm 用 CJK-aware tokenized search，对中文记忆的召回质量更高。但引入分词库会增加依赖，可以用简单的 bigram 分词代替。

3. **SQLite FTS5**（dsh-memory）：全文检索比线性扫描快得多。但 @dsh-pet/memory 的记忆量级（单会话 < 200 条）用线性扫描完全够用，引入 SQLite 是过度工程化。

4. **去重 + 过期审查**（@tr1v3r/dsh-ltm）：@dsh-pet/memory 无去重机制——模型可以反复记录相同内容。加一个 bigram 相似度去重（新记忆与最近 N 条比较，相似度 > 0.8 则合并而非新增）成本低收益高。

5. **管理面板**（@restregular/dsh-memory）：@dsh-pet/memory 有设置页但无记忆管理面板（查看/编辑/删除单条记忆）。加一个简单的记忆列表页能大幅提升可操作性。

---

## 四、升级建议（按优先级排序）

### P0：低成本高收益（建议立即做）

#### 4.1 显式/隐式记忆请求检测
- **改动**：在注入前用正则检测用户最近消息
- **效果**：用户说"不要记住"时不再自动记录；用户说"记住这个"时提高记录优先级
- **成本**：~20 行正则 + 逻辑分支
- **来源**：dsh-mnemon `lifecycle.ts`

#### 4.2 记忆去重
- **改动**：新记忆写入前与最近 N 条做 bigram 相似度比较，> 0.8 则合并
- **效果**：避免模型反复记录相同内容
- **成本**：~30 行 bigram + 比较逻辑
- **来源**：@tr1v3r/dsh-ltm 去重思路

#### 4.3 双重预算 + truncated 标记
- **改动**：maxItems + maxChars 双重限制，超限标记 truncated 并提示"可用 recall 查看更多"
- **效果**：用户知道还有更多记忆，不是被硬截断了
- **成本**：~10 行
- **来源**：dsh-mnemon `composition.ts:normalizeEvidence`

### P1：中等成本（建议近期做）

#### 4.4 recall 工具（按需召回）
- **改动**：在 `remember` 旁加一个 `recall` 工具，参数 `query` + `limit`，让模型在需要时主动召回更多记忆
- **效果**：从"每轮注入 6 条"变为"每轮注入 2 条事实 + 模型按需召回"，减少无关记忆注入
- **成本**：~50 行（工具定义 + 复用已有打分逻辑）
- **来源**：dsh-mnemon routed 模式

#### 4.5 容量管理 + 自动归档
- **改动**：记忆条数 > maxMemories（默认 200）时，按 score 排序，低分归档到 `archive-<sessionId>-<date>.json`
- **效果**：主文件不无限增长，归档可恢复
- **成本**：~40 行
- **来源**：dsh-mnemon `runtime-capacity.ts`

#### 4.6 记忆来源标记
- **改动**：remember 工具加 `source` 参数（"user_explicit" / "model_observed"），注入时标记来源
- **效果**：区分"用户明确要求记住"和"模型自己觉得该记住"，前者优先级更高
- **成本**：~15 行
- **来源**：dsh-mnemon ReadGrant 思路（简化版）

### P2：较高成本（可选，按需做）

#### 4.7 idle review（空闲复盘）
- **改动**：对话结束空闲 30 秒后，让模型回顾对话提取记忆
- **效果**：不依赖用户显式 remember，自动沉淀对话中的有价值信息
- **成本**：~80 行 + 额外 token 消耗
- **配置**：默认关，需手动开启
- **来源**：dsh-mnemon `skill-evolution.ts`

#### 4.8 JSONL 存储格式
- **改动**：从 JSON read-modify-write 改为 JSONL 追加写入
- **效果**：追加写入不需要读全文件，IO 开销从 O(n) 降到 O(1)
- **成本**：~60 行（存储层重写）+ 数据迁移
- **来源**：@restregular/dsh-memory
- **注意**：当前记忆量级（< 200 条）JSON 性能足够，仅在记忆量显著增长时才值得做

#### 4.9 记忆管理面板
- **改动**：在设置页加一个记忆列表页，支持查看/编辑/删除单条记忆
- **效果**：用户可以直接管理记忆，不用手动编辑 JSON
- **成本**：~100 行 UI + 后端 API
- **来源**：@restregular/dsh-memory 管理面板

---

## 五、不建议做的升级

| 升级 | 原因 |
|---|---|
| 三层记忆分离 | 过度工程化，单层 + 长期事实已够用 |
| SQLite/向量检索 | 记忆量级太小，线性扫描足够 |
| 记忆关联图 | 桌宠场景不需要记忆间的图遍历 |
| 9 个 Provider 插件化 | JSON 文件足够轻量 |
| Composable View 完整架构 | 只借鉴 eager/routed 思路即可，不需要 Strategy/Source/Core 三层 |
| Skill Evolution | 完全不同的职责 |
| 13 个工具 | 2-3 个工具（remember + recall + 可选 forget）足够 |

---

## 六、实施路线图

```
Phase 1 (P0): 显式/隐式检测 + 去重 + 双重预算
  ↓
Phase 2 (P1): recall 工具 + 容量管理 + 来源标记
  ↓
Phase 3 (P2, 可选): idle review / JSONL / 管理面板
```

每个 Phase 独立可交付，不依赖下一个 Phase。Phase 1 改动最小（~60 行），收益最明显。

---

## 七、与 task1 方案的关系

task1（`docs/task1-pet-memory-simplification.md`）已完成"桌宠前端记忆下沉到 DSH 后端"——@dsh-pet/memory 就是下沉后的记忆插件。本方案是 task1 的延续：在 @dsh-pet/memory 已有打分公式基础上，借鉴 dsh-mnemon 和社区插件的有用部分，做增量升级。

**核心原则**：做减法不做加法。每个升级建议都先问"桌宠场景真的需要这个吗？"，不需要的即使技术上有趣也不做。