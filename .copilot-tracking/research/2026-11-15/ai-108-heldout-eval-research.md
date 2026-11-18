<!-- markdownlint-disable-file -->

# Task Research: ai-108-heldout-eval

| Field              | Value                                                               |
|--------------------|---------------------------------------------------------------------|
| Date               | 2026-11-15                                                          |
| Researcher / agent | RPI Agent (`rpi-research`)                                          |
| Status             | Complete                                                            |
| Artifact path      | .copilot-tracking/research/2026-11-15/ai-108-heldout-eval-research.md |

## Research Brief

* What to research: Existing offline AI evaluation, held-out freeze/split, subgroup/cohort reporting, five-assistant + retained legacy task family coverage, and Tokenomics candidate/routing/caching comparison logic across `src/core`, `src/api`, and `src/agents`, plus the PRD/tokenomics requirements for Issue #108.
* Why it matters: Issue #108 requires offline RAI Held-Out and Tokenomics comparison enforcement and reporting in `src/core` and `src/api` without violating package dependency boundaries (`core` cannot depend on `agents`/`api`; `api` depends on `core`) or adding a separate governance service.
* Audience or intended use: RPI planning, critique, implementation, and review for `feat/ai-108-heldout-eval-0228` (`Refs #108`).
* Scope: `src/core`, `src/api`, relevant contracts/patterns in `src/agents`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, and `docs/reference/resources/ai-tokenomics.md`.
* Non-goals: Paid live Azure OpenAI calls, actual human participant runs, regional quota attestation, separate governance services, pushing to remote, or claiming full `Closes #108` closure while live/human criteria remain open.
* Criteria: Cover all three target acceptance groups (pre-eval freeze & prompt/tuning isolation; 5-assistant + legacy family coverage, controls, ambiguity, abstention, source integrity, factual support, metrics/hashes/denominators/calibration-NA; Tokenomics regression failure rule and single-lever routing/caching comparison).
* Requested outputs: Convergence recommendation for `src/core` and `src/api` modules, endpoints/exports, and unit tests.
* Output mode: convergence

## Research Parameters

