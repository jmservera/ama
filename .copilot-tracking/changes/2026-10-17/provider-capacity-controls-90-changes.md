<!-- markdownlint-disable-file -->
# Changes: provider-capacity-controls-90

Task #90, 2026-10-17. Scope: full approved plan, ordered execution.
Plan: .copilot-tracking/plans/2026-10-17/provider-capacity-controls-90-plan.md.
Details: .copilot-tracking/details/2026-10-17/provider-capacity-controls-90-phase-details.md.

## P01-T01: Baseline and failing-first reproduction

Uninstalled system interpreter failed with ModuleNotFoundError zava_forward. Created task-owned .venv and installed existing component extras only after that failure. Initial duplicate editable-core install resolution failed; corrected the invocation to one core[dev,sql] entry. Baseline existing quality/procurement: 21 tests pass. No private data read.

Executed before production edits: 29 tests, eight failures (four root behaviors reproduced on both JSON and SQLite): imported numeric-only capacity issues, out-of-period booking succeeds, appointment/non-booked/withdraw changes lack versions, and case advance without order succeeds. Original 21 tests still passed in that run.

## P01-T02: Domain controls and transaction progress

Existing procurement document retained. Source-bound accepted capacity and explicit trusted delegation now gate changes; every lifecycle mutation snapshots issuer/authority/state/appointments. Existing reservation progression works at quota; known zero records deficit; withdrawal explicitly releases with new version/reason. Original uploaded bytes and hash are checked, no fake production seed/delegation added. Deterministic SQLite last-slot, advance-versus-withdraw/rescope/loss, authority revocation, source change and audit failure tests pass: 47 focused tests. Coupled fixture prerequisites now explicitly supply fictional source/delegation, retaining existing safety/resident assertions.

## P02: Existing API, screen and preservation

Existing routes forward contract version and structured source evidence;
package reads deny contractors, whose order reads remain supplier-scoped.
Capacity UI adds original-source/date/home fields, native labels/date/number
controls, live refusal/focus, busy handling and a scrollable semantic table.
Common AI notes explicitly remain not an instruction before/after review.
No new service, role grant, send route, framework or unrelated redesign.

HTTP/browser replay caught and corrected a missing controls helper import.
The wider suite exposed an old building HTTP positive that relied on the
advance bypass; added an explicitly fictional authorized booking, retaining
all building/safety assertions. JSON operation-local compensation also covers
advance and save-then-audit failures; it is not cross-file crash atomicity.
No source test was removed. These are compatible implementation details,
not material deviations requiring another critique.

## Exact-Criterion Engineering Acceptance

| #90 criterion | Executed oracle | Result and boundary |
| --- | --- | --- |
| Nothing scheduled/confirmed beyond evidenced committed capacity | Legacy/unknown/wrong source/version/hash/dates/unit/scope/delegation denials; offered 9 / committed 1 admits one order and refuses second; exact-quota existing booking succeeds; advance cannot bypass; deterministic SQL last-slot and dependency races | Passed on JSON/SQLite and actual local SQL Server; real source truth/legal signature and production authority not attested |
| Every work-order change version + issuer | Sequential immutable issue/appointment/non-booked/reissue/completion/correction/withdraw snapshots, named email/time/delegation/capacity version; failed writes preserve chronology/cache/audit | Passed, including HTTP eight-version lifecycle and local SQL Server inherited checks |
| System draft never instruction | Template note, persisted AI instruction_status, review effect and UI label; accept/reject review never mutates procurement | Passed; no model inference or live send |
| Contractor read-only own orders | Two supplier identities, foreign/forged identity refusals, package denial and every mutation route refusal | Passed at domain and HTTP, both contractor browser screens |

## Final Validation

