---
title: Faster local gate 470 independent Review
ms.date: 2026-10-30
---

## Scope and Evidence

* Task ID: 470. Slug: faster-local-gate-470. Review date: 2026-10-30.
* Scope: one original independent post-implementation Review of the full
  supplied task boundary, including incomplete validation and acceptance.
* Base: 9ee48592a2e80e3a9f9e3c90ef039b9fa1987d19.
* Assessed HEAD: a5d483c65b70d249fb93d72f3f7a445eb1b0b934,
  ci/faster-local-gate-470.
* Complete base-to-HEAD diff read: src/README.md plus six new dated tracking
  artifacts. Complete tracked worktree diff read: plan, phase details, changes
  and RPI session state. The initialized untracked Review was also read.
  The only source delta is the 40-line benchmark recipe in src/README.md.
* Plan: .copilot-tracking/plans/2026-10-30/faster-local-gate-470-plan.md.
* Phase details: .copilot-tracking/details/2026-10-30/faster-local-gate-470-phase-details.md.
* Critique: .copilot-tracking/reviews/plans/2026-10-30/faster-local-gate-470-plan-critique.md.
* Changes: .copilot-tracking/changes/2026-10-30/faster-local-gate-470-changes.md.
* Research: .copilot-tracking/research/2026-10-30/faster-local-gate-470-research.md.
* Supporting contracts: tools/rpi-checks.py admission, scheduling capacity,
  receipt construction and verification; relevant tools/test_rpi_checks.py
  test inventory; src/README.md local gate and publication requirements.
* External evidence read directly: gate-tests.log, api.log error blocks and
  summary/static results, empty api-with-node.log, serial-a5d483c6.log and
  resources.json under /mnt/ama-rpi-gates/issue470-20261030-validation.
  The serial output directory was inspected for a receipt; none exists.
* Required project context was read, with bounded reads for large context
  documents. Remote #470/#475 provenance is supplied by the research and task
  direction, not independently refreshed during this Review.

## Opening Review State

* Interpreted goal: assess delivered benchmark documentation against the plan,
  original PC-001 disposition, existing runner contracts, all five issue
  criteria and actual external logs.
* Review scope: complete delivered/blocked task, not just the documentation.
* Evidence readiness: matching research, plan, details, critique, changes and
  adverse logs are available and sufficient for an honest bounded verdict.
* Acceptance basis: existing merged functionality is not reimplemented;
  remaining AC4 requires comparable successful full timings recorded in a PR.
* First comparison boundary: reconciliation and benchmark qualification,
  followed by actual validation evidence and routing.
* Active read-only boundaries: only this Review record may be written. No
  source/artifact/state correction, heavy checks, installations, agents,
  credential access, Azure, commits or publication are authorized.
* Initial blockers: full serial gate and corrected API validation failed shared
  lock admission; no successful full timing or final exact-head receipt exists.

## Execution Status

* Execution status: Complete.
* Review execution evidence: the complete supplied diff, current task artifacts,
  relevant runner contracts and external results were assessed on 2026-10-30.
  All findings and dispositions are recorded here; no second Review is planned.
* Implementation execution remains Partial: P01 is complete, P02 validation is
  blocked, and the benchmark attempt was disposed without successful timing.
  Complete Review execution does not mean complete implementation or acceptance.
* Review performed read-only inspection and lightweight Git whitespace checks
  only. Existing tests were not rerun. No other artifact was changed.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01 / P01-T01 checked | Existing-runner benchmark documented | Reconciled | Exact source delta matches scope; no runner or test change |
| P02 / P02-T01 unchecked | 35 gate tests and static passes; API failure and corrected admission timeout | Reconciled, incomplete execution | Remains unchecked; RV-002 |
| P02-T02 checked | Serial admission timeout; parallel not launched | Reconciled attempt disposition | Checked means attempt concluded, not full benchmark passed; RV-001 |
| P03 / P03-T01 unchecked | Review and local handoff pending | Reconciled at entry | This record completes only the Review portion; evidence commit/handoff is parent-owned and remains unclaimed |
| Follow-Up Items | Coordinator PR recording, free admission and final exact-head gate | Reconciled | Existing active gaps are not erased by follow-up wording; distinct routes below |
| RPI session state | Active Review; two admission/publication blockers | Reconciled | No contrary success or receipt claim; state not modified by reviewer |

