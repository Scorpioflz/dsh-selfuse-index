# 任务1：桌宠记忆下沉 DSH 插件层方案

> 状态：实施完成（待迁移旧数据）
> 目标：简化 dsh-pet-chubby_blue_whale 前端，让记忆的实现/记录/调整/遗忘全部下沉到 DSH 插件层，桌宠只做纯前端。

---

## 一、三项目记忆机制对比

### 1.1 dsh-fish-memory（推荐）

| 维度 | 实现 |
|------|------|
| 形式 | 单文件插件 `lib/index.js`（6309 行） |
| 存储 | 每会话一 JSON 文件 `memory<sid>.json` |
| 记忆结构 | `{ id, content, tags[], score, createdAt, lastAccessedAt, accessCount, importance, emotion, activated }` |
| 打分公式 | `P = C × (baselineWeight + activationWeight×A + importanceWeight×I + emotionWeight×E)` |
| 衰减 | 30 天半衰期（`baseHalfLifeDays`，可配），不删除只衰减 |
| 写入触发 | `remember` 工具，由模型主动调用 |
| 注入方式 | 通过 `systemPrompt.context` 注入（非 section，避免废系统提示词缓存） |
| 长期事实 | 有 factsMax 机制，高价值记忆常驻 |
| 工具暴露 | `remember`（写入）、`recall`（检索）、`forget`（遗忘）、`update_memory`（调整） |

**与桌宠需求匹配度**：高。记忆生命周期完整、配置灵活、注入方式优雅、单文件易部署。

### 1.2 dsh-mnemon

| 维度 | 实现 |
|------|------|
| 形式 | 三层可组合生态（Source/Strategy/Core），18 个子插件 |
| 工具数 | 16 个 |
| Provider | 9 个（向量/图/时序等） |
| 机制 | View 不可变、关系图、技能自进化 |

**与桌宠需求匹配度**：低。功能过剩——关系图、技能自进化、Provider 矩阵桌宠都用不上，部署与维护成本高。

### 1.3 dsh-pet-chubby_blue_whale 当前自带记忆（需移除）

桌宠在 Python 侧有**完整记忆系统**（约 2500 行），与 DSH 插件层职责重叠：

| 文件 | 行数 | 职责 |
|------|------|------|
| `pet/chat/memory.py` | 1104 | 四层记忆（user/fact/lesson/topic）、跨进程锁、原子写盘、命中队列 |
| `pet/chat/memory_recall.py` | 531 | BM25 打分、艾宾浩斯衰减（14 天半衰期）、已见去重、topic 归档 |
| `pet/chat/memory_extract.py` | 306 | 每 5 轮自动提炼记忆 |
| `pet/chat/prompt.py` | 148 | **客户端拼接** system prompt + memory_text + recall_text |

**关键发现**：桌宠当前在客户端做 system prompt 拼接，这与 DSH 的 `systemPrompt.context` 注入机制冲突——若两边都注入记忆，会重复。

---

## 二、推荐方案：fish-memory 作为桌宠记忆后端

### 2.1 架构变化

```
变更前：
  桌宠 Python ──(自带 memory.py 读写本地 JSON)──> 本地记忆文件
  桌宠 Python ──(拼接 prompt.py)──> DSH webapi ──> 模型

变更后：
  桌宠 Python ──(纯 UI + 会话管理)──> DSH webapi ──(fish-memory 插件)──> 模型
                                          └──(记忆读写)──> DSH 会话目录下 JSON
```

### 2.2 桌宠需保留的职责

1. **会话-角色映射**：每个 character_id 对应独立 DSH sessionId（已有 `dsh_session.json`）
2. **工作区管理**：角色对应的 DSH workspaceId
3. **system prompt 首发**：角色人设通过 `POST /sessions` 的 `systemPrompt` 字段一次性注入（fish-memory 的记忆通过 `context` 字段注入，不冲突）
4. **UI 交互**：聊天气泡、桌宠动画、用户操作

### 2.3 桌宠需移除的代码

| 文件 | 处理 |
|------|------|
| `pet/chat/memory.py` | **删除**（1104 行） |
| `pet/chat/memory_recall.py` | **删除**（531 行） |
| `pet/chat/memory_extract.py` | **删除**（306 行） |
| `pet/chat/prompt.py` | **重写**：移除 memory_text/recall_text 拼接，仅保留 system prompt 首发（148 → 约 30 行） |
| 相关 import 与调用点 | 清理 |

**预计净减约 2000 行代码。**

### 2.4 fish-memory 配置调整

| 参数 | 原默认 | 建议值 | 理由 |
|------|--------|--------|------|
| `baseHalfLifeDays` | 30 | 14 | 对齐桌宠原艾宾浩斯 14 天半衰期 |
| `baselineWeight` | - | 保持 | - |
| `activationWeight` | - | 保持 | - |
| `importanceWeight` | - | 适当调高 | 桌宠对话中"重要"信号较强 |
| `emotionWeight` | - | 适当调高 | 桌宠有情感维度 |
| `factsMax` | - | 保持 | 长期事实常驻机制有用 |

### 2.5 system prompt 引导

在角色 system prompt 中追加一段引导，让模型主动调用 `remember`：

```
当你从对话中识别到以下信息时，请调用 remember 工具记录：
- 关于用户的长期事实（偏好、身份、习惯）
- 重要的约定或承诺
- 情感显著的时刻
记录时设置合适的 importance（1-10）和 emotion（-1 到 1）。
```

---

## 三、数据迁移方案

桌宠现有记忆数据需迁移到 fish-memory 格式。

### 3.1 迁移脚本逻辑

