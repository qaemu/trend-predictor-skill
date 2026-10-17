# TREND-PREDICTOR — US software engineering salaries and workplaces

**Mode:** scan ("what becomes viable in this field by +5 / +10?")
**Field / region:** software engineering compensation and work / USA
**ORIGIN:** 2025 (last full calendar year) · **Horizons:** +5 = 2030, +10 = 2035 · **Run date:** 2026-10-17
**Evidence base:** reuses the PARADIGMA constraint-shift run of 2026-10-16 (`/Users/lucas/paradigma_swe_salaries_usa_2026-10-16/`) — 437 sourced points, 28 constraints, PESTEL rows, why-not rows, company map — plus one denser-history research pass (monthly Indeed index, monthly BLS CPS unemployment 2010–2025, NACE 2016–2020 start salaries).
**Perspective:** a builder deciding where to spend effort in this field. `better` values inherited from the PARADIGMA run (costs lower = better, supply/slack higher = better; `swe_senior_junior_ratio` is the worker-return metric).
**Files:** `points.csv`, `constraints.csv`, `requirements.csv`, `events.csv`, `scenarios.csv`, `signposts.csv`, `predictions_log.csv`, `forecasts.csv`, `hindcast.csv`, `calibration.csv`, `series_fit.csv`, `feasibility.csv`, `project_score.csv` (+ `proj1|2|3*/`), `plots/`, `trend_predictor_us-software-engineering-salaries-and-workplaces-scan.xlsx`.

---

## 1. Method and calibration (hindcast)

Random walk with drift (Farmer & Lafond 2016), Student-t bands, autocorrelation-corrected; every series hindcast from past origins on its own history before forecasting. Drift fits log period medians; money points are deflated to real 2025 USD with CPIAUCSL annual averages (through 2026-09).

**Pooled calibration (hindcast, origin 2025):** across the series with ≥5 yearly changes, empirical coverage of the 80% / 95% bands was 0.88 / 0.96 (trend-changed series included; see `calibration.csv`). Bias on log scale ≈ 0.02 — the bands are slightly optimistic on some series and pessimistic on others, not systematically off-centre.

**Series grades (`series_fit.csv`):**

| Grade | Series | Status |
|---|---|---|
| B | `grad_start_salary/nace_bachelors` (10 pts), `swe_senior_junior_ratio`, `swe_senior_plus_salary`, `wage_oes_p90` | fit, calibrated |
| C | `swe_junior_salary`, `swe_median_salary`, `swe_senior_salary`, `wage_oes_p10`, `wage_oes_median`, `junior_base`, `senior_base`, `h1b_junior_wage`, `h1b_senior_wage`, `swe_entry_bigtech_us`, `swe_entry_topofmarket_us` | fit, few checks or narrow bands — use with caution |
| C (uninformative) | `postings_index` (80% range 1.7 → 1,823 by 2030), `unemp_rate_comp` (biased ×1.6, bands too narrow) | **kept out of the headline**: converted to judgment / flagged |
| D | `ai_tool_adoption_planned`, `ai_tool_adoption_prof`, `ai_tool_daily_copilot`, `cs_degrees` (1 check), `h1b_senior_wage` (1 check), `*tc_bigtech*` | too few yearly changes — no forecast; judgment or truncated series |

**Automatic repairs applied:** front-loaded gap repair and window repair on the Payscale panels and the H-1B series; the SOC code break (15-1132 → 15-1256 → 15-1252) is recorded in `points.csv` notes and never treated as a trend.

**Break check (trend changed warning on the BLS/OEWS and Payscale series):** re-fit with only 2018–2025 (`recent/`). Drift shifts from +0.11→+0.33%/yr (all years) to +0.33→+0.48%/yr (recent) on the entry/median series, +0.14→+0.33 on the OEWS median; 2035 medians move by ≤1.9%. **No verdict changes** — the recent window is mildly *more* favorable to entry pay than the full decade, not a different regime. Both fits are reported.

**Rejected from the headline:** the Copilot subscriber series (3 points, product-generation change), the big-tech TC series (2 points, no forecast possible), and `postings_index` as a *model* (its range spans three orders of magnitude) — the last is re-issued as a judgment probability instead.

---

## 2. What the field looks like if the trend continues (forecasts, real 2025 USD)

