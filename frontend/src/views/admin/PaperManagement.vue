<template>
  <div class="paper-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>试卷管理</span>
          <el-button type="primary" @click="$router.push('/admin/papers/create')">创建试卷</el-button>
        </div>
      </template>
      <el-table v-loading="loading" :data="papers" stripe>
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="name" label="试卷名称" />
        <el-table-column prop="question_count" label="题目数" width="80" />
        <el-table-column prop="total_score" label="总分" width="80" />
        <el-table-column prop="pass_score" label="及格分" width="80" />
        <el-table-column prop="duration_minutes" label="时长(分)" width="90" />
        <el-table-column prop="created_by_name" label="创建人" width="100" />
        <el-table-column prop="created_at" label="创建时间" width="160" />
        <el-table-column label="操作" width="200">
          <template #default="{ row }">
            <el-button size="small" @click="$router.push(`/admin/papers/${row.id}/edit`)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getPapersApi, deletePaperApi } from '@/api/papers'

const loading = ref(false)
const papers = ref<any[]>([])

async function loadPapers() {
  loading.value = true
  try {
    const res = await getPapersApi()
    papers.value = res.data.data?.results || []
  } finally { loading.value = false }
}

async function handleDelete(row: any) {
  await ElMessageBox.confirm(`确定删除试卷"${row.name}"吗？`, '确认', { type: 'warning' })
  await deletePaperApi(row.id)
  ElMessage.success('已删除')
  loadPapers()
}

onMounted(loadPapers)
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>
