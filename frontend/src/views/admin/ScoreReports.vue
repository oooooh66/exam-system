<template>
  <div class="score-reports">
    <el-card>
      <template #header>
        <div style="display:flex;justify-content:space-between;align-items:center">
          <span>成绩报表</span>
          <div style="display:flex;gap:8px">
            <el-select v-model="selectedExamId" filterable placeholder="选择考试" @change="loadResults" style="width:300px" clearable>
              <el-option v-for="exam in exams" :key="exam.id" :label="exam.name" :value="exam.id" />
            </el-select>
            <el-button v-if="selectedExamId" @click="exportScores">导出 Excel</el-button>
          </div>
        </div>
      </template>

      <template v-if="resultsData">
        <!-- 分榜 Tab -->
        <el-tabs v-model="activeTab">
          <el-tab-pane label="资产榜" name="asset">
            <ScoreReportTable :list="resultsData.asset_ranking" :float-enabled="resultsData.float_enabled" :is-admin="isAdmin" @adjust="openAdjust" />
          </el-tab-pane>
          <el-tab-pane label="负债榜" name="liability">
            <ScoreReportTable :list="resultsData.liability_ranking" :float-enabled="resultsData.float_enabled" :is-admin="isAdmin" @adjust="openAdjust" />
          </el-tab-pane>
          <el-tab-pane label="全部" name="all">
            <ScoreReportTable :list="resultsData.all" :float-enabled="resultsData.float_enabled" :is-admin="isAdmin" @adjust="openAdjust" />
          </el-tab-pane>
        </el-tabs>
      </template>
      <el-empty v-else-if="selectedExamId" description="暂无成绩数据" />
    </el-card>

    <!-- 浮动分调整对话框 -->
    <el-dialog v-model="adjustVisible" title="浮动分管理" width="460px">
      <el-descriptions :column="1" border size="small">
        <el-descriptions-item label="姓名">{{ adjustStudent }}</el-descriptions-item>
        <el-descriptions-item label="考试分数">{{ adjustBase }}</el-descriptions-item>
        <el-descriptions-item label="当前浮动分">{{ adjustPrev }}</el-descriptions-item>
        <el-descriptions-item label="最终得分">
          <b style="font-size:18px;color:#409eff">{{ ((adjustBase||0) + (adjustScore||0)).toFixed(1) }}</b>
        </el-descriptions-item>
      </el-descriptions>
      <el-form label-width="90px" style="margin-top:16px">
        <el-form-item label="浮动分">
          <el-input-number v-model="adjustScore" :min="-10" :max="10" :step="1" />
          <span style="margin-left:8px;color:#909399;font-size:12px">范围: -10 ~ +10</span>
        </el-form-item>
        <el-form-item label="调整说明">
          <el-input v-model="adjustReason" type="textarea" :rows="2" placeholder="选填评定依据" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="adjustVisible = false">取消</el-button>
        <el-button type="primary" :loading="adjustSaving" @click="confirmAdjust">确认提交</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getExamsApi, getExamResultsApi, adjustScoreApi, exportResultsApi } from '@/api/exams'
import { useAuthStore } from '@/stores/auth'
import ScoreReportTable from './ScoreReportTable.vue'

const authStore = useAuthStore()
const isAdmin = ref(authStore.user?.role === 'admin')
const exams = ref<any[]>([])
const selectedExamId = ref<number | null>(null)
const resultsData = ref<any>(null)
const activeTab = ref('asset')

// 浮动分调分
const adjustVisible = ref(false); const adjustSaving = ref(false)
const adjustSubmissionId = ref(0); const adjustStudent = ref('')
const adjustBase = ref(0); const adjustScore = ref(0)
const adjustReason = ref(''); const adjustPrev = ref(0)

async function loadExams() {
  const res = await getExamsApi()
  exams.value = res.data.data?.results || []
}

async function loadResults() {
  if (!selectedExamId.value) { resultsData.value = null; return }
  try {
    const res = await getExamResultsApi(selectedExamId.value)
    resultsData.value = res.data.data
    activeTab.value = resultsData.value?.asset_ranking?.length ? 'asset' : 'all'
  } catch (err: any) { ElMessage.error('获取成绩失败') }
}

function openAdjust(row: any) {
  adjustSubmissionId.value = row.id
  adjustStudent.value = row.student_name
  adjustBase.value = row.total_score || 0
  adjustScore.value = row.float_score || 0
  adjustReason.value = row.float_score_reason || ''
  adjustPrev.value = row.float_score || 0
  adjustVisible.value = true
}

async function confirmAdjust() {
  if (!selectedExamId.value) return
  adjustSaving.value = true
  try {
    await adjustScoreApi(selectedExamId.value, {
      submission_id: adjustSubmissionId.value,
      float_score: adjustScore.value,
      reason: adjustReason.value,
    })
    ElMessage.success('浮动分已调整')
    adjustVisible.value = false
    loadResults()
  } catch (err: any) { ElMessage.error(err?.response?.data?.message || '调整失败') }
  finally { adjustSaving.value = false }
}

async function exportScores() {
  if (!selectedExamId.value) return
  try {
    const res = await exportResultsApi(selectedExamId.value)
    const url = window.URL.createObjectURL(new Blob([res.data]))
    const a = document.createElement('a'); a.href = url
    a.download = `${resultsData.value?.exam_name || '考试'}_成绩.xlsx`
    a.click(); window.URL.revokeObjectURL(url)
  } catch { ElMessage.error('导出失败') }
}

onMounted(loadExams)
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>
