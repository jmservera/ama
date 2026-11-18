<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #163 Model Provider Data-Handling and Region Position Contract

## Metadata

* Task ID: issue-163-chat-privacy-region
* Task slug: issue-163-chat-privacy-region
* Related plan: .copilot-tracking/plans/2026-11-15/issue-163-chat-privacy-region-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/issue-163-chat-privacy-region-research.md (`C1`–`C16`), src/core/src/zava_forward/core/chat_privacy.py, src/core/src/zava_forward/core/regulatory_privacy.py, src/core/src/zava_forward/core/data_protection.py, src/api/src/zava_forward/api/server.py, docs/reference/research/chat-memory-dpia.md

## Phase Index

| Phase ID | Name                                                            | Status | Detail sections        |
|----------|-----------------------------------------------------------------|--------|------------------------|
| P01      | Implement Enforceable Provider Data-Handling and Region Contract | ready  | P01, P01-T01, P01-T02  |
| P02      | Update Canonical Privacy and DPIA Reference Documentation       | ready  | P02, P02-T01, P02-T02  |
| P03      | Add Deterministic Unit Tests and Run Focused Validation         | ready  | P03, P03-T01, P03-T02  |

<!-- rpi:phase id=P01 -->
## P01: Implement Enforceable Provider Data-Handling and Region Contract

### Context

`chat_privacy.MODEL_PROVIDER_POSITION` (`C1`) currently exposes only narrative metadata (`provider`, `region`, `zava_stores_prompts`, `foundry_agent_memory`, `documented_terms`, `open_items`) with no runtime validation, while `ChatPrivacy.decision()` (`C2`) evaluates `CHAT_RETENTION_REF` and `CHAT_RETENTION_DAYS` without checking `approved` (`not missing`), ASCII digits, or provider residency/training posture. Furthermore, `src/core/pyproject.toml` (`C11`) excludes `chat_privacy.py` from `ruff format` and `mypy`.

### Intent

Provide one strictly typed, ruff-formatted source of truth (`chat_provider_position.py`) for model provider residency, zero-training, content-filtering/abuse-monitoring disclosure, and cross-border transfer controls, and wire it into `chat_privacy.py`, `regulatory_privacy.py`, and `/api/chat/status` alongside a fail-closed pre-approval retention gate.

### Boundaries

* Included: `src/core/src/zava_forward/core/chat_provider_position.py` (new canonical target), `src/core/src/zava_forward/core/chat_privacy.py`, `src/core/src/zava_forward/core/regulatory_privacy.py`, and `src/api/src/zava_forward/api/server.py` (`/api/chat/status` additive key). Generated targets: `none`.
* Excluded: `infra/` Bicep files, `src/agents/`, web UI JavaScript/HTML/CSS under `src/api/src/zava_forward/api/web/`, and any claim of verified human DPO/Legal sign-off.

### Likely Targets

* src/core/src/zava_forward/core/chat_provider_position.py: New typed contract and fail-closed validator module.
* src/core/src/zava_forward/core/chat_privacy.py: Enrich `MODEL_PROVIDER_POSITION`, add PEP 484 type annotations on `ChatPrivacy` entrypoints, add `ChatPrivacy.provider_position()`, gate `decision()` retention on `approved` + ASCII bounds + `actual_mode`/placeholder ref checks, and enforce provider validation in `_require()`.
* src/core/src/zava_forward/core/regulatory_privacy.py: Include no-echo `provider_position` in `readiness_report(env)` (preserving the 8-item `CRITERIA` tuple and `dpo_reviewed=False`) and enforce `evaluate_provider_position(env)` fail-closed in `build_foundry_query`.
* src/api/src/zava_forward/api/server.py: Add `provider_position` to `/api/chat/status` dictionary without altering existing keys.

### Dependencies

* None (`data_protection.actual_mode` already exists in `src/core`).

### Validation Expectations

* `PYTHONPATH=src python3 -m mypy` and `python3 -m ruff check` / `python3 -m ruff format --check` in `src/core` check `chat_provider_position.py` and `regulatory_privacy.py` with zero errors.
* `PortabilityTests.test_chat_privacy_has_no_own_sql_or_connection` (`C12`) and `test_content_standard.py` (`C15`) pass.

