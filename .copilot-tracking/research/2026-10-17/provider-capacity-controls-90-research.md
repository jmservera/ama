<!-- markdownlint-disable-file -->
## Research Brief

* Task: #90, provider-capacity-controls-90, 2026-10-17.
* Purpose: prepare surgical implementation and explicit acceptance evidence for the four issue criteria.
* Audience: delivery coordinator and named human contract managers.
* Output mode: convergence, prepares planning.
* Posture: focused, selected from exact caller scope and named source contracts.
* Evidence root: `.copilot-tracking/research/2026-10-17/`.
* Scope: migrated procurement, work orders, controller and JSON/SQL API behavior.
* Criteria: evidenced committed (not offered) capacity; immutable change versions and issuer; drafts never instructions; contractors read only their own orders.
* Boundaries: no private datasets, live orders, financial commitments, cloud, paid inference, framework/service or MVP changes; preserve #78 provenance and #97 forms.

## Research Parameters and Direction Controls

Existing delivery is a claim to verify, not a reason to rewrite. Inspect prior art first. Unknown capacity fails closed. Named authorized contract managers alone issue; human, resident and contractor rights remain intact. Owner explicitly requested the full ordered loop, publication to a main-targeting PR and stop after push.

## Extension Registry and Provenance

Repository `.github/copilot-instructions.md` selected for all paths. RPI research selected with inline wider/deeper/contrarian waves. Manager role review is a research instrument, not actual company permission. Backend-only work is exempt from web skills unless evidence establishes a necessary UI change. No external research needed for internal executable contracts.

## User Participation and Research Decisions

No intake question: exact scope, branch, source references and limits supplied. Branch is clean `feat/provider-capacity-controls-90`, at fetched latest main `adedf1f`; no open matching PR. Issue #89 is parent hierarchy and #90 explicitly has no dependencies.

## Candidate Research Areas and Questions

1. What do PRD FR-016 and BRD FR-016/RULE-007/008 require?
2. Where are capacity, issuance, versioning and provider reads enforced across JSON and SQL?
3. Can alternate controller/API paths bypass those guards or lose concurrent updates?
4. Which smallest fixture tests prove exact thresholds and immutable failures?

## Research Cycle Log

### Cycle 1, Wave 1: Wider

Read exact issue #90 and parent #89, original/addendum, index/memory, sector primer, core/API guides and source FR-016/RULE-007/008. Inventoried migrated procurement, controller, AI proposals and SQL document helpers. Reflection: existing UI/API and quota counting are valuable prior art, but broad roles and free-text evidence are not the exact source contract.

### Cycle 1, Wave 2: Deeper

Traced every procurement transition, contractor projection, SQL `_SyncLock`, checked documents, safety/resident transactional revalidation, named-actor prior art and case `advance`. Independent manager research is in `subagents/2026-10-17/provider-capacity-controls-90-manager.md`; no actual approval was supplied or implied. Reflection: retain one checked procurement document and current locks; explicitly bind evidence and authority rather than create a service or fake company approval.

### Cycle 1, Wave 3: Contrarian

Challenged the apparent passing capacity/version tests: numeric committed capacity with absent evidence in imported records still issues; booking ignores the package/evidence interval; rescope leaves old capacity usable; appointment/completion/withdrawal change orders without versions; case `advance` can mark Install booked without any order. SQL document CAS already prevents two successful competing quota writes, so replacing storage is rejected. Own-contractor HTTP permission matrix exists; direct package reads lack that guard. AI proposals already cannot invoke domain writes; explicit draft marker still needs to be carried by template drafts.

Reflection: baseline 21 quality/procurement tests pass after restoring missing packages to the task-owned `.venv`; this disproves sufficiency of the old test suite, not presence of the missing controls. Docker 29.9.0 and the standard SQL Server 2022 image are locally available. No external legal claim is needed.

### Parent Synthesis and Re-entry

Accept C1-C7 and manager boundary as engineering evidence. Reject rewrite and role-agent approval. Require failing-first tests for exact missing behaviors, then preserve existing resident/safety/finance controls. One complete focused cycle covers the coupled trace; no unresolved research question requires another cycle.

## Evidence Log

| ID | Finding | Location | Confidence |
| --- | --- | --- | --- |
| C1 | Exact versioned provider-package/source criteria; source BRD FR-016 is exception control, not the same numbering as PRD FR-016 | `docs/prds/zava-forward-retrofit-programme-demonstrator.md:851`; `docs/brds/agentic-retrofit-programme-brd.md:1436-1440` | High |
| C2 | Issue counts ACTIVE orders but trusts numeric imported capacity and broad manager roles | `src/core/src/zava_forward/core/procurement.py:49-144` | High |
| C3 | Only issue/reissue/correction create versions; booking/completion/withdrawal do not | `src/core/src/zava_forward/core/procurement.py:149-233` | High |
| C4 | Contractor order filtering exists; direct package reads lack guard | `src/core/src/zava_forward/core/procurement.py:255-278`; `src/api/tests/test_role_matrix.py:120-145` | High |
| C5 | Alternate case advance creates Install booked without capacity/order validation | `src/core/src/zava_forward/core/store.py:514-528` | High |
| C6 | Checked-document CAS, writer transaction and dependent safety/resident revalidation are reusable | `src/core/src/zava_forward/core/sqlstore.py:468-659` | High |
| C7 | Fresh actor and failed-operation restoration prior art; draft review never executes domain actions | `src/core/src/zava_forward/core/change_provenance.py:15-132`; `src/core/src/zava_forward/core/assistants.py:1-5`; `src/core/src/zava_forward/core/store.py:530-548` | High |

No external sources used for domain claims. Fresh web guidelines retrieved on 2026-10-17 solely because structured capacity inputs require a narrow existing-screen continuation; Fluent 2/content/WCAG baseline read. No redesign authorized.

## Findings Mapped to Questions and Evidence

Q1: C1 establishes exact authority and capacity contract. Q2: C2-C4 show concrete missing enforcement. Q3: C5-C7 identify alternate path and existing transaction helpers. Q4: tiny JSON/SQLite fixtures and opt-in local SQL Server adapter can exercise exact quota, version, rollback, authority and own-order behavior.

## Alternatives and Decision State

Selected: surgical procurement guards and immutable event snapshots, structured evidence on the current endpoint/screen, explicit contract-scoped delegation in trusted staff records, fresh named identity checks, current-order capacity validation on advance and SQL transaction recheck. No API grants delegations. Existing unstructured/imported evidence remains visible but cannot authorize new work. One unit is one home order for the package-period quota, never crews/week. Actual reduction records a deficit and blocks new progression, rather than falsely retaining the previous commitment. Rejected: broad role as delegation, offered capacity, a source string as proof, adding tables/services, fabricated company approval, and UI-only guards.

## Open Questions, Risks and Residual Uncertainty

Actual company delegations and live capacity are unavailable and must never be inferred from fixtures.

## Planning Readiness

Ready. Research disposition: executed, complete. Handoff: C1-C7 and manager report; no engineering blocker. Operational permission, actual evidence and human approval remain unknown and fail closed, not a blocker to fictional local tests.
