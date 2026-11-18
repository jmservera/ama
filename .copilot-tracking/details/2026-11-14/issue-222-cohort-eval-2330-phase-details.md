<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #222 Cohort and Missing-Data Evaluation Record (`OQ-018`)

## Metadata

* Task ID: issue-222-cohort-eval-2330
* Task slug: issue-222-cohort-eval-2330
* Related plan: .copilot-tracking/plans/2026-11-14/issue-222-cohort-eval-2330-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-14/issue-222-cohort-eval-2330-research.md, docs/reference/research/evaluation/cohort-evaluation-review-pack.md

## Phase Index

| Phase ID | Name                                                               | Status | Detail sections        |
|----------|--------------------------------------------------------------------|--------|------------------------|
| P01      | Core Cohort Evaluation `OQ-018` Boundary and Export Contract       | Ready  | P01, P01-T01, P01-T02  |
| P02      | Agents Harness Propagation and HTTP API Runtime/Export Surfaces    | Ready  | P02, P02-T01, P02-T02  |
| P03      | Documentation Sync, Focused Validation, and Local Commit Prep      | Ready  | P03, P03-T01           |

<!-- rpi:phase id=P01 -->
## P01: Core Cohort Evaluation `OQ-018` Boundary and Export Contract

### Context

`src/core/src/zava_forward/core/cohort_eval.py` builds versioned cohort and missing-data evaluation records (`RECORD_VERSION = "cohort-missing-data-evaluation-v1"`), checked strictly by `mypy` and `ruff`. Research (`C1`-`C4`, `C13`, `C16`, `C17`) identified that `evaluate(...)` does not yet emit `owner_approval_status`, `lawful_analysis_fields`, `lawful_analysis_fields_approved`, `live_activation_allowed`, `synthetic_not_fairness_evidence`, or `non_fairness_provenance_notice`, nor reject fictional owner tokens (`"fictional"`, `"placeholder"`, `"mock"`, `"synthetic"`) or undated/malformed approval timestamps on live activation.

### Intent

Extend `cohort_eval.py` with explicit, hash-bound `OQ-018` owner-approval state, lawful-field approval state, synthetic non-fairness disclaimer fields, strict `live=True` date/owner checks, and a fail-closed `export_record(...)` function, backed by focused unit tests.

### Boundaries

* Included: `src/core/src/zava_forward/core/cohort_eval.py`, `src/core/tests/test_cohort_eval.py`, `src/core/tests/test_rai_threshold_live_approval_guard.py`.
* Excluded: Modifying `ranking.py` rule order or mutating `cohort_eval_fixture.py`'s existing offline fixture shape.

### Likely Targets

* `src/core/src/zava_forward/core/cohort_eval.py`: Core approval validation, record fields, `live=True` gap enforcement, and `export_record(...)`.
* `src/core/tests/test_cohort_eval.py`: Focused unit tests for approval states, lawful fields, provenance notice, export integrity, and existing Issue #222 invariants.
* `src/core/tests/test_rai_threshold_live_approval_guard.py`: Live guard tests for fictional-owner rejection, ISO/epoch `approved_at` validation, and undated live rejection.

### Dependencies

* None.

### Validation Expectations

* `cd src/core && python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check .`
* `cd src/core && PYTHONPATH=src:tests python3 -m unittest discover -s tests -p "test_cohort_eval.py" -q && PYTHONPATH=src:tests python3 -m unittest discover -s tests -p "test_rai_threshold_live_approval_guard.py" -q && PYTHONPATH=src:tests python3 -m unittest discover -s tests -p "test_paired_equity.py" -q`

### Completion Evidence

* Zero `mypy`/`ruff` findings in `src/core` and passing core cohort/live-guard/paired-equity unit tests loaded from worktree `src/core/src`.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Implement `owner_approval_status`, `lawful_analysis_fields_approved`, non-fairness provenance, and `export_record` in `cohort_eval.py`

#### Context

