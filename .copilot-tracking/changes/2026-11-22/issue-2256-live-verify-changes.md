# Changes: issue 2256 live verification

Tier: focused. No src change; no rpi-checks run. Refs #2256.

## Files

* docs/reference/research/issue-2256-liveverify-2026-11-22.md: live verification note.
* docs/reference/research/issue-2256-liveverify-2026-11-22/: probe_handoff.py, probe-handoff-result.json, screens/handoff-waiting.png.
* .copilot-tracking/: research, critique, plan, details, changes, review, state for this verification.

## Validation

* core tests.test_handoff_escalation_83: 13 OK. api tests.test_handoff_waiting_view: 10 OK, 4 browser skipped.
* Live Playwright probe at 2026-11-22 23:02 UTC against ca-cutover-test-demo-api, revision 0000053.

## Per-criterion table

| Criterion | Status |
| --- | --- |
| Offered handoff appears in the waiting list | Proven live: /api/handoffs 4 rows and /api/handoffs/unaccepted 4 rows; screen lists ZF-2025-0029 to 0032 including ZF-2025-0030 |
| Chase owner shown | Proven live (Aadi Kapoor for ZF-2025-0030) |
| Due time shown | Unproven: seeded offers have no due_at, the screen shows Unknown |
| Waiting time | Partial: shows Unknown because offered_at has no timezone; never invented |
| Regression test | Proven: tests above, from #2258 |
| Fix on main | Proven: a6c0910c97 in base |
| Deployed image contains the fix | Proven by behaviour only; digest not mapped to a commit |
