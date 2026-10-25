---
title: Optional resident portal and communication agent — PRD draft amendment
date: 2026-10-23
status: unsigned-draft
prd_id: PRD-2026-AMA48-001
base_version: 0.18.0
candidate_version: 0.19.0
base_commit: 140d8f494482c78e84d15f3d46b9223d3c487af0
---

## Purpose and authority boundary

This package elaborates the owner's optional resident portal and communication
agent request into a **draft**, actionable acceptance contract. It is not
requirements signoff, a Finalize exit, an accepted application, permission to
send messages or a real resident deployment. The next step is the parent's ADR
commission, not implementation or a repository PR.

The target remains the existing
`docs/prds/zava-forward-retrofit-programme-demonstrator.md`.
`amendment.patch` is the only proposed repository change in this package. It
amends v0.18.0 to candidate v0.19.0 without replacing the PRD, changing its
logical ID, deleting history or marking tests completed. The file's inherited
`in-review` governance status is not new approval. Aggregate SMART status
becomes deferred for new proposed GOAL-005; the original four goals and
historical acceptance remain intact.

Upstream is `../brd/draft-prd-handoff.json`, artifact type
`DRAFT_BRD_AMENDMENT_HANDOFF`, not `BRD_TO_PRD_HANDOFF_V1`.
BRD v0.19.0 is the pinned base, v0.20.0 its **unsigned candidate**:
Define BLOCKED, Govern NOT_EVALUATED, no approvers, approved date or waivers.
100% structural link coverage is not tested correctness or governance approval.
The base/candidate/patch hashes are verified independently in `validation.json`.

Only this output directory contains new files. The dirty detached checkout,
index, refs, worktrees, GitHub and gate #97/PID 3440015 are untouched.
No fetch, checkout, git write, application test suite, cloud/tenant operation,
private resident input or paid call was used. Source reads use the pinned
commit, not the checkout. No company-role, PRD-authoring or ADR agent is needed
to invent answers to actual owner/design decisions.

## Product proposition and rationale

**Sell a testable capacity hypothesis, not a claim of savings:** a resident can
answer “what happens next?”, retrieve their approved document, supply a
requested file, respond to an appointment and reach a person without repeated
chasing. Staff work from the same case events and owned exception queues,
instead of retyping portal activity or reconciling competing case histories.
The agent adds a grounded explanation and handoff, not decision authority.
Compare the portal/workflow alone against agent assistance before attributing
benefit to AI.

The controlled quantitative source remains
`../brd/amendment.md#optional-resident-service--illustrative-capacity-case-2026-10-23`
and its candidate BRD section after integration. The PRD provides a short
linked pitch/formula summary, not a second uncontrolled scenario table.
The base illustration yields **14.74 net staff-hours/week**, after all stated
review/reconciliation/support/new-intake onboarding, and **48 one-off initial
onboarding hours**. Low **-1.594** and high **94.333** are joint sensitivities.
None is measured, a forecast, money ROI, a headcount saving or a cash claim.
Inputs are authorised author judgement, not public statistics. 60,000 homes
never implies a resident/account count. Default per-message human review
requires recomputing review effort; modeled policy eligibility is not approval.

## What the amendment adds

| Capability | Proposed observable result | Safety boundary |
| --- | --- | --- |
| Optional mobile resident projection | Own timeline/status/as-of, next action and approved documents | Case/field/task authorisation on every server request; no staff-directory membership assumption |
| Requested uploads | Traceable receipt, quarantine/scan and pending-review state | No model/reader access before validation; clean is not accepted/published |
| Appointment response | Accept/propose/postpone event and named update owner | No autonomous confirmed booking, inferred consent, no-access or unsafe pause |
| Shared event history | Portal plus assisted-channel event in the same case | Provenance, replay reconciliation, unknown connector status and no forced re-entry |
| Staff exceptions | Owned document, contact, ambiguity, overdue and handoff queues | Receipt/delivery is not accepted handoff; chase owner persists |
| Resident-answer task | Disclosed, cited current-case/process answer or abstention | New registry entry, current access, injection resistance, independent urgent/help route |
| Identity and authority | Fictional sign-in, scoped entitlement/recovery/revocation | Managed identity candidate; no homegrown passwords, shared-address rights or consent inference |
| Routine communication policy proposal | Explicit testable deny-by-default dispatch gate | No activated exception; sensitive/consequential/uncertain traffic always human-reviewed |
| Honest value comparison | Same-task effort, task success and adverse/non-digital results | No uptake-only success or double counting |

Phone, email, letters, visits and assisted service remain. A resident without
a safe device/account must not lose access, priority, complaint routes or human
review. Persistent resident/representative preference memory is excluded;
minimal service/handoff records do not become staff chat memory.

## Surgical changes to the existing PRD

The patch preserves all headings/history and all original FR/AC/NFR/CON/GOAL/DD
definition bytes. Only original decision-question OQ-023 is updated to
distinguish proposed resident scope from unresolved operational permission.
New sections, personas, rows and current boundary notes reconcile:

* The executive scope and “residents not users” statement prospectively;
  historical exercise approvals remain dated evidence.
* The dated staff Entra topology with a separate resident identity boundary.
* The staff-chat resident deferral row with the separate proposed resident
  increment, without expanding PRD FR-055 to FR-059 or staff ADR 0004.
* The resident-login exclusion with fictional sign-in only; real accounts,
  live sending and integrations stay excluded.
