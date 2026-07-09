/**
 * 题库管理 API
 */
import request from '@/utils/request'

// ========== 题目分类 ==========
export function getCategoriesApi(params?: any) {
  return request.get('/question-categories/', { params })
}
export function createCategoryApi(data: any) {
  return request.post('/question-categories/', data)
}
export function updateCategoryApi(id: number, data: any) {
  return request.put(`/question-categories/${id}/`, data)
}
export function deleteCategoryApi(id: number) {
  return request.delete(`/question-categories/${id}/`)
}

// ========== 题目 ==========
export function getQuestionsApi(params?: any) {
  return request.get('/questions/', { params })
}
export function getQuestionDetailApi(id: number) {
  return request.get(`/questions/${id}/`)
}
export function createQuestionApi(data: any) {
  return request.post('/questions/', data)
}
export function updateQuestionApi(id: number, data: any) {
  return request.put(`/questions/${id}/`, data)
}
export function deleteQuestionApi(id: number) {
  return request.delete(`/questions/${id}/`)
}
export function importQuestionsApi(formData: FormData) {
  return request.post('/questions/import/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
}

// ========== 机构 ==========
/** 获取所有不重复的机构列表 */
export function getOrgsApi() {
  return request.get('/questions/orgs/')
}
