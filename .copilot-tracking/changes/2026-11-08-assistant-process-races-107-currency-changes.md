---
title: Changes for the current-main currency of the process race tests (#107, C10)
description: Normal merge of main f548b65, preserved blobs, light results and unrun gates
ms.date: 2026-11-08
---

Research and plan: [currency research](../research/2026-11-08-assistant-process-races-107-currency-research.md). Critique: [critique](../plans/2026-11-08-assistant-process-races-107-currency-critique.md). Earlier [changes](2026-11-07-assistant-process-races-107-changes.md) are preserved unchanged.

## Delta

* Prospective commit `90f36a555` (records only), then ONE normal merge `cb28aecd0883c1590c1c48f58f54403d939f3487` with parents `90f36a555f2cb1203025c16452ed1bc79c001844` and `f548b65f4aa31eb92a2cc9cb801130e422daed7f`. No rebase, amend, reset, force or branch move; no conflict.
* Net change against main: only `src/api/tests/test_assistant_release.py`, `src/api/tests/assistant_process_worker.py` and `.copilot-tracking/` records. Both test files keep the blobs of `ede8bd701`. Main's `.github/rubric/scores/latest.json` (parses as JSON), `tools/rpi-checks.py`, `store.py` and `assistants.py` keep main's blobs. No test or fixture reconciliation was needed; no production, schema, policy or approval change.
* `git diff --check` against main exits 0.

## Lineage result for the coordinator

PR 1216 (OPEN, `docs/paper-scientific-reconciliation`, `50f776c3`, base main) is an unrelated paper PR, not an ancestor of this branch or of main, and touches neither test file. It is not this candidate or part of its stack. A future publication is a new PR from `test/assistant-process-races-107` to main with `Refs #107` and `Refs #104`. PR 1216 was not modified.

## Light results (fresh external venv `/mnt/ama-gates/g107-process-races-currency-1108/venv`, external caches, PYTHONDONTWRITEBYTECODE=1, unmasked exits)

* `pip install -e src/core -e src/agents -e "src/api[dev]"` exit 0; the three generated ignored egg-info folders were moved by explicit path to `.../egg/`; import origin is this worktree.
* `python -m unittest -v test_assistant_release test_assistants test_continuity` from `src/api` with `PYTHONPATH=tests:../core/tests:../agents/tests`: exit 0, 194 tests OK, 61 skipped. The three `SqliteUnleasedRevocation` methods, including both process cases, are `ok`; all three `MssqlUnleasedRevocation` methods are skipped (`ZF_TEST_MSSQL=1` absent).
* `ruff check .` exit 0; `mypy` exit 0. No orphan worker processes.

## Unrun gaps

The SQLite results are a proxy, not MSSQL process evidence. Not run: actual MSSQL, Docker or images, browser, scanners, the FULL runner, independent exact-head review and hosted gates. Human approvals, attestation and live-model or Azure evidence remain open and whole 107 and 104 are not accepted.

## Resume plan (future, after one nonqueued admission)

Fetch main; if it moved, one normal merge. Read the then-current `tools/rpi-checks.py` and `src/README.md`. Run `python3 tools/rpi-checks.py --all --base <fresh origin/main> --out <new external dir> --jobs 2 --lock-timeout 0 < /dev/null`. No `--extra-test` is used (it would skip without `ZF_TEST_MSSQL=1`). The SQL log must show `MssqlUnleasedRevocation.test_racing_processes_cannot_overspend_or_replenish_a_finite_allowance` and `MssqlUnleasedRevocation.test_processes_after_revocation_and_restart_are_denied_without_calls_or_replenishment` as `ok`. Verify the receipt with the runner against exact current main; commit nothing afterwards.
