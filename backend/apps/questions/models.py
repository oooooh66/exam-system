"""题库模块 - 数据模型"""
from django.db import models
from apps.users.models import BusiUser


class BusiQuestionCategory(models.Model):
    """题目分类"""
    name = models.CharField(
        max_length=100, unique=True,
        verbose_name='分类名称',
        help_text='分类的唯一标识名称，如"计算机基础"',
        db_comment='分类名称，唯一',
    )
    description = models.TextField(
        blank=True, default='',
        verbose_name='分类描述',
        help_text='分类的详细说明（选填）',
        db_comment='分类描述（选填）',
    )
    is_deleted = models.BooleanField(
        default=False, db_index=True,
        verbose_name='是否已删除',
        help_text='软删除标记：True=已删除，False=正常',
        db_comment='软删除标记：1=已删除，0=正常',
    )
    created_by = models.ForeignKey(
        BusiUser, on_delete=models.SET_NULL, null=True,
        related_name='question_categories',
        verbose_name='创建人',
        help_text='创建该分类的用户',
        db_comment='创建人用户ID',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间',
        help_text='记录首次创建的时间',
        db_comment='记录首次创建的时间',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间',
        help_text='记录最后修改的时间',
        db_comment='每次保存时自动更新为当前时间',
    )

    class Meta:
        db_table = 'busi_question_categories'
        verbose_name = '题目分类'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name


class BusiQuestion(models.Model):
    """题目模型，支持5种题型"""

    class QuestionType(models.TextChoices):
        SINGLE_CHOICE = 'single_choice', '单选题'
        MULTIPLE_CHOICE = 'multiple_choice', '多选题'
        TRUE_FALSE = 'true_false', '判断题'
        FILL_BLANK = 'fill_blank', '填空题'
        SHORT_ANSWER = 'short_answer', '简答题'

    class Difficulty(models.TextChoices):
        EASY = 'easy', '简单'
        MEDIUM = 'medium', '中等'
        HARD = 'hard', '困难'

    question_type = models.CharField(
        max_length=20, choices=QuestionType.choices,
        verbose_name='题目类型',
        help_text='single_choice/multiple_choice/true_false/fill_blank/short_answer',
        db_comment='题目类型：single_choice=单选, multiple_choice=多选, true_false=判断, fill_blank=填空, short_answer=简答',
    )
    content = models.TextField(
        verbose_name='题干内容',
        help_text='题目的文字描述，支持 Markdown 格式',
        db_comment='题干文字内容，支持Markdown格式',
    )
    options = models.JSONField(
        default=list, blank=True,
        verbose_name='选项列表',
        help_text='JSON数组，如 ["A. 北京", "B. 上海"]，仅选择题需要',
        db_comment='JSON数组格式的选项列表，仅选择题使用',
    )
    correct_answer = models.JSONField(
        verbose_name='正确答案',
        help_text='单选存字符串"A"，多选存数组["A","C"]，判断存"对"/"错"，填空简答存字符串',
        db_comment='正确答案：单选/判断存字符串，多选存JSON数组，填空/简答存字符串',
    )
    analysis = models.TextField(
        blank=True, default='',
        verbose_name='答案解析',
        help_text='对正确答案的详细解释，学生查看成绩时展示（选填）',
        db_comment='答案解析，学生查看成绩时展示',
    )
    category = models.ForeignKey(
        BusiQuestionCategory, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='questions',
        verbose_name='所属分类',
        help_text='题目归入的分类，便于管理和筛选',
        db_comment='所属分类ID，外键关联question_categories表',
    )
    difficulty = models.CharField(
        max_length=10, choices=Difficulty.choices, default=Difficulty.MEDIUM,
        verbose_name='难度等级',
        help_text='easy=简单，medium=中等，hard=困难',
        db_comment='难度等级：easy=简单, medium=中等, hard=困难',
    )
    org_id = models.CharField(
        max_length=50, blank=True, default='',
        verbose_name='机构号',
        help_text='试题所属机构的唯一编码',
        db_comment='机构唯一编码',
    )
    org_nm = models.CharField(
        max_length=100, blank=True, default='',
        verbose_name='机构名',
        help_text='试题所属机构的名称',
        db_comment='机构名称',
    )
    default_score = models.DecimalField(
        max_digits=5, decimal_places=2, default=5.00,
        verbose_name='默认分值',
        help_text='题目的默认分数，支持两位小数，在试卷中可被覆盖',
        db_comment='题目默认分值，支持两位小数，试卷中可覆盖',
    )
    created_by = models.ForeignKey(
        BusiUser, on_delete=models.SET_NULL, null=True,
        related_name='created_questions',
        verbose_name='创建人',
        help_text='出题人',
        db_comment='出题人用户ID',
    )
    is_deleted = models.BooleanField(
        default=False, db_index=True,
        verbose_name='是否已删除',
        help_text='软删除标记：True=已删除，False=正常',
        db_comment='软删除标记：1=已删除，0=正常',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间',
        help_text='题目首次创建的时间',
        db_comment='题目首次创建的时间',
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间',
        help_text='题目最后修改的时间',
        db_comment='每次保存时自动更新为当前时间',
    )

    class Meta:
        db_table = 'busi_questions'
        verbose_name = '题目'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['question_type'], name='idx_question_type'),
            models.Index(fields=['difficulty'], name='idx_difficulty'),
            models.Index(fields=['category'], name='idx_category'),
        ]

    def __str__(self):
        preview = self.content[:50] + '...' if len(self.content) > 50 else self.content
        return f'[{self.get_question_type_display()}] {preview}'
