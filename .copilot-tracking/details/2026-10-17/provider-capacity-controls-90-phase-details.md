<!-- markdownlint-disable-file -->
# Phase Details: provider-capacity-controls-90

Task 90, 2026-10-17. Parent plan: .copilot-tracking/plans/2026-10-17/provider-capacity-controls-90-plan.md.
Research C1-C7 and manager lane supply sufficient evidence; no actual operational authority.

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Complete | P01-T01, P01-T02; eight red failures before fixes; final exact semantics pass |
| P02 | Complete | P02-T01, P02-T02; 278 local/29 actual SQL Server tests; browser and quality gates |
| P03 | Delivered; Review Complete/Conformant | P03-T01; 19431ad pushed and PR #384 open; upstream integration/hosted CI remain owner follow-up |

<!-- rpi:phase id=P01 -->
## P01: Reproduce and enforce controls

<!-- rpi:task id=P01-T01 -->
### P01-T01: Failing-first tests

Target existing procurement suite and tiny temporary dataset. Prove versions are missing for booking/complete/withdraw, imported numeric-only evidence is wrongly trusted, invalid dates/scope and case advance bypass. Add actor/delegation/source/quota boundary tests, not just mocked calls. Record exact pre-fix results before source edits.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Domain/transaction implementation

Use `change_provenance._actor` prior art for current staff identity, and explicit `contract_authorities` records from trusted staff storage keyed to contract ref, version, reference and validity. No granting endpoint, wildcard or seed authority.

Final predicate: current named registered manager; trusted `contract_authorities` entry has reference/version, exact contract_ref and contract_version, revoked=false, inclusive effective dates, explicit actions, suppliers and scope_versions (optional explicit package_ids restriction). No wildcard or request-supplied delegation. Action matrix: create is draft-only, rescope/capacity/issue/reissue/appointment/complete/correct/withdraw require their corresponding action; advance preserves staff case progression permissions but requires a currently valid issuing-manager delegation for the booked order. Scope change also needs authority for the new scope version.

Capacity evidence names source version/date and review date, interval, unit `home-work-order`, exact case IDs and committed state; server binds package/supplier/contract/scope version. Unit means one home order over total package period, not slots or crew productivity. Validate strict whole counts, current review and source ordering; retain invalid legacy rows as unknown. Scope change invalidates prior capacity. Record actual reduction even below obligations and expose negative headroom.

Source resolution: source_case_id/document_id must resolve to an original, clean uploaded case document with exact source_version and verified stored content hash/bytes. Accepting manager is server-recorded with source/version, delegation/action/time; this attests the exercise user's acceptance, not legal signature verification. Current document/version/hash/scan must still match at progression. Replacement/missing/conflicting source blocks. Service-date clock is existing `_today`; source_date <= reviewed_on <= today, review age <= 7 days inclusive, future issue/review dates denied. Delivery interval endpoints inclusive and within package dates; future-effective commitments can be recorded but not confirm current work before the interval. Booking must be inside source/package delivery dates. Record zero/loss without needing positive commitment evidence.

Allocation matrix: issue requires used < committed; reissue/book/correct/complete require used <= committed for the existing counted order; completion retains consumption. Withdrawal releases allocation with named authorized action/reason/new version; withdrawn orders never reopen. Correction of completed work retains the same allocation. Advance selects exactly one Appointed current order for that case and requires latest appointment Booked, current scope/resident bindings, current issuing delegation and valid delivery date; it creates no reservation/order. Missing, ambiguous, withdrawn, issued-only, stale or deficit paths fail.

Use operation-local snapshot restoration; SQL rechecks actor and procurement-read dependency inside existing writer transaction before writes. Existing checked-document CAS handles concurrent quota changes. All order mutations snapshot state/appointments plus issuer email/name, delegation and capacity version; never mutate prior snapshots. Keep safety/resident/building decisions independent.

<!-- rpi:phase id=P02 -->
## P02: Existing surfaces and evidence

<!-- rpi:task id=P02-T01 -->
### P02-T01: API and capacity screen

Forward structured evidence in the existing capacity route. Extend existing labeled inputs, visible units/unknown state and evidence metadata without redesign. Display authority remains informational; backend checks every action. Add literal not-an-instruction marker to draft outputs without introducing a send route. Review changed web region against fresh guidelines and use local fictional browser.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Validation and documentation

Upgrade only coupled test prerequisites using explicitly fictional authority/evidence fixture helpers. Reuse opt-in SQL Server factory/wipe only on a newly task-owned local container on loopback random port. No existing DB/container touched. Run focused core/API, safety/resident/building, #78/#97 regressions and component lint/format/types at smallest covering boundary. Update component guides and existing KB synthesis/index/log with limits.

<!-- rpi:phase id=P03 -->
## P03: Review and publish

