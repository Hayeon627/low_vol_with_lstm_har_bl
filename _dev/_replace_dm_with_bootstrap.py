"""Replace cell [1+] (DM + Wilcoxon) with Stationary Block Bootstrap.

Politis-Romano (1994) stationary bootstrap on the monthly cross-section
squared-error loss differential series d_t. Two-sided p-value under H0:
E[d_t] = 0.
"""
from __future__ import annotations

import json
from pathlib import Path

NB_PATH = Path(r"C:\Users\서윤범\Desktop\temp\finance_project\final_pt\99_main_analysis.ipynb")

NEW_MD = """## [1+] σ 예측 4모형 페어 — Stationary Block Bootstrap

표 2 의 LSTM / HAR / Ensemble / ANN 4 모형 6 페어 × 5 기간에 대해
손실차 시계열 (월별 cross-section squared-error 평균 차) 의 0 검정.

- **Stationary Bootstrap** (Politis & Romano, 1994): 평균 블록 길이 = `T^{1/3}` (Newey-West HAC lag 와 동일 정신)
- 시계열 자기상관 보존, 분포 가정 없음, 작은 표본 (T=30) 에서도 정확한 사이즈
- `B = 10,000` resample, two-sided p-value: `P(|d̄*| ≥ |d̄|)` under H0

`mean_d > 0` & `p < 0.05` ⇒ 우측 모형이 좌측 모형보다 squared error 가 통계적으로 유의하게 작음.

본문 표 2 별표: `* p<.05, ** p<.01, *** p<.001` (vs Ensemble 3 페어만)"""

