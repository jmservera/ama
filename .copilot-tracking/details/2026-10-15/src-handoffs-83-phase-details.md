---
title: Issue 83 phase details
ms.date: 2026-10-15
---

Task #83 / src-handoffs-83. Research C1-C9 grounds the plan.

<!-- P01 -->
## P01 Core workflow

P01-T01: extend WorkflowMixin, preserving existing lock/_case/save/audit.
Return/reopen metadata uses authenticated actor identity, existing case owner,
source and next action. All new confirmations, including direct core calls,
require these inputs; old persisted history renders unknown values. Record
version and complete prior/current stage in each immutable history entry.
Do not accept an owner override: return/reopen cannot transfer accountability.
Record the current owner as receiving owner; another destination requires the
same handoff offer/accept path. Test malicious owner input cannot bypass this.

Add Received, Escalated and Completed, keep Offered/Declined for compatibility
and expose canonical Sent/Rejected status. Acceptance may follow sent/receipt/
escalation, only receiver; completion follows acceptance, only current owner.
Escalation records named manager, reason and previous state, never acceptance.
Keep sender chase ownership until acceptance and preserve transition history.
Optional due date has strict timezone-aware validation. No timer invents policy.
Urgency, next action and resident-update owner/date are separate metadata.
Missing values are null/unknown; preserve pending resident-update fields through
rejection and subsequent offers, without automatic messaging.

| Action | Source states | Actor |
| --- | --- | --- |
| Offer | absent, Declined, Withdrawn, Completed | current owner or manager |
| Receive | Offered | named recipient |
| Accept | Offered, Received, Escalated | named recipient |
| Decline | Offered, Received, Escalated | named recipient, reason required |
| Withdraw | Offered, Received, Escalated | sender or manager |
| Escalate | Offered, Received | sender or manager; named manager target and reason |
| Complete | Accepted | current owner (the acceptor); completion note required |

Receipt after escalation is not allowed; acceptance/rejection resolves it.
Replay and all unlisted state/actor edges fail without state/audit/history change.

P01-T02: legacy hand_over delegates to offer_handoff, no direct reassignment.
Prevent overwriting accepted unfinished handoffs. Reject replay and wrong
actors; preserve closed-case and safety behavior.

<!-- P02 -->
## P02 API, UI and evidence

P02-T01: wire receipt/escalation/completion plus metadata on existing case paths.
Show source, authority, receiving owner and next step; distinguish accountability,
destination, proposed/confirmed receiver, chase, due date and unknown values.
Queue includes sender/recipient and managers. Redact new free text with existing
need-role rules; contractor gets no workflow data or mutation authority.

P02-T02: two new semantic/integration test modules maximum; table-driven states,
negative permissions, restart persistence, exact audit and ownership invariants.
Existing role inventory covers new actions. Update API/core READMEs and knowledge
index/log, no regulatory or operational compliance claims.

<!-- P03 -->
## P03 Validation and delivery

P03-T01: pip editable local environment. All five src suites, component ruff,
format and mypy, changed JS syntax, migration regressions, synthetic loopback app
run and Docker attempt. SQL Server/live model/Azure unavailable are explicitly
not run, never replaced with mock acceptance.

P03-T02: fresh one-pass review compares plan, diff and evidence; route open
findings to follow-up, do not repeat review. In-scope correctness/permission
defects block passing acceptance and require draft/blocked publication; accepted
owner/live exclusions do not. Keep a finding-to-disposition ledger. Commit all RPI artifacts with trailer
and privacy-safe author/committer email, push assigned branch, create main PR
with Refs #83 and full validation/unchecked criteria. Never merge.
