# 清单、页面与 Logo

清单固定 `entry: "dist/index.js"`。字段类型支持 `text/textarea/number/boolean/files/profile/stringList`，通过 `key/label/type/required/default` 定义。`files` 写入运行选择而非普通 input。字段 key 应符合同版本校验规则；未知字段或不匹配类型会被后端拒绝。每项配置/动作参数上限 16 KiB。

```json
{
  "id":"example.my-plugin","name":"我的插件","version":"0.1.0","sdkVersion":"2",
  "author":"作者","description":"生成授权目录清单","entry":"dist/index.js",
  "permissions":["files.read","storage"],"config":[],
  "actions":[{"id":"run","label":"生成清单","fields":[{"key":"files","label":"目录","type":"files","required":true}]}],
  "ui":{"version":"1","entry":"ui/page.json","icon":"ui/icon.png"}
}
```

页面在 `src/ui/page.ts` 用类型检查，在构建时输出 `ui/page.json`。安装后浏览器只接收经过校验的 JSON；不加载作者的 React 或 JavaScript。`ui/icon.png` 来自插件包，安装时解码校验和重新编码，参与完整性哈希与回退。不要使用远程图片、SVG、HTML 或 CSS 作为 Logo。

```ts
import type {UIPage} from '../../sdk/ui-schema';
export default {
  version:'1',tabs:[{id:'run',label:'运行',content:[
    {component:'Card',props:{title:'选择目录'},children:[
      {component:'FilePicker'},
      {component:'Button',props:{label:'生成清单',action:'start',actionId:'run'}}
    ]},
    {component:'Table',props:{source:'run.result',columns:[
      {label:'文件',cells:[{component:'Text',props:{bind:'row.name',lines:2}}]}
    ]}}
  ]}]
} satisfies UIPage;
```

| 组件 | 作用 |
|---|---|
| Page、Stack、Grid、Card | 页面与响应式布局，受控间距、列数 |
| Text、Badge、Alert、Status、EmptyState | 文本、状态、错误、空态 |
| Input、Textarea、Select、Checkbox | 绑定清单参数或配置 |
| FilePicker、ProfilePicker | 宿主授权资源选择 |
| Steps、Metric、Progress | 阶段、统计、真实进度 |
| Table、Details、Search、Pagination | 结果表格、详情与分页 |
| Results、SelectionBar | MT 整理核验、修正和最终确认 |
| RunHistory、RunLog、ConfigForm、ScheduleForm、TaskList、DataManagement | 宿主管理组件 |
| Button | 声明动作或宿主固定事件 |

精确属性以同包 `ui-schema/index.d.ts` 和注册表为准。绑定命名空间为 `plugin/input/config/ui/run/stats/row`，只读取自身属性。`visibleWhen/disabledWhen` 仅支持 `eq/ne/truthy/falsy`，不接受 JS 表达式或函数。动态结果不能生成新组件。

按钮事件支持 `start/newRun/refresh/cancelRun/retry/editDraft/cancelTask/openTab/clearSelection/confirmDrafts`；`start` 只能指向已声明动作。`confirmDrafts` 只是打开宿主预览，不是直接入队。`run.result` 表格适合普通数组；`run.drafts` 使用宿主整理模型，作者不能伪造可提交状态。

页签为 `overview/run/history/settings`。把常用流程放运行页，把配置、定时放设置。展示真实排队/等待/失败/取消状态，未知总数使用不定进度。手机、深浅主题和键盘操作使用独立预览与真实浏览器检查；窄内容栏不等价手机视口。

## 普通结果批量选择

普通结果表使用稳定、唯一的字符串键，不把行号当身份：

```ts
{component:'Table',props:{
  source:'run.result',rowKey:'row.ref',selectionBind:'input.selectedRefs',
  columns:[{label:'文件',cells:[{component:'Text',props:{bind:'row.name'}}]}]
}}
```

动作清单声明 `{"key":"selectedRefs","label":"选择项","type":"stringList"}`，再用普通 `start` 按钮调用该动作。`stringList` 上限 1000 项、每项 512 字节，仍受每字段 16 KiB 总上限。表格每页 20 项、跨页选择，搜索不会自动取消选择；重复键和缺失键不可选。新结果中的失效选择会清除。脚本收到的选择是用户输入，调用文件或业务能力时后端仍独立校验引用和授权。

宿主始终提供“宿主管理与授权”，即使作者页面省略配置页，用户仍可管理配置、资源、密钥、调度、事件和数据。`TaskList` 展示业务任务与父流程；`DataManagement` 展示当前安装的数据空间。
