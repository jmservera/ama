<!-- markdownlint-disable-file -->
# Changes: Issue #133 acceptance-criteria evidence audit

* Task: `133-aftercare-ac-audit-1416`; Refs #133, #89; base `dafed6a270bdcc1f1be16cb0d2bca5550f8fcdaa`
* Plan: [plan](../../plans/2026-11-13/133-aftercare-ac-audit-1416-plan.md); critique: [critique](../../critiques/2026-11-13/133-aftercare-ac-audit-1416-critique.md)
* Scope: tracking-only; no source, test, GitHub issue or remote change. Tier Focused (documentation and evidence only).

## Executed test evidence

Environment: `/tmp/venv-133-1416` (`--system-site-packages`, editable `src/core`, `src/agents`, `src/api`), `ZF_RESIDENT_MSSQL` unset, `PYTHONDONTWRITEBYTECODE=1`. The first venv was deleted by another process after the core runs, so it was recreated and the api modules ran in the second one. The installs left no untracked files outside `.copilot-tracking`.

| Module | Directory | Ran | Result | Exit |
| --- | --- | --- | --- | --- |
| `test_aftercare` | `src/core/tests` | 23 | OK | 0 |
| `test_aftercare_intake` | `src/core/tests` | 44 | OK | 0 |
| `test_aftercare_store` | `src/core/tests` | 42 | OK, skipped=15 | 0 |
| `test_aftercare_screen` | `src/api` (`PYTHONPATH=../core/tests:../agents/tests`) | 13 | OK | 0 |
| `test_aftercare_served` | `src/api` (same) | 8 | OK | 0 |

* Total 130 tests ran, 0 failures, 15 skipped.
* All 15 skips are `opt-in owned loopback SQL Server` (the `MssqlAdapter` class). No MSSQL evidence exists in this run; the SQLite adapter ran.
* `test_aftercare_screen` calls `node -e` through `subprocess` in a vm with stubs (`test_aftercare_screen.py:114`). The node producer exited 0 because the module passed. It is not a served-browser or keyboard check; `src/api/checks/aftercare_browser_check.py` was not run here.

## Read-only probes (nothing written)

* AC5 denylist: `neutral_text` blocked only the literal `you will save`. It let through "You'll save money", "This will cut your bills", "The tenant caused this", "The resident is at fault", "Your bills will fall", "savings of 20% expected", "due to the occupant's behaviour", "Heating use led to the problem" and "Resident misunderstood".
* Pack surface: no occurrence of `pack` in `aftercare_intake.py` or `aftercare.js`; `AftercareService._route` (`aftercare_intake.py:861-922`) has no pack route.
* Registry entry `aftercare-concern-pack` (`ai_registry.py:130-141`): `enabled` false, `state` disabled, `approval_state` unapproved, `accountable_function` Retrofit Programme Manager, `accountable_individual` unknown, `manual_route` set, `required_approval_evidence` lists five unvalidated approvals, `impact_record.status` not assessed. It has no prompt or approved evaluation-threshold field.

## Per-criterion proof table

Verdict labels: `PROVEN` means every clause of the literal criterion is shown by merged, tested engineering; `NOT FULLY PROVEN` names the missing clause and its gate. Operational or human assurance is never inferred from code. Paths are relative to `src/core/src/zava_forward/core/` (`aftercare.py`, `aftercare_intake.py`, `ai_registry.py`), `src/api/src/zava_forward/api/` (`web/aftercare.js`, `server.py`) and the test directories above.

### AC1 A household or representative can raise a concern through an accessible route including a non-digital one: NOT FULLY PROVEN

| Clause | Implementation | Test (all passed) |
| --- | --- | --- |
| Household or representative as raiser, representative basis required | `aftercare.py:20,158,264-265`; `aftercare_intake.py:429-487` | `test_aftercare::test_representative_needs_a_stated_basis_and_kinds_are_checked`; `test_aftercare_intake::test_representative_basis_is_required_and_kept_verbatim` |
| Non-digital routes (phone, in person, paper, assisted visit) with a named recording staff member | `aftercare.py:258-263`; `aftercare_intake.py:63-68,489-499` | `test_aftercare::test_non_digital_route_needs_staff_and_channel`; `test_aftercare_intake::test_every_channel_is_accepted_and_digital_is_not` |
| Plain-language form with the accessible-route statement; manual paper fallback | `aftercare.py:33-36,91-149`; `aftercare_intake.py:403-427` | `test_aftercare::test_form_offers_non_digital_route_and_neutral_plain_text`; `test_aftercare_screen::test_form_uses_native_labelled_controls_and_no_owner_field` |
| Served and durable | `server.py:123,428-431,578,1322` | `test_aftercare_served::test_form_is_bounded_to_the_constructed_allowlist`, `test_replay_conflict_and_restart_readback` |

