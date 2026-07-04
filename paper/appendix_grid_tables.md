# Appendix: P 행렬 $\times$ 모든 슬롯 grid — 전체 45 슬롯 raw 결과 (6개 표)

> **출처**: `final_pt/99_main_analysis.ipynb` [3] P 행렬 grid 셀의 styled DataFrame 출력 원본.
> 
> **구성**: 표 1개 = 45 슬롯 ($p_w \times \text{prior} \times q$ = $3 \times 3 \times 5$) × 15 컬럼 (5 기간 × {L, A, Δ}). 총 6개 = omega ∈ {err, he} × metric ∈ {Sharpe, Sortino, MDD}.
> 
> **형식**: 본문 §4.3 표 (`tab:p_matrix_avg`) 컬럼 컨벤션 + 45행 MultiIndex(p_w/prior/q) + 노트북 styled output 색상 규칙.
> 
> **색상**: Δ 셀만 posgreen!50(+) / negred!50(−) 강조. $|\Delta| < 0.001$ ($|\Delta_{\text{MDD}}| < 0.05\%$)인 경우 색상 미적용.
> 
> **레이아웃**: $45 \times 18$ 컬럼 표이므로 \texttt{\textbackslash scriptsize} + \texttt{\textbackslash resizebox\{\textbackslash textwidth\}\{!\}\{...\}}로 portrait에 압축. 페이지 폭을 넘으면 paper3.md 프리앰블에 `\usepackage{pdflscape}` 추가 후 표 전체를 `\begin{landscape}` 으로 감싸 가로 회전.

## Sharpe — $\omega=$err

```latex
% NOTE: 표가 페이지 폭을 넘으면 paper3.md 프리앰블에 \usepackage{pdflscape}를 추가하고
%       \begin{landscape} ... \end{landscape}로 표 전체를 감싸 가로 회전하시기 바랍니다.
\begin{table}[!htbp]
\centering
\caption{전체 45 슬롯 Sharpe 비율 결과 ($\Omega=$err 고정). $p_w \times \text{prior} \times q$ = $3 \times 3 \times 5$ = 45 슬롯 각각의 LSTM(L)·ANN(A) Sharpe 비율 및 차이 $\Delta = \mathrm{L} - \mathrm{A}$를 5개 구간(All, R1 회복, R2 확장, R3 위기, R4 AI 랠리)에 대해 보고한다.}
\label{tab:app_grid_sharpe_err}
\setlength{\tabcolsep}{2pt}
\renewcommand{\arraystretch}{1.05}
\scriptsize
\resizebox{\textwidth}{!}{%
\begin{tabular}{lll ccc ccc ccc ccc ccc}
\toprule
 & & & \multicolumn{3}{c}{All} & \multicolumn{3}{c}{R1} & \multicolumn{3}{c}{R2} & \multicolumn{3}{c}{R3} & \multicolumn{3}{c}{R4} \\
\cmidrule(lr){4-6} \cmidrule(lr){7-9} \cmidrule(lr){10-12} \cmidrule(lr){13-15} \cmidrule(lr){16-18}
$p_w$ & prior & $q$ & L & A & $\Delta$ & L & A & $\Delta$ & L & A & $\Delta$ & L & A & $\Delta$ & L & A & $\Delta$ \\
\midrule
mcap & mcap & lam & $0.913$ & $0.952$ & \cellcolor{negred!50}$-0.038$ & $0.821$ & $1.041$ & \cellcolor{negred!50}$-0.220$ & $0.953$ & $1.213$ & \cellcolor{negred!50}$-0.260$ & $0.991$ & $0.638$ & \cellcolor{posgreen!50}$+0.353$ & $0.864$ & $0.833$ & \cellcolor{posgreen!50}$+0.030$ \\
 &  & raw & $0.976$ & $0.988$ & \cellcolor{negred!50}$-0.012$ & $0.818$ & $1.044$ & \cellcolor{negred!50}$-0.226$ & $1.115$ & $1.332$ & \cellcolor{negred!50}$-0.217$ & $0.999$ & $0.643$ & \cellcolor{posgreen!50}$+0.357$ & $0.864$ & $0.833$ & \cellcolor{posgreen!50}$+0.030$ \\
 &  & inv & $0.995$ & $0.982$ & \cellcolor{posgreen!50}$+0.014$ & $1.061$ & $1.244$ & \cellcolor{negred!50}$-0.183$ & $1.100$ & $1.084$ & \cellcolor{posgreen!50}$+0.016$ & $0.894$ & $0.738$ & \cellcolor{posgreen!50}$+0.156$ & $0.915$ & $0.963$ & \cellcolor{negred!50}$-0.048$ \\
 &  & vsp & $0.949$ & $0.948$ & $+0.000$ & $0.894$ & $1.105$ & \cellcolor{negred!50}$-0.211$ & $1.030$ & $1.067$ & \cellcolor{negred!50}$-0.037$ & $0.943$ & $0.720$ & \cellcolor{posgreen!50}$+0.223$ & $0.891$ & $0.958$ & \cellcolor{negred!50}$-0.067$ \\
 &  & fpm & $0.946$ & $0.945$ & $+0.000$ & $0.738$ & $1.059$ & \cellcolor{negred!50}$-0.321$ & $1.287$ & $1.076$ & \cellcolor{posgreen!50}$+0.212$ & $0.702$ & $0.850$ & \cellcolor{negred!50}$-0.148$ & $0.940$ & $0.712$ & \cellcolor{posgreen!50}$+0.228$ \\
\cmidrule(lr){2-18}
 & eq & lam & $0.895$ & $0.947$ & \cellcolor{negred!50}$-0.052$ & $0.979$ & $1.168$ & \cellcolor{negred!50}$-0.189$ & $0.997$ & $1.245$ & \cellcolor{negred!50}$-0.248$ & $0.956$ & $0.711$ & \cellcolor{posgreen!50}$+0.244$ & $0.505$ & $0.518$ & \cellcolor{negred!50}$-0.014$ \\
 &  & raw & $0.961$ & $0.984$ & \cellcolor{negred!50}$-0.023$ & $0.988$ & $1.163$ & \cellcolor{negred!50}$-0.176$ & $1.175$ & $1.382$ & \cellcolor{negred!50}$-0.207$ & $0.965$ & $0.717$ & \cellcolor{posgreen!50}$+0.248$ & $0.505$ & $0.518$ & \cellcolor{negred!50}$-0.014$ \\
 &  & inv & $0.905$ & $0.940$ & \cellcolor{negred!50}$-0.035$ & $1.164$ & $1.381$ & \cellcolor{negred!50}$-0.217$ & $1.075$ & $1.072$ & \cellcolor{posgreen!50}$+0.003$ & $0.823$ & $0.756$ & \cellcolor{posgreen!50}$+0.066$ & $0.455$ & $0.551$ & \cellcolor{negred!50}$-0.096$ \\
 &  & vsp & $0.888$ & $0.927$ & \cellcolor{negred!50}$-0.038$ & $1.042$ & $1.226$ & \cellcolor{negred!50}$-0.184$ & $1.018$ & $1.077$ & \cellcolor{negred!50}$-0.059$ & $0.905$ & $0.780$ & \cellcolor{posgreen!50}$+0.125$ & $0.437$ & $0.538$ & \cellcolor{negred!50}$-0.101$ \\
 &  & fpm & $0.894$ & $0.889$ & \cellcolor{posgreen!50}$+0.006$ & $0.919$ & $1.182$ & \cellcolor{negred!50}$-0.262$ & $1.276$ & $1.007$ & \cellcolor{posgreen!50}$+0.269$ & $0.673$ & $0.862$ & \cellcolor{negred!50}$-0.189$ & $0.623$ & $0.420$ & \cellcolor{posgreen!50}$+0.202$ \\
\cmidrule(lr){2-18}
 & rp & lam & $0.905$ & $0.946$ & \cellcolor{negred!50}$-0.041$ & $1.106$ & $1.295$ & \cellcolor{negred!50}$-0.189$ & $0.977$ & $1.229$ & \cellcolor{negred!50}$-0.252$ & $0.928$ & $0.653$ & \cellcolor{posgreen!50}$+0.276$ & $0.502$ & $0.478$ & \cellcolor{posgreen!50}$+0.024$ \\
 &  & raw & $0.966$ & $0.983$ & \cellcolor{negred!50}$-0.017$ & $1.110$ & $1.296$ & \cellcolor{negred!50}$-0.185$ & $1.133$ & $1.353$ & \cellcolor{negred!50}$-0.220$ & $0.942$ & $0.659$ & \cellcolor{posgreen!50}$+0.283$ & $0.502$ & $0.478$ & \cellcolor{posgreen!50}$+0.024$ \\
 &  & inv & $0.916$ & $0.947$ & \cellcolor{negred!50}$-0.031$ & $1.274$ & $1.478$ & \cellcolor{negred!50}$-0.204$ & $1.090$ & $1.098$ & \cellcolor{negred!50}$-0.008$ & $0.793$ & $0.720$ & \cellcolor{posgreen!50}$+0.073$ & $0.431$ & $0.512$ & \cellcolor{negred!50}$-0.081$ \\
 &  & vsp & $0.909$ & $0.935$ & \cellcolor{negred!50}$-0.027$ & $1.167$ & $1.346$ & \cellcolor{negred!50}$-0.179$ & $1.039$ & $1.086$ & \cellcolor{negred!50}$-0.046$ & $0.881$ & $0.742$ & \cellcolor{posgreen!50}$+0.138$ & $0.409$ & $0.506$ & \cellcolor{negred!50}$-0.097$ \\
 &  & fpm & $0.918$ & $0.904$ & \cellcolor{posgreen!50}$+0.014$ & $1.032$ & $1.299$ & \cellcolor{negred!50}$-0.267$ & $1.298$ & $1.038$ & \cellcolor{posgreen!50}$+0.260$ & $0.638$ & $0.829$ & \cellcolor{negred!50}$-0.191$ & $0.651$ & $0.394$ & \cellcolor{posgreen!50}$+0.257$ \\
\midrule
eq & mcap & lam & $1.067$ & $0.973$ & \cellcolor{posgreen!50}$+0.094$ & $1.076$ & $1.120$ & \cellcolor{negred!50}$-0.045$ & $1.320$ & $1.335$ & \cellcolor{negred!50}$-0.016$ & $0.956$ & $0.583$ & \cellcolor{posgreen!50}$+0.373$ & $0.638$ & $0.578$ & \cellcolor{posgreen!50}$+0.059$ \\
 &  & raw & $1.060$ & $0.976$ & \cellcolor{posgreen!50}$+0.084$ & $1.085$ & $1.125$ & \cellcolor{negred!50}$-0.040$ & $1.311$ & $1.345$ & \cellcolor{negred!50}$-0.034$ & $0.953$ & $0.583$ & \cellcolor{posgreen!50}$+0.370$ & $0.638$ & $0.578$ & \cellcolor{posgreen!50}$+0.059$ \\
 &  & inv & $1.047$ & $0.988$ & \cellcolor{posgreen!50}$+0.059$ & $1.240$ & $1.270$ & \cellcolor{negred!50}$-0.030$ & $1.195$ & $1.205$ & \cellcolor{negred!50}$-0.010$ & $0.878$ & $0.681$ & \cellcolor{posgreen!50}$+0.197$ & $0.816$ & $0.720$ & \cellcolor{posgreen!50}$+0.097$ \\
 &  & vsp & $1.040$ & $0.963$ & \cellcolor{posgreen!50}$+0.076$ & $1.131$ & $1.158$ & \cellcolor{negred!50}$-0.028$ & $1.205$ & $1.245$ & \cellcolor{negred!50}$-0.040$ & $0.914$ & $0.624$ & \cellcolor{posgreen!50}$+0.291$ & $0.772$ & $0.688$ & \cellcolor{posgreen!50}$+0.084$ \\
 &  & fpm & $1.099$ & $1.049$ & \cellcolor{posgreen!50}$+0.050$ & $0.872$ & $1.024$ & \cellcolor{negred!50}$-0.152$ & $1.421$ & $1.408$ & \cellcolor{posgreen!50}$+0.013$ & $0.888$ & $0.705$ & \cellcolor{posgreen!50}$+0.183$ & $1.066$ & $0.868$ & \cellcolor{posgreen!50}$+0.198$ \\
\cmidrule(lr){2-18}
 & eq & lam & $1.022$ & $0.935$ & \cellcolor{posgreen!50}$+0.086$ & $1.163$ & $1.203$ & \cellcolor{negred!50}$-0.040$ & $1.339$ & $1.350$ & \cellcolor{negred!50}$-0.011$ & $0.955$ & $0.621$ & \cellcolor{posgreen!50}$+0.334$ & $0.277$ & $0.227$ & \cellcolor{posgreen!50}$+0.050$ \\
 &  & raw & $1.016$ & $0.932$ & \cellcolor{posgreen!50}$+0.084$ & $1.164$ & $1.210$ & \cellcolor{negred!50}$-0.046$ & $1.339$ & $1.339$ & $-0.000$ & $0.953$ & $0.622$ & \cellcolor{posgreen!50}$+0.331$ & $0.277$ & $0.227$ & \cellcolor{posgreen!50}$+0.050$ \\
 &  & inv & $1.008$ & $0.947$ & \cellcolor{posgreen!50}$+0.061$ & $1.329$ & $1.337$ & \cellcolor{negred!50}$-0.007$ & $1.196$ & $1.194$ & \cellcolor{posgreen!50}$+0.002$ & $0.941$ & $0.748$ & \cellcolor{posgreen!50}$+0.193$ & $0.397$ & $0.349$ & \cellcolor{posgreen!50}$+0.048$ \\
 &  & vsp & $1.012$ & $0.956$ & \cellcolor{posgreen!50}$+0.057$ & $1.221$ & $1.247$ & \cellcolor{negred!50}$-0.026$ & $1.239$ & $1.285$ & \cellcolor{negred!50}$-0.046$ & $0.965$ & $0.723$ & \cellcolor{posgreen!50}$+0.243$ & $0.354$ & $0.317$ & \cellcolor{posgreen!50}$+0.038$ \\
 &  & fpm & $1.068$ & $1.031$ & \cellcolor{posgreen!50}$+0.037$ & $1.020$ & $1.123$ & \cellcolor{negred!50}$-0.103$ & $1.436$ & $1.461$ & \cellcolor{negred!50}$-0.025$ & $0.956$ & $0.802$ & \cellcolor{posgreen!50}$+0.154$ & $0.522$ & $0.405$ & \cellcolor{posgreen!50}$+0.117$ \\
\cmidrule(lr){2-18}
 & rp & lam & $1.013$ & $0.923$ & \cellcolor{posgreen!50}$+0.090$ & $1.268$ & $1.307$ & \cellcolor{negred!50}$-0.039$ & $1.317$ & $1.312$ & \cellcolor{posgreen!50}$+0.004$ & $0.891$ & $0.580$ & \cellcolor{posgreen!50}$+0.311$ & $0.230$ & $0.164$ & \cellcolor{posgreen!50}$+0.066$ \\
 &  & raw & $1.008$ & $0.922$ & \cellcolor{posgreen!50}$+0.085$ & $1.272$ & $1.313$ & \cellcolor{negred!50}$-0.041$ & $1.314$ & $1.307$ & \cellcolor{posgreen!50}$+0.007$ & $0.888$ & $0.581$ & \cellcolor{posgreen!50}$+0.307$ & $0.230$ & $0.164$ & \cellcolor{posgreen!50}$+0.066$ \\
 &  & inv & $1.012$ & $0.948$ & \cellcolor{posgreen!50}$+0.064$ & $1.462$ & $1.428$ & \cellcolor{posgreen!50}$+0.034$ & $1.218$ & $1.199$ & \cellcolor{posgreen!50}$+0.019$ & $0.884$ & $0.723$ & \cellcolor{posgreen!50}$+0.160$ & $0.350$ & $0.296$ & \cellcolor{posgreen!50}$+0.053$ \\
 &  & vsp & $1.014$ & $0.957$ & \cellcolor{posgreen!50}$+0.056$ & $1.339$ & $1.362$ & \cellcolor{negred!50}$-0.023$ & $1.238$ & $1.274$ & \cellcolor{negred!50}$-0.036$ & $0.908$ & $0.688$ & \cellcolor{posgreen!50}$+0.220$ & $0.326$ & $0.274$ & \cellcolor{posgreen!50}$+0.052$ \\
 &  & fpm & $1.081$ & $1.043$ & \cellcolor{posgreen!50}$+0.038$ & $1.116$ & $1.225$ & \cellcolor{negred!50}$-0.109$ & $1.453$ & $1.454$ & $-0.000$ & $0.908$ & $0.776$ & \cellcolor{posgreen!50}$+0.132$ & $0.484$ & $0.374$ & \cellcolor{posgreen!50}$+0.110$ \\
\midrule
rp & mcap & lam & $1.042$ & $0.940$ & \cellcolor{posgreen!50}$+0.101$ & $0.977$ & $0.956$ & \cellcolor{posgreen!50}$+0.021$ & $1.275$ & $1.285$ & \cellcolor{negred!50}$-0.010$ & $0.953$ & $0.620$ & \cellcolor{posgreen!50}$+0.333$ & $0.709$ & $0.647$ & \cellcolor{posgreen!50}$+0.061$ \\
 &  & raw & $1.036$ & $0.956$ & \cellcolor{posgreen!50}$+0.080$ & $0.986$ & $0.955$ & \cellcolor{posgreen!50}$+0.031$ & $1.270$ & $1.330$ & \cellcolor{negred!50}$-0.060$ & $0.951$ & $0.621$ & \cellcolor{posgreen!50}$+0.329$ & $0.709$ & $0.647$ & \cellcolor{posgreen!50}$+0.061$ \\
 &  & inv & $1.020$ & $0.922$ & \cellcolor{posgreen!50}$+0.098$ & $1.137$ & $1.001$ & \cellcolor{posgreen!50}$+0.136$ & $1.151$ & $1.129$ & \cellcolor{posgreen!50}$+0.023$ & $0.852$ & $0.679$ & \cellcolor{posgreen!50}$+0.172$ & $0.926$ & $0.808$ & \cellcolor{posgreen!50}$+0.117$ \\
 &  & vsp & $1.009$ & $0.906$ & \cellcolor{posgreen!50}$+0.103$ & $1.055$ & $0.977$ & \cellcolor{posgreen!50}$+0.078$ & $1.150$ & $1.151$ & \cellcolor{negred!50}$-0.001$ & $0.884$ & $0.631$ & \cellcolor{posgreen!50}$+0.254$ & $0.871$ & $0.769$ & \cellcolor{posgreen!50}$+0.102$ \\
 &  & fpm & $1.054$ & $0.970$ & \cellcolor{posgreen!50}$+0.084$ & $0.806$ & $0.809$ & \cellcolor{negred!50}$-0.003$ & $1.344$ & $1.311$ & \cellcolor{posgreen!50}$+0.033$ & $0.870$ & $0.714$ & \cellcolor{posgreen!50}$+0.155$ & $1.102$ & $0.900$ & \cellcolor{posgreen!50}$+0.202$ \\
\cmidrule(lr){2-18}
 & eq & lam & $1.003$ & $0.908$ & \cellcolor{posgreen!50}$+0.095$ & $1.098$ & $1.038$ & \cellcolor{posgreen!50}$+0.061$ & $1.289$ & $1.302$ & \cellcolor{negred!50}$-0.013$ & $0.941$ & $0.654$ & \cellcolor{posgreen!50}$+0.287$ & $0.363$ & $0.297$ & \cellcolor{posgreen!50}$+0.066$ \\
 &  & raw & $1.005$ & $0.909$ & \cellcolor{posgreen!50}$+0.096$ & $1.114$ & $1.042$ & \cellcolor{posgreen!50}$+0.072$ & $1.306$ & $1.307$ & \cellcolor{negred!50}$-0.001$ & $0.938$ & $0.654$ & \cellcolor{posgreen!50}$+0.284$ & $0.363$ & $0.297$ & \cellcolor{posgreen!50}$+0.066$ \\
 &  & inv & $0.962$ & $0.882$ & \cellcolor{posgreen!50}$+0.080$ & $1.223$ & $1.079$ & \cellcolor{posgreen!50}$+0.144$ & $1.133$ & $1.104$ & \cellcolor{posgreen!50}$+0.029$ & $0.890$ & $0.740$ & \cellcolor{posgreen!50}$+0.149$ & $0.447$ & $0.416$ & \cellcolor{posgreen!50}$+0.030$ \\
 &  & vsp & $0.971$ & $0.887$ & \cellcolor{posgreen!50}$+0.084$ & $1.140$ & $1.061$ & \cellcolor{posgreen!50}$+0.079$ & $1.181$ & $1.155$ & \cellcolor{posgreen!50}$+0.026$ & $0.911$ & $0.717$ & \cellcolor{posgreen!50}$+0.194$ & $0.415$ & $0.387$ & \cellcolor{posgreen!50}$+0.028$ \\
 &  & fpm & $1.020$ & $0.953$ & \cellcolor{posgreen!50}$+0.067$ & $0.997$ & $0.937$ & \cellcolor{posgreen!50}$+0.059$ & $1.339$ & $1.331$ & \cellcolor{posgreen!50}$+0.009$ & $0.910$ & $0.804$ & \cellcolor{posgreen!50}$+0.106$ & $0.535$ & $0.434$ & \cellcolor{posgreen!50}$+0.101$ \\
\cmidrule(lr){2-18}
 & rp & lam & $1.006$ & $0.901$ & \cellcolor{posgreen!50}$+0.105$ & $1.221$ & $1.141$ & \cellcolor{posgreen!50}$+0.080$ & $1.283$ & $1.265$ & \cellcolor{posgreen!50}$+0.018$ & $0.893$ & $0.615$ & \cellcolor{posgreen!50}$+0.278$ & $0.309$ & $0.243$ & \cellcolor{posgreen!50}$+0.066$ \\
 &  & raw & $1.003$ & $0.908$ & \cellcolor{posgreen!50}$+0.095$ & $1.237$ & $1.146$ & \cellcolor{posgreen!50}$+0.092$ & $1.283$ & $1.283$ & $-0.000$ & $0.891$ & $0.618$ & \cellcolor{posgreen!50}$+0.273$ & $0.309$ & $0.243$ & \cellcolor{posgreen!50}$+0.066$ \\
 &  & inv & $0.968$ & $0.896$ & \cellcolor{posgreen!50}$+0.072$ & $1.352$ & $1.175$ & \cellcolor{posgreen!50}$+0.177$ & $1.162$ & $1.124$ & \cellcolor{posgreen!50}$+0.037$ & $0.828$ & $0.727$ & \cellcolor{posgreen!50}$+0.101$ & $0.406$ & $0.365$ & \cellcolor{posgreen!50}$+0.042$ \\
 &  & vsp & $0.976$ & $0.893$ & \cellcolor{posgreen!50}$+0.083$ & $1.269$ & $1.150$ & \cellcolor{posgreen!50}$+0.119$ & $1.189$ & $1.157$ & \cellcolor{posgreen!50}$+0.032$ & $0.858$ & $0.692$ & \cellcolor{posgreen!50}$+0.166$ & $0.371$ & $0.340$ & \cellcolor{posgreen!50}$+0.031$ \\
 &  & fpm & $1.041$ & $0.971$ & \cellcolor{posgreen!50}$+0.070$ & $1.103$ & $1.038$ & \cellcolor{posgreen!50}$+0.065$ & $1.369$ & $1.338$ & \cellcolor{posgreen!50}$+0.031$ & $0.872$ & $0.781$ & \cellcolor{posgreen!50}$+0.091$ & $0.491$ & $0.390$ & \cellcolor{posgreen!50}$+0.100$ \\
\bottomrule
\end{tabular}}
\end{table}
```

