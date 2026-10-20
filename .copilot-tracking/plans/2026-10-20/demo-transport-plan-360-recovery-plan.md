<!-- markdownlint-disable-file -->
# RPI Plan: Authenticated roster transport design and tenant checklist (#360), recovery cycle

## Task Metadata

* Task ID: demo-transport-plan-360-recovery
* Task slug: demo-transport-plan-360-recovery
* Planning status: ready (critique dispositions recorded)
* Plan date: 2026-10-20
* Phase details: .copilot-tracking/details/2026-10-20/demo-transport-plan-360-recovery-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-20/demo-transport-plan-360-recovery-plan-critique.md

## Executive Summary

The repository already holds a design-only runbook section proposing a documented, authenticated way to return roster-candidate results from the private worker job: encrypted frames in ARM resource tags (option T1), a stronger binding of the result to the run, execution, image and manifest, and a 13-row tenant/operator checklist. An earlier session wrote it, and all its tracking artifacts, by hand without activating the RPI skills. This recovery cycle treats that draft as unverified, re-verified its evidence in a genuine research pass, and plans the smallest corrections and disclosures so the result can be reviewed honestly.

Nothing is executed: no cloud, tenant, Graph, secret, private-data or billing action, no parser change and no retry.

### User Decisions and Requirements Highlights

* Documentation-only design plus checklist; the owner wants Azure testing soon, but execution needs later approval.
* The prior draft is preserved as unverified; the intervention is disclosed, never backdated.

### What You May Not Know

* AEAD proves possession of the per-run key, not independent worker or image attestation; the design must say so (already stated, will be sharpened).
* The controller already knows the execution name, so binding it in the associated data is cheap.
* Tag values are plain text on several Azure surfaces; whether Activity Log records tag values was not established.
* Which code path the three failed attempts ran is unrecoverable from the repository (DN3).

### Unresolved Decisions or Blockers

* DN1 to DN5 remain reviewer or owner decisions; cost and execution approval is a later implementation precondition. No blockers for the design.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements).

## User Decisions and Requirements

