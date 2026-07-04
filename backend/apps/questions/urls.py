"""题库模块 - URL 路由配置"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.questions.views import QuestionCategoryViewSet, QuestionViewSet

router = DefaultRouter()
router.register(r'question-categories', QuestionCategoryViewSet, basename='question-category')
router.register(r'questions', QuestionViewSet, basename='question')

urlpatterns = [
    path('', include(router.urls)),
]
