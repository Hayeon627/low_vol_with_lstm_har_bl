import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# 맑은 고딕 한글 폰트 설정 (Windows 기본)
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 해상도 설정 (300 DPI, 학술지 조판 규격)
fig = plt.figure(figsize=(12.0, 13.5), dpi=300)

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
    
    # 결합 평균 라벨들
    ax.text(-0.8, -0.06, r"$\boldsymbol{\pi}$", ha='center', va='top', color=ACCENT_BLUE, fontsize=9.5)
    ax.text(1.2, -0.06, r"$q$", ha='center', va='top', color=ACCENT_RED, fontsize=9.5)
    ax.text(0.1, -0.06, r"$\boldsymbol{\mu}_{\mathrm{BL}}$", ha='center', va='top', color=ACCENT_GREEN, fontsize=10, weight='bold')
    
    ax.set_xlim(-4, 4)
    ax.set_ylim(-0.09, 0.58)
    ax.axis('off')
    
    # 범례 표시
    ax.legend(loc='upper right', frameon=False, fontsize=7.5, handlelength=1.5)

# ==============================================================================
# 1. [Box 1] Volatility Forecasting Model / 변동성 예측 모델 (좌측 상단, 가로폭 추가 축소)
# ==============================================================================
box1 = patches.FancyBboxPatch((0.5, 7.2), 3.0, 1.9, boxstyle="round,pad=0.08", fc=LIGHT_BG, ec=BORDER_COLOR, lw=1.8)
ax_main.add_patch(box1)
ax_main.text(0.7, 8.8, "변동성 예측 모델 [Volatility Forecasting]", fontsize=11.5, weight='bold', color=DARK_BLUE)

# 2개 모델 버튼 리사이징 및 가로 정렬 튜닝
models = [
    {"name": "LSTM", "x": 0.7, "w": 1.0},
    {"name": "HAR", "x": 1.9, "w": 1.0}
]

for m in models:
    btn = patches.FancyBboxPatch((m["x"], 8.2), m["w"], 0.28, boxstyle="round,pad=0.04", fc=ACCENT_BLUE, ec=ACCENT_BLUE, lw=1)
    ax_main.add_patch(btn)
    ax_main.text(m["x"] + m["w"]/2.0, 8.34, m["name"], ha='center', va='center', color='white', fontsize=10, weight='bold')

# 앙상블 결합 수식
ax_main.text(0.7, 7.82, r"$\hat{y}^{\mathrm{ens}}[t] = w_k^{\mathrm{LSTM}} \hat{y}^{\mathrm{LSTM}}[t] + w_k^{\mathrm{HAR}} \hat{y}^{\mathrm{HAR}}[t]$", fontsize=9.2, color=DARK_BLUE)
ax_main.text(0.7, 7.42, r"$\hat{\boldsymbol{\sigma}}[t] = \exp(\hat{y}^{\mathrm{ens}}[t]) \times \sqrt{252}$", fontsize=9.2, color='#37474f')

# ==============================================================================
# 2. [우측 통합 Box] 투자자 전망 파라미터 [View Parameters] (가로 여백 확대 및 3열 병렬 대전환)
# ==============================================================================
# 통합 파라미터 박스 (x: 4.3, y: 6.2, 너비=5.2, 높이=3.0)
box2_parameters = patches.FancyBboxPatch((4.3, 6.2), 5.2, 3.0, boxstyle="round,pad=0.08", fc=LIGHT_BG, ec=BORDER_COLOR, lw=1.8)
ax_main.add_patch(box2_parameters)
ax_main.text(6.9, 9.0, r"투자자 전망 파라미터 [$p, q, \omega$]", ha='center', fontsize=12, weight='bold', color=DARK_BLUE)

# [수직 분할 구분선 2개 조율]
ax_main.plot([6.0, 6.0], [6.3, 8.8], color='#cfd8dc', lw=0.8, ls='-')
ax_main.plot([7.8, 7.8], [6.3, 8.8], color='#cfd8dc', lw=0.8, ls='-')

