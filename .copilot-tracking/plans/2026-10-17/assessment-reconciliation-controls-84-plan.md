<!-- markdownlint-disable-file -->
# RPI Plan: Assessment reconciliation controls #84

## Task Metadata

* Task ID: 84
* Task slug: assessment-reconciliation-controls-84
* Plan date: 2026-10-17
* Planning status: Ready; one critique Complete / Revise, compatible findings resolved
* Delivery outcome: Not accepted; one Review complete, RV-001 High blocks successful delivery
* Phase details: .copilot-tracking/details/2026-10-17/assessment-reconciliation-controls-84-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-17/assessment-reconciliation-controls-84-plan-critique.md

## Executive Summary

Preserve and independently prove the four already-delivered #84 mechanisms.
Close two actual SQL gaps: cached revoked staff can still make technical/stock
decisions, and a failed case write can leave a success audit. A bounded decision
scope will reuse fresh registered-actor checks, current SQL writer transactions
and discard behavior. No new authority model, policy or product architecture.

### What You May Not Know

Existing tests already pass for comparisons, separate versioned decisions,
affected-only staleness and missing flags. New constructed negative probes,
not issue labels, justify this continuation. JSON's separate snapshot/ledger
files are not SQL-style crash-atomic; this slice does not redesign that backend.

### Unresolved Decisions or Blockers

No implementation blocker. Operational competence, source authority, full BRD
cohort/nomination acceptance and human accessibility acceptance remain unproven.
Superseding post-implementation outcome: RV-001 is a reproduced in-scope blocker.
Early/persistent discard-read failure can leak success audit or replace the
original operation error. Stop implementation under the explicit concrete-
blocker boundary; only incomplete visibility publication remains authorized.

## User Decisions and Requirements

* Full ordered RPI, dated committed research/plan/details/changes/review and phase execution; normal push/main PR using Refs #84, no closure/merge/rebase/force push.
* Exact four criteria; #81 hierarchy only; no explicit issue dependencies.
* Inspect actual current behavior; fail-before regressions for genuine root gaps only.
* Preserve existing independently approved sign-off authority and deterministic ranking; no AI control decisions or inferred health/competence/source authority.
* Tiny constructed fixtures; no private/cohort/real-map inputs, paid inference or real cloud.
* Avoid #90 procurement/capacity and #381 infrastructure/package changes; flag surgical shared Store/SQL seams.

## Goals

* Reconciliation and technical decisions use current registered authority and cannot retain failed SQL success events.
* Four exact engineering criteria remain independently reproducible without inflating operational acceptance.

## Scope and Non-Goals

In scope: stock.py, signoffs.py, minimal Store/SqlStore seams, existing core/API
test modules, component documentation and needed synthesis/index/append log.
No web edit expected. No procurement/schema/package/infra/ranking-policy change,
generic lock rewrite, new API or competence/source-policy registry.

## Functional Requirements

* Preserve both comparison values, query owner, source metadata and immutable terminal events.
* Preserve assessment/design/building/coordination role separation, versions and affected-only reassessment.
* Reject changed/deleted/unbound actors before mutation and revalidate inside the SQL writer lock, including OID identity where supplied.
* On SQL decision error, discard staged case and success audit; rethrow the original failure rather than succeed.
* Keep missing support Unknown and existing independent hazard/wait/stage ordering unchanged.

## Non-Functional Requirements

* Reuse existing actor and SQL mechanisms; no new schema, dialect SQL or dependency.
* Fresh-process/reopened durable state and ledger must agree after success/failure.
* Existing relevant tests and project Ruff/format/mypy commands must pass.
* Local throwaway SQL Server parity may use existing cached image only; never a real database.

## Acceptance Criteria

| Criterion | Independent evidence |
| --- | --- |
| Conflicting values and query owner | Existing JSON/SQLite + HTTP comparison tests |
| Four separate versioned sign-offs | Existing core sign-off tests, strengthened version/history assertions |
| Only affected sign-offs stale | Existing explicit affected-set tests plus persistence/reopen assertions |
| Not flags-only; missing unknown | Existing truth table, independent safety/wait rank and SQL ordering/upgrade tests |
| Genuine authority/failure gaps | New revoked/deleted/changed-OID actor, precommit race and write/audit failure tests fail before production edits |

## Sources

* .copilot-tracking/research/2026-10-17/assessment-reconciliation-controls-84-research.md: C1-C7, W1-W3 and exact baseline/probes.
* docs/prds/zava-forward-retrofit-programme-demonstrator.md: FR-012, FR-013.
* docs/brds/agentic-retrofit-programme-brd.md: FR-037/AC-065 and RULE-017; broader acceptance remains separate.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Focused regression and implementation

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Establish fail-before regression evidence

Add bounded negative tests for current staff and failed SQL decisions before
production edits. Strengthen existing four-criterion persistence assertions.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Scope reliable current-authority SQL decisions

Use existing actor helper in a stock/technical context, register a scoped
transaction validation hook, discard SQL pending edits/events on any failure.
Do not modify generic _SyncLock/_finish semantics or other workflows.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate and record exact boundaries

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Execute focused and project checks

