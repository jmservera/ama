---
title: Issue 530 focused-gate admission details (supersedes Phase 4 wording)
ms.date: 2026-11-08
---

## Prospective command (NOT YET ADMITTED; do not run now)

Attached, bounded, one foreground invocation from the repository root, after `git fetch origin main`, with a fresh short external output directory that does not yet exist and stdin from `/dev/null`:

```text
python3 tools/rpi-checks.py --changed --jobs 1 --lock-timeout 0 \
  --base <current-origin-main-sha> --out /tmp/rpi-530-focused-<new> < /dev/null
```

No manual setsid, background process, sleep or lock polling. Heavy lock `/tmp/ama-rpi-heavy.lock` is taken by the runner itself; `--lock-timeout 0` stops immediately if held.

## Expected selection (derived from source, to be compared with the runner's receipt)

* Groups: `preflight`, `namespace`, `static`.
* Skips: project-core, project-agents, project-api, project-orchestrator, project-importer, infra, migration, browser, mssql, image-*, logo-0600, each with the runner's own reason.
* Any other group, especially `browser`, `mssql` or `image-*`, is a scope conflict: stop and report, never waive or alter a check.

## Before the run

Confirm the inert-only changed-path list (see plan) and that no recorded group other than the three could be selected; if not, stop.

## After the run

Verify the receipt with `--verify-receipt <receipt.json> --base <current-origin-main-sha> --required-scope partial` (the default is full, and a changed-scope receipt is partial); keep all reporting external with no later source writes. A new commit invalidates the gate.

## Critique

Recorded in [.copilot-tracking/challenges/2026-11-08-issue-530-focused-gate-admission-critique.md](../challenges/2026-11-08-issue-530-focused-gate-admission-critique.md).
