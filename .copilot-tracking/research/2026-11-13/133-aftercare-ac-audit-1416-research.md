<!-- markdownlint-disable-file -->
# Task Research: Issue #133 literal acceptance-criteria evidence audit (AC1 to AC6)

* Task: `133-aftercare-ac-audit-1416`; session `rpi-133-ac-audit`; tier Focused; Refs #133, #89
* Base: `dafed6a270bdcc1f1be16cb0d2bca5550f8fcdaa` on `fix/demo-aftercare-persistence-133-1408`
* Research disposition: executed (static read of code, tests, README and PRD; test execution is deferred to Implement after plan critique)
* Planning Readiness: Ready

## Scope and sources read

* `src/core/src/zava_forward/core/aftercare.py` (488 lines), `aftercare_intake.py` (922), `aftercare_store.py` (153)
* `src/core/src/zava_forward/core/ai_registry.py:130-141` (pack registration)
* `src/api/src/zava_forward/api/web/aftercare.js` (400); server wiring `src/api/src/zava_forward/api/server.py:123,219,428-431,578,1322`
* Tests: `src/core/tests/test_aftercare.py`, `test_aftercare_intake.py`, `test_aftercare_store.py`; `src/api/tests/test_aftercare_screen.py`, `test_aftercare_served.py`
* `src/core/README.md:4933-5008` (self-declared "Not delivered" list); PRD `FR-036` (line 1411), `FR-049` (1424), `AC-063` (2159, status "Not run")
* Issue #133 body (read only via `gh issue view`; not edited): six unticked criteria; open dependencies are evaluator role access and the DPO position on outcome data

## Earlier merged work confirmed (not re-done)

* #1401 numeric restore order (#1456): `aftercare.py:173-177,197-224`
* #1402 blank `FileStateStore` refusal (#1458): `aftercare_intake.py:132-170`, `test_blank_state_*`

## Preliminary per-criterion findings (to be confirmed by executed tests)

| AC | Implementation evidence | Test evidence | Preliminary verdict |
| --- | --- | --- | --- |
| AC1 raise a concern, accessible, non-digital route | `aftercare.py:24-33,91-149,152-166,236-287`; `aftercare_intake.py:403-427,429-487`; `aftercare.js` form | `test_non_digital_route_needs_staff_and_channel`, `test_form_offers_non_digital_route_and_neutral_plain_text`, `test_every_channel_is_accepted_and_digital_is_not`, `test_representative_basis_is_required_and_kept_verbatim`, `test_form_uses_native_labelled_controls_and_no_owner_field`, `test_form_is_bounded_to_the_constructed_allowlist` | Engineering proves a staff-assisted non-digital route and representative basis. The served route is staff-only (`RECORD_ROLES`); no household self-service digital submission is served, and no assistive-technology or WCAG acceptance exists. Not fully proven. |
| AC2 owner, outcome, remedy that closure cannot erase | `aftercare.py:184-225,299-357`; `aftercare_intake.py:173,613-735` | `test_owner_is_required_and_only_owner_acts`, `test_closure_cannot_erase_concern_or_remedy`, `test_remedy_completion_needs_outcome_and_evidence`, `test_closure_never_changes_the_concern_or_erases_the_remedy`, `test_unknown_owner_cannot_be_acted_for_and_is_listed_unresolved` | Outcome, remedy and closure independence are proven. A served concern starts with owner `Unknown (no owner named)` until a manager names a synthetic scenario owner, so "each concern has an owner" holds only after assignment and the owners are synthetic roles. Split verdict. |
| AC3 sensor never dismisses | `aftercare.py:92-93,262,289-297,309-330,208`; `aftercare_intake.py:693-715` | `test_normal_sensor_never_dismisses_and_is_not_a_basis`, `test_later_normal_signal_is_context_only`, `test_normal_sensor_context_never_dismisses_and_stays_staff_only`, `test_valid_descriptive_context_is_kept_and_never_dismisses_or_touches_remedy`, `test_restore_refuses_a_snapshot_that_weakens_a_concern` | Proven in engineering: `dismissed_by_sensor` is always false, a sensor is not an outcome basis, and restore refuses a dismissed snapshot. |
| AC4 evaluator view with denominators and unknowns | `aftercare.py:180-182,383-429`; `aftercare_intake.py:739-835,80-86` | `test_denominators_unknowns_and_scope`, `test_unknown_baseline_is_stated_not_zero`, `test_every_home_has_a_row_with_denominators_and_unknowns`, `test_insufficient_or_missing_comparison_is_unknown_without_partial_means`, `test_evaluator_view_from_the_service_states_fraction_and_unknowns`, `test_evaluator_readback_has_unknown_denominator_and_no_closure` | Engineering proves the synthetic view. The view states itself that evaluator role access is not approved and the DPO position is Unknown; the baseline is a synthetic exercise comparison. Awaits those gates. |
| AC5 no causation, blame or savings in generated or templated text | `aftercare.py:46-72` (denylist of 10 phrases), guard call sites in `_labelled`, `_context`, `propose_pack`, `_receipt`, `_comparison` | `test_templated_text_has_no_causation_blame_or_savings` (core) and `test_no_templated_text_states_causation_blame_or_savings` (intake), `test_ai_summary_is_guarded_and_proposal_only`, `test_evaluator_view_from_the_service_states_fraction_and_unknowns` | The guard is a phrase denylist and `aftercare.js` static strings are not scanned. To be probed after critique for easy bypasses (for example "you'll save"). Not claimed fully proven. |
| AC6 optional AI pack is a registered proposal with human review (FR-036) | `aftercare.py:431-488`; `ai_registry.py:130-141` (disabled, unapproved, manual route) | `test_pack_exists_without_ai_and_is_unreviewed`, `test_ai_summary_is_guarded_and_proposal_only`, `test_review_by_named_owner_never_changes_the_concern`, `test_pack_is_a_registered_unapproved_task` | Core register and registry are proven. `AftercareService` and `/api/aftercare` expose no pack route or screen, so the human review has no served surface (README says "a pack screen" not delivered). Core-only. |

Final verdicts and corrected citations are in the changes file; where they differ from this preliminary table, the changes file governs (AC4 is not fully proven because the rendered table omits outcomes; AC3 is limited to implemented safeguards).

## Key facts and boundaries

* README 4971 and 5008 declare what is not delivered: evaluator role access, DPO position, a model route, a pack screen, SQL-hosted MSSQL evidence.
* `AftercareService` routes (`aftercare_intake.py:861-922`) cover form, evaluator, concerns, outcome, remedy, owner, sensor-context and closures only.
* PRD `AC-063` status is `Not run` and describes aging bands and lease evidence that the aftercare module does not implement; it is the PRD's closure acceptance, not the issue's criteria.
* No GitHub issue edits will be made. Verdicts feed the coordinator, who ticks only criteria whose every clause is proven.

## Open items for execution

* Run the five aftercare test modules in `/tmp/venv-133-1416` and record counts, SQL skips and producer exits.
* Probe the AC5 denylist after critique.

## Planning Readiness

Ready. The plan will produce one tracking-only evidence audit; no production code change is planned.
