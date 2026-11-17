<!-- markdownlint-disable-file -->
# RPI Phase Details: Journey Learning-Test Bundles and Role-Screen Scenario Verification (Issue #129)

## Metadata

* Task ID: issue-129-learning-test-bundles-0023
* Task slug: learning-test-bundles-129
* Related plan: .copilot-tracking/plans/2026-11-15/learning-test-bundles-129-plan.md
* Evidence sources: .copilot-tracking/research/2026-11-15/learning-test-bundles-129-research.md, docs/reference/research/ux/journey-learning-test-bundles.md, docs/prds/zava-forward-retrofit-programme-demonstrator.md, docs/adrs/0003-journey-derived-capabilities-runtime-fit.md

## Phase Index

| Phase ID | Name                                                               | Status   | Detail sections          |
|----------|--------------------------------------------------------------------|----------|--------------------------|
| P01      | Core Protocol Metadata Enrichment and Five-Bundle Unit Coverage    | Complete | P01, P01-T01, P01-T02    |
| P02      | Specialist Role-Screen and Aftercare Bundle Scenario Verification  | Complete | P02, P02-T01             |
| P03      | Focused Validation, Implementation Reconciliation, and Commit Readiness | Complete | P03, P03-T01, P03-T02    |

<!-- rpi:phase id=P01 -->
## P01: Core Protocol Metadata Enrichment and Five-Bundle Unit Coverage

### Context

`src/core/src/zava_forward/core/learning_test_bundles.py` already scores constructed two-arm net-effort inputs across all five candidate bundles (`story-once`, `pre-visit-pack`, `change-impact`, `handover-aftercare`, `funding-evidence`) and enforces `OUT_OF_SCOPE = frozenset({"O10", "O18", "O19", "O20"})`, `representative_data_retained is False`, and `O16` single-bundle accounting (`C4`). However, `Bundle` currently carries only `(key, atlas_ids, comparator, zero_measures)`, leaving canonical PRD/protocol fields (`title`, `linked_requirements`, `learning_question`, `beyond_effort_measures`, `stop_rule`) implicit in prose (`C1`, `C2`), and `src/core/tests/test_learning_test_bundles.py` omitted `"funding-evidence"` from its AC1 comparator/zero-measure check (`C5`, `C12`).

### Intent

Expose complete, immutable protocol metadata for all five bundles in `learning_test_bundles.py` without breaking existing CLI or Python callers, and verify all five bundles and NFR-009 invariants in `src/core/tests/test_learning_test_bundles.py`.

### Boundaries

* Included: `src/core/src/zava_forward/core/learning_test_bundles.py`, `src/core/README.md`, `src/core/tests/test_learning_test_bundles.py`.
* Excluded: Changing hyphenated bundle keys, altering `zero_measures` or `learning-bundle-constructed-input-v1` stdin schema keys, adding persistence/file I/O, or touching `O10`/`O18`-`O20`.

### Likely Targets

* `src/core/src/zava_forward/core/learning_test_bundles.py`: Extend `Bundle` dataclass and `compare_bundle` return payload with additive protocol metadata.
* `src/core/README.md`: Update the `learning_test_bundles` section if needed to note the protocol metadata exposed on `BUNDLES` and `compare_bundle`.
* `src/core/tests/test_learning_test_bundles.py`: Extend AC1 check to all 5 bundles and add protocol-metadata, NFR-009 resident-effort shift, all-6-zero-measure breach, and 5-bundle reconciled campaign tests.

### Dependencies

* None.

### Validation Expectations

* From `src/core`: `python3 -m ruff check .`, `python3 -m ruff format --check .`, `python3 -m mypy`, and `PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_learning_test_bundles.py' -v`.

### Completion Evidence

* All existing and new tests in `test_learning_test_bundles.py` pass with zero lint or strict-mypy issues.

### Unresolved Items

* None.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add backward-compatible protocol metadata to `learning_test_bundles.py` and update `src/core/README.md`

#### Context

