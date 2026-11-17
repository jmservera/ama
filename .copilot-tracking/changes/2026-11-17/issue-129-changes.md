---
title: Issue 129 changes (2026-11-17)
description: Changes log
ms.date: 2026-11-17
---

## Changes

* `src/core/tests/test_learning_test_bundles.py`: added `ProtocolDocAgreement` comparing the protocol bundle table with `BUNDLES`. Measured: passes on the real doc, fails when a stop rule in the doc is altered (mutation reverted).
* `docs/reference/research/ux/journey-learning-test-bundles.md`: `ms.date`, next-slices list now records the CLI, scenario tests and drift guard; criteria stay unmet.
* `docs/reference/log.md`, `docs/reference/README.md`: log entry and index row.

## Validation (FOCUSED)

| Command | Result |
| --- | --- |
| `python3 -m unittest tests.test_learning_test_bundles tests.test_live_doc_links` (src/core) | 29 tests OK |
| `ruff format --isolated --line-length 100 --check tests/test_learning_test_bundles.py` | already formatted |
| `python3 -m mypy` (src/core) | no issues, 327 files |

Not applicable: src/api tests (no api change), full gate, SQL, browser, hosted CI (no push).