* Exact suite, API cwd: `PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -m unittest test_quality_procurement test_procurement_api test_role_matrix -q`: 63 passed.
* Combined API-cwd preservation command adds test_resident_decisions, test_hazard_referral, test_buildings, test_sqlstore, test_mvp, test_change_provenance, test_bulk_edits, test_bulk_edit_api, test_form_staging, test_form_staging_api, test_ai_tasks, test_content_standard: 278 run, 277 passed and one existing opt-in skip.
* Distinct core-cwd test_buildings/test_quality_procurement/test_resident_decisions/test_hazard_referral: 114 run, 113 passed and one existing opt-in skip. This avoids mistaking the API module of the same name for the core building suite.
* Standard existing test_mssqlstore.MssqlProcurement and MssqlProcurementApi: 29 passed on a new task-owned loopback SQL Server 2022 container, no mounts/shared/live database. Environment connection credentials never printed or committed.
* Browser: `PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python checks/procurement_browser_check.py`: passed original-source input, inline refusal/focus, keyboard save, quota booking/version, two own-only contractor screens/write denials, 320/390/1280 reflow and reduced motion, zero page errors. External requests blocked. Teardown can log harmless loopback BrokenPipe for abandoned background fetches; these are not hidden application page errors.
* Existing configured changed-path Ruff passed, new typed test/browser and building fixture format passed; inherited migration exclusions unchanged. Core mypy passed 110 source files; API mypy passed 52 source files. Both changed JS files pass `node --check`; `git diff --check` passed.
* A later explicit-path format check bypassed existing migration exclusions and reported baseline formatting differences. Replayed with `ruff format --force-exclude --check` on the same changed core paths: four eligible files already formatted; excluded legacy modules left unchanged. Configured legacy mypy overrides also remain unchanged; type success does not imply newly strict coverage for those modules.
* Current web guidelines retrieved fully and refreshed on 2026-10-17 from raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md. Changed capacity fields/table/status and common AI note reviewed with existing Fluent 2 tokens/native semantics. No new changed-region substantive finding; existing action inputs/unsaved-navigation behavior is not redesigned. No full-site or WCAG claim.

## Remaining Boundaries and Follow-Ups

Actual contract evidence/delegations and operational approval belong to the
named human contract authority owner before live use. Hosted AI/Azure and
human/screen-reader/WCAG acceptance belong to later deployment/UX validation.
These are explicit distinct out-of-scope follow-ups, not blocked engineering
implementation. JSON is single-process and separate-file snapshot/ledger,
unlike SQL transaction/crash guarantees. No private data, live provider
instruction, award/payment, cloud/paid AI or production permission occurred.

## Phase Execution

| Phase | Execution | Evidence |
| --- | --- | --- |
| Research | Complete; Ready | Exact issue/PRD/BRD/current code, three research waves and bounded independent procurement-manager research instrument |
| Plan | Complete; Ready | Plan/details plus one Revise critique; PC-001..005 applied without divergent decisions |
| Implement | Complete | Failing-first eight failures, implemented controls, final exact/preservation/SQL/browser/quality evidence above |
| Review | Complete; Conformant | One independent read-only comparison, no substantive findings; canonical .copilot-tracking/reviews/logs/2026-10-17/provider-capacity-controls-90-review.md |
| Publication | Delivered | Privacy-safe 19431ad with co-author trailer pushed; main PR https://github.com/jmservera/ama/pull/384 opened using Refs #90; no closing/merge/rebase/force push |

## Implementation Status

P01/P02 complete and reconciled with plan/details; the one independent Review
is Complete with Conformant outcome. P03 implementation/evidence publication
is delivered in PR #384. Current-main integration is blocked as recorded
below; no active local engineering defect was found. This evidence does not
claim live company permission, contract approval or full PRD acceptance.

## Publication Preparation

Resolved authenticated GitHub account before staging and configured repository-local
privacy-safe author/committer email; required Copilot co-author trailer retained.
Task-owned loopback SQL container and its mode-0600 ephemeral credential file
were removed after final parity. No shared container/image or database touched.

The final freshness fetch found origin/main had advanced one commit from
reviewed baseline adedf1f to bab4bf3 (#381, initializer infrastructure and shared
KB documentation). No procurement/runtime change was added upstream. Preserved
the explicit no-merge/no-rebase direction; PR targets current main and must
report hosted mergeability/CI rather than invent integrated-main validation.
Shared KB index/log overlap may require later owner integration.

Publication reused the one completed independent Review rather than launching
the PR helper's extra review fan-out. The staged-change MCP tool is unavailable
in this host, so native Git staged diff/hygiene supplied equivalent evidence.
Existing unrelated generic PR notes are preserved; task-specific PR materials
use issue-90 names. No source behavior changed after Review.

## Publication Outcome and Stop

Implementation/evidence commit 19431ad was pushed to the requested topic.
Author and committer both use the resolved GitHub privacy-safe email; the
required Copilot trailer is present. `gh pr create` failed on GraphQL quota;
ordinary `gh api` REST creation succeeded: https://github.com/jmservera/ama/pull/384,
base main, open, Refs #90, no closure.

