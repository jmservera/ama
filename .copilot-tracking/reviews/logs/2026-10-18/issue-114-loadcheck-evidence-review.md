---
title: Issue 114 loadcheck evidence original independent Review
description: One bounded post-implementation Review of the frozen loadcheck evidence candidate
ms.date: 2026-10-18
---

## Scope and Evidence

* Task: issue-114-loadcheck-evidence, issue #114; original independent Review.
* Original base: f91353169756dc41ebbcca944bdd3f44f7c04b89.
* Frozen candidate and observed HEAD: e63426148b5bac564ffef4195a9ba3b1b873d068.
* Verified source SHA256: 7cd7a506e439f0814320cfb7b22e6a3f94b47a18ba255f8eb45dec7e5f581dfb.
* Verified tests SHA256: b45296f3a9eec3478fb3c68987b85b68a538a22ffad6793c5bfa50ebd01100d2.
* Branch: fix/loadcheck-evidence-114.

## Opening Review State

* Interpreted review goal: assess the complete bounded evidence-trust change, not close issue #114 or establish performance improvement.
* Review scope: requirements, current plan and details, critique dispositions, changes and state evidence, the two changed Python files, and bounded offline validation.
* Evidence readiness: supplied canonical artifacts are identified; source/test identities verified. Artifact contents and reconciliation remain to be assessed.
* Acceptance basis: bounded plan and issue AC2 evidence integrity, public CLI behavior, preflight validation, worker accounting, retained healthy evidence, raw latency comparisons, and truthful scope limits.
* First comparison boundary: reconcile the supplied artifact set before assessing frozen source and tests.
* Active read-only boundaries: only this original Review record may be written. No source corrections, other artifact edits, nested agents, inherited services, private data, remote writes, or integration.
* Initial blockers: none known. Existing dirty changes are restricted to parent-owned changes/state records and will not be modified.

## Execution Status

* Execution status: Complete.
* The single original Review compared the complete supplied bounded task and ran independent offline validation on the frozen candidate. This is Review execution status, not full-plan publication or issue completion.

## Plan-to-Change Reconciliation

| Current plan scope | Changes evidence | Reconciliation | Assessment |
| --- | --- | --- | --- |
| P01-T01 guards and evidence accounting | Harness correction and initial regression proof | Reconciled | Implemented in the canonical source; oversized numeric duration remains an uncovered preflight defect, RV-001. |
| P01-T02 focused and coupled validation | Validation Record; Regression and mutation details | Reconciled | Exactly 16 new test methods; no removals or configuration exemptions. Independently rerun 16 focused and 59 coupled tests, configured static checks, original-source red probe, four mutants and neutral-clock equality. |
| P02-T01 original Review | Candidate Source Identity; Pre-Review Reconciliation | Reconciled | Candidate and source/test pins match. This record is the one original Review; adverse finding must remain preserved. |
| P02-T02 publication | Remaining Work; Return-to-Caller State | Pending by design | Publication is parent-owned after Review, not missing implementation evidence or a completed task. |
| Follow-Up Items | Follow-Up Items and validation exclusions | Reconciled | Live performance/cost, annual ledger, DH-005 and human acceptance remain outside active work and unfulfilled. |

The plan and details mark P01 complete and P02 incomplete/review-ready. Changes correctly says full-plan execution is Partial. Parent-owned state advances active_phase to Review, pins the same candidate and leaves publication pending. The changes record's final "Current phase Implement" is its descriptive implementation handoff, not a competing Review completion claim. No stale artifact prevents assessment.

## Completed Work Assessment

