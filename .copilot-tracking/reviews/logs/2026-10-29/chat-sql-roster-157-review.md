---
title: "Independent Review: chat-sql-roster-157"
description: "One bounded post-implementation Review of authoritative SQL chat actors."
ms.date: 2026-10-29
---

## Opening Review State

* Interpreted review goal: independently assess the uncommitted SQL-roster authorization fix for task 157-chat-sql-roster, not the ancestry or whole acceptance of issue #157 or PR #503.
* Review scope: the working-tree delta from 6989bbb5d0f3e6a4c1319cd91220954c85b6cf9b in src/core/src/zava_forward/core/chat_isolation.py, src/core/tests/test_chat_panel.py and src/core/README.md, plus the supplied dated task artifacts.
* Evidence readiness: the six supplied research, plan, details, critique, changes and state artifacts exist; source changes are present; no prior canonical Review record exists. Substantive comparison and validation are pending.
* Acceptance basis: supplied owner requirements, current plan AC/FR and task markers, phase details, original critique dispositions, changes and validation evidence.
* First comparison boundary: reconcile current task artifacts before tracing shared actor lookup and the two existing dispatch/completion call sites against the regression tests.
* Active read-only boundaries: write only this canonical review record. No implementation, other artifact, Git, Azure, provider, network or rubric mutation; no delegation or repeated Review.
* Initial blockers: none identified during boundary discovery; local commit and publication gates are outside this Review and remain pending.

## Scope and Evidence

* Task ID: 157-chat-sql-roster; stable artifact slug: chat-sql-roster-157.
* Review date: 2026-10-29.
* Assessment count: exactly one independent post-implementation Review; no delegation.
* Branch: feat/agent-chat-157.
* Assessed baseline: HEAD 6989bbb5d0f3e6a4c1319cd91220954c85b6cf9b, including the supplied initial pull bot commit.
* Exact assessed source boundary: only the uncommitted delta in src/core/src/zava_forward/core/chat_isolation.py, src/core/tests/test_chat_panel.py and src/core/README.md. Diff totals: 129 added lines and three removed lines. No earlier PR #503 ancestry is assessed.
* Source-delta fingerprint: SHA-256 48ccded0a41bb6a6d8490b8dcd5eec6ac7ab4db48403ba8df2416b1ae76388bd, computed from `git diff --binary 6989bbb5d0f3e6a4c1319cd91220954c85b6cf9b --` followed by the three source paths in the order listed above. This identifies an uncommitted patch, not a committed-head or gate receipt.
* Acceptance boundary: the supplied stale roster-backed SQL authorization correction, FR1-FR3, non-functional requirements, AC1-AC4 and P01/P02 task evidence. Whole issue #157 acceptance, deployment, operational acceptance and publication are explicitly excluded.
* Related source was read only to trace actor identity, SQL/cache behavior, projection, thread ownership, completion audit and existing formatting/type policies. No independent audit of those unchanged components is claimed.
* Prior pull/rebase and remote PR lifecycle are supplied facts, not remotely revalidated by this Review. There were no Git mutations, network/provider commands, Azure operations or rubric edits by the reviewer. The executed regression suite includes its existing local HTTP fixtures, not external service validation.

| Artifact | Compared scope |
| --- | --- |
| .copilot-tracking/research/2026-10-29/chat-sql-roster-157-research.md | Research C1-C8, selected resolver repair, identity boundaries and limitations |
| .copilot-tracking/plans/2026-10-29/chat-sql-roster-157-plan.md | Owner requirements, FR/NFR/AC, P01/P02 markers, follow-up and handoff |
| .copilot-tracking/details/2026-10-29/chat-sql-roster-157-phase-details.md | Task-level contract, fixture design, validation and pending local delivery |
| .copilot-tracking/reviews/plans/2026-10-29/chat-sql-roster-157-plan-critique.md | Original one-time Complete/Pass critique and zero actionable findings |
| .copilot-tracking/changes/2026-10-29/chat-sql-roster-157-changes.md | Implementation, original failures, corrected passing results, decisions and limits |
| .copilot-tracking/rpi-sessions/2026-10-29/chat-sql-roster-157-state.json | Active Review, accepted decisions, no blockers and pending Review pointer |

