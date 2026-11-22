# Diagnostic 06 — State-conditioned false alarms and matched-checkpoint detection

**Date: 2026-11-22. Status: exploratory.** Full runnable code and aggregate results in `bitcoin_powerlaw_v091_diagnostic06_2026-11-22.zip`; no private BTC prices or synthetic daily price histories distributed.

## Question
Can models that control the overall 10-year false-alarm rate at 5% still generate materially different conditional false-alarm rates depending on where Bitcoin is trading relative to trend when monitoring begins? Do state-specific thresholds help? To make detector comparison fairer, evaluate both candidate methods only at exactly 1, 2, 5, and 10-year checkpoints.

## Procedure
- Original frozen private file independently hash-checked, 5,873 observations to 2026-08-14; 12 original screened v0.9 persistence/cycle/volatility model types.
- Three starting residual bins determined **solely from the simulated pre-onset OLS fit**: below -0.5, -0.5 to +0.5, above +0.5 log units.
- D=0 historical/forecast null scenarios used to calibrate a separate model/bin/detector cutoff. True local exponent declines of D=1 and D=3 evaluated on held-out, disjoint paths.
- Two detectors: (i) AR(.997)-whitened, signed, cumulative innovation-template score; (ii) 180-day EWMA forecast-gap score. Both observe **only** the same four dates and trigger when their accumulated signal exceeds their own cutoff at any checkpoint.
- **2,200 calibration paths and 1,200 independent evaluation paths/model** (26,400 calibration and 14,400 evaluation histories across all twelve models). The 12-model evaluation was run in four three-model batches using global model indices for deterministic unique seeds.
- Per-bin thresholds selected to make the *marginal, one-sided, 95% Clopper–Pearson upper bound* on each calibration group's null exceedances no greater than 5%. This is not simultaneous family-wise confidence control. The binomial calibration method and exact script are in the reproduction package.
- Local unit suite: **17 tests passed**. Published v0.9 model data and paper were not changed.

## Primary finding: model/start-state conditional, D=1 true local slope decline
| Rule | Detected by 2 years, min–max across 36 model/bin cells | Detected by 10 years | Observed 10-year null false-alarm range |
|---|---:|---:|---:|
| Innovation-score checkpoints | 0–6.41% | 1.29–23.42% | 0.65–7.92% |
| EWMA checkpoints | 0–5.13% | 2.90–17.05% | 0.62–6.87% |

For D=3, ten-year detection across model/bin cells spanned 18.31–98.27% for the innovation score and 18.48–90.91% for EWMA. Model-specific conditional detection power can improve relative to earlier unconditional detectors, but this does not solve the unknown-model/unknown-onset problem or make short-term D=1 detection reliable.

Weighted descriptive pooled 10-year null and D=1 rates across all models within each bin:
- Starting residual below -0.5: innovation null 2.91%, D1 6.90%; EWMA null 3.66%, D1 7.97%.
- Residual between -0.5 and +0.5: innovation null 3.95%, D1 12.92%; EWMA null 4.10%, D1 12.55%.
- Residual above +0.5: innovation null 3.59%, D1 11.49%; EWMA null 3.46%, D1 9.71%.

These pooled results mix models; they are **not** unconditional real-world Bitcoin probabilities or a claim about a known true stochastic model. Conditional evaluation bins have 158–852 paths/model, implying meaningful sampling error. Five of 36 model/bin cells for each method had observed false-alarm rates >5% in the disjoint holdout. The highest were 7.92% (innovation) and 6.87% (EWMA). This does not prove systematic failure given finite Monte Carlo and multiple comparisons, but **precludes claiming verified 5% conditional control in every group**.

## Scientific meaning
Conditional state calibration changes false alarms and measured power. Detecting a true local exponent decline is strongly model- and detector-dependent. A high historical Power Law R² is neither evidence of a timely prospective detector nor evidence that structural change is impossible to identify. **We have not established that Bitcoin's actual underlying exponent changed.**

## Important limitations / next requirements
1. These are **known-start**, calibrated-per-true-model experiments. A practical unknown-onset/unknown-model monitoring algorithm remains untested.
2. Calibration upper bounds are marginal, not simultaneous over 12 models × 3 state bins × 2 methods; finite-path conditional uncertainty remains substantial.
3. Simulation history is normalized using *only* historical detrended SD (the v0.9 retrospective convention), but full distributional equivalence, alternative scaling assumptions and future volatility are not independently confirmed for every process.
4. A 20-year robust experiment with a separately calibrated **20-year whole-path** size budget and onset-sensitivity is still necessary.
5. Request independent adversarial referee review of conditional thresholding, marginal-vs-simultaneous guarantees, the bin definitions, and the fairness of matching checkpoint schedules.
6. Any LinkedIn post should present these as **exploratory detector-specific outcomes**, not as proof the Power Law is broken or that every detector fails.

**Next execution:** increase evaluation sample for sparse bins and examine aggregate simultaneous size; implement onset-independent monitoring; package new materials for Claude's second pass. Public v0.9 unchanged.
