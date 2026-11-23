---
title: Issue 349 live r10 changes
ms.date: 2026-11-23
---

## Changes

* Planned: `src/api/tests/test_auth.py` gains one regression test (no production change).
* Added: research note `docs/reference/research/issue-349-tenant-prerequisites-live-r10-2026-11-23.md` and evidence under `.copilot-tracking/evidence/2026-11-23/issue-349-live10/`.

## Per-criterion table

| # | Verdict |
| --- | --- |
| 1 | Proven for the demo registration; provisioner owner-gated |
| 2 | Proven for the demo |
| 3 | Proven for resulting state; tool run unproven |
| 4 | Unproven, owner-gated (no roster) |
| 5 | Partly proven (test account live in r9; live wrong-role denial needs a second account; unit test added) |
| 6 | Proven with a qualification |

## Validation

`python3 -m unittest test_auth` in `src/api` passes (test-only change, focused tier, no `rpi-checks.py` run). Hosted CI for the head was not observed (nothing pushed).
