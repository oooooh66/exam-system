"""试卷模块 - 数据模型"""
from django.db import models
from apps.users.models import BusiUser
from apps.questions.models import BusiQuestion, BusiQuestionCategory


class BusiPaper(models.Model):
    """试卷模型"""
    name = models.CharField(
        max_length=200,
        verbose_name='试卷名称',
        help_text='试卷的唯一标识名称',
        db_comment='试卷名称',
    )
    description = models.TextField(
        blank=True, default='',
        verbose_name='试卷描述',
        help_text='试卷的补充说明（选填）',
        db_comment='试卷描述（选填）',
    )
    total_score = models.DecimalField(
        max_digits=6, decimal_places=2, default=0.00,
        verbose_name='总分',
        help_text='试卷满分，由关联题目的分值自动汇总计算',
        db_comment='试卷满分，由关联题目分值汇总计算',
    )
    pass_score = models.DecimalField(
        max_digits=5, decimal_places=2, default=60.00,
        verbose_name='及格分数线',
        help_text='达到此分数即为及格',
        db_comment='及格分数线，支持两位小数',
    )
    duration_minutes = models.PositiveIntegerField(
        default=60,
        verbose_name='考试时长（分钟）',
        help_text='整场考试允许的最长答题时间',
        db_comment='考试时长，单位：分钟',
    )
    questions = models.ManyToManyField(
        BusiQuestion, through='BusiPaperQuestion', related_name='papers',
        verbose_name='题目列表',
        help_text='试卷包含的题目，通过 PaperQuestion 中间表关联',
        db_comment='试卷包含的题目，通过中间表关联',
    )
    created_by = models.ForeignKey(
        BusiUser, on_delete=models.SET_NULL, null=True,
        related_name='created_papers',
        verbose_name='出卷人',
        help_text='创建该试卷的教师或管理员',
        db_comment='出卷人用户ID',
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
        help_text='试卷首次创建的时间',
        db_comment='试卷首次创建的时间',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间',
        help_text='试卷最后修改的时间',
        db_comment='每次保存时自动更新为当前时间',
    )

    class Meta:
        db_table = 'busi_papers'
        verbose_name = '试卷'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def update_total_score(self):
        """重新计算试卷总分"""
        total = self.paper_questions.aggregate(s=models.Sum('score'))['s'] or 0
        self.total_score = total
        self.save(update_fields=['total_score', 'updated_at'])


class BusiPaperQuestion(models.Model):
    """试卷-题目关联表（中间表）"""
    paper = models.ForeignKey(
        BusiPaper, on_delete=models.CASCADE, related_name='paper_questions',
        verbose_name='所属试卷',
        help_text='关联的试卷',
        db_comment='所属试卷ID',
    )
    question = models.ForeignKey(
        BusiQuestion, on_delete=models.CASCADE, related_name='paper_questions',
        verbose_name='题目',
        help_text='关联的题目',
        db_comment='关联的题目ID',
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='排序序号',
        help_text='题目在试卷中的展示序号，数字越小越靠前',
        db_comment='题目展示序号，数字越小越靠前',
    )
    score = models.DecimalField(
        max_digits=5, decimal_places=2,
        verbose_name='本题分值',
        help_text='该题在本试卷中的分值，支持两位小数（可覆盖题目的默认分值）',
        db_comment='本题在试卷中的分值，支持两位小数',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='关联时间',
        help_text='题目被添加到试卷的时间',
        db_comment='题目被添加到试卷的时间',
    )

    class Meta:
        db_table = 'busi_paper_questions'
        verbose_name = '试卷-题目关联'
        verbose_name_plural = verbose_name
        ordering = ['order']
        unique_together = [['paper', 'question']]

    def __str__(self):
        return f'[{self.paper.name}] {self.question.content[:30]}'

    def save(self, *args, **kwargs):
        if not self.score:
            self.score = self.question.default_score
        super().save(*args, **kwargs)


class BusiPaperRandomRule(models.Model):
    """
    试卷随机抽题规则

    每个规则定义：从某个分类中随机抽取 N 道题目加入试卷。
    多个规则组合使用，可实现复杂的随机组卷逻辑。
    """
    paper = models.ForeignKey(
        BusiPaper, on_delete=models.CASCADE, related_name='random_rules',
        verbose_name='所属试卷',
        help_text='应用此规则的试卷',
        db_comment='所属试卷ID',
    )
    category = models.ForeignKey(
        BusiQuestionCategory, on_delete=models.CASCADE,
        related_name='random_rules',
        verbose_name='抽取分类',
        help_text='从哪个题目分类中随机抽取',
        db_comment='题目分类ID',
    )
    question_count = models.PositiveIntegerField(
        default=1,
        verbose_name='抽取数量',
        help_text='从该分类中随机抽取的题目数量',
        db_comment='随机抽取的题目数量',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间',
        help_text='规则创建的时间',
        db_comment='规则创建时间',
    )

    class Meta:
        db_table = 'busi_paper_random_rules'
        verbose_name = '随机抽题规则'
        verbose_name_plural = verbose_name
        unique_together = [['paper', 'category']]

    def __str__(self):
        return f'[{self.paper.name}] {self.category.name} × {self.question_count}'
