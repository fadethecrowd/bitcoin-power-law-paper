# Bitcoin Power Law v0.9: robustness of the exponent, interval and compression results

Methodology and results report for the v0.9 statistical work package. Prepared on 25 October 2026 for the manuscript lead. All numbers come from the scripts in this package run on the frozen v0.8 file (SHA-256 `ada93367…886f`, 5,873 daily observations, 2010-07-17 to 2026-08-14). The genesis origin is fixed at 2009-01-03 throughout.

## Corrections made on 25 October 2026 (after the independent audit)

- `mean5` is the mean of the rolling 5-year B at **five checkpoints** (2022-12-31, 2023-12-31, 2024-12-31, 2025-12-31, 2026-08-14), not an average over every month of 2022–2026. §3.1 corrected; the figure labels now say so. The numbers were always computed this way.
- The four-year cycle is part of the simulation design. That only cycle models pass the screen is conditional on the family and the screen (two of six screening features target multi-year periodicity), not independent evidence of a cycle. §2.2 reworded.
- v0.8 did not claim that its detected breaks proved regime change; it already called the detector uninformative. FINDINGS and V09_CHANGES corrected.
- The curvature statistic was chosen after the data were examined. It is the *principal reported test*, not a preregistered primary test. V09_CHANGES corrected.
- The curvature statistic now leads the bottom line as the principal reported statistic; the multiplicity-adjusted battery is secondary. Model-indexed interval half-widths (§5.1) are sensitivity bounds conditional on the family and the data-dependent screen, not a replacement 95% confidence interval.
- Phillips–Perron replacement values verified with `arch` 8.0.0 (§1), and residual-based critical values simulated for the exact design (§5.2, new step 11).

## Bottom line

1. **No declining exponent is established, and none is excluded.** The recent rolling, post-2017 and curvature estimates fall inside what a constant exponent produces under the residual models that pass the screen. The principal reported statistic (curvature; chosen after the data were examined, not preregistered) gives p = 0.14–0.35 across the 12 screened models and rejects under none. As a secondary check, the six-statistic battery adjusted for multiple tests gives p < 0.05 under 1 of the 12; across them the adjusted p ranges from 0.011 to 0.56. Every model with adjusted p < 0.05 is from one corner of the family: the least persistent component (AR 0.990) with a dominant 4-year cycle and shrinking volatility.
2. **The tests have little power.** A test must hold its 5% size across every plausible model, because the data cannot say which model is true. Under that requirement, no statistic rejects more than about 18% of the time, even when the local exponent falls by 3 units over the sample. Even with the true model known, the best power at D = 3 is 0.45–0.60. Inverting the curvature test gives a 95% interval for the total decline in the local exponent, D, of roughly −2.5 to +5.9 under the best-fitting model (a negative decline would be a rise). The interval includes zero and includes large declines.
3. **v0.8's intervals for B are too narrow under most plausible models.** In 10 of 12 plausible models, the Newey–West (365-day) interval contains the true B in only 29–85% of simulated histories, not 95%. Under the best-fitting models the sampling SD of B is 0.32–0.43, against v0.8's 0.19.
4. **The unit-root evidence cannot decide between the models.** The ADF and PP statistics on the residuals reject a unit root at the Dickey–Fuller 5% value. Under shrinking volatility, though, that value rejects a true random walk 38–40% of the time. At the residual-based 5% value, only the ADF tests with 21 and 33 lags reject. v0.8's Phillips–Perron value of −2.380 could not be reproduced. A standard implementation gives −3.04 (lag 11) or −3.31 (automatic lag).
5. **Top-only compression is real in the data but only borderline as a test.** Cycle highs have fallen relative to the trend in every epoch while lows have held. The quantile-based asymmetry test gives p = 0.015–0.18. The epoch-extremes test is significant only when the incomplete current epoch is included, and that epoch's high could still rise.
6. **The October 25 review mostly holds up, with three revisions.** Its p-value range is replaced by one taken from a screened family. Its power figures were optimistic. Its asymmetry result needs the incomplete-epoch caveat. Section 7 has the full list.

## 1 Reproduction

`scripts/01_reproduce.py` recomputes every v0.8 number used below. It also checks the vectorized estimators against the v0.8 repository code (commit `95b6a2a`).

