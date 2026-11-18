# Changes: issue 130 live audit, run 4 (2026-11-18)

Tier: FOCUSED, docs and evidence only. No `src/` change; `rpi-checks.py --all` not run. Nothing created or changed in Azure, so nothing to delete.

## Files

* Added `docs/reference/research/issue-130-live-r4-nomination-route-audit-2026-11-18.md`.
* Updated `docs/reference/README.md` (index entry) and appended `docs/reference/log.md`.
* Added evidence under `.copilot-tracking/evidence/2026-11-18/issue-130-live-r4/` (probe scripts, JSON and raw outputs, image digest, offline test summary, two 1366 wide screenshots).
* Added RPI research, plan, details, critique, changes, review and state files under `.copilot-tracking/`.

## Per-criterion result (demo)

| Criterion | Result | Basis |
| --- | --- | --- |
| Representative participation and comprehension need authorized human evidence (unticked) | UNPROVEN; cannot be proven for the demo | Needs real representatives and residents; no confirmed authority in demo; person-run testing waived by owner; constructed checks cannot pass the gate |
| Nomination and self-referral keep account, source, channel | Proven offline; live write unproven | 66 core tests; live 403 |
| Acknowledged route and named owner before review | Proven offline; live owner list read | One staff owner listed |
| Challenge or correction retains competing evidence, reviewer, outcome | Proven offline; live write unproven | Route view 200, no records |
| Correction re-reviews dependents only | Proven offline; live unproven | Live write blocked |
| Hazard concerns route to #85 | Proven offline; route text read live | `test_hazard_referral` |
| Non-response and support needs never lower priority; unknown never none | Proven offline; partly live | Null hazard concern refused, not defaulted |
| Tests cover wrong identity, limited authority, manual route | Proven offline | 9 api tests |
| Nothing sent, booked or approved automatically | Proven live | No write succeeded |
| RAI challenge and correction criteria (ticked) | Read live only; offline tests | Panels render with no-sanction wording |

## Production-only items

OD-41 and OD-42 representative authority, real comprehension evidence, delivered staffed acknowledgement, appointed policy owner, Azure SQL nomination-specific coverage and whole-graph acceptance.

## Findings

* Image digest unchanged, new revision `--0000032`; the 403 "Reload your current staff identity" write refusal persists (`resident_decisions._operation`, FULL tier, redeploy needed).
* Form-encoded 400 is the JSON-only API, not a screen fault.
