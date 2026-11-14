---
title: Issue 130 challenge route changes
ms.date: 2026-11-14
---

## Changed files

* `src/core/src/zava_forward/core/resident_decisions.py`
* `src/core/tests/test_resident_decisions.py`

## Validation

* `TMPDIR=/dev/shm/zf-tmp PYTHONPATH=src:tests:../agents/src python3 -m unittest tests.test_resident_decisions -k nomination -k intake -k challenge -k hazard`: 96 ran, OK (35 skipped, existing skips).
* `tests.test_challenges`, `tests.test_hazard_referral`: 64 ran, OK.
* `ruff check` and `mypy` on both files: clean. `unittest discover` not run, as directed.

## Not done

Tier: focused (core logic, no gate, SQL schema, workflow or dependency change). No UI or API route change; hosted CI not observed; nothing pushed.
