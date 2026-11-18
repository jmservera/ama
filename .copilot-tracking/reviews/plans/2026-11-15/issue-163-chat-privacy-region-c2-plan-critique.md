<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #163 Model Provider Data-Handling and Region Position Remediation (Cycle 2)

## Metadata

* Task ID: issue-163-chat-privacy-region-c2
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/issue-163-chat-privacy-region-c2-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-c2-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Single-pass Cycle 2 remediation plan critique for Issue #163 on `feat/chat-163-privacy-region`, verifying that `P01` and `P02` completely and safely close Cycle 1 post-implementation review findings `RV-001` through `RV-005` under Focused validation while keeping `D1` to `D8` `"Not recorded"` (`DPO_LEGAL_APPROVED = False`) and preserving all existing tests, linters, formatters, and strict `mypy` gates.
* Research and evidence considered: .copilot-tracking/plans/2026-11-15/issue-163-chat-privacy-region-c2-plan.md, .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-c2-phase-details.md, .copilot-tracking/reviews/logs/2026-11-15/issue-163-chat-privacy-region-review.md, .copilot-tracking/research/2026-11-15/issue-163-chat-privacy-region-research.md, src/core/src/zava_forward/core/chat_provider_position.py, src/core/src/zava_forward/core/chat_privacy.py, src/core/src/zava_forward/core/regulatory_privacy.py, src/core/src/zava_forward/core/data_protection.py, src/api/src/zava_forward/api/server.py, src/core/README.md, docs/reference/research/chat-memory-dpia.md, docs/reference/log.md, src/core/pyproject.toml, src/api/pyproject.toml, src/core/tests/test_chat_provider_position.py, src/core/tests/test_chat_privacy.py, src/core/tests/test_chat_dpia_record.py, src/core/tests/test_regulatory_privacy.py, src/core/tests/test_regulatory_privacy_audit_217.py, src/api/tests/test_content_standard.py, and src/api/tests/test_chat_panel.py.
* Decisions, dependencies, and acceptance criteria considered: Cycle 1 defects `RV-001` through `RV-005`; preservation of Cycle 1 artifacts; human DPO/Legal gating (`DPO_LEGAL_APPROVED = False`, `D1` to `D8` `"Not recorded"`); backward compatibility with `PortabilityTests` SQL-keyword scan in `test_chat_privacy.py`, banned-phrase scan (`"human-approved"`) in `test_content_standard.py`, `ChatDpiaRecordGuard` in `test_chat_dpia_record.py`, `constructed` synthetic-ref fixtures, 8-criterion `readiness_report({})` / `readiness_report(self.REAL)` tests, `ruff format --check` (including `src/api/tests/test_chat_panel.py`), strict `mypy` in `src/core` and `src/api`, and `git diff --check`.
* Assessment boundary: Evaluates plan and phase-detail completeness, symbol accuracy, regression safety, and validation coverage against supplied repository sources and Cycle 1 review findings without mutating plan, source, test, or documentation files.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| `RV-001` / `P01-T01` (`ZF_DATA_PROCESSING=actual` blocked while `DPO_LEGAL_APPROVED` is `False`) | Covered | `DPO_LEGAL_APPROVED: Final[bool] = False` in `chat_provider_position.py` and `actual_hold = is_actual and not DPO_LEGAL_APPROVED` in `ChatPrivacy.decision()` / `_require()` cleanly block non-synthetic refs and retention in `actual` mode without affecting `constructed` fixtures, `PortabilityTests`, or `test_content_standard.py`. |
| `RV-002` / `P01-T02` (`regulatory_privacy` `env=None` ambient `os.environ` and non-mapping fail-closed) | Partial | Runtime design (`_provider_env(env)` in `readiness_report(env=None)` and `build_foundry_query(..., env=None)`) is sound and preserves `readiness_report({})` and `readiness_report(self.REAL)`, but `P02-T02` omits regression assertions for `readiness_report()` (`env=None` and non-mapping `env`) required by the Plan Functional Requirement (`PC-001`). |
| `RV-003` / `P01-T01` (`CHAT_RETENTION_DAYS` ASCII `1..36500` bounds) | Covered | `days.isascii() and days.isdigit() and 1 <= int(days) <= 36500` short-circuits `"\u00b2"` without `ValueError` and rejects `"\u0663\u0660"`, `"0"`, negative values, and `"36501"`, matching `regulatory_privacy._parse_retention_days`. |
| `RV-004` / `P01-T01`, `P02-T01` (Conservative unverified `CHAT_ABUSE_MONITORING_MODIFIED_REF` disclosure) | Covered | Adding `modified_abuse_monitoring_verified: False` and keeping `default_sample_retention_days: 30` and `human_review_possible: True` under `mode="modified_recorded_unverified"` aligns `AbuseMonitoringDisclosure`, `MODEL_PROVIDER_CONTRACT`, and `docs/reference/research/chat-memory-dpia.md`. |
| `RV-005` / `P02-T01` (`src/core/README.md` no-echo scope and EOF blank lines) | Covered | Narrowing no-echo claims away from `ChatPrivacy.decision()` (which returns `refs`) and removing trailing EOF blank lines at `docs/reference/log.md:11820` and `docs/reference/research/chat-memory-dpia.md:397` resolves `git diff --check` exit code `2`. |
| `RV-001`–`RV-005` / `P02-T02` (Core and HTTP `/api/chat/status` regression tests) | Partial | HTTP `/api/chat/status` test design in `src/api/tests/test_chat_panel.py` works with `patch.dict(os.environ, ...)` because `app.chat.privacy.env` aliases `os.environ`, but `P02-T02` references a nonexistent method `test_provider_and_pre_approval_retention_gates` in `src/core/tests/test_chat_privacy.py` (`PC-002`) and omits `readiness_report()` `env=None`/non-mapping assertions (`PC-001`). |

