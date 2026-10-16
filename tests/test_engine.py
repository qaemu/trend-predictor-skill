#!/usr/bin/env python3
"""Offline test of the TREND-PREDICTOR engine on synthetic data with known answers.

    python3 tests/test_engine.py

1. Simulates 60 cost series as random walks with drift and MA(1) noise (theta 0.63), the
   process Farmer & Lafond fitted to real technologies, and checks that hindcast coverage of
   the 80% and 95% ranges is close to nominal.
2. Builds a small project (a curve requirement, a dated regulation, a readiness step and a
   judgment input) and checks that probabilities rise with horizon, a target below the floor
   scores 0, and the verdict and start window are written.
"""
import os
import subprocess
import sys
import tempfile

import numpy as np
import pandas as pd

FAIL = []


def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + (f"  [{detail}]" if detail else ""))
    if not cond:
        FAIL.append(name)


ENGINE = os.path.join(os.path.dirname(__file__), "..", "skills", "trend-predictor", "scripts", "trend_predictor.py")


def run(args, cwd):
    r = subprocess.run([sys.executable, ENGINE] + args, cwd=cwd, capture_output=True, text=True)
    if r.returncode:
        print(r.stdout, r.stderr)
        raise SystemExit(f"engine failed: {args[0]}")
    return r.stdout


def main():
    rng = np.random.default_rng(7)
    d = tempfile.mkdtemp()
    rows = []
    for k in range(60):
        mu, K, th = rng.uniform(-0.15, -0.02), rng.uniform(0.05, 0.2), 0.63
        e = rng.normal(0, K, 31)
        y = np.log(1000.0)
        for i, yr in enumerate(range(1995, 2025)):
            y += mu + e[i + 1] + th * e[i]
            rows.append(dict(constraint_id=f"S{k:02d}", tier="all", date=str(yr), value=float(np.exp(y)),
                             unit="index", currency="", price_basis="", source_url=f"https://example.com/{k}/{yr}"))
    # the project's own curve: -12%/yr from 100, low noise
    for yr in range(2008, 2026):
        rows.append(dict(constraint_id="C1", tier="all", date=str(yr), value=1000 * 0.88 ** (yr - 2008) * rng.lognormal(0, 0.04),
                         unit="USD per kWh", currency="", price_basis="", source_url=f"https://example.com/c1/{yr}"))
    pd.DataFrame(rows).to_csv(os.path.join(d, "points.csv"), index=False)
    pd.DataFrame([dict(constraint_id="C1", name="Storage cost", unit="USD per kWh", better="lower", floor=8,
                       ceiling="", bound_source="https://example.com/floor", domain="energy")]).to_csv(
        os.path.join(d, "constraints.csv"), index=False)

    # 1. calibration
    out = run(["hindcast", "--end", "2025", "--cpi", "", "--max-tau", "10"], d)
    cal = pd.read_csv(os.path.join(d, "calibration.csv"))
    pooled = cal[cal.constraint_id == "ALL"].iloc[0]
    print(f"pooled coverage 80%: {pooled.cover80:.3f}  95%: {pooled.cover95:.3f}  n={int(pooled.n)}")
    check("80% ranges cover 72-90% of outcomes (honest)", 0.72 <= pooled.cover80 <= 0.90, round(pooled.cover80, 3))
    check("95% ranges cover 88-98.5% of outcomes (honest)", 0.88 <= pooled.cover95 <= 0.985, round(pooled.cover95, 3))

    # 2. forecast + feasibility
    run(["forecast", "--end", "2025", "--cpi", "", "--plots"], d)
    fit = pd.read_csv(os.path.join(d, "series_fit.csv"))
    c1 = fit[fit.constraint_id == "C1"].iloc[0]
    check("known -12%/yr curve recovered", abs(c1.annual_change_pct - (-12)) < 2, c1.annual_change_pct)
    check("fan chart written", os.path.exists(os.path.join(d, "plots", "fan_C1_all.png")))

    pd.DataFrame([dict(event_id="E1", description="Grid code allows home batteries", type="regulation", status="enacted",
                       date_scheduled="2028-07", source_url="https://example.com/law")]).to_csv(os.path.join(d, "events.csv"), index=False)
    pd.DataFrame([
        dict(req_id="R1", description="Storage below 30 USD/kWh", kind="curve", constraint_id="C1", target_value=30, critical="yes"),
        dict(req_id="R2", description="Regulation in force", kind="event", event_id="E1", critical="yes"),
        dict(req_id="R3", description="Controller reaches TRL 9", kind="readiness", current_trl=6, needed_trl=9, domain="electronics", critical="yes"),
        dict(req_id="R4", description="Insurers cover it", kind="judgment", p_5y=0.5, p_10y=0.8, source_url="https://example.com/q", critical="yes"),
        dict(req_id="R5", description="Below the floor (impossible)", kind="curve", constraint_id="C1", target_value=5, critical="no"),
    ]).to_csv(os.path.join(d, "requirements.csv"), index=False)
    run(["feasibility", "--end", "2025", "--cpi", "", "--lead-years", "2", "--plots"], d)
    fz = pd.read_csv(os.path.join(d, "feasibility.csv")).set_index("req_id")
    ps = pd.read_csv(os.path.join(d, "project_score.csv"))
    for r in ("R1", "R2", "R3", "R4"):
        check(f"{r}: probability by +10y >= by +5y", fz.loc[r, "p_10y"] >= fz.loc[r, "p_5y"])
    check("target below the physical floor is impossible (0)", fz.loc["R5", "p_10y"] == 0)
    check("enacted regulation due 2028 gets a 0.7-0.95 prior by +5y", 0.7 < fz.loc["R2", "p_5y"] < 0.95, fz.loc["R2", "p_5y"])
    check("project verdict written", "verdict" in ps and ps.verdict.notna().any())
    check("start window written", (ps.horizon_years.astype(str) == "start-window").any())
    print(fz[["p_5y", "p_10y", "median_crossing_year"]].to_string())
    print(ps.drop(columns=[c for c in ps if c == "joint_path"]).to_string(index=False))
    run(["workbook", "--project", "Test project", "--end", "2025", "--date", "2026-10-16"], d)
    check("workbook written", any(f.endswith(".xlsx") for f in os.listdir(d)))
    print("\nALL TESTS PASSED" if not FAIL else f"\n{len(FAIL)} FAILED: {', '.join(FAIL)}")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
