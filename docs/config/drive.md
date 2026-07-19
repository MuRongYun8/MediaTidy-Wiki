# 网盘配置

网盘配置页面用于管理 CloudDrive2 连接、115 账号、通用挂载点和 API 调用策略。

## CloudDrive2 配置

MediaTidy 通过 CD2 的 gRPC 接口进行文件操作（列表、移动、复制、删除、重命名等）。

| 配置项 | 字段 | 说明 | 示例 |
|--------|------|------|------|
| **CD2 地址** | `url` | CloudDrive2 服务地址（gRPC 端口） | `http://192.168.1.100:19798` |
| **认证方式** | `authMode` | `password`（用户名密码）或 `token` | — |
| **用户名** | `username` | CD2 登录用户名（authMode=password 时） | — |
| **密码** | `password` | CD2 登录密码（authMode=password 时） | — |
| **Token** | `token` | CD2 API Token（authMode=token 时） | — |
| **FUSE 挂载路径** | `mountBase` | CD2 FUSE 挂载的本地路径（可选） | `/CloudNAS` |

![CloudDrive2 连接与访问方式配置示例](/screenshots/drive-connection-settings.png)

*填写地址和认证信息后，再根据自己的部署方式选择文件管理与下载引擎。只有已经挂载 FUSE 时才选择“本地挂载 (FUSE)”。*

### FUSE 挂载路径说明

`mountBase` 是 CD2 将网盘挂载为本地文件系统的路径。配置后：
- 文件管理器可通过 FUSE 本地路径直接访问文件
- 某些操作（如文件监听、本地读取）会优先使用 FUSE 通道
- 如果不使用 FUSE 挂载，留空即可

::: warning
在 Docker 中使用 FUSE 挂载时，挂载卷需添加 `:rslave` 挂载传播选项，确保容器内能看到宿主机的 FUSE 挂载：
```yaml
- /CloudNAS:/CloudNAS:rslave
```
:::

---

## 115 账号管理

支持多 115 账号，每个账号独立配置，独立管理 Cookie 和风控状态。

### 账号字段

| 字段 | 说明 |
|------|------|
| `name` | 账号显示名称 |
| `cookie` | 115 登录 Cookie |
| `userId` | 自动获取的 115 用户 ID |
| `status` | 账号状态（`active` / `expired`） |
| `userInfo` | 缓存的用户信息（JSON） |

### 添加账号

1. 点击「添加 115 账号」
2. 填入账号名称（仅显示用，可随意取）
3. 填入 115 Cookie
4. 保存后系统自动验证连接并获取用户信息

### Cookie 获取方式

1. 浏览器登录 [115.com](https://115.com)
2. 按 F12 打开开发者工具 → 切换到「网络」(Network) 标签
3. 刷新页面，点击任意请求
4. 在请求头中找到 `Cookie` 字段，复制完整内容

::: tip
Cookie 有效期有限，过期后需重新获取并更新。系统会在 Cookie 失效时自动将账号状态标记为 `expired`。
:::

---

## 路径映射

路径映射是 MediaTidy 虚拟路径系统的核心，用于关联 CD2 挂载路径与 115 账号。

| 字段 | 说明 | 示例 |
|------|------|------|
| `cd2MountPath` | 该账号在 CD2 中的挂载路径 | `/115open` |
| `accountId` | 关联的 115 账号 ID | 1 |
| `label` | 显示标签（可选） | — |

### 虚拟路径机制

配置路径映射后，系统会生成虚拟路径供所有功能使用：

```
CD2 挂载路径: /115open        115 账号名: 我的115
                ↓
虚拟路径根: /我的115/
虚拟路径示例: /我的115/电影/阿凡达.mkv
                ↓
CD2 路径: /115open/电影/阿凡达.mkv
115 原生路径: /电影/阿凡达.mkv
```

虚拟路径在整理方案、STRM 方案、文件管理器中统一使用。系统根据路径自动识别所属账号，并路由到正确的后端通道（CD2 或 115 API）。

---

## 通用挂载点

通用挂载点用于管理非 115 的存储源（如阿里云盘、夸克、本地目录等），通过 CD2 挂载后统一管理。

| 字段 | 说明 | 示例 |
|------|------|------|
| `displayName` | 在文件管理器中显示的名称（唯一） | 阿里云盘 |
| `cd2MountPath` | 该存储在 CD2 中的挂载路径（唯一） | `/阿里云盘` |
| `providerType` | 存储类型标识 | `aliyun` / `quark` / `local` / `unknown` |

通用挂载点**只支持 CD2 通道**操作（不支持 115 原生 API），路径解析后直接使用 CD2 gRPC 接口。

---

## 路由配置

控制不同操作使用的引擎通道：

| 字段 | 可选值 | 说明 |
|------|--------|------|
| `fileManagement` | `cd2`（默认）/ `fuse` | 文件管理操作（列表、创建、重命名、移动等）使用的通道 |
| `download` | `direct`（默认）/ `cd2` | 下载链接获取使用的通道 |

- **cd2**：通过 CD2 gRPC API 操作，兼容性最好
- **fuse**：通过 FUSE 本地文件系统操作（需配置 `mountBase`）
- **direct**：通过 115 原生 API 直接操作，速度最快但仅支持 115 账号

::: tip
推荐配置：文件访问选择 **fuse**，下载选择 **direct**。

- 文件访问走 FUSE：浏览、整理、移动、复制等操作更像本地文件系统处理，适合已挂载 `/CloudNAS` 的环境。
- 下载走 direct：通过 115 Cookie 获取下载地址和播放直链，更适合 115 网盘和 STRM 场景。

如果没有配置 FUSE 挂载，文件访问再保持 `cd2`。
:::

---

## API 调用延迟

API 调用延迟用于控制对 115 服务器的请求频率，避免触发限频或风控。

| 字段 | 说明 | 单位 |
|------|------|------|
| `globalMultiplier` | 全局倍率，所有延迟乘以此值 | 倍数 |
| `globalDelay` | 所有操作的基础延迟 | 秒 |
| `listDelay` | 目录列表操作间隔 | 秒 |
| `renameDelay` | 重命名操作间隔 | 秒 |
| `deleteDelay` | 删除操作间隔 | 秒 |
| `fileOpDelay` | 移动/复制操作间隔 | 秒 |
| `downloadDelay` | 下载链接获取间隔 | 秒 |

::: warning
如果频繁触发 115 风控（code 911），可以适当增大延迟值或 `globalMultiplier`。
:::
