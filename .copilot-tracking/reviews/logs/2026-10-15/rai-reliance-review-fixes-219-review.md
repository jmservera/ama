---
title: RAI reliance review fixes 219 acceptance review
description: Bounded post-implementation correctness review of RV001-RV003 follow-up changes.
ms.date: 2026-10-15
ms.topic: reference
---

## Scope and Evidence

* Task: 219-review-fixes / rai-reliance-review-fixes-219.
* Branch: feat/src-rai-release-record-219; baseline HEAD 80143a9.
* Boundary: the seven changed src files relative to HEAD and the supplied canonical follow-up artifacts. No live release acceptance.
* Review authority: write only this record; no source, plan, changes, state, Git history or remote mutations; no nested agents.

## Opening Review State

* Interpreted goal: assess the original RV001-RV003 follow-up once for engineering correctness and acceptance.
* Evidence readiness: branch and dirty diff confirmed; supplied plan, details, critique, changes and original review are the comparison pointers, pending detailed inspection.
* Acceptance basis: exact nonempty selected reference even with inference disabled; current registered fast/strong reliance independent of historical model; same-version deny/cache/approve behavior; manual/template compatibility; offline-only harness adjustments.
* First comparison boundary: reconcile follow-up markers and critique dispositions against the seven-file HEAD diff and owning regressions.
* Active read-only boundaries: all evidence; only this canonical review record may be written.
* Initial blockers: none identified. Publication P02-T02 belongs to the parent; RV004 operational evidence remains outside engineering acceptance.

## Execution Status

* Execution status: Complete.
* Review execution evidence: exactly one bounded assessment on 2026-10-15 of the complete seven-file diff relative to HEAD 80143a9, canonical follow-up artifacts, original RV-001 through RV-004, and tightly coupled existing dispatch/review/cache/harness seams. No nested agents or corrective implementation.
* Implementation execution: P01/P01-T01 and P02-T01 are complete on the supplied evidence. P02/P02-T02 remain incomplete because this review and parent-owned publication share that marker. Completing this review does not claim commit, push, PR update or live acceptance.

## Compared Artifacts

* Plan: .copilot-tracking/plans/2026-10-15/rai-reliance-review-fixes-219-plan.md.
* Phase details: .copilot-tracking/details/2026-10-15/rai-reliance-review-fixes-219-phase-details.md.
* Final-candidate critique: .copilot-tracking/reviews/plans/2026-10-15/rai-reliance-review-fixes-219-plan-critique.md.
* Changes and recorded commands: .copilot-tracking/changes/2026-10-15/rai-reliance-review-fixes-219-changes.md.
* Original reproduced defects and residual gate: .copilot-tracking/reviews/logs/2026-10-15/src-rai-release-record-219-review.md, Findings RV-001 through RV-004.
* Changed files: src/core/src/zava_forward/core/store.py; src/core/src/zava_forward/core/sqlstore.py; src/core/src/zava_forward/core/ai_registry.py; src/api/tests/test_assistant_release.py; src/core/README.md; src/core/tests/release_support.py; src/agents/src/zava_forward/agents/ai_eval.py.
* Supporting read-only context: src/core/src/zava_forward/core/ai.py and src/core/src/zava_forward/core/ai_tasks.py; docs/case_study_48_original.md; relevant opening exercise/governance context in docs/case_study_48_addendum.md; docs/reference/README.md; docs/reference/memory.md. Memory supplies context, not evidence of approval.
* Research disposition: reused original defect reproductions and final-candidate critique; no new external research or live authority inference needed for these known engineering corrections.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01 / P01-T01 | P01: Reliance and Cache | Reconciled | Nonempty exact references, independent registered route selection, cache recovery and seven owning regression methods directly address the three reproduced defects. |
| P02 / P02-T01 | Commands and Results; P02: Validation and Publication | Reconciled | Required checks and final counts are recorded, including failed reproduction, initial full-suite harness failures and final successful runs. README matches the corrected behavior. |
| P02 / P02-T02 | Scope and Status; publication remaining | Reconciled, parent action pending | Review performed here; commit/push/update of existing PR 315 remains parent-owned. Unchecked publication acceptance is accurate, not a production defect. |
| Follow-Up Items | Remaining Evidence and Human Gates | Reconciled, open | RV-004 remains explicitly outside engineering completion and live acceptance. No unmet human/platform criterion is silently checked. |

