---
title: "Review: pr-605-capacity-sql-reopen-correction"
description: "Independent post-implementation assessment of the SQL reopen fixture correction."
ms.date: 2026-10-31
---

## Scope and Evidence

* Task ID: pr-605-capacity-sql-reopen-correction; PR #605; Refs #523.
* Review date: 2026-10-31.
* Review scope: the supplied complete correction task, one independent Review.
* Implementation HEAD: 183c4ca3df7e39d6f7c83b617ca680883bd049e7.
* Parent: e5f36c13dca8c9fcff34af6ab6c7a1d92b6b1da7.
* Branch: fix/capacity-page-523; opening worktree clean.
* Plan: .copilot-tracking/plans/2026-10-31/capacity-sql-reopen-correction-plan.md
* Phase details: .copilot-tracking/details/2026-10-31/capacity-sql-reopen-correction-phase-details.md
* Research: .copilot-tracking/research/2026-10-31/capacity-sql-reopen-correction-research.md
* Changes: .copilot-tracking/changes/2026-10-31/capacity-sql-reopen-correction-changes.md
* Critique: .copilot-tracking/reviews/plans/2026-10-31/capacity-sql-reopen-correction-plan-critique.md
* Source boundary: src/api/tests/test_procurement_api.py, src/api/tests/test_mssqlstore.py, src/api/README.md; surrounding implementation read only as needed.

## Opening Review State

* Interpreted review goal: compare the committed fixture correction and guide against the supplied accepted requirements, critique dispositions, validation evidence and remaining publication boundaries.
* Review scope: full supplied task, including P01-T01 and P01-T02 reconciliation.
* Evidence readiness: all five supplied artifacts exist; exact implementation HEAD and parent resolved; content comparison and validation provenance assessment pending.
* Acceptance basis: backend-preserving non-wiping reopen, detached audit invariants, missing-law refusal, root-cause evidence, authorized CI publication gate and preserved human approval.
* First comparison boundary: current plan/details/changes/critique/research against the three-file implementation diff and immediate fixture/application context.
* Active read-only boundaries: write only this canonical record; no source or other artifact mutation, commits, pushes, agents, or wiping SQL execution.
* Initial blockers: none identified at opening.

## Execution Status

* Execution status: Complete.
* Review execution evidence: exactly one independent post-implementation Review completed against the identified HEAD, its parent, all five task artifacts, the complete three-file source diff and immediate backend/application/CI context. No agents or test suites launched.
* Implementation execution is separate: source and requested validation are complete; intake P01-T02/P01 markers remain open for this Review and subsequent parent reconciliation. Publication and hosted/human acceptance are not complete.

## Assessed Byte Identity

The following SHA-256 hashes match both working-tree files and bytes read
directly from implementation HEAD 183c4ca3df7e39d6f7c83b617ca680883bd049e7.
That commit's first parent is e5f36c13dca8c9fcff34af6ab6c7a1d92b6b1da7.

| Assessed file | SHA-256 |
| --- | --- |
| src/api/tests/test_procurement_api.py | 797d94c08d67b3600906fde397c13f8bd63b04be6c0dfbcff242384a63021a1b |
| src/api/tests/test_mssqlstore.py | efbb6ebbbac2acfb985843f8a9b07d422907bba7271ab05ec841da57d25708cd |
| src/api/README.md | 0fe54567bfc71579622d4616b017dd428f78f1e7d9e9101ae851594a8db8f9b3 |