### Completion Evidence

* `evaluate_provider_position`, `require_provider_position`, `ChatPrivacy.provider_position()`, `ChatPrivacy.decision()`, `regulatory_privacy.readiness_report()`, and `/api/chat/status` return consistent structured dictionaries and enforce fail-closed raises on violations.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Create typed `chat_provider_position.py` contract and fail-closed validator

#### Context

Research findings `C1`, `C5`, `C9`, `C10`, `C11`, `C15`, and `C16` establish that primary platform deployments run in `uksouth` (`Standard`), the bounded synthetic resident assistant template uses `swedencentral` (`Standard`) with `DataZoneStandard` documented for EU data-zone capacity, live personal-data processing is flagged by `ZF_DATA_PROCESSING=actual` (`data_protection.actual_mode`), and standalone `"human-approved"` phrasing is prohibited by `test_content_standard.py`.

#### Intent

Create `src/core/src/zava_forward/core/chat_provider_position.py` with full type annotations (`TypedDict` / `Mapping[str, str]`) and zero external dependencies.

#### Boundaries

* Included:
  * Constants:
    * `PRIMARY_REGION = "uksouth"`
    * `EU_DATA_ZONE_REGIONS = ("swedencentral", "westeurope", "northeurope", "francecentral", "germanywestcentral", "italynorth", "polandcentral", "spaincentral")`
    * `APPROVED_RESIDENCY_REGIONS = (PRIMARY_REGION,) + EU_DATA_ZONE_REGIONS`
    * `APPROVED_DEPLOYMENT_TYPES = ("Standard", "DataZoneStandard")`
    * `SYNTHETIC_REF_PREFIXES = ("synth-", "syn-", "synthetic-")`
    * `DEMO_REF_MARKERS = ("chat-demo-storage-approval-", "chat-demo-breakglass-disclaimer-", "chat-memory-dpia.md")`
    * `PLACEHOLDER_REF_TOKENS = frozenset({"yes", "no", "true", "false", "1", "0", "ok", "approved", "none", "null", "n/a", "unknown", "tbd", "todo"})`
    * `DOCUMENTED_VENDOR_TERMS`, `CONTENT_FILTERING_DISCLOSURE`, `ABUSE_MONITORING_DISCLOSURE`, `CROSS_BORDER_TRANSFER_POLICY`, `RETENTION_APPROVAL_POLICY`, and `MODEL_PROVIDER_CONTRACT`.
  * Reference helpers (`PC-002`):
    * `is_demo_or_synthetic_ref(value: str) -> bool`: returns `True` when trimmed lower-case `value` starts with `SYNTHETIC_REF_PREFIXES` or contains any `DEMO_REF_MARKERS`.
    * `is_valid_governance_ref(value: str, *, actual: bool = False) -> bool`: returns `False` when empty, when trimmed lower-case `value` is in `PLACEHOLDER_REF_TOKENS` (a bare `"yes"` or `"true"` is never a governance reference), or when `actual` is `True` and `is_demo_or_synthetic_ref(value)` is `True`.
  * Evaluator `evaluate_provider_position(env: Mapping[str, str] | None = None, *, region: str | None = None, deployment_type: str | None = None, customer_data_training: bool | str | None = None, cross_border_transfer: bool | str | None = None, transfer_ref: str | None = None, abuse_monitoring_modified_ref: str | None = None) -> ProviderPositionEvaluation`:
    * Reads defaults from `env` (`CHAT_PROVIDER_REGION` defaulting to `"uksouth"` when key absent, `CHAT_DEPLOYMENT_TYPE` defaulting to `"Standard"` when key absent, `CHAT_PROVIDER_TRAINING` defaulting to `"false"`, `CHAT_CROSS_BORDER_TRANSFER` defaulting to `"false"`, `CHAT_TRANSFER_REF`, `CHAT_ABUSE_MONITORING_MODIFIED_REF`, and `ZF_DATA_PROCESSING` via `actual_mode`). If `"CHAT_PROVIDER_REGION"` or `"CHAT_DEPLOYMENT_TYPE"` is explicitly present in `env` as blank/whitespace (or `""` passed explicitly), fails closed rather than falling back to defaults.
    * Strict no-echo invariant (`PC-001`): Never echoes raw reference strings (`transfer_ref`, `abuse_monitoring_modified_ref`) or arbitrary unallowlisted `env` values into the returned dict; emits boolean `transfer_ref_recorded` and `modified_abuse_monitoring_recorded` flags, emits allowlisted `region` / `deployment_type` values (or `"unapproved"` when outside allowlists), and carries `dpo_legal_approved: False` and `documented_terms["dpo_accepted"]: False`.
    * Residency and cross-border classification (`PC-003`):
      * `region == "uksouth"`: `residency_zone = "uk_south"`; permits ONLY `deployment_type == "Standard"` (`DataZoneStandard` on `uksouth` is rejected with `"unapproved_deployment_residency"`); `cross_border_transfer` is `False` unless `CHAT_CROSS_BORDER_TRANSFER` is explicitly truthy.
      * `region in EU_DATA_ZONE_REGIONS`: `residency_zone = "eu_data_zone"`; permits `deployment_type in ("Standard", "DataZoneStandard")`; unconditionally derives `cross_border_transfer = True` and requires a valid `CHAT_TRANSFER_REF`.
      * Otherwise: `residency_zone = "unapproved"` and records `"unapproved_region"`.
    * Violation codes (ordered, deduplicated list):
      * `"unapproved_region"` when normalized `region` is not in `APPROVED_RESIDENCY_REGIONS`.
      * `"unapproved_deployment_residency"` when `deployment_type` is not in `APPROVED_DEPLOYMENT_TYPES` or when `region == "uksouth"` is paired with `DataZoneStandard`.
      * `"provider_training_prohibited"` when `customer_data_training` / `CHAT_PROVIDER_TRAINING` is anything other than `None`, `""`, `False`, `"false"`, `"0"`, `"no"`, `"off"`, `"disabled"`, or `"none"`.
      * `"invalid_cross_border_flag"` when `cross_border_transfer` / `CHAT_CROSS_BORDER_TRANSFER` is not a recognized boolean representation (`True`/`False`/`None`/`""`/`"true"`/`"false"`/`"1"`/`"0"`/`"yes"`/`"no"`/`"on"`/`"off"`).
      * `"cross_border_transfer_unapproved"` when `cross_border_transfer` is `True` and `transfer_ref` is empty or a bare placeholder token (`not is_valid_governance_ref(transfer_ref, actual=False)`).
      * `"synthetic_or_demo_transfer_ref_in_actual_mode"` when `cross_border_transfer` is `True`, `is_valid_governance_ref(transfer_ref, actual=False)` is `True`, `actual_mode(env)` is `True`, and `is_demo_or_synthetic_ref(transfer_ref)` is `True`.
      * `"invalid_abuse_monitoring_ref"` when `abuse_monitoring_modified_ref` is non-empty and in `PLACEHOLDER_REF_TOKENS`.
      * `"synthetic_or_demo_abuse_monitoring_ref_in_actual_mode"` when `abuse_monitoring_modified_ref` is non-empty, `actual_mode(env)` is `True`, and `is_demo_or_synthetic_ref(abuse_monitoring_modified_ref)` is `True`.
    * Always reports `zero_model_training: not training_violation`, `customer_data_training: training_violation`, `dpo_legal_approved: False`, `documented_terms` with `status="vendor_documentation_not_dpo_accepted"` and `dpo_accepted=False`, `content_filtering`, and `abuse_monitoring` (`mode="modified_recorded_unverified"` when valid `abuse_monitoring_modified_ref` is present, else `"platform_default_unverified"`).
  * Enforcer `require_provider_position(...) -> ProviderPositionEvaluation`: raises `ProviderPositionError` (subclass of `ValueError`) if `not result["valid"]`.
