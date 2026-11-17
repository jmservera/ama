<!-- markdownlint-disable-file -->
# Review: Issue #133 Aftercare Concern Route and Lived-Performance Review

## Scope and Evidence

* Task ID: aftercare-133-2346
* Review date: 2026-11-14
* Review scope: Full task (`P01`–`P04`)
* Assessed boundary: Accessible digital + non-digital concern intake (`phone`, `in_person`, `paper`, `assisted_visit`, `representative`), `"call_back"` support normalization, digital-only `household_receipt` isolation, handover/financial closure immutability and sensor non-dismissal, deterministic neutral-language guard across multiline/paraphrase/staff-evidence/restore surfaces, evaluator `unknown` preservation and `FR-036` AI concern pack proposal-only governance, `aftercare_fixture.py` `sys.modules` safety, tests, and package documentation.
* Plan: .copilot-tracking/plans/2026-11-14/aftercare-133-2346-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/aftercare-133-2346-phase-details.md
* Plan critique: .copilot-tracking/reviews/2026-11-14/aftercare-133-2346-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-14/aftercare-133-2346-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-14/aftercare-133-2346-research.md, `src/core` and `src/api` git diff against `feat/demo-233-same-home-tensions-0825`, static/unit/HTTP validation outputs, and `web-design-guidelines` review.

## Opening Review State

