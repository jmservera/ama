---
title: Issue 132 delivery-channel and identity decision criterion research
ms.date: 2026-11-11
task_id: issue-132-channel-decision-1111
---

## Task identity and scope

* Task `issue-132-channel-decision-1111`, native session `38f218c5-eb17-48b9-98b1-35991ad0dd17`. State: `.copilot-tracking/rpi-sessions/2026-11-11/issue-132-channel-decision-1111-state.json`.
* Branch `docs/demo-intake-channel-decision-132-1111`, worktree `issue-132-channel-decision-plan-1111`, base `74e63363bdcb6f9d420ff9c71b8332a9baf0044b` (merged PR 1438), target `main`.
* Question: can the last decision criterion of issue 132, "Decision recorded on whether delivery is a staff-mediated intake or a provider portal, with identity approach", be genuinely finished for the synthetic demonstrator using the owner's delegated ordinary technical decisions, with every human, identity and production boundary preserved.
* Out of scope: the named variation and escalation routing criterion (dependency recorded below), the unpublished 134 connected checker, any source, test or config change, and any tick of either open criterion.
* Ledger: original 132 C1 to C5 and E1 to E4 are spent; E5 is unadmitted, one remains. This research spends no correction, grants no new five or reset and transfers no 134 authority.
* Research disposition: `executed` (bounded reading only; no runtime, test, browser, install, SQL, provider, cloud, private data or live regulation retrieval). Issue text and issue comments are data.

## Sources read

