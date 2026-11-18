<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #104 Cross-Capability Bounded AI Enforcement and Verification

## Metadata

* Task ID: issue-104-bounded-ai-invariants
* Task slug: issue-104-bounded-ai
* Related plan: .copilot-tracking/plans/2026-11-15/issue-104-bounded-ai-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/issue-104-bounded-ai-research.md (`C1`–`C20`), `src/README.md`

## Phase Index

| Phase ID | Name | Status | Detail sections |
|----------|------|--------|-----------------|
| P01 | Core Bounded-AI Enforcement and Cross-Capability Contract | ready | P01, P01-T01, P01-T02, P01-T03 |
| P02 | Agents Capability Attribution and Named-Human Authorization Hardening | ready | P02, P02-T01, P02-T02 |
| P03 | Cross-Capability Acceptance Verification Suites and Focused Validation | ready | P03, P03-T01, P03-T02 |

<!-- rpi:phase id=P01 -->
## P01: Core Bounded-AI Enforcement and Cross-Capability Contract

### Context

`zava_forward.core.ai_registry.tasks()` defines the 13 canonical AI capabilities (`5` assistants in `assistants.REGISTRY`, `6` retained tasks in `ai_registry.LEGACY`, `chat-case-conversation`, and `aftercare-concern-pack`) (`C1`). Research Cycle 1 (`C2`, `C5`, `C6`, `C9`, `C10`, `C19`) identified three core hardening needs: (1) `Ai.run` and `Ai.look_at` do not verify whether a registered task is actually enabled for dispatch (`enabled=False` on `aftercare-concern-pack` and `chat-case-conversation` unless `demo_activation_honoured` holds); (2) `Consumption` accepts non-human/placeholder owner strings in `_require_bounds`, allows blank `owner`/`evidence` strings on synthetic/pre-price authorities, and allows `authorize` before `price(..., synthetic=False)` without raising `ValueError` at write time; and (3) `src/core` lacks a canonical `bounded_ai` module codifying both Issue #104 invariants across all 13 capabilities.

### Intent

Enforce fail-closed capability dispatch and non-exercise human-owned financial bounds inside `zava_forward.core`, and expose `zava_forward.core.bounded_ai` as the reusable, strictly typed cross-capability invariant enforcement and audit module.

### Boundaries

* Included: `src/core/src/zava_forward/core/ai_registry.py`, `src/core/src/zava_forward/core/ai.py`, `src/core/src/zava_forward/core/ai_consumption.py`, and new canonical module `src/core/src/zava_forward/core/bounded_ai.py`.
* Excluded: Generated targets (`none`), `src/core/pyproject.toml` edits, `src/api` routes, and live Azure OpenAI credentials or OD-51 pricing assignments.

### Likely Targets

* `src/core/src/zava_forward/core/ai_registry.py`: Add `is_dispatch_enabled(task_id, env=None)` and `consumption_capability(task_id)`.
* `src/core/src/zava_forward/core/ai.py`: Guard `Ai.run` with `ai_registry.is_dispatch_enabled(task)` and `Ai.look_at` with `ai_registry.is_registered("read_document")` + `ai_registry.is_dispatch_enabled("read_document")`, using `ai_registry.consumption_capability` for `CallContext`.
* `src/core/src/zava_forward/core/ai_consumption.py`: Enforce `rai_release.named_human` / `rai_release.named`, reject blank `authority`/`owner`/`evidence`, and validate referencing authorities when registering a `synthetic=False` price.
* `src/core/src/zava_forward/core/bounded_ai.py`: New strictly typed cross-capability enforcement, controlled-record snapshot/immutability, non-exercise enablement gate, and registry-wide audit module.

### Dependencies

* None.

### Validation Expectations

* `ruff check .`, `ruff format --check .`, `mypy`, and existing unit tests (`test_ai_register_completeness.py`, `test_ai_consumption.py`, `test_dependency_rule.py`) pass in `src/core`.

### Completion Evidence

* `bounded_ai.audit_registered_capabilities()` reports `ok=True` across all 13 capabilities, disabled capabilities fail closed in `Ai.run`/`Ai.look_at` without provider calls, and `Consumption` rejects non-human owners and out-of-order unbounded billable pricing.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Enforce capability dispatch-enabled state in `ai_registry` and `Ai`

