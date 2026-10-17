# Verification Notes — trend_swe_salaries_workplaces_2026-10-17
Verifier run: 2026-10-17. 84 checks in verification.csv (77 MATCH, 6 MISMATCH, 1 UNVERIFIABLE).
## Fatal (1)
- ev03 (ck065): "Wage/skill-weighted H-1B selection replaces the random lottery" is recorded status=proposed, but
  90 FR 60864 (doc 2025-23853) is a FINAL rule: published 2025-12-29, effective 2026-02-27 — in force for ~7.5 months
  at run date. The event's own note flagged this possibility; the verification pass confirms it. evreq03 ("in force")
  is therefore correct, but the event record understates a binding constraint. Fix: status=enacted, date_scheduled=
  2026-02-27, source_url=federalregister.gov/d/2025-23853, and re-run any scenario logic that treats the weighted
  lottery as a future event.
## Minor mismatches (5)
- ck057 req01: 96000 is 5.6% below the real floor 101731 (exact 5% = 96644); description says "5%". Conservative; cosmetic.
- ck058 req02: 74000 is 10.8% below real floor 82998 (exact = 74698); description says "10%". Conservative; cosmetic.
- ck070 ev01: description says the $100k payment "stays in force", but it was vacated (D. Mass. 2026-06-08) and the
  First Circuit denied a stay (2026-07-24). The note field and p_eventual_override=0.65 already reflect this; only the
  description/status wording is stale.
- ck052 points.csv line 52: swe_junior_tc_us 2024 = 152000; levels.fyi 2025 report.md shows 2024 entry-level = $152,500
  (the parallel row, line 158, correctly has 152500). $500 transcription slip, secondary series, no threshold depends on it.
- ck080 cpi.csv: 2025 base-year average uses 11 months (Dec 2025 absent), mildly biasing every real-2025-USD value;
  immaterial at forecast horizon but worth disclosing.

## Unverifiable (1)
- ck055 swe_entry_topofmarket_us 2024 (Hudson River Trading L1, 410000): 2024 levels.fyi report not retrievable in
  current public tables; grade-C single-source series as the run itself notes. Severity minor.

## What held up
- All 40 grade-B series points (OEWS P90 hourly + annual P90 ladder, 2016-2025, correct SOC transition
  15-1132 -> 15-1256 -> 15-1252) verified to the cent against BLS pages and the run's own Wayback xlsx captures;
  ratio rows re-derived from P75/P25 components.
- All 8 requirement thresholds recomputed under cpi.csv deflation; only the "5%/10%" wording (above) is off.
- All 6 events' substance verified; ev02 (still proposed), ev04 (signed 2026-03-23, effective 2027-06-30), ev05
  (Art. 9 reports 2027-06-07; only 4 states transposed), ev06 (SB26-189 effective 2027-01-01) all MATCH.
- Judgments: LEAP 7.0/7.8 (+ superforecasters 8/10), BLS 4.4% represented, SO 70/76/84, idea-round means, and the
  p_5y/p_10y column semantics all confirmed; rd01 TRL 7 defensible (evidence URL is a thin stub).
- 25 random data rows checked (NACE, Indeed, NCES, h1bdata medians recomputed from raw filings, Payscale, Stack
  Overflow, levels.fyi, Google L3, NY Fed, Microsoft FY25Q3) — all but one MATCH.
