"""Update [7] q^lam vs q^ff3 timeline plot cell (id 5dd0c5cc) — label/title/ylabel 수식 통일."""
import json, os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

nb_path = '99_main_analysis.ipynb'
nb = json.load(open(nb_path, encoding='utf-8'))

# Find cell by id
target_idx = None
for i, c in enumerate(nb['cells']):
    if c.get('id') == '5dd0c5cc':
        target_idx = i
        break
assert target_idx is not None, 'cell 5dd0c5cc not found'

new_code = r"""# ── [7] q^lam vs q^ff3 시계열 sign analysis ────────────────────
fpm_meta = loaded['mat_mcap_mcap_fpm_pap']['meta']
q_fpm = fpm_meta['Q'].copy()
q_fpm_cal = q_fpm.copy()
q_fpm_cal.index = q_fpm_cal.index + pd.offsets.MonthEnd(1)

REGIMES_T = {
    'R1 회복':   (pd.Timestamp('2010-02-28'), pd.Timestamp('2012-07-31')),
    'R2 확장':   (pd.Timestamp('2012-08-31'), pd.Timestamp('2020-01-31')),
    'R3 위기':   (pd.Timestamp('2020-02-29'), pd.Timestamp('2023-07-31')),
    'R4 정상화': (pd.Timestamp('2023-08-31'), pd.Timestamp('2026-01-31')),
}

print('='*80)
print('q^ff3 value sign distribution by regime (calendar 정렬)')
print('  q > 0 = long low-vol / short high-vol view')
print('  q < 0 = long high-vol / short low-vol view (sign flip)')
print('='*80)
print(f'{"regime":<14s}{"n_mo":>6s}{"mean q":>12s}{"median":>12s}{"% q<0":>10s}{"min":>12s}{"max":>12s}')
print('-'*78)
all_neg = (q_fpm_cal < 0).mean()*100
print(f'{"All":<14s}{len(q_fpm_cal):>6d}{q_fpm_cal.mean():>+12.5f}{q_fpm_cal.median():>+12.5f}{all_neg:>9.1f}%{q_fpm_cal.min():>+12.5f}{q_fpm_cal.max():>+12.5f}')
print('-'*78)
for lbl, (s, e) in REGIMES_T.items():
    sub = q_fpm_cal[(q_fpm_cal.index>=s)&(q_fpm_cal.index<=e)]
    if len(sub)==0: continue
    neg_pct = (sub<0).mean()*100
    print(f'{lbl:<14s}{len(sub):>6d}{sub.mean():>+12.5f}{sub.median():>+12.5f}{neg_pct:>9.1f}%{sub.min():>+12.5f}{sub.max():>+12.5f}')

lam_meta = loaded['mat_mcap_mcap_lam_pap']['meta']
q_lam = lam_meta['Q'].copy()
q_lam_cal = q_lam.copy(); q_lam_cal.index = q_lam_cal.index + pd.offsets.MonthEnd(1)
print('\n참고: q^lam (lambda_q-based) 의 음수 비율')
print(f'  All: {(q_lam_cal<0).mean()*100:.1f}%, mean={q_lam_cal.mean():+.5f}')
print(f'  → lambda_q-based 는 구조상 항상 양수, q^ff3 만 sign-flexible')

# ── 그림: q^lam vs q^ff3 timeline (단일 panel) ──
fig, ax = plt.subplots(1, 1, figsize=(14, 5))

regime_colors = {'R1 회복':'#dddddd', 'R2 확장':'#f5f5f5', 'R3 위기':'#ffe0e0', 'R4 정상화':'#e0e8ff'}
ylim_buf = max(abs(q_fpm_cal.min()), abs(q_fpm_cal.max()),
               abs(q_lam_cal.min()), abs(q_lam_cal.max())) * 1.15

for lbl, (s, e) in REGIMES_T.items():
    ax.axvspan(s, e, color=regime_colors[lbl], alpha=0.5, zorder=0)
    mid = s + (e - s)/2
    ax.text(mid, ylim_buf*0.92, lbl, ha='center', fontsize=9, color='dimgray', fontweight='bold')

ax.plot(q_lam_cal.index, q_lam_cal.values, color='#2ca02c', lw=1.2, marker='s',
        markersize=2.5, label=r'$q^{\mathrm{lam}}$ ($\lambda_q$-based)', alpha=0.85)
ax.plot(q_fpm_cal.index, q_fpm_cal.values, color='#1f77b4', lw=1.2, marker='o',
        markersize=2.5, label=r'$q^{\mathrm{ff3}}$ (FF3 회귀)', alpha=0.85)
ax.axhline(0, color='red', lw=0.8, ls='--', alpha=0.7)

ax.set_ylabel(r'$q$ value')
ax.set_title(r'$q^{\mathrm{lam}}$ vs $q^{\mathrm{ff3}}$ 월별 시계열 — $q^{\mathrm{lam}}$ 전 기간 양수, $q^{\mathrm{ff3}}$ 부호 반전 빈번')
ax.set_ylim(-ylim_buf, ylim_buf)
ax.legend(loc='upper left', fontsize=9)
ax.grid(True, alpha=0.3)
ax.tick_params(axis='x', rotation=20)

plt.tight_layout()
# plt.savefig('Figure/r4_fpm_lam.png', dpi=150, bbox_inches='tight')
plt.show()
"""

nb['cells'][target_idx]['source'] = new_code.splitlines(keepends=True)
nb['cells'][target_idx]['outputs'] = []
nb['cells'][target_idx]['execution_count'] = None

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f'Updated cell {target_idx} (id=5dd0c5cc)')
