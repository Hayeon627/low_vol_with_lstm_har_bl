# -*- coding: utf-8 -*-
import re, sys
path = sys.argv[1]
doc = open(path, encoding='utf-8').read()
HEAVY, LIGHT = 12, 4
WIDE_NCOLS = 12
FONT_WIDE = 13
TBLW = 9298
T2_LABELS = ['RMSE ↓', 'Spearman ↑', 'Hit-Low (30%) ↑', 'Hit-High (30%) ↑']

def b(side, sz):
    return '<w:%s w:val="single" w:sz="%d" w:space="0" w:color="auto"/>' % (side, sz)
def text_of(xml):
    return ''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', xml)).strip()
def grab(inner, tag, paired=False):
    if paired:
        m = re.search(r'<w:%s\b.*?</w:%s>' % (tag, tag), inner, re.S)
    else:
        m = re.search(r'<w:%s\b[^>]*?/>' % tag, inner)
    return m.group(0) if m else ''

def tokenize(s):
    out = []; i = 0; cur = ''
    while i < len(s):
        c = s[i]
        if c in '^_' and i + 1 < len(s) and s[i+1].isalnum():
            if cur: out.append((cur, 'n')); cur = ''
            kind = 'sup' if c == '^' else 'sub'
            i += 1; scr = ''
            while i < len(s) and s[i].isalnum():
                scr += s[i]; i += 1
            out.append((scr, kind))
        else:
            cur += c; i += 1
    if cur: out.append((cur, 'n'))
    return out
def mathify(p):
    txt = ''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>', p))
    whole = txt.strip()
    if '^' not in txt and '_' not in txt and whole not in ('p', 'w'):
        return p
    runs = re.findall(r'<w:r\b.*?</w:r>', p, re.S)
    rpr = ''
    if runs:
        mm = re.search(r'<w:rPr>.*?</w:rPr>', runs[0], re.S)
        rpr = mm.group(0) if mm else ''
    segs = tokenize(txt)
    # 벡터 p/w 볼드: sup/sub 직전의 단독 p·w, 또는 셀 전체가 p·w (Notation Guide)
    segs2 = []
    for i, (t2, kind) in enumerate(segs):
        nxt = segs[i+1][1] if i + 1 < len(segs) else ''
        if kind == 'n' and nxt in ('sup', 'sub') and t2 and t2[-1] in 'pw' and (len(t2) == 1 or not t2[-2].isalnum()):
            if t2[:-1]:
                segs2.append((t2[:-1], 'n'))
            segs2.append((t2[-1], 'nb'))
        else:
            segs2.append((t2, kind))
    if len(segs2) == 1 and segs2[0][1] == 'n' and segs2[0][0].strip() in ('p', 'w'):
        segs2 = [(segs2[0][0], 'nb')]
    newruns = ''
    for t2, kind in segs2:
        if not t2:
            continue
        rp = rpr
        if kind in ('sup', 'sub'):
            va = 'superscript' if kind == 'sup' else 'subscript'
            if '</w:rPr>' in rp:
                rp = rp.replace('</w:rPr>', '<w:vertAlign w:val="%s"/></w:rPr>' % va)
            else:
                rp = '<w:rPr><w:vertAlign w:val="%s"/></w:rPr>' % va
        elif kind == 'nb':
            if '<w:b/>' not in rp:
                if '<w:rPr>' in rp:
                    rp = rp.replace('<w:rPr>', '<w:rPr><w:b/>', 1)
                else:
                    rp = '<w:rPr><w:b/></w:rPr>'
        newruns += '<w:r>' + rp + '<w:t xml:space="preserve">' + t2 + '</w:t></w:r>'
    ppr = re.search(r'<w:pPr>.*?</w:pPr>', p, re.S)
    ppr = ppr.group(0) if ppr else ''
    op = re.match(r'<w:p\b[^>]*>', p).group(0)
    return op + ppr + newruns + '</w:p>'

def label_para(txt):
    return ('<w:p><w:pPr><w:pStyle w:val="a8"/></w:pPr><w:r>'
            '<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="바탕"/>'
            '<w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr>'
            '<w:t xml:space="preserve">%s</w:t></w:r></w:p>') % txt
def set_cell_para_style(body):
    def fix(pm):
        p = pm.group(0)
        if '<w:pStyle' in p:
            p = re.sub(r'<w:pStyle w:val="[^"]*"/>', '<w:pStyle w:val="a8"/>', p, count=1)
        elif '<w:pPr>' in p:
            p = p.replace('<w:pPr>', '<w:pPr><w:pStyle w:val="a8"/>', 1)
        elif '<w:pPr/>' in p:
            p = p.replace('<w:pPr/>', '<w:pPr><w:pStyle w:val="a8"/></w:pPr>', 1)
        else:
            p = re.sub(r'(<w:p\b[^>]*>)', r'\1<w:pPr><w:pStyle w:val="a8"/></w:pPr>', p, count=1)
        return p
    body = re.sub(r'<w:p\b.*?</w:p>', fix, body, flags=re.S)
    body = re.sub(r'<w:p\b.*?</w:p>', lambda m: mathify(m.group(0)), body, flags=re.S)
    return body
