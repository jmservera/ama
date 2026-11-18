<!-- markdownlint-disable-file -->
# RPI Phase Details: Offline RAI Held-Out Evaluation and Tokenomics Candidate Comparison (Issue #108)

## Metadata

* Task ID: issue-108-heldout-eval-tokenomics
* Task slug: ai-108-heldout-eval
* Related plan: .copilot-tracking/plans/2026-11-15/ai-108-heldout-eval-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/ai-108-heldout-eval-research.md, docs/prds/zava-forward-retrofit-programme-demonstrator.md, docs/reference/resources/ai-tokenomics.md

## Phase Index

| Phase ID | Name                                                                             | Status | Detail sections          |
|----------|----------------------------------------------------------------------------------|--------|--------------------------|
| P01      | Core Held-Out Freeze, Prompt/Tuning Isolation, and 11-Capability Offline Evaluator | Ready  | P01, P01-T01, P01-T02    |
| P02      | Core Tokenomics Candidate and Single-Lever Comparator                            | Ready  | P02, P02-T01             |
| P03      | API Endpoints, Report Integration, and Route Inventory                           | Ready  | P03, P03-T01             |
| P04      | Focused Unit Tests, Documentation, and Verification                              | Ready  | P04, P04-T01, P04-T02    |

<!-- rpi:phase id=P01 -->
## P01: Core Held-Out Freeze, Prompt/Tuning Isolation, and 11-Capability Offline Evaluator

### Context

`src/core` owns all five proposal-only assistants (`assistants.REGISTRY` / `ai_registry.ASSISTANTS`) and all six retained legacy task families (`ai_registry.LEGACY`: `briefing`, `message`, `summary`, `priority`, `funding_draft`, `read_document`), while `src/core/tests/test_dependency_rule.py` (`C1`) enforces `ALLOWED = {"core"}`. Existing `src/agents` scripts (`C6`, `C7`) neither cover the five core assistants nor enforce prompt/tuning answer isolation inside `core`.

### Intent

Build `zava_forward.core.heldout_eval` as a pure, deterministic, provider-free module that validates pre-evaluation freeze and prompt/tuning answer isolation before scoring, runs offline held-out evaluation across all 11 retained capabilities and 5 control/grounding dimensions, and produces complete RAI/operational reporting with explicit calibration non-applicability when scored probability predictions are absent.

### Boundaries

* Included: `src/core/src/zava_forward/core/heldout_eval.py` and `src/core/pyproject.toml` mypy override entry.
* Excluded: Network calls, provider URL fragments (`C17`), imports from `zava_forward.agents` or `zava_forward.api` (`C1`), or changes to live runtime behavior of `Store` or `Assistants`.

### Likely Targets

* `src/core/src/zava_forward/core/heldout_eval.py`: New module implementing freeze validation, prompt/tuning answer isolation, 11-capability evaluation, and canonical synthetic offline suite.
* `src/core/pyproject.toml`: Narrow `disallow_untyped_calls = false` entry for `zava_forward.core.heldout_eval` and its tests calling legacy untyped `core` modules.

### Dependencies

* None (`core` stdlib + existing `zava_forward.core` modules).

### Validation Expectations

* `ruff check`, `ruff format --check`, `mypy`, `test_dependency_rule.py`, and `test_heldout_eval.py` in `src/core`.

### Completion Evidence

* `canonical_offline_heldout_suite()` deterministically evaluates all 5 assistants and all 6 retained legacy families with `frozen=True`, `prompt_tuning_isolated=True`, complete hashes/denominators/subgroups/liabilities/protocol/calibration-NA fields, and fail-closed transitions on freeze, leakage, control, or grounding faults.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Implement `src/core/src/zava_forward/core/heldout_eval.py`

#### Context