The final handoffs, marker state, validation counts and remaining-work statements agree. No stale artifact prevents an engineering verdict.

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 / original RV-001 | src/core/src/zava_forward/core/store.py; src/api/tests/test_assistant_release.py | Reject invalid invocation references before any selection; require a nonempty selected reference and exact dictionary equality, without the old inference-configured shortcut | release_current checks registered task, dict type, nonblank string id/version/digest, then selects current binding. Production JSON release_context still returns None; SQL selection does not become optional when the endpoint is empty. | Missing/malformed references test; SQL/JSON inference-off ordinary/document and priority/cache regressions; bounded review assertions | Original None-equals-None defect resolved. Manual/template review and invalid-AI rejection remain allowed; AI accept/edit cannot use absent selection. |
| P01-T01 / original RV-002 | src/core/src/zava_forward/core/ai_registry.py; src/core/src/zava_forward/core/store.py; src/core/src/zava_forward/core/sqlstore.py; src/api/tests/test_assistant_release.py | Add one registered route helper for six retained tasks; use the current route independently of historical output model | briefing/message/summary use fast; priority/funding_draft/read_document use strong. A supplied historical alias differing from current denies before selection; omitted deployment still selects the registered current route. SQL default assessment uses the same helper. Exact original reference must still match the selected record. | Fast/strong ordinary/document review regressions; cached briefing zero-new-call regression; priority view/review regression; existing renewal coverage and bounded review assertions | Current routing cannot be masked by stored model. Renewal/replacement cannot authorize a different historical invocation reference. No production SQL statement or schema change. |
| P01-T01 / original RV-003 | src/core/src/zava_forward/core/store.py; src/api/tests/test_assistant_release.py | Do not reuse configured non-AI briefing fallback without a current exact release | Cached denial has no release and is retried; approval becomes visible without a case-version edit. Valid released fallback can still cache, including model-unavailable results with model=None because selection then uses current route. Workflow-only and unconfigured non-AI template shortcuts remain. | Full deny/repeat/record/request regression uses rel.record, checks unchanged store version, selected recorded ID, exactly one scripted call and subsequent same-object cache hit. | Original stale denied-cache recovery defect resolved without weakening authorization or ordinary workflow caching. |
| P02-T01 | src/core/README.md | Explain inference-off reference checks, registered-route reliance and approval-only cache recovery | Documentation agrees with actual guards and cache eligibility; explicit production JSON denial remains immediately below it. | Source/diff comparison | Accurate scoped documentation; no live-readiness claim. |
| P02-T01 | src/core/tests/release_support.py; src/agents/src/zava_forward/agents/ai_eval.py | Give existing explicit offline output-test harnesses labelled synthetic per-task references | Only test installation and isolated scripted evaluation Store instances override release_context/release_block. References bind to legacy task/configuration digest and the Ai release callback. _scripted still replaces _chat; no golden inputs changed. | Recorded corrected 66-test targeted run, full API/core reruns and agents suite/static checks | Compatible harness correction, not a production Store authorization option or a live-release bypass. |

Seven new tests are owned by the existing src/api/tests/test_assistant_release.py, within the eight-method ceiling. One route helper is added; no new production module, test file, dependency, schema or protected-path change appears in the diff.

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P02-T01 | Include existing core test support and agents scripted evaluation setup and agents validation | Initial full API run exposed old offline harnesses that bypassed dispatch admission but supplied no review/cache reference. Existing explicitly offline setup was corrected, not the production guard. No new product or human-authority decision needed. | Details describe the harness correction and unchanged golden data; changes record reports initial failures, reason, corrected tests and final checks; final plan handoff identifies it. | Final-candidate Pass assessed semantic regressions, one helper/test budget and no production bypass. Harness reconciliation is compatible with that direction; no material revision requiring new planning or critique. | Justified tightly coupled implementation adjustment; no unaccepted scope or autonomy expansion. |
| P01-T01 / P02-T01 | Preserve existing ai_tasks review callers and production dispatch instead of changing them | Shared release_current is already the ordinary/document/priority/cache seam; configured dispatch already supplies task deployment and invocation reference | Changes record explains why no production ai_tasks change is required; route metadata matches existing fast/strong dispatch. | Compatible with accepted shared-guard plan | No missing required production edit; acceptance is behavioral, not a file checklist. |

## Critique and Material Revision Assessment

