---
title: Issue 1830 live r2, preflight and timing tools re-created (2026-11-18)
description: Per-criterion proven and unproven table for issue 1830 after restoring the fail-closed preflight and read-only timing analyzer from the retained candidate
ms.date: 2026-11-18
---

Scope: synthetic demo, desktop only. Tier FOCUSED: `tools/` and documentation only, no `src/` change, no gate file edit, no live Azure, no Playwright (no web UI touched). `rpi-checks.py --all` was not run. The earlier audit is [issue-1830-live-20261118T1648Z-2026-11-18.md](issue-1830-live-20261118T1648Z-2026-11-18.md).

## What was restored

Five files from unmerged branch commit `a2c27fda6`, unchanged except two ruff ISC004 parenthesisations in the test file (the repository's default ruff configuration flags them): `tools/rpi-preflight.py`, `tools/rpi-gate-timing.py`, `tools/test_rpi_preflight.py`, `tools/test_rpi_gate_timing.py` and `docs/reference/method/rpi-gate-preflight.md`. The preflight keeps its fail-closed behaviour because the owner has not chosen a trust or isolation boundary (issue comment, 2026-11-16).

## Evidence

```text
python3 -m unittest tools.test_rpi_preflight tools.test_rpi_gate_timing -q
Ran 54 tests in 4.024s
OK

ruff check (4 files): All checks passed!
ruff format --isolated --line-length 100 --check (4 files): 4 files already formatted

python3 tools/rpi-preflight.py --python $(which python3) --test tools.test_rpi_checks --dry-run
NON-RECEIPT DEVELOPMENT FEEDBACK. Does not satisfy the full tier, review or hosted CI.
REFUSED (5): Refusing to run: selected tests, browser wrappers and browser checks execute repository-controlled code ... (rc=5)
python3 tools/rpi-preflight.py --python $(which python3) --browser-check src/api/checks/nonexistent.py --dry-run   (rc=5, same refusal)
```

Read-only analyzer on retained receipts (`rpi-gate-timing.py report`, chain seconds and command counts as the tool printed them):

| Receipt | Chain (s) | Commands |
| --- | --- | --- |
| 470-0001 (jobs 2) | 2788.0 | 217 |
| 470-2300 (jobs 2) | 2948.4 | 218 |
| g107-final-full-r1 (jobs 1) | 2865.4 | 205 |
| g1231-r35 (jobs 1) | 2926.9 | 204 |

The issue's reference receipt `/tmp/rpi-1297-pyc-full-20261116T1530Z/receipt.json` no longer exists. Receipts differ in head, base and suite size, so none of these figures is a before/after benchmark.

## Per-criterion table

| # | Criterion | State | Evidence and gap |
| --- | --- | --- | --- |
| 1 | Measured wall time, queue wait, per-command and group timing and critical path from multiple comparable retained receipts; high-cost, repeated and redundant checks; mandatory versus optimizable | Partly proven | The analyzer now exists in this branch and reproduces wall, concurrency, critical chain, longest commands and setup cost for four retained full receipts. Not proven: queue (lock) wait is absent from receipts; no pair shares head and base, so none is comparable; the 16 November receipt is gone; no redundancy or mandatory-versus-candidate conclusion is evidenced |
| 2 | Change-specific preflight with exact selectors, rejects zero-test and invalid paths, keeps SQL and browser prerequisites, non-receipt label; catches #1297 320px regression; reruns #1828 map check | Unproven | The preflight carries the non-receipt label but refuses every selected unit, browser and SQL run (rc 5), so it cannot catch the 320px regression or rerun the map check. Needs an owner-chosen trust boundary and FULL-tier source work, not provable for the demo |
| 3 | Focused tests and documentation for the preflight; benchmark method with before/after when an optimization is implemented; no mandatory group removed or control loosened | Partly proven | 54 tests pass; the method page is restored; no gate file is touched. No optimization was implemented, so no before/after pair exists |
| 4 | Dated RPI research, plan, details, changes, original review on an isolated branch; impact classified; selected tier run; independent exact-head review; hosted CI | Partly proven | Dated artifacts exist in `.copilot-tracking/` of this isolated worktree; impact classified focused (tools and docs only); focused tier run. Independent exact-head review and hosted CI need a pull request, which was not opened |

No criterion can be ticked.
