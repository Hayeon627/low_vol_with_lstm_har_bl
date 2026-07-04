"""Compute NVDA/TSLA/META 비중 변화 — mcap vs eq/rp P-matrix.

A4.4 재구성용 — sector 대신 specific high-vol M7 종목 기여도 분석.
질문: mcap-anchor R4 spread 음수가 NVDA/TSLA/META 같은 고변동 M7 의
시가총액 가중 집중에서 비롯됐다는 걸 데이터로 받쳐주는가?
"""
import pandas as pd
import numpy as np
import pickle
import os
from pathlib import Path

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

R4_S = pd.Timestamp('2023-07-31')
R4_E = pd.Timestamp('2025-12-31')

HIGH_VOL_M7 = ['NVDA', 'TSLA', 'META']
LOW_VOL_M7  = ['AAPL', 'MSFT']
ALL_M7      = HIGH_VOL_M7 + LOW_VOL_M7 + ['AMZN', 'GOOGL']

SLOTS = {
    'mcap-anchor (mcap-mcap-fpm)': 'mat_mcap_mcap_fpm_pap',
    'mcap-eq  (mcap-eq-fpm)':       'mat_mcap_eq_fpm_pap',
    'mcap-rp  (mcap-rp-fpm)':       'mat_mcap_rp_fpm_pap',
}

# Load relevant pkl
loaded = {}
for lbl, slot in SLOTS.items():
    fp = Path('results') / f'{slot}.pkl'
    if not fp.exists():
        print(f'MISSING: {fp}'); continue
    with open(fp, 'rb') as f:
        loaded[slot] = pickle.load(f)

# LSTM predicted sigma — for hivol classification
lstm_raw = pd.read_csv('data/03b_lstm/data/ensemble_predictions_stockwise.csv',
                       parse_dates=['date'])[['date','ticker','y_pred_ensemble']]
lstm_raw['ym'] = lstm_raw['date'].dt.to_period('M')
lstm_m = lstm_raw.sort_values('date').groupby(['ym','ticker'], as_index=False).last()
lstm_m['date'] = lstm_m['ym'].dt.to_timestamp(how='end').apply(
    lambda d: pd.Timestamp(d.year, d.month, 1) + pd.offsets.MonthEnd(0))
lstm_pivot = lstm_m.pivot(index='date', columns='ticker', values='y_pred_ensemble')

# ===== (1) M7 individual avg weight per slot =====
print('='*80)
print('(1) R4 (2023-07 to 2025-12) average weight per M7 stock')
print('='*80)
print(f'{"ticker":<8s}{"mcap-anchor":>14s}{"mcap-eq":>14s}{"mcap-rp":>14s}')
print('-'*52)

m7_stats = {}
for tk in ALL_M7:
    row = [tk]
    for lbl, slot in SLOTS.items():
        if slot not in loaded:
            row.append('--'); continue
        w = loaded[slot]['weights']
        w_r4 = w[(w.index >= R4_S) & (w.index <= R4_E)]
        if tk in w_r4.columns:
            avg = w_r4[tk].dropna().mean() * 100
            row.append(f'{avg:.2f}%')
            m7_stats.setdefault(tk, {})[slot] = avg
        else:
            row.append('--')
            m7_stats.setdefault(tk, {})[slot] = 0.0
    print(f'{row[0]:<8s}{row[1]:>14s}{row[2]:>14s}{row[3]:>14s}')

# ===== (2) high-vol M7 group sum vs low-vol M7 group sum =====
print('\n' + '='*80)
print('(2) Group sum: high-vol M7 (NVDA+TSLA+META) vs low-vol M7 (AAPL+MSFT)')
print('='*80)
print(f'{"group":<28s}{"mcap-anchor":>14s}{"mcap-eq":>14s}{"mcap-rp":>14s}')
print('-'*72)

