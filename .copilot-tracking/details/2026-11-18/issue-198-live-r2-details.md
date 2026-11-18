---
title: Issue 198 live r2 details
date: 2026-11-18
---

# Phase details

## Phase 2
* Add one row after the existing issue-198 row in `docs/reference/README.md`.
* Append a dated `update` entry to `docs/reference/log.md`; never edit earlier entries.
* Success: relative links resolve (checked with a link script); `git diff --stat` shows only docs and tracking files.

## Phase 3
* Changes record states the per-criterion table, validation run and non-applicable checks (mypy, ruff: no Python edited; web tests: no web edit; rpi-checks --all: not run).
* Review once; then commit with trailers.
