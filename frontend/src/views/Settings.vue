<template>
  <div class="settings-page">
    <!-- 侧边菜单 -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <router-link to="/app" class="logo-link">
          <div class="logo">
            <svg viewBox="0 0 32 32" fill="none">
              <circle cx="16" cy="16" r="14" stroke="currentColor" stroke-width="1.5"/>
              <circle cx="16" cy="8" r="2" fill="currentColor"/>
              <circle cx="10" cy="20" r="2" fill="currentColor"/>
              <circle cx="22" cy="20" r="2" fill="currentColor"/>
              <path d="M16 10L10 18M16 10L22 18M10 20H22" stroke="currentColor" stroke-width="1.5"/>
            </svg>
          </div>
          <span class="logo-text">OntologyFlow</span>
        </router-link>
      </div>

      <nav class="settings-nav">
        <button
          v-for="item in menuItems"
          :key="item.id"
          class="nav-item"
          :class="{ active: activeMenu === item.id }"
          @click="activeMenu = item.id"
        >
          <span class="nav-icon" v-html="item.icon"></span>
          <span class="nav-label">{{ item.label }}</span>
        </button>
      </nav>

      <div class="sidebar-footer">
        <button class="nexus-btn nexus-btn-secondary btn-full" @click="$router.push('/app')">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 12H5M12 19l-7-7 7-7"/>
          </svg>
          返回
        </button>
      </div>
    </aside>

    <!-- 主内容 -->
    <main class="main-content">
      <!-- 模型配置 -->
      <div v-show="activeMenu === 'models'" class="content-section">
        <header class="section-header">
          <h1>AI 模型配置</h1>
          <p>配置您的 AI 模型 API 密钥，用于数据分析</p>
        </header>

        <div class="config-area">
          <div class="config-header">
            <h2>已配置模型</h2>
            <button class="nexus-btn nexus-btn-primary" @click="showAddDialog = true">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="12" y1="5" x2="12" y2="19"/>
                <line x1="5" y1="12" x2="19" y2="12"/>
              </svg>
              添加模型
            </button>
          </div>

          <div class="config-grid">
            <div v-for="config in configs" :key="config.id" class="config-card glass">
              <div class="card-header">
                <div class="model-icon" :class="config.model_name">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <circle cx="12" cy="12" r="3"/>
                    <path d="M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83"/>
                  </svg>
                </div>
                <div class="card-info">
                  <h3>{{ getModelLabel(config.model_name) }}</h3>
                  <span class="card-status" :class="{ active: config.is_active }">
                    {{ config.is_active ? '已启用' : '未启用' }}
                  </span>
                </div>
              </div>
              <div class="card-details">
                <div class="detail-row">
                  <span class="detail-label">模型名称</span>
                  <span class="detail-value">{{ config.model_id || '未设置' }}</span>
                </div>
                <div class="detail-row">
                  <span class="detail-label">API Key</span>
                  <span class="detail-value">{{ config.api_key ? maskApiKey(config.api_key) : '未设置' }}</span>
                </div>
                <div class="detail-row" v-if="config.api_endpoint">
                  <span class="detail-label">端点</span>
                  <span class="detail-value mono">{{ config.api_endpoint }}</span>
                </div>
              </div>
              <div class="card-actions">
                <button class="action-btn" @click="editConfig(config)">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002-2v-7"/>
                    <path d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z"/>
                  </svg>
                  编辑
                </button>
                <button class="action-btn danger" @click="deleteConfigHandler(config.id)">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <polyline points="3 6 5 6 21 6"/>
                    <path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/>
                  </svg>
                  删除
                </button>
              </div>
            </div>

            <div v-if="configs.length === 0" class="empty-state glass">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
                <circle cx="12" cy="12" r="3"/>
                <path d="M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83"/>
              </svg>
              <p>还没有配置任何模型</p>
              <button class="nexus-btn nexus-btn-primary" @click="showAddDialog = true">添加第一个模型</button>
            </div>
          </div>
        </div>
      </div>

      <!-- 账户设置 -->
      <div v-show="activeMenu === 'account'" class="content-section">
        <header class="section-header">
          <h1>账户设置</h1>
          <p>管理您的账户信息和安全设置</p>
        </header>

        <div class="settings-area">
          <!-- 默认模型 -->
          <div class="settings-card glass">
            <div class="card-title">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <circle cx="12" cy="12" r="3"/>
                <path d="M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83"/>
              </svg>
              <span>默认 AI 模型</span>
            </div>
            <div class="card-body">
              <select v-model="selectedModelId" class="nexus-input" @change="saveDefaultModel">
                <option :value="null">请选择模型</option>
                <option v-for="config in configs" :key="config.id" :value="config.id">
                  {{ getModelLabel(config.model_name) }}
                </option>
              </select>
              <p class="hint">选择分析数据时默认使用的 AI 模型</p>
            </div>
          </div>

          <!-- 修改密码 -->
          <div class="settings-card glass">
            <div class="card-title">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                <path d="M7 11V7a5 5 0 0110 0v4"/>
              </svg>
              <span>修改密码</span>
            </div>
            <div class="card-body">
              <div class="field">
                <label>当前密码</label>
                <input v-model="passwordForm.old_password" type="password" class="nexus-input" placeholder="输入当前密码" />
              </div>
              <div class="field">
                <label>新密码</label>
                <input v-model="passwordForm.new_password" type="password" class="nexus-input" placeholder="输入新密码" />
              </div>
              <div class="field">
                <label>确认新密码</label>
                <input v-model="passwordForm.confirm_password" type="password" class="nexus-input" placeholder="再次输入新密码" />
              </div>
              <button class="nexus-btn nexus-btn-primary" @click="changePassword" :disabled="changingPassword">
                {{ changingPassword ? '修改中...' : '修改密码' }}
              </button>
            </div>
          </div>

          <!-- 用户信息 -->
          <div class="settings-card glass">
            <div class="card-title">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/>
                <circle cx="12" cy="7" r="4"/>
              </svg>
              <span>个人信息</span>
            </div>
            <div class="card-body">
              <div class="field">
                <label>昵称</label>
                <input v-model="profileForm.nickname" class="nexus-input" placeholder="输入昵称" />
              </div>
              <div class="field">
                <label>邮箱</label>
                <input v-model="profileForm.email" class="nexus-input" disabled />
                <p class="hint">邮箱不可修改</p>
              </div>
              <button class="nexus-btn nexus-btn-primary" @click="updateProfile" :disabled="updatingProfile">
                {{ updatingProfile ? '保存中...' : '保存信息' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- 添加/编辑模型弹窗 -->
    <div v-if="showAddDialog" class="modal-overlay" @click.self="showAddDialog = false">
      <div class="modal glass">
        <div class="modal-header">
          <h2>{{ editingId ? '编辑配置' : '添加模型配置' }}</h2>
          <button class="modal-close" @click="closeDialog">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 6L6 18M6 6l12 12"/>
            </svg>
          </button>
        </div>
        <form @submit.prevent="saveConfig">
          <div class="field">
            <label>选择模型类型</label>
            <select v-model="configForm.model_name" class="nexus-input" required>
              <option value="">请选择模型</option>
              <option value="claude">Claude (Anthropic)</option>
              <option value="openai">GPT-4V / GPT-4o (OpenAI)</option>
              <option value="gemini">Gemini (Google)</option>
              <option value="glm">GLM-4V (智谱AI)</option>
              <option value="qwen">Qwen (阿里云/百炼)</option>
              <option value="deepseek">DeepSeek</option>
              <option value="local">本地模型</option>
            </select>
          </div>
          <div class="field">
            <label>模型名称 <span class="optional">(调用时使用的模型ID)</span></label>
            <input v-model="configForm.model_id" class="nexus-input" placeholder="例如: qwen-coding-plan, gpt-4o, claude-3-opus" />
            <p class="hint">百炼平台示例: qwen-coding-plan, qwen-turbo, qwen-max 等</p>
          </div>
          <div class="field">
            <label>API Key</label>
            <input v-model="configForm.api_key" type="password" class="nexus-input" :placeholder="editingId ? '留空则保持原有 Key 不变' : '输入 API Key'" @focus="isApiKeyModified = true" />
            <p v-if="editingId" class="hint" style="color: var(--neon-amber); font-size: 0.75rem;">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="display:inline;vertical-align:middle;margin-right:4px"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
              编辑模式下 API Key 不会回显，留空则保持原有密钥不变
            </p>
          </div>
          <div class="field">
            <label>自定义端点 <span class="optional">(可选)</span></label>
            <input v-model="configForm.api_endpoint" class="nexus-input" placeholder="例如: https://coding.dashscope.aliyuncs.com/v1" />
          </div>
          <div class="modal-actions">
            <button type="button" class="nexus-btn nexus-btn-secondary" @click="closeDialog">取消</button>
            <button type="submit" class="nexus-btn nexus-btn-primary" :disabled="saving">
              {{ saving ? '保存中...' : '保存' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getAIConfigs, createAIConfig, updateAIConfig, deleteAIConfig, type AIConfig } from '@/api/ai-configs'
import { getCurrentUser, updateUserInfo, type User } from '@/api/auth'
import api from '@/api'

const menuItems = [
  {
    id: 'models',
    label: '模型配置',
    icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="3"/><path d="M12 1v4M12 19v4M4.22 4.22l2.83 2.83M16.95 16.95l2.83 2.83"/></svg>'
  },
  {
    id: 'account',
    label: '账户设置',
    icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M20 21v-2a4 4 0 00-4-4H8a4 4 0 00-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>'
  }
]

const activeMenu = ref('models')
const configs = ref<AIConfig[]>([])
const selectedModelId = ref<number | null>(null)
const user = ref<User | null>(null)

// 模型配置
const showAddDialog = ref(false)
const saving = ref(false)
const editingId = ref<number | null>(null)
const configForm = reactive({
  model_name: '',
  model_id: '',
  api_key: '',
  api_endpoint: ''
})

// 记录编辑时是否修改了 API Key
const isApiKeyModified = ref(false)

// 密码表单
const passwordForm = reactive({
  old_password: '',
  new_password: '',
  confirm_password: ''
})
const changingPassword = ref(false)

// 个人信息表单
const profileForm = reactive({
  nickname: '',
  email: ''
})
const updatingProfile = ref(false)

const modelLabels: Record<string, string> = {
  claude: 'Claude',
  openai: 'GPT-4',
  gemini: 'Gemini',
  glm: 'GLM-4V',
  qwen: 'Qwen-VL',
  deepseek: 'DeepSeek',
  local: '本地模型'
}

const getModelLabel = (name: string) => modelLabels[name] || name

const maskApiKey = (key: string) => {
  if (!key || key.length < 8) return '••••••••'
  return key.slice(0, 4) + '••••••••' + key.slice(-4)
}

// 加载数据
const loadConfigs = async () => {
  try {
    configs.value = await getAIConfigs()
  } catch {
    ElMessage.error('加载配置失败')
  }
}

const loadUser = async () => {
  try {
    user.value = await getCurrentUser()
    profileForm.nickname = user.value.nickname || ''
    profileForm.email = user.value.email || ''
  } catch {
    ElMessage.error('加载用户信息失败')
  }
}

const loadSelectedModel = () => {
  const saved = localStorage.getItem('selectedModelId')
  if (saved) selectedModelId.value = Number(saved)
}

const saveDefaultModel = () => {
  if (selectedModelId.value) {
    localStorage.setItem('selectedModelId', String(selectedModelId.value))
    ElMessage.success('默认模型已保存')
  }
}

// 模型配置操作
const editConfig = (config: AIConfig) => {
  editingId.value = config.id
  configForm.model_name = config.model_name || ''
  configForm.model_id = config.model_id || ''
  configForm.api_key = ''  // 编辑时不回显 API Key，避免明文显示
  configForm.api_endpoint = config.api_endpoint || ''
  isApiKeyModified.value = false  // 重置标记
  showAddDialog.value = true
}

const saveConfig = async () => {
  if (!configForm.model_name) {
    ElMessage.warning('请选择模型')
    return
  }

  saving.value = true
  try {
    if (editingId.value) {
      // ===== 编辑模式 =====
      const data: any = {
        model_name: configForm.model_name.trim(),
        // model_id 和 api_endpoint 始终传递（空字符串转 null，后端会清空该字段）
        model_id: configForm.model_id.trim() || null,
        api_endpoint: configForm.api_endpoint.trim() || null,
      }
      // api_key 只有填写了新值才传递，留空 = 不修改原有密钥
      if (configForm.api_key.trim()) {
        data.api_key = configForm.api_key.trim()
      }
      await updateAIConfig(editingId.value, data)
      ElMessage.success('更新成功')
    } else {
      // ===== 新建模式 =====
      if (!configForm.api_key.trim()) {
        ElMessage.warning('请输入 API Key')
        saving.value = false
        return
      }
      const data: any = {
        model_name: configForm.model_name.trim(),
        api_key: configForm.api_key.trim(),
        model_id: configForm.model_id.trim() || null,
        api_endpoint: configForm.api_endpoint.trim() || null,
      }
      await createAIConfig(data)
      ElMessage.success('添加成功')
    }
    await loadConfigs()
    closeDialog()
  } catch (e: any) {
    console.error('保存配置失败:', e)
    ElMessage.error(e.response?.data?.detail || '保存失败，请检查输入信息')
  } finally {
    saving.value = false
  }
}

const deleteConfigHandler = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定删除此配置？', '确认', { type: 'warning' })
    await deleteAIConfig(id)
    ElMessage.success('删除成功')
    loadConfigs()
  } catch {}
}

const closeDialog = () => {
  showAddDialog.value = false
  editingId.value = null
  Object.assign(configForm, {
    model_name: '',
    model_id: '',
    api_key: '',
    api_endpoint: ''
  })
  isApiKeyModified.value = false
}

// 密码修改
const changePassword = async () => {
  if (!passwordForm.old_password || !passwordForm.new_password) {
    ElMessage.warning('请填写完整')
    return
  }
  if (passwordForm.new_password !== passwordForm.confirm_password) {
    ElMessage.warning('两次密码不一致')
    return
  }

  changingPassword.value = true
  try {
    await api.post('/auth/change-password', {
      old_password: passwordForm.old_password,
      new_password: passwordForm.new_password
    })
    ElMessage.success('密码修改成功')
    passwordForm.old_password = ''
    passwordForm.new_password = ''
    passwordForm.confirm_password = ''
  } catch (e: any) {
    ElMessage.error(e.response?.data?.detail || '修改失败')
  } finally {
    changingPassword.value = false
  }
}

// 更新个人信息
const updateProfile = async () => {
  updatingProfile.value = true
  try {
    await updateUserInfo({ nickname: profileForm.nickname })
    ElMessage.success('信息已更新')
  } catch {
    ElMessage.error('更新失败')
  } finally {
    updatingProfile.value = false
  }
}

onMounted(async () => {
  await Promise.all([loadConfigs(), loadUser()])
  loadSelectedModel()
})
</script>

<style scoped>
.settings-page {
  display: grid;
  grid-template-columns: 220px 1fr;
  min-height: 100vh;
  background: var(--bg-primary);
}

/* Sidebar */
.sidebar {
  background: var(--bg-secondary);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  padding: 1.5rem;
}

.sidebar-header {
  margin-bottom: 2rem;
}

.logo-link {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  text-decoration: none;
}

.logo {
  width: 32px;
  height: 32px;
  color: var(--neon-cyan);
}

.logo-text {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 1rem;
  font-weight: 600;
  color: var(--text-primary);
}

.settings-nav {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.875rem 1rem;
  background: transparent;
  border: none;
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
  text-align: left;
  width: 100%;
  font-size: 0.875rem;
}

.nav-item:hover {
  background: var(--bg-tertiary);
  color: var(--text-primary);
}

.nav-item.active {
  background: var(--neon-cyan-dim);
  color: var(--neon-cyan);
}

.sidebar-footer {
  margin-top: auto;
}

.btn-full {
  width: 100%;
  justify-content: center;
}

/* Main Content */
.main-content {
  padding: 2rem;
  overflow-y: auto;
}

.content-section {
  max-width: 900px;
}

.section-header {
  margin-bottom: 2rem;
}

.section-header h1 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.section-header p {
  color: var(--text-secondary);
  font-size: 0.9rem;
}

/* Config Area */
.config-area {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.config-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.config-header h2 {
  font-size: 1rem;
}

.config-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1rem;
}

.config-card {
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  transition: all var(--transition-fast);
}

.config-card:hover {
  border-color: var(--border-glow);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border-color);
}

