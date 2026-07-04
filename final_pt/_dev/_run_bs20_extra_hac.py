"""bs20_extra_hac.pkl — 4 Ensemble 옵션 vs Ensemble-anchor 페어 SBB HAC 검정.

- 5 기간 × 4 옵션 슬롯 = 20 검정
- Ledoit & Wolf (2008) HAC studentized Boot-TS (bs100_hac와 동일 방법)
- 저장: outputs/99_main_analysis/bs20_extra_hac.pkl
"""
from __future__ import annotations

import io
import pickle
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_DIR = Path(r"C:\Users\서윤범\Desktop\temp\finance_project\final_pt")
RESULTS_DIR = BASE_DIR / 'results'
DATA_DIR = BASE_DIR / 'data'
OUT_DIR = BASE_DIR / 'outputs' / '99_main_analysis'

CUTOFF = '2025-12-31'
B_RUNS = 10_000

BASE_SLOTS = {
    'Ensemble-defensive (p^eq, q^lam)': 'mat_mcap_eq_lam_pap',
    'Ensemble-defensive (p^rp, q^lam)': 'mat_mcap_rp_lam_pap',
    'Ensemble-adaptive (p^eq, q^ff3)':  'mat_mcap_eq_fpm_pap',
    'Ensemble-adaptive (p^rp, q^ff3)':  'mat_mcap_rp_fpm_pap',
}
ENS_ANCHOR_KEY = 'mat_mcap_mcap_fpm_pap'

PERIODS = [
    ('All', None, None),
    ('R1',  '2010-01-01', '2012-06-30'),
    ('R2',  '2012-07-01', '2019-12-31'),
    ('R3',  '2020-01-01', '2023-06-30'),
    ('R4',  '2023-07-01', '2025-12-31'),
]


def _sharpe_sc(r, rfa):
    ex = r - rfa
    s = np.std(r, ddof=1)
    return float(ex.mean() * 12 / (s * np.sqrt(12))) if s > 0 else np.nan


def _sharpe_b(r_b, rf_b):
    ex = r_b - rf_b
    mu = ex.mean(axis=1) * 12
    s = r_b.std(axis=1, ddof=1) * np.sqrt(12)
    return np.where(s > 0, mu / s, np.nan)


def _hac_cov(z, lag):
    T = z.shape[0]
    z_dm = z - z.mean(axis=0)
    Gamma = z_dm.T @ z_dm / T
    for h in range(1, lag + 1):
        w = 1.0 - h / (lag + 1)
        Gamma_h = z_dm[h:].T @ z_dm[:-h] / T
        Gamma = Gamma + w * (Gamma_h + Gamma_h.T)
    return Gamma


def _hac_cov_batch(z_b, lag):
    B, T, k = z_b.shape
    z_dm = z_b - z_b.mean(axis=1, keepdims=True)
    Gamma = np.einsum('bti,btj->bij', z_dm, z_dm) / T
    for h in range(1, lag + 1):
        w = 1.0 - h / (lag + 1)
        Gamma_h = np.einsum('bti,btj->bij', z_dm[:, h:, :], z_dm[:, :-h, :]) / T
        Gamma = Gamma + w * (Gamma_h + Gamma_h.transpose(0, 2, 1))
    return Gamma


def _sr_gradient(mu_L, mu_A, gam_L, gam_A, s_L, s_A):
    return np.array([
         gam_L / s_L**3,
        -gam_A / s_A**3,
        -mu_L / (2 * s_L**3),
         mu_A / (2 * s_A**3),
    ])


