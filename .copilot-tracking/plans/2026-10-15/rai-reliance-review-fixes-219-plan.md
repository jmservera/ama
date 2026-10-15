---
title: RAI reliance review fixes
description: Bounded follow-up to PR 315 correctness review
ms.date: 2026-10-15
---

## Task Metadata

Task ID: 219-review-fixes. Slug: rai-reliance-review-fixes-219.
Parent: 219 / src-rai-release-record-219. Mode: automatic, explicitly requested
short RPI loop and publication on existing PR.

## Executive Summary

Close RV-001 through RV-003 with fail-closed historical-output reliance and
authorization-sensitive briefing caching. Preserve manual/template review and
reject paths. Keep RV-004 and unmet issue criteria open.

### What You May Not Know

Dispatch already denies the changed route; historical reliance independently
selected the old alias. Release approval does not change the case version.

## Sources

Research disposition: reused; Planning Readiness: Ready.
Evidence: .copilot-tracking/reviews/logs/2026-10-15/src-rai-release-record-219-review.md,
store.py, sqlstore.py, ai_registry.py, ai_tasks.py and test_assistant_release.py.
No new external research or human authority is needed for these known defects.

## User Decisions and Requirements

* Work only in the supplied worktree and branch; merge conflicting origin/main
  using /tmp/reslog.py for the append-only log.
* Fix RV-001/002/003; retain RV-004, Refs #219 and unchecked unmet criteria.
* Production code/tests only in src; do not change protected paths or use
  prohibited SQL patterns, private data, uv, new PRs or force pushes.
* Run core/API suites with CI PYTHONPATH and /tmp/zf164 tools, record actual
  results, commit artifacts with required identity/trailer, push same branch,
  update draft PR 315 and mark ready only after the fixes pass.

## Goals

Historical AI output requires an exact valid selected release on the current
task route even when inference is disabled; approval restores denied briefings.

## Scope and Non-Goals

Retained legacy reliance, shared route selection, owning API integration tests
and directly related README. No schema, deployment, provider, private-data or
authority changes. No removals; no new production modules or test files.
Maximum additions: one route helper and eight regression test methods.

## Functional Requirements

* Reject absent/malformed references and absent current selection.
* Select current fast/strong route from registered task metadata, independently
  of the historical output alias, and compare the original reference exactly.
* Do not reuse configured template fallback cache entries across approval.
* Preserve manual/template acceptance and AI rejection.

## Non-Functional Requirements

Use existing portable SQL and typed helpers; no new dependencies or exceptions
to lint/type policy. Tests remain synthetic, never live inference.

## Acceptance Criteria

* [x] RV-001 inference-off SQL/JSON ordinary/document accept/edit, cached AI
  and priority view/review deny absent/malformed references.
* [x] RV-002 fast/strong changes deny cached AI and ordinary/document/priority
  accept/edit; exact original reference and current selection both required.
* [x] RV-003 deny/repeat/approve/request yields one scripted call without case edit.
* [x] Core/API full suites, ruff/format/mypy pass; changes record exact results.
* [x] Same PR updated honestly and marked ready, without merging.
* [ ] RV-004 named holders, actual approved evaluation, Docker/SQL Server/Azure
  and direct human acceptance remain unverified, not acceptance of live use.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct reliance and recovery

<!-- rpi:task id=P01-T01 -->
* [x] P01-T01: Add regressions, reproduce defects, correct shared guards and cache.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate and publish

<!-- rpi:task id=P02-T01 -->
* [x] P02-T01: Run required checks; update README and changes evidence.
<!-- rpi:task id=P02-T02 -->
* [x] P02-T02: One post-implementation review; commit/push/update existing PR.

## Critique Disposition

Final-candidate critique Complete / Pass, no findings; implementation-ready.
Artifact: .copilot-tracking/reviews/plans/2026-10-15/rai-reliance-review-fixes-219-plan-critique.md.
Test owner: src/api/tests/test_assistant_release.py;
semantic coverage of the three actual failure scenarios, not only guard proxies.
Canonical source/README only; no generated targets or exact removals.

## Follow-Up Items

* RV-004: governance owners supply named holders and competent oversight;
  evaluation owners supply actual approved evaluation/serving proof; platform
  owners obtain permitted Docker, SQL Server and Azure evidence.

## Handoff

Details: .copilot-tracking/details/2026-10-15/rai-reliance-review-fixes-219-phase-details.md.
Changes: .copilot-tracking/changes/2026-10-15/rai-reliance-review-fixes-219-changes.md.
One critique before implementation; one review afterward.
P01/P02 complete; one Review Complete / Conformant within engineering scope.
Fix commit 0d44f03 and ordinary main integration 266f292 pushed to the existing
branch. PR 315 updated with Refs #219 and marked ready; merge state CLEAN at
publication, no CI checks reported yet. After late main integration, API 492
run/98 skipped and lint/format/mypy pass (36 files); core 312 and agents 70 pass.
All commands and harness corrections are recorded in changes/details.
RV-004 remains unchecked and does not block code review readiness; it does block
the affected live/human/platform acceptance. No further source work selected.
