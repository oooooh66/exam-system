"""试卷模块 - URL 路由配置"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.papers.views import BusiPaperViewSet

router = DefaultRouter()
router.register(r'papers', BusiPaperViewSet, basename='paper')

urlpatterns = [
    path('', include(router.urls)),
]
