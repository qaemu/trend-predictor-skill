# IDEA structured judgment — Estimator B (independent)
Judgment requirements J1–J4 for US software-engineering salaries/workplaces. ORIGIN = 2025; horizons +5 = by 2030 (any year-end 2026–2030 inclusive, index/threshold read at Dec 31), +10 = by 2035. Estimate date: 2026-10-17. All URLs below were opened on 2026-10-17 unless flagged.

---

## J1 — Indeed US software-development postings index ≥ 100 at year-end

**Current state (fact, not forecast):** index = **78.1 on 2026-10-09** (FRED series IHLIDXUSTPSOFTDEVE, https://fred.stlouisfed.org/data/IHLIDXUSTPSOFTDEVE), up from 67.3 at end-2025 (+16% in ~9.5 months). Need +28% more by end-2030, +55% by end-2035.

**Outside view (base rate ~45% for +5, ~60% for +10):** Deep sectoral hiring busts usually reverse on the macro cycle. Reference classes: the dot-com bust (computer & math employment −23% 2001→2004, regained its 2001 peak ~2006–07, i.e. ~5–6 yrs); post-2008 JOLTS openings took ~5 years from trough to regain pre-crisis level. Conditioning on a trough in late-2024/2025, ~half of such episodes recover the prior level within 5 years, ~two-thirds within 10 — *for purely cyclical crashes*.

**Adjusted: P(by 2030) = 35%, P(by 2035) = 45%.**

Three main reasons:
1. **Cyclical rebound is already running** — 67.3 (Dec 2025) → 78.1 (Oct 2026); Indeed Hiring Lab finds tech-vs-economy posting ratios have held steady since late 2023 ("macro dominates" reading), and their metro-level evidence (Austin vs Boston) also tracks local macro, so a normal macro upswing alone carries the index a long way.
2. **The mix inside the index is structurally damaged by AI substitution** — Indeed's own title-level data: software engineers −49%, Android/Java/.Net/iOS/web developers −60%+ vs early 2020, while ML/AI titles are +59% (Indeed Hiring Lab, 2025-07-30, https://hiringlab.indeed.com/2025/07/30/the-us-tech-hiring-freeze-continues/). Indeed's own conclusion: AI "could be preventing a bounce-back." The recovery must come from exactly the titles that emptied.
3. **Closest crowd anchor is bearish on demand** — Metaculus community, "US software developer % change vs 2025" (https://www.metaculus.com/questions/42613/ and https://www.metaculus.com/labor-hub/jobs/software-developers/, read 2026-10-17): median **−6.6% by 2030, −11% by 2035** (P25–P75 for 2030: −20.4% … +6.5%). The crowd expects employment *below* 2025 levels at both horizons, which is hard to square with postings +28–55%.

**Crowd forecast found:** none matches the postings-index condition itself. Metaculus Q42613 (above) is the nearest proxy and is used as an adjustment, not an anchor.

**What would change my mind:** Up — index prints ≥85 at end-2027 (on trend from the current rebound) → P2030 to ~55%; any AI-boom capex cycle that lifts postings broadly. Down — index re-tests <70 in 2027 (recession or agent displacement of mid-level roles accelerating), or SignalFire/Canaries-style data showing developer headcount falling fast → P2035 to ~25%.

**This number is wrong if:** a macro recession plus AI-driven title attrition keeps the index under ~85 through 2030 (I over-weighted cyclical mean reversion), or if the 2026 rebound extends at ~8%/yr (I under-weighted current momentum — it would hit 100 around 2029).

---

## J2 — ≥90% of professional developers "using or planning to use AI tools" (Stack Overflow)

**Current state:** 70% (2023) → 76% (2024) → 84% (2025); 2026 survey ~83% "use AI tools" (press summary of the 2026 release, https://www.comparethecloud.net/news/stack-overflows-2026-developer-survey-83-use-ai-tools-but-only-66-trust-ai-for-important-decisions), i.e. the headline metric has **plateaued ~83–84%**. Underneath it keeps intensifying: 73% of respondents now use coding assistants/agents daily, and "some level of trust" in AI outputs jumped 31% → 87% (https://survey.stackoverflow.co/2026/ai and https://survey.stackoverflow.co/2026/).

**Outside view (base rate ~50% for +5, ~65% for +10):** Adoption metrics asymptote below 100% — smartphone ownership plateaued ~85%, and the last 10–15% of any user base is the hardest (holdouts are principled, not poor). But this particular question is aspirationally worded ("or *planning* to use") and rides ubiquity: once tools are embedded in every IDE, browser and enterprise policy, "plan to use" costs nothing. Base rate for a metric already at 83–84% touching 90% in at least one survey year within 5 years ≈ coin flip; within 10 years ≈ two-thirds.

**Adjusted: P(by 2030) = 55%, P(by 2035) = 65%.**

Three main reasons:
1. **The curve is flattening exactly where 90% sits** — +6pp (2023→24), +8pp (2024→25), −1pp (2025→26): the easy adopters are in; crossing 90% requires converting resistant professionals, and S-curve tails are sticky.
2. **Underlying usage intensity and institutional pressure still push the tail** — daily coding-assistant use 51% (2025) → 73% (2026); trust 31% → 87% in one year; 10.6% of 2026 tool-switchers moved "because my organization required it" (https://survey.stackoverflow.co/2026/ai) — enterprise mandates erode holdouts slowly but one-directionally.
3. **The resistant tail is ideological and will not vanish** — among respondents who avoid AI: 17% fear losing skills, 15% cite morals/ethics, 13% privacy/security (2026 survey) — plus regulated-industry (finance/defense/health) restrictions that keep a floor of ~10% non-users in any respondent pool.

**Crowd forecast found:** none matching (searched Metaculus/Manifold for SO-survey AI-adoption thresholds). Nearest but non-matching: Metaculus "What percent of US workers will use AI daily?" — median 52.9% (2030), 65.8% (2035) (https://labor-hub-tools.metaculus.com/question-statistics, read 2026-10-17). Different population and metric; not used as anchor.

**What would change my mind:** Up — SO 2027/2028 headline ≥88% → P2030 to ~75%. Down — two consecutive readings ≤83%, or Stack Overflow dropping/rewording the "using or planning" question (the 2026 survey already reworked its AI chapter — metric-death is a live resolution risk) → treat as unresolved and cut P2030 to ~40% under a strict "as published" reading.

**This number is wrong if:** the survey's respondent base keeps drifting (31.9k → 30.9k responses, composition shifting toward AI-forward regions/roles), producing a reading ≥90% on composition change alone (I would then have over-weighted the plateau), or if privacy/regulation backlash hardens (I would have over-drifted upward).

---

## J3 — ≥10% new-grad share of big-tech hires (SignalFire metric: 15% 2019 → 7% 2025)

**Crowd/expert forecast found — DIRECT MATCH, used as the anchor:**
- **FRI/LEAP "Entry-Level Share of Big Tech Hiring"** — https://leap.forecastingresearch.org/forecasts/entry-level-tech-hiring (collected Nov 20–Dec 16 2025, updated Aug 11 2026, read 2026-10-17). Question: "What percentage of new hires at the top 15 tech companies will have one year or less of total experience…" — same metric as SignalFire's. n = 253 experts (56 CS, 57 econ, 53 industry, 87 policy), 59 superforecasters, 814 public.
- Median forecasts: **Experts 7.0% (end-2030), 7.8% (end-2040); Superforecasters 8% (2030), 10% (2040); Public 7% (both)**. By 2040 the expert distribution gives 25% chance ≤4.0% and 25% chance ≥13% — i.e. the expert panel puts P(≥10% at any point to 2040) at roughly one third, and by 2030 clearly below that.

**Adjusted: P(by 2030) = 20%, P(by 2035) = 30** (2030 anchored on the LEAP distribution: median 7% with P75 ≈ 10–11%; 2035 interpolated between the 2030 and 2040 medians, where even superforecasters only reach 10%).

Three main reasons:
1. **A purpose-built expert/superforecaster panel on the exact metric never sees ≥10% before 2040** — the panel's central expectation is *stagnation at 7%*, and its own rationale split (reversion-to-mean vs structural AI shift) is priced into the 25/75 spread, not an afterthought.
2. **Current data still moves away from recovery** — SignalFire 2026: entry-level hiring ~65% below 2019 at majors, ~76% at early-stage startups; Stanford Canaries (rev. 2026-08-12): 22–25-year-olds in most AI-exposed occupations ~19% below counterfactual, adjustment **via hiring, not pay** — the mechanism that directly suppresses this share.
3. **The offsetting forces are real but slow** — Boomer/Gen-X retirements eventually force pipeline rebuilding, curricula are adapting to AI, and AI-native junior roles may emerge (these are the high-forecasters' reasons, and why the expert P75 reaches 13% by 2040); but each works on a 5–10+ year lag, not by 2030.

**What would change my mind:** Up — SignalFire's next annual report (or LEAP's next update) showing the share ≥9% (would take P2030 to ~40%); a large, public "AI-era new-grad academy" program at 2+ hyperscalers. Down — share falling to ~4–5% (Canaries mechanism deepening): P2035 to ~15%.

**This number is wrong if:** the metric definition drifts (LEAP measures "≤1 year experience at top-15 tech companies"; SignalFire measures new-grad share of big-tech hires — a firm counting intern-to-full-time conversions could print ≥10% while LEAP's number stays at 7%), or if the LEAP panel (fielded Nov–Dec 2025) is anchoring on a stale trough and the 2026 hiring thaw already lifted the share (my 2030 number would then be too low).

---

## J4 — ≥3% of US software developers covered by a union or collective bargaining agreement

**Current state — the base rate is nearly the whole story:** In BLS CPS "Union Members — 2025" (released 2026-02-18, https://www.bls.gov/news.release/union2.htm, Table 3, read 2026-10-17): **computer & mathematical occupations are already at 3.7% union members / 4.4% represented by a contract** (239k and 285k of 6,517k, 2025) — above the 3% threshold *at ORIGIN*. But this group spans all IT support/analyst/quant/public-sector roles; **software developers specifically are a subset**, with covered developers concentrated in public-sector IT bargaining units and a handful of organized shops (Alphabet Workers Union ~1.4k members; game-studio CWA units in the hundreds) — dev-specific coverage is plausibly ~1–2%, i.e. **not yet crossed**. I forecast on the strict reading of the requirement ("software developers").

**Outside view (base rate ~15–25% for +5, ~25–35% for +10):** US unionization has drifted down for 40 years (10.0% of all workers 2025 vs 20.1% in 1983; private-sector professional occupations sit at 1–4%). Reference class "white-collar occupation triples-or-halves-its coverage within 5 years absent legal change": rare. But the threshold is low (3% ≈ ~50k covered developers) and one large contract can move it discontinuously.

**Adjusted (strict "software developers" reading): P(by 2030) = 20%, P(by 2035) = 30%.**
**Definitional fork, stated not averaged:** if resolution uses the CPS computer-&-math "represented" rate (4.4% at ORIGIN), the condition is **already true** — P ≈ 95%/97%, with only small risk from sampling drift or a strict "developers only" re-tabulation. The requirement as written says *software developers*, so 20%/30% is my estimate; the whole J4 outcome turns on which definition the scorer uses.

Three main reasons:
1. **No pro-union legal change is in the window** — the federal environment is hostile to new private-sector coverage (the FTC non-compete episode showed how fast worker-favourable rules die: set aside 2024, vacated 2025, removed from CFR 2026, per our noncost.csv); card-check or sectoral-bargaining legislation is not on any plausible 2026–35 agenda, and H-1B regime shifts (100k fee, weighted lottery) raise employer leverage over exactly the mobile developer workforce.
2. **Demand-side pressure cuts against it** — the entry-level collapse (J3) and elevated comp mean the people most likely to organize (juniors) are the people least present in big tech, while senior developers (high pay, low unemployment risk) have the least material motive; stagnation at ~1–2% developer coverage is the modal path.
3. **The upside tail is genuine and discontinuous** — layoff/AI precarity plus ~70% union approval among young workers could yield one or two large wins (a single 20–30k-developer unit at a top-10 firm, or public-sector developer units organizing) that clear 3% alone; union-coverage statistics also jump on definitional changes (e.g. counting worker associations like AWU), so a "statistical" resolution is nearly as plausible as an organizing one.

**Crowd forecast found:** none matching (searched Metaculus/Manifold for developer-unionization questions). Metaculus Q10877 "What percentage of American workers will be represented by a labor union in 2030?" is adjacent (all workers, not developers); its page returned HTTP 403 to automated fetch, so I did not use the number visible in search results.

**What would change my mind:** Up — a signed CBA at any top-10 tech employer covering >10k engineers (P2030 to ~50%); BLS publishing a developer-specific "represented" rate. Down — a failed high-profile drive (e.g. at a major AI-lab or game company) plus continued NLRB erosion → P2035 to ~15%.

**This number is wrong if:** the scorer adopts the CPS occupation-level definition (then the answer is "already true" and 20%/30% is far too low), or if one large contract lands 2027–2029 (then 20% is too low), or if tech-union drives keep failing one by one and coverage drifts to <1% (then 30% for 2035 is too high).

---

## Summary

| Req | Outside view | P by 2030 | P by 2035 | Anchor |
|---|---|---|---|---|
| J1 postings ≥100 | ~45% (+5), ~60% (+10) — post-bust cyclical recovery base rates | **35%** | **45%** | no matching crowd question; Metaculus Q42613 (dev employment −6.6%/−11%) as adjustment |
| J2 ≥90% SO AI adoption | ~50% (+5), ~65% (+10) — saturation-metric base rates | **55%** | **65%** | no matching crowd question; SO 2026 survey itself (plateau ~83%) |
| J3 ≥10% new-grad share | direct anchor: LEAP/FRI experts 7.0% (2030), 7.8% (2040) | **20%** | **30%** | https://leap.forecastingresearch.org/forecasts/entry-level-tech-hiring (read 2026-10-17) |
| J4 ≥3% devs covered | ~15–25% (+5) — white-collar organizing base rate; occupation-level CPS already 4.4% | **20%** | **30%** | no matching crowd question; BLS CPS Union Members 2025, Table 3 |

Grades: J3 Low-Medium (sourced expert panel, near-exact metric match); J1, J2 Low (IDEA-agents, no external forecast found — J2 additionally carries metric-continuity risk); J4 Low (definitional sensitivity dominates).
