# 规则引擎

MediaTidy 的规则引擎包含三种规则：**分类规则**、**命名规则**、**质量评分规则**。每种规则均使用 YAML 格式配置，支持三层优先级合并：**本地 > 订阅源 > 内置**。

## 规则来源与优先级

每种规则有三个来源，按优先级从高到低：

| 来源 | 说明 | 优先级 |
|------|------|--------|
| **本地** | 在管理面板「规则引擎」页面直接编辑的 YAML | 最高 |
| **订阅源** | 从远程 URL 定期拉取的 YAML | 中 |
| **内置** | 系统自带的默认规则 | 最低 |

**合并逻辑：**
- **命名规则 / 质量规则**：按规则的 `name` 字段合并。同名规则高优先级覆盖低优先级，不同名的规则全部保留
- **分类规则**：按整体替换。如果本地有分类规则，则完全使用本地的；如果本地为空但订阅源有，则使用订阅源的；都没有则使用内置默认

---

## 分类规则

分类规则根据 TMDB 元数据（类型、语言、国家、关键词等）将媒体文件自动归类到不同的媒体库子目录。

### YAML 格式

```yaml
movie:
  目标路径:
    条件字段1: "值"
    条件字段2: "值"

tv:
  目标路径:
    条件字段1: "值"
```

顶层分为 `movie`（电影）和 `tv`（剧集）两个区块，每个区块下定义多条规则。规则**按定义顺序从上到下匹配**，命中第一条即停止。

### 匹配条件字段

| 字段 | 数据来源 | 说明 | 示例值 |
|------|----------|------|--------|
| `genre_ids` | TMDB 类型 ID | 内容类型，支持多值逗号分隔 | `"16"` (动画)、`"16,10762"` |
| `original_language` | TMDB 原始语言 | ISO 639-1 语言代码 | `"zh"`, `"ja,ko"` |
| `origin_country` | TMDB 制作国家（TV） | ISO 3166-1 国家代码 | `"CN,TW,HK"` |
| `production_countries` | TMDB 制作国家（通用） | 会同时匹配 origin_country | `"US,GB"` |
| `keywords` | TMDB 标题文本 | 标题包含关键词即匹配 | `"奥特曼,假面骑士"` |
| `include_keywords` | TMDB 标签关键词 | 匹配 TMDB 的 keyword 标签 | `"tokusatsu,superhero"` |
| `filename_keywords` | 原始文件名 | 文件名包含关键词即匹配 | `"REMUX,Atmos"` |
| `series_directors` | TMDB 导演 | 导演名称包含匹配 | `"宫崎骏"` |
| `series_actors` | TMDB 演员 | 演员名称包含匹配（始终可选） | `"成龙,李连杰"` |
| `vote_average` | TMDB 评分 | 评分范围 min-max | `"0.1-5.6"` |
| `year` / `release_year` | TMDB 年份 | 精确、范围或列表 | `"2020"`, `"2000-2020"`, `"2020-"` |
| `file_extension` | 文件后缀名 | 小写扩展名 | `"mkv,iso"` |
| `resolution` | 分辨率 | 从文件名或 ffprobe 获取 | `"2160p,1080p"` |
| `hdr` / `dynamic_range` | HDR 类型 | 从文件名或 ffprobe 获取 | `"Dolby Vision,HDR10"` |

### 条件语法详解

#### 基本语法：逗号 = OR

多个值用逗号分隔，满足任一即匹配（支持中英文逗号）：

```yaml
original_language: "zh,cn,bo,za"   # 中文 OR 藏语 OR 壮语
```

#### 排除语法：`-` 前缀

值前加 `-` 表示排除，如果匹配则整条规则失败：

```yaml
genre_ids: "16,-10762"    # 有动画(16) AND 没有儿童(10762)
original_language: "-zh"   # 不是中文
```

#### 必须语法：`+` 前缀（仅 genre_ids）

值前加 `+` 表示必须同时包含：

```yaml
genre_ids: "+16,+10762"   # 必须同时有动画(16) AND 儿童(10762)
```

#### 可选条件：`?` 前缀

字段名前加 `?` 表示该条件为可选。所有必须条件都满足 + 至少一个可选条件满足 = 匹配：

```yaml
电视剧/香港剧:
  ?include_keywords: "TVB,HK"   # 可选：TMDB 标签含 TVB 或 HK
  ?origin_country: "HK"          # 可选：制作国家为香港
  # 两个可选条件满足任一即可
```

#### 否定条件：`-` 字段前缀

字段名前加 `-` 或 `!` 表示整个条件取反：

```yaml
-origin_country: "CN"   # 制作国家不是中国
```

#### 空条件 = 保底规则

没有任何条件的规则是保底规则（catch-all），永远匹配：

```yaml
电视剧/未分类:
  # 无条件，兜底匹配所有未被上方规则命中的剧集
```

### 匹配逻辑总结

```
规则匹配 = 所有必须条件全部通过 AND (没有可选条件 OR 至少一个可选条件通过)
```

- 必须条件（无 `?` 前缀）：全部 AND 关系
- 可选条件（有 `?` 前缀）：OR 关系，至少一个通过
- `series_actors` / `series_keywords` 即使没有 `?` 前缀也自动视为可选

### 完整示例

```yaml
movie:
  # 优先级1：特摄电影（标题或TMDB标签匹配，至少一个）
  电影/特摄电影:
    ?keywords: "奥特曼,假面骑士,铠甲勇士,Power Rangers"
    ?include_keywords: "tokusatsu,ultraman"

  # 优先级2：动画电影
  电影/动画电影:
    genre_ids: "16"

  # 优先级3：纪录电影
  电影/纪录电影:
    genre_ids: "99"

  # 优先级4：华语电影
  电影/华语电影:
    original_language: "zh,cn"

  # 优先级5：日韩电影
  电影/日韩电影:
    original_language: "ja,ko"

  # 优先级6：外语电影（兜底，排除已分类语言）
  电影/外语电影:
    original_language: "-cn,-zh,-ja,-ko"

tv:
  # 优先级1：综艺
  电视剧/综艺:
    genre_ids: "10764,10767"

  # 优先级2：纪录片
  电视剧/纪录片:
    genre_ids: "99,-10762"

  # 优先级3：国漫（动画 + 中港台，排除儿童）
  动漫/国漫:
    genre_ids: "16,-10762"
    origin_country: "CN,TW,HK"

  # 优先级4：日番
  动漫/日番:
    genre_ids: "16,-10762"
    origin_country: "JP"

  # 优先级5：国产剧
  电视剧/国产剧:
    origin_country: "CN,TW"

  # 优先级6：日韩剧
  电视剧/日韩剧:
    origin_country: "KR,JP"

  # 优先级7：欧美剧
  电视剧/欧美剧:
    origin_country: "US,GB,FR,DE,ES,IT,CA"

  # 保底
  电视剧/未分类:
```

