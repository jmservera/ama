<!-- markdownlint-disable-file -->
# RPI Changes: Issue #133 Aftercare Concern Route and Lived-Performance Review

## Metadata

* Task ID: aftercare-133-2346
* Related plan: .copilot-tracking/plans/2026-11-14/aftercare-133-2346-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/aftercare-133-2346-phase-details.md
* Implementation date: 2026-11-14

## Execution Status

* Status: Complete
* Declared invocation scope: Full plan (P01, P02, P03, P04)
* Completed scope markers: P01, P01-T01, P01-T02, P02, P02-T01, P02-T02, P03, P03-T01, P03-T02, P04, P04-T01, P04-T02
* All remaining active-plan markers: None
* Status basis: All four phases (`P01`–`P04`) implemented, verified with `mypy`, `ruff check`, `ruff format --check`, focused `unittest` suites across `src/core` and `src/api`, and `web-design-guidelines` review (`✓ pass`).

## Execution Summary

Delivered accessible digital and non-digital aftercare concern intake parity (`"representative"` channel, `"call_back"` support normalization, digital-only `household_receipt`, and `<select multiple>` UI support), hardened the deterministic neutral-language guard across multiline text, blame/causation/savings paraphrases, and staff outcome/remedy/pack-review/restore paths (including atomic validation before state mutation in `record_outcome`), exposed `FR-036` `ai_registry` proposal-only human-review governance metadata and strict `"Unknown"` non-coercion in the evaluator lived-performance view, eliminated `sys.modules.pop` bulk eviction from `aftercare_fixture.py`, added 14 focused semantic tests across `src/core` and `src/api`, updated package READMEs, and verified all static, unit, HTTP, and web guideline gates.

## Completed Work

### P01: Intake Channel Parity, Receipt Isolation, and Fixture Safety (`P01-T01`, `P01-T02`)

* Removed `sys.modules.pop(...)` bulk eviction from `src/core/tests/aftercare_fixture.py`, updating `sys.path` and namespace `__path__` in-place on `zava_forward` and `zava_forward.core`.
* Added `"representative"` to `NON_DIGITAL_CHANNELS`, `intake_form()["non_digital_channels"]`, `ACCESSIBLE_ROUTE`, `HOUSEHOLD_MANUAL_ROUTE`, `CHANNEL_LABELS`, and `raise_concern` validation; added `"multiple": True` on `support_needed` in `intake_form()`; normalized legacy `"call_back"` to `"callback_window"`; and restricted `AftercareService.household_receipt` to `route == "digital"` concerns.

### P02: Deterministic Causation, Resident-Blame, and Savings-Promise Guard (`P02-T01`, `P02-T02`)

* Hardened `strip_unsafe_sentences` to fold intra-paragraph newlines and re-verify joined sentences against `neutral_text`.
* Expanded `PARAPHRASE_PATTERNS` to reject occupant/user error/lifestyle/habits (including singular `'s`), thermostat/heating-control/ventilation/window/trickle-vent/drying-clothes blame, finite `"stems/arises/results from"`, scoped `"is responsible for"`, and bill-savings/reduction guarantees.
* Enforced `neutral_text` on `AftercareRegister.record_outcome`, `set_remedy`, `review_pack`, and `from_state` (including pack text fields while preserving verbatim `household_statement`), and added `NEUTRAL_EVIDENCE_MESSAGE` field validation and `_safe_error_text` in `AftercareService`.

### P03: Evaluator Unknown Preservation, FR-036 Pack Governance, and Accessible Web UI (`P03-T01`, `P03-T02`)

* Bound `FR-036` `ai_registry` metadata into `AftercareRegister.propose_pack` and `AftercareService.evaluator_view` (`concern_pack_task`).
* Updated `src/api/src/zava_forward/api/web/aftercare.js` with `AC_CHANNEL_LABELS`, `AC_SUPPORT_LABELS`, `<select multiple>` handling in `acField`/`acReadValues`, optional form-note guards, dynamic submit target selection, strict `"Unknown"` non-coercion in `aftercareEvaluatorView`, and plain-language `FR-036` proposal-only copy.

### P04: Focused Core and API Tests, Documentation Sync, and Verification (`P04-T01`, `P04-T02`)

