<!-- markdownlint-disable-file -->
# RPI Plan: Issue #108 Cycle 1 Independent Review Fixes and Parent Rebase

## Task Metadata

* Task ID: issue-108-heldout-eval-c1
* Task slug: ai-108-heldout-eval-c1
* Planning status: Implementation-ready (single-pass critique resolved)
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/ai-108-heldout-eval-c1-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/ai-108-heldout-eval-c1-plan-critique.md

## Executive Summary

This Cycle 1 (`c1`) plan resolves all five findings from the independent exact-head functional code review of `18dc9d132` and rebases `feat/ai-108-heldout-eval-0228` onto the latest stacked parent commit `7f83f4749` (`origin/feat/demo-164-chat-grounding-provenance-0900`). Together, these updates restore content-standard conformance (`test_content_standard.py`), replace dynamic runtime manifest signing with pinned `HELDOUT-FREEZE-2026-10-15` digests and live capability-version drift detection, eliminate candidate manifest re-signing, close summary-only candidate comparison bypasses in `tokenomics_comparison.py`, detect ungrounded numbers and `ZF-*` identifiers in candidate statements, and prevent per-case scoring when cohort or total sample floors are unmet.

### User Decisions and Requirements Highlights

* **Parent rebase and local commit boundary**: Rebase `feat/ai-108-heldout-eval-0228` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`7f83f4749`), validate at the Focused tier (no Docker/full gate), commit code + `c1` `.copilot-tracking/` artifacts with the Copilot trailer, leave `git status --short` empty, and do not push.
* **Content-standard conformance (`Critical`)**: Replace `"human-approved"` with `"human-authorized"` in `src/core/src/zava_forward/core/heldout_eval.py` and `src/core/README.md` so `CopyAudit.test_ai_label_is_exact_and_never_implies_approval` passes.
* **Pinned frozen manifest digests & capability-version drift (`High`)**: Pin `FROZEN_THRESHOLDS_DIGEST` and `FROZEN_MANIFEST_DIGEST` as module constants for `HELDOUT-FREEZE-2026-10-15` in `heldout_eval.py`, detect live `_capability_version_snapshot()` drift as `"capability_version_drift"` in `check_heldout_freeze()`, and remove dynamic manifest mutation/re-signing from `tokenomics_comparison.py` via an explicit `expected_serving_model` check in `evaluate_heldout()`.
* **Summary-only Tokenomics hardening (`High`)**: Require `responses` OR explicit verified `evaluation_outcome`, `accepted_case_ids`, and `gate_failures` (never defaulting missing `evaluation_outcome` to `"pass"` or `accepted_case_ids` to `case_ids`), enforce `candidate_usage.currency == baseline_usage.currency`, verify `baseline.get("manifest_digest") == freeze["manifest_digest"]` in `_validate_baseline_artifact`, and pass candidate `lever_config.get("prompt")` values through `check_prompt_tuning_isolation()` so leaked held-out case IDs or answer shingles fail `holdout_leakage_clear`.
* **Statement factual-support & sample-floor pre-gate (`Medium` & `Low`)**: Flag ungrounded numbers (`\b\d+\b`) and `ZF-*` identifiers in `_check_statement_support()` as `unsupported_claims`, and gate per-case scoring in `evaluate_heldout()` on `freeze["ready_for_evaluation"]`.

### What You May Not Know

