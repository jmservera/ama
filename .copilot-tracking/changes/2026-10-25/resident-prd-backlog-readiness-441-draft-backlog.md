---
title: Draft resident backlog for owner acceptance (issue 441)
description: Proposed bounded delivery slices for the unsigned resident PRD increment, not an approved implementation baseline
ms.date: 2026-10-25
---

## Status and boundary

DRAFT BACKLOG, DOCUMENTATION ONLY. This is not an approved implementation
baseline. The owner has not accepted it. No GitHub implementation issue exists
or is created from it, no runtime work is authorised, and no application code
changes in this slice. No real accounts, messages, deployments, paid calls or
live acceptance are involved. The PRD (v0.21.0) and BRD (v0.21.0) remain
unsigned drafts; Validate and Govern are not passed.

Inputs: owner decisions in issue 441 comment 6389938010 and the coordinator
follow-up 6391945752, PRD v0.21.0 resident increment (PRD::FR-062 to FR-071,
PRD::AC-111 to AC-140, PRD::NFR-018 to NFR-021, twenty stories PR442-S01 to
S20, stages R0 to R5, six journeys), the BRD resident requirements
(BRD::FR-053 to FR-062, BRD::AC-104 to AC-126; staff access BRD::FR-063/064 and
BRD::AC-127 to AC-132 is a separate namespace) and the unregistered proposal.
Namespaces are never joined on the bare number. The staff-access requirements
(PRD::FR-072/073, PRD::AC-141 to AC-147) are out of this backlog.

## Owner decisions applied

| Decision | Applied as |
| --- | --- |
| Resident ordinary case/status/receipt API p95 <=2s, five synthetic concurrent sessions, 30 minutes | PRD NFR-021/AC-139, resident-audience routes only |
| Upload <=10 MiB per file | Resident requested-upload route only (RB-11) |
| Preserve staff/core targets; explicit shared-operation applicability | PRD target applicability table; NFR-002 unchanged; RB-03 builds the audience classification |
| Provider-neutral synthetic identity first, no provider selected | RB-04 replaceable identity boundary with synthetic fixtures; OD-54/OQ-030 stay open |
| First milestone M1 | RB-01 to RB-10: sign-in, own case/documents, cross-case denial, representative revocation, assisted recovery |
| Date only after engineering sizing | Not yet estimable, see Sizing |
| Return for owner acceptance before implementation | Acceptance gate G0 below |

## Existing coverage reused, not duplicated

* Issue 444 (open, read-only loopback synthetic resident preview, branch
  `feat/resident-feedback-preview-444`, local worktree head a3e527fd, not
  pushed at inspection) already plans: resident projection with a positive
  field allowlist, server-owned synthetic identity harness, default-deny
  grants with expiry and revocation tests, two-resident and representative
  tests, offer versus confirmed appointment text and visible unavailable
  writes. RB-05, RB-06, RB-08 and part of RB-02 reuse its modules; their delta
  is stated per item. 444 excludes uploads, downloads, messaging, consent and
  AI, and is loopback only.
* Related open issues are references, not ordering edges: 154 resident UX, 86
  resident decisions and representatives, 128 accessibility testing, 121 data
  protection, 175 synthetic data provenance, 232 housing officer screens, 74
  versioned home case. Overlap is checked per item before any issue is
  created. No new issue duplicates their scope.

## Hierarchy

Hierarchy is organisational grouping only and is not a blocking dependency.

* Epic E0 (this readiness lane): G0 acceptance gate, RB-G1 to RB-G4.
* Stage R0: RB-01, RB-02, RB-03.
* Stage R1: RB-04, RB-05, RB-06, RB-07.
* Stage R2: RB-08, RB-09 (M1 portion); RB-11, RB-12 (post-M1).
* Milestone M1 evidence: RB-10.
* Stage R3: RB-13 to RB-16.
* Stage R4 (gated, not startable): RB-17 to RB-20.
* Stage R5: RB-21, RB-22, RB-23 and RB-24.

## Draft slices

Size is a relative complexity hint for discussion (XS to XL), not an estimate,
not a duration and not additive. Acceptance statements elaborate the cited
PRD criteria; all stay Not run.

