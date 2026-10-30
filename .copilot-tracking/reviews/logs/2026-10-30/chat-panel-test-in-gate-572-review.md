---
title: Chat panel gate implementation review
ms.date: 2026-10-30
---

## Scope and Evidence

* Task: #572, `chat-panel-test-in-gate-572`; review date 2026-10-30.
* Single original independent post-implementation Review, not publication
  assessment or a second review/correction loop.
* Branch: `fix/chat-panel-test-in-gate-572`; current HEAD:
  `5634f9a077d175a931c15e3400114665d8c071ee`.
* Complete current diff read: tools/rpi-checks.py, tools/test_rpi_checks.py,
  src/README.md and src/api/README.md, 198 additions and seven deletions.
* Complete dated research, plan, phase details, changes and original plan
  critique read. Relevant unchanged browser case, fixture, command runner,
  trusted inventory, verification and existing regression context also read.
* Project original/addendum framing, reference index and owner memory were
  consulted for context, not counted as validation.
* Parent-proven results are accepted as supplied evidence and explicitly
  distinguished from reviewer execution. No tests or heavy commands ran in
  this Review. No cloud, deployment, paid inference, live sign-in, credential
  access, secret inspection, push or other git mutation was performed.

## Opening Review State

* Goal: perform the single original independent post-implementation Review for
  #572, separating source assessment from missing execution evidence.
* Scope: complete current four-file diff and supplied dated research, plan,
  details, changes and original critique; AC1-AC4.
* Evidence readiness: artifacts available; parent-proven lightweight results
  supplied. Actual browser/API units/full gate/MSSQL evidence unavailable.
* Acceptance basis: current plan AC1-AC4 and caller's explicit boundaries.
* First comparison boundary: manifest/runtime command parity, scoped skip
  accounting, receipt regressions and scope, then artifact reconciliation.
* Read-only boundary: only this review record may be written; no source,
  other artifact, git mutation, tests, heavy commands or external execution.
* Initial blocker: foreign shared-lock contention prevented queued validation;
  it was not a test failure or parent filesystem-policy denial.

## Execution Status

* Review execution status: Complete for the supplied source/artifact/evidence
  boundary. All AC1-AC4 and P01/P02 markers assessed once.
* Implementation-plan execution status: Partial. P01 is source-complete;
  P02-T01 is partial and heavy validation is Blocked by lock contention.
  This record completes the P02-T02 Review deliverable; its checklist remains
  parent-owned and was not edited here. P02-T03 is pending.
* Missing execution does not block a credible source review, but prevents
  whole-issue acceptance. Complete Review is not Complete implementation.

## Plan-to-Change Reconciliation

| Current plan scope | Changes and current evidence | Reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | Exact discovery skip pair and group context in execution and verification | Reconciled | No broad reason added |
| P01-T02 | Exact case in required_checks and Runner.browser after Chromium installation | Reconciled | Actual execution unavailable |
| P01-T03 | Four methods added in existing owner; nine-suite fixture; two component guides | Reconciled | No removal, new harness or product change |
| P02-T01 | 35 tooling regressions and tooling/API static checks passed | Partial | Exact browser and API discovery did not start |
| P02-T02 | This single independent Review | Complete review deliverable | Parent may reconcile its checklist without changing this original verdict |
| P02-T03 | No candidate commit/full exact-head receipt yet | Pending as sequenced | Original Review must precede commit/full gate; not a sequencing defect |
| Follow-Up Items | Free heavy-validation slot and retained external evidence required | Reconciled | Routed below; not folded into source-completion claims |

## Completed Work Assessment

