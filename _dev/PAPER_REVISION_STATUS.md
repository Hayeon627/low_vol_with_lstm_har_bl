# KCI 논문 리비전 작업 상황 (2026-07-01 기준)

## 배경

- 논문: "변동성 예측을 결합한 블랙-리터만 저변동성 포트폴리오 전략"
- 저널: 지능정보연구 (KCI)
- 심사 결과: **수정 후 게재** (편위 + 심사위원 2명 모두 호의적)
- PDF: `C:/Users/서윤범/Desktop/KCI논문/변동성_예측을_결합한_블랙-리터만_저변동성_포트폴리오_전략_저자정보_제외.pdf` (44p)

## 심사 요구사항 (원문 확인 완료, 2026-07-01)

### 편집위원
> "실증 결과에 대한 통계적 유의성 검정을 추가하여 성과 차이의 신뢰성을 보다 명확히 제시하고, 제안된 슬롯 구성의 일반화 가능성 및 연구의 적용 범위와 한계에 대한 논의를 보완"

### 심사1
> "제안된 슬롯 구성이 다른 시장이나 기간에서도 유사하게 적용될 수 있는지에 대한 해석 범위" + "연구의 적용 범위 및 한계를 결론에서 보다 구체적으로 논의"

### 심사2
> "**모든 층위의 성능 비교** (표 2, 3, 4, 그림 6, 표 6) 를 수치 나열과 시각적 비교에 의존" → "**모형 간 관찰된 차이가 통계적으로 유의미한 수준인지를 적절한 통계적 검정**"
> "변동성 예측 결과가 본 연구에서 제안하는 포트폴리오 전략 외에 어떠한 방면으로 활용될 수 있는지"

## 심사 요구사항 → 작업 매핑

| ID | 요구 | 출처 | 위치 | 상태 |
|---|---|---|---|---|
| **A1** | 표 2 변동성 예측 성능 검정 | 편위 + 심사2 | 4.1절 | ✅ **완료** |
| **A2** | 표 3 슬롯별 SR 검정 | 심사2 | 4.2절 | ✅ **완료** (HAC 재검정 + 본문 정리) |
| **A3** | 표 4 marginal + 부록 B 검정 | 심사2 | 4.3절 + 부록 | 🟡 검정 완료, 본문 narrative 정리 대기 |
| **D** | 표 6 벤치마크 비교 검정 | 심사2 (자체 보강) | 4.4절 | 🟡 검정 완료, 본문 narrative 초안 있음 |
| **A4** | MCS (다중비교) | 심사2 (선택) | 부록 | ⏸ **본 라운드 skip 결정** (ROI 판단) |
| **B** | 일반화 가능성 + 적용 범위 + 한계 논의 | 편위 + 심사1 | 5절 | ⏳ **대기** |
| **C** | 변동성 예측 다른 활용 방안 | 심사2 | 5절 | ⏳ **대기** |

## 최종 통계 검정 방법론 (HAC studentized Boot-TS)

**Ledoit & Wolf (2008) 정확 구현** — NotebookLM 검증 완료

### 방법
1. **SBB (Politis & Romano, 1994)**: 페어 적용, B = 10,000, 평균 블록 길이 T^(1/3) 기간별 가변 (30개월 → 3, 210개월 → 6)
2. **Studentized 통계량**: t = (Δ_SR − Δ_obs) / SE_paired
3. **HAC SE**: Newey-West Bartlett kernel, lag = T^(1/3)
   - z_t = (e_L, e_A, e_L², e_A²) 벡터 (초과수익률 + 그 제곱)
   - Delta method: SE² = ∇f' · Ψ_HAC · ∇f / T
4. **Bootstrap-t 방식**: p-value + 95% 신뢰구간 (부트스트랩 t 분포 percentile)

### 인용 정리
- **Politis & Romano (1994)**: SBB 방법 자체
- **Ledoit & Wolf (2008)**: 페어 SR 차이 검정 framework + HAC 표준오차 구조
- 4.1 방법 문단에서 통합 인용 → 4.2 상세 방법 문단에서 재설명

### 4.1 은 별도 방법
- 페어 손실차 검정 (RMSE, Spearman, Hit) — SR 검정 아님
- SBB + Cohen's d_z 효과 크기
- Ledoit-Wolf framework 미적용 (SR 특수 문제 아님)

## 안 한 검정 (의도적, 심사 요구 밖)

- 슬롯 간 비교 (q_lam vs q_ff3 직접 검정) — MCS 영역
- ω 간 비교 (Ens ω=err vs ω=he) — descriptive 충분
- 표 4 marginal 검정 — 옵션 B, per-slot 90 슬롯 + 표 5 count 로 우회
- 같은 모델 내 ω 변경 효과 — 튜터님 질문 대기 중

