<!-- markdownlint-disable-file -->
# RPI Phase Details: Issue #81 Exercise-Scenario Safety and Resident Consent Gate Verification

## Metadata

* Task ID: issue-81-safety-consent-gates
* Task slug: issue-81-safety-consent-gates
* Related plan: .copilot-tracking/plans/2026-11-15/issue-81-safety-consent-gates-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/issue-81-safety-consent-gates-research.md, docs/brds/agentic-retrofit-programme-brd.md, docs/prds/zava-forward-retrofit-programme-demonstrator.md

## Phase Index

| Phase ID | Name                                                            | Status | Detail sections        |
|----------|-----------------------------------------------------------------|--------|------------------------|
| P01      | Fail-Closed Safety and Authorised-Exception Gate Hardening      | Ready  | P01, P01-T01, P01-T02  |
| P02      | Deterministic Exercise-Scenario Safety and Consent Verifier     | Ready  | P02, P02-T01           |
| P03      | Verification Suite, Core Documentation, and Focused Validation  | Ready  | P03, P03-T01, P03-T02  |

<!-- rpi:phase id=P01 -->
## P01: Fail-Closed Safety and Authorised-Exception Gate Hardening

### Context

Research (`C1`, `C2`, `C8`, `C9`, `C11`, `C17`) verified that `Store` already guards controlled transitions through `require_safety_clear`, `require_resident_clear`, and `require_booking_gates`, but Wave 3 contrarian analysis exposed three fail-closed edge cases: `gates.booking_gates` ignores standalone `safeguarding_items` / item-shaped `safeguarding` records, `Store._open_safety_items` does not fail closed when `hazards` is missing/non-list/non-dict or `safeguarding_items` is malformed, and `resident_decisions.py` has no structured validator for an explicitly authorised works exception (`BG-005`, `RULE-002`, `FR-014` `AC-018`).

### Intent

Harden `gates.py`, `store.py`, and `resident_decisions.py` so safety and consent/exception checks fail closed consistently across direct gate evaluation and every `Store`/`SqlStore` transition without breaking existing unit tests.

### Boundaries

* Included: `gates.booking_gates`, `Store._open_safety_items`, `resident_decisions.validate_authorised_works_exception`, and `_resident_decision_gate` fallback when `authorised_works_exceptions` is explicitly present.
* Excluded: Changing existing refusal message prefixes relied on by `test_gates.py`, `test_hazard_referral.py`, or `test_resident_decisions.py`, or allowing an exception to bypass tenure holds, open `"Needs human review"`, or safety holds.

### Likely Targets

* `src/core/src/zava_forward/core/gates.py`: Extend `booking_gates` safety evaluation to inspect `safeguarding_items` and item-shaped `safeguarding` records.
* `src/core/src/zava_forward/core/store.py`: Normalize missing or malformed `hazards` and `safeguarding_items` in `Store._open_safety_items` to an explicit `("Unverified safety evidence", "Building Safety Liaison")` blocker.
* `src/core/src/zava_forward/core/resident_decisions.py`: Add `validate_authorised_works_exception` and consult it in `_resident_decision_gate` when `Accepted` resident/representative consent is absent and `authorised_works_exceptions` is present for the bound measure.

### Dependencies

* None.

### Validation Expectations

* Existing `test_gates.py`, `test_hazard_referral.py`, `test_taskqueues.py`, and `test_resident_decisions.py` continue to pass unchanged.

### Completion Evidence

* Updated `gates.py`, `store.py`, and `resident_decisions.py` passing `mypy`, `ruff check`, and existing gate/safety/resident tests.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Harden standalone safeguarding, strict boolean `released`, and SQLite row tolerance in `gates.py`, `store.py`, and `sqlstore.py`

#### Context

In `gates.booking_gates`, `hazards = case.get("hazards")` currently yields `PASS` when `hazards == []` even if `case["safeguarding_items"]` holds an open safeguarding item or `case["safeguarding_items"] is None`. Moreover (`PC-002`), `taskqueues.is_open_safety_item` uses `bool(item.get("released"))`, which treats truthy non-booleans like `"false"` or `"pending"` as closed, and malformed legacy `case["safeguarding"]` (`"corrupt"`, `123`, `["corrupt"]`) is silently ignored. Meanwhile, `Store._open_safety_items` iterates `c.get("hazards", [])` directly, raising `TypeError`/`AttributeError` on `None` or non-dict entries and returning `[]` if `"hazards"` is absent, and `SqlStore._row` (`PC-001`) crashes on legacy string `appointments` entries present in `resident_preview_fixture.py`.

