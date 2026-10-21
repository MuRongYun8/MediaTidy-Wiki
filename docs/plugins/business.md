# 业务接口与组合示例

所有方法的准确参数、返回类型、能力权限与调用配额见 [能力清单](capabilities.md)。SDK 为同步 JSON 调用，失败抛出带 `code/message/retryable` 的错误。不要依赖中文错误文本做逻辑判断。

| 能力组 | 如何使用 |
|---|---|
| `runtime` | 查询运行 ID、资源、方法授权和额度；报告进度与检查取消 |
| `files` | `roots/list/stat/readText` 为读取；`scan/search` 和变更返回任务 |
| `system` | 公开版本、媒体扩展名、TMDB 语言、AI 模型标识及功能启用状态 |
| `rules` | 规则定义、修订、启用状态；`effective` 查询授权整理方案相关规则 |
| `media/tmdb` | 可选文件名解析或 MT 识别，以及独立作品搜索、详情和季集查询 |
| `organize` | 读取方案；授权自动执行；准备手动草稿后交给宿主确认 |
| `strm` | 方案、预览、生成、核验已有输出、授权清理孤立元数据 |
| `quality` | 准备评分数据、单项/批量评分、两文件比较及升级判断 |
| `records` | 按授权整理/STRM 方案读取业务历史和失败摘要 |
| `tasks/triggers` | 持久任务、逐项结果、取消、完成动作、定时和完成订阅 |
| `ai/http/notification` | 使用宿主模型、公开联网搜索、目标授权 HTTP 和指定通道通知 |
| `config/secrets/storage/log` | 自身配置、第三方密钥、业务持久化与有限日志 |

`config.get()` 是当前插件配置；`system.config()` 是 MT 公开业务配置；`organize.profile/strm.profile` 是已授权方案。它们不能用来读取全部数据库配置。规则与方案本轮只读，不提供系统设置、规则或方案的创建/修改/删除。

方案返回目录摘要：只有已授予对应文件目录时，才包含可用于 `files` 的 `rootId/path`。看到方案目录并不获得目录读写权限。自动执行方案则由方案授权覆盖其原有业务行为；方案内容变化会要求重新授权。

```ts
const run=mt.runtime.info();
const file=mt.files.stat({rootId:'目录ID',path:'notes.txt'});
const current=mt.files.readText({ref:file.ref});
const task=mt.files.writeText({
  destination:{rootId:file.rootId,path:file.path},fileRef:file.ref,
  text:current.text+'\n已处理',overwrite:true,idempotencyKey:run.runId+':notes'
});
mt.tasks.wait({refs:[task.ref]});
return {message:'正在写入'};
```

文本必须是 UTF-8，最大 128 KiB。复制/移动的 `destination` 指目标目录，宿主保留源名称；写文本的 `destination` 指目标文件。`rename` 的 `name` 只能是名称。文件搜索按名称/相对路径包含查询，不提供任意正则执行。批量变更最多 100 项，每项独立状态；整体不是事务，已完成部分不回滚。

```ts
const profile=mt.organize.profile({id:1});
const task=mt.organize.run({profileId:profile.id,idempotencyKey:mt.runtime.info().runId+':organize'});
mt.tasks.wait({refs:[task.ref],completion:{action:'send-summary',input:{}}});
return {message:'等待整理方案完成'};
```

自动执行遵循授权方案自身识别、命名、覆盖和清理策略。指定作品使用 `organize.manual.prepare` 或 `prepareBatch`；不会入队。目录展开为每文件草稿，混合作品应逐文件提议。作者页面使用宿主 `Results/SelectionBar`，用户可修正、预览并确认。参数变化会重新核验和确认。

`strm.preview` 产生含相对输出路径的任务结果；`strm.verify` 走原有生成队列核验已有输出；`strm.cleanup` 运行原有孤立元数据清理，需要独立能力。不能把核验或清理解释为只读操作。

评分先调用 `quality.prepare` 并等待完成，再使用评分/比较；缺失资料时检查 `completeness`，不能把缺失分值当成已验证的低质量。规则定义可读取，远程 FF 运行数据不可读取。

```ts
const token=mt.secrets.get({key:'apiToken'}).value;
const response=mt.http.request({url:'https://example.com/api/report',method:'POST',
  headers:{Authorization:'Bearer '+token},contentType:'application/json',
  body:JSON.stringify({count:3}),timeoutMs:10000,responseHeaders:['content-type']});
return {status:response.status};
```

请求必须匹配用户 HTTP 授权；禁止转发 MT 凭据。不要把密钥、完整请求或响应随意记录。通知返回成功表示进入通知队列，不代表对方已经收到。

AI 方法不会自动开启模型或联网。`ai.capabilities` 查询可用性；`ai.complete/chat` 只负责模型通信；工具执行由插件显式分发到允许的 SDK 方法。联网返回公开标题、摘要、来源。输入线索和查询词可能发送给用户配置的外部服务。模型输出不是权限、路径或整理确认。

常见错误：`PERMISSION_DENIED` 检查能力与资源；`RESOURCE_CHANGED/CONFLICT` 刷新并核对；`UNSUPPORTED` 调整方案，不绕过路由；`QUOTA_EXCEEDED` 缩小批次或请管理员管理配额；`OUTCOME_UNKNOWN` 停止自动重试并核对业务结果；`FLOW_WAITING` 立即返回释放工作进程。失败后使用同一幂等键查询已有任务，不通过换键掩盖未知结果。
