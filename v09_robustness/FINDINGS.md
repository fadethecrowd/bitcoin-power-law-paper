# Findings by status

Each finding is classified by what the v0.9 testing supports. Section references are to `REPORT.md`.

- **Confirmed:** holds under every plausible null model and in reproduction. Each item is tagged **[empirical]** (computed directly from the frozen series), **[analytic]** (follows mathematically from stated assumptions) or **[simulation]** (holds under the declared residual-model family only).
- **Suggestive:** consistent direction, but significant only under some models or some versions of the test.
- **Unsupported:** the evidence offered for it does not survive calibration.
- **Unresolved:** the data, or the material available here, cannot decide it.

## Confirmed

1. **v0.8's point estimates reproduce exactly.** [empirical] This covers:
   - B = 5.650938 and the Newey–West SE of 0.189;
   - post-2017 B = 4.8645;
   - the rolling, expanding and start-date estimates;
   - the 2025 decomposition and the break-detector output.

   Two exceptions: the block-bootstrap SD reproduces only approximately (0.249 against 0.240), and the PP statistic does not reproduce (see Unsupported). §1
2. **Within the declared family, only models with the imposed four-year stochastic cycle pass the screen** [simulation, conditional]. None of the 16 models without the cycle passes. This is not independent evidence of a four-year cycle: the period was fixed in advance, and two screening features target multi-year periodicity. Independent cycle validation is outside this package. §2.2
3. **Rolling, expanding and start-date exponent paths are consistent with a constant B.** [simulation] Every rolling path, at every window length, stays inside its constant-B band, which is the envelope of the 12 plausible models' pointwise 95% ranges. So does the start-date curve. Inside the envelope is weaker than inside every model's range. The expanding estimates leave their bands only in the first months after the 2011 and 2017 peaks, and only upward. Figures 1–3
4. **The selection-aware minimum of the rolling 5-year path is unremarkable** [simulation] (p = 0.38–0.81). A low rolling estimate somewhere in 16 years is expected under a constant exponent. §3.2
5. **v0.8's break detector carries no information about B.** [simulation] v0.8 already reported this under its AR(1) null; under every screened model here it selects four breaks in 100% of constant-B histories, and its power against a declining exponent is flat at the false-positive rate. §3.2, §4.3
6. **Rolling-window statistics have negligible power to detect a change in B.** [simulation] The 5-year rolling estimate at the cutoff reaches 0.15 at D = 3 even if the true residual model is known. §4.3
7. **v0.8's intervals for B are too narrow under most plausible models.** [simulation] Newey–West coverage is 0.29–0.85 in 10 of 12 models. Under the best-fitting models the sampling SD of B̂ is 0.32–0.43, against v0.8's SE of 0.19, and 1.5–1.9 times the Newey–West SE computed on the same simulated histories. §5.1
8. **Residual unit-root tests over-reject at Dickey–Fuller critical values, and declining volatility makes this worse.** [simulation] False rejection of a random walk with Bitcoin's volatility profile is 0.40 at the DF value and 0.19–0.22 at the residual-based value. This agrees with Baquero & Menezes. §5.2
9. **Volatility-scale invariance holds as a property of the stationary AR(1) model.** [analytic] The standardized-gap closing times reproduce: 390, 394 and 405 days, against v0.8's 398, 393 and 392. §5.3
10. **Descriptively, cycle highs have fallen relative to the trend in every epoch while lows have not.** [empirical] Epoch maxima were 2.76, 2.50, 1.86, 1.27 and then 0.30 in the incomplete epoch. Minima were −1.58, −0.97, −0.83, −0.82 and −0.82. §6.1
11. **The 2025 fall in the rolling 5-year exponent came from observations leaving the window.** [empirical] The departing contribution was −2.03 and the arriving 2025 prices +1.09. This is descriptive and is not calibrated against the null. §1
12. **The simulator reproduces Baquero & Menezes' published benchmarks** [simulation] for the drift + random-walk fit, ADF rejection and Newey–West coverage. §2.3

