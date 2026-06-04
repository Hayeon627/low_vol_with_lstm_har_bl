# JIIS docx 변환 — 작업 인수인계 (HANDOFF)

> **현재 보존 파일(2026-06-04, 최종)**: **`JIIS_변환_CP21.docx`(최신본·39쪽)**, **`JIIS_변환_BASE.docx`(파이프라인 베이스·삭제 금지)**, JIISsample.docx(템플릿), `_build_jiis/scripts/`, HANDOFF.md, REMAINING_TASKS.md. (CP1~CP20 삭제됨; 아래 CP 이력은 기록용.)
> **빠른 재생성**: BASE unzip → normalize_tables.py → finalize_doc.py → pack(--validate false).
> **전체 재생성**: prep2(paper.md) → cite(src2→src3, references.bib) → pandoc 2.9.2.1(--reference-doc=JIISsample) → front_matter_splice → gen_tables(/tmp/tablemap2.txt 필요) → normalize → finalize → pack.
> **CP21 (2026-06-04)**: #19 인용 8키 해소 — 사용자가 references.bib에 8엔트리 추가(키 정합 완료, timmermann은 2006 Forecast Combinations 챕터) → cite.py에 `@incollection`(In Eds., Booktitle, Vol., pp.)·`edition`(Revised ed.) 포맷 확장 → **전체 체인 재실행**. 참고문헌 22→30편, `bib 누락` 마커 0. 영문초록·교신저자·사사제거 등 finalize 단계 전부 유지.
> ⚠ **신규 함정(중요)**: 새 샌드박스의 pandoc이 자기닫힘 태그를 `" />"`(공백)로 직렬화 → `"/>"` 가정 정규식 전부 미스(본문 스타일 제거·제목 무번호·이미지 축소 실패 → 쪽수 +14 증상). **해결**: normalize/finalize 첫 줄에서 `doc.replace(' />','/>')` 캐논화(반영됨). gen_tables는 /tmp/tablemap2.txt를 읽으므로 보존본을 /tmp로 복사 후 실행.

> 목적: `paper.md`(LaTeX) → 지능정보연구(JIIS) 투고 양식 `.docx` 변환.
> 이 문서는 compact/세션 전환 후에도 작업이 끊기지 않도록 현재 상태·결정·파일 위치·남은 작업을 기록한다.
> 최종 업데이트: 2026-06-04 (CP3까지 완료 시점)

---

## 0. 확정 결정 사항 (사용자 승인)

- **투고 대상**: 지능정보연구(JIIS) / 한국지능정보시스템학회(KIISS) — 확정.
- **변환 범위**: 논문 **전체**(서론~결론 + 전체 부록, 90슬롯 표 포함).
- **분량**: 지금은 **축소하지 않고 그대로 변환**(쪽수는 측정·보고만; 한도 30쪽/권장 15쪽은 추후 판단).
- **색상 슬롯표**: **Word 표로 재구성 + 셀 음영**(posgreen `#D5E8D4` / negred `#F8CECC`, 소스의 `\cellcolor` 표시를 그대로 미러링).
- **영문 초록/키워드**: 팀원 작성 중 → **자리표시자**로 진행.

## 1. 핵심 파일 위치 (워크스페이스 기준)

| 용도 | 경로 |
|---|---|
| 원본 논문(LaTeX) | `paper/paper.md` (활성 §10, 소절 22, 주석 454줄, 수식 50환경, 표 cellcolor 308셀, 그림 7) |
| 양식 템플릿 | `paper/JIISsample.docx` |
| 그림(최종) | `paper/images/paper_final/` — 7개: ann_architecture, benchmark_plot, bl_pipeline, lstm_cell, marginal_mean, r4_ff3_lam, walkforward (소스는 `Figure/`로 참조 → 매핑 필요) |
| 참고문헌 | `paper/references.bib` (33 엔트리) |
| 변환 산출(체크포인트) | `paper/JIIS_변환_CP1초안.docx`, `paper/JIIS_변환_CP2.docx`, `paper/JIIS_변환_CP3.docx` |
| 작업 스크립트·중간본 | `paper/_build_jiis/scripts/` (prep2.py, cite.py, front_matter_splice.py, src2.tex, src3.tex, tablemap2.txt, labelmap.json) |
| PDF/페이지 프루프 | `paper/_build_jiis/*.png, draft.pdf` |
| 지침 번역 | `JIIS_지침_국문번역.md` (루트) |

