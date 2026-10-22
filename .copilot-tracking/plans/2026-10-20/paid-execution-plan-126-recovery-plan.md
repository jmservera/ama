<!-- markdownlint-disable-file -->
# RPI Plan: Finite costed execution plan for #126 (recovery run)

## Task Metadata

* Task ID: 126-paid-plan-recovery
* Task slug: paid-execution-plan-126-recovery
* Planning status: ready
* Plan date: 2026-10-20
* Phase details: .copilot-tracking/details/2026-10-20/paid-execution-plan-126-recovery-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-20/paid-execution-plan-126-recovery-plan-critique.md
* Recovery disclosure: written after the coordinator intervention of 2026-10-20T21:25Z. The earlier files `paid-execution-plan-126-{research,plan,phase-details,plan-critique}.md` were hand-authored before any rpi-* skill was invoked. They are unverified pre-RPI input, preserved unchanged, and are not evidence that a phase ran. This plan was produced by invoking the rpi-plan skill after the recovery research.

## Executive Summary

The plan adds one subsection to the existing Case Study 48 addendum (plus the knowledge-base index row and an append-only log entry) that gives the owner a finite, costed, approval-ready set of options for a usable but unfinished Azure synthetic demo. Nothing is executed or approved by this work.

The central finding is that the spend picture, not model tokens, decides feasibility. RG `ama` accrued 189.94 USD for 1-20 Oct (estimated, 20 Oct partial). At the observed 30.245 USD/day the month ends at about 535 USD, above the 500 USD total cap, before any new work. Actual-model tokens for the proposed finite allowance cost under 5 USD at list price. The plan therefore puts an idle-burn disposition and subscription-scope spend disclosure in front of every tranche, and defines a first deployment tranche (T1) that adds no new resources.

### User Decisions and Requirements Highlights

* USD 500 is the TOTAL monthly cap including accrued charges, so thresholds use projected month end.
* Authorization expires 2026-10-25T16:02Z; nothing may start after a hard do-not-start time before it.
* Output is documentation for owner approval; no issue acceptance or operational release is inferred.

### What You May Not Know

* This identity cannot see subscription-scope charges, so 500 USD compliance cannot be shown here. Unknown spend blocks execution.
* Front Door Premium (about 10.64 USD/day) and SQL (about 10.66 USD/day) are about 70 percent of the daily burn. The SQL saving from pausing is a 0 to about 10.66 USD/day range, not a promise.
* The demo API returns 403 by design (deny-all). That is not sign-in evidence.

### Unresolved Decisions or Blockers

* Owner supplies subscription-scope charges, credits and billing latency; chooses an idle-burn option; approves tranches. Private bootstrap, tenant registration, roster and executor remain open.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements).

## User Decisions and Requirements

* Run full RPI for #126 as a finite costed execution plan, documentation only, for separate owner approval; not paid execution (user brief; issue comments 6290697705, 6295338398, 6301554087).
* Priority is the shortest safe route to a usable unfinished Azure synthetic demo, not more generic governance.
* Scope includes #108/#222/#223 actual-model evaluation, #117/#122/#358/#360 Azure validation and #137/#360 sizing as eligible planned scopes; manifests and human gates are not approved.
* Read-only evidence only; never reveal credentials, tenant IDs or private bindings; no resources, jobs, inference, deployment changes or permissions; never change subscription; unknown spend or prices block execution; do not assume 500 USD is available.
* Reuse the existing benefits/budget synthesis; edit only the addendum, index and log; do not edit infra/README.md, form schema packs, map docs or the cohort pack.
* Include finite calls/tokens/model versions, per-resource counts/SKU/region/lifetime, local-first versus Azure-only need, provenance/date/currency, conservative envelope and reserve, monitoring and stop thresholds, expiry 2026-10-25T16:02Z, cleanup and script recreation with synthetic data; preserve identities and RG `ama`; account for all existing liabilities and private blockers; reference a transport design generically; do not retry known capacity failures.
* Provide a bounded first tranche with approval fields, commands or script references, preconditions and expected browser/roles/SQL/AI checks; state what the owner can test now only with real evidence.
* Coordinator intervention: recovery artifacts are distinct and disclose the pre-RPI draft; no push, PR or merge; full local gate and independent assessment remain mandatory.

