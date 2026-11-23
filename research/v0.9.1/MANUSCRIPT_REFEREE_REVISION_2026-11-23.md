# Manuscript referee revision 2026-11-23 — six blocking items addressed in local revised draft

**Status: working paper, NOT publication-ready.** User supplied Claude AI manuscript referee ZIP `referee_manuscript_2026-11-23.zip`. Referee verdict **major revisions; concept accepted**. It explicitly did **not** request additional synthetic detector experiments for the publication-focused Project 1.

## Revisions carried out

1. Results tables added from existing D12/D13/D15/D16/D18 results: held-out simulation power/null alarms at fixed endpoints and daily surveillance, stress false alarms, corrected historical one- and two-break SSE gain p-value ranges. Tables include number of simulations and conditional binomial Monte Carlo SEs.
2. **Related work/novelty corrected**: explicitly cite the prior econometrics of spurious trends and monitoring; Santostasi–Perrenod, Faulkner, Baquero–Menezes 2026a and particularly their **November 10, 2026** paper `Deceleration without identification` (arXiv:2611.13962), which directly anticipates much of the broad identification discussion. We claim a narrow Bitcoin-specific *audited monitoring/break-test comparison*, NOT discovery of the fit-vs-structure distinction.
3. The expanding-slope price-dependence identity is described as **standard recursive least squares** and its sign consequence is stated.
4. Twelve-family weaknesses made explicit: same-sample selection, flat 3.7–6.1% daily SD for lambda0 against 2011 9.17% and 2025 2.19%, near-integrated members dominating worst-case thresholds, post-hoc lower-tail concerns.
5. 2014 price-source/volatility caveat prominently disclosed: 11.3382% calendar-day log-return SD from frozen CSV, 4.0231% when Feb 15–27 omitted from SD calculation (not a revised series). Prior limited noise-input sensitivity documented.
6. Gaussian random-walk/log-age-slope finite-information calculation **derived** in Appendix A with assumptions and stationary-AR / linear-time contrasts.

Withdrawal log and multi-knot projection-coefficient vs actual break-size estimand caution included. Invalid D17 block-bootstrap, D18 unsigned gain inversion and old D19 fixed-SD alternative confidence are excluded.

## Independent current-turn SHA-pinned CSV audit
Frozen 5,873-row input hash `ada93367320ad9c45d713650377ee683cf0b58d1ff8fb290fb72cd8b3168886f`; independently computed B **5.650938373388455**, R² **0.961280709**, residual SD **0.697088073**. RLS exact updating equation checked on 5,508 expansions, max double-precision cum-sum error **8.07e-12**. Best annual 1-hinge 2014 improvement **5.5188346%**; 2-hinge 2014/2016 **12.4719852%** of residual SSE.

## Package and remaining gates

A revised full manuscript, audit script/results, Claude review and itemized response were prepared as user-local `bitcoin_power_law_v091_manuscript_revision_2026-11-23.zip`. The complete manuscript is not yet committed to GitHub (the repo contains this summary and prior diagnostics). Do not present this summary file as the complete paper.

Pending: final independent Claude **manuscript-focused** read, expert-human econometric review, metadata and citation finalization, replay/packaging and permission decisions. No new open-ended detector study is required for Project 1. Project 2 remains separate. Published v0.9 and retirement dashboard unchanged.
