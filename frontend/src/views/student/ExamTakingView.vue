<template>
  <div class="exam-taking">
    <!-- 顶部信息栏 -->
    <div class="exam-header">
      <div>
        <h3>{{ examInfo?.exam_name }}</h3>
        <span>{{ examInfo?.paper_name }}</span>
      </div>
      <div class="timer">
        <el-tag type="danger" size="large">
          <el-icon><Clock /></el-icon>
          {{ formattedTime }}
        </el-tag>
      </div>
    </div>

    <!-- 题目导航面板 -->
    <el-card class="question-nav">
      <div class="nav-header">
        <span>答题卡</span>
        <span>总分: {{ examInfo?.total_score }} | 已答: {{ answeredCount }}/{{ totalCount }}</span>
      </div>
      <div class="nav-grid">
        <div
          v-for="(q, idx) in questions"
          :key="idx"
          class="nav-item"
          :class="{ active: currentIdx === idx, answered: q.answer !== null && q.answer !== '' }"
          @click="goToQuestion(idx)"
        >
          {{ idx + 1 }}
        </div>
      </div>
    </el-card>

    <!-- 题目区域 -->
    <el-card v-if="currentQuestion" class="question-area">
      <div class="question-header">
        <span class="question-number">第 {{ currentIdx + 1 }} 题</span>
        <el-tag size="small">{{ currentQuestion.question_type_display }}</el-tag>
        <span class="score">({{ currentQuestion.score }} 分)</span>
      </div>

      <div class="question-content">{{ currentQuestion.content }}</div>

      <!-- 单选题 -->
      <el-radio-group
        v-if="currentQuestion.question_type === 'single_choice'"
        v-model="editingAnswer"
        class="options-group"
        @change="autoSave"
      >
        <el-radio
          v-for="(opt, optIdx) in currentQuestion.options"
          :key="optIdx"
          :value="String.fromCharCode(65 + optIdx)"
          class="option-item"
        >
          {{ String.fromCharCode(65 + optIdx) + '. ' + opt }}
        </el-radio>
      </el-radio-group>

      <!-- 多选题 -->
      <el-checkbox-group
        v-if="currentQuestion.question_type === 'multiple_choice'"
        v-model="editingAnswer"
        class="options-group"
        @change="autoSave"
      >
        <el-checkbox
          v-for="(opt, optIdx) in currentQuestion.options"
          :key="optIdx"
          :label="String.fromCharCode(65 + optIdx)"
          :value="String.fromCharCode(65 + optIdx)"
          class="option-item"
        >
          {{ String.fromCharCode(65 + optIdx) + '. ' + opt }}
        </el-checkbox>
      </el-checkbox-group>

      <!-- 判断题 -->
      <el-radio-group
        v-if="currentQuestion.question_type === 'true_false'"
        v-model="editingAnswer"
        class="options-group"
        @change="autoSave"
      >
        <el-radio value="对" class="option-item">对</el-radio>
        <el-radio value="错" class="option-item">错</el-radio>
      </el-radio-group>

      <!-- 填空题/简答题 -->
      <div v-if="['fill_blank', 'short_answer'].includes(currentQuestion.question_type)">
        <el-input
          v-model="editingAnswer"
          type="textarea"
          :rows="currentQuestion.question_type === 'short_answer' ? 5 : 2"
          placeholder="请输入答案"
          @blur="autoSave"
        />
      </div>

      <!-- 底部导航按钮 -->
      <div class="nav-buttons">
        <el-button :disabled="currentIdx === 0" @click="goToQuestion(currentIdx - 1)">上一题</el-button>
        <el-button @click="autoSave()">保存</el-button>
        <el-button v-if="currentIdx < totalCount - 1" type="primary" @click="goToQuestion(currentIdx + 1)">下一题</el-button>
        <el-button v-else type="danger" @click="handleSubmit">提交试卷</el-button>
      </div>
    </el-card>

    <!-- 交卷确认对话框 -->
    <el-dialog v-model="submitDialogVisible" title="确认交卷" width="400px">
      <p>您确定要提交试卷吗？交卷后无法修改答案。</p>
      <p v-if="unansweredCount > 0" style="color:#e6a23c">
        还有 {{ unansweredCount }} 道题未作答！
      </p>
      <template #footer>
        <el-button @click="submitDialogVisible = false">继续答题</el-button>
        <el-button type="primary" :loading="submitting" @click="doSubmit">确认交卷</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { startExamApi, saveAnswerApi, submitExamApi } from '@/api/exams'

const route = useRoute()
const router = useRouter()

