"""使用 Django ORM 导入测试数据"""
import os, sys, json, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
import django
django.setup()

from apps.questions.models import BusiQuestionCategory, BusiQuestion
from apps.users.models import BusiUser

# 清空
BusiQuestion.objects.all().delete()
BusiQuestionCategory.objects.all().delete()

# 创建分类
cats = {
    '资产': BusiQuestionCategory.objects.create(
        id=1, name='资产',
        description='资产类业务知识考核，涵盖固定资产、流动资产、无形资产等',
        created_by=BusiUser.objects.get(id=2)
    ),
    '负债': BusiQuestionCategory.objects.create(
        id=2, name='负债',
        description='负债类业务知识考核，涵盖流动负债、长期负债、或有负债等',
        created_by=BusiUser.objects.get(id=2)
    ),
    '制度': BusiQuestionCategory.objects.create(
        id=3, name='制度',
        description='银行制度规范考核，涵盖风控制度、合规制度、操作流程等',
        created_by=BusiUser.objects.get(id=2)
    ),
}
print(f'分类: {len(cats)}')

# 题目数据
orgs = [('ORG001', '总行营业部'), ('ORG002', '分行营业部'), ('ORG003', '支行网点')]

# JSON 转换函数
def s(val):
    """将字符串转为合法 JSON 字符串值"""
    return json.dumps(val, ensure_ascii=False)

questions = []
total = 0

def add_qs(qtype, content, opts, answer, analysis, cat_name, diff, score, org_id, org_nm):
    global total
    questions.append(BusiQuestion(
        question_type=qtype,
        content=content,
        options=opts if isinstance(opts, list) else [],
        correct_answer=answer if isinstance(answer, (list, str)) else answer,
        analysis=analysis,
        category=cats[cat_name],
        difficulty=diff,
        default_score=score,
        org_id=org_id,
        org_nm=org_nm,
        created_by_id=1,
    ))
    total += 1
    if total % 100 == 0:
        BusiQuestion.objects.bulk_create(questions)
        questions.clear()
        print(f'  已插入 {total} 题...')

# ============ 资产-单选题 ============
asset_single = [
    ('固定资产的确认条件中，以下哪项不是必须满足的？',
     ['A. 与该资产相关的经济利益很可能流入企业', 'B. 该资产的成本能够可靠计量', 'C. 该资产必须是有形资产', 'D. 企业拥有该资产的所有权或控制权'],
     'C', '固定资产可以是有形或无形的，关键是要满足经济利益流入和成本可靠计量两个条件。', '资产', 'easy', 2),
    ('以下哪种折旧方法不属于加速折旧法？',
     ['A. 双倍余额递减法', 'B. 年数总和法', 'C. 年限平均法', 'D. 递减折旧法'],
     'C', '年限平均法是直线折旧法。双倍余额递减法和年数总和法属于加速折旧法。', '资产', 'easy', 2),
    ('银行持有至到期投资的后续计量采用什么方法？',
     ['A. 公允价值计量', 'B. 摊余成本计量', 'C. 成本与市价孰低', 'D. 可变现净值'],
     'B', '持有至到期投资按摊余成本进行后续计量。', '资产', 'medium', 2),
    ('贷款损失准备的计提方法是？',
     ['A. 直接转销法', 'B. 备抵法', 'C. 余额百分比法', 'D. 账龄分析法'],
     'B', '根据会计准则，贷款损失准备应采用备抵法核算。', '资产', 'medium', 2),
    ('无形资产摊销年限不应超过多少年？',
     ['A. 5年', 'B. 10年', 'C. 20年', 'D. 按合同或法律规定'],
     'D', '无形资产的摊销年限应按合同性权利或法定权利的期限确定。', '资产', 'medium', 2),
    ('可供出售金融资产的公允价值变动计入哪个科目？',
     ['A. 投资收益', 'B. 公允价值变动损益', 'C. 其他综合收益', 'D. 资本公积'],
     'C', '可供出售金融资产的公允价值变动计入其他综合收益。', '资产', 'hard', 3),
    ('以下哪项不属于流动资产？',
     ['A. 应收账款', 'B. 交易性金融资产', 'C. 固定资产', 'D. 存货'],
     'C', '固定资产属于非流动资产，使用年限超过一个会计年度。', '资产', 'easy', 2),
    ('资产减值测试的频率是？',
     ['A. 每月一次', 'B. 每季度一次', 'C. 每年至少一次', 'D. 只在有减值迹象时'],
     'C', '企业应当在资产负债表日判断资产是否存在可能发生减值的迹象，至少每年进行一次。', '资产', 'medium', 2),
    ('银行最重要的盈利资产是？',
     ['A. 固定资产', 'B. 现金及存放央行款项', 'C. 贷款及垫款', 'D. 无形资产'],
     'C', '贷款及垫款是商业银行最重要的盈利性资产。', '资产', 'easy', 2),
    ('长期股权投资采用权益法核算时，被投资单位实现净利润，投资方应？',
     ['A. 不作处理', 'B. 确认投资收益', 'C. 冲减投资成本', 'D. 确认资本公积'],
     'B', '权益法下，投资方应按持股比例确认应享有的被投资单位净利润份额。', '资产', 'medium', 2),
]
for i, (c, o, a, an, cat, diff, score) in enumerate(asset_single):
    add_qs('single_choice', c, o, a, an, cat, diff, score, orgs[i % 3][0], orgs[i % 3][1])