* Excluded: Network calls, Azure SDK calls, or SQL queries.

#### Likely Targets

* src/core/src/zava_forward/core/chat_provider_position.py: New module.

#### Dependencies

* src/core/src/zava_forward/core/data_protection.py (`actual_mode`).

#### Validation Expectations

* Strict `mypy`, `ruff check`, and `ruff format --check` pass on `chat_provider_position.py`.

#### Completion Evidence

* Module exports typed contract constants, `ProviderPositionError`, `is_demo_or_synthetic_ref`, `evaluate_provider_position`, and `require_provider_position`.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Wire provider contract and pre-approval retention gate into `chat_privacy.py`, `regulatory_privacy.py`, and `server.py`

#### Context

`ChatPrivacy.decision()` (`C2`) currently permits `retention_days` to resolve to an integer even if `approved` is `False`, does not reject non-ASCII digits (`"\u00b2"`) or unreasonable upper bounds (`> 36500`), does not check `provider_position["valid"]`, and does not reject `SYNTH-*` or demo Markdown references when `ZF_DATA_PROCESSING=actual` (`C5`, `C16`). Meanwhile, `test_chat_privacy.py` (`C12`, `C13`) requires preserving legacy keys on `MODEL_PROVIDER_POSITION` and keeping SQL keywords out of `chat_privacy.py`.

