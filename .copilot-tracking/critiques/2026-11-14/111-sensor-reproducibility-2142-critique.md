---
title: "RPI Plan Critique: Deterministic Versioned Sensor Analysis and Review Task"
description: "Single-pass plan critique for Task ID 111-sensor-reproducibility-2142 in src/core (Refs #111)"
ms.date: 2026-11-14
---

<!-- markdownlint-disable-file -->

## Metadata

* Task ID: 111-sensor-reproducibility-2142
* Critique date: 2026-11-14
* Plan: .copilot-tracking/plans/2026-11-14/111-sensor-reproducibility-2142-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/111-sensor-reproducibility-2142-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Deliver locally verifiable acceptance criteria for Issue #111 in `src/core` on branch `feat/iot-111-sensor-reproducibility-2142` so outputs are reproducible from retained readings with deterministic versioned sensor analysis, `SENSOR_REVIEW_DUE` review task candidate generation, and explicit version provenance; write all four `.copilot-tracking/` artifacts; verify in `src/core` with bare `python3 -m mypy`, `python3 -m ruff check .`, `python3 -m ruff format --check .`, and `python3 -m unittest discover -s tests -p 'test_*sensor*.py' -v`; commit cleanly with `Refs #111` and the Copilot trailer; do not push.
* Research and evidence considered: .copilot-tracking/research/2026-11-14/111-sensor-reproducibility-2142-research.md, .copilot-tracking/plans/2026-11-14/111-sensor-reproducibility-2142-plan.md, .copilot-tracking/details/2026-11-14/111-sensor-reproducibility-2142-phase-details.md, src/core/src/zava_forward/core/sensor_analysis.py, src/core/src/zava_forward/core/sensor_analysis_store.py, src/core/src/zava_forward/core/sensor_review_draft.py, src/core/src/zava_forward/core/sensor_consumer.py, src/core/src/zava_forward/core/synthetic/sensor_scenarios.py, src/core/src/zava_forward/core/synthetic/sensor_faults.py, src/core/pyproject.toml, src/core/README.md, src/core/tests/test_sensor_analysis.py, src/core/tests/test_sensor_analysis_store.py, src/core/tests/test_sensor_analysis_reproducibility.py, src/api/tests/test_sensor_analysis_reproducibility.py.
* Decisions, dependencies, and acceptance criteria considered: FR-1 through FR-5, NFR-1, NFR-2, AC-1 through AC-6, ADR 0003 decision 6 non-authority and approved-rule gating, PRD FR-050 / AC-067 / AC-068 privacy and sufficiency bounds, `sensor_review_draft.py` `_VIEW_CANDIDATE` and `_VIEW_LINEAGE` compatibility, and open R1-R3 plus full-SQL publication gate boundaries.
* Assessment boundary: Evaluates plan and phase-details credibility, mathematical determinism, digest collision resistance, type-check compatibility, and local verification feasibility against primary repository code. Live SQL Server (`ZF_SENSOR_MSSQL=1`), full external gate execution (`tools/rpi-checks.py --all`), hosted CI, and R1-R3 primary-standards sign-off are explicitly outside this no-push slice.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| FR-1 / AC-1 (Pure deterministic reproduction) | Partial | Covered in P01-T01, except FR-1 promises identical `provenance`, `signal`, and `review_task` across `reproduce_review_task` and `reproduce_sensor_analysis` while P01-T01 omits `review_task` and `candidate` resolution in `reproduce_sensor_analysis` and `version_provenance` (`PC-002`). |
| FR-2 / AC-3 (Collision-free input, policy, and output digests) | Partial | P01-T01 adds `reading_id` and schema markers to `_quality_tuples`, yet `_digest` still sorts `reading_tuples` and `_quality_tuples` separately without per-row metric-to-quality binding, leaving cross-row swap collisions open (`PC-001`), and `policy_digest` lacks numeric `-0.0` / `int`-to-`float` normalization (`PC-002`). |
| FR-3 / AC-2 (Strict version and approval gating + `VersionProvenance`) | Partial | Approval masking on `policy.rule_approved` and `analysis_version` checks are sound; `version_provenance` and `review_task_candidate` still omit `signal.threshold_label == policy.threshold_label` and `candidate` consistency validation (`PC-002`), and P01-T01 misstates `sensor_faults.SCHEMA_VERSION` as `"reading-v1"` instead of `"sensor-fault-input-v1"` (`PC-004`). |
| FR-4 (Empty-window and malformed-home handling) | Covered | `_home_and_window` string validation, explicit `(home_id, window)` empty-slice support (`NO_READINGS_IN_WINDOW`), and `SINGLE_HOME_REQUIRED` / `NO_VALID_OBSERVATIONS` refusals are well specified in P01-T01 (ensure surrounding-whitespace `home_id` strings do not bypass exact equality in `derive_signal`). |
| FR-5 / AC-4 (`sensor_analysis_store.reproduce_retained`) | Partial | Read-only fail-closed design in P01-T02 is sound, except parity descriptions in P01-T02 and P02-T01 equate `reproduce_retained` to unwindowed `consumer.observed_series([home_id])` rather than window-bounded indoor rows (`PC-004`). |
| NFR-1 (Privacy and non-authority preservation) | Covered | `VersionProvenance` contains zero raw reading values, `sensor_id`, or `reading_id` values, masks unapproved `RuleApproval` metadata, and preserves `Signal` and `ReviewTaskCandidate` non-authority flags and `sensor_review_draft.py` schemas. |
| NFR-2 / AC-5 / AC-6 / C9 / C10 (Typing, test lock, docs, verification) | Partial | P02 / P02-T02 rely on creating a `/tmp` virtual environment (prohibited by runtime workspace rules) and assume `venv --system-site-packages` includes `~/.local` dev tools (`PC-003`); P02-T01 renames an existing committed test method despite P02 locking zero test removals (`PC-004`). |
| P01 / P01-T01 / P01-T02 | Partial | Actionable direct planner corrections needed for `PC-001`, `PC-002`, and `PC-004`. |
| P02 / P02-T01 / P02-T02 | Partial | Actionable direct planner corrections needed for `PC-001`, `PC-003`, and `PC-004`. |

