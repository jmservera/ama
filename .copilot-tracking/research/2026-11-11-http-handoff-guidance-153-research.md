---
title: Issue 153 pending-handoff HTTP refusal and error guidance research
ms.date: 2026-11-11
task_id: 153-http-handoff-1111
---

## Status

Original dated research, recorded 2026-11-11 on branch `fix/demo-handoff-http-guidance-153-1111` at main `7880b95b19525ff465cab27870ba9d55b57110a3`. Research and plan only. No source, test, runtime check, Review or publication has occurred.

## Scope

One initial, not-yet-implemented increment for criterion C3 of #153 ("Error and blocked messages state the reason, owner and next action"): the HTTP-response branch of `pendingHandoffs()` in `src/api/src/zava_forward/api/web/app.js`. It is not a retry of the transport-only guidance delivered by #1367 and merged to main through #1376 (`65c2ab9d9`, 2026-11-10). That slice explicitly left HTTP and malformed-200 paths outside its scope.

## Sources read

* Live #153 body and all ten comments (2026-10-15 to 2026-11-11): C1 ticked; C2, C3 and C5 unticked. Closure audit (2026-10-31) says C3 lacks "generic/raw API errors, technical refusals and Unknown/Unassigned regulatory ownership". The 2026-11-10 and 2026-11-11 comments record the #1367/#1376 lineage and that malformed-200 and broader HTTP residuals remain outside that increment.
* Both case studies (original and addendum), `docs/reference/README.md` index, `docs/reference/memory.md`, `docs/reference/research/ux/content-standard.md` (blocked and error messages: reason, owner as a role, one verb-led next action; generic error recovery must distinguish a failed read from an uncertain write; "adding a generic role name to every raw error would not establish real accountability").
* The prior slice records `.copilot-tracking/{research,plans,details,changes,reviews}/2026-11-10-handoff-read-guidance-153-*` and its state file (Review routed R1: non-JSON 200 reads as empty).
* Current Web Interface Guidelines, fetched 2026-11-11 from `vercel-labs/web-interface-guidelines/main/command.md`, complete. Rules relevant here: "Error messages include fix/next step, not just problem"; "Async updates need `aria-live`" (existing `role="alert"` is an implicit assertive live region); "Handle empty states"; semantic HTML before ARIA; active voice, second person; ASCII `...` is the repository convention over `…` (content standard, so the typography rule is a recorded owner-standard exception, not new work).
* Read-only inspection of the #83 worktree (`/home/azureuser/source/ama-demo-wt/issue-83-waiting-view-1111`, head `dd3c32910c3c5205a2cbedbe74608411c6f9f341`) and public PR #1444 description. No file there was changed.

## Source facts (base `7880b95b1`)

`api(path)` for a GET (`app.js:56-87`):

* `fetchReadRetrying` retries only non-JSON 5xx (502/503/504/500 without a JSON content type) as an existing cold-start measure, never a network rejection. JSON 4xx/5xx responses are returned at once. This increment does not touch it.
* A body that is not JSON becomes `{}` for reads (`res.json().catch`).
* 401 on a non-login path clears `me`, calls `login("Your session has ended. Sign in again.")` and throws an error with `status` 401.
* Any other non-OK response throws `Error(data.error || GENERIC_READ_ERROR)` with `status`, `generic`, `reasons`, `outcome`, `errors`. A rejected fetch propagates the browser error with no `status`. Abort propagates `AbortError`.

`GET /api/handoffs` server behaviour (`server.py`):

* Unauthenticated: 401 `Please sign in.`
* `projection.allowed(user, "handoffs")` false: 403 `Your role does not include this.` Every staff role is in `STAFF_GET` with `handoffs`; Contractor is not and does not get the staff work list. A 403 is therefore a refusal state reachable by role-matrix drift or a misconfigured account, not by an ordinary staff login. The served browser case must construct it.
* `pending_handoffs` raises `PermissionError` for non-staff, which `do_GET` does not catch for this route, so it would surface as the generic 500 JSON `The service hit an unexpected error...`. Treated as a 5xx here; not changed.
* Success: always a JSON array.

`pendingHandoffs()` (`app.js:753-774`) today: constant `HANDOFF_READ_ERROR` (reason, owner "application support", next action refresh) for errors with no `status`; `Could not load handoffs: ${e.message}` for any error with a `status`, so a 403 shows server text `Your role does not include this.` (no owner, no next action) and a 500 shows server text; a 200 with a non-array body (for example `{}` from non-JSON) makes `!rows.length` true and the card is hidden as if the queue were empty. Abort already returns silently before painting (preserved).

