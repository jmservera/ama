<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #163 Explicit Deployment Attestation in Actual Mode and IaC Mismatch Disclosure (Cycle 4)

## Task Metadata

* Task ID: issue-163-chat-privacy-region-c4
* Parent Task ID: issue-163-chat-privacy-region-c3
* Plan: .copilot-tracking/plans/2026-11-15/issue-163-chat-privacy-region-c4-plan.md
* Detail date: 2026-11-15

<!-- rpi:phase id=P01 -->
## P01: Enforce Actual-Mode Deployment Attestation, Document IaC Default Mismatch, and Verify (`RV-001`)

### Context

Cycle 3 review (`RV-001`) noted that `infra/main.bicep` currently defaults `chatModelSku` to `'GlobalStandard'` and `infra/modules/containerapps.bicep` does not inject `CHAT_PROVIDER_REGION` or `CHAT_DEPLOYMENT_TYPE`. While `constructed` mode (`ZF_DATA_PROCESSING` unset) intentionally falls back to `uksouth` / `Standard` for synthetic unit fixtures (`#281`) and the owner-approved synthetic demo (`#891`), `ZF_DATA_PROCESSING=actual` must fail closed if either setting is omitted rather than silently assuming `uksouth` / `Standard`, and all evaluations must expose `deployment_attested: bool`.

### Intent

Enforce explicit region and deployment-SKU attestation in `actual` mode, expose `deployment_attested` in `ProviderPositionEvaluation` and `MODEL_PROVIDER_CONTRACT`, document the `infra/main.bicep` mismatch, and verify with deterministic unit tests without touching `infra/`.

### Boundaries

* Included: `src/core/src/zava_forward/core/chat_provider_position.py`, `src/core/README.md`, `docs/reference/research/chat-memory-dpia.md`, `src/core/tests/test_chat_provider_position.py`.
* Excluded: `infra/` files, Cycle 1–3 RPI tracking artifacts, `tools/rpi-checks.py --all`.

### Likely Targets

* src/core/src/zava_forward/core/chat_provider_position.py
* src/core/README.md
* docs/reference/research/chat-memory-dpia.md
* src/core/tests/test_chat_provider_position.py

### Dependencies

* None.

### Validation Expectations

* Focused `src/core` and `src/api` test suites, `ruff check`, `ruff format --check`, `mypy`, and `git diff --check` exit `0`.

### Completion Evidence

