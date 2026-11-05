---
title: Issue 82 quality rule provenance details (2026-11-05, increment 4)
ms.date: 2026-11-05
---

* `gates.py` `QUALITY_RULE.source` becomes `docs/prds/zava-forward-retrofit-programme-demonstrator.md FR-008 (governing) and FR-017; versioned quality checklist in quality.CHECKLISTS (exercise fixture)`.
* Test: in `test_quality_gate_outcomes_and_rule`, assert `record["source"]` contains the PRD path and `FR-008`, and does not contain the BRD path.
* Checks (FOCUSED, from `src/core`, `PYTHONDONTWRITEBYTECODE=1`, exact-worktree `PYTHONPATH`): `python -m unittest test_gates test_quality_procurement.HandoverBlockersTest`, `ruff check --no-cache .`, `ruff format --no-cache --check .`, `mypy --cache-dir=/tmp/ama82-prov-mypy`.