# Add 10 more single_choice for 资产 to reach 20
extra_asset_single = [
    ('固定资产的入账价值不包括？', ['A. 购买价款', 'B. 运输费', 'C. 安装费', 'D. 日常维修费'], 'D', '日常维修费作为当期费用处理。', '资产', 'easy', 2),
    ('交易性金融资产初始确认时，交易费用如何处理？', ['A. 计入资产成本', 'B. 计入当期损益', 'C. 计入资本公积', 'D. 递延处理'], 'B', '交易费用直接计入当期损益（投资收益）。', '资产', 'medium', 2),
    ('以下哪项不计入存货成本？', ['A. 采购价格', 'B. 运输费用', 'C. 仓储保管费', 'D. 可抵扣增值税'], 'D', '可抵扣的增值税进项税额不计入存货成本。', '资产', 'medium', 2),
    ('银行抵债资产的入账价值应按什么确定？', ['A. 账面价值', 'B. 公允价值', 'C. 评估价值', 'D. 协商价格'], 'B', '抵债资产应按公允价值进行初始计量。', '资产', 'hard', 3),
    ('商誉的减值测试应当？', ['A. 单独测试', 'B. 结合资产组测试', 'C. 不需要测试', 'D. 按年限摊销'], 'B', '商誉应当结合相关的资产组进行减值测试。', '资产', 'hard', 3),
    ('应收款项坏账准备的计提体现什么会计原则？', ['A. 权责发生制', 'B. 谨慎性原则', 'C. 重要性原则', 'D. 实质重于形式'], 'B', '计提坏账准备体现了谨慎性原则。', '资产', 'easy', 2),
    ('银行间同业拆借属于哪种资产？', ['A. 固定资产', 'B. 长期资产', 'C. 流动资产', 'D. 递延资产'], 'C', '同业拆借通常期限较短，属于流动资产。', '资产', 'easy', 2),
    ('公允价值计量的输入值分为几个层级？', ['A. 2个', 'B. 3个', 'C. 4个', 'D. 5个'], 'B', '公允价值分为三个层级。', '资产', 'medium', 2),
    ('资产证券化中，基础资产应当满足什么条件？', ['A. 必须是有形资产', 'B. 能产生可预测的现金流', 'C. 必须是固定资产', 'D. 必须是无风险资产'], 'B', '基础资产必须能产生可预测的、稳定的现金流。', '资产', 'hard', 3),
    ('对于使用寿命不确定的无形资产，应如何处理？', ['A. 按10年摊销', 'B. 不摊销但每年减值测试', 'C. 按20年摊销', 'D. 一次性计入费用'], 'B', '使用寿命不确定的无形资产不摊销但每年减值测试。', '资产', 'medium', 2),
]
for i, (c, o, a, an, cat, diff, score) in enumerate(extra_asset_single):
    add_qs('single_choice', c, o, a, an, cat, diff, score, orgs[(i+10) % 3][0], orgs[(i+10) % 3][1])

# Quick: generate remaining questions for all categories/types using factory pattern
print('批量生成剩余题目...')

types_map = {
    'single_choice': '单选题', 'multiple_choice': '多选题', 
    'true_false': '判断题', 'fill_blank': '填空题', 'short_answer': '简答题'
}

