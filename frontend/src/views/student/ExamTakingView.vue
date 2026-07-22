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

    <!-- 答题卡 -->
    <el-card class="question-nav">
      <div class="nav-header">
        <span>答题卡</span>
        <span>总分: {{ examInfo?.total_score }} | 已答: {{ answeredCount }}/{{ totalCount }}</span>
      </div>
      <div v-for="group in questionGroups" :key="group.type" class="nav-group">
        <div class="nav-group-label">{{ group.typeDisplay }}</div>
        <div class="nav-grid">
          <div
            v-for="item in group.questions"
            :key="item.globalIdx"
            class="nav-item"
            :class="{ active: currentIdx === item.globalIdx, answered: isAnswered(item.q) }"
            @click="goToQuestion(item.globalIdx)"
          >
            {{ item.globalIdx + 1 }}
          </div>
        </div>
      </div>
    </el-card>

    <!-- 题目区域 -->
    <el-card v-if="currentQuestion" class="question-area">
      <div class="question-header">
        <span class="question-number">第 {{ currentIdx + 1 }} 题</span>
        <el-tag size="small">{{ TYPE_LABEL[currentQuestion.question_type] || currentQuestion.question_type_display }}</el-tag>
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
          {{ opt }}
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
          {{ opt }}
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
let autoSaveInterval: ReturnType<typeof setInterval> | null = null

const totalCount = computed(() => questions.value.length)
const currentQuestion = computed(() => questions.value[currentIdx.value] || null)

// 题型中文映射（后端 start_exam 只返回英文 question_type）
const TYPE_LABEL: Record<string, string> = {
  single_choice: '单选题',
  multiple_choice: '多选题',
  true_false: '判断题',
  fill_blank: '填空题',
  short_answer: '简答题',
}

// 按题型分组，保持原始题目顺序
const questionGroups = computed(() => {
  const groups: { type: string; typeDisplay: string; questions: { globalIdx: number; q: any }[] }[] = []
  const typeOrder: string[] = []
  for (let i = 0; i < questions.value.length; i++) {
    const q = questions.value[i]
    if (!typeOrder.includes(q.question_type)) {
      typeOrder.push(q.question_type)
      groups.push({ type: q.question_type, typeDisplay: TYPE_LABEL[q.question_type] || q.question_type, questions: [] })
    }
    groups[groups.length - 1].questions.push({ globalIdx: i, q })
  }
  return groups
})
const answeredCount = computed(() =>
  questions.value.filter((q: any) => isAnswered(q)).length
)
const unansweredCount = computed(() => totalCount.value - answeredCount.value)

const formattedTime = computed(() => {
  const h = Math.floor(timer.value / 3600)
  const m = Math.floor((timer.value % 3600) / 60)
  const s = timer.value % 60
  return `${h.toString().padStart(2, '0')}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`
})

function isAnswered(q: any): boolean {
  const a = q.answer
  if (a === null || a === undefined || a === '') return false
  if (Array.isArray(a)) return a.length > 0
  return true
}

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
  const saveIdx = currentIdx.value

  try {
    await saveAnswerApi(examId.value, {
      paper_question_id: q.paper_question_id,
      answer: answer,
    })
  } catch {
    // 静默失败，下次再保存
  }

  // 单选和判断题：作答后自动跳到下一题
  // 只有保存期间用户没有手动切换题目时才跳，避免覆盖用户导航
  const qt = currentQuestion.value.question_type
  if (currentIdx.value === saveIdx && (qt === 'single_choice' || qt === 'true_false') && currentIdx.value < totalCount.value - 1) {
    currentIdx.value++
    loadAnswer()
  }
}

async function handleSubmit() {
  submitDialogVisible.value = true
}

async function doSubmit() {
  if (submitting.value) return  // 防重复提交
  // 提交前确保所有答案已落库
  await saveAllDrafts()
  submitting.value = true
  try {
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
    // API 返回 saved_answer 字段，映射到 answer 以便恢复答题进度
    questions.value = (res.data.data.questions || []).map((q: any) => ({
      ...q,
      answer: q.saved_answer ?? q.answer,
    }))

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

// 批量保存所有已作答但未提交到服务端的答案
async function saveAllDrafts() {
  if (submitting.value) return
  for (const q of questions.value) {
    const a = q.answer
    if (a && !(Array.isArray(a) && a.length === 0)) {
      try {
        await saveAnswerApi(examId.value, {
          paper_question_id: q.paper_question_id,
          answer: a,
        })
        q.status = 'saved'
      } catch { /* 静默 */ }
    }
  }
}

// 键盘导航：方向键左右切换题目
function handleKeydown(e: KeyboardEvent) {
  if (e.key === 'ArrowLeft' && currentIdx.value > 0) {
    e.preventDefault()
    goToQuestion(currentIdx.value - 1)
  } else if (e.key === 'ArrowRight' && currentIdx.value < totalCount.value - 1) {
    e.preventDefault()
    goToQuestion(currentIdx.value + 1)
  }
}

onMounted(() => {
  loadExam()
  window.addEventListener('beforeunload', beforeUnload)
  window.addEventListener('keydown', handleKeydown)
  // 每 30 秒自动保存所有草稿，防止浏览器意外关闭丢失进度
  autoSaveInterval = setInterval(saveAllDrafts, 30_000)
})

onBeforeUnmount(() => {
  if (timerInterval) clearInterval(timerInterval)
  if (autoSaveInterval) clearInterval(autoSaveInterval)
  window.removeEventListener('beforeunload', beforeUnload)
  window.removeEventListener('keydown', handleKeydown)
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
.nav-group {
  margin-bottom: 12px;
}
.nav-group:last-child {
  margin-bottom: 0;
}
.nav-group-label {
  font-size: 13px;
  font-weight: 600;
  color: #606266;
  margin-bottom: 6px;
  padding-left: 2px;
}
.nav-item {
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #dcdfe6;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  position: relative;
  transition: all 0.15s;
}
.nav-item:hover { border-color: #a0cfff; }
.nav-item.active {
  border-color: #409eff;
  background: #ecf5ff;
  color: #409eff;
  font-weight: 700;
  font-size: 15px;
  box-shadow: 0 0 0 3px rgba(64, 158, 255, 0.3);
  transform: scale(1.15);
  z-index: 1;
}
.nav-item.answered { background: #409eff; border-color: #409eff; color: #fff; }
.nav-item.active.answered {
  background: #409eff;
  border-color: #1a6dd4;
  color: #fff;
  font-weight: 700;
  font-size: 15px;
  box-shadow: 0 0 0 3px rgba(64, 158, 255, 0.45);
  transform: scale(1.15);
  z-index: 1;
}
.question-area { margin-top: 16px; }
.question-header { display: flex; align-items: center; gap: 12px; margin-bottom: 16px; }
.question-number { font-weight: bold; font-size: 16px; }
.score { color: #e6a23c; }
.question-content { font-size: 15px; margin-bottom: 20px; line-height: 1.8; }
.options-group { display: flex; flex-direction: column; gap: 12px; }
.option-item { padding: 12px; border: 1px solid #e6e6e6; border-radius: 8px; margin: 0 !important; width: 100%; }
.nav-buttons { display: flex; justify-content: center; gap: 12px; margin-top: 24px; padding-top: 16px; border-top: 1px solid #e6e6e6; }
</style>
