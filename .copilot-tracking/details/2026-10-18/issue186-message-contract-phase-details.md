<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue186 message contract

## Metadata

* Task ID: issue186
* Task slug: issue186-message-contract
* Plan: .copilot-tracking/plans/2026-10-18/issue186-message-contract-plan.md
* Evidence: .copilot-tracking/research/2026-10-18/issue186-message-contract-research.md
* Initial direction: documentation/shared-contract verification only.
* Readiness: Ready; one critique Complete/Revise with PC-001/002 directly disposed.
* Blockers: none for bounded documentation.

## Phase Index

| Phase | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Document and measure | Complete | P01-T01, P01-T02 |
| P02 | Verify and reconcile | Complete | P02-T01 |

P01-T01 complete: actual measurement log records366 bytes with exact current
shape/reference checks and executed N1/N60000 rates.
P01-T02 complete: six documentation targets integrated with measured sample,
exact source description, replay/accounting and compatibility/gate boundaries.
P02-T01 complete:80 unchanged tests passed with SQLite/session TMPDIR; initial
repository-output refusal retained. Docs reproduction, field table, bytes,
relative links/anchors, append-only log and source parity pass. Both exact
scratch roots removed using rmdir. No active implementation markers remain.

<!-- rpi:phase id=P01 -->
## P01: Document and measure unchanged contract

Context: research C1-C11 proves authoritative imported shape, current fixture,
replay/conflict behavior and incompatible stock IDs. Intent: descriptive
source-linked contract, not an independently executable schema.
Boundary: existing docs plus tracking only; no source/test changes.
Dependency: one final-candidate critique disposed by planning parent.
Completion: actual measurement and six coherent documentation changes.
Unresolved: none; downstream compatibility is explicitly deferred.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Measure public current-contract example

Use existing sensor_consumer_fixture.observations()[0] unchanged. Print sorted
ASCII JSON using json.dumps(row,sort_keys=True,ensure_ascii=True).encode("utf-8"),
the exact prior-art expression in SensorConsumer._reference. State default
separators, no newline, byte length and SHA-256. This is one fully declared
sample, not a range maximum or adopted transport serialization.
Compare set(row) with imported READING_FIELDS, assert all fields strings and
consumer._shape(row) is None. Do not add a public API for this verification.
Use Fraction for exact3N/86400; multiply measured B by3N; assert N1/60000 expected
counts/rates and print results. No stock dataset required.
Dependency: installed src distributions. System import failure already observed;
use task-owned session venv, not PYTHONPATH=mvp. PYTHONPATH=src/core/tests adds
existing test helpers only. Never inspect .env or inherited private data paths.
Expected evidence: reproducible literal command and exact output in changes,
and production-facing reproduction in synthesis.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Integrate canonical documentation

Targets and roles:

* docs/reference/research/iot-sensor-analytics-research-plan.md: current section
  before historical privacy note; authoritative field table; stable key/replay/
  conflict; envelope limits vs closed shape; actual paired sample and rates.
* src/core/README.md: short link to existing synthesis from consumer section.
* src/api/README.md: link clarifying finite batches are not wire packetization.
* docs/case_study_48_addendum.md: concise sensor-section current accounting and
  compatibility boundary, preserving three/day and independent gates.
* docs/reference/README.md: route to new section with bounded claim.
* docs/reference/log.md: append dated material KB change; preserve full history.

Fields: sensor_id/reading_id/home_id/observed_at/temperature_c/humidity_pct/
source_type/scenario/seed/schema_version/temperature_unit/humidity_unit/calibrated.
All strings; use source exact limits, first-character rule, decimal/seed
grammar and version. Structural rejection and independently configured
mapping/consent/calibration/window/skew/range/order checks are distinct.
No raw/truth fields in envelope. Bounded receipts/DQ and batch prefix handling
must not claim whole-batch atomicity.
N is a declared eligible synthetic-home accounting population with one paired
observation slot three times/day, not proof60000 configured controls or devices.
Two scalar measures/row do not double observation records.
Report3N/day, mean3N/86400, optional nominal8h spacing as arithmetic only, not
new scheduler. API batches1..100 per callable, no scheduled calls chosen.
Wire messages only if explicit conditional one-row/message; if k rows/message,
formula with explicit packing assumptions, not a selected design.
Do not infer Hub billable units/tier capacity/cost from JSON. Exclude transport/
security/property overhead, retries, rejected delivery, database storage/index
and billing rounding; sample B is not a maximum, distribution or capacity claim.
Gap: stock.sensor_id SENS-SYN- +64-char SHA256 lowercase hex =>73; reading_id
embeds it and exceeds40. No truncation/remap/new IDs/relaxed validation. Fixture
is legacy sensor_for(ZF-1), not stock-selection proof. Downstream187/188 require
separate reviewed compatibility decision. ADR accepted2026-10-15 Basic exercise
amendment; no reopening acceptance or whole110 completion.
Dependency: P01-T01 results. Completion evidence: diff and reproduced values.

<!-- rpi:phase id=P02 -->
## P02: Verify and reconcile evidence

Context: unchanged source/runtime; docs must exactly describe, not repair it.
Intent: smallest adequate semantic and documentation checks.
Dependency: P01 complete. Boundary: no image/UI/actualSQL/Azure needed because no
behavior change or new engine behavior assertion. Existing baseline receipts
stay historical, not newly executed.
Completion: focused suites pass, links/shape/arithmetic/diff checked and changes
record reconciled. Unresolved: original Review later evaluates this boundary.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Run focused checks and reconcile artifacts

From root with task venv and issue-owned session scratch
/home/azureuser/.copilot/session-state/904bed7a-ed3d-4a25-bd79-ca51b4af63bd/files/issue186-temp
(created explicitly outside repo; TMPDIR absolute; no private settings inspected):
ZF_SENSOR_MSSQL=0 TMPDIR="/home/azureuser/.copilot/session-state/904bed7a-ed3d-4a25-bd79-ca51b4af63bd/files/issue186-temp"
PYTHONPATH=src/core/tests:src/api/tests python -m unittest
test_sensor_consumer test_sensor_ingestion test_sensor_faults -q.
The backend pin excludes store_at's MSSQL branch even if inherited opt-in is1.
Apply both pins to any SQL fixture reproduction as well. Do not probe/read/print
inherited SQL configuration or credentials. Verify tempfile.gettempdir() equals
the owned session scratch location; clean test temp directories and remove the
exact empty scratch directory afterward, excluding generated stores from commits.
Initial repository-local TMPDIR caused16 errors in80 tests because the unchanged
stock_fabric._destination deliberately refuses repository output for even tiny
synthetic generator fixtures. Retain that failed run. Session-owned scratch
preserves isolation without weakening the generator or changing approved scope.
This covers actual SQLite stable-key/reopen/replay/conflict, schema/unit/time
refusal, partial failure and existing fault observation shape.
No test changes or additions (max0, removals none). No configured lint/format/
type run necessary for docs-only changes; if a source edit seems needed, stop.
Verify field table/example against imported authority and existing consumer;
actual tempfile SQL admission/replay is already covered by unchanged tests.
Read changed docs, verify relative links/anchors and arithmetic, run git diff
--check and ensure only approved six docs plus issue186 tracking files changed.
Record commands, exit codes, skips/failures and limits without masking failures.
Update plan markers/details/changes/state before one original Review.
No independent final-head acceptance implied by original Review: coordinator
owns later whole-PR exact-head review, closure and merge.
