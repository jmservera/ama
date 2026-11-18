<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #108 Cycle 1 Independent Review Fixes and Parent Rebase

## Metadata

* Task ID: issue-108-heldout-eval-c1
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/ai-108-heldout-eval-c1-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/ai-108-heldout-eval-c1-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Cycle 1 (`c1`) remediation on branch `feat/ai-108-heldout-eval-0228` to rebase onto `origin/feat/demo-164-chat-grounding-provenance-0900` (`7f83f4749`), resolve all five findings from the supplied independent exact-head functional review of `18dc9d132` (content-standard `"human-approved"` removal; pinned `HELDOUT-FREEZE-2026-10-15` digests, live capability-version drift blocking, and immutable model candidate verification; summary-only candidate verification, currency parity, baseline `manifest_digest` binding, and candidate `lever_config["prompt"]` leakage checks; `_check_statement_support` ungrounded number and `ZF-*` detection; and gating per-case scoring on `freeze["ready_for_evaluation"]`), run Focused-tier local validation only, and commit locally with a clean worktree without pushing.
* Research and evidence considered: .copilot-tracking/research/2026-11-15/ai-108-heldout-eval-c1-research.md (`C1`-`C15`), .copilot-tracking/reviews/logs/2026-11-15/ai-108-heldout-eval-review.md (`RV-001`-`RV-004`), supplied independent functional review report for `18dc9d132`, src/core/src/zava_forward/core/heldout_eval.py, src/core/src/zava_forward/core/tokenomics_comparison.py, src/core/src/zava_forward/core/assistants.py, src/core/src/zava_forward/core/ai_tasks.py, src/core/pyproject.toml, src/core/README.md, src/api/src/zava_forward/api/server.py, src/api/pyproject.toml, src/api/README.md, src/api/tests/test_content_standard.py, src/core/tests/test_heldout_eval.py, src/core/tests/test_tokenomics_comparison.py, and src/api/tests/test_heldout_eval_api.py.
* Decisions, dependencies, and acceptance criteria considered: Confirmed Focused-tier validation scope (no Docker or full external gate), local-only commit boundary (no push), test-governance lock (`0` test removals, `0` new test files, `<= 16` added test methods), stacked parent dependency `origin/feat/demo-164-chat-grounding-provenance-0900` (`7f83f4749`), `FR-1` through `FR-5`, `NFR-1`, `NFR-2`, and `AC-1` through `AC-5`.
* Assessment boundary: Evaluates plan and phase-detail credibility against supplied repository source, configuration, tests, research, and review artifacts without modifying repository state, running live network calls, or executing git rebase during critique.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| FR-1, Q1 (`C1`, `C14`, `C15`), P01, P01-T01 | Covered | Rebase onto `7f83f4749` and 5-key `GET /api/ai/report` reconciliation (`evaluation`, `chat_evaluation`, `live`, `registry`, `consumption`) in src/api/src/zava_forward/api/server.py, src/api/README.md, and src/api/tests/test_heldout_eval_api.py are complete and accurate. |
| FR-2, Q2 (`C2`-`C4`), P02-T01 | Covered | Replacing unauthorized `"human-approved"` occurrences at src/core/src/zava_forward/core/heldout_eval.py lines 4 and 1397 and src/core/README.md line 15 with `"human-authorized"` directly satisfies `CopyAudit.test_ai_label_is_exact_and_never_implies_approval`. |
| FR-3, Q3 (`C5`, `C6`, `C9`, `C11`), P02-T01, P03-T01 | Partial | Static `CANONICAL_FREEZE_ID`, `FROZEN_THRESHOLDS_DIGEST`, `FROZEN_MANIFEST_DIGEST`, and `expected_serving_model` cleanly remove runtime manifest signing, but `P02-T01` appends only `capability_version_drift:<keys>` without the exact `"capability_version_drift"` blocker token requested by Caller Requirement 3 (`PC-004`). |
| FR-4, Q4 (`C9`, `C10`, `C12`), P03, P03-T01 | Partial | Summary-only candidate checks, currency parity, baseline digest binding, and prompt-lever isolation are planned, but unconditional `ValueError` in `_validate_baseline_artifact` collides with an existing unfrozen-manifest test, `_extract_candidate_metrics` omits `"gate_failures"` on the `responses` branch and allows blank strings (`PC-003`), and per-candidate `rendered_prompts` lacks a non-string sequence guard (`PC-004`). |
| FR-5, Q5 (`C7`, `C8`, `C13`), P02-T02 | Partial | Sample-floor pre-gating (`freeze["ready_for_evaluation"]`) is sound, but `_check_statement_support` extracts grounded `\d+` tokens from raw `snap["sources"]` JSON containing up to five 64-char SHA-256 hex digests per assistant case, allowing invented numbers that match hex digit runs to evade `unsupported_claims` (`PC-002`). |
| NFR-1, NFR-2, AC-5, P04, P04-T01 | Partial | Test governance and negative test scenarios cover all five findings, but `P04` passes `--isolated` to `ruff check` and `ruff format` across `src tests`, overriding pyproject.toml legacy exclusions and guaranteeing lint and format failure (`PC-001`), and `P04-T01` under-specifies summary fixture updates for existing negative tests (`PC-003`). |

