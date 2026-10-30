<!-- markdownlint-disable-file -->
---
title: Original view coverage implementation evidence
description: Routed browser-observability correction after the one Review
ms.date: 2026-10-28
---

Task ID: 524-view-coverage; parent 524-correction1. Full one-task scope; Complete.
Plan/details use the matching view-coverage slug and date.
Preserve .copilot-tracking/reviews/logs/2026-10-28/workspace-script-retry-524-correction1-review.md
Complete / Not accepted, including its RV-001 observer finding. Do not repeat it.
This bounded continuation is necessary to deliver the owner's existing requested
proof, not unselected unrelated follow-up work.
First execution boundary: replace late wrapper with existing CDP original-function
entry coverage in the one existing browser owner; validate under shared lock.
Completed: P01/P01-T01. Remaining: final publication gates and owner live follow-up.

## Implemented Result

Removed the load-event wrapper and its window counter. Existing CDP precise
coverage now reads the actual original roleScreensView function-entry range.
Require zero calls after real delayed settlement; after legitimate revisit,
take a new reset-interval sample and require one call. Top-level evaluation
counts, deterministic native load/error, unchanged source, status/hash/login,
request bounds and native controls remain asserted.

## Validation

* /tmp/ama-524-view-coverage-browser-20261028.log: full actual Chromium suite passed
  under shared nonblocking lock at 17:39:42Z, including original-function counts
  in navigation, timeout late execution and same-document 401/login.
* /tmp/ama-524-view-coverage-negative-20261028.log: negative control passed.
  Nonblocking contention retried every60s from17:40:18Z until admission. The
  constructed early original view invocation threw before rendering and was
  suppressed by the test-only injected caller; the new assertion detected it.
  This directly verifies the Review's precise false-pass concern, not only
  a successful normal run. No checkout or real companion source was mutated.
* Final 32 focused units passed in0.220s; Ruff check and47-file format check,
  mypy92, Node syntax and both changed Python files <=100 characters passed.
* Prior full API discovery1149/314 existing skips remains valid for unchanged
  production/session/unit files. Complete exact-head gate reruns its matrix.

## Validated Source Identity

| File | SHA-256 |
| --- | --- |
| src/api/src/zava_forward/api/web/app.js | 71d71ec29055b73e81f957a6c80e5fcbf581ed935c141f2ae6d82414e357a8c0 |
| src/api/tests/test_workspace_scripts.py | 4e69723822d0b922a7381db033c57731a998acc8eecbb3a120a8705c7828b8b1 |
| src/api/checks/workspace_scripts_browser_check.py | 8fb832a5e5308e218409b29c24c5f75403a90b38089f5301285cf8b0da6fa9ad |
| src/api/README.md | 27260076fc142af0a8d9ae213889c4e803a370aacd658d24b17f2c287ab7b0cd |

## Generated-Output Preservation

Finite selection:61 task-generated Ruff/bytecode files. Archived the entire
current tracking snapshot and selection (3278 members), verified full readback,
restored and hash-compared every selected member into fresh external scratch,
checked all tracked and tracking-protected bytes before/after journalled unlink.
No historical evidence deleted. Archive, exact manifest, protected identities,
restored bytes and journal: /tmp/ama-524-correction1-generated-archive-20261028.
Ignored candidate-file listing is now empty.

## Current Handoff

The original task Review and correction1 Review remain Complete / Not accepted,
unchanged. This is the routed bounded implementation, not a conformant Review
claim or a second RPI Review. Final independent exact-head assessment must cover
the post-Review original-function measurement delta and positive/negative logs.
Source/evidence ready for privacy-safe commit, full external exact-head gate,
fresh-main receipt verification, independent assessment and nonforce push/PR.
No current source/validation blocker. Required hosted/human approval and live
verification remain separate; live cause and deployment stay pending owner.
