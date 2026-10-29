---
title: Employee chat skills 530 independent review
description: Single post-implementation review of the committed candidate
ms.date: 2026-10-29
---

## Opening Review State

* Interpreted review goal: independently assess issue #530 implementation, permissions, stale asynchronous state, legacy panels and meaningful validation.
* Scope: committed candidate e34cd84a829397f64899ffa4a6e302d5c0a16dc0 against d70ee60ab3d7346a9991cf64382d9985f4d09f2e.
* Evidence readiness: clean matching HEAD; supplied research, plan, details, changes and state read. Critique is under plans, not the template's reviews/plans directory.
* Acceptance basis: confirmed single chat/five bounded skills/no router; projected sources, read-only answers, disclosures, fallback, minimal audit and accessible employee launcher.
* First comparison boundary: complete committed diff, current implementations and tests, then recorded external validation.
* Active read-only boundaries: only this review record may be written; no source fixes, state changes, commits, delegation or second Review.
* Initial blockers: full suites/disposable SQL blocked by occupied shared lock; no retries, queuing or foreign-resource use. Publication invokes prohibited az. No paid inference, live verification, push or remote writes authorized.

## Scope and Evidence

* Task: #530 / employee-chat-skills-530.
* Review date: 2026-10-29.
* Assessment count: one independent post-implementation Review; no delegation or second Review.
* Assessed commit: e34cd84a829397f64899ffa4a6e302d5c0a16dc0.
* Assessed base: d70ee60ab3d7346a9991cf64382d9985f4d09f2e.
* HEAD matched the candidate before and after independent checks. The initial worktree was clean. Only this review record was added.
* Compared artifacts:
  * .copilot-tracking/research/2026-10-29/employee-chat-skills-530-research.md
  * .copilot-tracking/plans/2026-10-29/employee-chat-skills-530-plan.md
  * .copilot-tracking/plans/2026-10-29/employee-chat-skills-530-critique.md
  * .copilot-tracking/details/2026-10-29/employee-chat-skills-530-phase-details.md
  * .copilot-tracking/changes/2026-10-29/employee-chat-skills-530-changes.md
  * .copilot-tracking/rpi-sessions/2026-10-29/employee-chat-skills-530-state.json
* Evidence comparison used the committed diff and current service, HTTP gates, chat isolation, external-context allowlist, assistants registry, agents ChatModel, employee shell, AsyncAction, preserved case/regulatory panel, unit tests and actual browser-check source.
* Context read: docs/case_study_48_original.md; docs/case_study_48_addendum.md; docs/reference/README.md; docs/reference/memory.md; docs/reference/research/sector/housing-association-primer.md; relevant design-system, content-standard and WCAG-baseline sections. No new legal currentness or operational interpretation is asserted.
* External evidence inspected, relative to this worktree:
  * ../../../.copilot/session-state/8df83efd-d268-4456-99f8-d2978b1a7a23/files/api-targeted-final.log
  * ../../../.copilot/session-state/8df83efd-d268-4456-99f8-d2978b1a7a23/files/core-targeted.log
  * ../../../.copilot/session-state/8df83efd-d268-4456-99f8-d2978b1a7a23/files/chat-browser-530/axe-results.json

## Execution Status

* Review execution status: Complete. The supplied boundary was assessed once, including independently executed small checks and explicitly unavailable evidence.
* Implementation execution status: Partial. P03-T02 remains unchecked; full-suite and actual SQL validation have not completed.
* These are not acceptance statuses. The outcome below is Not accepted.
* No source, plan, critique, details, changes, research or state corrections were made. Findings below are the original uncorrected Review findings.

## Plan-to-Change Reconciliation

