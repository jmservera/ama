# Issue 441 plan: accept resident portal ADR as ADR 0007

Details: [phase details](../details/2026-11-04-issue-441-adr-acceptance-details.md)

* [x] Phase 1: write `docs/adrs/0007-optional-resident-service-over-shared-case-authority.md` with Accepted status, decision, consequences, open decisions table and evidence boundaries.
* [x] Phase 2: copy diagram assets to `docs/architecture/` byte-identically and link them.
* [x] Phase 3: update BRD, PRD, architecture README and reference index; append log entry.
* [x] Phase 4: focused checks (links, ASCII, `tools/rpi-checks.py --changed`), review, commit, PR with `Refs #441`.

Critique (single, final candidate): the ADR must not claim criteria 5 or 9, must not overstate the demo exception as approval, must not supersede ADR 0004 or 0005, and must keep the proposal intact. Applied directly; no conflict with confirmed decisions.

Stacked slices: none needed. Remaining unmet criteria need the requirements owner's FR-044/AC-084 disposition and publication gates.
