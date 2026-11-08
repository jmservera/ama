---
title: Issue 79 details, continuation r17
ms.date: 2026-11-07
---

## Phase 2: base freeze

* Poll `gh run view 42361331168 --json status,conclusion` at bounded intervals (at most about 10 minutes in total) and fetch `origin/main` after each.
* Final base is `origin/main` once the run is `completed` and a second fetch shows no further movement; otherwise return a base blocker.

## Phase 3: rebase

* `git rebase origin/main` from the topic. On a `docs/reference/log.md` conflict keep all text from main, then append the topic's entry in original order; continue. Any non-log conflict stops the rebase for a recorded decision.
* Proof: `git range-diff` between the preserve ref and the new head, per-path blob comparison for the 64 non-log topic paths, and the log diff against the final base showing only additions.

## Phase 4: checks and records

* Run from `src/core/tests` and `src/api` with `PYTHONDONTWRITEBYTECODE=1` and the pinned tools in `/tmp/79-align-r13-1106/venv`: publication and runner tests, API wiring test, Ruff check and format, mypy.
* Write Changes, state and author Review under `.copilot-tracking/*/2026-11-07/issue-79-r17-*`, add one `docs/reference/log.md` entry, commit with the repository-local privacy-safe identity and the Copilot trailer.
