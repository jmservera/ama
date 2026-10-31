<!-- markdownlint-disable-file -->
# Review: demo-transport-blob-360

## Scope and Evidence

* Task ID: demo-transport-blob-360
* Review date: 2026-10-22
* Review scope: full task
* Assessed boundary: offline private-Blob transport implementation, Bicep, tests and documentation against owner decisions DN1 to DN5 and critique PC-001 to PC-011; no live behaviour
* Plan: .copilot-tracking/plans/2026-10-22/demo-transport-blob-360-plan.md
* Phase details: .copilot-tracking/details/2026-10-22/demo-transport-blob-360-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-22/demo-transport-blob-360-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-22/demo-transport-blob-360-changes.md
* Other evidence considered: research artifact; infra test run (378 OK), ruff, mypy, bicep builds

## Opening Review State

* Interpreted review goal: confirm the implementation honours DN1 to DN5 without overclaiming
* Review scope: full task
* Evidence readiness: all artifacts and validation present
* Acceptance basis: plan requirements and critique dispositions
* First comparison boundary: code and Bicep versus plan tasks
* Active read-only boundaries: this record only
* Initial blockers: none

## Execution Status

* Execution status: Complete
* Review execution evidence: 2026-10-22, direct read of the changed files, tests and docs; no subagent lenses needed

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01 | Controller, worker, codec | Reconciled | Plan checkbox markers were not ticked in the plan file (RV-003) |
| P02 | Bicep, tests, allowlists | Reconciled | Custom write-only role is a narrowing divergence |
| P03 | Documentation, KB log | Reconciled | None |
| P04 | Review and gate | Partial at review time | Gate and PR update follow this record |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
| --- | --- | --- | --- | --- | --- |
| P01 | infra/scripts/staff_blob.py, staff_azure.py, staff-azure-worker.py | Replace tag relay with private Blob | Retired-token grep test passes | Offline fake tests | reconciled |
| P02 | infra/modules/storage.bicep, staff-initializer-rbac.bicep, tests | Container, lifecycle, scoped role | bicep build OK; 378 tests OK | Offline | reconciled |
| P03 | infra/README.md, evidence pack, KB | Design, prerequisites, NOT RUN | Diff reviewed | Link anchors checked by name | reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
| --- | --- | --- | --- | --- | --- |
| Role design | Write-only custom data role instead of built-in contributor | PC-006 least privilege | Matrix, Bicep and tests aligned | Covered by critique PC-006 | reconciled |
| Phase details | Not rewritten for critique changes | Critique dispositions live in the plan | Plan disposition table is authoritative | Not needed | gap noted as RV-003 |

## Critique and Material Revision Assessment

* Latest critique dispositions: PC-001 to PC-011 applied; PC-011 is evidence-only
* Material revisions: none after critique
* Dependent-work pause assessment: no early resumption
* Justification assessment: supported

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
| --- | --- | --- | --- |
| Live private-route and Entra read test | Needs cost release and tenant prerequisites | Coordinator release | distinct follow-up |
| Historical failure root cause | Production follow-up per DN3 | Owner | distinct follow-up |
| Signed attestation | DN5 deferred | Owner | distinct follow-up |

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Real result size and position count unmeasured

* Related scope: P01
* Evidence: infra/scripts/staff_blob.py bounds (64 pages of 48 KiB); infra/README.md live prerequisite 6
* Impact: an over-bound result fails closed; it cannot be shown to fit until measured
* Destination: follow_up
* Smallest useful next action: measure on the first released live check run

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Offline fake clients cannot prove private routing, MI write or role scope

* Related scope: P02
* Evidence: infra/tests/test_staff_azure.py FakeContainer
* Impact: the Blob data-action names and the write-only role (write plus add) are unproven against real Azure; a missing data action would fail closed at the worker with a sanitised error
* Destination: follow_up
* Smallest useful next action: verify in the controlled live run, adjust the role if Put Blob needs another action

<!-- rpi:review id=RV-003 -->
### RV-003 [Low]: Phase details and plan markers not refreshed after critique

* Related scope: P01 to P04
* Evidence: plan checklist markers unchecked; details predate critique
* Impact: documentation drift only; the plan disposition table and changes record are authoritative
* Destination: follow_up
* Smallest useful next action: tidy in a later plan pass; original evidence is intentionally preserved

<!-- rpi:review id=RV-004 -->
### RV-004 [Low]: Account-wide principals can overwrite or delete result blobs

* Related scope: P02
* Evidence: infra/README.md residual risk paragraph
* Impact: authenticated encryption makes tampering a refusal, not a false success; availability can still be affected
* Destination: follow_up
* Smallest useful next action: consider immutability or a per-run container in production design

## Defects

* None blocking.

## Routed Findings

* RV-001, RV-002, RV-004: distinct follow-up (live validation after coordinator release)
* RV-003: rpi-plan tidy, optional

## Outcome

* Outcome: Residual work
* Rationale: offline contract conformant; live behaviour, deployment and acceptance are NOT RUN and #360 c, d, e remain unproved
