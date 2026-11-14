---
title: Changes - rule provenance tests (#82)
ms.date: 2026-11-14
---

* `src/core/tests/test_gates.py`: added `RuleProvenanceExposureTests` (3 tests).
* No production code changes. Existing tests cover AC1 (deterministic gate outcomes with reason), AC2 (unknown never passes) and AC3 (safety release by named role and different person).
* Validation: results recorded in the review.
