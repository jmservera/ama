<!-- markdownlint-disable-file -->
# Review: Offline RAI Held-Out Evaluation and Tokenomics Candidate Comparison (Issue #108)

## Scope and Evidence

* Task ID: issue-108-heldout-eval-tokenomics
* Review date: 2026-11-15
* Review scope: Full task (`P01`, `P02`, `P03`, `P04`)
* Assessed boundary: Offline RAI Held-Out evaluation (`zava_forward.core.heldout_eval`), Tokenomics candidate/single-lever comparator (`zava_forward.core.tokenomics_comparison`), manager-only API routes (`GET /api/ai/heldout-evaluation`, `POST /api/ai/candidate-comparison`, `GET /api/ai/report` summaries), role-endpoint inventory, unit tests, strict typing, and offline-scope documentation in `src/core` and `src/api`.
* Plan: .copilot-tracking/plans/2026-11-15/ai-108-heldout-eval-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/ai-108-heldout-eval-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/ai-108-heldout-eval-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/ai-108-heldout-eval-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/ai-108-heldout-eval-research.md (`C1`–`C18`), worktree `git diff`, and newly created modules/tests in `src/core` and `src/api`.

## Opening Review State

* Interpreted review goal: Independently verify that the full `P01`–`P04` implementation satisfies all three offline RAI Held-Out and Tokenomics comparison acceptance criteria for Issue #108, honors critique dispositions `PC-001` through `PC-006`, reconciles plan/detail/change artifacts, and preserves existing `src/core` and `src/api` governance gates.
* Review scope: Full task (`P01`, `P02`, `P03`, `P04`)
* Evidence readiness: Ready — plan markers (`P01`–`P04`), phase details, critique dispositions, changes record, and validation results (`unittest`, `ruff check`, `ruff format --check`, `mypy`) are complete and reconciled.
* Acceptance basis: `FR-1` through `FR-5`, `NFR-1`, `NFR-2`, `AC-1` through `AC-5`, and resolved critique findings `PC-001` through `PC-006` in .copilot-tracking/plans/2026-11-15/ai-108-heldout-eval-plan.md.
* First comparison boundary: Reconcile `P01`–`P04` plan markers and critique dispositions against `src/core` and `src/api` implementation files, tests, and validation logs without modifying source or upstream tracking artifacts.
* Active read-only boundaries: Read-only across repository source, tests, documentation, research, plan, phase details, critique, and changes record; write access restricted solely to `.copilot-tracking/reviews/logs/2026-11-15/ai-108-heldout-eval-review.md` and RPI session state.
* Initial blockers: None

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed full-boundary post-implementation comparison on 2026-11-15 across `.copilot-tracking/plans/2026-11-15/ai-108-heldout-eval-plan.md`, `.copilot-tracking/details/2026-11-15/ai-108-heldout-eval-phase-details.md`, `.copilot-tracking/reviews/plans/2026-11-15/ai-108-heldout-eval-plan-critique.md`, `.copilot-tracking/changes/2026-11-15/ai-108-heldout-eval-changes.md`, `.copilot-tracking/research/2026-11-15/ai-108-heldout-eval-research.md`, and the `src/core` and `src/api` source, test, configuration, and README diffs, augmented by an independent read-only adversarial `rubber-duck` lens.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`, `P01-T02`) | Core Held-Out Freeze, Prompt/Tuning Isolation, and 11-Capability Evaluator | Reconciled | Checked in plan and documented in changes record with `heldout_eval.py` and `src/core/pyproject.toml` completion evidence. |
| `P02` (`P02-T01`) | Core Tokenomics Candidate and Single-Lever Comparator | Reconciled | Checked in plan and documented in changes record with `tokenomics_comparison.py` completion evidence. |
| `P03` (`P03-T01`) | API Endpoints, Report Integration, and Route Inventory | Reconciled | Checked in plan and documented in changes record with `server.py` and `test_role_endpoint_inventory.py` completion evidence. |
| `P04` (`P04-T01`, `P04-T02`) | Focused Unit Tests, Documentation, and Verification | Reconciled | Checked in plan and documented in changes record with `test_heldout_eval.py`, `test_tokenomics_comparison.py`, `test_heldout_eval_api.py`, `src/api/pyproject.toml`, `src/core/README.md`, and `src/api/README.md` evidence. |
| `## Follow-Up Items` | Live Azure OpenAI held-out batch + regional quota attestation; human participant + OQ-018 owner sign-off | Reconciled | Preserved outside active `P01`–`P04` markers in both the plan and changes record. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01` (`P01-T01`, `P01-T02`) | `src/core/src/zava_forward/core/heldout_eval.py`, `src/core/pyproject.toml` | Delivered frozen manifest validation, prompt/tuning isolation across all 5 registered assistants (`stock-prioritisation`, `assessment-preparation`, `works-resident-coordination`, `funding-evidence`, `quality-evidence`) and all 6 retained legacy families (`message`, `summary`, `briefing`, `priority`, `funding_draft`, `read_document`), and 16-case offline evaluator across controls, ambiguity, abstention, source integrity, and factual support; configured narrow `mypy` override. | 16/16 canonical suite passes offline with hashes, split/seed, denominators, unaveraged subgroup results (`SYNTHETIC_NON_FAIRNESS_NOTICE`), `actual_serving_version`, usage, unknown liabilities, reviewer protocol, and calibration `not_applicable`. | Passed (`test_heldout_eval.py`, `ruff check`, `ruff format --check`, `mypy`). | Implemented; hardening gaps recorded in `RV-001`, `RV-003`, and `RV-004`. |
| `P02` (`P02-T01`) | `src/core/src/zava_forward/core/tokenomics_comparison.py` | Delivered quality-gated candidate comparator failing cheaper candidates that regress `critical_misses`, `unsupported_claims`, `overrides`, `reopened_cases`, `critical_errors`, or accepted case outcomes, and enforcing single-lever (`model`, `routing`, `caching`, `prompt`) attribution on identical held-out cases with exact `Decimal` deltas. | Canonical 3-candidate offline comparison rejects cheaper quality-regressing and multi-lever candidates (`is_saving=False`) and accepts single-lever caching (`is_saving=True`). | Passed (`test_tokenomics_comparison.py`, `ruff check`, `ruff format --check`, `mypy`). | Implemented; summary-input/provenance hardening gaps recorded in `RV-002`. |
| `P03` (`P03-T01`) | `src/api/src/zava_forward/api/server.py`, `src/api/tests/test_role_endpoint_inventory.py` | Wired manager-only (`MANAGER_ROLES`) `GET /api/ai/heldout-evaluation`, `POST /api/ai/candidate-comparison` (with 4-arg `s.audit`), `get_kind(path)` `"ai_report"` classification, `GET /api/ai/report` compact summaries, and role-endpoint inventory coverage. | Both routes enforce `MANAGER_ROLES`, reject query strings (`400`), preserve `GET /api/ai/report` top-level keys, and pass role/call-site/dependency inventories. | Passed (`test_role_endpoint_inventory.py`, `test_ai_call_site_inventory.py`, `test_dependency_rule.py`). | Reconciled and conformant with `PC-001` and `server.py` manager-tier conventions. |
| `P04` (`P04-T01`, `P04-T02`) | `src/core/tests/test_heldout_eval.py`, `src/core/tests/test_tokenomics_comparison.py`, `src/api/tests/test_heldout_eval_api.py`, `src/api/pyproject.toml`, `src/core/README.md`, `src/api/README.md` | Added 27 focused unit/HTTP tests across `src/core` and `src/api`, added `test_heldout_eval_api` typing override, and documented offline scope and live-boundary disclaimers in both READMEs with zero `.copilot-tracking/` references. | All focused unit tests, doc-link/cutover tests, `ruff check`, `ruff format --check`, and `mypy` succeeded (`exit code 0`). | Passed (`42` + `11` core tests, `114` API tests, `ruff`, `mypy`). | Reconciled; follow-on tests for `RV-001`–`RV-004` routed with their implementation items. |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P01-T01` (`Implementation-Time Plan and Detail Updates` in changes record) | Used `ai_prompts.PROMPTS` (the actual dictionary symbol in `zava_forward.core.ai_prompts`) when verifying and rendering the 6 legacy prompt templates in `heldout_eval._render_registered_prompt_corpus()`. | Local code inspection during `P01-T01`; no user decision required because approved intent (rendering all 6 registered legacy templates) is unchanged. | Recorded in `.copilot-tracking/changes/2026-11-15/ai-108-heldout-eval-changes.md` under `## Implementation-Time Plan and Detail Updates` (note: implementation iterates `sorted(LEGACY_FAMILIES)` and checks membership in `ai_prompts.PROMPTS`). | Not needed (ordinary local judgment preserving architecture and scope). | Reconciled; preserves confirmed user intent. |