#### Intent

Enforce both the provider/region contract and the pre-approval retention prohibition through `ChatPrivacy`, surface `provider_position` in `regulatory_privacy.readiness_report()` and `/api/chat/status`, and preserve full backward compatibility for existing synthetic/demo tests.

#### Boundaries

* Included:
  * `src/core/src/zava_forward/core/chat_privacy.py`:
    * Build `MODEL_PROVIDER_POSITION` from `MODEL_PROVIDER_CONTRACT` so existing keys (`provider`, `region`, `zava_stores_prompts`, `foundry_agent_memory`, `documented_terms`, `open_items`) keep exact expected values/shapes while adding `primary_region`, `eu_data_zone_regions`, `approved_deployment_types`, `zero_model_training`, `customer_data_training`, `content_filtering`, `abuse_monitoring`, `cross_border_transfer_policy`, and `retention_policy`.
    * Add PEP 484 type annotations (`PC-004`) to `ChatPrivacy.__init__`, `ChatPrivacy.provider_position`, `ChatPrivacy.decision`, `ChatPrivacy.start_thread`, `ChatPrivacy.add_message`, `ChatPrivacy.opt_in`, `ChatPrivacy.add_memory`, and `ChatPrivacy.purge_retention` so strictly typed `test_chat_provider_position.py` calls require zero `# type: ignore`.
    * Add `ChatPrivacy.provider_position(self) -> ProviderPositionEvaluation` returning `evaluate_provider_position(self.env)`.
    * Update `ChatPrivacy.decision(self) -> dict[str, Any]`:
      * Check `CHAT_DPIA_REF`, `CHAT_LAWFUL_BASIS_REF`, `CHAT_NOTICE_REF` using `is_valid_governance_ref(ref, actual=False)` for `missing` (rejecting empty or bare placeholder tokens like `"yes"`/`"true"`), and in `actual_mode(self.env)` collect any `is_demo_or_synthetic_ref(ref)` (`SYNTH-*`, `SYN-*`, `SYNTHETIC-*`, `chat-demo-*`, `chat-memory-dpia.md`) into `actual_mode_blocked`.
      * Evaluate `provider_pos = self.provider_position()`.
      * `approved = not missing and not actual_mode_blocked and provider_pos["valid"]`.
      * Check retention: `ret_ref = self._ref("CHAT_RETENTION_REF")`, `ret_ref_ok = is_valid_governance_ref(ret_ref, actual=is_actual)`, `days_ok = days.isascii() and days.isdigit() and 1 <= int(days) <= 36500`, `retention_set = approved and ret_ref_ok and days_ok`. When `not retention_set`, `retention_days` MUST be `None` and `retention` starts with `"Unknown"`.
      * Include `provider_position=provider_pos`, `actual_mode_blocked=actual_mode_blocked`, and `dpo_legal_approved=False` in `decision()`.
    * Update `ChatPrivacy._require(self) -> dict[str, Any]`:
      * When `not d["approved"]`, include missing gate names, `actual_mode_blocked` gates, or `provider_position["violations"]` in the raised `ChatNotApproved` message so callers receive a clear plain-language refusal reason.
  * `src/core/src/zava_forward/core/regulatory_privacy.py` (`PC-001`, `PC-005`):
    * Import `evaluate_provider_position` from `.chat_provider_position`.
    * Keep `CRITERIA` unchanged at its 8 Issue #217 4-tuples (`len(r["criteria"]) == 8`).
    * In `readiness_report(env: Any)`, normalize `mapping = env if isinstance(env, Mapping) else {}`, compute `pos = evaluate_provider_position(mapping)`, gate `permitted = not missing and not synthetic and bool(pos["valid"])`, and attach `"provider_position": pos` (which never echoes raw reference or unallowlisted `env` values).
    * In `build_foundry_query(..., env: Any = None)`, evaluate `pos = evaluate_provider_position(env if isinstance(env, Mapping) else {})` and fail closed (`permitted=False`, `fields={}`, `manual_path=MANUAL_PATH`, `provider_violations=list(pos["violations"])`) when `not pos["valid"]`.
  * `src/api/src/zava_forward/api/server.py`:
    * In `GET /api/chat/status` (`lines 1207-1222`), add `provider_position=dec["provider_position"]` to the returned dict.
