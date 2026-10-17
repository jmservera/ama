<!-- markdownlint-disable-file -->
# Review: Resident update and remedy controls

## Scope and Evidence

* Task ID: 88; slug resident-update-remedy-controls-88.
* Review date: 2026-10-17.
* Review scope: full issue task, P01-T01/T02 and P02-T01/T02.
* Assessed boundary: exact three issue criteria; current named identity and writer
  validation, legacy provenance, independent clocks, truthful recovery outcomes,
  minimal existing UI and preserved merged domains. Broader PRD lease/scope/
  age-band governance and operational/human/WCAG approval are not acceptance claims.
* Plan: .copilot-tracking/plans/2026-10-17/resident-update-remedy-controls-88-plan.md
* Phase details: .copilot-tracking/details/2026-10-17/resident-update-remedy-controls-88-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-17/resident-update-remedy-controls-88-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-17/resident-update-remedy-controls-88-changes.md
* Research: .copilot-tracking/research/2026-10-17/resident-update-remedy-controls-88-research.md
* Other evidence: current own uncommitted diff from supplied main base,
  actual regression/SQL/browser/image/static command results in changes record.

## Opening Review State

* Interpreted review goal: assess complete supplied task once against exact issue
  requirements, finalized plan/critique and actual implementation/validation;
  preserve adverse findings unchanged and route them, without self-certifying
  coordinator acceptance.
* Review scope: full task including evidence reconciliation and all implemented
  writer/error/identity/projection/closure behavior.
* Evidence readiness: all six canonical phase artifacts exist; P01/P02 task
  markers complete, details/changes reconciled, current validation recorded.
* Acceptance basis: user criteria and boundaries, plan Acceptance Criteria,
  PC-001 through PC-004 dispositions, preserved original Research and critique.
* First comparison boundary: compare requirements and finished plan markers with
  own source/test diff and recorded execution, not future service acceptance.
* Active read-only boundaries: only this canonical Review record may be edited;
  no production/test/plan/changes/research/critique mutations during Review.
  No other worktrees, private data, paid calls, external writes or second Review.
* Initial blockers: none known; substantive evidence comparison not yet executed.

## Execution Status

* Execution status: Complete.
* Review execution evidence: the original full-task comparison was performed on
  2026-10-17 in fix/resident-update-remedy-controls-88 against committed base
  1a05dfb8a4c4d9992d72a57228ce15123e9bcf2c. The persisted opening above is retained.
  All 17 changed tracked files, the five other canonical RPI artifacts and this
  record were examined. No subagent, second Review, implementation correction,
  commit, push, other worktree or private dataset was used.
* Review authority: only this record was edited. Independent source probes used
  fictional objects and SQLite `:memory:` without filesystem writes. Previously
  executed regression, browser, actual SQL Server, image and static results are
  attributed to the parent/changes evidence, not represented as rerun here.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | Domain and persistence; complete commitment and separate remedy | Reconciled | resident_decisions.py implements complete fields, scoped rights, versioned actions, explicit legacy confirmation and current-writer replay; existing response/quality/order/finance records remain separate. |
