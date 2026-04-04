<template>
  <div class="project-page">
    <el-container>
      <!-- 左侧菜单 -->
      <el-aside width="200px" class="side-menu">
        <div class="menu-header">
          <h3>数据血缘</h3>
        </div>
        <el-menu :default-active="activeMenu" @select="handleMenuSelect">
          <el-menu-item index="datasource">
            <el-icon><Upload /></el-icon>
            <span>数据源</span>
          </el-menu-item>
          <el-menu-item index="tasks">
            <el-icon><List /></el-icon>
            <span>任务</span>
          </el-menu-item>
          <el-menu-item index="graph">
            <el-icon><Share /></el-icon>
            <span>图谱</span>
          </el-menu-item>
          <el-menu-item index="settings">
            <el-icon><Setting /></el-icon>
            <span>设置</span>
          </el-menu-item>
        </el-menu>
        <div class="menu-footer">
          <el-button type="primary" @click="showNewTaskDialog = true">
            <el-icon><Plus /></el-icon>
            新建分析
          </el-button>
        </div>
      </el-aside>

      <!-- 主内容区 -->
      <el-container>
        <!-- 顶部工具栏 -->
        <el-header class="toolbar">
          <div class="toolbar-left">
            <span class="project-name">{{ project?.name }}</span>
            <el-select v-model="selectedTaskId" placeholder="选择任务" clearable style="width: 200px; margin-left: 1rem">
              <el-option
                v-for="task in tasks"
                :key="task.id"
                :label="`任务 #${task.id}`"
                :value="task.id"
              />
            </el-select>
            <el-select v-model="selectedModelId" placeholder="选择模型" style="width: 200px; margin-left: 0.5rem">
              <el-option
                v-for="config in aiConfigs"
                :key="config.id"
                :label="config.model_name"
                :value="config.id"
              />
            </el-select>
          </div>
          <div class="toolbar-right">
            <el-button @click="exportGraph('png')">导出PNG</el-button>
            <el-button @click="exportGraph('json')">导出JSON</el-button>
            <el-button @click="exportGraph('csv')">导出CSV</el-button>
          </div>
        </el-header>

        <!-- 内容区 -->
        <el-main>
          <!-- 数据源面板 -->
          <div v-show="activeMenu === 'datasource'" class="panel">
            <el-upload
              drag
              multiple
              :action="`/api/data-sources/upload?project_id=${projectId}`"
              :headers="{ Authorization: `Bearer ${token}` }"
              :on-success="handleUploadSuccess"
              :on-error="handleUploadError"
              accept="image/*,video/*,.txt,.md"
            >
              <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
              <div class="el-upload__text">
                拖拽文件到此处，或 <em>点击上传</em>
              </div>
              <template #tip>
                <div class="el-upload__tip">
                  支持图片、视频、文本文件
                </div>
              </template>
            </el-upload>
            <el-table :data="dataSources" stripe style="margin-top: 1rem">
              <el-table-column prop="file_name" label="文件名" />
              <el-table-column prop="type" label="类型" width="100" />
              <el-table-column label="操作" width="100">
                <template #default="{ row }">
                  <el-button size="small" text type="danger" @click="deleteDataSource(row.id)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>

          <!-- 任务面板 -->
          <div v-show="activeMenu === 'tasks'" class="panel">
            <el-table :data="tasks" stripe>
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column label="数据源" width="150">
                <template #default="{ row }">
                  {{ getDataSourceName(row.data_source_id) }}
                </template>
              </el-table-column>
              <el-table-column prop="status" label="状态" width="120">
                <template #default="{ row }">
                  <el-tag :type="getStatusType(row.status)">{{ row.status }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="created_at" label="创建时间" width="180">
                <template #default="{ row }">
                  {{ new Date(row.created_at).toLocaleString() }}
                </template>
              </el-table-column>
              <el-table-column label="操作">
                <template #default="{ row }">
                  <el-button size="small" @click="viewTaskResult(row)">查看结果</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>

          <!-- 图谱面板 -->
          <div v-show="activeMenu === 'graph'" class="panel graph-panel">
            <div ref="graphContainer" class="graph-container"></div>
            <!-- 右侧面板 -->
            <div class="side-panel">
              <el-card v-if="selectedEntity" class="entity-card">
                <template #header>
                  <span>实体详情</span>
                </template>
                <el-form label-width="60px">
                  <el-form-item label="名称">
                    <el-input v-model="selectedEntity.name" @change="updateEntity" />
                  </el-form-item>
                  <el-form-item label="类型">
                    <el-select v-model="selectedEntity.type" @change="updateEntity">
                      <el-option label="人物" value="person" />
                      <el-option label="概念" value="concept" />
                      <el-option label="流程" value="process" />
                      <el-option label="物体" value="object" />
                      <el-option label="事件" value="event" />
                    </el-select>
                  </el-form-item>
                  <el-form-item label="描述">
                    <el-input v-model="selectedEntity.description" type="textarea" @change="updateEntity" />
                  </el-form-item>
                  <el-form-item>
                    <el-button type="danger" @click="deleteSelectedEntity">删除</el-button>
                  </el-form-item>
                </el-form>
              </el-card>
              <el-card v-else>
                <template #header>
                  <span>添加实体</span>
                </template>
                <el-form :model="newEntity" label-width="60px">
                  <el-form-item label="名称">
                    <el-input v-model="newEntity.name" />
                  </el-form-item>
                  <el-form-item label="类型">
                    <el-select v-model="newEntity.type">
                      <el-option label="人物" value="person" />
                      <el-option label="概念" value="concept" />
                      <el-option label="流程" value="process" />
                      <el-option label="物体" value="object" />
                      <el-option label="事件" value="event" />
                    </el-select>
                  </el-form-item>
                  <el-form-item>
                    <el-button type="primary" @click="addEntity">添加</el-button>
                  </el-form-item>
                </el-form>
              </el-card>
            </div>
          </div>

          <!-- 设置面板 -->
          <div v-show="activeMenu === 'settings'" class="panel">
            <el-form :model="projectSettings" label-width="100px">
              <el-form-item label="项目名称">
                <el-input v-model="projectSettings.name" />
              </el-form-item>
              <el-form-item label="项目描述">
                <el-input v-model="projectSettings.description" type="textarea" />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="saveProjectSettings">保存</el-button>
              </el-form-item>
            </el-form>
          </div>
        </el-main>

        <!-- 底部状态栏 -->
        <el-footer class="status-bar">
          <span>实体数: {{ entities.length }}</span>
          <span style="margin-left: 1rem">关系数: {{ relations.length }}</span>
          <span style="margin-left: 1rem">最后保存: {{ lastSaved }}</span>
        </el-footer>
      </el-container>
    </el-container>

    <!-- 新建分析任务对话框 -->
    <el-dialog v-model="showNewTaskDialog" title="新建分析任务" width="500px">
      <el-form :model="newTask" label-width="80px">
        <el-form-item label="数据源" required>
          <el-select v-model="newTask.data_source_id" placeholder="选择数据源" style="width: 100%">
            <el-option
              v-for="ds in dataSources"
              :key="ds.id"
              :label="ds.file_name || '文字输入'"
              :value="ds.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="AI模型">
          <el-select v-model="newTask.ai_config_id" placeholder="选择模型" style="width: 100%">
            <el-option
              v-for="config in aiConfigs"
              :key="config.id"
              :label="config.model_name"
              :value="config.id"
            />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showNewTaskDialog = false">取消</el-button>
        <el-button type="primary" @click="createTaskHandler" :loading="creatingTask">创建</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, watch, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Upload, List, Share, Setting, Plus, UploadFilled } from '@element-plus/icons-vue'