| Field                                | Value                                                                                                                                                              |
|--------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)                 | How are held-out evaluation and tokenomics comparisons currently implemented across `src/agents`, `src/core`, and `src/api`, and what belongs in `src/core` + `src/api`? |
| Codebase scope                       | `src/core`, `src/api`, `src/agents`, `docs/prds/`, `docs/reference/resources/ai-tokenomics.md`                                                                     |
| External scope                       | none                                                                                                                                                               |
| Initial internal candidate areas     | `src/core/src/zava_forward/core/ai*.py`, `assistants.py`, `cohort_eval.py`, `rai_metrics.py`, `src/api/src/zava_forward/api/server.py`, `src/agents/src/zava_forward/agents/heldout_*.py`, `candidate_comparison.py`, `model_option_comparison.py` |
| Initial external candidate areas     | none                                                                                                                                                               |
| Research posture                     | balanced                                                                                                                                                           |
| Posture provenance                   | default (bounded internal feature with adjacent cross-package contracts in `src/agents`)                                                                           |
| Explicit limits / deadline           | Deliver in `src/core` and `src/api`; do not push; non-interactive session                                                                                          |
| Posture-specific completion basis    | balanced scope coverage and adequate evidence                                                                                                                      |
| Edits allowed during research?       | no, research-only                                                                                                                                                  |
| Resolved evidence root               | .copilot-tracking/                                                                                                                                                 |
| Known constraints / excluded sources | Respect package dependency rules (`core` -> stdlib only; `api` -> `core`); do not claim live-model or human-participant effectiveness from offline fixtures         |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                             | Match and provenance                              | Scoped authority or output contract                            | Selected / skipped reason                                                       |
|---------------------|---------------------------------------|---------------------------------------------------|----------------------------------------------------------------|---------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md`     | `applyTo: "**"` repository-wide instruction       | AMA knowledge base, dependency, testing, and git rules         | Selected: governs repository structure, validation tiers, and RAI boundaries    |
| Skill               | `python-foundational` / `rai-standards` | Optional domain skills in catalog                 | General Python / NIST AI RMF framing                           | Skipped: repository PRD and existing `core`/`agents`/`api` contracts are authoritative |
| Research specialist | `hve-core-all:rpi-researcher`         | Available subagent for independent lanes          | Separate lane file under `.copilot-tracking/research/subagents/` | Skipped in favor of direct inline inspection: tightly coupled cross-package Python modules |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                               | Answers / unanswered | Resulting decision or selected further research                                 |
|------------------|-------------------------------------------------------------------------------------|----------------------|---------------------------------------------------------------------------------|
| Intake           | Non-interactive execution with explicit branch, scope, target packages, and criteria | N/A (non-interactive) | Proceed with `balanced` posture and `convergence` output mode                   |
| Direction change | None at intake                                                                      | N/A                  | Maintain caller scope (`src/core` and `src/api`)                                |
| Convergence      | Non-interactive convergence supported by complete codebase evidence                 | N/A (non-interactive) | Selected pure `zava_forward.core.heldout_eval` + `zava_forward.core.tokenomics_comparison` surfaced via `src/api` manager routes and `GET /api/ai/report` |

## Scope and Success Criteria

* Scope: Offline RAI held-out freeze, leakage guard, 5-assistant + legacy family offline evaluation, and Tokenomics candidate & single-lever routing/caching comparison in `src/core` and `src/api`.
* Assumptions: `src/agents` may already contain partial or CLI-only held-out/comparison modules that either are not accessible from `src/core`/`src/api` due to dependency rules or lack pieces of the Issue #108 contract.
* Success criteria:
  * Every research question is answered or marked unanswerable with the missing evidence named.
  * Evidence is grounded in actual code, docs, or tooling results, with locations (`path:line` for code, URL + retrieval date for external).
  * Findings, decisions, and readiness claims cite Evidence Log IDs.
  * Alternatives are compared with trade-offs when the design space and output mode require it. A recommendation is selected only in convergence mode.
  * Open questions, risks, and residual uncertainty are recorded.
  * Self-check passes.

## Task Research Requests

* Explicit requests: Deliver the offline RAI Held-Out and Tokenomics comparison criteria (items 1, 2, 3) in `src/core` and `src/api` with dated RPI artifacts and focused validation.
* Inferred research questions: What already exists in `src/agents`, `src/core`, and `src/api`? What are the exact dependency rules between packages? How does `src/api` expose AI evaluation, RAI governance, and tokenomics surfaces?
* Caller constraints and non-goals: Do not add a governance service; do not transfer authority to AI; do not push; use `Refs #108`.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                    | Source / checkpoint | Effect on active brief, evidence, or revalidation                |
|----------------------------------------------------------|--------------------------------------------------------------------------|---------------------|------------------------------------------------------------------|
| narrow                                                   | Target implementation in `src/core` and `src/api`                        | Caller prompt       | Inspect `src/agents` for contract alignment, implement in `core` + `api` |
| exclude                                                  | Do not push to remote; commit locally with `Refs #108`                   | Caller prompt       | Keep branch local and worktree clean at completion               |

## Research Questions

|  # | Sub-question                                                                                                      | Type            | Priority | Status   |
|---:|-------------------------------------------------------------------------------------------------------------------|-----------------|----------|----------|
| Q1 | What dependency rules govern `src/core`, `src/agents`, and `src/api`?                                             | straightforward | H        | answered |
| Q2 | What held-out freeze, prompt/tuning leakage, assistant/legacy family coverage, and evaluation logic already exist? | depth           | H        | answered |
| Q3 | What Tokenomics candidate comparison and single-lever routing/caching logic already exist in `core`/`agents`/`api`? | depth           | H        | answered |
| Q4 | How does `src/api` expose AI evaluation, consumption/tokenomics, and governance evidence endpoints?               | breadth         | H        | answered |
| Q5 | What gaps or edge cases remain between existing code and the three target acceptance criteria for Issue #108?     | depth           | H        | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: Issue #108 body, `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/README.md`, `docs/reference/memory.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `docs/reference/resources/ai-tokenomics.md`.
* Reused (verified) findings: Issue #108 is partially delivered; live-model, regional quota, and actual human participant evidence remain open (`Refs #108` applies rather than `Closes #108`).
* Superseded / stale: Legacy `mvp/` paths mentioned in older issue labels were retired at `v0.21.0` cut-over in favor of `src/{core,agents,api,orchestrator,importer}`.

