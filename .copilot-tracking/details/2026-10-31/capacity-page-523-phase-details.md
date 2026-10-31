---
title: Capacity page 523 phase details
ms.date: 2026-10-31
---

## Metadata

Task ID 523; slug capacity-page-523. Plan:
.copilot-tracking/plans/2026-10-31/capacity-page-523-plan.md.
Evidence: .copilot-tracking/research/2026-10-31/capacity-page-523-research.md.
Current state: Ready after one Complete / Revise critique and direct dispositions.

## Phase Index

| Phase | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Regression-only implementation | Implemented | P01-T01 |
| P02 | Validation/freeze | Passed | P02-T01 |
| P03 | Review/publication | Not started | P03-T01, P03-T02, P03-T03 |

<!-- rpi:phase id=P01 -->
## P01: Regression-only implementation

<!-- rpi:task id=P01-T01 -->
### P01-T01: Persisted legacy SQL regression

Use ProcurementApi's constructed fixture, issue a work order using the supplied
capacity and resident bindings, then remove only package contract_version and
persist under store.lock. Reopen with self.make_store(self.path) and point
self.store/self.app.store at it, following existing HTTP-test prior art.
ProcurementApi is inherited by JsonProcurementApi: preserve both original backends,
assert reopened SQL path when self.sql, register new DB cleanup only for SQL.
Do not discard original connection cleanup or HTTP shutdown.
Capture persisted procurement/audit after reopening, verify resident bindings are
still supplied and no contract_version was invented. Call both GETs twice; check
identity, null projection, Unknown status, unchanged persisted source/audit.
Refused appointment offer uses existing offer payload and asserts 403/current
authority with no procurement mutation. Exactly one added method, no removals,
no production/check/fixture changes.

<!-- rpi:phase id=P02 -->
## P02: Validation/freeze

<!-- rpi:task id=P02-T01 -->
### P02-T01: Exact requested validation and defect sensitivity

Run focused regression first. Under a temporary test-only patch of
ProcurementMixin._appointment_binding, force the original strict lookup on the
legacy package, then invoke the new regression via unittest. Expect it to fail
on /api/workorders rather than accept a success proxy. No runtime file edits.
Run both SQL and JSON instances, full test_procurement_api and requested discovery using the exact caller
PYTHONPATH from src/api, plus ruff check . and ruff format --check . in the pip venv.
Use shared heavy lock and external session logs. Current Research already
executed the complete owned SQL/Chromium page check before implementation;
unchanged browser/runtime source needs no duplicate design review. No axe
acceptance claim: Research scans were NOT RUN.

<!-- rpi:phase id=P03 -->
## P03: Review/publication

<!-- rpi:task id=P03-T01 -->
### P03-T01: One independent implementation Review

Main advanced in unrelated infra/workflow/tooling/docs while validation waited.
Commit implementation, then merge latest origin/main into this topic branch
without rewriting history so required gate ancestry holds. Preserve initial
research/critique base; no main or other-worktree writes. Supply frozen diff,
plan, details, critique/dispositions, research and raw
validation logs. Reviewer writes only
.copilot-tracking/reviews/logs/2026-10-31/capacity-page-523-review.md.
Preserve original adverse findings and route later work. No second critique/Review.
Parent reconciles completed markers and state before local commit.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Commit and complete gate

Author and committer use authenticated gh account's privacy-safe noreply email
via repository-local config; required Copilot trailer. Commit exact source and
original RPI evidence before full gate. Keep authoritative receipt external:
/tmp/ama-523-20261031-c70d35f2-final. Run --all against freshly fetched origin/main,
then default full-scope verification. Any failure blocks publication. No skipped
prerequisites, cloud fallback, receipt mutation, main/other-worktree writes or
history rewriting. Independent exact-head publication assessment is separate
from original implementation Review. PC-002's alleged /tmp prohibition is not present in the
parent context; retain mandated serialization and external directories.
Any bookkeeping commit after gate
invalidates it and requires a new complete run.

<!-- rpi:task id=P03-T03 -->
### P03-T03: Authorized branch publication

Fetch main and verify receipt against current origin/main immediately before
push and exact-head assessment. Push only fix/capacity-page-523 without force.
Open PR to main with Refs #523 and evidence/validation/live-pending distinction.
Do not tick issue acceptance, merge, deploy or sign in.
