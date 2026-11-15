# Plan critique (rubber-duck, executed once, before code)

Verdict: Revise. All findings applied directly in the details file.

1. Blocking: inventory omitted rendered blocked states (ops.js 99-107, simulator-control.js 13-20 and 80-85, staff-intake.js 45). Applied.
2. Blocking: `/Owner:/` shortcut can leave a missing next action. Helper now requires both ordered clauses. Applied.
3. Blocking: next actions must differ by outcome (read failure, refusal, possibly committed change). Applied.
4. Non-blocking: extracted-function harness in test_case_journey.py; helper placement and unique global names. Applied.
5. Non-blocking: add runtime cases and keep the capacity "We could not load ... Try again." substring. Applied.
