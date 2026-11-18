---
title: "Task Research: 111-sensor-reproducibility-2142"
description: "Deterministic versioned sensor analysis and review task generation with explicit version provenance from retained readings (Refs #111)"
ms.date: 2026-11-14
---

| Field | Value |
| --- | --- |
| Date | 2026-11-14 |
| Researcher / agent | rpi-research (RPI Agent) |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-11-14/111-sensor-reproducibility-2142-research.md |

## Research Brief

* What to research: How `src/core` derives deterministic, versioned sensor signals and `SENSOR_REVIEW_DUE` human review task candidates from retained readings, what version provenance and digest guarantees currently hold, and what gaps prevent end-to-end deterministic reproduction from retained readings alone (pure and retained-store layers).
* Why it matters: Issue #111 criterion 1 ("Outputs are reproducible from retained readings") and PRD FR-050 / AC-067 / AC-068 / ADR 0003 decision 6 require sensor analysis and `SENSOR_REVIEW_DUE` proposal generation to be pure functions of retained readings, consent, window, `as_of`, and an explicit versioned policy, with fail-closed `INSUFFICIENT` handling and explicit version provenance.
* Audience or intended use: Planning, implementation, and review phases for `feat/iot-111-sensor-reproducibility-2142` in `src/core`.
* Scope: `src/core/src/zava_forward/core/sensor_analysis.py`, `src/core/src/zava_forward/core/sensor_analysis_store.py`, `src/core/README.md`, and `src/core/tests/test_sensor_analysis*.py` (preserving compatibility with `sensor_review_draft.py` and `src/api/tests/`).
* Non-goals: Live Azure IoT Hub or SQL Server provisioning, completing analytics research phases R1 to R3, changing threshold values from labelled exercise values, creating operational workflow tasks directly, modifying UI screens, or pushing to remote.
* Criteria: Pure and retained-store reproduction of both `Signal` and `ReviewTaskCandidate` (`SENSOR_REVIEW_DUE`) with explicit version provenance (`VersionProvenance`), collision-free canonical input/policy/output digests, no raw readings or sensor identifiers in outputs, strict `mypy` and `ruff` compliance in `src/core`, and green `test_*sensor*.py` suite.
* Requested outputs: Dated primary research artifact with convergence recommendation for `rpi-plan`.
* Output mode: convergence

## Research Parameters

| Field | Value |
| --- | --- |
| Research question(s) | Q1-Q4 below |
| Codebase scope | `src/core/`, `src/api/tests/test_sensor_*`, `docs/adrs/0003-*`, `docs/prds/zava-forward-*`, `docs/reference/research/iot-sensor-analytics-research-plan.md` |
| External scope | none (bounded internal codebase and repository specifications) |
| Initial internal candidate areas | `src/core/src/zava_forward/core/sensor_analysis.py`, `sensor_analysis_store.py`, `sensor_review_draft.py`, `synthetic/sensor_scenarios.py` |
| Initial external candidate areas | none |
| Research posture | focused |
| Posture provenance | default (bounded internal task with named `src/core` target and verification command) |
| Explicit limits / deadline | Deliver in `src/core` on branch `feat/iot-111-sensor-reproducibility-2142`; do not push |
| Posture-specific completion basis | focused scope and materiality |
| Edits allowed during research? | no, research-only |
| Resolved evidence root | `.copilot-tracking/` |
| Known constraints / excluded sources | Keep labelled exercise values (`EXERCISE VALUE`); never lower priority on `INSUFFICIENT`/`STALE`/`DECLINED`; preserve existing `Signal` and `ReviewTaskCandidate` serialized keys expected by `sensor_review_draft.py` |

## Extension Registry and Provenance

* Precedence: platform and host safety; caller scope and criteria; matching repository instructions and enforced schemas; rpi-research contract; domain skills and specialists; examples and preferences.

| Kind | Candidate | Match and provenance | Scoped authority or output contract | Selected / skipped reason |
| --- | --- | --- | --- | --- |
| Instruction | `.github/copilot-instructions.md` | `applyTo: "**"` matches repository files and tracking artifacts | Enforces AMA knowledge-base reading, tier classification disclosure, `Refs #111` discipline, and Markdown style | Selected: mandatory repository governance |
| Skill | `python-foundational` | Python typing and unit testing conventions | Strict typing and standard-library `unittest` patterns | Skipped: `src/core/pyproject.toml` already enforces strict `mypy` and `ruff` rules directly |
| Research specialist | `hve-core-all:rpi-researcher` | General internal research lane subagent | Compact lane evidence artifact | Skipped: inline fallback used because all 4 target modules fit direct inspection in <6 reads with tight coupling |

## User Participation and Research Decisions