* Latest critique: Complete / Pass, zero actionable PC findings. No unaddressed critique disposition exists.
* Semantic regression assessment: tests exercise actual SQL/JSON historical review actions, actual cached output and priority view/review, route changes, and actual release-record approval recovery. They are not merely helper-proxy assertions.
* Initial reproduction is recorded as 32 tests with 20 failing assertions/subtests before fixes; subsequent results distinguish corrected production behavior from separately corrected offline fixture assumptions.
* Material revisions: none requiring a new decision. The offline harness updates preserve the confirmed fail-closed production boundary and are reflected in final details/changes/handoff.
* Dependent-work pause: no unresolved material decision is evidenced. Execution chronology is reported by the canonical changes record, not independently reconstructed from absent raw logs.
* Publication readiness is an engineering handoff only; this review does not perform or certify parent-owned GitHub actions.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Original RV-004: named OQ-017 holders, delegations and competent human oversight | Local synthetic correctness tests cannot appoint accountable humans or demonstrate their oversight | Governance/sponsor and appropriate Safety, DPO/Legal and Assurance functions record named release/risk/suspension/restart authority and oversight evidence | Open distinct governance follow-up; retain unmet criteria unticked. |
| Original RV-004: approved actual evaluation, authoritative serving proof and direct acceptance | Scripted output and a synthetic record labelled actual exercise code semantics, not a real evaluation or approval | Authorized evaluation/task/control owners obtain and approve actual evidence and human acceptance | Open distinct evaluation/acceptance follow-up. |
| Original RV-004: permitted Docker, SQL Server and Azure evidence | Local Python/SQLite/static checks do not establish image, SQL Server concurrency or Azure deployment success | Platform owner obtains permitted runner, SQL Server validation and authorized Azure exercise | Open distinct platform follow-up; no prohibited access workaround. |

These remain excluded follow-ups, not new active P01/P02 implementation work.

## Findings

No new substantive engineering defect, decision gap or material engineering evidence gap was found in the complete supplied boundary. The actionable new defect set is empty: 0 Critical, 0 High, 0 Medium, 0 Low.

* Original RV-001 [High, resolved within engineering boundary]: typed nonempty reference plus current exact selection removes inference-off missing-reference acceptance. The owning regressions cover SQL/JSON ordinary/document acceptance/edit, priority view/review and cached AI; manual/template and reject paths remain.
* Original RV-002 [High, resolved within engineering boundary]: current registered fast/strong route is derived separately from historical model; changed historical aliases deny and exact reference equality remains mandatory after selection.
* Original RV-003 [Medium, resolved within engineering boundary]: configured no-release cache entries cannot indefinitely hide matching approval; the real record-function regression proves recovery at unchanged case version with one scripted call.

<!-- rpi:review id=RV-004 -->
### RV-004 [Medium, residual, retained]: Operational human, evaluation and platform gates remain open

* Related scope: plan Follow-Up Items and unchecked acceptance criteria; original RV-004 is retained, not newly discovered or reclassified as an implementation defect.
* Evidence: follow-up plan Acceptance Criteria/Follow-Up Items and changes Remaining Evidence and Human Gates explicitly leave named holders, competent oversight, actual approved evaluations/serving evidence, direct acceptance and permitted Docker/SQL Server/Azure validation unavailable.
* Impact: this engineering verdict cannot establish live readiness, genuine approval, regulatory satisfaction or production reliance authority.
* Destination: distinct RV-004 governance, evaluation/acceptance and platform follow-ups, owned as listed in Plan Follow-Up Assessment.
* Smallest useful next action: parent preserves open criteria and hands the respective evidence requests to those owners before making any affected live acceptance claim.

## Defects

* None newly found. Original RV-001 through RV-003 are resolved for this bounded engineering review.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| Retained RV-004 | Distinct governance, evaluation/acceptance and platform follow-ups | Respective owners obtain the actual authority, oversight, evaluation/serving, human acceptance and permitted platform evidence described above | Known operational residual work outside this engineering task; not a new rpi-implement, rpi-plan or rpi-research requirement. |

Each actionable residual is routed once above. No correction or repeat Review is requested.

## Residual Work

* RV-004 remains open with its separate owner actions; no live release acceptance.
* Parent-owned P02-T02 publication remains pending on the existing branch/PR. This is delivery continuation, not a code defect or additional review finding.

## Blockers and Remaining Work

* Engineering review blockers: none.
* Remaining active delivery: parent records this Review, commits/pushes the scoped work and updates existing PR 315 under the already accepted safeguards. This reviewer made no remote request or mutation.
* The unchecked publication criterion and RV-004 criterion must not be collapsed into a claim that all issue acceptance is complete.

## Validation Evidence

Reported implementation commands below come from the canonical changes record, not independent reruns or independently examined raw command logs.

