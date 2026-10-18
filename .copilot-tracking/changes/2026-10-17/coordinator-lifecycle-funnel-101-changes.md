---
title: Coordinator lifecycle funnel issue101 changes
description: Actual implementation, validation and delivery receipts
ms.date: 2026-10-17
---

## Execution Context

Task101, full plan scope, automatic. Initial base/head
ebc8dab87ae9bd6a33380b85e86f38be5ed9f213, branch
feat/coordinator-lifecycle-funnel-101. No prior source changes or PR.
Research executed/Ready; one final-candidate critique Complete/Revise, PC001-003
directly incorporated before implementation. Original critique retained unchanged.

## P01 Read-only Contract

P01-T01/T02 completed. Added coordinator.py, explicit staff-only API route and
projection permission, 13 semantic test methods (JSON/SQLite subclasses) and six
HTTP test methods (SQLite/JSON/opt-in MSSQL). No document/provenance/Store writer
or117-owned runtime changes. Current-stage source selection and metric-stage
drill selection are separate. Unknown history/unsupported exclusions cannot
become invented actuals. Record rows use the existing closed scalar field helper
rather than constructing full Store summaries and removing their private fields:
an immediately relevant simplification preserving the approved field boundary.
Current stop flags also remain accurate when drilling source-filter exclusions,
not just when displaying the selected cohort.

## P02 Existing Workbench

P02-T01/T02 completed. Existing overview links to scoped coordinator mode; reused
mapPanel and native Fluent-foundation tables/controls, independent URL selectors,
map/list focus route, stable record pages, explicit partial/unknown/approval cues.
Updated existing programme synthesis, index, append-only log and core/API guides.
web-design-guidelines and redesign-existing-projects loaded;
guideline source fetched fully before edits on 2026-10-17. Owner Fluent/native,
WCAG baseline and plain-language sources read. No conformance claim.

## P03 Validation and Delivery

P03-T01/T02 completed. Initial system-Python source import failed (missing package);
restored task-local .venv via pip editable core[sql,dev], agents, api[dev].
Chromium installation succeeded. Docker daemon available. No data files read
outside public existing test fixtures. No Azure or billable model operation.

### Commands and actual results

All commands below run in this worktree. `.venv` contains pip editable source
distributions, not PYTHONPATH=mvp. No full-suite claim.

| Check | Actual command / boundary | Result |
| --- | --- | --- |
| Coupled core regression | From src/core: `PYTHONPATH=tests ../../.venv/bin/python -m unittest test_coordinator test_progress_reports test_progress_event_capture test_taskqueues test_sqlqueues test_sqlreads test_sensor_privacy -q` | 154 run, 135 pass, 19 explicit opt-in/JSON-only skips, zero failures; existing queue/SQL tests generate their own synthetic 60,000 fixture, not private stock |
| Coupled API/UI regression | From src/api: `ZF_COORDINATOR_BROWSER=1 PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -m unittest test_coordinator_api test_progress_report_api test_role_endpoint_inventory test_design_system test_accessibility_baseline test_content_standard test_ui_support -q` | 97 run, 78 pass, 19 explicit opt-in/backend/browser ownership skips, zero failures; actual coordinator Chromium ran |
| Final semantic check | From src/core: `../../.venv/bin/python -m unittest discover -s tests -p test_coordinator.py -q` | 26 run/pass, zero skips/failures after final excluded-record stop assertion |
| Final HTTP/browser check | From src/api: `ZF_COORDINATOR_BROWSER=1 PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -m unittest test_coordinator_api -q` | 18 run, 11 pass, seven skips (six opt-in MSSQL, one JSON duplicate-browser); actual SQLite Chromium passes |
| Final actual SQL Server | `ZF_COORDINATOR_MSSQL=1 PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -m unittest test_coordinator_api.MssqlCoordinatorApi -v` from src/api with task-created loopback env | Six run, five pass, one browser-only skip. Disposable UUID databases dropped after tests; second-writer refresh, same-filter list parity, records/map counts, clustered viewport, excluded-record stops, denials and unchanged ledger/sequence |
| Configured Python checks | In each of src/core and src/api: `../../.venv/bin/ruff check . && ../../.venv/bin/ruff format --check . && ../../.venv/bin/mypy` | Pass; core120 and API56 typechecked source/test files; formatter67/24 files |
| JavaScript / whitespace | `node --check src/api/src/zava_forward/api/web/app.js`; `git diff --check` | Pass |
| Actual image build | `docker build -q -f src/api/Dockerfile -t zf-issue101-api:local src` | Final image sha256:c4238ecd132048bdd01ce5bbe5f0c71c31e9a9727ba9bab2507d656b34f2f08c |
| Image kernel/startup | `.venv/bin/python src/check-container.py api zf-issue101-api:local` | Pass: UID/GID10001, read-only root, writable state, zero capabilities, NoNewPrivs, five negative probes, plain nonroot and hardened default HTTP startup |
| Installed-image application | Task-local script launches final image with synthetic mounted fixture, SQLite, reduced kernel permissions, loopback random port | Pass: pam/rex staff200, contractor403, five selected records, one missing coordinate, exact exit-A drill, five installed source hashes match coordinator.py/projection.py/server.py/app.js/style.css |

