# dsh-cbw-bilibili — DSH B站值班插件

> 本分片由 bilibili 插件开发会话维护。更新本插件时改本文件，不碰根项目 README 主体。

## 基本信息

- **本地路径**：`D:\DSH-Dev\dsh-cbw-bilibili`（独立仓库）
- **仓库**：[Scorpioflz/dsh-cbw-bilibili](https://github.com/Scorpioflz/dsh-cbw-bilibili)
- **npm 包名**：`@dsh-cbw/bilibili`
- **许可证**：MIT（双版权：c1overzz + Scorpioflz）
- **派生自**：[c1overzz/dsh-bili-scroll](https://github.com/c1overzz/dsh-bili-scroll) v2.3.1（commit `a093f55`）

## 定位

Fork 自 dsh-bili-scroll，自研改进：固定会话延续 + 主人画像分析 + 兴趣学习 + 分镜图 + 评论闸门 + 观看统计。

## 派生关系

派生自 [c1overzz/dsh-bili-scroll](https://github.com/c1overzz/dsh-bili-scroll) v2.3.1，继承 `index.js`/`client.js`/`lib/`/`prompts`/`vendor`/`profile-template` 全部代码，在其上叠加改动。`upstream` remote 保留用于同步上游更新。

## 与上游差异

| 方面 | 上游 | 本 fork |
|---|---|---|
| 值班会话 | 一次性 CLI spawn，无上下文 | 固定 sessionId 复用（CLI `--session-id`），固定会话下跳过归档 |
| 主人识别 | mentionName（昵称单个）+ dmUid | masterUid（UID）+ mentionNames[]（昵称）+ dmRecipientUids[]（UID） |
| 爱好分析 | 无 | bili_user_favorites / bili_user_profile / bili_analyze_hobby |
| 搜索关键词 | 死配置 keywords[] | 自动学习兴趣词 + 半衰期淡忘（learned-interests.json） |
| 帧图 | 单帧 bili_frames | 分镜多格 bili_storyboard（6 帧一次） |
| 评论闸门 | 语感 + autoComment | + 三层硬禁区（政治/政府/前沿，force 不可越过） |
| 报告 | full/brief/off | + 观看统计段（完成度/时间分布/深夜比例）+ 收件箱段（回复/@/点赞分类） |

## 借鉴源

| 项目 | 借鉴内容 |
|---|---|
| [apiaoapiao/dsh-bili-statistics](https://github.com/apiaoapiao/dsh-bili-statistics) | 观看历史 API、统计维度 |
| [bilihave/dsh-whale-panel](https://github.com/bilihave/dsh-whale-panel) | 兴趣学习+半衰期、评论三层闸门 |
| [QiuYeDx/dsh-bili-eyes](https://github.com/QiuYeDx/dsh-bili-eyes) | 分镜多格拼图、收件箱分类 |
| [Yuuyuko-uu/dsh-fish-memory](https://github.com/Yuuyuko-uu/dsh-fish-memory) | 半衰期打分公式思路 |

## 功能依赖

- **[dsh-web-service](https://github.com/toddpan/dsh-webapi)** — P1 爱好分析工具的 REST/SSE API（P0 固定会话用 CLI `--session-id`，不依赖 web-service）
- **[@dsh-cbw/memory](https://github.com/Scorpioflz/dsh-cbw-memory)** — 爱好画像和兴趣词存储（可选但推荐）

## 新增 Config 字段

| 字段 | 默认 | 说明 |
|---|---|---|
| `masterUid` | `0` | 主人 B站 UID |
| `mentionNames` | `[]` | 评论 @ 昵称清单（可多个） |
| `dmRecipientUids` | `[]` | 私信收件人 UID 清单（可多个） |
| `fixedSession` | `false` | 固定会话开关 |
| `dutySessionId` | `''` | 值班固定会话 ID（传给 dsh CLI `--session-id`） |
| `dmSessionId` | `''` | 私信固定会话 ID |
| `webapiBase` | `''` | web-service 地址（P1 爱好分析工具用） |
| `webapiKey` | `''` | API Key |
| `hobbyRefreshDays` | `30` | 画像刷新周期（天） |
| `hobbyMaxVideos` | `500` | 单次分析最多视频数 |
| `hobbyLastRefresh` | `0` | 上次分析时间戳（自动更新） |
| `interestLearnEnabled` | `true` | 兴趣学习开关（从值班轮提取关键词+半衰期淡忘） |
| `interestHalfLifeDays` | `14` | 兴趣词半衰期（天） |
| `commentHardGate` | `true` | 评论三层硬禁区开关（政治/政府/前沿） |
| `watchedStatsEnabled` | `true` | 观看统计开关（日报里附加完成度/时间分布） |
| `watchedStatsDays` | `7` | 统计回看天数（1–30） |
| `inboxScanEnabled` | `false` | 收件箱扫描开关（分类回复/@/点赞通知） |
| `inboxScanPerRound` | `5` | 每轮最多处理几条收件箱通知（1–20） |

## 实施计划

| 阶段 | 内容 | 状态 |
|---|---|---|
| P0 | 固定会话 + 主人识别拆分 | ✅ 已完成（commit `681c17d`） |
| P1 | 爱好分析 + 画像 + 刷新周期 | ✅ 已完成（commit `19ca8cf`） |
| P2 | 兴趣学习+半衰期、分镜图、评论闸门 | ✅ 已完成（commit `4539076`） |
| P3 | 观看统计报告、收件箱分类 | ✅ 已完成（commit `9d8aa4a`） |

## 方案文档

- `docs/proposal-bilibili-integration.md` — 完整方案（§二爱好分析、§五详细设计、§六固定会话）