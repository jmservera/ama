<!-- markdownlint-disable-file -->
# RPI Evidence Lane: Retrofit PoC Contract Coverage

## Delegation Contract

| Field | Value |
| --- | --- |
| Cycle / wave | Cycle 1 / Wider |
| Lane type | Internal |
| Topic | Minimum credible transactional Proof of Concept (PoC) scope for the Proper Warm application |
| Research posture | Balanced |
| Parent primary artifact (not edited) | `.copilot-tracking/research/2026-10-07/retrofit-application-poc-research.md` |
| Lane artifact | `.copilot-tracking/research/subagents/2026-10-07/retrofit-poc-contract-lane.md` |
| Explicit stop condition | Stop when scoped contract evidence covers portfolio, contracts, authority, metrics, UX continuity, transitions, seeded demonstrations and failure scenarios. |
| Scope | The current PRD, prior prototype/research-plan context, and synthetic-pack README/data dictionary only. |
| Non-goals | Build code; choose a production architecture; inspect the synthetic generator or answer key; assert company authority or approve a design. |
| Wave evidence goal | Identify breadth of minimum transactional PoC capabilities and testable scenario candidates, including reusable prior-prototype material and material gaps. |

## Preflight and Research Actions

* Confirmed before this write that the lane path is below `.copilot-tracking/research/subagents/` and differs from the parent primary artifact.
* Read `docs/prds/proper-warm-retrofit-programme-demonstrator.md` (draft v0.7.0), the existing HTML prototype, the prior PRD-prototype research and plan, and the synthetic-pack README and data dictionary.
* Deliberately did **not** read any generator or answer-key material.
* No external sources were needed. No source contained instructions that altered this delegated scope.

## Factual Findings

### 1. Credible transactional boundary

| Question | Finding | Evidence / confidence |
| --- | --- | --- |
| What is the smallest coherent state boundary? | One versioned home case must link building, scheme/work package, resident-service, hazard, provider, quality and finance records; a building link cannot transfer a home gate. The API is the sole write path and programme state is authoritative. | `docs/prds/proper-warm-retrofit-programme-demonstrator.md:136-149,320-321,575-576`; High |
| What controls make it transactional rather than a clickable mock? | Controlled writes need server-enforced identity/action/field rules, deterministic evidence/authority gates, optimistic concurrency, audit creation, idempotency and fail-closed recovery. | `docs/prds/proper-warm-retrofit-programme-demonstrator.md:140-149,327-332,367-389`; High |
| Which authority must remain outside PoC state transition authority? | No live resident contact, supplier instruction, professional/safety approval, claim submission, payment, hazard-clock control or acceptance can be implied; a proposal may create a task/draft only. | `docs/prds/proper-warm-retrofit-programme-demonstrator.md:46-58,344-347,522-532,602-604`; High |

### 2. Workflow portfolio and coverage candidates

The full PoC portfolio has nine workflow representations: stock/prioritisation, technical readiness, resident service, procurement/capacity/release, hazard referral, quality/defects/handover, finance/grant, handoffs/orchestration, and portfolio insight. Every full-MVP workflow requires a screen/queue plus an exercise scenario; a prose-only/deferred label is insufficient.

| Coverage candidate (not approval) | Minimum transaction or safe block | PRD contract |
| --- | --- | --- |
| Stock conflict / eligibility | Create or review a candidate reconciliation item that retains two sourced values, validation status, resolution owner and an explicit unknown; no silent exclusion. | FR-012 / AC-015, AC-040: `docs/prds/proper-warm-retrofit-programme-demonstrator.md:331,589,614` |
| Technical readiness | Submit/return evidence against a design version; missing competent sign-off or evidence blocks transition and assigns a reviewer. | FR-013 / AC-016: `...:332,590` |
| Resident service and update continuity | Record a constructed service/decision item, scoped measure and independent update commitment; contact/access remains distinct from consent and a handoff cannot silently clear the update. | FR-014, FR-033 / AC-017, AC-035, AC-037: `...:333,352,591,609,611` |
| Hazard referral and hold | Record source/awareness, sent referral, unconfirmed receipt/acceptance, owner follow-up and a read-only linked hold; reject any UI release/clock/classification action. | FR-015 / AC-018, AC-038: `...:334,592,612` |
| Procurement/capacity | Record a draft package with scope/version, offered versus committed capacity, unmet prerequisites and next reviewer; block instruction/booking. | FR-016 / AC-019, AC-039: `...:335,593,613` |
| Quality/handover | Receive evidence, create return/remediation/reinspection work, and prevent provider self-acceptance or handover/payment progression. | FR-017 / AC-020, AC-042: `...:336,594,616` |
| Invoice and grant separation | Stage an invoice match exception with source lines, authorised scope, budget and accepted-milestone comparison; no payment. Keep grant states distinct. | FR-018–019 / AC-021–022, AC-042: `...:337-338,595-596,616` |
| Cross-team orchestration | Send, receive, accept, reject/return, escalate and complete a handoff while retaining current owner, destination, receiver, chase owner, reason and next action separately. | FR-009–011 / AC-012–014, AC-036: `...:328-330,586-588,610` |
| Portfolio metrics | Render filter/as-of-aware heatmap/funnel/history/forecast views only from declared records, with denominator, filter effect, data coverage and uncertainty; otherwise visibly label a separate illustrative cohort. | FR-020–024 / AC-023–027, AC-041: `...:339-343,597-601,615` |

