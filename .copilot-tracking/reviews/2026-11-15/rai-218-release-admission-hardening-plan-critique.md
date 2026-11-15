<!-- markdownlint-disable-file -->
# RPI Plan Critique: Live Release Admission and Readiness Hardening (#218 Child)

## Metadata

* Task ID: issue-218-rai-release-admission-hardening
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/rai-218-release-admission-hardening-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/rai-218-release-admission-hardening-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Execute the single final-candidate critique for child task `issue-218-rai-release-admission-hardening` (`rai-218-release-admission-hardening`) resolving routed defects `RV-001` and `RV-002` from parent review of Issue #218 under the confirmed focused validation tier (`unittest`, `mypy`, `ruff check`, `ruff format --isolated --line-length 100 --check`) without recommending `tools/rpi-checks.py`, pushing, or opening a pull request.
* Research and evidence considered: .copilot-tracking/reviews/logs/2026-11-15/rai-218-release-discipline-review.md, .copilot-tracking/research/2026-11-15/rai-218-release-admission-hardening-research.md, .copilot-tracking/plans/2026-11-15/rai-218-release-admission-hardening-plan.md, .copilot-tracking/details/2026-11-15/rai-218-release-admission-hardening-phase-details.md, src/core/src/zava_forward/core/rai_release.py, src/core/src/zava_forward/core/assistant_release.py, src/core/src/zava_forward/core/rai_control_plane.py, src/core/src/zava_forward/core/sqlstore.py, src/core/src/zava_forward/core/assistants.py, src/core/src/zava_forward/core/ai_registry.py, src/core/tests/release_support.py, src/core/tests/test_rai_release.py, src/core/tests/test_rai_threshold_live_approval_guard.py, src/core/tests/test_rai_control_plane_218.py, src/api/tests/test_assistant_release.py, src/api/tests/test_rai_release_readiness_api_218.py.
* Decisions, dependencies, and acceptance criteria considered: Parent defects `RV-001` and `RV-002`; research citations `C1` through `C9`; functional requirements `FR-H01` through `FR-H03`; non-functional requirements `NFR-H01` through `NFR-H03` (including the `<= 6` added test-method governance lock); acceptance criteria `AC-H01` through `AC-H04`; task dependency chain `P01-T01 -> P01-T02 -> P02-T01 -> P02-T02`; and confirmed focused-tier validation boundary.
* Assessment boundary: Evaluates plan and phase-detail credibility against the supplied repository code and test suites for `src/core` and `src/api`. Does not execute live Azure OpenAI or live Azure SQL deployments, full-gate `tools/rpi-checks.py`, or out-of-scope Epic #218 governance items (`OQ-017` office-holder appointment, `OQ-018`, `OQ-019`).

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| `RV-001`, `FR-H01`, `FR-H02`, `P01-T01`, `C1`, `C2`, `C4`..`C7` | Covered | Removing inner key-presence guards in `rai_release.missing_binding` while injecting `setdefault("approved_by", None)` and `setdefault("named_approval_id", None)` on SQL-loaded rows in `assistant_release.assessment(..., live=True)` closes partial-key and stored-row `OQ-017` bypasses without breaking isolated 4-key unit dicts or `rai_release.reference` digests. |
| `RV-002`, `FR-H03`, `NFR-H01`, `NFR-H02`, `P01-T02`, `C3`, `C8`, `C9` | Partial | Delegating to `_assistant_release.assessment(cursor_db, cap, binding, now_ts, live=True)` inside `with _assistant_release.read_only():` solves drifted/unattested SQL row inspection and portable `db.driver.Error` handling, but `P01-T02` omits `_assistants: Any` import/aliasing, calls untyped `ai_registry` helpers directly instead of `_ai_registry: Any`, uses an unguarded `legacy_deployment` attribute lookup that raises `AttributeError` on scripted providers during `Assistants.registry`, and lacks an `elif task_name in _ai_registry.LEGACY:` guard (`PC-001`). |
| `AC-H01`, `AC-H02`, `AC-H03`, `NFR-H03` | Covered | Acceptance criteria and the `<= 6` test-method budget across existing `#218` test files cover partial-key `missing_binding`, stored-SQL-row live dispatch denial, and read-only drifted-binding exclusion. |
| `AC-H04`, `P02-T01`, `P02-T02` | Partial | Focused validation commands match caller constraints, but `AC-H04` and `P02-T01` reference non-existent `verify_traceability_targets()["all_verified"]` (actual key `"all_resolved"`), `rai_release.py` already rejects `expires=True`, and `P02-T01` needs an explicit positive-to-negative setup in `test_rai_release_readiness_api_218.py` so the HTTP assertion genuinely fails before `P01` (`PC-002`). |

## Verdict