### TMDB 类型 ID 速查

| ID | 类型 | ID | 类型 |
|----|------|----|------|
| 16 | 动画 | 99 | 纪录 |
| 28 | 动作 | 12 | 冒险 |
| 35 | 喜剧 | 18 | 剧情 |
| 27 | 恐怖 | 53 | 惊悚 |
| 80 | 犯罪 | 878 | 科幻 |
| 14 | 奇幻 | 36 | 历史 |
| 10402 | 音乐 | 10749 | 爱情 |
| 10751 | 家庭 | 10752 | 战争 |
| 10762 | 儿童 | 10764 | 真人秀 |
| 10767 | 脱口秀 | 10770 | 电视电影 |

### 常用国家/语言代码

| 代码 | 国家/地区 | 代码 | 语言 |
|------|----------|------|------|
| CN | 中国大陆 | zh | 中文 |
| TW | 中国台湾 | ja | 日语 |
| HK | 中国香港 | ko | 韩语 |
| JP | 日本 | en | 英语 |
| KR | 韩国 | hi | 印地语 |
| US | 美国 | th | 泰语 |
| GB | 英国 | vi | 越南语 |

---

## 命名规则

命名规则定义整理后文件的**文件夹路径**和**文件名**格式。每条规则包含 `movie`（电影）和 `tv`（剧集）两套独立模板。

### YAML 格式

<div v-pre>

```yaml
naming:
  - name: 规则显示名称
    id: 唯一标识符
    movie:
      folder: "{{title}} ({{year}}) [tmdbid-{{tmdbid}}]"
      file: "{{title}} ({{year}}).{{fileExt}}"
    tv:
      folder: "{{title}} ({{year}}) [tmdbid-{{tmdbid}}]/Season {{season02}}"
      file: "{{title}} - {{seasonEpisode}}.{{fileExt}}"
```

</div>

- `folder`：文件夹路径模板，用 `/` 分隔多级目录
- `file`：文件名模板（含扩展名）

### 模板变量完整列表

<div v-pre>

**基本信息：**

| 变量 | 说明 | 示例 |
|------|------|------|
| `{{title}}` | TMDB 中文标题 | 流浪地球 |
| `{{originalTitle}}` | TMDB 原始标题 | The Wandering Earth |
| `{{tmdbid}}` | TMDB ID | 475132 |
| `{{year}}` | 年份 | 2019 |
| `{{mediaType}}` | 媒体类型 | movie / tv |
| `{{fileExt}}` | 文件扩展名（不含点） | mkv |

**季集信息（仅剧集有效）：**

| 变量 | 说明 | 示例 |
|------|------|------|
| `{{season}}` | 季号 | 1 |
| `{{season02}}` | 季号两位补零 | 01 |
| `{{episode}}` | 集号 | 5 |
| `{{episode02}}` | 集号两位补零 | 05 |
| `{{seasonEpisode}}` | 组合格式 | S01E05 |
| `{{episodeTitle}}` | 集标题（从文件名解析） | The Pilot |

**文件名解析字段（从文件名自动提取）：**

| 变量 | 说明 | 示例 |
|------|------|------|
| `{{videoFormat}}` | 分辨率 | 2160p, 1080p |
| `{{videoCodec}}` | 视频编码 | HEVC, AVC, AV1 |
| `{{audioCodec}}` | 音频编码 | DTS-HD MA, TrueHD |
| `{{audioChannels}}` | 声道 | 7.1, 5.1 |
| `{{audioProfile}}` | 音频特性 | Atmos |
| `{{source}}` | 片源 | BluRay, WEB-DL, BluRay Remux |
| `{{edition}}` | 版本 | Director's Cut, Extended |
| `{{dynamicRange}}` | 动态范围 | HDR, HDR10+, DV |
| `{{releaseGroup}}` | 发布组 | FRDS, CtrlHD |
| `{{streamingService}}` | 流媒体来源 | Netflix, Disney+ |
| `{{colorDepth}}` | 色深 | 10bit |
| `{{frameRate}}` | 帧率 | 60fps |
| `{{videoProfile}}` | 视频特性 | Main 10 |
| `{{regionCode}}` | 区域码 | R1, A |

**ffprobe 探测字段（开启元数据提取后可用，优先级高于文件名解析）：**

| 变量 | 说明 | 示例 |
|------|------|------|
| `{{probeResolution}}` | 探测分辨率 | 2160p, 1080p |
| `{{probeCodec}}` | 探测视频编码 | H.265, H.264 |
| `{{probeAudio}}` | 探测音频编码 | Dolby TrueHD, DTS-HD MA |
| `{{probeHDR}}` | 探测 HDR 类型 | Dolby Vision P8, HDR10 |
| `{{probeSubtitle}}` | 探测字幕 | PGS 简体中文 |
| `{{probeColorDepth}}` | 探测色深 | 10-bit |
| `{{probeFrameRate}}` | 探测帧率 | 24fps |

**多版本标签：**

| 变量 | 说明 | 示例 |
|------|------|------|
| `{{versionTag}}` | 多版本版本标签 | 2160p DV, 1080p SDR |

</div>

::: tip 变量优先级
当同时开启 ffprobe 探测时，`videoFormat`、`videoCodec`、`audioCodec`、`dynamicRange` 四个变量会被 ffprobe 结果覆盖（因为 ffprobe 从实际视频流提取，比文件名解析更准确）。如果你想明确使用 ffprobe 数据，可以直接用 `probeXxx` 系列变量。
:::

::: info 命名与轨道筛选的关系
`probeAudio` 和 `probeSubtitle` 用于生成文件名中的音频、字幕摘要。`scoring.audio_codec` 和 `scoring.subtitle` 中的轨道条件用于筛选资源，不会改变命名模板，也不会调整媒体内部的轨道、顺序或默认标记。
:::

### 模板语法说明

- 文件夹路径用 `/` 分隔层级
- 缺失的变量会被替换为空字符串，系统会自动清理多余空格和连字符
- 文件名中的特殊字符 `< > : " | ? *` 会被自动过滤
- 连续的空格、连续的点号（`..`）会被自动合并

