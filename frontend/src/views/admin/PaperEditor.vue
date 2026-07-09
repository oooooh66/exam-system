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
        <div v-for="(rule, idx) in randomRules" :key="idx" style="display:flex;gap:10px;align-items:center;margin-bottom:8px">
          <el-select v-model="rule.category_id" placeholder="选择分类" style="width:200px" clearable>
            <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id" />
          </el-select>
          <span>抽取</span>
          <el-input-number v-model="rule.question_count" :min="1" :max="99" size="small" />
          <span>题</span>
          <el-button size="small" type="danger" @click="randomRules.splice(idx, 1)">删除</el-button>
        </div>
        <el-button size="small" @click="randomRules.push({ category_id: null, question_count: 5 })">
          + 添加规则
        </el-button>
        <el-button
          v-if="randomRules.length"
          type="warning"
          size="small"
          :loading="drawing"
          style="margin-left:10px"
          @click="doRandomDraw"
        >
          随机抽题
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
        <el-form-item label="搜索">
          <el-input v-model="searchText" placeholder="搜索题干" clearable style="width:180px" @keyup.enter="loadQuestions" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadQuestions">搜索</el-button>
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
          {{ isEdit ? '保存修改' : '创建试卷' }}
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getQuestionsApi, getCategoriesApi } from '@/api/questions'
import { createPaperApi, updatePaperApi, getPaperDetailApi, randomDrawApi } from '@/api/papers'

const route = useRoute()
const router = useRouter()
const isEdit = computed(() => !!route.params.id)

const saving = ref(false)
const qLoading = ref(false)
const qPage = ref(1)
const qTotal = ref(0)
const filterType = ref<string[]>([])
const filterCategory = ref<number[]>([])
const searchText = ref('')
const categories = ref<any[]>([])

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
const randomRules = ref<{ category_id: number | null; question_count: number }[]>([])
const drawing = ref(false)

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

/** 执行随机抽题 */
async function doRandomDraw() {
  const validRules = randomRules.value.filter(r => r.category_id && r.question_count > 0)
  if (!validRules.length) { ElMessage.warning('请至少配置一条有效规则'); return }

  drawing.value = true
  try {
    const paperId = Number(route.params.id)
    if (paperId) {
      // 编辑已有试卷：直接调用该试卷的随机抽题接口
      const res = await randomDrawApi(paperId, {
        rules: validRules.map(r => ({ category_id: r.category_id, question_count: r.question_count })),
      })
      const data = res.data.data
      const pqList = data.paper?.paper_questions || data.paper?.busi_paper_questions || []
      selectedQuestions.value = pqList.map((pq: any) => ({
        question_id: pq.question || pq.question_id,
        question: pq.question || pq.question_id,
        question_detail: pq.question_detail,
        score: Number(pq.score) || 5,
        order: pq.order,
      }))
      ElMessage.success(data.message || `抽取了 ${data.added} 题`)
    } else {
      // 新建试卷：本地模拟抽题（调后端随机接口，但试卷未保存所以先本地处理）
      await loadQuestions()
      const rules = validRules.map(r => ({ category_id: r.category_id, question_count: r.question_count }))
      // 本地随机选择
      for (const rule of rules) {
        const pool = availableQuestions.value.filter(
          (q: any) => q.category === rule.category_id && !isAdded(q.id)
        )
        const picked = pool.sort(() => Math.random() - 0.5).slice(0, rule.question_count)
        for (const q of picked) {
          selectedQuestions.value.push({
            question_id: q.id, question: q.id,
            question_detail: q, score: Number(q.default_score) || 5,
            order: selectedQuestions.value.length,
          })
        }
      }
      ElMessage.success(`随机抽取了题目`)
    }
    updateTotal()
  } catch (err: any) {
    ElMessage.error(err?.response?.data?.message || '随机抽题失败')
  } finally { drawing.value = false }
}

/** 加载可选题库 */
async function loadQuestions() {
  qLoading.value = true
  try {
    const params: any = { page: qPage.value }
    if (filterType.value.length) params.question_type = filterType.value.join(',')
    if (filterCategory.value.length) params.category = filterCategory.value.join(',')
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
    if (isEdit.value) {
      await updatePaperApi(Number(route.params.id), payload)
      ElMessage.success('修改成功')
    } else {
      await createPaperApi(payload)
      ElMessage.success('创建成功')
    }
    router.push('/admin/papers')
  } catch (err: any) {
    ElMessage.error(err?.response?.data?.message || '保存失败')
  } finally { saving.value = false }
}

onMounted(() => {
  loadCategories()
  loadQuestions()
  loadPaperDetail()
})
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>
