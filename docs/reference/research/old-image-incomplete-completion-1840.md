---
title: Old-image incomplete completion classification (issue 1840)
description: Per-criterion evidence for #1840 in the demo
ms.date: 2026-11-18
---

Refs #1840. Fixture-level evidence only; no historical-image, SQL, live AI or whole-#107 acceptance follows.

| Criterion | Proven | Evidence |
| --- | --- | --- |
| Failing-first regressions | Yes | Six subcases failed (`VIOLATED != INSUFFICIENT`) before the change. |
| Incomplete completion is INSUFFICIENT | Yes, fixture | `Judge.test_incomplete_mismatch_completion_with_an_active_mutated_row_is_insufficient`. |
| Preserve positive control and adverse precedence | Yes, fixture | 41 tests pass, 0 skips in an isolated venv. |
| Tests and strict typing recorded | Yes | Bare mypy from `src/api` clean in the shared env; the two untyped `config()` errors reproduced at baseline and were fixed. |
| Self-test works without a pip-installed checkout | Yes, fixture | `python -I` worker launched through an explicit-path launcher; `SelfTest` fails before and passes after on origin/main e91b6fa81. |
| Independent exact-head review and full tier | No | The owner brief for this run sets the focused tier; the review and an external full receipt remain for the coordinator. |

Azure was not used: the offline judge runs on no authorised demo resource, and no throwaway resource was created. Full details: `.copilot-tracking/changes/2026-11-18/issue-1840-live2-changes.md`.
