<!-- markdownlint-disable-file -->
# RPI Changes: Offline RAI Held-Out Evaluation and Tokenomics Candidate Comparison (Issue #108)

## Metadata

* Task ID: issue-108-heldout-eval-tokenomics
* Related plan: .copilot-tracking/plans/2026-11-15/ai-108-heldout-eval-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/ai-108-heldout-eval-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`, `P02`, `P03`, `P04`)
* Completed scope markers: `P01` (`P01-T01`, `P01-T02`), `P02` (`P02-T01`), `P03` (`P03-T01`), `P04` (`P04-T01`, `P04-T02`)
* All remaining active-plan markers: None
* Status basis: All four phases (`P01`–`P04`) have verified source, test, documentation, lint (`ruff check`, `ruff format --check`), and strict typecheck (`mypy`) completion evidence in `src/core` and `src/api`.

## Execution Summary

Delivered the offline RAI Held-Out evaluation harness (`zava_forward.core.heldout_eval`) and Tokenomics candidate/single-lever comparator (`zava_forward.core.tokenomics_comparison`) in `src/core`, exposed manager-only `GET /api/ai/heldout-evaluation`, `POST /api/ai/candidate-comparison`, and `GET /api/ai/report` summaries in `src/api`, documented offline boundaries in `src/core/README.md` and `src/api/README.md`, and verified all unit tests, `ruff check`, `ruff format --check`, and `mypy` across both packages.

## Completed Work

### Core Held-Out Freeze, Prompt/Tuning Isolation, and 11-Capability Evaluator

* Related phase or task: `P01` (`P01-T01`, `P01-T02`)
* Files: `src/core/src/zava_forward/core/heldout_eval.py`, `src/core/pyproject.toml`
* What changed and why: Implemented pre-evaluation freeze validation (`approve_manifest`, `check_heldout_freeze`), prompt/tuning answer and case-ID isolation across all 5 assistant request builders and all 6 legacy prompt templates (`check_prompt_tuning_isolation`), and the 16-case canonical offline held-out evaluation suite (`evaluate_heldout`, `canonical_offline_heldout_suite`) covering all 5 assistants and all 6 retained legacy families across controls, ambiguity, abstention, source integrity, and factual support. Added narrow `disallow_untyped_calls = false` override in `src/core/pyproject.toml`.
* Completion evidence: `tests/test_heldout_eval.py` (12 tests) + `ruff check` + `ruff format --check` + `mypy` passed (`exit code 0`).
* Validation: Passed.

### Core Tokenomics Candidate and Single-Lever Comparator

* Related phase or task: `P02` (`P02-T01`)
* Files: `src/core/src/zava_forward/core/tokenomics_comparison.py`
* What changed and why: Implemented `compare_candidates` (`compare_tokenomics_candidates`) and `canonical_offline_candidate_comparison` (`canonical_offline_tokenomics_comparison`) enforcing single-lever attribution (`model`, `routing`, `caching`, `prompt`), identical held-out case IDs, exact `Decimal` cost accounting, explicit unknown-liability blocking, capacity-only time-released governance, and automatic `outcome='failure'` / `is_saving=False` whenever a cheaper candidate regresses `critical_misses`, `unsupported_claims`, `overrides`, `reopened_cases`, `critical_errors`, or accepted case outcomes.
* Completion evidence: `tests/test_tokenomics_comparison.py` (10 tests) + `ruff check` + `ruff format --check` + `mypy` passed (`exit code 0`).
* Validation: Passed.

### API Endpoints, Report Integration, and Route Inventory

* Related phase or task: `P03` (`P03-T01`)
* Files: `src/api/src/zava_forward/api/server.py`, `src/api/tests/test_role_endpoint_inventory.py`
* What changed and why: Mapped `/api/ai/heldout-evaluation` and `/api/ai/candidate-comparison` to `"ai_report"` in `get_kind(path)`, embedded compact `held_out` and `tokenomics_comparison` summaries inside `GET /api/ai/report`'s `evaluation` block while preserving top-level keys, added side-effect-free manager-only `GET /api/ai/heldout-evaluation` (rejecting query strings via `if url.query:`), added manager-only `POST /api/ai/candidate-comparison` with 4-argument `s.audit` recording and bounded request validation, and registered both endpoints in `test_role_endpoint_inventory.py`.
* Completion evidence: `tests/test_heldout_eval_api.py` (5 tests) and `tests/test_role_endpoint_inventory.py` passed (`exit code 0`).
* Validation: Passed.

### Focused Unit Tests, Documentation, and Verification

* Related phase or task: `P04` (`P04-T01`, `P04-T02`)
* Files: `src/core/tests/test_heldout_eval.py`, `src/core/tests/test_tokenomics_comparison.py`, `src/api/tests/test_heldout_eval_api.py`, `src/api/pyproject.toml`, `src/core/README.md`, `src/api/README.md`
* What changed and why: Added 12 core held-out evaluation tests, 10 core tokenomics comparison tests, and 5 real-HTTP API integration/role-denial tests; added `disallow_untyped_calls = false` override for `test_heldout_eval_api` in `src/api/pyproject.toml`; and documented the offline synthetic scope and live-boundary disclaimers in `src/core/README.md` and `src/api/README.md`.
* Completion evidence: All focused test suites (`42` core tests + `11` doc/cutover tests + `114` API tests), `ruff check`, `ruff format --check`, and `mypy` passed across `src/core` and `src/api` (`exit code 0`).
* Validation: Passed.

## Implementation-Time Plan and Detail Updates

* Local judgment (`P01-T01`): `zava_forward.core.ai_prompts` exposes its 6 legacy prompt templates dictionary as `ai_prompts.PROMPTS` (rather than `TEMPLATES`); `heldout_eval._render_registered_prompt_corpus()` reads `sorted(ai_prompts.PROMPTS)` directly, preserving approved intent without altering plan scope or architecture.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| Core focused unit tests (`test_heldout_eval`, `test_tokenomics_comparison`, `test_dependency_rule`, `test_ai_register_completeness`, `test_rai_threshold_live_approval_guard`) | `src/core` | Passed | 42 tests in 3.392s (`OK`) |
| Core doc-link and cutover-audit tests (`test_live_doc_links`, `test_cutover_audit`) | `src/core` | Passed | 11 tests in 4.797s (`OK`) |
| Core linter & formatter (`ruff check` + `ruff format --check`) | `src/core` | Passed | `All checks passed!`, `285 files already formatted` |
| Core strict typecheck (`mypy`) | `src/core` | Passed | `Success: no issues found in 338 source files` |
| API focused unit tests (`test_heldout_eval_api`, `test_ai_tasks`, `test_eval_candidate_regression_gate`, `test_role_endpoint_inventory`, `test_ai_call_site_inventory`, `test_dependency_rule`) | `src/api` | Passed | 114 tests in 55.823s (`OK`) |
| API consumption ledger integration tests (`test_ai_consumption_api`) | `src/api` | Passed | Verified passing in `src/api` suite |
| API linter & formatter (`ruff check` + `ruff format --check`) | `src/api` | Passed | `All checks passed!`, `197 files already formatted` |
| API strict typecheck (`mypy`) | `src/api` | Passed | `Success: no issues found in 281 source files` |

## Pre-Review Reconciliation

* Plan markers and phase details: Current (`P01`–`P04` checked and aligned)
* Completed-work evidence and handoff prose: Current
* Validation, blockers, remaining work, and follow-up items: Current
* Review readiness: Ready

## Blockers

* None

## Remaining Work

* None (`P01`–`P04` complete in declared full-plan scope).

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/ai-108-heldout-eval-plan.md, `## Follow-Up Items`
* Owner-authorized live Azure OpenAI held-out batch execution and regional quota attestation for Issue #108 — outside offline synthetic scope; owner/operator action on Issue #108.
* Human staff participant effectiveness evaluation and OQ-018 cohort owner sign-off for Issue #108 — outside offline synthetic scope; owner/programme lead action on Issue #108.

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: Full plan (`P01`–`P04`); completed: `P01`, `P02`, `P03`, `P04`; remaining: none
* Validation coverage: Complete across `src/core` and `src/api` (`unittest`, `ruff check`, `ruff format --check`, `mypy`)
* Blockers: None
* Current plan and detail updates: Local judgment noted for `ai_prompts.PROMPTS`; all markers reconciled
* Planning and critique state: Ready (`PC-001` through `PC-006` resolved)
* Follow-up items: Live Azure OpenAI held-out batch + regional quota attestation; human participant + OQ-018 owner sign-off
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: Confirmed automatic RPI Agent parent
