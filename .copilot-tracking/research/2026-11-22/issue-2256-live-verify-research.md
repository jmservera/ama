# Research: issue 2256 live verification

Disposition: executed. Planning Readiness: Ready.

* Main check: fix a6c0910c97 (#2258, merged 2026-11-22T17:31Z) is in this base (2893d5098d). `handoff_ageing` uses `_optional_tz_instant`; regression tests exist in src/core/tests/test_handoff_escalation_83.py and src/api/tests/test_handoff_waiting_view.py.
* Prior record: .copilot-tracking/changes/2026-11-22/issue-2256-live-changes.md left live verification unproven (not deployed).
* Live: active revision ca-cutover-test-demo-api--0000053 (created 2026-11-22T19:38Z, after the fix merge), healthy. Probe at 23:02Z: /api/handoffs 4 rows, /api/handoffs/unaccepted 4 rows, screen lists ZF-2025-0029 to 0032 with chase owner and proposed receiver.
* Gap: due time shows "Unknown" because the seeded offers have no due_at; waiting shows Unknown because offered_at has no timezone. Status label on this screen is "Sent".
* Evidence: docs/reference/research/issue-2256-liveverify-2026-11-22/ (probe script, result JSON, screenshot). No secrets printed, no Azure change.
