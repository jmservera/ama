<!-- markdownlint-disable-file -->
# RPI Changes: finance-96-98-99

## Metadata

* Task ID / slug: finance-96-98-99
* Date: 2026-10-27
* Plan: .copilot-tracking/plans/2026-10-27/finance-96-98-99-plan.md
* Details: .copilot-tracking/details/2026-10-27/finance-96-98-99-phase-details.md

## Execution Status

Complete for the full independent-slice plan: P01, P01-T01, P01-T02, P02, P02-T01, P02-T02. Approved-template/rule and actual Board functions remain blocked and excluded, not silently completed. Ready for the single independent Review, not whole-issue acceptance.

## Execution Summary

Implement working review notes, held draft diagnostics/manifests and missing-decision records. Source/HTTP changes remain within the plan's targets; no UI, AI, deployment or new financial authority.

## Completed Work

### Isolated field reviews and held manifests

P01-T01: src/core/src/zava_forward/core/form_review.py implements working review actions and pure diagnostic views. Existing unapproved schemas and staged candidates are reused; accept/correct/reject preserves prior values and named reviewer/reason/source, while controlled transactions retain rollback and current-actor writer rechecks. Pending/missing/infected/deleted evidence never triggers a hidden scan or historical disclosure. Same-case and exact-schema binding, raw acceptance, explicit typed correction, strict condition types, OR/Unknown semantics, field-scoped freshness and durable diagnostic snapshots are covered in src/core/tests/test_form_review.py.

Three held-decision records preserve missing Finance/template/rule and Board OD-12/15 authority with null inputs/evidence and owned correction paths. Acceleration is diagnostic Pause only, never a programme release gate, breach calculation or approval.

### Adapter and documentation integration

P01-T02 complete: the existing form handler exposes case form-review GET/POST and Store.detail strips both private review and held-decision keys before ordinary projection. Three added HTTP tests and the existing all-role inventory cover the route. Complete API discovery passes.

P02-T02 component docs, reference index and append-only log now state the actual working-review boundary and missing human inputs. Existing workflow/check names are unchanged.

## Implementation-Time Plan and Detail Updates

The single critique returned Revise. Directly applied PC-001 (no review-time scans), PC-002 (raw acceptance/explicit typed correction, exact typed conditions) and PC-003 (JSON single writer / SQLite rowversion protection). Original critique is retained, no repeat. These are engineering corrections, not new human financial decisions.

P02-T02's completion wording was clarified to documentation/pre-Review handoff. The automatic parent owns subsequent independent Review and publication, avoiding a circular requirement to complete Review before its implementation handoff. No behavior, acceptance scope or user decision changed.

## Validation Record

| Check | Scope | Status | Evidence |
| --- | --- | --- | --- |
| Initial system Python unittest | Existing form staging | Failed prerequisite | zava_forward not installed |
| pip editable core[dev], agents, api | External task venv | Passed | Installed with pip after missing-distribution failure; no manifests changed |
| Existing form staging | Core | Passed | 17 tests, 5.006s |
| New focused controls | Core | Passed | 9 tests, 6.735s, each backend exercised |
| Consolidated core regression | Forms, finance, grants, provenance, rescans | Passed | 199 tests, 63.263s; 54 opt-in SQL Server tests skipped, 145 executed |
| Ruff | All changed Python source/tests | Passed | Existing project configuration |
| mypy | Core module and new tests; HTTP form tests | Passed | Correct project cwd; 2 core and 1 API file checked |
| Complete API discovery | Requested caller command | Passed | 1124 tests, 599.297s; 314 existing optional skips, 810 executed, no failures |
| Changed documentation links/anchors | Four touched Markdown files' new sections | Passed | 5 relative links/anchors, diff whitespace clean |

Initial lint/type iterations found only formatting and harness typing issues: five overlong lines formatted, fixed tuple return annotation, and reran mypy from owning project so its relative source/test paths resolved. No untyped import blanket suppression was added; the narrow override permits calls to existing migrated untyped Store helpers only.

## Issue Acceptance Evidence

No GitHub criterion was ticked and none of these issues is closed.

