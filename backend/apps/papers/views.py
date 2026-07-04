"""试卷模块 - API 视图"""
from rest_framework import status, viewsets
from rest_framework.decorators import action

from apps.papers.models import Paper, PaperQuestion
from apps.papers.serializers import (
    PaperSerializer,
    PaperDetailSerializer,
    PaperCreateSerializer,
    PaperUpdateSerializer,
    PaperQuestionSerializer,
)
from apps.questions.models import Question
from utils.permissions import IsTeacher
from utils.response import APIResponse


class PaperViewSet(viewsets.ModelViewSet):
    """试卷管理 ViewSet"""
    queryset = Paper.objects.filter(is_deleted=False).prefetch_related('paper_questions')
    permission_classes = [IsTeacher]

    def get_serializer_class(self):
        if self.action in ('create',):
            return PaperCreateSerializer
        if self.action in ('update', 'partial_update'):
            return PaperUpdateSerializer
        if self.action == 'retrieve':
            return PaperDetailSerializer
        return PaperSerializer

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return []  # 所有人可查看试卷
        return [IsTeacher()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save(update_fields=['is_deleted', 'updated_at'])

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return APIResponse.success(data=response.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = PaperDetailSerializer(instance)
        return APIResponse.success(data=serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = PaperCreateSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return APIResponse.error(code=400, message=self._first_error(serializer.errors))
        paper = serializer.save()
        return APIResponse.created(data=PaperDetailSerializer(paper).data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = PaperUpdateSerializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            return APIResponse.error(code=400, message=self._first_error(serializer.errors))
        paper = serializer.save()
        # 重新计算总分
        paper.update_total_score()
        return APIResponse.success(data=PaperDetailSerializer(paper).data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return APIResponse.success(message='试卷已删除')

    @action(methods=['post'], detail=True, url_path='add-question')
    def add_question(self, request, pk=None):
        """向试卷中添加一道题目"""
        paper = self.get_object()
        question_id = request.data.get('question_id')
        score = request.data.get('score', 0)
        order = request.data.get('order', 0)

        if not question_id:
            return APIResponse.error(code=400, message='请提供题目 ID')

        try:
            question = Question.objects.get(id=question_id, is_deleted=False)
        except Question.DoesNotExist:
            return APIResponse.error(code=404, message='题目不存在')

        if PaperQuestion.objects.filter(paper=paper, question=question).exists():
            return APIResponse.error(code=400, message='该题目已在试卷中')

        if not score:
            score = question.default_score

        pq = PaperQuestion.objects.create(
            paper=paper, question=question, score=score, order=order,
        )
        paper.update_total_score()
        return APIResponse.success(
            data=PaperQuestionSerializer(pq).data,
            message='题目添加成功',
        )

    @action(methods=['delete'], detail=True, url_path='remove-question/(?P<question_id>[^/.]+)')
    def remove_question(self, request, pk=None, question_id=None):
        """从试卷中移除一道题目"""
        paper = self.get_object()
        deleted, _ = PaperQuestion.objects.filter(
            paper=paper, question_id=question_id,
        ).delete()
        if deleted:
            paper.update_total_score()
            return APIResponse.success(message='题目已移除')
        return APIResponse.error(code=404, message='题目不在试卷中')

    @action(methods=['post'], detail=True, url_path='update-questions')
    def update_questions(self, request, pk=None):
        """批量更新试卷题目顺序和分值"""
        paper = self.get_object()
        questions_data = request.data.get('questions', [])

        for q_data in questions_data:
            pq = PaperQuestion.objects.filter(
                paper=paper, question_id=q_data['question_id'],
            ).first()
            if pq:
                if 'score' in q_data:
                    pq.score = q_data['score']
                if 'order' in q_data:
                    pq.order = q_data['order']
                pq.save()

        paper.update_total_score()
        serializer = PaperDetailSerializer(paper)
        return APIResponse.success(data=serializer.data, message='题目更新成功')

    def _first_error(self, errors):
        for _, msgs in errors.items():
            return str(msgs[0]) if isinstance(msgs, list) else str(msgs)
        return '参数错误'
