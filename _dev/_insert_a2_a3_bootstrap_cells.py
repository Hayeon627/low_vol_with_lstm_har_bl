"""셀 [3+], [3++] 삽입: A2/A3 SR/Sortino Bootstrap 검정.

- [3+]: 90 슬롯 × 5 기간 × 2 지표 (Sharpe, Sortino) Stationary Block Bootstrap
- [3++]: 표 4 marginal Bootstrap (3 p × 5 기간, 15 슬롯 month-shared)

삽입 위치: 셀 17 (cell [3e]) 뒤
"""
from __future__ import annotations

import json
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

NB_PATH = Path(r"C:\Users\서윤범\Desktop\temp\finance_project\final_pt\99_main_analysis.ipynb")


CELL_3PLUS_MD = '''## [3+] 90 슬롯 페어와이즈 SR/Sortino 검정 (Stationary Block Bootstrap)

**목적**: §4.2 (표 3, 13 슬롯 anchor 1-dim 변형) + §4.3 (표 4 marginal) + 부록 B (표 A.7~A.12, 90 슬롯 전체) 의 통계적 유의성 검정.

- **방법**: 본문 §4.1 의 정상 블록 부트스트랩 (Politis & Romano, 1994; B=10,000, 평균 블록 길이 T^(1/3)) 동일 적용
- **단위**: 슬롯별 (LSTM 월별 수익률, ANN 월별 수익률) 페어 → 월 인덱스 동시 resample → Δ_SR (또는 Δ_Sortino) 분포 → p-value + 95% CI
- **메트릭**: Sharpe, Sortino (MDD 는 path-dependent → 검정 제외)
- **MDD**: raw 값만 부록에 그대로
'''


