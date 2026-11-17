---
title: Issue 1828 review correction cycle 1 changes
description: Changes record for the viewport premise attribution
ms.date: 2026-11-16
ms.topic: reference
---

## Status

Implementation complete; browser validation deferred (heavy lock held by #1297). Tier FOCUSED. Reviewed head 3a7c655603eeae861c476eca1268a0188efde9bc, base 18d3de459f20018e91fab3af87ab0d89123661c6.

## Planned changes (before edits)

* `src/api/checks/map_fullscreen_browser_check.py`: tighten `check_viewport_change_requests_map` (settle first, attribute the read by bbox-projected width), add helper `map_read_width_px`.
* `src/api/tests/test_map_viewport_premise.py`: new non-browser deterministic tests with a virtual-clock fake page.
* Not edited: application code, `style.css`, `case_journey_browser_check.py`, the original 1828 artifacts and evidence.

## Implemented

* `check_viewport_change_requests_map` now settles map reads (400 ms quiet window) before the resize, records the `#leaflet` client width before and after, collects only reads issued after the resize and requires one whose bbox-projected width (`map_read_width_px`) equals the resized container width (1 px) and differs from the earlier width (1 px). The container must actually change width or the check fails. The viewport and the listener are restored in `finally`. The old `expect_request` any-read acceptance is gone.
* `src/api/tests/test_map_viewport_premise.py`: four deterministic cases on a virtual-clock fake page (stale pending read rejected, resized read accepted, old-width read after resize rejected, unchanged container rejected).
* Unchanged: the `embedded browser shortcuts issue no map requests` assertion, `settle_map_reads`, `check_browser_shortcuts`, `check_shortcuts_after_pending_resize`, the call order in `run_browser`, all application code.
* Edit-method note: the check-file replacement was applied with a Python string replace (reviewed in the diff) and the state-file pointers with `sed`; the test file and other artifacts used `create`/`edit`.

## Failing-first and post-fix (raw logs under `.copilot-tracking/evidence/2026-11-16/issue-1828-review-correction/`)

| Check | Result |
| --- | --- |
| New tests against the old logic (`failing-first-old-logic.log`) | 4 run, 3 FAILED (`AssertionError not raised`: stale pending read, old-width read, unchanged container), the genuine-read positive passed |
| New tests against the fix (`post-fix-unit.log`) | 4 run, OK |
| Regression (`post-fix-regression.log`): `test_map_sensors`, `test_role_*`, `test_ui_support`, `test_browser_harness_scratch`, `test_employee_acceptance_check` | 13, 78, 12, 4, 13 OK |
| `ruff check` and `ruff format --check` on the check and the new test | pass |
| Full map browser and axe run | NOT RUN: heavy lock `/tmp/ama-rpi-heavy.lock` held by #1297 (PID 4021073, `rpi-checks.py --all --out /tmp/rpi-1297-mobile-full-20261116T1645Z`) at 16:45Z and at the last check; not competed for, queued or interrupted |

## Limits and handoff

* The fake page proves the decision logic, not the real Chromium geometry. Whether the bbox-projected width equals `#leaflet.clientWidth` within 1 px in Chromium, and that the check still reaches terminal pass with 14 axe scans, 0 violations and zero skips, is unobserved on this head.
* Named handoff: after the #1297 holder releases the heavy lock, run from `src/api` with `PYTHONPATH=tests:../core/tests:../agents/tests`: `flock -n /tmp/ama-rpi-heavy.lock python -m checks.map_fullscreen_browser_check --axe <pinned axe 4.10.3> --out <external dir>` on the new head, at least twice. If the width tolerance fails in Chromium, the bounded alternative is to attribute by an exact bbox difference from a baseline read captured from a persistent listener started before the expanded-filter step; do not drop attribution.
* The earlier focused browser evidence for head 3a7c655 is historical for the new head.
