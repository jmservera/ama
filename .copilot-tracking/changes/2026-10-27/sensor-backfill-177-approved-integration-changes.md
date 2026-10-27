---
title: Approved sensor backfill integration changes
ms.date: 2026-10-27
---

Task: 177-approved-integration-2026-10-27.
Declared scope: later owner-selected P04-T03 and remaining P04-T02.
Implementation execution: in progress. Original completed loop evidence below
is historical and preserved.

## P04-T03 Completion and P04-T02 Pre-Gate Checkpoint

Current-main merge56db2184c716d38fedde5022fd0204115e2bce46 includes
2e031c89a18ce1ceb3de4fda014fddcb90231fda and preserves all five original
child heads. No conflict resolution, rewrite or force push was needed.

Composed load_with_consumer now compares homes_covered against the actual
granted count, then budgets actual nominal observations and stock metadata
before TemporaryDirectory/write. Under/over-reported counts and accurate
oversized requests refuse without scratch, write, climate.series or consumer
processing. Zero-granted stock retains metadata limits and valid zero-row replay;
normal consumer loading succeeds exactly at its row limit. Existing fault
post-reconstruction/delivery guards and byte verification are unchanged.
Only two regression methods were added to the existing test module.

Focused validation command, from src/core with the existing installed external
environment and PYTHONDONTWRITEBYTECODE=1/PYTHONPATH=tests:
`python -m unittest test_historical_backfill test_sensor_backfill test_sensor_stock
test_sensor_faults test_sensor_privacy test_sensor_consumer -q`.
91 tests in13.385s PASS, one existing opt-in SQL skip; legacy test ResourceWarnings
are pre-existing. Nine composed methods pass. Complete core `ruff check
--no-cache .`, `ruff format --check --no-cache .` (100 files) and `mypy
--cache-dir=/tmp/ama-177-rv001-mypy-20261027` (153 files) PASS.
Logs: /mnt/ama-rpi-gates/177-rv001-20261027/focused-tests.log and static-types.log.
Initial explicit-file format inspection bypassed the existing migrated source's
format exclusion and failed; repository-configured format passes without
reformatting unrelated code. Initial mypy flagged test access to the unexported
tempfile import; string-based patch targets corrected that test-only issue.

P04-T03 checked; P04-T02 remains pending at this source checkpoint.
Original Review/critique bytes compare unchanged against31f5d2be.
Current plan/details, core README, KB synthesis/index and append-only log agree.
No new full Review, full-stock rerun, private input, production/human approval
or issue acceptance is claimed. Final exact-head gate, independent publication
assessment, child/parent publication and hosted outcomes will be recorded under
/mnt/ama-rpi-gates/177-rv001-20261027/ and in PR486, not in a post-gate commit.

## Later Owner-Selected Implementation, 2026-10-27

Standing authorization selects RV-001 implementation with a regression,
current-origin/main integration, one fresh scoped foreground gate and parent
publication. Preserve original critique/Not accepted Review and failed gate.
Use a normal merge of fetched main2e031c89 to retain all child ancestry instead
of an unnecessary rebase. No force push is anticipated; permission is restricted
to the run-owned parent if needed. No main merge or issue closure.

Active write boundary: composed loader, its existing historical tests, directly
related README/KB index/synthesis/log and canonical RPI plan/details/changes/
state. First execution boundary is current-main integration, then actual-stock
count and row-budget checks before temporary replay. Planned validation is the
focused historical/legacy/stock/fault/consumer suites, relevant core static/types
and the one newly authorized scoped gate. Lock contention waits rather than
ending the run. P04-T02 is not proven until external exact-head evidence exists.

## Plan and Critique

Research executed with Ready disposition. Single final-candidate critique
Complete / Revise, PC-001 through PC-004 directly dispositioned in plan/details;
original result preserved. Split independent climate and identity delivery into
whole P01/P02 phases for write-disjoint execution. No new critique or scope change.

## Owner Decisions and Boundaries

2026-10-27 key owner-approvals-2026-10-27-b approves synthetic-demo candidate
climate reuse, canonical stock home IDs, child integration and aggregate checks.
One scoped foreground changed gate supersedes --all; no main push/merge, uv,
private datasets, secrets or invented acceptance. Existing draft PRs reused.

## Execution

P01/P02 child implementations and P03 parent integration/aggregate validation
are complete. P04 original Review/publication remains. Detailed completion
evidence and exact heads follow.

### P02: Canonical identity child

Completed at 6fc8d0fef27839f720ddbbb1c13c91a1ca52c128 on existing
docs/backfill-consumer-183-stack. Compact collision-checked sensor keys preserve
canonical 128-unit export keys; consumer's 64-unit available-case boundary and
all independent controls stay explicit. Actual 35 consumer and 16 stock tests,
targeted Ruff/format/mypy passed. SQL Server remains pending aggregate gate.
Seven added methods, no removals. Child's dated approved changes record owns
detailed evidence. No private reads, remote publication or shared-schema widening.

