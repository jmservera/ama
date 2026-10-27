<!-- markdownlint-disable-file -->
# RPI Phase Details: finance-96-98-99

## Metadata

* Task ID / slug: finance-96-98-99
* Date: 2026-10-27
* Plan: .copilot-tracking/plans/2026-10-27/finance-96-98-99-plan.md
* Research: .copilot-tracking/research/2026-10-27/finance-96-98-99-research.md

## Phase Index

| Phase | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Independent draft controls | Complete | P01-T01, P01-T02 |
| P02 | Evidence and validation | Complete within independent boundary | P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Independent draft controls

Context: forms.py already stages immutable unapproved definitions/candidates. Approved schema/rule authority is missing. Build working review notes, not an approved-template preparation bypass.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Core review, diagnostic manifest and held ledger

Likely target: src/core/src/zava_forward/core/form_review.py. Typed core functions reuse forms validation helpers and current actor. All writes use change_provenance.controlled; audit precedes save within its rollback boundary. Per-case form_reviews stores drafts; finance_decision_holds stores unresolved decisions with actor/time and no monetary/approval defaults.

Open binds exact schema ID/version/digest and explicit unapproved status. Review accept/correct/reject requires exact draft version, field ID, reason and candidate binding for sourced values; source evidence must remain same case, schema version, kind, clean and exact current hash/version. Correction can record a manually supplied scalar only with explicit source evidence/reason; no human-only categories. Immutable field history carries prior/new value and reviewer. Staging remains unchanged.

PC-001: evidence checks are non-mutating and require already-clean evidence. Never call forms._document/ensure_scanned or a scanner in review/diagnostics. Missing/pending/infected evidence returns the existing DocumentUnavailable denial; a separate document scan/recovery must complete before retry. Acquire/recheck actor, case, version and source inside controlled; only then mutate review/history/holds. No review rollback resurrects separately quarantined metadata.

PC-002: accepting a staged candidate preserves raw text, never an implicit conversion. Typed number/integer/boolean values require explicit correction retaining raw source. Support string, exact int excluding bool, finite int/float excluding bool, exact bool, ISO YYYY-MM-DD valid calendar date, and enum using identical scalar type and value. Conditions use that same type-aware equality. Multiple required_when predicates combine with OR: any valid/current confirmed true makes required; otherwise an absent/invalid/stale controller makes condition Unknown, and all known false means not required. Unreviewed candidates never control requiredness. Unit, currency, formula and eligibility verification remain explicitly Not evaluated.

PC-003: JSON is one Store/writer only, with stale in-instance draft-version rejection. SQLite adds independent writer rowversion conflicts. No cross-process JSON guarantee.

Diagnostic functions are pure and never run model inference. Values count as confirmed only for accepted/corrected fields whose evidence is still current. Missing/conditional/type/conflict issues are field-scoped. Unknown approved rules/calculations/template authority always hold reviewed readiness. A manifest is a labelled working diagnostic artifact, not a reviewed pack. Attachments are bound original documents, not generated placeholders or fetched URLs.

For source changes, derive stale only for fields linked to that document; for schema changes all fields bound to that schema are stale. Keep previous values/reviews. Do not mutate downstream approvals or claim AC-051's full graph.

Board ledger records OD-12/15 missing evidence with null approved inputs. Expose Pause for human decision as a diagnostic only; there is no claimed programme release gate, breach calculator or restart.

Completion: field isolation, safe partial diagnostics, explicit held decisions, persistent exact lineage and no controlled side effects, covered over JSON and SQLite.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Authenticated HTTP and projection isolation

Targets: existing server form route handler, get_kind categorization and Store.detail. Case /form-review GET returns authorized working records/manifests; POST supports only open/review/diagnose. Bodies have strict exact keys; actor/status/approval are server-owned. Use current forms._actor checks in addition to generic route access. No browser/UI files changed.

Do not leak any stored field value or historical reason after evidence quarantine. Ordinary detail strips new private keys, including for staff; only the dedicated authorized endpoint returns them. Preserve documented 400/403/404/409/502/503 error semantics.

<!-- rpi:phase id=P02 -->
## P02: Evidence and validation

<!-- rpi:task id=P02-T01 -->
### P02-T01: Prove independent controls locally

Baseline: 17 existing form staging tests pass after missing packages were pip-installed into a task-specific external venv. Initial system Python run failed because distributions were absent, not because of a source failure.

Test ownership/removals/addition limits are fixed in the plan. Use a typed unittest fixture around the existing small dataset; no additional package fixtures. Tests compare whole authoritative case state minus new private review keys and audit-only metadata, compare unchanged sibling fields and original candidate arrays, reopen stores and inject failures. Exact affected/unaffected sets are asserted for this draft-only freshness boundary. Include pending/missing/infected source denial without scanner invocation, JSON/SQLite rollback/reopen, SQLite independent writer conflict, and table-driven six-type/typed equality/conditional Unknown checks. HTTP tests reuse FormApi's live loopback thread with /healthz confirmation; do not start a development server or Azure workload.

Run smallest core selectors together; run API full discover with PYTHONPATH=../core/tests:../agents/tests from src/api as requested. Escalate only for relevant failures. Run Ruff/mypy on changed typed files and touched server boundary according to component overrides. Do not claim Azure SQL/browser/production acceptance.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Document partial acceptance and prepare Review handoff

Targets: component READMEs; reference index and append-only log; dated changes/state and pre-Review reconciliation. Record per-issue criteria as proven, partial or blocked without modifying issues. Every partial criterion lists missing evidence. This task completes with the implementation handoff, not future parent-owned Review/publication. Independent Review executes once after implementation, and findings route to follow-up rather than an in-task repeat. Retain all original critique/Review outcomes.

Before commit use gh api user's id/login-derived local email for author and committer, include Conventional Commit and Copilot trailer. Push only existing topic branch, open one draft PR to main with Refs #96, Refs #98, Refs #99; include tests and exact human decision requests. If hosted checks have not run, state that rather than infer them.

## Completion Evidence

P01/P02 implementation and documentation handoff are complete. Consolidated core unittest selection: 199 tests, 54 optional SQL Server skips, no failures. Complete API discovery: 1124 tests, 314 optional skips, no failures. Changed Python Ruff and targeted core/API mypy pass; five new-section relative links/anchors and diff whitespace checked. New tests use one core class and three added HTTP methods, within the locked ownership limits. No test removed.

The parent now owns the single independent Review and draft publication. Human Finance/template/rule and Board OD-12/15 decisions remain unresolved. No --all or heavy --changed gate, browser/deployment/Azure SQL, real inference or operational acceptance is claimed.
