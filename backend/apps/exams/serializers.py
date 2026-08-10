"""考试模块 - 序列化器"""
from rest_framework import serializers

from apps.exams.models import BusiExamSession, BusiStudentAnswer, BusiExamSubmission
from apps.papers.models import BusiPaper
from apps.papers.serializers import BusiPaperSerializer


class BusiExamSessionListSerializer(serializers.ModelSerializer):
    """考试场次列表序列化器"""
    paper_name = serializers.CharField(source='paper.name', read_only=True)
    duration = serializers.IntegerField(source='paper.duration_minutes', read_only=True)
    total_score = serializers.IntegerField(source='computed_total_score', read_only=True)
    status = serializers.CharField(source='computed_status', read_only=True)
    student_count = serializers.SerializerMethodField()

    class Meta:
        model = BusiExamSession
        fields = [
            'id', 'name', 'paper', 'paper_name', 'total_score',
            'duration', 'start_time', 'end_time', 'status',
            'student_count', 'created_at', 'exam_scope',
        ]

    def get_student_count(self, obj):
        if obj.students.exists():
            return obj.students.count()
        return None  # None 表示开放所有人


class BusiExamSessionDetailSerializer(serializers.ModelSerializer):
    """考试场次详情序列化器"""
    paper = BusiPaperSerializer(read_only=True)
    submission_status = serializers.SerializerMethodField()

    class Meta:
        model = BusiExamSession
        fields = [
            'id', 'name', 'paper', 'start_time', 'end_time',
            'status', 'submission_status', 'created_at',
        ]

    def get_submission_status(self, obj):
        """获取当前学生的提交状态"""
        request = self.context.get('request')
        if not request or not request.user.is_authenticated:
            return None
        submission = BusiExamSubmission.objects.filter(
            exam_session=obj, student=request.user,
        ).first()
        if submission:
            return {
                'status': submission.status,
                'start_time': submission.start_time,
                'submit_time': submission.submit_time,
                'total_score': submission.total_score,
            }
        return None


