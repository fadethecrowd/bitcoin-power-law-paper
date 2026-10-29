# Change log: v0.8 → v0.9

*Bitcoin's Price Power Law: Stability, Maturation, and a Live Test of the Scaling Hypothesis.* Technical draft v0.9, October 2026.

## Unchanged

The following are carried over from v0.8 without change:

- the frozen sample: 5,873 completed UTC daily closes, 2010-07-17 to 2026-08-14, SHA-256 `ada93367…886f`;
- the genesis time origin (2009-01-03) and the model specification (unweighted daily OLS of ln P on ln t with a free intercept);
- all baseline estimates;
- the episode definition, rankings and refit decomposition;
- the volatility, persistence and recovery analysis;
- the keeping-pace versus catching-up analysis;
- the realized-growth open question;
- all five forward-monitoring markers, reproduced word for word in §11.6.

No price data after 2026-08-14 enters any result.

## Corrections

| Item | v0.8 | v0.9 | Where |
| --- | --- | --- | --- |
| Phillips–Perron Z_t | −2.380, presented as an audited value | Withdrawn. Replaced by −3.04 (11 lags) and −3.31 (automatic lag, 34) from `arch` 8.0.0, `PhillipsPerron(trend="c")`. The v0.8 value is stated as unreconciled. | §5.3, §6.3, Table 5 |
| Unit-root critical values | ADF rejection described against ordinary Dickey–Fuller values | Residual-based values (Phillips–Ouliaris, MacKinnon) reported alongside critical values simulated for the exact design, with constant and with declining volatility. The DF constant-only value is identified as over-rejecting about fourfold. | §5.3, §6.3, Table 5 |
| Stationarity conclusion | "mixed and lag-dependent" | Kept, with additions: no statistic rejects against a unit root with Bitcoin's declining volatility, and the tests cannot discriminate stationary from unit-root residuals. | §6.3, §12.3 |
| Data availability | Frozen dataset "will be released" with the final version | Withdrawn. The licensed series is not redistributed; the repository policy, schema and file hash are cited instead. | Data and code availability |
| Bootstrap reproduction | Audited SD 0.2401 | Value kept. A footnote reports that the publication-seed rerun gives 0.249, because the original seed was not preserved. | §6.2 |

## New material

- **§7 Exponent stability revisited (new section).** This section covers:
  - the rolling-window (4–10 year), post-2017 and start-date estimates, all deterministic;
  - why short windows swing: the narrow span of ln t, plus persistent residuals;
  - the 2025 departing-versus-arriving decomposition of the five-year decline;
  - a declared, screened family of 48 residual models;
  - calibrated one-sided p-values for six statistics, with Westfall–Young multiplicity adjustment;
  - sensitivity variants and a skewed-null check;
  - power against two shapes of exponent decline, with family-wide and oracle critical values;
  - a confidence interval for the decline, obtained by inverting the curvature statistic.
- **Principal reported statistic.** The curvature statistic is designated the principal reported statistic and is stated to have been chosen after the data were examined, not preregistered. The multiplicity-adjusted battery is reported as secondary.
- **`mean5` definition.** `mean5` is defined as the mean of the rolling five-year estimate at five checkpoints: 2022-12-31, 2023-12-31, 2024-12-31, 2025-12-31 and 2026-08-14.
- **The four-year cycle.** The cycle is described as imposed in the candidate family. That screened models contain it is conditional on the family and the screen, not an independent finding (§7.4, §12.8, Appendix B).
- **Coverage of intervals for B (§6.2, Table 4, Figure 3).** By simulation, the 365-day Newey–West interval under-covers in 10 of 12 screened models. Model-indexed half-widths are reported as sensitivity bounds, not as a replacement confidence interval.
- **Break detector under the broader family (§6.4).** v0.8's conclusion that the detector is uninformative already stood under its AR(1) null. v0.9 extends the same check across the twelve screened models and states that the result is conditional on the detector and the null.
- **§8 Asymmetric compression of cycle extremes (new section).** Epoch extremes and quantile slopes are reported. They are tested against symmetric and skewed shrinking nulls, and the dependence on the incomplete current epoch is stated.
- **Evidence-status table (Table 17, §11.3).** Each principal claim is labelled deterministic, analytic or simulation.
- **Appendices.** Appendix C covers family settings and seeds. Appendix D checks the simulator against Baquero & Menezes. Appendix E maps each result to its script.
- **New references.** Baquero & Menezes (Oct 2026), the deceleration working paper; Santostasi & Perrenod (Oct 2026), the Clauset-in-spirit test; Durlauf & Phillips (1988); Phillips (2007); Nelson & Kang (1981); Newey & West (1987); Künsch (1989); Dickey & Fuller (1979); Phillips & Perron (1988); Engle & Granger (1987); Phillips & Ouliaris (1990); MacKinnon (2010); Schwarz (1978); Harvey (1989); Westfall & Young (1993); Koenker & Bassett (1978); statsmodels; arch.

## Revised text

