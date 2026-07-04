"""
在线考试系统 - 主 URL 路由配置

路由规范：
- /api/auth/      — 认证相关接口（注册、登录、个人信息、修改密码）
- /api/users/     — 用户管理接口（管理员 CRUD）
- /api/questions/ — 题库管理接口
- /api/papers/    — 试卷管理接口
- /api/exams/     — 考试相关接口
- /api/reports/   — 成绩报表接口
- /api/docs/      — API 文档
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# JWT Token 刷新和验证（登录/注册由 users app 处理）
from rest_framework_simplejwt.views import (
    TokenRefreshView,         # 刷新 Token
    TokenVerifyView,          # 验证 Token
)

# API 文档
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    # Django Admin 管理后台
    path('admin/', admin.site.urls),

    # ============================================
    # API 路由入口（统一 /api/ 前缀）
    # ============================================
    path('api/', include('apps.users.urls')),
    path('api/', include('apps.questions.urls')),
    path('api/', include('apps.papers.urls')),
    path('api/', include('apps.exams.urls')),
    path('api/', include('apps.reports.urls')),

    # Token 刷新和验证（全局路由，不归 users 管理）
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # ============================================
    # API 文档
    # ============================================
    path('api/docs/schema/', SpectacularAPIView.as_view(), name='schema'),
    path(
        'api/docs/swagger/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui',
    ),
    path(
        'api/docs/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc',
    ),
]

# 开发环境支持媒体文件访问
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
