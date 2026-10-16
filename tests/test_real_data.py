#!/usr/bin/env python3
"""Backtest on real, sourced data: the PARADIGMA predictive-maintenance run.

    python3 tests/test_real_data.py

Stands in a past year, forecasts with only the data available then, and compares with what
actually happened. Also runs the full pipeline (hindcast + forecast + plots) on the data up to 2025.
Writes everything to examples/backtest-predictive-maintenance/output/.

What must hold:
- Wages (BLS, 18 years, smooth): honest coverage (>= 70% of later values inside the 80% range) and narrow
  ranges. Forecasts made from 2019 miss 2020-2023 (COVID jump, then inflation cutting real wages): an 80% range
  is supposed to miss about 1 time in 5, and a random walk cannot foresee a shock. The test records it.
- GPU launch prices (noisy, 1-3 per year): engine must NOT claim an informative 10-year forecast.
- Thermal imagers (mixed products): engine must apply the frontier repair and still call it uninformative.
"""
import argparse
import importlib.util
import math
import os
import subprocess
import sys

import numpy as np
import pandas as pd

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
ENGINE = os.path.join(ROOT, "skills", "trend-predictor", "scripts", "trend_predictor.py")
EX = os.path.join(ROOT, "examples", "backtest-predictive-maintenance")
DATA, OUT = os.path.join(EX, "data"), os.path.join(EX, "output")
spec = importlib.util.spec_from_file_location("tp", ENGINE)
tp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tp)
FAIL = []


def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + (f"  [{detail}]" if detail else ""))
    if not cond:
        FAIL.append(name)


def main():
    os.makedirs(OUT, exist_ok=True)
    args = ["--points", os.path.join(DATA, "points.csv"), "--constraints", os.path.join(DATA, "constraints.csv"),
            "--cpi", os.path.join(DATA, "cpi.csv"), "--end", "2025", "--outdir", OUT]
    for cmd in (["hindcast"], ["forecast", "--plots"]):
        r = subprocess.run([sys.executable, ENGINE] + cmd + args, capture_output=True, text=True)
        if r.returncode:
            print(r.stderr)
            sys.exit(f"engine failed: {cmd}")
    fit = pd.read_csv(os.path.join(OUT, "series_fit.csv"))
    ok = fit[fit.status == "ok"].set_index("constraint_id")

    a = argparse.Namespace(points=os.path.join(DATA, "points.csv"), cpi=os.path.join(DATA, "cpi.csv"), base_year=None,
                           end=2025, outdir=OUT, drift="endpoint", min_diffs=5, no_autofix=False)
    _, _, _, raw = tp.load_series(a)
    meta = tp.constraints_meta(os.path.join(DATA, "constraints.csv"))
    rows = []
    for cid, tier in [("C09", "all"), ("C02", "gpu_fp32_consumer")]:
        g = raw[(raw.constraint_id == cid) & (raw.tier == tier)]
        full = tp.yearly(g, "median", meta[cid]["better"])
        for origin in (2013, 2015, 2017, 2019):
            for fix in (False, True):
                a.no_autofix = not fix
                m, s, info = tp.choose_model(g[g.year <= origin], meta[cid], a, origin + 10)
                for _, r in full[full.year > origin].iterrows():
                    tau = r.year - m["t0"]
                    lo, med, hi = tp.m_value(m, tau, .1), tp.m_value(m, tau, .5), tp.m_value(m, tau, .9)
                    rows.append(dict(constraint_id=cid, tier=tier, origin=origin, autofix=fix, year=int(r.year),
                                     actual=round(r["median"], 6), forecast_median=round(med, 6),
                                     q10=round(lo, 6), q90=round(hi, 6), inside_80=lo <= r["median"] <= hi,
                                     error_factor=round(math.exp(abs(math.log(r["median"] / med))), 3),
                                     range80_10y_x=round(tp.m_value(m, 10, .9) / tp.m_value(m, 10, .1), 1),
                                     fixes=" | ".join(info["fixes"]) or "none"))
    bt = pd.DataFrame(rows)
    bt.to_csv(os.path.join(OUT, "backtest.csv"), index=False)
    summ = bt.groupby(["constraint_id", "origin", "autofix"]).agg(
        years_checked=("year", "size"), inside_80=("inside_80", "mean"),
        mean_error_factor=("error_factor", lambda s: round(math.exp(np.mean(np.log(s))), 2)),
        range80_10y_x=("range80_10y_x", "first")).reset_index()
    summ.to_csv(os.path.join(OUT, "backtest_summary.csv"), index=False)
    print(summ.to_string(index=False))
    print()

    w = bt[(bt.constraint_id == "C09") & bt.autofix]
    check("wages: honest coverage (>= 70% of later values inside the 80% range)", w.inside_80.mean() >= 0.70,
          f"{w.inside_80.mean():.0%} of {len(w)}")
    w19 = w[w.origin == 2019]
    print(f"note  wages forecast from 2019: {w19.inside_80.sum()} of {len(w19)} later years inside the 80% range "
          f"(2020 COVID jump, 2021-23 inflation)")
    check("wages: forecasts within 10% on average", math.exp(np.mean(np.log(w.error_factor))) < 1.10)
    check("wages: 10-year 80% range narrower than 1.5x", w.range80_10y_x.max() < 1.5, w.range80_10y_x.max())
    check("wages graded A or B today", ok.loc["C09", "grade"] in ("A", "B"), ok.loc["C09", "grade"])
    check("GPU: not claimed informative at 10 years", str(ok.loc["C02", "informative"]).startswith("NO"), ok.loc["C02", "informative"])
    check("GPU: grade C (cannot carry a headline)", ok.loc["C02", "grade"] == "C")
    g = bt[bt.constraint_id == "C02"]
    check("GPU: real values still inside the (wide) 80% range", g.inside_80.mean() >= 0.8, f"{g.inside_80.mean():.0%}")
    check("thermal: mixed products repaired with the frontier", ok.loc["C04", "aggregation"] == "frontier")
    check("thermal: still reported as uninformative", str(ok.loc["C04", "informative"]).startswith("NO"))
    for f in ("fan_C09_all.png", "fan_C02_gpu_fp32_consumer.png", "fan_C04_all.png"):
        check(f"plot {f}", os.path.exists(os.path.join(OUT, "plots", f)))
    print("\nALL REAL-DATA CHECKS PASSED" if not FAIL else f"\n{len(FAIL)} FAILED: {', '.join(FAIL)}")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