## Verdict

* Verdict: Revise
* Rationale: The architectural approach (`VersionProvenance` envelope without mutating `Signal` or `ReviewTaskCandidate`, approval-gated provenance, and read-only `reproduce_retained`) is well grounded in codebase contracts, but four substantive issues require direct planner revision before implementation: (1) an algebraic cross-row swap collision remaining in `_digest`, (2) an `output_digest` / `review_task` divergence between `FR-1` and `P01-T01` across `version_provenance` and `reproduce_sensor_analysis`, (3) a `/tmp` virtual environment plan that conflicts with workspace rules and Python `venv` user-site isolation (`~/.local`), and (4) an inaccurate `sensor_faults.SCHEMA_VERSION` literal (`"reading-v1"` instead of `"sensor-fault-input-v1"`), unwindowed `observed_series` parity wording, and a test-method rename that conflicts with the zero-removal test lock.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Independent sorting of `reading_tuples` and `_quality_tuples` leaves `_digest` vulnerable to cross-row swap collisions

* Related IDs: FR-2, AC-3, C2, C8, P01-T01, P02-T01
* Evidence: src/core/src/zava_forward/core/sensor_analysis.py:131-158, src/core/src/zava_forward/core/synthetic/sensor_scenarios.py:123-156, .copilot-tracking/details/2026-11-14/111-sensor-reproducibility-2142-phase-details.md
* Concern: P01-T01 appends `reading_id` and a schema-validity marker to `_quality_tuples`, while `_digest` continues to hash `[home_id, reading_tuples(rows), _quality_tuples(rows)]` as two separately sorted lists. Because `reading_tuples` omits `reading_id` and quality attributes while `_quality_tuples` omits `temperature_c`, `temperature_unit`, `humidity_pct`, and `humidity_unit`, within-row binding is lost whenever two rows share `(sensor_id, observed_at)`. For example, swapping `temperature_c="20.00"` and out-of-domain `temperature_c="999.00"` across two duplicate-timestamp rows `{reading_id="R1", calibrated="true"}` and `{reading_id="R2", calibrated="false"}` leaves both `reading_tuples` and `_quality_tuples` identical (same `input_digest`), yet `comparator.analyse` accepts 1 valid sample in the first set and 0 in the second (divergent `Signal.valid`, `Signal.coverage`, and `output_digest`). In addition, P01-T01 tests row string values with `type(v) is str` whereas `comparator.analyse` (`sensor_scenarios.py:124`) uses `isinstance(value, str)`.
* Impact: Breaks FR-2 and AC-3 collision resistance by allowing distinct retained reading sets with different `Signal` outcomes to share an `input_digest` and `ReviewTaskCandidate.task_key`.
* Smallest useful change: Keep `reading_tuples` unchanged for existing public callers (`src/api/tests/test_sensor_analysis_reproducibility.py:30`), update `_quality_tuples` (or a bound per-row canonical tuple list hashed by `_digest`) so each per-row tuple binds `(sensor_id, observed_at, reading_id, temperature_c, temperature_unit, humidity_pct, humidity_unit, calibrated, source_type, schema_version, schema_marker)` using `isinstance(v, str)` to match `comparator.analyse`, and include a duplicate-timestamp cross-row swap case in P02-T01.
* Action owner: planning parent (`rpi-plan`)
* Exact resolving evidence: Revised P01-T01 and P02-T01 in .copilot-tracking/details/2026-11-14/111-sensor-reproducibility-2142-phase-details.md specifying per-row metric-and-quality binding with `isinstance(v, str)` in `_digest` and a cross-row swap assertion.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: `version_provenance` and `reproduce_sensor_analysis` omit deterministic `candidate` resolution, causing `output_digest` divergence under approved policies

