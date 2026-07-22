<template>
  <div class="question-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>题库管理</span>
          <div class="header-actions">
            <el-button size="small" @click="openCategoryDialog">管理分类</el-button>
            <el-upload
              :show-file-list="false"
              accept=".xlsx,.xls"
              :http-request="handleImport"
            >
              <el-button size="small">批量导入</el-button>
            </el-upload>
            <el-button type="primary" size="small" @click="openDialog()">添加题目</el-button>
          </div>
        </div>
      </template>

      <!-- 筛选 -->
      <el-form :inline="true">
        <el-form-item label="题型">
          <el-select
            v-model="filters.question_type"
            multiple
            collapse-tags
            collapse-tags-tooltip
            clearable
            placeholder="全部"
            style="width: 180px"
            @change="loadQuestions"
          >
            <el-option label="单选题" value="single_choice" />
            <el-option label="多选题" value="multiple_choice" />
            <el-option label="判断题" value="true_false" />
            <el-option label="填空题" value="fill_blank" />
            <el-option label="简答题" value="short_answer" />
          </el-select>
        </el-form-item>
        <el-form-item label="难度">
          <el-select
            v-model="filters.difficulty"
            multiple
            collapse-tags
            collapse-tags-tooltip
            clearable
            placeholder="全部"
            style="width: 160px"
            @change="loadQuestions"
          >
            <el-option label="简单" value="easy" />
            <el-option label="中等" value="medium" />
            <el-option label="困难" value="hard" />
          </el-select>
        </el-form-item>
        <el-form-item label="分类">
          <el-select
            v-model="filters.category"
            multiple
            collapse-tags
            collapse-tags-tooltip
            clearable
            placeholder="全部"
            style="width: 180px"
            @change="loadQuestions"
          >
            <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="机构">
          <el-select v-model="filters.org_id" clearable placeholder="全部" style="width:160px" @change="loadQuestions">
            <el-option v-for="org in orgList" :key="org.org_id" :label="org.org_nm" :value="org.org_id" />
          </el-select>
        </el-form-item>
        <el-form-item label="搜索">
          <el-input v-model="filters.search" placeholder="搜索题干" clearable style="width:200px" @clear="loadQuestions" @keyup.enter="loadQuestions" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="loadQuestions">查询</el-button>
        </el-form-item>
      </el-form>

      <el-table v-loading="loading" :data="questions" stripe>
        <el-table-column label="ID" width="60" prop="id" />
        <el-table-column label="题型" width="90">
          <template #default="{ row }"><el-tag size="small">{{ row.question_type_display }}</el-tag></template>
        </el-table-column>
        <el-table-column label="题干" prop="content" show-overflow-tooltip />
        <el-table-column label="分类" width="120" prop="category_name" />
        <el-table-column label="难度" width="80">
          <template #default="{ row }">{{ row.difficulty_display }}</template>
        </el-table-column>
        <el-table-column label="机构" width="100" prop="org_nm" />
        <el-table-column label="分值" width="60" prop="default_score" />
        <el-table-column label="操作" width="140">
          <template #default="{ row }">
            <el-button size="small" @click="openDialog(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination">
        <el-pagination
          v-model:current-page="page"
          :page-size="20"
          :total="total"
          layout="prev, pager, next, total"
          @current-change="loadQuestions"
        />
      </div>
    </el-card>

    <!-- 添加/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="editing ? '编辑题目' : '添加题目'" width="700px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="90px">
        <el-form-item label="题目类型" prop="question_type">
          <el-select v-model="form.question_type" :disabled="editing" @change="onTypeChange">
            <el-option label="单选题" value="single_choice" />
            <el-option label="多选题" value="multiple_choice" />
            <el-option label="判断题" value="true_false" />
            <el-option label="填空题" value="fill_blank" />
            <el-option label="简答题" value="short_answer" />
          </el-select>
        </el-form-item>
        <el-form-item label="所属分类">
          <el-select v-model="form.category" clearable filterable allow-create placeholder="选择或输入分类">
            <el-option v-for="cat in categories" :key="cat.id" :label="cat.name" :value="cat.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="机构号">
          <el-input v-model="form.org_id" placeholder="机构编码" />
        </el-form-item>
        <el-form-item label="机构名">
          <el-input v-model="form.org_nm" placeholder="机构名称" />
        </el-form-item>
        <el-form-item label="难度">
          <el-radio-group v-model="form.difficulty">
            <el-radio value="easy">简单</el-radio>
            <el-radio value="medium">中等</el-radio>
            <el-radio value="hard">困难</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="题干" prop="content">
          <el-input v-model="form.content" type="textarea" :rows="3" />
        </el-form-item>

        <!-- 选择题选项 -->
        <template v-if="isChoiceType">
          <el-form-item v-for="(_, idx) in form.options" :key="idx" :label="`选项${String.fromCharCode(65+idx)}`" :prop="`options.${idx}`" :rules="[{ required: true, message: '请输入选项' }]">
            <el-input v-model="form.options[idx]" />
          </el-form-item>
          <el-form-item>
            <el-button @click="addOption" :disabled="form.options.length >= 6">添加选项</el-button>
            <el-button @click="removeOption" :disabled="form.options.length <= 2">移除选项</el-button>
          </el-form-item>
        </template>

        <!-- 正确答案 -->
        <el-form-item v-if="form.question_type === 'single_choice'" label="正确答案" prop="correct_answer">
          <el-select v-model="form.correct_answer">
            <el-option v-for="(opt, idx) in form.options" :key="idx" :label="String.fromCharCode(65+idx)" :value="String.fromCharCode(65+idx)" />
          </el-select>
        </el-form-item>
        <el-form-item v-if="form.question_type === 'multiple_choice'" label="正确答案" prop="correct_answer">
          <el-select v-model="form.correct_answer" multiple>
            <el-option v-for="(opt, idx) in form.options" :key="idx" :label="String.fromCharCode(65+idx)" :value="String.fromCharCode(65+idx)" />
          </el-select>
        </el-form-item>
        <el-form-item v-if="form.question_type === 'true_false'" label="正确答案" prop="correct_answer">
          <el-radio-group v-model="form.correct_answer">
            <el-radio value="对">对</el-radio>
            <el-radio value="错">错</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item v-if="['fill_blank', 'short_answer'].includes(form.question_type)" label="参考答案">
          <el-input v-model="form.correct_answer" type="textarea" :rows="2" />
        </el-form-item>

        <el-form-item label="解析">
          <el-input v-model="form.analysis" type="textarea" :rows="2" placeholder="答案解析（选填）" />
        </el-form-item>
        <el-form-item label="分值">
          <el-input-number v-model="form.default_score" :min="0.5" :max="100" :precision="2" :step="0.5" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>

    <!-- 分类管理对话框 -->
    <el-dialog v-model="categoryDialogVisible" title="分类管理" width="500px">
      <el-table :data="categories" max-height="300" stripe>
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="name" label="分类名称" />
        <el-table-column prop="question_count" label="题目数" width="80" />
        <el-table-column label="操作" width="140">
          <template #default="{ row }">
            <el-button size="small" @click="editCategory(row)">编辑</el-button>
            <el-button size="small" type="danger" @click="deleteCategory(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      <div style="margin-top:12px;display:flex;gap:8px">
        <el-input v-model="categoryForm.name" placeholder="输入分类名称" @keyup.enter="saveCategory" />
        <el-button type="primary" @click="saveCategory">
          {{ categoryEditing ? '保存' : '新增' }}
        </el-button>
        <el-button v-if="categoryEditing" @click="categoryForm.name = ''; categoryEditing = null">取消</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getQuestionsApi, createQuestionApi, updateQuestionApi, deleteQuestionApi, importQuestionsApi, getCategoriesApi, createCategoryApi, updateCategoryApi, deleteCategoryApi, getOrgsApi } from '@/api/questions'

