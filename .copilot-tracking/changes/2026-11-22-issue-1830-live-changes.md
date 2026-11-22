---
title: Issue 1830 live changes (2026-11-22)
ms.date: 2026-11-22
---

Tier: FOCUSED, documentation only. Added [r6 research note](../../docs/reference/research/issue-1830-live-r6-2026-11-22.md), a README index row and a `docs/reference/log.md` entry. No `src/`, `tools/` or workflow change; no live Azure; `rpi-checks.py --all` not run; no pull request, so hosted CI and independent exact-head review were not observed. Validation: `python3 -m unittest tools.test_rpi_preflight tools.test_rpi_gate_timing -q`, direct preflight selectors, and direct Playwright runs of the 320px reflow and map checks. Throwaway files in /tmp removed.

## Per-criterion table

| # | Criterion | State | Evidence and gap |
| --- | --- | --- | --- |
| 1 | Measured wall, queue wait, timing, critical path, high-cost and repeated checks | Partly proven | Fourteen full receipts (jobs 1, 2, 4). Unproven: queue wait, same-head and base pair, growth versus host load, redundant coverage |
| 2 | Exact-selector preflight, rejects invalid, non-receipt label, #1297 320px, #1828 rerun | Proven for the demo | Selectors executed; zero, unknown and injection-shaped input fail closed; 320px passes in 4.2 s and fails under a synthetic wide-element control; map check passes in 29 s. Gap: original #1297 commit not replayed |
| 3 | Tests, docs, benchmark method with before and after | Partly proven | Tests and README method pass; no optimization implemented, so no before and after pair |
| 4 | Dated artifacts, tier, exact-head review, hosted CI | Partly proven | Artifacts and FOCUSED tier done; independent review and hosted CI need a PR, which the brief forbids |
