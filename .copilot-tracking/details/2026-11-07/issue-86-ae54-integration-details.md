---
title: Issue 86 integration of local parent ae54963 details
description: Exact commands and checks for the merge (Refs #86)
ms.date: 2026-11-07
---

Scratch: `/mnt/ama-gates/g86-ae54-preparation-1107/{src,tmp,xdg,mypy,ruff}`, all new. `PYTHONDONTWRITEBYTECODE=1`. Venv from retained R4 core env (installed distributions); install only after an actual missing-package failure.

## Selectors, from `src/core` of the archive snapshot

* `python -m unittest tests.test_resident_decisions` (expected 308 tests, 110 skips, matching the corrected baseline).
* `python -m unittest tests.test_quality_procurement` for the incoming parent test change.
* `python -m mypy` (strict, 267 files in the component config) and `python -m ruff check .` and `ruff format --check .`.
* Print `zava_forward.core.resident_decisions.__file__` and `complaints_route.__file__` to prove origin in the snapshot.
* Blob check: `git rev-parse <pre-merge>:<path>` equals `HEAD:<path>` for the five complaint paths.
* Expected adoption: `appointments.py`, `case_journey_browser_check.py`, `latest.json` equal parent blobs.

Outputs and exits are kept unpiped to files in scratch. No deletion of anything.
