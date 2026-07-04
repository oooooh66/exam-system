"""
评分逻辑模块

负责客观题的自动批改：
- 单选题：精确匹配
- 多选题：选项集合匹配（全对得满分）
- 判断题：精确匹配
- 填空题/简答题：标记为待批改（is_correct=None）
"""
import logging
from django.utils import timezone

logger = logging.getLogger('apps')


def auto_grade_question(student_answer):
    """
    自动批改一道客观题

    根据题目的 question_type 和 correct_answer 判断学生答案是否正确。

    Args:
        student_answer: StudentAnswer 对象

    Returns:
        tuple: (is_correct, score_obtained)
        - is_correct: True/False/None（None 为主观题需人工批改）
        - score_obtained: 得分
    """
    question = student_answer.paper_question.question
    correct_answer = question.correct_answer
    student_ans = student_answer.answer

    # 没有作答
    if student_ans is None:
        return False, 0

    quest_type = question.question_type
    max_score = student_answer.paper_question.score

    try:
        if quest_type == 'single_choice':
            # 单选题：字符串精确匹配
            is_correct = str(student_ans).strip().upper() == str(correct_answer).strip().upper()
            return is_correct, max_score if is_correct else 0

        elif quest_type == 'multiple_choice':
            # 多选题：选项集合匹配
            if isinstance(student_ans, str):
                student_set = set(x.strip().upper() for x in student_ans.split(','))
            else:
                student_set = set(str(x).strip().upper() for x in student_ans)
            correct_set = set(str(x).strip().upper() for x in correct_answer)
            is_correct = student_set == correct_set
            return is_correct, max_score if is_correct else 0

        elif quest_type == 'true_false':
            # 判断题：精确匹配
            is_correct = str(student_ans).strip() == str(correct_answer).strip()
            return is_correct, max_score if is_correct else 0

        elif quest_type in ('fill_blank', 'short_answer'):
            # 主观题：标记为待批改
            return None, None

        return False, 0

    except Exception as e:
        logger.error(f'自动批改异常: {e}')
        return False, 0


def grade_exam_submission(submission):
    """
    批改整场考试的所有答题记录

    Args:
        submission: ExamSubmission 对象

    Returns:
        int: 总分
    """
    answers = submission.exam_session.student_answers.filter(
        student=submission.student,
        status='submitted',
    )

    total_score = 0
    for answer in answers:
        if answer.is_correct is None:  # 还未批改
            is_correct, score = auto_grade_question(answer)
            answer.is_correct = is_correct
            answer.score_obtained = score
            if is_correct is not None:
                answer.status = 'graded'
            answer.save(update_fields=['is_correct', 'score_obtained', 'status'])

        if answer.score_obtained:
            total_score += answer.score_obtained

    # 更新提交记录的总分
    submission.total_score = total_score
    submission.save(update_fields=['total_score', 'updated_at'])

    return total_score