### 内置命名规则

<div v-pre>

| 规则名称 | ID | 电影文件名示例 |
|----------|----|----|
| **标准命名** | `standard` | `流浪地球 (2019).mkv` |
| **详细命名** | `detailed` | `流浪地球 (2019) - 2160p H.265 WEB-DL.mkv` |
| **完整命名** | `full` | `流浪地球 (2019) - 2160p H.265 DTS-HD MA HDR WEB-DL FRDS.mkv` |
| **原始标题** | `original-title` | `The Wandering Earth (2019).mkv` |
| **双语标题** | `bilingual` | `流浪地球 The Wandering Earth (2019).mkv` |
| **Plex 风格** | `plex` | `流浪地球 (2019).mkv`（文件夹用 `{tmdb-xxx}`） |
| **精简命名** | `minimal` | `流浪地球.mkv` |
| **发烧友** | `audiophile` | `流浪地球 (2019) - 2160p H.265 DTS-HD MA 7.1 HDR 10bit BluRay Remux FRDS.mkv` |
| **流媒体标注** | `streaming-tag` | `流浪地球 (2019) - 2160p Netflix H.265.mkv` |
| **探测数据** | `probe-based` | `流浪地球 (2019) - 2160p H.265 Dolby TrueHD Dolby Vision P8.mkv` |

所有内置规则的文件夹模板统一为 `{{title}} ({{year}}) [tmdbid-{{tmdbid}}]`（电影）和 `{{title}} ({{year}}) [tmdbid-{{tmdbid}}]/Season {{season02}}`（剧集），确保与 Emby/Jellyfin 兼容。

</div>

### 自定义命名规则示例

<div v-pre>

```yaml
naming:
  # 自定义：按语言分文件夹 + 带质量信息
  - name: 语言分类命名
    id: my-custom
    movie:
      folder: "{{title}} ({{year}}) [tmdbid-{{tmdbid}}]"
      file: "{{title}} ({{year}}) - {{videoFormat}} {{source}} {{videoCodec}} {{dynamicRange}}.{{fileExt}}"
    tv:
      folder: "{{title}} ({{year}}) [tmdbid-{{tmdbid}}]/Season {{season02}}"
      file: "{{title}} - {{seasonEpisode}} - {{videoFormat}} {{source}}.{{fileExt}}"
```

</div>

---

## 质量评分规则

质量评分规则在整理方案开启**洗版升级**后生效，同时用于首次入库候选筛选和后续洗版比较。系统先判断资源是否满足硬性条件，再计算总分；不合格资源不会因为分数高而替换合格资源。

在 `scoring.audio_codec` 和 `scoring.subtitle` 中，可以使用字符串或轨道条件对象设置 `priority`。字符串适合按音频、字幕摘要排序；轨道条件对象适合按具体轨道的语言、编码、声道、来源和标记筛选。两种写法可以单独使用，也可以放在同一个列表中。

### 处理顺序

1. 检查音轨、字幕轨的最少/最多数量。
2. 检查启用且 `required: true` 的音轨或字幕条件是否至少命中一个。
3. 任一硬条件失败，资源标记为不合格，并记录全部原因。
4. 两个资源都合格时，先比较总分。
5. 总分完全相同时，比较命中的 `priority` 等级。
6. 优先级也相同时，才使用 `preferred_tracks` 距离破同分。
7. 两个资源都不合格时保留现有资源；首次整理没有合格资源时跳过。

::: tip 关键区别
`required`、`min_tracks`、`max_tracks` 是资格条件；`weight` 和 `priority` 是评分条件；`preferred_tracks` 只负责同分破局。三者不要混为一谈。
:::

### 基本写法

除音轨和字幕轨条件外，各评分项都使用字符串 `priority` 列表。例如：

```yaml
resolution:
  enabled: true
  unknown_policy: zero
  weight: 20
  priority:
    - 2160p
    - 1080p
    - 720p
```

- `enabled: true`：启用该评分项。
- `unknown_policy`：该维度遇到未知值时的处理方式，只能填写 `ignore` 或 `zero`。省略时默认 `ignore`。
- `weight`：该项对总分的影响程度，可以使用小数或负数。
- `priority`：从上到下排列偏好，第一项得分最高，未命中得 0 分。
- 字符串匹配不区分大小写，并支持以空格或 `+` 分隔的前缀匹配。例如 `Dolby Vision` 可以匹配 `Dolby Vision P8`，`Remux` 可以匹配 `Remux+BluRay`。
- YAML 字段名是 `unknown_policy`，接口 JSON 中对应 `unknownPolicy`。旧规则不需要补写该字段，保存和序列化时也不会被强制扩写。

![评分规则 YAML 编辑示例](/screenshots/quality-rule-editor.png)

*进入“规则引擎 → 整理规则 → 评分规则”编辑本地 YAML。示例中分辨率和字幕使用 `zero`，视频编码保留默认的双方忽略方式。*

### 评分公式

```text
总分 = Σ（维度权重 × 维度位置分）
```

- `priority` 有 `N` 项时，第 1 项位置分为 `10`，第 2 项为 `10 × (N-1) / N`，最后一项为 `10 / N`，未命中为 `0`。
- `weight` 控制该维度对总分的影响。
- `file_size`、`bitrate`、`video_bitrate` 使用连续数值公式，不使用 `priority`。
- 负权重仍然可用，例如用负的 `file_size` 权重偏好较小文件。

例如 `priority: [2160p, 1080p, 720p]` 的位置分依次为 `10`、`6.67`、`3.33`；当 `weight: 20` 时，对应维度得分为 `200`、`133.33`、`66.67`。

### 缺少信息时到底怎么评分

> **没取到信息，不等于确认没有。未知值怎么参与比较由每个评分维度自己的 `unknown_policy` 决定。**

| `unknown_policy` | 行为 | 适用场景 |
|------------------|------|----------|
| `ignore` | 默认值。任一侧未知时，双方都跳过整个维度 | 只希望双方都有可靠信息时才比较 |
| `zero` | 维度继续参与；未知侧显示“未知”并记 0 分，已知侧正常评分 | 希望信息明确的一侧可以胜过未知侧 |

例如只希望分辨率已知的资源获得分数：

```yaml
resolution:
  enabled: true
  unknown_policy: zero
  weight: 25
  priority: [2160p, 1080p, 720p]
```

具体比较结果如下：

