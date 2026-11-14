---
title: Challenge non-retaliation changes (issue 220)
ms.date: 2026-11-14
---

## Changes

* `src/core/src/zava_forward/core/challenges.py`: protected key set, snapshot, change detection, `assert_no_retaliation`, `GUARANTEES`.
* `src/core/src/zava_forward/core/resident_decisions.py`: guard in `challenge_open`, `challenge_resolve`, `nomination_correct`.
* `src/core/src/zava_forward/core/store.py` and `projection.py`: `challenge_guarantees` in detail, removed for readers without rights.
* `src/api/src/zava_forward/api/web/panels.js`: guarantees list in the challenge panel.
* `src/api/tests/test_challenge_non_retaliation_hazard_guard.py`: 6 focused tests.
* `src/core/README.md`: guard description.

## Validation (focused tier)

* New module, `test_resident_api`, `test_accessibility_baseline` (api) and `test_challenges`, `test_resident_decisions` (core): pass.
* mypy and ruff check and format with /tmp cache dirs in `src/core` and `src/api`: clean.
* Not run: `tools/rpi-checks.py --all`, Docker, hosted CI, browser harness.
* Local runs used PYTHONPATH to the worktree sources because editable installs point at another checkout.
