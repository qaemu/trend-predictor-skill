# IDEA structured judgment — Estimator A, ROUND 2

Read B's round-1 (`idea_B1.md`) on 2026-10-17. ORIGIN = 2025; horizons = calendar-year-end 2030 / 2035. Updates made only where B's reasoning or sourcing actually beats mine.

| ID | R1 (2030/2035) | **R2 (2030/2035)** | Direction |
|----|---------------|--------------------|-----------|
| J1 | 55 / 70 | **55 / 70** | unchanged |
| J2 | 45 / 55 | **50 / 60** | up |
| J3 | 30 / 40 | **25 / 35** | down |
| J4 | 55 / 65 | **30 / 40** | down (definition chosen) |

---

## J1 — P(2030) = 55%, P(2035) = 70%

**Unchanged because** B's case rests on older evidence plus a crowd reading I had already priced in. Their title-mix fact is genuinely good (Indeed 2025-07-30: SWE titles −49%, mobile/web/.NET −60% vs early 2020, ML/AI +59%, Indeed's own "AI could be preventing a bounce-back"), and it strengthens my composition argument — but it is superseded on the causal point by the newer Hiring Lab analysis I cited (2026-07-08: US software-dev postings +~15% since Claude Code's launch while overall postings fell 7%), which says the same force B calls a headwind is now the tailwind. Their Metaculus reading (−6.6% / −11%) matches the −5.3% / −9.5% (and −8.6% / −14.3%) I already used as my downward anchor. Their outside view (45/60) is statistically the same as mine (40/65).

- **Accepted:** the title-family attrition data as extra weight against a clean V — folded into my existing senior/junior composition concern; and their FRED reading (78.1 on 2026-10-09) as confirmation, not change, of my series.
- **Rejected:** "AI is preventing a bounce-back" (2025-07-30 vintage) — the 2026 Hiring Lab release contradicts it with post-Claude-Code data. Also rejected their implied sharp cut to 35/45: B under-weights the fact that 44% of the 61→100 gap closed in 17 months and concedes that ~8%/yr hits 100 around 2029.

---

## J2 — P(2030) = 50%, P(2035) = 60%

**Biggest reason I moved up:** B's implicit *multi-wave lottery* point that I under-weighted — I evaluated the threshold as if one reading decides it, but the window contains ~5 survey waves (2027–2031), and the item's "using **or planning to use**" wording is cheap to answer affirmatively once tools are embedded in IDEs, browsers and employer policy. One loose-worded or composition-shifted wave touching 90% is materially more likely than the flat 83–84% trend alone suggests. Second factor: enterprise mandates (10.6% of 2026 switchers, one-directional) erode the holdout share slowly but persistently.

- **Accepted:** the aspirational-wording argument and the mandate-erosion asymmetry; also B's framing that a plateau at 83–84% still leaves the threshold within one wave's reach.
- **Rejected:** B's intensity/trust evidence as a driver of the *headline* metric (daily use 51→73%, "some level of trust" 31→87%) — that is movement among existing users, not conversion of the 16–17% never-user share, which is what the threshold requires. Their trust number is also a different question from the 7%-for-important-decisions figure I cited. And I reject moving to their 55/65: two consecutive flat readings on a share that must fall by a third is still the dominant empirical fact.

---

## J3 — P(2030) = 25%, P(2035) = 35%

**Biggest reason I moved down:** B found a near-direct-match expert forecast I reported as nonexistent — the FRI/LEAP panel (n=253 experts plus 59 superforecasters) on essentially this metric: median **7.0% (end-2030)**, 7.8% (end-2040), superforecasters 8% (2030) / 10% (2040), with P75 ≈ 10–11% at 2030. That is strictly better sourcing than my analogy-based outside view, and it dominates it. A purpose-built panel never reaching ≥10% before 2040 moves me below my round-1 numbers.

- **Accepted:** the LEAP panel as the anchor; and their point that the offsetting forces (retirement-driven pipeline rebuilding, AI-native junior roles) work on 5–10-year lags, not by 2030.
- **Rejected — and the reason I stay above B's 20/30:** (a) B's own admitted metric gap — LEAP asks "≤1 year of total experience at the top 15 tech companies," SignalFire asks new-grad share of big-tech hires, and intern-to-full-time conversions can lift the latter while LEAP stays at 7%; (b) my Live Data finding (2026-06-09: 1 in 10 engineering hires at 28 large US tech firms in 2025 was a recent grad) puts a *different sample* of the same construct already at ~10%; (c) LEAP was fielded Nov–Dec 2025, on the trough, and B flags this too. A modest premium over B is warranted — not a split for its own sake.

---

## J4 — P(2030) = 30%, P(2035) = 40%

**Biggest reason I moved down:** I accepted B's definitional reasoning and therefore abandoned the occupation-group proxy that carried most of my round-1 55/65. The CPS *computer & mathematical* group (4.4% represented at ORIGIN) is padded by public-sector IT, telecom/hardware support, security analysts and quants; software developers as a class sit well below the group rate. My round-1 claim that "the threshold sits at today's level" was an artifact of the group reading, and once dropped, the base rate reverts to the white-collar organizing reference class, which is much lower. B's ~1–2% origin estimate for developers specifically is more consistent with the organized-share evidence (AWU ~1.4k members, game-studio CWA units in the hundreds) than my 2.5–3.5% guess.

- **Accepted:** the definition trap itself; that no pro-union legal change is in the window; that H-1B regime shifts raise employer leverage; that the outcome turns discontinuously on one large contract.
- **Rejected — and the reason I stay above B's 20/30:** B does not engage my 2026 organizing-momentum evidence (67% of 1,900 Blind respondents would join a union; 2,100 UC tech workers 96% yes, May 2026; Gallup 68% approval; CWA's ~400 digital-media companies), and B's own point 3 concedes the upside tail is discontinuous. Since a developer-specific point estimate plausibly straddles 3% (CPS sampling error ±0.5pp, plus the possibility of a definitional/statistical jump), a coin-flip-plus-tail is the honest posture — but well below my round-1 number. I also rejected B's implicit fork-averaging: I do not report 95/97 for the group reading (see definition below).

---

## My J4 definition (stated and held)

**J4 = the share of US *software developers* (SOC 15-1252, i.e. the narrow developer occupation, not the CPS computer & mathematical group) who are *represented* by a collective bargaining agreement — covered by a contract, not merely union members — as measured at calendar-year-end.** Threshold: ≥ 3%. Under this definition the condition is **not** satisfied at ORIGIN; origin coverage is plausibly ~1–2.5%, and my 30% / 40% is the probability of crossing 3% by year-end 2030 / 2035. I reject the occupation-group reading (which would make the item already true at ~95%) as inconsistent with the requirement's wording "software developers."