const loading = ref(false)
const saving = ref(false)
const questions = ref<any[]>([])
const categories = ref<any[]>([])
const orgList = ref<any[]>([])
const total = ref(0)
const page = ref(1)
const editing = ref(false)
const dialogVisible = ref(false)
const formRef = ref()

// 分类管理相关
const categoryDialogVisible = ref(false)
const categoryEditing = ref<any>(null)
const categoryForm = reactive({ name: '' })

const filters = reactive<{ question_type: string[]; difficulty: string[]; category: number[]; org_id: string; search: string }>({
  question_type: [],
  difficulty: [],
  category: [],
  org_id: '',
  search: '',
})

const form = reactive<any>({
  question_type: 'single_choice',
  content: '',
  options: ['', '', '', ''],
  correct_answer: '',
  analysis: '',
  category: null,
  difficulty: 'easy',
  default_score: 5,
  org_id: '',
  org_nm: '',
})

const rules = {
  question_type: [{ required: true }],
  content: [{ required: true, message: '请输入题干' }],
}

const isChoiceType = computed(() => ['single_choice', 'multiple_choice'].includes(form.question_type))

function onTypeChange() {
  if (form.question_type === 'single_choice') { form.options = ['', '', '', '']; form.correct_answer = '' }
  else if (form.question_type === 'multiple_choice') { form.options = ['', '', '', '']; form.correct_answer = [] }
  else if (form.question_type === 'true_false') { form.correct_answer = '对' }
  else { form.correct_answer = '' }
}