Issue #108 Criteria 1 and 2 require:
1. Pre-evaluation freeze of `task`, `model`, `prompt`, `policy`, and `source` versions, an independently labelled held-out split (`labelled_by` distinct from `prompt_author`), deterministic `seed`, expected outcomes, critical error rules, cohorts with `min_n` sample floors, and digest-bound `threshold_approval` before evaluation begins, plus strict verification that held-out answers never enter rendered prompts or tuning examples.
2. Offline held-out coverage across all 5 assistants (`stock-prioritisation`, `assessment-preparation`, `funding-evidence`, `works-resident-coordination`, `quality-evidence`) and all 6 retained legacy families (`briefing`, `message`, `summary`, `priority`, `funding_draft`, `read_document`), testing correct controls, ambiguity, abstention, source integrity, and factual support, and recording `critical_errors`, `critical_misses`, `usable_coverage`, `subgroup_results`, `hashes`, `split`, `seed`, `denominators`, `actual_serving_version`, `usage`, `unknown_liabilities`, `reviewer_protocol`, `outcome` (`pass` / `fail` / `insufficient`), and `calibration` (`not_applicable` when meaningful scored probability predictions are absent).

#### Intent

Create `heldout_eval.py` with clean, composable pure functions and a deterministic canonical synthetic suite exercising real `core` prompt builders and output/citation/consent/hazard validators.

#### Boundaries

* Included:
  * `REQUIRED_ASSISTANTS` (derived/verified against `ai_registry.ASSISTANTS`) and `REQUIRED_LEGACY_FAMILIES` (derived/verified against `ai_registry.LEGACY`).
  * `REQUIRED_DIMENSIONS = ("controls", "ambiguity", "abstention", "source_integrity", "factual_support")`.
  * `approve_manifest(manifest, *, approved_by, approved_at)` and `check_heldout_freeze(manifest, *, require_all_capabilities=True, live=False)`: checks suite and per-capability `versions` (`task`, `model`, `prompt`, `policy`, `source`), held-out split (`split_id`, `seed`, deduplicated `case_ids`, `denominator == len(case_ids)`, named-human `labelled_by` != `prompt_author`), per-case categorical `expected_outcome` + `>= 6`-word `expected_answer` prose + `cohort` + `capability` + `dimension`, `critical_errors` catalog, `cohorts` sample floor sufficiency (`n >= min_n`), disjointness against `prompt_case_ids` / `tuning_case_ids` / `calibration_case_ids`, `threshold_approval` binding both `thresholds_digest` and full `manifest_digest` (manifest excluding `threshold_approval`) with named-human `approved_by` and ISO-8601 `approved_at`, and rejection of `synthetic=True` manifests when `live=True`.
  * `check_prompt_tuning_isolation(manifest, *, rendered_prompts=(), tuning_examples=())`: renders all 5 assistants via `assistants.build_request` on synthetic non-held-out snapshots and all 6 `ai_prompts.TEMPLATES` entries via `ai_prompts.render` with task-specific synthetic non-held-out kwargs (`facts`, `owner`, `n`, `route`, `missing`, `name`) plus `ai_tasks.cite_instruction(...)`, alongside caller-supplied `rendered_prompts` and `tuning_examples`, failing closed if any held-out `case_id` or `>= 6`-word `expected_answer` prose (exact substring or normalized `>= 6`-word shingle overlap; never 1-word categorical `expected_outcome` enum tokens) appears in prompts or tuning material.
  * `evaluate_heldout_suite(manifest, responses, *, tuning_examples=(), extra_prompts=())`: runs `check_heldout_freeze` and `check_prompt_tuning_isolation` first; evaluates each assistant case through `assistants.capture`, `assistants.eligible`, `assistants.validate_output`, `assistants.shape_result`, `assistants.review_flag`, and `ai.FORBIDDEN`, and each legacy family case through `ai_tasks.statement_sources`, `ai_tasks.priority_items`, `ai_tasks.critical_misses`, `ai.FORBIDDEN`, document cleanliness/consent/abstention rules, and source snapshot hash checks; computes per-case, per-capability, per-dimension, and per-cohort (`subgroup_results`, unaveraged, carrying `cohort_eval.SYNTHETIC_NON_FAIRNESS_NOTICE`) outcomes (`pass` / `fail` / `insufficient`), `usable_coverage`, `hashes`, `split`, `seed`, `denominators`, `actual_serving_version` (detecting serving model version mismatches vs manifest and labelling offline scripted fixtures `"unattested (offline scripted fixture)"`), `usage`, `unknown_liabilities` (explicitly tracking missing/invalid usage, unpriced calls, or unsettled reservations without zeroing them), `reviewer_protocol`, structured `baseline_candidate` payload (`baseline_id`, `lever_config`, `case_ids`, `accepted_case_ids`, `manifest_digest`, `seed`, quality counts, usage, unit prices) for Tokenomics comparisons, and `calibration` (`status: "not_applicable"` with explicit rationale when scored probability predictions are absent, or empirical Brier/bin summary only if genuine `[0, 1]` probability predictions exist).
  * `canonical_offline_heldout_suite()`: builds a deterministic synthetic dataset, frozen manifest (>= 22 held-out cases covering all 11 capabilities, all 5 dimensions, and >= 3 synthetic cohorts meeting `min_n`), and scripted responses so `src/core` and `src/api` can execute and audit the full harness offline in milliseconds.
