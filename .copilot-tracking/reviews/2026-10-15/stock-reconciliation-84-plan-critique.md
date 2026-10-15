---
title: Issue 84 final-candidate plan critique
description: Independent bounded assessment of stock reconciliation planning readiness
ms.date: 2026-10-15
---

## Metadata

* Task ID: 84; stock-reconciliation-84.
* Critique date: 2026-10-15.
* Branch: feat/src-stock-reconciliation-84.
* Plan: .copilot-tracking/plans/2026-10-15/stock-reconciliation-84-plan.md.
* Phase details: .copilot-tracking/details/2026-10-15/stock-reconciliation-84-phase-details.md.
* Critique execution status: Complete.
* Assessment count: exactly one independent final-candidate critique. No delegation, implementation, test execution or source revision.

## Inputs and Criterion Boundary

* Read the supplied plan, details and .copilot-tracking/research/2026-10-15/stock-reconciliation-84-research.md, plus the original/addendum case study, reference index/memory and sector primer.
* Retrieved issue #84 body and comments with gh on 2026-10-15. The issue is open, names four acceptance criteria and declares no dependencies. Its owner comment separates nomination/self-referral/challenge into #130 and tenure/lease routing into #131. Neither is a missing requirement for this slice.
* Checked Accepted ADR 0006, src/README.md, scoped core/API implementations and existing sign-off tests/configuration. Relevant PRD contracts are FR-012/013/034 and AC-015/016/040. These inform the selected slice, not a claim to implement every linked programme requirement.
* Caller controls prevail: all new code/tests in src; reuse sign-off/building/hazard/handoff controls; core imports no workload; agents acquire no SQL/blob dependency; API may import agents until #144; pip only; no private data or new mvp code; no new SQL dialect; AI stays proposal-capable with human approval/consent and never supplies technical approval.
* Test ownership is fixed: core semantic and JSON/SQL persistence tests; API HTTP/auth/projection tests. No removals; at most two new Python test modules and 24 new methods total. Findings below must fit that budget, using subtests/table-driven scenarios and existing regression coverage.
* Protected paths were not opened or changed: .env, .vscode and .copilot-tracking/github-issues. The sole write target is this critique.
* Existing untracked plan/details/research/session-state artifacts were present on arrival. The named branch matches the authorized workstream; gh returned no existing PR for it. They were left in place.
* Boundary: assess whether the plan credibly directs bounded engineering and honest evidence collection. Do not certify legal compliance, professional competence, production readiness, source authority, real AI benefit or live Azure SQL behavior.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Issue AC1; FR-012; AC-040; P01-T01/P02-T01 | Partial | Both source assertions, metadata, registered owner, retained history, staff projection and explicit Unknowns are planned. Conflict guard placement and rendered evidence need PC-003/004. |
| Issue AC2; FR-013; P01-T02 | Covered | Four existing role mappings, authenticated identities, different-person checks, versioned history and pre-mutation validation are retained. Competence is explicitly not attested. |
| Issue AC3; P01-T02/P02-T02 | Covered | Explicit affected-list validation and affected-only reassessment reuse signoffs.py; no parallel approval engine. |
| Issue AC4; research C7/C13; P01-T03 | Partial | Tri-state intent is correct, but consumer representation and existing-database refresh are unspecified: PC-001/002. |
| AC-015/016; research C12; P01-T01/P01-T02 | Partial | Hazard independence and building reuse are explicit. Existing no-technical-record branch needs an explicit conflict test/guard contract: PC-003. |
| ADR 0006; src dependency rule; P01/P02 | Covered | Scope stays in core/API, SQL uses existing Store persistence, no agent persistence or workload imports into core are proposed. |
| AI/consent/human authority; research selected direction | Covered | No AI resolver or technical approver is introduced. Existing governed AI remains available; full suites provide regression evidence, not real-model acceptance. |
| P02-T02; locked test ownership/budget | Covered | Core semantics versus API HTTP split, two-module/24-method ceiling and no removals are explicit. Add the missing scenarios within this ceiling. |
| P03-T01 | Partial | Targeted/full suites, ruff/mypy, Node checks, synthetic HTTP and Docker attempts are planned; static delivery alone cannot prove the view: PC-004. |
| P03-T02 | Covered | Core/API contracts, reference routing and append-only log update are scoped; memory/regulatory snapshots remain unchanged. |
| P03-T03 | Covered | One implementation review, privacy-safe identity, topic-only push, Refs #84 PR and no merge are explicit. |
| External/owner-dependent acceptance | Covered as unmet | Live Azure SQL/model evidence, competence/delegation and direct human acceptance are not available locally and must remain unticked. |

