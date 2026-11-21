---
title: Issue 1830 live changes (2026-11-21)
ms.date: 2026-11-21
---

Tier: FOCUSED, documentation only. Added [docs/reference/research/issue-1830-live-r5-2026-11-21.md](../../docs/reference/research/issue-1830-live-r5-2026-11-21.md) and a log entry in `docs/reference/log.md`. No `src/`, `tools/` or workflow change; no live Azure; `rpi-checks.py --all` not run. Validation run: `python3 -m unittest tools.test_rpi_preflight tools.test_rpi_gate_timing -q` (56 OK), five preflight tests in `tools.test_rpi_checks` OK, direct Playwright reruns of the 320px reflow and map fullscreen checks. Throwaway files in /tmp removed. Hosted CI and exact-head review were not observed (no PR).

## Per-criterion table

| # | Criterion | State | Evidence and gap |
| --- | --- | --- | --- |
| 1 | Measured wall, queue wait, timing, critical path, high-cost and repeated checks | Partly proven | Ten full receipts (jobs 1, 2, 4) analysed. Unproven: queue wait for new runs (no log), same-head and base pair, growth versus host load, redundant coverage |
| 2 | Exact-selector preflight, rejects invalid, non-receipt label, #1297 320px, #1828 rerun | Proven for the demo | Selectors executed, zero or skipped or invalid fail closed, 320px check passes in 3.8 s and fails under a synthetic wide-element control, map check passes in 28.4 s. Gap: original #1297 commit not replayed |
| 3 | Tests, docs, benchmark method with before and after | Partly proven | Tests and README method pass; no optimization implemented, no before and after pair |
| 4 | Dated artifacts, tier, exact-head review, hosted CI | Partly proven | Artifacts and FOCUSED tier done; review by an independent party and hosted CI need a PR, not opened |
