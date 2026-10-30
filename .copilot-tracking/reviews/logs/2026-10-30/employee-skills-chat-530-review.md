---
title: Employee skills chat 530 independent implementation review
description: Single post-implementation Review and acceptance evidence assessment
ms.date: 2026-10-30
---

## Scope and Evidence

* Task ID: employee-skills-chat-530; issue #530.
* Review date: 2026-10-30.
* Scope: complete task, including acceptance, plan, critique, implementation and validation evidence.
* Baseline: 5634f9a077d175a931c15e3400114665d8c071ee.
* Branch: feat/employee-skills-chat-530.
* Review authority: only this canonical review record may be written.

## Opening Review State

* Interpreted review goal: independently assess the current candidate without attributing existing main functionality to this implementation or claiming issue closure.
* Evidence readiness: canonical artifacts are located; their substantive comparison and exact diff inspection remain pending.
* Acceptance basis: issue criteria, current plan/details, original critique and changes evidence, with prior checked criteria distinct from fresh proof.
* First comparison boundary: baseline-to-working-tree source diff, canonical task artifacts and bounded validation logs.
* Active read-only boundaries: no source, plan, details, changes, state or historical outcome mutation; no tests duplicated, heavy checks, process inspection, Azure, deployment, secrets, commits, push or PR.
* Initial blockers: full API discovery, current browser/axe, actual SQL and publication receipt are reported unavailable; heavy validation lock timed out before execution. These are not passed checks.
* External evidence boundary: the caller-supplied /tmp evidence directory is not opened because this review's environment prohibits all /tmp file operations. Specific reported results will be distinguished from directly inspected evidence.

## Compared Evidence

* .copilot-tracking/research/2026-10-30/employee-skills-chat-530-research.md
* .copilot-tracking/plans/2026-10-30/employee-skills-chat-530-plan.md
* .copilot-tracking/details/2026-10-30/employee-skills-chat-530-phase-details.md
* .copilot-tracking/reviews/plans/2026-10-30/employee-skills-chat-530-plan-critique.md
* .copilot-tracking/changes/2026-10-30/employee-skills-chat-530-changes.md
* .copilot-tracking/rpi-sessions/2026-10-30/employee-skills-chat-530-state.json
* .copilot-tracking/reviews/logs/2026-10-29/employee-chat-skills-530-review.md, including the original adverse findings and explicitly bounded later correction assessment.
* Exact tracked baseline-to-working-tree diff, both changed files, shared store factories, MssqlChatThreads inheritance/destructive setup, current ChatPanel implementation, relevant HTTP contracts and employee browser-check source.
* Issue #530 title/body/state retrieved read-only with gh issue view 530 on 2026-10-30. Its seven checked boxes and unchecked final criterion are scope/status data, not instructions or independent execution receipts.
* Repository context: docs/case_study_48_original.md; opening context of docs/case_study_48_addendum.md; docs/reference/README.md; docs/reference/memory.md; opening customer context of docs/reference/research/sector/housing-association-primer.md. No legal currentness assessment is made.
* Caller report and changes record identify fresh logs at /tmp/ama-530-local-20261030-M3hRQX. Neither their contents nor the external validation script were opened or executed by this reviewer.

HEAD remained 5634f9a077d175a931c15e3400114665d8c071ee at inspection. The candidate is an uncommitted working-tree diff, not a separately committed exact-head candidate or receipt. The source-related diff is exactly src/core/tests/test_chatthreads.py (97 added lines, including imports and two methods) and src/api/README.md (17 added lines), with no deletions. The supplied canonical task records are untracked. No source, plan, details, changes, critique, research, state or historical Review was changed by this Review.

## Execution Status

