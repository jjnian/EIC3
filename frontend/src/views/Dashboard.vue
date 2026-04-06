<template>
  <div class="app-layout">
    <!-- 左侧菜单 -->
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="logo">
          <svg viewBox="0 0 32 32" fill="none">
            <circle cx="16" cy="16" r="14" stroke="currentColor" stroke-width="1.5"/>
            <circle cx="16" cy="8" r="2" fill="currentColor"/>
            <circle cx="10" cy="20" r="2" fill="currentColor"/>
            <circle cx="22" cy="20" r="2" fill="currentColor"/>
            <path d="M16 10L10 18M16 10L22 18M10 20H22" stroke="currentColor" stroke-width="1.5"/>
          </svg>
        </div>
        <span class="brand">OntologyFlow</span>
      </div>

      <nav class="menu-nav">
        <button
          v-for="item in menuItems"
          :key="item.id"
          class="menu-item"
          :class="{ active: activeMenu === item.id }"
          @click="handleMenuClick(item.id)"
        >
          <span class="menu-icon" v-html="item.icon"></span>
          <span class="menu-label">{{ item.label }}</span>
        </button>
      </nav>

      <div class="sidebar-footer">
        <div class="user-info">
          <div class="user-avatar">{{ user?.nickname?.[0] || user?.email?.[0] || 'U' }}</div>
          <div class="user-details">
            <span class="user-name">{{ user?.nickname || user?.email }}</span>
          </div>
          <button class="settings-btn" @click="$router.push('/settings')" title="设置">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <circle cx="12" cy="12" r="3"/>
              <path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-2 2 2 2 0 01-2-2v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 01-2-2 2 2 0 012-2h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06a1.65 1.65 0 001.82.33H9a1.65 1.65 0 001-1.51V3a2 2 0 012-2 2 2 0 012 2v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9a1.65 1.65 0 001.51 1H21a2 2 0 012 2 2 2 0 01-2 2h-.09a1.65 1.65 0 00-1.51 1z"/>
            </svg>
          </button>
          <button class="logout-btn" @click="logout" title="退出">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M9 21H5a2 2 0 01-2-2V5a2 2 0 012-2h4"/>
              <polyline points="16 17 21 12 16 7"/>
              <line x1="21" y1="12" x2="9" y2="12"/>
            </svg>
          </button>
        </div>
      </div>
    </aside>

    <!-- 主内容区 -->
    <main class="main-content">
      <!-- 数据血缘页面 -->
      <div v-if="activeMenu === 'lineage'" class="lineage-page">
        <header class="page-header">
          <h1>数据血缘</h1>
          <div class="header-controls">
            <select v-model="selectedModelId" class="nexus-select" @change="saveSelectedModel">
              <option :value="null">选择 AI 模型</option>
              <option v-for="config in aiConfigs" :key="config.id" :value="config.id">
                {{ config.model_name }}{{ config.model_id ? ' (' + config.model_id + ')' : '' }}
              </option>
            </select>
          </div>
        </header>

        <!-- 对话框区域 -->
        <div class="chat-container">
          <!-- 消息列表 -->
          <div class="messages-area" ref="messagesContainer">
            <div v-if="messages.length === 0" class="welcome">
              <div class="welcome-icon">
                <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
                  <circle cx="12" cy="12" r="3"/>
                  <circle cx="19" cy="5" r="2"/>
                  <circle cx="5" cy="19" r="2"/>
                  <circle cx="19" cy="19" r="2"/>
                  <path d="M14.5 10.5L17 7M9.5 13.5L7 16M14.5 13.5L17 16M9.5 10.5L7 7"/>
                </svg>
              </div>
              <h2>输入文字或上传文件</h2>
              <p>AI 将自动提取实体与关系，构建知识图谱</p>
            </div>

            <div
              v-for="msg in messages"
              :key="msg.id"
              class="message"
              :class="msg.role"
            >
              <div class="message-avatar">
                <span v-if="msg.role === 'user'">{{ user?.nickname?.[0] || 'U' }}</span>
                <svg v-else width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                  <circle cx="12" cy="12" r="3"/>
                  <circle cx="19" cy="5" r="2"/>
                  <circle cx="5" cy="19" r="2"/>
                  <path d="M14.5 10.5L17 7M9.5 13.5L7 16"/>
                </svg>
              </div>
              <div class="message-content">
                <!-- 用户消息 -->
                <template v-if="msg.role === 'user'">
                  <div v-if="msg.content" class="text-bubble">{{ msg.content }}</div>
                  <div v-if="msg.file_url" class="file-preview">
                    <img v-if="msg.file_type === 'image'" :src="msg.file_url" />
                    <video v-else-if="msg.file_type === 'video'" :src="msg.file_url" controls></video>
                    <div v-else class="file-icon">
                      <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                        <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
                        <polyline points="14 2 14 8 20 8"/>
                      </svg>
                      <span>{{ msg.file_name }}</span>
                    </div>
                  </div>
                </template>

                <!-- AI 消息 -->
                <template v-else>
                  <div v-if="msg.status === 'analyzing'" class="analyzing">
                    <span class="dot"></span>
                    <span class="dot"></span>
                    <span class="dot"></span>
                    <span>正在分析中...</span>
                  </div>
                  <div v-else-if="msg.status === 'cancelled'" class="cancelled-bubble">
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <circle cx="12" cy="12" r="10"/>
                      <path d="M15 9l-6 6M9 9l6 6"/>
                    </svg>
                    <span>分析已取消</span>
                  </div>
                  <template v-else-if="msg.status === 'completed'">
                    <div class="result-section">
                      <div class="result-header">
                        <span class="result-title">分析结果</span>
                        <span class="result-stats">
                          {{ msg.entities?.length || 0 }} 实体 · {{ msg.relations?.length || 0 }} 关系
                        </span>
                      </div>

                      <!-- 图谱 -->
                      <div class="graph-section">
                        <div :id="'graph-' + msg.id" class="graph-canvas"></div>
                      </div>

                      <!-- 实体列表 -->
                      <div class="entities-section" v-if="msg.entities?.length">
                        <div class="section-title" @click="toggleExpand(msg.id)">
                          <span>实体列表</span>
                          <svg :class="{ expanded: expandedSet.has(msg.id) }" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="6 9 12 15 18 9"/>
                          </svg>
                        </div>
                        <div class="section-content" v-show="expandedSet.has(msg.id)">
                          <span v-for="entity in msg.entities" :key="entity.id" class="entity-tag" :class="entity.type">
                            {{ entity.name }}
                            <small v-if="entity.type">({{ entity.type }})</small>
                          </span>
                        </div>
                      </div>

                      <!-- 关系列表 -->
                      <div class="relations-section" v-if="msg.relations?.length">
                        <div class="section-title" @click="toggleExpand('rel-' + msg.id)">
                          <span>关系列表</span>
                          <svg :class="{ expanded: expandedSet.has('rel-' + msg.id) }" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <polyline points="6 9 12 15 18 9"/>
                          </svg>
                        </div>
                        <div class="section-content" v-show="expandedSet.has('rel-' + msg.id)">
                          <div v-for="rel in msg.relations" :key="rel.id" class="relation-item">
                            <span class="rel-source">{{ rel.source }}</span>
                            <span class="rel-type">{{ rel.type || '关联' }}</span>
                            <span class="rel-target">{{ rel.target }}</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </template>
                  <div v-else-if="msg.status === 'failed'" class="error-bubble">
                    分析失败: {{ msg.error }}
                  </div>
                </template>
              </div>
            </div>
          </div>

          <!-- 输入区域 -->
          <div class="input-area">
            <div class="input-box glass">
              <div class="input-actions">
                <button class="action-btn" @click="triggerUpload()" title="上传图片">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <rect x="3" y="3" width="18" height="18" rx="2"/>
                    <circle cx="8.5" cy="8.5" r="1.5"/>
                    <path d="M21 15l-5-5L5 21"/>
                  </svg>
                </button>
                <button class="action-btn" @click="triggerUpload()" title="上传视频">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <polygon points="5 3 19 12 5 21 5 3"/>
                  </svg>
                </button>
                <button class="action-btn" @click="triggerUpload()" title="上传文件">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
                    <polyline points="14 2 14 8 20 8"/>
                  </svg>
                </button>
              </div>
              <input
                v-model="inputText"
                type="text"
                placeholder="输入文字或上传文件进行分析..."
                @keyup.enter="sendMessage"
              />
              <button v-if="!isAnalyzing" class="send-btn" @click="sendMessage" :disabled="!canSend">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <line x1="22" y1="2" x2="11" y2="13"/>
                  <polygon points="22 2 15 22 11 13 2 9 22 2"/>
                </svg>
              </button>
              <button v-else class="stop-btn-input" @click="cancelCurrentAnalysis" title="停止分析">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <rect x="6" y="6" width="12" height="12" rx="1"/>
                </svg>
              </button>
            </div>
            <input ref="fileInput" type="file" accept="image/*,video/*,.txt,.md,.pdf" @change="handleFileSelect" hidden />
          </div>
        </div>
      </div>

      <!-- 其他菜单占位 -->
      <div v-else class="placeholder-page">
        <div class="placeholder-content">
          <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
            <rect x="3" y="3" width="18" height="18" rx="2"/>
            <path d="M3 9h18M9 21V9"/>
          </svg>
          <h2>{{ currentMenuLabel }}</h2>
          <p>功能开发中...</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Graph } from '@antv/x6'
