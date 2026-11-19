---
title: Issue 115 live research (2026-11-19)
ms.date: 2026-11-19
---

Refs #115. Demo, desktop only, FOCUSED tier unless src changes.

## Scope

* Criterion 1 (immutable container with lock): ticked, deferred to production (#1908). Not re-proven.
* Criterion 2 (scheduled verification alerts on mismatch): unticked. Prior note `docs/reference/research/digest-verification-alert-live-2026-11-18.md` proved verifier, marker and fired Azure Monitor alert by hand; left unproven the cron trigger (deployed job is `Manual`, source `containerapps.bicep` has `0 2 * * *`, covered by `test_bicep_policy.py:1232`).

## Findings so far

* Source has the schedule and tests; no source defect found. Gap is deployed-demo only.
* Plan: prove a scheduled trigger runs the verifier on the demo with a throwaway scheduled job, delete it afterwards, record in the docs research note.

Disposition: executed. Planning Readiness: Ready.
