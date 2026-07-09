"""题库模块 - URL 路由配置"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.questions.views import BusiQuestionCategoryViewSet, BusiQuestionViewSet

router = DefaultRouter()
router.register(r'question-categories', BusiQuestionCategoryViewSet, basename='question-category')
router.register(r'questions', BusiQuestionViewSet, basename='question')

urlpatterns = [
    path('', include(router.urls)),
]