## A1 완료 사항 (4.1 절)

- 4 metric × 6 pair × 5 period = 120 검정 (SBB percentile)
- 표 2: 4 모형 × 4 메트릭 × 5 기간 통합 표, 컬럼 순서 Ens | LSTM | HAR | ANN
- 각 셀: raw 값 + sig + d*
- Word TSV 완료
- 4.1 방법 문단 확장: SBB + Ledoit-Wolf framework 안내 (4.2 참조)

## A2 완료 사항 (4.2 절) — 최종

### 검정
- HAC studentized bs90 재실행 (percentile 폐기, IID Memmel 폐기)
- 결과: `outputs/99_main_analysis/bs90_hac.pkl`
- 카운트 (표 3 anchor 계열 + 부록 B):
  - ω=err: All 0, R1 3, R2 0, **R3 16**, R4 1 (총 20/225)
  - ω=he: All 0, R1 2, R2 0, R3 2, R4 1 (총 5/225)
  - percentile 43 → HAC 25 (보수적 개선)

### 표 3 (13 슬롯 1-step variation)
- HAC 기준 sig **1개만** (SET3 w^rp R1 = -0.267*)
- 이전 percentile 11 sig 대비 대폭 감소

### 본문 narrative 완성 (오타 3개 남음, 사용자 정정 중)
- Para 1: 슬롯 표기 규칙 + 소개
- **Para 2: 방법 문단 (Boot-TS 상세 설명)** 신규
- 표 3
- Para 3: 전체 개관 (Δ=+0.000, 슬롯 설계 필요)
- Para 4: q 부호 안정성 (표 3 anchor 계열 sig 0 정직 표현)
- **Para 5: p 대형주 완화 + q + p 결합 조건 강조** ⭐ 논문 하이라이트
- Para 6: w_mkt (w^rp R1 만 sig 정정)
- Para 7: ω (R1 예외 명시 + 검정 결과)

### 잔여 오타 (사용자 워드 정정)
1. Para 4: "계열(p^mcap 조건)에 대한" (조사 "에" 누락)
2. Para 5: "p 차원의" (띄어쓰기)
3. Para 5: "q≥0 이더라도" (이중 스페이스)

## A3 진행 사항 (4.3 절 + 부록 B) — 대기

### 검정
- HAC bs90_hac.pkl 완료 (A2 와 공유)
- 표 3 부록 A.7 (Sharpe ω=err): 20 sig 셀
  - p^eq: R3 10 sig (mcap/eq/rp prior × q^lam/raw/inv/vsp)
  - p^rp: R3 6 sig (eq/rp prior × q^lam/raw/vsp)
  - p^mcap: R3 sig 없음
- 부록 A.10 (Sharpe ω=he): 5 sig (미미)
- 부록 A.8, A.11 (Sortino): 검정 미적용 (Sharpe만)
- 부록 A.9, A.12 (MDD): 경로 의존적, 검정 미적용

### 본문 narrative 수정 대기
- Para 3 (R3 marginal): 25/45 → **16/45** 정정
- Para 4 (R1, R2 marginal): 11/45 → **3/45** 정정, p^mcap 국한 명시
- Para 5 (q 차원 marginal): q^ff3 R3 비유의 (기존 percentile 결과와 동일)
- 부록 B 캡션: "A.7/A.10 (Sharpe) HAC 검정, A.8/A.11 (Sortino), A.9/A.12 (MDD) 는 raw 참고"

## D 진행 사항 (4.4 절, 벤치마크 비교) — 대기

### 검정
- 5 BL × 4 comparator × 5 기간 = 100 검정 완료 (HAC)
- 결과: `outputs/99_main_analysis/bs100_hac.pkl`
- sig 셀 5개:
  - vs SPY: Ens-adaptive (p^eq) R3 +0.273*
  - vs 1/N: Ens-adaptive (p^eq, p^rp) R4 +0.594*, +0.629*
  - vs Risk Parity: Ens-adaptive (p^eq, p^rp) R4 +0.620*, +0.655*
  - vs ANN-anchor: **모두 비유의** (percentile 에선 Ens-anchor R1 sig 였는데 HAC 에선 p=0.062)

### 핵심 결과 (Para 5 동률 입증)
- Ens-anchor vs ANN-anchor All: Δ=+0.0003, SE=0.093, t=+0.003, p=0.998, CI [-0.20, +0.19]
  - **σ 모델 단독 교체 효과 정확히 0** 입증
- R1: Δ=-0.321, t=-2.48, p=0.062, CI [-0.79, -0.08] (경계 케이스)