#### Intent

Ensure both `gates.booking_gates` and `Store._open_safety_items` enforce strict boolean `released` semantics and fail closed on standalone safeguarding items and missing/malformed safety structures while keeping minimal hazard-only dicts (`{"funding_ok": True, "hazards": [{"released": True}], "owner": "Sam"}`) and note-only canary dicts (`{"note": "..."}`) compatible, and guard `SqlStore._row` so `resident_preview_fixture.build` datasets load cleanly in `SqlStore`.

#### Boundaries

* Included:
  * Strict safety-item helper semantics (`PC-002`):
    * For a hazard `dict`: closed only when `h.get("released") is True`; if `"released"` is present and `h.get("released") is not None` and `type(h.get("released")) is not bool`, treat as malformed/unverified (`UNKNOWN` in `booking_gates`, unverified blocker in `_open_safety_items`).
    * For a standalone safeguarding item `dict`: if `"released"` is present and `item.get("released") is not None`, `type(item.get("released"))` must be `bool` (closed when `True`, open when `False`, malformed/unknown otherwise); when `item.get("released") is None`, closed only when `isinstance(item.get("status"), str)` and `item["status"].strip().casefold() in {"closed", "released", "resolved"}`.
    * Legacy `case["safeguarding"]` when present and not `None`: valid only if a note-only `dict` disjoint from `SAFEGUARDING_ITEM_KEYS` (ignored), an item `dict` intersecting `SAFEGUARDING_ITEM_KEYS`, or a `list` of `dict`s; any other shape (`str`, `int`, `list` containing non-`dict`) fails closed (`safe = None` in `booking_gates`, `[("Unverified safety evidence", "Building Safety Liaison")]` in `_open_safety_items`).
  * In `gates.booking_gates`: evaluate `hazards`, `safeguarding_items` (when key present), and `safeguarding` (when key present and not `None`) under the strict boolean/fail-closed rules above, yielding `None` (`UNKNOWN`) on malformed/missing structures, `False` (`FAIL`) on any open hazard/safeguarding item, and `True` (`PASS`) only when every present collection is well-formed and closed/released.
  * In `Store._open_safety_items`: if `not isinstance(c, Mapping)` or `"hazards" not in c` or `not isinstance(c.get("hazards"), list)` or any hazard/safeguarding entry is malformed or has non-boolean non-`None` `released`: return `[("Unverified safety evidence", "Building Safety Liaison")]` so `gate_reasons`, `status_line`, and `require_safety_clear` fail closed with `GateError`.
  * In `SqlStore._row` (`sqlstore.py:984`, `PC-001`): check `isinstance(a, dict) and a.get("outcome") == "Booked"` when computing `nxt` so legacy string `appointments` entries do not raise `TypeError`.
* Excluded: Altering `taskqueues.project_safety_clock_and_owner` output fields.

#### Likely Targets

* `src/core/src/zava_forward/core/gates.py`: Update `booking_gates` safety state calculation.
* `src/core/src/zava_forward/core/store.py`: Guard `Store._open_safety_items` against missing/malformed `hazards`, `safeguarding_items`, `safeguarding`, and non-boolean `released`.
* `src/core/src/zava_forward/core/sqlstore.py`: Guard `isinstance(a, dict)` in `SqlStore._row`.
* `src/core/src/zava_forward/core/taskqueues.py`: Align `is_open_safety_item` and `has_open_safety` with strict boolean `released` and malformed safety-container fail-closed handling for `SqlStore._row`.

#### Dependencies

* None.

#### Validation Expectations

* `PYTHONPATH=src:tests python3 -m unittest tests/test_gates.py tests/test_hazard_referral.py tests/test_taskqueues.py -q` passes.

#### Completion Evidence

* `gates.booking_gates` returns `FAIL` for open `safeguarding_items` and `UNKNOWN` for `safeguarding_items=None`, `released="false"`, or malformed `safeguarding`; `Store.require_safety_clear` raises `GateError` on all missing/malformed/non-boolean safety states; and `SqlStore` loads `resident_preview_fixture.build` cleanly.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Add fail-closed `validate_authorised_works_exception` and deterministic `now` clock support in `resident_decisions.py`

#### Context

