"""成绩报表模块 - URL 路由配置"""
from django.urls import path

from apps.reports.views import (
    BusiExamStatisticsView,
    BusiStudentScoresView,
    BusiExamResultDetailView,
    BusiExportScoresView,
)

urlpatterns = [
    # 考试统计
    path('reports/exam/<int:exam_id>/statistics/', BusiExamStatisticsView.as_view(), name='exam-statistics'),
    # 导出成绩
    path('reports/exam/<int:exam_id>/export/', BusiExportScoresView.as_view(), name='exam-export'),
    # 学生成绩列表
    path('reports/student-scores/', BusiStudentScoresView.as_view(), name='student-scores'),
    # 学生某次考试的详细答题结果
    path('reports/result/<int:submission_id>/', BusiExamResultDetailView.as_view(), name='exam-result-detail'),
]
