<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #163 Explicit Deployment Attestation in Actual Mode and IaC Mismatch Disclosure (Cycle 4)

## Metadata

* Task ID: issue-163-chat-privacy-region-c4
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/issue-163-chat-privacy-region-c4-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-c4-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Close Cycle 3 post-implementation review finding `RV-001` (Medium) on branch `feat/chat-163-privacy-region` (`HEAD` `04e5da42e`) inside `src/core` and `docs/reference/` without editing `infra/` (Focused validation tier; `tools/rpi-checks.py --all` prohibited by caller), without breaking `constructed`-mode synthetic fixtures (`#281`, `#891`), `ChatDpiaRecordGuard` in `src/core/tests/test_chat_dpia_record.py`, `src/api/tests/test_content_standard.py`, `ruff`, `mypy`, or `git diff --check`, and while preserving `DPO_LEGAL_APPROVED = False`, `D1` to `D8` `"Not recorded"`, and Cycle 1 to Cycle 3 RPI artifacts intact.
* Research and evidence considered: .copilot-tracking/plans/2026-11-15/issue-163-chat-privacy-region-c4-plan.md; .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-c4-phase-details.md; .copilot-tracking/reviews/logs/2026-11-15/issue-163-chat-privacy-region-c3-review.md; src/core/src/zava_forward/core/chat_provider_position.py; src/core/src/zava_forward/core/chat_privacy.py; src/core/src/zava_forward/core/regulatory_privacy.py; src/core/src/zava_forward/core/data_protection.py; src/core/pyproject.toml; src/core/README.md; docs/reference/research/chat-memory-dpia.md; docs/reference/log.md; infra/main.bicep; infra/modules/containerapps.bicep; src/core/tests/test_chat_provider_position.py; src/core/tests/test_chat_privacy.py; src/core/tests/test_chat_dpia_record.py; src/core/tests/test_regulatory_privacy.py; src/core/tests/test_regulatory_privacy_audit_217.py; src/api/tests/test_content_standard.py; src/api/tests/test_chat_panel.py.
* Decisions, dependencies, and acceptance criteria considered: Focused validation tier (`infra/` edits routed as a separate Full-tier IaC follow-up item); locked test-method ceiling in `src/core/tests/test_chat_provider_position.py` (`0` removals, `0` new methods, preserving `13` methods); preserved `constructed`-mode synthetic fallback (`uksouth` and `Standard` with `deployment_attested = False`); human DPO and Legal review (`D1` to `D8`) retained as an open governance follow-up under `Refs #163`.
* Assessment boundary: Evaluates plan and phase-detail logic, type/lint/guard compatibility, caller propagation across `src/core` and `src/api`, and unit-test sufficiency against current workspace files on `feat/chat-163-privacy-region`; does not execute Cycle 4 edits, modify `infra/`, or substitute for named human DPO and Legal sign-off.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| Cycle 3 `RV-001` actual-mode omitted-setting fail-closed gate (`unattested_region_in_actual_mode`, `unattested_deployment_in_actual_mode`) | Covered | `P01-T01` checks `region_explicit` (`region is not None or "CHAT_PROVIDER_REGION" in source_env`) and `deployment_explicit` (`deployment_type is not None or "CHAT_DEPLOYMENT_TYPE" in source_env`), failing closed when `is_actual` is `True` and either setting is omitted while preserving blank-string `"unapproved_region"` / `"unapproved_deployment_residency"` rejections (including `regulatory_privacy._provider_env` non-Mapping guard) and avoiding false `requires_transfer_signoff` flags on omitted actual-mode region checks. |
| Cycle 3 `RV-001` `deployment_attested` contract across all modes (`P01-T01`) | Partial | `MODEL_PROVIDER_CONTRACT["deployment_attested"] = False` and `ProviderPositionEvaluation.deployment_attested: bool` are typed cleanly for strict `mypy`, and `constructed` defaults return `deployment_attested = False`. However, the `P01-T01` boolean formula (`safe_deployment != "unapproved"`) evaluates `deployment_attested = True` on prohibited `uksouth` + `DataZoneStandard` inputs because `safe_deployment` stays `"DataZoneStandard"` (`PC-001`). |
| Cycle 3 `RV-001` documentation of `infra/main.bicep` `chatModelSku = 'GlobalStandard'` mismatch (`P01-T01`) | Covered | `infra/main.bicep` (line 136) defaults `chatModelSku` to `'GlobalStandard'` and `infra/modules/containerapps.bicep` (lines 237 to 243) omits `CHAT_PROVIDER_REGION` and `CHAT_DEPLOYMENT_TYPE`. Documenting this mismatch and the actual-mode attestation rule in `docs/reference/research/chat-memory-dpia.md` (under `## Model provider and region`) and `src/core/README.md` without touching `infra/` satisfies Focused-tier boundaries, `ChatDpiaRecordGuard`, and `test_content_standard.py`. |
| `P01-T02` unit assertions and locked `13`-method test bound | Partial | Expanding `test_default_uksouth_standard_position_is_valid_and_not_dpo_accepted`, `test_actual_data_mode_rejects_synthetic_and_demo_references`, and `test_regulatory_privacy_readiness_and_foundry_query_enforce_provider_position_no_echo` preserves the `13`-method ceiling and keeps `constructed`-mode fixtures (`#281`, `#891`) passing, but misses assertions for `deployment_attested is False` on `uksouth` + `DataZoneStandard` and `MODEL_PROVIDER_POSITION["deployment_attested"] is False` (`PC-001`). |
| Preservation of Cycle 1 to Cycle 3 artifacts and Focused validation scope | Covered | `infra/`, Cycle 1 to Cycle 3 RPI artifacts, and `tools/rpi-checks.py --all` are explicitly excluded in both the plan and phase details. |