## Execution Status

* Execution status: Complete.
* This means the bounded Review executed completely, not that every implementation-plan task or delivery gate is complete.
* Review evidence: artifact reconciliation, complete scoped source diff inspection, related call-path inspection, independently passing six-module regression suite, eight corrected in-memory contract probes and whitespace validation on 2026-10-29.
* Only this canonical Review record was deliberately created or edited. Test runtime used automatically cleaned fixture directories under src/core with TMPDIR set to the current project directory and bytecode generation disabled.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01, complete | Shared actor resolver reads SQL by normalized authenticated email | Reconciled | Direct parameterized lookup under dblock replaces cached roster authorization for SQL stores; existing panel call sites remain unchanged |
| P01-T02, complete | One SqlRosterTests fixture, four tests, amended history fixture and README | Reconciled | Separate SQLite writer, both cache assertions, revocation matrices, allowed-role withholding and stable cited-answer control match details and budget |
| P01, complete | Resolver and regression contract implemented | Reconciled | Both child tasks have source and passing validation evidence |
| P02-T01, complete | Red/green, six-module tests, actual API script and corrected checks | Reconciled | Original failures and corrections remain visible; no failed first attempt is represented as a pass |
| P02-T02, pending | One independent Review and subsequent local commit | Reconciled | This record supplies the Review portion only; local commit and parent-owned marker/state reconciliation remain pending |
| P02, pending | Validate and independently review | Reconciled | Phase remains correctly unchecked while the local-commit portion of P02-T02 is unfinished |
| Follow-Up Items | Later full local publication and exact-head/hosted gates | Reconciled | Distinct later work if publication is requested; not added to current implementation or acceptance |
| Handoff and state | No source work or implementation blocker; active Review | Reconciled | State review=null and next_action=Review are the intentional pre-Review handoff snapshot, not evidence that the source is unreviewable |

## Requirements and Acceptance Reconciliation

| Requirement | Evidence and substantive assessment | Result within assessed boundary |
| --- | --- | --- |
| FR1: SQL authority by authenticated normalized email | ChatIsolation.current_user derives key through chatthreads.user_key, which strips/lowercases the authenticated email. The SQL branch executes SELECT body FROM staff WHERE email=? with the bound key inside dblock on every invocation. It does not consult or refresh either staff cache. ChatPanel.ask invokes it before dispatch; ChatPanel._ask invokes it after the model returns or fails and before completion persistence. | Met |
| FR2: fail closed on missing/disabled/inactive/disallowed actor | Missing rows become None and raise ChatForbidden. Disabled, active=False, contractor and unknown roles are rejected. SQLite update/delete matrices exercise both authorization points with valid answer canaries. SQL read and malformed JSON exceptions propagate rather than admitting the cached actor; independent in-memory probes confirm this behavior. | Met |
| FR3: preserve identity, history, projection and audit boundaries | Verified Entra remains a separate first branch using identity.verified and projection.allowed, not roster email authority. Invalid Entra identities are rejected, not routed through roster fallback. Non-SQL cache/list resolution remains available, now subject to the explicitly required disabled/inactive checks. Panel control flow, role/source comparison and ownership checks are unchanged; SQL history restoration is persisted to SQL. | Met |
| NFR: bounded locks and existing SQL convention | Only the SQL execute/fetch is under dblock. No database lock surrounds inference; no catch converts read failure to authorization. No schema, dependency, global cache, identity redesign or panel-flow change. MssqlStore inherits the parameterized store interface; this is static compatibility evidence, not executed SQL Server proof. | Met |
| AC1: deletion/demotion before dispatch | Five independent-writer subcases update to contractor/unknown/disabled/inactive or delete the row. Each raises ChatForbidden with zero model calls and an empty message list while both caches retain their original snapshots. | Met |
| AC2: deletion/demotion during inference | Five subcases commit SQL changes inside the model callback after producing a valid canary. Each raises ChatForbidden, leaves only the user question, stores no assistant answer and records chat.turn outcome=access-rejected with model_calls=1. The test also checks total model calls across the matrix. | Met |
| AC3: permitted role change and stable actor | A SQL-only switch to Quality Inspector produces kind=withheld, WITHHELD text, no citations and no persisted answer canary. An unchanged SQL actor receives kind=answer, the canary, valid ZF-1/stage citation and one model call. Existing source reprojection and role-scoped history remain intact. | Met |
| AC4: validation and independent evidence | Original red 4 tests/11 failures, focused green 146 tests, actual API 38 tests with one existing Chromium skip, final panel 22 tests, Ruff/configured format and targeted mypy are recorded. Review independently reran the 146-test set and whitespace check, plus eight contract probes. Original critique and this single Review exist. | Met for bounded local evidence; no publication or human acceptance inferred |
| Owner scope and delivery constraints | Production changes are confined to shared current_user; supporting changes are tests and core README under src/. Dated RPI artifacts are the requested exception. No rubric edits appear in the delta. Commit is intentionally after Review and has not occurred in this assessment. | Source/evidence scope met; local delivery remains parent-owned |