| Issue / criterion | Evidence and result |
| --- | --- |
| #96: approved versioned schema | Blocked: register_schema still records Unapproved, no actual Finance/template/source-policy approval supplied |
| #96: candidate raw/source/hash/locator | Existing delivered foundation, preserved; 17 staging tests and new retained-lineage assertions pass |
| #96: accept/correct/reject preserves prior values/reviewer | Proven for sourced unapproved working value fields, both stores; no claimed approved-template/manual-anchor-free workspace |
| #96: field-specific unknown/conflict/fail | Partial: deterministic structural draft diagnostics pass; approved eligibility/calculation/unit/currency verification remains Not evaluated |
| #96: reviewed export never submits/implies eligibility | Blocked reviewed export; only clearly labelled Held diagnostic manifests exist, with no financial state writes |
| #96: exact dependent source/schema/rule invalidation | Partial: exact working-field source/schema freshness sets tested; rule/input/calculation/pack-review/downstream approval propagation not implemented |
| #98: field review changes only its field | Proven for working reviews: sibling-field and authoritative-case equality, retained staging and prior/new history assertions |
| #98: approved rules and reviewer-confirmed validation inputs | Blocked approved rules; structural conditions use only valid/current confirmed inputs, not unreviewed candidates |
| #98: pack links fields/evidence/attachments/template/input versions | Partial: matching links/versions are proven for Held diagnostic manifests, not actual approved application or claim packs |
| #98: Finance review history kept | Proven working history across JSON/SQLite reopen, audit/save rollback, and SQL writer conflict |
| #99: envelope/tolerances recorded as human-approved, not invented | Blocked actual approved inputs; durable Held records retain null approved inputs/evidence, owner/time and correction path |
| #99: breach produces human pause | Blocked actual thresholds/breach evaluation; signal is Pause for human decision on unknown authority, not a fabricated breach or programme release gate |

### Human Decisions Required

Finance/template owner must supply the actual approved versioned template, field/source authority, route, rules/calculations and reviewer designation (including unresolved OQ-015/earlier FD-01..14 proposal decisions). Finance/Board must supply OD-12's investment envelope integrated with asset plan, liquidity/covenant evidence and OD-15's approved downside limits, scope, control owners and restart authority. No named appointee, number, financial approval or production delegation is inferred. Dependent implementation/activation stops here.

### Validation Boundaries

No --all gate, Azure deployment, real inference, private-data inspection or secret/.env access. No heavy --changed gate has been consumed; the complete API units and targeted core/type/lint checks are the selected local validation, not a full publication-gate receipt. Browser, Azure SQL, operational/human acceptance and hosted CI are not claimed. Optional SQL Server tests skipped by their existing opt-in guards are reported as skipped, not passing.

## Pre-Review Reconciliation

Plan/details markers, completed-work evidence, handoff and validation are reconciled. No active implementation markers remain. Original critique Revise and all direct dispositions are retained. The only remaining blockers are explicitly excluded human financial authority; independent Review may assess this partial boundary. Ready for the single independent Review.

## Blockers

Finance/template/rule authority and Board OD-12/15. Independent work may proceed; dependent approval, reviewed export and affordability/breach/restart functions stop.

## Remaining Work

No remaining active implementation markers. Parent-owned independent Review, commit and draft PR publication remain.

## Follow-Up Items

Canonical plan Follow-Up Items: Finance/template owner supplies approved versioned template/source/rules/route/delegation; Finance/Board supplies actual envelope/downside limits and restart ownership. No figures inferred from case study or sector comparators.

## Return-to-Caller State

Implementation complete within independent boundary; automatic parent owns the single Review and draft publication. No issue acceptance claimed; human-dependent work stops.

## Parent Closeout After the Single Review

Review execution Complete; outcome Not accepted, with two reproduced Medium defects:
RV-001 permits historical values when source bytes are missing in schema-stale
or historical-only paths; RV-002 counts obsolete/unqualified candidates as
current conflict alternatives. The original Review is preserved at
.copilot-tracking/reviews/logs/2026-10-27/finance-96-98-99-review.md.
Both route to later rpi-implement work; no automatic fix or second Review was
performed. Earlier passing test evidence is retained but does not disprove
these findings. The broad missing-evidence non-disclosure and current-conflict
claims above are subject to these explicit defects, not accepted guarantees.

The one-pass loop is complete, not defect-free or whole-issue accepted.
Publish only the caller-requested draft PR, with Refs for all three issues,
original research/plan/details/critique/changes/Review/state, all local-check
results/skips and missing human decisions. No issue checkbox changes, reviewed
export, approval, activation or merge. Stop dependent work under the caller's
human-decision condition. Ranked follow-ups are the two bounded software fixes,
actual Finance/template authority, then actual Board OD-12/15 inputs.
