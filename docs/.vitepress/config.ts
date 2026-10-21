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
      { text: '指南', link: '/guide/mt-manual', activeMatch: '/guide/' },
      { text: '功能', link: '/features/organize', activeMatch: '/features/' },
      { text: '配置', link: '/config/drive', activeMatch: '/config/' },
      { text: '插件与开发', link: '/plugins/', activeMatch: '/plugins/' },
      { text: 'FAQ', link: '/faq' },
      { text: '官方群组', link: 'https://t.me/MediaTidy_Offical' },
      { text: '联系作者', link: 'https://t.me/murongyun574_bot' },
    ],

    sidebar: {
      '/plugins/': [
        {
          text: '插件中心',
          items: [
            { text: '文档首页', link: '/plugins/' },
            { text: '用户指南', link: '/plugins/user-guide' },
            { text: '下载开发 Skill', link: '/plugins/downloads' },
          ],
        },
        {
          text: 'SDK v2 开发',
          items: [
            { text: '开发入门', link: '/plugins/getting-started' },
            { text: '完整能力清单', link: '/plugins/capabilities' },
            { text: '业务接口', link: '/plugins/business' },
            { text: '权限与 FF 保护', link: '/plugins/permissions' },
            { text: '定时、队列与完成事件', link: '/plugins/automation' },
            { text: '存储与数据管理', link: '/plugins/storage' },
            { text: '页面协议与 Logo', link: '/plugins/ui' },
            { text: '开发工具与发布', link: '/plugins/tooling' },
            { text: '验证记录与限制', link: '/plugins/validation' },
          ],
        },
      ],
      '/guide/': [
        {
          text: '入门指南',
          items: [
            { text: 'MT 入门使用手册', link: '/guide/mt-manual' },
            { text: '分享洗版教程', link: '/guide/share-manual' },
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
            { text: '插件中心', link: '/plugins/' },
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
      { icon: 'github', link: 'https://github.com/MuRongYun8/MediaTidy-Wiki' },
    ],

    footer: {
      message: 'MediaTidy - 全自动媒体库管理工具',
      copyright: 'Copyright © 2025 MuRongYun8',
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