## Cycle 1 Execution

### Wave 1: Wider (Inline)

* Investigated package dependency gates (`C1`, `C2`), PRD evaluation/RAI/tokenomics specifications (`C3`, `C4`), canonical AI task registries (`C5`), existing `agents` evaluation harnesses (`C6`, `C7`, `C8`, `C9`), and `api` reporting endpoints (`C14`).
* Inline disposition: Kept inline because all modules reside in a tightly coupled monorepo workspace (`src/{core,agents,api}`) where direct AST/contract inspection avoids subagent serialization overhead.
* Findings:
  * `src/core` strictly enforces `ALLOWED = {"core"}` (`C1`), prohibiting imports from `zava_forward.agents` or `zava_forward.api`. `src/api` permits `{"api", "core", "agents"}` only temporarily until `#144` (`C2`). Therefore, reusable offline held-out evaluation and tokenomics comparison logic must live in `src/core` so both `src/core` and `src/api` consume a single stdlib-only source of truth.
  * `ai_registry.py` (`C5`) defines the canonical task inventory: 5 proposal-only assistants (`stock-prioritisation`, `assessment-preparation`, `funding-evidence`, `works-resident-coordination`, `quality-evidence`) and 6 retained legacy task families (`briefing`, `message`, `summary`, `priority`, `funding_draft`, `read_document`).
  * `src/agents/src/zava_forward/agents/ai_eval.py` (`C6`) explicitly excludes all 5 assistants (`COVERAGE_NOTE`) and performs un-frozen scripted control checks rather than held-out evaluation.

### Wave 2: Deeper (Inline)

* Inspected `assistants.py` (`C10`), `ai_tasks.py` and `ai_prompts.py` (`C11`), `store.py` (`C12`), `cohort_eval.py` and `rai_release.py` (`C13`), `ai_consumption.py` (`C15`), `heldout_freeze.py` and `chat_heldout.py` (`C7`, `C8`), and `candidate_comparison.py` (`C9`).
* Findings:
  * **Pre-evaluation freeze and prompt/tuning leakage (`Q2`, `Q5`)**: `agents/heldout_freeze.py` (`C7`) validates single-task version keys (`task`, `model`, `prompt`, `policy`, `source`), held-out case IDs, seed, denominator, labeller independence from prompt author, expected outcomes, critical error definitions, cohort floors, and digest-bound threshold approval, while `agents/chat_heldout.py` (`C8`) checks 6-word shingle text leakage. However, `src/core` has neither freeze checking nor prompt/tuning answer-text leakage guards across rendered prompts (`ai_prompts.render`, `assistants.build_request`) and tuning inputs, nor multi-family coverage across all 5 assistants + 6 retained legacy families (`C5`, `C10`, `C11`).
  * **Five assistants + six legacy families offline held-out harness (`Q2`, `Q5`)**:
    * Each of the 5 assistants (`C10`) operates via `capture`, `eligible`, `build_request`, `validate_output`, `shape_result`, and `review_flag`, enforcing bounded read-only proposals, citation verification against captured facts/documents/sensors, resident sensor consent withholding (`quality-evidence`), unknown/conflict surfacing on ambiguous inputs, and abstention (`withheld`/ineligible/manual route) when evidence is missing or unconsented.
    * Each of the 6 retained legacy families (`C11`, `C12`) operates via `Store.briefing`, `Store.ai_run(..., "message"|"summary")`, `Store.ai_priority`, `Store.funding_draft`, and `Store.read_document` (`ai_tasks.run_document`), enforcing forbidden-action rejection (`ai.FORBIDDEN`), citation resolution (`statement_sources`), critical-miss checks on open safety hazards (`ai_tasks.critical_misses`), document malware/cleanliness gates (`require_clean`), and explicit template/workflow-only fallbacks.
    * Neither `src/core` nor `src/api` currently runs a frozen held-out suite across all 11 capabilities (5 assistants + 6 legacy families) recording critical errors/misses, usable coverage, subgroup results (never averaged, carrying OQ-018 synthetic non-fairness notice from `C13`), hashes, split/seed, denominators, actual serving version (`unattested` offline vs mismatched model version detection), token usage, unknown liabilities (missing/malformed usage or unpriced/unsettled reservations from `C15`), reviewer protocol, `pass`/`fail`/`insufficient` outcomes, and explicit calibration `not_applicable` documentation when meaningful scored probability predictions are absent.
  * **Tokenomics candidate comparison and single-lever rule (`Q3`, `Q5`)**:
    * `agents/candidate_comparison.py` (`C9`) checks candidate regressions in `agents`, and `api/tests/test_eval_candidate_regression_gate.py` (`C16`) tests `agents.candidate_comparison`. Neither `src/core` nor `src/api` (`server.py`, `C14`) exposes a `core`-owned Tokenomics candidate/option comparator or HTTP endpoint/report projection.
    * Under Criterion 3 and PRD/tokenomics rules (`C3`, `C4`), a cheaper candidate must fail (`outcome="failure"`, `is_saving=False`) whenever it raises `critical_misses`, `unsupported_claims`, `overrides`, or `reopened_cases` (or loses baseline-accepted proposals / introduces critical errors / has `Unknown` cost while claiming a saving) on the exact same frozen held-out case set. Furthermore, any routing or caching (or model/prompt) option evaluated must change **exactly one lever at a time** against the **same held-out cases** and a **recorded baseline**; multi-lever changes (`changed_levers` count != 1, or unrecorded baseline, or mismatched held-out case IDs) must fail closed (`not_comparable` / `failure`, never `saving`).

