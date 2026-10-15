---
title: Independent final-candidate plan critique for issue 75
ms.date: 2026-10-15
---

## Metadata

* Task ID: 75 / shared-systems-75
* Critique date: 2026-10-15
* Plan: .copilot-tracking/plans/2026-10-15/shared-systems-75-plan.md
* Phase details: .copilot-tracking/details/2026-10-15/shared-systems-75-phase-details.md
* Critique execution status: Complete
* Assessment: One independent final-candidate critique; no nested agents.

## Inputs and Criterion Boundary

* Caller requirements: src-only executable changes; no .env, .vscode or
  .copilot-tracking/github-issues access; SQL Server portable additions;
  independent human gates; synthetic-only data; retained existing AI paths;
  local suites, ruff, mypy and synthetic HTTP smoke; topic PR with Refs #75.
* Supplied research: .copilot-tracking/research/2026-10-15/shared-systems-75-research.md,
  particularly C3 to C8, W1 and the explicit-scope decision.
* Requirements assessed: issue criteria as recorded in W1; PRD FR-002 and
  AC-001/002/003, with AC-043 used only to check honest slice claims.
* Decisions assessed: core model/API view separation, checked-document storage,
  staff-only read views, Finance-view cost restriction, no inferred allocation,
  no imported approval authority, fail-closed unknown scope, no release/editor
  workflow and no hazard-response obstruction.
* Focused code evidence: Store initialization/detail/advance; SqlStore
  initialization, _seed, _sync, save and DOCS helpers; MssqlStore dialect hooks;
  projection role lists/redaction; procurement issue/reissue; quality's
  home-specific records. Project context and component README guidance were
  also consulted.
* Boundary: planning credibility, not implementation acceptance. No production
  code, plan, details or research was changed. No live services, private data,
  forbidden configuration paths or external research were used.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| FR-002 / W1: five shared categories with provenance | Covered | P01-T01 names schema, version, IDs, sources and exact money; P01-T02 names all categories and unknown states. |
| AC-001: home/building navigation and distinct financial context | Partial | Navigation is explicit, but P01-T02 prohibits building-view costs while requiring their Finance projection; PC-002. |
| AC-002 / C7: affected homes/scopes, independent gates | Partial | Shared-ID inference is rejected, but only case-level affects lists are specified; PC-001. |
| AC-003: independent decisions, approvals and evidence | Partial | Good two-home fixture intent; independent negative assertions for each gate family remain unspecified; PC-004. |
| C3/C4/C5: Store, SqlStore, inherited MssqlStore | Partial | Checked documents are a credible portable seam; legacy database behavior and mandatory local backend coverage need definition; PC-003. |
| C6: staff authorization and Finance-view restriction | Partial | Correct role boundary and home allocation restriction; conflicting building cost instruction and missing explicit field-level expectations; PC-002. |
| Read-only source-backed model | Covered | Required provenance, read isolation and no building mutations or approval/release endpoints are explicit. |
| Synthetic-only, human/resident gates, retained AI | Covered | Existing AI remains proposal-only; no new model authority or shared free-text financial prompt input is proposed. |
| P02-T01: local validation and evidence limits | Partial | All five suites, ruff/format/mypy, JS, HTTP smoke, migration and Docker probe are named; backend and gate assertions need tightening under PC-003/004. |
| P02-T02: documentation and PR delivery | Covered | Component READMEs, knowledge index/log, review, privacy-safe commit identity, topic push, main PR and Refs #75 are explicit; no merge/deployment authorized. |
| AC-043 / slice honesty | Covered for this boundary | The plan does not claim complete PRD acceptance, live SQL Server, Azure, model or human UX evidence from local tests. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 2 High, 2 Medium, 0 Low.
* Rationale: The architecture and authority boundaries are credible. Four
  bounded planner corrections are needed so implementation does not invent
  package applicability, suppress authorized financial context, overlook
  existing-store behavior or under-prove independent home gates.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Case-only affects lists do not define package or work-scope applicability

* Related IDs: FR-002, AC-002, research C7/C8, P01-T01, P02-T01.
* Evidence: The plan Functional Requirements says affects lists name exact
  cases; details P01-T01 requires per-record applicability but does not define
  its scope keys. PRD FR-002 expressly says a shared building ID cannot
  establish package applicability; AC-002 requires only affected homes/scopes
  to be blocked. In src/core/src/zava_forward/core/procurement.py,
  issue_work_order receives pid, case_id and scope, and reissue_work_order
  receives a work order and replacement scope.