# 各题型题库模板
templates = {
    '资产': {
        'single_choice': [
            ('{cat}类资产中，{item}的确认条件是？', ['A. 经济利益流入', 'B. 成本可计量', 'C. 两者都是', 'D. 以上都不对'], 'C'),
            ('关于{cat}资产折旧，以下说法正确的是？', ['A. 必须用直线法', 'B. 必须用加速法', 'C. 应反映经济利益消耗方式', 'D. 可任意选择'], 'C'),
            ('{cat}资产期末计量应采用什么方法？', ['A. 成本法', 'B. 公允价值', 'C. 成本与市价孰低', 'D. 重置成本'], 'A'),
            ('以下哪项不属于{cat}资产的确认条件？', ['A. 过去交易形成', 'B. 企业拥有或控制', 'C. 预期带来经济利益', 'D. 必须可立即变现'], 'D'),
            ('{cat}资产的减值损失确认后？', ['A. 可以转回', 'B. 不可转回', 'C. 部分可转回', 'D. 视情况而定'], 'B'),
            ('{cat}业务的初始计量应基于？', ['A. 历史成本', 'B. 公允价值', 'C. 重置成本', 'D. 可变现净值'], 'A'),
            ('关于{cat}资产管理，以下哪项是正确的？', ['A. 无需定期评估', 'B. 需定期减值测试', 'C. 一次性入账', 'D. 不存在风险'], 'B'),
            ('{cat}资产重估增值应计入？', ['A. 投资收益', 'B. 其他综合收益', 'C. 营业外收入', 'D. 主营业务收入'], 'B'),
            ('{cat}类资产的后续支出资本化条件是？', ['A. 任何支出都可以', 'B. 延长使用寿命或提高性能', 'C. 金额超过1000元', 'D. 管理层批准即可'], 'B'),
            ('{cat}资产报废处置时，净损益应计入？', ['A. 投资收益', 'B. 营业外收支', 'C. 管理费用', 'D. 财务费用'], 'B'),
        ],
        'multiple_choice': [
            ('以下哪些属于{cats}资产的特征？', ['A. 由过去交易形成', 'B. 预期带来经济利益', 'C. 企业拥有或控制', 'D. 必须是货币形式'], ['A','B','C']),
            ('关于{cat}资产，以下说法正确的有？', ['A. 需要定期评估', 'B. 应合理分类', 'C. 不计提减值', 'D. 账面价值需要披露'], ['A','B','D']),
            ('{cat}资产评估的方法包括？', ['A. 成本法', 'B. 市场法', 'C. 收益法', 'D. 随意法'], ['A','B','C']),
            ('影响{cat}资产价值的因素有？', ['A. 使用年限', 'B. 技术更新', 'C. 市场环境', 'D. 以上都是'], ['A','B','C','D']),
            ('{cat}资产风险管理包括？', ['A. 风险识别', 'B. 风险评估', 'C. 风险应对', 'D. 风险忽略'], ['A','B','C']),
        ],
        'true_false': [
            ('{cat}资产需要定期进行减值测试。', '对'),
            ('{cat}资产可以无限期使用不更新。', '错'),
            ('{cat}资产的管理应遵循谨慎性原则。', '对'),
            ('{cat}资产的记录可以不完整。', '错'),
            ('{cat}资产评估可采用多种方法结合使用。', '对'),
        ],
        'fill_blank': [
            ('{cat}资产的确认需满足经济利益流入和______两个条件。', '成本可计量'),
            ('{cat}资产应按______进行初始计量。', '历史成本'),
            ('{cat}资产减值测试应至少每年______次。', '一'),
            ('{cat}资产管理应遵循______原则。', '谨慎性'),
            ('{cat}资产的______价值等于原值减折旧减减值。', '账面'),
        ],
        'short_answer': [
            ('请简述{cat}资产的管理要点。', '{cat}资产的管理要点包括：建立完善的资产业务制度、规范资产的确认计量记录和报告流程、加强资产的日常维护和定期核查、及时评估资产减值风险并计提减值准备、建立健全的资产处置和报废机制。'),
            ('请说明{cat}资产的审计关注点。', '{cat}资产审计应重点关注以下方面：资产的真实性——核实资产是否真实存在、所有权是否清晰；资产的计价——检查初始计量和后续计量是否合规；减值测试——评估减值准备的充分性和合理性；披露完整性——检查财务报表附注是否充分披露资产相关信息。'),
            ('请分析{cat}资产的风险特征。', '{cat}资产的主要风险特征包括：市场风险——市场价值波动可能影响资产计量；信用风险——交易对手违约风险；操作风险——资产管理流程缺陷或人员失误；流动性风险——部分资产难以快速变现。管理措施包括建立风险限额、分散投资、定期重评等。'),
        ],
    },
    '负债': {},
    '制度': {},
}

