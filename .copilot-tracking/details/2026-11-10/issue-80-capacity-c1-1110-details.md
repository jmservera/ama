---
title: Issue 80 capacity browser check time-status expectation, details
description: Exact edit and validation commands for the C1 correction
ms.date: 2026-11-10
---

## Phase 1: the edit

File `src/api/checks/capacity_browser_check.py`, branch `elif href == "#/time":` inside `verify_route`. Replace the single `expect(... first).to_have_text("Time capture is on." if status["enabled"] else status["reason"])` with a local `banner` locator and three branches:

* `status["enabled"]`: `to_have_text("Time capture is on.")`.
* `not status["flag_on"]`: `to_have_text` of the exact sentence in `timecapture.js` `timeBlockedText` for the switched-off state.
* otherwise: `to_have_text(re.compile(r"\S\. Owner: .+\. Next action: .+"))`.

`re` is already imported. No other line changes.

## Phase 2: commands (from `src/api`, `PYTHONPATH` covering `src/*/src` and tests)

* `ruff check` and `ruff format --check` on the checker.
* `node --check src/zava_forward/api/web/ops.js`.
* List-export API unit tests (the 11 used in the original loop) and the related static tests (60).
* One run of `python3 checks/capacity_browser_check.py --axe`. It takes `/tmp/ama-rpi-heavy.lock` with `LOCK_NB` itself and builds its own temporary synthetic store; no outer lock, no `ZF_DATA`. Busy or missing prerequisite blocks and is reported.

## Success criteria

* Run reaches the manager route loop, both downloads and `empty capacity`, and exits 0; otherwise report the exact failing stage and exit.
* The original `browser-run1.log` and `.exit` stay unmodified; the new log is `ROOT/phase80-capacity-c1-evidence-1110/browser-run2.log`.