`BRD BG-005` measures "Work started without valid agreement or authorised exception" (target `Zero`), governed by `RULE-002` (`AC-004`: dated, source-identified, owned, reviewable rules), `FR-008` (`AC-011`: scope/design change invalidates approvals), `FR-011` (`AC-015`: consultation, silence, appointment access, or survey access is never consent), and `FR-014` (`AC-018`: work cannot start or restart until an authorised human records the decision and the resident is notified). Critique `PC-003` also identified that `"authorised_works_exceptions"` must be registered in `RESIDENT_FIELDS` for retention deletion, reject memory/sensor references, and thread optional `*, now: str | None = None` through `resident_gate` and `_resident_decision_gate`.

#### Intent

Provide an explicit, deterministic, fail-closed `validate_authorised_works_exception(case, measure, context, *, now=None)` function in `resident_decisions.py`, register `"authorised_works_exceptions"` in `RESIDENT_FIELDS`, thread optional `*, now=None` into `resident_gate` and `_resident_decision_gate`, and allow `_resident_decision_gate` to accept a bound measure without `"Accepted"` consent **only** when `validate_authorised_works_exception` returns `permitted=True` and no tenure, retention, or `"Needs human review"` hold is open.

#### Boundaries

* Included:
  * Add `"authorised_works_exceptions"` to `RESIDENT_FIELDS` (`resident_decisions.py:42-44`).
  * Define `AUTHORISED_EXCEPTION_ROLES = frozenset({"Building Safety Liaison", "Retrofit Programme Manager"})` and reuse automated-approver token rejection (`{"ai", "model", "assistant", "system", "auto", "automated", "bot", "llm"}`).
  * `validate_authorised_works_exception(case, measure, context, *, now=None)` inspects `case.get("authorised_works_exceptions")` (must be a `dict` mapping `measure` to a non-empty `list` of `dict`s; otherwise `permitted=False`).
  * Require every field fail-closed:
    * `status == "Authorised"` (exact string; `"Revoked"`, `"Expired"`, `"Draft"`, `"Pending"`, `"Disputed"` all fail).
    * `measure == expected_measure`, `type(context_revision) is int and context_revision == context["revision"]`, and `type(design_version) is int and design_version == context["design_version"]` (`FR-008`: scope or design bump immediately invalidates the exception).
    * Non-blank bounded `reference`, `rule_source` (identifying legal/tenancy/statutory rule basis per `RULE-002`), and `reason`, rejecting memory/sensor references (`k.is_memory_reference(...)` or `k.SENSOR_REF.search(...)`).
    * Named human `approved_by` (non-blank, no automated/AI tokens) and `approved_by_role in AUTHORISED_EXCEPTION_ROLES`.
    * ISO `YYYY-MM-DD` `effective_date` and `review_date` satisfying `effective_date <= check_day < review_date` (`RULE-002` `AC-004`), plus optional timezone-aware ISO-8601 `expires_at` strictly after `now_utc` (accepting either full UTC ISO-8601 or `YYYY-MM-DD` normalized to `YYYY-MM-DDT12:00:00+00:00` in `now`).
    * `resident_notified is True` (`type(...) is bool`) and non-blank bounded `notification_ref` (`FR-014` `AC-018`, also rejecting memory/sensor references).
  * Add optional `*, now=None` to `resident_gate(c, bindings=None, *, now=None)` and `_resident_decision_gate(c, bindings=None, *, now=None)`, forwarding `today=check_day` to `retention_schedule(c, today=check_day)` and `now=now_utc_iso` to `authority_for` and `validate_authorised_works_exception`.
  * In `_resident_decision_gate`: keep `_inventory_managed`, `_home_tenure_recorded`, `retention_schedule(c, today=...)["expired"]`, `require_context(c, binding)`, and `resident_reviews[measure]["status"] == "Needs human review"` unconditional; if `answer` is not `"Accepted"` on `context["revision"]`, check whether `authorised_works_exceptions` has a `permitted=True` latest record for `(measure, context)` before raising `ValueError("A current supplied resident acceptance is needed.")`.
* Excluded: Permitting any exception to bypass `require_safety_clear`, tenure verification, retention expiry, or open `"Needs human review"`.

#### Likely Targets

* `src/core/src/zava_forward/core/resident_decisions.py`: Add `"authorised_works_exceptions"` to `RESIDENT_FIELDS`, implement `validate_authorised_works_exception`, and thread `now` through `resident_gate` / `_resident_decision_gate`.

