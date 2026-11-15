<!-- markdownlint-disable-file -->
# Review: Issue #104 Cross-Capability Bounded AI Enforcement and Verification

## Scope and Evidence

* Task ID: issue-104-bounded-ai-invariants
* Review date: 2026-11-15
* Review scope: Full task (`P01`, `P02`, `P03`)
* Assessed boundary: Requirements `FR-1`–`FR-4`, `NFR-1`–`NFR-3`, acceptance criteria `AC-1`–`AC-4`, critique dispositions `PC-001`–`PC-005`, `src/core` and `src/agents` runtime enforcement and 13-capability verification suites, and Focused validation evidence (`unittest`, `ruff`, `mypy`, excluding `tools/rpi-checks.py`).
* Plan: .copilot-tracking/plans/2026-11-15/issue-104-bounded-ai-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-104-bounded-ai-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/issue-104-bounded-ai-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/issue-104-bounded-ai-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/issue-104-bounded-ai-research.md, working-tree `git diff`, new modules `src/core/src/zava_forward/core/bounded_ai.py` and `src/core/tests/test_epic104_bounded_ai_invariants.py`, and independent read-only adversarial code-review lens.

## Opening Review State

* Interpreted review goal: Independently verify that the delivered `src/core` and `src/agents` implementation, cross-capability contract (`zava_forward.core.bounded_ai`), 13-capability invariant suites, and Focused validation evidence satisfy `FR-1`–`FR-4`, `NFR-1`–`NFR-3`, `AC-1`–`AC-4`, and `PC-001`–`PC-005` without defects or scope drift.
* Review scope: Full task (`P01`, `P02`, `P03`)
* Evidence readiness: Ready; plan markers (`P01`–`P03` all `[x]`), phase details, critique dispositions (`PC-001`–`PC-005`), changes log, and Focused validation outputs are complete and reconciled.
* Acceptance basis: `FR-1`–`FR-4`, `NFR-1`–`NFR-3`, `AC-1`–`AC-4`, and resolved critique items `PC-001`–`PC-005` in .copilot-tracking/plans/2026-11-15/issue-104-bounded-ai-plan.md.
* First comparison boundary: Reconcile `P01`, `P02`, and `P03` completed-work evidence and actual `src/core` + `src/agents` source/test diffs against `AC-1`–`AC-4` and `PC-001`–`PC-005`.
* Active read-only boundaries: Read-only evidence inspection across `src/core`, `src/agents`, and `.copilot-tracking/` inputs; write authority restricted exclusively to `.copilot-tracking/reviews/logs/2026-11-15/issue-104-bounded-ai-review.md` and RPI session state JSON.
* Initial blockers: None

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass post-implementation review on 2026-11-15 across `.copilot-tracking/plans/2026-11-15/issue-104-bounded-ai-plan.md`, `.copilot-tracking/details/2026-11-15/issue-104-bounded-ai-phase-details.md`, `.copilot-tracking/reviews/plans/2026-11-15/issue-104-bounded-ai-plan-critique.md`, `.copilot-tracking/changes/2026-11-15/issue-104-bounded-ai-changes.md`, `.copilot-tracking/research/2026-11-15/issue-104-bounded-ai-research.md`, full working-tree `git diff` across `src/core` and `src/agents`, new modules `src/core/src/zava_forward/core/bounded_ai.py` and `src/core/tests/test_epic104_bounded_ai_invariants.py`, Focused validation outputs (`3,580` `src/core` unit tests, `533` `src/agents` unit tests, `ruff check`, `ruff format --check`, and `mypy` across `344` + `66` files), and an independent read-only adversarial code-review lens.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`–`P01-T03`) | `P01: Core Bounded-AI Enforcement and Cross-Capability Contract` | Reconciled | All three tasks checked `[x]`, documented with exact file/symbol evidence, and verified by `src/core` unit tests, `ruff`, and `mypy`. |
| `P02` (`P02-T01`–`P02-T02`) | `P02: Agents Capability Attribution and Named-Human Authorization Hardening` | Reconciled | Both tasks checked `[x]`, documented with exact file/symbol evidence, and verified by `src/agents` unit tests, `ruff`, and `mypy`. |
| `P03` (`P03-T01`–`P03-T02`) | `P03: Cross-Capability Acceptance Verification Suites and Focused Validation` | Reconciled | Both tasks checked `[x]`; test-count budgets respected (`17 <= 20` methods in `src/core/tests/test_epic104_bounded_ai_invariants.py`; `+5 <= 12` added methods in `src/agents/tests/test_epic104_bounded_ai_invariants.py`); `src/api/tests/test_content_standard.py` verified clean (`29` tests). |
| `Follow-Up Items` | Optional future `src/api` startup diagnostic exposing `bounded_ai.audit_registered_capabilities()` | Reconciled | Preserved outside active `P01`–`P03` scope in both the plan and changes record. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/core/src/zava_forward/core/ai_registry.py`, `src/core/src/zava_forward/core/ai.py` | Added `is_dispatch_enabled` and `consumption_capability`; hardened `authorizes_live` with `rai_release.named_human`; enforced registration/enabled guards in `Ai.run` and at entry of `Ai.look_at`, binding hyphenated capability IDs into `CallContext`. | Working-tree diff and `AiDispatchGateBypassRegressionTest` + `RegistryAndAuditContractTest` in `src/core/tests/test_epic104_bounded_ai_invariants.py`. | Passed (`ruff check`, `mypy`, `3,580` `src/core` unit tests) | Reconciled and conformant with `FR-1`, `AC-3`, `PC-001`, `PC-005`. |
| `P01-T02` | `src/core/src/zava_forward/core/ai_consumption.py` | Rejected blank `authority`/`owner`/`evidence`; enforced `rai_release.named_human` on `owner`/`alert_owner` and `rai_release.named` on `alert` for non-synthetic or alert-bearing authorities; blocked non-synthetic `price(...)` swap against unbounded pre-existing authorities; added `Consumption.non_exercise_status(...)`. | Working-tree diff and `NonExerciseConsumptionAndReleaseBoundsTest` in `src/core/tests/test_epic104_bounded_ai_invariants.py`. | Passed (`ruff check`, `ruff format --check`, `mypy`, `3,580` `src/core` unit tests) | Reconciled and conformant with `FR-2`, `AC-2`, `AC-3`, `PC-001`. |
| `P01-T03` | `src/core/src/zava_forward/core/bounded_ai.py` | Created strictly typed cross-capability contract covering 13-capability inventory parity, partitioned controlled-record snapshots (`Store` cases, deterministic `ranking`, aftercare `concerns`/`closures` vs. `funding_draft`/`read_document` workspace slots), recursive `enforce_proposal_only` (`_iter_mapping_keys`, resolving `F-003`), plain-language content-standard compliant docstring (`"approved by a named human"`, resolving `F-001`), `verify_non_exercise_enablement`, and `audit_registered_capabilities`. | Module inspection, `src/core/tests/test_epic104_bounded_ai_invariants.py`, and `src/api/tests/test_content_standard.py`. | Passed (`ruff check`, `ruff format --check`, `mypy --strict` across `348` files, `29` `test_content_standard` tests) | Reconciled and conformant with `FR-3`, `NFR-1`, `NFR-2`, `PC-001`, `PC-004`. |
| `P02-T01` | `src/agents/src/zava_forward/agents/chat.py` | Bound `CallContext(..., CHAT_TASK, ...)` in `ChatModel.__call__` when `CURRENT.get()` is `None`, preventing fallback to `"evidence"` while preserving outer `ChatPanel` context. | Working-tree diff and `ChatBoundaries.test_direct_chat_model_call_binds_chat_task_context_and_preserves_outer_panel_context`. | Passed (`ruff check`, `ruff format --check`, `mypy`, `533` `src/agents` unit tests) | Reconciled and conformant with `FR-2`, `AC-3`. |
| `P02-T02` | `src/agents/src/zava_forward/agents/chat_eval.py`, `src/agents/src/zava_forward/agents/heldout_batch.py` | Enforced `rai_release.named_human` on `authorised_by` and non-empty `approved_by`, blocking system/agent/bot/placeholder strings before any model call. | Working-tree diff and `HeldOutAdapters.test_heldout_and_chat_eval_reject_non_human_or_placeholder_approvers`. | Passed (`ruff check`, `ruff format --check`, `mypy`, `533` `src/agents` unit tests) | Reconciled and conformant with `FR-2`, `AC-2`, `AC-3`. |
| `P03-T01` | `src/core/tests/test_epic104_bounded_ai_invariants.py` | Added 17 strictly typed core acceptance tests (including recursive nested forbidden mutation-key rejection) across JSON `Store` and SQLite `SqlStore` covering all 13 capabilities for both Issue #104 invariants. | `Ran 17 tests in 3.804s OK`; `src/api/tests/test_content_standard.py` `Ran 29 tests in 0.425s OK`; `mypy` `348` files clean without touching `pyproject.toml`. | Passed | Reconciled and conformant with `FR-4`, `NFR-2`, `NFR-3`, `AC-1`–`AC-4`, `PC-003`. |
| `P03-T02` | `src/agents/tests/test_epic104_bounded_ai_invariants.py` | Added 5 focused cross-capability and regression tests (`27` total in file, `<= 12` addition cap) and executed complete Focused validation in workspace-local gitignored `.venv`. | `Ran 27 tests in 14.946s OK`; full `src/agents` suite `Ran 533 tests in 344.872s OK`; `mypy` `66` files clean; `git status --short` clean of `.venv`/`/tmp` artifacts. | Passed | Reconciled and conformant with `FR-4`, `NFR-1`–`NFR-3`, `AC-1`–`AC-4`, `PC-002`. |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P01-T03` (`bounded_ai.py`) | Extracted legacy task IDs from `dict(ai_registry.LEGACY)` keys and checked `prohibited_uses` and `limits` string lists via `rai_release.strings` to match `ai_registry.REQUIRED_FIELDS`. | Direct inspection of `src/core/src/zava_forward/core/ai_registry.py` during `P03-T01` execution; ordinary local judgment requiring no user decision. | Recorded in `.copilot-tracking/changes/2026-11-15/issue-104-bounded-ai-changes.md` under `## Implementation-Time Plan and Detail Updates`. | Not needed (preserves `FR-3` intent and `PC-001`–`PC-005` dispositions). | Reconciled. |
| `F-001`, `F-003` (`bounded_ai.py`, `test_epic104_bounded_ai_invariants.py`) | Replaced `"named-human-approved"` with `"approved by a named human"` to satisfy `CopyAudit.test_ai_label_is_exact_and_never_implies_approval` in `src/api/tests/test_content_standard.py` (`F-001`), and added `_iter_mapping_keys` recursive nested-key enforcement in `bounded_ai.enforce_proposal_only` with dedicated unit test coverage (`F-003`). | Independent `code-review-functional` audit (`/tmp/independent-review-104-757cd9b2a.md`) and explicit caller remediation instruction. | Recorded in `.copilot-tracking/changes/2026-11-15/issue-104-bounded-ai-changes.md`, `.copilot-tracking/plans/2026-11-15/issue-104-bounded-ai-plan.md`, and this review log. | Not needed (directly tightens `FR-3` and restores cross-package `src/api` content-standard guard). | Reconciled and verified. |

