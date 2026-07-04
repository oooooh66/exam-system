/**
 * 试卷管理 API
 */
import request from '@/utils/request'

export function getPapersApi(params?: any) {
  return request.get('/papers/', { params })
}
export function getPaperDetailApi(id: number) {
  return request.get(`/papers/${id}/`)
}
export function createPaperApi(data: any) {
  return request.post('/papers/', data)
}
export function updatePaperApi(id: number, data: any) {
  return request.put(`/papers/${id}/`, data)
}
export function deletePaperApi(id: number) {
  return request.delete(`/papers/${id}/`)
}
export function addQuestionToPaperApi(paperId: number, data: any) {
  return request.post(`/papers/${paperId}/add-question/`, data)
}
export function removeQuestionFromPaperApi(paperId: number, questionId: number) {
  return request.delete(`/papers/${paperId}/remove-question/${questionId}/`)
}
export function updatePaperQuestionsApi(paperId: number, data: any) {
  return request.post(`/papers/${paperId}/update-questions/`, data)
}