* **Parent commit `7f83f4749` adds `chat_evaluation` to `GET /api/ai/report`**: Rebasing onto `origin/feat/demo-164-chat-grounding-provenance-0900` merges `GET /api/ai/report` in `src/api/src/zava_forward/api/server.py`, adding top-level `"chat_evaluation"` alongside `"evaluation"`, `"live"`, `"registry"`, and `"consumption"`. Both `src/api/tests/test_heldout_eval_api.py` and `src/api/README.md` must reflect the 5-key top-level payload so `test_ai_consumption_api.py` and `test_heldout_eval_api.py` agree.
* **Digit-boundary nuance on canonical fixtures**: Canonical assistant case `HO-AST-AP-01` cites `"PAS 2035"` while its fixture stores `"pas2035-v2"`, `HO-AST-QE-02` cites `"08:00Z"` from `"2026-10-25T08:00:00Z"`, and legacy `HO-LEG-FD-01` references UK retrofit standard `"PAS 2035"`. Extracting grounded digit runs via `re.findall(r"\d+", grounded_source)` and excluding the fixed regulatory standard title `PAS 2035` prevents false positives on canonical responses while catching any ungrounded numeric claim or foreign `ZF-*` case identifier.

### Unresolved Decisions or Blockers

* None. All five findings and the parent rebase merge have deterministic repository evidence.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop for Cycle 1 (`c1`) of Issue #108 on branch `feat/ai-108-heldout-eval-0228` in `/home/azureuser/source/ama-demo-wt/feat-108-heldout-eval`, writing dated `c1` artifacts under `.copilot-tracking/` (`research`, `plans`, `details`, `changes`, `reviews`).
* Rebase onto latest parent branch via `git fetch origin && git rebase origin/feat/demo-164-chat-grounding-provenance-0900`.
* Resolve Finding 1 (`Critical`): Replace `"human-approved"` with `"human-authorized"` or `"person-reviewed"` in `src/core/src/zava_forward/core/heldout_eval.py` (lines 4 and 1397) and `src/core/README.md` (line 15) so `src/api/tests/test_content_standard.py` passes.
* Resolve Finding 2 (`High`): Pin `FROZEN_THRESHOLDS_DIGEST` and `FROZEN_MANIFEST_DIGEST` as module constants for `HELDOUT-FREEZE-2026-10-15` in `heldout_eval.py` rather than calling `approve_manifest(...)` dynamically on live `_capability_version_snapshot()` at runtime; compare `manifest.get("capability_versions")` against live `_capability_version_snapshot()` in `check_heldout_freeze()` and append `"capability_version_drift"` (with drifted keys) to `blockers` when prompt/policy/task versions differ without an explicit re-freeze; do not mutate `versions["model"]` and re-sign the manifest inside `tokenomics_comparison.py`, instead allowing `evaluate_heldout` to accept an explicit candidate model check while keeping the frozen manifest digest immutable.
* Resolve Finding 3 (`High`): In `tokenomics_comparison.py`, require `responses` OR explicit verified `evaluation_outcome`, `accepted_case_ids`, and `gate_failures` (never defaulting missing `evaluation_outcome` to `"pass"` or missing `accepted_case_ids` to all `case_ids`); enforce `candidate_usage.currency == baseline_usage.currency` (recording a gate failure / `ValueError` on currency mismatch); verify `baseline.get("manifest_digest") == freeze["manifest_digest"]` in `_validate_baseline_artifact`; and pass candidate `lever_config.get("prompt")` values through `check_prompt_tuning_isolation()` so held-out case IDs or fingerprints in candidate prompt overrides fail `holdout_leakage_clear`.
* Resolve Findings 4 & 5 (`Medium` & `Low`): In `_check_statement_support`, flag numbers (`\b\d+\b`) or `ZF-*` identifiers in a statement that do not appear in the case's grounded source labels/facts as `unsupported_claims`; in `evaluate_heldout()`, gate per-case scoring on `freeze["ready_for_evaluation"]`.
* Validate locally at the Focused tier (`unittest` across `test_content_standard.py`, `test_heldout_eval.py`, `test_tokenomics_comparison.py`, `test_heldout_eval_api.py`, `test_role_endpoint_inventory.py`; `mypy`, `ruff check`, `ruff format --check` in `src/core` and `src/api`; `python3 tools/rename-zava-tests.py`), commit all code + `c1` tracking artifacts with the Copilot trailer, leave `git status --short` empty, and do not push.

