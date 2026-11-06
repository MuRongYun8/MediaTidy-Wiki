# 两插件集合发布示例

本目录提供集合索引。先用现有 SDK 分别构建 `starter` 与 `examples/storage-table`，
然后把生成的运行包合并为集合。不要直接上传这个只有索引的目录。

从 `plugin-sdk` 目录运行（Python 3.12，PowerShell）：

```powershell
python -m mt_plugin pack --root starter --output dist/collection-parts/inventory.zip
python -m mt_plugin pack --root examples/storage-table --output dist/collection-parts/storage-table.zip
python -m zipfile -e dist/collection-parts/inventory.zip dist/collection/inventory
python -m zipfile -e dist/collection-parts/storage-table.zip dist/collection/storage-table
Copy-Item examples/collection/plugins.json dist/collection/plugins.json
python -m zipfile -c dist/example-collection.zip dist/collection
```

使用新的输出目录运行，避免上次构建残留文件进入集合。生成结果：

```text
collection/
  plugins.json
  inventory/      # 独立目录清单插件
  storage-table/  # 独立合成数据存储插件
```

上传 `dist/example-collection.zip`，依次选择两个插件。目录清单插件需要显式授权目录；
存储示例只使用合成数据。两者都可以保持停用来验收安装流程。
Git 发布时将 `dist/collection` 的内容作为发布仓库根目录提交。
旧版宿主继续使用 `dist/collection-parts` 中的单插件 ZIP。

完整规则见 [多插件仓库与 ZIP](/plugins/collections.md)。
