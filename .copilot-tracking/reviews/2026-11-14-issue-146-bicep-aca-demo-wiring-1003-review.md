# Review: Bicep Container Apps demo wiring contract (2026-11-14)

Execution: executed once after implementation. Outcome: conformant for the stated scope; no material findings open.

* Boundary: the new test file only; no template changes.
* The tests prove source wiring, not deployed identity grants or revisions.
* Residual (follow-up, not routed into this task): regex-based text parsing is sensitive to Bicep formatting; a Bicep-compiled ARM JSON check would be sturdier if bicep is available in CI.
* Human review and hosted CI remain required and are not claimed.