#### Dependencies

* None.

#### Validation Expectations

* `PYTHONPATH=src:tests python3 -m unittest tests/test_resident_decisions.py -q` passes all existing tests unchanged.

#### Completion Evidence

* `validate_authorised_works_exception` returns structured `{permitted, reason, rule_id, exception}` dicts and `_resident_decision_gate` enforces every fail-closed condition.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Deterministic Exercise-Scenario Safety and Consent Verifier

### Context

Issue `#81` requires deterministic proof across all exercise scenarios in `src/core` that (1) no controlled progression occurs with unresolved safety evidence (`RULE-001` / `FR-008`), and (2) no work starts without a valid active resident agreement or an explicitly authorised exception (`RULE-002` / `FR-011`). Exercise scenarios in `src/core` span constructed workbench seed cases (`ZF-1`..`ZF-5`), `synthetic/resident_preview_fixture.py` (`SYN-C1`..`SYN-C3`), `synthetic/sensor_scenarios.py` (`retrofit_exercise_scenarios()` + damp-risk scenarios), `synthetic/scale_fixture.py` (`CONSENT_STATES`, `REP_STATES`, `open_safety_issue`), and `learning_test_bundles.py` (`BUNDLES`).

### Intent

Create `src/core/src/zava_forward/core/safety_consent_exercise_gate.py` providing `verify_exercise_safety_and_consent_gates` (plus pure case/store inspection helpers) that builds isolated temporary `Store` (and optional `SqlStore`) instances for every exercise scenario suite, inspects static work-order activation invariants, executes every controlled progression and work-start transition against unresolved-safety and missing/invalid-consent/exception states, verifies explicit `GateError` / `GateResult` refusals (`RULE-001` / `FR-008` and `RULE-002` / `FR-011`) and zero state/audit mutation, and aggregates a deterministic verification report.

### Boundaries

* Included: `src/core/src/zava_forward/core/safety_consent_exercise_gate.py` with full type annotations, exercise-only notice (`Unreviewed exercise rule`), built-in scenario suite builders, custom scenario audit entrypoint `verify_store_safety_and_consent_invariants`, and `verify_exercise_safety_and_consent_gates`.
* Excluded:Importing from `src/core/tests/` inside production package `zava_forward.core` (`safety_consent_exercise_gate.py` must construct self-contained synthetic/constructed fixtures using only `zava_forward.core` modules and stdlib so installed `zava-forward-core` has zero test-directory runtime dependency!).

### Likely Targets

* `src/core/src/zava_forward/core/safety_consent_exercise_gate.py`: New deterministic verifier module.

### Dependencies

* P01 (`gates.py`, `store.py`, and `resident_decisions.py` hardening).

### Validation Expectations

* `mypy` and `ruff check` pass cleanly on `safety_consent_exercise_gate.py`; `verify_exercise_safety_and_consent_gates()` runs cleanly in standalone Python without `tests/` on `PYTHONPATH`.

### Completion Evidence

* `verify_exercise_safety_and_consent_gates(use_sql=False)` and `verify_exercise_safety_and_consent_gates(use_sql=True)` both return `passed=True` with `controlled_progressions_with_unresolved_safety == 0` and `work_started_without_agreement_or_exception == 0`.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Implement `src/core/src/zava_forward/core/safety_consent_exercise_gate.py`

#### Context

Production modules under `src/core/src/zava_forward/core/` cannot import `dataset.py` from `src/core/tests/` because `tests/` is not packaged into `zava-forward-core`. Therefore, `safety_consent_exercise_gate.py` must construct the canonical constructed workbench seed (`ZF-1`..`ZF-5` matching `scenario_manifest.SOURCES["fixture"]`) directly alongside importing `zava_forward.core.synthetic.resident_preview_fixture`, `zava_forward.core.synthetic.sensor_scenarios`, `zava_forward.core.synthetic.scale_fixture`, and `zava_forward.core.learning_test_bundles`.

#### Intent

Implement a clean, well-typed, deterministic verifier module with clear rule attribution (`SAFETY_GATE_RULE_ID = "RULE-001; PRD FR-008"`, `CONSENT_GATE_RULE_ID = "RULE-002; BRD FR-011; PRD FR-008"`) covering static state invariants and dynamic transition attempts across all six exercise suites.

#### Boundaries

