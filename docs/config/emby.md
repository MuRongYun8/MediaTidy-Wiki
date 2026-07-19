# Emby 配置

Emby 管理页面用于配置 Emby 反向代理、302 直链播放和 Webhook 联动。所有 Emby 相关配置集中在此页面管理。

::: tip
关于反向代理的详细工作原理和高级配置，请参阅[Emby 反向代理](/features/emby-proxy)功能文档。
:::

## Emby 服务器

### 添加服务器

| 配置项 | 字段 | 说明 |
|--------|------|------|
| **服务器名称** | `name` | 自定义名称（留空则自动从 Emby 获取） |
| **Emby 地址** | `embyUrl` | Emby 内网地址（如 `http://192.168.1.100:8096`） |
| **API Key** | `embyApiKey` | Emby 管理面板生成的 API 密钥 |
| **监听端口** | `listenPort` | 反代对外暴露的端口（每台服务器独立端口，不可重复） |
| **启用** | `enabled` | 是否启用此服务器的反代 |

![Emby 实例、Webhook 与路径映射配置示例](/screenshots/emby-server-settings.png)

*一个实例卡片内可以完成地址、代理端口、预缓存、Webhook 和路径映射设置。首次添加时先点“测试”，确认连接成功后再保存。*

系统会自动连接 Emby 的 `/System/Info/Public` 接口获取服务器名称和内部 ID。

### 获取 Emby API Key

1. 登录 Emby 管理面板
2. 进入「设置 → 高级 → API 密钥」
3. 点击「新建 API 密钥」
4. 填入应用名称（如 `MediaTidy`）
5. 复制生成的密钥

### 连接测试

添加前可点击「测试连接」按钮验证 Emby 地址和 API Key 是否有效，系统会返回服务器名称和版本号。

## 全局代理配置

| 配置项 | 字段 | 默认值 | 说明 |
|--------|------|--------|------|
| **管理端口** | `adminPort` | 2019 | MediaTidy 管理面板的 Web 端口 |

管理端口与所有 Emby 代理端口不可冲突。

## 每服务器配置

每台 Emby 服务器可独立配置以下功能：

### 预缓存

| 配置项 | 字段 | 默认值 | 说明 |
|--------|------|--------|------|
| **启用预缓存** | `preCacheEnabled` | false | 浏览详情页时提前解析 115 直链 |
| **预缓存 QPS** | `preCacheQps` | 2 | 每秒预缓存请求数 |

### 同播复制

| 配置项 | 字段 | 说明 |
|--------|------|------|
| **启用同播复制** | `concurrentCopy` | 多人同时播放同一文件时自动复制获取独立直链 |
| **复制目录** | `concurrentCopyDir` | 复制目标目录名（默认 `最近接收`） |

### Webhook

| 配置项 | 字段 | 说明 |
|--------|------|------|
| **启用 Webhook** | `webhookEnabled` | 接收 Emby 的事件通知 |
| **Webhook 事件** | `webhookEvents` | 订阅的事件类型（留空 = 全部） |
| **通知渠道** | `notificationChannelIds` | 事件转发的通知渠道（留空 = 全部） |

在 Emby 中配置 Webhook 地址为 `http://<mediatidy-ip>:8080/api/webhook/emby`。

支持的事件：

| 事件 | 用途 |
|------|------|
| **Library Changed** | 媒体库变更，触发 STRM 刷新 |
| **Item Added** | 新增媒体项 |
| **Item Removed** | 删除媒体项，可同步清理 STRM |
| **Playback Start** | 播放事件统计 |

### 路径映射

| 配置项 | 字段 | 说明 |
|--------|------|------|
| **路径映射** | `pathMappings` | MediaTidy 本地路径 → Emby 路径的映射 |

当 Docker 环境中 MediaTidy 和 Emby 的挂载路径不同时需要配置：

```json
[
  { "localPrefix": "/app/strm", "embyPrefix": "/media/strm" }
]
```

点击「检测路径映射」按钮可自动对比目录结构并推荐映射配置。

## Emby 刷新

整理或 STRM 生成完成后可自动触发 Emby 媒体库刷新（在整理方案或 STRM 方案中配置）：

- **精确刷新**：仅刷新变更的目录
- **延迟刷新**：等待一段时间后刷新，合并多次变更减少 Emby 负载
