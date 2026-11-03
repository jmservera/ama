<!-- markdownlint-disable-file -->
# Review: issue 572 r1 re-verification

Execution: executed once, self-review (not independent). Outcome: conformant for AC1-AC3 as re-verified by tests; AC4 open.

Evidence: [changes](../../changes/2026-11-03/issue-572-r1-reverification-changes.md), [research](../../research/2026-11-03/issue-572-r1-reverification-research.md).

| Criterion | Status | Evidence |
| --- | --- | --- |
| AC1 wired with flag and real execution | Proven by merged PRs; dispatch re-checked by tests | #575, #600; 81 gate tests OK; no new real Chromium run here |
| AC2 fail-closed skips | Proven | exact-pair skip tests pass |
| AC3 regression coverage | Proven | gate regression tests pass |
| AC4 fresh complete exact-head gate | Unmet | requires coordinator gate with Docker, MSSQL and Chromium |

Routed follow-up: the coordinator runs `python3 tools/rpi-checks.py --all` at the final exact head and verifies the receipt. Independent human review is not done. Use Refs #572, not Closes.