import axios from 'axios'
import { getAIConfigs, type AIConfig } from '@/api/ai-configs'
import { getCurrentUser, type User } from '@/api/auth'

interface Message {
  id: number
  role: 'user' | 'assistant'
  content?: string
  file_url?: string
  file_type?: string
  file_name?: string
  status?: string
  entities?: any[]
  relations?: any[]
  error?: string
}

const router = useRouter()
const token = localStorage.getItem('token') || ''

// 菜单配置
const menuItems = [
  {
    id: 'lineage',
    label: '数据血缘',
    icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="3"/><circle cx="19" cy="5" r="2"/><circle cx="5" cy="19" r="2"/><circle cx="19" cy="19" r="2"/><path d="M14.5 10.5L17 7M9.5 13.5L7 16M14.5 13.5L17 16M9.5 10.5L7 7"/></svg>'
  },
  {
    id: 'chat',
    label: '对话分析',
    icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M21 15a2 2 0 01-2 2H7l-4 4V5a2 2 0 012-2h14a2 2 0 012 2z"/></svg>'
  },
]

const activeMenu = ref('lineage')
const currentMenuLabel = computed(() => {
  const item = menuItems.find(m => m.id === activeMenu.value)
  return item?.label || ''
})

const user = ref<User | null>(null)
const aiConfigs = ref<AIConfig[]>([])
const selectedModelId = ref<number | null>(null)

