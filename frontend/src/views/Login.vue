<template>
  <div class="auth-page">
    <!-- 背景效果 -->
    <div class="bg-effects">
      <div class="grid-overlay"></div>
      <div class="glow-orb"></div>
    </div>

    <div class="auth-container">
      <!-- 左侧品牌区 -->
      <div class="auth-brand">
        <div class="brand-content">
          <div class="logo-large">
            <svg viewBox="0 0 64 64" fill="none">
              <circle cx="32" cy="32" r="28" stroke="currentColor" stroke-width="1.5"/>
              <circle cx="32" cy="18" r="4" fill="currentColor"/>
              <circle cx="18" cy="42" r="4" fill="currentColor"/>
              <circle cx="46" cy="42" r="4" fill="currentColor"/>
              <path d="M32 22L18 38M32 22L46 38M18 42H46" stroke="currentColor" stroke-width="2"/>
            </svg>
          </div>
          <h1>OntologyFlow</h1>
          <p class="brand-tagline">本体关系分析平台</p>
          <div class="brand-features">
            <div class="feature-item">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"/>
              </svg>
              <span>多模态数据输入</span>
            </div>
            <div class="feature-item">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"/>
              </svg>
              <span>AI 智能分析</span>
            </div>
            <div class="feature-item">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"/>
              </svg>
              <span>交互式图谱编辑</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧登录表单 -->
      <div class="auth-form-container">
        <div class="auth-form">
          <div class="form-header">
            <h2>欢迎回来</h2>
            <p>登录您的账户继续探索</p>
          </div>

          <form @submit.prevent="handleLogin">
            <div class="form-group">
              <label>邮箱地址</label>
              <div class="input-wrapper">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <rect x="2" y="4" width="20" height="16" rx="2"/>
                  <path d="M22 6L12 13 2 6"/>
                </svg>
                <input
                  v-model="form.email"
                  type="email"
                  placeholder="name@company.com"
                  required
                />
              </div>
            </div>

            <div class="form-group">
              <label>密码</label>
              <div class="input-wrapper">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <rect x="3" y="11" width="18" height="11" rx="2"/>
                  <circle cx="12" cy="16" r="1"/>
                  <path d="M7 11V7a5 5 0 0110 0v4"/>
                </svg>
                <input
                  v-model="form.password"
                  type="password"
                  placeholder="••••••••"
                  required
                />
              </div>
            </div>

            <div class="form-options">
              <label class="checkbox-wrapper">
                <input type="checkbox" v-model="rememberMe" />
                <span class="checkmark"></span>
                <span>记住我</span>
              </label>
              <a href="#" class="forgot-link">忘记密码?</a>
            </div>

            <button type="submit" class="nexus-btn nexus-btn-primary btn-full" :disabled="loading">
              <span v-if="!loading">登录</span>
              <span v-else class="loading-spinner"></span>
            </button>
          </form>

          <div class="form-divider">
            <span>或</span>
          </div>

          <div class="oauth-buttons">
            <button class="nexus-btn nexus-btn-secondary btn-full">
              <svg width="20" height="20" viewBox="0 0 24 24">
                <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
              </svg>
              使用 Google 登录
            </button>
          </div>

          <div class="form-footer">
            <span>还没有账户?</span>
            <router-link to="/register">立即注册</router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { login } from '@/api/auth'

const router = useRouter()
const loading = ref(false)
const rememberMe = ref(false)

const form = reactive({
  email: 'test@test.com',
  password: '123456'
})

const handleLogin = async () => {
  loading.value = true
  try {
    const res = await login(form)
    localStorage.setItem('token', res.access_token)
    ElMessage.success('登录成功')
    router.push('/app')
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '登录失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  background: var(--bg-primary);
  position: relative;
  overflow: hidden;
}

.bg-effects {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.grid-overlay {
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(0, 217, 255, 0.02) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 217, 255, 0.02) 1px, transparent 1px);
  background-size: 50px 50px;
}

.glow-orb {
  position: absolute;
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, var(--neon-cyan) 0%, transparent 70%);
  filter: blur(120px);
  opacity: 0.15;
  top: -200px;
  right: -100px;
}

.auth-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  min-height: 100vh;
  position: relative;
  z-index: 1;
}

/* 左侧品牌区 */
.auth-brand {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4rem;
  background: linear-gradient(135deg, rgba(0, 217, 255, 0.05) 0%, transparent 100%);
  border-right: 1px solid var(--border-color);
}

.brand-content {
  text-align: center;
}

.logo-large {
  width: 100px;
  height: 100px;
  margin: 0 auto 2rem;
  color: var(--neon-cyan);
  filter: drop-shadow(0 0 20px var(--neon-cyan-glow));
}

.auth-brand h1 {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  letter-spacing: -0.02em;
}

.brand-tagline {
  font-size: 1.125rem;
  color: var(--text-secondary);
  margin-bottom: 3rem;
}

.brand-features {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: var(--text-secondary);
  font-size: 0.95rem;
}

.feature-item svg {
  color: var(--neon-cyan);
}

/* 右侧表单区 */
.auth-form-container {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
}

.auth-form {
  width: 100%;
  max-width: 400px;
}

.form-header {
  margin-bottom: 2rem;
}

.form-header h2 {
  font-size: 1.75rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.form-header p {
  color: var(--text-secondary);
}

.form-group {
  margin-bottom: 1.25rem;
}

.form-group label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-secondary);
  margin-bottom: 0.5rem;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-wrapper svg {
  position: absolute;
  left: 1rem;
  color: var(--text-muted);
  pointer-events: none;
}

.input-wrapper input {
  width: 100%;
  padding: 0.875rem 1rem 0.875rem 3rem;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  color: var(--text-primary);
  font-size: 0.95rem;
  transition: all var(--transition-fast);
}

.input-wrapper input::placeholder {
  color: var(--text-muted);
}

.input-wrapper input:focus {
  outline: none;
  border-color: var(--neon-cyan);
  box-shadow: 0 0 0 3px var(--neon-cyan-dim);
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.checkbox-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: var(--text-secondary);
  cursor: pointer;
}

.checkbox-wrapper input {
  display: none;
}

.checkmark {
  width: 18px;
  height: 18px;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  position: relative;
  transition: all var(--transition-fast);
}

.checkbox-wrapper input:checked + .checkmark {
  background: var(--neon-cyan);
  border-color: var(--neon-cyan);
}

.checkbox-wrapper input:checked + .checkmark::after {
  content: '';
  position: absolute;
  left: 5px;
  top: 2px;
  width: 5px;
  height: 9px;
  border: solid var(--bg-primary);
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}

.forgot-link {
  font-size: 0.875rem;
  color: var(--neon-cyan);
}

.btn-full {
  width: 100%;
  padding: 1rem;
  font-size: 1rem;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid transparent;
  border-top-color: currentColor;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.form-divider {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin: 1.5rem 0;
  color: var(--text-muted);
  font-size: 0.875rem;
}

.form-divider::before,
.form-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--border-color);
}

.oauth-buttons {
  margin-bottom: 1.5rem;
}

.form-footer {
  text-align: center;
  font-size: 0.875rem;
  color: var(--text-secondary);
}

.form-footer a {
  color: var(--neon-cyan);
  margin-left: 0.25rem;
}

/* 响应式 */
@media (max-width: 900px) {
  .auth-container {
    grid-template-columns: 1fr;
  }

  .auth-brand {
    display: none;
  }
}
</style>