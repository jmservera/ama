---
title: Issue 96 Funding screen saved Held copy checker prospective UI research
description: Prospective research for a minimal Funding-screen control that calls the served saved Held export freshness check; planning only, no implementation
ms.date: 2026-11-12
---

## Identities and scope

* Worktree `issue-96-ui-plan-2323`, branch `research/demo-96-ui-plan-2323`, head `7f3386ddd0054f557fd0d092de0625cdd58ebe49` (tree `98b03f799f2e53eab8d26c5a63df9f1dba880870`), clean at start. `origin/main` at fetch is `e4854bd7e09488e9b76c4008d4e23ac821f63d29`; the pinned head's merge base is `eac1206c6`, so main has moved and the later repin must also re-check the base.
* Task id and slug `issue-96-ui-plan-2323`. Refs #96 only. This is prospective PLANNING evidence. No UI, README or product source is edited, and none may be until the root releases the corrected backend contract.
* Candidate head `7f3386ddd` is UNAPPROVED. The independent assessment at that head found verdict Revise with finding M1 (a broad `TypeError` to `Invalid` fallback masks internal failures). Backend96 M1 corrector is running. This plan is written against the candidate contract and names every point that must be re-read after the corrected head freezes.
* Budget carried unchanged: saved-check correction 1 is spent, the M1 correction (correction 2) is in progress under backend96, and this task adds no new pool. The UI plan does not request one.

## Evidence read

* Both coordinator results: `rpi-96-ui-readiness-2255-result.json` (read-only readiness, verdict ready to specify, blocked for implementation) and `rpi-96-independent-2307-result.json` (independent exact-head assessment, Revise, M1 Medium, L1 to L4).
* Mandatory project reads: `docs/case_study_48_original.md` (full) and the addendum purpose and status section (158 KB, not read end to end), `docs/reference/memory.md` (opening), the `docs/reference/README.md` index (targeted greps; large), `docs/reference/research/ux/design-system.md` (decision, layout rules, component inventory), `wcag-conformance-baseline.md` (decision and scope) and `content-standard.md` (standard and blocked and error messages).
* Component reads: `src/api/README.md` Held download and saved freshness sections (L1180 to L1225); core `form_export.py` `export_freshness` and `_digest`; `server.py` `held_download_enabled`, `_forms` (L1196 to L1243) and the POST dispatcher (L1320 to L1335); `role-screens.js` L1 to L25 helpers and L1335 to L1405 (`fundingDraftPanel`, `finance-funding`); `app.js` `mutationKey`, `GENERIC_*` errors and `api()` (L46 to L90); `checks/held_form_download_browser_check.py` (262 lines, structure and the authorised story).
* Not read end to end: the `src/core`, `src/agents`, `src/orchestrator` and `src/importer` READMEs (this slice touches only `src/api`; core is read at source for the one function it consumes). Disclosed, not claimed.
* Web guidelines: the current `vercel-labs/web-interface-guidelines` `command.md` was fetched successfully on 2026-11-12 and shaped the plan. No UI file changed, so no `file:line` review of changed files exists. A fresh fetch and review of the changed files is a required implementation step.

## Served interface at the candidate (to re-verify after M1)

* Route: `POST /api/cases/{case_id}/form-review/{draft_id}/held-export/freshness`. Body: the saved `held-form-draft-export.json` object, whose `draft_id` equals the path draft id. Body cap 8,000,000 bytes in the shared parser.
* Statuses at the candidate (exact, from `server.py` `_forms`, the dispatcher and the README precedence line):
  * 200 with `Current`, `Stale`, `Invalid` or `Unavailable`; `Cache-Control: private, no-store`; `reviewed` always `false`; no field values. `Invalid` and `Unavailable` omit `unaffected_fields` and the draft id; the UI must not assume either key.
  * 400 `Could not read that.` for an unreadable, empty or non-object body (shared parser, before routing); 400 `Supply the saved Held export of this working review.` for a non-object body or draft id mismatch inside the route.
  * 401 session ended (shared `api()` already sends the person to sign in). 403 for a trusted-proxy request without `X-ZF-CSRF`, for administrator view-only, and for role projection (`PermissionError`).
  * 404 `Not found.` when the operator switches are off or the provider is `trusted-proxy`; also 404 `Form source or case not found.` for an unknown case (`KeyError`).
  * 409 conflict `The form or source changed. Reload before retrying.`; 502 document store unavailable.
  * 503 `Form storage failed. Reload before retrying; no approval or submission occurred.` is the shared catch-all for any other exception, logged by type only.
* Gating: `held_download_enabled()` needs `ZF_FORM_HELD_DOWNLOAD=synthetic-demo-only` and `ZF_DEPLOYMENT_PROFILE=demo` and a provider that is not `trusted-proxy`. Default OFF. The Funding screen learns of it only from `held_download_enabled: true` in the form-review view; the freshness route shares that switch and has no flag of its own.

## Effect of M1 on UI failure handling