* Design a documented authenticated private worker-to-controller transport; no execution (#360 comment 6290697080, #126 comment 6290697705).
* Preserve the three failed attempts, original roster and adverse evidence. Do not relax the parser, decrypt, retry live jobs, infer completeness, reuse random users or invent staff bindings.
* Select a minimal justified proposal or record decision-needed options, with feasibility evidence and a script-oriented plan; no speculative success claims; provider samples are not protocol guarantees.
* Add an actionable tenant-admin/operator checklist; read-only RG metadata does not grant tenant authority; never delete RG ama or retire Front Door before verified replacement and explicit authorization.
* Keep edits to the infra runbook, cutover evidence, optional architecture record, and shared index/log. Do not edit budget/benefits, cohort, Finance form or map domains.
* Do not depend on the #126 plan result; state cost and execution approval as a later precondition. Whole #360 c/d/e remain unproved.
* Coordinator intervention: genuinely run research, plan with one critique, implement and one review; disclose the premature draft; append dated clarifications instead of rewriting; no push, PR or merge; full local gate and external receipt.

## Goals

* Verify and correct the existing design against the recovery research (C1-C11, W1-W6).
* Disclose the process defect in the permanent artifacts without altering history.
* Leave a frozen, gate-passing local candidate.

## Scope and Non-Goals

### In Scope

* infra/README.md design section (targeted corrections), docs/architecture/cutover-evidence-pack.md entry, docs/reference/README.md and log.md (new append-only entry), new recovery tracking artifacts, dated clarification notes appended to old draft artifacts.

### Non-Goals

* Source changes, tests, cloud or tenant actions, issue criteria ticking, edits to protected domains, rewriting or deleting old artifacts or log entries.

## Functional Requirements

* The runbook states that tag-relay authentication is Entra/RBAC for access plus AEAD key possession, not worker attestation.
  * Observable acceptance criteria: sentence present in the design section; DN5 retained.
* The threat table covers Merge overwrite of an existing tag name and Activity Log exposure uncertainty.
  * Observable acceptance criteria: both rows present with W2/W3 links.
* The binding extension names execution ID and job resource ID explicitly as controller-held.
  * Observable acceptance criteria: present (already) and consistent with research C9.
* A process-disclosure pointer to the recovery artifacts exists in the design section and evidence pack.
  * Observable acceptance criteria: statement that the original draft was authored before skill activation and is superseded by the recovery cycle for verification.

## Non-Functional Requirements

* ASCII only, no em dashes, `*` bullets, existing table style.
  * Objective threshold or evaluation condition: grep for non-ASCII characters in added lines returns none.
* No new unsourced claim: every external fact cites a URL and date.
  * Observable acceptance criteria: link and wording review.

## Acceptance Criteria

* Design section corrections applied and consistent with the recovery research.
* Old artifacts preserved byte-for-byte except an appended dated clarification.
* New log entry appended; earlier entries untouched.
* No edits outside the allowed domains (git diff name list).
* Full local gate passes against fresh origin/main with an external receipt verified.

## Implementation Context Record

| Context item                     | Current artifact or record |
|----------------------------------|----------------------------|
| Plan                             | .copilot-tracking/plans/2026-10-20/demo-transport-plan-360-recovery-plan.md |
| Phase details                    | .copilot-tracking/details/2026-10-20/demo-transport-plan-360-recovery-phase-details.md |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-10-20/demo-transport-plan-360-recovery-plan-critique.md |
| Relevant research                | .copilot-tracking/research/2026-10-20/demo-transport-plan-360-recovery-research.md |
| Changes-record role              | .copilot-tracking/changes/2026-10-20/demo-transport-plan-360-recovery-changes.md is created by implementation |
| Planning execution and readiness | Complete; Ready after critique dispositions |
| Continuation context             | confirmed automatic RPI Agent parent continues to rpi-implement |

## Sources

* .copilot-tracking/research/2026-10-20/demo-transport-plan-360-recovery-research.md: verified evidence C1-C11, W1-W6 and decisions.
* infra/README.md: current design section under "Authenticated Roster Result Transport Design".
* docs/architecture/cutover-evidence-pack.md, docs/reference/README.md, docs/reference/log.md: shared records.
* /tmp/ama-wave-20261020-2113-common.md: wave contract.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [ ] P01: Correct and disclose in the runbook design

* Intent: apply research-driven wording and table corrections plus a process disclosure.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [ ] P01-T01: Sharpen authentication claim and add threat rows

* Requirement and evidence: Q4 findings, C5, C8, W1-W3.
* Expected result: qualified wording, Merge-overwrite and Activity Log rows, execution ID wording.
* Detail section: P01-T01 in .copilot-tracking/details/2026-10-20/demo-transport-plan-360-recovery-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [ ] P01-T02: Add process disclosure to runbook and evidence pack

* Requirement and evidence: coordinator intervention.
* Expected result: dated disclosure paragraph, pointers to recovery artifacts.
* Detail section: P01-T02 in .copilot-tracking/details/2026-10-20/demo-transport-plan-360-recovery-phase-details.md

<!-- rpi:phase id=P02 -->
### [ ] P02: Records and clarifications

* Intent: new append-only log entry, index pointer update, dated clarifications on old draft artifacts.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [ ] P02-T01: Log, index and clarification notes

* Requirement and evidence: knowledge base conventions; intervention rules.
* Expected result: new log entry; appended clarification in old research, plan, details, critique, changes, review, state; old content unchanged.
* Detail section: P02-T01 in .copilot-tracking/details/2026-10-20/demo-transport-plan-360-recovery-phase-details.md

<!-- rpi:phase id=P03 -->
### [ ] P03: Review, freeze and gate

* Intent: one rpi-review, commit, full local gate, receipt verification.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [ ] P03-T01: Commit and run the full gate

* Requirement and evidence: AMA instructions local RPI gate.
* Expected result: new commit (no amend), external receipt verified against fresh origin/main.
* Detail section: P03-T01 in .copilot-tracking/details/2026-10-20/demo-transport-plan-360-recovery-phase-details.md

## Dependencies

* Later implementation (not this task): reviewer decisions DN1-DN5, approved finite cost and execution plan, tenant authority.

## Critique Disposition

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| PC-001 High: runbook says tag records are not a byte stream, but tag frames feed the shared console-line decoder, which skips non-frame values | resolved | P01-T01 corrects the two phrasings (requirements table, "structured tag records") to state the shared decoder and the skip behavior as a gap closed by S2 strict grammar; wording correction of my own unverified claim, evidence C4 |
| PC-002 High: no change budget; wording changes may imply removals | resolved | Change budget: additions only (two threat rows, one disclosure paragraph in runbook and evidence pack, one log entry, appended clarifications), plus exactly the two PC-001/PC-007 corrective phrase replacements; no other removals; authentication qualification already exists in the trust-assumption paragraph, so only a pointer is added |
| PC-003 Medium: test ownership unrecorded | resolved | No tests added or removed (docs only); future owner is S1-S4 in infra/tests/test_staff_azure.py; semantic coverage is the later work, regression is the existing full gate |
| PC-004 Medium: threat-row wording | resolved | Row A: another tag writer overwrites or deletes an owned frame name; worker refuses collisions at write time (C8), but later overwrite is detected only by AEAD and causes refusal (W2). Row B: Activity Log keeps management events 90 days (W3); whether tag values are recorded is unverified, so treat as possible exposure until DN1 review |
| PC-005 Medium: P03 lacks commands and checks | resolved | P03-T01 details now list commit set, fetch, gate and verify commands, diff allowlist/denylist, ASCII and link checks |
| PC-006 Medium: state JSON cannot gain a key without editing a line | resolved | Do not modify the old JSON; write a sidecar note demo-transport-plan-360-state-clarification.md and the new recovery state JSON |
| PC-007 Low: "other prefixes ignored but counted" not in code | resolved | Corrected to "other prefixes not read; a counting check is proposed for S2" |
| PC-008 Medium: "superseded" ambiguous | resolved | Disclosure says: first draft was written without skill activation, its critique and review were not genuine RPI outcomes, its content was re-verified by the recovery cycle, and the independent verification remains pending (human and coordinator gates) |
| PC-009 Low: disposition table pending | resolved | This table |

## Follow-Up Items

* None

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-10-20/demo-transport-plan-360-recovery-changes.md
* Ready phase or task: P01-T01
* Remaining provisional question or blocker: none

## Dated Correction 2026-10-20

Post-assessment correction (bounded, no redesign): the design's cost precondition now names the all-in USD 500 TOTAL October gate with accrued and forecast charges across all scopes and unknown bounded headroom. See the changes record. Critique and Review are not rerun.