def paired_sbb_hac(rL, rA, rfa, B=10_000, seed=42):
    rL_arr = np.asarray(rL.values, dtype=float)
    rA_arr = np.asarray(rA.values, dtype=float)
    rf_arr = np.asarray(rfa.values, dtype=float)
    T = len(rL_arr)
    nan_ret = dict(delta_obs=np.nan, t_obs=np.nan, se_obs=np.nan,
                   ci_lo=np.nan, ci_hi=np.nan, p_two=np.nan, n=T, hac_lag=0)
    if T < 6:
        return nan_ret

    SR_L = _sharpe_sc(rL_arr, rf_arr)
    SR_A = _sharpe_sc(rA_arr, rf_arr)
    d_obs = SR_L - SR_A
    if pd.isna(d_obs):
        return nan_ret

    lag = max(int(np.floor(T ** (1/3))), 1)

    eL = rL_arr - rf_arr
    eA = rA_arr - rf_arr
    mu_L = eL.mean();  mu_A = eA.mean()
    gam_L = (eL**2).mean();  gam_A = (eA**2).mean()
    s_L2 = gam_L - mu_L**2;  s_A2 = gam_A - mu_A**2
    if s_L2 <= 0 or s_A2 <= 0:
        return {**nan_ret, 'delta_obs': float(d_obs), 'hac_lag': lag}
    s_L = np.sqrt(s_L2);  s_A = np.sqrt(s_A2)

    z_obs = np.column_stack([eL, eA, eL**2, eA**2])
    Psi_obs = _hac_cov(z_obs, lag)

    g_obs = _sr_gradient(mu_L, mu_A, gam_L, gam_A, s_L, s_A)
    var_m_obs = float(g_obs @ Psi_obs @ g_obs) / T
    if var_m_obs <= 0:
        return {**nan_ret, 'delta_obs': float(d_obs), 'hac_lag': lag}
    SE_obs = np.sqrt(var_m_obs) * np.sqrt(12)
    t_obs = d_obs / SE_obs

    L_block = max(2.0, T ** (1/3))
    rng = np.random.default_rng(seed)
    new_block = rng.random((B, T)) < (1.0 / L_block)
    new_block[:, 0] = True
    seg_id = np.cumsum(new_block, axis=1) - 1
    starts = rng.integers(0, T, size=(B, T))
    seg_starts = np.take_along_axis(starts, seg_id, axis=1)
    t_arr = np.broadcast_to(np.arange(T), (B, T))
    last_new = np.where(new_block, t_arr, -1)
    last_new = np.maximum.accumulate(last_new, axis=1)
    offset = t_arr - last_new
    indices = (seg_starts + offset) % T

    rL_b = rL_arr[indices]
    rA_b = rA_arr[indices]
    rf_b = rf_arr[indices]
    eL_b = rL_b - rf_b
    eA_b = rA_b - rf_b

    sL_b = _sharpe_b(rL_b, rf_b)
    sA_b = _sharpe_b(rA_b, rf_b)
    delta_b = sL_b - sA_b

    mu_L_b = eL_b.mean(axis=1)
    mu_A_b = eA_b.mean(axis=1)
    gam_L_b = (eL_b**2).mean(axis=1)
    gam_A_b = (eA_b**2).mean(axis=1)
    s_L2_b = gam_L_b - mu_L_b**2
    s_A2_b = gam_A_b - mu_A_b**2
    valid_std = (s_L2_b > 0) & (s_A2_b > 0)
    s_L_b = np.where(valid_std, np.sqrt(np.maximum(s_L2_b, 0)), np.nan)
    s_A_b = np.where(valid_std, np.sqrt(np.maximum(s_A2_b, 0)), np.nan)

    with np.errstate(divide='ignore', invalid='ignore'):
        g_b = np.stack([
             gam_L_b / s_L_b**3,
            -gam_A_b / s_A_b**3,
            -mu_L_b / (2 * s_L_b**3),
             mu_A_b / (2 * s_A_b**3),
        ], axis=1)

    z_b = np.stack([eL_b, eA_b, eL_b**2, eA_b**2], axis=2)
    Psi_b = _hac_cov_batch(z_b, lag)

    var_m_b = np.einsum('bi,bij,bj->b', g_b, Psi_b, g_b) / T
    SE_b = np.where(var_m_b > 0, np.sqrt(np.maximum(var_m_b, 0)) * np.sqrt(12), np.nan)

    t_b = np.where(SE_b > 0, (delta_b - d_obs) / SE_b, np.nan)
    t_b = t_b[~np.isnan(t_b)]
    if len(t_b) < 100:
        return {**nan_ret, 'delta_obs': float(d_obs), 't_obs': float(t_obs),
                'se_obs': float(SE_obs), 'hac_lag': lag}

    p_two = float((np.abs(t_b) >= abs(t_obs)).mean())
    t_lo, t_hi = np.percentile(t_b, [2.5, 97.5])
    ci_lo = d_obs - t_hi * SE_obs
    ci_hi = d_obs - t_lo * SE_obs

    return dict(delta_obs=float(d_obs), t_obs=float(t_obs), se_obs=float(SE_obs),
                ci_lo=float(ci_lo), ci_hi=float(ci_hi), p_two=p_two,
                n=T, hac_lag=lag)


def main():
    print('=== 4 Ens 옵션 vs Ens-anchor SBB HAC 검정 (20 검정) ===\n')

    # rf 로드
    panel = pd.read_csv(DATA_DIR / 'monthly_panel.csv',
                        usecols=['date', 'ticker', 'rf_1m'], parse_dates=['date'])
    rf = panel.groupby('date')['rf_1m'].first().dropna()

    # Ens-anchor 수익률
    with open(RESULTS_DIR / f'{ENS_ANCHOR_KEY}.pkl', 'rb') as f:
        anc_data = pickle.load(f)
    r_anc = anc_data['ret'].dropna()
    r_anc = r_anc[r_anc.index <= CUTOFF]
    print(f'Ens-anchor: {len(r_anc)} 개월')

    t0 = time.perf_counter()
    rows = []
    for base_name, base_key in BASE_SLOTS.items():
        with open(RESULTS_DIR / f'{base_key}.pkl', 'rb') as f:
            base_data = pickle.load(f)
        r_base = base_data['ret'].dropna()
        r_base = r_base[r_base.index <= CUTOFF]

        common = r_base.index.intersection(r_anc.index)
        r_base_c = r_base.loc[common]
        r_anc_c = r_anc.loc[common]

        for plbl, s, e in PERIODS:
            rB = r_base_c; rA = r_anc_c
            if s is not None:
                rB = rB[rB.index >= s]; rA = rA[rA.index >= s]
            if e is not None:
                rB = rB[rB.index <= e]; rA = rA[rA.index <= e]
            if len(rB) < 6:
                continue
            rfa = rf.reindex(rB.index).fillna(0)
            r = paired_sbb_hac(rB, rA, rfa, B=B_RUNS, seed=42)
            p = r['p_two']
            sig = ('***' if pd.notna(p) and p < 0.001 else
                   '**'  if pd.notna(p) and p < 0.01  else
                   '*'   if pd.notna(p) and p < 0.05  else '')
            rows.append({
                'base': base_name, 'comparator': 'Ensemble-anchor',
                'period': plbl, **r, 'sig': sig,
            })

    df = pd.DataFrame(rows)
    elapsed = time.perf_counter() - t0
    print(f'\n완료: {elapsed:.1f}s, {len(df)} 검정\n')

    out_path = OUT_DIR / 'bs20_extra_hac.pkl'
    df.to_pickle(out_path)
    print(f'저장: {out_path}\n')

    print('=== 결과 ===')
    print(df[['base', 'period', 'delta_obs', 'se_obs', 'ci_lo', 'ci_hi', 'p_two', 'sig']].to_string(index=False))

    sig_count = (df['sig'] != '').sum()
    print(f'\n유의 셀: {sig_count}/{len(df)}')


if __name__ == '__main__':
    main()
