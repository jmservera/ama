# Details: issue 1204 live (2026-11-27)

## Step 2

File tools/test_check_coordinator_handoff.py, assertions at the five `assertLess(<name>elapsed, N)` sites (about lines 1224, 1242, 1414, 1580, 1666, 1793). Add module constant near the imports and compare each elapsed value to it. Success: tests pass in 5 consecutive runs at load average above 8.

## Step 4

Research note with the evidence listed in the research artifact, per-criterion table, and the exact follow-up command: `python3 tools/check-tick-log.py --require-extended <session.db>` once a window records the extended columns. Update docs/reference/README.md index (if research notes are indexed) and append to docs/reference/log.md.
