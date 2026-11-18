---
description: "Primary evidence artifact for Issue #164 local-testable RAI multi-turn revocation, refusal preservation, and separate held-out reporting"
---
<!-- markdownlint-disable-file -->

# Task Research: issue-164-chat-eval-revocation

| Field              | Value                                                                                  |
|--------------------|----------------------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                             |
| Researcher / agent | rpi-research (via RPI Agent)                                                           |
| Status             | Complete                                                                               |
| Artifact path      | .copilot-tracking/research/2026-11-15/issue-164-chat-eval-revocation-research.md       |

## Research Brief

* What to research: Remaining local-testable RAI multi-turn and memory evaluation criteria for Issue #164 across `src/core`, `src/agents`, and `src/api`, specifically: (1) mid-thread permission and source revocation authority clearing (covering unsupported claims with valid citations, stale/conflicting sources, ambiguity, abstention, and mid-thread revocation), (2) multi-turn refusal and human workflow route preservation (proving prior turns or memory cannot manufacture approval or resident consent for approve/decide/consent/diagnose/contact asks), and (3) separate chat multi-turn vs single-turn reporting and version-bound held-out freeze while keeping live chat enablement `disabled` until owner threshold approval.
* Why it matters: Closes any remaining gaps between `src/core` (`ai_eval.py`, `regulatory_chat.py`, `test_ai_eval.py`), `src/agents` (where PR #1643 landed agent-layer checks), and `src/api` (`test_ai_tasks.py`) so that core and API evaluation/chat boundaries deterministically enforce and regression-test all three local-testable RAI acceptance criteria of Issue #164 without transferring authority or enabling live calls.
* Audience or intended use: Downstream `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, and `rpi-review` phases in this confirmed automatic RPI session, plus PR reviewers on parent branch `feat/demo-164-chat-grounding-provenance-0900` (`#1641`).
* Scope: `src/core/src/zava_forward/core/` (`ai_eval.py`, `regulatory_chat.py`, and directly coupled chat/eval helpers), `src/agents/src/zava_forward/agents/` (read/compare as needed for parity), `src/core/tests/test_ai_eval.py`, `src/api/tests/test_ai_tasks.py` (and coupled API chat/eval modules), `docs/prds/zava-forward-retrofit-programme-demonstrator.md` (FR-036, FR-037, AC-045, AC-054, AC-057, RAI v0.16.0 contract), and prior `#164` tracking artifacts.
* Non-goals: Live serving-model calls, spend/budget authorization, competent-human exercise execution, owner threshold sign-off, enabling the chat task (`enabled` must remain `False`/`disabled`), running `tools/rpi-checks.py --all`, or pushing to remote.
* Criteria: Every claim grounded in workspace `path:line` (`C#`); clear mapping between `src/core`, `src/agents`, and `src/api`; converged surgical design covering all three target increments with focused unit tests, `mypy`, and `ruff`.
* Requested outputs: Converged implementation recommendation with exact file/function targets, gaps vs existing PR #1643/#1660/#1734 code, and test cases.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                                                                               |
|----------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)             | Q1-Q5 covering module layout (`src/core` vs `src/agents` vs `src/api`), mid-thread revocation clearing, multi-turn refusal/consent immunity, held-out version freeze + separate chat/single-turn reporting, and test harness conventions |
| Codebase scope                   | `src/core/`, `src/agents/`, `src/api/`, `docs/prds/`, `.copilot-tracking/`                                                          |
| External scope                   | none (codebase-internal contract and evaluation harness task)                                                                       |
| Initial internal candidate areas | `src/core/src/zava_forward/core/ai_eval.py`, `src/core/src/zava_forward/core/regulatory_chat.py`, `src/core/tests/test_ai_eval.py`, `src/api/tests/test_ai_tasks.py`, `.copilot-tracking/research/2026-11-14-issue-164-eval-revocation-0900-research.md` |
| Initial external candidate areas | none                                                                                                                                |
| Research posture                 | focused                                                                                                                             |
| Posture provenance               | caller-specified (named target files, three bounded local-testable criteria, and focused validation tier)                           |
| Explicit limits / deadline       | Focused validation tier only; do not run `tools/rpi-checks.py --all`; do not push                                                   |
| Posture-specific completion basis| focused scope and materiality: all named files, coupled chat/eval modules, and PRD/issue contracts verified with no unresolved gap  |
| Edits allowed during research?   | no, research-only                                                                                                                   |
| Resolved evidence root           | `.copilot-tracking/`                                                                                                                |
| Known constraints / excluded sources | Keep chat task `disabled`; no new governance service; no external model calls; preserve existing API/SQL/assistant contracts    |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                                  | Match and provenance                                   | Scoped authority or output contract                                  | Selected / skipped reason                                                          |
|---------------------|--------------------------------------------|--------------------------------------------------------|----------------------------------------------------------------------|------------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md`          | `applyTo: "**"` repository instructions                | Branch/commit rules, validation tiers, RAI/consent human boundaries  | Selected: governs focused validation tier, no-enablement boundary, and commit rule |
| Skill               | `rpi-research`                             | Explicit caller RPI phase 1 skill                      | Three-wave read-only research and primary evidence artifact          | Selected: active phase skill                                                       |
| Skill               | `python-foundational` / `rai-standards`    | Domain match on Python unit tests and RAI boundaries   | General reference only                                               | Skipped: repository codebase and PRD v0.16.0 already define exact local contracts  |
| Research specialist | `hve-core-all:rpi-researcher`              | General RPI lane worker                                | Delegated independent lane artifact                                  | Skipped (inline): tightly coupled 4-6 files in `src/core`, `src/agents`, `src/api` |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                                  | Answers / unanswered | Resulting decision or selected further research                                                  |
|------------------|------------------------------------------------------------------------------------------------------------------------|----------------------|--------------------------------------------------------------------------------------------------|
| Intake           | Non-interactive session with explicit caller scope, named files, validation tier, and commit-without-push instructions | N/A (autonomous)     | Proceed in `focused` posture on current worktree `feat-164-chat-revocation-0042` (`#1641` child) |
| Direction change | None at intake                                                                                                         | N/A                  | Retain initial three-part scope                                                                  |
| Convergence      | Non-interactive convergence after Cycle 1 Wider, Deeper, and Contrarian waves                                          | N/A (autonomous)     | Converged on pure-core `zava_forward.core.ai_eval`, `RegulatoryChat` hardening, held-out frozen expected-outcome gate, and separate `/api/ai/report` `chat_evaluation` reporting |

