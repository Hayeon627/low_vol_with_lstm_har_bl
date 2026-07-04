"""셀 [1+]: Panel B 출력을 B-α 형식 (Δ̄ (d*) sig) 단일 표 + LaTeX 로 교체.

- 현재 (A) "Δ̄^sig" + (B) "Δ̄ [CI] sig" 두 블록을 단일 B-α 형식으로 교체
- LaTeX `tabular` 출력 추가 (논문 직접 paste 용)
- 부록 long-form, 스타일 표 그대로 유지
"""
from __future__ import annotations

import json
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

NB_PATH = Path(r"C:\Users\서윤범\Desktop\temp\finance_project\final_pt\99_main_analysis.ipynb")

OLD_BLOCK = '''print()
print('=' * 92)
print('본문 표 2 — vs Ensemble  (양수 = Ens 우위 / * p<.05, ** p<.01, *** p<.001)')
print('=' * 92)

# (A) "Δ̄^sig" 만 — 좁은 본문 표용
for metric in METRICS:
    print(f'\\n[{metric_label[metric]}]  형식: Δ̄^sig')
    sub_m = vs_ens[vs_ens['metric'] == metric].copy()
    sub_m['cell'] = sub_m.apply(
        lambda r: '' if pd.isna(r['mean_adj']) else f"{r['mean_adj']:+.4f}{r['sig']}",
        axis=1,
    )
    tab = sub_m.pivot(index='period', columns='other', values='cell')
    tab = tab.reindex([p[0] for p in PERIODS_BS]).reindex(columns=['lstm','har','ann'])
    print(tab.to_string())

# (B) "Δ̄ [CI] sig" — 넓은 본문/부록 후보
print()
print('=' * 92)
print('본문 표 2 (확장 버전) — Δ̄ [95% CI] sig')
print('=' * 92)
for metric in METRICS:
    print(f'\\n[{metric_label[metric]}]')
    sub_m = vs_ens[vs_ens['metric'] == metric].copy()
    sub_m['cell'] = sub_m.apply(
        lambda r: '' if pd.isna(r['mean_adj'])
        else f"{r['mean_adj']:+.4f} [{r['ci_lo_adj']:+.4f}, {r['ci_hi_adj']:+.4f}]{r['sig']}",
        axis=1,
    )
    tab = sub_m.pivot(index='period', columns='other', values='cell')
    tab = tab.reindex([p[0] for p in PERIODS_BS]).reindex(columns=['lstm','har','ann'])
    print(tab.to_string())'''


NEW_BLOCK = '''# Panel B — 본문 표 2 (B-α 형식: Δ̄ (d*) sig)
print()
print('=' * 92)
print('본문 표 2 Panel B — vs Ensemble  /  형식: Δ̄ (d*) sig')
print('  양수 = Ens 우위  /  * p<.05, ** p<.01, *** p<.001  /  d* = Cohen\\'s d (Δ̄/SD)')
print('=' * 92)

for metric in METRICS:
    print(f'\\n[{metric_label[metric]}]')
    sub_m = vs_ens[vs_ens['metric'] == metric].copy()
    sub_m['cell'] = sub_m.apply(
        lambda r: '' if pd.isna(r['mean_adj'])
        else f"{r['mean_adj']:+.4f}{r['sig']:<3s} (d*={r['d_std_adj']:+.2f})",
        axis=1,
    )
    tab = sub_m.pivot(index='period', columns='other', values='cell')
    tab = tab.reindex([p[0] for p in PERIODS_BS]).reindex(columns=['lstm','har','ann'])
    print(tab.to_string())


# Panel B LaTeX 출력 (논문 직접 paste 용)
print()
print('=' * 92)
print('Panel B LaTeX (\\\\begin{tabular} ... \\\\end{tabular})')
print('=' * 92)

_metric_latex = {'rmse':r'RMSE $\\downarrow$', 'spearman':r'Spearman $\\uparrow$',
                 'hit_low':r'Hit-Low (30\\%) $\\uparrow$',
                 'hit_high':r'Hit-High (30\\%) $\\uparrow$'}

def _cell_latex(row):
    if pd.isna(row['mean_adj']):
        return '--'
    sup = f"^{{{row['sig']}}}" if row['sig'] else ''
    return f"${row['mean_adj']:+.4f}{sup}$ (${row['d_std_adj']:+.2f}$)"

print(r'\\begin{tabular}{l l rrr}')
print(r'\\toprule')
print(r'Metric & Period & $\\Delta$LSTM ($d^{*}$) & $\\Delta$HAR ($d^{*}$) & $\\Delta$ANN ($d^{*}$) \\\\')
print(r'\\midrule')
for metric in METRICS:
    sub_m = vs_ens[vs_ens['metric'] == metric].copy()
    sub_m['cell_tex'] = sub_m.apply(_cell_latex, axis=1)
    tab = sub_m.set_index(['period', 'other'])['cell_tex']
    for i, (lbl, _, _) in enumerate(PERIODS_BS):
        prefix = _metric_latex[metric] if i == 0 else ''
        cells = [tab.get((lbl, other), '--') for other in ['lstm','har','ann']]
        print(f'{prefix} & {lbl} & ' + ' & '.join(cells) + r' \\\\')
    print(r'\\midrule')
print(r'\\bottomrule')
print(r'\\end{tabular}')'''


def main() -> None:
    nb = json.loads(NB_PATH.read_text(encoding='utf-8'))
    cell = nb['cells'][5]
    assert cell['cell_type'] == 'code'
    src = ''.join(cell['source'])

    if OLD_BLOCK not in src:
        print('ERROR: OLD_BLOCK not found in cell [1+]')
        # diagnostic
        idx = src.find('(A) "Δ̄^sig" 만')
        if idx > 0:
            print('  found marker "(A)" at offset', idx)
            print('  context (200 chars before, 600 after):')
            print(src[max(0,idx-200):idx+600])
        return

    new_src = src.replace(OLD_BLOCK, NEW_BLOCK)
    assert new_src != src

    cell['source'] = new_src.splitlines(keepends=True)
    cell['outputs'] = []
    cell['execution_count'] = None
    NB_PATH.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding='utf-8')
    print('OK — 셀 [1+] Panel B 출력 B-α 형식 적용 완료.')
    print('  - 콘솔 출력: Δ̄ (d*) sig 단일 형식')
    print('  - LaTeX 출력: Panel B tabular (논문 paste 용)')
    print('  - 부록 long-form, 스타일 표 그대로')


if __name__ == '__main__':
    main()
