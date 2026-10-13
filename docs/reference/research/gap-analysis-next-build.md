---
title: Gap Analysis and Next Build
description: Review of the BRD, PRD, ADR, use case and addendum against the research and the working MVP, with the missing items ranked for the next build
author: AMA programme
ms.date: 2026-10-13
ms.topic: reference
---

## Scope and evidence

The later #65 [current handover](../../../infra/README.md#current-exercise-handover-2026-10-13)
and [ADR delivery delta](../../adrs/0002-pilot-readiness-architecture.md#current-exercise-delivery-delta-2026-10-13)
record recovered deployment/identity blockers. The dated reviews below remain
historical gap evidence, not an instruction to rebuild completed features or
a claim that remaining product/human gates passed.

### Current Build Direction (2026-10-11)

The ranked reviews below are dated snapshots, not an instruction to rebuild
features subsequently delivered. [Pinned #58 learning](../../ideas/typesafe-system-one-agent-fit.md#observed-feasibility-and-parallel-value-experiment-2026-10-11)
at `5136f192d583a5bf53adeeec4b0f21369b005c9d` records the continuing
60,000-home/980-case generated-data MVP with actual Azure SQL/Blob,
Decision 1 selection and cited generation. Later source controls are not
automatically deployed. Full workflow, permissions, cloud performance/
recovery and direct human acceptance remain distinct from those observations.

BRD v0.16.0 and PRD v0.13.0 candidates require real AI/SQL/Azure in
every subsequent accepted application exercise build: delivered AMA
prototype/PoC/MVP or update, not docs/unit/CI checks. Reuse the existing
application, generated data and platform contracts. Local state/mocks and
small fixtures support tests, not accepted delivery; no wholesale import
of an unmerged PR or guessed stock-to-case links. AC-086/AC-057 specify
changed-build identity/workflow/inference and SQL restart evidence.

The parallel four-arm experiment may accept/reject narrow Decision tasks,
not waive the required platform or whole-app AI. Proposed protocol is not
executed benefit evidence; binary support is not three-class F1. Preserve
current source/image/revision and per-task results, effective scoped budget/
authorization and cost/usage controls. Independent integration/control work
can proceed while quality/value adoption awaits reviewed results.

### Draft Experiment Closure Review (2026-10-13)

PM review and the requested UX Designer source review compared all four open
drafts with `main` at `71aaf9d9833804f2dc1d8bcc4907aa12a95883dc`.
The pins below are the inspected draft heads. None is an ancestor of that
main commit; retirement must not be described as all code having merged.
Branding-only normalization helps compare renamed paths, but a different
file does not by itself prove either missing or equivalent behavior.

Evidence is source-inspected, historically reported, or reviewer
interpretation, not fresh execution. No draft was run or deployed, no new
human study was performed, and no resource was deleted. Previous tests,
owner feedback, old browser runs and automated reviews retain their original
scope. The [UX synthesis](./ux/prototype-learnings-and-simplicity-review.md#draft-ux-closure-review-2026-10-13)
and [ADR learning](../../adrs/0002-pilot-readiness-architecture.md#retained-draft-architecture-learning-2026-10-13)
own the detail.

| Draft and inspected head | Retained learning and unique work | PM/UX recommendation |
| --- | --- | --- |
| [#19](https://github.com/jmservera/ama/pull/19), `5e52ceb7d5937f21a5eb7380ad009833608ed811` | Historical Python demonstrator: bounded read-only agent, explicit failed/unfinished runs, source-preserving workbook preview/import and local persistence. Its optional-inference/private-network templates are not the current deployment contract. Four task perspectives are not authenticated role journeys. | Ready to retire as learning after this capture merges and the owner authorizes closure. Preserve pinned evidence; deliberately do not import its alternative app, seed/import scripts or compile-only infrastructure. This is not acceptance of its code or a claim that every unique file was delivered elsewhere. |
| [#24](https://github.com/jmservera/ama/pull/24), `6029dc248911ddd3eebece5fb2067d881920494c` | Local Node PoC: transactional state/event/replay records, exact-intent retry, owned unknown-outcome recovery, separate handover reacceptance and scope-reconciled metrics. Nine constructed workflow fixtures, simulated roles and assistant do not establish real identity, AI or Azure acceptance. | Ready to retire as learning after capture and owner authorization; do not merge a second local application. Its reported 40 tests, five simulator fixtures and localhost GET p95 61.52 ms remain historical technical evidence, not cloud load or human value. |
| [#27](https://github.com/jmservera/ama/pull/27), `51d8ae41caaa4535ad53c7268f874ce5334242ee` | Architecture/runbook/resource split pinned to implementation `40e248a9f29bd518da0be1b9da233e422de46058`, not #24's final head. Local resource ownership, persistence and teardown boundaries are reusable; its proposed services and no-Azure-resource statement describe that experiment only. | Ready to retire after applicable learning is filed here and in ADR/UX homes, with owner authorization. Keep the old runbook as pinned history, not today's operator instructions; no independent application or UX pass follows from this docs-only PR. |
| [#58](https://github.com/jmservera/ama/pull/58), `6cbcb36e63597c6f4b90268207b5f1afbce4bb4a` | Continuing generated-data MVP with unique stock, connected-home/building, source-bound forms, forecast, portability and event journeys, plus later work-order/evidence/financial controls. These are not all in current main. Earlier real inference/deployment and later source tests are distinct observations. | Keep draft. Selectively carry forward, demonstrate an equivalent, or explicitly defer each capability below before retirement. Do not merge wholesale or mark accepted; preserve the owner's current-infrastructure validation gate and the earlier Partial / Not accepted review. |

#### #58 Carry-Forward and Acceptance Queue

This is a disposition queue against existing requirements, not approval of
new scope or a commitment to implement the old branch. Proposed accountable
roles below are review responsibilities, not confirmed company assignments.
All rows remain unresolved; closing the code requires an explicit owner
decision on carry-forward, demonstrated replacement or deferral.

| Capability requiring disposition | Pinned evidence and current-main gap | Existing contract and closure evidence |
| --- | --- | --- |
| Stock workspace and programme linkage | [Stock UI](https://github.com/jmservera/ama/blob/6cbcb36e63597c6f4b90268207b5f1afbce4bb4a/mvp/web/exercise.js#L165-L221) filters/pages the 60,000-home stock separately from 980 programme cases. Main has a case map, not this stock route. | FR-004/012/035, AC-006/040/043; Data/Programme review search, filtered population/map versus displayed page and explicit unknown stock-to-case links. Do not invent joins. |
| Linked home/building isolation and controlled events | [Connected UI and event editor](https://github.com/jmservera/ama/blob/6cbcb36e63597c6f4b90268207b5f1afbce4bb4a/mvp/web/exercise.js#L224-L289) and [lifecycle actions](https://github.com/jmservera/ama/blob/6cbcb36e63597c6f4b90268207b5f1afbce4bb4a/mvp/web/exercise.js#L379-L477) are absent as connected routes in main. Adjacent generic panels are not evidence of equivalence. | FR-001/002/009-011/014/015/022/033/035; Programme and resident/safety owners test sibling independence, scoped return/review, distinct handoff/update ownership and recovery without old shortcuts. |
| Source-bound form and independent pack review | [Forms UI](https://github.com/jmservera/ama/blob/6cbcb36e63597c6f4b90268207b5f1afbce4bb4a/mvp/web/exercise.js#L290-L375); draft `forms.py`/`decision.py` have no current-main equivalents. Generic AI notes do not establish these controls. | FR-036 to FR-044, AC-044 to AC-054; Finance/Data review source/hash/version, no-match/manual correction, deterministic totals, never-prefilled human-only fields, separate reviewer and export with no submission. AI quality/value stays separately evaluated. |
| Safe portability, import and bulk coordination | [Preview/export UI](https://github.com/jmservera/ama/blob/6cbcb36e63597c6f4b90268207b5f1afbce4bb4a/mvp/web/exercise.js#L64-L161) uses exact previews/fingerprints and partial row outcomes, unlike main's simpler import and CSV export. | FR-005-007/020, AC-007-010/023; Data/Programme review supported fields/formats, source preservation, conflicts, replay and forbidden consequential bulk actions against backend enforcement. |
| Forecast and stakeholder context | [Forecast UI](https://github.com/jmservera/ama/blob/6cbcb36e63597c6f4b90268207b5f1afbce4bb4a/mvp/web/exercise.js#L43-L57); draft `forecast.py`/`programme.py` are absent in main. Overview counts are not a validated forecast. | FR-021-024/035, AC-024-027/041/043; Data/Programme reconcile as-of, exact cohort/denominator, versions, unknowns, exclusions and uncertainty to retained events/oracles. |
| Version-bound quality, work release and financial lineage | Later draft `quality.py`, `procurement.py`, `finance.py` and `workflows.py` differ from current main; source presence/difference does not establish runtime parity. [ADR learning](../../adrs/0002-pilot-readiness-architecture.md#retained-draft-architecture-learning-2026-10-13) retains the regression semantics. | FR-009/010/013/016-019/043, AC-012/013/016/019-022/042/051; independent Quality, Programme and Finance review stale work-order/scope evidence, reacceptance, payment/milestone guards and preserved paid history/resident choice. |

For each carried change, record source, immutable image, config, endpoint and
ready revision on the continuing infrastructure, then verify actual Entra
roles/field access, SQL write/read/restart, permitted live AI and affected
workflow/recovery paths under CON-009/AC-057. The
[owner's gate](https://github.com/jmservera/ama/pull/58#issuecomment-6113913159)
named then-current `ca-warm-test-api`; the
[later handover](../../../infra/README.md#current-exercise-handover-2026-10-13)
identifies `ca-forward-test-api`. Neither old revision
`ca-properwarm-mvp--0000018` nor #65 welcome/identity work proves the
unmerged #58 source is delivered on that successor. Preserve the same stock,
programme history and evidence, with unknown relationships still unknown.

Representative task and accessibility checks remain Not run, including
queue/context restoration, honest map-to-list scope, role/workflow endpoints,
owned retry/conflict recovery and independently permitted approvals. The
available four-arm MVE evidence is a proposed protocol, not verified participant results or measured
15% net-effort improvement. Integration feasibility is not quality/value.
BRD v0.16.0 stays unchanged: no new business requirement, customer fact,
measured benefit or approval emerged. PRD v0.13.2 adds evidence/provenance
only; existing IDs, counts and candidate approval remain unchanged.

Retirement closes an obsolete research delivery route, not the requirements,
the continuing application, the open value experiment, production approval
or Azure/local resources. Merge the learning capture first; the owner decides
PR closure separately. Resource teardown requires a separate owned inventory,
preserved evidence/state and explicit authorization, never a copied historical
cleanup command.

Reviewed on 2026-10-08: the
[BRD v0.15.0](../../brds/agentic-retrofit-programme-brd.md), the
[PRD v0.9.0](../../prds/zava-forward-retrofit-programme-demonstrator.md),
[ADR 0001](../../adrs/0001-azure-architecture.md), the original case study, the
[addendum](../../case_study_48_addendum.md), the UX and company research, the
[capstone storage map](../../capstone/README.md), the latest rubric score
(31/100, outcome Incomplete) and the `mvp/` application merged in PR #34.

This is an internal judgement. It does not validate any company fact. Items are
gaps against the documents' own requirements, not new scope.

## What exists

| Area | State |
| --- | --- |
| Problem, case and value | Addendum, BRD and PRD are detailed and consistent in direction. Targets (20% cycle time, 25% effort) are proposals pending OD-18 |
| Architecture | ADR 0001 with options appraisal, threat model, data-store review, region choice and retention alignment. Bicep deploys end to end with a dev and a production profile |
| Working product | `mvp/` serves case lists, role-tailored My cases, All cases with owner filter, Overview map, Visits, Funding workflow, handover suggestions, documents, bounded Azure OpenAI drafts, audit chain and Excel import check. Deployed publicly on Azure Container Apps |
| Data | Constructed, realistic data from the stock register with generated names |
| Research | Sector baseline, regulatory snapshots, company-role challenges, UX simplicity review |

## Gaps, ranked

### 1. Capstone deliverables that score 0 (blocks the outcome)

The rubric records B1, B2, B3, B4, B5, B7, C2, C3 and D1 to D3 as 0, so the
outcome is Incomplete. None needs new product code.

| Missing asset | Store at | Covers |
| --- | --- | --- |
| Final deck with speaker notes | `docs/capstone/deck/` | B1, B2, B6, B7 |
| Demo script, rehearsal and Q&A transcripts, timing notes, recovery notes | `docs/capstone/pitch/` | B3 to B5, C2, C3 |
| One thought leadership artifact with a README (blog post of 800+ words with a publication link is the lightest option; a reference accelerator built from `mvp/` and `infra/` is the strongest) | `docs/capstone/thought-leadership/<name>/` | D1 to D3 |

### 2. The scorer does not see the MVP

`.github/rubric/artifacts.json` includes `src/**` and `prototype/**` for
solution code. The working application is in `mvp/`, so A4 (3/5) is scored on
the older in-memory prototype. Either add `mvp/**` (excluding `mvp/web/vendor/**`
and `mvp/data/**`) to the registry, or move the code. This is the cheapest
score gain and also the honest one, because the MVP is the real evidence.

### 3. Product gaps against PRD requirements

The MVP covers the staff day-to-day well. These PRD items are not built:

| Gap | PRD reference | Why it matters |
| --- | --- | --- |
| Real sign-in with Entra ID and role and field permissions enforced by the service. Today a shared password | FR-003, NFR security, OQ-005 | The controls story depends on it. Staff trust is the adoption risk |
| Durable storage: Azure SQL (or the chosen store), Blob for documents. Today ephemeral disk | ADR 0001, FR-001, FR-005 | State and uploads are lost on restart. Blocks any pilot |
| Bulk update with preview and the forbidden-bulk-action rules | FR-006, FR-007 | Excel users expect it; it must not bypass gates |
| Return and reopen with invalidation of downstream approvals | FR-009, FR-010 | Core to the case lifecycle, only partly present |
| Distinct handoff states (sent, received, accepted, returned, escalated) | FR-011, FR-033 | Handover today is an immediate owner change |
| Safety hazard referral, receipt and hold scope, with awareness time | FR-015, BRD safety control | Holds exist as a flag, not as a referral workflow |
| Procurement and capacity board; work-order and provider intake | FR-016, workflow 4 | No supplier or capacity screen yet |
| Quality acceptance, defects, reinspection and handover checklist | FR-017 | Largest missing lifecycle stage before completion |
| Budget, invoice match and grant ledger separate from claims | FR-018, FR-019 | Funding covers applications only |
| Funnel, event timeline, stakeholder export and forecast with uncertainty | FR-021 to FR-024 | Overview has counts and a map, not stage flow or forecast |
| Resident decision per measure with versions, pauses and complaints route | FR-014, BRD resident controls | Decision is one status per case |
| Missed-appointment threshold task (default 5) | FR-031, OD-40 | Exercise scenario owner asked for |
| Workflow-only path and paired comparison for every AI task, with evaluation harness | FR-028, PRD AI evaluation | The pilot gate decision (OD-34) needs this evidence |
| AI source citations on every output | FR-027 | Drafts say AI-drafted but do not cite sources |
| Accessibility checks (keyboard, screen reader). Map markers are not focusable | NFR-001, OQ-011 | Leaflet circle markers have no keyboard route; the list link is the only alternative |
| Observability: SLO measurement, dashboards, alerts | NFR section | None wired in the MVP |

### 4. Architecture gaps (ADR 0001 open items)

* Application images are built, but container hardening (non-root user,
  read-only root, dropped capabilities) and image scanning in CI are not done.
* Ledger digest upload and scheduled verification are not configured, so the
  tamper-evidence claim is unsubstantiated. The MVP's hash chain is a demo.
* The retention schedule is unapproved and the erasure versus immutable audit
  conflict is unresolved.
* Region: the MVP and `ama` group run in `uksouth`. The residency position
  (UK data at rest, inference possibly outside the UK) is open under OQ-012.
* Document Intelligence for scanned surveys and EPCs is deferred. The MVP reads
  documents with a vision model instead, which was not measured for accuracy.
* The public map tile service is a demo-only dependency (OSM policy). Production
  needs a licensed provider.
* Entra app registration, SharePoint site, Teams webhook and the SQL contained
  user script are unexercised.

### 5. Evidence and validation gaps

* No user has used the MVP. The PRD marks every journey as proposed, not
  observed. The riskiest assumption in the ADR, that role views over one case
  model reduce coordination effort, is untested.
* The Design Thinking cheap experiments (Excel shadowing with 3 to 5 staff,
  role task test against the current Excel method, Document Intelligence trial
  on 20 to 30 redacted documents) have not been run.
* No measured performance, load or cost for the deployed app. A5 stays at 2
  until real numbers exist.
* No AI evaluation results: held-out cases, draft acceptance, critical-error
  tests (the PRD requires zero missed critical exceptions in agreed tests).
* Open decisions that block live use: OD-14 (lawful basis, DPIA, retention),
  OD-17 (pilot locality), OD-18 (measurement definitions), OD-19 (allow and deny
  matrix), OD-36 (DPIA for measurement data). These need named humans, not
  more code.

### 6. Document consistency to fix

* The BRD, PRD and ADR still describe a read-only prototype slice (A, B, C) as
  the next step, while the MVP is already a writable application. Update the
  release framing so Slice A to C map to what `mvp/` covers and what remains.
* The PRD workflow coverage table lists nine workflows. The MVP covers
  prioritisation, resident service (partly), hazard (flag only) and funding
  (applications only). Record this as a coverage matrix.
* `mvp/` is not mentioned in the BRD or PRD traceability. Add FR-to-MVP
  coverage so requirement and code agree.
* ADR 0001 describes SQL and Blob; the deployed MVP uses neither. State the
  gap explicitly under Observed deployment measurements.

## Recommended next build

Ordered by value for the capstone and for a believable pilot. Each item is
small enough for one branch and pull request.

1. Capstone package (no product code): deck, pitch and Q&A transcripts, demo
   script from the MVP, and the thought leadership artifact. Removes the
   Incomplete outcome and about 40 points of 0 scores.
2. Register `mvp/` in the rubric artifacts, then add MVP evidence to the ADR
   (what is built, what is not).
3. Durable state: move the MVP store to Azure SQL and uploads to Blob, behind
   the existing `Store` interface, and run two replicas. Verify with a restart
   test. This closes the largest honesty gap.
4. Entra ID sign-in with role claims, replacing the shared password, plus
   field-level permission tests.
5. Lifecycle completion: return and reopen, handoff states, and the quality
   acceptance and defects screen. These finish the path from survey to handover.
6. Safety referral and hold workflow with awareness time and scoped release.
7. AI evaluation harness: a held-out set from the constructed data, workflow-only
   comparison, source citations on outputs and a critical-error test. This
   produces the evidence the pilot gate needs.
8. Coordinator insight: funnel, timeline, forecast with uncertainty and the
   stakeholder export.
9. Accessibility pass: keyboard route for map points, screen reader checks and
   a written test record.
10. Validation sessions: Excel shadowing and the task test with 3 to 5 people,
    recorded as evidence. Nothing else in this list replaces this.

Not recommended yet: Azure AI Search, Cosmos DB, a provider portal, live
integrations and payment execution. The documents defer or exclude them, and the
research gives no evidence that they are the binding constraint.

## Owner decisions (2026-10-08)

* `mvp/` replaces `prototype/` as the scored solution code. Done in
  `.github/rubric/artifacts.json`; `prototype/` is no longer read by the scorer.
* The next build targets pilot readiness (items 3 to 7 above), not the pitch
  first. Items 1 and 2 still matter for the rubric and run alongside.
* The thought leadership artifact is still to be chosen. Options below.

### Thought leadership options

Each is built from work already in the repository, so it adds evidence rather
than invention. The strongest candidates for D1 to D3 are the first two.

| Option | Idea | Format and audience | Effort |
| --- | --- | --- | --- |
| 1 | "Leaving Excel without losing control": how a housing association moves case management off spreadsheets with AI drafts, human approval and a data-handling baseline staff can trust | Technical blog post of 800+ words, or white paper of 2,000+ words, for housing digital leads and the AMA community | Low to medium |
| 2 | Reference accelerator: a case-management starter with role-tailored cards, a human-gated funding workflow, bounded Azure OpenAI drafts and a hash-chained audit log, built on constructed data | Repository with README (purpose, architecture, setup, limits) and a public link, for architects and partners | Medium |
| 3 | "Design for the person leaving Excel": the simplicity review and prototype learnings as architecture guidance | White paper, for product and design leads in social housing | Medium |
| 4 | Conference or community session on bounded agents in regulated housing delivery, using the pilot gate and paired-comparison design | Slides plus written notes and a recording link | Medium, needs a venue |

Recommendation: write option 1 as the artifact and link option 2 as the working
code. D3 needs a real publication or delivery beyond the cohort with link and
date, so choose the venue first.

## Owner direction on OD-14, OD-17, OD-19 and OD-36 (2026-10-08)

The owner answered these questions on 2026-10-08. They are owner direction for
the design baseline, not DPO, Legal or Board approval, and none is recorded as
ratified.

| ID | Question | Owner direction | Follow-up needed |
| --- | --- | --- | --- |
| OD-14 | Lawful basis for case management data | Contract (tenancy agreement) for service delivery; consent for decisions on works | DPO to confirm the basis fits each data class and the Article 9 condition |
| OD-14 | Vulnerability and health data | Contractors see only "needs notice and a named contact", never the reason; staff see the reason only with a role need | Define which roles have a need; test it in the role permission model |
| OD-14 | Retention defaults | Accept the addendum defaults as the design baseline | DPO and Legal approval; Legal to set limitation-related periods |
| OD-14 | Audit entries and erasure | Keep everything for the legal retention period | Differs from the addendum, which said audit entries must not hold deleted personal content. The DPO must confirm that an erasure request can be refused for audit data under Article 17(3), and the addendum and ADR are updated to say so |
| OD-36 | Pilot measurement | Individual staff time capture, with the staff's knowledge and a DPIA | Needs a DPIA before capture, a staff notice and a union or staff consultation view; use it for process measurement, not performance management |
| OD-17 | Pilot scope and ranking | Load the whole stock (about 60,000 homes). Home ranking is deterministic; AI prioritisation is a recommendation only (clarified 2026-10-08) | Differs from the BRD pilot of 80 to 100 candidate homes. Needs a decision on which homes are in live scope. Ranking rule: see the owner clarification below |
| OD-19 | AI authority | Recommend, draft, reconcile and flag only; a person approves every action | Detailed allow and deny matrix still to be approved by control owners |

Consequences for the build:

* Persistence must hold the audit data for the legal period, so the retention
  job must not delete audit content on an erasure request. Document the legal
  exception per request.
* Staff time capture needs an explicit staff notice, a DPIA and a consent-free
  basis agreed with the DPO. Capture is blocked until the DPIA exists.
* The data layer, search, map and filters must handle about 60,000 homes: paging,
  indexes, and map clustering instead of drawing every home.
* Home ranking is deterministic. The same data and the same published policy
  version must always give the same order, with visible reason codes, a
  versioned rule set owned by a named person, and tie-breaks that are fixed
  (for example open safety issue, then waiting days, then reference). Staff
  can still filter, sort and choose what to work on.
* AI prioritisation is a recommendation only. It sits beside the deterministic
  order, cites its reasons, can be accepted, edited or rejected with a reason,
  and never changes the ranking, a case or a queue by itself. It is evaluated
  against the deterministic order in the AI evaluation harness.

Pilot-readiness work that does not wait on approval can start now: durable
storage, Entra ID sign-in and role permissions, return and reopen, safety
referral, the AI evaluation harness and scale for 60,000 homes.

## Review against PRD v0.10.0 and ADRs after PR #36 (2026-10-09)

Reviewed `main` at `c6627e7` (MVP slices 1 to 3 merged) against the
[PRD](../../prds/zava-forward-retrofit-programme-demonstrator.md) requirements,
[ADR 0001](../../adrs/0001-azure-architecture.md) and
[ADR 0002](../../adrs/0002-pilot-readiness-architecture.md). Evidence: MVP unit
suite (154 tests) passing on the branch before merge, a read of `mvp/`, `infra/`
and `.github/workflows/mvp-ci.yml`, and keyword probes of the code. This is an
internal judgement, not company fact. Nothing was run in Azure.

### Closed since the 2026-10-08 gap list

Deterministic ranking with reason codes (PR-006, FR-012 in part), AI
recommendation kept separate with accept, edit and reject (PR-007, FR-026),
server-side field projection and a role-by-endpoint matrix (PR-002, FR-003),
return and reopen (FR-009, FR-010 in part), handoff states and safety referral
(FR-011, FR-015 in part), keyset paging and server-side map clusters at 60,000
homes (PR-005), time capture behind flags (PR-004), Entra provider code,
`DocumentStore` with Blob, accessible map list, import check and CSV export
(SA-005, SA-006).

### Pending work, ranked

| Rank | Pending item | Requirement or decision | Evidence | Effort |
| --- | --- | --- | --- | --- |
| 1 | Run the build in Azure: Azure SQL driver and migration, real Blob, Entra sign-in, 2+ replicas, restart-persistence test. Today SQL is sqlite, Blob ran on a fake transport and `infra/` sets `minReplicas: 1` | ADR 0002 decisions 1, 2, 3, 6; DH-005 | README honest limits; `infra/modules/containerapps.bicep:124` | Large, needs Azure |
| 2 | CI gaps: image vulnerability scan, SBOM, SQL Server integration job, read-only root and dropped-capability checks. `mvp-ci.yml` has tests, non-root and no-data checks only | ADR 0002 decision 6; ADR 0001 open items | `.github/workflows/mvp-ci.yml` | Small |
| 3 | Ranking snapshot per run with an explicit as-of input, and the policy as a versioned file with owner, effective date and content hash. Today the policy is a Python constant and the owner is "to be named" | ADR 0002 decision 4; PR-006 | `mvp/zavaforward_mvp/ranking.py:18-34` | Medium |
| 4 | AI evaluation measures: rank correlation, critical-miss count, citation validity, run-to-run variation, latency and cost. Only overlap is recorded, and the harness uses a scripted model | ADR 0002 decision 4; FR-027, FR-028; OD-34 | `mvp/zavaforward_mvp/store.py:540`; no matches in `ai_eval.py` | Medium |
| 5 | Source citations on every AI output (FR-027) and a workflow-only comparison record for each AI task (FR-028) | FR-027, FR-028, AC-029, AC-030 | No citation code found in `mvp/` | Medium |
| 6 | Quality acceptance, defects, reinspection and handover (FR-017); budget, invoice match and grant ledger (FR-018, FR-019); procurement and capacity board (FR-016); resident decision per measure with versions (FR-014); technical sign-offs (FR-013) | PRD workflows 2 to 8 | No matches for defect, reinspect, budget, capacity or work order | Large |
| 7 | Coordinator insight: funnel, event timeline, forecast with uncertainty, stakeholder export with as-of date (FR-021 to FR-024) | FR-021 to FR-024, GOAL-003 | No matches for funnel, forecast or timeline; stats and map exist | Medium |
| 8 | Bulk update with preview and the forbidden-bulk-action rules; missed-appointment task (default 5, strict greater-than) | FR-006, FR-007, FR-031 | No matches for bulk or missed | Medium |
| 9 | Data-handling controls: retention job with owner approval and legal hold, request log for access and erasure, audit digests to immutable Blob with scheduled verification, per-year ledger table test | DH-003, DH-004, DH-005; ADR 0002 decisions 1, 2 | Digests are local files; no retention code | Medium |
| 10 | Screen reader and mobile accessibility run, copy audit for internal terms (SA-003), and the usability sessions with 5 to 8 users per role (SA-009) | NFR-001, SA-003, SA-009 | Browser check is desktop Chromium only, run by hand, not in CI | Medium; sessions need people |
| 11 | Remaining reads and writes on the SQL store: case detail, map, stats, visits, facets, export, closed list and writes still use the in-memory copy | ADR 0002 decision 1 | README SQL store limits | Medium |
| 12 | Time capture screens and an audited administrator enable action, document malware scan and content sniffing, redaction of free-text notes | ADR 0002 decisions 2, 7; PR-002 | README honest limits | Small to medium |

### Blocked on people, not code

These stay open however much is built: DPO confirmation of lawful basis,
Article 9 condition and Article 17(3) for audit data; Legal retention period;
named ranking policy owner and sign-off of the rule order; roles with a need to
see a vulnerability reason (OD-14, OD-19); contractor identity model and tenant
consent; live-scope homes out of about 60,000 (OD-17); licensed tile provider;
DPIA, staff notice and consultation for time capture (OD-36); model transfer
position for `uksouth` (DH-006, OQ-012). Real resident data stays blocked
(DH-002) until these close.

### Document consistency to fix

* ADR 0002 and the PRD still list slices A to C and offset paging as deviations
  in places; refresh the Implementation status table after the next slice.
* The PRD traceability has no FR-to-`mvp/` coverage column, so requirement and
  code cannot be compared without this review.

### Recommended order

Items 2, 3 and 4 first (small to medium, no Azure or approvals needed), then 5.
Item 1 needs the owner to authorise Azure work. Items 6 to 8 are the largest
product gaps against the PRD and should be scoped as separate branches. Item 10
sessions are the evidence the ADR calls its riskiest assumption.

### Status update (2026-10-09)

Items 1 to 6 above were built after this review and merged to main by PRs #40 to #45: CI hardening and SBOM (#40), ranking policy snapshots (#41), quality and procurement (#42), AI evaluation and citations (#43), finance, grants, sign-offs and resident decisions (#44), and the Azure SQL store with Blob and two replicas (#45). Entra built-in authentication (needs an app registration by the owner), a Bicep module for the MVP app, an Azure load test, the ledger retention and erasure question for the DPIA, and the unverified browser run of the new screens remain open. Status per item is in [ADR 0002](../../adrs/0002-pilot-readiness-architecture.md).