### 3. Actor-authority and UX-continuity contract

* The PRD names eleven provisional staff workspaces; perspective selection is not authentication. Residents are affected stakeholders rather than non-production-MVP users. `docs/prds/proper-warm-retrofit-programme-demonstrator.md:215-231`.
* The PoC must show field/action permission enforcement independently of the selected view. `docs/prds/proper-warm-retrofit-programme-demonstrator.md:322,578-579`.
* Minimum continuity contract: visible current owner versus destination/proposed/confirmed receiver/chase owner, explicit unknowns, sent/received/accepted separation, return reason/source, and retained history. `docs/prds/proper-warm-retrofit-programme-demonstrator.md:330,588,610`.
* Queue scope must disclose perspective, workflow, query and all-cases precedence; reset returns the versioned default selection without changing records. `docs/prds/proper-warm-retrofit-programme-demonstrator.md:351,608,771-798`.
* The PRD defines a bounded lifecycle and return path; material return preserves history and sends only affected approvals for reassessment. `docs/prds/proper-warm-retrofit-programme-demonstrator.md:537-571,584-587`.

### 4. Seeded demonstration and failure candidates

| Candidate | What it demonstrates | Provenance |
| --- | --- | --- |
| `EX-HOME-646` conflict | Two values/provenance, unresolved eligibility and owner-based reconciliation. | Existing fixture: `.copilot-tracking/prototypes/2026-10-06/proper-warm-retrofit-workbench.html:849`; contract: `docs/prds/proper-warm-retrofit-programme-demonstrator.md:614` |
| `EX-HOME-104` technical gap | Missing design reference prevents readiness; return to competent reviewer. | `.copilot-tracking/prototypes/2026-10-06/proper-warm-retrofit-workbench.html:844`; `docs/prds/proper-warm-retrofit-programme-demonstrator.md:590` |
| `EX-HOME-208` resident scope | Scoped decision/access unknown and update owner; no inferred consent. | `.copilot-tracking/prototypes/2026-10-06/proper-warm-retrofit-workbench.html:845`; `docs/prds/proper-warm-retrofit-programme-demonstrator.md:591,609,611` |
| `EX-HOME-531` hazard | Sent referral versus unconfirmed receipt/acceptance, linked hold, and prohibited hazard release control. | `.copilot-tracking/prototypes/2026-10-06/proper-warm-retrofit-workbench.html:848`; `docs/prds/proper-warm-retrofit-programme-demonstrator.md:592,612` |
| `EX-HOME-317` capacity | Offered capacity and building dependency, but no instruction. | `.copilot-tracking/prototypes/2026-10-06/proper-warm-retrofit-workbench.html:846`; `docs/prds/proper-warm-retrofit-programme-demonstrator.md:593,613` |
| `EX-HOME-422` quality | Incomplete pack, return/reinspection owner, no acceptance. | `.copilot-tracking/prototypes/2026-10-06/proper-warm-retrofit-workbench.html:847`; `docs/prds/proper-warm-retrofit-programme-demonstrator.md:594,616` |
| `EX-HOME-752` finance | Quantity match exception and payment hold. | `.copilot-tracking/prototypes/2026-10-06/proper-warm-retrofit-workbench.html:850`; `docs/prds/proper-warm-retrofit-programme-demonstrator.md:595,616` |
| `EX-HOME-863` handoff | Return with unknown reason/receiver; no committed transition. | `.copilot-tracking/prototypes/2026-10-06/proper-warm-retrofit-workbench.html:851`; `docs/prds/proper-warm-retrofit-programme-demonstrator.md:610` |
| Missing/invalid workbook row | Quarantine without partial commit; owner-visible disposition and lineage. | `docs/prds/proper-warm-retrofit-programme-demonstrator.md:145,348,605` |
| AI/service/state failure | Typed/cited proposal failure falls back to owned workflow-only work; state store/orchestrator failure prevents duplicate or unrecorded transition. | `docs/prds/proper-warm-retrofit-programme-demonstrator.md:142-149,604` |
| Missed appointment threshold | Exercise-only counter uses confirmed resident no-access, strictly greater than configured threshold, excludes no-shows/cancellations/reschedules and does not delay hazard response. | `docs/prds/proper-warm-retrofit-programme-demonstrator.md:350,607` |

