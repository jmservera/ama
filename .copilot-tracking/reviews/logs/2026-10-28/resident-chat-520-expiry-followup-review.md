<!-- markdownlint-disable-file -->
---
title: Resident chat 520 proposal expiry follow-up review
ms.date: 2026-10-28
---

# Review: resident-chat-520-expiry-followup

## Scope and Evidence

Task ID: 520-expiry-followup. Review date: 2026-10-28.
Assessed boundary: narrow backend proposal-expiry repair against 72a78101,
regression, README and dated RPI evidence; not the entire #520 feature.
Canonical plan/details/research/critique/changes use the same date and slug.
Validation logs are in the external evidence root identified by changes.

## Opening Review State

* Interpreted review goal: independently compare the completed fix and actual evidence
  with the approved two-deadline transaction contract.
* Review scope: P01 implementation and readiness for P02 publication.
* Evidence readiness: P01 reconciled; exact final regression red/green, 92 unit/API
  tests without skips, API Ruff100/format100 and mypy94 passed on hashed source bytes.
* Acceptance basis: plan criteria, owner's bounded publication authorization,
  one original independent critique Complete / Pass and no findings.
* First comparison boundary: expiry selection/final instant and authorization rollback,
  isolated boundary regression, preserved slot-start/idempotency and validation logs.
* Active read-only boundaries: source and compared artifacts read-only; only this
  review record may be completed by the independent assessor.
* Initial blockers: complete gate unavailable because az is barred; no browser change,
  no browser run required; human/AT/hosted and final publication actions unclaimed.

## Execution Status

* Review execution: Complete. This is the task's one independent post-implementation
  assessment, performed under the active parent's rpi-review.
* Implementation execution: P01/P01-T01/P01-T02 complete; overall plan Partial because
  P02 publication and thread resolution deliberately follow this Review.
* Inspected the complete diff against 72a7810189db0994111b0a2d9b3341bd002f2f17
  for src/api/src/zava_forward/api/resident_demo/agenda.py,
  src/api/tests/test_resident_chat_agenda.py and src/api/README.md.
* Read the matching dated research, plan, phase details, original critique and changes;
  transaction, HTTP caller, existing agenda/API test and package configuration context;
  source local-gate guidance and relevant required project context.
* Validation was assessed from task-owned external logs, not rerun. Independently
  recomputed SHA256 for all three changed source/test/document files. No heavy command,
  installation, browser, gate, az, fetch, commit, push or GitHub mutation was performed.
  Only this review record was edited.

## Plan-to-Change Reconciliation

| Current plan scope | Changes-record summary | Reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01-T01 | Deterministic red, minimal query/final-check fix, one regression method, README | Reconciled | Exact final test has negative-control and green evidence; no public signature, schema or browser change. |
| P01-T02 | Final locked regression, six suites, API static checks and hashes | Reconciled | Original failures remain; final logs match assessed source hashes. |
| P02 | Review readiness, publication pending | Reconciled | This Review completes assessment only; commit, upstream reconciliation, normal push and named-thread verification remain with parent. |
| Follow-Up Items | Full gate and inherited human/AT/hosted acceptance | Reconciled | Explicitly outside active fix acceptance; not converted into implementation tasks or success claims. |

## Completed Work Assessment

| Marker | Files and evidence | Assessment |
| --- | --- | --- |
| P01-T01 | agenda.py:179-202; complete transaction and prior-booking context | Selecting o.expires makes the deadline available without a second query. One clock sample after successful authorised() supplies both <= checks. The insert and final check remain inside _transaction(), whose exception path rolls back. Authorization denial still precedes final deadline handling. |
| P01-T01 | test_resident_chat_agenda.py:115-143 | Exactly one new test method, no removals. Each subtest owns a separate constructed SQLite agenda. The callback changes the Mock clock from expiry minus one second to expiry minus one microsecond, exact expiry or plus one microsecond. The next-day slot isolates proposal expiry. Changed return_value and exactly two clock calls establish authorization-driven advancement and a fresh final sample. |
| P01-T01 | test_resident_chat_agenda.py:130-141 | Just-before commits and survives reopening; retry at exact expiry returns the committed booking. Exact/after raise the expected conflict, reopening shows no booking, and another owner finds the same earliest slot and successfully books it. This verifies durable rollback and slot reuse, not merely an exception. |
| P01-T01 | Existing agenda tests and unchanged HTTP caller | Static datetime callers, initial exact expiry/start rejection, final exact slot-start crossing, owner isolation, competition, cancellation and authorization rollback remain covered. Prior-booking idempotency and authorization ordering are unchanged. app.py passes app.now as a callable and maps AgendaConflict to HTTP 409. |
| P01-T01 | src/api/README.md:142-148 | Narrow clarification accurately describes both post-authorization deadlines and rollback; existing idempotent retry language remains. |
| P01-T02 | Final task-owned validation logs and SHA256 | Scoped tests/static checks passed on matching source bytes. No receipt, whole-feature acceptance or broader API-suite pass is inferred. |

