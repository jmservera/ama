<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #163 Actual-Mode Provider Gate, Expiry Hold, and Retention Bound Hardening (Cycle 3)

## Metadata

* Task ID: issue-163-chat-privacy-region-c3
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/issue-163-chat-privacy-region-c3-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-c3-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Close Cycle 2 review findings `RV-001` (Medium), `RV-002` (Low), and `RV-003` (Low) on branch `feat/chat-163-privacy-region` (`HEAD` `04e5da42e`) without breaking `constructed`-mode synthetic fixtures (`#281`), `PortabilityTests` SQL-keyword checks in `src/core/tests/test_chat_privacy.py`, banned-phrase checks (`"human-approved"`) in `src/api/tests/test_content_standard.py`, `ChatDpiaRecordGuard` in `src/core/tests/test_chat_dpia_record.py`, existing `test_regulatory_privacy*.py` suites, `ruff`, `mypy`, or `git diff --check`; preserve `DPO_LEGAL_APPROVED = False`, keep `D1` to `D8` as `"Not recorded"`, and leave Cycle 1 and Cycle 2 tracking artifacts untouched.
* Research and evidence considered: .copilot-tracking/plans/2026-11-15/issue-163-chat-privacy-region-c3-plan.md; .copilot-tracking/details/2026-11-15/issue-163-chat-privacy-region-c3-phase-details.md; .copilot-tracking/reviews/logs/2026-11-15/issue-163-chat-privacy-region-c2-review.md; .copilot-tracking/research/2026-11-15/issue-163-chat-privacy-region-research.md; src/core/src/zava_forward/core/chat_provider_position.py; src/core/src/zava_forward/core/chat_privacy.py; src/core/src/zava_forward/core/regulatory_privacy.py; src/core/pyproject.toml; src/core/README.md; docs/reference/research/chat-memory-dpia.md; docs/reference/log.md; src/core/tests/test_chat_provider_position.py; src/core/tests/test_chat_privacy.py; src/core/tests/test_chat_dpia_record.py; src/core/tests/test_regulatory_privacy.py; src/core/tests/test_regulatory_privacy_audit_217.py; src/api/tests/test_content_standard.py; src/api/tests/test_chat_panel.py.
* Decisions, dependencies, and acceptance criteria considered: Focused validation tier only (excluding `tools/rpi-checks.py --all`, remote push, and PR creation); locked test bounds (`0` removals and `0` new test methods in both `src/core/tests/test_chat_provider_position.py` at `13 <= 16` methods and `src/core/tests/test_chat_privacy.py`); human DPO and Legal review (`D1` to `D8`) kept as an open governance follow-up under `Refs #163`.
* Assessment boundary: Evaluates plan and phase-detail completeness, code-path accuracy, type/lint/guard compatibility, and regression-test sufficiency against current workspace state on `feat/chat-163-privacy-region`; does not execute Cycle 3 code edits or substitute for named human DPO and Legal sign-off.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| Cycle 2 `RV-001` (actual-mode DPO/Legal gate in `evaluate_provider_position`) | Covered | `P01-T01` appends `"actual_mode_dpo_legal_unapproved"` to `violations` when `is_actual and not DPO_LEGAL_APPROVED` and gates `transfer_ref_recorded = bool(transfer_ref_valid and (not is_actual or DPO_LEGAL_APPROVED))` in `src/core/src/zava_forward/core/chat_provider_position.py`. Because `DPO_LEGAL_APPROVED: Final[bool] = False` is annotated as `bool`, strict `mypy` in `src/core/pyproject.toml` accepts the guard cleanly. Direct callers (`evaluate_provider_position`, `require_provider_position`, `regulatory_privacy.readiness_report`, `regulatory_privacy.build_foundry_query`, and `GET /api/chat/status`) all fail closed in `ZF_DATA_PROCESSING=actual` mode (including `westeurope` with non-synthetic `CHAT_TRANSFER_REF="TRA-2026-99"`), while `ChatPrivacy._require()` preserves `d["actual_mode_unapproved"]` error precedence before `provider_position` violations and `constructed` mode remains unchanged. |
| Cycle 2 `RV-002` (`ChatPrivacy.purge_expired()` retention hold guard) | Covered | `P01-T01` adds `if not self.decision()["retention_days"]: return 0` at the start of `ChatPrivacy.purge_expired()` in `src/core/src/zava_forward/core/chat_privacy.py`, matching `purge_retention()` immediately below it, introducing zero SQL keywords prohibited by `PortabilityTests`, and preserving `test_expiry_set_and_purged_when_retention_approved` when synthetic retention is active. |
| Cycle 2 `RV-003` (`ChatPrivacy.decision()` oversized digit-string bound) | Covered | `P01-T01` updates `days_valid` in `src/core/src/zava_forward/core/chat_privacy.py` to `1 <= len(days) <= 5 and days.isascii() and days.isdigit() and 1 <= int(days) <= 36500`, short-circuiting before `int(days)` so `"9" * 5000` returns `retention_days=None` without hitting Python 3.12's `4300`-digit `sys.int_max_str_digits` `ValueError`, while accepting all canonical integers in `1..36500`. |
| Documentation, DPIA guard, content standard, and KB log invariants | Covered | `P01-T01` scopes narrative alignment to `src/core/README.md` and `### Runtime residency and data-handling enforcement` in `docs/reference/research/chat-memory-dpia.md`, avoiding `"human-approved"` (`src/api/tests/test_content_standard.py`), preserving `Unknown` data-map cells and `D1` to `D8` `"Not recorded"` cells (`src/core/tests/test_chat_dpia_record.py`), and remaining consistent with the existing uncommitted `[2026-11-15]` entry in `docs/reference/log.md`. |
| `P01` / `P01-T01` (runtime and documentation changes) | Covered | Target files, exact expressions, check ordering, and exclusions are unambiguous and minimal. |
| `P01` / `P01-T02` (regression assertions and focused validation) | Covered | Expands existing test methods in `src/core/tests/test_chat_provider_position.py` (`13` methods preserved, `0` added, `0` removed) and `ChatPrivacyBehaviour` in `src/core/tests/test_chat_privacy.py` (`0` added, `0` removed, inherited by `MemoryStoreChatPrivacy`, `SqlChatPrivacy`, and `MssqlChatPrivacy`) with assertions that fail without each of the three fixes, followed by focused unit, `ruff`, `mypy`, and `git diff --check` verification. |
| Preservation of Cycle 1 and Cycle 2 tracking artifacts | Covered | Explicitly excluded from edit scope in both the candidate plan and phase details. |

