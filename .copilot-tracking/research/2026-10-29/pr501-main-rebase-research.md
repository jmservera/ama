---
title: PR 501 main rebase research
description: Focused evidence for reconciling the resident UX draft with main
ms.date: 2026-10-29
---

## Brief and controls

Bring draft PR #501, branch `docs/resident-ux-153`, up to date with
`origin/main`, preserving resident UX and upstream intent. Refs #153.
The caller explicitly requests the full RPI loop and local commits, no push,
no Azure changes, no issue-closing keywords, source only under `src/`, tests
outside packages, and `/tmp/mv` validation. Preserve original RPI evidence.

Focused posture, convergence output, internal sources only. Audience: the
coordinator who owns publication. No interaction is available; the task is
specific enough to execute without questions. Research is inline because the
branch history, conflict trace and checks form one bounded investigation.

## Prior knowledge and extensions

Read the case-study original, addendum, knowledge-base index and owner memory.
Recent seven-day session-reference search found no PR 501 record. Existing
2026-10-27 RPI artifacts remain historical evidence, not fresh acceptance.
Selected RPI research/plan/implement/review contracts and repository branch,
append-only, source-layout and validation instructions. Web guidance applies
only if resolving web changes; no visual redesign is authorized. No Azure,
external research or full API suite without the caller's lock condition.

## Questions

* Which commits and files require reconciliation?
* Which upstream files must win, and which append-only entries must survive?
* Which local checks reproduce the relevant CI contracts?
* What can be established locally without publication or cloud changes?

## Cycle 1

### Wider wave

* C1: `src/README.md:11` keeps tests outside owning packages; lines 70-160
  document full and changed-path gate boundaries.
* C2: Initial read-only Git inspection: worktree clean, expected topic branch,
  open draft PR #501 targeting main. Fetched base
  `356a3cfbaa2cd63a6fbf80e87e11a29cacaaf4c7`.
* C3: `git diff --stat origin/main...HEAD` identifies 17 files, three branch
  commits, four small JS copy edits, a lexical test, two UX syntheses,
  knowledge-base index/log and historical evidence, plus a rubric score.

### Deeper wave

* C4: `.github/workflows/src-ci.yml:80` runs owning-project unittest,
  Ruff check/format and mypy; API additionally runs browser checks.
* C5: `src/api/tests/test_content_standard.py:92` adds three boundary tests.
  Upstream has not changed this test, but extensively refactors `app.js`;
  upstream moves the resident draft section into `const write` around line 901.
  Preserve that refactor and insert the draft-only copy in its new location.
* C6: `src/core/tests/test_scenario_manifest.py:21` validates all public source
  hashes. Main changed manifest pins; retain its manifest and rerun the module.
* C7: `/tmp/mv/bin/python`, Ruff and mypy exist (Python 3.12.3, Ruff 0.17.1,
  mypy 2.4.0). Resolve imports using explicit local sibling src/tests paths
  so preexisting shared editable installs cannot select another worktree.
* C8: `docs/reference/README.md:172` and the branch log entry add resident
  work; upstream also adds index/log entries. Preserve both at conflicts.

### Contrarian wave

* C9: Main has 1,083 changed lines in `app.js`, including attached tabs and
  chat. Taking the branch's whole file would erase upstream work. Resolve the
  changed block in the new upstream structure instead.
* C10: The branch rubric score describes its old head and must not overwrite
  main. Explicit caller direction selects main's entire rubric directory.
* C11: Historical changes artifact
  `.copilot-tracking/changes/2026-10-27/resident-content-153-154-changes.md:108`
  preserves incomplete human/AT/operational acceptance. A rebase cannot claim
  those approvals or hosted CI success without a push.
* W1: Web Interface Guidelines fetched in full from
  https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
  on 2026-10-29. Repository Fluent 2/plain ASCII and sentence-case rules take
  precedence over generic typographic preferences; only changed web lines are
  in scope.

## Decisions and readiness

Research disposition: executed. Planning Readiness: Ready.
Accepted: explicit rebase, block-level conflict resolution, upstream rubric and
manifest, targeted local checks, independent critique and Review. Rejected:
whole-file branch resolution of app.js, stale score, cloud validation and
claims that unpushed CI/mergeability have already changed. Defer publication
and exact-head hosted checks to the coordinator. No new research cycle is
needed: named sources answer the bounded questions; actual conflicts belong
to implementation. No research delegation was used.
