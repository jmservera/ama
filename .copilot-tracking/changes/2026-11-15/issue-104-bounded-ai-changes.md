<!-- markdownlint-disable-file -->
# RPI Changes: Issue #104 Cross-Capability Bounded AI Enforcement and Verification

## Metadata

* Task ID: issue-104-bounded-ai-invariants
* Related plan: .copilot-tracking/plans/2026-11-15/issue-104-bounded-ai-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-104-bounded-ai-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`, `P02`, `P03`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`, `P01-T03`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`, `P03-T02`
* All remaining active-plan markers: none
* Status basis: Every planned phase and task (`P01`–`P03`) is implemented, verified under the Focused validation tier (`unittest`, `ruff`, `mypy` across `src/core` and `src/agents`), and reconciled against the approved plan and phase details.

## Execution Summary

Delivered the cross-capability bounded-AI runtime enforcement contract (`zava_forward.core.bounded_ai`), closed five runtime edge-path bypasses across `src/core` and `src/agents`, and added exhaustive 13-capability acceptance verification suites in both `src/core/tests/test_epic104_bounded_ai_invariants.py` (16 test methods across `Store` and `SqlStore`) and `src/agents/tests/test_epic104_bounded_ai_invariants.py` (27 total test methods, +5 added). Focused validation passed cleanly across both packages without running `tools/rpi-checks.py`.

## Completed Work

### P01: Core Bounded-AI Enforcement and Cross-Capability Contract (`P01-T01`, `P01-T02`, `P01-T03`)

* `src/core/src/zava_forward/core/ai_registry.py` (`P01-T01`):
  * Added `is_dispatch_enabled(task_id, env=None)` so registered-but-disabled capabilities (`enabled is False` or `state == "disabled"`) fail closed unless explicitly demo-authorized (`chat-case-conversation` under `ZF_CHAT_DEMO_ACTIVATION=approved-2026-11-03` and `ZF_DEPLOYMENT_PROFILE=demo`) or live-authorized (`authorizes_live`).
  * Added `consumption_capability(task_id)` normalizing underscore registry IDs (`funding_draft` -> `funding-draft`, `read_document` -> `read-document`) to canonical hyphenated ledger capability IDs.
  * Tightened `authorizes_live(task_id, env=None)` with `rai_release.named_human` on `accountable_individual` and `authority.holder` and `rai_release.named` on `delegation`.
* `src/core/src/zava_forward/core/ai.py` (`P01-T01`):
  * Guarded `Ai.run` with `if not ai_registry.is_dispatch_enabled(task): return self._done(task, fallback, "template")` when `self.gate` is absent, and bound `ai_registry.consumption_capability(task)` into `CallContext`.
  * Guarded `Ai.look_at` at function entry (immediately after `export_fields.scalars(...)`, before `ai_prompts.render` and `self.configured`) with `if not (ai_registry.is_registered("read_document") and ai_registry.is_dispatch_enabled("read_document")): return dict(...)`, and bound `ai_registry.consumption_capability("read_document")` into `CallContext`.
* `src/core/src/zava_forward/core/ai_consumption.py` (`P01-T02`):
  * Rejected blank/whitespace `authority`, `owner`, and `evidence` in `Consumption.authorize`.
  * Updated `Consumption._require_bounds` to enforce `rai_release.named_human` on `owner` and `alert_owner` and `rai_release.named` on `alert` whenever non-synthetic prices apply or alert metadata is supplied, while omitting `"alert"` when `alert is None` on synthetic exercise fixtures.
  * Updated `Consumption.price(..., synthetic=False)` to validate pre-existing referencing authorities before appending a non-synthetic price, closing the pre-registered alertless authority swap bypass.
  * Added public `Consumption.non_exercise_status(capability, *, configuration=None, model=None, now=None)` read-only status inspection helper.
* `src/core/src/zava_forward/core/bounded_ai.py` (`P01-T03`):
  * Created strictly typed canonical cross-capability contract covering all 13 registered capabilities (`ASSISTANT_CAPABILITIES`, `RETAINED_CAPABILITIES`, `SPECIALIST_CAPABILITIES`, `EXPECTED_CAPABILITIES`):
    * `capability_inventory()` verifying exact registry parity.
    * `snapshot_controlled_records(store, *, aftercare=None)` and `assert_controlled_records_unchanged(before, after, *, allowed_proposal_slots=())` partitioning strictly invariant controlled state (`Store` case fields, deterministic `ranking`, aftercare `concerns`/`closures`) from proposal-only workspace slots (`funding_draft`, `read_document`).
    * `enforce_proposal_only(capability, payload)` rejecting `approved is not False`, non-proposal statuses, forbidden mutation/approval/execution/ranking keys, and forbidden action claims.
    * `verify_non_exercise_enablement(...)` and `audit_registered_capabilities(...)` verifying fail-closed non-exercise enablement unless registry, live `rai_release`, and finite human-approved `Consumption` call/token/money limits all pass.

### P02: Agents Capability Attribution and Named-Human Authorization Hardening (`P02-T01`, `P02-T02`)

* `src/agents/src/zava_forward/agents/chat.py` (`P02-T01`):
  * Updated `ChatModel.__call__` to bind a `CallContext` with `capability=CHAT_TASK` (`"chat-case-conversation"`) when `ai_consumption.CURRENT.get()` is `None`, preventing fallback to `"evidence"` while preserving outer `ChatPanel` `CallContext` instances when present.
* `src/agents/src/zava_forward/agents/chat_eval.py` and `src/agents/src/zava_forward/agents/heldout_batch.py` (`P02-T02`):
  * Enforced `rai_release.named_human` on `authorised_by` in `chat_eval.call_authorization` and on non-empty `approved_by` in `heldout_batch.authorization_problems` (preserving `"approved_by missing"` for missing/blank inputs).

### P03: Cross-Capability Acceptance Verification Suites and Focused Validation (`P03-T01`, `P03-T02`)

* `src/core/tests/test_epic104_bounded_ai_invariants.py` (`P03-T01`):
  * Added 16 strictly typed test methods exercising `bounded_ai`, `ai_registry`, `Ai.run`/`Ai.look_at`, `Consumption`, `rai_release`, `Store`, `SqlStore`, `Assistants`, `ChatPanel`, and `AftercareRegister` across all 13 registered capabilities for both Issue #104 invariants.
* `src/agents/tests/test_epic104_bounded_ai_invariants.py` (`P03-T02`):
  * Added 5 focused regression and cross-capability contract test methods (within the `<= 12` ceiling, 27 total tests in file) covering `bounded_ai.audit_registered_capabilities`, `AgentWorker` + `Store` + `AftercareRegister` controlled-record immutability, direct `ChatModel` `CHAT_TASK` `CallContext` binding, non-human `Consumption` owner and price-swap rejection, and `heldout_batch`/`chat_eval` non-human approver rejection.

## Implementation-Time Plan and Detail Updates

* Local judgment recorded during `P03`:
  * Aligned `bounded_ai.capability_inventory()` legacy task-ID extraction with `ai_registry.LEGACY` (`dict[str, dict[str, Any]]`) and aligned `bounded_ai.audit_registered_capabilities()` registry metadata checks with `ai_registry.REQUIRED_FIELDS` (`prohibited_uses` and `limits` string sequences via `rai_release.strings`). No scope, requirement, or acceptance-criteria change required.
  * Installed existing `src/core[iothub]` optional dependency in local gitignored `.venv` (`pip install -e ".[iothub]"`) so `test_device_registry_azure.py` executes cleanly during full `src/core` test discovery without changing any manifest.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `ruff check .` | `src/core` | Passed | `All checks passed!` (exit 0) |
| `ruff format --check .` | `src/core` | Passed | `291 files already formatted` (exit 0) |
| `mypy --python-executable ../../.venv/bin/python` | `src/core` | Passed | `Success: no issues found in 344 source files` (exit 0) |
| `unittest discover -s tests -p 'test_epic104_bounded_ai_invariants.py'` | `src/core` | Passed | `Ran 16 tests in 7.837s OK` (exit 0) |
| `unittest discover -s tests -q` + `test_device_registry_azure.py` | `src/core` | Passed | 3,580 discovered tests (`test_device_registry_azure.py`: `Ran 39 tests in 0.726s OK` after installing `.[iothub]` in `.venv`; zero failures across all 3,580 tests) |
| `ruff check .` | `src/agents` | Passed | `All checks passed!` (exit 0) |
| `ruff format --check .` | `src/agents` | Passed | `62 files already formatted` (exit 0) |
| `mypy --python-executable ../../.venv/bin/python` | `src/agents` | Passed | `Success: no issues found in 66 source files` (exit 0) |
| `PYTHONPATH=tests:../core/tests unittest discover -s tests -q` | `src/agents` | Passed | `Ran 533 tests in 344.872s OK` (`test_epic104_bounded_ai_invariants.py`: `Ran 27 tests in 14.946s OK`, exit 0) |
| `tools/rpi-checks.py` | Repository | Skipped | Explicitly excluded by caller direction (`Focused` validation tier) |

## Pre-Review Reconciliation

* Plan markers and phase details: Synchronized (`P01`, `P01-T01`–`P01-T03`, `P02`, `P02-T01`–`P02-T02`, `P03`, `P03-T01`–`P03-T02` all `[x]`).
* Completed-work evidence and handoff prose: Synchronized across plan, phase details, changes log, and durable RPI state JSON.
* Validation, blockers, remaining work, and follow-up items: Reconciled; Focused validation green across `src/core` and `src/agents`, zero blockers, zero remaining active-plan items.
* Review readiness: Ready for `rpi-review`.

## Blockers

* None

## Remaining Work

* None in declared plan scope (`P01`–`P03` complete).

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/issue-104-bounded-ai-plan.md, `## Follow-Up Items`
* Optional future `src/api` startup diagnostic exposing `bounded_ai.audit_registered_capabilities()` on an operator health/readiness surface: outside immediate `src/core` + `src/agents` scope; tracked for a later #104 API slice.

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: Full plan (`P01`–`P03`); completed: `P01`, `P01-T01`, `P01-T02`, `P01-T03`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`, `P03-T02`; remaining: none
* Validation coverage: Focused tier passed (`src/core`: 3,580 tests, `ruff`, `mypy` across 344 files; `src/agents`: 533 tests, `ruff`, `mypy` across 66 files; `tools/rpi-checks.py` skipped per caller constraint)
* Blockers: None
* Current plan and detail updates: Local alignment details recorded in `## Implementation-Time Plan and Detail Updates`; no scope/requirement divergence
* Planning and critique state: Ready (`PC-001`–`PC-005` resolved and verified in implementation)
* Follow-up items: Optional future `src/api` startup diagnostic
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: Confirmed automatic RPI Agent parent (proceeding immediately to `rpi-review`)