* Verdict: Revise
* Rationale: The core design for closing `RV-001` and `RV-002` is sound, minimal, and preserves both isolated bare-dict unit contracts and dual-deployment `legacy:*` release semantics, but two concrete implementation defects in the candidate details (`PC-001` runtime `AttributeError`/`NameError` and strict-`mypy` untyped-call failures in `P01-T02`, and `PC-002` `KeyError: 'all_verified'` plus non-discriminating API test setup in `AC-H04`/`P02-T01`) require direct planner corrections before implementation.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: `P01-T02` `_inspect_sql_live_releases` helper calls break scripted-provider `Assistants.registry`, strict `mypy`, and non-legacy task safety

* Related IDs: `RV-002`, `FR-H03`, `NFR-H02`, `P01`, `P01-T02`, `C3`, `C8`, `C9`
* Evidence: .copilot-tracking/plans/2026-11-15/rai-218-release-admission-hardening-plan.md (`FR-H03`), .copilot-tracking/details/2026-11-15/rai-218-release-admission-hardening-phase-details.md (`Task P01-T02`), src/core/src/zava_forward/core/rai_control_plane.py (lines 23-40, 937-995), src/core/src/zava_forward/core/ai_registry.py (lines 94-108, 135-153), src/core/src/zava_forward/core/assistants.py (lines 889, 1639-1645, 1662), src/api/tests/test_assistant_release.py (lines 252-256).
* Concern: `Task P01-T02` specifies referencing `_assistants.REGISTRY` and `_assistants.runtime_binding(task_name, ai_obj)` and falling into `Else (task_name in ai_registry.LEGACY): ... dep = ai_registry.legacy_deployment(task_name, ai_obj), and binding = ai_registry.legacy_binding(task_name, ai_obj, dep)`. Three issues follow directly from the code: (1) `rai_control_plane.py` does not import `assistants` or define `_assistants: Any`, and calling untyped functions directly on `ai_registry` instead of the module's `_ai_registry: Any` alias fails `src/core` strict `mypy` (`[no-untyped-call]`) and raises `NameError` for `_assistants`; (2) `ai_registry.legacy_deployment(task, ai)` executes `getattr(ai, LEGACY[task]["route"])` with no default, whereas `Assistants.registry(user)` runs against scripted test providers (`self.provider` in `test_assistants.py` and `test_assistant_release.py`) that are not `Ai` instances and may omit `.fast` or `.strong` (which is why `assistants.py` lines 889 and 1639 use `getattr(..., "fast", "")` and `getattr(..., "strong", "")` with `""` defaults before calling `exercise_acceptance_report`); and (3) an unconditional `else:` branch raises `KeyError` inside `LEGACY[task]` if any non-assistant, non-legacy registry task (such as `chat-case-conversation` or `aftercare-concern-pack`) is enabled in a test or future configuration.
* Impact: Implementing `P01-T02` as written will fail `cd src/core && python3 -m mypy`, raise `NameError` or `AttributeError` during `self.service.registry(...)` in existing `src/api/tests/test_assistant_release.py` tests, and raise `KeyError` instead of failing closed on non-legacy enabled tasks.
* Smallest useful change: Update `FR-H03` and `Task P01-T02` to (a) import `assistants` and bind `_assistants: Any = assistants` alongside `_ai_registry: Any = ai_registry` in `rai_control_plane.py`, (b) branch with `if task_name in _assistants.REGISTRY:` / `elif task_name in _ai_registry.LEGACY:` / `else: has_valid_live = False`, (c) resolve legacy deployment with a safe default (`route = str(_ai_registry.LEGACY[task_name]["route"]); dep = getattr(ai_obj, route, "") or ""`) before calling `_ai_registry.legacy_binding(task_name, ai_obj, dep)`, and (d) resolve `now_ts` from `assistants_service.now(cursor_db)` when `assistants_service` has SQL active, else `cursor_db.execute(store._epoch_sql)` when `hasattr(store, "_epoch_sql")`, falling back to `time.time()` on exception.
* Action owner: planning_parent
* Exact resolving evidence: Revised `FR-H03` in .copilot-tracking/plans/2026-11-15/rai-218-release-admission-hardening-plan.md and `Task P01-T02` in .copilot-tracking/details/2026-11-15/rai-218-release-admission-hardening-phase-details.md incorporating `_assistants: Any`, `_ai_registry: Any`, explicit `elif task_name in _ai_registry.LEGACY:` fail-closed branching, default-safe `getattr(ai_obj, route, "") or ""`, and DB-clock fallback.
* Decision route: direct_planner_correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: `AC-H04` and `P02-T01` reference a non-existent `"all_verified"` key and omit the live-endpoint baseline needed for `/api/ai/report` to fail before `P01`

