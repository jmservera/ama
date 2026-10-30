---
title: Safety consent 130 fix cycle 1 RPI Review
description: Independent bounded working-tree review for issue 130 and PR 509
ms.date: 2026-10-29
---

## Opening Review State

* Interpreted review goal: Perform the single independent post-implementation Review of fix cycle 1, not issue-wide acceptance or publication approval.
* Review scope: Working diff against HEAD ebcc0a16fc5815125681d858d2f74d772fde3063 in src/core/src/zava_forward/core/resident_decisions.py, src/core/tests/test_resident_decisions.py, src/core/README.md and src/api/tests/test_resident_api.py, plus the six supplied canonical task artifacts.
* Evidence readiness: Baseline, four-file dirty boundary and open PR 509 on docs/safety-consent-130 confirmed. Supplied task evidence is available for comparison; validation is reported evidence, not a new execution request.
* Acceptance basis: Preserve accepted resident decisions and heuristic while retaining tenure hold; prevent deleted nomination identity reuse; reconcile P01/P02 and pending P03 with critique dispositions and unchanged authority boundaries.
* First comparison boundary: Current plan, details, critique, research, changes and state against the bounded source diff and existing call paths.
* Active read-only boundaries: Only this review record may be written. No nested agents, tests, source edits, commits, pushes, Azure actions or latest.json updates.
* Initial blockers: None identified before evidence comparison.

## Scope and Evidence

* Task ID: issue-130-pr-509-fix-cycle-1; Refs #130, PR #509 only.
* Review date: 2026-10-29.
* Assessment count: Exactly one independent post-implementation RPI Review.
* Plan: .copilot-tracking/plans/2026-10-29/safety-consent-130-fix-cycle-1-plan.md.
* Phase details: .copilot-tracking/details/2026-10-29/safety-consent-130-fix-cycle-1-phase-details.md.
* Original critique: .copilot-tracking/reviews/plans/2026-10-29/safety-consent-130-fix-cycle-1-plan-critique.md.
* Changes: .copilot-tracking/changes/2026-10-29/safety-consent-130-fix-cycle-1-changes.md.
* Research: .copilot-tracking/research/2026-10-29/safety-consent-130-fix-cycle-1-research.md.
* State: .copilot-tracking/rpi-sessions/2026-10-29/safety-consent-130-fix-cycle-1-state.json.
* Direct evidence: Complete four-file working diff against ebcc0a16fc5815125681d858d2f74d772fde3063; relevant decision, intake, transaction, deletion, heuristic, lookup, projection-consumer and API fixture code; existing test structure and named safeguard coverage.
* Context: Original case study, addendum, knowledge-base index and owner memory; src/README.md and tracking retention policy. GitHub read-only inspection confirmed PR #509 is open on docs/safety-consent-130 targeting main and obtained issue #130's criteria.
* Boundary: This fixes two supplied regressions within existing intake, not all nomination/RAI criteria in issue #130. No issue criterion is ticked and no issue closure, final committed-head assessment or publication approval is implied.

## Execution Status

