---
title: 分享洗版教程
description: MediaTidy 项目部署、规则、自动整理、STRM 生成与分享归档的完整教程。
---

# MediaTidy 项目使用教程

> 基于 CloudDrive2 项目，面向 115 网盘的专注整理工具

> 📌 **说明：** 截至本教程编写，支持mt版本为V0.1.9。

## 一、项目简介

MediaTidy（以下简称 MT）是基于 CloudDrive2（CD2）面向 115 网盘的媒体文件整理工具。其主要特色功能如下：

| 功能                 | 说明                                                                                            |
|----------------------|-------------------------------------------------------------------------------------------------|
| **FF缓存服务**       | 整理时通过服务器或本地缓存读取媒体信息，无需真实访问 115 下载，大幅降低风控和限速风险           |
| **神医JSON缓存服务** | 缓存神医 JSON 数据，提升提取效率                                                                |
| **分布式分担**       | 服务器没有的文件媒体信息，由所有使用该项目的本地用户共同分担 FF 读取任务                        |
| **STRM洗版比对**     | 支持网盘文件和本地分享strm 的洗版比对，让每个入库文件都是库里最好而且无重复，且无存储空间烦恼。 |

## 二、搭建前的准备

### 2.1 前置条件

1.  **CloudDrive2（CD2）**：本项目基于 CD2 访问 115 网盘资源，需提前安装，为提高体验，建议开启会员。
2.  **MediaTidy 授权**：获取项目授权码
3.  **Telesave（可选）**：同作者的项目，作为资源入口使用，需另外获取授权

### 2.2 路径规划（以飞牛 NAS 为例）

| 类型             | 路径                              |
|------------------|-----------------------------------|
| 115 网盘         | `/云盘影视`、`/待整理`、`/未识别` |
| 本地 STRM 路径   | `/vol1/1000/strm`                 |
| 本地 Docker 路径 | `/vol1/1000/docker/mediatidy`     |

### 2.3 CD2的搭建（以飞牛 NAS 为例）

```yaml
services:
  cloudnas:
    image: cloudnas/clouddrive2:latest
    container_name: clouddrive2
    ports:
      - 19798:19798
    environment:
      - TZ=Asia/Shanghai
      - CLOUDDRIVE_HOME=/Config
    volumes:
      - ./config:/Config
      - /vol1/1000/CloudNAS:/CloudNAS:shared
      - /vol1/1000/strm:/strm
    devices:
      - /dev/fuse:/dev/fuse
    restart: always
    privileged: true
    network_mode: bridge
```

**CD2内的挂载推荐:**