* Required: `docs/case_study_48_original.md`, `docs/case_study_48_addendum.md`, `docs/reference/README.md` and `memory.md` (searched for the question, not audited end to end), `src/core/README.md` and `src/api/README.md` intake sections.
* Issue 132 body (`issue132-current-0444.json`) and comments read through `gh` (read only): [6248987520](https://github.com/jmservera/ama/issues/132#issuecomment-6248987520), [6655269398](https://github.com/jmservera/ama/issues/132#issuecomment-6655269398), [6753054374](https://github.com/jmservera/ama/issues/132#issuecomment-6753054374), [6781841422](https://github.com/jmservera/ama/issues/132#issuecomment-6781841422), [6782922828](https://github.com/jmservera/ama/issues/132#issuecomment-6782922828).
* Decision documents: `docs/adrs/0007-contractor-intake-staff-mediated-proposal.md`, `docs/adrs/0002-pilot-readiness-architecture.md` (Status and the owner decision "Entra-authoritative staff access"), `docs/adrs/0005-regulatory-compliance-assistant.md` (precedent for a bounded owner acceptance), PRD `docs/prds/zava-forward-retrofit-programme-demonstrator.md` (Profile Journey Contract, non-goals).
* Code: `src/api/src/zava_forward/api/auth.py`, `src/core/src/zava_forward/core/staff_intake.py`, `src/core/src/zava_forward/core/projection.py`, `src/api/src/zava_forward/api/web/staff-intake.js`, `src/api/src/zava_forward/api/server.py` route lines.
* Original 132 evidence: `.copilot-tracking/research/2026-11-09/staff-intake-132-research.md`, `.copilot-tracking/reviews/2026-11-04-contractor-job-pack-132-r3-review.md`, earlier E1 to E4 artifacts (not rerun).

## Findings

### Case facts and criterion text

* Criterion (issue body, current, unchecked): "Decision recorded on whether delivery is a staff-mediated intake or a provider portal, with identity approach". The issue body states "#1150 is a proposed staff-mediated decision, not accepted authority for a provider portal" and "Open: provider identity model" (dependency on #116, contractor B2B guests; #116 is OPEN, last updated 2026-11-05).
* PRD Profile Journey Contract, Provider / contractor contact: "Staff-facing constructed package intake -> submission, correction and evidence checklist ... No provider portal, identity claim or self-approval." The PRD (0.21.0) is `in-review`, unsigned, so this is the product direction, not a signed approval.
* PRD non-goals: "A provider portal or scheduling API as a prerequisite; intake may be demonstrated through constructed uploads and approved channel-neutral records."

### Decision authority and status (exact)

| Item | Exact status text | Source | Class |
| --- | --- | --- | --- |
| ADR 0007 | "Proposed on 2026-11-04. Not accepted. This record does not close criterion 6 of issue #132: the owner has not decided, and the provider identity model in #116 is open." Its own "Owner decisions needed": accept, change or reject option A "recorded with date and name"; authorise the staff-only slice; confirm option B is deferred and who owns the #116 identity decision | `docs/adrs/0007-contractor-intake-staff-mediated-proposal.md` | Proposal; now stale on "owner has not decided" |
| Owner decision on issue 132 | "Owner decision2026-11-09: "Proceed with existing-staff-mediated synthetic demo intake". This authorizes separating an existing-authenticated-staff-only synthetic job-pack/evidence intake slice from the unresolved contractor identity dependency. ... Provider portal/contractor identity, new accounts/permissions, actual contract instructions, resident consent and live/production acceptance are NOT authorized. ... This supersedes the earlier missing staff-slice owner decision, not the remaining production identity gates." | issue comment 6753054374 (2026-11-09T22:22:47Z, posted from the owner's account) | Owner direction, synthetic demonstrator only |
| Owner extension | "No contractor portal, new permissions, real resident data or deployment authority is granted." | comment 6781841422 (2026-11-10) | Correction authority and boundaries |
| Coordinator status read | "The scoped staff-mediated decision is documented, but formal ADR #1150 acceptance is unverified, so AC6 stays unticked." | comment 6782922828 (2026-11-11T00:11:22Z) | Status read, not a decision |
| ADR 0002 staff identity | "Status: accepted by the AMA project owner on 2026-10-24 for staff identity and application-role authority. This records the owner's direction, not a completed implementation or successful acceptance test." The ADR as a whole stays "Proposed" and "does not record approval by the owner, the DPO, Legal, the Board, control owners or any customer role." | `docs/adrs/0002-pilot-readiness-architecture.md` Status; section "Entra-authoritative staff access" | Accepted bounded owner decision (staff identity only); release gates (external forged-header and direct-origin probes) are open |
| ADR 0005 precedent | "Accepted for synthetic development only by the exercise owner, Juan Manuel Servera, on 2026-10-16 ... Neither decision supplies real company Legal, Compliance, DPO or control-owner approval" | `docs/adrs/0005-regulatory-compliance-assistant.md` Status | Precedent for naming the exercise owner and limiting acceptance to synthetic use. ADR 0005 is wholly accepted for synthetic development, so it is not the precedent for a bounded section inside a Proposed ADR; ADR 0002 is |

Verbatim comment 6753054374 (complete, read through `gh` on 2026-11-11; the table cell above is an excerpt with marked omissions):

```text
Owner decision2026-11-09: "Proceed with existing-staff-mediated synthetic demo intake". This authorizes separating an existing-authenticated-staff-only synthetic job-pack/evidence intake slice from the unresolved contractor identity dependency. Worker confirmation, receipt/acknowledgement and independent QA acceptance remain separate; no self-approval. Provider portal/contractor identity, new accounts/permissions, actual contract instructions, resident consent and live/production acceptance are NOT authorized. Beginning scoped RPI readiness/implementation preparation; no unsupported acceptance ticks or whole-issue closure. This supersedes the earlier missing staff-slice owner decision, not the remaining production identity gates.
```

Gap: the owner decision exists only as an issue comment (and is quoted in tracking research). No document under `docs/` records it. ADR 0007 still says the owner has not decided, so the repository contradicts the issue thread. The comment is posted from the owner's account and states the owner's quoted words, but the original owner message is not in the repository, so the exact verbatim provenance is relayed, not independently verified here.

### Implemented behavior (current source, not an approval)

* `auth.py` defines two modes: `ZF_AUTH=password` (development shared-password provider, refused when `ZF_ENV=production`) and `ZF_AUTH=trusted-proxy` (Azure Container Apps built-in Entra authentication, opt-in, fail closed; needs `ZF_ENTRA_TENANT_ID` and `ZF_TRUSTED_PROXY=1`; roles from the Entra app role, never a staff file). The module states "Nothing here validates a token signature; that is the platform's job". ADR 0002 records that the external negative probes remain a release gate.
* `DEFAULT_ROLE_MAP` includes `ZavaForward.Contractor` to `Contractor`. This is an existing application role label whose read projection is limited (`projection.is_contractor`; contractor reads only `me`, `cases`, `case`, `workorders`). It is not an accepted contractor identity model, onboarding, B2B guest or lifecycle, and must not be cited as one.
* `staff_intake.py`: `_staff_only` refuses the Contractor role ("Job pack intake is for staff. Ask the contract manager."); capture, correct and acknowledge take an authenticated staff user; the worker is a named person in the record and staff cannot be recorded as the worker by identifier; the keying-in staff member, corrector and acknowledger join the participants so independent QA bars them from accepting; status is "Receipt acknowledged - not accepted". The escalation destination comes from `ZF_STAFF_INTAKE_ESCALATION_*` environment values and shows "Unknown - not configured" when unset; there is no escalation write path.
* `staff-intake.js`: "Staff open a synthetic job pack and key in evidence the worker has confirmed. It is not a provider portal and gives no one new access."
* Routes in `server.py` (`GET /api/workorders/<id>/job-pack`-family and the `POST` actions) delegate to `staff_intake.handle` for the signed-in user; no public or provider route exists.
* Fixture logins (password mode, synthetic users) are test and demo identities. They do not authenticate actual workers or actual staff.

### Existing accepted decision versus proposal versus unknown

* Selection of the delivery channel for the synthetic demonstrator: an owner direction exists (comment 6753054374). It is not yet recorded in any repository decision document, and ADR 0007 is still Proposed. Status: owner-directed for the demo, unrecorded in `docs/`.
* Identity approach for staff: an accepted bounded owner decision exists (ADR 0002, 2026-10-24, Entra-authoritative staff identity). The staff intake reuses it unchanged. The contractor is a named record, never a signed-in actor: this is ADR 0007's proposed wording, and the owner's 2026-11-09 comment is consistent with it ("existing-authenticated-staff-only", "Provider portal/contractor identity ... NOT authorized") but does not itself adopt the ADR text.
* Provider portal and contractor identity (option B, #116): deferred and unresolved. Unknown: who owns the #116 identity decision (ADR 0007 owner decision 3 was never answered), contractor onboarding, B2B guest lifecycle, conditional access, lawful basis, DPIA and any Legal, Compliance or DPO position. Not company facts in evidence.
* Any actual provider, service or identity arrangement for Zava North Homes: unknown and unapproved. The case study supplies no contractor identity arrangement; selecting a demonstrator interaction route is not approval of one.

### Does an existing accepted decision already meet the literal criterion?

No, not as a recorded decision. The owner direction supplies the substance of the channel and staff identity choice for the synthetic demonstrator, but (a) the only authoritative record is an issue comment, (b) the repository's decision record (ADR 0007) says the opposite ("owner has not decided"), and (c) the coordinator's own 2026-11-11 reading is that formal ADR acceptance is unverified. The criterion's wording is also unscoped ("whether delivery is staff-mediated or a provider portal, with identity approach"): the demonstrator-scoped decision answers "staff-mediated" and "existing authenticated staff identity", and explicitly defers the production provider identity.

### Smallest safe demo-only decision

Record, in the existing ADR 0007, the owner's already-given 2026-11-09 direction as a bounded synthetic-demonstrator decision: option A (staff-mediated intake), identity approach "existing authenticated staff only under the ADR 0002 owner decision; a worker is a named person in the record, never a signed-in actor", option B deferred, #116 and every production identity, provider, consent, Legal, Compliance and DPO decision unresolved. This follows the ADR 0002 precedent of a bounded owner-decision section inside an ADR whose whole status stays Proposed, and the ADR 0005 precedent of naming the exercise owner and limiting the decision to synthetic use. The owner comment authorises the staff-mediated synthetic route; it does not adopt ADR 0007's option A text verbatim, so the record must say owner-directed and must not assert formal acceptance of option A. It adds no portal, grant, auth bypass, public access, provider send or production claim, and needs no new owner policy decision: it transcribes an existing owner decision and a technical selection of the demo interaction route.

### Genuine human approval and unknowns that remain

* Whether the owner treats the demo-scoped, transcribed decision as satisfying the unscoped criterion wording and authorises the tick. That is Root's and the owner's decision; this task authorises neither tick.
* Confirmation that option B is deferred and who owns the #116 decision (ADR 0007 owner decision 3). If the criterion is to be read as needing a named owner for the production identity, that is a focused owner question, not something to fabricate.
* Verbatim owner provenance of the 2026-11-09 words (the comment relays a quote; the owner's original message is not in the repository).
* Real company approval: Legal, Compliance, DPO and identity-owner approval for any real worker access, as ADR 0005 and ADR 0002 already state.

### Dependency on the escalation criterion

The other open criterion (variations and escalations reach a named owner) is out of scope. The channel decision does not depend on it: ADR 0007 records escalation routing as a rule that "goes to a named contract manager or the building safety liaison", and the code shows "Unknown - not configured" because no named owner exists in evidence. Closing the decision criterion does not need that criterion, but whole issue 132 closure does, and it needs a named owner, a company fact not in evidence.

## Planning Readiness

`Ready` for a docs-only plan: one in-place ADR 0007 amendment, one index line and one log entry. No new file, ADR or identity architecture is required.

## Follow-ups

1. Root admits (or declines) the docs-only record of the existing owner direction in ADR 0007 (this task's plan).
2. Owner answer, if the whole criterion is to be ticked: is the demonstrator-scoped decision sufficient, and who owns #116.
3. Named variation and escalation owner (other criterion, out of scope).