| Checkpoint | Questions or no-interaction rationale | Answers / unanswered | Resulting decision or selected further research |
| --- | --- | --- | --- |
| Intake | Non-interactive execution with explicit branch, worktree, `src/core` target, acceptance criteria, and verification command | No interaction needed | Proceed in confirmed automatic mode with focused posture; inspect and carry forward/harden uncommitted worktree edits on `feat/iot-111-sensor-reproducibility-2142` |
| Direction change | Worktree already held an uncommitted partial diff in `sensor_analysis.py` and `test_sensor_analysis.py` | Preserved per repository dirty-worktree rule (same branch/task) | Retain and harden `reproduce_review_task` while fixing four defects found during contrarian review |
| Convergence | Cycle 1 answered Q1-Q4 completely from primary repository code and specs | No interaction needed | Advance to `rpi-plan` |

## Scope and Success Criteria

* Scope: Deterministic versioned sensor analysis, `SENSOR_REVIEW_DUE` candidate generation, and explicit version provenance from retained readings in `src/core` (`sensor_analysis.py`, `sensor_analysis_store.py`, `src/core/README.md`, and `src/core/tests/test_sensor_analysis*.py`).
* Assumptions: Existing uncommitted changes in `sensor_analysis.py` and `test_sensor_analysis.py` in this dedicated worktree belong to this task and must be preserved and hardened rather than discarded; shared `~/.local` editable installs point to `/home/azureuser/source/ama/src/core`, so isolated `venv` or `PYTHONPATH=src` verification is required to avoid mutating shared user site-packages.
* Success criteria:
  * Every research question is answered with `C#` codebase evidence.
  * Evidence locations use `path:line`.
  * Findings, decisions, and readiness claims cite Evidence Log IDs.
  * Alternatives are compared with trade-offs and rejection rationale.
  * Open questions, risks, and validation-tier boundaries are recorded.
  * Self-check passes.

## Task Research Requests

* Explicit requests: Deliver locally verifiable acceptance criteria in `src/core` for Issue #111: outputs are reproducible from retained readings (deterministic versioned sensor analysis and review task generation with explicit version provenance); write all 4 `.copilot-tracking/` artifacts; verify with `mypy`, `ruff check .`, `ruff format --check .`, and `unittest discover -s tests -p 'test_*sensor*.py' -v`; commit cleanly without pushing.
* Inferred research questions: How do `derive_signal`, `reproduce_sensor_analysis`, `review_task_candidate`, and `sensor_analysis_store.analyse_retained` handle input canonicalization, digests, version provenance, approval mismatches, empty retained windows, and downstream callers?
* Caller constraints and non-goals: Local `src/core` delivery only; do not claim R1-R3 completion, operational rule activation, or full external gate / hosted CI completion; do not push.

## Direction Controls

| Control type (add / change / narrow / exclude / discard) | Direction or boundary | Source / checkpoint | Effect on active brief, evidence, or revalidation |
| --- | --- | --- | --- |
| narrow | Restrict code delivery to `src/core` and verify with bare `mypy`, `ruff`, and `test_*sensor*.py` | Caller prompt | Keep `Signal` and `ReviewTaskCandidate` serialized shapes compatible with `sensor_review_draft.py` and `src/api/tests/` |
| exclude | Do not push to remote; leave `git status --short` empty after commit | Caller prompt | Record full-tier SQL/external receipt and hosted CI as post-commit publication prerequisites rather than executed checks |

## Research Questions

| # | Sub-question | Type (depth / breadth / straightforward) | Priority | Status |
| ---: | --- | --- | --- | --- |
| Q1 | What versioned sensor analysis and `SENSOR_REVIEW_DUE` task-candidate interfaces already exist in `src/core` and who calls them? | breadth | H | answered |
| Q2 | What explicit version provenance fields and digests are required to prove deterministic reproduction from retained readings alone across pure and SQL-retained entry points? | depth | H | answered |
| Q3 | Can two distinct retained-reading inputs share an `input_digest`, or can mismatched approvals/versions leak into provenance or task candidates? | depth | H | answered |
| Q4 | How does the shared environment resolve `zava_forward.core` during `mypy`, `ruff`, and `unittest` runs in this worktree? | straightforward | M | answered |

## Prior Knowledge Gate