## 2. 양식 사양 (검증 완료, 변환 시 준수)

- 용지 A4(11906×16838), 여백 **위·아래 3cm(1701 twips)·좌·우 2.3cm(1304 twips)** — `--reference-doc`로 자동 상속됨.
- 본문 '표준'(Normal): 국문 **바탕**/영문 **Times New Roman 11pt(sz 22)**, 줄간격 1.5(line 360).
- 제목 스타일 ID: **제목1=`1`(14pt 굵게), 제목2=`2`(12pt), 제목3=`3`(11pt)** — pandoc이 자동 매핑 확인됨.
- 표 캡션 **위** `<표 N>` / 그림 캡션 **아래** `<그림 N>`, 가운데 정렬·들여쓰기 0; 표 내용은 '표본문'(center, line 240, after 0).
- 참고문헌: 본문 끝, **국내(가나다)→국외(알파벳)→URL**, APA. (현재 전부 국외)
- 저자 사진 2.3×2.7cm(게재 확정 후).

## 3. 변환 파이프라인 (엔진/순서)

- 엔진: **pandoc 2.9.2.1 (LaTeX→docx) + `--reference-doc=JIISsample.docx` + `--resource-path=paper/images/paper_final`**. 수식은 OMML로 자동 변환(검증됨). **citeproc 없음** → 인용/참고문헌은 `cite.py`가 references.bib에서 직접 생성.
- 순서: ①전처리(prep2.py: 주석제거·이미지경로·상호참조 번호화·복잡표 마커) → ②인용/참고문헌(cite.py) → ③pandoc → ④첫 페이지 XML 재작성(front_matter_splice.py) → ⑤pack(`--validate false`) → ⑥soffice PDF 검수.
- 복잡/색상 표는 pandoc이 못 다룸 → `TABLEPLACEHOLDER{n}` 마커로 빼두고 **별도 생성·주입**(Phase 4, 아직 미완).

### 재개(resume) 레시피 (sandbox)
```
SK=<.claude/skills/docx>
P=<...>/paper ; ABS="$P/images/paper_final"
# 처리된 최종 소스(src3.tex)는 _build_jiis/scripts에 보존됨
pandoc _build_jiis/scripts/src3.tex -f latex --reference-doc=$P/JIISsample.docx --resource-path=$ABS -o draft.docx
unzip draft.docx -d dx ; python3 _build_jiis/scripts/front_matter_splice.py dx/word/document.xml
python3 $SK/scripts/office/pack.py dx out.docx --original draft.docx --validate false
```
(주의: `/tmp`·`/sessions/.../mnt` 경로는 세션마다 달라질 수 있음 → 워크스페이스 보존본 사용.)

## 4. 완료 상태 (CP1 → CP3)

