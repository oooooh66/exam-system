"""试卷模块 - 序列化器"""
from decimal import Decimal

from rest_framework import serializers

from apps.papers.models import Paper, PaperQuestion
from apps.questions.serializers import QuestionSerializer


class PaperQuestionSerializer(serializers.ModelSerializer):
    """试卷题目关联序列化器"""
    question_detail = QuestionSerializer(source='question', read_only=True)

    class Meta:
        model = PaperQuestion
        fields = ['id', 'question', 'question_detail', 'order', 'score']


class PaperQuestionCreateSerializer(serializers.Serializer):
    """
    创建试卷题目关联的简化序列化器

    调用链（以 POST /api/papers/ 为例）：
      前端 JSON → {"questions":[{"question_id":5,"score":4.5,"order":0}, ...]}
        ↓
      PaperCreateSerializer(data=request.data)
        ↓ 嵌套校验 questions 列表
      ★ PaperQuestionCreateSerializer(data=each_question)
        ↓ 校验每个字段
        question_id: IntegerField → 必须是整数
        score: ★ DecimalField → 支持小数如 4.5
        order: IntegerField → 必须是整数
        ↓ 校验通过
      PaperCreateSerializer.create() → PaperQuestion.objects.create(score=4.5, ...)
        ↓
      INSERT INTO paper_questions (score, ...) VALUES (4.5, ...)

    ⚠️ 如果报类似 "请填写合法的整数值" 的校验错误，说明 Model 字段类型和 Serializer 字段类型不一致。
       排查步骤：
       1. 找到 Model 中的字段定义 → 看是什么类型（IntegerField / DecimalField / ...）
       2. 找到对应的 Serializer 字段 → 看是什么类型
       3. 两者不一致时，修改 Serializer 字段以匹配 Model
    """
    question_id = serializers.IntegerField(
        help_text='题目ID（必须存在于题库中）',
    )
    # score 字段类型必须与 PaperQuestion.score（DecimalField）保持一致
    # 之前是 IntegerField → 导致前端传 4.5 时报"请填写合法的整数值"
    score = serializers.DecimalField(
        max_digits=5,
        decimal_places=2,
        min_value=Decimal('0.5'),
        help_text='本题分值，支持两位小数，如 4.5 分',
    )
    order = serializers.IntegerField(
        default=0,
        min_value=0,
        help_text='题目在试卷中的展示顺序，数字越小越靠前',
    )


class PaperSerializer(serializers.ModelSerializer):
    """试卷列表序列化器（不含题目详情，减少数据传输量）"""
    question_count = serializers.SerializerMethodField()
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Paper
        fields = [
            'id', 'name', 'description', 'total_score', 'pass_score',
            'duration_minutes', 'question_count', 'created_by', 'created_by_name',
            'created_at', 'updated_at',
        ]

    def get_question_count(self, obj):
        return obj.paper_questions.count()


class PaperDetailSerializer(serializers.ModelSerializer):
    """试卷详情序列化器（含完整题目列表）"""
    paper_questions = PaperQuestionSerializer(many=True, read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Paper
        fields = [
            'id', 'name', 'description', 'total_score', 'pass_score',
            'duration_minutes', 'paper_questions', 'created_by', 'created_by_name',
            'created_at', 'updated_at',
        ]


class PaperCreateSerializer(serializers.ModelSerializer):
    """创建试卷序列化器"""
    questions = PaperQuestionCreateSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = Paper
        fields = [
            'id', 'name', 'description', 'pass_score', 'duration_minutes', 'questions',
        ]

    def create(self, validated_data):
        questions_data = validated_data.pop('questions', [])
        paper = Paper.objects.create(**validated_data, created_by=self.context['request'].user)

        # 关联题目
        for q_data in questions_data:
            from apps.questions.models import Question
            question = Question.objects.get(id=q_data['question_id'], is_deleted=False)
            PaperQuestion.objects.create(
                paper=paper,
                question=question,
                score=q_data.get('score', question.default_score),
                order=q_data.get('order', 0),
            )

        # 计算总分
        paper.update_total_score()
        return paper


class PaperUpdateSerializer(serializers.ModelSerializer):
    """修改试卷序列化器"""
    questions = PaperQuestionCreateSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = Paper
        fields = ['name', 'description', 'pass_score', 'duration_minutes', 'questions']

    def update(self, instance, validated_data):
        questions_data = validated_data.pop('questions', None)

        # 更新基本字段
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # 如果提供了题目列表，则替换全部题目
        if questions_data is not None:
            instance.paper_questions.all().delete()
            for q_data in questions_data:
                from apps.questions.models import Question
                question = Question.objects.get(id=q_data['question_id'], is_deleted=False)
                PaperQuestion.objects.create(
                    paper=instance,
                    question=question,
                    score=q_data.get('score', question.default_score),
                    order=q_data.get('order', 0),
                )
            instance.update_total_score()

        return instance