* Interpreted review goal: Verify once with direct repository evidence that `P01`–`P04` satisfy `FR-1`–`FR-4`, `NFR-1`–`NFR-2`, `AC-1`–`AC-5`, all resolved critique items (`PC-001`–`PC-007`), and caller constraints without introducing defects or scope drift.
* Review scope: Full task (`P01`, `P02`, `P03`, `P04`)
* Evidence readiness: Ready; plan, phase details, plan critique, changes log, research artifact, and working-tree diff are reconciled and available.
* Acceptance basis: `FR-1`–`FR-4`, `NFR-1`–`NFR-2`, `AC-1`–`AC-5`, Test Ownership and Verification Lock (`<= 18` net new test methods, zero `sys.modules` eviction), critique dispositions `PC-001`–`PC-007`, and caller validation constraints.
* First comparison boundary: Reconcile plan markers, changes record, and exact git diff across `src/core` and `src/api`.
* Active read-only boundaries: Review writes only `.copilot-tracking/reviews/2026-11-14/aftercare-133-2346-review.md` and RPI session state; source, test, plan, details, critique, and changes files remain read-only during Review.
* Initial blockers: None

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass post-implementation comparison on 2026-11-14 across `.copilot-tracking/plans/2026-11-14/aftercare-133-2346-plan.md`, `.copilot-tracking/details/2026-11-14/aftercare-133-2346-phase-details.md`, `.copilot-tracking/reviews/2026-11-14/aftercare-133-2346-plan-critique.md`, `.copilot-tracking/changes/2026-11-14/aftercare-133-2346-changes.md`, `.copilot-tracking/research/2026-11-14/aftercare-133-2346-research.md`, the 10-file working-tree diff in `src/core` and `src/api`, static/unit/HTTP validation runs, and `web-design-guidelines` verification.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`, `P01-T02`) | `P01: Intake Channel Parity, Receipt Isolation, and Fixture Safety` | Reconciled | Checked `[x]` in plan; changes log and git diff match `aftercare_fixture.py`, `aftercare.py`, and `aftercare_intake.py`. |
| `P02` (`P02-T01`, `P02-T02`) | `P02: Deterministic Causation, Resident-Blame, and Savings-Promise Guard` | Reconciled | Checked `[x]` in plan; changes log and git diff match multiline `strip_unsafe_sentences`, expanded `PARAPHRASE_PATTERNS`, and staff/snapshot `neutral_text` enforcement. |
| `P03` (`P03-T01`, `P03-T02`) | `P03: Evaluator Unknown Preservation, FR-036 Pack Governance, and Accessible Web UI` | Reconciled | Checked `[x]` in plan; changes log and git diff match `FR-036` `ai_registry` metadata and `web/aftercare.js` multi-select, labels, and `Unknown` non-coercion. |
| `P04` (`P04-T01`, `P04-T02`) | `P04: Focused Core and API Tests, Documentation Sync, and Verification` | Reconciled | Checked `[x]` in plan; 14 net new focused test methods (`<= 18` cap), zero removed tests, updated READMEs, and recorded `mypy`/`ruff`/`unittest` results. |
| `Follow-Up Items` | `Follow-Up Items` (`OD-54` resident showcase portal writes; `FR-036` held-out benchmark for live pack drafting) | Reconciled | Kept outside active `Pxx`/`Pxx-Txx` scope and mirrored accurately in changes record. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/core/tests/aftercare_fixture.py` | Replaced `sys.modules.pop` loop with `sys.path` and in-place `__path__` updates on `zava_forward` and `zava_forward.core` to preserve class identity during `unittest discover`. | Zero matches for `sys.modules.pop` or `del sys.modules`; verified by `test_aftercare_fixture_avoids_bulk_sys_modules_deletion`. | `unittest discover -s tests -p "test_aftercare*.py"` (142 tests, `OK`) and 278-test combined `src/core` run (`OK`). | Reconciled (`NFR-1`, `AC-5`). |
| `P01-T02` | `src/core/src/zava_forward/core/aftercare.py`, `src/core/src/zava_forward/core/aftercare_intake.py` | Added `"representative"` to `NON_DIGITAL_CHANNELS`, `ACCESSIBLE_ROUTE`, `HOUSEHOLD_MANUAL_ROUTE`, `CHANNEL_LABELS`, `intake_form()`, and `raise_concern`; added `"multiple": True` on `support_needed`; normalized `"call_back"` -> `"callback_window"`; scoped `household_receipt` to `route == "digital"`. | Verified in diff and covered by `test_representative_non_digital_channel_and_call_back_support_normalization` and `test_household_receipt_rejects_staff_recorded_concern_uniformly`. | `src/core` `mypy` (`0` errors), `ruff` (`0` errors), `unittest` (`OK`). | Reconciled (`FR-1`, `FR-2`, `AC-1`). |
| `P02-T01` | `src/core/src/zava_forward/core/aftercare.py` | Folded intra-paragraph newlines and re-checked joined output in `strip_unsafe_sentences`; expanded `PARAPHRASE_PATTERNS` for occupant/user error/lifestyle/habits, thermostat/ventilation/window/drying-clothes blame, finite causal verbs, scoped `responsible for`, and savings guarantees. | Verified in diff and covered by `test_strip_unsafe_sentences_blocks_multiline_split_clauses` and `test_expanded_guard_blocks_occupant_control_ventilation_causation_and_promises`. | `src/core` `mypy`, `ruff`, `unittest` (`OK`). | Reconciled (`FR-3`, `AC-2`). |
| `P02-T02` | `src/core/src/zava_forward/core/aftercare.py`, `src/core/src/zava_forward/core/aftercare_intake.py` | Enforced `neutral_text` atomically on `record_outcome`, `set_remedy`, `review_pack`, `from_state` (including pack text while exempting `household_statement`), and `AftercareService` (`HTTP 400` `ValidationError` via `NEUTRAL_EVIDENCE_MESSAGE`). | Verified in diff and covered by `test_staff_outcome_remedy_pack_review_and_restore_enforce_neutral_text` and `test_service_rejects_non_neutral_outcome_remedy_and_sensor_notes_with_neutral_400`. | `src/core` `mypy`, `ruff`, `unittest` (`OK`). | Reconciled (`FR-3`, `AC-2`). |
| `P03-T01` | `src/core/src/zava_forward/core/aftercare.py`, `src/core/src/zava_forward/core/aftercare_intake.py` | Bound `FR-036` `ai_registry` metadata (`proposal-pack`, `disabled`, `unapproved`, `live_authorized: False`, `requires_human_review: True`) into `propose_pack` and `evaluator_view` (`concern_pack_task`) via typed `cast(...)` helpers. | Verified in diff and covered by `test_propose_pack_exposes_fr036_ai_registry_proposal_metadata` and `test_evaluator_view_exposes_fr036_concern_pack_governance_and_preserves_unknowns`. | `src/core` `mypy` (`316` files clean) and `unittest` (`OK`). | Reconciled (`FR-4`, `AC-3`). |
| `P03-T02` | `src/api/src/zava_forward/api/web/aftercare.js` | Added channel/support maps, `<select multiple>` rendering and reading, optional form-note and null digital `recorded_by` guards, dynamic `target` submit path, strict `"Unknown"` non-coercion in `aftercareEvaluatorView`, and plain-language `FR-036` notice. | Verified in diff and covered by Node VM assertions, `test_content_standard.py`, `test_list_export_inventory.py`, and `web-design-guidelines` review (`✓ pass`). | `src/api` `mypy` (`283` files clean), `ruff` (`199` files clean), `unittest` (103 focused tests `OK`). | Reconciled (`FR-1`, `FR-4`, `NFR-2`, `AC-3`, `AC-4`). |
| `P04-T01` | `src/core/tests/test_aftercare.py`, `src/core/tests/test_aftercare_intake.py` | Added 10 focused semantic test methods (`6` + `4`) exercising every `P01`–`P03` core contract and regression boundary. | Net new core methods = `10` (within `<= 8` + `<= 5` lock); zero removed tests. | `src/core` `mypy`, `ruff`, and `unittest` (`OK`). | Reconciled (`AC-5`). |
| `P04-T02` | `src/api/tests/test_aftercare_screen.py`, `src/api/tests/test_aftercare_served.py`, `src/core/README.md`, `src/api/README.md` | Added 4 focused API/UI test methods (`3` + `1`, total `14 <= 18` cap) and updated `#133` sections in both package READMEs. | Zero `.copilot-tracking/` references in diff; README descriptions match implemented contracts. | `src/api` `mypy`, `ruff`, and `unittest` (`OK`). | Reconciled (`AC-4`, `AC-5`). |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P02-T02` (`AftercareRegister.record_outcome`) | Validated `neutral_text(_text(evidence, "Outcome evidence"))` before mutating `rec["investigation"] = "outcome_recorded"` so rejected evidence leaves in-memory state unchanged. | Caught during `P04-T01` test execution (`Issue133RefinementTests`); local judgment requiring no user decision. | Recorded in `.copilot-tracking/changes/2026-11-14/aftercare-133-2346-changes.md` (`## Implementation-Time Plan and Detail Updates`). | Not needed (preserves `P02-T02` contract and acceptance criteria). | Reconciled. |
| `P02-T02` (`AftercareService.handle` / `_staff_evidence`) | Introduced import-verified `NEUTRAL_EVIDENCE_MESSAGE` and `_safe_error_text` because `aftercare._NEUTRAL_ERROR` contains the word `"blame"` and would fail `neutral_text(str(exc))` if echoed directly. | Caught by code inspection during `P02-T02`; local judgment requiring no user decision. | Recorded in `.copilot-tracking/changes/2026-11-14/aftercare-133-2346-changes.md` and verified via `HTTP 400` neutral payload assertions. | Not needed (directly fulfills `PC-002` and `P02-T02` neutral `HTTP 400` requirement). | Reconciled. |