## Completed Work Assessment

| Marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | src/core/src/zava_forward/core/chat_isolation.py | Replace stale SQL roster cache admission at the shared resolver; reject revoked actors | Seven added/two removed lines retain verified Entra first and isolate SQL/non-SQL branches | New SQLite matrix and independent contract probes pass | Conformant |
| P01-T02 | src/core/tests/test_chat_panel.py | Add one fixture/four tests; persist the existing history test's final SQL role restoration | Within the five-method budget; no tests removed or assertion contract weakened | Six-module suite includes all 22 panel tests and passes | Conformant |
| P01-T02 | src/core/README.md | Describe authoritative dispatch/completion reads, withholding and SQLite limitations | Seven added lines accurately distinguish revoked access from permitted-role changes | Source/document cross-check and whitespace pass | Conformant |
| P02-T01 | Dated changes/details | Preserve original red/failed attempts and corrected validation | Counts and skips are consistent across plan, details and changes | Independent 146-test result matches supplied evidence | Conformant |
| P02-T02 | This Review record | One independent assessment before local commit | Record completed without implementation/artifact mutation | Source boundary and HEAD rechecked | Review portion complete; no claim that commit occurred |

### Actor, Persistence and Audit Trace

The incoming user object supplies the authenticated identity key, not an accepted caller-selected role. For roster-backed SQL, role and flags come from the selected SQL JSON row. Missing rows cannot fall through to self.store.staff or self.store.data["staff"]. Existing thread ownership remains keyed to the actor's normalized identity.

The initial current_user call precedes receipt construction, question persistence and provider dispatch. A rejected dispatch therefore creates no turn message and is not required by this plan to create a new chat.turn receipt. After inference, current_user, chat_resume and case_context run before finish can store an assistant response. Revocation raises and the outer handler/finally records access-rejected. A still-authorized changed role/source clears the candidate answer and returns the existing withheld response. This distinction is accurately asserted and documented.

SqlRosterTests.change_roster commits through a separate sqlite3 connection, updates/deletes the actual staff row, then compares serialized snapshots of both cached collections. No cache assignment, cache invalidation or store restart supplies the test's authorization change. Callback mutation occurs after the valid cited canary is generated but before it is returned to the panel, so the test cannot pass merely because the model returned unusable text. The stable-actor control proves normal answer release remains possible.

## Implementation-Time Plan and Detail Update Assessment

