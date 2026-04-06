<template>
  <div class="chat-page">
    <!-- 顶部导航 -->
    <header class="chat-header">
      <button class="back-btn" @click="$router.push('/app')">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M19 12H5M12 19l-7-7 7-7"/>
        </svg>
      </button>
      <h1 class="header-title">对话分析</h1>
      <div class="header-controls">
        <select v-model="selectedModelId" class="model-select">
          <option :value="null">选择AI模型</option>
          <option v-for="config in aiConfigs" :key="config.id" :value="config.id">
            {{ config.model_name }}
          </option>
        </select>
        <button class="clear-btn" @click="clearAll">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="3 6 5 6 21 6"/>
            <path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/>
          </svg>
          清空
        </button>
      </div>
    </header>

    <!-- 主体区域 -->
    <div class="main-content">
      <!-- 左侧：对话区域 -->
      <aside class="chat-sidebar">
        <div class="messages-container" ref="messagesContainer">
          <div v-for="(msg, index) in messages" :key="index" 
               :class="['message', msg.role]">
            <div class="message-avatar">
              <span v-if="msg.role === 'user'">我</span>
              <span v-else>AI</span>
            </div>
            <div class="message-content">
              <div class="message-text" v-html="formatMessage(msg.content)"></div>
              <span class="message-time">{{ msg.time }}</span>
            </div>
          </div>
          <div v-if="streaming" class="message assistant streaming">
            <div class="message-avatar">AI</div>
            <div class="message-content">
              <div class="message-text">{{ streamingContent }}<span class="cursor">|</span></div>
            </div>
          </div>
        </div>

        <div class="input-area">
          <textarea 
            v-model="inputMessage" 
            placeholder="描述你想分析的内容，例如：'分析一下电商系统的订单处理流程'..."
            @keydown.enter.prevent="sendMessage"
            rows="3"
          ></textarea>
          <button 
            class="send-btn" 
            :disabled="!inputMessage.trim() || !selectedModelId || streaming"
            @click="sendMessage"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="22" y1="2" x2="11" y2="13"/>
              <polygon points="22 2 15 22 11 13 2 9 22 2"/>
            </svg>
          </button>
        </div>
      </aside>

      <!-- 右侧：画布区域 -->
      <main class="canvas-area">
        <div class="canvas-header">
          <div class="stats">
            <span class="stat-item">
              <span class="stat-label">实体</span>
              <span class="stat-value">{{ entities.length }}</span>
            </span>
            <span class="stat-item">
              <span class="stat-label">关系</span>
              <span class="stat-value">{{ relations.length }}</span>
            </span>
          </div>
          <div class="canvas-actions">
            <button class="action-btn" @click="autoLayout">自动布局</button>
            <button class="action-btn" @click="exportGraph">导出</button>
          </div>
        </div>
        <div ref="graphContainer" class="graph-canvas"></div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { Graph } from '@antv/x6'
import { ElMessage } from 'element-plus'
import { getAIConfigs } from '@/api/ai-configs'
import type { AIConfig } from '@/api/ai-configs'

interface ChatMessage {
  role: 'user' | 'assistant' | 'system'
  content: string
  time: string
}

interface Entity {
  id: string
  name: string
  type: string
  description?: string
  x?: number
  y?: number
}

interface Relation {
  id: string
  source: string
  target: string
  type: string
  description?: string
}

const router = useRouter()
const token = localStorage.getItem('token') || ''

// 状态
const messages = ref<ChatMessage[]>([])
const inputMessage = ref('')
const streaming = ref(false)
const streamingContent = ref('')
const selectedModelId = ref<number | null>(null)
const aiConfigs = ref<AIConfig[]>([])
const entities = ref<Entity[]>([])
const relations = ref<Relation[]>([])
const messagesContainer = ref<HTMLElement | null>(null)
const graphContainer = ref<HTMLElement | null>(null)
let graph: Graph | null = null

// 加载AI配置
const loadAIConfigs = async () => {
  try {
    const response = await getAIConfigs()
    aiConfigs.value = response.data || []
    if (aiConfigs.value.length > 0) {
      selectedModelId.value = aiConfigs.value[0].id
    }
  } catch (e) {
    console.error(e)
  }
}

// 初始化画布
const initGraph = () => {
  if (!graphContainer.value) return
  graph = new Graph({
    container: graphContainer.value,
    grid: { size: 20, visible: true },
    panning: true,
    mousewheel: true,
    background: { color: 'var(--bg-tertiary)' },
    connecting: { anchor: 'center', connectionPoint: 'anchor', snap: true }
  })
}

