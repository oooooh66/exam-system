"""试卷模块 - URL 路由配置"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.papers.views import PaperViewSet

router = DefaultRouter()
router.register(r'papers', PaperViewSet, basename='paper')

urlpatterns = [
    path('', include(router.urls)),
]
