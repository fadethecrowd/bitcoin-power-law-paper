# Bitcoin Power Law v0.9 — robustness package

Statistical implementation, robustness tests and reproducibility materials for
v0.9 of *Bitcoin's Price Power Law: Stability, Maturation, and a Live Test of the
Scaling Hypothesis*. It reproduces the v0.8 exponent results and the October 2026
review findings, then re-tests them against one declared family of residual
models. Results and their interpretation are in [`REPORT.md`](REPORT.md); the
status of every finding is in [`FINDINGS.md`](FINDINGS.md); recommended paper
changes are in [`V09_CHANGES.md`](V09_CHANGES.md).

## Data policy

No price data are included or written. The scripts read a user-supplied CSV in
the v0.8 schema (`date, timestamp, price_usd, days_since_genesis`). Everything in
`outputs/` is aggregate: statistics at a handful of named dates, model-level
simulation summaries and p-values. Daily exponent or residual series are never
written, because a full-precision daily exponent series (or a residual series
plus A and B) reconstructs the price series. Figures are 300-dpi rasters and plot
real-series paths at month-end resolution only. `tests/test_package.py` fails if
any output holds a daily-resolution series.

Point values are limited to what the paper prints. `reproduction.json` gives the
largest and smallest residual in each of the five halving epochs rounded to 2 decimals
and **without dates**, so they cannot be matched to a particular day's close. Earlier
drafts of this package gave them to 3 decimals with dates; that was removed before
release. Exponent estimates (slopes, not prices) are reported at a handful of named
dates. `tests/test_package.py` checks the epoch format.

`cache/` holds per-path statistics of *simulated* histories. It contains no real
data but is large; it is excluded from version control and is rebuilt by step 2.

## Running

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python run_all.py /path/to/btc_daily.csv            # about 20 minutes on 2 cores
python -m pytest -q tests                            # reproduction + output-policy checks
```

`outputs/OUTPUT_MANIFEST.sha256` lists the SHA-256 of every output file. Figures are also reproducible byte for byte with the pinned matplotlib, because `07_figures.py` ignores any local matplotlibrc and uses the bundled DejaVu Sans font. After a
rerun with the frozen file, `cd outputs && sha256sum -c OUTPUT_MANIFEST.sha256`
should report every file as OK.

With the exact frozen v0.8 file (SHA-256 `ada93367…886f`) every deterministic
number matches the published values and, with the pinned requirements, every simulation reproduces bit for bit.
With independently sourced data, add `--allow-different-sample`; results are a
methodological reproduction and will differ in detail, most visibly for
short-window statistics.

| Step | Script | What it does | Main outputs |
| --- | --- | --- | --- |
| 1 | `01_reproduce.py` | v0.8 baseline, HAC, post-2017, expanding, rolling (4–10 y), start dates, 2025 decomposition, breaks, unit-root tests, quantile slopes, epoch extremes; checks fast code against the v0.8 reference code | `reproduction.json` |
| 2 | `02_simulate_nulls.py` | 1,000 constant-B histories for each of 48 declared null models | `cache/null_*.npz` |
| 3 | `03_calibrate.py` | screens models against observed residual features; calibrates every statistic; max-T adjustment; break-detector null | `screening.csv`, `plausible_models.json`, `calibration*.csv`, `maxT.csv`, `breaks_null.csv` |
| 4 | `04_power.py` | power against declining local exponents (two shapes, seven sizes) under each plausible model | `power_curves.csv`, `size_table.csv` |
| 5 | `05_hac_unitroot.py` | coverage of Newey–West and block-bootstrap intervals; ADF/PP rejection rates; re-run of the v0.8 AR(1) illustration | `hac_coverage.csv`, `unitroot.csv`, `scale_invariance.json` |
| 6 | `06_asymmetry.py` | quantile-slope and halving-epoch asymmetry against symmetric and skewed shrinking nulls | `asymmetry.csv`, `asymmetry_observed.json` |
| 7 | `07_figures.py` | paper figures | `figures/*.png` |
| 8 | `08_bm_crosscheck.py` | checks the simulator against Baquero & Menezes (Oct 2026) Fig. 1b | `bm_crosscheck.json` |
| 9 | `09_sensitivity.py` | volatility-shape and cycle-period variants of the plausible models | `sensitivity.csv` |
| 10 | `10_skew_battery.py` | re-calibrates the exponent battery with Bitcoin's right-skewed residual distribution imposed on every null path | `skew_battery.csv` |
| 11 | `11_unitroot_critical_values.py` | simulates residual ADF and Phillips–Perron critical values for the exact design (random walk around `B ln t`), with constant and with Bitcoin's declining volatility | `unitroot_critical_values.csv` |

## Seeds and settings

All settings live in [`lib/config.py`](lib/config.py): master seed `20261025`;
per-stage, per-model seeds are `SeedSequence([20261025, stage, model_index])`.
Stages: screen 1, calibrate 2, power 3, interval coverage 4, asymmetry 5, sensitivity 6,
skewed battery 7, unit-root critical values 8. The v0.8 bootstrap reconstruction and the v0.8 AR(1) illustration use the
repository seed `20261001`.

## Relationship to the v0.8 repository

The v0.8 public scripts (`fadethecrowd/bitcoin-power-law-paper`, commit
`95b6a2a`) remain the reference for v0.8. This package re-implements the
estimators it needs in vectorized form and checks them against the v0.8 code
(`lib/reference.py`): the Newey–West SE and the break detector agree exactly on
the frozen series and on random test paths.

## Known limitations

* Baquero & Menezes' replication package (Zenodo 23218897) could not be
  retrieved here, so their low-frequency test S1 is not re-implemented; their
  declared-family design is adapted instead and compared with their published
  figures (step 8, step 5).
* The family is Gaussian in its innovations; heavy tails and volatility
  clustering within years are not modelled (Baquero & Menezes report little
  effect on low-frequency statistics). Right skew is imposed separately in
  steps 6 and 10.
* The v0.8 Phillips–Perron value (−2.380) could not be reproduced with a standard
  implementation. Step 1 reports the reproducible values from `arch` 8.0.0
  (`PhillipsPerron(trend="c")`): −3.0416 at 11 lags and −3.3072 at the automatic
  lag (34). On daily data with no constant, a constant, or a constant and trend,
  at lags between 1 and 365, the statistic lies between −2.98 and −3.61; on
  weekly and month-end samples with a constant, between −2.80 and −3.43. None
  reproduces −2.380.
