"""
导入机构画像数据生成数据指标题（区间选项版）

用法:
    python manage.py import_data_questions C:/path/to/六枝机构画像.xlsx --data-dt=202607
"""
import math
import random
from decimal import Decimal
from django.core.management.base import BaseCommand, CommandError
from apps.questions.models import BusiQuestion, BusiQuestionCategory

LABELS = ['A', 'B', 'C', 'D']


def get_width_ratio(v: float) -> float:
    abs_v = abs(v)
    if abs_v < 100000:
        return 0.10
    return 0.06


def snap_step(correct_val: float, num_fmt: str = '3') -> float:
    """返回取整步长。fmt: 1=百分比, 2=小数, 3=整数"""
    abs_v = abs(correct_val)
    # 百分比始终用小步长
    if num_fmt == '1':
        return 0.01
    # 整数数据最小步长=1
    if num_fmt == '3':
        min_step = 1
    else:
        min_step = 0.01

    if abs_v < 1000000:
        step = max(min_step, 100)
        if abs_v < step:
            if num_fmt == '3':
                if abs_v < 10:
                    step = 1
                elif abs_v < 100:
                    step = 10
            else:
                step = min_step
    else:
        step = 1000000
    return step


def snap_value(val: float, step: float, direction: str) -> float:
    """direction='down' 向下取整, 'up' 向上取整；结果 round 消除浮点误差"""
    result = (math.floor(val / step) if direction == 'down' else math.ceil(val / step)) * step
    if step >= 1:
        return round(result, 0)
    decimals = len(str(step).split('.')[-1])
    return round(result, decimals)


def snap_interval(low: float, high: float, correct_val: float, step: float) -> tuple:
    """将区间边界取整到友好数值"""
    lo = snap_value(low, step, 'down')
    hi = snap_value(high, step, 'up')
    if hi - lo < step * 2:
        hi = lo + step * 2
    if correct_val < lo:
        lo = snap_value(correct_val, step, 'down')
    if correct_val > hi:
        hi = snap_value(correct_val, step, 'up')
    return lo, hi


def generate_interval_options(correct_val: float, num_fmt: str) -> tuple:
    v = float(correct_val)
    step = snap_step(v, num_fmt)
    width = abs(v) * get_width_ratio(v)
    if width < step * 2:
        width = step * 2

    gap = width * 1.5
    pick = random.choice(['left2', 'left1'])
    if pick == 'left2':
        centers = [v - 2 * gap, v - gap, v, v + gap]
    else:
        centers = [v - gap, v, v + gap, v + 2 * gap]

    intervals = []
    for c in centers:
        lo, hi = snap_interval(c - width / 2, c + width / 2, v, step)
        intervals.append([lo, hi])

    correct_idx = 2 if pick == 'left2' else 1
    if not (intervals[correct_idx][0] <= v <= intervals[correct_idx][1]):
        lo, hi = snap_interval(v - width / 2, v + width / 2, v, step)
        intervals[correct_idx] = [lo, hi]

    in_range = [1 if lo <= v <= hi else 0 for lo, hi in intervals]
    if sum(in_range) != 1:
        lo, hi = snap_interval(v - width / 2, v + width / 2, v, step)
        intervals[correct_idx] = [lo, hi]

    intervals.sort(key=lambda x: x[0])
    # 排序后重新定位正确答案在哪个区间
    correct_idx = next(i for i, (lo, hi) in enumerate(intervals) if lo <= v <= hi)
    decimals = len(str(step).split('.')[-1])
    for i in range(1, 4):
        if intervals[i][0] <= intervals[i - 1][1]:
            intervals[i][0] = round(intervals[i - 1][1] + step, decimals)
            intervals[i][1] = max(intervals[i][1], round(intervals[i][0] + step * 2, decimals))

    for i in range(4):
        intervals[i][0] = round(intervals[i][0], decimals)
        intervals[i][1] = round(intervals[i][1], decimals)
        if v >= 0 and intervals[i][0] < 0:
            intervals[i][0] = 0

    # 去重：确保区间唯一
    seen = set()
    for i in range(4):
        key = (intervals[i][0], intervals[i][1])
        if key in seen:
            intervals[i][0] = int(intervals[i][0] + step * 2)
            intervals[i][1] = int(intervals[i][0] + step * 2)
        seen.add(key)

    indices = list(range(4))
    random.shuffle(indices)
    shuffled = [intervals[i] for i in indices]
    correct_new_idx = indices.index(correct_idx)
    correct_letter = LABELS[correct_new_idx]

    options = {
        'A': shuffled[0], 'B': shuffled[1], 'C': shuffled[2], 'D': shuffled[3],
    }
    return options, correct_letter


def classify_table(table_name: str) -> str:
    """根据表名判断业务分类，返回 '资产-指标' 或 '负债-指标'"""
    liability_kw = {'存款'}
    asset_kw = {'贷款', '余额', '利率', '担保', '期限', '不良', '资产', '授信', '用信', '开卡', 'D类'}
    for kw in liability_kw:
        if kw in table_name:
            return '负债-指标'
    for kw in asset_kw:
        if kw in table_name:
            return '资产-指标'
    return '资产-指标'