* Concern: Explicit case membership fixes sibling inference, but does not
  establish whether a hold/dependency relates to the proposed package or
  work scope for that case. The candidate leaves the instruction checker to
  infer that relationship or block every instruction for an affected home.
* Impact: Unrelated work can be blocked, or an unproven package association
  can be treated as applicable. Neither is supported by AC-002.
* Smallest useful change: Specify the explicit applicability contract and
  its matching rules for detail readiness, advance, issue and reissue. Use
  explicit package/scope identifiers where those distinctions are represented;
  never derive them from building membership or free-text similarity.
  Define known-empty, missing and invalid scope separately, including the
  conservative unknown result. Do not introduce an allocation policy or
  a package-management workflow.
* Action owner: Planning parent.
* Exact resolving evidence: Revised P01-T01 defines applicability fields,
  reference validation and matcher inputs; P02-T01 requires same-building
  sibling independence and same-home different-package/scope tests, including
  reissue to a different scope, explicit non-applicability and unknown scope.
* Decision route: Direct planner correction; explicit-scope user direction
  already excludes shared-ID inference. No user response required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Building cost display is simultaneously required and prohibited

* Related IDs: FR-002, AC-001, research C6, P01-T02, P02-T01.
* Evidence: The plan requires a record containing GBP costs, all five
  shared-context categories and Finance-only visibility. Details P01-T02
  then says not to expose "costs in building view", immediately followed by
  applying existing Finance-view roles to building costs. In
  src/core/src/zava_forward/core/projection.py, FINANCE_VIEW lists the existing
  roles; redact_staff_detail removes finance and grants but currently has no
  cost_allocation rule.
* Concern: An implementer can comply with one sentence by omitting all
  building costs, or comply with the category requirement without a clear
  server-side cost projection. Endpoint role tests alone do not prove field
  restriction. The home allocation change also needs an explicit assertion,
  not reliance on existing finance/grants redaction.
* Impact: Authorized Finance users may lose required shared-cost context,
  or non-Finance responses can disclose newly introduced financial fields.
* Smallest useful change: Resolve the sentence to permit building-level
  costs only to FINANCE_VIEW roles while always excluding individual home
  allocations from the building response. Define non-Finance API omission
  and UI restricted-state behavior, plus home cost_allocation omission.
  Keep exact GBP representation and no inferred allocation/double counting.
* Action owner: Planning parent.
* Exact resolving evidence: Consistent P01-T02 projection contract and
  P02-T01 response-body assertions for Finance and non-Finance staff,
  contractor and unknown roles; authorized building costs remain visible,
  home allocations remain home-only, and unauthorized amounts are absent
  from serialized API responses, not merely hidden by the UI.
* Decision route: Direct planner correction; Finance visibility is already
  decided. No new role or user decision is needed.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Checked-document adoption leaves existing-database behavior and local persistence coverage optional

* Related IDs: Research C3/C4/C5, P01-T01, P02-T01, SQL Server portability.
* Evidence: Details P01-T01 selects SqlStore.DOCS; P02-T01 says "Test both
  stores where practical" without naming mandatory backends. In
  src/core/src/zava_forward/core/sqlstore.py, _seed imports DOCS only when
  cases is empty. Adding buildings to DOCS therefore does not import it
  from a changed seed into an already populated database. _proc_sync and
  _proc_write use the inherited checked-document contract; JSON Store uses
  live.json precedence in src/core/src/zava_forward/core/store.py.
* Concern: A successful fresh-seed SQLite restart does not establish how
  an existing JSON live file or populated SQL database behaves when building
  data is absent. Nor does optional testing establish that both local
  persistence implementations retain the new document and explicit links.
* Impact: Existing deployments may show unexplained missing context, or a
  future implementation may reset/reseed data to obtain the demonstration.
  SQLite-only success would not prove the JSON Store path.
* Smallest useful change: Make JSON Store and SQLite SqlStore fresh-load,
  read-isolation and reopen checks mandatory. Specify the non-destructive
  legacy-store behavior: absent document/linked missing record is explicitly
  unknown and cannot become a clear gate; no automatic reset or silent seed
  overwrite. If import into existing stores is deferred, document that limit
  rather than inventing an editor. Keep MssqlStore portability inspection
  explicit and real SQL Server evidence separately deferred.
