# Research and data provenance

## Frozen research sample

The v0.8 analysis is frozen to:

- completed UTC daily BTC/USD closes;
- 2010-07-17 through 2026-08-14 inclusive;
- 5,873 observations;
- zero missing dates;
- zero duplicate dates;
- Bitcoin genesis date 2009-01-03 for model time;
- no partial UTC day and no intraday/current spot in the regression.

The model is

`ln P(t) = ln A + B ln t`

fit by unweighted daily OLS with a free intercept.

## Inferred upstream source composition

The frozen series appears to be stitched from two upstream data paths:

- CryptoCompare / CoinDesk Data through 2026-01-10;
- CoinGecko from 2026-01-11 through the 2026-08-14 research cutoff.

This attribution is **inferred, not cryptographically proven**. It is strongly supported by the production ingestion code/history, file and output paths, row counts, and a clear precision-regime change beginning on 2026-01-11. The repository therefore describes the source boundary as an inference rather than claiming chain-of-custody proof for each row.

The production dataset continued updating after the August 14 research cutoff. Those later observations are outside the v0.8 research sample and must not enter a v0.8 reproduction.

The inferred 2026-01-11 provider transition occurs **inside the current below-trend episode**, which begins 2025-11-03 under the paper's strict 60-day episode definition. That is relevant when comparing alternative providers around the modern episode and is one reason a later cross-source robustness study remains separate from this v0.8 publication cleanup.

## Early-history market-structure note

The frozen sample includes the February 2014 Mt. Gox dislocation. Mt. Gox halted Bitcoin withdrawals on **2014-02-07** and went offline/suspended trading by **2014-02-25**. The note is included because the early history is high-leverage and market structure was unusually fragile; it is not used to alter or filter the frozen v0.8 series.

## Research-code provenance

The original August 2026 verification and volatility/recovery work was executed in isolated scratch directories. The audit record names files including `vlib.py`, `v1.py`, `v3.py`, `v4.py`, `v6.py`, `v8.py`, `v9.py` and several `.npz`/`.pkl` artifacts. Those scratch files were not preserved.

The code in this public repository is therefore a **publication reproduction implementation reconstructed from the frozen v0.8 paper, the audited research freeze, the pre-paper verification report and the frozen dataset**. It is not represented as the original scratch source tree.

Deterministic calculations have been checked against the frozen private CSV. Where original Monte Carlo seeds were not preserved, the public code uses a newly fixed publication-reconstruction seed and labels that fact explicitly.
