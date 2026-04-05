<template>
  <div class="project-page">
    <!-- 左侧菜单 -->
    <aside class="side-menu">
      <div class="menu-header">
        <button class="back-btn" @click="$router.push('/dashboard')">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 12H5M12 19l-7-7 7-7"/>
          </svg>
        </button>
        <h3>数据血缘</h3>
      </div>

      <nav class="menu-nav">
        <button
          v-for="item in menuItems"
          :key="item.id"
          class="menu-item"
          :class="{ active: activeMenu === item.id }"
          @click="activeMenu = item.id"
        >
          <span class="menu-icon" v-html="item.icon"></span>
          <span class="menu-label">{{ item.label }}</span>
        </button>
      </nav>

      <div class="menu-footer">
        <button class="nexus-btn nexus-btn-primary btn-full" @click="showNewTaskDialog = true">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <line x1="12" y1="5" x2="12" y2="19"/>
            <line x1="5" y1="12" x2="19" y2="12"/>
          </svg>
          新建分析
        </button>
      </div>
    </aside>

    <!-- 主内容 -->
    <main class="main-area">
      <!-- 顶部工具栏 -->
      <header class="toolbar glass">
        <div class="toolbar-left">
          <h1 class="project-title">{{ project?.name || '加载中...' }}</h1>
          <div class="toolbar-selects">
            <select v-model="selectedTaskId" class="nexus-select">
              <option :value="null">选择任务</option>
              <option v-for="task in tasks" :key="task.id" :value="task.id">
                任务 #{{ task.id }}
              </option>
            </select>
            <select v-model="selectedModelId" class="nexus-select">
              <option :value="null">选择模型</option>
              <option v-for="config in aiConfigs" :key="config.id" :value="config.id">
                {{ config.model_name }}
              </option>
            </select>
          </div>
        </div>
        <div class="toolbar-right">
          <button class="nexus-btn nexus-btn-secondary" @click="exportGraph('json')">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/>
            </svg>
            导出
          </button>
        </div>
      </header>

      <!-- 数据源面板 -->
      <section v-show="activeMenu === 'datasource'" class="panel">
        <div class="panel-header">
          <h2>数据源</h2>
        </div>
        <div class="upload-zone glass" @dragover.prevent @drop.prevent="handleDrop">
          <input type="file" ref="fileInput" multiple accept="image/*,video/*,.txt,.md" @change="handleFileSelect" hidden />
          <div class="upload-content" @click="$refs.fileInput?.click()">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1">
              <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/>
              <polyline points="17 8 12 3 7 8"/>
              <line x1="12" y1="3" x2="12" y2="15"/>
            </svg>
            <p>拖拽文件到此处或点击上传</p>
            <span class="upload-hint">支持图片、视频、文本文件</span>
          </div>
        </div>

        <div class="data-list">
          <div v-for="ds in dataSources" :key="ds.id" class="data-item glass">
            <div class="data-icon" :class="ds.type">
              <svg v-if="ds.type === 'image'" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <rect x="3" y="3" width="18" height="18" rx="2"/>
                <circle cx="8.5" cy="8.5" r="1.5"/>
                <path d="M21 15l-5-5L5 21"/>
              </svg>
              <svg v-else-if="ds.type === 'video'" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <polygon points="5 3 19 12 5 21 5 3"/>
              </svg>
              <svg v-else width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
                <polyline points="14 2 14 8 20 8"/>
                <line x1="16" y1="13" x2="8" y2="13"/>
                <line x1="16" y1="17" x2="8" y2="17"/>
              </svg>
            </div>
            <div class="data-info">
              <span class="data-name">{{ ds.file_name || '文字输入' }}</span>
              <span class="data-type">{{ ds.type }}</span>
            </div>
            <button class="delete-btn" @click="deleteDataSource(ds.id)">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="3 6 5 6 21 6"/>
                <path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/>
              </svg>
            </button>
          </div>
        </div>
      </section>

      <!-- 任务面板 -->
      <section v-show="activeMenu === 'tasks'" class="panel">
        <div class="panel-header">
          <h2>分析任务</h2>
        </div>
        <div class="task-list">
          <div v-for="task in tasks" :key="task.id" class="task-item glass" @click="viewTaskResult(task)">
            <div class="task-status" :class="task.status">
              <span class="status-dot"></span>
              {{ task.status }}
            </div>
            <div class="task-info">
              <span class="task-id">任务 #{{ task.id }}</span>
              <span class="task-source">{{ getDataSourceName(task.data_source_id) }}</span>
            </div>
            <span class="task-time">{{ new Date(task.created_at).toLocaleString() }}</span>
          </div>
          <div v-if="tasks.length === 0" class="empty-hint">
            暂无任务，点击左侧"新建分析"创建
          </div>
        </div>
      </section>

      <!-- 图谱面板 -->
      <section v-show="activeMenu === 'graph'" class="panel graph-panel">
        <div class="graph-area">
          <div ref="graphContainer" class="graph-canvas"></div>
        </div>
        <aside class="graph-sidebar">
          <div class="sidebar-card glass" v-if="selectedEntity">
            <div class="card-header">
              <span class="entity-type-badge" :class="selectedEntity.type">{{ selectedEntity.type || 'entity' }}</span>
              <h4>{{ selectedEntity.name }}</h4>
            </div>
            <div class="card-body">
              <div class="field">
                <label>名称</label>
                <input v-model="selectedEntity.name" class="nexus-input" @change="updateEntity" />
              </div>
              <div class="field">
                <label>类型</label>
                <select v-model="selectedEntity.type" class="nexus-input" @change="updateEntity">
                  <option value="person">人物</option>
                  <option value="concept">概念</option>
                  <option value="process">流程</option>
                  <option value="object">物体</option>
                  <option value="event">事件</option>
                </select>
              </div>
              <div class="field">
                <label>描述</label>
                <textarea v-model="selectedEntity.description" class="nexus-input" @change="updateEntity" rows="3"></textarea>
              </div>
              <button class="nexus-btn nexus-btn-secondary btn-full" @click="deleteSelectedEntity">
                删除实体
              </button>
            </div>
          </div>
          <div class="sidebar-card glass" v-else>
            <div class="card-header">
              <h4>添加实体</h4>
            </div>
            <div class="card-body">
              <div class="field">
                <label>名称</label>
                <input v-model="newEntity.name" class="nexus-input" placeholder="实体名称" />
              </div>
              <div class="field">
                <label>类型</label>
                <select v-model="newEntity.type" class="nexus-input">
                  <option value="concept">概念</option>
                  <option value="person">人物</option>
                  <option value="process">流程</option>
                  <option value="object">物体</option>
                  <option value="event">事件</option>
                </select>
              </div>
              <button class="nexus-btn nexus-btn-primary btn-full" @click="addEntity">
                添加实体
              </button>
            </div>
          </div>
        </aside>
      </section>

      <!-- 设置面板 -->
      <section v-show="activeMenu === 'settings'" class="panel">
        <div class="panel-header">
          <h2>项目设置</h2>
        </div>
        <div class="settings-form glass">
          <div class="field">
            <label>项目名称</label>
            <input v-model="projectSettings.name" class="nexus-input" />
          </div>
          <div class="field">
            <label>项目描述</label>
            <textarea v-model="projectSettings.description" class="nexus-input" rows="4"></textarea>
          </div>
          <button class="nexus-btn nexus-btn-primary" @click="saveProjectSettings">保存设置</button>
        </div>
      </section>

      <!-- 底部状态栏 -->
      <footer class="status-bar">
        <div class="status-item">
          <span class="status-label">实体</span>
          <span class="status-value">{{ entities.length }}</span>
        </div>
        <div class="status-item">
          <span class="status-label">关系</span>
          <span class="status-value">{{ relations.length }}</span>
        </div>
        <div class="status-item">
          <span class="status-label">保存</span>
          <span class="status-value">{{ lastSaved }}</span>
        </div>
      </footer>
    </main>

    <!-- 新建任务弹窗 -->
    <div v-if="showNewTaskDialog" class="modal-overlay" @click.self="showNewTaskDialog = false">
      <div class="modal glass">
        <div class="modal-header">
          <h2>新建分析任务</h2>
          <button class="modal-close" @click="showNewTaskDialog = false">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M18 6L6 18M6 6l12 12"/>
            </svg>
          </button>
        </div>
        <form @submit.prevent="createTaskHandler">
          <div class="field">
            <label>数据源</label>
            <select v-model="newTask.data_source_id" class="nexus-input" required>
              <option :value="null">选择数据源</option>
              <option v-for="ds in dataSources" :key="ds.id" :value="ds.id">
                {{ ds.file_name || '文字输入' }}
              </option>
            </select>
          </div>
          <div class="field">
            <label>AI模型</label>
            <select v-model="newTask.ai_config_id" class="nexus-input">
              <option :value="null">选择模型</option>
              <option v-for="config in aiConfigs" :key="config.id" :value="config.id">
                {{ config.model_name }}
              </option>
            </select>
          </div>
          <div class="modal-actions">
            <button type="button" class="nexus-btn nexus-btn-secondary" @click="showNewTaskDialog = false">取消</button>
            <button type="submit" class="nexus-btn nexus-btn-primary" :disabled="creatingTask">
              {{ creatingTask ? '创建中...' : '创建任务' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, watch, nextTick, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Graph } from '@antv/x6'
import api from '@/api'
import { getProject, type Project } from '@/api/projects'
import { getAIConfigs, type AIConfig } from '@/api/ai-configs'

interface DataSource { id: number; type: string; file_name: string; file_path: string; content: string }
interface Task { id: number; data_source_id: number; ai_config_id: number; status: string; created_at: string }
interface Entity { id: number; name: string; type: string; description: string; position_x: number; position_y: number }
interface Relation { id: number; source_entity_id: number; target_entity_id: number; relation_type: string }

const route = useRoute()
const router = useRouter()
const projectId = Number(route.params.id)
const token = localStorage.getItem('token') || ''

const menuItems = [
  { id: 'datasource', label: '数据源', icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>' },
  { id: 'tasks', label: '任务', icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M9 11l3 3L22 4"/><path d="M21 12v7a2 2 0 01-2 2H5a2 2 0 01-2-2V5a2 2 0 012-2h11"/></svg>' },
  { id: 'graph', label: '图谱', icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="3"/><circle cx="19" cy="5" r="2"/><circle cx="5" cy="19" r="2"/><path d="M14.5 10.5L17 7M9.5 13.5L7 16"/></svg>' },
  { id: 'settings', label: '设置', icon: '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-2 2 2 2 0 01-2-2v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 01-2-2 2 2 0 012-2h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06a1.65 1.65 0 001.82.33H9a1.65 1.65 0 001-1.51V3a2 2 0 012-2 2 2 0 012 2v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9a1.65 1.65 0 001.51 1H21a2 2 0 012 2 2 2 0 01-2 2h-.09a1.65 1.65 0 00-1.51 1z"/></svg>' },
]

const activeMenu = ref('graph')
const project = ref<Project | null>(null)
const aiConfigs = ref<AIConfig[]>([])
const dataSources = ref<DataSource[]>([])
const tasks = ref<Task[]>([])
const entities = ref<Entity[]>([])
const relations = ref<Relation[]>([])

const selectedTaskId = ref<number | null>(null)
const selectedModelId = ref<number | null>(null)
const selectedEntity = ref<Entity | null>(null)
const lastSaved = ref('--')

const showNewTaskDialog = ref(false)
const creatingTask = ref(false)
const fileInput = ref<HTMLInputElement | null>(null)

const newTask = reactive({ data_source_id: null as number | null, ai_config_id: null as number | null })
const newEntity = reactive({ name: '', type: 'concept' })
const projectSettings = reactive({ name: '', description: '' })

const graphContainer = ref<HTMLElement | null>(null)
let graph: Graph | null = null

// Load functions
const loadProject = async () => {
  try {
    project.value = await getProject(projectId)
    projectSettings.name = project.value.name
    projectSettings.description = project.value.description || ''
  } catch (error) {
    ElMessage.error('加载项目失败')
    router.push('/dashboard')
  }
}

const loadAIConfigs = async () => {
  try { aiConfigs.value = await getAIConfigs() } catch (e) { console.error(e) }
}

const loadDataSources = async () => {
  try { dataSources.value = await api.get<DataSource[]>(`/data-sources?project_id=${projectId}`) } catch (e) { console.error(e) }
}

const loadTasks = async () => {
  try { tasks.value = await api.get<Task[]>(`/tasks?project_id=${projectId}`) } catch (e) { console.error(e) }
}

const loadGraphData = async () => {
  if (!selectedTaskId.value) return
  try {
    const [entitiesData, relationsData] = await Promise.all([
      api.get<Entity[]>(`/graph/entities?task_id=${selectedTaskId.value}`),
      api.get<Relation[]>(`/graph/relations?task_id=${selectedTaskId.value}`)
    ])
    entities.value = entitiesData
    relations.value = relationsData
    renderGraph()
  } catch (e) { console.error(e) }
}

// Graph functions
const initGraph = () => {
  if (!graphContainer.value) return
  graph = new Graph({
    container: graphContainer.value,
    grid: { size: 20, visible: true, attrs: { stroke: 'rgba(0, 217, 255, 0.05)' } },
    panning: true,
    mousewheel: true,
    background: { color: 'var(--bg-tertiary)' },
    connecting: { anchor: 'center', connectionPoint: 'anchor', snap: true }
  })
  graph.on('node:click', ({ node }) => {
    selectedEntity.value = entities.value.find(e => e.id === Number(node.id)) || null
  })
  graph.on('node:moved', ({ node }) => {
    const entity = entities.value.find(e => e.id === Number(node.id))
    if (entity) {
      entity.position_x = node.position().x
      entity.position_y = node.position().y
      updateEntityPosition(entity)
    }
  })
}

const renderGraph = () => {
  if (!graph) return
  graph.clearCells()
  entities.value.forEach((entity, index) => {
    graph!.addNode({
      id: String(entity.id),
      shape: 'rect',
      x: entity.position_x || 100 + (index % 5) * 200,
      y: entity.position_y || 100 + Math.floor(index / 5) * 100,
      width: 140,
      height: 50,
      attrs: {
        body: { fill: '#0d1424', stroke: '#00d9ff', strokeWidth: 1.5, rx: 8, ry: 8 },
        label: { text: entity.name, fill: '#e8edf5', fontSize: 13, fontFamily: 'Space Grotesk' }
      }
    })
  })
  relations.value.forEach(relation => {
    graph!.addEdge({
      source: String(relation.source_entity_id),
      target: String(relation.target_entity_id),
      attrs: { line: { stroke: '#ffb800', strokeWidth: 2 } },
      labels: [{ attrs: { text: { text: relation.relation_type || '', fill: '#8a9bb8', fontSize: 11 } } }]
    })
  })
}

const updateEntity = async () => {
  if (!selectedEntity.value) return
  try {
    await api.put(`/graph/entities/${selectedEntity.value.id}`, selectedEntity.value)
    lastSaved.value = new Date().toLocaleTimeString()
    renderGraph()
  } catch { ElMessage.error('保存失败') }
}

const updateEntityPosition = async (entity: Entity) => {
  try { await api.put(`/graph/entities/${entity.id}`, { position_x: entity.position_x, position_y: entity.position_y }) } catch {}
}

const addEntity = async () => {
  if (!newEntity.name || !selectedTaskId.value) return
  try {
    const entity = await api.post<Entity>('/graph/entities', { task_id: selectedTaskId.value, ...newEntity, is_user_created: true })
    entities.value.push(entity)
    renderGraph()
    newEntity.name = ''
    newEntity.type = 'concept'
  } catch { ElMessage.error('添加失败') }
}

const deleteSelectedEntity = async () => {
  if (!selectedEntity.value) return
  try {
    await api.delete(`/graph/entities/${selectedEntity.value.id}`)
    entities.value = entities.value.filter(e => e.id !== selectedEntity.value!.id)
    selectedEntity.value = null
    renderGraph()
  } catch { ElMessage.error('删除失败') }
}

// Task functions
const createTaskHandler = async () => {
  if (!newTask.data_source_id) { ElMessage.warning('请选择数据源'); return }
  creatingTask.value = true
  try {
    await api.post<Task>('/tasks', { project_id: projectId, ...newTask })
    ElMessage.success('任务创建成功')
    showNewTaskDialog.value = false
    loadTasks()
  } catch { ElMessage.error('创建失败') }
  finally { creatingTask.value = false }
}

const viewTaskResult = (task: Task) => {
  selectedTaskId.value = task.id
  activeMenu.value = 'graph'
  loadGraphData()
}

// File handling
const handleFileSelect = async (e: Event) => {
  const files = (e.target as HTMLInputElement).files
  if (!files) return
  for (const file of Array.from(files)) await uploadFile(file)
}

const handleDrop = async (e: DragEvent) => {
  const files = e.dataTransfer?.files
  if (!files) return
  for (const file of Array.from(files)) await uploadFile(file)
}

const uploadFile = async (file: File) => {
  const formData = new FormData()
  formData.append('file', file)
  formData.append('project_id', String(projectId))
  try {
    await fetch('/api/data-sources/upload', {
      method: 'POST',
      headers: { Authorization: `Bearer ${token}` },
      body: formData
    })
    ElMessage.success('上传成功')
    loadDataSources()
  } catch { ElMessage.error('上传失败') }
}

const deleteDataSource = async (id: number) => {
  try {
    await api.delete(`/data-sources/${id}`)
    dataSources.value = dataSources.value.filter(d => d.id !== id)
    ElMessage.success('删除成功')
  } catch { ElMessage.error('删除失败') }
}

const getDataSourceName = (id: number) => dataSources.value.find(d => d.id === id)?.file_name || '文字输入'

const exportGraph = async (format: string) => {
  if (!selectedTaskId.value) { ElMessage.warning('请先选择任务'); return }
  try {
    const res = await api.post(`/graph/export?task_id=${selectedTaskId.value}&format=${format}`, {})
    const blob = new Blob([JSON.stringify(res, null, 2)], { type: 'application/json' })
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = `graph.${format}`
    link.click()
  } catch { ElMessage.error('导出失败') }
}

const saveProjectSettings = async () => {
  try {
    await api.put(`/projects/${projectId}`, projectSettings)
    if (project.value) { project.value.name = projectSettings.name; project.value.description = projectSettings.description }
    ElMessage.success('保存成功')
  } catch { ElMessage.error('保存失败') }
}

watch(selectedTaskId, loadGraphData)

onMounted(async () => {
  await Promise.all([loadProject(), loadAIConfigs(), loadDataSources(), loadTasks()])
  await nextTick()
  initGraph()
})
</script>

<style scoped>
.project-page {
  display: grid;
  grid-template-columns: 220px 1fr;
  min-height: 100vh;
  background: var(--bg-primary);
}

/* Side Menu */
.side-menu {
  background: var(--bg-secondary);
  border-right: 1px solid var(--border-color);
  display: flex;
  flex-direction: column;
  padding: 1rem;
}

.menu-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--border-color);
  margin-bottom: 1rem;
}

.back-btn {
  width: 32px;
  height: 32px;
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

.back-btn:hover { border-color: var(--neon-cyan); color: var(--neon-cyan); }

.menu-header h3 {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--neon-cyan);
}

.menu-nav { display: flex; flex-direction: column; gap: 0.25rem; flex: 1; }

.menu-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  background: transparent;
  border: none;
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
  cursor: pointer;
  transition: all var(--transition-fast);
  text-align: left;
  width: 100%;
}

.menu-item:hover { background: var(--bg-tertiary); color: var(--text-primary); }
.menu-item.active { background: var(--neon-cyan-dim); color: var(--neon-cyan); }

.menu-footer { padding-top: 1rem; border-top: 1px solid var(--border-color); }
.btn-full { width: 100%; justify-content: center; }

/* Main Area */
.main-area { display: flex; flex-direction: column; overflow: hidden; }

/* Toolbar */
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  background: var(--bg-secondary);
  border-bottom: 1px solid var(--border-color);
}

