<!-- markdownlint-disable-file -->
# RPI Phase Details: Approved sensor backfill integration

## Metadata

* Task ID: 177-approved-integration-2026-10-27
* Task slug: sensor-backfill-177-approved-integration
* Plan: .copilot-tracking/plans/2026-10-27/sensor-backfill-177-approved-integration-plan.md
* Evidence: matching research artifact, C1-C8 and W1-W3.

## Phase Index

| Phase | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Climate child implementation | Active | P01-T01 |
| P02 | Identity child implementation | Complete, 6fc8d0fe; 51 tests pass | P02-T01 |
| P03 | Integrated generator and validation | Composition active; final climate merge awaits P01 | P03-T01, P03-T02 |
| P04 | Review and publication | Pending P03 | P04-T01, P04-T02 |

<!-- rpi:phase id=P01 -->
## P01: Climate child implementation

<!-- rpi:task id=P01-T01 -->
### P01-T01: Approved climate

Existing #425 retains 2023 Open-Meteo ERA5 and NASA POWER/MERRA-2 raw records,
strict hash/unit/hour alignment and derived bounds. Source approval now applies
to synthetic demonstration only, not a declaration that all underlying terms
were legally verified. Acquire a genuinely contiguous two-year Open-Meteo
window. Retain source URL/request, retrieval date, exact hash, source resolution,
UTC timestamps and record-derived temperature/RH bounds. A core adapter must
fail on missing/malformed/misaligned values rather than fill, repeat or clip
climate inputs. Output remains synthetic projected indoors. Validate coverage,
hash mismatch, gaps, nonnumeric/invalid RH and reproducibility.
Boundary: docs/climate-reuse-178-stack; bounded source evidence and core climate
adapter/tests only. No private data or unrelated #425 edits.

<!-- rpi:phase id=P02 -->
## P02: Identity child implementation

<!-- rpi:task id=P02-T01 -->
### P02-T01: Canonical identity and consumer

Stock Selection already preserves opaque <=128 UTF-16-unit IDs. Derive compact
uppercase sensor IDs from complete canonical key, reject any collision; keep
home IDs unchanged and reading IDs <=40. Adapt home admission to the stock key
contract and ensure SQL text widths/collations do not truncate or conflate keys.
The existing consumer's cases availability check must remain; tests construct
explicit synthetic cases with canonical keys instead of disabling it.
Preserve closed observation schema, policy/control consent/calibration, units,
mapping intervals, ordering, idempotency and fault rejection. Exercise actual
consumer on valid and adversarial generated rows. Boundary:
docs/backfill-consumer-183-stack, sensor_stock/identity helper, consumer and tests.
Consumer store availability limits must be documented honestly.

PC-001: existing SQL cases.id is NVARCHAR(64), not the full stock 128-unit domain.
Export remains <=128, while SQL consumer admission requires an exact existing
store-representable case key. Test 64/65/128 units, case distinctions and non-ASCII;
unsupported or absent keys remain explicit unavailable/refused, never aliases.
No shared cases/audit schema expansion is authorized here.
PC-002: reserve namespace for unmapped faults: valid compact sensor keys plus
the nine-character UNMAPPED- prefix must remain <=20, or use an explicit bounded
unmapped identity preserving legacy fault behavior. Prove real UNMAPPED, not
IDENTITY, adjacent valid admission and unchanged replay.

<!-- rpi:phase id=P03 -->
## P03: Integrated generator

<!-- rpi:task id=P03-T01 -->
### P03-T01: Merge and wire

After clean committed child delivery, merge #481-#485 into parent with normal
merge commits and required coauthor trailer. Resolve only overlapping README
additions, retaining all sections. Climate is an explicit opt-in input. Apply
household profile/conditions and explicit dated measures to versioned projection;
empty history is neutral, never infer works. Fingerprint all source/input models
in manifest. Keep fault truth outside analysis. Generated stock fixture is
explicit public synthetic IDs, no assertion of unseen private-register equality.
Allow deterministic gzip if needed; retain legacy non-integrated API/bytes.

PC-003 composition seam: introduce a versioned opt-in composed projection,
owned by indoor_projection, with explicit effective fabric loss multiplier
(finite >0 and <=1 for dated effects), household Condition (setpoint 16-22 C,
ventilation 0.8-1.2 and moisture finite >=0), and outdoor pair. Multiply baseline
dwelling*age*construction loss by active dated measure multipliers; do not pass
it as construction_loss. Use household setpoint in the heating temperature term;
divide the household moisture contribution by ventilation in the vapour term.
Keep existing project() and its RNG calls unchanged. Validate input domains and
version/fingerprint the composition. Test each household field, combined loss
below the legacy construction whitelist, exact completion boundary, unrelated
homes/no-history neutrality, exclusions and legacy regression.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Aggregate tests and scale evidence

Use existing external focused venv only after installed paths point here; pip
install editable core/dev if missing. Never uv or PYTHONPATH=mvp. Run smallest
selectors, then package discovery from src components with existing shared test
fixture paths. Measure full-hourly estimate before full output. Full 60,000-home
run spans complete actual two-year window at explicitly recorded supported
cadence; stream compressed output when necessary. Reconcile all generated IDs
and counts, record source/input/output hashes and actual storage; repeat bounded
same-input output byte comparison. A lower cadence is not full hourly validation.

PC-004: before P03-T01, update only the current status/prospective continuation in
docs/reference/research/iot-sensor-analytics-research-plan.md, reconcile the
docs/reference/README.md introduction and append docs/reference/log.md. Preserve
historical blocked/Residual outcomes, do not edit memory or regulatory snapshots.
Record actual results only; all such source edits precede Review/commit/gate.

<!-- rpi:phase id=P04 -->
## P04: Review and publication

<!-- rpi:task id=P04-T01 -->
### P04-T01: Independent Review

Reconcile plan/details/changes and actual results; activate rpi-review once.
Independent reviewer assesses integrated diff and adversarial semantic coverage.
Original result stays immutable. Open substantive findings route later work and
block readiness; no second Review to make the result green.

<!-- rpi:task id=P04-T02 -->
### P04-T02: Scoped gate and GitHub evidence

Commit implementation and dated original Review. Preserve any finite selected
cleanup candidates with archive/readback/restore hash verification before the
authorized git clean -fdxq. Fresh fetched origin/main binds exactly one foreground
tools/rpi-checks.py --changed --lock-timeout 0 --base SHA --out NEW_EXTERNAL_DIR.
No outer lock, detached/nohup execution, fallback, second generation gate or
changed protection. Retain failed receipt if blocked. Verify partial scope receipt
immediately before push and independent exact-head assessment. Update PR bodies
with precise evidence and limitations; resolve historical blocker comments in
#178/#183 with owner decision plus new technical proof. Refs only. Keep #486
draft if any check/review/publication prerequisite is unmet; never merge main.
