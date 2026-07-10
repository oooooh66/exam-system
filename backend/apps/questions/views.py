"""
题库模块 - API 视图

提供以下接口：
- QuestionCategory CRUD: /api/question-categories/
- Question CRUD:      /api/questions/
- Question 批量导入:   POST /api/questions/import/
"""
import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.parsers import MultiPartParser

from apps.questions.models import BusiQuestionCategory, BusiQuestion
from apps.questions.serializers import (
    BusiQuestionCategorySerializer,
    BusiQuestionSerializer,
    BusiQuestionListSerializer,
    BusiQuestionImportSerializer,
)
from utils.excel_importer import import_questions_from_excel
from utils.permissions import IsAdmin, IsTeacher
from utils.response import APIResponse


class BusiQuestionCategoryViewSet(viewsets.ModelViewSet):
    """
    题目分类管理 ViewSet

    教师和管理员可以管理分类，学生只读。
    """
    queryset = BusiQuestionCategory.objects.filter(is_deleted=False)
    serializer_class = BusiQuestionCategorySerializer
    permission_classes = [IsTeacher]
    search_fields = ['name']
    ordering_fields = ['name', 'created_at']

    def get_permissions(self):
        """GET 请求允许学生查看，其他操作需要教师权限"""
        if self.action in ('list', 'retrieve'):
            return []  # 允许所有人查看分类
        return [IsTeacher()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_destroy(self, instance):
        """软删除分类"""
        instance.is_deleted = True
        instance.save(update_fields=['is_deleted', 'updated_at'])

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return APIResponse.success(data=response.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return APIResponse.success(data=serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return APIResponse.error(code=400, message=self._first_error(serializer.errors))
        self.perform_create(serializer)
        return APIResponse.created(data=serializer.data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            return APIResponse.error(code=400, message=self._first_error(serializer.errors))
        serializer.save()
        return APIResponse.success(data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return APIResponse.success(message='分类已删除')

    def _first_error(self, errors):
        for _, msgs in errors.items():
            return str(msgs[0]) if isinstance(msgs, list) else str(msgs)
        return '参数错误'


class BusiQuestionFilter(django_filters.FilterSet):
    """题目过滤器，支持多选（逗号分隔的多个值）"""
    question_type = django_filters.CharFilter(method='filter_question_type')
    difficulty = django_filters.CharFilter(method='filter_difficulty')
    category = django_filters.CharFilter(method='filter_category')
    org_id = django_filters.CharFilter(method='filter_org_id')

    class Meta:
        model = BusiQuestion
        fields = ['question_type', 'difficulty', 'category', 'org_id']

    def _split_values(self, value):
        """将逗号分隔的字符串拆分为列表"""
        if not value:
            return []
        return [v.strip() for v in value.split(',') if v.strip()]

    def filter_question_type(self, queryset, name, value):
        values = self._split_values(value)
        if values:
            return queryset.filter(question_type__in=values)
        return queryset

    def filter_difficulty(self, queryset, name, value):
        values = self._split_values(value)
        if values:
            return queryset.filter(difficulty__in=values)
        return queryset

    def filter_category(self, queryset, name, value):
        """分类多选：逗号分隔的ID列表"""
        values = self._split_values(value)
        if values:
            # 尝试转为整数 ID 列表查询
            try:
                ids = [int(v) for v in values]
                return queryset.filter(category_id__in=ids)
            except ValueError:
                pass
        return queryset

    def filter_org_id(self, queryset, name, value):
        """机构筛选：按org_id精确匹配"""
        if value:
            return queryset.filter(org_id=value)
        return queryset


class BusiQuestionViewSet(viewsets.ModelViewSet):
    """
    题目管理 ViewSet

    教师和管理员可以管理题目（增删改查 + 导入），学生只读列表。
    """
    queryset = BusiQuestion.objects.filter(is_deleted=False).select_related('category')
    permission_classes = [IsTeacher]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BusiQuestionFilter
    search_fields = ['content']
    ordering_fields = ['id', 'default_score', 'created_at', 'difficulty']

    def get_serializer_class(self):
        """根据 action 选择不同的序列化器"""
        if self.action == 'list':
            return BusiQuestionListSerializer
        return BusiQuestionSerializer

    def get_permissions(self):
        """GET 请求允许所有人查看，其他操作需要教师权限"""
        if self.action in ('list', 'retrieve', 'import_questions', 'orgs'):
            return []
        return [IsTeacher()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_destroy(self, instance):
        """软删除题目"""
        instance.is_deleted = True
        instance.save(update_fields=['is_deleted', 'updated_at'])

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return APIResponse.success(data=response.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = BusiQuestionSerializer(instance)
        return APIResponse.success(data=serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = BusiQuestionSerializer(data=request.data)
        if not serializer.is_valid():
            return APIResponse.error(code=400, message=self._first_error(serializer.errors))
        self.perform_create(serializer)
        return APIResponse.created(data=BusiQuestionSerializer(serializer.instance).data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = BusiQuestionSerializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            return APIResponse.error(code=400, message=self._first_error(serializer.errors))
        serializer.save()
        return APIResponse.success(data=BusiQuestionSerializer(serializer.instance).data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return APIResponse.success(message='题目已删除')

    @action(
        methods=['get'],
        detail=False,
        url_path='orgs',
    )
    def orgs(self, request):
        """
        获取所有不重复的机构列表（用于前端下拉筛选）

        GET /api/questions/orgs/
        返回: [{org_id: "ORG001", org_nm: "机构A"}, ...]
        """
        qs = BusiQuestion.objects.filter(is_deleted=False).exclude(
            org_nm=''
        ).values('org_id', 'org_nm').distinct().order_by('org_id')
        return APIResponse.success(data=list(qs))

    @action(
        methods=['post'],
        detail=False,
        url_path='random-draw',
    )
    def random_draw(self, request):
        """
        独立随机抽题（不绑定试卷，返回题目列表）

        POST /api/questions/random-draw/
        Body: {"rules": [{"category_id": 1, "counts": {"single_choice": 3, ...}}]}
        """
        from apps.papers.serializers import BusiPaperRandomDrawSerializer

        serializer = BusiPaperRandomDrawSerializer(data=request.data)
        if not serializer.is_valid():
            return APIResponse.error(code=400, message=self._first_error(serializer.errors))

        rules = serializer.validated_data['rules']
        import random
        added = 0
        skipped = 0
        picked_ids = set()
        all_questions = []

        for rule in rules:
            category_id = rule['category_id']
            counts = rule.get('counts', {})

            for qtype, need in counts.items():
                if need <= 0:
                    continue

                pool = list(BusiQuestion.objects.filter(
                    category_id=category_id,
                    question_type=qtype,
                    is_deleted=False,
                ).exclude(id__in=picked_ids).values_list('id', flat=True))

                random.shuffle(pool)
                batch = []
                for qid in pool:
                    if len(batch) >= need:
                        break
                    if qid not in picked_ids:
                        batch.append(qid)
                        picked_ids.add(qid)

                if len(batch) < need:
                    skipped += need - len(batch)
                added += len(batch)
                all_questions.extend(batch)

        questions = list(
            BusiQuestion.objects.filter(id__in=all_questions).select_related('category')
            .order_by('question_type', 'id')
        )
        return APIResponse.success(data={
            'added': added,
            'skipped': skipped,
            'questions': BusiQuestionListSerializer(questions, many=True).data,
        })

    @action(
        methods=['post'],
        detail=False,
        url_path='import',
        parser_classes=[MultiPartParser],
        permission_classes=[IsTeacher],
    )
    def import_questions(self, request):
        """
        批量导入题目（Excel 格式）

        POST /api/questions/import/
        表单字段：file（Excel 文件），category_id（可选）
        """
        serializer = BusiQuestionImportSerializer(data=request.data)
        if not serializer.is_valid():
            return APIResponse.error(code=400, message=self._first_error(serializer.errors))

        file_obj = serializer.validated_data['file']
        category_id = serializer.validated_data.get('category_id')

        result = import_questions_from_excel(
            file_obj=file_obj,
            user=request.user,
            default_category_id=category_id,
        )

        if result.fail_count > 0 and result.success_count == 0:
            return APIResponse.error(
                code=400,
                message=f'导入失败，共 {result.fail_count} 个错误',
                data={'errors': result.errors},
            )

        return APIResponse.success(
            data={
                'success_count': result.success_count,
                'fail_count': result.fail_count,
                'errors': result.errors,
            },
            message=f'导入完成，成功 {result.success_count} 条，失败 {result.fail_count} 条',
        )

    def _first_error(self, errors):
        for _, msgs in errors.items():
            return str(msgs[0]) if isinstance(msgs, list) else str(msgs)
        return '参数错误'
