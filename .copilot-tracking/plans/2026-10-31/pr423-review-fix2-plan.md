---
title: PR 423 integration and review correction plan
description: Minimal preservation-first offline repair plan
ms.date: 2026-10-31
---

## Task Metadata

Task ID and slug: pr423-review-fix2. Status: Source implementation and validation
complete; independent Review and local commit pending.

## Executive Summary

Merge ec2d784255c3377ab39e5d2d1b5140e76c8e7f36 into the supplied clean child
branch, retaining both parents and taking main's rubric JSON. Preserve already
built page/runbook corrections; explicitly cap Blob consumer reads, strengthen
regressions, clarify history/defaults/cleanup and qualify candidate provenance.
Local tests and Bicep compilation do not establish a successful full receipt,
live acceptance or publication authority.

## Sources

.copilot-tracking/research/2026-10-31/pr423-review-fix2-research.md C1-C9;
owner request and four unresolved PR threads retrieved 2026-10-31.

## User Decisions and Requirements

* Full ordered RPI loop with dated artifacts; owner PR #423, Refs #360.
* Merge origin/main, not rebase; lose none of the built work.
* Preserve both log append sequences; take main's latest.json.
* Bound downloads and every wrapper-inclusive page, with regressions.
* Current instructions use includeResultBlob default false and private access.
* Correct tracking provenance; owner alone edits the PR body.
* Pip only, no Azure/secrets, shared heavy lock, local commit with trailer;
  do not push.

## Goals

Preserve integrated work and demonstrate the exact four corrections honestly.

## Scope and Non-Goals

Source edits limited to staff Blob helper/tests, active infra runbook, old
changes qualification and dated tracking. Merge all main work intact.
No UI edits, cloud activity, private data, issue closure, publication or
rewriting original critique/Review outcomes.

## Functional Requirements

Ranged download and explicit read amount cap buffers at MAX_BLOB + 1.
Reject overflow and mismatched listed sizes before decoding. Retain existing
all-pages serialization validation, including head/wrappers. Preserve owned
temporary-job and roster-secret cleanup on refusal.

## Non-Functional Requirements

Reuse existing tests/fakes; sanitized failures, no fallback, no secrets.
Heavy validation/install/build commands use flock -w 600
/tmp/ama-rpi-heavy.lock. External task-owned venv/evidence only.
Complete exact-head gate remains required before publication, not replaced by
requested focused tests. No publication in this task.

## Acceptance Criteria

* AC1: Real merge retains 7eba6116 and pinned main ancestry; no source/tracking
  deletions; latest.json equals main; both parent log bodies survive.
* AC2: Replacement regression proves bounded read and controller cleanup;
  valid multi-page round trips remain complete.
* AC3: Exact ['x' * (PAGE_BYTES - 3), 'y'] refusal occurs before upload,
  every serialized page/head remains bounded, exact boundary controls retained.
* AC4: Active default-off Blob prerequisites, opt-in deployment and retention/
  IAM cleanup are unambiguous; dated tag commands remain historical.
* AC5: Tracking explicitly disclaims any successful receipt for the integrated
  candidate and marks run9/stale provenance historical; PR body untouched.
* AC6: Requested unittest and offline Bicep results, one independent Review
  and local commit identity/trailer recorded; no push or live claims.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### P01: Integration and correction

* [x] P01-T01: Merge pinned main and verify content/ancestry preservation.
* [x] P01-T02: Cap consumer read; strengthen existing Blob regressions.
* [x] P01-T03: Clarify runbook/history/cleanup and provenance qualification.

<!-- rpi:phase id=P02 -->
### P02: Validation, Review and local delivery

* [x] P02-T01: Restore missing installed namespace with pip externally; run
  targeted tests, related infra checks, Bicep and focused lint/types/diff checks.
* [ ] P02-T02: One independent Review; preserve outcome and route findings;
  reconcile artifacts, commit locally with privacy-safe identity and trailer.

## Test Ownership and Change Budget

Canonical test owner: infra/tests/test_staff_azure.py. Generated targets:
none committed; compiled Bicep stays external. Exact removals: none.
Maximum additions: two Blob regression tests; strengthen existing replacement,
round-trip and requested near-boundary tests. Semantic coverage: hard read
size, no readall, overflow/mismatch refusal, complete results and cleanup.
Regression coverage: reviewer counterexample, head and exact limits.
Use existing RBAC/Bicep tests unchanged. No test skips or gate relaxation.

## Dependencies and Readiness

P01-T02/T03 follow merge; P02-T01 follows source corrections; P02-T02 follows
validation. Research Ready. Baseline test import lacks installed core; pip
restore is authorized by that actual failure. No unresolved implementation
decision; publication gates remain unproven.

## Critique Disposition

Exactly one independent final-candidate critique executed: Complete / Pass,
zero findings. All owner direction and test ownership retained; no second
critique. Artifact: .copilot-tracking/plans/2026-10-31/pr423-review-fix2-critique.md.

## Follow-Up Items

Owner PR body correction; fresh complete exact-head gate and independent
hosted/human acceptance before publication; authorized live Blob exercise.
No follow-up source implementation is selected.

## Handoff

Details: .copilot-tracking/details/2026-10-31/pr423-review-fix2-phase-details.md.
Critique: .copilot-tracking/plans/2026-10-31/pr423-review-fix2-critique.md.
Implementation changes: .copilot-tracking/changes/2026-10-31/pr423-review-fix2-changes.md.
