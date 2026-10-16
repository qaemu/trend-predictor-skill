# Test results

Run on 2026-10-16 with Python 3.13.16, pandas 3.0.5, numpy 2.5.3.

| Suite | What it checks | Passed | Failed |
|---|---|---|---|
| [`test_engine`](test_engine.txt) | Calibration on 60 simulated technologies; end-to-end forecast, feasibility, plots, workbook | 13 | 0 |
| [`test_edge_cases`](test_edge_cases.txt) | Inflation, bad rows, mixed date formats, gaps, limits, mixed products, missing files, overrides | 34 | 0 |
| [`test_autofix`](test_autofix.txt) | Repairs stay out of the way on clean data and help on real breaks and outliers | 7 | 0 |
| [`test_real_data`](test_real_data.txt) | Backtest on sourced data (wages, GPU prices, thermal imagers) | 12 | 0 |

Calibration: pooled coverage 80%: 0.769  95%: 0.932  n=11775
(an honest method gives about 0.80 and 0.95)
