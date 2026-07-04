"""Replace mischaracterized 'σ-direct' terminology in 99_main_analysis.ipynb.

Investigation (bl_functions.py):
- lam/raw/inv: market 위험회피계수 λ scaling 기반 — NOT σ-direct
- vsp: vol_spread (vol_pred 사용) — σ-derived
- 4 모드의 공통 특성은 '양수 제약' (positive-constrained)이지 'σ-direct'가 아님

Replacements:
- 4-모드 umbrella term: 'σ-direct Q' → '양수 제약 Q'
- lam 단독 지칭: 'σ-direct' → 'λ-based'
"""
import json, os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

nb_path = '99_main_analysis.ipynb'
nb = json.load(open(nb_path, encoding='utf-8'))

# (cell_idx, old, new) 명시적 매핑 — 잘못된 치환 방지
edits = [
    # cell 25 — markdown header
    (25,
     '**목적**: σ-direct Q (lam/raw/inv/vsp) 와 fpm 의 본질적 차이를 데이터로 입증.',
     '**목적**: 양수 제약 Q (lam/raw/inv/vsp) 와 fpm 의 본질적 차이를 데이터로 입증.'),
    (25,
     '- σ-direct Q: λ scaling 으로 q 항상 양수 ("long low-vol / short high-vol" view 고정)',
     '- 양수 제약 Q: 구조적으로 q 항상 양수 ("long low-vol / short high-vol" view 고정)'),
    # cell 26 — lam 단독 지칭 (이미 legend는 수정됨)
    (26,
     "print('\\n참고: lam Q (σ-direct) 의 음수 비율')",
     "print('\\n참고: lam Q (λ-based) 의 음수 비율')"),
    # cell 28 — lam 단독 대조 셀
    (28,
     '# ── (1b) 대조: σ-direct Q (lam) — same family ───────────────',
     '# ── (1b) 대조: λ-based Q (lam) — same family ───────────────'),
    (28,
     "print(f'(1b) 대조 — σ-direct Q (lam) slot = {slot_lam}')",
     "print(f'(1b) 대조 — λ-based Q (lam) slot = {slot_lam}')"),
]

n_changed = 0
for cell_idx, old, new in edits:
    src_text = ''.join(nb['cells'][cell_idx]['source'])
    assert old in src_text, f'cell {cell_idx}: pattern not found: {old[:60]}'
    src_text = src_text.replace(old, new)
    nb['cells'][cell_idx]['source'] = src_text.splitlines(keepends=True)
    # code cell이면 output 재실행 필요
    if nb['cells'][cell_idx]['cell_type'] == 'code':
        nb['cells'][cell_idx]['outputs'] = []
        nb['cells'][cell_idx]['execution_count'] = None
    n_changed += 1

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f'Applied {n_changed} edits across cells 25, 26, 28')
