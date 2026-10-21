# 开发入门

先准备 Node.js 22 或更新版本、同版本 SDK 开发包和匹配平台的 `mt-plugin-runtime`。开发机可以安装构建依赖；MT 安装插件时只读取预打包文件，不执行 npm、构建或仓库脚本。

```sh
node /path/to/plugin-sdk/cli.cjs init ./my-plugin
cd my-plugin
npm install
npm run build
npm run check
npm test
npm run preview
npm run pack
```

`init` 默认以本地 SDK 路径作为开发依赖，不会寻找尚未发布的远程包。先修改 `plugin.json` 中的 `id/name/author/description`，保持 SDK 与页面版本。不同作者应使用不同 ID。仓库来源也是身份的一部分，同名仓库不能继承别人的数据或授权。

```text
plugin.json          清单、权限、参数及页面入口
src/worker/index.ts  同步 Goja 业务入口
src/ui/page.ts       TypeScript 页面定义
dist/index.js        构建出的业务脚本
ui/page.json         构建出的纯 JSON 页面
ui/icon.png          可选 Logo
sdk/                固定版本的类型与模拟接口快照
tests/goja.json      真实 Goja 执行场景
tests/preview.json   页面模拟数据
```

入口是 `module.exports.run(input)`，返回 JSON 值。`input` 包含 `action/files/input/config/sdkVersion/event`；`files` 是用户直接选择的文件和目录，目录不会隐式递归。SDK 在 Goja 内同步调用，不能用 `async`、Promise、Node 模块或浏览器 API。

```ts
module.exports.run = function (input: MTInput) {
  const previous = mt.storage.get({key: 'last-result'});
  const result = {count: input.files.length, hadPrevious: previous.found};
  mt.storage.set({key: 'last-result', value: result});
  return result;
};
```

在清单声明 `storage`；需要文件选择时再声明 `files.read`。用户仍需授予具体目录读取权限。单独声明能力不代表已经获得资源授权。

目录清单示例包含四个动作：

1. `scan-files`：将目录交给 `files.scan`，为每个扫描任务生成本次运行内稳定的幂等键；单独选择的文件保存到临时业务键。
2. `collect-report`：只接受宿主完成事件，分页读取任务结果，合并独立文件，去重后原子保存最新报告并删除临时键。
3. `show-report`：读取持久报告。MT 重启或刷新页面不会丢失报告。
4. `select-report`：读取表格跨页选择的相对路径，保存选中项，演示 `selectionBind`、`rowKey` 和 `stringList` 参数。

示例报告限制 1,000 行及一个 KV 值的字节预算；达到上限会提示缩小范围。更大报告应按页保存多个键，不应突破通信和存储上限。扫描失败时已生成的逐项结果仍可查看，不能把部分报告描述成完整扫描成功。

改动后运行 `build/check/test/pack`，再在测试用 MT 中安装并授予最小权限。修改页面只需重建 `ui/page.json`，不修改宿主 React 代码。