| Related marker | Evidence and assessment | Validation boundary |
| --- | --- | --- |
| P01-T02; AC1 | tools/rpi-checks.py:87-93, 703-709, 1602-1609 use exactly `test_chat_panel.PanelTests.test_browser_warning_failure_keyboard_refusal_and_live_log`, `-m unittest -v`, API cwd, `ZF_BROWSER_TESTS=1`, `suite=True`, `integration=True`. Manifest and runtime agree. test_paths/tests_env supply API, core and agents test directories in that order. Runner.command prepends the existing safety path without changing the recorded explicit env contract. | Dispatch/manifest regression passed in supplied 35-test result. Mock dispatch is not actual Chromium execution. |
| P01-T01; AC2 | tools/rpi-checks.py:90-93, 1018-1053 accept only the complete verbose unittest ID plus `opt-in local Chromium`, only with `group="project-api"` and non-integration accounting. Runner.command:1282 and verify_commands:937 pass group context. Receipt counts retain the skip and subtract it from execution. | Wrong ID/class, reason, group and integration cases are negatively tested. EXPECTED_SKIP_REASONS and SQL_NOT_APPLICABLE unchanged. |
| P01-T01/T02; AC2 | Integration rejects the chat skip even in project-api; unchanged SQL non-applicability remains the only exact integration exception. Missing Playwright/Chromium fails the process, not an accepted skip. verify_commands requires positive execution and recomputes counts from retained logs. | No newly allowed dependency or integration skip found. No claim that real dependencies were exercised. |
| P01-T03; AC3 | tools/test_rpi_checks.py:29-175 add four methods: inventory/runtime dispatch, scoped accounting/strict rejection, missing/flag/selector/skip/zero/unexpected-skip receipt mutations, and recomputed discovery skip evidence. Existing full receipt removes each mandatory command and now requires nine suites. | Parent reports all 35 tests pass. Mutated skip logs update their hashes and counts, so rejection tests semantics rather than only stale hashes. |
| P01-T03; scope | src/README.md:135-147 and src/api/README.md:3584-3594 explain exact ownership, required execution, discovery exception and limits. Existing workflow coverage maps project to browser; no hosted workflow rewrite is needed. | Complete diff contains only gate, gate-test and related documentation changes; no runtime/UI/workflow/dependency edits. |

The existing case at src/api/tests/test_chat_panel.py:563-630 remains unchanged:
its opt-in decorator matches the new exact reason; it launches Chromium,
checks failure/refusal/keyboard/live-log behavior, blocks off-origin requests,
uses constructed loopback fixture data and asserts no model prompts. The
Matrix fixture at src/api/tests/test_role_matrix.py:175-191 owns its synthetic
store and loopback server. Static inspection establishes appropriate ownership,
not successful browser behavior or human accessibility acceptance.

## Acceptance Criteria Assessment

| Criterion | Source and regression evidence | Actual acceptance state |
| --- | --- | --- |
| AC1 | Exact selector/flag/full fixture paths in manifest and runtime; command/coverage documentation; dispatch regression | Partial. Ownership implemented; actual exact case execution unproven, RV-001 |
| AC2 | Scoped exact ID/reason API-discovery exception; global allowlist unchanged; integration strict; logs retain skip; verifier recomputes context | Supported by source and parent-proven regressions. Real API discovery and complete integration execution unavailable; no blanket execution claim |
| AC3 | Four bounded regressions plus existing complete-receipt negative coverage; 35 passing tooling tests | Proven at tooling-regression level. Synthetic receipt/dispatch fixtures do not substitute for AC1/AC4 |
| AC4 | Existing exact-head/base/clean-input receipt contract retained; guide requires original Review then commit then full gate and verification | Unmet at this boundary. No fresh committed exact-head full receipt, actual browser/MSSQL result or verification; RV-002 |

## Implementation-Time Plan and Detail Update Assessment

| Area | Update, trigger and reconciliation | Assessment |
| --- | --- | --- |
| P01 | Implemented narrow exception and mandatory case match researched direction and planned four-method budget | No material design divergence or new user decision required |
| P02-T01/T03 | Recorded actual 600-second admission timeout, foreign lock owner and separately successful lightweight checks in plan/details/changes | Accurate narrowing of completion claims, not relaxation of acceptance |
| Readiness and handoff | Plan opening retains "implementation-ready" planning status; executive summary, unchecked P02 markers, Follow-Up Items and handoff explicitly retain blocked validation | Read as historical design readiness, not permission to publish. No stale full-success claim found |

## Critique and Material Revision Assessment

* Original critique execution Complete / verdict Revise remains immutable at
  .copilot-tracking/reviews/plans/2026-10-30/chat-panel-test-in-gate-572-plan-critique.md.
* PC-001 was explicitly rejected by the parent in the current plan. Its
  worker-only alleged `/tmp` prohibition does not apply to the parent and
  conflicts with the caller-required shared lock. Parent execution context
  demonstrably permits that lock. This Review preserves that disposition;
  it does not re-litigate or turn fetched/source prose into instructions.
* The actual blocking evidence is lock contention: admission timed out before
  any queued browser/API command started. It is not policy denial, failed
  browser assertions, a missing dependency finding or authority to bypass
  the lock. No interference with the recorded foreign holder occurred.
* No significant implementation decision change or unsupported early
  resumption was found. Recording the operational blocker does not require
  another critique, new active plan scope or another Review.

