# Plan: issue 2186 full receipt across docs-only main moves

Tier: FULL (edits tools/rpi-checks.py, a gate tool). Local commit only; no push, no rpi-checks.py --all.

* [x] Phase 1: allow base_relaxation for full receipts when every moved path is inert (docs/, .copilot-tracking/, support/, markdown outside src/); any other moved path fails closed.
* [x] Phase 2: add tests in tools/test_rpi_checks.py (full relax accepted; code, tool, image, src markdown moves rejected; verify output line).
* [x] Phase 3: research note with per-criterion evidence, index row and log entry.

Details: .copilot-tracking/details/2026-11-21/issue-2186-live-details.md