## Verdict

* Verdict: Revise.
* Severity summary: 0 Critical, 2 High, 2 Medium, 0 Low.
* Rationale: the selected feature boundary is credible, but the implementation contract leaves concrete missing-input and persisted-state inconsistencies possible. Correct the four findings directly before implementation. No new user decision is required and no second critique is requested.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Specify a consumer-safe Unknown support contract

* Related IDs: issue AC4, BRD AC-065, P01-T03, P02-T01/P02-T02; research C7/C13.
* Evidence: the details require a shared typed helper but do not define its returned representation, aggregation truth table or ranking encoding. src/core/src/zava_forward/core/ranking.py::_support is Boolean; sqlstore.py::_row casts it to int. projection.py::redact_staff_detail directly indexes adjustment and maps any value other than "None" to "Extra support noted". insights.py::stats sums priority_support directly. src/api/src/zava_forward/api/web/app.js uses truthiness for support flags and displays adjustment directly. store.py::_facts and ai_tasks.py also consume support inputs.
* Concern: missing keys/nulls can still raise, render blank, be redacted into an asserted need, or become a truthy "Unknown" string. A tri-state helper alone does not settle how ranking, flags, counts, filters, contractor notice and AI facts interpret incomplete coverage. The plan does not define known-positive plus missing-input behavior or distinguish known negative from incomplete evidence at these boundaries.
* Impact: AC4 can fail outside the pure helper even if its tests pass; staff or proposal inputs can incorrectly assert either vulnerability or absence, while queues/counts disagree.
* Smallest useful change: add one support truth table and response contract to P01-T03/details. Separate observed positive evidence from incomplete coverage; specify known false/"None", missing/null and mixed-input cases. State the deterministic missing-input sort encoding without adding a weight or changing known-input policy order. Enumerate updates to existing core/API consumers, including redaction, summaries/statistics/visits, contractor notice and existing AI fact generation. Explicitly forbid truthiness conversion of a display label.
* Action owner: planning parent, then core/API implementer within the existing workload boundaries.
* Exact resolving evidence: revised details contain the truth table and field/encoding contract; planned table-driven core scenarios cover both absent/null permutations and mixed inputs, known-input ranking equivalence and incomplete-case inclusion. API-owned scenarios verify authorized/redacted detail and list outputs never mislabel Unknown as a known need or "None". Changes evidence records the exercised AI-fact path without claiming live inference.
* Decision route: direct planner correction. The caller already requires Unknown and unchanged known-input ranking; do not request a policy-weight decision.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Plan an idempotent refresh of existing SQL-derived support and rank keys

