<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #220 Criterion 5 — No Retaliation, Inferred Refusal or Delayed Hazard Response

## Metadata

* Task ID: issue-220-no-retaliation-2026-11-15
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/220-no-retaliation-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/220-no-retaliation-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Issue #220 Criterion 5 (`No retaliation, inferred refusal or delayed hazard response`) across `src/core` and `src/api` without modifying `src/api/src/zava_forward/api/web/role-screens.js`; runtime non-retaliation, non-refusal, non-closure, and zero-hazard-delay invariants across resident digital, staff non-digital, representative/nominee, and AI/assistant proposal routes; immediate independent hazard intake routing on `hazard_concern`; explicit machine-checkable `non_retaliation_assurance` and `hazard_clock_preserved` contract; `test_challenge_no_retaliation_220.py` and `test_challenge_no_retaliation_api_220.py`; `test_content_standard.py` clean; Focused Tier validation via `pip` without pushing.
* Research and evidence considered: `.copilot-tracking/research/2026-11-15/220-no-retaliation-research.md`, `src/core/src/zava_forward/core/challenges.py`, `src/core/src/zava_forward/core/resident_decisions.py`, `src/core/src/zava_forward/core/sqlstore.py`, `src/core/src/zava_forward/core/mssqlstore.py`, `src/core/src/zava_forward/core/ai_tasks.py`, `src/core/src/zava_forward/core/assistants.py`, `src/api/src/zava_forward/api/server.py`, `src/api/src/zava_forward/api/web/panels.js`, `src/core/tests/test_resident_decisions.py`, `src/core/tests/test_issue_220_challenge_route.py`, `src/api/tests/test_resident_api.py`, `src/api/tests/test_content_standard.py`, `src/api/checks/challenge_browser_check.py`.
* Decisions, dependencies, and acceptance criteria considered: `FR-1`..`FR-4`, `NFR-1`..`NFR-2`, `P01`..`P04` (`P01-T01`..`P04-T03`), locked test scope (`removals = none`, `max additions = 2`), ADR 0006 formatting boundaries, and strict `mypy` requirements.
* Assessment boundary: Evaluates completeness and architectural soundness of the candidate plan against supplied codebase evidence and Issue #220 Criterion 5 invariants; runtime execution results belong to `rpi-implement` and `rpi-review`.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| FR-1 / P01-T02, P02-T01, P02-T03, P03-T01 | Partial | Reopen and `ai_task` target coverage need SQLite/MSSQL `_priority_correction_rows` and `ai_tasks.review` staleness fence alignment (`PC-002`, `PC-003`). |
| FR-2 / P01-T01, P02-T02, P03-T01 | Covered | Runtime `assert_no_adverse_challenge_effects` and `_ranking()` invariance cover priority, refusal/no-access/sanction/withdrawn/negative-engagement, and work-item closures. |
| FR-3 / P01-T01, P02-T02, P03-T01 | Partial | Atomic `hazard_intake` routing inside `_res_challenge_*` must guard against duplicate audit emission during `SqlStore` replay validation (`validate_resident_sql`, `PC-001`). |
| FR-4 / P01-T01, P02-T02, P03-T01, P03-T02 | Partial | `Assistants._view` projection fields (`non_retaliation_assurance`, `hazard_clock_preserved`) must be stripped before SQLite row persistence and scrubbed under `_withhold_sensors` (`PC-004`). |
| NFR-1 & NFR-2 / P03-T02, P04-T01..T03 | Covered | Backward-compatibility locks (`C11`-`C18`), `web/role-screens.js` exclusion, `test_content_standard.py`, `ruff`, and `mypy --strict` are explicitly specified. |

## Verdict

* Verdict: Revise
* Rationale: The four-phase architecture covers every Issue #220 Criterion 5 entrypoint and backward-compatibility lock cleanly, and four localized codebase-specific refinements (`PC-001`..`PC-004`, all planner-owned direct corrections requiring zero user questions) will prevent SQLite replay side effects, reopened-correction SQL index drift, unblocked stale `ai_task` acceptance, and assistant sensor-withholding leakage.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Prevent duplicate `hazard.persist_event` side effects during `SqlStore` replay validation

* Related IDs: FR-3, P02-T02, C9
* Evidence: `src/core/src/zava_forward/core/resident_decisions.py:555-565` (`validate_resident_sql` replays `getattr(store, "_res_" + action)(actor, json.loads(row[1]), body)` on a detached case dict while `context["validating"] = True`).
* Concern: If `_route_challenge_hazard` inside `_res_challenge_open`, `_res_challenge_update`, or `_res_challenge_reopen` invokes `hazard.persist_event` unconditionally, `SqlStore.save()`'s validation replay will execute `hazard.persist_event` a second time inside `store.dblock` on a detached object, either deadlocking or writing duplicate `safety_raised` / `safety_emergency` audit entries.
* Impact: Breaks `SqlStore` challenge + immediate `hazard_intake` writes or corrupts audit parity with JSON `Store`.
* Smallest useful change: Specify in `P02-T02` that `_route_challenge_hazard` checks `getattr(getattr(self, "local", None), "resident_validation", None)` (`validating == True`): during detached SQL validation replay it validates inputs and appends `h` to the detached `c["hazards"]` list without calling `hazard.persist_event`, and emits `hazard.persist_event` exactly once on the primary live mutation.
* Action owner: planning_parent
* Exact resolving evidence: Updated `P02-T02` detail and passing `SqlStore` immediate-hazard-intake audit parity test in `src/core/tests/test_challenge_no_retaliation_220.py`.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Align `sqlstore.py` and `mssqlstore.py` `priority_correction` indexing when reopening a corrected challenge

