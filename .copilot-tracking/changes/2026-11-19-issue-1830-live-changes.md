---
title: Issue 1830 changes (2026-11-19)
---

Tier FOCUSED: tools only, read-only analyzer; no gate file, runner semantics, security control or src change. No live Azure or browser use (no web UI touched). `rpi-checks.py --all` not run.

Changes: `repeated_commands` added to `tools/rpi-gate-timing.py report` (identical normalized commands run more than once, with runs, seconds, groups, setup flag; candidates only); one test in `tools/test_rpi_gate_timing.py`.

Validation: `python3 -m unittest tools.test_rpi_gate_timing tools.test_rpi_preflight -q` Ran 55, OK; ruff check passed; `ruff format --isolated --line-length 100 --check` clean. mypy not applicable (no src project modified).

| Criterion | State | Basis |
| --- | --- | --- |
| 1 wall, queue wait, per-command timing, critical path; repeated setup and redundancy candidates | Partly proven | Analyzer now reports all, including repeated commands (unit-tested). Not proven: no retained receipts share head and base; the 16 Nov receipt is gone; mandatory-versus-optimizable remains a policy call; no real-receipt run recorded |
| 2 executing preflight, 320px and map demos | Unproven | Preflight refuses selected execution until the owner chooses a trust boundary; FULL tier work |
| 3 tests, docs, before/after benchmark | Partly proven | Tests added; no optimization implemented, so no before/after |
| 4 RPI artifacts, exact-head review, hosted CI | Partly proven | Local dated artifacts exist; independent review and hosted CI need a PR (not opened) |
