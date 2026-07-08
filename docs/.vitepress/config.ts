import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'MediaTidy',
  description: 'MediaTidy 官方文档 - 全自动媒体库管理工具',
  lang: 'zh-CN',
  base: '/MediaTidy-Wiki/',
  head: [
    ['link', { rel: 'icon', href: '/MediaTidy-Wiki/favicon.ico' }],
  ],

  themeConfig: {
    logo: '/logo.png',
    siteTitle: 'MediaTidy',

    nav: [
      { text: '指南', link: '/guide/beginner', activeMatch: '/guide/' },
      { text: '功能', link: '/features/organize', activeMatch: '/features/' },
      { text: '配置', link: '/config/drive', activeMatch: '/config/' },
      { text: 'FAQ', link: '/faq' },
      { text: '官方群组', link: 'https://t.me/MediaTidy_Offical' },
      { text: '联系作者', link: 'https://t.me/mhchat1_bot' },
    ],

    sidebar: {
      '/guide/': [
        {
          text: '入门指南',
          items: [
            { text: 'MT 入门使用手册', link: '/guide/mt-manual' },
            { text: '新手须知', link: '/guide/beginner' },
            { text: '快速开始', link: '/guide/quick-start' },
            { text: '前置条件', link: '/guide/prerequisites' },
            { text: '升级指南', link: '/guide/upgrade' },
          ],
        },
      ],
      '/features/': [
        {
          text: '媒体管理',
          items: [
            { text: '自动整理', link: '/features/organize' },
            { text: 'STRM 生成', link: '/features/strm' },
            { text: '文件管理', link: '/features/file-manager' },
          ],
        },
        {
          text: 'Emby 集成',
          items: [
            { text: 'Emby 反向代理', link: '/features/emby-proxy' },
          ],
        },
        {
          text: '规则与策略',
          items: [
            { text: '规则引擎', link: '/features/rules' },
          ],
        },
        {
          text: '系统功能',
          items: [
            { text: '仪表盘与工具箱', link: '/features/dashboard' },
            { text: 'TMDB 缓存管理', link: '/features/tmdb-cache' },
            { text: 'FF 缓存', link: '/features/ff-cache-server' },
          ],
        },
        {
          text: '辅助功能',
          items: [
            { text: '通知服务', link: '/features/notification' },
            { text: '115 风控对抗', link: '/features/risk-control' },
          ],
        },
      ],
      '/config/': [
        {
          text: '配置参考',
          items: [
            { text: '网盘配置', link: '/config/drive' },
            { text: 'Emby 配置', link: '/config/emby' },
            { text: '系统设置', link: '/config/system' },
            { text: '环境变量', link: '/config/env' },
          ],
        },
      ],
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com/JieWSOFT/MediaTidy-Wiki' },
    ],

    footer: {
      message: 'MediaTidy - 全自动媒体库管理工具',
      copyright: 'Copyright © 2025 JieWSOFT',
    },

    outline: {
      label: '页面导航',
      level: [2, 3],
    },

    docFooter: {
      prev: '上一篇',
      next: '下一篇',
    },

    lastUpdated: {
      text: '最后更新于',
    },

    search: {
      provider: 'local',
      options: {
        translations: {
          button: { buttonText: '搜索文档', buttonAriaLabel: '搜索' },
          modal: {
            noResultsText: '没有找到结果',
            resetButtonTitle: '清除查询条件',
            footer: { selectText: '选择', navigateText: '切换', closeText: '关闭' },
          },
        },
      },
    },
  },
})
