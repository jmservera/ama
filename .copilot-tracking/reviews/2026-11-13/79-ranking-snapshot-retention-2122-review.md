# Review: #79 criterion 4, scheduled ranking publication

Date: 2026-11-13. Review executed once, after implementation. Boundary: the diff against origin/main `ee068a4b5`. Outcome: conformant for the software and template proof; no material finding open. Tier: focused.

## Validation (isolated pip venv, removed afterwards)

| Check | Result |
| --- | --- |
| `src/orchestrator` unit tests (125, includes 10 new) | OK |
| `src/orchestrator` ruff check, ruff format --check, mypy strict | pass |
| `infra` unit tests (515) incl. updated `test_bicep_policy` and the new job test | OK except `test_pipeline` import error, which also errors on unmodified main |
| `az bicep build` of `infra/main.bicep` | pass |
| `src/core` tests (3196) | only 50 failures/errors, all in `test_device_registry_azure` (optional Azure IoT SDK not installed); no ranking test failed; core unchanged |
| `src/agents` tests (415) | OK |
| `src/api` tests (2995) | only 10 import errors for browser harness modules (playwright not installed); api unchanged |
| `test_ai_call_site_inventory` | OK |
| core, agents, api ruff and format | pass |
| core, agents mypy | pass |
| api mypy | 66 errors, all missing optional imports and pre-existing; api unchanged |

## Findings

* Criterion 4 proof in software: scheduled job (template), store-sourced cases, Blob create-only retained records, no overwrite or delete, deterministic mock-Blob tests, idempotent repeat. Evidence is a mock transport and compiled template only; no deployment, job run, approved retention duration or locked immutability policy.
* Criterion 3 honesty: the shipped policy remains an unsigned draft; a test asserts the job refuses it and writes nothing. No signature was added.
* Open, routed later: a log-query missing-run alert (critique PC-005 follow-up); owner approval and locking of the retention duration; named policy owner signature (criterion 3); a real deployment observation. The issue checkbox for criterion 4 should not be ticked on this evidence alone.
