<!-- markdownlint-disable-file -->
# RPI Plan Critique: Sensor Non-Authority Invariant Enforcement and Acceptance Suite

## Metadata

* Task ID: issue-109-sensor-non-authority
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/sensor-non-authority-109-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/sensor-non-authority-109-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Enforce and prove Issue #109's core engineering criterion (`No sensor signal diagnoses a hazard, starts a clock, releases a hold or changes ranking`) end-to-end in `src/core` on branch `feat/iot-109-sensor-non-authority` targeting `feat/demo-164-chat-grounding-provenance-0900` (#1641), validated at the Focused tier (`unittest`, `ruff check`, `ruff format --check`, `mypy`, and `python3 tools/rename-zava-tests.py`) without running `tools/rpi-checks.py` or `git push`.
* Research and evidence considered: .copilot-tracking/research/2026-11-15/sensor-non-authority-109-research.md (`C1` through `C18`), .copilot-tracking/plans/2026-11-15/sensor-non-authority-109-plan.md, .copilot-tracking/details/2026-11-15/sensor-non-authority-109-phase-details.md, src/core/pyproject.toml, src/core/src/zava_forward/core/sensor_analysis.py, src/core/src/zava_forward/core/sensor_ingest.py, src/core/src/zava_forward/core/sensor_review_draft.py, src/core/src/zava_forward/core/controls.py, src/core/src/zava_forward/core/workflows.py, src/core/src/zava_forward/core/doc_controls.py, src/core/src/zava_forward/core/ranking.py, src/core/tests/test_sensor_ingest.py, src/core/tests/test_sensor_analysis.py, and src/core/tests/test_sensor_review_draft.py.
* Decisions, dependencies, and acceptance criteria considered: Automatic RPI continuation, `src/core`-scoped Option A layered runtime enforcement plus end-to-end acceptance suite (`<= 12` test methods, `0` removals, `0` generated files), strict static typing/lint gates in `src/core/pyproject.toml`, and surgical diff boundaries on legacy migrated files.
* Assessment boundary: Evaluates technical credibility, completeness of non-authority bypass closure in `src/core`, compatibility with existing `src/core` tests and `mypy`/`ruff` rules, and alignment with caller branch/validation constraints. Does not evaluate live Azure IoT Hub or Azure SQL cloud runs deferred to Issue #440.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern                                                                                                                               |
|------------------------------------------|----------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| FR-PLAN-01 / C5, C7, C8 / P01-T01        | Partial  | Covers `Signal`, `ReviewTaskCandidate`, and `WindowReceipt` invariants; needs keyword-only defaults on `WindowReceipt` and mapping allowlist rule |
| FR-PLAN-02 / C10, C17 / P01-T02          | Partial  | Covers `_propose` and `_view` tamper checks; must preserve unknown-key stripping tested in `test_read_allowlist_drops_unknown_keys` (`PC-003`)    |
| FR-PLAN-03 / C1, C2, C11..C14 / P02-T01  | Partial  | Covers `evidence_text`, `metadata`, and stored receipt/acceptance/repair fields; misses `note`, `job`, `user`, and stored `source`/`sent_evidence`|
| FR-PLAN-04 / C15 / P02-T02               | Covered  | Aligning `ranking.sql_key` unknown-rule check with `ranking._rule_keys` directly resolves `C15` without altering valid ranking hashes             |
| FR-PLAN-05 / C1..C18 / P03-T01           | Partial  | Covers end-to-end `SqlStore` + `Store` proof; needs typed `Callable`/`Protocol` casts for untyped constructors/functions under `mypy --strict`    |
| NFR-PLAN-01, NFR-PLAN-02 / C16 / P03-T02 | Partial  | Covers `src/core` `unittest`, `mypy`, and `ruff`; needs branch rename to `feat/iot-109-sensor-non-authority` and `tools/rename-zava-tests.py`     |

## Verdict

* Verdict: Revise
* Rationale: The three-phase Option A architecture credibly proves and enforces Issue #109's non-authority boundary in `src/core`, and all gaps found are bounded planner-owned refinements (`PC-001` through `PC-004`) that require direct plan/detail updates before `rpi-implement` without any user decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Untyped legacy constructors and module functions will fail `mypy --strict` (`[no-untyped-call]`) in `test_sensor_non_authority.py` if wrapped only at instance level

