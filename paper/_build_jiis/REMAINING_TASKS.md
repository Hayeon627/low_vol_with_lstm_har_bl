# 남은 태스크 상세 기록 (REMAINING_TASKS)

> 작성: 2026-06-04. 세션이 바뀌어도 이 문서와 `HANDOFF.md`만 읽으면 작업을 그대로 이어갈 수 있도록 기록한다.
> **현재 최신 산출물: `paper/JIIS_변환_CP20.docx` (38쪽)** — 양식 정합성 결함 0 (3회전 정밀 QA 완료).

---

## 0. 현재 상태 스냅샷

| 항목 | 상태 |
|---|---|
| 투고 대상 | 지능정보연구(JIIS), 일반논문(구두) — 확정 |
| 변환 파이프라인 | 완성·검증 (CP7 기반 + normalize_tables.py + finalize_doc.py, 재현 가능) |
| 양식 정합 | 용지/여백/글꼴/제목/캡션/표(booktabs·병합·음영·첨자·볼드)/번호(표 1~6·A.1~A.20, 그림 1~7·A.1) 전부 검증 통과 |
| 첫 페이지 | 국문제목·저자·교신저자(서정욱/한양대/이메일)·국문초록·주제어·영문초록·Key Words 완료. 사사 제거 완료 |
| 쪽수 | 38쪽 (JIIS 권장 15, **한도 30 초과** — A-3 참조) |

---

## A-트랙. JIIS 투고 마무리 (우선)

### A-1. 첫 페이지 자리표시자 2곳 채우기 — ⏳ 팀 정보 대기
남은 자리표시자(문서 앞부분):
1. `[Title in English — 작성 필요]` — **영문 제목**
2. `[저자 소속(국문/영문) 및 E-mail — 작성 필요]` — **저자 5인 소속·이메일**

**절차(정보 수신 시)**: `finalize_doc.py`에 교체 함수 추가(기존 `fill_en_abstract`/`fill_corresponding` 패턴 재사용) → 체인 재실행 → 새 CP. 약 5분 작업.

### A-2. 인용 누락 7키 보완 (#19) — ⏳ 사용자 BibTeX 대기
본문 9곳에 `[key? — bib 누락]` 마커로 노출 중. **su2026objective는 bib에 `su2026`으로 존재 → 사용자 작업 불필요(키 정합만 Claude 처리).**

**사용자가 줄 것 (7개)**: Google Scholar → 해당 논문 → "인용" → **BibTeX** → 블록 복사 → 채팅에 7개 일괄 붙여넣기. 키 이름이 달라도 됨(Claude가 본문 키로 교정).

| 본문 키 | 인용 맥락 | 유력 후보 (★=고신뢰) |
|---|---|---|
| cont2001 | §2 변동성 군집·장기기억 | ★ Cont (2001) Empirical properties of asset returns, *Quantitative Finance* |
| demiguel2009optimal | §2 1/N 분산투자 | ★ DeMiguel, Garlappi & Uppal (2009) Optimal versus naive diversification, *RFS* |
| hamilton1989new | 부록 A HMM (2곳) | ★ Hamilton (1989) A new approach…, *Econometrica* |
| timmermann2006forecast | 예측 결합(앙상블) | ★ Timmermann (2006) Forecast combinations, *Handbook of Economic Forecasting* |
| cochrane2005 | §2 자산가격(…, 1973와 병기) | ★ Cochrane (2005) *Asset Pricing*, Princeton (책 → publisher 필드) |
| barua2023using | §2 BL×ML 선행연구 | Barua 외 (2023), 제목 "Using…" 시작 — 팀 인용 논문 확인 필요 |
| lee2025llm | §2 LLM 관련 | Lee (2025), 제목에 LLM — 팀 인용 논문 확인 필요 |

**통합 절차(수신 시)** — 두 방식 중 택1:
- **(a) 전체 체인 재실행(정석)**: `references.bib` 갱신 → `cite.py`(src2.tex→src3.tex) → pandoc → `front_matter_splice.py` → `gen_tables.py` → CP7급 베이스 재생성 → `normalize_tables.py` → `finalize_doc.py` → pack. 모든 스크립트·src2.tex는 `_build_jiis/scripts/`에 보존됨. pandoc 2.9.2.1 사용.
- **(b) finalize 후처리(간편)**: 마커 9곳을 위치별 서식(서술형 `저자 (연도)` / 괄호형 `저자, 연도`)으로 치환 + 참고문헌 목록에 APA 항목을 알파벳 위치에 문단 삽입. 베이스(CP7) 재생성 불필요.
- 어느 쪽이든 마커가 정상 인용으로 바뀌고 참고문헌 22→29편이 된다. APA 규칙은 cite.py에 구현됨(괄호형 `&`, 서술형 `and`, 저널·권 이탤릭, 저널명 타이틀케이스).

### A-3. 분량 대응: 38쪽 > 한도 30쪽 — ⚠ 유일한 실질 차단 요소, 결정 필요
구성: 본문(서론~결론+참고문헌) ≈ 24쪽 + 부록 A~E ≈ 14쪽.

