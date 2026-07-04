"""셀 [1+]: 컬럼 순서 Ens. 먼저 오도록 변경.

기존: LSTM | HAR | Ens. | ANN
변경: Ens. | LSTM | HAR | ANN

- 콘솔 표 pivot reindex 변경
- TSV 헤더 + 셀 iteration 순서 변경
"""
from __future__ import annotations

import json
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

NB_PATH = Path(r"C:\Users\서윤범\Desktop\temp\finance_project\final_pt\99_main_analysis.ipynb")


def main() -> None:
    nb = json.loads(NB_PATH.read_text(encoding='utf-8'))
    cell = nb['cells'][5]
    assert cell['cell_type'] == 'code'
    src = ''.join(cell['source'])

    replacements = [
        # 콘솔 표 pivot 컬럼 순서
        ("tab = tab.reindex(columns=['lstm','har','ensemble','ann'])\n    tab.columns = ['LSTM','HAR','Ens.','ANN']",
         "tab = tab.reindex(columns=['ensemble','lstm','har','ann'])\n    tab.columns = ['Ens.','LSTM','HAR','ANN']"),
        # TSV 헤더
        ("print('Metric\\\\tPeriod\\\\tLSTM\\\\tHAR\\\\tEns.\\\\tANN')",
         "print('Metric\\\\tPeriod\\\\tEns.\\\\tLSTM\\\\tHAR\\\\tANN')"),
        # TSV 셀 iteration
        ("cells = [tab.get((lbl, m), '--') for m in ['lstm','har','ensemble','ann']]",
         "cells = [tab.get((lbl, m), '--') for m in ['ensemble','lstm','har','ann']]"),
    ]

    for old, new in replacements:
        if old not in src:
            print(f'WARN: pattern not found:\n  {old[:80]}...')
            continue
        src = src.replace(old, new)
        print(f'OK: replaced {old[:60]}...')

    cell['source'] = src.splitlines(keepends=True)
    cell['outputs'] = []
    cell['execution_count'] = None
    NB_PATH.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding='utf-8')
    print('\n셀 [1+] 컬럼 순서 → Ens. | LSTM | HAR | ANN 으로 변경 완료.')


if __name__ == '__main__':
    main()