Run focused core/API/ranking/hazard tests and Ruff/format/mypy; SQL rollback and
reopen cases mandatory. Reuse actual existing local SQL Server guide/image if
feasible, record unavailable checks honestly. No browser interaction change.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Update current component/synthesis evidence

Update core/API guides, existing relevant synthesis/index and append log only
as needed. Reconcile task markers, changes ledger and execution evidence.

<!-- rpi:phase id=P03 -->
### [x] P03: One Review and incomplete visibility publication (execution only)

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: One post-implementation RPI Review

Record execution separately from outcome and route accepted out-of-scope
residuals without a review loop. Failed exact criteria, current-authority denial
or durable rollback/audit consistency are in-scope blockers, not accepted
residuals. An unresolved blocker prevents a successful completion claim; stop
incomplete and label any visibility PR incomplete rather than acceptance-ready.
No second Review or automatic backlog selection.

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Privacy-safe commit, push and incomplete draft main PR

Resolve gh api user, local privacy-safe author/committer email and required
Co-authored-by trailer. Refs #84 with criterion evidence, overlap and limitations.
Stop at final publication as explicitly requested; no invented follow-up selection.
Actual evidence: source/evidence commit 2e45b5e normally pushed; draft main
PR #382, https://github.com/jmservera/ama/pull/382, explicitly Not accepted
and Do not merge. Authenticated gh account 8036360/jmservera supplied local
privacy-safe author/committer email; required Copilot trailer retained.

## Test Ownership and Locked Budget

* Canonical semantic/regression owner: src/core/tests/test_stock_reconciliation.py.
* HTTP owner: src/api/tests/test_stock_reconciliation_api.py; existing harness reused.
* SQL parity owner: existing opt-in src/api/tests/test_mssqlstore.py harness if extended.
* Maximum additions: 10 core methods, 2 HTTP methods, 1 opt-in parity class; none removed.
* Generated targets: none; existing constructed fixtures only.
* Validate negative cases fail before source edits; positive four-criterion assertions and focused suite pass after edits. No new testing tool.
* PC-002 lifecycle matrix within the same budget: success, entry rejection,
  body error, save error and BaseException precommit interruption; restore
  prior/absent scope and prove no leak into an unrelated later save. Preserve
  original failure when recovery reports its own fault; disclose uncertainty.
* PC-003 one opt-in MssqlStockDecisions class reuses selected canonical fixture
  tests: all three decision successes, stale identity and independent second
  connection pre-save role change, transactional failure/reopen/no delayed audit.
  Run from src/api with existing ZF_TEST_MSSQL/isolated localhost ZF_SQL settings:
  PYTHONPATH=tests:../core/tests:../agents/tests ../../.venv/bin/python -m unittest test_mssqlstore.MssqlStockDecisions -v.
  If unavailable, record exact Not run cases; generic harness success is not parity.

## Dependencies

No explicit issue dependencies. P01-T02 depends on P01-T01;
P02 depends on P01; P03 depends on recorded P02 evidence. #81 is hierarchy, not
RPI parent. Only owned Store/SQL hunks overlap potential #90 integration.

## Critique Disposition

Exactly one final-candidate critique executed, verdict Revise. No repeat.

| Finding | Owner/disposition | Resolving evidence |
| --- | --- | --- |
| PC-001 High | Planner, resolved directly | P03-T01 now distinguishes accepted residuals from failed engineering gates; incomplete-stop route, no successful acceptance claim |
| PC-002 Medium | Planner, resolved directly; implementer executes | Test Ownership lifecycle/error matrix and P01-T01 details, within existing budget |
| PC-003 Medium | Planner, resolved directly; implementer executes | Named MssqlStockDecisions parity class/command and exact selected cases; unavailable cases remain explicit |

Review supersedes implementation acceptance of PC-002: the recovery-fault
oracle discards successfully before raising, missing early/persistent reload
failure. RV-001 remains blocking; no second critique or Review.

## Follow-Up Items

* RV-001 High / blocker: later explicitly authorized implementation must
  contain pending failed success audits and original errors across early and
  persistent recovery failures. Not an accepted residual; current delivery
  remains incomplete. No child task or correction is started here.
* Human professional/delegation, source-policy/eligibility and broader AC-065 nomination/cohort acceptance remain outside this engineering slice; #130 owns nomination by owner direction.
* JSON cross-file crash atomicity is an existing backend limitation, not silently replaced by SQL claims.

## Handoff

Implementation evidence target:
.copilot-tracking/changes/2026-10-17/assessment-reconciliation-controls-84-changes.md.
Research complete; plan Ready after one critique and direct dispositions.
P01/P02 complete: 631 core tests (one existing opt-in skip), 72 targeted API tests
(one browser skip), separate actual Chromium comparison test, eight actual
isolated SQL Server tests, core/API static checks and documentation links.
One Review complete, outcome Not accepted due to RV-001. Incomplete draft
visibility PR #382 published; no successful delivery/acceptance claim.
No production edits occurred during Research or Plan. Full plan is not yet
acceptance-ready: all phase execution/publication markers complete, engineering
delivery remains blocked. Automatic session stopped at the caller's explicit
concrete-blocker/final-publication boundary. No follow-up work selected.