| Current plan scope | Changes summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | Explicit general/five-skill turns, filtered sources and metadata audit | Reconciled | Current role/owner/case checks and privacy admission retained. One model call, no proposal invocation. |
| P01-T02 | Existing ask route and new skills metadata endpoint | Reconciled | Explicit null/invalid/extra-field rejection; omission preserves legacy no-case abstention. |
| P02-T01 | Global dialog, route/session/denial disposal | Partial | Successful ask-path disposal exists, but skills-loading denial does not dispose the dialog: RV-001. |
| P02-T02 | AsyncAction/native Fluent-derived controls and old panels | Reconciled | Existing case/regulatory panel source remains unchanged; no framework substitution. |
| P03-T01 | Eight additional unit methods and one browser check | Partial | Useful semantic coverage exists; stale successful-completion evidence can be skipped: RV-002. |
| P03-T02 | Static, targeted unit and browser results; full suites/SQL blocked | Reconciled as incomplete | Recorded blockers are honest; missing material evidence remains RV-003. |
| P03-T03 | API guide, knowledge-base index/log and local evidence | Reconciled for supplied candidate | Original critique remains Revise. Review now exists; no publication receipt or full acceptance is implied. |
| Follow-Up Items | Live/human acceptance and publication boundary | Reconciled as open | Remain distinct later work, not new active implementation tasks. |

## Completed Work Assessment

| Related scope | Current source and evidence | Assessment |
| --- | --- | --- |
| P01: architecture | src/core/src/zava_forward/core/chat_panel.py; src/core/src/zava_forward/core/assistants.py; src/agents/src/zava_forward/agents/chat.py | Exactly five registry advisory lenses plus explicit general mode. Purpose and category selection are prompt/source transformations, not separate routed agents. No router, tools or domain-write path added. Existing injected adapter needs no skill-specific change. |
| P01: permission and data boundary | src/core/src/zava_forward/core/chat_isolation.py; src/core/src/zava_forward/core/export_fields.py; src/api/src/zava_forward/api/server.py | Current employee and owner-filtered thread checked each turn, then existing case projection and closed allowlist, then skill narrowing. No raw-record capture to fill missing survey/funding/quality facts. Proposal roles do not become chat permissions. |
| P01: citations and failure | src/core/src/zava_forward/core/chat_panel.py; src/api/tests/test_chat_panel.py | Permitted citation IDs only; malformed/uncited outputs abstain; missing/failed models give workflow-only fallback. Lexical refusal/action checks are not semantic accuracy guarantees. Each returned result carries the fixed AI label. |
| P01: privacy and audit | src/core/src/zava_forward/core/chat_panel.py; src/core/src/zava_forward/core/chat_privacy.py; src/core/src/zava_forward/core/chatthreads.py | Replacement of privacy.add_message preserves its require/redact behavior while obtaining actual stored sequence. New audit stores thread ID, question sequence, skill and outcome, not raw question text. Chat persistence and metadata audit are intentional writes, not domain writes. |
| P02: employee shell | src/api/src/zava_forward/api/web/chat.js; app.js; index.html; style.css | Launcher hidden signed out/Contractor; case-route context snapshot versus explicit general/no-record disclosure. Native labels, modal, polite log/status, text-node rendering, bounded visible exchange, shared busy feedback and source/unverified labels. RV-001 is the denial-path exception. |
| P02: stale/session handling | src/api/src/zava_forward/api/web/chat.js:15-39,78-102; src/api/src/zava_forward/api/web/app.js:69-72,293-294 | Abort plus root/session/signal guards suppress obsolete UI completion; route changes, login and sign-out dispose. Same-case tab changes intentionally retain context. No claim of cancelling an already-running server model call. |
| P02: preservation | src/api/src/zava_forward/api/web/chat.js:130 onward; src/api/src/zava_forward/api/server.py | Old case and regulatory panels are unchanged below the added launcher block; legacy omitted-skill endpoint remains distinct. Existing proposals/regulatory authorization is not widened by this change. |
| P03: meaningful tests | src/api/tests/test_chat_panel.py; src/core/tests/test_chat_panel.py; existing isolation/thread/privacy/adapter tests | New tests check selected purpose, one inference, all skills, no-record sources, invalid input before persistence/inference, role projection/privacy denial, metadata audit and unchanged case. Existing negative output/refusal/isolation tests are retained, not replaced with mere source-presence checks. |
| P03: browser evidence | src/api/checks/employee_chat_browser_check.py; src/api/checks/design_system_browser_check.py | Constructed loopback server strips inherited model/data settings; synthetic privacy admission is opt-in. Actual unavailable-model fallback is exercised; six successful answer states are intercepted rendering fixtures, not real model behavior. Two actual dialog-scoped axe states are evidenced. RV-002 limits the stale-success claim. |

