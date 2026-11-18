<!-- markdownlint-disable-file -->
# RPI Changes: Issue #164 Chat Evaluation, Revocation & Refusal Boundaries

## Metadata

* Task ID: issue-164-chat-eval-revocation
* Related plan: .copilot-tracking/plans/2026-11-15/issue-164-chat-eval-revocation-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/issue-164-chat-eval-revocation-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: Full plan (`P01` through `P04`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01`, `P04`, `P04-T01`, `P04-T02`
* All remaining active-plan markers: none
* Status basis: All planned tasks (`P01-T01` through `P04-T02`) implemented and verified green against focused unit suites, strict/configured `mypy`, `ruff check`, and `ruff format --check` across `src/core`, `src/agents`, and `src/api`.

## Execution Summary

Completed full-plan implementation in plan order (`P01` -> `P02` -> `P03` -> `P04`) for Issue #164 (`Grounding, evaluation and human-review boundaries for chat`): hardened `RegulatoryChat` mid-thread AI-consent revocation and pre-redaction `out_of_scope` human-workflow refusal routing; built the pure-`core` deterministic multi-turn evaluation, held-out freeze, and separate reporting module (`zava_forward.core.ai_eval`); extended `agents.chat_eval`, `evals/chat_golden.json`, and `agents.chat_heldout` with source/consent revocation, ambiguity abstention, and closed-set frozen expected-outcome gates; exposed multi-turn `chat_evaluation` separately from single-turn `evaluation` in `/api/ai/report` while keeping live chat enablement `disabled`; and added deterministic regression suites across `src/core`, `src/agents`, and `src/api`.

## Completed Work

### P01: Core `RegulatoryChat` Hardening and `zava_forward.core.ai_eval` Contract (`P01-T01`, `P01-T02`)

* Modified `src/core/src/zava_forward/core/regulatory_chat.py` (`P01-T01`):
  * Added `_question_refusal(question)` preserving caller-supplied `self.refuse(question)` precedence first and falling back to `REFUSED + out_of_scope(question)[1]`.
  * Evaluated `_question_refusal(clean_q)` in `ask()` prior to `redact(clean_q)` so special-category medical terms (such as `"Diagnose..."` -> `"[special_category removed]"`) cannot strip out-of-scope refusal routing while still storing only redacted text in `chat_repo`.
  * Enforced `consent_guidance(self.iso.ai_consent_state(cid))` after `self.store.detail(cid, user)` authorization in `bundle()` and `foundry_query()`, re-checked `ai_consent_state` inside `ask()`'s `repo.txn()` transaction, and blocked `doubt()` forwarding with `ChatForbidden` when recorded resident AI consent is withdrawn or not `Given`.
* Created `src/core/src/zava_forward/core/ai_eval.py` (`P01-T02`):
  * Pure-`core` module importing only `zava_forward.core.*` (`ALLOWED = {"core"}`).
  * Implemented deterministic `PanelSession` and `RegulatorySession` multi-turn harnesses, 8 built-in scenarios (`core_scenarios()`, `run_core_suite()`), closed-set `expected_outcome_problems`, `expected_outcomes_digest`, `heldout_freeze_problems`, `score_heldout`, canonical 4-component `REVIEW_EFFORT_INPUTS`, `chat_enablement_state` (`state="disabled"`), and `separate_evaluation_report`.

### P02: Agents Multi-Turn Golden Coverage and Held-Out Expected-Outcome Freeze (`P02-T01`)

* Modified `src/agents/src/zava_forward/agents/chat_eval.py`, `src/agents/evals/chat_golden.json`, and `src/agents/src/zava_forward/agents/chat_heldout.py` (`P02-T01`):
  * Added non-destructive `revoke_source` and `set_ai_consent` operations to `Run.apply`, unioned `WORKFLOW_RULES` into `_comparison` allowed citation IDs, and registered new `permission` and `grounding` revocation/ambiguity scenarios in `chat_golden.json` and `REVOCATION_SCENARIOS`.
  * Delegated `chat_heldout.freeze_problems` per-turn outcome verification and optional `expected_outcomes_sha256` digest checking to `zava_forward.core.ai_eval`, and exposed `chat_specific`, 4-part `review_effort`, `bindings`, and `enablement` (`state="disabled"`) on `run_heldout`.

### P03: Separate Chat Multi-Turn Reporting in `/api/ai/report` (`P03-T01`)

* Modified `src/api/src/zava_forward/api/server.py` (`P03-T01`):
  * Added separate top-level `"chat_evaluation": chat_eval.run_eval()` sibling in `/api/ai/report` alongside unchanged single-turn `"evaluation"` and `"live"`.

### P04: Deterministic Regression Suites and Focused Validation (`P04-T01`, `P04-T02`)

* Created `src/core/tests/test_ai_eval.py` (14 test methods, within `<= 22` cap) and extended `src/core/tests/test_regulatory_chat.py` (+3 test methods, within `<= 3` cap) (`P04-T01`).
* Extended `src/agents/tests/test_chat_heldout.py` (+3 test methods, within `<= 4` cap) and `src/api/tests/test_ai_tasks.py` (+2 test methods, within `<= 4` cap) (`P04-T02`).

## Implementation-Time Plan and Detail Updates

* Local judgment (`P01-T01`): During `P04-T01` execution, deterministic testing revealed that `RegulatoryChat.ask` called `redact(question.strip())[0]` before `bundle()`, causing `chat_privacy.redact` to replace `"Diagnose"` with `"[special_category removed]"` and bypass `out_of_scope` `"diagnose"` refusal routing when `self.refuse` returned `None`. Checking `self._question_refusal(clean_q)` before `redact(clean_q)` while continuing to store `masked` in `chat_repo` preserved approved plan intent and privacy guarantees without scope expansion.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `python3 -m unittest discover -s tests -p "test_*ai_eval*.py" -q` | `src/core` | Passed | 14 tests OK |
| `python3 -m unittest discover -s tests -p "test_regulatory_chat.py" -q` | `src/core` | Passed | 28 tests OK (JSON & SQLite) |
| `python3 -m unittest discover -s tests -p "test_chat_*.py" -q` & `test_dependency_rule.py` | `src/core` | Passed | 136 chat tests OK + 2 dependency-rule tests OK |
| `python3 -m mypy src tests`, `ruff check .`, `ruff format --check .` | `src/core` | Passed | `mypy` 0 issues in 334 files; `ruff` clean across 281 formatted files |
| `PYTHONPATH=../core/tests python3 -m unittest discover -s tests -p "test_chat_*.py" -q` | `src/agents` | Passed | 118 tests OK |
| `python3 -m mypy src tests`, `ruff check .`, `ruff format --check .` | `src/agents` | Passed | `mypy` 0 issues in 66 files; `ruff` clean across 62 formatted files |
| `PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -p "test_ai_tasks.py" -q` (+ `test_regulatory_chat_api.py`, `test_chat_*.py`) | `src/api` | Passed | 71 + 13 + 151 (1 skipped) tests OK |
| `python3 -m mypy src tests`, `ruff check .`, `ruff format --check .` | `src/api` | Passed | `mypy` 0 issues in 221 files; `ruff` clean across 196 formatted files |
| `python3 tools/rpi-checks.py --all` | Repository | Skipped | Explicitly prohibited by caller instructions (focused validation tier selected) |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled — `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01`, `P04`, `P04-T01`, `P04-T02` are all checked (`[x]`) and match phase details and test matrix caps (`14 <= 22`, `3 <= 3`, `3 <= 4`, `2 <= 4`, zero removals).
* Completed-work evidence and handoff prose: Reconciled across plan, phase details, and changes record.
* Validation, blockers, remaining work, and follow-up items: Reconciled — 533 focused tests + `mypy` + `ruff` green, zero active blockers, zero remaining in-scope tasks.
* Review readiness: Ready for `rpi-review`.

## Blockers

* None

## Remaining Work

* None in declared scope (`P01`–`P04` complete).

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/issue-164-chat-eval-revocation-plan.md, `## Follow-Up Items`
* Live/provider-hosted chat evaluation, human participant exercises, measured reviewer timing against the non-AI path, and owner threshold/enablement sign-off remain post-merge owner governance prerequisites under Issue #164 (`state="disabled"`).

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: Full plan (`P01`–`P04`), all markers `[x]`
* Validation coverage: Focused tier passed across `src/core` (180 tests + `mypy` + `ruff`), `src/agents` (118 tests + `mypy` + `ruff`), and `src/api` (235 tests + `mypy` + `ruff`); `tools/rpi-checks.py --all` explicitly skipped per caller directive
* Blockers: None
* Current plan and detail updates: Local pre-redaction `_question_refusal` ordering recorded under `P01-T01`
* Planning and critique state: Ready (`PC-001`–`PC-004` resolved)
* Follow-up items: Owner-gated live evaluation, human exercises, review-time measurement, and threshold approval
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: Parent confirmed automatic RPI Agent