CELL_3PLUS_CODE = '''# ── [3+] 90 슬롯 × 5 기간 × 2 지표 Stationary Block Bootstrap ──
import time
from itertools import product

# 슬롯 정의 (90 = 2 omega × 3 prior × 3 p_w × 5 q)
PRIORS_A    = ['mcap', 'eq', 'rp']
P_WEIGHTS_A = ['mcap', 'eq', 'rp']
Q_MODES_A   = ['lam', 'raw', 'inv', 'vsp', 'fpm']
OMEGAS_A    = ['pap', 'he']

slots90 = [(om, pw, pr, q)
           for om in OMEGAS_A
           for pw in P_WEIGHTS_A
           for pr in PRIORS_A
           for q  in Q_MODES_A]
print(f'90 슬롯 정의: {len(slots90)}')

# 검정 기간
PERIODS_A2 = [
    ('All', None, None),
    ('R1',  '2010-01-01', '2012-06-30'),
    ('R2',  '2012-07-01', '2019-12-31'),
    ('R3',  '2020-01-01', '2023-06-30'),
    ('R4',  '2023-07-01', '2025-12-31'),
]
B_RUNS_A2 = 10_000


# ── SR / Sortino 스칼라 (관측값) ──
def _sharpe_sc(r, rfa):
    exc = r - rfa
    vol = r.std(ddof=1) * np.sqrt(12)
    return float(exc.mean() * 12 / vol) if vol > 0 else np.nan

def _sortino_sc(r, rfa):
    exc = r - rfa
    neg = r[r < 0]
    if len(neg) < 2: return np.nan
    dn = neg.std(ddof=1) * np.sqrt(12)
    return float(exc.mean() * 12 / dn) if dn > 0 else np.nan


# ── 벡터화 SR / Sortino (B × T 매트릭스) ──
def _sharpe_b(r_b, rf_b):
    exc_b = r_b - rf_b
    mean_exc = exc_b.mean(axis=1)
    std_r = r_b.std(axis=1, ddof=1)
    return np.where(std_r > 0, mean_exc * 12 / (std_r * np.sqrt(12)), np.nan)

def _sortino_b(r_b, rf_b):
    exc_b = r_b - rf_b
    mean_exc = exc_b.mean(axis=1)
    neg_mask = r_b < 0
    n_neg = neg_mask.sum(axis=1)
    sum_neg = (r_b * neg_mask).sum(axis=1)
    mean_neg = np.where(n_neg > 0, sum_neg / n_neg, 0.0)
    diff_sq = ((r_b - mean_neg[:, None]) ** 2) * neg_mask
    var_neg = np.where(n_neg > 1, diff_sq.sum(axis=1) / (n_neg - 1), 0.0)
    sd_neg = np.sqrt(var_neg) * np.sqrt(12)
    return np.where(sd_neg > 0, mean_exc * 12 / sd_neg, np.nan)


# ── 페어 SBB 검정 ──
def paired_sbb_test(rL, rA, rfa, metric='sharpe', B=10_000, seed=42):
    """페어된 월별 수익률 SBB Δ 검정.

    rL, rA: pd.Series (월별 수익률, 같은 인덱스)
    rfa: rf 정렬됨
    metric: 'sharpe' or 'sortino'
    """
    rL_arr = np.asarray(rL.values, dtype=float)
    rA_arr = np.asarray(rA.values, dtype=float)
    rf_arr = np.asarray(rfa.values, dtype=float)
    T = len(rL_arr)
    if T < 6:
        return dict(delta_obs=np.nan, ci_lo=np.nan, ci_hi=np.nan, p_two=np.nan, n=T)

    if metric == 'sharpe':
        d_obs = _sharpe_sc(rL_arr, rf_arr) - _sharpe_sc(rA_arr, rf_arr)
    else:
        d_obs = _sortino_sc(rL_arr, rf_arr) - _sortino_sc(rA_arr, rf_arr)
    if pd.isna(d_obs):
        return dict(delta_obs=np.nan, ci_lo=np.nan, ci_hi=np.nan, p_two=np.nan, n=T)

    L = max(2.0, T ** (1/3))
    rng = np.random.default_rng(seed)

    new_block = rng.random((B, T)) < (1.0 / L)
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

    if metric == 'sharpe':
        sL = _sharpe_b(rL_b, rf_b)
        sA = _sharpe_b(rA_b, rf_b)
    else:
        sL = _sortino_b(rL_b, rf_b)
        sA = _sortino_b(rA_b, rf_b)

    delta_b = sL - sA
    delta_b = delta_b[~np.isnan(delta_b)]
    if len(delta_b) < 100:
        return dict(delta_obs=float(d_obs), ci_lo=np.nan, ci_hi=np.nan, p_two=np.nan, n=T)

    centered = delta_b - d_obs
    p_two = float((np.abs(centered) >= abs(d_obs)).mean())
    ci_lo, ci_hi = np.percentile(delta_b, [2.5, 97.5])

    return dict(delta_obs=float(d_obs), ci_lo=float(ci_lo), ci_hi=float(ci_hi),
                p_two=p_two, n=T)


# ── 메인 루프: 90 슬롯 × 5 기간 × 2 지표 ──
print(f'\\n90 슬롯 × {len(PERIODS_A2)} 기간 × 2 지표 (Sharpe, Sortino) Bootstrap 시작...')
print(f'B={B_RUNS_A2:,}, 평균 블록 길이 T^(1/3)')

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

    rL_full = rL_full.dropna()
    rA_full = rA_full.dropna()
    rL_full = rL_full[rL_full.index <= CUTOFF]
    rA_full = rA_full[rA_full.index <= CUTOFF]
    common = rL_full.index.intersection(rA_full.index)
    rL_full = rL_full.loc[common]
    rA_full = rA_full.loc[common]

    for plbl, s, e in PERIODS_A2:
        rL = rL_full; rA = rA_full
        if s is not None:
            rL = rL[rL.index >= s]; rA = rA[rA.index >= s]
        if e is not None:
            rL = rL[rL.index <= e]; rA = rA[rA.index <= e]
        if len(rL) < 6:
            continue
        rfa = rf.reindex(rL.index).fillna(0)

        for metric in ['sharpe', 'sortino']:
            r = paired_sbb_test(rL, rA, rfa, metric=metric, B=B_RUNS_A2, seed=42)
            p = r['p_two']
            sig = ('***' if pd.notna(p) and p < 0.001 else
                   '**'  if pd.notna(p) and p < 0.01  else
                   '*'   if pd.notna(p) and p < 0.05  else '')
            rows.append({
                'omega': om, 'p_w': pw, 'prior': pr, 'q': q,
                'period': plbl, 'metric': metric,
                **r, 'sig': sig,
            })

    if (i + 1) % 15 == 0:
        elapsed = time.perf_counter() - t0
        remain = elapsed * (len(slots90) / (i + 1) - 1)
        print(f'  {i+1:>3d}/{len(slots90)} 슬롯 완료 ({elapsed:.0f}s, 예상 잔여 {remain:.0f}s)')

if missing:
    print(f'\\n⚠ 누락 슬롯 {len(missing)}: {missing[:5]}...')

bs90 = pd.DataFrame(rows)
print(f'\\n완료: {time.perf_counter()-t0:.1f}s | 결과 {len(bs90)} 행 ({bs90.groupby(["omega","p_w","prior","q"]).ngroups} 슬롯)')

# 저장
bs90_path = OUT_DIR / 'bs90_per_slot.pkl'
bs90.to_pickle(bs90_path)
print(f'  저장: {bs90_path}')

# 요약: omega 별 유의 셀 수 (Sharpe)
print('\\n[Sharpe] omega 별 유의 (* 이상) 셀 카운트:')
for om in OMEGAS_A:
    sub = bs90[(bs90['omega']==om) & (bs90['metric']=='sharpe')]
    total = len(sub)
    sig_count = (sub['sig'] != '').sum()
    print(f'  omega={om}: {sig_count}/{total} 유의')
'''


