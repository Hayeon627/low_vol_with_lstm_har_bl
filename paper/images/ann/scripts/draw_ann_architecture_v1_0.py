# -*- coding: utf-8 -*-
"""
draw_ann_architecture_v1_0.py
ANN(Pyo & Lee, 2018) 변동성 예측 기준모델 아키텍처 — AI 생성 레퍼런스 재현 v1.0

구조: 입력층(x1..x10, 월별 실현변동성) → 은닉층(4 뉴런, ReLU) → 출력층(1 뉴런)
출력: ŷ_t = log(σ_{t+21})

* 색은 레퍼런스(AI 생성본)를 그대로 따른다: 회색 입력 / 초록 은닉(ReLU) / 분홍 출력.
폰트: Windows 'Malgun Gothic' 우선, 없으면 NanumGothic/Noto CJK로 자동 대체.
"""
import os
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import matplotlib.font_manager as fm

# ── 폰트 ───────────────────────────────────────────────────────
_avail = {f.name for f in fm.fontManager.ttflist}
for _cand in ['Malgun Gothic', 'NanumGothic', 'Noto Sans CJK KR',
              'Noto Sans KR', 'AppleGothic', 'DejaVu Sans']:
    if _cand in _avail:
        plt.rcParams['font.family'] = _cand
        break
plt.rcParams['axes.unicode_minus'] = False

# ── 색상 (레퍼런스 그대로) ─────────────────────────────────────
INPUT_FC,  INPUT_EC  = '#bcbcbc', '#6f6f6f'   # 입력 (회색)
HIDDEN_FC, HIDDEN_EC = '#a9d6a9', '#5aa15a'   # 은닉 ReLU (초록)
OUTPUT_FC, OUTPUT_EC = '#f3aab9', '#d56e82'   # 출력 (분홍)
LINE  = '#c4c4c4'                              # 연결선
INK   = '#1f2a33'                              # 본문 텍스트
RELU_TX = '#1f4d1f'                            # ReLU 글자

# ── 캔버스 (정사각) ────────────────────────────────────────────
fig = plt.figure(figsize=(10, 10), dpi=200)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.set_aspect('equal')
ax.axis('off')
ax.add_patch(plt.Rectangle((0, 0), 100, 100, facecolor='white', edgecolor='none', zorder=0))

# ── 헬퍼: 뉴런 ─────────────────────────────────────────────────
def neuron(cx, cy, r, fc, ec, label='', tc=INK, fs=14):
    ax.add_patch(Circle((cx, cy), r, facecolor=fc, edgecolor=ec, lw=1.7, zorder=3))
    if label:
        ax.text(cx, cy, label, ha='center', va='center', color=tc,
                fontsize=fs, fontweight='bold', zorder=4)

# ── 좌표 ───────────────────────────────────────────────────────
INPUT_X, HIDDEN_X, OUTPUT_X = 25, 48, 68
inputs  = [(INPUT_X, 75), (INPUT_X, 57), (INPUT_X, 22)]          # x1, x2, x10 (가시)
hiddens = [(HIDDEN_X, 78), (HIDDEN_X, 58), (HIDDEN_X, 38), (HIDDEN_X, 18)]
out     = (OUTPUT_X, 48)

# ── 연결선 (완전연결, 뉴런 뒤) ─────────────────────────────────
for ix, iy in inputs:
    for hx, hy in hiddens:
        ax.plot([ix, hx], [iy, hy], color=LINE, lw=0.8, zorder=1)
for hx, hy in hiddens:
    ax.plot([hx, out[0]], [hy, out[1]], color=LINE, lw=0.8, zorder=1)

# ── 입력 뉴런 ──────────────────────────────────────────────────
neuron(INPUT_X, 75, 5.0, INPUT_FC, INPUT_EC, r"$x_1$",    fs=15)
neuron(INPUT_X, 57, 5.0, INPUT_FC, INPUT_EC, r"$x_2$",    fs=15)
neuron(INPUT_X, 22, 5.0, INPUT_FC, INPUT_EC, r"$x_{10}$", fs=13)
for dy in (44, 41, 38):                                          # 생략 점(⋮)
    ax.add_patch(Circle((INPUT_X, dy), 0.55, facecolor='#6f6f6f', edgecolor='none', zorder=3))

# ── 은닉 뉴런 (ReLU) ───────────────────────────────────────────
for hx, hy in hiddens:
    neuron(hx, hy, 5.7, HIDDEN_FC, HIDDEN_EC, "ReLU", tc=RELU_TX, fs=12)

# ── 출력 뉴런 ──────────────────────────────────────────────────
neuron(out[0], out[1], 6.3, OUTPUT_FC, OUTPUT_EC, "")

# ── 출력 화살표 + 수식 ─────────────────────────────────────────
ax.annotate('', xy=(80, 48), xytext=(out[0] + 6.3, 48),
            arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.8, mutation_scale=18), zorder=4)
ax.text(81, 48, r"$\hat{y}_t = \log(\sigma_t)$", ha='left', va='center', fontsize=12.5, color=INK, zorder=4)

# ── 층 라벨 (상단) ─────────────────────────────────────────────
ax.text(INPUT_X,  92, "입력층\n(월별 실현변동성 입력)", ha='center', va='center', fontsize=12, color=INK, fontweight='bold')
ax.text(HIDDEN_X, 92, "은닉층\n(4개 뉴런, ReLU 활성화)", ha='center', va='center', fontsize=12, color=INK, fontweight='bold')
ax.text(OUTPUT_X, 92, "출력층\n(1개 뉴런)", ha='center', va='center', fontsize=12, color=INK, fontweight='bold')


# ── 좌측 입력 정의 ─────────────────────────────────────────────
ax.text(18, 75, r"$x_1 = \log(\sigma_{t-1})$",    ha='right', va='center', fontsize=10.5, color=INK)
ax.text(18, 57, r"$x_2 = \log(\sigma_{t-2})$",    ha='right', va='center', fontsize=10.5, color=INK)
ax.text(18, 22, r"$x_{10} = \log(\sigma_{t-10})$", ha='right', va='center', fontsize=10.5, color=INK)

# ── 층 라벨 (하단, 레퍼런스 중복 표기) ─────────────────────────

# ── 저장 ───────────────────────────────────────────────────────
out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
out_path = os.path.join(out_dir, "ann_architecture_v1_0.png")
plt.savefig(out_path, dpi=200, facecolor='white')
plt.close()
print("saved:", out_path)
