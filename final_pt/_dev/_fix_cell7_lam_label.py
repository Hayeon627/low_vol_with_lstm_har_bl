"""Fix cell [7] — q^lam은 σ-direct가 아니라 시장 위험회피계수 λ 기반.
legend 라벨과 print 문구 정정.
"""
import json, os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

nb_path = '99_main_analysis.ipynb'
nb = json.load(open(nb_path, encoding='utf-8'))

target_idx = None
for i, c in enumerate(nb['cells']):
    if c['cell_type'] == 'code':
        src = ''.join(c['source'])
        if 'lam Q vs fpm' in src:
            target_idx = i
            break
assert target_idx is not None, '[7] cell not found'

src_lines = nb['cells'][target_idx]['source']
src_text = ''.join(src_lines)

replacements = [
    ("label='lam q (σ-direct)'", "label='lam q (λ-based)'"),
    ('→ σ-direct 는 항상 양수, fpm 만 sign-flexible',
     '→ λ-based 는 구조상 항상 양수, fpm 만 sign-flexible'),
]

for old, new in replacements:
    assert old in src_text, f'pattern not found: {old}'
    src_text = src_text.replace(old, new)

nb['cells'][target_idx]['source'] = src_text.splitlines(keepends=True)
nb['cells'][target_idx]['outputs'] = []
nb['cells'][target_idx]['execution_count'] = None

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f'Fixed cell {target_idx} - sigma-direct -> lambda-based')