![2-3](https://img.remit.ee/api/file/BQACAgUAAyEGAASHRsPbAAEW4VRqT023R7TlRbMi3MS2q99Gm9Jb8AAC-SIAAuHegVbIa4O_tIt5wTwE.png)

### 2.4 CD2、MT、Emby 项目的映射路径解析

|   项目    | 容器内CD2挂载地址 | 容器内strm媒体库地址 |
|:---------:|:-----------------:|:--------------------:|
|   emby    |     /CloudNAS     |    /strm/云盘影视    |
| mediatidy |     /CloudNAS     |    /strm/云盘影视    |
|   基准    | 映射与mt保持一致  |  映射与emby保持一致  |

> **⚠️ 重要提醒**：如若有差异，须在Emby配置内进行路径映射，让mt能识别emby的内部容器地址

| 参数                 | 容器strm媒体目录地址 |
|----------------------|----------------------|
| emby:容器内路径      | /strm/云盘影视       |
| mt:容器内路径        | /app/strm/云盘影视   |
| mt项目内设置emby映射 | /app/strm:/strm      |

## 三、项目搭建与基础设置

### 3.1 Docker Compose 部署（推荐）

使用 Docker Compose 部署，便于后期维护。以下为飞牛 NAS 的 Compose 配置：

```yaml
services:
  mediatidy:
    image: murongyun574/mediatidy:latest
    container_name: mediatidy
    restart: always
    network_mode: "bridge"
    ports:
      - "2019:2019"      # Web 管理后台端口
      - "8091:8091"      # Emby 302 播放端口
    volumes:
      - ./data:/app/data                                          # 数据持久化
      - /vol1/1000/CloudNAS:/CloudNAS:rshared                     # CD2 FUSE 挂载点
      - /vol1/1000/strm:/strm                                     # 默认 STRM 挂载目录
    environment:
      - TZ=Asia/Shanghai
      - LOG_LEVEL=debug
      - LICENSE_CODE=             # 请填写你的授权码
```

### 3.2 首次启动与访问

1.  访问后台：http://\<本机IP\>:2019
2.  无默认账号密码，首次使用需自行注册

### 3.3 网盘配置

#### 3.3.1 CD2 配置

进入后台 → 网盘配置 → 添加 CD2 配置。链接方式支持账号密码或 Token 两种方式。  
挂载路径为 /CloudNAS/CloudDrive,最新版M169，推荐文件引擎为 「CloudDrive2」

![3-3-1](https://img.remit.ee/api/file/BQACAgUAAyEGAASHRsPbAAEW4VhqT04J4Npgxx31p7YOLSRxv6X4fwACASMAAuHegVZ3wisVJewLODwE.jpg)

#### 3.3.2 115 账号登录

- **115的cookie不是单项单用，可以多个项目共用一个cookie**

推荐抓取手机 App 的 cookie,操作以安卓手机软件Reqable(2.33.12版)为例：  
下载安装Reqable → 启动调试 → 打开115app并播放一段视频 → 关闭调试 → 搜索关键词vido → 在'原始'表中获取cookie

![3-3-2-1](https://img.remit.ee/api/file/BQACAgUAAyEGAASHRsPbAAEW4WFqT05PQWXx-AYGlOq9Ly_9oT2b6gACCiMAAuHegVbGoM7earUXvzwE.png)

![3-3-2-2](https://img.remit.ee/api/file/BQACAgUAAyEGAASHRsPbAAEW4WJqT059cX9XIaGqUG7yEiuOIYUAAb8AAgsjAALh3oFWP6Db70mmAw08BA.png)

#### 3.3.3 路径映射

按实际挂载路径和115账号做好映射关系，标签为MT项目文件管理器显示的自定义昵称，可自行修改。

![3-3-3](https://img.remit.ee/api/file/BQACAgUAAyEGAASHRsPbAAEW4WRqT06e0SbE9FMbFXrdB4VgyJ8QzwACDSMAAuHegVa1t9_aN_qAkTwE.jpg)

#### 3.3.4 115直连API 延时及CD2读取强度

推荐配置 CD2 读取强度为75%，频繁405可改为保守的50%。

![3-3-4-1](https://img.remit.ee/i/WA7mhFeZo7Rq)

- **115直连设置，主要影响到拉取分享strm的速度，主要影响项为-列表/搜索**

![3-3-4-2](https://img.remit.ee/i/7oOhBuMoOw5P)

#### 3.3.5 通用目录挂载

- 在CD2后台，把本地目录/strm挂载到CD2中 （如果是docker配置，先把/strm映射进CD2）
- 在通用挂载配置项目，扫码CD2，把新添加的/strm目录 挂载进mt文件管理器里

### 3.4 Emby 管理

1.  在后台 Emby管理 中添加 Emby 服务器，并生成API token填入,为了达到更美观的通知效果，入库延迟推荐180s，让emby有充分的时间刮削元数据。

![3-4](https://img.remit.ee/api/file/BQACAgUAAyEGAASHRsPbAAEW4WtqT08Zmyra09gF2sdi_N6A4EQmzwACFCMAAuHegVbLQ0re5i8SPDwE.png)

  
2. 在 Emby 内 通知地址 填写项目提供的 Webhook 地址  
http://\<本机IP\>:2019/api/webhook/emby

| 项目                  | 状态 |
|-----------------------|------|
| application/json      | 选择 |
| 媒体库/已添加新媒体   | 勾选 |
| 神医助手/媒体深度删除 | 勾选 |

3.  通知渠道推荐 双 TG 通知渠道，勾选为单独的 Emby 入库通知（不会混杂整理入库和 STRM 生成的通知）

### 3.5 系统设置

#### 3.5.1 Caddy 管理端口

MediaTidy 服务地址：填写 http://\<本机IP\>:2019，关系到分享 STRM 的正常工作。

#### 3.5.2 TMDB 配置

填写你自己的 TMDB API Key。如果没有请前往 TMDB 官网 申请，使用公共 Key 会影响整理效率。

#### 3.5.3 媒体后缀

- 在视频文件后缀添加.strm 保存。

#### 3.5.4 出站代理

按需填写，推荐使用 socks5:// 地址。（先保存再测试）

#### 3.5.5 AI 辅助识别（可选）

本项目支持调用 AI 对不规范命名进行标题提取。基于 GPT 的辅助识别配置较长，具体请到 TG 群组获取详细配置。

#### 3.5.6 系统通知

推荐使用 双 TG 通知：

- 一个用作整理通知，勾选整理相关通知
- 一个用作入库emby通知，不勾选任何选项，该通知在emby配置里勾选。

![3-5-6](https://img.remit.ee/api/file/BQACAgUAAyEGAASHRsPbAAEW4W9qT087CzjqsF2nsSVUXQpWap4EQQACGCMAAuHegVYiFU6VQFwR_DwE.png)

  
推荐勾选项请参照官方推荐配置。

\-**此外还有各类美观个性化通知模板，按需自取，很帅气！**  
<a href="https://github.com/MuRongYun8/-/blob/master/mt_tg.md#tg-%E9%80%9A%E7%9F%A5%E4%B8%BB%E9%A2%98%E6%A8%A1%E6%9D%BF%E5%90%88%E9%9B%86" class="external-link" data-footnote-index="1" target="_blank" rel="noopener noreferrer">个性化通知模板（点击跳转获取）</a>

## 四、规则引擎设置

MT 的整理、洗版、命名、分类功能均由规则引擎管理，使用 YAML 配置，简洁高效。

### 4.1 远程订阅链接

规则支持从 GitHub 远程加载，本地规则优先级高于远程规则。如果频繁读取不畅，可以用代理地址https://ghproxy.net/；  
示例为 https://ghproxy.net/https://raw.githubusercontent.com/MuRongYun8/-/refs/heads/master/output_name.yaml  
推荐策略：

- **参数精简主要为了美观，并不会影响洗版效果，推荐！**

| 规则类型 | 建议 | 远程规则链接                                                                        |
|----------|------|-------------------------------------------------------------------------------------|
| 命名规则 | 本地 | https://raw.githubusercontent.com/MuRongYun8/-/refs/heads/master/naming-rules.yaml  |
| 分类规则 | 本地 | https://raw.githubusercontent.com/MuRongYun8/-/refs/heads/master/category-rules     |
| 评分规则 | 本地 | https://raw.githubusercontent.com/MuRongYun8/-/refs/heads/master/quality-rules.yaml |
| 正则替换 | 远程 | https://raw.githubusercontent.com/MuRongYun8/-/refs/heads/master/full_rules.yaml    |
| TMDB覆盖 | 远程 | https://raw.githubusercontent.com/MuRongYun8/-/refs/heads/master/tmdb_override      |
| 参数精简 | 按需 | https://raw.githubusercontent.com/MuRongYun8/-/refs/heads/master/output_name.yaml   |

### 4.2 命名规则

命名规则主要有两种类型，一种为ff探测的参数，一种为文件名提取的参数，两者的参数值不一致，有需求自定义需要注意

- FF探测参数：需配合 FF 开关开启使用
- 文件名提取参数：需要文件名有此参数才能提取
- 本分享教程为三个整理任务，需要两种命名格式
- **本分享教程经过多次迭代，命名模板经过几次喜好转换。主要由\[tmdbid=xxx\]变更为{tmdb-xxx}，这只是个人喜好变更，请坚持你的原始命名，这个tmdb风格更改会涉及到前后目录的对齐，谨慎跟随。**
- 命名参数说明如下：

```yaml
# ============================================================================
# MediaTidy 命名规则模板
# ============================================================================
#
# 命名规则定义了整理后文件的 文件夹名 和 文件名 格式。
# 每条规则包含 movie（电影）和 tv（剧集）两套模板。
#
# ============================================================================
# 可用模板变量
# ============================================================================
#
# --- 基本信息 ---
#   {{title}}             TMDB 中文标题（如：流浪地球）
#   {{originalTitle}}     TMDB 原始标题（如：The Wandering Earth）
#   {{tmdbid}}            TMDB ID（如：475132）
#   {{year}}              年份（如：2019）
#   {{mediaType}}         媒体类型（movie / tv）
#   {{fileExt}}           文件扩展名（如：mkv、mp4）
#
# --- 季集信息（仅剧集有效）---
#   {{season}}            季号（如：1）
#   {{season02}}          季号两位补零（如：01）
#   {{episode}}           集号（如：5）
#   {{episode02}}         集号两位补零（如：05）
#   {{seasonEpisode}}     组合格式（如：S01E05）
#
# --- Guessit 解析字段（从文件名提取）---
#   {{videoFormat}}       分辨率（如：2160p、1080p、720p）
#   {{videoCodec}}        视频编码（如：HEVC、AVC、AV1）
#   {{audioCodec}}        音频编码（如：DTS-HD MA、TrueHD、AAC）
#   {{audioChannels}}     声道（如：7.1、5.1、2.0）
#   {{audioProfile}}      音频特性（如：Atmos）
#   {{source}}            片源（如：BluRay、WEB-DL、Remux）
#   {{edition}}           版本（如：Director's Cut、Extended）
#   {{dynamicRange}}      动态范围（如：HDR、HDR10+、DV）
#   {{releaseGroup}}      发布组（如：FRDS、CtrlHD）
#   {{streamingService}}  流媒体来源（如：Netflix、Disney+）
#   {{colorDepth}}        色深（如：10bit）
#   {{frameRate}}         帧率（如：60fps）
#
# --- ffprobe 探测字段（从媒体文件提取，优先级更高）---
#   {{probeResolution}}   探测分辨率（如：2160p、1080p）
#   {{probeCodec}}        探测视频编码（如：H.265、H.264）
#   {{probeAudio}}        探测音频编码（如：Dolby TrueHD、DTS-HD MA）
#   {{probeHDR}}          探测动态范围（如：Dolby Vision P8、HDR10）
#   {{probeSubtitle}}     探测字幕（如：PGS 简体中文）
#   {{probeColorDepth}}   探测色深（如：10-bit）
#   {{probeFrameRate}}    探测帧率（如：24fps）
#
# ============================================================================
# 模板语法说明
# ============================================================================
#
#   文件夹路径用 / 分隔层级，如 {{title}} ({{year}})/Season {{season02}}
#   缺失的变量会被替换为空字符串
#   特殊字符 < > : " | ? * 会被自动过滤
#
# ============================================================================
```

- ***推荐命名规则：***

```yaml
naming:
  - name: k自用-探测混合命名
    id: k-mixed
    movie:
      folder: "{{title}} ({{year}}) {tmdb-{{tmdbid}}}"
      file: "{{title}}.{{year}}.{{probeResolution}}.{{source}}.{{edition}}.{{probeHDR}}.{{probeColorDepth}}.{{probeFrameRate}}.{{probeBitrate}}.{{probeCodec}}.{{probeAudio}}.{{fileExt}}"
    tv:
      folder: "{{title}} ({{year}}) {tmdb-{{tmdbid}}}/Season {{season}}"
      file: "{{title}}.{{year}}.{{seasonEpisode}}.{{probeResolution}}.{{source}}.{{edition}}.{{probeHDR}}.{{probeColorDepth}}.{{probeFrameRate}}.{{probeBitrate}}.{{probeCodec}}.{{probeAudio}}.{{fileExt}}"

  - name: k自用-源信息命名
    id: k-filename
    movie:
      folder: "{{title}} ({{year}}) {tmdb-{{tmdbid}}}"
      file: "{{title}}.{{year}}.{{videoFormat}}.{{source}}.{{edition}}.{{dynamicRange}}.{{colorDepth}}.{{frameRate}}.{{bitrate}}.{{videoCodec}}.{{audioCodec}}.{{fileExt}}"
    tv:
      folder: "{{title}} ({{year}}) {tmdb-{{tmdbid}}}/Season {{season}}"
      file: "{{title}}.{{year}}.{{seasonEpisode}}.{{videoFormat}}.{{source}}.{{edition}}.{{dynamicRange}}.{{colorDepth}}.{{frameRate}}.{{bitrate}}.{{videoCodec}}.{{audioCodec}}.{{fileExt}}"
```

#### 命名效果示例

泰坦尼克号.1997.1080p.BluRay.REMUX.HDR10.10bit.24fps.50Mbps.HEVC.DTS-HDMA.mkv

提示：该命名添加了 REMUX、HDR、色深、帧率、码率等 FF 探测信息。如需自定义，可将参数说明交给 AI 辅助生成，或参照命名模板适配。

### 4.3 评分规则（洗版核心）

评分规则是 MT 洗版功能的核心，通过评分精准控制版本替换。  
**推荐版本为支持ISO，并iso作为多版本存在，不参与常规后缀的洗版。**

- **推荐规则**：按以下规则推荐，如有需要更改，请深度使用后再更改。
- **自定义规则**：可将评分语法说明交给 AI 学习，生成符合需求的规则。
- ***评分参数说明如下：***

```yaml
# ============================================================================
# MediaTidy 评分规则模板
# ============================================================================
#
# 评分规则用于对同一部影片的多个版本进行质量评分，自动选择最优版本。
# 每条规则包含 评分维度（scoring）和 排除规则（exclude）。
#
# ============================================================================
# 评分机制说明
# ============================================================================
#
# 总分 = 各维度得分之和
# 维度得分 = weight × 优先级位置分
#   优先级位置分：priority 列表中排名越靠前得分越高
#   例如 priority: [2160p, 1080p, 720p]
#        2160p → 最高分，1080p → 次高分，720p → 最低分
#
# file_size / bitrate 维度特殊：无 priority 列表，使用对数公式计算
#   file_size：文件越大得分越高（~50GB 饱和）
#   bitrate：码率越高得分越高（~100Mbps 饱和）
#
# ============================================================================
# 评分维度说明
# ============================================================================
#
#   resolution      分辨率（4320p > 2160p > 1080p > ...）
#   source          片源类型（Remux+UHD BluRay > ... > Unknown > ...）
#                   ⚠ Remux 必须使用组合格式：Remux+UHD BluRay / Remux+BluRay / Remux+BD
#                   ⚠ 无法识别来源的文件会映射为 Unknown
#   video_codec     视频编码（AV1 > H.265 > H.264 > ...）
#   audio_codec     音频编码（DTS:X > TrueHD Dolby Atmos > DTS-HD MA > ...）
#                   ⚠ 音频名称必须与 ffprobe 输出一致（见下方列表）
#   hdr             动态范围（Dolby Vision P7 > P8 > P5 > HDR10+ > HDR10 > ...）
#   color_depth     色深（12-bit > 10-bit > 8-bit）— 需 ffprobe
#   frame_rate      帧率（120fps > 60fps > 30fps > ...）— 需 ffprobe
#   subtitle        字幕（PGS 简体中文 > ASS > SRT > ...）— 需 ffprobe
#   file_extension  容器格式（mkv > mp4 > ts > ...）
#   file_size       文件大小（越大越好，对数公式）
#   bitrate         码率（越高越好，对数公式）— 需 ffprobe
#
# ============================================================================
# 音频编码标准名称（ffprobe 输出）
# ============================================================================
#
#   DTS:X                       对象式 DTS
#   TrueHD Dolby Atmos 7.1      Atmos TrueHD（7.1/5.1 等）
#   DTS-HD MA 7.1 / 5.1         DTS 无损（带声道）
#   Dolby TrueHD                TrueHD 无 Atmos
#   DTS-HD                      DTS-HD（非 MA）
#   Dolby Digital Plus Atmos    EAC3 Atmos
#   Dolby Digital Plus          EAC3
#   DTS                         标准 DTS
#   Dolby Digital               AC3
#   FLAC                        无损 FLAC
#   AAC                         AAC
#   MP3 / Opus / PCM            其他
#
# ============================================================================
# 排除规则说明
# ============================================================================
#
#   exclude.resolutions   排除的分辨率（如排除低清版本）
#   exclude.codecs        排除的编码（如排除过时编码）
#   exclude.hdr_types     排除的 HDR 类型
#
# ============================================================================
# ffprobe 探测控制
# ============================================================================
#
#   source_extract_metadata: true   对源文件执行 ffprobe 探测
#   dest_extract_metadata: true     对目标文件执行 ffprobe 探测
#   探测可获取更精确的编码、音频、字幕、码率信息，但会增加处理时间
#   ⚠ bitrate / color_depth / frame_rate / subtitle 维度需要 ffprobe 才能获取数据
#
# ============================================================================
```

- ***推荐评分规则：***

```yaml
quality:
  - name: 本地strm
    id: quality-strm
    version:
      enabled: true
      unmatched: best
      slots:
        - name: ISO
          match:
            file_extension: [iso]
    min_score_diff: 8
    scoring:
      resolution:
        enabled: true
        unknown_policy: zero
        weight: 20
        priority: [2160p, 1080p, 1080i, 720p, 480p]
      video_codec:
        enabled: true
        unknown_policy: zero
        weight: 10
        priority: [H.265, H.264, AV1, VP9]
      hdr:
        enabled: true
        unknown_policy: zero
        weight: 40
        priority: [Dolby Vision P7, Dolby Vision P5, Dolby Vision P8, Dolby Vision, HDR10+, HDR10, HLG, HDR, SDR]
      subtitle:
        enabled: true
        weight: 5
        priority:
          - score: 10.00
            languages: [zh-CN, zh]
            source: any
          - score: 8.00
            languages: [zh-TW, zh-HK, yue]
            source: any
          - score: 8.00
            languages: [und]
            source: any
      bitrate:
        enabled: true
        unknown_policy: zero
        weight: 25
    exclude:
      resolutions: [544p,480p,360p]
      codecs: [Xvid, DivX]
      hdr_types: []
 
  - name: 国语strm
    id: quality-guoman
    version:
      enabled: true
      unmatched: best
      slots:
        - name: ISO
          match:
            file_extension: [iso]
    min_score_diff: 8
    scoring:
      resolution:
        enabled: true
        unknown_policy: zero
        weight: 20
        priority: [2160p, 1080p, 1080i, 720p, 480p]
      video_codec:
        enabled: true
        unknown_policy: zero
        weight: 10
        priority: [H.265, H.264, AV1, VP9]
      hdr:
        enabled: true
        unknown_policy: zero
        weight: 40
        priority: [Dolby Vision P7, Dolby Vision P5, Dolby Vision P8, Dolby Vision, HDR10+, HDR10, HLG, HDR, SDR]
      bitrate:
        enabled: true
        unknown_policy: zero
        weight: 25
    exclude:
      resolutions: [544p,480p,360p]
      codecs: [Xvid, DivX]
      hdr_types: []

```

#### 多版本洗版方案（仅做说明，自行研究）

| 方案                 | 实现方式                                                  | 说明                         |
|:---------------------|:----------------------------------------------------------|:-----------------------------|
| 方案一：维度自动分槽 | 按分辨率 + HDR 自动保留多版本                             | GitHub 模板：「多版本均衡」  |
| 方案二：显式槽位     | 精选 4K DV + 4K HDR + 1080p 三版本                        | GitHub 模板���「多版本精选」 |
| 方案三：分类目录隔离 | 不同版本分入不同目录（如 `Season 1 DV` / `Season 1 HDR`） | 先分类，再在同类内洗版       |

### 4.4 分类规则

分类规则是迁移用户的重中之重，需要**对齐目录**和**对齐分类**。

#### 对齐目录

- **剧集**：对齐到 `/剧名 (年份) {tmdb-xxxx}/Season 1` 目录（注意 `Season 01` 与 `Season 1` 的区别）
- **电影**：对齐到 strm 所在目录即可

#### 对齐分类

- **电影分类**：推荐使用 `original_language`（语种）参数
- **剧集分类**：推荐使用 `origin_country`（国家）参数
- **不推荐参数**：`production_countries`（制片国家）参数，该参数容易混淆，错误命中。

#### 特殊分类示例（儿童/动漫）

```yaml
动漫/儿童:
  genre_ids: "10762,-10767,-99,-10764"
    
动漫/儿童:
  ?genre_ids: "&16,10751"
  ?keywords: "数码宝贝"
```

> 💡 `genre_ids` genre_ids这个参数在一个目录内通过或（?）连接，按照实践第二个genre_ids不会命中，如果有此需求，可以如例子进行多目录匹配。

- ***分类参数说明如下：***

```yaml
# ===================================================================================================
# 媒体库分类规则（按当前 MediaTidy 规则语法优化）
# ---------------------------------------------------------------------------------------------------
# 保留原粘贴版分类目录结构，仅优化匹配词和匹配条件。
#
# 一、文件结构
# ---------------------------------------------------------------------------------------------------
# movie: 电影规则
# tv:    剧集规则
#
# 每条规则格式：
#   分类/子分类/目录名:
#     字段名: "匹配值1,匹配��2,-排除值"
#
# 分类路径就是最终分类目录。路径里的 / 表示目录层级。
# 规则顺序就是优先级；从上往下匹配，命中第一条后停止，不再继续匹配后面的规则。
# 同一个分类路径可以重复出现，表示“多条独立规则都归入同一个目录”；MediaTidy 按 YAML
# 节点顺序读取并保留重复路径。不要为了消除 duplicate key 警告改成子目录，否则会改变目录结构。
# 空规则表示兜底分类，例如：
#   电视剧/未分类: {}
#
# 二、条件组合逻辑
# ---------------------------------------------------------------------------------------------------
# 普通字段为“必选条件”：同一规则内所有必选条件都必须匹配。
# 带 ? 的字���为“可选条件”：同一规则中只要至少一个 ? 条件命中即可。
# 同时存在必选条件和 ? 条件时：所有必选条件必须命中，并且至少一个 ? 条件命中。
#
# series_keywords / series_actors / series_directors 是辅助命中条件：
#   1. 即使不写 ?，也会按可选条件处理。
#   2. 如果规则里已有普通必选条件，它们不会阻止规则命中。
#   3. 如果一条规则只有 series_* 条件，则至少命中一个 series_* 才算命中。
#
# 三、字段名语法
# ---------------------------------------------------------------------------------------------------
# ?field      可选条件。例如 ?origin_country: "JP,KR"
# field?      同上，也表示可选条件。
# -field      字段级取反，表示该字段整体不能命中。一般更推荐用值级 -value。
# !field      同 -field；保存到 YAML 时会被 MediaTidy 预处理为 -field。
#
# 四、字段值语法
# ---------------------------------------------------------------------------------------------------
# 多个值用英文逗号分隔，也兼容中文逗号。
# value       包含任一普通值即匹配。例如 original_language: "ja,ko"
# -value      排除值；只要命中该值，当前条件失败。例如 genre_ids: "99,-16"
# !value      同 -value；保存到 YAML 时会被 MediaTidy 预处理为 -value。
# +value      genre_ids 专用，表示必须包含该类型。例如 genre_ids: "+16,10762"
# &value      genre_ids 专用，同 +value；为避免 YAML 锚点问题，推荐写 +value。
#
# 注意：
#   genre_ids: "16,10762"      表示包含 16 或 10762 任意一个即可。
#   genre_ids: "+16,10762"     表示必须包含 16，并且包含 10762 或普通值组中的任意一个。
#   genre_ids: "+16,+10762"    表示必须同时包含 16 和 10762。
#   genre_ids: "16,-10762"     表示包含 16，且不能包含 10762。
#   original_language: "-zh"   表示原始语言不是 zh；如果只有排除值，未命中排除值即通过。
#
# 五、支持字段总表（当前分类规则引擎支持的全部字段）
# ---------------------------------------------------------------------------------------------------
# 字段名                  别名/等价字段        来源                         匹配方式
# ---------------------------------------------------------------------------------------------------
# genre_ids               无                  TMDB genres                  类型 ID 匹配
# original_language       无                  TMDB original_language       单值代码精确匹配
# origin_country          无                  TMDB origin_country          多值国家/地区代码精确匹配
# production_countries    无                  TMDB production_countries    多值国家/地区代码精确匹配
# keywords                无                  TMDB 标题/name               标题包含关键词
# include_keywords        无                  TMDB keywords                TMDB 标签名精确匹配
# filename_keywords       无                  源文件名                     文件名包含关键词
# series_keywords         无                  TMDB 标题/name               标题包含关键词，辅助可选条件
# series_actors           无                  TMDB credits.cast            演员名包含关键词，辅助可选条件
# series_directors        无                  TMDB credits.crew Director   导演名包含关键词，辅助可选条件
# vote_average            无                  TMDB vote_average            评分区间匹配
# year                    release_year        TMDB release/first_air 年份   年份/年份区间匹配
# file_extension          无                  guessit 文件容器/后缀         单值精确匹配
# resolution              无                  ffprobe 或 guessit           单值精确匹配
# hdr                     dynamic_range       ffprobe 或 guessit           单值精确匹配
# dynamic_range           hdr                 ffprobe 或 guessit           单值精确匹配
#
# 不在上表中的字段不会参与分类匹配；例如 source、video_codec、audio_codec、file_size、
# bitrate、color_depth、frame_rate、subtitle 等是质量规则/命名/洗版相关字段，不是当前分类
# 规则字段。
#
# 六、字段详细说明
# ---------------------------------------------------------------------------------------------------
# 1. genre_ids
#   含义：TMDB 类型 ID。
#   适用：movie / tv。
#   来源：TMDB genres[].id。
#   匹配：
#     普通值为 OR：genre_ids: "16,99" 表示包含 16 或 99。
#     +值为必须包含：genre_ids: "+16,+10762" 表示同时包含动画和儿童。
#     -值为排除：genre_ids: "16,-10762" 表示动画但不是儿童。
#   支持：普通值、-排除、!排除、+必须包含、&必须包含。
#
# 2. original_language
#   含义：原始语言。
#   适用：movie / tv。
#   来源：TMDB original_language。
#   匹配：与语言代码精确匹配，大小写不敏感。
#   示例：original_language: "zh,cn,ja,ko"
#   支持：普通值、-排除、!排除。
#
# 3. origin_country
#   含义：剧集来源国家/地区。电影详情通常没有该字段。
#   适用：主要用于 tv。
#   来源：TMDB origin_country。
#   匹配：任一国家/地区代码命中即可，大小写不敏感。
#   示例：origin_country: "CN,TW,HK,MO"
#   支持：普通值、-排除、!排除。
#
# 4. production_countries
#   含义：制作国家/地区。
#   适用：movie / tv。
#   来源：TMDB production_countries[].iso_3166_1。
#   匹配：任一国家/地区代码命中即可，大小写不敏感。
#   注意：电影按地区分类时不推荐优先使用该字段；合拍、投资或发行背景可能导致
#         英语片等外语片带有 JP/KR/IN 等制作国家，从而误入地区分类。
#   特殊：用于 tv 时会先匹配 production_countries；如果没命中，会回退匹配 origin_country。
#   示例：production_countries: "US,GB,FR,DE,CA"
#   支持：普通值、-排除、!排除。
#
# 5. keywords
#   含义：标题关键词。
#   适用：movie / tv。
#   来源：电影使用 TMDB title；剧集使用 TMDB name。
#   匹配：标题包含任一关键词即可，大小写不敏感。
#   示例：keywords: "演唱会,Live,Concert,Tour"
#   支持：普通值、-排除、!排除。
#
# 6. include_keywords
#   含义：TMDB 标签关键词。
#   适用：movie / tv。
#   来源：TMDB keywords 列表。
#   匹配：TMDB keyword 名称与规则值精确相等，大小写不敏感；不是“包含”匹配。
#   示例：include_keywords: "tokusatsu,eroticism,marvel cinematic universe (mcu)"
#   支持：普通值、-排除、!排除。
#
# 7. filename_keywords
#   含义：源文件名关键词。
#   适用：movie / tv。
#   来源：整理任务当前文件名。
#   匹配：文件名包含任一关键词即可，大小写不敏感。
#   示例：filename_keywords: "remux,REMUX,Remux,AY,oSpecialCN"
#   支持：普通值、-排除、!排除。
#
# 8. series_keywords
#   含义：系列/片名辅助关键词。
#   适用：movie / tv。
#   来源：电影 title；剧集 name。
#   匹配：标题包含任一关键词即可，大小写不敏感。
#   特殊：series_* 字段天然是辅助可选条件，即使不写 ? 也不会卡住普通必选条件。
#   示例：series_keywords: "奥特曼,名侦探柯南,维也纳新年音乐会"
#   支持：普通值、-排除、!排除；排除标题更推荐写在 keywords 中，语义更直观。
#
# 9. series_actors
#   含义：演员辅助关键词。
#   适用：movie / tv。
#   来源：TMDB credits.cast[].name。
#   匹配：演员名包含任一关键词即可，大小写不敏感。
#   特殊：series_* 字段天然是辅助可选条件。
#   示例：series_actors: "周星驰,成龙,汤姆·克鲁斯"
#   支持：普通值；实现上不处理 - 排除。
#
# 10. series_directors
#   含义：导演辅助关键词。
#   适用：movie / tv。
#   来源：TMDB credits.crew 中 job=Director 的人员 name。
#   匹配：导演名包含任一关键词即可，大小写不敏感。
#   特殊：series_* 字段天然是辅助可选条件。
#   示例：series_directors: "宫崎骏,新海诚,克里斯托弗·诺兰"
#   支持：普通值；实现上不处理 - 排除。
#
# 11. vote_average
#   含义：TMDB 评分。
#   适用：movie / tv。
#   来源：TMDB vote_average。
#   匹配：闭区间，格式必须是 "最低分-最高分"。
#   示例：vote_average: "0.1-5.6"
#   支持：评分区间；不支持逗号列表和 - 排除。
#
# 12. year / release_year
#   含义：发行/首播年份。year 与 release_year 完全等价。
#   适用：movie / tv。
#   来源：电影 release_date 年份；剧集 first_air_date 年份。
#   匹配：
#     精确年份：year: "2024"
#     闭区间：  year: "2000-2009"
#     开始不限：year: "-1999"
#     结束不限：year: "2020-"
#     年份列表：year: "2020,2021,2022"
#   注意：年份为 0 或 TMDB 缺失年份时不会命中。
#
# 13. file_extension
#   含义：文件容器/扩展名。
#   适用：movie / tv。
#   来源：guessit 识别的 Container，通常为小写，如 mkv、mp4、iso。
#   匹配：与容器/后缀精确匹配，大小写不敏感。
#   示例：file_extension: "mkv,mp4,iso,m2ts"
#   支持：普通值、-排除、!排除。
#
# 14. resolution
#   含义：分辨率。
#   适用：movie / tv。
#   来源：优先使用 ffprobe 探针结果；没有探针结果时使用 guessit 文件名识别结果。
#   匹配：与分辨率文本精确匹配，大小写不敏感。
#   示例：resolution: "4320p,2160p,1080p,720p"
#   支持：普通值、-排除、!排除。
#
# 15. hdr / dynamic_range
#   含义：HDR / 动态范围。hdr 与 dynamic_range 完全等价。
#   适用：movie / tv。
#   来源：优先使用 ffprobe 探针结果；没有探针结果时使用 guessit 文件名识别结果。
#   匹配：与动态范围文本精确匹配，大小写不敏感。
#   示例：hdr: "Dolby Vision,HDR10,HDR10+,HLG,SDR"
#   支持：普通值、-排除、!排除。
#
# 七、空值和匹配细节
# ---------------------------------------------------------------------------------------------------
# 1. keywords / filename_keywords / series_keywords 的被匹配文本为空时，该条件不会命中。
# 2. include_keywords 依赖 TMDB keywords；如果 TMDB 没有返回标签，普通包含条件不会命中。
# 3. series_actors / series_directors 依赖 TMDB credits；如果没有演职员数据，不会命中。
# 4. file_extension / resolution / hdr 依赖文件识别或 ffprobe；如果未启用/未获取对应信息，普通包含条件不会命中。
# 5. 只有排除值的条件，例如 original_language: "-zh,-cn"，只要没有命中排除值就算通过。
# 6. 未知字段会返回不匹配；如果未知字段写成必选条件，会导致该规则永远不命中。
#
# 八、示例
# ---------------------------------------------------------------------------------------------------
# 动画且不是儿童：
#   genre_ids: "16,-10762"
#
# 必须同时是动画和儿童：
#   genre_ids: "+16,+10762"
#
# 日本或韩国电影按原始语言归类：
#   original_language: "ja,ko"
#
# 音乐类型且标题包含演出关键词：
#   genre_ids: "10402,-16"
#   keywords: "演唱会,Live,Concert,Tour"
#
# 4K HDR 文件：
#   resolution: "2160p"
#   hdr: "Dolby Vision,HDR10,HDR10+"
#
# ISO 原盘单独分类：
#   file_extension: "iso"
#
# 2020 年及以后的欧美剧：
#   ?origin_country: "US,GB,FR,DE,ES,IT,CA"
#   ?original_language: "en,fr,de,es,it"
#   year: "2020-"
#
# 低分电影：
#   vote_average: "0.1-5.6"
# ===================================================================================================
```

- ***分类规则推荐：(需按照自己的库进行调整)***

```yaml
movie:
  电影/外语电影:
    genre_ids: "!16"
    keywords: "超人"

  电影/特摄电影:
    genre_ids: "!16"
    ?include_keywords: "tokusatsu,ultraman,kaiju,kamen rider,super sentai,Power Rangers,VR Troopers,Beetleborgs,BIMA,Cicak-Man,Shaktimaan,Darna"
    ?keywords: "tokusatsu,ultraman,奥特曼,超人力霸王,特摄,特攝,假面骑士,假面騎士,铠甲勇士,金甲战士,超级战队,超級戰隊,超神战队,巨神战击队,金光布袋戏,布袋戏,霹雳布袋戏,苦海女神龙,霹雳神州,霹雳英雄,霹雳震寰宇,霹雳天命,云州大儒侠史艳文,Power Rangers,超凡战队,恐龙战队,VR Troopers,Beetleborgs,BIMA,神鹰勇士,Cicak-Man,Shaktimaan,Darna,光影天炎战甲,-超人"
    series_keywords: "奥特曼,超人力霸王,假面骑士,铠甲勇士,超级战队,金光布袋戏,霹雳布袋戏,GARO Collection"

  电影/R级电影:
    ?keywords: "聊斋艳谭, 肉蒲团, 蜜桃成熟时, 金瓶梅, 大内密探之零零性性, 聊斋之艳蛇, 超淫特攻队, Big波诱惑, 玉蒲团, 足本玉蒲团, 慈禧秘密生活, 飞虎出征, 现代应召女郎, 夜生活女王之霞姐传奇, 囡囡, 赤裸羔羊, 黑帮大佬和我的365日, 色戒, 戏梦巴黎, 苦月亮, 西西里的美丽传说, 你妈妈也一样, 巴黎最后的探戈, 罗马帝国艳情史, 卡里古拉, Caligula, 丁度·巴拉斯, Tinto Brass, 感官世界, 满清十大酷刑, 索多玛120天, 艾曼纽, 九歌, 女性瘾者, 花与蛇, 甜苦的月亮,花街柳巷里番,H动画,成人数码,成人动漫,18禁动画,ANIMATION,强奸,淫乱,乱伦"
    ?include_keywords: "Eroticism, Softcore, Sexual Fantasy, Erotic, Erotic Movie, Unusual Sexual Practices, Lesbian Sex, Gay Sex, Erotic Thriller, Erotic Drama, Erotic Horror, Erotic Animation, Blow Job, Unsimulated Sex, Sexual Torture, Pink Film, Sexuality, Sex, Softcore Pornography, Sexploitation, Skin Flick, Pornographic Film, Adult Entertainment, Erotic Film, Oral Sex, Explicit Sex,hentai,pornographic animation,hentai anime,anime porn"
    series_keywords: "美丽小蜜桃,深喉,艾曼纽,聊斋艳谭,蜜桃成熟时,五十度灰,禁忌,美式禁忌,小姐姐,妻子的情人,本能,女性瘾者,人体蜈蚣,俄罗斯学院，满清十大酷刑,痴汉日记,Caligula,花与蛇,强奸"

  电影/动画电影:
    genre_ids: "16"

  电影/演唱会:
    genre_ids: "10402,-16"
    ?keywords: "交响乐演唱会,演唱会,巡演,巡迴,巡回,演出,音乐会,音樂會,音乐剧,音樂劇,交响乐,交響樂,歌剧,歌劇,歌会,歌會,音乐节,音樂節,现场,現場,Live,Concert,Tour,Performance,Show,Stage,MV精选集,特别节目,湾区升明月,日本武道馆,初音未来,魔法未来,Hatsune Miku,少女时代,米津玄师,酒井法子,音乐盛宴,bilibili,维也纳新年音乐会,跨年晚会,元宵晚会,抖音,演唱會,蔡琴"
    series_actors: "周杰伦,林俊杰,王力宏,张韶涵,陈奕迅,张学友,孙燕姿,李宗盛,刘若英,郭富城,谭咏麟,林忆莲,初音未来,米津玄师,少女时代,酒井法子,蔡琴"
    series_keywords: "湾区升明月,中央广播电视总台,央视春节联欢晚会"

  电影/纪录电影:
    genre_ids: "99,-10402,-16"

  电影/华语电影:
    original_language: "zh,cn,bo,za,yue"

  电影/日韩电影:
    ?original_language: "ja,ko"
    ?origin_country: "JP,KR"

  电影/外语电影:

tv:
  电视剧/欧美剧:
    genre_ids: "!16"
    keywords: "超人"

  电视剧/特摄剧:
    genre_ids: "!16"
    ?include_keywords: "tokusatsu,ultraman,kaiju,kamen rider,super sentai,Power Rangers,VR Troopers,Beetleborgs,BIMA,Cicak-Man,Shaktimaan,Darna"
    ?keywords: "tokusatsu,ultraman,奥特曼,超人力霸王,特摄,特攝,假面骑士,假面騎士,铠甲勇士,金甲战士,超级战队,超級戰隊,超神战队,巨神战击队,金光布袋戏,布袋戏,霹雳布袋戏,苦海女神龙,霹雳神州,霹雳英雄,霹雳震寰宇,霹雳天命,云州大儒侠史艳文,Power Rangers,超凡战队,恐龙战队,VR Troopers,Beetleborgs,BIMA,神鹰勇士,Cicak-Man,Shaktimaan,Darna"
    series_keywords: "奥特曼,超人力霸王,假面骑士,铠甲勇士,超级战队,金光布袋戏,霹雳布袋戏"

  电视剧/综艺:
    genre_ids: "10764,10767,-99"

  电视剧/纪录片:
    genre_ids: "99,-10402,-16"

  动漫/儿童:
    genre_ids: "10762,-10751"

  动漫/儿童:
    ?genre_ids: "+16,10751"
    ?series_keywords: "喜羊羊,好奇世界,猫和老鼠,蓝猫淘气三千问,宝宝巴士,熊出没,猪猪侠,海底小纵队,汪汪队立大功,数码宝贝,宝可梦"

  动漫/国漫:
    genre_ids: "16,-10762"
    ?origin_country: "CN,TW,HK,MO"
    ?original_language: "zh,cn,bo,za,yue"
    keywords: "-名侦探柯南,-蜡笔小新,-宝可梦,-哆啦A梦"

  动漫/日番:
    genre_ids: "16"
    ?origin_country: "JP"
    ?original_language: "ja"
    series_keywords: "哆啦A梦,海贼王,火影忍者,名侦探柯南,死神,圣斗士,蜡笔小新,龙珠,宝可梦,鬼灭之刃,福音战士"

  动漫/欧美漫:
    genre_ids: "16"

  电视剧/港台剧:
    ?include_keywords: "TVB"
    ?keywords: "TVB,香港,港剧,港劇,HK,HongKong"
    ?origin_country: "TW,HK"
    ?original_language: "yue"

  电视剧/国产剧:
    ?origin_country: "CN"
    ?original_language: "zh,cn"

  电视剧/日韩剧:
    ?origin_country: "KR,JP,TH,VN,ID,MY,PH,MM,SG,KH,LA,BN"
    ?original_language: "ko,ja,th,vi,id,ms,tl,my,km,lo"

  电视剧/欧美剧:
```

------------------------------------------------------------------------

## 五、应用缓存设置

### 5.1 FF 缓存与神医 JSON 服务器

本项目最大的特色是 FF 缓存服务与神医 JSON 服务器。

- **激活条件**：需预先购买神医 Pro 版。
- **远程配置节点**：填入官方地址 `https://ff.mediatidy.dpdns.org`

### 5.2 神医缓存配置

| 配置项        | 推荐设置                               | 说明                                                    |
|:--------------|:---------------------------------------|:--------------------------------------------------------|
| 手动扫描      | 首次使用前建议执行一次                 | 类似于神医计划任务中的「提取 strm 媒体数据」            |
| 线程并发数    | 库内无缺失 JSON：16 线程；否则保持默认 | —                                                       |
| JSON 存放路径 | 必须与本地 strm 目录一致               | 如神医设置在其他目录，请改回                            |
| 自动整理池    | 推荐开启                               | 神医追更功能，适用于热剧入库                            |
| Emby 神医追更 | 需**关闭追更内的媒体提取**             | 避免与 MT 功能冲突                                      |
| 片头提取      | MT 暂不支持                            | 建议使用播放端 App 的片头标记或神医 Emby 的播放行为探测 |
| 定时整理      | 按需开启                               | 相当于神医 Emby 的定时提取计划任务                      |

![5-2-1](https://img.remit.ee/api/file/BQACAgUAAyEGAASHRsPbAAEW4XZqT0-X-QABA9D3fx6u0c7Hs6kbU5cAAh8jAALh3oFWQIQXe-Gdy8Q8BA.png)

![5-2-2](https://img.remit.ee/api/file/BQACAgUAAyEGAASHRsPbAAEW4Y9qT1CN3fxip9cY1CakiZg_N3b7TwACOCMAAuHegVYVYI4H6a8BxzwE.png)

## 六、自动整理任务

- **监控机制**：依托 CD2 的 gRPC，**只有通过 CD2 的操作才能被监控**。
- **入盘文件**：通过其他方式入盘的文件无法被监控，需使用**轮询监控**，推荐间隔 `20s ~ 30s`。
- **整理ff的激活需要再云盘模式下才能生效，整理任务必须用云盘模式**
- **在整理任务中，如需自定义添加视频后缀strm，在系统设置中添加也是一样效果**
- **元数据的筛选，需要在两个任务中都进行元数据的筛选**
- **剧集强匹配，需要在两个任务中都进行配置**
- 本地strm开启ff探测，需要在CD2中挂载本地目录，再通用挂载进mt内。
- 本地strm开启ff的先决条件，是strm文件的内容内要有对应文件的sha1值。

### 6.1 三个整理任务总览

| 序号 | 任务名称 |
|:----:|----------|
|  1   | 本地洗版 |
|  2   | 媒体入库 |
|  3   | 查重任务 |

------------------------------------------------------------------------

### 6.2 各任务配置详解

因流程变更，原来三任务流程，任务1为资源入口控制，所以只需在任务1控制黑名单及字幕相关。现在变更为双任务流程，则需要变更成每个任务都添加黑名单及字幕相关控制。

#### 6.2.1 新流程1：本地洗版

| 配置项                     | 设置                                         |
|----------------------------|----------------------------------------------|
| **储存类型**               | **云盘（重要！）**                           |
| **移动方式**               | **跳过（重要！）**                           |
| **源目录**                 | `/预处理`                                    |
| **目标目录**               | `/strm/云盘影视`                             |
| **最小文件大小**           | `0`                                          |
| **并发线程**               | 1 线程                                       |
| **命名规则**               | `k自用-探测混合命名`                         |
| **文件重命名**             | 开启                                         |
| **季强匹配**               | 开启                                         |
| **集强匹配**               | 关闭                                         |
| **洗版设置**               | 开启                                         |
| **评分规则**               | `本地strm`                                   |
| **按分类规则选择评分策略** | `开启`                                       |
| **FFprobe提取**            | 源文件探测和目标文件探测开启（其余复用关闭） |
| **FFprobe提取**            | 读取 STRM 内容 **开启**                      |
| **视频后缀**               | 自定义 → 添加 `.strm`（重要）                |
| **整理后清除**             | 开启                                         |
| **Emby媒体库刷新**         | 关闭                                         |
| **触发方式**               | 定期轮询 30s                                 |

**开启按分类规则选择评分策略，国产剧，国漫，港台剧，华语电影，另外实配‘字幕不参与评分‘的规则**  

![6-2-2](https://img.remit.ee/i/qWSeMlX98PDw)

------------------------------------------------------------------------

#### 6.2.2 新流程2：媒体入库

| 配置项                     | 设置                                         |
|----------------------------|----------------------------------------------|
| **储存类型**               | **云盘（重要！）**                           |
| **移动方式**               | 移动                                         |
| **源目录**                 | `/待整理`                                    |
| **目标目录**               | `/云盘影视`                                  |
| **最小文件大小**           | `0`                                          |
| **并发线程**               | 1 线程                                       |
| **命名规则**               | `k自用-探测混合命名`                         |
| **文件重命名**             | 开启                                         |
| **季强匹配**               | 开启                                         |
| **集强匹配**               | 关闭                                         |
| **洗版设置**               | 开启                                         |
| **评分规则**               | `本地strm`                                   |
| **按分类规则选择评分策略** | `开启`                                       |
| **FFprobe提取**            | 源文件探测和目标文件探测开启（其余复用关闭） |
| **FFprobe提取**            | 读取 STRM 内容 **关闭**                      |
| **整理后清除**             | 开启（重要）                                 |
| **触发方式**               | 手动执行                                     |

**开启按分类规则选择评分策略，国产剧，国漫，港台剧，华语电影，另外实配‘字幕不参与评分‘的规则**  

![6-2-3](https://img.remit.ee/i/HKGlGmi8pK1i)

------------------------------------------------------------------------

#### 6.2.4 查重任务

| 配置项             | 设置                          |
|--------------------|-------------------------------|
| **储存类型**       | 本地目录                      |
| **移动方式**       | **跳过（重要！）**            |
| **源目录**         | 本地目录 `/strm/云盘影视`     |
| **目标目录**       | 任意本地目录（空目录）        |
| **并发线程**       | 4 线程                        |
| **命名规则**       | `k自用-源信息命名`            |
| **最新文件大小**   | **0（重要！）**               |
| **文件重命名**     | 关闭                          |
| **季集强匹配**     | 关闭                          |
| **洗版设置**       | 开启                          |
| **评分规则**       | `本地strm`                    |
| **FFprobe提取**    | 全部关闭                      |
| **视频后缀**       | 自定义 → 添加 `.strm`（重要） |
| **整理后清除**     | 开启                          |
| **Emby媒体库刷新** | 关闭                          |
| **触发方式**       | 手动执行                      |

![6-2-4](https://img.remit.ee/api/file/BQACAgUAAyEGAASHRsPbAAEW4ZVqT1Cf5XqaUNyY8-TjbVsMGZvN5gACQCMAAuHegVa48vE05DgtMTwE.png)

------------------------------------------------------------------------

### 6.3 任务组设置

任务 1、2启用任务组联动：

- 在 **本地洗版** 任务中，添加 **媒体入库** 作为后续任务
- 实现一键触发完整整理流水线

------------------------------------------------------------------------

### 6.4 整体运行流程

1、新版任务组支持文件目录传递，子任务不重新扫描目录，此为双任务流程实现的基础。  
2、/待整理 目录的媒体文件通过跳过模式与本地strm目录内的strm文件进行洗版查重  
3、洗版查重后的文件再通过任务2移动到媒体目录  
4、新流程从旧流程的三层扫描目录缩减到一次扫描目录，大大缩短了整个流程的用时。

- ****此流程旨在每个入云盘文件，均进行本地洗版比对，保证唯一最优媒体文件。****
- ****跳过模式的逻辑****:**A对B进行洗版比对，如果A优于B则，删除B目录中对应的strm文件及元数据，并保留A目录中的文件；如果A劣于B则直接删除A对应中的文件。此教程中A为云盘目录，B为本地分享strm目录**

## 七、STRM 生成

> ⚠️ 当前版本仅推荐 **115 高速穿透**模式，strm 路径仅推荐 **CD2 本地路径模式**。

### 7.1 字幕与元数据同步

- **推荐方式**：**下载**

### 7.2 输出目录配置

| 路径类型 | 示例             | 说明                                             |
|:---------|:-----------------|:-------------------------------------------------|
| 绝对路径 | `/strm/云盘影视` | 对应 compose 中的 `/strm` 挂载                   |
| 相对路径 | `strm/云盘影视`  | 实际为 `/app/strm/云盘影视`，需核对 compose 映射 |

请根据实际 compose 配置按需更改。

### 7.3 清理功能说明

- **推荐方式**：**关闭清理孤立文件**

| 功能         | 风险等级 | 说明                                                      |
|:-------------|---------:|-----------------------------------------------------------|
| 清理脏元数据 |       低 | 清理本地 strm 目录内无对应 strm 文件的 nfo / jpg 等元数据 |
| 清理孤立文件 |    🔴 高 | 清理本地多余的 strm 及元数据（与 115 网盘无对应文件）     |

### 7.4 同步与刷新策略

- **实时同步**：基于 CD2 gRPC 消息监听，**需 CD2 会员**。
- **兜底策略**：CD2 gRPC 可能有遗漏，建议**设置定时任务每天执行**。
- **Emby 媒体库刷新**：
  - MT 与 Emby 的 strm 目录需保持一致（compose 中均为 `/strm` 则无需额外配置）。
  - 若 MT 为 `/app/strm`、Emby 为 `/strm`，需在「Emby 管理」中添加路径映射：`/app/strm` → `/strm`。

![7-4-1](https://img.remit.ee/api/file/BQACAgUAAyEGAASHRsPbAAEW4ZBqT1CQU2wBK_6Nyh4xRLMfcUW-EAACOSMAAuHegVZI8YQVg1HxWzwE.jpg)

  
（推荐配置截图如下）

![7-4-2](https://img.remit.ee/api/file/BQACAgUAAyEGAASHRsPbAAEW4ZFqT1CUM2mAJdmNTMKp-JmUi9PGOQACOiMAAuHegVbgLd6MPzH9BDwE.png)

## 八、分享strm归档（115网盘容量达上限时）

当115网盘容量达到上限时，可按以下步骤将现有媒体文件归档为分享链接，释放存储空间。

### 归档流程

- **在整个归档流程开始前，先将6-2-1所提及的’步骤1：预处理 ↔ 中转影视‘改为手动**

| 步骤 | 操作说明                                                                                                      |
|:----:|---------------------------------------------------------------------------------------------------------------|
|  1   | 先运行一次strm任务以补全缺漏strm                                                                              |
|  2   | 暂时关闭Emby项目，将115网盘内 `/网盘影视` 重命名为 `/归档+年份+序号`（如 `/归档2026-01`），并生成长期分享链接 |
|  3   | 等待分享链接正确识别容量大小后，通过MT按原分享账号拉取分享strm                                                |
|  4   | 将拉取到的分享strm主文件夹重命名，覆盖至本地目录 `/strm/网盘影视`                                             |
|  5   | 运行清理脚本，清除 `/strm/网盘影视` 内所有指向 `/CloudNAS` 的多余本地strm路径                                 |
|  6   | 运行本地strm查重任务（参考 6.2.4 查重任务配置）                                                               |
|  7   | 启动Emby，建议手动扫描一次媒体库以确保数据同步                                                                |
|  8   | 确认无误后，删除115网盘 `/网盘影视` 目录内文件即可                                                            |

- **清除本地 /strm/网盘影视 内多余路径 /CloudNAS 的strm 脚本。**

```python
import os
import shutil
import re
from pathlib import Path

# ==================<mark> 配置区域 </mark>==================
# 源目录（要扫描的目录，None表示当前目录）
SOURCE_DIR = "/vol1/1000/strm/云盘影视"

# ---- HTTP模式配置（模式1） ----
# 默认分享码（运行时可以修改）
DEFAULT_SHARE_CODE = "your_share_code"

# ---- 本地路径模式配置（模式2） ----
# 要匹配的本地路径前缀
LOCAL_PATH_PREFIX = "/CloudNAS"

# ==================<mark> 目标目录配置 </mark>==================
# 目标目录（移动/复制到这里）
TARGET_DIR = "/vol1/1000/strm/CloudNAS"

# ==================<mark> 文件关联配置 </mark>==================
# 文件名匹配规则（与.strm同名的文件会被一起操作）
FILE_PATTERNS = [
    "{base}.jpg",
    "{base}.nfo",
    "{base}-mediainfo.json",
    "{base}.xml",
    "{base}.srt",
    "{base}.ass",
]

# ==================<mark> 操作模式配置 </mark>==================
# 操作模式：'move' 移动（默认），'copy' 复制，'delete' 删除
OPERATION_MODE = 'move'  # 可选: 'move', 'copy', 'delete'

# 是否显示详细日志
VERBOSE = True

# 是否跳过已存在的文件（仅对复制模式有效）
SKIP_EXISTING = False

# 删除模式的安全确认
SAFE_DELETE = True

# ==================<mark> 辅助函数 </mark>==================

def get_operation_func(mode):
    """根据模式返回操作函数"""
    if mode == 'copy':
        return shutil.copy2
    else:
        return shutil.move

def match_share_code(content, pattern):
    """检查strm内容是否匹配分享码"""
    if not content or not pattern:
        return False
    
    try:
        if re.search(pattern, content):
            return True
    except re.error:
        if pattern in content:
            return True
    
    return False

def collect_matching_files(file_dir, base, patterns):
    """收集所有匹配模式的文件"""
    matching_files = []
    
    try:
        all_files = list(file_dir.iterdir())
    except OSError as e:
        if VERBOSE:
            print(f"警告: 无法读取目录 {file_dir} - {e}")
        return matching_files
    
    for pattern in patterns:
        for file_path in all_files:
            if file_path.is_file() and match_file_pattern(pattern, base, file_path.name):
                matching_files.append(file_path)
    
    return list(set(matching_files))

def match_file_pattern(pattern, base, file_name):
    """检查文件名是否匹配指定模式"""
    if '{base}' in pattern:
        base_pattern = pattern.replace('{base}', base)
    else:
        base_pattern = pattern
    
    if '*' in base_pattern:
        import fnmatch
        return fnmatch.fnmatch(file_name, base_pattern)
    else:
        return file_name == base_pattern

def delete_file_with_confirmation(file_path, safe_delete=True):
    """删除文件，带有安全确认（仅在SAFE_DELETE=True时确认）"""
    try:
        if safe_delete:
            confirm = input(f"确认删除文件: {file_path} ? (y/N): ")
            if confirm.lower() != 'y':
                print(f"跳过删除: {file_path}")
                return False
        
        if file_path.is_file():
            os.remove(file_path)
            return True
        elif file_path.is_dir():
            shutil.rmtree(file_path)
            return True
        else:
            print(f"无法删除: {file_path} (不是文件或目录)")
            return False
    except Exception as e:
        print(f"删除失败: {file_path} - {e}")
        return False

def process_files(src_dir, dest_root, strm_files, patterns, op_func, skip_existing):
    """处理strm文件及其关联文件"""
    deleted_count = 0
    processed_count = 0
    error_count = 0
    
    for strm_path in strm_files:
        # 计算相对路径（相对于源目录的根）
        try:
            rel_path = strm_path.relative_to(src_dir)
        except ValueError:
            print(f"错误: {strm_path} 不在源目录 {src_dir} 下")
            error_count += 1
            continue
        
        # 删除模式
        if OPERATION_MODE == 'delete':
            if delete_file_with_confirmation(strm_path, SAFE_DELETE):
                processed_count += 1
                if VERBOSE:
                    print(f"删除: {strm_path}")
            
            base_name = strm_path.stem
            src_dir_path = strm_path.parent
            related_files = collect_matching_files(src_dir_path, base_name, patterns)
            
            for src_file in related_files:
                if delete_file_with_confirmation(src_file, SAFE_DELETE):
                    deleted_count += 1
                    if VERBOSE:
                        print(f"  删除关联文件: {src_file.name}")
            
            try:
                if src_dir_path.exists() and not any(src_dir_path.iterdir()):
                    os.rmdir(src_dir_path)
                    if VERBOSE:
                        print(f"  删除空目录: {src_dir_path}")
            except OSError:
                pass
            
            continue
        
        # 构建目标路径（保持相同的目录结构）
        dest_strm_path = dest_root / rel_path
        
        if VERBOSE:
            print(f"\n处理: {rel_path}")
        
        # 检查是否跳过已存在的文件
        if skip_existing and op_func == shutil.copy2 and dest_strm_path.exists():
            if VERBOSE:
                print(f"  跳过(已存在): {dest_strm_path}")
            continue
        
        # 创建目标目录
        try:
            dest_strm_path.parent.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"  错误: 无法创建目录 {dest_strm_path.parent} - {e}")
            error_count += 1
            continue
        
        # 操作strm文件本身
        try:
            op_func(str(strm_path), str(dest_strm_path))
            processed_count += 1
            if VERBOSE:
                print(f"  ✓ {'复制' if op_func==shutil.copy2 else '移动'}: {strm_path.name}")
        except Exception as e:
            print(f"  ✗ 操作失败: {strm_path.name} - {e}")
            error_count += 1
            continue
        
        # 处理关联文件
        base_name = strm_path.stem
        src_dir_path = strm_path.parent
        
        related_files = collect_matching_files(src_dir_path, base_name, patterns)
        
        for src_file in related_files:
            dest_file = dest_root / rel_path.parent / src_file.name
            
            if skip_existing and op_func == shutil.copy2 and dest_file.exists():
                if VERBOSE:
                    print(f"    跳过关联文件(已存在): {src_file.name}")
                continue
            
            try:
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                op_func(str(src_file), str(dest_file))
                deleted_count += 1
                if VERBOSE:
                    print(f"    ✓ 关联: {src_file.name}")
            except Exception as e:
                print(f"    ✗ 关联失败: {src_file.name} - {e}")
                error_count += 1
    
    return processed_count, deleted_count, error_count

def main():
    print("=" * 60)
    print("STRM 文件处理工具")
    print("=" * 60)
    
    # 显示模式选择
    print("\n请选择匹配模式:")
    print("  1. HTTP模式 - 匹配分享码 (正则匹配)")
    print("  2. 本地路径模式 - 匹配 /CloudNAS 开头的路径")
    print("-" * 60)
    
    while True:
        choice = input("请输入 1 或 2: ").strip()
        if choice == '1':
            MATCH_MODE = 'http'
            break
        elif choice == '2':
            MATCH_MODE = 'local'
            break
        else:
            print("输入无效，请输入 1 或 2")
    
    # 如果是HTTP模式，让用户输入或确认分享码
    if MATCH_MODE == 'http':
        print("\n" + "=" * 60)
        print("分享码配置")
        print("=" * 60)
        print(f"默认分享码: {DEFAULT_SHARE_CODE}")
        print("\n提示: 分享码支持正则表达式")
        print("例如: your_share_code 或 share/[a-zA-Z0-9]{10,}")
        print("-" * 60)
        
        while True:
            share_input = input(f"请输入分享码 (直接回车使用默认: {DEFAULT_SHARE_CODE}): ").strip()
            if share_input == "":
                SHARE_CODE_PATTERN = DEFAULT_SHARE_CODE
                print(f"使用默认分享码: {SHARE_CODE_PATTERN}")
                break
            else:
                print(f"\n您输入的分享码: {share_input}")
                confirm = input("确认使用此分享码？(y/N): ").strip().lower()
                if confirm == 'y':
                    SHARE_CODE_PATTERN = share_input
                    print(f"已确认使用: {SHARE_CODE_PATTERN}")
                    break
                else:
                    print("请重新输入分享码")
                    continue
    
    # 确定源目录
    if SOURCE_DIR is None:
        src_dir = Path.cwd()
    else:
        src_dir = Path(SOURCE_DIR)
    
    if not src_dir.exists():
        print(f"错误: 源目录不存在 - {src_dir}")
        return
    
    print(f"\n源目录: {src_dir}")
    print(f"匹配模式: {'HTTP模式 (匹配分享码)' if MATCH_MODE == 'http' else '本地路径模式 (匹配/CloudNAS)'}")
    
    if MATCH_MODE == 'http':
        print(f"分享码: {SHARE_CODE_PATTERN}")
    else:
        print(f"本地路径前缀: {LOCAL_PATH_PREFIX}")
    
    # 确定目标根目录
    if OPERATION_MODE != 'delete':
        dest_root = Path(TARGET_DIR)
        if not dest_root.is_absolute():
            dest_root = src_dir / TARGET_DIR
        print(f"目标目录: {dest_root}")
    
    # 确定操作函数
    op_func = get_operation_func(OPERATION_MODE) if OPERATION_MODE != 'delete' else None
    print(f"操作模式: {'复制' if op_func==shutil.copy2 else '移动' if op_func else '删除'}")
    
    # 收集匹配的strm文件（不再需要确认配置）
    matched_strms = []
    skipped_count = 0
    
    print("\n扫描.strm文件...")
    for strm_file in src_dir.rglob("*.strm"):
        try:
            with open(strm_file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
            
            matched = False
            
            if MATCH_MODE == 'http':
                if match_share_code(content, SHARE_CODE_PATTERN):
                    matched = True
            else:
                if content.startswith(LOCAL_PATH_PREFIX):
                    matched = True
            
            if matched:
                matched_strms.append(strm_file)
                if VERBOSE:
                    rel = strm_file.relative_to(src_dir)
                    print(f"✓ 匹配: {rel}")
            else:
                skipped_count += 1
                if VERBOSE and skipped_count <= 5:
                    rel = strm_file.relative_to(src_dir)
                    preview = content[:50] + "..." if len(content) > 50 else content
                    print(f"✗ 跳过: {rel}")
        except Exception as e:
            print(f"读取失败: {strm_file} - {e}")
    
    if skipped_count > 5 and VERBOSE:
        print(f"... 还有 {skipped_count - 5} 个文件被跳过")
    
    # 直接执行操作，不再确认
    if not matched_strms:
        print(f"\n没有找到匹配的strm文件")
        return
    
    print(f"\n找到 {len(matched_strms)} 个匹配的文件，开始处理...")
    
    # 直接执行操作
    if OPERATION_MODE == 'delete':
        processed, deleted, errors = process_files(src_dir, None, matched_strms, FILE_PATTERNS, None, False)
        print(f"\n{'='*60}")
        print(f"完成！")
        print(f"  删除了 {processed} 个strm文件")
        print(f"  删除了 {deleted} 个关联文件")
        if errors > 0:
            print(f"  错误: {errors} 个")
    else:
        processed, deleted, errors = process_files(src_dir, dest_root, matched_strms, FILE_PATTERNS, op_func, SKIP_EXISTING)
        print(f"\n{'='*60}")
        print(f"完成！")
        print(f"  处理了 {processed} 个strm文件")
        print(f"  处理了 {deleted} 个关联文件")
        if errors > 0:
            print(f"  错误: {errors} 个")
        print(f"  目标位置: {dest_root}")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
```

<div class="footnotes-section">

------------------------------------------------------------------------

### 参考资料:

1.  <span id="fn-1">个性化通知模板（点击跳转获取）: <a href="https://github.com/MuRongYun8/-/blob/master/mt_tg.md#tg-%E9%80%9A%E7%9F%A5%E4%B8%BB%E9%A2%98%E6%A8%A1%E6%9D%BF%E5%90%88%E9%9B%86" target="_blank" rel="noopener noreferrer">https://github.com/MuRongYun8/-/blob/master/mt_tg.md#tg-%E9%80%9A%E7%9F%A5%E4%B8%BB%E9%A2%98%E6%A8%A1%E6%9D%BF%E5%90%88%E9%9B%86</a></span>

</div>