| Marker | Files | Assessment and evidence |
| --- | --- | --- |
| P01-T01 input guards | src/core/src/zava_forward/core/synthetic/loadcheck.py:25-30,46-58,107-124 | Positive integer homes/sessions/writers, writer range, finite positive ordinary numeric durations and empty cases reject before the specified workload boundaries. CLI nonfinite strings reject through argparse. Oversized integer duration bypasses CLI preflight and raises the wrong API exception; RV-001. |
| P01-T01 absent evidence | src/core/src/zava_forward/core/synthetic/loadcheck.py:41-43,99-106 | Empty pct is None. Missing classes retain n=0, null p50/p95/max and within=False. No missing observation can satisfy the class predicate. No invented sample quota or new max gate. |
| P01-T01 failures/privacy | src/core/src/zava_forward/core/synthetic/loadcheck.py:62-97,135 | Request failures count by class; ordinary worker-boundary failures count as session errors; documented Thread.start RuntimeError counts as startup. Only started workers are joined. Positive evidence from healthy classes survives, while overall CLI errors force 1. Types, not exception text, enter reports. Explicit request/worker exception boundaries are justified, not forbidden silent broad fallback; no BaseException catch. |
| P01-T01 timing | src/core/src/zava_forward/core/synthetic/loadcheck.py:60-81 | One shared monotonic deadline, perf_counter for request elapsed, completion captured before aggregation locking. Late workers add nothing, but an entered cycle finishes. Deadline includes startup skew; no new cancellation/barrier behavior is claimed. |
| P01-T01 unchanged successful contract | src/core/src/zava_forward/core/synthetic/loadcheck.py:22,68-74,99-106,109-111 | Default five sessions/two writers, list/detail/write requests and 1/1/2-second limits unchanged. Raw p95 determines within before four-decimal display rounding. Neutral-clock old/new reports independently compare exactly equal. |
| P01-T02 tests | src/core/tests/test_loadcheck.py | 16 methods cover absence, bad inputs, failure categories, healthy retention, real-worker aggregation, actual main() JSON/0/1 outcomes and deterministic timing distinctions. Fixtures are constructed; CLI environment is cleared and factory mocked. Nonfinite CLI spellings independently tested. Oversized numeric input is not covered. |

## Implementation-Time Plan and Detail Update Assessment

| Area | Change and trigger | Intent/reconciliation | Assessment |
| --- | --- | --- | --- |
| P01-T02 timing | PC-001 required falsifiable clock, late-worker, entered-cycle and lock-wait assertions plus timing mutants. | Present in both plan and details; tests implement them. Independently detected wall-clock and completion-inside-lock mutants. | Compatible correction, no divergent decision or new critique required. |
| P01-T02 scratch | PC-002 recommended a local scratch root and scoped tempfile.tempdir override despite its unverified parent-authority assertion. | Plan/details/changes explicitly reject that authority assertion while independently adopting isolation. Tests assert temporary paths and deletion. | Properly dispositioned without rewriting the original critique. This Review uses its separately authorized exact local scratch root. |
| P01 annotations/test typing | Strict mypy failures led to typed public signatures and typed test imports/fixtures; formatting was tool-owned. | Source/test footprint and behavior remain bounded. pyproject.toml is unchanged from the base. | No new mypy exceptions or architectural abstraction; dynamic Store boundary remains Any. |
| P02 candidate pin | Parent records source/test hashes and Review phase after the source candidate commit. | HEAD and hashes match; dirty changes/state remain parent-owned and were not edited. | Descriptive readiness update only; no material scope revision. |

## Critique and Material Revision Assessment

* Original critique verdict remains Revise, execution Complete, two Medium findings PC-001/PC-002. Its SHA256 independently verifies as 6f40180f9bff6315e3a0296310a61ece41092f943c41b1d755dd16d293cd7012.
* Both findings have explicit direct planner dispositions in the current plan and details, mirrored in changes. Timing criteria and scoped test temp-root behavior are implemented and independently exercised.
* No significant divergent decision, changed acceptance criterion, new workload, source-file expansion, or unapproved dependent-work resumption was found. The two compatible dispositions do not require another critique.
* Candidate diff against the exact original base contains only the two allowed Python files and six task artifacts. Publication, source correction and integration are not performed by this Review.

## Plan Follow-Up Assessment