Existing owner-isolation coverage includes same-role/cross-user, cross-role and spoofed-key thread probes; the new skill tests reuse the same owner-checked endpoint. JSON/SQLite persistence tests and SQL portability assertions are not actual SQL Server execution.

## Implementation-Time Plan and Detail Update Assessment

| Area | Change and trigger | Reconciliation and assessment |
| --- | --- | --- |
| P01-T02 / PC-002 | Omitted legacy versus explicit general wire modes | Reflected consistently in plan, details, endpoint, service and negative tests; no thread-task schema change. |
| P02-T01 / PC-001 | Session/disposal guards and explicit native focus wrapping | Reflected in plan/details/current source. Browser focus containment is useful. Denial coverage is incomplete at metadata loading (RV-001); original critique was not silently closed by this Review. |
| P03-T01 / PC-003 | Scan real open dialog and isolate constructed privacy references | Current check targets dialog in unavailable-model and synthetic-answer states. Harness change is narrow, optional and preserves original default behavior. |
| P03-T01 | Global script readiness test expectations | Necessary consequence of employee-wide chat.js; Contractor expectations retained. Not an unrelated route rewrite. |
| P03-T02 / PC-004 | Explicit worktree source bindings and occupied-lock disposition | The supplied owner direction/disposition rejects PC-004's alleged parent-context tmp prohibition. Preserve that rejection, not a new defect or reopened decision. This reviewer performed no tmp/venv/lock operations and did not verify shared-environment history. |
| P03-T03 / PC-005 | No-az full-gate disposition | Plan/details/changes/state explicitly distinguish local candidate evidence from forbidden full runner/publication. No runner, receipt, push or remote write executed. |
| P03-T02 | Partial validation rather than completion | Unchecked marker and blockers consistently preserved across all current artifacts. No basis to mark the whole issue accepted. |

The amendments preserve confirmed intent and do not justify introducing a router or widening data. No unresolved material architecture decision requires rpi-plan. P03-T01 and P02-T01 completion summaries are qualified by the original findings below.

## Critique and Material Revision Assessment

* Original critique: Complete / Revise, with PC-001 through PC-005 preserved verbatim in its original artifact.
* PC-001: accepted and substantially implemented; skills-fetch 403/404 disposal remains unimplemented (RV-001), and the delayed-success test is not reliable proof (RV-002).
* PC-002: accepted; explicit general/legacy distinction and invalid/null/type behavior verified in source/tests.
* PC-003: accepted; exact dialog target, pinned axe hash check and two distinct scanned states verified.
* PC-004: preserve the recorded partial rejection and owner's tmp/canonical-lock direction; do not convert the critique's context mismatch into a new supported defect.
* PC-005: accepted; blocked full publication gate recorded. Passing local tests do not satisfy it.
* Dependent-work assessment: current plan/details contain the accepted corrections; no unapproved significant design departure was found. This review does not reconstruct or certify every earlier execution ordering event.

## Plan Follow-Up Assessment

| Follow-up | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Live employee-site/model verification | Explicitly not authorized; loopback/intercepted evidence cannot substitute | Owner schedules separately authorized verification | Open distinct follow-up; no live claim. |
| Screen-reader/voice-control and human accessibility acceptance | Not supplied by axe or native semantics | Owner/accessibility reviewer arranges human checks | Open distinct follow-up; no WCAG or assistive-technology acceptance. |
| Complete publication gate | Runner invokes prohibited az; no publication authorized | Owner resolves authorization/prerequisites in separate publication work | Open distinct follow-up; no runner invocation, bypass or fabricated receipt. |