## Goals

* Rebase `feat/ai-108-heldout-eval-0228` cleanly onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`7f83f4749`) while preserving both `chat_evaluation` and `evaluation.{held_out,tokenomics_comparison}` on `GET /api/ai/report`.
* Enforce content-standard compliance, immutable frozen manifest digests (`HELDOUT-FREEZE-2026-10-15`), live capability-version drift blocking, statement-level numeric/`ZF-*` factual-support verification, and sample-sufficiency pre-gating in `zava_forward.core.heldout_eval`.
* Close all summary-only candidate comparison bypasses, currency mismatches, unbound baseline manifest digests, and candidate prompt-lever leakage gaps in `zava_forward.core.tokenomics_comparison`.

## Scope and Non-Goals

### In Scope

* Rebasing `feat/ai-108-heldout-eval-0228` onto `origin/feat/demo-164-chat-grounding-provenance-0900` and merging `src/api/src/zava_forward/api/server.py`, `src/api/tests/test_heldout_eval_api.py`, and `src/api/README.md`.
* Updating `src/core/src/zava_forward/core/heldout_eval.py`, `src/core/src/zava_forward/core/tokenomics_comparison.py`, and `src/core/README.md` to fix Findings 1–5.
* Updating summary-candidate fixtures and adding focused regression tests in `src/core/tests/test_heldout_eval.py`, `src/core/tests/test_tokenomics_comparison.py`, and `src/api/tests/test_heldout_eval_api.py`.

### Non-Goals

* Docker image builds, browser harness execution, or complete external local gate runs (Focused validation tier explicitly directed).
* Live Azure OpenAI calls, regional quota attestation, human participant studies, or pushing to `origin`.

## Functional Requirements

* **FR-1 (Clean parent rebase & `GET /api/ai/report` alignment)**: Rebase onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`7f83f4749`) so `GET /api/ai/report` returns `{"evaluation", "chat_evaluation", "live", "registry", "consumption"}` with `evaluation["held_out"]` and `evaluation["tokenomics_comparison"]` intact.
  * Observable acceptance criteria: `git merge-base --is-ancestor origin/feat/demo-164-chat-grounding-provenance-0900 HEAD` exits 0; `test_heldout_eval_api.py` and `test_ai_consumption_api.py` agree on the 5 top-level keys of `GET /api/ai/report`.
* **FR-2 (Content-standard compliance)**: Eliminate unattributed `"human-approved"` phrasing in `heldout_eval.py` and `src/core/README.md` in favor of `"human-authorized"`.
  * Observable acceptance criteria: `src/api/tests/test_content_standard.py` passes completely.
* **FR-3 (Pinned freeze digests, live drift check, & immutable model evaluation)**: Pin `CANONICAL_FREEZE_ID = "HELDOUT-FREEZE-2026-10-15"`, `FROZEN_THRESHOLDS_DIGEST`, and `FROZEN_MANIFEST_DIGEST` as static constants in `heldout_eval.py` using static frozen version maps in `canonical_heldout_manifest()` (without runtime `approve_manifest(...)` calls); compare `manifest.get("capability_versions")` against live `_capability_version_snapshot()` in `check_heldout_freeze()` and append both `"capability_version_drift"` and `"capability_version_drift:<keys>"` (plus `drifted_capability_versions` metadata) to `blockers` when prompt, policy, task, model, or source versions drift without re-freezing; accept `expected_serving_model: str | None = None` in `evaluate_heldout()` and remove `_manifest_for_candidate_model()` from `tokenomics_comparison.py`.
  * Observable acceptance criteria: `canonical_heldout_manifest()["threshold_approval"]` matches `FROZEN_THRESHOLDS_DIGEST` and `FROZEN_MANIFEST_DIGEST`; mutating a live prompt/policy/task version causes `check_heldout_freeze()` to emit `"capability_version_drift"` and `"capability_version_drift:..."` in `blockers` and `evaluate_heldout()` to fail; model-lever candidate comparisons verify serving model match while keeping `manifest_digest == FROZEN_MANIFEST_DIGEST`.
