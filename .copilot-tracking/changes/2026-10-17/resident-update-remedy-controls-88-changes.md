<!-- markdownlint-disable-file -->
# RPI Changes: Resident update and remedy controls

## Metadata

* Task ID: 88; slug resident-update-remedy-controls-88; date 2026-10-17.
* Plan: .copilot-tracking/plans/2026-10-17/resident-update-remedy-controls-88-plan.md
* Details: .copilot-tracking/details/2026-10-17/resident-update-remedy-controls-88-phase-details.md

## Execution Status

Original implementation of P01-T01/T02 and P02-T01/T02 completed and evidence
reconciled before the single original Review. Coordinator-authorized correction
ONE implemented/validated for the departed-response-owner Medium finding, separately evidenced
in resident-update-remedy-controls-88-correction-one.md in this directory.
P01/P02 implementation evidence complete: 145 tests (134 pass/11 existing skips)
including actual browser, 24 shared guard tests and eight actual MSSQL tests pass;
configured core/API statics/JS pass. Source/evidence published normally as
5cfa8e53ef28fbfe2a9aae681902c4c6829d53e3 on PR392. Independent external
correction disposition pending; the interrupted broader replay is not a pass.
Original Review/critique unchanged; no new full Review or current blocker.

## Execution Summary

Actual Research and Plan/critique completed before source work. Original critique
Revise retained; PC-001/002/003/004 directly incorporated in finalized contracts.

## Completed Work

### P01-T01 domain and persistence

Existing resident records now retain full commitments and independent response/
remedy clocks/history. New writes validate named current actors, owned transitions,
explicit versions and inputs again inside existing SQL writer transaction.
Canonical discard preserves prior audit on precommit failure; committed marker
crosses domain/HTTP boundary without replay after synchronization/projection faults.
Legacy missing provenance stays unknown until explicit confirmation.
Actual semantic/HTTP run: 65 tests OK, two opt-in skips. Core and API Ruff pass;
API mypy passes. Existing original test suite not removed.

## Implementation-Time Plan and Detail Updates

### Immediately relevant current-state refinements

P01/P02: add three finance payment-note provenance assignments because existing
payment_status has no own owner/date. No financial disposition/authority change.
Actual browser exposed nested array rendering in actForm; one map-to-flatMap
correction is necessary for the existing complaint closure controls. New scoped
forms also flatten labels/inputs and retain the existing CSRF header.
An actual cold Mssql import exposed a circular top-level _actor import; lazy
import preserves the canonical actor helper. These are ordinary in-scope corrections,
not a new architecture or user decision; plan/details synchronized, critique not repeated.

### P01-T02 existing journey and P02 evidence

Full commitments and independent response/remedy owner/date/status are visible in
the existing panel. Scoped native resident forms (including existing response
actions) share inline errors and committed/uncertain outcome retry prevention,
retain drafts and reuse the existing unsaved-navigation guard. Complete handoff
snapshots are also redacted outside resident-view roles. Status dates show local
date/time; legacy missing values remain Unknown.

Existing core/API guides and resident journey synthesis record exact contracts,
compatibility change and unperformed broader acceptance. Index route is additive;
upstream KB log is an exact byte prefix, SHA256
f35003c314bd9eb31bb4bb00ee1ccb2cc93ba0b35d72610e89f428872c8f80a1.

## Validation Record

| Check | Scope | Status | Evidence |
| --- | --- | --- | --- |
| installed-src baseline | resident, handoff, HTTP | Passed | 59 tests, one opt-in skip, before edits |
| failing-first exact tests | commitment/action and remedy | Failed as expected | Unknown step and missing remedy on original source |
| changed semantic/HTTP | JSON/SQLite resident | Passed | 65 tests, two opt-in skips |
| core/API Ruff/format/mypy | configured full projects | Passed | 60/22 files formatted; 113/54 source files typed; no issues |
| first actual SQL/browser | owned local | Initially failed; corrected before Review | cold import cycle, nested label arrays and no-owned-case login wait; retained as actual failures |
| final dependent suites | JSON/SQLite, HTTP, all directly dependent closure/writer recovery | Passed | 378 tests, five opt-in skips, 127.807 seconds |
| final focused plus actual browser | resident, handoff, HTTP; Chromium | Passed | 81 tests, one opt-in MSSQL skip, 22.760 seconds |
| actual SQL Server | eleven selected exact controls/negative writer probes | Passed | 11 tests, no skips, 72.049 seconds; UUID databases in own loopback container |
| final API image | src build context, non-root/hardening and compatible startup | Passed | sha256:485706b0361ccef3f6057faaed5f4ec7aeb1c3fdfd3c485a4eb854650b5c87b9; existing check-container.py controls/negative probes pass |
| source/diff | both changed JS files parse; whitespace and KB prefix | Passed | node --check, git diff --check, exact base log byte comparison and new route targets |

### Commands and SQL boundary