Missing clause: accessibility. No assistive-technology, keyboard or WCAG acceptance is recorded: the screen test states it is not a served-browser or keyboard check (`test_aftercare_screen.py:4-5`) and no test or document in the aftercare modules records an assistive-technology result. `src/core/README.md:4971` still lists "UI wiring (Fluent 2, WCAG)" as not delivered; that paragraph predates the served wiring and is stale, but it shows no accessibility acceptance was claimed (review finding R-1). The served route is staff-assisted only (`aftercare_intake.py:433`); the criterion does not require a digital self-service route, so its absence is a note, not a failed clause. Real operational use of the route is unobserved. Gate: accessibility testing with assistive technology and the owner's acceptance.

### AC2 Each concern has an owner, an investigation outcome and a remedy status that closure cannot erase: NOT FULLY PROVEN

| Clause | Implementation | Test |
| --- | --- | --- |
| Investigation outcome by the named owner with a human basis | `aftercare.py:299-330`; `aftercare_intake.py:613-660` | `test_aftercare::test_owner_is_required_and_only_owner_acts`; `test_aftercare_intake::test_only_the_owner_role_acts_and_remedy_needs_evidence` |
| Remedy status; completion needs outcome and evidence | `aftercare.py:332-343` | `test_aftercare::test_remedy_completion_needs_outcome_and_evidence` |
| Handover and financial closure never change a concern or remedy; unresolved stays visible | `aftercare.py:345-370`; `aftercare_intake.py:73-76,717-737` | `test_aftercare::test_closure_cannot_erase_concern_or_remedy`, `test_cannot_determine_stays_unresolved_and_overdue_lists_it`; `test_aftercare_intake::test_closure_never_changes_the_concern_or_erases_the_remedy` |
| Restore cannot weaken a record | `aftercare.py:197-224` | `test_aftercare::test_restore_refuses_a_snapshot_that_weakens_a_concern`, `test_restore_is_numeric_whatever_the_json_key_order` |

Missing clause: "has an owner". A served concern is created with owner `Unknown (no owner named)` (`aftercare_intake.py:53,473`), nobody can act on it until a manager names a synthetic scenario role (`aftercare_intake.py:623,673-691`), and the receipt says so plainly (`aftercare_intake.py:520-523`). Outcome and remedy start as states (`received`, `not_assessed`) rather than values. Covered by `test_unknown_owner_cannot_be_acted_for_and_is_listed_unresolved` and `test_assignment_is_manager_only_once_and_labelled_synthetic`. Closure independence is proven in software only; real owner naming and complaint handling are unobserved. Gate: named real owners and Housing owner acceptance.

### AC3 A resident report is never dismissed because a sensor reading is normal: PROVEN as an implemented safeguard (engineering)

| Clause | Implementation | Test |
| --- | --- | --- |
| `dismissed_by_sensor` is always false | `aftercare.py:282` | `test_aftercare::test_normal_sensor_never_dismisses_and_is_not_a_basis` |
| A sensor is not an outcome basis | `aftercare.py:24,317-318` | same test |
| Later sensor context changes no state, outcome or remedy | `aftercare.py:289-297`; `aftercare_intake.py:77-79,693-715` | `test_aftercare::test_later_normal_signal_is_context_only`; `test_aftercare_intake::test_normal_sensor_context_never_dismisses_and_stays_staff_only`, `test_valid_descriptive_context_is_kept_and_never_dismisses_or_touches_remedy` |
| Restore refuses a dismissed record | `aftercare.py:214` | `test_aftercare::test_restore_refuses_a_snapshot_that_weakens_a_concern` |
| Concern is listed whatever the comparison says | `aftercare_intake.py:739-791` | `test_aftercare_intake::test_concern_is_listed_whatever_the_comparison_says` |

Boundary (critique PC-002): the code stops a sensor-only basis and any dismissal flag; it cannot show that a person never relied on a normal reading. No operational evidence exists. The coordinator may treat the engineering criterion as met; a stricter reading needs observed investigations. No external gate blocks the software clause.

### AC4 Evaluator view shows baseline, outcomes and unresolved concerns with stated denominators and unknowns: NOT FULLY PROVEN