const messages = ref<Message[]>([])
const expandedSet = ref(new Set<string | number>())
const inputText = ref('')
const isAnalyzing = ref(false)
const pendingFile = ref<File | null>(null)
const messagesContainer = ref<HTMLElement | null>(null)
const fileInput = ref<HTMLInputElement | null>(null)
const abortController = ref<AbortController | null>(null)

const canSend = computed(() => inputText.value.trim() || pendingFile.value)

// 初始化
onMounted(async () => {
  await Promise.all([loadUser(), loadAIConfigs()])
})

const loadUser = async () => {
  try { user.value = await getCurrentUser() }
  catch { router.push('/login') }
}

const loadAIConfigs = async () => {
  try {
    aiConfigs.value = await getAIConfigs()
    const saved = localStorage.getItem('selectedModelId')
    if (saved) selectedModelId.value = Number(saved)
  } catch (e) { console.error(e) }
}

// 发送消息
const sendMessage = async () => {
  if (!canSend.value || isAnalyzing.value) return
  if (!selectedModelId.value) {
    ElMessage.warning('请先在页面上方选择 AI 模型')
    return
  }

  const userMsg: Message = {
    id: Date.now(),
    role: 'user',
    content: pendingFile.value ? '' : inputText.value,
  }

  // 处理文件：直接读取为 base64，不通过项目系统上传
  let fileBase64 = ''
  let fileType = ''
  let fileName = ''
  if (pendingFile.value) {
    const file = pendingFile.value
    fileName = file.name
    fileType = file.type.startsWith('image') ? 'image' : file.type.startsWith('video') ? 'video' : 'text'

    try {
      // 文本文件直接读内容；图片/视频转 base64
      if (fileType === 'text') {
        const text = await file.text()
        userMsg.content = text
        userMsg.file_name = fileName
      } else {
        const buffer = await file.arrayBuffer()
        fileBase64 = btoa(String.fromCharCode(...new Uint8Array(buffer)))
        userMsg.file_type = fileType
        userMsg.file_name = fileName
        // 图片创建预览 URL
        if (fileType === 'image') {
          userMsg.file_url = URL.createObjectURL(file)
        }
      }
    } catch {
      ElMessage.error('文件读取失败')
      return
    }
    pendingFile.value = null
  }

  messages.value.push(userMsg)
  inputText.value = ''
  scrollToBottom()

  // AI 消息
  const aiMsg: Message = {
    id: Date.now() + 1,
    role: 'assistant',
    content: '',
    status: 'analyzing'
  }
  messages.value.push(aiMsg)
  isAnalyzing.value = true
  scrollToBottom()

  // 创建 CancelToken
  const cancelSource = axios.CancelToken.source()
  abortController.value = cancelSource as any

  try {
    const formData = new FormData()
    formData.append('content', userMsg.content || '')
    // 如果是非文本文件，将 base64 内容和类型一并发送
    if (fileBase64) {
      formData.append('file_base64', fileBase64)
      formData.append('file_type', fileType)
    }
    formData.append('ai_config_id', String(selectedModelId.value))

    const res = await axios.post('/api/analyze', formData, {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'multipart/form-data'
      },
      cancelToken: cancelSource.token,
      timeout: 120000
    })

    aiMsg.status = 'completed'
    aiMsg.entities = res.data.entities
    aiMsg.relations = res.data.relations

    nextTick(() => renderGraph(aiMsg.id, res.data.entities, res.data.relations))
  } catch (e: any) {
    if (axios.isCancel(e)) {
      aiMsg.status = 'cancelled'
    } else {
      aiMsg.status = 'failed'
      aiMsg.error = e.response?.data?.detail || e.message || '分析失败'
    }
  } finally {
    isAnalyzing.value = false
    abortController.value = null
    scrollToBottom()
  }
}