NEW_CODE = '''# ── [1+] 4모형 페어 Stationary Block Bootstrap ────────────────────
from itertools import combinations

# 4모형 모두 가져오기 (셀 [1] 은 ensemble 만 사용)
_lstm = pd.read_csv(DATA_DIR / '03b_lstm' / 'data' / 'ensemble_predictions_stockwise.csv',
                    parse_dates=['date'])[['date','ticker','y_true',
                                           'y_pred_lstm','y_pred_har','y_pred_ensemble']]
_ann  = pd.read_csv(DATA_DIR / 'paper_ann_predictions.csv',
                    parse_dates=['date'])[['date','ticker','y_true','y_pred_ensemble']]
_lstm = _lstm.replace([np.inf,-np.inf], np.nan).dropna()
_ann  = _ann .replace([np.inf,-np.inf], np.nan).dropna()

# LSTM daily → 월말 (셀 [1] 과 동일 패턴)
_lstm['ym'] = _lstm['date'].dt.to_period('M')
_lstm_m = _lstm.sort_values('date').groupby(['ym','ticker'], as_index=False).last()
_ann['ym']  = _ann['date'].dt.to_period('M')

# 4모형 통합 panel (intersection on ym × ticker)
m4 = pd.merge(
    _lstm_m[['ym','ticker','y_pred_lstm','y_pred_har','y_pred_ensemble','y_true']]
       .rename(columns={'y_true':'y_true_l'}),
    _ann[['ym','ticker','y_pred_ensemble','y_true']]
       .rename(columns={'y_pred_ensemble':'y_pred_ann','y_true':'y_true_a'}),
    on=['ym','ticker'], how='inner',
)
m4['y_true'] = m4['y_true_a']
MODELS_4 = ['lstm','har','ensemble','ann']
PRED_4   = {m: f'y_pred_{m}' for m in MODELS_4}
print(f'4모형 통합 panel: {len(m4):,} 행 / {m4["ym"].nunique()} 개월 / {m4["ticker"].nunique()} 종목')


def _stationary_bootstrap_p(d, B=10_000, seed=42):
    """Politis-Romano (1994) stationary bootstrap two-sided p-value (H0: E[d]=0).

    Block length is Geometric(1/L) with mean L = max(2, T^{1/3}).
    """
    d = np.asarray(d, dtype=float)
    d = d[~np.isnan(d)]
    T = len(d)
    if T < 4:
        return np.nan, T
    L = max(2, int(np.floor(T ** (1/3))))
    p_geom = 1.0 / L
    rng = np.random.default_rng(seed)
    obs = d.mean()
    d0  = d - obs                                     # center under H0

    # Vectorize index construction: random starts + Bernoulli "new block" mask
    starts = rng.integers(0, T, size=(B, T))
    new_block = rng.random(size=(B, T)) < p_geom      # True = jump to new start
    new_block[:, 0] = True                            # first index is always a new start

    idx = np.empty((B, T), dtype=np.int64)
    for b in range(B):
        cur = starts[b, 0]
        idx[b, 0] = cur
        for t in range(1, T):
            if new_block[b, t]:
                cur = starts[b, t]
            else:
                cur = (cur + 1) % T
            idx[b, t] = cur
    means = d0[idx].mean(axis=1)
    p_two = float((np.abs(means) >= abs(obs)).mean())
    return p_two, T


def _loss_diff_series(df, m1, m2):
    """월별 cross-section squared-error 평균 차 (m1 − m2). >0 이면 m2 우위."""
    e1 = (df[PRED_4[m1]] - df['y_true']) ** 2
    e2 = (df[PRED_4[m2]] - df['y_true']) ** 2
    return df.assign(d=e1 - e2).groupby('ym')['d'].mean()


PERIODS_BS = [
    ('All',       None,         None),
    ('R1_회복',   '2010-01-01', '2012-06-30'),
    ('R2_확장',   '2012-07-01', '2019-12-31'),
    ('R3_위기',   '2020-01-01', '2023-06-30'),
    ('R4_정상화', '2023-07-01', '2025-12-31'),
]

print('\\n부트스트랩 계산 중 (B=10,000 × 6페어 × 5기간 = 30회)...')
rows = []
for lbl, s, e in PERIODS_BS:
    sub = m4
    if s: sub = sub[sub['ym'] >= pd.Period(s, freq='M')]
    if e: sub = sub[sub['ym'] <= pd.Period(e, freq='M')]
    for m1, m2 in combinations(MODELS_4, 2):
        d = _loss_diff_series(sub, m1, m2).dropna()
        p_two, T_use = _stationary_bootstrap_p(d.values, B=10_000)
        rows.append({
            'period':   lbl,
            'pair':     f'{m1} vs {m2}',
            'n_mo':     T_use,
            'mean_d':   float(d.mean()) if len(d) else np.nan,
            'p_two':    p_two,
            'sig':      ('***' if p_two < 0.001 else
                         '**'  if p_two < 0.01  else
                         '*'   if p_two < 0.05  else ''),
        })
bs_df = pd.DataFrame(rows)


# ── 6페어 전체 출력 (부록용) ───────────────────────────────────
print()
print('=' * 80)
print('Stationary Block Bootstrap — 6페어 × 5기간 (부록용)')
print('=' * 80)
print(f'{"period":<10s} {"pair":<22s} {"n_mo":>5s}  {"mean_d":>10s}  {"p":>8s}  sig')
print('-' * 80)
for r in rows:
    md = f'{r["mean_d"]:+.4f}' if pd.notna(r["mean_d"]) else '   nan'
    pp = f'{r["p_two"]:.4f}'   if pd.notna(r["p_two"])  else '   nan'
    print(f'{r["period"]:<10s} {r["pair"]:<22s} {r["n_mo"]:>5d}  {md:>10s}  {pp:>8s}  {r["sig"]}')


# ── 본문용: vs Ensemble 3페어만, 표 2 형식 ─────────────────────
print()
print('=' * 80)
print('본문 표 2 — vs Ensemble 별표 (* p<.05, ** p<.01, *** p<.001)')
print('=' * 80)
vs_ens = bs_df[bs_df['pair'].str.contains('ensemble')].copy()
# 페어를 "vs ensemble" 한 방향으로 통일: "{other} vs ensemble"
vs_ens['other'] = vs_ens['pair'].apply(
    lambda s: s.replace(' vs ensemble', '').replace('ensemble vs ', '')
)
# 표 2 형식: period 행 × other 열
pivot_sig = vs_ens.pivot(index='period', columns='other', values='sig').fillna('')
pivot_mean = vs_ens.pivot(index='period', columns='other', values='mean_d')
print('\\nSig (vs Ensemble):')
print(pivot_sig.reindex([p[0] for p in PERIODS_BS]).reindex(columns=['lstm','har','ann']))
print('\\nmean d (squared_error[other] - squared_error[ensemble]; >0 이면 Ensemble 우위):')
print(pivot_mean.reindex([p[0] for p in PERIODS_BS]).reindex(columns=['lstm','har','ann']).round(4))


# ── 스타일 표 (Jupyter 렌더) ───────────────────────────────────
def _hl_p(v):
    if not isinstance(v, (int, float)) or pd.isna(v): return ''
    if v < 0.001: return 'background-color: #b8e0b8; color: black; font-weight: bold'
    if v < 0.01:  return 'background-color: #d8f0d8; color: black'
    if v < 0.05:  return 'background-color: #f0f7d8; color: black'
    return ''

print()
bs_df.style.format({'mean_d':'{:+.4f}', 'p_two':'{:.4f}'}) \\
            .map(_hl_p, subset=['p_two'])
'''


def main() -> None:
    nb = json.loads(NB_PATH.read_text(encoding='utf-8'))
    cells = nb['cells']
    # cell 4 = md, cell 5 = code (DM test). Replace both.
    assert cells[4]['cell_type'] == 'markdown'
    assert cells[5]['cell_type'] == 'code'
    cells[4]['source'] = NEW_MD.splitlines(keepends=True)
    cells[5]['source'] = NEW_CODE.splitlines(keepends=True)
    cells[5]['outputs'] = []
    cells[5]['execution_count'] = None
    NB_PATH.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding='utf-8')
    print(f'Replaced cells 4 (md) and 5 (code) with Block Bootstrap version.')


if __name__ == '__main__':
    main()
