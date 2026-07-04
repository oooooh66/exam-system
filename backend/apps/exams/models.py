"""考试模块 - 数据模型"""
from django.db import models
from apps.users.models import User
from apps.papers.models import Paper, PaperQuestion


class ExamSession(models.Model):
    """考试场次"""
    paper = models.ForeignKey(
        Paper, on_delete=models.CASCADE, related_name='exam_sessions',
        verbose_name='试卷',
        help_text='本次考试使用的试卷',
        db_comment='考试使用的试卷ID',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='考试名称',
        help_text='如"2024年期末考试"',
        db_comment='考试名称',
    )
    start_time = models.DateTimeField(
        verbose_name='考试开始时间',
        help_text='在此时间之后学生才能进入考试',
        db_comment='考试开始时间',
    )
    end_time = models.DateTimeField(
        verbose_name='考试结束时间',
        help_text='到达此时间后自动提交未交卷的考试',
        db_comment='考试结束时间，到达后自动提交',
    )
    students = models.ManyToManyField(
        User, blank=True, related_name='assigned_exams',
        verbose_name='指定参考学生',
        help_text='为空则开放给所有学生参加',
        db_comment='指定参考学生（为空则所有人可参加）',
    )

    class Status(models.TextChoices):
        UPCOMING = 'upcoming', '未开始'
        ONGOING = 'ongoing', '进行中'
        FINISHED = 'finished', '已结束'

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.UPCOMING,
        verbose_name='考试状态',
        help_text='upcoming=未开始，ongoing=进行中，finished=已结束',
        db_comment='考试状态：upcoming=未开始, ongoing=进行中, finished=已结束',
    )
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name='created_exams',
        verbose_name='发布人',
        help_text='发布该考试的教师或管理员',
        db_comment='发布人用户ID',
    )
    is_deleted = models.BooleanField(
        default=False, db_index=True,
        verbose_name='是否已删除',
        help_text='软删除标记',
        db_comment='软删除标记：1=已删除，0=正常',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间',
        help_text='考试首次发布的时间',
        db_comment='考试首次发布的时间',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间',
        help_text='考试信息最后修改的时间',
        db_comment='每次保存时自动更新为当前时间',
    )

    class Meta:
        db_table = 'exam_sessions'
        verbose_name = '考试场次'
        verbose_name_plural = verbose_name
        ordering = ['-start_time']

    def __str__(self):
        return f'{self.name} ({self.get_status_display()})'


class StudentAnswer(models.Model):
    """学生逐题答题记录"""
    exam_session = models.ForeignKey(
        ExamSession, on_delete=models.CASCADE, related_name='student_answers',
        verbose_name='考试场次',
        help_text='所属的考试',
        db_comment='所属考试场次ID',
    )
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='exam_answers',
        verbose_name='学生',
        help_text='答题的学生',
        db_comment='答题学生用户ID',
    )
    paper_question = models.ForeignKey(
        PaperQuestion, on_delete=models.CASCADE, related_name='student_answers',
        verbose_name='试卷题目',
        help_text='对应的试卷题目及其分值',
        db_comment='对应的试卷题目ID',
    )
    answer = models.JSONField(
        null=True, blank=True,
        verbose_name='学生答案',
        help_text='单选/判断存字符串，多选存数组，填空/简答存字符串',
        db_comment='学生提交的答案（JSON格式）',
    )
    is_correct = models.BooleanField(
        null=True, blank=True,
        verbose_name='是否回答正确',
        help_text='True=正确，False=错误，None=主观题待批改',
        db_comment='是否正确：1=正确, 0=错误, NULL=待批改',
    )
    score_obtained = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        verbose_name='实际得分',
        help_text='该题学生获得的分数，0分为打错，NULL为未批改',
        db_comment='该题实际得分，支持两位小数',
    )

    class Status(models.TextChoices):
        DRAFT = 'draft', '暂存'
        SUBMITTED = 'submitted', '已提交'
        GRADED = 'graded', '已批改'

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.DRAFT,
        verbose_name='答题状态',
        help_text='draft=暂存（未提交），submitted=已提交，graded=已批改',
        db_comment='答题状态：draft=暂存, submitted=已提交, graded=已批改',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='首次保存时间',
        help_text='答题记录首次创建的时间',
        db_comment='答题记录首次创建的时间',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='最后更新时间',
        help_text='答案最后保存的时间',
        db_comment='答案最后保存的时间',
    )

    class Meta:
        db_table = 'student_answers'
        verbose_name = '学生答题记录'
        verbose_name_plural = verbose_name
        unique_together = [['exam_session', 'student', 'paper_question']]
        indexes = [
            models.Index(fields=['exam_session', 'student'], name='idx_exam_student'),
        ]

    def __str__(self):
        return f'{self.student.username} - {self.paper_question.question.content[:20]}'


class ExamSubmission(models.Model):
    """考试提交记录"""
    exam_session = models.ForeignKey(
        ExamSession, on_delete=models.CASCADE, related_name='submissions',
        verbose_name='考试场次',
        help_text='所属的考试',
        db_comment='所属考试场次ID',
    )
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='exam_submissions',
        verbose_name='学生',
        help_text='提交考试的学生',
        db_comment='提交考试的学生用户ID',
    )

    class Status(models.TextChoices):
        NOT_STARTED = 'not_started', '未开始'
        IN_PROGRESS = 'in_progress', '答题中'
        SUBMITTED = 'submitted', '已提交'
        AUTO_SUBMITTED = 'auto_submitted', '时间到自动提交'

    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.NOT_STARTED,
        verbose_name='提交状态',
        help_text='not_started=未开始，in_progress=答题中，submitted=已提交，auto_submitted=超时自动提交',
        db_comment='提交状态：not_started=未开始, in_progress=答题中, submitted=已提交, auto_submitted=超时自动提交',
    )
    start_time = models.DateTimeField(
        null=True, blank=True,
        verbose_name='开始答题时间',
        help_text='学生点击"开始考试"的时间',
        db_comment='学生点击开始考试的时间',
    )
    submit_time = models.DateTimeField(
        null=True, blank=True,
        verbose_name='实际提交时间',
        help_text='学生点击"交卷"或系统自动提交的时间',
        db_comment='实际提交或自动提交的时间',
    )
    total_score = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True,
        verbose_name='考试总分',
        help_text='整场考试的实际得分，由各题得分汇总计算',
        db_comment='考试实际总分，由各题得分汇总',
    )
    is_deleted = models.BooleanField(
        default=False,
        verbose_name='是否已删除',
        help_text='软删除标记',
        db_comment='软删除标记：1=已删除，0=正常',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间',
        help_text='提交记录首次创建的时间',
        db_comment='提交记录首次创建的时间',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间',
        help_text='提交记录最后修改的时间',
        db_comment='每次保存时自动更新为当前时间',
    )

    class Meta:
        db_table = 'exam_submissions'
        verbose_name = '考试提交记录'
        verbose_name_plural = verbose_name
        unique_together = [['exam_session', 'student']]

    def __str__(self):
        return f'{self.student.username} - {self.exam_session.name}'