| 左侧 | 右侧 | `ignore` | `zero` |
|------|------|----------|--------|
| 已知 | 已知 | 双方正常评分 | 双方正常评分 |
| 已知 | 未知 | 双方跳过该维度 | 已知侧正常评分，未知侧 0 分 |
| 未知 | 未知 | 双方跳过该维度 | 显示 `0:0`，该维度不产生胜者 |
| 已知 | 确认不存在 | 双方正常参与，不存在侧 0 分 | 双方正常参与，不存在侧 0 分 |

`unknown_policy` 只处理“无法判断”的普通评分项。“确认不存在”始终是可比较的已知事实，不受该策略控制。

先看最容易理解的字幕例子：

| 实际情况 | 系统如何处理 |
|----------|--------------|
| 完整字幕清单里有字幕 | 可以确定有字幕，按字幕格式、语言等正常评分 |
| 完整字幕清单是 `subtitleTracks: []` | 可以确定没有字幕，字幕项正常参与，无字幕方为 0 分 |
| 没有运行 FF、FF 失败，或旧缓存没有 `subtitleTracks` | 无法判断有没有字幕，不把它当成无字幕；按字幕维度的 `unknown_policy` 处理 |

音轨使用完全相同的判断方式。完整清单为空表示“确定没有”，没有采集到清单则表示“无法判断”。

::: tip `source` 也使用未知值策略
文件名没有识别出片源时，`source` 现在属于“无法判断”：`ignore` 会让双方跳过片源维度，`zero` 会让未知侧记 0 分、已知侧正常评分。不要再把 `Unknown` 写进 `source.priority`；旧规则中的该条目会在加载时自动过滤，不会改写原始 YAML。
:::

其他评分项按下面的实际场景处理：

| 实际场景 | 系统如何处理 |
|----------|--------------|
| 文件名有分辨率，或 FF 取得了分辨率 | 可以确定分辨率，正常评分 |
| 文件名没有分辨率，而且没有成功取得完整 FF | 无法判断分辨率，按 `resolution.unknown_policy` 处理 |
| 文件名没有识别出片源 | 无法判断片源，按 `source.unknown_policy` 处理 |
| 完整 FF 确认没有有效视频 | 可以确定没有有效视频，分辨率按 0 分参与 |
| 文件名和 FF 都没有明确 HDR 标签 | 按产品规则视为 `SDR`，正常参与 HDR 评分 |
| 完整 FF 确认没有有效视频 | HDR 也按 0 分参与 |
| 视频编码、色深或帧率能从文件名或 FF 取得 | 可以确定，正常评分 |
| 视频编码、色深或帧率没有采集到 | 无法判断，按对应维度的 `unknown_policy` 处理 |
| 完整 FF 已采集，但确认没有对应视频信息 | 确定没有，对应项目按 0 分参与 |
| 完整音轨或字幕清单为空 | 确定没有音轨或字幕，对应项目按 0 分参与 |
| 旧缓存没有音轨或字幕清单 | 无法判断，按音轨或字幕维度的 `unknown_policy` 处理 |
| 文件大小、容器总码率或视频流码率取不到有效数值 | 无法判断，按对应数值维度的 `unknown_policy` 处理 |
| 文件确实没有扩展名 | 确定没有扩展名，容器格式按 0 分参与 |

#### 普通偏好和硬性条件的区别

- `priority` 和 `preferred_tracks` 是普通偏好。完整轨道清单未知时按该维度的 `unknown_policy` 处理。
- 在 `zero` 模式下，未知侧会得到显式 0 分，但不会伪装成“0 条轨道”，也不会生成虚假的优先级、轨数或目标轨数距离；已知侧仍使用真实轨道数据。
- `required`、`min_tracks`、`max_tracks` 是必须满足的硬性条件。轨道清单无法判断时，系统无法证明资源符合要求，因此该资源直接判为不合格。
- 清单明确为空时不是“无法判断”，而是用 0 条轨道正常验证硬性条件。

### 评分维度

| 维度 | YAML 键 | 数据来源 | 说明 |
|------|---------|----------|------|
| 分辨率 | `resolution` | 文件名 / ffprobe | 4320p、2160p、1080p 等 |
| 片源 | `source` | 文件名 | Remux、BluRay、WEB-DL 等 |
| 视频编码 | `video_codec` | 文件名 / ffprobe | AV1、H.265、H.264 等 |
| 音频编码/音轨 | `audio_codec` | 文件名 / ffprobe | 可按音频摘要或具体音轨条件匹配 |
| HDR | `hdr` | 文件名 / ffprobe | Dolby Vision、HDR10+、HDR10、SDR 等 |
| 色深 | `color_depth` | 文件名 / ffprobe | 12-bit、10-bit、8-bit |
| 帧率 | `frame_rate` | 文件名 / ffprobe | 120fps、60fps、24fps 等 |
| 字幕/字幕轨 | `subtitle` | ffprobe；轨道条件还可使用可靠关联外挂字幕 | 可按字幕摘要或具体字幕轨条件匹配 |
| 容器格式 | `file_extension` | 文件名 / ffprobe | mkv、mp4、ts 等 |
| 文件大小 | `file_size` | 文件属性 | 对数公式，约 50GB 后趋于饱和 |
| 容器总码率 | `bitrate` | 文件名 / ffprobe | 对数公式，越高分数越高 |
| 视频流码率 | `video_bitrate` | 文件名 / ffprobe | 仅使用视频流码率，不用容器码率冒充 |

### 各评分项怎么写

| YAML 键 | 常用 `priority` 值 | 使用说明 |
|----------|-------------------|----------|
| `resolution` | `[4320p, 2160p, 1080p, 720p]` | ffprobe 有结果时使用实际视频分辨率，否则使用文件名识别值 |
| `source` | `[Remux+UHD BluRay, Remux+BluRay, UHD BluRay, BluRay, WEB-DL, HDTV]` | 从文件名识别；无法识别时按 `source.unknown_policy` 处理 |
| `video_codec` | `[AV1, H.265, H.264, VP9]` | ffprobe 有结果时使用实际视频编码，否则使用文件名识别值 |
| `audio_codec` | `[DTS:X, TrueHD Dolby Atmos, DTS-HD MA, Dolby TrueHD, AAC]` | 字符串按音频摘要评分；需要限定语言、声道或标记时使用下方轨道条件 |
| `hdr` | `[Dolby Vision P7, Dolby Vision P8, Dolby Vision, HDR10+, HDR10, HLG, HDR, SDR]` | 一个文件识别到多个 HDR 值时，采用列表中得分最高的一项；未识别到 HDR 时按 `SDR` 匹配 |
| `color_depth` | `[12-bit, 10-bit, 8-bit]` | 可从文件名识别；开启元数据提取后优先使用实际视频流信息 |
| `frame_rate` | `[120fps, 60fps, 30fps, 25fps, 24fps]` | `23.976fps` 会按 `24fps` 参与评分；开启元数据提取后优先使用实际视频流信息 |
| `subtitle` | `[PGS 简体中文, ASS 简体中文, SRT 简体中文, PGS, ASS, SRT]` | 字符串按字幕摘要评分；需要限定语言、来源或标记时使用下方轨道条件 |
| `file_extension` | `[mkv, mp4, ts, m2ts]` | 填写不带点号的小写或大写扩展名均可 |

