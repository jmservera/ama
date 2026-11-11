<!-- markdownlint-disable-file -->
# Task Research: Issue 134 connected same-home screen walk, smallest remaining slice (2026-11-11)

* Task: `134-connected-plan-1111`, slug `connected-plan-134-1111`; parent lineage: `134-keyboard-c4-1110` (delivered as PR 1414)
* Worktree `issue-134-connected-plan-1111`, branch `docs/demo-connected-walk-plan-134-1111`, target `main`, base `35eb0e559c7d0660ab87594732675b71be7bee67` (asserted equal to HEAD and merge-base; worktree clean before first write)
* Research disposition: executed (source inspection only; no runtime, browser, install, provider call, issue or PR write)
* Planning Readiness: Ready for planning. The slice below is actionable local engineering. No owner decision blocks planning; implementation still needs Root admission (see plan)

## Scope

Issue #134 (open) unmet criteria, quoted literally:

* C1: all eleven perspectives expose an entry, evidence inspection, safe endpoint, recovery route and accountable handoff over linked records
* C2: AC-034 to AC-043 pass or are recorded as deferred with reason
* C5: walkthroughs keep textual state meaning, keyboard operation and status announcements

Ticked and not re-examined: same-home EPC conflict to financial closure journey (Store/JSON), sibling and building negative controls, constructed-fixture labelling. Related #233 C4 (unticked) asks that a same-home connected journey is walked across role screens without relabelling separate examples as stages of one home. This plan neither ticks nor claims any criterion.

Excluded: any C5 keyboard-probe correction (corrections C1 to C4 of the original five are spent, one remains, this launch consumes and authorises none), #233 and #80 corrective authority, exhausted #135/#80/aftercare lineages, #1401/#1402 defects (separately owned, unmodified), #144/#131/#132 finite extensions.

## Prior evidence reused, not re-observed

| Evidence | What it already gives | Boundary |
| --- | --- | --- |
| [walkthrough planning matrix](./2026-11-10-walkthrough-plan-134-1110-research.md) | Eleven-perspective matrix, AC-034 to AC-043 mapping, served-screen registry, local-check constraints | Source inspection only. Every row "partial at best" |
| [`journey_trace.py`](../../src/core/src/zava_forward/core/journey_trace.py), [`test_journey_store.py`](../../src/core/tests/test_journey_store.py), [`test_journey_trace.py`](../../src/core/tests/test_journey_trace.py) | Real-Store same-home journey (conflict, correction, independent decisions, handover, financial closure), ordered, with Unknown intervals and sibling/building negatives | Core and audit chain only. Nothing in `src/api` or the web layer imports `journey_trace` (grep on this head); no screen shows event order |
| [`specialist_keyboard_browser_check.py`](../../src/api/checks/specialist_keyboard_browser_check.py) (PR 1414, merged 2026-11-10) | Per role, per screen keyboard walk, focus measurement, `#workspace-status` contract, evidence regions, handoff link, reset | Selects the first permitted home on each screen independently (`HOME = "a.item"`, `walk_screen`), on the `synthetic_data()` fixture with ZF-1, ZF-4, ZF-5. It is a per-screen walk, not one home carried across screens. DOM evidence, not AT |
| [`role_screens_browser_check.py`](../../src/api/checks/role_screens_browser_check.py) selectors `226` to `232s` | Per-story exact evidence for ZF-1 | Each story builds its own fixture (`role_screens_fixtures.py`: `synthetic_data`, `technical_quality_data`). The check text "same home remains ZF-1" asserts the label only. Several stories sharing the id ZF-1 are separate examples |
| [`programme-queue` screen and `journeyStageMap`](../../src/api/src/zava_forward/api/web/role-screens.js) (lines 478 to 531) | Same-home step table and links that preserve `case=<id>` | The eight-stage map is labelled in source "a design hypothesis, not observed behaviour". Its eight stages do not equal the five-stage core trace. Neither may be presented as an observed eight-stage consistency |

## Source findings that decide the slice

