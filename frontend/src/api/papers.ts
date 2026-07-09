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

/** 获取/保存随机抽题规则 */
export function getRandomRulesApi(paperId: number) {
  return request.get(`/papers/${paperId}/random-rules/`)
}
export function saveRandomRulesApi(paperId: number, data: any) {
  return request.post(`/papers/${paperId}/random-rules/`, data)
}

/** 随机抽题 */
export function randomDrawApi(paperId: number, data: any) {
  return request.post(`/papers/${paperId}/random-draw/`, data)
}
