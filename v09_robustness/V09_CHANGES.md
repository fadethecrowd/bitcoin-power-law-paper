# Recommended changes for v0.9

The changes are grouped by topic, because the v0.9 section numbering is the manuscript lead's to set. Each item says what to change and why, with a reference to `REPORT.md`. Items marked **[required]** correct a number or a claim that does not survive testing. The rest improve the paper but do not change its conclusions.

## Abstract and headline claims

1. **[required]** No claim that the exponent is stable, or that it is declining, should be stated as a test result. Suggested wording: *"Rolling, post-2017 and curvature estimates of the exponent are all compatible with a constant B under candidate residual models that pass a screen on Bitcoin's residual features (all of which include an imposed four-year stochastic cycle). The tests available have little power, so a moderate decline cannot be excluded either."* §3.4, §4.3
2. **[required]** Report B with model-indexed uncertainty instead of ±0.37:

   > B = 5.65. The 95% sampling half-width is 0.36 under the least persistent plausible residual model, 0.63–0.85 under the best-fitting models, and up to 2.4 if deviations follow a random walk with a cycle.

   §5.1

## Methods: inference

3. **Declare the null family in the paper.** Include:
   - a table of the components: persistence, cycle share, volatility shape, and rescaling to the observed residual SD;
   - the screening rule;
   - the 12 plausible models and the 36 sensitivity extremes, reported separately.

   This is what makes "significant" well defined when residuals are this persistent. §2
4. **Name one principal reported test for a change in the exponent, and say it was chosen after the data were seen.** It is not preregistered. Report its family-wide p-value and its range of model-specific p-values. Suggested principal reported test: the curvature statistic. It estimates the total change in the local exponent without bias under a smooth decline, so it inverts directly to a confidence interval for D (point estimate 1.76; 95% interval −2.5 to +5.9 under the best-fitting model). It also has the highest family-wide power against a decline spread across the whole sample. Report the multiplicity-adjusted battery as secondary. §3.1, §4.3
5. **Say where the one rejection comes from.** Adjusted p < 0.05 occurs only under AR(0.990) with a dominant cycle and shrinking volatility: 1 of 12 plausible models, or 3 of 38 with variants. That model fits Bitcoin's residuals no better than ar0.995–0.997 with cycle share 0.4, where adjusted p = 0.15–0.27. §3.2–3.3
6. **Report power.** A short table or Figure 5 is enough. With critical values valid across the plausible family, no test exceeds 0.18 power even for a 3-unit decline. Without that, a reader will read non-rejection as evidence of constancy. §4.3

## Rolling, expanding and start-date analysis

7. **[required]** Present rolling, expanding and start-date estimates **with their constant-B null bands** (Figures 1–3), not against the full-sample B alone.
8. **[required]** Stop using rolling-window statistics as tests of a change in B. Their power is negligible: the rolling 5-year estimate at the cutoff reaches 0.15 at D = 3 even if the true model is known. Keep them as descriptive. §4.3
9. Treat the end-2025 rolling 5-year value of 3.26 as the minimum of a path, and report its selection-aware p-value (0.38–0.81) rather than a fixed-date comparison. §3.2
10. Keep the 2025 departing-versus-arriving decomposition as a description of *why* the window moved. The fall came from 2020 data leaving the window; 2025 prices pushed the estimate up. Do not present it as evidence for or against a change in B. §1

## Structural breaks

11. Keep v0.8's break-detector conclusion, which was already cautious (uninformative under its AR(1) null: 99.7% of null runs select four breaks; observed largest change at the 54.7th percentile). Extend it: under the 12 screened models the detector selects four breaks in 100% of constant-B histories, the observed largest change sits at the 38th–60th percentile, and its power is flat at the false-positive rate. State that both results are conditional on the detector and the simulated residual processes. *(Corrected: an earlier draft of this item implied v0.8 had treated the breaks as evidence of regime change. It had not.)* §3.2, §4.3

## Stationarity and unit roots

