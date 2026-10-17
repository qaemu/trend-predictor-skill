---
name: trend-predictor
description: TREND-PREDICTOR projects a field's constraints (costs, performance, laws, patents, readiness, adoption) forward 5 and 10 years with calibrated ranges and scores whether a given project will be feasible at each horizon, with its weakest link and when to start building. Use when the user calls TREND-PREDICTOR, asks whether a project or idea will be feasible in N years, or wants to know what will become viable in a field.
---

# TREND-PREDICTOR: will this be feasible in 5 or 10 years?

**Goal:** PARADIGMA looks back: which constraints fell. TREND-PREDICTOR looks forward. It projects each constraint a project depends on to chosen horizons (default +5 and +10 years) with honest uncertainty ranges, adds dated future events and readiness/adoption base rates, and gives a probability that the project's requirements are met at each horizon, the requirement most likely to sink it, and when to start building. It is a decision aid, not a prophecy: every output is a dated, checkable claim with a probability.

**Invocation:** `/trend-predictor "<project>" [field] [region] [horizons] [standard|deep]` or `/trend-predictor scan "<field>" [region] [horizons]`.

- **Project mode (default):** "will *this* be feasible by +5 / +10?" Example: `/trend-predictor "home robot that folds laundry for under $2,000" robotics global`.
- **Scan mode:** "what becomes viable in *this field* by +5 / +10?" Projects every constraint, lists the thresholds most likely to be crossed (one probability per threshold), turns the top 3–5 into candidate projects and scores each one as in project mode. **Only candidate projects get a joint probability and a verdict.** Never multiply unrelated field-level conditions into one "feasibility of the field" number: it describes no project anyone could build, so it cannot be acted on.
- **`horizons`:** `5,10` by default. Accept `5`, `5,10,15`, `h=7`. Allowed 1–15. The engine's ranges are validated up to about 10–11 years (Farmer & Lafond 2016); beyond 10 say so in bold and treat results as scenarios, not forecasts.

## What the evidence says (why the skill works this way)

These come from the research behind this skill; keep them in mind at every step.

1. **Trend + calibrated ranges beat experts on cost and performance.** A technology's own past rate, extended as a random walk with drift, with Farmer–Lafond ranges, was unbiased up to ~11 years across 53 technologies. Experts and big institutional models were systematically too pessimistic (PV: models expected −2.6%/yr for 2010–2020, actual ≈ −15%/yr). → The engine does this; don't overrule it with opinion.
2. **Models are bad at adoption timing; base rates are slow.** Median 32 years from invention to widespread use (Gross et al. 2018); TRL 3→9 took 12–16 years in documented hardware cases. Experts are better at *whether* than *when*. → Readiness and adoption get their own priors.
3. **Announcements overshoot.** ~11% of announced 2030 hydrogen capacity was past final investment decision (IEA 2025); 54–75% of announced EU battery capacity expected to be built. → Dated events are discounted by type and status.
4. **Floors get breached, ceilings don't.** Engineering cost floors are tied to one chemistry/architecture and are often beaten (battery "floor" $124/kWh vs $108 average and $50 LFP by 2025). Physical limits (Shockley–Queisser, Betz, Landauer) cap performance. → Floors are soft unless the target is past a real physical limit.
5. **S-curve fits before the inflection can't find the ceiling.** → Never fit an asymptote; set ceilings from physics or market size, as scenarios.
6. **Biases point both ways.** Mass-manufactured, modular products (chips, panels, batteries, software) usually beat forecasts; large site-built projects (nuclear, big infrastructure) usually miss them. Long-range forecasts of physical technologies are less accurate than of information technologies. → Ranges widen beyond 5 years for physical domains.
7. **Timing kills.** Too early looks the same as wrong. → A "why now" gate and a start-window output.

## Non-negotiable rules

