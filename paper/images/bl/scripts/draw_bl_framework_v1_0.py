import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 맑은 고딕 한글 폰트 설정 (Windows 기본)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 해상도 설정 (300 DPI, 학술지 조판 규격)
fig = plt.figure(figsize=(12, 13.0), dpi=300)

# 메인 투명 축 레이아웃 설정 (텍스트, 박스, 연결선용)
ax_main = fig.add_axes([0, 0, 1, 1])
ax_main.set_xlim(0, 10)
ax_main.set_ylim(0, 10)
ax_main.axis('off')

# 공통 색상 및 스타일 정의
DARK_BLUE = '#1a2a3a'
LIGHT_BG = '#fcfdfe'
BORDER_COLOR = '#2c3e50'
CARD_BG = '#f8f9fa'
CARD_BORDER = '#cfd8dc'
ACCENT_BLUE = '#0d47a1'
ACCENT_RED = '#b71c1c'
ACCENT_GREEN = '#1b5e20'

# ==============================================================================
# [함수] 벨커브 단독 드로잉 헬퍼 (Prior, View 용)
# ==============================================================================
def draw_bell_curve(rect, center, std, color, line_label, center_label):
    ax = fig.add_axes(rect)
    x = np.linspace(-3.5, 3.5, 300)
    y = np.exp(-x**2 / 2) / np.sqrt(2 * np.pi)
    
    # 그리기
    ax.plot(x, y, color=color, lw=2, label=line_label)
    ax.fill_between(x, y, color=color, alpha=0.08)
    
    # 평균 중심선 및 라벨
    ax.axvline(0, color=color, ls='--', lw=1.2)
    ax.text(0, -0.05, center_label, ha='center', va='top', color=color, fontsize=10, weight='bold')
    
    ax.set_xlim(-3.5, 3.5)
    ax.set_ylim(-0.08, 0.46)
    ax.axis('off')

# ==============================================================================
# [함수] Box 5 전용 3색 융합 벨커브 드로잉 (Prior + View -> Posterior)
# ==============================================================================
def draw_fusion_bell_curve(rect):
    ax = fig.add_axes(rect)
    x = np.linspace(-4, 4, 400)
    
    # 1) Prior (파란색 점선, 중간 넓이)
    y_prior = np.exp(-(x + 0.8)**2 / (2 * 1.1**2)) / (1.1 * np.sqrt(2 * np.pi))
    ax.plot(x, y_prior, color=ACCENT_BLUE, ls='--', lw=1.5, alpha=0.6, label='Prior')
    
    # 2) View (빨간색 점선, 넓은 분산)
    y_view = np.exp(-(x - 1.2)**2 / (2 * 1.4**2)) / (1.4 * np.sqrt(2 * np.pi))
    ax.plot(x, y_view, color=ACCENT_RED, ls='--', lw=1.5, alpha=0.6, label='View')
    
    # 3) Posterior (녹색 실선, 융합되어 분산이 매우 좁고 높이가 높음)
    y_post = np.exp(-(x - 0.1)**2 / (2 * 0.75**2)) / (0.75 * np.sqrt(2 * np.pi))
    ax.plot(x, y_post, color=ACCENT_GREEN, ls='-', lw=2.2, label='Posterior')
    ax.fill_between(x, y_post, color=ACCENT_GREEN, alpha=0.1)
    
    # 중심 결합 화살표 시각화 (베이지안 수렴 표시)
    ax.axvline(-0.8, color=ACCENT_BLUE, ls=':', lw=1, alpha=0.5)
    ax.axvline(1.2, color=ACCENT_RED, ls=':', lw=1, alpha=0.5)
    ax.axvline(0.1, color=ACCENT_GREEN, ls='-', lw=1.2)
    
    # 결합 평균 라벨들 (pi, mu의 볼드화 적용)
    ax.text(-0.8, -0.06, r"$\boldsymbol{\pi}$", ha='center', va='top', color=ACCENT_BLUE, fontsize=9.5)
    ax.text(1.2, -0.06, r"$q$", ha='center', va='top', color=ACCENT_RED, fontsize=9.5)
    ax.text(0.1, -0.06, r"$\boldsymbol{\mu}_{\mathrm{BL}}$", ha='center', va='top', color=ACCENT_GREEN, fontsize=10, weight='bold')
    
    ax.set_xlim(-4, 4)
    ax.set_ylim(-0.09, 0.58)
    ax.axis('off')
    
    # 범례 표시
    ax.legend(loc='upper right', frameon=False, fontsize=7.5, handlelength=1.5)

