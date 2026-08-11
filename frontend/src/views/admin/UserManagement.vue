<template>
  <div class="user-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>用户管理</span>
          <div style="display:flex;gap:8px">
            <el-button @click="showImportDialog = true">导入考生</el-button>
            <el-button type="primary" @click="openDialog()">添加用户</el-button>
          </div>
        </div>
      </template>
      <el-table v-loading="loading" :data="users" stripe>
        <el-table-column label="序号" width="60" type="index" />
        <el-table-column prop="username" label="用户名" width="110" />
        <el-table-column prop="org_no" label="机构号" width="100" />
        <el-table-column prop="first_name" label="姓名" width="80" />
        <el-table-column prop="org_nm" label="村行" min-width="120" />
        <el-table-column prop="position" label="岗位" width="120" />
        <el-table-column label="分管业务" width="110">
          <template #default="{ row }">
            <template v-if="Array.isArray(row.business_scope) && row.business_scope.length">
              <el-tag v-for="s in row.business_scope" :key="s" size="small" style="margin-right:2px"
                :type="s==='资产'?'warning':s==='负债'?'primary':'info'">
                {{ s }}
              </el-tag>
            </template>
          </template>
        </el-table-column>
        <el-table-column prop="role_display" label="角色" width="70" />
        <el-table-column prop="remark" label="备注" min-width="140" show-overflow-tooltip />
        <el-table-column label="状态" width="70">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'danger'" size="small">
              {{ row.is_active ? '正常' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="date_joined" label="注册时间" width="160" />
        <el-table-column label="操作" width="260" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="openDialog(row)">编辑</el-button>
            <el-button size="small" @click="handleResetPwd(row)">重置密码</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div style="margin-top:16px;display:flex;justify-content:flex-end">
        <el-pagination
          v-model:current-page="page" :page-size="pageSize" :total="total"
          layout="total, prev, pager, next, jumper" @current-change="loadUsers"
        />
      </div>
    </el-card>

    <!-- 添加/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="editingUser ? '编辑用户' : '添加用户'" width="500px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="form.username" :disabled="!!editingUser" />
        </el-form-item>
        <el-form-item label="机构号">
          <el-input v-model="form.org_no" />
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="form.first_name" />
        </el-form-item>
        <el-form-item label="密码" :prop="editingUser ? '' : 'password'">
          <el-input v-model="form.password" type="password" :placeholder="editingUser ? '不填则不修改' : '请输入密码'" show-password />
        </el-form-item>
        <el-form-item label="村行">
          <el-input v-model="form.org_nm" />
        </el-form-item>
        <el-form-item label="岗位">
          <el-input v-model="form.position" />
        </el-form-item>
        <el-form-item label="分管业务">
          <el-checkbox-group v-model="form.business_scope">
            <el-checkbox value="资产">资产</el-checkbox>
            <el-checkbox value="负债">负债</el-checkbox>
            <el-checkbox value="零售">零售</el-checkbox>
          </el-checkbox-group>
        </el-form-item>
        <el-form-item label="备注">
          <el-input v-model="form.remark" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="角色" prop="role">
          <el-select v-model="form.role" style="width:100%">
            <el-option label="管理员" value="admin" />
            <el-option label="评委" value="teacher" />
            <el-option label="考生" value="student" />
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

    <!-- 导入考生对话框 -->
    <el-dialog v-model="showImportDialog" title="导入考生" width="480px">
      <el-upload :auto-upload="false" :limit="1" accept=".xlsx,.xls" :on-change="onFileChange" drag>
        <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
        <div class="el-upload__text">将 Excel 文件拖到此处，或<em>点击上传</em></div>
        <template #tip><div class="el-upload__tip">上传村行高管及业务部负责人考核人员统计表</div></template>
      </el-upload>
      <div v-if="importResult" style="margin-top:12px">
        <el-alert :title="importResult" type="success" :closable="false" />
      </div>
      <template #footer>
        <el-button @click="showImportDialog = false">关闭</el-button>
        <el-button type="primary" :loading="importing" :disabled="!selectedFile" @click="doImport">开始导入</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getUsersApi, createUserApi, updateUserApi, deleteUserApi, resetPasswordApi } from '@/api/users'
import { importCandidatesApi } from '@/api/exams'

const loading = ref(false)
const saving = ref(false)
const users = ref<any[]>([])
const page = ref(1)
const pageSize = ref(20)
const total = ref(0)
const dialogVisible = ref(false)
const editingUser = ref<any>(null)
const formRef = ref()

const form = reactive<any>({
  username: '', password: '', first_name: '', org_no: '', org_nm: '',
  position: '', business_scope: [], remark: '', role: 'student', is_active: true,
})

const rules = {
  username: [{ required: true, message: '请输入用户名' }],
  password: [{ required: true, message: '请输入密码', min: 6 }],
  role: [{ required: true, message: '请选择角色' }],
}

async function loadUsers() {
  loading.value = true
  try {
    const res = await getUsersApi({ page: page.value, page_size: pageSize.value })
    users.value = res.data?.data?.results || res.data?.results || []
    total.value = res.data?.data?.count || res.data?.count || 0
  } finally { loading.value = false }
}

function openDialog(row?: any) {
  editingUser.value = row || null
  if (row) {
    Object.assign(form, {
      username: row.username, password: '',
      first_name: row.first_name || '', org_no: row.org_no || '', org_nm: row.org_nm || '',
      position: row.position || '',
      business_scope: Array.isArray(row.business_scope) ? [...row.business_scope] : [],
      remark: row.remark || '', role: row.role, is_active: row.is_active,
    })
  } else {
    Object.assign(form, {
      username: '', password: '', first_name: '', org_no: '', org_nm: '',
      position: '', business_scope: [], remark: '', role: 'student', is_active: true,
    })
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
  } catch (err: any) { ElMessage.error(err?.response?.data?.message || '操作失败') }
  finally { saving.value = false }
}

async function handleDelete(row: any) {
  await ElMessageBox.confirm(`确定删除用户"${row.username}"吗？`, '确认删除', { type: 'warning' })
  await deleteUserApi(row.id)
  ElMessage.success('已删除')
  loadUsers()
}

async function handleResetPwd(row: any) {
  await ElMessageBox.confirm(`确定将"${row.username}"的密码重置为用户名（${row.username}）吗？`, '重置密码', { type: 'warning' })
  await resetPasswordApi(row.id)
  ElMessage.success('密码已重置')
  loadUsers()
}

// 导入考生（复用考试模块的导入接口）
const showImportDialog = ref(false); const importing = ref(false)
const selectedFile = ref<File | null>(null); const importResult = ref('')

function onFileChange(file: any) { selectedFile.value = file.raw }

async function doImport() {
  if (!selectedFile.value) return
  importing.value = true; importResult.value = ''
  try {
    const res = await importCandidatesApi(selectedFile.value)
    const d = res.data.data
    importResult.value = `导入完成：共 ${d.total} 人（资产${d.by_scope?.asset||0} / 负债${d.by_scope?.liability||0} / 双重${d.by_scope?.both||0}）`
    ElMessage.success(res.data.message)
    showImportDialog.value = false
    loadUsers()
  } catch (err: any) { ElMessage.error(err?.response?.data?.message || '导入失败') }
  finally { importing.value = false }
}

onMounted(loadUsers)
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>