### 본문 narrative 초안 완료
- 표 6 별표: **0개** (HAC 기준)
- Para 3: raw 우위 + 검정 통계력 한계 설명 (Ledoit-Wolf 인용)
- Para 4: 4 Ens vs ANN 검정 (양수 15/20, sig 0)
- Para 5: Ens-anchor 동률 (Δ=+0.0003, p=0.998) + R1 경계 (p=0.062)
- Para 6: 국면별 강점 + 외부 sig 4셀 인용

## 노트북 셀 인덱스 맵 (99_main_analysis.ipynb, 2026-07-01)

| Index | Type | 내용 |
|---|---|---|
| 0-1 | md, code | [0] 환경 셋업 |
| 2-5 | md, code | [1], [1+] σ 예측 검정 (SBB percentile) |
| 6-9 | md, code | [1b], [1c] 벤치마크 SPY/1N/RP + defensive/adaptive |
| 10-13 | md, code | [2] 1-step variation, [3] 45 슬롯 |
| 14-17 | md, code | [3], [3c], [3d], [3e] |
| 18-19 | md, code | **[3+] 90 슬롯 SBB (percentile, 함수 정의 재사용)** |
| 20-21 | md, code | [3++] marginal (미실행) |
| 22-23 | md, code | [3+++] percentile 진단 |
| 24-25 | md, code | [3++++] percentile Word TSV |
| 26-27 | md, code | [3b] R1-R3 sample |
| 28-38 | ... | [4], [5], [6], [6b], [7], [9] |
| 39-40 | md, code | **[4+] 4.4 벤치마크 SBB (percentile, 함수 정의 재사용)** |
| 41-42 | md, code | **[6+] HAC studentized 재검정 (bs90 + bs100, 최종 방법)** |
| 43-44 | md, code | **[7+] HAC bs90 진단 (표 3 + 부록 A.7/A.10 TSV)** |

**주의**: cell 41-42 [6+] 이 최종 검정 결과 (bs90_hac.pkl, bs100_hac.pkl). 이전 percentile 셀은 함수 정의 유지 목적으로 남김.

## 저장 파일

- `outputs/99_main_analysis/bs90_hac.pkl` — 4.2/4.3 HAC 결과 (450 검정)
- `outputs/99_main_analysis/bs100_hac.pkl` — 4.4 HAC 결과 (100 검정)
- `outputs/99_main_analysis/bs90_per_slot.pkl` — 기존 percentile (참조용)
- `outputs/99_main_analysis/bs100_strategy.pkl` — 기존 percentile (참조용)

## 튜터님 질문 대기 항목

1. **같은 모델 내 ω^err vs ω^he 검정** 필요성 (Para 7 마지막)
   - 심사 요구 밖이라 안 해도 OK 판단, 튜터 확인 대기
2. HAC lag/kernel 선택 (T^(1/3) fixed, Bartlett) 방어 논리 — 튜터 확인 대기

## 다음 즉시 할 일 (우선순위)

### 우선순위 1
1. **4.2 오타 3개 정정** (본인 워드) — 거의 완료
2. **4.3 본문 narrative 정정** — R3 25→16, R1 11→3, 부록 B 캡션
3. **4.4 본문 narrative 최종 반영** (본인 워드) — 표 6 별표 0, Para 5, 6 정정
4. **부록 A.7, A.10 sig 별표 정정** — 셀 [7+] (5), (6) TSV 활용

### 우선순위 2
5. **5절 B (일반화, 한계)** — 편위 + 심사1 필수
6. **5절 C (활용 방안)** — 심사2 필수

### 우선순위 3
7. 4.1 절 Ledoit-Wolf 인용 자연스러운지 재확인
8. 표 캡션 컨벤션 통일 (별표 의미 안내)

## 결정 미해결 항목

- 같은 모델 내 ω 변경 검정: 튜터 결정 대기
- Sortino 검정: **skip 결정** (Sharpe 만 검정, Sortino/MDD 는 raw 참고)
- MCS (A4): **skip 결정** (본 라운드)

## 사용자 멘탈 컨텍스트

- 번아웃 회복 중이나 논문 진척 속도 유지 (2026-07-01 시점)
- 통계 석사 — 정확한 통계 지식 보유
- **NotebookLM 으로 인용 검증 습관** — 항상 원문 확인 요구
- **비판적 검토 요구** — "혹시 놓친 부분?" 자주 확인
- **한국어 우선, 영문 병기만** — 이전 세션 부터 일관
- 결정 패턴: 한 번에 깊이 검토 → 확정 후 진행
- 5장과 4.1 정합성 중요 (LSTM "단순 구조" vs "복잡한 구조" 모순 잡아냄)
- **표현 안전성 중시** — "유리하게 적힌 것 아니냐" 자주 지적
- 별도 메모리: `~/.claude/projects/.../memory/MEMORY.md` 참조