* Action owner: Planning parent.
* Exact resolving evidence: P01-T01 records legacy-store semantics; P02-T01
  names both mandatory local backends and a pre-existing populated database
  case with preserved home state, plus reopen assertions for provenance,
  scope and amounts. Details retain DOCS/dialect-hook reuse with no new SQL
  syntax or DDL and no claim that a mock proves live SQL Server.
* Decision route: Direct planner correction; no new deployment or migration
  authority is required.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Separate fixture states do not yet prove each independent home gate remains effective

* Related IDs: AC-002, AC-003, P01-T01, P02-T01, independent human gates.
* Evidence: P02-T01 names separate consent, technical, funding, quality and
  closure state, but compresses expected behavior into "Prove no copied
  approvals". Store.gate_reasons/advance in
  src/core/src/zava_forward/core/store.py enforce resident, funding, hazard
  and technical checks; quality has separate per-case records and mutation
  methods in src/core/src/zava_forward/core/quality.py. P01-T01 adds building
  checks at detail, advance and instruction paths.
* Concern: Different initial fixture values and read-isolation assertions
  can pass even if a clear shared record accidentally replaces a home gate,
  or if reading shared context changes quality/closure state. A new shared
  blocker test alone does not test the inverse: shared readiness must not
  authorize a home.
* Impact: The issue's central no-inherited-approval regression can be
  under-tested despite all acceptance boxes appearing covered.
* Smallest useful change: Add an explicit expected-outcome matrix using
  the same two-home fixture: building clear plus one missing home gate;
  sibling approval present plus target approval absent; home clear plus
  applicable shared blocker; unrelated sibling/scope unaffected. Verify
  quality and closure remain separate using existing home workflow rules,
  without inventing new approvals or broadening this slice.
* Action owner: Planning parent.
* Exact resolving evidence: P02-T01 requires assertions for resident,
  technical, funding, quality, closure and evidence isolation individually;
  blocked advance/issue/reissue operations leave home state, work-order
  versions and approvals unchanged; read operations do not alter either
  home's records. Existing hazard intake remains available during shared
  holds. These cases can fit the already authorized test modules/helper.
* Decision route: Direct planner correction; human-gate independence is
  already required. No user response required.

## Strengths and Residual Risk

* Core ownership, API ownership and inherited checked-document persistence
  avoid workload imports and new dialect-specific storage.
* Read-only source-backed records, explicit unknowns, no building approval
  or hold-release API, home-only evidence/allocation and Finance-role reuse
  are appropriate boundaries.
* Existing AI remains enabled only through its existing proposal/human gates.
  No new AI task, deployment or model authority is proposed.
* Synthetic fixtures, local command recording and honest real-platform/human
  evidence limits are explicit. They must remain limits after implementation.
* The fixed test-module budget is not itself a defect; use table-driven
  cases within it rather than adding a new test framework.

## Questions or Blocking Evidence Gaps

* None requiring owner input for this bounded model/view slice. All four
  findings can be resolved from confirmed direction by the planning parent.
* The BRD FR-002 reference discrepancy is already disclosed in research;
  correcting the approved source document is outside this task.

## Limitations

* This is a read-only planning assessment, not test execution or proof that
  implementation meets the requirements.
* Issue text was assessed through supplied research W1, not a fresh external
  retrieval. No independent regulatory or company operating claims are made.
* Real building registers, live SQL Server, Azure deployment, real inference
  and human UX acceptance were not tested and are not prerequisites for
  accepting this explicitly local synthetic slice.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Define explicit applicability matching and revise
  the financial projection, persistence and gate-test contracts in place.
* User response required: No.
* Return this complete finding set to the active parent; revise directly
  and reconcile every PC ID without another independent critique pass.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-15/shared-systems-75-plan.md](.copilot-tracking/plans/2026-10-15/shared-systems-75-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-15/shared-systems-75-phase-details.md](.copilot-tracking/details/2026-10-15/shared-systems-75-phase-details.md) | Assessed task contracts |
| [.copilot-tracking/research/2026-10-15/shared-systems-75-research.md](.copilot-tracking/research/2026-10-15/shared-systems-75-research.md) | Supplied evidence and decisions |
| [.copilot-tracking/plans/2026-10-15/shared-systems-75-critique.md](.copilot-tracking/plans/2026-10-15/shared-systems-75-critique.md) | Complete independent finding set |

## Next Steps

The active planning parent should resolve PC-001 through PC-004 in the plan
and phase details, record their dispositions, and finalize planning without
another critique. No user action is required. This critique stops here;
implementation, production edits and publication remain with the parent.
