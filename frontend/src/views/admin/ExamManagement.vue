<template>
  <div class="exam-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>考试管理</span>
          <el-button type="primary" @click="openDialog()">发布考试</el-button>
        </div>
      </template>
      <el-table v-loading="loading" :data="exams" stripe>
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="name" label="考试名称" />
        <el-table-column prop="paper_name" label="试卷" />
        <el-table-column prop="total_score" label="总分" width="70" />
        <el-table-column prop="duration" label="时长(分)" width="80" />
        <el-table-column label="状态" width="90">
          <template #default="{ row }">
            <el-tag :type="statusType(row.status)" size="small">{{ statusText(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="start_time" label="开始时间" width="160" />
        <el-table-column prop="end_time" label="结束时间" width="160" />
        <el-table-column label="操作" width="160">
          <template #default="{ row }">
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 发布考试对话框 -->
    <el-dialog v-model="dialogVisible" title="发布考试" width="500px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="考试名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="选择试卷" prop="paper">
          <el-select v-model="form.paper" filterable style="width:100%">
            <el-option v-for="p in papers" :key="p.id" :label="p.name" :value="p.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="开始时间" prop="start_time">
          <el-date-picker v-model="form.start_time" type="datetime" placeholder="选择开始时间" style="width:100%" />
        </el-form-item>
        <el-form-item label="结束时间" prop="end_time">
          <el-date-picker v-model="form.end_time" type="datetime" placeholder="选择结束时间" style="width:100%" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="handleCreate">发布</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getExamsApi, createExamApi, deleteExamApi } from '@/api/exams'
import { getPapersApi } from '@/api/papers'

const loading = ref(false)
const saving = ref(false)
const dialogVisible = ref(false)
const exams = ref<any[]>([])
const papers = ref<any[]>([])
const formRef = ref()

const form = reactive({
  name: '',
  paper: null as number | null,
  start_time: '',
  end_time: '',
})

const rules = {
  name: [{ required: true, message: '请输入考试名称' }],
  paper: [{ required: true, message: '请选择试卷' }],
  start_time: [{ required: true, message: '请选择开始时间' }],
  end_time: [{ required: true, message: '请选择结束时间' }],
}

function statusType(s: string) {
  return { upcoming: 'info', ongoing: 'success', finished: 'default' }[s] || 'info'
}
function statusText(s: string) {
  return { upcoming: '未开始', ongoing: '进行中', finished: '已结束' }[s] || s
}

async function loadExams() {
  loading.value = true
  try {
    const res = await getExamsApi()
    exams.value = res.data.data?.results || []
  } finally { loading.value = false }
}

async function loadPapers() {
  const res = await getPapersApi()
  papers.value = res.data.data?.results || []
}

function openDialog() {
  form.name = ''
  form.paper = null
  form.start_time = ''
  form.end_time = ''
  dialogVisible.value = true
}

async function handleCreate() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return
  saving.value = true
  try {
    await createExamApi({
      name: form.name,
      paper: form.paper,
      start_time: new Date(form.start_time).toISOString(),
      end_time: new Date(form.end_time).toISOString(),
    })
    ElMessage.success('考试发布成功')
    dialogVisible.value = false
    loadExams()
  } catch (err: any) {
    ElMessage.error(err?.response?.data?.message || '发布失败')
  } finally { saving.value = false }
}

async function handleDelete(row: any) {
  await ElMessageBox.confirm(`确定删除"${row.name}"吗？`, '确认', { type: 'warning' })
  await deleteExamApi(row.id)
  ElMessage.success('已删除')
  loadExams()
}

onMounted(() => { loadExams(); loadPapers() })
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>