* Related IDs: P01-T03, P02-T02, P03-T01; research C5/C7/C13; issue AC4.
* Evidence: src/core/src/zava_forward/core/sqlstore.py::_migrate rebuilds derived columns only when CASE_COLS are absent or meta.rank_policy differs from the current policy version. _row persists support and rkey. Existing null adjustment is treated as support-positive by ranking._support. The plan preserves the known-input ranking policy and introduces no new schema, but specifies no alternative derived-data refresh trigger.
* Concern: correcting helper behavior does not refresh already stored support/rkey values when the policy version and columns are unchanged. A freshly seeded test database misses this upgrade path. Existing SQL lists/filtering/pagination may retain old inferred support and ordering while detail or in-memory snapshots use the new semantics.
* Impact: persistent SQL and JSON results can disagree after restart; homes may remain incorrectly prioritized or selected despite the corrected API detail.
* Smallest useful change: add a bounded, versioned/idempotent derived-data refresh task and regression scenario to P01-T03/P02-T02. Reuse existing persistence/dialect hooks and portable statements; distinguish an encoding/backfill revision from an invented business-policy change. Recompute support and rkey consistently without changing authoritative case assertions or resetting workflow/history.
* Action owner: planning parent and core persistence implementer.
* Exact resolving evidence: revised details name the refresh trigger and preserved state. A core-owned upgrade test creates a pre-change synthetic SQL database with current rank_policy/columns and a previously misderived null-support case, reopens it through the new path, and compares list/filter/order/cursors with JSON semantics. A second reopen proves idempotence; known-input order and case/audit history stay intact. Record that SQLite evidence is not SQL Server execution evidence.
* Decision route: direct planner correction; no new dialect, source-authority decision or user approval is needed.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Make unresolved-conflict gates independent of design-record existence

* Related IDs: P01-T01/P01-T02/P02-T02; FR-012/013; AC-015/016.
* Evidence: the details say the technical gate includes unresolved conflicts. src/core/src/zava_forward/core/signoffs.py::missing_items returns [] when technical is absent; technical_gate delegates to it. store.py::gate_reasons and advance reuse that gate. Existing test_finance_signoffs.py explicitly expects no technical missing items before design submission.
* Concern: simply adding conflict checks after the existing early return would leave newly reconciled homes without a technical record unheld. Existing fully signed homes receiving a later conflict are another essential entry state not named in the test plan.
* Impact: the promised owned conflict hold can be missing from detail/readiness or progression even while the comparison panel is visible.
* Smallest useful change: state that unresolved-comparison hold evaluation precedes or bypasses the no-technical-record return and is reused by progression and sign-off approval. Add the no-design and previously-signed entry states to the planned test matrix. Preserve records and unaffected sign-offs; do not invent conflict resolution or retrospectively erase approvals.
* Action owner: planning parent and core workflow implementer.
* Exact resolving evidence: revised P01/P02 details name these entry states. Core JSON/SQL scenarios show an owned blocker and refused advance with no design, refused new approval/progression after a conflict is appended to a signed case, retained approval history, and unaffected sibling/consent state. Hazard intake/referral still succeeds under the stock hold. Existing sign-off regressions remain in place.
* Decision route: direct planner correction. The plan already requires unresolved conflicts to block technical approval/progression but not hazard intake.

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: Add rendered-view evidence rather than treating static delivery as UI acceptance

* Related IDs: issue AC1/AC4, PRD AC-040, P02-T01/P02-T02/P03-T01.
* Evidence: P02-T01 promises a readable staff panel and Unknown states. P02-T02 verifies static app delivery; P03-T01 specifies Node syntax and synthetic HTTP. Neither specifies rendered inspection. Existing app.js support rendering uses truthiness/direct field display; AC-040 requires case-specific evidence when switching cases.
* Concern: valid JSON, a 200 asset response and syntax checks cannot establish that both values/source labels/owner are visible, Unknown is readable, or selecting another case clears stale evidence.
* Impact: the primary staff-view acceptance criterion can be claimed without exercising the view; UI regressions from the new support representation can escape the planned checks.
* Smallest useful change: add a synthetic rendered-view check using existing API browser tooling, or record its unavailable dependency/runtime as an unmet view-evidence gate. Exercise a conflict case, a distinct second case and incomplete support. Check both value/source/metadata groups, owner, Unknown labels, selection refresh and basic keyboard/heading access. Do not claim direct human usability acceptance.
* Action owner: planning parent and API implementer/evidence recorder.
* Exact resolving evidence: P03 details name the existing browser command or reproducible local inspection procedure and its assertions; the changes artifact records actual rendered outcomes and fixture IDs, or explicitly leaves view validation unmet if the runtime cannot execute. Keep Python HTTP tests API-owned and stay within two modules/24 methods; do not add a third Python module.
* Decision route: direct planner correction, not a new user-design decision.

