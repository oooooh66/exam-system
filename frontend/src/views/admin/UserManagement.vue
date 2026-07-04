<template>
  <div class="user-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>用户管理</span>
          <el-button type="primary" @click="openDialog()">添加用户</el-button>
        </div>
      </template>
      <el-table v-loading="loading" :data="users" stripe>
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="email" label="邮箱" />
        <el-table-column prop="role_display" label="角色" width="100" />
        <el-table-column label="状态" width="80">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'" size="small">
              {{ row.is_active ? '正常' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="date_joined" label="注册时间" width="160" />
        <el-table-column label="操作" width="180">
          <template #default="{ row }">
            <el-button size="small" @click="openDialog(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 添加/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="editingUser ? '编辑用户' : '添加用户'"
      width="500px"
    >
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" :disabled="!!editingUser" />
        </el-form-item>
        <el-form-item label="密码" :prop="editingUser ? '' : 'password'">
          <el-input v-model="form.password" type="password" :placeholder="editingUser ? '不填则不修改' : '请输入密码'" show-password />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="form.email" />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="form.role" style="width:100%">
            <el-option label="管理员" value="admin" />
            <el-option label="教师" value="teacher" />
            <el-option label="学生" value="student" />
          </el-select>
        </el-form-item>
        <el-form-item label="启用">
          <el-switch v-model="form.is_active" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getUsersApi, createUserApi, updateUserApi, deleteUserApi } from '@/api/users'

const loading = ref(false)
const saving = ref(false)
const users = ref<any[]>([])
const dialogVisible = ref(false)
const editingUser = ref<any>(null)
const formRef = ref()

const form = reactive({
  username: '',
  password: '',
  email: '',
  role: 'student',
  is_active: true,
})

const rules = {
  username: [{ required: true, message: '请输入用户名' }],
  password: [{ required: true, message: '请输入密码', min: 6 }],
  role: [{ required: true, message: '请选择角色' }],
}

async function loadUsers() {
  loading.value = true
  try {
    const res = await getUsersApi()
    users.value = res.data.data?.results || []
  } finally {
    loading.value = false
  }
}

function openDialog(row?: any) {
  editingUser.value = row || null
  if (row) {
    Object.assign(form, {
      username: row.username,
      password: '',
      email: row.email || '',
      role: row.role,
      is_active: row.is_active,
    })
  } else {
    form.username = ''
    form.password = ''
    form.email = ''
    form.role = 'student'
    form.is_active = true
  }
  dialogVisible.value = true
}

async function handleSave() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return
  saving.value = true
  try {
    if (editingUser.value) {
      await updateUserApi(editingUser.value.id, { ...form, password: form.password || undefined })
      ElMessage.success('修改成功')
    } else {
      await createUserApi(form)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadUsers()
  } catch (err: any) {
    ElMessage.error(err?.response?.data?.message || '操作失败')
  } finally {
    saving.value = false
  }
}

async function handleDelete(row: any) {
  await ElMessageBox.confirm(`确定删除用户"${row.username}"吗？`, '确认删除', { type: 'warning' })
  await deleteUserApi(row.id)
  ElMessage.success('已删除')
  loadUsers()
}

onMounted(loadUsers)
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>
