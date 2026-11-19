# Changes: issue 223 live run 4

Tier: FOCUSED (documentation only; no src, SQL, security, infrastructure or deployment change).

Files: `docs/reference/research/issue-223-live-r4-2026-11-19.md` (new), `docs/reference/README.md` (index row), `docs/reference/log.md` (entry), RPI artifacts under `.copilot-tracking/`.

Validation: `tests.test_review_effectiveness` (src/agents) 37 OK; `tests.test_human_review_effectiveness_223` (src/core) 6 OK; mypy, ruff and rpi-checks not applicable (no executable change); links reviewed by diff.

| Criterion | Status |
| --- | --- |
| 1 Seeded defects detected and gated | Proven offline (scripted); unproven with humans |
| 2 Reviewer, source, reason retained | Proven offline |
| 3 Detection, corrections, effort reported on same scenarios | Reporting proven; measurement unproven (needs human) |
| 4 Default acceptance and citation validity cannot pass | Proven offline |
| 5 Automation-bias test; OQ-017 authority | Test proven; authority unproven (owner appointment) |
