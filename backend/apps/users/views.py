"""
用户模块 - 视图层（View 层）
=====================
在整个请求链路中的位置：【中间核心 —— 接收请求、调度业务、返回响应】

完整调用链（以 POST /api/auth/register/ 为例）：
  1. 前端 → HTTP POST http://localhost:8000/api/auth/register/  ← 浏览器发出请求
                Body: {"username":"new","password":"123456","password_confirm":"123456","role":"student"}
                      │
  2. Django 中间件 ← 请求先经过一系列中间件（CORS、安全、Session...）
                      │
  3. URL 路由器 ← urls.py 中 path('auth/register/', RegisterView.as_view())
                      │  匹配成功！将请求分发给 RegisterView
                      │
  4. 权限校验 ← RegisterView 设置了 permission_classes = [AllowAny]，所有人可访问
                      │  如果是需要登录的接口，这里会检查 JWT Token
                      │
  5. ★ View 层 ← request 到达 RegisterView.post()
                      │  a. 创建 RegisterSerializer(data=request.data)
                      │  b. 调用 serializer.is_valid() → 触发 Serializer 的校验逻辑
                      │  c. 校验失败 → 返回错误信息
                      │  d. 校验通过 → 调用 serializer.save() → 触发 Serializer 的 create()
                      │     └─ create() 内部：User.objects.create(**data) → INSERT INTO users
                      │  e. 包装响应 → APIResponse.success(data=..., message='注册成功')
                      │
  6. 中间件（响应阶段） ← 响应再经过中间件（添加 CORS 头等）
                      │
  7. 前端接收 ← {"code":201, "message":"注册成功", "data":{"id":3, "username":"new", "role":"student"}}
"""
from django.contrib.auth import get_user_model               # 获取自定义 User 模型
from rest_framework import status, viewsets, mixins           # DRF 的核心模块
from rest_framework.decorators import action                  # ViewSet 自定义路由装饰器
from rest_framework.permissions import AllowAny               # 允许所有人访问（不需要登录）
from rest_framework.response import Response                 # DRF 的响应类
from rest_framework.views import APIView                      # DRF 的视图基类
from rest_framework_simplejwt.views import TokenObtainPairView  # SimpleJWT 的登录视图基类

# ==================== 导入本地模块 ====================
from apps.users.serializers import (
    RegisterSerializer,              # 注册序列化器
    CustomTokenObtainPairSerializer, # 登录序列化器
    UserProfileSerializer,           # 个人信息序列化器
    ChangePasswordSerializer,        # 修改密码序列化器
    UserManageSerializer,            # 管理员用户管理序列化器
)
from utils.permissions import IsAdmin, IsOwnerOrAdmin   # 自定义权限类
from utils.response import APIResponse                    # 统一响应类

# ==================== 获取 User 模型（这种方式比直接 import 更灵活） ====================
User = get_user_model()