import { Graph } from '@antv/x6'
import api from '@/api'
import { getProject, type Project } from '@/api/projects'
import { getAIConfigs, type AIConfig } from '@/api/ai-configs'

interface DataSource {
  id: number
  type: string
  file_name: string
  file_path: string
  content: string
}

interface Task {
  id: number
  data_source_id: number
  ai_config_id: number
  status: string
  created_at: string
}

interface Entity {
  id: number
  name: string
  type: string
  description: string
  position_x: number
  position_y: number
}

interface Relation {
  id: number
  source_entity_id: number
  target_entity_id: number
  relation_type: string
}

const route = useRoute()
const router = useRouter()
const projectId = Number(route.params.id)
const token = localStorage.getItem('token') || ''

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

const newTask = reactive({
  data_source_id: null as number | null,
  ai_config_id: null as number | null
})

const newEntity = reactive({
  name: '',
  type: 'concept'
})

const projectSettings = reactive({
  name: '',
  description: ''
})

const graphContainer = ref<HTMLElement | null>(null)
let graph: Graph | null = null

// 菜单切换
const handleMenuSelect = (index: string) => {
  activeMenu.value = index
}

// 加载项目数据
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

// 加载AI配置
const loadAIConfigs = async () => {
  try {
    aiConfigs.value = await getAIConfigs()
  } catch (error) {
    console.error('加载AI配置失败')
  }
}

