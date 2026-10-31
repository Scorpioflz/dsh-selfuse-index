# 方案二：Bilibili 相关方案

> 状态：分析完成，待讨论
> 日期：2026-10-31
> 分析对象：dsh-bili-scroll（当前插件）+ 社区 B站插件综合评估
> 目标：固定会话方案 + 评估"根据主人 B站 ID 访问收藏夹/观看历史/分析爱好"的可行性
> 历史背景：原 task2（固定会话方案）已整合至 §六

---

## 一、dsh-bili-scroll 当前能力补充

### 1.1 当前插件能做什么

**宿主会话工具**（13 个，用户在 DSH 对话里直接用）：

| 工具 | 功能 |
|---|---|
| `bili_whoami` | 看登录的是谁 |
| `bili_search` | 搜 B站视频（关键词、排序、翻页） |
| `bili_subtitle` | 取视频 AI 字幕全文 |
| `bili_comments` | 取热门评论 |
| `bili_cover` | 看封面（图片附件） |
| `bili_frames` | 看画面帧（从故事板裁 480×270） |
| `bili_reply` | 发评论/回复（有闸门） |
| `bili_status` | 看今天值班状态 |
| `bili_run` | 立刻跑一轮值班 |
| `bili_login_start/poll` | 扫码登录 |
| `bili_setup` | 建 venv 装依赖 |
| `bili_config` | 读/改设置 |

**值班轮工具**（通过 MCP 白名单下发，模型用）：

| 类别 | 工具 |
|---|---|
| 搜索/推荐 | `bili_search`, `bili_recommend`（首页推荐流） |
| 内容 | `bili_subtitle`, `bili_comments`, `bili_danmaku`, `bili_video_info` |
| 看图 | `bili_cover`, `bili_frames` |
| 写动作 | `bili_reply`（条件）, `bili_send_message`（条件） |
| 窄口 IO | `duty_paths/report_append/seen_append/digest_append/seen_recent` |
| 转写 | `bili_transcribe`（本地 Whisper） |

**MCP 服务器端存在但未进白名单的工具**（值班轮用不到）：
`bili_favorite_lists`, `bili_favorite_content`, `bili_hot_videos`, `bili_hot_buzzwords`, `bili_weekly_hot`, `bili_rank`, `bili_user_info`, `bili_user_videos`, `bili_unread_messages`, `bili_received_replies`, `bili_received_at_and_likes`, `bili_crawl`

### 1.2 ⭐ 收藏夹和观看历史（关键发现）

| 数据 | 值班轮模型 | 宿主侧 | 说明 |
|---|---|---|---|
| 收藏夹列表 | ❌ 不在白名单 | ✅ `favops.py` | 宿主侧自动收藏用，模型拿不到 |
| 收藏夹内容 | ❌ 不在白名单 | ❌ | MCP 工具存在但未使用 |
| 收藏视频动作 | ❌ | ✅ `favops.py add` | 宿主侧，模型拿不到 |
| **观看历史** | ❌ | ❌ | **完全不能访问，无此功能** |

**结论**：
1. 插件**能访问用户收藏夹**（列清单 + 收藏视频），但走宿主侧 `favops.py`，值班轮模型用不了
2. 插件**完全不能访问观看历史**——MCP 服务器和整个插件都没有这个功能
3. 值班轮的数据来源是**搜索 + 首页推荐流**，不是收藏夹或观看历史

---

## 二、用户需求分析：根据主人 B站 ID 访问收藏夹/观看历史/分析爱好

### 2.1 需求拆解

用户希望：
1. 输入主人的 B站 ID / 昵称
2. 访问主人的**收藏夹**（公开收藏夹）
3. 访问主人的**观看历史**
4. 分析主人的**爱好**（从收藏夹 + 观看历史推断）
5. 将分析结果**沿用**到桌宠这边（影响推荐/值班/对话风格）

### 2.2 B站 API 能力分析

#### 收藏夹（✅ 可行）