- **CP1** (`JIIS_변환_CP1초안.docx`): 기반 변환. 제목→제목1/2/3, 여백/A4 상속, **수식 1,364 OMML**, 그림 7 임베드, 단순표 18. 색상표는 placeholder.
- **CP2** (`JIIS_변환_CP2.docx`): **Phase 2 첫 페이지** JIIS 구조(국·영 제목/저자/소속·이메일/교신/사사/국문초록+주제어/영문초록 자리표시자) + **Phase 3 상호참조 전부 번호화**(수식 27개 번호, 절·그림·표 참조, 원시 `[eq:]` 0).
- **CP3** (`JIIS_변환_CP3.docx`): **Phase 6 인용·참고문헌**. 본문 인용 `(저자, 연도)`/`저자 (연도)` 채움, **참고문헌 22편 APA·국외 알파벳순 [국외 문헌]** 생성·렌더 확인. 59쪽.
- **CP5/CP6/CP7**: 색상 슬롯표 13개 주입·APA 보정·벤치마크표(멀티라인 행) 복구 완료. (CP7이 표 주입 최종본)
- **CP8** (`JIIS_변환_CP8.docx`, 최신): **샘플 표/그림 서식 정규화**. `_build_jiis/scripts/normalize_tables.py`로 CP7 위에 적용 —
  - 표 27개 전부 표 스타일 `a7`(내부 가로/세로 sz4) + 표 수준 바깥 4면 `sz18`(2.25pt 굵게) + tblLook 04A0 + 가운데. (JIISsample 예시표와 동일)
  - 모든 셀 `vAlign center` + 셀 문단 `a8`(표본문). 셀 음영(shd 1414개)·gridSpan·vMerge·런 굵게 전부 보존.
  - 표 캡션 `<표 N>`: 표준 문단·가운데·굵게 제거·keepNext(표 위). 그림 캡션 `<그림 N>`: 표준 문단·가운데(그림 아래).
  - 미정의 캡션 스타일(TableCaption/ImageCaption) 제거 → 표준 문단으로(LibreOffice·Word 모두 가운데 보장). 렌더 검수: 표1/표5/표6/그림1 OK.
  - 재실행: `unzip CP7 → python3 normalize_tables.py word/document.xml → pack.py --validate false`.
- **CP9** (`JIIS_변환_CP9.docx`, 최신·권장): **표 스타일 결정 변경 → 원 논문 PDF의 booktabs + 지표명 multirow 병합**(사용자 재확정, CP8의 JIIS 격자 대체).
  - `normalize_tables.py` 전면 개편(booktabs+merge 버전):
    - **booktabs 선**: 세로줄 전부 제거, 가로 rule만 — 상단/하단 굵게(sz12), 헤더 아래·그룹 사이 light(sz4). tcBorders로 행별 부여, tblBorders는 none.
    - **표2(tab:sigma_pred)**: pandoc이 잃은 라벨(RMSE↓·Spearman↑·Hit-Low(30%)↑·Hit-High(30%)↑) **복원** 후 5행씩 세로병합(vMerge)·세로 가운데. (Period=='All' 행을 그룹 시작으로 탐지)
    - **색상표(표3·부록 표13~18)**: 빈 col0 = multirow 연속 → vMerge 병합(표3 SET1~4, 부록 p^mcap/p^eq/p^rp 각 15행). 비색상 표의 빈 col0(예: 국면표 '전체' 요약행)은 병합 제외.
    - 음영(shd 1414)·gridSpan·런 굵게·캡션 가운데 전부 보존. vMerge restart 26개. 39쪽.
  - **검수**: 표2/표3/표5/표6/부록그리드(표16) 렌더 확인 — 원 PDF와 동일한 booktabs 외형. 부록 18열은 세로줄이 없어 밀도가 높으나 음영으로 구분됨(원하면 부록만 light 세로줄 복원 가능).
  - ⚠ **마운트 주의**: 워크스페이스의 `normalize_tables.py`를 bash가 읽을 때 동기화 지연으로 **잘린 캐시**를 볼 수 있음(증상: 출력 없음·미변경, EXIT=0). 이 경우 동일 내용을 `/tmp/normalize_tables.py`로 heredoc 작성해 실행할 것(검증됨).
