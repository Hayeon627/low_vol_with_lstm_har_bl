# -*- coding: utf-8 -*-
import re, sys
path = sys.argv[1]
doc = open(path, encoding='utf-8').read()
HEAVY, LIGHT = 12, 4

NONUM = '<w:numPr><w:ilvl w:val="0"/><w:numId w:val="0"/></w:numPr>'
def suppress_num(p):
    if '<w:numPr' in p:
        return re.sub(r'<w:numPr>.*?</w:numPr>', NONUM, p, flags=re.S)
    return re.sub(r'(<w:pStyle w:val="[123]"/>)', r'\1' + NONUM, p, count=1)
def prepend_run(p, text):
    rm = re.search(r'<w:r\b.*?</w:r>', p, re.S)
    if not rm: return p
    rpr = re.search(r'<w:rPr>.*?</w:rPr>', rm.group(0), re.S)
    rpr = rpr.group(0) if rpr else ''
    run = '<w:r>' + rpr + '<w:t xml:space="preserve">' + text + '</w:t></w:r>'
    return p[:rm.start()] + run + p[rm.start():]

st = {'h1': 0, 'past_refs': False, 'apx': []}
def fix(pm):
    p = pm.group(0)
    ps = re.search(r'<w:pStyle w:val="([^"]*)"', p)
    sid = ps.group(1) if ps else ''
    if sid in ('FirstParagraph', 'BodyText'):
        return re.sub(r'<w:pStyle w:val="(FirstParagraph|BodyText)"/>', '', p, count=1)
    if sid == '1':
        idx = st['h1']; st['h1'] += 1
        if idx == 5:
            st['past_refs'] = True; return suppress_num(p)
        if idx >= 6:
            letter = chr(ord('A') + idx - 6); st['apx'].append(letter)
            return prepend_run(suppress_num(p), '부록 %s. ' % letter)
        return p
    if sid == '2' and st['past_refs']:
        return suppress_num(p)
    return p
doc = re.sub(r'<w:p\b.*?</w:p>', fix, doc, flags=re.S)

c_cap = doc.count('부록~ 참조'); doc = doc.replace('부록~ 참조', '부록 E 참조')
c_ann = doc.count('ANN-anchor pyo2018'); doc = doc.replace('ANN-anchor pyo2018', 'ANN-anchor (Pyo &amp; Lee, 2018)')

# 그림3 캡션 복원
FIG3 = ('<w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r>'
        '<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="바탕"/>'
        '<w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>'
        '<w:t xml:space="preserve">&lt;그림 3&gt; Performance-weighted 앙상블 기반의 변동성 예측 흐름.</w:t></w:r></w:p>')
c_fig3 = 0
for mm in re.finditer(r'<w:tbl>.*?</w:tbl>', doc, re.S):
    if '가중 결합' in mm.group(0) and 'BL 입력' in mm.group(0):
        if '그림 3&gt; Performance-weighted' not in doc:
            doc = doc[:mm.end()] + FIG3 + doc[mm.end():]; c_fig3 = 1
        break

# 표21·22: 2단 헤더(multicolumn 그룹 + cmidrule) 복구
def bd(side, sz): return '<w:%s w:val="single" w:sz="%d" w:space="0" w:color="auto"/>' % (side, sz)
def hcell(text, span, top, bottom, bold=False):
    pr = '<w:tcPr>' + ('<w:gridSpan w:val="%d"/>' % span if span > 1 else '')
    if top or bottom:
        pr += '<w:tcBorders>' + (bd('top', top) if top else '') + (bd('bottom', bottom) if bottom else '') + '</w:tcBorders>'
    pr += '<w:vAlign w:val="center"/></w:tcPr>'
    run = ''
    if text:
        et = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        rpr = '<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="바탕"/>' + ('<w:b/>' if bold else '') + '</w:rPr>'
        run = '<w:r>' + rpr + '<w:t xml:space="preserve">' + et + '</w:t></w:r>'
    return '<w:tc>' + pr + '<w:p><w:pPr><w:pStyle w:val="a8"/></w:pPr>' + run + '</w:p></w:tc>'
specs = [(21, 3, ['국면','저변동','고변동','스프레드','저변동','고변동','스프레드']),
         (22, 2, ['국면','mean(q)','% q < 0','mean(q)','% q < 0'])]
