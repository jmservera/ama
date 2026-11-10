---
title: Issue 153 staff-time refusal and error guidance author review
ms.date: 2026-11-09
task_id: 153-staff-time-copy-1109
---

## Review execution and outcome

* Executed once on 2026-11-09T22:56Z by the author after implementation, against `timecapture.js` and `test_timecapture_copy.py`. Outcome: no open material finding in the assessed boundary; independent exact-head review remains required. Not an independent assessment, human approval or acceptance.
* Fresh Web Interface Guidelines fetched 2026-11-09T22:54Z (`logs/web-guidelines-review-fetch.md`, sha256 d246b026...0234, 191 lines) and applied to the changed web file.

## Guideline review (file:line, `timecapture.js`)

* Accessibility: async text keeps its live regions (`:6`, `:13` polite status; `:48` alert). No new controls, so labels, keyboard behaviour and focus are unchanged. Pass.
* Animation, typography, layout: none added. Pass.
* Content and copy: errors give the fix and a next step; active voice; existing sentence-case convention kept. Pass.
* Pre-existing, unchanged and out of scope: a failed save does not move focus to the message (guideline "focus first error"); status text is still announced politely.

## Contract and safety checks

* No server text is rendered (`textContent`/text nodes only). Only refusals the server raises before writing claim nothing changed; all other 403, 5xx, 409 and network outcomes say the outcome is unknown and to check My entries first, with the 200-entry limit. The ambiguous-save browser test proves both a lost request and a committed-but-lost response.
* Default-disabled behaviour, DPIA, consultation, notice and different-role enabling requirements, button availability and audit are untouched. No person is named; owners are the existing manager roles, the requester's role, you, or application support. No approval is asserted.

## Limits and routed work

* Source and served-fixture evidence only. Not WCAG conformance, assistive-technology, human resident-wording review, live acceptance or DPIA/DPO approval. Issue #153 C2, C3 and C5 and epic #149 stay open; this change Refs #153 and closes nothing.
* Routed to later work: other staff screens' raw error paths, knowledge-base audit row update (deferred for path ownership), axe incompletes not run here, focus-on-error pattern.
