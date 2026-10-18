---
title: Issue 126 RAI evidence register plan
ms.date: 2026-10-18
---

Task ID: 126. Slug: issue-126-rai-evidence-register.
Parent: 123. Base: ab0613f3336109ff9b96560a16758ee842232715.
Status: ordered loop complete; sole critique Complete / Revise, directly
dispositioned; sole original Review Complete / Conformant, bounded engineering only.

## Executive Summary

Append constructed claims to the existing checked governance document. Return all
22 immutable baseline findings with a detached, explicit assessment comparison.
No claim, including an independent-acceptance claim, grants acceptance or closure.
Existing AI release admission remains untouched. Real human/live gates remain unmet.

## User Decisions and Requirements

* Execute Research, Plan/details, one critique with dispositions, Implement, one
  original Review; preserve original adverse artifacts byte-identically.
* Use existing GovernanceMixin, GET governance and one closed append action.
* Preserve all 22 open baseline checks, current identity and exact provenance.
* No private sources, role grants, autonomous signatures, new service/table,
  acceptance endpoint, UI, live calls, Azure or deployment.
* Publish from pinned branch without rebase; PR uses Refs #126 only.

## Sources

Research: .copilot-tracking/research/2026-10-18/issue-126-rai-evidence-register-research.md.
C3-C9 ground implementation and validation. Live issue requirements retrieved
2026-10-18; original v0.16.0 source 7a8b1fe65475752fcf242ed52acab8e7e43b58d3.

## Goals

Complete finding inventory and reproducible claim provenance, not compliance.

## Scope and Non-Goals

Governance module; narrow SqlStore hooks; governance-only server route integration;
focused existing governance tests plus one HTTP test file; core/API guides,
addendum/PRD/ADR 0002, KB index and append-only log. No other control writers.
No generic JSON persistence rewrite. JSON crash atomicity remains unavailable.

## Functional Requirements

Closed claim body: finding_id, baseline_commit, assessment, evidence_tier,
result, references, limitations, decision_maker_status, decision_maker_ref,
event_ref, expected_revision. Assessment is exact closed mapping source_commit,
task_id, task_version, release_version, nonapplicability_reason.
Full lowercase 40-hex commits; either all three task/release strings or explicit
nonapplicability reason with null task fields. This is a declared comparison
context, not server deployment attestation; absence is Unknown. Baseline commit
can be recorded but never appears fresh.

Tiers: implemented/source-tested, deployed-observed, proposed, insufficient,
independent-acceptance. All are constructed unverified CLAIMS. Decision-maker
status: Unknown, Unappointed, Unverified reference; supplied refs never assign.
Server records fresh authenticated identity, UTC, global append revision.
Same event/ref/body/actor reconciles without write/audit even with old revision;
conflicting reuse fails. New append requires exact global expected revision.

GET returns exactly 22 unique IDs, original status/verdict and baseline provenance,
all claim history plus current matching claims/history classification. Completeness
of supplied dispositions is separate from evidence adequacy; acceptance Unknown,
all Open, no green summary. Missing/legacy evidence is insufficient.
GET uses optional assessment JSON query parameter with closed exact schema;
no query means Unknown. Returned data is detached and does not initialize defaults.

## Non-Functional Requirements

Require current registered manager before reads/writes. Reuse _actor and SQL
change_validation under writer transaction. Use shared governance CAS, audit,
_discard and a narrow immediate post-COMMIT witness. Failed pending success audit
must be quarantined before recovery. Postcommit error reports committed/reload.
Bound inline text/list lengths, inert refs, no fetch, no client actor/time overrides.

## Acceptance Criteria

All ten caller-focused criteria map to tests: inventory; append/reopen/provenance;
binding staleness/baseline history; completeness vs closure; invalid/promotional
body rejection; direct/HTTP role and transaction-time actor denial; rollback/race/
event reconciliation/acknowledgement; detached deterministic no-write reads;
existing governance and release preservation; supported docs with honest limits.
SQL parity and non-root image must actually execute or remain explicitly unmet.

## Phase Checklist

<!-- P01 -->
### P01: Core and API engineering

* [x] P01-T01: Add failing-first inventory/claim/adverse tests.
* [x] P01-T02: Implement bounded claim schema, detached view and checked SQL hooks.
* [x] P01-T03: Wire governance read/action only and running HTTP adverse tests.

<!-- P02 -->
### P02: Validation and documentation

* [x] P02-T01: Run targeted existing/new tests, Ruff/mypy, actual disposable SQL parity.
* [x] P02-T02: Build/run hardened non-root image with focused tests.
* [x] P02-T03: Update current guides/spec/ADR/index and append-only log with actual evidence.

<!-- P03 -->
### P03: Original Review and publication

* [x] P03-T01: Reconcile evidence, execute exactly one original Review, hash originals.
* [x] P03-T02: Commit owned source/artifacts, push and open non-closing PR; stop.

## Test Ownership and Change Budget

Parent owns all implementation/tests. No implementation subagents.
Exact removals: none. Maximum added source modules: zero. Maximum added test files:
one API harness; extend existing core test_governance.py. No generated targets.
Semantic tests: inventory/bindings/claims. Regression: existing protocol/releases/
breaches and task-release suites. Evidence: fail-before/pass-after, durable SQL,
running HTTP, non-root image commands and actual outcomes.

## Critique Disposition

Original: .copilot-tracking/reviews/2026-10-18/issue-126-rai-evidence-register-plan-critique.md.
Execution Complete; verdict Revise; two Medium findings. Original SHA256
4e24e7e0cc8cf21081c4e5823cbbfbd8fbf0d1d0a8e904220ecd5b0e3235c8bb.
PC-001 applied directly: distinct exact-context finding coverage, denominator 22,
separate history count, no-context Unknown and baseline coverage zero.
PC-002 applied directly: concrete primitive and cross-field matrix in details.
No user decision required; no second critique. Original remains unchanged.

## Follow-Up Items

Qualified current-source assessment, named competent decisions and human/live
AI/SQL/Azure acceptance remain independent, not implemented by this task.

## Handoff

Changes path: .copilot-tracking/changes/2026-10-18/issue-126-rai-evidence-register-changes.md.
No unresolved engineering authority; claim-only manager roles already exist.
Published PR #409 targets main; no source edits after the original Review.
Final handoff metadata is not a replacement assessment. Correction count 0.
Caller requires Stop for coordinator independent exact-head source/artifact/log review.

## Authorized Integration-Only Continuation

The initial no-rebase decision above describes the original publication. The
coordinator subsequently explicitly authorized this same task's owned-topic
rebase onto exact `9403dc6a8f52f1f04c5ad910faab11a57c29ee78`, with old local/remote
head `4a23f750f1ea943bb4aaf989256e7bd019a57d12` as the sole authorized first-push
lease. No new phase markers, source correction, critique or original Review.

Rebase completed; only the obvious additive KB log conflict required resolution.
All 30 original-path normalized patches and all six source/config/test patches
match byte-for-byte before/after normalization. Upstream protected files/modes
and original research, assessments and prior logs remain unchanged. Fresh focused
checks: 107 run/16 skips; consultation/API checks: 64 run/13 skips, both successful.
Configured core/API Ruff, formatter and mypy pass. Four existing excluded source
files retain their original formatting drift; no formatting was applied.
Historical actual SQL/image evidence is not represented as fresh integration work.

Separate receipt and full hash manifests:
.copilot-tracking/changes/2026-10-18/issue-126-rai-evidence-register-integration/receipt.md.
Publication uses only the authorized lease, then normal receipt pushes. Preserve
all unmet human/live gates and Stop for coordinator exact-head inspection.