The parent must compare these exact source hashes before pushing any later
evidence-only commit. This record assesses the implementation HEAD above, not
an unobserved later commit, rebase, changed base, image or hosted run.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01; AC2-AC5 | Genuine non-destructive reopening and audit oracle | Reconciled | Complete three-file diff implements the two-helper budget, seed removal, actual backend identity, audit and procurement invariants, and fail-closed law/action responses. |
| P01-T02; AC6 | Validation Record and Pre-Review Reconciliation | Reconciled | API-wide tool checks and 40/13 zero-skip test results are recorded; this Review was expressly the remaining boundary. An open marker is accurate at intake, not unfinished source work. |
| AC1 | Research W1/C1-C6 and adverse baseline | Reconciled | Original hosted terminal failure independently retrieved; local SQL failure and two-backend baseline are preserved as parent evidence. |
| AC7; publication | Remaining Work and Return-to-Caller State | Reconciled, not fully delivered | Implementation commit exists; original critique is committed and unchanged. This Review is now written. Parent evidence commit/non-force push and future hosted/human gates remain subsequent actions, not proven acceptance. |
| Follow-Up Items | None | Reconciled | No implementation-discovered distinct follow-up is asserted or needed. |

The plan's historical "Ready task after critique: P01-T01" handoff is
subordinate to its current checked P01-T01 and explicit P01-T02 validation/
Review state. Details and changes identify the same remaining boundary;
that historical readiness label creates no material scope ambiguity.

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01; AC2/AC3 | src/api/tests/test_procurement_api.py; src/api/tests/test_mssqlstore.py | Common reopen_store delegates to existing SQLite/file initialization; SQL override calls factory directly without wipe. | Initial SQL make_store still wipes only for fixture setup; reopening supplies the original state marker and unavailable seed. SQL factory derives the same state directory and creates a fresh MssqlStore adapter. | Parent: 40 SQLite/file/law tests and 13 real SQL HTTP tests passed, zero skips. | Genuine reopen, not a relaxed path-only assertion or reseeding. |
| P01-T01; AC2-AC4; PC-001 | src/api/tests/test_procurement_api.py | Remove the actual synthetic seed; retain original exact type and SQL db_path; assert distinct db adapter; detach nonempty audit before reopening. | Original procurement captured after save; equality checked immediately after reopening, after each repeated read cycle and after refusal. Audit uses the same detached pre-reopen oracle at all three boundaries. Missing seed remains absent. | Same focused parent runs. | Persistence and audit continuity are directly tested; missing contract_version remains null and appointment status Unknown. |
| P01-T01; AC4/AC5 | src/api/tests/test_procurement_api.py | Retain appointment offer refusal and explicitly exercise unloaded application-law checks. | App.law is None; twice-repeated checks return HTTP 503, status unknown, missing-law error and human emergency safe_route. Offer returns HTTP 403/current-authority error without procurement/audit mutation. | Procurement/law and real SQL HTTP parent runs. | No legal, contractual, appointment or resident-consent authority invented. |
| P01-T01 | src/api/README.md | Explain seed-independent three-store regression and SQL initial setup versus reopening. | Five added guide lines match the actual fixture lifecycle and unchanged application-law semantics. | Direct Markdown/context/diff review. | Directly related documentation only; no UI/source runtime change. |

Immediate context confirms SqlStore seeds only when durable case data is
absent, Store prefers saved live.json, and MssqlStore opens a new _Conn and
uses state_dir/mssql as its local marker. Removing the seed makes the old
wiping reopen fail instead of recreating a misleading baseline. The distinct
db assertion establishes separate adapters; direct _open inspection supports
their independently constructed SQL connections. No claim of live-platform
authority or concurrency acceptance follows.

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| Functional requirements; P01-T01 | Explicit detached nonempty pre-reopen audit and refusal-boundary comparisons | PC-001; already requested unchanged audit | Plan, details, changes and committed assertions agree | Accepted direct refinement; original Revise preserved | Implemented without divergent scope or extra helpers. |
| Dependencies; P01-T02 | Retain existing interpreter instead of worker-proposed relocation | PC-002 rejection; caller explicitly confirms parent permission and component guide examples | Disposition documented in plan/details/changes | Rejected, not applicable to parent | Justified. This Review worker's own filesystem restrictions do not create a parent prohibition or invalidate supplied parent validation. No forbidden-location execution by this reviewer. |
| P01-T01/P01-T02/P01 | Mark source complete, validation complete, Review remaining | Recorded tool and focused-suite successes | Checklist, phase index, changes and handoff reflect the active boundary | Ready after one critique and recorded dispositions | Accurate intake state; parent owns final marker reconciliation after receiving this record. |
| Publication boundary | CI instead of complete local gate | Explicit user direction, repeated in the supplied task | Plan non-goals, details and changes consistently preserve the exception | No unaccepted decision gap | Authorized task-specific boundary, not a fabricated local receipt or changed branch protection. |

