<template>
  <div class="home-page">
    <!-- 动态背景 -->
    <div class="bg-effects">
      <div class="grid-overlay"></div>
      <div class="glow-orb orb-1"></div>
      <div class="glow-orb orb-2"></div>
      <div class="glow-orb orb-3"></div>
    </div>

    <!-- 导航栏 -->
    <nav class="nav-bar glass">
      <div class="nav-brand">
        <div class="logo-icon">
          <svg viewBox="0 0 32 32" fill="none">
            <circle cx="16" cy="16" r="14" stroke="currentColor" stroke-width="1.5"/>
            <circle cx="16" cy="8" r="2" fill="currentColor"/>
            <circle cx="10" cy="20" r="2" fill="currentColor"/>
            <circle cx="22" cy="20" r="2" fill="currentColor"/>
            <path d="M16 10L10 18M16 10L22 18M10 20H22" stroke="currentColor" stroke-width="1.5"/>
          </svg>
        </div>
        <span class="brand-text">OntologyFlow</span>
      </div>
      <div class="nav-actions">
        <button class="nexus-btn nexus-btn-secondary" @click="$router.push('/login')">
          登录
        </button>
        <button class="nexus-btn nexus-btn-primary" @click="$router.push('/login')">
          开始使用
        </button>
      </div>
    </nav>

    <!-- 主内容 -->
    <main class="hero-section">
      <div class="hero-content">
        <div class="hero-tag">
          <span class="tag-dot"></span>
          本体关系分析平台
        </div>
        <h1 class="hero-title">
          <span class="title-line">从数据中</span>
          <span class="title-line highlight">提取知识图谱</span>
        </h1>
        <p class="hero-desc">
          上传图片、视频、文本，AI 自动识别实体与关系，
          <br />构建可视化知识图谱，洞察数据背后的关联
        </p>
        <div class="hero-actions">
          <button class="nexus-btn nexus-btn-primary btn-lg" @click="$router.push('/register')">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M5 12h14M12 5l7 7-7 7"/>
            </svg>
            免费开始
          </button>
          <button class="nexus-btn nexus-btn-secondary btn-lg">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <polygon points="5 3 19 12 5 21 5 3"/>
            </svg>
            观看演示
          </button>
        </div>
      </div>

      <!-- 右侧图谱预览 -->
      <div class="hero-visual">
        <div class="graph-preview glass">
          <div class="graph-header">
            <div class="graph-dots">
              <span></span><span></span><span></span>
            </div>
            <span class="graph-title">数据血缘图谱</span>
          </div>
          <div class="graph-canvas">
            <div class="node node-1">
              <span>用户行为</span>
            </div>
            <div class="node node-2">
              <span>转化漏斗</span>
            </div>
            <div class="node node-3">
              <span>数据清洗</span>
            </div>
            <div class="node node-4">
              <span>特征工程</span>
            </div>
            <div class="node node-5">
              <span>模型训练</span>
            </div>
            <svg class="edges" viewBox="0 0 300 200">
              <path class="edge" d="M60,50 Q100,30 140,50" />
              <path class="edge" d="M60,50 Q30,100 60,150" />
              <path class="edge" d="M140,50 Q200,50 240,80" />
              <path class="edge" d="M60,150 Q150,150 240,120" />
              <path class="edge" d="M240,80 L240,120" />
            </svg>
          </div>
        </div>
      </div>
    </main>

    <!-- 特性区域 -->
    <section class="features-section">
      <div class="feature-card glass">
        <div class="feature-icon">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <rect x="3" y="3" width="18" height="18" rx="2"/>
            <circle cx="8.5" cy="8.5" r="1.5"/>
            <path d="M21 15l-5-5L5 21"/>
          </svg>
        </div>
        <h3>多模态输入</h3>
        <p>支持图片、视频、文本多种数据格式，自动识别内容</p>
      </div>
      <div class="feature-card glass">
        <div class="feature-icon amber">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <path d="M12 2L2 7l10 5 10-5-10-5z"/>
            <path d="M2 17l10 5 10-5"/>
            <path d="M2 12l10 5 10-5"/>
          </svg>
        </div>
        <h3>多模型支持</h3>
        <p>Claude、GPT、Gemini、GLM、Qwen 等主流大模型</p>
      </div>
      <div class="feature-card glass">
        <div class="feature-icon green">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
            <circle cx="12" cy="12" r="10"/>
            <circle cx="12" cy="12" r="4"/>
            <path d="M12 2v4M12 18v4M2 12h4M18 12h4"/>
          </svg>
        </div>
        <h3>交互式编辑</h3>
        <p>可视化图谱编辑，拖拽调整，实时保存</p>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
</script>

<style scoped>
.home-page {
  min-height: 100vh;
  background: var(--bg-primary);
  position: relative;
  overflow-x: hidden;
}

/* 背景效果 */
.bg-effects {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}

.grid-overlay {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(0, 217, 255, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 217, 255, 0.03) 1px, transparent 1px);
  background-size: 60px 60px;
}

.glow-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  opacity: 0.4;
}

.orb-1 {
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, var(--neon-cyan) 0%, transparent 70%);
  top: -200px;
  right: -100px;
  animation: float 8s ease-in-out infinite;
}

.orb-2 {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, var(--neon-amber) 0%, transparent 70%);
  bottom: -100px;
  left: -100px;
  animation: float 10s ease-in-out infinite reverse;
}