#### 片源中的 Remux

从文件名同时识别到 Remux 和片源时，`source` 使用组合值：

| 识别结果 | `source` 匹配值 |
|----------|-----------------|
| Remux + UHD BluRay | `Remux+UHD BluRay` |
| Remux + BluRay | `Remux+BluRay` |
| 只有 Remux | `Remux+BD` |
| 无法识别片源 | 未知，按 `source.unknown_policy` 处理 |

### 文件大小和码率

这三个评分项使用 `enabled`、`weight` 和可选的 `unknown_policy`，不要填写 `priority`：

```yaml
file_size:
  enabled: true
  weight: 5
bitrate:
  enabled: true
  weight: 10
video_bitrate:
  enabled: true
  unknown_policy: zero
  weight: 15
```

| YAML 键 | 取值方式 | 计分范围 |
|----------|----------|----------|
| `file_size` | 文件实际大小 | 小于 0.1GB 时为 0 分，约 50GB 达到最高位置分 10 |
| `bitrate` | ffprobe 的容器总码率；没有时可识别文件名中的 `16.8Mbps` | 小于 0.5Mbps 时为 0 分，约 100Mbps 达到最高位置分 10 |
| `video_bitrate` | ffprobe 的主视频流码率；没有时可识别文件名中的 `V16.8Mbps` | 小于 0.5Mbps 时为 0 分，约 100Mbps 达到最高位置分 10 |

`video_bitrate` 不会使用容器总码率代替。候选资源或现有资源无法取得有效数值时，该项视为未知：`ignore` 会让双方跳过该数值维度，`zero` 会让未知侧记 0 分、已知侧按实际数值评分。

当同一集存在多个旧版本时，每个新旧文件对会独立确定可比维度。新文件必须逐一胜过全部旧候选；系统不会拿使用不同维度集合算出的旧文件总分互相排名。

### 音轨和字幕轨公共字段

以下字段仅用于 `audio_codec` 和 `subtitle`：

| 字段 | 类型 | 作用 |
|------|------|------|
| `enabled` | boolean | 是否启用该评分维度 |
| `unknown_policy` | `ignore` / `zero` | 轨道清单未知时双方跳过，或未知侧记 0 分；默认 `ignore` |
| `required` | boolean | 至少一个 `priority` 条目必须命中，否则资源不合格 |
| `min_tracks` | integer | 全部可用轨道数量不得少于此值；`0` 表示不限制 |
| `max_tracks` | integer | 全部可用轨道数量不得超过此值；`0` 表示不限制 |
| `preferred_tracks` | integer | 理想轨道数量，只在总分和优先级相同时破同分 |
| `weight` | number | 该维度的评分权重 |
| `priority` | list | 有序的字符串或轨道条件列表 |

轨道数量口径：

- 音轨：视频文件内的全部音频流。
- 字幕轨：全部内封字幕流 + 可靠关联的外挂字幕文件。
- 未知语言、评论轨和听障轨也计入总数量。
- 外挂字幕按文件路径去重。

### 轨道条件的匹配规则

```yaml
priority:
  - languages: [zh-CN]
    source: any
    hearing_impaired: false
  - languages: [zh-TW, zh-HK]
    source: any
```

- 一个对象内的字段是 **AND**：必须由同一条轨道同时满足。
- `priority` 各条目之间是 **OR**：命中任意一项即可，越靠前等级越高。
- 同一资源有多条轨道命中时，只取最高等级的一条计分。
- 不能用 A 音轨的语言和 B 音轨的编码拼成一次命中。
- 布尔字段省略表示“不限制”；明确写 `false` 才表示“必须为否”。
- 字符串条目和对象条目可以混用，并共享同一套列表顺序。

### 音轨条件字段

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `languages` | string[] | 音轨语言 | `[zh, zh-CN, yue]` |
| `codecs` | string[] | 音频编码族 | `[Dolby TrueHD]`、`[DTS-HD MA]` |
| `profiles` | string[] | ffprobe 音频 Profile | `[DTS-HD MA]` |
| `min_channels` | integer | 最少声道数 | `8` = 至少 7.1 |
| `max_channels` | integer | 最多声道数 | `6` = 最多 5.1 |
| `atmos` | boolean | 是否为 Atmos | `true` |
| `default` | boolean | 是否为默认音轨 | `false` |
| `forced` | boolean | 是否为强制音轨 | `false` |
| `commentary` | boolean | 是否为评论音轨 | `false` |
| `hearing_impaired` | boolean | 是否为听障音轨 | `false` |
| `visual_impaired` | boolean | 是否为视觉障碍辅助音轨 | `false` |
| `original` | boolean | 是否标记为原声 | `true` |
| `dub` | boolean | 是否标记为配音 | `true` |

`Dolby TrueHD` 会匹配 ffprobe 输出的 `TrueHD Dolby Atmos 7.1` 编码族；是否必须为 Atmos 应由 `atmos: true` 单独约束。

### 字幕条件字段

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `languages` | string[] | 字幕语言 | `[zh, zh-CN, zh-TW, zh-HK]` |
| `formats` | string[] | 字幕格式 | `[PGS, ASS, SRT]` |
| `source` | string | `embedded`、`external` 或 `any` | `any` |
| `default` | boolean | 是否为默认字幕 | `false` |
| `forced` | boolean | 是否为强制字幕 | `false` |
| `commentary` | boolean | 是否为评论字幕 | `false` |
| `hearing_impaired` | boolean | 是否为听障字幕 | `false` |

### 语言代码识别

