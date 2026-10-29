<!-- markdownlint-disable-file -->
# Review: Shared resident and employee chat widget

## Scope and Evidence

* Task ID: 550; review date: 2026-10-29.
* Scope: full local source/task boundary P01/P02/P03-T01 and documentation in
  P03-T02; Review and requested commit are closeout work, not prior completed work.
* Assessed boundary: issue #550, owner request, shared resident/employee UI,
  resident intent regression, retained #503/#525/#541 boundaries and local evidence.
* Plan: .copilot-tracking/plans/2026-10-29/chat-widget-550-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/chat-widget-550-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-29/chat-widget-550-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-29/chat-widget-550-changes.md
* Research: .copilot-tracking/research/2026-10-29/chat-widget-550-research.md
* External validation: /home/azureuser/.copilot/session-state/0fb34315-ee29-4b90-a777-4a0e8804c6ce/files

## Opening Review State

* Goal: assess the source and reconciled evidence once; separate engineering
  results from operational, accessibility and publication approval.
* Scope: one complete task, read-only source/artifacts; current uncommitted
  candidate on feat/chat-widget-550, baseline 9b74ac8d. Not an exact committed-head
  publication assessment.
* Evidence readiness: one coherent research/plan/details/critique/changes set.
  Final 194 tests (one opt-in skip), separate 38-test opt-in run, static checks,
  new shared and existing audience browser checks available.
* Acceptance basis: all nine issue criteria, original owner safeguards, critique
  PC-001/002/003 dispositions, current lifecycle and retained safety boundaries.
* First comparison: full source diff and new shared assets/check against the
  plan and issue; fresh canonical web-guidelines source fetched 2026-10-29.
* Read-only boundaries: only this canonical review record and wrapper-owned state
  may change during Review; independent reviewer has no write authority.
* Initial blockers: no evidence-readiness blocker. Broader case-journey baseline
  fails identically before/after; human acceptance and full publication gate
  remain unperformed and cannot be claimed.

## Execution Status

Complete. One independent read-only implementation review executed on 2026-10-29
by chat-widget-review, followed by parent evidence synthesis in this record.
No source correction or repeat Review was performed after its findings.

## Plan-to-Change Reconciliation

| Scope | Recorded change | Reconciliation | Gap |
| --- | --- | --- | --- |
| P01/P01-T01 | Shared factory/CSS, both adapters, shared case entry, admission/draft guards | Reconciled with current source and final local evidence | RV-001 and RV-002 keyboard-focus defects |
| P02/P02-T01 | Explicit supported home intents and seven negative route/HTTP cases | Reconciled | No additional defect found |
| P03/P03-T01 | Unit/static/new and migrated real-browser checks | Reconciled; failures and unavailable checks disclosed | Existing checks miss unobscured external focus and visible-background completion |
| P03/P03-T02 | API README; this Review and requested commit | Documentation reconciled; Review complete, commit is parent closeout | Does not establish issue acceptance |
| Follow-Up Items | Baseline mobile summary, human acceptance, future publication gate | Retained outside active source scope | Owner actions remain open |

Plan/details/changes are preserved as the reconciled pre-Review snapshots.
Their pending Review/commit closeout prose is superseded by this record and
wrapper-owned state, not silently rewritten during Review.

## Completed Work Assessment

| Marker | Files | Change/evidence | Assessment |
| --- | --- | --- | --- |
| P01 | src/api/src/zava_forward/api/web/chat-widget.js and chat-widget.css; web/chat.js; resident_demo/web/assistant.js; entry HTML/static serving | Same bytes in actual apps; named controls/log, six/one choices, retained thread/draft, lifecycle fencing, privacy admission and manual callback handoff | AC-1 through AC-7 supported by local engineering evidence; keyboard-focus gaps below |
| P02 | src/api/src/zava_forward/api/resident_demo/chat.py; src/api/tests/test_resident_chat_api.py | Rat/unrelated question receives honest inability/contact, not home summary; no raw-text model forwarding | AC-8 supported; no additional safety/authority defect found |
| P03 | src/api/checks/chat_widget_browser_check.py; existing checks/tests; src/api/README.md | 194 related tests (one opt-in skip), separate 38-test opt-in run, static checks and both browser audiences pass | AC-9 only partially proven; review reproduced two missed keyboard scenarios |

