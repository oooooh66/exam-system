/**
 * 成绩报表 API
 */
import request from '@/utils/request'

/** 考试统计 */
export function getExamStatisticsApi(examId: number) {
  return request.get(`/reports/exam/${examId}/statistics/`)
}

/** 学生成绩列表 */
export function getStudentScoresApi() {
  return request.get('/reports/student-scores/')
}

/** 考试详细答卷 */
export function getExamResultDetailApi(submissionId: number) {
  return request.get(`/reports/result/${submissionId}/`)
}

/** 导出成绩 Excel URL */
export function getExportUrl(examId: number) {
  return `/api/reports/exam/${examId}/export/`
}