| Clause | Implementation | Test |
| --- | --- | --- |
| Baseline per home, Unknown when not comparable | `aftercare_intake.py:800-835`; `aftercare.py:413-417` | `test_aftercare::test_unknown_baseline_is_stated_not_zero`; `test_aftercare_intake::test_insufficient_or_missing_comparison_is_unknown_without_partial_means` |
| Outcomes including `no_outcome_yet` in the API payload | `aftercare.py:398-400`; `aftercare_intake.py:764` | `test_aftercare::test_denominators_unknowns_and_scope`; `test_aftercare_intake::test_every_home_has_a_row_with_denominators_and_unknowns` |
| Unresolved with denominator and scope | `aftercare.py:180-182,419-424`; `aftercare_intake.py:783-791` | `test_aftercare_screen::test_unresolved_fraction_zero_unknown_and_malformed_denominators`, `test_evaluator_view_from_the_service_states_fraction_and_unknowns`; `test_aftercare_served::test_evaluator_readback_has_unknown_denominator_and_no_closure` |
| Stated unknowns | `aftercare.py:410,427`; `aftercare_intake.py:80-86,793` | `test_aftercare_screen::test_evaluator_table_is_named_scoped_and_scrolls_inside_a_region` |

Missing clauses (critique PC-001): the rendered table (`web/aftercare.js:170-204`) shows home, comparison, baseline and late means, concern count and unresolved count. It does not display outcomes by category, so "outcomes" is in the API payload but not shown to an evaluator. The view says itself that evaluator role access is not approved and the DPO position on outcome data is Unknown (`aftercare_intake.py:80-86`, the issue's open dependencies), and baselines are synthetic exercise values. Gates: evaluator role access, DPO position, and a rendered-outcomes change (a follow-up code item, not made here).

### AC5 No causation, blame or savings promise appears in any generated or templated text: NOT FULLY PROVEN

| Clause | Implementation | Test |
| --- | --- | --- |
| Fixed templates carry no banned phrase | `aftercare.py:33-58,66-72` | `test_aftercare::test_templated_text_has_no_causation_blame_or_savings`; `test_aftercare_intake::test_no_templated_text_states_causation_blame_or_savings` (form, receipt, concern, evaluator payloads) |
| AI summary and sensor context pass the guard | `aftercare.py:75-84,450` | `test_aftercare::test_ai_summary_is_guarded_and_proposal_only`, `test_context_text_is_guarded_and_typed` |
| Rendered evaluator text has no "blame" | `web/aftercare.js` | `test_aftercare_screen::test_evaluator_view_from_the_service_states_fraction_and_unknowns` (`:198`) |

Missing clause: the guard is a denylist of ten literal phrases (`aftercare.py:46-58`). The probe above shows common paraphrases of causation, fault and savings pass it, so the universal "any generated text" claim is not shown for the optional AI summary, and the tests scan selected payloads against the same list. Static strings in `aftercare.js` are not scanned by any guard. Observed templates contain no such wording, but that is a review of present text, not a control that holds for future or AI-generated text. Gate: a stronger guard or an approved human review of generated text (a follow-up code item, not made here).

### AC6 Optional AI concern pack stays a registered proposal with human review (FR-036): NOT FULLY PROVEN

| Clause | Implementation | Test |
| --- | --- | --- |
| Pack exists without AI, is unreviewed and unapproved | `aftercare.py:431-469` | `test_aftercare::test_pack_exists_without_ai_and_is_unreviewed` |
| Registered, unapproved and disabled; no live authorisation | `ai_registry.py:130-141` | `test_aftercare::test_pack_is_a_registered_unapproved_task` |
| Only the named owner accepts or rejects; the concern never changes | `aftercare.py:471-488` | `test_aftercare::test_review_by_named_owner_never_changes_the_concern` |

Missing clauses (critique PC-003): human review has no served surface (no pack route in `_route`, no pack screen; `src/core/README.md:4971`). The FR-036 registry fields (PRD line 1411) are only partly present: purpose, roles, capability, source permissions, accountable function, enable or disable state and manual fallback are set; prompt or options and approved evaluation thresholds are absent, the accountable individual is `unknown`, and `required_approval_evidence` is unvalidated. Gates: model route and release evidence, owner and DPO approvals, and a served review screen.

## Summary for the coordinator

* Fully proven by reviewed merged engineering and eligible to tick: AC3 only, on the engineering reading stated above.
* Not eligible to tick: AC1, AC2, AC4, AC5, AC6, with the missing clauses and gates listed per criterion.
* Already merged on `main` and confirmed in code and tests: #1456 numeric restore order and #1458 blank `FileStateStore` refusal; neither alters the verdicts.
* Suggested follow-ups (not done): render outcomes in the evaluator table (AC4); replace the phrase denylist or add human review of generated text (AC5); a served pack review route and the missing FR-036 fields (AC6); named owners at intake (AC2); assistive-technology test (AC1).

## Files changed

* Added tracking files only under `.copilot-tracking/` (research, plan, details, critique, changes, state).