# ==============================================================================
# 1. [Box 1] Volatility prediction [P] / 변동성 예측 및 전망 비중 (좌측 상단, 너비=4.0로 벌림)
# ==============================================================================
# 메인 박스 (x: 0.5 ~ 4.5)
box1 = patches.FancyBboxPatch((0.5, 6.3), 4.0, 2.9, boxstyle="round,pad=0.08", fc=LIGHT_BG, ec=BORDER_COLOR, lw=1.8)
ax_main.add_patch(box1)
ax_main.text(0.7, 9.0, "변동성 예측 및 전망 비중 [p]", fontsize=12, weight='bold', color=DARK_BLUE)

# 2개 모델 버튼 렌더링 ((본 연구) 및 -RV 제거)
models = [
    {"name": "LSTM", "x": 0.7, "w": 1.3},
    {"name": "HAR", "x": 2.4, "w": 1.3}
]

for m in models:
    btn = patches.FancyBboxPatch((m["x"], 8.35), m["w"], 0.32, boxstyle="round,pad=0.04", fc=ACCENT_BLUE, ec=ACCENT_BLUE, lw=1)
    ax_main.add_patch(btn)
    ax_main.text(m["x"] + m["w"]/2.0, 8.51, m["name"], ha='center', va='center', color='white', fontsize=10, weight='bold')

# 모델 결합 화살표 및 앙상블 수식
ax_main.annotate('', xy=(2.2, 7.85), xytext=(2.2, 8.25),
                 arrowprops=dict(facecolor=BORDER_COLOR, edgecolor=BORDER_COLOR, width=1, headwidth=5, headlength=5))
ax_main.text(2.3, 8.0, "성능 가중 앙상블 결합", fontsize=8.5, color='#546e7a', weight='bold')

# 앙상블 및 지수변환 수식 (sigma 볼드화 및 시간 인덱싱 정정 적용)
ax_main.text(0.7, 7.6, r"$\hat{y}^{\mathrm{ens}}[t] = w_k^{\mathrm{LSTM}} \hat{y}^{\mathrm{LSTM}}[t] + w_k^{\mathrm{HAR}} \hat{y}^{\mathrm{HAR}}[t]$", fontsize=10.5, color=DARK_BLUE)
ax_main.text(0.7, 7.25, r"$\hat{\boldsymbol{\sigma}}[t] = \exp(\hat{y}^{\mathrm{ens}}[t]) \times \sqrt{252}$ (연환산 실현변동성 뷰)", fontsize=9.5, color='#37474f')

# 3색 분위수 정렬 바 (x: 0.7 ~ 3.8)
bar_y = 6.8
ax_main.add_patch(patches.Rectangle((0.7, bar_y), 0.9, 0.25, facecolor='#dbe9f6', edgecolor='#4a90e2', lw=1))
ax_main.add_patch(patches.Rectangle((1.6, bar_y), 1.3, 0.25, facecolor='#eceff1', edgecolor='#90a4ae', lw=1))
ax_main.add_patch(patches.Rectangle((2.9, bar_y), 0.9, 0.25, facecolor='#ffebee', edgecolor='#e57373', lw=1))

ax_main.text(1.15, bar_y + 0.125, "저변동 L (30%)", ha='center', va='center', fontsize=7.5, weight='bold', color='#0d47a1')
ax_main.text(2.25, bar_y + 0.125, "중간 비중 (0%)", ha='center', va='center', fontsize=7.5, weight='bold', color='#37474f')
ax_main.text(3.35, bar_y + 0.125, "고변동 H (30%)", ha='center', va='center', fontsize=7.5, weight='bold', color='#c62828')

# 정렬 텍스트
ax_main.text(2.25, 7.08, "▼ 예측 변동성 기준 오름차순 정렬", ha='center', va='bottom', fontsize=8, color='#37474f', weight='bold')

# 전망 비중 수식 (중앙 x=2.5 정렬, 단일 공식 통일)
ax_main.text(2.5, 6.45, r"$p_i^{\mathrm{mcap}} = \pm \frac{m_i}{\sum_{\mathcal{G}} m_j} \quad p_i^{\mathrm{eq}} = \pm \frac{1}{n_g} \quad p_i^{\mathrm{rp}} = \pm \frac{\hat{\sigma}_i^{\gamma_i}}{\sum_{\mathcal{G}} \hat{\sigma}_j^{\gamma_i}} \ (\gamma_i = \mp 1)$", ha='center', fontsize=7.5, color=DARK_BLUE, weight='bold')

