# TMDB 缓存管理

MediaTidy 内置 TMDB 持久化缓存系统（SQLite 表 `tmdb_cache`），避免对同一影视反复请求 TMDB API。缓存采用 **LRU 淘汰策略**，当条目数超出上限时自动清除最久未访问的记录。

## 缓存配置

在「系统设置 → TMDB」中配置：

| 配置项 | 字段 | 默认值 | 说明 |
|--------|------|--------|------|
| **启用缓存** | `enabled` | `true` | 关闭后不再写入新缓存，但已有缓存仍可被读取 |
| **最大条目数** | `maxSize` | `5000` | 允许的最大缓存记录数（范围 100–200000），超出后自动 LRU 淘汰 |
| **FF 探测缓存** | `fileProbeCacheEnabled` | `true` | 按文件 SHA1 持久化整理阶段的 FFprobe 结果 |
| **FF 探测缓存上限** | `fileProbeCacheMaxSize` | `400000` | 本地 FF 探测缓存最大条目数（范围 100–400000） |
| **云端操作 QPS** | `cloudOperationQPS` | `12` | FF 阶段读取云盘元信息和 SHA1 时的全局 QPS 上限 |
| **云端并发数** | `cloudOperationInflight` | `4` | FF 阶段云端操作最大并发数 |

## 远程 FF 缓存

「系统设置 → TMDB / 缓存」里还可以配置远程 FF 缓存，用于把高成本的 FF 结果共享给多台 MediaTidy。

新版配置分为两套：

| 配置块 | 字段 | 说明 |
|--------|------|------|
| 整理远程 FF 缓存 | `organizeRemoteFFCache` | 缓存自动整理阶段的 FFprobe 结果 |
| 神医远程 FF 缓存 | `strmAssistantRemoteFFCache` | 缓存 STRM 神医读取到的 Emby 媒体源信息 |

每套远程配置都支持多节点、读取策略、上传策略、超时和上传开关。完整说明见 [FF 缓存服务](/features/ff-cache-server)。

---

## 缓存管理页面

进入「TMDB 缓存」页面，可以对缓存进行全面管理。

### 统计概览

页面顶部显示缓存统计信息：

- **缓存总数**：当前缓存的 TMDB 条目数量
- **已锁定数**：手动锁定、不会被自动淘汰的条目数
- **最大容量**：配置的 `maxSize` 值

### 搜索与筛选

- 按标题关键词搜索
- 按媒体类型筛选：全部 / 电影 / 剧集
- 分页浏览所有缓存条目

### 缓存操作

#### 编辑条目

手动修改缓存中的元数据，适用于 TMDB 数据不准确的情况：

- 中文标题 / 原始标题
- 年份
- 简介
- 海报路径 / 背景图路径
- 评分
- 类型标签
- IMDB ID
- 制片国家 / 原始语言

::: info 自动锁定
编辑后的条目会自动标记为**已锁定**，防止被 LRU 淘汰覆盖你的修改。
:::

#### 锁定 / 解锁

- **锁定**的条目不会被 LRU 淘汰，也不会被「清除全部」操作删除
- 可随时切换锁定状态

#### 从 TMDB 刷新

对单条缓存重新拉取 TMDB 最新数据。会覆盖本地修改（包括手动编辑的内容）。

::: warning 注意
刷新操作会覆盖你之前手动编辑的内容。如果需要保留自定义数据，请先确认是否真的需要刷新。
:::

#### 删除单条

删除指定的缓存记录。下次整理遇到该影视时会重新从 TMDB 获取。

#### 清除全部

一键删除所有**未锁定**的缓存条目。锁定条目不受影响。

---

## 缓存条目字段

每条缓存记录包含以下信息：

| 字段 | 说明 |
|------|------|
| `tmdbId` | TMDB ID |
| `mediaType` | `movie` 或 `tv` |
| `title` | 中文标题（取决于系统设置的 TMDB 语言） |
| `originalTitle` | 原始标题 |
| `year` | 年份 |
| `overview` | 简介 |
| `posterPath` | 海报图片路径 |
| `backdropPath` | 背景图路径 |
| `voteAverage` | TMDB 评分 |
| `genres` | 类型标签（JSON 数组，如 `["动作","科幻"]`） |
| `runtime` | 时长（分钟，仅电影有效） |
| `status` | 发行状态（如 Released / Ended / Returning Series） |
| `imdbId` | IMDB ID |
| `originCountry` | 制片国家（JSON 数组，如 `["US","GB"]`） |
| `originalLanguage` | 原始语言代码（如 `en`、`ja`） |
| `locked` | 是否锁定 |
| `accessedAt` | 最后访问时间（LRU 淘汰依据） |
| `createdAt` | 首次缓存时间 |
| `updatedAt` | 最后更新时间 |

---

## LRU 淘汰机制

当缓存条目数超过 `maxSize` 时，系统自动按 `accessedAt`（最后访问时间）排序，清除最久未被访问的记录。

**淘汰规则：**
- 仅淘汰**未锁定**的条目
- 每次写入新缓存时触发检查
- 锁定条目永远不会被自动淘汰

---

## 使用场景

### 修正 TMDB 中文标题

当 TMDB 返回的中文标题不准确时（常见于日本动漫、韩剧等）：

1. 在「TMDB 缓存」页面搜索该条目
2. 点击「编辑」修改为正确的中文标题
3. 条目自动锁定
4. 后续整理将使用你修改后的标题

### 大批量整理前的准备

大量整理会频繁查询 TMDB，建议：

- 适当提高 `maxSize`（如 10000–50000），减少因淘汰导致的重复 API 请求
- 整理完成后可恢复默认值

### 锁定重要条目

对于经常被整理引用的影视条目（如长期更新的剧集），建议锁定以确保缓存不被淘汰。

---

## API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/tmdb-cache` | GET | 分页列表查询（支持搜索、类型筛选） |
| `/api/tmdb-cache/stats` | GET | 获取缓存统计（总数、锁定数、最大容量） |
| `/api/tmdb-cache/config` | GET | 获取缓存配置 |
| `/api/tmdb-cache/config` | POST | 保存缓存配置 |
| `/api/tmdb-cache/:id` | PUT | 编辑单条缓存 |
| `/api/tmdb-cache/:id` | DELETE | 删除单条缓存 |
| `/api/tmdb-cache` | DELETE | 清除所有未锁定缓存 |
| `/api/tmdb-cache/:id/lock` | POST | 切换锁定状态 |
| `/api/tmdb-cache/:id/refresh` | POST | 从 TMDB 刷新数据 |