## Implementation-Time Plan and Detail Update Assessment

| Affected scope | Change and trigger | Reconciliation and assessment |
| --- | --- | --- |
| P01-T01 | First red run let an incorrectly committed exact-expiry booking contaminate the following case; isolated agendas remove contamination. | Details and changes preserve the original failure and explain independent per-boundary fixtures. The isolated red and final negative control both fail specifically with AgendaConflict not raised at exact/after expiry. No scope or test-method-count expansion. |
| P01-T02 | Initial Ruff reported four B023 loop-closure findings. | Callback default bindings and a standard-library Mock resolve lint inside the approved regression method. Final test retains the same clock, boundary and persistence intent. Changes retain initial failed lint and distinguish checks not reached in that command from final successful checks. |
| P01 completion/P02 readiness | Final regression, six selectors and package static checks completed. | Plan checkboxes, details, changes and handoff agree: P01 complete, P02 pending. The changes narrative's earlier queued-validation statement is historical and followed by a clearly dated final result, not a current blocker. |

## Critique and Material Revision Assessment

* Original independent critique: Complete / Pass, Critical 0, High 0, Medium 0,
  Low 0; no unresolved PC findings or omitted dispositions.
* Production changes follow the critiqued two-deadline transaction design exactly.
  Fixture isolation and callback binding are directly coupled implementation/test
  refinements, not significant or divergent decisions needing renewed planning.
* No material revision, new autonomy, dependency, public contract or acceptance
  change was discovered. No dependent-work pause violation is evidenced.
* Owner's explicit narrow tested-fix publication direction is preserved. It does not
  authorize a fabricated gate receipt, broader approval, force push, merge or deployment.

## Plan Follow-Up Assessment

| Follow-up | Why outside immediate scope | Owner / next action | Assessment and route |
| --- | --- | --- | --- |
| Complete local gate | Requires az, expressly barred for this task; no full-gate attempt is authorized. | Owner/validation owner: later authorization and prerequisites before running the complete gate. | Open, RV-001; separate future validation, not an implementation defect. |
| Human/AT and hosted acceptance | Local backend unit/static evidence does not establish human approval, assistive-technology acceptance or hosted exact-head results. | Parent preserves open status; human/AT reviewers and hosted checks supply their own evidence. | Open, RV-002; distinct inherited acceptance work, not new active fix scope. |

## Findings

Complete substantive finding set: no implementation defects, decision gaps or material
research gaps within P01. The following entries route non-blocking residuals once.
Severity describes the consequence of an unsupported acceptance claim, not a source defect.

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Complete local-gate evidence remains unavailable

* Related scope: plan Follow-Up Items; P02 publication evidence boundary.
* Evidence: plan and phase details explicitly bar az/full-gate attempts; changes
  Validation Record reports complete local gate Blocked/unattempted. External final
  logs contain only focused tests and API static checks, not a gate receipt.
* Impact: scoped success cannot establish complete local-gate or whole-issue acceptance.
  This limits assurance; it does not contradict the caller-authorized narrow fix.
* Destination: distinct follow-up, complete-gate validation owner.
* Smallest useful next action: retain the unavailable status in publication/reply;
  seek later authorization and prerequisites for the actual gate. Do not attempt
  the gate, fabricate a receipt or substitute cloud validation in this task.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Inherited human/AT and hosted acceptance remain separate

* Related scope: plan Follow-Up Items and inherited #520/#525 acceptance.
* Evidence: plan, details and changes leave human/AT/hosted approval unclaimed.
  The changed-file boundary contains no browser-facing code; final evidence consists
  of Python unit/API suites and static checks.
* Impact: this backend assessment establishes neither accessibility conformance,
  human approval nor future hosted exact-head success.
