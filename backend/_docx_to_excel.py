# -*- coding: utf-8 -*-
"""
Parse 资产业务题库.docx -> 资产业务题库_导入模板.xlsx
Matches backend/utils/excel_importer.py field contract.
"""
import re, zipfile
import xml.etree.ElementTree as ET
import openpyxl

DOCX = r"C:\project\exam-system\零售条线题库.docx"
OUT = r"C:\project\exam-system\零售条线题库_导入模板3.xlsx"

# ---------- 1. read paragraphs ----------
def read_paras(path):
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml")
    root = ET.fromstring(xml)
    W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    out = []
    for p in root.iter(W + "p"):
        texts = [t.text for t in p.iter(W + "t") if t.text]
        out.append("".join(texts))
    return out

# ---------- 2. noise cleaning ----------
# A .docx filename in this doc is ALWAYS a doc-title citation (a "关于印发...的
# 通知.docx" style block) inserted between questions. Crucially it is always
# immediately preceded by one of a small set of boundaries (解析：/指出：/——/。/
# ？/（/《/quote/line-start) and NEVER immediately preceded by an answer value
# (参考答案：正确 -> the 正确 sits after 答案's ：, which is NOT a boundary). We
# anchor the match to those boundaries so the answer value can never be eaten.
# The body still refuses to cross ? / ： / 。 / ， / 答案 / 参考 / 正确 / 错误 /
# X. / XX as a safety net. Forbidding the clause punctuation (：。，) is critical:
# it stops a match that accidentally starts at a STEM's first character (e.g. line
# start 根) from greedily consuming the whole stem just to reach a distant .docx.
_LEFT = (r'(?:(?<=解析：)|(?<=指出：)|(?<=——)|(?<=。)|(?<=？)|'
         r'(?<=（)|(?<=《)|(?<=“)|(?<=”)|(?<=\s)|(?<=\A))')
_DOCX_BODY = r'(?:(?!答案|参考|正确|错误|[A-Fa-f]\s*[.．、]|[A-Fa-f]{2,})[^？：。，])*?'
DOCX_CITE = re.compile(_LEFT + r'[一-鿿《（]' + _DOCX_BODY + r'\.docx')
NOTE_NOISE = re.compile(r'[（(]注[:：].*?[）)]')

def clean_para(p):
    p = NOTE_NOISE.sub('', p)
    p = DOCX_CITE.sub('', p)
    return p

# ---------- 3. section + answer detection ----------
SECTION_RE = re.compile(r'^[一二三四五六七八九十]+、\s*(单选题|多选题|判断题|填空题|简答题)')
ANS_RE = re.compile(r'(参考)?答案[:：]\s*([A-Fa-f]+|正确|错误|对|错)')
LEAD_NUM = re.compile(r'^\s*\d+[.．、]\s')

def has_options(text):
    return bool(re.search(r'A\s*[.．、]', text) and re.search(r'B\s*[.．、]', text))

def looks_complete(text):
    if not text or not text.strip():
        return False
    if re.search(r'[？?]', text) and re.search(r'[A-F]\s*[.．、]', text):
        return True
    if re.search(r'[（(]\s*[）)]', text):
        return True
    return False

def is_new_num_prefix(s):
    return bool(LEAD_NUM.match(s))

def looks_like_q_start(s):
    """Decide whether leftover text after an answer looks like the start of a
    NEW question (so it should be carried into `pending`) vs. pure noise
    (trailing discussion / doc-title debris) which should be discarded.

    A real question start is recognised by genuine question features (a ? mark,
    a （ ） bracket for judges, a leading number, or an A. option). A doc-title
    citation (a .docx filename, often starting with 关于/根据/《) contains NONE
    of those, so it must be treated as debris and dropped — otherwise it gets
    accumulated into `pending` and corrupts the following question."""
    s = s.strip()
    if not s:
        return False
    if '.docx' in s:
        return False
    if '？' in s or '（ ）' in s or '（）' in s:
        return True
    if re.match(r'^\s*\d+[.．、]', s):
        return True
    if re.match(r'^\s*A\s*[.．、]', s):
        return True
    return False

def starts_new_option_set(s):
    return bool(re.match(r'^\s*A\s*[.．、]', s))

def should_split(pending, before, qtype):
    if not pending or not pending.strip():
        return False
    if not looks_complete(pending):
        return False
    b = before.strip()
    if not b:
        return False
    if is_new_num_prefix(b):
        return True
    if starts_new_option_set(b):
        return True
    if has_options(b):
        return True
    if qtype == '判断题' and (re.search(r'[（(]\s*[）)]', b) or b.startswith(('根据', '关于', '《'))):
        return True
    return False

# ---------- 4. option parsing ----------
def parse_options(s):
    items = []
    for m in re.finditer(r'([A-F])\s*[.．、]\s*(.*?)(?=\s*[A-F]\s*[.．、]|$)', s, re.S):
        letter = m.group(1)
        content = m.group(2).strip()
        if content:
            items.append(f"{letter}. {content}")
    return items

