<!-- markdownlint-disable-file -->
---
title: PR 558 unresolved threads plan
ms.date: 2026-10-31
---

## Task Metadata

Task ID: pr-558-unresolved-threads-2026-10-31.
Task slug: pr-558-unresolved-threads. Planning status: ready after one critique.
Phase details: .copilot-tracking/details/2026-10-31/pr-558-unresolved-threads-phase-details.md.
Critique: .copilot-tracking/reviews/plans/2026-10-31/pr-558-unresolved-threads-plan-critique.md.

## Executive Summary

Normalize only the four textual authoring hash inputs to LF, then verify the
unchanged delivered PPTX and regenerate its source receipt. Retain and exercise
the already-fixed 5.1 guards. Update the PR description with runtime and authority
history, including changes now inherited from main. Publish only after an
external complete exact-head gate and independent assessment.

### What You May Not Know

Current HEAD already contains the finite fixes and LF digests from `aedc6713`.
The source contract still forbids normalization, and no host PowerShell exists.
An isolated local PowerShell container can execute the owning verifier without
installing host packages, uploading inputs or using uv. Windows/Office and human
acceptance remain unperformed.

## User Decisions and Requirements

* Complete research, plan, implement and one review in order with dated evidence.
* Address exactly the three unresolved threads on #558; normal direct push to
  `jmservera/fabric-research` is authorized. Never force-push or merge.
* Normalize source hashes to LF and regenerate receipt only after verification.
* Preserve PowerShell 5.1-compatible finite checks everywhere.
* Disclose January authority, SQL constraint migration, assistant routing/UI and
  hosted CI, with validation and no closing keywords.
* Run requested unittest and existing relevant tests. Package manager: pip only.
* Commit with required Copilot trailer, then push, reply and resolve each thread.

## Goals

Reproducible source binding, preserved native guard refusals, and an honest
reviewable PR description.

## Scope and Non-Goals

In scope: owning capstone verifier, targeted regression script, source guide and
receipt, related knowledge-base index/log, dated RPI evidence and remote thread
operations. No deck content/binary changes, new authorization, SQL or UI edits,
historical evidence deletion, framework changes or acceptance claims.

## Functional Requirements

Hash all four textual inputs as UTF-8 bytes with CRLF and lone CR converted to LF.
Retain every other byte including BOM/whitespace and all exact binary/media hashes.
Record convention in generated reports. Verify complete actual candidate package
before refreshing receipt. Reject nonfinite shapes through existing guards.

## Non-Functional Requirements

No network inside verifier container, repository mounted read-only, outputs
external and owned. Native helper remains Windows PowerShell 5.1-compatible.
Do not fabricate success, replace a failed local gate with CI, or change
branch protection.

## Acceptance Criteria

* LF/CRLF/lone-CR textual variants hash identically; meaningful bytes differ.
* Fresh Verify succeeds against checked-in delivery; four regenerated hashes
  match canonical inputs and binary delivery hash is unchanged.
* Existing 32 native checks pass; no Double.IsFinite remains in shared helper.
* `python3 -m unittest discover -s tools -p 'test_rpi_checks.py' -q` passes.
* One independent Review and full current-main exact-head gate permit push.
* Updated PR body contains all four disclosures, validation limitations and
  no closing keywords; three GraphQL replies/resolutions occur only after push.

## Sources

.copilot-tracking/research/2026-10-31/pr-558-unresolved-threads-research.md,
C1-C7 and W1; current source README, verifier and existing native tests.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Canonical source binding and compatibility validation

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Implement textual canonical hashing and targeted regression

Add one helper to the owning verifier, use it for four hashes, add one focused
PowerShell test script. Existing test ownership: retain Test-NativeShapes.ps1.
Removals: none. Maximum additions: one regression script, no Python duplicate
verifier. Semantic cases cover line endings and whitespace, plus four receipt
bindings. Generated target: verification.json and existing validation.json;
canonical target: unchanged checked-in PPTX.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Verify receipt, native guards and runner tests

Depends on P01-T01. Use existing local PowerShell runtime if available, otherwise
isolated local Docker runtime; no host package installation. Run native checks
and semantic source hash tests, then actual Verify on an external copy of delivery.
Refresh receipt from successful report, keeping native/preview history honest.
Run four receipt-binding assertions only after refresh. Update source guide and
directly related index/log. Resolve Microsoft's PowerShell container to immutable
digest, record actual version and run with `--pull=never --network=none`; scratch,
HOME and caches use only an owned external mount.

<!-- rpi:phase id=P02 -->
### [ ] P02: Review and gated remote publication

<!-- rpi:task id=P02-T01 -->
#### [ ] P02-T01: Prepare disclosure, original Review and commit

Depends on P01. Prepare PR body externally, including runtime ancestry and
actual evidence. Run one independent rpi-review; route any findings without
repeating Review. Commit candidate and original RPI evidence with authenticated
privacy-safe author/committer email and required trailer.

<!-- rpi:task id=P02-T02 -->
#### [ ] P02-T02: Gate, exact-head assessment, normal push and resolution

Depends on P02-T01. Fetch main; complete `--all` external local gate without
waiting on a foreign shared lock. Verify receipt against current main immediately
before independent exact-head assessment and normal push. Update PR body with
`gh pr edit 558 --body-file`, reply to each thread with exact evidence and resolve
via GraphQL. Any failed prerequisite blocks remote publication and resolution.

## Dependencies

PowerShell 7.4+ for current verifier; Docker available; Windows 5.1/Office not
available. Complete local gate dependencies, clean committed candidate and
unchanged origin/main. Owner remote authorization already supplied.

## Critique Disposition

One critique executed, verdict Revise; original critique preserved unchanged.

| Finding | Disposition | Resolving evidence |
| --- | --- | --- |
| PC-001 | Rejected as non-applicable to parent | Critique's claimed blanket prohibition on /tmp is not present in parent instructions; parent repository explicitly requires /tmp/ama-rpi-heavy.lock. Do not infer worker-specific restrictions as parent authority. Keep unchanged runner and all real publication gates. |
| PC-002 | Applied directly | Separate semantic checks from four post-refresh receipt bindings in P01-T02 and details. |
| PC-003 | Applied directly | Immutable Microsoft image, version preflight, pull-never/network-none execution and owned scratch/HOME/cache required in P01-T02 and details. |

No unresolved significant/divergent decision. Do not repeat critique.

## Follow-Up Items

* Direct Windows 5.1/Office acceptance remains a separate environment-dependent
  check, not an inferred Linux/container acceptance.

## Handoff

Changes: .copilot-tracking/changes/2026-10-31/pr-558-unresolved-threads-changes.md.
Next: P02-T01 commit after the completed original Review. Publication blocked until all actual
verification and exact-head gate conditions pass.
