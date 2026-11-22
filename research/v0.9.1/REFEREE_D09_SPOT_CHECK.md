# Diagnostic 09 — Independent referee's model-tail-mixture spot check (November 22, 2026)

The user-supplied `referee_d09_check_2026-11-22.zip` includes `round5_pcomb.py`, `round5.json`, and README. **Only the five lambda=0 models** were tested. Source and results were inspected, numerical summaries independently calculated from JSON; a full rerun **was attempted but timed out after training**. Treat figures below as referee-provided, **not independently reproduced Monte Carlo output**.

## Main experiment

Referee proposes a model-posterior-weighted *mixture of model-specific whole-path null-tail areas* instead of a shared threshold applied to raw scores. The mixture value is **not itself automatically a valid p-value**, so its threshold was independently calibrated using a second null split. Supplied mixture alarm cutoff P <= **0.0166023**; reference shared raw score cutoff S3 >= **3.43649**.

Five-model **mean** ten-year results (1,200 evaluation paths/model):

| Method | Null false alarm | D=1 detection | D=3 detection | D=1 detection by 2y |
|---|---:|---:|---:|---:|
| Shared raw cutoff | 1.77% | 3.82% | 29.65% | 0.52% |
| Posterior mixture of tail areas | 1.92% | 4.10% | 26.43% | 0.95% |
| Known-family oracle | 4.15% | 12.05% | 49.85% | 2.53% |

The tail mixture improved D=1 mean 10y detection by **0.28 percentage points**, but also increased observed null size by **0.15 points**; it underperformed raw scoring for D=3 and was not uniformly better across models. The known-family oracle operates at a *much larger achieved size*, so raw power comparisons remain confounded.

A basic integrity audit passed: all five model records were present, probabilities were within [0,1], and whole-path 10-year alarm rates were >= their two-year versions. However, the complete Monte Carlo rerun remains **unverified**.

## Methodological limitations

- This covers **5/12**, excluding changing volatility, fractional and mixed random-walk families.
- Each model has only 1,200 fresh evaluation histories; small differences can be Monte Carlo noise.
- Model posteriors derive from heuristic Gaussian historical-feature distributions, potentially misspecified.
- Both methods are designed around a known monitoring onset; neither establishes practical unknown-onset recognition.
- Size calibration only covers specified model family, not unexpected changes in future volatility/cycle structure.
- This statistic was developed after earlier results; preregister a fixed test before a new confirmatory fresh-seed study.

## Scientific conclusion

The referee has proposed an interesting alternative normalization of detector scores, **not a breakthrough** in robust real-time change detection. The strong historical descriptive fit remains distinct from latent structural stability and from prospective detection ability.

**Next:** preregister, implement and independently evaluate the mixture for **all twelve** families with larger disjoint batches; compare at matched achieved size and AUC; stress volatility and unknown onset; then seek external review.

**No change to frozen published v0.9.** The consolidated source+assessment package is maintained separately; no user data or licensed price observations were added here.
