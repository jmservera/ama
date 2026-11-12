---
title: Issue 96 Funding screen saved Held copy checker prospective UI plan
description: Prospective plan, written before independent critique, for a minimal read-only saved Held copy checker inside fundingDraftPanel; planning only
ms.date: 2026-11-12
---

## Status and honesty record

Prospective PLAN ONLY. No UI, README or product source is changed by this task, and none may change until the root releases the corrected backend contract. The plan is written at head `7f3386ddd` (UNAPPROVED, independent verdict Revise, M1) before any critique. The critique is run by a separate agent context, not the author. This is a continuation of the saved-check workstream: correction 1 is spent, the M1 correction (2) is in progress under backend96, and no new budget pool is requested. Refs #96 only; no closing claim, no tick.

## Objective

Specify the smallest Funding-screen control that lets a signed-in finance preparer compare a Held draft file they saved earlier with the current working review, using the served read-only freshness route, without storing the copy, showing values, auto-running, or implying approval.

## Implementation gates (all must hold before any UI code)

* G1 Root releases the corrected backend contract: an exact head SHA and tree for the frozen, independently accepted backend96 (M1 fixed), recorded by the root.
* G2 Repin: this branch is rebased or re-created from that exact head (no silent rebase; owner or root directs the method) and `origin/main` is re-fetched.
* G3 Contract diff: re-run the readiness diff of route, statuses, response keys and gating against the frozen head (checklist in details, section "Repin checklist") and amend this plan before editing if anything differs.
* G4 R-UI-1 resolved by the root before any UI code: the corrected contract must preserve numeric fidelity for a genuine unedited copy (see D4). Without it the UI cannot be released; a documented limit is not acceptable.
* G5 Fresh web-interface-guidelines fetch immediately before edits; skill list scan for relevant installed skills (none expected, public-page skills do not apply).

## Design decisions to test under critique

* D1 Placement: inside the existing `downloadEnabled && draft.draft_id` branch of `fundingDraftPanel`, directly below the download paragraph, in a labelled group. No new screen, route, nav entry, flag or role.
* D2 Controls: one native `<label>` plus `<input type="file" accept=".json,application/json">` and one native `<button type="button" class="btn alt">` "Check saved Held copy (read-only)". One press equals one POST. No drag and drop, no `autofocus`, no auto-run on choose, no hidden second request.
* D3 Client steps: file chosen; on press, refuse with inline text and no request when no file, size above 8,000,000 bytes, unreadable text, not valid JSON or not an object; otherwise POST through the existing `api(path, body)` helper (CSRF header, pending guard, 401 handling, error object). Path draft id is the panel `draft.draft_id`, encoded. The posted body is the saved object unmodified and never persisted, logged, cached or rendered.
* D4 R-UI-1 (critique CR-1): failing-first check with a genuine downloaded Held copy carrying float-valued (`12.0`) and above-2^53 field values. `api()` re-serialises parsed JSON, so such a copy can be falsely `Invalid`. Acceptable resolutions, root decision only: (a) the corrected backend compares numerically canonical values, which needs backend authority outside the carried budget and is therefore a root request; (b) an explicit root-recorded exception allowing one panel-local raw-text POST that sends `X-ZF-CSRF: 1`, `Content-Type: application/json` and maps errors through the same status table; it is not a shared helper change but it does bypass `api()` 401 and pending handling, so it must re-implement the 401 sign-in return and the pending guard and is tested for both. Rejected: documenting false `Invalid` as a limit, and weakening the digest. If the root selects neither, the task stays blocked.
* D5 Status region and the shared wrapper (CR-5): `h()` wraps `onclick` in `AsyncAction.handler`, which already sets native `disabled`, `aria-busy` and the progress notice while the returned promise runs, and restores them in its own `finally`. The panel therefore returns the promise from its click handler and sets no `disabled` or `aria-busy` itself. One status `<div role="status" aria-live="polite" aria-atomic="true">` is created with the panel; its text is replaced, the element is not. Text "Checking the saved copy…" is set on press.
* D6 Focus: no focus move on result and no `autofocus`. Whether the wrapper's `disabled` makes the browser drop focus is tested first, not assumed. Only if the test shows focus fell to `body`, and only after the wrapper has re-enabled the button (a macrotask after the handler promise settles, because restoring inside the handler would run while the button is still disabled), refocus the button if it is connected and `document.activeElement` is still `body`. Focus the person moved elsewhere is never taken; a body focus alone cannot prove that, so the test covers keyboard activation, deliberate focus movement during the check, and completion. Validation errors use `aria-invalid="true"` on the input with a linked `.field-error` text, no automatic focus move; the status region announces them.
* D7 Result mapping (statuses and keys as at the candidate; re-verify at G3):
  * `Current`: "Current. The details checked in this file match the working review now. The check compares information the file itself supplies, so it does not show that the whole file is genuine or who made it. It is still Held and unreviewed. This is not an approval, review, eligibility result or submission." (CR-2: never "the saved copy matches".)
  * `Stale`: list `stale_fields` and `unaffected_fields` (when the array is present) as field names, then the server `reasons` and `action` as plain text via `textContent`. Next: re-review the named fields and download a new Held copy; a person decides.
  * `Invalid`: "Invalid. This file is incomplete or was changed after download. Next action: download a new Held copy." Names no fields. Does not claim wrongdoing.
  * `Unavailable`: "Unavailable. The working review for this file is missing or belongs to another home. Owner: document owner. Next action: ask them to recover the evidence." Names no fields.
  * Unknown `status` or malformed body: treat as failure (D8), never as Current.
