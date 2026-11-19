# Issue 223 live demo changes (2026-11-18)

Refs #223. Tier FOCUSED (no source change). Added files: research note `docs/reference/research/human-review-effectiveness-live-demo-2026-11-18.md`, index and log entries, evidence under `.copilot-tracking/evidence/2026-11-18/issue-223-live/`, RPI artifacts. The per-criterion table is in the research note and repeated below at completion.

## Per-criterion table

| # | Criterion | Status | Basis |
| --- | --- | --- | --- |
| 1 | Seeded critical defects detected and prevented from satisfying a controlled gate | Partly proven (scripted competent panel only) | harness.json: 4 of 4, 0 uncorrected through gate. Not proven with a human or on the live app |
| 2 | Reviewer, source and reason retained | Proven for live path; real reviewer unproven | live_review_run5.json |
| 3 | Detection, corrections, effort reported against same workflow-only scenarios | Reporting proven; measurement unproven | Scripted units, no person-run sheet |
| 4 | Default acceptance and citation validity alone cannot pass | Proven offline | Default-accept and automation-bias panels fail |
| 5 | Automation-bias test; reviewer authority and evidence defined (OQ-017) | Test proven offline; authority unproven | No OQ-017 holder appointed |

## Validation

* `python3 -m zava_forward.agents.review_effectiveness --json`: passed true, 11 checks true.
* `unittest tests.test_review_effectiveness` (src/agents): 37 OK. `unittest tests.test_human_review_effectiveness_223` (src/core): 6 OK.
* Live Playwright run 5: see research note. Credential literal scan of evidence: 0 hits.
* Not run: mypy, ruff and rpi-checks (no source or Python under src changed); the evidence driver is not repository source. Hosted CI not observed (no push). Sloptrim detector not found, so prose was not scored.
* No Azure resource created; nothing to delete. No issue ticks made.
