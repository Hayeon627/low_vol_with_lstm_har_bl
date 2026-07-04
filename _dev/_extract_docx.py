"""Extract docx text and find enumeration expressions."""
import io, sys, zipfile, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

path = r'c:/Users/서윤범/Desktop/KCI논문/변동성_예측을_결합한_블랙-리터만_저변동성_포트폴리오_전략_저자정보_제외_수정본.docx'
with zipfile.ZipFile(path) as z:
    xml = z.read('word/document.xml').decode('utf-8')

text = re.sub(r'<w:p[^>]*>', '\n', xml)
text = re.sub(r'<[^>]+>', '', text)
lines = text.split('\n')

keywords = ['첫째', '둘째', '셋째', '우선', '다음으로', '마지막으로']
for i, l in enumerate(lines):
    if any(k in l for k in keywords):
        print(f'{i}: {l[:280]}')
