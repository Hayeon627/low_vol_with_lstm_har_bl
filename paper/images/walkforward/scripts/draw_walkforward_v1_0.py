# -*- coding: utf-8 -*-
"""
draw_walkforward_v1_0.py
Walk-Forward 슬라이딩 구조 — 논문 디자인(BL 도식 팔레트) v1.0
기간 2010/01/01 ~ 2025/12/31, 월(=21영업일) 슬라이드 → 192 folds.
각 fold = IS(1250) + Purge(21) + Embargo(63) + OOS(21) (총 1355영업일).
폰트: Windows 'Malgun Gothic' 우선, 없으면 NanumGothic/Noto CJK로 자동 대체.
"""
import os
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import matplotlib.font_manager as fm

_avail = {f.name for f in fm.fontManager.ttflist}
for _cand in ['Malgun Gothic', 'NanumGothic', 'Noto Sans CJK KR', 'Noto Sans KR', 'AppleGothic', 'DejaVu Sans']:
    if _cand in _avail:
        plt.rcParams['font.family'] = _cand
        break
plt.rcParams['axes.unicode_minus'] = False

DARK_BLUE, ACCENT_BLUE, ACCENT_RED = '#1a2a3a', '#0d47a1', '#b71c1c'
BORDER_CLR, CARD_BG, CARD_BORDER = '#2c3e50', '#f8f9fa', '#cfd8dc'
TX_SEC, TX_MUTE, WHITE = '#37474f', '#8a97a8', '#ffffff'
IS_COL, PG_COL, EM_COL, OOS_COL = DARK_BLUE, ACCENT_BLUE, '#aebfd2', ACCENT_RED

# 캔버스: 세로 여백 축소 (6.5->5.8, ylim 0-44)
fig = plt.figure(figsize=(13, 5.8), dpi=200)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 100); ax.set_ylim(0, 44); ax.axis('off')
ax.add_patch(plt.Rectangle((0, 0), 100, 44, facecolor=WHITE, edgecolor='none', zorder=0))

IS_F, PG_F, EM_F, OOS_F = 1250, 21, 63, 21
TOT = IS_F + PG_F + EM_F + OOS_F
L, H = 52, 3.0

def fold_bar(x0, yc):
    x = x0
    for val, col in [(IS_F, IS_COL), (PG_F, PG_COL), (EM_F, EM_COL), (OOS_F, OOS_COL)]:
        w = L * val / TOT
        ax.add_patch(plt.Rectangle((x, yc - H/2), w, H, facecolor=col, edgecolor=WHITE, lw=0.5, zorder=3))
        x += w
    return x

ax.text(50, 41.3, "Walk-Forward 슬라이딩 구조", ha='center', fontsize=16, fontweight='bold', color=DARK_BLUE)

leg_items = [("IS (1250일)", IS_COL), ("Purging (21일)", PG_COL),
             ("Embargo (63일)", EM_COL), ("OOS (21일)", OOS_COL)]
LEG_FS, DOT_R, DOT_GAP, ITEM_GAP, LEG_Y = 8.0, 0.6, 1.1, 3.4, 37.6
fig.canvas.draw()
_rend = fig.canvas.get_renderer()
_inv = ax.transData.inverted()
def _txt_w(s):
    _t = ax.text(0, -20, s, fontsize=LEG_FS)
    _bb = _t.get_window_extent(renderer=_rend); _t.remove()
    return abs(_inv.transform((_bb.x1, _bb.y0))[0] - _inv.transform((_bb.x0, _bb.y0))[0])
_lw = [_txt_w(s) for s, _ in leg_items]
_itemw = [DOT_R * 2 + DOT_GAP + w for w in _lw]
_total = sum(_itemw) + ITEM_GAP * (len(leg_items) - 1)
x = max(18.0, min(45.5 - _total / 2, 73.0 - _total))
for (name, col), iw, lw in zip(leg_items, _itemw, _lw):
    ec = '#8aa0bd' if col == EM_COL else 'none'
    ax.add_patch(plt.Circle((x + DOT_R, LEG_Y), DOT_R, facecolor=col, edgecolor=ec, lw=0.7, zorder=4))
    ax.text(x + DOT_R * 2 + DOT_GAP, LEG_Y, name, va='center', ha='left', fontsize=LEG_FS, color=TX_SEC)
    x += iw + ITEM_GAP

