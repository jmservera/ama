---
title: Ranking archive ancestor durability 1258 plan critique
description: Independent read-only critique of the issue 1258 plan, with direct dispositions
ms.date: 2026-11-08
---

## Inputs and boundary

* Plan, details and research under `.copilot-tracking/` dated 2026-11-08 for `ranking-archive-ancestor-durability-1258`.
* Independent read-only subagent (rubber-duck). Repository reads only; no test, install, network or git write. Critique ran once; it is not repeated for this task.

Critique execution: Complete. Verdict: Revise.

## Findings and direct dispositions

| Id | Severity | Finding | Disposition |
| --- | --- | --- | --- |
| PC-001 | High | Missing-at-start set misses partial creation by a failed earlier run or a concurrent creator whose sync has not happened; retry walk only for `written False` with an empty set could falsely confirm. | Applied. Replaced by one fail-closed ancestor chain on every confirmation (plan D3); tests 1.3 to 1.5 added. |
| PC-002 | High | Skipping `EACCES` on ancestors, mount boundary and symlinks not proven. | Applied. No skipping; boundary defined as the writable run to mount point or root (D3); realpath (D4); tests 1.6, 1.7. Mount stop is a mock boundary, stated as such. |
| PC-003 | High | `self.dir` is `tmp/"archive"` and not pre-created, so existing tests are already first runs; existing exact event-order test would change. | Applied. Fixture note; labelled-subsequence tests; test 1.9 updates the existing test deliberately and records it. |
| PC-004 | Medium | Retry red evidence aborted before retry; API faults only archive sync. | Applied. Retry state seeded independently (1.3); ancestor-targeted runner and API regression (1.8). |
| PC-005 | Low | Runner reports a parent failure as an archive-folder failure. | Applied. Message and assertion update (D6, 2.4). |
| PC-006 | Low | Hosted checks cannot precede push; corrective commits invalidate receipt. | Applied. Plan 4.2 to 4.4 resequenced. |

## Not accepted or open

* None rejected. The critique confirmed parent-of-missing-directory is the correct sync set for a known stable chain; the revised plan generalizes it for retry soundness.
* D5 (extra steady-state directory syncs) is a declared behavior change for owner and reviewer visibility, not a criterion relaxation. No user decision is required unless the owner wants to relax criteria.
