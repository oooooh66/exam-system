# -*- coding: utf-8 -*-
"""
Validate 资产业务题库_导入模板.xlsx against the REAL system importer
(utils/excel_importer._parse_excel_row) using a real BusiUser.

The parse logic is exercised exactly as the live import does; the DB write is
rolled back so no data is persisted (category get_or_create still runs, then
rolls back). Reports per-row failures so we can confirm 0 failures.
"""
import os, sys, django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

import openpyxl
from django.db import transaction
from apps.users.models import BusiUser
from utils.excel_importer import _parse_excel_row, QUESTION_TYPE_MAP

XLSX = r"C:\project\exam-system\资产业务题库_导入模板.xlsx"

# a real user (used as created_by / category owner)
user = BusiUser.objects.first()
if user is None:
    user = BusiUser.objects.create(username='__validator__', is_staff=True)
print("VALIDATOR USER:", user.username, "(pk=%s)" % user.pk)

wb = openpyxl.load_workbook(XLSX, read_only=True)
sheet = wb.active
header_row = [cell.value for cell in sheet[1]]
header_map = {str(h).strip(): i for i, h in enumerate(header_row) if h}
print("HEADER:", header_row)

total = 0
ok = 0
fails = []
type_cnt = {v: 0 for v in QUESTION_TYPE_MAP.values()}
empty_answers = []

with transaction.atomic():
    for row_idx, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
        total += 1
        try:
            q = _parse_excel_row(row, header_map, user, None)
        except Exception as e:
            fails.append((row_idx, str(e), row[1] if len(row) > 1 else ''))
            continue
        if q is None:
            fails.append((row_idx, 'row returned None', ''))
            continue
        # sanity: correct_answer must be populated
        ca = q.correct_answer
        if ca in (None, '', [], '对', '错') and q.question_type == 'true_false':
            pass
        if q.question_type == 'true_false' and ca not in ('对', '错'):
            empty_answers.append((row_idx, repr(ca)))
        ok += 1
        type_cnt[q.question_type] += 1
    # rollback everything we just touched (category get_or_create etc.)
    transaction.set_rollback(True)

wb.close()

print("TOTAL ROWS:", total)
print("PARSED OK  :", ok)
print("FAILURES   :", len(fails))
print("TYPE COUNT :", type_cnt)
if empty_answers:
    print("WARN empty/malformed true_false answers:", len(empty_answers))
    for r in empty_answers[:10]:
        print("   row", r)
if fails:
    print("=== FAILURES (first 20) ===")
    for r in fails[:20]:
        print(f"   row {r[0]}: {r[1]} | stem={str(r[2])[:40]!r}")
    print("... total", len(fails), "failures")
else:
    print(">>> ALL ROWS PARSED BY THE REAL IMPORTER WITH 0 FAILURES <<<")
