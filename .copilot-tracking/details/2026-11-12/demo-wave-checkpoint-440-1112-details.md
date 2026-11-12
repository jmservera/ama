---
title: Details, demo wave checkpoint 440 (2026-11-12)
description: Phase details for the bounded recurring checkpoint record
ms.date: 2026-11-12
---

Plan: [plan](../../plans/2026-11-12/demo-wave-checkpoint-440-1112-plan.md).

## P3 command shape

* Interpreter: `$E/venv/bin/python` where `E=/home/azureuser/.copilot/session-state/676885f4-85ba-42d8-929c-40f438e5190f/files/checkpoint-440-1112`; owned venv created with `--system-site-packages`, `pip install --no-deps -e src/core -e src/api`.
* Environment: `env -i` with `PATH`, an owned temporary `HOME` and `ZF_DATA`, `ZF_RESIDENT_MSSQL` unset; `PYTHONDONTWRITEBYTECODE=1` so tracked and ignored source folders are not touched.
* Critique-applied (C1, C4): selectors run from an owned external working directory with `python -m unittest discover -s <abs tests dir> -p <file> -q`. API selectors use `PYTHONPATH=<worktree>/src/core/tests:<worktree>/src/agents/tests` as the repository guide states (not `mvp`). Stdout, stderr and the exit code go to separate files per selector; counts are read from stderr. `git status --porcelain --ignored -- src` is compared before and after.
* Critique-applied (C2): the venv also installs `src/agents` with `--no-deps -e`; preflight prints the `__file__` of core, agents, api, `live_simulator`, `live_control`, `exposure_limits`, `ai` and of the test helper modules.
* Critique-applied (C3): provenance compares `git hash-object <file>` with `git rev-parse HEAD:<path>` for each tested and changed source file.
* Critique-applied (C5, C6): T3 is consumer regression only; non-finite behaviour is attributed to T2. Loopback HTTP fixtures (T3, T5) and Node (T6) are disclosed; `node --version` is preflighted.

## P4 sections to write

1. Heading `## Demo wave integrated-main checkpoint (2026-11-12, Refs #440 #99 #116 #80 #432 #184)` appended after the last section; text starts with Draft, local-only, not approved.
2. Identities table (pin, fresh main, trees, doc blobs, merged commits, hosted state, issue states, exclusions).
3. Label discrepancy table copied from the research.
4. Commands table (Id, selector, exit, ran, skipped, notes) and totals; raw log location.
5. Traceability table with classes; boundaries; findings; recommendation; process limits.
6. `docs/reference/log.md`: one appended entry. `docs/reference/README.md`: one pointer line next to the existing pack pointers, plus the existing ms.date handling if required by that file.

## Validation of the record

Markdown link check of new relative links, `git diff --stat`, check that no earlier line changed (`git diff` shows additions only for the pack and the log), ASCII punctuation and no em dashes, and that counts in the record equal the raw logs.