def rebuild_cell(tc, vmerge, top, bottom, new_body=None, tight=False):
    m = re.search(r'<w:tcPr>(.*?)</w:tcPr>', tc, re.S)
    inner = m.group(1) if m else ''
    tcW = grab(inner, 'tcW'); gridSpan = grab(inner, 'gridSpan'); shd = grab(inner, 'shd')
    tcMar = '<w:tcMar><w:top w:w="8"/><w:bottom w:w="8"/><w:left w:w="10"/><w:right w:w="10"/></w:tcMar>' if tight else grab(inner, 'tcMar', paired=True)
    borders = ''
    if top or bottom:
        borders = '<w:tcBorders>' + (b('top', top) if top else '') + (b('bottom', bottom) if bottom else '') + '</w:tcBorders>'
    vm = ''
    if vmerge == 'restart': vm = '<w:vMerge w:val="restart"/>'
    elif vmerge == 'continue': vm = '<w:vMerge/>'
    tcpr = '<w:tcPr>' + tcW + gridSpan + vm + borders + shd + tcMar + '<w:vAlign w:val="center"/></w:tcPr>'
    if m:
        body = tc[m.end():]; body = body[:body.rfind('</w:tc>')]
    else:
        body = tc[tc.find('>')+1: tc.rfind('</w:tc>')]
    if new_body is not None: body = new_body
    body = set_cell_para_style(body)
    return '<w:tc>' + tcpr + body + '</w:tc>'
def process_table(tm):
    tbl = tm.group(0)
    trs = re.findall(r'<w:tr\b.*?</w:tr>', tbl, re.S)
    if not trs: return tbl
    grid = [re.findall(r'<w:tc>.*?</w:tc>', tr, re.S) for tr in trs]
    col0 = [text_of(cs[0]) if cs else '' for cs in grid]
    nrows = len(trs)
    ncols = tbl.count('<w:gridCol')
    if ncols == 0: ncols = max((len(cs) for cs in grid), default=1)
    wide = ncols >= WIDE_NCOLS
    shaded = ('D5E8D4' in tbl) or ('F8CECC' in tbl)
    head0 = [text_of(c) for c in (grid[0] if grid else [])]
    is_t2 = ('Metric' in head0 and 'Period' in head0 and 'Ens.' in head0)
    t2_inject = {}
    if is_t2:
        starts = [i for i in range(1, nrows) if len(grid[i]) > 1 and text_of(grid[i][1]) == 'All']
        for k, ri in enumerate(starts[:len(T2_LABELS)]):
            t2_inject[ri] = T2_LABELS[k]; col0[ri] = T2_LABELS[k]
    vmerge = ['' for _ in range(nrows)]; group_starts = []
    if is_t2 or shaded:
        i = 0
        while i < nrows:
            t = col0[i]
            if t != '':
                j = i + 1
                while j < nrows and col0[j] == '': j += 1
                span = j - i
                if span >= 2:
                    vmerge[i] = 'restart'
                    for r in range(i + 1, j): vmerge[r] = 'continue'
                    group_starts.append(i)
                i = j
            else:
                i += 1
    vmerge1 = ['' for _ in range(nrows)]; g1 = []
    if shaded and ncols >= 4:
        col1 = [text_of(cs[1]) if len(cs) > 1 else '' for cs in grid]
        i = 0
        while i < nrows:
            t = col1[i]
            if t != '':
                j = i + 1
                while j < nrows and col1[j] == '': j += 1
                if j - i >= 2:
                    vmerge1[i] = 'restart'
                    for r in range(i + 1, j): vmerge1[r] = 'continue'
                    g1.append(i)
                i = j
            else:
                i += 1
    first_group = group_starts[0] if group_starts else None
    last_header = (first_group - 1) if first_group is not None else 0
    last_row = nrows - 1
    mid_rows = set(g for g in group_starts if g != first_group)
    if g1:
        mid_rows |= set(g for g in g1 if g != g1[0])
    new_trs = []
    for ri, tr in enumerate(trs):
        cells = grid[ri]; new_cells = []
        for ci, tc in enumerate(cells):
            top = bottom = 0
            if ri == 0: top = HEAVY
            if ri == last_header: bottom = max(bottom, LIGHT)
            if ri in mid_rows: top = max(top, LIGHT)
            if ri == last_row: bottom = max(bottom, HEAVY)
            vm = vmerge[ri] if ci == 0 else (vmerge1[ri] if ci == 1 else '')
            nb = label_para(t2_inject[ri]) if (ci == 0 and ri in t2_inject) else None
            new_cells.append(rebuild_cell(tc, vm, top, bottom, nb, tight=wide))
        head = tr[:tr.find('<w:tc>')] if '<w:tc>' in tr else tr[:tr.find('</w:tr>')]
        new_trs.append(head + ''.join(new_cells) + '</w:tr>')
    inner = (re.search(r'<w:tblPr>(.*?)</w:tblPr>', tbl, re.S) or [None, ''])
    inner = inner.group(1) if hasattr(inner, 'group') else ''
    tblW = grab(inner, 'tblW') or '<w:tblW w:w="%d" w:type="dxa"/>' % TBLW
    if 'w:type="pct"' in tblW or 'w:w="0"' in tblW or wide: tblW = '<w:tblW w:w="%d" w:type="dxa"/>' % TBLW
    layout = '<w:tblLayout w:type="fixed"/>' if wide else grab(inner, 'tblLayout')
    nil = ('<w:tblBorders>'
           '<w:top w:val="none" w:sz="0" w:space="0"/><w:left w:val="none" w:sz="0" w:space="0"/>'
           '<w:bottom w:val="none" w:sz="0" w:space="0"/><w:right w:val="none" w:sz="0" w:space="0"/>'
           '<w:insideH w:val="none" w:sz="0" w:space="0"/><w:insideV w:val="none" w:sz="0" w:space="0"/>'
           '</w:tblBorders>')
    tblpr = ('<w:tblPr>' + tblW + '<w:jc w:val="center"/>' + nil + layout +
             '<w:tblLook w:val="04A0" w:firstRow="1" w:lastRow="0" w:firstColumn="0" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/></w:tblPr>')
    if wide:
        w = TBLW // ncols
        cols = [w] * ncols; cols[-1] = TBLW - w * (ncols - 1)
        tblgrid = '<w:tblGrid>' + ''.join('<w:gridCol w:w="%d"/>' % c for c in cols) + '</w:tblGrid>'
    else:
        g = re.search(r'<w:tblGrid>.*?</w:tblGrid>', tbl, re.S)
        tblgrid = g.group(0) if g else ''
    result = '<w:tbl>' + tblpr + tblgrid + ''.join(new_trs) + '</w:tbl>'
    if wide:
        result = re.sub(r'(<w:sz w:val=)"\d+"', r'\g<1>"%d"' % FONT_WIDE, result)
        result = re.sub(r'(<w:szCs w:val=)"\d+"', r'\g<1>"%d"' % FONT_WIDE, result)
    return result

