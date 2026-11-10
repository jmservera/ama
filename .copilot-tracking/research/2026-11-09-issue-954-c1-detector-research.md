# Research: issue 954 C1 checker detector false positive (2026-11-09)

Task `issue-954-c1-detector`, parent `issue-954-photo-validation`. Local only: no push, PR, issue, board, live provider, credential, model or spend.

## Disposition

Research executed 2026-11-09 against frozen commit `e9fbcaf05` (tree `8431f506`). Planning Readiness: Ready.

## Chronology disclosure

The original lane wrote the checker in scratch before its planning commit (`fa2e2229b`); that disclosed ordering and every earlier failure (lock-busy attempts, interrupted retry loop, the 503 detector failure) are retained unchanged. This C1 cycle is a new, proper prospective cycle: research, plan, details and critique are committed before the checker is edited. It does not retroactively repair the original ordering.

## Correction budget

Standing limit five total scoped correction cycles per issue. Initial productive corrections: 0. C1 is explicitly authorized by the coordinator; after the source edit four remain. No reset and no grant beyond the standing five.

## Evidence

* Single nonqueued real-browser run (admission 2026-11-09T16:12Z) reached the real app and DOM; every behavioural assertion passed for 503, then failed `503: no disruptive toast, alert, dialog or modal`. Quiet classification and 403 were not reached.
* The only matched node is `<p id="account-error" class="err" role="alert"></p>` (`src/api/src/zava_forward/api/web/index.html:34`), a persistent empty inline live region. `app.js:193` clears it and `app.js:1693` fills it with an error message on a failed account action. The existing assertion already requires its text empty after the denials.
* Checker `WATCH` (src/api/checks/photo_flag_stale_browser_check.py) matches any added node with `[role=alert]`, `[role=alertdialog]`, `dialog`, `[aria-modal=true]`, `[class*=toast]`, `[class*=snackbar]`, `[id*=toast]` regardless of visibility or content, and only on added nodes, so a later fill of an existing alert would also be missed.
* No product or API bug is reproduced. Product code is out of scope.

## Defect classification

Checker-only false positive: an empty ordinary inline alert placeholder is not a disruptive toast or error. A blanket ignore of empty dialogs, modals, backdrops, icons with accessible names, or all `role=alert` nodes is rejected: visible meaningful overlays must still fail.

## Owner definition of quiet (unchanged)

No disruptive employee-facing toast and no unhandled application error after an expected 503/403. Inline status, initials fallback and native failed-resource diagnostics are acceptable and remain recorded unfiltered, with no broad console filtering.