1. Specialist screens already carry the selected home across screens. `roleScreensView` builds the menu with `screenHref(item.id, caseId)` (role-screens.js lines 40 to 48 and 68) and supports `#/screens?screen=<id>&case=<home>`. Switching screen keeps `case=`. No application change is needed to hold one home across screens within one signed-in role.
2. Role screens render from the case detail the real Store holds: `technical-queue` (`c.technical`, `c.stock_reconciliation`), `quality-queue` (`c.quality`, handover), `resident-choice` (`c.measure_decisions`), `finance-invoices` (`financeInvoicePanel(c)`, `/api/finance`), `asset-board` (`c.stock_reconciliation_events`), `programme-queue` (`programmeGates`). The Store journey already writes exactly these records for ZF-1. So a served copy of the journey result could populate the existing screens. This is a static inference; it is unobserved at runtime and each screen is a "confirm at first run" item.
3. No maintained fixture serves that journey. The browser checks use bespoke fixtures; the core journey runs in a temp `Store` inside unit tests and is never served. `design_system_browser_check.main` takes a `data_factory` returning the data dict (`json.dumps(data_factory())`, lines 276 to 280), so a factory can return the data of a Store driven through the journey. The Store audit chain is a separate `audit.jsonl` (`store.py` lines 57 to 63) and is not needed by any screen.
4. Precedent for importing core test helpers from an api check exists: `home_case_browser_check.py` inserts `src/core/tests` on `sys.path` and imports `building_fixture` (lines 17 to 24).
5. The journey actors are fixture staff in [`test_finance_signoffs.py`](../../src/core/tests/test_finance_signoffs.py) `STAFF` (GEO-1, PM-1, PM-2, QI-1, RC-1, RC-2, BSL-1, RLO-1, RLO-2, CON-1; password login shares one synthetic password under the harness). They are fixture identities, not authentication, human acceptance or owners.
6. New dependency drift, source-derived. `staff-job-pack-intake` (#132, PR 1425, 2026-11-11) registers a fourteenth specialist screen for seven roles (`staff-intake.js` lines 4, 137 to 140; loaded in `index.html`). The merged keyboard probe enumerates every served screen and `region_failures` fails any screen with neither a declared region expectation nor a declared gap (probe lines 148 to 169). The probe was merged 2026-11-10, a day before this screen, so it will likely fail on the new screen. This is unobserved (no run was admitted), it is not repaired here, and it is a separately owned matter because the probe correction balance is not extended. Consequence for the slice: a new check must name its own explicit screen chain and never enumerate the menu.
7. #132 intake and #133 aftercare are on main and are not stages of the Store journey (which starts at the EPC conflict). Stage 1 in `journeyStages` ("no screen yet") predates the intake screen, which shows worker job-pack evidence for a work order, not a source account. Whether that wording is stale is not decided here; the slice treats the intake, aftercare and entry-by-report stages as deferred.
8. What the screens cannot show: event order and unknown intervals live only in the core trace. Exposing them on screen would be a new endpoint or panel, which is an application change and not the smallest slice.

## Does the current source already permit one connected record?

Partly, with one narrow gap.

* Permits: signing in once as one fixture role, entering Specialist screens by keyboard, and walking several screens for one named home with `case=` preserved; each screen then shows its own domain state; the home link goes to `#/case/<home>`; Reset screen view is the recovery route; `#workspace-status` names role, screen and home.
* Does not permit with existing fixtures: a served home whose records across conflict, technical, resident, quality and finance already hold the Store journey result. No maintained fixture does that.
* Does not permit by design (existing roles): one role seeing every screen. Role projection splits the journey across roles (below). A same-home walk across roles needs one login per role, each deep-linked to the same home, with the home identity re-asserted by each screen. This is a legitimate "same home across role screens" but it is not a continuous session and must be reported as such.

So a narrowly scoped fixture factory plus a new checker is genuinely needed; no application, API, workbench-manifest or core change is needed on current source evidence.

## Smallest useful subset of the eleven perspectives

Role to screen mapping from the registries (`screenManagers`, `technicalRoles`, `qualityRoles`, `choiceRoles`, `financeRoles`) and the journey actors:

| Journey stage (core trace) | Journey actor in fixture | Screen | Perspective row (prior matrix) |
| --- | --- | --- | --- |
| EPC conflict and correction | PM-1 raises, PM-2 resolves (Retrofit Programme Manager) | `asset-board` | 1 Asset and investment (proxy: no asset role) |
| Independent technical decisions | RC-1, RC-2, QI-1, BSL-1 | `technical-queue` | 3 Retrofit case team, 4 Assessor, designer and Coordinator |
| Resident decision | RLO-1 | `resident-choice` | 5 Housing and Resident Engagement |
| Quality acceptance and handover | QI-2, RLO-1 | `quality-queue` | 9 Quality and assurance |
| Financial closure | GEO-1, PM-2 | `finance-invoices` | 10 Finance and Grants |
| Cross-stage same-home states | PM-1 | `programme-queue` | 2 Programme coordinator |

Proposed subset: seven perspective rows (1, 2, 3, 4, 5, 9, 10) over six screens, all for the home ZF-1 on one fixture. Explicit deferrals, not inferred and not relaxed:

* 6 Repairs and Building Safety: the journey holds no hazard, so `safety-lead` and `hazard-triage` for ZF-1 would show no records; the BSL actor gives a building sign-off only.
* 7 Procurement and contract manager: the journey commits and invoices work orders but does not feed `procurement-packages` (package queue), and there is no login role.
* 8 Provider and contractor contact: no contractor submission or correction in the journey; CON-1 acts in no step.
* 11 Digital operator and auditor: no journey link and no login role.
* Entry by report or nomination, intake, aftercare: not Store journey stages. The word "entry" in the slice means the case list to Specialist screens menu, as in the prior probe.

The proposed subset is a proposal only. It is not an approved perspective mapping; Asset (row 1) is a proxy through the Programme Manager, and constructed roles carry no authority.

## What would count as engineering proof, and what it never is

Engineering proof (constructed fixture, DOM, local): one run in which the same served home ZF-1 shows on each of the six screens, by the roles named, its own journey-derived state and the selected-home heading and status text; the existing case-workspace link targets ZF-1; Reset recovers; sibling ZF-2 on the same screens does not show the ZF-1 journey states (screen-level negative control); every claim is recorded as `observed`, `gap` or `not-run` text and is never summarised as a pass.

Never established by this proof: eleven-perspective coverage, AC-034 to AC-043 pass, AT or screen-reader output, user validation, WCAG conformance (baseline proposed, pending O-1), authentication, any human, resident, professional or control-owner approval, event-order display on screen, operational timings, live or production acceptance.

## Constraints for any later implementation

* Owned local synthetic environment: harness `main` starts its own loopback server with temporary `ZF_DATA`, `ZF_STATE`, `ZF_STORE=json`, `ZF_PASSWORD=synthetic-check`; no default dataset, no private data, no `.env`.
* Install the `src/<project>` distributions into a throw-away environment outside the checkout (no `PYTHONPATH=mvp`), prove imports resolve inside the worktree, Playwright Chromium present, canonical heavy lock `/tmp/ama-rpi-heavy.lock` with `flock -n`, scratch `ZF_BROWSER_SCRATCH` short absolute path outside the checkout, pinned axe file only if present locally (else "axe not run"). These are future prerequisites; none was touched now.
* Hosted CI does not reference the browser checks in the prior grep; a new browser check would be a local-only direct check and must be reported so.

## Retrieval and review notes

* Web Interface Guidelines source (`https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md`) not refetched: no web file is edited or reviewed in this documentation-only planning candidate. Any future edit of web-facing check output must refetch it. No conformance is inferred.
* Not performed: any runtime, browser, axe, install, test run, reading of every check body. Source references above are static greps and reads on this head.

## Follow-ups (ranked, for later user-selected work)

1. Root decision whether the proposed connected-home check fits the remaining original-history allowance or is classified as a new slice (not decided here).
2. Separately owned: the keyboard probe's undeclared-screen expectation for `staff-job-pack-intake` (unobserved).
3. Deferred rows 6, 7, 8, 11 need fixtures that do not exist; each is its own scoped decision.
