---
title: Issue 115 live recheck changes
date: 2026-11-18
---

Tier: FOCUSED, documentation only; no src, infra or workflow change. Evidence note: [research note](../../../docs/reference/research/digest-verification-alert-live-2026-11-18.md).

## Per-criterion table

| Criterion (issue 115) | Proven | Evidence or reason |
| --- | --- | --- |
| Digests land in an immutable container with a retention lock | Deferred to production (#1908) | Owner decision 2026-11-18 |
| Scheduled verification alerts on mismatch: verifier alerts and exits non-zero | Proven | Merged note; 31 digest_blob tests pass again |
| Same: Azure Monitor alert fires | Proven | Instance fired 08:18:52Z, rule still enabled, Sev1 |
| Same: email delivery to the ops receiver | Unproven | Mailbox not accessible; one email receiver configured |
| Same: runs from the cron schedule | Unproven | Trigger is Manual; reinstating it is an infra change |
| Same: direct log read | Unproven | Workspace and storage deny this host; rules unchanged |

## Validation

Read-only `az` queries; `unittest tests.test_digest_blob` in `src/orchestrator` (31 OK). No Azure resource created or changed.