| P01-T02 | Existing journey and scoped resident response handling | Reconciled | server.py distinguishes committed acknowledgement failures; panels.js adds scoped native forms and independent clocks; app.js removes incomplete handoff creation inputs. |
| P02-T01 | Dependent regression, owned SQL, browser, configured checks and image | Reconciled | Recorded executed coverage corresponds to source/tests and the parent-supplied actual results. Review independently checked core behavior in memory, JS syntax, diff hygiene, test limits and KB prefix. |
| P02-T02 | Guides, existing resident synthesis, additive KB route/log | Reconciled | Component contracts, resident synthesis and index describe the bounded behavior and unperformed acceptance honestly. The exact upstream log byte prefix was independently verified. |
| Follow-Up Items | Broader lease/scope/age-band governance and human/coordinator acceptance excluded | Partial routing, not missing implementation | Exclusion is justified, but the broader governance entry lacks an explicit actionable handoff owner/next step; RV-001 routes it separately. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01, PC-001 | src/core/src/zava_forward/core/resident_decisions.py:603-650; store.py:368-370 | Full commitment fields/history; legacy bootstrap without fictional original ownership/time | Version zero explicitly confirms old records; original raw commitment snapshot survives; legacy remedy original opened_at remains null and response remains unchanged | Source read; independent in-memory confirmation probe; recorded JSON/SQLite/MSSQL legacy regression | Meets bounded confirmation contract |
| P01-T01, PC-002 | resident_decisions.py:49-102,123-215,498-601,652-670; sqlstore.py:540-619 | Current named actor/assignee checks, captured ownership and actual transaction-time validation | Canonical actor lookup includes email/code/name/role/OID; exact resident-view role gate; detached current-case replay follows BEGIN IMMEDIATE and precedes writes; rowversion retained | Source trace and independent real in-memory SQL transaction with registry-only owner change refused and case unchanged; recorded concurrent-writer and registry-change tests | No writer-time identity/state bypass identified in assessed actions |
| P01-T01, PC-003 | resident_decisions.py:153-215; sqlstore.py:593-636,638-665 | Rollback, prior-audit preservation and truthful committed acknowledgement | Pre-COMMIT recovery calls canonical discard with prior pending prefix; discard quarantines before reload; resident persisted marker follows COMMIT before synchronization; committed recovery uses empty pending | Recorded actual audit insert/recovery-read/post-COMMIT tests inspected; no SQL Server rerun in Review | Compatible with retained stock/hazard/procurement hooks and no-audit-replay boundary |
| P01-T01, PC-004 | resident_decisions.py:528-601,652-670; workflows.py:180-207; finance.py:303-306 | Independent response/remedy clocks and retained existing delivery/quality/finance clocks | Response actions do not mutate remedy; remedy actions do not mutate response; handoff preserves resident_update; finance adds only payment-note provenance/history | Independent in-memory close/reopen/remedy-cycle probe; mixed-state test at test_resident_decisions.py:903-1010 carries distinct records through real unrelated actions/restart | Exact issue criteria supported; broader PRD acceptance not inferred |
| P01-T02 | src/api/src/zava_forward/api/server.py:876-895; web/panels.js:123-238; web/app.js:694-711 | Explicit HTTP committed result, manual existing-panel controls and no incomplete handoff input | Scoped forms keep draft/error, disable ordinary retry on committed/transport-uncertain result, label response versus remedy and show Unknown legacy provenance | Source read; fresh guideline retrieval/review; JS parses; recorded actual authenticated HTTP/Chromium evidence | No material changed-surface correctness defect identified |
| P01-T02, P02-T02 | src/core/src/zava_forward/core/projection.py:140-150; src/core/README.md; src/api/README.md; docs/reference/research/ux/customer-journeys/residents.md; docs/reference/README.md; docs/reference/log.md | Restrict new references, document compatibility and preserve durable evidence | New resident records and complete nested handoff snapshots stripped outside resident-view roles; contractor allowlist unchanged; no sending/authority/whole-PRD claim | Source/diff review; independent prefix hash and no-removal/test-count inspection | Bounded record/projection/documentation changes are reconciled |

Paths abbreviated to basenames in the table refer to the already named
src/core/src/zava_forward/core directory unless an API, test or documentation
path is given. Test references are under src/core/tests.

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01-T01, P02-T01 | finance.py adds payment_status_owner, payment_status_at and retained note history | Mixed-clock oracle exposed missing payment-note provenance; existing exact owner/date criterion, no new user decision | Details and changes describe the same three additive assignments; no disposition/payment/permission redesign in diff | Compatible PC-004 implementation refinement; no material replanning required | Justified in-scope amendment |
| P01-T02 | Existing actForm uses flatMap; adds input names/autocomplete | Actual browser exposed nested array rendering; no user policy decision | Diff is a bounded helper repair; scoped new forms likewise flatten label/control pairs; plan/details/changes explain it | Compatible existing-screen correction, not a framework/form-system replacement | Justified compatibility fix; collateral existing form rendering considered |
| P01-T01, P02-T01 | Canonical actor helper imported lazily | Recorded cold MSSQL import cycle; no new identity implementation | resident_decisions._actor delegates to change_provenance._actor rather than copying its policy; details/changes record the cause | Approved identity intent preserved; no new critique required | Justified dependency-order correction |
| P01-T02 | Existing resident response forms use the scoped error contract too | Response actions can also commit before acknowledgement failure | serviceForm delegates only resident actions to residentForm; finance/grant/technical remain on their prior path | Direct PC-003 completion, not a global error architecture | Reconciled |
| P01-T02, P02-T02 | Redact complete resident-update snapshots nested in handoff changes | A full commitment now carries more reference/history data than the old owner/due pair | projection.py, details, changes and guides state the same restricted-view behavior | Existing privacy/projection boundary preserved; no wider audit or authority expansion | Justified compatibility refinement |

## Critique and Material Revision Assessment

* PC-001: disposition verified against explicit update_record/remedy_confirm
  contracts, legacy Unknown projection, raw old snapshot retention, version-zero
  rules and test_resident_decisions.py:814-873. Independent source probes also
  confirmed Closed response and unknown original remedy time remain unchanged.
