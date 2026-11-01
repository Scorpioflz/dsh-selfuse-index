# dsh-cbw-bilibili — B站值班插件（CBW 分支）

> 最后更新：2026-11-01 | 会话焦点：无进行中任务

## 正在进行

- 无进行中任务

## 已完成

### attachSession 关联工作区修复（commit `b835a64`，v2.3.9，已推送+安装+验证通过）

- **问题**：v2.3.8 用 `insertSessionBefore` 关联新建 session 到工作区，报 `the session is not accounted`——该方法只能移动已 accounted 的 session 顺序，新 session 不在 registry 里直接拒绝
- **根因**：`insertSessionBefore`（dsh-workspace/lib/index.js:130）第一行就检查 `record.sessionIds.includes(sessionId)`，不在就 throw。正确方法是 `attachSession`（line 111-129）：读 session header 验证 cwd 匹配 workspace path → `rememberSessionPath` → 加入 sessionIds
- **修复**：index.js exit handler 里 `insertSessionBefore(newId)` → `attachSession(newId)`
- **验证**：config.json sessionId=`session-adeeab89-...`，workspace.json「大肥鱼池塘」sessionIds[0] 同一 session，updatedAt 2026-11-01T06:04:39 ✓
- **README 更新**：双语 README 已更新自动会话管理说明（commit `171ea5d`，待网络恢复后推送）

### 工作区下拉选择器（commit `d1f5f17`，v2.3.6，已推送+安装）

- host 加 `GET /api/dsh-cbw-bili/workspaces` 路由，返回 `workspaceRegistry.list()`
- client 工作区从文本框改为 `<select>`，选项：「无工作区（插件家）」+ 所有已登记工作区

### 崩溃修复 discoverDutySession is not defined（v2.3.7，已推送+安装）

- v2.3.5 引入 `discoverDutySession` 函数名但代码里只有 `discoverDmSession`，改成 `discoverDmSession`（通用 session 发现逻辑）

### insertSessionBefore 关联工作区（v2.3.8，已推送+安装，但失败）

- 尝试用 `insertSessionBefore` 关联新建 session → 报 `the session is not accounted` → v2.3.9 修复

### 自动会话管理 - 去掉 session ID 录入（commit `c39bc17`，v2.3.5，已推送+安装）

- **问题**：one-shot runner 不 compose 任何 agent preset（`assertAdoptable` 检查 `preset !== void 0` 就拒绝）。web UI 建的对话带 "standard" preset → one-shot runner 拒绝
- **解法**：合并 `fixedSession`/`dutySessionId`/`dmSessionId` → 内部 `sessionId`。第一次不传 `--session-id` 让 one-shot runner 自动创建无 preset session，跑完 `discoverDutySession` 捕获新 ID 存 config，之后固定复用。值班轮 + 私信回复共用一个 session
- **session 失效处理**：exit handler 检测 stderr 含 "does not exist" 或 "does not compose" → 清 `cfg.sessionId`，下次自动新建（值班轮）/ 即时重试（私信回复）
- **设置页**：去掉固定会话开关 + 两个 session ID 输入框，加「会话工作区」输入框（可填桌宠工作区路径共享记忆）
- **session 创建后不能改 cwd**：`assertAdoptable` 检查 `header.cwd !== cwd` 拒绝。要在创建时就用对的 cwd → 通过 `cfg.workspace` 配置

### 私信监听日志误报 + 值班会话不存在提醒（commit `3547d3d`，v2.3.4，已推送+安装）

