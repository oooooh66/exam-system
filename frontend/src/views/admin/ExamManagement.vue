<template>
  <div class="exam-management">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>考试管理</span>
          <div style="display:flex;gap:8px">
            <el-button @click="showImportDialog = true">导入考生</el-button>
            <el-button type="primary" @click="openDialog()">发布考试</el-button>
          </div>
        </div>
      </template>
      <el-table v-loading="loading" :data="exams" stripe>
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="name" label="考试名称" min-width="140" />
        <el-table-column prop="paper_name" label="试卷" min-width="120" />
        <el-table-column prop="total_score" label="总分" width="70" />
        <el-table-column prop="duration" label="时长(分)" width="80" />
        <el-table-column label="状态" width="90">
          <template #default="{ row }">
            <el-tag :type="statusType(row.status)" size="small">{{ statusText(row.status) }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="start_time" label="开始时间" width="160" />
        <el-table-column prop="end_time" label="结束时间" width="160" />
        <el-table-column label="操作" width="220" fixed="right">
          <template #default="{ row }">
            <el-button size="small" @click="openResults(row)">成绩</el-button>
            <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 发布考试对话框 -->
    <el-dialog v-model="dialogVisible" title="发布考试" width="640px">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="考试名称" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="考试时长(分)">
          <el-input-number v-model="form.duration_minutes" :min="1" :max="480" />
        </el-form-item>
        <el-form-item label="及格分数">
          <el-input-number v-model="form.pass_score" :min="0" :max="500" />
        </el-form-item>
        <el-form-item label="开始时间" prop="start_time">
          <el-date-picker v-model="form.start_time" type="datetime" placeholder="选择开始时间" style="width:100%" />
        </el-form-item>
        <el-form-item label="结束时间" prop="end_time">
          <el-date-picker v-model="form.end_time" type="datetime" placeholder="选择结束时间" style="width:100%" />
        </el-form-item>
        <el-form-item label="考试范围">
          <el-checkbox-group v-model="form.exam_scope">
            <el-checkbox value="资产">资产</el-checkbox>
            <el-checkbox value="负债">负债</el-checkbox>
          </el-checkbox-group>
          <div style="font-size:11px;color:#909399">只有分管业务包含此项的考生才能看到该考试</div>
        </el-form-item>
        <el-divider>高级设置</el-divider>
        <el-form-item label="浮动分">
          <el-switch v-model="form.float_enabled" />
          <span style="margin-left:8px;color:#909399;font-size:12px">
            范围：{{ form.float_min }} ~ {{ form.float_max }} 分
          </span>
        </el-form-item>
        <el-divider>组卷规则</el-divider>
        <el-form-item label="抽题规则">
          <div v-for="qt in ['single_choice','multiple_choice','true_false']" :key="qt" style="margin-bottom:4px;display:flex;align-items:center;gap:4px;flex-wrap:wrap">
            <span style="font-size:12px;white-space:nowrap">{{ {single_choice:'单选',multiple_choice:'多选',true_false:'判断'}[qt] }}</span>
            <el-input-number v-model="form.rules[qt].count" :min="0" :max="200" size="small" style="width:80px" />
            <span style="font-size:12px">题</span>
            <span style="font-size:11px;color:#909399">分类:</span>
            <el-select v-model="form.rules[qt].categories" multiple collapse-tags size="small" placeholder="全部" style="width:180px">
              <el-option v-for="c in categories" :key="c.id" :label="c.name" :value="c.id" />
            </el-select>
          </div>
          <div style="font-size:11px;color:#909399;margin-top:4px">考生点击"开始考试"时动态随机抽题，每人题目独立不重复</div>
          <div style="margin-top:6px;font-size:13px;color:#e6a23c">
            预估总分：<b>{{ estimatedTotal }}</b> 分
            <span v-if="form.pass_score > estimatedTotal" style="color:#f56c6c;margin-left:8px">⚠ 及格分数大于总分</span>
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="handleCreate">发布</el-button>
      </template>
    </el-dialog>

    <!-- 导入考生对话框 -->
    <el-dialog v-model="showImportDialog" title="导入考生" width="480px">
      <el-upload :auto-upload="false" :limit="1" accept=".xlsx,.xls" :on-change="onFileChange" drag>
        <el-icon class="el-icon--upload"><UploadFilled /></el-icon>
        <div class="el-upload__text">将 Excel 文件拖到此处，或<em>点击上传</em></div>
        <template #tip><div class="el-upload__tip">上传村行高管及业务部负责人考核人员统计表</div></template>
      </el-upload>
      <div v-if="importResult" style="margin-top:12px">
        <el-alert :title="importResult" type="success" :closable="false" />
      </div>
      <template #footer>
        <el-button @click="showImportDialog = false">关闭</el-button>
        <el-button type="primary" :loading="importing" :disabled="!selectedFile" @click="doImport">开始导入</el-button>
      </template>
    </el-dialog>

    <!-- 成绩查看对话框 -->
    <el-dialog v-model="resultsVisible" title="考试成绩" width="900px" top="3vh">
      <template v-if="resultsData">
        <div style="margin-bottom:12px;display:flex;justify-content:space-between;align-items:center">
          <span>考试：<b>{{ resultsData.exam_name }}</b> | 共 {{ resultsData.all?.length || 0 }} 人</span>
          <el-button size="small" @click="doExport">导出 Excel</el-button>
        </div>
        <el-tabs v-model="resultsTab">
          <el-tab-pane label="资产榜" name="asset">
            <ScoreTable :list="resultsData.asset_ranking" @adjust="openAdjust" />
          </el-tab-pane>
          <el-tab-pane label="负债榜" name="liability">
            <ScoreTable :list="resultsData.liability_ranking" @adjust="openAdjust" />
          </el-tab-pane>
          <el-tab-pane label="全部" name="all">
            <ScoreTable :list="resultsData.all" @adjust="openAdjust" />
          </el-tab-pane>
        </el-tabs>
      </template>
    </el-dialog>

    <!-- 浮动分调整对话框 -->
    <el-dialog v-model="adjustVisible" title="调整浮动分" width="420px">
      <el-form label-width="90px">
        <el-form-item label="考生">{{ adjustStudent }}</el-form-item>
        <el-form-item label="基础分">{{ adjustBase }}</el-form-item>
        <el-form-item label="浮动分">
          <el-input-number v-model="adjustScore" :min="floatMin" :max="floatMax" :step="1" />
          <span style="margin-left:8px;color:#909399;font-size:12px">范围: {{ floatMin }} ~ {{ floatMax }}</span>
        </el-form-item>
        <el-form-item label="最终得分"><b style="font-size:16px;color:#409eff">{{ (Number(adjustBase) + Number(adjustScore)).toFixed(1) }}</b></el-form-item>
        <el-form-item label="评定依据">
          <el-input v-model="adjustReason" type="textarea" :rows="2" placeholder="选填" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="adjustVisible = false">取消</el-button>
        <el-button type="primary" :loading="adjustSaving" @click="doAdjust">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getExamsApi, createExamApi, deleteExamApi, importCandidatesApi, getExamResultsApi, adjustScoreApi, exportResultsApi } from '@/api/exams'
