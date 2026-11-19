---
title: Issue 1830 live changes
ms.date: 2026-11-18
---

Tier FOCUSED (no `src/` change; no gate, workflow or dependency file edited). Basis: docs and evidence only. Disclosure: the research note and index and log rows were drafted during the research phase, before the changes file existed; no source file was edited at any point.

Files: `docs/reference/research/issue-1830-live-20261118T1648Z-2026-11-18.md` (new), `docs/reference/README.md` (index row), `docs/reference/log.md` (entry), and the `.copilot-tracking/` artifacts.

Validation: `python3 -m unittest tools.test_rpi_preflight tools.test_rpi_gate_timing -q` on an export of unmerged candidate `a2c27fda6` in a scratch directory: 54 tests, OK. Timing reports from seven retained full receipts. Markdown link and diff review. mypy, ruff and `rpi-checks.py` were not applicable (no executable change). Azure and browser not used (not relevant to the local gate).

## Per-criterion table

| # | Criterion | Proven or unproven | Reason |
| --- | --- | --- | --- |
| 1 | Measured gate timing from multiple comparable receipts, critical path, cost and redundancy analysis | Unproven (partly evidenced) | Per-receipt wall, group, command, critical chain from seven receipts; no shared head or base, no queue-wait data, the 16 November receipt is gone, no redundancy analysis |
| 2 | Change-specific preflight; 320px regression caught; #1828 map check rerun | Unproven | Candidate refuses all selected execution; needs an owner-chosen trust boundary and FULL-tier source work |
| 3 | Focused tests, documentation, before/after benchmark; no control loosened | Unproven (partly evidenced) | 54 tests pass and the branch loosens nothing, but nothing is merged to main and no optimization or before/after pair exists |
| 4 | Dated RPI artifacts, selected tier, independent review, hosted CI | Unproven | Independent exact-head review and hosted CI belong to a pull request; none exists |
