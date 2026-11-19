# Changes: issue 121 live run (2026-11-19)

No source change; documentation-only candidate (FOCUSED tier). Refs #121.

Stop line: every remaining unticked criterion is production-only (DPO/Legal, #1906 to #1908) or needs a redeploy/state change the owner excluded for the demo.

| Criterion | Status | Basis |
| --- | --- | --- |
| Map staff/tenant identities and review records separately | Proven offline; live partly | `subject_populations` in `data_protection.py`; deployed image predates it |
| Cover inputs, bytes, prompts, outputs, citations, reviewer identity, audit, telemetry, tokens, provider processing, retained copies | Proven offline; live partly | `WHOLE_SYSTEM_SURFACES`, `test_whole_system_inventory_covers_all_nine_actual_classes_and_surfaces` |
| Every task declares purpose, fields, prohibited content, necessity | Proven offline | `TASKS`, `validate_task_payload`, tests in `test_data_protection.py` |
| DPO/Legal and record owner approvals | Unproven: production-only | Human approval, #1906 |
| Upload permission is not AI dispatch approval | Proven offline; live unproven | `model_dispatch`, `document_model_hold`; live needs an upload (state change) |
| Retention, erasure, audit, restore explicit and owned | Partly proven; ownership production-only | See 2026-11-18 note |

Validation: no executable change, so no unit/mypy/ruff run; none applicable. Hosted CI not observed.
