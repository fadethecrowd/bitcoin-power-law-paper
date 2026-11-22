# Diagnostic 09 — 12-family conservative calibration, unknown-onset scan, and volatility stress

**2026-11-22 | Exploratory, unrefereed. Published v0.9 frozen.** The full local reproducibility bundle has the source, SHA-pinned licensed input requirements, simulation-score intermediates, held-out aggregate outputs, and an adversarial Claude review brief; it intentionally does **not** contain licensed BTC close prices or daily fitted histories.

## Main interpretation

Bitcoin's fitted exponent is derived from its observed price history. A change in the fitted value is not independent evidence of a shift in a true local scaling exponent. These 12-family *synthetic* experiments distinguish score discrimination from the much harder problem of jointly limiting false alarms when model identity, change onset and even future noise volatility are uncertain. **They neither prove nor disprove an underlying current Bitcoin structural break.**

## A. Larger 12-family size/power audit

- Frozen historical dataset 2010-07-17–2026-08-14, 5,873 rows, checked SHA256 `ada93367320ad9c45d713650377ee683cf0b58d1ff8fb290fb72cd8b3168886f`. True decline D=1 in hypothetical local log-age exponent after 2026-08-14.
- Each of the twelve originally screened residual processes: 500 synthetic *training*, 2,500 disjoint *calibration*, 2,000 disjoint *evaluation* histories (60,000 histories total). Paired null/alternative share evaluation noise draws. Known change onset. Fixed 1/2/5/10-year alarm inspections. Observable-only historical features.
- Ten-year average AUC across models: posterior-weighted **0.6786**, historically selected **0.6617**, privileged true-family-identity comparator **0.6884**. The identity oracle does not receive the true latent exponent.
- With **model-specific**, roughly 5%-null cutoffs, average D=1 detection **18.38% / 16.82% / 20.96%**. These cutoffs require knowing which stochastic family generated observations and are not operationally available.
- To create a **single** family-agnostic cutoff per adaptive detector, select the maximum of the 12 model-specific order-statistic cutoff bounds calibrated with one-sided Clopper–Pearson and Bonferroni `delta=.05/(12*2)`, alpha=.05. Under correctly specified independent family-null simulations this yields >=95% **simultaneous calibration confidence** that ten-year whole-path size <=5% across the 24 model/method cells. This is not a guarantee for real Bitcoin or misspecified noise.
- Independent 2,000-path/model null holdout: worst-family false alarms **4.05% / 3.60%**, averages **1.54% / 1.84%**. D=1 ten-year detection averages **3.99% / 4.77%**, model ranges **1.55–7.00% / 1.90–9.60%**. The simultaneously adjusted *holdout* upper confidence bound still reaches **5.48%** for the weighted rule; do not claim a separately empirically demonstrated uniform 5% cap.

## B. Unknown-onset yearly-candidate and quarterly-inspection experiment

- Candidate change starts **each year 0–9** following 2026-08-14; past-only OLS refit at each start; prospective alarms at **quarterly** checkpoints, pooled as ten-year whole-path maximum. Not a continuous unknown-onset algorithm.
- Predeclared true D=1 decline can start in year **2** or **5**; 900 independent null calibration and 500 disjoint evaluation paths/model, all 12 models. Each evaluation path is subjected to paired D0, year2, year5 scenarios. Fixed AR(.997)-working *state-corrected* innovation and 180-day EWMA rules; one conservative common threshold for each, using the same simultaneous marginal CP/Bonferroni scheme.
- Average ten-year null false alarms: **0.72% corrected / 0.92% EWMA**; worst-model **3.80% / 3.40%**.
- Average ten-year D=1 alarm: if true onset year2 **1.10% / 1.12%**, if year5 **0.83% / 1.03%**; rare alarms include a few that occur before the true change and therefore are not successful detections.
- Independent 500-path evaluation is too small for precise sparse-event estimates. Its simultaneous upper 95% confidence bound for worst false-alarm size is **6.93% / 6.41%**. The highly conservative realized alpha makes low power unsurprising. No universal detection impossibility follows.

## C. Unmodeled future volatility regime change

- Fix B's robust thresholds and rerun 500 **fresh** paths/model with primary and cycle innovations' **future** standard deviations increased (histories and fitted coefficients unchanged), no true exponent change:
- **+25%**: worst-family ten-year false alarm **5.2%** corrected / **6.8%** EWMA; 1 / 3 families respectively with empirical >5% size.
- **+50%**: worst-family false alarm **9.8%** corrected / **16.6%** EWMA; 2 / 5 families >5% size.
- This demonstrates **assumption sensitivity**, not the likelihood of future Bitcoin volatility shocks or an unconditional size guarantee. Other misspecifications (cycle periods, persistence or jumps) are still untested.

## Reproducibility, limitations and referee gate

- Six new tests verified frozen SHA, feature shape/sample alignment, future-only stress independence from pre-onset histories, CP cutoff selection, unknown-onset no-lookahead prefix invariance and 12-model output completeness. Five unknown-onset direct invariants separately passed. Environment Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0, pandas 2.2.3; BLAS single-thread.
- The complete generator's joint distribution has **not** yet been independently shown equivalent to the original v0.9 generator; comparison of screening medians is not enough. Further confidence requires higher-precision, independent holdouts, out-of-family testing, and a genuinely continuous/adaptive detector. Avoid claims of actual structural decline or permanent validity.
- **Next:** send the full Diagnostic 09 package to Claude with an explicitly adversarial brief to review CP simultaneous confidence, per-model versus shared cutoff comparability, monitor onset dates, future-only shock implementation and any statistical overclaim. **Do not merge into published v0.9 yet.**