| Follow-up | Why outside immediate scope | Owner/next action | Route |
| --- | --- | --- | --- |
| Issue #114 real Azure load, latency and cost | Requires separately authorized deployed-release measurements, fixed profile and actual service/cost evidence. | Owner/coordinator authorizes and schedules live acceptance work. | Distinct follow-up FU-114-LIVE; not RV-001 or active P01 scope. |
| Annual ledger verification | No ledger source or scheduled verification is changed by this evidence-harness slice. | Owner/coordinator obtains annual-ledger verification evidence separately. | Distinct follow-up FU-114-LEDGER. |
| DH-005 restore/deletion | Real Azure restore, deletion reapplication and storage controls are not exercised here. | Owner/coordinator schedules authorized recovery verification. | Distinct follow-up FU-114-RECOVERY. |
| Human/operational acceptance | Local generated fixtures and role/mock outcomes cannot establish it. | Owner/coordinator obtains required human acceptance. | Distinct follow-up FU-114-HUMAN. |

These existing unresolved items are not implementation defects, new active tasks or claims that issue #114 is complete. PRD exercise acceptance additionally requires declared warm-up, at least 200 interactive observations, deployed fixed-service evidence, thirty-minute workloads, additional classes and the separate twenty-session scale profile. No local result here establishes those gates or a performance improvement.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Oversized numeric duration reaches store initialization before failing validation

* Related scope: P01-T01/P01-T02; finite positive duration preflight, explicit direct-API ValueError and CLI argparse rejection before open_store.
* Exact source: src/core/src/zava_forward/core/synthetic/loadcheck.py:48 calls math.isfinite(seconds), which can itself raise OverflowError for Python integers outside float range. CLI --seconds uses unrestricted int at line 111 but checks only <=0 at lines 113-114; open_store executes at line 130 before run reaches that check at line 132.
* Independent reproduction: construct seconds = 10**400. Calling run(Mock(cases={"SYN-1": {}}), {}, seconds, 1, 1) raises OverflowError: int too large to convert to float, rather than the specified ValueError. With a local generated seed containing one case and a Retrofit Programme Manager, cleared environment, scoped local tempfile.tempdir and mocked factory, main(["--data", seed_path, "--homes", "1", "--seconds", str(10**400)]) raises the same OverflowError after open_store has been called exactly once.
* Observed output: DIRECT_HUGE_DURATION OverflowError int too large to convert to float; CLI_HUGE_DURATION OverflowError open_store_calls 1. By contrast, independent CLI nan/inf/-inf probes each exit 2 and call the factory zero times.
* Impact: A parser-accepted numeric duration that cannot enter the timer arithmetic escapes the promised pre-store guard and static parser error contract. With a real configured backend, store initialization could occur before the predictable rejection. No real backend, cloud side effect or privacy disclosure was exercised or asserted. This is a bounded validation defect, not a false-green successful report.
* Destination: rpi-implement, active parent; compatible correction within the current accepted direction.
* Smallest useful next action: make numeric duration representability/finite validation total for the supported numeric API input and run the equivalent check in main before opening data/store; normalize unsupported/overflowing duration to explicit ValueError for direct calls and argparse error for CLI. Do not add an arbitrary workload cap or change ordinary valid flags/defaults. Add subcases to existing parameter/CLI methods, preserving the 16-method budget and zero factory calls on rejection.
* Acceptance evidence for correction: the exact direct/CLI repro above rejects through the specified interfaces before store access, while existing valid duration, nonfinite/negative, default mix and 0/1 report tests remain green. Parent may record a separate correction receipt; this original Review remains unchanged and does not provide corrected-head acceptance.

## Defects

* RV-001: Medium input-validation gap; routed once to rpi-implement. No Critical/High/Low implementation findings identified.

## Routed Findings

| Finding | Destination | Owner/next action | Reason |
| --- | --- | --- | --- |
| RV-001 | rpi-implement | Active parent performs the bounded preflight correction and records exact reproduction/validation in a separate receipt. | Existing direction already requires explicit pre-store numeric validation; no new plan decision or research is needed. |

Later correction does not require another Review. No findings are withheld for a second original Review.

## Residual Work

* FU-114-LIVE, FU-114-LEDGER, FU-114-RECOVERY and FU-114-HUMAN remain distinct owner/coordinator follow-ups, as assessed above.
* P02-T02 artifact reconciliation, privacy-safe commit and PR publication remain parent-owned. This Review does not commit, push, mutate issue/board/PR state, integrate moving main or authorize merge.

