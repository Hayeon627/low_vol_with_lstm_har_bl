"""Insert DM test cells into 99_main_analysis.ipynb after cell [3] ([1] sigma forecast).

Adds two new cells (markdown + code) right after the current cell index 3.
"""
from __future__ import annotations

import json
from pathlib import Path

NB_PATH = Path(r"C:\Users\서윤범\Desktop\temp\finance_project\final_pt\99_main_analysis.ipynb")

MD_SOURCE = """## [1+] σ 예측 4모형 페어 — DM test + Wilcoxon

표 2 의 LSTM / HAR / Ensemble / ANN 4 모형, 6 페어 × 5 기간에 대해
손실차 시계열 (월별 cross-section squared-error 평균 차) 의 0 검정.

- **DM (Diebold-Mariano)**: HLN 작은표본 보정 + Newey-West HAC variance (lag = T^{1/3})
- **Wilcoxon signed-rank**: 비모수 강건성 보조

`mean_d > 0` & `p < 0.05` ⇒ 우측 모형이 좌측 모형보다 squared error 가 통계적으로 유의하게 작음."""

CODE_SOURCE = '''# ── [1+] 4모형 페어 DM test + Wilcoxon ────────────────────────────
from scipy.stats import wilcoxon, t as t_dist
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


def _dm_test(d_t):
    """정통 DM 검정 (HLN 보정, Newey-West HAC). d_t 는 손실차 시계열."""
    d_t = np.asarray(d_t, dtype=float)
    d_t = d_t[~np.isnan(d_t)]
    T = len(d_t)
    if T < 4:
        return np.nan, np.nan
    mu = d_t.mean()
    L  = int(np.floor(T ** (1/3)))
    gamma0 = ((d_t - mu) ** 2).mean()
    lrv = gamma0
    for k in range(1, L + 1):
        w  = 1 - k / (L + 1)
        gk = ((d_t[k:] - mu) * (d_t[:-k] - mu)).mean()
        lrv += 2 * w * gk
    if lrv <= 0:
        return np.nan, np.nan
    dm  = mu / np.sqrt(lrv / T)
    hln = np.sqrt((T + 1 - 2 + 1/T) / T) * dm        # HLN 작은표본 보정
    p   = 2 * (1 - t_dist.cdf(abs(hln), df=T - 1))
    return float(hln), float(p)


def _loss_diff_series(df, m1, m2):
    """월별 cross-section squared-error 평균 차 (m1 − m2). >0 이면 m2 우위."""
    e1 = (df[PRED_4[m1]] - df['y_true']) ** 2
    e2 = (df[PRED_4[m2]] - df['y_true']) ** 2
    return df.assign(d=e1 - e2).groupby('ym')['d'].mean()


PERIODS_DM = [
    ('All',       None,         None),
    ('R1_회복',   '2010-01-01', '2012-06-30'),
    ('R2_확장',   '2012-07-01', '2019-12-31'),
    ('R3_위기',   '2020-01-01', '2023-06-30'),
    ('R4_정상화', '2023-07-01', '2025-12-31'),
]

rows = []
for lbl, s, e in PERIODS_DM:
    sub = m4
    if s: sub = sub[sub['ym'] >= pd.Period(s, freq='M')]
    if e: sub = sub[sub['ym'] <= pd.Period(e, freq='M')]
    for m1, m2 in combinations(MODELS_4, 2):
        d = _loss_diff_series(sub, m1, m2)
        d_clean = d.dropna()
        dm_stat, dm_p = _dm_test(d_clean.values)
        if len(d_clean) >= 6:
            try:
                w_stat, w_p = wilcoxon(d_clean.values)
            except ValueError:
                w_stat, w_p = np.nan, np.nan
        else:
            w_stat, w_p = np.nan, np.nan
        rows.append({
            'period':     lbl,
            'pair':       f'{m1} vs {m2}',
            'n_mo':       int(len(d_clean)),
            'mean_d':     float(d_clean.mean()) if len(d_clean) else np.nan,
            'DM_stat':    dm_stat,
            'DM_p':       dm_p,
            'Wilcoxon_p': w_p,
        })

dm_df = pd.DataFrame(rows)

# 텍스트 출력
print()
print('=' * 92)
print('DM test + Wilcoxon — 4모형 6페어 × 5기간 (손실차 = squared_error[m1] − squared_error[m2])')
print('=' * 92)
print(f'{"period":<10s} {"pair":<22s} {"n_mo":>5s}  {"mean_d":>+10s}  '
      f'{"DM":>+8s} {"DM_p":>8s}  {"Wilc_p":>8s}')
print('-' * 92)
for r in rows:
    md  = f'{r["mean_d"]:+.4f}'  if pd.notna(r["mean_d"])  else '   nan'
    dms = f'{r["DM_stat"]:+.3f}' if pd.notna(r["DM_stat"]) else '   nan'
    dmp = f'{r["DM_p"]:.4f}'     if pd.notna(r["DM_p"])    else '   nan'
    wp  = f'{r["Wilcoxon_p"]:.4f}' if pd.notna(r["Wilcoxon_p"]) else '   nan'
    print(f'{r["period"]:<10s} {r["pair"]:<22s} {r["n_mo"]:>5d}  {md:>10s}  '
          f'{dms:>8s} {dmp:>8s}  {wp:>8s}')

# 스타일 표
def _hl_p(v):
    if not isinstance(v, (int, float)) or pd.isna(v): return ''
    if v < 0.01:  return 'background-color: #b8e0b8; color: black; font-weight: bold'
    if v < 0.05:  return 'background-color: #d8f0d8; color: black'
    if v < 0.10:  return 'background-color: #f7f0d0; color: black'
    return ''

print()
dm_df.style.format({'mean_d':'{:+.4f}', 'DM_stat':'{:+.3f}',
                    'DM_p':'{:.4f}', 'Wilcoxon_p':'{:.4f}'}) \\
            .map(_hl_p, subset=['DM_p','Wilcoxon_p'])
'''


def main() -> None:
    nb = json.loads(NB_PATH.read_text(encoding='utf-8'))
    cells = nb['cells']
    insert_at = 4  # right after current cell index 3 ([1] sigma forecast code)

    # build new cells using same metadata convention as the rest of the notebook
    md_cell = {
        'cell_type': 'markdown',
        'metadata': {},
        'source': MD_SOURCE.splitlines(keepends=True),
    }
    code_cell = {
        'cell_type': 'code',
        'execution_count': None,
        'metadata': {},
        'outputs': [],
        'source': CODE_SOURCE.splitlines(keepends=True),
    }

    cells.insert(insert_at,     md_cell)
    cells.insert(insert_at + 1, code_cell)

    NB_PATH.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding='utf-8')
    print(f'Inserted 2 cells at index {insert_at}. New total: {len(cells)} cells.')


if __name__ == '__main__':
    main()