| Quantity | v0.8 / Oct 25 | This package | Status |
| --- | --- | --- | --- |
| Full-sample B (OLS, ln P on ln t) | 5.650938 | 5.650938 | exact |
| Newey–West SE, 365-day lag | 0.18916 | 0.18916 (matches statsmodels) | exact |
| Post-2017 B | 4.8645 | 4.8645 | exact |
| Rolling 5-year B at year-ends 2021–2025, 2026-08-14 | 6.30, 4.92, 4.78, 4.20, 3.26, 4.12 | identical to 4 d.p. | exact |
| Rolling 5-year daily minimum / maximum | 3.255 (2025-12-18) / 7.588 (2020-01-12) | same | exact |
| 2025 change in rolling 5-year B, Shapley split | departing −2.030, arriving +1.094 | same | exact |
| Break detector: K, max adjacent change, slope range | 4, 13.93, 16.58 | same; fast code = reference | exact |
| 365-day block bootstrap SD of B | 0.2401 | 0.249 (repository seed 20261001) | close; not bit-identical |
| ADF on residuals, fixed lags 1/5/10/21/33 | — | −2.94, −3.17, −3.04, −3.43, −3.61 | reported |
| Phillips–Perron | **−2.380** | **−3.0416** (lag 11), −3.3072 (automatic, 34 lags); `arch` 8.0.0, `PhillipsPerron(trend="c")`. Daily data with no constant, a constant or a constant and trend, at lags between 1 and 365 and the automatic lag: −2.98 to −3.61; weekly and month-end samples with a constant: −2.80 to −3.43 | **not reproduced; unreconciled** |
| Quantile slopes τ = 0.05 / 0.50 / 0.95 | — | 5.885 / 5.847 / 4.925 | reported |

Expanding-window B (from 2010) at year-ends 2016–2025 and 2026-08-14 was 5.61, 5.87, 5.74, 5.89, 5.82, 5.71, 5.70, 5.70 and 5.65. Since 2017 the month-end range is 0.34. The fall from the 2022 peak (5.90) is 0.25.

B from 1 January of each year to 2026-08-14: 5.51 (2011), 5.58, 5.25, 5.36, 5.91, 5.59, 4.86 (2017), 4.59, 4.98, 4.43, 3.00 (2021) and 5.45 (2022).

## 2 The declared null family

### 2.1 Model

Under the null, ln P_t = A + B ln t + u_t with B constant. The deviation u_t is drawn from

```
u_t = k · [ sqrt(1−w) · p_t / sd(p) + sqrt(w) · c_t / sd(c) ],     shocks scaled by σ_t = h(year_t)^λ
```

- **p_t** is the persistent component. It starts at zero at genesis. The cases are AR(1) with daily ρ ∈ {0.990, 0.995, 0.997, 0.998, 0.999}, a random walk, and fractional integration with d ∈ {0.6, 0.9}. The AR(1) half-lives are 69, 138, 231, 346 and 693 days.
- **c_t** is a Harvey stochastic cycle: z_t = ρ_c e^{iω} z_{t−1} + η_t, c_t = Re z_t. The period is 4 years (ω = 2π/1461). ρ_c is set so the cycle's correlation halves after three periods. c_t starts from its stationary distribution. Because the cycle is stochastic, its peaks are **not** locked to halving dates.
- **w ∈ {0, 0.4, 0.8}** is the cycle's share of the deviation variance.
- **h(year)** is the observed annual SD of daily log returns, raised to **λ ∈ {0, 1}**. λ = 0 gives constant volatility. λ = 1 gives the shrinking volatility observed in Bitcoin.
- **k** rescales every path so that its residual SD from a constant-B OLS fit equals the observed value, 0.697.
- Innovations are Gaussian. Simulations run on the daily calendar from genesis and are sampled on the observed days.

That gives 8 persistence settings × 3 cycle shares × 2 volatility shapes = **48 models**, with 1,000 histories each.

### 2.2 Which models reproduce Bitcoin's residuals

Each model is screened on six features of the constant-B residuals:

- lag-1, lag-365 and lag-1461 autocorrelation;
- zero crossings;
- the amplitude ratio, last five years over first five;
- the share of variance at 3–5-year periods.

A model is *plausible* if the Mahalanobis p-value on all six features together is ≥ 0.05 **and** no single feature has p < 0.01. Two further features are reported but not screened on, because no Gaussian model can match them:

- the decline in daily volatility: observed 0.278, simulated about 0.31 in every λ = 1 model;
- residual skewness: observed +0.86, simulated about 0.

**12 of the 48 models pass** (`outputs/screening.csv`):

