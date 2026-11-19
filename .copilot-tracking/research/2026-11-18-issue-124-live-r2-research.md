# Research: issue #124 live audit, second pass (2026-11-18)

Disposition: executed. Planning Readiness: Ready (updated at close of research below).

Scope: re-audit the three unticked criteria on #124 against repo docs, code and demo data, and look for any deployed surface (apps `ca-cutover-test-demo-api`, `ca-resident-demo`, Event Hub `evhns-cutover-test-demo`) that exposes Phase 0 discovery. Demo only, desktop, docs/evidence only, Tier FOCUSED. Earlier pass (artifacts `2026-11-18-issue-124-live-*`, note `issue-124-phase0-discovery-evidence-2026-11-18.md`) is preserved unchanged.

Questions:
1. Do the 59 core discovery tests and the probe still hold on current main?
2. Does any api, orchestrator, agents, importer or infra file reference the discovery modules, and does the deployed app serve one?
3. Do the BRD brief and the synthetic pack still agree with the contract counts?
4. Which part of each criterion is owner/person-only?

## Findings

* 59 core discovery tests pass; probe output identical to the first pass after normalising the worktree path.
* No consumer of the discovery modules outside `src/core` (`consumers.txt`); no api discovery route. Live authenticated GETs of candidate paths return 403, identical to an invented control path, so the live probe is inconclusive alone; the code search carries the proof.
* Azure read-only: api revision `--0000031`, resident `--0000012`, Event Hub holds only `sensor-readings`. Nothing created.
* Synthetic pack: 992 candidates, 9,859 events, 4 of 15 contract events unmapped, mixed ISO and dd/mm/yyyy dates.
* All three unticked criteria are owner/person-only for the real outcome; contract rules are proven offline.

Evidence: `.copilot-tracking/evidence/2026-11-18/issue-124-live-r2/`. Planning Readiness: Ready. Deliverable: `docs/reference/research/issue-124-live-r2-phase0-discovery-audit-2026-11-18.md`.
