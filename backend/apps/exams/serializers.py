"""考试模块 - 序列化器"""
from rest_framework import serializers

from apps.exams.models import BusiExamSession, BusiStudentAnswer, BusiExamSubmission
from apps.papers.serializers import BusiPaperSerializer


class BusiExamSessionListSerializer(serializers.ModelSerializer):
    """考试场次列表序列化器"""
    paper_name = serializers.CharField(source='paper.name', read_only=True)
    duration = serializers.IntegerField(source='paper.duration_minutes', read_only=True)
    total_score = serializers.IntegerField(source='paper.total_score', read_only=True)
    status = serializers.CharField(source='computed_status', read_only=True)
    student_count = serializers.SerializerMethodField()

    class Meta:
        model = BusiExamSession
        fields = [
            'id', 'name', 'paper', 'paper_name', 'total_score',
            'duration', 'start_time', 'end_time', 'status',
            'student_count', 'created_at',
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
    student_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        write_only=True,
        help_text='指定学生 ID 列表，为空则开放所有人',
    )

    class Meta:
        model = BusiExamSession
        fields = ['id', 'name', 'paper', 'start_time', 'end_time', 'student_ids']

    def validate(self, attrs):
        if attrs['start_time'] >= attrs['end_time']:
            raise serializers.ValidationError({'end_time': '结束时间必须大于开始时间'})
        return attrs

    def create(self, validated_data):
        student_ids = validated_data.pop('student_ids', [])
        exam = BusiExamSession.objects.create(**validated_data, created_by=self.context['request'].user)
        if student_ids:
            exam.students.set(student_ids)
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
