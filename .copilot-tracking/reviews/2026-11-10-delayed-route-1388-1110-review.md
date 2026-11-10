---
title: Issue 1388 delayed-companion route-delivery review
ms.date: 2026-11-10
task_id: 1388-delayed-route-1110
---

## Execution

Review executed once on 2026-11-10 after implementation, over the uncommitted source delta from HEAD `83503b74e0e5f555382436c0ae27f64cd200971f` (two files) and the changes record. It was a same-agent review (no nested agents; the brief forbids new agents), so it is not the independent exact-head assessment that Root requires before publication. Outcome: accepted, no blocking finding; two Low findings routed to later work. No second Review is run in this task.

Assessed boundary: `src/api/checks/workspace_scripts_browser_check.py`, `src/api/tests/test_browser_asset_urls.py`, the plan, details, critique, research, issue record, state and the raw check logs in the coordinator session `checks-1388-initial-1110/`.

## Acceptance criteria assessment

* Deterministic DOM-ready-before-delivery regression through the real routine: met. Red on the original (16 failures, eight of them the exact count assertion over four variants at two delivery turns), green after.
* Zero-delivery and double-pending controls fail explicitly; prompt delivery succeeds; exact count one, intended identity (route-by-asset pattern, first aborted, later held) and `finally` cleanup preserved: met in the deterministic cases; cleanup is asserted in every case.
* Four real-browser variants retain their assertions: met. They were executed separately (isolated and after the recovery precursors), all PASS; the diff does not touch their assertions. Names and commands are in the changes record.
* Loader/checker tests and configured static checks pass, no production or retry-policy change: met. 24 selector tests, `ruff check`, `ruff format --check` and `mypy` pass with the pinned own-venv tools; `git diff --name-only -- src` shows only the two files.
* Own prospective RPI artifacts, original adverse evidence, independent exact-head review and hosted checks: artifacts and adverse evidence recorded; independent review and hosted checks remain required later and are not claimed.

## Findings

* Low: the pump loop exits as soon as `pending` is non-empty, so a duplicate retry arriving after that moment is only caught by the later `len(requests) == 2` assertions, not by the count. Same as the original semantics; the control covers duplicates delivered before the check. Route to a later task only if a duplicate-timing defect is observed.
* Low: the deterministic doubles depend on the call order up to the count assertion (a sentinel on the first later interaction). A future reorder of the routine's pre-count calls could break the test loudly rather than silently. Accepted; no change.
* Process note: the original-source baseline failure for `sign_out` had no captured traceback because the driver swallowed it; recorded as such, not rerun.

## Disposition

* The whole-workspace checker still stops at the independently owned #1384 exhaustion oracle (line 150 after the edit). It is not reported green and gives no delayed coverage; the separate variant runs do.
* Open work: Root independent exact-head assessment, hosted checks, and #1384 adoption followed by its own BOTH browser checks.
