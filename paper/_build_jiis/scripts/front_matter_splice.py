# 사용법: pandoc 변환 후 unpack한 word/document.xml 경로를 인자로 전달
# python3 front_matter_splice.py <unpacked>/word/document.xml
import re,sys
f=sys.argv[1]; x=open(f,encoding='utf-8').read()
def Pp(text,bold=False,size=22,center=False):
    rpr='<w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:eastAsia="바탕" w:cs="Times New Roman"/>'
    if bold: rpr+='<w:b/><w:bCs/>'
    rpr+=f'<w:sz w:val="{size}"/><w:szCs w:val="{size}"/></w:rPr>'
    ppr='<w:pPr>'+('<w:jc w:val="center"/>' if center else '')+'</w:pPr>'
    return f'<w:p>{ppr}<w:r>{rpr}<w:t xml:space="preserve">{text}</w:t></w:r></w:p>'
def find(style=None,contains=None):
    for m in re.finditer(r'<w:p\b.*?</w:p>',x,re.S):
        b=m.group(0)
        if style and f'w:val="{style}"' not in b: continue
        if contains:
            tt=''.join(re.findall(r'<w:t[^>]*>([^<]*)</w:t>',b))
            if contains not in tt: continue
        return b
    return None
title=find(style='Title');author=find(style='Author');date=find(style='Date');abs=find(style='Abstract');kw=find(contains='주제어')
if title: x=x.replace(title,title+Pp('[Title in English — 작성 필요]',True,28,True),1)
if author: x=x.replace(author,author+Pp('[저자 소속(국문/영문) 및 E-mail — 작성 필요]',center=True)+Pp('교신저자: [성명] / [주소] / Tel: — / Fax: — / E-mail: — (작성 필요)',center=True)+Pp('Acknowledgement (사사)',bold=True)+Pp('[지원기관이 있는 경우 사사 표기 — 작성 필요]'),1)
if date: x=x.replace(date,'',1)
if abs: x=x.replace(abs,Pp('국문초록',bold=True)+abs,1)
if kw: x=x.replace(kw,kw+Pp('Abstract',bold=True)+Pp('[영문 초록 — 팀원 작성 예정]')+Pp('Key Words',bold=True)+Pp('[영문 키워드 3–5개 — 작성 필요]'),1)
open(f,'w',encoding='utf-8').write(x); print("front splice done")
