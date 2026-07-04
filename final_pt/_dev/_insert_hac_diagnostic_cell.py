"""셀 [7+] HAC bs90 진단 — 4.2/4.3 표 3, 부록 A.7/A.10 sig 별표 정정용.

- bs90_hac.pkl 로드
- (1) 요약 카운트 (기간 × ω 별 sig 수)
- (2) ω=err (pap) Sharpe 45 슬롯 × 5 기간 표
- (3) ω=he Sharpe 45 슬롯 × 5 기간 표
- (4) 표 3 (13 슬롯, 1-step variation) TSV — 본문 4.2 paste
- (5) 부록 A.7 TSV — 45 슬롯 ω=err Sharpe
- (6) 부록 A.10 TSV — 45 슬롯 ω=he Sharpe
- (7) 상위 |Δ_SR| 셀 top 20
"""
from __future__ import annotations

import json
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

NB_PATH = Path(r"C:\Users\서윤범\Desktop\temp\finance_project\final_pt\99_main_analysis.ipynb")


CELL_MD = '''## [7+] HAC bs90 진단 — 표 3 + 부록 A.7/A.10 sig 별표 정정

**목적**: bs90_hac.pkl (HAC studentized 결과) 로부터 4.2/4.3 본문 표 3 및 부록 B 의
sig 별표 정정에 필요한 진단 출력 생성.

**출력**:
1. 요약: ω × 기간 별 sig 셀 카운트
2. ω=err (pap) Sharpe 전체 45 슬롯 × 5 기간 표 (Δ + sig)
3. ω=he Sharpe 전체 45 슬롯 × 5 기간 표
4. **표 3 (13 슬롯 1-step variation) TSV** — 본문 4.2 paste 용
5. **부록 A.7 TSV** — 45 슬롯 ω=err Sharpe paste
6. **부록 A.10 TSV** — 45 슬롯 ω=he Sharpe paste
7. 상위 |Δ_SR| 셀 top 20 (해석 참고)
'''