### Wave 3: Contrarian (Inline)

* Challenged the proposed `core` + `api` architecture against repository gate invariants (`C16`, `C17`, `C18`).
* Findings:
  * **Call-site inventory invariant (`C17`)**: `src/api/tests/test_ai_call_site_inventory.py` AST-scans every `src/*/src/**/*.py` file for `"chat/completions"`, `"/openai/deployments"`, `"/responses?api-version"`, and OpenAI/Azure AI SDK imports. Any new `core` or `api` module containing those strings would break `AiCallSiteInventoryTest`. Confirming our modules are strictly offline and provider-free preserves the call-site inventory invariant cleanly.
  * **Exhaustive role & route inventory invariant (`C18`)**: `src/api/tests/test_role_endpoint_inventory.py` regex-parses `server.py` for every `/api/...` literal and fails unless every route is listed in `GET_ENDPOINTS` or `POST_ENDPOINTS`, returns non-500 for all roles, denies `Contractor` and `Mystery` with 403/404, maps cleanly in `audit_resource` (`server.py:311`), and leaks zero restricted canary fields. Any new API endpoint (such as `GET /api/ai/heldout-evaluation` and `POST /api/ai/candidate-comparison`) must be wired into `MANAGER_ROLES`, `audit_resource`, and `test_role_endpoint_inventory.py`.
  * **Strict typing & shared environment (`pyproject.toml`)**: New files in `src/core` and `src/api` are checked under `mypy` (`strict = true`) and `ruff` (`line-length = 100`, `E, F, I, B, UP`). Calling untyped legacy modules (`assistants`, `ai_registry`, `ai_tasks`, `store`) from new typed `core` modules requires explicit `disallow_untyped_calls = false` module overrides in `src/core/pyproject.toml` (matching existing typed modules like `simulation_lane` and `sensor_review_draft`) or typed adapters. Also, global `~/.local` editable installs point to a sibling worktree, so validation must use a worktree-local `.venv` (already gitignored in `.gitignore:2`) or explicit `PYTHONPATH` to avoid cross-worktree contamination and leave `git status --short` empty.
  * **Existing `agents` compatibility**: `src/api/tests/test_eval_candidate_regression_gate.py` (`C16`) imports `zava_forward.agents.candidate_comparison`. Leaving `src/agents` untouched preserves 100% backward compatibility while adding the complete `core` modules and `api` surfaces.