# ------------------------------------------------------------------------------
# [1열: 전망 비중 p] (x: 4.3 ~ 6.0, 중심 x = 5.15, 3색 분위수 미니바 임베딩 완료)
# ------------------------------------------------------------------------------
ax_main.text(5.15, 8.7, "1. 전망 비중 [p]", ha='center', fontsize=9.2, weight='bold', color=DARK_BLUE)
ax_main.text(5.15, 8.45, "변동성 3분위 자산 배분", ha='center', fontsize=8.0, color='#37474f', weight='bold')

# [미니 3색 분위수 정렬 바 임베딩] (Y축: 8.0 ~ 8.2, 총 너비 1.5, x: 4.4 ~ 5.9)
ax_main.add_patch(patches.Rectangle((4.4, 8.0), 0.45, 0.20, facecolor='#dbe9f6', edgecolor='#4a90e2', lw=0.8))
ax_main.add_patch(patches.Rectangle((4.85, 8.0), 0.60, 0.20, facecolor='#eceff1', edgecolor='#90a4ae', lw=0.8))
ax_main.add_patch(patches.Rectangle((5.45, 8.0), 0.45, 0.20, facecolor='#ffebee', edgecolor='#e57373', lw=0.8))

# 분위수 바 내부 텍스트 라벨 (2행 분리, fontsize=5.8)
ax_main.text(4.625, 8.1, "저변동 L\n(30%)", ha='center', va='center', fontsize=5.8, color='#0d47a1', weight='bold')
ax_main.text(5.15, 8.1, "중간 비중\n(0%)", ha='center', va='center', fontsize=5.8, color='#37474f', weight='bold')
ax_main.text(5.675, 8.1, "고변동 H\n(30%)", ha='center', va='center', fontsize=5.8, color='#c62828', weight='bold')

# Y좌표 리밸런싱 수식들
ax_main.text(5.15, 7.55, r"$p_i^{\mathrm{mcap}} = \pm \frac{m_i}{\sum_{\mathcal{G}} m_j}$", ha='center', fontsize=8.2, color=DARK_BLUE, weight='bold')
ax_main.text(5.15, 7.15, r"$p_i^{\mathrm{eq}} = \pm \frac{1}{n_g}$", ha='center', fontsize=8.2, color=DARK_BLUE, weight='bold')

# rp 리스크 패리티 단일 수식 통일 (지수 감마 도입)
ax_main.text(5.15, 6.75, r"$p_i^{\mathrm{rp}} = \pm \frac{\hat{\sigma}_i^{\gamma_i}}{\sum_{\mathcal{G}} \hat{\sigma}_j^{\gamma_i}}$", ha='center', fontsize=8.2, color=DARK_BLUE, weight='bold')
ax_main.text(5.15, 6.38, r"$(\gamma_i = \mp 1)$", ha='center', fontsize=8.0, color='#37474f', weight='bold')

# ------------------------------------------------------------------------------
# [2열: 기대수익률 q] (x: 6.0 ~ 7.8, 중심 x = 6.9, q=p^Tr 공식 소거 완료)
# ------------------------------------------------------------------------------
ax_main.text(6.9, 8.7, "2. 기대수익률 [q]", ha='center', fontsize=9.2, weight='bold', color=DARK_BLUE)
ax_main.text(6.9, 8.45, "5종 다차원 전망 설계", ha='center', fontsize=8.0, color='#37474f', weight='bold')

# 5종 q 공식 세로 나열 (가독성 최적화)
ax_main.text(6.9, 8.02, r"$q^{\mathrm{raw\_lam}} = \max(0, q_0 \lambda_t^{\mathrm{raw}}/\bar{\lambda})$", ha='center', fontsize=7.5, color=DARK_BLUE, weight='bold')
ax_main.text(6.9, 7.62, r"$q^{\mathrm{lambda}} = q_0 \cdot \mathrm{clip}(\lambda_t/\bar{\lambda}, 0.1, 3.0)$", ha='center', fontsize=7.5, color=DARK_BLUE, weight='bold')
ax_main.text(6.9, 7.22, r"$q^{\mathrm{inv\_lambda}} = q_0 \cdot \mathrm{clip}(\bar{\lambda}/\lambda_t, 0.1, 3.0)$", ha='center', fontsize=7.5, color=DARK_BLUE, weight='bold')
ax_main.text(6.9, 6.82, r"$q^{\mathrm{vol\_spread}} = q_0 \cdot \mathrm{clip}(\Delta\hat{\sigma}_t/\overline{\Delta\hat{\sigma}}, 0.1, 3.0)$", ha='center', fontsize=7.5, color=DARK_BLUE, weight='bold')
ax_main.text(6.9, 6.42, r"$q^{\mathrm{ff3}} = \mathbf{p}^\top \hat{\mathbf{r}}$", ha='center', fontsize=7.5, color=DARK_BLUE, weight='bold')

