<!-- markdownlint-disable-file -->
# RPI Changes: controlled-bulk-preview-78

Task 78, 2026-10-17. Scope: original P01/P02, authorized P03 correction ONE
and P04 correction TWO on the same PR.
Plan: .copilot-tracking/plans/2026-10-17/controlled-bulk-preview-78-plan.md.
Details: .copilot-tracking/details/2026-10-17/controlled-bulk-preview-78-phase-details.md.
Critique: one execution, Revise, six direct dispositions applied.

## P01-T01: Core implementation

Complete. Added bulk_edits.py with strict closed-field request validation,
server-owned previews, exact ordered changes/failures/outcomes, current
creator/registered staff/OID and owner/note rights, source/version/reason,
whole-case SHA-256 and SQL rowversion snapshots. Canonical issuance digest and
consumption anchored independently in immutable audit. Returned response is
deep-copied; mutable request/document and ABA/replay corruption tests pass.

Two thin Store wrappers call module functions rather than adding a new mixin;
this is local implementation judgment, not a field/authority change. SQL adds
one checked document and a commit-time validation hook inside existing save,
including current governance snapshot. All-case writes/history, audit and
terminal result commit together. Bulk-scoped exception recovery restores cases,
pending success events and all shared docs, including absence. Faults exercise
first-row, document, queue, audit, before-commit and lost-acknowledgement paths.

New tests contain deterministic two-store interleavings for competing applies
(including all-no-op), role revocation between preparation and transactional
validation, guardrail change, stale/ABA, reopen, immutable provenance equality
and every controlled category. Source/version/time/reason and monotonic case
edit history are retained; redaction explicitly removes nested history text
for viewers without existing need. Ownership/decisions remain unchanged.

## P02: API and delivery

Complete after P01. Added exact preview/apply routes, existing authentication
and CSRF, role-inventory entries, metadata-only rejected role/malformed input
audit and explicit storage-failure 503 with uncertain-outcome recovery wording.
Actual loopback HTTP tests check responsive health, exact shape, zero preapply
mutation, batch blocking, source history, replay, controlled fields, creator,
cached password/proxy revocation, OID rebinding and authenticated claim limits.

Updated component docs, existing UX synthesis, index and append-only KB log.
Full FR-005 acceptance remains partial for preexisting evidence-upload and
handoff-transfer operations outside the new bounded edit path; no closure
claim. No UI/source assets changed and no browser/conformance claim.

PR #377 remains open (head observed 7e1dbdd95f5b7abb0124cba0bee8b9a27146475a).
Actual overlap: shared DOCS tuple, thin Store wrappers, projection history
redaction, server routes, route inventory, component guides/pyproject and KB.
Changes are additive and forms.py/routes remain untouched; no dependency,
merge, rebase or nested delivery assumed.

## Validation

System Python could not import zava_forward. Created own .venv and installed
editable core/agents/api and declared dev extras. No private datasets/cloud.

* Fail-before core: 25 tests, 2 failures/91 subtest errors, missing bulk methods
  and missing rejection audit; expected nonzero verified before implementation.
* Fail-before API: 5 tests failed with missing routes; health helper initially
  used wrong path/JSON assumption, corrected to actual text `/healthz`.
* New core/API contracts: 37 tests passed before final additional HTTP case.
  Final new core count 32; final API count 6, all passed in focused selections.
* Broader targeted selection: 172 attempted, 171 passed and one loader error
  (`tests.test_mvp` namespace missing in invocation of test_mssqlstore).
  Corrected PYTHONPATH to include src/api and reran only that module:
  51 tests, 3 passed/48 opt-in live SQL Server skipped, no live connection.
* Final new contracts + sqlqueues/handoff HTTP: 54 passed. Existing handoff
  fixture emits expected unavailable-law-store diagnostics; no rule approval
  or passed rule-engine claim is inferred.
* Final API and complete role inventory after malformed/storage-failure case:
  25 passed (6 new HTTP plus 19 role inventory checks).
