<!-- markdownlint-disable-file -->
# Asset and board AI-unavailable state: plan (2026-11-03)

Task: `issue-226-ai-unavailable`. Refs #226. Research: [../research/2026-11-03-issue-226-ai-unavailable-research.md](../research/2026-11-03-issue-226-ai-unavailable-research.md). Details: [../details/2026-11-03-issue-226-ai-unavailable-details.md](../details/2026-11-03-issue-226-ai-unavailable-details.md).

* [x] Phase 1: add AI report status and without-AI rows to `assetCost` in `role-screens.js`.
* [x] Phase 2: add a unit test for unavailable and loaded states.
* [x] Phase 3: update API README, atlas trace row and knowledge-base log.
* [x] Phase 4: run focused unit tests, ruff, mypy; record changes and review.

Critique: executed once inline; verdict accepted. Risk: the shared `assetCost` also feeds two other screens. Mitigation: wording is generic and the rows add no claim. Risk: browser check phrases. Mitigation: no existing phrase removed; browser check not re-run. No user decision needed.