No material implementation divergence from the current accepted plan was
found. No discovery requires new planning, another critique, or a second
Review. The user-authorized CI publication strategy differs from the standing
local-gate default but is not an implementation divergence from this plan.

## Critique and Material Revision Assessment

* PC-001 accepted and implemented: the detached, nonempty audit baseline is taken before unlink/reopen; immediate, repeated-read and refusal comparisons use that original baseline.
* PC-002 rejected with explicit parent-context rationale. The existing interpreter is supported by the caller and src/api/README.md examples. Worker-only constraints are not promoted into parent policy. No environment relocation, production change or second critique is required.
* The original critique execution Complete, verdict Revise, and its two Medium findings remain historical evidence; this Review does not relabel them as a passing critique.
* Material revision readiness: recorded direct dispositions cover the refinements; no unresolved significant or divergent user decision remains.
* Dependent-work pause: the supplied plan/details/changes consistently record readiness after disposition before implementation. No evidence of an unaccepted-direction continuation was found; this is an artifact-based assessment, not a reconstructed execution transcript.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| None | Plan and changes both declare none | None | No distinct follow-up item or extra active scope created. |

## Findings

No substantive RV-xxx finding identified in the supplied boundary.
Severity summary: 0 Critical, 0 High, 0 Medium, 0 Low.
Pending publication and hosted/human approval are explicit workflow boundaries,
not implementation defects or invented follow-up work.

## Defects

* None identified.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| None | None | Active parent receives this single Review | No implementation, decision or material research gap identified. |

Later action does not require a second Review under this task's one-Review
instruction.

## Residual Work

* No residual source implementation or distinct plan follow-up identified.
* Authorized publication remains parent work, not delivered by this reviewer.

## Blockers and Remaining Work

* Review blockers: none.
* Remaining active work: parent records this Review's disposition and reconciles P01-T02/P01, commits the review/evidence without changing assessed source bytes, verifies the hashes and continues authorized non-force publication on fix/capacity-page-523.
* AC7 is not fully satisfied at this boundary: the implementation commit exists, but subsequent evidence commit/push is outside this Review.
* Hosted checks for the corrected candidate, any rubric outcome and human merge approval remain unclaimed. Do not close #523 or claim all issue acceptance criteria on the basis of this bounded correction; retain Refs #523.
* No SQL database/container/image operation, installation, source correction, remote mutation or agent launch performed here. Root retains exclusive resource-isolation ownership.

## Validation Evidence

Parent commands were recorded from src/api with
PYTHONPATH=.:src:tests:../core/src:../agents/src:../core/tests:../agents/tests
and its existing permitted interpreter. Parent results are accepted supplied
validation evidence, not independent reruns by this reviewer.

