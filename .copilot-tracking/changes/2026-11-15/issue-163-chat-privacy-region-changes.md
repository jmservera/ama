<!-- markdownlint-disable-file -->
# RPI Changes: Issue #163 Model Provider Data-Handling and Region Position Contract

## Metadata

* Task ID: issue-163-chat-privacy-region
* Related plan: .copilot-tracking/plans/2026-11-15/issue-163-chat-privacy-region-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan
* Completed scope markers: P01, P01-T01, P01-T02, P02, P02-T01, P02-T02, P03, P03-T01, P03-T02
* All remaining active-plan markers: none
* Status basis: All planned phases and tasks (`P01` through `P03`) completed with verified focused unit test, linter, formatter, strict `mypy`, and documentation hygiene evidence.

## Execution Summary

Delivered the Issue #163 model provider data-handling and region position contract across `src/core`, `/api/chat/status`, and canonical privacy documentation while preserving the human DPO/Legal sign-off gate (`D1`–`D8` `"Not recorded"`, `dpo_legal_approved: False`). Implemented strictly typed fail-closed residency, SKU, zero-training, synchronous content-filtering vs 30-day abuse-monitoring disclosure, cross-border transfer, `ZF_DATA_PROCESSING=actual` synthetic/demo reference rejection, and pre-approval retention controls, backed by deterministic unit tests and zero-error `ruff` and `mypy` verification.

## Completed Work

### Enforceable Provider Data-Handling and Region Contract (`P01`, `P01-T01`, `P01-T02`)