* Added 6 focused semantic tests in `src/core/tests/test_aftercare.py` (`Issue133RefinementTests`) and 4 focused semantic tests in `src/core/tests/test_aftercare_intake.py` (`Issue133IntakeRefinementTests`), verifying zero `sys.modules` eviction in `aftercare_fixture.py`, `"representative"` channel intake, `"call_back"` normalization, digital-only `household_receipt`, multiline `strip_unsafe_sentences`, paraphrase guard coverage, atomic `record_outcome`/`set_remedy`/`review_pack`/`from_state` neutrality enforcement, and `FR-036` `concern_pack_task` metadata.
* Added 3 focused Node VM tests in `src/api/tests/test_aftercare_screen.py` and 1 served HTTP test in `src/api/tests/test_aftercare_served.py` (total 14 net new test methods within the `<= 18` plan cap), and updated `src/core/README.md` and `src/api/README.md`.

## Implementation-Time Plan and Detail Updates

* Local judgment (`AftercareRegister.record_outcome` atomicity): Moved `neutral_text(_text(evidence, "Outcome evidence"))` ahead of `rec["investigation"] = "outcome_recorded"` in `src/core/src/zava_forward/core/aftercare.py` so a rejected non-neutral outcome evidence string never leaves `rec["investigation"]` partially mutated in memory. Preserves approved `P02-T02` intent with no plan scope change.
* Local judgment (`AftercareService.handle` neutral error surface): Added import-verified `NEUTRAL_EVIDENCE_MESSAGE`, field-keyed `_staff_evidence` / `_context_errors` validation (`HTTP 400`), and `_safe_error_text` in `src/core/src/zava_forward/core/aftercare_intake.py` because `aftercare._NEUTRAL_ERROR` mentions `"blame"` and would otherwise fail `neutral_text(str(exc))` on direct domain `ValueError` fallbacks.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `python3 -m mypy` | `src/core` (316 files) | Passed | Exit 0 (`Success: no issues found in 316 source files`) |
| `python3 -m ruff check . && python3 -m ruff format --check .` | `src/core` (263 files) | Passed | Exit 0 (`All checks passed!`, `263 files already formatted`) |
| Focused `unittest` (`test_aftercare.py`, `test_aftercare_intake.py`, `test_aftercare_store.py`, `test_quality_procurement.py`) | `src/core` | Passed | Exit 0 (`Ran 278 tests in 263.391s — OK (skipped=15)`) |
| `python3 -m mypy` | `src/api` (283 files) | Passed | Exit 0 (`Success: no issues found in 283 source files`) |
| `python3 -m ruff check . && python3 -m ruff format --check .` | `src/api` (199 files) | Passed | Exit 0 (`All checks passed!`, `199 files already formatted`) |
| Focused `unittest` (`test_aftercare_screen.py`, `test_aftercare_served.py`, `test_sensor_handover_demo.py`, `test_sensor_handover_verify_guard.py`, `test_content_standard.py`, `test_list_export_inventory.py`, `test_role_endpoint_inventory.py`) | `src/api` | Passed | Exit 0 (`Ran 103 tests in 42.117s — OK`) |
| `web-design-guidelines` fresh rules audit | `src/api/src/zava_forward/api/web/aftercare.js` | Passed | Fresh fetch of `vercel-labs/web-interface-guidelines` `command.md`; `src/api/src/zava_forward/api/web/aftercare.js`: `✓ pass` |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled (`P01`–`P04` and all `P01-T01`–`P04-T02` tasks checked `[x]`)
* Completed-work evidence and handoff prose: Reconciled
* Validation, blockers, remaining work, and follow-up items: Reconciled
* Review readiness: Ready for one-pass `rpi-review`

## Blockers

* None

## Remaining Work

* None in declared plan scope.

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-14/aftercare-133-2346-plan.md, `## Follow-Up Items`
* Resident showcase portal (`resident_demo`) live session write route for aftercare concerns: deferred to `OD-54` resident-portal increment.
* Held-out benchmark and release sign-off for `aftercare-concern-pack` live model drafting: deferred to `FR-036` activation governance.

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: Full plan; `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01`, `P03-T02`, `P04`, `P04-T01`, `P04-T02` completed; none remaining
* Validation coverage: Focused tier complete (`mypy`, `ruff check`, `ruff format --check`, and focused aftercare/handover/inventory `unittest` suites in `src/core` and `src/api`, plus `web-design-guidelines` review)
* Blockers: None
* Current plan and detail updates: Local-judgment atomicity and neutral error-surface refinements recorded above; no scope or acceptance-criteria divergence
* Planning and critique state: Ready (`PC-001`..`PC-007` resolved in plan)
* Follow-up items: 2 deferred items mirrored from plan
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: Confirmed automatic RPI Agent parent
