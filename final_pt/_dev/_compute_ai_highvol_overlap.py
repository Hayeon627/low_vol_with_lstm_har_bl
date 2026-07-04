"""Compute overlap: R4 LSTM 고변동 분류 (top 30%) vs AI 섹터 종목.

A4.4 framing 재구성용 실제 수치 산출:
- 월별 R4 고변동 top 30% 중 AI 섹터 비율
- 월별 R4 저변동 bottom 30% 중 AI 섹터 비율 (대조)
- ANN 기준 동일 (LSTM-only 또는 양쪽 모두)
"""
import pandas as pd
import numpy as np
import os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

R4_S = pd.Timestamp('2023-07-31')
R4_E = pd.Timestamp('2025-12-31')
AI_SECTORS = {'Information Technology', 'Technology', 'Communication Services'}

# LSTM predicted σ
lstm_raw = pd.read_csv('data/03b_lstm/data/ensemble_predictions_stockwise.csv',
                       parse_dates=['date'])[['date','ticker','y_pred_ensemble']]
lstm_raw['ym'] = lstm_raw['date'].dt.to_period('M')
lstm_m = lstm_raw.sort_values('date').groupby(['ym','ticker'], as_index=False).last()
lstm_m['date'] = lstm_m['ym'].dt.to_timestamp(how='end').apply(
    lambda d: pd.Timestamp(d.year, d.month, 1) + pd.offsets.MonthEnd(0))
lstm_pivot = lstm_m.pivot(index='date', columns='ticker', values='y_pred_ensemble')

# Sector mapping
panel = pd.read_csv('data/monthly_panel.csv', parse_dates=['date'])
sector_map = (panel.dropna(subset=['gics_sector'])
                 .groupby('ticker')['gics_sector']
                 .agg(lambda s: s.mode().iloc[0] if len(s.mode())>0 else 'Unknown')
                 .to_dict())

# R4 monthly cross-tab
r4_dates = sorted(d for d in lstm_pivot.index if R4_S <= d <= R4_E)
print(f'R4 months: {len(r4_dates)} ({r4_dates[0].date()} ~ {r4_dates[-1].date()})')
print()
print(f'{"month":<9s}{"n_stocks":>9s}{"hi30":>6s}{"hi_AI":>7s}{"hi_AI%":>8s}{"lo30":>6s}{"lo_AI":>7s}{"lo_AI%":>8s}')
print('-'*70)

hi_ai_pcts, lo_ai_pcts = [], []
hi_ai_w_pcts = []  # AI 섹터 평균 weight share (count-weighted vs equal-weighted 비교용)

for dt in r4_dates:
    sig = lstm_pivot.loc[dt].dropna()
    n_total = len(sig)
    n_b = max(1, int(n_total * 0.30))
    hi_tix = sig.nlargest(n_b).index
    lo_tix = sig.nsmallest(n_b).index
    hi_ai = sum(1 for t in hi_tix if sector_map.get(t, '') in AI_SECTORS)
    lo_ai = sum(1 for t in lo_tix if sector_map.get(t, '') in AI_SECTORS)
    hi_pct = hi_ai / n_b * 100
    lo_pct = lo_ai / n_b * 100
    hi_ai_pcts.append(hi_pct)
    lo_ai_pcts.append(lo_pct)
    print(f'{dt.strftime("%Y-%m"):<9s}{n_total:>9d}{n_b:>6d}{hi_ai:>7d}{hi_pct:>7.1f}%{n_b:>6d}{lo_ai:>7d}{lo_pct:>7.1f}%')

print('-'*70)
print(f'R4 mean - top30 hivol class: AI sector share = {np.mean(hi_ai_pcts):.1f}% (std {np.std(hi_ai_pcts):.1f}%)')
print(f'R4 mean - bot30 lovol class: AI sector share = {np.mean(lo_ai_pcts):.1f}% (std {np.std(lo_ai_pcts):.1f}%)')
print(f'    diff: {np.mean(hi_ai_pcts) - np.mean(lo_ai_pcts):+.1f}%p (hivol vs lovol)')