class BusiExamSessionCreateSerializer(serializers.ModelSerializer):
    """创建考试场次序列化器"""
    student_ids = serializers.ListField(child=serializers.IntegerField(), required=False, write_only=True)
    float_score_enabled = serializers.BooleanField(required=False, default=False)
    float_score_min = serializers.IntegerField(required=False, default=-10)
    float_score_max = serializers.IntegerField(required=False, default=10)
    rules = serializers.ListField(child=serializers.DictField(), required=False, write_only=True,
                                   help_text='组卷规则 [{question_type, count, categories}]')
    duration_minutes = serializers.IntegerField(required=False, default=60, write_only=True,
                                                 help_text='考试时长（分钟）')
    pass_score = serializers.IntegerField(required=False, default=60, write_only=True)
    exam_scope = serializers.ListField(child=serializers.CharField(), required=False, default=list, write_only=True)
    paper = serializers.PrimaryKeyRelatedField(queryset=BusiPaper.objects.filter(is_deleted=False),
                                                required=False, allow_null=True)

    class Meta:
        model = BusiExamSession
        fields = ['id', 'name', 'paper', 'start_time', 'end_time', 'student_ids',
                  'float_score_enabled', 'float_score_min', 'float_score_max', 'rules',
                  'duration_minutes', 'pass_score', 'exam_scope']

    def validate(self, attrs):
        if attrs['start_time'] >= attrs['end_time']:
            raise serializers.ValidationError({'end_time': '结束时间必须大于开始时间'})
        return attrs

    def create(self, validated_data):
        from apps.exams.models import ExamConfig, ExamRule
        from apps.papers.models import BusiPaper as Paper
        student_ids = validated_data.pop('student_ids', [])
        float_enabled = validated_data.pop('float_score_enabled', False)
        float_min = validated_data.pop('float_score_min', -10)
        float_max = validated_data.pop('float_score_max', 10)
        rules = validated_data.pop('rules', [])
        duration = validated_data.pop('duration_minutes', 60)
        pass_s = validated_data.pop('pass_score', 60)
        paper = validated_data.pop('paper', None)
        exam_scope = validated_data.pop('exam_scope', [])

        # 未选试卷则自动创建容器卷
        if not paper:
            paper = Paper.objects.create(
                name=f'{validated_data["name"]}（动态卷）',
                duration_minutes=duration, pass_score=pass_s,
                created_by=self.context['request'].user,
            )

        exam = BusiExamSession.objects.create(paper=paper, **validated_data, created_by=self.context['request'].user)
        if student_ids:
            exam.students.set(student_ids)

        if float_enabled:
            ExamConfig.objects.create(exam_session=exam, float_score_enabled=True,
                                       float_score_min=float_min, float_score_max=float_max)

        for r in rules:
            qtype = r.get('question_type', '')
            count = int(r.get('count', 0))
            cats = r.get('categories', [])
            src = r.get('question_source', 'regular')
            dt = r.get('data_dt', '')
            if (qtype or src == 'data') and count > 0:
                ExamRule.objects.create(
                    exam_session=exam, question_type=qtype,
                    count=count, categories=cats,
                    question_source=src, data_dt=dt,
                )

        if exam_scope:
            exam.exam_scope = sorted(exam_scope)
            exam.save(update_fields=['exam_scope'])
        else:
            # 从抽题分类中提取业务范围前缀（如"资产-指标"→"资产"）
            all_cat_ids = set()
            for r in rules:
                cats = r.get('categories', [])
                if cats:
                    all_cat_ids.update(cats)
            if all_cat_ids:
                from apps.questions.models import BusiQuestionCategory
                cats = BusiQuestionCategory.objects.filter(id__in=all_cat_ids).values_list('name', flat=True)
                prefixes = set()
                for name in cats:
                    pre = name.split('-')[0].strip()
                    if pre:
                        prefixes.add(pre)
                exam.exam_scope = sorted(prefixes)
                exam.save(update_fields=['exam_scope'])

        return exam


class BusiAnswerSubmitSerializer(serializers.Serializer):
    """提交答案序列化器"""
    answers = serializers.ListField(
        child=serializers.DictField(),
        help_text='答题列表 [{paper_question_id, answer}, ...]',
    )

    def validate_answers(self, value):
        if not value:
            raise serializers.ValidationError('答案不能为空')
        return value


class BusiStudentAnswerSerializer(serializers.ModelSerializer):
    """学生答题记录序列化器"""
    question_content = serializers.CharField(source='paper_question.question.content', read_only=True)
    question_type = serializers.CharField(source='paper_question.question.question_type', read_only=True)
    question_type_display = serializers.CharField(source='paper_question.question.get_question_type_display', read_only=True)
    options = serializers.JSONField(source='paper_question.question.options', read_only=True)
    correct_answer = serializers.JSONField(source='paper_question.question.correct_answer', read_only=True)
    analysis = serializers.CharField(source='paper_question.question.analysis', read_only=True)
    score = serializers.DecimalField(source='paper_question.score', max_digits=5, decimal_places=2, read_only=True)
    order = serializers.IntegerField(source='paper_question.order', read_only=True)

    class Meta:
        model = BusiStudentAnswer
        fields = [
            'id', 'paper_question', 'question_content', 'question_type',
            'question_type_display', 'options', 'answer', 'correct_answer',
            'analysis', 'is_correct', 'score_obtained', 'score', 'order',
            'status', 'updated_at',
        ]


class BusiExamSubmissionSerializer(serializers.ModelSerializer):
    """考试提交记录序列化器"""
    student_name = serializers.CharField(source='student.username', read_only=True)
    exam_name = serializers.CharField(source='exam_session.name', read_only=True)

    class Meta:
        model = BusiExamSubmission
        fields = [
            'id', 'exam_session', 'exam_name', 'student', 'student_name',
            'status', 'start_time', 'submit_time', 'total_score', 'created_at',
        ]