const examId = computed(() => Number(route.params.id))
const examInfo = ref<any>(null)
const questions = ref<any[]>([])
const currentIdx = ref(0)
const editingAnswer = ref<any>(null)
const submitting = ref(false)
const submitDialogVisible = ref(false)
const timer = ref(0)
let timerInterval: ReturnType<typeof setInterval> | null = null

const totalCount = computed(() => questions.value.length)
const currentQuestion = computed(() => questions.value[currentIdx.value] || null)
const answeredCount = computed(() => questions.value.filter((q: any) => q.answer !== null && q.answer !== '').length)
const unansweredCount = computed(() => totalCount.value - answeredCount.value)

const formattedTime = computed(() => {
  const h = Math.floor(timer.value / 3600)
  const m = Math.floor((timer.value % 3600) / 60)
  const s = timer.value % 60
  return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
})

function goToQuestion(idx: number) {
  autoSave()
  currentIdx.value = idx
  loadAnswer()
}

function loadAnswer() {
  const q = questions.value[currentIdx.value]
  editingAnswer.value = q?.answer || (q?.question_type === 'multiple_choice' ? [] : '')
}

async function autoSave() {
  if (!currentQuestion.value || submitting.value) return
  const q = questions.value[currentIdx.value]
  const answer = editingAnswer.value

  // 不保存空答案
  if (answer === '' || answer === null || (Array.isArray(answer) && answer.length === 0)) {
    return
  }

  q.answer = answer
  q.status = 'draft'

  try {
    await saveAnswerApi(examId.value, {
      paper_question_id: q.paper_question_id,
      answer: answer,
    })
  } catch {
    // 静默失败，下次再保存
  }
}

async function handleSubmit() {
  submitDialogVisible.value = true
}

async function doSubmit() {
  submitting.value = true
  try {
    // 先保存所有未保存的答案
    for (const q of questions.value) {
      if (q.answer && q.status === 'draft') {
        await saveAnswerApi(examId.value, {
          paper_question_id: q.paper_question_id,
          answer: q.answer,
        })
      }
    }
    const res = await submitExamApi(examId.value)
    ElMessage.success(`提交成功！得分：${res.data.data?.total_score || '待批改'}`)
    if (timerInterval) clearInterval(timerInterval)
    router.push('/student/exams')
  } catch (err: any) {
    ElMessage.error(err?.response?.data?.message || '提交失败')
  } finally {
    submitting.value = false
  }
}

async function loadExam() {
  try {
    const res = await startExamApi(examId.value)
    examInfo.value = res.data.data
    questions.value = res.data.data.questions || []

    // 计算剩余时间
    const endTime = new Date(examInfo.value.end_time).getTime()
    const now = Date.now()
    timer.value = Math.max(0, Math.floor((endTime - now) / 1000))

    // 开始倒计时
    timerInterval = setInterval(() => {
      if (timer.value > 0) {
        timer.value--
      } else {
        // 时间到自动提交
        if (timerInterval) clearInterval(timerInterval)
        ElMessage.warning('考试时间到，正在自动提交...')
        doSubmit()
      }
    }, 1000)

    loadAnswer()
  } catch (err: any) {
    ElMessage.error(err?.response?.data?.message || '加载考试失败')
    router.push('/student/exams')
  }
}

// 防止意外关闭
function beforeUnload(e: BeforeUnloadEvent) {
  if (!submitting.value) {
    e.preventDefault()
  }
}

onMounted(() => {
  loadExam()
  window.addEventListener('beforeunload', beforeUnload)
})

onBeforeUnmount(() => {
  if (timerInterval) clearInterval(timerInterval)
  window.removeEventListener('beforeunload', beforeUnload)
})
</script>

<style scoped>
.exam-header {
  background: #fff;
  padding: 16px 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 2px solid #e6e6e6;
  margin-bottom: 16px;
}
.timer { font-size: 18px; }
.question-nav {
  margin-bottom: 16px;
}
.nav-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
}
.nav-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.nav-item {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}
.nav-item.active { border-color: #409eff; background: #ecf5ff; color: #409eff; }
.nav-item.answered { background: #f0f9eb; border-color: #67c23a; }
.question-area { margin-top: 16px; }
.question-header { display: flex; align-items: center; gap: 12px; margin-bottom: 16px; }
.question-number { font-weight: bold; font-size: 16px; }
.score { color: #e6a23c; }
.question-content { font-size: 15px; margin-bottom: 20px; line-height: 1.8; }
.options-group { display: flex; flex-direction: column; gap: 12px; }
.option-item { padding: 12px; border: 1px solid #e6e6e6; border-radius: 8px; margin: 0 !important; width: 100%; }
.nav-buttons { display: flex; justify-content: center; gap: 12px; margin-top: 24px; padding-top: 16px; border-top: 1px solid #e6e6e6; }
</style>