## Sortino — $\omega=$err

```latex
% NOTE: 표가 페이지 폭을 넘으면 paper3.md 프리앰블에 \usepackage{pdflscape}를 추가하고
%       \begin{landscape} ... \end{landscape}로 표 전체를 감싸 가로 회전하시기 바랍니다.
\begin{table}[!htbp]
\centering
\caption{전체 45 슬롯 Sortino 비율 결과 ($\Omega=$err 고정). $p_w \times \text{prior} \times q$ = $3 \times 3 \times 5$ = 45 슬롯 각각의 LSTM(L)·ANN(A) Sortino 비율 및 차이 $\Delta = \mathrm{L} - \mathrm{A}$를 5개 구간(All, R1 회복, R2 확장, R3 위기, R4 AI 랠리)에 대해 보고한다.}
\label{tab:app_grid_sortino_err}
\setlength{\tabcolsep}{2pt}
\renewcommand{\arraystretch}{1.05}
\scriptsize
\resizebox{\textwidth}{!}{%
\begin{tabular}{lll ccc ccc ccc ccc ccc}
\toprule
 & & & \multicolumn{3}{c}{All} & \multicolumn{3}{c}{R1} & \multicolumn{3}{c}{R2} & \multicolumn{3}{c}{R3} & \multicolumn{3}{c}{R4} \\
\cmidrule(lr){4-6} \cmidrule(lr){7-9} \cmidrule(lr){10-12} \cmidrule(lr){13-15} \cmidrule(lr){16-18}
$p_w$ & prior & $q$ & L & A & $\Delta$ & L & A & $\Delta$ & L & A & $\Delta$ & L & A & $\Delta$ & L & A & $\Delta$ \\
\midrule
mcap & mcap & lam & $1.464$ & $1.473$ & \cellcolor{negred!50}$-0.009$ & $1.295$ & $1.537$ & \cellcolor{negred!50}$-0.243$ & $1.311$ & $1.663$ & \cellcolor{negred!50}$-0.352$ & $2.261$ & $1.301$ & \cellcolor{posgreen!50}$+0.960$ & $1.198$ & $1.085$ & \cellcolor{posgreen!50}$+0.112$ \\
 &  & raw & $1.552$ & $1.530$ & \cellcolor{posgreen!50}$+0.021$ & $1.293$ & $1.544$ & \cellcolor{negred!50}$-0.251$ & $1.488$ & $1.923$ & \cellcolor{negred!50}$-0.435$ & $2.291$ & $1.315$ & \cellcolor{posgreen!50}$+0.976$ & $1.198$ & $1.085$ & \cellcolor{posgreen!50}$+0.112$ \\
 &  & inv & $1.395$ & $1.368$ & \cellcolor{posgreen!50}$+0.028$ & $1.447$ & $1.629$ & \cellcolor{negred!50}$-0.182$ & $1.200$ & $1.258$ & \cellcolor{negred!50}$-0.058$ & $1.980$ & $1.498$ & \cellcolor{posgreen!50}$+0.482$ & $1.425$ & $1.314$ & \cellcolor{posgreen!50}$+0.110$ \\
 &  & vsp & $1.403$ & $1.370$ & \cellcolor{posgreen!50}$+0.033$ & $1.345$ & $1.576$ & \cellcolor{negred!50}$-0.232$ & $1.209$ & $1.266$ & \cellcolor{negred!50}$-0.056$ & $2.139$ & $1.453$ & \cellcolor{posgreen!50}$+0.686$ & $1.314$ & $1.343$ & \cellcolor{negred!50}$-0.029$ \\
 &  & fpm & $1.320$ & $1.336$ & \cellcolor{negred!50}$-0.016$ & $1.190$ & $1.555$ & \cellcolor{negred!50}$-0.364$ & $1.481$ & $1.360$ & \cellcolor{posgreen!50}$+0.121$ & $1.174$ & $1.597$ & \cellcolor{negred!50}$-0.424$ & $1.513$ & $0.878$ & \cellcolor{posgreen!50}$+0.635$ \\
\cmidrule(lr){2-18}
 & eq & lam & $1.483$ & $1.526$ & \cellcolor{negred!50}$-0.043$ & $1.509$ & $1.731$ & \cellcolor{negred!50}$-0.222$ & $1.316$ & $1.699$ & \cellcolor{negred!50}$-0.382$ & $2.181$ & $1.532$ & \cellcolor{posgreen!50}$+0.649$ & $0.898$ & $0.888$ & \cellcolor{posgreen!50}$+0.011$ \\
 &  & raw & $1.594$ & $1.598$ & \cellcolor{negred!50}$-0.004$ & $1.528$ & $1.729$ & \cellcolor{negred!50}$-0.201$ & $1.547$ & $1.977$ & \cellcolor{negred!50}$-0.430$ & $2.221$ & $1.548$ & \cellcolor{posgreen!50}$+0.674$ & $0.898$ & $0.888$ & \cellcolor{posgreen!50}$+0.011$ \\
 &  & inv & $1.310$ & $1.356$ & \cellcolor{negred!50}$-0.046$ & $1.575$ & $1.796$ & \cellcolor{negred!50}$-0.221$ & $1.185$ & $1.238$ & \cellcolor{negred!50}$-0.053$ & $1.604$ & $1.475$ & \cellcolor{posgreen!50}$+0.129$ & $0.803$ & $0.929$ & \cellcolor{negred!50}$-0.125$ \\
 &  & vsp & $1.382$ & $1.410$ & \cellcolor{negred!50}$-0.028$ & $1.541$ & $1.752$ & \cellcolor{negred!50}$-0.210$ & $1.191$ & $1.290$ & \cellcolor{negred!50}$-0.099$ & $2.052$ & $1.637$ & \cellcolor{posgreen!50}$+0.415$ & $0.784$ & $0.926$ & \cellcolor{negred!50}$-0.141$ \\
 &  & fpm & $1.200$ & $1.271$ & \cellcolor{negred!50}$-0.071$ & $1.455$ & $1.755$ & \cellcolor{negred!50}$-0.300$ & $1.394$ & $1.300$ & \cellcolor{posgreen!50}$+0.094$ & $1.016$ & $1.548$ & \cellcolor{negred!50}$-0.532$ & $1.177$ & $0.522$ & \cellcolor{posgreen!50}$+0.655$ \\
\cmidrule(lr){2-18}
 & rp & lam & $1.499$ & $1.513$ & \cellcolor{negred!50}$-0.015$ & $1.679$ & $1.974$ & \cellcolor{negred!50}$-0.296$ & $1.325$ & $1.670$ & \cellcolor{negred!50}$-0.345$ & $2.108$ & $1.390$ & \cellcolor{posgreen!50}$+0.719$ & $0.877$ & $0.828$ & \cellcolor{posgreen!50}$+0.049$ \\
 &  & raw & $1.605$ & $1.585$ & \cellcolor{posgreen!50}$+0.020$ & $1.693$ & $1.972$ & \cellcolor{negred!50}$-0.279$ & $1.542$ & $1.907$ & \cellcolor{negred!50}$-0.365$ & $2.159$ & $1.406$ & \cellcolor{posgreen!50}$+0.753$ & $0.877$ & $0.828$ & \cellcolor{posgreen!50}$+0.049$ \\
 &  & inv & $1.318$ & $1.366$ & \cellcolor{negred!50}$-0.048$ & $1.677$ & $1.956$ & \cellcolor{negred!50}$-0.278$ & $1.245$ & $1.292$ & \cellcolor{negred!50}$-0.047$ & $1.533$ & $1.427$ & \cellcolor{posgreen!50}$+0.105$ & $0.740$ & $0.824$ & \cellcolor{negred!50}$-0.084$ \\
 &  & vsp & $1.418$ & $1.430$ & \cellcolor{negred!50}$-0.012$ & $1.688$ & $1.957$ & \cellcolor{negred!50}$-0.269$ & $1.265$ & $1.338$ & \cellcolor{negred!50}$-0.074$ & $2.007$ & $1.584$ & \cellcolor{posgreen!50}$+0.423$ & $0.737$ & $0.828$ & \cellcolor{negred!50}$-0.091$ \\
 &  & fpm & $1.233$ & $1.288$ & \cellcolor{negred!50}$-0.054$ & $1.595$ & $2.004$ & \cellcolor{negred!50}$-0.409$ & $1.455$ & $1.358$ & \cellcolor{posgreen!50}$+0.097$ & $0.970$ & $1.541$ & \cellcolor{negred!50}$-0.571$ & $1.251$ & $0.458$ & \cellcolor{posgreen!50}$+0.793$ \\
\midrule
eq & mcap & lam & $1.662$ & $1.523$ & \cellcolor{posgreen!50}$+0.139$ & $1.784$ & $1.765$ & \cellcolor{posgreen!50}$+0.019$ & $1.821$ & $1.974$ & \cellcolor{negred!50}$-0.153$ & $1.800$ & $1.127$ & \cellcolor{posgreen!50}$+0.673$ & $0.978$ & $0.872$ & \cellcolor{posgreen!50}$+0.106$ \\
 &  & raw & $1.696$ & $1.555$ & \cellcolor{posgreen!50}$+0.141$ & $1.800$ & $1.775$ & \cellcolor{posgreen!50}$+0.025$ & $1.947$ & $2.090$ & \cellcolor{negred!50}$-0.143$ & $1.795$ & $1.127$ & \cellcolor{posgreen!50}$+0.668$ & $0.978$ & $0.872$ & \cellcolor{posgreen!50}$+0.106$ \\
 &  & inv & $1.519$ & $1.367$ & \cellcolor{posgreen!50}$+0.152$ & $1.851$ & $1.774$ & \cellcolor{posgreen!50}$+0.077$ & $1.489$ & $1.431$ & \cellcolor{posgreen!50}$+0.057$ & $1.674$ & $1.183$ & \cellcolor{posgreen!50}$+0.491$ & $1.150$ & $1.034$ & \cellcolor{posgreen!50}$+0.116$ \\
 &  & vsp & $1.555$ & $1.378$ & \cellcolor{posgreen!50}$+0.177$ & $1.866$ & $1.716$ & \cellcolor{posgreen!50}$+0.150$ & $1.516$ & $1.534$ & \cellcolor{negred!50}$-0.019$ & $1.775$ & $1.110$ & \cellcolor{posgreen!50}$+0.665$ & $1.141$ & $1.022$ & \cellcolor{posgreen!50}$+0.119$ \\
 &  & fpm & $1.623$ & $1.548$ & \cellcolor{posgreen!50}$+0.075$ & $1.468$ & $1.653$ & \cellcolor{negred!50}$-0.185$ & $1.701$ & $1.721$ & \cellcolor{negred!50}$-0.020$ & $1.767$ & $1.307$ & \cellcolor{posgreen!50}$+0.460$ & $1.724$ & $1.642$ & \cellcolor{posgreen!50}$+0.082$ \\
\cmidrule(lr){2-18}
 & eq & lam & $1.715$ & $1.556$ & \cellcolor{posgreen!50}$+0.159$ & $2.088$ & $1.923$ & \cellcolor{posgreen!50}$+0.165$ & $1.844$ & $2.025$ & \cellcolor{negred!50}$-0.180$ & $1.961$ & $1.240$ & \cellcolor{posgreen!50}$+0.722$ & $0.529$ & $0.411$ & \cellcolor{posgreen!50}$+0.117$ \\
 &  & raw & $1.724$ & $1.567$ & \cellcolor{posgreen!50}$+0.157$ & $2.109$ & $1.939$ & \cellcolor{posgreen!50}$+0.170$ & $1.961$ & $2.082$ & \cellcolor{negred!50}$-0.121$ & $1.958$ & $1.241$ & \cellcolor{posgreen!50}$+0.717$ & $0.529$ & $0.411$ & \cellcolor{posgreen!50}$+0.117$ \\
 &  & inv & $1.539$ & $1.389$ & \cellcolor{posgreen!50}$+0.151$ & $2.035$ & $1.910$ & \cellcolor{posgreen!50}$+0.125$ & $1.508$ & $1.441$ & \cellcolor{posgreen!50}$+0.066$ & $1.737$ & $1.364$ & \cellcolor{posgreen!50}$+0.373$ & $0.730$ & $0.664$ & \cellcolor{posgreen!50}$+0.066$ \\
 &  & vsp & $1.623$ & $1.468$ & \cellcolor{posgreen!50}$+0.154$ & $2.041$ & $1.923$ & \cellcolor{posgreen!50}$+0.118$ & $1.575$ & $1.660$ & \cellcolor{negred!50}$-0.086$ & $2.041$ & $1.381$ & \cellcolor{posgreen!50}$+0.661$ & $0.665$ & $0.608$ & \cellcolor{posgreen!50}$+0.056$ \\
 &  & fpm & $1.680$ & $1.615$ & \cellcolor{posgreen!50}$+0.066$ & $1.749$ & $1.872$ & \cellcolor{negred!50}$-0.123$ & $1.738$ & $1.831$ & \cellcolor{negred!50}$-0.093$ & $2.009$ & $1.634$ & \cellcolor{posgreen!50}$+0.375$ & $0.952$ & $0.782$ & \cellcolor{posgreen!50}$+0.170$ \\
\cmidrule(lr){2-18}
 & rp & lam & $1.694$ & $1.572$ & \cellcolor{posgreen!50}$+0.122$ & $2.482$ & $2.213$ & \cellcolor{posgreen!50}$+0.268$ & $1.866$ & $2.029$ & \cellcolor{negred!50}$-0.164$ & $1.783$ & $1.164$ & \cellcolor{posgreen!50}$+0.618$ & $0.406$ & $0.292$ & \cellcolor{posgreen!50}$+0.114$ \\
 &  & raw & $1.710$ & $1.589$ & \cellcolor{posgreen!50}$+0.122$ & $2.500$ & $2.223$ & \cellcolor{posgreen!50}$+0.277$ & $1.973$ & $2.086$ & \cellcolor{negred!50}$-0.113$ & $1.779$ & $1.166$ & \cellcolor{posgreen!50}$+0.613$ & $0.406$ & $0.292$ & \cellcolor{posgreen!50}$+0.114$ \\
 &  & inv & $1.537$ & $1.393$ & \cellcolor{posgreen!50}$+0.145$ & $2.365$ & $2.067$ & \cellcolor{posgreen!50}$+0.299$ & $1.538$ & $1.457$ & \cellcolor{posgreen!50}$+0.081$ & $1.644$ & $1.349$ & \cellcolor{posgreen!50}$+0.295$ & $0.619$ & $0.536$ & \cellcolor{posgreen!50}$+0.083$ \\
 &  & vsp & $1.606$ & $1.485$ & \cellcolor{posgreen!50}$+0.121$ & $2.551$ & $2.151$ & \cellcolor{posgreen!50}$+0.399$ & $1.605$ & $1.668$ & \cellcolor{negred!50}$-0.063$ & $1.882$ & $1.348$ & \cellcolor{posgreen!50}$+0.535$ & $0.590$ & $0.476$ & \cellcolor{posgreen!50}$+0.114$ \\
 &  & fpm & $1.697$ & $1.671$ & \cellcolor{posgreen!50}$+0.026$ & $1.999$ & $2.228$ & \cellcolor{negred!50}$-0.229$ & $1.828$ & $1.856$ & \cellcolor{negred!50}$-0.028$ & $1.867$ & $1.615$ & \cellcolor{posgreen!50}$+0.252$ & $0.868$ & $0.685$ & \cellcolor{posgreen!50}$+0.183$ \\
\midrule
rp & mcap & lam & $1.644$ & $1.432$ & \cellcolor{posgreen!50}$+0.211$ & $1.672$ & $1.319$ & \cellcolor{posgreen!50}$+0.353$ & $1.746$ & $1.891$ & \cellcolor{negred!50}$-0.145$ & $1.794$ & $1.216$ & \cellcolor{posgreen!50}$+0.577$ & $1.099$ & $0.942$ & \cellcolor{posgreen!50}$+0.157$ \\
 &  & raw & $1.679$ & $1.481$ & \cellcolor{posgreen!50}$+0.198$ & $1.687$ & $1.321$ & \cellcolor{posgreen!50}$+0.366$ & $1.873$ & $2.070$ & \cellcolor{negred!50}$-0.197$ & $1.790$ & $1.218$ & \cellcolor{posgreen!50}$+0.573$ & $1.099$ & $0.942$ & \cellcolor{posgreen!50}$+0.157$ \\
 &  & inv & $1.476$ & $1.239$ & \cellcolor{posgreen!50}$+0.237$ & $1.906$ & $1.306$ & \cellcolor{posgreen!50}$+0.600$ & $1.377$ & $1.314$ & \cellcolor{posgreen!50}$+0.063$ & $1.629$ & $1.177$ & \cellcolor{posgreen!50}$+0.452$ & $1.312$ & $1.233$ & \cellcolor{posgreen!50}$+0.079$ \\
 &  & vsp & $1.540$ & $1.268$ & \cellcolor{posgreen!50}$+0.273$ & $1.818$ & $1.371$ & \cellcolor{posgreen!50}$+0.447$ & $1.441$ & $1.436$ & \cellcolor{posgreen!50}$+0.005$ & $1.771$ & $1.134$ & \cellcolor{posgreen!50}$+0.636$ & $1.320$ & $1.093$ & \cellcolor{posgreen!50}$+0.227$ \\
 &  & fpm & $1.586$ & $1.386$ & \cellcolor{posgreen!50}$+0.199$ & $1.438$ & $1.120$ & \cellcolor{posgreen!50}$+0.318$ & $1.643$ & $1.608$ & \cellcolor{posgreen!50}$+0.035$ & $1.749$ & $1.398$ & \cellcolor{posgreen!50}$+0.351$ & $1.779$ & $1.545$ & \cellcolor{posgreen!50}$+0.235$ \\
\cmidrule(lr){2-18}
 & eq & lam & $1.672$ & $1.465$ & \cellcolor{posgreen!50}$+0.207$ & $1.876$ & $1.538$ & \cellcolor{posgreen!50}$+0.338$ & $1.764$ & $1.935$ & \cellcolor{negred!50}$-0.171$ & $1.883$ & $1.324$ & \cellcolor{posgreen!50}$+0.560$ & $0.715$ & $0.536$ & \cellcolor{posgreen!50}$+0.179$ \\
 &  & raw & $1.692$ & $1.493$ & \cellcolor{posgreen!50}$+0.199$ & $1.895$ & $1.547$ & \cellcolor{posgreen!50}$+0.348$ & $1.894$ & $2.019$ & \cellcolor{negred!50}$-0.124$ & $1.881$ & $1.324$ & \cellcolor{posgreen!50}$+0.557$ & $0.715$ & $0.536$ & \cellcolor{posgreen!50}$+0.179$ \\
 &  & inv & $1.455$ & $1.272$ & \cellcolor{posgreen!50}$+0.183$ & $2.041$ & $1.494$ & \cellcolor{posgreen!50}$+0.547$ & $1.381$ & $1.330$ & \cellcolor{posgreen!50}$+0.051$ & $1.628$ & $1.359$ & \cellcolor{posgreen!50}$+0.269$ & $0.842$ & $0.805$ & \cellcolor{posgreen!50}$+0.036$ \\
 &  & vsp & $1.569$ & $1.348$ & \cellcolor{posgreen!50}$+0.220$ & $2.054$ & $1.546$ & \cellcolor{posgreen!50}$+0.509$ & $1.483$ & $1.472$ & \cellcolor{posgreen!50}$+0.012$ & $1.889$ & $1.414$ & \cellcolor{posgreen!50}$+0.475$ & $0.801$ & $0.750$ & \cellcolor{posgreen!50}$+0.052$ \\
 &  & fpm & $1.630$ & $1.445$ & \cellcolor{posgreen!50}$+0.185$ & $1.808$ & $1.317$ & \cellcolor{posgreen!50}$+0.491$ & $1.679$ & $1.679$ & $-0.000$ & $1.954$ & $1.635$ & \cellcolor{posgreen!50}$+0.319$ & $0.968$ & $0.800$ & \cellcolor{posgreen!50}$+0.167$ \\
\cmidrule(lr){2-18}
 & rp & lam & $1.696$ & $1.497$ & \cellcolor{posgreen!50}$+0.199$ & $2.457$ & $1.784$ & \cellcolor{posgreen!50}$+0.673$ & $1.806$ & $1.915$ & \cellcolor{negred!50}$-0.109$ & $1.747$ & $1.265$ & \cellcolor{posgreen!50}$+0.482$ & $0.583$ & $0.430$ & \cellcolor{posgreen!50}$+0.153$ \\
 &  & raw & $1.705$ & $1.529$ & \cellcolor{posgreen!50}$+0.176$ & $2.464$ & $1.799$ & \cellcolor{posgreen!50}$+0.665$ & $1.903$ & $2.019$ & \cellcolor{negred!50}$-0.115$ & $1.744$ & $1.269$ & \cellcolor{posgreen!50}$+0.475$ & $0.583$ & $0.430$ & \cellcolor{posgreen!50}$+0.153$ \\
 &  & inv & $1.458$ & $1.297$ & \cellcolor{posgreen!50}$+0.162$ & $2.476$ & $1.644$ & \cellcolor{posgreen!50}$+0.833$ & $1.414$ & $1.361$ & \cellcolor{posgreen!50}$+0.054$ & $1.534$ & $1.369$ & \cellcolor{posgreen!50}$+0.165$ & $0.739$ & $0.672$ & \cellcolor{posgreen!50}$+0.067$ \\
 &  & vsp & $1.561$ & $1.371$ & \cellcolor{posgreen!50}$+0.191$ & $2.592$ & $1.745$ & \cellcolor{posgreen!50}$+0.848$ & $1.514$ & $1.513$ & \cellcolor{posgreen!50}$+0.001$ & $1.756$ & $1.386$ & \cellcolor{posgreen!50}$+0.370$ & $0.691$ & $0.601$ & \cellcolor{posgreen!50}$+0.090$ \\
 &  & fpm & $1.676$ & $1.499$ & \cellcolor{posgreen!50}$+0.177$ & $1.983$ & $1.441$ & \cellcolor{posgreen!50}$+0.542$ & $1.711$ & $1.725$ & \cellcolor{negred!50}$-0.015$ & $1.845$ & $1.682$ & \cellcolor{posgreen!50}$+0.162$ & $0.882$ & $0.691$ & \cellcolor{posgreen!50}$+0.191$ \\
\bottomrule
\end{tabular}}
\end{table}
```

