---
layout: page
---

<main class="mt-home">
  <section class="mt-hero">
    <div class="mt-hero-inner">
      <div class="mt-hero-copy">
        <div class="mt-kicker">Go Powered Media Automation</div>
        <h1>Go 语言驱动的<br>极速媒体管理引擎</h1>
        <p class="mt-lead">为大规模媒体库打造的高性能自动化系统。深度集成 115 网盘、CloudDrive2、Emby、STRM 与 FF 缓存服务器，让整理、缓存、生成和播放链路都快起来。</p>
        <div class="mt-actions">
          <a class="mt-button mt-button-primary" href="/MediaTidy-Wiki/guide/beginner.html">新手部署</a>
          <a class="mt-button mt-button-secondary" href="/MediaTidy-Wiki/features/organize.html">功能介绍</a>
          <a class="mt-button mt-button-ghost" href="https://t.me/MediaTidy_Offical">官方群组</a>
        </div>
        <div class="mt-tags" aria-label="核心能力">
          <span>Go 高性能</span>
          <span>CD2 gRPC</span>
          <span>高速 STRM</span>
          <span>FF 缓存服务器</span>
          <span>Emby 反代</span>
        </div>
      </div>
      <div class="mt-hero-visual">
        <div class="mt-screen">
          <img src="/media-tidy-promo.png" alt="MediaTidy 用户端与中心端，全能媒体管理解决方案" />
        </div>
      </div>
    </div>
  </section>

  <section class="mt-performance" aria-label="性能优势">
    <a class="mt-perf-card mt-perf-primary" href="/MediaTidy-Wiki/features/ff-cache-server.html">
      <span>FF CACHE SERVER</span>
      <strong>FF 缓存服务器</strong>
      <p>集中复用 FFprobe、TMDB 与神医媒体源结果，大批量整理、STRM 重建、Emby 迁移时减少重复解析。</p>
    </a>
    <a class="mt-perf-card" href="/MediaTidy-Wiki/guide/prerequisites.html">
      <span>BUILT WITH GO</span>
      <strong>Go 高性能架构</strong>
      <p>并发任务队列、gRPC 文件访问、低资源占用，面向 NAS 与服务器长时间稳定运行。</p>
    </a>
    <a class="mt-perf-card" href="/MediaTidy-Wiki/features/strm.html">
      <span>115 FAST PATH</span>
      <strong>115 高速 STRM</strong>
      <p>115 高速穿透生成播放链路，直连播放地址与 Emby / Jellyfin 媒体库自然衔接。</p>
    </a>
  </section>

  <section class="mt-section">
    <div class="mt-section-head">
      <p>Core Engine</p>
      <h2>为大规模媒体库而生的高性能引擎</h2>
    </div>
    <div class="mt-feature-grid">
      <a class="mt-feature" href="/MediaTidy-Wiki/features/organize.html">
        <span>01</span>
        <h3>自动整理</h3>
        <p>基于 TMDB 识别电影与电视剧，自动命名、归档、分类，并支持洗版升级和质量评分。</p>
      </a>
      <a class="mt-feature" href="/MediaTidy-Wiki/features/strm.html">
        <span>02</span>
        <h3>STRM 生成</h3>
        <p>将云端视频生成 .strm 文件供 Emby / Jellyfin 播放，支持定时、监听、轮询和 Webhook。</p>
      </a>
      <a class="mt-feature" href="/MediaTidy-Wiki/features/ff-cache-server.html">
        <span>03</span>
        <h3>FF 缓存服务器</h3>
        <p>复用 FFprobe、TMDB 与神医媒体源结果，减少重复解析，让大规模媒体库恢复和重建更快。</p>
      </a>
      <a class="mt-feature" href="/MediaTidy-Wiki/features/emby-proxy.html">
        <span>04</span>
        <h3>Emby 反向代理</h3>
        <p>302 直链播放、预缓存、转码回落与 Webhook 联动，降低播放链路的维护成本。</p>
      </a>
      <a class="mt-feature" href="/MediaTidy-Wiki/features/file-manager.html">
        <span>05</span>
        <h3>文件管理</h3>
        <p>统一虚拟路径，多 115 账号和通用挂载点集中管理，目录浏览与文件操作更直观。</p>
      </a>
      <a class="mt-feature" href="/MediaTidy-Wiki/features/rules.html">
        <span>06</span>
        <h3>规则引擎</h3>
        <p>分类、命名、质量评分规则可视化配置，支持订阅同步，适配不同媒体库习惯。</p>
      </a>
    </div>
  </section>

  <section class="mt-dashboard">
    <div class="mt-dashboard-copy">
      <p>Dashboard</p>
      <h2>状态、任务、缓存和服务运行情况一眼看清</h2>
      <a href="/MediaTidy-Wiki/features/dashboard.html">查看仪表盘能力</a>
    </div>
    <img src="/media-tidy-dashboard.png" alt="MediaTidy 仪表盘与应用缓存管理" />
  </section>

  <section class="mt-quickstart">
    <div>
      <p>Beginner Guide</p>
      <h2>第一次部署，从这里开始</h2>
      <span>按步骤完成 Docker 部署、CD2、115、路径映射、自动整理、STRM 和 Emby 接入。</span>
    </div>
    <a class="mt-button mt-button-primary" href="/MediaTidy-Wiki/guide/beginner.html">打开新手须知</a>
  </section>
