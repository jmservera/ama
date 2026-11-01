<!-- markdownlint-disable-file -->
# RPI Plan: Chat storage approval (synthetic-data demo)

* Task slug: chat-storage-approval
* Date: 2026-11-01
* Research: .copilot-tracking/research/2026-11-01/chat-storage-approval-research.md
* Details: .copilot-tracking/details/2026-11-01/chat-storage-approval-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-11-01/chat-storage-approval-plan-critique.md
* Tier: full for infra changes (live scope limited below)

## Phases

* [x] P1 Decision record, index, log, DPIA pointer.
* [x] P2 Bicep wiring (containerapps, main, main.test.bicepparam, resident-demo) and tests.
* [ ] P3 Commit, push, PR (Refs #163 only).
* [ ] P4 Live: back up config, dry run, `az containerapp update --set-env-vars` for the five settings on `ca-cutover-test-demo-api` and `ca-resident-demo` only; verify min replicas 0 and jobs Manual.
* [ ] P5 Playwright: employee chat stores a thread, second user isolation, unauthenticated 401. Resident chat: record that no storage exists.
* [ ] P6 Changes record, single Review, PR evidence.

## Constraints

No deletes, no RBAC, no networking changes; secrets never printed; SQL private (counts only through the in-VNet init job if needed); never push to main.