`_validate_input` in `learning_test_bundles.py` validates `counts` against `bundle.zero_measures`, and `ConstructedReportCommand` tests compare `render_report(run_report(envelope(key)))` against CLI stdout (`C4`, `C5`). Adding defaulted fields after `zero_measures` on `Bundle` and adding metadata keys to `compare_bundle` keeps `zero_measures`, `_validate_input`, and `render_report` 100% compatible.

#### Intent

Populate exact PRD and `journey-learning-test-bundles.md` metadata for all five bundles on `Bundle` and `compare_bundle`:

1. `story-once`:
   * `title`: `"Story once and promise ownership"`
   * `atlas_ids`: `("O01", "O02", "O03", "O15")`
   * `linked_requirements`: `("FR-045", "FR-048", "AC-062", "AC-064", "GOAL-004")`
   * `comparator`: `"Manual re-asking and chase log"`
   * `zero_measures`: `("authority_or_consent_breaches", "promises_without_owner")`
   * `learning_question`: `"Does a scoped, corrected account cut repeat explanations without blurring authority?"`
   * `beyond_effort_measures`: `("repeat_ask_count", "promises_without_owner", "authority_or_consent_breaches")`
   * `stop_rule`: `"Stop if representative or consent boundaries blur"`
2. `pre-visit-pack`:
   * `title`: `"Pre-visit pack and readiness rehearsal"`
   * `atlas_ids`: `("O06", "O08", "O09")`
   * `linked_requirements`: `("FR-048", "FR-049", "AC-062", "AC-063", "AC-065")`
   * `comparator`: `"Current visit preparation"`
   * `zero_measures`: `("offers_misread_as_commitments",)`
   * `learning_question`: `"Does a cited pre-visit pack reduce missing facts and abortive visits?"`
   * `beyond_effort_measures`: `("missing_fact_count_at_visit", "offers_misread_as_commitments")`
   * `stop_rule`: `"Stop if an offer reads as a commitment"`
3. `change-impact`:
   * `title`: `"Change impact and evidence reuse"`
   * `atlas_ids`: `("O07", "O16")`
   * `linked_requirements`: `("FR-008", "FR-043", "AC-011", "AC-013", "AC-051")`
   * `comparator`: `"Manual dependency check"`
   * `zero_measures`: `("approvals_wrongly_carried_over",)`
   * `learning_question`: `"Does a dependency check catch stale evidence that a manual check misses?"`
   * `beyond_effort_measures`: `("stale_items_escaped", "approvals_wrongly_carried_over")`
   * `stop_rule`: `"Stop if reuse transfers an approval"`
4. `handover-aftercare`:
   * `title`: `"Accessible handover and aftercare"`
   * `atlas_ids`: `("O13", "O14")`
   * `linked_requirements`: `("FR-049", "FR-014", "AC-063")`
   * `comparator`: `"Paper handover"`
   * `zero_measures`: `("open_remedies_hidden",)`
   * `learning_question`: `"Can the resident use the handover material, and are open remedies still visible after it?"`
   * `beyond_effort_measures`: `("accessibility_defects_found", "open_remedies_hidden")`
   * `stop_rule`: `"Stop if handover closes an open remedy"`
5. `funding-evidence`:
   * `title`: `"Review-ready funding evidence"`
   * `atlas_ids`: `("O16", "O17")`
   * `linked_requirements`: `("FR-019", "FR-042", "AC-050")`
   * `comparator`: `"Manual evidence pack"`
   * `zero_measures`: `("inferred_submissions",)`
   * `learning_question`: `"Does the pack reduce reviewer return requests without implying submission or award?"`
   * `beyond_effort_measures`: `("reviewer_returns", "unsupported_statements", "inferred_submissions")`
   * `stop_rule`: `"Stop if a submission or award is inferred"`

#### Boundaries

* Included: `Bundle` fields with defaults, `BUNDLES` entries, `compare_bundle` metadata keys (`bundle_title`, `atlas_ids`, `linked_requirements`, `learning_question`, `beyond_effort_measures`, `stop_rule`), and concise `src/core/README.md` update.
* Excluded: Changing `render_report` lines or `SCHEMA_VERSION = "learning-bundle-constructed-input-v1"`.

