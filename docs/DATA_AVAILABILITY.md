# Data availability

## What is not distributed here

The 5,873-row BTC/USD price series used for the v0.8 paper is **not included** in this repository. Raw provider observations, the production price JSON, daily residual/fitted-value tables, figure-source tables containing daily observations, and per-row fingerprints are intentionally excluded.

This publication choice was made after review of the upstream data-provider redistribution restrictions. The repository is intended to expose the analysis, conventions, aggregate verification targets and two previously published single-day verification values without republishing the underlying provider-derived market-data series.

## Inferred price-data sources and attribution

Based on the ingestion history, the earlier BTC/USD observations appear to come from [CryptoCompare / CoinDesk Data](https://www.cryptocompare.com) (through 2026-01-10), and the later observations from [CoinGecko](https://www.coingecko.com) (2026-01-11 through the paper cutoff). For the later observations: **[Data provided by CoinGecko](https://www.coingecko.com)**. These source boundaries are inferred, not verified individually for each row; see [Provenance](PROVENANCE.md).

The two single-day verification values described below are already published in the v0.8 materials. They are retained without increasing precision. The underlying historical BTC/USD daily-price series is not released.

## What is published

The repository publishes:

- the v0.8 and v0.9 papers;
- the reconstructed publication reproduction code;
- statistical conventions and methods;
- deterministic verification targets: aggregate statistics, plus two single-day values that the paper also prints (the 2026-08-14 completed close and the 2026-06-30 episode-minimum residual), kept at full precision so the tests can check them;
- reconstructed bootstrap and structural-break Monte Carlo code;
- a new fixed publication RNG seed for reconstructed stochastic checks;
- the required input schema;
- provenance documentation;
- one whole-file SHA-256 for the exact frozen CSV used in the paper.

## Exact frozen-file identity versus statistical reproduction

The exact frozen CSV used for v0.8 has SHA-256:

`ada93367320ad9c45d713650377ee683cf0b58d1ff8fb290fb72cd8b3168886f`

That hash answers only one question: **is a local file byte-for-byte the exact frozen CSV used for v0.8?**

A reader who downloads Bitcoin history independently from an upstream provider should generally **not** expect to reproduce that hash. Provider revisions, endpoint conventions, decimal precision, close definitions and file serialization can all differ. A hash mismatch therefore does not by itself mean a reader cannot reproduce the paper's statistical methodology or obtain close results.

The older short research fingerprint recorded during the August audit is intentionally omitted here because its exact surviving computation/serialization convention is not documented well enough for an outside reader to verify independently. The whole-file SHA-256 above is the public identity check.

## Obtaining data

Readers should obtain Bitcoin historical price observations directly from a source they are lawfully permitted to use. For the closest methodological comparison to v0.8, construct a CSV following `data/SCHEMA.md` with:

- one completed UTC daily BTC/USD close per date;
- dates from 2010-07-17 through 2026-08-14 for the frozen-paper comparison;
- no duplicate dates or gaps;
- no partial current UTC day;
- `days_since_genesis = (date - 2009-01-03).days`.

Then run `scripts/reproduce_v08.py` against that local file.

## Note on the wording in v0.8

The v0.8 paper states that the frozen analysis dataset would be released publicly with the final publication version. After the paper text was frozen, the publication plan changed following review of upstream redistribution restrictions. The v0.9 paper formally replaces that statement with the policy described here.

## v0.9 outputs

The v0.9 robustness package (`v09_robustness/`) follows the same policy. It writes only aggregate statistics: model-level simulation summaries, p-values and statistics at a handful of named dates. Its tests fail if an output contains a daily-resolution series. Point values are limited to those the paper prints. The largest and smallest residual in each of the five halving epochs are given rounded to two decimals and without dates, so they cannot be tied to a particular day's close. Exponent estimates (slopes, not prices) are given at a handful of named dates. The package tests enforce the epoch format.