| Key | Slice and bounded scope | Trace (qualified) | Testable acceptance (Not run) | Exclusions and gates | Size hint |
| --- | --- | --- | --- | --- | --- |
| RB-01 | Freeze the resident protocol: story/AC/journey expectations, namespace-qualified trace, evidence manifest schema and unrun-state vocabulary. Documentation and test specification only | PRD::GOAL-005, PRD::AC-140; BRD::FR-062 | Every PRD::AC-111 to AC-140 has expected and Not-run observed fields; no renumbering; reviewed by product and engineering | No application or provider call | S |
| RB-02 | Versioned provider-neutral synthetic fixture pack: two unrelated residents, multi-occupant household, appointment-only and interpreter-only representatives, current/revoked/disputed grants, approved/internal/superseded documents, one upload request, one offered slot, one ambiguous intake. Reuse 444 fixture lineage and the generated 60,000-home/980-case stock links; unverified links stay unknown | PRD::FR-062/069; PRD::AC-111/113/126; PR442-S02 | Fixture hash and provenance recorded; no real identifiers; canary values present; reviewed for PII-free provenance | Initial fixtures are not final exercise acceptance; Azure, real SQL and registered AI evidence still required by PRD::CON-009/AC-057 | M |
| RB-03 | Target applicability and measurement design: audience/route classification for every request, frozen request mix and sample method for NFR-021, per-audience reporting, unit handling for 10 MiB versus 5 MB, minimum sample count and error/timeout ceiling, owner and location of the frozen request mix, rule for resident-audience classes not listed in the PRD applicability table, staff-limit check on promoting a resident file, open question on the 100 MB total | PRD::NFR-021; PRD::AC-139; PRD::NFR-002; BRD::OD-55 | A shared operation yields two separately reported audience distributions; an unclassifiable request is unresolved and cannot pass; no staff target is weakened | Design only; the load run belongs to RB-24. No production capacity or 60,000-user claim | S |
| RB-04 | Provider-neutral identity boundary: server-side validation of a synthetic identity assertion behind a replaceable interface; no custom password store; identity establishes a person only | PRD::FR-069; PRD::AC-127/128; PR442-S01; BRD::FR-060, BRD::AC-116/117 | Synthetic sign-in succeeds without staff membership and shows no case until a current grant passes; browser-supplied identity or role is ignored | No provider, tenant, enrolment, real account or Entra resident use; OD-54/OQ-030 open; separate from staff Entra work (360) | M |
| RB-05 | Grant model and server enforcement on shared case authority: subject, case, allowed fields/actions, validity; default deny; resident-specific routes distinct from staff routes. Delta over 444: grants held in the shared case store rather than a disposable preview dataset | PRD::FR-062/069; PRD::AC-111/113/126; PR442-S02; BRD::FR-053/060, BRD::AC-104/105/116 | Two residents, unrelated subject, direct id, search, export and model-context attempts return only granted scope with no existence metadata | No staff app role grants resident case access; no persisted real data; coordinate store changes with 444 and 350 before editing | L |
| RB-06 | Representative revocation and disputed authority: task-limited grants, revocation denying the next request in an open session, protected grant history retained | PRD::FR-069; PRD::AC-126/127; PR442-S04; BRD::AC-116/117 | Appointment-only, interpreter-only, disputed and revoked authority behave as specified; revocation denies the next protected request | Representative reference alone grants nothing; no consent or works authority inferred | M |
| RB-07 | Assisted recovery and safe logout: identity and grant revalidated separately, no cached prior content for the next user, a person route always available | PRD::FR-068/069; PRD::AC-125/127/128; PR442-S03; BRD::FR-059, BRD::AC-115/117 | Recovery never broadens rights; no account enumeration or emailed passwords; shared-device logout hides prior content | Real recovery policy, session and abuse settings stay unapproved (OQ-030); no real contact | M |
| RB-08 | Own case timeline and next action from a positive-allowlist resident projection with recorded-as-of and unknown/stale text. Delta over 444: server-side projection reused in the shared authority and added to the shared event timeline | PRD::FR-062; PRD::AC-111/113; PR442-S05; BRD::FR-053, BRD::AC-104/105 | Fields agree with the staff source; no internal note, safeguarding, finance or unrelated case appears in responses, HTML or errors | Consent and decisions never inferred; non-digital explanation uses the same projection | M |
| RB-09 | Approved document version view for the granted case, including revoked-link and superseded handling. Delta over 444 (no downloads): publication-authority fixture and download path | PRD::FR-062; PRD::AC-112/113/126; PR442-S06; BRD::FR-053, BRD::AC-104/105 | Only the current granted published version is returned with source and version; cache or link cannot bypass revocation | Publishing authority is staff; quarantine and review stay separate (RB-12) | M |
| RB-10 | M1 evidence review: journeys 1 (sign-in/recovery) and 2 (own case/documents) with their criteria reported individually, essential privacy and accessibility checks, exact versions | PRD::AC-111 to AC-113, AC-126 to AC-128, AC-134/135; PRD::GOAL-005 | Expected and observed-or-Not-run recorded for each cited criterion; critical privacy or accessibility miss blocks M1 | A passing M1 is synthetic engineering evidence only, not owner acceptance, live acceptance or conformance; PRD::CON-009/AC-057 still applies | S |
| RB-11 | Requested upload, post-M1: PDF/JPEG/PNG, one file/request, at most 10 MiB, quarantined, durable receipt, lost-ack retry creates one effect | PRD::FR-063; PRD::AC-114/115; PR442-S07; BRD::FR-054, BRD::AC-106/107 | Wrong type, oversize, interruption and retry cases follow PRD::AC-114/115 | Staff/core 5 MB and 100 MB limits unchanged; promotion to staff evidence is separate | M |
| RB-12 | Scan and review separation, post-M1: clean is not accepted or published; 60-second pending scan offers assisted follow-up; never fail open | PRD::FR-063; PRD::AC-114/115/135; PR442-S08 | Malicious, malformed and scan-outage fixtures stay inaccessible to readers and models | No real scanning provider chosen; no paid service | M |
| RB-13 | Appointment response and postponement as a response, not a booking | PRD::FR-064; PRD::AC-116/117; PR442-S09/PR442-S10; BRD::FR-055, BRD::AC-108/109 | Confirmation still needs staff, resident-authority and contractor capacity; urgent action never delayed | No consent, refusal or no-access inference | M |
| RB-14 | Shared event contract and labelled manual-channel intake with replay and ambiguity handling | PRD::FR-065/068; PRD::AC-118/119/125; PR442-S11/PR442-S12; BRD::FR-056/059 | Replay creates no duplicate effect; ambiguous match discloses nothing and enters an owned queue | No connector assumed; manual capture labelled | L |
| RB-15 | Owned exceptions and accepted-handoff queues | PRD::FR-066; PRD::AC-120/138; PR442-S13; BRD::FR-057 | Delivery never closes a handoff; next owner and update always visible | Synthetic ages are fixtures, not SLAs (OQ-028) | M |
| RB-16 | Verified contact and help requests with no portal detriment | PRD::FR-068; PRD::AC-124/125; PR442-S14; BRD::FR-059 | Same route and priority without portal use; unverified contact pauses | No staffing or channel commitment | S |
| RB-17 | R4 sourced status/process proposal, disclosed as AI | PRD::FR-067; PRD::AC-121/122; PR442-S15; BRD::FR-058, BRD::AC-113/114 | Each material assertion has source, version and as-of; held for named review | BLOCKED until a separate task registry entry, evaluation and release; no paid call or send | Not sized |
| RB-18 | R4 abstention and owned human route | PRD::FR-067/068; PRD::AC-122/123/125; PR442-S16; BRD::FR-058/059 | Missing evidence, injection, timeout, distress and controlled-domain requests produce no unsupported assertion and a traceable owned route; urgent help independent of the model | BLOCKED as RB-17 | Not sized |
| RB-19 | R4 deny-by-default dispatch policy decision | PRD::FR-070; PRD::AC-129/130; PR442-S17; BRD::FR-061, BRD::AC-118/119 | Any absent, expired or mismatched condition prevents dispatch; a future positive test uses a labelled simulated outbox only | BLOCKED; OD-53 evidence needed for any activation; per-message human review default and routine automation OFF | Not sized |
| RB-20 | R4 suspension and actual-disposition audit | PRD::FR-070; PRD::AC-131/138; PR442-S18; BRD::FR-061, BRD::AC-118/119 | Next dispatch denied after suspend; disposition auditable without an invented reviewer; restart needs distinct authorisation | BLOCKED as RB-19 | Not sized |
| RB-21 | Frozen paired effort and adverse-outcome protocol | PRD::FR-071; PRD::AC-132/133; PR442-S19; BRD::FR-062 | Matched packs, disjoint episodes, review and recovery effort included; unknowns stay unknown | No savings, uptake, cash or headcount claim | M |
| RB-22 | R5 six-journey milestone evidence manifest | PRD::GOAL-005; PRD::AC-134 to AC-140; PR442-S20 | All six journeys and 30 criteria reported individually; criteria whose slices are blocked (RB-17 to RB-20) or unbuilt are reported Not run or blocked, so the manifest cannot satisfy R5 or AC-140 until they have evidence | Not acceptance; owner decides | S |
| RB-23 | Accessibility and plain-language checks at 320, 390 and 1280 CSS pixels and 200% zoom, keyboard and screen reader, against the WCAG 2.2 AA engineering target | PRD::NFR-018; PRD::AC-134 | Each script reported; lost focus or blocked action fails the script | No conformance or participant validation claim; reuse 154 and 128 work | M |
| RB-24 | NFR-021 load and resilience run: five synthetic sessions (three resident scopes, two staff), 30 minutes, outage and restart drills | PRD::NFR-021, PRD::NFR-020; PRD::AC-137 to AC-139 | Resident p95 <=2s reported with all errors; staff requests reported against NFR-002 thresholds as observations only (two staff sessions are not the NFR-002 core workload); sign-in, scan and model waits separate | Synthetic data only; no spend; no production scale inference | M |

