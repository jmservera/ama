---
title: Issue 1837 nomination check lock diagnosis and per-criterion record (2026-11-27, run c)
description: Diagnosis of the nomination_browser_check timeout left open by run b, the harness repair, and the per-criterion status for issue 1837; synthetic demo only
ms.date: 2026-11-27
ms.topic: reference
---

## Scope

Synthetic demo, desktop only. Refs #1837. Base `337d3999d5`. No Azure resource was created or changed and no credential is recorded. Builds on the [run b record](issue-1837-live-demo-evidence-2026-11-27-b.md).

## Finding

No defect in the three standalone nomination forms. The open item from run b was a harness defect in `checks.nomination_browser_check` (read-only nomination view, #1381):

* The page's `GET /api/assistants` runs `assistants.registry`, which opens `BEGIN IMMEDIATE` on its own connection and keeps working after the page navigates away. Under host load (average 8 to 13) it held the SQLite write lock past the 5 s `busy_timeout`.
* The harness's out-of-band `nomination_review` write then failed with `database is locked` (HTTP 500) and the 5 s client timeout raised `TimeoutError`. [Lock-holder capture](issue-1837-live-2026-11-27-c/lock-diagnosis-before.txt): two of three probe runs failed.
* A first repair (wait for network idle) did not help, because the server keeps processing requests the page abandoned; three runs failed. It was reverted.
* Repair: the check's route handler aborts `/api/assistants*` requests, which the nomination view does not use. Three consecutive runs then passed ([1](issue-1837-live-2026-11-27-c/axe-nomination-result-1.json), [2](issue-1837-live-2026-11-27-c/axe-nomination-result-2.json), [3](issue-1837-live-2026-11-27-c/axe-nomination-result-3.json)), with no `database is locked` in any output.

Not changed: `assistants.registry` taking a write transaction for a GET. That is RAI control-plane policy outside #1837 and is routed as a follow-up. The check passed with `non_get_requests_while_viewing` empty.

## Other runs on this head

* `python3 -m unittest tests.test_nomination_api_routes tests.test_nomination_screen tests.test_accessibility_baseline tests.test_content_standard` from `src/api`: [68 OK](issue-1837-live-2026-11-27-c/unit-tests.txt).
* axe 4.10.3: [standalone forms](issue-1837-live-2026-11-27-c/axe-nomination_route_forms-result.json) and [challenge](issue-1837-live-2026-11-27-c/axe-challenge-result.json) passed.
* `python3 -m mypy` in `src/api`: no issues; `ruff check` and `ruff format --isolated --line-length 100 --check` on the changed file: clean.
* Live: the demo (`ca-cutover-test-demo-api`, revision 0000138, Running) answers `401` to unauthenticated requests for both scripts ([probe](issue-1837-live-2026-11-27-c/live-static-probe.txt)), so this run proves only that the revision is up. Authenticated no-write live proofs are in the [2026-11-20 record](issue-1837-live-demo-evidence-2026-11-20.md); live writes stay withheld because they add irreversible records to the shared demo.
