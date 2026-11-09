# Review addendum: native SQL Server evidence (#1292)

Dated 2026-11-08. The original review (`2026-11-08-priority-order-1292-review.md`,
Conformant on the agent review, SQL pending) is preserved. This addendum is not
a second review and not the independent exact-head review.

* Original blocker B-1 (native SQL pending) is resolved by the focused
  evidence in `changes/2026-11-08-priority-order-1292-changes-addendum-sql.md`:
  red on base and green on candidate for the new class and both original
  selectors, zero skips, backend confirmed.
* Acceptance criterion 3 (SQL parity) now has native focused evidence.
* Correction: the SQL schema and migration change requires the FULL local gate,
  recorded in `plans/2026-11-08-priority-order-1292-plan-amendment-gate-tier.md`.
  That gate is PENDING, as are receipt verification, independent exact-head
  review and hosted CI.
* Residual risks unchanged: ledger-enabled migration unproven; the same-`seq`
  batch case has no native red; legacy order is heuristic and needs a named
  data-owner decision for any live database; rolling deployments need old
  writers stopped first.
