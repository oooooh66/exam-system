<template>
  <div class="score-reports">
    <el-card>
      <template #header><span>成绩报表</span></template>

      <el-form :inline="true">
        <el-form-item label="选择考试">
          <el-select v-model="selectedExamId" filterable placeholder="请选择" @change="loadStats" style="width:300px">
            <el-option v-for="exam in exams" :key="exam.id" :label="exam.name" :value="exam.id" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadStats">查询</el-button>
          <el-button v-if="selectedExamId" @click="exportScores">导出Excel</el-button>
        </el-form-item>
      </el-form>

      <template v-if="stats">
        <!-- 概览卡片 -->
        <el-row :gutter="16" style="margin-bottom:20px">
          <el-col :span="4">
            <el-card shadow="hover"><div class="stat-item"><div class="stat-value">{{ stats.total_students }}</div><div class="stat-label">参考人数</div></div></el-card>
          </el-col>
          <el-col :span="4">
            <el-card shadow="hover"><div class="stat-item"><div class="stat-value">{{ stats.average_score }}</div><div class="stat-label">平均分</div></div></el-card>
          </el-col>
          <el-col :span="4">
            <el-card shadow="hover"><div class="stat-item"><div class="stat-value">{{ stats.max_score }}</div><div class="stat-label">最高分</div></div></el-card>
          </el-col>
          <el-col :span="4">
            <el-card shadow="hover"><div class="stat-item"><div class="stat-value">{{ stats.min_score }}</div><div class="stat-label">最低分</div></div></el-card>
          </el-col>
          <el-col :span="4">
            <el-card shadow="hover"><div class="stat-item"><div class="stat-value">{{ stats.pass_rate }}%</div><div class="stat-label">及格率</div></div></el-card>
          </el-col>
        </el-row>

        <!-- 学生成绩表 -->
        <el-table :data="stats.student_scores" stripe>
          <el-table-column label="排名" type="index" width="60" />
          <el-table-column prop="student_name" label="学生" />
          <el-table-column label="得分" width="100">
            <template #default="{ row }"><b>{{ row.total_score }}</b></template>
          </el-table-column>
          <el-table-column prop="submit_time" label="提交时间" width="160" />
          <el-table-column label="状态" width="100">
            <template #default="{ row }">
              <el-tag :type="row.status === 'submitted' ? 'success' : 'warning'" size="small">
                {{ row.status === 'submitted' ? '正常提交' : '自动提交' }}
              </el-tag>
            </template>
          </el-table-column>
        </el-table>
      </template>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getExamsApi } from '@/api/exams'
import { getExamStatisticsApi, getExportUrl } from '@/api/reports'

const exams = ref<any[]>([])
const selectedExamId = ref<number | null>(null)
const stats = ref<any>(null)

async function loadExams() {
  const res = await getExamsApi()
  exams.value = res.data.data?.results || []
}

async function loadStats() {
  if (!selectedExamId.value) return
  try {
    const res = await getExamStatisticsApi(selectedExamId.value)
    stats.value = res.data.data
  } catch (err: any) {
    ElMessage.error('获取统计数据失败')
  }
}

function exportScores() {
  if (!selectedExamId.value) return
  window.open(getExportUrl(selectedExamId.value), '_blank')
}

onMounted(loadExams)
</script>

<style scoped>
.stat-item { text-align: center; }
.stat-value { font-size: 28px; font-weight: bold; color: #409EFF; }
.stat-label { font-size: 13px; color: #909399; margin-top: 4px; }
</style>