* Related IDs: FR-1, FR-2, FR-3, AC-1, AC-2, C9, P01-T01
* Evidence: .copilot-tracking/plans/2026-11-14/111-sensor-reproducibility-2142-plan.md, .copilot-tracking/details/2026-11-14/111-sensor-reproducibility-2142-phase-details.md, src/api/tests/test_sensor_analysis_reproducibility.py:22-70, src/core/tests/test_sensor_analysis.py:175-190
* Concern: FR-1 states that `reproduce_review_task` and `reproduce_sensor_analysis` produce identical `provenance`, `signal`, and `review_task`, and FR-2 defines `output_digest` over `(signal, review_task)`. However, P01-T01 defines `version_provenance(signal, policy=None, candidate=None)` with `candidate` defaulting to `None` instead of resolving `review_task_candidate(signal, effective_policy)`, and updates `reproduce_sensor_analysis` to return `provenance` and `output_digest` without computing `candidate` or returning `review_task`. For a `SUFFICIENT` + `REVIEW_CANDIDATE` reading set under an approved policy, `reproduce_sensor_analysis(rows, APPROVED)` or `version_provenance(signal, APPROVED)` would compute `output_digest(signal, None)` while `reproduce_review_task(rows, APPROVED)` computes `output_digest(signal, candidate)`, producing two conflicting `VersionProvenance.output_digest` hashes for the same inputs. In addition, `review_task_candidate` and `version_provenance` do not verify `signal.threshold_label == policy.threshold_label` or reject a caller-passed `candidate` that disagrees with `review_task_candidate(signal, policy)`, `policy_digest` does not normalize float `humidity_threshold_pct` (`75` vs `75.0`, `-0.0` vs `0.0`), and returning untyped `dict[str, object]` forces caller `isinstance` narrowing (or `TypedDict` definitions) to satisfy `mypy --strict` without `# type: ignore[index]`.
* Impact: Causes inconsistent `VersionProvenance.output_digest` values across entry points, violates FR-1 parity between `reproduce_sensor_analysis` and `reproduce_review_task`, allows mismatched `threshold_label` or `candidate` pairing in `version_provenance`, and risks `mypy --strict` indexing errors in tests.
* Smallest useful change: Update P01-T01 so `review_task_candidate` also checks `signal.threshold_label == policy.threshold_label`; `version_provenance` resolves `expected = review_task_candidate(signal, effective_policy)` when `candidate` is omitted (using a sentinel or verifying `candidate == expected` when supplied, and checking `signal.threshold_label == effective_policy.threshold_label`); `reproduce_sensor_analysis` derives `candidate = review_task_candidate(signal, effective_policy)` and includes `"review_task"` alongside `"provenance"` and `"output_digest"`; `policy_digest` and `VersionProvenance` normalize `humidity_threshold_pct` as `0.0 if val == 0 else float(val)`; and reproduction return types use `TypedDict` (or explicit narrowing in tests) so `mypy --strict` passes with zero `# type: ignore`.
* Action owner: planning parent (`rpi-plan`)
* Exact resolving evidence: Revised P01-T01 in .copilot-tracking/details/2026-11-14/111-sensor-reproducibility-2142-phase-details.md specifying canonical `candidate` resolution/validation, `threshold_label` matching, `"review_task"` inclusion in `reproduce_sensor_analysis`, float normalization in `policy_digest`, and strict `TypedDict` / narrowing typing.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Planned `/tmp` virtual environment violates workspace no-`/tmp` constraints and `venv --system-site-packages` omits `~/.local` user site-packages