* Passing unit, lint, format, type, and whitespace checks recorded in `.copilot-tracking/changes/2026-11-15/issue-163-chat-privacy-region-c4-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Require explicit region and deployment SKU in `actual` mode, expose `deployment_attested`, and update docs (`RV-001`)

#### Context

See Cycle 3 `RV-001`.

#### Intent

* In `src/core/src/zava_forward/core/chat_provider_position.py`:
  * Add `deployment_attested: bool` to `ProviderPositionEvaluation` and `"deployment_attested": False` to `MODEL_PROVIDER_CONTRACT`.
  * In `evaluate_provider_position()`:
    * Determine `region_explicit = region is not None or "CHAT_PROVIDER_REGION" in source_env`.
      * When `region_explicit`: parse `raw_region` as before (`region` if not `None` else `source_env.get("CHAT_PROVIDER_REGION")`) and validate against `PRIMARY_REGION` / `EU_DATA_ZONE_REGIONS` (`"unapproved_region"` if invalid/blank).
      * When `not region_explicit`: if `is_actual`, set `raw_region = ""`, `residency_zone = "unapproved"`, `safe_region = "unapproved"`, and append `"unattested_region_in_actual_mode"` to `violations`; otherwise (`constructed` mode), set `raw_region = PRIMARY_REGION`, `residency_zone = "uk_south"`, `safe_region = PRIMARY_REGION`.
    * Determine `deployment_explicit = deployment_type is not None or "CHAT_DEPLOYMENT_TYPE" in source_env`.
      * When `deployment_explicit`: parse `raw_deployment` and validate via `_DEPLOYMENT_TYPE_MAP` (`"unapproved_deployment_residency"` if invalid/blank or `DataZoneStandard` outside `eu_data_zone`).
      * When `not deployment_explicit`: if `is_actual`, set `canonical_deployment = None`, `safe_deployment = "unapproved"`, and append `"unattested_deployment_in_actual_mode"` to `violations`; otherwise (`constructed` mode), set `canonical_deployment = "Standard"`, `safe_deployment = "Standard"`.
    * Compute `requires_transfer_signoff = (residency_zone == "eu_data_zone" or (region_explicit and raw_region != PRIMARY_REGION) or canonical_deployment == "DataZoneStandard" or explicit_transfer)` so omitting `CHAT_PROVIDER_REGION` in `actual` mode reports `"unattested_region_in_actual_mode"` cleanly without falsely classifying an unconfigured domestic check as an explicit cross-border request unless `explicit_transfer` or `DataZoneStandard` is set.
    * Set `deployment_attested = bool(region_explicit and deployment_explicit and residency_zone != "unapproved" and safe_deployment != "unapproved" and "unapproved_deployment_residency" not in violations)`.
* In `docs/reference/research/chat-memory-dpia.md` and `src/core/README.md`:
  * Document `deployment_attested`, the `unattested_region_in_actual_mode` / `unattested_deployment_in_actual_mode` fail-closed rules in `ZF_DATA_PROCESSING=actual`, and the current `infra/main.bicep` `chatModelSku = 'GlobalStandard'` mismatch (plain ASCII punctuation, zero `"human-approved"` phrasing, preserving `ChatDpiaRecordGuard` invariants).

#### Boundaries

* Included: `chat_provider_position.py`, `src/core/README.md`, `docs/reference/research/chat-memory-dpia.md`.
* Excluded: `infra/`.

#### Likely Targets

* src/core/src/zava_forward/core/chat_provider_position.py
* src/core/README.md
* docs/reference/research/chat-memory-dpia.md

#### Dependencies

* None.

#### Validation Expectations

* `ruff check`, `ruff format --check`, `mypy`, `ChatDpiaRecordGuard`, `test_content_standard.py`, and `git diff --check` pass.

#### Completion Evidence

* Updated `chat_provider_position.py` and synchronized documentation.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Expand unit assertions and run focused validation (`RV-001`)

#### Context

Lock test ownership before critique:
* Canonical targets: `src/core/tests/test_chat_provider_position.py` (`exact removals: none`, `maximum new test methods: 0`, keeping `13` total methods by expanding `test_default_uksouth_standard_position_is_valid_and_not_dpo_accepted`, `test_actual_data_mode_rejects_synthetic_and_demo_references`, and `test_regulatory_privacy_readiness_and_foundry_query_enforce_provider_position_no_echo`); generated targets: `none`.
* Semantic vs regression coverage: semantic assertions prove `deployment_attested` distinguishes defaulted `constructed` calls (`False`) from explicitly configured `uksouth` + `Standard` (`True`) and that `ZF_DATA_PROCESSING="actual"` fails closed with `"unattested_region_in_actual_mode"` / `"unattested_deployment_in_actual_mode"` when omitted while omitting those two codes when explicitly configured; regression assertions keep all `constructed` suites green.

#### Intent

* In `test_default_uksouth_standard_position_is_valid_and_not_dpo_accepted`:
  * Assert `MODEL_PROVIDER_CONTRACT["deployment_attested"]` and `chat_privacy.MODEL_PROVIDER_POSITION["deployment_attested"]` are `False`, and assert `pos["deployment_attested"]` is `False` when `env={}` (constructed default) and `True` when `env={"CHAT_PROVIDER_REGION": "uksouth", "CHAT_DEPLOYMENT_TYPE": "Standard"}`.
* In `test_uksouth_rejects_datazone_standard_because_uk_outside_eu_data_zone`:
  * Assert `pos["deployment_attested"]` is `False` on `uksouth` + `DataZoneStandard` (`PC-001`).
* In `test_actual_data_mode_rejects_synthetic_and_demo_references`:
  * Assert `evaluate_provider_position({"ZF_DATA_PROCESSING": "actual"})` has `deployment_attested is False` and includes `"unattested_region_in_actual_mode"`, `"unattested_deployment_in_actual_mode"`, and `"actual_mode_dpo_legal_unapproved"`.
  * Assert `evaluate_provider_position({"ZF_DATA_PROCESSING": "actual", "CHAT_PROVIDER_REGION": "uksouth", "CHAT_DEPLOYMENT_TYPE": "Standard"})` has `deployment_attested is True` and `violations == ["actual_mode_dpo_legal_unapproved"]` (proving that even once `DPO_LEGAL_APPROVED` is later enabled, explicit region + SKU attestation is required and `GlobalStandard` remains rejected).
* In `test_regulatory_privacy_readiness_and_foundry_query_enforce_provider_position_no_echo`:
  * Include `"CHAT_DEPLOYMENT_TYPE": "DataZoneStandard"` on `actual_eu_env` and verify both `actual_mode_dpo_legal_unapproved` and an unattested `ZF_DATA_PROCESSING="actual"` `readiness_report` / `build_foundry_query` call fail closed with `"unattested_deployment_in_actual_mode"`.
* Run focused `src/core` and `src/api` suites, `ruff`, `mypy`, and `git diff --check`.

#### Boundaries

* Included: `src/core/tests/test_chat_provider_position.py`.
* Excluded: `tools/rpi-checks.py --all`.

#### Likely Targets

* src/core/tests/test_chat_provider_position.py

#### Dependencies

* P01-T01

#### Validation Expectations

* Focused `unittest` suites, `ruff check`, `ruff format --check`, `mypy`, and `git diff --check` exit `0`.

#### Completion Evidence

* Passing outputs recorded in `.copilot-tracking/changes/2026-11-15/issue-163-chat-privacy-region-c4-changes.md`.

#### Unresolved Items

* None.