* **FR-4 (Summary-only candidate verification, currency parity, baseline digest binding, & prompt-lever isolation)**: In `tokenomics_comparison.py`: (a) require `responses` OR explicit verified `evaluation_outcome` (in `OUTCOMES`), `accepted_case_ids` (non-string sequence, subset of `case_ids`), and `gate_failures` (non-string sequence of `rai_release.named` strings, propagated into `failure_reasons` if non-empty, returned in both `responses` and summary branches of `_extract_candidate_metrics()`, and folded into summary `evaluation_digest`), raising `ValueError` when any of the three is omitted or malformed on a summary candidate, and comparing non-offline summary `actual_serving_version` against `expected_serving_version` or `cand_levers["model"]`; (b) enforce `candidate_usage.currency == baseline_usage.currency` (raising `ValueError` when missing/blank and recording `currency_mismatch` gate failure when mismatched); (c) emit `manifest_digest` in `baseline_candidate_from_evaluation()` and verify `baseline.get("manifest_digest") == freeze["manifest_digest"]` in `_validate_baseline_artifact()` (raising `ValueError` when missing/blank or mismatched against a frozen manifest / approval digest, while appending `"baseline_manifest_digest_mismatch"` to `suite_blockers` when `manifest` itself was mutated post-approval); and (d) reject bare `str | bytes | bytearray` on top-level and per-candidate `rendered_prompts` / `tuning_examples`, pass candidate `lever_config.get("prompt")` values (and optional candidate `rendered_prompts`) through `check_prompt_tuning_isolation()`, and expose `holdout_leakage_clear` (`bool`), failing closed when a candidate prompt override leaks held-out case IDs or `expected_answer` shingles.
  * Observable acceptance criteria: Summary-only candidates omitting `evaluation_outcome`, `accepted_case_ids`, or `gate_failures` fail validation (`ValueError` / HTTP 400); non-empty `gate_failures`, `evaluation_outcome != "pass"`, currency mismatch, baseline `manifest_digest` mismatch, or leaked held-out case IDs/shingles in `lever_config["prompt"]` reject savings (`is_saving=False` or `ValueError`).
* **FR-5 (Grounded numeric/`ZF-*` support check & sample-sufficiency pre-gate)**: Implement `_check_statement_support()` in `heldout_eval.py` stripping 64-char hex digests (`\b[0-9a-f]{64}\b`) from `grounded_corpus` before digit extraction and flagging any `\b\d+\b` number (outside fixed regulatory standard designations `PAS 2035` / `PAS 2030`) or `\bZF-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*\b` identifier in candidate statements/findings/reasons that does not appear in the case's grounded source labels/facts as `unsupported_claims` (`unsupported_factual_claim` critical error), and gate the per-case scoring loop in `evaluate_heldout()` on `freeze["ready_for_evaluation"] and isolation["isolated"]`.
  * Observable acceptance criteria: Canonical baseline suite still passes 16/16 (`unsupported_claims == 0`); injecting an ungrounded number or foreign `ZF-*` ID into an otherwise cited assistant or legacy output increments `unsupported_claims` and fails the case without SHA-256 hex digest false negatives; raising a cohort `min_n` above available cases yields `outcome == "insufficient"` with `evaluated_total == 0` (`cases == []`).

## Non-Functional Requirements

* **NFR-1 (Focused-tier static, unit, and migration checks)**
  * Objective threshold or evaluation condition: Zero errors across targeted `unittest` suites, configuration-respecting `mypy`, `ruff check`, and `ruff format --check` in `src/core` and `src/api` (plus exact caller validation invocations and `--isolated` lint/format checks on modified files), and `python3 tools/rename-zava-tests.py`.
  * Observable acceptance criteria: All Focused-tier validation commands exit 0 and `git status --short` is empty after commit.