## Goals

* Give the owner a decision-ready option set that shows headroom, burn, liabilities and the cheapest safe route to a usable demo.
* Keep every figure traceable to dated, currency-labelled evidence with unknowns stated.
* Preserve the human, tenant, privacy and legal approval boundaries.

## Scope and Non-Goals

### In Scope

* One new subsection in docs/case_study_48_addendum.md, an ms.date update, one index row and one append-only log entry.
* Recovery RPI artifacts and state, with the disclosure carried by the recovery artifacts; the pre-RPI draft files stay unchanged.

### Non-Goals

* Any Azure change, deployment, inference, permission or tenant action; any push, PR or merge.
* Edits to infra/README.md, form schema packs, map docs, the cohort pack or a new standalone page.
* Issue acceptance, operational release, or approval of any manifest.

## Functional Requirements

* The subsection states the October accrued figure, partial-day and latency caveats, current daily burn by service, liabilities and projected headroom.
  * Observable acceptance criteria: each number carries date, scope (RG `ama`), currency (USD) and source class; other-scope spend is a bounded month-end forecast U (accrued plus forecast through 31 Oct, excluding `ama`); unbounded U blocks every paid tranche.
* The subsection offers idle-burn options (S0 no change, S1 Front Door retired, S2 S1 plus SQL idled) with the arithmetic and a delay sensitivity.
  * Observable acceptance criteria: S0 is shown blocked; only options meeting the eligibility rule are marked eligible.
* The subsection defines tranches T0 to T4, each with a bill of materials (count/SKU/region/lifetime), finite calls/tokens/model versions, local-first versus Azure-only need, ceiling, thresholds, monitoring, cleanup and recreation.
  * Observable acceptance criteria: T1 has an approval template, commands or script references, preconditions and pass/fail checks for browser, roles, SQL and AI.
* The subsection states what the owner can test now only with real evidence and that redirects or 403 are not sign-in.

## Non-Functional Requirements

* Evidence integrity: no tenant, subscription, resource or principal IDs, secrets or private bindings.
  * Objective threshold or evaluation condition: a pattern scan of changed files finds none.
* Consistency: thresholds are computed from one stated formula.
  * Objective threshold or evaluation condition: every projected month-end value reproduces from the stated inputs.
* Markdown style per repository conventions; relative links resolve.

## Acceptance Criteria

* The addendum subsection, index row and log entry exist and satisfy the functional requirements.
* Hard gates are explicit: unknown subscription spend, missing owner approval, or a start time at or after the do-not-start time blocks every paid tranche.
* No file outside the in-scope list is changed except recovery artifacts.
* Local checks pass and the full gate receipt verifies at the committed head.

## Implementation Context Record

| Context item | Current artifact or record |
|---|---|
| Plan | .copilot-tracking/plans/2026-10-20/paid-execution-plan-126-recovery-plan.md |
| Phase details | .copilot-tracking/details/2026-10-20/paid-execution-plan-126-recovery-phase-details.md |
| Latest critique | .copilot-tracking/reviews/plans/2026-10-20/paid-execution-plan-126-recovery-plan-critique.md with Revise verdict, dispositions recorded |
| Relevant research | .copilot-tracking/research/2026-10-20/paid-execution-plan-126-recovery-research.md |
| Changes-record role | .copilot-tracking/changes/2026-10-20/paid-execution-plan-126-recovery-changes.md is created by implementation |
| Planning execution and readiness | complete; ready for implementation |
| Continuation context | confirmed automatic RPI Agent parent continues now and gates |

## Sources

* .copilot-tracking/research/2026-10-20/paid-execution-plan-126-recovery-research.md: C1-C17, W1, W2, findings F1-F6.
* .copilot-tracking/reviews/2026-10-20/paid-execution-plan-126-plan-critique.md: pre-RPI rubber-duck concerns PC001-PC006, used as unverified input and folded into the design.
* docs/case_study_48_addendum.md: EXA-012 and the cap note, the synthesis to extend.
* infra/README.md (read only): blockers, rollback and retirement, demo staging.
* /tmp/ama-wave-20261020-2113-common.md: wave contract.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Draft the costed-plan subsection