- **Abstract.** Adds the exponent-stability results with power, the conditional cycle language, the coverage finding, the PP correction and the compression result. The sentences on the episode and on keeping pace are unchanged.
- **Introduction.** Adds two contributions and a "What changed in version 0.9" paragraph.
- **Related work.** Adds the Baquero & Menezes deceleration paper as the template for the declared family, the Santostasi & Perrenod goodness-of-fit test (not applied here), and the classical results on regression on persistent series and slowly varying regressors.
- **Discussion.** "What does not survive" now covers both readings of the rolling estimates (structural decline, and constancy inferred from non-rejection). The evidence-status table is added.
- **Limitations.** New subsections cover the declared family and the cycle, post-hoc selection and multiplicity, data provenance and reproducibility scope, and material not re-examined.
- **Conclusion.** Adds the exponent-stability and power result. The final quoted conclusion now says the tests "do not establish … a constant exponent".
- **Figures.**
  - The v0.8 Figures 1–7 and A1 are retained with their original content and renumbered: v0.8 Figures 1–2 are now 1–2, v0.8 Figure 3 is now 4, v0.8 Figures 4–7 are now 5, 6, 7 and 14, and A1 is now 15.
  - The seven robustness figures are added as Figures 3 and 8–13.
  - Captions now say when a result is a simulation and that real-series paths are drawn at month-end resolution.

## Deliberately not changed

- The v0.8 wording "maximum raw log residual" for the episode's deepest point is kept.
- The sections on episode severity, refitting, volatility and recovery, and keeping pace, apart from cross-references.
- The forward-monitoring markers.
- The wineLightning "Test 74" uncertainty comparison.

## Release-preparation pass (25 October 2026, evening)

These changes respond to the independent publication review. No statistical result, qualification, sample boundary or forward-monitoring threshold changed.

- **Data redistribution (review gate B).** The public `v09_robustness/outputs/reproduction.json` previously gave the ten halving-epoch residual extremes to three decimals, with dates. Combined with the published A and B, each could approximate one day's licensed close.
  - These values are now rounded to two decimals, as printed in Table 13, and carry no dates.
  - Step 01 of the package was changed accordingly, and a test now enforces the format.
  - The output manifest, `REPORT.md`, the package README and `docs/DATA_AVAILABILITY.md` were updated to match.
  - One sentence was added to the paper's Data and code availability statement.
  - Figure 13 was redrawn from the rounded values; the change is not visible at print size.
- **Verification instructions (gate D).** `verify_manuscript.py` previously defaulted to paths in the author's working environment, and the README omitted the CSV argument. It now takes three required arguments (package, repository, frozen CSV). It stops with a clear message if a path is wrong or the CSV is not the frozen file, and contains no environment-specific paths. `README_BUILD.md` gives the exact command for the released ZIP layout.
- **Figure reproducibility.** A rerun in a fresh environment showed that the figure script used whatever font the local matplotlib configuration specified. The original environment's configuration supplied Inter; a fresh install falls back to DejaVu Sans. As a result, figure sizes and pixels differed between environments, although every number was identical.
  - `07_figures.py` now resets matplotlib to its built-in defaults and pins DejaVu Sans (bundled with matplotlib) and default text hinting.
  - The seven robustness figures (Figures 3 and 8–13) were redrawn and are now byte-identical across environments.
  - Two labels were shortened to fit the wider font (the power-curve x-axis and the battery legend entry), and the compression figure was widened slightly.
  - Content, data and titles are otherwise unchanged.
- **Authorship and AI disclosure (gate C).** Left unchanged, pending the author's decision. Draft options are in `RELEASE_CHECKLIST_v0.9.md`.

## Attribution update (25 October 2026)

- Added Maxwell Koenig as the sole human author on the PDF title page and in metadata, consistent with the v0.8 Zenodo author/creator arrangement.
- Acknowledged ChatGPT (OpenAI) and Claude (Anthropic) as AI research and analytical assistants on the title page and in the dedicated disclosure, not as additional human authors.
- No statistical methods, frozen data, model assumptions or monitoring thresholds changed.

## Editorial edits (October 2026, author-approved)

- §6.2: the closing sentences of the Santostasi–Perrenod comparison now explain that the regression weights each day equally, that successive days are not independent evidence about B, and that allowing for this serial dependence widens the uncertainty without changing the fitted exponent.
- §13: the 36.6% keep-pace figure and the 199%, 100.5% and 74.6% catch-up figures are restated as model-implied required price-growth rates (CAGR) at the 14 August 2026 cutoff, with their horizons, and are labelled as not forecasts. The numbers are unchanged.
- No statistical method, result, frozen input, figure or monitoring threshold changed.

## Final adversarial review corrections (28 October 2026)

- Corrected the abstract to identify the interval [−2.5, +5.9] as the interval for a **decline**, D, not for the signed change in B. The interval and all numerical estimates are unchanged.
- Clarified that Figures 8–10 use the envelope of pointwise 95% bands across screened models, rather than the band of any single model; the graphics and simulated outputs are unchanged.
- Corrected Baquero–Menezes benchmark descriptions in Appendix D and script/output paths in Appendix E.
- Added the verified working-paper DOI for Baquero–Menezes ahead of the software-package DOI in reference [10].
- Updated repository data-availability documentation to accurately describe two previously published single-day verification targets; no new provider data are included.
- Clarified reproducibility wording, method-specific uncertainty, figure-name crosswalk, and streamlined repeated editorial language.
- The 12.8 speculative direction-of-bias proposal was intentionally not adopted because no sensitivity run establishes its direction or magnitude.
- Frozen data, numerical results, figures, simulations, and all forward monitoring markers are unchanged.

## Source attribution and data-availability clarification (29 October 2026)

- Added linked, clearly labelled inferred price-source credits for CryptoCompare/CoinDesk Data and CoinGecko in §3, the Figure 1 caption and the numerical snapshot table. Attribution does not assert row-by-row provenance.
- Added visible, linked source credits in repository README, provenance and data-availability documentation.
- Retained the two single-day verification values at their previously published precision, as already disclosed by the README and data-availability policy. No new daily provider data are introduced.
- No statistical values, private sample, figures, model assumptions or monitoring thresholds changed.