Governance and approval items (not engineering slices):

| Key | Item | Owner and state |
| --- | --- | --- |
| G0 | Owner accepts, amends or rejects this backlog, its sizing assumptions and the M1 composition | Owner; PENDING. Nothing starts before this |
| RB-G1 | Fresh independent requirements-quality review of PRD v0.21.0 | Requirements owner; PENDING. Inherited findings below stay open |
| RB-G2 | OD-52 to OD-55 and OQ-028 to OQ-031 named owners and evidence | Programme and delegated owners; OPEN |
| RB-G3 | Native architecture registration of the unregistered proposal | Owner deferred; id null, registration UNMET; no ID guessed and no workaround |
| RB-G4 | Later accepted application build needs real Azure, real SQL and registered real AI evidence | PRD::CON-009, PRD::AC-057; synthetic slices do not satisfy it |

## Dependencies (explicit, separate from hierarchy)

| Item | Depends on | Reason |
| --- | --- | --- |
| RB-02, RB-03 | RB-01 | Fixtures and measurement design need the frozen protocol |
| RB-04 | RB-02 | Synthetic identities come from the fixture pack |
| RB-05 | RB-02, RB-04, 444 modules | Grants need subjects and the 444 projection |
| RB-06, RB-07 | RB-05 | Revocation and recovery act on grants |
| RB-08, RB-09 | RB-05 | Projection needs the entitlement check |
| RB-10 | RB-03, RB-04 to RB-09, RB-23 (M1 scripts only) | Evidence for the first milestone |
| RB-11, RB-12 | RB-05, RB-09 | Own-scope and publication boundary |
| RB-13 to RB-16 | RB-05, RB-08, RB-14 for RB-15/16 | Shared event contract |
| RB-17 to RB-20 | RB-15, plus external OD-53 gate | Independently gated |
| RB-21, RB-24 | RB-10 to RB-16, RB-03 | Measurement after the slices exist |
| RB-22 | RB-10 to RB-16 and RB-17 to RB-20 evidence or recorded blocked status | R5 needs all 30 criteria reported |

