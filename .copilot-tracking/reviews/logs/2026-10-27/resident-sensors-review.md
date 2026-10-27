<!-- markdownlint-disable-file -->
# Review: Resident sensors

## Scope and Evidence

* Task ID: 468; date: 2026-10-27.
* Scope: full task P01-P03 against candidate 61c9e98b68c869cc8197271679e5b37ff36b2512.
* Parent base: 55c239d90dabec1e974eb60330e224c3a0fc6190, feat/resident-interactive.
* Plan: .copilot-tracking/plans/2026-10-27/resident-sensors-plan.md
* Details: .copilot-tracking/details/2026-10-27/resident-sensors-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-27/resident-sensors-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-27/resident-sensors-changes.md
* Research: .copilot-tracking/research/2026-10-27/resident-sensors-research.md

## Opening Review State

* Goal: independently compare own-home boundary, accessible UI, tests and genuine evidence.
* Evidence readiness: P01-P03 checked, details/changes reconciled, unit and browser results available.
* Acceptance: issue #468, caller constraints, plan and PC-001-PC-003 dispositions.
* First boundary: committed source diff against parent and canonical evidence.
* Read-only boundary: source and phase evidence; only this review record may be written.
* Initial blockers: no source-review blocker; SQL Server compilation/integration intentionally unrun.
* Independent reviewer boundary: one post-implementation Review, not a critique repeat.
  Source is immutable; no SQL execution, Azure, private data, secrets, verifier,
  deployment, full gate, Git writes, or further agents. Only this record may change.
* Evidence attribution: supplied candidate test/browser results will be distinguished
  from checks independently executed during this Review.

## Execution Status

* Execution status: Complete.
* Outcome: Not accepted.
* Reviewed candidate: 61c9e98b68c869cc8197271679e5b37ff36b2512 against
  55c239d90dabec1e974eb60330e224c3a0fc6190. HEAD matched the candidate.
* One independent post-implementation Review covered all changed implementation,
  tests, documentation and P01-P03 evidence. No source was changed.
* Independently executed nine focused SQL-free tests: passed in 0.717s.
  Existing full-suite, lint/type and Chromium results are supplied implementation
  evidence, not independently rerun results.
* The pre-existing dirty session-state artifact belongs to the parent. It was
  not read or modified for this Review. Only this canonical review record changed.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01 / P01-T01 | Optional view history, typed parsing and session-owned projection | Reconciled as implemented | Exact SQL equality remains incomplete: RV-001 |
| P02 / P02-T01 | Native meters, static histories, disclosure/table and Fluent-token styling | Reconciled | Changed web hunks pass the fresh source-guideline assessment below; no screen-reader acceptance inferred |
| P03 / P03-T01 | Unit discovery, focused tests, Ruff/mypy, constructed-reader Chromium and README | Reconciled | Supplied checks and independent nine-test run distinguished; prohibited integration remains unrun |
| Follow-Up Items | Later authorised view apply/populated SQL and human screen-reader acceptance | Reconciled | Distinct follow-ups RV-002/RV-003, not missing active phase tasks |

Phase completion markers describe implementation and permitted checks performed.
They do not close RV-001 or establish acceptance. The research header still says
"In progress" and its question table says "Open", but its Planning Readiness,
answers C1-C7/W1 and final handoff explicitly say executed/ready. This historical
metadata inconsistency does not obscure the evidence boundary or block Review.

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | infra/sql/resident-showcase.sql; src/core/src/zava_forward/core/resident_showcase.py; src/core/src/zava_forward/core/resident_showcase_sql.py | Stored source data through the existing fixed view; chronological typed history with no public identifiers | TOP 48, both home predicates, both source predicates, INCLUDE_NULL_VALUES, strict parser and response allowlist inspected | Supplied boundary/core/API checks; independent nine focused tests passed | Good normal-path/session isolation; RV-001 prevents exact-match acceptance |
| P02-T01 | src/api/src/zava_forward/api/resident_demo/web/demo.js; src/api/src/zava_forward/api/resident_demo/web/demo.css | Latest stored observation, named single-unit plots and equivalent native table | Labels, native meter semantics, time alternatives, scoped headers, named scroll region, native disclosure and existing focus styling inspected | Supplied 23 Chromium assertions; fresh guideline/source assessment | Engineering boundary conformant; human acceptance remains separate |
| P03-T01 | src/core/tests/test_resident_sensors.py; src/api/tests/test_resident_demo_api.py; src/api/checks/resident_sensors_browser_check.py; src/api/README.md | Boundary regressions, fresh generator fixture and honest operational limitations | Commands/results and harness reviewed; README documents coordinated view/application update | Supplied full suites, changed-file Ruff/format/mypy and browser checks; independent focused tests/diff check | Permitted validation performed; no claim of SQL compilation, deployed rights or full accessibility conformance |

