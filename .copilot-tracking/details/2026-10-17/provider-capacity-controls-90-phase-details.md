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

## Coordinator-Authorized Integration

On 2026-10-17 the coordinator expressly overrode the earlier no-rebase limit
for this run-owned topic only. Clean old head/remote lease was 6e4dbe1;
fresh main is bab4bf3a2ac9ec030d78d27063d1390f800c5c7c. Rebase completed
at db83d4260e4f3d29fa80ce08624155ee4f59ecce before the evidence-only commit.
Only the append-only KB log conflicted; exact upstream prefix plus original
issue-90 entry and both index routing-row sets are retained. Exact src
patch parity and unchanged original Review were verified. No substantive
production conflict or full-suite rerun; coordinator external exact-head
gate remains forthcoming. Commands/base/head/validation and explicit lease
are recorded in changes. No main rewrite, merge, closure or invented authority.

## Authorized Correction ONE (2026-10-17)

Coordinator external Review of integrated 527a537 returned Revise, Medium:
new packages could persist an empty immutable contract version. Corrected
domain/API creation to require trimmed nonempty version; existing UI now
uses adjacent polite error/aria-describedby/aria-invalid and field focus
without a request/rerender or lost inputs. New omitted/empty/whitespace
regressions preceded fixes; valid version creates and later lifecycle still
works. Coupled positive fixtures now explicitly pass SYN-1 at creation.

Hosted failures also corrected without weakening contracts: exact existing
scenario-manifest fixture SHA-256 refreshed to dataset.py's bytes, with all
eleven/nine unavailable/provisional/proposed/no-approval fields identical and
validator unchanged; JSON/SQLite test_workflows safety positive now records
fictional source/delegation/booking after independent safety release, with
all original blocking/raiser/receiver/release assertions retained.

Executed: focused 107 pass; existing manifest/inventory 8/11 pass; full core
CI discovery 651 run/650 pass/one existing Azure SQL skip; full API discovery
shared by src-api/MVP CI/MVP validation 613 run/471 pass/142 existing opt-in
skips (141 SQL Server, one rendered opt-in). Separately actual local SQL
Server procurement domain/API inherited tests 31 pass and browser creation/
capacity/contractor journeys pass, including preserved input/field focus and
320/390/1280/reduced motion. Counts overlap. Task-owned SQL/credential cleaned.
Full configured lint/format/types, strict browser-harness lint/format,
JS syntax/compileall/diff pass; original legacy exemptions unchanged.

Changes records failing-first evidence, findings/dispositions and limitations.
No new RPI/Review cycle; original Review bytes unchanged and not promoted to
new source acceptance. External coordinator closure and hosted rerun remain
pending. Normal privacy-safe commit/push only, same branch, stop clean;
no rebase/force/merge/closure or actual professional authority.

## Authorized Post-#382 Integration Execution

The subsequent coordinator authorization supersedes the correction-only
no-rebase restriction solely for this owned topic. Fresh main
bbbc9243505b606550327c64bf5429243f457f2e; clean topic and exact remote
lease 5244f99db0a5b53f761b6c3a7bc5f1d9c4e829c1. Rebase completed at
7cf8df7b5ed67055dc6d40a95c554598b448c28e before integration edits.
Conflicts retained exact upstream KB prefix plus own entries, both SQL
validation hooks and both stock/procurement test classes.

Canonical upstream discard remains unchanged: disarm pending/transient
state, invalidate watermark and restore committed caches BEFORE reads.
Logical integration required procurement/advance recovery ownership alongside
stock, with original-exception identity and explicit uncertainty logging.
Eight recovery-fault subcases failed first (four failures/four errors).
Fixing ownership exposed committed checked-document snapshots lost on failed
reload (four errors); stage all document reads/decodes before publication.
Regression now checks both operations, pre-save and transaction refusals,
one-shot/persistent real SELECT failures, no leaked state/audit, fail-closed
reads, durable reopen and legitimate retry. The same test is inherited on
real SQL Server. No duplicate discard helper or finance topic imported.

Combined current-main finance budget/matching/approval/signoff, stock and
procurement tests plus affected API/workflows are the integration scope.
Original independent Review remains unchanged historical evidence, not
acceptance of this changed source; external exact-head closure still needed.

Final scope ownership includes BaseException cancellation, with a second
failing-first extension before the correction. Final twelve combinations
and legitimate withdrawal retry pass on SQLite and actual local SQL Server.
Source commit e2314a7c2ea0d6588b696030d153f29f74208dd7 on base bbbc924.
Final core combined194/no skips, affected API73/one existing skip, actual
combined SQL74/no skips, portability3, configured core/API lint/format/types
and preservation assertions pass. Logs retained session-locally; named
disposable SQL container/credential removed. Web and corrected fixture/hash
unchanged, so no redundant browser/full component suite. Changes records
full selectors/decisions and explicit expected-remote push command.
Terminal evidence commit is followed by authorized exact-lease publication;
final head goes in PR384 REST body/readback. No new Review verdict.

## Latest-Main Finance Advance and Final Combined Execution

Before publication main advanced to merged #94 d400eb8. Own evidence was
committed for a clean worktree, then the authorized topic-only latest-main
rebase continued. Additive docs/index/log conflicts retained both intents;
shared source retained all three validation hooks. Final source7c8965cf on
d400eb8 preserves canonical discard(pending), protected lock exit and
finance caller prior-audit recovery/logging exactly, plus stock/procurement
scope handling and staged checked-document snapshot publication.

Final combined core224 passed, API77 run/76 passed/one existing opt-in skip
including portability3, actual local SQL93 passed/no skips including merged
#94's existing19 finance checks, full configured core/API quality gates and
exact preservation assertions passed. Task-owned local SQL/credential
removed. No test deletion/skip to mask failure, weakened guard/validator or
professional authority invented. Original Review unchanged; no repeated
full RPI/Review. Changes records exact commands/base/source/head lineage.
Final evidence commit is documentation-only; exact publication head in PR384.
Same explicit expected-remote lease5244f99, only owned topic, stop clean.
