# IDEA structured judgment — Estimator A1

ORIGIN = 2025. Horizons: **+5 = calendar-year-end 2030**, **+10 = calendar-year-end 2035**.
Estimate produced 2026-10-17. I did not see estimator B's numbers and did not look for them.

| ID | Requirement | Outside view | P(by 2030) | P(by 2035) |
|----|-------------|--------------|-----------:|-----------:|
| J1 | Indeed US software-dev postings index ≥ 100 at year-end | ~40% (5 yr) / ~65% (10 yr) | **55%** | **70%** |
| J2 | ≥ 90% of professional devs "using or planning to use" AI tools (Stack Overflow) | ~50% | **45%** | **55%** |
| J3 | ≥ 10% new-grad share of big-tech hires (SignalFire metric) | ~20% | **30%** | **40%** |
| J4 | ≥ 3% of US software developers covered by a union/CBA | ~50% (threshold sits at today's level) | **55%** | **65%** |

---

## J1 — Postings recovery: index ≥ 100 at year-end

**Outside view (~40% by 2030, ~65% by 2035).** Base rate for "a sector demand index that has fallen more than 30% below its pre-shock baseline returns to that baseline within ~5 years of its trough" is well under even: the dot-com bust took roughly 6–7 years for tech demand/employment to regain its 2000 peak, and the GFC took ~6 years for US job openings to regain theirs. Over a 10-year window the base rate rises to roughly two-thirds. Indeed's own total-US index is the closest direct analogue: below 100 from April 2020 until 2022.

**Adjusted: P(2030) = 55%, P(2035) = 70%.** I move *up* from the outside view because the recovery is already well advanced and the remaining gap is small.

**Three main reasons**
1. **The series has already turned and is climbing fast.** The index troughed at 61.1 (May 2025) and read 76.62 on 2026-09-11 on FRED (https://fred.stlouisfed.org/series/IHLIDXUSTPSOFTDEVE, page last updated Sep 15 2026), ~78 in early Oct 2026 per a secondary compilation of the same FRED series (https://copilotinterview.com/blog/tech-hiring-statistics-2026, read 2026-10-17). That is ~+21% year-over-year and roughly 44% of the 61→100 gap already closed in 17 months. Getting to 100 by Dec 2030 now needs only ~6%/yr compounded — less than a third of the recent pace.
2. **Indeed Hiring Lab itself attributes the rebound to agentic AI, the same force that caused the decline** — "US software development job postings have grown by almost 15% since the launch of Claude Code in late February 2025, while overall job postings fell by 7%" (https://www.hiringlab.org/2026/07/08/ai-and-job-postings-from-destruction-to-creation, 2026-07-08). Under that read, AI widens the scope of software work in the near term, which is a demand *tailwind*, not a headwind.
3. **But the composition argues against a clean V-shaped return to 100:** 71% of the May-2025→May-2026 increase came from senior roles and 37% from AI-titled jobs; entry-level postings were only 4.5% of software postings in Q1 2026 (both Hiring Lab, same URL and the Q1-2026 hiring-trends release cited above). A permanent loss of the junior/graduate tier caps how far the aggregate index can climb, and the Metaculus Labor Hub crowd expects software-developer *employment* of −5.3% by 2030 and −9.5% by 2035 versus 2025.

**What would change my mind.** Down: two consecutive quarters of flat/declining postings after Q4 2026; a senior-only recovery that plateaus the index at 80–90; a US recession in 2027–28. Up: the index printing ≥ 90 at any year-end before 2029 (at which point I'd move P(2030) to ~80%). Also note a measurement hazard: this is an Indeed-platform index, and a material change in Indeed's employer mix or in Indeed's seasonal-adjustment method would resolve the question on a series that is not economically stable.

**Crowd forecast.** No crowd market resolves on the Indeed postings index. Closest anchors (all read 2026-10-17): Metaculus Labor Hub software-developer employment route (−5.3% by 2030, −9.5% by 2035; the hub's comparison table on the same page shows −8.6%/−14.3%, so the two renderings disagree and I treat both as "modest decline"): https://www.metaculus.com/labor-hub/jobs/software-developers and https://www.metaculus.com/questions/42613/us-software-developer-change-vs-2025/ (page text obtained via search-engine rendering; a direct fetch returned HTTP 403 on 2026-10-17). Manifold, "Will software engineers' inflation-adjusted salaries reach their 2021 levels by 2030?" — 68% via the Manifold API, ~59% in a cached search snippet: https://manifold.markets/MilfordHammerschmidt/will-software-engineers-inflationad

---

## J2 — AI adoption saturation: ≥ 90% "using or planning to use AI tools"

**Outside view (~50%).** For professional software tools, the base rate of reaching ≥90% of a professional population within ~5 years of hitting 70% is roughly even: email, PCs, version control and cloud all got past 90%, but typically over 7–10 years, and some (pair programming, TDD, on-prem→cloud migrations) stalled in the 70–85% band permanently.

**Adjusted: P(2030) = 45%, P(2035) = 55%** — i.e. slightly *below* the outside view, because the resistant share looks sticky rather than shrinking.

**Three main reasons**
1. **The level is already close but the residual is flat, not closing.** Our own series (using-or-planning) is 70% (2023) → 76% (2024) → 84% (2025). The 2026 Stack Overflow survey (published 2026-10-06) reports **83% currently use at least one AI tool and 17.2% say "I don't use AI tools"** (https://survey.stackoverflow.co/2026/ai/data, opened 2026-10-17). The 2025 survey's "don't plan to use" share was 16.2% (https://stackoverflow.blog/2026/09/30/getting-ready-for-2026-results-a-look-back-on-developer-survey-findings/). So the never-user share has been ~16–17% for two years — crossing 90% requires that share to fall by more than a third, and it has not moved.
2. **The stated reasons for avoidance are durable, and sentiment is cooling.** In the 2026 survey, 59% try to avoid AI for at least one reason — fear of losing skills (17%), ethics (15%), privacy/security (13%), environment (8%) — and favourable sentiment among respondents learning to code fell from 72.1% (2024) to 52.8% (2025), per the Stack Overflow retrospective above. Only 7% trust AI output for important decisions (https://survey.stackoverflow.co/2026/ai/data). Adoption driven by employer mandate ("my organization required it" was the reason for 10.6% of tool switches) can also reverse.
3. **Definitional risk is unusually high here.** The 2026 question is "Do you currently use AI tools or AI agents in your role at work?" with **no "plan to use" option** — the metric as worded in the requirement may no longer exist by 2030, and Stack Overflow's respondent base and question wording drift year to year. A rise in "using" (44%→62%→79% on Stack Overflow's own retrospective cut) can coexist with a flat "using or planning" total.

**What would change my mind.** Up: any 2027–2028 Stack Overflow wave with non-users below 12%, or enterprise data showing >90% of engineers using assistants under mandate. Down: non-users rising above 20%, or Stack Overflow discontinuing/rewording the AI-adoption item so the question becomes unresolvable (in which case I would want the requirement redefined before scoring).

**Crowd forecast.** **No forecast exists** matching this threshold on Metaculus, Manifold, GJO or published surveys (searched 2026-10-17 on Metaculus, Manifold API search, and web). Using my own estimate.

---

## J3 — Entry-level hiring recovery: ≥ 10% new-grad share of big-tech hires

**Outside view (~20%).** For an occupational entry-level share that has halved, the base rate of returning above its pre-shock level within 5 years is low — in most white-collar professions (journalism, finance, law, accounting) the entry-level tier never regained its pre-crisis share. The strongest positive analogue is the dot-com bust, where campus/intern pipelines rebounded within ~3–4 years, but that recovery involved no structural automation of junior tasks.

**Adjusted: P(2030) = 30%, P(2035) = 40%.**

**Three main reasons**
1. **This time the entry-level tier is falling even while overall hiring recovers** — the historically unusual part. Live Data Technologies (30–80 large US tech companies) found intern intake kept falling as SWE recruitment came back: "Historically, intern programmes have tended to bounce back pretty quickly once companies start hiring again. That hasn't happened this time" (https://newsletter.pragmaticengineer.com/p/the-job-market-in-2026-part-2, 2026-06-09, opened 2026-10-17). The same source: at 28 large US tech companies, **in 2025 just one in ten engineering hires was a recent grad, down from nearly three in ten in 2023**.
2. **The level is below the threshold and the underlying force is still active.** SignalFire: new-grad share ~15% (2019) → 7% (2025); entry-level hiring down ~65% at majors and ~76% at early-stage startups vs 2019 (our verified file). Stanford "Canaries in the Coal Mine": employment of 22–25-year-olds in the most AI-exposed occupations ~19% below counterfactual as of Aug 2026, adjusting through hiring rather than pay. Indeed: entry-level postings were 4.5% of software-development postings in Q1 2026 versus 69.3% senior (Hiring Lab Q1 2026 release cited above).
3. **Offsets that keep this far above zero:** the 10% threshold is only ~3 percentage points above current readings and these estimates are noisy and vendor-specific (SignalFire 7% vs Live Data ~10% on different samples); big-tech campus pipelines are cheap relative to senior comp and serve recruiting-brand, alumni-network and lobbying functions; and the +3-year rise in the average age of technical hires creates a senior-supply squeeze that can force firms to rebuild a junior tier by 2032–2035.

**What would change my mind.** Up: a SignalFire/Live Data report showing new-grad share ≥9% and rising for two consecutive years; a public return-to-campus program at two of Meta/Google/Amazon/Microsoft. Down: further decline in intern intake in the 2027–2028 reports, or evidence that AI agents absorb the tasks new grads were hired for.

**Crowd forecast.** **No forecast exists** matching this metric (searched 2026-10-17). Closest proxies, both about employment levels rather than hiring mix: Manifold "Will there be more software engineers in five years than there are today?" ~41% (https://manifold.markets/SanghyeonSeo/will-there-be-more-software-engineers-in, snippet read 2026-10-17); Manifold (Zvi Mowshowitz) "Will the BLS show growth in software engineer employment through 2029?" 36–38% (https://manifold.markets/ZviMowshowitz/will-the-bls-show-growth-in-softwar, read 2026-10-17). Using my own estimate.

---

## J4 — Collective bargaining: ≥ 3% of US software developers covered by a union or CBA

**Outside view (~50%, and mostly a measurement question).** US occupational unionization rates are famously sticky: the private-sector rate is 5.9% and at a post-war low (BLS Union Members 2025, below). The outside-view base rate for a low-density white-collar occupation *doubling or tripling* its density in 5 years is ~5–10%. But that is not this question: the threshold here sits essentially **at** the current level of the parent occupation group, so the base rate for "≥3% in a given year" is close to a coin flip on definitional grounds alone.

**Adjusted: P(2030) = 55%, P(2035) = 65%.**

**Three main reasons**
1. **The threshold is already borderline-satisfied by the best available proxy.** BLS CPS (release 2026-02-18, https://www.bls.gov/news.release/union2.nr0.htm and table at https://www.bls.gov/news.release/union2.t03.htm, opened 2026-10-17): *computer and mathematical occupations* had a union **membership** rate of 3.7% and were **represented by unions** (i.e. covered by a CBA) at **4.4%** in 2025 (4.7% in 2024 and 2023). On the "covered" wording in the requirement, the parent group is already above 3%. BLS does not publish a separate line for software developers (SOC 15-1252).
2. **Software developers specifically are probably *below* the group average,** which is what keeps me near 50–55% rather than 75%. Coverage in that group is carried by public-sector IT (universities, government), telecom/hardware support roles and a few organised shops; big-tech SWE remains barely organised — the Manifold market "US Software Engineer Union at Meta, Microsoft, Alphabet, Amazon, or Apple by end of 2026?" trades at **14%** (Manifold API, https://manifold.markets/Anthem/us-software-engineer-union-at-meta, read 2026-10-17). A developer-only point estimate would plausibly land in the 2.5–3.5% band, i.e. straddling the threshold, and the CPS sampling error on this group is on the order of ±0.5pp.
3. **Direction of travel is up, and AI is the stated driver.** 68% of Americans approved of unions in 2025 (Gallup, cited in https://www.computerworld.com/article/4191760/brewing-battle-more-tech-workers-want-unions-but-the-industry-doesnt.html, 2026-07-01, opened 2026-10-17); 67% of 1,900 tech professionals surveyed on Blind said they would join a union if offered one; 2,100 UC tech workers voted 96% in favour in May 2026; CWA organised ~400 digital-media companies 2022–24; and The Guardian reports AI-driven precarity pushing tech workers to the bargaining table (https://www.theguardian.com/technology/2026/jul/21/ai-tech-workers-unionize, 2026-07-21). Countervailing: intense employer resistance and a hostile federal backdrop (private-sector density at record lows).

**What would change my mind.** Up: any BLS release showing computer-and-math *represented* ≥ 5% with developers named; a first contract at a large software firm. Down: a developer-specific CPS/unionstats.com estimate below 2%, or successful employer campaigns (the Computerworld piece documents VC-threat and firing tactics) that stall the 2026 organising wave. If the scoring body reads "software developers" narrowly as SOC 15-1252 and "covered" as *membership* only, I would cut this to roughly 40% (2030) / 50% (2035).

**Crowd forecast.** No crowd forecast matches the ≥3%-coverage threshold. Closest: the 14% Manifold big-tech-SWE-union market above (read 2026-10-17). Using my own estimate.

---

## Sources opened for this note (2026-10-17)

- https://fred.stlouisfed.org/series/IHLIDXUSTPSOFTDEVE (Indeed US software-development postings index; 76.62 on 2026-09-11)
- https://www.hiringlab.org/2026/07/08/ai-and-job-postings-from-destruction-to-creation (Indeed Hiring Lab, 2026-07-08)
- https://survey.stackoverflow.co/2026/ai/data (Stack Overflow Developer Survey 2026, AI chapter)
- https://stackoverflow.blog/2026/09/30/getting-ready-for-2026-results-a-look-back-on-developer-survey-findings/
- https://stackoverflow.co/company/press/archive/stack-overflow-annual-developer-survey-ai-trust-conditional (2026-10-06 press release)
- https://newsletter.pragmaticengineer.com/p/the-job-market-in-2026-part-2 (2026-06-09; Live Data Technologies new-grad and intern data)
- https://www.bls.gov/news.release/union2.nr0.htm and https://www.bls.gov/news.release/union2.t03.htm (BLS Union Members — 2025, released 2026-02-18)
- https://www.computerworld.com/article/4191760/brewing-battle-more-tech-workers-want-unions-but-the-industry-doesnt.html (2026-07-01)
- https://www.theguardian.com/technology/2026/jul/21/ai-tech-workers-unionize (2026-07-21)
- https://www.metaculus.com/labor-hub/jobs/software-developers and https://www.metaculus.com/questions/42613/us-software-developer-change-vs-2025/ (crowd numbers taken from search-engine-rendered page text; direct fetch returned 403)
- Manifold API + market pages: https://manifold.markets/MilfordHammerschmidt/will-software-engineers-inflationad (68%), https://manifold.markets/ZviMowshowitz/will-the-bls-show-growth-in-softwar (36–38%), https://manifold.markets/MatthewBarnett/will-the-number-of-people-employed (21%), https://manifold.markets/Anthem/us-software-engineer-union-at-meta (14%)
- https://copilotinterview.com/blog/tech-hiring-statistics-2026 (secondary compilation of the FRED series; used only for the Oct 2026 reading and the 61.1 May-2025 trough)