</main>

<style>
:root {
  --mt-bg: #080b12;
  --mt-panel: #111722;
  --mt-panel-2: #151b27;
  --mt-line: rgba(150, 175, 215, 0.18);
  --mt-text: #f4f7fb;
  --mt-muted: #9aa7b8;
  --mt-blue: #55b8ff;
  --mt-cyan: #9f7cff;
  --mt-amber: #f6bf45;
  --mt-pink: #d565ff;
  --mt-purple: #a879ff;
}

body:has(.mt-home) .VPDoc {
  padding: 0 !important;
}

body:has(.mt-home) .VPDoc .container,
body:has(.mt-home) .VPDoc .content,
body:has(.mt-home) .VPDoc .content-container {
  max-width: none !important;
  padding: 0 !important;
}

body:has(.mt-home) .VPNavBar {
  border-bottom: 1px solid rgba(150, 175, 215, 0.14) !important;
  background: rgba(8, 11, 18, 0.88) !important;
  backdrop-filter: blur(18px);
}

body:has(.mt-home) .VPNavBar .title,
body:has(.mt-home) .VPNavBarMenuLink,
body:has(.mt-home) .VPNavBarMenuGroup .button {
  color: rgba(244, 247, 251, 0.92) !important;
}

body:has(.mt-home) .VPNavBarMenuLink:hover,
body:has(.mt-home) .VPNavBarMenuGroup .button:hover {
  color: #fff !important;
}

body:has(.mt-home) .VPNavBarSearch .DocSearch-Button,
body:has(.mt-home) .VPNavBarSearch .DocSearch-Button:hover {
  border: 1px solid rgba(150, 175, 215, 0.16);
  background: rgba(255, 255, 255, 0.06);
}

body:has(.mt-home) .VPNavBarSearch .DocSearch-Button-Placeholder,
body:has(.mt-home) .VPNavBarSearch .DocSearch-Button-Key {
  color: rgba(244, 247, 251, 0.72);
}

.mt-home {
  min-height: 100vh;
  margin: 0;
  background:
    radial-gradient(circle at 18% 12%, rgba(168, 121, 255, 0.22), transparent 28%),
    radial-gradient(circle at 74% 18%, rgba(122, 101, 255, 0.2), transparent 34%),
    radial-gradient(circle at 92% 42%, rgba(213, 101, 255, 0.18), transparent 28%),
    linear-gradient(180deg, rgba(12, 16, 24, 0.52) 0%, var(--mt-bg) 500px),
    linear-gradient(135deg, #080712 0%, #120d22 44%, #090712 100%);
  color: var(--mt-text);
}

.mt-hero {
  overflow: hidden;
  border-bottom: 1px solid var(--mt-line);
  position: relative;
}

.mt-hero::before {
  content: "";
  position: absolute;
  inset: 0;
  pointer-events: none;
  background-image:
    linear-gradient(rgba(85, 184, 255, 0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(85, 184, 255, 0.05) 1px, transparent 1px);
  background-size: 72px 72px;
  mask-image: linear-gradient(180deg, rgba(0, 0, 0, 0.62), transparent 78%);
}

.mt-hero-inner {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: minmax(390px, 0.82fr) minmax(560px, 1.18fr);
  gap: 40px;
  align-items: center;
  max-width: 1440px;
  min-height: 720px;
  margin: 0 auto;
  padding: 92px 40px 72px;
}

.mt-kicker,
.mt-section-head p,
.mt-dashboard-copy p,
.mt-quickstart p {
  margin: 0 0 16px;
  color: var(--mt-purple);
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0;
  text-transform: uppercase;
}

.mt-hero h1 {
  margin: 0;
  color: var(--mt-text);
  font-size: 64px;
  line-height: 1.04;
  font-weight: 850;
  text-shadow: 0 0 34px rgba(85, 184, 255, 0.18);
}

.mt-lead {
  max-width: 620px;
  margin: 28px 0 0;
  color: var(--mt-muted);
  font-size: 19px;
  line-height: 1.8;
}

.mt-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 36px;
}

.mt-button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 46px;
  padding: 0 20px;
  border: 1px solid var(--mt-line);
  border-radius: 8px;
  color: var(--mt-text);
  font-size: 15px;
  font-weight: 700;
  text-decoration: none;
  transition: transform 0.2s ease, border-color 0.2s ease, background 0.2s ease;
}

