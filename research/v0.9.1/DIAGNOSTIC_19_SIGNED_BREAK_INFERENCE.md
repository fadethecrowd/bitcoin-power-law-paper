# Diagnostic 19 — Signed fixed-knot inference following D16–D18 referee check

**2026-11-23 | Status: exploratory; external AI referee pending.** Published v0.9 and frozen licensed Bitcoin daily prices unchanged.

## Referee correction

Claude's `referee_response_check_2026-11-23.zip` confirms that D18 corrected null p-values and D16–D18 break-inversion counts reproduce exactly. It also identifies a **statistical identification flaw** in our previously proposed unsigned SSE-gain inversion: under a random-walk-plus-cycle family, the chance of a low observed gain is similarly small for no break (0.059) and a −3 break (0.068) at 2017. Thus the old statement that a gain-based inversion excludes some large exponent deteriorations is **withdrawn**. D17's invalid block-bootstrap significance was already withdrawn and remains withdrawn.

## New signed slope change analysis

Under `log(price_t) = a + B log(age_t) + D [log(age_t)-log(age_at_knot)]_+ + u_t`, fixed-knot OLS has `Dhat = D + (linear function of u)`. This allows direct signed test inversion under each stipulated residual family, unlike unsigned fit improvements.

On the exact frozen 5,873-row SHA-verified Bitcoin history, with dates 2017-01-01 and 2020-01-01 chosen from earlier sensitivity scenarios:

| Fixed knot | Observed signed fitted D | Conservative envelope of family-conditional 95% Bonferroni two-date intervals |
|---|---:|---:|
| 2017-01-01 | **−0.5264** | **[−3.88, +2.83]** |
| 2020-01-01 | **−1.1110** | **[−5.45, +3.20]** |

The 2014/2016 dates were chosen by an earlier search and are **descriptive only**, not fixed-date confirmatory intervals. All twelve 2017/2020 model-specific intervals include zero.

## Simulation/coverage execution

- **12 original v0.9-screened residual families**; historical path simulation using aggregate-only calibration; 3,500 calibration + 2,000 globally disjoint independent holdout histories **per family** (**42,000 + 24,000 simulations** total).
- Two-sided .0125/.9875 quantile interval per knot, Bonferroni two-date coverage; union of twelve model-specific confidence intervals. Conditional on one of these families being correctly specified, this retains nominal >=95% coverage *across the two fixed dates*, ignoring finite quantile-calibration uncertainty.
- Held-out *two-date joint* empirical coverage **95.25%–96.85%**, mean **96.05%** across 12 models. These are point estimates of conditional simulation coverage, **not** a verified real-Bitcoin confidence guarantee.
- **Seven local tests pass**, including exact algebraic shift-invariance of Dhat under ±1 and ±3 alternatives and exact dataset SHA verification. Earlier overlapping *cross-family* calibration/holdout seed namespaces were detected by a test and corrected to globally disjoint bases; all holdouts rerun.
- Independently verified referee oracle pure-RW-component GLS slope-change standard deviations **1.89 (2017)**, **2.16 (2020)**, conditional on known Gaussian/volatility assumptions and trend parametrization. These are not universal Bitcoin information bounds.

## Interpretation and limitations

We can estimate the direction of the stipulated fixed-date signed slope shift (negative for both knots), but under the full twelve-family uncertainty the data remain consistent with **zero, substantial positive, and substantial negative shifts**. The original "can exclude a −3 decline from SSE improvement" claim was invalid, not merely imprecise.

The family itself was selected after screening the same actual historical residuals; out-of-family noise, market-data provenance, and the fact that the knot dates were motivated by earlier exploration limit strict inferential generality. Quantile calibration error is not included in the stated intervals. Inference is conditional on a *single fixed hinge*, not a universal estimate of a time-varying latent Bitcoin exponent.

## Next gate

An adversarial Claude referee package was created with full source, aggregate outputs and a written review brief, with **no licensed Bitcoin daily price series**. Ask Claude to verify signs, Bonferroni allocation, global seed independence, model union, power/coverage under true signed alternatives, date-selection validity, and whether original per-path residual normalization affects inverse confidence arguments.

Only after a critical review should this replace earlier break-size claims in a manuscript. Public v0.9 unchanged.
