<template>
  <div class="settings">
    <el-container>
      <el-header>
        <h1>OntologyFlow</h1>
        <div class="header-right">
          <el-button @click="$router.push('/dashboard')" text>返回</el-button>
        </div>
      </el-header>
      <el-main>
        <h2>AI 模型配置</h2>
        <el-button type="primary" @click="showAddDialog = true" style="margin-bottom: 1rem">
          添加模型配置
        </el-button>

        <el-table :data="configs" stripe>
          <el-table-column prop="model_name" label="模型" width="150" />
          <el-table-column label="API Key" width="300">
            <template #default="{ row }">
              <span>{{ row.api_key ? '••••••••' + row.api_key.slice(-4) : '未设置' }}</span>
            </template>
          </el-table-column>
          <el-table-column prop="api_endpoint" label="自定义端点" />
          <el-table-column prop="is_active" label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="row.is_active ? 'success' : 'info'">
                {{ row.is_active ? '启用' : '禁用' }}
              </el-tag>
            </template>
          </el-table-column>
          <el-table-column label="操作" width="150">
            <template #default="{ row }">
              <el-button size="small" text type="primary" @click="editConfig(row)">编辑</el-button>
              <el-button size="small" text type="danger" @click="deleteConfigHandler(row.id)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </el-main>
    </el-container>

    <!-- 添加/编辑对话框 -->
    <el-dialog v-model="showAddDialog" :title="editingId ? '编辑配置' : '添加配置'" width="500px">
      <el-form :model="configForm" label-width="100px">
        <el-form-item label="模型" required>
          <el-select v-model="configForm.model_name" placeholder="选择模型" style="width: 100%">
            <el-option label="Claude (Anthropic)" value="claude" />
            <el-option label="GPT-4V / GPT-4o (OpenAI)" value="openai" />
            <el-option label="Gemini (Google)" value="gemini" />
            <el-option label="GLM-4V (智谱AI)" value="glm" />
            <el-option label="Qwen-VL (阿里云)" value="qwen" />
            <el-option label="DeepSeek" value="deepseek" />
            <el-option label="本地模型" value="local" />
          </el-select>
        </el-form-item>
        <el-form-item label="API Key">
          <el-input v-model="configForm.api_key" placeholder="请输入API Key" show-password />
        </el-form-item>
        <el-form-item label="自定义端点">
          <el-input v-model="configForm.api_endpoint" placeholder="可选，用于本地模型或代理" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAddDialog = false">取消</el-button>
        <el-button type="primary" @click="saveConfig" :loading="saving">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getAIConfigs, createAIConfig, updateAIConfig, deleteAIConfig, type AIConfig } from '@/api/ai-configs'

const configs = ref<AIConfig[]>([])
const showAddDialog = ref(false)
const saving = ref(false)
const editingId = ref<number | null>(null)

const configForm = reactive({
  model_name: '',
  api_key: '',
  api_endpoint: ''
})

const loadConfigs = async () => {
  try {
    configs.value = await getAIConfigs()
  } catch (error) {
    ElMessage.error('加载配置失败')
  }
}

const editConfig = (config: AIConfig) => {
  editingId.value = config.id
  configForm.model_name = config.model_name
  configForm.api_key = ''
  configForm.api_endpoint = config.api_endpoint || ''
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
      await updateAIConfig(editingId.value, configForm)
      ElMessage.success('更新成功')
    } else {
      await createAIConfig(configForm)
      ElMessage.success('添加成功')
    }
    showAddDialog.value = false
    resetForm()
    loadConfigs()
  } catch (error: any) {
    ElMessage.error(error.response?.data?.detail || '保存失败')
  } finally {
    saving.value = false
  }
}

const deleteConfigHandler = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定删除此配置？', '提示', { type: 'warning' })
    await deleteAIConfig(id)
    ElMessage.success('删除成功')
    loadConfigs()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const resetForm = () => {
  editingId.value = null
  configForm.model_name = ''
  configForm.api_key = ''
  configForm.api_endpoint = ''
}

onMounted(() => {
  loadConfigs()
})
</script>

<style scoped>
.settings {
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

h2 {
  margin-bottom: 1rem;
}
</style>