# ============================================
# 1. 注册视图 —— POST /api/auth/register/
# ============================================
class RegisterView(APIView):
    """
    【用户注册接口】不需要登录就能访问

    APIView 是 DRF 最基础的视图类，需要手动实现 get/post/put/delete 等方法。
    生命周期：
      1. as_view() → 将类转换为 Django 可调用的视图函数
      2. dispatch() → 根据 HTTP 方法分发到对应的处理方法（get → .get(), post → .post()）
      3. post() → 接收请求、校验数据、存储、返回响应
    """

    # permission_classes: 权限控制列表（AllowAny 表示不需要任何认证）
    permission_classes = [AllowAny]
    # authentication_classes: 认证方式列表（空列表表示不检查 JWT Token）
    authentication_classes = []

    def post(self, request):
        """
        【处理 POST 请求】用户注册的核心逻辑

        request 对象包含：
          - request.data: 前端传来的 JSON 数据（DRF 自动解析了）
            {"username": "new", "password": "123456", "password_confirm": "123456", "role": "student"}
          - request.user: 当前登录用户（注册时未登录，但如果认证类不为空会有值）
        """
        # === 步骤 1: 数据校验 ===
        # 创建序列化器实例，把前端 JSON 传入 data 参数
        serializer = RegisterSerializer(data=request.data)

        # is_valid() 触发序列化器的校验流程：
        #   a. 字段级校验 → validate_username()
        #   b. 对象级校验 → validate()
        #   校验失败 → serializer.errors 包含错误信息
        if not serializer.is_valid():
            # 提取第一个错误信息返回给前端
            return APIResponse.error(
                code=status.HTTP_400_BAD_REQUEST,
                message=self._get_first_error(serializer.errors),
            )

        # === 步骤 2: 保存数据 ===
        # serializer.save() 内部调用 RegisterSerializer.create()
        # create() 流程：
        #   1. 删除 password_confirm
        #   2. 用 make_password() 加密密码
        #   3. User.objects.create(**validated_data) → INSERT INTO users
        #   4. 返回新创建的 User 实例
        user = serializer.save()

        # === 步骤 3: 返回响应 ===
        # APIResponse.success() 把数据包装成统一格式：
        #   {"code": 201, "message": "注册成功", "data": {...}}
        return APIResponse.success(
            data={'id': user.id, 'username': user.username, 'role': user.role},
            message='注册成功',
            code=status.HTTP_201_CREATED,
        )

    def _get_first_error(self, errors):
        """【辅助方法】从 DRF 的嵌套错误字典中提取第一条可读的错误信息"""
        for field, messages in errors.items():
            if isinstance(messages, list):
                return str(messages[0])
            if isinstance(messages, dict):
                return self._get_first_error(messages)
            return str(messages)
        return '请求参数错误'


# ============================================
# 2. 登录视图 —— POST /api/auth/login/
# ============================================
class CustomTokenObtainPairView(TokenObtainPairView):
    """
    【用户登录接口】继承 SimpleJWT 的登录视图，使用我们自定义的序列化器

    TokenObtainPairView 内部流程：
      1. 接收 POST → {"username": "admin", "password": "admin123"}
      2. 创建 CustomTokenObtainPairSerializer(data=request.data)
      3. 调用 serializer.is_valid() →
         a. 父类 validate_username_password(): Django authenticate() 校验
         b. 我们的 validate(): 追加 user 信息
      4. serializer.validated_data → {"access": "xxx", "refresh": "xxx", "user": {...}}
      5. 生成 Response → {"access": "...", "refresh": "..."}
    """

    # 指定使用我们自定义的序列化器（增加了 user 信息返回）
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        """
        【重写 post 方法】把 SimpleJWT 的原始响应包装成统一格式

        原始 SimpleJWT 返回: {"access": "xxx", "refresh": "xxx"}
        我们包装后返回: {"code": 200, "message": "登录成功", "data": {"access": "xxx", "refresh": "xxx", "user": {...}}}
        """
        # 调用父类的 post 方法，拿到原始 DRF Response 对象
        response = super().post(request, *args, **kwargs)

        # 包装成统一格式
        return Response(
            data={
                'code': status.HTTP_200_OK,
                'message': '登录成功',
                'data': response.data,  # 包含 access, refresh, user 信息
            },
            status=status.HTTP_200_OK,
        )