## Verdict

* Verdict: Revise
* Rationale: Phase structure and architectural choices address the parent rebase and all five independent review findings, capability-by-capability, without violating stdlib or offline boundaries. However, four planner-correctable defects (`PC-001` through `PC-004`, three High and one Medium) would cause Focused-tier validation failure (`ruff --isolated` over excluded legacy files and an existing `test_tokenomics_comparison.py` assertion crash/response-branch `KeyError`) or leave subtle security/grounding bypasses (SHA-256 hex digits polluting grounded numeric tokens in `snap["sources"]`, and bare-string `rendered_prompts` shredding in candidate prompt isolation). All four are direct planner corrections requiring zero user decisions.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Focused-tier `ruff --isolated` commands ignore pyproject.toml legacy exclusions and fail validation

* Related IDs: NFR-1, AC-5, P04, P04-T01
* Evidence: .copilot-tracking/details/2026-11-15/ai-108-heldout-eval-c1-phase-details.md (`P04` Validation Expectations), .copilot-tracking/plans/2026-11-15/ai-108-heldout-eval-c1-plan.md (`NFR-1`), src/core/pyproject.toml, src/api/pyproject.toml, .copilot-tracking/reviews/logs/2026-11-15/ai-108-heldout-eval-review.md (`Validation Evidence`)
* Concern: `P04` and `NFR-1` instruct `rpi-implement` to run `ruff check --isolated src tests` and `ruff format --isolated --line-length 100 --check src tests` in both `src/core` and `src/api`, plus bare `mypy` in `src/api`. Ruff's `--isolated` flag ignores pyproject.toml, disabling `[tool.ruff.lint.per-file-ignores]` and `[tool.ruff.format] exclude` entries required for migrated `v0.21.0` modules (`server.py`, `auth.py`, `timecapture.py`, `assistants.py`, `ai.py`, `dataset.py`, `test_content_standard.py`, etc.). Running `--isolated` over `src tests` fails on hundreds of intentional legacy exclusions, and running `mypy` in `src/api` without `PYTHONPATH=../core/tests:../agents/tests` (and `.venv/bin/python -m` fallback) drops shared agent test paths.
* Impact: `P04-T01` validation will fail deterministically on untouched migrated files even when all Cycle 1 changes are conformant.
* Smallest useful change: Replace the `ruff` and `mypy` commands in `NFR-1`, `P04`, and `P04-T01` with configuration-respecting project runs: `(cd src/core && .venv/bin/python -m mypy && .venv/bin/python -m ruff check src tests && .venv/bin/python -m ruff format --check src tests)` and `(cd src/api && PYTHONPATH=../core/tests:../agents/tests .venv/bin/python -m mypy && .venv/bin/python -m ruff check src tests && .venv/bin/python -m ruff format --check src tests)` (falling back to `python3 -m` only if `.venv/bin/python` is unavailable; if `--isolated` is retained as an extra check, scope it strictly to `heldout_eval.py`, `tokenomics_comparison.py`, and the 3 branch test files, never `server.py` or `src tests`).
* Action owner: planning parent (`rpi-plan`)
* Exact resolving evidence: Updated validation commands in .copilot-tracking/plans/2026-11-15/ai-108-heldout-eval-c1-plan.md (`NFR-1`) and .copilot-tracking/details/2026-11-15/ai-108-heldout-eval-c1-phase-details.md (`P04`, `P04-T01`) that preserve pyproject.toml exclusions and `src/api` `mypy` import paths.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: SHA-256 hex digests inside `snap["sources"]` pollute grounded digit extraction in `_check_statement_support()`