* Existing artifacts reviewed: `.copilot-tracking/research/2026-11-14-issue-111-sensor-repro-research.md`, `.copilot-tracking/research/2026-11-14-issue-109-111-sensor-authority-reproducibility-0900-research.md`, `.copilot-tracking/research/2026-11-14-sensor-view-reproducibility-research.md`, `docs/adrs/0003-journey-derived-capabilities-runtime-fit.md`, `docs/prds/zava-forward-retrofit-programme-demonstrator.md`, `docs/reference/research/iot-sensor-analytics-research-plan.md`.
* Reused (verified) findings: `sensor_analysis.derive_signal` sorts rows canonically before calling `comparator.analyse` (C2); `sensor_review_draft.py` wraps `ReviewTaskCandidate` as default-off unapproved drafts and checks exact serialized candidate keys (C5); exercise thresholds must carry `EXERCISE VALUE` prefix until R1-R3 complete (C1, C6, C7).
* Superseded / stale: Earlier `2026-11-14-issue-111-sensor-repro-research.md` covered only pure `reproduce_sensor_analysis` for `Signal` without `SENSOR_REVIEW_DUE` review task reproduction, full version provenance (`comparator_version`, `schema_version`, `policy_digest`, `output_digest`), or a retained-store reproduction entry point; the editable install in `~/.local` still points to `/home/azureuser/source/ama/src/core` (Nov 4 checkout) rather than this worktree (C10).

## Research Cycle Log

### Cycle 1

* Active direction controls: narrow (`src/core` scope), exclude (no push)
* Active research posture and completion basis: focused; focused scope and materiality
* Explicit limits or deadline effect: Keeps changes surgical inside `src/core` while preserving `src/api` caller contracts.

#### Wave 1: Wider