* At the candidate, a genuine internal `TypeError` is answered 200 `Invalid` with the user-blaming text "incomplete or was edited" (M1). A UI built on the candidate would repeat that falsehood.
* After the M1 correction, either path in the independent routing is acceptable: the comparator becomes total (forged mixed-type field ids give the existing 200 `Invalid`) and the route `except TypeError` is deleted, or the route validates field id types and does not catch `TypeError`. In both cases an internal defect reaches the shared handler and answers 503 `Form storage failed. Reload before retrying; no approval or submission occurred.` The UI contract after M1 is therefore: 200 `Invalid` means only a copy problem (re-download a Held copy); 503 means the check could not run, the copy is not judged, nothing was approved or submitted, and the next action is to reload and retry once and then contact application support. The UI must never present a 503, 502, 409 or network failure as `Invalid`, `Stale` or `Current`.
* The shared `api()` returns the server `error` text when present and otherwise `GENERIC_CHANGE_ERROR` ("We cannot show whether this change was saved ... check the recorded history"), which is wrong for a read-only check. The plan keeps `api()` unchanged and maps `e.status` and `e.generic` locally with read-only wording.

## Design finding R-UI-1: client re-serialisation can falsify Invalid (needs a root decision)

* `api(path, body)` calls `JSON.stringify(body)`. The digest is computed in core from `json.dumps(body, sort_keys=True, separators=(",", ":"), allow_nan=False)`.
* Probe on 2026-11-12 (throwaway, no repository change): `JSON.parse('{"v":12.0}')` then `JSON.stringify` yields `{"v":12}`, and a parsed integer above 2^53 loses precision (`9007199254740993` becomes `9007199254740992`). Python then reads `12` as an int and `_digest` yields `12` not `12.0`, so a genuine, unedited saved copy that carries a float-valued field would answer `Invalid` and tell staff to regenerate.
* The candidate tests use string values only, so this is not covered. Options, in order of preference, all needing root release because the first touches the contract and the second sits at the helper boundary:
  1. Backend corrected contract states how the digest copes (for example canonical comparison on parsed numbers). Preferred, but backend96 has no budget for it, so only if the M1 corrector already covers it.
  2. The control posts the raw file text with `X-ZF-CSRF: 1` and `Content-Type: application/json` through one panel-local call that reproduces only the status mapping, not a second error system. It is not a shared helper change and keeps CSRF, but duplicates the fetch step of `api()`, including 401 handling.
  3. Accept the limit: refuse locally any copy whose text, when parsed and re-serialised, differs numerically (a cheap equality test on the text of numbers is not reliable), or document that float-valued fields can be reported `Invalid`. Weakest; truthful but unhelpful.
* Default recommendation: implement a failing-first check with a float-valued and a 2^53 field in the Held copy, so the facts decide. The implementation phase must not start on this choice without root direction.

## Existing UI owner and disjointness

* `role-screens.js` is a single large file. This task owns only `fundingDraftPanel` (L1346 to L1366 at the pinned head, "near 1340 plus") and, if needed, one new small panel-local function directly above it. The programme work item (233) owns the programme and `screenTable` regions near the top and around L300. The two sets of lines are disjoint; a rebase conflict is possible only through file-level line drift. No shared helper (`screenPanel`, `screenFields`, `screenValue`, `screenTable`, `h`, `api`, `app.js`) changes, and `style.css` changes only if existing classes (`.btn`, `.alt`, `.field-error`, `.status-line`, `.empty`, `.row`) cannot express a state, which is expected to be unnecessary.
* The browser check `src/api/checks/held_form_download_browser_check.py` is extended, not replaced. Its `no non-GET/HEAD/OPTIONS page requests` assertion at L192 must be narrowed so that no write occurs on load and exactly one freshness POST occurs per press.

## Guards the control must keep

* Switch OFF by default: the control exists only inside the same `downloadEnabled && draft.draft_id` branch as the download link. Hiding is convenience; the server stays authoritative (404/403).
* Role: Finance view plus resident view plus reason view are enforced per request by `forms._actor`; the UI adds no authority and does not infer permission from hiding.
* Manual path: staff can still re-download the Held copy and compare version and hash by eye, or ask the document owner or Retrofit Programme Manager to re-review. The panel keeps stating this.
* Consent and approval: human decisions are untouched. Nothing here records, approves, submits, assesses eligibility, marks reviewed, or changes any record.

## Wording boundaries (carry into every state)

* Current means only: the client-supplied copy matches the working review now, judged by comparing metadata the client supplied (digest, versions, field names, states). The digest is tamper evidence for accidental edits, not a signature and not authenticity. Current is not reviewed, not eligible, not submittable and not an approval, and a self-consistent forged copy can answer Current.
* The result names field identifiers only; it never shows values or edits the file. Nothing is stored or retained: the file is read in the browser, sent once on press, and not kept.
* Stale, Invalid, Unavailable name a person and a next action in plain words (content standard: reason, owner, next action).

## Planning Readiness

Disposition: executed. Readiness: Ready for planning and prospective independent critique; NOT ready for implementation. Implementation gates are in the plan.
