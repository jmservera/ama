---
title: Issue 73 workbench integration plan (exception screen child 135)
ms.date: 2026-11-07
---

* Research: `.copilot-tracking/research/2026-11-07-issue73-workbench-integration-research.md`. Details: `.copilot-tracking/details/2026-11-07-issue73-workbench-integration-details.md`. State: `.copilot-tracking/rpi-sessions/2026-11-07/issue73-workbench-integration-state.json`.
* Tier: FOCUSED (SMALL new UI integration over an already authorized endpoint). No backend, auth, store, schema, model or infrastructure change, no new dependency or framework, no new model call, no AI recovery agent, no autonomy activation. Any such need, or growth to a big scope, stops the work for reclassification and coordinator instruction.
* Reference ids: base `23b26a7f3a4693cd20dcf0447303d97491096cb3`; child commit `26ce7c711ebffb37129fe0ca24b7b94c0d8356e1`, tree `ccf89ee645b2cb00c9662ae6d42ded586e4ea9c7`, branch `feat/operator-exception-api-screen-135`.
* Status: PLANNED ONLY. Phases 1 onward are blocked. No implementation or Review has executed and none is claimed.

## Stop line for this launch

Research and plan complete. Stop pending the child's selected-tier validation (browser feature check, `Register` and `Endpoint` classes, native `--changed`), independent exact-head assessment and merge into `feat/workbench-integration-73-demo`. Implementation and Review are not started. The shared heavy lock is reserved for #135, so no heavy or service check runs under this plan until the coordinator admits it.

## Phases

* [ ] Phase 0 (gate, owner is the child): child gate passes, independent assessment records the exact head, child PR (target this topic, `Refs #135`) is merged. BLOCKED, not controlled by this loop.
* [ ] Phase 1 (re-baseline): fetch `origin/main`; record new base, new topic head and whether #1239, #1240 or others changed `src/core/.../store.py`, `exception_register.py`, `role-screens.js` or the API tests. Re-read the merged child diff and confirm it is still only `role-screens.js` and tests. If any backend, auth, store, schema, model or infrastructure change is needed, stop and reclassify.
* [ ] Phase 2 (refresh this plan): update research and this plan with actual merged-head evidence. Execute the single final-candidate critique on the refreshed plan (critique is NOT yet executed; it must not run twice). Apply compatible findings, reject findings that conflict with confirmed decisions, ask only about significant divergences.
* [ ] Phase 3 (integration trace, no source change expected): verify in source that the merged screen preserves the existing workbench contract: manager-only host, `scope` retention, case selection dropping `exceptions=1`, other `overview(signal)` screens unaffected, no non-GET call from the new block.
* [ ] Phase 4 (precise feature browser observation): one bounded extension of the existing `src/api/checks/data_operator_browser_check.py` only if the child did not already add equivalent committed evidence; otherwise reuse and cite it. Scenarios in the details file. Runs only after heavy admission.
* [ ] Phase 5 (focused gate, current): `python3 tools/rpi-checks.py --changed` on the integrated candidate, plus the unit and authority checks below. Refresh dependents named in the re-baseline phase with actual runs.
* [ ] Phase 6 (directly related documentation, if authorized): add a short integrated-state note to `src/api/README.md` next to the existing data-operator and exception register text, naming unmet criteria. KB index and log updates and any global doc edits need the owner's authorization and are not planned silently.
* [ ] Phase 7 (changes record): write `.copilot-tracking/changes/2026-11-07-issue73-workbench-integration-changes.md` with files, amendments, divergences and validation actually run.
* [ ] Phase 8 (single Review): one genuine `rpi-review` on the actual integrated head after independent exact-head review inputs exist. Outcome recorded separately from execution. Findings route to later work; no second Review in this task.
* [ ] Phase 9 (publication, authorized only): fresh GitHub privacy-safe local author and committer, canonical Copilot trailer, PR from this topic to `main` with `Refs #73` and `Refs #135` only (no closing keywords, no epic ticks) and an explicit list of unmet criteria. Hosted checks, independent exact-head review and human approvals are required and are not implied here.

## Validation plan (tier FOCUSED, run only after gate and heavy admission)

* Unit and authority, from `src/api` with `PYTHONPATH=../core/tests:../agents/tests`: `test_exception_register` (`Register`, `Config`, `Endpoint`), `test_exception_register_screen`, `test_data_operator_screen`, `test_role_screens`, `test_role_screens_conformance`, plus the API suite parts for any dependent the re-baseline names. Actual results only; a rubric score is not evidence.
* Browser: precise new-feature observation per the details file; record browser, viewport and keyboard steps actually performed.
* Native gate: `python3 tools/rpi-checks.py --changed` on the exact committed candidate, with the receipt kept external. The complete gate is not planned (focused tier, owner decision D4) unless the re-baseline shows a big or sensitive change.
* Independent review of the final head against the current target `main`, and all hosted checks, are required. Child gate results are inputs only.

## Truthful trace rows (planned content of the integration evidence; current status in brackets)