## Critique and Material Revision Assessment

* Latest critique dispositions: All six planner critique findings (`PC-001` through `PC-006`) in `.copilot-tracking/reviews/plans/2026-11-15/ai-108-heldout-eval-plan-critique.md` are recorded and marked `Resolved` in `.copilot-tracking/plans/2026-11-15/ai-108-heldout-eval-plan.md` (`## Critique Disposition`).
* Material revisions: None occurred during implementation; no second critique was run or required.
* Dependent-work pause assessment: No dependent phase executed out of order or bypassed a paused decision gate.
* Justification assessment: `PC-001`, `PC-002`, and `PC-006` are fully satisfied in implementation; `PC-003`, `PC-004`, and `PC-005` are implemented for canonical and response-backed flows, with adversarial bypasses on runtime digest pinning, summary-only candidate payloads, and extra ungrounded claims captured in `RV-001`–`RV-003`.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Owner-authorized live Azure OpenAI held-out batch execution and regional quota attestation for Issue #108 | Live model invocations require explicit spend authorization and deployed Azure OpenAI regional endpoints outside offline synthetic scope. | Repository owner / operator action on Issue #108 once spend and deployed model endpoints are authorized. | Open distinct follow-up route (not an active-plan defect). |
| Human staff participant effectiveness evaluation and OQ-018 cohort owner sign-off for Issue #108 | Scripted offline harnesses and role agents cannot substitute for named human staff participants or DPO/RAI owner approvals. | Repository owner / programme lead action on Issue #108. | Open distinct follow-up route (not an active-plan defect). |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Canonical manifest signs live code versions dynamically instead of pinning a frozen approval digest and checking active-code drift

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/heldout_eval.py` (`check_heldout_freeze`, `canonical_heldout_manifest`); `src/core/src/zava_forward/core/tokenomics_comparison.py` (`_manifest_for_candidate_model`)
* Impact: `approve_manifest` and `check_heldout_freeze` detect post-approval edits to an already-constructed manifest dict, but `canonical_heldout_manifest()` calls `approve_manifest(...)` at runtime from live `assistants.REGISTRY` and `ai_prompts.version(...)` values instead of asserting a pinned static `thresholds_digest` / `manifest_digest` constant, and `check_heldout_freeze` does not verify that a frozen manifest's `capability_versions` still match the executing prompt/policy/task versions unless explicitly opted into a candidate-lever override.
* Destination: `rpi-implement`
* Smallest useful next action: Pin the canonical approved `thresholds_digest` and `manifest_digest` constants in `heldout_eval.py`, compare `manifest["capability_versions"]` against live registered prompt/task/policy versions in `check_heldout_freeze` (allowing only an explicit single-lever candidate override in `tokenomics_comparison`), and add a negative regression test mutating a registered prompt version.

<!-- rpi:review id=RV-002 -->
### RV-002 [High]: Summary-only candidate comparison payloads allow unverified evaluation status, unchecked candidate prompt text, unbound baseline digests, and cross-currency subtraction

* Related scope: `P02-T01`, `P03-T01`
* Evidence: `src/core/src/zava_forward/core/tokenomics_comparison.py` (`_validate_baseline`, `_extract_candidate_metrics`, `compare_candidates`)
* Impact: When a candidate omits `responses` and supplies pre-aggregated summary fields (including via `POST /api/ai/candidate-comparison`), `_extract_candidate_metrics` defaults missing `evaluation_outcome` to `"pass"` and missing `accepted_case_ids` to `case_ids`, accepts `estimated_cost` without requiring token counts or matching `usage.currency` against `baseline.usage.currency`, checks `actual_serving_version` only when `expected_serving_version` is provided, does not pass candidate `lever_config["prompt"]` / per-candidate prompts through `check_prompt_tuning_isolation`, and does not verify `baseline["manifest_digest"] == freeze["manifest_digest"]`.
* Destination: `rpi-implement`
* Smallest useful next action: Bind `baseline["manifest_digest"]` and `seed` to the frozen manifest, enforce `currency` parity and explicit `evaluation_outcome == "pass"` plus explicit `accepted_case_ids` and serving-version matching against `cand_levers["model"]` (when non-offline), scan candidate `lever_config["prompt"]` and candidate prompt/tuning fields with `check_prompt_tuning_isolation`, and add negative unit/API tests.

<!-- rpi:review id=RV-003 -->
### RV-003 [Medium]: Offline factual-support check verifies citation resolution and required grounded tokens but does not reject injected unsupported numeric/factual claims alongside a valid citation

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/heldout_eval.py` (`_evaluate_assistant_case`, `_evaluate_legacy_case`)
* Impact: Appending an invented factual or numeric claim (for example an ungrounded count or hazard assertion) to a response that still includes the valid citation locator and required substrings can pass `factual_support` with `unsupported_claims == 0`.
* Destination: `rpi-implement`
* Smallest useful next action: Cross-check numeric tokens and case/identifier tokens in candidate outputs against the serialized frozen case source snapshot (incrementing `unsupported_claims` and recording an `ungrounded_claim` critical error on mismatch) and add a negative test case.

