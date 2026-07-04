# coding: utf-8
"""셀 [3++++] 삽입: 본문 표 3 + 부록 표 A.7-A.12 TSV 출력.

생성되는 7개 표:
- 본문 표 3: 13 슬롯 Sharpe (anchor 1-dim 변형)
- 부록 표 A.7: 45 슬롯 Sharpe (ω=err)
- 부록 표 A.8: 45 슬롯 Sortino (ω=err)
- 부록 표 A.9: 45 슬롯 MDD (ω=err, sig 없음)
- 부록 표 A.10: 45 슬롯 Sharpe (ω=he)
- 부록 표 A.11: 45 슬롯 Sortino (ω=he)
- 부록 표 A.12: 45 슬롯 MDD (ω=he, sig 없음)

각 TSV 블록: 워드 → "선택하여 붙여넣기 > 서식 없는 텍스트" → "텍스트를 표로 변환 (탭)"
"""
from __future__ import annotations

import json
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

NB_PATH = Path(r"C:\Users\서윤범\Desktop\temp\finance_project\final_pt\99_main_analysis.ipynb")


CELL_MD = '''## [3++++] 표 출력: 본문 표 3 + 부록 표 A.7-A.12 (TSV)

bs90 + raw 메트릭 결합 → 7개 표 TSV 형식 출력.

**Word paste 방법**:
1. 각 TSV 블록 전체 복사 (헤더 포함)
2. 워드에서 "선택하여 붙여넣기 > 서식 없는 텍스트"
3. 붙여넣은 텍스트 블록 선택 → "삽입 > 표 > 텍스트를 표로 변환" (구분자: **탭**)
4. 헤더 행 (1, 2행) 의 빈 셀 수동 병합 (period 헤더 spanning)

**셀 형식**:
- Sharpe/Sortino: `E값`, `A값`, `Δ+sig` (예: `+0.353*`)
- MDD: `E%`, `A%`, `Δ%` (sig 없음 — 경로 의존적이라 부트스트랩 미적용)
'''