### P03 dependency refinement

Immediately relevant sequencing refinement, no user decision: composition and
already-delivered child merges can proceed against agreed climate adapter seam
while isolated P01 acquisition executes. Final source integration and aggregate
validation still depend on P01. No repeated critique; current plan reconciled.

## Validation and Remaining Work

Focused/package tests, actual SQL parity and the 60,000-home generated-stock
730-day run passed. One independent Review and one scoped gate remain.
No human or operational acceptance is asserted.

## P01: Approved Climate Delivery

Child head 09ea9e23f1634d593ebd2dacf1b1f7fe78925c1b was committed on the
existing #481 branch, not pushed separately yet. Actual Open-Meteo acquisition
contains 17,544 hourly pairs for 2023-2024. Raw SHA-256
af76a90414d9ad8f19dacc95a38f06d4c4321a91bdf030ba231558c42506051e;
temperature -5.3..26.9 C and RH 36..100%. Typed core
ClimateHistory.read/series/manifest adapter and 12 test methods passed in parent;
child evidence reports 25 targeted checks and 30 reused candidate checks.
NASA 2023 sensitivity evidence remains separate, no source-year repetition.
Child approved changes record owns full acquisition/provenance evidence.
Initial untouched /tmp child worktree was moved to the repository worktree area
because the delegated worker could not access /tmp; no source was lost or copied.

## P03: Parent Integration

Normal, non-squash merges preserve all five child ancestries:
projection 9445645d, retrofit ace3f507, household 472346bc, identity c2a554db,
climate d3973924. Both README conflicts were resolved retaining every section;
sensor_backfill imports/fingerprints retain both projection and identity helpers.
No main merge, rebase or force push. Child source heads unchanged except the
two approved continuations above.

The explicit --climate/--climate-metadata mode composes household setpoint,
moisture/ventilation and dated fabric-loss effects without changing the legacy
equation/RNG. Default legacy payload hashes still pass. Explicit --measures
binds synthetic recorded dates; empty history remains neutral. Every climate,
stock, measure and source/model input is fingerprinted. Deterministic gzip
supports bounded local storage; optional fault truth remains evaluator-only,
compressed separately. Public observation helper preserves existing fault values.
Household fixed schedules no longer allocate an unused per-hour RNG; all
existing condition/subset outputs remain unchanged.

load_with_consumer reconstructs and byte-verifies current synthetic snapshots
before calling the actual consumer with explicit existing policy/controls and
delivery time. It does not create cases, grant consent/calibration, reset the
clock or bypass range/ordering. Legacy load_into stays distinct.

## Aggregate Validation So Far

* Full core discovery: 1,427 tests, 311.378 seconds, PASS with 186 pre-existing
  opt-in/integration skips; external core-unit.log retains exact output.
* Complete core Ruff, format (100 files) and mypy (153 source files): PASS.
* Seven composed aggregate tests: PASS, including separate household terms,
  exact retrofit activation/no-history/other-home neutrality, compressed
  reproducibility, exclusions, source/history binding, actual verified consumer
  load/replay/tampering refusal and measured hourly estimate.
* Actual-source hourly replay: four generated-stock homes, two days, seed183
  produces identical every-file hashes; seed184 changes readings. Outlier,
  duplicate and gap rates 0.1 each retain separate truth.
  External reproducibility-summary.json retains hashes.
* Existing task-owned SQL harness: first failed on missing mssql_python.
  Installed existing core[sql], agents and API distributions with pip only.
  Foreground `flock --nonblock /tmp/ama-rpi-heavy.lock ... sensor_sql_check.py`
  then passed all 45 actual SQL/API sensor tests in 16.351 seconds, including
  inherited canonical admission/64-unit/Unicode/oversized/missing/fault/control
  tests. Its own loopback SQL container was removed. No configured DB used.
  This focused harness is not a second RPI gate.
* Full-stock hourly pre-generation estimate: 1,051,200,000 rows, 158.0 CSV bytes
  per row, 154.68 GiB before compression/SQL/index overhead. Daily selected run:
  43,800,000 estimated rows, 6.45 GiB uncompressed. Both measured on 20 actual
  generated granted sensors before generation; no private data.
* Full-stock runtime and every-row reconciliation PASS externally under
  /mnt/ama-rpi-gates/177-approved-integration-20261027/. scale-summary.json binds
  exact commands and inputs. All 43,800,000 rows and all 60,000 canonical IDs were
  reconciled, exactly 730 daily rows per home. UTC window 2023-01-02 through
  2025-01-01 exclusive; seed183; 6,000 explicit generated synthetic loft measures.
  Reading gzip shards total 703,111,263 bytes. Generation/estimation 1,114.83
  seconds; including full verification 1,498.8 seconds.