## MDD — $\omega=$err

```latex
% NOTE: 표가 페이지 폭을 넘으면 paper3.md 프리앰블에 \usepackage{pdflscape}를 추가하고
%       \begin{landscape} ... \end{landscape}로 표 전체를 감싸 가로 회전하시기 바랍니다.
\begin{table}[!htbp]
\centering
\caption{전체 45 슬롯 최대낙폭 (MDD) 결과 ($\Omega=$err 고정). $p_w \times \text{prior} \times q$ = $3 \times 3 \times 5$ = 45 슬롯 각각의 LSTM(L)·ANN(A) 최대낙폭 (MDD) 및 차이 $\Delta = \mathrm{L} - \mathrm{A}$를 5개 구간(All, R1 회복, R2 확장, R3 위기, R4 AI 랠리)에 대해 보고한다. MDD는 음수가 손실이므로 $\Delta > 0$이 LSTM이 덜 빠진 경우이다.}
\label{tab:app_grid_mdd_err}
\setlength{\tabcolsep}{2pt}
\renewcommand{\arraystretch}{1.05}
\scriptsize
\resizebox{\textwidth}{!}{%
\begin{tabular}{lll ccc ccc ccc ccc ccc}
\toprule
 & & & \multicolumn{3}{c}{All} & \multicolumn{3}{c}{R1} & \multicolumn{3}{c}{R2} & \multicolumn{3}{c}{R3} & \multicolumn{3}{c}{R4} \\
\cmidrule(lr){4-6} \cmidrule(lr){7-9} \cmidrule(lr){10-12} \cmidrule(lr){13-15} \cmidrule(lr){16-18}
$p_w$ & prior & $q$ & L & A & $\Delta$ & L & A & $\Delta$ & L & A & $\Delta$ & L & A & $\Delta$ & L & A & $\Delta$ \\
\midrule
mcap & mcap & lam & $-16.48\%$ & $-16.03\%$ & \cellcolor{negred!50}$-0.45\%$ & $-16.22\%$ & $-13.51\%$ & \cellcolor{negred!50}$-2.72\%$ & $-16.48\%$ & $-13.08\%$ & \cellcolor{negred!50}$-3.40\%$ & $-9.95\%$ & $-16.03\%$ & \cellcolor{posgreen!50}$+6.08\%$ & $-6.87\%$ & $-7.07\%$ & \cellcolor{posgreen!50}$+0.20\%$ \\
 &  & raw & $-16.22\%$ & $-16.03\%$ & \cellcolor{negred!50}$-0.19\%$ & $-16.22\%$ & $-13.51\%$ & \cellcolor{negred!50}$-2.72\%$ & $-10.34\%$ & $-11.48\%$ & \cellcolor{posgreen!50}$+1.14\%$ & $-9.95\%$ & $-16.03\%$ & \cellcolor{posgreen!50}$+6.08\%$ & $-6.87\%$ & $-7.07\%$ & \cellcolor{posgreen!50}$+0.20\%$ \\
 &  & inv & $-15.77\%$ & $-16.06\%$ & \cellcolor{posgreen!50}$+0.29\%$ & $-13.25\%$ & $-11.41\%$ & \cellcolor{negred!50}$-1.83\%$ & $-15.77\%$ & $-16.06\%$ & \cellcolor{posgreen!50}$+0.29\%$ & $-12.88\%$ & $-15.89\%$ & \cellcolor{posgreen!50}$+3.02\%$ & $-8.11\%$ & $-7.47\%$ & \cellcolor{negred!50}$-0.64\%$ \\
 &  & vsp & $-16.78\%$ & $-15.70\%$ & \cellcolor{negred!50}$-1.09\%$ & $-15.22\%$ & $-12.80\%$ & \cellcolor{negred!50}$-2.43\%$ & $-16.78\%$ & $-15.70\%$ & \cellcolor{negred!50}$-1.09\%$ & $-11.82\%$ & $-15.21\%$ & \cellcolor{posgreen!50}$+3.39\%$ & $-7.82\%$ & $-7.45\%$ & \cellcolor{negred!50}$-0.38\%$ \\
 &  & fpm & $-20.48\%$ & $-18.39\%$ & \cellcolor{negred!50}$-2.10\%$ & $-17.12\%$ & $-12.54\%$ & \cellcolor{negred!50}$-4.58\%$ & $-17.57\%$ & $-16.10\%$ & \cellcolor{negred!50}$-1.47\%$ & $-16.53\%$ & $-16.14\%$ & \cellcolor{negred!50}$-0.39\%$ & $-13.95\%$ & $-18.39\%$ & \cellcolor{posgreen!50}$+4.43\%$ \\
\cmidrule(lr){2-18}
 & eq & lam & $-17.84\%$ & $-14.61\%$ & \cellcolor{negred!50}$-3.22\%$ & $-16.96\%$ & $-14.11\%$ & \cellcolor{negred!50}$-2.85\%$ & $-17.84\%$ & $-11.96\%$ & \cellcolor{negred!50}$-5.88\%$ & $-9.88\%$ & $-14.61\%$ & \cellcolor{posgreen!50}$+4.73\%$ & $-8.07\%$ & $-7.69\%$ & \cellcolor{negred!50}$-0.38\%$ \\
 &  & raw & $-16.96\%$ & $-14.61\%$ & \cellcolor{negred!50}$-2.35\%$ & $-16.96\%$ & $-14.11\%$ & \cellcolor{negred!50}$-2.85\%$ & $-10.73\%$ & $-9.93\%$ & \cellcolor{negred!50}$-0.80\%$ & $-9.88\%$ & $-14.61\%$ & \cellcolor{posgreen!50}$+4.73\%$ & $-8.07\%$ & $-7.69\%$ & \cellcolor{negred!50}$-0.38\%$ \\
 &  & inv & $-18.51\%$ & $-16.70\%$ & \cellcolor{negred!50}$-1.80\%$ & $-14.70\%$ & $-12.13\%$ & \cellcolor{negred!50}$-2.58\%$ & $-16.45\%$ & $-16.70\%$ & \cellcolor{posgreen!50}$+0.26\%$ & $-11.39\%$ & $-14.43\%$ & \cellcolor{posgreen!50}$+3.04\%$ & $-10.13\%$ & $-8.95\%$ & \cellcolor{negred!50}$-1.18\%$ \\
 &  & vsp & $-17.13\%$ & $-16.10\%$ & \cellcolor{negred!50}$-1.03\%$ & $-16.24\%$ & $-13.68\%$ & \cellcolor{negred!50}$-2.56\%$ & $-17.13\%$ & $-16.10\%$ & \cellcolor{negred!50}$-1.03\%$ & $-10.12\%$ & $-14.52\%$ & \cellcolor{posgreen!50}$+4.39\%$ & $-9.91\%$ & $-8.98\%$ & \cellcolor{negred!50}$-0.93\%$ \\
 &  & fpm & $-25.60\%$ & $-18.05\%$ & \cellcolor{negred!50}$-7.55\%$ & $-17.22\%$ & $-13.43\%$ & \cellcolor{negred!50}$-3.79\%$ & $-18.56\%$ & $-15.89\%$ & \cellcolor{negred!50}$-2.67\%$ & $-19.22\%$ & $-14.48\%$ & \cellcolor{negred!50}$-4.73\%$ & $-14.06\%$ & $-18.05\%$ & \cellcolor{posgreen!50}$+3.98\%$ \\
\cmidrule(lr){2-18}
 & rp & lam & $-16.41\%$ & $-13.97\%$ & \cellcolor{negred!50}$-2.44\%$ & $-14.40\%$ & $-11.99\%$ & \cellcolor{negred!50}$-2.41\%$ & $-16.41\%$ & $-11.06\%$ & \cellcolor{negred!50}$-5.35\%$ & $-10.15\%$ & $-13.97\%$ & \cellcolor{posgreen!50}$+3.82\%$ & $-6.99\%$ & $-6.85\%$ & \cellcolor{negred!50}$-0.15\%$ \\
 &  & raw & $-14.40\%$ & $-13.97\%$ & \cellcolor{negred!50}$-0.42\%$ & $-14.40\%$ & $-11.99\%$ & \cellcolor{negred!50}$-2.41\%$ & $-10.22\%$ & $-9.25\%$ & \cellcolor{negred!50}$-0.97\%$ & $-10.15\%$ & $-13.97\%$ & \cellcolor{posgreen!50}$+3.82\%$ & $-6.99\%$ & $-6.85\%$ & \cellcolor{negred!50}$-0.15\%$ \\
 &  & inv & $-17.22\%$ & $-15.53\%$ & \cellcolor{negred!50}$-1.69\%$ & $-12.38\%$ & $-10.70\%$ & \cellcolor{negred!50}$-1.68\%$ & $-15.44\%$ & $-15.53\%$ & \cellcolor{posgreen!50}$+0.09\%$ & $-10.93\%$ & $-13.79\%$ & \cellcolor{posgreen!50}$+2.85\%$ & $-8.80\%$ & $-7.96\%$ & \cellcolor{negred!50}$-0.84\%$ \\
 &  & vsp & $-15.68\%$ & $-14.82\%$ & \cellcolor{negred!50}$-0.86\%$ & $-13.87\%$ & $-11.74\%$ & \cellcolor{negred!50}$-2.13\%$ & $-15.68\%$ & $-14.82\%$ & \cellcolor{negred!50}$-0.86\%$ & $-10.26\%$ & $-13.76\%$ & \cellcolor{posgreen!50}$+3.51\%$ & $-8.69\%$ & $-8.01\%$ & \cellcolor{negred!50}$-0.68\%$ \\
 &  & fpm & $-23.79\%$ & $-17.35\%$ & \cellcolor{negred!50}$-6.44\%$ & $-14.74\%$ & $-11.57\%$ & \cellcolor{negred!50}$-3.17\%$ & $-17.50\%$ & $-14.96\%$ & \cellcolor{negred!50}$-2.53\%$ & $-17.73\%$ & $-13.84\%$ & \cellcolor{negred!50}$-3.89\%$ & $-12.93\%$ & $-17.35\%$ & \cellcolor{posgreen!50}$+4.42\%$ \\
\midrule
eq & mcap & lam & $-14.73\%$ & $-18.86\%$ & \cellcolor{posgreen!50}$+4.13\%$ & $-12.75\%$ & $-12.65\%$ & \cellcolor{negred!50}$-0.10\%$ & $-8.20\%$ & $-10.80\%$ & \cellcolor{posgreen!50}$+2.60\%$ & $-14.73\%$ & $-18.86\%$ & \cellcolor{posgreen!50}$+4.13\%$ & $-8.86\%$ & $-9.66\%$ & \cellcolor{posgreen!50}$+0.80\%$ \\
 &  & raw & $-14.73\%$ & $-18.86\%$ & \cellcolor{posgreen!50}$+4.13\%$ & $-12.75\%$ & $-12.65\%$ & \cellcolor{negred!50}$-0.10\%$ & $-8.35\%$ & $-11.00\%$ & \cellcolor{posgreen!50}$+2.65\%$ & $-14.73\%$ & $-18.86\%$ & \cellcolor{posgreen!50}$+4.13\%$ & $-8.86\%$ & $-9.66\%$ & \cellcolor{posgreen!50}$+0.80\%$ \\
 &  & inv & $-14.59\%$ & $-17.67\%$ & \cellcolor{posgreen!50}$+3.07\%$ & $-10.72\%$ & $-10.98\%$ & \cellcolor{posgreen!50}$+0.27\%$ & $-11.86\%$ & $-13.88\%$ & \cellcolor{posgreen!50}$+2.02\%$ & $-14.59\%$ & $-17.67\%$ & \cellcolor{posgreen!50}$+3.07\%$ & $-7.33\%$ & $-9.42\%$ & \cellcolor{posgreen!50}$+2.09\%$ \\
 &  & vsp & $-13.65\%$ & $-17.44\%$ & \cellcolor{posgreen!50}$+3.79\%$ & $-12.37\%$ & $-12.18\%$ & \cellcolor{negred!50}$-0.19\%$ & $-9.96\%$ & $-11.92\%$ & \cellcolor{posgreen!50}$+1.97\%$ & $-13.65\%$ & $-17.44\%$ & \cellcolor{posgreen!50}$+3.79\%$ & $-8.14\%$ & $-9.40\%$ & \cellcolor{posgreen!50}$+1.26\%$ \\
 &  & fpm & $-15.71\%$ & $-17.28\%$ & \cellcolor{posgreen!50}$+1.57\%$ & $-15.71\%$ & $-13.51\%$ & \cellcolor{negred!50}$-2.20\%$ & $-11.42\%$ & $-11.47\%$ & \cellcolor{posgreen!50}$+0.05\%$ & $-15.14\%$ & $-17.28\%$ & \cellcolor{posgreen!50}$+2.14\%$ & $-7.89\%$ & $-9.82\%$ & \cellcolor{posgreen!50}$+1.93\%$ \\
\cmidrule(lr){2-18}
 & eq & lam & $-13.65\%$ & $-18.55\%$ & \cellcolor{posgreen!50}$+4.90\%$ & $-13.36\%$ & $-12.73\%$ & \cellcolor{negred!50}$-0.63\%$ & $-8.17\%$ & $-10.27\%$ & \cellcolor{posgreen!50}$+2.10\%$ & $-13.65\%$ & $-18.55\%$ & \cellcolor{posgreen!50}$+4.90\%$ & $-8.95\%$ & $-9.87\%$ & \cellcolor{posgreen!50}$+0.92\%$ \\
 &  & raw & $-13.65\%$ & $-18.55\%$ & \cellcolor{posgreen!50}$+4.90\%$ & $-13.36\%$ & $-12.73\%$ & \cellcolor{negred!50}$-0.63\%$ & $-8.24\%$ & $-10.55\%$ & \cellcolor{posgreen!50}$+2.31\%$ & $-13.65\%$ & $-18.55\%$ & \cellcolor{posgreen!50}$+4.90\%$ & $-8.95\%$ & $-9.87\%$ & \cellcolor{posgreen!50}$+0.92\%$ \\
 &  & inv & $-17.57\%$ & $-16.55\%$ & \cellcolor{negred!50}$-1.02\%$ & $-11.18\%$ & $-11.09\%$ & \cellcolor{negred!50}$-0.09\%$ & $-12.02\%$ & $-14.23\%$ & \cellcolor{posgreen!50}$+2.21\%$ & $-11.38\%$ & $-15.26\%$ & \cellcolor{posgreen!50}$+3.88\%$ & $-8.30\%$ & $-10.02\%$ & \cellcolor{posgreen!50}$+1.72\%$ \\
 &  & vsp & $-13.74\%$ & $-15.65\%$ & \cellcolor{posgreen!50}$+1.91\%$ & $-12.50\%$ & $-12.25\%$ & \cellcolor{negred!50}$-0.25\%$ & $-10.13\%$ & $-11.52\%$ & \cellcolor{posgreen!50}$+1.39\%$ & $-11.48\%$ & $-15.65\%$ & \cellcolor{posgreen!50}$+4.18\%$ & $-8.64\%$ & $-10.08\%$ & \cellcolor{posgreen!50}$+1.44\%$ \\
 &  & fpm & $-15.10\%$ & $-14.93\%$ & \cellcolor{negred!50}$-0.16\%$ & $-15.10\%$ & $-14.06\%$ & \cellcolor{negred!50}$-1.04\%$ & $-11.49\%$ & $-11.00\%$ & \cellcolor{negred!50}$-0.49\%$ & $-11.81\%$ & $-14.93\%$ & \cellcolor{posgreen!50}$+3.12\%$ & $-9.58\%$ & $-11.01\%$ & \cellcolor{posgreen!50}$+1.43\%$ \\
\cmidrule(lr){2-18}
 & rp & lam & $-13.75\%$ & $-17.64\%$ & \cellcolor{posgreen!50}$+3.88\%$ & $-11.83\%$ & $-11.13\%$ & \cellcolor{negred!50}$-0.71\%$ & $-8.35\%$ & $-10.16\%$ & \cellcolor{posgreen!50}$+1.81\%$ & $-13.75\%$ & $-17.64\%$ & \cellcolor{posgreen!50}$+3.88\%$ & $-7.76\%$ & $-8.91\%$ & \cellcolor{posgreen!50}$+1.15\%$ \\
 &  & raw & $-13.75\%$ & $-17.64\%$ & \cellcolor{posgreen!50}$+3.88\%$ & $-11.83\%$ & $-11.13\%$ & \cellcolor{negred!50}$-0.71\%$ & $-8.48\%$ & $-10.27\%$ & \cellcolor{posgreen!50}$+1.79\%$ & $-13.75\%$ & $-17.64\%$ & \cellcolor{posgreen!50}$+3.88\%$ & $-7.76\%$ & $-8.91\%$ & \cellcolor{posgreen!50}$+1.15\%$ \\
 &  & inv & $-16.17\%$ & $-15.32\%$ & \cellcolor{negred!50}$-0.84\%$ & $-9.68\%$ & $-9.65\%$ & $-0.03\%$ & $-11.36\%$ & $-13.45\%$ & \cellcolor{posgreen!50}$+2.08\%$ & $-11.47\%$ & $-14.03\%$ & \cellcolor{posgreen!50}$+2.56\%$ & $-7.30\%$ & $-8.70\%$ & \cellcolor{posgreen!50}$+1.40\%$ \\
 &  & vsp & $-12.73\%$ & $-14.63\%$ & \cellcolor{posgreen!50}$+1.90\%$ & $-11.15\%$ & $-10.69\%$ & \cellcolor{negred!50}$-0.46\%$ & $-9.83\%$ & $-10.86\%$ & \cellcolor{posgreen!50}$+1.03\%$ & $-11.60\%$ & $-14.63\%$ & \cellcolor{posgreen!50}$+3.03\%$ & $-7.56\%$ & $-8.88\%$ & \cellcolor{posgreen!50}$+1.33\%$ \\
 &  & fpm & $-13.27\%$ & $-13.80\%$ & \cellcolor{posgreen!50}$+0.53\%$ & $-13.27\%$ & $-12.33\%$ & \cellcolor{negred!50}$-0.94\%$ & $-10.79\%$ & $-10.34\%$ & \cellcolor{negred!50}$-0.45\%$ & $-11.75\%$ & $-13.80\%$ & \cellcolor{posgreen!50}$+2.05\%$ & $-8.63\%$ & $-9.64\%$ & \cellcolor{posgreen!50}$+1.01\%$ \\
\midrule
rp & mcap & lam & $-14.01\%$ & $-18.62\%$ & \cellcolor{posgreen!50}$+4.61\%$ & $-14.01\%$ & $-15.13\%$ & \cellcolor{posgreen!50}$+1.12\%$ & $-8.45\%$ & $-10.60\%$ & \cellcolor{posgreen!50}$+2.15\%$ & $-13.43\%$ & $-18.62\%$ & \cellcolor{posgreen!50}$+5.19\%$ & $-8.74\%$ & $-9.34\%$ & \cellcolor{posgreen!50}$+0.60\%$ \\
 &  & raw & $-14.01\%$ & $-18.62\%$ & \cellcolor{posgreen!50}$+4.61\%$ & $-14.01\%$ & $-15.13\%$ & \cellcolor{posgreen!50}$+1.12\%$ & $-8.65\%$ & $-10.59\%$ & \cellcolor{posgreen!50}$+1.94\%$ & $-13.43\%$ & $-18.62\%$ & \cellcolor{posgreen!50}$+5.19\%$ & $-8.74\%$ & $-9.34\%$ & \cellcolor{posgreen!50}$+0.60\%$ \\
 &  & inv & $-14.72\%$ & $-17.59\%$ & \cellcolor{posgreen!50}$+2.87\%$ & $-10.96\%$ & $-15.30\%$ & \cellcolor{posgreen!50}$+4.34\%$ & $-13.57\%$ & $-14.73\%$ & \cellcolor{posgreen!50}$+1.16\%$ & $-14.72\%$ & $-17.59\%$ & \cellcolor{posgreen!50}$+2.87\%$ & $-6.94\%$ & $-8.38\%$ & \cellcolor{posgreen!50}$+1.44\%$ \\
 &  & vsp & $-13.98\%$ & $-17.51\%$ & \cellcolor{posgreen!50}$+3.53\%$ & $-12.67\%$ & $-15.17\%$ & \cellcolor{posgreen!50}$+2.50\%$ & $-11.30\%$ & $-13.23\%$ & \cellcolor{posgreen!50}$+1.92\%$ & $-13.98\%$ & $-17.51\%$ & \cellcolor{posgreen!50}$+3.53\%$ & $-7.78\%$ & $-8.57\%$ & \cellcolor{posgreen!50}$+0.79\%$ \\
 &  & fpm & $-19.24\%$ & $-17.17\%$ & \cellcolor{negred!50}$-2.07\%$ & $-19.24\%$ & $-16.10\%$ & \cellcolor{negred!50}$-3.14\%$ & $-12.58\%$ & $-12.43\%$ & \cellcolor{negred!50}$-0.14\%$ & $-15.02\%$ & $-17.17\%$ & \cellcolor{posgreen!50}$+2.15\%$ & $-7.54\%$ & $-9.50\%$ & \cellcolor{posgreen!50}$+1.96\%$ \\
\cmidrule(lr){2-18}
 & eq & lam & $-13.87\%$ & $-18.23\%$ & \cellcolor{posgreen!50}$+4.37\%$ & $-13.87\%$ & $-14.45\%$ & \cellcolor{posgreen!50}$+0.59\%$ & $-8.33\%$ & $-9.98\%$ & \cellcolor{posgreen!50}$+1.64\%$ & $-12.69\%$ & $-18.23\%$ & \cellcolor{posgreen!50}$+5.54\%$ & $-7.57\%$ & $-9.04\%$ & \cellcolor{posgreen!50}$+1.48\%$ \\
 &  & raw & $-13.87\%$ & $-18.23\%$ & \cellcolor{posgreen!50}$+4.37\%$ & $-13.87\%$ & $-14.44\%$ & \cellcolor{posgreen!50}$+0.58\%$ & $-8.38\%$ & $-10.26\%$ & \cellcolor{posgreen!50}$+1.88\%$ & $-12.69\%$ & $-18.23\%$ & \cellcolor{posgreen!50}$+5.54\%$ & $-7.57\%$ & $-9.04\%$ & \cellcolor{posgreen!50}$+1.48\%$ \\
 &  & inv & $-17.79\%$ & $-16.92\%$ & \cellcolor{negred!50}$-0.87\%$ & $-10.91\%$ & $-14.61\%$ & \cellcolor{posgreen!50}$+3.70\%$ & $-14.12\%$ & $-15.26\%$ & \cellcolor{posgreen!50}$+1.15\%$ & $-11.45\%$ & $-15.02\%$ & \cellcolor{posgreen!50}$+3.57\%$ & $-7.57\%$ & $-8.72\%$ & \cellcolor{posgreen!50}$+1.14\%$ \\
 &  & vsp & $-14.12\%$ & $-15.26\%$ & \cellcolor{posgreen!50}$+1.14\%$ & $-12.51\%$ & $-14.49\%$ & \cellcolor{posgreen!50}$+1.98\%$ & $-10.81\%$ & $-13.49\%$ & \cellcolor{posgreen!50}$+2.68\%$ & $-11.63\%$ & $-15.26\%$ & \cellcolor{posgreen!50}$+3.64\%$ & $-7.76\%$ & $-8.77\%$ & \cellcolor{posgreen!50}$+1.01\%$ \\
 &  & fpm & $-17.91\%$ & $-15.75\%$ & \cellcolor{negred!50}$-2.16\%$ & $-17.91\%$ & $-15.75\%$ & \cellcolor{negred!50}$-2.16\%$ & $-12.81\%$ & $-12.27\%$ & \cellcolor{negred!50}$-0.55\%$ & $-11.46\%$ & $-14.89\%$ & \cellcolor{posgreen!50}$+3.43\%$ & $-9.49\%$ & $-10.21\%$ & \cellcolor{posgreen!50}$+0.71\%$ \\
\cmidrule(lr){2-18}
 & rp & lam & $-12.84\%$ & $-17.33\%$ & \cellcolor{posgreen!50}$+4.49\%$ & $-11.88\%$ & $-12.91\%$ & \cellcolor{posgreen!50}$+1.04\%$ & $-8.59\%$ & $-9.90\%$ & \cellcolor{posgreen!50}$+1.31\%$ & $-12.84\%$ & $-17.33\%$ & \cellcolor{posgreen!50}$+4.49\%$ & $-6.89\%$ & $-8.15\%$ & \cellcolor{posgreen!50}$+1.26\%$ \\
 &  & raw & $-12.84\%$ & $-17.33\%$ & \cellcolor{posgreen!50}$+4.49\%$ & $-11.88\%$ & $-12.90\%$ & \cellcolor{posgreen!50}$+1.03\%$ & $-8.81\%$ & $-9.93\%$ & \cellcolor{posgreen!50}$+1.12\%$ & $-12.84\%$ & $-17.33\%$ & \cellcolor{posgreen!50}$+4.49\%$ & $-6.89\%$ & $-8.15\%$ & \cellcolor{posgreen!50}$+1.26\%$ \\
 &  & inv & $-16.42\%$ & $-15.59\%$ & \cellcolor{negred!50}$-0.83\%$ & $-9.59\%$ & $-13.06\%$ & \cellcolor{posgreen!50}$+3.47\%$ & $-13.26\%$ & $-14.32\%$ & \cellcolor{posgreen!50}$+1.05\%$ & $-11.55\%$ & $-13.86\%$ & \cellcolor{posgreen!50}$+2.31\%$ & $-7.13\%$ & $-7.66\%$ & \cellcolor{posgreen!50}$+0.53\%$ \\
 &  & vsp & $-12.95\%$ & $-14.40\%$ & \cellcolor{posgreen!50}$+1.45\%$ & $-10.84\%$ & $-12.94\%$ & \cellcolor{posgreen!50}$+2.11\%$ & $-10.22\%$ & $-12.53\%$ & \cellcolor{posgreen!50}$+2.31\%$ & $-11.72\%$ & $-14.40\%$ & \cellcolor{posgreen!50}$+2.68\%$ & $-7.27\%$ & $-7.85\%$ & \cellcolor{posgreen!50}$+0.58\%$ \\
 &  & fpm & $-15.69\%$ & $-13.96\%$ & \cellcolor{negred!50}$-1.73\%$ & $-15.69\%$ & $-13.96\%$ & \cellcolor{negred!50}$-1.73\%$ & $-11.87\%$ & $-11.38\%$ & \cellcolor{negred!50}$-0.48\%$ & $-11.64\%$ & $-13.54\%$ & \cellcolor{posgreen!50}$+1.91\%$ & $-8.60\%$ & $-9.19\%$ & \cellcolor{posgreen!50}$+0.59\%$ \\
\bottomrule
\end{tabular}}
\end{table}
```

