---
title: Issue 152 supported devices changes
description: Changes for the owner-decision proposal slice
ms.date: 2026-11-01
---

## Changes

* Added `docs/reference/research/ux/supported-devices-proposal.md` (proposed, not decided).
* Added `supported_devices` (status `proposed`) to `src/api/checks/workbench-manifest.json`.
* Added `test_supported_devices_stay_proposed_and_match_checked_widths` to `src/api/tests/test_workbench.py`.
* Indexed the proposal in `docs/reference/README.md`; appended `docs/reference/log.md`.

## Validation (focused tier, local venv, pip)

* `unittest test_workbench test_accessibility_baseline`: 11 tests OK.
* `ruff check`, `ruff format --check`, `mypy` on the touched test: clean.
* No heavy local gate; CI is the evidence. No web behaviour changed.

## Divergences

None. Plan phases 1 to 3 complete.