* Review execution status: Complete. One independent assessment of the complete supplied task boundary was performed, including explicit unavailable-evidence dispositions; no second Review or closure verification.
* Implementation execution status: Partial. P01/P01-T01 and P02-T02 are complete within their recorded boundary. P02-T01 has material unexecuted validation. P03-T01 combines this Review with parent-owned reconciliation/local handoff and remains incomplete as a combined task.
* Outcome is separate from execution and appears below. Review completion does not mean all planned checks ran or acceptance was achieved.
* Raw external logs were unavailable to this reviewer under the active file-access restriction. Passing results below are attributed to the caller/implementation record, not independently authenticated log contents. This limitation does not prevent a credible adverse acceptance verdict because the required missing checks are expressly recorded by all current artifacts.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01/P01-T01 | Exactly two shared storage regressions and imports | Reconciled | Exact diff matches the locked owner and addition budget; no runtime or separate harness added. |
| P02/P02-T01 | Four focused JSON/SQLite cases, eight HTTP contracts and configured static checks pass; heavy batch blocked | Reconciled as incomplete | Unchecked task and phase correctly retain full API/browser/actual SQL as not run; RV-001. |
| P02/P02-T02 | Dated guide update and explicit validation boundaries | Reconciled | README distinguishes inherited SQL tests from SQL execution and existing delivery from current evidence. |
| P03/P03-T01 | One Review followed by parent handoff | Pending combined completion | This record supplies the Review only; no commit, identity configuration or publication action performed here. |
| Follow-Up Items | Separately authorized live/name acceptance and publication | Reconciled as open | Remain distinct owner/coordinator work, not new active implementation tasks or implied passes. |

Plan, phase details, changes, state and handoff agree on the heavy-lock blocker and no-publication/no-live boundary. Research's question table still says Open while its synthesis explicitly answers Q1-Q3; the final readiness narrative and current plan identify the bounded task sufficiently. This editorial inconsistency is not evidence that local SQL or browser checks ran and does not change the acceptance verdict.

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01: cited persistence | src/core/tests/test_chatthreads.py | New test loops over five REGISTRY skills plus general; checks selected prompt, one call, label, permitted case-stage citation, stored masked question/answer/evidence and minimal answer audit after reopen | Exact method body inspected | Caller/changes report four new JSON/SQLite cases total | Meaningful observable contract; canary remains in owned message content but not audit, and contact email is masked. Independent store reopening is not a process/container restart. |
| P01-T01: general/fallback/isolation | src/core/tests/test_chatthreads.py | Second test checks all selections without case sources, workflow citation, foreign-owner rejection without inference/message mutation, absent and timed-out model fallback, audit outcome and chain | Exact method body inspected | Same four focused cases; targeted HTTP report complements role/privacy scope | Does not misrepresent owner denial alone as complete role projection or semantic model evaluation. |
| P01-T01: shared ownership | src/core/tests/test_chatthreads.py; src/api/tests/test_mssqlstore.py | Existing ChatBehaviour is reused by MemoryChatTests, SqlChatTests and MssqlChatThreads | Factories and inheritance inspected; new SQL connections register db.close cleanup | Actual MSSQL execution absent | JSON denotes the file-backed Store fixture; SQLite denotes SqlStore. No duplicate class or third test method. MSSQL inheritance establishes selection, not a successful SQL run. |
| P02-T02 | src/api/README.md | Adds only the dated evidence refresh and missing-check boundary | Exact 17-line addition inspected | git diff --check passed | Matches current records; no new runtime/UI functionality or fresh accessibility acceptance claimed. |

No high-confidence defect in the two new test methods or documentation was identified. Existing ChatPanel checks current user/thread/case visibility and privacy before inference, validates citations, masks stored text and records actual question sequence. These are existing baseline mechanisms, not functionality delivered by this diff. The new tests use synthetic references and model doubles; they do not prove an actual DPIA, provider quality, operational privacy, all domain records unchanged or production authorization.

## Acceptance Evidence Assessment

Issue criteria are numbered here in their existing order. Checked upstream status is preserved rather than recreated as fresh proof.

