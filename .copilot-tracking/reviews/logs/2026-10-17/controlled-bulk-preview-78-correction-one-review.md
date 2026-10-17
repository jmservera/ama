---
title: Controlled Bulk Preview 78 Correction ONE Independent Review
description: Independent bounded correction assessment and exact finding disposition
ms.date: 2026-10-17
ms.topic: reference
---

## Scope and Independence

Explicit owner-authorized same-issue correction ONE, not a full RPI repeat.
Independent read-only `code-review` agent `issue78-correction-one-review`
assessed the uncommitted correction against source HEAD `9eba0b9`, including
bulk eligibility, every-target validation, SQL transaction integration,
regressions and documented provenance residuals. No nested review, source edit,
network/cloud/private-data/model activity or delivery by the reviewer.

The [original Review](./controlled-bulk-preview-78-review.md) is preserved
unchanged with its historical **Not accepted** verdict. This record does not
retroactively relabel it Pass or establish full issue #78 acceptance.

## Independent Report

Substantive findings: none.

RV-001: corrected. Immutable issued outcomes, empty failures, exact ordered
request/record coverage, complete snapshots and consistent permitted changes
are required. Mutable status reset cannot authorize blocked issuance. Every
target, including no-ops, is revalidated before staging and after
`BEGIN IMMEDIATE`, before writes. Source inspection found creator/actor/OID,
current permissions, freshness, issuance/consumption anchors and recovery/
atomic audit behavior preserved. Accepted handoffs remain permitted without
expanding fields or authority.

RV-002: remains partial. Documented upload/handoff implementations and API/UI
callers still lack required provenance inputs and complete per-change ownership/
evidence provenance. Explicit caller-contract and compatibility work remains;
the bounded correction neither resolves nor conceals that residual.

Reviewer verification: source, correction tests and SQL rollback/commit
integration inspected. Independently ran an in-memory synthetic eligibility
probe: two valid envelopes accepted and ten invalid envelopes rejected.
Did not rerun the parent's reported 71-test validation or lint/type checks.

Independent verdict: **ACCEPTED for the bounded correction only**. Full issue
#78 acceptance remains unmet.

## Finding Disposition and Remaining Acceptance

| Finding / criterion | Correction ONE disposition | Evidence / boundary |
| --- | --- | --- |
| RV-001 | Corrected; independent bounded acceptance | Anchored issued eligibility and every-target transaction revalidation; cached/persisted corruption tests preserve exact cases/history/success audit; no-op and active-state tests |
| RV-002 / criterion 1 | Unfulfilled, partial | Missing explicit source/version/reason caller contracts and complete evidence/ownership per-change events in existing upload/offer/accept paths; exact source locations in changes/details and component guides |
| Criterion 2, preview before apply | Bounded synthetic engineering evidence | Existing exact target/change/failure/outcome and no-preapply-mutation contracts retained; blocked issuance cannot be enabled by status reset |
| Criterion 3, no controlled approvals | Bounded synthetic engineering evidence | Same closed fields and current permission checks; no approval, ownership, resident commitment or hazard clock expansion |
| Full FR-005 / issue closure | Not accepted | Coordinator must route explicit existing-caller provenance work; no closure phrase or merge authorization |
| Live SQL Server / UI-human / operational acceptance | Not assessed | No live platform, UI change, browser/conformance or human approval claim |

Parent validation receipt: 71 focused synthetic tests passed: 39 core bulk,
six real local HTTP and 26 existing handoff/document tests. Full core existing
ruff check and format check (51 files), mypy (104 source files) passed. Those
are parent's executed checks, not reviewer-run checks.

## Authorized Main Integration Delta (not a new independent assessment)

2026-10-17 owner authorized rebase from published
`97cdc2a311b29d3ea65ac5fe2643a523302041d0` onto main
`92d4f89dd718befbde8bef00dd5cd6db2d99af39` after PR #377 merged.
Tested source head: `8602473a78930a72aa7fbb2d424a76d56dba5b53`.
Final integration commit adds only evidence/docs/lifecycle to that source.
No source change to either scoped module or its tests: bulk files are
byte-identical to the old publication, forms files to the new main.

Rebase resolutions retain both guides and KB histories, both endpoint
inventories and SQL `form_schemas` plus `bulk_edits` checked documents.
Store form-staging hiding and bulk wrappers, projection form rights and bulk
history redaction, API form routes/error handling and bulk routes/error
handling, all existing SQL safety/concurrency checks and bulk commit hook are
present together. Upstream durable pending/missing-rescan behavior is retained.

Parent integration validation: 110 joint focused forms/bulk core/API,
permission inventory, handoff and document tests pass. Core ruff/format53/
mypy106 and API ruff/format19/mypy49 pass. Both KB histories retain all ordered
lines and both indexes all table rows. No whole-suite repeat, browser,
cloud/private/model/live SQL evidence or actual schema authority inferred.

