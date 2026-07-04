# -*- coding: utf-8 -*-
"""
draw_lstm_v1_0.py
LSTM 셀 구조 — AI 생성 레퍼런스 재현 v1.0
폰트: BL v3.0과 동일 (Malgun Gothic 우선, 없으면 NanumGothic/Noto CJK). 수식은 기본 mathtext.
"""
import os
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch
import matplotlib.font_manager as fm

_avail = {f.name for f in fm.fontManager.ttflist}
for _cand in ['Malgun Gothic', 'NanumGothic', 'Noto Sans CJK KR', 'Noto Sans KR', 'AppleGothic', 'DejaVu Sans']:
    if _cand in _avail:
        plt.rcParams['font.family'] = _cand
        break
plt.rcParams['axes.unicode_minus'] = False

# ── 색상 ──
CELL_FC, CELL_EC = '#e9eff5', '#d3dbe3'
A_BLUE = '#5b8fd0'
CIRC_FC, CIRC_EC = '#a8c6e8', '#5d8dc9'
SYM = '#28323c'
GX_FC, GX_EC = '#d8d8d8', '#9a9a9a'
A_GRAY = '#9a9a9a'
GRN_FC, GRN_EC = '#b9d8a8', '#7bb15f'
PNK_FC, PNK_EC = '#f5b8b8', '#dd8d8d'
INK = '#26303a'

fig = plt.figure(figsize=(10, 10), dpi=200)
ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 100); ax.set_ylim(0, 100)
ax.set_aspect('equal'); ax.axis('off')
ax.add_patch(plt.Rectangle((0, 0), 100, 100, facecolor='white', edgecolor='none', zorder=0))

# ── 좌표 ──
X_C1, X_C2, X_C3, X_C4 = 25, 38.5, 51, 64
X_TANH, X_HTUP, X_OUT = 81, 85.5, 92
Y_HTTOP, Y_CELLTOP, Y_TLAB, Y_C = 78.5, 70, 67.5, 63
Y_TANH, Y_GX, Y_OUTX, Y_BLAB = 56, 50, 46, 40.5
Y_PINK, Y_H, Y_CELLBOT, Y_XT = 36, 26, 20, 12.5
X_XT = 20
RB, RG = 3.2, 2.8   # 원 반지름(파랑/회색)

# 셀 박스
ax.add_patch(FancyBboxPatch((15, Y_CELLBOT), 73, Y_CELLTOP - Y_CELLBOT,
             boxstyle="round,pad=0,rounding_size=2.5", fc=CELL_FC, ec=CELL_EC, lw=1.5, zorder=1))

def arrow(p0, p1, color=A_BLUE, cs="arc3,rad=0", lw=2.0, ms=15, z=5):
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle='-|>', mutation_scale=ms,
                 color=color, lw=lw, connectionstyle=cs, shrinkA=0, shrinkB=0, zorder=z))

def line(p0, p1, color=A_BLUE, lw=2.0, z=4):
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=color, lw=lw, solid_capstyle='round', zorder=z)

def circ(cx, cy, r, sym, fc=CIRC_FC, ec=CIRC_EC, sc=SYM, fs=24):
    ax.add_patch(Circle((cx, cy), r, facecolor=fc, edgecolor=ec, lw=2.0, zorder=6))
    ax.text(cx, cy, sym, ha='center', va='center', color=sc, fontsize=fs, zorder=7)

def rbox(cx, cy, w, h, s, fc, ec, fs=13, tc=INK):
    ax.add_patch(FancyBboxPatch((cx - w/2, cy - h/2), w, h, boxstyle="round,pad=0,rounding_size=1.2",
                 fc=fc, ec=ec, lw=1.8, zorder=6))
    ax.text(cx, cy, s, ha='center', va='center', color=tc, fontsize=fs, zorder=7, linespacing=1.4)

