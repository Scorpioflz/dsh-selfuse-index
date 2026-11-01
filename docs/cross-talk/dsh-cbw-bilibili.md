# dsh-cbw-bilibili — B站值班插件（CBW 分支）

> 最后更新：2026-11-01 | 会话焦点：无进行中任务

## 正在进行

- 无进行中任务

## 已完成

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

## 对其他会话的通知/请求

- 无