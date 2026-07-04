"""Update [3d] Period × Dimension marginal cell (cell 14 in 99_main_analysis.ipynb).

Apply formal notation labels + Ensemble label + Korean suptitle, keeping slot counts.
"""
import json, os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

nb_path = '99_main_analysis.ipynb'
nb = json.load(open(nb_path, encoding='utf-8'))

target_idx = None
for i, c in enumerate(nb['cells']):
    if c['cell_type'] == 'code' and '_paired_box_d' in ''.join(c['source']):
        target_idx = i
        break
assert target_idx is not None, '[3d] cell not found'

new_code = '''# ── [3d] Period × Dimension marginal — 5 periods × 3 dimensions ──
# §5.3 보조 figure: regime별 슬롯 차원 효과를 모두 보여주는 detail view

_periods = list(dict.fromkeys(df_p_sh.columns.get_level_values("period")))

# ── 라벨 매핑 (코드명 → 논문 표기) ──
Q_DISPLAY = {
    'lam': r'$q^{\\mathrm{lam}}$',
    'raw': r'$q^{\\mathrm{raw}}$',
    'inv': r'$q^{\\mathrm{inv}}$',
    'vsp': r'$q^{\\mathrm{vsp}}$',
    'fpm': r'$q^{\\mathrm{ff3}}$',   # 코드 fpm → 논문 ff3
}
P_DISPLAY = {
    'mcap': r'$\\mathbf{p}^{\\mathrm{mcap}}$',
    'eq':   r'$\\mathbf{p}^{\\mathrm{eq}}$',
    'rp':   r'$\\mathbf{p}^{\\mathrm{rp}}$',
}
PRIOR_DISPLAY = {
    'mcap': r'$\\mathbf{w}^{\\mathrm{mcap}}$',
    'eq':   r'$\\mathbf{w}^{\\mathrm{eq}}$',
    'rp':   r'$\\mathbf{w}^{\\mathrm{rp}}$',
}

def _paired_box_d(ax, categories, data_L, data_A, title, ylabel="Sharpe"):
    n = len(categories)
    pos = np.arange(n)
    bpL = ax.boxplot(data_L, positions=pos - 0.2, widths=0.35, patch_artist=True,
                      showmeans=True, meanprops=dict(marker="D", markerfacecolor="black",
                      markeredgecolor="black", markersize=3))
    bpA = ax.boxplot(data_A, positions=pos + 0.2, widths=0.35, patch_artist=True,
                      showmeans=True, meanprops=dict(marker="D", markerfacecolor="black",
                      markeredgecolor="black", markersize=3))
    for patch in bpL["boxes"]: patch.set_facecolor("#d62728"); patch.set_alpha(0.55)
    for patch in bpA["boxes"]: patch.set_facecolor("#1f77b4"); patch.set_alpha(0.55)
    ax.set_xticks(pos); ax.set_xticklabels(categories, fontsize=10)
    ax.set_title(title, fontsize=10, fontweight="bold")
    ax.set_ylabel(ylabel, fontsize=9)
    ax.grid(True, alpha=0.3, axis="y")
    return bpL, bpA

n_periods = len(_periods)
fig, axes = plt.subplots(n_periods, 3, figsize=(15, 2.8*n_periods), sharey="row")
if n_periods == 1: axes = axes.reshape(1, -1)

for r, p in enumerate(_periods):
    p_L = df_p_sh[(p, "L")]; p_A = df_p_sh[(p, "A")]

    # Q dim
    data_L = [p_L.xs(q, level="q").dropna().values for q in Q_MODES]
    data_A = [p_A.xs(q, level="q").dropna().values for q in Q_MODES]
    q_ticks = [Q_DISPLAY[q] for q in Q_MODES]
    bpL, bpA = _paired_box_d(axes[r, 0], q_ticks, data_L, data_A,
                              f"{p} — $q$ (9 슬롯)")

    # P dim
    data_L = [p_L.xs(pw, level="p_w").dropna().values for pw in P_WEIGHTS]
    data_A = [p_A.xs(pw, level="p_w").dropna().values for pw in P_WEIGHTS]
    p_ticks = [P_DISPLAY[pw] for pw in P_WEIGHTS]
    _paired_box_d(axes[r, 1], p_ticks, data_L, data_A,
                  f"{p} — $\\\\mathbf{{p}}$ (15 슬롯)")

    # Prior dim
    data_L = [p_L.xs(pr, level="prior").dropna().values for pr in PRIORS]
    data_A = [p_A.xs(pr, level="prior").dropna().values for pr in PRIORS]
    pr_ticks = [PRIOR_DISPLAY[pr] for pr in PRIORS]
    _paired_box_d(axes[r, 2], pr_ticks, data_L, data_A,
                  f"{p} — $\\\\mathbf{{w}}_{{mkt}}$ (15 슬롯)")

fig.legend([bpL["boxes"][0], bpA["boxes"][0]], ["Ensemble", "ANN"],
           loc="upper right", bbox_to_anchor=(0.99, 0.99), fontsize=10, ncol=2)
plt.suptitle("구간 × 차원별 주변 분포 — Sharpe",
             fontsize=13, fontweight="bold", y=1.005)
plt.tight_layout()
plt.show()

# 콘솔 요약: period × dimension × value 평균 Δ
print("="*78)
print("Period × Dimension × Value — mean Δ Sharpe (Ensemble − ANN)")
print("="*78)
hdr = f"  {'period':<12s}" + "".join(f"{v:>9s}" for v in (Q_MODES + P_WEIGHTS + PRIORS))
print(hdr); print("  " + "-"*(len(hdr)-2))
for p in _periods:
    p_L = df_p_sh[(p, "L")]; p_A = df_p_sh[(p, "A")]
    cells = []
    for q in Q_MODES:
        d = (p_L - p_A).xs(q, level="q").dropna()
        cells.append(f"{d.mean():>+9.3f}")
    for pw in P_WEIGHTS:
        d = (p_L - p_A).xs(pw, level="p_w").dropna()
        cells.append(f"{d.mean():>+9.3f}")
    for pr in PRIORS:
        d = (p_L - p_A).xs(pr, level="prior").dropna()
        cells.append(f"{d.mean():>+9.3f}")
    print(f"  {p:<12s}" + "".join(cells))
'''

nb['cells'][target_idx]['source'] = new_code.splitlines(keepends=True)
nb['cells'][target_idx]['outputs'] = []
nb['cells'][target_idx]['execution_count'] = None

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print(f'Updated cell {target_idx}')