* `manifest_digest(manifest)` already hashes `{k: v for k, v in manifest.items() if k != "approval"}` (`cohort_eval.py:51-53`), which automatically binds `"lawful_analysis_fields"` alongside `"cases"`, `"cohorts"`, and `"thresholds"` without altering existing manifest digests.
* Existing tests:
  * `test_cohort_eval.py` calls `evaluate(m, clean_observed(m))` (`live=False`) with `cohort_eval_fixture.approved(m)` (`"Data lead (fictional)"`, no date) and expects `activation_allowed == True` for offline disposition mechanics and `fairness_evidence == True` on line 246 when `m["synthetic"] = False`.
  * `test_rai_threshold_live_approval_guard.py` calls `evaluate(m, clean_observed(m), live=True, now=NOW)` with `HUMAN` (`"Priya Shah, Data Lead"`, `"Tom Reed, DPO"`, `"Amina Okafor, RAI Owner"`, `"expires": NOW + 3600`, `synthetic=False`) and expects `blockers == []` and `activation_allowed == True`.

#### Intent

Implement exact approval/provenance helpers and `export_record(...)` in `cohort_eval.py`:
1. Constants: `OWNER_APPROVAL_APPROVED = "approved"`, `OWNER_APPROVAL_PENDING = "pending_owner_approval"`, `OWNER_APPROVAL_UNAPPROVED = "unapproved"`, `FICTIONAL_OWNER_TOKENS = frozenset({"fictional", "placeholder", "mock", "synthetic", "example", "todo", "tbd", "unapproved", "unknown"})`, and explicit `NON_FAIRNESS_PROVENANCE_NOTICE` / approved provenance notice strings referencing `OQ-018`. Preserve `manifest_digest(manifest)` as `digest({k: v for k, v in manifest.items() if k != "approval"})`.
2. `_real_human_owner(value: object) -> bool`: `named_human(value)` and no whitespace/punctuation token in `FICTIONAL_OWNER_TOKENS`.
3. `_valid_lawful_fields(manifest: Mapping[str, Any]) -> tuple[list[str], bool]`:
   * If `"lawful_analysis_fields"` is in `manifest`: verify it is a non-string `Sequence` of non-empty strings (each `named(item)`), returning `([str(item).strip() for item in raw], True)` when valid and non-empty, else `([], False)`.
   * Otherwise derive declared cohort dimension names from `manifest.get("cohorts")` when it is a non-empty `Mapping` whose keys satisfy `named(k)`, returning `(list(cohorts.keys()), True)`, else `([], False)`.
4. `_approval_dated_and_current(approval: Mapping[str, Any], now: float | None) -> tuple[bool, str | None]`:
   * Validate optional `"expires"`: if `"expires" in approval`, require `_finite_number(approval.get("expires"))` and `_finite_number(now)` and `float(approval["expires"]) > float(now)`, else return `(False, "live_approval_expired")`.
   * Validate optional `"approved_at"` / `"approved_on"`: for whichever key is present, require a valid ISO-8601 calendar date (`date.fromisoformat`) or ISO-8601 datetime (`datetime.fromisoformat`, normalizing trailing `Z`) or finite positive `int | float` (not `bool`, and `<= float(now)` when `_finite_number(now)`); otherwise return `(False, "live_approval_undated")`.
   * If none of `("expires", "approved_at", "approved_on")` is in `approval`, return `(False, "live_approval_undated")`.
   * Return `(True, None)`.
