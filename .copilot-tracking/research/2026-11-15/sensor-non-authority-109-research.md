<!-- markdownlint-disable-file -->

# Task Research: sensor-non-authority-109

| Field              | Value                                                                      |
|--------------------|----------------------------------------------------------------------------|
| Date               | 2026-11-15                                                                 |
| Researcher / agent | RPI Agent (`rpi-research`)                                                 |
| Status             | Complete                                                                   |
| Artifact path      | .copilot-tracking/research/2026-11-15/sensor-non-authority-109-research.md |

## Research Brief

* What to research: How `src/core` implements sensor ingestion (`sensor_ingest.py`), deterministic sensor analysis (`sensor_analysis.py`), case/programme state storage, deterministic home ranking, Awaab's Law / statutory hazard diagnosis and clock initiation, and hold/blocker release; where the non-authority boundary is already enforced versus implicit; and what explicit runtime invariant checks and end-to-end acceptance tests in `src/core` are needed to prove Issue #109's engineering criterion (`No sensor signal diagnoses a hazard, starts a clock, releases a hold or changes ranking`).
* Why it matters: Issue #109 requires auditable, regression-proof enforcement that simulated IoT Hub telemetry and derived review signals only produce bounded human review tasks or telemetry observations and can never mutate statutory hazards, clocks, holds, or home ranking.
* Audience or intended use: `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, and `rpi-review` phases in this RPI session, plus PR reviewers assessing `Refs #109`.
* Scope: `src/core/` (`sensor_ingest.py`, `sensor_analysis.py`, store/domain/ranking/hazard/hold modules and `src/core/tests/`), plus requirements and architecture references (`docs/brds/agentic-retrofit-programme-brd.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `docs/adrs/0002-pilot-readiness-architecture.md`, `docs/adrs/0003-journey-derived-capabilities-runtime-fit.md`).
* Non-goals: Azure IoT Hub cloud provisioning, database schema migrations outside `src/core` contracts if excluded by ADR 0003, running `tools/rpi-checks.py`, or pushing commits to remote.
* Criteria: Every surface named in the prompt (`sensor_ingest.py`, `sensor_analysis.py`, store, ranking, hazard/clock, hold/blocker) is traced with `path:line` evidence (`C#`), existing test coverage is inventoried, any enforcement gap or bypass vector is identified in Wave 3 Contrarian analysis, and a concrete design recommendation is converged for `src/core`.
* Requested outputs: Completed `rpi-research` artifact in `convergence` mode ready for `rpi-plan`.
* Output mode: convergence

## Research Parameters

| Field                            | Value                                                                                                                                                              |
|----------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Research question(s)             | How do sensor readings and derived signals interact with hazards, clocks, holds, and home ranking in `src/core`, and how should non-authority be enforced/tested? |
| Codebase scope                   | `src/core/`, `docs/brds/`, `docs/prds/`, `docs/adrs/`, `docs/case_study_48_*.md`                                                                                   |
| External scope                   | none                                                                                                                                                               |
| Initial internal candidate areas | `src/core/` (`sensor_ingest.py`, `sensor_analysis.py`, ranking/hazard/hold/store modules, `src/core/tests/`), BRD FR-048, PRD FR-050 / AC-066..068, ADR 0002/0003  |
| Initial external candidate areas | none                                                                                                                                                               |
| Research posture                 | focused                                                                                                                                                            |
| Posture provenance               | default (bounded internal task with named source targets and explicit scope)                                                                                       |
| Explicit limits / deadline       | Focused validation tier (`src/core` unit tests, `mypy`, `ruff`); single continuous non-interactive run; do not run `tools/rpi-checks.py`; do not push              |
| Posture-specific completion basis| focused scope and materiality                                                                                                                                      |
| Edits allowed during research?   | no, research-only                                                                                                                                                  |
| Resolved evidence root           | `.copilot-tracking/`                                                                                                                                               |
| Known constraints / excluded sources | Code-only internal research; preserve existing `src/core` behavior while hardening and proving sensor non-authority invariants                                 |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind                | Candidate                               | Match and provenance                                   | Scoped authority or output contract                                   | Selected / skipped reason                                                       |
|---------------------|-----------------------------------------|--------------------------------------------------------|-----------------------------------------------------------------------|---------------------------------------------------------------------------------|
| Instruction         | `.github/copilot-instructions.md` (AMA) | `applyTo: "**"` matches workspace and tracking files   | Repository conventions, regulatory/authority boundaries, test tiers   | Selected: governs Zava Forward code/test standards and safety boundaries        |
| Skill               | `rpi-research`                          | Active phase skill                                     | Three-wave read-only research artifact contract                       | Selected: active phase contract                                                 |
| Skill               | `python-foundational`                   | Python codebase (`src/core`)                           | General Python practices                                              | Skipped: existing `src/core` conventions, `mypy`, and `ruff` rules are direct   |
| Research specialist | `hve-core-all:rpi-researcher`           | Host-registered subagent for independent research lane | Subagent lane artifact under `.copilot-tracking/research/subagents/`  | Skipped (inline): tightly coupled single-package trace across `src/core` files  |

## User Participation and Research Decisions

| Checkpoint       | Questions or no-interaction rationale                                                                 | Answers / unanswered | Resulting decision or selected further research                                    |
|------------------|-------------------------------------------------------------------------------------------------------|----------------------|------------------------------------------------------------------------------------|
| Intake           | Non-interactive continuous RPI execution with explicit scope, target files, and validation tier.      | Not asked            | Proceed in `focused` posture and `convergence` mode on `src/core` non-authority.   |
| Direction change | None during Cycle 1.                                                                                  | N/A                  | Retained `focused` posture and `src/core` boundary.                                |
| Convergence      | Non-interactive automatic RPI mode; Cycle 1 evidence converged cleanly on Option A without ambiguity. | Not asked            | Selected Option A (layered `src/core` invariant guards + end-to-end test suite).   |

## Scope and Success Criteria

* Scope: `src/core` production modules and unit/acceptance tests covering sensor ingestion, deterministic sensor analysis, store integration, home ranking, hazard diagnosis, statutory clocks, and hold/blocker lifecycle.
* Assumptions:
  * `sensor_ingest.py` and `sensor_analysis.py` already exist on `feat/demo-109-sensor-non-authority` (or its parent branch) and must be inspected directly rather than assumed.
  * Store, hazard, clock, hold, and ranking functions exist in `src/core` and may either ignore sensor signals passively or guard against sensor-originated authority actions.
* Success criteria:
  * Every research question is answered with exact `path:line` codebase evidence (`C#`).
  * All four forbidden authority effects (hazard diagnosis, clock start, hold release, ranking change) are traced across ingestion, analysis, and store/domain surfaces.
  * Contrarian wave tests subtle bypass vectors (e.g., crafted payload fields, actor/role spoofing, indirect task/signal consumption, store mutation side effects, ranking input leakage).
  * Self-check passes and Planning Readiness reaches `Ready`.

## Task Research Requests

* Explicit requests:
  * Deliver an explicit end-to-end invariant enforcement and acceptance test suite in `src/core` for Issue #109's core engineering criterion: `No sensor signal diagnoses a hazard, starts a clock, releases a hold or changes ranking`.
  * Prove across ingestion (`sensor_ingest.py`), deterministic sensor analysis (`sensor_analysis.py`), and store/ranking/hazard/hold surfaces that no sensor reading or derived sensor signal can diagnose a hazard, start an Awaab's Law or statutory clock, release a hold/blocker, or alter deterministic home ranking.
* Inferred research questions:
  * Q1: What do BRD FR-048, PRD FR-050 / AC-066..068, ADR 0002, and ADR 0003 require for sensor non-authority?
  * Q2: What is currently implemented in `sensor_ingest.py` and `sensor_analysis.py` (data models, outputs, task creation, store hooks)?
  * Q3: How are hazards diagnosed, statutory/Awaab's Law clocks started, holds/blockers released, and homes deterministically ranked in `src/core`?
  * Q4: Where could a sensor reading, derived sensor signal, or sensor-generated review task accidentally or maliciously cross the authority boundary, and what explicit invariant enforcement + end-to-end acceptance tests close and prove every path?
* Caller constraints and non-goals: Focused tier only (`src/core` unit tests, `mypy`, `ruff`); do not run `tools/rpi-checks.py`; do not push.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary                                                                                   | Source / checkpoint | Effect on active brief, evidence, or revalidation                          |
|----------------------------------------------------------|---------------------------------------------------------------------------------------------------------|---------------------|----------------------------------------------------------------------------|
| narrow                                                   | Scope implementation and proof to `src/core` across ingestion, analysis, store, ranking, hazard, hold   | User prompt         | Focuses codebase trace on `src/core` and its governing docs                |
| exclude                                                  | Do not run `tools/rpi-checks.py` and do not push to remote                                              | User prompt         | Validation restricted to `src/core` unittest, `mypy`, and `ruff`           |

## Research Questions

|  # | Sub-question                                                                                                                     | Type            | Priority | Status   |
|---:|----------------------------------------------------------------------------------------------------------------------------------|-----------------|----------|----------|
| Q1 | What exact non-authority rules are specified in BRD FR-048, PRD FR-050 / AC-066..068, ADR 0002, and ADR 0003?                    | straightforward | H        | answered |
| Q2 | What contracts, outputs, and mutations exist today in `sensor_ingest.py`, `sensor_analysis.py`, and existing sensor tests?       | depth           | H        | answered |
| Q3 | How do `src/core` store, hazard diagnosis, statutory clock start, hold/blocker release, and deterministic ranking operate today? | depth           | H        | answered |
| Q4 | What bypass vectors or implicit assumptions exist, and what invariant guard(s) + acceptance tests provide complete proof?        | depth           | H        | answered |

## Cycle 1

### Wave 1: Wider

* Execution mode: Inline (single tightly coupled package `src/core`; delegating to an isolated worker would duplicate context without independent-lane benefit).
* Breadth findings:
  * Governing requirements and architecture documents establish an absolute non-authority boundary for in-use monitoring across `docs/case_study_48_addendum.md`, BRD FR-048 and RULE-014 (`docs/brds/agentic-retrofit-programme-brd.md:1588-1589`), PRD FR-050 and AC-066..AC-068 (`docs/prds/zava-forward-retrofit-programme-demonstrator.md:1425,2162-2164`), ADR 0002 (`docs/adrs/0002-pilot-readiness-architecture.md:122-145`), and ADR 0003 (`docs/adrs/0003-journey-derived-capabilities-runtime-fit.md:94-112`) (`C1`..`C4`).
  * Under FR-048, RULE-014, FR-050, and AC-067, raw sensor observations and derived deterministic signals can at most propose a human condition-review candidate (`SENSOR_REVIEW_DUE` on queue `condition-assessment`) when an approved rule matches. Neither adverse readings nor the absence of a sensor alert (`NO_SIGNAL`), nor missing, stale, or declined monitoring, may diagnose a hazard, start or back-date an Awaab's Law or statutory clock, release a hold/blocker, override a resident report, or alter deterministic home ranking.
  * Mapped all relevant `src/core` modules: `sensor_ingest.py`, `sensor_consumer.py`, `sensor_analysis.py`, `sensor_analysis_store.py`, `sensor_review_draft.py`, `controls.py`, `workflows.py`, `doc_controls.py`, `gates.py`, `ranking.py`, `store.py`, `sqlstore.py`, and `taskqueues.py`.
  * Audited existing tests: `src/api/tests/test_sensor_non_authority_boundary.py` tests passive snapshot non-mutation in `src/api/tests/`, while `src/core/tests/` has unit suites for `sensor_ingest`, `sensor_analysis`, `sensor_analysis_store`, `sensor_analysis_reproducibility`, and `sensor_review_draft`, but lacks an explicit `src/core` end-to-end non-authority invariant enforcement and acceptance suite (`C17`, `C18`).

### Wave 2: Deeper

* Ingestion (`sensor_ingest.py` and `sensor_consumer.py`):
  * `ingest_window(consumer, observations, received_at)` (`src/core/src/zava_forward/core/sensor_ingest.py:29-54`) validates `received_at` and batch shape via `preflight`, routes each row through `SensorConsumer.process`, and returns `WindowReceipt(accepted, replayed, rejected)`.
  * `SensorConsumer._shape` and `_live_shape` (`src/core/src/zava_forward/core/sensor_consumer.py:712-775`) enforce closed field sets (`READING_FIELDS` / `LIVE_FIELDS`), rejecting unexpected keys with `"SCHEMA"` into `sensor_data_quality_exception`, and writing accepted rows exclusively to `sensor_reading` and `sensor_delivery` (`src/core/src/zava_forward/core/sensor_consumer.py:570-625`) without touching `cases`, `hazards`, `legal_hold`, `ranking`, or `audit` (`C5`, `C6`).
  * `handover_continuity` (`src/core/src/zava_forward/core/sensor_ingest.py:104-148`) computes synthetic continuity metrics read-only (`C5`).
* Deterministic analysis (`sensor_analysis.py` and `sensor_analysis_store.py`):
  * `Signal` (`src/core/src/zava_forward/core/sensor_analysis.py:106-125`) defines `priority_effect: str = "NONE"` and `diagnoses_hazard: bool = False`.
  * `ReviewTaskCandidate` (`src/core/src/zava_forward/core/sensor_analysis.py:128-147`) defines `task_type = "SENSOR_REVIEW_DUE"`, `queue = "condition-assessment"`, `status = "PROPOSED"`, `resident_report_unaffected: bool = True`, `changes_ranking: bool = False`, `starts_clock: bool = False`, `releases_hold: bool = False`, and `diagnoses_hazard: bool = False` (`C7`).
  * `derive_signal`, `review_task_candidate`, `reproduce_sensor_analysis`, `reproduce_review_task`, `analyse_retained`, and `reproduce_retained` (`src/core/src/zava_forward/core/sensor_analysis.py:390-585`, `src/core/src/zava_forward/core/sensor_analysis_store.py:72-198`) are pure/read-only and fail closed to `INSUFFICIENT` or `DECLINED` with `priority_effect = "NONE"` (`C8`, `C9`).
* Review drafts (`sensor_review_draft.py`):
  * `_propose` and `_persist` (`src/core/src/zava_forward/core/sensor_review_draft.py:210-302`) persist unapproved drafts solely under `case["sensor_review_drafts"]` (`STATE = "PROPOSED_UNAPPROVED"`, `manual_review_only = True`, `approval_verified = False`, `activation = None`) (`C10`).
* Store, hazard, clock, hold, gate, and ranking surfaces:
  * `WorkflowMixin` (`src/core/src/zava_forward/core/workflows.py:864-995`) owns `raise_hazard` (sets `aware_at` and opens an active safety hold), `refer_hazard`, `receive_hazard`, `accept_hazard`, `observe_hazard_times` (sets `response_due_at`, `responded_at`, `resident_update_due_at`, `resident_updated_at`), `record_repair`, and `release_hazard` (`C11`).
  * `controls.evidence_text` (`src/core/src/zava_forward/core/controls.py:53-65`) refuses chat-memory references (`MEMORY_REF`) across controlled evidence inputs, and `workflows.release_hazard` (`src/core/src/zava_forward/core/workflows.py:971-973`) re-checks stored `receipt_evidence`, `acceptance_evidence`, and `repair_evidence` before releasing a hold (`C12`).
  * `DocControlsMixin.place_legal_hold` and `release_legal_hold` (`src/core/src/zava_forward/core/doc_controls.py:219-237`) manage case legal holds, and `gates.safety_release_gate` / `gates.booking_gates` (`src/core/src/zava_forward/core/gates.py:142-245`) enforce safety and legal holds as transition blockers (`C13`, `C14`).
  * `ranking._rule_keys`, `ranking.sql_key`, `ranking.reasons`, `ranking.rank`, and `ranking.snapshot` (`src/core/src/zava_forward/core/ranking.py:78-157`) allowlist `{"safety_open", "support", "waiting_days", "stage_order", "case_id"}` and ignore all sensor fields on case dicts (`C15`).
  * `src/core/pyproject.toml` (`src/core/pyproject.toml:26-105`) configures `ruff==0.17.1` and `mypy==2.4.0` (`strict = true`), excluding legacy migrated files (`controls.py`, `workflows.py`, `doc_controls.py`, `ranking.py`) from `ruff format` while checking typed sensor modules and new test files strictly (`C16`).

### Wave 3: Contrarian

Challenged the assumption that passive separation alone guarantees Issue #109's non-authority invariant:

1. Constructor and `dataclasses.replace(...)` bypass in `sensor_analysis.py` and `sensor_ingest.py` (`C5`, `C7`):
   * `Signal` and `ReviewTaskCandidate` lack `__post_init__` validation, allowing callers or deserializers to construct or `replace(...)` instances with `diagnoses_hazard=True`, `priority_effect="HIGH"`, `starts_clock=True`, `releases_hold=True`, `changes_ranking=True`, `resident_report_unaffected=False`, `status="ACTIVE"`, `task_type != TASK_TYPE`, or `queue != TASK_QUEUE`.
   * `WindowReceipt` (`src/core/src/zava_forward/core/sensor_ingest.py:20-26`) does not yet expose or enforce explicit non-authority flags.
2. Direct sensor citation or metadata smuggling into hazard, clock, and hold surfaces (`C11`, `C12`, `C13`):
   * Unlike chat memory (`MEMORY_REF` in `controls.py:53-65`), `controls.evidence_text` currently accepts sensor telemetry, signal, rule, schema, and draft identifiers (`SENSOR_REVIEW_DUE`, `SENSOR-RH-PERSISTENCE-EXERCISE`, `sensor-analysis-exercise-v1`, `sensor-comparator-exercise-v1`, `sensor-review-draft-v1`, `sensor-fault-input-v1`, `sensor-live-weather-sim-v1`, `sensor_reading:...`, `sensor_signal:...`, `sensor_analysis:...`, `sensor_review_draft:...`, `SENS-SYN-...`).
   * Without an explicit sensor non-authority guard in `controls.py`, `workflows.py`, and `doc_controls.py`, a caller could cite a sensor reading or `NO_SIGNAL` output as `source` in `raise_hazard` (diagnosing a hazard and setting `aware_at`), as `evidence` in `observe_hazard_times` (starting/updating statutory clocks), as `evidence` in `record_repair` / `release_hazard` (releasing an active safety hold in violation of RULE-014 and AC-067), as `reference` in `place_legal_hold`, or smuggle `sensor_signal` / `sensor_reading` / `sensor_review_draft` / `sensor_candidate` keys in hazard workflow `metadata`.
   * Verified all 84 hazard/clock/repair/release call sites and all `evidence_text` / `place_legal_hold` callers across `src/`: zero legitimate human workflows use sensor artefact tokens, whereas exact token/prefix matching (rather than matching the plain English word `"sensor"`) prevents false positives on human surveyor inspection notes.
3. Digest-recomputed stored draft tampering in `sensor_review_draft.py` (`C10`):
   * `_view(record)` (`src/core/src/zava_forward/core/sensor_review_draft.py:163-185`) checks `record.get("draft_digest") != _digest(record)` but does not verify that `state == STATE`, `manual_review_only is True`, `approval_verified is False`, `activation is None`, and all candidate authority flags remain non-authoritative if a stored draft's digest was recomputed after tampering.
4. Inconsistent unknown-rule error in `ranking.sql_key` (`C15`):
   * `ranking._rule_keys` (`src/core/src/zava_forward/core/ranking.py:88-90`) raises `ValueError("Unknown ranking rule: ...")` on unauthorized sensor rules, whereas `ranking.sql_key` (`src/core/src/zava_forward/core/ranking.py:111-115`) raises `KeyError`. Both ranking paths should uniformly raise `ValueError("Unknown ranking rule: ...")`.

### Cycle 1 Synthesis

* Re-entry decision: No second cycle needed. Every question (`Q1`..`Q4`) is answered with exact `path:line` evidence (`C1`..`C18`), contrarian vectors are verified against existing tests across `src/`, and convergence on Option A is complete.

## Evidence Log

| ID  | Location                                                                     | Evidence summary                                                                                                                                    |
|-----|------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| C1  | `docs/brds/agentic-retrofit-programme-brd.md:1588-1589`                      | FR-048 and RULE-014 forbid sensor signals or absence of alerts from diagnosing hazards, starting clocks, releasing holds, or changing ranking.       |
| C2  | `docs/prds/zava-forward-retrofit-programme-demonstrator.md:1425,2162-2164`   | FR-050 and AC-066..AC-068 restrict signals to `SENSOR_REVIEW_DUE` proposals under approved rules with zero direct hazard/clock/hold/ranking effect. |
| C3  | `docs/adrs/0002-pilot-readiness-architecture.md:122-145`                     | ADR 0002 separates telemetry retention from statutory clocks, hazard diagnosis, safety/legal holds, and portfolio ranking.                          |
| C4  | `docs/adrs/0003-journey-derived-capabilities-runtime-fit.md:94-112`          | ADR 0003 Decision 6 restricts deterministic sensor signals to human condition-review candidate generation with no authority mutation.               |
| C5  | `src/core/src/zava_forward/core/sensor_ingest.py:20-54,104-148`              | `WindowReceipt`, `ingest_window`, `home_series`, and `handover_continuity` ingest via `SensorConsumer` and never mutate case/hazard/hold/ranking.   |
| C6  | `src/core/src/zava_forward/core/sensor_consumer.py:570-625,712-775`          | `SensorConsumer` writes only `sensor_*` tables and rejects extra schema fields as `"SCHEMA"` data-quality exceptions.                               |
| C7  | `src/core/src/zava_forward/core/sensor_analysis.py:106-147,480-505`          | `Signal` and `ReviewTaskCandidate` carry non-authority fields without `__post_init__` constructor enforcement.                                      |
| C8  | `src/core/src/zava_forward/core/sensor_analysis.py:390-478,510-622`          | `derive_signal`, `review_task_candidate`, `reproduce_sensor_analysis`, and `reproduce_review_task` are pure and fail closed.                        |
| C9  | `src/core/src/zava_forward/core/sensor_analysis_store.py:72-198`             | `analyse_retained` and `reproduce_retained` are read-only over retained indoor readings and exclude `sensor-live-weather-sim-v1`.                   |
| C10 | `src/core/src/zava_forward/core/sensor_review_draft.py:55-68,163-185,210-302`| `sensor_review_draft` writes only `case["sensor_review_drafts"]` (`PROPOSED_UNAPPROVED`); `_view` checks digest without re-checking authority flags.|
| C11 | `src/core/src/zava_forward/core/workflows.py:864-995`                        | `raise_hazard`, `refer_hazard`, `receive_hazard`, `accept_hazard`, `observe_hazard_times`, `record_repair`, and `release_hazard` own hazard/clocks.  |
| C12 | `src/core/src/zava_forward/core/controls.py:53-65`                           | `controls.evidence_text` blocks `MEMORY_REF`, providing the exact pattern for refusing sensor telemetry/signal/draft citations (`SENSOR_REF`).      |
| C13 | `src/core/src/zava_forward/core/doc_controls.py:219-237`                     | `place_legal_hold` and `release_legal_hold` enforce manager-only legal holds on cases.                                                              |
| C14 | `src/core/src/zava_forward/core/gates.py:142-245`                            | `safety_release_gate` and `booking_gates` enforce open hazard holds and legal holds as blockers without consulting sensor data.                     |
| C15 | `src/core/src/zava_forward/core/ranking.py:78-157`                           | `_rule_keys`, `rank`, `reasons`, and `snapshot` allowlist five non-sensor rules and ignore sensor keys; `sql_key` lacks the `ValueError` rule check.|
| C16 | `src/core/pyproject.toml:26-105`                                             | Configures `ruff==0.17.1` and `mypy==2.4.0` (`strict = true`) for `src/core` with legacy migrated modules excluded from `ruff format`.             |
| C17 | `src/core/tests/test_sensor_review_draft.py:1-340`                           | `src/core/tests/` has unit tests per sensor module but no end-to-end `src/core` non-authority invariant enforcement and acceptance suite.           |
| C18 | `src/api/tests/test_sensor_non_authority_boundary.py:1-265`                  | Existing `src/api` boundary fixture tests passive SQL snapshot stability across 5 homes, leaving `src/core` active invariant guards untested.       |

## Options and Selected Recommendation

| Option   | Summary                                                                                                                                               | Disposition | Evidence-based rationale                                                                                                                           |
|----------|-------------------------------------------------------------------------------------------------------------------------------------------------------|-------------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| Option A | Layered `src/core` runtime invariant enforcement (`sensor_analysis`, `sensor_ingest`, `sensor_review_draft`, `controls`, `workflows`, `doc_controls`, `ranking`) + end-to-end acceptance suite in `src/core/tests/test_sensor_non_authority.py`. | Selected    | Closes all four Contrarian bypass vectors in `src/core` and proves end-to-end passive + active non-authority across `Store` and `SqlStore` (`C5`..`C18`). |
| Option B | Add acceptance tests in `src/core/tests/` only without runtime invariant enforcement in `src/core` production modules.                                | Rejected    | Leaves `Signal`/`ReviewTaskCandidate` overrides and sensor citation smuggling into `workflows.py`/`controls.py` open (`C7`, `C11`, `C12`).          |
| Option C | Block plain English substring `"sensor"` in `controls.evidence_text`.                                                                                 | Rejected    | Risks false positives on human surveyor inspection prose; exact sensor artefact/prefix matching (`SENSOR_REF`) is precise and safe (`C12`).         |

## Decisions, Risks, and Readiness

* Current decisions:
  * Enforce strict boolean/value non-authority invariants in `Signal.__post_init__`, `ReviewTaskCandidate.__post_init__`, `enforce_sensor_non_authority(...)` (`sensor_analysis.py`), `WindowReceipt.__post_init__` (`sensor_ingest.py`), and `sensor_review_draft._propose` / `_view`.
  * Add `SENSOR_REF`, `SENSOR_REFUSAL`, and `is_sensor_reference(value)` in `controls.py` (refused by `controls.evidence_text`), reject sensor payload metadata keys and stored sensor evidence in `workflows.py` and `doc_controls.py`, and align `ranking.sql_key` unknown-rule validation to raise `ValueError("Unknown ranking rule: ...")`.
  * Implement `src/core/tests/test_sensor_non_authority.py` covering `sensor_ingest.py`, `sensor_analysis.py`, `sensor_analysis_store.py`, `sensor_review_draft.py`, `Store`, `SqlStore`, `ranking.py`, hazards, Awaab's Law / statutory clocks, and safety/legal/gate holds.
* Open risks / blockers: None.
* Further research (deferred outside slice): Issue #440 stabilization checkpoint and live IoT Hub / Azure SQL cloud acceptance drill remain separate Epic #109 items.
* Research disposition: `executed`
* Planning Readiness: `Ready`

## Self-Check and Continuation Record

* Research-only constraint: Verified (`git status --short` has no production/test file edits).
* Three-wave completion: Verified (Cycle 1 Wider, Deeper, Contrarian, and Synthesis completed in order with `C1`..`C18`).
* Continuation: Active confirmed automatic RPI Agent parent advances directly to `rpi-plan`.