* Excluded: Live HTTP requests or modifications to `Store` persistent tables.

#### Likely Targets

* `src/core/src/zava_forward/core/heldout_eval.py`: Primary implementation file.

#### Dependencies

* `zava_forward.core.{ai,ai_consumption,ai_prompts,ai_registry,ai_tasks,assistants,cohort_eval,ranking}`.

#### Validation Expectations

* Unit tests verify `canonical_offline_heldout_suite()` passes offline with `live_release_authorized=False`, and each mutation (missing version, same labeller/author, tampered threshold, under-sampled cohort, leaked held-out answer in prompt/tuning, forbidden action claim, silent ambiguity guess, missed abstention on declined sensor consent, tampered source hash, unsupported citation, serving-version mismatch, missing usage liability) triggers the exact expected `insufficient`, `fail`, or `unknown_liabilities` classification.

#### Completion Evidence

* `heldout_eval.py` passes `ruff check`, `ruff format --check`, `mypy`, and `test_heldout_eval.py`.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Configure `src/core/pyproject.toml` typing boundary for `heldout_eval` and tests

#### Context

`src/core/pyproject.toml` sets `strict = true` for `mypy`, while legacy modules (`assistants`, `ai_registry`, `ai_tasks`, `ai`, `store`) use `ignore_errors = true` and expose untyped signatures. Existing typed modules in `src/core` (`simulation_lane`, `sensor_review_draft`, `chat_panel`) declare `disallow_untyped_calls = false` so all other strict checks (`disallow_untyped_defs`, `warn_return_any`, `no_implicit_optional`, `check_untyped_defs`) remain active.

#### Intent

Add `zava_forward.core.heldout_eval`, `zava_forward.core.tokenomics_comparison`, and their two test modules to a `disallow_untyped_calls = false` override block in `src/core/pyproject.toml` if needed for legacy `core` calls, keeping full strict type annotations on every function in the new modules and tests.

#### Boundaries

* Included: `src/core/pyproject.toml` `[[tool.mypy.overrides]]` entry.
* Excluded: Weakening global `strict = true` or adding `ignore_errors = true`.

#### Likely Targets

* `src/core/pyproject.toml`: Add narrow `disallow_untyped_calls = false` override block.

#### Dependencies

* P01-T01.

#### Validation Expectations

* `mypy` from `src/core` reports `Success: no issues found`.

#### Completion Evidence

* Zero `mypy` errors across `src/core`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Core Tokenomics Candidate and Single-Lever Comparator

### Context

Issue #108 Criterion 3 and `docs/reference/resources/ai-tokenomics.md` (`C4`) require offline candidate and optimization comparison where:
1. A cheaper candidate that raises `critical_misses`, `unsupported_claims`, `overrides`, or `reopened_cases` on the same held-out cases is reported as a **failure (not a saving)**.
2. Any routing or caching (or model/prompt) option evaluated changes **one lever at a time** against the **same held-out cases** and a **recorded baseline**.