* PC-002: disposition verified against the four exact existing resident-view
  roles, existing two-manager exception, identity-bound owner rights, filtered
  selectors and writer-time subject validation. Tests cover ineligible
  assignments/non-owner refusal/manager reassignment and registry changes.
* PC-003: disposition verified across COMMIT marker, ResidentCommittedError,
  explicit resident HTTP `outcome: "committed"`, subsequent detail/check failure,
  and scoped UI retry prevention. test_resident_api.py:191-234 inspects actual
  HTTP outcome, durable version and successful-audit count after both faults.
* PC-004: disposition verified against the mixed-state test, separate field
  oracle and unrelated-domain source. It tests independent request remedies,
  Defect/Charge query requests, quality defect/handover, work-order completion,
  financial note, return/reopen and restarted stores. Response/remedy-only
  reopening is covered separately. No existing test method was removed.
* Original critique remains Revise with its original four findings; this
  Review does not rewrite that historical verdict. Current plan dispositions
  resolve its compatible planning gaps.
* Dependent-work pause assessment: research, critique and final amendment order
  are recorded by the parent and the synchronized artifacts. Review did not
  independently observe the earlier execution chronology. No contradictory
  source/artifact evidence requiring a renewed planning pause was found.
* Justification assessment: listed refinements preserve exact issue scope;
  none supplies legal policy, actual delegation, paid execution, sending,
  a portal or a new architecture.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Full PRD lease evidence/Legal-reviewed positions, scope-change approval re-review, Housing/Complaints age bands | These extend beyond the user's three exact issue criteria; no thresholds or Legal authority may be invented | Existing plan/changes do not assign an explicit actionable handoff. Planning parent should identify or establish distinct backlog ownership/next action, without activating it in P01/P02 | Open, non-blocking residual; RV-001 |
| Direct human, screen-reader/WCAG and operational acceptance | Local fictional engineering evidence is not competent human or resident acceptance | Parent/coordinator retains acceptance gating and should arrange the appropriate human assessment before making those claims | Correctly unperformed and excluded, not a missing issue88 code task |
| Independent final-head acceptance/shared-file sequencing and later publication/cleanup | Original Review is not the coordinator gate; #91/#102 integration and held #92 remain outside source comparison | Existing parent/coordinator continuation; #81 remains hierarchy only and issue-level dependencies remain NONE | Explicitly retained gate; no Pass/merge/closure claim here |

Unresolved follow-ups remain distinct work. They are not added to active P01/P02
completion or treated as defects merely because the wider PRD still contains them.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Broader governance follow-up is excluded but not actionably owned

* Related scope: plan Follow-Up Items; P02-T02 evidence/handoff boundary.
* Evidence: .copilot-tracking/plans/2026-10-17/resident-update-remedy-controls-88-plan.md:192-195
  records only exclusion and no full acceptance claim.
  .copilot-tracking/changes/2026-10-17/resident-update-remedy-controls-88-changes.md:143-146
  mirrors the exclusion but names no distinct owner or next action.
  src/api/src/zava_forward/api/web/panels.js:207 correctly keeps remedy age bands
  Unknown; this is supporting evidence of residual governance, not a UI defect.
  The source PRD AC-063 and BRD FR-047/AC-089 still contain the broader controls.
* Concrete check: inspect those two Follow-Up Items entries. Neither identifies
  a receiving backlog item, an accountable follow-up owner, or an action to
  obtain that ownership for lease/scope/age-band governance. The distinct
  coordinator final-head gate does not itself own that governance work.
* Impact: the bounded code may be delivered correctly while the wider governance
  obligations remain an unowned exclusion and are later mistaken for completed
  PRD acceptance. This does not invalidate the three implemented issue criteria.
* Destination: distinct non-blocking follow-up, not rpi-implement and not an
  active issue88 plan expansion.
* Smallest useful next action: planning parent identifies an existing separately
  owned backlog route, or records the next action to assign one, for the broader
  lease/scope/age-band controls. Preserve Unknown states and the no-full-acceptance
  statement; do not fabricate thresholds, authority or completed ownership.

## Defects

* No actionable implementation defect was established by the full source/diff
  comparison and bounded independent probes. This is not a claim that all future
  integrations, untested failures or broader PRD behavior are defect-free.
* RV-001 is a non-blocking residual handoff gap, not a runtime defect.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
| --- | --- | --- | --- |
| RV-001 | Distinct follow-up ownership/next action | Planning parent identifies receiving governance backlog ownership or records the action to obtain it | Correctly excluded broader work needs an actionable route, not extra issue88 implementation |

