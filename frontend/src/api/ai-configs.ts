import api from './index'

export interface AIConfig {
  id: number
  user_id: number
  model_name: string
  model_id?: string
  api_key: string
  api_endpoint?: string
  is_active: boolean
  created_at: string
}

export interface CreateAIConfigParams {
  model_name: string
  model_id?: string
  api_key: string
  api_endpoint?: string
}

// 获取AI配置列表
export const getAIConfigs = () => {
  return api.get<AIConfig[]>('/ai-configs')
}

// 创建AI配置
export const createAIConfig = (data: CreateAIConfigParams) => {
  return api.post<AIConfig>('/ai-configs', data)
}

// 更新AI配置
export const updateAIConfig = (id: number, data: Partial<CreateAIConfigParams>) => {
  return api.put<AIConfig>(`/ai-configs/${id}`, data)
}

// 删除AI配置
export const deleteAIConfig = (id: number) => {
  return api.delete(`/ai-configs/${id}`)
}