* **NFR-2 (Tracking path & dependency hygiene)**
  * Objective threshold or evaluation condition: Zero `.copilot-tracking/` references in production code, docstrings, READMEs, or commit messages, and zero non-`core` imports in `src/core`.
  * Observable acceptance criteria: `test_dependency_rule.py`, `test_content_standard.py`, and diff inspection confirm clean boundaries.

## Acceptance Criteria

* [ ] Branch `feat/ai-108-heldout-eval-0228` is cleanly rebased onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`7f83f4749`) with `GET /api/ai/report` returning both `chat_evaluation` and enriched `evaluation`.
* [ ] `src/api/tests/test_content_standard.py` passes with zero unauthorized `"human-approved"` occurrences in `src/core` or `src/api`.
* [ ] `heldout_eval.py` pins `FROZEN_THRESHOLDS_DIGEST` and `FROZEN_MANIFEST_DIGEST` for `HELDOUT-FREEZE-2026-10-15`, detects live `_capability_version_snapshot()` drift as `"capability_version_drift"` in `check_heldout_freeze()`, gates per-case scoring on `freeze["ready_for_evaluation"]`, flags ungrounded `\b\d+\b` numbers and `ZF-*` IDs in `_check_statement_support()`, and accepts `expected_serving_model` without mutating frozen manifests.
* [ ] `tokenomics_comparison.py` validates `baseline["manifest_digest"] == freeze["manifest_digest"]` in `_validate_baseline_artifact()`, requires `responses` or explicit `evaluation_outcome`, `accepted_case_ids`, and `gate_failures`, enforces `candidate_usage.currency == baseline_usage.currency`, and checks candidate `lever_config["prompt"]` values via `check_prompt_tuning_isolation()` (`holdout_leakage_clear`).
* [ ] Test governance locked: exact test removals = `none`; new test files = `0`; max added test methods = `16` across `src/core/tests/test_heldout_eval.py`, `src/core/tests/test_tokenomics_comparison.py`, and `src/api/tests/test_heldout_eval_api.py`; all Focused-tier validation commands exit 0; code and `c1` `.copilot-tracking/` artifacts committed locally with Copilot trailer and clean worktree (`git status --short` empty, not pushed).

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                         |
|----------------------------------|--------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/ai-108-heldout-eval-c1-plan.md                                                  |
| Phase details                    | .copilot-tracking/details/2026-11-15/ai-108-heldout-eval-c1-phase-details.md                                       |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/ai-108-heldout-eval-c1-plan-critique.md (`Revise` -> all 4 findings resolved) |
| Relevant research                | .copilot-tracking/research/2026-11-15/ai-108-heldout-eval-c1-research.md                                           |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/ai-108-heldout-eval-c1-changes.md owned by `rpi-implement`                    |
| Planning execution and readiness | Complete and Implementation-ready                                                                                  |
| Continuation context             | Confirmed automatic RPI Agent session; transitioning automatically to `rpi-implement`                              |

## Sources

* `.copilot-tracking/research/2026-11-15/ai-108-heldout-eval-c1-research.md`: Cycle 1 evidence log `C1`–`C15`, rebase analysis, and canonical false-positive audit.
* `.copilot-tracking/reviews/logs/2026-11-15/ai-108-heldout-eval-review.md`: Routed review findings `RV-001`–`RV-004`.
* `src/core/src/zava_forward/core/{heldout_eval,tokenomics_comparison,assistants,ai_tasks}.py`: Core evaluation, comparison, snapshot, and citation validators.
* `src/api/src/zava_forward/api/server.py` and `src/api/tests/{test_content_standard,test_heldout_eval_api,test_role_endpoint_inventory}.py`: API endpoints, content-standard copy guard, and integration tests.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Rebase onto Latest Parent Branch and Align `GET /api/ai/report`

