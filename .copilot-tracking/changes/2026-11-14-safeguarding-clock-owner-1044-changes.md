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