### Acceptance comparison

* Generated data: source SQL uses existing dbo.sensor_register/sensor_reading;
  case home.stock_id, not case ID, selects readings. The browser fixture calls
  the existing generator and creates no live-data claim.
* Own-home authority: fixed LIST_SQL/ONE_SQL remain restricted to
  resident_showcase.v_resident_case. ONE_SQL parameterises only the signed-session
  case. Fresh authorisation remains in ResidentDemo.view_for; no browser home
  parameter, header or path supplies authority. Two-session, forged-selector,
  unauthenticated, forged-path and revoked-session regressions are present.
* Exactness: case-distinct identities and reading provenance are rejected;
  BIN2 predicates cover sensor ID, both home IDs and both source labels.
  However, SQL string-padding semantics leave the register-side exactness gap
  in RV-001. Python rechecks reading home/source only.
* Bounded typed output: SQL selects the latest 48, domain sorts chronologically,
  validates UTC timestamps, rejects duplicates, caps count and emits only time,
  numeric/null channels and statuses. Sensor, reading and home IDs are stripped.
* Unavailable versus malformed: missing numeric channels, out-of-range/nonfinite
  numbers and OUTLIER/STUCK preserve timestamps with explicit unavailable text.
  Invalid scalar types, shape, provenance, identity, UTC or unknown fault deny.
  Latest means latest observation, not an undisclosed older valid replacement.
* Presentation: synthetic/non-live/non-safety copy, labelled native meters only
  for valid latest channels, no fake zero, static SVG gaps and equivalent table
  are implemented. Meter values need not become keyboard tab stops; disclosure
  and the scrolling table region supply native keyboard paths.
* Scope protection: no header/index change, MAX_MAPPINGS change, new dependency,
  request-time generation, direct table grant, deployment or private input.
  Changed-file scope and diff were inspected.

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01 | Complete register/reading/case predicates and nullable channel contract | PC-001/PC-002; compatible with confirmed own-home and unavailable-state requirements | Plan dispositions, detailed state table, changes and source compared | Original Revise preserved; no significant divergent decision or new critique required | PC-002 resolved; PC-001 substantially implemented but not fully achieved because RV-001 |
| P02-T01 | Historical, non-safety display with meters, static plots and table | Research C1/C6/W1 and PC-002; existing generated readings are historical | Latest/fault/gap semantics agree across details, code, tests and README | No material revision beyond approved direction | Reconciled |
| P03-T01 | Controlled environments; SQL opt-ins disabled; constructed reader | PC-003 and explicit owner prohibition on SQL; owner replaces full gate with listed checks | Details and changes specify env -i, ZF_TEST_MSSQL=0 and no inherited ZF settings | Compatible correction, no user decision required | Resolved in supplied execution evidence; independent run also used a cleared environment |

## Critique and Material Revision Assessment

* PC-001: partially resolved in outcome, despite the plan's "Resolved directly"
  disposition. Required predicates and case-distinct checks are present, but
  BIN2 string equality is not length-exact. RV-001 is the implementation defect,
  not a repeat critique or a new planning request.
* PC-002: resolved. SQL preserves null properties; channel unavailable states
  are distinct from malformed-envelope denial; latest never silently falls back.
* PC-003: resolved by the recorded cleared subprocess environments and disabled
  SQL opt-ins. The browser harness constructs its reader and never enters the
  SQL-configured application entry point.
* No significant or divergent implementation-time decision was found. Optional
  source-table binding and historical rather than live values preserve intent
  and are recorded consistently in plan/details/README.
* No evidence of dependent work resuming before required compatible critique
  corrections. The original critique and its Revise outcome remain intact.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Source-view apply and populated SQL verification | SQL execution and deployment expressly prohibited; tables may legitimately be absent | Separately authorised operator validates both branches and coordinates application/view rollout | Open distinct operational follow-up RV-002; not an active phase defect |
