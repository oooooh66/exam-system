<template>
  <div>
    <el-card>
      <template #header><span>我的考试</span></template>
      <el-table v-loading="loading" :data="exams" stripe>
        <el-table-column prop="name" label="考试名称" />
        <el-table-column prop="paper_name" label="试卷" />
        <el-table-column prop="total_score" label="总分" width="80" />
        <el-table-column prop="duration" label="时长(分)" width="90" />
        <el-table-column label="状态" width="90">
          <template #default="{ row }">
            <el-tag :type="statusColor(row.status)" size="small">{{ statusText(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="start_time" label="开始时间" width="160" />
        <el-table-column prop="end_time" label="结束时间" width="160" />
        <el-table-column label="操作" width="140">
          <template #default="{ row }">
            <el-button v-if="row.status === 'ongoing'" type="primary" size="small" @click="$router.push(`/student/exams/${row.id}`)">
              进入考试
            </el-button>
            <el-tag v-else-if="row.status === 'upcoming'" size="small" type="info">未开始</el-tag>
            <el-button v-else size="small" @click="$router.push(`/student/scores?exam=${row.id}`)">
              查看成绩
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getMyExamsApi } from '@/api/exams'

const loading = ref(false)
const exams = ref<any[]>([])

function statusColor(s: string) {
  return { upcoming: 'info', ongoing: 'success', finished: 'default' }[s] || 'info'
}
function statusText(s: string) {
  return { upcoming: '未开始', ongoing: '进行中', finished: '已结束' }[s] || s
}

onMounted(async () => {
  loading.value = true
  try {
    const res = await getMyExamsApi()
    exams.value = res.data.data?.results || []
  } finally { loading.value = false }
})
</script>
