---
title: Conversational assistant experience live demo evidence (Refs #159)
description: Per-criterion record of what the live demo proves for the unticked acceptance criterion of issue 159 (keyboard operation and message announcement), with limits
ms.date: 2026-11-18
---

Refs #159. Scope is the synthetic demo, desktop only. Owner decisions of 2026-11-18 authorise live Azure in resource group `ama` (cap USD 700, no drills, no Key Vault rotation, no production change) and waive billing reconciliation, DPO and Legal approval and person-run assistive technology testing. No source code changed and no Azure resource was created. The only app state written was chat threads on one synthetic case, deleted at the end of each run.

## Method

* Playwright Chromium, 1366 by 900, signed in to `ca-cutover-test-demo-api` with the employee demo account (read at run time, never printed; a literal scan of the retained JSON and script found neither the user id nor the secret, and no e-mail address). Driver and output: `.copilot-tracking/evidence/2026-11-18/issue-159-live/live_chat_a11y_probe.py` and `live_chat_a11y_probe.json`; screenshot `chat-open-after-keyboard-turns-1366.png` in the same folder.
* The case workspace `#/case/{id}` of the first case returned by `/api/cases` was opened and driven by keyboard only: Tab, Enter, Shift+Enter, Escape. The only non-keyboard actions were sign-in, page loads and one programmatic `focus()` on the question box before the final Escape (an earlier run showed Escape does nothing once focus has left the non-modal panel; see adverse observations).
* Announcements were recorded by `MutationObserver` on the `role="log"` region and the `role="status"` region, plus the live-region attributes. This shows what a screen reader is offered, not what one speaks.
* axe-core (`axe.min.js` from the phase-witness store; the axe-core version was not recorded) ran on `#employee-chat` with the tags wcag2a, wcag2aa, wcag21aa and wcag22aa.
* Reused, not repeated: [issue-164-live-chat-grounding-evidence-2026-11-18.md](./issue-164-live-chat-grounding-evidence-2026-11-18.md) for citations, labels, refusal and workflow-only behaviour on the live demo.

## Observations (2026-11-18, final run)

| Step | Result |
| --- | --- |
| Launcher | `button`, accessible name "Chat", visible on the case workspace. |
| Tab from page start | Reached the launcher after 44 Tab presses (it sits late in the document order). |
| Enter on launcher | Opens `role="dialog"` "Employee assistant"; `aria-expanded` true; focus moves to the dialog heading. |
| Tab from heading | Close chat, About this chat, Chat size, conversation log (`tabindex` 0), then the question box. |
| Live regions | Log: `role="log"`, `aria-live="polite"`, `aria-relevant="additions"`, label "Employee assistant conversation". Status: `role="status"`, polite, atomic. Error: `role="alert"`. Question box labelled "Your work question", described by the entry warning, privacy note, key help and demo disclaimer. |
| Enter in question box | Submits. Observed additions: log entry for the user turn, status "Asking the assistant.", log entry for the assistant answer (outcome, label, citations summary), status "Answer added. Check the sources before relying on it." Focus stayed on the question box. |
| Shift+Enter | Inserts a newline without sending. |
| Second turn (follow-up) | Sent by keyboard; log grew to 4 messages; eight announcements in total. The workflow-only fallback status read "Workflow-only help added. No assistant answer was given. Check the case card for recorded facts." |
| axe, WCAG 2.2 AA tags | 0 violations, 21 passes on the open panel with two turns. |
| Escape in the panel | Panel hidden, `aria-expanded` false, focus returned to the launcher. |
| Cleanup | One thread listed, deleted (HTTP 200) (the listing held only that thread, so no earlier run left residue). |

## Per-criterion result

| # | Criterion | Demo result | Evidence and limit |
| --- | --- | --- | --- |
| 1 | Panel is available from a permitted case and never required to complete a task | Already ticked; not re-proven in full | The panel opened from a case; the case actions remain on the page. Unchanged. |
| 2 | Cited, labelled answers, abstention, label "AI suggestion, not approved" | Already ticked; re-observed | Answer entries show outcome, label and sources; see the #164 note for the label text. |
| 3 | Follow-up questions keep case context and re-check permissions | Already ticked; follow-up observed | Second turn ran in the same thread ("Questions in this conversation: 2 of 30"). Permission re-check not newly probed. |
| 4 | Proposal-only, cannot change a controlled record | Already ticked; consistent | The answer text states "No record was changed". |
| 5 | Model failure falls back to workflow-only with a clear message | Already ticked; observed | The live demo reached no model; the fallback message and status were shown. |
| 6 | Keyboard operable | Proven for the demo (desktop) | Open, send, newline, navigate, close and focus return all worked by keyboard; axe reported 0 violations. Escape proven only after returning focus to the panel. |
| 7 | Announces new messages | Proven at the programmatic level | The log and status regions carry the live-region semantics and each new message and status change was added to them. No assistive technology was run to confirm speech. |
| 8 | Screen-reader tested | Deferred, not proven | The owner waived person-run assistive-technology testing for the demo. Without it the criterion has no screen-reader evidence, so the combined criterion stays unticked. |
| 9 | Tokenomics: each turn records calls, tokens and outcome; thread bound; limit falls back to workflow-only | Already ticked; re-observed | Each answer carried "Model calls: 0. Tokens: Unknown. Outcome: fallback. Cost: Unknown." and the "2 of 30" thread bound. |

Net: the issue criterion "keyboard operable, screen-reader tested, and announces new messages" is two thirds evidenced for the demo. It stays unticked until a person runs a screen reader, or the owner rescopes the criterion for the demo.

## Adverse and incidental observations

* The panel is non-modal by design (`stayOpen`): after Send, one more Tab leaves the panel for the page header. Escape closes the panel only while focus is inside it; from elsewhere it does nothing. This is a design choice, not a defect shown by axe, but a keyboard user must return to the panel to close it, or use the launcher.
* The launcher is 44 Tab presses from the page start, after the navigation, queues and briefing controls.
* The demo disclaimer in the panel still reads "Answers are generated by an AI model" while the replies observed were rules-only (carried over from the #164 note).
* Both answers in the final run were produced without a model call (0 calls), so the announcement proof covers the workflow path only.
* The first probe attempts failed on harness errors (login selector, typing before focus moved to the question box). They wrote no JSON; only the final run is retained. They sent no question, so they created no thread; the final listing held one thread.

## Resources and residue

No Azure resource or role assignment was created or changed and no Azure CLI call was needed. Threads were deleted. Focused tier; no `rpi-checks.py --all`; independent review and hosted CI outstanding.

## Evidence limits

* Announcements are DOM mutations in live regions, not screen-reader output.
* One browser (Chromium), one viewport, one case and one account.
* The probe JSON retains the synthetic persona's case text; claims rest on it only where cited here.