* Existing core `ruff check .`, `ruff format --check .`, `mypy`: pass,
  51 formatted and 104 typechecked source files. API equivalent: pass,
  18 formatted and 48 typechecked files. Typed new modules/tests retain strict
  checking; narrowly scoped untyped-call overrides match existing Store boundary.
* `git diff --check`: pass. Added documentation links reviewed against exact
  paths/heading anchors. KB log only appended; memory/original untouched.
* No full test suite, cloud/Azure/paid model/Docker/private dataset used.

## Criterion Evidence

| Criterion | Evidence | Boundary |
| --- | --- | --- |
| Edits retain source/version/actor/time/reason | test_exact_preview_before_apply_and_provenance_reopens, exact hash-chain event/history equality, monotonic versions and projected history | New closed-field path; broader preexisting FR-005 remains partial |
| Targets/change/failure/outcome before apply | mixed missing/foreign/valid, no-op/mixed-no-op, closed/inactive and actual HTTP exact-shape tests | Backend API only, no new UI acceptance |
| No controlled approvals | All controlled categories and unknown/nested keys rejected, ownership/decisions/commitments unchanged, actor/OID/guardrail concurrency checks | Fictional local exercise, not operational approval |

## Review Handoff

Ready. Full plan markers and details synchronized, critique executed once and
six direct dispositions complete, no implementation blockers. Perform exactly
one post-implementation Review. Route any findings forward; do not repeat
implementation/Review in this task. Then privacy-safe commit, push and main PR
with Refs #78, exact criterion evidence and explicit outstanding boundaries.

## Correction Cycle ONE: owner-authorized continuation

2026-10-17: same issue #78, PR #378 and requested branch. Clean status and
draft/open PR head 9eba0b9 verified. Original Review remains Not accepted;
the prior source-fix stop is superseded by explicit user authorization.
P03-T01 in progress: fail-before status-corruption regressions, immutable
eligibility and complete target revalidation. P03-T02 investigates actual
older provenance gaps without inventing human inputs. P03-T03 requires one
independent correction assessment, verified commit/push and stop.

### P03-T01: RV-001 correction and fail-before evidence

The status-only regression was added before source edits and run against the
original implementation. All four cached/persisted SQL x changed/no-op
subtests failed with `AssertionError: ConflictError not raised`, reproducing
the real defect rather than a loader/dependency error. Raw local receipt:
`ama-78-correction1-fail-before.log` in the session files directory. The cached
store is refreshed between persisted subtests to avoid a stale meta-snapshot
fixture conflict, discovered on the first post-fix run.

`bulk_edits._applicable_request` now derives applicability from the anchored
issued envelope, requiring exact ordered unique target/record agreement,
complete snapshots, empty failures, exact requested old/new field shape and
new values, and consistent `would_apply` or `no_change` outcomes only.
`blocked`, `batch_blocked`, any failure and malformed/incomplete coverage are
never made eligible by mutable status. Existing issuance hash and durable
consumption anchors are retained and repeated in the SQL writer transaction.

Shared `_changes` generates preview fields and validates the exact proposed
old/new changes. Both staging and SQL commit iterate canonical request IDs,
revalidate every target's permission/rules/freshness and compare issued changes.
No-op targets are checked but receive no invented edit/history; active handoff
Offered/Received/Escalated/Accepted semantics are preserved. No allowed field,
permission, route, schema or controlled approval was added.

New tests cover all four original corruption cases with exact unchanged
cached/reopened cases/history and success-audit list, visible refusal and
verified hash chain; inherited contract-shape/outcome cases on both stores;
all active states/no-ops; actual transaction-bound every-target checks including
no-op; and an independent direct SQL commit-hook refusal of genuine blocked
issuance. Existing request/issuer hash tampering, stale/ABA/role/OID/guardrail
races, atomic rollback/reopen, lost acknowledgement and replay remain covered.

### P03-T02: RV-002 exact residual and validation

