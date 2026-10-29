---
title: IoT consumer and synthetic live streaming changes
ms.date: 2026-10-27
---

## Original Scope and Status (before correction cycle 1)

Task 110 / iot-consumer-110, full P01-P03 implementation scope.
Plan/details dated 2026-10-27. Research complete, one critique Revise preserved;
all six findings directly disposed without a second critique.
Implementation source scope executed; full delivery Partial. P01/P02 executed;
P03 local validation and one independent Review complete. Review outcome is
Not accepted, with three Medium defects routed to later implementation.
Gated publication remains blocked, not complete.
No Azure operations or secret/private-data reads.

## P01: Synthetic replay

Added core synthetic.sensor_stream and six owned tests. Exact existing
seasonal-generator comparison and odd/nonzero nominal-slot replay pass.
Synthetic-only stock validation, all declared fault modes, three/day default,
finite scale/bytes/quota controls and speed/pause/stop/cancellation pass.
Initial Ruff found one long assertion; formatter corrected it. Initial mypy
found calls to existing untyped generator; use the existing narrowly scoped
disallow_untyped_calls override pattern, not casts or ignored errors.

## P02: API transport

Source and test evidence complete for the executed local boundary; Review
findings remain open.
Pinned SDK witness: EventData.system_properties merges AMQP message properties
and annotations; EventData.properties exposes AMQP application properties.
Custom routed IoT properties are decoded only at the dedicated trusted
Hub-only sender endpoint; ambiguous bytes/string/annotation forms are refused.
Actual routed metadata remains a live verification gap.
Installed async SDK probe showed aiohttp absent and neither SDK declares it;
added an explicit pinned aiohttp dependency for asynchronous managed identity.
SDK PartitionContext.update_checkpoint without a store only warns/no-ops:
removed that misleading call. This run uses no checkpoint store and always
starts each new receiver at retained beginning (-1). SQL remains the only
durable restart state. Checkpoint-write failure is therefore not applicable.
Cancelled/timed-out shielded SQL work can still commit, but never checkpoint;
retain identities and replay to reconcile. The receiver's network wait deadline
is bounded; it cannot claim to roll back or forcibly stop a database operation.

## P03: Validation, Review and publication

Publication blocked. No full gate authorized; scoped checks cannot establish
complete repository final-publication acceptance.
Do not treat local/fake-SDK proof as actual Hub/Azure SQL or whole AC-066.

### Local validation completed so far

* Core configured Ruff check and format check: pass, 102 formatted files.
* Core configured strict mypy: pass, 155 source files.
* Core test_sensor*.py selector: 96 tests, pass, one existing opt-in SQL Server
  integration skip. Existing backfill tests emit unclosed-file ResourceWarnings.
* Core test_historical_backfill.py: 9 tests, pass.
* API configured Ruff check and format check: pass, 48 formatted files.
* API configured strict mypy: pass, 90 source files.
* New transport module: initially 16 tests, pass; final focused API transport
  and inherited sensor-ingestion selector: 62 tests, pass (17 new transport).
* Full existing API discovery: 1137 tests in 463.978 seconds, pass, 314 existing
  opt-in/integration skips. The additional distinct-device case was then
  covered by the final focused selector; no skipped integration is counted
  as Hub/Azure SQL success.
* Hashed runtime requirements dry-run: pass. Actual AioHttpTransport opens/closes
  locally without network; pip check passes.
* git diff --check: pass.
* New documentation section relative-file/heading links: pass.
* Existing migration authoring suite initially failed seven cases because
  system Python lacked python-pptx/Pillow. Installed the declared
  tools/rename-zava-requirements.txt in the external validation venv and reran:
  all 25 tests pass. No dependency pins were loosened.
* No SQL Server container, Azure, real AI, browser or deployment acceptance
  claimed from these local backend-only checks.

### Pre-Review reconciliation

Plan and phase details reflect the actual no-checkpoint strategy and shielded
SQL uncertainty, not the superseded warning-only SDK no-op. Source behavior,
documentation and test ownership agree. There are exactly two new test modules,
no existing test removals or workflow-name changes. Current fetched main equals
the branch base 09099ecd1a66ee9d37ad993707d1f2eda07cdfd4.
Required independent Review was unexecuted at that handoff and is now preserved
below. Publication gates remain unproven. A scoped gate is not full-gate evidence.

### Independent Review and parent closeout

Exactly one independent Review completed at
.copilot-tracking/reviews/logs/2026-10-27/iot-consumer-110-review.md.
Execution: Complete. Outcome: Not accepted. Original critique Revise unchanged.
Independent bounded probes reproduced three Medium findings:

* RV-001: a slow connect consumes a pre-reserved rate interval, permitting
  subsequent actual sends closer than the configured maximum rate.
