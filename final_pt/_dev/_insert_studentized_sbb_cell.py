"""셀 [5+] Studentized SBB 재검정 — Ledoit & Wolf (2008) 권장 정확 구현.

- Studentized t = (Δ_SR - Δ_obs) / SE_paired
- SE_paired = Memmel (2003) IID SE for paired SR difference
- SBB (Politis & Romano, 1994)
- bs90 (4.2/4.3) + bs100 (4.4) 모두 재실행
- 결과 저장: bs90_studentized.pkl, bs100_studentized.pkl
- 비교: 기존 percentile 결과 vs studentized 결과 sig 셀 변동

의존성:
- 셀 [1b] (cell 7) — ret_spy/1n/rp
- 셀 [3+] (cell 19) 의 환경 (loaded, rf, CUTOFF, OUT_DIR) — 함수는 새로 정의함
"""
from __future__ import annotations

import json
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

NB_PATH = Path(r"C:\Users\서윤범\Desktop\temp\finance_project\final_pt\99_main_analysis.ipynb")


CELL_MD = '''## [5+] Studentized SBB 재검정 — Ledoit & Wolf (2008) 정확 구현

**방법**: Studentized Stationary Block Bootstrap
- SBB: Politis & Romano (1994), 평균 블록 길이 T^(1/3)
- Studentized 통계량: t = (Δ_SR - Δ_obs) / SE_paired
- SE_paired: Memmel (2003) IID SE for paired SR difference
- Framework: Ledoit & Wolf (2008)
- B = 10,000

**기존 [3+], [4+] 의 percentile bootstrap 을 대체** — sig 결과 변동 비교.

**출력**:
- bs90_studentized.pkl (4.2/4.3, 900 검정)
- bs100_studentized.pkl (4.4, 100 검정)
- 기존 percentile 결과 vs studentized 결과 sig 셀 카운트 비교
'''