### Intent

Implement `zava_forward.core.tokenomics_comparison` using exact `Decimal` arithmetic and `heldout_eval` freeze verification so both model candidates and single-lever routing/caching options are evaluated fail-closed.

### Boundaries

* Included: `src/core/src/zava_forward/core/tokenomics_comparison.py`.
* Excluded: Modifying `src/agents/src/zava_forward/agents/candidate_comparison.py` (`C16`).

### Likely Targets

* `src/core/src/zava_forward/core/tokenomics_comparison.py`: New Tokenomics candidate and single-lever comparator.

### Dependencies

* P01 (`zava_forward.core.heldout_eval` freeze and isolation checks, `ai_consumption` exact-decimal helpers).

### Validation Expectations

* `ruff check`, `ruff format --check`, `mypy`, `test_dependency_rule.py`, and `test_tokenomics_comparison.py` in `src/core`.

### Completion Evidence

* Cheaper candidates with regressions on `critical_misses`, `unsupported_claims`, `overrides`, or `reopened_cases` return `outcome="failure"` and `is_saving=False`; multi-lever or mismatched-case routing/caching evaluations fail closed with `single_lever_valid=False`.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Implement `src/core/src/zava_forward/core/tokenomics_comparison.py`

#### Context

Tokenomics candidate comparisons must never trade away safety, factual grounding, or human rework for lower token cost, and must isolate single-lever experiments (`model`, `routing`, `caching`, `prompt`) against a recorded baseline over the identical frozen held-out split (`C3`, `C4`, `C9`).

#### Intent

Provide `compare_tokenomics_candidates(manifest, baseline, candidates, *, finance_confirmed_saving=False)` and `canonical_offline_tokenomics_comparison()`.

#### Boundaries

* Included:
  * Pre-flight check of `manifest` via `heldout_eval.check_heldout_freeze(..., require_all_capabilities=False)` and `check_prompt_tuning_isolation`. Unfrozen manifests mark the comparison `frozen=False` and prevent any candidate from passing (`outcome="insufficient"`, `is_saving=False`).
  * Recorded `baseline` validation: requires non-empty `baseline_id`, complete `lever_config` (`model`, `routing`, `caching`, `prompt`), case records matching the exact frozen `held_out.case_ids` set (no missing, extra, or duplicate cases), valid non-negative integer counts (`critical_misses`, `unsupported_claims`, `overrides`, `reopened_cases`, `critical_errors`, `prompt_tokens`, `cached_tokens`, `completion_tokens`, `retries`), and exact `Decimal` cost calculation (or `"Unknown"` when usage or unit pricing is absent/invalid). Computes immutable `baseline_digest`.
  * Per-candidate evaluation on the exact same held-out cases:
    * **Case-set parity check**: Candidate case IDs must match frozen `held_out.case_ids` and baseline case IDs 1-to-1; any mismatch fails closed (`same_held_out_cases=False`, `outcome="failure"`, `is_saving=False`).
    * **Single-lever check**: Computes `changed_levers` by diffing candidate `lever_config` vs baseline `lever_config` across `LEVERS = ("model", "routing", "caching", "prompt")`. Requires `len(changed_levers) == 1` AND requires optional caller-supplied `declared_lever` / `changed_levers` metadata to match that exact single changed config key (so disguised multi-lever bundles submitted under a single `lever="routing"` label are rejected). Changing 0 levers or >= 2 levers sets `single_lever_valid=False`, `outcome="failure"`, `is_saving=False`, and appends `"multiple_levers_changed: ..."` (or `"no_lever_changed"` / `"declared_lever_mismatch"`) to `blocking_reasons`.
    * **Regression & unknown-liability failure check**: Compares candidate vs baseline across the identical held-out cases. If candidate increases `critical_misses`, `unsupported_claims`, `overrides`, `reopened_cases`, or `critical_errors`, loses any case in `baseline["accepted_case_ids"]`, has candidate `critical_misses > 0` / `critical_errors > 0`, has candidate or baseline `status != "pass"` (`"fail"` or `"insufficient"`), has `serving_version_mismatch`, or has `unknown_liabilities > 0` / missing usage / `"Unknown"` cost, sets `outcome="failure"`, `passed=False`, `is_saving=False`, `cost_saving="Unknown"` when liabilities/prices are unresolved, and `classification="regression_failure"` (even when candidate measured token cost is lower than baseline!), recording exact per-metric deltas and `blocking_reasons`.
    * **Qualified candidate & saving semantics**: Only when `frozen=True`, `recorded_baseline_valid=True`, `same_held_out_cases=True`, `single_lever_valid=True`, zero regressions, zero critical misses/errors, and known `Decimal` costs does `passed=True` (`outcome="pass"`). Even then, `cost_lower_than_baseline` is distinguished from cash savings: `time_released_treatment` is `"capacity_only_not_cash_saving"` unless `finance_confirmed_saving=True`.
  * `canonical_offline_tokenomics_comparison()`: deterministic reference fixture running against the frozen held-out split demonstrating: (1) a cheaper model candidate that raises `critical_misses` / `unsupported_claims` / `overrides` / `reopened_cases` -> reported as `failure` (`is_saving=False`), (2) a valid single-lever `caching` option -> `pass`, (3) a valid single-lever `routing` option -> `pass`, and (4) an invalid multi-lever `routing+caching` option -> rejected (`single_lever_valid=False`, `outcome="failure"`).
