#!/usr/bin/env python3
"""Do the automatic repairs help when they should and stay out of the way when they shouldn't?

    python3 tests/test_autofix.py

A. Clean random walks (nothing to fix): fixes must rarely trigger and out-of-sample 80% coverage must stay honest.
B. A trend that slowed (-30%/yr for 12 years, then -6%/yr): the fix must trigger and beat the default out of sample.
C. An outlier first year: the robust trend must trigger and beat the default out of sample.
"""
import argparse
import importlib.util
import math
import os
import sys

import numpy as np
import pandas as pd

ENGINE = os.path.join(os.path.dirname(__file__), "..", "skills", "trend-predictor", "scripts", "trend_predictor.py")
spec = importlib.util.spec_from_file_location("tp", ENGINE)
tp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tp)
FAIL = []


def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + f"  [{detail}]")
    if not cond:
        FAIL.append(name)


def frame(years, vals):
    return pd.DataFrame({"year": years, "value": vals, "src": [f"https://x/{y}" for y in years]})


def oos(g_train, future, fix, mt=None):
    a = argparse.Namespace(drift="endpoint", min_diffs=5, no_autofix=not fix)
    mt = mt or {"better": "lower", "floor": np.nan, "ceiling": np.nan}
    m, s, info = tp.choose_model(g_train, mt, a, int(g_train.year.max()) + 10)
    errs, inside = [], []
    for y, v in future:
        tau = y - m["t0"]
        errs.append(abs(math.log(v / tp.m_value(m, tau, .5))))
        inside.append(tp.m_value(m, tau, .1) <= v <= tp.m_value(m, tau, .9))
    return np.mean(errs), np.mean(inside), info


rng = np.random.default_rng(11)
# A. clean random walks with drift + MA(1)
trig, cov_fix, cov_def, err_fix, err_def = 0, [], [], [], []
for k in range(80):
    mu, K, th = rng.uniform(-.15, -.02), rng.uniform(.05, .2), .63
    e = rng.normal(0, K, 31)
    y = np.log(1000) + np.cumsum(mu + e[1:] + th * e[:-1])
    yrs = np.arange(1995, 2025)
    g = frame(yrs[:20], np.exp(y[:20]))
    fut = list(zip(yrs[20:], np.exp(y[20:])))
    ef, cf, info = oos(g, fut, True)
    ed, cd, _ = oos(g, fut, False)
    trig += bool(info["fixes"])
    cov_fix.append(cf); cov_def.append(cd); err_fix.append(ef); err_def.append(ed)
check("A. clean data: fixes trigger rarely (<30% of series)", trig / 80 < 0.30, f"{trig}/80")
check("A. clean data: 80% coverage stays honest with fixes on (>=0.70)", np.mean(cov_fix) >= 0.70,
      f"fix {np.mean(cov_fix):.2f} vs default {np.mean(cov_def):.2f}")
check("A. clean data: fixes do not make accuracy worse (within 5%)", np.mean(err_fix) <= np.mean(err_def) * 1.05,
      f"fix {np.mean(err_fix):.3f} vs default {np.mean(err_def):.3f}")

# B. slowed trend
wins_b, trig_b = 0, 0
for k in range(30):
    yrs = np.arange(2000, 2026)
    lv = [np.log(1000)]
    for y in yrs[1:]:
        lv.append(lv[-1] + (-0.36 if y <= 2012 else -0.06) + rng.normal(0, 0.08))
    v = np.exp(lv)
    g = frame(yrs[yrs <= 2020], v[yrs <= 2020])
    fut = list(zip(yrs[yrs > 2020], v[yrs > 2020]))
    ef, cf, info = oos(g, fut, True)
    ed, cd, _ = oos(g, fut, False)
    trig_b += any("trend changed" in f for f in info["fixes"])
    wins_b += ef < ed
check("B. slowed trend: window fix triggers (>=70%)", trig_b / 30 >= 0.7, f"{trig_b}/30")
check("B. slowed trend: fixed forecast beats default out of sample (>=70%)", wins_b / 30 >= 0.7, f"{wins_b}/30")

# C. outlier first year
wins_c, trig_c = 0, 0
for k in range(30):
    yrs = np.arange(2003, 2026)
    lv = np.log(500) + np.cumsum(np.r_[0, rng.normal(-0.15, 0.1, len(yrs) - 1)])
    lv[0] += 1.6                       # first year ~5x too high (e.g. a launch price for a niche product)
    v = np.exp(lv)
    g = frame(yrs[yrs <= 2019], v[yrs <= 2019])
    fut = list(zip(yrs[yrs > 2019], v[yrs > 2019]))
    ef, cf, info = oos(g, fut, True)
    ed, cd, _ = oos(g, fut, False)
    trig_c += bool(info["fixes"])
    wins_c += ef < ed
check("C. outlier first year: a fix triggers (>=60%)", trig_c / 30 >= 0.6, f"{trig_c}/30")
check("C. outlier first year: fixed forecast beats default (>=60%)", wins_c / 30 >= 0.6, f"{wins_c}/30")

print("\nALL AUTOFIX CHECKS PASSED" if not FAIL else f"\n{len(FAIL)} FAILED: {', '.join(FAIL)}")
sys.exit(1 if FAIL else 0)
