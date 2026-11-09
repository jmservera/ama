---
title: Issue 86 resident SQL fixture baseline observations
description: Actual B1 and B2 single-method baseline results; observations kept separate from diagnosis
ms.date: 2026-11-08
---

Scope: issue #86 only. Baseline only; no test, helper, production or tools edit. Head `4afe52e4`, tree `3dcc6c91`; Main `0f05e9aa`; parent ref `c5edb320`; PR 1243 open, base `feat/controlled-lifecycle-integration-81`, head `6ff492ad`. No drift.

## Run

* Runtime: `/home/azureuser/.local/share/ama/gates/g86-fixture-baseline-r1/` (script, console and exit beside it; script exit 0). Canonical lock held non-blocking for the whole lifetime; one owned container (label `g86-fixture-baseline-r1`, loopback port 33293, 2 CPU, 3 GB); removed, exit 0; no containers afterwards. No pull, no prune.
* Two fresh venvs from `git archive` of `origin/main` and of HEAD; hash-locked API requirements and non-editable core, agents, api installs all exit 0; driver probe exit 0.
* Origins: test module and `dataset` from each tree's `src/core/tests`; `zava_forward.core.mssqlstore` and `sqlstore` from each venv site-packages. `PYTHONPATH` was only that tree's `src/core/tests`, run from `src/core`.
* Hashes: `dataset.py` identical in both (`a54612aa...`); `test_resident_decisions.py` differs (Main `30f049e6...`, candidate `9213851d...`) as expected because the child adds tests.

## Observations

| Run | Method | Result | Exit |
| --- | --- | --- | --- |
| B1 Main tree and Main packages | `MssqlResidentControls.test_challenge_edited_in_case_outside_generation_candidates` | Ran 1 test, FAILED (failures=1), `AssertionError: 4 != 40` at line 1261, no skips or errors | 1 |
| B2 candidate tree and candidate packages | same | Ran 1 test, FAILED (failures=1), `AssertionError: 4 != 40` at line 1262, no skips or errors | 1 |

Both executed the intended test unskipped, so both are conclusive observations. B3 was not run.

## Diagnosis (separate from observation)

The failure reproduces on Main packages with Main's own test, so it is not introduced by the child. This confirms Main reproduction only; it does not by itself prove the fixture root cause, which the later unskipped regression must show. No production defect is claimed. The run used a normal database, not Azure SQL ledger tables. The earlier author Medium finding and the interrupted FULL are unchanged.

## Next bounded scope

Separate coordinator admission for the test-only seeding correction (plan steps 4-7), then regression. No CI or selector change.