5. Compute `owner_approval_status` and `lawful_analysis_fields_approved`:
   * Let `fields, fields_valid = _valid_lawful_fields(manifest)`. If `"lawful_analysis_fields" in manifest` and not `fields_valid`, append blocker `("unapproved_lawful_analysis_fields", "lawful analysis fields must be non-empty owner-approved field names")` (and add `"unapproved_lawful_analysis_fields"` outside `DISPOSABLE` and inside `MEASUREMENT_BLOCKERS`).
   * Dated real-human approval holds (`dated_human_ok`) iff `not synthetic`, `_thresholds_approved(manifest)`, `fields_valid`, all three owners pass `_real_human_owner(...)`, and `_approval_dated_and_current(approval, now)[0]` is `True`.
   * Date-key defect check (`has_invalid_or_expired_date`): `isinstance(approval, Mapping)` and any explicitly supplied `"approved_at"`/`"approved_on"` is malformed or `"expires" in approval` fails when `_finite_number(now)` (expired) or is non-numeric (`None`/`bool`/`NaN`).
   * `owner_approval_status`:
     * `"approved"` when `dated_human_ok` is `True`.
     * `"pending_owner_approval"` when `isinstance(approval, Mapping)` and `_thresholds_approved(manifest)` and `fields_valid` and `all(named_human(approval.get(k)) for k in ("cohorts_owner", "lawful_fields_owner", "thresholds_owner"))` and not `has_invalid_or_expired_date` (e.g., bound undated/fictional offline fixtures or synthetic manifests, or `expires`-only manifests evaluated offline with `now=None`).
     * `"unapproved"` otherwise (default when no `approval` mapping is supplied, unbound digest, blank/agent/non-human owner, invalid thresholds, invalid lawful fields, malformed date, or expired approval).
   * `lawful_analysis_fields_approved = (owner_approval_status == OWNER_APPROVAL_APPROVED)`.
6. Tighten `_live_gaps(manifest, now)`:
   * Keep `constructed_thresholds_live` when `synthetic` is `True`.
   * If not `fields_valid`, emit `("unapproved_lawful_analysis_fields", "lawful analysis fields must be non-empty owner-approved field names")`.
   * Require `_real_human_owner(approval.get(k))` for all three owners (`live_approval_not_named_human`) so fictional/placeholder owners fail `live=True` even with a future `expires`.
   * Check `"expires" in approval`: if not (`_finite_number(approval.get("expires"))` and `_finite_number(now)` and `float(approval["expires"]) > float(now)`), emit `("live_approval_expired", "live approval needs an unexpired timestamp")`.
   * Check `"approved_at"` / `"approved_on"`: if either key is present and fails ISO/epoch validation, or if none of `("expires", "approved_at", "approved_on")` is in `approval`, emit `("live_approval_undated", "live approval needs a valid approval date")`.
7. Compute `fairness_evidence`, `live_activation_allowed`, `synthetic_not_fairness_evidence`, and `non_fairness_provenance_notice`:
   * `fairness_evidence = bool(not synthetic and _thresholds_approved(manifest) and fields_valid and not any(b["code"] in MEASUREMENT_BLOCKERS for b in blockers) and (not live or owner_approval_status == OWNER_APPROVAL_APPROVED))` (preserving `test_cohort_eval.py:246` offline while blocking `fairness_evidence` on invalid lawful fields or failed `live=True` owner approval).
   * `live_activation_allowed = bool(activation_allowed and owner_approval_status == OWNER_APPROVAL_APPROVED and lawful_analysis_fields_approved and not _live_gaps(manifest, now))` (inheriting `not open_blockers` and `DISPOSABLE` rejection rules from `activation_allowed`).
   * `synthetic_not_fairness_evidence = True`.
   * `non_fairness_provenance_notice`: explicit message citing `OQ-018` explaining that synthetic results are never fairness evidence and that cohorts, lawful analysis fields, and thresholds require dated human owner approval before live use.
8. Add `export_record(record: Mapping[str, Any]) -> dict[str, Any]`:
   * Deep-copy / normalize `record` without `record_hash`, verify `record.get("record_version") == RECORD_VERSION` and `digest(body) == record.get("record_hash")`, verify `record.get("synthetic_not_fairness_evidence") is True` and non-empty `non_fairness_provenance_notice`, and verify that if `record.get("synthetic")` is `True` or `record.get("owner_approval_status") != OWNER_APPROVAL_APPROVED` or not `record.get("lawful_analysis_fields_approved")`, then `live_activation_allowed` is `False` (and if `record.get("synthetic")` is `True`, `fairness_evidence` is `False`); raise `ValueError` on any violation. Return a fresh canonical copy ready for JSON serialization or HTTP response.