- **日志误报 bug**：`dmTick` 里判断"是否只回登录账号自己"用 `cfg.dmOwnerUid`（旧字段=0），但 `dmOwnerUid()` 函数实际用 `cfg.masterUid`（=9833388）⇒ owner 算对了、日志每分钟误刷警告。改成检查 `owner === dmCred.dedeuserid`（owner 是否真的回退到登录账号自己）
- **值班会话不存在提醒**：DSH CLI 遇到不存在的 session-id 会 code=1 退出（不自动新建）。按用户要求：不自动新建（避免丢上下文），而是在 exit handler 检测 stderr 含 "does not exist" 时打醒目提示，让用户去 DSH 侧栏新建对话、填 session ID 到配置
- **git push 代理 407 问题**：git 走了某个透明代理（user `08df1844-...`），环境变量/git config/WinHTTP/IE 代理都没配但仍然 407。解法：`no_proxy="*" NO_PROXY="*" git push` 强制绕过

### 合入上游 dsh-bili-scroll 3 commits（commit `d710fa2`，v2.3.3，已推送+安装）

| 上游 commit | 修复 | 改动文件 |
|------------|------|---------|
| `aadcdf7` | 自动收藏连续四天全失败（`FavoriteList` 参数错位 → 改用 `Video.set_favorite`） | `lib/favops.py` |
| `398e472` #150 | @ 昵称空格修复（B站只认紧挨着的 @） | `mcp_server.py`（`_normalize_mention`）+ `tools/check-mention.py` |
| `398e472` #162 | 私信 BV 号记录（让筛选能认出私信投递） | `mcp_server.py`（`dm-deliveries.jsonl`）+ `index.js`（`BILI_DUTY_RUN_DAY` + `dmDelivered`） |

### UP 主偏好时间权重（commit `5e6890c`，已推送+验证通过）

- 问题：`preferredUploaders` 原按收藏总数纯计数排序，凉风Kaze(24个)等历史收藏多的 UP 排前面，即使最近没收藏他们的视频
- 改动：`aggregateFavorites` 加时间衰减权重（`timeWeight` 累加），新增 `rawCount`/`lastFavDaysAgo`，画像输出 `preferredUploaderDetails`
- client.js 显示加时间标注：`凉风Kaze(3天前)、xxx(2月前)、yyy(2年前)`
- 验证结果：凉风Kaze 完全跌出 top 10，是个佑伊从第3降到第8（443天前最后一次收藏）；新冒出小芙ProMax(94天前)、穆小泠Official(32天前)等近期活跃 UP

### 画像深度增强（commit `1862664`，已推送）

- **时间衰减权重**：半衰期模型 `0.5^((now-fav_time)/halfLifeDays)`，默认 180 天，fav_time 缺失按 2020.7.1 统一计算
- **视频 Tag 采集**：对 top 50 最近视频调 `bili_video_info` 获取 tags（权重 ×3），需用 `get_tags()` API（`get_info()` 的 tag 字段为空）
- **UP 主签名词**：对 top 10 UP 主调 `bili_user_info` 获取 sign，n-gram 提取（权重 ×0.5）
- **三来源合并**：`mergeInterests` 去重 + 子串抑制，tag 词优先（虚拟主播/vup/翻唱等）
- **新增配置项**：`hobbyTimeHalfLifeDays`(180) / `hobbyDeepAnalyze`(true) / `hobbyDeepSampleSize`(50)
- **修复**：`bili_favorite_content` 加返回 `upper_mid`（UP 主 UID），`aggregateFavorites` 保存 `mid`
- 验证通过：tagInterests=["虚拟主播","vup","搞笑","全能音乐挑战赛","虚拟UP主","翻唱总动员","治愈","DJ","翻唱","古风dj"]

### 画像兴趣词修复（commit `8cd6e01`，已推送）

- `extractTitleKeywords` 暴力 n-gram 提取产生垃圾碎片（已失/已失效/失效等）
- 加停用词黑名单（含"失"/"效"的词 + 通用无意义词）+ 子串抑制（短词是长词子串且频率相近时抑制短词）

### bili_comment 工具修复（commit `ec2ed73`，已推送）

- bili_comment 工具缺 name 字段导致请求/头序列化失败，由另一个会话修复

### 四项功能改进（commit `951e620`，已推送）