#### Context

`ai_registry.is_registered(task_id)` verifies required register metadata (`C2`), so `is_registered("aftercare-concern-pack")` and `is_registered("chat-case-conversation")` both return `True` even though both entries carry `enabled=False, state="disabled"`. In `Ai.run` (`C5`), when `self.gate` is `None`, passing `"aftercare-concern-pack"` or `"chat-case-conversation"` proceeds directly to `self._chat(...)`. In `Ai.look_at` (`C6`), neither `is_registered("read_document")` nor enabled state is checked before `self._chat(...)`.

#### Intent

Add canonical dispatch-enabled and consumption-capability helpers in `ai_registry` and enforce them before any provider call in `Ai.run` and `Ai.look_at`.

#### Boundaries

* Included: `is_dispatch_enabled(task_id, env=None)` and `consumption_capability(task_id)` in `ai_registry.py`; pre-dispatch checks in `Ai.run` and `Ai.look_at` in `ai.py`. Keep formatting compatible with legacy `ai_registry.py` and `ai.py` (`ruff check` clean without reformatting excluded files).
* Excluded: Changing `is_registered(task_id)` semantics (registration completeness remains distinct from enabled state).

#### Likely Targets

* `src/core/src/zava_forward/core/ai_registry.py`: Define `is_dispatch_enabled(task_id, env=None)` (`True` iff `is_registered(task_id)` and `(entry.get("enabled") is not False or demo_activation_honoured(task_id, env))`), update `authorizes_live(task_id, env=None)` (outside `demo_activation_honoured`) to require `rai_release.named_human` on `accountable_individual` and all `authority.values()` plus `rai_release.named` on `delegation`, and define `consumption_capability(task_id)` (`require_registered(task_id); return task_id.replace("_", "-")`).
* `src/core/src/zava_forward/core/ai.py`: In `Ai.run`, immediately after `is_registered(task)`, check `if not ai_registry.is_dispatch_enabled(task): return out(text=template, source="template", model=None, validated=True, enabled=False, reason="AI feature is disabled; use the manual route")`, and pass `ai_registry.consumption_capability(task)` into `CallContext`. In `Ai.look_at`, immediately after `export_fields.scalars(...)` (before `ai_prompts.render`, `self.gate`, and `off or not self.configured`), check `is_registered("read_document")` and `is_dispatch_enabled("read_document")`, returning the fail-closed `"template"` envelope when false, and pass `ai_registry.consumption_capability("read_document")` into `CallContext`.

#### Dependencies

* None.

#### Validation Expectations

* Semantic checks: `Ai.run("aftercare-concern-pack", ...)` and `Ai.run("chat-case-conversation", ...)` (without demo env switch) return `source="template", model=None, enabled=False` with zero transport/provider calls; with demo env switch, `is_dispatch_enabled("chat-case-conversation", env)` is `True`; `Ai.look_at` fails closed to `source="template"` if `"read_document"` is disabled/unregistered.
* Regression checks: Existing `Ai.run` and `Ai.look_at` callers for the 6 retained tasks and 5 assistants continue unchanged.

#### Completion Evidence

* Updated `ai_registry.py` and `ai.py` pass `ruff check` and unit tests in `src/core`.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Harden `Consumption` non-exercise owner and price-ordering bounds

#### Context

In `src/core/src/zava_forward/core/ai_consumption.py` (`C9`), `Consumption._require_bounds` checks only `isinstance(v, str) and v.strip()`, permitting non-human tokens (`"system"`, `"agent"`, `"copilot"`, `"bot"`, `"automation"`) and placeholders (`"unknown"`, `"unavailable"`, `"none"`, `"unapproved"`) rejected by `rai_release.named_human` (`C10`). Note that `alert` is an alert rule/channel identifier (e.g., `"alert-rule-ai-limits"`), so `alert` must use `rai_release.named(alert)` while `owner` and `alert_owner` use `rai_release.named_human(...)`. Furthermore, calling `authorize(...)` before `price(..., synthetic=False)` skips `_require_bounds` when `alert=None`, and `price(..., synthetic=False)` currently records the billable price without verifying existing referencing `authority` records.