## Implementation-Time Plan and Detail Update Assessment

| Update | Trigger and rationale | Reconciliation and critique disposition |
| --- | --- | --- |
| Native articles in log | Axe invalid list semantics | Reflected in details/changes; preserves native semantics |
| Chat-only bounded shared-file readiness | Keep ordinary workspace usable after chat dependency failure | PC-002 intent retained without shell-wide dependency |
| Hide retains, disposal fences | PC-001 lifecycle uncertainty | Documented and tested for hidden completions and obsolete operations; visible external focus was not covered |
| Exact clock/layout assertions | PC-003 measurable acceptance | Controlled 199/200ms and fast timer cleanup, pinned composer and reflow supported |
| Shared case entry, moved privacy/draft controls | Remove duplicate generic chat implementation while retaining #525 boundaries | Plan/details/changes and migrated checks reconciled; proposal/regulatory authority retained |
| Explicit manual callback handoff | Keep window open and avoid automatic manual-form action after send | Within confirmed user intent; booking confirmation stays separate |

## Critique and Material Revision Assessment

Original plan critique execution remains one pass with verdict Revise.
PC-001/002/003 received compatible direct dispositions and remain preserved.
No rejected confirmed user decision or additional divergent planning choice was
identified. Implementation-time changes are justified and do not authorize a
second critique or Review. The defects below are missing behavior, not a basis
to rewrite the original critique result.

## Plan Follow-Up Assessment

| Item | Why outside immediate scope | Owner/next action |
| --- | --- | --- |
| Baseline 320px case-summary height | Identical 1705.96875px before/after; unrelated page layout | Separate owner-maintained baseline investigation; retain <=1600px oracle |
| Human accessibility/live-site acceptance | Synthetic browser/axe does not establish operational acceptance | Owner-led screen-reader, voice and live-service acceptance |
| Publication gate | No push requested/authorized; full gate not executed | Future publishing owner runs external exact-head gate and obtains independent/human/hosted approvals |

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Nonmodal popup can completely obscure externally focused controls

* Scope: P01/P01-T01; AC-9.
* Evidence: src/api/src/zava_forward/api/web/chat-widget.js:104-106 and
  src/api/src/zava_forward/api/web/chat-widget.css:2. Independent reviewer used
  checked-in resident HTML/CSS, shared widget and actual resident adapter in an
  isolated file-backed browser without API requests. At 320x800, open Chat then
  Shift+Tab twice: focus reaches #signin-button while popup remains open and
  completely covers it. Popup bounds (16,72)-(304,712); focused button bounds
  approximately (25,487.59)-(126.22,531.59).
* Impact: keyboard users can navigate into invisible underlying controls.
  Normal Tab escape alone does not establish visible keyboard focus. The old
  resident external-focus hiding protection was removed.
* Destination: later rpi-implement.
* Smallest next action: preserve unobscured external focus, such as hiding without
  cancelling retained work, and assert actual focused-control visibility.
  Do not introduce a modal focus trap.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Visible-background employee completion steals focus

* Scope: P01/P01-T01; AC-9.
* Evidence: src/api/src/zava_forward/api/web/chat.js:116 and :138.
  Independent reviewer used original employee adapter/shared assets and controlled
  synthetic API promises: start ask, deliberately focus an external textarea,
  resolve answer. Focus moves from review-note to employee-chat-question.
* Impact: asynchronous success/error cleanup or initialization interrupts normal
  keyboard work and redirects subsequent typing into chat. focusInput checks
  popup visibility, not ownership of current focus; hidden-result tests miss it.
* Destination: later rpi-implement.
* Smallest next action: respect deliberately moved external focus during setup
  and success/error cleanup; add controlled external-focus completion coverage.

## Web-Guideline Findings

