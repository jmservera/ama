---
title: Issue 96 Funding screen saved Held copy checker prospective UI details
description: Phase details, repin checklist, test matrix and resume conditions for the prospective saved Held copy checker UI plan; planning only
ms.date: 2026-11-12
---

## Scope of the later change (owned paths, none edited now)

* `src/api/src/zava_forward/api/web/role-screens.js`: `fundingDraftPanel` only (L1346 to L1366 at head `7f3386ddd`) plus at most one new panel-local function immediately above it. Not owned: the top-of-file shared helpers (L1 to L25), `screenTable` and programme regions near L300 owned by the 233 programme work, and everything in `app.js`.
* `src/api/checks/held_form_download_browser_check.py`: extend; narrow the L192 write assertion.
* `src/api/README.md`: one paragraph in the Held download section; `docs/reference/log.md`: one appended entry.
* `style.css`: only if an existing class cannot express a state (expected none).

## Repin checklist (G3), run against the frozen corrected head

1. Record head SHA, tree, merge base and `origin/main`; confirm independent acceptance reference from the root.
2. Route and method unchanged: `POST /api/cases/{case_id}/form-review/{draft_id}/held-export/freshness`.
3. Status table re-verified by reading `server.py` `_forms`, the dispatcher and `do_POST`, not by memory: 200 results; 400 (unreadable body, empty body reaching the draft id mismatch, mismatch, other `ValueError` texts); 401; 403 (trusted-proxy no CSRF, view-only, role projection, other dispatcher causes); 404 (switches or provider, unknown case or source); 409; 502; and the catch-all 503 text `Form storage failed. Reload before retrying; no approval or submission occurred.`
4. M1 closure confirmed by test (CR-4): core itself catches `TypeError` around the digest and saved-input processing, so also inject an internal failure inside that block, not only in `draft_export`; each injected internal failure reaches 503, not 200 Invalid; a forged mixed-type field id gives 200 Invalid. If the corrector chose route-level validation instead of a total comparator, record which.
5. Response keys: `status`, `stale_fields`, `unaffected_fields` (Current and Stale only), `reasons`, `action`, `reviewed`; Invalid and Unavailable omit `unaffected_fields` and the draft id.
6. Gating unchanged: shared with the download switch, no own flag, trusted-proxy never served; `held_download_enabled: true` in the form-review view.
7. Body cap and the shared parser behaviour unchanged (8,000,000 bytes).
8. How the digest treats floats and large integers (R-UI-1).
9. README wording for Current and digest still says comparison against client-supplied data only.
Any difference means amend the plan and re-critique the changed part before editing.

## Phase 1 test matrix (browser check, real Chromium, fictional data)

| Case | Expected |
| --- | --- |
| Load Funding screen, switch ON, allowed role | Control present, one file input with visible label, one button; no freshness request; no non-safe request on load |
| Choose file only | No request (no auto-run) |
| Press with no file | Inline error, input `aria-invalid`, no request, focus unmoved |
| Keyboard path | Tab to input, Tab to button, Enter or Space runs one POST |
| Genuine saved copy | `Current` text with the not-approval sentence; no values shown; no storage writes (`localStorage` and `sessionStorage` unchanged) |
| After a real review bump (open, review) | `Stale` with field names and next action |
| Edited copy (body changed, digest not) | `Invalid`, no field names |
| Another draft's file | 400 mapping text |
| Injected 503 or network error (route interception in the page, test only) | "The check could not run" text; no Invalid, Stale or Current word in the result |
| 404 (switch flipped OFF) | not-available text; control absent after reload |
| Denied roles (support, grants) and switch OFF | no control, no input |
| Float-valued and above-2^53 field in a genuinely downloaded copy | per G4 decision; must not report Invalid for an unedited copy |
| Change file after a result, or while pending | previous result cleared; obsolete response ignored |
| Second press during the file read | exactly one POST |
| Focus matrix | keyboard activation, deliberate focus move during the check, completion; no refocus of a moved focus |
| Network failure, unparseable 200 or 5xx body | "could not run" text, never a result word |
| Focus | After result the status region is announced and `document.activeElement` is unchanged, or the button if the browser dropped focus on `disabled` |
| 360px and 200% text | no horizontal overflow of the control |
| Result text rendered with `textContent` | a field id such as `<b>x</b>` in a forged copy shows as text |

## Ownership note

`AsyncAction.handler` (via `h()`) owns disabled, `aria-busy` and progress for `onclick`; the plan uses it unchanged and adds nothing to `async-action.js` or `app.js`.

## Validation tier classification

Focused tier: small, non-gate, synthetic-demo UI plus its browser check and a README paragraph. Basis: no workflow, gate tool, dependency manifest, Dockerfile, permission, secret, deployment, SQL or security-control change is planned, and the server contract is read-only and unchanged. If the root selects an R-UI-1 option that changes the backend contract or digest, the whole change is re-classified (backend and security-sensitive input handling take the full tier). Independent exact-head review, human approvals and hosted CI remain required; none is claimed here.

## Resume and repin conditions (the exact handover)

Resume implementation only when all hold:

1. The root records the corrected frozen backend head SHA and tree and that it is independently accepted (not just verified by its author).
2. The root directs the repin method for `research/demo-96-ui-plan-2323` (or authorises a new branch) and confirms the budget statement: saved-check correction 1 spent, M1 correction 2 closed or in a stated state, no new pool, and that a UI implementation task is separately authorised.
3. G3 contract diff is run, any difference is amended and critiqued, and G4 is decided.
4. `git status` is clean at the pinned head, the web-guidelines source is freshly fetched, and the 233 programme work's current touch of `role-screens.js` is checked for line drift before the first edit.

## Evidence and disclosure

* No test, server, browser or probe ran against repository code in this stage. The only probes were two throwaway interpreter one-liners (JSON round trip) and read-only greps.
* The candidate head is unapproved; every contract statement is conditional on G3.
* Independent critique: see the critique file. Author-only reading is not independent evidence.