# Copy template structure for 负债 and 制度
for cat_name in ['负债', '制度']:
    templates[cat_name] = {
        'single_choice': [
            ('关于{cat}类业务的{action}，以下哪项是正确的？', ['A. 选项一', 'B. 选项二', 'C. 选项三', 'D. 选项四'], 'A'),
            ('{cat}的管理原则包括？', ['A. 安全性优先', 'B. 盈利性优先', 'C. 流动性优先', 'D. 以上都是'], 'D'),
            ('以下哪个不属于{cat}管理的范畴？', ['A. 风险识别', 'B. 风险评估', 'C. 风险控制', 'D. 全能放任'], 'D'),
            ('{cat}管理中的{action}政策是？', ['A. 积极管理', 'B. 消极管理', 'C. 科学管理', 'D. 无效管理'], 'C'),
            ('{cat}的基本要求不包括？', ['A. 数据完整', 'B. 流程规范', 'C. 责任清晰', 'D. 可以随意操作'], 'D'),
            ('关于{cat}，以下说法正确的是？', ['A. 不重要', 'B. 需要高度重视', 'C. 可有可无', 'D. 只有大企业需要'], 'B'),
        ] * 2,  # duplicate to get more questions
        'multiple_choice': [
            ('以下哪些属于{cat}管理的要求？', ['A. 制度健全', 'B. 执行到位', 'C. 持续改进', 'D. 一成不变'], ['A','B','C']),
            ('{cat}管理中应注意的事项有？', ['A. 合规性', 'B. 时效性', 'C. 完整性', 'D. 以上都是'], ['A','B','C','D']),
            ('关于{cat}的风险管理，正确的有？', ['A. 需要定期评估', 'B. 应建立预警机制', 'C. 可随意处理', 'D. 需制定应急预案'], ['A','B','D']),
        ],
        'true_false': [
            ('{cat}的管理需要严格遵守相关制度规范。', '对'),
            ('{cat}管理中可以随意绕过制度流程。', '错'),
            ('{cat}的定期评估是管理工作的基础。', '对'),
            ('{cat}的相关记录不需要保存。', '错'),
        ],
        'fill_blank': [
            ('{cat}管理应建立______审核机制。', '分级'),
            ('{cat}控制的目标是确保______和有效性。', '合规性'),
            ('{cat}工作应遵循______流程。', '标准化'),
        ],
        'short_answer': [
            ('请简述{cat}的管理原则和要求。', '管理原则：建立完善的制度体系、明确责任分工、规范操作流程、加强监督考核。具体要求：严格遵守国家法律法规、建立健全内部控制机制、确保信息真实完整、定期评估和改进管理效果。'),
            ('请说明{cat}的风险防控措施。', '防控措施包括：完善制度建设——建立健全各项管理制度和操作规程；加强监督检查——定期和不定期检查制度执行情况；持续改进——根据检查结果和外部环境变化不断完善管理措施；强化责任追究——对违规行为严肃处理。'),
        ],
    }

# Flatten single_choice templates
for cat_name in ['负债', '制度']:
    sc = templates[cat_name]['single_choice']
    templates[cat_name]['single_choice'] = []
    for _ in range(20):
        templates[cat_name]['single_choice'].append(sc[_ % len(sc)])

# Flatten multiple_choice
for cat_name in ['负债', '制度']:
    mc = templates[cat_name]['multiple_choice']
    templates[cat_name]['multiple_choice'] = []
    for _ in range(20):
        templates[cat_name]['multiple_choice'].append(mc[_ % len(mc)])

# Flatten true_false
for cat_name in ['负债', '制度']:
    tf = templates[cat_name]['true_false']
    templates[cat_name]['true_false'] = []
    for _ in range(15):
        templates[cat_name]['true_false'].append(tf[_ % len(tf)])

# Flatten fill_blank
for cat_name in ['负债', '制度']:
    fb = templates[cat_name]['fill_blank']
    templates[cat_name]['fill_blank'] = []
    for _ in range(20):
        templates[cat_name]['fill_blank'].append(fb[_ % len(fb)])

# Flatten short_answer
for cat_name in ['负债', '制度']:
    sa = templates[cat_name]['short_answer']
    templates[cat_name]['short_answer'] = []
    for _ in range(20):
        templates[cat_name]['short_answer'].append(sa[_ % len(sa)])