PRD FR-005 at `docs/prds/zava-forward-retrofit-programme-demonstrator.md:840`
requires source/version/actor/timestamp/reason for each change. Inspection:

| Operation / caller | Already retained | Exact unfulfilled scope |
| --- | --- | --- |
| `Store.add_document`, `store.py:583-610`; upload route `server.py:822-827`; UI `app.js:794-798` | Content SHA-256, version 1, display-name/date metadata, separate email/time upload audit | No supplied source reference/version or change reason in API/store signature; no complete immutable per-change provenance event binding them |
| `offer_handoff`, `workflows.py:159-210`; `_handoff_event:211-225`; API `server.py:783-790`; UI `app.js:659-662` | Versioned sender/receiver snapshots, actor email/role/time, note and permitted handoff metadata | No explicit source/source-version contract; offer note is not a required general provenance reason |
| `accept_handoff`, `workflows.py:227-239`; API `server.py:791-792`; UI `app.js:622` | Recipient-only owner transfer; versioned from/to history, actor/time/role and acceptance audit | Empty-body acceptance has no reason or source/version input and no canonical old/new owner event containing the full provenance contract |

This cannot be completed by simply retaining currently supplied inputs.
Requiring new inputs affects existing UI and API clients and needs a deliberate
validation/history/compatibility decision. Do not fabricate sources from names,
relabel history versions as supplied source versions or invent an acceptance
reason. RV-002 remains unfulfilled; #78 criterion 1 remains partial. Coordinator
must route the exact existing upload/offer/accept caller contract and immutable
provenance work before claiming full acceptance. No unrelated partial source
patch or broader bulk fields are substituted for that requirement.

Validation: 71 focused tests pass using only temporary synthetic fixtures:
39 core bulk + six real local HTTP + 26 existing handoff/document tests.
Existing core ruff checks pass; format checks pass on 51 files; mypy passes
104 source files. Diff whitespace checked. No full suite repeat, live SQL
Server, cloud, private stock, Docker or model. No web code change; UI caller
inspection is evidence for scope only, not a design review/browser acceptance.

### P03-T03: Independent correction review

Independent read-only reviewer `issue78-correction-one-review` found no
substantive defects and accepted the bounded correction only. It inspected
core source/tests, SQL transaction/recovery and documented RV-002 residual,
and independently probed two valid and ten invalid synthetic issuance
envelopes. Parent's 71-test/tooling receipt is distinguished from reviewer
execution. The separate dated correction review records complete disposition;
the historical original Review file and Not accepted verdict are unchanged.
RV-001 is corrected; RV-002 and issue criterion 1 remain explicitly partial.

### Correction ONE publication receipt and stop

Source commit `dd52ae3a9ab0aee2ff96cda7e7496c3de29a58ec` pushed normally
to the same requested branch and verified via PR #378 `headRefOid`; clean
worktree after publication. PR remains draft/open, main-targeted, Refs #78,
no closure or merge authorization. Body now records exact criterion evidence,
corrected RV-001, independent bounded acceptance and unfulfilled RV-002 caller/
provenance work. Original Review and failing contract evidence remain intact.

Authenticated GitHub account was re-resolved as id 8036360 / jmservera;
repository-local noreply identity used for author and committer, with required
Copilot trailer. Final receipt changes only current lifecycle/publication
records. No source changes after independent assessment, integration with
#377, merge, rebase, history rewrite or force-push. Stop after final receipt
push; coordinator owns remaining provenance scope and eventual integration.

## Authorized integration onto merged #97 (same PR #378)

2026-10-17 owner explicitly authorized rebasing the topic from published
`97cdc2a311b29d3ea65ac5fe2643a523302041d0` onto latest origin/main
`92d4f89dd718befbde8bef00dd5cd6db2d99af39`, which includes merged PR #377.
This is same-delivery integration, not a new RPI/correction loop.