## Strengths and Residual Risk

* Reuse of existing four-role sign-offs, affected-only returns, shared building blockers, hazard holds and home-specific consent is preferable to duplicating authority engines.
* Registered identities and validation before mutation address the researched provenance/empty-affects issues without pretending role membership proves professional competence.
* Source comparison is append-only and bounded to non-resident fields. No latest-wins merge, automatic resolution, eligibility pass or AI technical approval is proposed.
* Core/API ownership and the test ceiling are clear; full src regression checks preserve existing governed AI proposal capability and dependency restrictions.
* Follow-up source resolution, operational delegation and live platform/human acceptance are explicitly outside this bounded delivery. An unresolved hold remaining unresolved is not a reason to invent an approval route.

## Questions or Blocking Evidence Gaps

* No unresolved significant/divergent user choice blocks these planner corrections.
* Live SQL Server/Azure, real-model results, named professional competence/delegation and direct human acceptance remain unmet. Keep the plan's external acceptance item unchecked, use Refs #84 rather than claiming complete issue acceptance, and retain these limits in delivery evidence.

## Limitations

* This was a static plan assessment, not an implementation review or executable verification. No baseline tests, Docker builds, live services, private fixtures or browser were run.
* Research claims about merged PRs were read as supplied; current scoped src evidence independently establishes the reuse points and placement rules. No broad external research was performed.
* Existing tooling exemptions were observed, not expanded or graded as a separate repository cleanup. New helpers/tests must satisfy the caller's existing-tooling requirement.
* Plan, details and research were read only. Pre-write SHA-256 fingerprints, respectively: 37edfbd1f6330e1fa86c64d30610a6737705e87c4fc9e4a15b841c285a9a09c0; 86b963ebaa4d2de63d2c084a7c4904522e6227016384fac8d3cc943dbc1809bf; 37939af78ac315fbfa16f56d7647e744fe90a7a567183b59f995c2523e44d4b6.

## Recommended Next Action

* Highest-impact finding: PC-001, because incomplete support evidence crosses ranking, projection and staff/AI presentation boundaries.
* Action owner: active planning parent.
* Smallest next action: add the support truth table/consumer contract, then disposition PC-002 through PC-004 in the same plan/details revision with the exact resolution evidence above.
* User response required: no. All four findings are direct corrections under existing direction.
* After revision, the authorized parent may finalize and continue the full RPI loop; do not run another plan critique. This reviewer stops here without implementation or remote writes.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-15/stock-reconciliation-84-plan.md](.copilot-tracking/plans/2026-10-15/stock-reconciliation-84-plan.md) | Unchanged final-candidate plan assessed |
| [.copilot-tracking/details/2026-10-15/stock-reconciliation-84-phase-details.md](.copilot-tracking/details/2026-10-15/stock-reconciliation-84-phase-details.md) | Unchanged phase details assessed |
| [.copilot-tracking/research/2026-10-15/stock-reconciliation-84-research.md](.copilot-tracking/research/2026-10-15/stock-reconciliation-84-research.md) | Supplied scoped research |
| [.copilot-tracking/reviews/2026-10-15/stock-reconciliation-84-plan-critique.md](.copilot-tracking/reviews/2026-10-15/stock-reconciliation-84-plan-critique.md) | Complete single-pass finding set and handoff |

## Next Steps

The active planning parent should resolve PC-001 through PC-004 directly, record their dispositions and finalize without another critique. Continue implementation only after that revision; leave external/owner-dependent evidence unmet until actually obtained. No user action is required.