Y1, Y2, YN = 31.5, 26.0, 9.5
f1_end = fold_bar(18.0, Y1); ax.text(16, Y1, "Fold 1", ha='right', va='center', fontsize=10, fontweight='bold', color=DARK_BLUE)
f2_end = fold_bar(20.5, Y2); ax.text(16, Y2, "Fold 2", ha='right', va='center', fontsize=10, fontweight='bold', color=DARK_BLUE)
fN_end = fold_bar(25.0, YN); ax.text(16, YN, "Fold 192", ha='right', va='center', fontsize=10, fontweight='bold', color=DARK_BLUE)

for dy in (20.5, 17.5, 14.5):
    ax.add_patch(plt.Circle((14.0, dy), 0.30, facecolor=TX_MUTE, edgecolor='none', zorder=3))
for dx, dy in [(45, 20.5), (49, 17.5), (53, 14.5)]:
    ax.add_patch(plt.Circle((dx, dy), 0.38, facecolor=TX_MUTE, edgecolor='none', zorder=3))

ax.text(24, 35.0, "Step = 21d (매월 슬라이드)", ha='center', fontsize=9, fontweight='bold', color=ACCENT_RED)
ax.annotate('', xy=(20.7, 27.3), xytext=(18.2, 32.8),
            arrowprops=dict(arrowstyle='-|>', color=ACCENT_RED, lw=1.6, shrinkA=0, shrinkB=0, mutation_scale=14), zorder=4)

ax.plot([18, 18], [3.4, 33.5], color=CARD_BORDER, lw=1.0, ls=(0, (1.5, 3)), zorder=1)
ax.plot([fN_end, fN_end], [3.4, 11.5], color=CARD_BORDER, lw=1.0, ls=(0, (1.5, 3)), zorder=1)
ax.text(18, 2.0, "2010/01/01", ha='center', fontsize=10.5, fontweight='bold', color=DARK_BLUE)
ax.text(fN_end, 2.0, "2025/12/31", ha='center', fontsize=10.5, fontweight='bold', color=DARK_BLUE)

ax.add_patch(FancyBboxPatch((75, 25.5), 20.5, 14.5, boxstyle="round,pad=0,rounding_size=1.3", fc=CARD_BG, ec=CARD_BORDER, lw=1.2, zorder=2))
info = [("IS", "In-Sample 학습 구간"), ("Purging", "target leakage 차단"),
        ("Embargo", "ACF spillover 차단"), ("OOS", "Out-Of-Sample 평가 구간")]
KEY_X, COLON_X, VAL_X = 76.8, 81.8, 82.8
iy = 37.4
for key, val in info:
    ax.text(KEY_X, iy, key, ha='left', va='center', fontsize=7.2, fontweight='bold', color=DARK_BLUE)
    ax.text(COLON_X, iy, ":", ha='center', va='center', fontsize=7.2, color=TX_SEC)
    ax.text(VAL_X, iy, val, ha='left', va='center', fontsize=7.0, color=TX_SEC)
    iy -= 3.4

# 콜아웃: 컴팩트 박스 + 브래킷 + 곡선 화살표
pe0 = 20.5 + L * IS_F / TOT
pe1 = pe0 + L * (PG_F + EM_F) / TOT
pe_cx = (pe0 + pe1) / 2
yb = Y2 - H/2 - 0.5
ax.plot([pe0, pe0, pe1, pe1], [yb, yb - 0.7, yb - 0.7, yb], color=BORDER_CLR, lw=1.3, zorder=4)
ax.add_patch(FancyBboxPatch((77, 11.8), 19.5, 5.4, boxstyle="round,pad=0,rounding_size=1.4", fc='#eef2f7', ec=BORDER_CLR, lw=1.3, zorder=2))
ax.text(86.75, 14.5, "train/test 시간 누수 방지", ha='center', va='center', fontsize=10, fontweight='bold', color=DARK_BLUE, zorder=3)
ax.annotate('', xy=(77.0, 14.8), xytext=(pe_cx, yb - 0.9),
            arrowprops=dict(arrowstyle='-|>', color=BORDER_CLR, lw=1.4, connectionstyle="arc3,rad=0.45", mutation_scale=14), zorder=2)

out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
out_path = os.path.join(out_dir, "walkforward_v1_0.png")
plt.savefig(out_path, dpi=200, facecolor=WHITE)
plt.close()
print("saved:", out_path)