Rebase source head is `8602473a78930a72aa7fbb2d424a76d56dba5b53`.
Five conflicts resolved additively: both component guide sections, both
append-only KB log entries, complete forms/bulk endpoint inventory and SQL
DOCS containing both `form_schemas` and `bulk_edits`. Auto-merges inspected
for both Store entrypoints, projection protections, API routing, component
type overrides and SQL validation hooks. Separate `forms` and `bulk_edits`
modules retained. Upstream forms module and both form test modules compare
byte-for-byte unchanged to main, including durable pending/missing-rescan fix.

`git range-diff e065ecd..97cdc2a 92d4f89..8602473` maps original commits:
1bd60e3 -> f1831a8 (additive conflict resolutions), 9eba0b9 -> 0b236c4
(identical patch), dd52ae3 -> d6c4295 (identical RV-001 correction patch),
97cdc2a -> 8602473 (identical receipt patch). Independent external review
`512a59c4` is reported active by owner on the original publication; it is not
claimed to have accepted this rebased SHA. Final delta/SHAs will be published
for that review, not replaced by a new review loop.

Joint focused forms/bulk core/API, endpoint permissions, handoff/document
rollback/reopen regressions and existing core/API tooling pending.
RV-001 correction evidence remains intact; RV-002 is still unfulfilled and
criterion 1 partial, not downgraded. Actual approved schema authority remains
an unrelated human blocker; neither integration nor synthetic tests supply it.

### Integration validation and finding disposition

One joint invocation passed 110 tests:
`test_form_staging test_form_staging_api test_bulk_edits test_bulk_edit_api
test_role_endpoint_inventory test_handoff_lifecycle test_documents`.
This covers durable pending/missing-rescan forms across repeated reads and SQL
reopen; schema registry/body/audit fault and cross-process rollback; current
permissions and route inventory for both features; blocked-status cached/
persisted RV-001 corruption, no-ops and all-target transaction checks; bulk
stale/ABA/role/OID/guardrail races, concurrency, rollback and lost-ack reopen.
Existing law-store-unavailable fixture diagnostics remain explicitly unknown
rule checks, not a failed suite or a rule-pass claim. Local raw receipt:
session files `ama-78-integration-focused.log`.

Existing component checks pass without dependency changes/install:
core ruff, format 53 files, mypy 106 source files;
API ruff, format 19 files, mypy 49 source files. Diff whitespace passes.
Automated preservation check confirms complete old/main KB log lines are
ordered subsequences and all table rows from both indexes remain present.
`forms.py` and both forms tests are byte-identical to main; `bulk_edits.py`
and both bulk tests are byte-identical to old publication. SQL retains existing
safety validators/checked-document concurrency plus bulk commit validation;
no unrelated validator or form registry is replaced.

RV-001 corrected implementation and its fail-before/independent bounded
assessment survive integration unchanged. RV-002 remains **unfulfilled and
blocking full criterion 1 / #78 acceptance**, not downgraded to optional work.
The actual approved-schema authority blocker belongs to #97 and is neither
caused nor satisfied by this integration. Original Not accepted Review remains
unchanged; no final-head independent Pass is inferred from prior assessments
or active review512a59c4. No new review or RPI loop invoked.

Publication uses a single explicit topic-only force-with-lease, expected remote
old head `97cdc2a311b29d3ea65ac5fe2643a523302041d0`, never an unrestricted
force or main write. Final evidence commit is artifact-only atop tested source
`8602473a78930a72aa7fbb2d424a76d56dba5b53`; exact final head and old/base/source
delta are supplied on PR #378 for the active independent reviewer. PR remains
draft, no merge or closure. Stop at final push/readback.

## Correction TWO: explicit RV-002 implementation authorization

2026-10-17: owner reports independent review512a59c4 Revise on97cdc2a
because full criterion 1 is unmet. Owner explicitly requires completing
existing upload/offer/accept caller/API/UI metadata validation and immutable
old/new events. Earlier residual-only disposition is superseded for these
operations; it is not a human-approval blocker or permission to omit the fix.
Rebase is already complete and clean at ae3adfb on main92d4f89.