* Related IDs: FR-5, P02, P02-T02, P04-T01
* Evidence: .copilot-tracking/details/2026-11-15/ai-108-heldout-eval-c1-phase-details.md (`P02-T02`), src/core/src/zava_forward/core/heldout_eval.py (`_base_case_record`), src/core/src/zava_forward/core/assistants.py (`capture`)
* Concern: `P02-T02` constructs `grounded_corpus` in `_evaluate_assistant_case()` from `json.dumps({"case_id": fixture["record"]["id"], "sources": snap["sources"], "citations": list(snap["citations"].keys())}, sort_keys=True)` and extracts grounded numbers via `set(re.findall(r"\d+", grounded_corpus))`. However, `assistants.capture()` embeds up to five 64-character SHA-256 hex digests per assistant snapshot (`survey.evidence_hash`, `funding.terms_hash`, `documents[*].content_sha256`, `finance.invoices[*].evidence_hash`). Across up to 320 hexadecimal characters, `re.findall(r"\d+", ...)` extracts dozens of incidental 1-, 2-, and 3-digit substrings (frequently including probe numbers like `99` or `45`), causing ungrounded numeric claims in assistant outputs to be misclassified as grounded. In addition, `r"\bZF-[A-Za-z0-9-]+\b"` is less precise at trailing punctuation boundaries than `r"\bZF-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*\b"`.
* Impact: Hallucinated numeric claims in assistant summaries and findings can silently pass `_check_statement_support()` with `unsupported_claims == 0`, defeating Finding 4 remediation and risking false passes in `P04-T01` tests.
* Smallest useful change: Update `P02-T02` so `_check_statement_support()` strips 64-character hexadecimal digests (`re.sub(r"\b[0-9a-f]{64}\b", " ", grounded_corpus, flags=re.IGNORECASE)`) from `grounded_corpus` before extracting grounded `\d+` tokens, and uses `r"\bZF-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*\b"` (case-insensitive) for `ZF-*` identifier extraction and stripping.
* Action owner: planning parent (`rpi-plan`)
* Exact resolving evidence: `P02-T02` in .copilot-tracking/details/2026-11-15/ai-108-heldout-eval-c1-phase-details.md explicitly strips 64-char hex digests from `grounded_corpus` prior to `\d+` token collection and uses the non-trailing-hyphen `ZF-*` pattern.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Baseline `manifest_digest` error behavior breaks existing unfrozen-manifest test and `_extract_candidate_metrics` omits response-branch `gate_failures`