| Model | Mahalanobis p | Weakest feature (p) |
| --- | --- | --- |
| ar0.995 · cycle 0.4 · λ1 | 0.30 | acf365 (0.10) |
| ar0.997 · cycle 0.4 · λ1 | 0.29 | acf365 (0.06) |
| ar0.998 · cycle 0.4 · λ1 | 0.22 | acf365 (0.02) |
| ar0.999 · cycle 0.4 · λ1 | 0.12 | acf365 (0.01) |
| random walk · cycle 0.4 · λ1 | 0.10 | acf365 (0.01) |
| ar0.997 · cycle 0.4 · λ0 | 0.09 | acf365 (0.05) |
| ar0.995 · cycle 0.4 · λ0 | 0.09 | zero crossings (0.03) |
| ar0.990 · cycle 0.8 · λ0 | 0.07 | acf365 (0.05) |
| ar0.990 · cycle 0.8 · λ1 | 0.07 | acf365 (0.03) |
| ar0.998 · cycle 0.4 · λ0 | 0.06 | acf365 (0.02) |
| frac 0.9 · cycle 0.8 · λ1 | 0.06 | acf365 (0.02) |
| ar0.999 · cycle 0.4 · λ0 | 0.05 | acf365 (0.01) |

The screen supports three conclusions:

- **Within this family, only models with the imposed cycle pass.** No model without the 4-year cycle passes, at any persistence or volatility setting. This is conditional, not independent evidence of a four-year cycle: the cycle's period was fixed in advance (following Baquero & Menezes' family), two of the six screening features (lag-1461 autocorrelation and the 3–5-year spectral share) target multi-year periodicity, and no other cyclical or long-memory structures outside the grid were tried.
- **Persistence is not identified.** Daily ρ from 0.990 to a unit root all pass. A 16-year history cannot separate a half-life of 2 months from no mean reversion at all, once a cycle carries most of the visible oscillation.
- **Shrinking volatility fits better.** The best fits have λ = 1, but λ = 0 versions of the same models also pass.

The 36 models that fail are kept as **sensitivity extremes**. Results are reported for them separately and never mixed into the plausible ranges.

### 2.3 Relationship to Baquero & Menezes (October 2026)

The design adapts Baquero & Menezes' declared-family approach: random-walk-type deviations, the observed volatility profile and a cycle. Their replication package (Zenodo 23218897) could not be retrieved from this environment. Their low-frequency test S1 is therefore **not** re-implemented. The simulator is instead checked against the figures they publish:

| Check | Baquero & Menezes | This package |
| --- | --- | --- |
| Constant drift + random walk: median fitted B (90% range) | 6.1 (3.4–9.2) | 6.35 (3.09–9.62) |
| Same: median R² / share above Bitcoin's R² | 0.897 / 0.14 | 0.888 / 0.106 |
| ADF rejection, random walk + volatility profile | 0.44 | 0.40 |
| ADF rejection, random walk, constant volatility | 0.18 | 0.20 |
| ADF rejection, random walk + cycle | 0.20 | 0.21 |
| Newey–West (four-year lag) coverage, random walk | 0.33–0.36 | 0.31–0.32 |

Their sample is weekly data from 2011 and ours is daily data from 2010, so close but not identical numbers are expected. Agreement at this level means the two simulators implement the same models.

The main difference is the screen. Baquero & Menezes report results across their declared family. Here, models that cannot reproduce Bitcoin's residual autocorrelation and spectrum are set aside as extremes before inference.

## 3 Exponent tests calibrated against the family

### 3.1 Statistics

Each statistic is computed identically on the real series and on every simulated history (`lib/stats.py`).

| Code | Statistic | Observed | Direction tested |
| --- | --- | --- | --- |
| d17 | post-2017 B minus full-sample B | −0.786 | low |
| curv | implied change in local exponent over the sample, 2c·(x_last − x_first), where c is the ln-t² coefficient | −1.758 | low |
| mean5 | mean of the rolling 5-year B at five checkpoints: 2022-12-31, 2023-12-31, 2024-12-31, 2025-12-31 and 2026-08-14 | 4.256 | low |
| r5_2025 | rolling 5-year B at 2025-12-31 | 3.265 | low |
| rmin5 | minimum of the whole rolling 5-year path (selection-aware: the minimum is taken in every simulated path too) | 3.265 | low |
| exp_drop | fall of expanding B from its post-2017 peak | 0.249 | high |
| rend L, rmin L, rsd L | rolling L-year B at the last date, its minimum and its SD, L = 4, 5, 6, 8, 10 | see `calibration.csv` | low / low / high |
| exp_range | range of expanding B since 2017 | 0.344 | high |
| brk | v0.8 BIC break detector: selected K, largest adjacent slope change, slope range | 4, 13.93, 16.58 | high |

### 3.2 Results

One-sided p-values across the 12 plausible models (`outputs/calibration_summary.csv`). Monte Carlo SE is ≤ 0.016 per p-value (1,000 histories).