- **CP10** (`JIIS_변환_CP10.docx`, 최신·권장): 부록 광폭표 **줄바꿈/늘어짐 해소** + **셀 내 수식 위/아래첨자** 표기. (`normalize_tables.py`에 2기능 추가)
  - **광폭표(열 ≥ 12: 표3·부록 표13~18)**: `tblLayout fixed` + 균등 열폭(9298/ncols) + 런 글꼴 6.5pt(sz13) + 셀 여백 축소 → 데이터가 한 줄에 들어가 행이 늘어지지 않음. 38쪽.
  - **셀 내 수식**: 텍스트로 풀려 있던 `q^ff3`, `p^mcap`, `w_mkt`, `p^eq`, `q^lam` 등을 런 분할 + `<w:vertAlign superscript/subscript>`로 **진짜 위/아래첨자** 처리(393개). 표2/표3/표5/표6/부록 전부 적용. (본문·캡션 수식은 pandoc OMML로 이미 정상; 이 처리는 표 셀 한정)
  - 음영·굵게·병합·캡션 전부 보존. 검수: 부록 MDD 그리드 고해상도 확인 — 줄바꿈 0, q^lam·w^mcap·p^eq 위첨자 정상.
  - (참고) 캡션 속 `w_mkt`는 평문 유지(요청이 표 내부 한정). 필요 시 캡션도 첨자화 가능.
- **CP11** (`JIIS_변환_CP11.docx`, 최신·권장): **#20 번호·스타일 정리 완료**. `_build_jiis/scripts/finalize_doc.py`를 normalize 다음 단계로 실행.
  - **참고문헌 제목 무번호**: 제목 스타일 "1"(numId 2 자동번호)을 참고문헌 문단에서 `numId 0`으로 덮어써 "6." 제거 → "참고문헌".
  - **부록 A~E**: 부록 5개 제목을 무번호화 + "부록 A. "~"부록 E. " 접두(문서 순서 H1 인덱스 6~10). 부록 하위절(A1~A7 등, 스타일 "2")도 무번호화(이전 "7.1 A1" 중복 → "A1"). 본문 절(2.1·4.4 등)은 자동번호 유지.
  - **본문 문단 스타일**: pandoc `FirstParagraph`(72)·`BodyText`(124) pStyle 제거 → 표준(Normal, 1.5줄). 이 영향으로 쪽수 38→40(본문이 규격대로 1.5줄 적용된 결과).
  - **표6 캡션**: gen_tables가 떨어뜨린 `\ref{app:benchmark}` → "부록 E 참조" 보정.
  - **ANN-anchor 인용**: 벤치마크 표 4곳 `ANN-anchor pyo2018` → `ANN-anchor (Pyo & Lee, 2018)`.
  - 검수: 부록A 제목/A1·A2·A3 하위절, 참고문헌 무번호, 표6 캡션·셀, 본문 4.4 절번호 렌더 확인.
  - ⚠ **쪽수 40 = JIIS 한도(30) 초과**. 분량 축소는 사용자 보류 상태 → #21/추후 결정. (본문만은 ~25쪽, 부록이 대부분)
  - 파이프라인 최종 순서: prep2 → cite → pandoc → front_matter → gen_tables → **normalize_tables.py → finalize_doc.py** → pack.
- **CP12** (`JIIS_변환_CP12.docx`, 최신·권장): **#21 최종 QA 완료본**. finalize_doc.py에 그림3 캡션 복원 단계 추가.
  - **그림3 복원**: `fig:ensemble_flow`는 이미지가 아니라 tabular 흐름도 → pandoc이 표로 바꾸며 `\caption` 누락. 흐름도 표 뒤에 "&lt;그림 3&gt; Performance-weighted 앙상블 기반의 변동성 예측 흐름." 캡션(하단·가운데) 삽입 → 그림 1~8 연속 복원, 본문 "그림 3" 참조 정합.
  - **QA 결과(샘플 대비 전수 점검)**: 용지 A4·여백(3cm/2.3cm)·Normal 11pt/1.5줄/바탕·TNR·제목1 14pt굵게·제목2 12pt = **샘플과 완전 일치**. 본문 절 1~5 자동번호 / 참고문헌·부록 A~E 무번호 / 부록 하위절 무번호 / 표캡션 26개(상단·가운데, 1~26 연속) / 그림 8개(하단·가운데, 1~8 연속) / 표 27개 booktabs·세로줄0·음영1414 / 수식 OMML·미해결참조0 / 잔여 LaTeX 아티팩트 0 / 빈 괄호·stray 0. 첫 페이지 JIIS 구조 완비(영문·저자정보는 팀원 자리표시자).
  - **남은 항목(보류, 결함 아님)**: ① 미해결 인용 마커 8키 `[key? — bib 누락]`(9곳) = #19: barua2023using, cochrane2005, cont2001, demiguel2009optimal, hamilton1989new, lee2025llm, su2026objective(→su2026 키 정합), timmermann2006forecast. ② 영문 제목/초록/주제어·저자 소속(팀원). ③ **쪽수 40 > JIIS 한도 30**(분량 축소 보류).
