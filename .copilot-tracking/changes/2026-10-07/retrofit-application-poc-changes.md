<!-- markdownlint-disable-file -->
# RPI Changes: Proper Warm Architecture and PoC

## Execution Context

* Task ID: 4aaf9ee3-da69-4ebb-812a-edccc5637af7
* Task slug: retrofit-application-poc
* Scope: full plan P01-P04.
* Plan: .copilot-tracking/plans/2026-10-07/retrofit-application-poc-plan.md
* Details: .copilot-tracking/details/2026-10-07/retrofit-application-poc-phase-details.md
* Execution: implementation complete, automatic; one Review pending.
* Blockers: none for synthetic local implementation.
* Critique: executed once, Revise with PC-001-PC-009 directly disposed.

## P01/P02: Execution Started

Whole phases delegated with write-disjoint boundaries: P01 backend/src/tests/
manifest/package and P02 public UI. Parent owns P03 docs/container and P04
integration, validation, publication and review reconciliation.

## Immediately Relevant Plan Maintenance

Split architecture/container task into independent P03 so P02 is a coherent
whole UI phase; validation becomes P04. No scope/acceptance expansion, no
second critique. Evidence contract unchanged.

Clarified P04-T02 completion as publication and review-ready reconciliation;
the wrapper executes its one Review only after Implement completes. This avoids
a circular dependency on Review as an implementation prerequisite. No acceptance
scope changed; one critique/one Review contracts retained.

## Validation

Complete for the bounded synthetic implementation; measured evidence below.

## P02: Workbench Delivered

Frontend worker completed only public/index.html, styles.css and app.js.
Nine config-driven views, scoped metric drilldown, complete case panels,
sourced command fields, simulator/error/task paths and exact-envelope retry
implemented. Worker reports in-memory contract smoke passed; parent independently
ran `node --check public/app.js` and Git whitespace checks successfully.
Browser/server integration remains P04, not implied by static smoke.

Immediately relevant appearance update: activated web-artifact theme uses
Clawpilot CSS variables rather than draft teal accent. Civic workbench layout,
native typography, accessible labels/keyboard/reduced-motion intent unchanged.
No requirement, domain or authority decision changed.

## Created Resources

Downloaded base image `node:24.18.0-bookworm-slim`, verified digest
sha256:6f7b03f7c2c8e2e784dcf9295400527b9b1270fd37b7e9a7285cf83b6951452d,
325761777 bytes. No application data/code uploaded to registry. Docker objects
and port3410 collision checks found no existing target resources.
Azure and M365 resource creation not needed.

## P03: Architecture and Container Sources

Added local/target diagrams, authority/threat/failure/scale/cost boundaries,
all-twenty-criterion rubric gap challenge, app runbook and preliminary resource
ledger. Original/addendum/memory/snapshots and prior prototype untouched.
Created non-root read-only image definition with writable scoped volume,
loopback Compose publication and pinned base digest. Scoped CI exercises
Node tests/evaluation/syntax/container health and read-only runtime smoke.
Parent authored `scripts/verify-runtime.mjs`: all nine workflow cohorts,
filter/held-home/API/export probes and 100-request p95 threshold.
Compose configuration and Git whitespace check pass; runtime validation pending.

Parent added native Python Playwright `scripts/verify-browser.py`; `--help`
passes against installed Playwright. It uses rendered controls for filters,
denied gate, sourced update, cited/failure assistant, server commit followed by
lost response and exact replay, export, drilldown and mobile overflow. Optional
screenshots go to explicit session artefacts. Run awaits backend/container.

## Remaining Work and Review Readiness

P01-P04 complete, including publication P04-T02. One Review is next.
No implementation test blockers. Human operational release approval remains
unchecked; this bounded synthetic delivery does not satisfy those gates.

## P01 and P04-T01: Verified Application

Backend delivered domain/seed/store/assistant/server/evaluation, four suites
and exact scenario manifest. Parent reproduced all 39 passing tests and five
passing simulator fixtures. Container built locally, non-root user node, named
volume write/health and loopback-only port confirmed.

Real Python Playwright passes sourced command, hazard gate denial, assistant
draft/failure/task, commit-then-lost-response exact replay, export, metric
drilldown, search/reset, 390px reflow and zero page errors. First run's retained
JSON check used inner_text on hidden details; corrected to text_content.
Mobile min-content grid overflow was fixed with sidebar min-width:0.
Cross-site initial UI navigation was falsely rejected; restrict Fetch Metadata
to writes while retaining Host and Origin checks, with API regression assertion.

Restart preserved version12/event12/resident update on EX-HOME-900. Final
100-request localhost sequential sample p50 14.25ms/p95 28.55ms, target <=250ms.
No production load, real model or company-benefit claims.

Resource ledger records actual app image/container/volume/network and screenshots;
Azure/M365 creations remain zero. Screenshot files retained in session files.
App is intentionally left running and healthy for user use; no helper service.

## Publication Preparation and Owner Update

Final regression run passed all 39 tests, including cross-site GET navigation.
126 relative documentation links resolved before publication. Commit e9658bf
contains the bounded implementation. The updated base was merged without
rewriting history in 2204fa0; the sole log conflict preserved both upstream
rubric entries and appended this task's entry. Application code was unaffected.

The owner identified support/synthetic-data and explicitly requested a PR.
Exercised the existing generator with seed1341953496 and --dry-run: 980
candidates, 13 tables, 23528 rows, zero validation errors. No pack, ground
truth or existing synthetic data was overwritten. Nine constructed acceptance
fixtures remain distinct from the analytical pack; importing tracker records
as approved operational state is not authorised by generation. Documented the
generator path, reproduction and import boundary in the runbook/resource ledger.

## Publication and Review Handoff

Commits e9658bf, 2204fa0 and f953a8d pushed on the task branch; PR24 opened
against main: https://github.com/jmservera/ama/pull/24. No merge, force push or
history rewrite. All plan markers/details reconciled with measured validation
and actual resources. Hosted checks remain pending until observed.
One post-implementation RPI Review assesses bounded acceptance, not production
release or full PRD conformance. No repeated critique or Review is authorised.

## P05: Owner-Directed Completion

Owner explicitly requested continued autonomous implementation until complete.
Declared later scope is RV-001, preserving approved authority/stage contracts.
Plan P05-T01/details updated before source changes. Source boundary:
domain.mjs and domain regression, runbook/resource evidence and lifecycle state.
No production feature expansion, new resource, repeated critique or Review.
First add the missing regression and observe failure, then restore stage
consistency, verify all tests and owned runtime, publish on existing PR.

### P05-T01: Implemented and Verified

New regression first failed with handed_over vs expected quality_accepted.
domain.mjs now downgrades completed stage when new accepted quality evidence
invalidates separate handover. Regression checks immutable retained history,
invoice/update continuity, idempotent replay with no duplicate events,
denied premature advance and completed-count 1 -> 0 -> 1 after independent
handover reacceptance and explicit advance.

All 40 tests and five simulator evaluation fixtures pass. Existing owned
container rebuilt healthy without deleting/resetting its volume. Isolated
in-memory regression passed inside the actual rebuilt image; persistent
EX-HOME-900 remains version12/event12. Latest 100-request runtime sample
p50 27.44ms/p95 61.52ms, below 250ms. Ledger updated with actual image ID/size.
No additional resources or approvals; original Review preserved as historical
evidence. RV-001 is implemented by this later invocation, not a second Review.
