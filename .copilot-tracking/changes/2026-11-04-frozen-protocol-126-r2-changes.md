---
title: Issue 126 round 2 changes
ms.date: 2026-11-04
---

* Modified `src/core/src/zava_forward/core/governance.py`, `src/core/tests/test_governance.py`, `src/core/README.md`, `docs/reference/log.md`.

## Validation

Run (PYTHONPATH pointed at this worktree because installed editable packages resolve to another worktree): `test_governance.py` (71 tests, 16 skipped opt-in MSSQL, pass), `src/api/tests/test_governance_evidence_api.py` (10 pass), `ruff check` on src/core (pass), `mypy` for src/core as in `src-ci.yml` with `--cache-dir=/tmp/mypy-126` (253 files including tests, pass).

Not run: the gate, benchmarks, full suites, MSSQL opt-in tests, browser checks, `ruff format --check` (governance.py was unformatted before this change).

## Divergence

None from the plan.