| Statistic | p, min–median–max | 5% critical value valid for every plausible model | Observed |
| --- | --- | --- | --- |
| d17 | 0.039 – 0.20 – 0.32 | −2.07 | −0.79 |
| curv | 0.137 – 0.25 – 0.35 | −5.37 | −1.76 |
| mean5 | 0.002 – 0.13 – 0.28 | 2.49 | 4.26 |
| r5_2025 | 0.066 – 0.14 – 0.26 | 0.27 | 3.26 |
| rmin5 | 0.38 – 0.72 – 0.81 | −1.03 | 3.26 |
| rend10 | 0.11 – 0.32 – 0.42 | 3.13 | 5.21 |
| exp_drop | 0.42 – 0.51 – 0.56 | 1.33 | 0.25 |

**Multiplicity.** The six-statistic battery (d17, curv, mean5, r5_2025, rmin5, exp_drop) is adjusted with the Westfall–Young min-p method within each model (`outputs/maxT.csv`). The adjusted p is:

- 0.011 for ar0.990 · cycle 0.8 · λ1, driven by mean5;
- 0.118 for the same model with λ0;
- 0.15–0.56 for the other ten models.

This adjustment covers the choice among the six statistics. It does **not** cover the choice of the battery itself. The battery mirrors statistics that v0.8 and the October 25 review chose after seeing the data, so even the adjusted values are, if anything, too small.

The **selection-aware minimum** of the rolling 5-year path (rmin5) is unremarkable, with p = 0.38–0.81. A low rolling estimate at some point in 16 years is what a constant exponent produces. The end-2025 value looks unusual only when that one date is singled out in advance.

**Exponent paths are calmer than the null, not wilder.** The observed SD of the rolling 5-year path and the range of expanding B since 2017 are smaller than in most simulated histories, with "high-side" p = 0.56–0.99 and 0.89–0.99. Two readings fit this. Either the family slightly overstates low-frequency variability, which would make every p-value above somewhat conservative. Or the true process sits at the less persistent end of the family, which is where the small p-values come from. The two cannot be separated with one history.

**Break detector.** v0.8's detector selects K = 4 in 100% of constant-B histories under every plausible model. The observed maximum adjacent slope change sits at the 38th–60th percentile of its null distribution. The detected breaks carry no information about a change in B. This confirms the October 25 finding.

### 3.3 Sensitivity

`scripts/09_sensitivity.py` re-simulates every plausible model with λ = 0.5 and 1.25 and with cycle periods of 3.5 and 4.5 years. That gives 38 distinct variants, because the λ variants of a λ0/λ1 pair coincide. 26 of them pass the same screen.

- Across all 38 plausible models (12 base + 26 variants), adjusted p runs from 0.000 to 0.56.
- **3 of 38 are below 0.05.** All three are ar0.990 · cycle 0.8 · λ ≥ 1: the base model 0.011, period 3.5 years 0.000, λ = 1.25 0.005.
- The eight best-fitting of these 38 models (Mahalanobis p 0.28–0.51) give 0.12–0.34.
- A fit-weighted mean, weighting by Mahalanobis p, is 0.27. This weighting is a descriptive summary, not a posterior.

`scripts/10_skew_battery.py` imposes Bitcoin's right-skewed residual distribution on every null path and re-runs the battery. The method is the same rank-mapping as in step 6. Adjusted p moves only slightly: from 0.011–0.56 to 0.006–0.53. One model is still below 0.05. Skewness does not change the conclusion.

### 3.4 Answer to the assignment question

Under the plausible part of the declared family, the post-2017, rolling and curvature statistics are compatible with a constant exponent. The only rejection comes from the least-persistent, cycle-dominated corner of the family. That corner fits Bitcoin's residuals no better than the others, and arguably worse than ar0.995–0.997 with cycle share 0.4. Whether a decline is "significant" therefore depends on a modelling choice the data cannot settle. v0.9 should report it that way.

## 4 Power against a declining local exponent

### 4.1 Alternatives

Under the alternative, ln P_t = A + B ln t + g_D(ln t) + u_t, with u_t drawn from a plausible model. Let x = ln t, with x₀ and x₁ the first and last observed values.

- **Linear decline across the sample.** The local exponent is β(x) = B + D·(½ − (x − x₀)/(x₁ − x₀)). It falls from B + D/2 to B − D/2 and averages B. Then g_D(x) = D·[(x − x₀)/2 − (x − x₀)²/(2(x₁ − x₀))].
- **Decline after 2017.** β(x) = B before x_k = ln t(2017-01-01). After that, β(x) = B − D·(x − x_k)/(x₁ − x_k), so it falls from B to B − D. Then g_D(x) = −D·(x − x_k)²/(2(x₁ − x_k)) for x ≥ x_k.

