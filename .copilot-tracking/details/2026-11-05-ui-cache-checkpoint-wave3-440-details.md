---
title: UI and cache recovery checkpoint wave 3 details (Refs #440)
description: Phase details, commands and acceptance for the focused checkpoint
ms.date: 2026-11-05
ms.topic: reference
---

## Phase 1: pin main

* `git fetch origin`; `gh run view 42036086584 --json status,conclusion`; proceed only when completed and `origin/main` is stable across two reads without sleeping or long-polling.
* Record commit, tree, and the diff from `2edba50b7` (expected: rubric file only).

## Phase 2: auxiliary worktree

* `git worktree add --detach /tmp/ama-main-440-ui-cache-wave3 <pinned-main>`; refuse if the path exists. No overwrite or delete.
* Own venv under `/tmp/ama-main-440-ui-cache-wave3-venv` (new path, refused if present); install `src/core`, `src/agents`, `src/api` from the worktree; verify `__file__` of `zava_forward` modules resolves inside the worktree; scrubbed environment with `PYTHONDONTWRITEBYTECODE=1`.

## Phase 3: observation

* Lock: Python `fcntl.flock(LOCK_EX | LOCK_NB)` on `/tmp/ama-rpi-heavy.lock`; held for both checks; if unavailable record and stop the slice.
* Check 1: `python -m unittest tools.test_rpi_checks.GateTests.test_api_install_prevents_scrubbed_server_child_writing_source_bytecode` from the worktree root.
* Check 2: from `src/api`, `python -m checks.case_journey_browser_check --axe <pinned axe> --out <external dir>`, discovering pinned Chromium and axe 4.10.3 as existing evidence records describe. Unchanged thresholds (320x800 bound 1600).
* Verify the worktree is clean (tracked, untracked, ignored) after the runs.

## Phase 4: documentation

* Append the seventh checkpoint after the sixth in `docs/architecture/cutover-evidence-pack.md` with identities, traceability, classification, commands, findings, recommendation and gates.
* Add one entry to the end of `docs/reference/log.md` and update the index row for the evidence pack in `docs/reference/README.md` only if it lists checkpoint counts.

## Acceptance

* Identities verified against git; every command and exit in the record is real; no claim beyond observation.
* Link, ASCII and diff checks clean; no deletion of existing records.
