---
title: Issue 86 focused-tier changes and evidence
description: Actual focused SQL run results after the interrupted FULL, with an adverse core MSSQL failure preserved
ms.date: 2026-11-08
---

Scope: issue #86 only. No production, test, tool or infra bytes changed. Prospective records were committed first as `5b107971` (tree `f4b8d3c5`); `src`, `tools`, `infra` and `.github` trees equal `40ec31e2`. Main `0f05e9aa`, parent ref `c5edb320` fetched with no drift.

## Interrupted FULL (preserved, not a pass)

`/home/azureuser/.local/share/ama/gates/g86-main0f-r1` was interrupted by SIGTERM 15 in the `mssql` group (receipt sha256 `dfa60d46...dea9`). Its eleven executed groups are historical same-code observations only.

## Focused SQL run (manual, not a runner receipt)

* Evidence: `/home/azureuser/.local/share/ama/gates/g86-focused-sql-1108/` (script `../g86-focused-sql-1108.sh`, console and `.exit` beside it, exit 0 for the script).
* Lock: `flock -n /tmp/ama-rpi-heavy.lock` acquired; no holder, no containers before or after. One owned container (label `ama.rpi.owner=g86-focused-1108`, loopback port bound, removed, exit 0). Image was already local; no pull.
* Environment: hash-locked `src/api/requirements.txt` (exit 0), non-editable install of core, agents and api from a `git archive` of HEAD, driver probe exit 0. Import origin: `zava_forward.core.mssqlstore` resolves into the evidence venv site-packages; `api` and `agents` are namespace-style so only core origin was provable by `find_spec`.
* Maintained `SQL_SELECTORS` from `src/api`: 301 tests, OK, 288 `ok`, 1 skip (`MssqlHazardReferral.test_json_postsave_audit_failure_reports_persisted_uncertainty`, JSON-only audit ordering), 0 failures, exit 0. `MssqlUnleasedRevocation` ran 3 tests, all ok.
* Core `MssqlResidentControls` with `ZF_RESIDENT_MSSQL=1`: 108 tests, 103 `ok`, 1 skip (`test_json_followup_failure_restores_record_and_ledger`, JSON file rollback only), **1 FAIL**, exit 1.

## Adverse result

`test_challenge_edited_in_case_outside_generation_candidates` failed at `test_resident_decisions.py:1262`: `4 != 40`. The test seeds 41 extra cases by writing a JSON file, which the MSSQL-backed store does not reload. The test body is byte-identical to Main `0f05e9aa` and `c5edb320` and is not in the maintained `SQL_SELECTORS`, so no maintained gate runs it. This is assessed as a pre-existing test/fixture incompatibility, not caused by the child, but that is not proven by a Main-side run. No edit was made.

## Not covered

No FULL, images, scans, logo or browser rerun. Resident complaint HTTP tests use SQLite; MSSQL ranking/export API paths are not claimed. Cross-process, multiuser, real receiver, model, legal, resident and AT approval, and #1238 remain open.