* RV-002: the descriptor's full-register digest does not bind the selected
  subset or mutable selected model inputs.
* RV-003: receiver partial construction is outside cleanup/sanitized errors.

No finding is claimed fixed. Per the one-pass RPI contract, route to later
owner-selected implementation, not a second Review or silent closure.
The RPI loop is complete, but implementation acceptance and publication are
blocked. No issue criterion or human-review checkbox has been ticked.
Existing local tests do not overrule the independent adverse evidence.

### Local persistence and publication decision

Source and original RPI evidence were committed locally as 7cd2400f on
feat/iot-consumer-110, with authenticated-account noreply author/committer
and the required Copilot trailer. No source was changed after Review.
The allowed scoped heavy gate was not run: the independent Review already
blocks this candidate, and the complete final-publication gate is explicitly
not authorized. No lock contention or passing receipt is claimed.
No push, PR, issue closure or Azure operation occurred. This is a persistent
local handoff, not successful delivery of the requested published PR.
P03 publication remains incomplete. The three ranked concrete defect
follow-ups are recorded in state; existing credential/live/budget and OD-43
owner gates remain distinct.

## Amendments and Divergences

Legacy seasonal model selected explicitly; composed climate handover deferred.
Normal-device mutated unmapped identity is a transport refusal, not SQL DQ.
Fresh receivers replay retained history from -1; no new checkpoint store.

## Blockers and Remaining Work

Actual #185 credential lifecycle, #188 live acceptance and #189 active budget
verification remain deferred under the issue criteria. No issue closure claimed.

## Correction Cycle 1: Opening Implementation State

Date: 2026-10-27. Task 110-correction-1, parent 110. Scope: correction P04-P07
only; original findings and original P01-P03 outcomes above remain historical.
Research Complete/Ready; correction critique executed once, Complete/Pass,
zero findings. P04 actual send admission is first, followed by P05 construction
cleanup and P06 canonical selected-input provenance. P07 validation/Review/
same-branch publication remains pending. No source edits yet; no new authority
or owner decision. User explicitly requests push to existing draft PR #508,
local units/lint/mypy, no full gate, Azure, secrets, private data or uv.

### Correction P04: Actual send admission

Separated nominal model wait from Pacer.admit_send; admission and SDK await
now execute adjacently in one coroutine after setup and truth preparation.
One limiter spans all clients. Core deterministic controls: 7 stream tests
pass. API publisher: 8 tests pass, including actual SDK-entry timestamps after
80ms connect/truth delays at a 50ms minimum interval for one/two homes.
Post-preparation stop/pause/deadline/cancel prevents SDK calls.
Initial targeted lint found loop-captured callbacks; bound callback inputs and
moved the send helper outside the loop. Targeted API lint then passed.
Declared packages/dev tools installed with pip in the external correction venv
after system missing-package evidence. No manifest or generated target changed.
P04/P04-T01 complete; proceed to P05.

### Correction P05: Receiver resource ownership

Credential/client construction and task startup now share the sanitized
try/except/finally. Cleanup closes only returned resources and cancels/observes
created tasks in one bounded call. Unexpected setup errors use
IOT_RECEIVE_FAILED; close failures use IOT_CLEANUP_FAILED; cancellation remains
cancellation. Receiver tests: 11 pass, including constructor/startup failure,
cleanup failure, setup cancellation and existing SQL uncertainty/restart.
API targeted lint and strict mypy (90 files) pass. P05/P05-T01 complete.

### Correction P06: Selected-input provenance

Shared _selected validates/canonicalizes a copied subset, derives sensors and
checks finite scale for both descriptor and replay. synthetic-stream-v2 retains
the original register stock_sha256 and adds selected_stock_sha256, selected
IDs/count and monitored count. Frames carry the selected digest separately from
unchanged observations; publisher copies it into restricted truth evidence.
Subset/fabric/consent mutation, normalization/order, invalid-input and mutation
after snapshot tests pass. Old frames keep original provenance after mutation.
No historical model, reading identity or wire schema changed.
P06/P06-T01 complete. Seven methods added across the two existing test modules;
zero test removals or new test modules, within the <=12-method lock.

### Correction P07: Local validation in progress

External venv: /tmp/ama-iot110-correction-1-c40e904e. Declared core[dev], agents
and api[dev] installed editable with pip after missing-dependency probe.
No dependency/lock/ignore/workflow changes. Commands use installed namespace
distributions; PYTHONPATH supplies tests only, never retired source.

* Core: python -m unittest discover -s tests -p 'test_sensor*.py' -q:
  99 tests pass, one existing opt-in SQL Server skip; existing unclosed-file
  ResourceWarnings in test_sensor_backfill remain.
* Core: python -m unittest discover -s tests -p test_historical_backfill.py -q:
  9 tests pass.