## Critique and Material Revision Assessment

* Latest critique dispositions: All five single-pass plan critique findings (`PC-001` through `PC-005`) and accepted residual policy boundary `OD-51` are explicitly disposed in `.copilot-tracking/plans/2026-11-15/issue-104-bounded-ai-plan.md` (`## Critique Disposition`) and verified in the delivered code and tests.
* Material revisions: None occurred during implementation; no scope, requirement, architecture, or acceptance-criteria divergence arose.
* Dependent-work pause assessment: Execution followed dependency order (`P01` -> `P02` -> `P03`) with no premature resumption or critique loop.
* Justification assessment: Supported by concrete source diffs and passing Focused validation across `src/core` and `src/agents`.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Optional future `src/api` startup diagnostic exposing `bounded_ai.audit_registered_capabilities()` on an operator health/readiness surface | Caller scoped this slice strictly to `src/core` and `src/agents` (`Non-Goals` excludes `src/api`). | Future Issue #104 `src/api` slice owner / post-Review follow-up selection. | Open non-blocking follow-up; kept outside active `P01`–`P03` scope and routed to distinct follow-up queue. |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Harden `bounded_ai.verify_non_exercise_enablement` helper defaults against direct caller misuse outside `Store`/`AgentWorker`

* Related scope: `P01-T03` (`src/core/src/zava_forward/core/bounded_ai.py`)
* Evidence: Independent adversarial review lens noted that `bounded_ai.verify_non_exercise_enablement` defaults `bound_keys: Sequence[str] = ()` and checks `approval_state not in (None, "", "unapproved", "unknown")` rather than an allowlist (`"approved"` / `"operational_release"`) with mandatory non-empty `bound_keys`, `configuration`, and `model` (note: nested-key recursion on `FORBIDDEN_MUTATION_KEYS` in `bounded_ai.enforce_proposal_only` was resolved directly via `_iter_mapping_keys` under `F-003`).
* Impact: Non-material within current runtime paths (where `ai_registry` is immutable offline scaffolding with `approval_state="unapproved"` and `Store` binds `ai_gate`/`ai_release`), but tightening `verify_non_exercise_enablement` helper defaults will make standalone callers in future slices (`src/api` / `src/orchestrator`) even harder to misconfigure.
* Destination: `follow-up`
* Smallest useful next action: In a follow-up hardening task, require explicit `approval_state == "approved"`, default `bound_keys` to `rai_release.TRIGGER_KEYS` union, and require non-`None` `configuration` and `model` in `verify_non_exercise_enablement`.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Distinguish static configuration validity from remaining budget capacity in `Consumption.non_exercise_status`