* Execution status: Complete.
* Review execution evidence: All six canonical input artifacts and the complete specified diff were compared on 2026-10-29. No nested agents or new test/static-check execution occurred.
* Implementation execution is separate: P01/P02 are evidenced complete; P03-T01 is fulfilled by this record, pending parent reconciliation. P03-T02 local evidence finalization and commit have not occurred at this review boundary.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01; AC1-4 | Three shared regression methods and two existing fixture updates; six original failures | Reconciled | Tests exercise JSON/SQLite persistence, ordering-sensitive heuristic equality, repeated deletion, missing legacy history, rejected stale writes and valid new correction. No test removed. |
| P01-T02; AC1-4 | Decision-only helper, UUID IDs and intake README additions | Reconciled | Exact source diff matches current plan; deletion implementation and retention metadata are untouched. |
| P02-T01; AC5 | Requested core checks, five relevant core modules, resident API module and changed API static checks | Reconciled | Command exits, counts, skips and explicit worktree import paths are recorded. Review relies on reported execution, not a rerun or receipt. |
| P02-T02 | Current plan/details and critique dispositions reconciled for handoff | Reconciled | Research and state retain the earlier counter proposal as history; current plan amendment and subsequent state disposition explicitly supersede it. |
| P03-T01 | One independent bounded working-candidate Review pending | Reconciled at review boundary | This record supplies the result; parent must update its owned markers and handoff without another Review. |
| P03-T02; AC6 | Local commit pending; no push | Pending as intended | Noreply attribution, trailer, final owned-file staging and committed status belong to the parent after this Review, not a claimed completed acceptance criterion. |
| Follow-Up Items | Human/operational acceptance and publication/hosted gates excluded | Reconciled | Distinct later owners/actions below; not hidden active implementation work. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T02 | src/core/src/zava_forward/core/resident_decisions.py | Extract _resident_decision_gate and use it for resident_status | Non-tenure retention, binding, current scope, acceptance, review and representative checks moved without substantive alteration | Reported six regressions and selected core suites pass | Accepted status no longer depends on tenure readiness. resident_gate still returns TENURE_HOLD before all decision checks, for both case and scoped work. No work-release bypass added. |
| P01-T02 | src/core/src/zava_forward/core/resident_decisions.py | Replace length-derived nomination IDs with NOM- plus uuid.uuid4().hex | Creation independent of deletable history; correction still uses exact k.find, version and owner checks inside _operation | Reported JSON/SQLite regression passes | Deleted legacy NOM-1 cannot match a new UUID identity. Retained sequential IDs remain lookup-compatible because no parser, migration or lookup contract changed. Full random UUIDs provide practical collision-resistant identity, not a mathematical zero-collision guarantee. |
| P01-T01 | src/core/tests/test_resident_decisions.py | Add exactly three methods inherited by SQLite and opt-in MSSQL; use returned ID in existing correction fixture | Complete diff retains existing assertions/tests; new checks compare durable state and audit after rejection/failure | Six constructed JSON/SQLite selectors fail original, pass fixed, per changes | Tests are semantic, not ID-pattern-only proxies. Tenure test compares complete heuristic results including reasons/citations and an ordering-sensitive competitor after reopening. Identity tests cover repeated deletion, legacy-only tombstone, rollback, stale refusal and valid correction. |
| P01-T01 | src/api/tests/test_resident_api.py | Use the returned first nomination identifier | Existing manual-route/correction/no-automatic-decision assertions unchanged | Reported resident API module and changed-file static checks pass | Correct opaque-ID client behavior without changing API or broadening runtime scope. |
| P01-T02 | src/core/README.md | Document opaque IDs, retained legacy IDs and status/readiness separation | Two additions in existing intake section match source | Read-only documentation/diff review | No new verification, consent, sending, booking, approval or release authority claimed. |

The shared helper continues to enforce expired retention, unknown/stale scope,
human-review holds and representative task/version/date/safe-contact bounds.
Existing store, insight, AI-source and SQL-write consumers continue to call the
common resident_status function; gate consumers remain on resident_gate.
Nomination IDs remain strings in the existing case payload, so this change adds
no schema, service, dependency or additional personal retention. The inspected
runtime consumers do not reconstruct sequential nomination identities.

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01/T02; AC3-4 | Initial counter proposal replaced with full UUID identities before implementation | PC-001 demonstrated an unrecoverable legacy high-water mark; user required non-reused identities, not sequential formatting | Functional requirements, ACs, tests, details, changes amendment and later state disposition all describe UUIDs | Original Complete / Revise preserved; explicit direct dispositions recorded, no second critique requested | Material design revision is ready and justified. It preserves user intent while avoiding new deletion persistence/privacy dependencies. |
| P01-T01; API fixture | Existing corrections now consume returned opaque IDs | Consequence of UUID amendment, not an unrelated interface redesign | Plan test ownership, details and changes identify both fixtures | Covered by amended plan and reported API checks | Appropriate narrow compatibility adjustment; no assertion removed. |
| P02-T01 | Explicit current-worktree source/test paths despite shared editable installs | Changes reports installed editable packages pointing elsewhere and module-origin verification | Details and changes specify core/API PYTHONPATH and no shared-environment mutation | Existing requested validation retained | Evidence identifies the tested source boundary without claiming shared environment changes or package installs. |