12. **[required]** Replace the Phillips–Perron value −2.380 with the reproducible values, verified with `arch` 8.0.0, `PhillipsPerron(trend="c")`, Bartlett kernel: −3.04 at 11 lags (−3.0416) and −3.31 at the automatic lag of 34 (−3.3072). Say that the v0.8 value remains unreconciled: no specification tried reproduces it (daily data, three trend specifications, lags between 1 and 365: −2.98 to −3.61; weekly and month-end samples: −2.80 to −3.43). §1
13. **[required]** State which critical values are used. Simulated 5% critical values for this exact design are −3.32 to −3.38 under a constant-volatility random walk, matching the Phillips–Ouliaris (−3.37) and MacKinnon (−3.34) residual-based values; the Dickey–Fuller constant-only value (−2.86) over-rejects about fourfold. Under a random walk with Bitcoin's declining volatility the 5% values are −4.1 to −4.3. Report the fixed-lag ADF statistics (−2.94 to −3.61): against the constant-volatility values only the 21- and 33-lag versions reject; against the declining-volatility values none does. §5.2
14. **[required]** Reword the stationarity conclusion. Suggested: *"Unit-root tests on the residuals cannot distinguish stationary from unit-root deviations here. With Bitcoin's declining volatility, they reject a true random walk 10–20% of the time at the 5% level, and they reject several plausible stationary models less often than that."* §5.2
15. Keep the volatility-scale invariance result, framed as **conditional**: *"If deviations follow a stationary AR(1), the time to close a gap of fixed size in standard-deviation units does not depend on the volatility level."* Update the illustration to the reproduced values (390, 394 and 405 days) or note that it agrees with v0.8 within Monte Carlo error. Add one sentence saying that persistence is not identified from the data, so the result is not evidence of mean reversion. §5.3

## Maturation and compression of highs and lows

16. Present top-only compression as a **descriptive** finding: epoch maxima fell in every epoch while minima held. Pair it with a calibrated test against shrinking nulls. Quantile asymmetry gives p = 0.015–0.18 and complete epochs give p = 0.04–0.28. §6
17. **[required]** Say explicitly that the strongest version (p < 0.01) includes the incomplete current epoch, whose maximum is a lower bound. Commit to re-running the test when the epoch closes. §6.2
18. **[required]** Credit prior observations of the pattern: wineLightning (Test 7), Banks, Perrenod (5 June 2026) and Crosby. Present v0.9's contribution as the calibrated test. Confirm the exact references. §6.2

## Figures

19. Suggested replacements and additions, all from `figures/` (300-dpi PNG; real-series paths drawn at month-end resolution only):
    - **Fig. 1:** rolling 5-year, expanding and post-2017 expanding B, each against its constant-B null band.
    - **Fig. 2:** rolling B for 4-, 5-, 6-, 8- and 10-year windows against their bands.
    - **Fig. 3:** B by regression start year against its band.
    - **Fig. 4:** one-sided and multiplicity-adjusted p-values by null model. It shows directly that the conclusion depends on the residual model.
    - **Fig. 5:** power curves for both critical-value types and both decline shapes.
    - **Fig. 6:** coverage of v0.8's intervals by model.
    - **Fig. 7:** epoch extremes and asymmetry p-values.

    The figure titles in the PNGs state the finding. Captions should add the model set and the number of simulations (see REPORT §9).

## Data and reproducibility

20. Ship this package, or its scripts, with v0.9. The package needs the licensed CSV to run and contains no price observations. Two exceptions should be checked against the licence: the ten halving-epoch residual extremes and the exponents at a handful of named dates (README, "Data policy").
21. Document exactly how v0.8's block bootstrap was run. The reconstruction with the repository seed gives an SD of 0.249 against the reported 0.240.
22. State the fixed genesis origin (2009-01-03) and the exact sample (5,873 daily observations, 2010-07-17 to 2026-08-14) next to every estimate.

## Limitations section (add)

23. Persistence of the deviations is not identified. Within the declared family only models with the imposed four-year cycle pass the screen; this is conditional on the family and screen and is not independent evidence of a cycle. Innovations are Gaussian, with right skew checked separately. The null cycle is not locked to halvings. The screen and the tests use the same history, so a slow trend change and persistent deviations cannot be fully separated. Baquero & Menezes' S1 test was not re-implemented because their replication package was unavailable. §8
