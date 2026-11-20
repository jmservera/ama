# Review: issue 2061 (2026-11-20)

Execution: one self-review pass of the diff (no correction cycles needed). Outcome: conformant for the offline Bicep scope; criteria 4 and 6 remain unproven.

Checked:

* Production unchanged: `demoSingleEnvironment` defaults false, guard rejects non-demo combinations, `internal` identity falls back to the API identity, new roles are conditional.
* Role matrix, SQL grants and tests agree (`test_identity_rbac`, wiring tests pass).
* No secrets, subscription id redacted in evidence files.

Routed follow-ups: deploy and live sign-in/negative test (needs owner approval); Entra URI before/after (needs directory read); full gate receipt; owner approval of the delete list.