Later correction or routing does not require another full Review, and does not
authorize replacing this original record's outcome.

## Residual Work

* RV-001: explicit separate ownership/next action for the broader lease, scope
  re-review and age-band governance follow-up remains unresolved at this
  comparison. No thresholds or legal/operational authority are supplied here.
* Human/screen-reader/WCAG assessment, full PRD acceptance and independent
  final-head integration acceptance remain unperformed external gates.
* Parent publication and owned-resource cleanup are later lifecycle work, not
  claimed completed by this read-only review.

## Blockers and Remaining Work

* Review blockers: none.
* Remaining active P01/P02 implementation: none demonstrated by this Review.
* Remaining review finding: RV-001, non-blocking distinct follow-up routing.
* No rpi-implement/rpi-plan/rpi-research invocation is required by an established
  implementation defect, invalid active-plan assumption or material source gap.
  Parent remains responsible for separate integration/acceptance decisions.

## Validation Evidence

| Command or evidence | Scope | Status | Summary |
| --- | --- | --- | --- |
| `git diff 1a05dfb8a4c4d9992d72a57228ce15123e9bcf2c -- ...` plus canonical artifact reads | Full own tracked diff and new RPI artifacts | Passed, Review-executed comparison | 17 changed tracked files; complete source/test/doc patch considered; excluded quality.py/assistants.py/progress.py unchanged |
| `.venv/bin/python -B` inline source probes with fictional Memory mixin and SQLite `:memory:` | Independent closure/remedy reopen, commitment retention, legacy confirmation and writer registry refusal | Passed, Review-executed | Closed response retained Open remedy; response reopen left remedy untouched; Resolved/Closed/Open remedy cycle preserved original time; commitment unchanged; legacy confirmation kept original time/response owner unknown; registry-only owner OID change refused during BEGIN IMMEDIATE with unchanged case |
| `.venv/bin/python -B` AST/base-prefix inspection | Test ownership lock and append-only KB evidence | Passed, Review-executed | 12 added core test methods, three added API methods, zero removed methods; below 18/5 maxima. Exact base log prefix SHA256 f35003c314bd9eb31bb4bb00ee1ccb2cc93ba0b35d72610e89f428872c8f80a1 independently verified |
| `node --check src/api/src/zava_forward/api/web/panels.js` and `node --check src/api/src/zava_forward/api/web/app.js`; `git diff --check` | Changed JS syntax/diff hygiene | Passed, Review-executed | Both JS files parse; no whitespace error |
| Fresh web-design-guidelines source retrieval and changed-surface read | panels.js/app.js changed forms/handoff surface | Passed for material changed-surface issues, Review-executed | Complete current source retrieved on 2026-10-17; native labels/controls, input names, live feedback, keyboard submission, Intl status dates, no new motion and scoped retry behavior checked; owner Fluent/plain-language/ASCII rules take precedence |
| Failing-first tests on original source | Missing full commitment/remedy behavior | Failed as expected, parent-executed | Changes and supplied execution evidence identify original unknown action/missing remedy failures; not rerun or relabelled as successful baseline behavior |
| Final directly dependent installed-src unittest selection | JSON/SQLite/HTTP, resident/handoff/workflow and retained stock/hazard/procurement/quality/finance/grant/sqlstore/recovery/change-provenance domains | Passed, parent-executed; five opt-in skips | 378 tests, 127.807 seconds; not rerun in Review |
| Final focused selection with `ZF_RESIDENT_BROWSER=1` | Resident/handoff/HTTP plus real local Chromium | Passed, parent-executed; one MSSQL opt-in skip | 81 tests, 22.760 seconds; recorded off-origin blocking, keyboard create/reassign, independent close/reopen, widths 320/390/1280 and reduced motion; not a fresh Review browser run |
| Eleven selected `MssqlResidentControls` tests, `ZF_RESIDENT_MSSQL=1` | Actual task-owned SQL Server 2022 loopback container and per-test UUID databases | Passed, parent-executed | 11 tests, no skips, 72.049 seconds, including registry-only changes, concurrent writers, real audit/recovery faults and committed/no-replay behavior. Review did not read connection secrets or access the container |
| Full configured core/API Ruff check, Ruff format check and mypy | Changed components with existing configuration/exemptions | Passed, parent-executed | Recorded 113/54 typed source files and no issues; no Review rerun/install |
| Existing `src/check-container.py api zf-issue88-api:local` | Final src-context image/non-root/hardening/plain health/negative probes | Passed, parent-executed | Image sha256:485706b0361ccef3f6057faaed5f4ec7aeb1c3fdfd3c485a4eb854650b5c87b9; not rebuilt or contacted in Review |
| Initial actual browser/SQL attempts | Cold import/render/login discovery | Failed then corrected, parent-executed | Retained failures have corresponding lazy import, flatMap and fixture login-wait corrections; final source reflects the recorded repair |
| Azure/shared SQL, broader inherited opt-in SQL and private/live datasets | Outside authorized local fictional boundary | Not run | Review did not enable opt-ins, contact other stores or read private data; recorded selected loopback MSSQL coverage is not expanded into Azure/full-suite parity |
| Human/screen-reader/WCAG, full PRD and coordinator final-head acceptance | Broader acceptance gates | Not run | Explicitly unperformed; no conformance, authority, message delivery or owner closure inferred |