Other settings:

- D ∈ {0, 0.25, 0.5, 1, 1.5, 2, 3}.
- 1,000 noise paths per model. The same paths are reused for every D (common random numbers), drawn with seeds independent of the calibration draws. The D = 0 row is therefore an out-of-sample false-positive rate.
- Monte Carlo SE ≤ 0.016.

Two kinds of critical value are used:

- **Family-wide.** The least favourable 5% critical value across the 12 plausible models. This is the only kind that controls size when the true model is unknown, which it is.
- **Model-specific (oracle).** The 5% critical value of the model that generated the noise. This is an upper bound on power, attainable only if the residual model were known.

### 4.2 Size and false-positive rates (`outputs/size_table.csv`)

| Critical value | False-positive rate, mean over models | Range across models |
| --- | --- | --- |
| Family-wide | 0.006 – 0.023, by statistic | 0.000 – 0.063 |
| Model-specific | 0.045 – 0.059, by statistic | 0.025 – 0.084 |

Family-wide critical values are conservative for most models. Their maximum slightly exceeds 0.05 because the least-favourable quantile is itself estimated from 1,000 draws. The model-specific values are close to nominal.

### 4.3 Power (`outputs/power_curves.csv`, Figure 5)

Rejection rates are means over the 12 plausible models.

| Test | Linear D = 1 | Linear D = 2 | Linear D = 3 | After-2017 D = 1 | After-2017 D = 2 | After-2017 D = 3 |
| --- | --- | --- | --- | --- | --- | --- |
| **Family-wide critical value** | | | | | | |
| Curvature | 0.04 | 0.09 | **0.18** | 0.04 | 0.08 | 0.14 |
| Post-2017 minus full B | 0.03 | 0.05 | 0.09 | 0.04 | 0.09 | **0.16** |
| Mean rolling-5y B | 0.02 | 0.04 | 0.06 | 0.03 | 0.07 | 0.15 |
| Rolling-5y at cutoff | 0.02 | 0.03 | 0.04 | 0.03 | 0.05 | 0.09 |
| Rolling-8y at cutoff | 0.02 | 0.04 | 0.07 | 0.03 | 0.08 | **0.18** |
| Expanding-B drop | 0.04 | 0.08 | 0.14 | 0.03 | 0.06 | 0.10 |
| Break detector | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02 |
| **Model-specific (oracle) critical value** | | | | | | |
| Curvature | 0.13 | 0.26 | 0.40 | 0.12 | 0.22 | 0.35 |
| Post-2017 minus full B | 0.11 | 0.18 | 0.28 | 0.14 | 0.27 | 0.42 |
| Mean rolling-5y B | 0.10 | 0.19 | 0.30 | 0.16 | 0.35 | 0.53 |
| Rolling-5y at cutoff | 0.08 | 0.11 | 0.15 | 0.11 | 0.19 | 0.30 |
| Rolling-10y at cutoff | 0.13 | 0.26 | 0.41 | 0.18 | 0.41 | **0.60** |
| Battery, multiplicity-adjusted | 0.14 | 0.29 | **0.45** | 0.17 | 0.36 | 0.54 |
| Break detector | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 | 0.06 |

Across models the range is wide. The battery's oracle power at D = 3 runs from 0.32 (ar0.999 · cycle 0.4) to 0.84 (ar0.990 · cycle 0.8) for the linear shape, and from 0.37 to 0.98 for the after-2017 shape.

How to read these results:

- **Rolling-window statistics have almost no power**, even with oracle critical values. The 5-year window at the cutoff reaches 0.15 at D = 3 for a linear decline. Rolling estimates are the least informative way to look for a change in B.
- **The v0.8 break detector has no power at all.** Its rejection rate is flat at about 0.06 at every D.
- **Not rejecting is weak evidence of constancy.** Under the linear alternative the curvature statistic estimates −D without bias, because the alternative is exactly quadratic in ln t. Its null quantiles therefore invert directly to a confidence interval for D. With the observed value of −1.76 (point estimate D = 1.76), the 95% interval is:
  - **−2.5 to +5.9** under the best-fitting model (ar0.995 · cycle 0.4 · λ1);
  - −1.0 to +4.5 under the least persistent plausible model;
  - −4.2 to +7.8 under random walk + cycle.

  A local exponent that stayed constant and one that fell from about 8 to about 3.5 over 2010–2026 are both compatible with the data.

## 5 HAC intervals and unit-root tests

### 5.1 Coverage of v0.8's intervals for B (`outputs/hac_coverage.csv`, Figure 6)