# ------------------------------------------------------------------------------
# [3열: 뷰 불확실성 \omega] (x: 7.8 ~ 9.5, 중심 x = 8.65)
# ------------------------------------------------------------------------------
ax_main.text(8.65, 8.7, r"3. 뷰 불확실성 [$\omega$]", ha='center', fontsize=9.2, weight='bold', color=DARK_BLUE)
ax_main.text(8.65, 8.45, "Uncertainty 추정", ha='center', fontsize=8.0, color='#37474f', weight='bold')

ax_main.text(8.65, 7.8, "• He-Litterman (HL)", ha='center', fontsize=8.5, weight='bold', color='#37474f')
ax_main.text(8.65, 7.4, r"$\omega^{\mathrm{HL}} = \tau \mathbf{p}^\top \boldsymbol{\Sigma} \mathbf{p}$", ha='center', fontsize=8.2, color=DARK_BLUE, weight='bold')
ax_main.text(8.65, 6.9, "• FF3 Residual", ha='center', fontsize=8.5, weight='bold', color='#37474f')
ax_main.text(8.65, 6.45, r"$\omega^{\mathrm{ff3}} = \max((q_{t-1} - \mathbf{p}_{t-1}^\top \mathbf{r}_t)^2, 10^{-8})$", ha='center', fontsize=7.2, color=DARK_BLUE, weight='bold')

# ==============================================================================
# 3. [Box 3] Market equilibrium portfolio / 시장 균형 Prior (중간 좌측, w=4.0, h=2.6)
# ==============================================================================
box3 = patches.FancyBboxPatch((0.5, 3.3), 4.0, 2.6, boxstyle="round,pad=0.08", fc=LIGHT_BG, ec=BORDER_COLOR, lw=1.8)
ax_main.add_patch(box3)
ax_main.text(0.7, 5.65, "시장 균형 사전 분포 [Prior]", fontsize=12, weight='bold', color=DARK_BLUE)

# 사전 수익률 계산 공식 기입
ax_main.text(0.7, 5.3, r"• 균형수익률: $\boldsymbol{\pi} = \lambda \boldsymbol{\Sigma} \mathbf{w}_{\mathrm{mkt}}$ (역최적화)", fontsize=10.5, color=DARK_BLUE)
ax_main.text(0.7, 5.05, r"• Ledoit-Wolf 수축 공분산 행렬 $\boldsymbol{\Sigma}$ 사용", fontsize=9.5, color='#37474f')

# Prior 벨커브 임베딩 (Subplot x비율: 0.08 ~ 0.38)
draw_bell_curve([0.08, 0.38, 0.30, 0.10], 0, 1, ACCENT_BLUE, 'Prior', r"$\boldsymbol{\pi}$")
# 수식 정렬
ax_main.text(2.5, 3.38, r"$\boldsymbol{\mu}_{\mathrm{prior}} \sim \mathcal{N}(\boldsymbol{\pi}, \tau \boldsymbol{\Sigma})$", ha='center', fontsize=11, color=ACCENT_BLUE, weight='bold')

# ==============================================================================
# 4. [Box 4] View portfolio / 투자자 전망 View (중간 우측, V10 오리지널 보관용 대형 규격)
# ==============================================================================
box4 = patches.FancyBboxPatch((5.5, 3.3), 4.0, 2.6, boxstyle="round,pad=0.08", fc=LIGHT_BG, ec=BORDER_COLOR, lw=1.8)
ax_main.add_patch(box4)
ax_main.text(5.7, 5.65, "투자자 전망 분포 [View]", fontsize=12, weight='bold', color=DARK_BLUE)