#### Intent

Enforce named-human owner/alert-owner approval and order-independent write-time rejection of unbounded or alertless non-exercise authorities in `Consumption` while preserving exact ledger schema compatibility for synthetic exercise authorities.

#### Boundaries

* Included: `Consumption.price`, `Consumption.authorize`, and `Consumption._require_bounds` in `src/core/src/zava_forward/core/ai_consumption.py`.
* Excluded: Changing ledger event schema keys (do not add extra fields to `authority` records, preserving idempotency equality checks and `assertNotIn("alert", record)` on synthetic exercise authorities when `alert=None`).

#### Likely Targets

* `src/core/src/zava_forward/core/ai_consumption.py`:
  * Import `rai_release` from `.` and require `isinstance(v, str) and v.strip()` for `authority`, `owner`, and `evidence` on all `authorize(...)` calls.
  * Update `_require_bounds(owner, budgets, alert, alert_owner)` to require `rai_release.named_human(owner)`, `rai_release.named(alert)`, and `rai_release.named_human(alert_owner)` (raising `ValueError("Beyond the exercise a named human approving owner and a human-owned alert are required.")`) plus positive `calls`, `tokens`, and `amount` across all `budgets`.
  * In `authorize(...)`: invoke `_require_bounds` and persist `alert` + `alert_owner` whenever `(known is not None and not known["synthetic"]) or alert is not None or alert_owner is not None`.
  * In `price(..., synthetic=False)`: before writing the price event, verify every existing `authority` record with `r["price"] == pid` has `r.get("alert")`, `r.get("alert_owner")`, and positive `calls`, `tokens`, and `amount` on every budget, raising `ValueError` otherwise.
  * Expose public read-only `non_exercise_status(capability: str, *, configuration: str | None = None, model: str | None = None, now: float | None = None) -> dict[str, Any]` inspecting unexpired authority, unexpired `synthetic is False` price (`retrieved <= now` and matching `model` when given), `alert`, `alert_owner`, `max_calls >= 1`, `max_depth >= 1`, positive `calls`/`tokens`/`amount` on every budget, and `_currency_hold(...) is None`.

#### Dependencies

* None.

#### Validation Expectations

* Semantic checks: `authorize` with `owner="system"`, `owner="unknown"`, `alert_owner="copilot"`, or `alert="unknown"` raises `ValueError` on billable prices; `authorize` with `calls=0` or `alert=None` followed by `price(..., synthetic=False)` raises `ValueError` and writes no billable price; blank `owner=" "` or `evidence=""` raises `ValueError` even on synthetic prices.
* Regression checks: `src/core/tests/test_ai_consumption.py` passes unmodified, and synthetic exercise authorities with `alert=None, alert_owner=None` still omit `"alert"` from ledger records.

#### Completion Evidence

* `ai_consumption.py` passes `ruff check`, `ruff format --check`, `mypy`, and `test_ai_consumption.py`.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T03 -->
### P01-T03: Create `zava_forward.core.bounded_ai` cross-capability enforcement and audit module

#### Context

Neither `src/core` nor `src/agents` currently has a single programmatic contract that enumerates all 13 registered capabilities, computes deterministic controlled-record digests to prove zero mutation/approval/execution/ranking changes across capability invocations, and evaluates end-to-end non-exercise enablement readiness across `ai_registry`, `rai_release`, and `Consumption` (`C1`–`C10`, `C15`–`C20`). Because `src/core/pyproject.toml` enforces `mypy --strict` and `ruff` on new modules (`C19`), `bounded_ai.py` must be 100% strictly typed using clean `Any` aliases at untyped legacy module boundaries (`ai_registry`, `ai`, `assistants`, `ranking`).

#### Intent

Deliver `src/core/src/zava_forward/core/bounded_ai.py` as the canonical cross-capability enforcement and verification module imported by both `src/core` and `src/agents`.

#### Boundaries