* Excluded: Changing UI layout or adding banned SQL tokens to `chat_privacy.py`.

#### Likely Targets

* src/core/src/zava_forward/core/chat_privacy.py
* src/core/src/zava_forward/core/regulatory_privacy.py
* src/api/src/zava_forward/api/server.py

#### Dependencies

* P01-T01

#### Validation Expectations

* Existing `test_chat_privacy.py`, `test_chat_memory.py`, `test_regulatory_privacy.py`, `test_regulatory_privacy_audit_217.py`, `test_chat_isolation.py`, and `test_chat_panel.py` pass unchanged.

#### Completion Evidence

* `ChatPrivacy` refuses chat/memory writes when provider/region/training/transfer checks fail, keeps `retention_days=None` until approval gates pass, and exposes `provider_position` on `decision()`, `readiness_report()`, and `/api/chat/status`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Update Canonical Privacy and DPIA Reference Documentation

### Context

`docs/reference/research/chat-memory-dpia.md` (`C7`) is the canonical privacy and draft DPIA document for chat and memory, guarded by `src/core/tests/test_chat_dpia_record.py` (`C14`). Knowledge-base conventions require updating `docs/reference/README.md` and appending to `docs/reference/log.md` on material updates, using `*` bullets, plain ASCII punctuation, no em dashes, and no bolded-prefix list items.

### Intent

Document the recorded and enforced model provider data-handling and region position contract in `docs/reference/research/chat-memory-dpia.md` and synchronize `src/core/README.md`, `docs/reference/README.md`, and `docs/reference/log.md` while keeping human DPO/Legal decisions `D1`–`D8` `"Not recorded"`.

### Boundaries

* Included: `docs/reference/research/chat-memory-dpia.md`, `src/core/README.md`, `docs/reference/README.md`, and `docs/reference/log.md`. Generated targets: `none`.
* Excluded: Modifying immutable snapshots under `docs/reference/regulatory/`, modifying `docs/case_study_48_original.md`, modifying `docs/reference/memory.md`, or recording fabricated DPO/Legal approvals.

### Likely Targets

* docs/reference/research/chat-memory-dpia.md
* src/core/README.md
* docs/reference/README.md
* docs/reference/log.md

### Dependencies

* P01

### Validation Expectations

* `test_chat_dpia_record.py` and `test_regulatory_privacy.py` (`DpiaScope`) pass; `git diff` confirms Markdown style compliance and zero `.copilot-tracking/` references in docs or source.

### Completion Evidence

* Updated `chat-memory-dpia.md` (`ms.date: 2026-11-15`), `src/core/README.md`, `docs/reference/README.md`, and appended `docs/reference/log.md` entry.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Record residency matrix, data-handling disclosures, transfer gate, and retention gate in `chat-memory-dpia.md`