* Included:
  * Normalize `as_of` (`YYYY-MM-DD` -> `as_of_day` and `as_of_utc = f"{as_of_day}T12:00:00+00:00"`) and pass `on=as_of_day` / `now=as_of_utc` into `gates.booking_gates`, `resident_gate`, and `validate_authorised_works_exception`; omit wall-clock timestamps and temp-directory paths from returned summaries so repeated invocations are structurally equal (`PC-003`).
  * Self-contained constructed workbench fixture builder (`ZF-1`..`ZF-5` matching `tests/dataset.py` `DATA` where `ZF-3` has valid scoped acceptance, plus explicit `ZF-3-LEGACY` with legacy case-wide `decision.status == "Accepted"` and no `measure_decisions`, and initial-seed `contract_authorities` on `Retrofit Programme Manager` so `SqlStore._sync()` preserves delegation; `PC-001`, `PC-004`).
  * Six deterministic verification suites executed inside `verify_exercise_safety_and_consent_gates(*, as_of: str = "2026-11-15", use_sql: bool = False, extra_stores: Sequence[tuple[str, Store]] = ())`:
    1. `constructed_workbench`: Checks static invariants on `ZF-1`..`ZF-5`, verifies `ZF-4` (open P1 `Damp` hazard), repaired-but-unreleased hazard, same-person safety release refusal (`gates.safety_release_gate`), standalone `safeguarding_items` hold, truthy string `released="false"`, malformed legacy `safeguarding="corrupt"`, and `hazards=None` unknown safety state all block every controlled progression (`advance`, `technical_action("signoff_give")`, `issue_work_order`, `reissue_work_order`, `record_wo_appointment("Booked")`, `appointment_control("confirm")`, `complete_work_order`, `correct_work_order`, `accept_quality`, `hand_over_quality`) with `RULE-001` / `FR-008` refusal and unchanged case/work-order/audit state while allowing `refer_hazard` (`FR-002`); and verifies `ZF-1` (`Waiting`), `ZF-2` (`Waiting`), and `ZF-3-LEGACY` (legacy case-wide `Accepted` without scoped `measure_decisions`) block work-order issuance, appointment activation (`Appointed`), and booking (`advance`) with `RULE-002` / `FR-011` consent refusal while `ZF-3` (valid scoped acceptance and clear safety) serves as the positive control.
    2. `resident_preview`: Materializes `resident_preview_fixture.build(preview_dir)` and opens `Store` or `SqlStore` with `docs_dir=str(preview_dir / "docs")` (`PC-001`), checks static work-order activation invariants (`SYN-C1` `Appointed` has valid active agreement and clear safety; `SYN-C2` is `Issued` unbooked with valid agreement; `SYN-C3` has zero work orders and zero `returns` `advance` events), verifies `SYN-C3` blocks all controlled progressions and work-start attempts on both safety (`RULE-001`) and consent (`RULE-002` / `FR-011`), verifies `SYN-C2`'s `Attend`-only representative `SYN-REP-B` cannot record installation consent, and verifies withdrawing/pausing consent or raising a hazard on `SYN-C1` immediately blocks completion and progression.
    3. `sensor_retrofit`: Loads `sensor_scenarios.generate(seed=sensor_scenarios.SEED)` (`C01`..`C07` damp scenarios, `SEED = 190`) and `sensor_scenarios.retrofit_exercise_scenarios(seed=sensor_scenarios.SEED)` (`C08`..`C11` retrofit scenarios) (`PC-004`) projected into `Store`/`SqlStore` home cases, verifying damp `REVIEW_CANDIDATE` (`C02`..`C04`) and `INSUFFICIENT` (`C05`..`C06`) hazard cases block all controlled progressions, sensor-derived repair evidence is rejected for safety hold release (`RULE-001`), and retrofit scenario homes (`C08`..`C11`) without valid resident agreement cannot start work (`RULE-002` / `FR-011`).
    4. `scale_matrix`: Builds the deterministic `15`-case Cartesian product of `open_safety_issue in (True, False)` and `scale_fixture.CONSENT_STATES` (`Not requested`, `Pending`, `Given`, `Declined`, `Withdrawn`) with `scale_fixture.REP_STATES` (`None recorded`, `Claimed - unverified`, `Authorised - evidence on file`) plus seeded `scale_fixture.homes` / `scale_fixture.households` samples, proving that every `open_safety_issue=True` case blocks progression even when consent is `Given`, and every non-`Given` or `Claimed - unverified` representative case blocks work start (`issue_work_order`, `appointment_control` -> `Appointed`, `record_wo_appointment("Booked")`, `advance`).
    5. `authorised_exception_controls`: Exercises `validate_authorised_works_exception` and work-start transitions across: (a) a valid human-approved (`Building Safety Liaison`), resident-notified, dated, current-scope `Authorised` exception (permitted when safety is clear), vs (b) invalid exceptions (AI/automated approver, unauthorized role, `resident_notified=False`, blank `notification_ref`, memory/sensor reference, expired `review_date`, expired `expires_at`, `Revoked` status, design-version bump `FR-008`, and concurrent open safety hazard `RULE-001` which must still block!).
    6. `learning_bundles`: Evaluates `learning_test_bundles.run_report` across `story-once`, `pre-visit-pack`, and `change-impact` (`representative_data_retained=False`, `o16_counted_under="change-impact"` when `"O16"` is in `bundle.atlas_ids` else `None`) (`PC-004`), verifying `report["stop"] is False` and `report["breaches"] == []` on clean exercise runs and immediate `report["stop"] is True` when `authority_or_consent_breaches > 0`, `offers_misread_as_commitments > 0`, or `approvals_wrongly_carried_over > 0`.
  * Also expose `verify_store_safety_and_consent_invariants(store: Store, *, suite_name: str = "custom", as_of: str = "2026-11-15")` (`PC-005`) checking: (1) every non-withdrawn work order (`"Issued"`, `"Appointed"`, `"Completed"`) has explicit `resident_bindings` passing `resident_gate(..., now=as_of_utc)` and every `"Appointed"`/`"Completed"` work order has clear safety (`_open_safety_items == []`), (2) any recorded `returns` `"advance"` event or accepted/handed-over quality checklist on a case with unresolved safety evidence or unmet resident gate is flagged as a violation (avoiding false positives on static display stage labels like `SYN-C3` that have zero work orders and zero `returns` events), and (3) isolated deep-copied dynamic transition probes verify runtime `GateError` refusal on every store case with unresolved safety evidence or missing agreement/exception.