REST readback reports mergeable=false / mergeable_state=dirty against
bab4bf3. This is a concrete owner/coordinator integration blocker, consistent
with upstream shared-KB overlap. No hosted check runs were registered for
19431ad at read time, so CI/rubric is Pending, not passed. The explicit
no-merge/no-rebase/no-force-push direction is preserved.

Task-specific PR body/reference log and terminal phase/state metadata are
prepared for the final evidence commit/push. No source change followed the
one Review. The automatic session stops after that final push as the user
directed; no child delivery or new review is started. Owner/coordinator
integration/hosted checks, real authority and human acceptance remain
distinct follow-ups, not claimed completed.

## Authorized PR #384 Main Integration (2026-10-17)

The coordinator explicitly authorized rebasing only this run-owned topic,
overriding the earlier no-rebase restriction solely for this integration.
The old publication/stop and conflict observations above remain historical.
No new RPI cycle, independent Review, professional authority or acceptance
claim was created.

* Clean worktree and branch verified before starting:
  feat/provider-capacity-controls-90 at
  6e4dbe18d111673b41049830eb68bf81f89051c8.
* Captured expected remote lease with
  `git ls-remote origin refs/heads/feat/provider-capacity-controls-90`:
  6e4dbe18d111673b41049830eb68bf81f89051c8.
* Ran `git fetch origin main --quiet`; freshly verified final integration
  base is bab4bf3a2ac9ec030d78d27063d1390f800c5c7c.
* Ran `git rebase origin/main`. Only docs/reference/log.md conflicted;
  removed the conflict separators while preserving all upstream bytes first
  and the original complete issue-90 entry afterward. README auto-merged,
  retaining the upstream initializer route and issue-90 capacity route.
* Ran `git add docs/reference/log.md` and
  `GIT_EDITOR=true git rebase --continue`. Integrated topic head before the
  evidence-only commit is db83d4260e4f3d29fa80ce08624155ee4f59ecce
  (implementation 19431ad -> 17d7b3a; evidence 6e4dbe1 -> db83d42).
* `git range-diff adedf1f..6e4dbe1 origin/main..HEAD` shows only shared
  KB context differences for the implementation and an identical evidence
  commit. Exact byte assertions confirm the entire src patch against the
  new base equals the originally reviewed src patch against adedf1f.
  All runtime/tests/browser/component documentation remain byte-identical
  to the reviewed topic. All twelve other upstream changed paths exactly
  match main. No substantive production conflict occurred.
* Exact byte assertion confirms the final KB log equals the complete
  upstream log prefix plus the unchanged issue-90 appended entry.
  All Markdown table rows from both prior index versions are present.
  The original independent Review file is byte-identical; its historical
  Complete/Conformant result is preserved, not promoted into a new
  exact-head external gate. `git diff --check` and main-ancestor check pass.
* No full suite, SQL/browser rerun or dependency installation was warranted:
  conflict resolution changed documentation only and production/test patch
  parity is exact. Earlier executed evidence remains unchanged. No #84/#94
  affected production path required a new combined selection.
* Authenticated account resolved again with `gh api user`; repository-local
  privacy-safe author/committer retained for the integration evidence commit.
  PR body will carry the final publication commit SHA after that commit,
  avoiding a self-referential hash inside its own contents.
* Authorized push command is
  `git push --force-with-lease=refs/heads/feat/provider-capacity-controls-90:6e4dbe18d111673b41049830eb68bf81f89051c8 origin HEAD:refs/heads/feat/provider-capacity-controls-90`.
  No unconditional force, main rewrite, merge or issue closure is authorized.
  External coordinator exact-head PR gate remains forthcoming; Refs #90 only.

## Correction Cycle ONE: Coordinator Revise and Hosted CI

Authorized 2026-10-17 against integrated head 527a537. Medium defect:
create_package permits an empty immutable contract version, making the
package unusable because later delegation checks require one and no update
route exists. Fix by requiring version at creation, not adding an editor or
authority grant. Add domain/API invalid and valid regressions plus explicit
inline browser validation preserving entered values and focusing the version.

Hosted failures also identify the intentionally changed dataset.py hash
stale in the #103 manifest, and JSON/SQLite workflow safety positives lacking
the new evidenced booked-order prerequisite. Refresh the existing exact
hash only; do not weaken validator/authority/coverage semantics. Add fictional
delegation/source/booking after independent safety release, retaining all
existing safety assertions and production guards.