## Verdict

* Verdict: Revise
* Rationale: The candidate Cycle 4 plan and phase details accurately isolate Cycle 3 `RV-001` within Focused `src/core` and `docs/reference/` boundaries while preserving `constructed`-mode synthetic fixtures, `ChatPrivacy._require()` diagnostic precedence, `ChatDpiaRecordGuard`, and `test_content_standard.py`. One substantive logic defect (`PC-001` Medium) in `P01-T01` and `P01-T02` requires a direct planner correction before finalization: `safe_deployment != "unapproved"` sets `deployment_attested = True` for the unapproved `uksouth` + `DataZoneStandard` combination because `chat_provider_position.py` preserves `safe_deployment = "DataZoneStandard"` when recording `"unapproved_deployment_residency"`.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: `P01-T01` `deployment_attested` formula evaluates `True` on prohibited `uksouth` + `DataZoneStandard` configurations and `P01-T02` omits regression assertions for that path and `MODEL_PROVIDER_POSITION`

* Related IDs: Functional Requirement 1 (`deployment_attested`), `P01`, `P01-T01`, `P01-T02`
* Evidence: .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-c4-phase-details.md (lines 75 and 79); .copilot-tracking/plans/2026-11-15/issue-163-chat-privacy-region-c4-plan.md (lines 54 to 58 and 97); src/core/src/zava_forward/core/chat_provider_position.py (lines 301 to 309); src/core/tests/test_chat_provider_position.py (lines 68 to 86).
* Concern: In `src/core/src/zava_forward/core/chat_provider_position.py` (lines 305 to 307), when `CHAT_PROVIDER_REGION="uksouth"` and `CHAT_DEPLOYMENT_TYPE="DataZoneStandard"`, `residency_zone` is `"uk_south"` (`!= "unapproved"`) and `safe_deployment` is set to `canonical_deployment` (`"DataZoneStandard"`, which is also `!= "unapproved"`) while appending `"unapproved_deployment_residency"` to `violations`. Consequently, the `P01-T01` expression `deployment_attested = bool(region_explicit and deployment_explicit and residency_zone != "unapproved" and safe_deployment != "unapproved")` returns `True` on an unapproved residency-SKU combination, contradicting the plan's Functional Requirement that both region and deployment SKU must resolve to approved values. In addition, `P01-T02` does not assert `pos["deployment_attested"] is False` in `test_uksouth_rejects_datazone_standard_because_uk_outside_eu_data_zone` or `MODEL_PROVIDER_POSITION["deployment_attested"] is False` (mirroring `MODEL_PROVIDER_CONTRACT["deployment_attested"]`) in `test_default_uksouth_standard_position_is_valid_and_not_dpo_accepted`.
* Impact: Callers inspecting `provider_position["deployment_attested"]` (including `GET /api/chat/status`, `ChatPrivacy.decision()`, and `regulatory_privacy.readiness_report()`) would report `deployment_attested = True` when `uksouth` is paired with `DataZoneStandard`, even though `DataZoneStandard` is unapproved outside `eu_data_zone`.
* Smallest useful change: In `P01-T01`, gate `deployment_attested` on approved residency and deployment checks (for example, track `deployment_approved = True` only in the valid `else` branch of deployment validation or check `"unapproved_region" not in violations and "unapproved_deployment_residency" not in violations` alongside `region_explicit and deployment_explicit`). In `P01-T02` (within the existing `13` test methods), assert `self.assertFalse(MODEL_PROVIDER_POSITION["deployment_attested"])` in `test_default_uksouth_standard_position_is_valid_and_not_dpo_accepted` and `self.assertFalse(pos["deployment_attested"])` in `test_uksouth_rejects_datazone_standard_because_uk_outside_eu_data_zone`.
* Action owner: planning_parent
* Exact resolving evidence: Updated `P01-T01` and `P01-T02` in `.copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-c4-phase-details.md` (and synchronized `Critique Disposition` in `.copilot-tracking/plans/2026-11-15/issue-163-chat-privacy-region-c4-plan.md`) ensuring `deployment_attested` is `False` whenever `"unapproved_deployment_residency"` or `"unapproved_region"` is present and locking both unit assertions without adding test methods.
* Decision route: direct_planner_correction

