---
title: Issue 82 quality rule provenance changes (2026-11-05, increment 4)
ms.date: 2026-11-05
---

* `src/core/src/zava_forward/core/gates.py`: `QUALITY_RULE.source` now cites `docs/prds/zava-forward-retrofit-programme-demonstrator.md FR-008 (governing) and FR-017` instead of the BRD FR-008. Gate, version 1, effective date 2026-11-05 and the unreviewed-exercise reviewer are unchanged.
* `src/core/tests/test_gates.py`: two assertions added to the existing `test_quality_gate_outcomes_and_rule` (source names the PRD requirement; the BRD FR-008 mis-citation is absent).
* RED: that test failed on the old source (AssertionError, exit 1; /tmp/ama82-prov-red.log).
* GREEN (FOCUSED): `test_gates`, `HandoverBlockersTest`, `JsonFlows` 71 tests OK exit 0; `ruff check --no-cache` 0; `ruff format --no-cache --check` 0 (213 files; one earlier E501 in my new test line was fixed); mypy 0 (266 files). External caches, bytecode off.
* No SQL, schema, persistence, role or predicate change. RV-001 history is preserved; the annotation resolves only the citation.