* Intent: Rebase `feat/ai-108-heldout-eval-0228` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`7f83f4749`) while preserving untracked `c1` session artifacts and merging `chat_evaluation` with `evaluation.{held_out,tokenomics_comparison}`.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Rebase onto `origin/feat/demo-164-chat-grounding-provenance-0900` and reconcile `server.py` and `src/api/README.md`

* Requirement and evidence: FR-1 (`C1`, `C14`, `C15`)
* Expected result: Clean linear history atop `7f83f4749` with `GET /api/ai/report` returning `evaluation` (including `held_out` and `tokenomics_comparison`), `chat_evaluation`, `live`, `registry`, and `consumption`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/ai-108-heldout-eval-c1-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Content Standard Fix, Pinned Freeze Digests, Drift Check, and Statement Support in `heldout_eval.py`

* Intent: Resolve Findings 1, 2 (core part), 4, and 5 in `src/core/src/zava_forward/core/heldout_eval.py` and `src/core/README.md`.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Replace `"human-approved"` wording and pin `FROZEN_THRESHOLDS_DIGEST` / `FROZEN_MANIFEST_DIGEST` with live drift checks

* Requirement and evidence: FR-2, FR-3 (`C2`–`C6`, `C8`, `C9`)
* Expected result: Zero unauthorized `"human-approved"` strings; `CANONICAL_FREEZE_ID = "HELDOUT-FREEZE-2026-10-15"`, `FROZEN_THRESHOLDS_DIGEST`, and `FROZEN_MANIFEST_DIGEST` pinned statically; `check_heldout_freeze()` records `"capability_version_drift:<keys>"` on live version drift; `evaluate_heldout()` accepts `expected_serving_model` and `baseline_candidate_from_evaluation()` includes `manifest_digest`.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/ai-108-heldout-eval-c1-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Add `_check_statement_support()` for numbers and `ZF-*` IDs and gate scoring on `freeze["ready_for_evaluation"]`

* Requirement and evidence: FR-5 (`C7`, `C8`, `C13`)
* Expected result: `_check_statement_support()` flags ungrounded `\b\d+\b` numbers and `ZF-*` case IDs in both assistant and legacy outputs as `unsupported_claims` (`unsupported_factual_claim`), and `evaluate_heldout()` skips per-case scoring when `not freeze["ready_for_evaluation"]`.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/ai-108-heldout-eval-c1-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Harden Tokenomics Candidate Comparison and Summary-Payload Guards

* Intent: Resolve Findings 2 (`tokenomics_comparison` part) and 3 in `src/core/src/zava_forward/core/tokenomics_comparison.py`.
* Dependencies: P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Remove manifest re-signing and enforce summary verification, currency parity, baseline digest binding, and prompt-lever isolation

* Requirement and evidence: FR-3, FR-4 (`C10`–`C12`)
* Expected result: `_manifest_for_candidate_model()` removed in favor of `expected_serving_model`; `_validate_baseline_artifact()` checks `baseline.get("manifest_digest") == freeze["manifest_digest"]`; summary candidates must supply explicit `evaluation_outcome`, `accepted_case_ids`, and `gate_failures`; `candidate_usage.currency == baseline_usage.currency` enforced; candidate `lever_config["prompt"]` scanned via `check_prompt_tuning_isolation()` with `holdout_leakage_clear` reported.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/ai-108-heldout-eval-c1-phase-details.md

<!-- rpi:phase id=P04 -->
### [x] P04: Regression Tests and Focused-Tier Validation

* Intent: Update summary-candidate test fixtures, add negative regression tests for all resolved findings, and pass all Focused-tier test, typing, lint, format, and rename checks.
* Dependencies: P01, P02, P03

<!-- rpi:task id=P04-T01 -->
#### [x] P04-T01: Update and expand `test_heldout_eval.py`, `test_tokenomics_comparison.py`, and `test_heldout_eval_api.py` and run Focused validation

