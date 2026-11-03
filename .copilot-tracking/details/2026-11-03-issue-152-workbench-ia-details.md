---
title: Details, issue 152 per-profile default manifest slice
ms.date: 2026-11-03
---

## Phase 1

* File: `src/api/checks/workbench-manifest.json`. Eight identity profiles gain `default`: `ids` equal the role's own queue; `count` equals its length; `order` equals `default_sort`; `selection` null; `empty_reason` "no representative scenario supplied" when empty. Deferred profiles stay without defaults.

## Phase 2

* File: `src/api/tests/test_workbench.py`: `test_profile_defaults_match_own_queues_and_declare_empty_reason`.
* File: `src/api/README.md`: manifest paragraph updated; still states not full AC-034/043.

## Phase 3

From `src/api` in a /tmp venv with editable src installs: `python -m unittest tests.test_workbench`, `ruff check`, `ruff format --check`, `mypy --cache-dir=/tmp/mypy-152`.