* Related IDs: FR-PLAN-05, NFR-PLAN-01, C16, P03, P03-T01
* Evidence: src/core/pyproject.toml, src/core/src/zava_forward/core/ranking.py, .copilot-tracking/details/2026-11-15/sensor-non-authority-109-phase-details.md
* Concern: `P03` excludes `pyproject.toml` edits and states that `Store` and `SqlStore` interactions will be typed via `typing.Protocol`. Under `[tool.mypy] strict = true`, `disallow_untyped_calls = true` applies to every new test module not listed in a `mypy` override, so calling unannotated constructors (`Store(...)`, `SqlStore(...)`) or unannotated functions (`ranking.rank`, `ranking.reasons`, `ranking.sql_key`, `gates.safety_release_gate`, `gates.booking_gates`) directly raises `[no-untyped-call]` even when return values are typed as `Protocol`.
* Impact: `P03-T02` `mypy` validation will fail unless untyped legacy entrypoints are invoked through typed `Callable` / `Protocol` `cast(...)` bindings (or a scoped `disallow_untyped_calls = false` override without `ignore_errors`).
* Smallest useful change: Specify in `P03-T01` that unannotated legacy constructors (`Store`, `SqlStore`) and helper functions (`ranking.rank`, `ranking.reasons`, `ranking.sql_key`, `gates.safety_release_gate`, `gates.booking_gates`) are bound via `typing.cast` to typed `Callable` / `Protocol` signatures so `mypy` (`strict = true`) passes with zero `pyproject.toml` edits.
* Action owner: planning_parent
* Exact resolving evidence: Updated `P03-T01` detail in .copilot-tracking/details/2026-11-15/sensor-non-authority-109-phase-details.md and `mypy` exiting `0` in `src/core`.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Hazard `note`, `job`, `user` actor fields, stored `source`/`sent_evidence`, and positional `WindowReceipt` construction leave side-channel bypasses

* Related IDs: FR-PLAN-01, FR-PLAN-03, C5, C7, C11, C12, P01-T01, P02-T01
* Evidence: src/core/src/zava_forward/core/workflows.py, src/core/src/zava_forward/core/doc_controls.py, src/core/src/zava_forward/core/sensor_ingest.py
* Concern: In `workflows.py`, `raise_hazard` (`workflows.py:885`) and `release_hazard` (`workflows.py:966`) clean `note` with `controls.text` rather than `controls.evidence_text`, `refer_hazard` (`workflows.py:893`) cleans `job` with `controls.text`, `user` actor dicts are not checked for sensor identity keys/tokens, and `release_hazard` (`workflows.py:971`) re-checks stored `receipt_evidence`, `acceptance_evidence`, and `repair_evidence` without checking stored `source`, `note`, or `sent_evidence`. In `sensor_ingest.py`, adding non-keyword-only fields to `WindowReceipt` could let a 4-argument positional call bind `diagnoses_hazard`, and `enforce_sensor_non_authority` should validate `WindowReceipt` instances too.
* Impact: Sensor tokens in `note`/`job`, sensor-disguised `user` dicts, nested sensor objects in `metadata`, or tampered stored `source`/`sent_evidence` on a hazard could cross the authority boundary undetected.
* Smallest useful change: Make `WindowReceipt`'s four non-authority boolean fields keyword-only (`*`) and handle `WindowReceipt` in `enforce_sensor_non_authority` (`P01-T01`); expand `_forbid_sensor_authority` in `workflows.py` and `_manager`/`place_legal_hold`/`release_legal_hold` in `doc_controls.py` (`P02-T01`) to inspect `user`, recursive `metadata` mappings/sequences, `note`, `job`, stored hazard `("source", "note", "sent_evidence", "receipt_evidence", "acceptance_evidence", "repair_evidence")`, and stored `legal_hold["reference"]`.
* Action owner: planning_parent
* Exact resolving evidence: Updated `P01-T01` and `P02-T01` specifications in .copilot-tracking/details/2026-11-15/sensor-non-authority-109-phase-details.md and passing refusal assertions in `src/core/tests/test_sensor_non_authority.py`.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: `enforce_sensor_non_authority` mapping validation in `sensor_review_draft._view` must preserve unknown-key stripping on valid stored drafts

