"""
用户模块 - 数据模型（Model 层）
=====================
在整个请求链路中的位置：【最后一步 —— 与数据库交互】

调用链：
  前端请求 → URL路由 → 权限校验 → View视图 → Serializer序列化器 → ★ Model模型 → 数据库

Model 的作用：
  1. 用 Python 类定义数据库表结构（字段名、类型、约束）
  2. Django ORM 会自动把 Python 类翻译成建表 SQL（通过 migrate 命令）
  3. 在代码中通过 Model.objects.xxx() 操作数据库，不需要写原生 SQL
  4. 每个 Model 实例 = 数据库中的一行记录

例子：
  BusiUser.objects.create(username='admin', password='...')
    → Django ORM 翻译成 INSERT INTO users VALUES (...)
  BusiUser.objects.filter(role='student')
    → Django ORM 翻译成 SELECT * FROM users WHERE role='student'
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class BusiUser(AbstractUser):
    """
    【数据库表映射类】自定义用户模型

    继承 Django 内置的 AbstractUser，自动拥有以下字段（不用自己写）：
      - username   : 用户名（唯一）
      - password   : 密码（自动哈希）
      - email      : 邮箱
      - first_name : 名
      - last_name  : 姓
      - is_active  : 是否激活（True=正常, False=禁用）
      - is_staff   : 是否可登录 Django Admin
      - is_superuser: 是否为超级管理员
      - last_login : 最后登录时间
      - date_joined: 注册时间

    我们额外扩展的字段：
      - role        : 用户角色（管理员 / 教师 / 学生）
      - is_deleted  : 软删除标记
      - created_at  : 创建时间
      - updated_at  : 更新时间
    """

    # ==================== 角色枚举类 ====================
    # TextChoices 是 Django 提供的枚举类型，数据库存英文值，界面上显示中文标签
    class Role(models.TextChoices):
        ADMIN = 'admin', '管理员'          # 数据库中存 'admin'，界面显示 '管理员'
        TEACHER = 'teacher', '教师'        # 数据库中存 'teacher'，界面显示 '教师'
        STUDENT = 'student', '学生'        # 数据库中存 'student'，界面显示 '学生'

    # ==================== 自定义字段 ====================

    # role 字段：用户角色
    #   - max_length=20: 数据库列最大长度
    #   - choices=Role.choices: 限定值只能是 admin/teacher/student
    #   - default=Role.STUDENT: 新用户默认是学生
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
        verbose_name='角色',
        help_text='用户角色：管理员(admin)/教师(teacher)/学生(student)',
        db_comment='用户角色：admin=管理员, teacher=教师, student=学生',
    )

    # is_deleted 字段：软删除标记
    #   - 值为 True 时表示"已删除"，但数据仍在数据库中
    #   - db_index=True: 给这个字段建索引，加快查询速度
    #   - 优点：误删可以恢复，保留历史审计记录
    is_deleted = models.BooleanField(
        default=False,
        verbose_name='是否已删除',
        help_text='软删除标记：True=已删除(不可见)，False=正常',
        db_comment='软删除标记：1=已删除，0=正常',
        db_index=True,
    )

    # created_at 字段：创建时间
    #   - auto_now_add=True: 记录第一次被创建的时间，之后不再自动更新
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间',
        help_text='账号首次创建的时间',
        db_comment='记录首次创建的时间，创建后不再自动更新',
    )

    # updated_at 字段：更新时间
    #   - auto_now=True: 每次保存（save()）都会自动更新为当前时间
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间',
        help_text='账号最后修改的时间',
        db_comment='每次保存时自动更新为当前时间',
    )

    # ==================== Meta 内部类：表级别配置 ====================
    class Meta:
        # db_table: 指定数据库中的表名（不指定则 Django 自动生成 appname_modelname）
        db_table = 'busi_users'
        # verbose_name: 在 Django Admin 后台显示的中文名称（单数）
        verbose_name = '用户'
        # verbose_name_plural: 复数形式
        verbose_name_plural = verbose_name
        # ordering: 默认排序规则（- 表示降序，即最新注册的排在前面）
        ordering = ['-date_joined']

    # ==================== __str__ 方法：对象的友好字符串表示 ====================
    def __str__(self):
        """返回对象的可读描述，在 Django Admin 后台和调试时使用"""
        return f'{self.username} ({self.get_role_display()})'

    # ==================== 便捷属性：快速判断用户角色 ====================
    # @property 装饰器让方法可以像属性一样调用（不用加括号）
    # 用法：user.is_admin  而不是 user.is_admin()

    @property
    def is_admin(self):
        """判断是否为管理员 —— 用法: if user.is_admin: ..."""
        return self.role == self.Role.ADMIN

    @property
    def is_teacher(self):
        """判断是否为教师 —— 用法: if user.is_teacher: ..."""
        return self.role == self.Role.TEACHER

    @property
    def is_student(self):
        """判断是否为学生 —— 用法: if user.is_student: ..."""
        return self.role == self.Role.STUDENT