# 전체 universe AI 섹터 baseline
all_tix_r4 = set()
for dt in r4_dates:
    all_tix_r4.update(lstm_pivot.loc[dt].dropna().index)
ai_baseline = sum(1 for t in all_tix_r4 if sector_map.get(t, '') in AI_SECTORS) / len(all_tix_r4) * 100
print(f'\nR4 universe AI sector baseline: {ai_baseline:.1f}% ({len(all_tix_r4)} stocks total)')
print(f'  hivol-class AI ({np.mean(hi_ai_pcts):.1f}%) over baseline: +{np.mean(hi_ai_pcts) - ai_baseline:.1f}%p')
print(f'  lovol-class AI ({np.mean(lo_ai_pcts):.1f}%) under baseline: {np.mean(lo_ai_pcts) - ai_baseline:+.1f}%p')

# 역방향: AI 섹터 종목들이 hivol top 30%에 얼마나 들어가나
print('\n=== Reverse: AI sector stocks - what % are in hivol top 30%? ===')
ai_in_hi_pcts = []
ai_in_lo_pcts = []
for dt in r4_dates:
    sig = lstm_pivot.loc[dt].dropna()
    ai_tix = [t for t in sig.index if sector_map.get(t, '') in AI_SECTORS]
    if len(ai_tix) == 0: continue
    n_b = max(1, int(len(sig) * 0.30))
    hi_set = set(sig.nlargest(n_b).index)
    lo_set = set(sig.nsmallest(n_b).index)
    ai_in_hi = sum(1 for t in ai_tix if t in hi_set) / len(ai_tix) * 100
    ai_in_lo = sum(1 for t in ai_tix if t in lo_set) / len(ai_tix) * 100
    ai_in_hi_pcts.append(ai_in_hi)
    ai_in_lo_pcts.append(ai_in_lo)
print(f'R4 mean - AI stocks in hivol top 30%: {np.mean(ai_in_hi_pcts):.1f}%')
print(f'R4 mean - AI stocks in lovol bot 30%: {np.mean(ai_in_lo_pcts):.1f}%')

# Magnificent 7 specifically
M7 = ['AAPL','MSFT','GOOGL','GOOG','AMZN','NVDA','META','TSLA']
print(f'\n=== M7 sigma percentile in R4 ===')
m7_pct_avg = {}
for dt in r4_dates:
    sig = lstm_pivot.loc[dt].dropna()
    ranks = sig.rank(pct=True)  # 0=lowest sigma, 1=highest sigma
    for tk in M7:
        if tk in ranks.index:
            m7_pct_avg.setdefault(tk, []).append(ranks[tk]*100)
for tk in M7:
    if tk in m7_pct_avg:
        vals = m7_pct_avg[tk]
        print(f'  {tk:<6s}: avg sigma rank percentile = {np.mean(vals):.1f}% ({len(vals)} months)')

# 직접 비교: AI vs non-AI realized sigma in R4
print('\n=== R4 average predicted sigma: AI vs non-AI ===')
ai_sigs, nonai_sigs = [], []
for dt in r4_dates:
    sig = lstm_pivot.loc[dt].dropna()
    for t in sig.index:
        s = sector_map.get(t, '')
        if s in AI_SECTORS:
            ai_sigs.append(sig[t])
        else:
            nonai_sigs.append(sig[t])
print(f'  AI sector avg predicted sigma:     {np.mean(ai_sigs):.4f} (n={len(ai_sigs)})')
print(f'  non-AI sector avg predicted sigma: {np.mean(nonai_sigs):.4f} (n={len(nonai_sigs)})')
print(f'  ratio: AI / non-AI = {np.mean(ai_sigs)/np.mean(nonai_sigs):.2f}x')