.toolbar-left { display: flex; align-items: center; gap: 1.5rem; }
.project-title { font-size: 1.25rem; font-weight: 600; }
.toolbar-selects { display: flex; gap: 0.75rem; }

.nexus-select {
  padding: 0.5rem 1rem;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-sm);
  color: var(--text-primary);
  font-size: 0.875rem;
  cursor: pointer;
  min-width: 140px;
}

.nexus-select:focus { border-color: var(--neon-cyan); outline: none; }

/* Panel */
.panel { flex: 1; padding: 1.5rem; overflow-y: auto; }

.panel-header { margin-bottom: 1.5rem; }
.panel-header h2 { font-size: 1.125rem; font-weight: 600; }

/* Upload Zone */
.upload-zone {
  border: 2px dashed var(--border-color);
  border-radius: var(--radius-lg);
  padding: 3rem;
  text-align: center;
  cursor: pointer;
  transition: all var(--transition-fast);
  margin-bottom: 1.5rem;
}

.upload-zone:hover { border-color: var(--neon-cyan); background: var(--neon-cyan-dim); }

.upload-content { display: flex; flex-direction: column; align-items: center; gap: 0.75rem; color: var(--text-secondary); }
.upload-hint { font-size: 0.75rem; color: var(--text-muted); }

/* Data List */
.data-list { display: flex; flex-direction: column; gap: 0.75rem; }

