# v0.9.1 manuscript referee rereview — minor revisions (2026-11-23)

**Reviewer:** Claude AI-assisted external review, NOT a human peer reviewer. **Verdict:** MINOR REVISIONS; original six major blockers addressed. Final edited working manuscript is packaged for the user as `bitcoin_powerlaw_v091_final_candidate_2026-11-23.zip`. **Published v0.9 remains frozen. The full final manuscript has not been committed to GitHub in this change.**

## Referee review and disposition

1. Corrected invalid Perron (1989) attribution for *endogenously selected break dates* to Zivot & Andrews (1992). Perron remains relevant to the persistence/break issue.
2. Table 4 one-hinge null exceedance range was replaced by the referee's **0.463–0.932** computed on the **same 1,000 null draws per 12 models** as corrected D18 two-hinge **0.541–0.981**. The new one-hinge rates are referee-reproduced but **not independently rerun** in this editorial session. Retired D15 single-hinge **0.529–0.942** from the main results table; no qualitative change.
3. Expanded positioning against Baquero–Menezes 2026b: it tests constant drift versus additional log-age term using a preregistered low-frequency/scale-invariant method and 1,216 declared noise models; our paper audits prospective structural exponent *change*, detection delays and false alarms under 12 historically screened families. Broad fit-vs-identification distinction is not original here.
4. Corrected **the referee's mistaken date recommendation**: official https://arxiv.org/abs/2611.13962 explicitly lists v1 submitted **Tue 10 Nov 2026 at 11:56:26 UTC**, not November 11. Retain 10 Nov citation and note any OSF prior registration separately.
5. D12 +25% volatility worst-family false alarms populated: ridge **5.67%**, EWMA **5.50%**. Table 3 SE revised to ~0.5–1.3 percentage points (1,200 vs 500 stress paths/model). Added large-break retrospective power sensitivity, 2014 perturbation, and corrected simultaneous calibration language.
6. Independently recalculated 2014 daily return-volatility exclusion including either endpoint in 15–27 Feb window: original **0.1133819164**, return-dated-window exclusion **0.0402313352** (352 return rows), either-endpoint exclusion **0.0402453016** (351 rows). Frozen dataset unchanged.
7. Changed reproduction provenance to *author rerun* and *AI-assisted referee audit*, not independent human reproduction. Original D17 bootstrap, unsigned-gain inference and unvalidated D19 multi-knot intervals remain withdrawn or excluded.

## Release status

**Exploratory preprint candidate, not yet approved or human-peer-reviewed.** No new detector simulation was run in this editorial revision. Final manuscript includes conditional quantitative rates only; it claims neither structural break proof nor permanent validity nor a universal detection impossibility. Open release steps: author proofread/metadata, citation/permissions check, reproducibility clean-room gate and optional specialist human econometric review. Project 2 early-warning feasibility remains separate.
