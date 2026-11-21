---
title: Issue 184 live plan critique
ms.date: 2026-11-20
---

Execution: executed once (rubber-duck). Verdict: proceed with changes.

| Finding | Disposition |
| --- | --- |
| Receiver 2400 s windows every 30 min overlap | Applied: window 1500 s, cron every 30 min is replaced by a non-overlapping window shorter than the interval; freshness measured live. |
| Backlog replay from retention start may not reach head | Applied: measure backlog and throughput live before relying on the schedule; record result or mark unproven. |
| Operator tool and registry SDK absent from API image | Applied: ship scripts to throwaway jobs through the OPS_SCRIPT env var (repository code imported from the image); registration through raw REST. Stop if a grant beyond existing ones is needed. |
| Secret volume, filename mapping and stop path unproven | Applied: prove deploy and file mapping before registration; stop path is control.json expiry plus job deletion. |
| First slot before policy window | Applied: policy and mapping windows start at the previous slot boundary minus one hour. |
| First 20 open cases may not include existing granted homes | Applied: cohort is explicit, the three granted homes plus the first open others; verify indexed consent after configure. |
