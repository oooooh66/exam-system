"""
题库模块 - 序列化器
"""
from rest_framework import serializers

from apps.questions.models import BusiQuestionCategory, BusiQuestion


class BusiQuestionCategorySerializer(serializers.ModelSerializer):
    """题目分类序列化器"""
    question_count = serializers.SerializerMethodField(read_only=True, help_text='该分类下的题目数量')

    class Meta:
        model = BusiQuestionCategory
        fields = [
            'id', 'name', 'description', 'question_count',
            'created_by', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

    def get_question_count(self, obj):
        """获取该分类下未删除的题目数量"""
        return BusiQuestion.objects.filter(category=obj, is_deleted=False).count()


class BusiQuestionSerializer(serializers.ModelSerializer):
    """题目序列化器（完整信息）"""
    question_type_display = serializers.CharField(source='get_question_type_display', read_only=True)
    difficulty_display = serializers.CharField(source='get_difficulty_display', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    # category 用 CharField 接收，允许前端传分类名称或ID字符串
    # 实际的外键对象在 validate() 中做转换
    category = serializers.CharField(required=False, allow_null=True, allow_blank=True, help_text='分类ID或分类名称')

    class Meta:
        model = BusiQuestion
        fields = [
            'id', 'question_type', 'question_type_display',
            'content', 'options', 'correct_answer', 'analysis',
            'category', 'category_name', 'difficulty', 'difficulty_display',
            'default_score', 'org_id', 'org_nm', 'created_by', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

    def validate_category(self, value):
        """
        校验 category 字段 —— 只做格式检查，不返回 Model 对象

        CharField 期望 validate_xxx 返回的还是字符/None，
        如果返回 QuestionCategory 实例会导致 DRF 报
        "期待为字典类型，得到的是 {datatype}" 的校验错误
        """
        if value is None or value == '':
            return None
        # 数字字符串 → 检查对应 ID 的分类是否存在
        if str(value).isdigit():
            if not BusiQuestionCategory.objects.filter(id=int(value), is_deleted=False).exists():
                raise serializers.ValidationError(f'分类 ID {value} 不存在')
        # 返回原始值（字符串），分类对象转换放到 validate() 里做
        return value

    def _resolve_category(self, value):
        """
        将 category 的字符串值转换为 QuestionCategory 模型实例

        支持三种输入：
        - None / 空字符串 → 返回 None
        - 纯数字字符串 "3" → 按 ID 查分类
        - 其他字符串 "单选题分类" → 按名称查找，找不到则自动创建
        """
        if value is None or value == '':
            return None
        if str(value).isdigit():
            return BusiQuestionCategory.objects.get(id=int(value), is_deleted=False)
        category, _ = BusiQuestionCategory.objects.get_or_create(
            name=str(value).strip(),
            defaults={'created_by': self.context['request'].user},
        )
        return category

    def validate(self, attrs):
        """根据题目类型校验字段完整性，并转换 category 为外键对象"""
        question_type = attrs.get('question_type', self.instance.question_type if self.instance else None)

        if question_type in ('single_choice', 'multiple_choice'):
            # 选择题必须有选项
            options = attrs.get('options', self.instance.options if self.instance else [])
            if not options or len(options) < 2:
                raise serializers.ValidationError({'options': '选择题至少需要 2 个选项'})

        if question_type == 'true_false':
            # 判断题答案只接受 对/错
            answer = attrs.get('correct_answer', self.instance.correct_answer if self.instance else None)
            if answer not in ('对', '错', True, False):
                raise serializers.ValidationError({'correct_answer': '判断题答案只能是"对"或"错"'})

        if question_type == 'fill_blank':
            # 填空题至少要有答案
            answer = attrs.get('correct_answer', self.instance.correct_answer if self.instance else None)
            if not answer:
                raise serializers.ValidationError({'correct_answer': '填空题必须填写正确答案'})

        # 把 category 的字符串/ID 值转换为外键对象
        # 这个转换必须放在 validate() 里而不是 validate_category() 里，
        # 因为 CharField 的 validate_xxx 方法只能返回字符串或 None，
        # 返回 Model 实例会导致 "期待为字典类型" 的校验错误
        if 'category' in attrs:
            attrs['category'] = self._resolve_category(attrs['category'])

        return attrs


class BusiQuestionListSerializer(serializers.ModelSerializer):
    """
    题目列表序列化器（简化版，不包含正确答案和解析）

    用于教师选题时浏览题目列表，避免直接暴露答案。
    管理员和教师可以通过详情接口查看完整信息。
    """
    question_type_display = serializers.CharField(source='get_question_type_display', read_only=True)
    difficulty_display = serializers.CharField(source='get_difficulty_display', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = BusiQuestion
        fields = [
            'id', 'question_type', 'question_type_display',
            'content', 'options',
            'category', 'category_name', 'difficulty', 'difficulty_display',
            'default_score', 'org_nm', 'created_at',
        ]


class BusiQuestionImportSerializer(serializers.Serializer):
    """
    Excel 批量导入题目的校验序列化器

    请求格式：multipart/form-data
    字段：
    - file: Excel 文件（.xlsx/.xls）
    - category_id: 默认分类 ID（可选，Excel 中可覆盖）
    """
    file = serializers.FileField(
        help_text='Excel 文件（.xlsx 或 .xls 格式）',
    )
    category_id = serializers.IntegerField(
        required=False,
        allow_null=True,
        help_text='默认分类 ID（Excel 中未指定分类时使用）',
    )

    def validate_file(self, value):
        """校验文件类型"""
        if not value.name.endswith(('.xlsx', '.xls')):
            raise serializers.ValidationError('仅支持 .xlsx 或 .xls 格式的 Excel 文件')
        if value.size > 10 * 1024 * 1024:  # 10MB
            raise serializers.ValidationError('文件大小不能超过 10MB')
        return value
