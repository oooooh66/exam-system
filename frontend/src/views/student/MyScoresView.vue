<template>
  <div>
    <el-card>
      <template #header><span>我的成绩</span></template>
      <el-table v-loading="loading" :data="scores" stripe>
        <el-table-column prop="exam_name" label="考试名称" />
        <el-table-column prop="paper_name" label="试卷" />
        <el-table-column label="得分/总分" width="120">
          <template #default="{ row }">
            <b>{{ row.score_obtained || 0 }}</b> / {{ row.total_score }}
          </template>
        </el-table-column>
        <el-table-column label="正确率" width="100">
          <template #default="{ row }">
            {{ row.total_score ? Math.round((row.score_obtained || 0) / row.total_score * 100) : 0 }}%
          </template>
        </el-table-column>
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'submitted' ? 'success' : 'warning'" size="small">
              {{ row.status === 'submitted' ? '正常提交' : '自动提交' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="submit_time" label="提交时间" width="160" />
        <el-table-column label="操作" width="120">
          <template #default="{ row }">
            <el-button size="small" @click="loadDetail(row)">查看详情</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 答题详情对话框 -->
    <el-dialog v-model="detailVisible" title="答题详情" width="800px" top="5vh">
      <div v-if="detailData">
        <p><b>得分：</b>{{ detailData.submission?.total_score || 0 }} 分</p>
        <el-divider />
        <div v-for="(a, idx) in detailData.answers" :key="idx" class="answer-detail">
          <div class="answer-header">
            <span class="q-num">{{ idx + 1 }}. </span>
            <el-tag size="small">{{ a.question_type_display }}</el-tag>
            <span>({{ a.score }}分)</span>
            <el-tag
              v-if="a.is_correct !== null"
              :type="a.is_correct ? 'success' : 'danger'"
              size="small"
              style="margin-left:8px"
            >
              {{ a.is_correct ? '正确 +' + a.score_obtained : '错误 0' }}
            </el-tag>
            <el-tag v-else type="warning" size="small" style="margin-left:8px">待批改</el-tag>
          </div>
          <div class="answer-content">{{ a.question_content }}</div>
          <div class="answer-row">
            <span>你的答案：</span>
            <span :class="{ correct: a.is_correct, wrong: a.is_correct === false }">
              {{ formatAnswer(a.answer, a.question_type) || '未作答' }}
            </span>
          </div>
          <div class="answer-row" v-if="a.correct_answer">
            <span>正确答案：</span>
            <span class="correct-text">{{ formatAnswer(a.correct_answer, a.question_type) }}</span>
          </div>
          <div class="answer-analysis" v-if="a.analysis">
            <span>解析：</span>
            <span>{{ a.analysis }}</span>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getStudentScoresApi } from '@/api/reports'
import { getExamResultDetailApi } from '@/api/reports'

const loading = ref(false)
const scores = ref<any[]>([])
const detailVisible = ref(false)
const detailData = ref<any>(null)

function formatAnswer(answer: any, type: string): string {
  if (answer === null || answer === undefined) return ''
  if (type === 'multiple_choice') {
    return Array.isArray(answer) ? answer.join(', ') : String(answer)
  }
  return String(answer)
}

async function loadScores() {
  loading.value = true
  try {
    const res = await getStudentScoresApi()
    scores.value = res.data.data || []
  } finally { loading.value = false }
}

async function loadDetail(row: any) {
  try {
    const res = await getExamResultDetailApi(row.submission_id)
    detailData.value = res.data.data
    detailVisible.value = true
  } catch {
    detailVisible.value = false
  }
}

onMounted(loadScores)
</script>

<style scoped>
.answer-detail {
  padding: 12px;
  border: 1px solid #e6e6e6;
  border-radius: 8px;
  margin-bottom: 12px;
}
.answer-header { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }
.q-num { font-weight: bold; }
.answer-content { margin-bottom: 8px; line-height: 1.6; }
.answer-row { margin-bottom: 4px; }
.correct { color: #67c23a; }
.wrong { color: #f56c6c; }
.correct-text { color: #67c23a; font-weight: bold; }
.answer-analysis { margin-top: 8px; padding: 8px; background: #f0f9eb; border-radius: 4px; }
</style>