* Destination: distinct inherited acceptance follow-up, human/AT reviewers and
  hosted CI owners; parent maintains the open status.
* Smallest useful next action: observe hosted checks after the normal push and leave
  human/AT acceptance to its named reviewers. No browser run is required for this fix.

## Defects

None found in the complete supplied source diff and necessary unchanged context.
No finding is routed to rpi-implement, rpi-plan or rpi-research.

## Routed Findings

| Finding | Destination | Owner / next action | Reason |
| --- | --- | --- | --- |
| RV-001 | Distinct full-gate validation follow-up | Owner/validation owner, future authorized prerequisites | Unavailable broader validation, not a defect or current gate success. |
| RV-002 | Distinct inherited acceptance follow-up | Human/AT reviewers and hosted CI owners; parent tracks | Independent acceptance remains unclaimed by local checks. |

Later implementation of any routed work does not require another Review of this task.

## Residual Work

* RV-001 and RV-002 remain outside P01 acceptance.
* Remaining active P02 actions belong to the parent: persist this original outcome,
  commit implementation and dated evidence with required privacy-safe identity/trailer,
  refresh/reconcile upstream under the explicit authorization, normally push and
  verify the tested fix is present, then reply to and GraphQL-resolve only
  PRRT_kwDOUU8JX86xTMcu on PR #525 and verify the result.
* Do not mark P02 complete before those actions. Any upstream/source change must
  receive appropriate refreshed validation; current hashes bind only inspected bytes.
  No merge, deployment, force push or PR closing keyword is authorized.

## Blockers and Remaining Work

* No blocker to credible scoped Review or parent continuation within the explicit
  narrow publication authorization.
* Complete gate is unavailable because its az prerequisite is barred; no attempt
  or receipt is claimed. This remains a blocker to claiming full-gate acceptance.
* Publication, reply/resolution and future hosted results were not assessed as
  completed; no live remote/thread state was refreshed by this assessor.

## Validation Evidence

External evidence root supplied by the parent:
/home/azureuser/.copilot/session-state/0632f8cf-cc46-45e2-acb7-aafa7811e9dd/files/520-expiry-validation.
Only named task-owned logs were inspected, not its environment or private inputs.

| Check / recorded command | Status | Evidence and scope |
| --- | --- | --- |
| Final exact regression with original 72a78101 book patched in process | Expected failure | final-negative-control.log: one method, two failures, exact/after expiry each AgendaConflict not raised, no errors; log explicitly records no source change. Caller and changes identify the in-process original-method control. |
| Final fixed regression | Passed | final-regression-green.log: one test, OK; source shows all three boundary subtests. |
| Six planned resident selectors | Passed | final-resident-suites.log: 92 tests in 43.557s, OK, no skips. Selectors are test_resident_chat_agenda, test_resident_chat_api, test_resident_demo_api, test_resident_assistant_api, test_resident_aoai and test_resident_assistant_provider. |
| ruff check --line-length 100 . from src/api | Passed | final-ruff-check.log: All checks passed; existing package configuration/exemptions unchanged. |
| ruff format --check --line-length 100 . from src/api | Passed | final-ruff-format.log: 50 files already formatted; final-format-applied.log retained. |
| mypy from src/api | Passed | final-mypy.log: no issues in 94 source files; configured package-wide strict scope and existing overrides unchanged. |
| Independent sha256sum of all three changed files | Passed | Exact matches with final-source-sha256.txt and changes; hashes below. |
| Retained initial red/isolated red and initial Ruff | Failed, expected or corrected | regression-red.log preserves contamination; regression-red-isolated.log isolates both missing-conflict failures; ruff-check.log preserves four B023 findings. Earlier green/suite logs remain distinct from final evidence. |
| Heavy admission | Recorded, not independently reacquired | final-admission.log: acquired 21:21:55Z, completed 21:22:44Z; changes document bounded admission. Review ran no heavy work. |
| Browser | Not applicable | No changed browser-facing code; no browser test required or claimed. |
| Complete local gate | Unavailable / unattempted | Barred az prerequisite; no receipt or broader integration success. |
| Human/AT and hosted exact-head checks | Unavailable in this assessment | Separate acceptance, not inferred from scoped logs. |
| P02 commit/push/thread resolution | Pending | Parent action after this Review, not a failed check. |

