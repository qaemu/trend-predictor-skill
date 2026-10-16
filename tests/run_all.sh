#!/usr/bin/env bash
# Run every test suite and save the output to tests/results/ (committed, so the results are visible on GitHub).
set -uo pipefail
cd "$(dirname "$0")/.."
mkdir -p tests/results
status=0
{
  echo "# Test results"
  echo
  echo "Run on $(date -u +%Y-%m-%d) with $(python3 --version 2>&1), pandas $(python3 -c 'import pandas; print(pandas.__version__)'), numpy $(python3 -c 'import numpy; print(numpy.__version__)')."
  echo
  echo "| Suite | What it checks | Passed | Failed |"
  echo "|---|---|---|---|"
} > tests/results/SUMMARY.md
for t in test_engine test_edge_cases test_autofix test_real_data; do
  python3 "tests/$t.py" > "tests/results/$t.txt" 2>&1 || status=1
  sed -i -E 's#/tmp/[A-Za-z0-9_]+#<tmpdir>#g' "tests/results/$t.txt"
  pass=$(grep -c '^PASS' "tests/results/$t.txt" || true)
  fail=$(grep -c '^FAIL' "tests/results/$t.txt" || true)
  case $t in
    test_engine) what="Calibration on 60 simulated technologies; end-to-end forecast, feasibility, plots, workbook";;
    test_edge_cases) what="Inflation, bad rows, mixed date formats, gaps, limits, mixed products, missing files, overrides";;
    test_autofix) what="Repairs stay out of the way on clean data and help on real breaks and outliers";;
    test_real_data) what="Backtest on sourced data (wages, GPU prices, thermal imagers)";;
  esac

  echo "| [\`$t\`]($t.txt) | $what | $pass | $fail |" >> tests/results/SUMMARY.md
done
echo >> tests/results/SUMMARY.md
grep -h "pooled coverage" tests/results/test_engine.txt | sed 's/^/Calibration: /' >> tests/results/SUMMARY.md
echo "(an honest method gives about 0.80 and 0.95)" >> tests/results/SUMMARY.md
cat tests/results/SUMMARY.md
exit $status
