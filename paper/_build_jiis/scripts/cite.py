import re
BIB=open('/sessions/sleepy-loving-thompson/mnt/low_vol_with_lstm_har_bl/paper/references.bib',encoding='utf-8').read()
import sys
SRC=sys.argv[1] if len(sys.argv)>1 else '/sessions/sleepy-loving-thompson/mnt/low_vol_with_lstm_har_bl/paper/_build_jiis/scripts/src2.tex'
t=open(SRC,encoding='utf-8').read()
def parse(bib):
    res={};i=0;n=len(bib)
    while True:
        at=bib.find('@',i)
        if at<0:break
        b=bib.find('{',at);typ=bib[at+1:b].strip().lower();d=0;j=b
        while j<n:
            if bib[j]=='{':d+=1
            elif bib[j]=='}':
                d-=1
                if d==0:break
            j+=1
        body=bib[b+1:j];key=body.split(',',1)[0].strip();rest=body[len(key)+1:];fields={}
        for fm in re.finditer(r'(\w+)\s*=\s*',rest):
            fn=fm.group(1).lower();vs=fm.end()
            if vs<len(rest) and rest[vs]=='{':
                dd=0;p=vs
                while p<len(rest):
                    if rest[p]=='{':dd+=1
                    elif rest[p]=='}':
                        dd-=1
                        if dd==0:break
                    p+=1
                val=rest[vs+1:p]
            else:
                p=rest.find(',',vs);val=rest[vs:p if p>=0 else len(rest)]
            fields[fn]=val.strip()
        res[key]=(typ,fields);i=j+1
    return res
ent=parse(BIB)
ACC={r'\"u':'ü',r'\"o':'ö',r'\"a':'ä',r"\'e":'é',r"\'i":'í',r"\'a":'á',r"\'o":'ó',r'\^o':'ô',r'\^e':'ê',r'\`e':'è'}
def clean(s):
    for k,v in ACC.items(): s=s.replace(k,v)
    s=s.replace('\\&','&').replace('---','—').replace('--','–');s=re.sub(r'[{}]','',s);return re.sub(r'\s+',' ',s).strip()
SMALL={'of','the','and','in','on','for','to','a','an','with','at','by','from','as','vs'}
def titlecase(s):
    ws=s.split();o=[]
    for i,w in enumerate(ws):
        o.append(w if (i>0 and w.lower() in SMALL) else (w[:1].upper()+w[1:] if w else w))
    return ' '.join(o)
def sa(f): return [a.strip() for a in re.split(r'\s+and\s+',f.replace('\n',' ')) if a.strip()]
def last_of(a):
    a=clean(a);return a.split(',',1)[0].strip() if ',' in a else (a.split()[-1] if a.split() else a)
def intext(af,paren=False):
    L=[last_of(a) for a in sa(af)];sep='&' if paren else 'and'
    return L[0] if len(L)==1 else (f'{L[0]} {sep} {L[1]}' if len(L)==2 else f'{L[0]} et al.')
def inits(g): return ' '.join(tok[0].upper()+'.' for tok in re.split(r'[ .]+',clean(g)) if tok)
def refau(af):
    ps=[]
    for a in sa(af):
        a=clean(a)
        if ',' in a:
            l,fi=a.split(',',1);ps.append(f'{l.strip()}, {inits(fi)}')
        else:
            tk=a.split();ps.append(f'{tk[-1]}, {inits(" ".join(tk[:-1]))}' if len(tk)>1 else a)
    return ps[0] if len(ps)==1 else ', '.join(ps[:-1])+', & '+ps[-1]
def fmt(k):
    typ,f=ent[k];au=refau(f.get('author',''));yr=clean(f.get('year','n.d.'));ti=clean(f.get('title',''))
    if typ=='article':
        j=titlecase(clean(f.get('journal','')));v=clean(f.get('volume',''));no=clean(f.get('number',''));pg=clean(f.get('pages',''))
        s=f'{au} ({yr}). {ti}. \\textit{{{j}, {v}}}' if v else f'{au} ({yr}). {ti}. \\textit{{{j}}}'
        if no:s+=f'({no})'
        if pg:s+=f', {pg}'
        s+='.'
        if f.get('doi'):s+=f' https://doi.org/{clean(f["doi"])}'
        return s
    if typ=='book': return f'{au} ({yr}). \\textit{{{ti}}}. {clean(f.get("publisher",""))}.'
    if typ=='techreport': return f'{au} ({yr}). {ti}. {clean(f.get("institution",""))}.'
    return f'{au} ({yr}). {ti}.'
cited=set();missing=set()
def rc(m):
    cmd=m.group(1);keys=[k.strip() for k in m.group(2).split(',')];out=[];paren=(cmd!='citet')
    for k in keys:
        cited.add(k)
        if k not in ent: missing.add(k);out.append(('['+k+'? — bib 누락]','',));continue
        out.append((intext(ent[k][1].get('author',''),paren),clean(ent[k][1].get('year',''))))
    if cmd=='citet': return ', '.join(f'{a} ({y})' if y else a for a,y in out)
    if cmd=='citealp': return '; '.join(f'{a}, {y}' if y else a for a,y in out)
    return '('+'; '.join(f'{a}, {y}' if y else a for a,y in out)+')'
t=re.sub(r'\\(citet|citep|citealp|cite)\{([^}]*)\}',rc,t)
def sk(k): return last_of(sa(ent[k][1].get('author',''))[0]).lower()
bl=sorted([k for k in cited if k in ent],key=sk)
bib='\\section*{참고문헌}\n\n[국외 문헌]\n\n'+'\n\n'.join(fmt(k) for k in bl)+'\n'
t=re.sub(r'\\bibliographystyle\{[^}]*\}','',t);t=t.replace('\\bibliography{references}',bib)
open('/tmp/src3.tex','w',encoding='utf-8').write(t)
print("참고문헌(국외):",len(bl)," 누락:",sorted(missing))