## Blockers and Remaining Work

* No blocker prevented completion of this Review.
* RV-001 prevents unqualified acceptance of the bounded preflight contract on the frozen candidate.
* Full-plan publication and whole-issue/live/human gates remain pending, not Review execution failures.

## Validation Evidence

All independent Python validation used the already-installed editable core and the supplied executable /home/azureuser/.copilot/session-state/619ef4ca-dccb-4a9a-b8db-fb4de739c825/files/loadcheck-venv/bin/python; Ruff/mypy are its siblings. No dependency installation was needed. `V` below denotes that virtualenv, `R` the worktree root. Tests/probes used env -i with PATH=/usr/bin:/bin, PYTHONDONTWRITEBYTECODE=1 and TMPDIR=$R/.copilot-tracking/.issue-114-review-tmp. CLI probes additionally clear os.environ and mock the factory. No inherited service configuration or external services were used.

| Independent command/check | Status | Actual evidence |
| --- | --- | --- |
| git status --short; git branch --show-current; git rev-parse HEAD; sha256sum canonical Python files | Passed | Branch, exact candidate and both supplied SHA256 pins match. Initially only parent-owned changes/state were dirty. |
| git diff BASE CANDIDATE --stat and canonical source diff | Passed | Two allowed Python files and six task artifacts; no runtime dependency/configuration or unrelated source change. |
| V/bin/python -m unittest discover -s src/core/tests -p test_loadcheck.py -v | Passed | 16 tests in 0.090s; no skips. |
| cd src/core/tests; V/bin/python -m unittest test_sqlreads test_sqlstore test_taskqueues test_sqlqueues test_queue_benchmark -q | Passed | 59 tests in 95.567s; no skips. Together with focused tests, 75 independent green checks. SQLite/generated 60,000-case structural evidence only. |
| cd src/core; V/bin/ruff check --no-cache .; V/bin/ruff format --check --no-cache . | Passed | All lint checks pass; 71 files already formatted. Existing source migration exclusions are retained, not a claim that excluded source was freshly formatted. |
| cd src/core; V/bin/mypy --cache-dir $R/.copilot-tracking/.issue-114-review-tmp/mypy | Passed | No issues in 124 source files; existing migrated-module exemptions remain, and no new test exemption was added. |
| Inline offline numeric-duration/API/actual-main probe | Failed contract, reproduced | 10**400 gives direct OverflowError and CLI OverflowError after exactly one mocked open_store call; RV-001. nan/inf/-inf CLI strings each give argparse exit 2, zero factory calls. |
| Inline git-show/in-memory original-source replay against all 16 new methods | Expected red, detected | Original base: 23 failure and 19 error subtest outcomes across 16 methods. Checked-out source never replaced. |
| Four inline in-memory mutants against all 16 methods | Expected red, all detected | Empty percentile zero: 7 failures; missing-class pass: 6; wall-clock deadline: 18; completion inside lock: 1. Zero errors for each mutant. |
| Separate inline old/new neutral-clock good path | Passed | Reports exactly equal: list/detail n=5, write n=2; all p50/p95/max=0.125, within=True; errors=0, error_kinds=[]. |
| Final source/critique identity, diff whitespace and scratch cleanup | Passed | Both Python pins and original critique hash remain exact; HEAD remains e63426148b5bac564ffef4195a9ba3b1b873d068; git diff --check passes. Exact review scratch root removed. Final status contains only the original parent-owned changes/state modifications plus this new Review record. |

The parent's complete 14-mutant receipt, its initial failed dependency/format/mypy attempts and earlier 75-test run are attributed to the supplied changes record, not presented as independently rerun in full. This Review independently ran four of those mutations, the original red probe and equality check, plus current tests/static checks. In-memory mutation input is derived from the verified frozen source; no source correction was made.

