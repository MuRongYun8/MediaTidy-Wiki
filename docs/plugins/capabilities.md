# SDK v2 能力清单（生成文件）

同步 JSON 调用；错误具有 `code/message/retryable`。每次调用重新校验授权、安装修订与配额。以下类型定义见 [index.d.ts](/downloads/plugins-sdk-v2/index.d.ts)。无权限名表示仍需插件启用和有效安装身份。

| 方法 | 权限 | 单次运行上限 | 输入 | 返回 |
|---|---|---:|---|---|
| `ai.capabilities` | — | 500 | `void` | `{chat:MTAvailability;webSearch:MTAvailability;tmdb:MTAvailability}` |
| `ai.chat` | ai.chat | 78 | `{messages:MTMessage[];tools?:MTTool[];fileRefs?:string[]}` | `{message:MTMessage;usage:MTUsage;toolsUnavailable?:boolean;metrics:MTMetrics}` |
| `ai.complete` | ai.complete | 32 | `{system:string;input:string;schema?:Record<string,MTJSON>}` | `{content:MTJSON;usage:MTUsage}` |
| `ai.web.search` | ai.web.search | 32 | `{query:string}` | `{items:{title:string;summary:string;url:string}[];usage:MTUsage;metrics:MTMetrics}` |
| `config.get` | — | 500 | `void` | `Record<string,MTJSON>` |
| `files.batch` | files.write | 500 | `{idempotencyKey:string;items:MTFileMutation[]}` | `MTTask` |
| `files.copy` | files.write | 500 | `MTMutation` | `MTTask` |
| `files.delete` | files.delete | 500 | `MTMutation` | `MTTask` |
| `files.list` | files.read | 500 | `MTSelection & {page:number}` | `{items:MTFile[];hasMore:boolean}` |
| `files.mkdir` | files.write | 500 | `MTMutation` | `MTTask` |
| `files.move` | files.write | 500 | `MTMutation` | `MTTask` |
| `files.readText` | files.read | 500 | `{ref:string}` | `{text:string;version:string}` |
| `files.rename` | files.write | 500 | `MTMutation` | `MTTask` |
| `files.roots` | files.read | 500 | `void` | `MTRoot[]` |
| `files.scan` | files.read | 500 | `MTScan` | `MTTask` |
| `files.search` | files.read | 500 | `MTScan` | `MTTask` |
| `files.stat` | files.read | 500 | `MTSelection` | `MTFile` |
| `files.writeText` | files.write | 500 | `MTMutation` | `MTTask` |
| `http.request` | http.request | 50 | `MTHTTPInput` | `{status:number;headers:Record<string,string>;body:string}` |
| `log` | — | 500 | `{level?:'info'&#124;'warn'&#124;'error';message:string}` | `boolean` |
| `media.parse` | media.parse | 500 | `{name:string}` | `MTMediaIdentity` |
| `media.recognize` | media.recognize | 100 | `{fileRef:string}` | `MTMediaIdentity` |
| `notification.send` | notification.send | 10 | `{channelId:string;title:string;content:string}` | `boolean` |
| `organize.manual.prepare` | organize.prepare | 500 | `MTProposal` | `MTDraft &#124; {items:MTDraft[]}` |
| `organize.manual.prepareBatch` | organize.prepare | 100 | `{items:MTProposal[]}` | `{items:MTDraft[]}` |
| `organize.profile` | organize.read | 500 | `{id:number}` | `MTProfile` |
| `organize.profiles` | organize.read | 500 | `void` | `MTProfile[]` |
| `organize.run` | organize.run | 500 | `MTProfileRun` | `MTTask` |
| `quality.compare` | quality.compare | 500 | `MTQualityInput & {otherRef:string}` | `MTQualityComparison` |
| `quality.evaluate` | quality.evaluate | 500 | `MTQualityInput` | `MTQualitySummary` |
| `quality.evaluateBatch` | quality.evaluate | 500 | `{fileRefs:string[];profileId:number}` | `{items:{fileRef:string;summary?:MTQualitySummary;error?:MTError}[];interrupted:boolean}` |
| `quality.prepare` | quality.prepare | 500 | `{fileRefs:string[];profileId:number;idempotencyKey:string}` | `MTTask` |
| `quality.upgrade` | quality.compare | 500 | `MTQualityInput & {otherRef:string}` | `{comparison:MTQualityComparison;shouldUpgrade:boolean}` |
| `records.list` | records.read | 500 | `{kind:'organize'&#124;'failure'&#124;'strm';profileId:number;cursor?:string;limit?:number}` | `MTPage<MTBusinessRecord>` |
| `rules.effective` | rules.read | 500 | `{profileId:number;mediaType?:'movie'&#124;'tv';categoryPath?:string;categoryRuleKey?:string}` | `{profile:MTProfile;rules:MTRule[];selection:{namingRuleId:string;qualityRuleId:string;routedRuleId:string};revision:string}` |
| `rules.get` | rules.read | 500 | `{id:string;family?:string}` | `MTRule` |
| `rules.list` | rules.read | 500 | `{family?:string;offset?:number;limit?:number}` | `MTOffsetPage<MTRule>` |
| `runtime.capabilities` | — | 500 | `void` | `MTCapability[]` |
| `runtime.checkpoint` | — | 500 | `void` | `boolean` |
| `runtime.info` | — | 500 | `void` | `MTRuntime` |
| `runtime.progress` | — | 500 | `MTProgress` | `boolean` |
| `runtime.resources` | — | 500 | `void` | `MTResources` |
| `secrets.get` | secrets.use | 30 | `{key:string}` | `{value:string}` |
| `storage.batch` | storage | 500 | `{operations:MTStorageOperation[]}` | `MTStorageEntry[]` |
| `storage.delete` | storage | 500 | `{key:string;expectedRevision?:string}` | `MTStorageEntry` |
| `storage.get` | storage | 500 | `{key:string;expectedRevision?:string}` | `MTStorageEntry` |
| `storage.list` | storage | 500 | `{prefix?:string;cursor?:string;limit?:number;values?:boolean}` | `MTPage<MTStorageEntry>` |
| `storage.set` | storage | 500 | `MTStorageWrite` | `MTStorageEntry` |
| `storage.usage` | storage | 500 | `void` | `MTStorageUsage` |
| `strm.cleanup` | strm.cleanup | 10 | `MTProfileRun` | `MTTask` |
| `strm.preview` | strm.read | 500 | `MTProfileRun` | `MTTask` |
| `strm.profile` | strm.read | 500 | `{id:number}` | `MTProfile` |
| `strm.profiles` | strm.read | 500 | `void` | `MTProfile[]` |
| `strm.run` | strm.run | 10 | `MTProfileRun` | `MTTask` |
| `strm.verify` | strm.run | 10 | `MTProfileRun` | `MTTask` |
| `system.config` | system.read | 500 | `void` | `MTSystemConfig` |
| `system.info` | system.read | 500 | `void` | `{version:string;sdkVersion:'2'}` |
| `tasks.cancel` | tasks.cancel | 500 | `{ref:string}` | `boolean` |
| `tasks.get` | tasks.read | 500 | `{ref:string}` | `MTTask` |
| `tasks.items` | tasks.read | 500 | `{ref:string;offset?:number;limit?:number}` | `MTOffsetPage<MTTaskItem>` |
| `tasks.list` | tasks.read | 500 | `{cursor?:string;limit?:number}` | `MTPage<MTTask>` |
| `tasks.wait` | tasks.wait | 500 | `{refs:string[];completion?:MTRunRequest}` | `{waiting:boolean}` |
| `tmdb.detail` | tmdb.read | 500 | `{id:number;mediaType:'movie'&#124;'tv'}` | `MTCandidate` |
| `tmdb.search` | tmdb.read | 500 | `{query:string;mediaType:'movie'&#124;'tv';year?:number}` | `MTCandidate[]` |
| `tmdb.season` | tmdb.read | 500 | `{id:number;season:number}` | `number[]` |
| `triggers.events.create` | events.subscribe | 100 | `Omit<MTEventSubscription,'id'&#124;'instanceId'&#124;'revision'>` | `MTEventSubscription` |
| `triggers.events.delete` | events.subscribe | 100 | `{id:string}` | `boolean` |
| `triggers.events.list` | events.subscribe | 100 | `void` | `MTEventSubscription[]` |
| `triggers.events.pause` | events.subscribe | 100 | `{id:string}` | `MTEventSubscription` |
| `triggers.events.update` | events.subscribe | 100 | `MTEventSubscription` | `MTEventSubscription` |
| `triggers.schedules.create` | triggers.manage | 500 | `MTScheduleCreate` | `MTSchedule` |
| `triggers.schedules.delete` | triggers.manage | 500 | `{id:string}` | `boolean` |
| `triggers.schedules.list` | triggers.manage | 500 | `void` | `MTSchedule[]` |
| `triggers.schedules.pause` | triggers.manage | 500 | `{id:string}` | `MTSchedule` |
| `triggers.schedules.update` | triggers.manage | 500 | `MTSchedule` | `MTSchedule` |
