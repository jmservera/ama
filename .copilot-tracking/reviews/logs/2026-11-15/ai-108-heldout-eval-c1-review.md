<!-- markdownlint-disable-file -->
# Review: Issue #108 Cycle 1 Independent Review Fixes and Parent Rebase

## Scope and Evidence

* Task ID: issue-108-heldout-eval-c1
* Review date: 2026-11-15
* Review scope: Full task (`P01`, `P02`, `P03`, `P04`; `P01-T01`, `P02-T01`, `P02-T02`, `P03-T01`, `P04-T01`)
* Assessed boundary: Cycle 1 (`c1`) remediation of all five findings from the independent exact-head functional review (`18dc9d132`), parent rebase reconciliation (`GET /api/ai/report` 5-key contract), test-governance lock (`0` test removals, `0` new test files, `13 <= 16` added test methods), and Focused-tier validation across `src/core` and `src/api`.
* Plan: .copilot-tracking/plans/2026-11-15/ai-108-heldout-eval-c1-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/ai-108-heldout-eval-c1-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/ai-108-heldout-eval-c1-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/ai-108-heldout-eval-c1-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/ai-108-heldout-eval-c1-research.md (`C1`–`C15`), `git diff` across `src/core` and `src/api`, and Focused-tier validation outputs (`unittest`, `mypy`, `ruff check`, `ruff format --check`, `tools/rename-zava-tests.py`).

## Opening Review State

* Interpreted review goal: Perform one evidence-based review of the completed Cycle 1 (`c1`) implementation for Issue #108, verifying that all five independent review findings, parent rebase requirements, and resolved plan-critique findings (`PC-001`–`PC-004`) are faithfully implemented, tested, and reconciled.
* Review scope: Full task (`P01` through `P04`)
* Evidence readiness: Ready; research, plan, phase details, single-pass plan critique, changes log, and Focused-tier validation outputs are complete and reconciled.
* Acceptance basis: `FR-1` through `FR-5`, `NFR-1`, `NFR-2`, `AC-1` through `AC-5`, and `PC-001` through `PC-004` in .copilot-tracking/plans/2026-11-15/ai-108-heldout-eval-c1-plan.md.
* First comparison boundary: Plan phase checklist (`P01`–`P04`) and critique dispositions (`PC-001`–`PC-004`) compared against .copilot-tracking/changes/2026-11-15/ai-108-heldout-eval-c1-changes.md and source diffs in `src/core` and `src/api`.
* Active read-only boundaries: Canonical review log creation only during `rpi-review`; no mutations to plan, phase details, critique, research, or changes artifacts.
* Initial blockers: None.

## Execution Status