| Human screen-reader acceptance | Chromium DOM/keyboard checks cannot establish assistive-technology task success or approve resident wording | Named accessibility/resident reviewer records browser/AT versions and task results | Open distinct acceptance follow-up RV-003; not an active phase defect |

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: BIN2 equality still accepts padded register identities and provenance

* Related scope: P01-T01, PC-001, exact register/reading/case identity and both
  SYNTHETIC-label requirements.
* Evidence: infra/sql/resident-showcase.sql:35-41 uses string `=` with BIN2
  collation but no length or equivalent byte-exact guard. SQL Server pads
  strings to equal lengths for `=` comparisons, including binary collations.
  Thus a register home `HOME-A ` matches canonical/reading home `HOME-A`;
  register sensor `SENS-A` joins reading sensor `SENS-A `; register source
  `SYNTHETIC ` matches `SYNTHETIC`.
* Surviving counterexample: canonical/reading home `HOME-A`, reading source
  `SYNTHETIC`, and register home `HOME-A ` or register source `SYNTHETIC `
  pass the SQL predicates. src/core/src/zava_forward/core/resident_showcase.py:132-140
  checks only the retained reading home and reading source, so cannot reject the
  mismatching register fields. Sensor IDs are not retained for a Python check.
* Source basis: src/core/src/zava_forward/core/synthetic/sensor_backfill.py:47-56
  defines variable-length columns without constraints preventing these stored
  inconsistencies. The stock generator rejects padded home input, reducing
  ordinary generation risk, but that is not a database boundary guarantee.
* Test evidence: src/core/tests/test_resident_sensors.py:137-153 checks SQL
  fragments, not padding semantics; mocked parsing tests cannot evaluate joins.
  Existing passing tests do not refute this counterexample.
* External corroboration: Microsoft Learn, "= (String comparison or assignment)",
  Remarks, source date 2023-06-07, retrieved 2026-10-27:
  https://learn.microsoft.com/en-us/sql/t-sql/language-elements/string-comparison-assignment?view=sql-server-ver17.
  It explicitly documents ANSI padding for equality and that ANSI_PADDING does
  not change comparison semantics. An initial obsolete troubleshooting URL
  returned 404; the authoritative language reference above was then retrieved.
* Impact: malformed register identity/provenance can be admitted as an exact
  synthetic association, contrary to the accepted fail-closed invariant. This
  is a source-derived counterexample, not an observed SQL execution or proof of
  disclosure between two valid generated homes. Normal fixtures still isolate.
* Destination: rpi-implement.
* Smallest useful next action: make identity and provenance comparisons
  length-sensitive as well as binary, accounting for VARCHAR/NVARCHAR conversion
  before any byte-length comparison; add padded register-home, sensor-ID and
  source-label regression cases. Do not repair by trimming/normalising IDs.
  Preserve the source-only/no-SQL constraint; operational semantic execution is
  still a separately authorised follow-up.
* Publication: blocking until this accepted boundary defect is addressed.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Optional-view compilation and populated SQL behaviour remain unverified

* Related scope: P01/P03 and existing operational Follow-Up Item.
* Evidence: changes Validation Record explicitly excludes T-SQL compilation and
  SQL integration. infra/sql/resident-showcase.sql:26-75 selects the branch at
  apply time, then creates the view dynamically. Absent tables yield the typed
  NULL/empty JSON branch; later table creation alone will not rebind that view.
  src/api/README.md:2928-2933 documents coordinated later view/application update.
* Impact: source review and constructed readers cannot prove dynamic view
  compilation, both optional-table branches, populated ordering/nulls or
  ownership-chain permissions. No live availability is established.
* Destination: distinct operational follow-up, not rpi-implement or rpi-research.
* Smallest useful next action: a separately authorised operator tests absent and
  populated branches, confirms exact predicates and view-only principal rights,
  and coordinates apply/deployment after accepted source corrections.
* Publication: not independently blocking a source-only PR; blocks claims of
  live integration readiness. No SQL or Azure operation is authorised here.

<!-- rpi:review id=RV-003 -->
### RV-003 [Low]: Assistive-technology and hosted acceptance remain separate

