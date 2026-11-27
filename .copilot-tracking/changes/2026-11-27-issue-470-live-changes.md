---
title: Issue 470 live changes (2026-11-27)
ms.date: 2026-11-27
---

Tier FOCUSED (documentation only, no `src/` change; basis: no executable, workflow or dependency file touched). `rpi-checks.py --all` not run.

## Changes

* Added `docs/reference/research/issue-470-live-r10-2026-11-27.md` (per-group wall times, critical chain, comparison limits).
* Added an index row in `docs/reference/README.md` and a log entry in `docs/reference/log.md`.

## Validation

* Per-group values computed from the two receipts and cross-checked against `tools/rpi-gate-timing.py report` for g2182b; the tool refuses the failed g2182 receipt.
* Relative links checked; `git diff --check` clean.
* Hosted CI: not observed (nothing pushed, by instruction).

## Per-criterion table

| # | Criterion | State |
| --- | --- | --- |
| 1 | `--changed` selects groups and records scope | Proven (already ticked, not re-tested) |
| 2 | `--verify-receipt` rejects partial receipts | Proven (already ticked, not re-tested) |
| 3 | `--jobs` parallel groups within the lock rule | Proven (already ticked, not re-tested) |
| 4 | Measured full-run time before and after recorded in the PR | Unproven: no like-for-like pair (different head, tree, jobs; one receipt failed at the 1800 s `project-api` timeout) and PR publication is forbidden |
| 5 | Tests for group selection and receipt scope | Proven (already ticked, not re-tested) |

Nothing was ticked or closed.
