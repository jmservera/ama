# Research: issue 2164, round 14 (2026-11-25)

Task: issue-2164-live-20261125T225906Z. Disposition: executed. Planning Readiness: Ready.

## Findings

* Issue 2164 has no checkbox criteria; the three asks are the scope decision, a `view_only` test and a scope-bypass test. Rounds 1 to 13 proved them (docs/reference/research/issue-2164-deployed-code-proof-2026-11-25.md).
* The only unproven item is a live restricted-roster-row sign-in. It needs a roster edit, excluded by the brief, so it stays unproven.
* Code angle: `AssistantService.authorize` (src/core/src/zava_forward/core/assistants.py) re-reads a bound principal's roster row and validates `case_ids` and `areas` shape (list, at most 1000 entries, strings of 1 to 128 characters) after the bound re-read, failing closed.
* Gap: tests in src/api/tests/test_assistants.py cover scope, revocation, forged pointer, tenant and `view_only`, but none sets a malformed scope on a bound row. Only the non-Entra path is exercised for malformed capability data elsewhere.

## Decision

Add one focused api test, `test_bound_entra_malformed_row_scope_fails_closed`. No src change, so the focused tier applies.
