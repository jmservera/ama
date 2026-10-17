---
title: "fix(core): enforce evidenced provider capacity and controlled orders"
ms.date: 2026-10-17
---

## Summary

Closed actual control gaps in the existing migrated procurement, work-order
and case-advance paths. Retained the delivered API/screens, existing SQL
transaction helpers, named human instruction authority, resident commitments,
safety/building gates, #78 provenance and #97 forms.

## Changes

* Bound positive committed capacity to original clean uploaded bytes/hash,
  source version/date, current review, delivery dates, covered homes and
  `home-work-order` units. Offered, legacy and unknown capacity cannot
  authorize work; recorded losses expose deficits instead of fictitious
  availability.
* Required current named managers with explicit trusted contract/supplier/
  scope/action delegation. No self-granting endpoint or production authority
  seed was added. Existing allocation progression works at exact quota;
  alternate case advancement requires an evidenced booked order.
* Added immutable version/issuer/authority/state/appointment snapshots for
  every order change. Preserved contractor own-order reads and denied their
  package reads and all writes. Marked template/AI/review drafts explicitly
  not instructions without adding a send/award path.
* Reused SQL checked-document/writer locks, adding commit-time source,
  identity, delegation and procurement dependency checks. Added surgical
  existing-screen source inputs and local fictional regressions.

## Exact-Criterion Evidence

| #90 criterion | Executed engineering acceptance |
| --- | --- |
| No schedule/confirmation beyond evidenced committed capacity, not offered | Offered 9 / committed 1 admits one allocation and denies a second; unknown/legacy/source/version/hash/unit/date/scope/delegation failures deny; existing at-quota booking succeeds; advance bypass and deterministic SQL last-unit/source/authority races are blocked |
| Every work-order change has version + issuer | Issue, every appointment outcome, reissue, completion, correction and withdrawal retain sequential immutable snapshots; HTTP eight-version lifecycle and failed-write/rollback/reopen checks pass |
| System draft never instruction | Template note, persisted AI marker, review effect and UI copy remain explicit; draft acceptance never mutates procurement |
| Contractor read-only own orders | Two supplier identities, forged/foreign identity checks, package-read denial and every write-route denial pass; both contractor browser screens show only own orders |

## Validation

* Failing-first: original 21 procurement tests passed while four new root
  regressions failed eight times across JSON/SQLite before production edits.
* Exact domain/HTTP/roles: **63 passed**.
* Combined API-cwd preservation: **278 run, 277 passed, one existing skip**.
  Separate core-cwd building/procurement/resident/hazard: **114 run,
  113 passed, one existing skip**. These counts overlap; do not sum them.
* Actual local SQL Server 2022, standard existing harness:
  **29 passed** for MssqlProcurement/MssqlProcurementApi, including inherited
  domain/HTTP/race behavior. Only a newly task-owned loopback container was
  used; container and ephemeral credential were removed afterward.
* Local browser: source input, inline refusal/focus, keyboard save,
  issue/book at quota and new version, two contractor views/write denials,
  320/390/1280 reflow and reduced motion passed. External requests were
  blocked; zero page errors.
* Configured changed-path lint/format/types, both changed JS syntax checks
  and diff hygiene passed. Existing migration format/type exemptions were
  unchanged. An explicit-path format invocation bypassed old exclusions;
  the configured force-exclude replay passed and is documented.
* One independent post-implementation Review: **Complete / Conformant**,
  no substantive findings. One earlier plan critique returned Revise;
  PC-001..005 were applied before implementation.

## Dated RPI Evidence

All phase artifacts are committed under the same stable task identity/date.