| Series | Current (2025) | Drift/yr | 2030 median [80%] | 2035 median [80%] |
|---|---|---|---|---|
| `swe_junior_salary` (BLS P25) | 105,210 | +0.33% | 106,932 [99,140–115,336] | 108,682 [95,688–123,440] |
| `swe_median_salary` | 135,980 | +0.14% | 136,948 [122,670–152,887] | 137,923 [114,595–165,999] |
| `swe_senior_salary` | 171,980 | +0.11% | 172,928 [156,796–190,719] | 173,881 [147,461–205,034] |
| `junior_base` (Payscale) | 82,998 | −1.79% | 75,832 [65,073–88,370] | 69,285 [53,555–89,634] |
| `senior_base` (Payscale) | 130,569 | −0.55% | 126,678 [111,557–143,850] | 122,904 [99,233–152,220] |
| `h1b_junior_wage` | 136,000 | −1.65% | 123,701 [105,536–144,991] | 112,513 [85,368–148,291] |
| `swe_senior_junior_ratio` (P75/P25) | 1.635 | −0.21% | 1.6 [1.6–1.7] | 1.6 [1.5–1.7] |
| `unemp_rate_comp` (monthly CPS) | 3.3% | +6.3% | 2.8 [1.0–7.7] | 2.4 [0.5–12.2] |
| `cs_degrees` (NCES, ends 2022) | 108,503 (2022) | +9.1% | exceeds 113,900 (P=0.995) | P=0.997 |

Crossing years for the thresholds: `req04` 2028.6 · `req02` 2031.4 · `req03` 2034.9 · `req06` (stale extrapolation).

**The one-sentence forecast:** entry and median pay are essentially **flat in real terms** over 2025–2035 under every fit; the *survey* panels (`junior_base`) continue the verified −1.8 to −2.1%/yr real decline already documented in PARADIGMA, while the BLS percentile series does not confirm it — a divergence the run carries explicitly rather than averaging away (see PARADIGMA §3e).

---

## 3. Dated events (priced with base-rate priors; `events.csv`)

| Event | Type | Date | P by +5 / +10 |
|---|---|---|---|
| H-1B $100k payment policy remains the governing rule (currently vacated nationwide, on appeal) | regulation, enacted | 2025-09-21 (policy window extended to 2027-09-21) | 0.65 / 0.65 (override: D. Mass. vacatur 2026-06-08, First Circuit stay denied 2026-07-24 — the payment is unenforceable at run date) |
| DHS flat $103,265 H-1B fee finalised | regulation, proposed | 2026-08-25 | 0.30 by date / 0.55 within 3 yrs |
| Wage/skill-weighted H-1B selection replaces the random lottery | regulation, **enacted (final rule 90 FR 60864)** | 2026-02-27 | 0.92 / 0.92 — already in force; recorded as proposed until the verification pass corrected it (fatal finding ck065) |
| WA HB 1155 near-total non-compete ban | regulation, enacted | 2027-06-30 | 0.75 / 0.92 |
| First EU 150+ employer pay-gap reports | regulation, enacted | 2027-06-07 | 0.75 / 0.92 |
| Colorado SB26-189 AI-in-hiring rules | regulation, enacted | 2027-01-01 | 0.75 / 0.92 |

Enacted-past priors are 0.75/0.92; all four enacted items have verified primary sources (federalregister.gov, leg.wa.gov, eur-lex, cdle.colorado.gov). ev03 is the only item already in force; correcting it moved its own probability 0.30→0.92 but changed **no verdict**, since it is non-critical in the scan and in all three projects.

---

## 4. Judgment inputs (IDEA, two estimators × two rounds)

No crowd forecast matches any of the four thresholds (checked Metaculus, Manifold, FRI/LEAP). Both estimators worked independently, saw each other's reasoning in round 2, and updated only where the other's evidence was better (`idea_A1/A2.md`, `idea_B1/B2.md`).

| ID | Threshold | P(2030) | P(2035) | Grade | Anchor |
|---|---|---|---|---|---|
| jud01 | Indeed software-dev postings index ≥ 100 (Feb 2020 = 100) | **0.50** | **0.65** | Low | outside view 45–60%, cut for structural AI damage to mid-level titles |
| jud02 | ≥90% of devs using/planning AI tools (Stack Overflow) | **0.50** | **0.60** | Low | observed 70→76→84 (2023–25); 16–17% holdout share |
| jud03 | New-grad share of big-tech hires ≥ 10% | **0.25** | **0.35** | Medium | FRI/LEAP expert panel (median 7.0% @2030, 7.8% @2040) — https://leap.forecastingresearch.org/forecasts/entry-level-tech-hiring |
| jud04 | ≥3% of SOC 15-1252 devs covered by collective bargaining | **0.30** | **0.40** | Low | narrow "represented" definition (the broader computer-&-math group is already ~4.4% per BLS Union Members 2025) |

Round-2 values converged to agreement on jud03/jud04 *because the evidence converged* (both adopted the LEAP panel and the definition trap), not by averaging.

---

## 5. Feasibility — scan of the field

**All four enabling conditions of the field simultaneously (critical: jud01, jud02, jud03, rd01):**

| Horizon | Joint P | Weakest link | Verdict |
|---|---|---|---|
| +5 (2030) | **0.062** | jud03 = 0.25 | UNLIKELY |
| +10 (2035) | **0.136** | jud03 = 0.35 | LONG SHOT |

