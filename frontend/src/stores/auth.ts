/**
 * 认证状态管理 (Pinia Store)
 *
 * 管理：用户信息、Token、登录状态
 * 持久化到 localStorage，刷新页面不丢失
 */
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { loginApi } from '@/api/auth'

export interface UserInfo {
  id: number
  username: string
  role: 'admin' | 'teacher' | 'student'
  role_display: string
}

export const useAuthStore = defineStore(
  'auth',
  () => {
    // ============================================
    // 状态
    // ============================================
    const accessToken = ref<string>('')
    const refreshToken = ref<string>('')
    const user = ref<UserInfo | null>(null)

    // ============================================
    // 计算属性
    // ============================================
    const isLoggedIn = computed(() => !!accessToken.value && hasValidToken())
    const isAdmin = computed(() => user.value?.role === 'admin')
    const isTeacher = computed(() => user.value?.role === 'teacher')
    const isStudent = computed(() => user.value?.role === 'student')

    // ============================================
    // 初始化：从 localStorage 恢复或 JWT 解析
    // ============================================

    /** 页面刷新时自动恢复用户信息 */
    function initFromStorage() {
      const savedToken = localStorage.getItem('access_token')
      const savedRefresh = localStorage.getItem('refresh_token')
      const savedUser = localStorage.getItem('user_info')

      if (savedToken) {
        accessToken.value = savedToken
        refreshToken.value = savedRefresh || ''

        // 优先从 localStorage 恢复用户
        if (savedUser) {
          try {
            user.value = JSON.parse(savedUser)
          } catch { /* ignore */ }
        }
        // 兜底：从 JWT payload 解析
        if (!user.value) {
          parseUserFromToken(savedToken)
        }
      }
    }

    /** 从 JWT Token 解析用户信息（兜底方案） */
    function parseUserFromToken(token: string) {
      try {
        const payload = JSON.parse(atob(token.split('.')[1]))
        if (payload.username && payload.role) {
          user.value = {
            id: payload.user_id,
            username: payload.username,
            role: payload.role,
            role_display: ({ admin: '管理员', teacher: '教师', student: '学生' } as Record<string, string>)[payload.role] || payload.role,
          }
        }
      } catch { /* ignore */ }
    }

    // ============================================
    // 方法
    // ============================================

    /** 登录 */
    async function login(username: string, password: string) {
      const res = await loginApi({ username, password })
      const data = res.data.data

      accessToken.value = data.access
      refreshToken.value = data.refresh

      // 持久化到 localStorage
      localStorage.setItem('access_token', data.access)
      localStorage.setItem('refresh_token', data.refresh)

      // 保存用户信息
      if (data.user) {
        user.value = data.user as UserInfo
        localStorage.setItem('user_info', JSON.stringify(data.user))
      }

      return data
    }

    /** 登出 */
    function logout() {
      accessToken.value = ''
      refreshToken.value = ''
      user.value = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user_info')
    }

    /** 检查 Token 是否有效 */
    function hasValidToken(): boolean {
      if (!accessToken.value) return false
      try {
        const payload = JSON.parse(atob(accessToken.value.split('.')[1]))
        return payload.exp * 1000 > Date.now()
      } catch {
        return false
      }
    }

    // 页面加载时执行初始化
    initFromStorage()

    return {
      accessToken,
      refreshToken,
      user,
      isLoggedIn,
      isAdmin,
      isTeacher,
      isStudent,
      login,
      logout,
      hasValidToken,
    }
  },
)
