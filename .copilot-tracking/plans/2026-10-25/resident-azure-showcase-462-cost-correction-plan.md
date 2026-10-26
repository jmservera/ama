# Prospective plan: cost evidence correction (issue 462)

Date: 2026-10-25, written 17:01Z before any query or edit for this correction. Read-only. No runtime change, cloud mutation, push or password.

Why: the coordinator found that the preflight extension's resource-type figures for 24 to 25 October (21.87 + 5.63 + 4.56 + 3.89 + 3.83 ...) exceed the stated day total of 22.39. That is a contradiction, not rounding.

Steps:
1. Re-query the same scope (resource group `ama`, ActualCost, USD) for 2026-10-24 to 2026-10-25 by day and by resource type with identical time period, and save aggregate JSON values-free under an external temp path, then record the concise rows.
2. Append an erratum to the extension retracting the earlier breakdown and the "conservative upper bound" wording; the 47.75 figure is relabelled a run-rate scenario, not a bound.
3. Reconstruct resources created or changed since 2026-10-24T13:39Z from resource creation timestamps and tracked deployment metadata; query Cost Management by ResourceId for those exact resources.
4. Price the planned app from Azure retail price metadata (public API, no secrets) with a time-bounded estimate; no headroom claim without proof; lag stays explicit.
5. Append corrections: the original cap is incremental and excludes the pre-existing baseline; the SQL view/principal named approval must be recorded; no purge is planned (default soft delete retains); secret expiry does not expire ARM deployment history, so no such cleanup claim is made.
6. Local commit only if needed; no push.