Read correctly: it is *unlikely* that postings fully recover **and** AI adoption saturates **and** entry hiring recovers **and** agents prove out — all at once. The binding item is entry-level hiring recovery (jud03), and the weakest-link bound (0.25/0.35) already sets the ceiling; the joint adds only the independence assumption.

**Thresholds most likely to cross (requirement table, `feasibility.csv`):**

| P(+5) | P(+10) | Requirement |
|---|---|---|
| 0.995 | 0.997 | req06 CS cohort exceeds its record (pipeline keeps growing while the entry rung shrinks) |
| 0.781 | 0.815 | req08 top-of-market entry offer sets a new real record |
| 0.594 | 0.731 | req04 H-1B junior listed wage breaks below its decade floor |
| 0.414 | 0.636 | **req02 junior base −10% real (crossing year 2031.4)** |
| 0.377 | 0.502 | req03 senior base sets a new real decade low |
| 0.129 | 0.203 | req07 comp/math unemployment above any month since 2010 |
| 0.041 | 0.105 | req01 BLS entry percentile at a new real decade low (trend moves away) |
| 0.007 | 0.032 | req05 senior/junior premium above 1.75 (trend moves away) |

The field's shape: **supply keeps loosening (certainty), the tail keeps paying more (high probability), the middle keeps deflating (even odds), and the experienced premium neither blows out nor compresses (near-certain to stay in band).**

---

## 6. Candidate projects (top 3–5 constraints turned into scored projects)

Scoring = probability that **all** critical requirements are met simultaneously; verdicts per the skill's bands (≥0.60 joint + ≥0.80 weakest = LIKELY; ≥0.35 = PLAUSIBLE; ≥0.15 = LONG SHOT; else UNLIKELY). Lead time 2 years for each (software product / program build).

### P1 — Junior/entry pay-band benchmarking + compliance reporting *(sell band benchmarks to employers under pay-transparency and AI-audit rules)*
Critical: jud01 (an entry market to benchmark), evreq05 (EU reports), evreq06 (Colorado AI rules). Supporting: req02, req06, jud02.

| +5 | +10 | Weakest | Verdict | Start window |
|---|---|---|---|---|
| **0.423** | **0.550** | jud01 (0.50/0.65) | **PLAUSIBLE / PLAUSIBLE** | **build by 2032** (P ≥0.5 first in 2034, minus 2y lead) |

Sensitivity: jud01 −25% relative → 0.317 (LONG SHOT @+5) / 0.529, start 2033; jud01 +25% → 0.529 / 0.643, start 2028. **The verdict at +10 is robust (PLAUSIBLE either way); the +5 verdict and the start date are fragile — they hinge entirely on whether postings recover.**

### P2 — Non-profit apprenticeship pipeline into SWE
Critical: jud01 (postings recovery), jud03 (entry hiring recovery). Supporting: req01, req02, req06.

| +5 | +10 | Weakest | Verdict | Start window |
|---|---|---|---|---|
| **0.125** | **0.227** | jud03 (0.25/0.35) | **LONG SHOT / LONG SHOT** | P stays <0.5 through 2035 |

The project needs the entry rung to *exist* again; the sourced LEAP panel says it will not be back to 10% by 2030. Non-critical support (supply, cost) is essentially free — all the risk sits in two judgments.

### P3 — Junior-plus-AI staffing (entry-priced capacity with agent tooling)
Critical: req02 (junior cost keeps falling), jud02 (tooling standard), rd01 (agents at TRL 9). Supporting: req01, jud03.

| +5 | +10 | Weakest | Verdict | Start window |
|---|---|---|---|---|
| **0.205** | **0.382** | req02 @+5 (0.414), jud02 @+10 (0.60) | **LONG SHOT / PLAUSIBLE** | P stays <0.5 through 2035 |

Sensitivity on the weakest link (req02 target ±25%): target 55,500 (deeper decline) → **0.006/0.079 UNLIKELY**; target 92,500 (shallower) → **0.469/0.553 PLAUSIBLE**. **Verdict flips across the band → very fragile; do not build on this score without re-checking `signposts.csv` first.** Note the sign of the fragility: the project needs junior pay to keep falling, and a *deeper* fall than the trend implies is itself unlikely.

**Stall scenario** (`scenarios.csv`: the verified real declines stop, rate 0 — constructed, not a published forecast): the scan's critical set is all judgments, so the scan joint is unchanged (0.062/0.136); the curve requirements downstream of P1/P3 (req02, req03) move as expected — their crossing probabilities drop, since the thresholds only trip on continuation.

**Ranking:** P1 > P3 > P2. P1 is the only project whose +10 verdict survives the sensitivity test; P3's score is dominated by a target choice; P2 is gated on a recovery the best-sourced panel does not expect.