// 渲染图谱
const renderGraph = () => {
  if (!graph) return
  graph.clearCells()
  
  // 渲染实体节点
  entities.value.forEach((entity, index) => {
    const colorMap: Record<string, string> = {
      person: '#ffb800',
      concept: '#00d9ff',
      process: '#00ff88',
      object: '#ff00aa',
      event: '#ff6b6b'
    }
    
    graph!.addNode({
      id: entity.id,
      shape: 'rect',
      x: entity.x ?? 100 + (index % 5) * 200,
      y: entity.y ?? 100 + Math.floor(index / 5) * 120,
      width: 160,
      height: 60,
      attrs: {
        body: { 
          fill: 'rgba(13, 20, 36, 0.9)', 
          stroke: colorMap[entity.type] || '#00d9ff', 
          strokeWidth: 2, 
          rx: 8, 
          ry: 8 
        },
        label: { 
          text: entity.name, 
          fill: '#e8edf5', 
          fontSize: 13,
          fontWeight: 500
        }
      }
    })
  })
  
  // 渲染关系连线
  relations.value.forEach((relation) => {
    const sourceNode = entities.value.find(e => e.name === relation.source)
    const targetNode = entities.value.find(e => e.name === relation.target)
    
    if (sourceNode && targetNode) {
      graph!.addEdge({
        source: sourceNode.id,
        target: targetNode.id,
        attrs: { 
          line: { stroke: '#ffb800', strokeWidth: 2 }
        },
        labels: [{ 
          attrs: { 
            text: { 
              text: relation.type, 
              fill: '#8a9bb8', 
              fontSize: 11 
            } 
          } 
        }]
      })
    }
  })
}

// 自动布局
const autoLayout = () => {
  // 简单的圆形布局
  const centerX = 400
  const centerY = 300
  const radius = 250
  
  entities.value.forEach((entity, index) => {
    if (!entity.x || !entity.y) {
      const angle = (index / entities.value.length) * 2 * Math.PI
      entity.x = centerX + radius * Math.cos(angle)
      entity.y = centerY + radius * Math.sin(angle)
    }
  })
  
  renderGraph()
}

// 导出图谱
const exportGraph = () => {
  const data = {
    entities: entities.value,
    relations: relations.value,
    messages: messages.value.map(m => ({ role: m.role, content: m.content }))
  }
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = `chat-analysis-${Date.now()}.json`
  link.click()
  ElMessage.success('导出成功')
}

// 清空所有
const clearAll = () => {
  messages.value = []
  entities.value = []
  relations.value = []
  renderGraph()
  ElMessage.success('已清空')
}

// 格式化消息（简单的换行处理）
const formatMessage = (content: string) => {
  return content.replace(/\n/g, '<br>')
}

// 滚动到底部
const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

// 生成唯一ID
const generateId = () => `_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`

// 处理流式响应
const handleStreamResponse = async (reader: ReadableStreamDefaultReader<Uint8Array>) => {
  const decoder = new TextDecoder()
  let buffer = ''
  
  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    
    buffer += decoder.decode(value, { stream: true })
    const lines = buffer.split('\n')
    buffer = lines.pop() || ''
    
    for (const line of lines) {
      if (line.startsWith('event: ')) {
        const eventType = line.slice(7)
        const dataLine = lines.find(l => l.startsWith('data: '))
        if (dataLine) {
          try {
            const data = JSON.parse(dataLine.slice(6))
            
            switch (eventType) {
              case 'content':
                streamingContent.value += data.content || ''
                scrollToBottom()
                break
              case 'entities':
                // 添加新实体
                if (data.entities) {
                  for (const e of data.entities) {
                    const exists = entities.value.find(ex => ex.name === e.name)
                    if (!exists) {
                      entities.value.push({
                        id: generateId(),
                        name: e.name,
                        type: e.type || 'concept',
                        description: e.description
                      })
                    }
                  }
                  renderGraph()
                }
                break
              case 'relations':
                // 添加新关系
                if (data.relations) {
                  for (const r of data.relations) {
                    const exists = relations.value.find(ex => 
                      ex.source === r.source && ex.target === r.target && ex.type === r.type
                    )
                    if (!exists) {
                      relations.value.push({
                        id: generateId(),
                        source: r.source,
                        target: r.target,
                        type: r.type,
                        description: r.description
                      })
                    }
                  }
                  renderGraph()
                }
                break
            }
          } catch (e) {
            console.error('Parse error:', e)
          }
        }
      }
    }
  }
}