No unrecorded implementation-time expansion was found. The research's initial
counter recommendation and the state's earlier accepted counter entry are
historical, not the current direction: the plan expressly supersedes them and
the later state disposition records UUID adoption. They are not mistaken for
fresh evidence that a counter was implemented.

## Critique and Material Revision Assessment

* Original critique remains Complete / Revise, with 1 High and 3 Medium findings. This Review does not rewrite it as a pass or imply a fresh critique of the revised plan.
* PC-001: Accepted root cause. Full UUID issuance removes dependence on a recoverable deleted high-water mark; the added legacy-only-tombstone test covers the previously missing state. The critique's sequential-ID prescription was a planner preference, not confirmed user intent; the supplied caller clarification and current plan permit opaque non-reused identities.
* PC-002: Resolved by removing the counter/deletion dependency. delete_resident_records is unchanged and remains outside _operation; no new deletion atomicity guarantee is asserted. The added failed-intake test covers the modified issuance boundary instead. A store-wide deletion recovery rewrite would be unrelated scope.
* PC-003: Resolved by leaving deletion metadata unchanged. Existing exact tombstone/privacy assertions are preserved, not weakened.
* PC-004: Rejected with explicit disposition. Its tool-location restriction arose only in the critique worker and is not a repository or parent requirement. The supplied task and changes report actual requested tool execution successfully. This Review does not propagate that worker restriction or execute those tools itself.
* Dependent-work pause assessment: Current plan/details and changes consistently place UUID amendment and dispositions before implementation. No contrary sequence is evidenced; this is artifact-based assessment, not an independently observed execution timeline.
* Justification: The material revision addresses the critique's highest-impact defect without changing human authority, retained personal metadata, deletion semantics or the user's functional requirement. No unresolved significant decision requires rpi-plan or rpi-research.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Existing issue-wide, human and operational acceptance | This is a constructed two-regression fix, not all #130 nomination/RAI acceptance; actual authority, participant and professional evidence is not supplied | Issue #130 owner and qualified human approvers retain existing criteria and arrange separately authorized acceptance evidence | Remains distinct follow-up; no implementation defect or automatic child work. |
| Publication, exact committed-head gate and hosted checks | User authorizes local commit only, with no push or Azure; working-tree review cannot assess a future commit | Publication owner, only if later authorized, applies current repository gate policy, exact-head assessment and hosted/human controls | Not run and not approved here; does not block the bounded Review or authorize publication. |

Unresolved follow-up items remain outside active implementation and acceptance
claims. They are not converted into defects or added to P01/P02.

## Findings

No substantive RV findings within the supplied boundary.
Severity summary: 0 Critical, 0 High, 0 Medium, 0 Low.
No finding ID is fabricated for planned local finalization or excluded gates.

## Defects

* None identified in the bounded working diff and supplied task evidence.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| None | None | Parent continues planned P03 finalization | No implementation defect, unresolved material decision or material evidence gap identified. |

Later implementation of any separately identified work does not require this
Review to run again.

## Residual Work

* Existing human/operational and publication/hosted work remains with the distinct owners above, not a new defect or automatic scope expansion.
* No new residual implementation work identified.

## Blockers and Remaining Work

* Review blockers: None.
* Remaining active work: Parent reconciles P03-T01 and state/changes to this result, then completes P03-T02 and the local-commit portion of AC6 with authenticated privacy-safe attribution and required trailer.
* Neither local commit nor final committed-head validation is claimed. Parent must preserve original critique/Review outcomes, keep Refs #130 / PR #509 only, and perform no push, issue closure, Azure action or latest.json hand edit.

## Validation Evidence

