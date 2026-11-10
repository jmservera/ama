---
title: Issue 109 prospective local integration changes
ms.date: 2026-11-10
task_id: 109-prospective-integration-1110
---

## Status

Prospective declaration written before `implement-start`; actuals recorded at implement-done.

## Planned changes

* One ordinary no-fast-forward merge of `origin/main` (`c66370042eb08f07839d054433f4483078703cf2`) and child `6b0ba7b14f9985cddd0d8cbc8ad27430c9acb9d2` into the local topic, committed once with the dated tracking records.
* Planned new tracking files: the research, plan, details, critique, changes, review and state records of task `109-prospective-integration-1110`.
* No authored product, test, configuration, workflow or dependency change.

## Amendment before implement-start (additive)

At the pre-implement recheck `origin/main` had advanced from `c66370042eb08f07839d054433f4483078703cf2` to `1290aa557660213f6511de054d2c69db167187f3` (one commit, #1399 docs Registry-wave checkpoint: 17 files, only `.copilot-tracking` records plus `docs/architecture/cutover-evidence-pack.md`, `docs/reference/README.md`, `log.md`; zero src, infra, tools, .github, BRD, PRD or ADR paths). Root asked for freshly fetched main, so this is the fresh main and the merge uses `1290aa557660213f6511de054d2c69db167187f3`. Dry run `git merge-tree` of main with child exits 0 (tree `acf5dff4a0d3d30db478cf78058ee4ae6457dec3`), HEAD with main exits 0 (tree `7cd89fd2df80835e9b43e6d0ddae49c042a33829`). Plan pins of `c66370042` are superseded by this identity; the child pin is unchanged.

## Actuals (implemented-unverified, PROSPECTIVE local composition)

Merge: `git merge --no-ff --no-commit origin/main 6b0ba7b14f9985cddd0d8cbc8ad27430c9acb9d2` from HEAD `a3d5e615f0b2617b40cd5bdd23d00db0be11284e` with main `1290aa557660213f6511de054d2c69db167187f3`; no conflict, zero unmerged paths; staged tree `02888b15e3d567a1cb48f9a0632b76bda02cb3c7` (73 staged files). Not committed at implement-done. Not the remote parent, not main, not the PR #1395 merge.

Invariants: every staged non-tracking path equals the child blob or the main blob except `src/core/pyproject.toml`, the only overlap, merged automatically: it keeps main's `iothub` extra and `dev` pins (`azure-iot-hub==2.7.0`, `six==1.17.0`) and the child's scoped `disallow_untyped_calls = false` stanza (3 insertions, 1 deletion versus child; 6 insertions versus main); the older exemption groups are unchanged. API test suppression line present once. No source authored.

Checks (raw logs, scripts and true exits under `ROOT/checks-109-prospective-integration-1110/`; owned venv `/tmp/z109-pi-1110/venv`, import origins proven inside this worktree):

* Core `tests.test_sensor_review_draft`: 65 run, 22 opt-in skips (not SQL passes), exit 0. `test_sensor_analysis` 11 OK, `test_sensor_analysis_store` 9 OK, `test_scenario_manifest` 8 OK.
* `test_device_registry_azure`: first run failed (missing `azure` module in the new owned venv, preserved in `03-core-tests.test_device_registry_azure.txt`); after pinned installs into the owned venv, 39 OK.
* API `tests.test_sensor_review_draft_api`: 6 run, 0 skips, exit 0.
* Core ruff, format check and configured mypy: pass (292 source files). API ruff and format: pass. `node --check ops.js`: exit 0.
* API configured mypy: first run red (4 errors in `tests/test_ai_consumption_api.py`, `import-not-found` for `zava_forward.agents.*`, caused by the owned venv lacking the editable agents install; preserved in `09-api-mypy.txt`); after `pip install --no-deps -e` of core, agents and api in the owned venv, green on 221 files (exact legacy `App` call suppression disclosed; not strict typing of `App`).
* Actual sensor browser check, one `flock -n` attempt, short owned cwd `/tmp/z109b.p78T` (removed): 33 checks passed, exit 0; unchanged check, local mock provider, synthetic fixtures; stderr only client-disconnect noise.
* Fresh scoped MSSQL `MssqlDraftCases`, one `flock -n` attempt, own disposable `mssql/server:2022-latest` container (removed): 22 run, 0 skips, OK. Local synthetic SQL only, not Azure SQL.
* Not run by design: full source discovery, full gate, `--changed`, images, cloud, provider, private data.

Gaps carried: unforced `ConflictError` and `CommittedReloadError`; scoped Core mypy exemptions; API `App` suppression; Core opt-in skips; no WCAG, assistive-technology, Azure Hub, Azure SQL, live UI or model acceptance; no independent review of this composition; PR #1395 hosted CI for the new head not final.
