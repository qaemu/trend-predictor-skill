# Dense-history supplement (points_dense.csv) — US SWE salaries & workplace conditions
Additive rows only: no row here duplicates anything already in points.csv / points_recent.csv. History ends 2025 (ORIGIN = last full year); built 2026-10-17.

## 1. postings_index / indeed_hiringlab — 71 rows, monthly 2020-02 … 2025-12
- Source file: https://raw.githubusercontent.com/hiring-lab/job_postings_tracker/master/US/job_postings_by_sector_US.csv (sector file; repo README confirms: seasonally adjusted daily series, 7-day trailing average, Feb 1 2020 = 100, each sector SA separately, history revised with the Nov 2024 Bundesbank-method change).
- Value = the exact published daily index for the LAST calendar day of the month (not a monthly mean), matching the existing annual rows' year-end convention; 2025-12-31 = 67.29 reproduces the existing 2025 annual value.
- Gaps: none inside 2020-02…2025-12 (every month has 25–31 daily observations). Pre-2020 months do not exist — the index is anchored at 2020-02-01.

## 2. unemp_rate_comp / bls_cps — 191 rows, monthly 2010-01 … 2025-12
- Source: BLS Public Data API v2, GET https://api.bls.gov/publicAPI/v2/timeseries/data/LNU04034021?startyear=2010&endyear=2019 and the same with startyear=2020&endyear=2025.
- Title verified against https://download.bls.gov/pub/time.series/ln/ln.series: "(Unadj) Unemployment Rate - Computer and Mathematical Occupations", monthly, not seasonally adjusted, coverage 2000 M01+ → no title mismatch, series is exactly computer/math occupations.
- Caveats: values are NOT seasonally adjusted (strong Jan/Jul seasonal swings); annual means of these months reproduce the existing annual rows within rounding (e.g. 2016 = 2.53 → 2.5).
- Gap: 2025-10 missing — the API returns value '-' (October 2025 CPS household survey was not collected during the federal shutdown). 2000-01…2009-12 also exist upstream but were left out to match the requested 2010–2025 span.

## 3. grad_start_salary / nace_bachelors — 5 rows, class years 2016–2020
- Same tier basis as the existing 2021–2025 rows: NACE Salary Survey, SUMMER edition executive summary, bachelor's, broad category computer and information sciences, average (not median), base salary only, final actuals for the class year. All five retrieved as PDFs via Wayback (exact URLs in the CSV):
  - Class of 2016 $71,916 and Class of 2017 $72,677 → 2018-nace-salary-survey-summer-executive-summary.pdf (snap 20240204071017); the 2016 figure is a prior-year comparison line inside that report, and the report calls the group "various computer science fields".
  - Class of 2018 $71,411 → 2019-nace-salary-survey-summer-executive-summary.pdf (snap 20200805120829), stated in the exec-summary text.
  - Class of 2019 $76,986 → 2020-nace-salary-survey-summer-executive-summary.pdf (snap 20211027063419), stated in the exec-summary text.
  - Class of 2020 $80,477 → nace-2022-summer-salary-survey-executive-summary.pdf (snap 20230804220038), Figure 1 prior-year column (the Summer 2021 report never states the group average, only the individual major).
- Gaps: none of 2016–2020. Category wording drifts ("computer science fields" → "computer and information sciences") but the CIP broad group is the same.

## 4. ai_tool_adoption_planned / ai_tool_adoption_prof — 0 rows added: DENSER HISTORY IMPOSSIBLE
- Verified the full official results pages survey.stackoverflow.co/2019, /2020, /2021 and /2022 (each page complete, ends with </html>): none of the four surveys contains any AI question — zero occurrences of "AI"/"artificial intelligence"/"Copilot" in the 2019 page, and the 2020/2021/2022 section inventories (60/56/78 sections) contain no AI section.
- Cross-checked against the Wayback snapshot of the page as originally published (https://web.archive.org/web/20190409133448/https://insights.stackoverflow.com/survey/2019, April 2019, 1 MB): also zero AI mentions, so this is not a re-render artefact. (The official microdata zips on the Wayback Machine downloaded only truncated/corrupted, so the published results pages are the evidence used.)
- Consequence: the AI questions begin in 2023 ("using or planning to use AI tools"); 2019–2022 is a permanent definitional gap, not a missing download. The series start cannot be moved earlier without changing the metric.

## 5. swe_entry_bigtech_us / bigtech-junior — 7 rows added, series now spans 2019–2025 for both firms
- Added: Meta E3 for 2020 ($179k), 2021 ($181k), 2023 ($185k) from Wayback snapshots of the levels.fyi Facebook software-engineer page (2020-11-30, 2021-12-08, 2023-12-09), and Google L3 + Meta E3 for 2024 ($196,851 / $184k) and 2025 ($184,537 / $191k) from snapshots 2024-11-30, 2025-11-15 (Google level pages) and 2024-12-21, 2025-12-06 (Facebook company tables). Exact URLs in the CSV.
- Caveat: levels.fyi labels these figures the "median total compensation package" for the level; the pre-existing 2019–2023 rows quote the same statistic but call it an "average" — same number, wrong word. Google level pages give exact dollars + base/stock/bonus; the Facebook company tables are rounded to $1k.
- Gaps: 2018 and earlier are unreachable — levels.fyi L3/E3 pages are not archived before mid-2020, and CNBC only covers 2019.
