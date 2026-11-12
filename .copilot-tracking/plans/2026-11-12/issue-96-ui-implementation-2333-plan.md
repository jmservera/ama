---
title: Issue 96 Funding screen saved Held copy checker UI implementation plan amendment
description: Amendment of the critiqued UI plan after repin to the released backend, G3 contract re-verification and the root G4 decision; written before re-critique and before any product edit
ms.date: 2026-11-12
---

## Status and identities

* Task `issue-96-ui-implementation-2333`, parent `issue-96-ui-plan-2323` (originals `cc5c9894d`, `7f7a31ce6` on this branch, cherry-picked with `-x` from `b8702f97b` and `ffc8b541f`; the originals stay untouched).
* Branch `feat/demo-96-ui-implementation-2333`, created from the root-released backend head `94760af7d274e1dc1d9ec8c37d76df85cbd46c28`, tree `46eb72d5249ce4d2bc3b40ef9afb3c5b5871feac` (verified by `git rev-parse`). Root closure evidence: `96-independent-m1-closure-2332.json` (bounded local M1 closure, 16 canonical API tests). Merge base with `origin/main` (`8e6e55457`) is `eac1206c6`; main has moved and is not merged (local freeze only).
* Budget: saved-check correction 1 and M1 correction 2 spent, no new pool. This is an admitted UI implementation, not a backend correction. Refs #96 only; no closing claim, tick, push, PR or publication.

## Gate disposition

* G1 met: exact head and tree released by the root. G2 met: new child branch from that head, only the two UI planning commits cherry-picked.
* G3 contract diff re-run on 2026-11-12 by reading `server.py` `_forms`, `do_POST`, `_body`, `held_download_enabled`, `saved_export_ids_are_text` and core `export_freshness`, and by running the canonical suite (`test_form_held_download_api.py`, 16 tests OK, fresh `ZF_DATA`, isolated pip venv). Diff `7f3386ddd..94760af7d` in `src/` changes only `server.py` (new `saved_export_ids_are_text`, broad `TypeError` fallback removed) plus tests and README. Result: route, method, statuses, response keys, gating, 8,000,000 byte cap, shared parser and `Current`/digest wording are unchanged from the plan. The route validates caller field id types (not a total comparator); an escaping internal `TypeError` reaches the shared logged 503. Core still maps its own digest and row-parsing faults to 200 `Invalid` (frozen). Forged mixed-type ids answer 200 `Invalid`. The plan D7 and D8 tables stand without change.
* G4 decided by the root: a narrowly authorised PANEL-LOCAL RAW JSON TEXT transport. No shared `api()`, `app.js` or backend change. Purpose: preserve `12.0` and integers above 2^53 from the downloaded file, which `JSON.stringify` would otherwise rewrite and falsely report `Invalid`.
* G5 met: web interface guidelines fetched on 2026-11-12 (`command.md`); skill list scanned, no public-page skill applies (this is a dashboard control).

## Amended decision D4 (supersedes the open D4 options)

* One new panel-local function `fundingCheckSavedCopy` directly above `fundingDraftPanel`. It reads the chosen file with `file.text()`, validates locally only that the text is within 8,000,000 UTF-8 bytes and parses (parse result discarded) to a JSON object, then POSTs the ORIGINAL TEXT unchanged as the body with `Content-Type: application/json` and `X-ZF-CSRF: 1` to the same path, same origin, default credentials, `routeController.signal`.
* It reuses, not re-creates, the existing safeguards: the CSRF header and same-origin fetch; session 401 handling identical to `api()` (`me = null; login("Your session has ended. Sign in again.")`, no panel message); the route abort signal (an abort or a response for a replaced file or disconnected panel is ignored silently); the existing `pendingMutations` set (key built with the existing `mutationKey` from the path, so a second press, including during the file read, is refused with no second request); and the `h()`/`AsyncAction.handler` wrapper for disabled, `aria-busy` and progress feedback. No second error system: the status table of D8 is the only mapping.
* Failures surface as readable check-failed text in the panel status region and never as `Invalid`, `Stale` or `Current`; they never imply that anything was written, approved or submitted.
* The posted text is never stored, logged, cached or rendered.

