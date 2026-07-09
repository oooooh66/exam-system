"""
用户模块 - 序列化器（Serializer 层）
==========================
在整个请求链路中的位置：【倒数第二步 —— 数据校验与转换】

调用链：
  前端请求 → URL路由 → 权限校验 → View视图 → ★ Serializer序列化器 → Model模型 → 数据库

Serializer 的作用：
  1. 【请求方向】校验前端传来的 JSON 数据是否合法（类型、长度、必填、格式）
  2. 【请求方向】将前端 JSON 数据转换为 Python 对象（反序列化）
  3. 【响应方向】将 Python 对象（Model 实例）转换为 JSON 返回给前端（序列化）
  4. 处理密码加密、外键关联等需要在存储前做的转换

类比：Serializer 就是一个"门卫 + 翻译官"
  - 门卫：检查数据是否合法（validate）
  - 翻译官：JSON ↔ Python 对象互转
"""

# ==================== 从 Django 的请求/响应框架中获取 Serializer 基类 ====================
from rest_framework import serializers

# ==================== 导入我们自定义的 User 模型 ====================
from apps.users.models import BusiUser

# ==================== 导入 SimpleJWT 的 Token 序列化器（我们要继承它来扩展） ====================
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# ============================================
# 1. 登录序列化器 —— 处理 POST /api/auth/login/
# ============================================
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    【登录专用】自定义 JWT Token 序列化器

    调用链路（以 POST /api/auth/login/ 为例）：
      1. 前端发来 JSON → {"username": "admin", "password": "admin123"}
      2. URL 路由匹配到 CustomTokenObtainPairView（views.py）
      3. DRF 框架把这个 JSON 传给这个 Serializer
      4. Serializer 调用父类 validate() 校验用户名密码
      5. 校验通过 → 生成 JWT Token（access + refresh）
      6. 调用 get_token() 在 Token 的 payload 里塞入自定义字段
      7. 调用 validate() 在响应里额外返回 user 信息
      8. 最终返回 → {"code":200, "message":"登录成功", "data":{"access":"...", "refresh":"...", "user":{...}}}
    """

    @classmethod
    def get_token(cls, user):
        """
        【生成 Token 时调用】在 JWT 的 payload 中添加自定义信息

        JWT Token 的结构（三段 Base64 编码）：
          Header.Payload.Signature
                ^^^^^^^ 这里就是我们能自定义的地方

        解码后的 payload 示例：
          {
            "token_type": "access",
            "exp": 1710000000,       # 过期时间
            "user_id": 1,            # 用户 ID
            "username": "admin",     # ← 我们加的
            "role": "admin"          # ← 我们加的（前端根据这个判断权限）
          }
        """
        # 1. 先调用父类方法，生成标准的 JWT Token（包含 user_id、过期时间等）
        token = super().get_token(user)

        # 2. 在标准 payload 基础上，添加我们需要的额外字段
        token['username'] = user.username   # 用户名
        token['role'] = user.role           # 角色（前端路由守卫用这个做权限控制）

        return token

    def validate(self, attrs):
        """
        【登录校验时调用】校验用户名密码，并在登录响应中返回用户信息

        attrs 参数：前端传来的原始数据 → {"username": "admin", "password": "admin123"}

        执行流程：
          1. 调用父类 validate() → 用 Django 的 authenticate() 校验用户名密码
          2. 校验通过 → self.user 被赋值为登录成功的 User 对象
          3. 拿到父类返回的标准 data → {"access": "xxx", "refresh": "xxx"}
          4. 在 data 中追加 user 信息（前端需要显示用户名、角色）
          5. 返回完整的 data
        """
        # 1. 父类校验：检查用户名密码是否正确
        #    内部会调用 Django 的 authenticate(username=..., password=...)
        #    如果校验失败会直接抛出 AuthenticationFailed 异常
        data = super().validate(attrs)

        # 2. 校验通过，self.user 就是登录的 User 对象
        user = self.user

        # 3. 在响应数据中追加用户信息（前端需要这些数据渲染界面）
        data['user'] = {
            'id': user.id,
            'username': user.username,
            'role': user.role,
            'role_display': user.get_role_display(),  # 如 '管理员'、'教师'、'学生'
        }

        return data


# ============================================
# 2. 注册序列化器 —— 处理 POST /api/auth/register/
# ============================================
class RegisterSerializer(serializers.ModelSerializer):
    """
    【注册专用】用户注册序列化器

    调用链路（以 POST /api/auth/register/ 为例）：
      1. 前端发来 JSON → {"username":"newuser", "password":"123456", "password_confirm":"123456", "role":"student"}
      2. View 创建这个 Serializer，传入 data=request.data
      3. 调用 is_valid() → 触发字段校验和全局校验
      4. 校验通过 → 调用 save() → 内部调用 create() 写入数据库
      5. 返回 → {"code":201, "message":"注册成功", "data":{"id":3, "username":"newuser", "role":"student"}}
    """

    # ==================== 定义需要额外处理的字段 ====================

    # password 字段：前端传来的原始密码，标记为 write_only
    #   - write_only=True: 只用于接收输入，序列化输出时不包含（安全考虑）
    password = serializers.CharField(
        write_only=True,
        min_length=6,         # 最少 6 位
        max_length=128,       # 最多 128 位
        style={'input_type': 'password'},  # 在 DRF 的 Browsable API 中渲染为密码输入框
        help_text='密码，最少 6 位',
    )

    # password_confirm 字段：确认密码，仅用于校验，不存库
    password_confirm = serializers.CharField(
        write_only=True,
        min_length=6,
        max_length=128,
        style={'input_type': 'password'},
        help_text='确认密码',
    )

    # role 字段：用户角色，限定只能选预定义的选项
    role = serializers.ChoiceField(
        choices=BusiUser.Role.choices,
        help_text='用户角色',
    )

    # ==================== Meta 内部类：关联 Model 和字段 ====================
    class Meta:
        # model: 告诉 Serializer 这个序列化器对应哪个数据库表
        model = BusiUser
        # fields: 指定哪些字段参与序列化/反序列化
        #   - password 和 password_confirm 在上面单独定义了
        #   - id 是只读的（由数据库自动生成）
        fields = ['id', 'username', 'password', 'password_confirm', 'role']
        extra_kwargs = {
            'username': {
                'min_length': 3,
                'max_length': 150,
                'help_text': '用户名，3-150 个字符',
            },
        }

    # ==================== 字段级校验 ====================

    def validate_username(self, value):
        """
        【注册校验——用户名唯一性检查】
        在当前未删除的用户中，检查这个用户名是否已被占用

        这个方法名必须遵循 Django 命名规范：validate_<field_name>

        value: 前端传来的用户名（如 "newuser"）
        返回: 校验通过则返回原值；失败则抛出 ValidationError
        """
        if BusiUser.objects.filter(username=value, is_deleted=False).exists():
            raise serializers.ValidationError('该用户名已被注册')
        return value  # 校验通过，原样返回

    # ==================== 对象级校验 ====================

    def validate(self, attrs):
        """
        【注册校验——全局校验】所有字段校验通过后，在这里做跨字段校验

        attrs 参数：所有字段校验通过后的数据字典 → {
            "username": "newuser",
            "password": "123456",
            "password_confirm": "123456",
            "role": "student"
        }
        """
        # 检查两次密码是否一致
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({
                'password_confirm': '两次输入的密码不一致'
            })
        return attrs  # 校验通过，返回清洗后的数据

    # ==================== 数据持久化 ====================

    def create(self, validated_data):
        """
        【注册核心——创建用户记录写入数据库】

        当调用 serializer.save() 时，DRF 框架内部会调用这个方法

        validated_data 参数：经过所有校验后的干净数据 → {
            "username": "newuser",
            "password": "123456",
            "role": "student"
        }
        （password_confirm 已在前面被 pop 掉了）

        流程：
          1. 删除 password_confirm（不需要存库）
          2. 用 make_password() 将明文密码哈希加密（绝对不能明文存储！）
          3. 调用父类 create() 执行 INSERT INTO users (...) VALUES (...)
        """
        # 1. 删除确认密码字段（不需要存入数据库）
        validated_data.pop('password_confirm')

        # 2. 密码加密：用 Django 的 PBKDF2 + SHA256 算法哈希
        #    数据库里存的是这种格式：pbkdf2_sha256$260000$salt$hash
        #    这就是为什么即使数据库泄露，密码也不会被直接看到
        validated_data['password'] = make_password(validated_data['password'])

        # 3. 调用父类 ModelSerializer 的 create() 方法
        #    内部执行：BusiUser.objects.create(**validated_data)
        #    Django ORM 翻译成 SQL：INSERT INTO users VALUES (...)
        return super().create(validated_data)


# ============================================
# 3. 个人信息序列化器 —— 处理 GET/PUT /api/auth/profile/
# ============================================
class BusiUserProfileSerializer(serializers.ModelSerializer):
    """
    【个人信息】查看和修改个人资料

    read_only_fields: id, username, role 这些字段只能看不能改
    可以修改的字段：email

    调用场景：
      - GET 请求 → 把 User 实例序列化成 JSON 返回
      - PUT 请求 → 把前端 JSON 校验后，更新数据库中的 User 记录
    """
    # 只读字段：根据 role 值动态生成对应的中文显示（需要 source 指定数据来源）
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = BusiUser
        fields = [
            'id', 'username', 'email', 'role', 'role_display',
            'date_joined', 'last_login', 'created_at', 'updated_at',
        ]
        # read_only_fields 里的字段在 PUT/PATCH 请求时不会被修改
        read_only_fields = ['id', 'username', 'role', 'date_joined', 'last_login', 'created_at', 'updated_at']


# ============================================
# 4. 修改密码序列化器 —— 处理 POST /api/auth/change-password/
# ============================================
class ChangePasswordSerializer(serializers.Serializer):
    """
    【修改密码】不需要关联 Model，所以继承 Serializer（不是 ModelSerializer）

    三个字段都是 write_only，因为密码绝不能出现在响应中返回给前端
    """
    old_password = serializers.CharField(write_only=True, min_length=6)
    new_password = serializers.CharField(write_only=True, min_length=6, max_length=128)
    new_password_confirm = serializers.CharField(write_only=True, min_length=6, max_length=128)

    def validate_old_password(self, value):
        """校验旧密码是否正确 —— 用 Django 的 check_password() 验证"""
        # self.context['request'].user 是 View 层传进来的当前登录用户
        user = self.context['request'].user
        if not user.check_password(value):
            # check_password() 内部：用相同的哈希算法加密用户输入，对比数据库中的密文
            raise serializers.ValidationError('旧密码不正确')
        return value

    def validate(self, attrs):
        """全局校验：两次新密码必须一致"""
        if attrs.get('new_password') != attrs.get('new_password_confirm'):
            raise serializers.ValidationError({'new_password_confirm': '两次输入的新密码不一致'})
        return attrs

    def save(self):
        """
        【核心】保存新密码到数据库

        调用 set_password() 会自动哈希，然后 save() 写入数据库
        """
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])  # 加密新密码
        user.save()  # UPDATE users SET password='xxx' WHERE id=...
        return user


# ============================================
# 5. 管理员用户管理序列化器 —— 处理 /api/users/ CRUD
# ============================================
class BusiUserManageSerializer(serializers.ModelSerializer):
    """
    【管理员专用】批量管理用户的增删改查

    与 RegisterSerializer 的区别：
      - RegisterSerializer：任何人都可以注册（公开接口）
      - BusiUserManageSerializer：只有管理员可以操作（需要 IsAdmin 权限）
      - 这个序列化器可以编辑更多字段（email、is_active 等）
    """
    password = serializers.CharField(write_only=True, min_length=6, max_length=128, required=False)
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = BusiUser
        fields = [
            'id', 'username', 'email', 'password', 'role', 'role_display',
            'is_active', 'date_joined', 'last_login', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'date_joined', 'last_login', 'created_at', 'updated_at']

    def create(self, validated_data):
        """
        【管理员创建用户】密码必填，用 make_password 加密后存库

        这个方法在 POST /api/users/ 时被调用
        """
        password = validated_data.pop('password', None)
        if password:
            validated_data['password'] = make_password(password)
        # 调用父类 create() → BusiUser.objects.create(**validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        【管理员修改用户】密码可选，提供了才更新

        这个方法在 PUT /api/users/{id}/ 时被调用

        参数：
          - instance: 数据库中的现有用户记录（要被修改的对象）
          - validated_data: 前端传来的更新数据
        """
        password = validated_data.pop('password', None)
        if password:
            # 只有提供了新密码才加密更新
            validated_data['password'] = make_password(password)
        # 调用父类 update() → 逐字段赋值后 save()
        return super().update(instance, validated_data)