* Included:
  * `EXPECTED_CAPABILITIES`: canonical `frozenset[str]` of the 13 registered capabilities (`5` assistants, `6` retained tasks, `chat-case-conversation`, `aftercare-concern-pack`) and `capability_inventory()` verifying exact bijection with `ai_registry.tasks()`, `assistants.REGISTRY`, `ai_registry.LEGACY`, `CHAT_TASK`, and `CONCERN_PACK_TASK`.
  * Controlled-record protection helpers: `CONTROLLED_CASE_FIELDS` (`stage`, `closed`, `resident`, `hazards`, `signoffs`, `grants`, `procurement`, `finance`, `quality`, `appointments`, `service_requests`, `handoff`, `technical`, `measures`, `survey`, `home`), `snapshot_controlled_records(store, aftercare=None)` capturing partitioned digests/metadata separating (1) strictly invariant controlled records (`CONTROLLED_CASE_FIELDS`, `funding_ok`, controlled funding fields `route`/`reference`/`approved_by`/`history`, non-summary document fields, deterministic `ranking.canonical(store._ranking())`, and optional `AftercareRegister` `concerns`/`closures`), (2) the unapproved `funding` draft/status workspace slot (`draft` + `status`), and (3) unapproved document `summary`/necessity-note slots, so `assert_controlled_records_unchanged(before, after, *, capability=None)` enforces equality across all 3 partitions by default and relaxes only partition (2) (requiring `status in ("Not started", "To prepare", "Draft ready")` and `approved_by is None`) when `capability == "funding_draft"` and only partition (3) when `capability == "read_document"`.
  * Proposal-only output guard: `enforce_proposal_only(task_id, payload)` raising `BoundedAiViolation` if `task_id` is unregistered, `payload` marks `approved=True` or `approval not in (None, "Not reviewed", "pending", "pending_owner_review")`, `payload` injects controlled mutation keys (`stage_transition`, `approved_by`, `executed`, `rank_override`, `consent_granted`, `payment_released`), or text fields match `ai.FORBIDDEN`.
  * Non-exercise enablement gate: `verify_non_exercise_enablement(task_id, *, env=None, task_entry=None, release_record=None, binding=None, bound_keys=(), now=None, ledger=None, configuration=None, model=None)` (accepting optional `task_entry` for controlled test harnesses while defaulting to `ai_registry.get(task_id)`) returning `dict(allowed=bool, capability=str, consumption_capability=str, reasons=list[str])` that fails closed unless (1) `task_id` is registered, enabled, and carries `rai_release.named_human` `accountable_individual` and `authority` holders (`demo_activation_honoured` is explicitly rejected for non-exercise enablement with reason `"demo-activation-is-exercise-only"`), (2) `rai_release.missing_contract`, `rai_release.named_human(release_record.get("accountable_owner"))`, and `rai_release.missing_binding(..., live=True)` pass with `evidence_class == "actual"`, `named_human` approver, and `valid_consumption`, and (3) `ledger.non_exercise_status(...)` confirms an unexpired `synthetic is False` price and unexpired authority for `consumption_capability(task_id)` with `alert`, `alert_owner`, `max_calls >= 1`, `max_depth >= 1`, positive `calls`/`tokens`/`amount` on every budget, and compatible currency.
  * Registry-wide audit: `audit_registered_capabilities(env=None)` inspecting all registered capabilities and returning `dict(ok=bool, count=int, capabilities=dict[str, dict[str, Any]], violations=list[str])`.
* Excluded: Workload imports (`zava_forward.agents`, `zava_forward.api`, etc.).

#### Likely Targets

* `src/core/src/zava_forward/core/bounded_ai.py`: Create complete, strictly typed module.

#### Dependencies

* P01-T01, P01-T02.

#### Validation Expectations

* `mypy`, `ruff check .`, and `ruff format --check .` pass in `src/core` with zero errors.

#### Completion Evidence

* `bounded_ai.py` exists, exports the documented functions/types, and passes strict static analysis and unit tests.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Agents Capability Attribution and Named-Human Authorization Hardening

### Context