CELL_CODE = '''# ── [3++++] 본문 표 3 + 부록 표 A.7-A.12 TSV 출력 ──
# 1) raw E/A/Δ 계산 (90 슬롯 × 5 기간 × 3 지표)
# 2) bs90 sig 와 merge
# 3) TSV 블록 7개 출력

PERIODS_OUT = [
    ('All', None, None),
    ('R1', '2010-01-01', '2012-06-30'),
    ('R2', '2012-07-01', '2019-12-31'),
    ('R3', '2020-01-01', '2023-06-30'),
    ('R4', '2023-07-01', '2025-12-31'),
]
PER_LBL = ['All','R1','R2','R3','R4']


def _calc_3metrics(name, start, end):
    if name not in loaded: return None
    ret = loaded[name].get('ret')
    if not isinstance(ret, pd.Series): return None
    r = ret.dropna()
    r = r[r.index <= CUTOFF]
    if start is not None: r = r[r.index >= start]
    if end is not None:   r = r[r.index <= end]
    if len(r) < 6: return None
    rfa = rf.reindex(r.index).fillna(0)
    exc = r - rfa
    vol = r.std(ddof=1) * np.sqrt(12)
    sh = float(exc.mean() * 12 / vol) if vol > 0 else np.nan
    neg = r[r < 0]
    dn = neg.std(ddof=1) * np.sqrt(12) if len(neg) >= 2 else np.nan
    so = float(exc.mean() * 12 / dn) if (dn and dn > 0) else np.nan
    cum = (1 + r).cumprod()
    mdd = float((cum / cum.cummax() - 1).min())
    return {'sharpe': sh, 'sortino': so, 'mdd': mdd}


# 90 슬롯 raw 계산
raw_rows = []
for om in ['pap', 'he']:
    for pw in ['mcap','eq','rp']:
        for pr in ['mcap','eq','rp']:
            for q in ['lam','raw','inv','vsp','fpm']:
                L_name = f'mat_{pr}_{pw}_{q}_{om}'
                A_name = L_name + '_ann'
                for plbl, s, e in PERIODS_OUT:
                    mL = _calc_3metrics(L_name, s, e)
                    mA = _calc_3metrics(A_name, s, e)
                    if not mL or not mA: continue
                    for met in ['sharpe','sortino','mdd']:
                        raw_rows.append({
                            'omega': om, 'p_w': pw, 'prior': pr, 'q': q,
                            'period': plbl, 'metric': met,
                            'E': mL[met], 'A': mA[met],
                            'delta': mL[met] - mA[met],
                        })
raw_df = pd.DataFrame(raw_rows)

# bs90 sig merge
bs90 = pd.read_pickle(OUT_DIR / 'bs90_per_slot.pkl')
merged = raw_df.merge(
    bs90[['omega','p_w','prior','q','period','metric','sig']],
    on=['omega','p_w','prior','q','period','metric'], how='left',
)
merged['sig'] = merged['sig'].fillna('')
print(f'raw + sig merge: {len(merged)} 행')


# ── 셀 포맷 헬퍼 ──
def _cell_sr(row):
    if pd.isna(row['delta']): return ('', '', '')
    return (f"{row['E']:.3f}", f"{row['A']:.3f}", f"{row['delta']:+.3f}{row['sig']}")

def _cell_mdd(row):
    if pd.isna(row['delta']): return ('', '', '')
    return (f"{row['E']*100:.2f}%", f"{row['A']*100:.2f}%", f"{row['delta']*100:+.2f}%")


def _lookup(omega, pw, pr, q, period, metric):
    row = merged[(merged['omega']==omega) & (merged['p_w']==pw) & (merged['prior']==pr) &
                 (merged['q']==q) & (merged['period']==period) & (merged['metric']==metric)]
    return row.iloc[0] if not row.empty else None


# ── 출력 1: 본문 표 3 ──
print('\\n' + '='*120)
print('<표 3> 본문 — 13 슬롯 Sharpe (anchor 1-dim 변형, TSV)')
print('='*120)
print('주: ★ = 기준 슬롯 (mcap_mcap_fpm_pap = Pyo & Lee 2018 기준)')
print()

# 헤더 2줄
hdr1 = '\\t\\t' + '\\t'.join(f'{p}\\t\\t' for p in PER_LBL)
hdr2 = '차원\\t슬롯\\t' + '\\t'.join('E\\tA\\tΔ' for _ in PER_LBL)
print(hdr1)
print(hdr2)

SLOTS_T3 = [
    ('SET 1 (q)',    'qlam',       'mcap','mcap','lam','pap'),
    ('SET 1 (q)',    'qraw',       'mcap','mcap','raw','pap'),
    ('SET 1 (q)',    'qinv',       'mcap','mcap','inv','pap'),
    ('SET 1 (q)',    'qvsp',       'mcap','mcap','vsp','pap'),
    ('SET 1 (q)',    'qff3 ★',     'mcap','mcap','fpm','pap'),
    ('SET 2 (p)',    'pmcap ★',    'mcap','mcap','fpm','pap'),
    ('SET 2 (p)',    'peq',        'mcap','eq',  'fpm','pap'),
    ('SET 2 (p)',    'prp',        'mcap','rp',  'fpm','pap'),
    ('SET 3 (wmkt)', 'wmcap ★',    'mcap','mcap','fpm','pap'),
    ('SET 3 (wmkt)', 'weq',        'eq',  'mcap','fpm','pap'),
    ('SET 3 (wmkt)', 'wrp',        'rp',  'mcap','fpm','pap'),
    ('SET 4 (ω)',    'ωerr ★',     'mcap','mcap','fpm','pap'),
    ('SET 4 (ω)',    'ωhe',        'mcap','mcap','fpm','he'),
]

for dim, slot, pr, pw, q, om in SLOTS_T3:
    cells = [dim, slot]
    for plbl in PER_LBL:
        r = _lookup(om, pw, pr, q, plbl, 'sharpe')
        if r is None:
            cells.extend(['', '', ''])
        else:
            E, A, D = _cell_sr(r)
            cells.extend([E, A, D])
    print('\\t'.join(cells))


# ── 출력 2~7: 부록 표 A.7~A.12 ──
def print_appendix(metric, omega, table_name, omega_label):
    note = ''
    if metric == 'mdd':
        note = ' — sig 없음 (MDD 경로 의존적, 부트스트랩 미적용)'
    print('\\n' + '='*120)
    print(f'<{table_name}> 부록 — 45 슬롯 {metric.capitalize()}, ω={omega_label}{note} (TSV)')
    print('='*120)

    hdr1 = '\\t\\t\\t' + '\\t'.join(f'{p}\\t\\t' for p in PER_LBL)
    hdr2 = 'p\\twmkt\\tq\\t' + '\\t'.join('E\\tA\\tΔ' for _ in PER_LBL)
    print(hdr1)
    print(hdr2)

    for pw in ['mcap','eq','rp']:
        for pr in ['mcap','eq','rp']:
            for q in ['lam','raw','inv','vsp','fpm']:
                # ★ 표시 (anchor: pmcap wmcap qff3 only)
                anchor_mark = ' ★' if (pw=='mcap' and pr=='mcap' and q=='fpm') else ''
                cells = [f'p{pw}', f'w{pr}', f'q{q}{anchor_mark}']
                for plbl in PER_LBL:
                    r = _lookup(omega, pw, pr, q, plbl, metric)
                    if r is None:
                        cells.extend(['', '', ''])
                    else:
                        E, A, D = _cell_mdd(r) if metric == 'mdd' else _cell_sr(r)
                        cells.extend([E, A, D])
                print('\\t'.join(cells))


print_appendix('sharpe',  'pap', '표 A.7',  'err')
print_appendix('sortino', 'pap', '표 A.8',  'err')
print_appendix('mdd',     'pap', '표 A.9',  'err')
print_appendix('sharpe',  'he',  '표 A.10', 'he')
print_appendix('sortino', 'he',  '표 A.11', 'he')
print_appendix('mdd',     'he',  '표 A.12', 'he')


print('\\n' + '='*120)
print('완료 — 위 7개 TSV 블록을 워드에 paste 하세요.')
print('  방법: TSV 복사 → 워드 "선택하여 붙여넣기 > 서식 없는 텍스트" → "삽입 > 표 > 텍스트를 표로 변환 (탭)"')
print('  헤더 1행 (period spanning) 빈 셀은 워드에서 수동 셀 병합')
print('='*120)


# ── 표 각주 안내 (워드 표 아래 작은 글씨) ──
print('\\n' + '='*120)
print('각 표 각주 (워드 표 아래 9pt 작은 글씨)')
print('='*120)
print("""
[본문 표 3 각주]
주: ★ = Pyo & Lee (2018) 기준 슬롯 (mcap_mcap_fpm_pap). E = 앙상블, A = ANN, Δ = E - A.
   별표는 본문 §4.1 에서 설명한 정상 블록 부트스트랩 검정 결과 (* p<.05, ** p<.01, *** p<.001).
   페어된 월별 수익률을 동시 재추출하여 페어링 및 자기상관 구조를 보존 (B = 10,000).

[부록 표 A.7~A.8, A.10~A.11 각주 — Sharpe/Sortino]
주: p = P 행렬 가중 방식, wmkt = 사전 분포, q = 뷰 산출 방식. E = 앙상블, A = ANN, Δ = E - A.
   별표는 본문 §4.1 동일 정상 블록 부트스트랩 검정 결과 (* p<.05, ** p<.01, *** p<.001).
   ★ = Pyo & Lee (2018) 기준 슬롯.

[부록 표 A.9, A.12 각주 — MDD]
주: MDD = 최대낙폭. 음수가 손실이므로 Δ > 0 이 앙상블이 덜 빠진 경우.
   MDD 는 경로 의존적 통계량이므로 부트스트랩 추론을 적용하지 않으며, 본 표에서는 raw 값과 차이만 보고.
""")
'''


def main() -> None:
    nb = json.loads(NB_PATH.read_text(encoding='utf-8'))
    print(f'현재 셀 수: {len(nb["cells"])}')

    # cell 23 = [3+++] code 확인
    c23 = ''.join(nb['cells'][23]['source'])
    assert '[3+++]' in c23 or 'bs90' in c23.lower(), f'cell 23 not [3+++]: {c23[:100]}'
    print('cell 23 = [3+++] 진단 셀 확인')

    def _cell(ct, src):
        return {
            'cell_type': ct, 'metadata': {},
            'source': src.splitlines(keepends=True),
            **({'outputs': [], 'execution_count': None} if ct == 'code' else {}),
        }

    new_cells = [_cell('markdown', CELL_MD), _cell('code', CELL_CODE)]
    nb['cells'] = nb['cells'][:24] + new_cells + nb['cells'][24:]

    NB_PATH.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding='utf-8')
    print(f'OK — 출력 셀 2개 삽입. 새 셀 수: {len(nb["cells"])}')
    print('  cell 24 (md): ## [3++++] 표 출력 안내')
    print('  cell 25 (code): 7개 TSV 블록 + 각주 출력')


if __name__ == '__main__':
    main()