## Verdict

* Verdict: Revise
* Rationale: The runtime and documentation remediations in `P01` and `P02-T01` safely close `RV-001` through `RV-005` without breaking existing tests, `PortabilityTests`, `test_content_standard.py`, `ChatDpiaRecordGuard`, `ruff`, or strict `mypy`, but `P02-T02` has an untested Functional Requirement acceptance criterion on `regulatory_privacy.readiness_report()` (`PC-001`) and targets a nonexistent test method name in `src/core/tests/test_chat_privacy.py` under a locked `<= 1 expanded test method` cap (`PC-002`). Both are direct planner corrections requiring no user input.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: `P02-T02` omits regression assertions for `regulatory_privacy.readiness_report()` with `env=None` and non-mapping `env`

* Related IDs: `RV-002`, `P01-T02`, `P02-T02`
* Evidence: .copilot-tracking/plans/2026-11-15/issue-163-chat-privacy-region-c2-plan.md (Functional Requirements for `RV-002` vs `P02-T02` Expected result) and .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-c2-phase-details.md (`P01-T02` vs `P02-T02`)
* Concern: The Functional Requirement for `RV-002` and `P01-T02` modify `regulatory_privacy.readiness_report(env: Any = None)` alongside `build_foundry_query(..., env: Any = None)` and define observable acceptance criteria for both functions when `env=None` (reading `os.environ`) and when `env` is a non-`None`, non-`Mapping` value (failing closed with `unapproved_region` without echoing input). However, `P02-T02` only specifies regression assertions for `build_foundry_query(...)`, leaving the new `readiness_report()` default-argument and malformed-`env` branches untested.
* Impact: Implementation following `P02-T02` literally would leave half of the `RV-002` Functional Requirement acceptance criteria unverified, risking a Cycle 2 `rpi-review` coverage finding or an undetected regression in `readiness_report()`.
* Smallest useful change: Update `P02-T02` in `.copilot-tracking/plans/2026-11-15/issue-163-chat-privacy-region-c2-plan.md` and `.copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-c2-phase-details.md` so `test_regulatory_privacy_readiness_and_foundry_query_enforce_provider_position_no_echo` in `src/core/tests/test_chat_provider_position.py` also asserts `regulatory_privacy.readiness_report()` (omitted `env=None` under `patch.dict(os.environ, {**REAL_REG_REFS, "CHAT_PROVIDER_REGION": "eastus"})` returning `live_data_permitted=False`) and `regulatory_privacy.readiness_report("PRIVATE-ENV-CANARY")` (returning `live_data_permitted=False`, `"unapproved_region"` in `provider_position["violations"]`, and not echoing `"PRIVATE-ENV-CANARY"`).
* Action owner: planning parent
* Exact resolving evidence: `P02-T02` in both Cycle 2 planning artifacts explicitly includes `readiness_report()` `env=None` and non-mapping no-echo assertions alongside `build_foundry_query(...)` within the existing `<= 16` method cap in `src/core/tests/test_chat_provider_position.py`.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Low]: `P02-T02` names nonexistent `test_provider_and_pre_approval_retention_gates` in `src/core/tests/test_chat_privacy.py`