**옵션(조합 가능, 예상 절감)**:
1. **부록 그리드 6개(표 A.7~A.12, 각 47행)를 별도 보충자료(Supplementary)로 분리** — 약 6쪽 절감. 본문 영향 없음(참조 문구만 "보충자료 참조"로 수정 필요 → §4·부록 B 도입부 1~2문장, 타 저자 영역이라 **팀 승인 필요**).
2. 부록 A(HMM, 표 A.1~A.6 + 설명) 압축 또는 분리 — 약 3~4쪽.
3. 부록 C·D·E 압축(보조 표 통합) — 약 2~3쪽.
4. 본문 그림 축소(그림 1·4 등 16.4cm 정사각 → 12cm) — 약 1쪽.
- 1+4만으로 약 31쪽, 1+2(또는 3)+4로 **30쪽 이내 가능**. 시뮬레이션 빌드 요청 시 즉시 생성 가능.
- **주의**: 부록 분리·압축은 타 저자 담당 영역 포함 → CLAUDE.md §7-2(담당 외 절 무단 수정 금지)에 따라 **팀/소유자 승인 후** 진행.

### A-4. DOI 보강 — 권장 (JIIS 지침: 학술지 논문 DOI "필수")
현재 참고문헌 22편(+신규 7편)에 DOI 미표기. cite.py가 bib의 `doi` 필드를 출력하도록 1줄 확장 + bib에 DOI 추가 필요. 사용자가 신규 7편 BibTeX에 DOI 포함해 주면 신규분은 자동 해결; 기존 22편은 일괄 보강 작업으로 별도 진행(Claude가 후보 DOI 조회 → 사용자 검증 권장).

### A-5. 최종 재생성 + 최종 QA (A-1·A-2 완료 후 1회)
1. 체인 재실행(A-2 방식에 따라 (a) 또는 normalize→finalize만).
2. **검증 체크리스트**(지금까지 누적된 자동 스캔 — 스크립트화돼 있음):
   - 용지 A4·여백 3/2.3cm·Normal 11pt/1.5줄 = 샘플 일치
   - 제목: 본문 1~5 자동번호 / 참고문헌 무번호 / 부록 A~E / 부록 하위절 무번호
   - 표 27(캡션 1~6·A.1~A.20, 위·가운데) / 그림 8(1~7·A.1, 아래·가운데)
   - booktabs(세로줄 0)·음영 1,414·병합(vMerge 80)·첨자 393·벡터/값 볼드
   - `(lr)`·cmidrule·TABLEPLACEHOLDER·원시참조·빈 헤더/라벨 = 0
   - `[? — bib 누락]` = 0 (A-2 후) / 자리표시자 = 0 (A-1 후)
   - 페이지 초과 이미지 0 · 쪽수 ≤ 30 (A-3 후)
3. soffice PDF 프루프 + 주요 페이지 육안 검수 → **투고본 확정**.

### A-6. 투고 행정 (문서 외)
- JIIS 온라인 투고 시스템 제출, 연구윤리 관련 동의, 심사료 등 — `JIIS_지침_국문번역.md`(루트) 참조.
- 저자 사진(2.3×2.7cm)은 **게재 확정 후** 제출.

---

## B. 빌드 시스템 참조 (요약 — 상세는 HANDOFF.md)

> (구 B-트랙 "유사 선행논문 조사"는 2026-06-04 사용자 지시로 **폐기** — 태스크 #8·#11~#15 삭제됨.)

- **파이프라인**: prep2 → cite → pandoc(2.9.2.1, `--reference-doc=JIISsample.docx`) → front_matter_splice → gen_tables → **normalize_tables.py → finalize_doc.py** → pack(`--validate false`).
- **스크립트·중간산출 보존 위치**: `paper/_build_jiis/scripts/` (prep2.py, cite.py, front_matter_splice.py, gen_tables.py, normalize_tables.py, finalize_doc.py, src2.tex, src3.tex, tablemap2.txt, labelmap.json).
- **빠른 재생성**(현행 CP 재현): CP7 unzip → normalize_tables.py → finalize_doc.py → pack.
- **알려진 함정**(반드시 HANDOFF의 해당 절 참조): ① 본문 참조의 `~`→NBSP(U+00A0) — 패턴은 `[  ]` 필수, ② 마운트 읽기 truncation — 스크립트는 /tmp에 heredoc으로 복사 후 실행, ③ 빈 셀 `<w:p/>` 자기닫힘 — run 삽입 시 문단 통째 교체, ④ re.sub 교체 템플릿에 `\uXXXX` 불가, ⑤ f-string 식 안 백슬래시 불가.

## C. 결정 대기 요약 (사용자/팀)

1. **A-3 분량 옵션 선택** (부록 분리 범위) — 팀 승인 포함
2. **A-2 BibTeX 7건 제공** (Google Scholar → BibTeX → 채팅 붙여넣기)
3. **A-1 영문 제목 + 저자 소속/E-mail 제공**
4. (선택) A-4 기존 참고문헌 DOI 일괄 보강 진행 여부
