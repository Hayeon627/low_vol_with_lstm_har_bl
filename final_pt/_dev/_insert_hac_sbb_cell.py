"""셀 [6+] HAC Studentized SBB — Ledoit & Wolf (2008) 정확 구현.

- SBB (Politis & Romano, 1994) + Ledoit-Wolf (2008) HAC studentized bootstrap-t
- HAC: Newey-West Bartlett kernel, lag = ⌊T^(1/3)⌋
- Delta method: paired SR difference SE 유도
- Vectorized batch HAC computation
- bs90 + bs100 모두 재실행

의존성:
- 셀 [3+], [4+] 의 환경 (loaded, rf, CUTOFF, OUT_DIR, slots90, PERIODS_A2, B_RUNS_A2,
  BASE_SLOTS_44, COMPARATORS_44, PERIODS_44, B_44, _sharpe_sc, _sharpe_b)
"""
from __future__ import annotations

import json
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

NB_PATH = Path(r"C:\Users\서윤범\Desktop\temp\finance_project\final_pt\99_main_analysis.ipynb")


CELL_MD = '''## [6+] HAC Studentized SBB — Ledoit & Wolf (2008) 정확 구현

**방법론 (Ledoit-Wolf 2008 정확 권장)**:
1. **SBB** (Politis & Romano, 1994): 평균 블록 길이 T^(1/3), B = 10,000
2. **Studentized 통계량**: t = (Δ_SR − Δ_obs) / SE_paired
3. **HAC SE**: Newey-West Bartlett kernel, lag = ⌊T^(1/3)⌋
   - z_t = (e_L,t, e_A,t, e_L,t², e_A,t²) 벡터, e = r − rf
   - Ψ_HAC = Γ_0 + Σ_h w_h · (Γ_h + Γ_h′)
   - Delta method: SE² = ∇f′ · Ψ_HAC · ∇f / T
4. **Bootstrap-t critical value**: t_b 분포의 2.5%, 97.5% percentile

**대체 이유**:
- 기존 [5+] 의 Memmel (2003) IID SE 는 이변량 정규성 가정 → heavy tails + volatility clustering 무시
- Ledoit-Wolf 지적: Memmel 은 fat-tail 또는 GARCH 데이터에서 over-reject (liberal)
- HAC 는 자기상관 + 조건부 이분산 모두 보정

**출력**:
- bs90_hac.pkl, bs100_hac.pkl
- percentile vs studentized(IID) vs studentized(HAC) 3 방법 비교
'''


