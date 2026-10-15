---
title: Role workbench IA 152 research
description: Focused evidence and acceptance boundaries for the shared src workbench
ms.date: 2026-10-15
---
<!-- markdownlint-disable-file -->

## Research Brief

Task identity: `152`, slug `role-workbench-ia-152`. RPI Agent executing the
user-requested full loop; output mode convergence, preparing implementation.
Research disposition: executed. Status: complete.

Research the current #152 criteria, owner updates, migrated API web layout,
server authorization, Fluent foundations and accessibility baseline. Audience:
implementer and PR reviewer. Non-goals: role-specific screens (#225 to #233),
client authorization, new deployment, private data, or owner device decisions.

## Research Parameters

Focused posture selected for the bounded caller scope. Evidence root:
`.copilot-tracking/research/2026-10-15/`. Initial internal areas: API web,
API role tests, PRD journey contract, ADR 0006 and parity matrix. External
areas: issue #152 and merged PR metadata only. Research changes evidence only.
No interaction is available; owner decisions and unavailable evidence will
remain open rather than being inferred.

## Extension Registry and Provenance

| Extension | Disposition | Scope |
| --- | --- | --- |
| `.github/copilot-instructions.md` | Selected, repository-wide | Topic branch, knowledge index/log, immutable memory/original case |
| RPI phase skills | Selected by explicit user request | One research/plan/critique/implementation/review loop |
| Accessibility skill | Selected | Keyboard, reflow, status and focus engineering checks |
| Research specialists | Skipped | One tightly coupled source trace; direct investigation |

## Direction Controls

* Only the specified worktree and `feat/src-role-workbench-ia-152`.
* New code/tests only in `src/`; `mvp/` receives no code.
* Reuse merged #150 foundations and accessibility baseline; no client role gating.
* No edits to `.env`, `.vscode`, memory or `.copilot-tracking/github-issues`.
* Pip only; no live inference/deployment or private operating data in tests.
* Commit research, plans, changes and reviews; PR uses Refs #152.

## Research Questions and Prior Knowledge Gate

| Question | State |
| --- | --- |
| Q1: Which IA work is authorized versus owner-only? | Issue read; device support remains owner-only |
| Q2: How do server scopes and navigation align? | Investigating server `/api/me` and endpoint permissions |
| Q3: How can reset, context and safety survive responsive simplification? | Investigating existing lists/case views |
| Q4: Which local evidence can establish layout without overstating acceptance? | Existing synthetic browser harness located |

Read original case, addendum, reference index/memory, sector primer, ADR 0006,
parity matrix and src README. Merged migrations #296 to #302 put web assets
in API package data. Existing design-system check uses a real loopback API
and constructed test data, not private working files.

## Research Cycle Log

### Cycle 1, Wave 1: Wider

Issue #152 retains five criteria after the src pivot. Device support and
cross-profile acceptance are not automatically decided by engineering widths.
Role-specific design is explicitly separate. Existing static navigation uses
client role checks and advertises broad queues. Existing browser harness
offers reusable real-app validation. Reflection: inspect server scopes before
choosing navigation; do not turn UI hiding into authorization.

### Cycle 1, Wave 2: Deeper

Server `/api/me` already owns projected identity; endpoint access comes from
`projection.allowed`, with additional Finance and manager checks. Use an
API-owned navigation descriptor based on those existing rules, not another
client role map. Preserve directory/overview access already permitted by the
server, explicitly distinguish those views from the signed-in user's queue.
List reset currently fails to restore sort, remains in all-cases scope and
rerenders focus to main. Case back links always return to mine, losing scope.
Safety detail appears after lengthy contact/return/handoff content.
Reflection: change presentation metadata and reset/context, not authorization.

### Cycle 1, Wave 3: Contrarian

Challenge: narrowing every endpoint to own cases would silently change existing
rights and harm cross-team safety visibility. Rejected. Hiding filters or safety
at mobile widths would reduce clutter at the cost of controls. Rejected.
Eleven PRD perspectives do not equal the eight implemented login roles:
do not invent identities/permissions. Record a bounded manifest with deferred
perspectives/workflows, rather than claiming full AC-043 coverage.

### Parent Synthesis and Re-entry

Accepted: server-described navigation, explicit scope, recoverable reset, early
safety detail, token-based wrapping and isolated synthetic browser checks.
Deferred: owner device/browser support, full eleven-profile/nine-workflow
acceptance, screen-reader/human validation and real-platform evidence.
No further cycle: all implementation questions answered; further evidence
requires owner/platform access outside this layout slice.

## Evidence Log

| ID | Source | Finding |
| --- | --- | --- |
| W1 | https://github.com/jmservera/ama/issues/152, retrieved 2026-10-15 | Five unchanged acceptance criteria; comments preserve shared IA scope and src migration |
| C1 | `docs/adrs/0006-src-layout-and-cutover.md:61` | Accepted src package placement and workload dependency boundaries |
| C2 | `src/api/src/zava_forward/api/web/app.js:73` | Current navigation construction uses client role branching |
| C3 | `src/api/checks/design_system_browser_check.py:246` | Existing isolated synthetic server launch pattern |
| C4 | `docs/prds/zava-forward-retrofit-programme-demonstrator.md:1480` | AC-034 reset does not change records; scope and zero-result explanations |
| C5 | `src/core/src/zava_forward/core/projection.py:58` | Existing default-deny endpoint access; no UI authorization |
| C6 | `src/api/src/zava_forward/api/server.py:265` | Projected identity response can carry navigation metadata |
| C7 | `src/api/src/zava_forward/api/web/app.js:312` | Current Clear filters does not restore sort or own scope |
| C8 | `src/api/src/zava_forward/api/web/app.js:357` | Case back link loses originating queue scope |
| C9 | `docs/reference/research/ux/zava-forward-prototype-profile-review.md:57` | Eleven research perspectives are not current auth roles |
| C10 | `.github/workflows/src-ci.yml:85` | Existing real-app browser check is run by src-api CI |

## Alternatives and Decision State

Selected server-described navigation, using existing permissions only. Client
renders descriptors and current-route state. Retain current contractor
projection/view behavior. Reject additional client role maps and any rights
expansion or reduction. No owner-supported devices or full journey acceptance
is inferred.

## Open Questions, Risks and Residual Uncertainty

Owner-supported device/browser matrix remains undecided. Real screen-reader,
human usability, live SQL Server/model/Azure evidence is unavailable locally.

## Planning Readiness

Ready for bounded engineering implementation. The full issue remains partial
until owner and cross-profile evidence gates are met. Research self-check:
scope, three ordered waves, alternatives, evidence IDs and residuals recorded.
Parent continuation: proceed to Plan under the explicit full-loop request.
