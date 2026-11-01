---
title: Issue 189 publisher wiring plan
ms.date: 2026-11-01
task_id: issue-189-publisher-wiring
---

## Plan

* [x] Add `HubPublisher.run_controlled(frames, controller, estimate_path, truth)` in `src/api`.
* [x] Tests: refuses without a recorded estimate and creates no client; sends with the controller pacer and leaves state `stopped`; stop signal from scale_down path keeps rate bounded.
* [x] Run unit tests, ruff check, ruff format --check, mypy for `src/api`.

## Critique

Single pass 2026-11-01: keep the change to one method; no HTTP route or startup activation (existing module contract). Compatible, applied.