| Row | Requirement or behaviour | Evidence required | Status |
| --- | --- | --- | --- |
| T1 | Existing `/api/exceptions` producer and view authority are unchanged | `Register` and `Endpoint` results plus empty diff of server, store, `exception_register.py` | Source-observed at base; not re-run; pending |
| T2 | Manager-only screen host; named non-manager refused at host | role screen conformance plus browser observation as a non-manager | Pending; F3 owner decision open |
| T3 | Audited read-only GET only on explicit request | request log shows no `/api/exceptions` call on default load and exactly one GET after the link; no non-GET | Pending |
| T4 | Failure and quarantine versus workflow-only distinguished | synthetic quarantined, fell-back and workflow-only fixtures render the fixed wording; no model call | Child renderer tests passed; browser pending |
| T5 | Manual and no-write paths | no control other than the link; manual guidance labelled placeholder, not an approved runbook | Child source test passed; browser pending |
| T6 | Conflict values with provenance; Unknown handling | both values with source, date, version, owner; eligibility Unknown; no winner | Child renderer tests passed; browser pending |
| T7 | Denied, unavailable, aborted and stale rows | 403 text, 500 and malformed show no rows; superseded navigation renders nothing | Child renderer tests passed; real DOM pending |
| T8 | Keyboard and narrow reflow | tab order, focus visible, scroll regions focusable, 320 px reflow without loss | Pending; engineering only, no AT claim |
| T9 | No model call, AI agent or autonomy change | empty diff outside `role-screens.js` and tests; network log | Child source observed; pending |
| T10 | Dependents after main moves | actual refreshed API and core runs on integrated head | Pending; possible #1239 and #1240 effects |

## Not claimed by this plan

* No #73 or #135 criterion is proven. Stabilization #440, parent traceability, role acceptance, human and AT observations, named stewards, runbooks, producers and durable recovery remain required before epic closure.
* No legal, consent, financial, human or AT approval is implied.

## Critique

* Not executed. One final-candidate critique will run on the refreshed Phase 2 plan once, after the child merge and re-baseline.

## Refresh 2026-11-07 (post-merge plan; the sections above are the preserved prospective plan)

* Status: ACTIVE for this continuation. Tier FOCUSED, rationale: small read-only UI integration over an authorized endpoint; the only planned source delta is one test, plus a bounded documentation checkpoint. No backend, auth, security, audit, persistence, SQL, deployment or infrastructure change. Any such need triggers FULL reassessment and a stop.
* Resource boundary: light local unit checks in a dedicated venv only. The selected-tier native `--changed` runner and the integrated browser observation are NOT run here; they await a new coordinator admission after the current heavy holder releases. Missing checks are open gates, not Pass.

### Refreshed phases

* [x] Phase 0: child #1257 merged into this topic (`d17aee537ec267162af106e14056440274ae589d`); coordinator-reported gate, input only.
* [x] Phase 1: re-baseline. `origin/main` unchanged at `23b26a7f…`; fast-forward of the topic completed; no foreign change, no ancestry conflict, owned files intact.
* [x] Phase 2: this refresh; critique below.
* [x] Phase 3: integration trace by source (done in research) and one host-level regression `HostIntegration` in `src/api/tests/test_exception_register_screen.py`. It loads `role-screens.js` in a node `vm` with a fake `api` and `h`, and drives `roleScreensView()`:
  * H1 manager with `exceptions=1`: host passes rows and case to `overview`; exactly one GET `/api/exceptions`; page summary still rendered; no non-GET; the register panel is passed to `show`.
  * H2 manager default hash: no `/api/exceptions` request, entry link shown.
  * H3 non-manager role: the screen is not installed; no `/api/cases` or `/api/exceptions` request.
  * H4 stale: route aborted while `/api/exceptions` is held; the host throws AbortError and `show` never receives the register or rows after the loading panel.
  * H5 denied 403: the page still shows the denied panel and no register rows.
  The test must fail if the host stopped forwarding `(signal, rows, c)` or the role filter or explicit-request rule regressed. If it cannot fail for a real seam break, drop it rather than keep a vacuous test.
* [ ] Phase 4 (open gate): browser observation DEFERRED (open gate, awaiting admission); the existing child scenarios S1 to S9 in the details file stay the plan.
* [x] Phase 5: light checks only: new and existing unit classes `Config`, `ExceptionRegisterScreen`, `HostIntegration`, `test_data_operator_screen`, `test_role_screens`, `test_role_screens_conformance`; ruff, format, mypy, `node --check`. `Register` and `Endpoint` (SQL store and local server fixtures) are heavy-class and NOT run.
* [x] Phase 6: bounded dated checkpoint in `docs/architecture/cutover-evidence-pack.md`, labelled parent-topic observed and candidate, not merged-main, Azure or human acceptance, naming source-qualified `BRD::` and `PRD::` ids, child PR and commands, limitations and remaining owners. No knowledge-base index, log, addendum or `src/api/README.md` edit unless the Review shows a stale statement.
* [x] Phase 7: changes record. Phase 8: one author Review (done 2026-11-07). Phase 9: local commit only; no push, PR, merge, rebase or retarget.

## Critique (executed once, 2026-11-07, on this refreshed final-candidate plan)

Verdict: proceed with direct amendments.

* C1 (applied): a host-level test that only re-reads source text would be vacuous; H1 to H5 must execute `roleScreensView` and assert recorded calls and `show` arguments.
* C2 (applied): the original plan listed `Register`, `Endpoint` and `--changed` as validation. They are heavy-class and the resource boundary forbids them now; they are recorded as open gates, not dropped.
* C3 (applied): the original plan implied README updates; the plan limits docs to the evidence pack checkpoint to avoid duplicating the child's statements and to avoid global edits.
* C4 (applied): the checkpoint must not tick, close or promote draft BRD (0.21.0 draft) or PRD (0.21.0 in review) text, and must cite the coordinator-reported hosted results as reported, not observed.
* C5 (rejected, conflicts with confirmed decision): widening screen roles for named non-manager stewards; owner decision F3 stays open.
* C6 (recorded, not applied): bounding rows above 50; no latency defect reproduced, follow-up only.
