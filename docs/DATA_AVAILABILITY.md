# Data availability

## What is not distributed here

The 5,873-row BTC/USD price series used for the v0.8 paper is **not included** in this repository. Raw provider observations, the production price JSON, daily residual/fitted-value tables, figure-source tables containing daily observations, and per-row fingerprints are intentionally excluded.

This publication choice was made after review of the upstream data-provider redistribution restrictions. The repository is intended to expose the analysis, conventions and aggregate verification targets without republishing the underlying licensed market-data series.

## What is published

The repository publishes:

- the v0.8 paper;
- the reconstructed publication reproduction code;
- statistical conventions and methods;
- deterministic aggregate verification targets;
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

The v0.8 paper states that the frozen analysis dataset would be released publicly with the final publication version. After the paper text was frozen, the publication plan changed following review of upstream redistribution restrictions. The paper has not been withdrawn solely to revise that sentence. This repository documents the resulting availability policy. A later paper revision can update the statement formally.
