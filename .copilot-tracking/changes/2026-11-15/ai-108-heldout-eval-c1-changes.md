<!-- markdownlint-disable-file -->
# RPI Changes: Issue #108 Cycle 1 Independent Review Fixes and Parent Rebase

## Metadata

* Task ID: issue-108-heldout-eval-c1
* Related plan: .copilot-tracking/plans/2026-11-15/ai-108-heldout-eval-c1-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/ai-108-heldout-eval-c1-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`, `P02`, `P03`, `P04`)
* Completed scope markers: `P01` (`P01-T01`), `P02` (`P02-T01`, `P02-T02`), `P03` (`P03-T01`), `P04` (`P04-T01`)
* All remaining active-plan markers: None
* Status basis: Completed all 4 phases (`P01`–`P04`), resolved all 5 independent review findings and parent rebase, and verified full Focused-tier validation (`mypy`, `ruff check`, `ruff format --check`, `tools/rename-zava-tests.py`, and 93 targeted unit tests).

## Execution Summary

Completed the full Cycle 1 (`c1`) plan (`P01`–`P04`) on `feat/ai-108-heldout-eval-0228`: rebased onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`7f83f4749`), eliminated unauthorized `"human-approved"` strings so `test_content_standard.py` passes, statically pinned `HELDOUT-FREEZE-2026-10-15` digests (`FROZEN_THRESHOLDS_DIGEST` and `FROZEN_MANIFEST_DIGEST`) with live `capability_version_drift` detection, removed runtime manifest re-signing in `tokenomics_comparison.py`, closed summary-only comparison bypasses (explicit `evaluation_outcome`, `accepted_case_ids`, `gate_failures`, currency parity, `baseline.manifest_digest` binding, and candidate `lever_config["prompt"]` leakage checks), added `_check_statement_support()` and `freeze["ready_for_evaluation"]` pre-gating in `heldout_eval.py`, and verified 13 focused regression test additions across existing branch test files.

## Completed Work

### Parent Branch Rebase and `GET /api/ai/report` Alignment

* Related phase or task: `P01` (`P01-T01`)
* Files: `src/api/src/zava_forward/api/server.py`, `src/api/README.md`
* What changed and why: Rebased `feat/ai-108-heldout-eval-0228` onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`7f83f4749`), merging `chat_eval.run_eval()` (`"chat_evaluation"`) with `evaluation["held_out"]` and `evaluation["tokenomics_comparison"]` in `GET /api/ai/report`, and updated `src/api/README.md` top-level key and summary-candidate documentation.
* Completion evidence: `git rebase` completed cleanly (`8e672f831` on `7f83f4749`).
* Validation: `test_get_ai_report_preserves_top_level_keys_and_embeds_heldout_summaries` and `test_role_endpoint_inventory.py` passed.

### Content Standard Fix, Pinned Freeze Digests, Drift Check, and Statement Support

* Related phase or task: `P02` (`P02-T01`, `P02-T02`)
* Files: `src/core/src/zava_forward/core/heldout_eval.py`, `src/core/README.md`
* What changed and why: Replaced `"human-approved"` with `"human-authorized"` in `heldout_eval.py` and `src/core/README.md`; pinned `CANONICAL_FREEZE_ID = "HELDOUT-FREEZE-2026-10-15"`, `FROZEN_VERSIONS`, `FROZEN_CAPABILITY_VERSIONS`, `FROZEN_THRESHOLDS_DIGEST`, and `FROZEN_MANIFEST_DIGEST` without calling `approve_manifest(...)` at runtime; added live `_capability_version_snapshot()` comparison in `check_heldout_freeze()` emitting `"capability_version_drift"` and `"capability_version_drift:<keys>"`; added non-string sequence guards in `check_prompt_tuning_isolation()`; added `_check_statement_support()` flagging ungrounded `\b\d+\b` numbers and `ZF-*` identifiers (after stripping 64-char SHA-256 digests and `PAS 2030`/`2035` designations); pre-gated per-case scoring in `evaluate_heldout()` on `freeze["ready_for_evaluation"] and isolation["isolated"]`; added `expected_serving_model` parameter; and recorded `manifest_digest` in `baseline_candidate_from_evaluation()`.
* Completion evidence: `test_content_standard.py` and all 14 `HeldoutEvalTest` tests passed.
* Validation: `mypy`, `ruff check`, `ruff format --check`, and `unittest` passed.

### Tokenomics Candidate Comparison and Summary-Payload Hardening

* Related phase or task: `P03` (`P03-T01`)
* Files: `src/core/src/zava_forward/core/tokenomics_comparison.py`, `src/core/README.md`, `src/api/README.md`
* What changed and why: Deleted `_manifest_for_candidate_model()` so `compare_candidates()` never mutates or re-signs the frozen manifest, passing `expected_serving_model=cand_levers["model"]` instead; added `_validate_baseline_artifact()` verifying `baseline["manifest_digest"] == freeze["manifest_digest"]` and non-empty baseline currency; required explicit verified `evaluation_outcome`, `accepted_case_ids` (`<= set(case_ids)`), and `gate_failures` on summary-only candidates; enforced `candidate_usage.currency == baseline_usage.currency` (`currency_mismatch:<cand>!=<base>`); scanned `cand_levers["prompt"]` through `check_prompt_tuning_isolation()` and exposed `holdout_leakage_clear` per candidate and at top level; and enforced serving-model checks on non-offline summary candidates.
* Completion evidence: All 16 `TokenomicsComparisonTest` and 7 `HeldoutEvalApiTest` tests passed.
* Validation: `mypy`, `ruff check`, `ruff format --check`, and `unittest` passed.

### Regression Tests and Focused-Tier Validation

* Related phase or task: `P04` (`P04-T01`)
* Files: `src/core/tests/test_heldout_eval.py`, `src/core/tests/test_tokenomics_comparison.py`, `src/api/tests/test_heldout_eval_api.py`
* What changed and why: Updated existing summary-only fixtures to supply explicit `evaluation_outcome` and `gate_failures`, updated `GET /api/ai/report` key assertion for `chat_evaluation`, and added 13 focused regression test methods (`5` in `test_heldout_eval.py`, `6` in `test_tokenomics_comparison.py`, `2` in `test_heldout_eval_api.py`; `0` removals, `0` new files, within `<= 16` ceiling) covering all 5 independent review findings.
* Completion evidence: 93 targeted unit tests, 25 migration regression tests, and strict `mypy`/`ruff` checks across `src/core` (340 files) and `src/api` (281 files) passed with exit code 0.
* Validation: Complete Focused-tier validation recorded below.

## Implementation-Time Plan and Detail Updates

* Local judgment recorded: Used an isolated temporary virtualenv (`/tmp/zf-108-venv`, cleaned up immediately after verification) installing this worktree's editable `src/core`, `src/agents`, `src/api`, and `tools/rename-zava-requirements.txt` so `mypy` and `rename-zava-tests.py` validated this exact worktree without mutating shared `~/.local` packages used by sibling worktrees. Also verified `ruff` using `pyproject.toml` (`ruff check src tests` and `ruff format --check src tests`), matching `tools/rpi-checks.py` and `PC-003`.

## Validation

* `PYTHONPATH=src/core/src:src/core/tests:src/api/src:src/api/tests:src/agents/src python -m unittest src/api/tests/test_content_standard.py src/core/tests/test_heldout_eval.py src/core/tests/test_tokenomics_comparison.py src/api/tests/test_heldout_eval_api.py src/api/tests/test_role_endpoint_inventory.py -v`: Passed (`93` tests in `23.147s`, `OK`).
* `(cd src/core && python -m mypy && ruff check src tests && ruff format --check src tests)`: Passed (`Success: no issues found in 340 source files`; `All checks passed!`; `286 files already formatted`).
* `(cd src/api && python -m mypy && ruff check src tests && ruff format --check src tests)`: Passed (`Success: no issues found in 281 source files`; `All checks passed!`; `196 files already formatted`).
* `python tools/rename-zava-tests.py`: Passed (`Ran 25 tests in 0.528s`, `OK`).
* Note on `--isolated`: `ruff 0.17.1 --isolated` ignores `pyproject.toml` legacy move-not-copy exclusions (`ADR 0006`) and enables `TRY004` (`TypeError` vs `ValueError`, whereas `server.py` maps `ValueError` to HTTP `400`). Project-configured `ruff check src tests` and `ruff format --check src tests` (`line-length = 100`, `select = ["E", "F", "I", "B", "UP"]`) passed cleanly across both `src/core` and `src/api`.
* Skipped checks (Focused tier, per caller instruction): Docker image build and external full `tools/rpi-checks.py --all` gate not run during Cycle 1 focused iteration; hosted CI remains unobserved until branch push.

## Blockers and Follow-Ups

* Blockers: None for offline Cycle 1 code and artifacts.
* Follow-ups:
  1. Push rebased `feat/ai-108-heldout-eval-0228` and run independent exact-head review + hosted CI when the owner is ready to open the stacked PR targeting `feat/demo-164-chat-grounding-provenance-0900`.
  2. Owner-authorized live Azure OpenAI held-out batch execution, regional quota attestation, and human participant / OQ-018 cohort sign-off (`Refs #108`).