Full suites/disposable SQL are not merely optional follow-ups: P03-T02 still requires their material local evidence (RV-003).

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Skills-loading denial retains the case-bound dialog

* Related scope: P02-T01 and accepted PC-001.
* Evidence: src/api/src/zava_forward/api/web/chat.js:123-124 - skills-fetch catch displays an unavailable message but does not dispose on 403/404. The ask-path catch at lines 95-98 does dispose. A role denial arriving while GET /api/chat/skills loads therefore takes a different lifecycle path.
* Independent reproduction: an in-memory Node harness executed the actual employeeChat initializer with a synthetic case route and an api() rejection carrying status 403. Output: metadataDenied403=true, dialogStillOpen=true, dialogRemoved=false, caseContextRetained=true.
* Impact: the required clear-on-denial contract is incomplete and stale case context remains visible in a modal after denied chat access. No prior-answer disclosure or successful authorization bypass was reproduced; this initialization path has not yet populated a transcript.
* Destination: later rpi-implement.
* Smallest useful next action: apply the existing denial-disposal policy to skills loading and add deterministic metadata 403/404 tests, retaining ordinary workflow recovery and appropriate focus.
* Status: original, uncorrected finding; no fix made by Review.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Stale-response browser proof can pass without an outstanding ask

* Related scope: P03-T01, stale async/session acceptance and PC-001 resolving evidence.
* Evidence: src/api/checks/employee_chat_browser_check.py:115-125 waits for aria-busy, not intercepted request arrival. AsyncAction sets aria-busy when the asynchronous task starts; it does not establish that the Python interception handler has populated held. The successful delayed reply is conditional on `if held`; an empty held list skips it. The check also accepts transport cancellation instead of observing a completed late-success callback.
* Impact: the test and PASS summary can claim delayed-response suppression without delivering any obsolete successful reply. The actual current()/abort guards are present and sensible by inspection; this finding is about missing deterministic regression proof, not a demonstrated stale-answer leak.
* Destination: later rpi-implement, test correction within the accepted direction.
* Smallest useful next action: require arrival of the outstanding ask before navigation; keep the transport-abort check separate from an in-memory delayed-completion test that actually resolves after disposal/session change and asserts no replacement transcript, status or focus mutation.
* Status: original, uncorrected finding; no test changed or rerun as a second Review.

<!-- rpi:review id=RV-003 -->
### RV-003 [High]: Required full-suite and actual SQL evidence is missing

* Related scope: P03-T02 and full-task acceptance.
* Evidence: plan marker remains unchecked; changes and state identify occupied canonical heavy-lock admission and foreign PID 771340/python3. Supplied logs establish targeted API 82 and core 54 tests, not complete suites. Core JSON/SQLite tests do not establish disposable SQL Server behavior.
* Impact: material persistence/regression acceptance remains unestablished. Neither a passing browser check nor the pure checks repeated here permits whole-issue acceptance or publication.
* Destination: rpi-research for missing validation evidence, with the parent coordinating later permitted validation execution.
* Smallest useful next action: once legitimately admitted in later coordinated work, run the required complete local suites and owned disposable SQL validation against an identified candidate/base; retain actual logs. Do not retry/queue the lock now, interrupt/reuse foreign resources, or invoke prohibited az.
* Status: original, unresolved evidence gap, not an asserted SQL implementation defect.

## Defects

* RV-001: employee dialog denial lifecycle defect; later rpi-implement.
* RV-002: non-deterministic stale-completion regression evidence; later rpi-implement.
* No additional domain-write, router, adapter, role-projection or legacy-panel regression was identified in the assessed source boundary.

## Routed Findings

| Finding | Destination | Owner or next action | Reason |
| --- | --- | --- | --- |
| RV-001 | rpi-implement | Parent schedules metadata-denial disposal and regression checks | Accepted lifecycle contract not fully implemented. |
| RV-002 | rpi-implement | Parent schedules deterministic stale-success/session test | Existing test can skip its central assertion. |
| RV-003 | rpi-research | Parent obtains missing local suite/owned SQL evidence when permitted | Material evidence absent; no invented pass. |