Source binding verified independently:

* src/api/src/zava_forward/api/resident_demo/agenda.py:
  1006b6b04b05ad0593e176695b42905ce4cd72cf1bd6da26cc66eb7b72c6d096.
* src/api/tests/test_resident_chat_agenda.py:
  4cae256edaf50b5e2add6a12020a167f617b86521aa9e3b08327fd2d47a2105e.
* src/api/README.md:
  7d0c31071fb8f3daa6cd50b2fcaa22be9b0ad89e705abb463ebc909c999b4553.

The logs are scoped execution evidence, not a signed/full-gate receipt. The assessor
did not rerun tests or independently refresh environment/tool identity. Existing
RuntimeError diagnostics accompany an OK suite result, not hidden test failures.

## Outcome

* Outcome: Residual work.
* P01 scoped correctness assessment: Conformant. The narrow repair and regression
  satisfy the two-deadline, authorization, persistence and compatibility requirements;
  no substantive source defect was identified.
* Overall rationale: Review is complete, but P02 publication remains deliberately
  pending and full-gate/human/AT/hosted assurance remains outside this evidence.
  No whole-issue acceptance or publication completion is asserted.

## Closeout Routing Record

| Finding class | Destination | Owner / next action |
| --- | --- | --- |
| Implementation defect | None | No rpi-implement handoff. |
| Decision gap or invalid assumption | None | No rpi-plan handoff; bounded intent preserved. |
| Material research gap | None | No rpi-research handoff. |
| Non-blocking residual validation | RV-001 distinct follow-up | Future authorized complete-gate owner. |
| Non-blocking inherited acceptance | RV-002 distinct follow-up | Human/AT reviewers and hosted CI owners. |
| Remaining active P02 | Active parent continuation | Commit/normal push and verified named-thread reply/resolution, preserving limits. |

* Review execution: Complete.
* Outcome: Residual work; P01 Conformant.
* Severity summary: Critical 0; High 0; Medium 1 residual; Low 1 residual; defects 0.
* Validation: exact final negative/positive control, 92 tests without skips,
  Ruff100/format100 and mypy94 logs plus independently matched SHA256.
* Blockers: complete-gate acceptance unavailable; no blocker to the bounded parent's
  explicitly authorized continuation. No second Review or lifecycle is requested.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-28/resident-chat-520-expiry-followup-research.md](.copilot-tracking/research/2026-10-28/resident-chat-520-expiry-followup-research.md) | Research and caller boundary. |
| [.copilot-tracking/plans/2026-10-28/resident-chat-520-expiry-followup-plan.md](.copilot-tracking/plans/2026-10-28/resident-chat-520-expiry-followup-plan.md) | P01 complete; P02 publication pending. |
| [.copilot-tracking/details/2026-10-28/resident-chat-520-expiry-followup-phase-details.md](.copilot-tracking/details/2026-10-28/resident-chat-520-expiry-followup-phase-details.md) | Implementation and validation contract. |
| [.copilot-tracking/reviews/plans/2026-10-28/resident-chat-520-expiry-followup-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-28/resident-chat-520-expiry-followup-plan-critique.md) | Original Complete / Pass critique. |
| [.copilot-tracking/changes/2026-10-28/resident-chat-520-expiry-followup-changes.md](.copilot-tracking/changes/2026-10-28/resident-chat-520-expiry-followup-changes.md) | Actual execution, retained failures and final validation. |
| [.copilot-tracking/reviews/logs/2026-10-28/resident-chat-520-expiry-followup-review.md](.copilot-tracking/reviews/logs/2026-10-28/resident-chat-520-expiry-followup-review.md) | This single independent assessment. |
| [src/api/src/zava_forward/api/resident_demo/agenda.py](src/api/src/zava_forward/api/resident_demo/agenda.py) | Assessed transaction and two-deadline fix. |
| [src/api/tests/test_resident_chat_agenda.py](src/api/tests/test_resident_chat_agenda.py) | Boundary regression and preserved behavior tests. |
| [src/api/README.md](src/api/README.md) | Updated callback contract. |

## Next Steps

Return this one assessment to the active parent for the remaining authorized P02
publication and named-thread actions. Preserve RV-001/RV-002 as distinct follow-ups,
the original critique/Review outcomes and all adverse logs. No user response or
second Review is required; this assessor stops without publication or GitHub mutation.