B站公开 API 支持查看**公开**收藏夹：
- `api.bilibili.com/x/v3/fav/resource/list` — 列收藏夹内容（需 fid + 用户 mid）
- `api.bilibili.com/x/v3/fav/folder/created/list-all` — 列用户创建的收藏夹（需 mid）

**限制**：
- 只能看**公开**收藏夹（用户设为私密的看不到）
- 需要登录态（SESSDATA cookie），但可以用值班号登录
- 不需要主人号登录——只需知道主人的 UID

#### 观看历史（⚠️ 有限可行）

B站观看历史 API：
- `api.bilibili.com/x/v2/history` — 获取**自己**的观看历史

**限制**：
- **只能看自己的观看历史**，不能看别人的
- 需要主人号登录（SESSDATA cookie 是主人号的）
- 最多返回 100 条（API 限制）
- **如果用主人号登录，会和主人同时在线冲突**（cookie 踢人）

**结论**：观看历史必须用主人号登录，但会踢主人下线。**不可行**，除非：
- 主人手动导出观看历史（B站设置页有导出功能）
- 或主人提供一个"只读"的 SESSDATA（B站没有这个概念）
- 或只在主人不用 B站时跑（深夜值班）

#### 用户信息（✅ 可行）

- `api.bilibili.com/x/space/acc/info` — 获取用户公开信息（昵称、头像、签名、关注数、粉丝数）
- `api.bilibili.com/x/space/fav/box` — 获取用户公开收藏夹概览
- `api.bilibili.com/x/polymer/web-dynamic/v1/opus/srv` — 获取用户动态

### 2.3 爱好分析方案

**数据源**（按可行性排序）：

| 数据源 | 可行性 | 数据量 | 分析价值 |
|---|---|---|---|
| 公开收藏夹 | ✅ 最可行 | 中（取决于收藏量） | 高（主动收藏 = 真喜欢） |
| 关注列表 | ✅ 可行 | 中 | 中（关注 = 持续兴趣） |
| 用户动态 | ✅ 可行 | 低 | 低（发动态不频繁） |
| 观看历史 | ⚠️ 需主人号登录 | 高（最多 100 条） | 最高（真实观看行为） |
| 主人号推荐流 | ⚠️ 需主人号登录 | 中 | 高（个性化推荐反映画像） |

**推荐方案**：**用公开收藏夹 + 关注列表做爱好分析**，不需要主人号登录，不会踢人。

**分析流程**：
```
1. 输入主人 UID/昵称
2. 调 B站 API 列公开收藏夹 → 遍历每个收藏夹的视频
3. 对每个视频取标题、标签、UP 主、分区
4. 聚合分析：
   - 分区分布（科技/游戏/知识/生活…）
   - UP 主偏好（最常收藏的 UP Top 10）
   - 标签词云（高频标签）
   - 时间分布（最近收藏 vs 早期收藏，看兴趣迁移）
5. 输出爱好画像：{ 分区偏好, UP 主偏好, 标签偏好, 活跃度 }
6. 将画像注入到：
   - 值班轮的搜索关键词（从爱好画像生成）
   - 桌宠对话风格（根据分区偏好调整语气）
   - 记忆插件（作为长期事实存入）
```

### 2.4 实现建议

#### 方案 A：在 dsh-bili-scroll 中新增工具（推荐）

在 `index.js` 中新增 3 个宿主工具：

| 工具 | 参数 | 功能 |
|---|---|---|
| `bili_user_favorites` | `uid` 或 `nickname` | 列用户公开收藏夹 + 每个夹的视频 |
| `bili_user_profile` | `uid` 或 `nickname` | 获取用户公开信息 + 关注列表 |
| `bili_analyze_hobby` | `uid` 或 `nickname` | 综合分析爱好，输出画像 JSON |

**实现要点**：
- 昵称→UID 解析复用已有 `lib/uid.mjs`
- API 调用复用已有凭证（值班号 SESSDATA）
- 分析逻辑在宿主侧做（不花模型 token），输出结构化画像
- 画像可存入 @dsh-cbw/memory 作为长期事实