.orb-3 {
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, var(--neon-magenta) 0%, transparent 70%);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  opacity: 0.2;
}

/* 导航栏 */
.nav-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 72px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 3rem;
  z-index: 100;
  background: rgba(10, 15, 26, 0.8);
  border-bottom: 1px solid var(--border-color);
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.logo-icon {
  width: 36px;
  height: 36px;
  color: var(--neon-cyan);
}

.brand-text {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
  letter-spacing: -0.02em;
}

.nav-actions {
  display: flex;
  gap: 0.75rem;
}

/* 主内容区 */
.hero-section {
  position: relative;
  z-index: 1;
  min-height: 100vh;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  padding: 8rem 4rem 4rem;
  max-width: 1400px;
  margin: 0 auto;
}

.hero-content {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.hero-tag {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: var(--neon-cyan-dim);
  border: 1px solid rgba(0, 217, 255, 0.3);
  border-radius: 999px;
  font-size: 0.875rem;
  color: var(--neon-cyan);
  margin-bottom: 1.5rem;
  width: fit-content;
}

.tag-dot {
  width: 6px;
  height: 6px;
  background: var(--neon-cyan);
  border-radius: 50%;
  animation: pulse-glow 2s ease-in-out infinite;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 700;
  line-height: 1.1;
  margin-bottom: 1.5rem;
  letter-spacing: -0.03em;
}

.title-line {
  display: block;
}

.title-line.highlight {
  background: linear-gradient(135deg, var(--neon-cyan) 0%, var(--neon-amber) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-desc {
  font-size: 1.125rem;
  color: var(--text-secondary);
  margin-bottom: 2rem;
  line-height: 1.7;
}

.hero-actions {
  display: flex;
  gap: 1rem;
}

.btn-lg {
  padding: 1rem 2rem;
  font-size: 1rem;
}

/* 图谱预览 */
.hero-visual {
  display: flex;
  align-items: center;
  justify-content: center;
}

.graph-preview {
  width: 100%;
  max-width: 480px;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-lg), 0 0 60px rgba(0, 217, 255, 0.1);
}

.graph-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem 1.25rem;
  background: rgba(0, 0, 0, 0.3);
  border-bottom: 1px solid var(--border-color);
}

.graph-dots {
  display: flex;
  gap: 6px;
}

.graph-dots span {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--text-muted);
}

.graph-dots span:first-child { background: #ff5f57; }
.graph-dots span:nth-child(2) { background: #ffbd2e; }
.graph-dots span:last-child { background: #28c840; }

.graph-title {
  font-size: 0.8rem;
  color: var(--text-secondary);
}

.graph-canvas {
  position: relative;
  height: 280px;
  padding: 2rem;
}

.node {
  position: absolute;
  padding: 0.5rem 1rem;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  font-size: 0.75rem;
  color: var(--text-primary);
  white-space: nowrap;
  animation: float 4s ease-in-out infinite;
}

.node-1 { top: 20px; left: 10px; animation-delay: 0s; }
.node-2 { top: 20px; left: 130px; animation-delay: 0.5s; }
.node-3 { top: 120px; left: 10px; animation-delay: 1s; }
.node-4 { top: 50px; right: 30px; animation-delay: 1.5s; }
.node-5 { top: 140px; right: 30px; animation-delay: 2s; }

.node:hover {
  border-color: var(--neon-cyan);
  box-shadow: 0 0 20px var(--neon-cyan-dim);
}

.edges {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.edge {
  fill: none;
  stroke: var(--neon-cyan);
  stroke-width: 1.5;
  stroke-dasharray: 4 2;
  opacity: 0.6;
  animation: dash 20s linear infinite;
}

@keyframes dash {
  to { stroke-dashoffset: -100; }
}

/* 特性区域 */
.features-section {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
  padding: 4rem;
  max-width: 1200px;
  margin: 0 auto;
}

.feature-card {
  padding: 2rem;
  text-align: center;
  transition: all var(--transition-normal);
}

.feature-card:hover {
  transform: translateY(-4px);
  border-color: var(--neon-cyan);
  box-shadow: var(--shadow-glow);
}

.feature-icon {
  width: 56px;
  height: 56px;
  margin: 0 auto 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--neon-cyan-dim);
  border-radius: var(--radius-md);
  color: var(--neon-cyan);
}

.feature-icon.amber {
  background: var(--neon-amber-dim);
  color: var(--neon-amber);
}

.feature-icon.green {
  background: rgba(0, 255, 136, 0.15);
  color: var(--neon-green);
}

.feature-icon svg {
  width: 28px;
  height: 28px;
}

.feature-card h3 {
  font-size: 1.125rem;
  margin-bottom: 0.5rem;
}

.feature-card p {
  font-size: 0.875rem;
  color: var(--text-secondary);
}

/* 响应式 */
@media (max-width: 1024px) {
  .hero-section {
    grid-template-columns: 1fr;
    text-align: center;
    padding: 6rem 2rem 2rem;
  }

  .hero-title {
    font-size: 2.5rem;
  }

  .hero-actions {
    justify-content: center;
  }

  .hero-visual {
    display: none;
  }

  .features-section {
    grid-template-columns: 1fr;
    padding: 2rem;
  }
}
</style>