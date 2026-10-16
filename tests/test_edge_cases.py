#!/usr/bin/env python3
"""Edge cases that clean synthetic data never triggers. Each check prints PASS/FAIL; exits 1 on any failure.

    python3 tests/test_edge_cases.py
"""
import math
import os
import subprocess
import sys
import tempfile

import numpy as np
import pandas as pd

ENGINE = os.path.join(os.path.dirname(__file__), "..", "skills", "trend-predictor", "scripts", "trend_predictor.py")
FAIL = []


def run(args, cwd, ok=True):
    r = subprocess.run([sys.executable, ENGINE] + args, cwd=cwd, capture_output=True, text=True)
    if ok and r.returncode:
        print(r.stdout[-2000:], r.stderr[-2000:])
        raise SystemExit(f"engine crashed on {args}")
    return r


def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + (f"  [{detail}]" if detail and not cond else ""))
    if not cond:
        FAIL.append(name)


def pts(rows):
    base = dict(tier="all", unit="u", currency="", price_basis="", source_title="", source_type="primary", note="")
    return pd.DataFrame([{**base, **r} for r in rows])


def main():
    rng = np.random.default_rng(3)
    d = tempfile.mkdtemp()
    rows = []
    # E1 nominal USD, flat in real terms, 3%/yr inflation
    cpi = pd.DataFrame({"year": range(2000, 2026), "cpi": [100 * 1.03 ** i for i in range(26)], "months": 12, "source": "x"})
    cpi.to_csv(os.path.join(d, "cpi.csv"), index=False)
    for y in range(2005, 2026):
        rows.append(dict(constraint_id="E1", date=str(y), value=50 * 1.03 ** (y - 2000) * rng.lognormal(0, .02),
                         currency="USD", price_basis="nominal", unit="USD per unit", source_url=f"https://e1/{y}"))
    # E2 bad rows: non-USD, no source, zero, bad date, after end
    rows += [dict(constraint_id="E2", date="2020", value=5, currency="EUR", price_basis="nominal", source_url="https://e2/a"),
             dict(constraint_id="E2", date="2020", value=5, source_url=""),
             dict(constraint_id="E2", date="2020", value=0, source_url="https://e2/c"),
             dict(constraint_id="E2", date="20-20", value=5, source_url="https://e2/d"),
             dict(constraint_id="E2", date="2031", value=5, source_url="https://e2/e")]
    # E3 quarterly / monthly / day dates with gaps (every other year), -10%/yr
    for i, y in enumerate(range(2004, 2026, 2)):
        dt = [f"{y}-Q2", f"{y}-07", f"{y}-07-01"][i % 3]
        rows.append(dict(constraint_id="E3", date=dt, value=100 * 0.9 ** (y - 2004) * rng.lognormal(0, .03), source_url=f"https://e3/{y}"))
    # E4 higher-is-better with a ceiling: efficiency rising toward 30
    for y in range(2008, 2026):
        rows.append(dict(constraint_id="E4", date=str(y), value=12 * 1.04 ** (y - 2008) * rng.lognormal(0, .01), source_url=f"https://e4/{y}"))
    # E5 short series (4 years)
    for y in (2021, 2022, 2023, 2024):
        rows.append(dict(constraint_id="E5", date=str(y), value=10 - (y - 2021), source_url=f"https://e5/{y}"))
    # E6 mixed products: two price classes 10x apart each year
    for y in range(2010, 2026):
        for v in (100, 10):
            rows.append(dict(constraint_id="E6", date=str(y), value=v * 0.9 ** (y - 2010) * rng.lognormal(0, .05), source_url=f"https://e6/{y}/{v}"))
    # E7 very noisy -> uninformative
    for y in range(2010, 2026):
        rows.append(dict(constraint_id="E7", date=str(y), value=math.exp(rng.normal(-0.1 * (y - 2010), 1.2)), source_url=f"https://e7/{y}"))
    pts(rows).to_csv(os.path.join(d, "points.csv"), index=False)
    pd.DataFrame([dict(constraint_id="E1", name="flat real", unit="USD per unit", better="lower", floor="", ceiling="", domain="hardware"),
                  dict(constraint_id="E3", name="gappy", unit="u", better="lower", floor="", ceiling="", domain="energy"),
                  dict(constraint_id="E4", name="efficiency", unit="%", better="higher", floor="", ceiling=30, bound_source="https://limit", domain="energy")]
                 ).to_csv(os.path.join(d, "constraints.csv"), index=False)
    pd.DataFrame([dict(constraint_id="E3", tier="", scenario="stall", annual_change_pct=0, volatility_multiplier="", source_url="https://s")]
                 ).to_csv(os.path.join(d, "scenarios.csv"), index=False)

    run(["hindcast", "--end", "2025"], d)
    run(["forecast", "--end", "2025", "--horizons", "1,5,10,15", "--plots"], d)
    fit = pd.read_csv(os.path.join(d, "series_fit.csv")).set_index("constraint_id")
    rej = pd.read_csv(os.path.join(d, "rejected_points.csv"))
    check("E1 CPI deflation: nominal +3%/yr becomes ~0% real", abs(fit.loc["E1", "annual_change_pct"]) < 1.5, fit.loc["E1", "annual_change_pct"])
    check("E2 all 5 bad rows rejected", (rej.constraint_id == "E2").sum() == 5, (rej.constraint_id == "E2").sum())
    check("E2 rejection reasons recorded", rej.reject_reason.str.len().min() > 3)
    check("E3 mixed date formats + gaps: trend ~ -10%/yr", abs(fit.loc["E3", "annual_change_pct"] + 10) < 2, fit.loc["E3", "annual_change_pct"])
    check("E5 short series graded D, no forecast", fit.loc["E5", "grade"] == "D")
    check("E6 mixed products auto-fixed (frontier)", fit.loc["E6", "aggregation"] == "frontier" and "mixed" in fit.loc["E6", "fixes_applied"])
    check("E6 frontier recovers the -10%/yr trend", abs(fit.loc["E6", "annual_change_pct"] + 10) < 3, fit.loc["E6", "annual_change_pct"])
    check("E7 noisy series flagged uninformative", str(fit.loc["E7", "informative"]).startswith("NO"), fit.loc["E7", "informative"])
    fc = pd.read_csv(os.path.join(d, "forecasts.csv"))
    e4 = fc[(fc.constraint_id == "E4") & (fc.scenario == "trend")]
    check("E4 approaching the ceiling -> gap-to-limit model", fit.loc["E4", "model"] == "gap to limit", fit.loc["E4", "model"])
    check("E4 ceiling caps the upper band", e4.q975.max() <= 30 + 1e-9, e4.q975.max())
    check("horizon 15 present", (fc.horizon == 15).any())
    e3 = fc[fc.constraint_id == "E3"]
    check("E3 stall scenario written", (e3.scenario == "stall").any())
    q = fc[(fc.constraint_id == "E3") & (fc.horizon == 10)].set_index("scenario")
    check("E3 bands monotone (q025<q500<q975)", bool(((q.q025 < q.q500) & (q.q500 < q.q975)).all()))
    for f in ("fan_E1_all.png", "fan_E3_all.png", "fan_E4_all.png", "fan_E7_all.png"):
        check(f"plot {f}", os.path.exists(os.path.join(d, "plots", f)))

    # feasibility edge cases
    pd.DataFrame([
        dict(event_id="V1", description="already in force", type="regulation", status="enacted", date_scheduled="2020-01", source_url="https://v1"),
        dict(event_id="V2", description="override", type="capacity", status="announced", date_scheduled="2027", p_on_time_override=0.9,
             p_eventual_override=0.95, override_source="https://v2", source_url="https://v2"),
        dict(event_id="V3", description="unknown type", type="weird", status="whatever", date_scheduled="2028", source_url="https://v3"),
    ]).to_csv(os.path.join(d, "events.csv"), index=False)
    pd.DataFrame([
        dict(req_id="R1", kind="curve", constraint_id="E3", target_value=20, critical="yes", description="trend"),
        dict(req_id="R2", kind="curve", constraint_id="E3", target_value=20, scenario="stall", critical="no", description="stall"),
        dict(req_id="R3", kind="curve", constraint_id="E4", target_value=35, better="higher", critical="no", description="above ceiling"),
        dict(req_id="R4", kind="curve", constraint_id="E5", target_value=1, critical="no", description="short series"),
        dict(req_id="R5", kind="curve", constraint_id="ZZ", target_value=1, critical="no", description="missing constraint"),
        dict(req_id="R6", kind="event", event_id="V1", critical="yes", description="past"),
        dict(req_id="R7", kind="event", event_id="V2", critical="no", description="override"),
        dict(req_id="R8", kind="event", event_id="V3", critical="no", description="unknown type"),
        dict(req_id="R9", kind="event", event_id="NOPE", critical="no", description="missing event"),
        dict(req_id="R10", kind="readiness", current_trl=9, needed_trl=9, critical="yes", description="mature"),
        dict(req_id="R11", kind="judgment", p_3y=0.4, source_url="https://j", critical="yes", description="only p_3y"),
        dict(req_id="R12", kind="curve", constraint_id="E4", target_value=20, better="higher", critical="no", description="E4 reachable"),
    ]).to_csv(os.path.join(d, "requirements.csv"), index=False)
    run(["feasibility", "--end", "2025", "--horizons", "5,10", "--plots"], d)
    fz = pd.read_csv(os.path.join(d, "feasibility.csv")).set_index("req_id")
    ps = pd.read_csv(os.path.join(d, "project_score.csv"))
    check("R2 stall scenario lowers probability", fz.loc["R2", "p_10y"] < fz.loc["R1", "p_10y"], (fz.loc["R2", "p_10y"], fz.loc["R1", "p_10y"]))
    check("R3 target above ceiling = 0", fz.loc["R3", "p_10y"] == 0)
    check("R4 short series -> no probability, explained", pd.isna(fz.loc["R4", "p_5y"]) and "no usable curve" in fz.loc["R4", "note"])
    check("R5 missing constraint -> no crash, explained", pd.isna(fz.loc["R5", "p_5y"]))
    check("R6 past event -> eventual prior", abs(fz.loc["R6", "p_5y"] - 0.92) < 1e-6, fz.loc["R6", "p_5y"])
    check("R7 overrides applied", abs(fz.loc["R7", "p_10y"] - 0.95) < 1e-6, fz.loc["R7", "p_10y"])
    check("R8 unknown event type falls back to 'other'", abs(fz.loc["R8", "p_10y"] - 0.70) < 1e-6, fz.loc["R8", "p_10y"])
    check("R9 missing event -> explained", "missing" in fz.loc["R9", "note"])
    check("R10 already mature = 1", fz.loc["R10", "p_5y"] == 1)
    check("R11 judgment with p_3y only -> flat after 3y", abs(fz.loc["R11", "p_10y"] - 0.4) < 1e-6, fz.loc["R11", "p_10y"])
    check("R12 higher-better reachable target in (0,1]", 0 < fz.loc["R12", "p_10y"] <= 1)
    check("project score has verdicts", ps.verdict.notna().sum() == 2, ps.to_dict())
    check("feasibility plot", os.path.exists(os.path.join(d, "plots", "feasibility.png")))

    # incomplete project: a critical requirement with no probability
    req = pd.read_csv(os.path.join(d, "requirements.csv"))
    req.loc[req.req_id == "R5", "critical"] = "yes"
    req.to_csv(os.path.join(d, "requirements.csv"), index=False)
    run(["feasibility", "--end", "2025"], d)
    ps = pd.read_csv(os.path.join(d, "project_score.csv"))
    check("unscored critical requirement -> 'incomplete', not a fake verdict",
          ps.status.astype(str).str.startswith("incomplete").any() and ps.get("verdict", pd.Series(dtype=str)).isna().all())

    # theilsen option, missing constraints.csv, workbook with missing files
    d2 = tempfile.mkdtemp()
    pts([r for r in rows if r["constraint_id"] == "E3"]).to_csv(os.path.join(d2, "points.csv"), index=False)
    r = run(["forecast", "--end", "2025", "--drift", "theilsen", "--cpi", ""], d2)
    check("runs with no constraints.csv and theilsen drift", os.path.exists(os.path.join(d2, "series_fit.csv")))
    run(["workbook", "--project", "Edge", "--end", "2025", "--date", "2026-10-16", "--dir", d2], d2)
    check("workbook with missing sheets", any(f.endswith(".xlsx") for f in os.listdir(d2)))
    r = run(["feasibility", "--end", "2025", "--cpi", ""], d2, ok=False)
    check("feasibility without requirements.csv exits with a clear message", r.returncode != 0 and "requirements" in (r.stderr + r.stdout))

    print(f"\n{'ALL EDGE CASES PASSED' if not FAIL else str(len(FAIL)) + ' FAILED: ' + ', '.join(FAIL)}  ({d})")
    sys.exit(1 if FAIL else 0)


if __name__ == "__main__":
    main()