.mt-button:hover {
  transform: translateY(-2px);
  text-decoration: none;
}

.mt-button-primary {
  border-color: transparent;
  background: linear-gradient(135deg, #7b61ff, #d565ff);
  color: #fff;
  box-shadow: 0 14px 34px rgba(168, 121, 255, 0.28);
}

.mt-button-secondary {
  background: rgba(255, 255, 255, 0.08);
}

.mt-button-ghost {
  color: var(--mt-muted);
}

.mt-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 28px;
}

.mt-tags span {
  padding: 7px 10px;
  border: 1px solid rgba(168, 121, 255, 0.3);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.04);
  color: #c9d5e6;
  font-size: 13px;
}

.mt-hero-visual {
  min-width: 0;
}

.mt-screen {
  position: relative;
  width: min(820px, 100%);
  margin-left: auto;
  border: 1px solid rgba(124, 153, 255, 0.34);
  border-radius: 8px;
  background: #050814;
  box-shadow: 0 32px 120px rgba(123, 97, 255, 0.3), 0 18px 56px rgba(0, 0, 0, 0.48), 0 0 0 1px rgba(213, 101, 255, 0.12);
}

.mt-screen::before {
  content: "";
  position: absolute;
  inset: -1px;
  border-radius: inherit;
  background: linear-gradient(135deg, rgba(123, 97, 255, 0.38), rgba(246, 191, 69, 0.16), rgba(213, 101, 255, 0.34));
  opacity: 0.56;
  z-index: 0;
}

.mt-screen img {
  position: relative;
  z-index: 1;
  display: block;
  width: 100%;
  height: auto;
  border-radius: 8px;
}

.mt-performance {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
  max-width: 1180px;
  margin: -54px auto 0;
  padding: 0 24px;
  position: relative;
  z-index: 2;
}

.mt-perf-card {
  position: relative;
  min-height: 188px;
  overflow: hidden;
  padding: 26px;
  border: 1px solid rgba(150, 175, 215, 0.18);
  border-radius: 8px;
  background:
    linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.025)),
    rgba(11, 17, 27, 0.9);
  color: inherit;
  text-decoration: none;
  box-shadow: 0 24px 72px rgba(0, 0, 0, 0.26);
  transition: transform 0.2s ease, border-color 0.2s ease, background 0.2s ease;
}

.mt-perf-card::before {
  content: "";
  position: absolute;
  inset: -60% -20% auto auto;
  width: 220px;
  height: 220px;
  border-radius: 999px;
  background: rgba(85, 184, 255, 0.16);
  filter: blur(4px);
}

.mt-perf-card:hover {
  transform: translateY(-5px);
  border-color: rgba(168, 121, 255, 0.48);
  text-decoration: none;
}

.mt-perf-primary {
  border-color: rgba(168, 121, 255, 0.4);
  background:
    linear-gradient(135deg, rgba(168, 121, 255, 0.18), rgba(85, 184, 255, 0.08)),
    rgba(9, 16, 25, 0.94);
}

.mt-perf-card span {
  display: block;
  color: var(--mt-amber);
  font-size: 12px;
  font-weight: 850;
  letter-spacing: 0;
}

.mt-perf-card strong {
  display: block;
  margin-top: 18px;
  color: var(--mt-text);
  font-size: 25px;
  line-height: 1.25;
}

.mt-perf-card p {
  margin: 16px 0 0;
  color: var(--mt-muted);
  font-size: 15px;
  line-height: 1.75;
}

.mt-section {
  max-width: 1180px;
  margin: 0 auto;
  padding: 86px 24px 48px;
}