* Core: ruff check ., ruff format --check ., mypy: all pass,
  102 formatted files and 155 type-checked source files.
* API focused IoT/ingestion: 66 tests pass; configured lint and mypy pass
  (90 files). Full API discovery and final format/lint/mypy passed below.
* Initial core targeted lint found a 101-character test statement; split the
  context managers and reran the complete core checks above successfully.

Updated API/core guides and the existing IoT synthesis, index and append-only
knowledge-base log. No issue criterion or human-review checkbox ticked.
P07 Review, final evidence reconciliation, commit/push and PR update pending.
No scoped/full heavy gate, Azure, secrets, private data or uv used.

Pre-Review supplementary checks: pip check and git diff --check pass. AST
inventory confirms exactly 3 core and 4 API test methods added with no removals.
Added local documentation link/heading resolves. Fetched origin/main is
f183ba391de10fb7bcfc6157cbcbb2290b9cf4fc; correction base remains branch HEAD
39f0a433c67b74b7a74985f0c5c5a9af3e53cada. No upstream change touches the four
stream source/test files. No merge/rebase/history rewrite is authorized or
performed; hosted integration remains separate from this branch-local proof.

### Correction P07: Final validation and pre-Review reconciliation

* From src/api: PYTHONPATH=../core/tests:../agents/tests python -m unittest
  discover -s tests -q: 1142 tests in 458.785 seconds, OK, 314 existing opt-in/
  integration skips. Skips are not counted as actual Hub/SQL/live success.
* API configured ruff check ., ruff format --check . and mypy all pass:
  48 formatted files, 90 source files checked. These checks cover final source.
* Full API output is retained externally in the session files directory as
  iot110-api-units.log. Expected negative-path server tracebacks did not produce
  unittest failures; runner exit status is zero.
* Core final tests/lint/format/mypy and pip/diff/link/test-inventory checks are
  recorded above. Exactly seven focused methods were added, none removed.

Correction source scope P04-P06 is complete and review-ready. Plan markers,
details and current handoff agree; P07 publication remains unchecked until
the independent Review, commit and same-branch push are evidenced. Original
parent P03 and original Not accepted Review remain historical, not reapproved.
The source/test tree is frozen for the one correction Review. Only review/
state/plan/details/changes closeout evidence may be updated afterward.
Separate credential, actual Hub/SQL/model seam, budget and OD-43 gates remain.

### Correction Review and publication handoff

Exactly one independent correction Review executed and is preserved at
.copilot-tracking/reviews/2026-10-27/iot-consumer-110-review-addendum.md.
Execution: Complete. Outcome: Conformant for this bounded correction.
Original RV-001, RV-003, RV-002 are corrected with evidence; no new findings.
Independent checks include 9 core stream tests, 10 publisher/metadata tests,
adapted disk-free new receiver regression bodies, all 20 full/suffix/fault
wire-compatibility scenarios, targeted lint/format and exact source fingerprints.
The reviewer explicitly distinguishes these from parent-reported full suites.

The original Complete / Not accepted Review and parent state remain byte-
identical. No second critique or Review ran for the correction. No source/test
changes occur after Review; only closeout evidence is being updated.
P07 commit/push and PR evidence update are the remaining authorized actions.
No exact-future-commit, live, hosted or human acceptance is claimed by this
precommit source assessment. Refs only; no issue closure, merge or force push.

### Correction P07: Verified same-branch publication

Source and complete original correction evidence committed as
d553b1a51bcac5bcac884772581fa554cd5f8d68
(fix(src): enforce IoT send safety and replay provenance), with authenticated
account's repository-local noreply email for author/committer and the required
Copilot Co-authored-by trailer. All four frozen source/test SHA-256 values
match the independent Review's fingerprints; no source changed after Review.

Non-force push to origin feat/iot-consumer-110 succeeded. The existing draft
PR https://github.com/jmservera/ama/pull/508 was updated, not replaced; gh pr view
verified OPEN/draft and exact remote head d553b1a51bcac5bcac884772581fa554cd5f8d68.
The PR includes local command/count evidence, finding-by-finding dispositions,
all dated artifacts and explicit unproven criteria, using Refs only. The
worktree was clean after this first push. No new PR, issue closure, force push,
merge, Azure operation or heavy/full gate occurred.

P04-P07 and the ordered correction RPI task are complete. This evidence-only
closeout records the verified publication above and is committed/pushed on the
same branch; it changes no assessed source. Original adverse Review and parent
state remain unchanged. Current child state retains the separately running
automatic session awaiting owner selection; no follow-up task is started.
Hosted/human/actual Hub/SQL/credential/budget/OD-43 acceptance remains separate,
not inferred from successful local correction delivery.