Changed-web guideline projection:

```text
## src/api/src/zava_forward/api/web/panels.js
pass - no material changed-surface guideline defect established; engineering
review only, not whole-app accessibility or human acceptance.

## src/api/src/zava_forward/api/web/app.js
pass - changed handoff form preserves native recorded-change controls and
removes incomplete commitment creation; unrelated surfaces not audited.
```

## Outcome

* Outcome: Residual work.
* Outcome rationale: the bounded implementation is supported by actual source,
  appropriately attributed executed evidence and independent non-mutating probes.
  No material implementation defect was established. The full Review nevertheless
  leaves RV-001 open because the explicitly excluded broader governance work has
  no actionable owner/next step in its canonical follow-up entries.
* This is the original Review outcome, not a coordinator Pass, issue closure,
  merge decision, legal determination, whole-PRD acceptance or WCAG claim.
  The exact original record must remain distinguishable from any later
  parent-authorized correction or final-head assessment.

## Closeout Routing Record

| Finding class | Destination | Owner or next action |
| --- | --- | --- |
| Implementation defect | None established | No rpi-implement handoff justified by this comparison |
| Decision gap or invalid active-plan assumption | None established | No active issue88 replanning required |
| Material evidence gap | None preventing bounded review | Do not claim unperformed wider acceptance |
| Non-blocking residual work | Distinct governance follow-up, RV-001 | Planning parent identifies receiving ownership/backlog route or records the action to obtain it |

* Execution status: Complete.
* Outcome: Residual work.
* Validation coverage: full own diff/artifact/source comparison; independent
  in-memory behavioral/writer probes, JS parsing, test-limit/prefix/diff checks;
  parent-executed wider regressions/browser/actual SQL/static/image evidence
  separately attributed above.
* Blockers: none to this completed Review; RV-001 remains a non-blocking handoff.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-17/resident-update-remedy-controls-88-research.md](.copilot-tracking/research/2026-10-17/resident-update-remedy-controls-88-research.md) | Research scope, sources and bounded readiness; unchanged |
| [.copilot-tracking/plans/2026-10-17/resident-update-remedy-controls-88-plan.md](.copilot-tracking/plans/2026-10-17/resident-update-remedy-controls-88-plan.md) | Completed plan, PC dispositions and unresolved follow-up route; unchanged |
| [.copilot-tracking/details/2026-10-17/resident-update-remedy-controls-88-phase-details.md](.copilot-tracking/details/2026-10-17/resident-update-remedy-controls-88-phase-details.md) | Reconciled phase contracts/refinements; unchanged |
| [.copilot-tracking/reviews/plans/2026-10-17/resident-update-remedy-controls-88-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-17/resident-update-remedy-controls-88-plan-critique.md) | Original Revise finding set retained; unchanged |
| [.copilot-tracking/changes/2026-10-17/resident-update-remedy-controls-88-changes.md](.copilot-tracking/changes/2026-10-17/resident-update-remedy-controls-88-changes.md) | Parent-executed validation, refinements, exclusions and publication boundary; unchanged |
| [.copilot-tracking/reviews/logs/2026-10-17/resident-update-remedy-controls-88-review.md](.copilot-tracking/reviews/logs/2026-10-17/resident-update-remedy-controls-88-review.md) | The one completed original full-task Review, with opening retained and RV-001 residual route |

## Next Steps

Return this single Review to the active parent. Parent should route RV-001 to
distinct follow-up ownership/next action, preserving its exclusion from active
issue88 scope. No second Review or implementation expansion is requested.
Independent coordinator final-head acceptance and the owner's publication/
merge decisions remain separate. This reviewer stops here without changing
source, other evidence, state, resources or remote systems.