## Verdict

* Verdict: Pass
* Rationale: The candidate Cycle 3 plan and phase details close `RV-001`, `RV-002`, and `RV-003` completely and surgically with exact code-level specifications, deterministic failing-before-fix assertions within locked test-method bounds, and verified compatibility with `constructed`-mode synthetic fixtures, `ChatPrivacy._require()` diagnostic precedence, `PortabilityTests`, `ChatDpiaRecordGuard`, `test_content_standard.py`, `test_regulatory_privacy*.py`, strict `mypy`, `ruff`, and `git diff --check`. Zero actionable `PC-xxx` defects or missing evidence items were found.

## Findings

* None. No Critical, High, Medium, or Low planning defects identified.

## Strengths and Residual Risk

* Preserving `ChatPrivacy._require()` check ordering (`missing` -> `synthetic_refs_in_actual_mode` -> `actual_mode_unapproved` -> `provider_position`) while adding `"actual_mode_dpo_legal_unapproved"` inside `evaluate_provider_position()` closes direct `evaluate_provider_position`, `require_provider_position`, and `regulatory_privacy` actual-mode calls without breaking existing `ChatNotApproved` message assertions in `src/core/tests/test_chat_provider_position.py`.
* Expanding `ChatPrivacyBehaviour.test_no_expiry_without_retention` and `ChatPrivacyBehaviour.test_storage_refused_when_provider_or_region_unapproved` automatically exercises both `RV-002` and `RV-003` across in-memory (`MemoryStoreChatPrivacy`) and SQLite (`SqlChatPrivacy`) repositories without adding test methods.
* Accepted governance residual risk: Named human DPO and Legal sign-off on decisions `D1` to `D8` in `docs/reference/research/chat-memory-dpia.md` (`DPO_LEGAL_APPROVED = False`) remains intentionally open outside engineering scope under `Refs #163` criterion 2.
* Implementation hygiene note (non-blocking): Keep plain ASCII punctuation (no em dashes) and avoid trailing blank lines when adding the `"actual_mode_dpo_legal_unapproved"` phrase to `src/core/README.md` and `docs/reference/research/chat-memory-dpia.md` so repository Markdown style and `git diff --check` stay clean.

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* Read-only single-pass critique over supplied Cycle 3 planning artifacts and current workspace files on `feat/chat-163-privacy-region`; runtime test and linter execution belongs to `P01-T02` during `rpi-implement`.

## Recommended Next Action

* Highest-impact finding: none
* Action owner: planning_parent
* Smallest next action: Finalize `.copilot-tracking/plans/2026-11-15/issue-163-chat-privacy-region-c3-plan.md` from `candidate` to `ready` with this `Pass` critique disposition and proceed directly to Cycle 3 `rpi-implement` (`P01-T01`, `P01-T02`).
* User response required: no