// 发送消息
const sendMessage = async () => {
  if (!inputMessage.value.trim() || !selectedModelId.value || streaming.value) return
  
  const content = inputMessage.value.trim()
  inputMessage.value = ''
  
  // 添加用户消息
  messages.value.push({
    role: 'user',
    content: content,
    time: new Date().toLocaleTimeString()
  })
  scrollToBottom()
  
  streaming.value = true
  streamingContent.value = ''
  
  try {
    const response = await fetch('/api/chat/stream', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        messages: messages.value.map(m => ({ role: m.role, content: m.content })),
        ai_config_id: selectedModelId.value
      })
    })
    
    if (!response.ok) {
      throw new Error('请求失败')
    }
    
    if (response.body) {
      const reader = response.body.getReader()
      await handleStreamResponse(reader)
    }
    
    // 添加AI回复到消息列表
    if (streamingContent.value) {
      messages.value.push({
        role: 'assistant',
        content: streamingContent.value,
        time: new Date().toLocaleTimeString()
      })
    }
    
  } catch (error) {
    ElMessage.error('发送失败: ' + (error as Error).message)
  } finally {
    streaming.value = false
    streamingContent.value = ''
    scrollToBottom()
  }
}

onMounted(async () => {
  await loadAIConfigs()
  await nextTick()
  initGraph()
})
</script>

<style scoped>
.chat-page {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: var(--bg-primary);
}

/* Header */
.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-color);
}

.chat-header .back-btn {
  width: 36px;
  height: 36px;
  background: transparent;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-fast);
}

.chat-header .back-btn:hover {
  border-color: var(--neon-cyan);
  color: var(--neon-cyan);
}

.header-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--text-primary);
}

.header-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.model-select {
  padding: 0.5rem 1rem;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  color: var(--text-primary);
  font-size: 0.875rem;
  cursor: pointer;
}

.model-select:focus {
  border-color: var(--neon-cyan);
  outline: none;
}

.clear-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: transparent;
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
  cursor: pointer;
  font-size: 0.875rem;
  transition: all var(--transition-fast);
}

.clear-btn:hover {
  border-color: var(--neon-magenta);
  color: var(--neon-magenta);
}

/* Main Content */
.main-content {
  display: flex;
  flex: 1;
  overflow: hidden;
}

/* Chat Sidebar */
.chat-sidebar {
  width: 420px;
  display: flex;
  flex-direction: column;
  border-right: 1px solid var(--border-color);
  background: var(--bg-secondary);
}

.messages-container {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.message {
  display: flex;
  gap: 0.75rem;
  max-width: 100%;
}

.message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 600;
  flex-shrink: 0;
}

.message.user .message-avatar {
  background: var(--neon-cyan-dim);
  color: var(--neon-cyan);
}

.message.assistant .message-avatar {
  background: rgba(255, 184, 0, 0.15);
  color: var(--neon-amber);
}

.message-content {
  max-width: calc(100% - 60px);
  padding: 0.75rem 1rem;
  border-radius: var(--radius-md);
  background: var(--bg-tertiary);
}

.message.user .message-content {
  background: var(--neon-cyan-dim);
}

.message-text {
  font-size: 0.9rem;
  line-height: 1.5;
  color: var(--text-primary);
}

.message-time {
  display: block;
  font-size: 0.7rem;
  color: var(--text-muted);
  margin-top: 0.25rem;
}

.cursor {
  animation: blink 1s infinite;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

/* Input Area */
.input-area {
  padding: 1rem;
  border-top: 1px solid var(--border-color);
  display: flex;
  gap: 0.75rem;
}

.input-area textarea {
  flex: 1;
  padding: 0.75rem 1rem;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-md);
  color: var(--text-primary);
  font-size: 0.9rem;
  resize: none;
  outline: none;
}

.input-area textarea:focus {
  border-color: var(--neon-cyan);
}

.input-area textarea::placeholder {
  color: var(--text-muted);
}

.send-btn {
  width: 48px;
  height: 48px;
  background: var(--neon-cyan);
  border: none;
  border-radius: var(--radius-md);
  color: var(--bg-primary);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-fast);
}

.send-btn:hover:not(:disabled) {
  background: var(--neon-cyan-hover, #00d9ff);
  transform: scale(1.05);
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Canvas Area */
.canvas-area {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: var(--bg-primary);
}

.canvas-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1rem 1.5rem;
  border-bottom: 1px solid var(--border-color);
}

.stats {
  display: flex;
  gap: 1.5rem;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
}

.stat-label {
  color: var(--text-muted);
}

.stat-value {
  color: var(--neon-cyan);
  font-weight: 600;
  font-family: 'JetBrains Mono', monospace;
}

.canvas-actions {
  display: flex;
  gap: 0.75rem;
}

.action-btn {
  padding: 0.5rem 1rem;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
  cursor: pointer;
  font-size: 0.875rem;
  transition: all var(--transition-fast);
}

.action-btn:hover {
  border-color: var(--neon-cyan);
  color: var(--neon-cyan);
}

.graph-canvas {
  flex: 1;
  margin: 1rem;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
}

/* Responsive */
@media (max-width: 900px) {
  .main-content {
    flex-direction: column;
  }
  
  .chat-sidebar {
    width: 100%;
    height: 50vh;
    border-right: none;
    border-bottom: 1px solid var(--border-color);
  }
}
</style>
