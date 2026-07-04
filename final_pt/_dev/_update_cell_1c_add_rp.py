"""Update [1c] — add RP P-matrix variants (LSTM-defensive-RP, LSTM-adaptive-RP).

Message: EQ ≈ RP, only mcap is the laggard. Keep EQ vs RP grouped by strategy
(defensive pair first, adaptive pair after). Visually distinguish via linestyle
(EQ solid, RP dashed, same hue family).
"""
import json, os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

nb_path = '99_main_analysis.ipynb'
nb = json.load(open(nb_path, encoding='utf-8'))

target_idx = None
for i, c in enumerate(nb['cells']):
    if c['cell_type'] == 'code':
        src = ''.join(c['source'])
        if '[1c]' in src and 'Benchmark comparison' in src:
            target_idx = i
            break
assert target_idx is not None, '[1c] cell not found'

new_code = '''# ── [1c] Benchmark comparison — EQ/RP × {defensive, adaptive} + 다지표 표 + 누적수익률 그림 ───
# [1b] 인프라 재사용: loaded, rf, ret_spy, ret_1n, ret_rp
# 메시지: mcap P만 열위, EQ ≈ RP — prior choice는 P-Q 결합 대비 부차적

CUTOFF_DT = pd.Timestamp('2025-12-31')

BL_SLOTS_C = {
    'ANN-anchor (Pyo-Lee 2018)':           'mat_mcap_mcap_fpm_pap_ann',
    'LSTM-anchor (σ swap)':                'mat_mcap_mcap_fpm_pap',
    'LSTM-defensive-EQ (eq P + lam Q)':    'mat_mcap_eq_lam_pap',
    'LSTM-defensive-RP (rp P + lam Q)':    'mat_mcap_rp_lam_pap',
    'LSTM-adaptive-EQ (eq P + fpm Q)':     'mat_mcap_eq_fpm_pap',
    'LSTM-adaptive-RP (rp P + fpm Q)':     'mat_mcap_rp_fpm_pap',
}

STRATS_C = [
    ('SPY (market)',               ret_spy),
    ('1/N (equal-weight)',         ret_1n),
    ('Risk Parity (1/σ_252d)',     ret_rp),
] + [(lbl, loaded[slot]['ret'].dropna()) for lbl, slot in BL_SLOTS_C.items()]

PERIODS_B = [
    ('All', None, None),
    ('R1', '2010-01-01','2012-06-30'),
    ('R2', '2012-07-01','2019-12-31'),
    ('R3', '2020-01-01','2023-06-30'),
    ('R4', '2023-07-01','2025-12-31'),
]

# 다지표 계산: AnnRet, AnnVol, Sharpe, Sortino, MDD, CumRet
def _full_metrics(s, st, et):
    r = s.dropna()
    if st: r = r[r.index >= st]
    if et: r = r[r.index <= et]
    if len(r) < 6: return None
    rfa = rf.reindex(r.index).fillna(0)
    exc = r - rfa
    ann_ret = (1+r).prod() ** (12/len(r)) - 1
    ann_vol = r.std() * np.sqrt(12)
    sh = float(exc.mean()*12/ann_vol) if ann_vol > 0 else np.nan
    dn = r[r<0].std() * np.sqrt(12)
    so = float(exc.mean()*12/dn) if (dn and dn>0) else np.nan
    cum = (1+r).cumprod()
    mdd = float((cum/cum.cummax() - 1).min())
    cum_ret = float(cum.iloc[-1] - 1)
    return dict(AnnRet=ann_ret, AnnVol=ann_vol, Sharpe=sh, Sortino=so, MDD=mdd, CumRet=cum_ret)

# 전략 × 기간 다지표 dict
metrics_data = {}
for label, s in STRATS_C:
    metrics_data[label] = {}
    for p, st, et in PERIODS_B:
        m = _full_metrics(s, st, et)
        if m: metrics_data[label][p] = m

# ───── 표 출력 (지표별) ─────
def _print_metric_table(title, key, fmt):
    print('\\n' + '='*120)
    print(title)
    print('='*120)
    hdr = f'{"strategy":<42s}' + ''.join(f'{p:>14s}' for p,_,_ in PERIODS_B)
    print(hdr); print('-'*len(hdr))
    for label in metrics_data:
        row = []
        for p,_,_ in PERIODS_B:
            m = metrics_data[label].get(p)
            row.append(fmt(m[key]) if m else '   —   ')
        print(f'{label:<42s}' + ''.join(f'{c:>14s}' for c in row))

_print_metric_table('Table 1: Sharpe ratio × period',         'Sharpe',  lambda v: f'{v:+.3f}')
_print_metric_table('Table 2: Sortino ratio × period',        'Sortino', lambda v: f'{v:+.3f}')
_print_metric_table('Table 3: MDD (max drawdown) × period',   'MDD',     lambda v: f'{v*100:+.2f}%')
_print_metric_table('Table 4: Annualized return × period',    'AnnRet',  lambda v: f'{v*100:+.2f}%')
_print_metric_table('Table 5: Cumulative return × period',    'CumRet',  lambda v: f'{v*100:+.1f}%')
_print_metric_table('Table 6: Annualized volatility × period','AnnVol',  lambda v: f'{v*100:.2f}%')

# ───── 그림: 누적 수익률 (log scale) + Drawdown ─────
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 9), sharex=True,
                                gridspec_kw={'height_ratios': [2.2, 1]})

# 색상: 같은 전략 family는 같은 hue, P matrix 차이는 linestyle(EQ solid, RP dashed)로 표시
style_map = {
    'SPY (market)':                       {'color':'#666666', 'ls':'-',  'lw':1.4, 'alpha':0.75},
    '1/N (equal-weight)':                 {'color':'#999999', 'ls':'--', 'lw':1.0, 'alpha':0.6},
    'Risk Parity (1/σ_252d)':             {'color':'#bbbbbb', 'ls':':',  'lw':1.0, 'alpha':0.6},
    'ANN-anchor (Pyo-Lee 2018)':          {'color':'#d62728', 'ls':'-',  'lw':1.5, 'alpha':0.85},
    'LSTM-anchor (σ swap)':               {'color':'#ff9896', 'ls':'-',  'lw':1.2, 'alpha':0.7},
    'LSTM-defensive-EQ (eq P + lam Q)':   {'color':'#1f77b4', 'ls':'-',  'lw':2.0, 'alpha':1.0},
    'LSTM-defensive-RP (rp P + lam Q)':   {'color':'#1f77b4', 'ls':'--', 'lw':2.0, 'alpha':0.85},
    'LSTM-adaptive-EQ (eq P + fpm Q)':    {'color':'#2ca02c', 'ls':'-',  'lw':2.0, 'alpha':1.0},
    'LSTM-adaptive-RP (rp P + fpm Q)':    {'color':'#2ca02c', 'ls':'--', 'lw':2.0, 'alpha':0.85},
}

REGIME_BOUNDS = [
    ('R1', pd.Timestamp('2010-01-01'), pd.Timestamp('2012-06-30')),
    ('R2', pd.Timestamp('2012-07-01'), pd.Timestamp('2019-12-31')),
    ('R3', pd.Timestamp('2020-01-01'), pd.Timestamp('2023-06-30')),
    ('R4', pd.Timestamp('2023-07-01'), pd.Timestamp('2025-12-31')),
]

# R3 음영
ax1.axvspan(pd.Timestamp('2020-01-01'), pd.Timestamp('2023-06-30'),
            color='#ffe0e0', alpha=0.5, zorder=0, label='_nolegend_')
ax2.axvspan(pd.Timestamp('2020-01-01'), pd.Timestamp('2023-06-30'),
            color='#ffe0e0', alpha=0.5, zorder=0)

# 라인 플롯
for label, s in STRATS_C:
    s2 = s[s.index <= CUTOFF_DT].dropna()
    if len(s2) < 6: continue
    cum = (1+s2).cumprod()
    style = style_map.get(label, {'color':'black','ls':'-','lw':1.0,'alpha':0.7})
    ax1.plot(cum.index, cum.values, label=label, **style)
    dd = cum / cum.cummax() - 1
    ax2.plot(dd.index, dd.values*100, **style)

# 레짐 경계 vline + 라벨
for lbl, st, et in REGIME_BOUNDS[1:]:
    ax1.axvline(st, color='gray', ls=':', lw=0.5, alpha=0.6)
    ax2.axvline(st, color='gray', ls=':', lw=0.5, alpha=0.6)
for lbl, st, et in REGIME_BOUNDS:
    mid = st + (et - st)/2
    ax1.text(mid, 1.02, lbl, transform=ax1.get_xaxis_transform(),
             ha='center', va='bottom', fontsize=10, fontweight='bold', color='dimgray')

ax1.set_title('Cumulative return (rebased = 1.0 at 2010-01) — R3 위기 구간 음영', fontweight='bold')
ax1.set_ylabel('Cumulative return (log)')
ax1.set_yscale('log')
ax1.legend(loc='upper left', fontsize=8, ncol=2, framealpha=0.9)
ax1.grid(True, alpha=0.3)

ax2.set_title('Drawdown')
ax2.set_ylabel('Drawdown (%)')
ax2.set_xlabel('Date')
ax2.axhline(0, color='black', lw=0.5)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()
'''

nb['cells'][target_idx]['source'] = new_code.splitlines(keepends=True)
nb['cells'][target_idx]['outputs'] = []
nb['cells'][target_idx]['execution_count'] = None

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f'Updated [1c] at idx {target_idx} — added RP variants (4 LSTM slots total)')