* Intent: add the evidence, options, gates and tranches to the addendum.
* Dependencies: recovery research (done).

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Cost position and options

* Requirement and evidence: accrued, burn, liabilities, S0/S1/S2, formula, thresholds (F1-F3).
* Expected result: a table set with arithmetic reproducible from stated inputs.
* Detail section: P01-T01 in .copilot-tracking/details/2026-10-20/paid-execution-plan-126-recovery-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Tranches T0 to T4 and T1 approval template

* Requirement and evidence: bill of materials, finite calls/tokens, local-first need, commands, preconditions, checks (F4, F5).
* Expected result: bounded tranche tables, approval fields and pass/fail checks.
* Detail section: P01-T02 in .copilot-tracking/details/2026-10-20/paid-execution-plan-126-recovery-phase-details.md

<!-- rpi:task id=P01-T03 -->
#### [x] P01-T03: Owner-testable now, blockers, cleanup and recreation

* Requirement and evidence: real-evidence-only statement, liabilities, blockers, expiry gate, recreation scripts (F5, F6).
* Expected result: explicit gates and cleanup rules without deleting RG `ama` or identities.
* Detail section: P01-T03 in .copilot-tracking/details/2026-10-20/paid-execution-plan-126-recovery-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Index, log, clarification and checks

* Intent: update the knowledge base index and log, and run focused checks.
* Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Index, log and ms.date

* Requirement and evidence: knowledge-base conventions; append-only log.
* Expected result: one index row and one appended log entry; the pre-RPI draft files stay unchanged and the recovery artifacts carry the disclosure.
* Detail section: P02-T01 in .copilot-tracking/details/2026-10-20/paid-execution-plan-126-recovery-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Focused checks

* Requirement and evidence: no IDs or secrets, links resolve, git diff scope, arithmetic reproduces.
* Expected result: recorded check outputs in the changes record.
* Detail section: P02-T02 in .copilot-tracking/details/2026-10-20/paid-execution-plan-126-recovery-phase-details.md

## Dependencies

* Owner-only data (subscription charges, approvals, tenant, roster): needed for any execution, not for this documentation.

## Critique Disposition

| Critique run and finding | Disposition | Plan response or residual risk |
|---|---|---|
| PC-001 U term for unknown other-scope spend | resolved | Added U to E and L; paid tranches blocked while U is unrecorded |
| PC-002 threshold contradiction and reserve | resolved | Split into approval envelope E (<=475) and live projection L (400/450/475); R flagged as an assumption |
| PC-003 S2 50 percent saving | resolved | S2 shown as an illustration, never used for eligibility |
| PC-004 do-not-start inconsistency | resolved | Per-tranche latest start with durations; Sunday noted |
| PC-005 T1 AI check and mutations | resolved | AI check conditional (not available, not pass); mutations and rollbacks listed |
| PC-006 T1 pass/fail evidence | resolved | Positive pass evidence; 3xx/401/403 are not sign-in |
| PC-007 T3 bill of materials | resolved with residual risk | Script paths named, lifetime and retention liability stated; T3 not approvable until commands and unit prices recorded |
| PC-008 append to pre-RPI draft | resolved | Draft files stay unchanged; recovery artifacts carry the disclosure |
| PC-009 T2 failure rule and price basis | resolved | Stop on first capacity or quota error; price basis dated |
| PC-010 S1 delay and rollback cost | resolved | Delay sensitivity and rollback cost note added |

Critique run once (verdict Revise, 0 Critical, 4 High, 3 Medium, 3 Low); all findings were planner-direct and applied in one batch; no second critique.

## Follow-Up Items

* None

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-10-20/paid-execution-plan-126-recovery-changes.md
* Ready phase or task: P01-T01 now
* Remaining provisional question or blocker: none for documentation; owner-only items for execution

## Post-Review Correction Note (2026-10-20)

Independent assessment of candidate 1607d562 found U was defined as accrued-only (High). Corrected in the addendum and phase details: U is a bounded month-end forecast outside `ama`, no double counting, unbounded blocks, no zero assumption, and limits on U replace the U = 0 illustration. PC-001 disposition stands as historical; this note supersedes its wording. The original Review and critique are unchanged.
