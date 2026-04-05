import api from './index'

export interface LoginParams {
  email: string
  password: string
}

export interface RegisterParams {
  email: string
  password: string
  nickname?: string
}

export interface User {
  id: number
  email: string
  nickname: string
  created_at: string
}

// 注册
export const register = (data: RegisterParams) => {
  return api.post<{ message: string }>('/auth/register', data)
}

// 登录
export const login = (data: LoginParams) => {
  return api.post<{ access_token: string; token_type: string }>('/auth/login', data)
}

// 获取当前用户信息
export const getCurrentUser = () => {
  return api.get<User>('/auth/me')
}

// 更新用户信息
export const updateUserInfo = (data: { nickname?: string }) => {
  return api.put<User>('/auth/me', data)
}