# 전망 핵심 가설 강조
ax_main.text(5.7, 5.3, "투자자 뷰 (View): 저변동성 자산군이 고변동성 자산군 대비", fontsize=9.5, color=ACCENT_RED, weight='bold')
ax_main.text(5.7, 5.05, "                   초과수익을 달성할 것으로 전망", fontsize=9.5, color=ACCENT_RED, weight='bold')

# View 벨커브 임베딩 (Subplot x비율: 0.60 ~ 0.90)
draw_bell_curve([0.60, 0.38, 0.30, 0.10], 0.8, 1.2, ACCENT_RED, 'View', r"$q$")
# 수식 정렬 (조건부 통일)
ax_main.text(7.5, 3.38, r"$q \sim \mathcal{N}(\mathbf{p}^\top \boldsymbol{\mu}_{\mathrm{prior}}, \omega)$", ha='center', fontsize=11, color=ACCENT_RED, weight='bold')

# ==============================================================================
# 5. [Box 5] 사후 결합 분포 및 최적 가중치 (최하단 대형 박스 - 3구획 카드 구조화)
# ==============================================================================
box5 = patches.FancyBboxPatch((0.5, 0.4), 9.0, 2.3, boxstyle="round,pad=0.08", fc=LIGHT_BG, ec=BORDER_COLOR, lw=1.8)
ax_main.add_patch(box5)
ax_main.text(0.7, 2.4, "사후 결합 분포 및 포트폴리오 최적화", fontsize=13, weight='bold', color=DARK_BLUE)

# [구획 1] 좌측 카드: Prior + View -> Posterior 3색 융합 벨커브 그래프 (mu, Sigma 볼드화)
card1 = patches.FancyBboxPatch((0.7, 0.55), 3.4, 1.7, boxstyle="round,pad=0.02", fc=CARD_BG, ec=CARD_BORDER, lw=1)
ax_main.add_patch(card1)
ax_main.text(2.4, 2.05, "정보 융합 (Bayesian Overlay)", ha='center', fontsize=9.5, weight='bold', color=ACCENT_GREEN)
draw_fusion_bell_curve([0.08, 0.08, 0.30, 0.10])
ax_main.text(2.4, 0.58, r"$\boldsymbol{\mu}_{\mathrm{post}} \mid q \sim \mathcal{N}(\boldsymbol{\mu}_{\mathrm{BL}}, \boldsymbol{\Sigma}_{\mathrm{BL}})$", ha='center', fontsize=11, color=ACCENT_GREEN, weight='bold')

# [구획 2] 중앙 카드: 사후 결합 파라미터 수식 (기대수익률 도출)
card2 = patches.FancyBboxPatch((4.3, 0.55), 2.5, 1.7, boxstyle="round,pad=0.02", fc=CARD_BG, ec=CARD_BORDER, lw=1)
ax_main.add_patch(card2)
ax_main.text(5.55, 2.05, "블랙-리터만 사후 기대수익률 도출", ha='center', fontsize=9.5, weight='bold', color=DARK_BLUE)

# BL 사후공분산 수식 (볼드화, 정밀 역행렬 괄호 및 academic top 트랜스포즈 적용)
ax_main.text(4.4, 1.50, r"$\boldsymbol{\Sigma}_{BL} = [(\tau\boldsymbol{\Sigma})^{-1} + \mathbf{p}^\top \omega^{-1}\mathbf{p}]^{-1}$", fontsize=10.5, color=DARK_BLUE)
# BL 사후평균 수식 (볼드화, 정밀 역행렬 괄호 및 academic top 트랜스포즈 적용)
ax_main.text(4.4, 1.00, r"$\boldsymbol{\mu}_{BL} = [(\tau\boldsymbol{\Sigma})^{-1} + \mathbf{p}^\top \omega^{-1}\mathbf{p}]^{-1}[(\tau\boldsymbol{\Sigma})^{-1}\boldsymbol{\pi} + \mathbf{p}^\top \omega^{-1}q]$", fontsize=9.2, color=DARK_BLUE)