Plan correction checklist active. Validation will reproduce exact failures,
then run focused and full core/API discovery matching the failing CI, browser
and configured quality checks. Actual SQL creation parity if available.
Original independent Review remains byte-identical; coordinator Revise and
correction evidence are separate, with external closure still required.

### Correction ONE Implementation and Focused Evidence

P01/P02 correction: create_package now strips and requires contract_version
before dates/store mutation/audit, API no longer invents the empty default.
UI uses existing native label/input/button/status patterns with required,
aria-describedby/aria-invalid, an adjacent polite inline message and explicit
focus to the empty version. Validation returns before request/rerender,
preserving all package inputs; input clears the invalid state. No new editor
or permission grant. Existing positive fixtures supply SYN-1 at creation;
old invalid-date/name tests still supply a valid version to retain their
original failure intent.

Red-first command ran six selectors: four domain/HTTP version methods
produced twelve subcase failures, plus both existing safety-flow selectors
errored on missing booking. Existing manifest integrity method reproduced
the stale dataset.py source hash. After the correction: focused combined
procurement/API/roles/MVP/workflows 107 passed; existing scenario manifest
8 passed and needs inventory 11 passed. Actual isolated local SQL Server
MssqlProcurement/MssqlProcurementApi 31 passed, including the new creation
tests. The task-owned correction container/credential were removed afterward.

Browser passed empty/whitespace refusal with no package mutation, retained
package inputs and version-field focus, valid trimmed version creation by
keyboard, original source capacity/quota/order/contractor journeys,
320/390/1280 reflow/reduced motion and zero page errors. Loopback navigation
teardown may log BrokenPipe for abandoned background fetches; no external
request is permitted. Fresh web guidelines fetched before edits and
refreshed before changed-region review on 2026-10-17. Existing Fluent styles
and native semantics retained; no redesign or full WCAG acceptance claimed.

Configured full core/API lint, format and mypy pass (core 57 eligible
formatted files/110 source files; API 20/52), existing migration exemptions
unchanged. Isolated strict lint/format for changed browser harness pass;
JS syntax, compilation of migrated production packages and diff hygiene
pass. One added long fixture call initially failed E501, was wrapped without
behavior change, then full core quality gates passed. No dependencies added.
Full core/API CI discovery subsequently passed; exact results are below,
not inferred from the previous focused runs.

Exact manifest-object comparison: only sources[id=fixture].sha256 changes
to d36bac22223c47167f5847e6b2e575c0f88dc19cf9fbc6fba4ffba5a7d6023a1.
All other fields, eleven profiles/nine workflows, unavailable states,
provisional roles/proposed journeys and no-approval labels are identical.
Validator untouched. Original Review bytes exactly match head 527a537.

Changed web-region review format:

### src/api/src/zava_forward/api/web/ops.js

Pass for correction region: associated inline status/invalid description,
focus first invalid version, native required input, preserved values and
keyboard activation. Existing inherited typography/navigation behavior is
not a whole-site audit. No substantive changed-region finding.

### Correction ONE Final Validation and Dispositions

| Reported gap | Implementation disposition | Executed evidence |
| --- | --- | --- |
| Coordinator Medium: immutable blank package contract version | Addressed in source; domain/API reject omitted/empty/whitespace version before any mutation; UI inline refusal preserves values and focuses version; no updateroute/authority grant | Twelve failing subcases first, then JSON/SQLite domain/HTTP positives/negatives and browser valid keyboard creation; inherited actual SQL Server creation tests pass |
| Hosted core needs-inventory/scenario-manifest stale source hash | Addressed by existing manifest's exact fixture SHA-256 refresh only; validator and complete authority/coverage object unchanged | Existing 8 manifest + 11 inventory tests pass; exact object assertion proves only one hash changed |
| Hosted API/MVP CI/validation JSON/SQL safety booking positives | Addressed with fictional evidenced source/delegation/booking after independent release; no assertions removed/skipped, guard unchanged | Both exact formerly failing selectors pass; full API discovery passes |

Full relevant CI replays from component directories, using the existing venv:

* Core: `../../.venv/bin/python -m unittest discover -s tests -v`:
  651 run, 650 passed, one existing isolated-Azure-SQL opt-in skip.
