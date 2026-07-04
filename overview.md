# 在线考试系统 - 开发完成概览

## ✅ 全部 6 个步骤已完成

---

## 后端 API 接口总览

### 认证接口 `/api/auth/`
| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| POST | `/api/auth/register/` | 用户注册 | 公开 |
| POST | `/api/auth/login/` | 用户登录（返回 JWT） | 公开 |
| POST | `/api/auth/token/refresh/` | 刷新 Token | 公开 |
| POST | `/api/auth/token/verify/` | 验证 Token | 公开 |
| GET | `/api/auth/profile/` | 获取个人信息 | 需登录 |
| PUT | `/api/auth/profile/` | 修改个人信息 | 需登录 |
| POST | `/api/auth/change-password/` | 修改密码 | 需登录 |

### 用户管理 `/api/users/`
| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | `/api/users/` | 用户列表（分页/搜索） | Admin |
| POST | `/api/users/` | 创建用户 | Admin |
| GET | `/api/users/{id}/` | 查看用户详情 | Admin |
| PUT | `/api/users/{id}/` | 修改用户 | Admin |
| DELETE | `/api/users/{id}/` | 软删除用户 | Admin |

### 题库管理 `/api/questions/`
| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | `/api/questions/` | 题目列表（按类型/难度/分类过滤） | 所有人 |
| POST | `/api/questions/` | 创建题目 | Teacher/Admin |
| GET | `/api/questions/{id}/` | 查看题目详情 | 所有人 |
| PUT | `/api/questions/{id}/` | 修改题目 | Teacher/Admin |
| DELETE | `/api/questions/{id}/` | 软删除题目 | Teacher/Admin |
| POST | `/api/questions/import/` | Excel 批量导入 | Teacher/Admin |
| CRUD | `/api/question-categories/` | 分类管理 | Teacher/Admin |

### 试卷管理 `/api/papers/`
| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | `/api/papers/` | 试卷列表 | 所有人 |
| POST | `/api/papers/` | 创建试卷（含选题） | Teacher/Admin |
| GET | `/api/papers/{id}/` | 查看试卷详情（含题目） | 所有人 |
| PUT | `/api/papers/{id}/` | 修改试卷 | Teacher/Admin |
| DELETE | `/api/papers/{id}/` | 软删除试卷 | Teacher/Admin |
| POST | `/api/papers/{id}/add-question/` | 添加题目 | Teacher/Admin |
| DELETE | `/api/papers/{id}/remove-question/{qid}/` | 移除题目 | Teacher/Admin |

### 考试模块 `/api/exams/`
| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | `/api/exams/` | 考试列表 | 所有人 |
| POST | `/api/exams/` | 发布考试 | Teacher/Admin |
| DELETE | `/api/exams/{id}/` | 删除考试 | Teacher/Admin |
| POST | `/api/exams/{id}/start/` | 学生开始答题 | Student |
| POST | `/api/exams/{id}/save/` | 暂存答案 | Student |
| POST | `/api/exams/{id}/submit/` | 提交考试 | Student |
| GET | `/api/exams/my-exams/` | 我的考试列表 | Student |
| GET | `/api/exams/{id}/my-result/` | 查看答题结果 | Student |

### 成绩报表 `/api/reports/`
| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| GET | `/api/reports/exam/{id}/statistics/` | 考试统计 | Teacher/Admin |
| GET | `/api/reports/exam/{id}/export/` | 导出成绩 Excel | Admin |
| GET | `/api/reports/student-scores/` | 学生成绩列表 | Student |
| GET | `/api/reports/result/{id}/` | 答题详情 | Student |

---

## 项目结构

