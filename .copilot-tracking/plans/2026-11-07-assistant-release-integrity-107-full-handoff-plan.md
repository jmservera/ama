# Plan: FULL handoff for the #107 candidate

Research: [research](../research/2026-11-07-assistant-release-integrity-107-full-handoff-research.md). Details: [details](../details/2026-11-07-assistant-release-integrity-107-full-handoff-details.md). Critique: [critique](2026-11-07-assistant-release-integrity-107-full-handoff-critique.md).

## Decisions

* Exactly one normal (merge or single rebase, chosen then) integration of the eventual admitted fresh main; none now and none gratuitously.
* Preserve the test commit, all RPI records, skips and adverse outcomes. No new behaviour.
* No gate, SQL, browser, scanner or image service now; no push, PR, main move or criterion tick.

## Phases (not started)

* [ ] Phase 1: when the coordinator admits a fresh main, record its SHA and fetch; confirm the candidate is still source-identical.
* [ ] Phase 2: one integration, then light checks (ruff, mypy, 46-test selector from `src/api`, PYTHONDONTWRITEBYTECODE=1, pip-installed packages) and freeze.
* [ ] Phase 3: separately admitted FULL gate, then independent exact-head review and hosted gates.
