# v0.9.1 — Referee D16–D18 response and independent rechecks (2026-11-23)

**Verdict: major revisions. AI-assisted referee, not human peer review.** Frozen v0.9 data and the published release remain unchanged. The full corrected code, reproducibility tests and non-reconstructing aggregate JSON are in the user's local `bitcoin_powerlaw_v091_d16_d18_referee_response_2026-11-23.zip`, **not committed with private BTC prices**.

## Confirmed/accepted corrections

**D16 two-hinge mathematics:** referee independently reproduced null p-values, calibration and power to ~4e-15 and verified exact two-hinge gain equals brute-force OLS. A two-year knot separation is a minimum-regime-length assumption, not a numerical stability requirement.

**D17 withdrawn:** referee's direct size check under twelve simulated *no-break* families showed the circular block bootstrap of residual levels rejects a true null **97–100%** at 30-day blocks (nominal 5%), **51.5–99%** at 90 days, with unreliable 365/730-day sizes. It is **invalid as break evidence, non-break evidence or a calibrated identification-sensitivity chart**. Historical source is preserved solely as a negative methodological example.

**D18 closure bug fixed:** the original nested `score` closed over mutable `mask`/design variables; its unmasked null paths were actually scored using the final masked design. Factory-function scoping fixed the error. **Independently reran all 12 models at original 1,000 paths/model and fixed seeds on the SHA-verified original file. Six local regression/consistency tests passed.** Correct full-sample p-value range **0.54146–0.98102** (previous reported 0.540–0.982); correctly masked 2014-Feb15–27 p-value range **0.54845–0.98302**, identical to previously published masked-case output. Largest full-sample p shift **0.004995**. Observed best two hinges still **2014-01-01, 2016-01-01**; ~**12.5%** original residual SSE reduction, ~**12.3%** excluding February anomalous rows. No null rejection under specified families.

**Selected slope signs:** refitted full historical log-price observed series at 2014/2016 hinges. Slope **6.964 before 2014**, **3.048 during 2014–15**, **5.881 post-2016**. Hinge deltas **−3.915 then +2.832**. These opposing fitted changes likely capture some 2014–15 bubble/correction structure; not independently established as changes in the true economic exponent.

## Fresh-seed break-size inversion: an exploratory follow-on

Independently implemented six illustrative alternatives, **1,200 fresh synthetic histories/model** across all **12** originally screened families (14,400 unique noise histories; six alternatives share shocks per history), single-hinge scan with 2013–23 annual knot search, observed gain 5.5%. The probability under a *stipulated true break* of observing a scan no more break-like than Bitcoin was:

| True change | Min–max across 12 models | Empirical p<0.05 cells | Mixed RW+cycle |
|---|---|---|---|
| −1 beginning 2017 | 0.058–0.322 | 0/12 | 0.058 |
| −2 beginning 2017 | 0.033–0.102 | 2/12 | 0.084 |
| −3 beginning 2017 | 0.000–0.068 | 11/12 | 0.068 |
| −1 beginning 2020 | 0.063–0.407 | 0/12 | 0.063 |
| −2 beginning 2020 | 0.081–0.185 | 0/12 | 0.081 |
| −3 beginning 2020 | 0.008–0.081 | 5/12 | 0.078 |

For p≈.05 and n=1200, binomial MC SE≈0.0063. These are **not posterior probabilities** for a Bitcoin break, **not simultaneous/multiple-model confidence bounds**, and the scenario grid was chosen after seeing the data/referee observations; model dependence and conditional calibration remain. The findings nevertheless reinforce the referee's point that enormous 2017 declines are hard to reconcile with this *specific* observed statistic under moderately persistent noise, but less so under a mixed random walk.

## Additional major reservations

- Family admission was screened against residuals from the very same observed history. A real break might inflate apparent residual persistence and bias toward non-rejection.
- Original per-path/per-component sample normalization constrains cycle shares and understates possible tails compared with unconditional mixture scales. Nonzero/diffuse initial state and volatility shocks need checking.
- Referee's finding that actual scan gains sit unusually low in *some* highly persistent model nulls was post hoc; no formal two-sided model rejection established.
- 2014 provenance requires cross-source replacement with documented source rules and re-screen, not merely deleting anomalous dates.
- A more robust broken-trend test needs to accommodate I(0)/I(1) uncertainty (e.g., suitably implemented Perron–Yabu / Harvey–Leybourne–Taylor), and persistence should be jointly evaluated under null and alternative.
- D17's old p-value-versus-block-length chart must **not** be used in public posts or manuscripts as a valid statistical significance finding.

## Scientific interpretation

Strong retrospective Power Law fit, a stable structural exponent, and prospective ability to recognize genuine deterioration are separate claims. No reliable broad rejection or proof of constancy has emerged. Some *large specified* breaks are conditionally constrained by the data; smaller changes remain difficult to exclude. This is an exploratory result pending external adversarial review and robust family-validity analyses.

**Next:** ensure this D18 repair and D17 withdrawal are propagated to the research manuscript, then pursue simultaneous/robust conditional inversion, break+persistence joint estimation and split-sample family-validity diagnostics. The published v0.9 is still frozen.