Installed source packages in local .venv with pip; no mvp workaround. Full
dependent unittest selection: JsonResidentDecisions/SqlResidentDecisions,
test_handoff_lifecycle/test_handoff_api/test_workflows, JSON/SQL finance match,
test_finance_signoffs/test_finance_match_api, JSON/SQL grant lifecycle/API,
JSON/SQL hazard/API, stock/API, quality_procurement/procurement API, role matrix,
sqlstore/recovery/change_provenance and resident API. PYTHONPATH contains only
src test modules and src/api; all application imports resolve installed packages.

Actual browser: ZF_RESIDENT_BROWSER=1, test_resident_api.ResidentApi.
test_browser_commitment_reassignment_response_closure_and_remedy_reopen.
Page errors prohibited; all external requests blocked; 320/390/1280 widths and
reduced motion, keyboard create/reassign, inline refusal, response/remedy independent
closure/reopen exercised. Not screen-reader, resident research or WCAG acceptance.

Actual MSSQL: ZF_RESIDENT_MSSQL=1, MssqlResidentControls eleven new applicable
methods: complete update, incomplete/date/identity, independent close/reopen,
legacy confirmation, actionable identity/projection, mixed closure, handoff,
writer registry changes, concurrent writers, audit/recovery read faults,
post-COMMIT synchronization. Bound only 127.0.0.1:32802; task-owned
issue88-sql-3a36c179. Generated secret remains outside repository. Each test
creates/drops only its own UUID zf_resident88 database. Other inherited opt-in
MSSQL suites are not claimed run. Baseline suite skips remain documented.

Full configured checks from each src/core and src/api: ruff check .,
ruff format --check ., mypy. API image built with Dockerfile src/api/Dockerfile
and src context, then src/check-container.py api zf-issue88-api:local.

### Fresh changed-web guideline review

Source refreshed 2026-10-17 from vercel-labs/web-interface-guidelines/main/command.md;
changed portions read against all fetched rules, with owner-selected Fluent/plain
language/ASCII conventions retained over generic typography/capitalization advice.

```text
## src/api/src/zava_forward/api/web/panels.js
pass - changed resident forms: native labels/keyboard, names/autocomplete, live
errors/focus, unsaved guard, scoped retry handling and Intl dates; no added motion.

## src/api/src/zava_forward/api/web/app.js
pass - changed handoff inputs retain existing native recorded-change form and
explicit owner/due/basis route; no new navigation, layout or animation.
```

This is a changed-surface engineering review, not a fresh whole-app audit.

## Pre-Review Reconciliation

Ready: all plan tasks checked and details synchronized; no pending implementation
or validation blockers. Original Review not yet run; no human approval invented.
Original critique is retained unchanged and is not substituted for Review.

Actual shared overlap: resident_decisions.py, sqlstore.py, store.py, projection.py,
workflows.py, finance.py, server.py, panels.js, app.js, resident/handoff tests and
component guides/KB. Coordinator owns main sequencing with #91/#102. No edits to
quality.py, assistants.py, progress.py, shared API fixtures/configuration or held
#92 source; no other worktree was read.

## Blockers

None.

## Remaining Work

Own commit/push/main PR publication and owned-resource cleanup. Original Review
has completed; no implementation correction cycle was needed.

## Follow-Up Items

Full PRD lease/scope-change/age-band governance, human/WCAG and independent
coordinator final-head acceptance remain outside this bounded issue, not proven.
RV-001 distinct handoff: routing owner is planning parent/repository owner.
Next action at the next #81 backlog triage is to identify an existing separately
owned governance item or assign one, retaining Legal/Housing/Complaints approval.
No backlog item, actual service authority or band threshold is fabricated, and
no new child work starts here.

## Original Review Result and Post-Review Routing

Exactly one original full-task Review ran after evidence reconciliation at
.copilot-tracking/reviews/logs/2026-10-17/resident-update-remedy-controls-88-review.md.
Execution Complete; outcome Residual work; RV-001 Low is the separately owned
governance handoff above. No implementation defect established. Review retained
unchanged; no second full Review, source correction or coordinator Pass.
Post-Review updates only assign the next routing action in plan/details/changes/
state, not pretend the broader governance work or independent acceptance is done.

## Return-to-Caller State

Task phases complete. Published https://github.com/jmservera/ama/pull/392 against
main, implementation head 2672dcbb968524b734e34666c3114439e0472c14. Normal push,
fresh authenticated GitHub noreply author/committer and required Copilot trailer.
Original Review retained unchanged, SHA256
204aab7fa36e86feae5b5f76a2107e8e7a2655a6b11a6d2113a3c231ea008e99.
Final publication/state bookkeeping is a separate normal commit, not an amend.

Verified exact owned SQL container ID, then removed issue88-sql-3a36c179, own
API image tag and generated external credential/named logs. Only task resources
were removed. No other worktree or private data touched.
Automatic session stopped at the explicit user-selected PR endpoint; no child
task, second critique/Review, merge, rebase, force push or issue closure.
Resume ID: 3a36c179-e1e3-4332-9c33-fa947262fd79.

GitHub reported no check results at initial PR publication; no remote CI or
independent final-head coordinator acceptance is claimed. Local evidence above
is complete for the bounded criteria. Owner/coordinator retains integration,
checks and merge decision; planning parent/repository owner retains RV-001's
next #81 backlog routing action.