| Area | What changed and why | Triggering evidence and user decision | Reconciliation | Planning/critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01 resolver boundary | Shared current_user rather than duplicate panel checks | Research C1-C4 established both required call sites already exist; selected before implementation | Research, plan, details, changes and patch agree | Original critique explicitly assesses this direction | No divergence |
| P01 history fixture | Persist final restored role in SQL | Research C6 identified the cache-only restoration | Present in plan/details before implementation and reflected in changes | Included in original critique | No assertion weakening or scope expansion |
| P02 API selector | Invoke actual API test script rather than colliding module-name discovery | Original API selector imported the core module first | Failed attempt and corrected 38-test script result retained | Command-selection correction only; no material plan revision | Justified execution detail |
| P02 test callback/type fixes | Bind loop variable and annotate mutation element types | Ruff B023 and targeted mypy failures | Both failures and corrections are in changes; final source reflects them | No changed requirement or acceptance basis | Justified execution detail |
| P02 formatting | Use --force-exclude on explicit files | Explicit-file format check bypassed existing migration exclusion | Current plan, details and changes name the configured format command; pyproject policy unchanged | No new formatting exemption introduced | Justified execution detail; production file is not claimed format-checked |

No material or divergent implementation decision requiring new owner authorization was identified. The descriptive updates reconcile current execution details without changing the confirmed intent, task markers, acceptance contract or source-change budget.

## Critique and Material Revision Assessment

* Latest critique: the supplied original one-time final-candidate critique records execution Complete, verdict Pass and zero findings at every severity.
* Dispositions: no PC-xxx action required implementation or owner decision; the plan records the Pass and points to the original artifact.
* Material revisions: none in the assessed implementation. Callback binding, typing, API selector and formatter invocation corrections are evidence-backed execution details, not a new architecture or authorization contract.
* Dependent-work pause: no evidence that a material unresolved decision or critique finding was bypassed; independent Review follows completed P02-T01 evidence.
* Original outcomes were preserved. No new critique, repeated Review or corrective implementation occurred during this assessment.

## Plan Follow-Up Assessment

| Follow-up | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Full local publication gate and independent exact-head/hosted acceptance | Owner permits only local commit and forbids push; current patch is uncommitted | Implementation parent/release owner, only if later publication is requested | Remains distinct later publication work; no gate receipt or approval inferred |

## Findings

No actionable RV-xxx findings within the exact assessed boundary.

Severity counts: Critical 0; High 0; Medium 0; Low 0. No implementation defect, material decision gap or material research-evidence gap requires routing.

## Defects

None found in the supplied fix and associated task evidence.

## Routed Findings

| Finding | Destination | Owner or next action | Reason |
| --- | --- | --- | --- |
| None | None | None | No substantive actionable finding identified |

## Residual Work

* The supplied publication follow-up remains outside active implementation: release owner must separately complete the full local gate, current-base receipt verification and independent exact-head/hosted assessment before any later authorized publication.
* SQLite and fake-model results do not prove SQL Server isolation/visibility, actual provider behavior, live employee-site/browser accessibility, operational approval or whole #157 acceptance. These existing limitations remain with their issue/release owners; this Review neither closes nor expands them.
* The completion read and eventual answer write are not one atomic transaction. Revocation after the completion lookup is not covered by a new atomicity guarantee. Research and critique explicitly preserve this limitation; it is not newly misrepresented as solved.
* Verified Entra principals intentionally retain their existing verified-identity contract, including its distinct roster-binding semantics. This is not a general Entra token/role revocation redesign.

## Blockers and Remaining Work

* Review blockers: none.
* Remaining active work: implementation parent must reconcile the completed Review pointer/markers and locally commit implementation plus dated original evidence under P02-T02. Required privacy-safe author/committer resolution and requested Conventional Commit/trailer remain parent's responsibility. This reviewer does not perform that commit or edit those artifacts.
* Publication remains blocked by unrun later gates and the explicit no-push instruction. Completion of this Review is not exact committed-head acceptance.

## Validation Evidence