#### Context

`## Model provider and region` in `docs/reference/research/chat-memory-dpia.md` (`C7`) currently has narrative prose from 2026-11-01 without the structured residency matrix, runtime gate variables, or fail-closed enforcement contract.

#### Intent

Expand `## Model provider and region` (and synchronize `## Status`, `## Decision record`, and `## Status record` plus frontmatter `ms.date: 2026-11-15`) to record:
1. UK South (`uksouth` `Standard`) primary residency posture vs bounded EU data-zone (`DataZoneStandard` / EEA regions) posture vs prohibited `GlobalStandard` and non-UK/non-EU regions.
2. Zero foundation-model training on customer prompts, completions, and opt-in memory (`CHAT_PROVIDER_TRAINING` fail-closed gate).
3. Synchronous `Azure AI Content Safety` harm-filtering disclosure vs platform-default 30-day abuse-monitoring flagged-sample retention and human-review disclosure (`CHAT_ABUSE_MONITORING_MODIFIED_REF`, EEA-only documented reviewer residency vs unverified UK South reviewer residency).
4. Cross-border transfer prohibition outside domestic `uksouth` `Standard` without recorded DPO/Legal transfer sign-off (`CHAT_TRANSFER_REF`), and `ZF_DATA_PROCESSING=actual` rejection of `SYNTH-*` and demo references.
5. Pre-approval retention hard gate ensuring `retention_days` remains inactive (`None` / `Unknown`) until all DPO/Legal approval gates and `CHAT_RETENTION_REF` are satisfied, while preserving `D1`–`D8` as `"Not recorded"` and chat/memory data-map retention rows starting with `"Unknown"`.

#### Boundaries

* Included: `docs/reference/research/chat-memory-dpia.md`.
* Excluded: Changing `D1`–`D8` status from `"Not recorded"` or changing `chat_message`/`chat_thread`/`chat_memory` data-map retention away from `"Unknown ..."`.

#### Likely Targets

* docs/reference/research/chat-memory-dpia.md

#### Dependencies

* P01-T01, P01-T02

#### Validation Expectations

* `src/core/tests/test_chat_dpia_record.py` and `src/core/tests/test_regulatory_privacy.py` pass.

#### Completion Evidence

* All five contract invariants and runtime environment controls are explicitly documented with source and retrieval dates in `docs/reference/research/chat-memory-dpia.md`.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Synchronize `src/core/README.md`, `docs/reference/README.md`, and `docs/reference/log.md`

#### Context

Repository instructions require updating component READMEs when module contracts expand and updating `docs/reference/README.md` + `docs/reference/log.md` when a knowledge-base document changes materially.

#### Intent

Document `chat_provider_position.py` and the provider/region/transfer/retention gates in `src/core/README.md`, update the `chat-memory-dpia.md` summary in `docs/reference/README.md`, and append one `2026-11-15` entry to `docs/reference/log.md`.

#### Boundaries

* Included: `src/core/README.md`, `docs/reference/README.md`, `docs/reference/log.md` (append-only).
* Excluded: Rewriting prior entries in `docs/reference/log.md` or touching `docs/reference/memory.md`.

#### Likely Targets

* src/core/README.md
* docs/reference/README.md
* docs/reference/log.md

#### Dependencies

* P02-T01

#### Validation Expectations

* Relative Markdown links resolve and diff inspection confirms ASCII punctuation, `*` list markers, no em dashes, and no bolded-prefix list items in new Markdown content.

#### Completion Evidence

* Clean diff across `src/core/README.md`, `docs/reference/README.md`, and `docs/reference/log.md`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Add Deterministic Unit Tests and Run Focused Validation

### Context

Objective 3 requires deterministic unit tests in `src/core/tests/` verifying exposure, validation, fail-closed rejection on unapproved regions or provider training flags, and preservation of the DPO/Legal human gate. Objective 4 specifies the Focused validation tier (`src/core` and `src/api` unit tests, `ruff check`, `ruff format --check`, `mypy`; excluding `tools/rpi-checks.py --all`).