# ============================================
# 3. 个人信息视图 —— GET/PUT /api/auth/profile/
# ============================================
class ProfileView(APIView):
    """
    【个人信息接口】需要登录后才能访问（没有设置 permission_classes = [AllowAny]）

    默认的 permission_classes 在 settings.py 里配了 IsAuthenticated，
    所以这个视图会自动要求 JWT 认证。前端请求时必须带 Authorization: Bearer <token>
    """

    def get(self, request):
        """
        【GET /api/auth/profile/】查看自己的个人信息

        request.user 是从 JWT Token 中解析出来的 User 对象：
          JWT payload: {"user_id": 1, "username": "admin", "role": "admin"}
          → Django 查数据库 → User.objects.get(id=1) → request.user
        """
        # 把 User 实例传给序列化器，它会自动转换为 JSON
        # 内部：遍历 fields 列表，逐个获取属性值，组装成字典，再 json.dumps
        serializer = UserProfileSerializer(request.user)
        return APIResponse.success(data=serializer.data)

    def put(self, request):
        """
        【PUT /api/auth/profile/】修改自己的个人信息（如邮箱）

        partial=True 表示"部分更新"，不是所有字段都必须传
        前端可以只传要修改的字段，如 {"email": "new@example.com"}
        """
        # instance=request.user → 指定要更新的对象
        # data=request.data → 前端传来的更新数据
        # partial=True → 允许部分字段更新（PATCH 语义）
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)

        if not serializer.is_valid():
            return APIResponse.error(
                code=status.HTTP_400_BAD_REQUEST,
                message=self._get_first_error(serializer.errors),
            )

        # serializer.save() 内部调用 update() → 逐字段修改 → instance.save()
        # SQL 层面：UPDATE users SET email='new@example.com', updated_at=NOW() WHERE id=1
        serializer.save()
        return APIResponse.success(data=serializer.data, message='个人信息更新成功')

    def _get_first_error(self, errors):
        for field, messages in errors.items():
            if isinstance(messages, list):
                return str(messages[0])
            return str(messages)
        return '请求参数错误'


# ============================================
# 4. 修改密码视图 —— POST /api/auth/change-password/
# ============================================
class ChangePasswordView(APIView):
    """
    【修改密码接口】需要登录

    流程：
      1. 前端传 {"old_password": "xxx", "new_password": "yyy", "new_password_confirm": "yyy"}
      2. Serializer 校验旧密码是否正确（用 check_password）
      3. 校验通过 → save() → set_password(new_password) → 哈希后存库
    """

    def post(self, request):
        # context={'request': request} 是关键 —— 把当前请求传给 Serializer
        # Serializer 里通过 self.context['request'].user 获取当前登录用户
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})

        if not serializer.is_valid():
            return APIResponse.error(
                code=status.HTTP_400_BAD_REQUEST,
                message=self._get_first_error(serializer.errors),
            )

        serializer.save()
        return APIResponse.success(message='密码修改成功')

    def _get_first_error(self, errors):
        for field, messages in errors.items():
            if isinstance(messages, list):
                return str(messages[0])
            return str(messages)
        return '请求参数错误'


