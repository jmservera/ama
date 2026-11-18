<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #104 Cross-Capability Bounded AI Enforcement and Verification

## Metadata

* Task ID: issue-104-bounded-ai-invariants
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/issue-104-bounded-ai-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-104-bounded-ai-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Continuous automatic RPI run on branch `feat/demo-104-bounded-ai` (stacked child targeting `feat/demo-164-chat-grounding-provenance-0900`, PR #1641) delivering an explicit cross-capability enforcement and acceptance verification suite across `src/core` and `src/agents` for Issue #104's two engineering invariants: (1) AI never approves, executes, ranks, or mutates controlled records; and (2) no registered AI capability is enabled beyond the exercise without finite, owner-approved call, token, and budget limits. Validation uses the Focused tier (`src/core` and `src/agents` unit tests, `ruff check`, `ruff format --check`, and `mypy`, explicitly excluding `tools/rpi-checks.py`), followed by a local commit with `Refs #104` and the Copilot co-author trailer without pushing.
* Research and evidence considered: `.copilot-tracking/research/2026-11-15/issue-104-bounded-ai-research.md` (`C1`-`C20`), `.copilot-tracking/plans/2026-11-15/issue-104-bounded-ai-plan.md`, `.copilot-tracking/details/2026-11-15/issue-104-bounded-ai-phase-details.md`, `src/core/src/zava_forward/core/ai_registry.py`, `src/core/src/zava_forward/core/ai.py`, `src/core/src/zava_forward/core/ai_consumption.py`, `src/core/src/zava_forward/core/rai_release.py`, `src/core/pyproject.toml`, `src/agents/src/zava_forward/agents/chat.py`, `src/agents/src/zava_forward/agents/chat_eval.py`, `src/agents/src/zava_forward/agents/heldout_batch.py`, `src/agents/tests/test_epic104_bounded_ai_invariants.py`, `src/core/tests/test_ai_consumption.py`, and `src/api/tests/test_nonexercise_capability_bounds.py`.
* Decisions, dependencies, and acceptance criteria considered: Confirmed caller decisions (continuous automatic RPI loop, Focused validation tier without `tools/rpi-checks.py`, `Refs #104` local commit only, no push, no `pyproject.toml` edits, and preservation of open decision OD-51 fail-closed defaults), ADR 0006 package dependency direction (`agents` imports `core`; `core` imports stdlib/internal `core` only), functional requirements `FR-1`-`FR-4`, non-functional requirements `NFR-1`-`NFR-3`, and acceptance criteria `AC-1`-`AC-5`.
* Assessment boundary: This critique verifies every planned enforcement seam, helper contract, static-typing constraint, backward-compatibility claim, and test target directly against the supplied research (`C1`-`C20`) and the 11 referenced source, configuration, and test files. Unread sibling files in `src/core` and `src/agents` (`store.py`, `sqlstore.py`, `assistants.py`, `chat_panel.py`, `aftercare.py`, `dispatch.py`, `runtime.py`, `test_chat_eval.py`, `test_heldout_batch.py`) are assessed strictly through verified `C1`-`C20` evidence and their usages in `src/agents/tests/test_epic104_bounded_ai_invariants.py`.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| FR-1 (`ai_registry.py`, `ai.py` dispatch gating) | Partial | `P01-T01` adds `is_dispatch_enabled` and `consumption_capability`, but `Ai.look_at` guard placement and `consumption_capability` wiring in `ai.py` are underspecified (`PC-005`). |
| FR-2 (`Consumption`, `chat.py`, `chat_eval.py`, `heldout_batch.py`) | Covered | `P01-T02`, `P02-T01`, and `P02-T02` close blank-field, non-human owner, price-after-authority, and direct `ChatModel` `CHAT_TASK` attribution gaps while preserving synthetic `alert=None` ledger schema and existing fixture strings. |
| FR-3 (`zava_forward.core.bounded_ai` contract) | Partial | `P01-T03` covers all 13 capabilities, but `verify_non_exercise_enablement` lacks a controlled-harness registry seam, `named_human` checks on registry/contract owner fields, and a public `Consumption` read helper (`PC-001`), and `snapshot_controlled_records` needs partitioned workspace-slot digests (`PC-004`). |
| FR-4 (`core` and `agents` 13-capability suites) | Partial | `P03-T01` and `P03-T02` cover all 13 capabilities across both invariants, subject to the controlled-harness seam (`PC-001`), `mypy --strict` `Any` aliases in `P03-T01` (`PC-003`), and removing `/tmp` venv paths in `P03-T02` (`PC-002`). |
| NFR-1 (ADR 0006 dependency isolation) | Covered | `bounded_ai.py` lives in `zava_forward.core` with stdlib/internal `core` imports only; `P02-T01` imports only `ai_registry` and `ai_consumption` in `agents/chat.py`, matching the `allowed_core` AST guard in `src/agents/tests/test_epic104_bounded_ai_invariants.py:125`. |
| NFR-2 (`mypy`, `ruff check`, `ruff format --check` with untouched `pyproject.toml`) | Partial | `P01-T03` specifies `Any` boundaries for `bounded_ai.py`, but `P03-T01` omits `Any`-alias typing discipline for untyped legacy `core` classes (`Store`, `SqlStore`, `Assistants`, `Ai`, `ai_registry`, `ranking`) under `strict = true` (`PC-003`). |
| NFR-3 (Backward compatibility and test budget) | Covered | Zero test removals, 1 new test file (`<= 20` methods), `<= 12` added methods in `src/agents/tests/test_epic104_bounded_ai_invariants.py`, and existing owner fixture strings (`"owner"`, `"alert-owner"`, `"approving-owner-fixture"`, `"constructed-finance-owner"`) pass `rai_release.named_human`. |
| AC-1 (Invariant 1: read-only / propose-only controlled records) | Partial | Covered structurally across all 13 capabilities once `snapshot_controlled_records` partitions strictly invariant fields from capability-scoped workspace slots (`PC-004`). |
| AC-2 (Invariant 2: non-exercise finite human-approved limits) | Partial | Covered across `Consumption`, `rai_release`, `chat_eval`, and `heldout_batch` once registry/release-owner `named_human` validation and the controlled-harness seam are added (`PC-001`). |
| AC-3 (Runtime bypass closures across `core` and `agents`) | Partial | All four Wave 3 bypasses are targeted; `P01-T01` needs entry-level guard placement in `Ai.look_at` so offline tests without `AI_ENDPOINT` observe registration/enabled refusal (`PC-005`). |
| AC-4 (Focused validation tier without `tools/rpi-checks.py`) | Partial | Commands match Focused tier, but `P03-T02` directs creating `/tmp/zf-104-venv` (`PC-002`) and `P03-T01` risks `mypy` `[no-untyped-call]` errors (`PC-003`). |
| AC-5 (Local commit with `Refs #104`, co-author trailer, no push) | Partial | Commit metadata and no-push rule match caller constraints; `P03-T02` must keep any local `.venv` gitignored or cleaned up inside the workspace without touching `/tmp` (`PC-002`). |
| Research `C1`-`C20` | Covered | Every codebase finding in `.copilot-tracking/research/2026-11-15/issue-104-bounded-ai-research.md` is traced to concrete tasks in `P01`-`P03`. |
| P01-T01 | Partial | Needs `Ai.look_at` top-of-function registration/enabled guard, `consumption_capability` wiring in `Ai.run`/`Ai.look_at`, and `named_human` checks in `ai_registry.authorizes_live` (`PC-001`, `PC-005`). |
| P01-T02 | Partial | Hardens `_require_bounds` and `price(..., synthetic=False)` accurately; should also expose a public read-only non-exercise inspection helper on `Consumption` so `bounded_ai.py` need not call private `_read` (`PC-001`). |
| P01-T03 | Partial | Needs optional `task_entry` test seam and `named_human` release/registry owner checks in `verify_non_exercise_enablement` (`PC-001`) plus partitioned slot digests in `snapshot_controlled_records` (`PC-004`). |
| P02-T01 | Covered | `ChatModel.__call__` safely binds `CallContext(..., CHAT_TASK, ...)` when `CURRENT.get() is None`, `Ai._request` replaces `configuration` with the active deployment digest (`src/core/src/zava_forward/core/ai.py:192`), and imports remain within `allowed_core`. |
| P02-T02 | Covered | `chat_eval.call_authorization` and `heldout_batch.authorization_problems` enforce `rai_release.named_human` while preserving `"no named owner authorisation"` and `"approved_by missing"` messages. |
| P03-T01 | Partial | Needs explicit `: Any` boundary aliases for untyped `zava_forward.core` collaborators so `mypy` (`strict = true`) passes without modifying `src/core/pyproject.toml` (`PC-003`). |
| P03-T02 | Partial | Must remove `/tmp/zf-104-venv` instructions and use an existing or workspace-local gitignored `.venv` (`PC-002`). |

## Verdict

* Verdict: Revise
* Rationale: The candidate plan's 3-phase architecture, 13-capability inventory (`ai_registry.tasks()`), ADR 0006 placement (`zava_forward.core.bounded_ai`), and four Wave 3 runtime hardening targets are well-grounded in `C1`-`C20`. However, five concrete, planner-correctable issues in the candidate plan and phase details would block clean implementation or weaken invariant verification if left unaddressed: (1) `verify_non_exercise_enablement` lacks a `task_entry` seam for `P03-T01`'s positive controlled-harness verification, omits `rai_release.named_human` checks on registry/contract owner fields, and lacks a public `Consumption` read helper (`PC-001`); (2) `P03-T02` directs creating a virtual environment under `/tmp/zf-104-venv` in an environment where `/tmp` writes are prohibited (`PC-002`); (3) `P03-T01` calls untyped legacy `core` classes directly under `mypy --strict` without `pyproject.toml` overrides or `: Any` aliases (`PC-003`); (4) `snapshot_controlled_records` collapses case digests before `capability` is known in `assert_controlled_records_unchanged` (`PC-004`); and (5) `P01-T01` places `Ai.look_at`'s registration/enabled check after `ai_prompts.render` and `not self.configured` (`PC-005`). All five are direct planner corrections requiring zero user input.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: `verify_non_exercise_enablement` lacks a controlled-harness registry seam, registry/contract `named_human` checks, and a public `Consumption` read helper

* Related IDs: FR-1, FR-2, FR-3, FR-4, AC-2, C1, C2, C9, C10, P01-T01, P01-T02, P01-T03, P03-T01
* Evidence: `src/core/src/zava_forward/core/ai_registry.py:131-185, 238-244`; `src/core/src/zava_forward/core/rai_release.py:80-113, 127-141, 155-189`; `src/core/src/zava_forward/core/ai_consumption.py:514-532, 712-748`; `.copilot-tracking/details/2026-11-15/issue-104-bounded-ai-phase-details.md:162-167, 299-302`
* Concern: Three interlocking gaps exist in the non-exercise enablement contract across `P01` and `P03-T01`:
  1. `ai_registry.tasks()` builds fresh dictionaries on every call with `accountable_individual="unknown"` across all 13 capabilities and `enabled=False` on `chat-case-conversation` and `aftercare-concern-pack`, while `verify_non_exercise_enablement` rightly rejects `demo_activation_honoured` with `"demo-activation-is-exercise-only"`. Without an optional `task_entry: Mapping[str, Any] | None = None` override parameter (defaulting to `ai_registry.get(task_id)` in production), `verify_non_exercise_enablement` can never evaluate `allowed=True` for any of the 13 capabilities in `P03-T01` item 5's controlled test harness without monkeypatching `ai_registry.tasks`.
  2. `ai_registry.authorizes_live` (`src/core/src/zava_forward/core/ai_registry.py:238-244`) checks only `!= "unknown"` and `!= "unapproved"` rather than `rai_release.named_human(...)`, and `rai_release.missing_contract` / `valid_consumption` (`src/core/src/zava_forward/core/rai_release.py:84, 139`) check `named(...)` rather than `named_human(...)` on `accountable_owner` and `alert_contact`. Non-human values such as `"system"` or `"copilot"` in registry `accountable_individual` or `authority` values or in `release_record["accountable_owner"]` would pass those predicates unless `named_human` is enforced explicitly.
  3. `Consumption` exposes no public read method (`_read` at `src/core/src/zava_forward/core/ai_consumption.py:514` is private), and checking only static price/authority existence in `bounded_ai.py` without verifying `retrieved <= now`, `start <= now < end`, `model == price["model"]`, and `_currency_hold(...) is None` diverges from `Consumption.reserve_in` (`src/core/src/zava_forward/core/ai_consumption.py:715, 744`).
* Impact: `P03-T01` cannot cleanly execute positive non-exercise admission and subsequent exhaustion verification across all 13 capabilities; non-human tokens in registry or release `accountable_owner` fields could bypass Invariant 2; and `bounded_ai.py` would couple to private `Consumption._read` with weaker checks than `reserve_in`.
* Smallest useful change: Update `FR-3`, `P01-T01`, `P01-T02`, and `P01-T03` so that: (a) `ai_registry.authorizes_live` (outside the demo switch) and `bounded_ai.verify_non_exercise_enablement` require `rai_release.named_human` on `accountable_individual`, all `authority` holders, and `release_record["accountable_owner"]` (plus `rai_release.named` on `delegation`); (b) `verify_non_exercise_enablement` accepts an optional `task_entry: Mapping[str, Any] | None = None` parameter for controlled test harnesses while defaulting to `ai_registry.get(task_id)`; and (c) `Consumption` exposes a public read-only non-exercise readiness method checking unexpired authority, unexpired `synthetic is False` price with `retrieved <= now` and matching `model`, `alert`, `alert_owner`, `max_calls >= 1`, `max_depth >= 1`, positive `calls`/`tokens`/`amount` on every budget, and `_currency_hold is None`.
* Action owner: planning parent
* Exact resolving evidence: `.copilot-tracking/plans/2026-11-15/issue-104-bounded-ai-plan.md` (`FR-3`, `P01-T02`, `P01-T03`) and `.copilot-tracking/details/2026-11-15/issue-104-bounded-ai-phase-details.md` (`P01-T01`, `P01-T02`, `P01-T03`) explicitly specify `named_human` checks on registry and release owners, the optional `task_entry` parameter on `verify_non_exercise_enablement`, and the public `Consumption` non-exercise readiness helper.
* Decision route: Direct planner correction; no user decision required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: `P03-T02` instructs creating a temporary virtual environment in `/tmp/zf-104-venv`, violating workspace-only write constraints

* Related IDs: AC-4, AC-5, P03, P03-T02
* Evidence: `.copilot-tracking/details/2026-11-15/issue-104-bounded-ai-phase-details.md:274, 323, 333`
* Concern: `P03-T02` (`Boundaries` at line 323 and `Validation Expectations` at line 333) instructs placing a temporary test virtual environment under `/tmp/zf-104-venv`. Writing to `/tmp` or any temporary directory outside the workspace root is prohibited by active host execution constraints, and conflicts with `P03` line 274 which specifies workspace-local `.venv` usage.
* Impact: If `rpi-implement` follows `P03-T02` literally and attempts to create `/tmp/zf-104-venv`, validation violates host rules or fails execution; conversely, creating an unignored venv directory inside the worktree without pre-commit verification risks staging untracked environment files in the `Refs #104` commit (`AC-5`).
* Smallest useful change: Remove all `/tmp` references from `P03-T02` in `.copilot-tracking/details/2026-11-15/issue-104-bounded-ai-phase-details.md` and specify reusing an existing Python environment or a workspace-relative gitignored `.venv` (confirming via `git status --short` that `.venv` is ignored or removed before committing).
* Action owner: planning parent
* Exact resolving evidence: `.copilot-tracking/details/2026-11-15/issue-104-bounded-ai-phase-details.md` (`P03-T02`) contains no `/tmp` paths and directs workspace-local gitignored `.venv` validation plus `git status --short` verification before commit.
* Decision route: Direct planner correction; no user decision required.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: `P03-T01` omits `: Any` boundary aliases for untyped legacy `zava_forward.core` modules under `mypy --strict`

* Related IDs: NFR-2, AC-4, C19, P01-T03, P03-T01
* Evidence: `src/core/pyproject.toml:36-41, 56-148`; `src/agents/tests/test_epic104_bounded_ai_invariants.py:43`; `.copilot-tracking/plans/2026-11-15/issue-104-bounded-ai-plan.md:42, 80, 108-112`; `.copilot-tracking/details/2026-11-15/issue-104-bounded-ai-phase-details.md:145, 283-315`
* Concern: `src/core/pyproject.toml` sets `strict = true` (`disallow_untyped_calls = true`) across `files = ["src", "tests"]`, while legacy migrated modules (`ai`, `ai_registry`, `assistants`, `ranking`, `store`, `sqlstore`) carry `ignore_errors = true` with untyped function and class definitions. Every existing typed test in `src/core/tests/` that invokes `Store`, `SqlStore`, `ranking`, or `ai` required a `disallow_untyped_calls = false` override in `src/core/pyproject.toml:76-148`, yet modifying `pyproject.toml` is a locked Non-Goal. Although `P01-T03` explicitly requires `: Any` aliases in `bounded_ai.py`, `P03-T01` directs `src/core/tests/test_epic104_bounded_ai_invariants.py` to instantiate and call `Store`, `SqlStore`, `Assistants`, `Ai`, `ai_registry`, and `ranking` without documenting `: Any` boundary aliases.
* Impact: Direct calls to `Store(...)`, `SqlStore(...)`, `Assistants(...)`, `Ai()`, `ai_registry.tasks()`, or `ranking.canonical(...)` inside `src/core/tests/test_epic104_bounded_ai_invariants.py` fail `mypy` in `src/core` with `[no-untyped-call]`.
* Smallest useful change: Add explicit guidance in `P03-T01` (mirroring `P01-T03` and `src/agents/tests/test_epic104_bounded_ai_invariants.py:43`) requiring `: Any` aliases at module/constructor import boundaries for untyped `zava_forward.core` collaborators (`Store`, `SqlStore`, `Assistants`, `Ai`, `ai_registry`, `ranking`) so `mypy` exits 0 without touching `src/core/pyproject.toml`.
* Action owner: planning parent
* Exact resolving evidence: `.copilot-tracking/details/2026-11-15/issue-104-bounded-ai-phase-details.md` (`P03-T01`) explicitly requires `: Any` boundary aliases for untyped legacy `core` modules and constructors.
* Decision route: Direct planner correction; no user decision required.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: `snapshot_controlled_records` and `assert_controlled_records_unchanged` need partitioned workspace-slot digests to support capability-scoped draft allowances

* Related IDs: FR-3, FR-4, AC-1, C15, C16, P01-T03, P03-T01
* Evidence: `.copilot-tracking/research/2026-11-15/issue-104-bounded-ai-research.md:104, 152`; `.copilot-tracking/details/2026-11-15/issue-104-bounded-ai-phase-details.md:155-160, 292-295`
* Concern: `P01-T03` defines `snapshot_controlled_records(store, aftercare=None)` without a `capability` argument and pairs it with `assert_controlled_records_unchanged(before, after, *, capability=None)`, stating that `funding.draft` and `"Not started"`/`"To prepare"` -> `"Draft ready"` transitions are excluded only when `capability == "funding_draft"`, and unapproved `doc["summary"]` / necessity-summary metadata are excluded only when `capability == "read_document"`. If `snapshot_controlled_records` hashes each case into a single combined digest before `capability` is supplied, `assert_controlled_records_unchanged` cannot distinguish `funding_draft` or `read_document` workspace-note writes from unauthorized mutations without ignoring those slots across all other 11 capabilities.
* Impact: Implementers will either hit false-positive digest failures on `Store.funding_draft` and `Store.read_document` in `P03-T01` or silently weaken `snapshot_controlled_records` by omitting `funding.draft` and `doc["summary"]` checks for capabilities that must never touch them (such as `briefing`, `message`, `summary`, or `priority`).
* Smallest useful change: Specify in `P01-T03` that `snapshot_controlled_records` captures partitioned per-case digests/metadata separating (1) strictly invariant controlled records (`CONTROLLED_CASE_FIELDS`, `funding_ok`, `grants`, non-summary document fields, deterministic `ranking`, and optional `aftercare` `concerns`/`closures`), (2) the unapproved `funding` draft/status workspace slot, and (3) unapproved document summary/necessity-note slots, so `assert_controlled_records_unchanged` enforces equality across all partitions by default and relaxes only partition (2) (verifying `status == "Draft ready"`) when `capability == "funding_draft"` and only partition (3) when `capability == "read_document"`.
* Action owner: planning parent
* Exact resolving evidence: `.copilot-tracking/details/2026-11-15/issue-104-bounded-ai-phase-details.md` (`P01-T03`) defines partitioned controlled vs. workspace-slot snapshot fields for `snapshot_controlled_records` and `assert_controlled_records_unchanged`.
* Decision route: Direct planner correction; no user decision required.

<!-- rpi:critique id=PC-005 -->
### PC-005 [Low]: `Ai.look_at` registration/dispatch-enabled guard placement and `consumption_capability` wiring in `P01-T01` are underspecified

* Related IDs: FR-1, AC-3, C5, C6, P01, P01-T01
* Evidence: `src/core/src/zava_forward/core/ai.py:291-320, 338-382`; `.copilot-tracking/details/2026-11-15/issue-104-bounded-ai-phase-details.md:38, 82-90`
* Concern: In `Ai.look_at` (`src/core/src/zava_forward/core/ai.py:338-367`), `ai_prompts.render("read_document", name=name)` executes at line 341 and `if off or not self.configured:` returns `reason="AI is not configured"` at line 362 before the `try:` block calling `self._chat(...)` at line 378. `P01-T01` (`line 84`) says to check `is_registered("read_document")` and `is_dispatch_enabled("read_document")` "before calling `self._chat(...)`". Placed right before `self._chat(...)`, an unconfigured `Ai()` instance in unit tests returns `"AI is not configured"` rather than failing closed on unregistered/disabled state (unlike `Ai.run` at line 291), and unregistering `"read_document"` can fail earlier in `ai_prompts.render`. Additionally, `P01` (`line 38`) states `Ai.run` and `Ai.look_at` will use `ai_registry.consumption_capability` for `CallContext`, whereas `P01-T01` (`lines 82-84`) omits that edit target.
* Impact: Offline unit tests of `Ai.look_at` without `AI_ENDPOINT` may not reach the new registration/dispatch-enabled guard, and `ai_registry.consumption_capability` may remain unwired in `ai.py`.
* Smallest useful change: Update `P01-T01` in `.copilot-tracking/details/2026-11-15/issue-104-bounded-ai-phase-details.md` so `Ai.look_at` checks `ai_registry.is_registered("read_document")` and `ai_registry.is_dispatch_enabled("read_document")` immediately after `export_fields.scalars(...)` (before `ai_prompts.render`, `self.gate`, and `off or not self.configured`), and explicitly wire `ai_registry.consumption_capability` into `CallContext` construction in both `Ai.run` and `Ai.look_at`.
* Action owner: planning parent
* Exact resolving evidence: `.copilot-tracking/details/2026-11-15/issue-104-bounded-ai-phase-details.md` (`P01-T01`) specifies entry-level guard placement in `Ai.look_at` and `ai_registry.consumption_capability` usage in `Ai.run` and `Ai.look_at`.
* Decision route: Direct planner correction; no user decision required.

## Strengths and Residual Risk

* Strong canonical anchoring: Parameterizing enforcement and acceptance verification over `ai_registry.tasks()` (all 13 capabilities: 5 assistants, 6 retained tasks, `chat-case-conversation`, and `aftercare-concern-pack`) eliminates drift between `zava_forward.core` and `zava_forward.agents`.
* Clean ADR 0006 and AST-whitelist compliance: Placing `bounded_ai.py` in `zava_forward.core` respects `agents -> core` dependency rules, and `P02-T01` importing only from `zava_forward.core.ai_registry` and `zava_forward.core.ai_consumption` in `src/agents/src/zava_forward/agents/chat.py` preserves `AssistantNonMutation.test_worker_and_chat_adapters_import_no_store_or_controlled_record_module` (`allowed_core = {"assistants", "ai_registry", "ai", "ai_consumption", "chat_panel"}` at `src/agents/tests/test_epic104_bounded_ai_invariants.py:125`).
* Careful backward compatibility with existing fixtures: Distinguishing `rai_release.named(alert)` (accepting `"alert-rule-ai-limits"`, which contains the token `"ai"`) from `rai_release.named_human(owner)` and `rai_release.named_human(alert_owner)` (accepting `"owner"`, `"alert-owner"`, `"approving-owner-fixture"`, and `"constructed-finance-owner"` while rejecting `"system"`, `"agent"`, `"copilot"`, `"bot"`, `"automation"`, `"unknown"`, and `"unapproved"`), and omitting `"alert"` when `alert=None` on synthetic exercise prices, preserves `src/core/tests/test_ai_consumption.py` and `src/api/tests/test_nonexercise_capability_bounds.py`.
* Explicitly accepted residual risk: Open decision OD-51 (live Azure OpenAI pricing, operational budgets, and named human authorities) remains intentionally unassigned policy outside software scope, keeping all 13 capabilities `non_exercise_enabled == False` by default; `src/api` HTTP diagnostic surfacing of `bounded_ai.audit_registered_capabilities()` is appropriately deferred outside this `src/core` + `src/agents` slice, and commit linkage properly uses `Refs #104`.

## Questions or Blocking Evidence Gaps

* None. All five findings (`PC-001` through `PC-005`) are fully resolved by supplied codebase evidence and confirmed caller constraints without requiring user input or additional research.

## Limitations

* Sibling modules not included in the caller's 11-file read-only verification list (`store.py`, `sqlstore.py`, `assistants.py`, `chat_panel.py`, `aftercare.py`, `dispatch.py`, `runtime.py`, `test_chat_eval.py`, `test_heldout_batch.py`) were not opened directly during critique per `rpi-plan-critique` non-research constraints; their interfaces and behaviors were evaluated from verified research evidence (`C1`-`C20`) and `src/agents/tests/test_epic104_bounded_ai_invariants.py`.
* No unit tests, linters, or typecheckers were executed during this read-only plan critique phase; runtime and static verification occurs in `P03` during `rpi-implement`.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning parent
* Smallest next action: Apply direct planner revisions for `PC-001` through `PC-005` in `.copilot-tracking/plans/2026-11-15/issue-104-bounded-ai-plan.md` and `.copilot-tracking/details/2026-11-15/issue-104-bounded-ai-phase-details.md`, record critique disposition, finalize the plan without a second critique pass, and continue automatically to `rpi-implement`.
* User response required: no
