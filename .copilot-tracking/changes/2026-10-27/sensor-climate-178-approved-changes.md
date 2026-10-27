---
title: Approved paired climate child implementation
description: Genuine two-year ERA5 input, typed core adapter and scoped sensitivity evidence
ms.date: 2026-10-27
---

Refs #178, parent #177. P01 implementation on
`docs/climate-reuse-178-stack`, existing PR #481 targeting
`feat/sensor-backfill-177`. Initial child head:
`8871cbd3b7704212b538d284f04668c51dbd8042`.

## Approval and Scope

The supplied owner decision `owner-approvals-2026-10-27-b` approves existing
candidate climate reuse terms for the synthetic demonstrator and child
integration. This prospectively supersedes the owner-decision blocker in the
earlier child record. It does not erase historical UNMET outcomes or establish
underlying C3S, NASA, commercial or production legal permission.

Explicitly scoped reuse from unmerged candidate
`72f5235889fcf42632e30d4003436f02849c0f12`:

* Adapted the strict hash, unit, hourly alignment and Magnus consistency
  approach from `tools/climate_paired_bounds.py` into typed core code.
* Retained the exact NASA POWER MERRA-2 2023 raw bytes, original request,
  retrieval date, API version, attribution and unverified licence status.
* Derived a compact sensitivity summary instead of duplicating the candidate's
  177,317-byte full report. Preserved the original report SHA-256 and original
  2023 comparison, separately from the comparison with the new primary input.
* Executed the candidate's unchanged 30-test module against a scoped external
  extraction of its code and evidence.

No candidate PR merge, unrelated candidate code/history import, parent artifact,
generator, indoor projection, shared README or knowledge-base index/log/synthesis
edit occurred. The parent owns wiring and knowledge-base updates.

## Genuine Two-Year Acquisition

Retrieved the official public archive endpoint on 2026-10-27. The one response
requests both calendar years explicitly, including leap day; the earlier
candidate year was neither repeated nor concatenated into this input.

```bash
curl --fail --silent --show-error --retry 2 --max-time 180 \
  'https://archive-api.open-meteo.com/v1/archive?latitude=54.775&longitude=-1.585&start_date=2023-01-01&end_date=2024-12-31&hourly=temperature_2m,relative_humidity_2m,dew_point_2m&models=era5&timezone=UTC&temperature_unit=celsius&timeformat=iso8601' \
  -o docs/reference/research/climate-paired-source-178/open-meteo-era5-durham-2023-2024-raw.json
```

The response bytes are retained unchanged. A future acquisition may return
different bytes or revised values; use these committed pins for replay rather
than assuming the endpoint reproduces the same hash.

| Property | Actual result |
| --- | --- |
| Request location | Durham, latitude 54.775, longitude -1.585 |
| Returned cell | Latitude 54.75, longitude -1.5, elevation 65 m |
| Model | Explicit `models=era5`, not best-match or ERA5-Land |
| Source resolution | Hourly, 0.25-degree ERA5 grid |
| Source resolution reference | <https://open-meteo.com/en/docs/historical-weather-api>, HTML checked 2026-10-27 |
| Time standard | Response GMT, offset zero; adapter uses aware UTC |
| Window | 2023-01-01T00:00Z through 2024-12-31T23:00Z inclusive |
| Half-open end | 2025-01-01T00:00Z |
| Complete records | 17,544 paired hours, 731 days |
| Temperature bounds | -5.3 to 26.9 degC |
| Relative humidity bounds | 36 to 100 percent |
| Dew point bounds | -7.1 to 19.6 degC |
| Maximum Magnus RH residual | 0.845228 RH percentage points; tolerance 1.0 |
| Source/API revision | ERA5 and `/v1/archive`; exact data revision/server build not exposed |

Bounds are computed from every actual record, not imposed replay limits,
instantaneous design extremes, regional safety thresholds or station
observations. The new request's default returned elevation is 65 m, unlike
the candidate's 98 m at requested latitude 54.768. The original candidate
comparison and new-primary comparison are explicitly distinguished.

### Input and Metadata Pins

All four files are in `docs/reference/research/climate-paired-source-178/`.

| Filename | Bytes | SHA-256 |
| --- | --- | --- |
| `open-meteo-era5-durham-2023-2024-raw.json` | 542897 | `af76a90414d9ad8f19dacc95a38f06d4c4321a91bdf030ba231558c42506051e` |
| `open-meteo-era5-durham-2023-2024-metadata.json` | 5550 | `628e05cb4a8ce6731800dd3a587be8180f4a3a5e04f62b8577e5020d79cf48b4` |
| `nasa-power-merra2-durham-2023-raw.json` | 327067 | `cba9cf308878e9a4b2f2847cbbc4e66f06d14a1b734d4da48be0133fef9c6db1` |
| `nasa-power-merra2-durham-2023-sensitivity.json` | 3237 | `877348102df6f364b09f6d775316e8b498c3fde17373ab3c0dc6811dbc11e3f6` |

NASA bytes were extracted without transformation:

```bash
git show 72f52358:docs/reference/research/climate-paired-sample-178/nasa-power-merra2-durham-2023-raw.json \
  > docs/reference/research/climate-paired-source-178/nasa-power-merra2-durham-2023-raw.json
```

The retained NASA request is
<https://power.larc.nasa.gov/api/temporal/hourly/point?parameters=T2M,RH2M&community=RE&longitude=-1.585&latitude=54.768&start=20230101&end=20231231&format=JSON&time-standard=UTC>.
Its retrieval date is 2026-10-22 and retained header identifies POWER Hourly API
v2.10.3. All 8,760 UTC hours validate. Actual NASA bounds are -3.35 to 24.61
degC and 43.43 to 100 percent RH. It is sensitivity evidence only, not 2024
coverage or a source for filling primary records.