Each entry uses 300 constant-B histories per model. Monte Carlo SE is ≤ 0.029.

| Model | True SD of B̂ | Mean NW-365 SE | Coverage NW-365 | Coverage NW-1461 | Coverage 365-day block bootstrap |
| --- | --- | --- | --- | --- | --- |
| ar0.990 · cycle 0.8 · λ0/λ1 | 0.18–0.19 | 0.22 | 0.98–0.99 | 0.86 | 1.00 |
| ar0.995 · cycle 0.4 · λ0/λ1 | 0.27–0.32 | 0.20–0.22 | 0.79–0.85 | 0.67–0.74 | 0.86–0.91 |
| ar0.997 · cycle 0.4 · λ0/λ1 | 0.34–0.43 | 0.21–0.22 | 0.69–0.76 | 0.60–0.68 | 0.81–0.82 |
| ar0.998 · cycle 0.4 · λ0/λ1 | 0.38–0.53 | 0.21–0.23 | 0.62–0.72 | 0.55–0.65 | 0.73–0.77 |
| ar0.999 · cycle 0.4 · λ0/λ1 | 0.49–0.62 | 0.23–0.24 | 0.60–0.64 | 0.55–0.63 | 0.59–0.66 |
| frac 0.9 · cycle 0.8 · λ1 | 0.57 | 0.24 | 0.62 | 0.49 | 0.75 |
| random walk · cycle 0.4 · λ1 | 1.22 | 0.25 | 0.29 | 0.30 | 0.40 |

Newey–West under-covers in 10 of the 12 plausible models. A longer lag (1,461 days) does not help, because the Bartlett kernel also shrinks the estimate. The underlying problem is that, with deviations this persistent, 16 years contain only about four effectively independent cycles.

The defensible statement for v0.9 is a **model-indexed interval**: B = 5.65 ± 1.96 × SD(B̂ | model).

| Model | Half-width of 95% interval |
| --- | --- |
| Least persistent plausible model | ±0.36 |
| Best-fitting models | ±0.63 to ±0.85 |
| ar0.999 | ±1.0 to ±1.2 |
| Random walk + cycle | ±2.4 |

The interval is wide because persistence is unidentified.

### 5.2 ADF and PP under declining volatility (`outputs/unitroot.csv`)

Rejection rates of the residual ADF test (AIC lag) and PP test (lag 11), 300 histories per model:

| Model | Unit root true? | ADF, DF 5% (−2.86) | ADF, residual-based 5% (−3.37) | PP, residual-based 5% |
| --- | --- | --- | --- | --- |
| random walk, constant volatility (screened out) | yes | 0.20 | **0.05** | 0.06 |
| random walk, shrinking volatility (screened out) | yes | **0.40** | **0.19** | 0.22 |
| random walk + cycle, shrinking volatility (plausible) | yes | 0.21 | 0.10 | 0.09 |
| ar0.990 · cycle 0.8 (plausible) | no | 0.31–0.39 | 0.03–0.08 | 0.03–0.09 |
| ar0.995 · cycle 0.4 (plausible) | no | 0.80–0.85 | 0.45–0.54 | 0.45–0.58 |
| ar0.999 · cycle 0.4 (plausible) | no | 0.11–0.22 | 0.02–0.10 | 0.01–0.08 |
| frac 0.9 · cycle 0.8 (plausible) | no | 0.05 | 0.02 | 0.02 |

What this shows:

- **The critical value matters.** The residual is from an estimated regression on a constant and ln t. The Dickey–Fuller constant-only value over-rejects about fourfold even with constant volatility: 0.20 under a homoskedastic random walk. The residual-based value (−3.37) has correct size in that case. v0.9 should use residual-based or simulated critical values.
- **Declining volatility inflates false rejection, as Baquero & Menezes report.** At the residual-based value, a random walk with Bitcoin's volatility profile is rejected 19–22% of the time instead of 5%. Adding the cycle brings this down to about 10%.
- **The tests cannot discriminate between plausible models.** Under plausible stationary models, ADF power at the correct 5% level ranges from 2% to 54%. Several stationary models are rejected *less* often than the plausible random walk + cycle.
- **Simulated critical values for this exact design** (`scripts/11_unitroot_critical_values.py`, 2,000 random walks per null). Under a random walk with constant volatility, the 5% critical values are −3.32 to −3.38 across the eight statistics, close to the Phillips–Ouliaris (−3.37) and MacKinnon (−3.34) residual-based values; only ADF at lags 21 (p = 0.040) and 33 (p = 0.022) reject. Under a random walk with Bitcoin's declining volatility, the 5% critical values are −4.12 to −4.30 and no statistic rejects (p = 0.13–0.38).
- **On the real series**, the fixed-lag ADF statistics are −2.94 to −3.61. All reject at the DF value; at the residual-based value, only lags 21 and 33 reject. PP gives −3.04 (lag 11) and −3.31 (automatic lag); neither rejects at the residual-based value. A rejection, where it occurs, would be expected 10–20% of the time under a unit root with Bitcoin's volatility profile.

