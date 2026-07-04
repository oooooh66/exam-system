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

from apps.questions.models import QuestionCategory, Question
from apps.questions.serializers import (
    QuestionCategorySerializer,
    QuestionSerializer,
    QuestionListSerializer,
    QuestionImportSerializer,
)
from utils.excel_importer import import_questions_from_excel
from utils.permissions import IsAdmin, IsTeacher
from utils.response import APIResponse


class QuestionCategoryViewSet(viewsets.ModelViewSet):
    """
    题目分类管理 ViewSet

    教师和管理员可以管理分类，学生只读。
    """
    queryset = QuestionCategory.objects.filter(is_deleted=False)
    serializer_class = QuestionCategorySerializer
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


class QuestionFilter(django_filters.FilterSet):
    """题目过滤器，支持多选（逗号分隔的多个值）"""
    question_type = django_filters.CharFilter(method='filter_question_type')
    difficulty = django_filters.CharFilter(method='filter_difficulty')
    category = django_filters.CharFilter(method='filter_category')

    class Meta:
        model = Question
        fields = ['question_type', 'difficulty', 'category']

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


class QuestionViewSet(viewsets.ModelViewSet):
    """
    题目管理 ViewSet

    教师和管理员可以管理题目（增删改查 + 导入），学生只读列表。
    """
    queryset = Question.objects.filter(is_deleted=False).select_related('category')
    permission_classes = [IsTeacher]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = QuestionFilter
    search_fields = ['content']
    ordering_fields = ['id', 'default_score', 'created_at', 'difficulty']

    def get_serializer_class(self):
        """根据 action 选择不同的序列化器"""
        if self.action == 'list':
            return QuestionListSerializer
        return QuestionSerializer

    def get_permissions(self):
        """GET 请求允许所有人查看，其他操作需要教师权限"""
        if self.action in ('list', 'retrieve', 'import_questions'):
            return []  # retrieve 需要看详情时也要权限？按需求教师/管理员
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
        serializer = QuestionSerializer(instance)
        return APIResponse.success(data=serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = QuestionSerializer(data=request.data)
        if not serializer.is_valid():
            return APIResponse.error(code=400, message=self._first_error(serializer.errors))
        self.perform_create(serializer)
        return APIResponse.created(data=QuestionSerializer(serializer.instance).data)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = QuestionSerializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            return APIResponse.error(code=400, message=self._first_error(serializer.errors))
        serializer.save()
        return APIResponse.success(data=QuestionSerializer(serializer.instance).data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return APIResponse.success(message='题目已删除')

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
        serializer = QuestionImportSerializer(data=request.data)
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
