# DSH 插件市场调研 — 能丰富桌宠助手能力的插件建议

> 生成时间：2026-11-01 | 最后重新评估：2026-11-01 | 数据来源：GitHub API 搜索（`topic:dsh-plugin` + 关键词搜索）
> 桌宠现有功能模块：weather / divination / todo / festival / voice / music / chat / file_interpret / vision / proactive / agent_link / dynamic_island / quick_launch / system_tools
> 桌宠角色：shenshen（鲸鱼娘，帧序列 `lossless-frame-v1`，非 Live2D），动作 7 类（click/drag/events/idle/move/random/turn）
> 桌宠 TTS：4 引擎（doubao/edge/mimo/sapi），缺 ASR 语音输入
> 已安装 DSH 插件：dsh-webapi / dsh-balance-panel / @dsh-cbw/bilibili / dsh-chat-manager / dsh-skills-manager / dsh-custom-reasoning / billion-context / dsh-univer-office / dsh-preset-bridge / modsearch / cc-safety-net / dsh-persona-dafeiyu / @dsh-cbw/memory / dsh-codex-style-computer-use / **dsh-knowledge（2026-11-01 新装）** / **dsh-session-bridge（2026-11-01 新装）**
>
> **重新评估说明（2026-11-01）**：一~四章已按用户要求重新过滤/评估：
> - **一、桌宠**：过滤掉其他角色资源（petdex/Live2D 系列），只保留能丰富 shenshen 的思路；新增自研建议（动作类型扩展/成就系统/工作姿态联动）
> - **二、记忆**：逐个判定"独立并存 vs 整合到 @dsh-cbw/memory"——dsh-knowledge/dsh-ontology/dsh-deepread 独立并存（职责不同），dsh-memory-connect/dsh-continual-harness 已整合或已吸收
> - **三、语音**：整体下调优先级（TTS 已够用，缺的是 ASR），未来路线：ASR > 声音克隆 > 全双工
> - **四、人设**：在 dsh-persona-dafeiyu 基础上评估，补齐动态角色扮演/角色经历累积/分支对话（dsh-liketavern/dsh-nexttavern），注意 systemPrompt 段落 order 不冲突

---

## 一、桌宠/宠物增强（丰富已有角色 shenshen 的动作与互动）

> **重新评估（2026-11-01）**：用户明确**不需要其他角色资源**，目标是**丰富已有角色 shenshen**（更多动作、成就、工作姿态等）。
> 当前桌宠是 PySide6 帧序列方案（`lossless-frame-v1`，非 Live2D），角色资源在 `assets/characters/shenshen/frameseq/` 下按动作类型组织（现有 7 类：click/drag/events/idle/move/random/turn），通过 `character.json` 索引、`sprite_behavior` 管理状态机。
> **筛选标准**：(1) 必须能整合到当前帧序列桌宠系统（非 Live2D、非独立应用）；(2) 提供的是"丰富 shenshen"的能力/思路，而非新角色素材。