| Command or evidence | Scope | Status | Summary |
| --- | --- | --- | --- |
| Supplied pre-fix SqlRosterTests execution | Old resolver/new regression | Failed as expected; implementation evidence | Four tests, 11 failures; ten revocation subcases and permitted-role-change canary exposed stale cache; stable actor passed. Not rerun or reconstructed by reviewer |
| Supplied focused six-module unittest execution | Core panel/threads/privacy/memory, API isolation, regulatory chat | Passed; implementation evidence | 146 tests |
| Supplied corrected explicit API test_chat_panel.py script | Actual API panel module | Passed with skip; implementation evidence | 38 tests, one existing opt-in Chromium skip; initial discovery-name collision retained as failure |
| Supplied final core test_chat_panel execution | Final panel tests | Passed; implementation evidence | 22 tests after callback/type corrections |
| Supplied Ruff check | Two changed Python files | Passed; implementation evidence | Original callback B023 failure and correction preserved |
| Supplied Ruff format --check --force-exclude | Configured changed-file formatting | Passed with existing exclusion; implementation evidence | Test file checked; migrated chat_isolation.py excluded by unchanged core configuration. Earlier explicit-file failure preserved, not reclassified |
| Supplied targeted mypy | Changed resolver and test paths | Passed; implementation evidence | Earlier two test inference errors corrected; inherited ignore_errors for migrated chat_isolation remains, so this is not full strict typing proof for production resolver |
| `cd src/core && PYTHONDONTWRITEBYTECODE=1 TMPDIR="$PWD" PYTHONPATH=src:tests:../agents/src:../agents/tests:../api/src:../api/tests python3 -m unittest test_chat_panel test_chatthreads test_chat_privacy test_chat_memory test_chat_isolation test_regulatory_chat -q` | Independent Review six-module rerun with Python 3.12.3 | Passed | 146 tests, 52.936 seconds, no skips. Existing isolation fixtures log missing-law-store rule warnings without test failures |
| Inline Python in-memory contract probes, first attempt | Reviewer fixture construction | Failed; harness setup only | Synthetic SimpleNamespace lacked chat_repo, so ChatPrivacy raised TypeError before any resolver assertion. Corrected the ephemeral harness, not source |
| Corrected inline probes with chat_repo attribute and SQLite :memory: | Normalized key/SQL role authority, deleted-row no-fallback, malformed JSON failure, SQL read failure, verified/invalid Entra, non-SQL cache/list paths | Passed | Eight contract assertions; no files, external network or provider calls |
| `git diff --check` | Assessed working-tree patch | Passed; independently executed | No whitespace errors |
| Fresh reviewer Ruff/mypy/API-script/browser/SQL Server/live-provider/full-gate executions | Beyond independently rerun checks | Not run | Prior lint/type/API results assessed from supplied evidence; no extra tool installation or external/live validation authorized or needed for the bounded verdict |

The review rerun did not mutate the source or substitute a new validation outcome for any original failed attempt. No SQL Server skip, browser skip, unrun full gate or absent operational evidence is counted as a pass.

## Outcome

* Outcome: Conformant.
* Rationale: the exact uncommitted change implements authoritative roster-backed SQL actor resolution at both existing required boundaries, fails closed without cached fallback, preserves the intended identity/control-flow contracts, and has substantive independent SQLite regression support. Plan, details, critique, changes and state are consistent with completed source work and a pending Review/local-commit task.
* Acceptance limit: this verdict applies to the bounded fix and evidence only. It is not approval of PR ancestry, all issue #157 criteria, a later committed head, deployment, human acceptance or publication.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None | No later rpi-implement correction needed from this Review |
| Decision gap or invalid assumption | None | No rpi-plan route needed |
| Material evidence gap | None | No rpi-research route needed for the bounded verdict |
| Non-blocking residual work | Distinct existing publication follow-up | Release owner, only if publication is later requested |
| Remaining accepted plan work | Parent continuation, P02-T02 | Reconcile Review evidence/state and commit locally; no push and no repeated Review |

* Execution status: Complete.
* Outcome: Conformant.
* Validation coverage: independent 146-test pass, eight corrected contract probes and whitespace pass; original broader focused validation assessed with failures/skips retained.
* Blockers: no Review or source blocker; local commit pending and publication gates unrun.

## Next Steps

Return this one Review result to the active implementation parent. The parent may complete P02-T02 evidence/state reconciliation and the requested local commit, retaining this original Review outcome. Do not push, claim publication approval, repeat Review or mark whole #157 accepted. No user action is required for this bounded Review.
