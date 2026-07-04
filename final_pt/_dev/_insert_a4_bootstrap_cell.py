"""셀 [4+] 4.4 벤치마크 성능 비교 — 페어 SBB 검정 100개.

- 5 BL (Ensemble-anchor + 4 Ens 옵션) × 4 comparator (ANN-anchor + SPY/1N/RP) × 5 기간 = 100 Sharpe 검정
- paired_sbb_test 는 [3+] 셀에서 이미 정의됨 → 같은 커널에서 재사용
- 결과 pickle: outputs/99_main_analysis/bs100_strategy.pkl
- 출력: (1) base × period 표 (comparator 별), (2) 유의 셀 카운트, (3) 표 6 TSV (ANN 대비 sig), (4) 외부 sig
"""
from __future__ import annotations

import json
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

NB_PATH = Path(r"C:\Users\서윤범\Desktop\temp\finance_project\final_pt\99_main_analysis.ipynb")


CELL_MD = '''## [4+] 4.4 벤치마크 비교 — 페어 SBB 검정 (5 BL × 4 comparator)

표 6 의 5 BL 슬롯 (Ensemble-anchor + 4 Ens 옵션) vs 4 comparator (ANN-anchor, SPY, 1/N, Risk Parity)
페어 부트스트랩 SR 검정.

**검정 방법**: 4.2/4.3 과 동일 (Stationary Block Bootstrap, B=10,000, 평균 블록 길이 T^(1/3))

**페어 정의**: Δ_SR = base (BL) − comparator. Δ > 0 면 BL 우위.

**결과**:
- 5 × 4 페어 × 5 기간 = 100 검정 (Sharpe 만; Sortino 는 부록 E 보조 raw)
- `bs100_strategy.pkl` 저장
- 표 6 paste 용 TSV (sig 별표 ANN-anchor 대비)
- 외부 벤치마크 (SPY/1N/RP) 대비 sig 도 별도 출력

**의존성**: 셀 [3+] 의 `paired_sbb_test`, `_sharpe_sc`, `_sharpe_b` 함수가 동일 커널에서 이미 정의되어 있어야 함.
'''


