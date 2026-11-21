# Structural-break forward engine — calibration audit 03 (2026-11-21)

**Status:** progress in engineering validation; no inferential power estimate yet.

## Material defect detected and repaired

A horizon-prefix invariance test initially **FAILED** in a local vintage-refitted forward simulation. Cause: the synthetic four-year stochastic-cycle innovation process consumed a horizon-dependent number of random values *before* drawing its initial latent state; requesting a longer forecast therefore changed the simulated historical/earlier future cycle state. This is an unacceptable form of simulation-horizon dependence.

Fixed in the repository's `research/v0.9.1/forward_family.py`: the stationary initial cycle state now comes from a **separate seeded RNG stream**, and the cycle uses an explicit initial filter state. The future horizon may be extended without changing earlier simulated draws.

The previously asserted seven prototype tests should not be treated as independently verified evidence of prefix invariance before this fix. Validation in a separate local vintage-refit prototype exposed the bug. The corrected local prototype passed its six unit checks and additional across-all-12-family prefix tests. The fixed GitHub module still needs CI or a direct full test run in its pinned environment.

## Historical-data source and model assumptions

Frozen 5,873-row private source independently matched published SHA256. OLS B=5.650938373388459 and residual SD=0.6970880734627248.

Volatility inputs based on *completed prior years only*:
- 2023 annual daily log-return SD = 0.02279753428;
- 2024 = 0.02774864969;
- 2025 = 0.02192479255.
- Future lambda=1 sensitivity (not an observed forecast): 2025 held constant 0.02192479255 vs 2023–25 simple mean 0.02415699217.

A local synthetic pre-onset calibration prototype was run on each of the 12 screened families with 35 independent training/calibration draws and 30 evaluation draws (four-year synthetic future, full past-vintage OLS refit for each path). Six new unit checks passed, including D=0 equivalence, anchored alternatives, identical seeds, EWMA no-future influence, and horizon-prefix equality. The prefix/anchoring test was additionally checked on every family.

Crucially, the *forecast residual* in this prototype is constructed relative to an OLS trend fitted to the **simulated history before the forecasting date**; a random-walk's accumulated pre-onset level is not naively compared with a fixed globally-known zero residual. This avoids the biggest false-alarm mechanism uncovered in audit 02.

## Why no detection probabilities are reported

Thirty evaluation paths per family are far too few to estimate a ten-year 5% first-alarm threshold or robust power. The prototype does not yet recreate all published 2010–2026 null screening statistics under its past-only fixed scale, and the fractional/RW initial-state assumptions need distributional equivalence checks. These are engineering smoke-test paths only.

## Next acceptance gate

1. Validate original `forward_family.py` under pinned dependencies with its seven unit tests after the RNG fix.
2. Match the historical ACF/scale/cycle screening-feature distribution of each new model to original v0.9 before forecast extension.
3. Freeze forecast-start conditioning, innovation scales, volatility extrapolation and false-alarm score definitions.
4. Only then simulate disjoint 2,000+ calibration and evaluation draws with whole-path first-alarm control, and report per-model power and resolution delays.

This work remains focused on the paper's structural-identifiability hypothesis, not optimizing a P10 downside forecast or retirement dashboard.