### 5.3 Volatility-scale invariance: mathematics versus evidence

v0.8 shows that, in a stationary AR(1), the time needed to close a gap of a given size *in units of the current standard deviation* does not depend on the level of volatility. Re-running v0.8's illustration with ρ = 0.99699 and σ ∈ {0.85, 0.55, 0.31} (4,000 replications, repository seed) gives:

- standardized gap: median 390, 394 and 405 days, against v0.8's reported 398, 393 and 392;
- fixed raw gap: 202, 306 and 487 days.

The result is a correct property of the AR(1) model. It reproduces within Monte Carlo error and is **not** contradicted by anything here.

What is not established is that Bitcoin follows such a process. Section 2.2 shows that daily persistence from 0.990 to a unit root fits equally well. Under a random walk there is no reversion time at all. v0.9 should keep the result as a conditional statement ("if deviations follow a stationary AR(1), then …"). It should not be presented as evidence of mean reversion.

## 6 Asymmetric compression of highs and lows

### 6.1 What is observed

Residual extremes from the full-sample fit by halving epoch (ln units; rounded to two decimals and reported without dates, under the data policy):

| Epoch | Coverage | Maximum | Minimum |
| --- | --- | --- | --- |
| E0 | partial: data start 2010-07-17 | 2.76 | −1.58 |
| E1 | complete | 2.50 | −0.97 |
| E2 | complete | 1.86 | −0.83 |
| E3 | complete | 1.27 | −0.82 |
| E4 | incomplete: from 2024-04-20 | 0.30 | −0.82 |

Quantile slopes give the same picture. The 95th-percentile slope is 0.92 below the median slope, while the 5th-percentile slope is 0.04 above it. The upper envelope has flattened and the lower envelope has not.

### 6.2 Tests

Statistics:

- **Aq** = b₀.₉₅ + b₀.₀₅ − 2b₀.₅₀. This is about 0 under symmetric shrinkage and negative when only the top compresses. Observed −0.885.
- **Aep** = slope of epoch maxima + slope of epoch minima across epochs. Observed:
  - −0.544 over E1–E3, the three complete epochs;
  - −0.268 over E0–E3;
  - −0.447 over E0–E4.

These are tested against two **shrinking** nulls for every plausible model (400 histories each, Monte Carlo SE ≤ 0.025):

- **Symmetric:** the Gaussian paths as simulated. Under λ = 1 they shrink.
- **Skewed:** the same paths rank-mapped onto Bitcoin's standardized residual distribution, which has skewness +0.47. Under this null, highs compress more than lows in absolute terms purely because of skew. It is the harder benchmark.

| Statistic | p, symmetric shrinking null | p, skewed shrinking null |
| --- | --- | --- |
| Aq (quantile asymmetry) | 0.015 – 0.135 | 0.033 – 0.178 |
| Lower-quantile slope alone | 0.09 – 0.62 | 0.11 – 0.58 |
| Aep, E1–E3 (complete epochs only) | 0.040 – 0.24 | 0.08 – 0.28 |
| Aep, E0–E3 | 0.048 – 0.15 | 0.11 – 0.23 |
| Aep, E0–E4 (includes incomplete E4) | < 0.0025 for all models | 0.000 – 0.010 |

What the tests show:

- **The pattern is in the data and its direction is consistent.** All three epoch versions and the quantile version point the same way.
- **Significance depends on the incomplete current epoch.** With complete epochs only, p ranges from 0.04 to 0.28. Adding E4 makes it decisive. But E4's maximum so far (0.30) is a lower bound: a rally later in the epoch could raise it. With three complete epochs, the slope of maxima is estimated from three points.
- **The lows show nothing unusual on their own** (p = 0.09–0.62). The asymmetry comes entirely from the highs.
- **The null may be conservative.** Its cycle is not locked to halvings, so simulated epoch extremes are noisier than they would be if cycle peaks were tied to halving dates. That makes the epoch test conservative to an unknown degree.

**Credit.** Earlier work described the same pattern: cycle highs falling relative to the power-law trend while lows hold. That work includes wineLightning's Test 7, Banks, Perrenod's 5 June 2026 post and Crosby. v0.9 should cite them as prior observations and present its own contribution as the calibrated test against shrinking nulls. The manuscript lead should confirm the exact citations; this package did not re-read those sources.

