#!/usr/bin/env python3
"""Re-score a real model-run with the current engine: MiMo V2.6 Flash, scan of US software-engineering pay
(examples/mimo-scan-swe-salaries). The run's own inputs are re-used unchanged.

    python3 tests/test_real_run.py

What must hold:
- The engine reproduces the run's joint probabilities exactly (same inputs, same math).
- Verdicts whose weakest link is weak evidence (the run's own IDEA estimates, or a grade-C curve) become
  UNCERTAIN; the run had reported them as PLAUSIBLE / LONG SHOT. The original verdict is kept in
  verdict_if_inputs_hold.
- A verdict whose weakest link cites an external expert panel (LEAP) is left unchanged.
"""
import os
import shutil
import subprocess
import sys
import tempfile

import pandas as pd

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
ENGINE = os.path.join(ROOT, "skills", "trend-predictor", "scripts", "trend_predictor.py")
EX = os.path.join(ROOT, "examples", "mimo-scan-swe-salaries")
DATA, ORIG = os.path.join(EX, "data"), os.path.join(EX, "original_run")
OUT = os.path.join(EX, "rescored")
FAIL = []
RUNS = {"scan": ("requirements_scan.csv", "project_score.csv"),
        "p1_entry_band_benchmarking": ("requirements_p1_entry_band_benchmarking.csv", "projects/project_score_p1.csv"),
        "p2_nonprofit_apprenticeship": ("requirements_p2_nonprofit_apprenticeship.csv", "projects/project_score_p2.csv"),
        "p3_junior_plus_ai_staffing": ("requirements_p3_junior_plus_ai_staffing.csv", "projects/project_score_p3.csv")}


def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + (f"  [{detail}]" if detail else ""))
    if not cond:
        FAIL.append(name)


def score(name, req):
    d = os.path.join(OUT, name)
    os.makedirs(d, exist_ok=True)
    shutil.copy(os.path.join(DATA, "calibration.csv"), d)       # the run's own hindcast verdicts
    args = [sys.executable, ENGINE, "feasibility", "--end", "2025", "--horizons", "5,10",
            "--points", os.path.join(DATA, "points.csv"), "--constraints", os.path.join(DATA, "constraints.csv"),
            "--cpi", os.path.join(DATA, "cpi.csv"), "--events", os.path.join(DATA, "events.csv"),
            "--scenarios", os.path.join(DATA, "scenarios.csv"), "--requirements", os.path.join(DATA, req),
            "--domain", "software", "--lead-years", "2", "--outdir", d]
    r = subprocess.run(args, capture_output=True, text=True)
    if r.returncode:
        print(r.stderr[-2000:])
        sys.exit(f"engine failed on {name}")
    return pd.read_csv(os.path.join(d, "project_score.csv")), pd.read_csv(os.path.join(d, "feasibility.csv"))


def main():
    new, old = {}, {}
    rows = []
    for name, (req, orig) in RUNS.items():
        ps, fz = score(name, req)
        ps = ps[ps.horizon_years.astype(str).isin(["5", "10"])]
        new[name] = ps.set_index(ps.horizon_years.astype(str))
        o = pd.read_csv(os.path.join(ORIG, orig))
        old[name] = o[o.horizon_years.astype(str).isin(["5", "10", "5.0", "10.0"])]
        old[name].index = old[name].horizon_years.astype(float).astype(int).astype(str)
        for h in ("5", "10"):
            rows.append(dict(run=name, horizon=f"+{h}y", joint=new[name].loc[h, "joint_if_independent"],
                             weakest=new[name].loc[h, "weakest_requirement"],
                             evidence=new[name].loc[h, "weakest_evidence"],
                             mimo_verdict=old[name].loc[h, "verdict"], engine_verdict=new[name].loc[h, "verdict"]))
    table = pd.DataFrame(rows)
    table.to_csv(os.path.join(OUT, "comparison.csv"), index=False)
    print(table.to_string(index=False))
    print()

    for name in RUNS:
        for h in ("5", "10"):
            a, b = float(new[name].loc[h, "joint_if_independent"]), float(old[name].loc[h, "joint_if_independent"])
            check(f"{name} +{h}y: joint probability reproduced", abs(a - b) < 0.002, f"{a} vs {b}")
            check(f"{name} +{h}y: original verdict kept as verdict_if_inputs_hold",
                  new[name].loc[h, "verdict_if_inputs_hold"] == old[name].loc[h, "verdict"])
    for name in ("p1_entry_band_benchmarking", "p3_junior_plus_ai_staffing"):
        for h in ("5", "10"):
            v = str(new[name].loc[h, "verdict"])
            check(f"{name} +{h}y: weak weakest link -> UNCERTAIN", v.startswith("UNCERTAIN"), v)
    for h in ("5", "10"):
        v, e = str(new["p2_nonprofit_apprenticeship"].loc[h, "verdict"]), new["p2_nonprofit_apprenticeship"].loc[h, "weakest_evidence"]
        check(f"p2 +{h}y: externally sourced weakest link (LEAP, Medium) -> verdict unchanged",
              e == "Medium" and not v.startswith("UNCERTAIN"), f"{e}, {v}")
    _, fz = score("p1_entry_band_benchmarking", RUNS["p1_entry_band_benchmarking"][0])
    check("IDEA-agent judgment graded Low", fz.set_index("req_id").loc["jud01", "evidence_grade"] == "Low")
    print("\nALL REAL-RUN CHECKS PASSED" if not FAIL else f"\n{len(FAIL)} FAILED: {', '.join(FAIL)}")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
