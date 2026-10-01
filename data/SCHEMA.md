# Input data schema

The public repository does **not** include the frozen Bitcoin price observations.

The reproduction scripts accept a user-supplied CSV with these columns:

| column | type | meaning |
|---|---|---|
| `date` | `YYYY-MM-DD` | completed UTC observation date |
| `timestamp` | integer | UTC timestamp in milliseconds; used for validation only |
| `price_usd` | positive number | BTC/USD completed UTC daily close |
| `days_since_genesis` | integer | `(date - 2009-01-03).days` |

For the v0.8 research convention, the target sample is 5,873 consecutive completed UTC daily closes from `2010-07-17` through `2026-08-14` inclusive.

The regression itself uses only `price_usd` and `days_since_genesis`, but the other fields make date continuity and provenance mistakes easier to detect.