* Related scope: `P01-T02` (`src/core/src/zava_forward/core/ai_consumption.py`)
* Evidence: Independent adversarial review lens observed that `Consumption.non_exercise_status(...)` verifies unexpired authority, non-synthetic price, human-owned alert, and finite positive limits (`allowed=True` when configured), whereas dynamic call/token/money exhaustion is enforced by `Consumption.reserve(...)` (`DispatchHeld`).
* Impact: Non-material to runtime enforcement (`Consumption.reserve` deterministically holds exhausted calls, tokens, and money across all 13 capabilities, verified in `Nfr012Limits` and `NonExerciseConsumptionAndReleaseBoundsTest`), but exposing `exhausted` / remaining-budget fields on `non_exercise_status` will prevent operator confusion if surfaced on a health endpoint.
* Destination: `follow-up`
* Smallest useful next action: Extend `Consumption.non_exercise_status` with remaining call/token/amount capacity summary when wiring `bounded_ai` diagnostics into `src/api`.

## Defects

* none

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` [Low] | `follow-up` | Post-Review follow-up candidate (rank 1) | Non-blocking defensive hardening of `bounded_ai` standalone helper defaults beyond current `FR-3` contract. |
| `RV-002` [Low] | `follow-up` | Post-Review follow-up candidate (rank 2, paired with `src/api` diagnostic follow-up) | Non-blocking observability enrichment on `Consumption.non_exercise_status`; runtime exhaustion holds already enforced by `Consumption.reserve`. |

Later implementation of a routed finding does not require another Review.

## Residual Work

* `RV-001` [Low]: Optional defensive tightening of `bounded_ai.verify_non_exercise_enablement` default `bound_keys` / `approval_state` allowlist.
* `F-002` [Low]: Optional `Consumption.authorize` / `Consumption.price` digest-check cleanup (`rai_release.named_human` validation before `reference()` hashing when `known` price is not yet registered).
* `RV-002` [Low] + Plan Follow-Up: Optional `src/api` operator readiness diagnostic exposing `bounded_ai.audit_registered_capabilities()` and remaining budget capacity in `Consumption.non_exercise_status`.

## Blockers and Remaining Work

* Blockers: None (`AC-5` local git commit is executed by the parent workflow immediately upon Review completion per caller instructions).
* Remaining active work: None in `P01`–`P03`.

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `../../.venv/bin/ruff check .` | `src/core` | Passed | `All checks passed!` (exit 0) |
| `../../.venv/bin/ruff format --check .` | `src/core` | Passed | `295 files already formatted` (exit 0) |
| `../../.venv/bin/mypy` | `src/core` | Passed | `Success: no issues found in 348 source files` (exit 0) |
| `PYTHONPATH=src/core/src:src/core/tests python3 -m unittest src/core/tests/test_epic104_bounded_ai_invariants.py -v` | `src/core` | Passed | `Ran 17 tests in 3.804s OK` (exit 0) |
| `PYTHONPATH=src/core/src:src/agents/src:src/api/src:src/core/tests:src/agents/tests python3 -m unittest src/api/tests/test_content_standard.py -v` | `src/api` | Passed | `Ran 29 tests in 0.425s OK` (exit 0; verifies `F-001` fix) |
| `PYTHONPATH=tests ../../.venv/bin/python -m unittest discover -s tests -q` + `test_device_registry_azure.py` | `src/core` | Passed | All discovered tests passed (`test_device_registry_azure.py`: `Ran 39 tests in 0.726s OK`) |
| `ruff check .` | `src/agents` | Passed | `All checks passed!` (exit 0) |
| `ruff format --check .` | `src/agents` | Passed | `62 files already formatted` (exit 0) |
| `mypy --python-executable ../../.venv/bin/python` | `src/agents` | Passed | `Success: no issues found in 66 source files` (exit 0) |
| `PYTHONPATH=src/core/src:src/agents/src:src/core/tests:src/agents/tests python3 -m unittest src/agents/tests/test_epic104_bounded_ai_invariants.py -q` | `src/agents` | Passed | `Ran 27 tests in 6.553s OK` (full `src/agents` suite `533` tests passed, exit 0) |
| `grep -rn '\.copilot-tracking'` | Changed/new `src/` files | Passed | Zero `.copilot-tracking/` references in source or test files |
| `python3 tools/rpi-checks.py` | Repository | Skipped | Explicitly excluded by caller direction (`Focused` validation tier) |

## Outcome

* Outcome: Conformant
* Outcome rationale: Every planned requirement (`FR-1`–`FR-4`, `NFR-1`–`NFR-3`), engineering acceptance criterion (`AC-1`–`AC-4`), and plan-critique disposition (`PC-001`–`PC-005`) is implemented, reconciled, and verified across all 13 registered AI capabilities in `src/core` and `src/agents` with zero material findings, zero defects, zero decision gaps, and zero evidence gaps. Two low-severity, non-blocking defensive/observability enhancements (`RV-001`, `RV-002`) and the pre-existing `src/api` diagnostic item are routed cleanly as distinct follow-up candidates.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | None |
| Decision gap or invalid assumption | none | None |
| Material evidence gap | none | None |
| Non-blocking residual work | `follow-up` | Ranked post-Review follow-up choices (`RV-001`, `F-002`, `RV-002` + `src/api` diagnostic) |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Focused tier complete and passing across `src/core` (`17` #104 invariant tests + full suite, `ruff`, `mypy` on `348` files), `src/api` (`29` `test_content_standard.py` tests), and `src/agents` (`27` #104 invariant tests / `533` total tests, `ruff`, `mypy` on `66` files); `tools/rpi-checks.py` skipped per caller constraint.
* Blockers: None

