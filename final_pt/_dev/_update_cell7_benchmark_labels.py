"""Update [1c] benchmark cell (cell 7) — LSTM → Ensemble labels, formal slot notation.

Changes:
- BL_SLOTS_C dict keys: LSTM-* → Ensemble-*, (σ swap) → (σ 모델 교체)
- BL_SLOTS_C label suffix: (eq P + lam Q) → ($p^{eq}$, $q^{lam}$), fpm → ff3
- style_map dict keys: match BL_SLOTS_C
- figure titles: Korean
"""
import json, os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

nb_path = '99_main_analysis.ipynb'
nb = json.load(open(nb_path, encoding='utf-8'))

target_idx = 7
src_text = ''.join(nb['cells'][target_idx]['source'])

# 명시적 mapping (현재 → 수정). 안전하게 fragment 단위로 교체.
replacements = [
    # BL_SLOTS_C dict keys
    ("'LSTM-anchor (σ swap)':                'mat_mcap_mcap_fpm_pap'",
     "'Ensemble-anchor (σ 모델 교체)':         'mat_mcap_mcap_fpm_pap'"),
    ("'LSTM-defensive-EQ (eq P + lam Q)':    'mat_mcap_eq_lam_pap'",
     "'Ensemble-defensive ($p^{eq}$, $q^{lam}$)':    'mat_mcap_eq_lam_pap'"),
    ("'LSTM-defensive-RP (rp P + lam Q)':    'mat_mcap_rp_lam_pap'",
     "'Ensemble-defensive ($p^{rp}$, $q^{lam}$)':    'mat_mcap_rp_lam_pap'"),
    ("'LSTM-adaptive-EQ (eq P + fpm Q)':     'mat_mcap_eq_fpm_pap'",
     "'Ensemble-adaptive ($p^{eq}$, $q^{ff3}$)':     'mat_mcap_eq_fpm_pap'"),
    ("'LSTM-adaptive-RP (rp P + fpm Q)':     'mat_mcap_rp_fpm_pap'",
     "'Ensemble-adaptive ($p^{rp}$, $q^{ff3}$)':     'mat_mcap_rp_fpm_pap'"),

    # style_map dict keys
    ("'LSTM-anchor (σ swap)':               {",
     "'Ensemble-anchor (σ 모델 교체)':       {"),
    ("'LSTM-defensive-EQ (eq P + lam Q)':   {",
     "'Ensemble-defensive ($p^{eq}$, $q^{lam}$)':   {"),
    ("'LSTM-defensive-RP (rp P + lam Q)':   {",
     "'Ensemble-defensive ($p^{rp}$, $q^{lam}$)':   {"),
    ("'LSTM-adaptive-EQ (eq P + fpm Q)':    {",
     "'Ensemble-adaptive ($p^{eq}$, $q^{ff3}$)':    {"),
    ("'LSTM-adaptive-RP (rp P + fpm Q)':    {",
     "'Ensemble-adaptive ($p^{rp}$, $q^{ff3}$)':    {"),

    # 헤더 주석
    ("# ── [1c] Benchmark comparison — EQ/RP × {defensive, adaptive}",
     "# ── [1c] Benchmark comparison — Ensemble defensive / adaptive"),

    # 그림 title (영어 → 한국어)
    ("ax1.set_title('Cumulative return (rebased = 1.0 at 2010-01) — R3 위기 구간 음영', fontweight='bold')",
     "ax1.set_title('누적수익률 (2010-01 = 1.0, log scale) — R3 위기 구간 음영', fontweight='bold')"),
    ("ax1.set_ylabel('Cumulative return (log)')",
     "ax1.set_ylabel('누적수익률 (log)')"),
    ("ax2.set_title('Drawdown')",
     "ax2.set_title('Drawdown')"),  # 유지
    ("ax2.set_xlabel('Date')",
     "ax2.set_xlabel('날짜')"),
]

n_changed = 0
for old, new in replacements:
    if old in src_text:
        src_text = src_text.replace(old, new)
        n_changed += 1
    else:
        print(f'MISS: {old[:60]}...')

nb['cells'][target_idx]['source'] = src_text.splitlines(keepends=True)
nb['cells'][target_idx]['outputs'] = []
nb['cells'][target_idx]['execution_count'] = None

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f'Applied {n_changed}/{len(replacements)} replacements')