* Related IDs: NFR-2, AC-6, C9, C10, P02, P02-T02
* Evidence: .copilot-tracking/plans/2026-11-14/111-sensor-reproducibility-2142-plan.md, .copilot-tracking/details/2026-11-14/111-sensor-reproducibility-2142-phase-details.md, .copilot-tracking/research/2026-11-14/111-sensor-reproducibility-2142-research.md, src/core/pyproject.toml:18-40
* Concern: The plan (`What You May Not Know`, `NFR-2`, `Dependencies`) and phase details (`P02`, `P02-T02`) place the isolated verification virtual environment under `/tmp` (`python3 -m venv --system-site-packages /tmp/...`). Execution rules strictly prohibit writing files or directories to `/tmp` or `/var/tmp`. Furthermore, Python's `venv` disables `site.ENABLE_USER_SITE` even when `--system-site-packages` is set, excluding `~/.local/lib/python3.12/site-packages` (where user packages are installed per `C10`). If `mypy` or `ruff` live in `~/.local` rather than system `/usr/lib`, bare `python3 -m mypy` and `python3 -m ruff` inside that venv will fail with `No module named mypy` unless selectively linked/exposed without activating `~/.local`'s stale `__editable__.zava_forward_core-0.1.0.pth`.
* Impact: Blocks execution of the required bare verification suite in P02-T02 or violates the workspace `/tmp` prohibition.
* Smallest useful change: Update the plan (`What You May Not Know`, `NFR-2`, `Dependencies`) and phase details (`P02`, `P02-T02`) to create the temporary verification venv inside a worktree-local path (for example `.venv-verify-111` under the repository root, deleted before `git status --short` and `git commit`) and ensure `mypy` and `ruff` modules/binaries are linked or available inside that venv while `zava_forward.core` resolves exclusively to this worktree's `src/core/src` without touching shared `~/.local`.
* Action owner: planning parent (`rpi-plan`)
* Exact resolving evidence: Updated .copilot-tracking/plans/2026-11-14/111-sensor-reproducibility-2142-plan.md and .copilot-tracking/details/2026-11-14/111-sensor-reproducibility-2142-phase-details.md replacing `/tmp` venv paths with a cleaned worktree-local venv path and handling `~/.local` dev-tool visibility.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Phase details misstate `sensor_faults.SCHEMA_VERSION` as `"reading-v1"`, overstate unwindowed `observed_series` parity, and rename a committed test method under a zero-removal lock

