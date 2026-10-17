<!-- markdownlint-disable-file -->
# RPI Plan Critique: Assessment reconciliation controls #84

## Metadata

* Task ID: 84
* Task slug: assessment-reconciliation-controls-84
* Critique date: 2026-10-17
* Plan: .copilot-tracking/plans/2026-10-17/assessment-reconciliation-controls-84-plan.md
* Phase details: .copilot-tracking/details/2026-10-17/assessment-reconciliation-controls-84-phase-details.md
* Critique execution status: Complete
* Critique execution: Exactly one final-candidate assessment; no child agents, source edits, tests, containers, publication or second critique.

## Inputs and Criterion Boundary

* Caller direction: full ordered RPI delivery followed by a normal push and main-targeted PR using Refs #84. This critique assesses that plan; it does not execute its implementation or publication phases.
* Exact issue criteria: both compared stock values and query owner; four separate versioned assessment/design/building/coordination sign-offs; design changes stale only affected sign-offs; ranking does not depend only on vulnerability and missing flags remain Unknown, never an assertion of none.
* Supplied research: .copilot-tracking/research/2026-10-17/assessment-reconciliation-controls-84-research.md, particularly C1-C7 and W1-W3. The reported 47 core tests and 18 API/ranking tests with one browser skip, revoked-role SQL probe and failed-save audit probe are supplied execution evidence, not reruns performed by this critique.
* Current implementation evidence: src/core/src/zava_forward/core/stock.py, signoffs.py, store.py, change_provenance.py, sqlstore.py, mssqlstore.py and the relevant commit/discard pattern in forms.py.
* Current test evidence: src/core/tests/test_stock_reconciliation.py; src/api/tests/test_stock_reconciliation_api.py test inventory; src/api/tests/test_mssqlstore.py and its opt-in factories/classes.
* Requirements and existing evidence boundaries: docs/prds/zava-forward-retrofit-programme-demonstrator.md FR-012/FR-013; docs/brds/agentic-retrofit-programme-brd.md FR-037/AC-065 and RULE-017; src/core/README.md stock-comparison/sign-off contract. Original case study, relevant addendum exercise context, reference index, memory and sector primer supplied project orientation, not new acceptance evidence.
* Dependencies: P01-T01 precedes P01-T02; P02 follows P01; P03 follows recorded P02 evidence. #81 is hierarchy only. #130 owns nomination by supplied owner direction. No procurement #90 or infrastructure/package #381 implementation is authorized.
* Locked scope: reuse change_provenance._actor, the existing SQL writer transaction and _discard through a bounded stock/technical decision context and minimal Store/SQL hook. Preserve current role mappings and independently approved authority/policy boundaries; do not infer operational competence, source authority or health.
* Locked test ownership: canonical core semantics in src/core/tests/test_stock_reconciliation.py, HTTP in src/api/tests/test_stock_reconciliation_api.py, SQL parity in src/api/tests/test_mssqlstore.py; at most 10 new core methods, 2 HTTP methods and 1 opt-in parity class, with no removals or generated targets.
* Assessment boundary: credibility and completeness of the supplied final candidate, not implemented correctness, fresh legal research, actual human approval, real-cloud acceptance, accessibility conformance or a broad repository audit.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Exact criterion 1; C1/C4; PRD FR-012 | Covered | Existing comparison test preserves left/right assertions, metadata and query owner across JSON/SQLite reopen; HTTP evidence is identified. No winning source or stock overwrite is proposed. |
| Exact criterion 2; C2; PRD FR-013 | Covered | Existing fixture uses four different signers; source enforces separate role mappings and no design self-approval. Planned strengthened version/history assertions are appropriate. This is an exercise mechanism, not competence certification. |
| Exact criterion 3; C2; P01-T01 | Covered | Existing explicit affected-set test preserves assessment/coordination and stales design/building; plan adds reopen/history and sibling assertions without broadening dependencies. |
| Exact criterion 4; C3; BRD FR-037/AC-065 subset | Covered | Existing truth table distinguishes explicit No from Unknown; independent safety and waiting factors and SQL ordering/upgrade assertions exist. Retaining the current nonpositive ranking bucket does not mean missing flags are recorded as none. Broader cohort/referral acceptance is explicitly separate. |
| C5/C7; P01-T01/T02 current authority | Covered | _actor reads the current SQL staff row rather than self.staff, compares identity including oid and returns a copy. Plan requires entry and transaction-time checks for all three entry points. |
| C5/C7; writer-lock race | Covered | SqlStore.save begins the writer transaction before existing validators; the same narrow hook can revalidate before writes. Existing independent-store query/terminal race tests already exercise competing changes. No generic lock rewrite is justified. |
| C6; P01-T01/T02 rollback/reopen | Covered | Plan explicitly requires case-write and audit-write failures, unchanged durable case/audit/sequence, reopen and no delayed flush by a later operation. _discard clears pending events and reloads touched cases. |
| C6/C7; scoped context lifecycle | Partial | Implementation intent says restore/clear context, but no required test proves restoration on every exit or lack of validation leakage into later saves; PC-002. |
| P02-T01; SQL Server parity | Partial | Existing harness does not run stock/technical reconciliation cases; the optional class must be explicitly bound to this change's regressions; PC-003. |
| P02-T02; documentation and evidence | Covered | Current component guides and conditional synthesis/index/append-log updates are scoped; changes artifact owns actual commands and timestamps. No memory, original case study or snapshot edits. |
| P03-T01/T02; review outcome and publication | Partial | One review and normal publication are clear, but routing all findings to future work lacks a blocking-defect disposition; PC-001. |
| Human approval, policy and operational acceptance | Covered | Plan retains unproved human delegation/competence, source policy, broader BRD acceptance and accessibility acceptance. No new user decision is needed to keep these boundaries. |
| Scope, overlap, test budget and sequencing | Covered | Explicit exclusions, surgical shared-file overlap, fail-before sequencing and fixed ownership/budget are credible. All findings below can be resolved without expanding them. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 1 High, 2 Medium, 0 Low.
* Rationale: the bounded root fix and four-criterion preservation are credible. The candidate needs an explicit blocking-review disposition and two concrete validation commitments before it can reliably claim completed delivery. These are compatible planner corrections, not reasons to redesign transactions, reopen policy decisions or run another critique.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Unconditional future-work routing can publish failed acceptance as completed delivery