## Evidence Log

| ID  | Kind | Location                                                              | Summary                                                                                                                                      |
|-----|------|-----------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------|
| C1  | code | `src/core/tests/test_dependency_rule.py:13`                           | `ALLOWED = {"core"}`: `zava_forward.core` cannot import `agents` or `api`.                                                                   |
| C2  | code | `src/api/tests/test_dependency_rule.py:14`                            | `ALLOWED = {"api", "core", "agents"}`: `api` depends on `core` (`agents` allowed only temporarily until `#144`).                             |
| C3  | doc  | `docs/prds/zava-forward-retrofit-programme-demonstrator.md:949`       | PRD AI Model Selection, Held-Out Evaluation, Subgroup Reporting, Calibration-NA, and Tokenomics comparison contract for Issue #108.          |
| C4  | doc  | `docs/reference/resources/ai-tokenomics.md:107`                       | Tokenomics evaluation rules: cost per accepted proposal, single-lever routing/caching evaluation, regression = failure (never saving).       |
| C5  | code | `src/core/src/zava_forward/core/ai_registry.py:61`                    | Canonical registry of 5 proposal-only assistants (`ASSISTANTS`) and 6 retained legacy task families (`LEGACY`).                              |
| C6  | code | `src/agents/src/zava_forward/agents/ai_eval.py:102`                   | `COVERAGE_NOTE`: existing `agents` harness is un-frozen control scaffolding and does not evaluate the 5 core assistants.                     |
| C7  | code | `src/agents/src/zava_forward/agents/heldout_freeze.py:17`             | Single-task freeze check in `agents` (not importable from `core`; lacks prompt/tuning rendered-answer text guard and 11-task suite support). |
| C8  | code | `src/agents/src/zava_forward/agents/chat_heldout.py:52`               | 6-word shingle text leakage detection pattern for held-out vs prompt/development text.                                                       |
| C9  | code | `src/agents/src/zava_forward/agents/candidate_comparison.py:199`      | `agents`-local candidate comparison helper; lacks single-lever routing/caching isolation gate in `core` and `api` exposure.                  |
| C10 | code | `src/core/src/zava_forward/core/assistants.py:43`                     | Core 5-assistant contracts: `REGISTRY`, `capture`, `eligible`, `build_request`, `validate_output`, `shape_result`, `review_flag`.            |
| C11 | code | `src/core/src/zava_forward/core/ai_tasks.py:29`                       | Core legacy task controls: `statement_sources`, `priority_items`, `critical_misses`, `run_text_task`, `run_document`.                        |
| C12 | code | `src/core/src/zava_forward/core/store.py:808`                         | `Store` entry points for `read_document`, `ai_run` (`message`, `summary`), `briefing`, `ai_priority`, and `funding_draft`.                   |
| C13 | code | `src/core/src/zava_forward/core/cohort_eval.py:32`                    | `named_human`, `NON_FAIRNESS_PROVENANCE_NOTICE`, digest-bound threshold approval, and subgroup floor conventions.                            |
| C14 | code | `src/api/src/zava_forward/api/server.py:902`                          | Manager-only `GET /api/ai/report` and `GET /api/ai/cohort-evaluation` HTTP handlers and `audit_resource` (`server.py:311`).                  |
| C15 | code | `src/core/src/zava_forward/core/ai_consumption.py:55`                 | Exact-decimal token/cost primitives, `usage()`, `reference()`, and explicit `Unknown` liability handling.                                    |
| C16 | code | `src/api/tests/test_eval_candidate_regression_gate.py:9`              | Existing regression gate test in `src/api/tests` importing `zava_forward.agents.candidate_comparison` (must remain unbroken).                |
| C17 | code | `src/api/tests/test_ai_call_site_inventory.py:24`                     | AST gate ensuring no unclassified provider URL fragments or SDK imports appear in `src/*/src/**/*.py`.                                       |
| C18 | code | `src/api/tests/test_role_endpoint_inventory.py:18`                    | Regex/HTTP role-matrix gate requiring every `/api/...` route in `server.py` to be registered and access-controlled across all roles.         |