// 取消当前分析
const cancelCurrentAnalysis = () => {
  if (abortController.value) {
    (abortController.value as any).cancel('用户取消')
  }
  // 找到最后一个 analyzing 状态的消息并更新
  const lastAnalyzing = [...messages.value].reverse().find(m => m.status === 'analyzing')
  if (lastAnalyzing) {
    lastAnalyzing.status = 'cancelled'
  }
  isAnalyzing.value = false
}

// 渲染图谱
const renderGraph = (msgId: number, entities: any[], relations: any[]) => {
  const container = document.getElementById(`graph-${msgId}`)
  if (!container || !entities?.length) return

  const width = container.offsetWidth || 500
  const cols = Math.floor(width / 130)

  const graph = new Graph({
    container,
    width,
    height: Math.max(200, Math.ceil(entities.length / cols) * 70 + 40),
    grid: { visible: true, attrs: { stroke: 'rgba(0, 217, 255, 0.05)' } },
    panning: true,
    background: { color: 'var(--bg-tertiary)' }
  })

  entities.forEach((entity, i) => {
    graph.addNode({
      id: String(entity.id || i),
      shape: 'rect',
      x: 20 + (i % cols) * 130,
      y: 20 + Math.floor(i / cols) * 60,
      width: 110,
      height: 40,
      attrs: {
        body: { fill: '#0d1424', stroke: '#00d9ff', strokeWidth: 1, rx: 6 },
        label: { text: entity.name, fill: '#e8edf5', fontSize: 11 }
      }
    })
  })

  const nameToId = new Map(entities.map((e, i) => [e.name, e.id || i]))
  relations?.forEach(rel => {
    const sourceId = String(rel.source_entity_id || nameToId.get(rel.source))
    const targetId = String(rel.target_entity_id || nameToId.get(rel.target))
    if (sourceId && targetId) {
      graph.addEdge({
        source: sourceId,
        target: targetId,
        attrs: { line: { stroke: '#ffb800', strokeWidth: 1.5 } },
        labels: [{ attrs: { text: { text: rel.type || '', fill: '#8a9bb8', fontSize: 10 } } }]
      })
    }
  })
}

const toggleExpand = (key: string | number) => {
  if (expandedSet.value.has(key)) {
    expandedSet.value.delete(key)
  } else {
    expandedSet.value.add(key)
  }
}

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