#### Likely Targets

* `src/core/src/zava_forward/core/learning_test_bundles.py`
* `src/core/README.md`

#### Dependencies

* None.

#### Validation Expectations

* `python3 -m mypy` and `python3 -m ruff check .` in `src/core`.

#### Completion Evidence

* `compare_bundle` returns exact metadata for all 5 bundles while all 22 pre-existing tests still pass unchanged.

#### Unresolved Items

* None.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Expand `src/core/tests/test_learning_test_bundles.py` for full five-bundle, NFR-009, and target-zero parity

#### Context

`test_ac1_bundles_each_have_a_non_ai_comparator_and_zero_measure` currently tests only 4 keys (`C5`, `C12`). We also want direct unit proof of the NFR-009 resident-effort transfer rule (`docs/reference/research/ux/journey-learning-test-bundles.md:69-70`), every target-zero breach across all 6 target-zero measures across the 5 bundles, and a full 5-bundle constructed run campaign reconciled with `reconcile_o16`.

#### Intent

Update `test_ac1_bundles_each_have_a_non_ai_comparator_and_zero_measure` to cover all 5 bundle keys (including `"funding-evidence"`), and add focused tests verifying:
1. Canonical PRD/protocol alignment (`title`, `atlas_ids`, `linked_requirements`, `learning_question`, `beyond_effort_measures` superset of `zero_measures`, `stop_rule`) across all 5 bundles.
2. Resident-effort transfer invariant (`NFR-009`): shifting staff minutes (`preparation`/`coordination`) onto `resident_effort` or `support_cost` yields `"comparator lower or equal"` rather than a false workflow saving.
3. Target-zero breach activation on each individual `zero_measure` across all 5 bundles (including both `"authority_or_consent_breaches"` and `"promises_without_owner"` in `story-once`) in both `"comparator"` and `"workflow"` arms, with `"STOP:"` rendered ahead of effort medians.
4. Full 5-bundle `run_report` + `reconcile_o16` campaign confirming consistent single-bundle `O16` attribution across `change-impact` and `funding-evidence` while rejecting retained representative data.

#### Boundaries

* Included: `src/core/tests/test_learning_test_bundles.py`.
* Excluded: Modifying unrelated `src/core/tests/` files.

#### Likely Targets

* `src/core/tests/test_learning_test_bundles.py`

#### Dependencies

* P01-T01.

#### Validation Expectations

* Subprocess and in-process tests in `test_learning_test_bundles.py` pass under `PYTHONPATH=$(pwd)/src:$(pwd)/tests python3 -m unittest discover -s tests -p 'test_learning_test_bundles.py' -v` from `src/core`.

#### Completion Evidence

* Passing test output from `test_learning_test_bundles.py` plus clean `ruff` and `mypy`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P02 -->
## P02: Specialist Role-Screen and Aftercare Bundle Scenario Verification

### Context

Specialist role screens in `src/api/src/zava_forward/api/web/role-screens.js` and accessible aftercare views in `src/api/src/zava_forward/api/web/aftercare.js` implement the deterministic plain-language reader and staff-assisted surfaces whose boundaries correspond to the five learning-test bundles (`C6`, `C7`), while `docs/reference/research/ux/journey-learning-test-bundles.md:102-103` keeps direct bundle-runner screen wiring and run-record storage gated on Atlas-owner and DPO decisions (`C1`). Adding a dedicated cross-layer scenario test module in `src/api/tests/` proves that the live workbench screens and `AftercareService` uphold every bundle's stop-rule boundary and pair cleanly with two-arm `learning_test_bundles` scoring without violating the screen/storage gate.

### Intent

Create `src/api/tests/test_learning_test_bundle_scenarios.py` executing real Node-VM renders of `role-screens.js` and `aftercare.js` alongside `AftercareService` and `zava_forward.core.learning_test_bundles` for all five candidate bundles.

### Boundaries