### 5. Synthetic-pack suitability

The pack supports credible seeded transactions without real data: `candidate_id` joins lifecycle, contacts, appointments, quality, finance and issues; it deliberately includes duplicate/mistyped references, mixed dates, missing events and stale statuses. Relevant evidence tables include lifecycle events, safety holds, quality evidence and grant/finance. These imperfections should be surfaced as validation/exception paths rather than corrected silently.

* `docs/reference/research/retrofit-synthetic-data/README.md:106-123,130-137`
* `docs/reference/research/retrofit-synthetic-data/data-dictionary.md:19-23,31,60-77,93-143`

## Existing Prototype: Reuse Feasibility and Material Gaps

### Reusable, with confidence

The self-contained HTML is usable as a **visual interaction and fixture-seeding reference**, not as a transactional base: it already carries eleven role perspectives, nine workflow cards, eight named constructed fixtures, case selection, profile/workflow/search/all-cases filtering, live announcements and non-production/authority labels.

* Profile/workflow/case fixtures: `.copilot-tracking/prototypes/2026-10-06/proper-warm-retrofit-workbench.html:817-851`.
* Filtering and queue rendering: `...:908-956`.
* Case-specific detail/source/history and bounded suggestion copy: `...:957-988`.
* UI-only interactions: `...:992-1037`.

### Material gaps to preserve for parent synthesis

1. It has no persistent programme state, authoritative API write path, identity, server-side authorization, concurrency, audit event store or idempotent orchestration; all current interactions are in-browser filters/rendering. This fails the transactional component contracts.
2. It does not implement controlled state changes, handoff receipt/acceptance, returns/reopens, evidence versioning, field-level permissions, bulk preview/disposition, import quarantine, export, or recovery/failure state.
3. Metrics are fixed illustrative figures disconnected from the eight case fixtures; the portfolio workflow has no matching fixture. The PRD itself records this limitation. `docs/prds/proper-warm-retrofit-programme-demonstrator.md:196-208`.
4. It lacks the required manifest/reset contract and the Slice B/C connections: a connected exception-to-owner path, independent home gates for shared building work, and a linked same-home event sequence. `docs/prds/proper-warm-retrofit-programme-demonstrator.md:617,634-637,739-798`.
5. The current PRD is v0.7.0 while the HTML presents v0.6.2; reuse therefore requires traceability update rather than treating the HTML as conformant.

## Compact Evidence Relationships for Parent Synthesis

* **Shared case → transactional state boundary →** PRD FR-001/FR-002 and component contracts support a single versioned home/building/work-package model, while prohibiting inferred shared-home gates (`docs/prds/proper-warm-retrofit-programme-demonstrator.md:136-149,320-321,575-576`).
* **Nine workflow portfolio → minimum end-to-end scenario suite →** workflow coverage table and full-MVP rule support 9/9 represented paths with safe endpoints, rather than nine navigational labels (`...:292-308,739-798`).
* **Actor views → no implied authority →** provisional role list and FR-003/AC-004 support contextual screens but require service enforcement (`...:215-231,322,578-579`).
* **Metrics → reconcile-or-label rule →** FR-020–024/AC-023–027/AC-041 support drillable, denominator-aware metrics and weaken reuse of the HTML's fixed snapshot (`...:339-343,597-601,615`).
* **Existing HTML → visual/fixture reuse only →** implementation is explicitly client-rendered sample interaction (`.copilot-tracking/prototypes/2026-10-06/proper-warm-retrofit-workbench.html:908-1037`), which leaves the API/state/audit contract unresolved.
* **Synthetic data → credible failure seeds →** identifier joins and documented data defects support import/reconciliation/exception scenarios without using real data (`docs/reference/research/retrofit-synthetic-data/README.md:123,130-137`; `docs/reference/research/retrofit-synthetic-data/data-dictionary.md:19-31,60-77`).

## Gaps and Stop Decision

* **Unresolved evidence:** Named product owner, actual role/field permissions, source-system authorities, lifecycle/event dictionary, contract/payment rules, approved metric definitions and accessibility/user validation remain PRD open questions. They preclude production claims but do not prevent constructed PoC candidates. `docs/prds/proper-warm-retrofit-programme-demonstrator.md:932-947`.
* **Conflict:** The prior HTML labels PRD v0.6.2; current PRD is v0.7.0. The current PRD documents its own known prototype shortcomings rather than resolving them (`docs/prds/proper-warm-retrofit-programme-demonstrator.md:196-208`).
* **Stop decision:** Scoped contract evidence is covered; source review saturated under the stated internal, research-only boundary. No architecture selection or implementation recommendation is made by this lane.

