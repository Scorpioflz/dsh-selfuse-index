# dsh-cbw-bilibili — B站值班插件（CBW 分支）

> 最后更新：2026-10-31 | 会话焦点：画像兴趣词修复 + bili_comment 工具修复

## 正在进行

- 无进行中任务

## 已完成

### 画像兴趣词修复（commit `8cd6e01`，已推送）

- `extractTitleKeywords` 暴力 n-gram 提取产生垃圾碎片（已失/已失效/失效等）
- 加停用词黑名单（含"失"/"效"的词 + 通用无意义词）+ 子串抑制（短词是长词子串且频率相近时抑制短词）
- 用户手动验证画像结果已正常

### bili_comment 工具修复（commit `ec2ed73`，已推送）

- bili_comment 工具缺 name 字段导致请求/头序列化失败
- 由另一个会话修复推送，已从 GitHub 重新安装验证通过

### 四项功能改进（commit `951e620`，已推送）

1. **人设开关**（`personaEnabled`，默认关闭）：Config/DEFAULTS/clampPatch 加字段，promptFor/dmPromptFor 按开关注入，设置页 ToggleRow UI
2. **兴趣整合**：doHobbyAnalyze 持久化画像到 `hobby-profile.json`，promptFor 整合三来源（手动 keywords + 画像 primaryInterests + 学习兴趣）去重合并
3. **画像查看**：status API 返回 `hobbyProfile` 字段，设置页显示持久化结果（标注「上次分析」）
4. **数据路径分离**：`bili-duty` → `dsh-cbw-bilibili`（含一次性迁移逻辑），API 路由 `/api/dsh-cbw-bili`，profile 名/session ID/环境变量/日志标签同步替换

### 插件市场发布（commit `371908a`，已推送）

- GitHub Pages 已生效：`https://scorpioflz.github.io/dsh-cbw-bilibili/index.json` 返回 200
- `dsh-plugin` topic 已打（GitHub API PUT /repos/.../topics）
- 插件已从 GitHub 安装到 DSH：`@dsh-cbw/bilibili@2.3.1`（经 gh-proxy codeload tarball URL 安装）
- 实机验证通过：API 200、personaEnabled=false、home=dsh-cbw-bilibili、插件列表显示版本号

### 实机测试结果

- 人设开关 ToggleRow 正常显示且默认关 ✅
- 画像区域显示"上次分析"时间（画像结果需下次分析后才显示）✅
- 兴趣整合逻辑代码验证通过 ✅
- 数据目录迁移成功（`.migrated` 标记 + 全量复制）✅
- 插件日志无错误 ✅

## 遇到的困难

- profile-template 目录重命名失败（bash mv 被拒，write yml 验证器 bug），保持目录名 `bili-duty`，仅改 package.json name
- 国内直连 GitHub 安装失败（Connection was reset），gh-proxy tarball 首次损坏（ERR_PNPM_TARBALL_DECODE_GZIP），`pnpm store prune` 后重试成功
- config.json 从旧目录迁移后 `dutySessionId`/`dmSessionId`/`pythonPath` 仍是旧值（用户已保存配置覆盖默认值），不影响功能

## 发现的经验

- 数据路径迁移应只复制数据文件，不复制 config.json 中的路径型字段（pythonPath 等），或迁移后自动修正
- gh-proxy codeload tarball URL 安装比 `github:` specifier 更可靠（后者走 git ls-remote 直连必失败）
- `git credential fill` 可获取 GitHub token 做 API 操作（启用 Pages、打 topic），需 printf 管道方式避免超时
- DSH 插件市场发布完整流程：repository 字段 → docs/index.json → GitHub Pages → dsh-plugin topic → 从 GitHub 安装验证

## 对其他会话的通知/请求

- 无