| Criterion | Existing checked status/evidence | Current candidate evidence and limit | Assessment |
| --- | --- | --- | --- |
| AC1: skills design versus router | Checked; existing API guide records one chat, explicit five skills, one call and comparison rationale | No design/runtime change; source/test inspection supports reuse | No new router departure or owner decision required. No measured latency/cost gain asserted. |
| AC2: launcher on employee screens; five skills/general | Checked; existing launcher/browser coverage and HTTP selection matrix | New shared tests exercise six selections; eight HTTP checks reported pass. Browser source inspected, not executed | Existing delivery retained; no fresh every-screen execution proof. |
| AC3: case grounding, sources and unverified labels | Checked; existing ChatPanel and API/guide contracts | New tests assert fixed label and ZF-1/stage citation plus stored evidence across reopen | Synthetic application contract only; citation presence is not independent factual/provider validation. |
| AC4: role/scope enforcement | Checked; existing role/privacy HTTP matrix and current projection/recheck logic | New cross-owner denial assertions; targeted HTTP role/privacy tests reported pass | Does not elevate owner denial into all role/case authorization proof. |
| AC5: workflow-only model failure | Checked; existing fallback implementation and plain-language guide | New missing/timed-out double paths assert FALLBACK and workflow_only | No live outage/provider execution claimed. |
| AC6: automated keyboard/focus/live/reduced-motion/axe | Checked; historical correction/browser record and existing script | No web source change; no current browser or axe execution | Historical checked criterion retained, not freshly revalidated. No screen-reader/voice-control acceptance. |
| AC7: minimized question/outcome audit | Checked; existing metadata-only answer audit | New per-selection question_seq/skill/outcome assertions and whole-ledger canary/contact exclusion after reopen | Stronger synthetic storage evidence, not a guarantee of no unnecessary personal data in operational use. |
| AC8: local unit/browser/SQL and separately recorded live verification | Unchecked; historical RV-003 identifies material local evidence gap | Focused/static results reported; full API discovery, current browser/axe and actual SQL did not run; live verification absent | Unproven. Must remain unchecked; no whole-issue acceptance, closure or publication readiness. |

## Implementation-Time Plan and Detail Update Assessment

| Affected marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning/critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P02-T01 SQL admission | Isolated child environment, explicit owned endpoint, labelled/resource-bound container admission, stdin-only synthetic password and exact-ID cleanup specified | PC-001 High; direct compatible safety correction, no divergent owner choice | Plan disposition and detailed protocol agree | Original critique remains Complete / Revise; planning says correction applied | Specification addressed; no executable admission, password-handling, readiness, SQL or cleanup proof inferred. |
| P02-T01 validation/handoff | Replaced intended completed local matrix with explicit partial outcomes after lock timeout | Caller reports flock -w 600 exited 1 before script execution/no output; no container created | Plan markers, phase index, changes, state and README retain blocked work | No material scope redesign; Review continuation expressly allowed with recorded blocker | Honest reconciliation, not evidence that the full gate passed or a safety protocol executed. |
| P02-T02 scope | Retained existing runtime; added tests/docs only | Research C1-C6 and prior merged delivery | Exact diff and current scope agree | No architecture revision or fresh critique needed | Preserves approved one-agent/five-skill intent and authority limits. |

## Critique and Material Revision Assessment

