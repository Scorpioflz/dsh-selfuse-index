# DSH 插件市场调研 — 能丰富桌宠助手能力的插件建议

> 生成时间：2026-11-01 | 数据来源：GitHub API 搜索（`topic:dsh-plugin` + 关键词搜索）
> 桌宠现有功能模块：weather / divination / todo / festival / voice / music / chat / file_interpret / vision / proactive / agent_link / dynamic_island / quick_launch / system_tools
> 已安装 DSH 插件：dsh-webapi / dsh-balance-panel / @dsh-cbw/bilibili / dsh-chat-manager / dsh-skills-manager / dsh-custom-reasoning / billion-context / dsh-univer-office / dsh-preset-bridge / modsearch / cc-safety-net / dsh-persona-dafeiyu / @dsh-cbw/memory / dsh-codex-style-computer-use

---

## 一、桌宠/宠物增强（Live2D、素材、成就系统）

| 插件 | ★ | 说明 | 优先级 | 推荐理由 |
|---|---|---|---|---|
| [Sutera-Diffusus/dsh-whale-musume](https://github.com/Sutera-Diffusus/dsh-whale-musume) | 194 | 鲸鱼娘桌宠：45 项成就、3 个小游戏、跨端存档迁移；按工具类型切换工作姿态 | **高** | 成就系统+小游戏+工作姿态切换，直接丰富桌宠的互动性和趣味性 |
| [crafter-station/petdex](https://github.com/crafter-station/petdex) | 4308 | 动画宠物画廊：多宠物素材库 | **高** | 为桌宠提供更多角色素材选择 |
| [Loping151/dsh-nekowhale-stickers](https://github.com/Loping151/dsh-nekowhale-stickers) | 125 | 大肥鱼/GPT娘 贴纸知识包 | 中 | 贴纸/表情包可丰富桌宠的气泡表达 |
| [Andersen216/dsh-whale-girl-live2d](https://github.com/Andersen216/dsh-whale-girl-live2d) | 76 | Live2D 鲸鱼娘桌宠 | 中 | Live2D 方案参考（若桌宠未来想引入 Live2D） |
| [A8Chann/dsh-pet-live2d](https://github.com/A8Chann/dsh-pet-live2d) | 64 | Live2D 桌宠：可拖动、跟随鼠标、状态切换 | 中 | 同上 |
| [cyanfish-x/dsh-live2d-pets](https://github.com/cyanfish-x/dsh-live2d-pets) | 32 | Live2D 桌宠 + 互动陪伴 | 中 | 同上，内置宽松许可预设模型 |
| [liyupi/dsh-kun-like-pet](https://github.com/liyupi/dsh-kun-like-pet) | 112 | 小坤宠：9 种动作，任务完成播放音效 | 低 | 动作状态机思路可参考 |
| [MeteorNOX/DeepSeek-Balance-Whale-Widget](https://github.com/MeteorNOX/DeepSeek-Balance-Whale-Widget) | 6676 | 余额监控小鲸鱼娘 | 低 | 已有 dsh-balance-panel，但桌宠形态的余额监控可参考 |

---

## 二、记忆/知识增强（RAG、本体论、持续学习）

| 插件 | ★ | 说明 | 优先级 | 推荐理由 |
|---|---|---|---|---|
| [Soren-ABT/dsh-knowledge](https://github.com/Soren-ABT/dsh-knowledge) | 86 | 知识库 & RAG：chunking、本地 embedding、向量检索 | **高** | @dsh-cbw/memory 目前是对话记忆，缺知识库/RAG 能力；此插件补齐"文档知识"维度 |
| [PerryLink/dsh-library](https://github.com/PerryLink/dsh-library) | 23 | 本地文档知识库：library_add/remove/list、混合检索 | **高** | 轻量文档库，可参考或直接用，让桌宠能查本地文档 |
| [tancheng33/dsh-ontology](https://github.com/tancheng33/dsh-ontology) | 21 | 本体论/推理：TBox + ABox | 中 | 结构化知识表示，适合工程场景记忆（桌宠正朝通用助手发展） |
| [jasen215/dsh-continual-harness](https://github.com/jasen215/dsh-continual-harness) | 14 | 持续学习：自改进 agent | 中 | 持续学习思路可借鉴到 @dsh-cbw/memory 的 idle review |
| [NeoHotaru/dsh-knowledge-canvas](https://github.com/NeoHotaru/dsh-knowledge-canvas) | 13 | 树形知识库 + 右侧画布编辑 | 中 | 树形知识结构，适合桌宠设置页展示 |
| [Asher-2000/dsh-memory-connect](https://github.com/Asher-2000/dsh-memory-connect) | 8 | 跨会话记忆：自动提取、语义召回、调度 | 中 | 可对比 @dsh-cbw/memory 的实现差异 |
| [xiehuan123/dsh-deepread](https://github.com/xiehuan123/dsh-deepread) | 66 | 证据优先阅读：文章/书籍/PDF → 可追溯 | 中 | 文档深度阅读，配合桌宠 file_interpret |

---

## 三、语音/TTS 增强（语音输入、声音克隆、全双工）

| 插件 | ★ | 说明 | 优先级 | 推荐理由 |
|---|---|---|---|---|
| [beiyege-01/dsh-voice-ai-girlfriend](https://github.com/beiyege-01/dsh-voice-ai-girlfriend) | 861 | 语音 AI：Whisper 语音输入 + Qwen3-TTS 声音克隆 | **高** | 桌宠 voice 模块目前只有 TTS 输出，缺语音输入；Whisper ASR + 声音克隆大幅提升交互 |
| [Yuuyuko-uu/dsh-tts-bridge](https://github.com/Yuuyuko-uu/dsh-tts-bridge) | 207 | DSH 朗读桥：会话内容自动朗读 | **高** | 与桌宠 voice 模块互补，让 DSH 会话也能朗读 |
| [PolinniZhong/dsh-omi-voice](https://github.com/PolinniZhong/dsh-omi-voice) | 75 | 豆包 TTS 朗读：沉浸式听 | 中 | 桌宠 voice 已支持豆包 TTS，可参考其沉浸式实现 |
| [ppy-web/dsh-plugin-xiaomi-mimo-tts](https://github.com/ppy-web/dsh-plugin-xiaomi-mimo-tts) | 40 | 小米 MiMo TTS + 豆包 Seed TTS + 桌宠联动 | 中 | 明确提到"桌宠联动"，值得研究 |
| [haoku123/dsh-voice](https://github.com/haoku123/dsh-voice) | 5 | 全双工语音：mic → SenseVoice ASR | 中 | 全双工语音对话，桌宠朝助手发展需要 |
| [PerryLink/dsh-talk](https://github.com/PerryLink/dsh-talk) | 18 | 语音优先会话循环：麦克风按钮 | 低 | 语音交互 UI 参考 |
| [xcw520/dsh-dania-voice](https://github.com/xcw520/dsh-dania-voice) | 25 | 本地 GPT-SoVITS TTS | 低 | 本地 TTS 方案参考 |

---

## 四、角色扮演/人设（酒馆、角色卡、长篇记忆）

| 插件 | ★ | 说明 | 优先级 | 推荐理由 |
|---|---|---|---|---|
| [Amakurai/dsh-liketavern](https://github.com/Amakurai/dsh-liketavern) | 230 | SillyTavern 风格角色扮演 | **高** | 桌宠有人设注入（dsh-persona-dafeiyu），但缺角色扮演深度；酒馆式交互丰富桌宠对话 |
| [a86582751/dsh-nexttavern](https://github.com/a86582751/dsh-nexttavern) | 216 | 长篇角色扮演：角色卡导入、分支对话、长篇记忆、关键词+语义检索 | **高** | 长篇记忆+分支对话，与 @dsh-cbw/memory 互补 |
| [oliblue-evan/dsh-roleplay-preset](https://github.com/oliblue-evan/dsh-roleplay-preset) | 32 | 沉浸式角色扮演预设：零工具纯对话、酒馆式演出 | 中 | 人设预设参考 |
| [chinosk6/dsh-roleplay](https://github.com/chinosk6/dsh-roleplay) | 23 | 角色扮演：角色卡创作+导入 | 中 | 角色卡管理 |
| [loonai321/dsh-humanized-deepseek-maid](https://github.com/loonai321/dsh-humanized-deepseek-maid) | 12 | 人性化鲸鱼女仆人设 | 低 | 人设内容参考（与当前人设模板对比） |

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

## 十一、上下文/会话管理（多 agent、跨会话、侧边栏）

| 插件 | ★ | 说明 | 优先级 | 推荐理由 |
|---|---|---|---|---|
| [NanmiCoder/dsh-agent-teams](https://github.com/NanmiCoder/dsh-agent-teams) | 2622 | Agent Teams 多智能体协作 | **高** | 桌宠目前单 agent，多智能体协作大幅扩展能力 |
| [heartmove/dsh-session-bridge](https://github.com/heartmove/dsh-session-bridge) | 8 | 跨会话驱动：创建/发送/等待/读取/恢复/跨工作区查找 | **高** | 桌宠 agent_link 可借此驱动其他 DSH 会话 |
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

## 汇总：按优先级排序的 Top 20 推荐

| # | 插件 | 类别 | ★ | 核心价值 |
|---|---|---|---|---|
| 1 | Sutera-Diffusus/dsh-whale-musume | 桌宠增强 | 194 | 成就系统+小游戏+工作姿态切换 |
| 2 | crafter-station/petdex | 桌宠增强 | 4308 | 动画宠物素材库 |
| 3 | Soren-ABT/dsh-knowledge | 记忆/知识 | 86 | 知识库 & RAG，补齐文档知识维度 |
| 4 | PerryLink/dsh-library | 记忆/知识 | 23 | 轻量本地文档库 |
| 5 | beiyege-01/dsh-voice-ai-girlfriend | 语音 | 861 | Whisper 语音输入 + 声音克隆 |
| 6 | Yuuyuko-uu/dsh-tts-bridge | 语音 | 207 | DSH 朗读桥 |
| 7 | Amakurai/dsh-liketavern | 角色扮演 | 230 | SillyTavern 风格角色扮演 |
| 8 | a86582751/dsh-nexttavern | 角色扮演 | 216 | 长篇角色扮演 + 分支对话 |
| 9 | Alterssss/dsh-bili-whale | B站 | 823 | 按作息刷 B 站 + 双日记 |
| 10 | titanwings/dsh-automation | 自动化 | 103 | 编码任务按计划自动运行 |
| 11 | GooDAnDReaDY/dsh-cron | 自动化 | 13 | 通用定时 cron 任务 |
| 12 | john-walks-slow/dsh-proactive | 自动化 | 8 | 主动跟进 + 闹钟调度 |
| 13 | Clizo1209/dsh-playwright-browser | 浏览器 | 16 | Playwright 浏览器自动化 |
| 14 | HuanLinOTO/dsh-plugin-mineru | 文档 | 51 | MinerU 多格式文档解析 |
| 15 | omdsh-dev/dsh-office | 文档 | 29 | Office 三件套 |
| 16 | wsz987/dsh-channels | 消息 | 13 | 微信/QQ/钉钉/飞书/Telegram 接入 |
| 17 | Lxiayu/DshCockpit | 监控 | 40 | token 用量/成本追踪 |
| 18 | NanmiCoder/dsh-agent-teams | 多agent | 2622 | 多智能体协作 |
| 19 | heartmove/dsh-session-bridge | 会话 | 8 | 跨会话驱动 |
| 20 | gychen-NJU/dsh-game-daily | 游戏 | 34 | 游戏日常代理（原神/崩坏3） |

---

## 附录：搜索方法

- GitHub API: `q=topic:dsh-plugin` 按星降序，50 条
- GitHub API: `q=dsh+plugin in:name,description` 按星降序，50 条
- GitHub API: 分类关键词搜索（pet/memory/tool/mcp/automation/persona/bilibili/music/voice/weather/news/todo/file/document/office/pdf/image/vision/draw/canvas/notify/message/chat/monitor）
- 搜索时间：2026-11-01
- 未覆盖：npm 注册表搜索、DSH 内置插件市场 Discover 页面（需 DSH 运行时访问）