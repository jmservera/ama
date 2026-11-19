---
title: Issue 145 live r7 research (2026-11-19)
---

# Research

Disposition: reused. The same-day audit [issue-145-live-20261119T1419Z-2026-11-19.md](../../docs/reference/research/issue-145-live-20261119T1419Z-2026-11-19.md) and the r6 note hold the read-only Azure SQL evidence and the per-criterion table. Issue #145 re-read at HEAD 7ea3a1ff6: C4 and R1 to R5 remain unticked.

Findings at this head:

* C4: `infra/modules/sql.bicep` already parameterises `backupStorageRedundancy` and `backupRetentionDays`; the missing piece is an approved #121 retention decision (deferred to #1906, production). Nothing to build.
* R1, R2: need a restore drill or legal-hold state; drills are not authorised for the demo.
* R3: `recovery.reapply_deletions` reapplies erasure only. Release suspension or revocation and allowance state live only in the database, so it is the one real code gap. It touches release authority and SQL state, which the brief routes to the FULL tier with the complete gate, and `rpi-checks.py --all` is forbidden here.
* R4 waived for the demo; R5 needs an independent qualified person.

No Azure action was taken in this run. Planning Readiness: Ready for a stop outcome.