No unchecked task is claimed complete. Plan "Ready" is planning readiness, not
release readiness. Details permit assessment after attempt disposition; P03 does
not require pretending that the P02 validation succeeded.

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | src/README.md | Reproducible same-candidate serial/parallel procedure for the sole remaining criterion | a5d483c65b70d249fb93d72f3f7a445eb1b0b934; 40 added lines | Direct contract comparison; whitespace passed | Conformant documentation, not measured acceptance |
| P02-T01 | Existing tools/test_rpi_checks.py, unchanged | Verify merged selection, scope and scheduling behavior | gate-tests.log: 35 tests, 11.897 s, OK | Existing result inspected, not rerun | Regression evidence supports AC1/AC2/AC3/AC5 within its limits |
| P02-T02 | External serial output/log | Attempt full serial admission without nested locking | Exact candidate/base command in changes; explicit lock timeout log | No receipt or execution interval | Attempt disposition supported; benchmark incomplete |

### Documentation-to-runner contracts

* main and heavy_lock own the shared lock internally. The new recipe correctly
  uses --lock-timeout 600 directly and forbids an outer flock around the runner.
  Other heavy bundles must coordinate with that lock.
* main prints queued/acquired timestamps after successful lock admission and
  worker_limit. Runner records effective jobs in receipt.jobs. Requested three
  is not proof of more than one admitted worker.
* Runner.run cleans owned resources before assigning receipt.sealed. The chosen
  acquired-to-sealed interval includes setup/checks/cleanup, excludes queueing,
  and ends before later receipt metadata/hash work and final verification.
  It is an explicitly defined comparable execution interval, not total CLI
  latency or a sum of overlapping command durations.
* main requires a new external output path; no changed/resume mode is used in
  the pair. Same clean committed HEAD/base, identical extras and comparable
  execution conditions are required.
* verify defaults to full scope and rejects partial evidence before live probes.
  The recipe independently verifies both full receipts and preserves failed
  evidence; no scope weakening or reuse of historical partial timings occurs.
* Serial admission one, parallel admission above one, matching conditions and
  explicit cache/download/scanner/order qualifications implement PC-001.
  No unsupported positive speedup or statistical guarantee is promised.
* Later evidence commits invalidate final publication applicability without
  deleting historical benchmark observations. No benchmark receipt exists here.

### Acceptance dispositions

| Criterion | Reviewed evidence | Disposition |
| --- | --- | --- |
| AC1 | Existing changed-path mapping/closure, unusual-path and scoped receipt tests; 35-test OK | Supported by focused regressions; functionality already merged in #475 |
| AC2 | Existing test_partial_scope_is_rejected_by_default_before_live_probes and verify contract | Supported by focused regressions; no full receipt supplied |
| AC3 | Existing independent overlap, thread-local logging, SQL/image serialization, shared-environment ordering and cgroup/capacity tests | Supported at regression level for merged functionality; no new successful full parallel execution |
| AC4 | Serial lock timeout, absent receipt, no parallel attempt and no PR timing record | UNMET; neither full execution timing nor comparable before/after measurement exists |
| AC5 | Existing canonical gate suite: 35 tests, OK | Supported by existing run |

Fixture-produced "FAILED", timeout, missing-tool and "VERIFIED full" messages
inside gate-tests.log are expected test stimuli/results at fixture identities,
not actual candidate gate failures or successful full candidate receipts.

## Implementation-Time Plan and Detail Update Assessment

| Affected area | What changed and why | Triggering evidence / decision | Reconciliation | Planning / critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 / P02-T02 | Added actual parallel admission and comparability qualifications | Original PC-001; direct correction within existing intent | Plan requirements, details and source recipe agree | Original Revise preserved; finding disposition recorded | No significant/divergent decision or fresh critique needed |
| P02-T01 | Preserved initial failure; corrected validation PATH without source changes | All 76 errors are missing-node FileNotFoundError; corrected attempt blocked | Plan unchecked, details blocked, changes retain both attempts | Execution-environment correction, not new scope | Honest incomplete validation; RV-002 |
| P02-T02 / Follow-Up Items | Checked attempted execution disposition; retained missing benchmark | Serial lock timeout before admission; no repeat parallel queue | Plan, details, changes and state preserve AC4 unmet | Existing stop rule allows shared-prerequisite blocker disposition | No unauthorized gate weakening; RV-001 |
| P03 | Review proceeds on delivered/blocked evidence | Credible evidence set despite incomplete validation | Review/handoff remains unchecked in supplied plan | Assessment only, no fixes or publication | No false completion; parent owns later handoff |

