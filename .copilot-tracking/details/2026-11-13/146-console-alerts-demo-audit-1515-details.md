<!-- markdownlint-disable-file -->
# Details: #146 console-alerts demo decision record

## Phase 2

* Insert `## Demo Routing Decision (bicep_146_routing)` in `infra/monitoring-runbooks.md` immediately before `## Issue Evidence and Gap Matrix`.
* Content: decision text; reason (`main.bicep` ledger alerts query `ContainerAppConsoleLogs`, `containerapps.bicep` `allLogs` retained); table AC1..AC5 with file:line proof and status, using the research table; deferred-to-production list (9c2a59f6, Action Group wiring and candidate activation, poison producer, privacy approval); statement that no deployment, cloud read or acceptance is claimed.
* Style: ASCII, `*` lists, no em dashes, no bolded prefixes.
* Update frontmatter `ms.date` to 2026-11-13.
* Add one sentence to the #146 paragraph in `docs/reference/README.md` (index, lines 347-353) and append a dated entry to `docs/reference/log.md`.
* Wording: source configuration preserved, not operation proven; defer Action Group delivery verification and activation, not source wiring; AC2 and AC3 unmet overall with partial source evidence.

## Validation

* `git diff --check`; re-run line-reference spot checks; tests and bicep already run, no source changes.