* Related IDs: P03-T01, P03-T02, P02 acceptance evidence; all four exact criteria and C5/C6.
* Evidence: .copilot-tracking/details/2026-10-17/assessment-reconciliation-controls-84-phase-details.md:90-103 says to route findings to future work, not repeated review/implementation, and then publish. The plan requires review execution separate from outcome, but does not state what happens when that outcome identifies a broken required control.
* Concern: a single-review limit does not distinguish an accepted out-of-scope residual from an unresolved in-scope defect. As written, a reproduced revoked-actor bypass or success-audit leak could be deferred under the same rule as an unperformed human acceptance check.
* Impact: the lifecycle could complete and publish success-shaped criterion evidence despite a known failure of the very controls this continuation exists to establish.
* Smallest useful change: define P03 dispositions explicitly. Only accepted residuals outside the exact engineering boundary may be routed to future work. An unresolved in-scope blocking defect prevents a successful completion claim. Retain exactly one review: allow a bounded direct correction with targeted evidence if already authorized, or stop with the failed/blocked outcome clearly recorded. If the requested PR is still published for visibility, identify it as incomplete, not acceptance-ready. Do not introduce a review loop or automatically choose another backlog item.
* Action owner: planning parent for the gate wording; implementation/review owner for recording its eventual outcome.
* Exact resolving evidence: matching plan/details gate text states that failed exact criteria, current-authority denial or durable rollback/audit consistency cannot be deferred as accepted residuals; it specifies the bounded correction-or-incomplete-stop route and preserves the single review, normal main PR, Refs #84 and owner-only merge decision.
* Decision route: direct planner correction. Existing user direction already requires working controls and a single ordered lifecycle; no significant or divergent user decision is needed.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: Context restoration and original-error propagation have no explicit regression oracle

