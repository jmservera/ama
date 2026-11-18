---
title: Issue 163 Chat Model Provider Data-Handling and Region Position Plan Critique
description: Independent credibility assessment of the RPI plan and phase details for Issue 163
author: GitHub Copilot
ms.date: 2026-11-15
---

## Critique Summary

* Critique execution: Complete
* Critique verdict: Revise
* Plan path: .copilot-tracking/plans/2026-11-15/issue-163-chat-privacy-region-plan.md
* Phase details path: .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-phase-details.md
* Critique path: .copilot-tracking/reviews/plans/2026-11-15/issue-163-chat-privacy-region-plan-critique.md
* Severity summary: 0 Critical, 2 High, 2 Medium, 1 Low
* Highest-impact finding: PC-001
* Action owner: planning_parent
* Smallest next action: Revise P01, P01-T01, P01-T02, and P03-T01 to align with the actual 8-tuple regulatory_privacy.CRITERIA and no-echo readiness_report(env) invariants, remove the non-existent data_protection.is_synthetic_ref import, scope DataZoneStandard residency classification to EU_DATA_ZONE_REGIONS, add PEP 484 signatures on ChatPrivacy methods called by strict-typed tests, and gate build_foundry_query on evaluate_provider_position(env).
* User response required: No

The candidate plan and phase details establish a strong architectural boundary: isolating the typed validator in `src/core/src/zava_forward/core/chat_provider_position.py` preserves the SQL-portability source guard on `chat_privacy.py`, keeps DPIA decisions `D1`-`D8` and `DATA_MAP` retention guards intact, prevents retention periods from activating before DPO and Legal approval, and honours the focused validation and local-commit workflow on stacked branch `feat/chat-163-privacy-region`. However, cross-checking the plan and phase details against the supplied codebase exposed five concrete contract mismatches (`PC-001` through `PC-005`) that would cause runtime errors, test regressions, or strict `mypy` failures during implementation. Every finding is resolvable by direct planner correction without a new user decision.

## Criterion Boundary and Supplied Inputs