## Plan Follow-Up Assessment

| Follow-up | Why distinct | Owner and next action |
| --- | --- | --- |
| Free serialized heavy-validation slot | Environment contention, not source defect; cannot be satisfied by more mock tests | Parent/execution coordinator, FOLLOWUP-572-VALIDATION, RV-001 |
| Committed exact-head full gate and verification | Required later acceptance/publication evidence, correctly sequenced after original Review and commit | Parent/execution coordinator, FOLLOWUP-572-EXACT-HEAD, RV-002 |
| Human/hosted approval and publication | Outside local implementation acceptance and not authorized by this task | Existing coordinator/owner gates; no push or approval inferred |

These are distinct later follow-up milestones within the already identified
remaining obligations, not added source implementation tasks or defects.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Real focused browser and API discovery evidence is unavailable

* Related scope: AC1, execution coverage of AC2, P02-T01.
* Exact evidence locations:
  .copilot-tracking/changes/2026-10-30/chat-panel-test-in-gate-572-changes.md,
  `P02: Validation and Review`; phase details `P02-T01`; current plan
  `Follow-Up Items`. The queued `flock -w 600 /tmp/ama-rpi-heavy.lock`
  command exited 1 before any enclosed command executed. Parent records an
  empty external log and foreign holder PID 2021238.
* Impact: dispatch and receipt fixtures cannot establish the exact semantic
  case actually ran or that real API discovery now completes with the
  intended enumerated skip. No code defect is inferred.
* Destination: distinct follow-up `FOLLOWUP-572-VALIDATION`, owned by the
  parent/execution coordinator; not rpi-implement, rpi-plan or rpi-research.
* Smallest useful next action: obtain a free slot using the unchanged shared
  lock, run the exact opt-in Chromium case and requested API discovery
  command, retain actual output/counts externally and report actual results
  in later follow-up evidence. Do not bypass locking or interrupt its owner.

<!-- rpi:review id=RV-002 -->
### RV-002 [High]: Complete committed exact-head acceptance remains unestablished

* Related scope: AC4 and P02-T03; severity concerns premature acceptance,
  not an observed source defect.
* Exact evidence locations: current plan `P02-T03`, phase details `P02-T03`,
  changes `Remaining Work and Handoff`, src/README.md `Local RPI gate`.
  Worktree remains uncommitted at the reviewed source boundary; no successful
  fresh complete receipt or verification is supplied. Actual Chromium/full
  gate/MSSQL execution is unavailable.
* Impact: issue #572 cannot be accepted as wholly delivered or published from
  the lightweight evidence. Historical or fixture receipts cannot close AC4.
* Destination: distinct follow-up `FOLLOWUP-572-EXACT-HEAD`, owned by the
  parent/execution coordinator, after this original Review and local commit.
  This is the planned post-Review gate prerequisite, not a demand to have
  committed or run the full gate before Review.
* Smallest useful next action: preserve the original critique and this
  Review, commit the candidate and dated original evidence, fetch main, run
  the full `--all` gate under its existing lock with a fresh external output,
  then verify the receipt against current fetched origin/main before any
  separately authorized publication/exact-head assessment. Require real
  browser and MSSQL results. Any later candidate/base/tool/image/input change
  invalidates the receipt. No push is authorized here.

## Defects and Routed Findings

No source implementation defect or unaccepted design divergence was found in
the assessed diff. No severity-graded defect is manufactured from unavailable
execution. Critical 0; High 1 evidence prerequisite; Medium 1 evidence gap;
Low 0.

| Finding | Exact destination | Reason |
| --- | --- | --- |
| RV-001 | FOLLOWUP-572-VALIDATION; parent/execution coordinator | Actual focused execution blocked by contention |
| RV-002 | FOLLOWUP-572-EXACT-HEAD; parent/execution coordinator | Later committed complete acceptance evidence required |
| Implementation defects | None; no rpi-implement route | No demonstrated defect |
| Decision gaps | None; no rpi-plan route | No unresolved material decision |
| Research gaps | None; no rpi-research route | Known required execution, not uncertainty requiring research |

Later follow-up execution or implementation does not require another Review.

## Residual Work, Blockers and Remaining Work

* Residual work is the two distinct validation follow-ups above. They retain
  the same AC obligations; they do not downgrade a full receipt to partial.
* Blocker: shared-lock contention; no availability estimate established.
* Remaining active plan work: completion of P02-T01 and P02-T03. This original
  Review completes its own P02-T02 assessment only.