Existing roles usable as owners (`app.js:478`, `role-screens.js:4`, `projection.STAFF_ROLES`): Retrofit Programme Manager, Programme Support Officer. Existing support owner string: "application support" (`GENERIC_READ_ERROR`, `HANDOFF_READ_ERROR`). #83's new screen uses fixed copy "Owner: a programme owner" for its own 403; no named person or access approval exists in the repository for this.

## Smallest supported states

| State | Detection from the `api()` contract | Needed copy |
| --- | --- | --- |
| Abort | `e.name === "AbortError"` | Existing: return, paint nothing (keep) |
| Session ended | `e.status === 401` | Existing: sign-in screen replaces the view (keep text and path) |
| Permission refusal | `e.status === 403` | NEW fixed refusal copy, no retry advice, queue unknown |
| Server or other HTTP failure | any other truthy `e.status` (400, 404, 429, 5xx, generic) | NEW: reuse fixed load-failure copy, no server text, queue unknown |
| Transport or non-HTTP failure | no `e.status` | Existing `HANDOFF_READ_ERROR` (unchanged) |
| Malformed 200 | resolved value is not an array | NEW: same load-failure copy, card visible, not hidden as empty |
| Empty array | `[]` | Existing: hide card (keep) |
| Rows | non-empty array | Existing list and both download links (keep) |

Reusing the existing `HANDOFF_READ_ERROR` for every non-403 failure keeps the delivered transport tests valid and adds exactly one new string. A separate string per HTTP code would add copy the user cannot act on differently.

## Historical provenance

* `git log -S"Could not load handoffs" -- src`: `a2253a7c7` (#311) introduced the raw HTTP message; `65c2ab9d9` (#1376, containing #1367) added the transport guidance. No earlier failed, reviewed or candidate change for the HTTP branch exists in repository history or local branches.
* Historical #153 correction balance: UNKNOWN (not recovered). The prior slice had its own original Review, one independent CI-driven type correction and recorded R1-R4 residuals; those are preserved and are not an allowance for this task. This is one INITIAL unimplemented increment: no post-Review source correction batch, no new default five, no transfer from #83, #131, #132 or #134 is authorized or assumed.
* No named human wording review exists. Appointment of the reviewer (2026-10-15) is not review of this text; C5 and universal C2/C3 stay unproved. Refs only.

## Dependency and conflict analysis (#1444 / #83)

* #83 edits `route()` (status text and a route), adds `handoffWaitingView` and constants after `workSteps` (~line 800), adds a header link in `listView`, `src/api/README.md` and a new test file. It does not touch `pendingHandoffs` or `HANDOFF_READ_ERROR`; its hunks are 25+ lines away. Textual conflict risk with this plan: low. Semantic risk: both depend on `api()` and share the owner-wording vocabulary; this plan must not alter the `/api/handoffs/unaccepted` path, the new header link, nor `workSteps`.
* Both existing slice-extraction tests (`test_handoff_read_guidance`, `test_unaccepted_handoff_download_ui`) cut the source from `const HANDOFF_READ_ERROR` to `let briefingBox`. A new constant must be placed after that marker and before `function pendingHandoffs` so both extractions keep working, and #83 lines (after `workSteps`) must not fall inside the slice. They sit after `let briefingBox`, so they are outside.
* Resume point: implementation is blocked until the coordinator confirms #1444 merged, then adopt `origin/main` into this branch by ordinary merge (no rebase, no history rewrite), re-run the slice-marker check and the #83 regressions.

## Risks recorded

* A 403 can look like a transient fault and invite repeated refresh. The "mine" list filters by `owner_code` (`store.py:358`), so it may not show a handoff addressed to the user; fallback copy must not imply it shows every waiting handoff. Copy must say refreshing will not change the result and avoid retry advice.
* Genuine failure must never read as empty: card stays visible, text says "we cannot tell whether any are waiting".
* The 500 JSON body carries service-authored text. It is a server string, not user data, but it is "raw server text" under this brief and is not shown.
* The `fetchReadRetrying` cold-start retry for non-JSON 5xx pre-exists and is not changed or extended; tests must not claim "no retry" for that path beyond the card code itself.
* Role vocabulary differs between #83 ("a programme owner") and the existing role names. Plan uses the existing role names because the content standard requires "a named person or role", and records the difference for review rather than asserting an access process.

## Disposition

Research disposition: executed. Planning Readiness: Ready, conditional on the #1444 dependency for implementation, not for planning.
