"""셀 [1+]: Word paste 용 TSV 출력 추가.

- 콘솔 표 (현재 형식) 유지
- LaTeX 블록 → Word TSV 블록으로 교체
- TSV: 탭 구분, "선택하여 붙여넣기 > 서식 없는 텍스트" → "텍스트를 표로 변환"
- 각 셀 = "0.4157*** (d*=+0.85)" 단일 문자열
"""
from __future__ import annotations

import json
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

NB_PATH = Path(r"C:\Users\서윤범\Desktop\temp\finance_project\final_pt\99_main_analysis.ipynb")

OLD_BLOCK = '''# ── 본문 표 2 LaTeX 출력 ─────────────────────────────────────
print()
print('=' * 100)
print('본문 표 2 LaTeX (통합)')
print('=' * 100)

def _cell_latex(row):
    raw = row['raw']
    if pd.isna(raw): return '--'
    if row['model'] == 'ensemble':
        return f'${raw:.4f}$'
    sig = row['sig'] if pd.notna(row['sig']) and row['sig'] else ''
    d   = row['d_std_adj']
    sup = f"^{{{sig}}}" if sig else ''
    d_str = f' (${d:+.2f}$)' if pd.notna(d) else ''
    return f'${raw:.4f}{sup}${d_str}'

unified['cell_tex'] = unified.apply(_cell_latex, axis=1)

_metric_latex = {'rmse':     r'RMSE $\\downarrow$',
                 'spearman': r'Spearman $\\uparrow$',
                 'hit_low':  r'Hit-Low (30\\%) $\\uparrow$',
                 'hit_high': r'Hit-High (30\\%) $\\uparrow$'}

print(r'\\begin{tabular}{l l cccc}')
print(r'\\toprule')
print(r'Metric & Period & LSTM ($d^{*}$) & HAR ($d^{*}$) & Ens. & ANN ($d^{*}$) \\\\')
print(r'\\midrule')
for metric in METRICS:
    sub = unified[unified['metric'] == metric]
    tab = sub.set_index(['period','model'])['cell_tex']
    for i, (lbl, _, _) in enumerate(PERIODS_BS):
        prefix = _metric_latex[metric] if i == 0 else ''
        cells = [tab.get((lbl, m), '--') for m in ['lstm','har','ensemble','ann']]
        print(f'{prefix} & {lbl} & ' + ' & '.join(cells) + r' \\\\')
    print(r'\\midrule')
print(r'\\bottomrule')
print(r'\\end{tabular}')
print()
print('Notes: 각 셀 = monthly aggregate raw value + sig (vs Ens) + ($d^{*}$).')
print('       $d^{*}$ = Cohen\\'s d 표준화 효과 크기, 양수 = Ens 우위 방향.')
print('       Stationary Block Bootstrap (Politis-Romano 1994; B=10,000, L=$T^{1/3}$).')'''


NEW_BLOCK = '''# ── 본문 표 2 — Word paste 용 TSV (탭 구분) ─────────────────
# 사용법: 아래 TSV 블록 복사 → 워드에서 "선택하여 붙여넣기 > 서식 없는 텍스트"
#         → 붙여넣은 텍스트 블록 선택 → "삽입 > 표 > 텍스트를 표로 변환 (구분: 탭)"
print()
print('=' * 100)
print('본문 표 2 — Word paste 용 TSV (아래 헤더 포함 전체 복사)')
print('=' * 100)

print('Metric\\tPeriod\\tLSTM\\tHAR\\tEns.\\tANN')
for metric in METRICS:
    sub = unified[unified['metric'] == metric]
    tab = sub.set_index(['period','model'])['cell']
    for i, (lbl, _, _) in enumerate(PERIODS_BS):
        m_label = _metric_label_short[metric] if i == 0 else ''
        cells = [tab.get((lbl, m), '--') for m in ['lstm','har','ensemble','ann']]
        # 셀 안 공백을 단일 공백으로 통일 (TSV paste 후 가독성)
        cells = [' '.join(c.split()) for c in cells]
        print(f'{m_label}\\t{lbl}\\t' + '\\t'.join(cells))

print()
print('=' * 100)
print('표 각주 (Word 표 아래 작은 글씨)')
print('=' * 100)
print("주: 각 셀은 'raw value (sig) (d*=...)' 형식 — Ensemble 은 baseline (sig·d* 미표시).")
print("    별표는 Ensemble 대비 차이의 통계적 유의수준 (* p<.05, ** p<.01, *** p<.001).")
print("    Stationary Block Bootstrap (Politis & Romano 1994; B=10,000, 평균 블록 길이 T^(1/3)).")
print("    d* = Cohen's d_z, paired 손실차의 평균을 표준편차로 나눈 표준화 효과 크기 (양수 = Ens 우위).")
print("    효과 크기 95% 신뢰구간 및 전체 페어 비교는 부록 표 A.x 참조.")'''


def main() -> None:
    nb = json.loads(NB_PATH.read_text(encoding='utf-8'))
    cell = nb['cells'][5]
    assert cell['cell_type'] == 'code'
    src = ''.join(cell['source'])

    if OLD_BLOCK not in src:
        print('ERROR: LaTeX block not found in cell [1+]')
        idx = src.find('LaTeX 출력')
        if idx > 0:
            print('  found marker at offset', idx)
            print('  context (300 chars):')
            print(src[idx:idx+600])
        return

    new_src = src.replace(OLD_BLOCK, NEW_BLOCK)
    assert new_src != src

    cell['source'] = new_src.splitlines(keepends=True)
    cell['outputs'] = []
    cell['execution_count'] = None
    NB_PATH.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding='utf-8')
    print('OK — 셀 [1+] LaTeX 블록 → Word TSV 블록 교체 완료.')
    print('  - 콘솔 표 (raw + sig + d*) 유지')
    print('  - Word paste 용 TSV (탭 구분) 추가')
    print('  - 워드 표 각주 안내 문구 추가')
    print('  - 부록 long-form, 스타일 표 그대로')


if __name__ == '__main__':
    main()
