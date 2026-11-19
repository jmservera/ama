# Issue 1830 live r4 research

Opening note 2026-11-19. Scope: demo, desktop, FOCUSED, docs only. Prior: docs/reference/research/issue-1830-live-r3-2026-11-19.md.

Re-verification: 54 focused tests pass; preflight dry run still refuses selected execution (rc 5); receipt /tmp/rpi-1297-pyc-full-20261116T1530Z is absent; issue 1830 has no new owner decision (5 comments, last unchanged). Disposition: reused r3 evidence. Planning Readiness: Ready (docs-only record).

| # | Criterion | State | Reason |
| --- | --- | --- | --- |
| 1 | Measured wall time, queue wait, critical path | Partly proven | Analyzer exists; queue wait not recorded; reference receipt absent; no same head/base pair |
| 2 | Change-specific preflight, 320px and #1828 reruns | Unproven | Preflight refuses all selected execution (rc 5) by design; needs owner trust or isolation choice and FULL tier |
| 3 | Focused tests, docs, before/after benchmark | Partly proven | 54 tests pass; no optimization implemented, so no before/after |
| 4 | Dated artifacts, tier, independent review, hosted CI | Partly proven | Dated artifacts and focused tier done; review and CI need a PR, not opened |
