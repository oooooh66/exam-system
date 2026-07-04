"""
Excel 题目批量导入工具

支持的 Excel 表头（第一行必须是以下列名）：
- 题型: single_choice / multiple_choice / true_false / fill_blank / short_answer
- 题干: 题目内容
- 选项A / 选项B / 选项C / 选项D / 选项E / 选项F: 选择题选项（可空）
- 正确答案: 选择题存选项字母（如 A 或 A,C），判断存 对/错，填空简答存文本
- 解析: 答案解析（可空）
- 难度: easy / medium / hard（可空，默认 easy）
- 分类: 分类名称（可空）
- 分值: 数字（可空，默认 5）
"""
import logging
import traceback

import openpyxl
from django.db import transaction

from apps.questions.models import QuestionCategory, Question

logger = logging.getLogger('apps')

# 题型中文映射
QUESTION_TYPE_MAP = {
    '单选题': 'single_choice',
    '多选题': 'multiple_choice',
    '判断题': 'true_false',
    '填空题': 'fill_blank',
    '简答题': 'short_answer',
}

DIFFICULTY_MAP = {
    '简单': 'easy',
    '中等': 'medium',
    '困难': 'hard',
}


class ExcelImportResult:
    """导入结果"""

    def __init__(self):
        self.success_count = 0
        self.fail_count = 0
        self.errors = []

    def add_success(self):
        self.success_count += 1

    def add_error(self, row, error):
        self.fail_count += 1
        self.errors.append(f'第 {row} 行: {error}')


def import_questions_from_excel(file_obj, user, default_category_id=None):
    """
    从 Excel 文件批量导入题目

    Args:
        file_obj: 上传的文件对象
        user: 当前用户（作为创建人）
        default_category_id: 默认分类 ID

    Returns:
        ExcelImportResult: 导入结果
    """
    result = ExcelImportResult()
    workbook = None

    try:
        workbook = openpyxl.load_workbook(file_obj, read_only=True)
        sheet = workbook.active

        # 读取表头（第一行）
        header_row = [cell.value for cell in sheet[1]]
        header_map = {str(h).strip(): i for i, h in enumerate(header_row) if h}

        # 必需列
        required_columns = ['题型', '题干', '正确答案']
        for col in required_columns:
            if col not in header_map:
                result.add_error(0, f'缺少必需列: {col}')
                return result

        # 逐行解析和导入
        questions_to_create = []
        errors = []

        for row_idx, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
            try:
                question = _parse_excel_row(row, header_map, user, default_category_id)
                if question:
                    questions_to_create.append(question)
                    result.add_success()
            except Exception as e:
                result.add_error(row_idx, str(e))
                continue

        # 批量创建（事务保护）
        if questions_to_create:
            with transaction.atomic():
                Question.objects.bulk_create(questions_to_create)

    except Exception as e:
        logger.error(f'Excel 导入异常: {traceback.format_exc()}')
        result.add_error(0, f'文件解析失败: {str(e)}')
    finally:
        if workbook:
            workbook.close()

    return result


def _parse_excel_row(row, header_map, user, default_category_id):
    """解析单行 Excel 数据，返回 Question 对象"""
    # 读取字段
    question_type_cn = _get_cell(row, header_map, '题型')
    content = _get_cell(row, header_map, '题干')
    correct_answer = _get_cell(row, header_map, '正确答案')
    analysis = _get_cell(row, header_map, '解析') or ''
    difficulty_cn = _get_cell(row, header_map, '难度') or '简单'
    category_name = _get_cell(row, header_map, '分类')
    score = _get_cell(row, header_map, '分值') or 5

    if not all([question_type_cn, content, correct_answer]):
        raise ValueError('题型、题干、正确答案为必填项')

    # 题型转换
    question_type = QUESTION_TYPE_MAP.get(question_type_cn)
    if question_type is None:
        raise ValueError(f'无效的题型: {question_type_cn}，支持: {list(QUESTION_TYPE_MAP.keys())}')

    # 难度转换
    difficulty = DIFFICULTY_MAP.get(difficulty_cn, 'easy')

    # 分值转换
    try:
        score = int(score)
    except (ValueError, TypeError):
        score = 5

    # 解析选项（选择题）
    options = []
    if question_type in ('single_choice', 'multiple_choice'):
        option_labels = ['选项A', '选项B', '选项C', '选项D', '选项E', '选项F']
        for label in option_labels:
            if label in header_map:
                opt = _get_cell(row, header_map, label)
                if opt:
                    options.append(opt)
        if len(options) < 2:
            raise ValueError('选择题至少需要 2 个选项')

    # 正确答案格式化
    if question_type in ('single_choice', 'multiple_choice'):
        # 把 "A,C" 格式转换为 ["A", "C"]
        if question_type == 'single_choice':
            correct_answer = correct_answer.strip().upper()
        else:
            correct_answer = [x.strip().upper() for x in str(correct_answer).split(',') if x.strip()]
    elif question_type == 'true_false':
        correct_answer = correct_answer.strip()
        if correct_answer not in ('对', '错'):
            raise ValueError('判断题答案应为"对"或"错"')

    # 分类处理
    category = None
    if category_name:
        category, _ = QuestionCategory.objects.get_or_create(
            name=category_name,
            defaults={'created_by': user},
        )

    # 创建 Question 对象
    return Question(
        question_type=question_type,
        content=content,
        options=options,
        correct_answer=correct_answer,
        analysis=analysis,
        category=category,
        difficulty=difficulty,
        default_score=score,
        created_by=user,
    )


def _get_cell(row, header_map, column_name):
    """从行数据中获取单元格值"""
    col_idx = header_map.get(column_name)
    if col_idx is None:
        return None
    if col_idx >= len(row):
        return None
    value = row[col_idx]
    return str(value).strip() if value else None