#### Boundaries

* Included: `src/core/src/zava_forward/core/cohort_eval.py`.
* Excluded: Changing callers outside `cohort_eval.py` (handled in P02).

#### Likely Targets

* `src/core/src/zava_forward/core/cohort_eval.py`: Add constants, helpers, `evaluate(...)` record fields, and `export_record(...)`.

#### Dependencies

* None.

#### Validation Expectations

* `mypy` and `ruff` pass with zero warnings in `src/core`.

#### Completion Evidence

* `cohort_eval.evaluate` and `cohort_eval.export_record` satisfy all type and runtime checks.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Add focused core unit tests for `OQ-018` approval states, fictional/undated/synthetic rejection, and export tamper checks

#### Context

Core tests live in `src/core/tests/test_cohort_eval.py` and `src/core/tests/test_rai_threshold_live_approval_guard.py` (both strictly checked by `mypy` and `ruff`).

#### Intent

Add focused unit tests proving:
1. Default unapproved manifest emits `owner_approval_status == "unapproved"`, `lawful_analysis_fields_approved is False`, `live_activation_allowed is False`, `synthetic_not_fairness_evidence is True`, and `OQ-018` in `non_fairness_provenance_notice`.
2. Undated fictional offline fixture (`manifest()`) emits `owner_approval_status == "pending_owner_approval"`, `lawful_analysis_fields_approved is False`, `live_activation_allowed is False`, `fairness_evidence is False`, and `synthetic_not_fairness_evidence is True`.
3. Non-synthetic manifest with dated real-human owner approval (`approved_at: "2026-11-14"`, real named owners for cohorts, lawful fields, and thresholds) emits `owner_approval_status == "approved"`, `lawful_analysis_fields_approved is True`, `live_activation_allowed is True`, and passes `evaluate(..., live=True)`; whereas the exact same dated real-human approval on `synthetic=True` keeps `owner_approval_status == "pending_owner_approval"`, `lawful_analysis_fields_approved is False`, `fairness_evidence is False`, `live_activation_allowed is False`, and blocks `live=True`.
4. Fictional owner tokens (`"Data lead (fictional)"`) with future `expires` are rejected on `live=True` (`live_approval_not_named_human`) and never gain `owner_approval_status == "approved"`.
5. Editing `lawful_analysis_fields` after `approve(...)` or supplying empty/blank `lawful_analysis_fields` invalidates `lawful_analysis_fields_approved` and blocks activation.
6. `export_record(...)` round-trips valid records and raises `ValueError` when tampered (`record_hash` mismatch, `synthetic_not_fairness_evidence=False`, or synthetic `fairness_evidence=True` / unapproved `live_activation_allowed=True`).

#### Boundaries

* Included: `src/core/tests/test_cohort_eval.py`, `src/core/tests/test_rai_threshold_live_approval_guard.py`.
* Excluded: Duplicate restatement of existing tests.

#### Likely Targets

* `src/core/tests/test_cohort_eval.py`: Up to 5 focused test methods.
* `src/core/tests/test_rai_threshold_live_approval_guard.py`: Up to 3 focused test methods.

#### Dependencies

* P01-T01.

#### Validation Expectations

* All tests in `test_cohort_eval.py`, `test_rai_threshold_live_approval_guard.py`, and `test_paired_equity.py` pass under `PYTHONPATH=src:tests`.

#### Completion Evidence

* Passing `unittest`, `mypy`, and `ruff` output in `src/core`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Agents Harness Propagation and HTTP API Runtime/Export Surfaces

### Context

`ai_eval.cohort_report()` (`src/agents/src/zava_forward/agents/ai_eval.py:601`) builds `run_eval()["cohorts"]`, which `GET /api/ai/report` (`src/api/src/zava_forward/api/server.py:902`) exposes over HTTP. CLI runners `cohort_ranking_eval.py` and `cohort_ai_eval.py` also emit JSON evaluation exports via `--json`.

