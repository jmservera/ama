# Issue 2164 research (2026-11-27)

Task: decide whether roster-bound Entra staff inherit roster case_ids/areas in `assistants.authorize`, with tests for view_only and scope bypass.

Disposition: executed. Planning Readiness: Ready.

Findings
* `src/core/src/zava_forward/core/assistants.py` `authorize` (line ~1555) rejects view_only principals, then, for a principal with a verified `bound` pointer, re-reads the roster row by bound email, requires matching `oid` and `row_tenant_ok`, and applies that row's role, disabled/active, `case_ids` and `areas` checks. Unbound principals keep the verified-key authority.
* Delivered by commit 6a03928ccb (#2274, Refs #2164). Tests in `src/api/tests/test_assistants.py`: `test_bound_entra_staff_inherit_roster_scope_and_revocation`, `test_bound_entra_forged_pointer_tenant_and_area_scope`, `test_bound_entra_malformed_row_scope_fails_closed`, `test_challenge_staff_gate_bound_entra_row`, `test_unbound_and_view_only_entra_principals`.
* Issue 2164 is still open with no acceptance-criteria checklist; its body asks to decide and add tests.
* Live Azure is not relevant: the behaviour is a pure authorization rule with no deployed surface to probe.