* Related scope: P02/P03 and existing human acceptance Follow-Up Item.
* Evidence: supplied browser results cover Chromium DOM, keyboard focus,
  disclosure, reflow and static reduced-motion states. No human screen-reader
  session, hosted CI/rubric result or independent hosted exact-head assessment
  is supplied. The WCAG baseline explicitly distinguishes engineering checks
  from human conformance/acceptance.
* Impact: accessible source semantics and local checks do not prove screen-reader
  task success, approve resident-facing wording or satisfy hosted/human gates.
* Destination: distinct accessibility/hosted follow-up.
* Smallest useful next action: named human reviewer records actual AT/browser
  task results; parent preserves normal hosted review/check gates before merge.
* Publication: not independently blocking a source-only PR, but no accessibility
  conformance, hosted-pass or approval claim may be made.

## Defects

* RV-001: exact register-side identity/provenance remains incomplete; route once
  to later rpi-implement. No UI implementation defect found in changed hunks.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| RV-001 | rpi-implement | Parent arranges source-only length-sensitive equality and regressions | Defect within the already accepted direction, not a new design decision |
| RV-002 | Distinct operational follow-up | Separately authorised operator validates/applies the view | Prohibited and explicitly deferred live integration |
| RV-003 | Distinct human/hosted acceptance follow-up | Accessibility reviewer and parent/PR reviewers | Engineering checks do not grant human or hosted acceptance |

Later implementation of RV-001 does not require another Review. Preserve this
original finding and outcome; record correction evidence in later implementation.

## Residual Work

* RV-002 and RV-003 remain outside active P01-P03 scope and are not defects.
* Real SQL compilation/integration, human screen-reader work and hosted review
  remain unrun, not implicitly passed. No full local gate was run or required by
  the task-specific owner instruction.

## Blockers and Remaining Work

* Review execution blockers: none.
* Candidate publication blocker: RV-001.
* Remaining active implementation markers: none; completed work still requires
  the routed defect correction before candidate acceptance/publication.
* No source fix, plan mutation, Git write, deployment or subsequent Review was
  performed.

## Validation Evidence

| Command or evidence | Scope | Status | Summary |
| --- | --- | --- | --- |
| Cleared-environment candidate commands in changes record | Core/API full unit discovery | Passed, supplied | Core 1380 tests / 186 skipped / 624.748s; API 1068 / 308 skipped / 721.139s; not rerun |
| Focused candidate commands in changes record | Boundary and generator/API | Passed, supplied | 113 tests / 19 skips; 65 tests; not rerun wholesale |
| Ruff check/format and mypy commands in changes record | Four changed core and two changed API Python files | Passed, supplied | Changed-file lint/format and types; no fresh independent lint claim |
| python src/api/checks/resident_sensors_browser_check.py | Real loopback app, fresh generator output, constructed reader, Chromium | Passed, supplied | 23 assertions; harness source inspected; no SQL/integration inference |
| env -i PATH=<session-venv>:/usr/bin:/bin HOME=<session-files> PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src/core/tests:src/api/tests ZF_TEST_MSSQL=0 <session-venv>/python -m unittest test_resident_sensors test_resident_demo_api.SignInTests.test_sensor_history_is_session_owned_and_rechecked -q | Independent focused boundary regression | Passed, independently executed | Nine tests, 0.717s; no SQL integration imports enabled |
| git diff --check 55c239d9 61c9e98b | Candidate diff | Passed, independently executed | No whitespace errors |
| Fresh Web Interface Guidelines fetch and changed-hunk source assessment | demo.js/demo.css only, with existing semantics/token context | Passed by inspection | All fetched rule categories considered; grouped results below; human AT not run |
| T-SQL compile, real SQL, Azure, deployment, full gate, private data | Explicitly excluded | Not run | Owner boundary preserved |
| Human screen reader and hosted review/checks | Later acceptance | Unavailable/unrun | Residuals RV-002/RV-003 remain open |

The session venv is
/home/azureuser/.copilot/session-state/05da8f58-6691-4faf-a297-cc25ae7c428d/files/venv;
session-files is its parent. The independent test used that exact interpreter.
No environment values, .env, private dataset or verifier file were read.

### Fresh web-guideline assessment