- **CP14** (`JIIS_변환_CP14.docx`, 최신·최종·권장): 사용자 2차 정밀 QA에서 발견된 **2단 헤더·multicolumn 결함 3건**을 finalize_doc.py에 복구 로직으로 추가.
  - **표21(tab:r4_anchor_weights)·표22(tab:r4_q_sign)**: `\multicolumn{2/3}{c}{앙상블 (E)}{ANN (A)}` + `\cmidrule` 2단 헤더를 pandoc이 망가뜨림(그룹헤더 행 비고 "(lr)2-4 …"가 셀에 새어듦). → 헤더 2줄을 소스 기준 재구성(그룹헤더+cmidrule(light)+컬럼헤더+header rule). booktabs·gridSpan 적용.
  - **표1(tab:regimes)**: `\multicolumn{1}{l}{전체}` 텍스트가 pandoc에서 드롭됨(요약행 첫 칸 공백) → "전체" 라벨 주입 + 요약행 상단 light rule(소스 `\midrule`) 복구. (주의: 빈 셀은 `<w:p/>` 자기닫힘이라 run 주입 시 문단 통째 교체 필요)
  - **최종 검증(CP14)**: 표 27·세로줄 0·음영 1414 / (lr)·cmidrule 잔재 0 / 빈 헤더행·빈 col0 데이터행 0 / 표캡션 26·그림캡션 8(연속) / 수식 OMML 609·미해결참조 0. **양식 정합성 결함 0**. 40쪽.
  - 빌드 스크립트 보존: `_build_jiis/scripts/normalize_tables.py`(booktabs+병합+수식), `finalize_doc.py`(번호·스타일·그림3·표21/22·표1). 마운트 읽기 지연 시 /tmp로 heredoc 작성해 실행.
- **CP15** (`JIIS_변환_CP15.docx`, 최신·최종·권장): **수식·볼드 정밀 QA** 결과 반영.
  - **본문 수식(OMML)**: \mathbf(p·w·x·r·X·P)·\boldsymbol(Σ·π·μ) 모두 `m:sty="b"`로 볼드 보존 확인 — 본문은 무결.
  - **표25(MDD)·표26(연환산)**: 소스가 값 볼드를 `$\mathbf{값}$`으로 표기(표6·24는 `\textbf`) → gen_tables가 미인식해 **최우수값 10곳 볼드 누락** → finalize에 소스 (행,열) 매핑 복원(`fix_benchmark_value_bold`). 같은 값(+16.4% 2회)도 소스 위치만 볼드 — 검증 완료.
  - **표 라벨 벡터 볼드**: Notation Guide상 $\mathbf{p}$·$\mathbf{w}$는 볼드 → normalize mathify에 규칙 추가(위/아래첨자 직전의 단독 p·w, 또는 셀 전체 p·w → 볼드런). 벡터볼드런 157. q·ω(스칼라)는 비볼드 유지(오볼드 0 검증).
  - gen_tables.py에도 `\mathbf{숫자}` 볼드 인식 패치(향후 전체 재생성 대비).
  - 최종 스캔: 표27·세로줄0·음영1414·(lr)0·빈헤더0·빈col0 0·표캡션26·그림캡션8·OMML609·미해결참조0. 40쪽.