* Related IDs: FR-5, AC-2, AC-4, AC-5, NFR-2, C4, C8, P01-T01, P01-T02, P02, P02-T01, P02-T02
* Evidence: src/core/src/zava_forward/core/synthetic/sensor_faults.py:10, src/core/src/zava_forward/core/synthetic/sensor_scenarios.py:141, src/core/src/zava_forward/core/sensor_analysis_store.py:28-31, src/core/src/zava_forward/core/sensor_consumer.py:1051-1076, src/core/tests/test_sensor_analysis.py:193-198, .copilot-tracking/details/2026-11-14/111-sensor-reproducibility-2142-phase-details.md
* Concern: Three concrete specification drifts exist in the phase details:
  1. P01-T01 states that `sensor_faults.SCHEMA_VERSION` is `"reading-v1"` (propagated from C8), whereas `sensor_faults.py:10` defines `SCHEMA_VERSION = "sensor-fault-input-v1"` (the exact constant enforced by `comparator.analyse` at `sensor_scenarios.py:141`).
  2. P01-T02 and P02-T01 state that `reproduce_retained(consumer, home_id, window, ...)` matches `reproduce_review_task` over `consumer.observed_series([home_id])`, overlooking that `analyse_retained` passes `{home_id: (first, last)}` (`[window.start, window.end - 1s]`) to `retained_envelopes`, whereas unwindowed `observed_series([home_id])` returns out-of-window retained rows too (which `derive_signal` hashes into `input_digest` and `comparator.analyse` marks `OUTSIDE_WINDOW_OR_OFF_GRID`).
  3. P02 locks `Exact test removals: none`, while P02-T01 item 3 renames existing method `test_digest_changes_with_calibration_flag` (`test_sensor_analysis.py:193`) to `test_digest_changes_with_calibration_reading_id_and_schema_shape`.
* Impact: Can cause failing `VersionProvenance.schema_version` assertions or inaccurate `src/core/README.md` documentation, false multi-window parity assumptions, and a test-removal lock discrepancy during review.
* Smallest useful change: Correct P01-T01 to record `sensor_faults.SCHEMA_VERSION` as `"sensor-fault-input-v1"`, clarify in P01-T02, P02-T01, and P02-T02 (`src/core/README.md`) that `reproduce_retained` matches pure `reproduce_review_task` over window-bounded retained indoor rows (`observed_series([home_id], {home_id: (first, last)})`), and retain the existing method name `test_digest_changes_with_calibration_flag` in P02-T01 (extending its assertions in place or adding a separate method within the budget).
* Action owner: planning parent (`rpi-plan`)
* Exact resolving evidence: Revised P01-T01, P01-T02, P02-T01, and P02-T02 in .copilot-tracking/details/2026-11-14/111-sensor-reproducibility-2142-phase-details.md reflecting `"sensor-fault-input-v1"`, window-bounded `observed_series` parity, and zero renamed/removed test methods.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Separating provenance metadata into `VersionProvenance` while keeping `Signal` and `ReviewTaskCandidate` fields and `ReviewTaskCandidate.task_key` unchanged cleanly protects `sensor_review_draft.py` (`_VIEW_CANDIDATE`, `_VIEW_LINEAGE`, and stored `draft_digest` integrity checks) and `src/api` callers.
* Gating `approver_role` and `approval_reference` in `VersionProvenance` on `policy.rule_approved` closes the uncommitted working-tree defect where mismatched `RuleApproval` objects leaked unapproved references into provenance.
* Fail-closed `INSUFFICIENT` handling with `priority_effect="NONE"` and `review_task=None` across missing, stale, declined, unknown, weather-only (`LIVE_VERSIONS`), and `ConsumerError` store paths aligns with ADR 0003 decision 6 and PRD FR-050 / AC-067 / AC-068.
* Accepted residual risk outside this no-push slice: R1-R3 primary-standards confirmation (`docs/reference/research/iot-sensor-analytics-research-plan.md`) and the full publication gate (`tools/rpi-checks.py --all` with `ZF_SENSOR_MSSQL=1` plus hosted CI per `src/README.md`) remain explicitly deferred follow-ups and must not be claimed as completed in `src/core/README.md` or the `Refs #111` commit message.

## Questions or Blocking Evidence Gaps

* None. All four findings are resolved from primary repository code and require no user input or additional research.

## Limitations

* Critique inspected supplied artifacts and `src/core` / `src/api` Python modules statically without mutating any repository or environment state; live SQL Server (`ZF_SENSOR_MSSQL=1`) and hosted CI workflows remain outside the local no-push boundary.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning parent (`rpi-plan`)
* Smallest next action: Apply direct planner revisions for PC-001, PC-002, PC-003, and PC-004 to .copilot-tracking/plans/2026-11-14/111-sensor-reproducibility-2142-plan.md and .copilot-tracking/details/2026-11-14/111-sensor-reproducibility-2142-phase-details.md, record their dispositions in the plan's Critique Disposition table, and finalize for `rpi-implement` without running a second critique pass.
* User response required: no