```
exam-system/
├── backend/
│   ├── config/                     # Django 配置
│   │   ├── settings.py             # 数据库/DRF/JWT/CORS
│   │   ├── urls.py                 # 路由入口
│   │   └── wsgi.py
│   ├── apps/
│   │   ├── users/                  # 用户模块
│   │   │   ├── models.py           # User (AbstractUser + role)
│   │   │   ├── serializers.py      # 注册/登录/个人信息
│   │   │   ├── views.py            # Register/Login/Profile/CRUD
│   │   │   ├── urls.py
│   │   │   └── management/commands/init_data.py
│   │   ├── questions/              # 题库模块
│   │   │   ├── models.py           # QuestionCategory, Question
│   │   │   ├── serializers.py
│   │   │   ├── views.py            # CRUD + Excel 导入
│   │   │   └── urls.py
│   │   ├── papers/                 # 试卷模块
│   │   │   ├── models.py           # Paper, PaperQuestion
│   │   │   ├── serializers.py
│   │   │   ├── views.py            # 组卷/选题/换题
│   │   │   └── urls.py
│   │   ├── exams/                  # 考试模块
│   │   │   ├── models.py           # ExamSession, StudentAnswer, ExamSubmission
│   │   │   ├── serializers.py
│   │   │   ├── views.py            # 发布/答题/提交/自动批改
│   │   │   ├── scoring.py          # 评分引擎
│   │   │   └── urls.py
│   │   └── reports/                # 成绩模块
│   │       ├── views.py            # 统计/导出/成绩查询
│   │       └── urls.py
│   ├── utils/
│   │   ├── response.py             # APIResponse 统一格式
│   │   ├── exceptions.py           # 全局异常处理
│   │   ├── permissions.py          # IsAdmin/IsTeacher/IsStudent
│   │   └── excel_importer.py       # Excel 批量导入
│   ├── .env                        # 环境变量
│   ├── requirements.txt
│   └── manage.py
├── frontend/
│   └── src/
│       ├── api/                    # API 接口封装
│       │   ├── auth.ts, users.ts, questions.ts, papers.ts, exams.ts, reports.ts
│       ├── stores/auth.ts          # Pinia 认证状态
│       ├── router/index.ts         # Vue Router + 角色守卫
│       ├── utils/request.ts        # Axios 封装 + Token 刷新
│       ├── layouts/DashboardLayout.vue  # 主布局（侧边栏+顶部）
│       └── views/
│           ├── auth/LoginView.vue, RegisterView.vue
│           ├── admin/              # 管理员/教师页面
│           │   ├── DashboardView.vue
│           │   ├── UserManagement.vue
│           │   ├── QuestionManagement.vue
│           │   ├── PaperManagement.vue
│           │   ├── PaperEditor.vue
│           │   ├── ExamManagement.vue
│           │   └── ScoreReports.vue
│           ├── teacher/DashboardView.vue
│           └── student/
│               ├── DashboardView.vue
│               ├── ExamListView.vue
│               ├── ExamTakingView.vue    # 考试答题页(倒计时/自动保存)
│               └── MyScoresView.vue
└── sql/init_database.sql
```

---

## 核心技术实现

| 特性 | 实现方式 |
|------|----------|
| JWT 认证 | SimpleJWT + Token 黑名单 + 自定义 payload（role） |
| 角色权限 | 自定义 DRF BasePermission（IsAdmin/IsTeacher/IsStudent） |
| 软删除 | is_deleted 布尔字段，所有删除操作标记而非物理删除 |
| 统一响应 | APIResponse 类包装 `{code, message, data}` |
| 异常处理 | 全局异常处理 → 统一 JSON 错误响应 |
| 自动批改 | 单选/多选/判断自动匹配判分，填空/简答标记待批改 |
| Excel 导入 | openpyxl 解析 + Django bulk_create 批量写入 |
| Token 刷新 | Axios 拦截器 401 → 自动刷新 → 重试原请求 |
| 倒计时 | setInterval 1 秒刷新 + 时间到自动提交 |
| 答题暂存 | 每次切换题目触发保存 API |
| Excel 导出 | openpyxl 生成成绩单，带样式和自动列宽 |
| API 文档 | drf-spectacular → Swagger UI / ReDoc |

## 启动方式

```bash
# 后端
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py init_data         # 创建默认用户
python manage.py runserver 8000

# 前端
cd frontend
npm install
npm run dev                        # http://localhost:5173
```

## 默认账号
- 管理员：`admin` / `admin123`
- 教师：`teacher` / `teacher123`
- 学生：`student` / `student123`