## Synthesis and Alternatives

### Question Synthesis

* **Q1 (Dependency boundaries)**: `src/core` is stdlib-only (`C1`); `src/api` consumes `src/core` (`C2`). Placing pure offline held-out evaluation and tokenomics comparison modules in `src/core` satisfies dependency direction cleanly.
* **Q2 (Held-out freeze, leakage, and 11-capability harness)**: `src/core` needs a pure offline held-out freeze + prompt/tuning leakage validator and deterministic offline evaluator covering all 5 assistants (`C10`) and all 6 retained legacy families (`C5`, `C11`, `C12`). Before any case is scored, the harness must verify frozen versions (`task`, `model`, `prompt`, `policy`, `source`), an independently labelled held-out split (`labelled_by` != `prompt_author`), expected outcomes, critical error definitions, cohort sample floors, approved thresholds (digest-bound), and zero held-out case-ID or held-out answer/expected-text leakage into rendered prompts or tuning corpora.
* **Q3 (Tokenomics candidate & single-lever comparison)**: `src/core` needs a pure deterministic comparator enforcing that (a) any cheaper candidate raising `critical_misses`, `unsupported_claims`, `overrides`, or `reopened_cases` (or losing baseline-accepted proposals, adding critical errors, or having `Unknown` cost) on the exact same frozen held-out cases is reported as `outcome="failure"` and `is_saving=False`, and (b) any routing, caching, model, or prompt option evaluated changes **exactly one lever at a time** against the **same held-out cases** and a **recorded baseline** (failing closed when 0 or >1 levers change, baseline is unrecorded, or held-out case sets diverge).
* **Q4 & Q5 (`src/api` exposure & edge cases)**: `src/api` should expose manager-only (`MANAGER_ROLES`) endpoints `GET /api/ai/heldout-evaluation` (returning the verified canonical offline held-out evaluation across all 5 assistants + 6 legacy families plus baseline single-lever tokenomics checks) and `POST /api/ai/candidate-comparison` (evaluating caller-supplied frozen manifest + recorded baseline + candidate/routing/caching runs through `core` validation with bounded JSON input), and attach a compact `heldout_evaluation` summary block inside `GET /api/ai/report` (`evaluation.held_out`) without breaking existing `evaluation` fields (`C14`, `C18`).

### Alternatives Evaluated

| Option | Summary | Trade-offs | Disposition |
|---|---|---|---|
| Option A: Pure `src/core` modules (`heldout_eval.py`, `tokenomics_comparison.py`) + manager-only `src/api` endpoints and `/api/ai/report` summary | Implement complete freeze, prompt/tuning answer-leakage guard, 11-capability deterministic offline held-out harness, and single-lever tokenomics comparator in `zava_forward.core`, surfaced via `GET /api/ai/heldout-evaluation`, `POST /api/ai/candidate-comparison`, and `GET /api/ai/report` | Zero cross-package violation (`C1`), zero network call sites (`C17`), preserves `agents` backward compatibility (`C16`), directly testable in both `core` and `api` | **Selected** |
| Option B: Import `zava_forward.agents` inside `src/core` or wire `src/api` only to `src/agents` | Reuse `agents/heldout_freeze.py` and `agents/candidate_comparison.py` directly | Violates `src/core` dependency gate (`C1`), deepens temporary `api -> agents` coupling (`#144`, `C2`), and still lacks 5-assistant + 6-legacy held-out coverage (`C6`) and single-lever enforcement | Rejected |
| Option C: Add a separate evaluation microservice | Stand up a standalone FastAPI/HTTP governance service | Explicitly forbidden by PRD/Issue #108 constraints ("do not add a governance service") | Rejected |

## Decisions and Risks