* Plan under review: .copilot-tracking/plans/2026-11-15/issue-163-chat-privacy-region-plan.md
* Phase details under review: .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-phase-details.md
* Caller requirements and task context: Deliver Issue #163 engineering criterion 5 (`Model provider data handling and region position is recorded`) while keeping criterion 2 (`Lawful basis, staff notice and a DPIA decision are recorded by the DPO and Legal; no retention period is set before approval`) explicitly gated on human DPO/Legal sign-off; record and enforce UK South / EU data-zone residency posture, zero model training on customer prompts/completions, abuse-monitoring and content-filtering disclosures, cross-border transfer prohibition without DPO/Legal sign-off, and no active retention period before DPO/Legal approval in `src/core` and canonical privacy reference docs; add deterministic unit tests in `src/core/tests/`; validate at the Focused tier (`src/core` and `src/api` unit tests, `ruff check`, `ruff format --check`, `mypy`, without `tools/rpi-checks.py --all`); commit locally on `feat/chat-163-privacy-region` without pushing or opening a PR.
* Supplied research and evidence: .copilot-tracking/research/2026-11-15/issue-163-chat-privacy-region-research.md (`C1`-`C16`), cross-checked against `src/core/src/zava_forward/core/chat_privacy.py`, `src/core/src/zava_forward/core/regulatory_privacy.py`, `src/core/src/zava_forward/core/data_protection.py`, `src/core/src/zava_forward/core/chat_panel.py`, `src/core/src/zava_forward/core/regulatory_chat.py`, `src/api/src/zava_forward/api/server.py`, `src/core/pyproject.toml`, `src/api/pyproject.toml`, `src/core/tests/test_chat_privacy.py`, `src/core/tests/test_chat_dpia_record.py`, `src/core/tests/test_regulatory_privacy.py`, `src/core/tests/test_regulatory_privacy_audit_217.py`, `src/api/tests/test_content_standard.py`, `src/api/tests/test_chat_panel.py`, `docs/reference/research/chat-memory-dpia.md`, `docs/reference/research/chat-demo-storage-approval-2026-11-01.md`, `docs/reference/README.md`, `docs/reference/log.md`, `src/core/README.md`, and `infra/modules/containerapps.bicep`.
* Dependencies and acceptance criteria: Stacked branch `feat/chat-163-privacy-region` onto `feat/demo-164-chat-grounding-provenance-0900` (PR #1641); Issue #163 remains `Refs #163` because criterion 2 stays human-gated on DPO and Legal sign-off; existing guard suites (`test_chat_dpia_record.py`, `PortabilityTests` in `test_chat_privacy.py`, `Readiness` in `test_regulatory_privacy.py`, and `test_content_standard.py`) must continue to pass alongside strict `mypy` and `ruff`.
* Assessment boundary and limitations: Single-pass read-only verification against supplied repository artefacts and authoritative caller instructions; no live Azure OpenAI / Microsoft Foundry tenant inspection or external legal sign-off exists in repository scope.

## Coverage Assessment

| Area | Status | Notes |
| --- | --- | --- |
| Requirements | Revise | All five contract pillars and the human DPO/Legal gate are represented, but `DataZoneStandard` geography handling (`PC-003`) and `regulatory_privacy` readiness/Foundry enforcement (`PC-001`, `PC-005`) need precision fixes. |
| Research and evidence | Revise | Research `C3` and `C5` contain two codebase inaccuracies carried into the plan: `regulatory_privacy.CRITERIA` has no `id="provider_and_region_position"` dict item (`PC-001`), and `data_protection.py` has no `is_synthetic_ref` helper (`PC-002`). |
| Phases and tasks | Revise | Three-phase decomposition (`P01`-`P03`) and file ownership are clean, including SQL-keyword avoidance in `chat_privacy.py` and plain-language avoidance of standalone `human-approved`; `P01-T01`, `P01-T02`, and `P03-T01` require targeted corrections. |
| Acceptance criteria and validation | Revise | Focused validation commands match caller direction, but strict `mypy` in `src/core` will reject untyped `ChatPrivacy` calls from `test_chat_provider_position.py` unless `ChatPrivacy` method signatures are typed (`PC-004`). |
| Dependencies, decisions, and risks | Pass | Stacked branch lineage (`feat/chat-163-privacy-region`), `Refs #163` non-closure discipline, `D1`-`D8` preservation, and zero-infrastructure/zero-UI scope are properly bounded. |
| Missed concerns | Revise | `readiness_report` enforces a strict no-echo test against reference values and arbitrary `env` strings (`PC-001`), repo synthetic/demo markers include `SYN-*`, `SYNTHETIC-*`, and `chat-demo-breakglass-disclaimer-*` (`PC-002`), and `build_foundry_query` currently omits provider/region gating (`PC-005`). |

## Actionable Findings

### PC-001 - Mismatched regulatory_privacy.CRITERIA schema, parameter name, and no-echo readiness invariant

* Severity: High
* Related IDs: P01, P01-T01, P01-T02, P03-T01, C3
* Evidence: .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-phase-details.md (`P01-T02` lines 130-133; `P03-T01` line 231) vs `src/core/src/zava_forward/core/regulatory_privacy.py` (lines 134-184) and `src/core/tests/test_regulatory_privacy.py` (lines 120-138).
* Concern: `P01-T02` instructs updating criterion 5 (`id="provider_and_region_position"`) `code_control` string and keeping `dpo_accepted: False`, and adding `"provider_position": evaluate_provider_position(source)` to `readiness_report()`, while `P03-T01` asserts criterion 5 `dpo_accepted=False`. In `src/core/src/zava_forward/core/regulatory_privacy.py`, `CRITERIA` is an 8-element tuple of 4-tuples `(cid, text, status, ref)` for Issue #217 (`dpia`, `retention`, `foundry_minimisation`, `entra_roles`, `audit`, `injection_cross_role`, `art22`, `metering`) with no `provider_and_region_position` entry and no `code_control` or `dpo_accepted` keys, and `readiness_report(env: Any)` takes `env` (which may be `None`), not `source`. In addition, `Readiness.test_default_refuses_live_data` (`src/core/tests/test_regulatory_privacy.py` line 124) asserts `len(r["criteria"]) == 8`, and `Readiness.test_report_holds_no_reference_values_or_other_env` (lines 135-138) asserts that `json.dumps(readiness_report({**self.REAL, "OTHER": "PRIVATE-CANARY"}))` contains neither raw reference values nor arbitrary `env` values.
* Impact: Following `P01-T02` and `P03-T01` verbatim either fails with `NameError` / schema errors or breaks `test_regulatory_privacy.py` (`len(r["criteria"]) == 8` and the no-echo privacy test if `evaluate_provider_position` echoes raw `CHAT_TRANSFER_REF`, `CHAT_ABUSE_MONITORING_MODIFIED_REF`, or unapproved `env` string values into `provider_position`).
* Smallest useful change: Keep `regulatory_privacy.CRITERIA` at its existing 8 Issue #217 4-tuples; in `readiness_report(env: Any)`, normalize `mapping = env if isinstance(env, Mapping) else {}`, compute `pos = evaluate_provider_position(mapping)`, attach `"provider_position": pos`, and include `pos["valid"]` in `live_data_permitted`. In `P01-T01`, specify that `evaluate_provider_position` never echoes raw reference strings or arbitrary unapproved `env` values verbatim (emit boolean flags such as `transfer_ref_recorded` and `modified_abuse_monitoring_recorded`, emit allowlisted region/deployment strings or `"unapproved"` when outside the allowlist, and carry `dpo_legal_approved: False` and `documented_terms["dpo_accepted"]: False` inside `provider_position`). Update `P03-T01` item 10 to assert `readiness_report(env)["provider_position"]` and the no-echo invariant rather than a non-existent `CRITERIA` item.
* Action owner: planning_parent
* Resolving evidence: Updated `P01-T01`, `P01-T02`, and `P03-T01` matching `src/core/src/zava_forward/core/regulatory_privacy.py` lines 134-184 and preserving both `len(r["criteria"]) == 8` and `test_report_holds_no_reference_values_or_other_env`.
* Decision route: Direct planner correction

### PC-002 - Non-existent data_protection.is_synthetic_ref import and incomplete synthetic/demo reference detection

* Severity: High
* Related IDs: P01, P01-T01, P01-T02, P03-T01, C5
* Evidence: .copilot-tracking/plans/2026-11-15/issue-163-chat-privacy-region-plan.md (`Sources` line 33; `P01` Dependencies line 104), .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-phase-details.md (`P01-T01` lines 53, 60-61), and .copilot-tracking/research/2026-11-15/issue-163-chat-privacy-region-research.md (`C5`) vs `src/core/src/zava_forward/core/data_protection.py` (lines 184, 217, 249, 381), `src/core/src/zava_forward/core/chat_privacy.py` (line 10), `src/api/tests/test_chat_panel.py` (lines 42-43), and `docs/reference/research/chat-demo-breakglass-disclaimer-2026-11-03.md`.
* Concern: The plan and `P01-T01` instruct importing `is_synthetic_ref` from `zava_forward.core.data_protection`, assuming it already exists alongside `actual_mode`. `data_protection.py` defines `actual_mode` (line 217) and uses inline `.startswith("SYNTH-")` checks (lines 184, 249, 381), so `is_synthetic_ref` does not exist anywhere in `src/`. Furthermore, existing synthetic tests and demo records also use `SYN-*` (for example `SYN-DPIA` and `SYN-BASIS` in `test_chat_panel.py`), `SYNTHETIC-*`, and `chat-demo-breakglass-disclaimer-2026-11-03.md`, while `chat_privacy.py` line 10 states `"A bare yes is not a reference"`.
* Impact: Importing `is_synthetic_ref` from `data_protection` triggers immediate `ImportError` and `mypy` `[attr-defined]` failures, and checking only `SYNTH-*`, `chat-demo-storage-approval-*`, and `chat-memory-dpia.md` under `ZF_DATA_PROCESSING=actual` allows `SYN-*`, `SYNTHETIC-*`, `chat-demo-breakglass-disclaimer-*`, or bare `"yes"`/`"true"` tokens to bypass actual-mode reference rejection.
* Smallest useful change: Import only `actual_mode` from `zava_forward.core.data_protection` in `chat_provider_position.py`, implement `is_demo_or_synthetic_ref(value: str) -> bool` locally in `chat_provider_position.py` covering case-insensitive prefixes `("synth-", "syn-", "synthetic-")` and demo markers `("chat-demo-storage-approval-", "chat-demo-breakglass-disclaimer-", "chat-memory-dpia.md")`, and reject bare affirmative/placeholder tokens (`{"yes", "no", "true", "false", "1", "0", "ok", "approved", "none", "null", "n/a", "unknown", "tbd", "todo"}`) as invalid governance references while continuing to accept `SYNTH-*` / `SYN-*` in non-`actual` synthetic/test modes. Add coverage for `SYN-*` and bare `"yes"` rejection in `P03-T01`.
* Action owner: planning_parent
* Resolving evidence: Updated `Plan` (`Sources`, `P01`) and `P01-T01` / `P01-T02` / `P03-T01` removing the `data_protection.is_synthetic_ref` import and specifying local synthetic/demo/placeholder reference validation.
* Decision route: Direct planner correction

### PC-003 - Unscoped DataZoneStandard residency classification and implicit cross-border flag derivation

* Severity: Medium
* Related IDs: P01-T01, P03-T01, C7, C9, C10
* Evidence: .copilot-tracking/plans/2026-11-15/issue-163-chat-privacy-region-plan.md (`Functional Requirements` line 77), .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-phase-details.md (`P01-T01` lines 66-82; `P03-T01` lines 224-226), and `docs/reference/research/chat-memory-dpia.md` (lines 89-93).
* Concern: `Plan` line 77 and `P01-T01` treat `deployment_type == "DataZoneStandard"` unconditionally as `residency_zone = "eu_data_zone"`. In Azure OpenAI / Microsoft Foundry, `DataZoneStandard` routes processing within the data zone of the resource's geography (EU Data Zone only for EU/EEA regions; US Data Zone for US regions; the UK is outside the EU Data Zone, and domestic `uksouth` residency requires regional `Standard`). Separately, `P01-T01` defaults `CHAT_CROSS_BORDER_TRANSFER` to `"false"`, whereas `P03-T01` item 4 expects `cross_border_transfer=True` whenever an EU data-zone region such as `swedencentral` is configured, even when `CHAT_CROSS_BORDER_TRANSFER` is unset or `"false"`.
* Impact: Pairing `region="uksouth"` or `region="eastus"` with `deployment_type="DataZoneStandard"` can misreport `residency_zone="eu_data_zone"` (or treat `uksouth` + `DataZoneStandard` as an EU data-zone deployment), and relying on raw `CHAT_CROSS_BORDER_TRANSFER` instead of deriving cross-border status from non-`uksouth` residency creates an internal mismatch between `P01-T01` and `P03-T01`.
* Smallest useful change: Specify in `Plan` (`Functional Requirements`) and `P01-T01` that: (1) `region == "uksouth"` permits only `deployment_type == "Standard"` (`residency_zone = "uk_south"`) and rejects `DataZoneStandard` on `uksouth` with `"unapproved_deployment_residency"`; (2) `region in EU_DATA_ZONE_REGIONS` permits `deployment_type in ("Standard", "DataZoneStandard")` (`residency_zone = "eu_data_zone"`), unconditionally derives `cross_border_transfer = True`, and requires a valid `CHAT_TRANSFER_REF`; (3) any region outside `uksouth` and `EU_DATA_ZONE_REGIONS` sets `residency_zone = "unapproved"` and records `"unapproved_region"`; and (4) explicit `CHAT_CROSS_BORDER_TRANSFER=true` also sets `cross_border_transfer = True` and requires `CHAT_TRANSFER_REF`.
* Action owner: planning_parent
* Resolving evidence: Updated `Plan` (`Functional Requirements`) and `P01-T01` / `P03-T01` scoping `DataZoneStandard` to `EU_DATA_ZONE_REGIONS` and defining derived `cross_border_transfer` semantics.
* Decision route: Direct planner correction

### PC-004 - Strict mypy no-untyped-call failure risk between test_chat_provider_position.py and chat_privacy.py

* Severity: Medium
* Related IDs: P01-T02, P03-T01, P03-T02, C11
* Evidence: `src/core/pyproject.toml` (lines 32-68), `src/core/src/zava_forward/core/chat_privacy.py` (lines 113-141, 299-316), `src/core/tests/test_chat_dpia_record.py` (line 61), and .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-phase-details.md (`P01-T02` lines 120-129; `P03-T01` lines 215-248).
* Concern: `src/core/pyproject.toml` enforces `strict = true` (`disallow_untyped_calls = true`, `disallow_untyped_defs = true`) across `src` and `tests`, with legacy `ignore_errors = true` overrides for `zava_forward.core.chat_privacy` and `test_chat_privacy`. In `chat_privacy.py`, `ChatPrivacy.__init__`, `ChatPrivacy.decision`, and `ChatPrivacy.purge_retention` currently lack type annotations (requiring `# type: ignore[no-untyped-call]` in `test_chat_dpia_record.py` line 61). `P03-T01` places `ChatPrivacy` integration assertions (`provider_position()`, `decision()`, pre-approval retention checks) in the new strictly checked `src/core/tests/test_chat_provider_position.py` and prohibits adding `pyproject.toml` exclusions.
* Impact: Running `python3 -m mypy` from `src/core` in `P03-T02` will fail with `[no-untyped-call]` whenever `test_chat_provider_position.py` instantiates `ChatPrivacy` or calls unannotated methods on it.
* Smallest useful change: Specify in `P01-T02` that `ChatPrivacy.__init__`, `ChatPrivacy.provider_position`, `ChatPrivacy.decision`, and `ChatPrivacy.purge_retention` in `src/core/src/zava_forward/core/chat_privacy.py` carry explicit PEP 484 type annotations (`store: Any`, `env: Mapping[str, str] | None = None`, `-> dict[str, Any]`) while avoiding SQL keywords in `chat_privacy.py` so `PortabilityTests` continues to pass.
* Action owner: planning_parent
* Resolving evidence: Updated `P01-T02` requiring typed signatures on the `ChatPrivacy` entrypoints invoked by `src/core/tests/test_chat_provider_position.py`.
* Decision route: Direct planner correction

### PC-005 - regulatory_privacy.build_foundry_query omits evaluate_provider_position(env) enforcement

* Severity: Low
* Related IDs: P01-T02, P03-T01, C3
* Evidence: `src/core/src/zava_forward/core/regulatory_privacy.py` (lines 345-436) and .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-phase-details.md (`P01-T02` lines 130-133).
* Concern: `regulatory_privacy.build_foundry_query(..., env: Any = None)` constructs question-scoped Foundry model query payloads and returns `permitted: bool`. `P01-T02` wires `evaluate_provider_position` into `regulatory_privacy.readiness_report()` in the same file, but leaves `build_foundry_query` able to return `permitted=True` when `env` sets `CHAT_PROVIDER_REGION="eastus"`, `CHAT_DEPLOYMENT_TYPE="GlobalStandard"`, or `CHAT_PROVIDER_TRAINING="true"`.
* Impact: Outbound Foundry query assembly in `regulatory_privacy.py` would bypass the fail-closed provider/region/training contract even when invalid `CHAT_PROVIDER_*` environment settings are supplied directly to `build_foundry_query`. Because `evaluate_provider_position({})` defaults to valid `uksouth` + `Standard`, enforcing it in `build_foundry_query` breaks zero existing `test_regulatory_privacy_audit_217.py` tests.
* Smallest useful change: Extend `P01-T02` so `regulatory_privacy.build_foundry_query` checks `pos = evaluate_provider_position(env if isinstance(env, Mapping) else {})` and fails closed (`permitted=False`, `fields={}`, `manual_path=MANUAL_PATH`, `provider_violations=list(pos["violations"])`) when `not pos["valid"]`, and add one unit test assertion in `P03-T01`.
* Action owner: planning_parent
* Resolving evidence: Updated `P01-T02` and `P03-T01` covering `build_foundry_query` fail-closed enforcement on invalid provider/region `env` settings.
* Decision route: Direct planner correction

## Residual Risks and Limitations

* Live Azure tenant inspection (`ContentLogging` abuse-monitoring exemption status, deployed resource SKU/region drift outside Bicep, and human DPO/Legal sign-off on `D1`-`D8`) cannot be proven in repository code alone; the plan appropriately mitigates this by keeping `dpo_legal_approved: False`, preserving `D1`-`D8` as `"Not recorded"`, and referencing Issue #163 with `Refs #163` rather than closing it.
* `src/core/src/zava_forward/core/chat_privacy.py` has a source-text guard (`PortabilityTests.test_chat_privacy_has_no_own_sql_or_connection`) forbidding `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `CREATE TABLE`, `sqlite3`, and `assistant_connection` anywhere in its raw source text, including docstrings and comments; keeping that constraint explicit during `P01-T02` edits avoids accidental token collisions.

## Recommended Disposition

Return `Revise` to the active `rpi-plan` planning parent. All five findings (`PC-001` through `PC-005`) are direct planner-owned technical corrections grounded in supplied repository files and require no user input or scope change; once applied to the plan and phase details, the plan can be finalized directly without another critique pass.