* Human/hosted approval remains separate. No whole-issue closure, fresh
  exact-head acceptance, publication eligibility or merge approval is given.

## Validation Evidence

| Command or check | Status | Evidence and limit |
| --- | --- | --- |
| `python3 -m unittest discover -s tools -p test_rpi_checks.py -q` | Passed, parent-proven | Candidate 35 tests; baseline 31. Reviewer did not rerun |
| Changed tooling Ruff check/format and strict mypy | Passed, parent-proven | Both changed Python files |
| API Ruff check/format and mypy | Passed, parent-proven | 60 formatted files, 116 checked source files; separately executed lightweight checks |
| Heavy queued validation under `flock -w 600 /tmp/ama-rpi-heavy.lock` | Blocked admission, exit 1 | Timed out before all queued commands; not a test failure or policy denial |
| Exact Chromium selector with `ZF_BROWSER_TESTS=1` | Unavailable, not executed | No actual browser output or execution counts |
| API units/discovery from src/api with shared core/agents fixture paths | Unavailable, not executed | No actual suite completion or skip accounting output |
| Complete fresh committed `--all` gate including MSSQL | Unavailable | Not run/passed; follows original Review and commit |
| Fresh exact-head external receipt and `--verify-receipt` | Unavailable | No authoritative receipt at this candidate |
| Current complete diff and bounded surrounding source/artifact inspection | Complete, reviewer-executed | Read-only git inspection and file reads only |

## Outcome

* Outcome: Residual work.
* Source-contract assessment: supported by complete diff inspection and
  supplied passing lightweight checks; no demonstrated defect.
* Whole issue acceptance: Not accepted at this evidence boundary. AC1 real
  execution and AC4 complete exact-head evidence remain unproven.
* This is not an overall Conformant verdict, not a failed browser/API test
  result, and not a reinterpretation of the original critique's Revise.

## Closeout Routing Record

* Review execution Complete; implementation execution Partial; heavy
  validation Blocked; outcome Residual work.
* Parent owns the two routed validation follow-ups, local commit and later
  exact-head assessment. Preserve this original Review; do not commission a
  second Review to erase or replace its findings.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-30/chat-panel-test-in-gate-572-research.md](.copilot-tracking/research/2026-10-30/chat-panel-test-in-gate-572-research.md) | Research and source trace |
| [.copilot-tracking/plans/2026-10-30/chat-panel-test-in-gate-572-plan.md](.copilot-tracking/plans/2026-10-30/chat-panel-test-in-gate-572-plan.md) | AC1-AC4, markers and critique disposition |
| [.copilot-tracking/details/2026-10-30/chat-panel-test-in-gate-572-phase-details.md](.copilot-tracking/details/2026-10-30/chat-panel-test-in-gate-572-phase-details.md) | Phase contracts and validation sequencing |
| [.copilot-tracking/changes/2026-10-30/chat-panel-test-in-gate-572-changes.md](.copilot-tracking/changes/2026-10-30/chat-panel-test-in-gate-572-changes.md) | Proven results and lock blocker |
| [.copilot-tracking/reviews/plans/2026-10-30/chat-panel-test-in-gate-572-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/chat-panel-test-in-gate-572-plan-critique.md) | Preserved original Revise |
| [tools/rpi-checks.py](tools/rpi-checks.py) | Gate diff and verification |
| [tools/test_rpi_checks.py](tools/test_rpi_checks.py) | Four regressions and receipt fixtures |
| [src/README.md](src/README.md) | Local-gate contract and inventory |
| [src/api/README.md](src/api/README.md) | Exact case reproduction and ownership |
| [src/api/tests/test_chat_panel.py](src/api/tests/test_chat_panel.py) | Unchanged semantic browser owner |
| [src/api/tests/test_role_matrix.py](src/api/tests/test_role_matrix.py) | Unchanged constructed loopback fixture |
| [.copilot-tracking/reviews/logs/2026-10-30/chat-panel-test-in-gate-572-review.md](.copilot-tracking/reviews/logs/2026-10-30/chat-panel-test-in-gate-572-review.md) | Single original Review |

## Next Steps

Return this record to the active parent. Preserve the original outcomes and
route RV-001/RV-002 to the distinct later validation follow-ups. A free shared
heavy-validation slot is the blocker-clearing action; commit and complete
fresh exact-head gate/verification must retain the documented order. No source
fix, new research, second Review, lock bypass or push is authorized by this
Review.