Source retrieved in full on 2026-10-27:
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md.
Reviewed the changed demo.js/demo.css hunks against every fetched category:
accessibility, focus, forms, animation, typography, content handling, images,
performance, navigation/state, touch, safe areas/layout, theming, locale,
hydration, hover, copy and listed anti-patterns. Categories without a changed
surface are not applicable, not claims about the entire site. Existing native
focus/skip/status context was read only to interpret the changed components.

#### src/api/src/zava_forward/api/resident_demo/web/demo.js

* src/api/src/zava_forward/api/resident_demo/web/demo.js:31-168 - pass:
  native labelled meters; named/described static SVG; exact native table with
  caption and scope; keyboard disclosure/scroll region; empty/fault text;
  bounded history; Intl values/times and exact datetime alternatives.
* No new form, image asset, route/filter, destructive action, animation,
  hydration surface or gesture-only interaction. Disclosure need not become a
  URL-authoritative home selector. No innerHTML or user-controlled markup.

#### src/api/src/zava_forward/api/resident_demo/web/demo.css

* src/api/src/zava_forward/api/resident_demo/web/demo.css:67-86 - pass:
  responsive grid, minimum-width handling, table-contained horizontal scroll,
  numeric alignment, inherited focus-visible, native disclosure hit area and
  hover, static charts, and existing Fluent aliases.
* Repository plain ASCII punctuation and sentence case take precedence over
  generic curly-quote/ellipsis/title-case preferences. These are justified
  standards choices, not findings. No unrelated header or whole-site audit.

## Outcome

* Outcome: Not accepted.
* Rationale: completed source work and permitted validation support the normal
  own-home display, unavailable-state contract and accessible engineering
  patterns, but RV-001 violates an explicit exact-match boundary. Passing
  source-fragment/mocked tests cannot establish the missing SQL semantics.
* Severity summary: 0 Critical, 0 High, 1 Medium defect; 2 Low residual findings.
* Publication should be blocked for this candidate until RV-001 is addressed.
  RV-002/RV-003 alone do not prohibit a source-only PR, but remain required
  before their corresponding live/accessibility/hosted acceptance claims.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | rpi-implement | Parent routes RV-001 for source-only correction and regressions |
| Decision gap or invalid assumption | None | No divergent decision found |
| Material evidence gap | None requiring rpi-research | SQL semantics corroborated by official language reference; operational evidence remains explicitly deferred |
| Non-blocking residual work | Distinct operational and accessibility/hosted follow-ups | RV-002 operator; RV-003 named human/PR reviewers |

* Execution status: Complete.
* Outcome: Not accepted.
* Validation coverage: independent nine-test SQL-free run and diff check; supplied
  full unit, lint/type and 23-assertion Chromium evidence; fresh UI source review.
* Blockers: RV-001 blocks candidate publication. SQL/human/hosted checks unrun.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-27/resident-sensors-plan.md](.copilot-tracking/plans/2026-10-27/resident-sensors-plan.md) | Complete P01-P03 plan and follow-ups |
| [.copilot-tracking/details/2026-10-27/resident-sensors-phase-details.md](.copilot-tracking/details/2026-10-27/resident-sensors-phase-details.md) | Boundary and unavailable-state contract |
| [.copilot-tracking/reviews/plans/2026-10-27/resident-sensors-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-27/resident-sensors-plan-critique.md) | Preserved original critique and dispositions |
| [.copilot-tracking/research/2026-10-27/resident-sensors-research.md](.copilot-tracking/research/2026-10-27/resident-sensors-research.md) | C1-C7/W1 evidence and selected direction |
| [.copilot-tracking/changes/2026-10-27/resident-sensors-changes.md](.copilot-tracking/changes/2026-10-27/resident-sensors-changes.md) | Supplied implementation/validation record |
| [.copilot-tracking/reviews/logs/2026-10-27/resident-sensors-review.md](.copilot-tracking/reviews/logs/2026-10-27/resident-sensors-review.md) | This task's one independent Review |

## Next Steps

The active parent should route RV-001 to later rpi-implement, preserving this
Review and its original outcome, and hold candidate publication until correction
evidence addresses exact comparison semantics. Keep RV-002/RV-003 as distinct
follow-ups. Do not invoke another Review, execute SQL or expand operational
authority. No user response is required for this compatible defect correction.
