<!-- markdownlint-disable-file -->
# RPI Changes: Issue #163 Explicit Deployment Attestation in Actual Mode and IaC Mismatch Disclosure (Cycle 4)

## Metadata

* Task ID: issue-163-chat-privacy-region-c4
* Parent Task ID: issue-163-chat-privacy-region-c3
* Date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/issue-163-chat-privacy-region-c4-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-c4-phase-details.md
* Declared scope: Full plan (`P01`)
* Implementation status: Complete

## Active Execution Summary

Completed full-plan implementation (`P01-T01` and `P01-T02`), closing Cycle 3 review finding `RV-001` and Cycle 4 critique item `PC-001` and reconciling all artifacts before Cycle 4 `rpi-review`.

## Completed Work by Plan Area

### Actual-Mode Deployment Attestation and IaC Mismatch Disclosure (`P01-T01`)

* `src/core/src/zava_forward/core/chat_provider_position.py`:
  * Added `deployment_attested: bool` to `ProviderPositionEvaluation` and `"deployment_attested": False` to `MODEL_PROVIDER_CONTRACT` (mirrored on `chat_privacy.MODEL_PROVIDER_POSITION`).
  * Updated `evaluate_provider_position()` so `deployment_attested` is `True` only when both region (`region` arg or `CHAT_PROVIDER_REGION`) and deployment SKU (`deployment_type` arg or `CHAT_DEPLOYMENT_TYPE`) are explicitly supplied and resolve without `"unapproved_region"` or `"unapproved_deployment_residency"` (`PC-001`, ensuring `uksouth` + `DataZoneStandard` reports `deployment_attested = False`).
  * Kept `constructed`-mode synthetic fallback (`uksouth` / `Standard`, `deployment_attested = False`) for `#281` unit fixtures and `#891` synthetic demo, while requiring explicit `CHAT_PROVIDER_REGION` and `CHAT_DEPLOYMENT_TYPE` whenever `ZF_DATA_PROCESSING=actual` (`"unattested_region_in_actual_mode"`, `"unattested_deployment_in_actual_mode"`) so `actual` mode fails closed against `infra/main.bicep`'s current `chatModelSku = 'GlobalStandard'` default (`RV-001`).
* `src/core/README.md` and `docs/reference/research/chat-memory-dpia.md`: Documented `deployment_attested`, the actual-mode attestation violations (`unattested_region_in_actual_mode`, `unattested_deployment_in_actual_mode`), and the current `infra/main.bicep` `chatModelSku = 'GlobalStandard'` / `infra/modules/containerapps.bicep` mismatch while leaving `infra/` untouched under Focused scope.

### Unit Assertions and Focused Validation (`P01-T02`)

* `src/core/tests/test_chat_provider_position.py` (`13` test methods, `0` removals, `0` new methods): Expanded `test_default_uksouth_standard_position_is_valid_and_not_dpo_accepted`, `test_uksouth_rejects_datazone_standard_because_uk_outside_eu_data_zone`, `test_actual_data_mode_rejects_synthetic_and_demo_references`, and `test_regulatory_privacy_readiness_and_foundry_query_enforce_provider_position_no_echo` to assert `MODEL_PROVIDER_CONTRACT["deployment_attested"] is False`, `MODEL_PROVIDER_POSITION["deployment_attested"] is False`, `deployment_attested` transitions (`False` when defaulted or on `uksouth` + `DataZoneStandard`; `True` when `uksouth` + `Standard` are both explicitly set), and `"unattested_region_in_actual_mode"` / `"unattested_deployment_in_actual_mode"` across `evaluate_provider_position`, `readiness_report`, and `build_foundry_query`.

## Discoveries, Amendments, and Divergences

* Local judgment (`ruff format`): Applied `ruff format` to `chat_provider_position.py` (`100`-character line width). No plan amendments or divergences occurred.

## Validation Evidence

* `cd src/core && python3 -m ruff check && python3 -m ruff format --check && python3 -m mypy`: Passed (`All checks passed!`, `310 files already formatted`, `Success: no issues found in 363 source files`).
* `cd src/api && python3 -m ruff check && python3 -m ruff format --check && PYTHONPATH=../core/src:../agents/src python3 -m mypy`: Passed (`All checks passed!`, `216 files already formatted`, `Success: no issues found in 300 source files`).
* `cd src/core && PYTHONPATH=src:tests python3 -m unittest tests/test_chat_provider_position.py tests/test_chat_privacy.py tests/test_chat_dpia_record.py tests/test_regulatory_privacy.py tests/test_regulatory_privacy_audit_217.py -q`: Passed (`Ran 81 tests in 10.567s — OK`).
* `cd src/api && PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest tests/test_chat_panel.py tests/test_content_standard.py tests/test_accessibility_baseline.py -q`: Passed (`Ran 122 tests in 37.326s — OK (skipped=1)`).
* `python3 tools/rename-zava-tests.py`: Passed (`Ran 25 tests in 0.540s — OK`).
* `git --no-pager diff --check`: Passed (exit code `0`).
* `tools/rpi-checks.py --all`: Intentionally skipped per caller instruction (`Validation tier: Focused`).

## Blockers and Remaining Work

* Blockers: None.
* Remaining in-scope work: None (`P01-T01` and `P01-T02` complete).
* Follow-up items outside active scope:
  * Named human DPO and Legal review and sign-off on `D1` to `D8` in `docs/reference/research/chat-memory-dpia.md` (`Refs #163`).
  * Separate Full-tier IaC PR aligning `infra/main.bicep` `chatModelSku` and injecting `CHAT_PROVIDER_REGION` and `CHAT_DEPLOYMENT_TYPE` in `infra/modules/containerapps.bicep` after DPO/Legal `D6` confirmation.