<!-- rpi:review id=RV-004 -->
### RV-004 [Low]: `evaluate_heldout` executes per-case scoring before returning `outcome="insufficient"` when cohort sample floors fail

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/heldout_eval.py` (`evaluate_heldout`)
* Impact: Unmet sample floors still produce `outcome == "insufficient"` (never `"pass"`), but gating case scoring on `freeze["ready_for_evaluation"]` (or short-circuiting before per-case scoring when `not freeze["sample_sufficient"]`) makes the pre-evaluation sample-sufficiency gate strict before evaluation runs.
* Destination: `rpi-implement`
* Smallest useful next action: Short-circuit per-case scoring in `evaluate_heldout` when `not freeze["sample_sufficient"]` while still returning full freeze/isolation/denominator diagnostics and `outcome == "insufficient"`.

## Defects

* `RV-001` [High] -> `rpi-implement`
* `RV-002` [High] -> `rpi-implement`
* `RV-003` [Medium] -> `rpi-implement`
* `RV-004` [Low] -> `rpi-implement`

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | `rpi-implement` | Pin frozen canonical manifest digests and enforce live capability-version drift detection in `heldout_eval.py`. | Implementation hardening defect within approved architecture. |
| `RV-002` | `rpi-implement` | Harden `tokenomics_comparison.py` baseline-digest binding, currency parity, candidate prompt-lever isolation, and summary-payload verification. | Implementation hardening defect within approved architecture. |
| `RV-003` | `rpi-implement` | Reject ungrounded numeric/identifier claims against frozen case source text in `heldout_eval.py`. | Implementation hardening defect within approved architecture. |
| `RV-004` | `rpi-implement` | Gate per-case scoring on `freeze["sample_sufficient"]` before scoring held-out responses in `heldout_eval.py`. | Minor pre-evaluation gating refinement within approved architecture. |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Owner-authorized live Azure OpenAI held-out batch execution and regional quota attestation for Issue #108 (outside offline synthetic scope; owner/operator action).
* Human staff participant effectiveness evaluation and OQ-018 cohort owner sign-off for Issue #108 (outside offline synthetic scope; owner/programme lead action).

## Blockers and Remaining Work

* Blockers: None
* Remaining active work: None in `P01`–`P04`; routed findings `RV-001`–`RV-004` are queued for a follow-up `rpi-implement` task if selected.

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `PYTHONPATH=tests .venv/bin/python -m unittest -q tests/test_heldout_eval.py tests/test_tokenomics_comparison.py tests/test_dependency_rule.py tests/test_ai_register_completeness.py tests/test_rai_threshold_live_approval_guard.py` | `src/core` | Passed | Ran 42 tests in 3.392s (`OK`) |
| `PYTHONPATH=tests .venv/bin/python -m unittest -q tests/test_live_doc_links.py tests/test_cutover_audit.py` | `src/core` | Passed | Ran 11 tests in 4.797s (`OK`) |
| `.venv/bin/python -m ruff check && .venv/bin/python -m ruff format --check && .venv/bin/python -m mypy` | `src/core` | Passed | `All checks passed!`, `285 files already formatted`, `Success: no issues found in 338 source files` |
| `PYTHONPATH=../core/tests:../agents/tests:tests .venv/bin/python -m unittest -q tests/test_heldout_eval_api.py tests/test_ai_tasks.py tests/test_eval_candidate_regression_gate.py tests/test_role_endpoint_inventory.py tests/test_ai_call_site_inventory.py tests/test_dependency_rule.py` | `src/api` | Passed | Ran 114 tests in 55.823s (`OK`) |
| `.venv/bin/python -m ruff check && .venv/bin/python -m ruff format --check && PYTHONPATH=../core/tests:../agents/tests .venv/bin/python -m mypy` | `src/api` | Passed | `All checks passed!`, `197 files already formatted`, `Success: no issues found in 281 source files` |

## Outcome

* Outcome: Defects found
* Outcome rationale: Planned phases `P01`–`P04` executed completely and pass all 167 unit/doc/inventory tests, `ruff check`, `ruff format --check`, and strict `mypy` across `src/core` and `src/api`, delivering the 11-capability offline held-out harness, Tokenomics comparator, and manager API endpoints; however, independent adversarial review identified four hardening defects (`RV-001` through `RV-004`) where dynamic canonical signing, summary-only candidate payloads, ungrounded extra numeric claims, or pre-scoring sample gates can be tightened in a follow-up `rpi-implement` pass. Per stop rules, a conformant outcome is withheld while material findings remain open.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | `rpi-implement` | Harden pinned manifest digest / active-code drift (`RV-001`), summary-candidate provenance/currency/prompt-lever checks (`RV-002`), ungrounded numeric claim detection (`RV-003`), and pre-scoring sample-floor short-circuit (`RV-004`). |
| Decision gap or invalid assumption | None | None |
| Material evidence gap | None | None |
| Non-blocking residual work | Distinct follow-up on Issue #108 | Owner-authorized live Azure OpenAI held-out batch + regional quota attestation; human staff participant + OQ-018 cohort owner sign-off. |

* Execution status: Complete
* Outcome: Defects found
* Validation coverage: Complete focused test, linter, formatter, and strict typecheck coverage passed in `src/core` and `src/api` (`exit code 0`)
* Blockers: None