.data-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  transition: all var(--transition-fast);
}

.data-item:hover { border-color: var(--border-glow); }

.data-icon {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
}

.data-icon.image { background: rgba(0, 217, 255, 0.15); color: var(--neon-cyan); }
.data-icon.video { background: rgba(255, 184, 0, 0.15); color: var(--neon-amber); }
.data-icon.text { background: rgba(0, 255, 136, 0.15); color: var(--neon-green); }

.data-info { flex: 1; display: flex; flex-direction: column; gap: 0.25rem; }
.data-name { font-size: 0.9rem; font-weight: 500; }
.data-type { font-size: 0.75rem; color: var(--text-muted); text-transform: uppercase; }

.delete-btn {
  background: transparent;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 0.5rem;
  transition: color var(--transition-fast);
}

.delete-btn:hover { color: var(--neon-magenta); }

/* Task List */
.task-list { display: flex; flex-direction: column; gap: 0.75rem; }

.task-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.task-item:hover { border-color: var(--border-glow); transform: translateX(4px); }

.task-status {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.375rem 0.75rem;
  border-radius: 999px;
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
}

.status-dot { width: 6px; height: 6px; border-radius: 50%; }

.task-status.pending { background: var(--neon-amber-dim); color: var(--neon-amber); }
.task-status.pending .status-dot { background: var(--neon-amber); }
.task-status.running { background: var(--neon-cyan-dim); color: var(--neon-cyan); }
.task-status.running .status-dot { background: var(--neon-cyan); animation: pulse-glow 1s infinite; }
.task-status.completed { background: rgba(0, 255, 136, 0.15); color: var(--neon-green); }
.task-status.completed .status-dot { background: var(--neon-green); }
.task-status.failed { background: rgba(255, 0, 170, 0.15); color: var(--neon-magenta); }
.task-status.failed .status-dot { background: var(--neon-magenta); }