| 规则值 | 含义 | 常见别名/来源 |
|--------|------|---------------|
| `zh` | 泛中文，匹配任意 `zh-*` | `chi`、`zho`、`cmn`、`chinese`、`中文` |
| `zh-CN` | 简体中文 | `chs`、`zh-CHS`、`zh-Hans`、`zh-SG`、`Simplified`、简体中文、简中、简英 |
| `zh-TW` | 繁体中文 | `cht`、`zh-CHT`、`zh-Hant`、`zh-TW`、`Traditional`、繁体中文、繁中、繁英、Taiwan |
| `zh-HK` | 香港/澳门繁体中文 | `zh-HK`、`zh-MO`、`zh-Hant-HK`、Hong Kong、香港、澳门 |
| `yue` | 粤语 | `zh-yue`、`cantonese`、粤语、粵語、广东话、廣東話 |
| `en` | 英语 | `eng`、`english`、`en-US`、`en-GB` |
| `ja` | 日语 | `jpn`、`japanese`、日本語、日文 |
| `ko` | 韩语 | `kor`、`korean`、한국어、韩文、韓文 |
| `fr` / `de` / `es` / `pt` | 法语 / 德语 / 西班牙语 / 葡萄牙语 | `fra/fre`、`deu/ger`、`spa`、`por` 及其本地语言名称 |
| `ru` / `it` / `ar` | 俄语 / 意大利语 / 阿拉伯语 | `rus`、`ita`、`ara` 及其本地语言名称 |
| 其他二字代码 | 其他常见语言 | 同时兼容常见 ISO 639-2/3 三字码和 BCP-47 地区标签 |
| `und` | 无法识别语言 | language 标签和标题/文件名均无可靠标记 |

::: warning “中文”与“简体中文”不同
`chi`、`zho`、`cmn` 本身只能证明是泛中文。如果轨道标题还包含 `Simplified`、`简体` 或 `简中`，会识别为 `zh-CN`；包含 `Traditional`、`繁体` 或 `繁中`，会识别为 `zh-TW`。标题没有这些明确标记时仍为 `zh`。
:::

当语言标签是泛中文或为空时，系统会继续检查轨道标题。中文优先识别文字体系、地区和粤语；其他语言识别常见英文名称、本地语言名称以及二字/三字语言码。明确的语言标签不会被冲突标题覆盖；仍无法识别时使用 `und`。

常见结果：

| FFprobe language | 轨道标题 | 识别结果 |
|------------------|----------|----------|
| `chi` | `Simplified, Singapore` | `zh-CN` |
| `chi` | `Traditional, Hong Kong` | `zh-HK` |
| `chi` | `Traditional, Taiwan` | `zh-TW` |
| `chi` | `简体中文（国语）` | `zh-CN` |
| `chi` | `繁體中文（國語）` | `zh-TW` |
| `chi` | 无明确细分 | `zh` |
| `eng` | 任意标题 | `en` |
| 空 | `日本語` | `ja` |
| 空 | `Português (Brasil)` | `pt` |

规则中建议使用归一化后的值，例如 `languages: [zh-CN, zh-TW, en, ja, ko]`。除中文文字体系和地区外，普通 BCP-47 地区标签按基础语言比较，例如 `en-US`、`en-GB` 和 `eng` 都能匹配 `en`。

### 外挂字幕如何关联

外挂字幕只有在同目录并能可靠关联主视频时才计入。可靠情况包括：

- 完整媒体基名相同：`Movie.mkv` + `Movie.srt`。
- 在完整媒体基名后增加已知语言或字幕标记：`Movie.zh-CN.srt`、`Movie.chs.ass`、`Movie.en.forced.srt`。
- 剧集文件使用完整集文件基名：`Show.S01E03.mkv` + `Show.S01E03.zh-CN.ass`。

`Movie2.srt`、`MovieExtra.srt`、`Movie-edition.srt` 这类模糊前缀不会满足硬性字幕要求。

#### 外挂字幕没有语言标记

`Movie.srt` 能可靠确认“属于 Movie”，但不能确认字幕语言，因此：

- 会作为一条 `external` 字幕计入 `min_tracks`、`max_tracks` 和 `preferred_tracks`。
- 语言为 `und`。
- 不能满足 `languages: [zh-CN]` 或 `languages: [zh]`。
- 可以满足没有填写 `languages` 的条件，例如 `formats: [SRT]` + `source: external`。
- 系统不会读取字幕正文猜测语言，避免把英文字幕误判为中文字幕。

### 示例一：必须有任意中文字幕

最多 5 条字幕，理想 2 条；简体优先，其次繁体：

```yaml
subtitle:
  enabled: true
  required: true
  min_tracks: 1
  max_tracks: 5
  preferred_tracks: 2
  weight: 20
  priority:
    - languages: [zh-CN]
      source: any
      hearing_impaired: false
    - languages: [zh, zh-TW, zh-HK]
      source: any
      hearing_impaired: false
```

结果示例：

| 资源 | 结果 | 原因 |
|------|------|------|
| 内封 `zh-CN` ASS + 外挂英文 SRT | 合格 | 第一优先级命中，字幕共 2 条 |
| `Movie.chi.srt` | 合格 | `chi` 归一化为泛中文 `zh`，命中第二优先级 |
| `Movie.srt`，无语言标记 | 不合格 | 字幕存在但语言为 `und`，没有命中中文条件 |
| 8 条字幕且包含简中 | 不合格 | 超过 `max_tracks: 5`，即使中文条件命中也会拒绝 |

### 示例二：只接受简体中文字幕

```yaml
subtitle:
  enabled: true
  required: true
  weight: 20
  priority:
    - languages: [zh-CN]
      source: any
      hearing_impaired: false
```

`.zh-CN.srt`、`.chs.ass` 或标题标记为“简中”的内封字幕可以命中；`.chi.srt`、繁体字幕和无语言标记字幕不能命中。

### 示例三：必须有中文高规格音轨

最多 3 条音轨，理想 2 条；优先 TrueHD Atmos 7.1，其次 DTS-HD MA 5.1，最后接受中文立体声：

```yaml
audio_codec:
  enabled: true
  required: true
  min_tracks: 1
  max_tracks: 3
  preferred_tracks: 2
  weight: 20
  priority:
    - languages: [zh, zh-CN, yue]
      codecs: [Dolby TrueHD]
      min_channels: 8
      atmos: true
      commentary: false
    - languages: [zh, zh-CN, yue]
      codecs: [DTS-HD MA]
      min_channels: 6
      commentary: false
    - languages: [zh, zh-CN, yue]
      min_channels: 2
      commentary: false
```

