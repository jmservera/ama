---
title: Resident validator tool-failure correction details
description: Actual CLI contract and prospective candidate Review boundary
ms.date: 2026-10-24
---

Task jmservera/ama#441, same native59f31558. Research Complete/Ready;
Plan candidate, source/bot edits blocked pending one independent critique.
Fresh HEAD2b364/treee1e412/basef1e2/topicb06ca0b4 direct-parent verified.

<!-- rpi:phase id=P01 -->
## P01 - Preserving bot and implementing failure classification

<!-- rpi:task id=P01-T01 -->
### P01-T01 - Normal bot fast-forward

Recheck exact expected main/topic/local and diff parent/path before ff-only.
Only owned new correction3tracking exists; no stash/discard/moving source.
If unexpected changes stop/report. Bot full16+/16-delta already read:
score metadata/rationales/citations, no source change. Preserve exact score
SHA and ancestry, never reproduce/edit generated content manually.

<!-- rpi:task id=P01-T02 -->
### P01-T02 - Lint result validity

Modify only lint() in existing validate-integration.py. Actual0.45.0text
emitter produces stdin:line[:column] MDnnn/aliases description and writes
diagnostics to stderr. Existing helper merges output and normalizes location
prefix; retain shape and counter semantics. Validate complete output first,
then normalize. Status0requires empty output; status1requires at least one
genuine line and no unrecognized line. Reject status2/3/4/negative etc and
startup/config errors even if accompanied by genuine diagnostics.
Use explicit RuntimeError with CLI/status/output context, no catches/defaults.
Node absence OSError propagates. No need for custom-rule formats: command
loads task config built-in rules only. Do not silently accept empty1.

Retain all15existing methods, add at most four in existing integration tests.
Test actual missing CLI subprocess and main caller using real repository
ROOT/BASE retained before real-git fixture patch; main should fail on first
lint and create no report. This does not invoke whole-app or heavy gate.
Mocked CompletedProcess cases cover clean, genuine optional-column/duplicate
normalization and mixed config/startup, empty/noise/inconsistent-status. Mocks
verify public lint function, not a detached regex. External real installed CLI
demonstrates real contract and post-change success/failure.

<!-- rpi:task id=P01-T03 -->
### P01-T03 - Focused validation and preservation

One coherent source/test batch, then combined test_validate*.py, both actual
CLI validators, actual absent CLI main re-run with new external output path.
Actual CLI clean and genuine MD012/MD034/MD059 fixtures and missing/malformed
config must behave as designed; use external temp config, no source mutation.
New Markdown artifacts lint/links, real manifest/product/source/score diff
preservation. Correction-only diff check reported separately from FAILED52
full-branch including12refinement. All adverse original logs retained.
If this cycle fails stop/report, no another extra cycle or silent fixes.

<!-- rpi:phase id=P02 -->
## P02 - Committing and reviewing actual candidate

<!-- rpi:task id=P02-T01 -->
### P02-T01 - Commit implementation before Review

Resolve gh api user, configure local privacy-safe author/committer, conventional
message and required Copilot trailer. Stage only correction3target sources and
new artifacts, no scores/products/raw archives. Commit implementation with
honest pre-Review state, never preclaim future Review. Record actual UTC time,
head/tree/base/remote and clean state externally, preserving exact phase order.

<!-- rpi:task id=P02-T02 -->
### P02-T02 - One Review then evidence-only finalization

Review actual committed implementation once, all accepted criteria/current
markers/changes, genuine tests and failure evidence, residuals. No source,
plan, details, changes, research or critique edits during/after Review.
If defect remains stop/report, no further cycle. Write canonical Review only;
then commit this new Review evidence only using same safe-identity procedure.
Final evidence-only commit does not change assessed source/test bytes; it still
needs later coordinator exact-head gate/assessment, no self-attestation.
Session-only JSON final handoff owns actual Review/commit completion and exact
identities. Include timestamps, commands/results, bot hash, residuals/limits,
clean tracked/index/untracked/ignored and no heavy gate/publication.

## Pre-Commit Actual State

P01 Complete, all3tasks evidenced, no divergent plan change or blocker.
Research file birth08:13:30.678UTC, plan08:16:16.743/details08:16:16.745,
critic08:17:34.611, changes08:18:00.551, normal botff observed08:18:09,
source/test modification08:18:42.055/.057. These are actual filesystem birth/
modify and tool-observed UTC events, not fabricated phase history; exact
timestamps externally retained in441-correction3-phase-file-times.json.
Actual installed CLI contract probes/complete main failure and19test results
recorded under Changes. All requested current product/quality/identity/live
boundaries remain unchanged. P02implementation commit must happen next,
then Review its actual head/tree, not uncommitted hypothetical code.