* Execution status: Complete
* Review execution evidence: Reviewed full Cycle 1 artifact set and `src/core` / `src/api` diffs on 2026-11-15 across `P01-T01`, `P02-T01`, `P02-T02`, `P03-T01`, and `P04-T01`.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`) | Parent Branch Rebase and `GET /api/ai/report` Alignment | Reconciled | `server.py`, `src/api/README.md`, and `test_heldout_eval_api.py` preserve both `chat_evaluation` and `evaluation.{held_out,tokenomics_comparison}`. |
| `P02` (`P02-T01`, `P02-T02`) | Content Standard Fix, Pinned Freeze Digests, Drift Check, and Statement Support | Reconciled | Unauthorized `"human-approved"` removed; `HELDOUT-FREEZE-2026-10-15` digests pinned statically; `capability_version_drift` blocker check, `_check_statement_support()`, `freeze["ready_for_evaluation"]` pre-gate, `expected_serving_model`, and baseline `manifest_digest` implemented. |
| `P03` (`P03-T01`) | Tokenomics Candidate Comparison and Summary-Payload Hardening | Reconciled | `_manifest_for_candidate_model()` deleted; `_validate_baseline_artifact()` checks `manifest_digest` and currency; summary candidates require `evaluation_outcome`, `accepted_case_ids`, and `gate_failures`; currency parity and `lever_config["prompt"]` isolation (`holdout_leakage_clear`) enforced. |
| `P04` (`P04-T01`) | Regression Tests and Focused-Tier Validation | Reconciled | Summary fixtures updated, 13 focused regression test methods added (`0` removals, `0` new files, within `<= 16` cap), and Focused-tier checks passed. |
| `Follow-Up Items` | Blockers and Follow-Ups | Reconciled | Live Azure OpenAI held-out batch execution, regional quota attestation, and human staff / OQ-018 cohort sign-off remain outside offline scope (`Refs #108`). |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/api/src/zava_forward/api/server.py`, `src/api/README.md` | Reconciled `GET /api/ai/report` with parent `chat_eval.run_eval()` (`"chat_evaluation"`) alongside `evaluation.{held_out,tokenomics_comparison}` and documented summary candidate requirements. | 5-key payload verified in `server.py` and `src/api/README.md`. | `test_heldout_eval_api.py`, `test_role_endpoint_inventory.py` passed. | Reconciled |
| `P02-T01` | `src/core/src/zava_forward/core/heldout_eval.py`, `src/core/README.md` | Replaced `"human-approved"` with `"human-authorized"`, pinned `CANONICAL_FREEZE_ID`, `FROZEN_THRESHOLDS_DIGEST`, and `FROZEN_MANIFEST_DIGEST` using `FROZEN_VERSIONS` / `FROZEN_CAPABILITY_VERSIONS` without runtime `approve_manifest(...)`, added live `_capability_version_snapshot()` drift detection in `check_heldout_freeze()`, added `expected_serving_model`, and emitted `manifest_digest` in `baseline_candidate_from_evaluation()`. | Static constants match canonical freeze; zero unattributed `"human-approved"` matches in `heldout_eval.py` or modified README lines. | `test_content_standard.py`, `test_heldout_eval.py`, `mypy`, `ruff` passed. | Reconciled |
| `P02-T02` | `src/core/src/zava_forward/core/heldout_eval.py` | Added `_check_statement_support()` (stripping 64-char SHA-256 hex digests and `PAS 2030`/`2035` designations before checking `\b\d+\b` numbers and `\bZF-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*\b` IDs) and pre-gated per-case scoring in `evaluate_heldout()` on `freeze["ready_for_evaluation"] and isolation["isolated"]`. | Canonical 16-case baseline achieves `unsupported_claims == 0`; injected numbers/foreign `ZF-*` fail closed; insufficient cohort floor skips scoring (`evaluated_total == 0`). | `test_heldout_eval.py`, `mypy`, `ruff` passed. | Reconciled |
| `P03-T01` | `src/core/src/zava_forward/core/tokenomics_comparison.py`, `src/core/README.md`, `src/api/README.md` | Removed `_manifest_for_candidate_model()`, validated `baseline["manifest_digest"] == freeze["manifest_digest"]` and baseline currency, enforced explicit `evaluation_outcome`, `accepted_case_ids`, and `gate_failures` on summary candidates, enforced `candidate_usage.currency == baseline_usage.currency`, and scanned `lever_config["prompt"]` via `check_prompt_tuning_isolation()` (`holdout_leakage_clear`). | All summary-only bypass vectors fail closed (`ValueError` or `is_saving=False`). | `test_tokenomics_comparison.py`, `test_heldout_eval_api.py`, `mypy`, `ruff` passed. | Reconciled |
| `P04-T01` | `src/core/tests/test_heldout_eval.py`, `src/core/tests/test_tokenomics_comparison.py`, `src/api/tests/test_heldout_eval_api.py` | Updated summary fixtures and added 13 focused regression test methods (`5` + `6` + `2`) covering all five review findings. | `13 <= 16` added methods, `0` removed tests, `0` new test files. | 93 targeted unit tests + 25 migration tests passed. | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P04-T01` validation execution | Validated `mypy`, `unittest`, and `tools/rename-zava-tests.py` using a temporary virtualenv (`/tmp/zf-108-venv`, deleted after verification) with editable installs of this worktree's `src/core`, `src/agents`, and `src/api` so shared `~/.local` sibling-worktree paths were neither relied upon nor mutated. | Local judgment during `P04-T01` (`~/.local` editable paths pointed to another active worktree). No user decision required. | Recorded in .copilot-tracking/changes/2026-11-15/ai-108-heldout-eval-c1-changes.md and .copilot-tracking/details/2026-11-15/ai-108-heldout-eval-c1-phase-details.md. | Not needed; preserves `NFR-1` and `PC-001` intent. | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All four single-pass critique findings (`PC-001` through `PC-004`) in .copilot-tracking/reviews/plans/2026-11-15/ai-108-heldout-eval-c1-plan-critique.md were resolved in the plan and verified in the implementation:
  * `PC-001`: Configuration-respecting `mypy`, `ruff check src tests`, and `ruff format --check src tests` passed across `src/core` and `src/api`, and `ruff format --isolated --line-length 100 --check` passed on all 5 modified Python files.
  * `PC-002`: `_HEX_DIGEST_RE` strips 64-character hex digests from `grounded_corpus` before digit token extraction in `_check_statement_support()`, preventing SHA-256 hash substrings from masking hallucinated integers.
  * `PC-003`: `_validate_baseline_artifact()` raises `ValueError` when `baseline["manifest_digest"]` is missing or mismatches a frozen manifest while recording `"baseline_manifest_digest_mismatch"` in `suite_blockers` when `manifest` itself was mutated post-approval; `"gate_failures"` is returned in both branches of `_extract_candidate_metrics()` and folded into summary `evaluation_digest`.
  * `PC-004`: `check_heldout_freeze()` emits both `"capability_version_drift"` and `"capability_version_drift:<keys>"`; bare strings are rejected on `rendered_prompts` and `tuning_examples`; non-offline summary candidates validate `actual_serving_version` against `expected_serving_version` or `cand_levers["model"]`.
* Material revisions: None occurred during implementation.
* Dependent-work pause assessment: No dependent-work pause was needed; phases executed strictly in dependency order (`P01` -> `P02` -> `P03` -> `P04`).
* Justification assessment: Supported by code and test evidence.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Live Azure OpenAI held-out batch execution and regional quota attestation (`Refs #108`) | Offline Cycle 1 harness cannot authorize live model spend or verify live regional quota without deployed Azure OpenAI endpoints. | Programme owner / AI release owner when live Foundry/AOAI environment is authorized. | Open external gate; distinct follow-up (`Refs #108`). |
| Human staff participant effectiveness evaluation and OQ-018 cohort owner sign-off (`Refs #108`) | Requires real staff evaluation sessions and named DPO/RAI owner governance sign-off outside synthetic repository code. | Named DPO, RAI governance owner, and programme manager. | Open external gate; distinct follow-up (`Refs #108`). |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Upstream stacked parent branch advanced (`0c1fa1da4`, PR #1769) after `P01-T01` rebase

* Related scope: `P01-T01`
* Evidence: `origin/feat/demo-164-chat-grounding-provenance-0900` was at `7f83f4749` (`#1761`) during `P01-T01` rebase and subsequently advanced to `0c1fa1da4` (`#1769`), adding 1-line route entries in `src/api/src/zava_forward/api/server.py` (`get_kind`) and `src/api/tests/test_role_endpoint_inventory.py` (`GET_ENDPOINTS`, `POST_ENDPOINTS`).
* Impact: Non-defect operational branch-lineage sync item; syncing the commit stack onto `0c1fa1da4` before pushing ensures conflict-free stacked PR creation against `feat/demo-164-chat-grounding-provenance-0900`.
* Destination: follow_up
* Smallest useful next action: Rebase the committed `#108` branch stack onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`) and re-verify Focused-tier tests before pushing/opening the PR.

## Defects

* None.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | `follow_up` | Branch git sync onto latest `origin/feat/demo-164-chat-grounding-provenance-0900` (`0c1fa1da4`) prior to PR push | Concurrent upstream merge (`#1769`) on stacked parent branch after `P01-T01` completed; zero defects in Cycle 1 code or tests |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Sync stacked branch ancestry with concurrent parent commit `0c1fa1da4` (`#1769`) prior to PR creation (`RV-001`), run independent exact-head review + hosted CI on the pushed PR head, and retain `Refs #108` for owner-authorized live Azure OpenAI batch evaluation, quota attestation, and human participant / OQ-018 sign-off.

## Blockers and Remaining Work

* Blockers: None for Cycle 1 offline code and evidence.
* Remaining active work: None (`P01` through `P04` complete).

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `PYTHONPATH=src/core/src:src/core/tests:src/api/src:src/api/tests:src/agents/src python -m unittest src/api/tests/test_content_standard.py src/core/tests/test_heldout_eval.py src/core/tests/test_tokenomics_comparison.py src/api/tests/test_heldout_eval_api.py src/api/tests/test_role_endpoint_inventory.py -v` | `src/core` and `src/api` targeted suites | Passed | `Ran 93 tests in 23.147s`, `OK`. |
| `(cd src/core && python -m mypy && ruff check src tests && ruff format --check src tests)` | `src/core` typing, lint, format | Passed | `Success: no issues found in 340 source files`; `All checks passed!`; `286 files already formatted`. |
| `(cd src/api && python -m mypy && ruff check src tests && ruff format --check src tests)` | `src/api` typing, lint, format | Passed | `Success: no issues found in 281 source files`; `All checks passed!`; `196 files already formatted`. |
| `ruff format --isolated --line-length 100 --check` on modified Python files | Modified Cycle 1 `.py` files | Passed | `5 files already formatted`. |
| `python tools/rename-zava-tests.py` | Repository migration regression suite | Passed | `Ran 25 tests in 0.528s`, `OK`. |
| Docker build & `tools/rpi-checks.py --all` | Full external gate | Skipped | Focused tier requested by caller (no Docker/full gate during Cycle 1). |

## Outcome

* Outcome: Conformant
* Outcome rationale: All five independent review findings (`18dc9d132`), `FR-1` through `FR-5`, `NFR-1`, `NFR-2`, `AC-1` through `AC-5`, and `PC-001` through `PC-004` are completely resolved, reconciled across plan/details/changes artifacts, and verified by 13 focused regression test methods plus Focused-tier static and unit checks with zero defects.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | None |
| Decision gap or invalid assumption | none | None |
| Material evidence gap | none | None |
| Non-blocking residual work | distinct follow-up | Sync stacked branch onto concurrent parent tip `0c1fa1da4` (`RV-001`), push + run independent exact-head review & hosted CI, and keep `Refs #108` for live AOAI batch / quota / human OQ-018 sign-off |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: 93 targeted unit tests, strict `mypy` (340 `core` + 281 `api` files), `ruff check` + `ruff format --check` across `src/core` and `src/api`, and `tools/rename-zava-tests.py` (25 tests) passed; Docker/full external gate intentionally skipped per Focused-tier scope.
* Blockers: None for offline Cycle 1 remediation; live AOAI batch execution, quota attestation, and human OQ-018 cohort sign-off remain external (`Refs #108`).