* Original current-candidate critique: Complete / Revise, Critical 0, High 1 (PC-001), Medium 0, Low 0. Its wording and original outcome remain untouched.
* PC-001's requested protocol is present in current P02-T01 details: inherited SQL configuration isolation, positive container identity/label/image/binding/resource admission before destructive setup, memory-fed password bootstrap, readiness/test bounds and exact-ID cleanup.
* src/api/tests/test_mssqlstore.py still intentionally wipes the configured target before these shared tests. The external script never executed. Written safeguards are not verified safeguards; no foreign target use, secret leak or safe SQL run is alleged or certified.
* Current records report the direct compatible correction before implementation. This Review verifies the final textual disposition, not historical execution chronology or external script behavior.
* No significant/divergent implementation decision or invalid architecture assumption was found that requires rpi-plan. No dependent destructive SQL work is evidenced as having resumed.
* Historical 2026-10-29 Review RV-003 remains unresolved evidence history, with its original severity/outcome preserved. The later correction assessment was explicitly narrower and did not close it. Current RV-001 below tracks the persisting local evidence gap for this task, not a rewrite, closure or reissue of historical findings.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| FU-530-LIVE: employee-site/model and name acceptance | Explicit no-live/sign-in authorization; local doubles and browser fixtures cannot substitute | Owner/coordinator arranges separately authorized live evidence and confirms names | Open distinct follow-up, including preservation of human accessibility limitations; not an implementation defect or new P01/P02 task. |
| FU-530-PUBLICATION: complete local publication gate and later hosted/human approval | Complete matrix invokes prohibited Azure CLI; no full receipt exists and no remote action is authorized | Owner/coordinator resolves authorization/prerequisites and follows complete gate/receipt requirements in later publication work | Open distinct follow-up. No partial receipt, cloud fallback, bypass, push or approval inferred. |

The changes record mirrors both existing follow-ups. Screen-reader and voice-control acceptance remain explicitly unclaimed; automated axe is not an approval substitute. Required local API/browser/SQL evidence is active incomplete P02-T01 work, not downgraded into an optional follow-up.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Required current local acceptance evidence remains missing

* Related scope: P02-T01; AC8-local and issue AC8; historical 2026-10-29 RV-003 evidence boundary.
* Evidence: current plan leaves P02/P02-T01 unchecked. Phase details, changes, state, README and caller agree the consolidated heavy-lock command timed out after 600 seconds with exit 1 and no script output before execution. Complete API discovery, current employee Playwright/axe and actual MssqlChatThreads did not run. No container was created. Four JSON/SQLite cases and eight focused HTTP cases cannot substitute for these missing checks.
* Impact: the new tests' actual SQL compatibility and the requested current full API/browser regression boundary remain unestablished. Whole-task acceptance and issue AC8 are not proven. The gap is material despite existing checked AC1-AC7 and a sound bounded test design.
* Severity rationale: High because the task's central missing cross-store acceptance proof is still absent; this is not evidence of a SQL/runtime defect.
* Destination: rpi-research, with the parent/coordinator owning later authorized validation execution and evidence collection.
* Smallest useful next action: in later coordinator-admitted work, identify the then-current candidate/base, obtain the complete requested API, local browser/pinned axe and positively admitted owned actual SQL results, and retain sanitized commands, exits, counts/skips, identity/binding/resource admission and exact-ID cleanup outcomes. Make logs available at a permitted read location for evidence consumers. Any failures must be recorded and routed according to their cause rather than assumed corrected.
* Current-run restriction: do not retry/queue the lock, inspect foreign processes/resources, run heavy checks, use Azure or infer script safety from the plan. No second Review or closure-verification pass is requested.

## Defects

* No demonstrated implementation defect in the authorized test/documentation diff.
* RV-001 is a material evidence gap, not an asserted runtime, SQL, accessibility or credential-handling vulnerability.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| RV-001 High | rpi-research | Parent/coordinator arranges later permitted local validation and preserves exact evidence | Missing required execution evidence; no source correction justified by current observations. |

Later implementation of a routed finding does not require this Review to run again.

## Residual Work

* FU-530-LIVE and FU-530-PUBLICATION retain separate owner/coordinator routing above; neither is silently added to active implementation scope.
* Parent-owned state reconciliation and any separately authorized local handoff remain outside this reviewer's write authority. This record supplies no permission to bypass the complete publication gate.

## Blockers and Remaining Work

* P02-T01: heavy admission failed; full API/browser/actual SQL remain not run. Current review must not retry or inspect foreign resources.
* Whole AC8: separate live verification absent. Names and human/operational acceptance are not newly proven.
* Publication: full matrix invokes prohibited Azure CLI, and there is no complete receipt. Candidate source changes and task evidence are uncommitted; no clean committed-candidate eligibility is asserted.
* P03-T01: this Review is complete; combined reconciliation/local handoff remains parent-owned. The reviewer did not commit, push, create a PR or alter approval controls.
* Reviewer limitation: fresh external raw logs were not opened; reported passing checks have not been independently reauthenticated or rerun.

