# Issue 136 ranking archive Blob Bicep plan critique (2026-11-09)

Refs #136, Refs #1258. One critique of the final-candidate plan (`.copilot-tracking/plans/2026-11-09-ranking-blob-bicep-136-plan.md`) by an independent read-only subagent (rubber-duck). Executed once. Verdict: Revise; one Blocking, two Significant, one Minor. No finding conflicts with a confirmed owner decision and none needs a user decision. Not repeated for this task.

| ID | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| PC-001 | Blocking | The new guard argument also needs the constrained parameter and output entry in `infra/modules/guard.bicep`; omitting it fails compilation | Accepted. Added to D6, Phase 3 and details. The existing generic guard test (`Empty means`, `minLength` 1, passed set equals declared set) enforces it |
| PC-002 | Significant | Tests do not trace the compiled conditional output through both modules to the API env values | Accepted. Details test 7 evaluates the compiled chain for off, on/0 and on/30 |
| PC-003 | Significant | The guard name implied approval though it only checks a positive number | Accepted. Renamed `pilotRankingArchiveRequiresConfiguredRetention`; docs state approval and locking remain unverified |
| PC-004 | Minor | `allowProtectedAppendWrites: false` matches `ledger-digests`, not `audit-archive` (true) | Accepted. Plan cites the ledger-digests pattern |
