---
title: Issue 220 bounded finding disposition
description: Independent disposition of the historical action correction and permitted fresh primary evidence only
ms.date: 2026-10-19
ms.topic: reference
assessment_type: bounded-finding-disposition
issue: jmservera/ama#220
branch: feat/affected-person-challenge-220
comparison_head: d6874f3ee3d2dcfae096bb2f5fc8c3bd299097f4
rv001: corrected-within-assessed-boundary
rv002: fresh-primary-evidence-available-historical-access-limit-preserved
publication_authorized: false
---

## Scope and verdict

RV-001 is corrected within the retained-priority historical action boundary.
RV-002 now has independently accessible, substantive fresh primary evidence.
This does not establish access to the original excluded external logs or
retroactively change the original assessment.

This is the specifically requested bounded finding disposition, not the
original RPI Review, a repeat Review, plan critique, security audit or whole-issue
assessment. No Review/code-review skill or delegated assessment was used.
Only this report was written; existing dirty work was left in place.

The coordinator directive at
`/home/azureuser/.copilot/session-state/b9cc4727-b806-4e0f-a2cf-c5010d92428c/files/issue220-coordinator-review-disposition.txt`
was readable. The canonical plan, phase details, changes and state were consulted
for the selected continuation and historical limits. Executable assessment is
limited to the current three-file delta against `d6874f3e`, including directly
relevant existing draft/route helpers, not unrelated original implementation or
issue #360 infrastructure/operator work.

## Source and original-artifact boundary

HEAD remained `d6874f3ee3d2dcfae096bb2f5fc8c3bd299097f4`; the correction is
uncommitted working-tree content, not a corrected frozen commit. Independently
verified SHA256 values match `source-and-originals.sha256`:

| File | SHA256 |
| --- | --- |
| `src/api/src/zava_forward/api/web/app.js` | `e99599e11591dfde3de338b515d82d73d0b16984f7f36102bb362577d2e084c8` |
| `src/api/src/zava_forward/api/web/panels.js` | `66834393fd91ea9437376d40cabaa346f16b7a01659bcdf112da2b72e08869de` |
| `src/api/checks/challenge_browser_check.py` | `3c1d9ff182b7796f8025788c7ae79521c5255775b8abd47e06aff55572ea82c5` |

Original artifacts were checked for byte preservation by hashes and absence of
diff against HEAD, not reassessed or rewritten:

* `.copilot-tracking/reviews/logs/2026-10-19/affected-person-challenge-220-review.md`:
  `eec22d64aea801d63ae007c5c8b6e4b69709099d70f4e3a7c9b8f4dc2744fc8e`.
  Original **Partial / Not accepted** remains unchanged.
* `.copilot-tracking/reviews/plans/2026-10-19/affected-person-challenge-220-plan-critique.md`:
  `1a37cbb8f57d8e673eac17d86b81b983ec6244a09eb104d7c157109ac16ffaf0`.
  Original **Revise** remains unchanged.

## Primary evidence inspected and limits

The independently readable fresh bundle is
`/home/azureuser/.copilot/session-state/bc713866-d9c3-479b-acc9-bb5780f2ebcd/files/issue220-evidence/`.
It contains newly executed public-synthetic outputs, not relocated or
reconstructed restricted historical logs. No permitted-bundle read was refused.
Original excluded external logs and gate receipts were intentionally not opened;
their historical access gap remains, with no independent inspection claimed.

| Evidence actually inspected | Observed result |
| --- | --- |
| `manifest.txt`, `source-and-originals.sha256`, `outputs.sha256` | Commands, boundaries and substantive output bindings available; all 5 source/original hashes and all 10 output hashes verified |
| Complete `focused.log` | 19 JSON/SQLite/HTTP challenge tests OK, no skips; explicit missing-law-store Unknown diagnostics |
| Complete `static-final.log` | Ruff passes; 28 files already formatted; mypy passes for 62 source files |
| `history-before.log`, failure and relevant DOM snapshot sections | Actual missing Older suggestions control; snapshot shows 50 of 52 targets and visible CH-3 through CH-52, not older CH-1/CH-2 actions |
| `history-after.log`, terminal failure section | Intermediate strict locator ambiguity between summary and submit button, not a passing product result |
| Complete `history-final.json` and substantive `history-final.log` result/diagnostics | Passed; Chromium 156.0.8078.4; 52 targets, 53 challenges; CH-1 correction, CH-2 older explanation, exactly one stale target |
| Complete `browser-final.json` and substantive `browser-final.log` result/diagnostics | Original mode passed; Digital/Phone; four scoped scans; explicit screen-reader/human acceptance Not run |

Both final raw-log JSON results were independently parsed and compared equal to
their corresponding JSON files. All preceding final-log lines are the explicit
missing-law-store diagnostic tracebacks, not hidden browser failures. Rule
coverage is Unknown; none of these outputs constitutes legal-rule approval.
The intermediate `history-after-02.*` files were hash-verified only, not used as
the final behavioral result. The manifest discloses an earlier fixture attribute
mistake before the meaningful failing-before run; no independent observation of
that earlier attempt is claimed.

The behavioral executions were performed by the supplying implementation
session; this assessor inspected their raw outputs and current assertion logic,
not independently reran Chromium or the Python tests. A behavioral rerun was
not necessary for this bounded evidence disposition. Independently executed
checks here were the hashes, final-log/result equality, both changed JS syntax
checks and `git diff --check`, all successful.

