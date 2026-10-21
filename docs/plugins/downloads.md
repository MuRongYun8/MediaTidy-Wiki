# 开发 Skill 下载与使用

[下载 mediatidy-plugin-development 2.0.0 完整 ZIP](/downloads/mediatidy-plugin-development-2.0.0.zip)

MT「插件中心」内的「下载开发 Skill 完整包」通过当前 MT 直接下载同版本文件，不依赖访问文档站。官方 Wiki 的下载内容由同一份源码生成。

## 包内内容

```text
README.md
mediatidy-plugin-development/
  SKILL.md
  agents/openai.yaml
  references/
    index.d.ts
    ui-schema.d.ts
    capabilities.md
    business.md
    automation.md
    storage.md
    permissions.md
    ui.md
    getting-started.md
    tooling.md
    ...其他同版本说明
```

包含完整 Skill、SDK v2 文档、业务与 UI 类型；不是单独一份 SKILL.md，也不是可直接安装到 MT 的插件。包中没有账号、密钥、用户目录、平台运行器或模型配置。

## 导入 AI 开发工具

1. 解压 ZIP，保留完整 `mediatidy-plugin-development` 目录。
2. Codex 用户可将该目录复制到 `~/.codex/skills/`，重新打开会话后使用 `$mediatidy-plugin-development`。其他工具按其 Skill 导入方式操作，也可直接让 AI 读取目录内的 `SKILL.md`。
3. 告诉 AI 要实现的功能、可用目录和允许的业务操作，要求使用 SDK v2 的真实类型，并完成清单、Goja 和页面验证。

示例需求：

```text
使用 mediatidy-plugin-development Skill 开发一个目录清单插件。
只申请授权目录的读取权限。后台扫描完成后保存结果，页面支持搜索、分页和跨页选择。
不要启用定时、执行真实云盘操作、发送外部通知或发布仓库。
```

Skill 不会自动安装开发依赖或 MT 插件，也不代表用户已授予任何目录、任务或网络权限。

## SDK 开发环境

CLI、模拟 SDK、通用示例和独立预览属于 SDK 开发包。参照[工具与验证](tooling.md)准备同版本工具及匹配平台的 Goja 运行器，再按[开发入门](getting-started.md)编写、测试和打包。Skill ZIP 提供指导与类型，不包含平台二进制，不替代开发环境安装。

MT 只安装已经打包的插件资源，不执行仓库安装、构建或迁移脚本。请勿上传开发 Skill ZIP 到 MT 的插件安装入口。