All execution results below are reported by the canonical changes record, not
newly executed or independently reproduced by this reviewer. Its fenced command
block is the exact-command source; paths and counts are retained without
claiming a full-suite or publication receipt.

| Command or recorded check | Scope | Status | Summary |
| --- | --- | --- | --- |
| Six fully qualified JsonResidentDecisions/SqlResidentDecisions selectors listed in changes; unittest -v with explicit current-worktree PYTHONPATH | Three new regressions on JSON and SQLite | Failed on original; passed fixed | Original 6 failures, exit 1, 0.689s; fixed 6 tests OK, no skips, 0.893s. These are not added to the full-module count as separate unique tests. |
| /tmp/mv/bin/ruff check . from src/core | Complete core project | Passed, reported | All checks passed. |
| /tmp/mv/bin/ruff format --check . from src/core | Complete core project | Passed, reported | 110 files already formatted. |
| /tmp/mv/bin/mypy from src/core | Complete configured core type scope | Passed, reported | No issues in 163 source files. |
| PYTHONPATH=src:tests:../agents/src:../agents/tests /tmp/mv/bin/python -m unittest -q test_resident_decisions test_hazard_referral test_consultation_controls test_quality_procurement test_dependency_rule | Five selected core modules | Passed with skips, reported | 384 tests reported, OK, 90 skipped, 65.216s; not 384 executed passes. |
| PYTHONPATH=../api:../api/src:../api/tests:src:tests:../agents/src:../agents/tests /tmp/mv/bin/python -m unittest -q test_resident_api from src/core | Resident API module | Passed with skip, reported | 16 tests reported, OK, 1 skipped, 17.792s; not 16 executed passes. |
| /tmp/mv/bin/ruff check tests/test_resident_api.py; /tmp/mv/bin/ruff format --check tests/test_resident_api.py; /tmp/mv/bin/mypy tests/test_resident_api.py from src/api | Changed API test | Passed, reported | One formatted file; no type issues in one source file. |
| git diff --check | Implementation diff | Passed, reported | No whitespace errors reported in changes. |
| Opt-in MSSQL/Azure and backend-specific tests | Integration and backend applicability | Skipped, reported | Existing opt-in or non-applicable paths; new inherited MSSQL regressions are not SQL Server execution evidence. |
| New test execution, full publication gate, SQL Server, Azure, real model, browser, participant/human acceptance and hosted checks | Outside this Review/local fix validation boundary | Not run here | Explicitly excluded; no operational or publication conformance claim. |

The changes record also reports module-origin verification, no dependency
installation/shared-venv mutation and expected injected-recovery/law-store
warnings in passing tests. Unknown law readiness remains Unknown.

## Outcome

* Outcome: Conformant with justified divergence.
* Outcome rationale: The working implementation conforms to the revised plan and both requested regression fixes. UUID allocation is a justified, explicitly reconciled departure from the initial research/counter preference, not a departure from confirmed user requirements. P01/P02 are supported by the recorded validation; planned local commit remains the parent's next action, not completed evidence.
* Acceptance limit: This accepts the bounded working implementation evidence only. It does not accept all issue #130 criteria, retroactively approve the original critiqued design, assess a future committed head or approve publication/live use.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No rpi-implement correction identified. |
| Decision gap or invalid assumption | None | No rpi-plan handoff required. |
| Material evidence gap | None | No rpi-research handoff required for this bounded verdict. |
| Non-blocking excluded work | Distinct issue acceptance and future publication work | Issue owner/qualified approvers and publication owner, only under separate authorization. |

* Execution status: Complete.
* Outcome: Conformant with justified divergence.
* Validation coverage: Reported baseline/fixed JSON/SQLite regressions, complete configured core static checks, five selected core modules, resident API module and changed API static checks; skips and unrun boundaries retained.
* Blockers: None for the bounded Review.
* Parent continuation: Finalize owned evidence/state and commit locally as P03-T02. This is the single Review result; do not schedule another Review or describe it as final-head/publication approval.
