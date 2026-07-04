/**
 * 在线考试系统 - 路由配置
 *
 * 路由结构：
 * - /login, /register              公开页面
 * - /admin/*                        管理员路由（需 admin 角色）
 * - /teacher/*                      教师路由（需 teacher/admin 角色）
 * - /student/*                      学生路由（需 student 角色）
 */
import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

// 懒加载页面组件
const LoginView = () => import('@/views/auth/LoginView.vue')
const RegisterView = () => import('@/views/auth/RegisterView.vue')
const DashboardLayout = () => import('@/layouts/DashboardLayout.vue')
const NotFoundView = () => import('@/views/NotFoundView.vue')

const routes: RouteRecordRaw[] = [
  // ============================================
  // 公开页面（无需登录）
  // ============================================
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
    meta: { guest: true },
  },
  {
    path: '/register',
    name: 'Register',
    component: RegisterView,
    meta: { guest: true },
  },

  // ============================================
  // 需要登录的页面
  // ============================================
  {
    path: '/',
    component: DashboardLayout,
    meta: { requiresAuth: true },
    redirect: (to) => {
      const auth = useAuthStore()
      const role = auth.user?.role
      if (role === 'admin') return '/admin/dashboard'
      if (role === 'teacher') return '/teacher/dashboard'
      if (role === 'student') return '/student/dashboard'
      return '/login'
    },
    children: [
      // ---------- 管理员页面 ----------
      {
        path: 'admin',
        redirect: '/admin/dashboard',
      },
      {
        path: 'admin/dashboard',
        name: 'AdminDashboard',
        component: () => import('@/views/admin/DashboardView.vue'),
        meta: { roles: ['admin'] },
      },
      {
        path: 'admin/users',
        name: 'UserManagement',
        component: () => import('@/views/admin/UserManagement.vue'),
        meta: { roles: ['admin'] },
      },
      {
        path: 'admin/questions',
        name: 'AdminQuestions',
        component: () => import('@/views/admin/QuestionManagement.vue'),
        meta: { roles: ['admin', 'teacher'] },
      },
      {
        path: 'admin/papers',
        name: 'AdminPapers',
        component: () => import('@/views/admin/PaperManagement.vue'),
        meta: { roles: ['admin', 'teacher'] },
      },
      {
        path: 'admin/papers/create',
        name: 'PaperCreate',
        component: () => import('@/views/admin/PaperEditor.vue'),
        meta: { roles: ['admin', 'teacher'] },
      },
      {
        path: 'admin/papers/:id/edit',
        name: 'PaperEdit',
        component: () => import('@/views/admin/PaperEditor.vue'),
        meta: { roles: ['admin', 'teacher'] },
      },
      {
        path: 'admin/exams',
        name: 'AdminExams',
        component: () => import('@/views/admin/ExamManagement.vue'),
        meta: { roles: ['admin', 'teacher'] },
      },
      {
        path: 'admin/reports',
        name: 'AdminReports',
        component: () => import('@/views/admin/ScoreReports.vue'),
        meta: { roles: ['admin', 'teacher'] },
      },

      // ---------- 教师页面 ----------
      {
        path: 'teacher',
        redirect: '/teacher/dashboard',
      },
      {
        path: 'teacher/dashboard',
        name: 'TeacherDashboard',
        component: () => import('@/views/teacher/DashboardView.vue'),
        meta: { roles: ['admin', 'teacher'] },
      },

      // ---------- 学生页面 ----------
      {
        path: 'student',
        redirect: '/student/dashboard',
      },
      {
        path: 'student/dashboard',
        name: 'StudentDashboard',
        component: () => import('@/views/student/DashboardView.vue'),
        meta: { roles: ['student'] },
      },
      {
        path: 'student/exams',
        name: 'StudentExams',
        component: () => import('@/views/student/ExamListView.vue'),
        meta: { roles: ['student'] },
      },
      {
        path: 'student/exams/:id',
        name: 'ExamTaking',
        component: () => import('@/views/student/ExamTakingView.vue'),
        meta: { roles: ['student'] },
      },
      {
        path: 'student/scores',
        name: 'StudentScores',
        component: () => import('@/views/student/MyScoresView.vue'),
        meta: { roles: ['student'] },
      },
    ],
  },

  // ============================================
  // 404 页面
  // ============================================
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFoundView,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// ============================================
// 全局路由守卫
// ============================================
router.beforeEach((to, _from, next) => {
  const authStore = useAuthStore()

  // 检查 Token 是否有效
  if (authStore.accessToken && !authStore.user && !authStore.hasValidToken()) {
    authStore.logout()
  }

  // 需要认证但未登录 → 跳转登录页
  if (to.matched.some((r) => r.meta.requiresAuth)) {
    if (!authStore.isLoggedIn || !authStore.hasValidToken()) {
      authStore.logout()
      return next({ name: 'Login', query: { redirect: to.fullPath } })
    }
  }

  // 已登录但访问 guest 页面 → 跳转首页
  if (to.meta.guest && authStore.isLoggedIn) {
    const role = authStore.user?.role
    if (role === 'admin') return next('/admin/dashboard')
    if (role === 'teacher') return next('/teacher/dashboard')
    return next('/student/dashboard')
  }

  // 角色权限校验
  if (to.meta.roles) {
    const allowedRoles = to.meta.roles as string[]
    const userRole = authStore.user?.role
    if (userRole && !allowedRoles.includes(userRole)) {
      return next({ name: 'NotFound' })
    }
  }

  next()
})

export default router