Canonical source freshly fetched by parent and independent reviewer:
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md.
Changed web scope reviewed against all fetched rules; repository Fluent/plain-
language/ASCII requirements override generic typography/Title Case preferences.

### src/api/src/zava_forward/api/web/chat-widget.js

src/api/src/zava_forward/api/web/chat-widget.js:104 - external focus can be fully
covered by the still-open nonmodal popup (RV-001).

### src/api/src/zava_forward/api/web/chat.js

src/api/src/zava_forward/api/web/chat.js:116 - completion redirects deliberately
moved external focus into chat; initialization at :138 does likewise (RV-002).

No additional substantive changed-scope finding was identified. Nonmodal
interaction, memory-only conversation, unsupported attachment/voice controls and
truthful rules labels are justified choices, not unsupported conformance claims.

## Defects

Two Medium defects: RV-001 and RV-002. No High/Critical finding identified.
No additional material authority, consent, session-isolation, resident routing
or draft-preservation defect was identified in the assessed boundary.

## Routed Findings

| Finding | Destination | Next action |
| --- | --- | --- |
| RV-001 | Later rpi-implement | Unobscured external focus without modal trapping or cancelling retained work |
| RV-002 | Later rpi-implement | Focus-owned initialization/completion and controlled external-focus regression |

These are later work, not corrected or closure-verified inside this Review.
A later implementation invocation does not require repeating this Review.

## Validation Evidence

Exact commands and log locations are in the changes artifact.

| Evidence | Status | Scope |
| --- | --- | --- |
| Related unittest modules | Passed, 194 tests, one opt-in skip | Resident/API/access/role/audit/web regressions |
| ZF_BROWSER_TESTS=1 test_chat_panel | Passed, 38 tests, no skip | Privacy admission failure and draft/error behavior |
| Ruff check/format, isolated new-check lint/format | Passed | API and new browser check |
| Configured mypy | Passed, 110 source files | CI typing surface |
| Node syntax | Passed | Three changed JS modules |
| Shared actual-app browser and existing audience checkers | Passed | Synthetic-only layout/keyboard/consent/session/recovery/denial evidence |
| Existing case journey | Failed | Unchanged baseline 320px summary height; modified chat lifecycle cases passed |
| Independent focused browser reproductions | Defects reproduced | RV-001 file-backed resident UI, RV-002 controlled employee promises |
| Full external exact-head publication gate | Unperformed | No publication authorized; not an exact committed-head assessment |
| Human screen-reader/voice, live-site/model acceptance | Unperformed | Owner acceptance remains open |

Independent Review relied on recorded suite results rather than rerunning the
complete suites. Its focused reproductions are additional evidence, not claimed
as actual-service acceptance.

## Residual Work

Retain distinct baseline-layout, owner human-acceptance and future-publication
follow-ups. They are not added as new active plan scope or mislabeled as defects.

## Blockers and Remaining Work

AC-9 is not fully met because RV-001/RV-002 remain open. No issue-closing keyword
is justified; any future PR must use Refs #550 until all criteria are proven.
Requested local commit is parent closeout only, not acceptance or publication.
No source change, repeat Review, remote write or Azure operation is authorized
by this record.

## Outcome

* Execution: Complete.
* Outcome: Defects found.
* Rationale: local engineering evidence supports AC-1 through AC-8 and most
  AC-9 behavior, but the independent Review reproduced two keyboard-focus
  defects. Do not report a conformant outcome or issue completion.

## Closeout Routing Record

| Class | Destination | Owner/next action |
| --- | --- | --- |
| Implementation defects | Later rpi-implement | RV-001/RV-002; preserve original adverse Review |
| Decision gap or invalid assumption | None identified | No new decision required |
| Material evidence gap | None blocking this bounded Review | Human/publication acceptance is separately scoped |
| Non-blocking residual work | Distinct owner follow-ups | Baseline summary layout, human acceptance, publication gates |

Execution Complete; outcome Defects found. Review is complete but issue acceptance
is blocked. Parent may make the requested local commit with Refs only; no push.
