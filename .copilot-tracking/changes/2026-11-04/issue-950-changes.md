---
title: Issue 950 changes
ms.date: 2026-11-04
---

* `src/core/src/zava_forward/core/discovery_register.py`: `SEED_PROPOSER`, set on seeds.
* `src/core/tests/test_discovery_register.py`: `test_seed_constraints_name_a_proposer`.
* `docs/reference/log.md`: entry appended.
* Validation run: `test_discovery_register` (13 OK), ruff check and format, mypy strict with `--cache-dir=/tmp/mypy-949` on both files.
* Not run: gate, benchmarks, full suites, other projects.
