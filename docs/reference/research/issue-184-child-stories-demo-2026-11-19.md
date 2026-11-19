---
title: Issue 184 child stories closed (demo)
description: Per-criterion proven or unproven record for #184 on the synthetic demo, 2026-11-19
ms.date: 2026-11-19
ms.topic: reference
---

Refs #184. Scope: synthetic desktop demo; owner decisions of 2026-11-18. Base `adb10ae6d`. No Azure resource created, no credentials read, no source change.

## Per-criterion result

| Criterion | Ticked | Proven for the demo | Evidence |
| --- | --- | --- | --- |
| All child stories closed or deferred | No | Yes, as a backlog state at 2026-11-19 | GitHub sub-issue API for #184 returns five children, all `closed` with reason `completed`; `sub_issues_summary` is 5 of 5, 100 percent |
| Simulator never connects to, discovers or represents installed real devices | Yes | Not re-run | Already ticked; no change |
| No device key or connection string in source, logs or telemetry | Yes | Not re-run | Already ticked; the issue notes whole-source and log scans were still unproved, which this note does not change |

## Child stories

| Issue | Title | Closed (UTC) |
| --- | --- | --- |
| #185 | Simulated device identity and provisioning | 2026-11-19T14:21:35Z |
| #186 | Message schema, rate and volume | 2026-10-18T13:17:23Z |
| #187 | Replay, speed controls and failure injection | 2026-10-31T09:51:42Z |
| #188 | Ingestion into the store and consistency with the backfill | 2026-11-18T08:09:08Z |
| #189 | Cost, scale and run controls for the simulator | 2026-11-19T14:21:21Z |

Commands: `gh api repos/jmservera/ama/issues/184/sub_issues` and `gh api repos/jmservera/ama/issues/184 --jq .sub_issues_summary`.

## Limits

* #1288 mentions #184 in its body but is not a sub-issue of #184; it is a related, open quality feature and is not counted.
* #185 and #189 closed about half an hour before this check; this note records their closed state, not a review of their closing evidence.
* Whether each child's own acceptance criteria hold was not re-audited here. The criterion in the issue is the closed-or-deferred state only.
* Live simulator, Hub, SQL and UI flow stay unproved by this note, and no live Azure action was taken.
* The checkbox is left unticked for the coordinator or owner to tick after exact-head review.
