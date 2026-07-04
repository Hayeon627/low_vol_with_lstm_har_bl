"""셀 [1+] 본문 출력 블록 교체: Ens 우위 부호 통일 + "Δ̄^sig" 형식.

- bs_df 산출 부분 (bootstrap 자체) 은 그대로 둠
- "본문용" 블록만 교체: 부호 통일 (양수 = Ensemble 우위) + 한 셀 = "Δ̄^sig"
- 부록 long-form 은 sign convention 주석만 추가
"""
from __future__ import annotations

import json
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

NB_PATH = Path(r"C:\Users\서윤범\Desktop\temp\finance_project\final_pt\99_main_analysis.ipynb")

# 교체 대상: 본문용 블록 (vs Ensemble 별표 표)
OLD_BLOCK = '''# ── 본문용: vs Ensemble 3페어 × 4메트릭 × 5기간 별표 표 ────────
print()
print('=' * 92)
print('본문 표 2 — vs Ensemble 별표 (* p<.05, ** p<.01, *** p<.001)')
print('=' * 92)
vs_ens = bs_df[bs_df['pair'].str.contains('ensemble')].copy()
vs_ens['other'] = vs_ens['pair'].apply(
    lambda s: s.replace(' vs ensemble', '').replace('ensemble vs ', '')
)

metric_label = {'rmse':'RMSE ↓', 'spearman':'Spearman ↑',
                'hit_low':'Hit-Low (30%) ↑', 'hit_high':'Hit-High (30%) ↑'}

for metric in METRICS:
    print(f'\\n[{metric_label[metric]}]')
    sub_m = vs_ens[vs_ens['metric'] == metric]
    sig_tab = sub_m.pivot(index='period', columns='other', values='sig').fillna('')
    sig_tab = sig_tab.reindex([p[0] for p in PERIODS_BS]).reindex(columns=['lstm','har','ann'])
    md_tab  = sub_m.pivot(index='period', columns='other', values='mean_d')
    md_tab  = md_tab.reindex([p[0] for p in PERIODS_BS]).reindex(columns=['lstm','har','ann'])
    std_tab = sub_m.pivot(index='period', columns='other', values='mean_d_std')
    std_tab = std_tab.reindex([p[0] for p in PERIODS_BS]).reindex(columns=['lstm','har','ann'])
    combined = sig_tab.astype(str) + '  (' + md_tab.round(4).astype(str) + ', d*=' + std_tab.round(2).astype(str) + ')'
    print(combined.to_string())'''


NEW_BLOCK = '''# ── 본문용: vs Ensemble 3페어 — 부호 통일 (양수 = Ens 우위) ────────
# pair 표기: combinations 순서 때문에 'X vs ensemble' / 'ensemble vs X' 가 섞임
# → metric × pair 위치에 따라 mean_d 부호 의미가 갈리므로, "Ens 우위 = +" 로 통일
def _ens_adv_sign(metric, pair):
    """반환값 ±1 을 mean_d 에 곱하면 양수 = Ens 우위.

    - RMSE (낮을수록 좋음): d=m1-m2. m2=ens 이면 d>0 → Ens 우위 (+1).
                            m1=ens 이면 d>0 → 상대 우위 → flip (-1).
    - Spearman/Hit (높을수록 좋음): m1=ens 이면 d>0 → Ens 우위 (+1).
                                    m2=ens 이면 d>0 → 상대 우위 → flip (-1).
    """
    ens_is_m1 = pair.startswith('ensemble')
    if metric == 'rmse':
        return -1 if ens_is_m1 else +1
    return +1 if ens_is_m1 else -1


vs_ens = bs_df[bs_df['pair'].str.contains('ensemble')].copy()
vs_ens['sgn']        = vs_ens.apply(lambda r: _ens_adv_sign(r['metric'], r['pair']), axis=1)
vs_ens['mean_adj']   = vs_ens['mean_d']     * vs_ens['sgn']
vs_ens['d_std_adj']  = vs_ens['mean_d_std'] * vs_ens['sgn']
# CI 부호 flip 시 lo/hi 스왑
vs_ens['ci_lo_adj']  = np.where(vs_ens['sgn'] > 0, vs_ens['ci_lo'], -vs_ens['ci_hi'])
vs_ens['ci_hi_adj']  = np.where(vs_ens['sgn'] > 0, vs_ens['ci_hi'], -vs_ens['ci_lo'])
vs_ens['other']      = vs_ens['pair'].apply(
    lambda s: s.replace('ensemble vs ', '').replace(' vs ensemble', '')
)

metric_label = {'rmse':'ΔRMSE (Ens 우위 = +)',
                'spearman':'ΔSpearman (Ens 우위 = +)',
                'hit_low':'ΔHit-Low30 (Ens 우위 = +)',
                'hit_high':'ΔHit-High30 (Ens 우위 = +)'}

print()
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


def main() -> None:
    nb = json.loads(NB_PATH.read_text(encoding='utf-8'))
    cell = nb['cells'][5]
    assert cell['cell_type'] == 'code', f'cell 5 is {cell["cell_type"]}, not code'
    src = ''.join(cell['source'])

    if OLD_BLOCK not in src:
        print('ERROR: OLD_BLOCK not found in cell [1+] (cell index 5)')
        # diagnostic
        if '본문용: vs Ensemble' in src:
            idx = src.find('본문용: vs Ensemble')
            print('  found "본문용: vs Ensemble" at offset', idx)
            print('  surrounding 200 chars:', src[max(0,idx-50):idx+500])
        return

    new_src = src.replace(OLD_BLOCK, NEW_BLOCK)
    assert new_src != src

    cell['source'] = new_src.splitlines(keepends=True)
    cell['outputs'] = []
    cell['execution_count'] = None
    NB_PATH.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding='utf-8')
    print('OK — 셀 [1+] 본문 출력 블록 교체 완료.')
    print('  - 부호 통일: 양수 = Ensemble 우위')
    print('  - 출력 A: "Δ̄^sig" (좁은 표용)')
    print('  - 출력 B: "Δ̄ [95% CI] sig" (넓은 표/부록용)')
    print('  - 부록 long-form (전체 6 pair) 은 그대로 유지')


if __name__ == '__main__':
    main()