* Excluded: Network calls, floating-point money math, or mutating `agents`.

#### Likely Targets

* `src/core/src/zava_forward/core/tokenomics_comparison.py`: Primary implementation file.

#### Dependencies

* P01-T01 (`heldout_eval`, `ai_consumption`).

#### Validation Expectations

* Unit tests verify each regression counter (`critical_misses`, `unsupported_claims`, `overrides`, `reopened_cases`) independently turns a cheaper candidate into `outcome="failure"` and `is_saving=False`, and verify single-lever routing and caching options succeed when isolated and fail when combined or run on altered case IDs or an unrecorded baseline.

#### Completion Evidence

* `tokenomics_comparison.py` passes `ruff check`, `ruff format --check`, `mypy`, and `test_tokenomics_comparison.py`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: API Endpoints, Report Integration, and Route Inventory

### Context

`src/api/src/zava_forward/api/server.py` (`C14`) serves manager-only AI governance reports (`GET /api/ai/report` and `GET /api/ai/cohort-evaluation`), and `src/api/tests/test_role_endpoint_inventory.py` (`C18`) enforces that every `/api/...` route in `server.py` is registered in the role-matrix inventory, denies `Contractor` and `Mystery` roles, returns non-500 responses across all roles, and maps in `audit_resource`.

### Intent

Expose the `core` offline RAI held-out evaluation and Tokenomics comparator in `src/api` without adding UI bloat, breaking existing `/api/ai/report` consumers, or tripping AST/role-matrix gates.

### Boundaries

* Included: `src/api/src/zava_forward/api/server.py` and `src/api/tests/test_role_endpoint_inventory.py`.
* Excluded: Web UI changes, deployment/Bicep changes, or unauthenticated endpoints.

### Likely Targets

* `src/api/src/zava_forward/api/server.py`: Add `GET /api/ai/heldout-evaluation`, `POST /api/ai/candidate-comparison`, `audit_resource` entries, and `evaluation["held_out"]` + `evaluation["tokenomics_comparison"]` summary projection in `GET /api/ai/report`.
* `src/api/tests/test_role_endpoint_inventory.py`: Add `/api/ai/heldout-evaluation` to `GET_ENDPOINTS` and `/api/ai/candidate-comparison` to `POST_ENDPOINTS`.

### Dependencies

* P01, P02.

### Validation Expectations

