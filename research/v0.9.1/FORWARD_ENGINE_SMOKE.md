# Forward 12-family engine — initial engineering smoke test (2026-11-21)

This is an **implementation milestone, not a finding about whether Bitcoin's power-law exponent is changing**.

## Completed
- Added `forward_family.py` to the research branch, with explicit support for all 12 screened v0.9 residual model identifiers: ten AR(1) models, one fractionally integrated model, and one random-walk model, each with its specified stochastic-cycle weight and volatility-profile label.
- Supports synthetic pre-onset warmup and continuous, anchored shifts in the forward local exponent.
- Uses two independent pseudorandom streams for persistence and cycle components; future-volatility sensitivity is explicitly provided instead of read from future Bitcoin prices.
- **Does not** divide simulated paths by their realized future residual standard deviation.
- Added `test_forward_family.py`; all 7 engineering tests passed in a local Python environment. These include all 12 model identities, deterministic seeds, no future-horizon prefix changes, future volatility isolation for lambda=0, input validation and continuous break anchoring.
- Separate `FORWARD_EXPERIMENT_SPEC.md` freezes intended scientific comparisons before examining all-family performance.

## NOT yet complete / scientifically critical
- **Parameter calibration:** `persistence_scale=.015` and `cycle_scale=.015` are placeholder innovation scales, not calibrated to the original v0.9 observed residual variance and component mix. Do not run scientific power calculations with these defaults.
- **Historical-volatility profile:** lambda=1 currently indicates a predeclared forecast multiplier but does not yet reconstruct original v0.9 historical annual-volatility scaling. The future assumption must be fit from *past-only* returns and sensitivity tested.
- **Equivalence check:** must quantitatively check synthetic pre-onset path properties (ACF, cycle amplitude, marginal residual variance, historical screen statistics) against original v0.9 `lib/nulls.py` on the original time grid before comparing research outcomes.
- **Fractional and RW uncertainty:** finite warmup behavior and statistical calibration must be validated; they are not interchangeable with stationary AR behavior.
- **Detection thresholds:** not yet optimized, calibrated or validated across the 12-model family; neither 5% false-alarm control nor detection power has been established for this new engine.
- **Seed/version freeze:** pin runtime package versions and commit the final configuration before confirmatory simulation.
- Historical observed exponent decline, simulation results and P10 exploratory analysis reported earlier remain separate and unchanged.

## Next execution gate
Perform pre-onset distribution matching and past-only innovation-scale calibration, then validate whole-path false alarm behavior across the screened family before running any alternative-break power experiment. If models fail equivalence, fix the simulation machinery and re-run tests, not the scientific thresholds.