| Command or check | Scope | Status | Summary and provenance |
| --- | --- | --- | --- |
| python -m ruff check . | API-wide | Passed, parent evidence | All checks passed, exit 0. |
| python -m ruff format --check . | API-wide | Passed, parent evidence | 66 files already formatted, exit 0; existing SQL fixture format exemptions remain unchanged. |
| python -m mypy | API-wide | Passed, parent evidence | 125 source files, exit 0; existing untyped migrated/SQL exemptions remain, so this is not newly strict coverage of all SQL code. |
| python -m unittest test_procurement_api test_rule_alerts -q | SQLite/file procurement and law | Passed, parent evidence | 40 tests in 42.516s, zero skips, exit 0. |
| Isolated runtime SQL runner, test_mssqlstore.MssqlProcurementApi -q | Real SQL procurement HTTP | Passed, parent evidence | 13 tests in 33.305s, zero skips, exit 0. Only session-created ama_605_reopen_20261031_0845339f on protected ama-350-feedback-sql. Not rerun by Review. |
| Named SQL failure and SQLite/file baseline | Pre-correction AC1 | Failed as expected / Passed, research evidence | Original named SQL test failed at the hardcoded SQLite-path assertion; two corrected SQLite/file selectors passed. Invocation error for nonexistent FileProcurementApi preserved separately. |
| gh run view 41212776695 --repo jmservera/ama --log-failed | Original CI W1 | Completed, independently retrieved | Terminal named path-assertion failure verified: 269 tests in 314.277s; failures=1, skipped=1; exit 1. Earlier missing-law logs are not the terminal failure. |
| git diff --check | Current tracked diff | Passed, independently executed | Exit 0; source unchanged during Review. |
| git show HEAD:file and sha256sum | Exact three-file identity | Passed, independently executed | Committed and working-tree bytes match the recorded source hashes. |
| Complete local gate | Publication | Skipped | Explicit caller requests CI publication gate; no receipt produced or claimed. |
| Corrected hosted CI / human merge approval | Publication/acceptance | Unavailable at assessed boundary | Future parent publication and hosted/human decisions; original failed CI is not corrected-candidate success. |

Parent evidence reports protected container identity
793cb3650397532c73fd27a46e4e7c600c03a7198d76832942c733a30ca32ae8,
running protected 2022-latest with no removal/restart. Review did not inspect
credentials, execute the runtime runner or independently verify live resource
identity. This limitation is bounded by explicit root ownership and supplied
zero-skip SQL evidence; it is not permission to run a wiping suite.

## Outcome

* Outcome: Conformant.
* Outcome rationale: the exact committed source correction meets AC2-AC5 and the locked budget, source/guide match the supported root cause, critique dispositions are justified, and supplied AC1/AC6 evidence supports the bounded candidate. AC7 continuation and hosted/human acceptance remain expressly pending, not claimed complete.
* Acceptance limit: engineering conformance of this correction, not issue-wide closure, full local-gate completion, production legal satisfaction, live-platform validation, hosted success or merge approval.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | None identified. |
| Decision gap or invalid assumption | None | No unresolved critique or material divergence. |
| Material evidence gap | None | Bounded supplied validation accepted with provenance limitations above. |
| Non-blocking residual work | None | No distinct follow-up; parent retains ordinary publication continuation. |

* Execution status: Complete.
* Outcome: Conformant.
* Validation coverage: supplied API tool checks, 40 SQLite/file/law tests and 13 isolated real SQL HTTP tests; independent source/guide/CI-log/hash review.
* Blockers: none for this Review; future CI/human acceptance pending.
* Write boundary verification: only this canonical review record created; original task artifacts and source unchanged.

| Artifact | Description |
| --- | --- |
| .copilot-tracking/plans/2026-10-31/capacity-sql-reopen-correction-plan.md | Current requirements, dispositions and markers |
| .copilot-tracking/details/2026-10-31/capacity-sql-reopen-correction-phase-details.md | Current task details |
| .copilot-tracking/research/2026-10-31/capacity-sql-reopen-correction-research.md | C1-C6/W1 and original baseline |
| .copilot-tracking/changes/2026-10-31/capacity-sql-reopen-correction-changes.md | Implementation and parent validation evidence |
| .copilot-tracking/reviews/plans/2026-10-31/capacity-sql-reopen-correction-plan-critique.md | Preserved original Revise critique |
| .copilot-tracking/reviews/logs/2026-10-31/capacity-sql-reopen-correction-review.md | This single independent Review and source hashes |

## Next Steps

No user action required. Active parent owns marker reconciliation, evidence
commit and hash-verified authorized non-force publication. Preserve this
assessed HEAD and source hashes, CI publication boundary and future human
merge approval. No second Review is planned or requested.
