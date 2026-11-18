---
title: Issue 116 live r2 changes
ms.date: 2026-11-18
---

## Changes

* Added docs/reference/research/issue-116-live-r2-evidence-2026-11-18.md, README row and log entry.
* Added evidence under .copilot-tracking/evidence/2026-11-18/issue-116-live-r2/.
* No source change; tier FOCUSED (documentation and read-only live probes). Live Azure: read-only only, nothing created or deleted. rpi-checks.py --all not run.

## Per-criterion table

| # | Criterion | Proven or unproven | Basis |
| --- | --- | --- | --- |
| 1 | Reason roles confirmed (OD-14, OD-19) | Unproven (enforcement for one role shown) | No second sign-in; Graph privileges insufficient; human approval excluded for demo |
| 2 | Allowlists at every provider boundary | Unproven live | Provider payloads not exposed; offline spies only |
| 3 | Output and export permission recheck | Partly proven | Zero reason-value hits across 7 surfaces for the one role; no second role or model call |
| 4 | Document AI hold | Unproven live | No uploaded document; upload would change state |

Validation: 0 credential matches in retained files; git diff review of docs; no unit tests apply.