* Related IDs: P01-T01, P01-T02, P02-T01; C6/C7.
* Evidence: .copilot-tracking/details/2026-10-17/assessment-reconciliation-controls-84-phase-details.md:26-55 requires rollback/reopen tests and says "Always restore/clear context" without naming a lifecycle assertion. src/core/src/zava_forward/core/sqlstore.py stores pending/touched/validation data in thread-local state and _SyncLock calls _finish on outer exit. src/core/src/zava_forward/core/change_provenance.py uses finally cleanup but catches Exception; src/core/src/zava_forward/core/forms.py:_commit catches BaseException. The helper is an identity source to reuse, not proof that a new scope cleans up correctly.
* Concern: passing durable rollback tests alone would not prove that the new actor-validation context is absent/restored after success, entry rejection, body failure or save failure. A stale context can wrongly deny an unrelated later save; clearing a pre-existing context can erase its validation. A handler limited to Exception also leaves the plan's "any failure" promise untested for interruption-style exits. A cleanup failure can mask the original operation error unless precedence is deliberate.
* Impact: the narrow hook could alter unrelated workflows or fail to preserve the original exception, violating the no-expansion and failure-integrity requirements even when ordinary reopen assertions pass.
* Smallest useful change: add an explicit lifecycle/error-preservation matrix to the existing core regression owner using subtests or existing method extensions. Cover success, initial authority rejection, an in-scope body/validation error, ordinary SQL save failure and a synthetic BaseException interruption before commit. Check restoration of any pre-existing context, or absence when none existed; verify a subsequent legitimate stock action and an unrelated existing save do not consume the old actor or flush a failed success event. Require cleanup attempts not to replace the original operation failure; if cleanup itself cannot complete, report that uncertainty without claiming rollback succeeded. Keep changes inside the bounded decision context, not generic lock/save semantics.
* Action owner: planning parent to specify the oracle; core implementation/test owner to implement it in src/core/tests/test_stock_reconciliation.py.
* Exact resolving evidence: plan/details name this lifecycle matrix within the unchanged 10-method budget; implementation evidence later shows context state before/after each exit, original exception identity/type preserved on the cleanup-fault case, unchanged durable case/ledger/sequence for known precommit failures, and no stale validation or delayed success event on the next unrelated save. Do not label a post-commit acknowledgement failure as a proven rollback.
* Decision route: direct planner correction. No new framework, API, dependency, authority model or user decision is required.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Running the existing SQL Server harness does not by itself exercise the new decision scope

* Related IDs: P01-T01, P02-T01, locked SQL parity owner; C5-C7.
* Evidence: .copilot-tracking/plans/2026-10-17/assessment-reconciliation-controls-84-plan.md:138 makes the existing parity harness conditional on extension. Phase details:70-73 say local parity is feasible and prescribe container isolation, but do not identify which new decision cases must run there. src/api/tests/test_mssqlstore.py currently replays handoff, time, chat, generic store and read suites, not src/core/tests/test_stock_reconciliation.py. src/core/src/zava_forward/core/mssqlstore.py adapts BEGIN IMMEDIATE to a transaction-owned application lock and supplies different connection/error behavior.
* Concern: a green existing SQL Server suite could be reported as parity for this continuation without ever invoking the new stock/technical validation hook, fresh staff read or failed-decision cleanup. SQLite coverage remains valuable but does not establish those paths on the adapter.
* Impact: the planned local SQL Server validation can consume time while leaving the actual changed transaction path untested and its acceptance evidence ambiguous.
* Smallest useful change: explicitly allocate the permitted one opt-in parity class to bounded reuse of the canonical constructed fixture/regression logic. Require representative stock comparison, terminal disposition and technical-action success; stale registered actor denial plus a pre-save authority change from a second connection; and actual transactional case/audit failure with reopen/no-later-flush assertions. Use a scoped subset/subtests, not a second independently maintained semantic suite. If the cached-image run is unavailable, record exact Not run/Blocked cases and limit claims to SQLite rather than silently substituting generic suite results.
* Action owner: planning parent to pin the parity selection; SQL parity test owner in src/api/tests/test_mssqlstore.py to wire and execute it.
* Exact resolving evidence: revised plan/details name the selected cases, opt-in class/command, isolated throwaway-database safeguards and unchanged class budget. The changes artifact later records the specific executed test names/counts, rollback/reopen results and database/container cleanup, or the precise unavailable checks. Authority-race evidence must change the staff row independently without relying on a case-sequence bump. No real database, cloud call, image pull, package work or infrastructure edit is authorized.
* Decision route: direct planner correction within the already permitted parity class and local validation scope; no user response is required.

## Strengths and Residual Risk

