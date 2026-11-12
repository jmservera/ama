---
title: Changes, demo wave checkpoint 440 (2026-11-12)
description: Changes record for the bounded recurring checkpoint
ms.date: 2026-11-12
---

Plan: [plan](../../plans/2026-11-12/demo-wave-checkpoint-440-1112-plan.md). Critique: [critique](../../plans/2026-11-12/demo-wave-checkpoint-440-1112-critique.md).

## Files changed

* `docs/architecture/cutover-evidence-pack.md`: one appended section `Demo wave integrated-main checkpoint (2026-11-12 ...)` (83 added lines) and `ms.date` 2026-11-11 to 2026-11-12. No earlier line is changed.
* `docs/reference/README.md`: one appended index paragraph. `docs/reference/log.md`: one appended entry.
* `.copilot-tracking/{research,plans,details,changes,reviews,rpi-sessions}/2026-11-12/demo-wave-checkpoint-440-1112-*`: original RPI evidence.
* No source, test, tool, workflow, requirement or ADR file is changed.

## Divergences and amendments

* The plan's selectors ran as designed except: API selectors needed `src/api` on `PYTHONPATH` for `checks`, and `azure-eventhub`, `azure-identity` and `azure-iot-device` (declared pins) were pip-installed into the owned venv only after missing-dependency import failures. Every failed attempt is preserved in the external raw logs and named in the record.
* A preflight one-liner syntax error was rerun and the first log kept.
* The research hosted-state line was amended (not rewritten) after a direct read of workflow runs.
* The PR labels supplied in the task do not match the merged PRs; this is recorded in the research and the pack as an adverse qualification.

## Validation

* 281 tests ran, 0 skipped, 0 failures in the final runs (T1 14, T2 16, T3 4, T4 34, T5 37, T6 77, T7 79, T8 20). Raw output: `/home/azureuser/.copilot/session-state/676885f4-85ba-42d8-929c-40f438e5190f/files/checkpoint-440-1112/`.
* `git diff` shows additions only apart from the `ms.date` line; added lines are ASCII; the new pack anchor resolves.
* Not run: full suites, SQL Server, Docker, browser harness, scanners, hosted CI, any Azure, model or telemetry call, the full or `--changed` RPI gate (documentation-only focused tier).