CELL_CODE = r'''# ── [5+] Studentized SBB 재검정 ──
import time

# ── Memmel (2003) IID SE for paired SR difference (annualized) ──
def _paired_sr_se_iid(rL_a, rA_a, rf_a, T):
    """Annualized SE for paired Sharpe ratio difference (Memmel 2003 IID)."""
    excL = rL_a - rf_a
    excA = rA_a - rf_a
    std_L = rL_a.std(ddof=1) if hasattr(rL_a, 'std') else np.std(rL_a, ddof=1)
    std_A = rA_a.std(ddof=1) if hasattr(rA_a, 'std') else np.std(rA_a, ddof=1)
    if std_L <= 0 or std_A <= 0:
        return np.nan
    SR_L_m = excL.mean() / std_L  # monthly raw SR
    SR_A_m = excA.mean() / std_A
    rho = np.corrcoef(excL, excA)[0,1]
    if np.isnan(rho):
        return np.nan
    var_m = (1.0/T) * (2.0*(1.0 - rho) + 0.5*(SR_L_m**2 + SR_A_m**2 - 2.0*(rho**2)*SR_L_m*SR_A_m))
    if var_m <= 0:
        return np.nan
    return np.sqrt(var_m) * np.sqrt(12)  # annualized SE


# ── Studentized paired SBB test ──
def paired_sbb_studentized(rL, rA, rfa, B=10_000, seed=42):
    """Studentized paired SBB for Sharpe ratio difference (Ledoit-Wolf 2008)."""
    rL_arr = np.asarray(rL.values, dtype=float)
    rA_arr = np.asarray(rA.values, dtype=float)
    rf_arr = np.asarray(rfa.values, dtype=float)
    T = len(rL_arr)
    nan_ret = dict(delta_obs=np.nan, t_obs=np.nan, se_obs=np.nan,
                   ci_lo=np.nan, ci_hi=np.nan, p_two=np.nan, n=T)
    if T < 6:
        return nan_ret

    # observed annualized SR difference
    SR_L = _sharpe_sc(rL_arr, rf_arr)
    SR_A = _sharpe_sc(rA_arr, rf_arr)
    d_obs = SR_L - SR_A
    if pd.isna(d_obs):
        return nan_ret

    SE_obs = _paired_sr_se_iid(rL_arr, rA_arr, rf_arr, T)
    if pd.isna(SE_obs) or SE_obs <= 0:
        return {**nan_ret, 'delta_obs': float(d_obs)}

    t_obs = d_obs / SE_obs

    # SBB indices
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

    rL_b = rL_arr[indices]   # (B, T)
    rA_b = rA_arr[indices]
    rf_b = rf_arr[indices]

    # vectorized annualized SR
    sL = _sharpe_b(rL_b, rf_b)
    sA = _sharpe_b(rA_b, rf_b)
    delta_b = sL - sA

    # vectorized SE_b (Memmel IID)
    excL_b = rL_b - rf_b
    excA_b = rA_b - rf_b
    mean_excL = excL_b.mean(axis=1)
    mean_excA = excA_b.mean(axis=1)
    std_L_b = rL_b.std(axis=1, ddof=1)
    std_A_b = rA_b.std(axis=1, ddof=1)
    SR_L_m_b = np.where(std_L_b > 0, mean_excL / std_L_b, np.nan)
    SR_A_m_b = np.where(std_A_b > 0, mean_excA / std_A_b, np.nan)

    # rho_b: corr(excL_b, excA_b) per row
    cov_b = ((excL_b - mean_excL[:,None]) * (excA_b - mean_excA[:,None])).sum(axis=1) / (T - 1)
    std_excL_b = excL_b.std(axis=1, ddof=1)
    std_excA_b = excA_b.std(axis=1, ddof=1)
    rho_b = np.where((std_excL_b > 0) & (std_excA_b > 0), cov_b / (std_excL_b * std_excA_b), np.nan)

    var_m_b = (1.0/T) * (2.0*(1.0 - rho_b) + 0.5*(SR_L_m_b**2 + SR_A_m_b**2 - 2.0*(rho_b**2)*SR_L_m_b*SR_A_m_b))
    SE_b = np.where(var_m_b > 0, np.sqrt(np.maximum(var_m_b, 0)) * np.sqrt(12), np.nan)

    t_b = np.where(SE_b > 0, (delta_b - d_obs) / SE_b, np.nan)
    t_b = t_b[~np.isnan(t_b)]
    if len(t_b) < 100:
        return {**nan_ret, 'delta_obs': float(d_obs), 't_obs': float(t_obs), 'se_obs': float(SE_obs)}

    p_two = float((np.abs(t_b) >= abs(t_obs)).mean())

    # studentized CI (translate t quantiles to Δ scale)
    t_lo, t_hi = np.percentile(t_b, [2.5, 97.5])
    ci_lo = d_obs - t_hi * SE_obs
    ci_hi = d_obs - t_lo * SE_obs

    return dict(delta_obs=float(d_obs), t_obs=float(t_obs), se_obs=float(SE_obs),
                ci_lo=float(ci_lo), ci_hi=float(ci_hi), p_two=p_two, n=T)


# ──────────────────────────────────────────────
# (A) bs90 재실행 — 4.2/4.3 (90 슬롯 × 5 기간, Sharpe only)
# ──────────────────────────────────────────────
print('='*100)
print('(A) bs90 재실행 — 90 슬롯 × 5 기간 = 450 Sharpe 검정 (studentized)')
print('='*100)

t0 = time.perf_counter()
rows = []
missing = []
for i, (om, pw, pr, q) in enumerate(slots90):
    L_name = f'mat_{pr}_{pw}_{q}_{om}'
    A_name = L_name + '_ann'
    if L_name not in loaded or A_name not in loaded:
        missing.append(L_name); continue
    rL_full = loaded[L_name].get('ret')
    rA_full = loaded[A_name].get('ret')
    if not isinstance(rL_full, pd.Series) or not isinstance(rA_full, pd.Series):
        missing.append(L_name); continue
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
        r = paired_sbb_studentized(rL, rA, rfa, B=B_RUNS_A2, seed=42)
        p = r['p_two']
        sig = ('***' if pd.notna(p) and p < 0.001 else
               '**'  if pd.notna(p) and p < 0.01  else
               '*'   if pd.notna(p) and p < 0.05  else '')
        rows.append({'omega': om, 'p_w': pw, 'prior': pr, 'q': q,
                     'period': plbl, 'metric': 'sharpe', **r, 'sig': sig})
    if (i + 1) % 30 == 0:
        elapsed = time.perf_counter() - t0
        remain = elapsed * (len(slots90) / (i + 1) - 1)
        print(f'  {i+1:>3d}/{len(slots90)} 슬롯 ({elapsed:.0f}s, 잔여 {remain:.0f}s)')

bs90_st = pd.DataFrame(rows)
print(f'\n완료: {time.perf_counter()-t0:.1f}s, {len(bs90_st)} 행')
bs90_st_path = OUT_DIR / 'bs90_studentized.pkl'
bs90_st.to_pickle(bs90_st_path)
print(f'저장: {bs90_st_path}')


# ──────────────────────────────────────────────
# (B) bs100 재실행 — 4.4
# ──────────────────────────────────────────────
print('\n' + '='*100)
print('(B) bs100 재실행 — 5 BL × 4 comparator × 5 기간 = 100 Sharpe 검정 (studentized)')
print('='*100)

t0 = time.perf_counter()
rows = []
for base_name, base_key in BASE_SLOTS_44.items():
    rB_full = loaded[base_key].get('ret')
    if not isinstance(rB_full, pd.Series):
        continue
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
            r = paired_sbb_studentized(rB, rC, rfa, B=B_44, seed=42)
            p = r['p_two']
            sig = ('***' if pd.notna(p) and p < 0.001 else
                   '**'  if pd.notna(p) and p < 0.01  else
                   '*'   if pd.notna(p) and p < 0.05  else '')
            rows.append({'base': base_name, 'comparator': comp_name,
                         'period': plbl, **r, 'sig': sig})

bs100_st = pd.DataFrame(rows)
print(f'완료: {time.perf_counter()-t0:.1f}s, {len(bs100_st)} 행')
bs100_st_path = OUT_DIR / 'bs100_studentized.pkl'
bs100_st.to_pickle(bs100_st_path)
print(f'저장: {bs100_st_path}')


# ──────────────────────────────────────────────
# (C) 비교: percentile vs studentized sig 카운트
# ──────────────────────────────────────────────
print('\n' + '='*100)
print('(C) Sig 셀 카운트 비교 — percentile (기존) vs studentized (Ledoit-Wolf 정확)')
print('='*100)

# bs90 비교
bs90_old = pd.read_pickle(OUT_DIR / 'bs90_per_slot.pkl')
bs90_old_sh = bs90_old[bs90_old['metric']=='sharpe']

print('\n[bs90 — 4.2/4.3, 450 검정 (Sharpe)]')
print(f'{"period":>6s} | {"percentile":>12s} | {"studentized":>12s}')
print('-'*40)
for plbl in ['All','R1','R2','R3','R4']:
    n_old = (bs90_old_sh[bs90_old_sh['period']==plbl]['sig'] != '').sum()
    n_st  = (bs90_st[bs90_st['period']==plbl]['sig'] != '').sum()
    print(f'{plbl:>6s} | {n_old:>12d} | {n_st:>12d}')
n_old_total = (bs90_old_sh['sig'] != '').sum()
n_st_total  = (bs90_st['sig'] != '').sum()
print(f'{"합":>6s} | {n_old_total:>12d} | {n_st_total:>12d}')

# bs100 비교
bs100_old = pd.read_pickle(OUT_DIR / 'bs100_strategy.pkl')

print('\n[bs100 — 4.4, 100 검정 (Sharpe)]')
print(f'{"comparator":>14s} {"period":>6s} | {"percentile":>12s} | {"studentized":>12s}')
print('-'*55)
for comp in ['ANN-anchor','SPY','1/N','Risk Parity']:
    for plbl in ['All','R1','R2','R3','R4']:
        n_old = (bs100_old[(bs100_old['comparator']==comp) & (bs100_old['period']==plbl)]['sig'] != '').sum()
        n_st  = (bs100_st [(bs100_st ['comparator']==comp) & (bs100_st ['period']==plbl)]['sig'] != '').sum()
        if n_old > 0 or n_st > 0:
            print(f'{comp:>14s} {plbl:>6s} | {n_old:>12d} | {n_st:>12d}')

n_old_total = (bs100_old['sig'] != '').sum()
n_st_total  = (bs100_st ['sig'] != '').sum()
print(f'{"합":>21s} | {n_old_total:>12d} | {n_st_total:>12d}')


# ──────────────────────────────────────────────
# (D) bs100 studentized 핵심 셀 lookup
# ──────────────────────────────────────────────
print('\n' + '='*100)
print('(D) studentized 결과 — Ens-anchor vs ANN-anchor 핵심 셀 (Para 5 동률 입증)')
print('='*100)
print(f'{"period":>6s} {"Δ_SR":>9s} {"SE":>8s} {"t_obs":>8s} {"95% CI":>22s} {"p_two":>8s} {"sig":>5s}')
print('-'*70)
for plbl, _, _ in PERIODS_44:
    row = bs100_st[(bs100_st['base']=='Ensemble-anchor') & (bs100_st['comparator']=='ANN-anchor') & (bs100_st['period']==plbl)]
    if row.empty: continue
    r = row.iloc[0]
    ci_str = f'[{r["ci_lo"]:+.3f}, {r["ci_hi"]:+.3f}]'
    print(f'{plbl:>6s} {r["delta_obs"]:>+9.4f} {r["se_obs"]:>8.3f} {r["t_obs"]:>+8.3f} {ci_str:>22s} {r["p_two"]:>8.4f} {r["sig"]:>5s}')


# ──────────────────────────────────────────────
# (E) bs100 studentized 표 6 paste 용 TSV
# ──────────────────────────────────────────────
print('\n' + '='*100)
print('(E) studentized 결과 — 표 6 TSV (Ens 행 ANN-anchor 대비 sig 별표)')
print('='*100)

def _sig_st(base_name, period):
    row = bs100_st[(bs100_st['base']==base_name) & (bs100_st['comparator']=='ANN-anchor') & (bs100_st['period']==period)]
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

ROW_DEFS = [
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
for row_name, ret_s, base_lookup in ROW_DEFS:
    cells = [row_name]
    for plbl, s, e in PERIODS_44:
        v = _sharpe_period(ret_s, s, e)
        s_star = _sig_st(base_lookup, plbl) if base_lookup else ''
        cells.append(f'{v:.2f}{s_star}' if not np.isnan(v) else '')
    print('\t'.join(cells))


# ──────────────────────────────────────────────
# (F) bs100 외부 벤치마크 대비 sig 셀
# ──────────────────────────────────────────────
print('\n' + '='*100)
print('(F) studentized 결과 — 외부 벤치마크 대비 sig 셀 (5 BL × 3 외부 × 5 기간)')
print('='*100)
for ext in ['SPY','1/N','Risk Parity']:
    print(f'\n[vs {ext}]')
    sub = bs100_st[bs100_st['comparator']==ext].copy()
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
    print(f'  cell {len(nb["cells"])-2} (md): [5+] Studentized SBB 재검정')
    print(f'  cell {len(nb["cells"])-1} (code): studentized bs90 + bs100 재실행 + 비교')


if __name__ == '__main__':
    main()
