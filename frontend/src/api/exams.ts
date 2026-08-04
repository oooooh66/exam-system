/**
 * 考试模块 API
 */
import request from '@/utils/request'

export function getExamsApi(params?: any) {
  return request.get('/exams/', { params })
}
export function getExamDetailApi(id: number) {
  return request.get(`/exams/${id}/`)
}
export function createExamApi(data: any) {
  return request.post('/exams/', data)
}
export function deleteExamApi(id: number) {
  return request.delete(`/exams/${id}/`)
}
export function startExamApi(id: number) {
  return request.post(`/exams/${id}/start/`)
}
export function saveAnswerApi(examId: number, data: any) {
  return request.post(`/exams/${examId}/save/`, data)
}
export function submitExamApi(examId: number, data?: Record<string, any>) {
  return request.post(`/exams/${examId}/submit/`, data)
}
export function getMyExamsApi() {
  return request.get('/exams/my-exams/')
}
export function getExamResultApi(examId: number) {
  return request.get(`/exams/${examId}/my-result/`)
}

/** 教师查看待批改列表 */
export function getGradeListApi(examId: number) {
  return request.get(`/exams/${examId}/grade-list/`)
}

/** 教师手动批改一道题 */
export function gradeAnswerApi(examId: number, data: { answer_id: number; score_obtained: number }) {
  return request.post(`/exams/${examId}/grade/`, data)
}

/** 批量导入考生（上传 Excel） */
export function importCandidatesApi(file: File) {
  const formData = new FormData()
  formData.append('file', file)
  return request.post('/exams/import-candidates/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

/** 查看考试所有考生成绩 */
export function getExamResultsApi(examId: number) {
  return request.get(`/exams/${examId}/results/`)
}

/** 调整考生浮动分 */
export function adjustScoreApi(examId: number, data: { submission_id: number; float_score: number; reason?: string }) {
  return request.post(`/exams/${examId}/adjust-score/`, data)
}

/** 导出成绩 Excel */
export function exportResultsApi(examId: number) {
  return request.get(`/exams/${examId}/export/`, { responseType: 'blob' })
}