```
对每个 character_id:
  1. 读取桌宠旧记忆文件（四层：user/fact/lesson/topic）
  2. 对每条记忆：
     - content = 旧记忆文本
     - tags = [对应层级名]  # user/fact/lesson/topic → tag
     - importance = 旧打分映射到 1-10
     - emotion = 0（旧数据无情感维度，默认中性）
     - createdAt/lastAccessedAt = 旧时间戳
     - accessCount = 旧命中次数
  3. 写入 fish-memory 的 memory<sid>.json（sid = 该角色的 DSH sessionId）
```

### 3.2 迁移注意

- 旧记忆的 topic 层有"归档"概念，fish-memory 无归档只有衰减——归档记忆可降低 importance 后导入
- 旧记忆的 lesson 层有"已见去重"，迁移时需保留 accessCount 以维持衰减曲线
- 迁移脚本一次性运行，运行后旧文件备份不删

---

## 四、风险与注意事项

| 风险 | 影响 | 缓解 |
|------|------|------|
| fish-memory 记忆按 DSH 会话隔离，桌宠多角色多会话需确认 sessionId 稳定 | 中 | 桌宠已有 `dsh_session.json` 维持映射，风险可控 |
| 模型不主动调用 `remember` 导致记忆不写入 | 高 | system prompt 引导 + 前期人工抽检 |
| 旧记忆迁移后打分体系不一致，检索排序变化 | 中 | 迁移后观察一周，微调权重 |
| fish-memory 单文件 6309 行，未来维护依赖上游 | 低 | 浅克隆，可 fork |
| 桌宠移除记忆代码后，离线场景无记忆 | 低 | 桌宠本就依赖 DSH webapi，离线本不可用 |

---

## 五、待讨论决策点

1. **fish-memory vs 自研精简版**：是直接用 fish-memory，还是参考它写一个更精简的桌宠专用记忆插件？
2. **多角色记忆隔离粒度**：每角色独立 sessionId（当前方案）vs 共用一个 sessionId 用 tag 区分角色？
3. **记忆迁移时机**：先部署新架构再迁移 vs 迁移后再切换？
4. **fish-memory 配置调优**：权重值需实际对话数据校准，是否先小范围试跑？
5. **prompt.py 重写边界**：system prompt 首发是否完全移到 DSH 侧（`POST /sessions` 时传入），还是桌宠仍保留一份？
6. **emotion 维度**：旧记忆无情感，迁移默认 0；新记忆由模型判断 emotion，是否需要桌宠侧再校准？
---

## 六、实施记录（2026-10-29）

### 6.1 已完成

#### A. 桌宠自带记忆系统移除
- 删除 `pet/chat/memory.py`（1104 行）、`pet/chat/memory_recall.py`（531 行）、`pet/chat/memory_extract.py`（306 行）
- 删除对应测试 `tests/test_chat_memory.py`、`test_chat_memory_extract.py`、`test_memory_recall.py`
- 清理 9 个引用方文件中的记忆相关代码（prompt.py、service.py、legacy_widgets.py、widgets.py、ai_settings_page.py、quick_chat.py、app.py、config.py、modern_settings_dialog.py）
- 保留 `pet/proactive/memory.py`（主动识屏记忆）和 `pet/memory_trim.py`（Windows 内存修剪），与聊天记忆无关

#### B. 工作区随角色走改造
- 重写 `pet/dsh_workspace.py`：从全局工作区改为按角色绑定，新增 `get_character_workspace_title()`、`ensure_character_workspace_title()`、`bind_character_workspace()`、`unbind_character_workspace()`
- 重写 `pet/chat/dsh_provider.py`：数据结构改为每角色一个工作区（path=`~/.dsh-pet-workspace/<char_id>`），兼容旧格式自动迁移
- 修改 `pet/app.py` 的 `switch_character`：切换角色时检查工作区绑定，未绑定则弹窗要求提供工作区名称

#### C. 记忆插件创建（`integrations/dsh-pet-memory/`）
- 基于 fish-memory 源码改造，存储路径改为 `dsh-pet-memory`
- `baseHalfLifeDays` 从 30 改为 14（对齐桌宠原艾宾浩斯半衰期）
- **核心改造**：加 workspace 映射缓存，`storePath(sid)` 有 workspace 映射时用 `ws-<workspaceId>.json`（按工作区共享记忆），否则回退 `<sessionId>.json`
- 在 `apply(ctx)` 中初始化 workspaceRegistry 并定期刷新缓存

#### D. 记忆插件安装检查与设置入口
- 新建 `pet/memory_plugin_link.py`：检查 `@dsh-pet/memory` 是否已安装到 DSH profile，提供 `install_memory_plugin()` 一键安装函数
- 在 `pet/app.py` 启动流程中集成检查：DSH provider 启用时，未安装记忆插件则气泡提醒
- 在 `pet/chat/ai_settings_page.py` 添加"DSH 记忆插件"设置区：状态显示 + 一键安装按钮（仅 DSH provider 可见）

### 6.2 决策点落实

| 决策点 | 落实 |
|--------|------|
| 1. fish-memory vs 自研 | 直接用 fish-memory 改造为 dsh-pet-memory |
| 2. 多角色记忆隔离 | 每角色一个工作区，工作区内共享记忆（非每角色独立 sessionId） |
| 3. 迁移时机 | 先部署新架构，旧数据迁移待做 |
| 5. prompt.py 边界 | system prompt 仍由桌宠首发，记忆由插件通过 context 注入 |

### 6.3 待完成

- 旧记忆数据迁移脚本（§三）
- fish-memory 配置权重校准（§2.4，需实际对话数据）
- system prompt 引导段（§2.5，建议追加 remember 工具引导）