# ==============================================================================
# 2. [Box 2] Expected return prediction [q] / 기대수익률 전망 (우측 상단, x시작=5.5, 너비=4.0로 벌림)
# ==============================================================================
box2 = patches.FancyBboxPatch((5.5, 6.3), 4.0, 2.9, boxstyle="round,pad=0.08", fc=LIGHT_BG, ec=BORDER_COLOR, lw=1.8)
ax_main.add_patch(box2)
ax_main.text(5.7, 9.0, "기대수익률 전망 [q]", fontsize=12, weight='bold', color=DARK_BLUE)

# 5종 q 슬롯 - 3.6 가로폭으로 세로 5단 그리드 대형 카드 배치 (Fama-French 비교 앵커 카드 완전 삭제)
q_slots = [
    {"label": r"$q^{\mathrm{raw\_lam}} = \max(0, q_0 \lambda_t^{\mathrm{raw}}/\bar{\lambda})$", "y": 8.45},
    {"label": r"$q^{\mathrm{lambda}} = q_0 \cdot \mathrm{clip}(\lambda_t/\bar{\lambda}, 0.1, 3.0)$", "y": 7.95},
    {"label": r"$q^{\mathrm{inv\_lambda}} = q_0 \cdot \mathrm{clip}(\bar{\lambda}/\lambda_t, 0.1, 3.0)$", "y": 7.45},
    {"label": r"$q^{\mathrm{vol\_spread}} = q_0 \cdot \mathrm{clip}(\Delta\hat{\sigma}_t/\overline{\Delta\hat{\sigma}}, 0.1, 3.0)$", "y": 6.95},
    {"label": r"$q^{\mathrm{ff3}} = \mathbf{p}^\top \hat{\mathbf{r}}$  (Fama-French 3요소 기대치)", "y": 6.45}
]

for qs in q_slots:
    c_patch = patches.FancyBboxPatch((5.7, qs["y"]), 3.6, 0.34, boxstyle="round,pad=0.01", fc='#eceff1', ec='#cfd8dc', lw=0.8)
    ax_main.add_patch(c_patch)
    ax_main.text(7.5, qs["y"] + 0.17, qs["label"], ha='center', va='center', fontsize=9.2, color=DARK_BLUE, weight='bold')

# ==============================================================================
# 3. [Box 3] Market equilibrium portfolio / 시장 균형 Prior (중간 좌측, 너비=4.0로 벌림)
# ==============================================================================
box3 = patches.FancyBboxPatch((0.5, 3.4), 4.0, 2.6, boxstyle="round,pad=0.08", fc=LIGHT_BG, ec=BORDER_COLOR, lw=1.8)
ax_main.add_patch(box3)
ax_main.text(0.7, 5.75, "시장 균형 사전 분포 [Prior]", fontsize=12, weight='bold', color=DARK_BLUE)

# 사전 수익률 계산 공식 기입 (pi, Sigma 볼드화)
ax_main.text(0.7, 5.4, r"• 균형수익률: $\boldsymbol{\pi} = \lambda \boldsymbol{\Sigma} \mathbf{w}_{\mathrm{mkt}}$ (역최적화)", fontsize=10.5, color=DARK_BLUE)
ax_main.text(0.7, 5.15, r"• Ledoit-Wolf 수축 공분산 행렬 $\boldsymbol{\Sigma}$ 사용", fontsize=9.5, color='#37474f')

# Prior 벨커브 임베딩 (Subplot x비율: 0.08 ~ 0.38)
draw_bell_curve([0.08, 0.39, 0.30, 0.10], 0, 1, ACCENT_BLUE, 'Prior', r"$\boldsymbol{\pi}$")
# 수식 y좌표 및 가로 중심(x=2.5) 정렬 (mu, pi, Sigma 볼드화)
ax_main.text(2.5, 3.48, r"$\boldsymbol{\mu}_{\mathrm{prior}} \sim \mathcal{N}(\boldsymbol{\pi}, \tau \boldsymbol{\Sigma})$", ha='center', fontsize=11, color=ACCENT_BLUE, weight='bold')

# ==============================================================================
# 4. [Box 4] View portfolio / 투자자 전망 View (중간 우측, x시작=5.5, 너비=4.0로 벌림)
# ==============================================================================
box4 = patches.FancyBboxPatch((5.5, 3.4), 4.0, 2.6, boxstyle="round,pad=0.08", fc=LIGHT_BG, ec=BORDER_COLOR, lw=1.8)
ax_main.add_patch(box4)
ax_main.text(5.7, 5.75, "투자자 전망 분포 [View]", fontsize=12, weight='bold', color=DARK_BLUE)

