---
title: Issue 1397 live changes
ms.date: 2026-11-18
---

Refs #1397. FOCUSED tier basis: documentation only; no src, workflow, SQL, infrastructure or security change.
Live Azure was authorised but not needed; none was used.

## Changes

* Added `docs/reference/research/rubric-1397-live-run-history-2026-11-18.md`.
* Added an index row in `docs/reference/README.md` and an entry in `docs/reference/log.md`.

## Per-criterion table

| Criterion | Result | Evidence |
|-----------|--------|----------|
| 1 Preserve attempt and identities | Proven (earlier, PR 1408) | README.md lines 230-266 |
| 2 Classify rejection from actual payload | Proven | `agent_output.json` of run 42838857558: one placeholder item, `details` `{}`, error `Maximum allowed: 1` for line 2 |
| 3 Recurrence and limits | Proven (earlier, PR 1408) | README.md lines 268-307 |
| 4 Source-bound recovery and publication | Proven (cumulative diff) | run 42841391974 scored `6cc59776` changes, PR 1398 merged `c66370042`; a per-SHA score for `6cc59776` cannot exist |

Still open for owner action: tick criteria 2 and 4 and decide on closure; design items (refuse placeholder before
append, reconcile prompt quota statement, upload `decision.json`) need workflow or prompt edits and the full tier.

## Validation

* `git diff` and link review of the three files: pass (see review).
* No tests, mypy or ruff: no executable file changed. `rpi-checks.py --all` not run.