* D8 Failure handling after M1 (exact, re-verify at G3). Map locally by `e.status`, because `api()` stays unchanged:
  * 400 (CR-3): "Choose the saved Held file for this draft (held-form-draft-export.json). Next action: pick the file you downloaded for this draft." Covers the draft id mismatch and the empty body (an empty body becomes `{}` and reaches the mismatch 400), `Could not read that.`, and any other `ValueError` text; the UI shows its own sentence for every 400 and does not echo server text.
  * 401: shared handler already returns the person to sign in; the panel adds no message.
  * 403 (any of: trusted-proxy without CSRF header, administrator view-only, role projection, or another dispatcher cause): "Your role cannot run this check. Owner: the Retrofit Programme Manager. Next action: ask them, or compare the version and hash in the file by hand."
  * 404 (switch off, trusted-proxy, or unknown case or form source): "This check is not available here. Next action: compare the version and hash in the file by hand." The UI does not promise the control disappears; it disappears on reload only when the view no longer reports `held_download_enabled`.
  * 409: "The form or source changed. Next action: reload the page, then check again."
  * 502: "The document store is unavailable. Nothing was approved or submitted. Next action: reload and try again."
  * 503 after M1 and any other 5xx or network error: "The check could not run, so nothing is judged about your file. Nothing was approved or submitted. Owner: application support. Next action: reload and try once more, then contact application support." Never shown as Invalid, Stale or Current.
  * `e.generic` true (HTTP error without server text): use the read-only wording above, not `GENERIC_CHANGE_ERROR`. `e.generic` exists only for parsed HTTP errors (CR-7); a network failure, an unparseable response (api() rethrows the JSON error for a keyed POST) and an abort have no status and fall to the 503 wording, except an abort or obsolete response, which is ignored silently.
* D9 Copy and content: plain ASCII, no em dashes, plain terms (no digest, hash only where already used by the existing link text), names actor and next action. Existing panel text ("Not submitted; eligibility Not assessed", "may be newer than input version") stays byte-exact so the existing browser check still passes.
* D10 Browser check (CR-8): extend `held_form_download_browser_check.py`. The request listener is attached before navigation and before the reload so load is observed; the writes assertion allows only `POST` to the exact path `/api/cases/ZF-1/form-review/{draft_id}/held-export/freshness`, counted per action (zero on load and on choose, exactly one per press), and any other non-safe request still fails. Existing text and download assertions are retained.
* D11 Lifecycle (CR-6, CR-7): changing the selected file clears the previous result and any error; a response is applied only if the panel is still connected and the file selection is the one that was sent, otherwise ignored; whole-page re-render builds a fresh empty status region, so no old result survives a re-render. A local in-flight flag blocks a second press before the asynchronous file read, because the shared pending key is built from the path and selected body fields and does not cover that read. The 8,000,000 byte limit applies to the file size and to the serialised request bytes. `accept` is a picker hint only; content is validated after reading.

## Phases

* [ ] Phase 0 (gated): root releases the corrected backend contract; repin; contract diff; G4 decision; amend this plan. No UI source edit before this.
* [ ] Phase 1: failing-first browser check additions (stale result cleared on file change; obsolete response ignored; second press during read; label and keyboard path; Current; Stale after a real review bump; Invalid on an edited copy; Invalid never shown for an injected 503; wrong-draft 400; float and large-integer copy per G4; denied roles and switch-OFF show no control; 404 after switch flip; 360px reflow; no POST on load or on choose).
* [ ] Phase 2: implement D1 to D9 in `fundingDraftPanel` only (plus one panel-local function if needed).
* [ ] Phase 3: focused verification: extended browser check, API `test_form_held_download_api`, `test_role_endpoint_inventory`, ruff and mypy on changed Python, `node --check` of changed JS, `git diff --check`, README diff review. Not a full gate; no axe, no assistive-technology acceptance claimed.
* [ ] Phase 4: `src/api/README.md` Held download section: one short paragraph on the control; `docs/reference/log.md` entry; no index change expected.
* [ ] Phase 5: independent final Review in a separate agent context of the exact head; record outcome; no repeat.

## Validation tier

Owner demo focused tier (small, non-gate, synthetic demo UI): targeted local checks plus hosted CI read for the exact head. Classification and basis are recorded in details. No change to permissions, workflows, dependencies, Dockerfiles, deployment or security controls is planned; if any appears, the tier is re-classified to the strictest applicable.

## Boundaries

Local only: no push, PR, merge, issue, acceptance tick, human, Finance, legal or accessibility approval, cloud, private data, production, spend, shared cleanup or publication. The setup uses pip only, no uv, no source-package `PYTHONPATH` (test-helper directories allowed). Dependent-only invalidation criteria C1, C5 and C6 remain unproven and unticked.
