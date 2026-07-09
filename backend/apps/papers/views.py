"""试卷模块 - API 视图"""
from rest_framework import status, viewsets
from rest_framework.decorators import action

from apps.papers.models import BusiPaper, BusiPaperQuestion, BusiPaperRandomRule
from apps.questions.models import BusiQuestion
from apps.papers.serializers import (
    BusiPaperSerializer,
    BusiPaperDetailSerializer,
    BusiPaperCreateSerializer,
    BusiPaperUpdateSerializer,
    PaperBusiQuestionSerializer,
)
from apps.questions.models import BusiQuestion
from utils.permissions import IsTeacher
from utils.response import APIResponse


class BusiPaperViewSet(viewsets.ModelViewSet):
    """试卷管理 ViewSet"""
    queryset = BusiPaper.objects.filter(is_deleted=False).prefetch_related('busi_paper_questions')
    permission_classes = [IsTeacher]

    def get_serializer_class(self):
        if self.action in ('create',):
            return BusiPaperCreateSerializer
        if self.action in ('update', 'partial_update'):
            return BusiPaperUpdateSerializer
        if self.action == 'retrieve':
            return BusiPaperDetailSerializer
        return BusiPaperSerializer

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
        serializer = BusiPaperDetailSerializer(instance)
        return APIResponse.success(data=serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = BusiPaperCreateSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return APIResponse.error(code=400, message=self._first_error(serializer.errors))
        paper = serializer.save()
        return APIResponse.created(data=BusiPaperDetailSerializer(paper).data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = BusiPaperUpdateSerializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            return APIResponse.error(code=400, message=self._first_error(serializer.errors))
        paper = serializer.save()
        # 重新计算总分
        paper.update_total_score()
        return APIResponse.success(data=BusiPaperDetailSerializer(paper).data)

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
            question = BusiQuestion.objects.get(id=question_id, is_deleted=False)
        except BusiQuestion.DoesNotExist:
            return APIResponse.error(code=404, message='题目不存在')

        if PaperBusiQuestion.objects.filter(paper=paper, question=question).exists():
            return APIResponse.error(code=400, message='该题目已在试卷中')

        if not score:
            score = question.default_score

        pq = PaperBusiQuestion.objects.create(
            paper=paper, question=question, score=score, order=order,
        )
        paper.update_total_score()
        return APIResponse.success(
            data=PaperBusiQuestionSerializer(pq).data,
            message='题目添加成功',
        )

    @action(methods=['delete'], detail=True, url_path='remove-question/(?P<question_id>[^/.]+)')
    def remove_question(self, request, pk=None, question_id=None):
        """从试卷中移除一道题目"""
        paper = self.get_object()
        deleted, _ = PaperBusiQuestion.objects.filter(
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
        questions_data = request.data.get('busi_questions', [])

        for q_data in questions_data:
            pq = PaperBusiQuestion.objects.filter(
                paper=paper, question_id=q_data['question_id'],
            ).first()
            if pq:
                if 'score' in q_data:
                    pq.score = q_data['score']
                if 'order' in q_data:
                    pq.order = q_data['order']
                pq.save()

        paper.update_total_score()
        serializer = BusiPaperDetailSerializer(paper)
        return APIResponse.success(data=serializer.data, message='题目更新成功')

    @action(methods=['get', 'post'], detail=True, url_path='random-rules')
    def random_rules(self, request, pk=None):
        """
        管理试卷的随机抽题规则

        GET: 获取当前试卷的所有随机抽题规则列表
        POST: 保存/替换随机抽题规则
              请求体: {"rules": [{"category_id": 1, "question_count": 5}, ...]}
        """
        paper = self.get_object()

        if request.method == 'GET':
            rules = paper.random_rules.select_related('category').all()
            from apps.papers.serializers import BusiPaperRandomRuleSerializer
            serializer = BusiPaperRandomRuleSerializer(rules, many=True)
            return APIResponse.success(data=serializer.data)

        # POST: save/replace rules
        from apps.papers.serializers import BusiPaperRandomRuleSerializer
        rules_data = request.data.get('rules', [])
        paper.random_rules.all().delete()
        for r in rules_data:
            BusiPaperRandomRule.objects.create(
                paper=paper,
                category_id=r['category_id'],
                question_count=r['question_count'],
            )
        updated = paper.random_rules.select_related('category').all()
        return APIResponse.success(
            data=BusiPaperRandomRuleSerializer(updated, many=True).data,
            message='随机规则保存成功',
        )

    @action(methods=['post'], detail=True, url_path='random-draw')
    def random_draw(self, request, pk=None):
        """
        按配置的随机规则抽取题目并添加到试卷

        从 random-rules 读取规则，从对应的分类中随机选取相应数量的题目，
        自动排除试卷中已存在的题目，添加到试卷后重新计算总分。
        """
        from apps.papers.serializers import BusiPaperRandomDrawSerializer

        paper = self.get_object()
        serializer = BusiPaperRandomDrawSerializer(data=request.data)
        if not serializer.is_valid():
            return APIResponse.error(code=400, message=self._first_error(serializer.errors))

        rules = serializer.validated_data['rules']
        added_count = 0
        skipped_count = 0

        for rule in rules:
            category_id = rule['category_id']
            count = rule['question_count']

            # 从该分类中随机取题，排除已在试卷中的
            existing_ids = paper.paper_questions.values_list('question_id', flat=True)
            candidates = BusiQuestion.objects.filter(
                category_id=category_id, is_deleted=False,
            ).exclude(id__in=existing_ids).order_by('?')[:count]

            for question in candidates:
                BusiPaperQuestion.objects.create(
                    paper=paper,
                    question=question,
                    score=question.default_score,
                    order=paper.paper_questions.count(),
                )
                added_count += 1

            if candidates.count() < count:
                skipped_count += count - candidates.count()

        paper.update_total_score()
        return APIResponse.success(
            data={
                'added': added_count,
                'skipped': skipped_count,
                'total_score': paper.total_score,
                'paper': BusiPaperDetailSerializer(paper).data,
            },
            message=f'成功抽取 {added_count} 题' + (f'，{skipped_count} 题因数量不足跳过' if skipped_count > 0 else ''),
        )

    @action(methods=['post'], detail=True, url_path='save-random-rules')
    def save_random_rules(self, request, pk=None):
        """保存随机抽题规则（同时保存规则和触发抽题）"""
        paper = self.get_object()
        rules_data = request.data.get('rules', [])
        do_draw = request.data.get('do_draw', False)

        # 保存规则
        paper.random_rules.all().delete()
        for r in rules_data:
            BusiPaperRandomRule.objects.create(
                paper=paper,
                category_id=r['category_id'],
                question_count=r['question_count'],
            )

        # 如果需要立即抽题
        if do_draw:
            existing_ids = paper.paper_questions.values_list('question_id', flat=True)
            added = 0
            for r in rules_data:
                candidates = BusiQuestion.objects.filter(
                    category_id=r['category_id'], is_deleted=False,
                ).exclude(id__in=existing_ids).order_by('?')[:r['question_count']]
                for question in candidates:
                    BusiPaperQuestion.objects.create(
                        paper=paper, question=question,
                        score=question.default_score,
                        order=paper.paper_questions.count(),
                    )
                    existing_ids = list(existing_ids) + [question.id]
                    added += 1
            paper.update_total_score()

        return APIResponse.success(
            data=BusiPaperDetailSerializer(paper).data,
            message='规则保存成功' + ('并完成随机抽题' if do_draw else ''),
        )

    def _first_error(self, errors):
        for _, msgs in errors.items():
            return str(msgs[0]) if isinstance(msgs, list) else str(msgs)
        return '参数错误'