# [구획 3] 우측 카드: SLSQP MVO 최적 가중치 계산 (사후 모수 볼드화)
card3 = patches.FancyBboxPatch((7.0, 0.55), 2.3, 1.7, boxstyle="round,pad=0.02", fc=CARD_BG, ec=CARD_BORDER, lw=1)
ax_main.add_patch(card3)
ax_main.text(8.15, 2.05, "평균-분산 최적화 (MVO)", ha='center', fontsize=9.5, weight='bold', color=DARK_BLUE)

# MVO 식 통합 기입 (Sigma_BL, mu_BL 볼드화)
ax_main.text(7.1, 1.55, r"$\mathbf{w}^* = \arg\min_{\mathbf{w}} \left( \frac{\lambda}{2}\mathbf{w}^\top \boldsymbol{\Sigma}_{\mathrm{BL}}\mathbf{w} - \mathbf{w}^\top \boldsymbol{\mu}_{\mathrm{BL}} \right)$", fontsize=9.2, color=DARK_BLUE)
# 제약조건
ax_main.text(7.1, 1.15, "제약조건 (Constraints):", fontsize=8.5, weight='bold', color='#37474f')
ax_main.text(7.2, 0.85, r"$\sum_{i=1}^n w_i = 1, \quad 0 \leq w_i \leq 0.1$", fontsize=10.5, color=ACCENT_RED, weight='bold')

# ==============================================================================
# 6. 화살표 및 흐름 연결선 배치 (V2 신규 레이아웃 정밀 배분)
# ==============================================================================
# 1) 변동성 예측 모델 단독 Box -> 우상단 통합 파라미터 Box (예측 변동성 \hat{\sigma}[t] 전송, 가로 여백 대폭 확보)
# 가로 연결 화살표: x=3.5 에서 x=4.3 로 우향 연결, y=8.15
ax_main.annotate('', xy=(4.3, 8.15), xytext=(3.5, 8.15),
                 arrowprops=dict(facecolor=BORDER_COLOR, edgecolor=BORDER_COLOR, width=1.5, headwidth=7, headlength=7))
ax_main.text(3.9, 8.35, r"$\hat{\boldsymbol{\sigma}}[t]$", ha='center', fontsize=11, color=BORDER_COLOR, weight='bold')

# 2) 통합 파라미터 Box -> View Box 4 수직 하향 화살표 (뷰 파라미터 주입)
# x=7.5 상에서 y=6.2 에서 y=5.95 로 수직 하향 연결
ax_main.annotate('', xy=(7.5, 5.95), xytext=(7.5, 6.2),
                 arrowprops=dict(facecolor=BORDER_COLOR, edgecolor=BORDER_COLOR, width=1.5, headwidth=7, headlength=7))

# 3) Prior 및 View -> 사후결합 대형 결합 화살표 구조
# Prior Box 3 (x=2.5, y=3.3) 과 View Box 4 (x=7.5, y=3.3) 의 중간 결합 축
# Box 3과 Box 4 사이의 대형 플러스 기호 (+) - 정중앙 대칭축 x=4.85 에 정렬
ax_main.text(4.85, 3.9, "+", fontsize=28, weight='bold', ha='center', va='center', color=BORDER_COLOR)

# 두 분포의 하향 결합 대형 화살표 (x=4.85 축 상에서 y=3.3 에서 y=2.75 로 수직 하향)
ax_main.annotate('', xy=(4.85, 2.75), xytext=(4.85, 3.3),
                 arrowprops=dict(facecolor=BORDER_COLOR, edgecolor=BORDER_COLOR, width=3.2, headwidth=10, headlength=10))

# ==============================================================================
# 7. 메인 타이틀
# ==============================================================================
ax_main.text(5.0, 9.6, "통합 Black-Litterman 포트폴리오 자산 배분 프레임워크", fontsize=18, weight='bold', ha='center', color=DARK_BLUE)

# 이미지 출력 및 보존 (Workspace images/bl 폴더에 v2_1로 저장!)
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
output_path = os.path.join(output_dir, "bl_framework_v2_1.png")

plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close()

print(f"Publication-ready V2.1 diagram successfully generated at: {output_path}")