c_hdr = 0
for num, span, hdr in specs:
    mc = re.search(r'<w:t[^>]*>&lt;표 %d&gt;' % num, doc)
    if not mc: continue
    tm = re.search(r'<w:tbl>.*?</w:tbl>', doc[mc.end():], re.S)
    if not tm: continue
    tbl = tm.group(0); s = mc.end() + tm.start(); e = mc.end() + tm.end()
    rows = re.findall(r'<w:tr\b.*?</w:tr>', tbl, re.S)
    if len(rows) < 3: continue
    pre = tbl[:tbl.find('<w:tr')]
    r0 = hcell('', 1, HEAVY, 0) + hcell('앙상블 (E)', span, HEAVY, LIGHT) + hcell('ANN (A)', span, HEAVY, LIGHT)
    r1 = ''.join(hcell(h, 1, 0, LIGHT) for h in hdr)
    newtbl = pre + '<w:tr>' + r0 + '</w:tr><w:tr>' + r1 + '</w:tr>' + ''.join(rows[2:]) + '</w:tbl>'
    doc = doc[:s] + newtbl + doc[e:]; c_hdr += 1

# 표1: \multicolumn{1}{l}{전체} 라벨 드롭 복구 + 요약행 상단 구분선
def fix_table1(doc):
    mc = re.search(r'<w:t[^>]*>&lt;표 1&gt;', doc)
    if not mc: return doc, 0
    tm = re.search(r'<w:tbl>.*?</w:tbl>', doc[mc.end():], re.S)
    if not tm: return doc, 0
    tbl = tm.group(0); s = mc.end()+tm.start(); e = mc.end()+tm.end()
    def at(seg): return ''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', seg))
    rows = re.findall(r'<w:tr\b.*?</w:tr>', tbl, re.S); out=[]; ch=0
    for r in rows:
        if '192' in at(r) and '전체' not in at(r):
            ftc = re.search(r'<w:tc>.*?</w:tc>', r, re.S).group(0)
            run = '<w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="바탕"/></w:rPr><w:t xml:space="preserve">전체</w:t></w:r>'
            para = '<w:p><w:pPr><w:pStyle w:val="a8"/></w:pPr>' + run + '</w:p>'
            if '<w:p/>' in ftc:
                ntc = ftc.replace('<w:p/>', para, 1)
            elif '<w:p></w:p>' in ftc:
                ntc = ftc.replace('<w:p></w:p>', para, 1)
            else:
                ntc = re.sub(r'</w:p>', run + '</w:p>', ftc, count=1)
            r2 = r.replace(ftc, ntc, 1)
            r2 = r2.replace('<w:tcBorders>', '<w:tcBorders><w:top w:val="single" w:sz="4" w:space="0" w:color="auto"/>')
            out.append(r2); ch=1
        else:
            out.append(r)
    if ch:
        pre = tbl[:tbl.find('<w:tr')]
        doc = doc[:s] + pre + ''.join(out) + '</w:tbl>' + doc[e:]
    return doc, ch
doc, c_t1 = fix_table1(doc)
print('표1 전체 라벨 복구:%d' % c_t1)

# 표25/26: 소스 \mathbf{값} 볼드를 (행,열) 매핑으로 복원
def fix_benchmark_value_bold(doc):
    src = open('/sessions/sleepy-loving-thompson/mnt/low_vol_with_lstm_har_bl/paper/paper.md', encoding='utf-8').read()
    src = '\n'.join(l for l in src.split('\n') if not l.lstrip().startswith('%'))
    def block(lab):
        for t in re.finditer(r'\\begin\{table\}.*?\\end\{table\}', src, re.S):
            if '\\label{' + lab + '}' in t.group(0): return t.group(0)
    total = 0
    for num, lab in [(25, 'tab:benchmark_mdd'), (26, 'tab:benchmark_annret')]:
        blk = block(lab)
        if not blk: continue
        tab = re.search(r'\\begin\{tabular\}.*?\\end\{tabular\}', blk, re.S).group(0)
        rows = [r for r in re.split(r'\\\\', tab) if '&' in r]
        boldpos = []
        for ri, row in enumerate(rows):
            for ci, c in enumerate(row.split('&')):
                if '\\mathbf{' in c: boldpos.append((ri, ci))
        mc = re.search(r'<w:t[^>]*>&lt;표 %d&gt;' % num, doc)
        if not mc: continue
        tm = re.search(r'<w:tbl>.*?</w:tbl>', doc[mc.end():], re.S)
        if not tm: continue
        tbl = tm.group(0); st = mc.end() + tm.start(); en = mc.end() + tm.end()
        trs = re.findall(r'<w:tr\b.*?</w:tr>', tbl, re.S)
        for (ri, ci) in boldpos:
            if ri >= len(trs): continue
            cs = re.findall(r'<w:tc>.*?</w:tc>', trs[ri], re.S)
            if ci >= len(cs): continue
            c = cs[ci]
            if '<w:b/>' in c: continue
            nc = c.replace('<w:rPr>', '<w:rPr><w:b/>')
            trs[ri] = trs[ri].replace(c, nc, 1); total += 1
        pre = tbl[:tbl.find('<w:tr')]
        doc = doc[:st] + pre + ''.join(trs) + '</w:tbl>' + doc[en:]
    return doc, total
