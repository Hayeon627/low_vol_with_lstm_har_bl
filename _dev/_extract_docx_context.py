"""Extract §5 context around 활용 방안 and 한계."""
import io, sys, zipfile, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

path = r'c:/Users/서윤범/Desktop/KCI논문/변동성_예측을_결합한_블랙-리터만_저변동성_포트폴리오_전략_저자정보_제외_수정본.docx'
with zipfile.ZipFile(path) as z:
    xml = z.read('word/document.xml').decode('utf-8')

text = re.sub(r'<w:p[^>]*>', '\n', xml)
text = re.sub(r'<[^>]+>', '', text)
lines = text.split('\n')

# print §5 area
# print §5 area — look around 2660-2720
for i in range(2650, 2740):
    if lines[i].strip():
        print(f'{i}: {lines[i][:400]}')
