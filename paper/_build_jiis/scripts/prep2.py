import re,sys
src=sys.argv[1]; ABS=sys.argv[2]
t=open(src,encoding='utf-8').read()
t='\n'.join(ln for ln in t.split('\n') if not re.match(r'^\s*%',ln))
t=t.replace('{Figure/','{'+ABS+'/')
labelmap={}

# ---- 1) 섹션 번호 (본문/부록 분리) ----
ap=t.find('\\appendix')
def num_sec(text,app):
    cs=ss=sss=0; A=0; cur_sec=cur_sub=cur_subsub=''
    out=[]
    for ln in text.split('\n'):
        if re.match(r'\s*\\section\b|\s*\\section\*',ln):
            if app: A+=1; cur_sec='부록 '+chr(64+A)
            else: cs+=1; cur_sec=str(cs)
            ss=0; sss=0; cur_sub=cur_subsub=''
        elif re.match(r'\s*\\subsection\b|\s*\\subsection\*',ln):
            ss+=1; sss=0; cur_sub=(cur_sec+'.'+str(ss)); cur_subsub=''
        elif re.match(r'\s*\\subsubsection\b',ln):
            sss+=1; cur_subsub=cur_sec+'.'+str(ss)+'.'+str(sss)
        for lab in re.findall(r'\\label\{([^}]*)\}',ln):
            if lab.startswith(('sec:','app:')): labelmap[lab]=cur_sec
            elif lab.startswith('subsubsec:'): labelmap[lab]=cur_subsub or cur_sub or cur_sec
            elif lab.startswith('subsec:'): labelmap[lab]=cur_sub or cur_sec
        out.append(ln)
    return '\n'.join(out)
if ap<0: t=num_sec(t,False)
else: t=num_sec(t[:ap],False)+num_sec(t[ap:],True)

# ---- 2) 그림 번호 + 캡션 접두 ----
fig=[0]
def figrepl(m):
    blk=m.group(0); fig[0]+=1; n=fig[0]
    for lab in re.findall(r'\\label\{(fig:[^}]*)\}',blk): labelmap[lab]=str(n)
    blk=re.sub(r'\\caption(\[[^\]]*\])?\{', lambda mm: mm.group(0)+f'<그림 {n}> ', blk, count=1)
    return blk
t=re.sub(r'\\begin\{figure\}.*?\\end\{figure\}', figrepl, t, flags=re.S)

# ---- 3) 표 번호 (복잡표→placeholder, 단순표→캡션 접두) ----
FORCE_MARK={'tab:benchmark_sharpe','tab:benchmark_sortino','tab:benchmark_mdd','tab:benchmark_annret'}
tab=[0]; placemap=[]
def tabrepl(m):
    blk=m.group(0); tab[0]+=1; n=tab[0]
    labs=re.findall(r'\\label\{(tab:[^}]*)\}',blk)
    for lab in labs: labelmap[lab]=str(n)
    if ('cellcolor' in blk) or ('resizebox' in blk) or ((labs[0] if labs else '') in FORCE_MARK):
        placemap.append((n, labs[0] if labs else 'unlabeled'))
        return f'\n\nTABLEPLACEHOLDER{n}\n\n'
    blk=re.sub(r'\\caption(\[[^\]]*\])?\{', lambda mm: mm.group(0)+f'<표 {n}> ', blk, count=1)
    return blk
t=re.sub(r'\\begin\{table\}.*?\\end\{table\}', tabrepl, t, flags=re.S)

# ---- 4) 수식 번호 (라벨 제거 후 줄 끝에 (N)) ----
eqc=[0]
def eqenv(m):
    env=m.group(1); body=m.group(2)
    if env.startswith('align'):
        segs=re.split(r'\\\\', body); newseg=[]
        for seg in segs:
            labs=re.findall(r'\\label\{(eq:[^}]*)\}',seg)
            s2=re.sub(r'\\label\{eq:[^}]*\}','',seg)
            if labs:
                eqc[0]+=1; n=eqc[0]
                for lab in labs: labelmap[lab]=str(n)
                s2=s2.rstrip()+f' \\qquad({n})'
            newseg.append(s2)
        return '\\begin{'+env+'}'+'\\\\'.join(newseg)+'\\end{'+env+'}'
    labs=re.findall(r'\\label\{(eq:[^}]*)\}',body)
    b2=re.sub(r'\\label\{eq:[^}]*\}','',body)
    if labs:
        eqc[0]+=1; n=eqc[0]
        for lab in labs: labelmap[lab]=str(n)
        b2=b2.rstrip()+f' \\qquad({n})'
    return '\\begin{'+env+'}'+b2+'\\end{'+env+'}'
t=re.sub(r'\\begin\{(equation\*?|align\*?)\}(.*?)\\end\{\1\}', eqenv, t, flags=re.S)

# ---- 5) 본문 상호참조 치환 ----
unresolved=[]
def refrepl(m):
    cmd,lab=m.group(1),m.group(2)
    v=labelmap.get(lab)
    if v is None: unresolved.append(lab); return m.group(0)
    return f'({v})' if cmd=='eqref' else v
t=re.sub(r'\\(eqref|ref)\{([^}]*)\}', refrepl, t)

open('/tmp/src2.tex','w',encoding='utf-8').write(t)
open('/tmp/tablemap2.txt','w').write('\n'.join(f'{n}\t{lab}' for n,lab in placemap))
import json; open('/tmp/labelmap.json','w').write(json.dumps(labelmap,ensure_ascii=False))
print("라벨 매핑 수:",len(labelmap)," / 수식 번호:",eqc[0]," 그림:",fig[0]," 표:",tab[0])
print("미해결 ref:",sorted(set(unresolved)))
print("복잡표 placeholder:",[n for n,_ in placemap])
