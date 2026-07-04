# -*- coding: utf-8 -*-
"""
draw_bl_framework_v3_0.py
통합 Black-Litterman 프레임워크 — 세로형(포트레이트) 인포그래픽 v3.0

레이아웃: 세로 단계 흐름(① 변동성 → ② 슬롯 설계 → ③ 분포 → ④ 사후/최적화)
디자인: 기존 v2.x 코드 팔레트(흰 배경 + 네이비 보더 + ACCENT_BLUE/RED/GREEN)와
        Malgun Gothic 폰트를 그대로 따른다.

폰트: Windows의 'Malgun Gothic' 우선, 없으면 NanumGothic/Noto CJK로 자동 대체.
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle
import matplotlib.font_manager as fm

# ──────────────────────────────────────────────────────────────
# 0. 폰트 (기존 코드와 동일하게 Malgun Gothic 우선)
# ──────────────────────────────────────────────────────────────
_avail = {f.name for f in fm.fontManager.ttflist}
for _cand in ['Malgun Gothic', 'NanumGothic', 'Noto Sans CJK KR',
              'Noto Sans KR', 'AppleGothic', 'DejaVu Sans']:
    if _cand in _avail:
        plt.rcParams['font.family'] = _cand
        break
plt.rcParams['axes.unicode_minus'] = False

# ──────────────────────────────────────────────────────────────
# 1. 색상 팔레트 (기존 v2.x 코드 그대로)
# ──────────────────────────────────────────────────────────────
DARK_BLUE    = '#1a2a3a'
LIGHT_BG     = '#fcfdfe'
BORDER_CLR   = '#2c3e50'
CARD_BG      = '#f8f9fa'
CARD_BORDER  = '#cfd8dc'
ACCENT_BLUE  = '#0d47a1'
ACCENT_RED   = '#b71c1c'
ACCENT_GREEN = '#1b5e20'
TX_SEC       = '#37474f'   # 보조 텍스트
TX_MUTE      = '#78909c'   # 흐린 라벨
WHITE        = '#ffffff'

# 변동성 3분위 바(기존 코드의 분위수 셀 색)
BAR_LOW_FC,  BAR_LOW_EC,  BAR_LOW_TX  = '#dbe9f6', '#4a90e2', '#0d47a1'
BAR_MID_FC,  BAR_MID_EC,  BAR_MID_TX  = '#eceff1', '#90a4ae', '#37474f'
BAR_HIGH_FC, BAR_HIGH_EC, BAR_HIGH_TX = '#ffebee', '#e57373', '#c62828'

# ──────────────────────────────────────────────────────────────
# 2. 캔버스 (세로형, 비율 ≈ 0.59)
# ──────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(10, 17), dpi=200)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 100)
ax.set_ylim(0, 170)
ax.axis('off')
ax.add_patch(plt.Rectangle((0, 0), 100, 170, facecolor=WHITE, edgecolor='none', zorder=0))

# ──────────────────────────────────────────────────────────────
# 3. 헬퍼 함수
# ──────────────────────────────────────────────────────────────
def box(x, y, w, h, fc=LIGHT_BG, ec=BORDER_CLR, lw=1.7, rs=1.4, z=1):
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle=f"round,pad=0,rounding_size={rs}",
                       fc=fc, ec=ec, lw=lw, zorder=z)
    ax.add_patch(p)
    return p

def card(x, y, w, h, fc=WHITE, ec=CARD_BORDER, lw=0.9, rs=0.8):
    ax.add_patch(FancyBboxPatch((x, y), w, h,
                 boxstyle=f"round,pad=0,rounding_size={rs}",
                 fc=fc, ec=ec, lw=lw, zorder=1))

def pill(cx, cy, w, h, txt, fc, tc, fs, weight='bold'):
    ax.add_patch(FancyBboxPatch((cx - w/2, cy - h/2), w, h,
                 boxstyle=f"round,pad=0,rounding_size={h/2}",
                 fc=fc, ec=fc, zorder=3))
    ax.text(cx, cy, txt, ha='center', va='center', color=tc,
            fontsize=fs, fontweight=weight, zorder=4)

def bell(cx, base, w, h, color, fa, label):
    xs = np.linspace(cx - w/2, cx + w/2, 160)
    ys = base + h * np.exp(-((xs - cx) / (w * 0.21))**2)
    ax.plot(xs, ys, color=color, lw=1.8, zorder=3)
    ax.fill_between(xs, base, ys, color=color, alpha=fa, zorder=2)
    ax.plot([cx, cx], [base, base + h], color=color, ls=(0, (3, 3)), lw=0.9, zorder=3)
    ax.text(cx + 1.3, base + h * 0.74, label, color=color, fontsize=9,
            style='italic', zorder=4)

def arrow(x0, y0, x1, y1, color, dashed=False, lw=1.7):
    ax.annotate('', xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='-|>', color=color, lw=lw,
                                linestyle='--' if dashed else '-',
                                shrinkA=0, shrinkB=0, mutation_scale=16),
                zorder=3)

def header(x, y, txt):
    ax.text(x, y, txt, fontsize=8.5, color=TX_SEC, fontweight='bold', zorder=4)

# ══════════════════════════════════════════════════════════════
# ① VOLATILITY FORECASTING  (상단 전폭)
# ══════════════════════════════════════════════════════════════
box(4, 150, 92, 17)
header(7, 163.6, "①  변동성 예측 모델 (Volatility Forecasting)")

pill(13.5, 159.6, 13, 3.4, "LSTM",   ACCENT_BLUE, WHITE, 9)
pill(26, 159.6, 10, 3.4, "HAR", ACCENT_BLUE, WHITE, 9)

ax.text(7, 155.0, r"$\hat{y}_t^{\mathrm{ens}} = w_k^{\mathrm{LSTM}}\hat{y}_t^{\mathrm{LSTM}} + w_k^{\mathrm{HAR}}\hat{y}_t^{\mathrm{HAR}}$",
        fontsize=9, color=DARK_BLUE, zorder=4)
ax.text(7, 152.0, r"$\hat{\boldsymbol{\sigma}}_t = \exp(\hat{y}_t^{\mathrm{ens}}) \times \sqrt{252}$",
        fontsize=9, color=TX_SEC, zorder=4)

# Low / High σ̂ 3분위 바 (기존 분위수 셀 스타일)
bar_x, bar_y, bar_w, bar_h = 47, 156.6, 46, 4.2
seg = bar_w / 3
ax.add_patch(plt.Rectangle((bar_x,         bar_y), seg, bar_h, facecolor=BAR_LOW_FC,  edgecolor=BAR_LOW_EC,  lw=0.9, zorder=3))
ax.add_patch(plt.Rectangle((bar_x + seg,   bar_y), seg, bar_h, facecolor=BAR_MID_FC,  edgecolor=BAR_MID_EC,  lw=0.9, zorder=3))
ax.add_patch(plt.Rectangle((bar_x + 2*seg, bar_y), seg, bar_h, facecolor=BAR_HIGH_FC, edgecolor=BAR_HIGH_EC, lw=0.9, zorder=3))
ax.text(bar_x + 0.5*seg, bar_y + bar_h/2, r"Low $\hat{\sigma}_t$",  ha='center', va='center', color=BAR_LOW_TX,  fontsize=8.5, fontweight='bold', zorder=5)
ax.text(bar_x + 1.5*seg, bar_y + bar_h/2, "· · ·",                ha='center', va='center', color=BAR_MID_TX,  fontsize=8.5, zorder=5)
ax.text(bar_x + 2.5*seg, bar_y + bar_h/2, r"High $\hat{\sigma}_t$", ha='center', va='center', color=BAR_HIGH_TX, fontsize=8.5, fontweight='bold', zorder=5)
ax.text(bar_x + 0.5*seg, bar_y - 1.8, "bottom 30%", ha='center', color=TX_MUTE, fontsize=7, zorder=5)
ax.text(bar_x + 2.5*seg, bar_y - 1.8, "top 30%",    ha='center', color=TX_MUTE, fontsize=7, zorder=5)

# ── ① → ② 듀얼 라벨 화살표 ─────────────────────────────────
ax.text(23, 146.6, r"$\hat{\boldsymbol{\sigma}}_t$ 미개입 — 독립 경로", ha='center', color=TX_MUTE, fontsize=7.5, zorder=4)
arrow(23, 145, 23, 139, TX_MUTE, dashed=True, lw=1.4)
# sigma-hat non-intervention block mark (X badge)
_xc, _yc = 23, 142
ax.add_patch(Circle((_xc, _yc), 0.85, facecolor=WHITE, edgecolor=BORDER_CLR, lw=0.8, zorder=5))
ax.plot([_xc-0.42, _xc+0.42], [_yc-0.42, _yc+0.42], color=BORDER_CLR, lw=1.5, zorder=6, solid_capstyle='round')
ax.plot([_xc-0.42, _xc+0.42], [_yc+0.42, _yc-0.42], color=BORDER_CLR, lw=1.5, zorder=6, solid_capstyle='round')
ax.text(71, 146.6, r"$\hat{\boldsymbol{\sigma}}_t$ 로 뷰 파라미터 구성", ha='center', color=TX_SEC, fontsize=7.5, zorder=4)
arrow(71, 145, 71, 139, BORDER_CLR, lw=1.6)

# ══════════════════════════════════════════════════════════════
# ② PRIOR 슬롯 (좌)  /  ② 투자자 전망 파라미터 (우)
# ══════════════════════════════════════════════════════════════
# ---- ② Prior 슬롯 박스 ----
box(4, 80, 38, 58)
header(7, 134.8, "②  PRIOR 슬롯 — 시장 비중")
ax.text(7, 131.0, r"$\mathbf{w}_{\mathrm{mkt}}$", fontsize=9.5, color=DARK_BLUE, fontweight='bold', zorder=4)
ax.text(7, 128.2, r"균형수익률 $\boldsymbol{\pi}=\lambda\boldsymbol{\Sigma}\mathbf{w}_{\mathrm{mkt}}$ 의 $\mathbf{w}$ 구성", fontsize=7.5, color=TX_SEC, zorder=4)
pill(23, 124.5, 11, 2.8, "3 options", DARK_BLUE, WHITE, 6.8)

w_cards = [
    (r"$\mathbf{w}^{\mathrm{mcap}}$", r"$\pm mcap_i \,/\, \sum_{j} mcap_j$", "시가총액 비중"),
    (r"$\mathbf{w}^{\mathrm{eq}}$",   r"$1/n$",                    "동일가중"),
    (r"$\mathbf{w}^{\mathrm{rp}}$",   r"$\pm 1/\sigma_{i,\mathrm{real}} \,/\, \sum_{j}(1/\sigma_{j,\mathrm{real}})$", "역변동성 가중"),
]
cy = 122.0
for title, formula, desc in w_cards:
    card(7, cy - 12, 32, 12, fc=CARD_BG, rs=1.0)
    ax.text(9.5, cy - 3.0, title,   fontsize=9.3, color=DARK_BLUE, zorder=4)
    ax.text(9.5, cy - 6.4, formula, fontsize=7.6, color=ACCENT_BLUE, zorder=4)
    ax.text(9.5, cy - 9.6, desc,    fontsize=7.0, color=TX_MUTE, zorder=4)
    cy -= 14.3

# ---- ② 투자자 전망 파라미터 박스 ----
box(46, 80, 50, 58)
header(49, 135.3, "②  투자자 전망 파라미터 (View Parameters)")
ax.text(49, 132.2, r"$\mathbf{p},\ q,\ \omega$  —  $\hat{\boldsymbol{\sigma}}_t$ 로부터 도출", fontsize=8.5, color=DARK_BLUE, fontweight='bold', zorder=4)

cP, cQ, cW = 55.0, 71.0, 87.5
ax.plot([63, 63], [81, 130], color=CARD_BORDER, lw=0.9, zorder=2)
ax.plot([79.5, 79.5], [81, 130], color=CARD_BORDER, lw=0.9, zorder=2)

def col_head(cx, kr, en, letter, opt):
    ax.text(cx, 129.0, kr, ha='center', color=DARK_BLUE, fontsize=6.3, fontweight='bold', zorder=4)
    ax.text(cx, 127.4, f"({en})", ha='center', color=TX_MUTE, fontsize=4.7, fontweight='bold', zorder=4)
    ax.text(cx, 122.5, letter, ha='center', color=DARK_BLUE, fontsize=12.5, zorder=4)
    pill(cx, 118.3, 11, 2.6, opt, DARK_BLUE, WHITE, 6.6)

col_head(cP, "뷰 포트폴리오", "VIEW PORTFOLIO", r"$\mathbf{p}$", "3 options")
col_head(cQ, "뷰 기대수익률", "EXPECTED RETURN", r"$q$", "5 options")
col_head(cW, "뷰 신뢰도", "UNCERTAINTY", r"$\omega$", "2 options")

def pcard(cx, cy, title, formula, h=6.2, fs=6.0):
    card(cx - 7.3, cy - h, 14.6, h, fc=WHITE, rs=0.8)
    ax.text(cx, cy - 2.5, title,   ha='center', fontsize=8.2, color=DARK_BLUE, zorder=4)
    ax.text(cx, cy - 5.1, formula, ha='center', fontsize=fs, color=ACCENT_BLUE, zorder=4)

# P 열
pcard(cP, 116, r"$p_i^{\mathrm{mcap}}$", r"$\pm mcap_i/\sum_{j} mcap_j$")
pcard(cP, 108.5, r"$p_i^{\mathrm{eq}}$",  r"$+1/|L|,\ -1/|H|$")
pcard(cP, 101, r"$p_i^{\mathrm{rp}}$",    r"$\pm(1/\hat{\sigma}_i)/\sum_{j}(1/\hat{\sigma}_j)$")

# q 열 (5종)
pcard(cQ, 116, r"$q^{\mathrm{lam}}$", r"$q_0\cdot \mathrm{clip}(\lambda_q/\bar{\lambda}_q)$")
pcard(cQ, 109, r"$q^{\mathrm{raw}}$", r"$\max(0,\,q_0\cdot\lambda_q^{\mathrm{raw}}/\bar{\lambda}_q)$")
pcard(cQ, 102, r"$q^{\mathrm{inv}}$", r"$q_0\cdot \mathrm{clip}(\bar{\lambda}_q/\lambda_q)$")
pcard(cQ, 95,  r"$q^{\mathrm{vsp}}$", r"$q_0\cdot \mathrm{clip}(\Delta\hat{\sigma}/\mathrm{median}(\Delta\hat{\sigma}_{\mathrm{train}}))$", fs=5.0)
pcard(cQ, 88,  r"$q^{\mathrm{ff3}}$", r"$\mathbf{p}\hat{\mathbf{r}}\ (\mathrm{FF3})$")

# ω 열 (2종)
pcard(cW, 116,   r"$\omega^{\mathrm{he}}$",  r"$\tau\cdot \mathbf{p}\boldsymbol{\Sigma}\mathbf{p}^{\top}$")
pcard(cW, 108.5, r"$\omega^{\mathrm{err}}$", r"$(q_{t-1}-\mathbf{p}\mathbf{r}_{t-1})^2$")

# ── ② → ③ 화살표 ─────────────────────────────────────────
arrow(23, 79, 23, 69, ACCENT_BLUE, lw=1.6)
arrow(71, 79, 71, 69, ACCENT_RED, lw=1.6)

# ══════════════════════════════════════════════════════════════
# ③ MARKET EQUILIBRIUM PRIOR (좌) / ③ INVESTOR VIEW (우)
# ══════════════════════════════════════════════════════════════
box(4, 39, 41, 29)
ax.text(7, 64.3, "③  시장 균형 사전 분포 (Prior)", fontsize=9.5, color=DARK_BLUE, fontweight='bold', zorder=4)
bell(24, 47.5, 30, 8.0, ACCENT_BLUE, 0.12, r"$\boldsymbol{\pi}$")
ax.text(24, 60.0, r"$\boldsymbol{\pi}=\lambda\boldsymbol{\Sigma}\mathbf{w}_{\mathrm{mkt}}\ \ (\lambda = 2.5)$", ha='center', fontsize=8, color=DARK_BLUE, zorder=5)
ax.text(24, 43.5, r"$\boldsymbol{\mu}_{\mathrm{prior}}\sim\mathcal{N}(\boldsymbol{\pi},\tau\boldsymbol{\Sigma})$", ha='center', fontsize=7.6, color=TX_SEC, zorder=5)

box(51, 39, 45, 29)
ax.text(54, 64.3, "③  투자자 전망 분포 (Investor View)", fontsize=9.5, color=DARK_BLUE, fontweight='bold', zorder=4)
ax.text(54, 60.6, "저변동 → 초과성과 뷰", fontsize=7.5, color=ACCENT_RED, zorder=4)
bell(73, 47.5, 32, 8.0, ACCENT_RED, 0.10, r"$q$")
ax.text(73, 44.5, r"$q \mid \boldsymbol{\mu} \sim \mathcal{N}(\mathbf{p}^{\top}\boldsymbol{\mu},\ \omega)$", ha='center', fontsize=7.8, color=DARK_BLUE, zorder=5)
ax.text(73, 41.0, r"$q \sim \mathcal{N}(\mathbf{p}\boldsymbol{\pi},\ \omega + \mathbf{p}(\tau\boldsymbol{\Sigma})\mathbf{p}^{\top})$", ha='center', fontsize=7.3, color=DARK_BLUE, zorder=5)

ax.text(48, 53, "+", ha='center', va='center', fontsize=24, color=TX_SEC, fontweight='bold', zorder=5)

# ── ③ → ④ Bayesian update 브래킷 병합 ─────────────────────
ax.plot([24, 24], [39, 36], color=ACCENT_BLUE, lw=1.4, zorder=3)
ax.plot([73, 73], [39, 36], color=TX_SEC, lw=1.4, zorder=3)
ax.plot([24, 73], [36, 36], color=TX_SEC, lw=1.4, zorder=3)
ax.text(48, 37.1, "Bayesian update", ha='center', color=ACCENT_BLUE, fontsize=8, fontweight='bold', zorder=4)
arrow(48, 36, 48, 34.3, TX_SEC, lw=2.0)

# ══════════════════════════════════════════════════════════════
# ④ POSTERIOR  (라이트 박스 — 기존 디자인에 맞춤)
# ══════════════════════════════════════════════════════════════
box(4, 3, 92, 31)
ax.text(7, 30.3, "④  사후 결합 분포 및 포트폴리오 최적화",
        fontsize=11, color=DARK_BLUE, fontweight='bold', zorder=4)

ax.plot([37, 37], [6, 26], color=CARD_BORDER, lw=0.9, zorder=3)
ax.plot([66, 66], [6, 26], color=CARD_BORDER, lw=0.9, zorder=3)

# (1) BAYESIAN OVERLAY
ax.text(8, 26.0, "사후 결합", color=TX_MUTE, fontsize=6.5, fontweight='bold', zorder=4)
xo = np.linspace(8, 34, 200)
def g(mu, s, h): return 10 + h * np.exp(-((xo - mu)/s)**2)
ax.plot(xo, g(18, 5.0, 7), color=ACCENT_BLUE, lw=1.2, ls=(0, (4, 3)), zorder=4)   # Prior
ax.plot(xo, g(25, 5.5, 6), color=ACCENT_RED,  lw=1.2, ls=(0, (4, 3)), zorder=4)   # View
yp = g(21, 3.4, 10)
ax.plot(xo, yp, color=ACCENT_GREEN, lw=2.0, zorder=5)                              # Posterior
ax.fill_between(xo, 10, yp, color=ACCENT_GREEN, alpha=0.12, zorder=4)
ax.text(21, 21.4, r"$\boldsymbol{\mu}_{\mathrm{BL}}$", ha='center', color=ACCENT_GREEN, fontsize=7, zorder=6)
ax.plot([8, 11], [7.2, 7.2], color=ACCENT_BLUE, lw=1.2, ls=(0, (3, 2)), zorder=5)
ax.text(11.6, 7.2, "Prior", va='center', color=TX_SEC, fontsize=5.6, zorder=5)
ax.plot([19, 22], [7.2, 7.2], color=ACCENT_RED, lw=1.2, ls=(0, (3, 2)), zorder=5)
ax.text(22.6, 7.2, "View", va='center', color=TX_SEC, fontsize=5.6, zorder=5)
ax.plot([29, 32], [7.2, 7.2], color=ACCENT_GREEN, lw=1.8, zorder=5)
ax.text(32.6, 7.2, "Posterior", va='center', color=TX_SEC, fontsize=5.6, zorder=5)
ax.text(21, 4.4, r"$\boldsymbol{\mu}_{\mathrm{post}}\,|\,q \sim \mathcal{N}(\boldsymbol{\mu}_{\mathrm{BL}},\boldsymbol{\Sigma}_{\mathrm{BL}})$",
        ha='center', color=TX_SEC, fontsize=7, zorder=5)

# (2) BL UPDATE
ax.text(39, 26.0, "블랙-리터만 사후 기대수익률 도출", color=TX_MUTE, fontsize=6.5, fontweight='bold', zorder=4)
ax.text(39, 20.0, r"$\boldsymbol{\Sigma}_{\mathrm{BL}} = [(\tau\boldsymbol{\Sigma})^{-1} + \mathbf{p}^{\top}\omega^{-1}\mathbf{p}]^{-1}$",
        color=DARK_BLUE, fontsize=7.6, zorder=4)
ax.text(39, 14.0, r"$\boldsymbol{\mu}_{\mathrm{BL}} = \boldsymbol{\Sigma}_{\mathrm{BL}}[(\tau\boldsymbol{\Sigma})^{-1}\boldsymbol{\pi} + \mathbf{p}^{\top}\omega^{-1}q]$",
        color=DARK_BLUE, fontsize=7.6, zorder=4)

# (3) OPTIMAL WEIGHTS
ax.text(68, 26.0, "평균-분산 최적화 (MVO)", color=TX_MUTE, fontsize=6.5, fontweight='bold', zorder=4)
ax.text(68, 19.6, r"$\mathbf{w}^* = \min_{\mathbf{w}}\ \frac{1}{2}\lambda\, \mathbf{w}^{\top}\boldsymbol{\Sigma}_{\mathrm{BL}}\mathbf{w} - \mathbf{w}^{\top}\boldsymbol{\mu}_{\mathrm{BL}}$", color=DARK_BLUE, fontsize=7.2, zorder=4)
ax.text(68, 14.2, r"$s.t.\ \sum w_i=1,\ 0\leq w_i\leq 0.1$", color=TX_SEC, fontsize=6.6, zorder=4)
card(68, 5.5, 25, 6.6, fc=CARD_BG, rs=0.8)
ax.text(70, 8.7, r"$\mathbf{w}^*$  —  저변동 포트폴리오 최적 가중치", color=DARK_BLUE, fontsize=7.0, fontweight='bold', zorder=5)

# ──────────────────────────────────────────────────────────────
# 저장
# ──────────────────────────────────────────────────────────────
out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
out_path = os.path.join(out_dir, "bl_framework_v3_0.png")
plt.savefig(out_path, dpi=200, bbox_inches='tight', facecolor=WHITE)
plt.close()
print("saved:", out_path)