* Related IDs: `RV-001`, `RV-003`, `P02`, `P02-T02`
* Evidence: .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-c2-phase-details.md (`P02` Boundaries and `P02-T02` Intent) and src/core/tests/test_chat_privacy.py (`ChatPrivacyBehaviour`, lines 68-77)
* Concern: `P02` locks `src/core/tests/test_chat_privacy.py` to `<= 1 expanded test method` (`exact removals: none`), and `P02-T02` instructs the implementer to expand `test_provider_and_pre_approval_retention_gates`. No method with that name exists in `src/core/tests/test_chat_privacy.py`; Cycle 1 added `test_storage_refused_when_provider_or_region_unapproved` adjacent to `test_no_retention_period_before_approval` on `ChatPrivacyBehaviour` (inherited by `MemoryStoreChatPrivacy`, `SqlChatPrivacy`, and `MssqlChatPrivacy`).
* Impact: An implementer following `P02-T02` could either fail to locate the target method or add a new method that breaches the `P02` boundary wording (`<= 1 expanded test method` vs adding a new method).
* Smallest useful change: Replace `test_provider_and_pre_approval_retention_gates` in `P02-T02` of `.copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-c2-phase-details.md` with the actual `ChatPrivacyBehaviour` method name `test_storage_refused_when_provider_or_region_unapproved` (or `test_no_retention_period_before_approval`, updating the `P02` count note if both are expanded).
* Action owner: planning parent
* Exact resolving evidence: `P02-T02` in `.copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-c2-phase-details.md` names an existing `ChatPrivacyBehaviour` method in `src/core/tests/test_chat_privacy.py` consistent with the `P02` test-method bound.
* Decision route: direct planner correction

## Strengths and Residual Risk

* **Complete runtime closure of `RV-001` through `RV-004`**: Exporting `DPO_LEGAL_APPROVED: Final[bool] = False` (`__all__` + `typing.Final`), gating `ZF_DATA_PROCESSING=actual` before human DPO/Legal approval, enforcing `days.isascii() and days.isdigit() and 1 <= int(days) <= 36500`, keeping `default_sample_retention_days: 30` and `human_review_possible: True` when `CHAT_ABUSE_MONITORING_MODIFIED_REF` is unverified, and routing `env=None` to `os.environ` in `regulatory_privacy` (while importing `os` in `regulatory_privacy.py`) resolve every Cycle 1 code defect cleanly.
* **Verified guard compatibility across core and API**:
  * `PortabilityTests.test_chat_privacy_has_no_own_sql_or_connection` in `src/core/tests/test_chat_privacy.py`: none of the planned `chat_privacy.py` identifiers, docstrings, or `ChatNotApproved` messages trigger banned SQL tokens (`INSERT OR`, `REPLACE INTO`, `AUTOINCREMENT`, `PRAGMA`, `sqlite3`, `CREATE TABLE`, `chat.sqlite`, `executescript`, `OBJECT_ID`, or `(SELECT|DELETE FROM|INSERT INTO|UPDATE).*chat_`).
  * `CopyAudit.test_ai_label_is_exact_and_never_implies_approval` in `src/api/tests/test_content_standard.py`: planned strings contain no prohibited `"human-approved"` phrasing.
  * `ChatDpiaRecordGuard` in `src/core/tests/test_chat_dpia_record.py`: planned `docs/reference/research/chat-memory-dpia.md` updates preserve `Unknown` retention prefixes, `"Not recorded"` across `D1` to `D8`, and all required `## Model provider and region` tokens (keep plain ASCII punctuation such as `D1 to D8` rather than Unicode dashes in prose edits).
  * `src/api/tests/test_chat_panel.py` and `ruff`/`mypy`: `app.chat = ChatIsolation(store)` binds `app.chat.privacy.env` directly to `os.environ`, so `patch.dict(os.environ, ...)` dynamically toggles `/api/chat/status` in `PanelTests`; `src/api/tests/test_chat_panel.py` is formatted under `ruff format --check` (not in `src/api/pyproject.toml` `[tool.ruff.format].exclude`), which `P02-T02` explicitly validates.
* **Accepted residual risk**: Decisions `D1` to `D8` in `docs/reference/research/chat-memory-dpia.md` remain `"Not recorded"` (`DPO_LEGAL_APPROVED = False`) pending named human DPO and Legal review (`Refs #163`).

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* Critique is static and read-only; unit suites, `ruff`, `mypy`, and `git diff --check` execute during `P02-T02` implementation.

## Recommended Next Action

* Highest-impact finding: `PC-001`
* Action owner: planning parent
* Smallest next action: Directly revise `P02-T02` in `.copilot-tracking/plans/2026-11-15/issue-163-chat-privacy-region-c2-plan.md` and `.copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-c2-phase-details.md` to resolve `PC-001` and `PC-002`, then finalize the Cycle 2 plan without another critique pass.
* User response required: no