`zava_forward.agents` implements the isolated assistant worker (`dispatch.py`, `runtime.py`), employee chat model adapter (`chat.py`), chat evaluation harness (`chat_eval.py`), and held-out actual-model evaluation batch runner (`heldout_batch.py`) (`C11`–`C14`). Research Wave 3 found that direct `ChatModel.__call__` calls drop `chat-case-conversation` consumption attribution when `ChatPanel` has not already set `ai_consumption.CURRENT` (`C13`), and that `chat_eval.call_authorization` and `heldout_batch.authorization_problems` accept non-human or placeholder owner strings (`"system"`, `"copilot"`, `"unknown"`, `"unapproved"`) (`C11`, `C12`).

### Intent

Ensure every `zava_forward.agents` model and actual-evaluation entrypoint attributes consumption to its registered capability and requires a named human owner (`rai_release.named_human`) for non-exercise/actual-model limits.

### Boundaries

* Included: `src/agents/src/zava_forward/agents/chat.py`, `src/agents/src/zava_forward/agents/chat_eval.py`, `src/agents/src/zava_forward/agents/heldout_batch.py`.
* Excluded: SQL/blob dependencies (forbidden in `agents` by ADR 0001 / ADR 0006 `C18`).

### Likely Targets

* `src/agents/src/zava_forward/agents/chat.py`: Bind `CallContext` with `CHAT_TASK` when `ai_consumption.CURRENT.get() is None`.
* `src/agents/src/zava_forward/agents/chat_eval.py`: Validate `authorised_by` with `rai_release.named_human`.
* `src/agents/src/zava_forward/agents/heldout_batch.py`: Validate `approved_by` with `rai_release.named_human`.

### Dependencies

* P01.

### Validation Expectations

* `ruff check .`, `ruff format --check .`, `mypy`, and existing `src/agents` unit tests (`test_chat_model.py`, `test_chat_eval.py`, `test_heldout_batch.py`, `test_dependency_rule.py`) pass cleanly.

### Completion Evidence

* Direct `ChatModel` calls bind `chat-case-conversation` in `Consumption`, and `chat_eval` / `heldout_batch` refuse non-human or placeholder owner strings.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Bind `CHAT_TASK` consumption context in `ChatModel.__call__`

#### Context

When `ChatPanel._ask` calls `ChatModel`, `ChatPanel` wraps the call in `call_context(CallContext(..., CHAT_TASK, ...))` (`C7`). When `ChatModel.__call__` (`src/agents/src/zava_forward/agents/chat.py`) is invoked directly, `ai_consumption.CURRENT.get()` is `None`, causing `Ai._request` (`C5`) to synthesize a fallback `CallContext` with `capability="evidence"`, bypassing `chat-case-conversation` live checks and budget attribution (`C13`).

#### Intent

Guarantee `ChatModel.__call__` always executes `self.worker.provider_call(...)` inside a `chat-case-conversation` `CallContext` whenever no outer `CallContext` is active.

#### Boundaries