### Intent

Ensure every runtime/API cohort payload and JSON export carries `owner_approval_status`, `lawful_analysis_fields`, `lawful_analysis_fields_approved`, `live_activation_allowed`, `synthetic_not_fairness_evidence: True`, and `non_fairness_provenance_notice`, validated through `cohort_eval.export_record(...)`, and expose a direct manager-only HTTP export route `GET /api/ai/cohort-evaluation` in addition to enriching `GET /api/ai/report`.

### Boundaries

* Included: `src/agents/src/zava_forward/agents/{ai_eval,cohort_ranking_eval,cohort_ai_eval}.py`, `src/api/src/zava_forward/api/server.py`, and their focused test files (`test_ai_eval.py`, `test_cohort_ranking_eval.py`, `test_cohort_ai_eval.py`, `test_ai_tasks.py`, `test_role_endpoint_inventory.py`).
* Excluded: Frontend UI changes (`web/*.js`) or database schema changes.

### Likely Targets

* `src/agents/src/zava_forward/agents/ai_eval.py`: Enrich `cohort_report()` and add `cohort_evaluation_export()` helper returning `export_record(...)` outputs for deterministic ranking and AI priority offline cohort runs.
* `src/agents/src/zava_forward/agents/cohort_ranking_eval.py` and `cohort_ai_eval.py`: Validate outputs via `cohort_eval.export_record(...)`.
* `src/api/src/zava_forward/api/server.py`: Map `"/api/ai/cohort-evaluation": "ai_report"` in `get_kind`, expose enriched `evaluation.cohorts` in `GET /api/ai/report` (preserving the top-level 4-key contract), and serve manager-only `GET /api/ai/cohort-evaluation`.
* `src/agents/tests/test_ai_eval.py`, `src/agents/tests/test_cohort_ranking_eval.py`, `src/agents/tests/test_cohort_ai_eval.py`, `src/api/tests/test_ai_tasks.py`, `src/api/tests/test_role_endpoint_inventory.py`: Focused assertions and `GET_ENDPOINTS` registration.

### Dependencies

* P01.

### Validation Expectations

* `cd src/agents && python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check .`
* `cd src/agents && PYTHONPATH=../core/src:src:tests:../core/tests python3 -m unittest discover -s tests -p "test_cohort*.py" -q && PYTHONPATH=../core/src:src:tests:../core/tests python3 -m unittest discover -s tests -p "test_ai_eval.py" -q`
* `cd src/api && python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check .`
* `cd src/api && PYTHONPATH=../core/src:../agents/src:src:tests:../core/tests:../agents/tests python3 -m unittest tests/test_ai_tasks.py tests/test_role_endpoint_inventory.py tests/test_list_export_inventory.py -q`

### Completion Evidence

* Zero `mypy`/`ruff` errors and 100% green focused unit/API/inventory suites in `src/agents` and `src/api`.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Propagate `OQ-018` fields and `export_record` in `ai_eval.py`, `cohort_ranking_eval.py`, and `cohort_ai_eval.py` with tests

#### Context

`test_ai_eval.py:213-221` asserts `co["status"]`, `co["activation_allowed"]`, `co["synthetic"]`, `co["fairness_evidence"]`, `co["blockers"]`, `co["dimensions"]`, `co["total_cases"]`, and `co["ai_task_cohorts"].startswith("not evaluated")`. All existing keys must remain intact while adding the new `OQ-018` fields and `cohort_evaluation_export()`.

#### Intent