## Carried unchanged

D1 to D3, D5 to D11 of the critiqued plan stand, with these precisions: D3 posts raw text instead of calling `api(path, body)`; D5 the wrapper owns `disabled` and `aria-busy`, the panel returns the promise; D8 mapping is by `res.status` of the raw response (non-JSON error bodies fall to the status text, an unparseable 200 is a failure); D10 the browser check attaches its request listener before navigation and counts exactly one freshness POST per press and none on load or on choose. Default OFF, operator attestation, role gating, human and manual-path boundaries are unchanged. Current means only that the details checked in the supplied file match the working review now, judged on metadata the file supplies; it is not authenticity.

## Numeric fidelity test (required, failing first)

The browser check uses real downloaded synthetic copies: (a) a number field `area` corrected to the float `12.0`, (b) the same field corrected to the integer `9007199254740993`. Each copy is downloaded through the real link, saved by Playwright, chosen in the file input and checked. Expected: `Current`. A control check posts the same downloaded copy re-serialised in the page with `JSON.stringify` and expects `Invalid`, proving the fidelity test would fail with the shared helper. The failing-first run happens before the raw-text transport exists (control absent or using `api()`), and the result is recorded.

## Scope of edits (owned paths)

* `src/api/src/zava_forward/api/web/role-screens.js`: `fundingDraftPanel` and one panel-local function above it only (about L1340 onward). Not touched: the programme, `screenTable` and top-of-file regions owned by the 233 work, `app.js`, `async-action.js`, `style.css`.
* `src/api/checks/held_form_download_browser_check.py`: extended, existing assertions retained except the writes assertion, narrowed to the exact freshness path counted per action.
* `src/api/README.md`: one short paragraph. No `docs/reference/log.md`, index or `style.css` edit (existing classes only; no knowledge-base file changes).

## Phases

* [ ] Phase 1: failing-first browser additions (matrix in the parent details plus the numeric fidelity cases) and a focused unit check of the 16 canonical API tests.
* [ ] Phase 2: implement `fundingCheckSavedCopy` and panel changes.
* [ ] Phase 3: focused verification: extended browser check, 16 API tests, `test_role_endpoint_inventory`, pinned ruff and mypy on changed Python, `node --check`, `git diff --check`, pinned axe check if the repository already has one for this screen, README diff review. No full gate.
* [ ] Phase 4: README paragraph.
* [ ] Phase 5: one independent read-only Review of the exact head; record outcome; no repeat.

## Validation tier

Focused tier (small synthetic-demo UI, no workflow, dependency, Dockerfile, permission, secret, deployment, SQL or security-control change; the server contract is unchanged and read-only). Raw-text transport adds no new server surface. Independent exact-head review, human approvals and hosted CI remain required and are not claimed. The eventual publication is the same #96 backend plus UI candidate, not a separate unrelated PR. Local freeze only.

## Amendments after independent re-critique (PC-1 to PC-6, applied directly, none rejected)

Critique: [issue-96-ui-implementation-2333-critique.md](issue-96-ui-implementation-2333-critique.md). Executed once, verdict Revise, not repeated.

* PC-1: the pending guard uses `mutationKey(path, {})`, acquired before the file read and released in `finally` only when this call acquired it; a second press while held makes no request; tests cover retry after failure and after abort.
* PC-2: the route signal and session identity are captured at press, before the read; abort, panel connection and file selection are rechecked immediately before the POST and after the response; navigation during the read sends nothing.
* PC-3: the fixture stages an `area` candidate from a source span in the uploaded text (`12.0` at its offsets), corrects it through the real review API to the float `12.0`, downloads and checks; then stages a second `area` candidate for `9007199254740993`, corrects, downloads and checks. No mocking.
* PC-4: a 401 for the still-current session is handled (sign-in return) before obsolete-selection filtering; an old session's response never replaces a newer login; tested.
* PC-5: `file.size` over 8,000,000 is refused before reading; the text is read with a fatal UTF-8 decoder (malformed bytes refused with the plain "could not read that file" sentence); the encoded request size is checked too; boundary and malformed-byte cases tested.
* PC-6: log, index and CSS edits removed from scope (above).