SQL task runner was executed using `.venv/bin/python -c` plus runpy on the
session-owned `files/issue101_sql_check.py`; it creates and waits for its own
local SQL container, supplies ephemeral credentials only in process environment,
runs the command above, drops its fixture databases and removes its container.
Final name zf-issue101-sql-4ac71345ad0f is stopped/removed. Earlier parity run
zf-issue101-sql-605de2a0db7f also stopped/removed (same five passes/one skip).
Final image application container zf-issue101-api-0e01bf6b80f4 stopped/removed.
Earlier image check containers were also removed. Task debug loopback server
stopped and browser closed. Shared issue117 SQL resource was not touched.

### Browser evidence and rerun history

Actual Chromium exercised keyboard filter application, a case now in Contacting
resident drilling from observed exit Contact paused, case detail and browser back,
native map-list focus, forced cluster keyboard zoom with retained selection,
source filter/list/map parity, unknown history/coordinates, empty cohort,
contractor and changed-role403 denials, and 320/390/1280px reduced-motion reflow.
No page errors on final run. Independent human/screen-reader/zoom/full-WCAG
or production-scale coordinator acceptance is not established.

Initial browser failed before the controls appeared because test-only MAP_CAP=1
with fixture points crossing zero longitude cannot converge in the legacy grid.
The tiny fixture was corrected to one geographic hemisphere; production cap500
and cluster algorithm were not changed. A subsequent diagnostic wait used an
eval-string disallowed by the real CSP; changed to arrow predicates without
weakening CSP. Playwright cleanup ordering was corrected to close contexts before
the driver. Two later failures exposed test route races (interacting before
new content, and old same-count content satisfying a wait); fixed using explicit
new-route content/response synchronization. Final module18 run/11pass/seven skips
and a separate repeated actual journey1pass establish the current browser result;
the last final module rerun after excluded-stop handling also passes.

Initial SQL session-file direct execution failed import before any resource was
created. Execution via installed-project Python/runpy succeeded; no package or
PYTHONPATH workaround was needed. Initial lint/type gates found new-file long
lines, formatting and migrated-call annotations; fixed, then both complete
configured project gates passed. No test removal or xfail introduced.

### Before Original Review

All buildable P01/P02 and P03-T01/T02 work is complete. P03-T03 original Review
and P03-T04 delivery remain pending. Original Review must be retained with all
findings; no independent coordinator approval is implied by engineering checks.

## Deviations, Blockers and Follow-Ups

No material scope deviation or writer ordering dependency identified during
implementation. The later original Review exposed RV-001 below.
KB index/log overlap with117 declared; preserve both histories on a later
authorized integration. No rebase authorized. Independent human/coordinator
acceptance, full historical exclusions and WCAG acceptance remain outside delivery.

## Original Review and Current Delivery Gate

P03-T03 completed once. Original record:
.copilot-tracking/reviews/logs/2026-10-17/coordinator-lifecycle-funnel-101-review.md.
Execution Complete, outcome **Defects found**, not independent acceptance.
RV-001 Medium reproduces legitimate mixed-case stored email authenticating and
reading cases200 but coordinator403, on JSON and SQLite. Required correction:
normalize the coordinator registry lookup key consistently with Store/auth, while
retaining current code/role/email checks; add direct and HTTP regressions.
No source correction or second Review has occurred.

The bounded backend lens additionally ran44 tests (36 pass, eight skips),63
malformed-history variants and targeted timestamp/ledger/identity repros.
These are supplementary Review evidence, not replacement browser/SQL/image
receipts and not a pass for the exposed identity counterexample. The original
Review also records a Low map-status number-format residual at app.js:1053.