1. In `cohort_ranking_eval.run(...)` and `cohort_ai_eval.run(...)`, pass the evaluated record through `cohort_eval.export_record(...)` so every programmatic and `--json` CLI export is integrity- and provenance-verified.
2. In `ai_eval.cohort_report()`, preserve all existing keys (`cohort_ranking_eval.run()` only, avoiding executing `Store.ai_priority` inside `run_eval()` fault-injection tests) and add `record_version`, `owner_approval_status`, `lawful_analysis_fields`, `lawful_analysis_fields_approved`, `live_activation_allowed`, `synthetic_not_fairness_evidence`, `non_fairness_provenance_notice`, and `authority_gap`.
3. Add `ai_eval.cohort_evaluation_export()` returning a canonical export envelope containing `record_version`, `authority_gap`, `owner_approval_status: "unapproved"`, `lawful_analysis_fields_approved: False`, `live_activation_allowed: False`, `synthetic_not_fairness_evidence: True`, `non_fairness_provenance_notice`, `ranking` (`cohort_ranking_eval.run()`), and `ai_priority` (`cohort_ai_eval.run("faithful")`).
4. Update `test_ai_eval.py`, `test_cohort_ranking_eval.py`, and `test_cohort_ai_eval.py` with focused assertions on the new `OQ-018` and non-fairness fields.

#### Boundaries

* Included: `src/agents/src/zava_forward/agents/{ai_eval,cohort_ranking_eval,cohort_ai_eval}.py` and their tests.
* Excluded: HTTP server wiring (handled in P02-T02).

#### Likely Targets

* `src/agents/src/zava_forward/agents/ai_eval.py`
* `src/agents/src/zava_forward/agents/cohort_ranking_eval.py`
* `src/agents/src/zava_forward/agents/cohort_ai_eval.py`
* `src/agents/tests/test_ai_eval.py`, `test_cohort_ranking_eval.py`, `test_cohort_ai_eval.py`

#### Dependencies

* P01-T01.

#### Validation Expectations

* `mypy`, `ruff`, and `test_cohort_ranking_eval.py`, `test_cohort_ai_eval.py`, `test_ai_eval.py` pass in `src/agents`.

#### Completion Evidence

* Clean `src/agents` test and static-check execution.

#### Unresolved Items

* None.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Expose `OQ-018` cohort fields on `GET /api/ai/report` (`evaluation.cohorts`) and manager-only `GET /api/ai/cohort-evaluation` in `server.py` with API and role-inventory tests

#### Context

* `server.py` enforces `projection.allowed(u, get_kind(url.path))` at line 563 before reaching `/api/ai/...` handlers, maps `"/api/ai/report": "ai_report"` in `get_kind` (line 311), and handles `GET /api/ai/report` for `MANAGER_ROLES` (lines 902-932).
* `src/api/tests/test_ai_consumption_api.py` enforces `set(held) == {"evaluation", "live", "registry", "consumption"}` on `GET /api/ai/report`.
* `src/api/tests/test_role_endpoint_inventory.py` checks every `/api/...` literal in `server.py` against `GET_ENDPOINTS` (`list[str]`) / `POST_ENDPOINTS`.

#### Intent