# ── 원/박스 ──
circ(X_C1, Y_C, RB, "×")
circ(X_C3, Y_C, RB, "+")
circ(X_C3, Y_GX, RG, "×", fc=GX_FC, ec=GX_EC, sc='#555', fs=20)
circ(X_TANH, Y_OUTX, RB, "×")
rbox(X_TANH, Y_TANH, 8.0, 5.0, "tanh", GRN_FC, GRN_EC, fs=14)
rbox(X_C1, Y_PINK, 11, 6.4, "시그모이드\n($\\sigma$)", PNK_FC, PNK_EC, fs=12)
rbox(X_C2, Y_PINK, 11, 6.4, "시그모이드\n($\\sigma$)", PNK_FC, PNK_EC, fs=12)
rbox(X_C3, Y_PINK, 11, 6.4, "tanh", PNK_FC, PNK_EC, fs=13)
rbox(X_C4, Y_PINK, 11, 6.4, "시그모이드\n($\\sigma$)", PNK_FC, PNK_EC, fs=12)

# ── 게이트 라벨 ──
ax.text(X_C1, Y_TLAB, "망각 게이트", ha='center', fontsize=14, fontweight='bold', color=INK, zorder=8)
ax.text(X_C3, Y_TLAB, "입력 게이트", ha='center', fontsize=14, fontweight='bold', color=INK, zorder=8)
ax.text(X_C1, Y_BLAB, "망각 게이트", ha='center', fontsize=12.5, fontweight='bold', color=INK, zorder=8)
ax.text(X_C2, Y_BLAB, "입력 게이트", ha='center', fontsize=12.5, fontweight='bold', color=INK, zorder=8)
ax.text(X_C3, Y_BLAB, "후보 기억", ha='center', fontsize=12.5, fontweight='bold', color=INK, zorder=8)
ax.text(X_C4, Y_BLAB, "출력 게이트", ha='center', fontsize=12.5, fontweight='bold', color=INK, zorder=8)

# ── 변수 라벨 (math) ──
ax.text(8, Y_C,    r"$c_{t-1}$", ha='center', va='center', fontsize=21, color=INK)
ax.text(8, Y_H,    r"$h_{t-1}$", ha='center', va='center', fontsize=21, color=INK)
ax.text(X_XT, Y_XT, r"$x_t$",    ha='center', va='center', fontsize=21, color=INK)
ax.text(X_OUT, Y_C,    r"$c_t$", ha='center', va='center', fontsize=21, color=INK)
ax.text(X_OUT, Y_OUTX, r"$h_t$", ha='center', va='center', fontsize=21, color=INK)
ax.text(X_HTUP, Y_HTTOP, r"$h_t$", ha='center', va='center', fontsize=21, color=INK)

# ── 데이터 흐름 (파랑) ──
arrow((11.5, Y_C), (X_C1 - RB, Y_C))
arrow((X_C1 + RB, Y_C), (X_C3 - RB, Y_C))
arrow((X_C3 + RB, Y_C), (90.0, Y_C))
arrow((76, Y_C), (X_TANH, Y_TANH + 2.6), cs="arc3,rad=-0.4")     # c-line -> tanh
arrow((X_TANH, Y_TANH - 2.6), (X_TANH, Y_OUTX + RB))             # tanh -> output×
arrow((X_TANH + RB, Y_OUTX), (90.0, Y_OUTX))                     # output× -> h_t(right)
arrow((X_HTUP, Y_OUTX), (X_HTUP, Y_HTTOP - 2.2))                 # 위로 -> h_t(top)

# h_{t-1}, x_t 입력선 + 분기
line((11.5, Y_H), (X_C4, Y_H))
line((X_XT, Y_XT + 1.4), (X_XT, Y_H))
for xb in (X_C1, X_C2, X_C3, X_C4):
    arrow((xb, Y_H), (xb, Y_PINK - 3.2))

# ── 게이트 -> 노드 (회색) ──
arrow((X_C1, Y_PINK + 3.2), (X_C1, Y_C - RB), color=A_GRAY)
arrow((X_C2, Y_PINK + 3.2), (X_C3 - RG, Y_GX), color=A_GRAY, cs="angle,angleA=90,angleB=0,rad=6")
arrow((X_C3, Y_PINK + 3.2), (X_C3, Y_GX - RG), color=A_GRAY)
arrow((X_C3, Y_GX + RG), (X_C3, Y_C - RB), color=A_GRAY)
arrow((X_C4, Y_PINK + 3.2), (X_TANH - RB, Y_OUTX), color=A_GRAY, cs="angle,angleA=90,angleB=0,rad=6")

out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
out_path = os.path.join(out_dir, "lstm_v1_0.png")
plt.savefig(out_path, dpi=200, facecolor='white')
plt.close()
print("saved:", out_path)