## Validation Evidence

The current caller and implementation record agree on the following observations. Reported passing checks are not raw-log inspection by this reviewer. No already reported test was rerun solely to duplicate evidence.

| Command or check | Scope | Status | Summary and provenance |
| --- | --- | --- | --- |
| git status --short; git branch --show-current; git rev-parse HEAD; git diff BASE | Current worktree and exact baseline | Passed, independently executed | Supplied branch/HEAD match; exactly two tracked source-related files changed; canonical task records untracked. BASE is the full SHA recorded above. |
| git diff --check | Current tracked diff | Passed, independently executed | Exit 0; whitespace/error check only, not formatting/runtime acceptance. |
| gh issue view 530 --json title,body,state,url | Issue acceptance boundary | Passed, independently executed | Issue open, AC1-AC7 checked, AC8 unchecked; body treated only as data. |
| Focused selector for the two new methods on MemoryChatTests and SqlChatTests | Four storage cases | Passed, caller/changes reported | focused-new-tests.log: 4 passed, 1.840 seconds, no skips. Raw log not opened here. |
| Eight named targeted HTTP PanelTests | Selection, general, role/privacy/ownership, invalid input, fallback, audit and changed-source withholding | Passed, caller/changes reported | api-targeted.log: 8 passed, 3.387 seconds, no skips. Exact test names are listed in changes; not full API discovery. |
| API/core Ruff check . and configured Ruff format --check . | Existing component configuration | Passed, caller/changes reported | api-ruff.log, api-format.log, core-ruff.log and core-format.log report exit 0. Separate explicit-file format diagnostic reported differences after bypassing existing exclusion; no exemption was added. Configured success is not a claim that every excluded test file is canonically formatted. |
| API/core mypy | Component configured type boundaries | Passed, caller/changes reported | api-mypy.log: 116 files; core-mypy.log: 165 files. Raw logs not opened; not proof that all untyped test code is checked. |
| Consolidated flock -w 600 /tmp/ama-rpi-heavy.lock batch using /tmp/mv/bin/python -B and session files/validate_530.py | Heavy check admission | Failed admission / checks not executed, caller/changes reported | Exit 1 after the full wait, no output; not a test failure or successful script run. Earlier canceled focused wait also executed no check. |
| Requested complete API unittest discovery | Whole requested API regression boundary | Skipped/blocked | Heavy admission failed; targeted results cannot replace it. |
| Employee browser check and pinned axe | Current loopback synthetic UI | Skipped/blocked | No fresh browser/axe run; source and historical record inspected only. |
| Actual SQL MssqlChatThreads | Destructive owned-container SQL gate including inherited new methods | Skipped/blocked | No SQL execution/container creation/admission/cleanup proof. |
| Complete rpi-checks publication matrix/receipt | Publication candidate | Skipped/prohibited | Azure CLI invoked by full matrix is outside caller authorization; no receipt or bypass. |
| Live employee site/model, name confirmation and human accessibility | Operational/human acceptance | Unavailable/outside authorization | No live sign-in/provider execution, screen-reader/voice-control or approval claim. |

No web source changed. Research reports fetched Web Interface Guidelines; that retrieval is not a fresh changed-UI review. This Review makes no fresh Web Interface Guidelines, Fluent, WCAG, screen-reader or voice-control conformance claim. No tool/dependency install, external model call, credential-file access, heavy check or foreign resource/process inspection was performed.

## Outcome

