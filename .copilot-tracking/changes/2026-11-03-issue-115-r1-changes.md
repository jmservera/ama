---
title: Issue 115 round 1 changes
ms.date: 2026-11-03
---

* src/orchestrator/src/zava_forward/orchestrator/digest_blob.py: `reconcile`, `--reconcile`, two markers.
* src/orchestrator/tests/test_digest_blob.py: three reconcile tests.
* src/orchestrator/README.md: usage and boundary.
* No knowledge-base file changed, so no index or log.md entry.

## Validation

Run in src/orchestrator: `python3 -m unittest tests.test_digest_blob` (26 OK, with PYTHONPATH=../core/tests:../core/src:src), `ruff check`, `mypy --cache-dir=/tmp/mypy-115 src` (clean).

Not run: gate, full suites, benchmarks, Azure, deployment or hosted checks.