P03-T04 publication/completed delivery is blocked by RV-001 under accepted
PC-003. Source and all RPI artifacts are retained locally for persistence.
No push, PR, remote-head equality or CI result is claimed. Main's freshly queried
remote head remained ebc8dab87ae9bd6a33380b85e86f38be5ed9f213; no rebase/force.
One-pass task status completed with Defects found is distinct from successful
delivery; automatic session stays running at Follow-up with rank1 correction
awaiting later selection. No child work or review-closure assessment started.

| Issue acceptance criterion | Current evidence/status |
| --- | --- |
| Counts show denominator, holds, priority, coverage | Engineering evidence on tested authorized fixtures; access coverage blocked by RV-001; no independent acceptance |
| Same-filter list/map totals agree | JSON/SQLite/actual MSSQL and Chromium receipts; not universal access acceptance while RV-001 is open |
| Funnel drills to records | Current/observed exit-A/returns/reopens and unknown semantics exercised; authoritative lifecycle exclusions remain Unknown, not invented |

No overall issue closure or full PRD acceptance. Independent coordinator, human
understanding and WCAG acceptance remain explicitly unchecked.

### Final local persistence checks

After Review, only documentation/workflow metadata changed; production source
matches the tested final image. Final `git diff --check`, `node --check` and
state JSON parsing passed. Link targets across11 affected documentation/artifact
files resolve, honoring the canonical RPI workspace-relative link convention;
anchors were not independently checked. The first naive relative-only link
checker falsely flagged four original critique workspace-root links; the
convention-aware rerun passed without editing the preserved critique.

Final owned-container inspection finds no zf-issue101 container, and no running
task shell remains. Removed only the two known task-generated Playwright
console/snapshot files. No shared resource stopped or changed. Fresh GitHub
identity resolved id8036360/loginjmservera; local commit author and committer use
the privacy-safe noreply address. P03-T04 remains partial: local persistence only,
no normal push/PR/remote-head equality/CI claim while RV-001 is open.

## Correction ONE: Authorized RV-001 Scope (P03-C01)

Coordinator explicitly authorized this bounded correction on 2026-10-17 in the
same original RPI0789cf67-8f5d-4441-a33f-2b243944b799. Clean source head
42f08556e2f2854024ddfa5a03b926039d28edff, branch unchanged, fresh remote main
ebc8dab87ae9bd6a33380b85e86f38be5ed9f213 and no PR. No rebase needed/authorized.
Plan/details updated before source work. Write boundary: coordinator lookup,
its direct/API tests and related current documentation/workflow artifacts only.
First boundary failing-first JSON/SQLite direct and authenticated HTTP regression;
retain code/email/role equality and all denial controls. Then narrow production
fix, focused regression/browser/static gates, normal commit/push/main PR Refs #101.
No Low formatting work, no new Review or critique, no writer paths.
Original Review/critique hashes frozen in phase details for final byte verification.

### Correction ONE: Result and Focused Receipts

P03-C01 complete. Only production edit is the guarded lowercase registry lookup
in core/coordinator.py; current actor email/code/role equality and registered
staff-role requirements remain exactly unchanged. No whitespace normalization,
privileged fallback, auth-provider change, writer/query/schema/refresh change,
web edit or low-priority formatting work. Source predecessor42f08556 and
integration baseebc8dab8 unchanged. New direct/core and real HTTP tests share
existing JSON/SQLite harnesses and public synthetic fixture.

