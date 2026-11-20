---
title: Issue 1830 live changes (2026-11-19)
ms.date: 2026-11-19
---

Tier: FOCUSED. Impact: `tools/` read-only analyzer and docs only; no gate semantics, permissions, images, packages or security control changed, no `src/` change. `rpi-checks.py --all` not run; no live Azure; no Playwright.

## Changes

* `tools/rpi-gate-timing.py`: `report --log` refuses an unreadable or empty log (exit 2).
* `tools/test_rpi_gate_timing.py`: one test for both cases.
* `docs/reference/research/issue-1830-live-20261119T1346Z-2026-11-19.md`, index entry and log entry.

## Validation

* `python3 -m unittest tools.test_rpi_gate_timing tools.test_rpi_preflight -q`: OK (the timing module has 16 tests).
* `python3 -m ruff check` and `ruff format --isolated --line-length 100 --check` on the two tool files: pass.
* mypy per `src/<project>`: not applicable, no `src/` change.

## Per-criterion proven and unproven

| # | State | Basis |
| --- | --- | --- |
| 1 | Partly proven | Timing for eight receipts and queue wait for four proven; no like-for-like pair, redundancy unproven |
| 2 | Unproven | Preflight refuses all selected execution pending owner trust boundary |
| 3 | Partly proven | Tests pass; no optimization, so no before and after |
| 4 | Partly proven | Artifacts and branch done; independent review and hosted CI need a PR (not opened) |

Full detail: [research note](../../../docs/reference/research/issue-1830-live-20261119T1346Z-2026-11-19.md).