## Critique and Material Revision Assessment

* One original critique executed Complete with verdict Revise. That historical
  verdict remains unchanged; it is not retrospectively relabelled Pass.
* PC-001, Medium, is applied to the planning and documentation boundary:
  admitted-worker eligibility, comparable inputs/resources/tool identities,
  identical elapsed boundaries and adverse-evidence qualification are present.
* Its prospective measurement evidence remains absent, explicitly covered by
  RV-001 rather than fabricated as a completed comparison.
* No significant/divergent implementation decision, new test ownership,
  optimization redesign or change in confirmed user intent was found.
* Dependent work was not resumed under a false acceptance claim. Skipping a
  second queued full run after the same foreign-lock failure follows the
  accepted stop rule. No re-critique or re-review is required by this record.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner / next action | Assessment and route |
| --- | --- | --- | --- |
| Actual timings in delivery PR | Publication not authorized in local-only task | Coordinator records qualifying measurements only when separately authorized | Open; AC4 stays unmet, measurement route RV-001 |
| Free admission for API and benchmark | Reviewer cannot interrupt foreign owner or launch heavy work | Coordinator arranges safe availability; separate evidence work items | Open; RV-001 and RV-002, not new active plan scope |
| Final exact-head gate and publication approvals | Later evidence commit and authorization boundary | Coordinator obtains final gate/verification and human/hosted approvals | Distinct non-blocking handoff residual RV-003; publication itself remains blocked |

These are not newly invented implementation defects. Existing incomplete
P02-T01 and AC4 remain incomplete even where follow-up prose names their owner.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Mandatory full timing acceptance is unproven

* Related scope: AC4; P02-T02; PC-001 measurement evidence.
* Evidence: changes records the full serial command at a5d483c6/base 9ee48592
  with --all --jobs 1 --lock-timeout 600 and output
  /mnt/ama-rpi-gates/issue470-20261030-serial-a5d483c6.
  serial-a5d483c6.log explicitly says "BLOCKED: Global heavy-resource lock
  timeout"; the output directory contains no receipt. Parallel was not launched.
* Impact: no admitted jobs, acquired-to-sealed interval, verified full pair or
  PR timing record exists. Neither the 600-second admission wait nor historical
  partial timing is a full benchmark. This prevents whole-issue acceptance.
* Destination: rpi-research, distinct follow-up 470-full-timing-evidence,
  owned by the coordinator/evidence collector; no runner fix is indicated.
* Smallest useful next action: arrange safe free admission and capacity for
  parallel jobs above one, then collect a qualifying same-candidate/base full
  serial/parallel pair into new immutable external directories. Verify both full
  receipts, compare conditions, calculate identical intervals and retain all
  adverse history. Coordinator must subsequently record the actual qualified
  timings in its separately authorized PR before AC4 can be proven.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Required corrected API validation has no execution result

* Related scope: P02-T01, not a source regression attributed to this candidate.
* Evidence: api.log reports 1370 tests in 345.040 s, errors=76, skipped=318,
  unittest=1. Direct inspection confirms all 76 ERROR blocks contain
  FileNotFoundError for node. API lint, format and mypy return zero.
  api-with-node.log is zero bytes; changes/details report the PATH-preserving
  corrected bundle exited on flock admission after 600 seconds.
* Impact: missing Node in the first invocation was a validation-environment
  error, not evidence that the benchmark documentation broke API behavior.
  Correcting PATH is not proof that tests passed; required API validation
  remains incomplete and its skip applicability is not independently accepted.
* Destination: rpi-research, distinct follow-up 470-corrected-api-evidence,
  owned by the coordinator/validation executor, separate from benchmark work.