## Strengths and Residual Risk

* Preserving `region_explicit` and `deployment_explicit` via key-presence (`"CHAT_PROVIDER_REGION" in source_env` and `"CHAT_DEPLOYMENT_TYPE" in source_env`) cleanly separates omitted container settings (`unattested_region_in_actual_mode` / `unattested_deployment_in_actual_mode` in `actual` mode; `uksouth` / `Standard` synthetic fallback with `deployment_attested = False` in `constructed` mode) from explicit blank or malformed values (`unapproved_region` / `unapproved_deployment_residency` in all modes, including `regulatory_privacy._provider_env` non-Mapping inputs).
* Narrowing `requires_transfer_signoff` to `residency_zone == "eu_data_zone" or (region_explicit and raw_region != PRIMARY_REGION) or canonical_deployment == "DataZoneStandard" or explicit_transfer` prevents an omitted `CHAT_PROVIDER_REGION` in `ZF_DATA_PROCESSING=actual` from emitting a spurious `"cross_border_transfer_unapproved"` violation while preserving existing behavior for explicit non-domestic or blank regions.
* Accepted governance and Full-tier residual risks: Named human DPO and Legal sign-off on decisions `D1` to `D8` in `docs/reference/research/chat-memory-dpia.md` (`DPO_LEGAL_APPROVED = False`) and Full-tier IaC alignment of `infra/main.bicep` (`chatModelSku`) plus `infra/modules/containerapps.bicep` (`CHAT_PROVIDER_REGION`, `CHAT_DEPLOYMENT_TYPE`) remain explicitly tracked in `## Follow-Up Items` outside Focused Issue #163 scope.

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* Single-pass read-only critique of supplied Cycle 4 planning artifacts and current workspace files on `feat/chat-163-privacy-region`; test, lint, format, and type execution belongs to `P01-T02` during `rpi-implement`.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning_parent
* Smallest next action: Apply the direct planner correction for `PC-001` in `.copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-c4-phase-details.md` (`P01-T01` and `P01-T02`), record the critique disposition and set `Planning status: ready` in `.copilot-tracking/plans/2026-11-15/issue-163-chat-privacy-region-c4-plan.md`, and proceed to Cycle 4 `rpi-implement` without another critique pass.
* User response required: no