* Created strictly typed `src/core/src/zava_forward/core/chat_provider_position.py` defining `PRIMARY_UK_REGION = "uksouth"`, bounded EEA `EU_DATA_ZONE_REGIONS`, `APPROVED_DEPLOYMENT_TYPES` (`Standard`, `DataZoneStandard`), `PROHIBITED_DEPLOYMENT_TYPES` (`GlobalStandard`, `GlobalBatch`, `GlobalProvisionedManaged`), separate `CONTENT_FILTERING_DISCLOSURE` and `ABUSE_MONITORING_DISCLOSURE` contracts, `MODEL_PROVIDER_CONTRACT`, `is_demo_or_synthetic_ref()`, `is_valid_governance_ref()`, `evaluate_provider_position()`, `require_provider_position()`, and `ProviderPositionError`.
* Scoped `DataZoneStandard` exclusively to `EU_DATA_ZONE_REGIONS` (rejecting `DataZoneStandard` on `uksouth` as `unapproved_deployment_residency`), derived `cross_border_transfer=True` unconditionally whenever `region != "uksouth"`, enforced zero-training (`CHAT_PROVIDER_TRAINING` / `customer_data_training`), and rejected bare placeholder tokens (`"yes"`, `"true"`, `"approved"`) in all modes plus `SYNTH-*`/`SYN-*`/`SYNTHETIC-*`/demo/draft Markdown references under `ZF_DATA_PROCESSING=actual`.
* Integrated `chat_provider_position` into `src/core/src/zava_forward/core/chat_privacy.py` (preserving legacy `MODEL_PROVIDER_POSITION` keys while adding structured residency/handling fields, adding PEP 484 type annotations on `ChatPrivacy` entrypoints, failing closed with `ChatNotApproved` when `provider_position["valid"]` is `False` or `actual_mode` receives synthetic/demo approval refs, and blocking `retention_days` before full DPO/Legal approval or with invalid/non-ASCII `CHAT_RETENTION_DAYS`).
* Integrated `evaluate_provider_position` into `src/core/src/zava_forward/core/regulatory_privacy.py` (`readiness_report(env)` no-echo `provider_position` while preserving the 8-item Issue #217 `CRITERIA` tuple and gating `live_data_permitted`; `build_foundry_query(...)` fail-closed `provider_violations` check) and exposed `"provider_position"` on `GET /api/chat/status` in `src/api/src/zava_forward/api/server.py`.

### Canonical Privacy, DPIA, and Knowledge-Base Documentation (`P02`, `P02-T01`, `P02-T02`)

* Updated `docs/reference/research/chat-memory-dpia.md` (`ms.date: 2026-11-15`) with the UK South / EU data-zone residency posture table, zero-training enforcement rule, synchronous content-filtering vs 30-day abuse-monitoring disclosure, cross-border transfer prohibition (`CHAT_TRANSFER_REF`), `ZF_DATA_PROCESSING=actual` synthetic/demo reference rejection, and pre-approval retention hard gate while keeping `D1`–`D8` `"Not recorded"` and chat/memory data-map retention `"Unknown ..."`.
* Updated `src/core/README.md` (`chat_provider_position.py` contract and environment gates), `docs/reference/README.md` (`chat-memory-dpia.md` summary), and appended a dated `2026-11-15` entry to `docs/reference/log.md` with zero `.copilot-tracking/` references in source or docs.

### Deterministic Unit Tests and Focused Validation (`P03`, `P03-T01`, `P03-T02`)

* Created strictly typed `src/core/tests/test_chat_provider_position.py` (`13` test methods, within `<= 15` cap; `0` removals) covering default `uksouth` `Standard` posture, unapproved regions, global SKUs and `uksouth`+`DataZoneStandard` mismatch, EU data-zone `CHAT_TRANSFER_REF` gating, `ZF_DATA_PROCESSING=actual` synthetic/demo ref rejection, provider training rejection, abuse-monitoring disclosure and no-echo guarantees, `ChatPrivacy` write/opt-in blocking and pre-approval retention blocking, `/api/chat/status` contract exposure, and `regulatory_privacy` `readiness_report` + `build_foundry_query` fail-closed behavior.
* Added `1` end-to-end `ChatContractMixin` regression test in `src/core/tests/test_chat_privacy.py` (executed against both `MemoryStore` and SQLite `SqlStore`) and `1` documentation-contract guard test in `src/core/tests/test_chat_dpia_record.py` (`2` methods combined, within `<= 6` cap; `0` removals).

## Implementation-Time Plan and Detail Updates

* Current-state validation wording update (`P03`, `P03-T02`): Refined `P03-T02` validation phrasing in `.copilot-tracking/plans/2026-11-15/issue-163-chat-privacy-region-plan.md` and `.copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-phase-details.md` to specify the focused chat/memory/privacy/DPIA/regulatory/content-standard/dependency-rule `unittest` suites across `src/core`, `src/agents`, and `src/api`. Unfiltered host `/usr/bin/python3 -m unittest discover` in `src/core` without an editable `pip install -e ".[dev]"` virtualenv encounters host-environment prerequisites in 3 unrelated suites (`test_discovery_assistant_demo` and `test_learning_test_bundles` spawning subprocess `python3 -m zava_forward.core` without `PYTHONPATH`, and `test_device_registry_azure` requiring optional `azure.iot.hub`) plus 1 unrelated pre-existing parent-branch error in `test_challenge_no_retaliation_220` (`assistants.py`); all 3,622 in-process `src/core` tests and 100% of chat/privacy/DPIA/regulatory/API/dependency tests pass.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| Core privacy, DPIA, and regulatory unit tests | `src/core` (`14` test modules, `285` tests) | Passed | `Ran 285 tests in 123.445s — OK (skipped=1)` including `test_chat_provider_position.py` (13), `test_chat_privacy.py`, `test_chat_dpia_record.py`, `test_regulatory_privacy.py`, and `test_regulatory_privacy_audit_217.py` |
| Agents chat unit tests | `src/agents` (`test_*chat*.py`, `124` tests) | Passed | `Ran 124 tests in 16.149s — OK` |
| API chat, privacy, consent, resident, and content-standard unit tests | `src/api` (`9` test modules, `239` tests) | Passed | `Ran 165 tests in 180.5s — OK (skipped=1)` + `Ran 74 tests in 47.6s — OK` including `test_chat_panel.py`, `test_chat_isolation.py`, `test_home_chat_api.py`, `test_regulatory_chat_api.py`, `test_chat_consent_boundary.py`, `test_resident_chat_api.py`, `test_diagnostic_log_privacy.py`, and `test_content_standard.py` |
| Dependency-rule and migration regression tests | `src/core`, `src/api`, `tools/` (`29` tests) | Passed | `test_dependency_rule.py` in `src/core` (`2` tests OK) and `src/api` (`2` tests OK); `tools/rename-zava-tests.py` (`25` tests OK) |
| Ruff lint and format check | `src/core` and `src/api` | Passed | `ruff check .` (`All checks passed!`) and `ruff format --check .` (`310 files already formatted` in `src/core`; `216 files already formatted` in `src/api`) |
| Strict `mypy` type check | `src/core` and `src/api` | Passed | `Success: no issues found in 363 source files` (`src/core`); `Success: no issues found in 300 source files` (`src/api`) |
| Complete local gate (`tools/rpi-checks.py --all`) | Repository-wide | Skipped (explicit caller constraint) | Caller prompt explicitly set Focused validation tier and instructed: `do not run tools/rpi-checks.py --all` |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`, `P03-T02` all `[x]`)
* Completed-work evidence and handoff prose: Reconciled across `src/core`, `src/api`, and `docs/reference/`
* Validation, blockers, remaining work, and follow-up items: Reconciled (`0` blockers, `0` remaining engineering items; human DPO/Legal sign-off preserved in follow-ups)
* Review readiness: Ready for `rpi-review`

## Blockers

* None

## Remaining Work

* None in declared plan scope

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/issue-163-chat-privacy-region-plan.md, `## Follow-Up Items`
* Obtain named DPO and Legal sign-off on decisions `D1`–`D8` in `docs/reference/research/chat-memory-dpia.md` before enabling live personal-data chat/memory storage or retention (owner: human DPO and Legal).

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan; completed: P01, P01-T01, P01-T02, P02, P02-T01, P02-T02, P03, P03-T01, P03-T02; remaining: none
* Validation coverage: 677 targeted unit/regression tests passed across `src/core` (287), `src/agents` (124), `src/api` (241), and `tools/` (25); `ruff check`, `ruff format --check`, and `mypy` passed with 0 issues across `src/core` (363 files) and `src/api` (300 files); `tools/rpi-checks.py --all` skipped per explicit caller direction
* Blockers: None
* Current plan and detail updates: Refined `P03`/`P03-T02` validation phrasing to record exact focused `unittest` suites alongside full `ruff` and `mypy`
* Planning and critique state: Ready (`PC-001` through `PC-005` resolved)
* Follow-up items: Named human DPO/Legal sign-off on `D1`–`D8` (`Refs #163` criterion 2)
* Review readiness or no-handoff reason: Ready for post-implementation `rpi-review`
* Continuation owner: parent (confirmed automatic RPI Agent)
