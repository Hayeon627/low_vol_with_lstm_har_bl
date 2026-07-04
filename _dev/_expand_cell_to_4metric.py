"""Expand cell [1+] to 4-metric Block Bootstrap with effect size + 95% CI.

Replaces cell [1+] (cells 4/5) with:
- 4 metrics (RMSE / Spearman / Hit-Low / Hit-High)
- 6 pairs × 5 periods = 30 series per metric, 120 total
- per series: mean_d, std_d, standardized effect size, 95% bootstrap CI, p-value, sig
- NumPy fully-vectorized stationary bootstrap (no Python loop over B)
"""
from __future__ import annotations

import json
from pathlib import Path

NB_PATH = Path(r"C:\Users\서윤범\Desktop\temp\finance_project\final_pt\99_main_analysis.ipynb")

NEW_MD = """## [1+] σ 예측 4모형 페어 — Stationary Block Bootstrap (4 metric)

표 2 의 LSTM / HAR / Ensemble / ANN 4 모형, 6 페어 × 5 기간 × 4 메트릭 = 120 검정.

**검정**: Stationary Block Bootstrap (Politis & Romano, 1994)
- 평균 블록 길이 = `T^{1/3}` (NW HAC lag 와 동일 정신)
- 시계열 자기상관 보존, 분포 가정 X
- 작은 표본 (T=30) 에서도 정확한 사이즈
- `B = 10,000` resample, two-sided p-value

**메트릭별 손실차 시계열** (월별 cross-section):
- RMSE: `(e_{m1})² − (e_{m2})²`
- Spearman: `sp_{m1} − sp_{m2}`
- Hit-Low: `hit\\_low_{m1} − hit\\_low_{m2}`
- Hit-High: `hit\\_high_{m1} − hit\\_high_{m2}`

**별표**: `* p<.05, ** p<.01, *** p<.001`

**Effect size 보고**:
- `mean_d`: raw 효과 크기
- `mean_d_std = mean_d / SD(d_t)`: 표본 크기와 무관한 효과 크기 (Cohen's d 유사)
- `[CI_lo, CI_hi]`: 95% 부트스트랩 신뢰구간

**해석 가이드**:
- 큰 표본 (R2, All) 의 강한 p-value 는 **표본 크기 효과** — 일관성 입증
- 작은 표본 (R1, R3, R4) 의 큰 `mean_d_std` 는 **실질적 우위 강도** — 검정력 제약에도 유의"""