## Parent Integration Contract

Implementation:
`src/core/src/zava_forward/core/synthetic/climate_history.py`.
There is one new test module, `src/core/tests/test_climate_history.py`,
with 12 test methods.

```python
from datetime import UTC, datetime
from pathlib import Path

from zava_forward.core.synthetic.climate_history import ClimateHistory

pack = Path("docs/reference/research/climate-paired-source-178")
climate = ClimateHistory.read(
    pack / "open-meteo-era5-durham-2023-2024-raw.json",
    pack / "open-meteo-era5-durham-2023-2024-metadata.json",
)
pairs = climate.series(datetime(2023, 1, 2, tzinfo=UTC), days=730, cadence=360)
metadata = climate.manifest()
```

* `ClimateHistory.read(path, metadata_path, *, expected_sha256=None,
  expected_metadata_sha256=None) -> ClimateHistory` is the actual constructor.
  The caller trusts the metadata contract unless externally pinning it;
  committed tests pin both files independently.
* `series(start: datetime, days: int, cadence: int)
  -> list[tuple[float, float]]` returns temperature degC and RH percent.
  Cadence is minutes, a positive whole-hour multiple dividing 1,440.
  Start must be an aware UTC exact hour; the entire half-open window must fit.
  Non-midnight starts are supported without realignment.
* Sampling uses exact source timestamps, never filling, clipping, repeating or
  interpolating. Unsupported subhourly cadence fails.
* `manifest() -> dict[str, object]` returns a detached JSON-serializable copy
  with source/request/retrieval/version/resolution, coverage, derived bounds,
  terms, approval, `input_sha256` and `metadata_sha256`.
* `start` and `end_exclusive` are aware UTC datetime attributes. There is no
  `revision_sources()` method; the manifest supplies the pins.

Strict admission checks hashes/bytes, JSON objects/duplicate keys, supported
metadata, units, explicit UTC, full aligned coverage, finite numeric values,
RH in 0..100, dew point <= temperature, Magnus consistency, source request
period/model/coordinates, returned grid and record-derived bounds.

## Validation

Isolated external tooling was installed with the repository dev pins, without
uv, cloud models, credentials or private data:

```bash
python3 -m venv /home/azureuser/.local/share/ama/backfill-177-climate-20261027/venv
/home/azureuser/.local/share/ama/backfill-177-climate-20261027/venv/bin/python \
  -m pip --quiet install -e 'src/core[dev]'
```

From `src/core`, using that environment's Python:

```bash
export TMPDIR=/home/azureuser/.local/share/ama/backfill-177-climate-20261027/scratch
python -m ruff format --check src/zava_forward/core/synthetic/climate_history.py tests/test_climate_history.py
python -m ruff check src/zava_forward/core/synthetic/climate_history.py tests/test_climate_history.py
python -m mypy src/zava_forward/core/synthetic/climate_history.py tests/test_climate_history.py
python -m unittest discover -s tests -p test_climate_history.py -q
python -m unittest discover -s tests -p test_sensor_backfill.py -q
python -m unittest discover -s tests -p test_sensor_plausibility.py -q
```

Results: Ruff format/lint pass; strict mypy passes both new files; new climate
tests 12/12; existing backfill tests 5/5; existing plausibility tests 8/8.
The backfill tests emit pre-existing unclosed-file ResourceWarnings but pass.
Use `TMPDIR` set to the external acquisition scratch for tests that create files.
The new climate tests do not create scratch files.
The final combined targeted runner also passes 25/25:

```bash
python -m unittest tests/test_climate_history.py tests/test_sensor_backfill.py tests/test_sensor_plausibility.py -q
```

Candidate regression command, using an unchanged scoped extraction in the
external acquisition scratch:

```bash
python -m unittest discover \
  -s /home/azureuser/.local/share/ama/backfill-177-climate-20261027/candidate/tools \
  -p test_climate_paired_bounds.py -q
```

Candidate results: 30/30 pass, including regeneration of the historical report.
The candidate parser also successfully validates the new 17,544-hour response.
The parent-shaped smoke call in the integration example returns exactly 2,920
pairs for 730 days at 360-minute cadence; strict JSON serialization of the
manifest also passes.
`git diff --check` passes.

## Terms, Limits and Handoff

Attribution: Weather data by Open-Meteo.com (<https://open-meteo.com/>),
CC BY 4.0; underlying ERA5 is Copernicus Climate Change Service (C3S) material.
Raw bytes are unchanged; bounds are summarised and exact timestamps subsampled
for synthetic indoor projection. Dataset citation: Hersbach et al. (2023),
ERA5 hourly data on single levels from 1940 to present, ECMWF,
<https://doi.org/10.24381/cds.adbb2d47>. Software citation: Zippenfenig (2023),
<https://doi.org/10.5281/ZENODO.7970649>.

The candidate's published terms snapshot was read on 2026-10-22:
<https://open-meteo.com/en/terms>, <https://open-meteo.com/en/licence> and
<https://power.larc.nasa.gov/docs/referencing/>. Its free-API non-commercial
condition and attribution are preserved, not reinterpreted as production
permission. NASA attribution retains POWER Hourly API v2.10.3 and access date
2026-10-22. No new complete legal-terms retrieval is asserted. Underlying C3S
reuse and NASA licence text remain unverified; the candidate recorded HTTP 403
for the NASA data policy page.

No acquisition blocker remains for this child. Single-cell modelled outdoor
history is not station-grade/regional verification, production acceptance or
observed indoor measurements. Generated indoors remain synthetic. Parent
generator wiring, 60,000-home run, aggregate gate, independent review and
publication remain parent responsibilities. No RPI gate, push, PR/issue
modification or merge was performed by this child.
