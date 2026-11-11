<!-- markdownlint-disable-file -->
# Plan: Issue 134 connected same-home screen walk, one bounded checker slice (2026-11-11)

* Task `134-connected-plan-1111`; base `35eb0e559c7d0660ab87594732675b71be7bee67`; branch `docs/demo-connected-walk-plan-134-1111`
* Research: [research](../research/2026-11-11-connected-plan-134-1111-research.md); details: [details](../details/2026-11-11-connected-plan-134-1111-details.md); critique: [critique](./critiques/2026-11-11-connected-plan-134-1111-plan-critique.md); state: [state](../rpi-sessions/2026-11-11/connected-plan-134-1111-state.json)
* Status: planned, not started. This is a documentation-only planning candidate (Markdown, link and diff checks, no runtime gate). No source, fixture, test, checker, install, browser, provider, issue, PR or board action is admitted. Implementation needs a separate Root admission.

## Objective

Define the smallest remaining engineering slice that could advance literal criterion C1 (and supply evidence toward the C2 disposition of AC-036, AC-040 and AC-043 and #233 C4) by walking one home, ZF-1, across role screens using records produced by the real Store journey, instead of separate per-screen examples. It never ticks, relaxes or claims C1, C2 or C5.

## Decision recorded for Root (not approved here)

* Readiness: Ready. Actionable local engineering exists; no owner decision is needed to plan it.
* Proposed slice S1: one new local browser check `src/api/checks/connected_home_browser_check.py` that serves a data factory built from the real Store journey, plus one pure-helper test `src/api/tests/test_connected_home_check.py`. No application, API, manifest, core, workflow or existing check change.
* Classification question for Root (not decided): whether a new check file counts against the original five-total correction history (C1 to C4 spent, one left) or is a new slice. This plan consumes no correction and authorises no C5. If Root classifies S1 as a correction, it must not start without the remaining allowance being explicitly spent.
* If Root does not admit S1, the precise blocker is admission, not evidence: the source already permits the walk, and nothing else is missing.

## Owned paths

| Path | Action if admitted | Why |
| --- | --- | --- |
| `src/api/checks/connected_home_browser_check.py` | Create | Factory plus keyboard-driven same-home walk, local-only |
| `src/api/tests/test_connected_home_check.py` | Create | Pure helper tests (no browser) |
| `src/api/README.md` | Edit one short paragraph | State the check, its limits, how to run it |
| `.copilot-tracking/{research,plans,details,changes,reviews}/...-connected-impl-...` | Create at implementation | Dated RPI evidence for the implementation task |

Not owned and not touched: `specialist_keyboard_browser_check.py` and its test (probe stays as merged), `workbench-manifest.json`, `perspective_walkthroughs.py`, `journey_acceptance.py` (registers stay partial/unmet/deferred), `role-screens.js`, `journey_trace.py`, `test_journey_store.py`, `src/api/checks/role_screens_fixtures.py`, any #1401/#1402, Atlas, aftercare, intake or #135/#80 file.

## Prior evidence and dependencies

* Reused, not re-run: PR 1414 probe and its qualifications, the 2026-11-10 walkthrough matrix, core Store journey and negatives, `home_case_browser_check` import precedent.
* Reuse points: `design_system_browser_check.main/check`, `workbench_browser_check.MANIFEST`, probe helpers `expected_status`, `status_contract_failures`, `focus_failures`, `tab_to`, `login`, `wait_status` (read-only import), `test_journey_store.StoreJourney` (setUp and `journey()`, unmodified), `test_finance_signoffs.STAFF`.
* Source-derived dependency: the 14th specialist screen `staff-job-pack-intake` exists; the S1 check names its own screen chain and must never enumerate the menu (see research finding 6). The probe's possible undeclared-screen failure is unobserved and separately owned.
* Genuine external prerequisites for a future run: worktree-venv install of the five distributions, Playwright Chromium, heavy lock, short scratch, optional pinned axe. Not touched now.

## Smallest missing behavior or proof

A served same-home record across conflict, technical, resident, quality and finance screens, walked with the same home id on each, with Unknown stated where a screen holds no record. Nothing else is missing for this slice.

## Proposed walk (design to confirm at implementation start; not approved)

Fixture: Store driven through `StoreJourney.journey()` on `dataset.DATA`, data dict returned to the harness. Home ZF-1, sibling ZF-2.

| Step | Fixture login (role) | Screen | Same-home assertions |
| --- | --- | --- | --- |
| 1 | `pm-1@example.test` (Retrofit Programme Manager) | entry via Specialist screens menu, then `asset-board` | heading names ZF-1; source conflict SQ-1 shown "Reconciled (recorded by a named person)" with its owner; status text role, screen, home |
| 2 | same session, no reset between steps 1 and 2 | `programme-queue` via the in-page menu link | `case=ZF-1` retained in the link; panel "Connected view for ZF-1" and the "Same-home step states" table present; stage map links keep `case=ZF-1`; the "no stage clears another" sentence is reported as a source statement only |
| 3 | `rc-1@example.test` | `technical-queue` | sign-offs for ZF-1 with named person and design version, or recorded Unknown |
| 4 | `rlo-1@example.test` | `resident-choice` | decision for ZF-1 Loft insulation as recorded; not a message or consent claim |
| 5 | `qi-2@example.test` | `quality-queue` | accepted and handed-over record for ZF-1 with named people |
| 6 | `geo-1@example.test` | `finance-invoices` | invoice INV-100 for ZF-1 with the recorded status; payment is outside this system |
| 7 | each | case-workspace link | `href` targets `#/case/ZF-1` |
| 8 | each | Reset screen view | status returns to "No home selected." |
| N1 | PM session | `asset-board` and `technical-queue` for ZF-2 | no ZF-1 conflict, sign-off, decision, quality or invoice state appears; states read Unknown or not recorded |

Keyboard operation: only Tab, Shift+Tab and Enter between entry, menu, screen, home, region, link and reset on each step, reusing the probe's measured-focus and status helpers. Each assertion is reported as `observed`, `gap` or `not-run` text.

## Static proposed selectors (future, not run now)

From `src/api` in the exact worktree environment:

* `PYTHONPATH=../core/tests:../agents/tests python3 -m unittest tests.test_connected_home_check tests.test_specialist_keyboard_check -q` (pure helpers; the second is the unchanged probe test, to show no regression)
* `PYTHONPATH=../core/tests python3 -m unittest test_journey_store test_journey_trace -q` from `src/core/tests` (the unchanged core journey, to show the factory input stays valid)
* `ZF_BROWSER_SCRATCH=/tmp/z134c python -m checks.connected_home_browser_check` wrapped in `flock -n /tmp/ama-rpi-heavy.lock` (local-only direct check)
* `python3 tools/rpi-checks.py --changed` optional only; never replaces the planned checks above
* Documentation: Markdown link review and `git diff --check` for the README edit

## What would count as successful engineering proof

* The check, run once on the admitted head, exits zero only when every required journey-record marker for the six screens is `observed` in ZF-1 selected-home evidence (a missing marker fails; `gap` is allowed only for declared deferrals or a screen P1 proves cannot render a Store field), the sibling ZF-2 control is rejected, every run-only mutation control is rejected, no uncaught page error, and the fixture factory proven to leave `test_journey_store` unchanged and green.
* The report prints the explicit subset (seven perspective rows, six screens) and the explicit deferral list below, and states "no AC and no criterion is passed by this check".
* Raw logs retained outside the checkout.

## Remains human, user, AT, consent or professional approval

User validation (OQ-004, OQ-005, OQ-011); assistive-technology and screen-reader output; WCAG conformance and owner confirmation O-1; any role mapping or proxy (Asset through the Programme Manager is a proxy); resident consent and handover meaning; control-owner, professional and legal approval; actual payment and funding decisions; hosted CI outcome; independent exact-head review; owner decision on ticks and `Closes` versus `Refs`. No real approval is invented, and every fixture identity is a constructed role, not authentication.

## Explicit deferrals (exact smallest subset, nothing relaxed)

* Subset delivered by S1: perspective rows 1 (proxy), 2, 3, 4, 5, 9, 10.
* Deferred: row 6 Repairs and Building Safety (no hazard in the journey), row 7 Procurement (journey does not feed `procurement-packages`; no login role), row 8 Provider and contractor (no submission step), row 11 Digital operator and auditor (no journey link, no login role); entry by report or nomination, intake and aftercare stages; screen display of event order and Unknown intervals (needs a new endpoint or panel, an application change outside this slice); eight-stage screen consistency (the stage map is a design hypothesis and is not claimed); AC-034 to AC-043 dispositions (S1 supplies evidence toward AC-036, AC-040 and AC-043 only; each remains Partial or Deferred); C5 status announcement and AT acceptance.

## Phases (all gated on Root admission)

| Phase | Content | Needs |
| --- | --- | --- |
| P0 | Root admits S1 and records the correction-balance classification; fetch main; fresh venv outside checkout; confirm imports resolve in the worktree; heavy lock free | Root admission |
| P1 | Static confirmation that each of the six screens renders from Store-journey fields (no run); if a screen cannot, record a source-bound gap, do not change application source | P0 |
| P2 | Write factory, helpers and check; write pure-helper test | P1 |
| P3 | Run the selectors above; capture logs externally | P2 |
| P4 | README paragraph, KB log entry, index if a KB file changes | P3 |
| P5 | One independent Review; findings route to later work | P4 |

Tier classification (to record at implementation): focused tier, because the change adds a local check, a pure test and one README paragraph and touches no workflow, dependency manifest, Dockerfile, permission, secret, deployment or gate semantics. Doubt, a gate-tool or hosted-check edit, or any application change escalates to the full tier.

## Stop conditions

Root admission missing; heavy lock held; imports outside the worktree; need of the default or private dataset; a screen requiring an application change to show a Store-journey record (record as a gap and stop that step); any need to edit the probe, registers, #1401/#1402, Atlas or aftercare source; any result that tempts a pass or tick.