* Smallest useful next action: after safe admission, execute the documented
  complete API bundle with installed Node discoverable through preserved PATH,
  retain its exit/skip/static evidence and diagnose any remaining failures
  without altering the historical first-run evidence.
* Evidence limitation: the empty corrected log cannot independently prove
  timeout duration or command identity. That disposition comes from the
  reconciled changes/details and supplied execution account; no API execution
  or pass is inferred from silence.

<!-- rpi:review id=RV-003 -->
### RV-003 [Low]: Final publication handoff remains a distinct gated follow-up

* Related scope: P03-T01 and plan Follow-Up Items.
* Evidence: supplied plan leaves P03 unchecked; current tracking changes are
  uncommitted. No final full receipt exists, no current-main refresh/receipt
  verification was performed here, and human approval is not evidenced.
* Impact: this completed Review and historical focused tests cannot authorize
  publication or represent final exact-head acceptance. This is expected
  out-of-scope handoff work, not a defect in the delivered recipe.
* Destination: distinct follow-up 470-final-publication-handoff, coordinator.
* Smallest useful next action: preserve the original critique/Review and adverse
  logs; complete permitted local evidence handoff under parent authority.
  Before any later authorized push, obtain a fresh final exact-head complete
  gate against fetched current main and immediately verify its external receipt;
  retain independent exact-head, human and hosted approval requirements.
  Any later input/commit/base/tool/image change invalidates that gate.

## Defects

* No implementation defect identified in the scoped source delta. No route to
  rpi-implement for a source fix and no route to rpi-plan for a decision gap.
  Missing measurement and validation evidence must not be manufactured into
  source changes or a new optimization project.

## Routed Findings

| Finding | Destination | Owner / next action | Reason |
| --- | --- | --- | --- |
| RV-001 High | rpi-research: 470-full-timing-evidence | Coordinator / qualifying full pair and eventual PR timing record | Mandatory measurement gap |
| RV-002 Medium | rpi-research: 470-corrected-api-evidence | Validation executor / PATH-preserving full API bundle after admission | Separate required validation gap |
| RV-003 Low | Distinct follow-up: 470-final-publication-handoff | Coordinator / final candidate gate and approvals when authorized | Expected out-of-scope publication residual |

Later work does not require this original Review to run again.

## Residual Work

* Keep all three destinations distinct. Do not silently add them as completed
  active tasks or treat the publication follow-up as an implementation defect.
* Shared cache/image reuse remains outside this issue's remaining scope.
* Required human approval: [ ] Unchecked; no approval was granted by Review.

## Blockers and Remaining Work

* Foreign shared-heavy-lock admission blocks actual full benchmark and corrected
  API evidence. Review did not inspect foreign results, interrupt ownership,
  acquire that lock or execute a heavy check.
* Resource snapshots are pre-admission observations only. Four affinity CPUs
  and recorded MemAvailable 9,335,900 kB do not establish later admitted jobs;
  the earlier reported cap of three requested to one is not a full parallel run.
* Remaining active work at supplied boundary: P02-T01 and parent-owned P03-T01
  evidence commit/handoff. This record supplies only P03's Review component.
* Successful controlled full timing, AC4 PR recording and final publication
  remain UNMET. No closing keyword, issue closure or push is justified.

## Validation Evidence

| Command / evidence | Scope | Status | Summary |
| --- | --- | --- | --- |
| cd tools; python3 -m unittest -q test_rpi_checks; gate-tests.log | Existing gate regressions | Passed, existing run | 35 tests, 11.897 s, OK; fixture diagnostics are not candidate full-gate receipts |
| Gate Ruff lint/format and strict mypy | Unchanged tooling | Passed, reported | Changes records two formatted/typed files; separate raw static logs not supplied, not rerun |
| Required API unittest discovery; api.log | Existing API tests | Failed | 1370 tests, 76 missing-node errors, 318 skips; 345.040 s; not benchmark timing |
| API Ruff lint/format/mypy; api.log | Existing API static checks | Passed, existing run | lint=0, format=0, types=0; 60 formatted files, 116 typed files |
| Corrected complete API bundle; api-with-node.log | Required API validation | Unavailable: admission blocked | Zero-byte log; bounded flock timeout reported in reconciled artifacts; no tests executed |
| --all --jobs 1 --lock-timeout 600 at supplied HEAD/base | Full serial gate | Unavailable: admission blocked | Explicit Global heavy-resource lock timeout; no receipt or execution interval |
| --all --jobs 3 | Full parallel gate | Skipped | Not launched after common serial admission blocker; not a passed check |
| Comparable full timing / independent receipt verification | AC4 | Unavailable | No complete pair or full receipt; no speedup calculation possible |
| git diff --check; git diff BASE HEAD --check | Tracking/source whitespace | Passed during Review | Lightweight read-only checks; not a test suite or publication gate |
| Final exact-head complete gate / current-main receipt verification | Publication | Unavailable | No receipt; later evidence commit and current-main/approval gates remain coordinator-owned |