No dependency on live Azure, real accounts, employee Entra (360) or paid
inference is claimed unless a specific technical dependency appears during
sizing; that is an unknown, not an edge.

## Sizing assumptions, unknowns and date

A delivery date is **not yet estimable**. No engineering sizing exists, no
team capacity or velocity is recorded, and the unknowns below change the
critical path. This backlog proposes no date. After owner acceptance of the
slice list, engineering provides three-point estimates per slice with named
assumptions; the critical path for M1 is RB-01, RB-02 and RB-03 (R0 freeze), RB-04, RB-05, then
RB-06/07/08/09 in parallel if capacity allows, then RB-10. Only then may a date
with buffer be proposed for separate owner acceptance.

Assumptions to validate: synthetic fixtures only; resident routes reuse the
existing SQL case authority; 444 modules merge before RB-05 starts or are
reused by agreement; one shared test environment; capacity is shared with the
priority employee access repair and other open lanes.

Unknowns: team capacity; whether 444 merges as implemented (it is unpushed
local work at inspection); identity-boundary shape without a provider;
whether resident files count toward the 100 MB evidence total; MB versus MiB
reading of the staff 5 MB limit; accessibility test resources and screen-reader
tooling; shared SQL schema change effort; reviewer availability.

## Inherited quality findings (unchanged unless stated)

| Finding | State in this slice |
| --- | --- |
| pr442-qual-005 High, bundled FR-044/FR-060 and AC-104 to AC-106 | Unresolved |
| pr442-qual-040 High, unsigned BRD and absent governed handoff | Unresolved |
| pr442-qual-006 Medium, feasibility | Unresolved; sizing is the next evidence |
| pr442-qual-024 Medium, GOAL-005 SMART | Unresolved; no date set |
| pr442-qual-041 Medium, latency and file-size precedence | Authored text corrected using owner answers; needs fresh independent review; not closed |
| pr442-qual-009 Low, table shape | Unresolved |
| pr442-qual-039 Low, FR-059 trace | Unresolved |

BRD, original case study, legal snapshots, owner memory and numbered ADRs are
unchanged. OD-52 to OD-55, registration UNMET and the assisted-channel and
no-detriment commitments remain.
