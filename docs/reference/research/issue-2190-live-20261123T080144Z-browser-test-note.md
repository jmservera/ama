---
title: "Issue 2190: deterministic browser regression test for the late_success race"
description: A real Chromium test reproduces the gap between the list route's two reads and shows the settle wait closes it, which earlier notes recorded as unproven.
ms.date: 2026-11-23
---

Scope: issue #2190, flake 2 (`late_success` in `src/api/checks/employee_chat_browser_check.py`). Synthetic DEMO, desktop only. No Azure resource was read or changed. Earlier notes: [2026-11-21](./issue-2190-live-20261121-2026-11-21.md), [2026-11-23](./issue-2190-live-20261123-note.md), [r2](./issue-2190-live-20261123T071426Z-note.md).

## Change

`src/api/tests/test_employee_chat_settle.py` gains `SettleRouteBrowserTests`. A local page writes `#workspace-status` 1200 ms after a hash change with no request in flight, which models the gap between the list route's facets read and cases read. `networkidle` alone returns with the status still empty (the race); `settle_route(page, "#/")` returns with `Perspective:` written. No source or check change; no check relaxed.

## Evidence

* Three consecutive runs of `python3 -m unittest tests.test_employee_chat_settle` from `src/api`: 4 tests OK each time, about 2.7 s.
* `python3 -m mypy` in `src/api` clean; ruff check and 100-column format pass on the file.
* Not run: the complete local gate (coordinator-owned) and hosted CI for the exact head. Tier focused, since no source code changed.

## Per-criterion verdict

| Criterion | Verdict | Basis |
| --- | --- | --- |
| Each flake reproduced or explained | Flake 2 now reproduced deterministically in miniature; flakes 1 and 3 proven in earlier notes | Control test above |
| Fixed with a regression test | Proven for flake 2 with a behavioural test; flakes 1 and 3 per earlier notes | This note |
| No check relaxed | Proven | Only a test was added |
