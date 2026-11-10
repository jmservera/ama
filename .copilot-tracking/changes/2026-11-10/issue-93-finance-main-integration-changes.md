---
title: Issue 93 finance main integration changes
description: Actual merge, byte-identity and targeted validation observations for the finance integration at the merged tree
ms.date: 2026-11-10
---

Observed 2026-11-10T01:01Z to 01:05Z, after the prospective records were committed (`05aaca608`). Plan: [plan](../../plans/2026-11-10/issue-93-finance-main-integration-plan.md). Raw logs: `/tmp/issue93-finance-main-1110/logs/` (outside the tree; 16-hex SHA-256 prefixes below).

## Changes made

* No product, test, config, README, log or shared-hook edit by this task. Only ordinary merges and tracking records.
* Fast-forward of the local branch ref from `0472fd5d` to the brief pin `4642b55f` (ancestor; no reset or rebase).
* Merge 1 `9fce46fb4`: `test/demo-finance-parent-440-1110` (`ef63d180`), clean, tracking only, seven records preserved.
* Merge 2 `fff8cbe25`: main pin `5318f738f6bc58a10a9d4df1ca18ae51c1547a79`, clean, no conflicts, so no README or log resolution was needed. Both append-only documentation histories are preserved by the textual merge.
* Merged tree before these records: `90822736d2e85a81e1e72ed6a14d09ab1ae1e7c8`.

## Byte guards (all pass)

* Six finance product blobs at the merged tree equal the finance `4642b55f` blobs (`forms.py` `c01ca735`, `form_review.py` `65427853`, `form_export.py` `bf07132e`, `test_form_dependencies.py` `306ad5c3`, `test_form_export.py` `e958edb7`, `test_form_review.py` `76b3169f`). The seventh product file, `src/core/README.md`, differs from main by `39 added, 7 removed`, exactly the parent's own numstat against the merge base, and all seven removed lines exist in the merge base.
* `server.py` blob `187c3648` and `test_form_staging_api.py` blob `eec669fb` equal main. Non-documentation diff versus main lists only the six finance source and test files.
* `docs/reference/log.md` differs from main by 3 added lines, 0 removed. The seven `issue-440-finance-parent-verification` records are byte-identical to `ef63d180`.

## Environment (isolated, external)

* `/tmp/issue93-finance-main-1110/venv`, Python 3.12.3. Hashed `src/build-requirements.txt` (packaging 26.3, wheel 0.48.0, setuptools 84.2.1), then `pip install --no-deps --no-build-isolation -e src/core -e src/agents -e src/api` (all `0.1.0`). `direct_url.json` for core, agents and api is `file:///home/azureuser/source/ama-demo-wt/issue-93-finance-main-1110/src/{core,agents,api}` with `editable: true`. `forms`, `form_review`, `form_export` and `api.server` resolve under that worktree. Test module paths resolve under the worktree and the blobs of `test_form_export.py` and `test_form_staging_api.py` equal the merged tree.
* Tools `ruff==0.17.1`, `mypy==2.4.0`. After a recorded missing-dependency failure, `playwright==1.64.0` (the API dev pin, Python package only, no browser) and the hashed `src/api/requirements.txt` (`--no-deps`; includes `aiohttp==3.14.5`, `azure-identity==1.26.0`, `mssql-python==1.15.0`) were installed. Install used network for package download only; no SQL connection, Azure, model, provider or private data. No `uv`, global install or source-path hack. `PYTHONDONTWRITEBYTECODE=1`, external mypy cache, Ruff `--no-cache`; `git status --short --ignored` was empty after every step.

## Observations

| Id | Command (cwd) | Exit | Result | Log |
| --- | --- | --- | --- | --- |
| A0 | `python -m unittest tests.test_form_export...` (`src/core`) | 1 | Adverse, wrong invocation: tests import flat sibling modules, class name was `FormExport`. Not a product failure; preserved | `1c12c4a9` |
| A | `PYTHONPATH=tests python -m unittest -v test_form_export.FormExport.test_export_carries_ordered_detached_review_history ...test_history_is_integrity_covered_and_legacy_copy_is_invalid` (`src/core`) | 0 | 2 tests OK, 0 skips | `33ce5e33` |
| B | `PYTHONPATH=tests python -m unittest -v test_form_dependencies test_form_review test_form_review_pack test_form_export test_form_staging` (`src/core`) | 0 | 67 tests OK, 0 skips (A's two are inside these 67) | `32b3e93f` |
| C | `PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest -v test_form_staging_api` (`src/api`) | 0 | 14 tests OK, 0 skips; module has 14 `def test`, including main's schema-CSV tests (empty list, denials, revocation, formula neutralisation) | `e85e13a7` |
| D1 | `python -m mypy` (`src/core`) | 0 | Success, 284 source files | `6261ed61` |
| D2a | `python -m mypy` (`src/api`) | 1 | Adverse: 70 errors, all `import-not-found` for `playwright` | `f4554ae0` |
| D2b | same, after `playwright==1.64.0` | 1 | Adverse: 20 errors in main-owned files: 18 `import-not-found` for azure and `mssql_python`, and 2 `unused-ignore` in `live_simulator.py` lines 142 and 154 that arise only while those stubs are missing (clear in D2c) | `4ec28b9d` |
| D2c | same, after hashed `src/api/requirements.txt` | 0 | Success, 211 source files | `7eb4120d` |
| E1 | `python -m ruff check --no-cache` on the six Core product paths (`src/core`) | 0 | All checks passed | `82b3e6a6` |
| E2 | `python -m ruff format --check --no-cache`, same paths | 0 | 6 files already formatted | `ef7d13d0` |

Unique executed tests: 67 Core (including the 2 history tests) plus 14 main API, 81 unique; the A rerun makes 83 executions. Skips: 0. The earlier parent-only observation (74 unique) is history and is not reused: the API module now holds 14 tests, not 7. `src/core/README.md` is Markdown and has no Ruff gate; docs were reviewed by diff only.

## SQL and MSSQL determination

* The parent delta touches no `sqlstore`, `mssqlstore`, schema, infrastructure or store path; it reads `store.data` read-only and adds no persisted key.
* No MSSQL or `sqlguard` backed test names form review, history, staging or export in the merged tree (search of test and check files that mention `mssql`, `sqlguard` or `mssql_python`). Only the generic `form_schemas` document name appears in `sqlstore.DOCS`.
* Result: absent MSSQL form and history contract; reported as absent, not as a pass. SQL not materially impacted, so no shared-heavy-resource admission, no SQL service and no SQLite substitution claim. The history contract remains observed only on the in-memory JSON store; MSSQL behaviour is unobserved.

## Deviations and divergences

* The branch ref was fast-forwarded from the stale `0472fd5d` to the brief pin before the loop; recorded in research.
* The original author of the preserved verification records created them through shell heredocs; preserved as a process deviation. This task wrote its records with the editor tool.
* Corrections used: 0 of 5 total review-correction cycles.
