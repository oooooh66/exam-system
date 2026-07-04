<template>
  <el-container class="dashboard-layout">
    <!-- 侧边栏 -->
    <el-aside :width="isCollapsed ? '64px' : '220px'" class="sidebar">
      <div class="logo">
        <span v-if="!isCollapsed">在线考试系统</span>
        <span v-else class="logo-collapsed">E</span>
      </div>

      <el-menu
        :default-active="activeMenu"
        :collapse="isCollapsed"
        :router="true"
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409EFF"
      >
        <template v-for="item in menuItems" :key="item.index">
          <el-sub-menu v-if="item.children" :index="item.index">
            <template #title>
              <el-icon><component :is="item.icon" /></el-icon>
              <span>{{ item.title }}</span>
            </template>
            <el-menu-item
              v-for="child in item.children"
              :key="child.index"
              :index="child.index"
            >
              <span>{{ child.title }}</span>
            </el-menu-item>
          </el-sub-menu>
          <el-menu-item v-else :index="item.index">
            <el-icon><component :is="item.icon" /></el-icon>
            <span>{{ item.title }}</span>
          </el-menu-item>
        </template>
      </el-menu>
    </el-aside>

    <!-- 主体区域 -->
    <el-container>
      <el-header class="header">
        <div class="header-left">
          <el-button
            text
            @click="isCollapsed = !isCollapsed"
          >
            <el-icon :size="20">
              <Fold v-if="!isCollapsed" />
              <Expand v-else />
            </el-icon>
          </el-button>
        </div>
        <div class="header-right">
          <el-tag :type="roleTagType" size="small">
            {{ authStore.user?.role_display }}
          </el-tag>
          <el-dropdown @command="handleCommand">
            <span class="user-info">
              <el-icon><UserFilled /></el-icon>
              {{ authStore.user?.username }}
              <el-icon><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="logout">
                  <el-icon><SwitchButton /></el-icon>
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </el-header>

      <el-main class="main-content">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

interface MenuItem {
  index: string
  title: string
  icon?: string
  children?: { index: string; title: string }[]
}

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()
const isCollapsed = ref(false)

const activeMenu = computed(() => route.path)

const roleTagType = computed(() => {
  const role = authStore.user?.role
  if (role === 'admin') return 'danger'
  if (role === 'teacher') return 'warning'
  return 'success'
})

/** 根据角色动态生成菜单 */
const menuItems = computed<MenuItem[]>(() => {
  const role = authStore.user?.role

  const adminMenus = [
    { index: '/admin/dashboard', title: '工作台', icon: 'HomeFilled' },
    { index: '/admin/users', title: '用户管理', icon: 'User' },
    {
      index: 'questions-menu',
      title: '题库管理',
      icon: 'Collection',
      children: [
        { index: '/admin/questions', title: '题目列表' },
      ],
    },
    {
      index: 'papers-menu',
      title: '试卷管理',
      icon: 'Document',
      children: [
        { index: '/admin/papers', title: '试卷列表' },
        { index: '/admin/papers/create', title: '创建试卷' },
      ],
    },
    {
      index: 'exams-menu',
      title: '考试管理',
      icon: 'EditPen',
      children: [
        { index: '/admin/exams', title: '考试列表' },
      ],
    },
    { index: '/admin/reports', title: '成绩报表', icon: 'DataAnalysis' },
  ]

  const teacherMenus = [
    { index: '/teacher/dashboard', title: '工作台', icon: 'HomeFilled' },
    { index: '/admin/questions', title: '题库管理', icon: 'Collection' },
    { index: '/admin/papers', title: '试卷管理', icon: 'Document' },
    { index: '/admin/exams', title: '考试管理', icon: 'EditPen' },
    { index: '/admin/reports', title: '成绩统计', icon: 'DataAnalysis' },
  ]

  const studentMenus = [
    { index: '/student/dashboard', title: '工作台', icon: 'HomeFilled' },
    { index: '/student/exams', title: '我的考试', icon: 'EditPen' },
    { index: '/student/scores', title: '我的成绩', icon: 'Trophy' },
  ]

  if (role === 'admin') return adminMenus
  if (role === 'teacher') return teacherMenus
  return studentMenus
})

/** 下拉菜单操作 */
function handleCommand(command: string) {
  if (command === 'logout') {
    authStore.logout()
    router.push('/login')
  }
}
</script>

<style scoped>
.dashboard-layout {
  height: 100vh;
}

.sidebar {
  background-color: #304156;
  overflow-y: auto;
  overflow-x: hidden;
  transition: width 0.3s;
}

.sidebar :deep(.el-menu-item) {
  min-width: 0;
}

.sidebar :deep(.el-menu-item span),
.sidebar :deep(.el-sub-menu__title span) {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 统一图标宽度，让文字标签对齐 */
.sidebar :deep(.el-menu-item .el-icon),
.sidebar :deep(.el-sub-menu__title .el-icon) {
  width: 24px;
  text-align: center;
  flex-shrink: 0;
}

.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 18px;
  font-weight: bold;
  border-bottom: 1px solid rgba(255,255,255,0.1);
}

.logo-collapsed {
  font-size: 24px;
}

.header {
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #e6e6e6;
  padding: 0 20px;
  height: 60px;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  font-size: 14px;
}

.main-content {
  background: #f0f2f5;
  padding: 20px;
  overflow-y: auto;
}

:deep(.el-menu) {
  border-right: none;
}
</style>
