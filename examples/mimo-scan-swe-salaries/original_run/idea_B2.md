# IDEA structured judgment — Estimator B, ROUND 2

Read estimator A's round-1 note (`idea_A1.md`) after finalizing my round-1. All updates below are responses to A's specific arguments/evidence. J4 definition re-verified against the primary BLS Table 3 (fetched 2026-10-17).

| Req | R1 (B) | **R2 (B)** | A's R1 | Direction |
|---|---|---|---|---|
| J1 | 35 / 45 | **45 / 60** | 55 / 70 | up |
| J2 | 55 / 65 | **50 / 60** | 45 / 55 | down |
| J3 | 20 / 30 | **25 / 35** | 30 / 40 | up slightly |
| J4 | 20 / 30 | **30 / 40** | 55 / 65 | up slightly |

---

## J1 — P(2030) = 45%, P(2035) = 60% (was 35/45)

**Biggest reason I moved:** A sourced a newer, directly contradictory Indeed Hiring Lab piece — "AI and job postings: from destruction to creation" (2026-07-08): software-dev postings +15% since Claude Code's late-Feb 2025 launch while overall postings fell. My round-1 mechanism (AI "preventing a bounce-back," Indeed Hiring Lab 2025-07-30) was the best evidence I had, but A's source is 11 months newer and comes from the same lab, attributing the rebound *to* agentic AI. My title-level attrition argument stands as a cap, not as a headwind against the recovery itself. Also accepted A's momentum arithmetic: ~44% of the 61→100 gap closed in 17 months; only ~6%/yr needed versus ~20%/yr recent.

**Accepted from A:** the "destruction to creation" Hiring Lab finding; the trough (61.1, May 2025) and gap-closed calculation; the measurement hazard (Indeed-platform index, seasonal-adjustment changes could resolve it on a non-economic series).

**Rejected from A:** their P(2035) = 70%. A's own reason 3 defeats most of their 2035 number: 71% of the recovery came from senior roles, entry-level postings 4.5% of the total, and their crowd anchor expects dev employment −5.3%/−9.5% (mine reads the same Metaculus question as −6.6%/−11%). Postings +28%/+55% over an employment base expected to *shrink* implies a large intensity-per-engineer rebound; plausible but not a 70% proposition. I moved up on their evidence but kept the composition cap as my main source of residual doubt.

---

## J2 — P(2030) = 50%, P(2035) = 60% (was 55/65)

**Biggest reason I moved:** A documented the flatness of the holdout share from the primary data page (survey.stackoverflow.co/2026/ai/data): non-users 16.2% (2025) → 17.2% (2026), i.e. *not shrinking* while my "asymptotic tail" story assumed slow erosion. Crossing 90% requires the never-user share to fall by a third from a two-year plateau. This is a better-sourced measurement than my generic S-curve reasoning.

**Accepted from A:** the flat non-user share (16–17% for two years); the 2026 question rewording ("Do you currently use AI tools or AI agents…," no "plan to use" option) — this is the concrete instance of the metric-continuity risk I had only flagged as a possibility; the sentiment cooling among learners (72.1% → 52.8%) and only 7% trust for important decisions, as counterweights to my trust-jump datapoint.

**Rejected from A:** treating the rewording as near-fatal to resolution. "Currently use" is a *subset* of "using or planning" — if the current-use reading reaches 90%, the requirement is satisfied under any reasonable interpretation; only complete discontinuation of the item is truly unresolvable. And I keep my round-1 intensity evidence (daily assistant use 51%→73%; 10.6% of switchers citing employer mandate; trust jumping to 87%), which is why I stay above A's 45/55: mandates and enterprise diffusion still push the last ~8pp over a 10-year window even from a flat plateau.

---

## J3 — P(2030) = 25%, P(2035) = 35% (was 20/30)

**Biggest reason I moved:** A's Live Data Technologies datapoint — at 28 large US tech companies in 2025, ~1 in 10 engineering hires was a recent grad (vs SignalFire's 7% at big tech) — is genuine evidence that the metric *family* straddles the 10% threshold on live samples. It raises the probability that the named SignalFire-style metric prints ≥10% on definitional/sampling slippage (intern-to-full-time conversions, "recent grad" vs "new grad") even if the structural recovery is weak.

**Accepted from A:** the vendor-disagreement/resolution-noise argument (7% vs ~10% on different samples); the Live Data "intern intakes haven't bounced back" evidence; the senior-supply-squeeze offset for the 2032–2035 window.

**Rejected from A:** their level. A explicitly found *no* matching crowd forecast and estimated from base rates alone. My round-1 anchor — the LEAP/FRI panel (n=253 experts + 59 superforecasters, exact-metric question, updated Aug 2026): expert median 7.0% (2030), 7.8% (2040), superforecasters 10% only by 2040 — remains the single best source on this question and supports *stagnation below 10%*. The expert panel's distribution absorbs the same noise and reversion-vs-structure debate A and I discuss. Net: small upward adjustment for metric noise, not an acceptance of 30/40.

---

## J4 — P(2030) = 30%, P(2035) = 40% (was 20/30)

**Definition (locked, same as round 1):** share of *US software developers* (SOC 15-1252, narrow) who are **covered by a union or employee-association contract** ("represented," BLS footnote 2), regardless of membership.

**Biggest reason I moved:** A's direction-of-travel evidence is concrete, recent, and better than my purely structural bearishness: UC's ~2,100 tech workers voting 96% yes (May 2026), 67% of 1,900 Blind respondents saying they'd join a union, 68% Gallup approval, CWA's ~400 digital-media companies. Combined with the discontinuity I already conceded (one 20–30k-engineer unit clears 3% ≈ ~50k covered devs on its own), this warranted a real move.

**Also re-verified myself:** I fetched BLS Table 3 (2025): computer & mathematical occupations 3.7% members / 4.4% represented (285k of 6,517k); public sector overall 36.4% represented. Confirms neither estimator can get a developer-specific rate from published tables — the whole question is a composition estimate.

**Accepted from A:** the organizing-momentum datapoints above; their developer-only point estimate (2.5–3.5%) as a plausible straddle — my round-1 ~1–2% likely under-counted public-sector developer bargaining units (state/local coverage is 33–41%), so a straddling base rate is fairer than mine.

**Rejected from A:** their headline logic that the condition is "already borderline-satisfied at ORIGIN." Under my stated definition — software developers specifically, not the parent computer-&-math group — 4.4% is the wrong denominator's rate; developers are plausibly below it and 3% is not yet crossed. A's own 55/65 treats the occupation-group proxy as near-resolving; under the definition I locked, that reading is inadmissible, and their conditional "narrow reading" numbers (40/50) are the only ones comparable to mine — still above my 30/40 because I weight the hostile federal backdrop and employer-resistance evidence they under-weight.

---

## Summary of round-2 pairs

- **J1: P(2030) = 45%, P(2035) = 60%**
- **J2: P(2030) = 50%, P(2035) = 60%**
- **J3: P(2030) = 25%, P(2035) = 35%**
- **J4: P(2030) = 30%, P(2035) = 40%** — definition: US software developers (SOC 15-1252) **covered by a union or employee-association contract** (BLS "represented" concept), not the computer-&-math occupation group.
