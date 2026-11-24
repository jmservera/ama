---
title: Issue 220 no-retaliation closure evidence
description: Test and live-probe evidence for the last unticked criterion of issue 220
ms.date: 2026-11-24
---

Criterion: "No retaliation, inferred refusal or delayed hazard response". Demo, synthetic data, desktop.

## Test evidence (checkout of main at 7023da86d8, run 2026-11-24)

* `src/core`: `PYTHONPATH=src:tests python3 -m unittest test_no_retaliation_guard_220 test_challenge_no_retaliation_220 test_issue_220_challenge_route`: 13 tests, OK.
* `src/api`: `PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest test_challenge_no_retaliation_api_220 test_challenge_non_retaliation_hazard_guard`: 10 tests, OK. A logged "law store is not loaded" traceback comes from a test fixture and does not fail a test.

| Promise | Tests |
| --- | --- |
| No retaliation | `test_each_protected_change_is_refused`, `test_retaliating_writer_is_refused_and_nothing_saved`, `test_adverse_keys_are_rejected_despite_case_spacing_and_hyphen_variants`, `test_safeguard_verifier_fails_closed_on_every_adverse_mutation_class` |
| No inferred refusal | `test_challenge_open_and_resolve_leave_protected_state_unchanged`, `test_assurance_is_stamped_only_when_nothing_protected_changed` |
| No delayed hazard response | `test_hazard_concern_is_routed_to_hazard_intake_and_saves_nothing`, `test_http_assistant_proposal_challenge_endpoint_lifecycle_and_safety_routing` (hazard added immediately, clock preserved, existing hazards unchanged) |

## Live probe

`probe_live.py` signed in to `ca-cutover-test-demo-api` (revision 0000059) with the staff test user, read at runtime. GET `/api/me` returned 200; a challenge POST to a nonexistent proposal returned 400 "Supply the integer proposal revision.", so the route is deployed and authenticated. Result: `live-probe-result.json`; screenshot: `live-app.png`. Nothing was created, so no cleanup is needed.

## Limits

The live probe does not prove the no-retaliation behaviour; that rests on the tests. The deployed image was not matched to this commit. A mutating live challenge was avoided to keep hazard-intake data off the shared demo.