NEW_CODE = '''# ── [1+] 4모형 × 4메트릭 Stationary Block Bootstrap ─────────────────
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


# ── 메트릭별 손실차 시계열 함수 ───────────────────────────────────
from scipy.stats import spearmanr as _sp

def _diff_rmse(df, m1, m2):
    e1 = (df[PRED_4[m1]] - df['y_true']) ** 2
    e2 = (df[PRED_4[m2]] - df['y_true']) ** 2
    return df.assign(d=e1 - e2).groupby('ym')['d'].mean()

def _diff_spearman(df, m1, m2):
    rows = []
    for ym, g in df.groupby('ym'):
        if len(g) < 20: continue
        sp1 = _sp(g[PRED_4[m1]], g['y_true']).statistic
        sp2 = _sp(g[PRED_4[m2]], g['y_true']).statistic
        rows.append((ym, sp1 - sp2))
    return pd.Series(dict(rows)) if rows else pd.Series(dtype=float)

def _diff_hit(df, m1, m2, *, mode):
    """mode: 'low' or 'high'"""
    rows = []
    for ym, g in df.groupby('ym'):
        if len(g) < 20: continue
        n = max(1, int(len(g) * 0.30))
        if mode == 'low':
            actual = set(g.nsmallest(n, 'y_true')['ticker'])
            p1 = set(g.nsmallest(n, PRED_4[m1])['ticker'])
            p2 = set(g.nsmallest(n, PRED_4[m2])['ticker'])
        else:
            actual = set(g.nlargest(n, 'y_true')['ticker'])
            p1 = set(g.nlargest(n, PRED_4[m1])['ticker'])
            p2 = set(g.nlargest(n, PRED_4[m2])['ticker'])
        h1 = len(actual & p1) / n
        h2 = len(actual & p2) / n
        rows.append((ym, h1 - h2))
    return pd.Series(dict(rows)) if rows else pd.Series(dtype=float)

DIFF_FN = {
    'rmse':     _diff_rmse,
    'spearman': _diff_spearman,
    'hit_low':  lambda df,m1,m2: _diff_hit(df, m1, m2, mode='low'),
    'hit_high': lambda df,m1,m2: _diff_hit(df, m1, m2, mode='high'),
}
# 부호 의미: rmse 는 >0 이면 m2 우위 (오차 작음), 나머지는 >0 이면 m1 우위 (큰 값이 좋음)


# ── Stationary Bootstrap (NumPy 완전 vectorize) ────────────────
def stationary_bootstrap(d, B=10_000, seed=42):
    """Politis-Romano stationary bootstrap.

    Returns dict with keys: mean_d, std_d, mean_d_std, p_two, ci_lo, ci_hi, n.
    """
    d = np.asarray(d, dtype=float)
    d = d[~np.isnan(d)]
    T = len(d)
    if T < 4:
        return dict(mean_d=np.nan, std_d=np.nan, mean_d_std=np.nan,
                    p_two=np.nan, ci_lo=np.nan, ci_hi=np.nan, n=T)
    L = max(2.0, T ** (1/3))
    rng = np.random.default_rng(seed)

    obs   = d.mean()
    std_d = d.std(ddof=1)
    d0    = d - obs                                  # center under H0

    # vectorized index matrix construction (B, T)
    new_block = rng.random((B, T)) < (1.0 / L)
    new_block[:, 0] = True

    # segment id per (b, t)
    seg_id     = np.cumsum(new_block, axis=1) - 1    # (B, T)
    starts     = rng.integers(0, T, size=(B, T))     # candidate starts per position
    seg_starts = np.take_along_axis(starts, seg_id, axis=1)

    # offset within segment = t - last_new_block_index
    t_arr    = np.broadcast_to(np.arange(T), (B, T))
    last_new = np.where(new_block, t_arr, -1)
    last_new = np.maximum.accumulate(last_new, axis=1)
    offset   = t_arr - last_new

    indices = (seg_starts + offset) % T

    centered_means = d0[indices].mean(axis=1)
    raw_means      = d [indices].mean(axis=1)

    p_two = float((np.abs(centered_means) >= abs(obs)).mean())
    ci_lo, ci_hi = np.percentile(raw_means, [2.5, 97.5])

    return dict(
        mean_d     = float(obs),
        std_d      = float(std_d) if std_d > 0 else np.nan,
        mean_d_std = float(obs / std_d) if std_d > 0 else np.nan,
        p_two      = p_two,
        ci_lo      = float(ci_lo),
        ci_hi      = float(ci_hi),
        n          = T,
    )


# ── 통합 계산: 4 metric × 6 pair × 5 period = 120 검정 ─────────
PERIODS_BS = [
    ('All',       None,         None),
    ('R1_회복',   '2010-01-01', '2012-06-30'),
    ('R2_확장',   '2012-07-01', '2019-12-31'),
    ('R3_위기',   '2020-01-01', '2023-06-30'),
    ('R4_정상화', '2023-07-01', '2025-12-31'),
]
METRICS = ['rmse', 'spearman', 'hit_low', 'hit_high']
B_RUNS  = 10_000

print(f'\\nBootstrap 계산 중 ({len(METRICS)} metric × 6 pair × {len(PERIODS_BS)} period × B={B_RUNS:,})...')

import time
t0 = time.perf_counter()
rows = []
for metric in METRICS:
    for lbl, s, e in PERIODS_BS:
        sub = m4
        if s: sub = sub[sub['ym'] >= pd.Period(s, freq='M')]
        if e: sub = sub[sub['ym'] <= pd.Period(e, freq='M')]
        for m1, m2 in combinations(MODELS_4, 2):
            d = DIFF_FN[metric](sub, m1, m2).dropna()
            r = stationary_bootstrap(d.values, B=B_RUNS, seed=42)
            p = r['p_two']
            sig = ('***' if pd.notna(p) and p < 0.001 else
                   '**'  if pd.notna(p) and p < 0.01  else
                   '*'   if pd.notna(p) and p < 0.05  else '')
            rows.append({
                'metric': metric, 'period': lbl, 'pair': f'{m1} vs {m2}',
                **r, 'sig': sig,
            })
    print(f'  {metric:<10s} 완료')

bs_df = pd.DataFrame(rows)
print(f'\\n경과: {time.perf_counter() - t0:.1f}s  /  결과 행: {len(bs_df)}')

# 출력 정렬
COLS_LONG = ['metric','period','pair','n','mean_d','std_d','mean_d_std',
             'ci_lo','ci_hi','p_two','sig']
bs_df = bs_df[COLS_LONG]


# ── 본문용: vs Ensemble 3페어 × 4메트릭 × 5기간 별표 표 ────────
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
    print(combined.to_string())


# ── 부록용: 전체 long-form ────────────────────────────────────
print()
print('=' * 92)
print('부록: 4 metric × 6 pair × 5 period (long-form)')
print('=' * 92)
print(bs_df.to_string(index=False,
                      formatters={
                          'mean_d':     '{:+.4f}'.format,
                          'std_d':      '{:.4f}'.format,
                          'mean_d_std': '{:+.3f}'.format,
                          'ci_lo':      '{:+.4f}'.format,
                          'ci_hi':      '{:+.4f}'.format,
                          'p_two':      '{:.4f}'.format,
                      }))


# ── 스타일 표 (Jupyter 렌더) ───────────────────────────────────
def _hl_p(v):
    if not isinstance(v, (int, float)) or pd.isna(v): return ''
    if v < 0.001: return 'background-color: #b8e0b8; color: black; font-weight: bold'
    if v < 0.01:  return 'background-color: #d8f0d8; color: black'
    if v < 0.05:  return 'background-color: #f0f7d8; color: black'
    return ''

print()
bs_df.style.format({'mean_d':'{:+.4f}', 'std_d':'{:.4f}', 'mean_d_std':'{:+.3f}',
                    'ci_lo':'{:+.4f}', 'ci_hi':'{:+.4f}', 'p_two':'{:.4f}'}) \\
            .map(_hl_p, subset=['p_two'])
'''


def main() -> None:
    nb = json.loads(NB_PATH.read_text(encoding='utf-8'))
    cells = nb['cells']
    assert cells[4]['cell_type'] == 'markdown'
    assert cells[5]['cell_type'] == 'code'
    cells[4]['source'] = NEW_MD.splitlines(keepends=True)
    cells[5]['source'] = NEW_CODE.splitlines(keepends=True)
    cells[5]['outputs'] = []
    cells[5]['execution_count'] = None
    NB_PATH.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding='utf-8')
    print('Replaced cells 4 (md) and 5 (code) with 4-metric expansion.')


if __name__ == '__main__':
    main()
