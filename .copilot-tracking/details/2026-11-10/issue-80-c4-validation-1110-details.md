---
title: Issue 80 capacity C4 instrumented validation, details
description: Phase details for the single observed whole capacity browser execution
ms.date: 2026-11-10
---

## Phase 1: pre-run integrity

* `git status --short` empty, `git rev-parse HEAD` equals `2cc34027...`, tree `b41c022b...`.
* sha256 of `src/api/checks/capacity_browser_check.py` and every `src/api/src/zava_forward/api/web/*` file recorded to `pre-hashes.txt`; observer sha256 in `observer.py.sha256`.
* Import origins from the owned venv `/tmp/ama-80-audit-venv-1110/bin/python` with the prior-chain `PYTHONPATH` (core, agents, api, orchestrator, importer sources plus allowed test-helper paths `core/tests`, `agents/tests`, `api/tests`) recorded to `origins.txt`; `ZF_DATA` absent.
* Host `uptime` and any other browser or heavy-lock holder noted; the checker takes the lock non-blocking itself.

## Phase 2: execution

* From `src/api`: `python observer.py <checks dir> <events.jsonl> /tmp/axepk/package/axe.min.js > run.log 2>&1; echo $? > run.exit`. No pipe, so the exit is the python process exit.
* No timeout wrapper that kills the run, no retry. Expected duration several minutes.

## Phase 3: reading

* Extract milestone lines in order and compare against the checker scenario names; confirm downloads, time, aftercare 403, both `delayed 401` iterations and the empty-capacity assertion line (about 885).
* Report served-asset hashes versus owned files, console and page errors, any non-2xx statuses by path and the primary exception.

## Phase 4: review and handoff

* One native review after `implement-done`; findings routed to Root. Handoff `handoff-80-c4-instrumented-validation-1110.md`.
