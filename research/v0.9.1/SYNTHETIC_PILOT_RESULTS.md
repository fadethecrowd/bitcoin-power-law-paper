# Synthetic sequential-detection pilot — 2026-11-21

**NOT a confirmatory Bitcoin result.** All numbers arise from simulated AR(1) residuals about an oracle-known frozen Power Law trend; no historical Bitcoin price dataset was used. The screened 12-model family and predictive P10 backtest remain to be executed.

Source: `research/v0.9.1/sequential_pilot.py`; `python -m unittest test_sequential_pilot.py` passed 7/7 locally. NumPy 2.3.5. Reproduction: `python sequential_pilot.py --paths 2000 --rho 0.997` (also rho 0.995 and 0.999).

## Design
- Monitoring starts on 2026-08-14 (age 6432 days after genesis) and covers ten years.
- Null forecast residual: Gaussian AR(1), stationary scale 0.30 log units, rho 0.995, 0.997 or 0.999, initialized at zero (conditioning on exact trend at onset).
- Alternative: continuous break in forward local slope of D=0.5,1,3: log-price deviation at +t days is `-D log((6432+t)/6432)`.
- EWMA of log deviation with 180-day half-life. One alarm when EWMA drops below a *whole ten-year path* cutoff.
- Null threshold calibrated from 2,000 separate null paths at a nominal whole-path alpha 0.05, then tested on independent seeds and paths. Each D has 2,000 evaluation paths.
- Fixed seed 20261121. Estimates are noisy at low probabilities: binomial MC SE ~0.005 near 5%, ~0.011 near 50%.

## Pilot detection probability (percent)
| rho | D | within 2y | within 5y | within 10y |
|---|---:|---:|---:|---:|
|0.995|0|0.30|2.00|4.25|
|0.995|0.5|0.85|5.55|23.10|
|0.995|1|0.85|11.30|62.20|
|0.995|3|5.20|81.75|100.00|
|0.997|0|0.05|1.65|3.75|
|0.997|0.5|0.80|5.00|19.30|
|0.997|1|0.50|9.15|50.05|
|0.997|3|3.95|68.40|100.00|
|0.999|0|0.00|1.50|4.55|
|0.999|0.5|0.20|3.60|15.70|
|0.999|1|0.15|6.85|36.55|
|0.999|3|1.70|54.10|99.80|

**Important:** independent Monte Carlo randomness means estimates need not increase monotonically with D in finite runs. Zeroing the initial residual, assuming a known trend, preselecting EWMA 180 days, using no stochastic cycle, and setting future volatility to a fixed 0.30 all make this a deliberately simplified demonstration; none establishes a best-case upper bound for all detectors. In fact a more effective detector could have substantially different power.

## Interpretation
For this specific detector, 2-year detection is poor even for large local-slope breaks. The ten-year false-alarm budget makes the threshold severe. This supports testing the *design tradeoff* rather than adopting a calendar-duration alarm, but proves nothing universal about Bitcoin or other detectors.

## Next
1. Freeze full screened-family forward forecasting, parameter uncertainty, P10 vintage design and volatility forecasting rules.
2. Extend to screened models including cycles and nonstationarity; calibrate false alarms for each and the worst-case family.
3. Evaluate multiple predeclared detectors and P10 separately; only then assess claims of statistical power.
