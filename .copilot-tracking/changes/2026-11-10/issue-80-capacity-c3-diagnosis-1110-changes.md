---
title: Issue 80 capacity C3 stage-local checker correction, changes
description: Prospective and final change record for the admitted C3 continuation
ms.date: 2026-11-10
---

## Prospective (before implement-start)

* Root admitted the continuation on 2026-11-10: the smallest checker-only, stage-local correction for the delayed sibling 401 scenario, after the diagnosis in the [research](../../research/2026-11-10/issue-80-capacity-c3-diagnosis-1110-research.md) (partial chain: launch, research-open, plan-done; prior research and plan stay historical).
* Planned source change: `src/api/checks/capacity_browser_check.py` only. After the first non-JSON 503 for the selected failing endpoint, answer its further startup retries with the same 503 (not held) until the failure assertion passes, then clear that mode before the existing retry click. The sibling read stays held until its original release point.
* Unchanged: all assertions, scenario order, the 401 release point, session-opacity checks, the 60 s timeout, non-JSON `startupFailure` behavior, fatal handling of unexpected errors, both endpoint iterations. No app, API, core, auth, UI or `ops.js` change.
* Claims limit: research observed one packages focused setup only. The workorders iteration and the full original ordering are exercised only by the one allowed whole `capacity_browser_check --axe` run.
* Planned records: this file, review (after the implement-done marker), state. Not yet done: edit, validation, browser run, review.

## Final (2026-11-10)

* Changed `src/api/checks/capacity_browser_check.py` only (+11, 0 deleted; raw diff `phase80-capacity-c3-evidence-1110/impl.diff`): a per-iteration flag `startup_retry_failure`, read by `hold_capacity_read`. While set, requests to the selected failing endpoint (exact `/api/<endpoint>`) are fulfilled with the same non-JSON 503 and not held; the sibling stays held. The flag is set just before the first `failed.fulfill(503)` and cleared right after the existing failure-text assertion, before the retry click. No assertion, ordering, 401 release point, timeout or app change.

| Check | Exit | Result |
| --- | --- | --- |
| Ruff check, format check (checker) | 0, 0 | Pass |
| `node --check ops.js` (unchanged) | 0 | Pass |
| `test_list_export_api` | 0 | 11 OK |
| Related static (5 modules) | 0 | 60 OK |
| `capacity_browser_check --axe`, ONE run, direct Python exit (no pipe), `browser-run1.log/.exit/.head` | 1 | FAILED at an earlier stage, see below |

## Browser run 1 outcome (adverse)

* Passed before failing: seeded render, axe 0 violations, `packages.csv` (1 row) and `workorders.csv` (601 rows) keyboard downloads, all manager routes including `#/time` and `#/aftercare`.
* Failed: scenario `initial packages 503/retry`, `capacity_browser_check.py:571`, `expect(alert).to_contain_text('We could not load packages. Try again.')`, no `alert` for the 60 s timeout; final snapshot showed the status "The service is still starting. Trying again, this can take a few seconds." This stage precedes the edited stage (line ~716) and is not touched by this change. The C2 run passed this stage on the same source, so this is a new unexplained difference; cause UNKNOWN (no instrumentation, no retry, no app-defect claim, no baseline observation).
* Not reached: both delayed 401 iterations (so the correction is unexercised by the whole run), the empty-capacity zero-anchor assertion and later scenarios. Correction validity is therefore UNPROVEN by this run; the earlier focused packages observation (research) remains the only evidence.
* No retry, no auto-repair. Cleanup: no `/tmp/ama-capacity*` scratch or helper left.
