---
title: Issue 1288 UI and snapshot correlation research (0900)
ms.date: 2026-11-14
---

## Scope

Local engineering evidence only. No live model call, Azure write or private dataset. Base `origin/main` 61e1917dd; PR #1331 (1b7a1719b) is already merged. Disposition: Research executed.

## Findings

* Delivered: bounded permission-projected read model (`sensor_view`, `GET /api/cases/{id}/sensors`, Retrofit Programme Manager and Quality Inspector only), the ops.js sensor panel, the Quality assistant snapshot with `sources.sensors`, and the proactive scan with dedupe, gate and cursor machinery. Existing `test_quality_sensors*.py` pass (191 plus 239 tests; MSSQL variants skipped locally).
* Existing tests prove API/model-request equality and restart de-duplication on the churn path, but no suite correlated the UI source fields, snapshot citations and failure states together, and none pinned the H0 note.
* H0 note: `review_flag` status is `not-current` when the task is not actionable (`assistants.py` `review_flag`; actionable needs the current epoch and `body.release == release_reference`), otherwise `review-suggested`. Fresh-service equality therefore holds only with the same synthetic release and epoch. This is intended behaviour, not a defect.
* No genuine wiring gap found; no source change needed. Chat and role-screen files are untouched.
* The Chromium check `checks/quality_sensors_browser_check.py` could not run: Chrome aborts because the worktree path makes the profile socket path too long (environment limit, not an application result). Not claimed.

## Planning Readiness

Ready: add one focused test module.
