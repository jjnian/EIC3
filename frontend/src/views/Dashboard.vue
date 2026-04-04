<template>
  <div class="dashboard">
    <el-container>
      <el-header>
        <h1>OntologyFlow</h1>
        <div class="header-right">
          <span>{{ user?.nickname || user?.email }}</span>
          <el-button @click="logout" text>退出</el-button>
        </div>
      </el-header>
      <el-main>
        <div class="toolbar">
          <h2>我的项目</h2>
          <el-button type="primary" @click="showCreateDialog = true">
            新建项目
          </el-button>
        </div>
        <el-row :gutter="20">
          <el-col :span="6" v-for="project in projects" :key="project.id">
            <el-card class="project-card" @click="$router.push(`/project/${project.id}`)">
              <h3>{{ project.name }}</h3>
              <p>{{ project.description || '暂无描述' }}</p>
              <div class="meta">
                {{ new Date(project.created_at).toLocaleDateString() }}
              </div>
            </el-card>
          </el-col>
        </el-row>
        <el-empty v-if="projects.length === 0" description="暂无项目，点击上方按钮创建" />
      </el-main>
    </el-container>

    <!-- 创建项目对话框 -->
    <el-dialog v-model="showCreateDialog" title="新建项目" width="500px">
      <el-form :model="newProject" label-width="80px">
        <el-form-item label="项目名称" required>
          <el-input v-model="newProject.name" placeholder="请输入项目名称" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="newProject.description" type="textarea" placeholder="请输入项目描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showCreateDialog = false">取消</el-button>
        <el-button type="primary" @click="createProjectHandler" :loading="creating">创建</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getProjects, createProject, type Project } from '@/api/projects'
import { getCurrentUser, type User } from '@/api/auth'

const router = useRouter()
const projects = ref<Project[]>([])
const user = ref<User | null>(null)
const showCreateDialog = ref(false)
const creating = ref(false)

const newProject = reactive({
  name: '',
  description: ''
})

const loadProjects = async () => {
  try {
    projects.value = await getProjects()
  } catch (error) {
    ElMessage.error('加载项目列表失败')
  }
}

const loadUser = async () => {
  try {
    user.value = await getCurrentUser()
  } catch (error) {
    router.push('/login')
  }
}

const createProjectHandler = async () => {
  if (!newProject.name) {
    ElMessage.warning('请输入项目名称')
    return
  }

  creating.value = true
  try {
    await createProject(newProject)
    ElMessage.success('创建成功')
    showCreateDialog.value = false
    newProject.name = ''
    newProject.description = ''
    loadProjects()
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '创建失败')
  } finally {
    creating.value = false
  }
}

const logout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}

onMounted(() => {
  loadUser()
  loadProjects()
})
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background: #f5f7fa;
}

.el-header {
  background: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}

.el-header h1 {
  margin: 0;
  font-size: 1.5rem;
  color: #409eff;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.toolbar h2 {
  margin: 0;
}

.project-card {
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.project-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.project-card h3 {
  margin: 0 0 0.5rem;
  font-size: 1rem;
}

.project-card p {
  color: #909399;
  font-size: 0.875rem;
  margin: 0 0 1rem;
  height: 40px;
  overflow: hidden;
}

.project-card .meta {
  font-size: 0.75rem;
  color: #c0c4cc;
}
</style>