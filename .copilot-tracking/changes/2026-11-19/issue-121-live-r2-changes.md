# Changes: issue 121 live r2 (2026-11-19)

No source change; documentation-only (FOCUSED tier). Refs #121.

Stop: every remaining unticked criterion is production-only or needs an owner-excluded redeploy/upload.

| Criterion | Status | Basis |
| --- | --- | --- |
| Map staff/tenant identities and review records separately | Proven offline; live unproven this run | `subject_populations`; 32 tests OK; 2026-11-18 note |
| Cover inputs, bytes, prompts, outputs, citations, reviewer identity, audit, telemetry, tokens, provider processing, retained copies | Proven offline; live unproven this run | `WHOLE_SYSTEM_SURFACES` and its coverage test |
| Every task declares purpose, fields, prohibited content, necessity | Proven offline | `TASKS`, `validate_task_payload` tests |
| DPO/Legal and record owner approvals | Unproven: production-only | Human approval, #1906 |
| Upload permission is not AI dispatch approval | Proven offline; live unproven | `model_dispatch`, `document_model_hold`; live needs an upload |
| Retention, erasure, audit, restore explicit and owned | Partly proven; ownership production-only | `RightsRequestLedger`, retention tests; owners need Legal |

Validation: `cd src/core && PYTHONPATH=src:tests python3 -m unittest tests.test_data_protection -q` gives 32 tests OK. mypy/ruff not applicable (no executable change). Hosted CI not observed.