for grp_name, grp in [('high-vol M7 (NVDA+TSLA+META)', HIGH_VOL_M7),
                       ('low-vol M7 (AAPL+MSFT)', LOW_VOL_M7),
                       ('M7 total (7 stocks)', ALL_M7)]:
    row = [grp_name]
    for slot in SLOTS.values():
        if slot not in loaded:
            row.append('--'); continue
        w = loaded[slot]['weights']
        w_r4 = w[(w.index >= R4_S) & (w.index <= R4_E)]
        grp_cols = [t for t in grp if t in w_r4.columns]
        if not grp_cols:
            row.append('--'); continue
        avg_sum = w_r4[grp_cols].sum(axis=1).mean() * 100
        row.append(f'{avg_sum:.2f}%')
    print(f'{row[0]:<28s}{row[1]:>14s}{row[2]:>14s}{row[3]:>14s}')

# ===== (3) High-vol bucket weight 분해 — NVDA/TSLA/META 기여도 =====
print('\n' + '='*80)
print('(3) High-vol bucket weight 분해 (top 30% sigma): NVDA/TSLA/META 기여도')
print('='*80)
print(f'{"slot":<28s}{"total hi30":>12s}{"NVDA+TSLA+META":>18s}{"M7 hivol/total":>18s}')
print('-'*76)

for lbl, slot in SLOTS.items():
    if slot not in loaded: continue
    w = loaded[slot]['weights']
    w_r4 = w[(w.index >= R4_S) & (w.index <= R4_E)]
    total_hivols, m7_hivols = [], []
    for dt in w_r4.index:
        wt = w_r4.loc[dt].dropna()
        if dt not in lstm_pivot.index: continue
        sig = lstm_pivot.loc[dt].dropna()
        common = wt.index.intersection(sig.index)
        if len(common) < 10: continue
        sig_c = sig.loc[common]
        n_b = max(1, int(len(sig_c)*0.30))
        hi_tix = sig_c.nlargest(n_b).index
        total_hi_w = wt.loc[hi_tix].sum()
        m7_in_hi = [t for t in HIGH_VOL_M7 if t in hi_tix]
        m7_hi_w = wt.loc[m7_in_hi].sum() if m7_in_hi else 0
        total_hivols.append(total_hi_w)
        m7_hivols.append(m7_hi_w)
    total_avg = np.mean(total_hivols) * 100
    m7_avg = np.mean(m7_hivols) * 100
    share = (m7_avg / total_avg * 100) if total_avg > 0 else 0
    print(f'{lbl:<28s}{total_avg:>11.2f}%{m7_avg:>17.2f}%{share:>17.1f}%')

# ===== (4) Spread 분해 =====
print('\n' + '='*80)
print('(4) Spread (low30 - hi30) 변화: slot 비교')
print('='*80)
print(f'{"slot":<28s}{"low30 w":>10s}{"hi30 w":>10s}{"spread":>10s}')
print('-'*58)

for lbl, slot in SLOTS.items():
    if slot not in loaded: continue
    w = loaded[slot]['weights']
    w_r4 = w[(w.index >= R4_S) & (w.index <= R4_E)]
    lo_avg_w, hi_avg_w = [], []
    for dt in w_r4.index:
        wt = w_r4.loc[dt].dropna()
        if dt not in lstm_pivot.index: continue
        sig = lstm_pivot.loc[dt].dropna()
        common = wt.index.intersection(sig.index)
        if len(common) < 10: continue
        sig_c = sig.loc[common]
        n_b = max(1, int(len(sig_c)*0.30))
        lo_avg_w.append(wt.loc[sig_c.nsmallest(n_b).index].sum())
        hi_avg_w.append(wt.loc[sig_c.nlargest(n_b).index].sum())
    lo, hi = np.mean(lo_avg_w)*100, np.mean(hi_avg_w)*100
    print(f'{lbl:<28s}{lo:>9.2f}%{hi:>9.2f}%{lo-hi:>+9.2f}%')
