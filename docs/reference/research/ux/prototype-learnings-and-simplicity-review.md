---
title: Prototype Learnings and Simplicity Review
description: Historical prototype simplicity review and dated PR58 real-platform and decision-model learning
author: AMA programme
ms.date: 2026-10-11
ms.topic: reference
---

## Purpose and evidence boundary

Open pull requests #19 (Python prototype), #24 (Node proof of concept) and #27 (architecture and runbook documents) are kept unmerged to preserve what the prototypes taught the project. This page records those learnings and the result of a simplicity critique run on 2026-10-08 by the UX designer, the Design Thinking coach and six company-role agents (Neighbourhood Housing Officer, Retrofit Programme Manager, Resident Engagement, Data and Performance, Building Safety, Asset Executive).

Evidence labels: observed means seen in the PR content; hypothesis means a role or coach view; unknown means no evidence. Role views are research instruments, not company facts. No usability study with real staff has been done, so every ease-of-use claim here is untested. All prototype data is synthetic.

## What the prototypes proved

### Continuing MVP Learning (2026-10-11)

[#58](https://github.com/jmservera/ama/pull/58) at
`5136f192d583a5bf53adeeec4b0f21369b005c9d` records real Azure SQL/Blob,
Decision 1 source-bound EPC selection and cited GPT-4.1-mini generation
on the original 60,000 generated stock rows/980 programme cases. These
reported results were inspected, not rerun here. The wrong provider host
caused an earlier auth failure; its correction demonstrates integration
feasibility, not calibrated quality or benefit.

The [current model learning](../../../ideas/typesafe-system-one-agent-fit.md#observed-feasibility-and-parallel-value-experiment-2026-10-11)
and PRD experiment intake separate four-arm comparative evidence from
successful inference. Binary support does not establish three-class F1;
missing human labels/effort means Not evaluated/Inconclusive. Later source
tests are not automatically deployed evidence; no full user-acceptance claim.

The owner now requires real AI/SQL/Azure in every accepted application
exercise build, including delivered prototypes and iterations. Historical
static/fake-door tests remain useful UX experiments, not accepted delivery.
AI remains optional for the individual user's task and unavailable-model
manual recovery, not optional in the whole deployed application.
Clear structured fields should use rules unless semantic selection proves
additional value. Preserve source/human-review labels, unknowns, explicit
errors and consent/financial/safety authority; do not fake a rationale from
a closed scorer or hide failed assistance. Independent app/platform work
need not wait for the parallel experiment; adoption/value claims do.

### Historical Prototype Findings (2026-10-08)

| Learning | Source | Status |
| --- | --- | --- |
| Deterministic gate, hold and threshold logic works without AI (0.03 ms workflow-only latency against a 12.5 s median and 17.7 s p95 for the live agent step) | PR #19 | Observed |
| The AI step adds readable handoff drafting, not better blocker detection. Reviewer effort saved is unmeasured | PR #19 | Hypothesis, effort unknown |
| Machine validation of agent output caught an unsupported finding (live eval 5/6, then 6/6 after prompt v2 with no loosened validator) | PR #19 | Observed |
| Bounded read-only tools, a call budget, and a run record committed before inference keep an agent from acting. Failure is recorded, never replayed silently | PR #19 | Observed |
| Import with preview then commit, source never modified, row lineage kept. Only a 3-row demo workbook was tested | PR #19 | Observed, real files unknown |
| A defect (RV-001, re-acceptance after handover) sat outside test coverage. The plan critique found gates were not executable contracts and stale approvals could survive a material change. Fixes: action-to-role matrix, predicate table, "unknown never passes", return, invalidate and re-accept | PR #24 | Observed |
| Local p95 about 61 ms for case-list reads, container restart preserved state, 40 tests and 5 simulator fixtures passed. No model was called and nothing proves load behaviour | PR #24, #27 | Observed |
| SQL must be the source of truth for case state. Container Apps local storage is ephemeral, so an SQLite app must not run multi-replica and cannot move to Azure unchanged | PR #24, #27 | Observed |
| Foundry standard agent setup documentation contradicts itself on state resources, and project capability settings cannot be edited after creation | PR #27 | Observed, correct values unknown |
| Large tracking artifacts (plan, details, changes, research, critique, review, state) were costly to review | PR #24 | Observed |
| Owner feedback (PR #26): liked style, logo, fonts and colours; red appears where nothing is an error; role changes did not visibly change the UI; unclear whether a case is ready, who takes it and what the agent does with the data; wants a full-screen case with address, phone and working data | PR #26, PR #24 | Observed, owner-reported |

Reconciliation with the main-branch ADR 0001: PR #27 treats Cosmos DB as non-authoritative agent state, which is a scope difference from the ADR (SQL only); its queue and model choices are unreconciled; its statement that no Azure resources exist predates the deployed `uksouth` stack. Do not merge the PRs; treat them as evidence.

## Where the prototypes are too complex

All eight critics converged on the same five problems.

* Too much on one screen. The Python prototype combines an actor picker, four perspective buttons, a metric strip, a searchable list, a detail panel, a six-card agent map (five agents unimplemented) and an import panel; the Node PoC adds nine workflows, an 11-role simulator and eight lifecycle stages. Observed. Nobody can name the first action.
* Internal vocabulary. Gate, hold, stale review, provenance, tool trace, episode, "Control room", GATE_BLOCKED. Observed vocabulary; hypothesis that staff read it as bureaucracy or a fault.
* A long path to value. Pick a perspective, find a case, open it, run the agent for 12 to 18 seconds, read the trace, accept. "Accept" only acknowledges a draft and is easy to read as a safety decision or consent. Observed.
* Rejections that look like errors, plus red where nothing is wrong. Excel users expect to overwrite cells (hypothesis).
* A brittle import. An exact nine-column sheet named `cases`, and one bad header fails the file. Observed, so the first task for a data owner would likely fail.

## Consensus simplification

These are proposals, each from at least five of the eight critics.

* Open on one list, "My cases today", with the role taken from sign-in. Remove the perspective picker and role simulator from user views. A perspective switch is not authorisation.
* One full-screen case card: contact details, resident preferences and adjustments, flags, last contact, next appointment, next owner. One plain status line: "Ready", "Waiting on [named person]: [reason]" or "Stopped until [named person] confirms".
* Plain words in place of internal terms: gate becomes "check before next step", hold becomes "waiting on" or "stopped until", quarantine becomes "rows to fix", Accept becomes "Use this draft". Add a copy audit for the core flow.
* Requesting AI per record is optional, on demand or background, and never required to see a case. The subsequent-build rule still requires real AI in the deployed app. Show deterministic status instantly; distinguish "AI suggestion, not approved" from human-reviewed drafts and controlled approvals. Hide unbuilt agents.
* A forgiving import: drop any workbook, auto-map columns and sheet names, import good rows, show "rows to fix" with a plain reason, and offer an Excel-shaped download of those rows. The source file stays untouched.
* Neutral colours for waiting; red only for real hazards or errors. Never colour alone.
* Blocked steps give a reason, an owner and a next action, with a button to ask the owner.
* Export to Excel or CSV on every list from day one, so staff never feel locked in (TR-001).

## What must not be simplified away

Agreed by every critic: server-side gates and "unknown never passes", human approval and the authority matrix (no self-approval), re-acceptance after a material change, hazard and safeguarding clocks with a named owner and an out-of-hours route that does not rely on Teams, resident consent recorded as the resident's own choice and never inferred, accessibility and safe-contact adjustments shown at the point of contact, per-case history and audit, minimum-necessary fields enforced by the server, and the source workbook never modified. A decision or hazard recorded only in Excel stays invalid. Simplify the wording, not the control. Do not state any Awaab's Law figure without current official guidance or legal review.

## Angle-specific changes

| Angle | Proposed simplest change |
| --- | --- |
| UX designer | A table-like Today list with one primary button per row and inline edits of safe fields; trace and provenance behind "How was this worked out?" |
| Design Thinking coach | Test the job first: shadow users, a wizard-of-oz plain "next action" summary for one pilot team, concierge import of three real workbooks, a fake-door "Ask AI" button |
| Housing officer | One "Log a call" box (reached, no answer, no access, refused, hazard) in under 30 seconds, name, phone and address first |
| Programme manager | A prioritised queue grouped "needs you, waiting on others, stuck", a missing-evidence checklist and "return with reason" |
| Resident engagement | A "Resident says" panel at the top of the case; a separate resident decision field; AI drafts internal summaries only and never sends or decides |
| Data and performance | Replace dual write in the parallel run with a read-only Excel mirror from day one; aggregate-only adoption signals; agree the audit-use statement with staff first |
| Building safety | A "Hazards: due soon, overdue, no owner" list with a visible clock and one confirm button; bring the offline hazard list (TR-007) forward before any real hazard data |
| Asset executive | Four drillable numbers (waiting, blocked, overdue, AI time saved); keep the AI only if it saves reviewer minutes without an undetected critical error |

## Proposed ease measures

Thresholds are proposals for the owners to set and to test with real, consenting staff on anonymised or constructed workbooks.

* At least 80 percent of 5 to 8 Excel users per role find their case and state the next step and owner in under 5 minutes, unaided.
* At least 80 percent correctly say what "Use this draft" means and who decides; none confuse it with consent or safety approval.
* A data owner reaches an import preview with row dispositions in 10 minutes or less on a real workbook, in at least 4 of 5 trials, with at least 90 percent of rows auto-mapped, sampled and audited so a systematic error cannot hide.
* An officer logs a call outcome unaided in 3 minutes or less and re-enters fewer than 2 fields per call.
* Zero hold bypasses in the acceptance suite; at least 90 percent say a denial told them what to do next.
* Training of 30 minutes or less; double-entry rate falls to zero during the parallel run.
* Core flows answer in under 2 seconds. AI drafts run in the background or return in under about 5 seconds, or leave the default path.
* A System Usability Scale score of at least 70.
* Adoption metrics are aggregate only. No ranking of individuals.

## Contradictions and tensions to resolve

* Inline editing and bulk actions (UX designer, coach) versus the dual-write hazard in ADR 0001. Edit only fields the workbench owns and never write back to Excel.
* Hiding gates versus showing safety clocks. Hide the vocabulary, keep the clock and the owner visible.
* The coach asks for audit earlier (TR-006) to avoid a surveillance feeling; the Data lead asks for the audit-use statement before any adoption metric. Both support moving TR-006 earlier.
* Run the AI automatically (UX designer) versus on demand (others). Resolve by testing with users; the default here is on demand or background.

## Unknowns

Real workbook structures, owners, macros and vulnerability content; whether Excel users want AI and for which task; staff comprehension of the vocabulary; hazard triage rules and clock definitions; out-of-hours cover; device mix; whether staff and HR have been consulted on logging; tenant and licences (OQ-012); DPIA status; reviewer effort saved by AI drafts; and any resident research.

## Next steps

* Observe 5 to 8 real Excel users before further build, then run the concierge import and the plain "next action" summary test.
* Prototype the single-list, full-screen-case flow with plain wording and compare it against the current screens.
* Reflect the agreed requirements in the PRD (see Simplicity and adoption requirements) and revisit ADR 0001 stage 1 to remove dual write.