No installation, full suite, scanner, browser, SQL, Docker validation, remote
lookup or publication was run during this Review.

## Outcome

* Outcome: Not accepted.
* Rationale: the benchmark documentation is conformant to the scoped plan and
  runner, and the blocked attempt is honestly reconciled. However, the supplied
  full task cannot be accepted because mandatory AC4 is still unmet and required
  corrected API validation is incomplete. This is not a finding that the new
  documentation caused the initial API errors or a demand for duplicate features.
* Severity summary: one High material measurement gap, one Medium validation
  gap, one Low distinct publication follow-up; no Critical finding or source
  implementation defect.

## Closeout Routing Record

| Finding class | Destination | Owner / next action |
| --- | --- | --- |
| Implementation defect | None | No source fix indicated |
| Decision gap or invalid assumption | None | Approved intent and PC-001 preserved |
| Material evidence gap | rpi-research, two distinct later evidence items | Coordinator arranges safe admission; RV-001 full timings and RV-002 corrected API result |
| Non-blocking residual work | 470-final-publication-handoff | Coordinator handles final receipt, human/hosted approvals and authorization separately |

* Review execution status: Complete; implementation execution: Partial.
* Outcome: Not accepted for full-task/issue acceptance.
* Coverage: existing 35-test pass and API static passes; first API discovery
  failed; corrected discovery and full benchmark blocked/unperformed.
* No re-review, fixes, state changes or publication were performed or requested.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/reviews/logs/2026-10-30/faster-local-gate-470-review.md](.copilot-tracking/reviews/logs/2026-10-30/faster-local-gate-470-review.md) | This single original Review |
| [.copilot-tracking/research/2026-10-30/faster-local-gate-470-research.md](.copilot-tracking/research/2026-10-30/faster-local-gate-470-research.md) | Current research and #470/#475 provenance |
| [.copilot-tracking/plans/2026-10-30/faster-local-gate-470-plan.md](.copilot-tracking/plans/2026-10-30/faster-local-gate-470-plan.md) | Plan markers and acceptance boundary |
| [.copilot-tracking/details/2026-10-30/faster-local-gate-470-phase-details.md](.copilot-tracking/details/2026-10-30/faster-local-gate-470-phase-details.md) | Phase contracts and blocked disposition |
| [.copilot-tracking/reviews/plans/2026-10-30/faster-local-gate-470-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/faster-local-gate-470-plan-critique.md) | Preserved original Revise and PC-001 |
| [.copilot-tracking/changes/2026-10-30/faster-local-gate-470-changes.md](.copilot-tracking/changes/2026-10-30/faster-local-gate-470-changes.md) | Actual execution, errors and remaining work |
| [.copilot-tracking/rpi-sessions/2026-10-30/faster-local-gate-470-state.json](.copilot-tracking/rpi-sessions/2026-10-30/faster-local-gate-470-state.json) | Read-only parent continuation state |
| [src/README.md](src/README.md) | Assessed source recipe |
| [tools/rpi-checks.py](tools/rpi-checks.py) | Timing, admission and receipt contracts |
| [tools/test_rpi_checks.py](tools/test_rpi_checks.py) | Existing regression contracts |

## Next Steps

Return this one Complete / Not accepted Review to the active parent. Preserve
the original critique and findings, leave human approval unchecked, and route
RV-001/RV-002 to distinct later evidence work after safe admission. Coordinator
owns RV-003 and any separately authorized local handoff or future publication.
No source fix, re-review, push or further user action is authorized by this
Review.