### Intent

Lock test ownership with `0` test removals and bounded semantic + regression test additions, then verify every unit test, linter, formatter, and strict type check across `src/core` and `src/api`.

### Boundaries

* Included:
  * Test ownership and bounds:
    * `src/core/tests/test_chat_provider_position.py` (new strictly typed semantic test suite; exact removals: `none`; maximum additions: `15` test methods).
    * `src/core/tests/test_chat_privacy.py` and `src/core/tests/test_chat_dpia_record.py` (regression and integration guard tests; exact removals: `none`; maximum additions: `6` test methods combined).
  * Focused validation execution across `src/core` and `src/api`.
* Excluded: `tools/rpi-checks.py --all`, external network or live Azure/MSSQL dependencies.

### Likely Targets

* src/core/tests/test_chat_provider_position.py
* src/core/tests/test_chat_privacy.py
* src/core/tests/test_chat_dpia_record.py

### Dependencies

* P01, P02

### Validation Expectations

* Focused chat, memory, privacy, DPIA, regulatory, and dependency-rule `unittest` suites in `src/core` (and `src/agents` chat suites) exit `0`.
* Focused chat, isolation, consent-boundary, resident-chat, diagnostic-privacy, content-standard, and dependency-rule `unittest` suites in `src/api` exit `0`.
* `python3 -m ruff check .`, `python3 -m ruff format --check .`, and `python3 -m mypy` in `src/core` (and `PYTHONPATH=../core/src:../agents/src python3 -m mypy` plus `ruff` in `src/api`) all exit `0`.

### Completion Evidence

* Recorded command outputs and zero-error exit codes in `.copilot-tracking/changes/2026-11-15/issue-163-chat-privacy-region-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Add deterministic unit tests in `src/core/tests/`

#### Context

Because `test_chat_privacy.py` is excluded from `mypy` (`C11`), placing primary contract unit tests in `src/core/tests/test_chat_provider_position.py` subjects both the test file and `chat_provider_position.py` to strict `mypy` and `ruff format --check`, while targeted tests in `test_chat_privacy.py` (exercising both `MemoryStore` and SQLite `SqlStore` via `ChatContractMixin`) and `test_chat_dpia_record.py` verify end-to-end integration and documentation sync.

#### Intent

Cover both semantic invariants and regression boundaries deterministically:
* Semantic coverage in `src/core/tests/test_chat_provider_position.py` (`<= 15` methods):
  1. Default posture (`uksouth` + `Standard`) exposes residency, zero-training, synchronous content-filtering, platform-default abuse-monitoring disclosure, cross-border transfer policy, and `dpo_legal_approved=False`.
  2. Unapproved regions (`eastus`, `westus`, `australiaeast`, explicit blank `""`) fail closed with `unapproved_region` and raise `ProviderPositionError`, even when `CHAT_TRANSFER_REF` is supplied.
  3. Global deployment SKUs (`GlobalStandard`, `GlobalBatch`, `GlobalProvisionedManaged`, explicit blank `""`) and `DataZoneStandard` paired with `uksouth` fail closed with `unapproved_deployment_residency`.
  4. EU data-zone regions (`swedencentral`, `westeurope`, `northeurope`) with `Standard` or `DataZoneStandard` derive `cross_border_transfer=True` and require `CHAT_TRANSFER_REF`: fail closed (`cross_border_transfer_unapproved`) when unset or set to a bare placeholder (`"yes"`), pass technical residency/transfer validation when recorded in synthetic mode (`residency_zone="eu_data_zone"`, `cross_border_transfer=True`, `dpo_legal_approved=False`), and fail closed (`synthetic_or_demo_transfer_ref_in_actual_mode`) when `SYNTH-*`, `SYN-*`, `SYNTHETIC-*`, or demo Markdown refs are supplied under `ZF_DATA_PROCESSING=actual`.
  5. Provider training flags (`CHAT_PROVIDER_TRAINING="true"`, `"1"`, `"yes"`, `"enabled"`, `"unexpected"`, or `customer_data_training=True`) fail closed with `provider_training_prohibited`.
  6. Abuse-monitoring mode transitions to `"modified_recorded_unverified"` only with a valid `CHAT_ABUSE_MONITORING_MODIFIED_REF`, rejects bare placeholder tokens and `ZF_DATA_PROCESSING=actual` synthetic/demo refs, never echoes raw reference values, and keeps `uk_reviewer_residency_verified=False`.
  7. `regulatory_privacy.readiness_report(env)` includes the no-echo `provider_position` (preserving `len(criteria) == 8` and `dpo_reviewed=False`, blocking `live_data_permitted` when `provider_position` is invalid), and `regulatory_privacy.build_foundry_query` fails closed (`permitted=False`, `fields={}`) when `env` violates the provider/region/training contract.
* Integration and documentation guard coverage in `test_chat_privacy.py` and `test_chat_dpia_record.py` (`<= 6` methods combined):
  1. `ChatPrivacy` (`MemoryStore` + `SqlStore`) blocks `start_thread`, `add_message`, `opt_in`, and `add_memory` with `ChatNotApproved` when `CHAT_PROVIDER_REGION` is unapproved, `CHAT_PROVIDER_TRAINING` is enabled, or cross-border transfer lacks `CHAT_TRANSFER_REF`.
  2. `ChatPrivacy.decision()["retention_days"]` stays `None` and `purge_retention()["applied"]` stays `False` when `CHAT_RETENTION_DAYS` + `CHAT_RETENTION_REF` are configured before DPO/Legal approval (`CHAT_DPIA_REF` / `CHAT_LAWFUL_BASIS_REF` / `CHAT_NOTICE_REF` missing or provider invalid), with non-ASCII digits (`"\u00b2"`), or with `SYNTH-*` / demo refs under `ZF_DATA_PROCESSING=actual`.
  3. `ChatDpiaRecordGuard` asserts `## Model provider and region` in `docs/reference/research/chat-memory-dpia.md` records UK South (`uksouth`), EU data-zone (`DataZoneStandard` / `swedencentral`), zero model training, synchronous content filtering, 30-day abuse monitoring, `CHAT_TRANSFER_REF`, and pre-approval retention blocking while `D1`–`D8` remain `"Not recorded"`.