* Related IDs: FR-1, FR-2, P02-T01, P02-T02
* Evidence: `src/core/src/zava_forward/core/resident_decisions.py:617-625`, `src/core/src/zava_forward/core/sqlstore.py:1124-1131`, and `src/core/src/zava_forward/core/mssqlstore.py:224-235`.
* Concern: `P02-T01` specifies setting `prior_correction_preserved: True` when reopening a `"Correction recorded"` challenge so dependent proposals remain stale until fresh human review, but `sqlstore.py` (`_priority_correction_rows` and `priority_correction` column computation) and `mssqlstore.py` (`_priority_correction_rows`) currently check only `$.resolution.outcome = 'Correction recorded'`. Without updating `sqlstore.py` and `mssqlstore.py` alongside `resident_decisions.py`, SQLite writer-fence checks (`sql_current=True`) will miss reopened corrections.
* Impact: Reopening a previously corrected challenge in `SqlStore` would silently allow concurrent `accept`/`edit` of a stale priority suggestion (`validate_priority_sql`).
* Smallest useful change: Include `src/core/src/zava_forward/core/sqlstore.py` and `src/core/src/zava_forward/core/mssqlstore.py` in `P02-T01` / `P02-T02` targets so `priority_correction` column projection and `_priority_correction_rows()` treat `prior_correction_preserved = true` identically to `resolution.outcome = 'Correction recorded'`.
* Action owner: planning_parent
* Exact resolving evidence: Updated `P02` scope/targets in plan and phase details, plus `SqlStore` reopen-staleness test in `src/core/tests/test_challenge_no_retaliation_220.py`.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Enforce `"Correction recorded"` staleness fence in `ai_tasks.review`

* Related IDs: FR-1, FR-2, P02-T03, C6
* Evidence: `src/core/src/zava_forward/core/ai_tasks.py:350-405` and `src/core/src/zava_forward/core/resident_decisions.py:675-695`.
* Concern: `P02-T03` adds `ai_task` and `form_review` suggestions to `challenge_catalog` and `priority_challenge_state`, but `ai_tasks.review` (`ai_tasks.py:350`) does not yet consult `priority_challenge_state(store, rec)["stale"]` before accepting or editing an `ai_task` recommendation.
* Impact: An `ai_task` recommendation marked stale by `"Correction recorded"` could still be accepted via `/api/ai/review` instead of requiring fresh work or manual handling.
* Smallest useful change: Include `src/core/src/zava_forward/core/ai_tasks.py` in `P02-T03` so `ai_tasks.review` refuses `accept`/`edit` (still permitting `reject`) with `PermissionError` when `priority_challenge_state(store, rec)["stale"]` is `True`.
* Action owner: planning_parent
* Exact resolving evidence: Updated `P02-T03` targets/details and `ai_tasks.review` stale-correction rejection test in `src/core/tests/test_challenge_no_retaliation_220.py`.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Strip transient `_view` assurance keys on `assistant_tasks` writes and scrub challenge notes when sensor consent is withheld

* Related IDs: FR-4, P03-T01, C7
* Evidence: `src/core/src/zava_forward/core/assistants.py:1166-1183,2084-2085`.
* Concern: `Assistants.review` pops computed `_view` keys before writing `stored` back to `assistant_tasks.body`, and `_withhold_sensors` / `_scrub_events` redacts notes on `quality-evidence` proposals when monitoring consent is not currently granted. Adding `non_retaliation_assurance` and `hazard_clock_preserved` in `_view` and challenge notes in `stored["challenges"]` / `assistant_events` requires popping transient `_view` keys in both `review` and `challenge` and scrubbing free-text challenge notes (while keeping structural challenge status, owner, next update, and `non_retaliation_assurance` / `hazard_clock_preserved` visible!) when `_withhold_sensors` applies.
* Impact: Prevents stale view-key persistence and preserves indoor sensor consent-withholding privacy rules on challenged `quality-evidence` proposals.
* Smallest useful change: Specify transient key stripping and `_withhold_sensors` challenge-note redaction (`WITHHELD_NOTE`) in `P03-T01`.
* Action owner: planning_parent
* Exact resolving evidence: Updated `P03-T01` detail and sensor-withheld assistant challenge test in `src/core/tests/test_challenge_no_retaliation_220.py`.
* Decision route: direct_planner_correction

## Strengths and Residual Risk

* Strong backward-compatibility verification (`C11`-`C18`), explicitly protecting `after.pop("affected_challenges"); after == before`, `nomination_record(hazard_concern=True)` fail-closed semantics, `challenge_browser_check.py`'s 9-field submission contract, ADR 0006 `ruff format` exclusions, `test_content_standard.py`, and the strict prohibition on modifying `web/role-screens.js`.
* Residual risk: None after applying `PC-001`..`PC-004`.

## Questions or Blocking Evidence Gaps

* None.

## Limitations

* Static plan and codebase verification only; runtime validation executes in `P04`.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning_parent
* Smallest next action: Apply `PC-001`..`PC-004` directly in one coherent batch to `.copilot-tracking/plans/2026-11-15/220-no-retaliation-plan.md` and `.copilot-tracking/details/2026-11-15/220-no-retaliation-phase-details.md`, record dispositions in `## Critique Disposition`, mark the plan `Ready`, and advance to `rpi-implement`.
* User response required: no