- **CP16** (`JIIS_변환_CP16.docx`, 최신·최종·권장): **부록 표/그림 재번호 — 원본 LaTeX 체계 복원**(사용자 지적).
  - 소스 1283~1288행: `\appendix` + `\renewcommand{\thetable}{A.\arabic{table}}` + `\setcounter{table}{0}`(figure 동일) → **원본 PDF는 부록에서 표 A.1~A.20, 그림 A.1**. 기존 변환(연속 표7~26·그림8)은 이를 누락(이전 grep이 head로 잘려 재정의를 못 봄).
  - finalize `renumber_appendix`: 캡션 21곳(`<표 7>`→`<표 A.1>` … `<표 26>`→`<표 A.20>`, `<그림 8>`→`<그림 A.1>`) + 본문 참조 11곳 재번호(범위 `표 13–15`→`표 A.7–A.9`, `표 16–18`→`표 A.10–A.12` 포함).
  - ⚠ **NBSP 함정**: LaTeX `표~\ref`의 `~`가 pandoc에서 U+00A0(NBSP)로 변환 → 본문 참조가 "표 24" 형태라 일반 공백 패턴이 못 잡음. 패턴은 반드시 `[  ]` 사용(검증 스캔도 동일). re.sub 교체 템플릿에 `\uXXXX` 불가 → 실제 문자/람다 사용.
  - 검증: 캡션 1~6+A.1~A.20 / 그림 1~7+A.1, 잔여 구번호 0(NBSP 인식 스캔), 본문 A.x 참조 11, p39 "표 A.18는 Sortino…"·p40 `<표 A.20>` 렌더 확인. 40쪽.
- **CP17** (`JIIS_변환_CP17.docx`, 최신·최종·권장): 사용자 요청 2건.
  - **그림2(BL 파이프라인) 축소**: 16.4×27.6cm(본문영역 23.7cm 초과·페이지 이탈) → finalize `shrink_images`(높이 한도 6.8e6 EMU=18.9cm, 비례 축소; wp:extent+a:ext 동시) → 11.2×18.9cm, 캡션+본문 수 줄과 한 페이지 수납. 쪽수 40→38.
  - **부록 그리드(표 A.7~A.12) w_mkt 5행 구분**: normalize에 col1(w_mkt) 그룹 로직 추가 — 빈칸=연속 병합(vMerge, 6표×9그룹=54) + 각 그룹 시작행에 가는 top rule(sz4). p그룹 경계는 기존 굵은 구분 유지. (shaded & span≥2 조건이라 표3·표4·5에는 영향 0 검증)
  - 회귀 스캔: 표27·세로줄0·음영1414·(lr)0·캡션 1~6+A.1~A.20/그림 1~7+A.1·구번호0·OMML609·페이지초과 이미지 0. vMergeRestart 80.
- **CP18** (`JIIS_변환_CP18.docx`, 최신·최종·권장): **영문 초록·Key Words 삽입**(사용자 제공 원문).
  - finalize `fill_en_abstract`: 자리표시자 `[영문 초록 — 팀원 작성 예정]`·`[영문 키워드 3–5개 — 작성 필요]`를 원문으로 교체. `p^eq`/`p^rp` 위첨자·`w_mkt` 아래첨자 런 분리, en-dash(–) 5곳·em-dash(—) 2곳·ω·`S&P`(&amp;) 원문 그대로. 전문 일치 검증 통과.
  - **남은 자리표시자 4곳**: 영문 제목([Title in English]), 저자 소속(국문/영문)+E-mail, 교신저자(성명/주소/Tel/Fax/E-mail), 사사(Acknowledgement). 받으면 같은 방식으로 삽입.
  - 38쪽 유지.
- **CP19** (`JIIS_변환_CP19.docx`, 최신·최종·권장): **교신저자 삽입**(사용자 제공, 성명은 서정욱으로 확인).
  - finalize `fill_corresponding`: "교신저자: 서정욱 / Department of Applied Artificial Intelligence, Hanyang University, 55, Hanyangdaehak-ro, Ansan-si, 15588, Republic of Korea / E-mail: sju02051@hanyang.ac.kr" (Tel/Fax 미제공 → 생략; 필요 시 추가).
  - **남은 자리표시자 3곳**: 영문 제목, 저자 소속(국문/영문)+E-mail, 사사.
