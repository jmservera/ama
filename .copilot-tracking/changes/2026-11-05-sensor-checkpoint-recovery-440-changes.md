---
title: Sensor checkpoint recovery changes (Refs #440 #184 #110)
description: Changes, validation commands and limits for the documentation-only sensor record
ms.date: 2026-11-05
ms.topic: reference
---

## Changes

* `docs/architecture/cutover-evidence-pack.md`: appended 147 lines, section "Fifth stabilization checkpoint: current-main sensor contract, retention and handover (2026-11-05, Refs #440 #184 #110)". No earlier line changed (`git diff --stat`: 3 files, 155 insertions, 0 deletions).
* `docs/reference/README.md`: 3 lines added to the existing #110/#184 index entry linking the new section.
* `docs/reference/log.md`: one new dated entry appended; earlier entries untouched.
* No source, test, schema, infra, workflow, coordinator, agent, prompt or case study file changed. No new canonical page.

## Actual commands and outcomes (2026-11-05, working tree before commit)

| Command | Outcome |
| --- | --- |
| `git fetch origin main` then `git rev-parse origin/main` | `c6d5a8f3c3a35892322300be27b9747f7b11362d` |
| `git diff --stat HEAD c6d5a8f3 -- src docs infra` | Empty: sensor source and documents identical to the working base |
| `git rev-parse c6d5a8f3:<path>` for BRD, PRD, ADR 0002, ADR 0003, `live_readings.py`, `sensor_consumer.py` and four other cited sources | Blob IDs match those cited in the record (`34d88395`, `c788b917`, `cbe21530`, `d6064539`, `289051ee`, `8125b88b`) |
| `git diff --check` | exit 0 |
| Local read-only Python script: relative link and anchor check of added Markdown lines in the three docs | 0 problems |
| Same script: added text scan | 0 non-ASCII characters, 0 em dashes |
| `ps -p 1361642` | Alive, elapsed 14:44; native FULL gate command observed earlier with base `c6d5a8f3`; observation only |
| `gh issue view` 440, 184, 110, 188, 109, 165, 183, 185, 186, 189, 140 and `gh pr view` 1203, 1205, 1209, 1210; `gh issue list --search` for duplicates | Read-only GitHub reads, exit 0 (one `gh issue view --comments --json` call exited 1 on a flag error and was not repeated; issue comments were taken from the external scope report) |

## Not run (unperformed, not passed)

* `python3 tools/rpi-checks.py --changed` (takes the shared heavy lock currently owned by the native FULL gate; a fail-fast attempt was also not made).
* Package unit suites, Ruff, mypy, SQLite or SQL Server integration, Docker and images, Chromium or browser, FULL gate, benchmarks.
* Cloud, provider, model, billing and private dataset access; Azure or IoT Hub sends; issue, PR or remote writes.
* No native gate receipt was created or inferred.

## Deviations

* One edit to the research artifact (blob ID placeholders) used a local script instead of the edit tool; content only replaced placeholders.
* No scope divergence. The final commit identity is recorded externally and in the final response because a committed file cannot hold its own hash.