1. 人设开关（`personaEnabled`，默认关闭）
2. 兴趣整合（画像持久化 + promptFor 三来源合并）
3. 画像查看（设置页显示持久化结果）
4. 数据路径分离（`bili-duty` → `dsh-cbw-bilibili`）

### 插件市场发布（commit `371908a`，已推送）

- GitHub Pages + dsh-plugin topic + 从 GitHub 安装验证通过

## 遇到的困难

- B 站 `video.get_info()` 返回的 tag 字段为空，必须单独调 `get_tags()` API（耗费多轮调试定位）
- `bili_favorite_content` 不返回 UP 主 UID，需自己加 `upper_mid` 字段
- profile-template 目录重命名失败，保持目录名 `bili-duty`，仅改 package.json name
- gh-proxy tarball 首次损坏（ERR_PNPM_TARBALL_DECODE_GZIP），`pnpm store prune` 后重试成功

## 发现的经验

### DSH 插件开发通用经验（分享给其他会话）

- **时间衰减权重模型**适合任何"偏好随时间变化"的场景（兴趣词、UP 主偏好等）。半衰期 180 天效果良好：5 年前权重 ≈ 0.0009，近期 ≈ 1.0，自然区分当前偏好 vs 历史偏好
- **收藏时间才是兴趣的真实信号**，关注时间不是——用户可能 5 年前关注但最近还在看，只有最近还收藏这个 UP 的视频才说明仍感兴趣
- **深度采集要分批并发**（每批 10 个 Promise.allSettled），避免一次性打太多 API 被限流
- **多来源合并要设权重分层 + 子串抑制去重**：tag(×3) > 标题 n-gram(×1) > 签名(×0.5)，子串抑制避免"虚拟UP主"和"虚拟主播"重复
- **fav_time 缺失按 2020.7.1 统一计算**（B 站 2020.7 之前收藏时间信息可能已被清除）
- **n-gram 提取需停用词过滤**：CJK 2-4 字词会产生大量无意义碎片，需黑名单 + 子串抑制

### B 站 API 相关

- `video.get_info()` 的 `tag` 字段为空，必须单独调 `video.get_tags()` API 获取视频标签
- `bili_favorite_content` 返回的视频对象没有 UP 主 UID（只有 `author` 名字），需加 `upper_mid` 字段
- gh-proxy codeload tarball URL 安装比 `github:` specifier 更可靠（后者走 git ls-remote 直连必失败）
- `git credential fill` 可获取 GitHub token 做 API 操作（启用 Pages、打 topic）

### pnpm 插件安装缓存问题（重要！分享给所有 DSH 插件开发会话）

- **问题**：pnpm 用 tarball URL 作 cache key。用 `tar.gz/refs/heads/main` 安装时，推送后 URL 不变，pnpm 跳过下载（"Lockfile is up to date, resolution step is skipped"），装的还是旧代码
- **解法**：用 **commit hash** 替代 branch ref：`tar.gz/050952d` 而非 `tar.gz/refs/heads/main`。URL 变了 pnpm 就会重新下载/解压
- **bump package.json 版本号**也有帮助（pnpm 会识别版本变化），但关键是 **tarball URL 要变**
- **开发期快速验证**：可直接 `cp` 本地开发目录的 index.js/client.js 到安装目录 `~/.dsh/profiles/web/node_modules/@dsh-cbw/bilibili/`，绕过 pnpm（需重启 DSH）

### git push 透明代理 407 问题

- **现象**：`git push` 报 `CONNECT tunnel failed, response 407`，git 走了某个透明代理（Proxy auth user `08df1844-...`），但环境变量/git config/WinHTTP/IE 代理设置都没配。`curl github.com` 直连正常（200）
- **解法**：`no_proxy="*" NO_PROXY="*" git push origin main` 强制绕过代理直连
- **排查**：`GIT_CURL_VERBOSE=1 git push 2>&1 | grep -i proxy` 可看代理来源

## 对其他会话的通知/请求

- 无