#### Boundaries

* Included: `src/core/tests/test_chat_provider_position.py`, `src/core/tests/test_chat_privacy.py`, `src/core/tests/test_chat_dpia_record.py`.
* Excluded: Removing or weakening any existing test assertion (`exact removals: none`).

#### Likely Targets

* src/core/tests/test_chat_provider_position.py
* src/core/tests/test_chat_privacy.py
* src/core/tests/test_chat_dpia_record.py

#### Dependencies

* P01, P02

#### Validation Expectations

* All tests execute deterministically in `< 5s` in `src/core` and pass `ruff check`, `ruff format --check`, and `mypy`.

#### Completion Evidence

* Passing test output from `src/core` unit test discovery and static checks.

#### Unresolved Items

* None.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Run focused test, lint, format, and type-check suite across `src/core` and `src/api`

#### Context

Focused validation requires running all affected unit tests and CI-equivalent local linters/formatters/type-checkers in `src/core` and `src/api` (since `/api/chat/status` and `test_content_standard.py` live in `src/api`), while explicitly honoring the caller's instruction not to run `tools/rpi-checks.py --all`.

#### Intent

Verify zero test regressions, zero lint/format findings, and zero `mypy` errors across `src/core` and `src/api`, plus clean Markdown/link diff verification.

#### Boundaries

* Included: `unittest`, `ruff check`, `ruff format --check`, and `mypy` in `src/core` and `src/api`; `git diff` check for `.copilot-tracking/` leaks in non-tracking files.
* Excluded: `tools/rpi-checks.py --all`.

#### Likely Targets

* No additional source edits unless a check surfaces an issue.

#### Dependencies

* P03-T01

#### Validation Expectations

* All commands return exit code `0`.

#### Completion Evidence

* Exact commands and pass counts recorded in `.copilot-tracking/changes/2026-11-15/issue-163-chat-privacy-region-changes.md`.

#### Unresolved Items

* None.