## 7 What happened to the October 25 findings

| October 25 finding (paraphrased) | Status after this work | Basis |
| --- | --- | --- |
| Rolling-window estimates have little power to detect a change in B | **Survives, strengthened** | §4.3: rolling 5-year power ≤ 0.15 at D = 3 even with oracle critical values |
| v0.8's break detector is uninformative: it finds K = 4 under a constant B | **Survives** | §3.2: K = 4 in 100% of null histories; observed at the 38th–60th percentile |
| v0.8's HAC interval is too narrow | **Survives**, now quantified | §5.1: NW-365 coverage 0.29–0.85 in 10 of 12 plausible models |
| ADF/PP over-reject under declining volatility | **Survives** | §5.2: 19–22% false rejection at the residual-based 5% value |
| The 2025 fall in rolling 5-year B comes from observations leaving the window, not from 2025 prices | **Survives** (reproduced exactly) | departing −2.03, arriving +1.09. This is descriptive and is not calibrated against the null |
| Start-date and window-length sensitivity is a property of the estimator under persistent residuals | **Survives** | Figures 1–3: every path stays inside its constant-B band (the envelope across the 12 plausible models), apart from the first months after the 2011 and 2017 peaks, where the excursions are upward |
| Calibrated p-values for the recent decline span "< 0.001 to 0.39" depending on the null | **Revised** | The upper end reflected unscreened stationary surrogates, now superseded. Replace with: adjusted p 0.011–0.56 over the 12 plausible models (0.000–0.56 with sensitivity variants); 3 of 38 below 0.05, all from one corner of the family |
| Power against a declining exponent of about 0.12–0.49 | **Revised downward** | Those figures implicitly assumed the noise model was known. With critical values valid across the plausible family, power is ≤ 0.18 at D = 3 |
| Top-only compression is borderline significant, p ≈ 0.06–0.14 | **Revised, partly confirmed** | The quantile version reproduces at p = 0.015–0.18. The epoch version is decisive only with the incomplete E4 |
| v0.8's PP statistic of −2.380 | **Not reproduced** | −3.04 (lag 11) / −3.31 (automatic) with a standard implementation |

No October 25 finding is withdrawn outright. The headline p-value range and the power figures should not appear in v0.9 in their October 25 form.

## 8 Limitations

- **Inaccessible material.** Baquero & Menezes' replication package could not be downloaded, so their S1 statistic is not re-implemented. Their published figures were used to check the simulator (§2.3). The sources for the compression pattern credited in §6 were not re-read for this package.
- **Gaussian innovations.** Heavy tails and within-year volatility clustering are not modelled. Right skew is imposed only in steps 6 and 10. The decline in daily volatility is matched in direction but not exactly (0.31 simulated against 0.28 observed).
- **The cycle is not locked to halvings.** This is deliberate, so the null does not assume the halving mechanism, but it probably makes the epoch tests conservative.
- **Screening and testing use the same history.** The family is screened on residuals from the constant-B fit. If B in fact declined, part of the decline would appear in those residuals as low-frequency variation, and models with more of it would be favoured. Persistence and slow curvature in the trend are not separately identified in one 16-year history.
- **The battery was chosen after seeing the data.** The max-T adjustment covers multiplicity within the battery, not the choice of battery.
- **Two v0.8 numbers are reproduced only approximately or not at all.** The block-bootstrap SD reproduces approximately (0.249 against 0.240). The PP statistic does not reproduce.

## 9 Simulation settings

| Stage | Histories per model | Seed |
| --- | --- | --- |
| Screening and calibration (48 models) | 1,000 | SeedSequence([20261025, 2, model]) |
| Power (12 plausible models × 2 shapes × 7 values of D) | 1,000, common random numbers | ([20261025, 3, model]) |
| Interval coverage and unit roots (16 models) | 300 | ([20261025, 4, model]) |
| Asymmetry (12 plausible models × 2 nulls) | 400 | ([20261025, 5, model]) |
| Sensitivity variants (38 distinct, 26 plausible) | 1,000 | ([20261025, 6, variant]) |
| Skewed battery (12 plausible models) | 1,000 | ([20261025, 7, model]) |
| v0.8 bootstrap and AR(1) illustration | as v0.8 | repository seed 20261001 |

All settings are in `lib/config.py`. With the frozen file, every number in this report is reproduced bit for bit by `python run_all.py <csv>` (about 20 minutes on two cores). A clean rerun from empty `outputs/` on 25 October 2026 reproduced every output file with identical values; after a fix to the row order of steps 4–6, files are byte-identical across runs.