| 插件 | ★ | 说明 | 优先级 | 整合方式 | 评估 |
|---|---|---|---|---|---|
| [Sutera-Diffusus/dsh-whale-musume](https://github.com/Sutera-Diffusus/dsh-whale-musume) | 194 | 鲸鱼娘桌宠：45 项成就、3 个小游戏、跨端存档迁移；按工具类型切换工作姿态 | 中 | **借鉴思路，自研模块** | 它是独立桌宠应用，非 DSH 插件，不能直接装。但三个思路可借鉴到 shenshen：①成就系统（作为桌宠新 feature module，记录互动里程碑）；②工作姿态切换（根据 DSH 当前任务类型切换 shenshen 的 idle/work/busy 动画）；③内置小游戏（喂食/点击小游戏，用帧序列实现） |
| [Loping151/dsh-nekowhale-stickers](https://github.com/Loping151/dsh-nekowhale-stickers) | 125 | 大肥鱼/GPT娘 贴纸知识包 | 低 | **气泡表达扩展** | 贴纸/表情包可作为 `speech_bubble` 的图片气泡扩展，但当前气泡以文字为主，收益有限 |
| [liyupi/dsh-kun-like-pet](https://github.com/liyupi/dsh-kun-like-pet) | 112 | 小坤宠：9 种动作，任务完成播放音效 | 低 | **思路已部分实现** | 当前 shenshen 已有 sprite_behavior 状态机+7 类动作，"任务完成音效"思路可借鉴但优先级低 |

**过滤掉（不整合）**：
- `crafter-station/petdex`（4308★）：多宠物素材库 → 用户不需要其他角色
- `Andersen216/dsh-whale-girl-live2d`、`A8Chann/dsh-pet-live2d`、`cyanfish-x/dsh-live2d-pets`：均为 Live2D 方案 → 与当前帧序列渲染管线（PetSprite/MovieLibrary/character_pack）完全不兼容，引入需重写整个渲染层，违背"丰富已有角色"目标
- `MeteorNOX/DeepSeek-Balance-Whale-Widget`（6676★）：余额监控桌宠形态 → 已有 dsh-balance-panel

**自研建议（丰富 shenshen，不依赖外部插件）**：
1. **新增动作类型**：当前 7 类，可扩展 `feeding`（喂食）、`sleep`（睡眠）、`work`（工作姿态）、`celebrate`（庆祝）、`sad`（情绪低落）——只需在 `frameseq/` 下加目录 + `character.json` 加索引，无需改渲染管线
2. **成就系统**（借鉴 dsh-whale-musume）：作为新 feature module（`pet/achievements/`），记录互动里程碑（对话轮数、陪伴时长、任务完成数），成就解锁触发 celebrate 动画
3. **工作姿态联动**：DSH agent 执行任务时，桌宠切换到 work 动画；空闲时回 idle——通过 agent_link 的 DSH 状态（8-state converger）驱动 sprite_behavior

---

## 二、记忆/知识增强（RAG、本体论、持续学习）

> **重新评估（2026-11-01）**：当前 `@dsh-cbw/memory` v0.5.1 是**对话记忆**（remember/recall 工具 + memory-hint 中间件 + 半衰期衰减 + 情感加权 + category 分类 + 归档索引 + LRU），**不是知识库/RAG**。
> **核心判断**：每个插件是"独立并存"还是"整合到 @dsh-cbw/memory"——依据是职责边界与技术栈差异。DSH 插件架构鼓励"挂载到旁边"而非"塞进一个插件"。
> **已安装**：`dsh-knowledge`（2026-11-01，知识库 & RAG，补齐文档知识维度）。当前记忆/知识三件套已齐：`@dsh-cbw/memory`（对话记忆）+ `dsh-knowledge`（文档知识 RAG）+ 桌宠 `file_interpret`（文件解读）。

| 插件 | ★ | 说明 | 优先级 | 整合方式 | 评估 |
|---|---|---|---|---|---|
| [Soren-ABT/dsh-knowledge](https://github.com/Soren-ABT/dsh-knowledge) | 86 | 知识库 & RAG：chunking、本地 embedding、向量检索 | **高** | **独立并存** | 职责完全不同：@dsh-cbw/memory 是"记住用户说过的话"（对话记忆），dsh-knowledge 是"索引用户提供的文档"（文档知识）。技术栈也不同（bigram+半衰期 vs embedding+向量检索）。整合会让 @dsh-cbw/memory 职责膨胀。**注入方式**：通过工具（tool-knowledge）让模型主动检索，非 systemPrompt 段落，与 @dsh-cbw/memory 的 remember/recall 模式一致，无冲突。**补齐"文档知识"维度**。**已安装（2026-11-01）** |
| [PerryLink/dsh-library](https://github.com/PerryLink/dsh-library) | 23 | 本地文档知识库：library_add/remove/list、混合检索 | 中 | **与 dsh-knowledge 二选一** | 与 dsh-knowledge 功能重叠（都是本地文档库），dsh-knowledge 偏 RAG（chunking+embedding），dsh-library 偏轻量管理。dsh-knowledge 已装，不需要 |
| [tancheng33/dsh-ontology](https://github.com/tancheng33/dsh-ontology) | 21 | 本体论/推理：TBox + ABox | **不必要** | — | **2026-11-01 复评：不必要**。本体论是专家系统场景（企业知识图谱/规则推理），需手动建 TBox 本体建模成本高；桌宠朝通用助手发展（非专家系统），dsh-knowledge 的 RAG + @dsh-cbw/memory 的 category 分类已覆盖个人知识管理。无冲突但投入产出比低 |
| [xiehuan123/dsh-deepread](https://github.com/xiehuan123/dsh-deepread) | 66 | 证据优先阅读：文章/书籍/PDF → 可追溯 | **不必要** | — | **2026-11-01 复评：不必要**。与 dsh-knowledge 重叠（都做 PDF/文档解析+检索），dsh-deepread 独有的"证据链追溯（哪段话支撑哪个结论）"是学术研究窄场景；dsh-knowledge 的文档解析（MinerU/mupdf/pdfjs）+ chunking + 检索 + 桌宠 file_interpret 已覆盖通用文档处理。无冲突但投入产出比低 |

**已整合/无需独立安装**：
- `jasen215/dsh-continual-harness`（14★）：持续学习思路**已借鉴**到 @dsh-cbw/memory 的 idle review（4.7 增量定时沉淀已实施），不需要独立装
- `Asher-2000/dsh-memory-connect`（8★）：跨会话记忆+自动提取+语义召回——**已由 @dsh-cbw/memory 实现**，功能重叠，不需要
- `NeoHotaru/dsh-knowledge-canvas`（13★）：树形知识库+画布编辑——与 dsh-knowledge 功能重叠（都是知识库），仅 UI 形态不同，选 dsh-knowledge 后不需要

**整合 vs 独立决策总结**：
| 维度 | 对话记忆 | 文档知识/RAG | 结构化知识 | 阅读流程 |
|---|---|---|---|---|
| 归属 | @dsh-cbw/memory（已有） | dsh-knowledge（独立） | dsh-ontology（独立） | dsh-deepread（独立） |
| 技术 | bigram+半衰期+归档 | embedding+向量检索 | TBox+ABox 推理 | PDF 解析+追溯 |
| 冲突 | — | 无（段落不同） | 无 | 无 |

---

## 三、语音/TTS 增强（声音克隆、全双工）

> **重新评估（2026-11-01）**：优先级**整体下调，放到后面做**。
> 当前桌宠 TTS 已有 4 引擎（`pet/tts/`：doubao/edge/mimo/sapi），voice 模块有 self_talk（自言自语）+ chime（提示音）。
> **DSH 自身已提供语音录入（ASR）功能**，故 ASR 类插件参考移除。剩余方向：①声音克隆（个性化 TTS）> ②全双工对话 > ③DSH 会话朗读桥。

| 插件 | ★ | 说明 | 原优先级 | 新优先级 | 评估 |
|---|---|---|---|---|---|
| [Yuuyuko-uu/dsh-tts-bridge](https://github.com/Yuuyuko-uu/dsh-tts-bridge) | 207 | DSH 朗读桥：会话内容自动朗读 | 高 | **低** | 桌宠已有 4 引擎 TTS，DSH 会话朗读是锦上添花，非必需 |
| [ppy-web/dsh-plugin-xiaomi-mimo-tts](https://github.com/ppy-web/dsh-plugin-xiaomi-mimo-tts) | 40 | 小米 MiMo TTS + 豆包 Seed TTS + 桌宠联动 | 中 | **低** | 已有 mimo TTS 引擎，"桌宠联动"思路可参考但引擎已覆盖 |
| [PolinniZhong/dsh-omi-voice](https://github.com/PolinniZhong/dsh-omi-voice) | 75 | 豆包 TTS 朗读：沉浸式听 | 中 | **低** | 已有 doubao TTS，沉浸式实现可参考 |
| [PerryLink/dsh-talk](https://github.com/PerryLink/dsh-talk) | 18 | 语音优先会话循环：麦克风按钮 | 低 | **低** | UI 参考 |
| [xcw520/dsh-dania-voice](https://github.com/xcw520/dsh-dania-voice) | 25 | 本地 GPT-SoVITS TTS | 低 | **低** | 本地 TTS 方案，已有 4 引擎够用 |

**已移除（DSH 自身提供）**：
- `beiyege-01/dsh-voice-ai-girlfriend`（861★）：Whisper ASR 语音输入——DSH 已自带 ASR；其 Qwen3-TTS 声音克隆部分如未来需要可单独评估
- `haoku123/dsh-voice`（5★）：SenseVoice ASR 全双工——DSH 已自带 ASR

**未来做语音时的路线**（ASR 已由 DSH 提供，无需自做）：
1. 声音克隆（Qwen3-TTS/GPT-SoVITS）→ 个性化桌宠音色
2. 全双工对话（需 DSH ASR + TTS + 打断逻辑联动）
3. DSH 会话朗读桥（锦上添花）

---

## 四、角色扮演/人设（酒馆、角色卡、长篇记忆）

> **重新评估（2026-11-01）**：已安装 `dsh-persona-dafeiyu`，能力：内置 3 条人设（大肥鱼/阿茶/听澜）+ 导入/导出/自建 + 全局/工作区/会话三档生效 + 免重启切换 + 人设广场（外部仓库链接）+ 通过 `systemPrompt.section()` 注入**静态人设文本**。
> **核心问题**：人设插件只注入静态文本，缺**动态角色扮演**（世界书触发、情景记忆、分支对话、角色经历累积）。以下评估每个插件的功能性、必要性、冲突、补充的缺陷。

| 插件 | ★ | 说明 | 优先级 | 整合方式 | 评估 |
|---|---|---|---|---|---|
| [Amakurai/dsh-liketavern](https://github.com/Amakurai/dsh-liketavern) | 230 | SillyTavern 风格角色扮演 | 中 | **独立并存** | **补的缺陷**：人设插件缺动态角色扮演（世界书、情景触发、深度对话）。**冲突风险**：都改 systemPrompt，需确认段落顺序（人设插件 order=0，liketavern 需用不同 order）。**必要性**：中，取决于是否需要酒馆式深度角色扮演。已克隆分析（`_plugin-references/dsh-liketavern`），systemPrompt 冲突结论见下 |
| [a86582751/dsh-nexttavern](https://github.com/a86582751/dsh-nexttavern) | 216 | 长篇角色扮演：角色卡导入、分支对话、长篇记忆、关键词+语义检索 | 中 | **独立并存，与 @dsh-cbw/memory 划清边界** | **补的缺陷**：人设插件缺"角色经历累积"（长篇记忆）和"分支对话"。**与 @dsh-cbw/memory 关系**：维度不同——nexttavern 记的是"角色经历/剧情进展"，@dsh-cbw/memory 记的是"用户事实/偏好"，可并存但需明确边界（建议：角色经历归 nexttavern，用户事实归 memory）。**冲突**：长篇记忆的检索可能与 memory 的 recall 重复触发，需配置优先级 |
| [oliblue-evan/dsh-roleplay-preset](https://github.com/oliblue-evan/dsh-roleplay-preset) | 32 | 沉浸式角色扮演预设：零工具纯对话、酒馆式演出 | 低 | **预设内容参考** | 是 preset（预设），不是独立能力。人设插件已有预设机制，重叠。仅参考预设内容 |
| [chinosk6/dsh-roleplay](https://github.com/chinosk6/dsh-roleplay) | 23 | 角色扮演：角色卡创作+导入 | 低 | **独立并存（仅酒馆生态需要）** | **补的缺陷**：人设插件导入是 .md 文本，角色卡是酒馆生态格式（PNG+JSON embed）。**必要性**：仅在使用酒馆生态角色卡时需要，否则人设插件的 .md 导入已够用 |
| [loonai321/dsh-humanized-deepseek-maid](https://github.com/loonai321/dsh-humanized-deepseek-maid) | 12 | 人性化鲸鱼女仆人设 | 低 | **人设内容参考** | 仅人设内容，人设插件已有大肥鱼+可导入，不需要装。可参考其人设写法 |

**dsh-persona-dafeiyu 缺陷总结与补充建议**：
| 缺陷 | 补充方式 | 优先级 |
|---|---|---|
| 缺动态角色扮演（世界书、情景触发） | dsh-liketavern（独立并存，注意 systemPrompt 段落 order 不冲突） | 中 |
| 缺角色经历累积（长篇记忆） | dsh-nexttavern（独立并存，与 @dsh-cbw/memory 划清边界：角色经历 vs 用户事实） | 中 |
| 缺分支对话 | dsh-nexttavern | 中 |
| 缺酒馆角色卡格式（PNG+JSON） | dsh-roleplay（仅酒馆生态需要） | 低 |
| 内置人设只有 3 条 | 已由人设广场（外部仓库）解决 | — |

**冲突注意**：
- dsh-liketavern / dsh-nexttavern 都注入 systemPrompt，必须与 dsh-persona-dafeiyu 的 `dafeiyu:persona` 段落（order=0）用不同 order，避免覆盖
- dsh-nexttavern 的长篇记忆检索与 @dsh-cbw/memory 的 recall 可能重复，需配置触发优先级（建议：角色扮演场景 nexttavern 优先，通用对话 memory 优先）

**dsh-liketavern systemPrompt 冲突确认（2026-11-01，已读源码 `src/agent.ts:99`）**：
- dsh-liketavern 注入两个段落：
  - `tavern:standing`（角色卡+预设骨架）— `order = getSectionOrder('TOOLS_SDK') + 10`，**在工具说明之后**
  - `tavern:turn`（runtime context，每轮世界书/记忆）— `order = 20`
- dsh-persona-dafeiyu 注入 `dafeiyu:persona`（人设文本）— `order = DEPLOYMENT_PERSONA_PREFIX = 0`，**在工具前缀之前**
- **技术层面：无冲突**。三者 order 完全不同（0 < 20 < TOOLS_SDK+10），不会互相覆盖，DSH 段落合并会按 order 排序拼接
- **语义层面：需注意**。同时启用时模型会收到两份"你是谁"定义——dafeiyu 的人设文本（如"你是大肥鱼"）+ liketavern 的角色卡 systemPrompt（如"你是艾莉亚"）。若两者描述的角色不一致，模型可能困惑
- **使用建议**：
  - 用 liketavern 角色扮演时，把 dafeiyu 人设切到「此会话不启用」（dafeiyu 支持会话级关闭），避免双重人设
  - 或让 dafeiyu 人设与 liketavern 角色卡描述保持一致（dafeiyu 注入通用风格，liketavern 注入具体角色剧情）
  - 日常非角色扮演对话：只用 dafeiyu，不绑 liketavern 角色卡（liketavern 未绑卡时 standing 为固定短文案，不冲突）

**未来丰富角色扮演的解决方案（2026-11-01 决策，待执行）**：
- **方案选择**：方案2（人设文档补充角色卡映射 + 生成 liketavern 角色卡 JSON），**不整合插件**（方案1 已否决：两个第三方插件，liketavern 是完整酒馆运行时，整合代价极高且违背已放弃自研人设插件决策）
- **执行步骤**（未来需要时）：① 在 `docs/大肥鱼_蓝鲸女仆人设模板.md` 末尾加"角色卡映射"附录（人设字段 → liketavern chara_card_v2 字段：name/description/personality/scenario/first_mes/mes_example）② 生成 `docs/大肥鱼_角色卡.json` ③ 导入 liketavern
- **使用模式**：日常对话 dafeiyu 注入人设文档全文；深度角色扮演 liketavern 导入角色卡 JSON + dafeiyu 切「此会话不启用」；人设文档是 single source of truth，角色卡从它派生

---

## 五、B 站增强（视频理解、自动回复、悬浮看片）

> 已有 @dsh-cbw/bilibili（fork 自 dsh-bili-scroll），以下为补充能力

| 插件 | ★ | 说明 | 优先级 | 推荐理由 |
|---|---|---|---|---|
| [Alterssss/dsh-bili-whale](https://github.com/Alterssss/dsh-bili-whale) | 823 | 有日子的鱼：按作息刷 B 站、真看懂视频、写两本日记 | **高** | "按作息"和"两本日记"思路可借鉴到 @dsh-cbw/bilibili |
| [InariNGT-Ofiicial/dsh-bili-humanism](https://github.com/InariNGT-Ofiicial/dsh-bili-humanism) | 217 | 人类世界训练人格：历史/收藏/点赞/投币 | 中 | 用 B 站行为数据训练人格，与桌宠人设互补 |
| [bronyacccxz/dsh-bilibili-reply](https://github.com/bronyacccxz/dsh-bilibili-reply) | 111 | 自动回复 @ 你的视频：带时间戳评论 | 中 | @dsh-cbw/bilibili 有评论功能，此插件的时间戳评论可借鉴 |
| [icyaaaww/dsh-bili-vision](https://github.com/icyaaaww/dsh-bili-vision) | 7 | B 站视频理解：时间戳帧、本地 ASR/OCR | 中 | 视频理解能力，@dsh-cbw/bilibili 的分镜图可参考 |
| [Sacredbluedragon/dsh-bili-watch](https://github.com/Sacredbluedragon/dsh-bili-watch) | 6 | 给模型看 B 站视频：字幕/转写/抽帧 OCR/评论/弹幕 | 中 | 同上，更全面 |
| [pyf2818/dsh-bili-widget](https://github.com/pyf2818/dsh-bili-widget) | 5 | B 站悬浮看片：边 coding 边刷视频 | 低 | 悬浮窗看片，与桌宠 overlay 形态互补 |
| [holoiallo/dsh-bili-scroll](https://github.com/holoiallo/dsh-bili-scroll) | 14 | dsh-bili-scroll 二改：赤石模式/巡航狂暴/UP订阅/评论台账 | 低 | 上游 fork 的 fork，功能思路可参考 |

---

## 六、自动化/定时任务（cron、主动跟进、日程）

| 插件 | ★ | 说明 | 优先级 | 推荐理由 |
|---|---|---|---|---|
| [titanwings/dsh-automation](https://github.com/titanwings/dsh-automation) | 103 | 编码任务按计划在独立 Session 运行 + 定时任务管理 | **高** | 桌宠有 todo/提醒，但缺"让 AI 自动执行任务"能力 |
| [GooDAnDReaDY/dsh-cron](https://github.com/GooDAnDReaDY/dsh-cron) | 13 | 定时 cron 任务 + 后台自动化 + agent 执行 | **高** | 通用定时任务，可让桌宠定时触发 DSH 任务 |
| [john-walks-slow/dsh-proactive](https://github.com/john-walks-slow/dsh-proactive) | 8 | 主动跟进：模型调度 host 级闹钟 | **高** | 桌宠有 proactive（主动识屏），此插件是"主动跟进"互补 |
| [dsh-plugin-collection/dsh-later](https://github.com/dsh-plugin-collection/dsh-later) | 5 | 定时发送：到点自动以你的身份送出 | 中 | 定时消息发送 |
| [aa1355721445-lgtm/dsh-daily-schedule](https://github.com/aa1355721445-lgtm/dsh-daily-schedule) | 5 | 每日日程：每晚生成第二天全天日程 | 中 | 日程生成，与桌宠 todo/festival 互补 |
| [MichengAI/dsh-automation](https://github.com/MichengAI/dsh-automation) | 36 | 独立 Session 执行编码任务 | 低 | 与 titanwings/dsh-automation 类似 |

---

## 七、桌面自动化/Computer Use（浏览器、GUI 操作）

> 已有 dsh-codex-style-computer-use，以下为补充

| 插件 | ★ | 说明 | 优先级 | 推荐理由 |
|---|---|---|---|---|
| [LJL454/dsh-computer-use](https://github.com/LJL454/dsh-computer-use) | 65 | 看屏幕、动鼠标键盘、操作窗口与控件 | 中 | 桌宠有 vision/识屏，此插件补齐"操作"维度 |
| [Clizo1209/dsh-playwright-browser](https://github.com/Clizo1209/dsh-playwright-browser) | 16 | Playwright 浏览器自动化 | **高** | 桌宠缺浏览器自动化能力，Playwright 方案成熟 |
| [IKEASven69/dsh-opencli](https://github.com/IKEASven69/dsh-opencli) | 4 | 登录态真实浏览器 × 180 站点结构化命令 | 中 | 登录态浏览器操作，比 Playwright 更贴近真实用户 |
| [Tencent/BrowserSkill](https://github.com/Tencent/BrowserSkill) | 9858 | 让 AI 用你真实登录的浏览器 | 中 | 腾讯出品，真实浏览器操作 |
| [988hj7tczd-oss/dsh-computer-use](https://github.com/988hj7tczd-oss/dsh-computer-use) | 64 | 跨平台 Computer Use | 低 | 与已有 dsh-codex-style-computer-use 类似 |

---

## 八、文档处理（PDF、Office、论文、文献）

> 已有 dsh-univer-office，以下为补充

| 插件 | ★ | 说明 | 优先级 | 推荐理由 |
|---|---|---|---|---|
| [HuanLinOTO/dsh-plugin-mineru](https://github.com/HuanLinOTO/dsh-plugin-mineru) | 51 | MinerU 文档解析：PDF/图片/DOCX/PPTX/XLSX → Markdown/JSON | **高** | 桌宠 file_interpret 目前能力有限，MinerU 补齐多格式文档解析 |
| [omdsh-dev/dsh-office](https://github.com/omdsh-dev/dsh-office) | 29 | Office 三件套：生成/读取/编辑 | **高** | 与 dsh-univer-office 互补或替代 |
| [sueccku/dsh-plugin-wps-office-next](https://github.com/sueccku/dsh-plugin-wps-office-next) | 28 | WPS 操作：表格/文字/演示，中文对话操作 | 中 | WPS 本地化方案 |
| [GGboya/dsh-paper-reader](https://github.com/GGboya/dsh-paper-reader) | 32 | 论文伴读工作台：PDF 转录/检索/流式问答 | 中 | 论文阅读场景 |
| [Hongcheng-LI/dsh-zotero](https://github.com/Hongcheng-LI/dsh-zotero) | 22 | Zotero 文献管理：搜索/读取元数据/全文 | 中 | 文献管理，学术场景 |
| [taxueseek/dsh-files](https://github.com/taxueseek/dsh-files) | 41 | 文件夹按钮 + 文档解析（PDF/DOCX/XLSX） | 低 | 文件上传 UI 参考 |
| [hairyf/dsh-office-kit](https://github.com/hairyf/dsh-office-kit) | 14 | Office/PDF/演示/表格 | 低 | 与 omdsh-dev/dsh-office 类似 |

---

## 九、通知/消息/社交（微信、QQ、多平台 IM）

| 插件 | ★ | 说明 | 优先级 | 推荐理由 |
|---|---|---|---|---|
| [wsz987/dsh-channels](https://github.com/wsz987/dsh-channels) | 13 | 微信/QQ/钉钉/飞书/Telegram 接入 DSH | **高** | 桌宠目前只接 DSH，接入 IM 后桌宠可代收/代回多平台消息 |
| [GooDAnDReaDY/dsh-messenger-gateway](https://github.com/GooDAnDReaDY/dsh-messenger-gateway) | 5 | Telegram 桥接 | 中 | 单平台桥接参考 |
| [epsilonH-eps/dsh-tts-bridge-wechatagent-bridge](https://github.com/epsilonH-eps/dsh-tts-bridge-wechatagent-bridge) | 5 | 微信语音条：朗读桥声音 → 微信语音 | 中 | 桌宠 voice + 微信联动 |
| [Jesse-njx/dsh-chatnode-wechat](https://github.com/Jesse-njx/dsh-chatnode-wechat) | 7 | 微信监控/审批 DSH agent | 低 | 微信远程控制 DSH |

---

## 十、系统监控（余额、token、性能）

| 插件 | ★ | 说明 | 优先级 | 推荐理由 |
|---|---|---|---|---|
| [Lxiayu/DshCockpit](https://github.com/Lxiayu/DshCockpit) | 40 | 桌面驾驶舱：token 用量/成本追踪/预算 | **高** | 桌宠有 dsh-balance-panel，但缺 token 用量/成本追踪 |
| [jelly-000/dsh-balance-monitor](https://github.com/jelly-000/dsh-balance-monitor) | 9 | 多 provider 余额/配额/token 用量 | 中 | 多 provider 监控 |
| [licyer/dsh-token-monitor](https://github.com/licyer/dsh-token-monitor) | 12 | 模型余量与用量监控 | 中 | 轻量监控 |
| [beltex/dshb](https://github.com/beltex/dshb) | 472 | macOS 系统监控 | 低 | macOS 专用，桌宠是 Windows |
| [epool86/dsh-monitor](https://github.com/epool86/dsh-monitor) | 12 | 实时任务控制：看 agent 和子 agent 工作 | 低 | agent 监控 |

---

## 十一、上下文/会话管理（跨会话、侧边栏）

> **DSH 自身已提供 Agent Team 多智能体协作功能**，故 dsh-agent-teams 参考移除。
> **已安装**：`dsh-session-bridge`（2026-11-01，跨会话驱动，15 个 session_bridge_* 工具）。

| 插件 | ★ | 说明 | 优先级 | 推荐理由 |
|---|---|---|---|---|
| [heartmove/dsh-session-bridge](https://github.com/heartmove/dsh-session-bridge) | 8 | 跨会话驱动：创建/发送/等待/读取-恢复/跨工作区查找 | **高** | 桌宠 agent_link 可借此驱动其他 DSH 会话。**已安装（2026-11-01）** |
| [Fei2411/DS-Bot](https://github.com/Fei2411/DS-Bot) | 4751 | 长生命周期 bot 团队：主 bot + bot 间消息 | 中 | 长生命周期 agent 思路 |
| [bowenliang123/dsh-context](https://github.com/bowenliang123/dsh-context) | 3941 | 上下文洞察和管理 | 中 | 上下文管理参考 |
| [omdsh-dev/DSH-better-sidebar](https://github.com/omdsh-dev/DSH-better-sidebar) | 4790 | 侧边栏底座：文件渲染/终端/对话/Git/子代理 | 低 | 侧边栏增强，与桌宠形态不同 |

---

## 十二、视觉/画图/创意（生成式 UI、无限画布、Figma）

| 插件 | ★ | 说明 | 优先级 | 推荐理由 |
|---|---|---|---|---|
| [liangmianya/dsh-synapse](https://github.com/liangmianya/dsh-synapse) | 636 | 非线性对话工作区：可视化对话画布 | 中 | 非线性对话，桌宠 chat 可参考 |
| [MindLab-Research/dsh-generative-ui](https://github.com/MindLab-Research/dsh-generative-ui) | 109 | 生成式 UI：agent 写 TSX，web UI 编译 | 中 | 生成式 UI 思路 |
| [q253595422/dsh-imagegen-video](https://github.com/q253595422/dsh-imagegen-video) | 69 | 图片+视频生成工作室 + 无限画布 | 中 | 图片/视频生成 |
| [DSH-to-Figma](https://github.com/Duoasa/DSH-to-Figma) | 38 | Figma 集成：读取/编辑设计 | 低 | 设计工具集成 |

---

## 十三、其他工具（游戏、壁纸、Blender、鸿蒙）

| 插件 | ★ | 说明 | 优先级 | 推荐理由 |
|---|---|---|---|---|
| [gychen-NJU/dsh-game-daily](https://github.com/gychen-NJU/dsh-game-daily) | 34 | 游戏日常代理：原神/崩坏3/星穹铁道自动执行 | **高** | 桌宠有 todo/提醒，游戏日常代理是有趣的应用场景 |
| [elysia395/dsh-wallpaper-engine](https://github.com/elysia395/dsh-wallpaper-engine) | 4367 | Wallpaper Engine 壁纸搬进 DSH | 中 | 桌宠 overlay + 壁纸引擎联动 |
| [sixtysevenlf/dsh-blender-plugin](https://github.com/sixtysevenlf/dsh-blender-plugin) | 1511 | Blender 直连：15 个模型工具 | 低 | 3D 建模场景 |
| [1na-ko/dsh-hdc-bridge](https://github.com/1na-ko/dsh-hdc-bridge) | 20 | 鸿蒙开发助手：hdc 设备闭环调试 | 低 | 鸿蒙开发场景 |
| [tian-yu200/dsh-solidworks](https://github.com/tian-yu200/dsh-solidworks) | 20 | SolidWorks 自动化 | 低 | CAD 场景 |

---

## 十四、生态资源（精选列表、插件雷达、手册）

| 资源 | ★ | 说明 | 用途 |
|---|---|---|---|
| [awesome-dsh-plugin/awesome-dsh-plugin](https://github.com/awesome-dsh-plugin/awesome-dsh-plugin) | 21824 | DSH 插件精选列表 | 持续跟踪新插件 |
| [AdamPlatin123/dsh-plugin-radar](https://github.com/AdamPlatin123/dsh-plugin-radar) | 1488 | 插件生态雷达 | 发现新插件 |
| [0xsline/awesome-deepseek-harness](https://github.com/0xsline/awesome-deepseek-harness) | 1287 | DSH 生态精选 | 同上 |
| [Electricitysheep/dsh-handbook](https://github.com/Electricitysheep/dsh-handbook) | 930 | DSH 深度手册 | 开发参考 |
| [PerryLink/dsh-plugin-guide](https://github.com/PerryLink/dsh-plugin-guide) | 65 | 插件开发知识库 | 开发参考 |

---

## 汇总：重新评估后的推荐排序（2026-11-01）

> 原 Top 20 已按四类重新评估调整。桌宠类过滤掉新角色资源；记忆类明确独立 vs 整合；语音类整体下调；人设类降为补缺陷的中优先级。

### 第一梯队（高优先级，建议近期安装）

> 已安装：`dsh-knowledge`（2026-11-01，知识库 & RAG）、`dsh-session-bridge`（2026-11-01，跨会话驱动）

| # | 插件 | 类别 | ★ | 核心价值 | 整合方式 |
|---|---|---|---|---|---|
| 1 | Alterssss/dsh-bili-whale | B站 | 823 | 按作息刷 B 站 + 双日记 | 借鉴思路到 @dsh-cbw/bilibili |
| 2 | titanwings/dsh-automation | 自动化 | 103 | 编码任务按计划自动运行 | 独立并存 |
| 3 | GooDAnDReaDY/dsh-cron | 自动化 | 13 | 通用定时 cron 任务 | 独立并存 |
| 4 | john-walks-slow/dsh-proactive | 自动化 | 8 | 主动跟进 + 闹钟调度 | 独立并存，与桌宠 proactive 互补 |
| 5 | Clizo1209/dsh-playwright-browser | 浏览器 | 16 | Playwright 浏览器自动化 | 独立并存 |
| 6 | HuanLinOTO/dsh-plugin-mineru | 文档 | 51 | MinerU 多格式文档解析 | 独立并存，补齐 file_interpret |
| 7 | omdsh-dev/dsh-office | 文档 | 29 | Office 三件套 | 独立并存，与 dsh-univer-office 互补 |
| 8 | wsz987/dsh-channels | 消息 | 13 | 微信/QQ/钉钉/飞书/Telegram 接入 | 独立并存 |
| 9 | Lxiayu/DshCockpit | 监控 | 40 | token 用量/成本追踪 | 独立并存 |
| 10 | gychen-NJU/dsh-game-daily | 游戏 | 34 | 游戏日常代理 | 独立并存 |

> 已移除：`NanmiCoder/dsh-agent-teams`（DSH 自身已提供 Agent Team 多智能体协作）、`Soren-ABT/dsh-knowledge`（2026-11-01 已安装）、`heartmove/dsh-session-bridge`（2026-11-01 已安装）

### 第二梯队（中优先级，按需安装）

| # | 插件 | 类别 | ★ | 核心价值 | 整合方式 |
|---|---|---|---|---|---|
| 13 | Sutera-Diffusus/dsh-whale-musume | 桌宠增强 | 194 | 成就系统+工作姿态切换思路 | 借鉴思路自研，非直接安装 |
| 14 | Amakurai/dsh-liketavern | 角色扮演 | 230 | SillyTavern 风格，补动态角色扮演 | 独立并存，注意 systemPrompt order |
| 15 | a86582751/dsh-nexttavern | 角色扮演 | 216 | 长篇记忆+分支对话，补角色经历累积 | 独立并存，与 @dsh-cbw/memory 划边界 |

### 第三梯队（低优先级/暂缓）

- 桌宠：Loping151/dsh-nekowhale-stickers（贴纸）、liyupi/dsh-kun-like-pet（思路已部分实现）
- 语音：Yuuyuko-uu/dsh-tts-bridge、ppy-web/dsh-plugin-xiaomi-mimo-tts、PolinniZhong/dsh-omi-voice 等（TTS 已够用，整体暂缓）
- 人设：oliblue-evan/dsh-roleplay-preset、chinosk6/dsh-roleplay、loonai321/dsh-humanized-deepseek-maid（人设插件已覆盖核心功能）

> 已移除：`beiyege-01/dsh-voice-ai-girlfriend`（Whisper ASR）、`haoku123/dsh-voice`（SenseVoice ASR）——DSH 自身已提供语音录入（ASR）功能

### 自研建议（不依赖外部插件）

- **桌宠动作扩展**：为 shenshen 新增 feeding/sleep/work/celebrate/sad 动作类型（加 frameseq 目录 + character.json 索引）
- **桌宠成就系统**：新 feature module，记录互动里程碑，解锁触发 celebrate 动画（借鉴 dsh-whale-musume 思路）
- **桌宠工作姿态联动**：DSH agent 执行任务时切换 work 动画，空闲回 idle（通过 agent_link 8-state 驱动 sprite_behavior）

---

## 附录：搜索方法

- GitHub API: `q=topic:dsh-plugin` 按星降序，50 条
- GitHub API: `q=dsh+plugin in:name,description` 按星降序，50 条
- GitHub API: 分类关键词搜索（pet/memory/tool/mcp/automation/persona/bilibili/music/voice/weather/news/todo/file/document/office/pdf/image/vision/draw/canvas/notify/message/chat/monitor）
- 搜索时间：2026-11-01
- 未覆盖：npm 注册表搜索、DSH 内置插件市场 Discover 页面（需 DSH 运行时访问）