* API (same command shared by src-api, MVP CI and MVP validation):
  `PYTHONPATH=../core/tests:../agents/tests ../../.venv/bin/python -m unittest discover -s tests -v`:
  613 run, 471 passed, 142 skips. Of those, 141 are existing SQL Server
  opt-ins and one is the opt-in rendered check. No skips were added.
  The changed procurement browser was executed separately and passed;
  changed SQL behavior was executed separately on actual local SQL Server.
* Actual task-local SQL Server 2022:
  `test_mssqlstore.MssqlProcurement test_mssqlstore.MssqlProcurementApi -q`:
  31 passed, no skips. These counts overlap discovery and are not summed.
* Focused core/API/workflow/role/MVP 107 passed, exact existing manifest 8
  and inventory 11 passed. No inference/cloud/private datasets/live orders.
* Full configured core/API Ruff lint/format and mypy passed; strict changed
  browser harness lint/format, JS syntax, migrated-package compileall and
  diff hygiene passed. Dependency manifests and existing exemptions unchanged.

Only the user-requested failing component suites were broadened. No unrelated
full service/infrastructure/container build was substituted for the exact
checks. No full original RPI or independent Review was rerun. Production
changed after original Review, so its historical Complete/Conformant result
is not current correction closure. Coordinator external exact-head closure
and hosted rerun remain pending until independently provided.

All corrections are local engineering changes with the original four criteria,
human/contractor/resident/safety controls retained. No real professional
authority, actual capacity, financial commitment, AI/cloud or human/WCAG
acceptance is claimed. Plan/details/state/PR will reflect implementation
complete and external closure pending, not an invented Pass. Normal push
only on the same branch; no rebase/force/merge/issue closure in this cycle.

### Correction ONE Publication Boundary

This terminal payload contains implementation, regressions, exact manifest
hash, component/KB documentation, plan/details/state and PR evidence. Source
baseline is integrated 527a537; no new base/rewrite operation in this cycle.
Final commit SHA is included in the live PR publication readback rather than
self-referenced inside its own commit. Authenticated GitHub identity will be
resolved before commit, using repository-local privacy-safe author/committer
and required Copilot trailer. Use ordinary `git push origin
feat/provider-capacity-controls-90`, never rebase/force/merge/closure.
Stop clean after success; any new hosted/independent result belongs to the
external coordinator gate, not an invented local Review verdict.

## Authorized Integration After #382 (2026-10-17)

Coordinator authorizes topic-only rebase after correction ONE, onto freshly
fetched main bbbc9243505b606550327c64bf5429243f457f2e. Clean owned topic and
expected remote lease were both 5244f99db0a5b53f761b6c3a7bc5f1d9c4e829c1.
`git rebase origin/main` conflicts were the append-only KB log, additive
SQL Server harness classes, and shared SQL validation hooks. Both stock and
procurement validation and test classes retained; upstream canonical discard
cleanup-before-reads, committed-cache restoration and watermark invalidation
retained verbatim. README routing auto-merge preserves both intents.
`GIT_EDITOR=true git rebase --continue` completed at
7cf8df7b5ed67055dc6d40a95c554598b448c28e before integration evidence/fixes.

Shared save's refusal branch retains stock decision-scope cleanup ownership.
The combined source revealed the analogous procurement/advance cleanup still
could mask the original exception if canonical reload fails. A bounded
integration regression will reproduce persistent/one-shot reload failures;
apply stock's existing exception-note/logging pattern to those existing
caller scopes, retaining one canonical discard primitive, not a duplicate.
No unmerged finance-94 branch is imported; all existing finance controls/
callbacks are preserved and tested along with merged stock/procurement.

Validation scope: combined finance-match/signoff, stock reconciliation/API,
procurement/API/workflows and shared store/provenance gates; real local SQL
Server stock+procurement parity after shared transaction reconciliation.
No full RPI or Review; original historical Review untouched, external
coordinator exact-head closure remains required. No professional authority
or hosted acceptance invented.

### Integration Validation and Publication Payload

Final integrated source head:
e2314a7c2ea0d6588b696030d153f29f74208dd7.
Final base: bbbc9243505b606550327c64bf5429243f457f2e.
The subsequent evidence-only commit is the terminal publication payload;
its exact final head is recorded by the PR REST head/readback after push.
Source commit author and committer are the authenticated account's
privacy-safe noreply identity, with the required Copilot trailer.