* Requirement and evidence: FR-1 through FR-5, NFR-1, NFR-2 (`C1`, `C2`, `C14`)
* Expected result: Focused negative tests prove every fixed finding; all unit tests, `mypy`, `ruff check`, `ruff format --check`, and `tools/rename-zava-tests.py` exit 0.
* Detail section: P04-T01 in .copilot-tracking/details/2026-11-15/ai-108-heldout-eval-c1-phase-details.md

## Dependencies

* `origin/feat/demo-164-chat-grounding-provenance-0900` (`7f83f4749`): Stacked parent branch providing `chat_eval` integration on `GET /api/ai/report`.
* Existing `zava_forward.core` contracts (`ai`, `ai_consumption`, `ai_prompts`, `ai_registry`, `ai_tasks`, `assistants`, `cohort_eval`, `quality`, `rai_release`, `ranking`).

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| `PC-001` [High]: Focused-tier `ruff --isolated` over `src tests` ignores `pyproject.toml` exclusions on migrated `v0.21.0` files and bare `mypy` in `src/api` omits shared test `PYTHONPATH` | Resolved | Updated NFR-1, P04, and P04-T01 to run configuration-respecting `mypy`, `ruff check src tests`, and `ruff format --check src tests` (with `PYTHONPATH=../core/tests:../agents/tests` in `src/api`), alongside `--isolated --line-length 100` lint/format verification on all Cycle 1 modified files and testing the caller's exact command invocations without mutating untouched legacy modules. |
| `PC-002` [High]: SHA-256 hex digests inside `snap["sources"]` pollute grounded digit extraction in `_check_statement_support()` | Resolved | Updated FR-5 and P02-T02 to strip 64-character hex digests (`\b[0-9a-f]{64}\b`, case-insensitive) from `grounded_corpus` prior to `\d+` extraction and tightened the `ZF-*` pattern to `\bZF-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*\b`. |
| `PC-003` [High]: Unconditional `ValueError` in `_validate_baseline_artifact` collides with unfrozen-manifest test, response-branch `_extract_candidate_metrics` omits `gate_failures`, and negative summary fixtures need explicit fields | Resolved | Updated FR-4, P03-T01, and P04-T01 so `_validate_baseline_artifact` raises `ValueError` when `baseline["manifest_digest"]` is missing/blank or mismatches a frozen manifest / approval digest while recording `"baseline_manifest_digest_mismatch"` in `suite_blockers` when `manifest` itself was mutated post-approval; returned `"gate_failures"` in both `responses` and summary branches, validated summary `gate_failures` items via `rai_release.named`, included `evaluation_outcome`/`accepted_case_ids`/`gate_failures` in summary `evaluation_digest`; and updated all existing non-schema-error summary fixtures across tests. |
| `PC-004` [Medium]: Exact `"capability_version_drift"` blocker token compatibility, bare-string `rendered_prompts` sequence bypass, and non-offline summary serving-model fallback | Resolved | Updated FR-3, FR-4, P02-T01, and P03-T01 to append both `"capability_version_drift"` and `"capability_version_drift:<keys>"` to `blockers`, reject bare `str | bytes | bytearray` for top-level and per-candidate `rendered_prompts` and `tuning_examples`, and compare non-offline summary `actual_serving_version` against `expected_serving_version` or `cand_levers["model"]`. |

## Follow-Up Items

* Owner-authorized live Azure OpenAI held-out batch execution and regional quota attestation for Issue #108 — outside offline synthetic scope; requires owner spend authorization and deployed Azure OpenAI endpoints.
* Human staff participant effectiveness evaluation and OQ-018 cohort owner sign-off for Issue #108 — outside offline synthetic scope; requires named human staff participants and DPO/RAI owner approvals.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/ai-108-heldout-eval-c1-changes.md
* Ready phase or task: `P01-T01` through `P04-T01` ready for `rpi-implement`
* Remaining provisional question or blocker: None