CELL_CODE = r'''# ── [7+] HAC bs90 진단 (4.2/4.3, 부록 B) ──
bs90_hac = pd.read_pickle(OUT_DIR / 'bs90_hac.pkl')
print(f'로드 완료: {len(bs90_hac)} 행 (450 검정)')


# ── (1) 요약 카운트 ──
print('\n' + '='*70)
print('(1) HAC sig 셀 카운트 — ω × period')
print('='*70)
for om in ['pap', 'he']:
    print(f'\n[ω={om}]')
    sub = bs90_hac[bs90_hac['omega']==om]
    summary = sub.assign(is_sig=(sub['sig']!='').astype(int)).groupby('period')['is_sig'].agg(['sum','count'])
    summary['비율(%)'] = (summary['sum']/summary['count']*100).round(1)
    summary.columns = ['유의셀', '전체', '비율(%)']
    print(summary.reindex(['All','R1','R2','R3','R4']).to_string())


# ── (2) ω=err (pap) Sharpe 45 슬롯 표 ──
print('\n' + '='*100)
print('(2) HAC ω=err (pap) Sharpe: 45 슬롯 × 5 기간 — Δ + sig')
print('='*100)
sub_err = bs90_hac[bs90_hac['omega']=='pap'].copy()
sub_err['cell'] = sub_err.apply(
    lambda r: '' if pd.isna(r['delta_obs']) else f"{r['delta_obs']:+.3f}{r['sig']:<3s}",
    axis=1,
)
tab_err = sub_err.pivot_table(index=['p_w','prior','q'], columns='period', values='cell', aggfunc='first')
tab_err = tab_err[['All','R1','R2','R3','R4']]
pw_order = ['mcap','eq','rp']; pr_order = ['mcap','eq','rp']; q_order = ['lam','raw','inv','vsp','fpm']
idx_order = [(pw, pr, q) for pw in pw_order for pr in pr_order for q in q_order]
tab_err = tab_err.reindex(idx_order)
print(tab_err.to_string())


# ── (3) ω=he Sharpe 45 슬롯 표 ──
print('\n' + '='*100)
print('(3) HAC ω=he Sharpe: 45 슬롯 × 5 기간 — Δ + sig')
print('='*100)
sub_he = bs90_hac[bs90_hac['omega']=='he'].copy()
sub_he['cell'] = sub_he.apply(
    lambda r: '' if pd.isna(r['delta_obs']) else f"{r['delta_obs']:+.3f}{r['sig']:<3s}",
    axis=1,
)
tab_he = sub_he.pivot_table(index=['p_w','prior','q'], columns='period', values='cell', aggfunc='first')
tab_he = tab_he[['All','R1','R2','R3','R4']]
tab_he = tab_he.reindex(idx_order)
print(tab_he.to_string())


# ──────────────────────────────────────────────
# (4) 표 3 (13 슬롯 1-step variation) TSV — 본문 4.2 paste 용
# ──────────────────────────────────────────────
# Anchor: prior=mcap, p_w=mcap, q=fpm, ω=pap
# SET 1 (Q only): prior=mcap, p_w=mcap, ω=pap → q ∈ {lam, raw, inv, vsp, fpm★}
# SET 2 (P only): prior=mcap, q=fpm, ω=pap → p_w ∈ {mcap★, eq, rp}
# SET 3 (Prior only): p_w=mcap, q=fpm, ω=pap → prior ∈ {mcap★, eq, rp}
# SET 4 (Omega only): prior=mcap, p_w=mcap, q=fpm → ω ∈ {pap★, he}

print('\n' + '='*100)
print('(4) 표 3 (13 슬롯 1-step variation) — HAC sig 별표 TSV')
print('='*100)

TAB3_SLOTS = [
    # (label, omega, p_w, prior, q)
    ('SET1 q=lam',     'pap', 'mcap', 'mcap', 'lam'),
    ('SET1 q=raw',     'pap', 'mcap', 'mcap', 'raw'),
    ('SET1 q=inv',     'pap', 'mcap', 'mcap', 'inv'),
    ('SET1 q=vsp',     'pap', 'mcap', 'mcap', 'vsp'),
    ('SET1 q=fpm★',    'pap', 'mcap', 'mcap', 'fpm'),
    ('SET2 p=mcap★',   'pap', 'mcap', 'mcap', 'fpm'),
    ('SET2 p=eq',      'pap', 'eq',   'mcap', 'fpm'),
    ('SET2 p=rp',      'pap', 'rp',   'mcap', 'fpm'),
    ('SET3 prior=mcap★','pap','mcap', 'mcap', 'fpm'),
    ('SET3 prior=eq',  'pap', 'mcap', 'eq',   'fpm'),
    ('SET3 prior=rp',  'pap', 'mcap', 'rp',   'fpm'),
    ('SET4 ω=err★',    'pap', 'mcap', 'mcap', 'fpm'),
    ('SET4 ω=he',      'he',  'mcap', 'mcap', 'fpm'),
]

print('Slot\tAll\tR1\tR2\tR3\tR4')
for label, om, pw, pr, q in TAB3_SLOTS:
    cells = [label]
    for plbl in ['All','R1','R2','R3','R4']:
        row = bs90_hac[(bs90_hac['omega']==om) & (bs90_hac['p_w']==pw) &
                        (bs90_hac['prior']==pr) & (bs90_hac['q']==q) & (bs90_hac['period']==plbl)]
        if row.empty:
            cells.append('')
        else:
            r = row.iloc[0]
            if pd.isna(r['delta_obs']):
                cells.append('')
            else:
                cells.append(f"{r['delta_obs']:+.3f}{r['sig']}")
    print('\t'.join(cells))


# ──────────────────────────────────────────────
# (5) 부록 A.7 TSV — 45 슬롯 ω=err Sharpe (Δ + sig)
# ──────────────────────────────────────────────
print('\n' + '='*100)
print('(5) 부록 A.7 (ω=err Sharpe 45 슬롯) — HAC sig TSV')
print('='*100)

print('p_w\tprior\tq\tAll\tR1\tR2\tR3\tR4')
for pw in pw_order:
    for pr in pr_order:
        for q in q_order:
            cells = [pw, pr, q]
            for plbl in ['All','R1','R2','R3','R4']:
                row = bs90_hac[(bs90_hac['omega']=='pap') & (bs90_hac['p_w']==pw) &
                                (bs90_hac['prior']==pr) & (bs90_hac['q']==q) & (bs90_hac['period']==plbl)]
                if row.empty or pd.isna(row.iloc[0]['delta_obs']):
                    cells.append('')
                else:
                    r = row.iloc[0]
                    cells.append(f"{r['delta_obs']:+.3f}{r['sig']}")
            print('\t'.join(cells))


# ──────────────────────────────────────────────
# (6) 부록 A.10 TSV — 45 슬롯 ω=he Sharpe (Δ + sig)
# ──────────────────────────────────────────────
print('\n' + '='*100)
print('(6) 부록 A.10 (ω=he Sharpe 45 슬롯) — HAC sig TSV')
print('='*100)

print('p_w\tprior\tq\tAll\tR1\tR2\tR3\tR4')
for pw in pw_order:
    for pr in pr_order:
        for q in q_order:
            cells = [pw, pr, q]
            for plbl in ['All','R1','R2','R3','R4']:
                row = bs90_hac[(bs90_hac['omega']=='he') & (bs90_hac['p_w']==pw) &
                                (bs90_hac['prior']==pr) & (bs90_hac['q']==q) & (bs90_hac['period']==plbl)]
                if row.empty or pd.isna(row.iloc[0]['delta_obs']):
                    cells.append('')
                else:
                    r = row.iloc[0]
                    cells.append(f"{r['delta_obs']:+.3f}{r['sig']}")
            print('\t'.join(cells))


# ──────────────────────────────────────────────
# (7) 상위 |Δ_SR| sig 셀 top 20 (해석 참고)
# ──────────────────────────────────────────────
print('\n' + '='*100)
print('(7) HAC sig 셀 |Δ_SR| top 20')
print('='*100)
sig_sub = bs90_hac[bs90_hac['sig'] != ''].copy()
sig_sub['abs_d'] = sig_sub['delta_obs'].abs()
top = sig_sub.nlargest(20, 'abs_d')[['omega','p_w','prior','q','period','delta_obs','se_obs','t_obs','ci_lo','ci_hi','p_two','sig']]
print(top.to_string(index=False,
    formatters={'delta_obs':'{:+.3f}'.format, 'se_obs':'{:.3f}'.format,
                't_obs':'{:+.3f}'.format, 'ci_lo':'{:+.3f}'.format,
                'ci_hi':'{:+.3f}'.format, 'p_two':'{:.4f}'.format}))
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
    print(f'  cell {len(nb["cells"])-2} (md): [7+] HAC bs90 진단')
    print(f'  cell {len(nb["cells"])-1} (code): 표 3 + 부록 A.7/A.10 TSV + 진단')


if __name__ == '__main__':
    main()
