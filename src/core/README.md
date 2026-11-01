---
title: Zava Forward core library
description: Domain, store, ledger, law store, chat storage and synthetic-data documentation for the core project, split from the former mvp README in M6 of #199
author: AMA programme
ms.date: 2026-10-31
ms.topic: reference
---

## AI consumption ledger (#432)

`ai_consumption.Consumption` extends the existing immutable `assistant_events`
stream and serializable assistant transaction, without a second database or DDL.
The dedicated `ai-consumption` partition contains closed, versioned metadata:
opaque root/attempt/output references, capability/case class, configuration and
prompt fingerprints, model, input/output/cached tokens, retries, failures and
owned workflow-only alerts. It does not copy historical proposal text into the
consumption stream. Historical calls and the separate resident SQL accounting
remain explicitly unjoined.

An operator can supply `price(...)`, `authorize(...)` and `billing(...)` evidence
through this Python interface on a constructed/local or separately authorised
store. These methods do not retrieve prices, grant spend, verify an invoice,
appoint an owner or approve a quality floor. There is no new HTTP write endpoint
or automatic authority. `price` requires an official source URL, source SHA-256,
retrieval/version/effective period, model/currency and exact rates per million
input/output/cached tokens. The [public-source snapshot](../../docs/reference/resources/azure-ai-price-source-2026-10-31.json)
has unavailable numerical rates; it is not an applicable price table.

`authorize` binds an immutable operator evidence/owner reference, price and exact
`Ai.configuration(deployment, temperature, max_tokens)` fingerprint. Supply both
period and task budget IDs with finite calls/tokens/decimal currency amounts,
UTC start/end and maximum request calls/depth. A reused budget ID keeps all
previous liability; overlapping configuration authorities and changed limits
are rejected, including unresolved/cross-currency reuse at authority, price and
admission boundaries. Default authority is absent. Named live owners and OD-51 approval
are still missing; the unassigned-owner reference is a gap, not an appointment.

Reservations commit before physical dispatch, with expiry checked again after
credential acquisition and immediately before the network. This also rechecks
all intersecting budgets for intervening unknown/held liabilities. Synthetic prices
cannot admit production transport; only an explicit HTTP loopback fake provider
is nonbillable test transport. Root calls and depth (starting at
one) share durable bounds; duplicate attempts cannot dispatch again. Complete
serialized ASCII text request bytes bound input tokens conservatively. Images
have unknown liability and are not dispatched, while file storage/manual work
continues. Pending calls retain the upper bound; unresolved calls after 40 seconds,
unknown cached usage, malformed usage or actual overruns stop subsequent
budget dispatch. Explicit cached zero differs from absent cached usage.
There is no automatic timeout refund or hold-clearing operation.
Financial completion survives proposal fencing/quarantine independently.
Returned-model mismatches retain a closed `model-mismatch` outcome and at most
512 characters of model evidence through worker serialization. Oversized or
non-string names become null, not provider-unavailable; completion quarantines
the task without retry, suspends its release and withholds provider output.
Financial usage remains recorded, with uncertain liability held.
An already-revoked release stays revoked; mismatch quarantine is still saved.

A call admitted at 9,999 events can reach 10,001 on reservation/completion.
Publication-only `DispatchHeld` handling retains saved legacy/priority drafts
but shows and returns the manual fallback with explicit unresolved
`financial_attribution` and Unknown cost. Chat saves the same workflow-only
fallback it returns: SQL finalizes the actual message and financial join in
one transaction; JSON uses the actual saved message and persists its fallback.
No redispatch occurs. Subsequent dispatch remains held, and missing output
joins keep reporting incomplete/Unknown after read recovery. Other financial
link or persistence errors still propagate; strict `output()` remains unchanged.
Assistant completion also stages financial publication before serializing its
task/event: a hold saves unresolved attribution and withholds actionable output
without rolling back quarantine, release safety state or token settlement.

`report(start=..., end=..., as_of=...)` uses UTC `[start,end)` call cohorts and
review state as of the cutoff. All attempts, including retries/failures, belong
to the numerator; only eligible, human accept/edit-accept output records count
once. Verification, templates, chat replies and rejected/quarantined outputs
are not accepted proposals. Legacy output/review saves and financial links are
not cross-store atomic: pending review intents commit before domain review
saves, and an interrupted financial link leaves `unjoined_reviews` nonzero and
prohibits a money ratio. A matching authoritative review can retry its pending
link without reapplying content edits. Missing output links block accept/edit,
not rejection: legacy drafts retain an opaque original-root association and
human disposition, with incomplete output/review joins until the matching
original output link is repaired. Assistant rejection creates an ineligible
link for an unlinked metered task in the same transaction as its disposition;
existing eligibility is never rewritten. Capacity-held or invalid metering
cannot roll back an authorised assistant withdrawal: an explicit
`financial_attribution` unresolved flag and immutable withdrawal marker persist.
As-of reports exclude those outputs from acceptance and keep economics Unknown
even after ledger reads recover. Equal-time withdrawal markers take precedence;
repeated reviews or later events do not automatically clear unresolved state.
Events remain immutable, but monotonically ordered
review revisions preserve human acceptance withdrawal and latest/as-of state.

Billing imports need the exact exclusive period, currency, shared budget scope,
source/allocation evidence, complete coverage and an explicit owner tolerance
fraction. Duplicate/overlapping imports fail; immutable corrections need separate
work. Billing is the financial numerator, projected token charge is a separate
diagnostic, and variance is `abs(billed - projected) / billed`. Zero billed
reconciles only with zero projection. No bill, incomplete allocation, uncertain
liability or zero accepted denominator means Unknown, never an estimate.

Optional report inputs for quality use the returned cohort hash and observed
counts/denominators plus upper-bound floors and matched baseline rates for
critical misses, unsupported claims, overrides and reopened cases. Unknown or
unapproved quality never qualifies a cost. A worse rate is Failure even when
cost is lower. Hosting, review, correction, assurance and support are separate
proposed TCA components; missing components leave the total Unknown. Components,
quality and capacity inputs are supplied observations, not verified Finance
approval. Capacity hours are never cash; booked destination evidence is not
implemented or assumed.

Local tests are synthetic ledger and fake-loopback HTTP exercises, not a paid
held-out batch, reconciled Azure invoice, live authority or whole-issue acceptance:

```bash
# From src/core after pip installation:
PYTHONPATH=src:tests python3 -m unittest test_ai_consumption test_ai_consumption_demo -q
# Credential-free synthetic walk-through (Unknown cost, dispatch holds, loop stop, report):
PYTHONPATH=src python3 -m zava_forward.core.ai_consumption_demo
# From src/api:
PYTHONPATH=.:src:tests:../core/src:../agents/src:../core/tests:../agents/tests \
  python3 -m unittest test_ai_consumption_api -q
```

## Dependent-policy RAI release binding (#218, #219)

The stock assistant and retained priority task bind the actual current
deterministic ranking policy content, not just their prompt/output-filter
versions. The quality assistant also binds checklist definitions and ordered
keyword-to-checklist selection. Changing these policies denies new dispatch,
queued claims and proposal reliance under the previous release; in-flight
results are quarantined. Stock evidence explicitly reads the current policy.
Unrelated assistant/task bindings remain unchanged. No ranking or checklist
rule is changed by this control.

Existing dependent releases need renewed evaluation and a fresh authorized
release record; rollback cannot revive a superseded record. No actual release
is renewed automatically. Constructed matching records prove proposal-only
mechanics, not approved evaluation evidence or live OQ-017 authority.

From `src/api`, with editable projects installed, local synthetic regressions:

```bash
PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest \
  test_assistant_release.DependentPolicyRelease \
  test_assistants.HumanReviewMechanics -q
```

The review checks seed plausible wrong, unsupported, incomplete and stale
proposals, retain scripted rejection/correction provenance and preserve case
data. Their automation-bias negative control deliberately demonstrates that a
false source-verification attestation can accept wrong text. Valid citations
and an acceptance click are not semantic truth, reviewer competence or a
controlled domain approval. Actual reviewer detection, corrections and total
preparation/review effort against paired workflow-only scenarios remain
unmeasured; #223 is not satisfied by these tests.