## Critique and Material Revision Assessment

* Latest critique dispositions: All seven critique findings (`PC-001` through `PC-007`) recorded in `.copilot-tracking/reviews/2026-11-14/aftercare-133-2346-plan-critique.md` were applied directly in `.copilot-tracking/plans/2026-11-14/aftercare-133-2346-plan.md` and `.copilot-tracking/details/2026-11-14/aftercare-133-2346-phase-details.md` and honored in implementation (`cast(...)` around `ai_registry.get` / `authorizes_live`, real pack snapshot keys with `household_statement` exempted, `HTTP 400` + `GET /api/aftercare/evaluator`, `"multiple": True` + seven exact `SUPPORT_OPTIONS` labels, dynamic `target` POST path + `test_content_standard.py`-clean copy, scoped `responsible for` + `(?:s'|'s|s)?`, updated `raise_concern` channel error + `src/core/README.md`, and `Array.isArray(v.rows)` / `acWhole(totals.concerns_raised)` guards).
* Material revisions: None required during implementation; both implementation-time adjustments were local-judgment refinements preserving approved intent.
* Dependent-work pause assessment: No dependent-work pause was needed; phases executed in plan order `P01` -> `P02` -> `P03` -> `P04`.
* Justification assessment: Supported by direct diff and passing static/unit/HTTP tests.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Resident showcase portal (`resident_demo`) live session write route for aftercare concerns | PRD `OD-54` gates live/authenticated resident portal identity and session persistence; `server.py` remains staff-session gated (`test_role_endpoint_inventory.py`). | Future `OD-54` resident-portal increment owner | Open, distinct follow-up route (kept outside `#133` local scope; commit uses `Refs #133`). |
| Held-out benchmark and release sign-off for `aftercare-concern-pack` live model drafting | PRD `FR-036` keeps `aftercare-concern-pack` `disabled` and `unapproved` in `ai_registry.py` until quality/effort benchmarks and named governance approval exist. | Future `FR-036` AI evaluation and governance owner | Open, distinct follow-up route (kept outside `#133` local scope; proposal-only metadata verified). |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

