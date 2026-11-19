# Research: issue 1258 (run 20261119T161404Z)
Disposition: reused. Planning Readiness: Ready.
Issue #1258 has four ticked criteria (ancestor sync in `_confirmed`, `ranking_publication.py` lines 335-360;
committed_unconfirmed; syscall-order regression; retry/audit behaviour). Rerun of `test_ranking_publication*.py`
on this head: 110 tests OK.
Only unticked criterion: complete original RPI, FULL receipt, independent exact-head review, hosted checks.
Each needs a human, a push, or `rpi-checks.py --all`, which the brief forbids. No buildable code criterion remains.
Prior evidence: `.copilot-tracking/research/2026-11-19/issue-1258-live-research.md`.
