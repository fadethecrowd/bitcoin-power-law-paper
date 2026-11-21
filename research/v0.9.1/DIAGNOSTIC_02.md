# Diagnostic 02 — idealized power to detect local exponent declines

**Date:** 2026-11-21. **Status:** analytic/synthetic benchmark only. Not an empirical claim about the current Bitcoin exponent, and not a sequential monitoring alarm.

## Motivation
Our paper asks whether a sustained decrease in Bitcoin's local power-law exponent can be statistically distinguished from persistent price deviations. This diagnostic isolates that question under favorable *simple-versus-simple* assumptions: a known onset, known shift D, known stationary Gaussian AR(1) residual process and known original trend.

For age t0=6,432 days on 2026-08-14, the alternative has continuous deviation
m(t) = -D ln((t0+t)/t0)
for an abrupt decrease D in local log-price/log-age slope. The AR(1) residual has stationary standard deviation 0.30 and rho in {0.995, 0.997, 0.999}, initialized at zero at onset. A two-year linearly ramping slope alternative was also evaluated.

The transformed innovations have SD sigma_e = 0.30 sqrt(1-rho^2), and mean shift d_t = m_t - rho m_{t-1}. For a *fixed endpoint* horizon T, the simple-vs-simple Gaussian likelihood-ratio statistic has normalized separation
S = sqrt(sum_{t=1}^T d_t^2)/sigma_e.
Its exact one-sided 5% power is Phi(S-Phi^{-1}(0.95)). This is a best-case *Neyman–Pearson* benchmark within these fully specified Gaussian alternatives, **not** a universal bound for any composite / sequential detector, unknown-onset setting or different noise process.

## Verified results — rho=0.997, abrupt drop

| Exponent drop D | 1-year power | 2-year power | 5-year power | 10-year power |
|---:|---:|---:|---:|---:|
| 0 (null) | 5.00% | 5.00% | 5.00% | 5.00% |
| 0.5 | 6.10% | 7.26% | 13.05% | 32.98% |
| 1.0 | 7.38% | 10.23% | 27.32% | 77.76% |
| 3.0 | 14.57% | 30.31% | 93.05% | ~100% |

## Smooth two-year ramp, rho=0.997

| Drop D | 2-year power | 5-year power | 10-year power |
|---:|---:|---:|---:|
| 0.5 | 5.99% | 10.32% | 26.32% |
| 1.0 | 7.12% | 18.88% | 64.72% |
| 3.0 | 13.32% | 73.99% | ~100% |

## Verification
- Implemented in `oracle_detection_bound.py` and `test_oracle_detection_bound.py`.
- Six automated checks passed locally, including comparison of the closed-form normal power with a 100,000-draw random simulation.
- No licensed daily price information was read for the power computation; the time origin and published sample endpoint were used only to define age.
- Ancillary sensitivity at rho 0.995/0.999 is emitted by the script; do not cherry-pick rho 0.997 as the only model.

## Interpretation and scope
Even this favorable known-alternative calculation gives only 10.23% power for D=1.0 after two years. It is therefore unsurprising that realistic monitoring rules with unknown change dates, uncertain original B, multiple checks and changing volatility struggle to detect changes quickly. However this result **cannot establish** an impossibility theorem about Bitcoin, or demonstrate a true exponent decline.

This sharply supports the *paper-focused* primary experiment: assess the statistical identifiability of growth-law deterioration in the v0.9 residual-model family. Real-time P10 is only a bounded check on the interpretation of retrospective v0.9 floor statements, not the research centerpiece.

## Next formal experiment
Extend to the original twelve screened null processes (including stochastic cycle, near unit root/fractional/random-walk processes and declining volatility), estimate baseline parameter uncertainty, calculate performance of predeclared realistic detectors with full-path false-alarm control, and check the sensitivity of the findings to onset/shape. The pilot is not a substitute for that analysis.