注意：一条英文 TrueHD Atmos 音轨和另一条中文 AAC 音轨不能拼成第一项命中，因为语言、编码、声道和 Atmos 必须来自同一条音轨。

### 示例四：只限制轨道数量

如果不要求特定语言或编码，只是不想要轨道太多，可以只配置数量：

```yaml
audio_codec:
  enabled: true
  max_tracks: 3
  preferred_tracks: 2
  weight: 20
  priority:
    - Dolby TrueHD
    - DTS-HD MA
    - AAC

subtitle:
  enabled: true
  max_tracks: 5
  preferred_tracks: 2
  weight: 10
  priority:
    - PGS 简体中文
    - ASS 简体中文
    - SRT 简体中文
```

这里 `max_tracks` 是硬限制；`preferred_tracks` 不会淘汰资源，也不会改变显示总分。

### 示例五：混合使用字符串和轨道条件

```yaml
audio_codec:
  enabled: true
  weight: 20
  priority:
    - Dolby TrueHD
    - languages: [zh-CN]
      codecs: [DTS-HD MA]
      min_channels: 6
    - AAC
```

三个条目按列出的顺序共同参与优先级评分：字符串匹配音频编码摘要，条件对象匹配满足全部条件的具体音轨。

### 完整可复制示例

下面是一条同时要求中文字幕和中文音轨、并限制轨道数量的完整质量规则：

```yaml
quality:
  - name: 中文轨道收藏
    id: chinese-tracks
    scoring:
      resolution:
        enabled: true
        weight: 25
        priority: [2160p, 1080p, 720p]

      video_codec:
        enabled: true
        weight: 10
        priority: [AV1, H.265, H.264]

      audio_codec:
        enabled: true
        required: true
        min_tracks: 1
        max_tracks: 3
        preferred_tracks: 2
        weight: 20
        priority:
          - languages: [zh, zh-CN, yue]
            codecs: [Dolby TrueHD]
            min_channels: 8
            atmos: true
            commentary: false
          - languages: [zh, zh-CN, yue]
            codecs: [DTS-HD MA]
            min_channels: 6
            commentary: false
          - languages: [zh, zh-CN, yue]
            min_channels: 2
            commentary: false

      subtitle:
        enabled: true
        required: true
        min_tracks: 1
        max_tracks: 5
        preferred_tracks: 2
        weight: 20
        priority:
          - languages: [zh-CN]
            source: any
            hearing_impaired: false
          - languages: [zh, zh-TW, zh-HK]
            source: any
            hearing_impaired: false

      file_extension:
        enabled: true
        weight: 5
        priority: [mkv, mp4, ts]

    exclude:
      resolutions: [480p, 360p]
      codecs: [MPEG-2, Xvid]
      hdr_types: []

    version:
      enabled: false
```

使用这条规则时，只有同时存在合格中文音轨和中文字幕、且音轨/字幕数量没有超限的资源才有资格入库或洗版。分辨率、视频编码和容器格式只影响合格资源之间的总分。

### 使用轨道条件前的准备

使用轨道条件或轨道数量限制时，请在整理方案中开启源文件和目标文件的元数据提取。无法取得轨道信息时：

- 普通轨道偏好按该维度的 `unknown_policy` 处理：`ignore` 时双方跳过，`zero` 时未知侧明确记 0 分。
- 未知清单不会被当成 0 条轨道，也不会参与轨道数量或目标距离决胜。
- `required`、`min_tracks`、`max_tracks` 无法验证时，资源判定为不合格，并显示“轨道信息未提取”。
- 评分对比工具在没有目录伴随文件信息时只统计内封字幕；整理文件时还会统计可靠关联的外挂字幕。

### 配置校验

保存前会完整解析并校验。以下配置会拒绝保存，原有效配置保持不变：

- `required: true` 但 `priority` 为空。
- `unknown_policy` 不是 `ignore` 或 `zero`；错误信息会同时指出对应的评分维度。
- 数量为负数，或 `min_tracks > max_tracks`。
- `preferred_tracks` 不在已设置的最小/最大范围内。
- `min_channels > max_channels`。
- 音频条件使用 `formats`/`source`，或字幕条件使用 `codecs`/`atmos` 等错误字段。
- `source` 不是 `embedded`、`external`、`any`。
- 轨道条件没有填写任何匹配字段。
- 在音轨/字幕以外的普通评分维度使用轨道资格或数量字段。

### 排除规则

排除规则在评分前过滤资源：

```yaml
exclude:
  resolutions: [480p, 360p]
  codecs: [MPEG-2, Xvid, DivX]
  hdr_types: []
```

- `resolutions`：按最终识别到的分辨率精确匹配。
- `codecs`：按最终识别到的视频编码精确匹配。
- `hdr_types`：按最终识别到的 HDR 值精确匹配；未识别到 HDR 的资源按 `SDR` 处理。
- 匹配不区分大小写，但不使用 `priority` 的前缀匹配规则。例如排除 `HDR10` 不等于排除所有以 `HDR10` 开头的值。
- 命中任意一项就会跳过该资源，不再计算质量分数。

### 多版本功能

每个版本槽位内部都使用相同的资格判断和评分比较，不合格资源不能绕过轨道要求进入某个槽位。

#### 按字段自动分槽

```yaml
version:
  enabled: true
  dimensions: [resolution, hdr]
```

`dimensions` 可以使用：

- `resolution`
- `hdr`
- `video_codec`
- `audio_codec`
- `source`
- `file_extension`（也可写 `container`）

系统使用这些字段的实际值组合成槽位。例如 `dimensions: [resolution, hdr]` 会分别形成 `2160p + Dolby Vision`、`2160p + HDR10`、`1080p + SDR` 等槽位。命名模板中的 `{{versionTag}}` 会输出对应的简短标签。

#### 自定义槽位

```yaml
version:
  enabled: true
  unmatched: skip
  slots:
    - name: 4K DV
      match:
        resolution: [2160p]
        hdr: [Dolby Vision, Dolby Vision P7, Dolby Vision P8]
    - name: 4K HDR
      match:
        resolution: [2160p]
        hdr: [HDR10+, HDR10]
    - name: 1080p SDR
      match:
        resolution: [1080p]
        hdr: [SDR]
```

- 槽位按配置顺序匹配，命中第一个后停止。
- 同一槽位的多个字段是 AND；同一字段数组中的多个值是 OR。
- 值匹配不区分大小写，并支持与普通 `priority` 相同的前缀匹配。
- `unmatched: skip`：不符合任何槽位的资源直接跳过。这也是未填写 `unmatched` 时的行为。
- `unmatched: best`：不符合自定义槽位的资源归入同一个未匹配组，并在组内保留评分最好的资源。
- 同时填写 `slots` 和 `dimensions` 时，使用 `slots`。