.task-info { flex: 1; display: flex; flex-direction: column; gap: 0.25rem; }
.task-id { font-size: 0.9rem; font-weight: 500; }
.task-source { font-size: 0.75rem; color: var(--text-muted); }
.task-time { font-size: 0.75rem; color: var(--text-muted); }

.empty-hint { text-align: center; padding: 2rem; color: var(--text-muted); }

/* Graph Panel */
.graph-panel { display: grid; grid-template-columns: 1fr 320px; gap: 1.5rem; }

.graph-area { display: flex; flex-direction: column; }

.graph-canvas {
  flex: 1;
  background: var(--bg-tertiary);
  border: 1px solid var(--border-color);
  border-radius: var(--radius-lg);
  min-height: 400px;
}

.graph-sidebar { display: flex; flex-direction: column; gap: 1rem; }

.sidebar-card { padding: 1.25rem; }
.card-header { margin-bottom: 1rem; }
.card-header h4 { font-size: 0.95rem; margin-top: 0.5rem; }

.entity-type-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  font-size: 0.65rem;
  font-weight: 600;
  text-transform: uppercase;
  border-radius: 4px;
  background: var(--neon-cyan-dim);
  color: var(--neon-cyan);
}

.entity-type-badge.person { background: rgba(255, 184, 0, 0.15); color: var(--neon-amber); }
.entity-type-badge.process { background: rgba(0, 255, 136, 0.15); color: var(--neon-green); }
.entity-type-badge.event { background: rgba(255, 0, 170, 0.15); color: var(--neon-magenta); }