import { getCategoriesApi } from '@/api/questions'
import ScoreTable from './ScoreTable.vue'

const loading = ref(false)
const saving = ref(false)
const dialogVisible = ref(false)
const exams = ref<any[]>([])
const categories = ref<any[]>([])
const formRef = ref()

const form = reactive<any>({
  name: '', duration_minutes: 60, pass_score: 60,
  start_time: '', end_time: '', exam_scope: [] as string[],
  float_enabled: false, float_min: -10, float_max: 10,
  rules: {
    single_choice: { count: 30, categories: [] as number[] },
    multiple_choice: { count: 10, categories: [] as number[] },
    true_false: { count: 10, categories: [] as number[] },
  },
})

// 预估总分（每题默认2分）
const estimatedTotal = computed(() => {
  const r = form.rules
  return (r.single_choice.count || 0) * 2 + (r.multiple_choice.count || 0) * 2 + (r.true_false.count || 0) * 2
})

const rules = {
  name: [{ required: true, message: '请输入考试名称' }],
  start_time: [{ required: true, message: '请选择开始时间' }],
  end_time: [{ required: true, message: '请选择结束时间' }],
}

// 导入考生
const showImportDialog = ref(false); const importing = ref(false)
const selectedFile = ref<File | null>(null); const importResult = ref('')

// 成绩
const resultsVisible = ref(false); const resultsData = ref<any>(null); const resultsTab = ref('asset')
const currentExamId = ref<number>(0)

// 浮动分
const adjustVisible = ref(false); const adjustSaving = ref(false)
const adjustSubmissionId = ref(0); const adjustStudent = ref(''); const adjustBase = ref(0)
const adjustScore = ref(0); const adjustReason = ref(''); const adjustPrev = ref(0)
const floatMin = ref(-10); const floatMax = ref(10)

function statusType(s: string) { return { upcoming: 'info', ongoing: 'success', finished: '' }[s] || 'info' }
function statusText(s: string) { return { upcoming: '未开始', ongoing: '进行中', finished: '已结束' }[s] || s }