## Scope and Success Criteria

* Scope: Inspect `src/core`, `src/agents`, and `src/api` chat/evaluation modules and tests to determine what already exists on `feat/demo-164-chat-grounding-provenance-0900` (`fef48b6df`) versus what is missing or only in `src/agents` vs `src/core`/`src/api`, and converge on a clean, deterministic increment.
* Assumptions:
  * Some chat evaluation code may reside in `src/agents` (`ai_eval.py` or `chat_eval.py`) as well as or instead of `src/core/src/zava_forward/core/ai_eval.py`; verify exact module locations first.
  * PR #1643 (`788408e25`), PR #1660 (`2e1dee5e1`), and PR #1734 (`2b1d40db0`) are already ancestors of HEAD (`fef48b6df`); verify exactly what they cover and what gaps remain in `src/core` and `src/api`.
* Success criteria:
  * Every research question is answered or marked unanswerable with the missing evidence named.
  * Evidence is grounded in actual code, docs, or tooling results, with locations (`path:line` for code).
  * Findings, decisions, and readiness claims cite Evidence Log IDs.
  * Alternatives are compared with trade-offs and one converged recommendation is selected.
  * Open questions, risks, and residual uncertainty are recorded.
  * Self-check passes.

## Task Research Requests

* Explicit requests:
  1. Inspect `src/core/src/zava_forward/core/ai_eval.py`, `src/core/src/zava_forward/core/regulatory_chat.py`, `src/core/tests/test_ai_eval.py`, and `src/api/tests/test_ai_tasks.py`.
  2. Complete and regression-test mid-thread permission & source revocation authority clearing (prior-turn content cannot retain authority after permission or source revocation mid-thread; cover unsupported claims with valid citations, stale/conflicting sources, ambiguity, abstention, and mid-thread revocation).
  3. Complete and regression-test multi-turn refusal & human workflow route preservation (approve, decide, consent, diagnose, contact residents refused with workflow route across turns; previous turns or memory cannot manufacture approval or resident consent).
  4. Verify and regression-test separate chat multi-turn vs single-turn reporting and version-bound held-out freeze (independently labelled held-out conversation scenarios freeze expected outcomes, critical errors, and task/model/prompt/policy/source/memory versions before testing; chat-specific failures and complete review effort reported separately from single-turn task results; live task enablement stays `disabled` until owner threshold approval).
