import re
PAPER='/sessions/sleepy-loving-thompson/mnt/low_vol_with_lstm_har_bl/paper/paper.md'
src=open(PAPER,encoding='utf-8').read()
TARGETS={}
for ln in open('/tmp/tablemap2.txt',encoding='utf-8'):
    ln=ln.rstrip('\n')
    if '\t' in ln:
        n,lab=ln.split('\t');TARGETS[int(n)]=lab.strip()
def block(label):
    for m in re.finditer(r'\\begin\{table\}.*?\\end\{table\}',src,re.S):
        if '\\label{'+label+'}' in m.group(0): return m.group(0)
def split_top(s,delim):
    out=[];d=0;cur='';i=0
    while i<len(s):
        c=s[i]
        if c=='{':d+=1;cur+=c
        elif c=='}':d-=1;cur+=c
        elif d==0 and s[i:i+len(delim)]==delim: out.append(cur);cur='';i+=len(delim);continue
        else:cur+=c
        i+=1
    out.append(cur);return out
GREEK=[('\\Delta','Δ'),('\\omega','ω'),('\\sigma','σ'),('\\pi','π'),('\\lambda','λ'),('\\tau','τ'),('\\mu','μ'),('\\Sigma','Σ'),('\\star','★'),('\\times','×'),('\\cdot','·'),('\\hat',''),('\\,',''),('\\;',''),('\\ ',' ')]
def l2t(s):
    s=re.sub(r'\\cellcolor\{[^}]*\}','',s)
    s=re.sub(r'\\textbf\{([^{}]*)\}',r'\1',s)
    s=re.sub(r'\\shortstack(\[[^\]]*\])?\{(.*?)\}',lambda m:m.group(2),s,flags=re.S)
    s=s.replace('\\\\',' ').replace('$','')
    for k,v in GREEK:s=s.replace(k,v)
    s=re.sub(r'\\(mathbf|mathrm|text|boldsymbol|mathcal|mathit)\{([^{}]*)\}',r'\2',s)
    s=re.sub(r'\^\{([^{}]*)\}',r'^\1',s);s=re.sub(r'_\{([^{}]*)\}',r'_\1',s)
    s=re.sub(r'\\[a-zA-Z]+','',s).replace('{','').replace('}','').replace('\\','')
    return re.sub(r'\s+',' ',s).strip()
def clean_cap(blk):
    i=blk.find('\\caption');b=blk.find('{',i);d=0;j=b
    while j<len(blk):
        if blk[j]=='{':d+=1
        elif blk[j]=='}':
            d-=1
            if d==0:break
        j+=1
    cap=blk[b+1:j]
    cap=re.sub(r'\\citet\{pyo2018\}','Pyo and Lee (2018)',cap)
    cap=re.sub(r'\\cite[a-z]*\{[^}]*\}','',cap)
    cap=re.sub(r'\\(ref|eqref)\{[^}]*\}','',cap)
    cap=re.sub(r'\\texttt\{([^}]*)\}',lambda m:m.group(1).replace('\\_','_'),cap)
    return l2t(cap)
def parse_cell(c):
    fill=None;bold=('\\textbf' in c) or bool(re.search(r'\\mathbf\{\s*[+\-0-9]', c))
    if 'posgreen' in c:fill='D5E8D4'
    elif 'negred' in c:fill='F8CECC'
    span=1
    mc=re.search(r'\\multicolumn\{(\d+)\}\{[^}]*\}\{(.*)\}',c,re.S)
    if mc:span=int(mc.group(1));c=mc.group(2)
    mr=re.search(r'\\multirow\{(\d+)\}\{\*\}\{(.*)\}',c,re.S)
    if mr:c=mr.group(2)
    return span,fill,bold,l2t(c)
def esc(t):return t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
def cellxml(text,span,fill,bold,sz=15):
    pr='<w:tcPr>'+(f'<w:gridSpan w:val="{span}"/>' if span>1 else '')+(f'<w:shd w:val="clear" w:color="auto" w:fill="{fill}"/>' if fill else '')+'<w:tcMar><w:top w:w="15"/><w:bottom w:w="15"/><w:left w:w="36"/><w:right w:w="36"/></w:tcMar><w:vAlign w:val="center"/></w:tcPr>'
    rpr=f'<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="바탕"/>{"<w:b/>" if bold else ""}<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/></w:rPr>'
    return f'<w:tc>{pr}<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="0" w:line="240" w:lineRule="auto"/></w:pPr><w:r>{rpr}<w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:p></w:tc>'
def gen(label,num):
    blk=block(label);captxt=clean_cap(blk)
    tab=re.search(r'\\begin\{tabular\}\{([^}]*)\}(.*?)\\end\{tabular\}',blk,re.S)
    spec=tab.group(1);body=tab.group(2);gridcols=len(re.findall(r'[lcr]',spec))
    rows=[]
    for seg in split_top(body,'\\\\'):
        seg=re.sub(r'\\(top|mid|bottom)rule','',seg);seg=re.sub(r'\\cmidrule(\([^)]*\))?\{[^}]*\}','',seg)
        if seg.strip()=='':continue
        hdr=('multicolumn' in seg) or (('All' in seg) and ('R3' in seg)) or bool(re.search(r'&\s*E\s*&\s*A\s*&',seg))
        xc=[]
        for c in split_top(seg,'&'):
            span,fill,bold,txt=parse_cell(c);xc.append(cellxml(txt,span,fill,bold or hdr))
        rows.append('<w:tr>'+''.join(xc)+'</w:tr>')
    totalw=9298;w=totalw//gridcols
    grid=''.join(f'<w:gridCol w:w="{w}"/>' for _ in range(gridcols))
    tblpr=f'<w:tblPr><w:tblW w:w="{totalw}" w:type="dxa"/><w:jc w:val="center"/><w:tblBorders><w:top w:val="single" w:sz="4" w:color="000000"/><w:bottom w:val="single" w:sz="4" w:color="000000"/><w:insideH w:val="single" w:sz="2" w:color="BBBBBB"/></w:tblBorders><w:tblLook w:val="04A0"/></w:tblPr>'
    cap=f'<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:after="40"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="바탕"/><w:b/><w:sz w:val="20"/><w:szCs w:val="20"/></w:rPr><w:t xml:space="preserve">{esc("<표 "+str(num)+"> "+captxt)}</w:t></w:r></w:p>'
    return cap+f'<w:tbl>{tblpr}<w:tblGrid>{grid}</w:tblGrid>{"".join(rows)}</w:tbl>',gridcols,len(rows)
docf='/tmp/dx7/word/document.xml';x=open(docf,encoding='utf-8').read()
for num,label in sorted(TARGETS.items()):
    xml,gc,nr=gen(label,num)
    pat=r'<w:p\b(?:(?!</w:p>).)*?TABLEPLACEHOLDER'+str(num)+r'\b(?:(?!</w:p>).)*?</w:p>'
    x2=re.sub(pat,xml,x,count=1,flags=re.S)
    print(f"표{num} {label}: cols={gc} rows={nr} {'OK' if x2!=x else 'FAIL'}")
    x=x2
open(docf,'w',encoding='utf-8').write(x)