---

## 7. Signposts, log, pre-mortem, limitations

**Signposts (`signposts.csv`, 12 rows)** — earliest readings that move a probability, each with its next-check date. The four that matter most:
- **2027-01-31** — Indeed index: ≥100 → jud01 ≥0.70; ≤60 → ≤0.35. *(Rechecks: 2027-10-17 for all rows.)*
- **2027-03-31** — First Circuit H-1B fee ruling: affirmance → 0.90, reversal → 0.20.
- **2027-06-30** — Payscale entry base inside 73,967–86,642 (80% band); below → req02 accelerating.
- **2027-04-30** — Stack Overflow 2027 survey: ≥90 → jud02 met early (0.9); two flat surveys → 0.30.

**Prediction log (`predictions_log.csv`)** — 14 falsifiable claims with resolve dates (2027 → 2036), each with probability and source. First run: **no prior log exists, so no prior forecast has been scored.** Each future run must backfill `resolved_value`/`outcome`/`brier` for the 14 rows before publishing new numbers.

**Pre-mortem — three ways this forecast is wrong:**
1. **The structural break is real and the drift is the wrong tool.** Both entry-hiring metrics already broke (15%→7% new-grad share; Stanford's 19% shortfall). If hiring rather than pay absorbs the adjustment, `swe_junior_salary` stays flat while the *opportunity set* for juniors keeps shrinking — the forecasts would be right about pay and wrong about the field. Mitigant: jud01/jud03 carry that weight as explicit judgments, and they are the critical set.
2. **The Payscale/BLS divergence is a measurement artifact, not a trend.** If the Payscale panel's 2020 methodology change (average vs median) and panel composition explain the −2.1%/yr, then req02's 0.414 is spurious and P3's critical requirement is fiction. Mitigant: the divergence is reported side by side, never blended; req01 (BLS) is kept as the independent check at 0.041/0.105.
3. **IDEA priors are doing the work where data can't.** Four judgments, three of them Low-grade, two estimators that know each other's reasoning — agreement can be convergence on the same outside view. There is no crowd anchor for jud01/j02/j04. Mitigant: signposts with numeric triggers, and jud03 anchored to the external FRI/LEAP panel rather than to our own reasoning.

**Limitations.** No experience split in BLS OEWS (percentiles are only an experience proxy; SOC break 15-1132→15-1256→15-1252). `cs_degrees` ends 2022 (grade D/1 check) — its 0.99+ is trend extrapolation of a stale series, not a real forecast. `postings_index` and `unemp_rate_comp` are uninformative/weak as models and are only admitted as judgments. Readiness (rd01, P≈0.99) says agents will be *proven*, not that they will be *adopted or economic* — adoption is captured separately by jud02 and cost by req02. The real-value base year (2025) rests on 11 months of CPIAUCSL because FRED carries no value for **2025-10-01** (a shutdown-era collection gap at source, not an engine omission); interpolating October at the Sep/Nov midpoint raises the annual average by 0.07%, so every real figure here is at most 0.07% overstated — three orders of magnitude below the forecast bands. One grade-C point (the 2024 top-of-market HRT L1 offer, $410k) is single-source and no longer re-retrievable from the publisher.

**Reproducibility.** `python3 trend_predictor.py cpi`; `hindcast --end 2025`; `forecast --end 2025 --horizons 5,10 --plots`; `forecast --points points_recent.csv --outdir recent` (break check); `feasibility --end 2025 --horizons 5,10 --requirements requirements.csv --events events.csv --domain software --lead-years 2 --plots`, then the three `proj*` runs with their own requirement files. Engine copied verbatim from the skill; inputs are the PARADIGMA run folder plus `points_dense.csv` (merged additively, 3 duplicate keys dropped).

**Independent verification (`verification.csv`, `verification_notes.md`).** A fresh agent that took no part in the research re-checked 84 items: every grade-B point (all 40, to the cent, including the SOC code transition), all 8 threshold derivations recomputed under the run's own CPI file, all 6 event dates and statuses, the TRL claim, the judgment sources (LEAP panel, BLS 4.4%, Stack Overflow series), the IDEA probability pairs, 25 random data points including recomputed h1bdata medians, and the inflation convention. **77 MATCH / 6 MISMATCH / 1 UNVERIFIABLE → 92% pass rate, one fatal.** The fatal (ev03 recorded as proposed although the final rule has been in force since 2026-02-27) is corrected in `events.csv`, `requirements.csv` and §3 above; the five remaining mismatches are corrected in the files (req01/req02 percentages to 5.6%/10.8%, a $500 transcription slip at `points.csv` line 52, the stale ev01 description) or documented as source limits (the 11-month 2025 CPI base). Re-scoring after the corrections left every verdict and every critical probability unchanged.
