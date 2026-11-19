# Changes: issue 130 live run 6

Refs #130. FOCUSED tier; documentation and tracking only, no `src/` edit.

## Files

* docs/reference/research/issue-130-live-r6-nomination-route-audit-2026-11-19.md (new)
* docs/reference/README.md (index sentence), docs/reference/log.md (entry)
* .copilot-tracking research, plan, details, critique, changes, review, state and evidence for 2026-11-19

## Validation

* `az containerapp show -g ama` (read-only): API --0000033, resident --0000014 Running; API digest unchanged.
* `src/core` unittest nomination_route, nomination_bootstrap, hazard_referral: 66 tests OK, 1 skipped.
* Not applicable: mypy, ruff, web tests (no source or web change); `rpi-checks.py --all` (not run by instruction).

## Per-criterion table

| Criterion | Result |
| --- | --- |
| Representative participation and comprehension (human evidence) | Unproven for the demo; cannot be code |
| Nomination keeps account, source, channel | Proven offline |
| Acknowledged route and named owner | Proven offline |
| Challenge or correction, evidence, reviewer, outcome | Proven offline |
| Correction re-reviews dependents only | Proven offline |
| Hazard route to #85 | Proven offline |
| Non-response and unknown never lowers priority | Proven offline |
| Wrong identity, limited authority, manual route | Proven offline |
| Live staff write | Not re-observed; run 5 saw 403 |