CELL_CODE = r'''# ── [6+] HAC studentized SBB (Ledoit-Wolf 2008 정확 구현) ──
import time


# ── Newey-West Bartlett HAC covariance (single) ──
def _hac_cov(z, lag):
    """z: (T, k) array. Returns (k, k) HAC covariance (long-run variance)."""
    T = z.shape[0]
    z_dm = z - z.mean(axis=0)
    Gamma = z_dm.T @ z_dm / T
    for h in range(1, lag + 1):
        w = 1.0 - h / (lag + 1)  # Bartlett weight
        Gamma_h = z_dm[h:].T @ z_dm[:-h] / T
        Gamma = Gamma + w * (Gamma_h + Gamma_h.T)
    return Gamma


# ── Newey-West Bartlett HAC covariance (batch, vectorized) ──
def _hac_cov_batch(z_b, lag):
    """z_b: (B, T, k). Returns (B, k, k) HAC covariance for each batch."""
    B, T, k = z_b.shape
    z_dm = z_b - z_b.mean(axis=1, keepdims=True)   # (B, T, k)
    # Gamma_0: (B, k, k)
    Gamma = np.einsum('bti,btj->bij', z_dm, z_dm) / T
    for h in range(1, lag + 1):
        w = 1.0 - h / (lag + 1)
        Gamma_h = np.einsum('bti,btj->bij', z_dm[:, h:, :], z_dm[:, :-h, :]) / T
        Gamma = Gamma + w * (Gamma_h + Gamma_h.transpose(0, 2, 1))
    return Gamma


# ── SR gradient (Delta method) for excess return formulation ──
def _sr_gradient(mu_L, mu_A, gam_L, gam_A, s_L, s_A):
    """Gradient of Δ_SR = μ_L/s_L − μ_A/s_A w.r.t. (μ_L, μ_A, γ_L, γ_A).

    Uses identity s² = γ − μ² so gradient closed form.
    """
    return np.array([
         gam_L / s_L**3,           # ∂/∂μ_L
        -gam_A / s_A**3,           # ∂/∂μ_A
        -mu_L / (2 * s_L**3),      # ∂/∂γ_L
         mu_A / (2 * s_A**3),      # ∂/∂γ_A
    ])


def paired_sbb_hac(rL, rA, rfa, B=10_000, seed=42):
    """Ledoit & Wolf (2008) HAC studentized paired SBB for SR difference."""
    rL_arr = np.asarray(rL.values, dtype=float)
    rA_arr = np.asarray(rA.values, dtype=float)
    rf_arr = np.asarray(rfa.values, dtype=float)
    T = len(rL_arr)
    nan_ret = dict(delta_obs=np.nan, t_obs=np.nan, se_obs=np.nan,
                   ci_lo=np.nan, ci_hi=np.nan, p_two=np.nan, n=T, hac_lag=0)
    if T < 6:
        return nan_ret

    # observed annualized SR difference
    SR_L = _sharpe_sc(rL_arr, rf_arr)
    SR_A = _sharpe_sc(rA_arr, rf_arr)
    d_obs = SR_L - SR_A
    if pd.isna(d_obs):
        return nan_ret

    # HAC lag (T^(1/3), min 1)
    lag = max(int(np.floor(T ** (1/3))), 1)

    # ── Observed SE via HAC ──
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
    SE_obs = np.sqrt(var_m_obs) * np.sqrt(12)   # annualized
    t_obs = d_obs / SE_obs

    # ── SBB indices (B, T) ──
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

    rL_b = rL_arr[indices]    # (B, T)
    rA_b = rA_arr[indices]
    rf_b = rf_arr[indices]
    eL_b = rL_b - rf_b
    eA_b = rA_b - rf_b

    # ── Batch SR ──
    sL_b = _sharpe_b(rL_b, rf_b)
    sA_b = _sharpe_b(rA_b, rf_b)
    delta_b = sL_b - sA_b

    # ── Batch HAC SE ──
    mu_L_b = eL_b.mean(axis=1)
    mu_A_b = eA_b.mean(axis=1)
    gam_L_b = (eL_b**2).mean(axis=1)
    gam_A_b = (eA_b**2).mean(axis=1)
    s_L2_b = gam_L_b - mu_L_b**2
    s_A2_b = gam_A_b - mu_A_b**2
    valid_std = (s_L2_b > 0) & (s_A2_b > 0)
    s_L_b = np.where(valid_std, np.sqrt(np.maximum(s_L2_b, 0)), np.nan)
    s_A_b = np.where(valid_std, np.sqrt(np.maximum(s_A2_b, 0)), np.nan)

    # Gradient (B, 4)
    with np.errstate(divide='ignore', invalid='ignore'):
        g_b = np.stack([
             gam_L_b / s_L_b**3,
            -gam_A_b / s_A_b**3,
            -mu_L_b / (2 * s_L_b**3),
             mu_A_b / (2 * s_A_b**3),
        ], axis=1)

    # z_b (B, T, 4)
    z_b = np.stack([eL_b, eA_b, eL_b**2, eA_b**2], axis=2)
    Psi_b = _hac_cov_batch(z_b, lag)   # (B, 4, 4)

    # var_m = g' Psi g / T for each b
    var_m_b = np.einsum('bi,bij,bj->b', g_b, Psi_b, g_b) / T
    SE_b = np.where(var_m_b > 0, np.sqrt(np.maximum(var_m_b, 0)) * np.sqrt(12), np.nan)

    t_b = np.where(SE_b > 0, (delta_b - d_obs) / SE_b, np.nan)
    t_b = t_b[~np.isnan(t_b)]
    if len(t_b) < 100:
        return {**nan_ret, 'delta_obs': float(d_obs), 't_obs': float(t_obs),
                'se_obs': float(SE_obs), 'hac_lag': lag}

    # Two-sided bootstrap-t p-value
    p_two = float((np.abs(t_b) >= abs(t_obs)).mean())

    # Bootstrap-t CI (translate t percentile to Δ scale)
    t_lo, t_hi = np.percentile(t_b, [2.5, 97.5])
    ci_lo = d_obs - t_hi * SE_obs
    ci_hi = d_obs - t_lo * SE_obs

    return dict(delta_obs=float(d_obs), t_obs=float(t_obs), se_obs=float(SE_obs),
                ci_lo=float(ci_lo), ci_hi=float(ci_hi), p_two=p_two,
                n=T, hac_lag=lag)


# ──────────────────────────────────────────────
# (A) bs90 재실행 — 4.2/4.3
# ──────────────────────────────────────────────
print('='*100)
print('(A) bs90 재실행 — HAC studentized (Ledoit-Wolf 2008 정확)')
print('='*100)

t0 = time.perf_counter()
rows = []
for i, (om, pw, pr, q) in enumerate(slots90):
    L_name = f'mat_{pr}_{pw}_{q}_{om}'
    A_name = L_name + '_ann'
    if L_name not in loaded or A_name not in loaded:
        continue
    rL_full = loaded[L_name].get('ret')
    rA_full = loaded[A_name].get('ret')
    if not isinstance(rL_full, pd.Series) or not isinstance(rA_full, pd.Series):
        continue
    rL_full = rL_full.dropna(); rA_full = rA_full.dropna()
    rL_full = rL_full[rL_full.index <= CUTOFF]
    rA_full = rA_full[rA_full.index <= CUTOFF]
    common = rL_full.index.intersection(rA_full.index)
    rL_full = rL_full.loc[common]; rA_full = rA_full.loc[common]

    for plbl, s, e in PERIODS_A2:
        rL = rL_full; rA = rA_full
        if s is not None: rL = rL[rL.index >= s]; rA = rA[rA.index >= s]
        if e is not None: rL = rL[rL.index <= e]; rA = rA[rA.index <= e]
        if len(rL) < 6: continue
        rfa = rf.reindex(rL.index).fillna(0)
        r = paired_sbb_hac(rL, rA, rfa, B=B_RUNS_A2, seed=42)
        p = r['p_two']
        sig = ('***' if pd.notna(p) and p < 0.001 else
               '**'  if pd.notna(p) and p < 0.01  else
               '*'   if pd.notna(p) and p < 0.05  else '')
        rows.append({'omega': om, 'p_w': pw, 'prior': pr, 'q': q,
                     'period': plbl, 'metric': 'sharpe', **r, 'sig': sig})
    if (i + 1) % 30 == 0:
        elapsed = time.perf_counter() - t0
        remain = elapsed * (len(slots90) / (i + 1) - 1)
        print(f'  {i+1:>3d}/{len(slots90)} ({elapsed:.0f}s, 잔여 {remain:.0f}s)')

bs90_hac = pd.DataFrame(rows)
print(f'\n완료: {time.perf_counter()-t0:.1f}s, {len(bs90_hac)} 행')
bs90_hac_path = OUT_DIR / 'bs90_hac.pkl'
bs90_hac.to_pickle(bs90_hac_path)
print(f'저장: {bs90_hac_path}')


# ──────────────────────────────────────────────
# (B) bs100 재실행 — 4.4
# ──────────────────────────────────────────────
print('\n' + '='*100)
print('(B) bs100 재실행 — HAC studentized (Ledoit-Wolf 2008 정확)')
print('='*100)

t0 = time.perf_counter()
rows = []
for base_name, base_key in BASE_SLOTS_44.items():
    rB_full = loaded[base_key].get('ret')
    if not isinstance(rB_full, pd.Series): continue
    rB_full = rB_full.dropna()
    rB_full = rB_full[rB_full.index <= CUTOFF]
    for comp_name, rC_raw in COMPARATORS_44:
        rC_full = rC_raw.dropna()
        rC_full = rC_full[rC_full.index <= CUTOFF]
        common = rB_full.index.intersection(rC_full.index)
        rB_c = rB_full.loc[common]; rC_c = rC_full.loc[common]
        for plbl, s, e in PERIODS_44:
            rB = rB_c; rC = rC_c
            if s is not None: rB = rB[rB.index >= s]; rC = rC[rC.index >= s]
            if e is not None: rB = rB[rB.index <= e]; rC = rC[rC.index <= e]
            if len(rB) < 6: continue
            rfa = rf.reindex(rB.index).fillna(0)
            r = paired_sbb_hac(rB, rC, rfa, B=B_44, seed=42)
            p = r['p_two']
            sig = ('***' if pd.notna(p) and p < 0.001 else
                   '**'  if pd.notna(p) and p < 0.01  else
                   '*'   if pd.notna(p) and p < 0.05  else '')
            rows.append({'base': base_name, 'comparator': comp_name,
                         'period': plbl, **r, 'sig': sig})

bs100_hac = pd.DataFrame(rows)
print(f'완료: {time.perf_counter()-t0:.1f}s, {len(bs100_hac)} 행')
bs100_hac_path = OUT_DIR / 'bs100_hac.pkl'
bs100_hac.to_pickle(bs100_hac_path)
print(f'저장: {bs100_hac_path}')


# ──────────────────────────────────────────────
# (C) 3 방법 비교 (percentile / studentized-IID / HAC) sig 카운트
# ──────────────────────────────────────────────
print('\n' + '='*100)
print('(C) Sig 셀 카운트 3 방법 비교')
print('='*100)

bs90_perc = pd.read_pickle(OUT_DIR / 'bs90_per_slot.pkl')
bs90_perc = bs90_perc[bs90_perc['metric']=='sharpe']
bs90_iid_path = OUT_DIR / 'bs90_studentized.pkl'
bs90_iid = pd.read_pickle(bs90_iid_path) if bs90_iid_path.exists() else None

print('\n[bs90 (4.2/4.3), 450 검정]')
print(f'{"period":>6s} | {"percentile":>10s} | {"stud-IID":>10s} | {"stud-HAC":>10s}')
print('-'*50)
for plbl in ['All','R1','R2','R3','R4']:
    n_perc = (bs90_perc[bs90_perc['period']==plbl]['sig'] != '').sum()
    n_iid  = (bs90_iid [bs90_iid ['period']==plbl]['sig'] != '').sum() if bs90_iid is not None else -1
    n_hac  = (bs90_hac [bs90_hac ['period']==plbl]['sig'] != '').sum()
    print(f'{plbl:>6s} | {n_perc:>10d} | {n_iid:>10d} | {n_hac:>10d}')
print(f'{"합":>6s} | {(bs90_perc["sig"]!="").sum():>10d} | '
      f'{(bs90_iid["sig"]!="").sum() if bs90_iid is not None else -1:>10d} | '
      f'{(bs90_hac["sig"]!="").sum():>10d}')

bs100_perc = pd.read_pickle(OUT_DIR / 'bs100_strategy.pkl')
bs100_iid_path = OUT_DIR / 'bs100_studentized.pkl'
bs100_iid = pd.read_pickle(bs100_iid_path) if bs100_iid_path.exists() else None

print('\n[bs100 (4.4), 100 검정]')
print(f'{"comparator":>14s} | {"percentile":>10s} | {"stud-IID":>10s} | {"stud-HAC":>10s}')
print('-'*54)
for comp in ['ANN-anchor','SPY','1/N','Risk Parity']:
    n_perc = (bs100_perc[bs100_perc['comparator']==comp]['sig'] != '').sum()
    n_iid  = (bs100_iid [bs100_iid ['comparator']==comp]['sig'] != '').sum() if bs100_iid is not None else -1
    n_hac  = (bs100_hac [bs100_hac ['comparator']==comp]['sig'] != '').sum()
    print(f'{comp:>14s} | {n_perc:>10d} | {n_iid:>10d} | {n_hac:>10d}')
print(f'{"합":>14s} | {(bs100_perc["sig"]!="").sum():>10d} | '
      f'{(bs100_iid["sig"]!="").sum() if bs100_iid is not None else -1:>10d} | '
      f'{(bs100_hac["sig"]!="").sum():>10d}')


# ──────────────────────────────────────────────
# (D) HAC 핵심 셀 — Ens-anchor vs ANN-anchor
# ──────────────────────────────────────────────
print('\n' + '='*100)
print('(D) HAC 결과 — Ens-anchor vs ANN-anchor (Para 5 동률 입증 핵심)')
print('='*100)
print(f'{"period":>6s} {"Δ_SR":>9s} {"SE_HAC":>8s} {"t_obs":>8s} {"lag":>4s} {"95% CI":>22s} {"p_two":>8s} {"sig":>5s}')
print('-'*80)
for plbl, _, _ in PERIODS_44:
    row = bs100_hac[(bs100_hac['base']=='Ensemble-anchor') & (bs100_hac['comparator']=='ANN-anchor') & (bs100_hac['period']==plbl)]
    if row.empty: continue
    r = row.iloc[0]
    ci_str = f'[{r["ci_lo"]:+.3f}, {r["ci_hi"]:+.3f}]'
    print(f'{plbl:>6s} {r["delta_obs"]:>+9.4f} {r["se_obs"]:>8.3f} {r["t_obs"]:>+8.3f} {int(r["hac_lag"]):>4d} {ci_str:>22s} {r["p_two"]:>8.4f} {r["sig"]:>5s}')


# ──────────────────────────────────────────────
# (E) HAC 표 6 TSV — Ens 행 ANN-anchor 대비 sig
# ──────────────────────────────────────────────
print('\n' + '='*100)
print('(E) HAC 결과 — 표 6 TSV (Ens 행 ANN-anchor 대비 sig)')
print('='*100)

def _sig_hac(base_name, period):
    row = bs100_hac[(bs100_hac['base']==base_name) & (bs100_hac['comparator']=='ANN-anchor') & (bs100_hac['period']==period)]
    if row.empty: return ''
    return row.iloc[0]['sig']

def _sharpe_period(ret_s, s, e):
    r = ret_s.dropna(); r = r[r.index <= CUTOFF]
    if s is not None: r = r[r.index >= s]
    if e is not None: r = r[r.index <= e]
    if len(r) < 6: return np.nan
    rfa = rf.reindex(r.index).fillna(0)
    exc = r - rfa
    vol = r.std(ddof=1) * np.sqrt(12)
    return float(exc.mean()*12/vol) if vol>0 else np.nan

ROW_DEFS_E = [
    ('SPY (market)',                  ret_spy,                                                          None),
    ('1/N (equal-weight)',            ret_1n,                                                           None),
    ('Risk Parity (1/σ)',             ret_rp,                                                           None),
    ('ANN-anchor (Pyo & Lee, 2018)',  loaded['mat_mcap_mcap_fpm_pap_ann']['ret'],                       None),
    ('Ensemble-anchor (σ 모형 교체)',  loaded[BASE_SLOTS_44['Ensemble-anchor']]['ret'],                  'Ensemble-anchor'),
    ('Ensemble-defensive (peq,qlam)', loaded[BASE_SLOTS_44['Ensemble-defensive (p^eq, q^lam)']]['ret'], 'Ensemble-defensive (p^eq, q^lam)'),
    ('Ensemble-defensive (prp,qlam)', loaded[BASE_SLOTS_44['Ensemble-defensive (p^rp, q^lam)']]['ret'], 'Ensemble-defensive (p^rp, q^lam)'),
    ('Ensemble-adaptive (peq,qff3)',  loaded[BASE_SLOTS_44['Ensemble-adaptive (p^eq, q^ff3)']]['ret'],  'Ensemble-adaptive (p^eq, q^ff3)'),
    ('Ensemble-adaptive (prp,qff3)',  loaded[BASE_SLOTS_44['Ensemble-adaptive (p^rp, q^ff3)']]['ret'],  'Ensemble-adaptive (p^rp, q^ff3)'),
]

print('Strategy\tAll\tR1\tR2\tR3\tR4')
for row_name, ret_s, base_lookup in ROW_DEFS_E:
    cells = [row_name]
    for plbl, s, e in PERIODS_44:
        v = _sharpe_period(ret_s, s, e)
        s_star = _sig_hac(base_lookup, plbl) if base_lookup else ''
        cells.append(f'{v:.2f}{s_star}' if not np.isnan(v) else '')
    print('\t'.join(cells))


# ──────────────────────────────────────────────
# (F) HAC 외부 벤치마크 대비
# ──────────────────────────────────────────────
print('\n' + '='*100)
print('(F) HAC 결과 — 외부 벤치마크 대비 (5 BL × 3 외부 × 5 기간)')
print('='*100)
for ext in ['SPY','1/N','Risk Parity']:
    print(f'\n[vs {ext}]')
    sub = bs100_hac[bs100_hac['comparator']==ext].copy()
    sub['cell'] = sub.apply(lambda r: f"{r['delta_obs']:+.3f}{r['sig']:<3s}" if pd.notna(r['delta_obs']) else '', axis=1)
    tab = sub.pivot_table(index='base', columns='period', values='cell', aggfunc='first')
    tab = tab[['All','R1','R2','R3','R4']]
    tab = tab.reindex(list(BASE_SLOTS_44.keys()))
    print(tab.to_string())
'''


def main() -> None:
    nb = json.loads(NB_PATH.read_text(encoding='utf-8'))
    print(f'현재 셀 수: {len(nb["cells"])}')

    def _cell(ct: str, src: str) -> dict:
        return {
            'cell_type': ct, 'metadata': {},
            'source': src.splitlines(keepends=True),
            **({'outputs': [], 'execution_count': None} if ct == 'code' else {}),
        }

    new_cells = [_cell('markdown', CELL_MD), _cell('code', CELL_CODE)]
    nb['cells'] = nb['cells'] + new_cells

    NB_PATH.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding='utf-8')
    print(f'OK — 새 셀 2개 추가. 새 셀 수: {len(nb["cells"])}')
    print(f'  cell {len(nb["cells"])-2} (md): [6+] HAC Studentized SBB')
    print(f'  cell {len(nb["cells"])-1} (code): HAC bs90 + bs100 재실행 + 3방법 비교')


if __name__ == '__main__':
    main()