* Outcome: Not accepted for complete task/whole-issue acceptance.
* Rationale: the bounded test/doc implementation matches the approved direction and no new source defect was identified, but required current full API/browser/actual SQL evidence remains materially absent (RV-001), and AC8 stays unproven. Existing checked AC1-AC7 are not newly delivered runtime functionality or fresh whole-feature validation.
* Severity summary: Critical 0; High 1; Medium 0; Low 0. Distinct existing live/publication follow-ups remain open; they are not fabricated implementation defects.
* Original Complete / Revise critique and historical Review outcomes, including historical RV-003, are preserved. No approval, issue closure, publication receipt or second Review is implied.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None established | No source fix requested on current evidence. |
| Decision gap or invalid assumption | None established | No rpi-plan re-entry or owner design decision required. |
| Material evidence gap | rpi-research, RV-001 | Parent/coordinator obtains later authorized current local API/browser/actual SQL evidence. |
| Non-blocking residual work outside this run | FU-530-LIVE; FU-530-PUBLICATION | Owner/coordinator separately authorizes live/name/human acceptance and complete publication gates. |

* Review execution: Complete; implementation execution: Partial.
* Outcome: Not accepted for whole-task acceptance.
* Validation coverage: exact diff/source/ownership and whitespace independently inspected; focused/static passes reported; full API/current browser/actual SQL/live/publication not established.
* Current blockers and authorization exclusions remain in force. Parent owns continuation; no nested agent or second assessment was used.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-30/employee-skills-chat-530-research.md](.copilot-tracking/research/2026-10-30/employee-skills-chat-530-research.md) | Existing delivery and bounded evidence research |
| [.copilot-tracking/plans/2026-10-30/employee-skills-chat-530-plan.md](.copilot-tracking/plans/2026-10-30/employee-skills-chat-530-plan.md) | Current scope and incomplete local validation |
| [.copilot-tracking/details/2026-10-30/employee-skills-chat-530-phase-details.md](.copilot-tracking/details/2026-10-30/employee-skills-chat-530-phase-details.md) | Shared tests, written safety protocol and blocked execution |
| [.copilot-tracking/reviews/plans/2026-10-30/employee-skills-chat-530-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/employee-skills-chat-530-plan-critique.md) | Preserved Complete / Revise and PC-001 |
| [.copilot-tracking/changes/2026-10-30/employee-skills-chat-530-changes.md](.copilot-tracking/changes/2026-10-30/employee-skills-chat-530-changes.md) | Implementation and reported validation |
| [.copilot-tracking/rpi-sessions/2026-10-30/employee-skills-chat-530-state.json](.copilot-tracking/rpi-sessions/2026-10-30/employee-skills-chat-530-state.json) | Parent-owned Review handoff state |
| [.copilot-tracking/reviews/logs/2026-10-29/employee-chat-skills-530-review.md](.copilot-tracking/reviews/logs/2026-10-29/employee-chat-skills-530-review.md) | Preserved historical findings, RV-003 and bounded correction outcome |
| [src/core/tests/test_chatthreads.py](src/core/tests/test_chatthreads.py) | Exactly two added shared methods |
| [src/api/tests/test_mssqlstore.py](src/api/tests/test_mssqlstore.py) | Existing MSSQL reuse and destructive fixture |
| [src/core/src/zava_forward/core/chat_panel.py](src/core/src/zava_forward/core/chat_panel.py) | Existing runtime behavior, not changed delivery |
| [src/api/tests/test_chat_panel.py](src/api/tests/test_chat_panel.py) | Existing targeted HTTP contracts |
| [src/api/checks/employee_chat_browser_check.py](src/api/checks/employee_chat_browser_check.py) | Existing browser source, not a fresh execution |
| [src/api/README.md](src/api/README.md) | Design and current dated evidence boundaries |
| [.copilot-tracking/reviews/logs/2026-10-30/employee-skills-chat-530-review.md](.copilot-tracking/reviews/logs/2026-10-30/employee-skills-chat-530-review.md) | This single independent Review |

## Next Steps

Return this record to the active parent for reconciliation and later routing of RV-001 to rpi-research under coordinator-admitted authorization. Preserve the current no-retry/no-heavy boundary, historical outcomes and unchecked AC8. Keep live/name acceptance and complete publication as distinct owner/coordinator follow-ups. No user action, second Review, closure verification or further execution by this reviewer is required.