doc, c_vb = fix_benchmark_value_bold(doc)
print('표25/26 값볼드 복원:%d' % c_vb)

# 부록 표/그림 재번호: 원본 LaTeX 체계 (\appendix에서 카운터 리셋 -> 표 A.1~A.20, 그림 A.1)
def renumber_appendix(doc):
    n_cap = 0
    for n in range(7, 27):
        new = 'A.%d' % (n - 6)
        b4 = doc
        doc = doc.replace('&lt;표 %d&gt;' % n, '&lt;표 %s&gt;' % new)
        if doc != b4: n_cap += 1
    b4 = doc
    doc = doc.replace('&lt;그림 8&gt;', '&lt;그림 A.1&gt;')
    if doc != b4: n_cap += 1
    SP = '[ \u00a0]'
    doc = re.sub('표(%s)13(\u2013|--|-)15' % SP, lambda m: '표'+m.group(1)+'A.7'+m.group(2)+'A.9', doc)
    doc = re.sub('표(%s)16(\u2013|--|-)18' % SP, lambda m: '표'+m.group(1)+'A.10'+m.group(2)+'A.12', doc)
    for n in range(26, 6, -1):
        k = 'A.%d' % (n - 6)
        doc = re.sub('표(%s)%d(?!\\d)' % (SP, n), (lambda kk: (lambda m: '표'+m.group(1)+kk))(k), doc)
    doc = re.sub('그림(%s)8(?!\\d)' % SP, lambda m: '그림'+m.group(1)+'A.1', doc)
    return doc, n_cap
doc, c_ren = renumber_appendix(doc)
print('\ubd80\ub85d \uc7ac\ubc88\ud638 \uce90\uc158:%d' % c_ren)

# 페이지 초과 이미지 축소 (높이 한도 18.9cm, 비례 축소)
def shrink_images(doc):
    MAXH = 6800000
    n = [0]
    def fix(m):
        d = m.group(0)
        e = re.search(r'<wp:extent cx="(\d+)" cy="(\d+)"/>', d)
        if not e: return d
        cx, cy = int(e.group(1)), int(e.group(2))
        if cy <= MAXH: return d
        sc = MAXH / cy
        d = d.replace('cx="%d"' % cx, 'cx="%d"' % int(cx * sc)).replace('cy="%d"' % cy, 'cy="%d"' % MAXH)
        n[0] += 1
        return d
    doc = re.sub(r'<w:drawing>.*?</w:drawing>', fix, doc, flags=re.S)
    return doc, n[0]
doc, c_img = shrink_images(doc)
print('이미지 축소:%d' % c_img)

# 영문 초록/키워드 삽입 (사용자 제공, 2026-06)
ABS_EN = ('The Black-Litterman (BL) model mitigates the estimation-error sensitivity of mean-variance '
'optimization (MVO) by combining market equilibrium with investor views, yet its dependence on '
'expert-formed views remains a persistent limitation. Although a growing body of research applies '
'machine learning to the BL model, most efforts have concentrated on return forecasting; the direct '
'integration of volatility forecasts into BL views remains underexplored. Building on the framework '
'of Pyo and Lee (2018), which incorporates an artificial neural network (ANN)\u2013based volatility '
'forecast as a BL view, this study extends the approach along two complementary dimensions. First, '
'we replace the single ANN with a performance-weighted LSTM\u2013HAR ensemble to capture the multi-scale '
'and sequential dependence structure of volatility. Second, we define the four BL input slots '
'(p, q, \u03c9, w_mkt) as candidate sets and systematically explore the 90 combinations formed by their '
'Cartesian product. In an empirical study of 617 S&P 500 constituents from 2010 to 2025 (192 months), '
'the LSTM\u2013HAR ensemble consistently outperforms the ANN in volatility forecasting accuracy, with the '
'largest gap observed during the crisis regime (R3), which includes the COVID-19 period. Translating '
'this forecasting advantage into portfolio performance, however, depends critically on mitigating the '
'large-cap concentration of the view portfolio through equal (p^eq) or risk-parity (p^rp) weighting. '
'The two slot configurations proposed in this study\u2014Ensemble-defensive (Sharpe 1.04\u20131.07), which '
'maintains a consistent low-volatility view across market regimes, and Ensemble-adaptive (Sharpe '
'1.05\u20131.10), which adapts to bull-market regimes\u2014outperform SPY (Sharpe 0.93), the 1/N portfolio '
'(0.86), the Risk Parity portfolio (0.89), and the ANN-anchor (0.95) even after accounting for '
'one-sided transaction costs of 20 basis points (bps). By examining dimension-wise marginal '
'distributions across the 90 slots and regime-conditional performance, this study provides '
'operational guidance for objective-specific slot selection in BL low-volatility strategies driven '
'by volatility forecasts.')
KW_EN = 'Black-Litterman model; volatility forecasting; LSTM; HAR; low-volatility portfolio'
RPR_EN = ('<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="바탕" '
          'w:cs="Times New Roman"/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>')