Scope-owned cleanup also handles BaseException cancellation, matching stock's
existing pattern. Cancellation extension failed first (one failure/three
errors), then passed after both scopes assumed the full cleanup ownership.
Final regression covers twelve operation/failure/persistence combinations,
including transaction cancellation, exact original exception identity,
explicit logs/notes, canonical disarm/cache restoration, unavailable-read
refusal, no later mutation/audit flush and a valid three-version retry.
No cleanup helper is duplicated. Canonical `_discard` remains AST-identical
to upstream; `_proc_sync` now stages complete reads/decodes without erasing
known committed document snapshots on partial failure.

Executed commands/results (installed own venv; fictional fixtures only):

* Core cwd, `PYTHONPATH=tests ../../.venv/bin/python -m unittest
  test_finance_signoffs test_stock_reconciliation test_quality_procurement
  test_sqlstore test_change_provenance test_bulk_edits test_form_staging -q`:
  194 passed on the final source, no skips.
* API cwd, `PYTHONPATH=tests:../core/tests:../agents/tests
  ../../.venv/bin/python -m unittest test_stock_reconciliation_api
  test_procurement_api test_workflows test_role_matrix test_mvp
  test_form_staging_api test_bulk_edit_api -q`:
  73 run, 72 passed, one existing opt-in skip. Explicit fixture law-store
  unknown warnings remain; no success-shaped regulatory fallback introduced.
* Actual task-local SQL Server 2022, existing opt-in harness and disposable
  loopback/master only, `python -m unittest
  test_mssqlstore.MssqlStockDecisions test_mssqlstore.MssqlFinanceSignoffs
  test_mssqlstore.MssqlProcurement test_mssqlstore.MssqlProcurementApi
  test_mssqlstore.MssqlStoreTests test_mssqlstore.MssqlImproveTests -v`:
  final 74 passed, no skips. SELECT 1 established responsiveness first.
  Added finance class reuses existing SqlFlows via existing factory/fixture
  reset; current-main matching, limits, independent approvals and human
  technical signoffs are retained, not fabricated unmerged #94 controls.
  Combined SQL replay was repeated only after final cancellation ownership
  changed; not a duplicate full component suite. Container
  `zf-issue90-i84-12428a68` and mode-0600 ephemeral credential removed in
  finally; no other container, image or database touched.
* Shared portability selectors: 3 passed. Full configured core/API
  `ruff check .`, `ruff format --check .`, `mypy` and `git diff --check`
  passed after final source edits; existing exclusions unchanged.

Preservation assertions passed: exact upstream KB bytes as prefix plus the
unchanged own suffix; original Review/critique byte-identical; canonical
discard unchanged; upstream stock/signoffs/finance and their tests exact;
all upstream index rows and own added routes retained; twelve
non-overlapping upstream files exact; corrected dataset/manifest and both
changed web files byte-identical to published correction ONE; main ancestor.
An initial over-strict index check expected an obsolete pre-#382 stock row.
The correct intent check retains #382's updated stock row and all own added
rows; no routing was removed. Browser rerun is not warranted for this
backend-only integration with byte-identical UI.

Terminal commands: privacy-safe source/evidence commits, then
`git push --force-with-lease=refs/heads/feat/provider-capacity-controls-90:5244f99db0a5b53f761b6c3a7bc5f1d9c4e829c1 origin HEAD:refs/heads/feat/provider-capacity-controls-90`.
Expected remote is explicit; no unconditional force, main rewrite, merge,
issue closure, extra full RPI or Review. REST updates PR #384 with the exact
final head/base and this evidence, then verifies remote/clean status once.
External coordinator closure and hosted exact-head checks remain pending;
original independent Review is historical, not a new Pass.

### Latest-Main Advance Detected Before Publication

Final remote lease verification found main advanced to
d400eb8d1d0d6567445b0fc11803260eab897a65 (#383, finance #94).
`git fetch origin main` confirms that head. Nothing has been force-pushed:
owned remote remains the explicit old lease5244f99. The preceding bbbc924
integration/validation is historical, not the terminal latest-main outcome.
Its run-owned evidence is committed to make the worktree clean before
continuing the same authorized latest-main rebase. No stash/discard or
unrelated branch import; finance is now merged upstream.

New main preserves canonical pending-before-read cleanup but extends
`_discard(pending=())`, original-exception logging and protected lock exit,
and adds finance commit-time actor/independence validation. Retain all of
these plus stock/procurement scope ownership and staged document reload;
replay combined actual finance-match/stock/procurement suites and local
SQL after resolving source conflicts. External acceptance still pending.
