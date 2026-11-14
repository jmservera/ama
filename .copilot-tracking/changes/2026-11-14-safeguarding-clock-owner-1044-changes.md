---
title: Changes, safeguarding clock and named owner display
ms.date: 2026-11-14
---

## Changes

* `src/core/src/zava_forward/core/taskqueues.py`: `safeguarding_clocks` and constant `SAFEGUARDING_HELD`; `context` now returns `safeguarding_clocks` (empty unless `reason_ok`) and `safeguarding_visibility`.
* `src/api/src/zava_forward/api/web/app.js`: `workSummary` renders a text `safeguarding-clock` paragraph for queue rows and the case card.
* `src/core/tests/test_taskqueues.py`: `SafeguardingClock` (visibility, no free text, Unknown owner, overdue/completed/closed, membership unchanged).
* `src/api/tests/test_safeguarding_clock_a11y.py`: Node-run rendering of the real `workSummary`: text-only status, named owner, nothing when absent.

## Validation

* Editable installs resolve to the main checkout, so worktree sources were run with explicit `PYTHONPATH`.
* `unittest`: 134 core tests across taskqueue, SQL queue, coordinator, reads, AI consumption and exception feeds pass; 44 api tests (role screens, queue empty state, resident API, new a11y) pass with 1 pre-existing skip. The full core and api discovery runs were stopped after exceeding 40 minutes on a shared host and are NOT claimed.
* `mypy .` clean in core and api; `ruff check .` and `ruff format --check .` clean in both.
* Not run: browser checks, hosted CI, complete local RPI gate.

## Divergences and limits

* Data feed: no importer or API writes `safeguarding_items` yet; the display is dormant until the owner records the safeguarding policy (duration, lead role, DPIA, visibility). Issue criterion NOT ticked; this PR should use `Refs #76`.
* Visibility reuses the existing need-to-know roles (`can_see_reason`); the owner may change that set.
* Validation tier: focused (non-gate UI/core display), strictest applicable not triggered as no infra, SQL, deployment or security-control change; however safeguarding visibility is privacy-sensitive, so an independent exact-head review is still required.

## Cycle 1 of 5 fixes (independent review of 1411c83a4, Refs #76)

* Critical: `Store.detail()` (inherited by `SqlStore`), `projection.redact_staff_detail()` and `hold_notes()` now strip raw `safeguarding_items`; only the allowlisted `work.safeguarding_clocks` leaves the store, so free-text notes never leak to any role.
* Medium: `taskqueues.safeguarding_clocks()` accepts a string or dict owner (trimmed) and ignores non-string or unparseable `response_due_at` without raising.
* Tests: `src/api/tests/test_safeguarding_detail_boundary.py` (HTTP `/api/cases/<id>` and `SqlStore.detail()` role matrix with canaries) and `SafeguardingClockInputs` in `src/core/tests/test_taskqueues.py`.
* Validation: test_taskqueues, test_safeguarding_detail_boundary, test_safeguarding_clock_a11y, test_accessibility_baseline, test_role_screens pass; ruff check, ruff format --check and mypy clean in src/core and src/api (run with worktree PYTHONPATH because editable installs point at another checkout). Focused tier; full gate not run. Not pushed.