* Related IDs: FR-4, AC-4, AC-5, P03, P03-T01, P04-T01
* Evidence: .copilot-tracking/details/2026-11-15/ai-108-heldout-eval-c1-phase-details.md (`P03-T01`, `P04-T01`), src/core/src/zava_forward/core/tokenomics_comparison.py (`_extract_candidate_metrics`, `compare_candidates`), src/core/tests/test_tokenomics_comparison.py (`test_unfrozen_manifest_or_prompt_leak_fails_all_candidates`)
* Concern: Three implementation hazards arise in `P03-T01` and `P04-T01`: (1) `test_tokenomics_comparison.py` lines 241-245 mutate `tampered["versions"]["source"] = "mutated-without-reapproval"` on a copy of `manifest` and assert `compare_candidates(tampered, baseline, [good_cand])` returns `suite_valid is False` and `is_saving is False` (`0` test removals allowed by `AC-5`). Mutating `tampered` changes `freeze["manifest_digest"]` (`manifest_body_digest(tampered)`) while `tampered["threshold_approval"]["manifest_digest"]` still equals `baseline["manifest_digest"]`; raising `ValueError` unconditionally whenever `baseline.get("manifest_digest") != freeze["manifest_digest"]` crashes that test before `suite_blockers` can report `suite_valid=False`. (2) `P03-T01` adds `"gate_failures"` only to the summary-only return dict of `_extract_candidate_metrics()` without adding `"gate_failures"` to the `responses`-backed return dict, risking `KeyError: 'gate_failures'` in `compare_candidates()`, does not require `rai_release.named(gf)` on each summary `gate_failures` entry (allowing `[""]`), and omits `evaluation_outcome`, `accepted_case_ids`, and `gate_failures` from the summary `evaluation_digest`. (3) `P04-T01` states "Update existing valid summary-only test fixtures", whereas existing negative summary-only comparison fixtures in `test_tokenomics_comparison.py` (Tests 2, 3, 4, 5, 7, 8) and `test_heldout_eval_api.py` (`cheap-regresses-overrides`) also omit `responses` and need explicit `evaluation_outcome` and `gate_failures` so they reach candidate regression evaluation rather than raising `ValueError` early.
* Impact: Unadjusted `P03-T01` and `P04-T01` steps will break existing `test_tokenomics_comparison.py` tests, risk `KeyError` on response-backed candidates, and leave blank-string `gate_failures` and summary `evaluation_digest` collisions open.
* Smallest useful change: Revise `P03-T01` and `P04-T01` so that: (a) `_validate_baseline_artifact()` raises `ValueError` when `baseline.get("manifest_digest")` is missing/blank or when `baseline["manifest_digest"] != freeze["manifest_digest"]` on a validly frozen manifest (`freeze["frozen"]` is `True` or `baseline["manifest_digest"] != approval.get("manifest_digest")`), while appending `"baseline_manifest_digest_mismatch"` to `suite_blockers` when `not freeze["frozen"]` due to post-approval manifest mutation; (b) `_extract_candidate_metrics()` returns `"gate_failures"` in both its `responses` and summary branches, validates every summary `gate_failures` item with `rai_release.named`, and includes `evaluation_outcome`, `sorted(accepted_ids)`, and `gate_failures` in the summary `evaluation_digest`; and (c) `P04-T01` updates all existing non-schema-error summary fixtures (passing and regression cases alike) in `test_tokenomics_comparison.py` and `test_heldout_eval_api.py` with explicit `evaluation_outcome` and `gate_failures`.
* Action owner: planning parent (`rpi-plan`)
* Exact resolving evidence: Revised `P03-T01` and `P04-T01` sections in .copilot-tracking/details/2026-11-15/ai-108-heldout-eval-c1-phase-details.md (and `FR-4` in .copilot-tracking/plans/2026-11-15/ai-108-heldout-eval-c1-plan.md) incorporating all three safeguards.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Exact `"capability_version_drift"` blocker token compatibility and bare-string sequence bypass on candidate `rendered_prompts`

