# Bitcoin's Price Power Law — v0.8 reproducibility materials

Supporting code and documentation for **Bitcoin's Price Power Law: Stability, Maturation, and a Live Test of the Scaling Hypothesis**, technical draft v0.8, with research data frozen through **2026-08-14**.

The paper studies the empirical relationship

`ln P(t) = ln A + B ln t`

using completed UTC daily Bitcoin closes, with `t` measured in days since Bitcoin's 2009-01-03 genesis date.

## Frozen v0.8 sample

- 2010-07-17 through 2026-08-14
- 5,873 completed UTC daily closes
- zero gaps and zero duplicate dates
- no partial UTC day
- no intraday/current spot in the regression
- unweighted daily OLS with a free intercept

Using the exact frozen file, the baseline fit is:

- `A = 4.1568315435e-17`
- `B = 5.6509383734`
- `R² = 0.9612807091`
- residual sample SD `= 0.6970880735`
- lag-1 residual autocorrelation `= 0.9969852404`
- naive OLS SE on `B = 0.0148014`
- HAC/Newey-West SE at lag 365 `= 0.1891599`

## Why the raw price file is not here

The frozen 5,873-row provider-derived price series is intentionally **not redistributed** in this repository following review of upstream data-provider redistribution restrictions. The same rule applies to raw production JSON, daily residual/fitted-value tables, figure-source tables containing daily observations, per-row hashes and other artifacts that would effectively reconstruct the provider series.

See [Data availability](docs/DATA_AVAILABILITY.md) for the exact scope and for the v0.8 paper's now-stale statement that the frozen dataset would be released.

## Reproducing the analysis with your own data

1. Obtain Bitcoin daily price history from a source you are lawfully permitted to use.
2. Construct a local CSV using the schema in [`data/SCHEMA.md`](data/SCHEMA.md).
3. Install the Python requirements.
4. Run the deterministic reproduction script:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/reproduce_v08.py /path/to/your/btc_daily.csv --output output/reproduction.json
```

For the reconstructed stochastic checks:

```bash
python scripts/stochastic_checks.py /path/to/your/btc_daily.csv --output output/stochastic.json
```

For researchers who already possess the exact frozen CSV, byte identity can be checked with:

```bash
python scripts/verify_exact_frozen_file.py /path/to/btc_power_law_paper_data_2010-07-17_to_2026-08-14.csv
```

The frozen CSV's SHA-256 is published in [`data/FROZEN_DATASET_SHA256.txt`](data/FROZEN_DATASET_SHA256.txt). Independently downloaded provider data will generally **not** match that hash byte-for-byte and are not expected to.

## Reproducibility status

The original August 2026 scratch research scripts were not preserved. The public scripts here are **reconstructed publication implementations**, built from the frozen v0.8 paper, the audited research freeze, the pre-paper verification report and the exact private frozen dataset. They are not represented as archival copies of the original scratch code.

The deterministic implementation has been checked against the exact private frozen file. The original stochastic RNG seeds do not survive, so the public Monte Carlo script uses a new, explicitly named publication-reconstruction seed (`20261001`). The repository therefore distinguishes exact deterministic reproduction from stochastic method replication. See [`docs/REPRODUCIBILITY_SCOPE.md`](docs/REPRODUCIBILITY_SCOPE.md).

### Phillips-Perron reconstruction note

The original Phillips-Perron scratch implementation did not survive. A standard reconstructed implementation did not reproduce the v0.8 reported statistic (`Zt = -2.380`). Rather than publish a contradictory number as if it were an exact reconstruction, the public stationarity script leaves PP uncomputed, records the v0.8 reported value, and marks the discrepancy unresolved for a later re-audit/revision.

## Source provenance

Review of the production ingestion history strongly supports an inferred source composition of:

- CryptoCompare / CoinDesk Data through 2026-01-10;
- CoinGecko from 2026-01-11 through the paper cutoff.

The attribution is intentionally described as **inferred rather than cryptographically proven**. See [`docs/PROVENANCE.md`](docs/PROVENANCE.md).

## Repository contents

- [`paper/Bitcoin_Power_Law_Technical_Paper_v0.8.pdf`](paper/Bitcoin_Power_Law_Technical_Paper_v0.8.pdf) — the v0.8 circulation paper
- [`figures/`](figures/) — publication figure images only; no figure-source daily tables
- [`scripts/reproduce_v08.py`](scripts/reproduce_v08.py) — deterministic reproduction calculations
- [`scripts/stochastic_checks.py`](scripts/stochastic_checks.py) — reconstructed bootstrap, structural-break null and AR(1) scale-invariance checks
- [`scripts/stationarity_checks.py`](scripts/stationarity_checks.py) — ADF / Engle-Granger-style residual diagnostics; the unreproduced v0.8 Phillips-Perron value is documented but intentionally not recomputed
- [`scripts/verify_exact_frozen_file.py`](scripts/verify_exact_frozen_file.py) — exact frozen-file SHA-256 check
- [`expected/v0.8_expected_results.json`](expected/v0.8_expected_results.json) — aggregate audited targets only; no daily provider data
- [`data/SCHEMA.md`](data/SCHEMA.md) — input schema
- [`docs/DATA_AVAILABILITY.md`](docs/DATA_AVAILABILITY.md) — data-withholding and user-supplied-data policy
- [`docs/PROVENANCE.md`](docs/PROVENANCE.md) — research/data provenance
- [`docs/REPRODUCIBILITY_SCOPE.md`](docs/REPRODUCIBILITY_SCOPE.md) — exact conventions and limitations

## Important interpretation limits

The repository reproduces the principal deterministic v0.8 calculations and reconstructs the documented stochastic methods. Some secondary v0.8 diagnostics are explicitly outside the reconstructed public implementation; see `docs/REPRODUCIBILITY_SCOPE.md`. It does not establish that the Bitcoin Power Law is immutable, that its numerical exponent is invariant to the time origin, that residuals are cleanly stationary under every specification, that the structural-break exercise proves structural change is impossible, or that historical episode recovery guarantees future recovery.

See the paper itself for the full statistical interpretation and limitations.

## License

The repository's **source code** is licensed under the [MIT License](LICENSE).

That code license does **not** apply to:

- the paper PDF, which remains copyright of its author(s);
- the publication figures, which remain copyright of their author(s); or
- any upstream/provider price data, which are not included here and remain subject to their own terms.

No rights to witheld provider data are granted or implied by the MIT license.
