<template>
  <div class="register-container">
    <el-card class="register-card">
      <template #header>
        <h2 class="register-title">创建账号</h2>
        <p class="register-subtitle">注册在线考试系统账号</p>
      </template>

      <el-form ref="formRef" :model="form" :rules="rules" label-width="0">
        <el-form-item prop="username">
          <el-input v-model="form.username" placeholder="用户名（3-150字符）" size="large" />
        </el-form-item>

        <el-form-item prop="password">
          <el-input v-model="form.password" type="password" placeholder="密码（至少6位）" size="large" show-password />
        </el-form-item>

        <el-form-item prop="password_confirm">
          <el-input v-model="form.password_confirm" type="password" placeholder="确认密码" size="large" show-password />
        </el-form-item>

        <el-form-item prop="role">
          <el-select v-model="form.role" placeholder="选择角色" size="large" style="width:100%">
            <el-option label="学生" value="student" />
            <el-option label="教师" value="teacher" />
          </el-select>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" size="large" :loading="loading" style="width:100%" @click="handleRegister">
            {{ loading ? '注册中...' : '注册' }}
          </el-button>
        </el-form-item>
      </el-form>

      <div class="register-footer">
        <span>已有账号？</span>
        <el-link type="primary" :underline="false" @click="$router.push('/login')">去登录</el-link>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { registerApi } from '@/api/auth'

const router = useRouter()
const formRef = ref()
const loading = ref(false)

const form = reactive({
  username: '',
  password: '',
  password_confirm: '',
  role: 'student',
})

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }, { min: 3, message: '至少3个字符', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }, { min: 6, message: '至少6位', trigger: 'blur' }],
  password_confirm: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: (_rule: any, value: string, cb: any) => value === form.password ? cb() : cb(new Error('两次密码不一致')), trigger: 'blur' },
  ],
  role: [{ required: true, message: '请选择角色', trigger: 'change' }],
}

async function handleRegister() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return

  loading.value = true
  try {
    await registerApi({
      username: form.username,
      password: form.password,
      password_confirm: form.password_confirm,
      role: form.role as 'student' | 'teacher',
    })
    ElMessage.success('注册成功，请登录')
    router.push('/login')
  } catch (err: any) {
    ElMessage.error(err?.response?.data?.message || '注册失败')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
.register-card {
  width: 420px;
  border-radius: 12px;
}
.register-title { text-align: center; margin: 0 0 8px; }
.register-subtitle { text-align: center; color: #909399; font-size: 14px; margin: 0; }
.register-footer { text-align: center; font-size: 14px; color: #909399; }
</style>
