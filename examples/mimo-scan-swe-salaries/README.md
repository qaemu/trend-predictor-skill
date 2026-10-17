# Real run: scan of US software-engineering pay, on a free flash model

> A full TREND-PREDICTOR run made by **MiMo V2.6 Flash (free, in OpenCode)** on 2026-10-17, in **scan mode** on "US software engineering salaries and workplaces". It reused the sourced data of a PARADIGMA run made the day before. Kept here as a test case: what a cheap model got right, what it got wrong, and what the engine now enforces because of it. Reproduce the re-scoring with `python3 tests/test_real_run.py`.

## Folders

- [`original_run/`](original_run): the run's own outputs, unchanged: [`report.md`](original_run/report.md), verification, series fits, project scores, the agents' judgment estimates (`idea_*.md`), signposts, predictions log and charts.
- [`data/`](data): the inputs needed to re-score it (points, constraints, CPI, events, scenarios, calibration, and the requirement files of the field scan and the 3 candidate projects).
- [`rescored/`](rescored): the same inputs scored by the current engine. [`comparison.csv`](rescored/comparison.csv) puts the run's verdicts next to the engine's.

## Review

**What held up**
- The data work. It reused the PARADIGMA data and sent a research pass for denser history (monthly Indeed postings, monthly BLS unemployment, NACE start salaries 2016–2020), all from primary sources, and said where denser history does not exist (Stack Overflow asked no AI questions before 2023).
- The independent check: 84 items, 92% match. All 40 grade-B data points matched BLS to the cent. One fatal error caught and fixed (an H-1B rule recorded as "proposed" that has been law since February 2026).
- Uninformative curves (job postings, unemployment) were kept out of the headline and turned into judgments, as the skill says.
- Its one external anchor is real: the LEAP expert panel on new-grad share of big-tech hiring (7% in 2030, vs 15% in 2019).

**What went wrong**

| Problem | Effect | Fixed by |
|---|---|---|
| Two project verdicts rested on weak evidence: P1's weakest link was a probability made up by the run's own estimators (Low grade); P3's was a grade-C curve at +5 and a Low judgment at +10 | P1 reported as PLAUSIBLE / PLAUSIBLE, P3 as LONG SHOT / PLAUSIBLE: more confident than the evidence allows | **Engine**: every requirement now carries an `evidence_grade`; when the weakest link is C, D or Low, the verdict is `UNCERTAIN (driven by <req>)` and the score moves to `verdict_if_inputs_hold` |
| The report quoted calibration as 88% / 96% coverage and bias ≈ 0.02; the engine's own `calibration.csv` says 77% / 95% and 0.157 | Better-looking numbers than the run's own data | **Instructions**: calibration figures must be copied verbatim from `calibration.csv` |
| It scored "the whole field" by multiplying four unrelated conditions into one number (6% by 2030) | A number that describes no project anyone could build | **Instructions**: in scan mode only candidate projects get a joint probability and a verdict |
| "AI agents become a drop-in junior engineer" was entered as a technology-readiness step, so the software TRL prior made it ~99% by 2030 | Looks far more solid than it is | **Instructions**: capability and adoption claims are judgments, not readiness |

**Re-scored by the current engine** (same inputs, same probabilities, new rule):

| Project | Run's verdict (+5 / +10) | Engine now | Weakest link |
|---|---|---|---|
| P1 entry pay-band benchmarking | PLAUSIBLE / PLAUSIBLE | **UNCERTAIN / UNCERTAIN** | jud01: postings recovery, estimated by the run's own agents (Low) |
| P2 non-profit apprenticeship pipeline | LONG SHOT / LONG SHOT | LONG SHOT / LONG SHOT (unchanged) | jud03: anchored on the LEAP expert panel (Medium) |
| P3 junior-plus-AI staffing | LONG SHOT / PLAUSIBLE | **UNCERTAIN / UNCERTAIN** | req02: Payscale curve (C); jud02 at +10 (Low) |

The joint probabilities are reproduced exactly; only the labels change, and only where the evidence is weak. P2's verdict stands because its weakest link cites an outside panel.

**Bottom line.** For a free model the data collection and verification are good, and the wage forecasts can be used. The project verdicts could not, until the engine stopped letting a weak input carry them. P1 also sits in a market PARADIGMA marked crowded (Pave, Carta); feasibility scoring doesn't look at competition, so read it next to the PARADIGMA run.