* Excluded: Modifying any user data file outside `tempfile.TemporaryDirectory()`.

#### Likely Targets

* `src/core/src/zava_forward/core/safety_consent_exercise_gate.py`: Create module.

#### Dependencies

* P01-T01, P01-T02.

#### Validation Expectations

* Running `PYTHONPATH=src python3 -c "from zava_forward.core.safety_consent_exercise_gate import verify_exercise_safety_and_consent_gates; r = verify_exercise_safety_and_consent_gates(); assert r['passed']"` inside `src/core` succeeds with zero dependency on `src/core/tests`.

#### Completion Evidence

* Module created, typed cleanly under `mypy`, formatted/linted cleanly under `ruff check`, and returning deterministic structured reports.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Verification Suite, Core Documentation, and Focused Validation

### Context

Caller requirements 3, 4, and 5 require a dedicated test `src/core/tests/test_safety_consent_exercise_scenarios_81.py`, documentation in `src/core/README.md`, and clean `ruff check`, `mypy`, and `unittest` execution in `src/core`.

### Intent

Add focused, high-signal unit/integration tests proving both `#81` exercise-scenario invariants and verifier tamper-detection across `Store` and `SqlStore`, document the capability in `src/core/README.md`, and run all `src/core` checks.

### Boundaries

* Included: `src/core/tests/test_safety_consent_exercise_scenarios_81.py`, `src/core/README.md`, and local `src/core` validation commands.
* Excluded: Modifying unrelated test modules or claiming live operational compliance.

### Likely Targets

* `src/core/tests/test_safety_consent_exercise_scenarios_81.py`: New test module.
* `src/core/README.md`: New top-level reference section documenting `#81` exercise-scenario safety and consent gate verification.

### Dependencies

* P01, P02.

### Validation Expectations

* `python3 -m ruff check`, `python3 -m mypy`, and `PYTHONPATH=src:tests python3 -m unittest discover -s tests -q` all exit `0` in `src/core`.

### Completion Evidence

* Passing test output, zero lint/type errors, and clean Markdown/link review in `src/core/README.md`.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Add `src/core/tests/test_safety_consent_exercise_scenarios_81.py`

#### Context

