---
title: Issue 184 child stories, live re-check (demo)
description: Fresh read of the #184 sub-issue states and a per-criterion proven or unproven record, 2026-11-19
ms.date: 2026-11-19
ms.topic: reference
---

Refs #184. Scope: synthetic desktop demo; owner decisions of 2026-11-18. Base `46920a0dd`. Read at 2026-11-19T16:08Z with the existing `gh` login. No Azure resource created, no credentials read, no source change. It repeats, from fresh data, the earlier [child stories note](./issue-184-child-stories-demo-2026-11-19.md).

## Per-criterion result

| Criterion | Ticked | Proven for the demo | Evidence |
| --- | --- | --- | --- |
| All child stories closed or deferred | No | Yes, as a backlog state at 2026-11-19T16:08Z | Five sub-issues, all `closed` with reason `completed`; `sub_issues_summary` is 5 of 5 |
| Simulator never connects to, discovers or represents installed real devices | Yes | Not re-run | Already ticked |
| No device key or connection string in source, logs or telemetry | Yes | Not re-run | Already ticked; the issue still lists whole-source and log scans as unproved |

## Child stories

| Issue | State | Reason | Closed (UTC) |
| --- | --- | --- | --- |
| #185 | closed | completed | 2026-11-19T14:21:35Z |
| #186 | closed | completed | 2026-10-18T13:17:23Z |
| #187 | closed | completed | 2026-10-31T09:51:42Z |
| #188 | closed | completed | 2026-11-18T08:09:08Z |
| #189 | closed | completed | 2026-11-19T14:21:21Z |

Commands: `gh api repos/jmservera/ama/issues/184 --jq .sub_issues_summary` and `gh api repos/jmservera/ama/issues/<n> --jq '[.number,.state,.state_reason,.closed_at]|@tsv'` for each child.

## Limits

* #1288 is related and open but is not a sub-issue of #184, so it is not counted.
* This records closed state only; it does not re-audit each child's own acceptance criteria.
* The offline audit in `tools/test_epic_child_disposition_audit.py` still lists #184 as `deferred` under #165. That table is repository-evidence only and is not asserted against live state; it is left unchanged.
* No code test was added: a test cannot assert live GitHub state and would restate a snapshot.
* The checkbox stays unticked for the owner after exact-head review.