* Related IDs: FR-3, FR-4, P02-T01, P03-T01
* Evidence: .copilot-tracking/plans/2026-11-15/ai-108-heldout-eval-c1-plan.md (`FR-3`, `FR-4`), .copilot-tracking/details/2026-11-15/ai-108-heldout-eval-c1-phase-details.md (`P02-T01`, `P03-T01`), src/core/src/zava_forward/core/tokenomics_comparison.py (`_extract_candidate_metrics`, `compare_candidates`), src/api/src/zava_forward/api/server.py (`POST /api/ai/candidate-comparison`)
* Concern: Two contract-hardening gaps remain: (1) Caller Requirement 3 asks to `append "capability_version_drift" to blockers when prompt/policy/task versions differ without an explicit re-freeze`, whereas `P02-T01` appends only `f"capability_version_drift:{','.join(drifted)}"`; exact membership checks (`"capability_version_drift" in freeze["blockers"]`) fail unless `"capability_version_drift"` is also appended. (2) `P03-T01` item 5 unpacks optional `candidate.get("rendered_prompts")` (and top-level `rendered_prompts` / `tuning_examples`) into `check_prompt_tuning_isolation(...)`, and `server.py` validates only top-level `body["rendered_prompts"]`, not per-candidate `rendered_prompts`. Because a Python `str` is a `Sequence[str]`, passing `"rendered_prompts": "HO-AST-FE-02"` on a candidate iterates single characters (`"H"`, `"O"`, ...) and completely bypasses case-ID and 6-word shingle leak detection. Similarly, on summary candidates where a non-offline `actual_serving_version` is supplied without `expected_serving_version`, comparing against `cand_levers["model"]` closes undeclared model-serving drift.
* Impact: Malformed string-typed per-candidate `rendered_prompts` or omitted `expected_serving_version` on non-offline summary candidates can bypass `holdout_leakage_clear` or serving-version verification, and exact `"capability_version_drift"` checks would miss the suffixed-only token.
* Smallest useful change: In `P02-T01`, append both `"capability_version_drift"` and `f"capability_version_drift:{','.join(drifted)}"` to `blockers` when `manifest["capability_versions"]` differs from live `_capability_version_snapshot()`. In `P03-T01`, reject `str | bytes | bytearray` (requiring sequences of strings, or strings/mappings for `tuning_examples`, else raising `ValueError`) for both top-level and per-candidate `rendered_prompts` and `tuning_examples`, and check non-offline summary `actual_serving_version` against `expected_serving_version` when set or `cand_levers["model"]` otherwise.
* Action owner: planning parent (`rpi-plan`)
* Exact resolving evidence: Updated `P02-T01` and `P03-T01` in .copilot-tracking/details/2026-11-15/ai-108-heldout-eval-c1-phase-details.md and `FR-3`/`FR-4` in .copilot-tracking/plans/2026-11-15/ai-108-heldout-eval-c1-plan.md recording exact `"capability_version_drift"` blocker inclusion, non-string sequence validation on prompt/tuning inputs, and non-offline summary serving-model verification.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Rebase analysis (`Q1`, `P01-T01`) accurately identifies the exact `GET /api/ai/report` intersection with parent commit `7f83f4749` (`chat_eval.run_eval()`) across `server.py`, `src/api/README.md`, and `test_heldout_eval_api.py`.
* False-positive auditing (`Q5`, `P02-T02`) proactively caught canonical fixture nuances (`pas2035-v2` vs `PAS 2035` and `2026-10-25T08:00:00Z` vs `08:00Z`) before implementation.
* Immutable model candidate evaluation via `expected_serving_model` (`P02-T01`, `P03-T01`) cleanly eliminates dynamic manifest mutation and approval forgery without breaking single-lever model experiments.
* Explicitly accepted residual risk: Offline synthetic fixtures and deterministic tariffs provide engineering verification only and do not establish live Azure OpenAI benchmarks, regional quota attestation, human participant studies, or OQ-018 fairness clearance (tracked under `## Follow-Up Items`).

## Questions or Blocking Evidence Gaps

* None. All four findings have deterministic, repository-verified planner resolutions requiring no user input.

## Limitations

* Critique was performed read-only on `18dc9d132` prior to executing `git rebase origin/feat/demo-164-chat-grounding-provenance-0900` (`7f83f4749`), relying on the verified parent diff evidence recorded in .copilot-tracking/research/2026-11-15/ai-108-heldout-eval-c1-research.md (`C1`).

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning parent
* Smallest next action: Apply direct planner revisions for `PC-001` through `PC-004` in .copilot-tracking/plans/2026-11-15/ai-108-heldout-eval-c1-plan.md and .copilot-tracking/details/2026-11-15/ai-108-heldout-eval-c1-phase-details.md, record their dispositions, and finalize the plan for `rpi-implement` without another critique pass.
* User response required: no
