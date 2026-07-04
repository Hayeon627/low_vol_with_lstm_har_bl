"""§4.3 marginal 분석 — q 차원 각 옵션의 marginal Sharpe Δ (앙상블 - ANN).

각 q 옵션 (lam/raw/inv/vsp/fpm) 고정 시, 나머지 3 차원 (w_mkt × p × omega = 3×3×2 = 18 슬롯) 평균 Sharpe.
앙상블 = mat_{...}_{q}_{om}.pkl, ANN = mat_{...}_{q}_{om}_ann.pkl.
omega 코드: pap → 논문에서 err.
"""
import os
import pickle
from pathlib import Path
import numpy as np
import pandas as pd

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

RESULTS_DIR = Path('results')

REGIMES = [
    ('All',  '2010-01-01', '2025-12-31'),
    ('R1',   '2010-01-01', '2012-06-30'),
    ('R2',   '2012-07-01', '2019-12-31'),
    ('R3',   '2020-01-01', '2023-06-30'),
    ('R4',   '2023-07-01', '2025-12-31'),
]

# rf 로드 (월말 인덱스 통일)
ff3 = pd.read_csv('data/ff3_monthly.csv', parse_dates=['date']).set_index('date')
rf = ff3['rf']
# pkl ret 도 월말 timestamp 이므로 동일 인덱스로 매칭

def sharpe_subperiod(ret, rf, s, e):
    sub = ret[(ret.index >= s) & (ret.index <= e)]
    if len(sub) < 6:
        return np.nan
    rf_sub = rf.reindex(sub.index).fillna(0)
    exc = sub - rf_sub
    vol = sub.std() * np.sqrt(12)
    return float(exc.mean() * 12 / vol) if vol > 0 else np.nan

# pkl 파일 enumerate
PRIORS = ['mcap', 'eq', 'rp']
PS     = ['mcap', 'eq', 'rp']
QS     = ['lam', 'raw', 'inv', 'vsp', 'fpm']    # fpm = 논문의 ff3
OMS    = ['pap', 'he']                            # pap = 논문의 err

def load_ret(prior, p, q, om, model):
    suffix = '_ann' if model == 'ANN' else ''
    fp = RESULTS_DIR / f'mat_{prior}_{p}_{q}_{om}{suffix}.pkl'
    if not fp.exists():
        return None
    with open(fp, 'rb') as f:
        d = pickle.load(f)
    return d['ret']  # pd.Series, monthly returns

# Marginal: q 고정 → 나머지 18 슬롯 Sharpe 평균
print(f'{"q":<6s} {"regime":<6s} {"E_mean":>8s} {"A_mean":>8s} {"Δ_mean":>8s}  {"n_slots":>3s}')
print('-' * 50)

marg = {}  # marg[q][regime] = (E_mean, A_mean, Delta_mean)
for q in QS:
    marg[q] = {}
    for lbl, s, e in REGIMES:
        s_dt, e_dt = pd.Timestamp(s), pd.Timestamp(e)
        Es, As = [], []
        for prior in PRIORS:
            for p in PS:
                for om in OMS:
                    re = load_ret(prior, p, q, om, 'E')
                    ra = load_ret(prior, p, q, om, 'ANN')
                    if re is None or ra is None:
                        continue
                    Es.append(sharpe_subperiod(re, rf, s_dt, e_dt))
                    As.append(sharpe_subperiod(ra, rf, s_dt, e_dt))
        Es = [x for x in Es if not np.isnan(x)]
        As = [x for x in As if not np.isnan(x)]
        if not Es or not As:
            marg[q][lbl] = (np.nan, np.nan, np.nan, 0)
            continue
        Em, Am = float(np.mean(Es)), float(np.mean(As))
        marg[q][lbl] = (Em, Am, Em - Am, len(Es))
        print(f'{q:<6s} {lbl:<6s} {Em:>+8.4f} {Am:>+8.4f} {Em-Am:>+8.4f}  {len(Es):>3d}')
    print()

# 깔끔한 LaTeX 표
print('\n' + '='*72)
print('Marginal Sharpe by q (averaged over w_mkt × p × omega = 18 slots)')
print('='*72)
print(r'\begin{tabular}{l ccc ccc ccc ccc ccc}')
print(r'\toprule')
print(r'  & \multicolumn{3}{c}{All} & \multicolumn{3}{c}{R1} & \multicolumn{3}{c}{R2} & '
      r'\multicolumn{3}{c}{R3} & \multicolumn{3}{c}{R4} \\')
print(r'\cmidrule(lr){2-4} \cmidrule(lr){5-7} \cmidrule(lr){8-10} \cmidrule(lr){11-13} \cmidrule(lr){14-16}')
print(r'$q$ & E & A & $\Delta$ & E & A & $\Delta$ & E & A & $\Delta$ & E & A & $\Delta$ & E & A & $\Delta$ \\')
print(r'\midrule')
for q in QS:
    q_paper = 'ff3' if q == 'fpm' else q
    cells = [f'$q^{{\\mathrm{{{q_paper}}}}}$']
    for lbl, _, _ in REGIMES:
        E, A, D, n = marg[q][lbl]
        cells += [f'{E:.3f}', f'{A:.3f}', f'{D:+.3f}']
    print(' & '.join(cells) + r' \\')
print(r'\bottomrule')
print(r'\end{tabular}')
