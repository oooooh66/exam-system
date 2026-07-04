"""
自定义权限控制模块（Permission 层）
=========================
在整个请求链路中的位置：【权限校验 —— 在 URL 匹配之后、View 方法执行之前】

完整调用链（以 DELETE /api/users/5/ 为例）：
  1. URL 匹配 → path('users/', include(router.urls)) → DELETE /api/users/5/
  2. ★ 权限校验 ★ → DRF 框架调用 IsAdmin.has_permission(request, view)
        ↓  检查 request.user.role == 'admin' ？
        ↓  YES → 放行，继续执行 View 的 destroy() 方法
        ↓  NO  → 返回 403 Forbidden {"code":403, "message":"您没有执行此操作的权限"}
  3. View 方法执行 → UserViewSet.destroy() → 软删除用户

DRF 的权限执行时机（两个检查点）：
  has_permission(request, view)      → 在 View 方法执行之前调用（列表/创建接口）
  has_object_permission(request, view, obj) → 在对具体对象操作时调用（详情/修改/删除接口）

DRF 权限系统规则：
  - permission_classes 是 AND 关系（所有权限类都通过才算通过）
  - 返回 True 表示放行，False 表示拒绝
  - 不需要权限时设置 permission_classes = [] 或 [AllowAny]
"""
from rest_framework.permissions import BasePermission


# ============================================
# 1. 管理员权限 —— 仅 admin 角色可访问
# ============================================
class IsAdmin(BasePermission):
    """
    【管理员权限类】

    用法：在 View/ViexSet 中设置 permission_classes = [IsAdmin]

    检查逻辑：
      1. 必须有用户（request.user 不为空）
      2. 用户必须已认证（is_authenticated = True）
      3. 角色必须是 'admin'

    典型用途：用户管理 CRUD（/api/users/）
    """

    def has_permission(self, request, view):
        """
        通用权限检查（在任何操作之前执行）

        当用户访问 GET /api/users/（列表）时：
          只有管理员能看到所有用户列表，普通用户返回 403
        """
        return (
            request.user                          # 用户对象存在
            and request.user.is_authenticated      # 已通过 JWT 认证
            and request.user.role == 'admin'       # 角色是管理员
        )

    def has_object_permission(self, request, view, obj):
        """
        对象级权限检查（操作具体对象时执行）

        当用户访问 DELETE /api/users/5/（删除具体用户）时：
          DRF 先调用 get_object() 获取用户 5，然后调用这个方法

        obj 参数：被操作的具体对象（如 User 实例）
        """
        return self.has_permission(request, view)


# ============================================
# 2. 教师权限 —— admin 或 teacher 角色可访问
# ============================================
class IsTeacher(BasePermission):
    """
    【教师权限类】管理员也可以访问（因为 admin 拥有所有权限）

    检查逻辑：
      1. 必须有用户且已认证
      2. 角色是 'admin' 或 'teacher'

    典型用途：题库管理、试卷管理、考试管理
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ('admin', 'teacher')
        )

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


# ============================================
# 3. 学生权限 —— 仅 student 角色可访问
# ============================================
class IsStudent(BasePermission):
    """
    【学生权限类】只允许学生角色

    典型用途：参加考试、查看个人成绩
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'student'
        )

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


# ============================================
# 4. 管理员或教师权限（别名）
# ============================================
class IsAdminOrTeacher(BasePermission):
    """
    【管理员或教师权限】和 IsTeacher 逻辑相同，语义更明确
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role in ('admin', 'teacher')
        )

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


# ============================================
# 5. 对象所有者或管理员权限
# ============================================
class IsOwnerOrAdmin(BasePermission):
    """
    【所有者或管理员权限】只有当用户是"数据拥有者"或"管理员"时才能操作

    例子：
      - 学生只能看自己的成绩（obj.student == request.user）
      - 但管理员可以看所有人的成绩（request.user.role == 'admin'）

    判断逻辑：
      1. 先检查是不是管理员（→ 直接放行）
      2. 再检查对象上有没有 user/created_by/student 字段
      3. 如果有这些字段且等于当前用户 → 放行
      4. 都不满足 → 拒绝
    """

    def has_object_permission(self, request, view, obj):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        # 管理员：一切皆可
        if user.role == 'admin':
            return True

        # 检查常见的所有者字段
        if hasattr(obj, 'user') and obj.user == user:
            return True
        if hasattr(obj, 'created_by') and obj.created_by == user:
            return True
        if hasattr(obj, 'student') and obj.student == user:
            return True

        return False


# ============================================
# 6. 只读权限 —— 仅允许 GET/HEAD/OPTIONS 请求
# ============================================
class ReadOnly(BasePermission):
    """
    【只读权限】仅允许安全方法（不会修改数据的 HTTP 方法）

    安全方法包括：GET, HEAD, OPTIONS
    拒绝的方法：POST, PUT, PATCH, DELETE
    """

    def has_permission(self, request, view):
        return request.method in ('GET', 'HEAD', 'OPTIONS')


# ==================== 旧命名兼容 ====================
IsAdminPermission = IsAdmin
IsTeacherPermission = IsTeacher
IsStudentPermission = IsStudent
IsAdminOrTeacherPermission = IsAdminOrTeacher
IsOwnerOrAdminPermission = IsOwnerOrAdmin