| Command / scope | Actual result |
| --- | --- |
| `PYTHONPATH=src/core/tests:src/api/tests:src/agents/tests .venv/bin/python -m unittest test_coordinator.Coordinator.test_mixed_case_registered_identity_preserves_exact_current_checks test_coordinator.SqliteCoordinator.test_mixed_case_registered_identity_preserves_exact_current_checks test_coordinator_api.CoordinatorApi.test_mixed_case_registered_email_authenticates_without_widening_access test_coordinator_api.JsonCoordinatorApi.test_mixed_case_registered_email_authenticates_without_widening_access -v` before fix | Four run, two direct PermissionError errors, two HTTP403-versus200 failures, zero pass; existing authentication and case-list200 assertions succeeded |
| Exact four selectors after fix | Four run/pass, zero skips/failures/errors |
| `PYTHONPATH=src/core/tests:src/api/tests:src/agents/tests ZF_COORDINATOR_BROWSER=1 .venv/bin/python -m unittest test_coordinator test_coordinator_api -q` |49 run,41 pass,eight skips (seven opt-in MSSQL, one JSON duplicate-browser), zero failures/errors; real existing Chromium journey passes |
| Final core module plus two mixed-case HTTP selectors, same PYTHONPATH |30 run/pass, zero skips/failures/errors, after adding malformed/missing actor-field assertions |
| Actual Chromium selector with test-only fixture patched before setup to stored Pam@Example.Test |One run/pass, zero skips/failures; real login, keyboard filters, count/record/map parity, observed exit-A drill/back, unknowns, cluster focus, reduced-motion reflow, contractor and changed-role denials |
| Configured `ruff check . && ruff format --check . && mypy` in core and API |Final pass;67/24 files formatted,120/56 files typechecked. Initial core mypy failed from reused test-loop variable inferred as string-only; renamed second loop variable, reran both projects successfully |
| `node --check src/api/src/zava_forward/api/web/app.js`; `git diff --check` |Pass; no web source edits |
| `docker build -q -f src/api/Dockerfile -t zf-issue101-api:local src`; `.venv/bin/python src/check-container.py api zf-issue101-api:local` |New image8279cbf06ba19bf5a57c45896ec0ef65292d80c2ad3338bb6ca88e707cd11a13; kernel controls, negative probes and compatible startup pass |
| Session image HTTP/hash script with mixed-case seed, installed image and task-owned loopback container |Pass: Pam/Rex200, contractor403, totals5/missing-coordinate1, exact exit-A/ZF-1 drill and five installed-source hashes; zf-issue101-api-3d5eb295a627 stopped/removed in finally |

Direct tests retain denials for mismatched exact email, unknown/missing/malformed
email, missing code/role, changed code, changed/unknown/missing role, contractor
and revoked registry. HTTP tests prove real mixed-case auth and same-filter
list/record/map totals, unauthenticated401, contractor403, unknown/empty/None
current roles403 and removed-registry401. Other existing scope/privacy/audit/
unknown/funnel regressions remain passing. SQL fixture writes exist only in tests.

Actual MSSQL not rerun for this pure in-memory key normalization: no database
contract/query/count/field/filter/lock change; SQLite reload and actual HTTP
exercise the normalization at the common Store boundary. Prior actual MSSQL
six run/five pass/one skip remains historical only; the newly inherited MSSQL
identity test is not claimed executed. Prior coupled154/97 checks also historical;
no full-suite, human/WCAG or independent coordinator Pass.

Original Review and critique SHA256 match their frozen values byte-for-byte.
RV-001's engineering counterexample is addressed by separate failing-first
receipts, without changing original Complete/Defects found or critique Revise.
PC-003 publication gate is satisfied for this bounded correction; independent
coordinator review remains pending. All three issue criteria retain their prior
count/coverage/map/filter/drill semantics and tested engineering evidence;
unsupported lifecycle exclusions remain explicitly Unknown, not new history.
No117 writer/runtime/shared resource changes. No task-owned container remains.

### Correction ONE: Publication (P03-T04)

Fresh gh api user returned id8036360/loginjmservera. Configured repository-local
privacy-safe noreply author/committer and committed with Copilot trailer:
5464f8da69bbc979171d8cffd23c4013843aeb96. Normal push created the same topic
remote without force/rebase. Main still ebc8dab87ae9bd6a33380b85e86f38be5ed9f213.
Opened https://github.com/jmservera/ama/pull/396 to main with Refs #101, complete
RPI/correction commands and honest historical/current validation limits.
Initial PR head equals correction commit, clean worktree; initial statusCheckRollup
empty (not CI pass). This final metadata receipt is persisted by an additional
ordinary commit and normal push; final exact head/clean/PR check reported externally
without a self-referential commit hash in its own content.
First check observation: image-paths and src-no-working-data passed; remaining
checks pending. This is not final-head CI evidence or permission to merge.

P03-C01 and P03-T04 complete. No second Review/critique, no independent acceptance,
merge or closure. Current task outcome is published engineering delivery with
correction ONE evidence; original Review Complete/Defects found remains historical
and byte-identical. Next action is independent coordinator review of PR396 final
head. All three ACs have bounded tested engineering evidence; unsupported general
lifecycle exclusions and full conversion remain Unknown, human/coordinator/WCAG
acceptance unchecked, Low map-number formatting explicitly deferred.
Actual MSSQL/image prior receipts remain historical pending evidence-based
validation decision; no historical result will be relabelled as current.