CELL_CODE = '''# ── [4+] 4.4 벤치마크 비교 페어 SBB ──
import time

BASE_SLOTS_44 = {
    'Ensemble-anchor':                    'mat_mcap_mcap_fpm_pap',
    'Ensemble-defensive (p^eq, q^lam)':   'mat_mcap_eq_lam_pap',
    'Ensemble-defensive (p^rp, q^lam)':   'mat_mcap_rp_lam_pap',
    'Ensemble-adaptive (p^eq, q^ff3)':    'mat_mcap_eq_fpm_pap',
    'Ensemble-adaptive (p^rp, q^ff3)':    'mat_mcap_rp_fpm_pap',
}

ANN_ANCHOR_KEY = 'mat_mcap_mcap_fpm_pap_ann'

COMPARATORS_44 = [
    ('ANN-anchor',   loaded[ANN_ANCHOR_KEY]['ret']),
    ('SPY',          ret_spy),
    ('1/N',          ret_1n),
    ('Risk Parity',  ret_rp),
]

PERIODS_44 = [
    ('All', None, None),
    ('R1',  '2010-01-01', '2012-06-30'),
    ('R2',  '2012-07-01', '2019-12-31'),
    ('R3',  '2020-01-01', '2023-06-30'),
    ('R4',  '2023-07-01', '2025-12-31'),
]

B_44 = 10_000
n_test = len(BASE_SLOTS_44) * len(COMPARATORS_44) * len(PERIODS_44)
print(f'{len(BASE_SLOTS_44)} BL × {len(COMPARATORS_44)} comparator × {len(PERIODS_44)} 기간 = {n_test} 검정')
print(f'SBB B={B_44:,}, 평균 블록 T^(1/3)')

t0 = time.perf_counter()
rows = []
for base_name, base_key in BASE_SLOTS_44.items():
    rB_full = loaded[base_key].get('ret')
    if not isinstance(rB_full, pd.Series):
        print(f'⚠ 누락: {base_name}'); continue
    rB_full = rB_full.dropna()
    rB_full = rB_full[rB_full.index <= CUTOFF]

    for comp_name, rC_raw in COMPARATORS_44:
        rC_full = rC_raw.dropna()
        rC_full = rC_full[rC_full.index <= CUTOFF]
        common = rB_full.index.intersection(rC_full.index)
        rB_c = rB_full.loc[common]
        rC_c = rC_full.loc[common]

        for plbl, s, e in PERIODS_44:
            rB = rB_c; rC = rC_c
            if s is not None:
                rB = rB[rB.index >= s]; rC = rC[rC.index >= s]
            if e is not None:
                rB = rB[rB.index <= e]; rC = rC[rC.index <= e]
            if len(rB) < 6:
                continue
            rfa = rf.reindex(rB.index).fillna(0)
            r = paired_sbb_test(rB, rC, rfa, metric='sharpe', B=B_44, seed=42)
            p = r['p_two']
            sig = ('***' if pd.notna(p) and p < 0.001 else
                   '**'  if pd.notna(p) and p < 0.01  else
                   '*'   if pd.notna(p) and p < 0.05  else '')
            rows.append({
                'base': base_name, 'comparator': comp_name,
                'period': plbl, **r, 'sig': sig,
            })

print(f'완료: {time.perf_counter()-t0:.1f}s, 결과 {len(rows)} 행')

bs100 = pd.DataFrame(rows)
bs100_path = OUT_DIR / 'bs100_strategy.pkl'
bs100.to_pickle(bs100_path)
print(f'저장: {bs100_path}')


# ── (1) base × period 표 (comparator 별) ──
print('\\n' + '='*100)
print('(1) Sharpe Δ + sig — base × period (comparator 별)')
print('='*100)
for comp_name in [c[0] for c in COMPARATORS_44]:
    print(f'\\n[vs {comp_name}]')
    sub = bs100[bs100['comparator']==comp_name].copy()
    sub['cell'] = sub.apply(lambda r: f"{r['delta_obs']:+.3f}{r['sig']:<3s}" if pd.notna(r['delta_obs']) else '', axis=1)
    tab = sub.pivot_table(index='base', columns='period', values='cell', aggfunc='first')
    tab = tab[['All','R1','R2','R3','R4']]
    tab = tab.reindex(list(BASE_SLOTS_44.keys()))
    print(tab.to_string())


# ── (2) 유의 셀 카운트 ──
print('\\n' + '='*100)
print('(2) 유의 셀 카운트 — comparator × period')
print('='*100)
summary = bs100.assign(is_sig=(bs100['sig']!='').astype(int)).groupby(['comparator','period'])['is_sig'].agg(['sum','count'])
summary['ratio(%)'] = (summary['sum']/summary['count']*100).round(1)
summary.columns = ['유의셀','전체','비율(%)']
print(summary.to_string())


# ── (3) 표 6 paste 용 TSV (Sharpe + ANN-anchor 대비 sig) ──
print('\\n' + '='*100)
print('(3) 표 6 paste 용 TSV — raw Sharpe (Ens 행은 ANN-anchor 대비 sig 별표)')
print('='*100)

def _sharpe_period(ret_s, s, e):
    r = ret_s.dropna(); r = r[r.index <= CUTOFF]
    if s is not None: r = r[r.index >= s]
    if e is not None: r = r[r.index <= e]
    if len(r) < 6: return np.nan
    rfa = rf.reindex(r.index).fillna(0)
    exc = r - rfa
    vol = r.std(ddof=1) * np.sqrt(12)
    return float(exc.mean()*12/vol) if vol>0 else np.nan


def _sig_vs_ann(base_name, period):
    row = bs100[(bs100['base']==base_name) & (bs100['comparator']=='ANN-anchor') & (bs100['period']==period)]
    if row.empty: return ''
    return row.iloc[0]['sig']

# 표 6 행 정의 (사용자 원본 순서)
ROW_DEFS = [
    ('SPY (market)',                  ret_spy,                                                         None),
    ('1/N (equal-weight)',            ret_1n,                                                          None),
    ('Risk Parity (1/σ)',             ret_rp,                                                          None),
    ('ANN-anchor (Pyo & Lee, 2018)',  loaded[ANN_ANCHOR_KEY]['ret'],                                  None),
    ('Ensemble-anchor (σ 모형 교체)',  loaded[BASE_SLOTS_44['Ensemble-anchor']]['ret'],                'Ensemble-anchor'),
    ('Ensemble-defensive (peq,qlam)', loaded[BASE_SLOTS_44['Ensemble-defensive (p^eq, q^lam)']]['ret'],'Ensemble-defensive (p^eq, q^lam)'),
    ('Ensemble-defensive (prp,qlam)', loaded[BASE_SLOTS_44['Ensemble-defensive (p^rp, q^lam)']]['ret'],'Ensemble-defensive (p^rp, q^lam)'),
    ('Ensemble-adaptive (peq,qff3)',  loaded[BASE_SLOTS_44['Ensemble-adaptive (p^eq, q^ff3)']]['ret'], 'Ensemble-adaptive (p^eq, q^ff3)'),
    ('Ensemble-adaptive (prp,qff3)',  loaded[BASE_SLOTS_44['Ensemble-adaptive (p^rp, q^ff3)']]['ret'], 'Ensemble-adaptive (p^rp, q^ff3)'),
]

print('Strategy\\tAll\\tR1\\tR2\\tR3\\tR4')
for row_name, ret_s, base_lookup in ROW_DEFS:
    cells = [row_name]
    for plbl, s, e in PERIODS_44:
        v = _sharpe_period(ret_s, s, e)
        s_star = _sig_vs_ann(base_lookup, plbl) if base_lookup else ''
        cells.append(f'{v:.2f}{s_star}' if not np.isnan(v) else '')
    print('\\t'.join(cells))


# ── (4) 외부 벤치마크 대비 sig 셀 별도 표 ──
print('\\n' + '='*100)
print('(4) 외부 벤치마크 대비 (5 BL × 3 외부 × 5 기간) — Δ + sig')
print('='*100)
for ext in ['SPY','1/N','Risk Parity']:
    print(f'\\n[vs {ext}]')
    sub = bs100[bs100['comparator']==ext].copy()
    sub['cell'] = sub.apply(lambda r: f"{r['delta_obs']:+.3f}{r['sig']:<3s}" if pd.notna(r['delta_obs']) else '', axis=1)
    tab = sub.pivot_table(index='base', columns='period', values='cell', aggfunc='first')
    tab = tab[['All','R1','R2','R3','R4']]
    tab = tab.reindex(list(BASE_SLOTS_44.keys()))
    print(tab.to_string())


# ── (5) Narrative 인용 핵심 셀 lookup ──
print('\\n' + '='*100)
print('(5) Narrative 인용 핵심 셀 — Ensemble-anchor vs ANN-anchor (Para 4 동률 입증)')
print('='*100)
print(f'{"period":>6s} {"Δ_SR":>9s} {"95% CI":>22s} {"p_two":>8s} {"sig":>5s}')
print('-'*55)
for plbl, _, _ in PERIODS_44:
    row = bs100[(bs100['base']=='Ensemble-anchor') & (bs100['comparator']=='ANN-anchor') & (bs100['period']==plbl)]
    if row.empty: continue
    r = row.iloc[0]
    ci_str = f'[{r["ci_lo"]:+.3f}, {r["ci_hi"]:+.3f}]'
    print(f'{plbl:>6s} {r["delta_obs"]:>+9.4f} {ci_str:>22s} {r["p_two"]:>8.4f} {r["sig"]:>5s}')
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
    print(f'OK — 새 셀 2개 노트북 끝에 추가. 새 셀 수: {len(nb["cells"])}')
    print(f'  cell {len(nb["cells"])-2} (md): [4+] 4.4 벤치마크 비교')
    print(f'  cell {len(nb["cells"])-1} (code): 100 검정 + 진단 + TSV')


if __name__ == '__main__':
    main()
