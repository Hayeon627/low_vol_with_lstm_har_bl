"""Modify cell [1] in 99_main_analysis.ipynb: RMSE/Spearman panel-level → monthly aggregate.

- _fc_metrics 함수만 수정: 월별 cross-section RMSE/Spearman 계산 → 평균
- Hit Rate (_hit_rate_split) 는 이미 monthly aggregate 라 그대로
- 다른 부분 (데이터 로드, 표 출력, 스타일) 전부 유지
"""
from __future__ import annotations

import json
from pathlib import Path

NB_PATH = Path(r"C:\Users\서윤범\Desktop\temp\finance_project\final_pt\99_main_analysis.ipynb")

OLD_FC_METRICS = '''def _fc_metrics(df):
    rmse_l = float(np.sqrt(((df['y_pred_lstm'] - df['y_true'])**2).mean()))
    rmse_a = float(np.sqrt(((df['y_pred_ann']  - df['y_true'])**2).mean()))
    sp_l   = float(spearmanr(df['y_pred_lstm'], df['y_true']).statistic)
    sp_a   = float(spearmanr(df['y_pred_ann'],  df['y_true']).statistic)
    hit_lo_l, hit_hi_l = _hit_rate_split(df, 'y_pred_lstm')
    hit_lo_a, hit_hi_a = _hit_rate_split(df, 'y_pred_ann')
    return dict(rmse_l=rmse_l, rmse_a=rmse_a,
                sp_l=sp_l, sp_a=sp_a,
                hit_lo_l=hit_lo_l, hit_lo_a=hit_lo_a,
                hit_hi_l=hit_hi_l, hit_hi_a=hit_hi_a,
                n_mo=df['date'].nunique(), n_obs=len(df))'''

NEW_FC_METRICS = '''def _fc_metrics(df):
    """Monthly aggregate: 각 월별 cross-section 에서 RMSE/Spearman 계산 → 평균.

    Hit-Low/High 는 _hit_rate_split 에서 이미 monthly aggregate 로 처리됨.
    BL 의 사용 시나리오 (매월 cross-section 단위 입력) 와 정합.
    """
    rmse_l_list, rmse_a_list, sp_l_list, sp_a_list = [], [], [], []
    for dt, g in df.groupby('date'):
        if len(g) < 20: continue
        rmse_l_list.append(np.sqrt(((g['y_pred_lstm'] - g['y_true']) ** 2).mean()))
        rmse_a_list.append(np.sqrt(((g['y_pred_ann']  - g['y_true']) ** 2).mean()))
        sp_l_list  .append(spearmanr(g['y_pred_lstm'], g['y_true']).statistic)
        sp_a_list  .append(spearmanr(g['y_pred_ann'],  g['y_true']).statistic)
    rmse_l = float(np.mean(rmse_l_list)) if rmse_l_list else np.nan
    rmse_a = float(np.mean(rmse_a_list)) if rmse_a_list else np.nan
    sp_l   = float(np.mean(sp_l_list))   if sp_l_list   else np.nan
    sp_a   = float(np.mean(sp_a_list))   if sp_a_list   else np.nan
    hit_lo_l, hit_hi_l = _hit_rate_split(df, 'y_pred_lstm')
    hit_lo_a, hit_hi_a = _hit_rate_split(df, 'y_pred_ann')
    return dict(rmse_l=rmse_l, rmse_a=rmse_a,
                sp_l=sp_l, sp_a=sp_a,
                hit_lo_l=hit_lo_l, hit_lo_a=hit_lo_a,
                hit_hi_l=hit_hi_l, hit_hi_a=hit_hi_a,
                n_mo=df['date'].nunique(), n_obs=len(df))'''

OLD_HEADER = "print('LSTM vs ANN σ 예측 성능 (log-daily-std 단위)')"
NEW_HEADER = "print('LSTM vs ANN σ 예측 성능 (log-daily-std, Monthly aggregate)')"


def main() -> None:
    nb = json.loads(NB_PATH.read_text(encoding='utf-8'))
    cell = nb['cells'][3]
    assert cell['cell_type'] == 'code'
    src = ''.join(cell['source'])

    if OLD_FC_METRICS not in src:
        print('ERROR: OLD_FC_METRICS pattern not found in cell [3]')
        # diagnostic: print first 60 lines
        for i, ln in enumerate(src.splitlines(), 1):
            if 'def _fc_metrics' in ln or 'rmse_l' in ln:
                print(f'  line {i}: {ln!r}')
        return

    src = src.replace(OLD_FC_METRICS, NEW_FC_METRICS)
    if OLD_HEADER in src:
        src = src.replace(OLD_HEADER, NEW_HEADER)
    else:
        print('WARN: header line not found, only _fc_metrics replaced')

    cell['source'] = src.splitlines(keepends=True)
    cell['outputs'] = []
    cell['execution_count'] = None
    NB_PATH.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding='utf-8')
    print('OK — cell [1] _fc_metrics modified to monthly aggregate.')


if __name__ == '__main__':
    main()