* Inferred research questions:
  * How do `src/core` and `src/agents` divide or share `ai_eval` and `regulatory_chat` responsibilities after the `src/` package cut-over?
  * What did commit `788408e25` (`#1643`) implement, and what remains uncovered or weakly enforced in `src/core` (`ai_eval.py`, `regulatory_chat.py`, `test_ai_eval.py`) and `src/api` (`test_ai_tasks.py`)?
* Caller constraints and non-goals: Focused validation tier (`unittest`, `mypy`, `ruff`), no `tools/rpi-checks.py --all`, keep live chat enablement `disabled`, commit locally with Copilot trailer, do not push.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                                                   | Source / checkpoint | Effect on active brief, evidence, or revalidation                         |
|----------------------------------------------------------|---------------------------------------------------------------------------------------------------------|---------------------|---------------------------------------------------------------------------|
| narrow                                                   | Local-testable deterministic multi-turn revocation, refusal, and separate reporting in core/agents/api  | Caller intake       | Constrains scope to offline deterministic contracts and regression suites |
| exclude                                                  | Do not enable live chat task, make live model calls, run `tools/rpi-checks.py --all`, or push to remote | Caller intake       | Preserves `enabled=False` gate and focused local validation tier          |

## Research Questions

|  # | Sub-question                                                                                                                                             | Type            | Priority | Status   |
|---:|----------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------|----------|----------|
| Q1 | Where do `ai_eval.py`, `regulatory_chat.py`, `test_ai_eval.py`, and `test_ai_tasks.py` live across `src/core`, `src/agents`, and `src/api`, and how are they wired? | straightforward | H        | answered |
| Q2 | How do runtime chat (`regulatory_chat.py` / agents / API) and the evaluation harness currently handle mid-thread permission/source revocation, unsupported claims with valid citations, stale/conflicting sources, ambiguity, and abstention? | depth           | H        | answered |
| Q3 | How are multi-turn out-of-scope requests (`approve`, `decide`, `consent`, `diagnose`, `contact`) and prior-turn/memory-manufactured approval or consent currently handled across runtime and eval? | depth           | H        | answered |
| Q4 | How does the held-out evaluation freeze bind expected outcomes, critical errors, and `task`/`model`/`prompt`/`policy`/`source`/`memory` versions before testing, and how are chat multi-turn failures and complete review effort separated from single-turn task results while keeping chat `disabled`? | depth           | H        | answered |
| Q5 | Could existing tests pass trivially (e.g., fixture-only metadata checks without runtime state enforcement, or `src/agents` checks bypassed in `src/core`/`src/api`)? | depth           | H        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `.copilot-tracking/research/2026-11-14-issue-164-eval-revocation-0900-research.md`, `.copilot-tracking/changes/2026-11-14-issue-164-eval-revocation-0900-changes.md`, `.copilot-tracking/changes/2026-11-14/164-case-domain-grounding-1445-changes.md`, verified against HEAD `fef48b6df`.
* Reused (verified) findings: PRs `#1643`, `#1660`, and `#1734` are ancestors of HEAD `fef48b6df`, supplying `ChatPanel` grounding/refusal/consent rules and `agents.chat_eval`/`agents.chat_heldout`.
* Superseded / stale: Legacy `mvp/zavaforward_mvp/ai_eval.py` paths in Issue #164 body were retired at the `2026-10-27` `src/` cut-over (`v0.21.0`).

## Cycle 1 Execution

### Wave 1: Wider