// 文件处理
const triggerUpload = () => {
  fileInput.value?.click()
}

const handleFileSelect = (e: Event) => {
  const files = (e.target as HTMLInputElement).files
  if (files?.length) {
    pendingFile.value = files[0]
    inputText.value = `📎 ${files[0].name}`
  }
}

const saveSelectedModel = () => {
  if (selectedModelId.value) {
    localStorage.setItem('selectedModelId', String(selectedModelId.value))
  }
}

const logout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}

const handleMenuClick = (menuId: string) => {
  if (menuId === 'chat') {
    router.push('/chat')
  } else {
    activeMenu.value = menuId
  }
}
</script>

<style scoped>
.app-layout {
  display: grid;
  grid-template-columns: 200px 1fr;
  height: 100vh;
  background: var(--bg-primary);
}

/* 侧边栏 */
.sidebar {
  background: var(--bg-secondary);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1.25rem;
  border-bottom: 1px solid var(--border-color);
}

.logo {
  width: 28px;
  height: 28px;
  color: var(--neon-cyan);
}

.brand {
  font-family: 'Space Grotesk', sans-serif;
  font-size: 0.95rem;
  font-weight: 600;
}

.menu-nav {
  flex: 1;
  padding: 0.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.menu-item {
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

.menu-item:hover {
  background: var(--bg-tertiary);
  color: var(--text-primary);
}

.menu-item.active {
  background: var(--neon-cyan-dim);
  color: var(--neon-cyan);
}

.menu-icon :deep(svg) {
  stroke: currentColor;
}

.sidebar-footer {
  padding: 1rem;
  border-top: 1px solid var(--border-color);
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.user-avatar {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, var(--neon-cyan), var(--neon-amber));
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--bg-primary);
}

.user-details {
  flex: 1;
  min-width: 0;
}

.user-name {
  font-size: 0.8rem;
  color: var(--text-secondary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.logout-btn {
  background: transparent;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 0.25rem;
  transition: color var(--transition-fast);
}

.logout-btn:hover {
  color: var(--neon-magenta);
}

.settings-btn {
  background: transparent;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 0.25rem;
  transition: color var(--transition-fast);
}

.settings-btn:hover {
  color: var(--neon-cyan);
}

/* 主内容 */
.main-content {
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.lineage-page {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-color);
}

.page-header h1 {
  font-size: 1.125rem;
  font-weight: 600;
}

.nexus-select {
  padding: 0.5rem 0.75rem;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  color: var(--text-primary);
  font-size: 0.875rem;
  min-width: 140px;
  cursor: pointer;
}

.nexus-select:focus {
  border-color: var(--neon-cyan);
  outline: none;
}

/* 对话容器 */
.chat-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.messages-area {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
}

.welcome {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
  color: var(--text-muted);
}

.welcome-icon {
  margin-bottom: 1rem;
  opacity: 0.5;
}

.welcome h2 {
  font-size: 1.125rem;
  color: var(--text-secondary);
  margin-bottom: 0.5rem;
}

.welcome p {
  font-size: 0.875rem;
}

.message {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.message-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  font-size: 0.8rem;
}

.message.user .message-avatar {
  background: linear-gradient(135deg, var(--neon-cyan), var(--neon-amber));
  color: var(--bg-primary);
  font-weight: 600;
}

.message.assistant .message-avatar {
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  color: var(--neon-cyan);
}

.message-content {
  flex: 1;
  min-width: 0;
}

.text-bubble {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  padding: 0.75rem 1rem;
  border-radius: var(--radius-md);
  display: inline-block;
}

.file-preview {
  margin-top: 0.5rem;
  border-radius: var(--radius-md);
  overflow: hidden;
  max-width: 300px;
}

.file-preview img, .file-preview video {
  width: 100%;
  display: block;
}

.file-icon {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  background: var(--bg-tertiary);
  color: var(--text-secondary);
  font-size: 0.875rem;
}

.analyzing {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  color: var(--neon-cyan);
  padding: 0.75rem;
}

.analyzing .dot {
  width: 6px;
  height: 6px;
  background: var(--neon-cyan);
  border-radius: 50%;
  animation: bounce 1s infinite;
}

.analyzing .dot:nth-child(2) { animation-delay: 0.2s; }
.analyzing .dot:nth-child(3) { animation-delay: 0.4s; }

.cancelled-bubble {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  color: var(--text-muted);
  padding: 0.75rem 1rem;
  border-radius: var(--radius-md);
  font-size: 0.875rem;
}

@keyframes bounce {
  0%, 100% { opacity: 0.3; transform: translateY(0); }
  50% { opacity: 1; transform: translateY(-4px); }
}

.result-section {
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.result-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 1rem;
  background: rgba(0, 217, 255, 0.05);
  border-bottom: 1px solid var(--border-color);
}

.result-title {
  font-weight: 600;
  font-size: 0.9rem;
}

.result-stats {
  font-size: 0.75rem;
  color: var(--text-muted);
}

.graph-section {
  padding: 1rem;
}

.graph-canvas {
  min-height: 150px;
}

.section-title {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 1rem;
  cursor: pointer;
  font-size: 0.85rem;
  color: var(--text-secondary);
  background: var(--bg-tertiary);
}

.section-title svg {
  transition: transform var(--transition-fast);
}

.section-title svg.expanded {
  transform: rotate(180deg);
}

.section-content {
  padding: 0.75rem 1rem;
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.entity-tag {
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.375rem 0.625rem;
  font-size: 0.75rem;
  background: var(--neon-cyan-dim);
  color: var(--neon-cyan);
  border-radius: 4px;
}

.entity-tag small {
  opacity: 0.7;
}

.entity-tag.person { background: var(--neon-amber-dim); color: var(--neon-amber); }
.entity-tag.process { background: rgba(0, 255, 136, 0.15); color: var(--neon-green); }
.entity-tag.event { background: rgba(255, 0, 170, 0.15); color: var(--neon-magenta); }

.relation-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.375rem 0.625rem;
  font-size: 0.75rem;
  background: var(--bg-tertiary);
  border-radius: 4px;
}

.rel-source, .rel-target {
  color: var(--neon-cyan);
}

.rel-type {
  color: var(--neon-amber);
}

.error-bubble {
  background: rgba(255, 0, 170, 0.1);
  border: 1px solid rgba(255, 0, 170, 0.3);
  color: var(--neon-magenta);
  padding: 0.75rem 1rem;
  border-radius: var(--radius-md);
  font-size: 0.875rem;
}

/* 输入区域 */
.input-area {
  padding: 1rem;
  border-top: 1px solid var(--border-color);
  background: var(--bg-secondary);
}

.input-box {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem;
  background: var(--bg-card);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
}

.input-actions {
  display: flex;
  gap: 0.25rem;
}

.action-btn {
  width: 36px;
  height: 36px;
  background: transparent;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-fast);
}

.action-btn:hover {
  background: var(--bg-tertiary);
  color: var(--neon-cyan);
}

.input-box input {
  flex: 1;
  background: transparent;
  border: none;
  color: var(--text-primary);
  font-size: 0.9rem;
  padding: 0.5rem;
}

.input-box input::placeholder {
  color: var(--text-muted);
}

.input-box input:focus {
  outline: none;
}

.send-btn {
  width: 40px;
  height: 40px;
  background: var(--neon-cyan);
  border: none;
  border-radius: var(--radius-sm);
  color: var(--bg-primary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-fast);
}

.send-btn:hover:not(:disabled) {
  box-shadow: 0 0 15px var(--neon-cyan-glow);
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.stop-btn-input {
  width: 40px;
  height: 40px;
  background: var(--neon-magenta);
  border: none;
  border-radius: var(--radius-sm);
  color: white;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-fast);
}

.stop-btn-input:hover {
  box-shadow: 0 0 15px rgba(255, 0, 170, 0.5);
}

/* 占位页面 */
.placeholder-page {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.placeholder-content {
  text-align: center;
  color: var(--text-muted);
}

.placeholder-content svg {
  opacity: 0.3;
  margin-bottom: 1rem;
}

.placeholder-content h2 {
  font-size: 1.25rem;
  color: var(--text-secondary);
  margin-bottom: 0.5rem;
}

@media (max-width: 768px) {
  .app-layout {
    grid-template-columns: 1fr;
  }
  .sidebar {
    display: none;
  }
}
</style>