# ============================================
# 5. 管理员用户管理 ViewSet —— 处理 /api/users/ CRUD
# ============================================
class UserViewSet(mixins.ListModelMixin,      # 列表查询 GET /api/users/
                  mixins.CreateModelMixin,    # 创建用户 POST /api/users/
                  mixins.UpdateModelMixin,    # 修改用户 PUT /api/users/{id}/
                  mixins.DestroyModelMixin,   # 删除用户 DELETE /api/users/{id}/
                  viewsets.GenericViewSet):
    """
    【管理员专用】用户管理 ViewSet

    ViewSet 和 APIView 的区别：
      APIView: 手动写 get/post/put/delete 方法
      ViewSet: 结合 Router 自动生成标准的 RESTful 路由

    ViewSet + Router 自动生成的路由：
      GET    /api/users/        → list()      — 查询所有用户
      POST   /api/users/        → create()    — 创建用户
      GET    /api/users/{id}/   → retrieve()  — 查看单个用户详情
      PUT    /api/users/{id}/   → update()    — 修改用户
      DELETE /api/users/{id}/   → destroy()   — 删除用户

    这些方法由 mixins 提供，我们在这里重写来自定义行为。
    """

    # ==================== 基础配置 ====================
    serializer_class = UserManageSerializer          # 默认使用的序列化器
    permission_classes = [IsAdmin]                    # 只有管理员可以操作

    # queryset: 定义查询的数据范围
    #   过滤掉 is_deleted=True 的（软删除的）用户
    queryset = User.objects.filter(is_deleted=False)

    # search_fields: 允许前端用 ?search=xxx 搜索的字段
    search_fields = ['username', 'email']

    # ordering_fields: 允许前端用 ?ordering=xxx 排序的字段
    ordering_fields = ['id', 'username', 'date_joined', 'role']

    # 默认排序（最新注册的在前）
    ordering = ['-date_joined']

    # ==================== 自定义方法 ====================

    def perform_destroy(self, instance):
        """
        【软删除】不真的删除数据库记录，只标记 is_deleted=True

        为什么用软删除？
          1. 误删除可以恢复
          2. 保留历史数据（学生成绩、创建记录等关联数据）
          3. 满足审计要求

        SQL 层面：UPDATE users SET is_deleted=1, is_active=0, updated_at=NOW() WHERE id=?
        而不是：DELETE FROM users WHERE id=?
        """
        instance.is_deleted = True
        instance.is_active = False  # 同时禁用账号登录
        instance.save(update_fields=['is_deleted', 'is_active', 'updated_at'])

    def retrieve(self, request, *args, **kwargs):
        """
        【GET /api/users/{id}/】查看用户详情

        调用链：
          1. Router 匹配 URL → GET /api/users/5/
          2. 框架调用 self.get_object() → User.objects.get(id=5, is_deleted=False)
          3. 序列化 → UserManageSerializer(instance).data
          4. 包装 → APIResponse.success(data=serializer.data)
        """
        instance = self.get_object()  # 从数据库获取对应 ID 的用户
        serializer = self.get_serializer(instance)  # 序列化为 JSON
        return APIResponse.success(data=serializer.data)

    def list(self, request, *args, **kwargs):
        """
        【GET /api/users/】分页查询用户列表

        调用链：
          1. 框架调用 self.filter_queryset(self.get_queryset()) → 过滤 + 搜索 + 排序
          2. 框架调用 self.paginate_queryset(queryset) → 分页（默认每页 20 条）
          3. 框架调用 serializer(queryset, many=True) → 批量序列化
          4. 框架返回分页 Response → {"count": 50, "results": [...]}

        我们重写是为了把分页响应包装成统一格式
        """
        response = super().list(request, *args, **kwargs)
        # response.data 格式：{"count": 50, "next": "...", "previous": "...", "results": [...]}
        return APIResponse.success(data=response.data)

    def create(self, request, *args, **kwargs):
        """
        【POST /api/users/】管理员创建用户

        调用链：
          1. 创建序列化器 → UserManageSerializer(data=request.data)
          2. 校验 → serializer.is_valid()
          3. 保存 → serializer.save() → create() → make_password() → User.objects.create()
          4. 包装响应 → APIResponse.success()
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return APIResponse.error(
                code=status.HTTP_400_BAD_REQUEST,
                message=self._get_first_error(serializer.errors),
            )
        user = serializer.save()
        return APIResponse.success(
            data=UserManageSerializer(user).data,
            message='用户创建成功',
            code=status.HTTP_201_CREATED,
        )

    def update(self, request, *args, **kwargs):
        """
        【PUT /api/users/{id}/】管理员修改用户
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            return APIResponse.error(
                code=status.HTTP_400_BAD_REQUEST,
                message=self._get_first_error(serializer.errors),
            )
        user = serializer.save()
        return APIResponse.success(
            data=UserManageSerializer(user).data,
            message='用户修改成功',
        )

    def destroy(self, request, *args, **kwargs):
        """
        【DELETE /api/users/{id}/】管理员删除用户（软删除）
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return APIResponse.success(message='用户已删除')

    def _get_first_error(self, errors):
        """辅助方法：提取第一条错误信息"""
        for field, messages in errors.items():
            if isinstance(messages, list):
                return str(messages[0])
            if isinstance(messages, dict):
                return self._get_first_error(messages)
            return str(messages)
        return '请求参数错误'
