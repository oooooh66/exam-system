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


def friendly_step(v: float, num_fmt: str = '2'):
    """友好取整步长：保留 3 位有效数字；普通数值(num_fmt=2)强制整数步长"""
    abs_v = abs(v)
    if abs_v < 1e-9:
        return 1
    exp = math.floor(math.log10(abs_v))
    step = 10 ** (exp - 2)
    if num_fmt == '2':
        step = max(step, 1)
    return step


def snap_value(val: float, step: float, direction: str) -> float:
    """direction='down' 向下取整, 'up' 向上取整；结果 round 消除浮点误差"""
    result = (math.floor(val / step) if direction == 'down' else math.ceil(val / step)) * step
    if step >= 1:
        return round(result, 0)
    decimals = len(str(step).split('.')[-1])
    return round(result, decimals)


def snap_interval(low: float, high: float, step: float) -> tuple:
    """将区间边界取整到友好数值"""
    lo = snap_value(low, step, 'down')
    hi = snap_value(high, step, 'up')
    if hi - lo < step * 2:
        hi = lo + step * 2
    return lo, hi


def generate_interval_options(correct_val: float, num_fmt: str = '2', float_ratio=None) -> tuple:
    v = float(correct_val)
    step = friendly_step(v, num_fmt)
    decimals = 0 if step >= 1 else len(str(step).split('.')[-1])

    if float_ratio:
        # 浮动区间模式：宽度 = 正确值 × 2 × 浮动比例
        width = abs(v) * 2 * float_ratio
    else:
        # 固定步长模式：宽度 = 正确值 × 比例（10% 或 6%）
        width = abs(v) * get_width_ratio(v)
    if width < step * 2:
        width = step * 2

    gap = width * 1.5
    pick = random.choice(['left2', 'left1'])
    if v >= 0 and (v - 2 * gap - width / 2) < 0:
        # 正确值太靠左，4 个区间全部向右排，避免出现负区间
        centers = [v, v + gap, v + 2 * gap, v + 3 * gap]
        correct_pos = 0
    elif pick == 'left2':
        centers = [v - 2 * gap, v - gap, v, v + gap]
        correct_pos = 2
    else:
        centers = [v - gap, v, v + gap, v + 2 * gap]
        correct_pos = 1

    intervals = []
    for i, c in enumerate(centers):
        lo = c - width / 2
        hi = c + width / 2
        if i == correct_pos:
            lo = min(lo, v)
            hi = max(hi, v)
        lo, hi = snap_interval(lo, hi, step)
        if i == correct_pos:
            # 取整后仍确保正确值在区间内
            if v < lo:
                lo = snap_value(v, step, 'down')
            if v > hi:
                hi = snap_value(v, step, 'up')
        intervals.append([round(lo, decimals), round(hi, decimals)])

    # 排序
    intervals.sort(key=lambda x: x[0])

    # 重叠修复：保证区间不重叠且顺序正确
    for i in range(1, 4):
        if intervals[i][0] <= intervals[i - 1][1]:
            intervals[i][0] = round(intervals[i - 1][1] + step, decimals)
            intervals[i][1] = max(intervals[i][1], round(intervals[i][0] + step * 2, decimals))

    # 非负修复
    for i in range(4):
        if v >= 0 and intervals[i][0] < 0:
            intervals[i][0] = 0

    # 去重：确保区间唯一
    seen = set()
    for i in range(4):
        key = (intervals[i][0], intervals[i][1])
        if key in seen:
            intervals[i][0] = round(intervals[i][0] + step * 2, decimals)
            intervals[i][1] = round(intervals[i][0] + step * 2, decimals)
        seen.add(key)

    # 定位正确值所在区间（排序/去重后位置可能变化）
    correct_idx = 0
    for i, (lo, hi) in enumerate(intervals):
        if lo <= v <= hi:
            correct_idx = i
            break

    # 打乱
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


def _fmt_decimal(n: float) -> str:
    """数值转字符串，去除多余尾零"""
    if n == int(n):
        return str(int(n))
    return ('%f' % n).rstrip('0').rstrip('.')


def fmt_num(n: float, num_fmt: str = '') -> str:
    """按 num_fmt 加单位后缀：1=百分比, 3=万元, 2=普通数值（不缩放）"""
    n = float(n)
    if num_fmt == '1':
        return _fmt_decimal(n) + '%'
    if num_fmt == '3':
        if n >= 10000:               # >= 1亿（10000万）
            return f'{n / 10000:.2f}亿'
        return _fmt_decimal(n) + '万'
    return _fmt_decimal(n)


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
        parser.add_argument('--float-ratio', type=float, default=None,
                            help='选项浮动区间比例，如 0.05 表示上下各浮动 5%（选填，不填用固定步长）')

    def handle(self, *args, **options):
        filepath = options['file']
        data_dt = options['data_dt']
        float_ratio = options.get('float_ratio')
        try:
            import openpyxl
        except ImportError:
            raise CommandError('请安装 openpyxl: pip install openpyxl')

        wb = openpyxl.load_workbook(filepath, read_only=True)
        ws = wb.active

        COL_ORG_ID, COL_TABLE, COL_LABEL, COL_BUSI, COL_COLNM, COL_FMT, COL_EXPR = 0, 6, 8, 10, 12, 14, 15

        def _parse_expr(raw) -> float:
            """解析 expr_0：只去掉单位后缀，直接存展示数值（不缩放）"""
            s = str(raw).strip().replace(',', '').replace('，', '')
            for suffix in ('万', '亿', '%'):
                s = s.replace(suffix, '')
            if not s:
                return 0.0
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
                'expr': _parse_expr(expr_raw),
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

        created = updated = 0
        for r in raw:
            val = float(r['expr'])
            stem = build_stem(r['table'], r['label'], r['busi'], r['col'])
            options, correct_letter = generate_interval_options(val, r['fmt'], float_ratio)
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
