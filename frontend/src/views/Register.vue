<template>
  <div class="auth-page">
    <div class="bg-effects">
      <div class="grid-overlay"></div>
      <div class="glow-orb amber"></div>
    </div>

    <div class="auth-container">
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
          <p class="brand-tagline">开始您的知识图谱之旅</p>
        </div>
      </div>

      <div class="auth-form-container">
        <div class="auth-form">
          <div class="form-header">
            <h2>创建账户</h2>
            <p>免费开始使用，探索数据价值</p>
          </div>

          <form @submit.prevent="handleRegister">
            <div class="form-group">
              <label>邮箱地址</label>
              <div class="input-wrapper">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <rect x="2" y="4" width="20" height="16" rx="2"/>
                  <path d="M22 6L12 13 2 6"/>
                </svg>
                <input v-model="form.email" type="email" placeholder="name@company.com" required />
              </div>
            </div>

            <div class="form-group">
              <label>昵称 <span class="optional">(可选)</span></label>
              <div class="input-wrapper">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <circle cx="12" cy="8" r="4"/>
                  <path d="M4 20c0-4 4-6 8-6s8 2 8 6"/>
                </svg>
                <input v-model="form.nickname" type="text" placeholder="您的昵称" />
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
                <input v-model="form.password" type="password" placeholder="至少6位字符" required />
              </div>
            </div>

            <div class="form-group">
              <label>确认密码</label>
              <div class="input-wrapper">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <rect x="3" y="11" width="18" height="11" rx="2"/>
                  <circle cx="12" cy="16" r="1"/>
                  <path d="M7 11V7a5 5 0 0110 0v4"/>
                </svg>
                <input v-model="form.confirmPassword" type="password" placeholder="再次输入密码" required />
              </div>
            </div>

            <div class="form-options">
              <label class="checkbox-wrapper">
                <input type="checkbox" v-model="agreeTerms" required />
                <span class="checkmark"></span>
                <span>我同意 <a href="#">服务条款</a></span>
              </label>
            </div>

            <button type="submit" class="nexus-btn nexus-btn-amber btn-full" :disabled="loading">
              <span v-if="!loading">创建账户</span>
              <span v-else class="loading-spinner"></span>
            </button>
          </form>

          <div class="form-footer">
            <span>已有账户?</span>
            <router-link to="/login">立即登录</router-link>
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
import { register } from '@/api/auth'

const router = useRouter()
const loading = ref(false)
const agreeTerms = ref(false)

const form = reactive({
  email: '',
  password: '',
  confirmPassword: '',
  nickname: ''
})

const handleRegister = async () => {
  if (form.password !== form.confirmPassword) {
    ElMessage.error('两次密码输入不一致')
    return
  }
  if (!agreeTerms.value) {
    ElMessage.warning('请同意服务条款')
    return
  }

  loading.value = true
  try {
    await register({
      email: form.email,
      password: form.password,
      nickname: form.nickname || undefined
    })
    ElMessage.success('注册成功，请登录')
    router.push('/login')
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '注册失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.optional {
  color: var(--text-muted);
  font-weight: 400;
}

.glow-orb.amber {
  background: radial-gradient(circle, var(--neon-amber) 0%, transparent 70%);
}

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

.auth-brand {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4rem;
  background: linear-gradient(135deg, rgba(255, 184, 0, 0.05) 0%, transparent 100%);
  border-right: 1px solid var(--border-color);
}

.brand-content {
  text-align: center;
}

.logo-large {
  width: 100px;
  height: 100px;
  margin: 0 auto 2rem;
  color: var(--neon-amber);
  filter: drop-shadow(0 0 20px rgba(255, 184, 0, 0.4));
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
}

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
  border-color: var(--neon-amber);
  box-shadow: 0 0 0 3px rgba(255, 184, 0, 0.15);
}

.form-options {
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
  background: var(--neon-amber);
  border-color: var(--neon-amber);
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

.form-footer {
  text-align: center;
  font-size: 0.875rem;
  color: var(--text-secondary);
  margin-top: 1.5rem;
}

.form-footer a {
  color: var(--neon-amber);
  margin-left: 0.25rem;
}

@media (max-width: 900px) {
  .auth-container {
    grid-template-columns: 1fr;
  }
  .auth-brand {
    display: none;
  }
}
</style>