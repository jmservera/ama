---
title: Issue 83 table inventory D1 research
ms.date: 2026-11-11
task_id: issue-83-table-inventory-d1-1111
parent_task: issue-83-waiting-view-1111
---

## Scope

Continuation for PR 1444 (same branch, no new issue). Hosted API job 130403684801 failed one test: `test_accessibility_baseline.Wcag22Baseline.test_every_table_has_a_caption_and_column_headers` (13 != 12, "new table: audit it and update this check and the record"). Raw log: `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/pr1444-hosted-api-failed-1111.log`. Original issue83 artifacts, source-author Review and independent assessment are preserved unchanged.

Admitted: one bounded D1 audit and test-metadata correction. Not admitted: product JS, API, CSS, store, permissions, D2, new issue, push.

## Evidence

* C1 Pre-change reproduction at head dd3c32910c3c5205a2cbedbe74608411c6f9f341 (tree edf6b0501df00c01bf8287de22da20e83240458d), worktree sources via PYTHONPATH: the same test fails, `AssertionError: 13 != 12`, output kept at `.copilot-tracking/reviews/logs/2026-11-11/issue-83-table-inventory-d1-1111-pre-change.txt`.
* C2 Test mechanism (`src/api/tests/test_accessibility_baseline.py`, test named above): regex `h\("table", \{\},\s*(.{0,60})` over every `web/*.js`; asserts the first 60 characters contain `h("caption"`; rejects `h("th", {}`; asserts the count. The regex does not match `ops.js` line 28 (`h("table", { "aria-label": title }`), a pre-existing form outside this failure.
* C3 Per-file regex-site counts, main 7880b95b vs dd3c: aftercare.js 1/1, app.js 5/6, ops.js 1/1 (line 453; the separate line 28 `aria-label` form is not matched), panels.js 3/3, progress.js 1/1, role-screens.js 1/1. Only app.js changed (+1). Counted by the regex: 12 on main, 13 at dd3c. The thirteenth is `app.js` `handoffWaitingView`.
* C4 Thirteen counted sites (file: caption variant): aftercare.js caption in table; app.js five existing (sr-only x4, one `muted`), plus the new waiting table (sr-only); ops.js one (muted caption, line 453); panels.js three sr-only; progress.js; role-screens.js.
* C5 Audit of the new table (`app.js`, function `handoffWaitingView`, table in `section.card[aria-label="Unaccepted handoffs"]`): first child is `caption.sr-only` "Unaccepted handoffs and how long each has waited"; seven `th scope="col"` (Case, Status, Waiting, Due, Chase owner, Proposed receiver, Escalation); each row's case id is `th scope="row"` with an `a href` to the case; status, waiting hours, due, owners and escalation reasons are `td` text (not colour-only); the wrapper is `div.table-scroll[tabindex=0][role=region][aria-label="Unaccepted handoffs table"]`, matching the existing named scroll-region pattern; the global `:focus-visible` rule (`style.css` line 48) gives the two-tone focus indicator; `.table-scroll{max-width:100%;overflow-x:auto}`. No product accessibility defect found in this source reading.
* C6 Constructed-browser evidence already in `src/api/tests/test_handoff_waiting_view.py` (Chromium, opt-in): table renders, links keyboard reachable, failure shows alert with no table. Not a screen-reader, reflow or conformance result.
* C7 Baseline record `docs/reference/research/ux/wcag-conformance-baseline.md` Tables row records 11 (2026-11-04) and 12 (2026-11-10, unwired aftercare); it needs the dated 13 entry and limitations. Index entry and append-only log must be updated for a material KB change.
* C8 Web rules retrieved 2026-11-11 from the vercel-labs source (two parts, complete); relevant: semantic `<table>` and `<a>`, keyboard-reachable scroll region, visible focus. Accessibility skill rules (WCAG 1.3.1, 2.4.7, 4.1.2) applied at source level only.

## Decision

Register observed inventory 13 in the existing assertion (a literal, not dynamic), keep the regex and failure-on-new-table mechanism unchanged, and record the audit and limits in the baseline, index and log. No extra regression: the existing test already enforces caption-first and the bare-`th` ban for the new table; a scope-attribute test would be a new policy beyond this failure.

## Planning Readiness

Ready. Disposition: executed.

## Limits

Not tested: screen-reader navigation, reflow at 320 px, zoom, assistive technology, manual acceptance. No approved global OD-09 times exist. Whole #83 criterion 3 stays unmet. Out of scope: original critique's three Low relative links and unbounded-row performance qualification; `ops.js` aria-label table form.