## Sharpe — $\omega=$he

```latex
% NOTE: 표가 페이지 폭을 넘으면 paper3.md 프리앰블에 \usepackage{pdflscape}를 추가하고
%       \begin{landscape} ... \end{landscape}로 표 전체를 감싸 가로 회전하시기 바랍니다.
\begin{table}[!htbp]
\centering
\caption{전체 45 슬롯 Sharpe 비율 결과 ($\Omega=$he 고정). $p_w \times \text{prior} \times q$ = $3 \times 3 \times 5$ = 45 슬롯 각각의 LSTM(L)·ANN(A) Sharpe 비율 및 차이 $\Delta = \mathrm{L} - \mathrm{A}$를 5개 구간(All, R1 회복, R2 확장, R3 위기, R4 AI 랠리)에 대해 보고한다.}
\label{tab:app_grid_sharpe_he}
\setlength{\tabcolsep}{2pt}
\renewcommand{\arraystretch}{1.05}
\scriptsize
\resizebox{\textwidth}{!}{%
\begin{tabular}{lll ccc ccc ccc ccc ccc}
\toprule
 & & & \multicolumn{3}{c}{All} & \multicolumn{3}{c}{R1} & \multicolumn{3}{c}{R2} & \multicolumn{3}{c}{R3} & \multicolumn{3}{c}{R4} \\
\cmidrule(lr){4-6} \cmidrule(lr){7-9} \cmidrule(lr){10-12} \cmidrule(lr){13-15} \cmidrule(lr){16-18}
$p_w$ & prior & $q$ & L & A & $\Delta$ & L & A & $\Delta$ & L & A & $\Delta$ & L & A & $\Delta$ & L & A & $\Delta$ \\
\midrule
mcap & mcap & lam & $0.968$ & $0.882$ & \cellcolor{posgreen!50}$+0.086$ & $1.041$ & $1.146$ & \cellcolor{negred!50}$-0.105$ & $1.201$ & $1.195$ & \cellcolor{posgreen!50}$+0.006$ & $0.709$ & $0.415$ & \cellcolor{posgreen!50}$+0.294$ & $0.677$ & $0.505$ & \cellcolor{posgreen!50}$+0.172$ \\
 &  & raw & $0.999$ & $0.910$ & \cellcolor{posgreen!50}$+0.089$ & $1.059$ & $1.156$ & \cellcolor{negred!50}$-0.097$ & $1.243$ & $1.243$ & $+0.000$ & $0.722$ & $0.425$ & \cellcolor{posgreen!50}$+0.298$ & $0.677$ & $0.505$ & \cellcolor{posgreen!50}$+0.172$ \\
 &  & inv & $0.983$ & $0.927$ & \cellcolor{posgreen!50}$+0.056$ & $1.390$ & $1.539$ & \cellcolor{negred!50}$-0.150$ & $1.237$ & $1.154$ & \cellcolor{posgreen!50}$+0.083$ & $0.567$ & $0.515$ & \cellcolor{posgreen!50}$+0.052$ & $0.906$ & $0.712$ & \cellcolor{posgreen!50}$+0.194$ \\
 &  & vsp & $0.965$ & $0.896$ & \cellcolor{posgreen!50}$+0.069$ & $1.149$ & $1.220$ & \cellcolor{negred!50}$-0.071$ & $1.250$ & $1.167$ & \cellcolor{posgreen!50}$+0.083$ & $0.567$ & $0.476$ & \cellcolor{posgreen!50}$+0.092$ & $0.880$ & $0.706$ & \cellcolor{posgreen!50}$+0.173$ \\
 &  & fpm & $0.830$ & $0.871$ & \cellcolor{negred!50}$-0.041$ & $0.882$ & $1.133$ & \cellcolor{negred!50}$-0.251$ & $1.178$ & $1.043$ & \cellcolor{posgreen!50}$+0.135$ & $0.580$ & $0.680$ & \cellcolor{negred!50}$-0.100$ & $0.599$ & $0.637$ & \cellcolor{negred!50}$-0.038$ \\
\cmidrule(lr){2-18}
 & eq & lam & $0.976$ & $0.913$ & \cellcolor{posgreen!50}$+0.063$ & $1.200$ & $1.283$ & \cellcolor{negred!50}$-0.083$ & $1.241$ & $1.221$ & \cellcolor{posgreen!50}$+0.019$ & $0.811$ & $0.530$ & \cellcolor{posgreen!50}$+0.282$ & $0.374$ & $0.369$ & \cellcolor{posgreen!50}$+0.006$ \\
 &  & raw & $1.001$ & $0.942$ & \cellcolor{posgreen!50}$+0.059$ & $1.213$ & $1.288$ & \cellcolor{negred!50}$-0.076$ & $1.266$ & $1.275$ & \cellcolor{negred!50}$-0.009$ & $0.823$ & $0.536$ & \cellcolor{posgreen!50}$+0.287$ & $0.374$ & $0.369$ & \cellcolor{posgreen!50}$+0.006$ \\
 &  & inv & $0.913$ & $0.918$ & \cellcolor{negred!50}$-0.004$ & $1.617$ & $1.828$ & \cellcolor{negred!50}$-0.211$ & $1.265$ & $1.217$ & \cellcolor{posgreen!50}$+0.048$ & $0.562$ & $0.534$ & \cellcolor{posgreen!50}$+0.028$ & $0.410$ & $0.385$ & \cellcolor{posgreen!50}$+0.025$ \\
 &  & vsp & $0.914$ & $0.906$ & \cellcolor{posgreen!50}$+0.008$ & $1.344$ & $1.419$ & \cellcolor{negred!50}$-0.075$ & $1.325$ & $1.273$ & \cellcolor{posgreen!50}$+0.052$ & $0.565$ & $0.521$ & \cellcolor{posgreen!50}$+0.044$ & $0.367$ & $0.374$ & \cellcolor{negred!50}$-0.007$ \\
 &  & fpm & $0.795$ & $0.813$ & \cellcolor{negred!50}$-0.019$ & $1.076$ & $1.317$ & \cellcolor{negred!50}$-0.241$ & $1.216$ & $1.014$ & \cellcolor{posgreen!50}$+0.202$ & $0.572$ & $0.628$ & \cellcolor{negred!50}$-0.056$ & $0.334$ & $0.387$ & \cellcolor{negred!50}$-0.053$ \\
\cmidrule(lr){2-18}
 & rp & lam & $0.959$ & $0.897$ & \cellcolor{posgreen!50}$+0.062$ & $1.361$ & $1.458$ & \cellcolor{negred!50}$-0.097$ & $1.189$ & $1.167$ & \cellcolor{posgreen!50}$+0.022$ & $0.742$ & $0.465$ & \cellcolor{posgreen!50}$+0.276$ & $0.339$ & $0.346$ & \cellcolor{negred!50}$-0.007$ \\
 &  & raw & $0.981$ & $0.935$ & \cellcolor{posgreen!50}$+0.046$ & $1.372$ & $1.465$ & \cellcolor{negred!50}$-0.092$ & $1.213$ & $1.241$ & \cellcolor{negred!50}$-0.028$ & $0.752$ & $0.474$ & \cellcolor{posgreen!50}$+0.278$ & $0.339$ & $0.346$ & \cellcolor{negred!50}$-0.007$ \\
 &  & inv & $0.906$ & $0.923$ & \cellcolor{negred!50}$-0.017$ & $1.706$ & $1.981$ & \cellcolor{negred!50}$-0.275$ & $1.254$ & $1.224$ & \cellcolor{posgreen!50}$+0.030$ & $0.537$ & $0.515$ & \cellcolor{posgreen!50}$+0.022$ & $0.357$ & $0.331$ & \cellcolor{posgreen!50}$+0.025$ \\
 &  & vsp & $0.918$ & $0.911$ & \cellcolor{posgreen!50}$+0.007$ & $1.524$ & $1.618$ & \cellcolor{negred!50}$-0.094$ & $1.281$ & $1.266$ & \cellcolor{posgreen!50}$+0.015$ & $0.566$ & $0.488$ & \cellcolor{posgreen!50}$+0.078$ & $0.318$ & $0.312$ & \cellcolor{posgreen!50}$+0.006$ \\
 &  & fpm & $0.805$ & $0.831$ & \cellcolor{negred!50}$-0.026$ & $1.194$ & $1.498$ & \cellcolor{negred!50}$-0.304$ & $1.218$ & $1.022$ & \cellcolor{posgreen!50}$+0.196$ & $0.557$ & $0.617$ & \cellcolor{negred!50}$-0.060$ & $0.289$ & $0.356$ & \cellcolor{negred!50}$-0.066$ \\
\midrule
eq & mcap & lam & $0.950$ & $0.907$ & \cellcolor{posgreen!50}$+0.043$ & $1.147$ & $1.159$ & \cellcolor{negred!50}$-0.011$ & $1.226$ & $1.207$ & \cellcolor{posgreen!50}$+0.020$ & $0.584$ & $0.425$ & \cellcolor{posgreen!50}$+0.160$ & $0.499$ & $0.505$ & \cellcolor{negred!50}$-0.007$ \\
 &  & raw & $0.958$ & $0.923$ & \cellcolor{posgreen!50}$+0.035$ & $1.164$ & $1.173$ & \cellcolor{negred!50}$-0.009$ & $1.220$ & $1.221$ & \cellcolor{negred!50}$-0.001$ & $0.590$ & $0.429$ & \cellcolor{posgreen!50}$+0.161$ & $0.499$ & $0.505$ & \cellcolor{negred!50}$-0.007$ \\
 &  & inv & $1.057$ & $1.038$ & \cellcolor{posgreen!50}$+0.019$ & $1.571$ & $1.738$ & \cellcolor{negred!50}$-0.167$ & $1.380$ & $1.326$ & \cellcolor{posgreen!50}$+0.054$ & $0.585$ & $0.534$ & \cellcolor{posgreen!50}$+0.051$ & $0.903$ & $0.865$ & \cellcolor{posgreen!50}$+0.037$ \\
 &  & vsp & $1.040$ & $1.011$ & \cellcolor{posgreen!50}$+0.028$ & $1.287$ & $1.256$ & \cellcolor{posgreen!50}$+0.031$ & $1.422$ & $1.389$ & \cellcolor{posgreen!50}$+0.033$ & $0.551$ & $0.522$ & \cellcolor{posgreen!50}$+0.029$ & $0.828$ & $0.820$ & \cellcolor{posgreen!50}$+0.008$ \\
 &  & fpm & $0.998$ & $0.988$ & \cellcolor{posgreen!50}$+0.010$ & $0.857$ & $0.987$ & \cellcolor{negred!50}$-0.130$ & $1.448$ & $1.312$ & \cellcolor{posgreen!50}$+0.136$ & $0.582$ & $0.588$ & \cellcolor{negred!50}$-0.006$ & $0.910$ & $0.961$ & \cellcolor{negred!50}$-0.050$ \\
\cmidrule(lr){2-18}
 & eq & lam & $0.908$ & $0.898$ & \cellcolor{posgreen!50}$+0.009$ & $1.329$ & $1.367$ & \cellcolor{negred!50}$-0.038$ & $1.199$ & $1.189$ & \cellcolor{posgreen!50}$+0.010$ & $0.564$ & $0.478$ & \cellcolor{posgreen!50}$+0.086$ & $0.237$ & $0.257$ & \cellcolor{negred!50}$-0.019$ \\
 &  & raw & $0.925$ & $0.905$ & \cellcolor{posgreen!50}$+0.020$ & $1.349$ & $1.373$ & \cellcolor{negred!50}$-0.024$ & $1.210$ & $1.180$ & \cellcolor{posgreen!50}$+0.030$ & $0.572$ & $0.486$ & \cellcolor{posgreen!50}$+0.087$ & $0.237$ & $0.257$ & \cellcolor{negred!50}$-0.019$ \\
 &  & inv & $0.954$ & $0.960$ & \cellcolor{negred!50}$-0.006$ & $1.654$ & $1.815$ & \cellcolor{negred!50}$-0.160$ & $1.394$ & $1.328$ & \cellcolor{posgreen!50}$+0.067$ & $0.526$ & $0.530$ & \cellcolor{negred!50}$-0.004$ & $0.396$ & $0.430$ & \cellcolor{negred!50}$-0.034$ \\
 &  & vsp & $0.935$ & $0.956$ & \cellcolor{negred!50}$-0.022$ & $1.513$ & $1.515$ & \cellcolor{negred!50}$-0.002$ & $1.429$ & $1.380$ & \cellcolor{posgreen!50}$+0.050$ & $0.422$ & $0.504$ & \cellcolor{negred!50}$-0.082$ & $0.343$ & $0.397$ & \cellcolor{negred!50}$-0.054$ \\
 &  & fpm & $0.924$ & $0.947$ & \cellcolor{negred!50}$-0.023$ & $1.093$ & $1.224$ & \cellcolor{negred!50}$-0.131$ & $1.474$ & $1.345$ & \cellcolor{posgreen!50}$+0.129$ & $0.511$ & $0.596$ & \cellcolor{negred!50}$-0.085$ & $0.315$ & $0.411$ & \cellcolor{negred!50}$-0.096$ \\
\cmidrule(lr){2-18}
 & rp & lam & $0.902$ & $0.886$ & \cellcolor{posgreen!50}$+0.016$ & $1.471$ & $1.529$ & \cellcolor{negred!50}$-0.058$ & $1.177$ & $1.159$ & \cellcolor{posgreen!50}$+0.018$ & $0.539$ & $0.424$ & \cellcolor{posgreen!50}$+0.116$ & $0.202$ & $0.246$ & \cellcolor{negred!50}$-0.044$ \\
 &  & raw & $0.915$ & $0.895$ & \cellcolor{posgreen!50}$+0.020$ & $1.480$ & $1.535$ & \cellcolor{negred!50}$-0.055$ & $1.186$ & $1.156$ & \cellcolor{posgreen!50}$+0.029$ & $0.546$ & $0.431$ & \cellcolor{posgreen!50}$+0.115$ & $0.202$ & $0.246$ & \cellcolor{negred!50}$-0.044$ \\
 &  & inv & $0.938$ & $0.947$ & \cellcolor{negred!50}$-0.009$ & $1.725$ & $1.865$ & \cellcolor{negred!50}$-0.140$ & $1.365$ & $1.310$ & \cellcolor{posgreen!50}$+0.056$ & $0.501$ & $0.504$ & \cellcolor{negred!50}$-0.002$ & $0.346$ & $0.394$ & \cellcolor{negred!50}$-0.047$ \\
 &  & vsp & $0.926$ & $0.951$ & \cellcolor{negred!50}$-0.024$ & $1.638$ & $1.693$ & \cellcolor{negred!50}$-0.055$ & $1.374$ & $1.339$ & \cellcolor{posgreen!50}$+0.035$ & $0.426$ & $0.477$ & \cellcolor{negred!50}$-0.051$ & $0.299$ & $0.362$ & \cellcolor{negred!50}$-0.063$ \\
 &  & fpm & $0.925$ & $0.935$ & \cellcolor{negred!50}$-0.010$ & $1.184$ & $1.330$ & \cellcolor{negred!50}$-0.146$ & $1.438$ & $1.312$ & \cellcolor{posgreen!50}$+0.126$ & $0.511$ & $0.562$ & \cellcolor{negred!50}$-0.051$ & $0.271$ & $0.354$ & \cellcolor{negred!50}$-0.083$ \\
\midrule
rp & mcap & lam & $0.935$ & $0.865$ & \cellcolor{posgreen!50}$+0.069$ & $1.088$ & $0.926$ & \cellcolor{posgreen!50}$+0.161$ & $1.186$ & $1.185$ & \cellcolor{posgreen!50}$+0.001$ & $0.619$ & $0.447$ & \cellcolor{posgreen!50}$+0.172$ & $0.534$ & $0.534$ & $+0.000$ \\
 &  & raw & $0.960$ & $0.893$ & \cellcolor{posgreen!50}$+0.067$ & $1.092$ & $0.931$ & \cellcolor{posgreen!50}$+0.161$ & $1.222$ & $1.216$ & \cellcolor{posgreen!50}$+0.006$ & $0.626$ & $0.471$ & \cellcolor{posgreen!50}$+0.156$ & $0.534$ & $0.534$ & $+0.000$ \\
 &  & inv & $1.061$ & $0.989$ & \cellcolor{posgreen!50}$+0.072$ & $1.590$ & $1.127$ & \cellcolor{posgreen!50}$+0.462$ & $1.353$ & $1.342$ & \cellcolor{posgreen!50}$+0.011$ & $0.593$ & $0.551$ & \cellcolor{posgreen!50}$+0.042$ & $0.929$ & $0.878$ & \cellcolor{posgreen!50}$+0.051$ \\
 &  & vsp & $1.030$ & $0.985$ & \cellcolor{posgreen!50}$+0.045$ & $1.233$ & $0.983$ & \cellcolor{posgreen!50}$+0.250$ & $1.394$ & $1.409$ & \cellcolor{negred!50}$-0.015$ & $0.560$ & $0.543$ & \cellcolor{posgreen!50}$+0.017$ & $0.851$ & $0.841$ & \cellcolor{posgreen!50}$+0.010$ \\
 &  & fpm & $0.969$ & $0.957$ & \cellcolor{posgreen!50}$+0.012$ & $0.810$ & $0.859$ & \cellcolor{negred!50}$-0.049$ & $1.421$ & $1.320$ & \cellcolor{posgreen!50}$+0.101$ & $0.577$ & $0.580$ & \cellcolor{negred!50}$-0.003$ & $0.883$ & $0.953$ & \cellcolor{negred!50}$-0.070$ \\
\cmidrule(lr){2-18}
 & eq & lam & $0.906$ & $0.875$ & \cellcolor{posgreen!50}$+0.031$ & $1.277$ & $1.112$ & \cellcolor{posgreen!50}$+0.166$ & $1.171$ & $1.181$ & \cellcolor{negred!50}$-0.010$ & $0.603$ & $0.515$ & \cellcolor{posgreen!50}$+0.088$ & $0.274$ & $0.303$ & \cellcolor{negred!50}$-0.029$ \\
 &  & raw & $0.933$ & $0.892$ & \cellcolor{posgreen!50}$+0.041$ & $1.289$ & $1.123$ & \cellcolor{posgreen!50}$+0.166$ & $1.207$ & $1.194$ & \cellcolor{posgreen!50}$+0.013$ & $0.613$ & $0.527$ & \cellcolor{posgreen!50}$+0.086$ & $0.274$ & $0.303$ & \cellcolor{negred!50}$-0.029$ \\
 &  & inv & $0.951$ & $0.913$ & \cellcolor{posgreen!50}$+0.038$ & $1.687$ & $1.227$ & \cellcolor{posgreen!50}$+0.459$ & $1.352$ & $1.321$ & \cellcolor{posgreen!50}$+0.031$ & $0.543$ & $0.537$ & \cellcolor{posgreen!50}$+0.006$ & $0.392$ & $0.438$ & \cellcolor{negred!50}$-0.045$ \\
 &  & vsp & $0.924$ & $0.916$ & \cellcolor{posgreen!50}$+0.008$ & $1.437$ & $1.140$ & \cellcolor{posgreen!50}$+0.297$ & $1.407$ & $1.387$ & \cellcolor{posgreen!50}$+0.020$ & $0.425$ & $0.513$ & \cellcolor{negred!50}$-0.088$ & $0.338$ & $0.401$ & \cellcolor{negred!50}$-0.062$ \\
 &  & fpm & $0.908$ & $0.925$ & \cellcolor{negred!50}$-0.017$ & $1.062$ & $1.079$ & \cellcolor{negred!50}$-0.016$ & $1.451$ & $1.356$ & \cellcolor{posgreen!50}$+0.095$ & $0.503$ & $0.595$ & \cellcolor{negred!50}$-0.091$ & $0.289$ & $0.399$ & \cellcolor{negred!50}$-0.110$ \\
\cmidrule(lr){2-18}
 & rp & lam & $0.890$ & $0.865$ & \cellcolor{posgreen!50}$+0.025$ & $1.425$ & $1.230$ & \cellcolor{posgreen!50}$+0.195$ & $1.140$ & $1.159$ & \cellcolor{negred!50}$-0.019$ & $0.560$ & $0.461$ & \cellcolor{posgreen!50}$+0.100$ & $0.210$ & $0.276$ & \cellcolor{negred!50}$-0.066$ \\
 &  & raw & $0.916$ & $0.888$ & \cellcolor{posgreen!50}$+0.029$ & $1.434$ & $1.240$ & \cellcolor{posgreen!50}$+0.194$ & $1.177$ & $1.186$ & \cellcolor{negred!50}$-0.009$ & $0.567$ & $0.470$ & \cellcolor{posgreen!50}$+0.098$ & $0.210$ & $0.276$ & \cellcolor{negred!50}$-0.066$ \\
 &  & inv & $0.933$ & $0.913$ & \cellcolor{posgreen!50}$+0.020$ & $1.739$ & $1.348$ & \cellcolor{posgreen!50}$+0.392$ & $1.333$ & $1.309$ & \cellcolor{posgreen!50}$+0.025$ & $0.514$ & $0.511$ & \cellcolor{posgreen!50}$+0.003$ & $0.354$ & $0.412$ & \cellcolor{negred!50}$-0.058$ \\
 &  & vsp & $0.916$ & $0.921$ & \cellcolor{negred!50}$-0.005$ & $1.577$ & $1.283$ & \cellcolor{posgreen!50}$+0.294$ & $1.357$ & $1.359$ & \cellcolor{negred!50}$-0.002$ & $0.417$ & $0.493$ & \cellcolor{negred!50}$-0.075$ & $0.299$ & $0.372$ & \cellcolor{negred!50}$-0.073$ \\
 &  & fpm & $0.914$ & $0.921$ & \cellcolor{negred!50}$-0.007$ & $1.170$ & $1.178$ & \cellcolor{negred!50}$-0.008$ & $1.423$ & $1.323$ & \cellcolor{posgreen!50}$+0.100$ & $0.499$ & $0.565$ & \cellcolor{negred!50}$-0.067$ & $0.242$ & $0.348$ & \cellcolor{negred!50}$-0.105$ \\
\bottomrule
\end{tabular}}
\end{table}
```

