---
title: Issue 1262 queue browser result synchronization changes
ms.date: 2026-11-07
---

## Source changes (test-only)

* `src/api/checks/workbench_browser_check.py`: added `wait_queue_result(page, queue, expected, *, timeout_ms=None)`; imported Playwright `TimeoutError`; the queue loop and the later `overdue` reselection now call it instead of `wait_cases`. Every `check(...)` and the expected IDs are unchanged. `wait_cases` and its 29 other call sites are unchanged.
* `src/api/tests/test_workbench_live_defaults.py` (existing): added `QueueResultSynchronization` (4 tests): equal-count stale to overdue, equal-count empty transition (overdue, priority, unowned), timeout diagnostics, and a drift guard that `app.js` still contains the two status format tokens. It skips only when the Chromium executable is absent.
* Not changed: API, UI, ranking, policy, auth, SQL, infra, expected IDs, the failed receipt, old logs, any web file. The checker is excluded from ruff format by `pyproject.toml`, so no unrelated reformatting was applied (an explicit-file format run was reverted).

## Prospective evidence (VM scratch `/tmp/zf1262`, external, not committed)

* Environment: own venv, editable installs of `src/core`, `src/agents`, `src/api`, `ruff==0.17.1`, `mypy==2.4.0`, `playwright` 1.64.1 (repo pin 1.64.0; Chromium revision 1248 matched, Chromium 156.0.8078.4); `PYTHONDONTWRITEBYTECODE=1`; no uv, foreign tree or production-src PYTHONPATH shortcut.
* Admission: every browser command ran as `flock -n /tmp/ama-rpi-heavy.lock <command>` (lock file free beforehand; holder was this session's single command). No waits or duplicate jobs.
* Probe A (unchanged checker helpers on a constructed delayed-render page, in-page 300 ms timer standing in for the response-to-render gap): before, IDs `['ZF-1']`, status `... Work queue: stale.`; select control value `overdue`; after old `wait_cases(page, 1)` returned: IDs `['ZF-1']`, status `... Work queue: stale.`; eventually `['ZF-4']`, `Work queue: overdue.`. Exit 0. This reproduces the mechanism (the old wait is satisfied by the previous equal-count render) in a harness fixture. It does not prove what happened in the real failed R31 run and makes no product claim.
* Probe B (unchanged maintained journey `python -m checks.workbench_browser_check`, 2026-11-07, about 20:43Z): exit 0, 100 PASS lines, all five queue checks passed. The actual failure did NOT reproduce on this VM, so it is a timing-dependent race; the actual R31 observed IDs remain unknown and are not claimed.
* Red: the four new tests with `wait_queue_result` replaced externally by the old `wait_cases(page, len(expected))` behavior: exit 1, 3 failures (`['ZF-1'] != ['ZF-4']`; status still `Work queue: stale.`; `AssertionError not raised`), the drift guard passes. Log `/tmp/zf1262/red2.log`.
* Green: `python -m unittest test_workbench_live_defaults -v` exit 0, 7 tests OK, 0 skipped. `ruff check .` exit 0; `ruff format --check .` exit 0 (117 files); `python -m mypy` exit 0 (189 source files). Maintained journey with the fix: exit 0, 100 PASS lines, about 13 s. All exits are literal, not pipeline tails.

## Disclosures

* No `--all`, SQL, containers, builds or image work. No Azure, model calls, private data or human acceptance claims. Web-design-guidelines: no web file changed; not loaded (no changed web review scope).
* The green journey is not proof of the fix for a timing race; the deterministic delayed-render tests are the evidence.
