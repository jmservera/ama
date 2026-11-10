---
title: Details for #185 current-main preparation
ms.date: 2026-11-05
---

* Phase 1: verify pins and clean ignored-inclusive status (done).
* Phase 2: ordinary merge of pinned main into the child.
* Phase 3: selectors `test_device_identity.py` and `test_device_provision.py` (previous 45 tests), ruff check and format check with no cache, mypy over src and tests as in `.github/workflows/src-ci.yml` with `--cache-dir=/tmp/mypy-185-prep`.
* Phase 4: changes, review and state records.