* Related IDs: `AC-H01`, `AC-H03`, `AC-H04`, `NFR-H03`, `P02`, `P02-T01`
* Evidence: .copilot-tracking/plans/2026-11-15/rai-218-release-admission-hardening-plan.md (`AC-H04`), .copilot-tracking/details/2026-11-15/rai-218-release-admission-hardening-phase-details.md (`Task P02-T01`), src/core/src/zava_forward/core/rai_control_plane.py (lines 873-878, 900-903), src/core/src/zava_forward/core/rai_release.py (lines 224-230), src/core/tests/release_support.py (lines 47-48, 70-76), src/api/tests/test_rai_release_readiness_api_218.py (lines 66-71).
* Concern: First, `AC-H04` and `Task P02-T01` state `verify_traceability_targets()["all_verified"] is True`, whereas `verify_traceability_targets()` in `rai_control_plane.py` returns keys `{"all_resolved", "verified_target_count", "unresolved"}` (and `traceability_summary()` returns `"targets_verified"` and `"complete"`), so asserting `["all_verified"]` raises `KeyError`. Second, `Task P02-T01` expects all new tests to fail before `P01`, but in `RaiReleaseReadinessApi218Tests.setUp` (`test_rai_release_readiness_api_218.py`), `self.store.ai.endpoint` defaults to `""`, causing `release_support.install` to skip all six `legacy:*` tasks so `oq017_named_live_releases_recorded.passed` is already `False` before `P01`; additionally, `rai_release.missing_binding` (line 227) already checks `isinstance(expires, bool)`, whereas the pre-`P01` `bool` expiry gap was in `_inspect_sql_live_releases`.
* Impact: Causes `KeyError: 'all_verified'` if coded literally and risks an HTTP API regression test in `test_rai_release_readiness_api_218.py` that passes trivially without exercising `RV-001` or `RV-002`.
* Smallest useful change: Replace `verify_traceability_targets()["all_verified"]` with `verify_traceability_targets()["all_resolved"]` in `AC-H04` and `Task P02-T01`, keep `expires=True` paired inside the partial-key `missing_binding` unit test (and/or in SQL row readiness inspection), and specify in `Task P02-T01` that the `test_rai_release_readiness_api_218.py` test first configures `self.store.ai.endpoint = "https://zava-live-openai.invalid"` and calls `release_support.install(self.store, self.store.ai, cls="actual")` to observe `oq017_named_live_releases_recorded.passed is True` before mutating a stored SQL release row (omitting `OQ-017` keys or drifting `prompt_version` / `model_version`) to prove `passed` flips to `False` and `rai_exercise_acceptance.passed` stays `True` without mutating SQL row status.
* Action owner: planning_parent
* Exact resolving evidence: Updated `AC-H04` in .copilot-tracking/plans/2026-11-15/rai-218-release-admission-hardening-plan.md and `Task P02-T01` in .copilot-tracking/details/2026-11-15/rai-218-release-admission-hardening-phase-details.md using `"all_resolved"` and specifying the positive-then-drifted `/api/ai/report` test sequence.
* Decision route: direct_planner_correction

## Strengths and Residual Risk

* Preserving the outer `if live and ("approved_by" in record or "named_approval_id" in record):` guard in `rai_release.missing_binding` while normalizing SQL-loaded records with `setdefault("approved_by", None)` and `setdefault("named_approval_id", None)` in `assistant_release.assessment(..., live=True)` cleanly closes `RV-001` across all live dispatch and readiness callers (`Assistants.admission`, `Assistants.release_reference`, `SqlStore.release_assessment`, and `rai_control_plane._inspect_sql_live_releases`) without breaking existing isolated 4-key unit tests (`test_rai_release.py`, `test_rai_threshold_live_approval_guard.py`) or `rai_release.reference` digests on valid `actual` rows.
* Skipping `invalidate_changed` for `legacy:*` capabilities inside `assistant_release.assessment` continues to preserve dual `fast` and `strong` deployment rows installed under `legacy:{task}`, while `rai_release.select` still enforces `BOUND` equality, serving-model attestation (`model_version` vs `model_version_strong`), live monitoring thresholds, and `OQ-017` named approval on whichever active row matches the route deployment.
* Delegating SQL release inspection to `_assistant_release.assessment` inside `with _assistant_release.read_only():` also upgrades error handling from SQLite-only `sqlite3.Error` to `db.driver.Error if hasattr(db, "driver") else sqlite3.Error` without mutating `assistant_releases` or `assistant_events`.
* Explicitly accepted residual risk: Live office-holder appointments (`OQ-017`), representative non-synthetic cohort manifests and live disparity thresholds (`OQ-018`), and Legal/DPO automated decision-making sign-off (`OQ-019`) remain deferred owner gates outside this defect-hardening child task, and validation intentionally stays at the caller-specified focused tier.

## Questions or Blocking Evidence Gaps

* None. All required evidence is present in the supplied plan, research, parent review, and source/test files, and both findings are direct planner corrections.

## Limitations

* This critique is a static, read-only credibility assessment of the supplied plan, phase details, research, parent review, and workspace source/test files; no code edits or test executions were performed during critique.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning_parent
* Smallest next action: Apply direct planner revisions for `PC-001` and `PC-002` to `.copilot-tracking/plans/2026-11-15/rai-218-release-admission-hardening-plan.md` and `.copilot-tracking/details/2026-11-15/rai-218-release-admission-hardening-phase-details.md`, record their critique dispositions, finalize planning without another critique pass, and proceed to `rpi-implement`.
* User response required: no
