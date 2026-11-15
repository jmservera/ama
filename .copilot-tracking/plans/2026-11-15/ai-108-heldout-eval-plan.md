<!-- markdownlint-disable-file -->
# RPI Plan: Offline RAI Held-Out Evaluation and Tokenomics Candidate Comparison (Issue #108)

## Task Metadata

* Task ID: issue-108-heldout-eval-tokenomics
* Task slug: ai-108-heldout-eval
* Planning status: Ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/ai-108-heldout-eval-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/ai-108-heldout-eval-plan-critique.md

## Executive Summary

This plan delivers the offline Responsible AI (RAI) held-out evaluation harness and Tokenomics candidate/lever comparison contract in `src/core` and `src/api` for Issue #108 (`Refs #108`). Currently, `src/agents` contains partial single-task freeze and candidate-comparison helpers that `src/core` cannot import under package dependency rules and that explicitly omit the five core proposal-only assistants. Implementing pure, stdlib-only evaluation and comparison modules in `zava_forward.core` and exposing them on manager-only `zava_forward.api` endpoints establishes one verifiable, provider-free offline gate across all 11 retained AI capabilities (five assistants and six retained legacy task families).

### User Decisions and Requirements Highlights

* **Target packages and branch**: Implement in `src/core` and `src/api` on `feat/ai-108-heldout-eval-0228` (targeting `feat/demo-164-chat-grounding-provenance-0900`, PR #1641), commit locally with `Refs #108` and the Copilot trailer, and do not push.
* **Pre-evaluation freeze and leakage prevention**: Freeze task, model, prompt, policy, and source versions, an independently labelled held-out split, expected outcomes, critical error rules, cohorts with sufficient samples, and full-manifest + threshold digest-bound named-human approved thresholds before scoring; verify held-out case IDs and `>= 6`-word `expected_answer` prose never enter rendered prompts or tuning inputs.
* **Eleven-capability offline evaluation and honest reporting**: Cover all five assistants and all six retained legacy families across controls, ambiguity, abstention, source integrity, and factual support; report critical errors/misses, usable coverage, unaveraged subgroup results (carrying `cohort_eval.SYNTHETIC_NON_FAIRNESS_NOTICE`), hashes, split/seed, denominators, actual serving version, usage, unknown liabilities, reviewer protocol, `pass`/`fail`/`insufficient` outcomes, structured `baseline_candidate` payload, and explicit `not_applicable` calibration status when meaningful scored probability predictions are absent.
* **Tokenomics candidate and single-lever discipline**: Fail any cheaper candidate that raises critical misses, unsupported claims, overrides, or reopened cases, carries `unknown_liabilities > 0`, or mismatches serving versions on the same held-out cases (`is_saving=False`), and verify actual `lever_config` diffs so any routing, caching, model, or prompt option changes exactly one lever at a time against the same held-out cases and a recorded baseline.

### What You May Not Know

* **AST and `get_kind(path)` gates in `src/core` and `src/api`**: `src/core/tests/test_dependency_rule.py` forbids `core` from importing `agents` or `api`; `src/api/tests/test_ai_call_site_inventory.py` forbids unclassified provider URL fragments or OpenAI/Azure AI SDK imports anywhere under `src/*/src/**/*.py`; `server.py:get_kind(path)` gates `projection.allowed(u, get_kind(url.path))` before route dispatch; and `src/api/tests/test_role_endpoint_inventory.py` requires every `/api/...` route in `server.py` to appear in the role-matrix endpoint inventory.
* **Offline synthetic boundary**: Constructed offline fixtures prove harness gates, controls, subgroup sufficiency checks, and regression rejection (`Refs #108`), not live Azure OpenAI accuracy, regional quota availability, or human staff participant effectiveness (`live_release_authorized=False`).

### Unresolved Decisions or Blockers

* None for the scoped offline `src/core` and `src/api` deliverables. Live Azure OpenAI held-out batch execution and human participant evaluation remain tracked on Issue #108 outside this offline slice.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop (`research`, `plan`, `critique`, `implement`, `review`) in `/home/azureuser/source/ama-demo-wt/feat-108-heldout-eval` on branch `feat/ai-108-heldout-eval-0228` targeting `feat/demo-164-chat-grounding-provenance-0900` (`PR #1641`) for Issue #108 (`AI evaluation harness and model selection`).
* Deliver offline RAI Held-Out and Tokenomics comparison criteria in `src/core` and `src/api` without adding a separate governance service (caller prompt; `docs/prds/zava-forward-retrofit-programme-demonstrator.md`).
* Freeze task/model/prompt/policy/source versions, an independently labelled held-out split, expected outcomes, critical errors, cohorts, sufficient samples, and approved thresholds before evaluation, and ensure held-out answers never enter prompts or tuning (Criterion 1).
* Cover all five assistants (`stock-prioritisation`, `assessment-preparation`, `funding-evidence`, `works-resident-coordination`, `quality-evidence`) and each retained legacy family (`briefing`, `message`, `summary`, `priority`, `funding_draft`, `read_document`), testing correct controls, ambiguity, abstention, source integrity, and factual support; record critical errors/misses, usable coverage, subgroup results, hashes, split/seed, denominators, actual serving version, usage, unknown liabilities, reviewer protocol, `pass`/`fail`/`insufficient` outcomes, and document calibration as not applicable when meaningful scored predictions are absent (Criterion 2; `src/core/src/zava_forward/core/ai_registry.py`).
* Ensure Tokenomics candidate comparison reports a cheaper candidate that raises critical misses, unsupported claims, overrides, or reopened cases on the same held-out cases as a failure (not a saving), and ensure any routing or caching option evaluated changes one lever at a time against the same held-out cases and recorded baseline (Criterion 3; `docs/reference/resources/ai-tokenomics.md`).
* Write dated RPI artifacts under `.copilot-tracking/` (`research`, `plans`, `details`, `reviews/plans`, `changes`, `reviews`), run focused tests in `src/core` and `src/api` plus `ruff check`, `ruff format --check`, and `mypy`, and commit locally with `Refs #108` and the Copilot `Co-authored-by` trailer without pushing, leaving `git status --short` empty (caller prompt).

## Goals

* Provide a pure, deterministic `zava_forward.core` held-out freeze validator, prompt/tuning answer-leakage guard, and offline held-out evaluation suite covering all five assistants and all six retained legacy task families.
* Provide a pure, exact-decimal `zava_forward.core` Tokenomics candidate and single-lever (`model`, `routing`, `caching`, `prompt`) comparator bound to frozen held-out manifests and recorded baselines.
* Expose manager-only read and comparison surfaces in `zava_forward.api` (`GET /api/ai/heldout-evaluation`, `POST /api/ai/candidate-comparison`, and `GET /api/ai/report` summary fields) while preserving all existing API, role-matrix, call-site, and dependency invariants.

## Scope and Non-Goals

### In Scope

* New `src/core/src/zava_forward/core/heldout_eval.py` and `src/core/src/zava_forward/core/tokenomics_comparison.py` modules with typing boundary overrides in `src/core/pyproject.toml` and `src/api/pyproject.toml`.
* Manager-only HTTP wiring in `src/api/src/zava_forward/api/server.py` (`get_kind(path)`, `do_GET`, `do_POST`) and route registration in `src/api/tests/test_role_endpoint_inventory.py`.
* Focused unit tests in `src/core/tests/` (`test_heldout_eval.py`, `test_tokenomics_comparison.py`) and `src/api/tests/` (`test_heldout_eval_api.py`), plus `src/core/README.md` and `src/api/README.md` updates.

### Non-Goals

* Making live Azure OpenAI network calls, provisioning cloud infrastructure, or claiming regional quota or human-participant sign-off (`Closes #108` is out of scope; use `Refs #108`).
* Modifying or breaking `src/agents` modules (`heldout_freeze.py`, `candidate_comparison.py`) relied upon by existing `agents` and `api` tests.
* Adding a standalone governance service or pushing commits to `origin`.

## Functional Requirements

* **FR-1 (Pre-evaluation freeze & prompt/tuning answer isolation)**: Validate before any scoring that the manifest freezes `task`, `model`, `prompt`, `policy`, and `source` versions, records a deduplicated `held_out` split with deterministic `seed`, denominator, categorical `expected_outcome` plus `>= 6`-word `expected_answer` prose, critical error rules, independent named-human `labelled_by` != `prompt_author`, cohort `min_n` floors, and `threshold_approval` bound to both `thresholds_digest` and full `manifest_digest` (with ISO-8601 `approved_at`, named-human approver validation, and `synthetic=True` blocked when `live=True`), and verifies neither held-out `case_ids` nor `>= 6`-word `expected_answer` prose (exact substring or 6-word shingle overlap) enters rendered system/user prompts or tuning inputs.
  * Observable acceptance criteria: Missing/altered freeze fields, post-approval edits to either `thresholds` or `versions`/`held_out`/`cohorts`, non-independent or agent-attributed labellers/approvers, invalid ISO dates, `synthetic=True` with `live=True`, under-sampled cohorts, or leaked held-out case IDs/`expected_answer` prose into rendered prompts or tuning examples yield `frozen=False` and `outcome="insufficient"` (never `pass`).
* **FR-2 (11-capability offline evaluation & behavioral controls)**: Deterministically evaluate held-out cases across all five assistants (`stock-prioritisation`, `assessment-preparation`, `funding-evidence`, `works-resident-coordination`, `quality-evidence`) and all six retained legacy families (`briefing`, `message`, `summary`, `priority`, `funding_draft`, `read_document`), exercising correct controls, ambiguity handling, abstention, source integrity, and factual support through core validators.
  * Observable acceptance criteria: Canonical offline suite covers all 11 capabilities and all 5 behavioral dimensions; injected control violations, silent ambiguity guessing, failed abstention on missing/unconsented inputs, tampered source hashes/citations, or unsupported claims increment `critical_errors`/`critical_misses` and force `outcome="fail"`.
* **FR-3 (Comprehensive RAI & operational reporting)**: Emit structured evaluation reports containing `critical_errors`, `critical_misses`, `usable_coverage`, unaveraged `subgroup_results` (with `cohort_eval.SYNTHETIC_NON_FAIRNESS_NOTICE`), `hashes`, `split`, `seed`, `denominators`, `actual_serving_version` (including serving-model mismatch detection), `usage`, `unknown_liabilities` (keeping missing/unpriced usage explicit rather than zero), `reviewer_protocol`, `outcome` (`pass` / `fail` / `insufficient`), structured `baseline_candidate` summary for default Tokenomics comparisons, and `calibration` documented as `not_applicable` when meaningful scored probability predictions are absent.
  * Observable acceptance criteria: Every listed report key is populated with exact denominators and SHA-256 hashes; `calibration["status"] == "not_applicable"` when scored probability predictions are absent; missing usage or unpriced calls surface in `unknown_liabilities` with `"Unknown"` cost.
* **FR-4 (Tokenomics regression failure & single-lever comparison)**: Compare candidate runs against a recorded baseline on the exact same frozen held-out cases using `Decimal` arithmetic; verify actual `lever_config` (`{model, routing, caching, prompt}`) diffs match a single changed lever (matching optional declared `lever` and `changed_levers`); mark any cheaper candidate that increases `critical_misses`, `unsupported_claims`, `overrides`, or `reopened_cases` (or loses baseline-accepted proposals, adds critical errors, mismatches `actual_serving_version`, has non-`pass` status, or carries `unknown_liabilities > 0` / missing usage / `"Unknown"` cost) as `outcome="failure"` and `is_saving=False` (`cost_saving="Unknown"` when liabilities are unresolved).
  * Observable acceptance criteria: Lower-cost candidates with +1 `critical_misses`, `unsupported_claims`, `overrides`, or `reopened_cases`, or with `unknown_liabilities > 0` or serving-version mismatch, return `outcome="failure"` and `is_saving=False`; disguised multi-lever config changes (even if submitted with a single `lever` label) or mismatched held-out case sets return `single_lever_valid=False`, `outcome="failure"`, and `is_saving=False`.
* **FR-5 (Manager-only API endpoints and report summary)**: Expose side-effect-free `GET /api/ai/heldout-evaluation` (rejecting any non-empty `url.query` with 400) and `POST /api/ai/candidate-comparison` (reading `do_POST`'s pre-parsed `body` dict, optionally defaulting omitted `baseline` to `canonical_offline_heldout_suite()["baseline_candidate"]`, and auditing with 4-arg `s.audit(u["email"], "ai_candidate_comparison", "-", ...)`) restricted to `MANAGER_ROLES`, map both paths to `"ai_report"` in `get_kind(path)`, include compact `held_out` and `tokenomics_comparison` summaries under `GET /api/ai/report` `evaluation`, and register new routes in `test_role_endpoint_inventory.py` (including `test_contractor_audit_view_and_export_are_denied`).
  * Observable acceptance criteria: Managers receive HTTP 200 deterministic JSON on both endpoints and in `/api/ai/report`; non-managers and contractors receive HTTP 403; blank or non-empty query strings (`?foo=`) on `GET /api/ai/heldout-evaluation` and malformed body payloads on `POST /api/ai/candidate-comparison` return HTTP 400; `test_role_endpoint_inventory.py` and `test_ai_tasks.py` pass across all roles.

## Non-Functional Requirements

* **NFR-1 (Package dependency & call-site purity)**
  * Objective threshold or evaluation condition: Zero forbidden imports in `src/core` (`ALLOWED = {"core"}`) and zero new provider call sites in `src/*/src/**/*.py`.
  * Operating condition or verification approach, if needed: Verified via `src/core/tests/test_dependency_rule.py`, `src/api/tests/test_dependency_rule.py`, and `src/api/tests/test_ai_call_site_inventory.py`.
  * Observable acceptance criteria: All three AST gate tests pass with zero modifications to `INVENTORY`.
* **NFR-2 (Determinism, exact-decimal money math, and strict static checks)**
  * Objective threshold or evaluation condition: Identical SHA-256 report digests across repeated offline runs, `Decimal`-only currency calculations, and zero `ruff check`, `ruff format --check`, or `mypy` errors across `src/core` and `src/api`.
  * Operating condition or verification approach, if needed: Run `ruff check`, `ruff format --check`, `mypy`, and targeted `unittest` suites in an isolated worktree environment without dirtying tracked files.
  * Observable acceptance criteria: All linters, type checks, and focused test suites exit 0, and `git status --short` is empty after commit.

## Acceptance Criteria

* [ ] `zava_forward.core.heldout_eval` enforces pre-evaluation freeze (versions, independent labeller, seed, expected outcomes, critical errors, cohort sample floors, approved threshold digest) and blocks held-out case IDs and held-out expected answers from entering rendered prompts or tuning inputs before scoring.
* [ ] `zava_forward.core.heldout_eval` deterministically evaluates all 5 assistants and all 6 retained legacy task families across controls, ambiguity, abstention, source integrity, and factual support, recording critical errors/misses, usable coverage, unaveraged subgroup results, hashes, split/seed, denominators, actual serving version, usage, unknown liabilities, reviewer protocol, `pass`/`fail`/`insufficient` outcomes, and `calibration.status == "not_applicable"` when scored probability predictions are absent.
* [ ] `zava_forward.core.tokenomics_comparison` reports any cheaper candidate raising `critical_misses`, `unsupported_claims`, `overrides`, or `reopened_cases` on the same held-out cases as `outcome="failure"` (`is_saving=False`), and rejects any routing/caching/model/prompt option that changes zero or multiple levers, lacks a recorded baseline, or alters the held-out case set.
* [ ] `zava_forward.api.server` exposes manager-only `GET /api/ai/heldout-evaluation` and `POST /api/ai/candidate-comparison`, surfaces held-out/tokenomics status in `GET /api/ai/report`, and passes `test_role_endpoint_inventory.py` and `test_ai_call_site_inventory.py`.
* [ ] Test plan governance locked: exact test removals = `none`; maximum new test files = 3 (`src/core/tests/test_heldout_eval.py`, `src/core/tests/test_tokenomics_comparison.py`, `src/api/tests/test_heldout_eval_api.py`, <= 45 focused semantic + boundary test methods total) plus route-list additions in `src/api/tests/test_role_endpoint_inventory.py`; `src/core/README.md` and `src/api/README.md` updated; `ruff check`, `ruff format --check`, `mypy`, and focused tests pass; committed locally with `Refs #108` and Copilot trailer (`git status --short` empty, not pushed).

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/ai-108-heldout-eval-plan.md                                                                           |
| Phase details                    | .copilot-tracking/details/2026-11-15/ai-108-heldout-eval-phase-details.md                                                                |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/ai-108-heldout-eval-plan-critique.md with Revise verdict resolved via PC-001 through PC-006 direct corrections |
| Relevant research                | .copilot-tracking/research/2026-11-15/ai-108-heldout-eval-research.md                                                                    |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/ai-108-heldout-eval-changes.md is created or continued by implementation as its evidence record     |
| Planning execution and readiness | Complete; implementation-ready after resolving PC-001 through PC-006                                                                     |
| Continuation context             | Automatic RPI Agent parent return; transitions immediately to Implement                                                                  |

## Sources

* `.copilot-tracking/research/2026-11-15/ai-108-heldout-eval-research.md`: Evidence log `C1`–`C18`, dependency rules, 11-capability inventory, and option selection.
* `docs/prds/zava-forward-retrofit-programme-demonstrator.md`: Issue #108 RAI held-out evaluation, subgroup reporting, calibration-NA, and Tokenomics acceptance criteria.
* `docs/reference/resources/ai-tokenomics.md`: Single-lever routing/caching discipline, cost per accepted proposal, and quality-gated failure semantics.
* `src/core/src/zava_forward/core/{ai_registry,assistants,ai_tasks,ai_prompts,cohort_eval,ai_consumption}.py`: Canonical task definitions, prompt builders, citation/control validators, subgroup approval helpers, and exact-decimal consumption primitives.
* `src/api/src/zava_forward/api/server.py` and `src/api/tests/{test_role_endpoint_inventory,test_ai_call_site_inventory,test_eval_candidate_regression_gate}.py`: HTTP server conventions and AST/role-matrix regression gates.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Core Held-Out Freeze, Prompt/Tuning Isolation, and 11-Capability Offline Evaluator

* Intent: Deliver `zava_forward.core.heldout_eval` enforcing pre-evaluation freeze, prompt/tuning answer-leakage prevention, and deterministic offline evaluation across all 5 assistants and all 6 retained legacy families.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Implement `src/core/src/zava_forward/core/heldout_eval.py`

* Requirement and evidence: FR-1, FR-2, FR-3, NFR-1, NFR-2 (`C1`, `C5`, `C7`, `C8`, `C10`–`C13`, `C15`, `C17`)
* Expected result: Pure `core` module providing `check_heldout_freeze`, `check_prompt_tuning_isolation`, `evaluate_heldout_suite`, and `canonical_offline_heldout_suite` covering all 5 assistants + 6 legacy families, all 5 control/grounding dimensions, and all required report fields including `calibration.status == "not_applicable"`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/ai-108-heldout-eval-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Configure `src/core/pyproject.toml` typing boundary for `heldout_eval` and tests

* Requirement and evidence: NFR-2 (`src/core/pyproject.toml`)
* Expected result: `mypy` runs cleanly in strict mode across `src/core`, using a narrow `disallow_untyped_calls = false` override only where typed `heldout_eval` or its tests invoke legacy untyped `core` modules (`assistants`, `ai_registry`, `ai_tasks`, `store`).
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/ai-108-heldout-eval-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Core Tokenomics Candidate and Single-Lever Comparator

* Intent: Deliver `zava_forward.core.tokenomics_comparison` enforcing quality-gated candidate comparison and single-lever (`model`, `routing`, `caching`, `prompt`) isolation against a recorded baseline on the same frozen held-out cases.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Implement `src/core/src/zava_forward/core/tokenomics_comparison.py`

* Requirement and evidence: FR-4, NFR-1, NFR-2 (`C1`, `C3`, `C4`, `C9`, `C15`)
* Expected result: Pure `core` module providing `compare_tokenomics_candidates` and `canonical_offline_tokenomics_comparison` that fail cheaper candidates raising `critical_misses`, `unsupported_claims`, `overrides`, or `reopened_cases` (`is_saving=False`) and enforce changing one lever at a time against the recorded baseline and identical frozen held-out cases.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/ai-108-heldout-eval-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: API Endpoints, Report Integration, and Route Inventory

* Intent: Expose the `core` held-out evaluation and Tokenomics comparator on manager-only HTTP endpoints and in `GET /api/ai/report` while preserving role-matrix and call-site gates.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Wire `GET /api/ai/heldout-evaluation`, `POST /api/ai/candidate-comparison`, and `GET /api/ai/report` in `src/api`

* Requirement and evidence: FR-5, NFR-1 (`C2`, `C14`, `C17`, `C18`)
* Expected result: Manager-only endpoints added to `src/api/src/zava_forward/api/server.py`, mapped to `"ai_report"` in `get_kind(path)`, summarized in `GET /api/ai/report`, and registered in `src/api/tests/test_role_endpoint_inventory.py`.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/ai-108-heldout-eval-phase-details.md

<!-- rpi:phase id=P04 -->
### [x] P04: Focused Unit Tests, Documentation, and Verification

* Intent: Prove semantic and boundary behavior in `src/core` and `src/api`, document honest offline boundaries in component READMEs, pass all linters/typechecks/tests, and prepare for post-implementation Review and clean local commit.
* Dependencies: P01, P02, P03

<!-- rpi:task id=P04-T01 -->
#### [x] P04-T01: Author `src/core/tests/test_heldout_eval.py` and `src/core/tests/test_tokenomics_comparison.py`

* Requirement and evidence: FR-1, FR-2, FR-3, FR-4, NFR-1, NFR-2 (`C1`–`C15`)
* Expected result: Focused semantic and negative-case unit tests in `src/core/tests/` verifying freeze failures, prompt/tuning answer leakage rejection, all 11 capabilities across all 5 dimensions, subgroup/hash/denominator/serving-version/liability/calibration-NA reporting, cheaper-candidate quality regressions (`critical_misses`, `unsupported_claims`, `overrides`, `reopened_cases`), and single-lever routing/caching rules.
* Detail section: P04-T01 in .copilot-tracking/details/2026-11-15/ai-108-heldout-eval-phase-details.md

<!-- rpi:task id=P04-T02 -->
#### [x] P04-T02: Author `src/api/tests/test_heldout_eval_api.py` and update README documentation

* Requirement and evidence: FR-5, NFR-1, NFR-2 (`C14`, `C16`–`C18`, `src/core/README.md`, `src/api/README.md`)
* Expected result: HTTP integration and role-denial tests in `src/api/tests/test_heldout_eval_api.py`, concise documentation sections in `src/core/README.md` and `src/api/README.md`, and green execution of `unittest`, `ruff check`, `ruff format --check`, and `mypy` across `src/core` and `src/api`.
* Detail section: P04-T02 in .copilot-tracking/details/2026-11-15/ai-108-heldout-eval-phase-details.md

## Dependencies

* `zava_forward.core.ai_registry`, `assistants`, `ai_tasks`, `ai_prompts`, `cohort_eval`, `ai_consumption`, and `store`: Existing core contracts that `heldout_eval` and `tokenomics_comparison` exercise directly without duplicating rule definitions.
* Worktree-isolated Python environment (`.venv` gitignored under `.gitignore`): Prevents interfering with sibling worktrees sharing user site-packages while running editable `zava-forward-core`, `zava-forward-agents`, and `zava-forward-api` validation.

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| `PC-001` [Critical]: `server.py` `get_kind(path)`, `u`, pre-parsed `body`, `if url.query:`, and 4-arg `s.audit` contract | Resolved | Updated FR-5 and P03-T01 to map both new paths to `"ai_report"` in `get_kind(path)`, use `u` and pre-parsed `body` in `do_POST`, check `if url.query:` on `GET /api/ai/heldout-evaluation`, keep GET side-effect-free, use 4-arg `s.audit(u["email"], "ai_candidate_comparison", "-", ...)` on POST, and include `/api/ai/heldout-evaluation` in `test_contractor_audit_view_and_export_are_denied`. |
| `PC-002` [Critical]: `cohort_eval.SYNTHETIC_NON_FAIRNESS_NOTICE` constant name | Resolved | Updated FR-3 and P01-T01 to use `cohort_eval.SYNTHETIC_NON_FAIRNESS_NOTICE` (replacing non-existent `NON_FAIRNESS_PROVENANCE_NOTICE`). |
| `PC-003` [High]: Full `manifest_digest` binding, named-human approver, ISO `approved_at`, and `live=True` synthetic rejection | Resolved | Updated FR-1, P01-T01, and P04-T01 so `approve_manifest` / `threshold_approval` binds both `thresholds_digest` and full `manifest_digest` (manifest excluding `threshold_approval`), validates named-human approvers and ISO-8601 `approved_at`, rejects `synthetic=True` when `live=True`, and tests post-approval tampering of both `thresholds` and `versions`/`held_out`/`cohorts`. |
| `PC-004` [High]: Actual `lever_config` diff check, `unknown_liabilities` / serving-version fail-closed economics, and `baseline_candidate` payload | Resolved | Updated FR-3, FR-4, P01-T01, P02-T01, and P03-T01 so `compare_tokenomics_candidates` diffs actual `lever_config` keys (`model`, `routing`, `caching`, `prompt`) against `declared_lever`, forces `outcome="failure"` / `is_saving=False` / `cost_saving="Unknown"` when `unknown_liabilities > 0`, usage is missing, status != `"pass"`, or serving versions mismatch, and emits `baseline_candidate` from `canonical_offline_heldout_suite()` for default POST comparisons. |
| `PC-005` [Medium]: Separate categorical `expected_outcome` from `>= 6`-word `expected_answer` prose and pass task-specific kwargs to `ai_prompts.render` | Resolved | Updated FR-1 and P01-T01 so shingle/substring isolation inspects `>= 6`-word `expected_answer` prose and `case_id`s (never short categorical enum labels) and renders all 6 `ai_prompts.TEMPLATES` with task-specific synthetic non-held-out kwargs + `ai_tasks.cite_instruction(...)` alongside all 5 `assistants.build_request(...)` payloads. |
| `PC-006` [Low]: Include `src/api/pyproject.toml` in Plan `In Scope` and `test_ai_tasks` + `test_eval_candidate_regression_gate` in `P04-T02` | Resolved | Added `src/api/pyproject.toml` to Plan `In Scope` and added `test_ai_tasks.py` + `test_eval_candidate_regression_gate.py` to `P04-T02` validation commands. |

## Follow-Up Items

* Owner-authorized live Azure OpenAI held-out batch execution and regional quota attestation for Issue #108 — outside offline synthetic scope because live model calls require explicit spend authorization and deployed endpoints; owner/operator action on Issue #108.
* Human staff participant effectiveness evaluation and OQ-018 cohort owner sign-off for Issue #108 — outside offline synthetic scope because scripted harnesses and role agents cannot substitute for named human participants or DPO/RAI owner approvals; owner/programme lead action on Issue #108.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/ai-108-heldout-eval-changes.md
* Ready phase or task: All planned phases (`P01`–`P04`) completed and reconciled for `rpi-review`
* Remaining provisional question or blocker: None