**优点**：改动最小，复用已有基础设施
**缺点**：dsh-bili-scroll 职责膨胀

#### 方案 B：独立新插件 dsh-bili-profile

新建一个轻量插件，只做用户画像分析：

```
dsh-bili-profile/
  index.js    # 3 个工具：bili_user_favorites / bili_user_profile / bili_analyze_hobby
  lib/
    api.mjs   # B站 API 调用
    analyze.mjs # 爱好分析逻辑
```

**优点**：职责分离，不影响 dsh-bili-scroll
**缺点**：多一个插件要维护

#### 推荐：方案 A

理由：dsh-bili-scroll 已有 B站 API 调用基础设施（凭证管理、uid 解析、MCP 客户端），新增 3 个工具的边际成本远低于新建插件。

---

## 三、社区 B站插件综合评估

### 3.1 评估矩阵

| 插件 | 功能 | 与 dsh-bili-scroll 关系 | 整合价值 |
|---|---|---|---|
| **apiaoapiao/dsh-bili-statistics** ⭐ | **观看统计**：读观看历史 + 统计 + 模型写概览 + 报告 + DM/邮件通知 | 互补（statistics 读历史，scroll 做值班） | ⭐⭐⭐ 观看历史能力 |
| **bilihave/dsh-whale-panel** ⭐ | **策展浮窗**：兴趣学习 + 半衰期淡忘 + token 额度 + 挑片 + 评论 | 竞品（功能重叠度高，但 whale-panel 更成熟） | ⭐⭐ 兴趣学习 + 半衰期 |
| **QiuYeDx/dsh-bili-eyes** ⭐ | **看视频**：分镜图 + 台词 + 热评 + 弹幕 + 逛 B站 + 收件箱 + 守评论区 | 互补（eyes 看视频能力更强） | ⭐⭐ 分镜图、收件箱 |
| **Sacredbluedragon/dsh-bili-watch** | 看视频：字幕 + 转写 + 抽帧 OCR + 评论 + 弹幕 | 互补（类似 bili-eyes） | ⭐ 抽帧 OCR |
| **rentaoyan0628-collab/dsh-bili-danmaku-lite** | 直播弹幕：看/发/挂机听/自动陪聊 | 无重叠（直播 vs 点播） | ⭐ 直播弹幕 |
| **minedalang/dsh-dafeiyu-life** | 大肥鱼长期生活：自主刷 B站 + 互动 + 长期记忆 + 成长 | 竞品 + 有记忆维度 | ⭐ 长期记忆 + 成长 |
| **whiteguo233/OpenBiliClaw** | 自进化内容发现 Agent：B站 + 小红书 + 抖音 + YouTube… | 竞品（多平台 vs 单平台） | ⭐ 多平台思路 |
| **2tenthree/bilibili-download-skill** | 批量下载 B站视频（yt-dlp + ffmpeg） | 无重叠（下载 vs 值班） | — |
| **fromzero1501/dsh-video-downloader-v2** | 视频下载 | 无重叠 | — |
| **Britneycode/dsh-fish-soul** | 鱼人格 + 按人记忆 + B站/抖音私信 | 竞品（更偏人格 + 多平台） | ⭐ 按人记忆 |
| **dogeheng/dsh-omni** | QQ ↔ DSH bridge + B站卡片/贴纸 | 无重叠 | — |

### 3.2 重点插件分析

#### apiaoapiao/dsh-bili-statistics（⭐ 最值得借鉴）

**功能**：读取**自己的**观看历史，计算统计事实，让模型写概览 + 计划状态，生成 Markdown/HTML 报告，可通过 DM/邮件发送。

**关键能力**：
- **读取观看历史**（`api.bilibili.com/x/v2/history`）——dsh-bili-scroll 完全没有
- 统计：条目数、平均完成度、22 点后比例、自动播放链、与最近 14 次对比
- 互动：点赞、投币、收藏（窗口内）
- 报告：Markdown/HTML，按日/周/月/自定义
- 调度：定时触发，无需会话