function addOption() { if (form.options.length < 6) form.options.push('') }
function removeOption() { if (form.options.length > 2) form.options.pop() }

async function loadQuestions() {
  loading.value = true
  try {
    const params: any = { page: page.value }
    if (filters.question_type.length) params.question_type = filters.question_type.join(',')
    if (filters.difficulty.length) params.difficulty = filters.difficulty.join(',')
    if (filters.category.length) params.category = filters.category.join(',')
    if (filters.org_id) params.org_id = filters.org_id
    if (filters.search) params.search = filters.search
    const res = await getQuestionsApi(params)
    questions.value = res.data.data?.results || []
    total.value = res.data.data?.count || 0
  } finally { loading.value = false }
}

async function loadCategories() {
  const res = await getCategoriesApi()
  categories.value = res.data.data?.results || []
}

function openDialog(row?: any) {
  editing.value = !!row
  if (row) {
    Object.assign(form, {
      question_type: row.question_type,
      content: row.content,
      options: row.options?.slice() || [],
      correct_answer: row.correct_answer,
      analysis: row.analysis || '',
      category: row.category,
      difficulty: row.difficulty, org_id: row.org_id || '', org_nm: row.org_nm || '',
      default_score: row.default_score,
    })
    if (!form.options.length) form.options = ['', '', '', '']
  } else {
    form.question_type = 'single_choice'
    form.content = ''
    form.options = ['', '', '', '']
    form.correct_answer = ''
    form.analysis = ''
    form.category = null
    form.difficulty = 'easy'
    form.default_score = 5
  }
  dialogVisible.value = true
}

async function handleSave() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return
  saving.value = true
  try {
    const data = { ...form }
    if (!isChoiceType.value) delete data.options
    if (editing.value) {
      await updateQuestionApi(form.id, data)
      ElMessage.success('修改成功')
    } else {
      await createQuestionApi(data)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    loadQuestions()
  } catch (err: any) {
    ElMessage.error(err?.response?.data?.message || '操作失败')
  } finally { saving.value = false }
}

async function handleDelete(row: any) {
  await ElMessageBox.confirm('确定删除该题目吗？', '确认', { type: 'warning' })
  await deleteQuestionApi(row.id)
  ElMessage.success('已删除')
  loadQuestions()
}

async function handleImport(params: any) {
  const formData = new FormData()
  formData.append('file', params.file)
  loading.value = true
  try {
    const res = await importQuestionsApi(formData)
    const data = res.data.data
    ElMessage.success(`导入完成：成功${data.success_count}条，失败${data.fail_count}条`)
    loadQuestions()
  } catch (err: any) {
    ElMessage.error('导入失败')
  } finally { loading.value = false }
}

// ==================== 分类管理 ====================

function openCategoryDialog() {
  categoryEditing.value = null
  categoryForm.name = ''
  categoryDialogVisible.value = true
}

function editCategory(row: any) {
  categoryEditing.value = row
  categoryForm.name = row.name
}

async function saveCategory() {
  if (!categoryForm.name.trim()) { ElMessage.warning('请输入分类名称'); return }
  try {
    if (categoryEditing.value) {
      await updateCategoryApi(categoryEditing.value.id, { name: categoryForm.name })
      ElMessage.success('修改成功')
    } else {
      await createCategoryApi({ name: categoryForm.name })
      ElMessage.success('新增成功')
    }
    categoryForm.name = ''
    categoryEditing.value = null
    loadCategories()
  } catch (err: any) {
    ElMessage.error(err?.response?.data?.message || '操作失败')
  }
}

async function deleteCategory(row: any) {
  await ElMessageBox.confirm(`确定删除分类"${row.name}"吗？`, '确认', { type: 'warning' })
  await deleteCategoryApi(row.id)
  ElMessage.success('已删除')
  loadCategories()
}

async function loadOrgs() {
  try { const res = await getOrgsApi(); orgList.value = res.data.data || [] } catch { /* ignore */ }
}

onMounted(() => { loadQuestions(); loadCategories(); loadOrgs() })
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; }
.header-actions { display: flex; gap: 8px; }
.pagination { margin-top: 16px; display: flex; justify-content: flex-end; }
</style>