## Sortino — $\omega=$he

```latex
% NOTE: 표가 페이지 폭을 넘으면 paper3.md 프리앰블에 \usepackage{pdflscape}를 추가하고
%       \begin{landscape} ... \end{landscape}로 표 전체를 감싸 가로 회전하시기 바랍니다.
\begin{table}[!htbp]
\centering
\caption{전체 45 슬롯 Sortino 비율 결과 ($\Omega=$he 고정). $p_w \times \text{prior} \times q$ = $3 \times 3 \times 5$ = 45 슬롯 각각의 LSTM(L)·ANN(A) Sortino 비율 및 차이 $\Delta = \mathrm{L} - \mathrm{A}$를 5개 구간(All, R1 회복, R2 확장, R3 위기, R4 AI 랠리)에 대해 보고한다.}
\label{tab:app_grid_sortino_he}
\setlength{\tabcolsep}{2pt}
\renewcommand{\arraystretch}{1.05}
\scriptsize
\resizebox{\textwidth}{!}{%
\begin{tabular}{lll ccc ccc ccc ccc ccc}
\toprule
 & & & \multicolumn{3}{c}{All} & \multicolumn{3}{c}{R1} & \multicolumn{3}{c}{R2} & \multicolumn{3}{c}{R3} & \multicolumn{3}{c}{R4} \\
\cmidrule(lr){4-6} \cmidrule(lr){7-9} \cmidrule(lr){10-12} \cmidrule(lr){13-15} \cmidrule(lr){16-18}
$p_w$ & prior & $q$ & L & A & $\Delta$ & L & A & $\Delta$ & L & A & $\Delta$ & L & A & $\Delta$ & L & A & $\Delta$ \\
\midrule
mcap & mcap & lam & $1.690$ & $1.537$ & \cellcolor{posgreen!50}$+0.153$ & $1.678$ & $1.905$ & \cellcolor{negred!50}$-0.227$ & $1.854$ & $1.837$ & \cellcolor{posgreen!50}$+0.017$ & $1.601$ & $0.982$ & \cellcolor{posgreen!50}$+0.619$ & $1.190$ & $0.779$ & \cellcolor{posgreen!50}$+0.411$ \\
 &  & raw & $1.793$ & $1.625$ & \cellcolor{posgreen!50}$+0.168$ & $1.714$ & $1.912$ & \cellcolor{negred!50}$-0.198$ & $2.018$ & $2.014$ & \cellcolor{posgreen!50}$+0.004$ & $1.624$ & $1.013$ & \cellcolor{posgreen!50}$+0.611$ & $1.190$ & $0.779$ & \cellcolor{posgreen!50}$+0.411$ \\
 &  & inv & $1.392$ & $1.343$ & \cellcolor{posgreen!50}$+0.049$ & $1.907$ & $2.142$ & \cellcolor{negred!50}$-0.235$ & $1.520$ & $1.446$ & \cellcolor{posgreen!50}$+0.073$ & $1.026$ & $1.003$ & \cellcolor{posgreen!50}$+0.023$ & $1.577$ & $1.087$ & \cellcolor{posgreen!50}$+0.489$ \\
 &  & vsp & $1.453$ & $1.344$ & \cellcolor{posgreen!50}$+0.109$ & $1.775$ & $1.950$ & \cellcolor{negred!50}$-0.175$ & $1.563$ & $1.417$ & \cellcolor{posgreen!50}$+0.146$ & $1.123$ & $1.004$ & \cellcolor{posgreen!50}$+0.119$ & $1.460$ & $1.103$ & \cellcolor{posgreen!50}$+0.357$ \\
 &  & fpm & $1.180$ & $1.260$ & \cellcolor{negred!50}$-0.079$ & $1.462$ & $1.818$ & \cellcolor{negred!50}$-0.356$ & $1.585$ & $1.424$ & \cellcolor{posgreen!50}$+0.161$ & $0.966$ & $1.225$ & \cellcolor{negred!50}$-0.259$ & $0.779$ & $0.827$ & \cellcolor{negred!50}$-0.048$ \\
\cmidrule(lr){2-18}
 & eq & lam & $1.742$ & $1.595$ & \cellcolor{posgreen!50}$+0.147$ & $2.149$ & $2.418$ & \cellcolor{negred!50}$-0.269$ & $1.944$ & $1.914$ & \cellcolor{posgreen!50}$+0.030$ & $1.784$ & $1.051$ & \cellcolor{posgreen!50}$+0.733$ & $0.648$ & $0.640$ & \cellcolor{posgreen!50}$+0.007$ \\
 &  & raw & $1.796$ & $1.663$ & \cellcolor{posgreen!50}$+0.133$ & $2.174$ & $2.417$ & \cellcolor{negred!50}$-0.243$ & $1.998$ & $2.036$ & \cellcolor{negred!50}$-0.038$ & $1.805$ & $1.069$ & \cellcolor{posgreen!50}$+0.736$ & $0.648$ & $0.640$ & \cellcolor{posgreen!50}$+0.007$ \\
 &  & inv & $1.272$ & $1.311$ & \cellcolor{negred!50}$-0.039$ & $2.538$ & $2.951$ & \cellcolor{negred!50}$-0.414$ & $1.531$ & $1.538$ & \cellcolor{negred!50}$-0.007$ & $0.921$ & $0.881$ & \cellcolor{posgreen!50}$+0.040$ & $0.709$ & $0.675$ & \cellcolor{posgreen!50}$+0.034$ \\
 &  & vsp & $1.367$ & $1.378$ & \cellcolor{negred!50}$-0.011$ & $2.373$ & $2.572$ & \cellcolor{negred!50}$-0.199$ & $1.597$ & $1.597$ & $-0.000$ & $1.022$ & $0.945$ & \cellcolor{posgreen!50}$+0.077$ & $0.631$ & $0.664$ & \cellcolor{negred!50}$-0.033$ \\
 &  & fpm & $1.098$ & $1.183$ & \cellcolor{negred!50}$-0.085$ & $1.862$ & $2.395$ & \cellcolor{negred!50}$-0.533$ & $1.530$ & $1.383$ & \cellcolor{posgreen!50}$+0.147$ & $0.886$ & $1.010$ & \cellcolor{negred!50}$-0.124$ & $0.512$ & $0.584$ & \cellcolor{negred!50}$-0.073$ \\
\cmidrule(lr){2-18}
 & rp & lam & $1.727$ & $1.599$ & \cellcolor{posgreen!50}$+0.128$ & $2.532$ & $2.719$ & \cellcolor{negred!50}$-0.187$ & $1.927$ & $1.897$ & \cellcolor{posgreen!50}$+0.030$ & $1.616$ & $0.943$ & \cellcolor{posgreen!50}$+0.673$ & $0.553$ & $0.586$ & \cellcolor{negred!50}$-0.034$ \\
 &  & raw & $1.763$ & $1.675$ & \cellcolor{posgreen!50}$+0.088$ & $2.540$ & $2.717$ & \cellcolor{negred!50}$-0.177$ & $1.953$ & $2.027$ & \cellcolor{negred!50}$-0.075$ & $1.631$ & $0.966$ & \cellcolor{posgreen!50}$+0.665$ & $0.553$ & $0.586$ & \cellcolor{negred!50}$-0.034$ \\
 &  & inv & $1.263$ & $1.325$ & \cellcolor{negred!50}$-0.062$ & $2.577$ & $3.045$ & \cellcolor{negred!50}$-0.469$ & $1.527$ & $1.565$ & \cellcolor{negred!50}$-0.038$ & $0.906$ & $0.886$ & \cellcolor{posgreen!50}$+0.020$ & $0.590$ & $0.542$ & \cellcolor{posgreen!50}$+0.048$ \\
 &  & vsp & $1.377$ & $1.388$ & \cellcolor{negred!50}$-0.011$ & $2.585$ & $2.885$ & \cellcolor{negred!50}$-0.299$ & $1.603$ & $1.582$ & \cellcolor{posgreen!50}$+0.021$ & $1.045$ & $0.922$ & \cellcolor{posgreen!50}$+0.123$ & $0.525$ & $0.516$ & \cellcolor{posgreen!50}$+0.009$ \\
 &  & fpm & $1.122$ & $1.215$ & \cellcolor{negred!50}$-0.093$ & $2.204$ & $2.680$ & \cellcolor{negred!50}$-0.476$ & $1.535$ & $1.431$ & \cellcolor{posgreen!50}$+0.104$ & $0.892$ & $1.006$ & \cellcolor{negred!50}$-0.114$ & $0.428$ & $0.519$ & \cellcolor{negred!50}$-0.091$ \\
\midrule
eq & mcap & lam & $1.655$ & $1.572$ & \cellcolor{posgreen!50}$+0.083$ & $1.764$ & $1.867$ & \cellcolor{negred!50}$-0.103$ & $2.124$ & $2.092$ & \cellcolor{posgreen!50}$+0.032$ & $1.134$ & $0.863$ & \cellcolor{posgreen!50}$+0.270$ & $0.805$ & $0.768$ & \cellcolor{posgreen!50}$+0.037$ \\
 &  & raw & $1.670$ & $1.606$ & \cellcolor{posgreen!50}$+0.064$ & $1.796$ & $1.892$ & \cellcolor{negred!50}$-0.097$ & $2.097$ & $2.107$ & \cellcolor{negred!50}$-0.010$ & $1.146$ & $0.872$ & \cellcolor{posgreen!50}$+0.274$ & $0.805$ & $0.768$ & \cellcolor{posgreen!50}$+0.037$ \\
 &  & inv & $1.481$ & $1.444$ & \cellcolor{posgreen!50}$+0.037$ & $2.057$ & $2.049$ & \cellcolor{posgreen!50}$+0.007$ & $1.730$ & $1.738$ & \cellcolor{negred!50}$-0.008$ & $1.051$ & $0.963$ & \cellcolor{posgreen!50}$+0.088$ & $1.332$ & $1.214$ & \cellcolor{posgreen!50}$+0.118$ \\
 &  & vsp & $1.528$ & $1.487$ & \cellcolor{posgreen!50}$+0.041$ & $1.844$ & $1.849$ & \cellcolor{negred!50}$-0.005$ & $1.858$ & $1.765$ & \cellcolor{posgreen!50}$+0.092$ & $1.001$ & $1.003$ & \cellcolor{negred!50}$-0.002$ & $1.301$ & $1.210$ & \cellcolor{posgreen!50}$+0.091$ \\
 &  & fpm & $1.451$ & $1.548$ & \cellcolor{negred!50}$-0.097$ & $1.378$ & $1.618$ & \cellcolor{negred!50}$-0.240$ & $1.819$ & $1.889$ & \cellcolor{negred!50}$-0.070$ & $1.050$ & $1.088$ & \cellcolor{negred!50}$-0.039$ & $1.531$ & $1.653$ & \cellcolor{negred!50}$-0.123$ \\
\cmidrule(lr){2-18}
 & eq & lam & $1.637$ & $1.608$ & \cellcolor{posgreen!50}$+0.029$ & $2.268$ & $2.264$ & \cellcolor{posgreen!50}$+0.004$ & $2.048$ & $2.087$ & \cellcolor{negred!50}$-0.038$ & $1.175$ & $0.945$ & \cellcolor{posgreen!50}$+0.230$ & $0.384$ & $0.406$ & \cellcolor{negred!50}$-0.022$ \\
 &  & raw & $1.673$ & $1.627$ & \cellcolor{posgreen!50}$+0.046$ & $2.316$ & $2.282$ & \cellcolor{posgreen!50}$+0.033$ & $2.069$ & $2.088$ & \cellcolor{negred!50}$-0.019$ & $1.196$ & $0.964$ & \cellcolor{posgreen!50}$+0.232$ & $0.384$ & $0.406$ & \cellcolor{negred!50}$-0.022$ \\
 &  & inv & $1.319$ & $1.309$ & \cellcolor{posgreen!50}$+0.010$ & $2.278$ & $2.291$ & \cellcolor{negred!50}$-0.013$ & $1.776$ & $1.685$ & \cellcolor{posgreen!50}$+0.091$ & $0.902$ & $0.873$ & \cellcolor{posgreen!50}$+0.029$ & $0.605$ & $0.622$ & \cellcolor{negred!50}$-0.016$ \\
 &  & vsp & $1.390$ & $1.406$ & \cellcolor{negred!50}$-0.016$ & $2.336$ & $2.329$ & \cellcolor{posgreen!50}$+0.006$ & $1.931$ & $1.804$ & \cellcolor{posgreen!50}$+0.127$ & $0.765$ & $0.879$ & \cellcolor{negred!50}$-0.115$ & $0.513$ & $0.591$ & \cellcolor{negred!50}$-0.078$ \\
 &  & fpm & $1.401$ & $1.556$ & \cellcolor{negred!50}$-0.156$ & $1.961$ & $2.166$ & \cellcolor{negred!50}$-0.205$ & $1.833$ & $2.046$ & \cellcolor{negred!50}$-0.213$ & $0.948$ & $1.106$ & \cellcolor{negred!50}$-0.158$ & $0.515$ & $0.682$ & \cellcolor{negred!50}$-0.167$ \\
\cmidrule(lr){2-18}
 & rp & lam & $1.624$ & $1.575$ & \cellcolor{posgreen!50}$+0.048$ & $2.383$ & $2.519$ & \cellcolor{negred!50}$-0.136$ & $2.036$ & $2.002$ & \cellcolor{posgreen!50}$+0.034$ & $1.095$ & $0.835$ & \cellcolor{posgreen!50}$+0.260$ & $0.342$ & $0.394$ & \cellcolor{negred!50}$-0.052$ \\
 &  & raw & $1.661$ & $1.592$ & \cellcolor{posgreen!50}$+0.068$ & $2.395$ & $2.526$ & \cellcolor{negred!50}$-0.131$ & $2.084$ & $1.993$ & \cellcolor{posgreen!50}$+0.091$ & $1.109$ & $0.850$ & \cellcolor{posgreen!50}$+0.259$ & $0.342$ & $0.394$ & \cellcolor{negred!50}$-0.052$ \\
 &  & inv & $1.307$ & $1.304$ & \cellcolor{posgreen!50}$+0.002$ & $2.294$ & $2.263$ & \cellcolor{posgreen!50}$+0.031$ & $1.757$ & $1.682$ & \cellcolor{posgreen!50}$+0.075$ & $0.860$ & $0.835$ & \cellcolor{posgreen!50}$+0.025$ & $0.512$ & $0.585$ & \cellcolor{negred!50}$-0.072$ \\
 &  & vsp & $1.407$ & $1.415$ & \cellcolor{negred!50}$-0.008$ & $2.368$ & $2.532$ & \cellcolor{negred!50}$-0.164$ & $1.947$ & $1.816$ & \cellcolor{posgreen!50}$+0.131$ & $0.789$ & $0.838$ & \cellcolor{negred!50}$-0.049$ & $0.448$ & $0.549$ & \cellcolor{negred!50}$-0.101$ \\
 &  & fpm & $1.420$ & $1.557$ & \cellcolor{negred!50}$-0.136$ & $2.069$ & $2.320$ & \cellcolor{negred!50}$-0.251$ & $1.835$ & $2.033$ & \cellcolor{negred!50}$-0.198$ & $0.951$ & $1.054$ & \cellcolor{negred!50}$-0.103$ & $0.427$ & $0.590$ & \cellcolor{negred!50}$-0.163$ \\
\midrule
rp & mcap & lam & $1.625$ & $1.407$ & \cellcolor{posgreen!50}$+0.218$ & $1.814$ & $1.237$ & \cellcolor{posgreen!50}$+0.577$ & $2.010$ & $2.034$ & \cellcolor{negred!50}$-0.023$ & $1.196$ & $0.883$ & \cellcolor{posgreen!50}$+0.313$ & $0.855$ & $0.802$ & \cellcolor{posgreen!50}$+0.053$ \\
 &  & raw & $1.683$ & $1.473$ & \cellcolor{posgreen!50}$+0.210$ & $1.817$ & $1.250$ & \cellcolor{posgreen!50}$+0.567$ & $2.101$ & $2.129$ & \cellcolor{negred!50}$-0.027$ & $1.213$ & $0.935$ & \cellcolor{posgreen!50}$+0.278$ & $0.855$ & $0.802$ & \cellcolor{posgreen!50}$+0.053$ \\
 &  & inv & $1.489$ & $1.305$ & \cellcolor{posgreen!50}$+0.184$ & $2.194$ & $1.083$ & \cellcolor{posgreen!50}$+1.112$ & $1.692$ & $1.724$ & \cellcolor{negred!50}$-0.031$ & $1.087$ & $0.981$ & \cellcolor{posgreen!50}$+0.106$ & $1.402$ & $1.266$ & \cellcolor{posgreen!50}$+0.136$ \\
 &  & vsp & $1.520$ & $1.371$ & \cellcolor{posgreen!50}$+0.149$ & $1.943$ & $1.215$ & \cellcolor{posgreen!50}$+0.728$ & $1.770$ & $1.765$ & \cellcolor{posgreen!50}$+0.005$ & $1.021$ & $1.021$ & $+0.000$ & $1.342$ & $1.256$ & \cellcolor{posgreen!50}$+0.086$ \\
 &  & fpm & $1.421$ & $1.360$ & \cellcolor{posgreen!50}$+0.061$ & $1.400$ & $1.026$ & \cellcolor{posgreen!50}$+0.374$ & $1.763$ & $1.869$ & \cellcolor{negred!50}$-0.106$ & $1.043$ & $1.100$ & \cellcolor{negred!50}$-0.057$ & $1.568$ & $1.627$ & \cellcolor{negred!50}$-0.060$ \\
\cmidrule(lr){2-18}
 & eq & lam & $1.647$ & $1.488$ & \cellcolor{posgreen!50}$+0.159$ & $2.335$ & $1.578$ & \cellcolor{posgreen!50}$+0.756$ & $1.985$ & $2.018$ & \cellcolor{negred!50}$-0.033$ & $1.287$ & $1.015$ & \cellcolor{posgreen!50}$+0.272$ & $0.443$ & $0.484$ & \cellcolor{negred!50}$-0.041$ \\
 &  & raw & $1.708$ & $1.530$ & \cellcolor{posgreen!50}$+0.178$ & $2.350$ & $1.605$ & \cellcolor{posgreen!50}$+0.746$ & $2.065$ & $2.047$ & \cellcolor{posgreen!50}$+0.018$ & $1.312$ & $1.045$ & \cellcolor{posgreen!50}$+0.268$ & $0.443$ & $0.484$ & \cellcolor{negred!50}$-0.041$ \\
 &  & inv & $1.316$ & $1.210$ & \cellcolor{posgreen!50}$+0.106$ & $2.447$ & $1.224$ & \cellcolor{posgreen!50}$+1.222$ & $1.656$ & $1.645$ & \cellcolor{posgreen!50}$+0.012$ & $0.934$ & $0.875$ & \cellcolor{posgreen!50}$+0.059$ & $0.614$ & $0.636$ & \cellcolor{negred!50}$-0.022$ \\
 &  & vsp & $1.360$ & $1.298$ & \cellcolor{posgreen!50}$+0.062$ & $2.436$ & $1.477$ & \cellcolor{posgreen!50}$+0.959$ & $1.807$ & $1.765$ & \cellcolor{posgreen!50}$+0.042$ & $0.755$ & $0.891$ & \cellcolor{negred!50}$-0.136$ & $0.513$ & $0.598$ & \cellcolor{negred!50}$-0.085$ \\
 &  & fpm & $1.394$ & $1.402$ & \cellcolor{negred!50}$-0.008$ & $2.102$ & $1.323$ & \cellcolor{posgreen!50}$+0.778$ & $1.815$ & $2.007$ & \cellcolor{negred!50}$-0.192$ & $0.929$ & $1.109$ & \cellcolor{negred!50}$-0.180$ & $0.484$ & $0.689$ & \cellcolor{negred!50}$-0.205$ \\
\cmidrule(lr){2-18}
 & rp & lam & $1.612$ & $1.484$ & \cellcolor{posgreen!50}$+0.127$ & $2.476$ & $1.708$ & \cellcolor{posgreen!50}$+0.768$ & $1.955$ & $1.979$ & \cellcolor{negred!50}$-0.024$ & $1.140$ & $0.902$ & \cellcolor{posgreen!50}$+0.238$ & $0.351$ & $0.447$ & \cellcolor{negred!50}$-0.096$ \\
 &  & raw & $1.672$ & $1.532$ & \cellcolor{posgreen!50}$+0.140$ & $2.501$ & $1.742$ & \cellcolor{posgreen!50}$+0.758$ & $2.045$ & $2.028$ & \cellcolor{posgreen!50}$+0.017$ & $1.157$ & $0.924$ & \cellcolor{posgreen!50}$+0.233$ & $0.351$ & $0.447$ & \cellcolor{negred!50}$-0.096$ \\
 &  & inv & $1.295$ & $1.222$ & \cellcolor{posgreen!50}$+0.073$ & $2.231$ & $1.310$ & \cellcolor{posgreen!50}$+0.921$ & $1.673$ & $1.661$ & \cellcolor{posgreen!50}$+0.011$ & $0.883$ & $0.846$ & \cellcolor{posgreen!50}$+0.037$ & $0.533$ & $0.608$ & \cellcolor{negred!50}$-0.075$ \\
 &  & vsp & $1.363$ & $1.334$ & \cellcolor{posgreen!50}$+0.029$ & $2.458$ & $1.623$ & \cellcolor{posgreen!50}$+0.835$ & $1.820$ & $1.779$ & \cellcolor{posgreen!50}$+0.041$ & $0.746$ & $0.865$ & \cellcolor{negred!50}$-0.119$ & $0.452$ & $0.565$ & \cellcolor{negred!50}$-0.113$ \\
 &  & fpm & $1.420$ & $1.434$ & \cellcolor{negred!50}$-0.014$ & $2.040$ & $1.415$ & \cellcolor{posgreen!50}$+0.626$ & $1.840$ & $2.030$ & \cellcolor{negred!50}$-0.190$ & $0.930$ & $1.089$ & \cellcolor{negred!50}$-0.159$ & $0.393$ & $0.584$ & \cellcolor{negred!50}$-0.191$ \\
\bottomrule
\end{tabular}}
\end{table}
```

