"""考试模块 - URL 路由配置"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.exams.views import BusiExamSessionViewSet

router = DefaultRouter()
router.register(r'exams', BusiExamSessionViewSet, basename='exam')

urlpatterns = [
    path('', include(router.urls)),
]