Later implementation of these routed findings does not require another Review. Preserve this complete original finding set and verdict.

## Web Interface Guidelines Assessment

Fresh complete source retrieved on 2026-10-29 from https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md before changed-web review.

Changed web hunks were read with applicable surrounding shared styles/helpers. Assessment covered labels/native semantics/live updates; focus/keyboard; form naming, feedback and busy states; reduced motion; content wrapping and bounded transcript; state/disposal; touch/scroll containment; responsive layout; theme/select colors; hover/focus inheritance; and plain actionable error/AI wording.

* src/api/src/zava_forward/api/web/chat.js:123 - denied skills metadata leaves the case-context dialog open; RV-001.
* src/api/src/zava_forward/api/web/app.js - no additional substantive changed-hunk finding; route/login/sign-out lifecycle wiring assessed.
* src/api/src/zava_forward/api/web/index.html - labelled native launcher with dialog hint and signed-out hidden state.
* src/api/src/zava_forward/api/web/style.css - token-based dialog/native select colors, wrapping, bounded viewport and contained overscroll; no new animation.
* The question has name/autocomplete-off/visible label; skill has a name/label; rendering uses text nodes. No new images, media, gestures, hydration, date/currency formatting or long unbounded result list to assess.
* Chat text/case details should not be serialized into a URL merely to satisfy generic state-linking advice. Repository plain-ASCII punctuation, sentence case and resident/human boundaries take precedence over generic curly-quote/ellipsis/title-case preferences.
* These are source-review observations plus the limited automated evidence below, not complete Web Interface Guidelines, WCAG, Fluent, screen-reader or voice-control acceptance.

## Validation Evidence

| Check | Scope | Status | Evidence and boundary |
| --- | --- | --- | --- |
| python3 -B -m unittest test_chat_panel -q | Core pure tests with explicit worktree core/agents/test paths and bytecode disabled | Passed independently | 11 tests. No SQL, model or server resources. |
| python3 -B -m unittest test_chat_model -q | Existing agents adapter with explicit worktree paths and bytecode disabled | Passed independently | 2 tests; synthetic provider envelopes only. |
| node --check on chat.js and app.js | Changed JavaScript | Passed independently | Syntax only. |
| git diff --check base candidate | Entire committed change | Passed independently | No whitespace errors. |
| In-memory Node metadata-denial reproduction | Actual new employeeChat initialization with 403 rejection | Defect reproduced | RV-001; not a full browser or accessibility test. |
| Supplied api-targeted-final.log | Five API selectors | Passed, supplied evidence inspected | 82 tests, final OK; logged law-store exception is not a failed suite result. Not a complete API suite. |
| Supplied core-targeted.log | Panel/thread/privacy selectors | Passed, supplied evidence inspected | 54 tests, final OK. JSON/SQLite, not actual SQL Server. |
| API/core Ruff, format and mypy | API/core projects | Reported passed in committed changes | 107 API/157 core files reported typed. Not independently rerun or backed here by a complete receipt. |
| Agents targeted panel adapter/provenance/fixture tests | Three agents selectors | Reported passed in committed changes | 16 tests reported; this Review independently repeated only the 2 adapter tests above. |
| Employee browser check | Constructed loopback employee UI | Reported passed; source and axe output inspected | Actual fallback versus six intercepted answers distinguished. Browser not repeated; stale-success proof qualified by RV-002. |
| Supplied axe-results.json | Open dialog, actual-model-unavailable and synthetic-cited-answer | Passed, supplied evidence inspected | Each state: 0 violations, 20 passes. Does not cover whole page/all states/manual acceptance. |
| Complete local API/core/full relevant suites and disposable SQL | Required P03-T02 | Blocked / not run | Existing foreign heavy-lock ownership; no retry, queue, interruption or foreign resource use by reviewer. RV-003. |
| Complete publication runner/receipt | Publication candidate | Blocked / not run | Invokes forbidden az; no receipt or publication readiness established. |
| Live employee site/model, hosted approval and human assistive-technology checks | Operational acceptance | Not run / not authorized | No live, paid-model, screen-reader, voice-control or human acceptance claim. |