* Source inspection supports the supplied C5/C6 explanation: technical_action and _stock_actor consult cached self.staff; _sync populates that cache only when empty. Generic save failures roll back SQL but leave pending success events available to _finish. The proposed local scope addresses these seams without changing generic behavior for other workflows.
* Fresh authority checks must run before mutation and again after acquiring the SQL writer transaction, before case/audit writes. The existing helpers and hook pattern support this; preserve two-store hazard/query and rowversion race tests. Do not replace a deterministic interleaving with a timing-dependent sleep.
* On known precommit case/audit failures, compare the durable case body, rowversion/change sequence, ledger contents and head after reopen, and verify the next successful action appends only its own events. Audit failure injection must reach the transactional write path, not merely raise before save. These are precise applications of the existing rollback requirements, not additional product scope.
* The SQL Server application lock coordinates participating store writers. This critique does not establish serialization against arbitrary external staff-table edits that bypass that protocol. Document the actual tested interleaving; do not turn this slice into an IAM or locking redesign.
* Reopen coverage should preserve all four sign-offs' original actor/version/history, increment only the intended design version, stale only selected dependencies and leave siblings unchanged. Failed decisions must not create a design version, terminal query event or success audit.
* JSON's separate case/ledger files remain an explicitly disclosed non-crash-atomic boundary. The SQL decision guarantee must not be generalized to a JSON crash or an unknown commit outcome.
* Stock comparisons remain competing assertions with a query owner; reconciliation remains a human attestation, not verified source authority. Existing role mappings and independent human/professional approvals remain unchanged.
* No ranking weights, inferred vulnerability/health, nomination route, procurement/capacity, architecture, package or infrastructure change is justified. No web change is planned; an unexpected web edit would require its own applicable validation rather than relying on the existing browser skip.
* Engineering criterion evidence can support an open Refs #84 PR without asserting full BRD AC-065, operational readiness, actual human accessibility/competence acceptance or permission to close/merge the issue.

## Questions or Blocking Evidence Gaps

* No decision-critical user question. The three findings are directly resolvable by the planning parent within current direction.
* The supplied research does not embed raw baseline/probe transcripts. It is sufficient for this planning assessment alongside source corroboration; implementation must retain exact red/green commands and failures before production edits, not treat narrative summaries as new execution evidence.
* Current container responsiveness, cached image availability and real SQL Server outcomes were not independently checked by this read-only critique. The plan must report actual execution rather than convert feasibility into a completed result.

## Limitations

* No test, fault probe, container, GitHub query, paid/cloud call or private dataset access was performed in this critique.
* The reported baseline is not a whole-project regression result; the browser skip is not human or WCAG acceptance.
* Source inspection is bounded to the supplied mechanism and relevant current seams/tests. No exploitable-vulnerability audit or unrelated workflow review was conducted.
* Planning verdict is not implementation approval. No future test result, actual professional delegation or current legal/source-policy approval is invented.
* Only this critique artifact is written. Plan, phase details, research, source, existing review records and lifecycle state are left unchanged.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: directly revise P03-T01/T02 to distinguish accepted residuals from unresolved in-scope blockers, and incorporate PC-002/PC-003 as bounded validation commitments in P01/P02.
* User response required: No.
* Handoff: return Complete / Revise to the active planning parent with this entire actionable set. The parent finalizes compatible corrections without another critique, then continues the already requested ordered RPI lifecycle.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-17/assessment-reconciliation-controls-84-plan.md](.copilot-tracking/plans/2026-10-17/assessment-reconciliation-controls-84-plan.md) | Supplied final-candidate plan; unchanged |
| [.copilot-tracking/details/2026-10-17/assessment-reconciliation-controls-84-phase-details.md](.copilot-tracking/details/2026-10-17/assessment-reconciliation-controls-84-phase-details.md) | Supplied phase details; unchanged |
| [.copilot-tracking/research/2026-10-17/assessment-reconciliation-controls-84-research.md](.copilot-tracking/research/2026-10-17/assessment-reconciliation-controls-84-research.md) | Supplied evidence synthesis; unchanged |
| [.copilot-tracking/reviews/plans/2026-10-17/assessment-reconciliation-controls-84-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-17/assessment-reconciliation-controls-84-plan-critique.md) | Complete single critique; Revise, 1 High and 2 Medium |

## Next Steps

Active planning parent: resolve PC-001 through PC-003 directly in the existing
plan/details, preserve scope and test budgets, and finalize without a second
critique. No user action is required. This critique execution stops here; it
does not start implementation, review, commit, push or PR publication.
