---
title: Approved sensor backfill integration changes
ms.date: 2026-10-27
---

Task: 177-approved-integration-2026-10-27.
Declared scope: full plan. Implementation execution: in progress.

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
