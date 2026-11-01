# Research: issue 466 resident sensors and assistant, focused re-verification (r3), 2026-11-01

* Disposition: executed (fresh local run on branch `feat/resident-sensor-assistant`, equal to origin/main 51657d30). Planning Readiness: Ready.
* Prior evidence reused: [2026-11-01 research](2026-11-01-issue-466-resident-sensor-gauges-research.md), [decision record](../../docs/architecture/resident-assistant-prototype.md), log entries 2026-10-31 and 2026-11-01 (Refs #466).

## Findings

* The slice is already merged (PRs #472, #473, #474, #586, #603, #677): own-home synthetic gauges and history, own-case advisory assistant, cross-resident tests, recorded model, cap and credential decision.
* Branch has no diff against origin/main, so no source change is required for the acceptance criteria 2 to 6.
* Criterion 1 (owner confirms scope and priority) is human approval and cannot be proven by an agent; it stays unmet.
* Manual assistive-technology acceptance and live resident checks remain owner-run. No Azure live resource is touched.

## Validation evidence (fresh venv, pip only)

| Check | Result |
| --- | --- |
| core `test_resident*.py` | 355 run, OK, 103 skipped (SQL/opt-in) |
| core `test_sensor*.py` | 144 run, OK, 1 skipped |
| api `test_resident*.py` | 167 run, OK, 9 skipped (browser/opt-in) |
| ruff check, ruff format --check (core, api) | pass, 216 files formatted |
| mypy core / api | no issues (190 / 139 files) |
| node --check resident.js | ok |

## Open items

* Owner scope confirmation (criterion 1); manual AT acceptance; hosted CI as publication evidence.
