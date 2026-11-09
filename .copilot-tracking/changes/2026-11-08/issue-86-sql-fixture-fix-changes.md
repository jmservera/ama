---
title: Issue 86 resident SQL fixture correction changes
description: Test-only seeding correction and its focused evidence
ms.date: 2026-11-08
---

Scope: issue #86 only. Plan amendment committed first as `f3ec2224`. Baseline `f5309e5b` (B1 Main and B2 candidate both failed `4 != 40`) is preserved.

## Change

One file, `src/core/tests/test_resident_decisions.py` (+18/-2): a `seed_extra_cases(count)` helper on `JsonResidentDecisions` keeps the write-new-file-and-reopen flow for JSON and SQLite; `MssqlResidentControls` overrides it to write a cases-only seed, call public `merge_seed(apply=True, expect_added=count)`, assert `to_insert == count` and `applied`, then reopen. Only `test_challenge_edited_in_case_outside_generation_candidates` uses it (41 cases). All assertions and skips unchanged. Production, tools, infra and .github untouched.

## Evidence (`/home/azureuser/.local/share/ama/gates/g86-fixture-fix-r1/`)

Canonical lock held non-blocking; one owned container (2 CPU, 3 GB, loopback), removed exit 0, none remain. Fresh venv with hash-locked requirements and non-editable core, agents, api; test module and dataset from the snapshot, installed core from the venv.

| Check | Result |
| --- | --- |
| Method on Json, Sql, Mssql classes | Ran 3, OK, no skips, exit 0 |
| `-k challenge` on the three classes | Ran 45, OK, exit 0 |
| `tests.test_seed_merge` | Ran 21, OK, exit 0 |
| ruff check / format check (touched file) | exit 0 / exit 0 |
| mypy (core project) | 269 files, no issues |

`merge_seed` on MSSQL passed with exactly 41 inserted, which resolves the earlier unproven behaviour for this fixture. Normal database append-only trigger only, not Azure SQL ledger tables. Whole 108 and API 301 were not rerun (owner CI-first scope). The fixed unskipped regression supports the fixture root cause; no production defect is claimed.