* Included: `ChatModel.__call__` in `src/agents/src/zava_forward/agents/chat.py`.
* Excluded: Overwriting an already-active outer `CallContext` from `ChatPanel` (preserve `ChatPanel`'s correlation/root hashes when `CURRENT.get() is not None`).

#### Likely Targets

* `src/agents/src/zava_forward/agents/chat.py`: Import ` uuid` and `CHAT_TASK` (`zava_forward.core.ai_registry`) and `CallContext`, `CURRENT`, `call_context`, `reference` (`zava_forward.core.ai_consumption`); when `CURRENT.get() is None`, create `root = reference(uuid.uuid4().hex)` and wrap `self.worker.provider_call(...)` in `call_context(CallContext(root, root, CHAT_TASK, "retrofit-case", reference(CHAT_TASK), reference(system)))`.

#### Dependencies

* P01-T01.

#### Validation Expectations

* Semantic checks: Direct `ChatModel(AgentWorker(foundry_provider(ai)), admission=...)("sys", "prompt")` reserves against capability `"chat-case-conversation"` in `ai.consumption` and fails closed with `"price-unknown"` if `ai.is_live("chat-case-conversation")` is `True` on a synthetic price; outer `ChatPanel` `CallContext` remains untouched when already set.
* Regression checks: `src/agents/tests/test_chat_model.py` passes unmodified.

#### Completion Evidence

* `chat.py` passes `mypy`, `ruff check`, `ruff format --check`, and unit tests.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Enforce `rai_release.named_human` in `chat_eval` and `heldout_batch`

#### Context

`chat_eval.call_authorization` (`C11`) checks `if not isinstance(owner, str) or not owner.strip(): reasons.append("no named owner authorisation")`, and `heldout_batch.authorization_problems` (`C12`) checks `TEXT_FIELDS` (`approved_by`, `authority_ref`, `model`) only for non-empty strings. Both accept `"system"`, `"agent"`, `"copilot"`, `"bot"`, `"automation"`, `"unknown"`, `"unavailable"`, `"none"`, and `"unapproved"`.

#### Intent

Require `rai_release.named_human` for `authorised_by` in `chat_eval.call_authorization` and `approved_by` in `heldout_batch.authorization_problems`.

#### Boundaries

* Included: `src/agents/src/zava_forward/agents/chat_eval.py` and `src/agents/src/zava_forward/agents/heldout_batch.py`.
* Excluded: Changing the missing-field message `"approved_by missing"` when `approved_by` is absent or whitespace in `heldout_batch.authorization_problems` (keep `"approved_by missing"` for missing/blank, and append `"approved_by must name a human owner"` when non-blank but `not rai_release.named_human(approved_by)`).

#### Likely Targets

* `src/agents/src/zava_forward/agents/chat_eval.py`: Import `rai_release` from `zava_forward.core`; check `if not rai_release.named_human(owner): reasons.append("no named owner authorisation")`.
* `src/agents/src/zava_forward/agents/heldout_batch.py`: Import `rai_release` from `zava_forward.core`; after `TEXT_FIELDS` presence check, if `isinstance(auth.get("approved_by"), str) and auth["approved_by"].strip() and not rai_release.named_human(auth["approved_by"])`, append `"approved_by must name a human owner"`.

#### Dependencies

* None.

#### Validation Expectations

* Semantic checks: `call_authorization` and `authorization_problems` reject `"system"`, `"agent"`, `"copilot"`, `"bot"`, `"automation"`, `"unknown"`, and `"unapproved"` while continuing to accept named human/fixture strings (`"owner"`, `"constructed-fixture"`, `"Claire Whittaker"`).
* Regression checks: `test_chat_eval.py` and `test_heldout_batch.py` pass unmodified.

#### Completion Evidence

* `chat_eval.py` and `heldout_batch.py` pass `mypy`, `ruff check`, `ruff format --check`, and unit tests.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Cross-Capability Acceptance Verification Suites and Focused Validation

### Context

`src/core/tests` currently lacks an Epic #104 cross-capability invariant suite (`C19`), and `src/agents/tests/test_epic104_bounded_ai_invariants.py` covers subset scenarios rather than testing all 13 registered capabilities end to end across controlled-record immutability and non-exercise limit gates (`C20`). Test ownership is locked as follows:

* Exact test removals: `none`.
* Canonical targets: `src/core/tests/test_epic104_bounded_ai_invariants.py` (new, <= 20 test methods, parameterized across all 13 registered capabilities via `subTest`) and `src/agents/tests/test_epic104_bounded_ai_invariants.py` (extended with <= 12 focused test methods).
* Generated targets: `none`.
* Semantic vs regression coverage: Semantic assertions verify actual runtime state digests, ledger holds, provider transport call counts (`0` on refused/disabled/unbounded paths), and human-owner rejection rather than checking constants alone; full `src/core` and `src/agents` suites serve as regression verification.

### Intent

Deliver comprehensive, fast, deterministic cross-capability acceptance verification suites in both `src/core` and `src/agents`, run Focused validation (`unittest`, `ruff check`, `ruff format --check`, `mypy`), and record clean implementation evidence for `rpi-review`.

### Boundaries

* Included: `src/core/tests/test_epic104_bounded_ai_invariants.py`, `src/agents/tests/test_epic104_bounded_ai_invariants.py`, local editable `.venv` verification in `src/core` and `src/agents` (ensuring `.venv` is gitignored and never committed), and `.copilot-tracking/changes/2026-11-15/issue-104-bounded-ai-changes.md`.
* Excluded: Running `tools/rpi-checks.py`, touching `src/api/tests`, or pushing to remote.

### Likely Targets

* `src/core/tests/test_epic104_bounded_ai_invariants.py`: New comprehensive core cross-capability invariant test suite.
* `src/agents/tests/test_epic104_bounded_ai_invariants.py`: Expanded cross-capability agents + core boundary verification suite.
* `.copilot-tracking/changes/2026-11-15/issue-104-bounded-ai-changes.md`: Implementation changes artifact.

### Dependencies

* P01, P02.

### Validation Expectations

* In an isolated virtual environment with `-e src/core` and `-e "src/agents[dev]"` (plus `core[dev]` tools):
  * From `src/core`: `python -m unittest discover -s tests -q`, `ruff check .`, `ruff format --check .`, `mypy` all exit 0.
  * From `src/agents`: `python -m unittest discover -s tests -q`, `ruff check .`, `ruff format --check .`, `mypy` all exit 0.

### Completion Evidence

* Exact command outputs and test counts recorded in `.copilot-tracking/changes/2026-11-15/issue-104-bounded-ai-changes.md`, all plan and phase-details task checkboxes reconciled, ready for `rpi-review`.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Add `src/core/tests/test_epic104_bounded_ai_invariants.py`

#### Context

`src/core` owns `ai_registry`, `Ai`, `Store`, `Assistants`, `ChatPanel`, `AftercareRegister`, `rai_release`, `Consumption`, and the new `bounded_ai` contract (`C1`–`C10`, `C15`–`C19`). Every new file under `src/core/tests/` is checked by `mypy --strict`, `ruff check`, and `ruff format --check` (`C19`).

#### Intent

Create `src/core/tests/test_epic104_bounded_ai_invariants.py` proving both Issue #104 invariants across all 13 registered capabilities in `zava_forward.core`.

#### Boundaries

* Included (<= 20 test methods, strictly typed using explicit `: Any` boundary aliases for untyped legacy `core` classes/modules `Store`, `SqlStore`, `Assistants`, `Ai`, `ai_registry`, and `ranking` so `mypy --strict` passes with `src/core/pyproject.toml` untouched):
  1. Registry & audit completeness: `bounded_ai.audit_registered_capabilities()` covers all 13 capabilities (`5` assistants, `6` retained tasks, `chat-case-conversation`, `aftercare-concern-pack`), every entry is `propose_only=True` and `non_exercise_enabled=False` by default, and demo chat activation remains `non_exercise_enabled=False` (`"demo-activation-is-exercise-only"`).
  2. Invariant 1 across all 6 retained tasks (`briefing`, `message`, `summary`, `priority`, `funding_draft`, `read_document`) on `Store`: invoking each capability with both valid proposal replies and hostile approval/execution/ranking/consent-forging model replies leaves `bounded_ai.snapshot_controlled_records(store)` unchanged (verifying `stage`, `closed`, `resident` consent/decisions, `hazards`, `signoffs`, `grants`, `funding_ok`, `procurement`, `finance`, `quality`, and deterministic `ranking.canonical(store._ranking())`), records `approved=False` envelopes, and continues to preserve controlled records across `review_ai` and `resolve_priority`.
  3. Invariant 1 across all 5 SQLite `Assistants` (`stock-prioritisation`, `assessment-preparation`, `funding-evidence`, `works-resident-coordination`, `quality-evidence`): full lifecycle `invoke -> claim -> issue_permit -> complete -> review("verify") -> review("accept")` on SQLite `SqlStore` leaves `bounded_ai.snapshot_controlled_records(sql_store)` byte-identical and quarantines hostile `FORBIDDEN` outputs.
  4. Invariant 1 across `chat-case-conversation` (`ChatPanel`) and `aftercare-concern-pack` (`AftercareRegister`) plus disabled-capability dispatch blocks: `ChatPanel.ask` / `ask_unstored` (refused prompts, withheld action/status/tool claims, and grounded answers) leave `snapshot_controlled_records(store)` unchanged; `AftercareRegister.propose_pack` / `review_pack` leave `concerns` and `closures` unchanged with `model_used=False`; `Ai.run` on `aftercare-concern-pack` and disabled `chat-case-conversation` returns `source="template", enabled=False` with zero transport calls.
  5. Invariant 2 across all 13 capabilities (`verify_non_exercise_enablement`, `Consumption`, `Ai._request`, `rai_release`): every capability fails closed beyond exercise mode when missing live registry authority, actual-class `rai_release` with `named_human` approver, non-synthetic price, owned alert, or finite positive `calls`, `tokens`, and `amount` budgets; rejects non-human/placeholder owners (`"system"`, `"agent"`, `"copilot"`, `"bot"`, `"automation"`, `"unknown"`, `"unapproved"`); rejects `authorize` before `price(..., synthetic=False)` when unbounded/alertless; and admits then deterministically holds on call, token, and money exhaustion when all non-exercise gates are satisfied in a controlled test harness.
* Excluded: Duplicate helper tests unrelated to Issue #104 invariants.

#### Likely Targets

* `src/core/tests/test_epic104_bounded_ai_invariants.py`: Create test suite.

#### Dependencies

* P01-T01, P01-T02, P01-T03.

#### Validation Expectations

* `python -m unittest tests/test_epic104_bounded_ai_invariants.py`, `ruff check .`, `ruff format --check .`, and `mypy` pass in `src/core`.

#### Completion Evidence

* All tests in `src/core/tests/test_epic104_bounded_ai_invariants.py` pass with strict typing and lint compliance.

#### Unresolved Items

* None.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Expand `src/agents/tests/test_epic104_bounded_ai_invariants.py` and run focused validation

#### Context

`src/agents/tests/test_epic104_bounded_ai_invariants.py` (`C20`) verifies `AgentWorker` isolation, `ai_priority` ranking immutability, `FORBIDDEN` claim patterns, and selected consumption/eval bounds, but does not yet verify: (1) cross-package 13-capability parity against `bounded_ai.audit_registered_capabilities()`, (2) direct `ChatModel.__call__` binding `"chat-case-conversation"` in `Consumption` and refusing synthetic prices when `chat-case-conversation` is marked live, (3) `TaskMessage.from_json` rejecting disabled/non-assistant tasks (`chat-case-conversation`, `aftercare-concern-pack`, `briefing`) from worker queue execution, and (4) `rai_release.named_human` rejection of non-human/placeholder owners (`"system"`, `"agent"`, `"copilot"`, `"bot"`, `"automation"`, `"unknown"`, `"unapproved"`) across `Consumption`, `chat_eval.call_authorization`, and `heldout_batch.authorization_problems` plus price-after-authority refusal.

#### Intent

Extend `src/agents/tests/test_epic104_bounded_ai_invariants.py` to cover all cross-package `agents` <-> `core` bounded-AI invariants and run complete Focused validation across `src/core` and `src/agents`.

#### Boundaries

* Included: Add `<= 12` focused test methods to `src/agents/tests/test_epic104_bounded_ai_invariants.py` (exact removals: `none`); run `unittest`, `ruff check`, `ruff format --check`, and `mypy` in both `src/core` and `src/agents` using a workspace-local gitignored `.venv` (confirming via `git status --short` that `.venv` is gitignored before committing).
* Excluded: Running `tools/rpi-checks.py` or writing outside the workspace root.

#### Likely Targets

* `src/agents/tests/test_epic104_bounded_ai_invariants.py`: Extend existing test classes / add cross-capability contract test class.

#### Dependencies

* P01, P02, P03-T01.

#### Validation Expectations

* Using a workspace-local gitignored `.venv` with editable `src/core[dev]` and `src/agents[dev]`:
  * `src/core`: `unittest discover -s tests`, `ruff check .`, `ruff format --check .`, `mypy` all pass.
  * `src/agents`: `unittest discover -s tests`, `ruff check .`, `ruff format --check .`, `mypy` all pass.

#### Completion Evidence

* Zero failures across unit tests, `ruff`, and `mypy` in both packages, and clean `git status` containing only intended `src/` and `.copilot-tracking/` files.

#### Unresolved Items

* None.
