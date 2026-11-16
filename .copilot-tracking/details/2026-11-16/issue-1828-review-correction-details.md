---
title: Issue 1828 review correction cycle 1 details
description: Phase details for the viewport premise attribution
ms.date: 2026-11-16
ms.topic: reference
---

## Phase 1 details

* Pure helpers in the check module: `map_read_width_px(url)` returns the projected pixel width from `bbox` and `zoom`, or `None`.
* The fake page has a virtual clock (`time.monotonic` patched) so settle logic runs without real waiting, schedules request events, resizes the container on `set_viewport_size`, and emulates `expect_request` so the same test drives the old logic.
* Expected against old logic: the stale-read case passes the old check, so its test fails (failing-first).

## Phase 2 details

`check_viewport_change_requests_map`:

1. `settle_map_reads` (existing 400 ms quiet window).
2. Record `before` container width, install a request listener, resize.
3. Poll up to 5 s for a read after the resize; compare its bbox width with the container width read then; require agreement within 1 px and a difference from `before` of at least 1 px.
4. Restore the viewport and the listener in `finally`.

Failure messages name the cause (no read, unattributed read, container did not change). No weakening: nothing is skipped or accepted without a bbox.

## Phase 3 and 4 details

Run `unittest` for the new file from `src/api`, `ruff check` and `ruff format --check`. Browser: check heavy lock holder first; use `flock -n /tmp/ama-rpi-heavy.lock` only if free.