* Goal/requirement/criterion matrices, new OQs, release/journey contracts,
  linked capacity assumptions and a current candidate boundary note.
* Inherited stale candidate heading/counts are identified as historical
  snapshots, not rewritten as current acceptance evidence.

The new `Resident upstream trace` table is the author-maintained PRD mapping.
`id-traceability.md` gives allocation, stable document namespaces and the
amendment acceptance registry. No inherited BRD issues are repaired here.

## Explicit provisional exercise assumptions

These are **author proposals to make the slice executable**, not unanswered
questions hidden in prose or owner-approved production defaults:

* Six task scripts under GOAL-005; each new AC has separate Not run status.
  A separately reviewed resident milestone does not restart the earlier T0,
  commit a date or expand eleven staff profiles to thirteen.
* Retained generated 60,000-home/980-case lineage with labelled fictional
  identity/household/representative fixtures; unverified links stay unknown.
* PDF/JPEG/PNG, 10 MiB/file, one file/request; quarantine until checks pass.
  A 60-second pending scan offers help, never fail-open.
* One model call, no delegated-agent/tool loop, 15-second timeout, bounded
  input/output and the existing finite budget gate; no paid call is authorised.
* A simulated ordinary handoff exercises one-working-day acknowledgement
  and two-working-day next-update aging. Urgent human/help routes are
  immediate and independent; these are not actual service promises.
* Three fictional resident and two staff sessions for 30 minutes; proposed
  p95 at most two seconds for permitted case/status/receipt API actions,
  excluding sign-in/scan/model waits reported separately. No capacity claim.
* Session, recovery, rate/abuse and real retention choices require ADR and
  OQ-030/031; missing safe configuration fails closed. Basic demo privacy,
  upload safety, authorisation and accessibility cannot be postponed as
  “production hardening”.

The owner may review these assumptions without pretending to be the company's
DPO, service owner or security authority. For delivery story refinement, the
capabilities are Valuable/Testable candidates, but independence, size and
estimation are not established; slice them along the six jobs and their
shared entitlement/event prerequisites during native RPI.

## Significant upstream contradiction for parent

**BRD FR-044 still says every output shall preserve human review, while its
new AC-084 allows a policy approver/automated disposition instead.** This is
an upstream body-versus-criterion contradiction, not merely an unresolved
choice of identity provider. The changed RULE-018/022/025 and new RULE-028
otherwise describe an explicit routine-policy exception.

Do not silently choose the permissive interpretation. PRD FR-070/AC-129 and
OQ-029 require parent reconciliation plus OD-53/release before any activation.
Per-message human review remains the default, including in-portal AI replies.
This PRD package does not change BRD bytes or broaden staff or regulatory
assistant send authority. The contradiction blocks exception activation,
not delivery of the bounded unsigned draft or the ADR comparison.

## Residual decisions and quality dispositions

| Upstream decision/finding | Treatment in this draft | What remains blocked |
| --- | --- | --- |
| OD-52 | OQ-028; proposed Programme/Housing/Engagement/Digital ownership and manual fallback | Live service without named staffed/source/channel owners |
| OD-53 | OQ-029, FR-070; complete routine-policy activation predicate and simulated outbox | Every per-message-review exception until actual evidence/authority and wording reconciliation |
| OD-54 | OQ-030, FR-069, NFR-019; resident identity/files/privacy/rights boundary to ADR | Real accounts/data, unsupported recovery or retention assumptions |
| OD-55 | OQ-031, FR-071, NFR-021; explicit hypothetical inputs and proposed test limits | Achieved benefit, production SLO/capacity or uptake claims |
| OD-41/42/47 | Operational discovery/representative/communication authority retained | Real resident use; staff ADR acceptance is not closure |
| OD-18/25/35/36/49/51 | Existing measurement/service/incident/privacy/evaluation/economic gates retained | Applicable activation, budgets or operational assertions |
| BRD req-qual-001/002 | Inherited SMART/feasibility/signoff blockers retained | Define/Govern and PRD formal approval |
| BRD req-qual-003 | Review says performance efficiency absent, but base NFR-012 exists | Resident sizing still open; do not repeat the erroneous absence claim |
| BRD req-qual-004 | Carry feasibility gaps to ADR/service owners | No operational readiness assertion |
| BRD reviewer artifact limits | Duplicate `top_findings`, missing persisted findings reference, inspection-only counts and post-review edits recorded | No strict validated signed-handoff claim |

`quality-review.md` records PRD draft quality evidence and its limitations.
Static validation demonstrates an exact patch, preserved IDs and links, not
implementation, feasibility, human user validation or lifecycle acceptance.
Finalize is not attempted; no final approval is declared.

## Delivery and downstream handoff

1. Parent re-reads the integration base and registries in its isolated native
   RPI process. If changed, rebase/reallocate only new IDs and regenerate
   exact hashes/quality evidence; do not apply with fuzz or renumber history.
2. Integrate BRD, PRD and prospective dependent-document reconciliations
   together. Resolve the upstream contradiction explicitly.
3. Commission the ADR from `adr-handoff.md` after this draft. No ADR agent
   was launched here and no ADR decision is represented as accepted.
4. Obtain independent exact integrated-byte requirements review and owner
   exercise acceptance. Service, identity, privacy and live authority gates
   remain separate; the current work does not authorise implementation.
5. Staff landing/auth remains independently deliverable unless a verified
   shared dependency is recorded with evidence and owner.