* Included: `src/api/tests/test_learning_test_bundle_scenarios.py`.
* Excluded: Editing `role-screens.js`, `aftercare.js`, `style.css`, or `server.py` (preserving pinned table counts in `test_accessibility_baseline.py`, closed route inventory in `test_role_endpoint_inventory.py`, and the protocol's screen-wiring gate).

### Likely Targets

* `src/api/tests/test_learning_test_bundle_scenarios.py`: New focused scenario verification module.

### Dependencies

* P01-T01.

### Validation Expectations

* From `src/api`: `python3 -m ruff check .`, `python3 -m ruff format --check .`, `python3 -m mypy`, and `PYTHONPATH=src:tests:../core/src:../core/tests:../agents/src:../agents/tests python3 -m unittest discover -s tests -p 'test_learning_test_bundle_scenarios.py' -v` plus existing conformance suites.

### Completion Evidence

* All scenario tests pass in Node VM and Python, and `mypy --strict` passes in `src/api`.

### Unresolved Items

* None.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Create `src/api/tests/test_learning_test_bundle_scenarios.py` covering Bundles 1-5 and governance boundaries

#### Context

In `src/api`, `mypy` runs with `strict = true` and `follow_imports = "skip"` for `zava_forward.core.*`. Every test helper in `test_learning_test_bundle_scenarios.py` must therefore explicitly type its inputs and outputs (`dict[str, Any]`, `list[dict[str, Any]]`, `str`, `None`) and cast or bind `Any` results into typed locals before returning.

#### Intent

Implement focused scenario tests in `src/api/tests/test_learning_test_bundle_scenarios.py`:
1. **`test_bundle_1_story_once_and_promise_ownership_across_role_screens` (`story-once` / `O01, O02, O03, O15`):**
   * Renders `resident-choice`, `resident-service-issues`, and `programme-queue` for one home (`ZF-129`) in Node VM, plus `aftercareScreens.receiptView` for a representative-raised concern with explicit `representative_basis`.
   * Verifies measure-specific choice (`"Contact or access is never read as a yes"`, `"Generic consent is not accepted"`), separate `Chase owner` vs `Resident-update owner` and named update-commitment owner, and representative basis visibility; scores clean and stop-triggered (`authority_or_consent_breaches` / `promises_without_owner`) constructed two-arm runs via `learning_test_bundles.run_report`.
2. **`test_bundle_2_pre_visit_pack_and_readiness_rehearsal_across_role_screens` (`pre-visit-pack` / `O06, O08, O09`):**
   * Renders `procurement-packages`, `resident-choice`, and `contractor-job-pack` on home `ZF-129`.
   * Verifies `"Offered capacity is not a booking and not a promise to any resident"`, Stage 4 `"An offer is not a booking."`, resident choice/pause precedence over offered slots, and contractor `Needs notice` without leaking private household reasons; scores constructed two-arm `pre-visit-pack` runs (clean vs `offers_misread_as_commitments` stop).
3. **`test_bundle_3_change_impact_and_evidence_reuse_across_role_screens` (`change-impact` / `O07, O16`):**
   * Renders `technical-queue` (with a scoped design change moving `building` sign-off to `"Needs reassessment"` while keeping unaffected `assessment` signed off on its stated version) and `finance-funding` (with `dependency_impact.approvals` requiring re-review and `stale_fields` / `proposal_freshness` flagged).
   * Verifies readiness stays blocked and approvals are never carried over on reuse; scores constructed two-arm `change-impact` runs with `o16_counted_under="change-impact"` (clean vs `approvals_wrongly_carried_over` stop).
4. **`test_bundle_4_accessible_handover_and_aftercare_keeps_open_remedies_visible` (`handover-aftercare` / `O13, O14` — Bundle 5 in caller prompt / 4th row in PRD table):**
   * Renders `quality-queue` (returned defect blocking handover readiness, non-colour prefixes `"Action needed:"` / `"Open: awaiting a fix by the defect owner"`), `programme-queue` Stage 7 (`"7. Handover and live with measures"` -> `"Open remedies are not closed by handover."`), `resident-choice` (accessible jump links `a[data-jump]`, word-first state cues), and `aftercareScreens.evaluatorView` over a real `AftercareService` temporary store where a home has an unresolved concern alongside recorded `handover` and `financial` closures (`unresolved_with_handover_or_financial_closure == 1`).
   * Verifies handover and financial closure never hide or close open remedies or aftercare concerns, and scores both workflow-lower and comparator-lower (`Paper handover` first-class outcome) plus `open_remedies_hidden` stop-rule scenarios.
5. **`test_bundle_5_review_ready_funding_evidence_and_o16_reconciliation` (`funding-evidence` / `O16, O17`):**
   * Renders `finance-funding` and `finance-invoices` on home `ZF-129`.
   * Verifies Held unreviewed export copy (`"Not submitted; eligibility Not assessed"`, `"Submission, award and payment"` -> `"Not recorded here. This screen never infers them."`), Stage 8 `"No award is inferred from an invoice."`, AI-unavailable manual continuity (`"Finance decisions and invoice checks work the same when AI is unavailable"`), capacity-not-cash boundary, and cross-bundle `reconcile_o16` with `change-impact`.
6. **`test_protocol_screen_wiring_and_run_storage_remain_gated`:**
   * Inspects `role-screens.js` registered screen IDs and `server.py` route registrations to confirm no unratified learning-bundle runner screen or stored run-record endpoint is exposed while Atlas-owner confirmation and DPO retention remain open, and verifies `OUT_OF_SCOPE` (`O10`, `O18`-`O20`) appears in zero bundle definitions.

#### Boundaries

* Included: `src/api/tests/test_learning_test_bundle_scenarios.py`.
* Excluded: Network calls, browser launches, or reading `~/.zava-forward`.

#### Likely Targets

* `src/api/tests/test_learning_test_bundle_scenarios.py`

#### Dependencies

* P01-T01.

#### Validation Expectations

* `ruff check .`, `ruff format --check .`, `mypy`, and `unittest` discovery on `test_learning_test_bundle_scenarios.py` in `src/api`.

#### Completion Evidence

* Passing test execution across all six scenario/governance tests in `test_learning_test_bundle_scenarios.py`.

#### Unresolved Items

* None.

<!-- rpi:phase id=P03 -->
## P03: Focused Validation, Implementation Reconciliation, and Commit Readiness

### Context

Validation follows the focused tier (owner decision D4 / #1294). After implementation, `rpi-implement` reconciles `.copilot-tracking/changes/2026-11-15/learning-test-bundles-129-changes.md`, plan markers, and repository-local noreply Git author identity before Review freeze; `rpi-review` then executes one read-only post-implementation review to `.copilot-tracking/reviews/logs/2026-11-15/learning-test-bundles-129-review.md`, state transitions to `Follow-up` (`status: "completed"`, `session_status: "running"`), and the automatic RPI parent commits all changes locally on `feat/ux-129-learning-test-bundles-0023` without pushing.

### Intent

Verify zero regressions across core and API linters, typecheckers, unit tests, and UX/role-screen guardrails, finalize implementation reconciliation, and configure privacy-safe local commit readiness prior to `rpi-review` and final branch freeze.

### Boundaries

* Included: Local focused validation commands, `.copilot-tracking/` implementation reconciliation for `2026-11-15`, and repository-local `git config --local user.email` (`8036360+jmservera@users.noreply.github.com`) for the post-Review local commit with `Refs #129` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`.
* Excluded: `git push`, `gh pr create`, or editing `main`.

### Likely Targets

* `.copilot-tracking/changes/2026-11-15/learning-test-bundles-129-changes.md`
* `.copilot-tracking/plans/2026-11-15/learning-test-bundles-129-plan.md`
* `.copilot-tracking/details/2026-11-15/learning-test-bundles-129-phase-details.md`
* `.copilot-tracking/rpi-sessions/2026-11-15/learning-test-bundles-129-state.json`

### Dependencies

* P01, P02.

### Validation Expectations

* `src/core`: `ruff check .`, `ruff format --check .`, `mypy`, `test_learning_test_bundles.py`, `test_atlas_screen_trace.py`, `test_live_doc_links.py`.
* `src/api`: `ruff check .`, `ruff format --check .`, `mypy`, `test_learning_test_bundle_scenarios.py`, `test_role_screens.py`, `test_role_screens_conformance.py`, `test_role_screens_connected_journey.py`, `test_technical_quality_screens.py`, `test_accessibility_baseline.py`, `test_content_standard.py`, `test_epic149_ux_journey_requirement_traceability.py`, `test_aftercare_screen.py`.
* Tracking hygiene check: `grep` confirming zero `.copilot-tracking/` occurrences in touched `src/` files.

### Completion Evidence

* Reconciled `learning-test-bundles-129-changes.md`, all `P01`-`P03` markers complete, and verified `git config --local user.email` (`8036360+jmservera@users.noreply.github.com`) ready for the post-Review frozen local commit on `feat/ux-129-learning-test-bundles-0023`.

### Unresolved Items

* None.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Run focused linters, strict typechecks, and unit/guardrail test suites in `src/core` and `src/api`

#### Context

Both `src/core` and `src/api` enforce `ruff` (`line-length = 100`, `select = ["E", "F", "I", "B", "UP"]`) and `mypy` (`strict = true`).

#### Intent

Run all targeted linters, format checks, typechecks, and unit/guardrail suites and verify Markdown relative links in `src/core/README.md` and `docs/reference/research/ux/journey-learning-test-bundles.md`.

#### Boundaries

* Included: Read-only validation execution across `src/core` and `src/api`.
* Excluded: Blanket cloud/SQL/Playwright full-tier gate runs not required by focused tier.

#### Likely Targets

* `src/core/` and `src/api/` validation runners.

#### Dependencies

* P01-T02, P02-T01.

#### Validation Expectations

* Exit code `0` on every lint, typecheck, and unit-test command.

#### Completion Evidence

* Recorded command outputs and counts in `.copilot-tracking/changes/2026-11-15/learning-test-bundles-129-changes.md`.

#### Unresolved Items

* None.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Reconcile RPI implementation records and configure local noreply commit readiness

#### Context

Repository instructions require resolving the authenticated GitHub user with `gh api user`, configuring repository-local `user.email` as `{id}+{login}@users.noreply.github.com`, citing `Refs #129` (not `Closes #129`), including `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, and keeping `.copilot-tracking/` paths out of production code, docstrings, comments, and commit messages. Because `rpi-review` is read-only with respect to plan, phase details, and changes artifacts, implementation reconciliation completes prior to entering `Review`, and the automatic RPI parent creates the final frozen local commit once `Review` and `Follow-up` state persistence complete.

#### Intent

Reconcile plan task checkboxes, phase-details statuses, and `.copilot-tracking/changes/2026-11-15/learning-test-bundles-129-changes.md`, and configure repository-local noreply `user.email` via `gh api user` before handing off to `rpi-review`.

#### Boundaries

* Included: Tracking reconciliation and local git author email setup (`8036360+jmservera@users.noreply.github.com`).
* Excluded: Any remote git/GitHub write (`git push`, `gh pr`) and post-Review mutation of implementation/planning artifacts.

#### Likely Targets

* `.copilot-tracking/plans/2026-11-15/learning-test-bundles-129-plan.md`
* `.copilot-tracking/details/2026-11-15/learning-test-bundles-129-phase-details.md`
* `.copilot-tracking/changes/2026-11-15/learning-test-bundles-129-changes.md`
* `.copilot-tracking/rpi-sessions/2026-11-15/learning-test-bundles-129-state.json`

#### Dependencies

* P03-T01.

#### Validation Expectations

* `git config --local --get user.email` returns `8036360+jmservera@users.noreply.github.com`; all plan and phase-detail markers reconcile cleanly with `learning-test-bundles-129-changes.md`.

#### Completion Evidence

* Recorded commit SHA and clean working tree verification.

#### Unresolved Items

* None.
