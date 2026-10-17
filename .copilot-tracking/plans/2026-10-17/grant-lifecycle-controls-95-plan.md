<!-- markdownlint-disable-file -->
# RPI Plan: Grant lifecycle controls

## Task Metadata

* Task ID: 95
* Task slug: grant-lifecycle-controls-95
* Plan date: 2026-10-17
* Planning status: Ready after one critique and direct dispositions
* Phase details: .copilot-tracking/details/2026-10-17/grant-lifecycle-controls-95-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-17/grant-lifecycle-controls-95-plan-critique.md

## Executive Summary

Retain the existing separate application and grant state records, and close
reproduced authorization gaps. Reuse #94's registered actor, independent identity,
write recovery and SQL transaction validation rather than a second persistence
implementation. Require explicit scoped, dated, human exercise designation for
authority-bearing grant/application records; no role alone confers authority.
Keep GBP-only amounts explicit, with no opportunity-to-award/cash carry-forward.

### What You May Not Know

The existing grant second-person check was email-only and accepted unregistered
role dictionaries; both JSON and SQLite reproduced this. Existing application
submission has a separate bypass. Current dashboards do not contain the case
GBP 40 million or aggregate monetary grant-capture totals. Full PRD pack/version
acceptance is broader than this issue and will not be invented here.

No real delegation is supplied. Exercise designations must be explicitly
synthetic, never seeded automatically or treated as verified real delegation.
Production real financial actions remain unsupported and fail closed.
The single independent Review executed and returned Not accepted (RV-001).
Coordinator-authorized correction ONE restores current legacy preparer lookup
at commit; original verdict remains, no second Review or independent Pass.

## User Decisions and Requirements

* Full ordered automatic RPI loop with one critique and one independent Review.
* Exact criteria: no dashboard presents opportunity as award/cash; only designated
  human financial authority submits, certifies or records receipt.
* Preserve #94 controls and explicit branch/base; #93 is hierarchy only.
* Tiny fictional fixtures, local-first tests and actual SQL Server parity.
* No private data, live financial actions, Azure writes, paid model calls or web
  redesign; preserve original case and append-only KB log.
* Commit own artifacts/source/docs, normally push and create main-targeted PR
  with Refs #95. Stop at clean pushed PR. Never merge or close the issue.

## Goals

* Refuse unregistered/stale/role-only actors and self-approval aliases.
* Retain exact source, amount, currency and identity per grant transition.
* Demonstrate separation of application, award, claim and cash from provider
  invoices and payments without rewriting functioning features.

## Scope and Non-Goals

In scope: grants.py; funding_step in store.py; surgical reusable operation
extraction in finance.py; synthetic test fixtures, focused regressions and guides.
No new endpoints. One narrow application label/evidence-input correction is
required by PC-001; no visual redesign. No new financial submission/payment executor,
scheme rules, real delegation administration or production authority verification.
Full PRD FR-019/042 review/export/pack workflows remain separate follow-up scope.

## Functional Requirements

* Every grant and legacy application write resolves the current registered actor.
* Grant approval requires manager role plus exact designation permission
  `grant:<target state>`. Application approve/submit/confirm require
  `application:<action>`. Permissions never imply each other.
* Trusted staff `financial_authority` is exactly one dictionary: `kind="Synthetic
  exercise"`, `status="Active"`, `human=true`, `subject` containing exact
  email/code/OID, nonempty `evidence_ref`, timezone-aware `effective_from` and
  `expires_at`, and nonempty `permissions` list. Each permission has exactly
  `action`, `case_id`, `route`; grant route is its exact scheme, application route
  is funding.route. No wildcards, implicit all-case authority or request override.
  A fresh UTC authorization clock must satisfy effective_from <= now < expires_at
  both at entry and inside writer transaction. Unknown route refuses.
* Missing, expired, nonhuman, proposed/unverified or production exercise authority
  refuses. The request body cannot grant authority. No existing staff is backfilled.
* Repeat actor, designation and preparer independence inside SQL writer transaction.
* Use captured email/code/OID with #94's legacy lookup fallback. Retain prior
  legitimate audit on failure, no false success, preserve original errors.
* Reject non-GBP or malformed currency instead of silently interpreting it as GBP.
  Preserve existing optional amount compatibility; never inherit opportunity value.
* History adds explicit property, scheme, currency, preparer/approver identities
  and designation snapshot; old histories remain untouched, not "verified".
* Legacy pending grant proposals missing explicit GBP provenance must be withdrawn
  and re-proposed, never automatically re-attested. Legacy preparer identity still
  uses #94 lookup and refuses if unknown. New amounts are event-local, not copied.
* Application approve/submit/confirm history captures action/time, case, route,
  source reference, current identity and designation snapshot. Each requires
  supplied event-specific evidence; keep existing status/reference fields.
* Application events remain in funding, grant events in grants; neither changes
  provider finance or promotes the other workflow.

## Non-Functional Requirements

* Existing #94 suites must remain green. No payment behavior or schema changes.
* JSON/SQLite targeted denial and rollback tests, authenticated loopback API,
  real disposable loopback-only SQL Server; Ruff/format/mypy component gates.
* No public data dump, secret output or full WCAG/live-platform/human acceptance claim.

## Acceptance Criteria