| Artifact | Path |
| --- | --- |
| Research | [.copilot-tracking/research/2026-10-17/provider-capacity-controls-90-research.md](https://github.com/jmservera/ama/blob/feat/provider-capacity-controls-90/.copilot-tracking/research/2026-10-17/provider-capacity-controls-90-research.md) |
| Manager research instrument | [.copilot-tracking/research/subagents/2026-10-17/provider-capacity-controls-90-manager.md](https://github.com/jmservera/ama/blob/feat/provider-capacity-controls-90/.copilot-tracking/research/subagents/2026-10-17/provider-capacity-controls-90-manager.md) |
| Plan | [.copilot-tracking/plans/2026-10-17/provider-capacity-controls-90-plan.md](https://github.com/jmservera/ama/blob/feat/provider-capacity-controls-90/.copilot-tracking/plans/2026-10-17/provider-capacity-controls-90-plan.md) |
| Details and execution | [.copilot-tracking/details/2026-10-17/provider-capacity-controls-90-phase-details.md](https://github.com/jmservera/ama/blob/feat/provider-capacity-controls-90/.copilot-tracking/details/2026-10-17/provider-capacity-controls-90-phase-details.md) |
| One critique/dispositions | [.copilot-tracking/reviews/plans/2026-10-17/provider-capacity-controls-90-plan-critique.md](https://github.com/jmservera/ama/blob/feat/provider-capacity-controls-90/.copilot-tracking/reviews/plans/2026-10-17/provider-capacity-controls-90-plan-critique.md) |
| Changes/criterion acceptance/phase execution | [.copilot-tracking/changes/2026-10-17/provider-capacity-controls-90-changes.md](https://github.com/jmservera/ama/blob/feat/provider-capacity-controls-90/.copilot-tracking/changes/2026-10-17/provider-capacity-controls-90-changes.md) |
| One independent Review | [.copilot-tracking/reviews/logs/2026-10-17/provider-capacity-controls-90-review.md](https://github.com/jmservera/ama/blob/feat/provider-capacity-controls-90/.copilot-tracking/reviews/logs/2026-10-17/provider-capacity-controls-90-review.md) |
| Durable state | [.copilot-tracking/rpi-sessions/2026-10-17/provider-capacity-controls-90-state.json](https://github.com/jmservera/ama/blob/feat/provider-capacity-controls-90/.copilot-tracking/rpi-sessions/2026-10-17/provider-capacity-controls-90-state.json) |

## Scope and Readiness

This is local fictional engineering acceptance, not real company authority,
supplier commitment/signature verification, operational approval, live AI/
Azure SQL, financial commitment or full PRD/WCAG acceptance. Actual trusted
delegation remains the human contract authority owner's prerequisite;
deployment/UX owners must commission hosted/human/screen-reader acceptance.
JSON remains single-process with separate snapshot/ledger crash limitations.
No private dataset, paid AI, live provider order, award or payment was used.

The requested branch started from then-latest main adedf1f. Upstream advanced
one initializer/shared-KB commit to bab4bf3 during delivery. The initial
publication preserved the then-explicit no-merge/no-rebase direction.
The subsequent coordinator-authorized integration is recorded below.

PR #384 was created successfully through the REST API after the GraphQL
quota was exhausted. The original dirty/conflict readback was historical.
On 2026-10-17 the coordinator expressly authorized topic-only integration
onto freshly fetched main bab4bf3a2ac9ec030d78d27063d1390f800c5c7c.
`git rebase origin/main` produced integrated head
db83d4260e4f3d29fa80ce08624155ee4f59ecce before its evidence-only commit.
Only the append-only KB log conflicted. Exact byte checks proved the complete
upstream prefix plus the unchanged issue-90 entry, both README routing-row
sets, all twelve other upstream files exactly main, and byte-identical src
production/test/browser/documentation patches and original Review.
`git range-diff`, main ancestry and diff hygiene passed. No substantive
production conflict occurred, so no full-suite duplication or #84/#94
production-path rerun was warranted.

The final evidence commit records commands/base/integrated head and preserves
the original independent Review's historical Complete/Conformant result.
Topic-only publication uses an explicit force-with-lease expecting old
remote 6e4dbe18d111673b41049830eb68bf81f89051c8, never unconditional force.
External coordinator exact-head gating and hosted CI/rubric remain pending;
the original Review is not a fabricated new gate. No main rewrite, merge or
issue closure was performed.

* [x] Ordered Research -> Plan -> Implement -> Review and local evidence completed.
* [x] Exactly four issue criteria assessed; existing #78/#97 behavior retained.
* [ ] Hosted CI, including rubric scoring, completed successfully.
* [ ] Owner/coordinator accepted delivery and authorized issue closure.

## Related Issues

Refs #90. Parent #89 is hierarchy only, not an explicit dependency.
No issue closure or merge was requested or performed.