# 전망 핵심 가설 강조
ax_main.text(5.7, 5.4, "투자자 뷰 (View): 저변동성 자산군이 고변동성 자산군 대비", fontsize=9.5, color=ACCENT_RED, weight='bold')
ax_main.text(5.7, 5.15, "                   초과수익을 달성할 것으로 전망", fontsize=9.5, color=ACCENT_RED, weight='bold')

# View 벨커브 임베딩 (Subplot x비율: 0.60 ~ 0.90)
draw_bell_curve([0.60, 0.39, 0.30, 0.10], 0.8, 1.2, ACCENT_RED, 'View', r"$q$")
# 수식 y좌표 및 가로 중심(x=7.5) 정렬 (p, pi, Sigma 볼드화 및 조건부 통일)
ax_main.text(7.5, 3.48, r"$q \sim \mathcal{N}(\mathbf{p}^\top \boldsymbol{\mu}_{\mathrm{prior}}, \omega)$", ha='center', fontsize=11, color=ACCENT_RED, weight='bold')

# ==============================================================================
# 5. [Box 5] 사후 결합 분포 및 최적 가중치 (최하단 대형 박스 - 3구획 카드 구조화)
# ==============================================================================
box5 = patches.FancyBboxPatch((0.5, 0.4), 9.0, 2.6, boxstyle="round,pad=0.08", fc=LIGHT_BG, ec=BORDER_COLOR, lw=1.8)
ax_main.add_patch(box5)
ax_main.text(0.7, 2.7, "사후 결합 분포 및 포트폴리오 최적화", fontsize=13, weight='bold', color=DARK_BLUE)

# [구획 1] 좌측 카드: Prior + View -> Posterior 3색 융합 벨커브 그래프 (mu, Sigma 볼드화)
card1 = patches.FancyBboxPatch((0.7, 0.55), 3.4, 2.0, boxstyle="round,pad=0.02", fc=CARD_BG, ec=CARD_BORDER, lw=1)
ax_main.add_patch(card1)
ax_main.text(2.4, 2.35, "정보 융합 (Bayesian Overlay)", ha='center', fontsize=9.5, weight='bold', color=ACCENT_GREEN)
draw_fusion_bell_curve([0.08, 0.08, 0.30, 0.12])
ax_main.text(2.4, 0.58, r"$\boldsymbol{\mu}_{\mathrm{post}} \mid q \sim \mathcal{N}(\boldsymbol{\mu}_{\mathrm{BL}}, \boldsymbol{\Sigma}_{\mathrm{BL}})$", ha='center', fontsize=11, color=ACCENT_GREEN, weight='bold')

# [구획 2] 중앙 카드: 사후 결합 파라미터 수식 (기대수익률 도출로 정정)
card2 = patches.FancyBboxPatch((4.3, 0.55), 2.5, 2.0, boxstyle="round,pad=0.02", fc=CARD_BG, ec=CARD_BORDER, lw=1)
ax_main.add_patch(card2)
ax_main.text(5.55, 2.35, "블랙-리터만 사후 기대수익률 도출", ha='center', fontsize=9.5, weight='bold', color=DARK_BLUE)

# BL 사후공분산 수식 (볼드화, 정밀 역행렬 괄호 및 academic top 트랜스포즈 적용)
ax_main.text(4.4, 1.65, r"$\boldsymbol{\Sigma}_{BL} = [(\tau\boldsymbol{\Sigma})^{-1} + \mathbf{p}^\top \omega^{-1}\mathbf{p}]^{-1}$", fontsize=10.5, color=DARK_BLUE)
# BL 사후평균 수식 (볼드화, 정밀 역행렬 괄호 및 academic top 트랜스포즈 적용)
ax_main.text(4.4, 1.05, r"$\boldsymbol{\mu}_{BL} = [(\tau\boldsymbol{\Sigma})^{-1} + \mathbf{p}^\top \omega^{-1}\mathbf{p}]^{-1}[(\tau\boldsymbol{\Sigma})^{-1}\boldsymbol{\pi} + \mathbf{p}^\top \omega^{-1}q]$", fontsize=9.2, color=DARK_BLUE)

# [구획 3] 우측 카드: SLSQP MVO 최적 가중치 계산 (사후 모수 볼드화)
card3 = patches.FancyBboxPatch((7.0, 0.55), 2.3, 2.0, boxstyle="round,pad=0.02", fc=CARD_BG, ec=CARD_BORDER, lw=1)
ax_main.add_patch(card3)
ax_main.text(8.15, 2.35, "평균-분산 최적화 (MVO)", ha='center', fontsize=9.5, weight='bold', color=DARK_BLUE)