function resetForm() {
  Object.assign(form, {
    name: '', duration_minutes: 60, pass_score: 60, exam_scope: [],
    start_time: '', end_time: '',
    float_enabled: false, float_min: -10, float_max: 10,
    rules: { single_choice: { count: 30, categories: [] }, multiple_choice: { count: 10, categories: [] }, true_false: { count: 10, categories: [] } },
  })
}

function openDialog() { resetForm(); dialogVisible.value = true }

async function handleCreate() {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return
  saving.value = true
  try {
    const payload: any = {
      name: form.name, start_time: form.start_time, end_time: form.end_time,
      duration_minutes: form.duration_minutes, pass_score: form.pass_score,
      exam_scope: form.exam_scope || [],
    }
    if (form.float_enabled) {
      payload.float_score_enabled = true; payload.float_score_min = form.float_min; payload.float_score_max = form.float_max
    }
    // 组卷规则转为数组发送
    payload.rules = []
    for (const qt of ['single_choice', 'multiple_choice', 'true_false']) {
      const r = form.rules[qt]
      if (r.count > 0) payload.rules.push({ question_type: qt, count: r.count, categories: r.categories || [] })
    }
    await createExamApi(payload)
    ElMessage.success('考试发布成功')
    dialogVisible.value = false
    loadExams()
  } catch (err: any) { ElMessage.error(err?.response?.data?.message || '发布失败') }
  finally { saving.value = false }
}

async function loadExams() {
  loading.value = true
  try { const res = await getExamsApi(); exams.value = res.data.data?.results || [] }
  finally { loading.value = false }
}

async function handleDelete(row: any) {
  try {
    await ElMessageBox.confirm('确定删除该考试吗？', '提示', { type: 'warning' })
    await deleteExamApi(row.id)
    ElMessage.success('已删除')
    loadExams()
  } catch { /* cancel */ }
}

function onFileChange(file: any) { selectedFile.value = file.raw }

async function doImport() {
  if (!selectedFile.value) return
  importing.value = true; importResult.value = ''
  try {
    const res = await importCandidatesApi(selectedFile.value)
    const d = res.data.data
    importResult.value = `导入完成：共 ${d.total} 人（资产${d.by_scope?.asset||0} / 负债${d.by_scope?.liability||0} / 双重${d.by_scope?.both||0}）`
    ElMessage.success(res.data.message)
    showImportDialog.value = false
  } catch (err: any) { ElMessage.error(err?.response?.data?.message || '导入失败') }
  finally { importing.value = false }
}

// 成绩查看
async function openResults(row: any) {
  currentExamId.value = row.id
  resultsVisible.value = true; resultsData.value = null
  try {
    const res = await getExamResultsApi(row.id)
    resultsData.value = res.data.data
    resultsTab.value = 'asset'
  } catch (err: any) { ElMessage.error(err?.response?.data?.message || '加载失败'); resultsVisible.value = false }
}

function openAdjust(sub: any) {
  adjustSubmissionId.value = sub.id
  adjustStudent.value = sub.student_name
  adjustBase.value = sub.total_score || 0
  adjustScore.value = sub.float_score || 0
  adjustReason.value = sub.float_score_reason || ''
  adjustPrev.value = sub.float_score || 0
  resultsData.value?.float_enabled ? null : (floatMin.value = -10, floatMax.value = 10)
  adjustVisible.value = true
}

async function doAdjust() {
  adjustSaving.value = true
  try {
    await adjustScoreApi(currentExamId.value, {
      submission_id: adjustSubmissionId.value,
      float_score: adjustScore.value,
      reason: adjustReason.value,
    })
    ElMessage.success('浮动分已调整')
    adjustVisible.value = false
    openResults({ id: currentExamId.value }) // 刷新
  } catch (err: any) { ElMessage.error(err?.response?.data?.message || '调整失败') }
  finally { adjustSaving.value = false }
}

async function doExport() {
  try {
    const res = await exportResultsApi(currentExamId.value)
    const url = window.URL.createObjectURL(new Blob([res.data]))
    const a = document.createElement('a'); a.href = url
    a.download = `${resultsData.value?.exam_name || '考试'}_成绩.xlsx`
    a.click(); window.URL.revokeObjectURL(url)
  } catch { ElMessage.error('导出失败') }
}

onMounted(async () => {
  loadExams()
  const cr = await getCategoriesApi()
  categories.value = cr.data.data?.results || []
})
</script>

<style scoped>
.card-header { display: flex; justify-content: space-between; align-items: center; }
</style>
