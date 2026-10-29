# Bitcoin's Price Power Law — reproducibility materials (v0.8 and v0.9)

Supporting code and documentation for **Bitcoin's Price Power Law: Stability, Maturation, and a Live Test of the Scaling Hypothesis**, technical drafts v0.8 (September 2026) and v0.9 (October 2026), with research data frozen through **2026-08-14**. Version 0.9 uses the same frozen sample, time origin and model specification as v0.8.

## Published papers and DOIs

- **Version 0.9 (October 29, 2026):** [Zenodo publication](https://doi.org/10.5281/zenodo.23774503) — DOI: [10.5281/zenodo.23774503](https://doi.org/10.5281/zenodo.23774503).
- **Version 0.8 (September 25, 2026):** [Zenodo publication](https://doi.org/10.5281/zenodo.22966136) — DOI: [10.5281/zenodo.22966136](https://doi.org/10.5281/zenodo.22966136).
- **All versions (concept DOI):** [10.5281/zenodo.22966135](https://doi.org/10.5281/zenodo.22966135), which resolves to the latest published version.

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

### Phillips-Perron: replaced in v0.9 (v0.8 value unreconciled)

The original Phillips-Perron scratch implementation did not survive, and no standard implementation reproduces the v0.8 reported statistic (`Zt = -2.380`). Version 0.9 replaces it with values computed by `arch` 8.0.0 (`PhillipsPerron(trend="c")`, Bartlett kernel) on the exact frozen file: **-3.0416 at 11 lags** and **-3.3072 at the automatic lag (34)**. On daily data with no constant, a constant, or a constant and trend, at lags between 1 and 365 and the automatic lag, the statistic lies between -2.98 and -3.61; on weekly and month-end samples with a constant, between -2.80 and -3.43. None reproduces -2.380, so the v0.8 value remains unreconciled and is withdrawn. `scripts/stationarity_checks.py` now computes PP and reports the archived v0.8 value alongside it.

## Version 0.9 robustness package

[`v09_robustness/`](v09_robustness/) contains the scripts behind the new v0.9 analyses: a declared family of persistent residual models, calibrated tests of rolling-window, post-2017 and curvature exponent statistics, power against a declining exponent, coverage of the intervals for `B`, simulated unit-root critical values and the compression of cycle extremes. It has its own README, pinned requirements (Python 3.13, `arch` 8.0.0), fixed seeds and tests. Its outputs are aggregate statistics only and follow the data policy below.

```bash
cd v09_robustness
pip install -r requirements.txt
python run_all.py /path/to/btc_daily.csv            # runtime varies; one clean two-worker rerun took about 42 minutes
python -m pytest -q tests
```

With the exact frozen CSV every deterministic number matches the paper and every simulation reproduces bit for bit with the pinned requirements; with independently obtained data add `--allow-different-sample`.

## Source provenance

Review of the production ingestion history strongly supports an inferred source composition of:

- [CryptoCompare / CoinDesk Data](https://www.cryptocompare.com) through 2026-01-10;
- [CoinGecko](https://www.coingecko.com) from 2026-01-11 through the paper cutoff.

**Price-data credit:** Earlier BTC/USD observations: [CryptoCompare / CoinDesk Data](https://www.cryptocompare.com). For observations dated 2026-01-11 onward: [Data provided by CoinGecko](https://www.coingecko.com). This credit follows the inferred source composition and does not establish row-by-row provenance.

The attribution is intentionally described as **inferred rather than cryptographically proven**. See [`docs/PROVENANCE.md`](docs/PROVENANCE.md).

## Repository contents

- [`paper/Bitcoin_Power_Law_Technical_Paper_v0.9.pdf`](paper/Bitcoin_Power_Law_Technical_Paper_v0.9.pdf) — the v0.9 paper
- [`paper/Bitcoin_Power_Law_Technical_Paper_v0.8.pdf`](paper/Bitcoin_Power_Law_Technical_Paper_v0.8.pdf) — the v0.8 circulation paper
- [`v09_robustness/`](v09_robustness/) — v0.9 robustness package (scripts, settings, aggregate outputs, figures, tests)
- [`figures/`](figures/) — publication figure images only; no figure-source daily tables
- [`scripts/reproduce_v08.py`](scripts/reproduce_v08.py) — deterministic reproduction calculations
- [`scripts/stochastic_checks.py`](scripts/stochastic_checks.py) — reconstructed bootstrap, structural-break null and AR(1) scale-invariance checks
- [`scripts/stationarity_checks.py`](scripts/stationarity_checks.py) — ADF and Phillips-Perron residual diagnostics with residual-based critical values; reports the unreproduced v0.8 PP value alongside the v0.9 replacement
- [`scripts/verify_exact_frozen_file.py`](scripts/verify_exact_frozen_file.py) — exact frozen-file SHA-256 check
- [`expected/v0.8_expected_results.json`](expected/v0.8_expected_results.json) — audited v0.8 verification targets: aggregate statistics plus two single-day values the paper also prints (the 2026-08-14 completed close and the 2026-06-30 episode-minimum residual), stored at full precision for testing; no daily series
- [`expected/v0.9_expected_results.json`](expected/v0.9_expected_results.json) — aggregate v0.9 targets (exponent-stability statistics, PP replacement values, calibration summaries)
- [`data/SCHEMA.md`](data/SCHEMA.md) — input schema
- [`docs/DATA_AVAILABILITY.md`](docs/DATA_AVAILABILITY.md) — data-withholding and user-supplied-data policy
- [`docs/PROVENANCE.md`](docs/PROVENANCE.md) — research/data provenance
- [`docs/REPRODUCIBILITY_SCOPE.md`](docs/REPRODUCIBILITY_SCOPE.md) — exact conventions and limitations

## Important interpretation limits

The v0.9 simulation results (calibrated p-values, power, interval coverage, unit-root critical values) are conditional on the declared residual-model family, which imposes a four-year stochastic cycle by design; they are not independent empirical findings and do not establish that such a cycle exists.

The repository reproduces the principal deterministic v0.8 calculations and reconstructs the documented stochastic methods. Some secondary v0.8 diagnostics are explicitly outside the reconstructed public implementation; see `docs/REPRODUCIBILITY_SCOPE.md`. It does not establish that the Bitcoin Power Law is immutable, that its numerical exponent is invariant to the time origin, that residuals are cleanly stationary under every specification, that the structural-break exercise proves structural change is impossible, or that historical episode recovery guarantees future recovery.

See the paper itself for the full statistical interpretation and limitations.

## License

The repository's **source code** is licensed under the [MIT License](LICENSE).

That code license does **not** apply to:

- the paper PDF, which remains copyright of its author(s);
- the publication figures, which remain copyright of their author(s); or
- any upstream/provider price data, which are not included here and remain subject to their own terms.

No rights to withheld provider data are granted or implied by the MIT license.
