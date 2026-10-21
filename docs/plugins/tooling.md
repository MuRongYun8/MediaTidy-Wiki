# 工具、验证与发布

`mt-plugin init/check/build/test/preview/pack` 是开发机工具，宿主不执行这些命令。SDK 包版本 `2.0.0`，不表示 MT 主应用版本变更。

| 命令 | 验证内容 |
|---|---|
| init | 复制通用目录清单、类型及模拟接口，使用本地开发包依赖 |
| build | 打包 worker，编译页面为 JSON，再做类型和清单校验 |
| check | 清单、能力名、页面协议、脚本语法、TypeScript |
| test | 宿主包校验 + 独立 Goja 执行 `tests/goja.json` 场景 |
| preview | 仅监听 127.0.0.1，使用 MT 同一渲染器、模拟数据和受控事件 |
| pack | 白名单资源生成 ZIP，并通过宿主包读取器验证 |

`tests/goja.json` 每个场景包含 `input`、按顺序的 `calls`、可选 `result`。调用项有 `method/input/result` 或 `error`。测试执行真实 Goja，因此能发现 Node API、Promise 或工作进程协议问题；SDK 响应是模拟值，不证明真实云盘/AI 可用。

另可 `require('./sdk/mock.cjs')` 使用 `createMockHost`。它维护隔离 KV、TTL、条件更新、原子批次和配额；未显式配置的业务方法会失败，避免“万能成功”模拟。真实权限、SSRF 和 FF 边界由宿主 Go 测试验证。

开发包维护者从 MT 根目录构建：

```sh
node scripts/sync-plugin-sdk-v2.cjs --types-only
node plugin-sdk/cli.cjs build plugin-sdk/starter
node scripts/sync-plugin-sdk-v2.cjs
cd backend
go build -o ../plugin-sdk/bin/mt-plugin-runtime ./cmd/plugin-devtool
cd ../frontend
pnpm exec vite build --config vite.plugin-preview.config.ts
cd ..
node scripts/generate-plugin-sdk.cjs --check
npm --prefix plugin-sdk test
node plugin-sdk/cli.cjs test plugin-sdk/starter
```

Windows 二进制名称使用 `mt-plugin-runtime.exe`。也可用 `MT_PLUGIN_RUNTIME` 指定匹配版本工具的绝对路径。预览资源输出到 `plugin-sdk/preview`；开发包必须带上它和本机平台二进制。插件运行环境不依赖开发包中的 Node 依赖。

`sync-plugin-sdk-v2.cjs` 同时生成插件中心下载的 Skill ZIP，不再将任何示例插件打入宿主。更新官方文档项目时执行 `node scripts/sync-plugin-wiki.cjs <MediaTidy-Wiki目录>`，将同版本文档、类型和同一份 ZIP 同步到 VitePress；导航设置由文档项目维护。同步与本地构建不会推送或部署站点。

发布仓库提交 `plugin.json/dist/index.js/ui/page.json` 及可选 `ui/icon.png`，打版本标签。MT 通过 GitHub/Gitee 公开仓库的分支或标签解析固定提交，用户审阅权限后安装。更新是用户操作，失败保留旧版本。不要提交密钥、测试数据库或真实日志；开发 Skill 不隐含推送、发布或扩大授权。

排错顺序：先 `check/build`，再 Goja 测试，最后在测试实例授权运行。找不到 runtime 时提供匹配工具；找不到 preview 时构建开发包资源；`INCOMPATIBLE` 检查 SDK 版本；权限拒绝核对清单和资源；方案变化重新审阅授权；清理被阻止查看任务中心。模型、云盘或联网环境不可用时标记未验证，不用模拟结果宣称真实业务成功。

SDK v1 文档和旧 AI 模板仅作历史参考。开发新插件以本目录、同包类型和通用示例为准；不要运行旧模板同步脚本覆盖它们。