* `test_role_endpoint_inventory.py`, `test_ai_call_site_inventory.py`, `test_dependency_rule.py`, `test_ai_consumption_api.py`, and `test_heldout_eval_api.py` pass in `src/api`.

### Completion Evidence

* HTTP 200 responses for `MANAGER_ROLES` on both new endpoints and `/api/ai/report`; HTTP 403 for non-manager staff, `Contractor`, `Application Administrator`, and `Mystery`; HTTP 400 on unexpected query params on `GET /api/ai/heldout-evaluation` or malformed JSON body on `POST /api/ai/candidate-comparison`.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Wire `GET /api/ai/heldout-evaluation`, `POST /api/ai/candidate-comparison`, and `GET /api/ai/report` in `src/api`

#### Context

`server.py` lines 273–312 define `get_kind(path)` (checked by `projection.allowed(u, get_kind(url.path))` in `do_GET`), lines 902–939 implement side-effect-free `GET /api/ai/report` and `GET /api/ai/cohort-evaluation` using `u["role"] in MANAGER_ROLES` and `if url.query:`, and `do_POST` (`server.py:1375`) pre-parses `body = self._body()` and uses 4-arg `s.audit(u["email"], action, "-", detail)`.

#### Intent

Add clean manager-only handlers for `GET /api/ai/heldout-evaluation` and `POST /api/ai/candidate-comparison`, enrich `GET /api/ai/report` `evaluation` with compact `held_out` and `tokenomics_comparison` summary metadata, and update `get_kind(path)` and `test_role_endpoint_inventory.py`.

#### Boundaries

