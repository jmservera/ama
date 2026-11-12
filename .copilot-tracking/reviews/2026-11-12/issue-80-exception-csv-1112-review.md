<!-- markdownlint-disable-file -->
# Review: #80 browser-built exception-summary CSV (issue-80-exception-csv-1112)

Execution: executed once by the implementing author after implementation. It is not independent exact-head review, which is required before publication and is not claimed.
Assessed boundary: branch feat/demo-exception-summary-csv-80-1112 on base 139176fa0382add781b1830b1ac9db785ed086fe, the working tree before the local commit.
Outcome: Conformant to the admitted bounded scope, with the limits below. No material finding is open.

## Evidence checked

* Contract: four columns with closed vocabularies; per-view reference qualified in header and note; unknown values `Unknown`; non-matching id, `state != ok`, empty and any unreadable entry offer no file. Byte contract (UTF-8, no BOM, CRLF, quoting, apostrophe prefix) checked by exact-bytes test and parity with `list_export.safe_cell`.
* No exposure: marker strings in every excluded field and the owner address never reach the file (unit test); the browser file bytes equal an independent projection of the JSON the page received.
* No new request: node harness records zero `api` calls on activation; the browser check records zero http requests on two activations and exactly one `/api/exceptions` request on the populated view. Blob and data URLs are excluded from that count by design.
* Audit and writes: Store-level test shows one view adds one ledger entry and leaves the data unchanged; browser check shows no non-GET request and no model request. No zero-audit claim is made.
* Failure and cleanup: Blob failure and click failure give "No file was created" text, remove the anchor and release the URL; success releases the URL after a delay (browser: 2 created, 2 released).
* Web guidelines (fetched fresh before edits and again before the final review): native button, `aria-describedby`, `role="status"` live message, global `:focus-visible` and hover states, no transition, no inline style, reflow at 320 px checked, error message has a next step. Findings: none open. Role-screens.js:930-966 reviewed.
* Scope: `git diff --stat` shows only the files listed in the changes record plus dated `.copilot-tracking` artifacts.

## Limits and residual risks

* Chromium only; axe skipped; no manual assistive-technology evidence, so no accessibility acceptance is claimed. A browser download event proves initiation, not that the file was saved.
* A delayed (1 s) `revokeObjectURL` is not proven for slow browsers; a download that starts later than that is not covered.
* The conformance "no timers" guard was narrowed to one exact allowed call; a reviewer should confirm that is acceptable.
* The status message repeats text on a second activation, so a screen reader may not re-announce it.
* Not run: full gate, `--changed`, hosted CI, endpoint inventory test. No named human, operational or AT acceptance; no issue criterion is proven or ticked, so a PR must use `Refs #80`.

## Routed follow-ups

1. Independent exact-head review before any publication.
2. Optional later: axe and manual keyboard/screen-reader evidence; owner decisions P1-P4 of the PR1462 contract.
