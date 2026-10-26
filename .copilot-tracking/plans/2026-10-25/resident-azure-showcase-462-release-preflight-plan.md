# Issue 462 release preflight: prospective research and plan (2026-10-25T22:20Z)

Written BEFORE any probe in this route. Read-only; group `ama` only. Candidate under separate
coordinator assessment: `aaee4d32`. No application source edits.

## Intent

Produce release-decision evidence: refreshed Cost Management ledger with retained raw metadata,
baseline versus work-created resources, a priced minimal deployment to 2026-10-26T12:00Z with a
lag reserve, and exact resource and action scopes for the later SQL job and vault write path.

## Constraints

* No push, full gate, Azure write, secret list or read, job start or exec, SQL query, role or
  network change, paid test, RG deletion. Original cumulative USD 50 incremental cap not reset;
  USD 700 October applies to `ama` only.
* Earlier raw cost JSON was deleted (Addendum 2 erratum); earlier summaries are historical only.

## Plan

1. Create a private evidence directory `~/.ama462-evidence/release-preflight-2026-10-25` mode 0700
   outside the repository; keep sanitized non-secret raw JSON and a SHA-256 manifest; never delete.
2. Cost Management queries scoped to `ama` (ActualCost, USD): ungrouped daily and by ResourceId by
   day, from 2026-10-24 to now. Record coverage, row counts, totals, retrieval time; reconcile
   the two shapes. State lag honestly; no hard-ceiling claim.
3. ARM metadata (read): resource list with creation and change times, container app and job
   revisions, identities, role assignments at exact scopes, vault properties. Classify baseline
   versus work-created or changed.
4. Price the bounded configuration (at most 1 replica, min 0, stated CPU and RAM) using the
   public retail meters already recorded plus fresh API values where needed; include build, SQL
   job, vault operations, image storage, logging and egress with explicit assumptions, and a
   billing-lag reserve derived from the observed lag.
5. Identify the SQL init job identity and vault write and workload read scopes from metadata only.
6. Append findings as a dated release-preflight evidence artifact, run one read-only review, commit
   locally with the privacy-safe identity. No critique of a new action is claimed because nothing
   new is authorised; this route is evidence only.

## Stop conditions

If headroom cannot responsibly be cleared, name the smallest missing owner decision and a concrete
stop condition. Do not ask the owner to invent a ledger.