def fmt_num(n: float, num_fmt: str = '') -> str:
    """数值格式化：百分比加%，百万级加万，亿级加亿"""
    n = float(n)
    if num_fmt == '1':
        v = n * 100
        if v == int(v):
            return f'{int(v)}%'
        s = ('%.2f' % v).rstrip('0').rstrip('.')
        return f'{s}%'
    if abs(n) >= 100000000:
        v = n / 100000000
        s = ('%.2f' % v).rstrip('0').rstrip('.')
        return f'{s}亿'
    if abs(n) >= 1000000:
        v = int(round(n / 10000))
        return f'{v}万'
    if n == int(n):
        return str(int(n))
    s = ('%f' % n).rstrip('0').rstrip('.')
    return s
    if n == int(n):
        return str(int(n))
    s = ('%f' % n).rstrip('0').rstrip('.')
    return s


def build_stem(table_name, label_type, busi_type, col_nm):
    parts = [table_name, label_type, busi_type, col_nm]
    seen = set()
    unique = []
    for p in parts:
        p = str(p).strip()
        if p and p not in seen:
            seen.add(p)
            unique.append(p)
    if len(unique) >= 2:
        stem = unique[0] + '中，' + '的'.join(unique[1:]) + '落在哪个区间？'
    else:
        stem = unique[0] + '落在哪个区间？'
    return stem


class Command(BaseCommand):
    help = '从机构画像 Excel 导入数据指标题（区间选项）'

    def add_arguments(self, parser):
        parser.add_argument('file', help='Excel 文件路径')
        parser.add_argument('--data-dt', required=True, help='数据日期，如 202607')

    def handle(self, *args, **options):
        filepath = options['file']
        data_dt = options['data_dt']
        try:
            import openpyxl
        except ImportError:
            raise CommandError('请安装 openpyxl: pip install openpyxl')

        wb = openpyxl.load_workbook(filepath, read_only=True)
        ws = wb.active

        COL_ORG_ID, COL_TABLE, COL_LABEL, COL_BUSI, COL_COLNM, COL_FMT, COL_EXPR = 0, 6, 8, 10, 12, 14, 15

        def _parse_expr(raw, num_fmt: str) -> float:
            """解析 expr_0 字段：去除万/% 单位，转回原始数值"""
            s = str(raw).strip().replace(',', '').replace('，', '')
            if not s:
                return 0.0
            if num_fmt == '3' and '万' in s:       # 万元 → 原值 * 10000
                return float(s.replace('万', '')) * 10000
            if num_fmt == '1' and '%' in s:          # 百分比 → 除以 100
                return float(s.replace('%', '')) / 100
            return float(s)

        raw = []
        for row in ws.iter_rows(min_row=2, values_only=True):
            col_nm = str(row[COL_COLNM]).strip() if row[COL_COLNM] else ''
            fmt = str(row[COL_FMT]).strip() if row[COL_FMT] is not None else '2'
            expr_raw = row[COL_EXPR]
            if expr_raw is None:
                continue
            org = str(row[COL_ORG_ID]).strip()
            org_nm = str(row[1]).strip() if row[1] else ''
            raw.append({
                'org': org, 'org_nm': org_nm,
                'table': str(row[COL_TABLE]).strip(),
                'label': str(row[COL_LABEL]).strip(),
                'busi': str(row[COL_BUSI]).strip(),
                'col': col_nm,
                'fmt': fmt,
                'expr': _parse_expr(expr_raw, fmt),
                'expr_raw': str(expr_raw).strip(),
            })
        wb.close()

        # 缓存分类对象
        cat_cache = {}
        def get_category(table_name):
            cat_name = classify_table(table_name)
            if cat_name not in cat_cache:
                cat_cache[cat_name], _ = BusiQuestionCategory.objects.get_or_create(
                    name=cat_name,
                    defaults={'created_by': None},
                )
            return cat_cache[cat_name]

        # fmt 映射：新模板 1=百分比,2=普通数值,3=万元 → 生成器需要的格式
        def _map_fmt(fmt: str) -> str:
            if fmt == '1':
                return '1'   # 百分比，step=0.01
            return '3'       # 普通数值/万元用整数精度

        created = updated = 0
        for r in raw:
            val = float(r['expr'])
            stem = build_stem(r['table'], r['label'], r['busi'], r['col'])
            options, correct_letter = generate_interval_options(val, _map_fmt(r['fmt']))
            category = get_category(r['table'])

            options_display = [
                f'[{fmt_num(options["A"][0], r["fmt"])}, {fmt_num(options["A"][1], r["fmt"])}]',
                f'[{fmt_num(options["B"][0], r["fmt"])}, {fmt_num(options["B"][1], r["fmt"])}]',
                f'[{fmt_num(options["C"][0], r["fmt"])}, {fmt_num(options["C"][1], r["fmt"])}]',
                f'[{fmt_num(options["D"][0], r["fmt"])}, {fmt_num(options["D"][1], r["fmt"])}]',
            ]
            q, is_new = BusiQuestion.objects.update_or_create(
                question_type='single_choice', content=stem, org_id=r['org'],
                defaults={
                    'options': options_display,
                    'correct_answer': correct_letter,
                    'default_score': 1,
                    'org_nm': r.get('org_nm', ''),
                    'category': category,
                    'data_dt': data_dt,
                    'analysis': r['expr_raw'],
                },
            )
            if is_new:
                created += 1
            else:
                updated += 1

        self.stdout.write(self.style.SUCCESS(
            f'导入完成：新增 {created} 题，更新 {updated} 题，共 {created + updated} 题'
        ))