* Inspected package boundaries, existing evaluation modules, registry definitions, and unit suites across `src/core`, `src/agents`, and `src/api` (`C1`–`C8`).
* Confirmed `src/core/tests/test_dependency_rule.py` enforces `ALLOWED = {"core"}` across every `.py` file under `src/core/src` and `src/core/tests` (`C1`); `zava_forward.core.ai_eval` must import only `zava_forward.core.*`.
* Confirmed `src/core/src/zava_forward/core/ai_eval.py` and `src/core/tests/test_ai_eval.py` do not exist yet, so `python3 -m unittest discover -s tests -p "test_*ai_eval*.py" -q` inside `src/core` finds zero tests until `test_ai_eval.py` is created (`C2`).
* Confirmed `ai_registry.py` registers `chat-case-conversation` as `unapproved` with `authorizes_live("chat-case-conversation") == False` (`C3`).

### Wave 2: Deeper

* Inspected `ChatPanel.ask` (`C4`, `C5`), `ChatIsolation` (`C6`), `RegulatoryChat` (`C7`, `C8`), `agents.chat_eval` (`C9`, `C10`), `agents.chat_heldout` (`C11`), `evals/chat_golden.json` (`C12`), `server.py` `/api/ai/report` (`C13`), and `api/tests/test_ai_tasks.py` (`C14`).
* Verified `ChatPanel.ask` excludes all assistant messages and prior-role user messages from prompt history (`m["role"] == "user" and m.get("actor_role") == user["role"]`), re-verifies role and `permitted_sources` post-provider (`C5`), withholds lexical action claims (`ACTION_CLAIM`) and unsupported numeric/status claims on valid citations (`unsupported_claims` -> `UNGROUNDED`), and routes non-`Given` `ai_data_use_consent` via `consent_guidance` (`C4`, `C5`).
* Verified `RegulatoryChat.ask` and `RegulatoryChat.bundle` re-admit the user and re-project the case per turn without passing prior conversation turns into retrieval, flag changed/superseded cited provisions or multi-signature cards as `conflict=True`, refuse when `>2` cards or `>4` provisions match, and re-verify inside `repo.txn()` (`C7`, `C8`).
* Verified `/api/ai/report` in `server.py` returns single-turn `evaluation: ai_eval.run_eval()` where `task_coverage` marks `chat-case-conversation` as `"not evaluated by this harness"`, without a separate multi-turn `chat_evaluation` sibling (`C13`, `C15`).

### Wave 3: Contrarian

* **Contrarian Finding 1 — Missing ambiguity, mid-thread source-field deletion, and mid-thread AI-consent withdrawal coverage in multi-turn evaluation (`C9`, `C12`)**:
  * `evals/chat_golden.json` and `agents.chat_eval` contain zero explicit ambiguity scenarios (`C12`), and `Run._apply` supports only `set`, `set_role`, `remove_staff`, `remove_case`, and `remember` (`C9`), lacking mid-thread case-source deletion/revocation and nested `resident.ai_data_use_consent` withdrawal operations.
* **Contrarian Finding 2 — `RegulatoryChat` in `core` relies solely on caller `refuse` callback for out-of-scope asks and omits `ai_consent_state` mid-thread revocation checks (`C7`, `C16`, `C17`)**:
  * When `RegulatoryChat` receives a minimal `refuse` callback (such as `lambda _: None` in `core/tests/test_regulatory_chat.py:401`), `RegulatoryChat.bundle` and `RegulatoryChat.foundry_query` do not fall back to `core.chat_panel.out_of_scope(question)`, failing to refuse `approve`/`decide`/`consent`/`diagnose`/`contact` asks at the core boundary (`C7`, `C16`). Checking `self.refuse(question)` first and falling back to `REFUSED + hit[1]` when `out_of_scope(question)` matches closes this core gap while preserving `REASONS["legal"]` in `agents/tests/regulatory_gate_fixture.py:31` (`C17`).
  * `RegulatoryChat` also omits `consent_guidance(self.iso.ai_consent_state(cid))` (`C6`, `C7`). Enforcing `consent_guidance` across `bundle`, `foundry_query`, and `doubt` leaves cases without recorded `ai_data_use_consent` (`None`) unchanged while immediately revoking home-fact retrieval, Foundry queries, and turn forwarding when resident AI/data-use consent is `"Withdrawn"`, `"Declined"`, `"Pending"`, or `"Not requested"` mid-thread.
