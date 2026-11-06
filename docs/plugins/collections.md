# 多插件仓库与 ZIP

MT 0.1.14（当前未发布）宿主支持一个公开 GitHub/Gitee 仓库或一个 ZIP 中包含多个 SDK v2 插件。
每次选择一个插件、审阅配置与权限后独立安装；多插件 ZIP 只需上传一次，安装完成后可选择“继续安装其他插件”。

## 作者发布

每个插件目录必须是独立运行包：

```text
my-plugins/
  plugins.json
  poster/
    plugin.json
    plugin.py
    pyproject.toml
    uv.lock
    ui/
  organizer/
    plugin.json
    plugin.py
    pyproject.toml
    uv.lock
```

建议在根目录提供发布索引：

```json
{
  "schemaVersion": 1,
  "plugins": [
    { "id": "example.poster", "path": "poster" },
    { "id": "example.organizer", "path": "organizer" }
  ]
}
```

ID 必须与对应 `plugin.json` 一致；根插件的 path 为 `""`。
有索引时只允许安装已列出的目录；索引格式、版本、路径或重复路径错误会拒绝整个来源，不自动扫描兜底。
清单损坏、ID 不一致、必要文件缺失只禁用对应候选；重复 ID 的所有相关候选都禁止安装。

无索引时递归发现 `plugin.json`，跳过 `.git`、`.venv`、`node_modules`、`__pycache__`、`mt_plugin`。
选中插件的子目录若另有 `plugin.json`，整个子插件目录都不会进入当前运行包，即使它未被索引发布或清单损坏。
根索引、环境目录和宿主保留文件不进入运行包。

在作者机器上对每个项目分别执行现有 `python -m mt_plugin pack --root <项目目录> --output <单插件ZIP>`。
将每个构建完成的单插件 ZIP 解压到集合的独立子目录，添加索引，再压缩整个集合目录。
[两插件集合示例](/plugins/collection)提供现有目录清单与存储示例的集合索引和完整组包命令，源码包含在[开发 Skill 完整包](downloads.md)中。
不要把单插件 ZIP 文件本身直接嵌套进集合 ZIP；宿主不递归打开内部 ZIP。
Git 发布分支也应提交这些独立构建产物。宿主不执行仓库构建脚本，不构建 React，不接受父目录/兄弟目录的运行资源或路径依赖。
依赖安装沿用 SDK v2 的 Python 3.12、锁文件和公开 PyPI wheel 限制。

集合 ZIP 可以有一层共同包装目录；仓库子目录保持真实位置。
单个来源最大 40 MiB，整个归档解压后最大 200 MiB、1000 个条目，忽略的目录也计入限制。
非法路径、链接、特殊文件、大小写冲突以及文件/目录冲突会拒绝整个归档。

## 安装与更新

在插件安装窗口填写仓库或上传 ZIP。候选总数为一个且有效时直接进入预览，否则显示候选列表。
选择已安装 ID 会进入更新预览，沿用已有配置与授权；新增能力不会自动获得授权。
插件 ID 是宿主唯一安装标识，同一 ID 不能安装两份。

Git 更新只检查安装时保存的仓库目录：

- 分支跟随该分支，预览固定到一次发现的 commit；安装不会重新取分支头。
- 标签与完整 commit 锁定原提交；作者移动同名标签不会自动更新已安装插件。
- 主动更换版本需填写新的 ref；分支和标签同名时使用 `refs/heads/名称` 或 `refs/tags/名称`。
- 当前目录消失、被索引移除或 ID 改变时直接报错，旧安装保持不变，不寻找或迁移到其他目录。
- 需要更换目录时，先备份，再卸载并保留数据，从新目录安装后通过数据管理手动关联同 ID、同仓库的保留数据；重新审阅配置和授权。
- 其他插件或根索引变化不会改变当前插件内容哈希。无内容变化时无需重装，可显式修复安装文件。

ZIP 更新入口只匹配唯一相同 ID；没有匹配或重复 ID 时拒绝更新。
ZIP 内部目录不作为 Git 来源记录。ZIP 更新已有 Git 插件保留其仓库、目录和 ref；新 ZIP 构建不冒充原 Git 提交。
ZIP 插件可通过明确的 Git 更新预览绑定来源，即使代码内容相同也需要确认。不同 Git 仓库之间不支持原地迁移。

上传会话有效期为上传完成后 30 分钟，全局最多 10 份、400 MiB。
关闭窗口或更换来源会主动释放；过期和服务重启会清理。安装成功后保留会话供继续选包。
已经生成的有效预览及已经开始的安装不依赖原 ZIP，会话释放不会中断它们。
预览本身也有效 30 分钟；提交任务不会延长票据有效期，已接受的安装任务可继续完成。过期预览需重新生成，配置、授权或安装状态变化后也需重新审阅。

## 数据、修复与恢复

每个插件仍独立维护实例、配置、授权、任务与数据。
修复不改变来源；回滚恢复上一版本对应的完整来源，包括原 ZIP 的无远程来源。
来源绑定或主动切换 ref 也占用现有的一个上一版本记录，不提供完整来源历史。

ZIP 绑定 Git 后，旧备份仅在目标数据实例有对应绑定记录时允许跨此次来源差异恢复，并要求再次确认。
旧备份没有可验证的实例标识，用户必须确认它确实属于该插件原数据；此功能不允许跨 Git 仓库恢复。
保留数据卸载时保留绑定关系，卸载并清除数据时清除关系。代码回滚不撤销插件已写入的业务数据。

升级前备份数据库与插件目录。旧宿主使用作者提供的单插件 ZIP 或旧仓库标签；降级应恢复升级前快照。

## 管理接口

- `POST /api/plugins/repositories/discover`：`url`、`ref`；更新时携带 `pluginId` 和保存的 `path`。
- `POST /api/plugins/packages/discover`：multipart `file`，返回 `token`、`expires`、`candidates`。
- `POST /api/plugins/packages/inspect`：`token`、`path`、`pluginId`，返回现有安装票据及操作类型。
- `DELETE /api/plugins/packages/:token`：幂等释放当前用户的上传。
- `POST /api/plugins/inspect`：增加 `path`、`pluginId`、`commit`、`refKind`；使用发现响应固定的提交和类型。

`path` 省略表示自动选择唯一候选；显式 `""` 表示根插件。
旧单插件预检成功响应保持原字段；多插件来源返回 `PLUGIN_SELECTION_REQUIRED`。
预览 `operation` 为 `install`、`update`、`bindSource`、`unchanged`；修复继续使用显式 `repair: true`。
