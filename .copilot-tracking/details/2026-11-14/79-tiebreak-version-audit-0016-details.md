---
title: "Details: #79 tie-break, policy-version and read-only archive regression"
ms.date: 2026-11-14
task_id: 79-tiebreak-version-audit-0016
---

## Phase 1: core tests

File: `src/core/tests/test_ranking_tiebreak_audit.py`

* Cases with equal safety, support, days and stage, and one shared home address, ranked under every permutation: order equals sorted case ids; `snapshot` canonical bytes identical; `deciding_rule` for tied rows is `case_id`.
* `rank` entries and `snapshot` stamp the policy version; a second registry version stamps its own version and hash without changing the v1 result.
* `verify` over a published local archive: directory listing, file bytes and mtimes unchanged; a registry without the version reports a problem and still modifies nothing; an absent archive folder is not created.

## Phase 2: API tests

File: `src/api/tests/test_ranking_tiebreak_read.py`, reusing `QualityMatrix` from `test_role_matrix.py`.

* `/api/ranking/snapshot` entries stamped with the policy version and hash; repeated reads byte-identical.
* `/api/ranking/publication` after one publish: archive bytes, case data and audit entries unchanged across reads; a tampered policy hash in the registry is reported by the verify path without touching the archive (core call).

## Validation

Per the plan: ruff check, ruff format --check, mypy in `src/core` and `src/api`, targeted unittest runs, `test_scenario_manifest.py`.
