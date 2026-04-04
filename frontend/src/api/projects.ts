import api from './index'

export interface Project {
  id: number
  user_id: number
  name: string
  description?: string
  default_model_config_id?: number
  created_at: string
  updated_at: string
}

export interface CreateProjectParams {
  name: string
  description?: string
  default_model_config_id?: number
}

// 获取项目列表
export const getProjects = () => {
  return api.get<Project[]>('/projects')
}

// 创建项目
export const createProject = (data: CreateProjectParams) => {
  return api.post<Project>('/projects', data)
}

// 获取项目详情
export const getProject = (id: number) => {
  return api.get<Project>(`/projects/${id}`)
}

// 更新项目
export const updateProject = (id: number, data: Partial<CreateProjectParams>) => {
  return api.put<Project>(`/projects/${id}`, data)
}

// 删除项目
export const deleteProject = (id: number) => {
  return api.delete(`/projects/${id}`)
}