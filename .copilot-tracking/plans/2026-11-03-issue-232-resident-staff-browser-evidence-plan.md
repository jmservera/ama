# Plan: issue #232 resident-staff browser evidence

* [x] Phase 1: add scenario `232s` (service issue queue) with exact phrases and queue region checks
* [x] Phase 2: generalise `check_readonly_accessibility` with a resident-staff branch (text state, read-only statement, table regions, Tab reach, axe) and add 232, 232s to STORY_ACCESSIBLE
* [x] Phase 3: document stories 232 and 232s in `src/api/README.md`
* [x] Phase 4: focused validation (browser stories with pinned axe, ruff, mypy, related unit tests)

## Critique (executed once, inline)

* Verdict: proceed. Risk: weak assertions that pass vacuously. Mitigation: exact phrases and a Tab-reach comparison against every labelled table region. A speculative CSS-class assertion was removed after review.
* Validation tier: focused. No gate run.

Details: [details](../details/2026-11-03-issue-232-resident-staff-browser-evidence-details.md)
