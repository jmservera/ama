---
title: Sensor MSSQL gate issue record
ms.date: 2026-11-08
---

Issue: [1297](https://github.com/jmservera/ama/issues/1297), `fix(tools): bind sensor MSSQL skips to required SQL execution`.
Labels: `bug`, `delivery:demo-next`. State when read in this RPI: OPEN. Priority high: blocks #184 full-gate publication.

Creation was done by the earlier backlog discovery workflow on 2026-11-08, recorded in the supplied backlog records (discovery/sensor-mssql-gate-2026-11-08: handoff, issue-analysis, issues-plan, planning-log; outside this worktree and not modified). No milestone, parent or dependency field was set; #111 is related and not claimed complete; no other implementation dependency confirmed.

The body was read here with `gh issue view 1297` as data. Its criteria map to .copilot-tracking/plans/2026-11-08/sensor-mssql-gate-1297-plan.md. This record is issue-creation provenance only; it is not RPI evidence for the fix.

Branch fix/sensor-mssql-gate-1297 from main fa7ae0c9770e890f82482456bfcb8e97f1e05429.

Observed discrepancy: the issue cites ten sensor skips; main has eight (the #184 candidate has ten). See the research artifact.