* Included:
  * `get_kind(path)` (`server.py:307`): map `"/api/ai/heldout-evaluation": "ai_report"` and `"/api/ai/candidate-comparison": "ai_report"` so `projection.allowed(u, get_kind(url.path))` permits staff reachability into the `MANAGER_ROLES` check on GET and allows manager `GET /api/ai/candidate-comparison` to fall through to HTTP 404.
  * `GET /api/ai/heldout-evaluation`: require `u["role"] in MANAGER_ROLES` (else 403), reject any query string via `if url.query: return self._json(400, {"error": "Unknown held-out evaluation parameter."})`, remain side-effect-free (no `s.audit` mutation, matching `/api/ai/report` and `/api/ai/cohort-evaluation`), and return `{"held_out_evaluation": heldout_eval.canonical_offline_heldout_suite(), "tokenomics_comparison": tokenomics_comparison.canonical_offline_tokenomics_comparison()}`.
  * `POST /api/ai/candidate-comparison`: inside `do_POST` using `u` and the already-parsed `body` dict (never calling `self._body()` a second time), require `u["role"] in MANAGER_ROLES` (else 403), reject non-empty `url.query` (400), validate `candidates` (`list` of 1..50 `dict` entries; else 400 so `test_role_endpoint_inventory.py`'s empty `{}` POST probe cleanly receives HTTP 400 for managers and HTTP 403 for non-managers, never 500), default omitted `manifest` and `baseline` to the canonical frozen offline manifest and `canonical_offline_heldout_suite()["baseline_candidate"]` when `manifest`/`baseline` are omitted (or validate caller-supplied `dict`s), record `s.audit(u["email"], "ai_candidate_comparison", "-", f"candidates={len(candidates)} passed={result['all_passed']}")`, and return HTTP 200 JSON from `tokenomics_comparison.compare_tokenomics_candidates(...)`.
  * `GET /api/ai/report`: merge `held_out` and `tokenomics_comparison` compact summary blocks into the returned `evaluation` dict while preserving top-level keys `{"evaluation", "live", "registry", "consumption"}` and every existing key inside `evaluation`.
  * `src/api/tests/test_role_endpoint_inventory.py`: register `"/api/ai/heldout-evaluation"` in `GET_ENDPOINTS` and in `test_contractor_audit_view_and_export_are_denied`, and register `("/api/ai/candidate-comparison", {})` in `POST_ENDPOINTS`.
* Excluded: Changing existing route contracts or adding network calls.

#### Likely Targets

* `src/api/src/zava_forward/api/server.py`
* `src/api/tests/test_role_endpoint_inventory.py`

#### Dependencies

* P01-T01, P02-T01.

#### Validation Expectations

* Full `test_role_endpoint_inventory.py` matrix passes with zero 500s and zero unauthorized disclosures.

#### Completion Evidence

* Verified via `test_role_endpoint_inventory.py` and `test_heldout_eval_api.py`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P04 -->
## P04: Focused Unit Tests, Documentation, and Verification

### Context

Repository validation rules (owner decision D4 / `#1294`) classify bounded offline library + read/check API additions with zero workflow, Dockerfile, dependency-manifest, SQL DDL, infrastructure, or security-control weakening under the focused validation tier: run all planned targeted unit tests, AST/role-matrix regression tests, `ruff check`, `ruff format --check`, and `mypy` in both `src/core` and `src/api`, and update component READMEs.

### Intent

Lock semantic and edge-case test coverage across `src/core` and `src/api`, document honest offline boundaries in `src/core/README.md` and `src/api/README.md`, and verify everything passes cleanly.

### Boundaries

* Included:
  * Test removals: `none`.
  * New test files (maximum 3): `src/core/tests/test_heldout_eval.py`, `src/core/tests/test_tokenomics_comparison.py`, `src/api/tests/test_heldout_eval_api.py` (<= 45 focused test methods total).
  * Existing test update: `src/api/tests/test_role_endpoint_inventory.py` endpoint tuple registration only.
  * Documentation updates: `src/core/README.md` and `src/api/README.md` (`ms.date: 2026-11-15`).
* Excluded: `.copilot-tracking/` paths in code, comments, docstrings, READMEs, or commit messages; pushing to remote.

### Likely Targets

* `src/core/tests/test_heldout_eval.py`
* `src/core/tests/test_tokenomics_comparison.py`
* `src/api/tests/test_heldout_eval_api.py`
* `src/core/README.md`
* `src/api/README.md`

### Dependencies

* P01, P02, P03.

### Validation Expectations

* Isolated worktree `.venv` (`--system-site-packages`) with editable `src/core`, `src/agents`, `src/api`:
  * `src/core`: `python -m unittest discover -s tests -p "test_*heldout*.py"`, `test_tokenomics_comparison.py`, `test_dependency_rule.py`, `test_ai_register_completeness.py`, `test_rai_threshold_live_approval_guard.py`, plus `ruff check`, `ruff format --check`, and `mypy`.
  * `src/api`: `PYTHONPATH=../core/tests:../agents/tests python -m unittest` on `test_heldout_eval_api.py`, `test_ai_tasks.py`, `test_eval_candidate_regression_gate.py`, `test_role_endpoint_inventory.py`, `test_ai_call_site_inventory.py`, `test_dependency_rule.py`, `test_ai_consumption_api.py`, plus `ruff check`, `ruff format --check`, and `mypy`.

### Completion Evidence

* Zero failures across unit tests, `ruff check`, `ruff format --check`, and `mypy`; READMEs updated; clean local commit after `rpi-review`.

### Unresolved Items

* None.

<!-- rpi:task id=P04-T01 -->
### P04-T01: Author `src/core/tests/test_heldout_eval.py` and `src/core/tests/test_tokenomics_comparison.py`

#### Context

Tests must fail without the implementation and cover genuine semantic behavior and negative edge cases rather than restating constants.

#### Intent

Create `test_heldout_eval.py` and `test_tokenomics_comparison.py` in `src/core/tests/`.

#### Boundaries

* Included:
  * `test_heldout_eval.py`: tests canonical 11-capability pass (`live_release_authorized=False`), missing/blank task/model/prompt/policy/source versions, non-independent labeller (`labelled_by == prompt_author`), tampered thresholds after approval, cohort sample count below `min_n`, held-out case ID overlap with prompt/tuning sets, held-out expected answer verbatim and 6-word shingle leakage into rendered prompts and tuning examples, control failure (`FORBIDDEN` action claim), ambiguity failure (guessing instead of surfacing unknowns), abstention failure (emitting sensor-derived proposal when resident sensor consent is declined), source integrity failure (mismatched source hash / fabricated citation), factual support failure (unsupported claim), subgroup unaveraged failure propagation + non-fairness notice, serving-version mismatch detection, missing usage -> `unknown_liabilities` + `"Unknown"` cost, and `calibration` `not_applicable` vs genuine scored-prediction branch.
  * `test_tokenomics_comparison.py`: tests cheaper candidate raising `critical_misses`, `unsupported_claims`, `overrides`, and `reopened_cases` (each independently causing `outcome="failure"` and `is_saving=False`), lost baseline-accepted case failure, `Unknown` price/usage failure, valid single-lever `routing` and single-lever `caching` evaluations against recorded baseline on identical held-out cases, multi-lever `routing+caching` rejection (`single_lever_valid=False`), zero-lever rejection, unrecorded/incomplete baseline rejection, mismatched held-out case set rejection, unfrozen manifest gating, and capacity-only time-released treatment unless Finance confirms.
* Excluded: Trivial getter/constant assertions.

#### Likely Targets

* `src/core/tests/test_heldout_eval.py`
* `src/core/tests/test_tokenomics_comparison.py`

#### Dependencies

* P01, P02.

#### Validation Expectations

* Both test modules pass under `unittest`, `ruff`, and `mypy`.

#### Completion Evidence

* Test execution output recorded in `.copilot-tracking/changes/2026-11-15/ai-108-heldout-eval-changes.md`.

#### Unresolved Items

* None.

<!-- rpi:task id=P04-T02 -->
### P04-T02: Author `src/api/tests/test_heldout_eval_api.py` and update README documentation

#### Context

API surfaces require HTTP role-boundary verification and honest documentation of offline synthetic limits in `src/core/README.md` and `src/api/README.md`.

#### Intent

Create `src/api/tests/test_heldout_eval_api.py`, update `src/core/README.md` and `src/api/README.md`, and run the complete focused validation suite across `src/core` and `src/api`.

#### Boundaries

* Included:
  * `src/api/tests/test_heldout_eval_api.py` (with `disallow_untyped_calls = false` in `src/api/pyproject.toml` matching `test_ai_consumption_api` since `App`/`make_handler` are untyped): tests manager HTTP 200 on `GET /api/ai/heldout-evaluation`, `POST /api/ai/candidate-comparison` (valid single-lever pass, cheaper regression failure, and multi-lever failure over HTTP), and `GET /api/ai/report` (`evaluation.held_out` and `evaluation.tokenomics_comparison` presence without regressing existing fields); tests HTTP 403 for non-manager staff (`Retrofit Coordinator`), `Contractor`, and `Application Administrator`; tests HTTP 400 for query parameters on `GET /api/ai/heldout-evaluation` and invalid JSON payloads on `POST /api/ai/candidate-comparison`.
  * `src/core/README.md` and `src/api/README.md`: add concise sections documenting the offline RAI held-out evaluation and Tokenomics single-lever candidate comparison contracts and explicit non-claims (offline synthetic fixtures only; live model batch, regional quota, and human participant evidence remain open on `#108`).
* Excluded: Unrelated README edits.

#### Likely Targets

* `src/api/tests/test_heldout_eval_api.py`
* `src/api/pyproject.toml`
* `src/core/README.md`
* `src/api/README.md`

#### Dependencies

* P01, P02, P03, P04-T01.

#### Validation Expectations

* Focused `unittest` suites, `ruff check`, `ruff format --check`, and `mypy` exit 0 in both `src/core` and `src/api`.

#### Completion Evidence

* Recorded command outputs and exit codes in `.copilot-tracking/changes/2026-11-15/ai-108-heldout-eval-changes.md`.

#### Unresolved Items

* None.