RV-001 remains corrected without a changed correction patch; RV-002 remains
unfulfilled and blocks full criterion 1 / issue acceptance. Actual approved
schema authority remains an unrelated human blocker. The original RPI Review
is unchanged. Owner reports external independent review `512a59c4` active on
the original published head; neither that active status nor this parent
integration validation is a final-rebased-head independent Pass.
Exact final commit is posted to PR #378 with old/base/source SHAs and this
delta. No new reviewer or RPI loop is launched; no merge is authorized.

## Correction TWO: RV-002 Source Disposition, Independent Reassessment Pending

Owner reports independent reviewer512a59c4 returned Revise on97cdc2a:
SQLite-reopened uploads lacked source/source_version/reason, audit was only
kind/filename, accepted handoff history lacked those fields, audit only named
prior owner and API callers supplied no provenance. Those are concrete
implementation gaps. The explicit correction TWO instruction supersedes the
earlier residual-only scope decision for these exact existing operations.
It does not supersede/falsify either historical review result.

| Finding / required evidence | Correction TWO source disposition |
| --- | --- |
| RV-001 immutable failed-preview eligibility | Unchanged scoped implementation; regression suite remains green |
| RV-002 upload inputs/history/audit | Implemented explicit caller source/version/reason, server actor/UTC/event version, exact before/after document-reference lists, identical full event in document_history and immutable upload audit, SQL reopen tested |
| RV-002 handoff inputs/history/audit | Implemented required source/version/reason/current handoff version in offer/accept API/UI/store, exact old/new handoff/ownership with registered actor/UTC/history version and identical audit; recipient-only acceptance preserved |
| Legacy missing request metadata | Refused with actionable required-field errors; new native forms collect inputs, never fabricate defaults from hashes/filenames/state; older stored records untouched/unknown |
| Permission/stale/atomicity | Fresh actor check at SQL commit, existing target rowversions and explicit handoff history version; denied recipients/revoked actor, conflicts, rollback/no ghost successes and lost-ack byte retention tested |
| Directly dependent forms | Existing pending/missing-rescan behavior retained; scoped forms implementation unchanged, fixtures explicitly supply now-required upload metadata |
| Full criterion 1 / #78 acceptance | Pending coordinator independent rereview of exact final pushed head; not self-certified or downgraded to an optional residual |
| Actual form authority | Separate unrelated human prerequisite; not used to omit source implementation |

Fail-before: seven new JSON/SQL tests, four accepted-missing-input assertion
failures and 34 missing-keyword-contract errors, not harness-loader errors.
After source/caller correction, full core609 (one skip), full API574 (111
opt-in skips) pass. Additional final edge cases covered in focused119 pass.
Existing core ruff/format55/mypy108 and API ruff/format19/mypy50 pass.
Local Chromium verifies explicit required-field focus/keyboard upload/offer/
accept, stale inline refusal with focused error/retained values, recipient
transfer, 390px/reduced motion and SQL reopen/history-audit equality; no page
errors or external requests. No cloud/private/model or live-platform claim.

Fresh guidelines retrieved before UI edits and again before scoped changed
UI review. `src/api/src/zava_forward/api/web/app.js:607` - pass for changed
form regions; existing owner-selected Fluent/native/plain-language rules
preserved, no whole-file WCAG/screen-reader or human acceptance claim.

This appended section is the implementer's finding disposition/evidence,
**not** an independent Review Pass. Original Not accepted file unchanged.
Coordinator owns required independent final-head rereview after push. No new
independent agent loop, issue closure, approval authority or merge.

Exact correction TWO source published:
`2e63cdf74a2f28d17e2cf3cbc993171755424fbb`, parent
`ae3adfb3f214ea3c30b073b2b71c074df4ec06ed`. Final receipt adds only
tracking evidence atop this tested source. PR378 records exact final SHA for
coordinator rereview. This source disposition does not replace historical
independent verdicts with Pass.

## Same-PR CI Maintenance After Reported Final Pass5676285

Owner reports independent Pass5676285 for all three criteria. This is a
reported final-head assessment, not a rewritten historical verdict or a new
finding cycle. Subsequent exact-head CI run39036057567/job117406113195
reproduced one test harness error in 113 tests: inherited MSSQL handoff
provenance reopen directly called SQLite SqlStore, which tried to seed its
unrelated empty local database from a deliberately absent file.

Test-only fix introduces backend-polymorphic `reopen_store`: SQLite retains
its existing constructor, MSSQL uses the repository's existing `factory`
without `wipe()`. Same nonexistent seed ensures retained server data is read.
All durable lineage/audit/ownership checks and 400/409/403 guards unchanged;
no skip added or actual server substituted. Local nine handoff/portability
tests and API ruff/format19/mypy50 pass. Mocked MSSQL factory/no-wipe routing
probe passes but is not a live-dialect claim. No configured opt-in disposable
server locally; final actual MSSQL CI remains a required gate.

Coordinator independent delta assessment is required for the exact new head
published on PR378. No new reviewer loop or self-certified Pass, merge,
rebase, force-push or main write. Prior published source5676285 is the parent.
