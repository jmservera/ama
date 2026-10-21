---
title: In-Use Monitoring Analytics Research Plan (Dew Point and Trend Risks)
description: Research phase plan for analysing humidity and temperature sensor data received through Azure IoT Hub, including dew point and surface condensation risk, with leads, unknowns, evidence rules and exit criteria
author: AMA programme
ms.date: 2026-10-27
ms.topic: reference
---

## Status

Plan with a first source check. Nothing here is a validated method,
threshold, legal duty or approved rule. The leads came from an uncited web
synthesis and were checked on 2026-10-14 against the sources in
[Source verification (2026-10-14)](#source-verification-2026-10-14). Phase R1
remains open: the standards are paywalled and several confirmations rest on
secondary sources, so a competent reviewer must confirm against the official
text before use. Sensor data remains
simulated until the open items in
[BRD OD-43](../../brds/agentic-retrofit-programme-brd.md) are closed.

The separate [historical climate evidence update](#historical-climate-evidence-2026-10-17-refs-178)
now includes official product/terms checks and retrieved Durham monthly
temperature statistics. It does not validate the indoor analytics methods,
supply humidity records or approve external-data reuse.

Related decisions: [ADR 0003](../../adrs/0003-journey-derived-capabilities-runtime-fit.md)
(Azure IoT Hub ingestion), [ADR 0002](../../adrs/0002-pilot-readiness-architecture.md#sensor-data-capture-analysis-and-map)
(capture and review-signal design), BRD FR-048/AC-090 and RULE-014, and PRD
FR-050 with AC-066 to AC-068.

## Shared observation contract and volume (2026-10-18, Refs #186)

This documents the unchanged finite consumer merged in
[PR #411](https://github.com/jmservera/ama/pull/411) at
`100ead1bacdb72a8ea7ce5867233db30b22b2f50`. The contract dependency on
#110 is supplied by that merge; whole issue #110 and its live acceptance gates
remain open. Parent #184 is hierarchy, not delivery ordering.
This is shared-contract verification and measured accounting, not live producer
or backfill interoperability, a new schema, or a transport implementation.

### Authority and required observation fields

The authoritative version and closed field set are
[`synthetic.sensor_faults.SCHEMA_VERSION` and `READING_FIELDS`](../../../src/core/src/zava_forward/core/synthetic/sensor_faults.py).
The [consumer imports both directly](../../../src/core/src/zava_forward/core/sensor_consumer.py);
its `_shape`, `_quality`, `process` and `preflight` define current validation.
The table below describes that source, not an independently maintained schema
API. There is no version negotiation: only `sensor-fault-input-v1` is accepted.
Do not substitute the legacy backfill `reading-v1` SQL/CSV shape.

One observation is **one record containing both temperature and relative
humidity**, not two scalar records. All 13 fields below are required, and all
values are JSON strings, including numbers and the calibration claim. Extra
fields, evaluator labels, clean/truth records and `injected_fault` are not part
of this observation. Only `Packet.rows` are delivered observations; a generator
`Packet` groups two observations for evaluation, not a chosen wire message.

| Field | Required type | Current constraint / meaning |
| --- | --- | --- |
| `sensor_id` | string | 1..20 uppercase ASCII letters/digits/underscore/hyphen; first character letter or digit |
| `reading_id` | string | Same alphabet/first-character rule, 1..40; stable within the sensor namespace |
| `home_id` | string | Same alphabet/first-character rule, 1..12; independently configured mapping and existing home must agree |
| `observed_at` | string | Valid UTC calendar time, exactly `YYYY-MM-DDTHH:MM:SSZ`; no offsets or fractional seconds |
| `temperature_c` | string | Decimal grammar `-?(0\|[1-9][0-9]{0,2})(\.[0-9]{1,2})?`; absolute value at most 999.99, then independent exercise range |
| `humidity_pct` | string | Same decimal grammar/structural bound; independent humidity range lies within 0..100 |
| `source_type` | string | Exactly `SYNTHETIC`; a label, not proof of source or authority |
| `scenario` | string | Same uppercase ID alphabet/first-character rule, 1..20 |
| `seed` | string | Optional minus, no plus or leading zeros except `0`/`-0`; integer magnitude at most 9223372036854775807 |
| `schema_version` | string | Exactly imported `sensor-fault-input-v1` |
| `temperature_unit` | string | Accepted admission requires `degC`, matching independent control |
| `humidity_unit` | string | Accepted admission requires `percent`, matching independent control |
| `calibrated` | string | Shape permits `true` or `false`; admission requires `true` and independently confirmed, in-period calibration |

Numbers are not rounded, clamped or converted. Exponents, NaN/infinity,
whitespace, plus signs and more than two fractional digits are invalid numeric
strings. The seed magnitude check is the current symmetric bound, not the full
signed-64-bit minimum. Structural validity does not establish admission.
Independent trusted exercise policy/control configuration supplies mapping,
monitoring consent, calibration, units, window, clock-skew limits, numeric ranges
and accountable manual-review route. Observations cannot install these controls.
Mapping/calibration/observation intervals are half-open; ranges and skew limits
are inclusive. New observations must be strictly later than retained valid
observations for that sensor. These controls are fictional fixtures, not real
consent, calibration, legal authority or approved operational thresholds.

### Envelope, refusals and stable append

The [existing API callable](../../../src/api/src/zava_forward/api/sensor_ingestion.py)
accepts a materialized list/tuple of 1..100 primitive dictionaries, each at most
20 keys and 4096 bytes under `preflight`'s ASCII JSON serialization. Keys must
be strings of at most 80 characters; values must be primitive
string/integer/float/boolean/null, with integer magnitude at most 2^63-1.
Nested values, oversized envelopes and invalid trusted `received_at` UTC seconds
are refused before any writes. This envelope bound is not the closed observation
schema or a wire-message-size/billing limit. A primitive row with missing or
extra fields, wrong types or wrong version/source instead yields owned per-row
DQ under the independently installed controls.

Current row rejection codes are `SCHEMA`, `IDENTITY`, `PROVENANCE`, `UTC_TIME`,
`NUMBER`, `CALIBRATION`, `UNMAPPED`, `HOME_MISMATCH`, `HOME_UNAVAILABLE`,
`MAPPING_INTERVAL`, `CONSENT`, `WINDOW`, `CLOCK_SKEW`, `UNIT`, `RANGE`,
`OUT_OF_ORDER` and `IDENTITY_CONFLICT`. The first applicable check wins;
these are not diagnoses or automatic property/workflow decisions.
Missing/malformed SQL or controls, malformed retained outcomes and uncertain
commits are explicit bounded errors, not empty success or invented DQ authority.

Append identity is the existing SQL primary key `(sensor_id, reading_id)`.
Retain both IDs and the same observation on retry; this work assigns no new
producer IDs. Delivery reference is SHA-256 of sorted ASCII JSON of the complete
observation using default separators. JSON object key order is immaterial;
changed string values are changed content, even if numerically equivalent.

* An identical accepted replay with a consistent retained witness/reading
  returns the historical `accepted`/`ACCEPTED` receipt with `replay=true`.
  Reading, delivery and DQ counts do not increase. Later control withdrawal or
  clock/window change does not turn reconciliation into fresh admission.
* Changed, structurally valid content under an already accepted key yields
  `IDENTITY_CONFLICT`, never an overwrite. A legacy reading without a consumer
  witness also conflicts. Structurally invalid changed input may fail earlier.
* Identical rejected replay returns the historical rejection and existing Open
  DQ, even after controls are repaired. Malformed/inconsistent retained history
  raises `SENSOR_OUTCOME_MALFORMED`, not a successful replay.

Receipts contain only opaque reference, status, reason and replay flag, not
IDs or raw readings. Restricted DQ metadata contains reason, Open status,
parseable observation time, receipt time, declared accountable role/manual route
and reviewer or `Unassigned`; inspection is in-process only, not an HTTP route.
Closed-shape rejected observations remain restricted in the delivery record;
unknown-field/malformed shapes retain digest/DQ, not arbitrary unknown content.
Transactions are per observation, not whole-batch atomic. Row rejections continue;
database failure or uncertain acknowledgement stops the finite batch.
`BatchStopped.completed` retains the acknowledged prefix; replay the exact
batch to reconcile an uncertain append, never assume that nothing committed.

### Three-per-day accounting, not live packetization

The [addendum baseline](../../case_study_48_addendum.md#sensor-data-capture-analysis-and-map-demonstrator-design)
remains three paired observations per simulated home per day. Declare N as the
number of eligible fictional homes in this accounting scenario, with one paired
observation at each of three daily slots, no missing/rejected observations and
no replays. N=60,000 uses the fictional programme stock scale, not a private stock
extract or evidence of 60,000 devices, configured controls or throughput.

Observation records/day = `3N`; time-averaged records/second = `3N / 86400`.
There are two scalar measures per record, but that does not double the record
count. The mean is not a peak or tested processing rate; synchronized slots could
burst. No scheduler or live cadence is implemented or changed here.

| Declared N homes | Paired observations/home/day | Observation records/day | Mean observation records/second |
| --- | --- | --- | --- |
| 1 | 3 | 3 | 1/28800 = 0.0000347222222222 |
| 60,000 | 3 | 180,000 | 25/12 = 2.08333333333 |

Finite API batches of 1..100 records are callable arguments, not chosen
transport batches or scheduled API calls. Hypothetical wire messages/day equal
`3N` **only if** one observation record is sent per message. No such live choice
is made. For any separately approved grouping into devices/gateways `d`, with
`R_d` daily records and at most `k_d` records/message, perfectly full packing
apart from the last message would give `sum_d ceil(R_d/k_d)` messages/day.
That conditional formula assumes permitted grouping and no additional byte/time
limits, retries or rejections; it is not an adopted design.
IoT Hub billable units, peak throughput, tier capacity and cost require separate
transport/properties/security/packing/retry measurements and current sizing
review. This arithmetic does not establish any of them.

### Measured public synthetic sample and reproduction

On 2026-10-18 the unchanged
[`sensor_consumer_fixture.observations()[0]`](../../../src/core/tests/sensor_consumer_fixture.py)
produced this current-contract example from legacy `sensor_for({"id": "ZF-1"})`
and clean `Packet.rows`, not from a stock Selection. The fixture's two hourly
observations are a small validation input, not a change to the three/day
accounting baseline.

```json
{"calibrated": "true", "home_id": "ZF-1", "humidity_pct": "54.36", "humidity_unit": "percent", "observed_at": "2024-10-01T00:00:00Z", "reading_id": "SENS-SYN-1-1727740800", "scenario": "BACKFILL_2Y", "schema_version": "sensor-fault-input-v1", "seed": "183", "sensor_id": "SENS-SYN-1", "source_type": "SYNTHETIC", "temperature_c": "16.73", "temperature_unit": "degC"}
```

Serialization is exactly the existing `_reference` expression:
`json.dumps(row, sort_keys=True, ensure_ascii=True).encode("utf-8")`, default
separators including spaces, no newline. The serialized example is **366 bytes**,
SHA-256 `efccea5eb698a3310aca7409837ad9b5ad3673b949ddb3c2395da21a8b01dc6c`.
The fenced block's display newline is not measured. This canonical sample for
accounting is not a mandated wire encoding, sample distribution or upper bound.
IDs, seed, scenario and numeric-string lengths vary.

| Declared N | Sample bytes/record | Records/day | Sample-scaled JSON bytes/day |
| --- | --- | --- | --- |
| 1 | 366 | 3 | 1,098 |
| 60,000 | 366 | 180,000 | 65,880,000 |

These are `366 * 3N` illustrative payload bytes, not measured daily traffic.
No 60,000-home dataset was read or generated. Transport envelopes, array/batch
framing, properties, security/TLS, retries, rejected deliveries, SQL storage/
indexes, protocol overhead and billing rounding are excluded. The existing
backfill `estimate()` measures CSV/default-hourly history, not these JSON/day
or wire bytes; its defaults and implementation remain unchanged.

Reproduce from repository root with the `src/core` distribution installed as
described in [source commands](../../../src/README.md#commands). `PYTHONPATH`
below exposes the existing public test helper only, not application source or
`mvp`. No database, private settings or stock files are needed:

```bash
PYTHONPATH=src/core/tests python - <<'PY'
import hashlib
import json
from fractions import Fraction
from sensor_consumer_fixture import observations
from zava_forward.core.sensor_consumer import SensorConsumer, preflight
from zava_forward.core.synthetic.sensor_faults import READING_FIELDS, SCHEMA_VERSION

row = observations()[0]
assert set(row) == set(READING_FIELDS) and len(row) == 13
assert all(type(value) is str for value in row.values())
assert row["schema_version"] == SCHEMA_VERSION
assert preflight([row]) == [row] and SensorConsumer._shape(row) is None
payload = json.dumps(row, sort_keys=True, ensure_ascii=True).encode("utf-8")
assert hashlib.sha256(payload).hexdigest() == SensorConsumer._reference(row)
print(payload.decode("utf-8"))
print("bytes_per_sample:", len(payload))
print("sha256:", hashlib.sha256(payload).hexdigest())
for homes, expected_records, expected_rate in (
    (1, 3, Fraction(1, 28800)),
    (60000, 180000, Fraction(25, 12)),
):
    records = 3 * homes
    rate = Fraction(records, 86400)
    assert records == expected_records and rate == expected_rate
    print(homes, records, rate, records * len(payload))
PY
```

This focused verifier intentionally checks current private implementation seams
without creating a public schema API. Drift in required shape/version/validation
fails explicitly; byte output must be compared with the dated sample above.
Existing [core semantic tests](../../../src/core/tests/test_sensor_consumer.py)
and [API tests](../../../src/api/tests/test_sensor_ingestion.py) exercise actual
SQLite append/reopen/replay/conflict and schema/unit/time refusal. This is local
engineering evidence only. No runtime, application image or UI changes occur.

### Explicit producer compatibility gap and remaining gates

[`sensor_stock.Selection.sensors`](../../../src/core/src/zava_forward/core/synthetic/sensor_stock.py)
constructs `sensor_id = "SENS-SYN-" + sha256(home_id.encode()).hexdigest()`:
9 prefix characters plus 64 lowercase-hex characters = **73**, versus the
consumer's uppercase alphabet and maximum **20**. The existing backfill reading
ID embeds that sensor ID plus timestamp and also exceeds the consumer's 40
character limit. Supporting the stock SQL table's wider columns does not make
these payloads admissible.

No truncation, remap, new producer IDs, validation weakening, consumer fix or
generator rewrite is made. Current fixture-valid records prove the shared
consumer contract **only**, not stock/live interoperability.
[Replay #187](https://github.com/jmservera/ama/issues/187) and
[live/backfill consistency #188](https://github.com/jmservera/ama/issues/188)
need a separately reviewed compatibility decision before using this contract
with stock-derived/live inputs. This is not a waiver of their acceptance.

[ADR 0003](../../adrs/0003-journey-derived-capabilities-runtime-fit.md#status)
was already owner-accepted on 2026-10-15 with Basic IoT Hub sufficient for the
exercise, excluding cloud-to-device messages, twins and device management.
Its original Proposed paragraph is historical, not approval pending.
Live Hub identities/transport, cost/network/provisioning/credential authority,
actual Azure SQL/registered real AI acceptance, OD-43, privacy/legal and human
gates remain separate. No issue criteria, priorities, review tasks, resident
communications, data approvals or operational rules change.

## Historical backfill stack boundary (2026-10-27, Refs #177)

### Original blocked stack

The five draft child PRs target `feat/sensor-backfill-177`, not main.
They remain unmerged; the parent is coordination/evidence, not an integrated
historical generator. Existing synthetic stock and its opaque home IDs are
preserved. No private stock extract, household records or device data were
read. No original issue acceptance checkbox or deferral is asserted.

| Child | Draft PR and bounded delivery | Still unproved |
| --- | --- | --- |
| #178 | [#481](https://github.com/jmservera/ama/pull/481): existing source/terms decision and owner blocker | Exact paired source reuse and approved two-year records; [#425](https://github.com/jmservera/ama/pull/425) remains separate and open |
| #179 | [#482](https://github.com/jmservera/ama/pull/482): typed/versioned legacy indoor equation, explicit exercise domain and provenance | Historical record-derived physical bounds and integrated new models |
| #180 | [#483](https://github.com/jmservera/ama/pull/483): explicit per-home dated exercise fabric-loss effects | Actual source completion-date mapping and writer integration |
| #181 | [#484](https://github.com/jmservera/ama/pull/484): seeded neutral household condition fixtures and monitoring exclusions | Full indoor/writer integration and any real monitoring authority |
| #183 | [#485](https://github.com/jmservera/ama/pull/485): exact consumer incompatibility and conditional size estimate | Owner-selected identity compatibility path and reuse of actual #110 admission |

A public synthetic stock observation was passed to the actual consumer's
`_shape` verifier on 2026-10-27. It returned `IDENTITY` while the public valid
control passed. Sensor/reading/home lengths were 73/84/23 against 20/40/12,
also subject to the uppercase alphabet. This reproduces the existing
compatibility gap above; no IDs were shortened, source controls invented or
validation bypassed. The legacy loader is not the #110 consumer.

Conditional capacity arithmetic at three paired observations/day for 730
days and 60,000 fictional homes is 131,400,000 nominal records. Existing
`sensor_backfill.estimate(homes=60000, days=730, cadence=480)` sampled 20
legacy scale-fixture homes: estimated 131,025,000 rows after dropout,
121.0 bytes/CSV row and 14.77 GiB. This was an estimate only, before any
generation; it is not the private stock's measured storage, a size bound,
SQL/index/transport cost or evidence of consumer compatibility.

The source/reuse and identity decisions block final historical acceptance.
The owner's synthetic fallback permits exercise components, not invented
outdoor records, completion dates, calibrated physics or resident judgements.
Focused child tests and the parent's documentation-scoped gate have different
boundaries; neither proves an unmerged aggregate. Owner integration and a
subsequent aggregate candidate assessment remain necessary.

### Owner-approved integration continuation (2026-10-27)

The later explicit owner decisions under `owner-approvals-2026-10-27-b`
approve existing candidate climate reuse for synthetic demonstration, adopt
existing stock home IDs as canonical keys, and authorize child integration and
aggregate validation. This prospectively supersedes the source/identity owner
blockers above, not their original findings or Residual work Review.

The integrated code now includes all five child branches. The
[pinned paired source metadata](./climate-paired-source-178/open-meteo-era5-durham-2023-2024-metadata.json)
records a genuine 2023-2024 Open-Meteo ERA5 Durham-grid acquisition on
2026-10-27: 17,544 UTC hourly pairs; input SHA-256
`af76a90414d9ad8f19dacc95a38f06d4c4321a91bdf030ba231558c42506051e`;
record-derived temperature -5.3 to 26.9 C and RH 36 to 100%.
The NASA 2023 [sensitivity evidence](./climate-paired-source-178/nasa-power-merra2-durham-2023-sensitivity.json)
is retained separately, not used to invent a second year. Attribution and
historical terms remain explicit; owner approval is not underlying legal or
production terms verification. Source #425 is not silently merged or rewritten.

Canonical home keys are preserved exactly, including case/Unicode. Compact
11-character, collision-checked sensor keys preserve the existing 20-character
consumer limit including `UNMAPPED-`; malformed, absent or unsupported identities
still fail. Export supports the stock 128-UTF-16-unit domain, while actual
consumer availability remains limited to existing exact cases and 64 units on
both stores. No shared case identity migration, alias, truncation or created
availability is implied. Actual consumer tests retain consent, calibration,
mapping, unit, clock, ordering and replay failures.

The [core composition and loading contract](../../../src/core/README.md#approved-paired-climate-composition-2026-10-27-refs-177)
wires versioned indoor projection, explicit dated synthetic measures and neutral
household conditions. Legacy default reading bytes remain unchanged. Output is
synthetic, with optional evaluator-only fault truth separate from analysis.
The verified replay loader calls actual #110 admission; the old legacy loader
is not promoted into an equivalent contract.

Aggregate evidence is recorded in the dated continuation changes/Review and
PR #486. Core discovery passed 1,427 tests (186 existing skips); targeted
static/type checks passed. The full-stock exercise uses an explicitly generated
public 60,000-home fixture, a complete 730-day window and a declared daily cadence,
with hourly capacity estimated before generation. The run passed every-row and
every-ID reconciliation: 43,800,000 rows, 730 per home, UTC 2023-01-02 through
2025-01-01 exclusive; 703,111,263 compressed reading bytes. The uncompressed
reading SHA-256 is
`d07715c8b55fc4e0b6d771472f6f823110fe7b39ed47eab370ef7daf4d98bc41`.
Six thousand explicitly generated synthetic dated measures were supplied, not
inferred from private history. Actual owned-loopback SQL sensor/API tests also
passed all 45 cases, including canonical keys and independent controls.
No exact unread-private-register equality or full-hourly/diurnal-scale
validation is asserted. The original independent Review executed Complete /
Not accepted at its original boundary: Medium RV-001 identified a
composed-loader pre-replay budget check trusting unverified manifest counts.
The original Review and the subsequent ancestry-blocked gate at1b3f623f are
preserved, not reclassified or repeated.

The later 2026-10-27 standing owner authorization selects implementation of
RV-001, current-main integration and one new scoped gate before publication.
Current main2e031c89 is integrated by a normal merge retaining child ancestry.
The loader now requires manifest homes to equal the supplied stock's actual
granted count, then budgets actual nominal rows and stock metadata before
temporary scratch or output. Tests assert pre-write refusal for under/over-
reported counts and accurate oversized replay, metadata-budget refusal even
with zero granted homes, valid zero-row replay and exact-budget normal loading.
Existing fault, byte-comparison and independent consumer safeguards remain.
The new gate, independent exact-head publication assessment and hosted checks
are separate prerequisites; no second full Review, full-stock rerun, private-
register equality, production or human approval is inferred.

### Indoor record-derived envelope correction (2026-10-27, #179)

The later #179 correction replaces the fixed exercise 8 C floor and 15..98%
RH clips in both projection paths. This supersedes the earlier current-value
claim that legacy default reading bytes are unchanged, not the original
stack's findings, tests, Review outcome or recorded aggregate hashes.
Versions `indoor-projection-exercise-v2` and
`indoor-projection-composed-exercise-v2` retain the noiseless equations and
two-draw RNG order but cap each Gaussian residual at three standard deviations.
The cap, scales, schedules, model coefficients and supported input domains
remain explicitly exercise assumptions.

For each retained outdoor temperature/RH pair and dwelling model, calculate
noiseless indoor temperature `B` and vapour `V`. Temperature bounds are
`[B-0.9,B+0.9]` C; RH bounds are
`[100*V/sat(B+0.9)-4.5,100*V/sat(B-0.9)+4.5]`, with each endpoint limited
to the physical 0..100% RH domain. The [core model documentation](../../../src/core/README.md#register-backed-sensor-history-177)
defines inputs, equations, tail policy, provenance, rounding and nominal/fault
boundaries. No independent fixed indoor floor/clip is substituted.

The [projection regression suite](../../../src/core/tests/test_indoor_projection.py)
checks actual hash-pinned public 2023-2024 ERA5 pairs through legacy and
composed generator paths: all 17,544 hourly pairs for apartments and detached
dwellings, with independently reconstructed equations, household conditions
and an explicit synthetic dated retrofit. It also checks supported-domain
endpoints, forced tails, saturation, weather/fabric sensitivity and exact
equation/RNG behaviour. These are engineering checks of an exercise model,
not observed indoor data or empirical physical calibration.

| #179 criterion | Re-evaluation and evidence boundary |
| --- | --- |
| 1. Inputs, equations and parameters documented and versioned | Supported by both v2 parameter mappings, manifest/model fingerprint binding tests and the core documentation. |
| 2. Every parameter sourced or labelled exercise | All coefficients, factors, schedules, domains and noise/tail parameters are explicitly exercise-valued; physical RH saturation is distinguished. No new parameter source is asserted. |
| 3. Indoor series within plausible bounds derived from outdoor record | Supported at the synthetic exercise boundary by per-pair temperature/vapour-derived envelopes, full retained public hourly-record traversal through both paths and adversarial tests. Not calibrated or validated as a real dwelling model. |

This correction does not establish PRD AC-066 live IoT Hub/SQL/AI acceptance,
AC-067 operational analysis, AC-068 competent method/threshold approval, OD-43,
private-stock equality or whole-parent #177 acceptance. Existing monitoring
choice, manual/safety and human approval boundaries are unchanged.

## Sensor privacy engineering boundary (2026-10-17, Refs #112)

The source audit at upstream `74617981b71bc3f10bd21d0b78691bc3cf36c473`
found an offline synthetic generator/SQL loader, not an implemented IoT consumer,
`sensor_analysis` read model or registered sensor AI purpose. The ADR's proposed
deterministic analysis is not current executable delivery. No new health
indicator, threshold or sensor-model permission is introduced by this change.

The [core admission/export contract](../../../src/core/README.md#sensor-admission-and-external-context-112)
now requires exact current-generator manifest and payload replay before schema
or register writes. Source labels, pseudonymized identifiers, filenames,
recalculated hashes and human-approval-looking strings alone confer no admission.
Stock mode needs the independently supplied original synthetic Selection; it
does not reconstruct authorization from candidate snapshot files. Replay proves
generated observations, not stock-anchor truth, genuine consent or lawful use.
The unresolved historic external origins recorded under #175 remain unverified.

Chat uses a closed home-field projection instead of recursively exposing the
whole home. Malformed structured values in selected chat, legacy AI/citation and
map fields explicitly refuse; unknown diagnostic fields are not authorized
context. Stored/manual case detail is unchanged. Points and clusters still have
no sensor fields; third-party tile URLs remain static deployment configuration,
not observation-bearing URLs. Existing map licensing and manual routes remain.
Loader receipts contain counts, not observations or device identifiers.

The one original Review found two structured-data escapes through already
stringified status and late document-name validation (Not accepted). Correction
ONE validates raw status contributors before external export and document
metadata/citation inputs before dispatch and reading-route audit interpolation.
Actual chat/briefing and document provider/transport/audit refusal regressions
failed first and pass after correction. The adverse original Review is retained;
these correction checks do not constitute a second independent acceptance.

This is a bounded structured-data control, not semantic DLP for arbitrary
human-entered prose, a universal PII guarantee, legal approval or complete FR-048
delivery. No new retention authority, DPO grant, resident consent or deployment
is inferred. OD-43 inventory/mapping/calibration, lawful basis/DPIA, resident
choice, retention, freshness/gaps, analysis windows/thresholds and operational
review ownership remain prerequisites for real use. The named authorized human
approval evidence remains unverified, so no real-data activation is implemented.

## Questions

* Which derived measures are meaningful from air temperature and relative
  humidity alone, and which need surface temperature or outdoor conditions?
* How should dew point be derived, with what formula, valid range and error,
  and what margin to a surface temperature indicates condensation or mould
  risk?
* What persistence rule (duration, repeat count, time of day) separates a
  transient peak from a sustained risk, and how much data is sufficient?
* Which trends are worth surfacing to a human reviewer: sustained high
  humidity, small gap between air temperature and dew point, repeated
  overnight peaks, slow drift after a retrofit measure, or divergence from
  comparable homes?
* How do sensor accuracy, placement, calibration, clock drift and missing data
  change the confidence of each signal?
* How can the result be explained to a resident, a housing officer and a
  retrofit assessor without implying a diagnosis?

## Leads and verification status

| Lead | What to confirm | Status (2026-10-14) |
| --- | --- | --- |
| Dew point from air temperature and relative humidity by the Magnus approximation, with commonly cited constants for temperatures above 0 C | Constants, validity range and error against a psychrometric reference; behaviour at low temperature | Partly verified: constants and range confirmed through Lawrence (2005); the original paper's own error figure was not retrieved |
| Surface condensation when a surface is at or below the dew point; mould risk when surface relative humidity is sustained near 80 percent | Whether 80 percent and any margin to dew point are stated in current UK guidance; the averaging period | Partly verified: the 80 percent and 70 percent air figures are in BS 5250:2011 text via a mirror only; not found in current gov.uk damp and mould guidance |
| Temperature factor (fRsi) compares internal surface temperature with internal and external air temperature, with commonly cited dwelling thresholds near 0.75 | Definition, thresholds and when it applies; needs surface and outdoor temperature, which the demonstration does not capture | Verified in the BS 5250:2011 text via a mirror and two secondary sources; BRE IP 1/06 original not retrieved |
| Persistence and trend rules reduce false alerts | Window lengths, minimum valid samples and seasonal effects | Verified at practitioner level (LOTI 2025); no peer-reviewed study found |
| Occupancy behaviour, ventilation and heating drive indoor humidity | How to separate behaviour, building fabric and weather without blaming residents | Verified for the no-blame principle (Housing Ombudsman); behaviour separation method still open |

The web synthesis claimed that PAS 2035 mandates ongoing monitoring of air and
surface conditions. This is an overstatement. A secondary source states that
PAS 2035 requires a risk-based monitoring and evaluation strategy, with sensor
monitoring at intermediate levels, not for every retrofit. Do not cite a
blanket sensor mandate; the official PAS 2035 text is paywalled and was not
read.

## Phases

| Phase | Work | Output | Gate |
| --- | --- | --- | --- |
| R1 Source review | Locate and cite primary sources for each lead; record source date, retrieval date and classification (guidance, technical standard, research) | Cited evidence table in this file | Each retained lead has a primary source; unverified leads are dropped or labelled |
| R2 Method options | Specify candidate derived measures (dew point, dew point margin, sustained-high-humidity duration, overnight peak count, post-measure drift) with inputs, formula, data sufficiency and failure modes | Versioned method specification; no numeric threshold asserted without a source | Competent building-physics reviewer and Asset sign off the method as a candidate |
| R3 Synthetic validation | Generate labelled fictional scenarios (normal, condensation-prone, sensor fault, missing data, seasonal shift) and test each method for detection, false alerts and sufficiency handling | Scenario pack, confusion summary and sensitivity notes, kept separate from real data | Methods meet agreed false-alert and miss limits on synthetic data; limits are labelled exercise values |
| R4 Explainability and review | Draft the reviewer view, resident-safe wording and non-AI comparator; check accessibility and no-diagnosis wording | Review-ready explanation set | DPO, Resident Engagement and Safety review wording; no diagnosis or blame |
| R5 Real-data readiness | Confirm inventory, mapping, calibration, lawful basis, retention and thresholds with owners | Updated OD-43 disposition | Named owners approve before any non-synthetic use |

## Constraints

* Derived signals only create a human condition-review task. They never
  diagnose a hazard, start a statutory clock, override a resident report,
  release a hold or change investment ranking directly (BRD FR-048, RULE-014).
* The deterministic method is primary. Any AI-assisted trend discovery is
  exploratory, runs on synthetic or approved data only, is compared against the
  deterministic result, and needs its own purpose, field access and evaluation
  (PRD CON-009 still applies to delivered builds).
* Missing, stale or invalid data is `INSUFFICIENT`, never normal, and never
  lowers a home's priority or service.
* Residents may decline monitoring without penalty.
* Cite source and retrieval dates for every regulatory or standards claim, and
  record newer retrievals in the regulatory register rather than editing
  snapshots.

## Exit criteria

* A cited evidence table, a versioned method specification and a synthetic
  scenario result exist.
* Every threshold is either sourced or labelled as an exercise value.
* The owner has accepted, rejected or deferred each candidate measure.

## Evidence record

| Date | Action | Result |
| --- | --- | --- |
| 2026-10-14 | Plan created from an uncited web synthesis and Microsoft Learn IoT Hub results | Leads listed |
| 2026-10-14 | Source check by the research agent against public pages (below) | Leads partly verified; official BSI, BRE and AMS texts not read; R1 stays open; R2 to R5 not started |

## Source verification (2026-10-14)

All sources were retrieved on 2026-10-14. Quotes are short extracts reported by
the checking agent and were not independently re-read by the author.
Status values: Verified, Partly or Not found.

| # | Lead | Status | Source | Caveat |
| --- | --- | --- | --- | --- |
| 1 | Magnus dew point, a = 17.625, b = 243.04 C, range about -40 to +50 C | Verified (constants and range); Partly (stated error) | Lawrence, M.G. (2005), Bulletin of the American Meteorological Society 86(2), 225-233, as cited on Wikipedia "Dew point"; Alduchov and Eskridge (1996) title confirmed only through an abstract mirror | The publisher page was blocked, so the original paper's error figure was not read |
| 2 | Mould risk when surface relative humidity exceeds 80 percent; room air above 70 percent likely to give surface above 80 percent | Verified in BS 5250:2011 text; provenance Partly | BS 5250:2011 text via a third-party mirror, not BSI; BSI product page not accessible | Not found in current gov.uk "Understanding and addressing the health risks of damp and mould" guidance, which gives no numeric threshold. Confirm against the official standard |
| 3 | fRsi not less than 0.75 sufficient to avoid mould growth; see BS EN ISO 13788 and BRE IP 1/06 | Verified | BS 5250:2011 text via the same mirror; thermalbridgecalcs.com and specifierreview.com corroborate | BRE IP 1/06 original was not reachable. fRsi needs surface and outdoor temperature, not captured in the demonstration |
| 4 | PAS 2035 mandates ongoing monitoring | Partly: overstated | RISE Retrofit "Monitoring and Evaluation" toolkit, riseretrofit.org.uk (secondary guidance) | Accurate wording: PAS 2035 requires a risk-based monitoring and evaluation strategy that may include sensor data. BSI's PAS 2035 page is paywalled and was not read |
| 5 | Persistence and trend rules reduce false alerts | Verified (practitioner) | London Office of Technology and Innovation, "IoT Sensors for Damp and Mould Project: Winter Follow-Up", loti.london, 2025 | Practitioner report, not peer reviewed; no BRE or university study located |
| 6 | Avoid blaming residents for damp and mould | Verified | Housing Ombudsman Service, "Housing Ombudsman urges zero tolerance approach on damp and mould", 2021-10-26 (Spotlight report "Damp and mould: It's not lifestyle") | None significant |
| 7 | Azure IoT Hub tiers, routing, provisioning and authentication | Verified | learn.microsoft.com: iot-hub/iot-hub-scaling, iot-hub/iot-hub-devguide-messages-d2c, iot-dps/about-iot-dps, iot-hub/authenticate-authorize-azure-ad | Pages carry no fixed date. Basic tier is device-to-cloud only; standard adds cloud-to-device messaging, twins and IoT Edge. Message routing is available on both tiers. Devices authenticate with symmetric keys or X.509, not Entra ID; managed identity applies to service-side access |

Consequences for the design: use the 80 percent and fRsi figures only as
candidate exercise values labelled with the BS 5250:2011 source until the
official text is confirmed, and keep the analysis review-only.

## arXiv search (2026-10-14)

Searched the arXiv API (export.arxiv.org) on 2026-10-14 for dew point and
humidity formulas, mould and damp in housing, condensation risk in dwellings,
hygrothermal mould models, retrofit and social-housing indoor monitoring,
occupant behaviour, and the Magnus formula. No result addressed these topics,
so arXiv does not validate leads 1 to 6 above; the BS 5250, fRsi, PAS 2035 and
mould-risk questions need standards, BRE and building-physics journal sources.

Only generic sensor-method papers were relevant. They were read as abstracts
only and support method design (phase R2), not any threshold or standard:

| arXiv ID | Date | Title | Possible use |
| --- | --- | --- | --- |
| [1805.11999](https://arxiv.org/abs/1805.11999) | 2018-05-30 | Reference-free Calibration in Sensor Networks | Calibration of dense low-cost sensor networks without a reference |
| [2406.17488](https://arxiv.org/abs/2406.17488) | 2024-06-25 | Environmental Variation or Instrumental Drift? A Probabilistic Approach to Gas Sensor Drift Modeling and Evaluation | Separating real change from sensor drift |
| [2112.09072](https://arxiv.org/abs/2112.09072) | 2021-12-14 | Sampling Trade-Offs in Duty-Cycled Systems for Air Quality Low-Cost Sensors | Sampling cadence versus data quality |
| [1411.2188](https://arxiv.org/abs/1411.2188) | 2014-11-09 | Semantic-based Detection of Segment Outliers and Unusual Events for Wireless Sensor Networks | Outlier and unusual-event detection in sensor streams |

Next step for R1: search building-science sources (for example Building and
Environment, Energy and Buildings, BRE, Housing Ombudsman) and obtain the
official BS 5250, BS EN ISO 13788 and PAS 2035 texts through the owner's
licensed access.

## Historical climate evidence (2026-10-17, Refs #178)

This online continuation of merged PR #367 supersedes the all-unknown
comparison as the current evidence position, not the original immutable
source snapshots. All retrievals below actually occurred on **2026-10-17
UTC**. This date is not a dataset publication date or owner approval date.
Only official public metadata, terms and one bounded station file were
retrieved; no accounts, paid downloads, terms-acceptance forms or private
datasets were used.

### Candidate comparison

Source IDs resolve to the dated source register below. Coverage describes the
product, not verified coverage at every intended demonstration home.

| Candidate | North East coverage and historical period | Spatial/temporal resolution and variables | Licence, reuse and access | Assessment |
| --- | --- | --- | --- | --- |
| Met Office HadUK-Grid v1.3.2.ceda | UK land coverage includes North East England; release extends through 2025, starts vary by variable. Monthly relative humidity starts 1961 | Observations interpolated to 1km; coarser grids and regional averages also provided. Temperature daily/monthly; RH (`hurs`) monthly/seasonal/annual, not daily | C178-HUK: exact regional release OGL v3, catalogue citation required. CEDA register/login required; actual regional RH download returned login HTML | Recommended **regional monthly context candidate only**, not paired replay bounds or direct station observations |
| Met Office MIDAS Open hourly weather observations | UK station collection begins 1853 to previous full year, but station operation/variables vary. Durham, Northumberland and Tyne-and-Wear directories are listed in v202607; individual station coverage not verified | Station points; hourly weather and separate daily products. Archive lists air temperature, dew point and **calculated** RH; inspect actual fields/flags per station before use | C178-MIDAS: collection explicitly OGL; v202607 README request redirected to login. Exact release acknowledgement and North East station/QC packet not retrieved | Best cadence-oriented next investigation for three-per-day history; no records or station recommendation claimed |
| Met Office historic station data, Durham | Retrieved Durham 1880-01 through provisional 2026-09; 54.768 N, -1.585 E, 102m elevation. A single site, not a region-wide sample | Monthly averages of daily maximum/minimum temperature, frost, rain, sunshine. **No RH**. No adjustment for small site/instrument changes | C178-DUR/C178-TERMS: public file linked by official station page; website content OGL v3 grant and attribution, with exclusions and separate automated-copy restriction requiring review | Retrieved temperature-only cross-check; not a replacement paired source and no more automated Met Office retrieval planned |
| Copernicus ERA5 single levels | Global coverage includes North East; 1940 onwards | Hourly reanalysis on 0.25-degree lat/lon grid (ensemble uncertainty 0.5 degree); model/observation assimilation, not station measurements. No RH calculation or record extraction performed here | C178-ERA: current exact catalogue declares **CC-BY-4.0**, not assumed OGL. Standard CDS route requires account/PAT and manual dataset terms agreement | Spatially complete alternative, but access/derived-variable/method work remains; no account or agreement made |
| CIBSE 2025 weather files v1.1 | 28 UK climate zones; historical input baseline 1994-2023, morphed TRY/DSY files and 2030s/2050s/2080s projections. Exact North East zone not selected | Hourly dry-bulb/dew-point temperature and RH over design/reference years, not an unmodified chronological observation series | C178-CIBSE: prepayment before download, user licences including additional institutional users. Exact redistribution/derived-output permission not retrieved; **not established as open reuse** | Excluded from this no-purchase observed-history delivery; design-year extrema would answer a different question |
| Met Office UKCP18, owner lead | UK/global observations and climate projections through 2100 are distinct products | Projection models at 60km global, 12km UK and downscaled 2.2km; family is not one observational dataset | C178-UKCP: family page is not proof of a particular file's licence or historical suitability | Refine the lead explicitly to the HadUK observational context product below, not projections used as measured history |
| Environment Agency, owner lead | Examined England flood-monitoring API, not every EA collection | Documented water level/flow and rainfall; levels/flows usually 15-minute measurements with variable transfer frequency. No temperature/RH pair documented in this API | C178-EA: explicit OGL v3, no registration, specific acknowledgement below | This identified API does not answer the weather-pair need. No conclusion that all EA products lack climate variables; another exact dataset would need evidence |

The generic Met Office HadUK variable page still lists daily temperature from
1960. The current release-specific CEDA history says daily temperature was
extended to 1931 in v1.3.1 and daily mean temperature added in v1.3.2.
Use the release-specific catalogue rather than silently repeating the older
generic start date. Neither change supplies daily humidity.

### Conditional recommendation and current source register

Recommend **HadUK-Grid Climate Observations by Administrative Regions over
the UK, v1.3.2.ceda (1836-2025)**, UUID
`386b3c1ee2054ef5ae0d73060963a9f1`, as the candidate for regional monthly
historical context. Its observational basis, UKCP18-compatible geography,
explicit RH field and dataset-specific OGL v3/citation make it more
defensible for that limited purpose than a generic UKCP18/EA name, ERA5
reanalysis or purchased design years. This is an explicit refinement of the
owner's UKCP18 lead, not approval of a silent replacement.

The 1km HadUK release (`789b3065d74a4c948ab05d33556c86d0`) is a distinct
grid alternative, not the regional product's citation or tested download.
No region index, cell or station has been adopted for replay. **No candidate
currently qualifies as an adopted paired historical replay source.** Regional
monthly context cannot establish three-per-day extrema. MIDAS is the next
cadence-oriented lead if an authorized station/QC packet becomes available.
The existing labelled `synthetic-uk-seasonal-model-v1` remains unchanged.

All rows were checked on 2026-10-17. These are dataset metadata, provider
terms and access evidence, not a legal opinion or operational rule.

| ID / official source | Version/date and retained evidence | Reuse / attribution / current limitation |
| --- | --- | --- |
| C178-HUK: [regional release catalogue](https://catalogue.ceda.ac.uk/uuid/386b3c1ee2054ef5ae0d73060963a9f1/), [1km alternative](https://catalogue.ceda.ac.uk/uuid/789b3065d74a4c948ab05d33556c86d0/), [variables](https://www.metoffice.gov.uk/research/climate/maps-and-data/data/haduk-grid/datasets) | v1.3.2.ceda, published 2026-06-23; regional DOI `10.5285/386b3c1ee2054ef5ae0d73060963a9f1`. Metadata and licence retrieved, **records not retrieved** | Regional catalogue explicitly links OGL v3 and requires its dataset citation. Registration/login is separately required |
| C178-HUK-ACCESS: [actual regional RH request](https://dap.ceda.ac.uk/badc/ukmo-hadobs/data/insitu/MOHC/HadOBS/HadUK-Grid/v1.3.2.ceda/region/hurs/mon/v20260512/hurs_hadukgrid_uk_region_mon_196101-202512.nc?download=1) | URL identifies monthly 1961-01 to 2025-12 file, version directory v20260512. Followed request returned HTTP 200 `text/html` at `accounts.ceda.ac.uk`, **not NetCDF** | Precise blocker: authenticated CEDA access, confirmed by catalogue access rules and [token guidance](https://help.ceda.ac.uk/article/5100-archive-access-tokens). No login, token or registration attempted; do not mistake a 200 login page for data |
| C178-MIDAS: [collection](https://catalogue.ceda.ac.uk/uuid/dbd451271eb04662beade68da43546e1/), [guide](https://help.ceda.ac.uk/article/4982-midas-open-user-guide), [v202607 hourly archive](https://data.ceda.ac.uk/badc/ukmo-midas-open/data/uk-hourly-weather-obs/dataset-version-202607) | Current directory v202607 listed; [release README request](https://dap.ceda.ac.uk/badc/ukmo-midas-open/data/uk-hourly-weather-obs/dataset-version-202607/00README_catalogue_and_licence.txt) ended at login HTML | Collection OGL verified, exact release citation/acknowledgement and station records not retrieved. `qc-version-1` means latest record state, not proof every field passed QC. Ignore the guide's stale 2020 availability FAQ |
| C178-DUR: [historic stations](https://www.metoffice.gov.uk/research/climate/maps-and-data/historic-station-data), [Durham record file](https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/durhamdata.txt) | Actual 92,268-byte file retrieved 2026-10-17; SHA-256 `d2c9ff2a443b8502957ce88fe8bfdbbd0d5ac111208eab0842bc574d4d4306f9`. Full input retained outside repository during analysis; only derived report published | Website-content terms below apply unless separately excluded; no station-specific alternative notice found in file. No RH. Retained hash does not guarantee the rolling URL will later serve identical bytes |
| C178-TERMS: [Met Office legal](https://www.metoffice.gov.uk/policies/legal), [website terms](https://www.metoffice.gov.uk/policies/tandc), [OGL v3](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/) | Terms retrieved 2026-10-17; no asserted publication/revision date for undated pages. Website content grant is free OGL v3 with stated exclusions | Attribution adjacent to reproduced licensed content: "Contains public sector information licensed under the Open Government Licence v3.0". OGL allows copying/adaptation/commercial reuse with attribution, exclusions and no endorsement/warranty. Website terms also restrict automated monitoring/copying except authorized APIs; **no further Met Office fetches after discovering this clause**. Owner must review access/reuse compatibility before repeat retrieval or adoption; no blanket automation permission inferred |
| C178-ERA: [exact ERA5 catalogue](https://cds.climate.copernicus.eu/api/catalogue/v1/collections/reanalysis-era5-single-levels), [CDS access instructions](https://cds.climate.copernicus.eu/how-to-api), [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | DOI `10.24381/cds.adbb2d47`; catalogue updated 2026-10-17, declares `CC-BY-4.0` | Credit source, link licence and indicate changes; no endorsement/additional restrictions. CDS instructions require manual dataset terms agreement and account/PAT before the standard retrieval route. No record job submitted or terms accepted |
| C178-CIBSE: [current weather product page and FAQs](https://www.cibse.org/knowledge-research/weather-data/) | 2025 release v1.1; source states baseline, variables, zone count, purchase and user-licence route | Prepayment and MyCIBSE download; exact redistribution terms not retrieved. Purchase, institutional access and a user licence must not be assumed to permit redistribution. No files ordered/downloaded |
| C178-UKCP: [UKCP18 overview](https://www.metoffice.gov.uk/research/approach/collaboration/ukcp) | Family remains provider-recommended/validated while UKCI is introduced; not a release identifier for this task | No family-wide licence or observation-bound claim made; use C178-HUK's exact terms for the recommended product |
| C178-EA: [flood-monitoring API reference](https://environment.data.gov.uk/flood-monitoring/doc/reference) | Public API metadata/docs, not a downloaded weather dataset | OGL v3; provider acknowledgement: "this uses Environment Agency flood and river level data from the real-time data API (Beta)". No weather-pair bounds derived |

Required regional HadUK citation, from that exact catalogue:
Met Office; Hollis, D.; Carlisle, E.; Kendon, M.; Packman, S.; Doherty, A.
(2026): HadUK-Grid Climate Observations by Administrative Regions over the
UK, v1.3.2.ceda (1836-2025). NERC EDS Centre for Environmental Data
Analysis, 23 June 2026. doi:10.5285/386b3c1ee2054ef5ae0d73060963a9f1.
Retain this citation and the [OGL v3 link](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/)
with any later authorized derived asset. Citation here is provenance,
not owner approval.

**Owner licence/reuse approval: UNMET**, including for Durham derived evidence
and the recommended HadUK product. Juan Manuel Servera remains the named
exercise reviewer. Public availability, a licence grant, retrieval permission
and an agent's recommendation do not record his approval, sign a new agreement
or authorize operational reuse.

### Retrieved temperature evidence and reproduction

The [derived JSON report](./climate-source-evidence-178.json) records the
actual Durham input hash, retrieval date, statistic definitions, source
line/month for every tied extremum, quality counts and explicit unavailable
humidity. It contains derived numbers, not a bundled provider dataset.
Attribution for the Met Office-derived statistics: Contains public sector
information licensed under the [Open Government Licence v3.0](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).
No endorsement is implied.

Selected window: **1991-01 through 2020-12**, a declared 30-year comparison
window, not a claim that this sample captures all North East weather.
All 360 calendar months are present. Nine estimated `*` values in each
temperature field are excluded, leaving **351 accepted same-month pairs**;
zero missing/provisional values within this window. There are 1,401
out-of-window rows. Calendar completeness is not 100 percent usable coverage.
Provisional rows, then missing tokens, then estimated values are mutually
exclusive rejection categories per field; no filling or clipping.

| Statistic (degC) | Minimum and month | Maximum and month | Accepted count |
| --- | --- | --- | --- |
| Monthly average of daily maximum temperature (`tmax`) | 2.7, 2010-12 | 24.2, 2006-07 | 351 |
| Monthly average of daily minimum temperature (`tmin`) | -3.4, 2010-12 | 12.8, 2003-07 / 2013-07 / 2019-07 | 351 |
| Arithmetic monthly midpoint `(tmax+tmin)/2`, not a separately retrieved mean field | -0.35, 2010-12 | 18.3, 2006-07 | 351 pairs |

These are sample extrema of **monthly statistics**, not instantaneous/daily
extremes, physical limits, a joint temperature/RH envelope or generator
parameters. RH is **unavailable and not inferred**. One inland station and
selected quality-filtered years do not establish coastal/upland or region-wide
bounds. No historical humidity value or synthetic parameter is introduced.

From repository root, using the already retained local input, the
[offline helper](../../../tools/climate_station_bounds.py) reproduces the report:

```bash
python3 tools/climate_station_bounds.py /path/to/retained/durhamdata.txt \
  --source-url https://www.metoffice.gov.uk/pub/data/weather/uk/climate/stationdata/durhamdata.txt \
  --retrieved-on 2026-10-17 --start-year 1991 --end-year 2020 \
  --expected-sha256 d2c9ff2a443b8502957ce88fe8bfdbbd0d5ac111208eab0842bc574d4d4306f9
python3 -m unittest discover -s tools -p 'test_climate_station_bounds.py' -v
```

The helper never downloads, accepts terms or changes data. It fails explicitly
on hash/schema/unit/date/duplicate/malformed-value errors; an entirely excluded
series reports unavailable/null extrema, not default bounds. Report SHA-256:
`f75566fc1bf62608a78cf7f12647779dab12f0d0cddf86f6f1a7083df6f95615`.
The rolling original file is not bundled and cannot be reconstructed from this
hash. Reproduction after this session requires the exact retained bytes or an
owner-authorized matching packet; a later changed download is a new retrieval,
not this evidence. Review website access conditions before any new retrieval.

### Current issue #178 criterion audit

| Original criterion | Progress on 2026-10-17 | Remaining acceptance boundary |
| --- | --- | --- |
| Compare coverage, resolution, licence and reuse | Substantive official-source comparison delivered for all issue candidates plus both owner leads | CIBSE exact redistribution terms, MIDAS release acknowledgement and exact North East station/zone coverage remain explicit gaps; no blanket complete terms verification claimed |
| Record chosen source, retrieval date and licence; keep licence open until owner confirms | Exact regional HadUK candidate, metadata/terms retrieval date, OGL v3 and required citation recorded | Conditional context recommendation, not an adopted paired replay source. Data retrieval blocked at CEDA login. **Owner reuse approval UNMET** |
| Derive outdoor temperature and humidity bounds from records | Actual Durham monthly temperature statistics derived, quality-filtered and reproducible | **Unmet as a paired criterion**: no humidity records, no instantaneous/three-per-day or region-wide envelope. Requires authorized paired records and competent method/geographic review |

Leave original issue checkboxes unchanged and #178 open. No sensor-method,
live-platform, legal or operational acceptance follows. The next human actions
are dataset-specific reuse/access review and, if authorized, provision of the
exact paired source/station/QC packet; not invention of missing bounds.

## Paired historical climate access check (2026-10-21, Refs #178)

A bounded continuation tested whether official paired North-East temperature
and humidity records can be retrieved without an account. Retrievals occurred
on 2026-10-21 UTC (not a publication or approval date). Evidence:
[access-blocker record](./climate-paired-source-blocker-178.json).

* MIDAS Open (OGL stated on its CEDA catalogue page) exposes anonymous
  directory listings, including North-East stations, but every file fetched
  (data licence README, station metadata, station capability) required a CEDA
  login. Account creation or credential use is outside this task, so no
  hourly temperature or relative humidity records were obtained.
* Environment Agency Hydrology (OGL 3) carries no humidity or dew-point
  property; its temperature measures are not atmospheric paired data.
* No bounds, thresholds or replay limits are derived. The Durham monthly
  temperature statistics remain temperature-only, and no synthetic value
  stands in for observed records. Synthetic data stays permitted only when
  clearly labelled synthetic and cannot fulfil record-derived bounds.
* Owner action: an authorised human with their own CEDA account supplies
  selected MIDAS qc-version-1 files and licence text and records reuse and
  station approval, or the owner approves another public no-login source.
  Source selection and licence/reuse remain UNMET. #179 stays sequenced behind
  grounded paired input.

## Historical outdoor climate source decision (2026-10-16, Refs #178)

Historical offline audit, retained for provenance. For the current evidence
position use the [2026-10-17 update](#historical-climate-evidence-2026-10-17-refs-178)
above; the unknowns below describe the earlier audit only.

This is an offline evidence audit, not a completed historical-source study.
The issue and its owner comment were read on 2026-10-16; that is a GitHub
decision-evidence date, not a climate-data or licence retrieval date. No
external climate records or licence pages were retrieved for this audit.
The existing generator and tests explicitly state that climate records have
not been retrieved. No outdoor temperature or humidity figure is introduced
here.

### Owner direction and current selection

The [owner's issue comment](https://github.com/jmservera/ama/issues/178)
dated 2026-10-15 directs use of Met Office (UKCP18) and Environment Agency
open data under the Open Government Licence (OGL) where available, otherwise
clearly labelled synthetic data, with retrieval dates and licence recorded
per dataset. This is source direction, not dataset-specific reuse confirmation.

The selected current fallback remains
`synthetic-uk-seasonal-model-v1`, as declared by
[`sensor_backfill.py`](../../../src/core/src/zava_forward/core/synthetic/sensor_backfill.py).
It is constructed demonstration data, not historical North East England
weather, and has no external climate retrieval date. The owner-directed
external source family is recorded, but no historical product, station,
grid cell, release or observation period is selected as verified.

UKCP18 is the owner's named lead. Before selecting any product from that
family, establish whether the particular files contain historical
observations, historical model output or future projections; neither a
projection nor a generic provider name proves historical observation bounds.
HadUK-Grid and MIDAS Open remain candidates, not silent substitutions for
the owner's direction. A different product choice must be explicit.

### Candidate comparison and verification gaps

The candidate names in #178 were explicitly unverified. The table compares
their outstanding suitability questions, not verified product properties.
`Unverified` means no supporting dataset metadata, records or terms are held
in this audit; it does not mean unavailable from the provider. No candidate
passes the historical temperature-and-humidity evidence gate yet.

| Candidate | North East coverage and historical period | Resolution and required variables | Licence and reuse evidence | Current disposition |
| --- | --- | --- | --- | --- |
| Met Office HadUK-Grid, via CEDA | Unverified; identify cells and period covering the intended North East locations | Unverified; confirm spatial/temporal resolution and both outdoor temperature and relative humidity fields | Unverified; obtain the exact release's terms, attribution and redistribution conditions; do not assume OGL | Issue-named candidate; no records retrieved |
| Met Office MIDAS Open station data, via CEDA | Unverified; identify station IDs, locations, elevations, period and missingness | Unverified; confirm observation cadence, temperature and relative humidity availability and quality flags | Unverified; confirm the selected collection/version's access and reuse terms and attribution | Issue-named candidate; no records retrieved |
| Met Office historic station data | Unverified; identify a representative station and actual record period | Unverified; confirm whether the published variables and cadence support both required bounds rather than temperature alone | Unverified; retain the selected station file's applicable terms and attribution | Issue-named candidate; no records retrieved |
| Copernicus ERA5 reanalysis | Unverified; identify cells, product, version and period | Unverified; distinguish modelled fields from observations; establish whether relative humidity is supplied or must be derived from other fields with a cited method | Unverified; confirm product-specific licence, acknowledgement and redistribution terms | Issue-named alternative; no records retrieved |
| CIBSE weather files | Unverified; identify location, vintage and whether the file represents actual history or a constructed design year | Unverified; confirm cadence and both variables, and whether design-year extrema are suitable for historical bounds | Unverified; check access, purchase, permitted use and redistribution terms before obtaining or sharing files | Issue-named alternative; no records retrieved or purchase authorized |
| Met Office UKCP18 | Unverified; resolve the owner's lead to an exact historical product and period, if suitable | Unverified; distinguish observations, model output and projections; confirm both variables, units and resolution | Unverified; establish dataset-specific OGL applicability or other terms rather than generalizing from the owner comment | Owner-directed lead; no verified historical dataset selected |
| Environment Agency open data | Unverified; no collection or station has been identified | Unverified; first establish whether a collection supplies both required climate variables at relevant locations/cadence | Unverified; confirm the exact dataset's licence and attribution even where described as open data | Owner-directed lead; not yet an identified climate dataset |

### Retrieval, provenance and reuse register

| Field | Recorded state on 2026-10-16 |
| --- | --- |
| Current generator source | Labelled synthetic seasonal model; unchanged |
| Verified historical dataset and release | None selected |
| Climate record retrieval date | Not retrieved; no date to record |
| Licence evidence retrieval date | Not retrieved; no date to record |
| Dataset licence, version and terms | Unknown; OGL only where dataset-specific evidence establishes applicability |
| Attribution | Not yet verified; retain the provider's exact required acknowledgement with the eventual dataset citation |
| Source URLs, station/cell IDs, observation period and input hashes | No retrieved dataset packet held; must be recorded before deriving historical bounds |
| Reuse confirmation | Open; Juan Manuel Servera is the synthetic-exercise Legal, Compliance and DPO owner, not an inferred operational approver |
| Observed outdoor temperature and humidity bounds | Not derived; no retrieved records available |

An open-data label, access permission, or owner source preference does not
itself establish the terms for redistributing records or derived assets.
Agents may retrieve when authorized, compare, summarise and flag terms;
legal interpretation and reuse confirmation stay with the named human owner.
Real owners and sources remain a gap before operational reliance, consistent
with [ADR 0005's synthetic-only acceptance](../../adrs/0005-regulatory-compliance-assistant.md#owner-decision-acceptance-and-authority-2026-10-16).
No consent, safety decision, operational rule, purchase or financial
commitment follows from this source register.

### Evidence packet and bounds derivation gate

To resume offline, supply a locally retained evidence packet; alternatively
obtain separate authorization for external climate retrieval. The packet
must identify the provider, exact product/release and stable source URLs;
dataset and terms retrieval dates; applicable licence text/version or
reference and required attribution; raw file hashes; station IDs or grid
coordinates and elevation where supplied; historical period, timezone,
cadence, variable definitions, units, quality flags and missing-value codes.
Record any download query, extraction and conversion so the analysis can be
reproduced. Do not redistribute protected records before reuse review.

Derive bounds from the retained records, not from the generator's parameters:

1. Establish the selected locations and observation window from metadata and
   preserve the raw inputs. Identify observation versus modelled data; do not
   silently pool products, stations, periods or resolutions.
2. Parse timestamps and units using the source definitions. Count total,
   missing, duplicate, quality-rejected and valid values per variable,
   location and period. Retain rejection reasons; do not silently fill gaps.
   If humidity must be derived, cite and version that method and its inputs.
3. Calculate the minimum and maximum of the retained valid temperature and
   relative humidity records. Report the extrema with their source row/time,
   sample counts, window and input hashes. Report paired-sample coverage if
   temperature and humidity support a joint model. An empty required variable
   is insufficient evidence, never a default bound.
4. Retain the analysis command/code version and output hash. Review seasonal
   and location coverage and limitations before using the results to justify
   any synthetic range. One station or a short period cannot establish
   region-wide extremes. Observed sample extrema are not physical limits,
   a forecast, indoor thresholds or safety rules.
5. Obtain the owner's dataset-specific reuse confirmation and any required
   competent method review before adopting changed generator/test limits.
   Keep derived historical evidence separate from synthetic scenario
   parameters and injected faults; do not clip observations to make an
   exercise test pass.

The existing
[`OUTDOOR_EXERCISE` expectations](../../../src/core/tests/test_sensor_plausibility.py)
remain selected exercise values. Their tests establish internal synthetic
plausibility, not historical climate validity. Neither they nor this audit
satisfy the broader PRD AC-066 to AC-068 IoT, method or live-platform gates.

### Issue #178 acceptance audit

| Acceptance criterion | Status | Evidence and missing work |
| --- | --- | --- |
| Candidate sources compared on coverage, resolution, licence and reuse terms | Unmet; offline comparison framework only | All issue-named candidates and owner leads are listed above, but the dataset properties and terms remain unverified. Retrieve and compare primary metadata and applicable terms |
| Chosen source, retrieval date and licence recorded; licence stays open until the owner confirms reuse | Unmet; fallback/source direction recorded only | Synthetic fallback and owner direction are explicit; no verified historical source, retrieval date or licence evidence exists. Dataset-specific reuse confirmation remains open |
| Outdoor temperature and humidity bounds derived from retrieved records, not typed in | Unmet; blocked on records | Existing bounds are exercise values. No historical observations or calculated extrema are available; execute and retain the derivation above once records are supplied |

All three issue checkboxes remain unchanged. This audit is a bounded
documentation contribution, not completion of #178 or approval for real use.

## Public document check (owner-supplied, 2026-10-14)

Two public documents on BS 5250:2021 were supplied by the owner.

| Document | Result |
| --- | --- |
| BMI Group, "BS 5250:2021 Management of moisture in buildings: a guide to the updated British Standard and the changes to pitched and flat roofing", issued August 2021 (PDF on assets.ctfassets.net) | Retrieved and text-extracted. A manufacturer's roofing guide, not the standard. It confirms that a 2021 edition of BS 5250 exists and defines condensation as deposition when air temperature drops to or below the dew point. It lists BS EN ISO 13788 (internal surface temperature to avoid critical surface humidity and interstitial condensation) as a calculation method. It does not state the 80 percent surface humidity figure, the 70 percent room air figure or an fRsi threshold, and says nothing about sensor monitoring |
| Scribd, "BS5250 2021 New Guidance on Managing Moisture Risk in Buildings" | Not read. The page returned an access challenge to an automated request, and the full document needs a signed-in browser session. It may be a copy of protected material and its provenance is unknown, so it is not used as a source until the owner confirms the right to use it |

Effects on the leads:

* The thresholds checked earlier come from the 2011 edition of BS 5250. A 2021
  edition now exists, so each figure (80 percent surface humidity, fRsi 0.75)
  must be confirmed against the 2021 edition and BS EN ISO 13788 before use.
  Until then they stay labelled candidate exercise values from the 2011 text.
* The dew point definition of condensation is supported by the BMI guide only
  as a general definition; it does not validate the Magnus constants.
* Nothing in these documents changes the PAS 2035 finding.
