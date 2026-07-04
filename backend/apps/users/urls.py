"""
用户模块 - URL 路由配置（URL 层）
=========================
在整个请求链路中的位置：【第一步 —— 路由匹配与分发】

完整调用链（以 GET /api/auth/profile/ 为例）：
  1. 浏览器 → HTTP GET http://localhost:8000/api/auth/profile/
                 ↓
  2. Django WSGI 层 → 把 HTTP 请求包装成 HttpRequest 对象
                 ↓
  3. ★ URL 路由器（这里！）→ 遍历 urlpatterns，逐条匹配正则/路径
                 ↓   找到匹配的 path('auth/profile/', ProfileView.as_view())
                 ↓
  4. 传给 View 层 → ProfileView.as_view()(request) → dispatch() → get()
                 ↓
  5. 响应返回 → APIResponse 包装 → JSON 字符串 → HTTP Response → 浏览器

Router 的作用：
  ViewSet + Router 自动创建标准的 RESTful 路由，不需要手动写每一条。
  例如 router.register(r'users', UserViewSet) 会自动生成：
    GET    /api/users/        → list
    POST   /api/users/        → create
    GET    /api/users/{id}/   → retrieve
    PUT    /api/users/{id}/   → update
    DELETE /api/users/{id}/   → destroy
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# 导入视图
from apps.users.views import (
    RegisterView,               # 注册
    CustomTokenObtainPairView, # 登录
    ProfileView,                # 个人信息
    ChangePasswordView,         # 修改密码
    UserViewSet,               # 管理员用户管理
)

# ==================== DRF Router：自动生成 ViewSet 的 CRUD 路由 ====================
router = DefaultRouter()

# 注册 UserViewSet，basename 是路由名的基础前缀
# 注册后自动生成 5 条路由：
#   GET    /users/         → UserViewSet.list()         （用户列表）
#   POST   /users/         → UserViewSet.create()       （创建用户）
#   GET    /users/{id}/    → UserViewSet.retrieve()     （用户详情）
#   PUT    /users/{id}/    → UserViewSet.update()       （修改用户）
#   DELETE /users/{id}/    → UserViewSet.destroy()      （删除用户）
router.register(r'users', UserViewSet, basename='user-manage')

# ==================== urlpatterns：URL 模式列表 ====================
urlpatterns = [
    # ---------- 1. 把 Router 生成的路由注册进来 ----------
    # include(router.urls): 把上面自动生成的所有路由都添加进来
    path('', include(router.urls)),

    # ---------- 2. 单独注册的 APIView 路由 ----------
    # 因为这些视图不是 ViewSet，不能用 Router 自动注册，需要手动写 path()

    # 注册：POST /api/auth/register/
    #   RegisterView.as_view() → 把类视图转换成 Django 可调用的函数
    path('auth/register/', RegisterView.as_view(), name='register'),

    # 登录：POST /api/auth/login/
    #   CustomTokenObtainPairView.as_view() → SimpleJWT 的登录视图
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='login'),

    # 个人信息：GET/PUT /api/auth/profile/
    path('auth/profile/', ProfileView.as_view(), name='profile'),

    # 修改密码：POST /api/auth/change-password/
    path('auth/change-password/', ChangePasswordView.as_view(), name='change-password'),
]
