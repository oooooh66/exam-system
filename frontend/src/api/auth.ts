/**
 * 认证相关 API 接口
 */
import request from '@/utils/request'
import type { ApiResponse } from '@/utils/request'

/** 登录请求参数 */
export interface LoginParams {
  username: string
  password: string
}

/** 登录响应数据 */
export interface LoginResponse {
  access: string
  refresh: string
  user?: {
    id: number
    username: string
    role: string
    role_display: string
  }
}

/** 注册请求参数 */
export interface RegisterParams {
  username: string
  password: string
  password_confirm: string
  role: 'student' | 'teacher'
}

/** 用户信息 */
export interface UserProfile {
  id: number
  username: string
  role: string
  email: string
  date_joined: string
}

/**
 * 用户登录
 */
export function loginApi(data: LoginParams) {
  return request.post<ApiResponse<LoginResponse>>('/auth/login/', data)
}

/**
 * 用户注册
 */
export function registerApi(data: RegisterParams) {
  return request.post<ApiResponse<null>>('/auth/register/', data)
}

/**
 * 刷新 Token
 */
export function refreshTokenApi(refresh: string) {
  return request.post<ApiResponse<{ access: string }>>('/auth/token/refresh/', { refresh })
}

/**
 * 获取当前用户信息
 */
export function getUserProfileApi() {
  return request.get<ApiResponse<UserProfile>>('/auth/profile/')
}