# Now generate all remaining questions
counts = {}
for cat_name in ['资产', '负债', '制度']:
    # Skip single_choice for 资产 (already done 20)
    if cat_name == '资产':
        sc_count = 20
    else:
        sc_count = 0
    
    for qtype, qtype_cn in types_map.items():
        if cat_name == '资产' and qtype == 'single_choice':
            counts[f'{cat_name}_{qtype}'] = 20
            continue
        
        need = 20 if cat_name == '资产' else 20
        templates_list = templates[cat_name][qtype]
        
        current = 0
        tpl_idx = 0
        items = [
            ('固定资产', '折旧', '折旧处理'), ('贷款', '拨备', '计提风险'), 
            ('存货', '盘点', '价值评估'), ('应收账款', '回收', '逾期管理'),
            ('投资', '收益', '投资回报'), ('无形资产', '估值', '价值评定'),
            ('商誉', '测试', '合并评估'), ('金融资产', '分类', '资产重分'),
            ('长期股权', '核算', '权益核算'), ('在建工程', '结转', '完工转固'),
            ('银行存款', '管理', '资金管理'), ('应收票据', '贴现', '票据处理'),
            ('预付账款', '核销', '预付款项'), ('其他应收款', '清理', '往来清理'),
            ('持有至到期', '计量', '摊余成本'), ('交易性金融', '评估', '市值评估'),
            ('可供出售', '重分类', '资产调整'), ('投资性房产', '转换', '模式切换'),
            ('抵债资产', '处置', '资产变现'), ('递延所得税', '确认', '税会差异'),
        ]
        
        for _ in range(need):
            item, action, context = items[tpl_idx % len(items)]
            tpl = templates_list[current % len(templates_list)]
            
            if qtype == 'single_choice':
                content_t = tpl[0].replace('{cat}', cat_name).replace('{item}', item).replace('{action}', context)
                opts = tpl[1]
                ans = tpl[2]
                analysis = f'{cat_name}类知识考核题，考察{item}相关概念。'
                add_qs(qtype, content_t, opts, ans, analysis, cat_name, 'easy', 2, 
                       orgs[tpl_idx % 3][0], orgs[tpl_idx % 3][1])
                
            elif qtype == 'multiple_choice':
                content_t = tpl[0].replace('{cat}', cat_name).replace('{cats}', cat_name).replace('{item}', item)
                opts = tpl[1]
                ans = tpl[2]
                analysis = f'多选题，考察{cat_name}领域知识。'
                add_qs(qtype, content_t, opts, ans, analysis, cat_name, 'medium', 3,
                       orgs[(tpl_idx+20) % 3][0], orgs[(tpl_idx+20) % 3][1])
                
            elif qtype == 'true_false':
                content_t = tpl[0].replace('{cat}', cat_name).replace('{item}', item)
                ans = tpl[1]
                analysis = '判断题，考察基本概念。'
                add_qs(qtype, content_t, [], ans, analysis, cat_name, 'easy', 2,
                       orgs[tpl_idx % 3][0], orgs[tpl_idx % 3][1])
                
            elif qtype == 'fill_blank':
                content_t = tpl[0].replace('{cat}', cat_name).replace('{item}', item)
                ans = tpl[1]
                analysis = f'填空题，考察{cat_name}领域基础知识。'
                add_qs(qtype, content_t, [], ans, analysis, cat_name, 'easy', 3,
                       orgs[(tpl_idx+10) % 3][0], orgs[(tpl_idx+10) % 3][1])
                
            elif qtype == 'short_answer':
                content_t = tpl[0].replace('{cat}', cat_name).replace('{item}', item)
                ans = tpl[1]
                analysis = f'简答题，考察{cat_name}领域的综合分析能力。'
                add_qs(qtype, content_t, [], ans, analysis, cat_name, 'medium', 5,
                       orgs[tpl_idx % 3][0], orgs[tpl_idx % 3][1])
            
            current += 1
            tpl_idx += 1

# Flush remaining
if questions:
    BusiQuestion.objects.bulk_create(questions)

print(f'\n=== 导入完成 ===')
print(f'总题目数: {BusiQuestion.objects.count()}')
for qt, qtn in types_map.items():
    c = BusiQuestion.objects.filter(question_type=qt).count()
    print(f'  {qtn}: {c}')
for cat in cats.values():
    c = BusiQuestion.objects.filter(category=cat).count()
    print(f'  {cat.name}: {c}')
