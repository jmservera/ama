<!-- markdownlint-disable-file -->
# Critique: Issue 1530 plan (rubber-duck, single pass)

Verdict: Revise. Executed once, before any code or tests.

| # | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| 1 | Blocking | Restart eligibility must mirror `require_independent` including the history fallback, and require a safety role plus the accountable role for non-legacy holds | Accepted. Client check reads `raised_identity`/`repaired_identity`, falls back to the `history` actor for `safety_raised`/`safety_repaired`, then email/name fields. Tests cover history-only identity and role mismatch. Server stays authoritative |
| 2 | Blocking | Referral needs `!released && !referral_version`; timings stay available to the receiver after release | Accepted. Both conditions coded and tested |
| 3 | Blocking | Draft preservation across `refresh()` untested | Accepted. DOM test with two hazards checks unique ids and that each form submits only its own fields |
| 4 | Non-blocking | Receiver matching underspecified | Accepted. Receiver is a safety role with matching `code` (as before); receipt then acceptance then repair order stated |
| 5 | Non-blocking | Static fallback cannot prove criteria | Accepted. Use the existing node DOM shim in `test_case_journey.py`; no source-parsing fallback for DOM criteria |
| 6 | Non-blocking | Preserve existing contracts | Accepted. Verification matrix runs the existing tests and three browser checks |