Bounded correction TWO, final allowed cycle: fail-before metadata/reopen/audit
regressions, required explicit source/source-version/reason, handoff-version
stale refusal, exact document-reference and ownership changes, fresh actor/
transaction protection and rollback, directly dependent fixtures/callers,
accessible native UI paths and local browser check. No new bulk fields or
controlled approvals, defaults or invented historical provenance. Preserve
forms/rescan and RV-001. Required web skills loaded and current guidelines
fully fetched before edits; Fluent/native semantics/plain-language baseline
prevails over unrelated visual suggestions. No redesign/framework switch.
Original reviews remain historical, coordinator must independently reassess
the final head. No cloud/private/paid model, merge or new RPI loop.

### P04-T01: Failing-Before and Source Correction

New `test_change_provenance` ran before production edits: seven tests yielded
four failures (missing metadata accepted) and 34 errors (missing metadata
keyword/signature contract), with actual original operations reached. No
loader/dependency error. Raw session receipt `ama-78-correction2-fail-before.log`.

`change_provenance.operation` now requires explicit source/source-version/
reason and server-records named actor/UTC time/sequential event version. It
refuses missing/blank/nonstring/oversized metadata and actor/time/version/
old-new overrides. Offer/accept also require integer current `handoff_version`
matching the existing history count; changed offer/receipt/escalation/answer
requires fresh case detail. No fallback to filename/hash/current state or
invented historical values.

`Store.add_document` accepts metadata, retains source/version/reason on the
document, and appends `document_history` with complete old/new document-reference
lists (id/name/kind/content hash/document version). The exact same full event
is immutable `upload_document` audit. Returning a deep copy prevents accidental
caller mutation. Existing byte/size/type/scanning path retained.

`offer_handoff` and recipient-only `accept_handoff` enrich existing
`handoff_history` with explicit metadata and exact ownership/handoff changes;
offers include resident-update changes. Audit `handoff_offered`/
`handoff_accepted` holds the identical full event, not a name-only string.
Legacy hand_over stays an offer alias, now forwarding required metadata.
No wider recipients/owners, bulk fields, approval or control scope.

SQL rechecks current registered actor after acquiring its existing writer
transaction, and existing case rowversions reject competing writers. History/
case/ledger commit together; failure discards touched state/staged success
audit and records safe rejection. Uncommitted bytes are cleaned up; lost
commit acknowledgement explicitly remains uncertain and committed bytes are
retained. JSON restores operation-local state, retaining its existing
separate-file crash-atomicity boundary. Notes/source-version/change trees
are redacted for existing roles without note visibility. Scoped forms and
bulk implementations are unchanged, including RV-001 and rescan correction.

### P04-T02: Direct Callers, Native UI and Executed Validation

API upload/offer/accept (and legacy offer alias) forwards caller metadata.
No mandatory metadata is synthesized in production. A test-only fixture
supplies explicit synthetic source/version/reason/current-history inputs to
directly affected document/forms/stock/handoff/queue tests. Existing malformed
metadata tests bypass that fixture and assert refusal.

The existing document and handoff panels collect three labeled required inputs
with current handoff version. Native forms support Enter/required-field focus;
pending save disables only its submit, inline polite errors retain values and
focus their message, and beforeunload warns on unsaved edits. Source details
and unknown legacy values are visible under existing role projection. No
CSS/framework/service changes or unrelated workflow redesign.