**借鉴建议**：
1. **观看历史读取**：dsh-bili-scroll 可以借鉴其观看历史 API 调用，加到 `bili_user_profile` 工具中（但需要主人号登录，有踢人风险）
2. **统计报告**：dsh-bili-scroll 的 `out/` 日报可以借鉴其统计维度（完成度、时间分布等）
3. **定时调度**：dsh-bili-scroll 已有峰谷调度，不需要借鉴

#### bilihave/dsh-whale-panel（⭐ 兴趣学习值得借鉴）

**功能**：按概率学习兴趣、按半衰期淡忘、token 额度管理、挑片、评论。

**关键能力**：
- **兴趣画像是学的**：不用维护关键词，旧兴趣自动淡出
- **半衰期淡忘**：兴趣随时间衰减
- **token 额度**：花的不是"次数"而是 token 金额
- **三层评论闸门**：政治/政府/前沿科学硬禁区

**借鉴建议**：
1. **兴趣学习 + 半衰期**：dsh-bili-scroll 的 `keywords` 是死配置，可以借鉴 whale-panel 的兴趣学习机制——从值班轮挑的视频中自动提取兴趣词，按半衰期淡忘。这与 @dsh-cbw/memory 的半衰期机制异曲同工。
2. **token 额度**：dsh-bili-scroll 用 `perDay`（每天几条），可以借鉴 token 额度思路——但这对桌宠场景可能过重。
3. **评论闸门**：dsh-bili-scroll 已有语感闸门 + autoComment 闸门，可以借鉴三层硬禁区（政治/政府/前沿）。

#### QiuYeDx/dsh-bili-eyes（⭐ 分镜图 + 收件箱值得借鉴）

**功能**：给模型一个 B站链接就能"看"视频——分镜图 + 台词 + 热评 + 弹幕 + 逛 B站 + 收件箱。

**关键能力**：
- **分镜图**：每张 6~16 格，按剪辑节奏分格，约 384 token/张
- **自己逛**：插件按时间表自己逛，把好东西推荐给你
- **收件箱**：后台看未读数，回复/@/私信自动处理
- **守评论区**：盯着主人投稿的评论区

**借鉴建议**：
1. **分镜图**：dsh-bili-scroll 有 `bili_frames`（单帧），但 bili-eyes 的分镜图（多格拼一张）token 效率更高。可以借鉴其分镜拼接逻辑。
2. **收件箱自动处理**：dsh-bili-scroll 有 `dmWatch`（私信监听），但 bili-eyes 的自动处理（回复/@/私信分类处理）更完善。
3. **自己逛**：dsh-bili-scroll 的值班轮已经是"自己逛"，不需要借鉴。

---

## 四、综合建议

### 4.1 短期（与固定会话方案一起做）

1. **固定会话**（§六方案 A）：先解决值班轮无上下文的问题
2. **收藏夹访问**：在 dsh-bili-scroll 新增 `bili_user_favorites` 工具，用值班号登录访问主人公开收藏夹
3. **爱好分析**：新增 `bili_analyze_hobby` 工具，从收藏夹 + 关注列表推断爱好画像
4. **画像注入记忆**：将爱好画像作为长期事实存入 @dsh-cbw/memory

### 4.2 中期（提升值班质量）

5. **兴趣学习 + 半衰期**（借鉴 bilihave/dsh-whale-panel）：从值班轮挑的视频中自动提取兴趣词，按半衰期淡忘，替代死配置 `keywords`
6. **分镜图**（借鉴 QiuYeDx/dsh-bili-eyes）：用多格拼图替代单帧，token 效率更高
7. **评论三层闸门**（借鉴 bilihave/dsh-whale-panel）：政治/政府/前沿科学硬禁区
8. **观看统计报告**（借鉴 apiaoapiao/dsh-bili-statistics）：在日报中加入统计维度（完成度、时间分布等）

