"""§4.1 변동성 예측 성능 표 산출 — LSTM / HAR / Ensemble / ANN.

기존 LSTM-only 표를 4-모델로 확장. own-sample 평가 (각 모델은 자기 y_true 에 대해 측정).
- LSTM/HAR/Ens: forward 21d std (lstm csv 의 y_true)
- ANN: 월말 trailing 21d 기반 (paper_ann_predictions csv 의 y_true)

모든 메트릭(RMSE / Spearman / Hit Low30 / Hit High30) 은 monthly aggregate 통일.
각 월별 cross-section 메트릭을 계산한 뒤 기간 평균. BL 의 사용 시나리오
(매월 cross-section σ̂_t 벡터 입력) 와 정합한 통계량.
"""
import os
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.stats import spearmanr

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

LSTM_CSV = 'data/03b_lstm/data/ensemble_predictions_stockwise.csv'
ANN_CSV  = 'data/paper_ann_predictions.csv'

REGIMES = [
    ('All',       '2010-01-01', '2025-12-31'),
    ('R1 (회복)',   '2010-01-01', '2012-06-30'),
    ('R2 (확장)',   '2012-07-01', '2019-12-31'),
    ('R3 (위기)',   '2020-01-01', '2023-06-30'),
    ('R4 (AI랠리)', '2023-07-01', '2025-12-31'),
]

# ── 로드 & 정리 ─────────────────────────────────────────────
lstm = pd.read_csv(LSTM_CSV, parse_dates=['date'])
ann  = pd.read_csv(ANN_CSV,  parse_dates=['date'])

lstm = (lstm[['date','ticker','y_true','y_pred_lstm','y_pred_har','y_pred_ensemble']]
        .replace([np.inf,-np.inf], np.nan).dropna()
        .drop_duplicates(subset=['date','ticker'], keep='last'))

ann = (ann[['date','ticker','y_true','y_pred_ensemble']]
       .rename(columns={'y_pred_ensemble':'y_pred_ann'})
       .replace([np.inf,-np.inf], np.nan).dropna()
       .drop_duplicates(subset=['date','ticker'], keep='last'))

# LSTM 은 daily 라 (year, month, ticker) 별 마지막 거래일 prediction 을 월말 equiv 로 사용.
# (ANN 은 calendar month-end, LSTM 은 trading day 라 직접 isin 매칭은 주말·휴일 월말에서 빠짐)
lstm['ym'] = lstm['date'].dt.to_period('M')
lstm_me = (lstm.sort_values('date')
                .groupby(['ym','ticker'], as_index=False)
                .last())
# 캘린더 month-end 로 date 통일 (ANN 과 join 가능하게)
lstm_me['date'] = lstm_me['ym'].dt.to_timestamp(how='end').dt.normalize()
lstm_me = lstm_me.drop(columns=['ym'])

print(f'ANN month-end dates: {ann["date"].nunique():,}  | '
      f'LSTM month-end dates: {lstm_me["date"].nunique():,}')

# ── metric 함수 (Monthly aggregate 통일) ────────────────────
def metrics(df, pred_col, true_col='y_true'):
    """RMSE / Spearman / Hit Low30 / Hit High30 — 모두 monthly aggregate.

    각 월별 cross-section 메트릭을 계산한 뒤 평균. BL 의 사용 시나리오
    (매월 cross-section σ̂_t 벡터 입력) 와 정합한 통계량.
    """
    if len(df) < 5:
        return dict(rmse=np.nan, sp=np.nan, hit_low=np.nan, hit_high=np.nan, n=0, n_dates=0)
    rmse_list, sp_list, hits_low, hits_high = [], [], [], []
    for dt, g in df.groupby('date'):
        if len(g) < 20: continue
        rmse_list.append(np.sqrt(((g[pred_col] - g[true_col]) ** 2).mean()))
        sp_list  .append(spearmanr(g[pred_col], g[true_col]).statistic)
        n = max(1, int(len(g) * 0.30))
        actual_low  = set(g.nsmallest(n, true_col)['ticker'])
        actual_high = set(g.nlargest (n, true_col)['ticker'])
        pred_low    = set(g.nsmallest(n, pred_col)['ticker'])
        pred_high   = set(g.nlargest (n, pred_col)['ticker'])
        hits_low .append(len(actual_low  & pred_low ) / n)
        hits_high.append(len(actual_high & pred_high) / n)
    return dict(
        rmse     = float(np.mean(rmse_list)) if rmse_list else np.nan,
        sp       = float(np.mean(sp_list))   if sp_list   else np.nan,
        hit_low  = float(np.mean(hits_low))  if hits_low  else np.nan,
        hit_high = float(np.mean(hits_high)) if hits_high else np.nan,
        n        = len(df),
        n_dates  = df['date'].nunique(),
    )