| Executed check | Result / precise boundary |
| --- | --- |
| First dependent selection | 177 tests, three expected assertion updates needed for new visible rejection audits; corrected those exact directly affected expectations |
| Core suite after caller contract change | 609 tests OK, one existing skip; no blanket second run |
| API suite after caller contract change | 574 tests OK, 111 existing opt-in skips; no live SQL/platform test enabled |
| Final focused selection after added race/redaction tests | 119 tests OK: provenance, bulk core/API, forms core/API, handoff core/API and role inventory |
| Final exact-shape assertions | 13 provenance tests OK after strengthening complete reference lists, sequential event versions, full new ownership and defensive-copy assertions; core tooling rerun passes |
| Existing core tooling | Ruff check, format55, mypy108 pass |
| Existing API tooling / UI syntax | Ruff check, format19, mypy50, node --check pass |
| Final local Chromium | Required-field focus, keyboard upload/offer/accept, stale inline error/input retention/focus, recipient transfer, 390px/reduced motion, SQL reopen/event-audit equality; no page errors or external requests |
| Preserved modules/original Review | forms.py and bulk_edits.py plus historical original Review unchanged versus ae3adfb; forms/rescan tests only receive required synthetic upload metadata |

Full suites were justified once by the mandatory shared core caller contract.
New edge tests were added after those runs and covered by the final narrow
119-test selection, not a false claim that full suites included later additions.
Local receipts: `ama-78-correction2-core.log`, `ama-78-correction2-api.log`,
`ama-78-correction2-final-focused.log`, `ama-78-correction2-browser.log`.
Existing law-store diagnostics stay explicit unknowns; existing sensor-test
ResourceWarnings are not corrected as unrelated work. Browser harness first
used welcome entry `/`, then corrected to `/app`; final path passes. No new
dependency install/cloud/private/paid inference or real template authority.

### P04-T03: Source Finding Disposition and Final-Head Review Gate

RV-002 requested existing upload/offer/accept gap is now implemented rather
than treated as human-blocked or deferred. Missing legacy payloads refuse
with actionable errors and updated UI collects actual inputs. Original
Review and reported review512a59c4 Revise remain historical, not rewritten
Pass. This is implementation evidence, not a fresh independent acceptance.
Coordinator must rereview the final exact SHA before full criterion 1/#78
acceptance or merge; no downgrade of that acceptance gate. Actual schema
authority is separate #97 human work and did not block this correction.

### Changed Web Region Review (fresh guidelines)

Scope: changed `app.js` helper and upload/offer/accept controls/history only.
Current complete upstream rules fetched before editing and refreshed before
review. Existing Fluent tokens/focus/reduced-motion/native semantics and
owner plain ASCII/sentence-case standard take precedence over generic
typographic/title-case suggestions. No new motion/image/framework.

`src/api/src/zava_forward/api/web/app.js:607` - pass for changed form regions:
labeled/named/autocomplete controls, native keyboard submit/first-required
focus, status/error focus, retained input, pending state, unsaved exit warning,
source/legacy display, existing word wrapping/focus/motion and 390px check.
No claim of whole-file audit, screen-reader or WCAG conformance. No blocking
changed-region finding remains; unrelated preexisting page patterns excluded.

### Correction TWO Publication Receipt

Source `2e63cdf74a2f28d17e2cf3cbc993171755424fbb`, parent integrated
`ae3adfb3f214ea3c30b073b2b71c074df4ec06ed`, base
`92d4f89dd718befbde8bef00dd5cd6db2d99af39`. Privacy-safe author/committer
resolved from gh user8036360/jmservera with repository-local noreply email;
Conventional Commit and required Copilot trailer. Source normal-pushed to
the same topic and verified by remote branch plus PR API draft/open/main.
Immediate PR view initially lagged; direct subsequent API confirmed exact
source, not assumed successful from the stale response.

Final receipt is artifact-only atop tested/published2e63cdf; exact final SHA
posted to PR378 for coordinator independent rereview. Delta from original
published97cdc2a consists of the already documented main92d4f89 rebase/
additive integration through ae3adfb, then this exact RV-002 source correction
and final evidence-only receipt. RV-001/forms implementations and original
Not accepted Review unchanged from ae3adfb. KB prior histories/all index
link targets retained. No further source change, merge or new review loop.
Stop after final ordinary push/readback; full acceptance still pending.