* Readings SHA-256:
  d07715c8b55fc4e0b6d771472f6f823110fe7b39ed47eab370ef7daf4d98bc41.
  Manifest SHA-256:
  6625698566e3a7b8ca4a7efc38d870edf629f97cb0a4c23dd0e87ece8acc16d4.
  Canonical normalized stock SHA-256:
  2802547013b069c6e3917d987e1bfcd3d9b758dae4e75a48a2b6381838cd98b2.
  Generated CSV SHA-256:
  91d2ae3f15e1f2d501faa7d9d24430263bc823a8179a40a016e7555ccb417dc7.
  Generator revision:
  sha256:7a4179b6720337eac04dcbfa59c7f36f6efef24d75c946879e11898f2bd5e893.
* The full run is daily, not a billion-row hourly run or proof of the unread
  private register's exact keys. Hourly seed/fault behavior was independently
  exercised on the actual-source four-home/two-day bounded replay above.

## Pre-Review Remaining Work

Full-stock reconciliation and KB/marker synchronization complete; ready for
one independent Review after committing implementation. Then commit original
Review/state evidence, archive/
restore-verify finite task-created ignored metadata/caches, authorized clean,
one scoped gate, official receipt verification, independent exact-head receipt
assessment and normal child/parent publication. No readiness claim yet.

## Pre-Review Reconciliation

P01, P02 and P03 markers/tasks checked with actual completion evidence.
Current phase details, KB status, plan summary, changes and state agree.
No implementation blocker or unimplemented model integration remains.
P04-T01 original Review and P04-T02 gate/publication remain unchecked; this is
review readiness, not publication or whole-issue acceptance.
Known scientific, regional, private-register and real monitoring limitations
remain explicit follow-ups, not hidden validation failures or invented approval.

## Original Review and Final Pre-Gate Checkpoint

Independent Review execution Complete; outcome Not accepted. Assessed
implementation 263e1dbfddd0587528c37dca5b8abb9697208dc9 against historical
base864a5021. One Medium RV-001: composed loader uses an unverified manifest
home count in its pre-replay budget check; inconsistent metadata can cause
reconstruction above max_rows before rejection. No consumer admission bypass
was demonstrated. Original record preserved; no correction or second Review
performed in this loop. Route to later rpi-implement with a bounded pre-write
refusal regression. Parent must remain draft.

P04-T01 checked for executed Review, not acceptance. P04-T02 intentionally
unchecked at this committed source checkpoint. Administrative completion will
be recorded externally and in PR bodies, without a post-gate source commit.
Fresh fetched main2e031c89a18ce1ceb3de4fda014fddcb90231fda supersedes the
Review's fixed historical comparison for the upcoming gate only; no rebase.
Exactly one authorized foreground changed gate will target a fresh
/mnt/ama-rpi-gates/177-approved-integration-parent-gate-20261027-final with
--lock-timeout 0 after archive/readback/restore/hash-verified finite cache
selection and git clean -fdxq. Original Review and historical receipts do not
become a passing exact-head/source acceptance assessment by this operation.
Publish new child heads before parent; update decision-blocker comments and
all five child/parent bodies truthfully. No ready transition while RV-001 open,
regardless of gate/hosted success; no main merge.

## Sole Gate Attempt and Blocked Publication

The sole authorized foreground invocation ran at
1b3f623f62a332b0e327ab270964d1bcb1800946 against freshly fetched
2e031c89a18ce1ceb3de4fda014fddcb90231fda, with --changed,
--lock-timeout 0 and the fresh external --out above. Exit1:
"BLOCKED: Candidate does not descend from the reviewed main base".
Main had added #479 after the topic fork. No check group, image, SQL suite or
receipt generation ran. The output directory/receipt do not exist; preserve
the external .log, not a fabricated failure receipt.

Finite cleanup succeeded beforehand. Tracking/cache archive SHA-256:
0a0fb7549425bffd13364422087539e650f267f6024db2df6b78f47c0d375437.
Full archive readback, selected restore hashes and protected tracking hashes
verified; authorized git clean -fdxq left no candidates.

No retry, old-base substitution, rebase, main merge, gate-policy relaxation,
branch push or readiness transition. Independent exact-head receipt assessment,
official verification and hosted new-head checks are unavailable, not passed.
Post-attempt changes are status/evidence only and claim no successful gate.
All implementation commits remain local; remote child/parent heads retain their
previous candidates. PR bodies and decision-blocker comments will explicitly
distinguish local evidence from hosted delivery.

The coordinator must select later implementation of RV-001 and authorize normal
current-main integration plus a new scoped gate before branch publication.
This completed Research/Plan/Implement/Review loop retains the original
Not accepted outcome and does not start a child or repeat Review automatically.