1. In `src/api/src/zava_forward/api/server.py`:
   * Map `"/api/ai/cohort-evaluation": "ai_report"` in `get_kind` so `projection.allowed(...)` applies the exact same role gate as `"/api/ai/report"`.
   * Preserve `GET /api/ai/report`'s top-level keys (`{"evaluation", "live", "registry", "consumption"}`) while `evaluation["cohorts"]` exposes the enriched `ai_eval.cohort_report()` `OQ-018` fields.
   * Add manager-only `GET /api/ai/cohort-evaluation` (checking `u["role"] not in MANAGER_ROLES` -> HTTP 403 and rejecting any unknown query parameters -> HTTP 400, matching `GET /api/ai/report`'s fail-closed hygiene) returning `ai_eval.cohort_evaluation_export()`.
2. Append `"/api/ai/cohort-evaluation"` to `GET_ENDPOINTS` and `test_contractor_audit_view_and_export_are_denied` in `src/api/tests/test_role_endpoint_inventory.py`.
3. Add focused API tests in `src/api/tests/test_ai_tasks.py` verifying:
   * `GET /api/ai/report` exposes `evaluation["cohorts"]` with `owner_approval_status == "unapproved"`, `lawful_analysis_fields_approved is False`, `live_activation_allowed is False`, `synthetic_not_fairness_evidence is True`, `fairness_evidence is False`, and `OQ-018` in `non_fairness_provenance_notice`.
   * `GET /api/ai/cohort-evaluation` returns HTTP 200 for Programme Manager with full `export_record`-verified records for `ranking-policy` and `ai-priority-recommendation` (`sensor_completeness`, `support_need`, `source_completeness`, `appointment_history`), reconciled counts/intervals, `unapproved_thresholds` blockers, and `OQ-018` non-fairness disclaimer, HTTP 403 for non-manager roles, HTTP 400 on unknown query parameters, and HTTP 404 on POST.

#### Boundaries

* Included: `src/api/src/zava_forward/api/server.py`, `src/api/tests/test_ai_tasks.py`, `src/api/tests/test_role_endpoint_inventory.py`.
* Excluded: Unrelated API routes or frontend assets.

#### Likely Targets

* `src/api/src/zava_forward/api/server.py`
* `src/api/tests/test_ai_tasks.py`
* `src/api/tests/test_role_endpoint_inventory.py`

#### Dependencies

* P02-T01.

#### Validation Expectations

* `mypy`, `ruff`, and `test_ai_tasks.py`, `test_role_endpoint_inventory.py`, `test_list_export_inventory.py` pass in `src/api`.

#### Completion Evidence

* Clean `src/api` test and static-check execution.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Documentation Sync, Focused Validation, and Local Commit Prep

### Context

Repository rules require updating directly coupled documentation alongside executable changes and verifying the Focused validation tier before review and commit.

### Intent

Document the `OQ-018` approval/provenance fields and `GET /api/ai/cohort-evaluation` endpoint in `src/core/README.md`, `src/agents/README.md`, and `src/api/README.md`, run the complete Focused validation matrix across all touched directories, and reconcile tracking artifacts ahead of `rpi-review`.

### Boundaries

* Included: `src/core/README.md`, `src/agents/README.md`, `src/api/README.md`, and Focused validation execution.
* Excluded: Remote `git push` or full-gate `rpi-checks.py --all`.

### Likely Targets

* `src/core/README.md`
* `src/agents/README.md`
* `src/api/README.md`

### Dependencies

* P01, P02.

### Validation Expectations

* `mypy`, `ruff check .`, `ruff format --check .`, and all focused cohort/AI/inventory unit tests exit 0 across `src/core`, `src/agents`, and `src/api` with verified worktree module `__file__` provenance.

### Completion Evidence

* Recorded command outputs and zero diff drift in `.copilot-tracking/changes/2026-11-14/issue-222-cohort-eval-2330-changes.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Update `src/core/README.md`, `src/agents/README.md`, and `src/api/README.md` and run Focused validation (`mypy`, `ruff`, unit/API tests)

#### Context

Component READMEs document `cohort_ranking_eval`, `cohort_ai_eval`, `ai_eval`, and `GET /api/ai/report`.

#### Intent

Add concise documentation of `owner_approval_status`, `lawful_analysis_fields_approved`, `live_activation_allowed`, `synthetic_not_fairness_evidence`, `non_fairness_provenance_notice`, `cohort_eval.export_record`, and manager-only `GET /api/ai/cohort-evaluation`, then execute all Focused checks.

#### Boundaries

* Included: `src/core/README.md`, `src/agents/README.md`, `src/api/README.md`.
* Excluded: Editing immutable regulatory snapshots or `docs/case_study_48_original.md`.

#### Likely Targets

* `src/core/README.md`, `src/agents/README.md`, `src/api/README.md`.

#### Dependencies

* P01, P02.

#### Validation Expectations

* Clean Markdown links/style and exit code 0 across all Focused tier checks.

#### Completion Evidence

* Verified Focused validation transcript in changes artifact.

#### Unresolved Items

* None.