### 4.3 长期（可选）

9. **观看历史**（借鉴 apiaoapiao/dsh-bili-statistics）：需要主人号登录，有踢人风险。只在主人明确同意 + 深夜值班时跑。
10. **直播弹幕**（借鉴 rentaoyan0628-collab/dsh-bili-danmaku-lite）：完全不同的场景，看需求
11. **多平台**（借鉴 whiteguo233/OpenBiliClaw）：B站 + 小红书 + 抖音，看需求

### 4.4 不建议做的

| 功能 | 原因 |
|---|---|
| 用主人号登录看观看历史 | 踢人下线，用户体验差 |
| 新建独立插件 | dsh-bili-scroll 已有基础设施，边际成本低 |
| 整合 bili-eyes 的全部功能 | 功能重叠太多，挑有价值的借鉴即可 |
| 多平台支持 | 偏离 dsh-bili-scroll 的定位（B站值班） |

---

## 五、爱好分析功能详细设计

### 5.1 工具定义

```
bili_analyze_hobby(uid?: number, nickname?: string) → {
  uid: number,
  nickname: string,
  favorites: {
    folders: [{ id, name, count, cover }],
    totalVideos: number,
    topCategories: [{ category, count, ratio }],
    topUploaders: [{ uid, name, count, ratio }],
    topTags: [{ tag, count, ratio }],
    timeDistribution: [{ month, count }],
  },
  following: {
    count: number,
    topCategories: [...],
  },
  hobbyProfile: {
    primaryInterests: string[],    // 主要兴趣分区
    secondaryInterests: string[],  // 次要兴趣分区
    preferredUploaders: string[],  // 偏好 UP 主
    tags: string[],                // 标签词云
    activityLevel: 'high'|'medium'|'low',
    interestShift: 'stable'|'shifting'|'new',  // 兴趣迁移
  },
}
```

### 5.2 实现步骤

```
1. 昵称→UID（复用 lib/uid.mjs）
2. 调 /x/space/fav/box 列公开收藏夹
3. 遍历每个收藏夹调 /x/v3/fav/resource/list 取视频
4. 对每个视频取 title, tag, upper_name, tid（分区）
5. 聚合统计：
   - 分区频次 → topCategories
   - UP 主频次 → topUploaders
   - 标签频次 → topTags
   - 收藏时间 → timeDistribution
6. 调 /x/space/acc/info 取关注数
7. 生成 hobbyProfile：
   - primaryInterests = topCategories 前 3
   - secondaryInterests = topCategories 4-6
   - activityLevel = totalVideos > 200 ? 'high' : > 50 ? 'medium' : 'low'
   - interestShift = 最近 3 个月 vs 之前的分区分布对比
8. 返回结构化画像
```

### 5.3 画像注入记忆

将爱好画像存入 @dsh-cbw/memory 作为长期事实：

```json
{
  "content": "主人B站爱好：主要兴趣=科技(35%)、游戏(20%)、知识(15%)；偏好UP主=林亦、影视飓风、极客湾；活跃度=高",
  "importance": "critical",
  "tags": ["bilibili", "hobby", "user_profile"],
  "source": "user_explicit"
}
```

值班轮搜索时，从记忆中取出爱好画像，生成关键词：
```
爱好画像 → primaryInterests + preferredUploaders → 搜索关键词
```

---

## 六、固定会话方案（原 task2 整合）

> 原 task2（`docs/task2-bili-scroll-fixed-session.md`）已整合至此。
> 目标：让 dsh-bili-scroll 在固定对话中运行，有上下文，更好留存记忆，不让对话工作区混乱。

### 6.1 当前会话机制根因

值班轮通过 `child_process.spawn` 起新 dsh CLI 进程（`index.js:1600-1632`）：

```js
spawn('dsh', ['-p', 'bili-duty', '--print', prompt], { cwd: pluginHome })
```