# MVO 식 통합 기입 (Sigma_BL, mu_BL 볼드화)
ax_main.text(7.1, 1.5, r"$\mathbf{w}^* = \arg\min_{\mathbf{w}} \left( \frac{\lambda}{2}\mathbf{w}^\top \boldsymbol{\Sigma}_{\mathrm{BL}}\mathbf{w} - \mathbf{w}^\top \boldsymbol{\mu}_{\mathrm{BL}} \right)$", fontsize=9.2, color=DARK_BLUE)
# 제약조건
ax_main.text(7.1, 1.05, "제약조건 (Constraints):", fontsize=8.5, weight='bold', color='#37474f')
ax_main.text(7.2, 0.75, r"$\sum_{i=1}^n w_i = 1, \quad 0 \leq w_i \leq 0.1$", fontsize=10.5, color=ACCENT_RED, weight='bold')

# ==============================================================================
# 6. 화살표 및 흐름 연결선 배치 (Arrows & Connectors - 6차 기하학적 수평 대칭/간격 튜닝 완료)
# ==============================================================================
# 1) Box 1 -> Box 2 수평 우향 (변동성 뷰 정보 연계) - 가로 범위 확장(4.6 -> 5.4), 텍스트 대칭 정중앙(5.0) 배치!
ax_main.annotate('', xy=(5.4, 7.8), xytext=(4.6, 7.8),
                 arrowprops=dict(facecolor=BORDER_COLOR, edgecolor=BORDER_COLOR, width=1.5, headwidth=7, headlength=7))
ax_main.text(5.0, 8.02, r"$\hat{\boldsymbol{\sigma}}[t]$", ha='center', fontsize=9.5, color=BORDER_COLOR, weight='bold')

# 2) Box 1 -> Box 4 대각선 우하향 점선 (전망 비중 p 주입선) - y좌표를 5.82로 살짝 상향하여 대각선과 안 겹치게 분리!
ax_main.annotate('', xy=(5.45, 4.7), xytext=(4.45, 6.4),
                 arrowprops=dict(facecolor=BORDER_COLOR, edgecolor=BORDER_COLOR, width=1.0, headwidth=6, headlength=6, ls='dashed'))
ax_main.text(4.95, 5.82, r"$\mathbf{p}$", fontsize=12, color=BORDER_COLOR, weight='bold', rotation=-21, ha='center')

# 3) Box 2 -> Box 4 수직 하향 (전망 q 주입선) - 대칭축 7.5로 이동, 텍스트 x를 7.75로 밀어 겹침 차단!
ax_main.annotate('', xy=(7.5, 6.0), xytext=(7.5, 6.3),
                 arrowprops=dict(facecolor=BORDER_COLOR, edgecolor=BORDER_COLOR, width=1.5, headwidth=7, headlength=7))
ax_main.text(7.75, 6.12, r"$q$ 전달", fontsize=9.5, color=BORDER_COLOR, weight='bold')

# 4) Box 3과 Box 4 사이의 대형 플러스 기호 (+) - 대칭 정중앙(x=5.0)으로 정확히 정렬!
ax_main.text(5.0, 4.7, "+", fontsize=28, weight='bold', ha='center', va='center', color=BORDER_COLOR)

# 5) Prior 및 View -> 사후결합 대형 결합 화살표 - 대칭 정중앙(x=5.0)으로 정확히 정렬!
# 텍스트 라벨을 완전히 소거하여 순수 결합 화살표만 깨끗하게 표시.
ax_main.annotate('', xy=(5.0, 3.0), xytext=(5.0, 3.4),
                 arrowprops=dict(facecolor=BORDER_COLOR, edgecolor=BORDER_COLOR, width=3.2, headwidth=10, headlength=10))

# ==============================================================================
# 7. 메인 타이틀
# ==============================================================================
ax_main.text(5.0, 9.45, "통합 Black-Litterman 포트폴리오 자산 배분 프레임워크", fontsize=18, weight='bold', ha='center', color=DARK_BLUE)

# 이미지 출력 및 보존 (Workspace images/bl 폴더에 v1_0으로 저장!)
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
output_path = os.path.join(output_dir, "bl_framework_v1_0.png")

plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()

print(f"Publication-ready V1.0 diagram successfully generated at: {output_path}")