// 加载数据源
const loadDataSources = async () => {
  try {
    dataSources.value = await api.get<DataSource[]>(`/data-sources?project_id=${projectId}`)
  } catch (error) {
    console.error('加载数据源失败')
  }
}

// 加载任务
const loadTasks = async () => {
  try {
    tasks.value = await api.get<Task[]>(`/tasks?project_id=${projectId}`)
  } catch (error) {
    console.error('加载任务失败')
  }
}

// 加载图谱数据
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
  } catch (error) {
    console.error('加载图谱数据失败')
  }
}

// 初始化图谱
const initGraph = () => {
  if (!graphContainer.value) return

  graph = new Graph({
    container: graphContainer.value,
    grid: true,
    panning: true,
    mousewheel: true,
    connecting: {
      anchor: 'center',
      connectionPoint: 'anchor',
      snap: true
    }
  })

  graph.on('node:click', ({ node }) => {
    const entityId = Number(node.id)
    selectedEntity.value = entities.value.find(e => e.id === entityId) || null
  })

  graph.on('node:moved', ({ node }) => {
    const entityId = Number(node.id)
    const entity = entities.value.find(e => e.id === entityId)
    if (entity) {
      entity.position_x = node.position().x
      entity.position_y = node.position().y
      updateEntityPosition(entity)
    }
  })
}

// 渲染图谱
const renderGraph = () => {
  if (!graph) return

  graph.clearCells()

  // 添加节点
  entities.value.forEach((entity, index) => {
    graph!.addNode({
      id: String(entity.id),
      shape: 'rect',
      x: entity.position_x || 100 + (index % 5) * 200,
      y: entity.position_y || 100 + Math.floor(index / 5) * 100,
      width: 120,
      height: 40,
      attrs: {
        body: {
          fill: '#f0f5ff',
          stroke: '#1890ff',
          rx: 4,
          ry: 4
        },
        label: {
          text: entity.name,
          fill: '#333'
        }
      }
    })
  })

  // 添加边
  relations.value.forEach(relation => {
    graph!.addEdge({
      source: String(relation.source_entity_id),
      target: String(relation.target_entity_id),
      attrs: {
        line: {
          stroke: '#1890ff',
          strokeWidth: 2
        }
      },
      labels: [{
        attrs: {
          text: {
            text: relation.relation_type
          }
        }
      }]
    })
  })
}