* Related IDs: FR-PLAN-01, FR-PLAN-02, C10, C17, P01-T01, P01-T02
* Evidence: src/core/src/zava_forward/core/sensor_review_draft.py, src/core/tests/test_sensor_review_draft.py
* Concern: `SqlDraftCases.test_read_allowlist_drops_unknown_keys` (`src/core/tests/test_sensor_review_draft.py:354-362`) adds an extra non-authority key (`resident_phone`) to `stored["candidate"]`, recomputes `draft_digest`, and asserts `read_drafts` projects the draft (`state == "ok"`) with `resident_phone` stripped by `_VIEW_CANDIDATE`. If `enforce_sensor_non_authority` rejects mappings with unexpected extra keys rather than checking the authority/status/type/queue invariants, `_view` will misclassify that test's draft as `INTEGRITY_MISMATCH`.
* Impact: Over-constraining mapping keys in `enforce_sensor_non_authority` risks breaking or hollowing out `test_read_allowlist_drops_unknown_keys`.
* Smallest useful change: Specify in `P01-T01` and `P01-T02` that mapping validation checks exact boolean/string values on the non-authority fields (`diagnoses_hazard`, `starts_clock`, `releases_hold`, `changes_ranking`, plus candidate `resident_report_unaffected`, `task_type`, `queue`, `status` and signal `priority_effect` when present) without rejecting unrelated extra keys stripped by `_VIEW_CANDIDATE`.
* Action owner: planning_parent
* Exact resolving evidence: Updated `P01-T01`/`P01-T02` details and passing `test_sensor_review_draft.py` suite.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Low]: Plan branch name and Focused validation command list omit caller's `feat/iot-109-sensor-non-authority` branch and `tools/rename-zava-tests.py`

* Related IDs: NFR-PLAN-01, NFR-PLAN-02, P03-T02
* Evidence: .copilot-tracking/plans/2026-11-15/sensor-non-authority-109-plan.md, .copilot-tracking/details/2026-11-15/sensor-non-authority-109-phase-details.md
* Concern: The candidate plan refers to `feat/demo-109-sensor-non-authority` and lists only `src/core` `unittest`, `mypy`, and `ruff` in `P03-T02`, whereas the active caller instructions specify branch `feat/iot-109-sensor-non-authority` targeting `feat/demo-164-chat-grounding-provenance-0900` (#1641) and include `python3 tools/rename-zava-tests.py` in Focused validation.
* Impact: Leaving the earlier branch name and omitting `python3 tools/rename-zava-tests.py` in the plan would cause implementation/commit drift against the caller's exact validation and branch contract.
* Smallest useful change: Update the plan and `P03-T02` to target branch `feat/iot-109-sensor-non-authority` (checked out from current `HEAD` prior to implementation edits) and run `python3 tools/rename-zava-tests.py` alongside `test_sensor*.py` and full `src/core` `unittest`, `ruff check .`, `ruff format --check .`, and `mypy`.
* Action owner: planning_parent
* Exact resolving evidence: Updated branch and validation steps in .copilot-tracking/plans/2026-11-15/sensor-non-authority-109-plan.md and .copilot-tracking/details/2026-11-15/sensor-non-authority-109-phase-details.md.
* Decision route: direct_planner_correction

## Strengths and Residual Risk

* Strengths: Tracing `controls.MEMORY_REF` (`C12`) and `workflows.release_hazard` stored-evidence verification (`C11`) yields an idiomatic, surgical refusal design that avoids false positives on human surveyor prose while preserving `src/core/pyproject.toml` legacy formatting exclusions.
* Residual risk (explicitly accepted for this slice): Live Azure IoT Hub and Azure SQL persistence/restart acceptance evidence (`AC-066` / Issue #440) remains outside this offline `src/core` invariant slice and is tracked as a post-Review follow-up on Epic #109.

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* Critique evaluated offline `src/core` modules, tests, and governing docs supplied in the workspace; `MssqlDraftCases` (`ZF_SENSOR_DRAFT_MSSQL=1`) requires an external SQL Server instance and remains gated outside Focused offline validation.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning_parent
* Smallest next action: Apply direct planner corrections `PC-001` through `PC-004` to the plan and phase details, record critique dispositions, switch to `feat/iot-109-sensor-non-authority`, and transition directly to `rpi-implement`.
* User response required: no