* **Contrarian Finding 3 — Vacuous held-out scenarios when per-turn expected outcomes are omitted (`C10`, `C11`)**:
  * `chat_heldout.freeze_problems` checks digest, independent `labelled_by`, `frozen_at`, `critical_errors`, the 6 `REQUIRED_BINDINGS`, non-empty scenarios, and development/prompt leaks, **but does not verify that every held-out scenario turn freezes an expected outcome (`expect.kind` or `expect.error`) before testing** (`C11`). Because `_check_turn` checks only keys present in `turn.get("expect", {})` (`C10`), a turn with `expect={}` vacuously passes! Also, `run_heldout` omits `chat_specific`, `review_effort`, and `enablement` (`state="disabled"`).

## Evidence Log

| ID | Location | Finding |
|----|----------|---------|
| `C1` | `src/core/tests/test_dependency_rule.py:13` | `ALLOWED = {"core"}` forbids any `zava_forward.agents` or `zava_forward.api` import inside `src/core/src` and `src/core/tests`. |
| `C2` | `src/core/src/zava_forward/core/` | `ai_eval.py` and `src/core/tests/test_ai_eval.py` are absent; `unittest discover -s tests -p "test_*ai_eval*.py"` in `src/core` exits non-zero unless `test_ai_eval.py` exists. |
| `C3` | `src/core/src/zava_forward/core/ai_registry.py:145` | `chat-case-conversation` is registered `unapproved` with `authorizes_live("chat-case-conversation") == False`. |
| `C4` | `src/core/src/zava_forward/core/chat_panel.py:92` | `OUT_OF_SCOPE`, `ACTION_CLAIM`, `unsupported_claims`, and `consent_guidance` define refusal routes, lexical action-claim withholding, unsupported status/number claim withholding (`UNGROUNDED`), and resident AI-consent blocking. |
| `C5` | `src/core/src/zava_forward/core/chat_panel.py:863` | `ChatPanel.ask` blocks non-`Given` `ai_data_use_consent`, restricts prompt history to same-role user turns, and re-verifies role and `permitted_sources` post-provider. |
| `C6` | `src/core/src/zava_forward/core/chat_isolation.py:92` | `ChatIsolation.ai_consent_state` returns `None` when `ai_data_use_consent` is unset and returns the recorded state otherwise; memory items carry `authority="none"` and `evidence=False`. |
| `C7` | `src/core/src/zava_forward/core/regulatory_chat.py:258` | `RegulatoryChat.bundle`, `foundry_query`, `ask`, and `doubt` re-admit the user and re-check active rule cards/provisions per turn, but rely solely on `self.refuse` for out-of-scope prompts and omit `ai_consent_state` checks. |
| `C8` | `src/core/src/zava_forward/core/regulatory_chat.py:288` | `RegulatoryChat.bundle` marks changed/ineligible cited provisions or multi-signature cards `conflict=True` and refuses when `>2` cards or `>4` provisions match. |
| `C9` | `src/agents/src/zava_forward/agents/chat_eval.py:194` | `Run._apply` supports `set`, `set_role`, `remove_staff`, `remove_case`, and `remember`, lacking mid-thread source-field deletion and nested `resident.ai_data_use_consent` mutation ops. |
| `C10` | `src/agents/src/zava_forward/agents/chat_eval.py:292` | `_check_turn` checks only keys present in `turn.get("expect", {})`, allowing empty `expect` dicts to pass vacuously. |
| `C11` | `src/agents/src/zava_forward/agents/chat_heldout.py:55` | `freeze_problems` omits per-turn frozen expected-outcome checks and `run_heldout` omits `chat_specific`, `review_effort`, and `enablement` (`state="disabled"`). |
| `C12` | `src/agents/evals/chat_golden.json:1` | Golden scenarios lack explicit mid-thread source-field deletion, mid-thread resident AI-consent withdrawal, and multi-turn ambiguity abstention scenarios. |
| `C13` | `src/api/src/zava_forward/api/server.py:928` | `/api/ai/report` returns single-turn `evaluation: ai_eval.run_eval()` without a separate multi-turn `chat_evaluation` sibling report. |
| `C14` | `src/api/tests/test_ai_tasks.py:628` | `Endpoints.test_report_is_manager_only` checks `/api/ai/report` single-turn `evaluation` only. |
| `C15` | `src/agents/src/zava_forward/agents/ai_eval.py:211` | Single-turn `ai_eval.task_coverage()` marks `chat-case-conversation` as `evaluated=False`. |
| `C16` | `src/core/tests/test_regulatory_chat.py:401` | `RegulatoryChat` unit fixture passes `lambda _: None` as `refuse`. |
| `C17` | `src/agents/tests/regulatory_gate_fixture.py:31` | `REASONS["legal"]` asserts `agents.regulatory_chat.refusal` exact string `"This question needs a human decision or legal interpretation."`. |