1. Opportunity amount remains only its own event; grant summary and dashboard
   projections never call it award/cash or grant-captured. No source-case promotion
   or monetary carry-forward. Exact issue first criterion has static/projection
   evidence. An Opportunity-only case with a Confirmed application must say
   application confirmation only, never award; actual changed UI exercised locally.
2. Only current, designated, registered humans can record grant approvals,
   submitted/accepted/cash states or application approve/submit/confirm; aliases,
   stale registry records and transaction-time revocation are refused. This proves
   exercise mechanics, not real delegation.
3. Refused/failed writes leave persisted records and success audit unchanged;
   authorized distinct same-role people can progress the existing flow.

## Implementation Context Record

Research: .copilot-tracking/research/2026-10-17/grant-lifecycle-controls-95-research.md
(executed, Ready). Changes record to be created by Implement:
.copilot-tracking/changes/2026-10-17/grant-lifecycle-controls-95-changes.md.
Independent Review: .copilot-tracking/reviews/logs/2026-10-17/grant-lifecycle-controls-95-review.md.

## Sources

* Fresh issue #95, source PRD FR-019/AC-022/050; BRD FR-023/024 and RULE-009/010,
  not stale BRD capacity FR-019.
* Research C4-C8 and actual fail-before probes; #383 merged base d400eb8.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Evidence-led lifecycle hardening

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add failing-first exact regressions

Own tests: new core test_grant_lifecycle_controls.py and API
test_grant_lifecycle_api.py, adapting only synthetic success fixtures in
test_finance_signoffs.py and dataset.py. Exact removals: none.
Maximum additions: two test modules, at most 24 semantic tests inherited across
JSON/SQLite/MSSQL; use existing SQL lifecycle setup and loopback API helpers without inheriting
concrete finance tests. Generated
targets: none. Canonical production targets: grants.py, finance.py, store.py.
Mutation/regression probes target actual unauthorized acceptance, not source text.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Reuse finance operation and current designation checks

Extract the unchanged finance write boundary as a context manager; extend its
existing SQL validation context with optional designation snapshot checks.
Grant and funding actions reuse that boundary. Keep all prior finance behavior.

<!-- rpi:task id=P01-T03 -->
#### [x] P01-T03: Validate and document for independent Review

Run focused then relevant full core/API suites; Ruff/format/type gates in existing
projects. Create unique task-owned loopback SQL container, reuse existing driver,
clean only this container and its UUID test databases. Update component guides,
existing finance synthesis, index and append-only log. Execute one independent
RPI Review of final code and exact criteria as the subsequent parent-owned
lifecycle gate, not an already completed implementation task. Preserve any adverse verdict; one
coordinator-authorized concrete correction cycle permitted.

<!-- rpi:phase id=P02 -->
### [x] P02: Coordinator-selected RV-001 correction

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Restore legacy lookup provenance with failing-first regressions

Grant and preserved-finance code/OID rebind tests must fail before the root
one-line fix. Retain original missing identity in transaction validation context
while returning resolved entry identity only for event history. Captured
historical identity semantics remain unchanged.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Validate correction and publish with original adverse verdict

Run current JSON/SQLite/API/finance suites, actual local SQL parity and existing
quality gates. Preserve original Review artifact. Document resolving evidence
without claiming independent closure; coordinator owns final gate.

## Dependencies

No declared issue dependencies. #94 is a coordinator sequencing prerequisite,
already merged as #383; preserve base without independent rebase.

## Critique Disposition

One independent critique executed; original verdict **Revise** retained.

| Finding | Disposition | Resolving plan evidence |
| --- | --- | --- |
| PC-001 | Applied directly | Mixed Opportunity/Confirmed regression; neutral application label and evidence input, fresh web guidelines and actual browser |
| PC-002 | Applied directly | Exact trusted designation schema and action/case/route matrix above |
| PC-003 | Applied directly | Fresh aware UTC predicate repeated inside transaction; unchanged-snapshot expiry regression |
| PC-004 | Applied directly | Application event history and separate evidence per approve/submit/confirm |
| PC-005 | Applied directly | Legacy pending withdrawal/re-proposal, no currency fabrication |
| PC-006 | Applied directly | Setup-only test reuse, fixture-local designation; path-specific rollback/recovery and parity |

No divergent decision needed, no second critique. Source remains untouched at
planning finalization.

## Follow-Up Items

* Full PRD pack/form/version/export application and claim acceptance belongs to
  later form workflow work, not this issue's two exact criteria.
* Real company delegation and human acceptance require separately supplied,
  verified evidence; no synthetic fixture can satisfy them.

## Handoff

P01 implementation and the one Review executed. Explicitly selected P02 later
implementation is complete with failing-first and local closure evidence;
original Not accepted retained, no second Review. Source and all task evidence
published to main-targeted PR #386 with clean matching local/remote/PR source
head. Publication state is committed separately. Automatic session stops at the
explicitly requested PR boundary; coordinator owns independent closure/checks
and merge. No child task, merge or issue closure.

Subsequent explicit integration authorization is complete: rebased onto fresh
main 1fc7325b93ea845b9cb2e827efbea624f7d20d30, preserving upstream log/index,
actual combined fixture hash and entire own src patch byte parity. Fresh 156
integration tests and existing core/API quality gates pass; earlier SQL/full
suite evidence remains historical. Same original Review and verdict retained.
Publish exact-lease topic update to PR #386 and stop at coordinator gate.