1. **No source, no number.** Every history point, floor, ceiling, event date, TRL claim and judgment probability has a source URL. Never fill from memory.
2. **All forecast math runs in the engine** (Appendix A). No hand-drawn trend lines, no endpoint-to-endpoint % in prose, no "I estimate 70%" without the engine or a cited source.
3. **Forecasts are conditional.** State the condition (trend continues; scenario X). Show scenario spread separately from statistical spread. Never average scenarios into one number.
4. **Check the method on the data first.** Run `hindcast` before `forecast`. If a series' 80% range covered less than 65% of past outcomes, widen it (scenario with `volatility_multiplier`) or downgrade it, and say so.
5. **Report the weakest link next to the joint probability.** Requirements are not independent; the joint is an estimate, the weakest link is a ceiling.
6. **Write every output as a resolvable prediction** (metric, threshold, date, probability) in `predictions_log.csv` so it can be scored later.
7. **Verify independently before delivery.** An agent that did not do the research checks sources.
8. **Anchor dates to today.** Get today's date first. `ORIGIN` = last full calendar year (history ends there; horizons count from it). Print ORIGIN and horizons at the top of the report.

## Setup

1. Task list with phases 1–9.
2. Working folder `trend_<project-slug>_<YYYY-MM-DD>/`. Copy the engine in (Appendix A) and run `python3 trend_predictor.py cpi`.
3. **Reuse PARADIGMA if there is a run for this field** (if PARADIGMA isn't installed, say once that it pairs with this skill: https://github.com/qaemu/paradigma-skill, and continue without it) (a `paradigma_<field>_*` folder with `points.csv`, `constraints.csv`, `noncost.csv`). The schemas are the same: copy those files in and extend them instead of re-collecting. Also copy `out_of_window.csv` (PARADIGMA v0.4.2+) and append its rows to `points.csv`: points older than PARADIGMA's window are exactly the longer history forecasting needs.
4. Create the CSVs from Appendix B.

## Phase 1: Turn the project into requirements

Write down, in one paragraph, what the project delivers, to whom, at what price, and what it competes with today. Then list the **requirements**: things that must be true for it to work. Use the PARADIGMA groups (components and hardware, manufacturing, software and AI, data, labor and skills, distribution, compliance and insurance, trust) and a PESTEL sweep.

For each requirement decide its **kind**:

- **curve:** a measurable cost or performance that must reach a **target value** (e.g. actuator cost ≤ $40 per joint; battery ≥ 400 Wh/kg). Derive the target from unit economics, not hope: target price to the customer, minus margin and other costs, gives the most this input can cost. If the project must beat an incumbent, the target is the incumbent's *projected* value at the horizon (forecast the incumbent too, and say so). Record the derivation in `requirements.csv:target_derivation`.
- **event:** a dated future change: a law in force, a patent expiring, a standard published, a factory or launch. Goes in `events.csv`.
- **readiness:** a specific component or process not yet proven at scale. Record the current TRL (1–9) **with evidence** (a paper, demo, pilot, product) and the TRL needed (usually 9). Use it only for a concrete artefact with an engineering path (a gripper, a cell chemistry, a sensor). "AI can do job X", "the market accepts Y" and similar capability or adoption claims are **judgment** requirements, not readiness: the TRL duration priors would make them look near-certain.
- **judgment:** anything else (customer behavior, insurer coverage, social acceptance). Needs a probability per horizon from a cited source: Metaculus/Manifold/Good Judgment Open questions, published expert elicitations, adoption studies, surveys. If none exists, see Phase 6.

Mark each as `critical` (project fails without it) or not. Aim for 5–12 requirements; more than 15 means the project is too vague: ask the user to narrow it.

**"Why now" gate.** Name the constraint that changed in the last 0–3 years (date, source) that makes this project possible now or soon. If none, write "no why-now: high too-early risk" in the report's first section.

If the project description is too vague to set targets (no price, no customer), ask once with AskUserQuestion: who pays, how much, and what it replaces. If nobody answers, choose the most common version, state it at the top, and continue.

## Phase 2: History for every curve requirement

Same rules as PARADIGMA Phase 2 (source priority, nominal/real, USD conversion with cited rate, one tier and generation per series). If an Agent tool is available, split the curves across 3–5 research agents with the Appendix C prompt.

Forecasting needs **longer** history than PARADIGMA: aim for **≥ 10 yearly values** and **≥ 3 independent sources**. The engine refuses fewer than 5 yearly changes. Short-history fields (e.g. AI token prices) still work, but their ranges are wide and grade C; say so.

For each curve also record, in `constraints.csv`:
- `floor` / `ceiling` with `bound_source` — only a **physical or thermodynamic limit**, or a materials floor with a cited materials-cost share. A floor tied to one chemistry or architecture is soft: leave it blank and mention it in the card instead.
- `domain`: `software | electronics | compute | ai | hardware | energy | infrastructure | materials | bio | medical` (sets widening and readiness priors).

## Phase 3: Forecast

```
python3 trend_predictor.py hindcast --end <ORIGIN>
python3 trend_predictor.py forecast --end <ORIGIN> --horizons 5,10 --plots
```

- **Read `calibration.csv` first, and quote it exactly.** Every calibration number in the report (coverage of the 80% and 95% ranges, bias) is copied from `calibration.csv`, the `ALL` row for the pooled figure. Never restate, round in your favour, or recompute it in prose. `calibrated` = trust the ranges. `bands too narrow` = add a scenario row with `volatility_multiplier` (1.5–2) and use it, or grade the series C. `too few checks` = say the ranges are untested.
- **Break check** (`series_fit.csv`): `slowing` or `accelerating` means the second half of the history moved at a different rate. Then the recent rate is the better guide: rerun with only recent years (filter `points.csv` into `points_recent.csv`, pass `--points`) and present both.
- **Scenarios** (`scenarios.csv`, optional, each sourced): `roadmap` (an industry roadmap's stated rate, e.g. IRDS, IEA), `wright` (learning rate × a cited deployment forecast: annual_change = (1−LR)^(log2 of yearly growth in cumulative production) − 1; write the arithmetic in `note`), `stall` (rate halves or stops, e.g. after a physical limit or subsidy end). Show them as dotted lines; never merge them. If you weight scenarios, the weights must sum to 1 (people's scenario probabilities typically sum to ~2 before renormalising).
- **Automatic repairs.** The engine checks every series and fixes what arithmetic can fix, recording each repair in `series_fit.csv:fixes_applied` and on the fan chart. Each is chosen by an explicit test, not by trying many fits and keeping the best one (that overfits noise):
  - **Mixed products** (values in the same year differ more than 3×): switches to the **best available value so far** (the price-performance frontier).
  - **Outliers** (a yearly change more than 5.5 robust SDs from typical): switches to a robust trend (Theil–Sen) and volatility (MAD).
  - **Trend changed** (drift in the last 15/10/8 years differs from the years before, z > 3.2 under Farmer–Lafond errors): fits on the recent window.
  - **Runs into a physical limit** (the straight trend crosses a sourced floor/ceiling inside the horizon): models the remaining gap to the limit, so progress slows as it approaches.
  - Tested on simulated technologies: on clean data the repairs trigger for 1–3% of series and leave accuracy unchanged; on a real slowdown they trigger in about half the cases and cut forecast error 20–37%. Check them anyway, and rerun with `--no-autofix` to show the default for comparison.
- **What arithmetic cannot fix → go get data.** `unresolved_warnings` lists what is left. For each series with `informative = NO` (80% range wider than 100× at the last horizon) or still `mixed products`/`hindcast biased`, do this **once**, automatically:
  1. Send a research agent (Appendix C prompt) for **denser** history: more data points per year, one product line or tier only, a longer span, or a primary dataset instead of launch prices (e.g. all GPU models per year instead of flagships; distributor price lists; a published learning-curve dataset).
  2. Merge, rerun `hindcast` and `forecast`.
  3. If it is still uninformative, keep it out of the headline: turn its requirement into a `judgment` requirement (Phase 6) and say in the report that the data cannot decide it.
- Look at every fan chart. A history that mixes tiers or generations gives false volatility: split and rerun.

## Phase 4: Dated events

Search for every scheduled change that touches a requirement in the window ORIGIN to ORIGIN + max horizon:
- **Laws and rules with effective dates:** official gazettes (Federal Register, EUR-Lex, Boletín Oficial), regulator calendars. Check for delays and omnibus revisions (e.g. the EU AI Act's 2026 deferral of high-risk obligations).
- **Patent expiries:** Google Patents / Lens.org. Expiry ≈ filing + 20 years, marked approximate (extensions, SPCs, term adjustments). Check the jurisdiction: core patents can expire in one country and not another (semaglutide 2026: China, India, Brazil yes; EU protected to 2031).
- **Capacity and launches:** fabs, gigafactories, satellite constellations, product launches. Record the **status**: announced, fid (final investment decision), under_construction. Count only what the source states.
- **Standards:** ISO/IEC/IEEE drafts and publication dates.

The engine applies base-rate priors by type and status (Appendix A, `EVENT_PRIORS`). Override only with a cited reason (`p_on_time_override`, `p_eventual_override`, `override_source`).

## Phase 5: Readiness and adoption

- **Readiness:** for each `readiness` requirement cite the evidence for the current TRL (lab demo = 4, prototype in relevant environment = 6, operational system = 7–8, proven in real use = 9). The engine uses a duration prior per TRL step by domain (Appendix A, `READINESS_PRIORS`). If the field's own history shows a different pace (e.g. a similar component went TRL 5→9 in 4 years), pass `years_per_step` with its source.
- **Adoption** is separate from feasibility. Feasible ≠ adopted. For the report, give the adoption base rate for the closest reference class (Gross et al. 2018: invention→market ~18 years median, market→20% of peak ~18 more; consumer products faster than power generation). A path to wide adoption in under 5 years needs a named reason: software distribution, a drop-in replacement for something already bought, or a mandate.
- **Adoption readiness (DOE ARL):** rate the 4 risk areas Low/Medium/High with one line of evidence each: value proposition, market acceptance, resource maturity (supply chain, workforce, capital), license to operate (regulation, permitting, social acceptance). High-risk areas become `judgment` requirements if they are critical.

## Phase 6: Judgment inputs

For each `judgment` requirement, in this order:
1. A **crowd forecast**: Metaculus, Manifold, Good Judgment Open. Record the question URL, the probability and the date read. Crowds are best for 1–3 year milestones; beyond that, use them only as a prior.
2. A **published expert elicitation or survey** (e.g. LBNL wind experts, adoption surveys).
3. If neither exists, run an **IDEA-style estimate**: two fresh agents, each given only the requirement and the evidence files (not each other's answer), each writes a probability for +5 and +10 with reasons. Show each the other's reasons, ask for a second private estimate, and take the mean of the second round. Label the source `IDEA-agents (no external forecast found)` and grade it Low. Never weight by self-rated confidence.

Start every judgment from the **outside view**: what fraction of similar things in the past happened within this many years? Then adjust for specifics. Write both numbers.

## Phase 7: Score feasibility

```
python3 trend_predictor.py feasibility --end <ORIGIN> --horizons 5,10 --lead-years <L> --plots --title "Feasibility: <project>"
```

- `--lead-years`: how long it takes to build and launch the project once the constraints allow it (cite or justify; typical: software 1, hardware product 2–3, regulated medical 5+).
- Outputs: `feasibility.csv` (per requirement and horizon, plus the full year-by-year path and median crossing year), `project_score.csv` (joint probability, weakest link, verdict, start window), `plots/feasibility.png`.
- **Verdicts:** LIKELY FEASIBLE (weakest ≥ 80% and joint ≥ 60%), PLAUSIBLE (joint ≥ 35%), LONG SHOT (≥ 12%), UNLIKELY (< 12%).
- **UNCERTAIN (applied by the engine).** Every requirement gets an `evidence_grade` in `feasibility.csv`: curves inherit their series grade (A–D); judgments are Low when the probability came from this run's own estimators (IDEA) and Medium when it cites an external forecast, elicitation or survey (set `evidence_grade` in `requirements.csv` to override, with the reason in `note`); readiness and events are Medium with cited evidence, Low without. When the weakest critical requirement's evidence is C, D or Low, `project_score.csv` reports **`UNCERTAIN (driven by <req>)`**, and keeps the score in `verdict_if_inputs_hold`. Report the UNCERTAIN verdict as the headline. You may show `verdict_if_inputs_hold` next to it, labelled as conditional, never instead of it. The way to remove UNCERTAIN is better evidence for that requirement (denser data, a crowd forecast, a published elicitation), not a different label.
- **Start window:** the first year the joint probability passes 50%, minus the lead time. "Start building by YYYY." If that year has passed, the project is buildable now; if it never comes within the horizons, say which requirement holds it back.
- **Sensitivity:** for the weakest link, rerun with its target ±25% and with the `stall` scenario. Report how much the verdict moves. A verdict that flips on a ±25% target change is fragile; say so.

**Pre-mortem.** Assume it's ORIGIN + 10 and the project failed. Write the 3 most likely reasons. Check each against the failure modes: linear extrapolation of a curve that bent; trusting announced capacity; adoption assumed as fast as feasibility; a complement missing (charging network, insurer, installer workforce); hype counted as traction; too early. If a reason isn't covered by a requirement, add one and rerun.

**Signposts.** For each critical requirement, write in `signposts.csv` what to watch and the value that would change the verdict. For curves, use `forecasts.csv` at ORIGIN + 2: the q100 and q900 values; a reading outside that 80% range means re-run. For events, the next decision date (vote, FID, examination). Set `recheck_date` (default: 12 months).

## Phase 8: Independent verification

A **fresh** general-purpose agent, given only the CSVs, opens every source URL and checks: every point behind an A/B series (or a random 40 if more than 150), every floor/ceiling, every event date and status, every TRL claim, every judgment source. It writes `verification.csv` (MATCH / MISMATCH / UNVERIFIABLE). Fix, rerun phases 3 and 7, report the pass rate. Without an Agent tool, do it yourself as a separate pass and say it was self-checked.

## Phase 9: Deliverables

1. **Report.** Use the Docs artifact type if listed, otherwise an HTML page. Write for a reader with no forecasting background; explain each term once. Sections:
   1. **Verdict** (one screen): project, ORIGIN, horizons, date. Verdict per horizon with joint probability and weakest link. Start window. Why-now result. The one thing to watch.
   2. **Feasibility chart** (`plots/feasibility.png`) and a table: requirement, kind, P(+5), P(+10), median crossing year, grade/source.
   3. **Requirement cards:** target and how it was derived, fan chart (`plots/fan_<id>_<tier>.png`), trend and volatility, calibration result, break check, scenarios, floor/ceiling, P per horizon, what would change it.
   4. **Dated events timeline** with statuses and the probability each holds.
   5. **Readiness and adoption:** TRL path, ARL table, adoption base rate and the gap between "feasible" and "adopted".
   6. **Pre-mortem and signposts.**
   7. **Method and confidence:** calibration summary, which numbers are judgment defaults (event priors, readiness priors, widening), verification pass rate, data gaps, what would most improve the forecast.
   8. **Sources.**
2. **Workbook:** `python3 trend_predictor.py workbook --project "<project>" --field "<field>" --end <ORIGIN> --date <YYYY-MM-DD>`.
3. **Predictions log** (`predictions_log.csv`): one row per resolvable claim. On a re-run, first score the previous log (Brier score per claim, against 0.25 for always saying 50%) and show it at the top: that is how the skill learns whether to trust itself.
4. **Final reply:** 3–5 lines: verdict per horizon, weakest link, start window, main caveat, deliverables. Offer once to set a scheduled task to re-run on the recheck date.

## Interpretation rules

- **Not prophecy.** "61% by 2035, if the 2010–2025 trend continues" — always with the condition.
- **Grade C/D series and Low-grade judgments can't carry the headline.** The engine enforces this (UNCERTAIN verdict, see Phase 7); don't override it in prose.
- **Feasible ≠ adopted ≠ profitable.** Say which one each number is about.
- **Don't argue with the calibrated trend on cost and performance** unless a break check or a cited physical limit says to. Argue freely about adoption.
- **Beyond 10 years, scenarios only.**

## Appendix A: the engine

`scripts/trend_predictor.py`, next to this SKILL.md. Copy it into the working folder, in this order:
1. from the `scripts/` folder beside this SKILL.md (Claude Code: `${CLAUDE_SKILL_DIR}/scripts/trend_predictor.py`);
2. from the user's local copy of the plugin, if the session can reach it;
3. if the host loaded only SKILL.md: `curl -fsSL https://raw.githubusercontent.com/qaemu/trend-predictor-skill/main/skills/trend-predictor/scripts/trend_predictor.py -o trend_predictor.py`.

Never rewrite the engine from memory. If none works, stop and tell the user the engine is missing.

Subcommands: `cpi`, `hindcast`, `forecast`, `feasibility`, `workbook`. `-h` for options. Needs pandas, numpy, matplotlib; scipy for exact Student-t; openpyxl for `workbook`.

**Method (Farmer & Lafond 2016).** Yearly medians on log scale; drift μ = (y_last − y_first)/years (the published, hindcast-validated form; `--drift theilsen` if the first year is an outlier); volatility K from yearly changes, gaps scaled by √Δt; forecast median = y_last + μτ; spread K·√(A*/(1+θ²)) with A* = −2θ + (1 + 2(m−1)θ/m + θ²)(τ + τ²/m), θ = 0.63; Student-t quantiles with m−1 degrees of freedom. On simulated technologies this gives about 77% / 93% coverage for the 80% / 95% ranges.

**Judgment defaults (tunable, labelled in every report):**
- `EVENT_PRIORS` (P by scheduled date / within 3 years after): patent granted 0.90/0.97; regulation enacted 0.75/0.92, proposed 0.30/0.55; standard published 0.95/0.98, draft 0.45/0.75; capacity announced 0.25/0.45, FID 0.60/0.85, under construction 0.75/0.92; launch announced 0.45/0.70, with dated contract 0.65/0.85.
- `READINESS_PRIORS` (median years per TRL step, log-sd of total): software 0.6, electronics 1.3, hardware 2.0, bio 2.2, energy/medical/materials 2.5, infrastructure 3.0; log-sd 0.6–0.7.
- `WIDEN`: physical domains get spread × (1 + 0.4·(h−5)/5) beyond 5 years; information domains none. `--widen` to change.

## Appendix B: CSV schemas

Same as PARADIGMA for `points.csv`, `noncost.csv`, `companies.csv`, `verification.csv`.

**constraints.csv** — PARADIGMA columns plus `floor,ceiling,bound_source,domain`.

**requirements.csv**
`req_id,description,kind,critical,constraint_id,tier,target_value,better,target_derivation,scenario,event_id,current_trl,needed_trl,trl_evidence_url,years_per_step,domain,p_now,p_5y,p_10y,source_url,evidence_grade,note`
- `kind`: `curve | event | readiness | judgment`. Fill only the columns that kind uses.
- `evidence_grade` (judgment, optional): `High | Medium | Low`. Blank = inferred (IDEA agents → Low; cited external source → Medium).
- `p_Ny` (judgment): probability by +N years; any horizons, e.g. `p_3y`.

**events.csv**
`event_id,description,type,status,jurisdiction,date_scheduled,source_url,p_on_time_override,p_eventual_override,override_source,note`
- `type`: `regulation | patent_expiry | standard | capacity | launch | other`. `status`: `enacted | proposed | granted | published | draft | announced | fid | under_construction | dated_contract | any`.

**scenarios.csv** (optional)
`constraint_id,tier,scenario,annual_change_pct,volatility_multiplier,source_url,note`

**signposts.csv**
`req_id,watch,on_track_range,trigger_value,next_check_date,recheck_date,source_url`

**predictions_log.csv**
`claim_id,run_date,claim,metric,threshold,resolve_date,probability,resolved_value,outcome,brier,source`

**Engine outputs:** `series_fit.csv`, `forecasts.csv` (q025…q975 per year and scenario), `hindcast.csv`, `calibration.csv`, `feasibility.csv` (with `evidence_grade` per requirement), `project_score.csv` (with `weakest_evidence`, `verdict`, `verdict_if_inputs_hold`), `rejected_points.csv`, `plots/fan_*.png`, `plots/feasibility.png`, `trend_predictor_<project>.xlsx`.

**Series grades:** A = ≥15 yearly changes, ≥3 sources, data no older than ORIGIN−2. B = ≥8 changes, ≥2 sources, ≤3 years stale. C = usable but weak, or an unresolved warning (a repaired series is at most B). D = fewer than 5 changes: no forecast.

## Appendix C: research agent prompt

> You are collecting sourced history for a forecast of **<CONSTRAINTS>** for the project **<PROJECT>** (<REGION>). Today is <DATE>; history ends <ORIGIN>.
> Return ONLY CSV rows with this header: <points.csv header>.
> - Every row needs a source URL you opened. Never estimate or recall numbers. Leave missing years out.
> - Go back as far as consistent data exists (aim ≥ 10 years, ≥ 3 independent sources). One tier and product generation per series.
> - Values exactly as published, with currency, nominal/real basis and date precision.
> - Also report any physical limit or materials-cost floor for the metric, with source.
> - Priority: primary datasets (Our World in Data, Santa Fe Performance Curve Database, Epoch AI, IEA, NREL, USGS, BLS/FRED, NHGRI, learning-curve papers), then price lists and Wayback snapshots, then reputable press.
> After the rows, up to 5 lines on coverage gaps.