## Parent Synthesis and Converged Recommendation

* **Selected Recommendation**:
  1. **Core Multi-Turn Chat & Held-Out Evaluation Contract (`src/core/src/zava_forward/core/ai_eval.py`)**: Implement a pure-`core` module (importing only `zava_forward.core.*`, respecting `C1`) providing deterministic multi-turn conversation evaluation across `ChatPanel` and `RegulatoryChat`, version-bound held-out freeze verification (requiring frozen per-turn expected outcomes `kind`/`error`, `critical_errors`, independent `labelled_by`, `frozen_at`, `scenarios_sha256`, optional `expected_outcomes_sha256`, all 6 version `bindings`, and development/prompt leak rejection), separate multi-turn vs single-turn report assembly (`separate_evaluation_report`, `chat_specific`, `review_effort` requiring all 4 review-effort inputs, and `enablement_decision` keeping `state="disabled"` until owner threshold approval and live gates), and deterministic multi-turn scenarios covering unsupported claims with valid citations, stale/conflicting sources, ambiguity, abstention, mid-thread permission/source/consent revocation, and multi-turn refusal/workflow route preservation (`approve`, `decide`, `consent`, `diagnose`, `contact`) with zero manufactured approval or resident consent from history or memory.
  2. **Core `RegulatoryChat` Boundary Hardening (`src/core/src/zava_forward/core/regulatory_chat.py`)**: Enforce `consent_guidance(self.iso.ai_consent_state(cid))` across `bundle`, `foundry_query`, and `doubt` when recorded `ai_data_use_consent` is revoked/not `Given`, and enforce fallback `REFUSED + out_of_scope(question)[1]` in `bundle` and `foundry_query` whenever `self.refuse(question)` returns `None` (`C7`, `C16`, `C17`).
  3. **Agents Multi-Turn & Held-Out Alignment (`src/agents/src/zava_forward/agents/chat_eval.py`, `chat_heldout.py`, `evals/chat_golden.json`)**: Add `revoke_source` (field deletion) and `set_ai_consent` operations to `Run._apply`; add multi-turn source-field revocation, mid-thread AI-consent revocation, and ambiguity abstention scenarios to `evals/chat_golden.json` and `REVOCATION_SCENARIOS`; enforce frozen per-turn expected outcomes (`expect.kind` or `expect.error`, plus `expected_outcomes_sha256` when present) in `chat_heldout.freeze_problems` and include `chat_specific`, `review_effort`, and `enablement` (`state="disabled"`) in `chat_heldout.run_heldout`.
  4. **Separate API Reporting (`src/api/src/zava_forward/api/server.py`) & Deterministic Regression Suites (`src/core/tests/test_ai_eval.py`, `src/core/tests/test_regulatory_chat.py`, `src/agents/tests/test_chat_heldout.py`, `src/api/tests/test_ai_tasks.py`)**: Expose separate `chat_evaluation` sibling in `/api/ai/report` without mixing into single-turn `evaluation`, and add comprehensive regression tests across all 3 scope items.
* **Rejected Alternatives**:
  * Importing `zava_forward.agents` inside `src/core` — rejected because `test_dependency_rule.py` (`C1`) forbids non-`core` imports.
  * Leaving `src/core/tests/test_ai_eval.py` absent — rejected because caller explicitly targets `src/core/src/zava_forward/core/ai_eval.py` and `src/core/tests/test_ai_eval.py` (`C2`).
* **Research execution status**: Complete (Cycle 1 Wider, Deeper, Contrarian finished; re-entry not needed).
* **Research disposition**: `executed`
* **Planning Readiness**: `Ready`
