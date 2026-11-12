---
title: Issue 153 stale-stage refusal changes
ms.date: 2026-11-12
task_id: 153-blocked-copy-readiness-1112
---

## Changes

* `src/core/src/zava_forward/core/store.py` `Store.advance`: the stage-precondition `ValueError` now reads "This case is not at the final checks. It may have changed since you opened it. Case owner: {c['owner']}. Next action: copy any unsaved notes, then reload the case and check its current stage before taking further action." Same exception type, 400 status, no client, gate, permission or approval change.
* `src/api/tests/test_mvp.py` `ApiTests.test_stale_advance_refusal_names_case_owner_and_next_action`: Sam and Pam sign in over HTTP; Pam advances ZF-3 (200); Sam's stale advance and an earlier-stage advance (ZF-1) both return 400 with the new reason, case owner and next action, no `reasons`, and the case stays `Install booked` with no extra advance event.

## Amendments to the plan (from the critique)

Wording changed from "refresh the case and check its history" and "Owner:" to the unsaved-notes and "Case owner:" form (see the critique record). Earlier-stage case added to the test.

## Validation (all in the isolated pip venv `/tmp/i153/venv`, no uv, no source-package PYTHONPATH; `PYTHONPATH=../core/tests:../agents/tests` only exposes shared test fixtures as the guide specifies)

| Command (from `src/api` unless noted) | Result |
| --- | --- |
| Regression before the source change (`python -m unittest tests.test_mvp.ApiTests.test_stale_advance_refusal_names_case_owner_and_next_action`) | Exit 1, failed on the old message (`/tmp/i153/test-before.txt`) |
| `python -m unittest tests.test_mvp tests.test_content_standard tests.test_case_journey -q` | 72 tests OK (`/tmp/i153/test-after.txt`) |
| `ruff check .` in core and api | passed |
| `ruff format --check .` in core (245 files) and api (152 files) | passed; `store.py` is format-excluded by project config |
| `mypy` in core (298 files) and api (236 files) | no issues |
| `/tmp/i153/race.py` repeat (`/tmp/i153/race-out-after.txt`) | Client A rendered message: the new text; button and stale card still shown |

Original outputs retained unchanged: `/tmp/i153/race-out.txt` (before), `/tmp/i153/trace*-out.txt`, `/tmp/i153/ui-out.txt`.

## Not run or limits

Full or `--changed` gate, hosted CI, SQL Server tests, axe/contrast, the full api and core suites, human or accessibility acceptance. The browser check is a non-repository script. No browser test of unsaved-draft retention: the client path is unchanged. The stale card and button remain after the refusal (existing behaviour, unchanged by design: no automatic refresh or replay). web-design-guidelines was loaded and fetched before work; no web file was edited.

## Remaining criteria

Issue 153 criteria 2, 3 (universal) and 5 stay unproven and unticked.