---

## 自定义规则

除了上述三种整理规则外，MediaTidy 还提供自定义规则系统，用于在文件名识别阶段进行预处理和增强。所有自定义规则使用统一的 YAML 格式配置。

### YAML 结构总览

```yaml
# 渲染词（正则替换）- 识别前对文件名进行预处理
mr:
  - pattern: "正则表达式"
    replace: "替换内容"
  - pattern: "要删除的内容"
    action: remove

# 输出渲染词 - 对最终命名结果进行后处理
output_mr:
  - pattern: "正则表达式"
    replace: "替换内容"

# 季集映射 - 修正 TMDB 与实际季集号的差异
mp:
  - tmdb: 12345
    from: { season: 1, ep: [1, 24] }
    to:   { season: 2, ep: [1, 24] }

# 制作组识别
groups:
  - name: "FRDS"
    keywords: ["FRDS", "frds"]

# 流媒体服务识别
streaming:
  - name: "Netflix"
    keywords: ["Netflix", "NF"]

# 区域码识别
region:
  - name: "R1"
    keywords: ["R1", "Region A"]
```

### 渲染词（MR 规则）

渲染词是文件名识别前的正则预处理规则，按定义顺序依次执行。

#### 基本用法

```yaml
mr:
  # 删除文件名中的广告文字
  - pattern: "\\[www\\.example\\.com\\]"
    action: remove

  # 替换文字
  - pattern: "S(\\d+)EP"
    replace: "S$1E"

  # 带名称的规则（便于管理）
  - name: 修正剧集编号
    pattern: "第(\\d+)集"
    replace: "E$1"
```

#### TMDB 绑定

通过 `bind` 字段直接绑定 TMDB ID，跳过自动搜索：

```yaml
mr:
  - name: 某某动漫合集
    pattern: "某某动漫"
    bind:
      tmdb: 12345
      media: tv
      season: 1
      episode: "$1"   # 从正则捕获组提取集号
```

#### 输出渲染词（output_mr）

在命名完成后对最终文件名进行二次处理：

```yaml
output_mr:
  - pattern: "\\s{2,}"
    replace: " "
  - pattern: "\\.\\."
    replace: "."
```

#### 正则语法说明

- 默认**不区分大小写**
- 支持 Python 风格的 `(?<=...)` 后顾断言（自动转换为 Go RE2 兼容格式）
- 支持 `(?=...)` 前瞻断言
- 替换中使用 `$1`、`$2` 引用捕获组（也支持 `\1`、`\2`，自动转换）

### 季集映射（MP 规则）

当 TMDB 上的季集划分与实际文件不一致时使用。例如 TMDB 将动漫续作标为第 2 季，但文件名中集号从第 1 集开始。

```yaml
mp:
  # 将 TMDB ID 12345 的 S1E25-E48 映射到 S2E1-E24
  - tmdb: 12345
    from: { season: 1, ep: [25, 48] }
    to:   { season: 2, ep: [1, 24] }

  # 将全集编号(S1E1-E100)拆分到多季
  - tmdb: 67890
    from: { season: 1, ep: [1, 24] }
    to:   { season: 1, ep: [1, 24] }
  - tmdb: 67890
    from: { season: 1, ep: [25, 48] }
    to:   { season: 2, ep: [1, 24] }
```

映射支持以下集号表达式：
- **固定偏移**：`EP-24`（集号减 24）、`EP+1`（集号加 1）
- **原样保持**：`EP`（仅改变季号）
- **固定值**：直接指定目标集号范围

### 标签匹配（制作组 / 流媒体 / 区域码）

```yaml
# 简写方式：名称即关键词
groups:
  - "FRDS"
  - "CtrlHD"
  - "WIKI"

# 完整格式：一个名称对应多个匹配关键词
groups:
  - name: "FRDS"
    keywords: ["FRDS", "Frds"]

streaming:
  - name: "Netflix"
    keywords: ["Netflix", "NF", "NFLX"]
  - name: "Disney+"
    keywords: ["DSNP", "Disney+", "DisneyPlus"]

region:
  - name: "R1"
    keywords: ["R1", "Region A", "Region 1"]
```

关键词匹配规则：
- 不区分大小写
- 在文件名中匹配时会检查边界字符（方括号、下划线、空格、连字符等）

### 规则生效流程

```
mr 渲染词替换 → guessit 文件名解析 → TMDB 匹配 → 季集映射(MP) → 命名模板 → output_mr 输出渲染
```

### 规则管理

- **本地规则**：在「自定义规则」页面直接编辑 YAML
- **订阅源**：支持从远程 URL 同步规则，自动与本地规则合并
- **生效规则查看**：查看合并后实际生效的所有规则
- **单条禁用**：对生效规则列表中的单条规则进行启用/禁用切换
- **导出**：将当前生效规则导出为 YAML 文件

---

## 规则订阅

所有规则（分类、命名、质量、自定义规则）都支持从远程 URL 订阅。MediaTidy 使用**统一订阅管理**系统：

### 添加订阅

1. 进入「订阅管理」页面
2. 添加订阅源 URL 并选择规则类型
3. 系统定期自动同步（默认每 6 小时一次）
4. 也可手动触发同步

### 订阅类型

| 类型 | 说明 |
|------|------|
| `naming` | 命名规则订阅 |
| `quality` | 质量评分规则订阅 |
| `category` | 分类规则订阅 |
| `custom_rules` | 自定义规则订阅（渲染词 + 季集映射 + 标签） |

### 合并机制

- **命名/质量规则**：按规则的 `name` 字段合并，同名规则高优先级覆盖低优先级，不同名全部保留
- **分类规则**：整体替换，本地 > 订阅 > 内置
- **自定义规则**：本地和订阅的 YAML 按字段合并（`mr`、`mp`、`groups` 等分别拼接），本地规则排在前面（优先执行）

### GitHub Webhook 自动同步

支持配置 GitHub Webhook，当仓库推送更新时自动触发规则同步：

1. 在「订阅管理」中复制 Webhook URL
2. 在 GitHub 仓库 → Settings → Webhooks 添加
3. Content type 选 `application/json`
4. 填入 Secret（订阅管理页面可查看/重新生成）
5. 之后每次 `push` 事件都会自动同步最新规则