def strip_lead_num(stem):
    return re.sub(r'^\s*\d+[.．、]\s*', '', stem).strip()

def build_question(qtype, text, val, analysis):
    text = text.strip()
    if qtype in ('单选题', '多选题'):
        m = re.search(r'([A-F])\s*[.．、]', text)
        if not m:
            return None
        stem = strip_lead_num(text[:m.start()])
        opt_raw = text[m.start():]
        opts = parse_options(opt_raw)
        if len(opts) < 2:
            return None
        val_u = val.upper()
        if qtype == '单选题':
            answer = val_u
        else:
            answer = ','.join(list(val_u))
        return {'type': qtype, 'stem': stem, 'options': opts,
                'answer': answer, 'analysis': analysis or ''}
    else:  # 判断题
        stem = strip_lead_num(text)
        if val in ('正确', '对'):
            answer = '对'
        elif val in ('错误', '错'):
            answer = '错'
        else:
            return None
        return {'type': qtype, 'stem': stem, 'options': [],
                'answer': answer, 'analysis': analysis or ''}

# ---------- 5. main accumulation ----------
paras = read_paras(DOCX)
questions = []
no_answer = []
failed = []

current_type = None
pending = ''

def flush_no_answer():
    global pending
    if pending.strip():
        no_answer.append({'type': current_type, 'raw': pending.strip()})
    pending = ''

for raw in paras:
    line = clean_para(raw).strip()
    if not line:
        continue
    msec = SECTION_RE.match(line)
    if msec:
        flush_no_answer()
        current_type = msec.group(1)
        continue
    if current_type is None:
        continue

    markers = list(ANS_RE.finditer(line))
    if not markers:
        if pending and is_new_num_prefix(line) and looks_complete(pending):
            flush_no_answer()
        pending += line
        continue

    prev_end = 0
    for mi, m in enumerate(markers):
        before = line[prev_end:m.start()]
        val = m.group(2)
        after = line[m.end():]
        if mi == 0 and should_split(pending, before, current_type):
            flush_no_answer()
        qtext = pending + before
        if qtext.strip():
            analysis = ''
            next_start = after
            if next_start.lstrip().startswith('解析'):
                a = next_start.lstrip()[2:].lstrip()
                a = DOCX_CITE.sub('', a)
                analysis = a.strip()
                next_start = ''
            q = build_question(current_type, qtext.strip(), val, analysis)
            if q:
                questions.append(q)
            else:
                failed.append({'type': current_type, 'raw': qtext.strip(), 'val': val})
        # carry leftover to pending only if it looks like a new question start;
        # otherwise it is trailing noise (doc-title debris / discussion) -> drop.
        if mi == len(markers) - 1:
            pending = after if looks_like_q_start(after) else ''
        else:
            pending = ''
        prev_end = m.end()

flush_no_answer()

# ---------- 6. report ----------
# residual-noise scan
polluted = []
for q in questions:
    blob = q['stem'] + ' ' + ' '.join(q['options']) + ' ' + q['analysis']
    if '.docx' in blob or '印发' in blob or '的通知 .' in blob or blob.lstrip().startswith('关于印发'):
        polluted.append(q)
print("POLLUTED (residual noise):", len(polluted))
for q in polluted[:10]:
    print("   POLL:", q['type'], "::", (q['stem'] + ' ' + ' '.join(q['options']))[:70])
# show a few samples per type
for t in ('单选题', '多选题', '判断题'):
    print(f"--- sample {t} ---")
    for q in questions:
        if q['type'] == t:
            print("   题干:", q['stem'][:45])
            print("   选项:", q['options'])
            print("   答案:", q['answer'], "| 解析:", q['analysis'][:30])
            break
from collections import Counter
cnt = Counter(q['type'] for q in questions)
print("PARSED:", len(questions), dict(cnt))
print("NO_ANSWER (flagged):", len(no_answer))
for n in no_answer:
    print("   [NO_ANSWER]", n['type'], "::", n['raw'])
print("BUILD_FAILED:", len(failed))
for f in failed:
    print("   [FAIL]", f['type'], "val=", f['val'], "::", f['raw'][:60])

# ---------- 7. write excel ----------
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "题库导入"
headers = ['题型', '题干', '选项A', '选项B', '选项C', '选项D', '选项E', '选项F',
           '正确答案', '解析', '难度', '分类', '分值']
ws.append(headers)
for q in questions:
    row = [q['type'], q['stem']]
    opts = q['options']
    for i in range(6):
        row.append(opts[i] if i < len(opts) else '')
    row.append(q['answer'])
    row.append(q['analysis'])
    row.append('')          # 难度 -> default easy
    row.append('资产')      # 分类
    row.append('')          # 分值 -> default 5
    ws.append(row)
wb.save(OUT)
print("WROTE:", OUT, "rows:", len(questions))
