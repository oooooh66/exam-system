<template>
  <div class="paper-editor">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>{{ isEdit ? '编辑试卷' : '创建试卷' }}</span>
          <el-button @click="$router.back()">返回</el-button>
        </div>
      </template>

      <!-- 基本信息 -->
      <el-form :model="paper" label-width="100px" style="max-width:600px">
        <el-form-item label="试卷名称" required>
          <el-input v-model="paper.name" placeholder="请输入试卷名称" />
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="paper.description" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="及格分">
          <el-input-number v-model="paper.pass_score" :min="0" :max="999" :precision="2" :step="0.5" />
        </el-form-item>
        <el-form-item label="考试时长(分)">
          <el-input-number v-model="paper.duration_minutes" :min="1" :max="999" />
        </el-form-item>
      </el-form>

      <!-- 已选题目 -->
      <el-divider />
      <h3 style="margin-bottom:12px">
        试卷题目（{{ selectedQuestions.length }} 题，总分 {{ totalScore.toFixed(2) }}）
      </h3>

      <el-table :data="selectedQuestions" stripe>
        <el-table-column label="序号" type="index" width="60" />
        <el-table-column label="题型" width="90">
          <template #default="{ row }">
            <el-tag size="small">{{ row.question_detail?.question_type_display }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="题干" show-overflow-tooltip>
          <template #default="{ row }">{{ row.question_detail?.content }}</template>
        </el-table-column>
        <el-table-column label="分值" width="120">
          <template #default="{ row }">
            <el-input-number
              v-model="row.score"
              :min="0.5"
              :max="100"
              :precision="2"
              :step="0.5"
              size="small"
              @change="updateTotal"
            />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="80">
          <template #default="{ $index }">
            <el-button size="small" type="danger" @click="removeQuestion($index)">移除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-empty v-if="!selectedQuestions.length" description="暂无题目，请从下方题库中添加" />

      <!-- 随机抽题配置 -->
      <el-divider />
      <h3 style="margin-bottom:12px">随机抽题规则</h3>
      <div style="margin-bottom:16px">
        <div v-for="(rule, idx) in randomRules" :key="idx" style="border:1px solid #ddd;border-radius:6px;padding:10px;margin-bottom:10px;background:#fafafa">
          <div style="display:flex;gap:10px;align-items:center;margin-bottom:8px">
            <el-select v-model="rule.category_id" placeholder="选择分类" style="width:160px" clearable>
              <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id" />
            </el-select>
            <span style="font-size:13px">总抽题数</span>
            <el-input-number v-model="rule.total" :min="0" :max="99" size="small" style="width:80px" controls-position="right" />
            <el-tag :type="typeTotal(rule) === rule.total ? 'success' : 'danger'" size="small">
              {{ typeTotal(rule) === rule.total ? `= ${rule.total} 题` : `${typeTotal(rule)}≠${rule.total}` }}
            </el-tag>
            <el-button
              size="small"
              type="primary"
              :loading="rule.drawing"
              :disabled="!rule.category_id || typeTotal(rule) !== rule.total || rule.total === 0"
              @click="doRuleDraw(idx)"
            >
              {{ rule.drawn ? '刷新抽题' : '随机抽题' }}
            </el-button>
            <el-button size="small" type="danger" @click="removeRule(idx)">删除</el-button>
          </div>
          <div style="display:flex;gap:12px;flex-wrap:wrap">
            <span v-for="t in questionTypes" :key="t.value" style="display:flex;align-items:center;gap:4px;font-size:13px">
              {{ t.label }}
              <el-input-number v-model="rule.counts[t.value]" :min="0" :max="99" size="small" style="width:70px" controls-position="right" />
            </span>
          </div>
        </div>
        <el-button size="small" @click="randomRules.push({ category_id: null, total: 0, drawn: false, drawing: false, counts: { single_choice: 0, multiple_choice: 0, true_false: 0, fill_blank: 0, short_answer: 0 }, questions: [] })">
          + 添加规则
        </el-button>
      </div>

      <!-- 选题区域 -->
      <el-divider />
      <h3 style="margin-bottom:12px">从题库选题</h3>

      <el-form :inline="true">
        <el-form-item label="题型">
          <el-select
            v-model="filterType"
            multiple
            collapse-tags
            collapse-tags-tooltip
            clearable
            placeholder="全部"
            style="width: 200px"
            @change="loadQuestions"
          >
            <el-option label="单选题" value="single_choice" />
            <el-option label="多选题" value="multiple_choice" />
            <el-option label="判断题" value="true_false" />
            <el-option label="填空题" value="fill_blank" />
            <el-option label="简答题" value="short_answer" />
          </el-select>
        </el-form-item>
        <el-form-item label="分类">
          <el-select
            v-model="filterCategory"
            multiple
            collapse-tags
            collapse-tags-tooltip
            clearable
            placeholder="全部"
            style="width: 200px"
            @change="loadQuestions"
          >
            <el-option
              v-for="cat in categories"
              :key="cat.id"
              :label="cat.name"
              :value="cat.id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="机构">
          <el-select
            v-model="filterOrg"
            clearable
            filterable
            placeholder="全部"
            style="width: 180px"
            @change="loadQuestions"
          >
            <el-option
              v-for="org in orgList"
              :key="org.org_id"
              :label="`${org.org_id} ${org.org_nm}`"
              :value="org.org_id"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="搜索">
          <el-input v-model="searchText" placeholder="搜索题干" clearable style="width:180px" @keyup.enter="loadQuestions" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadQuestions">搜索</el-button>
          <el-button @click="resetFilters">重置</el-button>
        </el-form-item>
      </el-form>

      <el-table
        ref="questionTable"
        v-loading="qLoading"
        :data="availableQuestions"
        stripe
        @selection-change="onSelectionChange"
      >
        <el-table-column type="selection" width="50" :selectable="rowSelectable" />
        <el-table-column label="ID" width="60" prop="id" />
        <el-table-column label="题型" width="90">
          <template #default="{ row }"><el-tag size="small">{{ row.question_type_display }}</el-tag></template>
        </el-table-column>
        <el-table-column label="题干" prop="content" show-overflow-tooltip />
        <el-table-column label="分类" width="100">
          <template #default="{ row }">
            <el-tag type="info" size="small">{{ row.category_name }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="难度" width="80">
          <template #default="{ row }"><el-tag size="small">{{ row.difficulty_display }}</el-tag></template>
        </el-table-column>
        <el-table-column label="分值" width="70" prop="default_score" />
        <el-table-column label="操作" width="80">
          <template #default="{ row }">
            <el-button size="small" type="success" :disabled="isAdded(row.id)" @click="quickAdd(row)">添加</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div style="margin-top:16px;display:flex;justify-content:space-between;">
        <el-button type="primary" @click="addSelected">添加选中题目</el-button>
        <el-pagination
          v-model:current-page="qPage"
          :page-size="15"
          :total="qTotal"
          layout="prev, pager, next"
          @current-change="loadQuestions"
        />
      </div>

      <div style="margin-top:24px;text-align:center">
        <el-button type="primary" size="large" :loading="saving" @click="handleSave">
          {{ route.name === 'PaperCreate' ? '创建试卷' : '保存修改' }}
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getQuestionsApi, getCategoriesApi, getOrgsApi, randomPickApi } from '@/api/questions'
import { createPaperApi, updatePaperApi, getPaperDetailApi } from '@/api/papers'

const route = useRoute()
const router = useRouter()
const isEdit = computed(() => !!route.params.id)

const saving = ref(false)
const qLoading = ref(false)
const qPage = ref(1)
const qTotal = ref(0)
const filterType = ref<string[]>([])
const filterCategory = ref<number[]>([])
const filterOrg = ref('')
const searchText = ref('')
const categories = ref<any[]>([])
const orgList = ref<any[]>([])

// 表格 ref
const questionTable = ref()

const paper = reactive({
  name: '',
  description: '',
  pass_score: 60,
  duration_minutes: 60,
})

const selectedQuestions = ref<any[]>([])
const availableQuestions = ref<any[]>([])
const selectedRows = ref<any[]>([])
const totalScore = ref(0)
const questionTypes = [
  { value: 'single_choice', label: '单选' },
  { value: 'multiple_choice', label: '多选' },
  { value: 'true_false', label: '判断' },
  { value: 'fill_blank', label: '填空' },
  { value: 'short_answer', label: '简答' },
]
const randomRules = ref<{
  category_id: number | null
  total: number
  counts: Record<string, number>
  drawn: boolean
  drawing: boolean
  questions: any[]
}[]>([])
const drawing = ref(false)

function typeTotal(rule: any): number {
  return Object.values(rule.counts || {}).reduce((s: number, v: any) => s + (v || 0), 0)
}

function removeRule(idx: number) {
  // 从 selectedQuestions 中移除该规则的题目
  const qids = new Set(randomRules.value[idx].questions.map((q: any) => q.id))
  selectedQuestions.value = selectedQuestions.value.filter(
    (q: any) => !qids.has(q.question_detail?.id ?? q.question_id)
  )
  randomRules.value.splice(idx, 1)
}

/** 检查题目是否已在试卷列表中 */
function isAdded(id: number): boolean {
  return selectedQuestions.value.some(
    (q: any) => (q.question_detail?.id ?? q.question_id ?? q.question) === id
  )
}

/** 行是否可选（已添加的不可再勾选） */
function rowSelectable(row: any): boolean {
  return !isAdded(row.id)
}

/** Element Plus 表格选中变化回调 */
function onSelectionChange(rows: any[]) {
  selectedRows.value = rows
}

/** 单题快速添加 */
function quickAdd(row: any) {
  if (isAdded(row.id)) return
  const score = Number(row.default_score) || 5
  selectedQuestions.value.push({
    question_id: row.id,
    question: row.id,
    question_detail: row,
    score: score,
    order: selectedQuestions.value.length,
  })
  updateTotal()
}

/** 批量添加选中的题目，自动排除已在试卷列表中的 */
function addSelected() {
  // 过滤掉已经添加过的题目
  const toAdd = selectedRows.value.filter((row: any) => !isAdded(row.id))
  for (const row of toAdd) {
    const score = Number(row.default_score) || 5
    selectedQuestions.value.push({
      question_id: row.id,
      question: row.id,
      question_detail: row,
      score: score,
      order: selectedQuestions.value.length,
    })
  }
  // 清空表格选中状态和内部数据
  if (toAdd.length > 0) {
    updateTotal()
  }
  selectedRows.value = []
  questionTable.value?.clearSelection()
}

/** 移除题目 */
function removeQuestion(index: number) {
  selectedQuestions.value.splice(index, 1)
  // 移除后刷新表格的选中状态（防止已勾选的行残留）
  questionTable.value?.clearSelection()
  selectedRows.value = []
  updateTotal()
}

/** 重新计算总分 */
function updateTotal() {
  totalScore.value = selectedQuestions.value.reduce(
    (sum: number, q: any) => sum + (Number(q.score) || 0),
    0
  )
}

/** 执行单条规则的随机抽题 */
async function doRuleDraw(idx: number) {
  const rule = randomRules.value[idx]
  if (!rule.category_id || typeTotal(rule) !== rule.total || rule.total === 0) return

  rule.drawing = true
  try {
    const res = await randomPickApi({
      rules: [{
        category_id: rule.category_id,
        counts: rule.counts,
      }],
    })

    const data = res.data.data
    const newQuestions = (data.questions || []).map((q: any) => ({
      question_id: q.id,
      question: q.id,
      question_detail: q,
      score: Number(q.default_score) || 5,
      order: 0,
    }))

    // 刷新模式：先移除旧题目，再添加新题目
    if (rule.drawn && rule.questions.length) {
      const oldIds = new Set(rule.questions.map((q: any) => q.question_detail?.id ?? q.question_id))
      selectedQuestions.value = selectedQuestions.value.filter(
        (q: any) => !oldIds.has(q.question_detail?.id ?? q.question_id)
      )
    }

    // 添加新题目（追加到末尾）
    const startIdx = selectedQuestions.value.length
    newQuestions.forEach((q: any, i: number) => { q.order = startIdx + i })
    selectedQuestions.value.push(...newQuestions)

    rule.questions = newQuestions
    rule.drawn = true
    reorderByType()
    updateTotal()
    ElMessage.success(data.skipped > 0
      ? `抽取 ${data.added} 题，${data.skipped} 题因题库不足跳过`
      : `成功抽取 ${data.added} 题`)
  } catch (err: any) {
    ElMessage.error(err?.response?.data?.message || '随机抽题失败')
  } finally {
    rule.drawing = false
  }
}

/** 按题目类型排序 */
function reorderByType() {
  const order = ['single_choice', 'multiple_choice', 'true_false', 'fill_blank', 'short_answer']
  selectedQuestions.value.sort((a: any, b: any) => {
    const ta = a.question_detail?.question_type ?? ''
    const tb = b.question_detail?.question_type ?? ''
    return order.indexOf(ta) - order.indexOf(tb)
  })
  selectedQuestions.value.forEach((q: any, i: number) => { q.order = i })
}

/** 加载可选题库 */
async function loadQuestions(page?: number) {
  qLoading.value = true
  if (page) qPage.value = page
  try {
    const params: any = { page: qPage.value }
    if (filterType.value.length) params.question_type = filterType.value.join(',')
    if (filterCategory.value.length) params.category = filterCategory.value.join(',')
    if (filterOrg.value) params.org_id = filterOrg.value
    if (searchText.value) params.search = searchText.value
    const res = await getQuestionsApi(params)
    availableQuestions.value = res.data.data?.results || []
    qTotal.value = res.data.data?.count || 0
  } finally { qLoading.value = false }
}

/** 加载分类列表 */
async function loadCategories() {
  try {
    const res = await getCategoriesApi()
    categories.value = res.data.data?.results || []
  } catch { /* ignore */ }
}

/** 加载机构列表 */
async function loadOrgs() {
  try {
    const res = await getOrgsApi()
    orgList.value = res.data.data || []
  } catch { /* ignore */ }
}

/** 重置筛选条件 */
function resetFilters() {
  filterType.value = []
  filterCategory.value = []
  filterOrg.value = ''
  searchText.value = ''
  qPage.value = 1
  loadQuestions()
}

/** 加载试卷详情（编辑模式） */
async function loadPaperDetail() {
  if (!isEdit.value) return
  const res = await getPaperDetailApi(Number(route.params.id))
  const data = res.data.data
  Object.assign(paper, {
    name: data.name,
    description: data.description || '',
    pass_score: Number(data.pass_score) || 60,
    duration_minutes: data.duration_minutes || 60,
  })
  selectedQuestions.value = (data.paper_questions || []).map((pq: any) => ({
    question_id: pq.question,
    question: pq.question,
    question_detail: pq.question_detail,
    score: Number(pq.score) || Number(pq.question_detail?.default_score) || 5,
    order: pq.order,
  }))
  updateTotal()
}

/** 保存试卷 */
async function handleSave() {
  if (!paper.name) { ElMessage.warning('请输入试卷名称'); return }
  if (!selectedQuestions.value.length) { ElMessage.warning('请至少添加一道题目'); return }

  saving.value = true
  try {
    const payload = {
      ...paper,
      pass_score: Number(paper.pass_score),
      questions: selectedQuestions.value.map((q: any, idx: number) => ({
        question_id: q.question_id || q.question,
        score: Number(q.score) || 5,
        order: idx,
      })),
    }
    const isCreate = route.name === 'PaperCreate'
    if (isCreate) {
      await createPaperApi(payload)
      ElMessage.success('创建成功')
    } else {
      await updatePaperApi(Number(route.params.id), payload)
      ElMessage.success('修改成功')
    }
    router.push('/admin/papers')
  } catch (err: any) {
    ElMessage.error(err?.response?.data?.message || '保存失败')
  } finally { saving.value = false }
}

onMounted(() => {
  loadCategories()
  loadOrgs()
  loadQuestions()
  loadPaperDetail()
})
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>
