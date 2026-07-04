/**
 * 在线考试系统 - Axios 请求封装
 *
 * 功能：
 * - 统一请求/响应拦截
 * - 自动注入 Token
 * - 401 自动跳转登录
 * - Token 过期自动刷新
 * - 统一错误处理
 */
import axios, {
  type AxiosInstance,
  type AxiosResponse,
  type InternalAxiosRequestConfig,
} from 'axios'
import { ElMessage } from 'element-plus'
import router from '@/router'

/** 后端统一响应格式 */
export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}

/** 分页响应格式 */
export interface PaginatedData<T = any> {
  count: number
  next: string | null
  previous: string | null
  results: T[]
}

// ============================================
// 创建 Axios 实例
// ============================================
const request: AxiosInstance = axios.create({
  baseURL: '/api', // 开发环境由 Vite 代理到 Django
  timeout: 30000, // 30 秒超时
  headers: {
    'Content-Type': 'application/json',
  },
})

// ============================================
// 请求拦截器 —— 自动注入 Token
// ============================================
request.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('access_token')
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// ============================================
// 响应拦截器 —— 统一处理错误
// ============================================
// Token 刷新锁：防止多个请求同时刷新 Token
let isRefreshing = false
let refreshSubscribers: Array<(token: string) => void> = []

/**
 * 将等待中的请求加入队列，Token 刷新后统一执行
 */
function subscribeTokenRefresh(callback: (token: string) => void) {
  refreshSubscribers.push(callback)
}

/**
 * Token 刷新成功后，执行所有等待的请求
 */
function onTokenRefreshed(newToken: string) {
  refreshSubscribers.forEach((callback) => callback(newToken))
  refreshSubscribers = []
}

request.interceptors.response.use(
  (response: AxiosResponse<ApiResponse>) => {
    return response
  },
  async (error) => {
    const originalRequest = error.config
    const status = error.response?.status

    // 401 未认证：尝试刷新 Token
    if (status === 401 && !originalRequest._retry) {
      if (!isRefreshing) {
        isRefreshing = true
        originalRequest._retry = true

        const refreshToken = localStorage.getItem('refresh_token')
        if (refreshToken) {
          try {
            // 调用刷新 Token 接口
            const { data } = await axios.post<ApiResponse<{ access: string }>>(
              '/api/auth/token/refresh/',
              { refresh: refreshToken }
            )

            const newAccessToken = data.data.access
            localStorage.setItem('access_token', newAccessToken)

            // 执行等待队列中的请求
            onTokenRefreshed(newAccessToken)

            // 重试原请求
            originalRequest.headers!.Authorization = `Bearer ${newAccessToken}`
            return request(originalRequest)
          } catch (refreshError) {
            // 刷新失败：清除认证状态，跳转登录
            localStorage.removeItem('access_token')
            localStorage.removeItem('refresh_token')
            localStorage.removeItem('exam-auth')
            router.push({ name: 'Login', query: { redirect: router.currentRoute.value.fullPath } })
            ElMessage.error('登录已过期，请重新登录')
            return Promise.reject(refreshError)
          } finally {
            isRefreshing = false
          }
        } else {
          // 没有 refreshToken：直接跳转登录
          localStorage.removeItem('access_token')
          router.push({ name: 'Login' })
          ElMessage.error('请先登录')
        }
      } else {
        // 正在刷新 Token：加入等待队列
        return new Promise((resolve) => {
          subscribeTokenRefresh((token: string) => {
            originalRequest.headers!.Authorization = `Bearer ${token}`
            resolve(request(originalRequest))
          })
        })
      }
    }

    // 其他错误：统一提示
    const message = error.response?.data?.message || error.message || '网络错误'
    if (status !== 401) {
      ElMessage.error(message)
    }

    return Promise.reject(error)
  }
)

export default request