CELL_3PP_MD = '''## [3++] §4.3 표 4 marginal Bootstrap — p별 평균 Δ_SR

**목적**: 표 4 의 3 p × 5 기간 = 15 셀 marginal 평균 Δ_SR 의 통계적 유의성 검정.

- **단위**: 각 (p, 기간) 에 대해 15 슬롯 (prior 3 × q 5, ω=err 고정) 의 평균 Δ_SR
- **핵심**: 월 인덱스 SBB 를 15 슬롯에 **동시 적용** → 슬롯 간 시장 환경 상관 보존
- **출력**: marginal Δ_SR + 95% CI + p
'''


CELL_3PP_CODE = '''# ── [3++] 표 4 marginal Bootstrap (3 p × 5 기간) ──
def marginal_sbb(slot_pairs, rfa, metric='sharpe', B=10_000, seed=42):
    """월 인덱스 공유 SBB. 15 슬롯의 페어 SR 평균에 대해 검정.

    slot_pairs: list of (rL_series, rA_series) — 모두 같은 월 인덱스
    """
    n_slots = len(slot_pairs)
    T = len(slot_pairs[0][0])
    if T < 6:
        return dict(delta_obs=np.nan, ci_lo=np.nan, ci_hi=np.nan, p_two=np.nan, n=T, n_slots=n_slots)

    rL_mat = np.array([np.asarray(rL.values, dtype=float) for rL, rA in slot_pairs])  # (n_slots, T)
    rA_mat = np.array([np.asarray(rA.values, dtype=float) for rL, rA in slot_pairs])
    rf_arr = np.asarray(rfa.values, dtype=float)

    # observed: per slot SR 계산 후 평균
    obs_L = np.array([_sharpe_sc(rL_mat[s], rf_arr) if metric=='sharpe' else _sortino_sc(rL_mat[s], rf_arr)
                      for s in range(n_slots)])
    obs_A = np.array([_sharpe_sc(rA_mat[s], rf_arr) if metric=='sharpe' else _sortino_sc(rA_mat[s], rf_arr)
                      for s in range(n_slots)])
    d_obs = np.nanmean(obs_L) - np.nanmean(obs_A)
    if pd.isna(d_obs):
        return dict(delta_obs=np.nan, ci_lo=np.nan, ci_hi=np.nan, p_two=np.nan, n=T, n_slots=n_slots)

    L = max(2.0, T ** (1/3))
    rng = np.random.default_rng(seed)
    new_block = rng.random((B, T)) < (1.0 / L)
    new_block[:, 0] = True
    seg_id = np.cumsum(new_block, axis=1) - 1
    starts = rng.integers(0, T, size=(B, T))
    seg_starts = np.take_along_axis(starts, seg_id, axis=1)
    t_arr = np.broadcast_to(np.arange(T), (B, T))
    last_new = np.where(new_block, t_arr, -1)
    last_new = np.maximum.accumulate(last_new, axis=1)
    offset = t_arr - last_new
    indices = (seg_starts + offset) % T  # (B, T) 공유

    rf_b = rf_arr[indices]  # (B, T)

    delta_b_per_slot = np.zeros((n_slots, B))
    for s in range(n_slots):
        rL_b = rL_mat[s][indices]
        rA_b = rA_mat[s][indices]
        if metric == 'sharpe':
            sL = _sharpe_b(rL_b, rf_b)
            sA = _sharpe_b(rA_b, rf_b)
        else:
            sL = _sortino_b(rL_b, rf_b)
            sA = _sortino_b(rA_b, rf_b)
        delta_b_per_slot[s] = sL - sA

    delta_b_mean = np.nanmean(delta_b_per_slot, axis=0)
    delta_b_mean = delta_b_mean[~np.isnan(delta_b_mean)]
    if len(delta_b_mean) < 100:
        return dict(delta_obs=float(d_obs), ci_lo=np.nan, ci_hi=np.nan, p_two=np.nan, n=T, n_slots=n_slots)

    centered = delta_b_mean - d_obs
    p_two = float((np.abs(centered) >= abs(d_obs)).mean())
    ci_lo, ci_hi = np.percentile(delta_b_mean, [2.5, 97.5])

    return dict(delta_obs=float(d_obs), ci_lo=float(ci_lo), ci_hi=float(ci_hi),
                p_two=p_two, n=T, n_slots=n_slots)


# 표 4: ω=err (pap) 고정, 각 p_w 에 대해 15 슬롯 marginal Bootstrap (Sharpe 만)
print('\\n표 4 marginal Bootstrap (3 p × 5 기간 × Sharpe) 시작...')
import time
t0 = time.perf_counter()
marg_rows = []
for pw in P_WEIGHTS_A:
    pair_full = []
    for pr in PRIORS_A:
        for q in Q_MODES_A:
            L_name = f'mat_{pr}_{pw}_{q}_pap'
            A_name = L_name + '_ann'
            if L_name not in loaded or A_name not in loaded:
                continue
            rL = loaded[L_name].get('ret').dropna()
            rA = loaded[A_name].get('ret').dropna()
            rL = rL[rL.index <= CUTOFF]
            rA = rA[rA.index <= CUTOFF]
            common = rL.index.intersection(rA.index)
            if len(common) < 6: continue
            pair_full.append((rL.loc[common], rA.loc[common]))
    print(f'  p_w={pw}: {len(pair_full)} 슬롯 (prior×q)')

    for plbl, s, e in PERIODS_A2:
        pair_period = []
        for rL, rA in pair_full:
            r1 = rL; r2 = rA
            if s is not None:
                r1 = r1[r1.index >= s]; r2 = r2[r2.index >= s]
            if e is not None:
                r1 = r1[r1.index <= e]; r2 = r2[r2.index <= e]
            common = r1.index.intersection(r2.index)
            if len(common) < 6: continue
            pair_period.append((r1.loc[common], r2.loc[common]))
        if not pair_period: continue

        rfa = rf.reindex(pair_period[0][0].index).fillna(0)
        r = marginal_sbb(pair_period, rfa, metric='sharpe', B=B_RUNS_A2, seed=42)
        p = r['p_two']
        sig = ('***' if pd.notna(p) and p < 0.001 else
               '**'  if pd.notna(p) and p < 0.01  else
               '*'   if pd.notna(p) and p < 0.05  else '')
        marg_rows.append({'p_w': pw, 'period': plbl, 'metric': 'sharpe',
                          **r, 'sig': sig})

bs_marg = pd.DataFrame(marg_rows)
print(f'\\n완료: {time.perf_counter()-t0:.1f}s | {len(bs_marg)} 행')
bs_marg.to_pickle(OUT_DIR / 'bs_marginal_table4.pkl')

print('\\n표 4 marginal Bootstrap 결과:')
print(bs_marg.to_string(index=False,
    formatters={'delta_obs': '{:+.4f}'.format, 'ci_lo': '{:+.4f}'.format,
                'ci_hi': '{:+.4f}'.format, 'p_two': '{:.4f}'.format}))
'''


