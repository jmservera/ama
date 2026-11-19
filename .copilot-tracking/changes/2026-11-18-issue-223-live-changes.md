# Changes: issue 223 live audit

No source change; tier FOCUSED. Refs #223.

## Files

* Added `docs/reference/research/issue-223-live-r2-2026-11-18.md`; README row and log entry.
* Added evidence `.copilot-tracking/evidence/2026-11-18/issue-223-live-r2/` and the dated RPI artifacts.
* The state file `issue-223-live-state.json` was overwritten from the earlier run's version, as the brief names this path.

## Validation

* Offline gate: exit 0, passed true.
* `tests.test_review_effectiveness` 37 OK; `tests.test_human_review_effectiveness_223` 6 OK.
* Live Playwright run on `ca-cutover-test-demo-api`: 400 without reason, 200 with retained evidence, 400 on second review.
* Credential literal scan of evidence: no match. mypy, ruff: not applicable (no src change). `rpi-checks --all`: not run, by brief.

## Per-criterion table

| Criterion | Result |
| --- | --- |
| Seeded critical defects detected and prevented from satisfying a gate | Proven offline (scripted panel); unproven live and with humans |
| Reviewer, source and reason retained | Proven on live route (source label is a convention) |
| Detection, corrections, effort reported against workflow-only | Proven as reporting; effort scripted units, unproven as measurement |
| Default acceptance and citation validity alone cannot pass | Proven offline; not with live humans |
| Automation-bias test; reviewer authority and evidence (OQ-017) | Test proven offline; authority unproven |

Production-only or human-only: OQ-017 holders, human participants and paired measured effort, live-model defects, DPO and Legal.

## Residue

No Azure resource created. Two more synthetic AI records in the demo store.