Supplied external results are useful evidence, not a clean exact-head/base/tool/image-bound full receipt. No validation output directories, temporary fixtures, environment installations, database resources or browser processes were created by this Review.

## Residual Work

* Preserve distinct existing owner follow-ups for live verification, screen-reader/voice-control/human checks and authorized publication prerequisites.
* Do not silently add those follow-ups to completed P01/P02 work or convert their absence into an implementation defect.

## Blockers and Remaining Work

* P03-T02 is materially incomplete; RV-003 retains the local full-suite/SQL blocker.
* RV-001 and RV-002 need later implementation/test work; this review leaves them uncorrected.
* Full publication remains separately blocked by no-az/no-push directions. No bypass or protection change is proposed.
* Source corrections, later commits or base changes invalidate any earlier candidate-specific gate evidence. Original critique and this Review remain historical records, not rewritten acceptance.

## Outcome

* Outcome: Not accepted.
* Rationale: source direction is substantially consistent with the owner-selected bounded architecture, but the denial lifecycle and stale-success regression proof need later correction, and required full-suite/actual SQL evidence remains missing. Do not mark the whole issue accepted.
* Severity summary: 0 Critical, 1 High evidence gap, 2 Medium implementation/test findings, 0 Low.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation/test defects | rpi-implement | Parent routes RV-001 and RV-002 to later work, without modifying original Review. |
| Decision gap or invalid assumption | None identified | No router/permission widening or new architecture decision needed. |
| Material evidence gap | rpi-research | Parent coordinates RV-003 evidence when admitted and authorized. |
| Non-blocking residual work | Distinct owner follow-ups | Live/manual acceptance and publication prerequisites remain separate. |

* Review execution: Complete.
* Planned implementation execution: Partial.
* Outcome: Not accepted.
* Validation coverage: independent 11 core pure/2 adapter tests, JavaScript syntax, committed diff check and denied-metadata reproduction; inspected targeted logs and two limited axe states.
* No second Review, remote write, commit, full suite, SQL, paid model or az operation performed.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-29/employee-chat-skills-530-research.md](.copilot-tracking/research/2026-10-29/employee-chat-skills-530-research.md) | Research basis and bounded architecture. |
| [.copilot-tracking/plans/2026-10-29/employee-chat-skills-530-plan.md](.copilot-tracking/plans/2026-10-29/employee-chat-skills-530-plan.md) | Current plan; P03-T02 incomplete. |
| [.copilot-tracking/plans/2026-10-29/employee-chat-skills-530-critique.md](.copilot-tracking/plans/2026-10-29/employee-chat-skills-530-critique.md) | Original Complete / Revise critique. |
| [.copilot-tracking/details/2026-10-29/employee-chat-skills-530-phase-details.md](.copilot-tracking/details/2026-10-29/employee-chat-skills-530-phase-details.md) | Reconciled phase contracts. |
| [.copilot-tracking/changes/2026-10-29/employee-chat-skills-530-changes.md](.copilot-tracking/changes/2026-10-29/employee-chat-skills-530-changes.md) | Implementation results and blockers. |
| [.copilot-tracking/rpi-sessions/2026-10-29/employee-chat-skills-530-state.json](.copilot-tracking/rpi-sessions/2026-10-29/employee-chat-skills-530-state.json) | Supplied pre-Review parent state, unchanged. |
| [.copilot-tracking/reviews/logs/2026-10-29/employee-chat-skills-530-review.md](.copilot-tracking/reviews/logs/2026-10-29/employee-chat-skills-530-review.md) | Single complete original Review result. |

## Next Steps

Return this record to the active parent. Route RV-001/RV-002 to later rpi-implement and RV-003 to rpi-research for permitted missing validation evidence. Preserve the original critique and this finding set; do not run a second Review or alter source in this stage. Keep all work local and retain the current resource/az/publication restrictions.