| Command or evidence | Scope | Status | Summary |
| --- | --- | --- | --- |
| API unittest discovery for test_assistant_release.py before fixes | Original failure scenarios | Failed as expected, reported | 32 tests, 20 failing subtests/assertions, no errors. |
| Same targeted discovery after production fixes | Owning release tests | Passed, reported | 32 tests. |
| First full API discovery | Offline fixture compatibility | Failed, reported | 490 run, 98 skipped, 3 failures and 3 errors; explicit offline harnesses lacked release references. Reason and corrections are reconciled, not hidden. |
| API unittest test_ai_tasks test_assistant_release dataset.ImproveTests.test_briefing_cached_until_data_changes with PYTHONPATH=tests:../core/tests:../agents/tests | Owning regressions and prior failing offline cases | Passed, reported | Final targeted 66 tests after harness corrections. |
| Final core unittest discovery | Core component | Passed, reported | 312 tests. Earlier sensor-backfill ResourceWarnings are recorded, not failures. |
| Final API unittest discovery with PYTHONPATH=../core/tests:../agents/tests | API component | Passed with skips, reported | 490 tests run, 98 skipped, not 490 passing assertions/tests; conditional SQL Server coverage remains unavailable. |
| Agents unittest discovery | Scripted evaluation component | Passed, reported | 70 tests. |
| /tmp/zf164/bin/ruff check ., ruff format --check ., mypy in core/API/agents | All three affected components | Passed, reported | 73 core, 35 API and 16 agents files type-checked; no policy exclusion added. |
| git diff --check | Complete current tracked patch | Passed, independently run | No whitespace errors; seven changed src files only. Golden-input diff is empty. |
| PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src/core/src /tmp/zf164/bin/python -B, in-memory review probe | Six changed Python files and shared release guard | Passed, independently run | AST parsing plus 67 assertions across all six registered routes: malformed/blank references deny; exact selected reference accepts even with endpoint empty in this isolated selection stub; historical alias, missing selection, replacement reference and unregistered task deny. No disk fixtures, provider calls or SQL writes. This supplements, not substitutes for, owning SQL/JSON regressions. |
| Full-suite reruns during this review | Previously recorded successful suites | Skipped | Unnecessary duplication; authoritative implementation evidence is sufficient for this bounded review. No test fixture/scratch files created by the reviewer. |
| Live provider, human oversight/acceptance, Docker, SQL Server and Azure | Operational gates | Unavailable in supplied successful validation | Deliberately outside this review; no success inferred from synthetic records, local runs or skipped tests. |

## Outcome

* Outcome: Conformant.
* Boundary: engineering corrections for original RV-001 through RV-003 only, not complete issue or live-release acceptance.
* Rationale: source and semantic regression evidence establish exact selected-reference reliance independent of inference configuration and historical routing, and approval-only cache recovery. Manual/template acceptance, edit and reject behavior remains. Explicit offline harness adjustments are correctly isolated and reconciled. No substantive new defect or unaccepted decision was found.
* Known residual outcome: RV-004 operational gates remain unmet; parent-owned publication P02-T02 remains pending. Neither is misrepresented as completed by this verdict.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No later rpi-implement correction requested. |
| Decision gap or invalid assumption | None | No rpi-plan revision requested. |
| Material engineering evidence gap | None | No rpi-research request needed for the three resolved defects. |
| Non-blocking operational residual | Retained RV-004 distinct follow-ups | Governance, evaluation/acceptance and platform owners obtain the missing actual evidence. |
| Delivery continuation, not a finding | Active parent, P02-T02 | Record Complete / Conformant engineering review and perform already authorized same-PR publication while preserving open criteria. |

* Execution status: Complete.
* Outcome: Conformant within the bounded engineering scope.
* Validation coverage: recorded targeted/full/static checks plus independently run diff hygiene, syntax parsing and bounded in-memory guard assertions.
* Blockers: none for engineering review; operational residual gates stay open.
* Write boundary: only this review record was added; existing dirty source/artifact work preserved without editing, staging, committing or publishing.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-15/rai-reliance-review-fixes-219-plan.md](.copilot-tracking/plans/2026-10-15/rai-reliance-review-fixes-219-plan.md) | Current follow-up scope and open acceptance markers |
| [.copilot-tracking/details/2026-10-15/rai-reliance-review-fixes-219-phase-details.md](.copilot-tracking/details/2026-10-15/rai-reliance-review-fixes-219-phase-details.md) | Execution boundary and reconciled harness adjustment |
| [.copilot-tracking/reviews/plans/2026-10-15/rai-reliance-review-fixes-219-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-15/rai-reliance-review-fixes-219-plan-critique.md) | Complete / Pass final-candidate critique |
| [.copilot-tracking/changes/2026-10-15/rai-reliance-review-fixes-219-changes.md](.copilot-tracking/changes/2026-10-15/rai-reliance-review-fixes-219-changes.md) | Reported reproduction, corrections, validation and remaining gates |
| [.copilot-tracking/reviews/logs/2026-10-15/src-rai-release-record-219-review.md](.copilot-tracking/reviews/logs/2026-10-15/src-rai-release-record-219-review.md) | Original RV-001 through RV-004 |
| [.copilot-tracking/reviews/logs/2026-10-15/rai-reliance-review-fixes-219-review.md](.copilot-tracking/reviews/logs/2026-10-15/rai-reliance-review-fixes-219-review.md) | This single bounded review result |

## Next Steps

Return this Complete / Conformant engineering result to the active parent for P02-T02 publication on existing PR 315. Keep RV-004 and unmet human/platform/live acceptance criteria unticked and routed to their respective owners. Do not repeat Review or infer live release approval. No new user decision is required for this review.
