# Review: keyless IoT Hub Registry adapter (#185, initial increment)

Executed once, 2026-11-10T02:43Z, by the implementing agent (no nested agent). Boundary: working tree against base `2bfd5e07545db18380f48a9854654c8393d0e9bc`. Independent exact-head assessment remains required and is not claimed here.

## Execution

Reviewed the diff and adapter source against the brief; reran nothing beyond the recorded focused validation (35 new, 50 existing tests, ruff, mypy all clean).

## Outcome

Conformant for the stated scope, with minor open items routed to follow-up. No correction cycle is authorised (balance UNKNOWN).

## Checks

* Ownership boundary: only the four owned source files and dated records changed. No `device_identity`, `device_provision`, CLI, API, infra or KB edits.
* Lazy optional SDK; import effect-free (subprocess test); Core imports without SDK.
* Create-only conditional header, disabled, exact marker, public thumbprints; conflict never adopts.
* Delete needs current exact ownership and exact quoted non-wildcard ETag; drift refuses; no unconditioned retry.
* `list_run` refuses at 1000; 404 distinguished from 401/403/5xx/timeout; sanitised fixed codes; only owned clients closed.
* Dev extra pins the SDK so Core CI runs the tests, not skips.

## Findings (routed to later work)

* F1 (low): a DELETE answered 404 after a positive ownership read maps to `REJECTED`; the documented 204 for a missing resource makes this unlikely, but the safer reading is a readback. Route to a later user-selected plan.
* F2 (low): a marked identity not in the enrolment that the list payload hides cannot be found; documented in README.
* F3 (info): the simulator models the documented REST table; Azure create-only, ETag, list limit and RBAC behaviour is unobserved.
* F4 (open, out of scope): Registry-before-credential order, no auth-update, and whole #185 credential lifecycle remain open.
* F5 (info): hosted CI unobserved; focused tier, not the full gate.