def main() -> None:
    nb = json.loads(NB_PATH.read_text(encoding='utf-8'))
    print(f'기존 셀 수: {len(nb["cells"])}')

    # cell 17 이 [3e] 인지 확인
    cell17_src = ''.join(nb['cells'][17]['source'])
    assert '[3e]' in cell17_src, f'cell 17 not [3e], got: {cell17_src[:100]}'
    print('cell 17 = [3e] 확인')

    # 새 셀 생성
    def _new_cell(cell_type: str, source: str) -> dict:
        return {
            'cell_type': cell_type,
            'metadata': {},
            'source': source.splitlines(keepends=True),
            **({'outputs': [], 'execution_count': None} if cell_type == 'code' else {}),
        }

    new_cells = [
        _new_cell('markdown', CELL_3PLUS_MD),
        _new_cell('code',     CELL_3PLUS_CODE),
        _new_cell('markdown', CELL_3PP_MD),
        _new_cell('code',     CELL_3PP_CODE),
    ]

    # cell 17 뒤에 삽입 (insert at index 18)
    new_list = nb['cells'][:18] + new_cells + nb['cells'][18:]
    nb['cells'] = new_list

    NB_PATH.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding='utf-8')
    print(f'OK — 셀 4개 삽입 완료. 새 셀 수: {len(new_list)}')
    print('  insert position: cell 18, 19, 20, 21 (markdown, code, markdown, code)')
    print('  [3+] : 90 슬롯 × 5 기간 × 2 지표 SBB (예상 ~22분)')
    print('  [3++] : 표 4 marginal Bootstrap (3 p × 5 기간, 예상 ~5분)')


if __name__ == '__main__':
    main()