// 更新实体
const updateEntity = async () => {
  if (!selectedEntity.value) return
  try {
    await api.put(`/graph/entities/${selectedEntity.value.id}`, selectedEntity.value)
    lastSaved.value = new Date().toLocaleTimeString()
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

// 更新实体位置
const updateEntityPosition = async (entity: Entity) => {
  try {
    await api.put(`/graph/entities/${entity.id}`, {
      position_x: entity.position_x,
      position_y: entity.position_y
    })
  } catch (error) {
    console.error('更新位置失败')
  }
}

// 添加实体
const addEntity = async () => {
  if (!newEntity.name || !selectedTaskId.value) return
  try {
    const entity = await api.post<Entity>('/graph/entities', {
      task_id: selectedTaskId.value,
      ...newEntity,
      is_user_created: true
    })
    entities.value.push(entity)
    renderGraph()
    newEntity.name = ''
    newEntity.type = 'concept'
  } catch (error) {
    ElMessage.error('添加失败')
  }
}

// 删除选中实体
const deleteSelectedEntity = async () => {
  if (!selectedEntity.value) return
  try {
    await api.delete(`/graph/entities/${selectedEntity.value.id}`)
    entities.value = entities.value.filter(e => e.id !== selectedEntity.value!.id)
    selectedEntity.value = null
    renderGraph()
  } catch (error) {
    ElMessage.error('删除失败')
  }
}

// 创建任务
const createTaskHandler = async () => {
  if (!newTask.data_source_id) {
    ElMessage.warning('请选择数据源')
    return
  }

  creatingTask.value = true
  try {
    const task = await api.post<Task>('/tasks', {
      project_id: projectId,
      ...newTask
    })
    tasks.value.push(task)
    showNewTaskDialog.value = false
    ElMessage.success('任务创建成功，正在分析...')
  } catch (error) {
    ElMessage.error('创建任务失败')
  } finally {
    creatingTask.value = false
  }
}

// 查看任务结果
const viewTaskResult = (task: Task) => {
  selectedTaskId.value = task.id
  activeMenu.value = 'graph'
  loadGraphData()
}

// 上传成功
const handleUploadSuccess = () => {
  ElMessage.success('上传成功')
  loadDataSources()
}

// 上传失败
const handleUploadError = () => {
  ElMessage.error('上传失败')
}

// 删除数据源
const deleteDataSource = async (id: number) => {
  try {
    await api.delete(`/data-sources/${id}`)
    dataSources.value = dataSources.value.filter(d => d.id !== id)
    ElMessage.success('删除成功')
  } catch (error) {
    ElMessage.error('删除失败')
  }
}

// 获取数据源名称
const getDataSourceName = (id: number) => {
  const ds = dataSources.value.find(d => d.id === id)
  return ds?.file_name || '文字输入'
}

// 获取状态类型
const getStatusType = (status: string) => {
  const map: Record<string, string> = {
    pending: 'info',
    running: 'warning',
    completed: 'success',
    failed: 'danger'
  }
  return map[status] || 'info'
}

// 导出图谱
const exportGraph = async (format: string) => {
  if (!selectedTaskId.value) {
    ElMessage.warning('请先选择任务')
    return
  }
  try {
    const response = await api.post(`/graph/export?task_id=${selectedTaskId.value}&format=${format}`, {})
    if (format === 'png' && graph) {
      graph.toPNG((dataUri) => {
        const link = document.createElement('a')
        link.download = 'graph.png'
        link.href = dataUri
        link.click()
      })
    } else {
      const blob = new Blob([JSON.stringify(response, null, 2)], { type: 'application/json' })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.download = `graph.${format}`
      link.href = url
      link.click()
    }
  } catch (error) {
    ElMessage.error('导出失败')
  }
}

// 保存项目设置
const saveProjectSettings = async () => {
  try {
    await api.put(`/projects/${projectId}`, projectSettings)
    if (project.value) {
      project.value.name = projectSettings.name
      project.value.description = projectSettings.description
    }
    ElMessage.success('保存成功')
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

// 监听任务选择
watch(selectedTaskId, () => {
  loadGraphData()
})

// 初始化
onMounted(async () => {
  await Promise.all([
    loadProject(),
    loadAIConfigs(),
    loadDataSources(),
    loadTasks()
  ])
  await nextTick()
  initGraph()
})
</script>

<style scoped>
.project-page {
  height: 100vh;
}

.side-menu {
  background: #304156;
  display: flex;
  flex-direction: column;
}

.menu-header {
  padding: 1rem;
  color: white;
  border-bottom: 1px solid #3a4a5b;
}

.menu-header h3 {
  margin: 0;
}

.side-menu .el-menu {
  border-right: none;
  background: transparent;
}

.side-menu :deep(.el-menu-item) {
  color: #bfcbd9;
}

.side-menu :deep(.el-menu-item:hover),
.side-menu :deep(.el-menu-item.is-active) {
  background: #263445;
}

.menu-footer {
  padding: 1rem;
  margin-top: auto;
}

.toolbar {
  background: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1rem;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}

.toolbar-left {
  display: flex;
  align-items: center;
}

.project-name {
  font-size: 1.25rem;
  font-weight: 500;
}

.toolbar-right {
  display: flex;
  gap: 0.5rem;
}

.panel {
  padding: 1rem;
  background: white;
  border-radius: 4px;
  height: 100%;
}

.graph-panel {
  display: flex;
  gap: 1rem;
}

.graph-container {
  flex: 1;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
}

.side-panel {
  width: 300px;
}

.status-bar {
  background: #f5f7fa;
  display: flex;
  align-items: center;
  padding: 0 1rem;
  font-size: 0.875rem;
  color: #909399;
}

:deep(.el-aside) {
  overflow: hidden;
}
</style>