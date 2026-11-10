<!-- markdownlint-disable-file -->
# RPI Plan Critique: issue-152-mobile-empty-c4-1110

* Task ID: issue-152-mobile-empty-c4-1110
* Executed once, before implementation. Verdict: Revise.
* Boundary: plan, details and research only; no source assessed.

## Coverage

All brief requirements are mapped to AC1-AC6. Gaps below are precision issues, no user decision needed.

### PC-001 [Medium]: negative could leak into later checks
A hidden-style mutation left in the page would poison subsequent role checks or mask a real failure. Fix: restore DOM and viewport inside the same step and assert the mutation was caught before continuing.

### PC-002 [Low]: role-specific wording is not in the product
The product copy is role-independent; "role-specific" must not tempt invented copy. Fix: assert the product sentence for roles with empty manifest ids and no element for roles with ids.

### PC-003 [Low]: viewport side effect
The loop changes the viewport the rest of the harness assumes is 1280. Fix: end the loop at 1280 so later checks are unchanged.
