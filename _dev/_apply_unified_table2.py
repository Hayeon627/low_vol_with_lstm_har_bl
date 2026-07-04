"""셀 [1+] Panel B 를 통합 표 (raw + sig + d*) 로 교체.

- 4모형 raw 메트릭 (monthly aggregate, m4 기반) 계산 추가
- 통합 표: Ens 는 raw 만, 나머지는 raw + sig + d*
- LaTeX tabular 출력 추가
- 부록 long-form, 스타일 표 그대로
"""
from __future__ import annotations

import json
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

NB_PATH = Path(r"C:\Users\서윤범\Desktop\temp\finance_project\final_pt\99_main_analysis.ipynb")

OLD_BLOCK = '''# Panel B — 본문 표 2 (B-α 형식: Δ̄ (d*) sig)
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


NEW_BLOCK = '''# ── 본문 표 2 (통합): raw + sig + d* ─────────────────────────
# 4모형 raw 메트릭 (monthly aggregate) 계산 — m4 재사용
def _model_metric(df, model, metric):
    pred = PRED_4[model]
    vals = []
    for ym, g in df.groupby('ym'):
        if len(g) < 20: continue
        if metric == 'rmse':
            vals.append(float(np.sqrt(((g[pred] - g['y_true'])**2).mean())))
        elif metric == 'spearman':
            vals.append(float(_sp(g[pred], g['y_true']).statistic))
        else:  # hit_low / hit_high
            n = max(1, int(len(g) * 0.30))
            if metric == 'hit_low':
                actual = set(g.nsmallest(n, 'y_true')['ticker'])
                p_set  = set(g.nsmallest(n, pred)['ticker'])
            else:
                actual = set(g.nlargest(n, 'y_true')['ticker'])
                p_set  = set(g.nlargest(n, pred)['ticker'])
            vals.append(len(actual & p_set) / n)
    return float(np.mean(vals)) if vals else np.nan

raw_rows = []
for metric in METRICS:
    for lbl, s, e in PERIODS_BS:
        sub = m4
        if s: sub = sub[sub['ym'] >= pd.Period(s, freq='M')]
        if e: sub = sub[sub['ym'] <= pd.Period(e, freq='M')]
        for model in MODELS_4:
            raw_rows.append({
                'metric': metric, 'period': lbl, 'model': model,
                'raw': _model_metric(sub, model, metric),
            })
raw_df = pd.DataFrame(raw_rows)

# vs_ens 에서 (metric, period, other) 별 sig + d_std_adj 가져와 merge
inf_stats = vs_ens[['metric','period','other','sig','d_std_adj']].copy()
inf_stats = inf_stats.rename(columns={'other':'model'})
unified = raw_df.merge(inf_stats, on=['metric','period','model'], how='left')

# 셀 포맷 (콘솔)
def _cell_console(row):
    raw = row['raw']
    if pd.isna(raw): return '--'
    if row['model'] == 'ensemble':
        return f'{raw:.4f}'
    sig = row['sig'] if pd.notna(row['sig']) and row['sig'] else ''
    d   = row['d_std_adj']
    d_str = f'(d*={d:+.2f})' if pd.notna(d) else ''
    return f'{raw:.4f}{sig:<3s} {d_str}'

unified['cell'] = unified.apply(_cell_console, axis=1)

_metric_label_short = {
    'rmse':     'RMSE ↓',
    'spearman': 'Spearman ↑',
    'hit_low':  'Hit-Low30 ↑',
    'hit_high': 'Hit-High30 ↑',
}

print()
print('=' * 100)
print('본문 표 2 (통합) — Monthly aggregate, 4 모형 × 4 메트릭 × 5 기간')
print('  Ens. = baseline / sig 별표 = vs Ens bootstrap p / d* = Cohen\\'s d (양수 = Ens 우위)')
print('  * p<.05, ** p<.01, *** p<.001')
print('=' * 100)

for metric in METRICS:
    print(f'\\n[{_metric_label_short[metric]}]')
    sub = unified[unified['metric'] == metric]
    tab = sub.pivot(index='period', columns='model', values='cell')
    tab = tab.reindex([p[0] for p in PERIODS_BS])
    tab = tab.reindex(columns=['lstm','har','ensemble','ann'])
    tab.columns = ['LSTM','HAR','Ens.','ANN']
    print(tab.to_string())


# ── 본문 표 2 LaTeX 출력 ─────────────────────────────────────
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


def main() -> None:
    nb = json.loads(NB_PATH.read_text(encoding='utf-8'))
    cell = nb['cells'][5]
    assert cell['cell_type'] == 'code'
    src = ''.join(cell['source'])

    if OLD_BLOCK not in src:
        print('ERROR: OLD_BLOCK (B-α Panel B) not found in cell [1+]')
        idx = src.find('Panel B — 본문 표 2')
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
    print('OK — 셀 [1+] Panel B → 통합 표 (raw + sig + d*) 교체 완료.')
    print('  - 4모형 raw 메트릭 (monthly aggregate) m4 기반 계산')
    print('  - 콘솔: 4메트릭 × 5기간 × 4모형 통합 표')
    print('  - LaTeX: \\\\begin{tabular} ... \\\\end{tabular} 논문 paste 용')
    print('  - 부록 long-form, 스타일 표 그대로')


if __name__ == '__main__':
    main()