.mt-section-head {
  display: flex;
  align-items: end;
  justify-content: space-between;
  gap: 32px;
  margin-bottom: 30px;
}

.mt-section-head h2,
.mt-dashboard-copy h2,
.mt-quickstart h2 {
  margin: 0;
  color: var(--mt-text);
  font-size: 44px;
  line-height: 1.2;
}

.mt-feature-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 14px;
}

.mt-feature {
  min-height: 230px;
  padding: 24px;
  border: 1px solid rgba(150, 175, 215, 0.16);
  border-radius: 8px;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.06), rgba(255, 255, 255, 0.025)),
    rgba(11, 16, 24, 0.78);
  color: inherit;
  text-decoration: none;
  transition: transform 0.2s ease, border-color 0.2s ease, background 0.2s ease;
}

.mt-feature:hover {
  transform: translateY(-4px);
  border-color: rgba(85, 184, 255, 0.48);
  background: linear-gradient(180deg, rgba(85, 184, 255, 0.12), rgba(255, 255, 255, 0.03));
  text-decoration: none;
}

.mt-feature span {
  color: var(--mt-amber);
  font-size: 13px;
  font-weight: 800;
}

.mt-feature h3 {
  margin: 18px 0 0;
  color: var(--mt-text);
  font-size: 22px;
}

.mt-feature p {
  margin: 14px 0 0;
  color: var(--mt-muted);
  font-size: 15px;
  line-height: 1.8;
}

.mt-dashboard {
  display: grid;
  grid-template-columns: 0.72fr 1.28fr;
  gap: 36px;
  align-items: center;
  max-width: 1180px;
  margin: 32px auto 0;
  padding: 32px;
  border: 1px solid var(--mt-line);
  border-radius: 8px;
  background: linear-gradient(135deg, rgba(21, 27, 39, 0.94), rgba(9, 14, 24, 0.94));
}

.mt-dashboard-copy a {
  display: inline-flex;
  margin-top: 28px;
  color: var(--mt-cyan);
  font-weight: 700;
  text-decoration: none;
}

.mt-dashboard img {
  display: block;
  width: 100%;
  border: 1px solid var(--mt-line);
  border-radius: 8px;
}

.mt-quickstart {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 28px;
  max-width: 1180px;
  margin: 32px auto 0;
  padding: 40px 32px 72px;
}

.mt-quickstart span {
  display: block;
  max-width: 720px;
  margin-top: 14px;
  color: var(--mt-muted);
  font-size: 17px;
  line-height: 1.7;
}

@media (max-width: 1100px) {
  .mt-hero-inner {
    grid-template-columns: 1fr;
    min-height: auto;
  }

  .mt-screen {
    width: 100%;
  }

  .mt-performance,
  .mt-feature-grid,
  .mt-dashboard {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .mt-performance {
    margin-top: 0;
  }
}

@media (max-width: 720px) {
  body:has(.mt-home) .VPNavBar {
    height: 64px !important;
  }

  body:has(.mt-home) .VPNavBar .container {
    height: 64px !important;
  }

  body:has(.mt-home) .VPNavBarSearch .DocSearch-Button {
    width: 42px !important;
    height: 42px !important;
    border-radius: 8px !important;
    padding: 0 !important;
  }

  body:has(.mt-home) .VPNavBarSearch .DocSearch-Button-Placeholder,
  body:has(.mt-home) .VPNavBarSearch .DocSearch-Button-Key {
    display: none !important;
  }

  body:has(.mt-home) .VPNavBarHamburger .container {
    top: 50% !important;
    transform: translateY(-50%) !important;
  }

  .mt-hero-inner {
    padding: 72px 18px 44px;
  }

  .mt-hero h1 {
    font-size: 44px;
  }

  .mt-lead {
    font-size: 17px;
  }

  .mt-performance,
  .mt-feature-grid,
  .mt-dashboard {
    grid-template-columns: 1fr;
  }

  .mt-performance {
    margin: 0;
    padding: 0 18px;
  }

  .mt-section,
  .mt-dashboard,
  .mt-quickstart {
    margin-left: 18px;
    margin-right: 18px;
    padding-left: 0;
    padding-right: 0;
  }

  .mt-section-head,
  .mt-quickstart {
    display: block;
  }

  .mt-section-head h2,
  .mt-dashboard-copy h2,
  .mt-quickstart h2 {
    font-size: 30px;
  }

  .mt-quickstart .mt-button {
    margin-top: 24px;
  }
}
</style>
