---
title: Issue 146 live2 changes (2026-11-18)
---

Tier FOCUSED. Docs and evidence only; no src, infra or workflow change. Read-only Azure queries; no resource created or deleted in this pass.

## Files

* docs/reference/research/issue-146-live2-monitoring-evidence-2026-11-18.md (new)
* docs/reference/research/issue-146-live2-evidence-2026-11-18/ (new, redacted raw output)
* docs/reference/README.md (index entry), docs/reference/log.md (append)
* .copilot-tracking/ research, critique, plan, details, changes, review, state `issue-146-live2-state.json`

## Deviation

The brief's state path `issue-146-live-state.json` already exists (committed by an earlier run); to avoid overwriting it this pass uses `issue-146-live2-state.json`.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| C1 alerts for jobs, poison queue, digest, IoT | Partly proven | Digest installed and fired (raw retained). Job-failure rule fired Sev3 (alert history retained, rule deleted). IoT metric exists. Poison queue unproven (no queue logs). No permanent job, IoT or poison alert installed |
| C2 workbook for availability, errors, latency, cost vs budget | Unproven | No workbook installed; query access private-link only, so no render |
| C3 runbook entry with owner for each alert | Partly proven | 20 proposed-owner entries, 52 offline tests pass; owners are roles, not named people |
| T2 AI usage by capability beside Azure cost with variance | Unproven | Panels in source only; no render; no cost export table |

## Process note

The first `implement-start` witness call was refused because the state file lacked the changes pointer; the note and index edits had already been written, and the witness recorded the source as already dirty. Retry succeeded after the state was corrected.