<!-- rpi:task id=P03-T01 -->
### P03-T01: Independent Review and publication

Activate rpi-review once. Criterion acceptance must cite executed exact tests, not operational evidence. Preserve actual findings and route later. Resolve gh authenticated user to privacy-safe local author/committer email, include required Copilot trailer, commit artifacts/code/docs, push named branch and create PR targeting main with Refs #90 and exact criterion evidence. No close/merge/rebase/force push.

## Execution Manifest (critique PC-004/005)

Canonical paths: src/core/src/zava_forward/core/{procurement,store,sqlstore,ai_tasks}.py; src/api/src/zava_forward/api/server.py; src/api/src/zava_forward/api/web/ops.js. Sources not generated; no edits to #78/#97 implementations. Tests: src/core/tests/test_quality_procurement.py (up to 18 new definitions/subtest families), src/api/tests/test_procurement_api.py (up to 5), src/api/tests/test_mssqlstore.py (up to 3, inherited behavior), plus at most 9 narrowly necessary fixture/helper/race definitions within total 35. Coupled fixture prerequisites in dataset/building_fixture/test_resident_decisions/test_hazard_referral only where existing positives require new evidence/delegation. No existing test removed.

Named semantic families: evidence_matrix, named_authority, full_quota_lifecycle, every_change_snapshot, deficit, advance_requires_booking, detached_reads, failed_save, concurrent_last_slot, advance_dependency_race, commit_authority_race, source_dependency_race, draft_review_no_instruction, own_order_http, capacity_http, lifecycle_http. Deterministic SQL interleavings replace first store save with second-store change followed by real save, so race occurs after validation before transaction recheck. Losing operation must leave durable and cached orders/versions/cases/success audit unchanged, then clean retry succeeds. JSON injected-save failure must restore memory and retain no success event; SQL audit failure must roll back document and versions.

Commands from root: `.venv/bin/python -m unittest discover -s src/core/tests -p test_quality_procurement.py -v`; `PYTHONPATH=src/core/tests:src/api/tests:src/agents/tests .venv/bin/python -m unittest test_procurement_api test_role_matrix test_resident_decisions test_hazard_referral test_buildings test_change_provenance test_bulk_edits test_bulk_edit_api test_form_staging test_form_staging_api -q`. SQL replay selects new MssqlProcurement/Api classes in existing test_mssqlstore harness, task-owned loopback container only. Per component: cwd src/core or src/api, `../../.venv/bin/ruff check <changed paths>`, `ruff format --check <changed paths>` honoring current exclusions, `mypy` with existing config; no exemption changes to hide errors. `node --check src/api/src/zava_forward/api/web/ops.js`. Browser: authenticate fictional manager, record sourced commitment through existing screen, issue/book at quota, verify versions; authenticate both contractors and verify only own order/denied writes. Inspect 320/390/1280 widths and keyboard labels/error status on changed capacity region. No screen-reader/human/WCAG conformance claim.

## Executed P01/P02 Reconciliation

Actual API/SQL imports require component cwd `src/api` and
`PYTHONPATH=tests:../core/tests:../agents/tests`; use that canonical replay,
not root module-name resolution where `test_buildings` is ambiguous.
Final local command selects test_quality_procurement, test_procurement_api,
test_role_matrix, test_resident_decisions, test_hazard_referral, API
test_buildings, test_sqlstore, test_mvp, test_change_provenance,
test_bulk_edits, test_bulk_edit_api, test_form_staging,
test_form_staging_api, test_ai_tasks and test_content_standard.
It ran 278 tests: 277 passed, one existing opt-in skip. A separate core-cwd
selection ran 114: 113 passed, one existing opt-in skip. Actual local SQL Server
MssqlProcurement/MssqlProcurementApi passed 29. No Azure target was used.

Implementation-time corrections preserve the plan: missing controller helper
import was caught by HTTP/browser replay; the coupled building HTTP positive
needed an evidenced booked order; JSON save/audit recovery was applied to
advance as well as direct order changes. No source test was removed and no
production delegation was introduced. Browser passed the specified loopback
journeys; changed-path lint/format, JS syntax and component mypy passed.
Current web guidelines were retrieved before implementation and refreshed
for changed-region review on 2026-10-17. Existing Fluent styles were reused.
The one independent Review is Complete with Conformant outcome and no
substantive findings. Implementation 19431ad and all dated phase evidence
were committed/pushed with private author/committer and required trailer.
PR #384 is open against main using Refs #90, without closure or merge.
GraphQL quota failure was resolved through ordinary REST PR creation.
GitHub reports mergeable=false/dirty versus concurrently advanced main
bab4bf3; no hosted runs registered for 19431ad at readback. Owner/coordinator
integration and hosted acceptance remain separate; no merge/rebase or second
Review was performed. Final parent action publishes the terminal evidence
snapshot and stops as explicitly requested.
