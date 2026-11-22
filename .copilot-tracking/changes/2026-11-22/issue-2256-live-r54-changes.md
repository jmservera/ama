# Changes: issue 2256 live re-verification (revision 0000054)

Tier: focused. No src change; no rpi-checks run; no Azure change. Refs #2256.

## Files

* docs/reference/research/issue-2256-liveverify-r54-2026-11-22.md: verification note.
* docs/reference/research/issue-2256-liveverify-r54-2026-11-22/: probe_handoff.py, probe-handoff-result.json, screens/handoff-waiting.png, screens/case-ZF-2025-0030.png.
* .copilot-tracking/: research, plan, details, critique, changes, review and state for this run.

## Validation

* Live Playwright probe at 2026-11-22 23:34 UTC against ca-cutover-test-demo-api, revision 0000054 (active, Healthy, 100% traffic). Sign-in values read at runtime, never printed. No unit tests rerun: no src change.

## Per-criterion table

| Criterion | Status |
| --- | --- |
| A. Offered handoff (ZF-2025-0030) appears in the waiting list | Proven live: API 4 rows and screen lists ZF-2025-0029 to 0032 |
| B1. Chase owner shown | Proven live: Aadi Kapoor, matches the case card |
| B2. Due time shown | Unproven for the demo: seeded due_at is null, screen shows Unknown; no value invented |
| Waiting time (extra) | Partial: Unknown because offered_at has no timezone |
| C. Case card and waiting list agree | Proven: same open offer to Miguel Garcia in both |
| Deployed revision contains the fix | Proven by behaviour only; image digest not mapped to a commit |

Defect remaining: none in code. Residual: seed data lacks due_at and timezone-aware offered_at (follow-up).
