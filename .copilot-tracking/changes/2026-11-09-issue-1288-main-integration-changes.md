<!-- markdownlint-disable-file -->
# Release Changes: #1288 ordinary main integration

Plan: [plan](../plans/2026-11-09-issue-1288-main-integration-plan.md). Details: [details](../details/2026-11-09-issue-1288-main-integration-details.md). Research: [research](../research/2026-11-09-issue-1288-main-integration-research.md). Plan, research and details committed (69d1a0c30) before the merge. Refs #1288 only.

## Change

* Ordinary no-ff merge of fetched origin/main cd687abadd9d18befe19089e65ba7373771b767f (PR #1328) into the run-owned branch. Parents: 8e3fda601 (candidate with plan records) and cd687abad. No rebase, amend, force or push. Auto-merged server.py and core/README.md with no conflict.
* No source edit by this run. E8 is not consumed; E1-E7 spent, E8-E10 remain.

## Source and config input comparison

* Merged delta in src/infra versus candidate 84b1a6d06 is exactly main's 19 paths (infra 7, core 8, api 2, core tests 4 incl. new fixture). Main-owned paths (ranking*.py, store.py, infra, ranking tests, wiring test) are byte-identical to main. Main did not change any pyproject.toml or .github file since the merge base 5c3b8b4be, so the lint, format and mypy inputs are the candidate's own.
* The only shared files are server.py (main: one hunk in the `/api/ranking/publish` handler adding `ArchiveWriteUncertainError`; candidate: simulation lane, quality, inventory routes) and core/README.md (additive both sides). Both intents are preserved. Main's store.py and ranking*.py do not touch the candidate's AI, transport, lane, assistants or consumption modules.

## Fresh runs at the merged HEAD (raw logs in session files/logs-1288-main-integration/)

* Core SDK-free (owned mktemp venv, `-e src/core[dev]`): ruff check 0, format 0 (229 files), mypy 0 (282 files). API (`.venv-1288`, azure-storage-blob 12.31.0): ruff check 0, format 0 (134 files), mypy 0 (211 files). Pinned ruff 0.17.1, mypy 2.4.0.
* Core: ranking_archive_blob 26 OK, ranking_publication 57 OK, ranking_publication_runner 53 OK, ai_consumption 42 OK, ai_input_bounds 6 OK, sensor_consumer 47 OK.
* API: ranking_publication_wiring 36 OK, quality_simulation_lane 30 OK, ai_transport_deadline 7 OK, role_endpoint_inventory 23 OK, ai_call_site_inventory 6 OK, ai_consumption_api 17 OK, assistants 120 OK (58 skipped: needs disposable SQL Server ZF_TEST_MSSQL=1), assistants_dispatch 2 OK, assistant_release 54 OK (4 skipped), quality_sensors_c7 45 OK (7 skipped), quality_sensors_e2 62 OK (31 skipped), ai_tasks 69 OK.
* Infra: `infra/tests/test_bicep_policy.py` 59 OK (offline).
* Skips other than assistants were not re-derived here; they are the same suites and counts as the E7 runs at 2c2fc7298.

## SQL qualification

No SQL was run. Main changes no SQL schema, assistants, admission or sensor code, and the ranking tests have no SQL Server dependency (grep of the ranking, wiring and bicep tests for SQL markers is empty). The SQL605/1skip and Core53 result at 5827ebede remains HISTORICAL and is not final-head SQL. The 58 assistants SQL skips are not exercised. If final audit-persistence SQL evidence is required, the selectors are the assistants SQL selectors plus the E6 refused-send persistence case, under one non-queued `flock -n /tmp/ama-rpi-heavy.lock` admission.

## Limits

* Real-provider simulation route remains code-disabled (test_quality_simulation_lane and inventory green on the merged tree). No provider call, credential, deployment, financial activation or role grant.
* Residuals unchanged: ordinary-assistant post-fence suspension race; socket shutdown is local only; final SQL audit-persistence is not proven at this head. No browser or Blob-emulator run: Blob behaviour was verified only through main's own unit tests, not against a live or emulated Azure service.
* Whole #1288 and actual-model demo acceptance are not claimed.