# ── 모델별 / 레짐별 산출 ────────────────────────────────────
results = {}  # results[regime_label][model_label] = metric dict

for lbl, s, e in REGIMES:
    s_dt, e_dt = pd.Timestamp(s), pd.Timestamp(e)

    L = lstm_me[(lstm_me['date'] >= s_dt) & (lstm_me['date'] <= e_dt)]
    A = ann   [(ann   ['date'] >= s_dt) & (ann   ['date'] <= e_dt)]

    r = {}
    r['LSTM'] = metrics(L, 'y_pred_lstm')
    r['HAR']  = metrics(L, 'y_pred_har')
    r['Ens.'] = metrics(L, 'y_pred_ensemble')
    r['ANN']  = metrics(A, 'y_pred_ann')
    results[lbl] = r

    print(f'\n[{lbl}]  ({s} ~ {e})')
    print(f'  LSTM/HAR/Ens n={L.shape[0]:,} ({L["date"].nunique()} dates) | '
          f'ANN n={A.shape[0]:,} ({A["date"].nunique()} dates)')
    for m in ['LSTM','HAR','Ens.','ANN']:
        d = r[m]
        print(f'  {m:5s}: RMSE={d["rmse"]:.4f}  Sp={d["sp"]:+.4f}  '
              f'HitL30={d["hit_low"]:.4f}  HitH30={d["hit_high"]:.4f}')

# ── LaTeX 표 생성 (20-col wide form + pivoted long form 둘 다) ────────
print('\n\n' + '='*100)
print('(A) 20-col wide form (Period × {LSTM,HAR,Ens,ANN} for each of 4 metrics)')
print('='*100)
print(r'\begin{tabular}{l cccc cccc cccc cccc}')
print(r'\toprule')
print(r'        & \multicolumn{4}{c}{RMSE} & \multicolumn{4}{c}{Spearman} & '
      r'\multicolumn{4}{c}{Hit Rate (low 30\%)} & \multicolumn{4}{c}{Hit Rate (high 30\%)} \\')
print(r'\cmidrule(lr){2-5} \cmidrule(lr){6-9} \cmidrule(lr){10-13} \cmidrule(lr){14-17}')
print(r'Period & LSTM & HAR & Ens. & ANN & LSTM & HAR & Ens. & ANN & '
      r'LSTM & HAR & Ens. & ANN & LSTM & HAR & Ens. & ANN \\')
print(r'\midrule')
for lbl, _, _ in REGIMES:
    r = results[lbl]
    cells = [lbl]
    for k in ['rmse','sp','hit_low','hit_high']:
        for m in ['LSTM','HAR','Ens.','ANN']:
            v = r[m][k]
            cells.append(f'{v:.4f}')
    print(' & '.join(cells) + r' \\')
print(r'\bottomrule')
print(r'\end{tabular}')

print('\n\n' + '='*100)
print('(B) Pivoted long form (metric block × {model cols}, 4 periods within each block)')
print('='*100)
print(r'\begin{tabular}{ll cccc}')
print(r'\toprule')
print(r'Metric & Period & LSTM & HAR & Ens. & ANN \\')
print(r'\midrule')
for k, k_label in [('rmse','RMSE'), ('sp','Spearman'),
                    ('hit_low','Hit Rate (low 30\%)'),
                    ('hit_high','Hit Rate (high 30\%)')]:
    for i, (lbl, _, _) in enumerate(REGIMES):
        prefix = k_label if i == 0 else ''
        r = results[lbl]
        vals = ' & '.join(f'{r[m][k]:.4f}' for m in ['LSTM','HAR','Ens.','ANN'])
        print(f'{prefix} & {lbl} & {vals} \\\\')
    print(r'\midrule')
print(r'\bottomrule')
print(r'\end{tabular}')