## Suggestive

1. **Top-only compression of residual extremes.** Quantile asymmetry gives p = 0.015–0.135 against symmetric shrinking nulls and 0.033–0.18 against skewed ones. The epoch test on complete epochs gives p = 0.04–0.28. Significance is decisive only when the incomplete current epoch is included (p < 0.01), and that epoch's maximum is still a lower bound. The pattern was reported earlier by others, credited in §6. §6.2
2. **Shrinking volatility fits better than constant volatility.** The five best-fitting models all have λ = 1, but the λ = 0 versions also pass the screen. §2.2
3. **The null family may slightly overstate low-frequency variability.** Observed rolling and expanding exponent paths are calmer than in most simulated histories: p = 0.56–0.99 for the rolling SD and 0.89–0.99 for the expanding range. If so, the p-values for a decline are somewhat conservative. §3.2
4. **The point estimates point toward a lower recent exponent.** The post-2017 estimate is 0.79 below the full-sample B, and the curvature implies a 1.76-unit decline. The direction is consistent across estimators; the size is not distinguishable from zero (see Unresolved 1).

## Unsupported

1. **A statistically significant decline in B.** After multiplicity adjustment, 1 of 12 plausible models gives p < 0.05, or 3 of 38 including sensitivity variants. All of them are the least-persistent, cycle-dominated model with shrinking volatility, which fits no better than the others. Skewed-null calibration does not change this. §3.2–3.4
2. *(Withdrawn from this list.* An earlier draft listed "v0.8's detected breaks as evidence of regime change" here. v0.8 made no such claim: it already reported the detector as uninformative under its AR(1) null.)
3. **The v0.8 Newey–West interval (±0.37) as a 95% interval for B.** See Confirmed 7. §5.1
4. **Residual stationarity or mean reversion established by ADF/PP.** The tests reject a plausible random walk 10–20% of the time at the correct 5% value, and plausible stationary models only 2–54% of the time. They cannot discriminate between the models. §5.2
5. **v0.8's Phillips–Perron statistic of −2.380.** `arch` 8.0.0 gives −3.04 at lag 11 and −3.31 with automatic lag selection; no specification on a broad grid reproduces −2.380. Neither replacement rejects at simulated or residual-based 5% critical values. §1, §5.2
6. **The end-2025 rolling 5-year value (3.26) as an anomaly.** It is the path minimum, and the selection-aware test gives p = 0.38–0.81. §3.2
7. **The October 25 review's power range (about 0.12–0.49) and p-value range (< 0.001 to 0.39).** Both are superseded. Power is ≤ 0.18 at D = 3 with critical values valid across the plausible family. The p-value range over plausible models is 0.011–0.56. §7

## Unresolved

1. **Whether the local exponent is constant or declining.** The 95% interval for the total decline in the local exponent over 2010–2026, D, is about −2.5 to +5.9 under the best-fitting model, and −1.0 to +4.5 up to −4.2 to +7.8 across plausible models (a negative decline would be a rise). It includes zero and includes large declines. §4.3
2. **How persistent the deviations are.** Daily AR(1) persistence from 0.990 (half-life 69 days) to a unit root all fit. Mean reversion, and any reversion time, is therefore not identified. §2.2, §5.3
3. **Whether top-only compression is significant on complete data.** This can be settled only when the current epoch ends, around 2028, by re-running step 6 with E4 complete. §6.2
4. **Results of Baquero & Menezes' S1 low-frequency test under a screened family.** Their replication package could not be retrieved, so S1 was not re-implemented. §2.3
5. **Whether cycle peaks are tied to halvings.** The null deliberately does not assume this, which probably makes the epoch tests conservative by an unknown amount. §6.2
6. **Effects of heavy tails and within-year volatility clustering.** Innovations are Gaussian. Right skew was checked separately and does not change the conclusions; other departures from Gaussianity were not tested. §8
