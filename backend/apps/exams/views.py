"""
考试模块 - API 视图

提供以下接口：
- 教师/管理员：发布考试、查看考试列表
- 学生：查看可参加的考试、开始答题、提交答案、暂存答案
"""
from django.utils import timezone
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.exams.models import BusiExamSession, BusiStudentAnswer, BusiExamSubmission
from apps.exams.serializers import (
    BusiExamSessionListSerializer,
    BusiExamSessionDetailSerializer,
    BusiExamSessionCreateSerializer,
    BusiAnswerSubmitSerializer,
    BusiStudentAnswerSerializer,
    BusiExamSubmissionSerializer,
)
from apps.exams.scoring import auto_grade_question, grade_exam_submission
from apps.papers.models import BusiPaperQuestion
from utils.permissions import IsTeacher, IsAdmin
from utils.response import APIResponse


class BusiExamSessionViewSet(viewsets.ModelViewSet):
    """考试场次管理 ViewSet"""
    queryset = BusiExamSession.objects.filter(is_deleted=False).select_related('paper')
    permission_classes = [IsTeacher]

    def get_serializer_class(self):
        if self.action == 'create':
            return BusiExamSessionCreateSerializer
        if self.action in ('list',):
            return BusiExamSessionListSerializer
        return BusiExamSessionDetailSerializer

    def get_permissions(self):
        """学生也可以查看可用考试列表"""
        if self.action in ('list', 'retrieve', 'start_exam', 'save_answer',
                           'submit_exam', 'my_exams', 'my_result'):
            return []
        return [IsTeacher()]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save(update_fields=['is_deleted', 'updated_at'])

    def get_queryset(self):
        qs = super().get_queryset()
        # 学生只看分配给自己的或开放的考试
        if self.request.user.is_student:
            qs = qs.filter(
                models.Q(students__isnull=True) | models.Q(students=self.request.user)
            ).distinct()
        return qs

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return APIResponse.success(data=response.data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = BusiExamSessionDetailSerializer(instance, context={'request': request})
        return APIResponse.success(data=serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = BusiExamSessionCreateSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return APIResponse.error(code=400, message=self._first_error(serializer.errors))
        exam = serializer.save()
        return APIResponse.created(
            data=BusiExamSessionListSerializer(exam).data,
            message='考试发布成功',
        )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return APIResponse.success(message='考试已删除')

    @action(methods=['post'], detail=True, url_path='start')
    def start_exam(self, request, pk=None):
        """学生开始答题"""
        exam = self.get_object()

        # 检查考试状态
        now = timezone.now()
        if now < exam.start_time:
            return APIResponse.error(code=400, message='考试尚未开始')
        if now > exam.end_time:
            return APIResponse.error(code=400, message='考试已结束')

        # 检查是否已提交
        submission, created = BusiExamSubmission.objects.get_or_create(
            exam_session=exam,
            student=request.user,
            defaults={'status': 'in_progress', 'start_time': now},
        )

        if submission.status == 'submitted':
            return APIResponse.error(code=400, message='您已提交过本场考试')

        if created:
            # 首次进入：初始化答题记录
            paper_questions = exam.paper.paper_questions.all()
            for pq in paper_questions:
                BusiStudentAnswer.objects.get_or_create(
                    exam_session=exam,
                    student=request.user,
                    paper_question=pq,
                    defaults={'answer': None, 'status': 'draft'},
                )

        # 返回试卷完整信息
        paper_data = {
            'exam_id': exam.id,
            'exam_name': exam.name,
            'paper_id': exam.paper.id,
            'paper_name': exam.paper.name,
            'duration_minutes': exam.paper.duration_minutes,
            'total_score': exam.paper.total_score,
            'start_time': exam.start_time,
            'end_time': exam.end_time,
            'submission_start_time': submission.start_time,
            'questions': [],
        }

        for pq in exam.paper.paper_questions.all().select_related('question'):
            answer = BusiStudentAnswer.objects.filter(
                exam_session=exam, student=request.user, paper_question=pq,
            ).first()
            paper_data['questions'].append({
                'paper_question_id': pq.id,
                'order': pq.order,
                'score': pq.score,
                'question_type': pq.question.question_type,
                'content': pq.question.content,
                'options': pq.question.options,
                'saved_answer': answer.answer if answer else None,
                'status': answer.status if answer else 'draft',
            })

        return APIResponse.success(data=paper_data, message='考试开始')

    @action(methods=['post'], detail=True, url_path='save')
    def save_answer(self, request, pk=None):
        """暂存答案（不提交）"""
        exam = self.get_object()
        now = timezone.now()

        if now > exam.end_time:
            return APIResponse.error(code=400, message='考试已结束，无法保存')

        paper_question_id = request.data.get('paper_question_id')
        answer_data = request.data.get('answer')

        if not paper_question_id:
            return APIResponse.error(code=400, message='缺少题目 ID')

        try:
            answer = BusiStudentAnswer.objects.get(
                exam_session=exam,
                student=request.user,
                paper_question_id=paper_question_id,
            )
        except BusiStudentAnswer.DoesNotExist:
            return APIResponse.error(code=404, message='无效的题目')

        answer.answer = answer_data
        answer.status = 'draft'
        answer.save(update_fields=['answer', 'status', 'updated_at'])

        return APIResponse.success(message='答案已保存')

    @action(methods=['post'], detail=True, url_path='submit')
    def submit_exam(self, request, pk=None):
        """学生提交考试"""
        exam = self.get_object()
        now = timezone.now()

        if now > exam.end_time:
            # 超时自动提交
            pass
        elif now < exam.start_time:
            return APIResponse.error(code=400, message='考试尚未开始')

        # 获取提交记录
        try:
            submission = BusiExamSubmission.objects.get(
                exam_session=exam,
                student=request.user,
            )
        except BusiExamSubmission.DoesNotExist:
            return APIResponse.error(code=400, message='请先开始考试')

        if submission.status == 'submitted':
            return APIResponse.error(code=400, message='您已提交过本场考试')

        # 批量更新答案状态
        with transaction.atomic():
            BusiStudentAnswer.objects.filter(
                exam_session=exam,
                student=request.user,
            ).update(status='submitted')

            # 自动批改客观题并计算总分
            grade_exam_submission(submission)

            submission.status = 'submitted'
            submission.submit_time = now
            submission.save()

        return APIResponse.success(
            data={
                'total_score': submission.total_score,
                'submit_time': submission.submit_time,
            },
            message='提交成功',
        )

    @action(methods=['get'], detail=False, url_path='my-exams')
    def my_exams(self, request):
        """学生查看我的考试列表"""
        if not request.user.is_student:
            qs = self.get_queryset().filter(created_by=request.user)
        else:
            qs = self.get_queryset().filter(
                models.Q(students__isnull=True) | models.Q(students=request.user)
            ).distinct()

        serializer = BusiExamSessionListSerializer(qs, many=True)
        data = serializer.data

        # 为学生附加提交状态
        if request.user.is_student:
            exam_ids = [e['id'] for e in data]
            submissions = {
                s.exam_session_id: s.status
                for s in BusiExamSubmission.objects.filter(
                    exam_session_id__in=exam_ids, student=request.user,
                )
            }
            for exam in data:
                sub_status = submissions.get(exam['id'])
                exam['submission_status'] = sub_status

        return APIResponse.success(data={'results': data, 'count': qs.count()})

    @action(methods=['get'], detail=True, url_path='my-result')
    def my_result(self, request, pk=None):
        """学生查看某场考试的成绩"""
        exam = self.get_object()
        submission = BusiExamSubmission.objects.filter(
            exam_session=exam, student=request.user,
        ).first()

        if not submission or submission.status not in ('submitted', 'auto_submitted'):
            return APIResponse.error(code=400, message='尚未提交考试')

        answers = BusiStudentAnswer.objects.filter(
            exam_session=exam, student=request.user,
        ).select_related('paper_question__question').order_by('paper_question__order')

        serializer = BusiStudentAnswerSerializer(answers, many=True)
        return APIResponse.success(data={
            'submission': BusiExamSubmissionSerializer(submission).data,
            'answers': serializer.data,
        })

    @action(methods=['get'], detail=True, url_path='grade-list')
    def grade_list(self, request, pk=None):
        """教师查看待批改列表（某场考试的所有未批改主观题）"""
        exam = self.get_object()
        ungraded = BusiStudentAnswer.objects.filter(
            exam_session=exam,
            is_correct__isnull=True,
            status='submitted',
        ).select_related('paper_question__question', 'student').order_by('student', 'paper_question__order')

        serializer = BusiStudentAnswerSerializer(ungraded, many=True)
        return APIResponse.success(data={
            'count': ungraded.count(),
            'answers': serializer.data,
        })

    @action(methods=['post'], detail=True, url_path='grade')
    def grade_answer(self, request, pk=None):
        """教师手动批改一道题"""
        answer_id = request.data.get('answer_id')
        score_obtained = request.data.get('score_obtained')

        if not answer_id or score_obtained is None:
            return APIResponse.error(code=400, message='缺少 answer_id 或 score_obtained')

        try:
            answer = BusiStudentAnswer.objects.get(
                id=answer_id, exam_session_id=pk,
            )
        except BusiStudentAnswer.DoesNotExist:
            return APIResponse.error(code=404, message='答题记录不存在')

        answer.score_obtained = score_obtained
        answer.is_correct = score_obtained > 0
        answer.status = 'graded'
        answer.save()

        # 重新计算该学生的总分
        from apps.exams.scoring import grade_exam_submission
        submission = BusiExamSubmission.objects.filter(
            exam_session_id=pk, student=answer.student,
        ).first()
        if submission:
            submission.total_score = BusiStudentAnswer.objects.filter(
                exam_session_id=pk, student=answer.student,
            ).aggregate(s=models.Sum('score_obtained'))['s'] or 0
            submission.save()

        return APIResponse.success(message='批改成功', data={
            'answer_id': answer.id,
            'score_obtained': answer.score_obtained,
        })

    def _first_error(self, errors):
        for _, msgs in errors.items():
            return str(msgs[0]) if isinstance(msgs, list) else str(msgs)
        return '参数错误'


# 需要导入 models 模块用于 Q 查询
from django.db import models
