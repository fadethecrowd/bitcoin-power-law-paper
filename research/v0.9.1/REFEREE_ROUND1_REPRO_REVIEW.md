# External referee reproduction — assessment of uploaded package (2026-11-22)

**Provenance:** independently supplied ZIP `referee_reproduction_2026-11-22(1).zip` (README.md, referee_checks.py, extra_checks.py, extra_checks_output.txt, full.json). This note is our *inspection of the referee's provided scripts and outputs*, not an independent rerun of all computations. The original private licensed data were not present. The ZIP is not a conventional narrative peer-review report.

## Scope
Referee explicitly ran the **five lambda=0 models**, not all twelve screened null models. These are:
- `ar0.990|cyc0.8|lam0`
- `ar0.995|cyc0.4|lam0`
- `ar0.997|cyc0.4|lam0`
- `ar0.998|cyc0.4|lam0`
- `ar0.999|cyc0.4|lam0`

Inputs: historical calendar-day grid, frozen sample dates and published residual SD 0.697088; package simulation engine. Original experimental calibration/evaluation draws: 5,000 / 3,000. Referee's scripts report E0–E5 variants and extra checks. Seven lambda=1/fractional/random-walk models **not** independently reproduced.

## Main findings from full.json
1. **Reproduction E0:** null and D=1 power from the original 180-day EWMA detector were closely reproduced with its exact original seeds and thresholds. This supports code consistency but using the *same seeds* is not a fresh independent Monte Carlo validation.
2. **E1: matched 2-year false-alarm horizon.** Calibrating a 2-year rather than a 10-year alarm budget raised D=1 detection at 2 years from the original generally sub-1% rates to **4.83–5.83%** (five models); but the 2-year null false-alarm rate was already **4.0–5.13%**. The marginal power above size is still small. This demonstrates the importance of comparable error budgets.
3. **E2: variance-standardized boundary.** Standardizing each monitoring date by its null time-varying score SD produced ten-year D=1 power about **5.4–7.0%** in these five models, compared with **6.6–8.5%** for the original unstandardized 180-day EWMA in the same five. It did not fix the weak power in this test.
4. **E3: known-alternative, fixed-horizon covariance-aware linear discriminant (referee describes as oracle Neyman–Pearson).** At a two-year 5% endpoint size, D=1 power was **6.2–8.1%**. At ten years, D=1 power **12.8–72.7%**, highly model-dependent. D=3 ten-year power **44.6–100%**. The method knows D, onset and covariance, uses the simulated history summary, and has a **fixed-horizon 5% test**, not a ten-year sequential 5% any-time false-alarm budget. Its covariance is *estimated from synthetic data*, so it is an approximation to the idealized Gaussian oracle, not an exact closed-form NP bound. Nevertheless, it concretely shows alternative decision rules can be much stronger on some models, particularly over ten years.
5. **E4: per-path normalization sensitivity.** Original historical per-path detrended-scale factors have coefficient of variation **7.0–11.7%** for the five models. Fixed model-median scaling yielded similar, but not identical, D=1 ten-year EWMA power (**7.2–8.9%** versus **6.6–8.5%** under historical per-path normalization); thus scaling is not the main cause of weak EWMA performance *in these five cases*. Remaining seven models require testing.
6. **E5: conditional false alarms by initial trend residual.** With original unconditional ten-year EWMA threshold, the false-alarm rate for initial residual **>+0.5** log units was about **12.6–15.1%**, versus typically **0–0.9%** for starting residual **<-0.5** (with some near 2.8% among near-trend starts). This matters: unconditional size is not conditional size. False alarms are highly uneven across initial states.
7. **Extra conditional refit:** For a below-trend start (initial residual <=-0.5), calibrating a separate 5% threshold in three lambda=0 models gave ten-year D=1 detection about **7.8–11.2%**. D=3 about **20.1–56.0%**. Conditioning changed threshold and performance but did not restore strong short-horizon detection.
8. **Original-generator distribution comparison:** two AR+cycle lambda=0 models compared against original v0.9 generator using 1,000 paths each and selected KS tests. Reported KS p-values for ACF(365), ACF(1461), zero-cross, spectral band, and historical slope error were **0.22–0.97**; the slope-error SD was 0.263 vs 0.266 for AR(.995), and 0.516 vs 0.547 for AR(.999). Failure to reject at 1,000/model does NOT prove equality. In particular, comparisons exclude other screened models, the full joint distribution and the lambda=1 historical volatility shape.

## Reproducibility caveats
- `referee_checks.py` requires our *separately supplied* original `family_experiment.py`, `detector_comparison.py`, and `detectors_5000_3000.json`; the five-file ZIP alone is not self-sufficient.
- `extra_checks.py` contains hardcoded paths on the referee's machine (`/home/claude/...`), so it is not directly portable without edits.
- This review inspected the supplied aggregate `full.json` and script code. We should re-execute checks with clean dependencies before treating results as a confirmatory independent replication.

## Implications for the paper
- **Supports:** our existing 90/180/365-day EWMA alarm is weak at identifying two-year exponent declines under the tested price-persistence models.
- **Strong qualification:** no inference that any structural break is impossible to detect quickly; model-aware likelihood tests can perform better. The real finding might be the tradeoff between modeling assumptions, conditional state and timely detection.
- **New research requirement:** define and test *starting-residual-state-conditioned* alarm thresholds and distinguish unconditional vs conditional false-alarm control.
- **Comparison fairness:** ensure 2-year fixed-horizon oracle and 10-year sequential alarm are not naively compared.
- **Scientific status:** no new evidence that actual Bitcoin's underlying growth exponent has broken. This is about the *power of detection procedures* under the declared models.

## Action list / next steps
1. Treat this package as Round 1 partial independent validation, not the final referee verdict.
2. Implement a genuinely distinct practical detection method (e.g. conditional innovation CUSUM / Gaussian forecast likelihood score) under matched 10-year sequential false-alarm budget, and include initial-state conditioning.
3. Reproduce the referee's five lambda=0 comparisons with portable scripts, confirm matched null-distribution tests on *all twelve* models (especially lambda=1, RW and fractional).
4. Add 20-year and ramp-change sensitivity, calibrating false alarms over their own surveillance horizons.
5. Re-submit updated full reproduction bundle to referee, request review of theoretical identifiability claims, and decide whether the November 24 LinkedIn communication should be a preliminary-methods post only.

**Never state that the referee endorsed an actual change in Bitcoin's exponent or that its Power Law is broken.**
