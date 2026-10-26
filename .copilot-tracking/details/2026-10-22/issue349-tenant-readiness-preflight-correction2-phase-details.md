---
title: Issue 349 preflight correction2 phase details
description: Bounded task completion expectations
ms.date: 2026-10-22
---

Task ID: 349. Slug: issue349-tenant-readiness-preflight-correction2.
Initial direction: three local shape guards, no live calls. Research C1-C8 is adequate.

<!-- phase: P01 -->
## P01: Shape guards and regression evidence

<!-- task: P01-T01 -->
### P01-T01

Use the canned Fake transport. Exercise each collection field with integers,
floats, true/false, nonempty/empty strings and objects, including matching URI
keys that previously falsely passed. Assert CLI exit 1, fixed unknown reason,
empty facts, no stderr and no private synthetic sentinels in either format.
Preserve missing/null/list behavior and target-blocker priority.
Add explicit non-null list guards before each iteration; no catch-all wrapper.
Completed: three new test methods; red run 32 tests with 42 failures and
19 errors; green run 32 tests passes. Guards cover all three fields.

<!-- task: P01-T02 -->
### P01-T02

Run python3 -B -m unittest discover -s infra/tests -p test_tenant_readiness_preflight.py -q.
Use /tmp/ama-349-correction2-checks installed after observed missing Ruff.
Run isolated Ruff/format on both files and strict script mypy with external cache.
Record commands/outcomes and any amendments in the changes record.
Completed: focused suite, isolated Ruff/format and strict script mypy pass.
Strict mypy exposed two baseline repeated-get narrowing errors in the immediate
api/web readers. Bind each raw value once, then narrow with the existing dict
guard; behavior is unchanged. This is a local type-safe clarification, not a
schema expansion.

<!-- phase: P02 -->
## P02: Review and exact-head publication

<!-- task: P02-T01 -->
### P02-T01

Activate rpi-review once with the correction2 research/plan/details/changes.
Review only this correction delta and supplied finding; preserve earlier adverse
outcomes. Distinguish local functional outcome from pending full gate and final
independent PR review. Do not mark human criteria complete.
Completed once: execution Complete, outcome Residual work. No source defects
found; RV-001 routes authorized publication and RV-002 preserves coordinator
assessment/live-human boundaries. No repeated Review.

<!-- task: P02-T02 -->
### P02-T02

Resolve gh api user and configure repository-local noreply email before committing.
Commit source/tests plus correction2 artifacts only, Conventional Commit and
Co-authored-by trailer. Fetch main and check requested base. Invoke full gate once
with new external --out and sufficient --lock-timeout to wait for shared owner.
After the gate, explicitly fetch origin main again, resolve its current SHA and
verify the receipt with that freshly fetched --base against the unchanged new
head and clean inputs immediately before normal push. If main moved, stop
publication without rebasing or running a second full gate. Any mismatch or
failure blocks publication; never reuse the old receipt.
Do not change committed source/evidence after gating. Final gate outcome belongs
in external session evidence and PR body, not a new commit invalidating receipt.