def en_runs(text):
    text = text.replace('&', '&amp;')
    out = ''; i = 0; cur = ''
    def emit(t, va=None):
        rp = RPR_EN
        if va:
            rp = rp.replace('</w:rPr>', '<w:vertAlign w:val="%s"/></w:rPr>' % va)
        return '<w:r>' + rp + '<w:t xml:space="preserve">' + t + '</w:t></w:r>'
    while i < len(text):
        c = text[i]
        if c in '^_' and i + 1 < len(text) and text[i+1].isalnum():
            if cur: out += emit(cur); cur = ''
            kind = 'superscript' if c == '^' else 'subscript'
            i += 1; scr = ''
            while i < len(text) and text[i].isalnum():
                scr += text[i]; i += 1
            out += emit(scr, kind)
        else:
            cur += c; i += 1
    if cur: out += emit(cur)
    return out
def fill_en_abstract(doc):
    n = 0
    for key, content in (('영문 초록', ABS_EN), ('영문 키워드', KW_EN)):
        for pm in re.finditer(r'<w:p\b.*?</w:p>', doc, re.S):
            p = pm.group(0)
            t = ''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', p))
            if key in t:
                op = re.match(r'<w:p\b[^>]*>', p).group(0)
                ppr = re.search(r'<w:pPr>.*?</w:pPr>', p, re.S)
                newp = op + (ppr.group(0) if ppr else '') + en_runs(content) + '</w:p>'
                doc = doc[:pm.start()] + newp + doc[pm.end():]
                n += 1
                break
    return doc, n
doc, c_abs = fill_en_abstract(doc)
print('영문 초록/키워드 삽입:%d' % c_abs)

# 교신저자 삽입 (사용자 제공 + 성명 확인: 서정욱)
CORR = ('교신저자: 서정욱 / Department of Applied Artificial Intelligence, Hanyang University, 55, '
        'Hanyangdaehak-ro, Ansan-si, 15588, Republic of Korea / E-mail: sju02051@hanyang.ac.kr')
def fill_corresponding(doc):
    for pm in re.finditer(r'<w:p\b.*?</w:p>', doc, re.S):
        p = pm.group(0)
        t = ''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', p))
        if '교신저자' in t and '작성 필요' in t:
            op = re.match(r'<w:p\b[^>]*>', p).group(0)
            ppr = re.search(r'<w:pPr>.*?</w:pPr>', p, re.S)
            rpr = ''
            rm = re.search(r'<w:r\b.*?</w:r>', p, re.S)
            if rm:
                rr = re.search(r'<w:rPr>.*?</w:rPr>', rm.group(0), re.S)
                rpr = rr.group(0) if rr else ''
            run = '<w:r>' + rpr + '<w:t xml:space="preserve">' + CORR + '</w:t></w:r>'
            doc = doc[:pm.start()] + op + (ppr.group(0) if ppr else '') + run + '</w:p>' + doc[pm.end():]
            return doc, 1
    return doc, 0
doc, c_corr = fill_corresponding(doc)
print('교신저자 삽입:%d' % c_corr)

# 사사 없음(사용자 확정) -> Acknowledgement 라벨+자리표시자 문단 제거
def remove_ack(doc):
    n = 0
    for key in ('Acknowledgement', '사사 표기'):
        for pm in re.finditer(r'<w:p\b.*?</w:p>', doc, re.S):
            p = pm.group(0)
            t = ''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', p))
            if key in t and ('작성 필요' in t or 'Acknowledgement' in t):
                doc = doc[:pm.start()] + doc[pm.end():]
                n += 1
                break
    return doc, n
doc, c_ack = remove_ack(doc)
print('사사 제거 문단:%d' % c_ack)

open(path, 'w', encoding='utf-8').write(doc)
print('부록:%s | 캡션E:%d ANN:%d 그림3:%d 2단헤더복구:%d' % (st['apx'], c_cap, c_ann, c_fig3, c_hdr))
