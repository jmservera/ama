---
title: Issue 115 live changes
date: 2026-11-18
---

Tier: FOCUSED. Documentation only; no src, infra or workflow file changed. Live Azure actions were run as authorised on 2026-11-18 and are recorded in the [research note](../../../docs/reference/research/digest-verification-alert-live-2026-11-18.md).

Files: that research note (new), `docs/reference/README.md` (index entry), `docs/reference/log.md` (entry).

## Per-criterion table

| Criterion (issue 115) | Proven | Evidence or reason |
| --- | --- | --- |
| Digests land in an immutable container with a retention lock | Deferred to production (#1908) | Owner decision 2026-11-18; not attempted |
| Scheduled verification alerts on mismatch: verifier detects mismatch on a copy | Proven | `LEDGER_DIGEST_ALERT`, exit 1 at 08:09:35 |
| Same: Azure Monitor alert fires | Proven | Alert `Fired`, Sev1, 08:18:52 |
| Same: baseline on real digests stays intact | Proven | `LEDGER_DIGEST_OK`, 2 digests, 996 entries |
| Same: email delivery to the ops receiver | Unproven | Mailbox not accessible |
| Same: runs from the cron schedule | Unproven | Deployed job trigger is Manual; schedule not reinstated (infra change) |

## Cleanup

Throwaway job deleted; copy blobs and container deleted (soft delete applies); two failed override executions (env dropped by override) preserved on the real job's history.

## Validation

Git diff and link review of the three documentation files. No unit tests or mypy applicable (no code change).
