---
layout: home

hero:
  name: MediaTidy
  text: 全自动媒体库管理工具
  tagline: 深度集成 115 网盘 / CloudDrive2 / Emby，从文件整理到直链播放的一站式解决方案
  image:
    src: /media-tidy-promo.png
    alt: MediaTidy 用户端与中心端宣传图
  actions:
    - theme: brand
      text: 快速开始
      link: /guide/beginner
    - theme: alt
      text: 功能介绍
      link: /features/organize
    - theme: alt
      text: 官方群组
      link: https://t.me/MediaTidy_Offical

features:
  - icon: 🎬
    title: 自动整理
    details: 基于 TMDB 自动识别电影/电视剧，按规范命名和目录结构整理，支持洗版升级和多维度质量评分
  - icon: 📄
    title: STRM 生成
    details: 将云端视频生成 .strm 文件供 Emby/Jellyfin 直接播放，支持 Webhook/监听/轮询实时触发，并可联动神医 FF 缓存
  - icon: ⚡
    title: FF 缓存
    details: 复用整理 FFprobe 与 STRM 神医媒体源结果，加速自动整理和库内媒体信息恢复
  - icon: 🖥️
    title: Emby 反向代理
    details: 内嵌反向代理引擎，302 重定向直链播放 + 预缓存 + 转码回落，自动 HTTPS 证书管理
  - icon: 📁
    title: 文件管理
    details: Web 文件浏览器，统一虚拟路径系统，多 115 账号 + 通用挂载点统一管理
  - icon: 🛡️
    title: 115 风控对抗
    details: 内置 OCR 验证码自动识别，风控检测→自动破解→解除拦截全流程自动化
  - icon: ⚙️
    title: 规则引擎
    details: 灵活的分类/命名/质量规则，支持可视化编辑和远程订阅同步
  - icon: 📊
    title: 仪表盘 & 通知
    details: 实时任务进度、历史统计、系统监控，支持 Telegram Bot 和 Webhook 通知
  - icon: 🎨
    title: 海报卡片
    details: 整理完成后生成精美海报通知卡片，支持自定义字体和样式
---

<section class="home-promo">
  <img src="/media-tidy-promo.png" alt="MediaTidy 用户端与中心端，全能媒体管理解决方案" />
</section>

<style scoped>
.home-promo {
  max-width: 1120px;
  margin: 16px auto 0;
  padding: 0 24px 48px;
}

.home-promo img {
  display: block;
  width: 100%;
  height: auto;
  border: 1px solid var(--vp-c-divider);
  border-radius: 12px;
  box-shadow: 0 24px 60px rgba(0, 0, 0, 0.18);
}

@media (max-width: 640px) {
  .home-promo {
    padding: 0 16px 32px;
  }

  .home-promo img {
    border-radius: 8px;
  }
}
</style>