- **CP20** (`JIIS_변환_CP20.docx`, 최신·최종·권장): **사사 없음 확정** → finalize `remove_ack`로 Acknowledgement 라벨+자리표시자 문단 2개 제거. **남은 자리표시자 2곳**: 영문 제목, 저자 소속(국문/영문)+E-mail.

## 5. 남은 작업 (Phase 4·5·7·8·9 + 보정)

1. **Phase 4 — 색상 슬롯표 9개 생성·주입 (CP4, 최대 작업)**
   - 마커→라벨(`_build_jiis/scripts/tablemap2.txt`):
     - 3=tab:1step_variation, 4=tab:p_matrix_avg, 5=tab:p_matrix_win
     - 13~18 = tab:app_grid_{sharpe,sortino,mdd}_{err,he} (부록 90슬롯)
   - 각 표를 소스(paper.md의 LaTeX 또는 `paper/appendix_grid_tables.md`)에서 파싱 → OOXML 표 생성(셀 음영 posgreen `#D5E8D4`/negred `#F8CECC`, gridSpan/vMerge, '표본문' 스타일, 캡션 상단 `<표 N>`) → `document.xml`의 `TABLEPLACEHOLDER{n}` 문단을 치환.
2. **Phase 6b — 인용 APA 3가지 보정** (cite.py 수정):
   - (a) **괄호형 인용 `and`→`&`** (현재 `(Black and Litterman, 1992)` → `(Black & Litterman, 1992)`). 서술형은 `and` 유지.
   - (b) **참고문헌 권 번호 이탤릭** (`*Journal*, 48(5)` → `*Journal, 48*(5)`).
   - (c) **저널명 타이틀케이스** (`nature`→`Nature`, `Journal of financial economics`→`… Financial Economics`).
3. **references.bib 보완** (팀 조치; 초안 제공 가능):
   - **누락 7키**(BibTeX 추가 필요): `barua2023using`, `cochrane2005`, `cont2001`, `demiguel2009optimal`, `hamilton1989new`, `lee2025llm`, `timmermann2006forecast`.
   - **키 불일치**: 본문 `su2026objective` ↔ bib `su2026` (본문을 su2026로 바꾸거나 bib에 별칭).
4. **Phase 5/7 — 정리**:
   - 캡션 위/아래 배치 최종 검증(`<표 N>` 위, `<그림 N>` 아래).
   - **참고문헌 제목이 "6."로 자동번호** → 무번호 처리.
   - **부록 제목 번호가 본문 참조("부록 A~E")와 불일치**(스타일이 6,7…) → 부록 번호 체계 정합.
   - 본문 문단 스타일(pandoc Compact/BodyText/FirstParagraph) → '표준' 정합(여백·들여쓰기 일관성).
5. **Phase 8/9 — 쪽수 측정·최종 QA**: PDF 변환 후 수식·표 음영/병합·그림 캡션 위치·여백 육안 검수, 쪽수 보고(현재 59쪽).

## 6. 알려진 이슈(사소, 점검 목록)

- 수식 속 `\text{}` 한글이 일부 케이스식(예: `p_i^{mcap}` 분기 조건)에서 샌드박스 PDF상 공백으로 보임(폰트 의존; 워드 확인 필요).
- 첫 페이지 `국문초록` 라벨 등 일부 한글이 샌드박스 렌더에서 흐릿(워드에선 정상 예상).
- 본문에 stray `X` 등 사소한 흔적(원본 점검 필요).
- 타 저자 섹션은 **내용 무수정**(서식 변환만). 분량 축약 등은 팀/소유자 승인 필요.

## 7. 별개 태스크 (논문 유사연구 조사) — 폐기

- 2026-06-04 사용자 지시로 **트랙 전체 폐기**(태스크 #8·#11~#15 삭제). 완료분 기록만 유지: #10 선물연구(JDQS) — BL 방법 사용 0편 확인.