.card-body { display: flex; flex-direction: column; gap: 1rem; }

.field { display: flex; flex-direction: column; gap: 0.5rem; }
.field label { font-size: 0.8rem; font-weight: 500; color: var(--text-secondary); }

/* Settings */
.settings-form { max-width: 500px; padding: 2rem; display: flex; flex-direction: column; gap: 1rem; }

/* Status Bar */
.status-bar {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  padding: 0.75rem 1.5rem;
  background: var(--bg-secondary);
  border-top: 1px solid var(--border-color);
}

.status-item { display: flex; align-items: center; gap: 0.5rem; font-size: 0.8rem; }
.status-label { color: var(--text-muted); }
.status-value { color: var(--neon-cyan); font-weight: 500; font-family: 'JetBrains Mono', monospace; }

/* Modal */
.modal { max-width: 400px; padding: 1.5rem; }
.modal-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
.modal-header h2 { font-size: 1.125rem; }
.modal-close { background: transparent; border: none; color: var(--text-muted); cursor: pointer; }
.modal-close:hover { color: var(--text-primary); }
.modal-actions { display: flex; justify-content: flex-end; gap: 0.75rem; margin-top: 1.5rem; }

@media (max-width: 900px) {
  .project-page { grid-template-columns: 1fr; }
  .side-menu { display: none; }
  .graph-panel { grid-template-columns: 1fr; }
  .graph-sidebar { display: none; }
}
</style>