## MDD — $\omega=$he

```latex
% NOTE: 표가 페이지 폭을 넘으면 paper3.md 프리앰블에 \usepackage{pdflscape}를 추가하고
%       \begin{landscape} ... \end{landscape}로 표 전체를 감싸 가로 회전하시기 바랍니다.
\begin{table}[!htbp]
\centering
\caption{전체 45 슬롯 최대낙폭 (MDD) 결과 ($\Omega=$he 고정). $p_w \times \text{prior} \times q$ = $3 \times 3 \times 5$ = 45 슬롯 각각의 LSTM(L)·ANN(A) 최대낙폭 (MDD) 및 차이 $\Delta = \mathrm{L} - \mathrm{A}$를 5개 구간(All, R1 회복, R2 확장, R3 위기, R4 AI 랠리)에 대해 보고한다. MDD는 음수가 손실이므로 $\Delta > 0$이 LSTM이 덜 빠진 경우이다.}
\label{tab:app_grid_mdd_he}
\setlength{\tabcolsep}{2pt}
\renewcommand{\arraystretch}{1.05}
\scriptsize
\resizebox{\textwidth}{!}{%
\begin{tabular}{lll ccc ccc ccc ccc ccc}
\toprule
 & & & \multicolumn{3}{c}{All} & \multicolumn{3}{c}{R1} & \multicolumn{3}{c}{R2} & \multicolumn{3}{c}{R3} & \multicolumn{3}{c}{R4} \\
\cmidrule(lr){4-6} \cmidrule(lr){7-9} \cmidrule(lr){10-12} \cmidrule(lr){13-15} \cmidrule(lr){16-18}
$p_w$ & prior & $q$ & L & A & $\Delta$ & L & A & $\Delta$ & L & A & $\Delta$ & L & A & $\Delta$ & L & A & $\Delta$ \\
\midrule
mcap & mcap & lam & $-11.65\%$ & $-13.81\%$ & \cellcolor{posgreen!50}$+2.16\%$ & $-10.74\%$ & $-10.37\%$ & \cellcolor{negred!50}$-0.38\%$ & $-11.65\%$ & $-11.33\%$ & \cellcolor{negred!50}$-0.32\%$ & $-10.05\%$ & $-13.81\%$ & \cellcolor{posgreen!50}$+3.77\%$ & $-4.91\%$ & $-5.91\%$ & \cellcolor{posgreen!50}$+1.00\%$ \\
 &  & raw & $-13.69\%$ & $-13.81\%$ & \cellcolor{posgreen!50}$+0.12\%$ & $-10.79\%$ & $-10.45\%$ & \cellcolor{negred!50}$-0.34\%$ & $-13.69\%$ & $-13.45\%$ & \cellcolor{negred!50}$-0.24\%$ & $-10.05\%$ & $-13.81\%$ & \cellcolor{posgreen!50}$+3.77\%$ & $-4.91\%$ & $-5.91\%$ & \cellcolor{posgreen!50}$+1.00\%$ \\
 &  & inv & $-14.76\%$ & $-15.37\%$ & \cellcolor{posgreen!50}$+0.61\%$ & $-7.43\%$ & $-7.13\%$ & \cellcolor{negred!50}$-0.30\%$ & $-11.76\%$ & $-12.87\%$ & \cellcolor{posgreen!50}$+1.11\%$ & $-13.39\%$ & $-15.37\%$ & \cellcolor{posgreen!50}$+1.98\%$ & $-5.31\%$ & $-7.17\%$ & \cellcolor{posgreen!50}$+1.86\%$ \\
 &  & vsp & $-12.73\%$ & $-14.35\%$ & \cellcolor{posgreen!50}$+1.63\%$ & $-9.54\%$ & $-9.26\%$ & \cellcolor{negred!50}$-0.28\%$ & $-9.46\%$ & $-11.42\%$ & \cellcolor{posgreen!50}$+1.96\%$ & $-12.48\%$ & $-14.35\%$ & \cellcolor{posgreen!50}$+1.87\%$ & $-5.19\%$ & $-7.19\%$ & \cellcolor{posgreen!50}$+2.01\%$ \\
 &  & fpm & $-19.84\%$ & $-18.91\%$ & \cellcolor{negred!50}$-0.92\%$ & $-11.90\%$ & $-10.47\%$ & \cellcolor{negred!50}$-1.43\%$ & $-16.60\%$ & $-12.84\%$ & \cellcolor{negred!50}$-3.76\%$ & $-19.84\%$ & $-15.17\%$ & \cellcolor{negred!50}$-4.66\%$ & $-18.74\%$ & $-18.91\%$ & \cellcolor{posgreen!50}$+0.17\%$ \\
\cmidrule(lr){2-18}
 & eq & lam & $-12.18\%$ & $-13.01\%$ & \cellcolor{posgreen!50}$+0.83\%$ & $-12.18\%$ & $-11.51\%$ & \cellcolor{negred!50}$-0.66\%$ & $-11.50\%$ & $-12.09\%$ & \cellcolor{posgreen!50}$+0.59\%$ & $-9.79\%$ & $-13.01\%$ & \cellcolor{posgreen!50}$+3.22\%$ & $-6.83\%$ & $-7.18\%$ & \cellcolor{posgreen!50}$+0.35\%$ \\
 &  & raw & $-14.19\%$ & $-14.05\%$ & \cellcolor{negred!50}$-0.14\%$ & $-12.18\%$ & $-11.51\%$ & \cellcolor{negred!50}$-0.66\%$ & $-14.19\%$ & $-14.05\%$ & \cellcolor{negred!50}$-0.14\%$ & $-9.79\%$ & $-13.01\%$ & \cellcolor{posgreen!50}$+3.22\%$ & $-6.83\%$ & $-7.18\%$ & \cellcolor{posgreen!50}$+0.35\%$ \\
 &  & inv & $-18.88\%$ & $-17.89\%$ & \cellcolor{negred!50}$-0.98\%$ & $-7.57\%$ & $-6.31\%$ & \cellcolor{negred!50}$-1.26\%$ & $-12.18\%$ & $-12.44\%$ & \cellcolor{posgreen!50}$+0.26\%$ & $-13.28\%$ & $-14.77\%$ & \cellcolor{posgreen!50}$+1.49\%$ & $-8.64\%$ & $-9.33\%$ & \cellcolor{posgreen!50}$+0.69\%$ \\
 &  & vsp & $-15.65\%$ & $-15.12\%$ & \cellcolor{negred!50}$-0.52\%$ & $-10.31\%$ & $-10.00\%$ & \cellcolor{negred!50}$-0.31\%$ & $-9.79\%$ & $-11.03\%$ & \cellcolor{posgreen!50}$+1.24\%$ & $-11.97\%$ & $-14.35\%$ & \cellcolor{posgreen!50}$+2.38\%$ & $-8.29\%$ & $-9.19\%$ & \cellcolor{posgreen!50}$+0.89\%$ \\
 &  & fpm & $-24.34\%$ & $-19.65\%$ & \cellcolor{negred!50}$-4.69\%$ & $-12.73\%$ & $-10.07\%$ & \cellcolor{negred!50}$-2.66\%$ & $-17.61\%$ & $-12.58\%$ & \cellcolor{negred!50}$-5.04\%$ & $-19.41\%$ & $-14.22\%$ & \cellcolor{negred!50}$-5.20\%$ & $-20.34\%$ & $-19.65\%$ & \cellcolor{negred!50}$-0.69\%$ \\
\cmidrule(lr){2-18}
 & rp & lam & $-12.56\%$ & $-12.65\%$ & \cellcolor{posgreen!50}$+0.09\%$ & $-10.44\%$ & $-9.77\%$ & \cellcolor{negred!50}$-0.67\%$ & $-11.70\%$ & $-12.65\%$ & \cellcolor{posgreen!50}$+0.95\%$ & $-10.15\%$ & $-12.24\%$ & \cellcolor{posgreen!50}$+2.09\%$ & $-6.81\%$ & $-6.84\%$ & $+0.03\%$ \\
 &  & raw & $-14.37\%$ & $-13.81\%$ & \cellcolor{negred!50}$-0.56\%$ & $-10.44\%$ & $-9.77\%$ & \cellcolor{negred!50}$-0.67\%$ & $-14.37\%$ & $-13.81\%$ & \cellcolor{negred!50}$-0.56\%$ & $-10.15\%$ & $-12.24\%$ & \cellcolor{posgreen!50}$+2.09\%$ & $-6.81\%$ & $-6.84\%$ & $+0.03\%$ \\
 &  & inv & $-17.57\%$ & $-16.73\%$ & \cellcolor{negred!50}$-0.84\%$ & $-6.56\%$ & $-5.56\%$ & \cellcolor{negred!50}$-1.00\%$ & $-11.78\%$ & $-11.81\%$ & $+0.04\%$ & $-12.56\%$ & $-14.13\%$ & \cellcolor{posgreen!50}$+1.57\%$ & $-7.58\%$ & $-8.31\%$ & \cellcolor{posgreen!50}$+0.73\%$ \\
 &  & vsp & $-14.51\%$ & $-14.19\%$ & \cellcolor{negred!50}$-0.33\%$ & $-8.69\%$ & $-8.24\%$ & \cellcolor{negred!50}$-0.45\%$ & $-9.46\%$ & $-10.57\%$ & \cellcolor{posgreen!50}$+1.11\%$ & $-11.40\%$ & $-13.84\%$ & \cellcolor{posgreen!50}$+2.44\%$ & $-7.40\%$ & $-8.24\%$ & \cellcolor{posgreen!50}$+0.84\%$ \\
 &  & fpm & $-22.39\%$ & $-19.01\%$ & \cellcolor{negred!50}$-3.38\%$ & $-10.85\%$ & $-8.38\%$ & \cellcolor{negred!50}$-2.47\%$ & $-16.89\%$ & $-11.93\%$ & \cellcolor{negred!50}$-4.97\%$ & $-17.57\%$ & $-13.43\%$ & \cellcolor{negred!50}$-4.14\%$ & $-19.62\%$ & $-19.01\%$ & \cellcolor{negred!50}$-0.60\%$ \\
\midrule
eq & mcap & lam & $-12.82\%$ & $-14.16\%$ & \cellcolor{posgreen!50}$+1.34\%$ & $-9.97\%$ & $-10.51\%$ & \cellcolor{posgreen!50}$+0.53\%$ & $-12.82\%$ & $-13.37\%$ & \cellcolor{posgreen!50}$+0.55\%$ & $-10.99\%$ & $-14.16\%$ & \cellcolor{posgreen!50}$+3.17\%$ & $-5.35\%$ & $-5.12\%$ & \cellcolor{negred!50}$-0.23\%$ \\
 &  & raw & $-15.16\%$ & $-15.46\%$ & \cellcolor{posgreen!50}$+0.30\%$ & $-9.97\%$ & $-10.51\%$ & \cellcolor{posgreen!50}$+0.53\%$ & $-15.16\%$ & $-15.46\%$ & \cellcolor{posgreen!50}$+0.30\%$ & $-10.99\%$ & $-14.16\%$ & \cellcolor{posgreen!50}$+3.17\%$ & $-5.35\%$ & $-5.12\%$ & \cellcolor{negred!50}$-0.23\%$ \\
 &  & inv & $-14.46\%$ & $-16.41\%$ & \cellcolor{posgreen!50}$+1.95\%$ & $-5.95\%$ & $-6.25\%$ & \cellcolor{posgreen!50}$+0.30\%$ & $-10.81\%$ & $-11.45\%$ & \cellcolor{posgreen!50}$+0.63\%$ & $-14.46\%$ & $-16.41\%$ & \cellcolor{posgreen!50}$+1.95\%$ & $-5.23\%$ & $-4.79\%$ & \cellcolor{negred!50}$-0.44\%$ \\
 &  & vsp & $-12.64\%$ & $-15.47\%$ & \cellcolor{posgreen!50}$+2.83\%$ & $-8.56\%$ & $-8.84\%$ & \cellcolor{posgreen!50}$+0.28\%$ & $-8.70\%$ & $-9.39\%$ & \cellcolor{posgreen!50}$+0.69\%$ & $-12.64\%$ & $-15.47\%$ & \cellcolor{posgreen!50}$+2.83\%$ & $-5.37\%$ & $-4.94\%$ & \cellcolor{negred!50}$-0.43\%$ \\
 &  & fpm & $-16.01\%$ & $-15.84\%$ & \cellcolor{negred!50}$-0.16\%$ & $-13.82\%$ & $-11.96\%$ & \cellcolor{negred!50}$-1.85\%$ & $-10.22\%$ & $-8.53\%$ & \cellcolor{negred!50}$-1.69\%$ & $-16.01\%$ & $-15.84\%$ & \cellcolor{negred!50}$-0.16\%$ & $-7.44\%$ & $-7.60\%$ & \cellcolor{posgreen!50}$+0.16\%$ \\
\cmidrule(lr){2-18}
 & eq & lam & $-13.31\%$ & $-13.52\%$ & \cellcolor{posgreen!50}$+0.20\%$ & $-10.36\%$ & $-10.46\%$ & \cellcolor{posgreen!50}$+0.10\%$ & $-13.31\%$ & $-13.52\%$ & \cellcolor{posgreen!50}$+0.20\%$ & $-10.46\%$ & $-12.41\%$ & \cellcolor{posgreen!50}$+1.95\%$ & $-7.06\%$ & $-6.78\%$ & \cellcolor{negred!50}$-0.28\%$ \\
 &  & raw & $-15.11\%$ & $-15.54\%$ & \cellcolor{posgreen!50}$+0.44\%$ & $-10.36\%$ & $-10.46\%$ & \cellcolor{posgreen!50}$+0.10\%$ & $-15.11\%$ & $-15.54\%$ & \cellcolor{posgreen!50}$+0.44\%$ & $-10.46\%$ & $-12.41\%$ & \cellcolor{posgreen!50}$+1.95\%$ & $-7.06\%$ & $-6.78\%$ & \cellcolor{negred!50}$-0.28\%$ \\
 &  & inv & $-16.87\%$ & $-16.79\%$ & \cellcolor{negred!50}$-0.08\%$ & $-5.80\%$ & $-5.79\%$ & $-0.01\%$ & $-10.57\%$ & $-11.07\%$ & \cellcolor{posgreen!50}$+0.51\%$ & $-13.23\%$ & $-14.15\%$ & \cellcolor{posgreen!50}$+0.92\%$ & $-7.37\%$ & $-6.81\%$ & \cellcolor{negred!50}$-0.55\%$ \\
 &  & vsp & $-14.20\%$ & $-14.57\%$ & \cellcolor{posgreen!50}$+0.36\%$ & $-8.24\%$ & $-8.81\%$ & \cellcolor{posgreen!50}$+0.57\%$ & $-8.59\%$ & $-9.19\%$ & \cellcolor{posgreen!50}$+0.60\%$ & $-12.71\%$ & $-13.75\%$ & \cellcolor{posgreen!50}$+1.04\%$ & $-7.59\%$ & $-7.07\%$ & \cellcolor{negred!50}$-0.52\%$ \\
 &  & fpm & $-14.26\%$ & $-13.59\%$ & \cellcolor{negred!50}$-0.68\%$ & $-12.43\%$ & $-11.48\%$ & \cellcolor{negred!50}$-0.95\%$ & $-9.84\%$ & $-8.23\%$ & \cellcolor{negred!50}$-1.61\%$ & $-13.84\%$ & $-13.59\%$ & \cellcolor{negred!50}$-0.25\%$ & $-9.03\%$ & $-9.18\%$ & \cellcolor{posgreen!50}$+0.15\%$ \\
\cmidrule(lr){2-18}
 & rp & lam & $-13.34\%$ & $-13.51\%$ & \cellcolor{posgreen!50}$+0.17\%$ & $-8.96\%$ & $-8.82\%$ & \cellcolor{negred!50}$-0.14\%$ & $-13.34\%$ & $-13.51\%$ & \cellcolor{posgreen!50}$+0.17\%$ & $-9.81\%$ & $-11.88\%$ & \cellcolor{posgreen!50}$+2.07\%$ & $-6.76\%$ & $-6.75\%$ & $-0.02\%$ \\
 &  & raw & $-15.07\%$ & $-15.53\%$ & \cellcolor{posgreen!50}$+0.46\%$ & $-8.96\%$ & $-8.82\%$ & \cellcolor{negred!50}$-0.14\%$ & $-15.07\%$ & $-15.53\%$ & \cellcolor{posgreen!50}$+0.46\%$ & $-9.81\%$ & $-11.88\%$ & \cellcolor{posgreen!50}$+2.07\%$ & $-6.76\%$ & $-6.75\%$ & $-0.02\%$ \\
 &  & inv & $-16.28\%$ & $-16.10\%$ & \cellcolor{negred!50}$-0.18\%$ & $-5.46\%$ & $-5.62\%$ & \cellcolor{posgreen!50}$+0.15\%$ & $-10.16\%$ & $-10.61\%$ & \cellcolor{posgreen!50}$+0.45\%$ & $-12.86\%$ & $-13.45\%$ & \cellcolor{posgreen!50}$+0.60\%$ & $-6.90\%$ & $-6.68\%$ & \cellcolor{negred!50}$-0.23\%$ \\
 &  & vsp & $-13.47\%$ & $-13.90\%$ & \cellcolor{posgreen!50}$+0.43\%$ & $-7.02\%$ & $-7.11\%$ & \cellcolor{posgreen!50}$+0.09\%$ & $-8.30\%$ & $-8.87\%$ & \cellcolor{posgreen!50}$+0.57\%$ & $-12.03\%$ & $-13.04\%$ & \cellcolor{posgreen!50}$+1.02\%$ & $-7.06\%$ & $-6.67\%$ & \cellcolor{negred!50}$-0.40\%$ \\
 &  & fpm & $-14.32\%$ & $-12.87\%$ & \cellcolor{negred!50}$-1.45\%$ & $-11.06\%$ & $-9.91\%$ & \cellcolor{negred!50}$-1.15\%$ & $-9.48\%$ & $-8.15\%$ & \cellcolor{negred!50}$-1.33\%$ & $-13.39\%$ & $-12.87\%$ & \cellcolor{negred!50}$-0.51\%$ & $-8.51\%$ & $-8.61\%$ & \cellcolor{posgreen!50}$+0.10\%$ \\
\midrule
rp & mcap & lam & $-11.87\%$ & $-14.19\%$ & \cellcolor{posgreen!50}$+2.32\%$ & $-11.87\%$ & $-14.19\%$ & \cellcolor{posgreen!50}$+2.32\%$ & $-11.64\%$ & $-11.84\%$ & \cellcolor{posgreen!50}$+0.20\%$ & $-11.06\%$ & $-13.94\%$ & \cellcolor{posgreen!50}$+2.87\%$ & $-5.25\%$ & $-4.96\%$ & \cellcolor{negred!50}$-0.29\%$ \\
 &  & raw & $-13.78\%$ & $-14.68\%$ & \cellcolor{posgreen!50}$+0.90\%$ & $-11.87\%$ & $-14.19\%$ & \cellcolor{posgreen!50}$+2.32\%$ & $-13.78\%$ & $-14.68\%$ & \cellcolor{posgreen!50}$+0.90\%$ & $-11.06\%$ & $-13.94\%$ & \cellcolor{posgreen!50}$+2.87\%$ & $-5.25\%$ & $-4.96\%$ & \cellcolor{negred!50}$-0.29\%$ \\
 &  & inv & $-14.61\%$ & $-16.25\%$ & \cellcolor{posgreen!50}$+1.64\%$ & $-6.36\%$ & $-13.99\%$ & \cellcolor{posgreen!50}$+7.63\%$ & $-11.85\%$ & $-12.03\%$ & \cellcolor{posgreen!50}$+0.18\%$ & $-14.61\%$ & $-16.25\%$ & \cellcolor{posgreen!50}$+1.64\%$ & $-5.12\%$ & $-4.84\%$ & \cellcolor{negred!50}$-0.28\%$ \\
 &  & vsp & $-12.88\%$ & $-15.39\%$ & \cellcolor{posgreen!50}$+2.51\%$ & $-9.51\%$ & $-14.09\%$ & \cellcolor{posgreen!50}$+4.58\%$ & $-9.18\%$ & $-9.63\%$ & \cellcolor{posgreen!50}$+0.45\%$ & $-12.88\%$ & $-15.39\%$ & \cellcolor{posgreen!50}$+2.51\%$ & $-5.19\%$ & $-4.93\%$ & \cellcolor{negred!50}$-0.26\%$ \\
 &  & fpm & $-16.24\%$ & $-15.66\%$ & \cellcolor{negred!50}$-0.58\%$ & $-16.24\%$ & $-13.81\%$ & \cellcolor{negred!50}$-2.43\%$ & $-10.49\%$ & $-8.54\%$ & \cellcolor{negred!50}$-1.95\%$ & $-15.93\%$ & $-15.66\%$ & \cellcolor{negred!50}$-0.27\%$ & $-7.60\%$ & $-7.51\%$ & \cellcolor{negred!50}$-0.09\%$ \\
\cmidrule(lr){2-18}
 & eq & lam & $-12.42\%$ & $-13.57\%$ & \cellcolor{posgreen!50}$+1.15\%$ & $-11.30\%$ & $-13.57\%$ & \cellcolor{posgreen!50}$+2.27\%$ & $-12.39\%$ & $-12.11\%$ & \cellcolor{negred!50}$-0.28\%$ & $-10.43\%$ & $-12.10\%$ & \cellcolor{posgreen!50}$+1.66\%$ & $-6.96\%$ & $-6.82\%$ & \cellcolor{negred!50}$-0.14\%$ \\
 &  & raw & $-14.16\%$ & $-14.63\%$ & \cellcolor{posgreen!50}$+0.47\%$ & $-11.30\%$ & $-13.57\%$ & \cellcolor{posgreen!50}$+2.26\%$ & $-14.16\%$ & $-14.63\%$ & \cellcolor{posgreen!50}$+0.47\%$ & $-10.43\%$ & $-12.10\%$ & \cellcolor{posgreen!50}$+1.66\%$ & $-6.96\%$ & $-6.82\%$ & \cellcolor{negred!50}$-0.14\%$ \\
 &  & inv & $-16.99\%$ & $-17.01\%$ & $+0.03\%$ & $-6.23\%$ & $-13.39\%$ & \cellcolor{posgreen!50}$+7.16\%$ & $-11.78\%$ & $-11.84\%$ & \cellcolor{posgreen!50}$+0.05\%$ & $-13.17\%$ & $-14.01\%$ & \cellcolor{posgreen!50}$+0.84\%$ & $-7.32\%$ & $-6.87\%$ & \cellcolor{negred!50}$-0.45\%$ \\
 &  & vsp & $-14.68\%$ & $-14.93\%$ & \cellcolor{posgreen!50}$+0.25\%$ & $-9.30\%$ & $-13.48\%$ & \cellcolor{posgreen!50}$+4.19\%$ & $-9.11\%$ & $-9.33\%$ & \cellcolor{posgreen!50}$+0.22\%$ & $-12.59\%$ & $-13.56\%$ & \cellcolor{posgreen!50}$+0.97\%$ & $-7.54\%$ & $-7.13\%$ & \cellcolor{negred!50}$-0.41\%$ \\
 &  & fpm & $-14.51\%$ & $-13.49\%$ & \cellcolor{negred!50}$-1.02\%$ & $-14.51\%$ & $-13.07\%$ & \cellcolor{negred!50}$-1.44\%$ & $-9.97\%$ & $-8.19\%$ & \cellcolor{negred!50}$-1.78\%$ & $-13.66\%$ & $-13.49\%$ & \cellcolor{negred!50}$-0.17\%$ & $-9.38\%$ & $-9.16\%$ & \cellcolor{negred!50}$-0.22\%$ \\
\cmidrule(lr){2-18}
 & rp & lam & $-13.11\%$ & $-12.18\%$ & \cellcolor{negred!50}$-0.94\%$ & $-9.58\%$ & $-12.13\%$ & \cellcolor{posgreen!50}$+2.55\%$ & $-12.57\%$ & $-12.18\%$ & \cellcolor{negred!50}$-0.39\%$ & $-9.90\%$ & $-11.90\%$ & \cellcolor{posgreen!50}$+1.99\%$ & $-6.77\%$ & $-6.75\%$ & $-0.03\%$ \\
 &  & raw & $-14.24\%$ & $-14.56\%$ & \cellcolor{posgreen!50}$+0.32\%$ & $-9.58\%$ & $-12.12\%$ & \cellcolor{posgreen!50}$+2.54\%$ & $-14.24\%$ & $-14.56\%$ & \cellcolor{posgreen!50}$+0.32\%$ & $-9.90\%$ & $-11.90\%$ & \cellcolor{posgreen!50}$+1.99\%$ & $-6.77\%$ & $-6.75\%$ & $-0.03\%$ \\
 &  & inv & $-16.41\%$ & $-16.26\%$ & \cellcolor{negred!50}$-0.14\%$ & $-5.57\%$ & $-11.94\%$ & \cellcolor{posgreen!50}$+6.36\%$ & $-11.10\%$ & $-11.21\%$ & \cellcolor{posgreen!50}$+0.11\%$ & $-12.81\%$ & $-13.36\%$ & \cellcolor{posgreen!50}$+0.55\%$ & $-6.83\%$ & $-6.73\%$ & \cellcolor{negred!50}$-0.10\%$ \\
 &  & vsp & $-13.91\%$ & $-14.03\%$ & \cellcolor{posgreen!50}$+0.13\%$ & $-7.82\%$ & $-12.03\%$ & \cellcolor{posgreen!50}$+4.21\%$ & $-8.82\%$ & $-9.03\%$ & \cellcolor{posgreen!50}$+0.21\%$ & $-12.05\%$ & $-12.98\%$ & \cellcolor{posgreen!50}$+0.94\%$ & $-7.00\%$ & $-6.72\%$ & \cellcolor{negred!50}$-0.28\%$ \\
 &  & fpm & $-13.90\%$ & $-12.70\%$ & \cellcolor{negred!50}$-1.21\%$ & $-12.72\%$ & $-11.34\%$ & \cellcolor{negred!50}$-1.38\%$ & $-9.55\%$ & $-7.99\%$ & \cellcolor{negred!50}$-1.56\%$ & $-13.19\%$ & $-12.70\%$ & \cellcolor{negred!50}$-0.50\%$ & $-8.83\%$ & $-8.60\%$ & \cellcolor{negred!50}$-0.23\%$ \\
\bottomrule
\end{tabular}}
\end{table}
```