* **Selected recommendation**: Option A.
  1. Add `src/core/src/zava_forward/core/heldout_eval.py` implementing:
     * `check_heldout_freeze(...)` and `check_prompt_tuning_isolation(...)`: freezes `task`/`model`/`prompt`/`policy`/`source` versions, independent labeller (`labelled_by` distinct from `prompt_author`), held-out split + deterministic `seed`, expected outcomes, critical error definitions, cohort sample floors, digest-bound approved thresholds, and ensures neither held-out case IDs nor held-out expected answers/verbatim answer shingles ever enter rendered system/user prompts or tuning examples.
     * `evaluate_heldout_suite(...)` and `canonical_offline_heldout_suite()`: deterministic offline evaluation covering **all 5 assistants** (`stock-prioritisation`, `assessment-preparation`, `funding-evidence`, `works-resident-coordination`, `quality-evidence`) and **all 6 retained legacy families** (`briefing`, `message`, `summary`, `priority`, `funding_draft`, `read_document`), exercising **correct controls**, **ambiguity**, **abstention**, **source integrity**, and **factual support**; recording `critical_errors`, `critical_misses`, `usable_coverage`, `subgroup_results` (per-cohort, unaveraged, with OQ-018 synthetic non-fairness notice), `hashes`, `split`, `seed`, `denominators`, `actual_serving_version`, `usage`, `unknown_liabilities`, `reviewer_protocol`, `outcome` (`pass` / `fail` / `insufficient`), and documenting `calibration` as `not_applicable` when meaningful scored probability predictions are absent.
  2. Add `src/core/src/zava_forward/core/tokenomics_comparison.py` implementing:
     * `compare_tokenomics_candidates(...)`: validates frozen held-out manifest and recorded baseline, enforces that a cheaper candidate raising `critical_misses`, `unsupported_claims`, `overrides`, or `reopened_cases` (or dropping accepted proposals / adding critical errors / carrying `Unknown` cost liabilities) on the exact same held-out cases is reported as `outcome="failure"` (`is_saving=False`), and enforces single-lever isolation (`model`, `routing`, `caching`, `prompt` — changing one lever at a time against the exact same held-out cases and recorded baseline, failing closed as `failure` / `single_lever_valid=False` on multi-lever or unbaselined changes).
  3. Expose in `src/api/src/zava_forward/api/server.py`:
     * Read-only manager endpoint `GET /api/ai/heldout-evaluation` (rejecting non-managers with 403, query parameters with 400, writes with 404/405 per server conventions) returning the verified canonical offline held-out evaluation report and reference single-lever tokenomics comparison matrix.
     * Manager endpoint `POST /api/ai/candidate-comparison` validating bounded JSON payloads and returning the deterministic `compare_tokenomics_candidates` evaluation without mutating domain state or making provider calls.
     * Include `evaluation["held_out"]` summary metadata in `GET /api/ai/report` while preserving all existing keys.
     * Register new endpoints in `audit_resource` (`server.py`) and `src/api/tests/test_role_endpoint_inventory.py`.
* **Residual risks and honest boundaries**:
  * Offline held-out suite uses constructed synthetic cases and deterministic scripted model outputs; it proves offline harness/control/freeze/tokenomics logic (`Refs #108`), not live Azure OpenAI model performance, regional quota attestation, or human participant acceptance. Every emitted report carries explicit `offline_synthetic_only=True` and `live_release_authorized=False` markers.
  * Shared host Python environment has sibling-worktree editable installs; use an isolated worktree `.venv` (`--system-site-packages`, gitignored) during implementation/testing and remove or verify `git status --short` is completely empty before commit.

## Further Research (Optional)

* None required for the scoped offline RAI Held-Out and Tokenomics deliverables in `src/core` and `src/api`. Live model batch execution and human participant evaluation remain tracked on Issue #108 as separate gated items requiring owner spend/participant authorization.

## Readiness and Handoff

* **Research Disposition**: `executed`
* **Planning Readiness**: `Ready`
* **Self-Check**:
  * [x] Brief, parameters, extension registry, and direction controls recorded.
  * [x] Cycle 1 completed `Wider`, `Deeper`, and `Contrarian` waves in order.
  * [x] All questions `Q1`–`Q5` answered with `C1`–`C18` `path:line` evidence.
  * [x] Selected convergence recommendation and rejected alternatives documented.
  * [x] Zero source code modifications made during Research.