Tests should verify behavior introduced by this slice—both `#81` invariants across all exercise suites, JSON + SQLite parity, `dataset.DATA` parity, fail-closed edge cases from Wave 3, and negative tamper-detection proving the verifier catches violations if introduced.

#### Intent

Create `src/core/tests/test_safety_consent_exercise_scenarios_81.py` with focused test cases that would fail if any safety or consent gate regressed or if the verifier failed to inspect a scenario suite.

#### Boundaries

* Included:
  * Full exercise-suite verification on JSON `Store` and SQLite `SqlStore` (`controlled_progressions_with_unresolved_safety == 0`, `work_started_without_agreement_or_exception == 0`, all 6 suites present and passing, deterministic across repeated runs, and zero dependency on `tests/` imports inside the core module).
  * Direct verification against `tests/dataset.py` `DATA` (`ZF-1`..`ZF-5`) via `extra_stores` / `verify_store_safety_and_consent_invariants`.
  * Fail-closed safety hardening tests: standalone `safeguarding_items` open/malformed, truthy string `released="false"`, and malformed legacy `safeguarding="corrupt"` in `gates.booking_gates` and `Store.require_safety_clear`, missing/`None`/corrupt `hazards` in `Store.require_safety_clear`, repaired-but-unreleased hazard refusal, same-person release refusal, and independent `Building Safety Liaison` release restoring progression only when consent is also valid.
  * Fail-closed consent & authorised-exception tests: consultation/contact note, silence, survey/appointment offer, legacy case-wide `Accepted` without `measure_decisions`, `Attend`-only representative, expired representative window, design-version bump (`FR-008`), paused/withdrawn consent requiring human review, `RESIDENT_FIELDS` retention deletion of `authorised_works_exceptions`, valid human-authorised resident-notified exception allowing work start when safety is clear, and invalid exceptions (AI approver, wrong role, unnotified resident, memory/sensor reference, expired review window, revoked status, design drift, or concurrent open safety hold) all blocked with zero state/audit mutation.
  * Verifier tamper-detection test: injecting an unconsented `Issued`/`Appointed`/`Completed` work order, an `Appointed`/`Completed` work order on a case with unresolved safety evidence, or a `returns` `advance` event on an unsafe case into `verify_store_safety_and_consent_invariants` flips `passed` to `False` and increments `controlled_progressions_with_unresolved_safety` / `work_started_without_agreement_or_exception`.
* Excluded: Redundant restatements of trivial constants.

#### Likely Targets

* `src/core/tests/test_safety_consent_exercise_scenarios_81.py`: Create test file.

#### Dependencies

* P01, P02.

#### Validation Expectations

* `PYTHONPATH=src:tests python3 -m unittest tests/test_safety_consent_exercise_scenarios_81.py -v` passes all tests.

#### Completion Evidence

* Passing targeted and full `src/core` unit test runs.

#### Unresolved Items

* None.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Document verifier in `src/core/README.md` and run `src/core` validation

#### Context

Repository instructions require updating directly related component documentation (`src/core/README.md`), using `*` for unordered lists, avoiding em dashes and bolded-prefix list items, preserving honest synthetic/offline boundaries, and matching `.github/workflows/src-ci.yml` locally in `src/core`.

#### Intent

Add a concise section (`## Exercise-scenario safety and resident consent gate verification (2026-11-15, Refs #81)`) to `src/core/README.md` and run `ruff check`, `mypy`, and full `unittest` discovery in `src/core`.

#### Boundaries

* Included: `src/core/README.md` documentation update and `src/core` lint, typecheck, and unit-test verification.
* Excluded: Touching `docs/reference/` unless knowledge-base files change (none needed for this bounded `src/core` deliverable).

#### Likely Targets

* `src/core/README.md`: Add section describing `safety_consent_exercise_gate`, `verify_exercise_safety_and_consent_gates`, `verify_store_safety_and_consent_invariants`, `validate_authorised_works_exception`, and offline synthetic-exercise evidence limits.

#### Dependencies

* P03-T01.

#### Validation Expectations

* From `src/core`:
  * `python3 -m ruff check`
  * `python3 -m mypy`
  * `PYTHONPATH=src:tests python3 -m unittest discover -s tests -q`

#### Completion Evidence

* Zero `ruff` findings, zero `mypy` errors, all `src/core` unit tests passing, and Markdown style verified in `git diff`.

#### Unresolved Items

* None.