* Plan and independent lanes: Survey requirements (Issue #111, PRD FR-050/AC-067/AC-068, ADR 0003 decision 6), all `sensor_*` modules in `src/core`, downstream callers in `src/api`, and existing worktree diff.
* Worker evidence relationships or inline fallback: Inline inspection mapped Q1 -> C1-C8 and Q4 -> C9-C10.
* Reflection: `sensor_analysis.py` has `derive_signal`, `reproduce_sensor_analysis`, `review_task_candidate`, and an uncommitted draft of `reproduce_review_task`, while `sensor_analysis_store.py` only exposes `analyse_retained` (returning `Signal` alone). `sensor_review_draft.py` pins `_VIEW_CANDIDATE` and `_VIEW_LINEAGE` keys.

#### Wave 2: Deeper

* Parent-prioritized material from Wave 1: Inspect exact digest inputs (`reading_tuples`, `_quality_tuples`), comparator checks (`sensor_scenarios.analyse`), task key construction (`review_task_candidate`), retained-store failure modes (`analyse_retained`), and `mypy`/`ruff` configuration (`pyproject.toml`).
* Plan and independent lanes: Trace every field read by `comparator.analyse` against `_digest`, trace `RuleApproval` validation and matching against `AnalysisPolicy.rule_approved`, and trace `sensor_analysis_store.analyse_retained` under `ConsumerError`, weather-only rows, and consent states.
* Worker evidence relationships or inline fallback: Inline trace mapped Q2 and Q3 -> C2, C3, C4, C5, C8.
* Reflection: Found concrete provenance completeness gaps: `comparator.METHOD_VERSION` (`sensor-comparator-exercise-v1`) and `sensor_faults.SCHEMA_VERSION` (`reading-v1`) are used by the comparator but absent from provenance; policy threshold overrides (`humidity_threshold_pct`, `max_staleness_hours`) under an unchanged `policy.version` string have no `policy_digest` or `output_digest`; `sensor_analysis_store` lacks a retained-store reproduction function that emits provenance + signal + candidate together.

#### Wave 3: Contrarian

* In-scope challenge targets and boundaries: Challenge whether `_digest`, `_home_and_window`, `review_task_candidate`, and the uncommitted `reproduce_review_task` draft are truly deterministic functions of retained readings and policy across edge and fault inputs, and whether changing `Signal`/`ReviewTaskCandidate` dataclasses would break downstream consumers.
* Plan and independent lanes: Test contrarian inputs mentally and against callers: (a) duplicate `reading_id` or missing `injected_fault` field with identical `(sensor_id, observed_at, metric, value, unit, calibrated, source_type, schema_version)`, (b) unapproved `RuleApproval` with mismatched `rule_id` or `policy_version`, (c) stale `Signal` with mismatched `analysis_version` passed to `review_task_candidate`, (d) empty retained reading slice `[]` for a known `(home_id, window)`, (e) non-string/missing `home_id` in row mappings, and (f) changing `Signal`/`ReviewTaskCandidate` fields vs keeping provenance in a dedicated `VersionProvenance` structure.
* Worker evidence relationships or inline fallback: Contrarian verification established four real defects (C2, C3, C8) and disproved adding fields directly onto `ReviewTaskCandidate` because `test_sensor_review_draft.py:249` and `sensor_review_draft.py:42` lock its serialized schema (C5).
* Reflection: Keeping `Signal` and `ReviewTaskCandidate` fields intact while introducing `VersionProvenance`, `version_provenance()`, hardened `_digest()`, hardened `_home_and_window()`, `reproduce_review_task()`, and `sensor_analysis_store.reproduce_retained()` fixes every contrarian defect without breaking any `src/core` or `src/api` contract.

#### Parent Synthesis and Disposition

| Material / claim | Evidence IDs or worker pointers | Parent disposition (accepted / rejected / deferred) | Evidence-based rationale | Primary-artifact treatment |
| --- | --- | --- | --- | --- |
| Include `reading_id` and canonical schema-validity flag in `_quality_tuples` for `input_digest` | C2, C8 | accepted | `comparator.analyse` checks `reading_id` duplicates/emptiness and exact `READING_FIELDS` string schema; omitting them allows digest collisions with divergent `Signal` outcomes, and hashing leaks no raw IDs | Selected recommendation |
| Add `VersionProvenance` dataclass and `version_provenance()` with `analysis_version`, `comparator_version`, `schema_version`, `policy_version`, `policy_digest`, `threshold_label`, `humidity_threshold_pct`, `max_staleness_hours`, `rule_id`, `rule_approved`, `approver_role`, `approval_reference` (only when `rule_approved`), `home_id`, `window_start`, `window_end`, `as_of`, `input_digest`, and `output_digest` | C1, C2, C3, C8 | accepted | Proves complete version, policy, approval, window, input, and output provenance while masking unapproved/mismatched `RuleApproval` references | Selected recommendation |
| Support optional `home_id` on `reproduce_sensor_analysis` and `reproduce_review_task`, and reject missing/non-string row `home_id` | C2, C3 | accepted | Allows pure reproduction of empty retained windows (`NO_READINGS_IN_WINDOW`) when `home_id` and `window` are supplied, while rejecting mixed or malformed `home_id` rows | Selected recommendation |
| Check `signal.analysis_version == ANALYSIS_VERSION` in `review_task_candidate` | C2 | accepted | Prevents minting a `SENSOR_REVIEW_DUE` candidate from a `Signal` produced by a different `analysis_version` | Selected recommendation |
| Add read-only `reproduce_retained` in `sensor_analysis_store.py` | C4 | accepted | Pairs `analyse_retained`, `review_task_candidate`, and `version_provenance` over SQL-retained readings with fail-closed `INSUFFICIENT` semantics and zero writes | Selected recommendation |
| Mutate `ReviewTaskCandidate` or `task_key` formula | C5 | rejected | `sensor_review_draft.py` and `test_sensor_review_draft.py` assert exact `as_dict(candidate)` equality and idempotent `task_key` across `as_of` shifts | Alternative 1 rejected |
| Modify shared `~/.local` editable pip install | C9, C10 | rejected | Environment is shared across concurrent worktrees; verify via isolated temporary venv (`--system-site-packages` + editable `src/core`) so bare commands succeed safely | Operational safeguard |

#### Cycle Re-entry Evaluation

* Another complete three-wave cycle needed: no
* Trigger or stop basis: All research questions (Q1-Q4) are answered from primary repository files (`C1`-`C10`), contrarian edge cases are resolved, and no external uncertainty exists within the exercise scope.
* Revised brief or revalidation required: none
* Readiness effect: Ready

## Evidence Log

* Delegation: inline: bounded four-module `src/core` slice where tight coupling between `sensor_analysis.py`, `sensor_scenarios.py`, `sensor_analysis_store.py`, and `sensor_review_draft.py` made direct single-context inspection faster and more accurate.

### Codebase Evidence

| ID | Claim / finding | Location (`path:line`) | Tool | Confidence | Notes |
| --- | --- | --- | --- | --- | --- |
| C1 | PRD FR-050, AC-067, AC-068 and ADR 0003 decision 6 require deterministic versioned signals reproducible from retained readings, labelled sufficiency, exercise-labelled thresholds until R1-R3 complete, `SENSOR_REVIEW_DUE` tasks only from approved rules, no priority reduction on `INSUFFICIENT`/`DECLINED`, and no raw readings or device IDs in outputs | `docs/adrs/0003-journey-derived-capabilities-runtime-fit.md:149` | view / grep | high | Confirmed against `docs/prds/zava-forward-retrofit-programme-demonstrator.md:384` (`FR-050`, `AC-067`, `AC-068`) |
| C2 | `sensor_analysis.py` defines `ANALYSIS_VERSION`, `RULE_ID`, `TASK_TYPE = "SENSOR_REVIEW_DUE"`, `RuleApproval`, `AnalysisPolicy`, `Signal`, `ReviewTaskCandidate`, `_digest`, `derive_signal`, `reproduce_sensor_analysis`, and `review_task_candidate`; `_quality_tuples` omits `reading_id` and schema completeness, and `review_task_candidate` checks `signal.policy_version == policy.version` without checking `signal.analysis_version == ANALYSIS_VERSION` | `src/core/src/zava_forward/core/sensor_analysis.py:19` | view | high | Lines 19-336 |
| C3 | Uncommitted working-tree diff on `feat/iot-111-sensor-reproducibility-2142` extracts `_home_and_window` and drafts `reproduce_review_task`, but populates `provenance["approval_reference"]` even when `policy.rule_approved` is `False`, coerces missing/None `home_id` via `str(...)`, cannot reproduce an empty retained window even with known `(home_id, window)`, and omits `comparator_version`, `schema_version`, `policy_digest`, and `output_digest` | `src/core/src/zava_forward/core/sensor_analysis.py:246` | bash (`git diff`) / view | high | Lines 246-367 in working tree |
| C4 | `sensor_analysis_store.analyse_retained` reads retained envelopes and consent read-only, filters `LIVE_VERSIONS` weather rows (`WEATHER_NOT_INDOOR`), and fails closed on `ConsumerError` (`RETAINED_READINGS_UNAVAILABLE`), returning `Signal` only with no combined provenance + `ReviewTaskCandidate` reproduction helper | `src/core/src/zava_forward/core/sensor_analysis_store.py:21` | view | high | Tested in `src/core/tests/test_sensor_analysis_store.py:39` and `test_sensor_analysis_mssql.py:42` |
| C5 | `sensor_review_draft.py` pins `_VIEW_CANDIDATE` (15 fields) and `_VIEW_LINEAGE` (11 fields), and `test_sensor_review_draft.py` asserts exact `record["candidate"] == sa.as_dict(expected)` and `task_key` stability across `as_of` changes | `src/core/src/zava_forward/core/sensor_review_draft.py:42` | view | high | Confirmed in `src/core/tests/test_sensor_review_draft.py:249` and `276` |
| C6 | `iot-sensor-analytics-research-plan.md` confirms R1-R3 remain open and all indoor humidity/persistence rules remain labelled synthetic exercise values | `docs/reference/research/iot-sensor-analytics-research-plan.md:11` | view | high | Prohibits claiming operational rule sign-off or `Closes #111` |
| C7 | `src/README.md` classifies `sensor_analysis.py` under the SQL group requiring the complete external gate (`rpi-checks.py --all`) and hosted CI before PR publication/merge | `src/README.md:274` | grep / view | high | Must disclose unexecuted full gate and hosted CI in local no-push cycle |
| C8 | `synthetic/sensor_scenarios.py` defines `METHOD_VERSION = "sensor-comparator-exercise-v1"` and `analyse()`, which checks `set(row) == set(sensor_faults.READING_FIELDS)`, `all(isinstance(v, str) ...)`, `reading_id` non-emptiness and uniqueness (`DUPLICATE`), `SCHEMA_VERSION` (`reading-v1`), calibration, units, and domain bounds | `src/core/src/zava_forward/core/synthetic/sensor_scenarios.py:16` | view | high | Lines 16 and 114-160 |
| C9 | `src/core/pyproject.toml` configures strict `mypy` (`files = ["src", "tests"]`, `strict = true`) and `ruff` (`line-length = 100`, `select = ["E", "F", "I", "B", "UP"]`); `sensor_analysis.py`, `sensor_analysis_store.py`, and their tests have no `ignore_errors` override and must typecheck strictly | `src/core/pyproject.toml:34` | view | high | Lines 25-40 |
| C10 | Shared user site-packages (`~/.local/lib/python3.12/site-packages/__editable__.zava_forward_core-0.1.0.pth`) points to `/home/azureuser/source/ama/src/core` (`50c5a0902`), causing bare `python3 -m unittest` without worktree installation or `PYTHONPATH=src` to import stale modules | `src/core/pyproject.toml:1` | bash (`pip show`) | high | Use an isolated `/tmp` venv (`--system-site-packages` + `--no-deps -e src/core`) to run the exact bare verification command without mutating shared `~/.local` |

### External Evidence

| ID | Claim / finding | Source (title) | URL | Retrieved | Version/date | Confidence |
| --- | --- | --- | --- | --- | --- | --- |

### Contradictions / Conflicts

* none

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence IDs | Confidence | Decision or readiness implication |
| --- | --- | --- | --- | --- |
| Q1 | `sensor_analysis` provides `derive_signal`, `reproduce_sensor_analysis`, and `review_task_candidate`; `sensor_analysis_store` provides `analyse_retained`; `sensor_review_draft` and `src/api/tests/test_sensor_analysis_reproducibility.py` consume them directly | C2, C4, C5 | high | Preserve existing public signatures and dataclass fields while adding explicit provenance and review-task reproduction |
| Q2 | Complete deterministic reproduction requires explicit `VersionProvenance` binding `analysis_version`, `comparator_version`, `schema_version`, `policy_version`, `policy_digest`, `threshold_label`, `humidity_threshold_pct`, `max_staleness_hours`, `rule_id`, `rule_approved`, `approver_role`, `approval_reference` (gated on `rule_approved`), `home_id`, `window_start`, `window_end`, `as_of`, `input_digest`, and `output_digest` across both pure (`reproduce_review_task`) and store (`reproduce_retained`) entry points | C1, C2, C3, C4, C8 | high | Implement `VersionProvenance`, `version_provenance()`, `reproduce_review_task()`, enriched `reproduce_sensor_analysis()`, and `sensor_analysis_store.reproduce_retained()` |
| Q3 | `_quality_tuples` omitted `reading_id` and schema validity, allowing digest collisions with distinct `DUPLICATE`/`SCHEMA_FIELDS` outcomes; uncommitted `reproduce_review_task` leaked `approval_reference` when `rule_approved` was `False`; `review_task_candidate` omitted `signal.analysis_version == ANALYSIS_VERSION`; `_home_and_window` coerced `None` `home_id` and disallowed empty reading slices even with explicit `(home_id, window)` | C2, C3, C8 | high | Fix all four edge cases in `sensor_analysis.py` and cover each with focused unit tests |
| Q4 | Shared `~/.local` editable install points to `/home/azureuser/source/ama/src/core`; running bare `mypy`, `ruff`, and `unittest` inside an isolated `/tmp` venv with `-e src/core --no-build-isolation --no-deps` exercises this worktree cleanly without mutating shared user state | C9, C10 | high | Use a temporary `/tmp` venv during verification and remove any temporary files before finishing |

## Key Discoveries

* `_digest` in `sensor_analysis.py` previously omitted `reading_id` and row-schema validity even though `comparator.analyse` branches on duplicate/empty `reading_id` and exact `READING_FIELDS` string keys (C2, C8).
* Gating `approver_role` and `approval_reference` in `VersionProvenance` on `policy.rule_approved` prevents a mismatched `RuleApproval` (wrong `rule_id` or `policy_version`) from appearing as active provenance when `review_task` is `None` (C2, C3).
* Adding `policy_digest` and `output_digest` alongside `input_digest`, `analysis_version`, `comparator_version`, `schema_version`, and `policy_version` proves both input-only invariance (policy changes preserve `input_digest`) and full output determinism across row permutations, redeliveries, batch sizes, and fresh processes (C1, C2, C8).

## Alternatives and Decision State

### Selected Recommendation (convergence only)

* Approach: Introduce frozen `VersionProvenance` and pure `version_provenance(signal, policy, candidate)` in `sensor_analysis.py`; harden `_digest` (include `reading_id` and canonical schema validity in `_quality_tuples`), `_home_and_window` (strict string `home_id` validation plus optional `home_id` parameter supporting empty retained slices when `window` is supplied), and `review_task_candidate` (require `signal.analysis_version == ANALYSIS_VERSION`); deliver pure `reproduce_review_task(...)` and backwards-compatible `provenance`/`output_digest` metadata on `reproduce_sensor_analysis(...)`; add read-only `reproduce_retained(...)` in `sensor_analysis_store.py`; update `src/core/README.md` and `src/core/tests/test_sensor_analysis*.py`.
* Rationale: Delivers deterministic versioned sensor analysis and `SENSOR_REVIEW_DUE` review task reproduction with explicit version provenance at both pure and SQL-retained layers without altering `Signal` or `ReviewTaskCandidate` schemas relied upon by `sensor_review_draft.py` and `src/api`.
* Evidence refs: C1, C2, C3, C4, C5, C8, C9
* Implementation impact: `src/core/src/zava_forward/core/sensor_analysis.py`, `src/core/src/zava_forward/core/sensor_analysis_store.py`, `src/core/README.md`, `src/core/tests/test_sensor_analysis.py`, `src/core/tests/test_sensor_analysis_store.py`, `src/core/tests/test_sensor_analysis_reproducibility.py`.
* Confidence: high: all callers in `src/core` and `src/api` are statically known and locally testable.

File tree:

```text
src/core/
  README.md
  src/zava_forward/core/
    sensor_analysis.py
    sensor_analysis_store.py
  tests/
    test_sensor_analysis.py
    test_sensor_analysis_reproducibility.py
    test_sensor_analysis_store.py
```

### Alternative: Embed new provenance fields directly on `Signal` and `ReviewTaskCandidate`

* Approach: Add `comparator_version`, `schema_version`, `policy_digest`, and `output_digest` attributes directly to `Signal` and `ReviewTaskCandidate`, and incorporate policy thresholds into `ReviewTaskCandidate.task_key`.
* Trade-offs: Co-locates fields on existing dataclasses, but changes `as_dict(candidate)` and `as_dict(signal)` payloads consumed by `sensor_review_draft.py` (`_VIEW_CANDIDATE` allowlist and `test_sensor_review_draft.py` equality assertions) and alters persisted draft digests.
* Evidence refs: C2, C5
* Rejection rationale: Breaks existing `sensor_review_draft` schema contracts unnecessarily when a dedicated `VersionProvenance` envelope cleanly separates provenance metadata from the candidate record.

### Alternative: Pure-only `reproduce_review_task` without `sensor_analysis_store.reproduce_retained`

* Approach: Ship only `sensor_analysis.reproduce_review_task` over in-memory row sequences and leave `sensor_analysis_store` returning `Signal` alone.
* Trade-offs: Minimal diff, but leaves SQL-retained reading callers manually stitching `analyse_retained`, `review_task_candidate`, and provenance construction across fail-closed store error and outdoor-weather filtering paths.
* Evidence refs: C3, C4
* Rejection rationale: Providing `sensor_analysis_store.reproduce_retained` ensures retained SQL store paths (including `RETAINED_READINGS_UNAVAILABLE`, `WEATHER_INPUT_NOT_INDOOR_MEASUREMENT`, and declined/unknown consent) emit the exact same deterministic provenance envelope as pure row reproduction.

## Open Questions, Risks, and Residual Uncertainty

* Blocking: none
* Important: Research phases R1 to R3 in `docs/reference/research/iot-sensor-analytics-research-plan.md` remain open before any derived measure is used beyond a labelled exercise rule (C6); `src/README.md` maps `sensor_analysis.py` to the Full SQL gate (`rpi-checks.py --all` with `ZF_SENSOR_MSSQL=1` and external verified receipt) plus hosted CI before PR publication/merge (C7).
* Follow-up: Wire approved policy governance and SQL Server `ZF_SENSOR_MSSQL=1` reproducibility suite in the full publication gate before merging any PR touching `sensor_analysis.py`.
* Residual uncertainty: Live Azure SQL Server restart persistence and R1-R3 standards confirmation are outside this local `src/core` slice and remain explicitly unclaimed.

## Current Decisions

| Decision | Status (proposed / confirmed / deferred / superseded) | Owner / source (user / evidence / constraint) | Rationale | Evidence IDs | Implications |
| --- | --- | --- | --- | --- | --- |
| Keep `ANALYSIS_VERSION = "sensor-analysis-exercise-v1"` and `EXERCISE VALUE` labels | confirmed | constraint (ADR 0003, analytics research plan) | R1-R3 are incomplete; thresholds must remain labelled exercise values | C1, C2, C6 | Commit references `Refs #111`, never `Closes #111` |
| Preserve `Signal` and `ReviewTaskCandidate` field sets and expose `VersionProvenance` via `version_provenance`, `reproduce_review_task`, `reproduce_sensor_analysis`, and `sensor_analysis_store.reproduce_retained` | confirmed | evidence | Preserves `sensor_review_draft` and `src/api` compatibility while delivering complete version provenance | C2, C4, C5, C8 | Zero breaking changes to existing callers |
| Verify bare commands via an isolated `/tmp` venv without modifying shared `~/.local` | confirmed | constraint (shared environment) | Avoids cross-worktree interference while proving exact bare `mypy`, `ruff`, and `unittest` invocations | C9, C10 | Clean temporary venv removal after verification |

## Unresolved Decisions

| Decision | Smallest evidence or answer needed | Owner | Impact | Blocker status |
| --- | --- | --- | --- | --- |
| R1-R3 analytics method and threshold sign-off | Competent reviewer confirmation against primary standards and synthetic validation | Programme / Technical Lead | Required before non-exercise rule approval (`Issue #111` criterion 3) | follow-up |
| Full publication gate (`rpi-checks.py --all` + `ZF_SENSOR_MSSQL=1` + hosted CI) | External full receipt and PR run when owner authorizes push | Delivery Coordinator / Owner | Required before PR publication/merge per `src/README.md:274` | follow-up |

## Potential Next Research

| Priority | Research item | Expected value | Trigger | Selected? | Related questions / evidence |
| --- | --- | --- | --- | --- | --- |
| M | R1-R3 primary-source confirmation for dew-point margin and humidity persistence | Enables operational rule approval beyond exercise thresholds | Owner schedules analytics research phases R1-R3 | deferred | Q1; C1, C6 |

## Planning Readiness

* Status: Ready
* Decision state: Convergence recommendation selected (pure + retained-store deterministic reproduction with `VersionProvenance` and collision-free digests).
* Evidence basis: C1, C2, C3, C4, C5, C6, C7, C8, C9, C10
* Preconditions met: Target files, caller contracts, edge cases, typing/linting rules, and verification commands are fully established.
* Blockers: none
* Smallest action to change readiness: none (ready for `rpi-plan`)

## Closeout Record

| Field | Record |
| --- | --- |
| Research execution status | Complete |
| Completed waves | Wider, Deeper, and Contrarian completed in order for Cycle 1 |
| Lane evidence or inline fallback | Inline fallback used: tightly coupled four-module `src/core` slice inspected directly |
| Research disposition | executed |
| Planning Readiness | Ready (C1-C10) |
| Blockers | none |
| Continuation owner and state | Confirmed automatic RPI Agent; automatic continuation to `rpi-plan` |

## Advisory Next Step

| Field | Record |
| --- | --- |
| Research disposition | executed |
| Planning Readiness | Ready (C1-C10) |
| Output mode and planning support | convergence; yes, single evidence-backed design selected |
| Acting owner | confirmed automatic RPI Agent |
| Required gates or confirmations | Research disposition recorded (passed); Planning Readiness Ready (passed); pre-transition state write (passed) |
| Continuation result | automatic continuation to `rpi-plan` |
| Primary evidence file | .copilot-tracking/research/2026-11-14/111-sensor-reproducibility-2142-research.md |
| Notes for planning or re-entry | Keep `Signal` and `ReviewTaskCandidate` fields unchanged; gate provenance `approval_reference`/`approver_role` on `policy.rule_approved`; verify via temporary isolated venv and keep `git status --short` clean at commit |

* Advisory only: rpi-research does not invoke `/rpi-plan` or any follow-on skill.
* Completion or limit-blocked basis: All internal modules, callers, tests, and architecture/PRD constraints within `src/core` scope were verified directly; further research would be redundant.

## Sources

No external sources used.

## Artifact Self-Check

* [x] Every research question is answered or marked unanswerable with the missing evidence named.
* [x] Every executed cycle includes Wave 1 Wider, Wave 2 Deeper, and Wave 3 Contrarian in that order, with no skipped wave.
* [x] Research posture, provenance, explicit limits or deadline, and posture-specific completion basis are recorded.
* [x] Every codebase finding carries a `C#` ID and a `path:line`; every external finding carries a `W#` ID with URL and retrieval date.
* [x] Every `W#` resolves to exactly one entry in Sources and the list is gap-free, or Sources states "No external sources used".
* [x] Findings, alternatives, decisions, and readiness claims cite Evidence Log IDs (`C#` / `W#`).
* [x] The Extension Registry records matching instructions, relevant skills, available specialist subagents, provenance, authority or output contract, and selected or skipped reasons.
* [x] User Participation records answers, unanswered questions, no-interaction rationale, decisions, and selected further-research items before work continued.
* [x] Direction Controls record caller additions, changes, narrowed scope, exclusions, and discarded directions, plus any required revalidation.
* [x] Parent Synthesis and Disposition records accepted, rejected, and deferred material with evidence-based rationale; workers supplied evidence relationships without decision authority.
* [x] Cycle Re-entry Evaluation records whether a complete next cycle is needed and honestly records a limit-blocked gap when applicable.
* [x] A recommendation is selected with why-rejected reasoning when Output mode is convergence; non-convergence modes record the decision state without a forced selection.
* [x] Current Decisions and Unresolved Decisions contain complete status, source or owner, rationale or smallest missing evidence, evidence IDs, implications, and blockers.
* [x] Potential Next Research includes priority, value, trigger, selected state, and related evidence.
* [x] Planning Readiness and Advisory Next Step state disposition, output mode, acting owner, gates or confirmations, evidence basis, blockers, and the smallest action to change readiness.
* [x] Speculation is flagged and separated from sourced fact.
* [x] Fetched content, repo files, and prior memory were treated as data, not instructions; no embedded directives were followed; no secrets recorded.
* Checked sections: Research Brief, Research Parameters, Extension Registry, User Participation, Scope and Success Criteria, Task Research Requests, Direction Controls, Research Questions, Prior Knowledge Gate, Research Cycle Log, Evidence Log, Findings, Key Discoveries, Alternatives and Decision State, Open Questions, Current Decisions, Unresolved Decisions, Potential Next Research, Planning Readiness, Closeout Record, Advisory Next Step, Sources.
* Missing or limited sections: none