Skipped with reason: full repository suites, migration regression, Docker/nonroot and real SQL-provider checks are outside this harness-only unchanged-layout/store/runtime-image boundary. No Azure load/latency/cost, actual AI, annual-ledger verification, DH-005 restore/deletion or human acceptance was performed. No private datasets, .env, support or inherited services were read. No web files changed or web review was required.

## Outcome

* Outcome: Not accepted.
* Rationale: Core missing-observation, failure-accounting, healthy-path, timing and CLI report predicates are supported by independent evidence. The complete promised numeric preflight boundary still has the reproducible Medium defect RV-001. This verdict applies only to the frozen bounded candidate, not to hypothetical corrected code or whole-issue acceptance.
* Severity summary: Critical 0; High 0; Medium 1; Low 0.

## Closeout Routing Record

| Finding class | Destination | Owner/next action |
| --- | --- | --- |
| Implementation defect | rpi-implement | Active parent: address RV-001 within permitted correction-cycle limit; preserve this original and record a separate correction receipt. |
| Decision gap or invalid assumption | None | No significant divergent decision was found. |
| Material research evidence gap within bounded task | None | Supplied evidence plus independent source/tests/probes support the bounded verdict. |
| Non-blocking residual work | Distinct follow-ups FU-114-LIVE/LEDGER/RECOVERY/HUMAN | Owner/coordinator controls separate authorization and acceptance. |

* Review execution: Complete.
* Outcome: Not accepted.
* Validation: 75 tests, configured static checks, original red probe, four mutants and exact healthy-path equality independently verified; one numeric-boundary repro fails contract.
* Blockers: none to Review execution; RV-001 remains to be corrected by the parent.
* Artifact identity: the final SHA256 of this record is returned to the parent after its last write; a self-referential digest is deliberately not embedded in the hashed file.

## Relevant Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-18/issue-114-loadcheck-evidence-research.md](.copilot-tracking/research/2026-10-18/issue-114-loadcheck-evidence-research.md) | C1-C8 and bounded issue-evidence scope |
| [.copilot-tracking/plans/2026-10-18/issue-114-loadcheck-evidence-plan.md](.copilot-tracking/plans/2026-10-18/issue-114-loadcheck-evidence-plan.md) | Current accepted direction, markers and follow-ups |
| [.copilot-tracking/details/2026-10-18/issue-114-loadcheck-evidence-phase-details.md](.copilot-tracking/details/2026-10-18/issue-114-loadcheck-evidence-phase-details.md) | Task-level requirements and critique dispositions |
| [.copilot-tracking/reviews/plans/2026-10-18/issue-114-loadcheck-evidence-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-18/issue-114-loadcheck-evidence-plan-critique.md) | Preserved original Revise critique |
| [.copilot-tracking/changes/2026-10-18/issue-114-loadcheck-evidence-changes.md](.copilot-tracking/changes/2026-10-18/issue-114-loadcheck-evidence-changes.md) | Implementation receipt and attributed validation |
| [.copilot-tracking/rpi-sessions/2026-10-18/issue-114-loadcheck-evidence-state.json](.copilot-tracking/rpi-sessions/2026-10-18/issue-114-loadcheck-evidence-state.json) | Parent-owned active Review state and candidate pin |
| [src/core/src/zava_forward/core/synthetic/loadcheck.py](src/core/src/zava_forward/core/synthetic/loadcheck.py) | Frozen production candidate |
| [src/core/tests/test_loadcheck.py](src/core/tests/test_loadcheck.py) | Frozen 16-method regression suite |
| [.copilot-tracking/reviews/logs/2026-10-18/issue-114-loadcheck-evidence-review.md](.copilot-tracking/reviews/logs/2026-10-18/issue-114-loadcheck-evidence-review.md) | This one original independent Review |

## Next Steps

The active parent should continue to rpi-implement for RV-001, if using an authorized source-correction cycle, and preserve this original Review and verdict unchanged. Record corrections, before/after identities and actual validation in a separate receipt; do not run another original Review or claim this record accepts corrected code. Keep distinct live/ledger/recovery/human follow-ups unmet, then perform only the authorized parent publication steps. This Review worker stops after returning the final artifact identity and hash. No user action is required.
