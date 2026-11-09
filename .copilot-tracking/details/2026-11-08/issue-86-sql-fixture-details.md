---
title: Issue 86 resident-control SQL fixture correction details
description: Exact selectors, environment and evidence layout for the later baseline and regression
ms.date: 2026-11-08
---

* Evidence directory (new, not yet created): `/home/azureuser/.local/share/ama/gates/g86-fixture-<ts>/`; `.out`, `.err`, `.exit` per command; raw outputs preserved.
* Main baseline tree: `git archive origin/main` into `main/`; candidate tree: `git archive HEAD` into `cand/`; venvs `venv-main` and `venv-cand`, each with `pip install --require-hashes -r src/api/requirements.txt` then non-editable `pip install --no-deps src/core src/agents src/api` from that tree; import-origin and file-hash proof per venv; no repository-source `PYTHONPATH` except the tests directory.
* Method selector: `tests.test_resident_decisions.MssqlResidentControls.test_challenge_edited_in_case_outside_generation_candidates`, run from `<tree>/src/core` with `ZF_RESIDENT_MSSQL=1` and the synthetic SQL variables used by the earlier focused run (`ZF_SQL_SERVER=127.0.0.1`, mapped port, `ZF_SQL_AUTH=password`, `ZF_SQL_USER=sa`, `ZF_SQL_TRUST_CERT=1`, throwaway password by environment only).
* Regression selectors: the same method on `JsonResidentDecisions` and `SqlResidentDecisions`; `-k challenge` on the three classes; `tests.test_seed_merge`; whole `MssqlResidentControls`.
* Container: one, `--memory=3g --cpus=2 --publish=127.0.0.1::1433`, owner label, inside `flock -n /tmp/ama-rpi-heavy.lock`; endpoint ownership checks; remove only the owned container.
* Counting: use the unittest `Ran N tests` and `OK`/`FAILED` lines; list skips and failures by name; `... ok` line counts are not totals.
* Static: `mypy` and `ruff` on the touched test file only.
