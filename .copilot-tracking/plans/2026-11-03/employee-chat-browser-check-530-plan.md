<!-- markdownlint-disable-file -->
# Employee chat browser check repair: plan (2026-11-03)

Task: `employee-chat-browser-check-530`. Refs #530. Research: [../../research/2026-11-03/employee-chat-browser-check-530-research.md](../../research/2026-11-03/employee-chat-browser-check-530-research.md). Details: [../../details/2026-11-03/employee-chat-browser-check-530-details.md](../../details/2026-11-03/employee-chat-browser-check-530-details.md).

* [x] Phase 1: give the chat log a minimum share of the panel (`src/api` web CSS).
* [x] Phase 2: align the shared browser checks with the stay-open employee chat (#568) and the four-attempt script budget (#812).
* [x] Phase 3: run focused unit tests, ruff, mypy and the employee leg of the browser and axe check.
* [x] Phase 4: record changes, review and follow-ups; keep criterion 8 unticked.

Critique: executed once inline; verdict accepted. Risk 1: weakening checks to go green. Mitigation: only assertions that contradict the owner-approved stay-open behaviour were changed, each with a comment, and external focus visibility is still asserted. Risk 2: CSS change shrinking the composer. Mitigation: the employee 320px, 390px and 1280px Send-in-viewport and axe assertions pass. Direct disposition: no conflict with confirmed decisions; no user decision needed.

Stacked follow-up slices (not in this PR): resident 320px composer layout (#520); live employee verification and agent-name confirmation (owner); remaining SQL selectors of the complete gate (coordinator).
