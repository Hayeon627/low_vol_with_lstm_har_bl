"""셀 [3+++] 삽입: 진단/확인용 출력.

bs90 결과를 4가지 관점에서 표시:
1. 요약 — omega × 기간 × metric 유의 셀 카운트
2. omega=err Sharpe 전체 표 (45 슬롯 × 5 기간, Δ + sig)
3. narrative 인용 주요 셀 lookup
4. 상위 유의 셀 top 20
"""
from __future__ import annotations

import json
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

NB_PATH = Path(r"C:\Users\서윤범\Desktop\temp\finance_project\final_pt\99_main_analysis.ipynb")


CELL_MD = '''## [3+++] Bootstrap 결과 진단 — bs90 확인

본 셀은 `bs90_per_slot.pkl` 로드해 4가지 관점에서 결과 확인:

1. **요약 통계** — omega × 기간 × metric 별 유의 셀 카운트
2. **omega=err Sharpe 전체** — 45 슬롯 × 5 기간 (Δ + sig 별표)
3. **omega=he Sharpe 전체** — 동일
4. **narrative 인용 셀 lookup** — 본문에서 인용한 핵심 셀 결과
5. **상위 유의 셀 top 20** — |Δ_SR| 큰 순서 + p-value
'''


CELL_CODE = '''# ── [3+++] bs90 결과 진단 ──
from IPython.display import display
bs90 = pd.read_pickle(OUT_DIR / 'bs90_per_slot.pkl')
print(f'로드 완료: {len(bs90)} 행 ({bs90["omega"].nunique()} omega × {bs90["p_w"].nunique()} p_w × {bs90["prior"].nunique()} prior × {bs90["q"].nunique()} q × {bs90["period"].nunique()} period × {bs90["metric"].nunique()} metric)')

# ── (1) 요약: omega × metric × period 유의 카운트 ──
print('\\n' + '='*70)
print('(1) 유의 셀 카운트 (p<.05)')
print('='*70)
for met in ['sharpe', 'sortino']:
    print(f'\\n[{met.upper()}]')
    sub = bs90[bs90['metric'] == met]
    summary = sub.assign(is_sig=(sub['sig'] != '').astype(int)).groupby(['omega', 'period'])['is_sig'].agg(['sum', 'count'])
    summary['ratio'] = (summary['sum'] / summary['count'] * 100).round(1)
    summary.columns = ['유의셀', '전체', '비율(%)']
    print(summary.to_string())


# ── (2) omega=err Sharpe 표 (45 슬롯 × 5 기간, Δ + sig) ──
print('\\n' + '='*100)
print('(2) ω=err (pap) Sharpe: 45 슬롯 × 5 기간 — Δ + sig')
print('='*100)
sub_err = bs90[(bs90['omega']=='pap') & (bs90['metric']=='sharpe')].copy()
sub_err['cell'] = sub_err.apply(
    lambda r: '' if pd.isna(r['delta_obs']) else f"{r['delta_obs']:+.3f}{r['sig']:<3s}",
    axis=1,
)
tab_err = sub_err.pivot_table(index=['p_w','prior','q'], columns='period',
                                values='cell', aggfunc='first')
# 기간 순서
tab_err = tab_err[['All','R1','R2','R3','R4']]
# slot 순서 (mcap→eq→rp, mcap→eq→rp, lam→raw→inv→vsp→fpm)
pw_order = ['mcap','eq','rp']; pr_order = ['mcap','eq','rp']; q_order = ['lam','raw','inv','vsp','fpm']
idx_order = [(pw, pr, q) for pw in pw_order for pr in pr_order for q in q_order]
tab_err = tab_err.reindex(idx_order)
print(tab_err.to_string())


# ── (3) omega=he Sharpe 표 ──
print('\\n' + '='*100)
print('(3) ω=he Sharpe: 45 슬롯 × 5 기간 — Δ + sig')
print('='*100)
sub_he = bs90[(bs90['omega']=='he') & (bs90['metric']=='sharpe')].copy()
sub_he['cell'] = sub_he.apply(
    lambda r: '' if pd.isna(r['delta_obs']) else f"{r['delta_obs']:+.3f}{r['sig']:<3s}",
    axis=1,
)
tab_he = sub_he.pivot_table(index=['p_w','prior','q'], columns='period',
                              values='cell', aggfunc='first')
tab_he = tab_he[['All','R1','R2','R3','R4']]
tab_he = tab_he.reindex(idx_order)
print(tab_he.to_string())


# ── (4) Narrative 인용 셀 lookup ──
print('\\n' + '='*100)
print('(4) Narrative 인용 셀 (본문 §4.2 / §4.3 인용 슬롯)')
print('='*100)

# 본문 4.2 인용 슬롯들 — (omega, p_w, prior, q, period, metric)
narrative_cells = [
    # q 변형 분석 (anchor: mcap_mcap, omega=pap)
    ('pap', 'mcap', 'mcap', 'lam', 'R3', 'sharpe', 'q=lam R3 (q≥0 부호 안정)'),
    ('pap', 'mcap', 'mcap', 'raw', 'R3', 'sharpe', 'q=raw R3'),
    ('pap', 'mcap', 'mcap', 'inv', 'R3', 'sharpe', 'q=inv R3'),
    ('pap', 'mcap', 'mcap', 'vsp', 'R3', 'sharpe', 'q=vsp R3'),
    ('pap', 'mcap', 'mcap', 'fpm', 'R3', 'sharpe', 'q=fpm R3 (anchor, 부호 유동)'),
    # p 변형 분석
    ('pap', 'mcap', 'mcap', 'fpm', 'All', 'sharpe', 'p=mcap All (anchor)'),
    ('pap', 'eq',   'mcap', 'fpm', 'All', 'sharpe', 'p=eq All'),
    ('pap', 'rp',   'mcap', 'fpm', 'All', 'sharpe', 'p=rp All'),
    # w_mkt 변형 (R1, R3 ANN 우위 vs R2, R4 LSTM 우위)
    ('pap', 'mcap', 'mcap', 'fpm', 'R1', 'sharpe', 'anchor R1'),
    ('pap', 'mcap', 'mcap', 'fpm', 'R3', 'sharpe', 'anchor R3'),
    ('pap', 'mcap', 'mcap', 'fpm', 'R2', 'sharpe', 'anchor R2'),
    ('pap', 'mcap', 'mcap', 'fpm', 'R4', 'sharpe', 'anchor R4'),
    # omega 변형 (omega=he vs omega=err)
    ('he',  'mcap', 'mcap', 'fpm', 'All', 'sharpe', 'omega=he All (vs anchor)'),
]
print(f'{"슬롯 설명":<40s} {"Δ_SR":>9s} {"95% CI":>22s} {"p_two":>8s} {"sig":>5s}')
print('-' * 90)
for om, pw, pr, q, period, met, label in narrative_cells:
    row = bs90[(bs90['omega']==om) & (bs90['p_w']==pw) & (bs90['prior']==pr) &
               (bs90['q']==q) & (bs90['period']==period) & (bs90['metric']==met)]
    if row.empty:
        print(f'{label:<40s} (not found)')
        continue
    r = row.iloc[0]
    ci_str = f'[{r["ci_lo"]:+.3f}, {r["ci_hi"]:+.3f}]'
    print(f'{label:<40s} {r["delta_obs"]:>+9.4f} {ci_str:>22s} {r["p_two"]:>8.4f} {r["sig"]:>5s}')


# ── (5) 상위 유의 셀 top 20 (|Δ_SR| 기준) ──
print('\\n' + '='*100)
print('(5) |Δ_SR| 큰 순서 상위 20 셀 (Sharpe, sig ≠ "")')
print('='*100)
sub = bs90[(bs90['metric']=='sharpe') & (bs90['sig'] != '')].copy()
sub['abs_d'] = sub['delta_obs'].abs()
top = sub.nlargest(20, 'abs_d')[['omega','p_w','prior','q','period','delta_obs','ci_lo','ci_hi','p_two','sig']]
print(top.to_string(index=False,
    formatters={'delta_obs':'{:+.4f}'.format, 'ci_lo':'{:+.4f}'.format,
                'ci_hi':'{:+.4f}'.format, 'p_two':'{:.4f}'.format}))
'''


def main() -> None:
    nb = json.loads(NB_PATH.read_text(encoding='utf-8'))
    print(f'현재 셀 수: {len(nb["cells"])}')

    # 셀 21 확인 — [3++] code
    c21 = ''.join(nb['cells'][21]['source'])
    assert '[3++]' in c21, f'cell 21 not [3++]'
    print('cell 21 = [3++] 확인 — 그 뒤에 삽입')

    def _cell(ct: str, src: str) -> dict:
        return {
            'cell_type': ct, 'metadata': {},
            'source': src.splitlines(keepends=True),
            **({'outputs': [], 'execution_count': None} if ct == 'code' else {}),
        }

    new_cells = [_cell('markdown', CELL_MD), _cell('code', CELL_CODE)]
    nb['cells'] = nb['cells'][:22] + new_cells + nb['cells'][22:]

    NB_PATH.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding='utf-8')
    print(f'OK — 진단 셀 2개 삽입 완료. 새 셀 수: {len(nb["cells"])}')
    print('  cell 22 (md): ## [3+++] Bootstrap 결과 진단')
    print('  cell 23 (code): bs90 로드 + 4가지 진단 출력')


if __name__ == '__main__':
    main()
