---
title: Issue 1837 standalone nomination forms, live demo evidence
description: Per-criterion record for issue 1837 on current main and the deployed synthetic demo, with failing-first, axe and negative-boundary evidence
ms.date: 2026-11-18
ms.topic: reference
---

## Scope

Synthetic demo only, desktop only. Refs #1837. Source at `cfd272051` (main) on branch `test/nomination-ack-live-20261118T1854Z`. Deployed target: `ca-cutover-test-demo-api` revision `0000032` (resource group `ama`). No Azure resource was created, nothing was deployed, no demo record was written, and no credential is recorded.

## Finding

The transport defect in the issue was repaired in source by #1878: `web/nomination-routes.js` cancels the native submit and posts JSON with `X-ZF-CSRF: 1`. The server still reads JSON only, which is the correct shape: a header-less urlencoded post could not carry the trusted-proxy CSRF header, so accepting urlencoded bodies server side would have widened the write surface. The deployed demo image predates that script: `/nomination-routes.js` returns 404 and the routes page has no script tag.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Failing-first regression coverage for all three browser submissions, valid challenge target | Proven on source; not failing on main | [failing-first-at-9da3fcd.txt](issue-1837-live-2026-11-18/failing-first-at-9da3fcd.txt): both new/extended tests fail at the issue source `9da3fcd` and pass on main (8 module tests OK) |
| Valid submissions succeed and retain account, owner, provenance, correction and challenge records; JSON callers compatible | Proven locally; unproven live | Extended `test_standalone_route_forms_submit_in_browser` asserts owner, original account, correction source and challenge record; existing JSON tests unchanged and passing. Live write not attempted: the deployed image lacks the script and redeploying is a production change |
| Negative tests keep authorization, case isolation, malformed input, same-origin/CSRF | Proven | New `test_native_form_encoding_is_refused_and_writes_nothing` (400, case unchanged); existing role-denial (403) and malformed tests; live [live-negative-probe.json](issue-1837-live-2026-11-18/live-negative-probe.json): urlencoded 400, JSON without header 403, malformed 400, unknown case 404, mismatched body case 400, case unchanged |
| Directly affected browser journeys with axe, zero unexpected skips, unit tests | Partly proven | [axe-route-forms-result.json](issue-1837-live-2026-11-18/axe-route-forms-result.json): three real browser submissions all 200, axe 4.10.3 (SHA-256 verified) zero violations except one `target-size` (WCAG 2.5.8) on the unstyled standalone page, recorded as an open finding; one `color-contrast` incomplete in the open state. `tests.test_nomination_api_routes` 8 tests OK, no skips |
| Separate dated RPI evidence; independent exact-head review; hosted CI | Partly proven | RPI artifacts dated 2026-11-18 under `.copilot-tracking/`; independent review and hosted CI cannot be done by this worker and are not claimed |
| Conservative full-tier classification; verified external full receipt | Unproven by instruction | Classified FULL (a file under `src/api/checks/` and write-handler tests changed); the full gate was not run, as instructed |

## Open items

* axe `target-size` on the standalone routes page (summaries about 19px high). Fix needs a stylesheet decision for that page; out of the transport repair.
* The deployed demo needs a rebuild from current main before the live journeys can be shown; that is a deployment action outside this task.

## Commands

* `python3 -m unittest tests.test_nomination_api_routes` from `src/api` (8 OK)
* `python3 -m checks.nomination_route_forms_browser_check --axe <axe-4.10.3.min.js> --out axe-route-forms-result.json`
* `python3 -m mypy` in `src/api`: no issues in 348 files; `ruff check` and `ruff format --isolated --line-length 100 --check` clean on changed files. The test and ruff runs were re-observed in independent review (8 tests OK, ruff clean); the mypy result is observed; raw output not retained.
* Live probes: `probe_readonly.py`, `probe_negative.py` (read credentials at run time, print none)
