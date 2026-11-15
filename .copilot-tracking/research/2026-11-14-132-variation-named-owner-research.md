# Research: #132 variations and escalations reach a named owner (2026-11-14)

Disposition: executed. Planning Readiness: Ready.

## Evidence

* `gh issue view 132`: 5/6 ACs ticked; the remaining AC is "Variations and escalations reach a named owner and never act as a contract instruction". Owner comments (2026-11-09/11) authorise only the synthetic staff-mediated slice; no contractor portal, no new permissions, no actual contract instructions.
* `src/core/.../job_pack.py` `escalation()` already required an owner name and role, but accepted placeholder names (for example "Unknown - not configured", "TBC") and the `contract_instruction=False` flag was a literal that nothing enforced.
* `src/core/.../staff_intake.py` `escalation_destination()` returned "Unknown - not configured" with `configured=False` but no explicit owner-needed statement, and nothing routed a variation to that destination.
* `src/api/.../web/staff-intake.js` showed owner/role/contact and a note, with no explicit owner status or advisory-only line.

## Gaps

1. Placeholder or blank owners could be treated as named.
2. No enforcement that a variation record is never a contract instruction.
3. No routing helper that refuses when no named owner is configured.
4. UI/API lacked an explicit owner-assignment status and advisory-only guard.

## Cycle 1 correction research (1 of 5, 2026-11-14)

Source: independent exact-head review of `6a603370e` (verdict `request_changes`; Critical 1, High 2, Medium 1).

* Critical: `route_escalation` had no caller; `ACTIONS` and the generic `/api/workorders/{id}/{action}` POST route in `server.py` did not expose it, and nothing persisted. Case bodies (JSON store and SQL `cases.body`) persist the whole case record, and `_quality_operation` provides the existing rollback plus audit pattern used by `correct` and `acknowledge`.
* High: `named_owner` matched only a short placeholder list and the `unknown` prefix. The review cites `governance._looks_placeholder` and `_PLACEHOLDER_RE`; neither exists in this checkout (grep over `src/`), so the nearest comparators are the `_PLACEHOLDERS` sets in `synthetic/device_provision.py` and `synthetic/sensor_stream.py`.
* High (tests): only direct-Python calls existed; no HTTP, restart or fail-closed state checks.
* Not addressed here (out of the four listed items, routed): the staff-intake.js hardcoded advisory text, the escalation form and readback table, and browser coverage.
* Environment note: editable installs resolve to `/home/azureuser/source/ama`; tests need `PYTHONPATH` set to this worktree's `src/*/src`.
Disposition: executed. Planning Readiness: Ready.

## Cycle 2 correction (2 of 5)

Fixed independent cycle 1 findings: escalation summary held for roles without a recorded need (advisory note kept), staff-intake.js escalation form, readback and computed contract-instruction text, non-string and dotted-initial owner rejection, README and AC5 numbering. Focused core/api tests, ruff and mypy pass. Browser, SQL Server, human AT and hosted CI not run. Refs #132.
