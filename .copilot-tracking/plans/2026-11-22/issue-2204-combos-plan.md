# Plan: issue 2204 combinations live (2026-11-22)

Tier: focused (no src change; no rpi-checks --all). Evidence under `.copilot-tracking/evidence/2026-11-22/issue-2204-combos/`.

1. Insert temporary Contractor roster row for the test account oid (exec, SQL via managed identity).
2. Run `live_combos.py`: Contractor case (remove PM, assign Contractor, probe, remove); then ProgrammeManager baseline and PM plus each capability, one at a time; always restore ProgrammeManager.
3. Delete the temporary row; verify roster back to 2 rows and the assignment is ProgrammeManager only.
4. Write the research note `docs/reference/research/issue-2204-contractor-capability-combos-live-2026-11-22.md`, index and log entries, changes record, review, commit.
