<!-- markdownlint-disable-file -->
# Review: Cut-over evidence pack

## Scope and Evidence

Task: issue-201 / cutover-evidence-201. Date: 2026-10-16.
One review of the prepared evidence pack and supporting source audit/build
changes, not owner acceptance or a healthy-deployment certification.

* Plan: .copilot-tracking/plans/2026-10-16/cutover-evidence-201-plan.md
* Details: .copilot-tracking/details/2026-10-16/cutover-evidence-201-phase-details.md
* Critique: .copilot-tracking/plans/2026-10-16/cutover-evidence-201-critique.md
* Changes: .copilot-tracking/changes/2026-10-16/cutover-evidence-201-changes.md
* Research: .copilot-tracking/research/2026-10-16/cutover-evidence-201-research.md
* Delivery: docs/architecture/cutover-evidence-pack.md and its three evidence
  files, src/acr-cutover.yaml, source audit and external tests.

## Opening Review State

Evidence ready for bounded review. P01/P02 markers are complete as preparation
and execution attempts, not cloud acceptance. P03 publication is pending.
Read-only review; only this review record is written. Direct comparison is
sufficient; no second agent or second Review is used.

## Execution Status

Complete. Compared requirements, phase tasks, seven critique dispositions,
implementation amendment, source diff, test outputs, generated reconciliation,
image digests, actual failed ARM diagnostics, current owner comments and
unchecked sign-off checklist.

## Plan-to-Change Reconciliation

| Scope | Evidence and assessment |
| --- | --- |
| P01-T01 | Five complete suites and final targeted audit suite; all five Ruff/format/mypy; infra86/rename25, Bicep, JS, namespace, data and Chromium checks. Initial failures and corrected invocations retained. SQL skips and no measured coverage comparison disclosed |
| P01-T02 | Incremental ama-only bootstrap attempted and Failed; no app endpoint. Four ACR images built and remote contracts passed. Scoped inventory/IDs retained; no false deployed pass |
| P02-T01 | One stdlib audit module and one external test module; 130 historical row/patterns cover 578 tracked historical names; explicit divergences, no missing destinations; substantive old-context and target-map mutation failures |
| P02-T02 | Pack, machine-readable reports, README/index/log, post-cut-over rename proposal and unchecked owner checklist present |
| P03 | Review executed once; commit/push/PR remain parent publication actions, not review claims |

## Implementation-Time Update Assessment

The added ACR task and golden-only context exception are justified by direct
remote build failures, not speculative refactoring. The existing Dockerfiles
already explicitly COPY that runtime golden; no new package/client authority
or dependency pin was added. BuildKit task succeeds and tests image properties
before push. No Dockerfile changed.

The initial omission of sandbox-pattern rows was corrected before Review;
all 578 historical names are accounted for. Proposed matrix paths are preserved
alongside actual paths. The doc-specific sign-off checker was not implemented:
the parent narrowed it to a real source/reference oracle and direct docs review,
while preserving the requested negative evidence and unchecked owner boundary.
No significant new owner choice or second critique was required.

PC-001 through PC-007 were directly dispositioned in the plan. Scope, outputs,
validation state and observed blockers agree with the changes record. No
deployment prerequisite was bypassed to obtain a health result.

## Evidence Integrity Checks

Mechanical comparison passed for all relative pack file links, zero checked
owner boxes, Failed deployment, empty deployed-app list, 65 retained resource
IDs, four runtime output lines, image digests in prose, all recorded build-input
SHA-256 values and 130 reconciliation rows with no missing destination.
Generated inventory check passed before review-owned additions; parent must
regenerate once after final tracking updates.

The 482-test core complete run predates the final sandbox regression, which
was included in the nine-test targeted pass. The pack does not turn this into
a claimed 483-test full run. Aggregate complete-suite count is 1155/104 skips;
test counts are expressly not measured coverage equivalence.

The retained source tree contains no modifications to mvp/, prototype/,
.env, .vscode or github-issues tracking. No private dataset or secret value
is part of the recorded evidence.

## Findings and Routing

<!-- rpi:review id=RV-001 -->
### RV-001 [High]: Requested deployed proof remains unavailable

* Evidence: docs/architecture/cutover-azure-evidence.json records Failed ARM
  deployment, Microsoft.Devices NotRegistered, SQL firewall/public-interface
  rejection and no deployed app.
* Impact: This task cannot provide healthy src revisions or real deployed
  HTTP/auth/SQL/restart smoke proof; cut-over must not be accepted.
* Destination: distinct follow-up, beginning with authorized platform/network
  prerequisite resolution, then rpi-implement for deployment evidence.
* Next action: authorized subscription operator resolves provider registration;
  owner-approved SQL network/policy path and existing tenant credentials are
  established before application deployment.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Independent owner and comparative-evidence gates remain

* Evidence: pack owner checklist and stale rubric snapshot; 104 local skips
  and no measured before/after line/branch coverage.
* Impact: Count growth, remote builds and document merge cannot establish
  private copy/open/encrypted-backup, coverage parity or owner acceptance.
* Destination: distinct owner evidence review; rpi-research for an actual
  comparable coverage/rubric assessment when prerequisites are available.
* Next action: owner attests privately and records explicit go/no-go in #201.

<!-- rpi:review id=RV-003 -->
### RV-003 [Low]: Partial stack remains billable

* Evidence: 65 resources, new budget-cutover-test and retained unique image tags;
  no current mandatory post-evidence cleanup pattern established.
* Impact: Retained services can accrue charges while deployment is blocked.
* Destination: distinct owner retention/remediation/ID-scoped cleanup choice.
* Next action: inspect inventory; never delete group ama or pre-existing budget.

## Defects

No current-task code or evidence-integrity defect identified in the assessed
boundary. Findings above are unfulfilled requested cloud/human evidence, not
permission to label the full cut-over task accepted.

## Plan Follow-Up Assessment

Owner-only data attestation, owner sign-off, later single-PR workflow rename,
worker transport and service-role denial remain explicit independent work.
No legacy deletion or workflow/protection update is performed here. Owner
#323 direction governs warning-only rulesets; live API returned 403, honestly
disclosed rather than replaced by an enforcement claim.

## Outcome

Execution: Complete. Outcome: **Residual work**. The evidence pack is
reviewable and honest; deployed proof and owner/comparative acceptance remain
unfulfilled. Not a conformant cut-over or sign-off. No second Review planned.
Parent may publish this explicitly incomplete/blocked evidence PR, then route
RV-001 through RV-003 without starting new implementation in this lifecycle.
