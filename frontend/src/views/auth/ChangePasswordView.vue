<template>
  <div class="change-pwd-container">
    <el-card class="change-pwd-card">
      <template #header>
        <h2>首次登录 - 修改初始密码</h2>
        <p style="color:#909399;font-size:13px;margin-top:4px">
          您的初始密码与用户名相同，为保障账号安全，请先修改密码再使用系统
        </p>
      </template>
      <el-form ref="formRef" :model="form" :rules="rules" label-width="0" @submit.prevent="handleSubmit">
        <el-form-item prop="new_password">
          <el-input v-model="form.new_password" type="password" placeholder="新密码（至少6位）"
            :prefix-icon="Lock" size="large" show-password />
        </el-form-item>
        <el-form-item prop="new_password_confirm">
          <el-input v-model="form.new_password_confirm" type="password" placeholder="确认新密码"
            :prefix-icon="Lock" size="large" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" size="large" :loading="loading" style="width:100%"
            @click="handleSubmit" native-type="submit">
            确认修改
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Lock } from '@element-plus/icons-vue'
import { changeInitialPasswordApi } from '@/api/auth'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const loading = ref(false)
const formRef = ref()

const form = reactive({ new_password: '', new_password_confirm: '' })
const rules = {
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码至少6位', trigger: 'blur' },
  ],
  new_password_confirm: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    {
      validator: (_: any, v: string, cb: any) =>
        v === form.new_password ? cb() : cb(new Error('两次密码不一致')),
      trigger: 'blur',
    },
  ],
}

async function handleSubmit() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return
  loading.value = true
  try {
    await changeInitialPasswordApi({ new_password: form.new_password, new_password_confirm: form.new_password_confirm })
    ElMessage.success('密码修改成功，请重新登录')
    authStore.logout()
    router.push('/login')
  } catch (err: any) {
    ElMessage.error(err?.response?.data?.message || '修改失败')
  } finally { loading.value = false }
}
</script>

<style scoped>
.change-pwd-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f7fa;
}
.change-pwd-card {
  width: 420px;
}
</style>
