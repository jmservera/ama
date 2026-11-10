---
title: Issue 144 main-based slice A port phase details
description: Phase details and exact bounded commands for E1
ms.date: 2026-11-10
task_id: issue-144-main-port-extension1
---

## Environment

* Own venv outside the repository: `ROOT/144-main-port-extension1-1110/venv`; external pip cache; `PYTHONDONTWRITEBYTECODE=1`. Install editable `src/core`, `src/agents`, `src/api` and declared tools only after a missing-dependency failure, then assert editable origins in this worktree.
* Each command records its own exit directly into a unique immutable log under `ROOT/144-main-port-extension1-1110/logs`; no tail or tee masking; a first failure keeps its full trace.

## Phase 1: Core ledger (ai_consumption.py)

Add `_scope`, `reserve_in`, `dispatch_window_ms`, `complete_in`, the two constants; wrap `reserve` and `complete`.

## Phase 2: Interface (ai.py)

Add `is_live`, `request_plan`; `_request` uses `is_live`.

## Phase 3: Permit service (assistants.py)

Constants, marker block in `claim`, `_markers`, `_fence_in` (shared with `fence_send`), gates, `_refuse_attempt`, `issue_permit`, `complete_result`, `_settle_meter`.

## Phase 4: Tests

Core ledger tests in `src/core/tests/test_ai_consumption.py`; service permit and fail-closed tests in `src/api/tests/test_ai_consumption_api.py`.

## Phase 5: Validation

Selectors: the two edited test files, `test_ai_call_site_inventory.py`, `test_ai_dispatch_marker.py`, `test_assistants.py`; ruff and mypy as configured. Red evidence: new fail-closed and clock tests must fail on the base bytes (run against `git stash`-free copy: run the new tests with the three source files from origin/main in a temporary external checkout).

## Phase 6: Review

One authored review; open findings route to later work.