The #222 cohort manifest in open PR #421 still needs owner approval before
evaluator implementation. Cohorts, lawful fields, sample sufficiency and
thresholds remain unapproved, and synthetic results cannot prove fairness.
Actual release/residual-risk/review/restart holders remain unknown under
OQ-017. The [incident](#operator-incidents-and-constructed-restart-221) and
[challenge](#version-bound-affected-person-challenges-220) contracts retain
their separate approval and coverage limits. No child or epic closure,
human-witnessed drill, broader assistant/form challenge coverage, legal
screening or #440 stabilization is inferred.

## Unverified nomination and tenure intake (#130, #131)

The existing `resident_action` ledger accepts `nomination_record`,
`nomination_correct` and `tenure_intake`. These are constructed staff-recorded
intake, not nomination eligibility, verified identity, consent, Legal approval
or an offer. Current registered staff need both resident-workflow and
recorded-reason rights. Owners are named follow-up staff, not appointed Legal
or Home Ownership decision makers. Each successful command is audited with
non-sensitive record identifiers and persisted using the existing transaction.
SQL writers recheck the actor, owner and current case revision before commit.

Nomination keeps the exact supplied original account, source, reported subject
and channel, a staff-recorded acknowledgement reference, named owner,
next-update date and staffed non-digital route. Acknowledgement evidence is
not verified delivery. Digital, phone, letter, in-person and trusted-intermediary
channels are supported as staff capture, not direct resident authentication.
Accounts longer than 4000 characters are refused, never truncated.
Identity, support needs and risk flags remain `Unknown`. Corrections retain
the original and competing accounts/subject references with actor/time and
require re-review; a same-case generic challenge may be linked without
resolving it. No resident identity, authority, ranking, consent or hazard
record changes. Hazard-marked reports are refused with the independent
hazard-intake route; no automatic triage, classification, dispatch or clock
change occurs.

New nomination identifiers use an opaque `NOM-` plus full random UUID, never a
ledger position. Retention deletion and subsequent intake therefore cannot
reuse a deleted record's identity or accept a stale correction for another
subject. Existing sequential identifiers remain valid for retained records.
Corrections must use the recorded identifier and its current version.

Tenure reports retain each supplied household reference, reported tenure and
lease interest, source, unresolved identity state, follow-up owner and update
date. A report is not verified household membership. Verification, decision
route, Legal responsibility and Finance cost remain `Unknown`. Every report
sets a case-wide hold on resident work gates and new measure-scope recording,
including ambiguous/unknown households and otherwise accepted measures.
Revisions and other households' agreements cannot release it. There is no
release or verification action. A static responsibility-question checklist
identifies missing evidence; it is not a pack derived from reviewed leases.
Prior homes without intake are unchanged: this does not prove complete tenure
coverage or an all-offer gate across the programme.

The tenure hold is separate from resident-decision status. An otherwise current
acceptance remains `Accepted` in lists, prompts and priority suggestions after
tenure intake; the hold still blocks case-wide and scoped resident work.
Existing decision retention, scope, human-review and representative-authority
checks continue to apply.

Raw intake is excluded from unrelated-role detail, contractor output,
assistant source allow-lists and case CSV. Sensitive histories follow existing
resident-record deletion handling for constructed tests; the separate
non-sensitive `tenure_review_required` marker survives evidence deletion so
deletion is not approval. No new actual retention duration, applicability,
lawful basis or privacy approval is established.

Operational extensions remain blocked on OD-41/42, real participant and
representative evidence, a named Legal/Home Ownership decision owner,
verified household/lease identity, approved responsibility/cost and applicable
DPO/Compliance retention/release decisions. Nothing is sent, booked or
approved. No issue-wide acceptance or user/accessibility conformance is claimed.
The existing generic RAI challenge remains separate from nomination-specific
eligibility and review decisions.

Focused local constructed tests:

```bash
python3 -m unittest discover -s tests -p test_resident_decisions.py -q
```

## Unapproved working field review (#96, #98, #99)

`form_review.action(store, user, case_id, body)` supports `open`, `review` and
`diagnose` only. It binds a supplied registered schema, never an approved form.
All schemas and source-policy/rule authority remain unapproved. Named staff
must have the existing Finance, resident-record and reason-view rights.

An individual accept/correct/reject changes only that working field and its
append-only review history. Acceptance copies the exact candidate raw text;
typed integer/number/boolean corrections are explicit, retain the raw evidence,
and require a same-case, exact-schema staged candidate as their source anchor.
Corrections without a staged source anchor remain unavailable. Declarations,
signatures, consent and approvals cannot be accepted by this working-review
path. It never writes original sources, authoritative case fields, ranking,
consent, budget, invoice, grant, award, submission or cash states.

`review` requires `draft_id`, `expected_version`, `field_id`, `decision`,
`batch_id`, `candidate_id`, `value` and `reason`, in addition to `action`.
For `accept`, `value` is null. For `correct`, supply a finite scalar value.
For `reject`, batch/candidate/value are null; prior evidence remains in history.
An unknown field, stale version, foreign candidate or extra server-owned key
is refused. JSON supports one Store/writer with in-instance version checks;
SQLite additionally protects independent writers with database rowversions.

`view` and `diagnose` provide field-specific Unknown/Conflict/Fail draft
diagnostics and source-linked diagnostic manifests. Conditions use confirmed,
valid, current values only, combine predicates with OR and compare types
exactly (`true` is not integer `1`). Missing/invalid/stale controlling inputs
produce Unknown unless another predicate is true. Empty or whitespace-only
strings remain recorded corrections but are not confirmed inputs: unconditional
and active conditional requirements still report missing input. Numeric zero
and boolean false remain valid confirmed inputs. Dates must be valid calendar
dates in `YYYY-MM-DD`; numeric checks exclude booleans and non-finite floats.
Units, currency, eligibility and approved calculations remain Not evaluated.
`reviewed_ready` is always false, even if no local structural issue remains.
Manifests retain exact schema/template/rule/input versions, field IDs/values,
source hashes/versions/locators, attachment references and reviewer history.
They are not reviewed application/claim exports or evidence of eligibility.

Source/schema freshness is evaluated on reads/actions, not pushed into a
downstream approval graph. Each report checks an exact source ID, version,
content hash and kind once, reusing its freshness result for shared fields
and staged alternatives only within that report. Source bytes are read/hashed
at most once per distinct document across current fields, history, snapshots
and alternative checks; missing-byte results are also reused locally.
Action preflight shares these reads with its resulting report. Later reports
check afresh; no cross-request cache is retained. A source change marks only its
bound working fields stale; a new schema version affects all fields bound to that schema. Historical
reviews/values and recorded diagnostic snapshots remain intact. This is not
full FR-043/AC-051 rule/calculation/pack-review/approval stale propagation.
Already-clean evidence is required: reads/reviews never scan or save a source.
Missing, pending, quarantined or deleted retained evidence blocks disclosure of
the entire affected draft/history, including recorded diagnostics. On `view`,
availability is isolated per draft: the affected entry contains only `draft_id`,
`status: "Unavailable"` and a fixed recovery `notice`; unrelated available
drafts remain readable. Actions on an affected draft still refuse access.
Availability is checked for current fields, prior/new history evidence and diagnostic
fields/history/attachments even when the schema is stale or a field was
rejected/replaced. Staleness alone does not remove available history.
Unreviewed alternatives count toward Conflict only if their case/schema,
source version/hash/kind/bytes and field source policy allow review; unavailable
or stale alternatives are excluded without changing staged history.
Missing bytes are reported as unavailable evidence; storage-service failures
remain distinct errors, never empty/successful diagnostics.
Recover or rescan through the separate document owner route before retrying.
Ordinary case detail and generic case exports
exclude the private review/decision-hold records.

Opening notes durably records Held decisions for template/source/rule authority
and Board OD-12/15, with owner role, correction path, recorder/time and null
approved inputs/evidence. These are decision-needed records, not approvals.
The diagnostic acceleration signal is `Pause for human decision`, with null
envelope/tolerances and breach assessment Not evaluated. It does not enforce a
programme-wide release or contain live activity. Finance/Board must supply
actual approved investment, liquidity, covenant and downside inputs; no company
figures, approved thresholds or restart authority are invented.

From `src/core`, after pip editable installation:

```bash
PYTHONPATH=tests python3 -m unittest test_form_review test_form_staging -q
```

Tests use the public tiny synthetic fixture with temporary JSON/SQLite storage.
Full #96/#98 approved readiness/export and #99 envelope/breach acceptance remain
blocked on human decisions. No issue closure or production acceptance is implied.

## Resident advisory assistant (#469)

`resident_assistant.advise(topic, CaseProgress(...), provider)` builds bounded
advisory text from the current authenticated resident projection. `Provider`
accepts and returns only a `Topic` enum; `FakeProvider` is deterministic and
network-free. A provider cannot supply answer text or select a different task.
Status reuses the page's plain-language facts; document requests remain unknown,
and form help is generic. All answers include sources, an advisory notice and a
person-help route. No submission, consent or decision authority is added.

The API owns authentication and the disabled real adapter. See the
[design awaiting owner decision](../../docs/architecture/resident-assistant-prototype.md)
for model, credential, USD 5 budget and activation boundaries.

## Finite synthetic stream replay (#184)

`synthetic.sensor_stream.replay(selection, Replay(...))` reuses the existing
seasonal `sensor_backfill.readings` model, forcing its legacy random fault
profile off, then converts to the shared 13-string `sensor-fault-input-v1`
contract. It accepts only explicitly selected synthetic stock records;
declined/unknown monitoring choices produce no device or reading. No installed
device discovery or real dataset is used. Sensor keys are the existing compact,
collision-checked stock keys; one `SYN-<sensor_id>` device maps to one home.

Default cadence is 480 minutes: three paired observations/home/day.
`Replay(seed=183, origin=<UTC whole-second datetime>, days=2,
first_slot=0, end_slot=None)` describes a finite original model window.
The complete original random sequence is generated before selecting the
half-open nominal slot interval, so nonzero and odd suffixes reproduce the
same values/IDs as the existing clean backfill. Do not restart the seed at
handover. The default remains the labelled synthetic seasonal model.
For composed backfill parity, explicitly pass the same `climate=` adapter and
`measures=` tuple to both `replay` and `descriptor` as to the backfill writer.
This reuses its full-origin household and dated retrofit projection; it never
restarts model state at the handover. The climate adapter must supply the complete
original window. Composed descriptors include climate manifest, model parameters
and sorted dated-history hash; these match the composed backfill manifest.
`descriptor(selection, spec)` records the original register `stock_sha256`
separately from `selected_stock_sha256`, the digest of the validated canonical
selected model inputs, plus selected home IDs/count, granted count, seed, origin,
window, cadence, schema/model context and explicit fault mode. Each Frame carries
the selected digest outside its observation, binding that frame to the snapshot
actually used for generation. A later selection mutation changes newly computed
provenance, not old frames; match the descriptor's selected digest to the frames.
Each Frame also carries `nominal_at`, the UTC time from the original origin and
slot cadence, outside the observation. Publishers use this time for scheduling,
not the fault-injected observation timestamp; duplicates retain the same nominal time.
The descriptor version is `synthetic-stream-v2`; reading IDs/bytes are unchanged.
Keep descriptors and selected-home evidence restricted, not ordinary telemetry.

### Synthetic handover consistency (#188)

`synthetic.sensor_consistency.report(observed, reference, handover=...,
cadence_minutes=480)` compares a joint queried window with an independently
generated continuous same-input reference. Both inputs use the canonical
13-field observation contract. Each home has exactly one sensor; every expected
UTC slot, stable reading ID, unit, schema and provenance field must match.
There must be at least two samples on each side per home. Malformed, empty,
duplicate, incomplete or irregular series raise explicit errors, not a pass.
Use explicit SQL observation queries plus trusted persisted control units, not
relabelled incoming units, when constructing the observed input.

The JSON-compatible result includes `passed`, declared tolerances and per-home
before/after counts, channel means and population standard deviations.
`Tolerance(point=0, mean_step=0, stddev=0)` is the default for each of the
`temperature=` and `humidity=` arguments. All limits are inclusive, finite and
nonnegative, in C or RH percentage points. Decimal point comparisons and
cross-multiplied reference-adjusted sums preserve inclusive boundaries; the
mean-step check compares sums against the scaled limit before dividing, so
recurring means cannot reject an exact-limit handover. Division is used only
to report the mean-step error. The standard-deviation check compares exact
rational population variances through a guarded squared inequality, preserving
inclusive limits without subtracting rounded square roots. Standard deviations
and their error remain rounded diagnostic metrics, not acceptance inputs.
Mean-step error subtracts the reference's
expected step, while point and per-side standard-deviation errors prevent
offset/variance cancellation. This detects ingestion discontinuity without
calling legitimate weather or dated works a seam. A numeric failure sets
`passed=False` with individual metric checks; it does not invent replacement
readings or approve sensor accuracy.

The constructed four-day proof uses two granted homes (including a long stock
ID), changing outdoor weather, works at handover, actual CSV bytes and the shared
consumer. It retains twelve readings/home at three/day and replays all 24 after
reopening. See the [API SQL proof](../api/README.md#synthetic-handover-sql-proof-188).
This is model/ingestion parity, not a real-sensor statistical assessment, live
Hub run, actual Azure SQL proof, physical calibration or whole-issue acceptance.

The generator limits actual granted homes to 1..100 and original
homes-times-slots to 100,000 before model generation, independently of summary
metadata. This aligns with the existing finite consumer control batch; it is
not 60,000-device throughput evidence. `wire(frame.row)` uses the shared
consumer's sorted ASCII JSON representation and caps each body at 4096 bytes.

Explicit modes are `valid`, `duplicate`, `out_of_order`, `unmapped`, `wrong_unit`,
`clock_skewed`, `uncalibrated`, `gap`, `disconnect` and `burst`. Frames keep truth
outside the observation. Duplicate emits identical IDs/content; out-of-order
swaps nominal adjacent slots with an odd final singleton unchanged. Selection
always uses nominal slots, not shifted timestamps. Wrong-unit conversion,
one-day clock skew and calibration flags are labelled synthetic exercises,
not science or policy. Gap emits no frames; an empty send run is refused.
The replay descriptor records the omitted window and mode. Disconnect/burst
are runner actions, not extra telemetry fields. A normal device claiming a
mutated unmapped sensor is refused by the API binding before SQL.

`RunBudget` performs finite message/byte/B1 headroom checks before sending.
`Pacer` exposes `paused` and `stopped`, finite speed in (0,1000], a monotonic
deadline and a separate maximum send rate. `wait` applies model-time spacing;
`admit_send` enforces global send-attempt spacing and must be awaited immediately
before the SDK send, after connection/setup and truth preparation. Speed-up and
burst never bypass this admission. Active pacing sleeps until the nearer target,
deadline or 50 ms poll, so rates up to 100/s are not limited by the poll interval.
Pause keeps positive polling bounded by 50 ms and the deadline even after the
target passes. Pause continues consuming the run time allowance, not a way to leave a
simulator running unattended. See the [API runner](../api/README.md#opt-in-iot-consumer-and-synthetic-publisher-110-184)
for actual SDK operation bounds, credential handling and activation gates.

#### Cost estimate and run controls (#189)

`synthetic.run_plan` records a pre-run estimate for N homes before any run:
messages/day (3 per home by default), 4 KiB metered units against the decided
B1/one-unit quota (400,000/day with a 40,000 reserve, less any units already
used that day via `daily_used_units`), prorated hub cost for the provisioned time
(whole days of `max_seconds`, not the simulated replay span) and budget cap, plus the run owner, time limit (at most 3600 s) and budget alert
reference and threshold. It counts the whole run (all days) against the daily
quota and refuses over-quota, over-budget, too-short or over-100,000-message
runs (the `RunBudget` publisher limit; larger stock needs separately budgeted
runs). The plan records a `replay_speed` (default and maximum 1000) that is
passed to the `Pacer`; the replay span (days x 86,400 s / speed) must fit
`max_seconds`. `RunController` starts only against a recorded, untampered estimate whose
complete body matches the current plan, estimate and alert amount, allows one run, stops it, scales homes and rate down (never up) and
inherits the `Pacer` hard deadline. Prices are public list estimates, not a quote.
Nothing here sends traffic or verifies the live Azure budget alert (#146).

```bash
python3 -m zava_forward.core.synthetic.run_plan --homes 30000 --owner "<name>" \
  --budget-usd 10 --alert-reference "<budget alert name>" --out estimate.json
```

From `src/core`, with the package installed:

```bash
python -m unittest discover -s tests -p test_sensor_stream.py -q
```

## Constructed offline sensor consumer (#110)

`sensor_consumer.SensorConsumer` is a finite SQL-only processor, distinct from
the unchanged exact-generator replay loader. The existing API package owns the
[finite callable adapter](../api/README.md#finite-offline-sensor-ingestion-110).
No live Hub client, device identity authentication, thread, public route, analysis,
case task, resident contact or property mutation is added.

Trusted in-process exercise setup calls `configure(ExercisePolicy, [SensorControl])`
with independently constructed mapping, monitoring consent, calibration context,
units, numeric bounds, observation window, maximum past/future skew and accountable
manual-review role/route. Unknown reviewer is `Unassigned`; an unusable route is
refused. These are exercise fixtures, not operating policy, staff delegation,
resident consent evidence or live authority. Observations cannot install controls.
Current SQL controls and mapped-home existence are checked within each database
writer transaction. A payload's home, source label or `calibrated=true` never grants
mapping, consent or calibration authority.

Input is the closed `sensor-fault-input-v1` observation shape from
`synthetic.sensor_faults.READING_FIELDS`, not Packet labels/clean rows/evaluator
truth. The [shared field reference and measured daily accounting](../../docs/reference/research/iot-sensor-analytics-research-plan.md#shared-observation-contract-and-volume-2026-10-18-refs-186)
describe this imported authority without another schema: three paired records/
home/day gives 3N records, not a selected wire-message count. Stock-derived
73-character lowercase-hex sensor IDs are incompatible with this consumer;
fixture-valid records do not prove stock/live interoperability.
All fields are strings; sensor/reading/home IDs are uppercase ASCII
letters/digits/underscore/hyphen, with maximum lengths 20/40/12, no whitespace.
Scenario uses the same alphabet, max 20; seed is a signed 64-bit integer string.
Numbers are decimal strings with at most two fractional places, no exponent,
NaN/infinity or rounding. Bounds are explicit exercise controls. Time is UTC
whole seconds ending `Z`. Mapping, calibration and observation windows are
half-open; numeric and clock-skew bounds are inclusive. Unsupported units or
calibration, declined/unknown consent and timestamp order produce visible DQ.
Out-of-order/equal-time input is rejected, never promoted to latest or "normal".

`sensor_reading` reuses the generator table and composite key. Fresh SQLite and
SQL Server plus supported existing legacy/stock reading shapes are supported;
legacy SQL Server schema_version is widened from 12 to 32 without replacing
rows or keys. Other incompatible shapes are explicitly unsupported. New
restricted SQL tables hold current controls, digest-keyed delivery outcomes
and owned data-quality metadata, not case workflow exceptions. No shared
sqlstore/mssqlstore change is needed.
Closed-schema observations, including rejected quality cases, remain only in
the restricted SQL delivery record so manual reviewers can trace the source.
Malformed/unknown-field input retains only its digest and DQ, not arbitrary
unknown payload content. Metadata inspection never returns the observation body.

Identical witnessed replay returns the historical outcome before new authority/
clock checks, with no new reading, success witness or DQ. This is reconciliation,
not renewed admission after consent withdrawal. Changed content under an accepted
sensor/reading key produces identity conflict without overwrite; legacy rows
without a consumer witness are also explicit conflict. Identical rejected replay
retains its historical DQ even if controls are later repaired.

Accepted replay validates the restricted historical witness digest, closed shape
and retained reading time/numeric/source consistency before acknowledging history.
All retained readings for the target sensor receive timestamp/numeric validation,
and consumer readings must match their accepted witnesses, before deriving the
latest observation for a new admission. No unchecked SQL MAX can hide a
low-sorting corrupt timestamp or skip a duplicate-maximum row. Two sensor-filtered
SQL reads and an in-memory witness index avoid a query per retained row. Returned
data and in-memory validation are linear in that sensor's history; the JSON
witness predicate may scan delivery history. This is finite constructed
processing, not a throughput or production sizing claim.
Legacy generator readings retain their separate witness-free contract.
Malformed persistence raises bounded `SENSOR_OUTCOME_MALFORMED`, not a successful
replay or raw parse failure. These checks do not reapply today's consent,
calibration or window to truthful historical replay.
Validated seed values compare as integers across SQL representations, including
`-0` persisted as BIGINT zero; the original observation and exact-retry digest
remain unchanged.

Receipts expose only opaque reference, status, reason and replay flag. Raw values,
device IDs and keys never enter receipts, diagnostics, AI, maps or ordinary UI.
`inspect_exception(reference)` is restricted in-process metadata inspection,
not an HTTP route: reason, Open status, observed time if parseable, receipt time,
declared exercise accountable role/manual route and reviewer/Unassigned.
The SQL database remains restricted; this callable does not establish deployment
database permissions or human acceptance. JSON is explicitly unsupported.
Missing, inaccessible or malformed SQL/controls is unavailable, never empty success.

Actual constructed tests cover independent connections/store instances, writer
serialization, current control/home rechecks, reopen, accepted/rejected rollback
and postcommit acknowledgement reconciliation. From this directory:

```bash
python -m unittest discover -s tests -p 'test_sensor_consumer.py' -q
python -m unittest discover -s tests -p 'test_sensor_*.py' -q
```

Local SQL Server/image checks are engineering evidence only. Distinct real Hub
identities, live transport, Azure SQL application acceptance, registered real AI
and OD-43 remain unmet.
[ADR 0003](../../docs/adrs/0003-journey-derived-capabilities-runtime-fit.md#status)
was owner-accepted with amendment on 2026-10-15: Basic IoT Hub for the exercise,
without cloud-to-device messages, device twins or device management. That
decision is not live cost, network, provisioning, credential or privacy approval.
Issue 110 cannot be considered
complete from this slice; analysis issue 111 and infrastructure issue 140 remain
separate, with 140 depending on the consumer, not the reverse.

## Appointment agreements and visit evidence (#87)

`appointment_control(user, work_order_id, body)` records explicit offers, separate
resident/staff/current committed-capacity confirmations, bounded appointment-only
representative authority, visit facts and provisional configuration. Each action
requires an event reference; identical retries reconcile the recorded action and
conflicting reuse fails. `appointment_control` in work-order projections derives
Unknown/Offer/Committed on the server; withdrawing an agreed order derives Ended,
with its confirmations retained as history. Historical Booked does not confer agreement.
Direct booking, completion and case advance require the current agreement as well
as existing capacity, works consent, safety and building gates.

Offers bind the actual home, work-order scope, resident scope revisions, contract,
package period, date and visit period. Replacement requires the current offer ID.
Capacity/authority changes invalidate dependent evidence without clearing unrelated
resident decisions or the independently owned resident-update/remedy records.
Create the named #88 resident-update commitment first. Record options, household
constraints, pause/deferral and minimum-necessary provider instructions; provider
projections omit household reasons, confirmation sources and investigations.
Appointment evidence requires both the existing resident-view and recorded-reason
entitlements. Unrelated staff receive the same minimal scheduling fields as
providers, not household reasons, representative sources or closure/investigation
histories. Direct summary reads require an explicit current registered actor;
there is no privileged default.
Bundles need explicit resident agreement and exact-scope competence evidence with
a nonblank textual reference of at most 500 characters.
Nothing schedules or sends anything, and urgent hazard intake remains independent.

Verified resident no-access counts only once per explicitly confirmed visit while
the underlying home case has `closed is False`. Provider/cancel/reschedule/Unknown,
unverified and unconfirmed events never qualify. The versioned exercise threshold
defaults provisionally to 5; count strictly greater than the threshold creates one
owned human investigation, not refusal, withdrawal, sanctions or priority changes.
Changing configuration atomically evaluates already eligible active counts across
affected home cases. It does not require another failed visit, recount events or
reset an existing task. New tasks reference the current rule version and existing
eligible events; inactive cases and consumed pre-closure events cannot create one.
Human checks record confirmation, notice, attendance, adjustments, contact and
circumstances as evidence or explicit Unknown, corrective action and next update.
Preference-breach and abortive facts have independent overlapping cause/owner
counts; their reporting threshold remains Unknown.

`appointment_control` action `close_case` records only a supplied human decision
to close the existing underlying home case (PRD DD-006/AC-033, BRD RULE-006/AC-025,
addendum EXA-014). Current registered manager and contract appointment authority,
exact `case_id`, the staff summary's `case_version` as `expected_case_version`, `confirmed: true`,
unique `event_ref`, decision `source`, `source_version` and human `reason` are
required. Actor/time and the controlled-event history are server-recorded.
Closure atomically sets the existing `closed` field and resets only active
no-access counting; visit/configuration histories, consumed IDs and prior human
investigation remain. Outstanding resident updates, remedies and other decisions
are unchanged. Task disposition, pause, order/appointment completion, remedy
closure, imported closed flags and reopening never reset counts or permit replay.
Existing reopening remains separate. New eligible visits after reopening use the
new count boundary. Recording closure is not technical handover, legal/financial
approval, agent-decided readiness or ratified live closure policy.

SQL writes recheck procurement, case rowversions and current contract authority
inside the writer transaction. Failed pending audit rolls back. A committed change
whose acknowledgement fails raises `AppointmentCommittedError`; reload history
rather than executing another action. Focused synthetic checks extend
`tests/test_quality_procurement.py` and the shared explicit appointment fixture.

## Read-only coordinator populations (#101)

Original Review RV-001 exposed false denial for registered staff whose stored
email uses mixed case. Correction ONE normalizes only the registry lookup key
and retains exact current email/code/role checks. Failing-first JSON/SQLite
direct/HTTP regressions pass. Original Defects found verdict remains unchanged;
separate correction evidence is not independent coordinator acceptance.

`coordinator.read(store, user, query)` composes existing synchronized Store
filtering, queue context, closed map-field validation, Leaflet grid data and
validated progress event readers. It does not change Store/document/provenance
writers, event capture, schemas or the priority policy. Current registered
staff identity/role is checked under the refresh lock; own/all open scopes match
existing case-list access. Counts precede bounded stable-ID record pagination.
Record rows use a closed scalar allowlist; no resident narrative, diagnoses,
raw event actors/references or financial evidence is returned.

* Denominator: current authorized open baseline and current source-filtered
  selection are separate from group/metric drill total.
* Heatmap: recorded area, case building ID or home type by current stage;
  absent data forms an explicit Unknown bucket, not an inferred relationship.
* Stopped work: an existing current-stop blocker or an explicitly paused current
  stage. This does not stop the independent safety service or approve restart.
* Priority: unchanged deterministic policy status/version. Draft means approved
  priority count is null/Unknown, not zero and not AI authority.
* Flow: distinct cases with trusted recorded transitions in inclusive UTC
  boundaries. Entry is `to_stage`, exit is `from_stage`, return/reopen is
  `to_stage` of that event kind. `metric_stage` never overrides the current
  `stage` source filter. Stage/metric rows can overlap, so no additive funnel or
  true conversion is claimed.
* History: progress102 version/order/time/precision validation is reused.
  Ambiguous or contradictory stage streams are unknown, not trusted events.
  Missing initial entry/final exit does not manufacture a clock or invalidate
  an otherwise observed transition. Untrusted audit makes observed counts
  unavailable. Legacy absent history remains unknown; complete coverage is zero.
* Exclusions: source-filter exclusions are current baseline minus selected
  cases. Lifecycle exclusions, true conversion and whole-home closure outcomes
  are unsupported/Unknown, never inferred from consent refusal or closed status.
* Coordinates: missing, nonnumeric/nonfinite and out-of-range values remain in
  denominator/table/drillthrough. Only valid points reach the existing map
  field guard and cluster builder. Map total equals selected record total;
  mapped/missing/viewport counts are explicitly independent.

Pure semantic tests use the public tiny `dataset.DATA` fixture plus explicitly
labelled event mutations, not private generated stock. From `src/core`:

```bash
../../.venv/bin/python -m unittest discover -s tests -p test_coordinator.py -q
```

The [API guide](../api/README.md#coordinator-heatmap-and-lifecycle-funnel-101)
documents actual HTTP/browser/SQL entry points. These checks do not establish
operational authority, complete event capture or independent acceptance.

The shared domain library (`zava_forward.core`): stores (JSON, SQLite, Azure SQL), ledger, law store,
rule cards, governance, continuity, chat storage and isolation, and the synthetic tools. It imports no
workload. The sections below are moved unchanged from the former `mvp/README.md` (ADR 0006, issue #199,
M6); the staff-facing behaviour and configuration are in [api](../api/README.md).

Test paths named `tests/...` are in `src/core/tests/` unless they name another project:
`test_chat_isolation` and `test_continuity` are in `src/api/tests/`. Run the suite from `src/core` with
`python3 -m unittest discover -s tests`. Data fixtures and generated datasets are written to the
per-user `ZF_DATA` folder, never under `src/`.

## Bounded pending-document rescans (#117)

`document_rescan.run(store, limit=100, after=None)` consumes one SQL-only
page of missing/pending non-generated documents through the existing
`_scan_stored` service, using a non-deleting bad-verdict mode. `after` is a
`(case_id, document_id)` tuple and limits must be integer 1..100. See the
[orchestrator command](../orchestrator/README.md#bounded-document-rescan-job-117)
for configuration, explicit synthetic opt-in, counters, exit codes and sweep
continuation. The older unbounded `rescan_pending()` is retained for compatibility,
not used by the bounded job.

Each candidate is rechecked under the current Store lock and touched through
`_case`, so SQL persists scan metadata through the existing optimistic writer.
Concurrent writers cannot overwrite a newer scan or unrelated case change.
Failed attempts preserve the prior pending audit prefix and quarantine failed
success audit before recovery I/O; retries begin a new sweep. An explicit
own-operation witness set immediately after COMMIT distinguishes committed
refresh/acknowledgement failure from a competitor's refreshed snapshot.
Committed failures cannot replay audit at lock exit and report reconciliation,
never rejection. Store construction now closes an opened connection if setup
fails, without replacing the original initialization error.

Only exact clean is available. Scan results must be exact two-string tuples
with a closed `clean|pending|infected|mismatch` verdict. Malformed results
are explicit errors before upload/rescan metadata mutation, not deletion or
availability; no supplied object is coerced or echoed. Valid manual scan
exceptions remain unchanged. Unknown verdicts are errors; pending/Defender
tag outage remains pending. Infected/mismatched worker results retain bytes and
remain unavailable; the job cannot delete, approve retention or release a hold.
Manual scan behavior, existing retention listing/approval, resident safeguards,
sensor exports and progress capture are unchanged. The worker identity
`system:document-rescan` is an audit purpose, not a human delegation.
No retention trigger/period or real scanner approval is introduced.

`tests/test_document_rescan.py` uses fresh synthetic fixtures only. Its
original 17-test suite ran on actual independent loopback SQL Server connections
on 2026-10-17 as well as SQLite. Correction ONE (2026-10-18) ran all 19 current
worker cases plus 11 actual SQL progress/resident recovery guard cases, passing
30/30. It covers persisted pending/bad/clean results,
fairness including all-skipped pages, 100-attempt bound, CAS retry/conflict with
failed recovery, SQL failure after audit INSERT, prior prefix, and immediate/
refresh post-COMMIT failure without duplicate successful transition audit.
Actual command/image receipts are described in the orchestrator guide.
The worker now owns SQL recovery before nested automatic diagnostic logging.
Entire CLI root streams in the conflict/recovery reproduction contain no private
sentinel or traceback, with original conflict, competing winner and audit prefix
preserved. Non-worker recovery behavior remains unchanged. Original Review
Complete / Not accepted and original critique remain unchanged; these targeted
correction results are not independent coordinator acceptance or a new Review.
Operational Defender enablement, hosted cadence/missing-run monitoring and
owner/Legal/DPO authority remain unmet; no production protection is claimed.

## Sensor admission and external context (#112)

`synthetic.sensor_backfill.load_into()` admits only exact current-generator
synthetic snapshots. It requires the generated manifest, supported version/
schema, current generator revision, exact payload set and hashes, and an exact
deterministic replay from the declared seed/window. Unknown, malformed, real,
pseudonymized or merely relabelled/rehash-matched data refuses before the schema
hook or any SQL statement. It loads private temporary replay bytes, never
reopens candidate bytes after verification, and returns only inserted/rejected
counts. No raw reading, identifier, supplied diagnostic or path is included in
admission errors. Database failures remain failures, not admission successes.

Stock mode additionally requires `load_into(conn, path, stock=selection)` with
the original explicitly supplied `sensor_stock.Selection`. A manifest or fabric
CSV cannot confer that source authorization. Constructed readings do not prove
real stock identity/consent; #175's unresolved origins remain unverified.
Default `max_rows=2_000_000` bounds nominal observations, steps and selected homes
before replay; an offline caller can explicitly raise that positive integer
computational budget for a reviewed larger exercise. Replay costs additional
generation time and temporary disk, cleaned on completion/refusal. Older
generator revisions must be explicitly regenerated; retained snapshots are not
overwritten or silently migrated. Opt-in fault inputs remain unsupported by
this legacy unit/calibration-unaware loader.

`export_fields` applies closed selected-field contracts at chat, legacy
AI/citation and map boundaries. Chat does not recursively expose the complete
home dictionary. Unknown nested diagnostics stay out; selected structured/
nonfinite fields explicitly refuse rather than stringify their contents.
Stored/manual detail, access checks and all case/domain state are unchanged.
Map points/clusters carry no sensor fields, and the static tile/manual routes
are unchanged. No new sensor AI task, automatic domain mutation or indicator/
health threshold is authorized. This is not semantic DLP for arbitrary prose.

The original #112 Review was Not accepted for two outbound ordering defects.
Correction ONE validates raw waiting/hazard-owner status contributors before
exporting chat context or assembling briefing facts, without changing manual
status/detail. Selected document metadata and case citations are validated
before model dispatch; the ordinary document-reading route also checks metadata
before scan/audit interpolation. Both original findings have failing-first
regressions. The adverse Review remains retained, not replaced with a second
independent Pass; final acceptance is coordinator-owned.

Run the owned fictional regressions after pip editable installation:

```bash
PYTHONPATH=src/core/tests .venv/bin/python -m unittest \
  test_sensor_privacy test_sensor_backfill test_sensor_stock test_sensor_faults -q
```

`ZF_SENSOR112_MSSQL=1` enables the owned-loopback test using existing `ZF_SQL_*`
settings. It refuses non-loopback hosts, creates/drops only a UUID-named
`zf_sensor112_*` database and tests actual refusal-before-schema, generated
inserts and idempotency. Use only a uniquely named task-owned local container.
These checks do not approve inventory, DPIA/lawful basis, retention, resident
choice, source rights, thresholds or live operation. Real-data activation
remains denied; see the [dated synthesis](../../docs/reference/research/iot-sensor-analytics-research-plan.md#sensor-privacy-engineering-boundary-2026-10-17-refs-112).

## Historical progress evidence and declared forecasts (#102)

`Store.progress_report(user, as_of=..., start=None, view="mine",
filters=None, scenario=None)` is read-only and staff-only, including direct
calls. It reuses the existing current-record cohort filter under the Store
lock, including SQL refresh and manager-only closed views. Cohort membership
is current-source selection, not reconstructed historical membership.
The versioned `progress/v1` report freezes case IDs, filters, baseline/
selected/excluded denominators, inclusive UTC period and approval status.

Exact structured `returns`, `handoff_history` and `quality/*/history`
events supply clocks. Prospective controlled `advance` now appends to the
existing `returns` stream alongside explicit `return` and `reopen` events;
the name of that legacy collection is retained. The only actual forward
writer is final checks to install booked, with its real work-order version.
Return/reopen and every handoff state record registered actor and receiving
owner provenance; metadata-required offer/accept keep their explicit source
version and expected handoff-version checks. Internal `controlled/*` sources
name the writer contract version, not externally verified operational evidence.
Versions, timezone-aware times, exact stages/states and chain consistency are
checked. A consistent pair of advance/return/reopen boundaries yields calendar elapsed
seconds clipped to the selected period. First entry and last exit remain
unknown. Only `Contact paused` and `Resident paused works` classify observed
paused stage intervals. Separate lifecycle decisions are never inferred from
these stages. Handoff receipt is not acceptance; an observed offer-to-terminal
wait and a pending censored wait are distinguished. Repeated reopenings remain
events, not completions.

Handoff lifecycle order is the recorded append/version sequence, not a sort
of timestamps. Legacy `_now()` handoff writers truncated to UTC minutes;
their minute-shaped timestamps represent an interval, not second zero. A
seconds-expanded minute is treated that way only when its matching legacy
state timestamp corroborates the lost precision. Fractional precise timestamps,
backward dates outside that minute, invalid versions, identities and lifecycle
orders still produce contradictions. Affected waits remain null with
`unknown_event_precision` / `unknown_handoff_duration`, not an invented duration.
If the as-of falls inside that minute, the event and dependent later versions
are not asserted to have occurred yet; `unknown_event_as_of` is explicit.
Start-boundary ambiguity is likewise unresolved. Exported `time_precision`
and `latest_possible_at` describe bounds, not reconstructed observations.
The same minute bounds also apply to legacy return/reopen and quality clocks.
Events are returned as independent stage, handoff and per-record quality streams in source order;
no cross-stream chronology is invented. New handoff writes use precise UTC
timestamps through the existing helper. Prospective stage and quality history
boundaries also use microsecond UTC; existing business-date fields are not clocks.
Persisted historical events are never rewritten. A contradictory handoff
lifecycle observed by the as-of makes its waits unknown, including earlier
pairs; an earlier as-of before that contradiction keeps its supported answer.

Each new quality history dictionary records its append `version`, exact
`event_type`, immutable `evidence_version`, checklist/source version, actor and
owner. `accepted_handovers` pairs only actual quality acceptance followed by
handover within the same record/evidence version. It reports historical
acceptance-to-handover elapsed time and, when observed by the as-of, a later
supersession timestamp. Later replacement does not rewrite an earlier answer
or join two evidence versions. Resident-told evidence is not resident
acceptance, whole-home completion or financial closure; the whole-home
`accepted_handover_actuals` denominator remains unknown. Legacy unversioned
quality prefixes, missing provenance and contradictions remain unresolved.
All measured collections, including quality pairs, become null/Untrusted
when audit integrity is false or unknown.

Controlled writers save events with their successful case change. SQL also
commits the existing audit in that transaction; failed writes quarantine
pending success audit before recovery I/O. A failed post-COMMIT refresh is
explicitly committed, not rejected; retry cannot repeat the same transition.
Source-recorded operational failures are audited after rollback with a generic
safe reason, not caller filenames, bytes or transport diagnostics. A document
storage outage records `upload_document_failed` then `upload_document_rejected`
without document metadata or success history. Prior audit prefixes survive;
restoration, failure-audit or orphan cleanup errors retain the original error
with explicit diagnostic notes. A committed outcome never becomes rejection.
`QualityOutcomeError` remains the public alias of the shared committed-outcome
error, preserving the existing API 503 `outcome=committed` response without
changing its handler. JSON atomically replaces the case/event file and rolls
back failed calls using the existing audit-prefix recovery pattern, but its
separate audit file is not cross-file process-crash atomic. No stronger JSON
or external-writer immutability guarantee is claimed.

Narrative `history`, current `stage_since`/`days_in_stage`, closure flags and
prose/naive-time audit entries never establish historical durations or accepted
handover. Missing, malformed, unmappable, contradictory and incomplete history
produces null clocks and unresolved exceptions, not a fabricated zero.
Structured history is reported as partial coverage, not a proof that each event
is ledger-anchored or that no intervening events were omitted. Ledger integrity
is checked separately without rewriting it. Raw actor identities, source
references, reasons, notes, resident data and commercial values are withheld;
safe source locators, metadata status and event versions remain inspectable.

Without a declared scenario the Forecast is unavailable, not a zero projection.
`scenario={"ready": 12}` on a selected denominator of 16 uses the
[addendum's EXA-009](../../docs/case_study_48_addendum.md#numerical-targets-and-attribution):
two independent installation and QA/handover resource pools, capacity two at
each stage, one-week stage duration, four weeks. Central cumulative hypothetical
handovers are `[0, 2, 4, 6]`; capacity one/three and two-week duration
sensitivities are `[0, 1, 2, 3]`, `[0, 3, 6, 9]`, `[0, 0, 0, 2]`.
Optional `capacity`, `duration` and `weeks` are bounded positive integers;
`ready` must be a whole number within the selected denominator.
The declared ready subset is hypothetical, not derived installation readiness.
Held cases never silently enter the scenario. Sensitivity ranges are not
statistical confidence intervals, targets, approved plans, promises or actuals.
Committed resources, dependency releases, source freshness and calibration
remain unverified; no professional approval, consent or finance authority is
created. This baseline does not validate AI or imply no AI elsewhere.

Run the owned fictional tests from the repository root:

```bash
PYTHONPATH=src/core/tests .venv/bin/python -m unittest test_progress_reports -q
PYTHONPATH=src/core/tests .venv/bin/python -m unittest test_progress_event_capture -q
```

See the [API/export contract](../api/README.md#historical-progress-report-and-export-102)
for local HTTP, SQLite and opt-in actual loopback MSSQL consumers.
`ZF_CAPTURE_MSSQL=1` additionally runs actual controlled domain writers against
task-owned loopback SQL Server using `ZF_SQL_*`. The test creates unique
`zf_capture102_*` databases and retains them. Never use a shared/live server.
No private dataset, provider call, operational forecast validation, Azure or
human acceptance follows from these checks.

## Resident commitments and independent remedy clocks (#88)

The existing resident action boundary records staff-mediated fictional commitments,
not messages. `update_record` requires `expected_version` (zero for absent or
unversioned legacy), purpose/linked issue, named `owner` email, timezone-aware
`due_at`, human-selected `basis`, and `status` Outstanding or Proposed.
`safe_contact_ref` is a minimum-necessary reference or Unknown; no contact reasons
or new resident channel are needed. Explicit revisions/reassignments retain old
snapshots and original open date. Handoffs preserve the commitment and can no
longer create an incomplete owner/due pair; create it through the resident route.

Existing service requests retain `status` as response/service-record status,
`status_owner`, `status_at` and `version`. A separate `remedy` retains its own
status, owner identity, status date, original open date, version and history.
Complaint response closure never resolves/closes this remedy or another Defect,
Charge query or Household dispute request. `remedy_update` requires its expected
version, supplied progress/reopening evidence and an explicit next status.
Only Resolved may become Closed; Closed may explicitly reopen to Open.
Optional `owner` explicitly reassigns responsibility and preserves its history.
`service_reopen` affects only a Closed response and requires its current version
and reason. Neither action changes resident choices, work orders, quality,
grant or finance records. Their original clocks stay separate; payment-status
notes additionally retain their own named owner/date/history without paying.

If a response assignee leaves eligible staff, an existing resident-workflow
manager can explicitly use `service_reassign`: request `id`, current integer
`expected_version`, `responsibility` (`service` or `redress`), new named `owner`
email and reason `note`. This changes only that responsibility, not the remedy
owner or status. The response status owner/date changes only for its owning
responsibility: redress when Closed or on the Independent review route, service
otherwise. The same person may hold both responsibilities on a Service request;
matching their email does not make the other responsibility own the status.
Reassigning the non-owning responsibility preserves the captured status owner/date
exactly, including absent legacy provenance. An explicit owning reassignment
records its new owner/date but keeps absent old provenance null in history.
History retains old/new captured
identities, prior status owner/date, named acting manager, reason and event time.
Missing legacy identity/date remains null in that history; it is not reconstructed
from today's registry. A captured departed owner need not remain eligible to
preserve their historical event. New owner and acting manager must be current
inside the writer transaction. Complaint/review assignees remain distinct;
the contested decision recorder cannot become its independent reviewer.
Ordinary update, close and reopen retain their existing authority checks.

Writers/assignees use the existing Resident Liaison Officer, Retrofit Coordinator,
Retrofit Programme Manager and Programme Support Officer roles. Only the current
captured owner or either existing manager may revise/reassign a commitment/remedy.
Creation is by case owner or either manager. Service/redress assignees must be
eligible for this same workflow; independent review remains with its named reviewer.
Registered email/name/code/role/OID, current inputs/state/version and assigned
identities are rechecked in the existing SQL writer transaction, without relying
on a case-sequence change. New event identities retain only these identity fields.
Legacy missing identities are looked up by their recorded email for current
authorization only; captured history is never rebound to a replacement person.

Absent legacy response/remedy provenance projects as Unknown/null, not today's
actor/date. `remedy_confirm` explicitly records current eligible responsibility
and supplied `basis` at expected version zero, leaving even a Closed response
unchanged and original remedy open time unknown. Complete `update_record`
similarly confirms old owner/due pairs while preserving their original snapshot.
No migration fabricates historical completion or evidence.

Resident writes reuse canonical SQL discard and commit markers: failed state/
success audit is quarantined before recovery reads, prior legitimate audit and
original diagnostics survive, and post-COMMIT synchronization reports committed
outcome without audit replay. JSON caught-error restoration covers record and
ledger tail; separate files do not promise abrupt-crash atomicity.
Full PRD AC-063 lease evidence/Legal positions, scope-review policy and age-band
configuration remain outside this bounded issue; no operational authority,
resident communication or full PRD acceptance is inferred.

From the root with pip-installed source packages:

```bash
PYTHONPATH=src/core/tests:src/api:src/api/tests:src/agents/tests \
  .venv/bin/python -m unittest test_resident_decisions.JsonResidentDecisions \
  test_resident_decisions.SqlResidentDecisions test_resident_api -q
```

`ZF_RESIDENT_MSSQL=1` enables `MssqlResidentControls` against an explicitly
task-owned loopback SQL Server configured through `ZF_SQL_*`. Each test creates/
drops only its UUID-named `zf_resident88_*` database. Never use shared/live SQL.
## Consultation records and confirmation holds (#92)

The existing provider package is the contract/call-off reference record.
New records default to `consultation_status: "unknown"`; legacy missing values
are also unknown. `record_consultation` accepts supplied statuses `applies`,
`complete`, `not_applicable` or `unknown`, but stores them in
`consultation_history` as unverified claims, never as effective clearance.
Every record requires a named supplied human decision maker, reason, exact
source case/document/version and expected history version. Clean non-generated
original bytes must match their stored hash. The server records the current
registered manager recorder separately, UTC time, monotonic version, contract
reference/version, scope version and source hash. It does not decide applicability,
interpret leases, certify completion or verify that the supplied adviser has
Legal authority. Stale expected versions return a conflict without a new record.

The current registry has contract-manager delegations and rule-card owner roles,
but no verified contract-consultation Legal capability. ADR 0005's named exercise
Legal owner is scoped to fictional rule-card/source review, not contract approval.
No new role/mapping/designation is added. Effective status therefore remains
unknown for every supplied decision, including complete and not_applicable.
Owner direction on 2026-10-18 limits the hold to consultation-dependent actions
and preserves unrelated service work. Ordinary order issuance, reissue,
correction, positive booking and case advancement do not require consultation
clearance. Their existing contract-action authority, provider/capacity, resident,
hazard, building, appointment, stock, technical and funding controls remain.
No operation becomes consultation-dependent merely because of a label, tenure,
client boolean, source hash or supplied positive status.

Existing building dependencies and holds still block their explicitly affected
case/package instructions, including Unknown status and unknown applicability.
Another package can pass package-aware checks, but final case advancement keeps
its existing case-wide building hold. A different eligible case does not inherit
an explicitly case-scoped hold. These are existing generic dependency controls,
not verified Legal applicability or clearance. `require_consultation_clear`
still refuses unconditionally; no genuine contract let/renew transition or
Legal-clearance path exists. Neither is invented here.

Consultation uses the existing procurement JSON document and SQL writer
validation: current recorder, original procurement snapshot and source-case
rowversion are rechecked in the transaction. No Store/schema changes or approved
fixture backfills are made. Application history is not a legally signed record.
This is **partial #92 acceptance**: supplied statuses and existing scoped dependency
holds are implemented, but a verified named Legal record and a dedicated contract/framework/
call-off let/renew workflow are absent. Neither a draft nor a case advance is
claimed as exact letting/renewal acceptance. Both issue criteria remain partial.

After editable source installation, from the repository root:

```bash
PYTHONPATH=src/core/tests:src/api/tests:src/agents/tests \
  .venv/bin/python -m unittest test_consultation_controls test_procurement_api -q
```

Semantic and procurement, building, hazard, resident and role-matrix regressions
exercise real scoped behavior without consultation-guard bypass mocks. Ordinary
service lifecycle success does not turn effective unknown into Legal clearance.
Main's independent resident/staff/capacity appointment commitments are exercised
through the existing explicit synthetic fixture helper, never patched off.
For a disposable, task-owned local SQL Server only, set existing `ZF_SQL_*`
connection settings and `ZF_TEST_MSSQL=1`, then run
`test_consultation_controls.MssqlConsultation` with
`PYTHONPATH=src/api:src/core/tests:src/api/tests:src/agents/tests`.
Its existing wipe/factory harness resets the configured test database.
Never target shared, Azure or operational data. No legal-currentness claim,
operational approval, real order, private dataset or UI acceptance is established.

## Grant lifecycle and human exercise designation (#95)

The existing `grants` state machine and separate `funding` application object
remain separate from provider `finance` records. Opportunity, Award, Claimable,
Submitted, Accepted/Rejected and Cash received have distinct retained grant
events; application approval/submission/confirmation never creates a grant
award, claim or receipt. This is not full PRD FR-019/042 pack/export acceptance.
The original GBP 40 million is an unverified opportunity, not an evidenced
award, approved budget, claimable amount or cash. There is no built-in promotion
or monetary dashboard aggregate. Each new transition has its own supplied
source and optional amount (required for cash); amounts never carry forward.
Only GBP is supported; an explicit other/malformed currency is refused.

Grant writes and application steps reuse the #94 operation boundary below.
Every writer must match current registered email, staff code, name, role and
optional OID. Grant approvals retain manager role and independent preparer
email/code/OID checks. A role alone no longer permits approval or application
approve/submit/confirm. These actions additionally require a trusted staff
`financial_authority` dictionary containing exactly:

* `kind`: `Synthetic exercise`; `status`: `Active`; `human`: boolean `true`.
* `subject`: exact registered `email`, `code`, `oid` (null when absent).
* `evidence_ref`: supplied nonempty designation reference, not proof of real delegation.
* `effective_from`, `expires_at`: timezone-aware ISO timestamps; current UTC server
  time must satisfy `effective_from <= now < expires_at`.
* `permissions`: nonempty list of exact `{action, case_id, route}` records.
  Actions are `grant:Opportunity`, `grant:Award`, `grant:Claimable`,
  `grant:Submitted`, `grant:Accepted`, `grant:Rejected`, `grant:Cash received`,
  or `application:approve`, `application:submit`, `application:confirm`.
  Grant route matches the exact scheme; application route matches its recorded
  route. Unknown routes and wildcards do not confer authority.

Authority comes only from the existing staff registry, never request data.
No app endpoint creates a designation, no existing staff is backfilled, and
`ZF_ENV=production` refuses exercise authority. Proposed or real delegation
labels are not supported substitutes. Actual delegation verification and
operational use remain unimplemented, not inferred from an exercise role.
SQL rechecks current registry, the full time predicate, exact designation
snapshot and independence inside the existing writer transaction, even if
case sequence has not changed.

New grant history retains case/scheme/GBP/source, preparer/approver identities,
server dates and the designation snapshot. Source status remains `Supplied,
unverified`. Old completed history stays untouched. Old pending proposals
without explicit GBP must be withdrawn and re-proposed; do not fabricate
currency or verification. Legacy preparers use the #94 registered-email lookup,
refusing unknown identity and repeating current lookup inside the SQL writer
transaction; captured historical identities remain distinct. The #95 independent
Review found a regression in that distinction (RV-001, original Not accepted).
Correction ONE restores it with failing-first grant/finance code/OID rebinding
regressions. Coordinator final independent closure remains pending; local tests
do not replace that gate. Application approve/submit/confirm each requires
its own evidence reference and appends action/time/case/route/identity/authority
history while preserving compatible status/reference fields. Existing callers
must now supply that evidence; confirmation is not award or receipt.

From the repository root after pip editable source installation:

```bash
PYTHONPATH=src/core/tests:src/api/tests:src/agents/tests .venv/bin/python -m unittest \
  test_grant_lifecycle_controls.JsonGrantChecks \
  test_grant_lifecycle_controls.SqlGrantChecks test_grant_lifecycle_api -q
```

`ZF_GRANT_MSSQL=1` enables `MssqlGrantChecks` against an explicitly disposable
local SQL Server configured through the existing `ZF_SQL_*` variables. Each test
creates/drops only its UUID-named `zf_grant95_*` database. Do not point it at
Azure or a shared dataset. JSON caught-error rollback is retained, not a promise
of cross-file abrupt-crash atomicity. No grant submission, payment, banking or
real commitment is executed.

## Per-measure quality and handover controls (#91)

The existing quality workflow remains Submitted -> Accepted or Returned ->
Fixed, awaiting reinspection -> independent acceptance -> resident handover.
Staff record provider submissions as evidence only. Contractors still have
no quality, defect-closure or finance write capability; no quality step
executes payment or changes finance, grant or funding records.

Every quality write resolves current registered named staff. SQLite and the
inherited SQL Server path repeat that identity check inside the existing writer
transaction. Accepting staff need the existing Quality Inspector/manager role,
but a fixture role is not evidence of professional competence or delegation.
Independence excludes the original recorder/submitter and every retained fixer,
including aliases sharing a populated name, email, staff code or OID.
Legacy recorder identities are resolved from retained names/codes, including
every earlier FIXED-history recorder; unresolved contributors block acceptance
for quality-owner review. Known independent staff can still accept legacy
repeated-remediation records; earlier recorders and their aliases cannot.

A correction needs a nonempty description of remediation and its photo,
document or inspection reference. It remains evidence, not acceptance.
Reinspection only applies to Fixed records; legacy Fixed records without that
evidence cannot pass. The existing workflow requires independent acceptance
for all returned work; this change invents no risk classifications or policy.
Existing safety and explicit measure/resident-scope checks remain in force.

Submitting replacement evidence through the existing method retires every
Accepted/Handed over record for that same measure, including multiple legacy
handovers. The old records become `Superseded`, link to the replacement index,
retain original checklist evidence, history, defects and aftercare, and move
their former acceptance/handover into `prior_acceptance`. They are no longer
actionable. Replacement has an incrementing `evidence_version`, lists its
`supersedes` indices, requires an explicit current resident scope revision,
and needs fresh independent acceptance and fresh resident handover. Other
measures and financial history are unchanged. In-progress duplicate evidence
remains refused. This implements the retained
[ADR 0002 replacement learning](../../docs/adrs/0002-pilot-readiness-architecture.md).

The proposal-only quality assistant uses the same active-record selector:
Superseded evidence is excluded from captured sources, per-measure checks and
current-contributor review. It does not pick an arbitrary newest record;
multiple active versions remain a discrepancy. Missing/unknown measures,
pending/returned/fixed work and incomplete/conflicting current checklist evidence
remain gaps. Current `evidence_version` is included in the scalar allowlist and
source signature, so same-content replacement invalidates old proposals.
Historical-only edits cannot make retired evidence current. Assistant proposal
verification/acceptance is still separate from quality acceptance, handover or
professional approval; no assistant gains domain-write authority.

Failed SQL writes use the existing decision-scope quarantine/rowversion
mechanisms; failed success audit cannot flush later, while a caller's legitimate
pending audit prefix survives a pre-commit refusal. After confirmed COMMIT, a refresh failure
instead raises `QualityOutcomeError` with explicit committed/reload guidance;
an already committed prefix is never requeued. The original read failure remains
the exception cause and is logged. Tests cover actual case/audit writes followed
by pre-commit failure, early/persistent recovery-read failure, committed refresh
failure, exactly-once audit, original errors, reopen and stale writers.
JSON restores caught state/audit failures, including failures
after an actual file write. Failed restoration explicitly reports an unknown
durable outcome; separate JSON/ledger files are not abrupt-crash atomic.

With editable src packages installed, from the repository root:

```bash
PYTHONPATH=src/api:src/core/tests:src/api/tests:src/agents/tests \
  .venv/bin/python -m unittest test_quality_procurement \
  test_role_matrix.QualityMatrix test_resident_decisions -q
```

The existing `test_mssqlstore.MssqlProcurement` inherits the canonical SQL
quality/provider tests once. With `ZF_TEST_MSSQL=1` and `ZF_SQL_*` pointing only
at an explicitly disposable local SQL Server/database, it replays those tests.
It wipes test tables: never point it at a private or existing application
database. The final 2026-10-17 run passed 38 actual local SQL Server tests in a unique
loopback-only disposable container, removed afterwards. Local evidence does not
establish Azure SQL acceptance, real professional approval or full PRD adoption.

## Record-only finance controls (#94)

The existing finance workflow records approved budgets, commitments, invoice or
valuation lines, exceptions, holds and human disposition. It never executes
payment. `Paid outside this system` is a human-entered note, not a bank result;
it does not change budgets, commitments or grant/cash records. There is no
payment adapter, banking integration or model approval.

Every match exception carries its affected zero-based `line` index, including
budget, commitment and duplicate blockers that affect every invoice line.
Missing budget, commitment or milestone references remain blocking unknowns;
multiple matching approved commitments are ambiguous, never first-match wins.
References record supplied evidence, not verified milestone authority.
Acceptance recomputes matching against current records: a previously matched
invoice cannot bypass a later accepted amount or a newly received duplicate.
Resolve/reject the duplicate before accepting the original. Holds and
`Keep on hold` remain record-only and cannot authorize payment.

Finance writes require current registered named staff. Preparation captures
email, staff code and optional OID; an approver matching any populated identifier
is not independent, even with another email/role. Different people with the same
permitted role can approve. Legacy preparers are looked up by their recorded
email; an unresolved identity refuses approval rather than assuming independence.
This establishes synthetic identity mechanics, not real delegated authority.

SQLite and inherited SQL Server save repeat actor/independence checks inside the
existing writer transaction; rowversions reject stale concurrent writes.
Failure recovery drops failed-operation success audit and touched/validation
state before any fallible recovery read, restores cached snapshots and forces
the next healthy entry to refresh persisted records. A caller's prior legitimate
audit prefix is retained. Recovery and lock-exit failures are logged and attached
as exception notes without masking the original operation error. A retained
audit prefix that cannot flush remains pending for the next healthy write.
JSON caught save/audit failures restore the prior case and ledger tail;
separate JSON/ledger files still do not promise cross-file abrupt-crash atomicity.
Ledger rollback runs independently of the state retry. If that retry also
cannot persist, an explicit error marks the durable outcome as potentially
unknown: reload persisted records before retrying, never infer approval.
Shared SQL edits are the finance validation hook, canonical `SqlStore._discard`
cleanup and original-error preservation at save-refusal/lock-exit recovery.
The `_discard` primitive integrates merged #84 / PR #382 from main `bbbc924`:
committed checked-document snapshots restore before recovery reads, and an
active stock/technical decision retains caller-owned refusal cleanup and actor
context. The same save transaction retains provenance, bulk, stock, finance and
safety/resident/stock checks; no second discard helper was introduced.
Procurement #90 and signoffs #84 remain separate scopes, not inferred dependencies.

From the repository root with editable src packages installed:

```bash
PYTHONPATH=src/core/tests:src/api/tests:src/agents/tests .venv/bin/python -m unittest \
  test_finance_match_controls.JsonFinanceChecks \
  test_finance_match_controls.SqlFinanceChecks test_finance_signoffs \
  test_finance_match_api -q
```

The local isolated SQL Server contract reuses the
[existing SQL configuration](../api/README.md) and the CI MSSQL image/driver.
With `ZF_SQL_*` pointing at an explicitly disposable local server and credentials
supplied privately, set `ZF_FINANCE_MSSQL=1` and run
`test_finance_match_controls.MssqlFinanceChecks`. Each test creates and removes
only its own UUID-named database, never wipes an existing database. On 2026-10-17,
the original 14 local SQL Server cases passed, including reopen, audit rollback, fresh
role/OID refusal and concurrent writers. The initial run's 14 cleanup errors
were driver-pooled connections; the harness now disconnects only its created
database before dropping it. This is local engineering evidence, not Azure,
tenant, real-payment or full PRD AC-021/042 acceptance. Correction TWO then
passed 18 SQL Server cases plus one added internal-save-refusal case, covering
actual audit INSERT followed by first/persistent recovery SELECT failure,
prior legitimate audit retention, failed lock-exit retry, original-error
identity, reopened Proposed state, lock release and subsequent healthy approval.
The exact-852b342 coordinator verdict remains Revise until external closure;
local resolving evidence is not an independent Pass.

After the authorized main integration, 232 local tests passed across finance,
stock, procurement/workflows and shared callers, with one existing opt-in
browser test skipped. Actual isolated local SQL Server passed all 19 finance
tests and 18 canonical stock/selected procurement/workflow tests. The combined
checks cover rollback/reopen, early/persistent recovery failure, original
errors/logging, current authority, independent sign-offs, capacity and work-order
history. External coordinator closure of the integrated #94 head remains pending.
## Evidenced provider capacity and controlled orders (#90)

The existing procurement document remains the package/order store. Positive
committed capacity now requires an original clean uploaded source, its exact
version and verified SHA-256 bytes, source/review dates, delivery interval,
covered home IDs and unit `home-work-order`. One unit allocates one home order
over the entire package period, not a crew, weekly throughput or concurrent
appointment slot. Offered, legacy numeric-only and unknown evidence never
authorize issue, booking, correction, completion or case advancement.

Source date must be no later than review date, which must be no later than
today and at most seven days old. Delivery endpoints are inclusive and within
the package period. Booked dates must also fall inside that interval. Accepted
evidence is bound to supplier, contract version and package scope version;
rescope, source replacement, a changed hash or stale review requires renewed
human acceptance. Zero or reduced commitment can be recorded without inventing
positive evidence. Deficits remain visible and block further progression.

Consequential actions require a current registered named manager and a trusted
staff `contract_authorities` entry. It contains `reference`, string `version`,
exact `contract_ref`/`contract_version`, `revoked: false`, inclusive
`valid_from`/`valid_to`, and explicit `actions`, `suppliers`, `scope_versions`;
optional `package_ids` further restricts scope. Actions are `capacity`,
`rescope`, `issue`, `reissue`, `appointment`, `complete`, `correct`, `withdraw`.
Rescope requires both old and new scope versions. There is no wildcard,
self-granting endpoint or production delegation seed. Draft package creation
grants no authority. Creation requires a nonempty contract/call-off version,
which is trimmed and fixed at creation; blank versions are refused before any
package or success audit is written. Real trusted provisioning remains a
human prerequisite; the test-only fixture helper is not an operational delegation.

New allocations require used capacity strictly below commitment. Existing
allocations may progress at equality; completed orders retain consumption.
Authorized withdrawal releases one allocation with a reason and new version,
and withdrawn orders cannot reopen. Every successful order mutation appends an
immutable sequential snapshot with named issuer/email/time, reason, state,
appointments, scope/resident bindings, delegation and capacity version.
Returned records are copies. Contractors can only read their own orders;
they cannot change orders or read packages. Template/AI outputs explicitly
remain **not an instruction**, including after review.

The alternate case `advance` path requires exactly one current Appointed order
whose latest appointment is Booked, plus current authority, capacity,
resident and safety/building controls. It creates no order or allocation.
SQL repeats actor/delegation, source-case rowversion and procurement dependency
checks inside existing writer/application locks and checked-document
transactions; rejected writes restore cache and discard success audit.
Procurement/advance scopes own failed-operation recovery, alongside the
existing stock/technical scope. Recovery clears pending writes before reload;
checked-document reload publishes only a complete decoded snapshot. A failed
reload logs explicit uncertainty and adds a note without replacing the
original refusal/error. Cached committed state is retained, reads fail closed
while unavailable, and later saves cannot flush the rejected mutation/audit.
JSON uses its existing single-process lock and compensating snapshot recovery,
not cross-process isolation or snapshot/ledger crash atomicity.

The [API guide](../api/README.md#provider-capacity-and-order-api-90) gives the
structured payload and local replay commands. Tiny fictional tests exercise
JSON, SQLite and actual local SQL Server 2022, including competing last-unit
writers and authority/source/booking races. These are engineering checks, not
live supplier commitments, legal signature verification, actual delegations,
Azure acceptance or full PRD approval.

## Form schema registry and candidate staging (#97)

`forms` adds an immutable, sequentially versioned registry in the existing
`form_schemas` checked document and append-only `form_staging` batches in the
existing case body. JSON and SQLite use the existing store interfaces;
MssqlStore inherits the SQL checked-document and case-row-version machinery.
No new service, table, dependency or AI task is introduced.

Schemas contain type/template and rule versions, stable field/section IDs,
types (`string`, `integer`, `number`, `boolean`, `date`, `enum`), explicit units
or null, enum options, required/conditional metadata, source-kind precedence,
evidence requirements, calculation references and a registered reviewer.
Funding association is explicitly `Unknown`, `Not applicable` or `Evidenced`
with scheme/route/evidence references. Funding forms cannot choose not
applicable. These are supplied **unapproved policy references**, not verified
scheme terms or actual authority. Conditions and calculation references are
data only; this module does not run form validation or calculations.

Every registered version is `Unapproved`, with null approval evidence and a
server-recorded actor, time and `ai_registry.digest`. Registration cannot
accept an approved flag, approval evidence or actor override. No actual
approved form/template or delegated authority was supplied for this slice.
It cannot prepare an approved form; real recorded version-specific authority
and binding remain unmet. Synthetic fixtures demonstrate mechanics only.

A separate fictional review pack, `src/core/evals/fictional_form_review_pack.json`
(registered `DS-FICT-FORM-REVIEW-PACK`; [reviewer guide](../../docs/reference/research/retrofit-synthetic-data/form-review-pack-97.md)),
supplies a concrete versioned template, per-field authority, evidence, freshness
and lineage, proposed role separation and stale propagation, and fourteen null
Finance decision fields for human review. Its schema uses this path, but the
public file carries a placeholder reviewer (public payloads may not hold email
addresses) and is refused as published; only a copy differing in `reviewer`,
set to an existing registered person, registers, as `Unapproved`. The pack is
not an approved template, and criterion 1 stays unmet.

Candidate collection copies the existing case-owned document ID,
`content_sha256`, version and upload date. Original bytes must match the stored
hash; generated placeholders, foreign documents and unclean sources are not
accepted. All alternatives remain separate candidates in input order, with
`Not reviewed` state; no winner, normalized value, source correction,
eligibility, financial commitment or submission is produced. Source authority
stays `Not established`. Declarations, signatures, attestations, consent and
approval categories cannot receive candidates.

Supplied `processing` records parser/version, optional model version and
route/error references as `Supplied, unverified`, never attested execution.
The separate server verifier is `form-source-locator-1`:

* Text: strict UTF-8, no newline normalization, zero-based Unicode-code-point
  half-open `start`/`end` offsets, exact raw-span equality.
* CSV: strict UTF-8 and the standard strict CSV reader; one-based `row` and
  `column`, including the header. Quoted/multiline cells retain their decoded
  cell text as raw value.
* OCR import: asserted one-based page and a nonblank region string (at most 300
  characters), supplied route evidence and
  error record required. Pixel content and route authority are **unverified**;
  no OCR/model is called or approved.

Unsupported text/CSV source types, decoding failures and malformed CSV record
`Manual recovery required`, the schema's registered reviewer as owner and a
manual correction/transcription path, with zero candidates. A source-storage
failure is an error, not successful manual recovery.

Arbitrary source-derived content is conservatively restricted to current
staff with the intersection of existing Finance-view, resident-record-view
and reason-view rights (normally the Programme Manager). SQL rereads the
registered actor on each operation; a schema can never grant access. Retained
reads recheck these rights and source presence/clean scan. Generic case detail
never includes the raw staging body. Audit stores IDs, source hash and candidate
count, never raw values. SQL commits body/registry and audit transactionally,
and restores failed/conflicting operations. JSON uses the existing separate
snapshot/ledger files with operation-local failure restoration; it does not
provide SQL's cross-file crash atomicity.

The [API contract](../api/README.md#form-schema-and-candidate-api-97) lists
payloads and HTTP behavior. From the repository root in an installed pip venv:

```bash
PYTHONPATH=src/core/tests python -m unittest discover \
  -s src/core/tests -p test_form_staging.py -v
```

Offline synthetic tests cover JSON/SQLite restart, immutable versions,
Unicode/CSV matching, alternatives, OCR assertion retention, wrong-source/hash
denial, current rights/scan, human-only fields and failed-save/audit rollback.
This is not full PRD AC-046/047/053 acceptance, approved-form preparation,
actual extraction, live SQL Server/Azure proof or the downstream #98
field-review/validation/pack/staleness workflow.

## Controlled administrative bulk edits (#78)

`bulk_edits` adds a closed preview/apply contract through
`Store.bulk_edit_preview(user, body)` and `Store.bulk_edit_apply(user, body)`.
It does not provide an arbitrary JSON patch or a controlled decision route.
The API guide gives [request examples and outcomes](../api/README.md#controlled-bulk-preview-api-78).

| Permitted field | Stored field | Additional condition |
| --- | --- | --- |
| `case_reason` | `case.reason` | Administrative explanation only; no state change |
| `handoff_due_at` | `case.handoff.due_at` | Existing active handoff; timezone-qualified time, normalized to UTC |
| `handoff_next_action` | `case.handoff.next_action` | Existing active handoff; no work instruction or approval |

Every field requires a current registered named human, existing owner or
programme-manager authority, existing case-note visibility and an open,
unpaused case. The current default note-visible roles are Resident Liaison
Officer, Building Safety Liaison and Retrofit Programme Manager; manager status
alone does not grant note visibility. Identity email/code/name/role/OID must
match the current staff record. A trusted-proxy claim never acquires a wider
database role. JSON keeps its existing single-process lock; SQL reads staff
fresh even when the normal process cache has not seen a case-sequence change.

Preview records selected IDs in order, each field's old/new values, failures and
predicted outcomes. Missing or noneditable targets return only the submitted ID
and refusal, not values. Any target failure blocks the whole batch; no failure
is silently skipped. Unchanged targets are `no_change` and receive no invented
case edit history/version. One case is valid too. Source, source version and
change reason are mandatory and strict-length validated, never truncated.

The existing checked `bulk_edits` meta document retains server-owned requests,
snapshots and results. SHA-256 of the canonical issuance envelope is anchored
in the append-only hash-chain audit, independently of that mutable document.
Returned objects are copies. Apply accepts only the creator's preview ID,
verifies issuance and unused state, schema, current staff/role/OID, ownership,
case rules, whole-case digest and SQL rowversion. A changed-away-and-back SQL
case is still stale. Changed data, tampering, consumed/blocked previews and
authority changes require a fresh preview; permission denial is not repaired
by switching screens. This is not protection against rewriting both trusted
storage and its ledger.

Application eligibility is derived from the anchored issued records, never
from mutable `status` alone. Ordered request IDs and records must match exactly,
snapshots must cover every target, failures must be empty, and only consistent
`would_apply`/`no_change` outcomes with the exact proposed fields are eligible.
Changing `blocked` to `pending` in cached or persisted SQL state cannot enable
a failed batch. The SQL commit repeats this contract and revalidates every
issued target, including no-ops, against its exact proposed old/new changes.

SQL repeats identity, case and governance-snapshot validation after
`BEGIN IMMEDIATE`, inside the existing cross-process writer transaction.
Case writes, per-case `edit_history`, batch consumption/result, queue maintenance
and hash-chain events commit together. The inherited SQL Server adapter uses
its existing application lock and the same portable SELECTs; no new schema or
service is required. On failure the bulk-scoped recovery drops staged success
events/edits and reloads all shared documents, restoring absence too, before
recording a metadata-only refusal. A lost commit acknowledgement is explicitly
uncertain: inspect persisted case history before retry; replay cannot apply a
consumed preview again.

Each changed case retains exact old/new fields, source/version, registered
actor/role, UTC timestamp, change reason, monotonic edit version and batch ID.
The complete same event is hash-chain audited. Roles without note visibility
see only event identifiers/actor/time and a held-details label. Request-wide
input errors and apply denials are visibly audited without raw hostile values.
Successful/blocked preview issuance is anchored; per-target failures remain in
the retained issued preview.

Bulk edits cannot alter technical work, consent, safety, procurement,
budget commitments, invoices, payments, claims, quality, defect/complaint
closure, contractor instructions, ownership, source documents or resident
commitments/deadlines. A next-action note records an administrative chase, never
issues contractor instructions. Named receiver acceptance remains the sole
handoff ownership-transfer path.

Offline tests use only temporary synthetic fixtures:

```bash
PYTHONPATH="$PWD/src/core/tests:$PWD/src/api/tests:$PWD/src/agents/tests" \
  .venv/bin/python -m unittest test_bulk_edits test_bulk_edit_api -q
```

Coverage includes exact previews/history, mixed/no-op outcomes, every controlled
category, stale and ABA cases, creator/role/OID revocation, interleaved
two-store apply, guardrail races, issuance corruption, rollback at case/document/
audit/commit boundaries, lost acknowledgement and reopen. SQLite establishes
the local transactional evidence; no live Azure SQL, private stock, model or
operational approval is claimed. JSON retains its existing separate-file
case/audit limitation and is not cross-process transactional evidence.
Correction TWO implements the earlier RV-002 upload/offer/accept provenance
gap below. This supersedes the earlier residual-only disposition, not the
historical Not accepted Review. Final-head independent reassessment is still
required; engineering checks are not human, platform or full PRD acceptance.

### Single-record upload and handoff change sources (correction TWO)

`add_document(..., metadata=body)`, `offer_handoff(..., metadata=body)` and
`accept_handoff(..., metadata=body)` require caller-supplied nonblank strings:
`source` (maximum 200), `source_version` (100), `reason` (300). No filename,
content hash, history count, acceptance state or default stands in for those
inputs. Actor, UTC time, change version and exact old/new fields are server
recorded; caller overrides are refused. Source metadata records a human
assertion, not verified source authority or controlled approval.

Offer/accept also require `handoff_version`, the nonnegative integer count of
current `handoff_history` events from case detail (zero when absent). A changed
offer/receipt/escalation/answer requires reload, even if the recipient is the
same. Legacy `hand_over` is still an offer-only alias and requires the same
metadata. Existing owner/manager offering and recipient-only acceptance remain
mandatory; there is no immediate or bulk reassignment.

Uploads retain supplied source/version/reason on the document and append
`document_history` with the complete before/after document-reference lists
(ID, name, kind, hash and document version). Handoff offer/accept enrich the
existing sequential `handoff_history` with supplied metadata, registered actor,
UTC time and exact old/new handoff and ownership (`owner`, `owner_code`,
`owner_role`, `waiting_on`); an offer records resident-update changes too.
The identical complete event is hash-chain audited as `upload_document`,
`handoff_offered` or `handoff_accepted`. Source version and server history
version are distinct. Returned documents and case detail are copies.

`change_provenance` shares validation/commit/recovery only across these
single-record operations, separate from forms and bulk permissions/contracts.
SQL rechecks the registered actor under its writer transaction and uses the
existing rowversion check to refuse concurrent target changes. Metadata,
history and audit commit together. Failure discards staged changes/success
audit and records a safe refusal; uncommitted uploaded bytes are removed.
A lost commit acknowledgement remains explicitly uncertain: reload history
before retry; a document that actually committed keeps its bytes. Blob and
SQL do not become a distributed transaction. JSON keeps its separate-file
crash-atomicity limitation, with operation-local restoration on failure.

Legacy requests missing metadata now refuse with actionable errors; updated
API/UI paths collect explicit details. Existing historical records remain
unchanged/unknown, never backfilled. Normal note restrictions redact new
source/version/reason/change details; form-staging bodies remain hidden.
No controlled decision/approval is introduced.

`test_change_provenance` covers missing/blank/typed/oversized and forged input,
exact source retention/event-audit equality after SQL reopen, stale handoff,
recipient-only ownership, actor revocation at commit, row conflicts, rollback,
lost acknowledgement, byte retention and note redaction. Existing forms
pending/missing-rescan and bulk RV-001 tests remain in the combined selection.

## Read-only source cadence labels (#216)

`source_monitor.source_freshness`, `card_freshness` and `dated_card` read the
existing monitoring configuration and observations without creating tables or
modifying a source, card, approval, clock, hold or alert. They share #213's
cadence semantics: a source becomes `out_of_cadence` at
`last_success + cadence_days`, including equality. A failed attempt never
refreshes the successful observation. Missing tables/configuration/success and
a clock before the latest attempt (even a failed attempt) return `unknown`,
never fresh. Free-text source-register cadence is not guessed into a duration.

Per-source status, configured cadence, last-success date and due date accompany
the card label. Any known overdue source makes the card out-of-cadence;
otherwise incomplete/empty coverage is unknown; only all in-cadence sources
yield in-cadence. This is a monitoring label, **not legal-currentness evidence**,
source eligibility or permission to rely on a rule. Existing source/version
gates and human approval remain separate; freshness reads never suppress safety
alerts. API collection/version reads and bounded chat use the same read model.
Historical chat stores the label and its as-of date, not a live freshness claim.

From the repository root with editable packages installed:

```bash
PYTHONPATH="$PWD/src/core/tests" python3 -m unittest \
  test_source_freshness test_source_monitor test_rule_engine test_regulatory_chat -q
```

The [evaluation report and acceptance audit](../agents/README.md#regulatory-evaluation-gates-216)
distinguish the generated 60,000-home stateless rule baseline from a small
SQLite integration slice and the unexecuted continuing-stock/staff trials.
No owner threshold agreement, legal approval or operational use is claimed.
The [integrated full-suite record](../agents/README.md#integrated-full-suite-correction-evidence-2026-10-16)
distinguishes executed passes from opt-in skips. Empty-source LawStore HTTP
coverage verifies unknown cadence and unknown draft-rule checks without alerts;
missing storage remains an explicit service-unavailable state with a human route.

## Derived role task queues (#76)

`taskqueues` provides the shared, read-only `work-queues-1` definition/default
contract and case task context. Store and SqlStore return identical projected
context in staff list/detail. Both retain a process-local case-ID membership
cache before filtering/counting/paging. JSON builds all six memberships together
from the canonical evaluator on a cache miss.

Funding, resident-decision and technical final-check requirements remain visible
in `work.blockers` at other stages with `current_stop=false`; they do not place
that case in Blockers or replace its current-stage reason/action. At
`Final checks before ordering` those outstanding requirements are current stops,
including when a handoff is pending. Membership and the selected reason/action
use the same active set. Safety, unresolved stock and applicable shared-building
holds retain their existing stop precedence, owners and snapshot clocks. No
transition, consent, funding or competent-role approval gate is relaxed.

SqlStore and MssqlStore persist six `queue_*` integer columns, each indexed with
the case ID. Seeding and case writes maintain membership in the same transaction
as the body, sequence and audit. Ordinary unlinked-case writes evaluate only
changed cases. Shared building/procurement and linked-home writes conservatively
recompute all memberships using authoritative SQL bodies and shared documents,
not a stale process copy. Older schemas add default-zero columns without marking
them ready; startup backfills before certifying the complete generation. Reopening
a populated database does not need the seed file.

A persisted fingerprint covers queue definition version, internal membership
evaluation revision, dataset `as_of`,
complete ranking policy and current resident-authority/retention day. Changes
force a full refresh; flags, fingerprint and generation publish atomically.
The current-stage correction keeps public `work-queues-1` and the reset/default
contract unchanged, but advances the internal membership revision to 2. Populated
SQLite and SQL Server databases with the original fingerprint refresh derived
flags without changing case bodies, rowversions, sequences or audit history.
Every lookup, including a hot hit, checks freshness under a short cross-process
writer lock and synchronises the case copy. A cache miss selects only IDs from
the relevant covering SQL index. Filtering, global ranking and sorting still
run in memory after lookup; they are not constant-time. Cached IDs contain no
viewer-projected context: visibility, ownership, filters and returned narratives
are checked anew for each request. No approval, assignment or event semantics
change. CSV still projects every matching output row.
The API guide documents [definitions, source fields, snapshot clock, redaction
and remaining owner decisions](../api/README.md#role-task-queues-and-shared-case-context-76).
JSON/SQLite semantic tests cover seven/30/180-day boundaries, unknowns,
handoff lifecycle, independent deadlines, missing named owners and 120-case
paging/sort/export parity. Role-only responsibility never invents a named owner;
draft policy and accepted AI advice cannot produce approved programme priority.

### Generated 60,000-case queue timing (#327, 2026-10-16)

Local Python 3.12 SQLite results, not Azure or private-stock evidence. The
reproducible fixture is `test_sqlreads.queue_cases(60000)`, seed 5, snapshot
2026-10-16: fictional Test Road homes with deterministic stage dates, EPC dates,
handoffs and resident-update deadlines; 58,224 are open. Measurements exclude
generation/database initialisation and include the same lightweight evaluator
counter in both runs. Baseline is the exact merged `Store`/`SqlStore` source at
`aedd616` (#336), loaded in memory without altering the checkout. Three rounds
per queue each commit a one-case `benchmark_revision` change, read the first
50-row page with a cold application cache, then repeat that identical page.
These are application-cold reads after a write, not flushed OS/database caches.
The unavailable priority queue has no output rows.

All values are median milliseconds, before/after this SQL-membership change:

| Queue | Matches | Cold before | Cold after | Repeat before | Repeat after | Write before / after |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| new | 19,375 | 2900.0 | 1062.9 | 60.8 | 54.1 | 16.6 / 5.1 |
| priority (draft policy) | 0 | 2850.5 | 1140.5 | 0.2 | 0.2 | 6.1 / 4.7 |
| stale | 14,539 | 3487.7 | 1107.9 | 59.2 | 41.0 | 4.2 / 4.7 |
| blocked | 58,224 | 3153.5 | 1241.0 | 191.8 | 145.0 | 3.4 / 4.0 |
| overdue | 18,326 | 3029.8 | 1157.0 | 55.3 | 54.3 | 2.5 / 3.6 |
| unowned | 11,675 | 3032.2 | 1130.5 | 43.6 | 34.2 | 3.8 / 4.1 |

Cold reads evaluate exactly 50 output contexts, down from 58,274; priority
evaluates zero rather than 58,224. Repeat reads still evaluate output contexts.
Global ranking is rebuilt after each write, even for the empty queue, and
remains a significant cold cost. Across these rounds cold times ranged
2281.6-4305.1 ms before and 474.9-1259.4 ms after. Baseline write outliers
reached 1005.2 ms; final writes ranged 3.3-7.4 ms. These small, noisy samples
do not establish a write-speed improvement or a production latency guarantee.

Fresh database initialisation, measured separately including seed/backfill,
was 14.213 s before and 15.029 s after. Day, policy, definition or snapshot
refreshes and shared-dependency writes can still recompute the whole stock
under the writer lock; their latency is not represented by the ordinary
one-case write column. No live Azure SQL timings were collected.

A later full-suite run after integrating `main` at `79b153b` observed cold
medians of 1.33-2.00 s, repeat medians of 0.3-222.6 ms and initialisation of
25.521 s. Context counts remained exactly 50/zero. This additional observation
illustrates timing variability; the paired table is not a stable latency promise.

The earlier cache-only #336 measurement was 3217.4/3090.6 ms for a first cold
`new` page: it did not materially improve cold latency. That historical
second-page experiment is not interchangeable with this post-write benchmark.

Run from `src/core` in the installed pip venv:

```bash
python -m unittest discover -s tests -p test_queue_benchmark.py -v
python -m unittest discover -s tests -p test_sqlqueues.py -v
python -m unittest discover -s tests -p test_taskqueues.py -v
```

The benchmark asserts bounded context calls, not a noisy cold-time ceiling.
It fails for all six queues with the baseline source. Separate mutation checks
also fail when SQL lookup, incremental writes or shared-dependency maintenance
are disabled. The existing `test_sqlreads` scale test retains its 1500 ms
repeat-page ceiling. JSON/SQLite parity covers every queue, sort and view,
including positive approved priority, search, combined filters, exports and
cursors. SQL tests verify physical flags, index plans, backfill without a seed,
rollback and cross-process shared-context/generation handling. Server-free
tests check SQL Server integer schema/migration, index translation and portable
lookup/write statements. `MssqlQueueMembership` wires the same behavior tests
into the existing opt-in SQL Server harness; skipped live tests are not evidence
of actual Azure SQL execution.

## Resident decisions and representatives (#86)

`resident_decisions` records supplied human statements, never inferred consent.
Every measure starts `Not recorded`, including when a historical case-wide
answer says Accepted. A staff member first records the exact measure scope,
its source and the current technical design version. Scope revisions increase
monotonically; any case-wide technical design change invalidates the current
resident contexts conservatively. Changing back never restores an old answer.
New answers require the exact current context revision, a supplied source and
who spoke. Recorded home, measure, scope, design, actor, time and version remain
in history. Contact, access, AI drafts and other measures cannot populate them.

A pause, withdrawal or decline creates a human-review flag for that measure.
Its siblings' statements are unchanged. Restart requires a new supplied
acceptance and human-review evidence; neither a complaint outcome nor an AI
proposal clears it. Case advancement checks every measure; work-order versions
and quality records bind explicit measure/context revisions and check only
those dependencies. Unbound legacy work/quality records cannot release work.
Package scope changes require reissue with explicit current resident bindings.
Safety, technical, funding and shared-building checks remain independent.
The existing SQL transaction rechecks resident bindings, current authority and
case row versions before commit, including operations that only change work
orders. SQLite concurrency/restart and a separate synthetic Azure SQL exercise
are tested; this is not real resident or operational acceptance.

Each representative reference has versioned task-limited authority: measure,
scope/design, source, evidence date, review date, resident's stated wishes and
confirmed safe-contact reference/revision. Scheduling/attendance/interpreting
does not grant works-decision authority. Authority must be Confirmed, cover the
requested task/current context, start no later than today and have a review date
strictly after today (the review date itself stops reliance). Unclear, disputed,
revoked, superseded, missing or expired authority stops representative decisions
and disclosure checks until staff confirms through the safe route. A contact
change, even changing back, requires new authority. Historical representative
acceptance is rechecked at use time against its exact latest authority version;
another valid representative cannot substitute. A resident's direct supplied
statement remains recordable independently. Nothing is sent by the checker.

Independent review is a separate service type linked to an actual recorded
measure-decision version. Its reviewer must be neither the contested recorder
nor the request handler; only the named reviewer updates/closes that review.
New decision versions capture the registered server recorder's email, staff code
and oid (when present), with name/role as recorded labels. New independent review
requests retain that exact decision version's identity snapshot, not the latest
answer or today's owner of its email. Opening and redress reassignment compare
nonblank email/code/oid case-insensitively, so an email change cannot make the
original recorder independent. Client identity fields cannot override evidence.
Decision recording uses the existing atomic resident writer and SQL actor replay.
Email-only or missing historical snapshots are explicitly `Unknown`; assignment
of independent review is refused until original evidence can be resolved. Old
records are not backfilled. A legacy request without its own bound snapshot stays
Unknown even if a decision with the same measure/version exists: retention can
delete and later reuse that ordinal. New bound requests preserve their original
snapshot after resident payload deletion. This does not change retention or
authorize historical erasure. Unrelated supplied consent, service/complaint
requests and service-owner reassignment remain under their existing controls.
Recorder snapshots are visible only to existing resident-view roles, not other
staff, contractor detail, exports or model facts.
Complaints retain separate handler/redress owners and independent closure.
These routes remain recordable on paused or closed retrofit cases and do not
change consent, ranking inputs, hazards, tenancy or repair state. No live formal
complaints integration or real-user without-detriment evidence is established.

The owner confirmed the field matrix on
[2026-10-16](https://github.com/jmservera/ama/issues/86#issuecomment-6209881675).
Existing `Resident Liaison Officer` represents Neighbourhood/Resident Engagement;
`Retrofit Coordinator` represents Retrofit staff. Both record and view decisions,
authority evidence, wishes and safe-contact references. `Retrofit Programme
Manager` and `Programme Support Officer` view, but cannot record these fields,
including through the legacy decision endpoint. Writers must match a registered
named human, not merely supply a role. Separate complaint/redress actions retain
their existing named-owner controls; they cannot change works decisions.
Other staff do not receive authority/contact/source/wishes narratives.
Resident viewing rights do not depend on `ZF_REASON_ROLES`; unrelated vulnerability
and contact-note restrictions still apply. Contractors receive only per-measure
`Proceed` or `Hold` resident readiness, never the underlying resident reason,
wishes, vulnerability or safe-contact details. Other existing operational
allow-listed fields remain. AI tasks use narrow task inputs; no authority,
wishes, safe-contact history or complete decision record enters those inputs.
Views detach histories before redaction. Audit uses event/version metadata;
new legacy decision notes are no longer copied into the immutable ledger.

The [owner's first-contact clarification](https://github.com/jmservera/ama/issues/86#issuecomment-6209904857)
sets retention to five calendar years from the resident's first recorded
interaction, not the decision, withdrawal, authority expiry or work completion.
`RESIDENT_RETENTION_YEARS` in `resident_decisions.py` is the configurable constant.
The earliest eligible valid nonfuture `contacts`/`resident_contact_history` timestamp or
`resident.first_contact_at` establishes the origin. Recording contact or a
resident-confirmed safe route preserves the earliest marker until deletion. Missing/invalid
history stays `Unknown`, never inferred from a decision; reconcile it before
operational use. The schema has no universal cross-case resident identity:
importers must preserve the resident's actual first-contact marker across cases,
not match people by name or address.

`resident_retention` in staff detail reports origin, due date and expiry.
February 29 anniversaries use February 28 in a non-leap year. At the anniversary,
decisions and representative disclosure/consent checks cannot release work,
even if legal hold retains the records. Withdrawn decisions and expired
authority use exactly the same schedule. The existing manager retention list
includes a `resident-decisions` item; approve it through `retention-approve`
to remove current scoped decisions, authorities, wishes, safe-contact references/
history, resident reviews and scopes, reset the legacy answer, clear the resident
representative and remove service-request representative references. The cached
first-contact marker is cleared. A personal-data-free tombstone retains only the
count of general contacts present at deletion, alongside the deletion date.
Complaint outcomes and general contact
records have separate purposes and are not silently deleted. Legal hold blocks
deletion, not expiry. Deletion is manager-reviewed, not a configured automatic
purge job. Existing ledger text, backups and SQL row history are not erased by
current-payload removal; operational erasure needs a separately approved design.

The [owner's restart decision](https://github.com/jmservera/ama/issues/86)
(2026-10-16) starts a new five-year period from the first contact recorded after
deletion, not from deletion itself. Until that contact, origin and due date are
`Unknown`. The tombstone excludes the retained pre-deletion contact prefix, even
when renewed contact has the same day/minute timestamp. Either a newly logged
general contact or a newly confirmed safe-contact route can start the period;
later contacts do not extend it. Old decisions, authority and scopes are not
revived: staff must record fresh scoped evidence. Expiry still holds release and
representative disclosure until manager-approved deletion and renewed evidence.
Each later approved deletion establishes a new boundary. For older date-only
deletion records without a count tombstone, general contacts on or before the
deletion date are conservatively excluded because their same-day ordering cannot
be recovered; a later-day contact or fresh safe-contact confirmation can establish
the new period. Neither path infers resident consent.

Cards, missing-decision filters and AI citation labels use current scoped
status, not the legacy answer. The SQL missing-decision filter deliberately uses
the existing live in-memory path because authority can expire without a write;
other indexed filters remain unchanged. Existing AI proposal configuration,
release and human-review controls remain enabled as before. Representative-
addressed legacy templates refuse unchecked disclosure; staff-facing AI
message/summary proposals do not depend on that addressed template and remain
unapproved drafts, never consent or sending.

`tests/test_resident_decisions.py` covers JSON/SQLite exact-context decisions,
authority expiry/supersession/contact, sibling-only work/QA release, independent
review, privacy persistence and stale transaction refusal. Synthetic adapter
calls are not live inference. Formal complaint routing, human accessibility/
without-detriment acceptance, actual model and full hosted workflow acceptance
remain unmet. The opt-in `AzureResidentDecisions` test exercises the SqlStore
behavior through MssqlStore on an isolated Azure SQL database using constructed
DATA only, verifies reopened state/current-payload purge and an intact audit
chain, and reports the database ledger mode. It refuses database names outside
the `resident86test` prefix. The operator must create a fresh database, supply
Entra authentication, and remove verification resources afterward:

```bash
ZF_RESIDENT_AZURE_TEST=1 PYTHONPATH=src/core/tests python3 -m unittest test_resident_decisions.AzureResidentDecisions -v
```

This is a real SQL engine check, not evidence that historical database copies
were erased or that any real resident accepted the service.

## Stock comparisons and human technical sign-offs (#84)

Review status, 2026-10-17: the original Review returned **Not accepted** for
RV-001. Authorized correction ONE disarms pending writes/audits and restores
known snapshots before fallible SQL reload. Actual one-shot/persistent reload
faults now preserve the original error without delayed success events across
technical actions, stock comparisons and terminal dispositions. Ten canonical
local SQL Server tests pass. Bounded independent verification closes RV-001
for this correction, including 91 independent focused tests and two snapshot
probes. This does not establish professional/source authority or operational
acceptance; the original adverse Review remains historical.

`stock.py` validates staff-recorded conflicting assertions for `epc`, `type`
or `built`. Each comparison preserves two different values and each source's
identifier, ISO date, version and recorded validation state, plus a registered
query owner and authenticated recorder. Comparisons append as `SQ-n` with a
case-local version. The original home value is unchanged; authority,
resolution and eligibility remain `Unknown`. A source assertion labelled
`Validated` is not a decision that it is authoritative.

Unresolved queries expose an owned blocker before a design exists and after
sign-off. They prevent technical approval and installation progression, never
remove a home from ranking or block independent hazard intake. There is no
automatic resolver, eligibility-rule engine or stock overwrite. An approved
source-authority/resolution workflow remains future work.

Only the registered case owner or a programme/manager role may open a query.
`stock_query_event` appends a separate `SQE-n` event referencing `SQ-n`; it
never edits the original assertion or any previous event. A query's original
raiser (not merely its assigned query owner), or a programme/manager role,
may `withdraw` with a reason. Only a registered named human in the existing
`Retrofit Programme Manager` or `Programme Support Officer` roles may `resolve`,
with a reason and human review evidence reference. Agents and client-supplied
actor identities cannot exercise these rights. Repeated terminal events fail.

Effective `Withdrawn`/`Reconciled` status is derived from those events in
views and blockers. Reconciliation records a human attestation only: no
source wins, no home value changes, no professional sign-off is given, and
authority, resolution policy and eligibility remain `Unknown`/
owner-approval-needed. These are minimal exercise permissions, not ratified
operational resolution rules or competence/delegation. A new query is needed
to raise a later concern; closed history cannot be reopened or overwritten.
Other unresolved queries and independent technical, building and hazard gates
remain effective after disposition.

JSON retains assertions/events and the hash-chained audit. SQL inherits this
case-body contract and commits the new event and audit together using existing
rowversion checks; concurrent terminal events fail closed. Technical approval
also rechecks current stock holds inside the SQL writer transaction. No new
schema or dialect-specific inserts/error classes are introduced. Local
SQLite evidence does not establish SQL Server/Azure acceptance.

The 2026-10-17 continuation binds stock comparison, terminal disposition and
technical actions to the current registered staff row, including identity/OID,
rather than a process-cached role. SQL repeats that check inside its existing
writer transaction. A failed decision discards its pending case edits and
success audit before lock cleanup, so a later save cannot flush a failed
design change, sign-off or query disposition. Recovery failures are explicitly
logged and annotate the original exception; reload to establish an uncertain
outcome. Canonical discard clears pending audit/touched/validation state before
database reads, restores cached case/recommendation/shared-document snapshots,
and invalidates the sync watermark so the next operation must retry reload.
An ongoing read outage still raises an error, never a successful fallback.
Stock/technical transaction refusals defer discard to their existing decision
scope so recovery cannot mask the original GateError/ConflictError.
This is not a new authority grant or a guarantee against arbitrary
external staff writes outside the store's writer-lock protocol.

The existing `signoffs.py` owns separate assessment, design, building and
coordination decisions. They require registered staff identities in the
existing exercise roles, distinct people and no self-approval of the recorded
design. History records the actor email/role and design version. A design change
returns only the selected design-dependent sign-offs; omitted selection returns
all design-dependent sign-offs, but empty, duplicate or invalid selections are
rejected before mutation. Unaffected decisions keep their original version.
Human reapproval is explicit. Existing building blockers and home hazard holds
are reused, with no transfer of sibling approvals or resident consent.
These role mappings do not attest professional competence or actual delegation.

Support is tri-state: `Yes` for an observed true flag or recorded adjustment;
`No` only for an explicit false flag and `"None"` adjustment; otherwise
`Unknown`. `support_coverage` separately reports `Unknown` if either input is
missing, including mixed positive cases. Compatibility Boolean `support` and
contractor `needs_notice` mean observed positive only, not known absence.
Staff detail/list, counts, visits, filters and AI facts share this meaning.
Unknown inputs remain in the existing nonpositive support ranking bucket;
safety, waiting time, stage and case-ID factors remain independent. No new
health inference or policy weight is introduced. SQL refreshes existing
derived support/rank columns once using `meta.support_encoding=1`, preserving
source assertions, workflow state and audit; no new SQL schema/dialect is added.

`tests/test_stock_reconciliation.py` covers JSON/SQLite semantics and upgrade
behavior, current/deleted/changed-OID actors, an independent-connection
pre-save role change, case/audit rollback and reopen, no delayed success audit,
and decision-context cleanup. The selected canonical cases also passed against
an isolated, local SQL Server 2022 container via
`test_mssqlstore.MssqlStockDecisions` on 2026-10-17: initially eight tests;
correction ONE ten tests, no skips. Added actual early/persistent reload faults
check all three wrappers, original error/log, unchanged case/history/audit,
cross-thread lock availability, cache state, failed retry, later recovery and
reopen. GateError/ConflictError refusal recovery preserves the original error too.
That fixture used no private stock, cloud service or real source authority.
JSON still uses separate snapshot/ledger files and does not gain SQL-style
cross-file crash atomicity from this change.
The [API guide](../api/README.md#stock-reconciliation-api-84) describes
the staff endpoint, rendered synthetic check and remaining acceptance gates.
Deployed SQL Server/Azure, real model use, source authority, competent human review
and direct user acceptance are not established by these local tests.

## Operator incidents and constructed restart (#221)

The existing `continuity` document is the incident authority for AI containment,
not a second release system. Suspension immediately blocks the affected task's
dispatch, completion and pending/ready reliance. Its SQL writer transaction
captures impacted proposals, exact release references and existing serving
bindings without the earlier 500-row preview truncation. Evidence, owner,
containment, resident impact, remediation and declared restart authority are
retained; absent information is explicitly `Unavailable`, never approval.
Legacy output snapshots and append-only incident/corrective-claim audit evidence
are retained. JSON supports durable containment/manual work but has no qualified
release snapshot and cannot restart AI.

Completeness includes every affected pending, leased, ready or accepted
assistant proposal and proposed or accepted/edited legacy output, not just
current releases. Each impact retains its original
release ID/version/digest, exact retained release snapshot and binding, envelope,
task version and prompt version. A prior release is not replaced by today's
candidate. Missing, inconsistent or unresolved historical evidence remains
explicitly incomplete and denies constructed restart without delaying containment.
Both assistant versions and legacy envelope task versions must equal the
original retained release binding's `registry_version`, not today's registry.
Malformed JSON and non-object release bodies deny current admission and are
retained verbatim in the impacted snapshot with explicit incomplete diagnostics.
They cannot roll back containment or qualify a constructed restart.

The global epoch remains event ordering, but historical validity now uses
task/all-scope suspension and restart boundaries. Unaffected ready, accepted
and in-flight proposals remain eligible under their independent release and
source checks. Affected historical work never revives; a fresh activation is
required after a constructed restart. Missing/future/malformed history denies.
Every epoch must appear exactly once in coherent registered-scope suspension/
restart history. Generic missing-task records are noncurrent; recognized old
priority shapes retain their task identity and explicit historical unknowns,
without manufacturing missing release or task-version evidence.
Suspension validates existing history before appending and rejects every
duplicate exact open scope. A whole-release incident and distinct task
incidents may legitimately overlap; the former cannot hide a duplicate task.
Source export validates and normalizes retained task identity before registry,
snapshot or release checks. Missing, array or object capabilities remain in
historical source and HTTP bundle evidence, explicitly noncurrent, stale and
nonactionable with no reliance; they neither abort export nor acquire a grant.

Corrective proposals retain a test ID/reference, explicit constructed Pass
claim, recorder/time, incident/epoch, full server-derived current candidate and
its digest. Replacement releases or model/prompt/policy/data/permission drift
require freshly proposed evidence, without overwriting incident-time versions
or earlier proposals. Decisions need the exact proposal digest and a distinct
current registered OID-bound manager with the separate trusted `ai_restart`
capability. Email, staff code and OID independence are checked. SQL repeats
local identity and candidate checks within its existing atomic writer and
optimistic continuity-document fence. Denied restart attempts are audited
separately; rolled-back actions cannot leak a partial restart.
Early invalid/inactive identities are recorded as unverified claims, not named
verified actors. SQL denial events use the existing atomic audit-only writer
after action rollback, so document-writer failure cannot discard the denial.
Source and bundle export use the trusted current store provider for constructed
versus actual holds; caller-supplied fixture flags cannot relax actual use.

Custody, witness and stop expectations for any future drill are prepared, and not
yet approved, in
[Non-operative custody, recovery and witness preparation (#122)](#non-operative-custody-recovery-and-witness-preparation-122-2026-10-21).

Only a constructed restart drill is implemented. The separate permission
proves an engineering authorization boundary, not OD-35 appointment or
acceptance of corrective tests. `actual_hold` stays true, including after
reopen, provider switching and replacement release approval; actual `Ai`
dispatch and reliance stay blocked. Older restarted incidents without this
field also remain held for actual use. There is no actual restart approval
route while OD-35/RULE-020 evidence is unavailable. No fixture, text reference,
seeded role, model response or synthetic result appoints an actual approver.
Approved monitoring thresholds, competent test acceptance and the
human-witnessed drill remain unmet; this mechanism does not close the issue.
Manual casework, resident challenge, emergency and statutory hazard response
remain independent. No monitor threshold or live model is activated here.

## Task-bound RAI release records (#219)

`assistant_release.py` reuses the migrated `assistant_releases` and
`assistant_events` tables. `rai_release.py` owns pure typed validation/selection;
`ai_registry.py` owns the eleven registered tasks. No workload import, new
schema, SQL dialect extension or SQL/blob dependency for agents is added.
Existing records without the extended contract deny dispatch until a human
records a replacement; startup never upgrades an old approval automatically.

A record requires `release_version`, registry-matching `intended_use`,
`prohibited_uses` and `affected_stakeholders`, a named `accountable_owner`,
`impact_assessment`, `residual_risk_decision: Accept`, a residual-risk note,
`evaluation_decision: Pass`, 1-20 approved evaluation references in `evidence`,
and all seven `material_change_triggers`: `intended_use`, `model`, `prompt`,
`policy`, `data`, `evidence`, `permissions`. A reference is a human-recorded
assertion, not an automated finding that an evaluation passed. Evidence class
distinguishes `constructed-fixture` from `actual`; constructed records cannot
authorize the real `Ai` client.

Bindings include the task use/impact contract hash and evaluation protocol
version, model, registry/schema, prompt, policy, data/provenance and permission
versions. `ai_prompts.py` supplies actual retained-task instructions and their
hash for dispatch, release matching and stored output metadata. Routine case
edits stale source-dependent proposals; changed use, model, instructions,
policy, evidence or permissions invalidate the release or its dependent work.
`AI_MODEL_VERSION` supplies the expected provider model identifier for the fast
deployment; `AI_MODEL_VERSION_STRONG` supplies it for strong requests (defaults
to the fast value). Unattested configured models deny actual dispatch. A
returned model comparison is not independent serving-version attestation.

Approval supersedes every active record for that task, including old routing
configurations, while preserving events. One record approves one deployment;
changing the task's fast/strong route requires renewed approval. A rollback
cannot revive a superseded record. Activations retain release ID/version/body
digest; renewal creates a distinct assistant activation without overwriting
old work. Claim, dispatch, completion, detail/review and export reliance recheck
that reference. Cached briefings, ordinary/document reviews and separate
priority views/reviews also recheck the selected record. Changed releases
during calls discard/quarantine results, even when a replacement has the same
binding. Manual templates, human review, consent and safety controls remain.

Historical AI output requires a nonempty exact release reference and a currently
selected matching record even when inference is switched off. Reliance uses the
task's registered current fast/strong deployment, not its stored historical
alias. Configured briefing fallbacks without a current release are retried rather
than reused from cache, so recording matching approval restores generation
without an unrelated case edit. Workflow-only and unconfigured template caching
and manual/template acceptance remain available.

Configured JSON-store inference now denies because it has no SQL-owned release
record; it remains usable for manual/workflow-only work. Synthetic output
tests explicitly install test-only authorization rather than weakening this
production boundary. No real resident data or model call is needed to exercise
the release-control semantics.

OQ-017 remains open: live release, residual-risk acceptance, suspension and
restart holders and competent-review delegations are not evidenced. The
project contact in a denial is not a grant of those authorities. Approved real
evaluation, provider attestation, Azure SQL race evidence and direct human
oversight remain separate gates. Local synthetic checks do not approve live use.

## Hazard referral and home retrofit holds (#85)

The existing `workflows` module records an unverified observation and links an
external hazard/repair case. Reported category and urgency are not the service's
classification. The existing hazard and repairs service owns categorisation,
clocks, action, resident updates and closure; no command here changes them.
No transport is implemented: sending, receipt, acceptance, repair and timing
references are human-recorded assertions, not independently verified delivery.

New observations require a source/channel reference and timezone-aware
`aware_at`. Reporter, recording time and hold scope are server-derived.
Every hold explicitly covers the linked home/case, not its whole building or
another household. Referral requires a destination staff safety receiver,
external case/job reference and sending evidence. It does not imply receipt.
Only that receiver can separately record receipt and then acceptance, each
with evidence. Sender retains referral follow-up until acceptance; the retrofit
case owner and resident decision never change through these actions.

The receiver may record external response/resident-update due and actual
times, supported by an evidence reference. Unknown times stay unknown;
existing observations cannot be overwritten here. These are not calculated
statutory clocks, service updates or promises of compliance. Previously unknown
external times can still be recorded after retrofit work restarts; lifting that
restriction does not end the external response or updates. Each transition
has an immutable versioned snapshot and an audit-ledger entry, persisted using
the existing case body on JSON, SQLite and SQL Server without a new schema.
Local durability evidence now includes the task-owned loopback SQL Server
exercise below, not Azure or verified external service delivery.

External repair evidence must follow receipt and acceptance. A different
safety-role actor, neither reporter nor repair recorder, must record the
release reason and external supporting evidence. This releases only the
retrofit hold, not the external hazard case. Active holds block technical
sign-off, installation advancement, new/reissued/corrective work orders,
booking/completion and quality acceptance/handover. Existing building,
resident consent, funding and technical gates remain independent.
Manual hazard intake/referral remains available despite AI failure, retrofit
pause or a closed retrofit record, without reopening or changing that record.

SQL-backed guarded transitions reload the dependent home's hazards and check
its row version inside the committing transaction, including work orders that
do not modify the case itself. The existing SQLite writer transaction and
SQL Server transaction-owned application lock serialize intake against that
validation and commit. A hold or stale dependency refuses the entire transition
and its audit entry; it cannot be waived by a process-local precheck.

The safety-role mapping and independent release check above are demonstrator
controls, not ratified operational authority. Repairs, Safety and Housing owners
have not approved who may release a retrofit hold, response/resident-update
timing, or escalation policy (RV-002). Recorded due times are external assertions,
not an approved timetable. Original issue acceptance remains unmet and unchecked.

Legacy hazards display unknown missing provenance rather than inferred dates
or receivers. Active legacy referrals/repairs need a prospective evidenced
referral binding, retaining the original record, then new receipt, acceptance
and repair evidence. Already released legacy holds stay released.
New evidence/source narratives are withheld from staff without a recorded
need and contractors see no hazard record; they are not added to AI prompts.

`tests/test_hazard_referral.py` covers these semantics on JSON and SQLite,
including restart, legacy continuation, invalid actors/indexes/replays,
closed-record intake, consent/building gates and model-source minimisation.
Interleaved two-store SQLite regressions cover all guarded transitions,
including the previously reproducible work-order completion race. The original
SQLite race/trace checks are not relabelled as SQL Server concurrency proof.
Operational timing/escalation policy, real service integration, permitted real
model inference, Azure workflow and human acceptance remain open.
AI remains available through existing configuration/release/human-review
gates; this slice grants it no safety authority and cannot certify those gates.

### Current hazard actor and persistence evidence (2026-10-17)

The hazard-owned `hazard.py` scope now requires current registered identity for
each existing hazard event, reusing the canonical staff lookup. Referrals also
check the destination separately; SQL repeats both checks under its existing
writer transaction. Removed/demoted staff, changed OIDs and substituted receiver
identities cannot acquire authority from a cached session or recycled code.
No delegation or role policy is granted by this check.

Reporter and repair-recorder snapshots retain code/email/OID. Independent
retrofit restart rejects a match on any nonempty normalized identifier, with
retained event/legacy identity fallbacks. The recorded decision is still an
external human evidence assertion, not product assessment of release sufficiency
or external hazard closure. Home scope, separate sent/receipt/acceptance,
sender follow-up and unknown externally supplied timing remain unchanged.

Failed SQL events quarantine staged state/success audit before recovery reads,
retain prior pending audit and original errors, and clear their validation scope.
Correction ONE also marks an acknowledged SQL COMMIT before post-commit
synchronization. If that later read fails, recovery never replays the already
committed audit baseline; it retains/logs the original error and explicitly
reports that the transaction committed. Reload and reconcile before retrying.
JSON persists before emitting success/emergency audit: known pre-replacement
failure restores memory without a success entry. JSON state and its separate
audit file are not one transaction; an audit failure after save explicitly logs
and annotates a potentially persisted outcome. Reload and reconcile before
retrying, rather than assume rollback or duplicate the referral.

Canonical hazard tests run on JSON/SQLite (33 run, one JSON-only skip on SQLite)
and the opt-in `test_mssqlstore.MssqlHazardReferral` adapter runs them on an
actual disposable local SQL Server (16 run, one JSON-only skip). The latter
includes separate-connection commit-time authority changes and failed
release/audit/recovery-read probes, including one-shot/persistent post-commit
synchronization failure with release and prior audit retained exactly once.
The independent Review found that latter defect before correction; its original
Not accepted result remains historical, and parent correction checks are not
independent final-head acceptance. It does not run SQLite-specific transaction
trace tests or establish Azure concurrency, verified transport, real approval
or operational timing policy. Shared fixture recipe and exact manifest hashes
remain unchanged; eleven profile/nine workflow full-journey acceptance is still
unavailable and provisional.

## Return, reopen and handoff accountability (#83)

`workflows.py` is shared by JSON/SQLite local stores and the Azure SQL store.
Every new return/reopen requires a reason, source reference and next action,
and records version, prior/current stage, authenticated initiating authority and
the existing named case owner as receiving owner. A return/reopen never assigns
another owner. Older history is preserved; absent provenance is unknown, not
verified or reconstructed. Selective downstream approval invalidation under
FR-043 is not established by this slice.

Handoffs expose canonical `status` alongside the legacy `state`: `Offered` means
Sent and `Declined` means Rejected. Received, Accepted, Escalated and Completed
are distinct states; Withdrawn remains an explicit terminal alternative.
Only a named recipient may receive/accept/reject. Only the sender or a manager
may withdraw or manually escalate to a named manager. Completion requires the
accepting current owner and a note; it completes the handoff, not the retrofit.
Receipt and escalation never transfer ownership. Acceptance alone changes the
case owner and chase owner. An accepted unfinished handoff cannot be overwritten.
The legacy `hand_over` method now creates an offer using the same checks.

Case detail and immutable `handoff_history` snapshots distinguish accountable
owner, destination role, proposed/confirmed receiver and chase owner. Urgency,
due date, next action and resident-update owner/commitment are independent fields;
missing values remain null. Due dates require an explicit timezone and normalize
to UTC. A pending resident-update commitment survives rejection, withdrawal,
acceptance, completion and replacement offers; handoffs cannot silently change
it. No message is sent, consent inferred or safety hold released.

`pending_handoffs` includes sent/received/escalated work for sender, recipient
and managers. Existing need-role projection holds notes, source references and
next-action text; contractors and unknown roles cannot use these workflows.
The coordination assistant's existing deterministic trigger includes all three
unaccepted states, without gaining action or approval authority.

These are local engineering controls, not approved operational escalation
timings. BG-010/OD-09 remains open: optional human-selected due dates and manual
escalation do not prove acceptance/escalation within approved periods. EXA-008's
24/48/72-hour fixtures are not a production SLA or statutory clock.

Semantic tests: `tests/test_handoff_lifecycle.py` runs on JSON and SQLite;
HTTP tests and a CI-only SQL Server replay live in `../api/tests/`.

## Building shared context (issue #75)

`buildings.py` implements the PRD FR-002 read model. Seed data can contain a
`buildings` list and each home case can carry an explicit `building_id`.
Building records contain exactly `id`, `name`, positive integer `version`,
`source`, `systems`, `dependencies`, `holds`, `works` and `costs`. Each category
is `null` when unknown or a list (including `[]` for explicitly none).
No building approval, resident evidence or home allocation fields are accepted.

* Systems contain `id`, `label` and `source`.
* Dependencies, holds and works add `owner`, `status`, `case_ids` and
  `package_ids`. Case IDs must identify homes explicitly linked to this building;
  package IDs must exist in procurement. `null` applicability is unknown,
  `[]` means none and nonempty lists are exact explicit references. Building
  membership and description text never establish package applicability.
* Dependencies and holds have recorded status `Open`, `Resolved` or `Unknown`;
  works have `Proposed`, `In progress` or `Completed`. These imported statuses
  are source assertions, not application-generated approvals or safety releases.
* Costs contain `id`, `work_id`, `amount_gbp` and `source`. They reference an
  explicit shared work, and GBP amounts are finite nonnegative decimal strings
  with at most two fractional places, bounded at GBP 100,000,000. No allocation
  formula, grant eligibility, spending authority or payment is inferred.
* Home `cost_allocation` entries (`shared_cost_id`, `amount_gbp`, `source`)
  remain on each home, as do documents, consent, technical, funding, quality
  and closure state. Allocations are not added to shared building costs.

Missing/invalid explicitly linked context and applicable unresolved
dependencies/holds block home advancement. New, reissued and corrective work
instructions check the exact package; unknown scope fails closed, an explicit
unaffected home/package does not block. Home readiness considers all applicable
packages. Hazard intake/referral and resident contact remain independent.
Unlinked legacy homes retain their existing behavior, not a claim that
building checks have passed.

JSON Store retains the document in `live.json`; SQL Store seeds, synchronizes
and persists it through the existing checked-document `DOCS` interface inherited
by MssqlStore, without new SQL or DDL. Existing live files and populated databases
are **not reseeded** from a modified seed; absent context stays unknown.
Loading real registers and governed updates/release authority are future work.
There is no building editor or release endpoint in this slice.

`tests/building_fixture.py` supplies a wholly fictional two-home block, two
packages, ventilation work and GBP costs. `tests/test_buildings.py` verifies
JSON/SQLite reopen, independent gates/evidence, explicit/unknown applicability,
role projection, blocked instructions, and uninterrupted hazard intake/referral.
API tests and staff navigation are documented in [api](../api/README.md#building-shared-context-issue-75).
Local SQLite evidence does not establish live SQL Server or Azure behavior.

## Datasets, fixtures and synthetic tools

### Offline provenance and privacy audit (#175)

The [dictionary](../../docs/reference/research/retrofit-synthetic-data/data-dictionary.md#dataset-coverage-and-provenance)
and [provenance register](../../docs/reference/research/retrofit-synthetic-data/provenance-register.json)
cover current sensor, scale/fabric and generated/runtime chat families.
`synthetic.privacy` scans only public registered payloads or an explicitly
supplied snapshot. It does not discover/read private working data, certify
arbitrary text PII-free, or authorize publication of real map anchors or chat.
Run from the repository root with the editable core installed:

```bash
python -m zava_forward.core.synthetic.privacy --public-root "$PWD"
python -m zava_forward.core.synthetic.privacy --public-root "$PWD" --sources
python -m zava_forward.core.synthetic.privacy --snapshot /path/to/fresh-snapshot --kind sensor
PYTHONPATH="$PWD/src/core/tests" \
  python -m unittest test_synthetic_provenance test_synthetic_determinism -q
```

Snapshot kinds are `scale`, `sensor` (including register-backed fabric) and
`chat`. Exit 0 means the bounded pattern/label checks passed, 1 lists
sanitized violations and 2 reports malformed/unreadable input. Every expected
payload is scanned; extra/missing files, wrong labels or hash mismatches fail.
Sensor rows use `source_type=SYNTHETIC`; scale homes/events inherit the exact
hash-bound manifest label; chat/households use Boolean row labels.
Public fixture metadata exemptions never exempt their contents from scanning.
Regexes detect email, UK phone, NI and postcode patterns, not all real names,
addresses or contextual identification. The exact fictional scale-home
`TE[0-8] 1ST` field has a narrow exception. Runtime chat can be personal.

The public-only command passes without private support files. The separate
`--sources` command currently returns 1: Census TS054, IMD 2025 and ONS
boundaries lack verified historic retrieval dates/licence/attribution terms.
This explicitly leaves issue #175's external-source criterion unmet. No dates
are inferred from commits and no official-source currentness is claimed.
Exercise Legal/Compliance/DPO owner Juan Manuel Servera owns the follow-up,
not an automated approval. Rehashed mutation tests independently demonstrate
pattern/label rejection, not merely an unrelated integrity failure.

The [synthetic needs inventory](../../docs/reference/research/retrofit-synthetic-data/needs-inventory.json)
and [scenario manifest](../../docs/reference/research/retrofit-synthetic-data/scenario-manifest.json)
bind each iteration's engineering review by inventory version/date and SN row.
Run `python3 -m unittest discover -s tests -p test_needs_inventory.py -v`
from this project to check that binding and negative mutations. This is a
recorded pre-build gate, not owner approval or full scenario acceptance;
partial/missing needs still require an owner volume/scope decision before
data-consuming build work starts.

### Constructed-scenario manifest (#103)

The same [manifest](../../docs/reference/research/retrofit-synthetic-data/scenario-manifest.json)
v0.2.1 records the offline iteration's exact eleven profiles, nine workflows,
required paths, safe endpoints/unknowns and partial IA provenance. All twenty
full journeys are explicitly unavailable for this slice; existing API or
navigation checks do not imply represented journeys or approved deferrals.
The existing three-case `152-ia-v1` recipe is retained, with SHA-256 source
bindings, exact role/profile defaults, ordered IDs/counts and null selection.
No new resident/home fixture, registry or scale regeneration is introduced.

`synthetic.scenario_manifest.validate_manifest(manifest, repository_root)`
reads only the fixed public recipe/IA/test files and inventory metadata.
It raises actionable `ValueError` on omissions, duplicates, substitutions,
malformed metadata, stale hashes/defaults/inventory or unsupported status
promotions. It never reads runtime `ZF_DATA` or private stock. This contract
deliberately refuses represented/deferred against the current partial IA
evidence; future evidence needs a reviewed manifest and validator update.
Hashes detect reviewed-source drift, not arbitrary identifying content.
The source inventory describes provisional product roles and PRD-proposed
constructed journeys, not approved company roles or customer/owner decisions.
The `inventory_authority` contract records that distinction and absent approval
separately from coverage; missing, promoted or substituted authority metadata
fails validation. This corrects v0.2.0's approval overclaim without establishing
independent acceptance; final-head review remains required.

From `src/core`, run the smallest combined contract suite:

```bash
PYTHONPATH=tests python3 -m unittest test_scenario_manifest test_needs_inventory -q
```

Core CI discovery runs these tests automatically. Coverage includes destructive
metadata mutations and exact PRD/chat-perspective inventory cross-checks.
The [criterion audit](../../docs/reference/research/retrofit-synthetic-data/README.md#constructed-scenario-manifest-acceptance-audit-2026-10-17-103)
separates completed metadata acceptance from unknown operational owners,
pending owner ratification, full journey execution and CON-007 application
acceptance. No production workflow, API, browser or authority behavior changes.

### Generator coverage baseline (#167)

From the repository root, inspect the public routing metadata without reading
datasets or generating files:

```bash
python3 -m zava_forward.core.synthetic.coverage \
  docs/reference/research/retrofit-synthetic-data/needs-inventory.json
```

### Stock fabric and case references (#168)

Inventory row SN-01 remains partial. This iteration reuses PR 246's
`stock-fabric-v1` draw algorithm and seed 4820260930, moved into
`zava_forward.core.synthetic.stock_fabric`; it does not generate a second
stock register. The retained builder and EPC generator now import installed
core. Install with pip before invoking those support tools.

```bash
python3 -m zava_forward.core.synthetic.stock_fabric \
  --register /private/path/private-north-east-stock-register.csv \
  --cases /private/path/zavaforward.json \
  --seed 4820260930 --as-of 2026-10-16 \
  --out /private/path/new-stock-fabric-snapshot
```

Without explicit paths, the register is `private-north-east-stock-register.csv`
and the new snapshot is `stock-fabric/` under `ZF_DATA` (or
`~/.zava-forward/data/`). `ZF_DATA` can be a directory or the runtime seed file;
a file selects its parent. The CLI refuses repository destinations, symlinks
to them and nonempty snapshots. It checks the resolved destination and its
ancestors for `.git` files or directories, including when installed outside
a checkout and when the snapshot directory does not exist yet. It validates
inputs before creating output.
Snapshots contain `stock-fabric.csv`, `summary.json` and, with `--cases`,
`linked-cases.json`. No generated output belongs in git or an image.

The CLI receipt (`summary.json`) records seed, algorithm version, full source
revision, payload hashes, an optional strict ISO `--as-of` and `input_sha256`
for the exact register and optional case bytes consumed. Logical keys
`register`/`cases` contain hashes only, never paths or source content; `cases`
is absent without `--cases`. Omitted as-of is `null` (unknown), not the clock.
The date is a snapshot label, not a filter, survey date or assertion that
operational evidence is current. Changing only that label leaves CSV/linked
case bytes unchanged. BOM, line endings or JSON whitespace change input
fingerprints even when parsed values and generated payloads stay identical.
Replay requires the same input bytes, seed, source dependencies and Python
runtime; seed/date alone cannot reconstruct external stock or case history.
The fabric algorithm and existing linked-case behavior remain unchanged.

Refs #176: the offline audit proves repeated bytes for fabric, EPC, the public
pack, fixture-backed programme data and both sensor modes. The original
OSM-anchored register generator and pinned source inputs remain unavailable:
the constructed 60,000-home regression is not its reproduction. Historical
manifests are not regenerated. See the
[criterion-by-criterion audit](../../docs/reference/research/retrofit-synthetic-data/README.md#offline-acceptance-audit-2026-10-16-refs-176);
the issue remains partially delivered.

Every fabric row carries `fabric_is_synthetic=true` and `is_synthetic=true`.
Build year/age band, dwelling type, construction and heating are modelling
assumptions, not company facts, survey results or EPCs. Summary weights/counts,
seed, v1 draw version, source revision and payload SHA-256 hashes are recorded.
Core revisions use full SHA-256; retained support manifests retain their
16-hex revision shape and now include the moved core dependency sources.

`resolve_cases` and `link_report` account for every case. Valid identifiers are
opaque nonblank strings without outer whitespace; no coercion or fuzzy repair.
Missing/invalid/not-found/ambiguous anchors produce explicit unlinked reasons.
Duplicate/invalid case IDs fail rather than collapse rows. Bulk fabric
generation rejects duplicate/invalid stock IDs. Each `case.stock_link` gives
`case_id`, nullable `stock_home_id`, status/reason, `shared_anchor`, synthetic
label and non-unit scope. A unique register reference is not verified dwelling
identity. Legacy `distinct_stock_homes` and `stock_homes_shared_by_cases` count
source anchors, not dwellings. Shared anchors stay explicit and valid as source
references; they never transfer consent, approvals or household identity.

`attach_fabric` refreshes only derived stock linkage/fabric, discards prior
derived `stock_epc` so it cannot outlive a changed link, and leaves operational
home fields, histories, consent and approvals unchanged. The retained builder
then rebuilds its synthetic EPC block for uniquely matched source rows; the
standalone CLI does not rebuild EPCs. Original input files are never overwritten.
Top-level reports remain seed metadata; per-case evidence survives existing
JSON-body SQL persistence without schema changes. Existing populated stores
are not reseeded or migrated automatically.

`tests/test_stock_fabric.py` verifies a connected fictional 60,000-row register
and retained 980-case builder, pre-move v1 golden values, diagnostics, CLI safety,
byte-level reproducibility, revision sensitivity and closed SQLite restart.
This is local engineering evidence only: actual private corpus reproduction,
owner inventory approval, unit reconciliation and real AI/SQL Server/Azure/human
application acceptance remain unverified. AI configuration and human
approval/resident-consent gates are unchanged; this data tool grants no authority.

### Coverage baseline results and limits

The deterministic JSON report includes every need, coverage totals, child
issues or justified deferrals, convention declarations and pending owner items.
Covered needs require delivered closure, and delivered closure requires covered
coverage. Invalid IDs, duplicate rows/references, blank rationale, malformed
issues, missing declarations or contradictory coverage/closure fail with a
nonzero exit and no JSON report. Missing needs and deferred closures instead
appear in `open_gaps` with a JSON report and exit 1, even with a child route or
deferral rationale. Partial needs with child routes do not trigger that exit.
`tests/test_generator_coverage.py` owns these semantic checks and CLI regressions;
the existing generator/determinism tests retain their output-contract checks.

`routing_shape_validated=true` means only metadata shape and consistency passed;
it replaces the overbroad `routing_validated` field. Issue existence is explicitly
`issue_existence=not-assessed`: a well-shaped reference such as `#99999` is
accepted without proving it exists. No GitHub lookup or complete issue registry
is used, and exit 0 is not evidence that child issues exist or are delivered.

Inventory v1.3.0 has two covered and eleven partial needs, with no missing
rows. A well-shaped route is not proof that the child exists or is delivered,
that generated records meet every convention, or that the owner approved scope. In particular,
the scale fixture's homes/events use a synthetic manifest label rather than
per-record `is_synthetic=true`; the inventory's universal declaration is not
fully evidenced. This tool does not change those historical snapshots.
Private regeneration, owner mapping/volume decisions, full SQL-scale tests,
real AI/Azure and human acceptance remain separate gates. Existing human
approvals, resident consent and AI release controls are unchanged. Dataset
generation still uses the existing tools and `ZF_DATA`, not this metadata CLI.

* Evaluation dataset registry (`src/agents/evals/registry.json`) lists every golden and
  evaluation dataset with version, owner and purpose; a test fails for an
  unregistered file in any `src/<project>/evals/` folder. The stock-scale fixture (60,000 homes, 600,000
  events, wholly fictional, seeded) is rebuilt with
  `python3 -m zava_forward.core.synthetic.scale_fixture` (moved in M3), writes to
  `scale-fixture/` under the per-user `ZF_DATA` folder (default
  `~/.zava-forward/data/`, outside the repository) and is never committed. Dataset owners are
  an open owner decision.
* Chat and memory fixtures (#172): `PYTHONPATH=src/agents/tests python3 -m
  chat_fixture` (test support, moved to `src/agents/tests` in M3) writes seeded, labelled-synthetic personas
  (two per PRD perspective, mapped to existing app roles), threads, memory
  items, opt-in states, exclusion probes, and isolation, expiry and deletion
  cases to `chat-fixture/` under the `ZF_DATA` folder. Case IDs come from the
  60,000-home stock. Retention is an illustrative 90 days, not a policy
  (BRD OD-45/OD-46 open); expectations are targets for #160 to #164.
* Sensor backfill (#177/#183): `python3 -m zava_forward.core.synthetic.sensor_backfill
  --estimate-only` prints the volume and size estimate for two years of hourly
  temperature and humidity across all 60,000 homes (about 1.05 billion rows,
  about 118 GiB as CSV, measured on a 20-home sample); `--homes N` writes
  sharded CSV, `sensors.csv`, `estimate.json` and `manifest.json` (seed,
  versions, climate source, parameters, hash) to `sensor-backfill/` under
  the `ZF_DATA` folder. Same seed gives identical bytes. Every row is
  `SYNTHETIC` with a stock home ID and a deterministic sensor ID; `load_into()`
  validates and appends idempotently on sensor ID plus reading ID, and
  `SQL_DDL` is the Azure SQL schema. Climate remains a labelled synthetic
  model unless the explicit paired-climate mode below is supplied.
  The [online source comparison and criterion audit](../../docs/reference/research/iot-sensor-analytics-research-plan.md#historical-climate-evidence-2026-10-17-refs-178)
  now records official metadata/terms, a conditional regional HadUK-Grid
  context recommendation and retrieved Durham monthly temperature statistics.
  CEDA humidity access remains login-blocked. The 2026-10-27 owner decision
  approves the alternative ERA5 candidate for synthetic demonstration only,
  not production/legal qualification or physical calibration.
  The legacy `load_into()` is not the authoritative #110 admission path;
  use `load_with_consumer()` for verified composed snapshots and independently
  supplied policy/controls and available cases.
### Register-backed sensor history (#177)

The following three component descriptions preserve their original independent
delivery boundaries. Their approved opt-in integration is described below.

The #179 exercise component is `synthetic.indoor_projection`. As of 2026-10-27,
`indoor-projection-exercise-v2` and `indoor-projection-composed-exercise-v2`
replace v1's fixed 8 C floor and 15..98% RH clips with per-outdoor-record,
dwelling-derived nominal envelopes. Both paths use the same calculation.
Every factor, schedule, coefficient, noise scale and tail cap is an exercise
assumption, not calibrated building physics. `PARAMETERS` and
`COMPOSED_PARAMETERS` record equations, noise policy and envelope derivation
in manifests. The supported outdoor input domain (-80..60 C, 0..100% RH,
known fabric factors) remains an API guard, not measured climate bounds or a
healthy-home threshold; invalid inputs raise `ValueError`.

For each supplied outdoor pair, let `L` be the dwelling/age/construction loss
with its applicable retrofit factor. The noiseless indoor temperature is
`B = setpoint + min(0,(outdoor-5)*0.08*L) + max(0,(outdoor-16)*0.35)`.
Model vapour `V = sat(outdoor)*outdoor_RH/100 + moisture*L`, divided by the
ventilation multiplier on the moisture term in composed mode. The saturation
equation is `sat(T) = 6.112*exp(17.62*T/(243.12+T))` hPa; these coefficients
also remain exercise values. Temperature and RH residuals are Gaussian draws
with exercise standard deviations 0.3 C and 1.5 percentage points, each capped
at +/-3 standard deviations. This tail cap is a selected exercise policy,
not an empirical confidence interval.

Nominal temperature therefore lies in `[B-0.9, B+0.9]` C. Since saturation
pressure increases over the supported indoor range and `V >= 0`, nominal RH
lies between `100*V/sat(B+0.9)-4.5` and `100*V/sat(B-0.9)+4.5`, with each
endpoint limited to the physical RH domain 0..100%. Saturation can reach 100%;
there is no replacement fixed exercise humidity floor or ceiling. These bounds
are causal functions of each actual outdoor pair and dwelling/household input,
not typed historical extrema. CSV rounding can differ from an endpoint by
0.005. Injected faults are deliberately outside the nominal-bound guarantee.

Tests traverse all 17,544 paired hours of the pinned public Durham ERA5
record through both generator paths for two synthetic dwelling forms, with
explicit household conditions and a dated synthetic retrofit, independently
checking each row's envelope. Endpoint, forced-tail, saturation and exact
equation/RNG tests supplement that record-specific evidence. Default outdoor
inputs remain the labelled synthetic seasonal series; the approved paired
history requires the explicit climate mode below. This establishes
model-consistent exercise bounds, not measured indoor plausibility, safety,
building-physics calibration or operational acceptance.
The two Gaussian draws retain their order; v2 intentionally changes nominal
values where v1 clipped or an uncapped tail escaped. Source fingerprints bind
the helper. Old snapshots remain unchanged and require their original generator
revision for replay; they are not silently migrated.

Snapshot versions also advance for these intentional row changes: default
`sensor-backfill-v3`, register `sensor-backfill-stock-v2`, paired-climate
`sensor-backfill-integrated-v2`, and non-composed fault output
`sensor-backfill-faults-v2`. The fault snapshot records
`fault_model_version=sensor-fault-packets-v1`; its packet algorithm, truth
version and reading schemas are unchanged. Fault-enabled composed output uses
the integrated v2 snapshot version. Loaders admit only current versions and
exact current-revision replays; historical snapshots require their original
generator revision/runtime, not relabelling or automatic migration.

The versioned golden in `tests/test_synthetic_determinism.py` pins default v3
with projection v2. For its seed183, 12-home, three-day fixture, the reading
SHA-256 changes from
`657ff373107807b34bd4bb6720dec534fcef13134292c5d753ef24bdbd723549` to
`25bb5259d89554560e179ae5412f3148595c47a87def9ee2fca61518e18ded5b`.
Scale payload and sensor-register goldens remain unchanged. This is a new
generator baseline, not approval to refresh or overwrite published datasets;
follow the [snapshot version and refresh policy](../../docs/reference/research/retrofit-synthetic-data/README.md#determinism-manifests-and-refresh-policy-2026-10-15).

The #180 stacked `synthetic.retrofit_effects` component is deliberately not yet
wired into the writer. It accepts explicit synthetic `Measure` records with
stock home ID, unique measure ID, supported kind and recorded whole-second
UTC completion time. `apply_loss(baseline, home_id, at, measures)` multiplies
fabric loss only for that home from `at >= completed_at`, inclusively.
Version `retrofit-effects-exercise-v1` assumes Loft insulation 0.90,
Cavity wall 0.85, Solid wall insulation 0.80 and Glazing 0.95. All are
exercise values, not measured savings or promised humidity improvements.
Multiple records multiply in canonical time/ID order; duplicate IDs,
unsupported kinds, invalid timestamps or non-synthetic claims raise
`ValueError`. Missing history has multiplier 1.0, not proof of no works.
No completion dates or private #173 records are invented. Actual source
mapping, #179/#183 integration and before/after history acceptance remain open.

The #181 stacked `synthetic.household_conditions` component models fictional
variation, not inferred resident behaviour. `profile(home_id, seed, choice,
is_synthetic=True)` draws independent equal-choice heating and occupancy
patterns; Uniform[18,22] C setpoint, [0.8,1.2] ventilation multiplier,
[0.8,1.6] hPa occupied moisture, [0.2,0.8] hPa drying increment and a uniform
UTC drying hour. All are exercise distributions, not company facts.
`conditions(..., timestamps, is_synthetic=True)` returns canonical UTC
conditions; absent-time moisture is 0.4 hPa and off-schedule setpoint is 16 C.
The versioned `DISTRIBUTIONS` records schedule boundaries. Variable occupancy
uses seeded Bernoulli(0.5) per UTC hour; subset runs agree with full windows.
Declined/unknown monitoring produces no profile, conditions or RNG draws;
these fictional choices are not real consent or activation authority.
No demographic inputs, resident assessment or attribution are used.
The writer still uses its legacy schedules until #179/#183 integration;
no full household-model history or resident choice approval is claimed.

The explicit `--register` mode (`sensor-backfill-stock-v2`) reuses merged
`stock-fabric-v1`, seed 4820260930, rather than drawing unrelated dwelling
attributes or treating the scale fixture as the private stock. Supply a wholly
synthetic CSV with `synthetic_home_id`, `is_synthetic=true`,
`building_form_osm`, `locality_theme` and `monitoring_consent`. Building form and
locality use the same defaults as the fabric generator when absent. Monitoring
choices are exactly `granted`, `declined`, or `unknown`; missing/blank is unknown.
These are fictional fixture choices, never real resident consent or permission
to activate devices. Other columns are discarded, not copied or fingerprinted.
Do not supply private resident/device data.

Both estimate and write require explicit positive `--homes N` no larger than
the register. IDs are unique opaque strings, sorted before selecting the first
N, then monitoring choices are applied. Excluded homes are not replaced by
other opted-in homes. Declined and unknown homes have no sensor or readings;
an all-excluded subset produces zero-count metadata and an empty sensor CSV.
Coverage records register/selected/unselected/monitored counts, every selected
ID and each exclusion reason. Register anchors are not verified stock-unit IDs.

```bash
python -m zava_forward.core.synthetic.sensor_backfill \
  --register /private/synthetic-fixtures/stock.csv --homes 12 \
  --days 730 --as-of 2026-10-15 --estimate-only
python -m zava_forward.core.synthetic.sensor_backfill \
  --register /private/synthetic-fixtures/stock.csv --homes 12 \
  --days 730 --as-of 2026-10-15 \
  --out /private/synthetic-fixtures/new-sensor-history
```

Outputs must be outside any repository and in a new/empty nonsymlink folder.
`estimate.json` is written before reading shards, measured from up to 20 of the
actual granted sensors. The estimate includes dropout; it is not a guaranteed
upper bound or SQL storage quote. No full-stock write is an implied approval.
Manifest metadata records normalized allowlisted register SHA-256, source
fingerprints, fabric/adapter versions, window, coverage and all payload hashes.
`stock-fabric.csv` preserves selected v1 fabric plus fictional monitoring choices.
Changing only an ignored column or CSV row order does not change output.

The projection reuses the existing equations: loss = dwelling factor * age
factor * construction factor. Stock build year selects the existing age bucket.
Construction factors are Solid brick 1.15, Stone 1.20, Cavity brick 1.0,
precast concrete 1.10, Timber frame 0.90, partial-fill cavity 0.85 and full-fill
cavity 0.75. Heating schedules are seeded equal-choice morning/evening, all-day
or low; they are variation fixtures, not judgements of residents. All factors
and bounds are exercise assumptions, not calibrated physics or climatic facts.
The shared indoor equations are in `indoor_projection.py`; basic fault rates
remain in `sensor_backfill.py`, and construction factors and exact fabric
mappings are in `sensor_stock.py`.
No dated measure history is supplied: `retrofitted=False` is a modelling
assumption, not evidence that no works occurred, and no before/after claim follows.

Stock sensor IDs now use `stock-sensor-v2`: `S` plus ten uppercase Base32
SHA-256 characters from the entire canonical home key. A collision stops
generation; it never reassigns a home ID. Eleven-character keys leave room
for the existing `UNMAPPED-` fault namespace. Reading IDs append epoch seconds.
Home IDs preserve case and Unicode and must fit 128 UTF-16 code units. For a fresh
SQL Server database apply `STOCK_SQL_DDL` (`stock-reading-v1`, sensor
VARCHAR(73), reading VARCHAR(96), home NVARCHAR(128)), then call
`load_into(conn, output, create_schema=None)`. Legacy `SQL_DDL` and CSV field
layouts are unchanged; v2 projection values can differ. Do not use the narrow
legacy DDL for stock mode. The loader
does not migrate databases. SQLite tests and portable conditional-insert checks
do not prove live SQL Server execution.

This remains bounded synthetic #177 delivery: child issues are not automatically
closed or owner-deferred. Actual private-stock equality, measured physical
calibration, real monitoring authority and production acceptance are unproved.
No CO2/energy is generated.
The opt-in fault/truth feature for #182 is described below; it does not close
the parent's other child or live-platform acceptance.
No AI review, hazard diagnosis, ranking change, resident action or approval
occurs in the generator. Existing AI release/human gates are unchanged.

### Approved paired-climate composition (2026-10-27, Refs #177)

The owner approved candidate climate reuse for synthetic demonstration under
`owner-approvals-2026-10-27-b`. The pinned
[2023-2024 ERA5 input and metadata](../../docs/reference/research/climate-paired-source-178/open-meteo-era5-durham-2023-2024-metadata.json)
contain 17,544 genuine hourly pairs for a Durham grid cell. Temperature
[-5.3, 26.9] C and RH [36, 100]% are calculated sample extrema, not safety or
regional design thresholds. Open-Meteo/C3S attribution, retrieval/hash, source
resolution, historical terms and the limited owner approval are retained.
The NASA 2023 sensitivity sample is separate, never used to fill the second year.
The strict adapter rejects gaps, mismatches and invalid units/values; exact UTC
subsampling does not fill or repeat weather records.

```bash
python -m zava_forward.core.synthetic.sensor_backfill \
  --register /external/generated-stock.csv --homes 60000 \
  --climate docs/reference/research/climate-paired-source-178/open-meteo-era5-durham-2023-2024-raw.json \
  --climate-metadata docs/reference/research/climate-paired-source-178/open-meteo-era5-durham-2023-2024-metadata.json \
  --days 730 --as-of 2025-01-01 --cadence 1440 --estimate-only
```

Use the same arguments with `--compress --out /external/new-history` to write
deterministic gzip shards. Cadence 1440 is a declared daily exercise, not hourly
or diurnal-scale validation. Default hourly capacity is estimated independently.
`--measures /external/measures.json` accepts a JSON list of explicit
`measure_id`, canonical `home_id`, supported `kind`, UTC `completed_at` and
`is_synthetic=true`. Empty history is neutral, not evidence that no works occurred.
No dates, consent or calibration are inferred from the stock.

Composed projection is separately versioned: baseline dwelling/age/construction
loss is multiplied by active dated measures; household setpoint affects indoor
temperature, and household moisture divided by ventilation affects vapour.
Both projection paths now use the v2 derived envelopes described above;
noiseless equations and RNG draw order are retained, not v1 output values.
All model coefficients/distributions are exercise assumptions. Manifest hashes
bind climate/metadata, stock, explicit measure history, source revisions, seed,
window, cadence, payloads and model versions. No operational approval claim
follows from generated readings.

Composed output uses the existing 13-field consumer schema. Clean mode has no
fault labels; optional `--fault-rate NAME=RATE` keeps evaluator-only packet truth
under `truth/`, separate from `analysis/`, including compressed truth when selected.
`load_with_consumer(consumer, output, stock=..., climate=...,
received_at=..., measures=..., fault_rates=...)` first reconstructs and verifies
the exact current synthetic snapshot within its explicit row budget, then calls
the real `SensorConsumer`. Before creating replay scratch or writing output, it
requires the manifest home count to match the supplied stock's actual granted
count and budgets nominal rows from that count and the requested time slots.
The stock metadata count must also fit the budget, even with zero granted homes.
Fault-expanded rows remain bounded by the post-reconstruction and delivery guards.
Existing independent policy, available cases, mapping,
consent, calibration, units, clock, range, ordering and replay checks still apply.
The loader never creates cases or grants controls. Export accepts 128-unit home
keys, but consumer availability remains bounded to the shared SQL case model's
64 UTF-16 units on both stores. Longer or absent keys produce `HOME_UNAVAILABLE`;
undersized/non-Unicode legacy SQL reading columns fail explicitly instead of
truncating. This is not a shared case-schema migration or real monitoring activation.
`tests/test_sensor_stock.py` covers bounded 730-day histories, fabric/ID/choice
reconciliation, byte reproducibility, bounds, estimates, hashes and local loads.

### Opt-in sensor fault packets (#182)

Repeat `--fault-rate NAME=RATE` on the existing sensor-backfill command. This
reuses the same stock adapter, home/sensor identities, fictional monitoring
choices, outdoor model and indoor equations; it does not create another stock.
Omitting every `--fault-rate` preserves historical CSV bytes and legacy embedded
labels. Opting in disables those historical implicit faults and uses the new
`sensor-fault-input-v1` schema. To generate a clean valid control in the new
schema, use `--fault-rate gap=0`.

```bash
python -m zava_forward.core.synthetic.sensor_backfill \
  --register /path/to/wholly-fictional-stock.csv --homes 5 \
  --days 4 --cadence 60 --as-of 2026-10-17 --seed 7 \
  --fault-rate outlier=0.08 --fault-rate stuck=0.08 \
  --fault-rate drift=0.08 --fault-rate gap=0.08 \
  --fault-rate duplicate=0.08 --fault-rate out_of_order=0.08 \
  --fault-rate unmapped=0.08 --fault-rate wrong_unit=0.08 \
  --fault-rate clock_skewed=0.08 --fault-rate uncalibrated=0.08 \
  --out /path/to/new-synthetic-fault-snapshot
```

API: `write(path, stock=selection, days=4, seed=7,
fault_rates={"duplicate": 0.1, "gap": 0.1})`; `estimate()` accepts the same
mapping, and `--estimate-only` uses the same injected row generation. Rates must
be finite in [0, 1], with sum <=1; unknown/duplicate option names are errors.
Each rate is a probability per consecutive two-observation packet, not an
independent per-reading probability or guaranteed quota. One exclusive class
applies to both observations; the remainder is `valid`. An even number of at
least two nominal observations per monitored home is required. Invalid rates
or windows fail before creating output. Canonical class order and a separate
seed/sensor RNG make assignments independent of option order, sampling and
shard boundaries. Reproduce with the same Python runtime and inputs.

All following magnitudes are fictional exercise values, not calibration,
scientific bounds, anomaly thresholds or operational rules.

| Class | Observable injected input |
| --- | --- |
| valid | Original nominal values, degC/percent, calibrated=true |
| outlier | Add 25 C to each temperature, without clipping |
| stuck | Hold first packet temperature and humidity for both observations |
| drift | Add 0.05 C times the one-based nominal slot index across that sensor's series |
| gap | Omit both observations; retain both in evaluator truth |
| duplicate | Emit each observation twice with identical sensor/reading identity |
| out_of_order | Deliver second observation before first, preserving IDs and observed timestamps |
| unmapped | Prefix the sensor ID with UNMAPPED-, absent from the sensor register |
| wrong_unit | Convert temperature to Fahrenheit and declare temperature_unit=degF |
| clock_skewed | Advance observed_at by 24 hours; preserve reading ID and clean time in truth |
| uncalibrated | Set calibrated=false on both observations |

The new snapshot has two sibling directories:

* `analysis/`: CSV shards, sensor register without `fault_profile`, sanitized
  stock fabric when selected, estimate and manifest. Readings have explicit
  `temperature_unit`, `humidity_unit` and `calibrated`; no `injected_fault`.
  For compatibility with the existing observation shape, the numeric column
  remains named `temperature_c` even in a wrong-unit packet: consumers must
  inspect the declared unit before interpreting it. Schema/version are explicit.
* `truth/`: evaluator-only JSONL shards and manifest with canonical rates,
  exercise magnitudes, seed and clean nominal packets. Each packet records its
  label, sensor, packet index, analysis shard and zero-based emitted data-row
  positions (headers excluded). Gaps have empty positions; duplicates have four.
  The truth manifest hashes its payloads and binds the analysis manifest hash.

Point analysis only at `analysis/`, never recursively at the snapshot root;
give `truth/` only to an evaluator after analysis. Analysis metadata contains no
rates, class labels, clean counterfactuals, fault profiles or truth-file links.
This is file/interface separation, not an OS access-control boundary; operators
must restrict evaluator files appropriately. Per-file hashes authenticate bytes,
not scientific validity. No real device/resident data is accepted or generated.
Declined/unknown homes still emit no sensors, observations or truth packets.
Outputs must be outside repositories and new/empty nonsymlink snapshots.

The existing `load_into()` intentionally refuses these snapshots or their
analysis directory before changing a database. Legacy DDL/loaders do not
understand the new unit/calibration contract; no migration is implied. #183/#110
own future ingestion checks. AC-066's seven input classes are fixture-covered,
not live IoT Hub/SQL/AI acceptance. AC-067/068 analytics, scientific method
approval, resident monitoring and human review rules remain unchanged.

`tests/test_sensor_faults.py` covers each forced class, valid controls, seeded
packet frequencies, complete multi-sensor/multi-shard truth joins, no embedded
answers, snapshot safety, hashes and tiny installed-module CLI replay. Local
2026-10-17 evidence: 15 deliberately broken in-memory variants were detected;
a five-home fictional selection produced 292 delivered rows and 144 truth
packets across all 11 classes, with byte-identical reruns. These are synthetic
engineering results, not real-device or predictive-performance evidence.

### Synthetic scenario validation pack (#190, #192, #193, #194)

The installed `synthetic.sensor_scenarios` module generates a separate bounded
exercise pack; it never appends to general history or reads private stock,
resident data or installed devices. It reuses clean `sensor_backfill.readings()`
and the shared observation schema. Profiles are explicit fictional overlays,
not calibrated building physics or the beneficial-only dated fabric-loss model.
Default backfill bytes and workflow/check names are unchanged.

`sensor_scenarios.retrofit_exercise_scenarios()` gives #111/#133 consumers the
four before/after retrofit cases (improvement, no change, delayed effect,
adverse effect) as analysis rows, a measure date and expected direction/size,
each labelled `EXERCISE VALUE: fictional, not sourced`. Only fixture tests use
it today; #111/#133 consumer tests remain unproven.

From the repository root, with the core package installed:

```bash
python3 -m zava_forward.core.synthetic.sensor_scenarios \
  --seed 190 --out /external/new-sensor-scenarios-190
cd src/core
python3 -m unittest discover -s tests -p test_sensor_scenarios.py -v
python3 -m unittest discover -s tests -p test_sensor_retrofit_consumer_contract.py -v
python3 -m unittest discover -s tests -p test_sensor_damp_consumer_contract.py -v
```

`test_sensor_retrofit_consumer_contract.py` is the reusable fixture contract
for the later #111 and #133 consumer tests: observation-only before/after
deltas classify the four retrofit profiles using labelled exercise tolerances.
It is not those consumers and not an operational rule.

`test_sensor_damp_consumer_contract.py` does the same for the seven damp cases:
observation-only derivation is reproducible, missing or faulty data is
`INSUFFICIENT` and never ranks below a no-signal result, and a resident report
always routes to human investigation whatever the sensors read (labelled
exercise oracle, not the #111 or #133 implementation).

Choose a genuinely new external path, not the literal example if unavailable.
The CLI rejects repository/worktree destinations, symlink components, files and
nonempty folders. Same seed, sources and Python version reproduce identical
bytes. `--seed` is an integer 0..2^63-1 (default 190); `--out` is required.
`--humidity-threshold` changes the exercise comparator's RH percent threshold
(finite 0..100, default 75), not the fixed expected labels. Exit 0 means every
listed exercise outcome/delta check matched, 1 means checks failed (report is
retained), and 2 means invalid input or an I/O failure. There is deliberately
no single overall pass field.

| Parameter or profile | Exercise definition |
| --- | --- |
| Window/cadence | 2024-01-01 inclusive to 2024-01-29 exclusive, hourly UTC; 672 nominal observations/case |
| Baseline | 20 C, 55% RH plus 0.15 times centred weekly clean-backfill residuals, repeated weekly |
| Weather | Constructed constant 2 C/70% outdoor RH; not the separately retained ERA5 data |
| Normal | Baseline; expected NO_EXERCISE_SIGNAL |
| Condensation-prone | -5 C/+37 RH points; expected REVIEW_CANDIDATE, not proof of surface condensation |
| Sustained high humidity | +27 RH points; expected REVIEW_CANDIDATE |
| Repeated overnight peaks | +30 RH points at UTC hours 00..05; expected REVIEW_CANDIDATE |
| Sensor fault | Both channels held at 20 C/55% for first 48 hours; expected INSUFFICIENT |
| Missing data | Retain only every fourth nominal hour (75% missing); expected INSUFFICIENT |
| Seasonal shift | Linear -2 C/+8 RH points across the window; expected NO_EXERCISE_SIGNAL |
| Retrofit improvement | From day 14: +2 C/-10 RH points |
| Retrofit no change | Recorded completion day 14, zero temperature/RH step |
| Retrofit delayed effect | Recorded completion day 14; from day 21: +1.5 C/-6 RH points |
| Retrofit adverse effect | From day 14: -1 C/+8 RH points |

These are hand-designed tests, not observed performance, prevalence, a safety
threshold, evidence of completed works, resident behaviour or a savings promise.
The linear seasonal case is an exercise trend, not historical climate validation.
Air temperature/RH alone cannot establish surface condensation or mould.

Point any analysis only at `analysis/`:

* `analysis/C01.csv` through `C11.csv` use the exact 13-field
  `sensor-fault-input-v1` contract. All have `source_type=SYNTHETIC`,
  `scenario=SCENARIO_PACK` and the common actual pack seed. Neutral identities
  and that seed are never used as classification features. No labels,
  expected outcomes, injected-fault columns or RNG keys are present.
* `analysis/windows.json` holds neutral case/file IDs, the common UTC window,
  cadence and a completion instant for the four retrofit cases. It exposes
  no outcome, size or delayed activation time.
* `truth/cases.json` holds evaluator-only labels, actual seed/RNG stream keys,
  expected outcomes, exercise deltas and delay. `truth/report.json` holds
  per-case checks, observed statistics, confusion and sensitivity.
* `truth/manifest.json` binds all relative payload hashes, generator/comparator
  versions, source fingerprint, Python version, seed, weather and parameters.
  The report separately hashes only its analysis inputs. No absolute path or
  current wall-clock time affects payloads.

This is interface/file separation, not OS access control. Restrict truth access;
do not give the evaluator directory to an analysis process. General backfill
loaders are not scenario importers; no case/control/consent records are granted.

The observations-only exercise comparator checks the exact UTC hourly grid,
order, uniqueness, units, labels, calibration and finite exercise domains
(-10..45 C, 0..100% RH). It requires >=90% valid coverage in the whole window,
each UTC day and each UTC overnight [00:00,06:00), and rejects >=24 consecutive
identical paired samples as a flatline. Missing slots break persistence runs.
Invalid/inadequate data yields INSUFFICIENT with reasons and null means.
Otherwise >=12 consecutive hours at/above the RH threshold, or >=3 nights
each with >=3 high-RH overnight samples, yields REVIEW_CANDIDATE.
NO_EXERCISE_SIGNAL is not an assurance of a healthy or safe home. Freshness
against an operational clock and approved thresholds remain #111 work.

Confusion uses seven damp cases, one case per trial: five binary-eligible
cases and two expected-insufficient cases. TP/TN/FP/FN use only binary
predictions; unexpected insufficiency is an explicit abstention, not a true
negative or silently removed eligible case. Expected-insufficient results
have separate correct/incorrect counters. Rates state their classified
denominators and are null when not computable. Sensitivity reruns 70/75/85%
against the same truth, so the 85% setting exposes misses.
The four retrofit cases are excluded from binary confusion.

Retrofit comparisons show independent counts/coverage and means for baseline
[day0,day7), early [day14,day21) and late [day21,day28), with per-window
sufficiency and null deltas on insufficient input. The first early sample is
the completion instant; the first late sample is delayed activation.
Each early/late delta is checked separately against its exercise target
within 0.02 C/RH points. Matched weekly cycles isolate the constructed step;
they do not establish causal weather adjustment for real homes.

### Two-stage simulator operation and limits (#194)

Run the credential-free validation from `src/core` after installing the core
distribution with pip:

```bash
flock -w 600 /tmp/ama-rpi-heavy.lock \
  python3 -m unittest discover -s tests -p 'test_sensor_*.py' -v
```

Verbose unittest output reports each check independently, including failures
and skips; a skipped SQL integration is not a pass. Existing Source CI discovers
these tests without a new workflow. `test_sensor_stage_validation.py` compares
365 hourly days for four declared synthetic homes (35,040 samples/stage,
seed 190, origin 2024-01-01 UTC). It asserts the stock-derived dwelling, age and
heating profiles before generation. Annual exact-row/mean/population-standard-
deviation/inclusive-quartile equality is deterministic backfill/replay parity,
not independent proof of climate accuracy. Separate per-stage checks cover
finite exercise domains (-10..45 C, 0..100% RH), annual mean/spread, January/July
structure, winter noon/midnight structure and paired flatlines, with corrupted
inputs proving that range and flatline guards fail. Every range and seasonal/
diurnal expectation is an exercise value, not a safety or healthy-home limit.
Existing plausibility/fault/replay tests retain stochastic injection-rate,
gap/duplicate, timing and pacing coverage. Composed ERA5-model continuity and
actual transport are not established by legacy-model parity.

Stage 1 is runnable through `synthetic.sensor_backfill`; estimate before writing.
The legacy, register, fault and approved paired-climate commands above describe
their distinct schemas and limits. Defaults are 730 days, 60-minute cadence,
seed 183 and a synthetic seasonal weather model. Explicit `--as-of` selects a
half-open UTC window; `--cadence` must divide 1440. Paired-climate mode requires
an explicit wholly synthetic register, complete retained hourly source coverage
and optional synthetic dated measures. Exact subsampling neither fills gaps nor
repeats years. Storage estimates are not completed full-stock materializations.

Stage 2 (#184) has a delivered shared observation contract (#186) and the
opt-in [finite replay and pacing library](#finite-synthetic-stream-replay-184)
with an [API SDK publisher](../api/README.md#opt-in-iot-consumer-and-synthetic-publisher-110-184).
The scenario pack does not invoke that publisher. Local fake-network tests
are not verified live Hub operation, approved credential lifecycle or cloud
acceptance. No provisioner or autonomous retry scheduler is added.
Separately authorized live operation must use the shared schema, stable IDs,
per-device authentication, synthetic-only identities, explicit N/rate/volume/
replay/cost limits and the independent #110 consumer controls. The declared
live exercise accounting is three paired observations/home/day: `3N` records/day,
180,000 for N=60,000; the hourly scenario pack is a separate offline test cadence.
See the [shared schema and measured-volume contract](../../docs/reference/research/iot-sensor-analytics-research-plan.md#shared-observation-contract-and-volume-2026-10-18-refs-186).
No simulator discovers, connects to or represents an installed real device.
Never put device keys/connection strings in source, generated rows or logs.

The [climate source metadata](../../docs/reference/research/climate-paired-source-178/open-meteo-era5-durham-2023-2024-metadata.json)
records Open-Meteo ERA5 Durham-grid hourly outdoor reanalysis, retrieved
2026-10-27, 2023-01-01 through 2024-12-31, input SHA-256
`af76a90414d9ad8f19dacc95a38f06d4c4321a91bdf030ba231558c42506051e`.
It is one 0.25-degree cell, not a station or indoor measurements.
Attribution: Weather data by [Open-Meteo.com](https://open-meteo.com/),
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); underlying ERA5 is
Copernicus Climate Change Service (C3S) material. Raw bytes retained unchanged;
bounds summarised and exact timestamps subsampled for synthetic projections.
Hersbach et al. (2023), DOI
[10.24381/cds.adbb2d47](https://doi.org/10.24381/cds.adbb2d47);
Open-Meteo software: Zippenfenig (2023),
[10.5281/ZENODO.7970649](https://doi.org/10.5281/ZENODO.7970649).
The metadata preserves 2026-10-22 terms snapshots, free-API non-commercial
conditions and unverified underlying C3S reuse terms. Owner approval
`owner-approvals-2026-10-27-b` is synthetic-demonstrator-only, not Legal or
production qualification. No new terms retrieval/approval occurs here.
The scenario pack uses none of those climate bytes.

All emitted indoor data is simulated, not evidence of installed devices or
real home conditions. No signal diagnoses a hazard, dismisses a resident report,
starts a clock, releases a hold, changes ranking, grants consent or creates an
approved task. Human review, resident choice and BRD OD-43 remain unchanged.
Actual #111/#133 consumer test use, verified live stage operation, competent R2 review,
agreed R3 limits and operational acceptance are still unproven.

### Existing reproducibility and plausibility evidence

* Reproducibility and refresh (#176): scale fixture v1.3.0 and sensor backfill
  v2 record seed, version, `as_of`, dependency-aware `generator_revision` and
  SHA-256 for every payload file. Both require a new or empty output folder;
  a repeat write to an existing snapshot fails without replacing files.
  Generate a new versioned destination rather than deleting live data.
  Source fingerprints are independent of Git HEAD, clock and output location;
  exact reproduction also requires the same Python/runtime environment.
  Scale `--as-of` is a snapshot label, not an event cutoff: its events remain
  calendar-year 2026 fixtures. Sensor `--as-of YYYY-MM-DD` is the exclusive UTC
  end of `--days` days; omitting it preserves the historical 2024-10-01 start
  (730 days ends on 2026-10-01). `--estimate-only` accepts the same window.
  Cadence must divide 1440 minutes and all sizes must be positive.
  Example, after setting `ZF_DATA` to a private folder outside the repository:

  ```bash
  python -m zava_forward.core.synthetic.scale_fixture --seed 174 \
    --as-of 2026-10-15 --out "$ZF_DATA/scale-fixture-2026-10-15-v1.3.0"
  python -m zava_forward.core.synthetic.sensor_backfill --seed 183 \
    --as-of 2026-10-15 --days 2 --cadence 60 --homes 12 \
    --out "$ZF_DATA/sensor-backfill-2026-10-15-v2"
  ```

  `tests/test_synthetic_determinism.py` checks every output byte, multiple
  sensor shards, source/hash metadata, window propagation, unchanged historical
  payloads and refused refreshes. This wholly fictional stock-scale fixture
  is not the private OSM-anchored stock register. That generator remains absent;
  neither these tests nor the sensor sample establishes full-stock feasibility.
  The [refresh cadence and approval policy](../../docs/reference/research/retrofit-synthetic-data/README.md#determinism-manifests-and-refresh-policy-2026-10-15)
  is still proposed. These tools confer no approval, resident consent,
  live SQL reset authority or permission to replace private tenant bindings.
* Sensor plausibility tests (#191): `tests/test_sensor_plausibility.py` runs in
  the existing MVP CI unittest step over 150 stock homes for two years. It
  fails on out-of-bounds or flat-line series, checks seasonal and diurnal
  structure and humidity by age band and dwelling, and checks that dropout,
  outlier and stuck fault rates match the configured injection. Expected
  outdoor ranges are labelled exercise values until the climate source in #178
  is retrieved and recorded (open item).

## Law store (ADR 0005, phase 1)

`src/core/src/zava_forward/core/lawstore.py` loads the dated snapshots in `docs/reference/regulatory/`
into append-only tables (`reg_source`, `reg_version`, `reg_provision`, `reg_gap`) and
writes each snapshot once, content hashed, through a snapshot interface. The target is
Azure only: `ZF_LAW_STORE=mssql` uses Azure SQL (the `ZF_SQL_*` settings of the main
store; append-only ledger tables when the database is ledger enabled, otherwise an
append-only trigger) and `AzureBlobSnapshots` (`ZF_LAW_BLOB_ACCOUNT_URL`,
`ZF_LAW_BLOB_CONTAINER`, `DefaultAzureCredential`; writes never overwrite). SQLite and a
local folder (`ZF_LAW_DB`, `ZF_LAW_BLOBS`) are local test doubles only. Seed with
`python -m zava_forward.core.lawstore REGULATORY_DIR DB_FILE BLOB_DIR` (or
`ZF_LAW_STORE=mssql python -m zava_forward.core.lawstore REGULATORY_DIR`); a changed file
becomes a new version and nothing existing is altered. Partial sources carry
`completeness: partial` and results say so. Leasehold, complaints handling, TrustMark
and licensed PAS 2035 are gaps answered as "no source held". The keyword index
(`rebuild_index`) is derived from SQL. The same suite runs on SQL Server in the CI
`mssql` job (`test_lawstore.MssqlStoreTests`). Open items: the Azure Blob container
immutability (WORM) policy and the Azure SQL deployment are infrastructure and are not
verified here; the Azure Blob client is tested only against a fake container. The
read-only viewer at `/law.html` and the source/search routes under `/api/law/`
serve staff roles with no AI; the separate [rule-card API](../api/README.md#rule-card-approval-api-211)
adds controlled exercise writes. Seeded
versions are `not_reviewed` with owner "to be named"; this is a reference copy, not
legal advice or approval. Seed metadata is `src/core/src/zava_forward/core/law/law-source-register.json`.

## Rule cards (ADR 0005, phase 2)

`src/core/src/zava_forward/core/rulecards.py` (moved from `mvp/` in M1 of #199) holds versioned rule cards in append-only tables
(`rule_card_version`, `rule_card_event`, `rule_card_review`, `rule_card_review_event`,
`rule_card_check`) with a draft, approved,
active, held, retired lifecycle. A card is drafted by the `rule_author` role and only
its named `rule_owner` can approve, activate, hold, release or retire it; an author
cannot approve their own card. Versions, approver, approval date and effective dates
are retained. `source_changed` records an open review item (RULE-021, AC-068) naming the
affected card, active version, requirements and tests, source versions and effective date,
and never alters an approved card. `assess_review` lets only the card's named owner record
the interpretation, tests, effective date, notification, rollback and any hold; it never
activates a rule, so activation still needs propose, approve and activate by named humans.
`LawStore.rules` reuses this store on the existing SQLite or SQL Server adapter.
Initialization idempotently adds the two draft exercise seeds. Public mutations
hold the shared adapter reentrant lock and a database write transaction before
version/state reads, including supersession and assessment holds; a failure
rolls back the whole mutation. SQLite uses its writer lock, SQL Server reuses
the existing cross-replica application lock. Rule IDs are explicitly allocated
inside that transaction, without SQLite-only identity syntax or pagination.
The existing SQL Server backend initializes append-only ledger tables (when
enabled) or append-only triggers. Local adapter-contract tests are not a live
SQL Server run.

Changed source ingestion now adds review records inside the same transaction as
source/provision rows. First ingestion and unchanged retries add no review.
Card contents, approval events and snapshots are never overwritten. The derived
keyword index is rebuilt after commit and repaired by unchanged retries; an
index failure does not undo already committed source/review evidence. Failed
ingestion can leave an unreferenced immutable blob; it is not deleted or treated
as approved evidence. Existing SQLite rule histories and identity strings remain
unchanged on reopen. Direct core callers remain trusted internal code; HTTP
authority is enforced by the API, never by accepting request role strings.

The card-to-requirement and test trace for the two seed cards is a static exercise map;
unmapped cards are flagged for the owner. The two seed cards (hazard awareness clock, automated decision
safeguard) remain unapproved drafts until a distinct named exercise owner acts;
any approval is explicitly simulated. They are not
law or real approval, and the owner, clock durations and citations remain open items
for named Compliance and DPO approval. The API binds separate Entra rule
capabilities to a unique provisioned identity; actual tenant assignments, human
approval of specific cards and the rule-card UI remain open. The bounded
exercise engine below does not supply those approvals.

## Source change monitoring and review (#213)

`source_monitor.SourceMonitor` extends the delivered #127 review workflow on
the #210 law store, #211 rule cards and #212 deterministic evaluator.
It is a bounded offline exercise, not a live legal monitoring service.
Juan Manuel Servera is the exercise Legal, Compliance and DPO owner.
Approval-bearing records explicitly say `simulated` and `EXERCISE ONLY`;
neither agent output nor a fixture is real human legal approval.

The store reuses the law SQL adapter, immutable snapshot store and rule-card
transaction. Four append-only tables retain configuration revisions,
observations, candidate changes and lifecycle events. SQLite triggers enforce
local append-only behavior. SQL Server uses ledger tables when enabled,
otherwise denial triggers, with the existing transaction-scoped exclusive
`zavaforward_write` application lock. Only the local adapter/SQL contracts have
been exercised here, not a live SQL Server or Azure run.

### Detection and bounded impact

`configure(source_id, cadence_days=..., likelihood=..., rationale=...,
impact=..., actor=..., role=...)` records a positive 1..366-day interval, exact
`High`/`Medium`/`Low` likelihood, the register rationale and explicit lists of
`requirements`, `journeys`, `tests` and `communications`. The source must
already exist. Configuration is owner-controlled and append-only; repeating
the same configuration is idempotent. Use the
[register](../../docs/reference/regulatory/README.md#change-assessment-and-monitoring-register)
to select the interval and rationale, including increased cadence around
commencement; the code does not guess an interval from prose or turn
likelihood into legal importance. Unconfigured sources are not monitored.

`due(source_id, today)` measures cadence from the last successful retrieval,
not the last attempt. Failures remain recorded but do not reset the timer:
a due source stays eligible for the next run, including the next day. A source
with no successful observation is always due. A successful retry starts a new
cadence interval; success is not verification. Dates before the latest attempt,
including a failed attempt, are rejected.

`observe` accepts explicit UTF-8 bytes, publication metadata, provenance,
discovery method and an exercise date, or an explicit retrieval error.
It compares hashes/metadata against the retained law-store baseline and stores
content, metadata or retrieval-failure review items, including a capped
200-line unified difference with an explicit truncation flag. Full candidate
bytes remain in a content-addressed snapshot alongside, not over, the baseline.
Missing observations are failures, not successful checks. Scraping, feed and
metadata results all start unverified. Changed bytes do not inherit the old
source's completeness; an explicit completeness assertion still requires
owner review.

Candidates never enter `reg_version`, `reg_provision` or the search index.
Detection does not alter a card or its lifecycle. Exact canonical source IDs
match cards, not source-name substrings. Each change freezes matched card
versions/states, requirements, journeys, tests and communications and links the
existing per-card review records by candidate/configuration IDs. The source
version on those reviews is the actual baseline, not an invented published
candidate version. Empty impact fields or no matched cards are explicitly
unmapped; nonempty lists establish completeness only for that bounded
configuration, not exhaustive legal impact analysis.

### Simulated owner release and rollback

These are trusted in-process functions, not an authenticated public API.
`actor="Juan Manuel Servera"` and `role=rulecards.OWNER` are exercise call
inputs, not proof of identity. No monitor approval/configuration/activation
endpoint was added; the role endpoint inventory is unchanged. Provisioned
HTTP card identities keep their existing independent author/owner boundary.

1. The distinct author drafts an immutable replacement with an executable
   contract; the named card owner separately approves it. Existing active or
   held cards can instead receive an explicit `no_change` disposition.
2. The exercise owner calls `monitor.approve` with provenance/completeness
   review evidence, interpretation, notification and rollback plans, effective
   date, every affected card's exact target and local regression cases. Failed
   or explicitly partial retrievals and incomplete impact lists cannot pass.
   Existing linked card reviews receive the corresponding simulated owner
   assessment. This does not publish a source or send communications.
3. `monitor.regress` runs the frozen cases through the existing deterministic
   evaluator after approval, retaining observed/expected results and pass/fail.
   Every configured test ID and target must be covered. Cases contain
   `test_id`, `card_id`, `facts` and `expected` result states. They are bounded
   data, not Python expressions, arbitrary commands or a Python-suite runner.
   Configured IDs identify these regression cases; listing a suite path alone
   is not evidence that that suite ran.
4. `monitor.activate` is another named-owner action. It requires the latest
   run for the exact approval to pass and refuses dates before the effective
   date, candidate date or regression. It rechecks source/configuration,
   candidate integrity, exact card histories, evaluator version and current,
   complete, reviewed citations under the transaction. A failed rerun cannot
   reuse an older pass; material observations invalidate approval even if
   bytes later revert. Harmless duplicate observations do not.
5. Replacement activation cannot supersede a human hold. A separately
   approved/regressed `no_change` decision can release that exact held card.
   Direct card `activate`/`release`, including alternate versions, cannot
   bypass monitoring once a card has a detected change.
   A newly drafted card citing a changed source also joins the gate and
   requires a refreshed observation. If a card cites multiple changed sources,
   activation fails closed: coordinated multi-source release is not supplied
   by this offline slice and one source's approval cannot stand for another.
6. `monitor.rollback` requires the same owner and a reason. It atomically
   compares the exact activation histories and restores captured eligible
   prior active versions, or retires a replacement where none was active.
   A no-change hold release can be rolled back to the captured hold.
   Intervening holds, retirements, new card versions, repeated rollback or
   expired/ineligible prior versions block rollback rather than undo later
   human decisions. All earlier versions, dates and events remain.

Ordinary unmonitored card activation now also refuses a date outside the
card's effective/retirement window, preserving the previous active version
until an eligible replacement is actually activated. Detection never delays
independent emergency, resident or hazard routes.

Publication of a candidate as a verified law-store version is deliberately
not implemented. Positive release tests use clearly synthetic reviewed
baseline provisions already held by the law store. A card citing an
unpublished candidate, stale, missing, partial or unreviewed provision cannot
pass runtime-equivalent eligibility. This offline rule-release demonstration
is not proof of activating a newly published legal interpretation.

### Acceptance audit

| Issue #213 acceptance criterion | Bounded local result | Unmet boundary |
| --- | --- | --- |
| Differences stored with affected cards, journeys, tests and communications | Met for configured fixtures: retained differences, exact card histories, source versions, impact lists, owner and linked reviews | Live discovery and exhaustive legal/journey/template impact mapping are not delivered |
| Scraping is unverified until provenance and completeness review | Met locally: discovery is unverified; simulated owner evidence is required and retained separately | No actual official provenance/currentness or human legal review is claimed |
| Detection never overwrites approved cards | Met locally: candidate isolation, immutable snapshots/cards and retained lifecycle histories | Live storage permissions and immutable Blob policy remain unverified |
| Approval, regression, effective-date activation and rollback | Met for simulated single-source existing-source executable cards, including failures, holds and atomic rollback; overlapping changed sources fail closed | Coordinated multi-source release, verified new-source publication, actual human approval, operational regression/accessibility/privacy/communications suites and live activation remain unmet |
| Configurable cadence per source | Met locally: explicit versioned intervals, due boundary and bounded orchestrator pages | No hosted regulatory timer, official adapter, missed-run alert or adaptive calendar policy is deployed |
| High/Medium/Low likelihood per register | Met as an exact validated enum with retained register rationale | No automatic register-to-runtime policy synchronization or owner ratification is claimed |

`tests/test_source_monitor.py` covers local detection, authority, provenance,
coverage, failure/staleness, effective dates, no-change/holds, actual runtime
eligibility, restart, concurrent adapters, append-only SQL contracts and atomic
multi-card release/reversal. Run from `src/core`:

```bash
PYTHONPATH="$PWD/tests" /tmp/zf164/bin/python -m unittest discover -s tests -p 'test_source_monitor.py' -q
/tmp/zf164/bin/ruff check . && /tmp/zf164/bin/ruff format --check . && /tmp/zf164/bin/mypy
```

The [offline job recipe](../orchestrator/README.md#offline-source-change-job-213)
does no scraping and has no approval or activation command. Refs #213; these
local results do not close the issue.

## Deterministic checks and alerts (#212)

`rule_engine` reads persisted SQL case bodies and row versions, never a model's
fact snapshot. It has no model, resident-message, awareness-write or hold-release
interface. Existing hazard intake/referral and independent human hold release
remain authoritative. A bounded `clear` means only that particular check passed,
not that a home is compliant, safe, or released.

New draft cards may include an optional immutable `check` object. Its exact
contents appear in card history before the existing distinct named-owner
approval and activation. No contract is attached to old versions or seed drafts.
The two allowed kinds are:

| Kind | SQL case evidence and deterministic result |
| --- | --- |
| `hazard-awareness-clock` | Explicit `hazards` list; an empty list is not applicable. Each open record needs a valid, non-future timezone-aware `aware_at`, report `source`, known `priority` and explicit `released` boolean. `hours` is an owner-supplied integer 1..8760, not a guessed statutory period. Due time is awareness plus those elapsed hours; at due time the result is breach risk. Within `attention_hours` before due it is attention; before that it is clear for this clock only. Missing duration/evidence is unknown. Evidenced independent human release can be clear, but the checker never changes a hold. |
| `automated-decision-safeguard` | Explicit `automated_decisions` list; missing is unknown, empty is not applicable. An explicitly non-significant entry is not applicable. Significant entries need named `decision_owner` and proposal `source`; explicit `state: pending` is attention. `state: recorded` additionally needs human `evidence` and a non-future timezone-aware `decided_at` to be clear. Missing or contradictory evidence stays unknown. This field has no general-purpose writer or AI write path in this slice. |

For example, an exercise author can propose
`"check": {"kind": "hazard-awareness-clock", "hours": 48, "attention_hours": 24}`.
Those numbers are an illustrative fictional contract, not legal advice or
approved operational timings. The decision kind accepts only `kind`, no clock.
Unknown keys, expressions, model awareness dates and suppression flags are
rejected. Prose clocks are never parsed into executable rules.

Only an active, human-approved card inside its effective/retirement dates is
executable. A newer draft does not disable a prior eligible active version.
Every citation must be an exact held provision ID, such as
`source-id@v1#0001`. Missing citations, incomplete/unreviewed sources or
superseded versions prevent clear and return unknown. Consultations, historical
sources and future effective dates return `not applicable` and never fire as
active controls. These are local metadata checks, not verification that
legislation is currently correct.
Seed references and their review state remain unchanged.

Checks retain card/version/status, exact citations and source statuses, case
revision/evidence pointers, input hash, journey step, UTC evaluation time, safe
action, named decision owner and clock. All results, including throttled ones,
are retained. Checks, alert publication and the checkpoint commit atomically in
the law-store SQL adapter. Tables are append-only ledger tables on a
ledger-enabled SQL backend, otherwise protected by append-only triggers.
No SQLite replace/ignore/automatic-ID syntax is added.

Data/step retries use stable case-revision, card/source fingerprint and engine
version keys; schedule retries add a UTC minute bucket. Replaying a key returns
its original persisted time/results, even later or after restart. API case
mutations evaluate after commit; schedule pages revisit persisted cases to
recover missed or failed dispatch. Intermediate revisions that were never
checked are not reconstructed. Supply trusted SQL/law configuration, then run:

```bash
python -m zava_forward.core.rule_engine --limit 100 --after ""
```

Run successive pages using `next_after` until a page is empty, then restart at
the beginning on the next scheduled sweep. The maximum page is 100; the
existing store's backend-specific pagination is reused. The command does not
install a timer or change a deployment. A failed page exits unsuccessfully;
retry from the previous page token. Already committed home checkpoints replay,
and a later sweep advances the clocks.

Alerts group by explicit home ID (case ID when no separate home ID is held),
then rank by due time, harm, and stable IDs. Home groups rank by their first
alert. Attention publication is limited to once per 24 elapsed hours for a
home/card/step/evidence item; it never suppresses evaluations or breach
escalations. Latest attention/unknown episodes replace their older visible
copies; clear/inactive checks remove those advisory copies from the open view.
Unresolved breach risks remain visible across changes, holds and retirement,
labelled with their original evaluation and current-control availability.
Only the exact named owner with trusted `rule_owner` capability can acknowledge
or record outcomes/classifications. Breach outcome requires acknowledgement;
neither action changes the underlying hazard hold. An unresolved underlying
risk can raise a new alert after a recorded outcome.

False-positive and confirmed classifications are append-only and mutually
exclusive per alert, with total/classified/unclassified counts and
`false_positives / classified` (null for zero classified alerts). This is an
owner-classified fatigue indicator, not measured clinical/legal accuracy.
Classification never suppresses checks or substitutes for breach acknowledgement
and outcome. Read scopes and HTTP behavior are in the
[API guide](../api/README.md#deterministic-step-alert-api-212).

Local tests use constructed SQL facts and explicitly simulated approvals only.
Issue #329 regressions assert exact source-gating results and retained citation
metadata, with no evaluator call or persisted alert for ineligible sources.
Attention tests use distinct cases on the same home and changed due-time
episodes on one case: checks/checkpoints persist while publications are
suppressed just before 24 hours and allowed at exactly 24 hours. Independent
home/card/step/item keys and cross-case breach escalation have positive controls.
Nine in-memory mutations of source gates, shared throttling, its boundary and
each key dimension fail the intended assertions. These tests exposed no
production defect; the existing rule-engine implementation is unchanged.
Actual legal approvals, a deployed timer, step UI, real staff precision and
comprehension trials, operational retention policy, continuing 60,000-home
acceptance and live SQL Server/Azure verification remain unmet. Refs #212,
not issue closure or production acceptance.

### Issue #212 acceptance audit

Statuses below describe observed local engineering evidence only.
`test_rule_engine` is in core/tests; `test_rule_alerts` and the endpoint
inventory are in api/tests. No row grants operational or legal approval.

| Issue acceptance criterion | Local status and evidence | Unmet boundary |
| --- | --- | --- |
| Five cited results and status | Met locally: exact-threshold, missing-evidence, explicit empty applicability and cited source/status tests | No genuinely approved operational card or live source-currentness verification |
| Missing evidence unknown, never clear | Met locally: absent/invalid/future awareness, source, release and decision evidence tests | No fabricated source or human evidence fills gaps |
| Future/consulted rules never active | Met locally: future card/source dates, consultation, historical, partial/unreviewed and superseded source tests | No legal currentness claim |
| Model never sets awareness or suppresses checks | Met locally: no model dependency/write interface; unsupported spec/body fields denied; SQL facts unchanged by checks | No real-model safety evaluation is claimed |
| Safe action, owner, clock; breach acknowledgement/outcome | Met locally: payload assertions, exact-owner/capability and acknowledgement-before-outcome HTTP tests | Real decision-owner delegation and tenant assignment not evidenced |
| No alert sends a resident message | Met locally: no send interface or messaging side effect; HTTP lifecycle preserves contact records and holds | Human communication stays in its separate existing workflow |
| Home grouping, clock/harm ranking, attention limits, false positives | Partial end-to-end: local grouping/ranking, 24-hour publication and retained-classification tests pass; cases without `home_id` group by a derived `address_key` (normalised postcode and address, `home_scope` shows it) | The address key is not a registered home identifier; cases lacking address or postcode stay `case_only`; no real staff precision/false-positive trial |
| Safety routes work with engine down | Met locally: absent/evaluation/persistence failure HTTP tests preserve emergency intake/referral and show unknown/manual route | No Azure outage exercise |
| Idempotent and checkpointed | Met locally: exact retries, later-time retry, restart, concurrent adapters, atomic rollback and scheduled catch-up/page tests | No deployed timer or live SQL Server recovery evidence; unevaluated intermediate revisions are not reconstructed |

The API makes alerts available at their recorded journey step, but a workbench
alert component is not delivered. Together with real approvals, hosted
scheduling, staff trial and live-platform evidence, this remains an explicit
unmet end-to-end acceptance boundary rather than an issue-closing claim.

## SQL store

`ZF_STORE=sqlite` uses `sqlstore.py` on stdlib sqlite3 as the dev and test
driver, with the same `Store` interface. Each case row has a row version and a
save is `UPDATE ... WHERE rowversion = ?`; a lost race returns HTTP 409, and
nothing is written. The audit table is full-content, append-only (triggers
refuse update and delete) and hash-chained. Indexes cover the list filters,
owner, open safety issues, postcode, address and the ledger sequence, and a test
checks the query plans use them. No per-process state is needed for
correctness: a second process catches up from a database sequence before every
operation, and dev sign-in cookies are signed, not held in memory.

List reads are answered by SQL: each row carries derived, indexed columns
(a fixed-width rank key built by `ranking.sql_key`, days, owner, contractor,
stage, flags, search text). Filters, sorts, search, totals, header counts and
paging run in SQL, and ranks are global (a window over open cases). The default
sort also has keyset paging (`after` cursor, `next_cursor` in the response),
which the work list uses for "Show more"; other sorts use offset in SQL. A
migration adds the columns and rebuilds keys when the ranking policy version
changes. Tests check parity with the in-memory store, query plans and a
60,000-case timing.

In a ledger-enabled Azure SQL database every store table except the append-only audit table is an updatable
ledger table, and such a table accepts a new column only as nullable with no default. A column-adding
migration there (`MssqlStore._add_column_default`) therefore adds the column nullable, backfills the same
default in the same transaction, then adds a `CHECK (col IS NOT NULL)` and the default constraint. Defaults,
the non-null guarantee and the ledger history are kept; the one difference is that `sys.columns` reports the
column as nullable, because a ledger table cannot be altered to NOT NULL in place. Ordinary SQL Server and
SQLite keep the original `NOT NULL DEFAULT` statement. Local SQL Server 2022 ledger tests reproduce the
Azure SQL error and prove the migration; they are not proof against Azure SQL itself.

Azure SQL is implemented by `mssqlstore.py` and has run with the API managed
identity. It uses explicit `BIGINT` row versions, `NVARCHAR(MAX)` JSON bodies,
binary text collation and a transaction-owned `sp_getapplock` writer lock.
The audit table is append-only ledger when the database supports/enables it,
otherwise an `INSTEAD OF UPDATE, DELETE` trigger rejects mutation. External
immutable digest anchoring and the per-year ledger-table design in ADR 0002
remain open; a hash chain alone does not prove those proposed controls.

## Azure SQL store

`ZF_STORE=mssql` uses `mssqlstore.py`, a T-SQL dialect over the same `SqlStore`
logic, with the pinned `mssql-python` driver (`src/api/requirements.txt`, hashes
checked in the image build; the image adds `libltdl7` and `libkrb5-3`). Writers are
serialised across replicas by a transaction holding an exclusive application
lock (the equivalent of SQLite's write lock), every compared text column uses a
binary collation so ordering matches the other stores, and a connection dropped
between requests is reopened. Sign-in is Microsoft Entra with the app's managed
identity (`ZF_SQL_AUTH=msi`, plus `ZF_SQL_CLIENT_ID` for a user-assigned one), so
there is no database password. The audit table is an append-only ledger table
when the database has Azure SQL ledger enabled (the engine refuses update and
delete), otherwise an `INSTEAD OF` trigger does it. Every other table in a ledger
database also keeps row history, which matters for erasure and retention
(DPIA item to resolve before real data).

The first start seeds an empty database from `ZF_DATA`; the image carries no data,
so seed once from an operator machine with `ZF_SQL_AUTH=token` and
`ZF_SQL_TOKEN=$(az account get-access-token --resource https://database.windows.net/ --query accessToken -o tsv)`.
The app identity needs a contained user with `db_datareader`, `db_datawriter` and
`db_ddladmin` (see `infra/scripts/create-sql-users.sql`). `tests/test_mssqlstore.py`
runs the SQL store suites and the list-read parity suite against a real SQL Server
when `ZF_TEST_MSSQL=1` (and `ZF_SQL_*` point at a throwaway database).

### Merging a generated seed into a populated database (issue #360)

`SqlStore` seeds only an empty database, so a populated demo database cannot take
a baseline that way. `python -m zava_forward.core.seed_merge --seed PATH` (with
`ZF_STORE=sqlite|mssql` and the usual `ZF_*` settings) calls `SqlStore.merge_seed`,
an insert-only merge. It is a dry run unless `--apply` is given, prints counts
only, and `--expect-added N` aborts before any write when the number of cases to
add differs. In one transaction it first checks that the audit chain matches its
head, then skips a case that is already stored with identical content, aborts on a
case or document that differs (nothing is updated or deleted), inserts missing
shared documents (the stored `continuity` document is kept and reported), never
inserts staff, never changes `as_of`, recommendations or existing audit rows, and
appends one `seed_merge` audit entry that carries the seed SHA-256. Applying also recomputes the derived queue flags and
queue generation, which leaves the stored case content, `seq` and row versions of
existing cases unchanged; opening the store runs its usual schema checks, so run it
only against a populated database that the current release already serves (an empty
target is refused and left empty). A repeat run
adds nothing and no audit entry. For `sqlite`, the target is the same database the app would open from `ZF_SQLITE`, `ZF_STATE` or `ZF_DATA`.
Keep the seed file private and outside the
repository. Tests: `tests/test_seed_merge.py`, and `MssqlLedgerMigration` in
`src/api/tests/test_mssqlstore.py` for ledger and plain SQL Server databases.

## Frozen protocol, benefits register and release gates (issue #126)

`src/core/src/zava_forward/core/governance.py` records, and never decides, the pilot governance in the existing store (JSON or SQL, so it survives a restart). Managers use `GET /api/governance` and `POST /api/governance/{protocol-freeze,protocol-approve,benefits-record,benefits-approve,release,breach,restart}`. No AI assistant, ranking or tool has any part in it.

* Protocol (RULE-019, AC-062): a version freezes all thirteen required fields. A different person approves it with the OD-36 DPIA and lawful measurement-basis references. A change needs a reason and a new approval. `capture_gate()` keeps Phase 0 capture closed until the latest version and the BG-011 register are approved.
* Benefits register (BG-011, OD-18): event definitions and the MDE are recorded. `target_verdict` never returns pass or fail when the MDE is missing or exceeds a target (20% cycle time, 25% coordination hours); it returns "Not assessable" or "Interval estimate only".
* Release decisions (RULE-020, AC-063): each phase (Phase 0 capture, Shadow testing, Live pilot) and tranche has a Release or Withhold record with requirements, evidence, unresolved issues, cost and risk envelope reference and named approvers. Releasing Phase 0 capture needs the capture gate; Shadow testing needs entry evidence, and Shadow testing and Live pilot need Phase 0 capture released first.
* Guardrail breach (RULE-024, AC-078): `breach_record` (managers, quality inspectors and building safety liaisons, so a hazard-aware role can raise a breach without waiting for a manager) pauses the home, work package, archetype or workstream. `breach_restart` needs a different person, the OD-35 authority reference, accepted remediation evidence and a Release decision recorded after the breach. `guard_case_event` calls `require_not_paused` (home by case id or address, archetype by home type) and, for cases flagged `pilot`, `require_capture_open` in `log_call`, `set_decision`, `advance` and `return_case`; emergency and statutory hazard response continues outside any pause.

Tests: `tests/test_governance.py` (JSON and SQL stores, labelled synthetic demonstration values). Open items, not invented here: the real OD-18 definitions and MDE, the OD-36 DPIA and lawful basis, the OD-35 named authority, actual approvers, how cases are enrolled in the pilot cohort (the `pilot` flag), pause scopes for work package and workstream, and extending the guard to the remaining case workflows. The original protocol work did not deliver the RAI finding registers. The bounded claim register below now records their evidence inventory, not a fresh qualified assessment or owner acceptance; live use stays blocked.

### Constructed RAI evidence claims (2026-10-18, #126)

`rai_evidence_record(user, body)` appends an unverified constructed claim to the
existing checked `governance` document. Current registered Retrofit Programme
Managers and Programme Support Officers can record claims, not accept or close
findings. SQL rechecks the exact actor inside the writer transaction and commits
document plus success audit atomically. Competing writers fail closed. An identical
event reference/content/recorder reconciles the original record without another
audit; different content or actor conflicts. A new event requires `expected_revision`.
Server UTC, recorder identity, event reference and append revision are retained.
Unverified decision-maker references never assign responsibility or authority.

The detached `governance_view(user, assessment=None)["rai_evidence"]` always lists
the eleven residual and eleven unassessed original findings. Baseline commit
`1cb398c7b90bec05a5700008a97d0cfac494144a`, PRD v0.14.0, report 2026-10-14 and
planning-only acceptance 2026-10-15 remain immutable; DOWNGRADED stays open.
The optional exact assessment object is caller-declared, not deployment
attestation: full source commit plus task/version/release, or null task fields
with explicit nonapplicability. No context means Unknown; a changed component
moves claims into history, and baseline-source replay never becomes fresh.
References and result text are bounded inert strings, never fetched or executed.

Tiers distinguish implemented/source-tested, deployed-observed, proposed,
insufficient and independent-acceptance claims. Every tier remains an unverified
claim, including an independent-acceptance claim. Distinct matching finding
dispositions can cover 22/22 while all 22 remain Open, adequacy remains
unestablished and acceptance remains Unknown. History record count is separate.
Missing/legacy evidence is insufficient; malformed history is explicitly counted
and cannot make completeness true. Reads initialize no defaults and write no audit.
This inventory does not change task-release admission, capture, breaches, consent,
safety, finance, procurement or continuity.

`GovernanceCommittedError` means SQL persisted but acknowledgement failed:
reload and reconcile the event reference before another action. JSON retains
best-effort in-process restoration and its existing cross-file crash/non-atomic
boundary; it is not SQL-equivalent crash durability.

From the repository root, with installed source distributions:

```bash
PYTHONPATH=src/api/tests:src/core/tests:src/agents/tests .venv/bin/python -m unittest \
  test_governance test_governance_evidence_api test_assistant_release -q
```

On 2026-10-18 this ran 107 tests with 16 explicit MSSQL opt-in skips; the same
suite passed in the existing API image as UID10001 with read-only root,
capabilities dropped and writable tmpfs state. Separately, all 16 current
register cases passed on actual disposable loopback SQL Server 2022, each with a
unique database; its owned container was removed. Local SQL is not Azure,
witnessed restore, real-model, qualified human or application acceptance.

### Per-year ledger digests, load check and recovery drill (issue #114)

* `python -m zava_forward.core.ledger --seal-years` writes one immutable `year-YYYY.json`
  digest per completed year (entries, first link, head); `--by-year` verifies every
  year on its own, the links between years and each sealed digest, and reports a
  dropped sealed year. A self-consistent rewrite of a sealed year is caught only by
  its digest, so those files belong in the immutable Blob container. Proven in
  `src/core/tests/test_recovery.py`; run the scheduled `--by-year` check before relying on the ledger.
* `python -m zava_forward.core.synthetic.loadcheck --data zavaforward.json --homes 60000` runs the
  NFR-002 mix (five sessions, two writers) against the configured store and prints
  p50/p95/max per class. Local SQLite on 2026-10-15 over 60,000 labelled synthetic
  homes for 30 s: list p95 0.28 s, detail 0.30 s, write 0.33 s, no errors (limits 1 s,
  1 s, 2 s). Open items: the same run against Azure SQL, dashboard and import preview
  classes, and cost (needs Azure meter rates and measured vCore time).
* `src/core/src/zava_forward/core/recovery.py` erases a resident's personal fields and keeps a
  personal-data-free deletion register outside the database. The register is one
  write-once entry per erasure under the reserved case id `_erasures` in the document
  backend: Azure Blob Storage when `ZF_DOC_STORE=azure-blob` (same configuration as case
  documents), a local folder only as the local-test backend. The entry is written
  before the redaction, so a crash between the two leaves an erasure that
  `reapply_deletions` completes (audited as `erasure_reapplied`), never an unrecorded
  one; if the register cannot be written, nothing is redacted, and an unreadable
  register is an error, never an empty one. Tests: a SQLite backup restore proves the
  erasure returns, a fake Blob transport proves the register backend and the write
  ordering.
* Unverified: the Azure SQL point-in-time restore drill (DH-005) has not been run;
  the register has not been run against a real storage account, nor has its
  retention or immutability policy been configured or tested; the Blob container
  should carry a WORM/immutability policy, which is infrastructure and unproven here;
  cost (storage, transactions, restore) is not measured.

## Per-user chat thread storage (issue #160)

`chatthreads.py` stores chat threads and messages per user (ADR 0004 decision 3), behind the `Store` interface: the
in-memory `Store` keeps them in its live file, `SqlStore` and `MssqlStore` in the additive, idempotent `chat_thread` and
`chat_message` tables (Azure SQL in deployment, SQLite for local tests). A thread carries the server-derived owner,
case reference, assistant task and version, and model identity; a message carries its role, evidence references and,
for assistant messages, the model. `chat_create_thread`, `chat_add_message`, `chat_list_threads`, `chat_resume`,
`chat_archive` and `chat_delete` always filter on the owner (another user's thread is reported as not found). Writes use
the thread row version and raise `ConflictError` when a caller's expected version is stale. The audit ledger receives
metadata only (thread id, case, counts, role), never message text or title, so deleting a thread leaves the chain intact.
Not in this slice: the panel (#159), model calls, memory (#161), isolation hardening (#162), retention and export
(#163; retention policy is unlocked for the exercise, legal retention lock deferred). Fixtures are synthetic.
Tests: `tests/test_chatthreads.py` (in-memory and SQLite parity; `MssqlChatThreads` runs with `ZF_TEST_MSSQL=1`).

The employee panel records server-derived `actor_role` per message and includes
only prior user questions asked under the caller's current role. Changing from
role A to B and back does not relabel earlier questions. Existing JSON messages
without this field and SQL messages migrated with an empty role remain stored
but are excluded from model context because their asking role is unknown.
SQLite and SQL Server add the column idempotently; new messages persist it
across restarts. The panel's 4,000-character history cap measures the actual
dispatched `UNTRUSTED` block, including delimiter expansion, wrappers and
newlines, while preserving the newest fitting questions in chronological order.
The current question must fit the 1,000-character limit both before and after
redaction. An oversized masked question returns the context-limit workflow
fallback without a model call, rather than silently truncating the question.

The panel holds the existing reentrant store lock around message persistence
and its audit events, the answer event and the final turn receipt, including
rejected turns. These short sections serialize JSON audit predecessor updates
with other locked writes; model inference does not hold the lock. Nested JSON
and SQLite callers retain the same lock ownership and audit-flush behavior.
Synthetic concurrent rejected/completed-turn regressions verify the shared
chain, not just receipt counts. This is not a cross-process JSON write guarantee.

Regulatory chat's direct paired-message and referral writers also persist
`actor_role`. An owner inbox copy keeps the original asking role, not the
recipient's role; a legacy copy without known provenance keeps an empty role.
Both explicit and automatic conflict referrals retain this distinction across
JSON and SQLite restarts. The separate bounded audit snapshot and offline
usage summary do not load these message bodies.

## Chat and memory isolation (issue #162)

`chat_isolation.py` sits on the #160 repository and #163 privacy rules and adds no tables. Endpoints (staff roles only; contractors and unknown roles are denied, default deny): `GET/POST /api/chat/threads`, `GET /api/chat/threads/{id}`, `POST /api/chat/threads/{id}/messages|archive|delete`, `GET/POST /api/chat/memory` (the POST needs `task` and a prior opt-in), `GET /api/chat/memory/status?task=`, `POST /api/chat/memory/opt-in|opt-out|erase|global|task` and `POST /api/chat/memory/{id}/edit|delete` (the #285 lifecycle; `global` and `task` switches are administrator-only), `POST /api/chat/breakglass`. The owner is always the authenticated user; request fields such as `owner` or `email` are ignored, and another user's thread, or a case outside the caller's scope, is reported as not found (404, so existence cannot be probed). Prompts carry the masked question and only memory from `privacy.prompt_memory` (opt-in, switch-gated, labelled non-authoritative); stored model replies are redacted like user messages.

* Every turn re-reads the user's current role and re-projects the case through the same `store.detail` projection as the case card, so a changed or revoked role applies on the next turn.
* For roster-backed SQL users, the cited chat panel reads the authoritative SQL
  staff row at dispatch and again after inference, without relying on the staff
  cache. Deleted, disabled, inactive or non-chat staff are denied; a changed
  permitted role or projected source withholds the answer. Rejected completions
  store no assistant reply. SQLite regressions change rows through an independent
  connection while leaving both staff caches unchanged; they do not establish
  SQL Server, live-model or operational acceptance.
* The prompt holds only the caller's own thread, own unexpired memory and the projected case, each inside `UNTRUSTED` blocks with the block delimiters neutralised. The channel has no tools; replies are text only, labelled as unapproved, and a reply carrying tool-call or record-change syntax or a withheld reason is replaced by a refusal.
* Break-glass is refused until `CHAT_BREAKGLASS_REF` (owner policy reference) is recorded and the caller role is named in `CHAT_BREAKGLASS_ROLES`. When allowed it needs a purpose, expires within 60 minutes, returns counts and ids only (never content) and writes granted and refused attempts, each with actor, target and redacted purpose, to the audit ledger. Policy options for the owner and DPO are in `docs/reference/research/chat-memory-dpia.md`.
* Open items: the break-glass and administrator content-access policy is an owner decision (BRD OD-46) and is not decided here; whether contractors may use chat is undecided (denied); the injection set in `src/api/tests/test_chat_isolation.py` is a recorded regression set, not evidence of complete coverage; real-model behaviour was not exercised.

Tests: `src/api/tests/test_chat_isolation.py` (extends the role matrix; replays the synthetic isolation fixture cases).

## Service continuity, versioning and export (issue #122)

`continuity.py` adds a persisted AI suspension (whole release or one registered task), a restart gate, a versioned
change register and a supplier-independent evidence export. Synthetic demonstration data only.

* Suspend: `POST /api/continuity/suspend` records scope, incident owner, containment, constructed communication
  (never sent), and the affected queued, leased and ready proposals, and raises an epoch.
* Enforcement: the epoch is read on the caller's own SQL connection at invoke, scan, claim, dispatch, complete and
  review, and shown in list and detail views; it does not depend on disabled buttons. In-flight provider calls may
  finish and stay charged or unknown; late results are quarantined and never actionable. No remote cancellation or
  exactly-once billing is claimed.
* Manual fallback: suspended AI paths return the workflow template with the reason; case work, resident challenge
  and hazard response are unaffected. Reject stays available.
* Restart: `restart-propose` (corrective evidence) then `restart-decide` by a different manager, with the current
  epoch and a named authority reference. Self-approved, stale, replayed or unauthorised restarts fail. The authority
  reference is recorded, not verified.
* Changes: `POST /api/continuity/change` and `change-reverse` version model, rule and configuration changes with an
  evaluation result (a failed evaluation is Blocked); reversal is a superseding record.
* Export: `GET /api/continuity/export` returns `zf-evidence-export/1` with a digest and ledger chain checked offline by
  `continuity.verify_export`, with no AI supplier needed. The bundle carries `complete` and `incomplete_reasons`: when
  the 5,000 assistant-proposal limit is hit it is flagged incomplete (with total and exported counts) and
  `verify_export` reports it not valid, so a truncated bundle is never presented as whole. The bundle records the ledger
  head (count and hash) and any sealed digests; `verify_export` fails when the entries do not reach that head. A
  recorded head can be rewritten together with the entries, so pass `expected_head` from a copy held outside the
  application (an immutable digest) to detect that.
* JSON store: AI task suspension, restart gating, the change register and export are enforced and tested on the JSON
  store. The five assistants are durable SQL only, so the bundle states `assistants.supported: false` and exports no
  assistant proposals there; assistant suspension on a JSON store is unsupported.
* Open owner items: witnessed authorised drill, recovery and response limits, supplier contract terms, Azure SQL
  drill evidence, interface identifier mapping, and the named restart authority.

### Non-operative custody, recovery and witness preparation (#122, 2026-10-21)

Preparation only. This subsection describes what an owner-approved drill would need to show. It is not a drill,
an appointment of any authority, legal or privacy compliance, or release acceptance. Every bullet below is a
proposed expectation, not an existing control. The controls above and the
constructed restart in [Operator incidents and constructed restart (#221)](#operator-incidents-and-constructed-restart-221)
are not proof of an actual authorised, witnessed drill. This repository holds no actual decision, participant,
Azure immutable storage or Azure SQL drill evidence. Every #122 acceptance criterion and the #221 restart
criteria stay unticked until reviewed actual evidence exists.

* Custody and verification expectations. `verify_export` checks the bundle digest, ledger chain, recorded head,
  an optional `expected_head` and completeness. An export is relied on only when it passes with an
  `expected_head` taken from a copy held outside the application. Sealed-year digest checks
  (`--by-year`, see [issue #114](#per-year-ledger-digests-load-check-and-recovery-drill-issue-114)) are a separate
  step. Record the head, who took the external copy, when, and where. An incomplete, truncated or
  self-recorded-head bundle is not evidence. The immutable external Azure head container and its retention policy
  are UNAPPROVED and not configured. No repository source shows that pre-gate (legacy) images are excluded from
  serving, so that exclusion is treated as not enforced or evidenced.
* Decision rights (roles only; no person, delegation or approval is recorded here):

  | Decision | Role | Status |
  | --- | --- | --- |
  | Suspend AI for a release or task | Incident owner recorded as text on the suspension | UNASSIGNED for actual use (OQ-017); recorded text is not verified authority |
  | Restart AI after an incident | Actual restart authority, distinct from the proposer | UNASSIGNED (OQ-017, RULE-020); OD-35 names Building Safety and Sponsor as owners of override authority and restart evidence, which supplies evidence and does not hold or delegate authority |
  | Accept corrective evidence | Competent reviewer | UNASSIGNED (OQ-017) |
  | Authorise a drill and its witness | Not named by any source | UNASSIGNED and UNAPPROVED |
  | Custody of the external head copy | Not named by any source | UNASSIGNED |
  | Resident, safety, professional and Finance decisions | Their existing human owners | Unchanged; AI and this protocol take none |

  Operator identity, the recorded authority reference, a seeded role or a model output never establishes authority.
* Witness (proposed; no source defines a witness role). A drill would need a witness who is authorised in
  writing, is not the incident owner, proposer or restart decider, and records what they observed. Until one is
  approved, no run counts as witnessed.
* Sequence for an approved drill (proposed). Suspension and export each append audit entries, so the head moves.
  Two heads are therefore kept apart: a pre-suspension baseline and the exact snapshot head of the export.
  (1) Confirm written authorisation, scope and a non-live data set. (2) Record the baseline head (n0, h0) outside
  the application; it is never the `expected_head` for a later export. (3) Suspend (this appends audit entries, such as `ai_suspend`) and
  confirm epoch enforcement and manual fallback. (4) Freeze other writers, then read the live head with the
  read-only `ledger_head()` (it writes no audit entry) and have the held-copy keeper record it outside the
  application as the snapshot head (ns, hs). (5) Export. `continuity_export` captures the head and entries before
  it appends its own `evidence_export` entry, so the bundle ends exactly at (ns, hs) while the live head then moves
  on; any later export needs a fresh step 4. (6) Run `verify_export(bundle, expected_head=(ns, hs))`; the head
  recorded inside the bundle is not independent custody. (7) Check the baseline separately: in the verified
  bundle, entry n0 has hash h0 and the entries after it are only the expected suspension entries. `verify_export`
  does not do this prefix check, so it is a proposed manual or tooling step. (8) Corrective evidence, then a
  distinct authorised restart decision. (9) Record outcome and residuals. A failed step, including any head
  mismatch from a write between steps 4 and 5, stops the drill and leaves AI suspended; whether to retry is a
  human decision.
* Communication. Owner and audience are UNASSIGNED. Notices stay constructed templates; nothing contacts residents,
  staff or suppliers automatically, and a real notice is a separate human decision.
* Stop conditions. Stop and keep AI suspended if authority or witness is unclear, the data is not constructed, the
  external head is missing or disagrees, the export is incomplete, a hazard or resident emergency arises (that
  response stays independent), or spend or Azure changes are not authorised.
* Not evidence: this text, constructed fixtures, earlier tests, the recorded authority reference, a template
  notice, or a green CI run. Evidence needed: named approvals, the witness record, the external head custody
  record, Azure SQL drill output and an enforced pre-gate-image exclusion, each independently reviewed.

## Synthetic home-specific cited chat (#214)

`regulatory_chat.RegulatoryChat` is the API-owned offline retrieval and storage
boundary. It reuses existing `LawStore`, approved exercise cards and
`citation_eligibility`, not a new vector store. The agents callback receives only
a bounded data bundle; it has no database, write tool or provider connection.
Only active simulated cards with complete, reviewed, current-version,
non-future provisions support an answer. Seeds stay unapproved. Held,
retired, missing, partial and unreviewed sources cannot support an answer.
Changed approved-source versions and same-purpose cards with differing
safe-action/clock text are flagged as potential conflicts, not reconciled.
This is not general semantic conflict detection or a live source-currentness check.

The supported lookup purposes are hazard sources and automated-decision sources.
Hazard facts are restricted further to Building Safety Liaison, Resident Liaison
Officer and Programme Manager roles: at most two hazards' enumerated category
and priority, after the existing case projection. No vulnerability, health,
address, resident name, contact, report narrative, memory or previous assistant
answer is retrieved. Other roles receive source excerpts and an explicit
missing-facts statement. Automated-decision lookup currently retrieves sources
only; it does not infer a decision or home applicability.

Fact citations bind the case/path, value and observation time by hash, with
unknown effective date; law citations retain immutable provision/version,
status, effective/retrieval dates and hash. Excerpts are limited to 350
characters and explicitly mark truncation and unverified live currentness.
The complete `regulatory-chat-v1` envelope is stored in the existing isolated
assistant message, with string IDs in evidence. Questions are limited to 1,000
characters, sources to four, cards to two and facts to four. An envelope over
the existing 8,000-character message limit fails before writing; it is never
silently truncated.

Answer pairs and explicit selected-turn doubt copies use single chat-repository
transactions. Supported conflicts automatically copy both cited versions and
the question to the named exercise owner's inbox in the same transaction as
the answer and sender receipt. Missing, ambiguous or unauthorized owner scope
prevents that conflict turn from being stored. Ordinary answers and refusals
retain the manual doubt action. JSON restores a pre-image on pre-save failure;
SQLite uses rollback.
A copied pair lives in the uniquely provisioned Juan Manuel Servera exercise
owner's own isolated thread, with a sender receipt and idempotent referrals per
stored source-thread/assistant-turn. A repeated ask, even with equal text, is
a new turn and may create a new referral; reload history after uncertain
responses instead of blindly resubmitting.
The sender's other messages and memory are not shared. Both current roles/case
rights are checked again inside the locked transaction before mutation; SQL
provisioning is read freshly, not from the legacy
staff cache. Trusted-proxy roles remain claim-derived instead of being replaced
by a wider staff-register role. Historical reads deny changed roles instead of
replaying wider content. SQL turn/referral metadata audit now commits in the
same transaction as the messages and receipt; an audit failure rolls back both.
The JSON file store alone retains the post-commit separate-ledger error boundary:
an audit failure after save reports that the turn/referral was saved and
requires history reload. It is not evidence of SQL audit atomicity. Audit holds
metadata only. Tests distinguish a real SQL COMMIT-before-effect failure from
the repository's no-op commit hook; neither establishes lost-acknowledgement
idempotency.
Copies have independent thread ownership/deletion; deleting the sender's
thread does not delete the explicit owner's copy. No email or live delivery
is implied. No rule-engine alert, consent, safety hold or case fact is changed.

Admission requires `ZF_REGULATORY_CHAT=synthetic-demo`, omitted/test/development
`ZF_ENV`, the loaded dataset's `regulatory_chat_exercise=synthetic-demo`
declaration (SQL `meta` key or JSON root) and all three existing privacy
references prefixed `SYNTH-`. These are simulated exercise references, not
actual privacy approvals; the marker is a trusted fixture declaration, not a
detector of real data. Do not set it on private or operational data. Unknown or
production environments deny. No automatic dataset marking or owner
provisioning is performed. Ordinary chat and memory gates are unchanged.

### Regulatory privacy and audit (#217)

`regulatory_privacy.retention_report` aligns own-thread review metadata with
the existing `CHAT_RETENTION_REF` and `CHAT_RETENTION_DAYS` settings. Without
both, periods and due status are unknown. For synthetic reporting, both must
be valid, the reference must start `SYNTH-` and days must be 1..36500 (technical
input bound, not a legal period). Review due is creation time plus days,
inclusive at the exact due instant, and includes archived regulatory threads.
No content is loaded, no records are deleted and no DPO approval is inferred.
Other source/card/check/alert/audit/usage periods stay explicitly unknown. Usage
inherits its parent records' access and unresolved DPO retention/hold review;
it has no separate indefinite-retention permission. This is
not a complete retention or rights implementation; the
[draft DPIA](../../docs/reference/research/chat-memory-dpia.md#regulatory-assistant-dpia-draft-for-dpo-review-2026-10-16-refs-217)
requires DPO review and remains unapproved.

Rule/card approvals, source reviews, checks and alerts already retain append-only
SQL history. SQL chat turn events now include actor/role, case/thread/sequence,
model, citation IDs and answer hash, never question/answer/excerpt/health content.
Referrals retain receipt and decision-owner linkage, once per selected pair.
Rollback-after-audit-insert and reopen tests cover the chain head and data.
Metadata and linkable hashes are not anonymous; DPO retention review is still needed.

### Offline regulatory consumption (2026-10-27, #208)

`regulatory_usage` records task/schema version, UTC day, outcome and zero model
calls/input/output/cached tokens/retries, without case/chat/source content.
Chat SQL audit writes this metadata with its turn; checks and alerts retain
the corresponding model-free metadata in their existing append-only records.
Every role's inference allowance is zero per UTC day. This is disabled
inference, not a spending approval, request quota or limit on urgent intake.

The authenticated user's current-role/day summary reads at most the latest
1,000 audit positions. SQL uses a primary-key sequence window and projects
other actors/actions' detail as NULL; it never loads chat messages or performs
an all-ledger detail query. JSON additionally tails at most 256 KiB from the
captured file size, excludes later appends and drops the leading partial line.
Truncation returns `bounded_partial`; otherwise
`recorded_audit_only`. Counts describe recorded events, never exact daily turn
totals: legacy unmetered records and post-save JSON audit failures cannot be
reconstructed. Unmetered events in the selected role/window are explicit.

Service cost and AI cost per accepted check remain Unknown, not zero. Missing
inputs are owner-agreed acceptance/counts, dated prices, attributable billing/
shared-service allocation and human review effort. No model evaluation or
paid budget/expiry authority is created.

Engine contract version 2 requires nonempty `reasons` as well as named human,
source, evidence and decision timestamp before a significant-decision check is
clear. An evidence ID alone, absent reasons or whitespace reasons stays unknown.
Version 1 checkpoints are not reused. This is a bounded evidence check, not
proof of a real human decision or UK GDPR compliance.

Run the synthetic core proofs with an installed editable package, from the
repository root:

```bash
PYTHONPATH="$PWD/src/core/tests" python3 -m unittest \
  test_regulatory_chat test_chat_panel test_chatthreads test_rule_engine \
  test_rulecards test_source_monitor -q
```

### Version-bound affected-person challenges (#220)

The existing resident operation records supplied challenges against retained
priority suggestions (`kind != "ai_task"`). It does not replace measure-decision
independent review or complaint/remedy controls. Both resident-information and
recorded-reason permissions are required to read or write the new fields.
`Store.detail` supplies `challenge_targets` with immutable proposal and separate
human-decision version tokens; callers must echo both when opening a challenge.
The registered server actor and current named owner remain authoritative.
Eligibility includes both original generation candidates and cases retained in
the human decision's `final_items`. A person may edit in an owned open case
outside the original 40 candidates. That case can challenge the retained
proposal/decision without changing the original generation `case_ids`, source
hashes or proposal version. Its missing source hash stays Unknown; a source
challenge is refused rather than inventing generation evidence.

`challenge_open` requires `proposal_id`, `proposal_version`, `decision_version`,
`target_kind` (`proposal`, `source` or `policy`), supplied `channel`, `source`,
`request`, `explanation`, `owner`, `non_digital_route` and `next_update`.
Digital means staff recording supplied digital evidence, not resident
self-authentication. Phone, Letter and In person use the same controlled path.
`challenge_resolve` requires `id`, `expected_version`, `resolution`,
`resolution_ref`, `explanation` and `next_update`. The named owner or an existing
authorised manager can record one terminal resolution, either
`Correction recorded` or `Explanation recorded`. Opening evidence and the
original human decision are retained; terminal corrections cannot be erased by
a later resolution. These are human-supplied records, not automated redress.

New priority generation hashes the actual audience-filtered case citation labels
at input capture, before generation. These are citation-snapshot versions, not
universal raw-document versions. Legacy missing hashes stay Unknown; their
proposal or recorded policy may still be challenged. Source/policy publication,
law applicability and approval authority are not changed.

A supplied correction derives stale state only for the exact proposal, case/hash
or recorded ranking-policy version. A policy correction can affect matching
suggestions on other cases. Original proposal content and accepted/edited human
dispositions stay historical; `stale`, `review_stale` and `challenge_ids` explain
why reliance is disabled. Accept/edit is fenced again inside the SQL writer;
reject, manual work and independent hazard intake remain available.
Continuity export includes derived stale metadata, not challenge narrative.
Audit records contain action/record IDs, not the supplied free text.

Challenge references in priority generation, latest and review responses require
both resident-information and recorded-reason rights on the current registered
reader. Without those rights, stale/actionable/reliance flags remain accurate
but `challenge_ids` is empty, including corrections recorded on another case.
Case detail applies the same current-reader check to both challenge narratives
and the target catalog, including when a cookie or populated store cache still
holds a downgraded or removed staff identity. Denial removes both fields without
removing the ordinary case card; trusted internal `user=None` remains unchanged.
Release/model-route denial audit survives a failed accept/edit; failed human
disposition changes and their acceptance/edit audit entries are rolled back.

Catalog and continuity reads build one correction-dependency lookup per read,
not one case scan per retained proposal. Writer revalidation obtains only
correction IDs and targets through SQLite JSON extraction or SQL Server
`OPENJSON`, under the existing serialized transaction. The derived
`priority_correction` case flag and filtered `ix_cases_priority_correction`
index follow the existing derived case-column pattern. Seed/save maintains the
flag in the same row update as the challenge; an existing database is backfilled
with column addition and rebuild in one serialized transaction. A failed rebuild
rolls back the column too, so restart cannot mistake default-zero rows for a
completed migration. SQL Server uses its existing dialect hook boundary for
`ALTER TABLE ... ADD`. No dependency table, service or pretransaction authority
cache is introduced. Only flagged case bodies reach JSON extraction; matching
still uses exact proposal/source/policy versions and current writer checks.

On 2026-10-19, an owned local SQL Server 2022 container (2 CPUs, 3 GiB limit)
measured exactly 60,000 generated public case bodies (74,566,390 UTF-8 bytes)
with one corrected case. The actual baseline plan scanned 60,000 rows and
executed `OPENJSON` 60,000 times; the filtered plan sought one flagged row and
executed it once. Three warm-cache query samples fell from 1.458-1.533 seconds
to 0.792-0.889 milliseconds. A competing unrelated writer using the same
application lock waited 1.489-1.565 seconds versus 32.083-32.442 milliseconds;
that wait and the measured lock interval include a deliberate 25 ms rendezvous,
not just query time. These are bounded sparse-correction engineering observations,
not an SLA, full application throughput or production capacity result. Dense
corrections, larger narratives, cold I/O and operational concurrency remain
unmeasured; the lookup still scales with flagged case/challenge count.

Focused synthetic JSON/SQLite proof, with installed editable distributions:

```bash
PYTHONPATH=src/core/tests:src/agents/tests:src/api/tests:src/api python3 -m unittest \
  test_resident_decisions.JsonResidentDecisions \
  test_resident_decisions.SqlResidentDecisions test_resident_api -k challenge -q
```

This is a bounded retained-priority slice, not whole-system AC-071 acceptance.
Other assistant/form paths, operational native SQL Server acceptance, qualified
legal/RAI review and resident comprehension remain unproven. Seven constructed
native SQL Server correction-race, dependency, entitlement and rollback
regressions supplement the JSON/SQLite checks. Subsequent native cached-reader,
atomic migration/restart, correction-flag rollback and persisted denial-audit
regressions add focused coverage, not operational acceptance. The bounded
60,000-case query measurement above is not a whole-workflow load claim.

## Resident-owned preview boundary (#444)

`zava_forward.core.resident_preview` is the narrow boundary behind the synthetic resident
preview; `zava_forward.core.synthetic.resident_preview_fixture` builds its invented dataset by
driving the existing store with explicit synthetic inputs.

* `resolve_grant` re-reads a server-owned fixture and returns the one current grant for a subject.
  Everything else denies by default: unknown subject, no grant, revoked, expired, not yet valid,
  more than one current grant, malformed or non-empty `actions`, wildcard or empty case ids.
* `resident_view` builds the response field by field from named, mapped values (a positive
  allowlist), never from staff payloads or `projection.py`. A new staff field stays hidden until it
  is mapped. Appointments come from the existing appointment status: only `Committed` is a
  confirmed arrangement, `Offer` is shown as not confirmed, anything else is counted as unknown.
* A representative grant shows only fields for tasks the existing domain authority record
  currently confirms for the stated measure; a malformed record denies rather than raises.
* `safe_start` refuses cloud, store and AI environment variables, non-loopback hosts, symlinked or
  missing files, the normal `ZF_DATA` or `~/.zava-forward` location, and files that are not a
  matching disposable synthetic dataset and fixture. `open_store` works on a private temporary copy
  so the preview never writes beside the dataset.
* Stage text is a fixed plain-language map; an unmapped stage stays "unknown".

Tests: `src/core/tests/test_resident_preview.py`. This is feedback tooling, not a resident
service, and it is not an approval of the resident design in PR 442.

The boundary's assets, trust boundaries, threats, controls, evidence and residual risks are
stated in the [preview threat model](../api/README.md#threat-model-for-the-synthetic-preview-444).

## Synthetic resident showcase boundary (#462)

`zava_forward.core.resident_showcase` is the pure domain for the fake-email resident showcase and
`resident_showcase_sql` is its read-only adapter. They do not use `resident_preview.safe_start`,
`resolve_grant`, `resident_view`, `open_store` or `Grant`, so the #444 loopback fixture guard is
unchanged. Only its read-only plain-language constants are reused.

* `canonical_email`: trim spaces, lower-case, ASCII only, `example.com` only, at most 64 local chars.
* `exclusion` and `build_identity_map` admit a row only with non-blank provenance, not revoked, in
  its window, a canonical `example.com` email and exactly one case with that email across all cases.
  At most 1000 mappings (raised from 25 for the owner-approved 2026-10-26 allowlist); more fails the whole map closed. Excluded rows are counted, never listed.
* `authorise` re-checks one freshly read row for the case in the session and requires its email to
  equal the email admitted in the map.
* `client_key` picks the limiter source: the peer, or under `ingress-rightmost` only the last
  `X-Forwarded-For` entry, falling back to the peer when it is not a bare IP.
* `resident_showcase_verifier` holds the password-strength policy and `build_verifier` used by the
  offline tool `infra/scripts/resident_demo_verifier.py`.
* `PasswordVerifier` and `make_verifier` use scrypt. `verify_login` does one scrypt run for every
  attempt. `SessionCodec` issues signed, expiring, process-bound session and CSRF tokens.
  `LoginLimiter` is a bounded sliding window.
* `showcase_view` is a positive allowlist built field by field. `config_from_env` fails closed.
* `ShowcaseReader` runs two fixed SELECTs on `[resident_showcase].[v_resident_case]` and nothing else.

Tests: `src/core/tests/test_resident_showcase.py` (no SQL) and `test_resident_showcase_sql.py`
(loopback SQL Server only). The live synthetic provenance of the homes database is not established:
cases have no per-case synthetic flag, so the allowlist table, filled only after named approval,
is the provenance record. See the [API section](../api/README.md#synthetic-resident-showcase-462).

## Affected-person challenge and correction route (#220)

`zava_forward.core.challenges.ChallengeRegister` is a store-independent register for constructed
challenges (FR-052, AC-071, FR-043). `record_digital` and `record_staff` (named staff, phone,
in-person, paper or assisted-visit channel) record a challenge against a source, policy or proposal
version and the human decision, with a human owner, a next-update date and a fixed accessible
non-digital route statement. `view` shows only permitted explanations. Only the named owner can
`review` or `resolve` with evidence. Graph nodes are `(kind, id, version)` tuples, so a correction
to `POL-1/v1` does not touch dependents of `POL-1/v2`. A `corrected` outcome marks exactly the
transitive dependents in the injected dependency graph stale and preserves prior versions; `upheld` and `withdrawn` mark
nothing. The register has no consent, refusal, sanction, closure or hazard-clock fields and never
reads or writes them.

Not delivered: persistence in the JSON, SQL and MSSQL stores, API and UI wiring, and the
no-retaliation and no-delayed-hazard-response criterion, which needs live workflow evidence and
human review. Tests: `src/core/tests/test_challenges.py`.

## Data steward and digital operator exception queue (#135)

`zava_forward.core.exception_queue.ExceptionQueue` is a store-independent register (FR-012, FR-029,
AC-040) for identity and source conflicts, failed imports, failed AI or integration runs and stranded
tasks. A named `data_steward` owns conflicts and imports; a named `digital_operator` owns AI,
integration and stranded-task items. `raise_conflict` needs two different values, each with source,
date and version, and shows them with the resolution owner in `conflict_view`. `queue` is scoped to
the caller's role and every view, denial and action is appended to the audit log shown by
`access_report(actor)`, which limits item audit entries to the caller's role scope and includes all non-item entries (queue views, outages, denials). `request_recovery` (hold, request_rerun, resolve_by_owner) needs a reason and records
`replayed` and `released` as False; nothing is replayed, corrected or released automatically. The
original source is deep-copied and kept, and eligibility stays `Unknown`. Outage notes and clearance evidence are
kept in the audit. `outage_banner` reports a missing, invalid, future or stale (over one hour) check as
Unknown, never healthy.

Not delivered: persistence in the JSON, SQL and MSSQL stores, API and UI wiring, importer and AI-run
producers, and owner approval of the role names and runbooks (open). Tests:
`src/core/tests/test_exception_queue.py`.