None within the assessed `#133` task boundary (`FR-1`–`FR-4`, `NFR-1`–`NFR-2`, `AC-1`–`AC-5`).

## Defects

* None

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| None | none | No `rpi-implement`, `rpi-plan`, or `rpi-research` follow-up required for `#133` local scope | All assessed acceptance criteria and verification gates passed |

Later implementation of a routed finding does not require another Review.

## Residual Work

* External issue-level gates outside this task's declared scope remain tracked under `Refs #133`: `OD-54` live resident portal session writes, DPO/assistive-technology formal sign-off, and `FR-036` held-out benchmark approval before enabling live `aftercare-concern-pack` inference.
* Optional engineering-cleanup opportunity (non-defect follow-up): reword `aftercare._NEUTRAL_ERROR` in `src/core/src/zava_forward/core/aftercare.py` so its diagnostic message avoids the banned token `"blame"`, allowing `aftercare_intake._safe_error_text` fallback translation to be simplified once callers/tests asserting on `_NEUTRAL_ERROR` wording are updated together.

## Blockers and Remaining Work

* Blockers: None
* Remaining active work: None

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `python3 -m mypy` | `src/core` (316 source files) | Passed | `Success: no issues found in 316 source files` |
| `python3 -m ruff check . && python3 -m ruff format --check .` | `src/core` (263 files) | Passed | `All checks passed!`, `263 files already formatted` |
| `PYTHONPATH=src:tests python3 -m unittest discover -s tests -p "test_aftercare*.py" -q` | `src/core` (`test_aftercare.py`, `test_aftercare_intake.py`, `test_aftercare_store.py`) | Passed | `Ran 142 tests in 166.213s — OK (skipped=15)` |
| `PYTHONPATH=src:tests python3 -m unittest tests/test_aftercare.py tests/test_aftercare_intake.py tests/test_aftercare_store.py tests/test_quality_procurement.py -q` | `src/core` aftercare + `#87` handover suite | Passed | `Ran 278 tests in 263.391s — OK (skipped=15)` |
| `python3 -m mypy` | `src/api` (283 source files) | Passed | `Success: no issues found in 283 source files` |
| `python3 -m ruff check . && python3 -m ruff format --check .` | `src/api` (199 files) | Passed | `All checks passed!`, `199 files already formatted` |
| `PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest tests/test_aftercare_screen.py tests/test_aftercare_served.py tests/test_sensor_handover_demo.py tests/test_sensor_handover_verify_guard.py tests/test_content_standard.py tests/test_list_export_inventory.py tests/test_role_endpoint_inventory.py -q` | `src/api` aftercare + handover + static inventory/content gates | Passed | `Ran 103 tests in 42.117s — OK` |
| `web-design-guidelines` audit against fresh `vercel-labs/web-interface-guidelines` `command.md` | `src/api/src/zava_forward/api/web/aftercare.js` | Passed | `src/api/src/zava_forward/api/web/aftercare.js`: `✓ pass` |

## Outcome

* Outcome: Conformant
* Outcome rationale: Every in-scope requirement (`FR-1`–`FR-4`, `NFR-1`–`NFR-2`), acceptance criterion (`AC-1`–`AC-5`), test ownership lock (`14 <= 18` net new test methods, zero `sys.modules` eviction), and critique disposition (`PC-001`–`PC-007`) is implemented cleanly and verified by passing static, unit, Node VM, HTTP, and web-guideline checks.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | None |
| Decision gap or invalid assumption | none | None |
| Material evidence gap | none | None |
| Non-blocking residual work | distinct follow-up | Track `OD-54` resident portal writes, `FR-036` live pack benchmark sign-off, and optional `_NEUTRAL_ERROR` wording cleanup as separate follow-up choices |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Focused tier passed (`mypy`, `ruff check`, `ruff format --check`, and focused `unittest` suites across `src/core` and `src/api`, plus `web-design-guidelines` review)
* Blockers: None