.model-icon {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--neon-cyan-dim);
  color: var(--neon-cyan);
}

.model-icon.openai { background: rgba(0, 255, 136, 0.15); color: var(--neon-green); }
.model-icon.gemini { background: rgba(255, 0, 170, 0.15); color: var(--neon-magenta); }
.model-icon.glm { background: var(--neon-amber-dim); color: var(--neon-amber); }
.model-icon.qwen { background: rgba(255, 0, 170, 0.15); color: var(--neon-magenta); }
.model-icon.deepseek { background: var(--neon-cyan-dim); color: var(--neon-cyan); }
.model-icon.local { background: rgba(255, 255, 255, 0.1); color: var(--text-secondary); }

.card-info h3 {
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.card-status {
  font-size: 0.65rem;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  background: var(--bg-tertiary);
  color: var(--text-muted);
}

.card-status.active {
  background: rgba(0, 255, 136, 0.15);
  color: var(--neon-green);
}

.card-details {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
}

.detail-label {
  color: var(--text-muted);
}

.detail-value {
  color: var(--text-secondary);
}

.detail-value.mono {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
}

.card-actions {
  display: flex;
  gap: 0.5rem;
}

.action-btn {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.4rem;
  padding: 0.5rem;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
  font-size: 0.75rem;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.action-btn:hover {
  border-color: var(--neon-cyan);
  color: var(--neon-cyan);
}

.action-btn.danger:hover {
  border-color: var(--neon-magenta);
  color: var(--neon-magenta);
}

.empty-state {
  grid-column: 1 / -1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 3rem;
  text-align: center;
  color: var(--text-muted);
}

.empty-state svg {
  margin-bottom: 1rem;
  opacity: 0.5;
}

.empty-state p {
  margin-bottom: 1rem;
}

/* Settings Area */
.settings-area {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.settings-card {
  padding: 1.5rem;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.25rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border-color);
  font-weight: 600;
}

.card-title svg {
  color: var(--neon-cyan);
}

.card-body {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.field label {
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--text-secondary);
}

.hint {
  font-size: 0.75rem;
  color: var(--text-muted);
}

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.modal {
  width: 100%;
  max-width: 420px;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.modal-header h2 {
  font-size: 1.125rem;
}

.modal-close {
  background: transparent;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 0.25rem;
}

.modal-close:hover {
  color: var(--text-primary);
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
  margin-top: 1.5rem;
}

.optional {
  color: var(--text-muted);
  font-weight: 400;
}

/* Input */
.nexus-input {
  width: 100%;
  padding: 0.625rem 0.875rem;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  color: var(--text-primary);
  font-size: 0.875rem;
  transition: border-color var(--transition-fast);
}

.nexus-input:focus {
  border-color: var(--neon-cyan);
  outline: none;
}

.nexus-input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

@media (max-width: 768px) {
  .settings-page {
    grid-template-columns: 1fr;
  }

  .sidebar {
    display: none;
  }
}
</style>