doc = re.sub(r'<w:tbl>.*?</w:tbl>', process_table, doc, flags=re.S)

def set_center(p):
    if '<w:pPr>' in p:
        if '<w:jc ' in p: p = re.sub(r'<w:jc w:val="[^"]*"/>', '<w:jc w:val="center"/>', p, 1)
        else: p = p.replace('</w:pPr>', '<w:jc w:val="center"/></w:pPr>', 1)
    elif '<w:pPr/>' in p: p = p.replace('<w:pPr/>', '<w:pPr><w:jc w:val="center"/></w:pPr>', 1)
    else: p = re.sub(r'(<w:p\b[^>]*>)', r'\1<w:pPr><w:jc w:val="center"/></w:pPr>', p, 1)
    return p
def fix_caption(pm):
    p = pm.group(0); t = text_of(p).lstrip()
    is_tbl = t.startswith('&lt;표') or t.startswith('<표')
    is_fig = t.startswith('&lt;그림') or t.startswith('<그림')
    if is_tbl or is_fig:
        p = re.sub(r'<w:pStyle w:val="(TableCaption|ImageCaption|Caption)"/>', '', p)
        p = set_center(p); p = p.replace('<w:b/>', '').replace('<w:bCs/>', '')
        if is_tbl and '<w:keepNext/>' not in p and '<w:pPr>' in p:
            p = p.replace('<w:pPr>', '<w:pPr><w:keepNext/>', 1)
    return p
doc = re.sub(r'<w:p\b.*?</w:p>', fix_caption, doc, flags=re.S)
open(path, 'w', encoding='utf-8').write(doc)
print('OK tables=%d shd=%d vMergeRestart=%d superscript=%d 벡터볼드런=%d' % (
    doc.count('<w:tbl>'), doc.count('<w:shd '), doc.count('<w:vMerge w:val="restart"/>'),
    doc.count('w:val="superscript"'), doc.count('<w:rPr><w:b/>')))