## RV-001: corrected within the selected boundary

* `src/api/src/zava_forward/api/web/panels.js:263`: the shared helper slices
  each history into at most 50 rendered records, with reachable Older/Newer
  native buttons, clamped integer page input, visible live status and focus
  after paging. Both targets and challenge/resolution records use it.
* `src/api/src/zava_forward/api/web/panels.js:276`: page state is retained in
  the case hash query without replacing the other history's parameter.
  `src/api/src/zava_forward/api/web/app.js:157` separates that query from the
  decoded case ID. The final history run includes a real full reload and
  assertions that older records remain visible and both lists stay bounded.
* `src/api/src/zava_forward/api/web/panels.js:381`: the labelled native
  datalist-backed text input permits an exact reference from the entire
  authorized retained target collection, not only its current 50 suggestions.
  The exact lookup at line 388 rejects an unknown reference before dispatch.
  The final browser asserts 52 records remain after invalid entry, then opens
  CH-53 against the oldest retained target.
* `src/api/src/zava_forward/api/web/panels.js:272`: leaving a page containing
  an unsaved resolution requires confirmation. The final browser dismisses
  that dialog and checks CH-1's typed evidence survives, then submits its
  actual correction. Target paging updates only its own content/datalist,
  preserving the opening form and draft.
* `src/api/src/zava_forward/api/web/panels.js:390`: proposal and observed
  decision tokens still come from the retained form's captured target;
  resolution still submits the captured record version at line 403.
  Existing capture/restore helpers preserve actual unsaved forms and their
  closures across unrelated refreshes; route/unload warnings remain.
  Current history assertions check draft retention and exact persisted target
  equality; existing focused passing cases cover stale bindings and writer-time
  negative boundaries. No new independent wire-token capture is claimed.
* `src/api/checks/challenge_browser_check.py:175`: historical invalidation uses
  an explicit proposal challenge, 52 actual distinct retained targets and
  the original accepted decision. Lines 294-300 check the terminal correction,
  CH-53's exact target equality, byte-equivalent original recommendation/review
  data and the exact singleton stale-ID set. This is not a vacuous
  any-stale assertion: 51 other targets must remain non-stale. It is deliberately
  not evidence of historical source/policy fan-out; the existing focused tests
  separately cover those bindings.
* `src/api/checks/challenge_browser_check.py:292`: actual historical negative
  comparisons retain decisions, measure decisions, hazards, closed state and
  service requests. Lines 301-304 assert both new collections remain absent
  for all three denied roles. The original mode still executes its Digital/
  Phone, keyboard validation, draft/navigation/correction cancellation and
  denied-role journeys. Its changes are input adaptation and formatting, not
  removal of its original flow. The source delta is web/harness only; no
  authorization, manual route, hazard operation or core binding logic changed.

The missing-button pre-correction failure is consistent with the baseline
last-50 diff. The current final run exercises the formerly inaccessible older
actions through real SQLite/HTTP/Chromium, rather than merely showing history
text or mocking a successful response. RV-001's concrete cutoff is corrected;
this conclusion applies to the listed source hashes, not a future edited or
rebased candidate.

## Changed web files: bounded guidelines assessment

Full current rules were successfully fetched immediately before changed-file
assessment from
`https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`.
Applicable rules were checked against the scoped changes and relevant helpers.
Owner Fluent 2, plain ASCII, sentence-case and native-semantics requirements take
precedence over generic curly punctuation/title-case preferences.

### src/api/src/zava_forward/api/web/panels.js

Pass for the scoped change; no concrete introduced defect identified.
Native buttons, labelled input, live/focusable paging status, empty states,
bounded lists, query-state persistence and unsaved-resolution confirmation are
present. Three history plus four original-mode pinned axe 4.10.3 scoped scans
have zero violations and zero incomplete checks; inspected JSON includes
visible target dimensions at 320/390/1280px. This is not full WCAG conformance,
screen-reader validation or native datalist usability acceptance.

### src/api/src/zava_forward/api/web/app.js

Pass for the single scoped route-regex change; no concrete introduced defect
identified. Query state no longer becomes part of the case ID, while existing
route draft warnings and native navigation remain unchanged.

## RV-002 disposition and remaining blockers

Fresh-evidence availability is satisfied for this bounded assessment: permitted
raw tests, browser results and static logs are substantive, readable and
hash-bound to the current executable files. Historical excluded-log availability
is not established, and neither the original Partial verdict nor its RV-002
finding is rewritten into a historical pass.

* RV-003 remains open: other-assistant/form dependency integration and whole-
  system AC-071 are not assessed or accepted here.
* RV-004 remains open: named human/legal/RAI, resident comprehension, full
  accessibility, live/model and native-SQL-specific challenge acceptance
  remain unperformed or outside this evidence. No cloud/private data was used.
* The corrected exact-HEAD full 17-group gate has not run. The original
  candidate's gate cannot close RV-001 or cover these later source hashes.
  The coordinator additionally reports a historical project-api gate failure
  with nine TaskReleaseRecord identity errors. Its resolution is not established
  by these 19 focused tests and was not investigated in this bounded scope;
  the coordinator must reconcile it before the corrected full gate.
* Corrected commit/freeze, complete fresh receipt, required verification and
  independent exact-head/coordinator publication assessment still follow.
  This disposition authorizes no commit, source push, issue closure, full
  acceptance or replacement of an original artifact.