- **纯 CLI 一次性模式**：prompt 作为命令行参数传入，进程结束即会话结束
- **非 API 复用会话**：不调用 webapi，无 sessionId 复用
- **每轮独立会话**：无上下文延续

跨轮记忆靠三个文件：`seen.md`（判重）、`digest/`（月归档）、`out/`（日报）。文件记忆无法提供对话上下文，模型每轮"失忆"。

### 6.2 四个候选方案

| 方案 | 描述 | 上下文 | 记忆 | 改动量 | 风险 |
|------|------|--------|------|--------|------|
| **A** 固定会话复用 sessionId | 首次建会话，后续续写 | ✅ 完整 | ✅ remember 持久化 | 中 | ⚠️ 会话无限增长，需 compaction |
| B 固定工作区+每天新会话+注入记忆 | 每天新会话，systemPrompt 含昨日摘要 | ⚠️ 仅当日 | ⚠️ 需手动注入 | 中 | 低 |
| C 固定会话+超阈值归档换新 | 会话超限时归档+摘要+新建 | ✅ 强 | ✅ | 高 | 中 |
| D CLI 不变仅加 workspace 归组 | spawn 时加 --workspace | ❌ | ❌ | 极小 | 极低 |

### 6.3 推荐：方案 A（固定会话复用 sessionId）

```
首次：POST /sessions { sessionId: "bili-duty-fixed", workspaceId: "bili-duty-ws", ... }
后续：POST /sessions/bili-duty-fixed/prompt-stream { prompt }
```

理由：改动量适中，完整对话上下文最符合目标，记忆插件在固定会话下自然生效。compaction 兜底：DSH 有会话 compaction 机制。若验证 compaction 在 bili-duty profile 下不生效，则退到方案 C。

### 6.4 待验证未知项

1. **bili-duty profile 下 compaction 是否自动生效**（关掉了多数工具，compaction 若依赖某工具可能被禁）
2. **会话级 permission 与 profile disabled 的叠加语义**（固定会话的权限是会话级还是 profile 级？）

### 6.5 风险与注意事项

| 风险 | 影响 | 缓解 |
|------|------|------|
| 固定会话无限增长导致 token 爆炸 | 高 | compaction 兜底 / 方案 C 归档 |
| bili-duty profile 下 compaction 不生效 | 高 | 验证后选方案 C |
| webapi 不可用时值班中断 | 中 | 保留 CLI fallback；webapi 重试 |
| 多值班轮并发写同一会话 | 中 | 加锁或每轮串行 |
| 权限泄露（固定会话权限叠加） | 高 | 验证叠加语义；保持 profile 级禁用 |

### 6.6 待讨论决策点

1. 固定 sessionId 命名（`bili-duty-fixed`？带日期/版本？）
2. workspaceId 命名与是否新建
3. compaction 不生效时的降级策略
4. 并发控制（多值班轮是否允许并发写同一会话？）
5. webapi 地址与认证（bili-scroll 插件如何获知 webapi 的 host:port？）
6. CLI fallback 保留与否

---

## 七、社区插件源地址

| 插件 | GitHub | npm |
|---|---|---|
| dsh-bili-statistics | apiaoapiao/dsh-bili-statistics | dsh-bili-statistics |
| dsh-whale-panel | bilihave/dsh-whale-panel | — |
| dsh-bili-eyes | QiuYeDx/dsh-bili-eyes | dsh-bili-eyes |
| dsh-bili-watch | Sacredbluedragon/dsh-bili-watch | — |
| dsh-bili-danmaku-lite | rentaoyan0628-collab/dsh-bili-danmaku-lite | — |
| dsh-dafeiyu-life | minedalang/dsh-dafeiyu-life | — |
| OpenBiliClaw | whiteguo233/OpenBiliClaw | — |
| bilibili-download-skill | 2tenthree/bilibili-download-skill | — |
| dsh-fish-soul | Britneycode/dsh-fish-soul | — |
| dsh-omni | dogeheng/dsh-omni | — |