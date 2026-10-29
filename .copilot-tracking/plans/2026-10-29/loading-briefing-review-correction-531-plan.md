<!-- markdownlint-disable-file -->
# RPI Plan: loading-briefing-review-correction-531

## Task Metadata

* Task ID: 531-review-correction-2026-10-29
* Task slug: loading-briefing-review-correction-531
* Planning status: Ready; original critique Revise, findings disposed
* Plan date: 2026-10-29
* Phase details: .copilot-tracking/details/2026-10-29/loading-briefing-review-correction-531-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-29/loading-briefing-review-correction-531-plan-critique.md

## Executive Summary

Make law-viewer helper failure recoverable with a native reload, strengthen the
workspace's incomplete-helper readiness boundary, and preserve complete
punctuation runs with their own citations. Keep existing action semantics,
bounded workspace recovery, abbreviation handling and human-review boundaries.
Execute strict checks and regression-first tests, then one independent Review
and local Conventional Commits; do not publish.

### What You May Not Know

Only index.html and law.html load the helper. Workspace readiness checks only
handler although it also needs run/feedback. Unicode ellipsis is another
parser sibling: it currently merges separate cited claims. Heavy suites may be
unavailable under the explicitly authorized nonblocking-lock fallback.

## User Decisions and Requirements

* Correct both Copilot findings and audit complete sibling surfaces before edits.
* Complete Research, Plan, Implement and Review with dated, committed evidence.
* Reuse feat/loading-briefing-hax-531 / PR #538; pull --rebase first, already done.
* Source in src/; no push, az, force-push or closing keywords.
* Run mypy, Ruff lint/format in API/core; use source-first unit paths and relevant browser check.
* Hold flock -n /tmp/ama-rpi-heavy.lock for full suites; if busy, run targeted tests and disclose unmet checks.
* Preserve scenario manifest pins; update only if a pinned source changes.

## Goals

* No helper download/interface failure strands the standalone viewer.
* Statement text, resolved citations and unresolved references stay together.

## Scope and Non-Goals

In scope: law.js, app.js helper-readiness predicate, existing loader tests,
loading browser check, ai_tasks.py, core parser tests and API README.
No redesign, helper loader refactor, generalized language parser, data edits,
Azure, release or unrelated cleanup.

## Functional Requirements

* Law checks callable handler/run before binding or fetching. Missing/null/empty/
  incomplete helpers render a live actionable error plus native Reload law viewer.
  Disable inert search controls and prevent form navigation; no automatic reads
  or dependency reinjection. Reload after network recovery restores real handlers.
* Workspace gates handler/run/feedback before start and direct consumer work.
  Preserve native terminal recovery and existing bounded retry behavior.
* Shared statement terminator matches full ASCII punctuation runs and Unicode
  ellipsis followed by supported closing quotes/brackets. Relocation and split
  reuse it; normalize space before Unicode ellipsis like other terminators.

## Non-Functional Requirements

* Native keyboard recovery, explicit live error and no uncaught page error.
* No new dependencies, test suppressions or type escapes.
* Tests own constructed public data only; no private default data or real model.

## Acceptance Criteria

* Full-object regressions cover ellipses, ?!, mixed runs, Unicode ellipsis,
  closing delimiters, before/after/uncited, tabs and line breaks.
* Existing title, suffix, abbreviation, unresolved and dropped-bullet behavior stays intact.
* Browser blocks law helper, observes terminal state/no reads/no page errors,
  activates native reload by keyboard, then exercises restored listing/search/details.
* Workspace tests reject partial interfaces without premature listeners or reads.
* Requested strict commands pass; full/browser suites pass or are explicitly
  blocked by nonblocking admission, with targeted fallback evidence.

## Sources

Research: .copilot-tracking/research/2026-10-29/loading-briefing-review-correction-531-research.md, C1-C8/W1.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Helper readiness and recovery

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add helper-failure regressions and recover the law page

Use actual law.js in a Node VM for absent/null/empty/partial/non-callable helper
objects and native reload. Add browser cases for blocked/missing/partial law
helper and restored interactions; extend existing app readiness tests.
Apply the loaded web-design-guidelines skill and successfully retrieved current
rules before web edits; preserve repository content/ASCII conventions.

<!-- rpi:phase id=P02 -->
### [x] P02: Complete punctuation ownership

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Expand full-object parser goldens and fix the shared terminator

Expand existing delimiter/trailing citation matrices; add literal supplied
two-statement regression. Preserve all prior tests and parser behavior.

<!-- rpi:phase id=P03 -->
### [ ] P03: Validation and local delivery

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Document and validate the correction

Update API README. Nonblocking admission owns shared venv mutation and heavy
tests; install current core/agents/api editable distributions only while owned.
Run full API/core discovery and browser if admitted; otherwise scoped units,
strict mypy, ruff check . and ruff format --check . with source-first paths.
Do not queue or poll a foreign lock. Check manifest hashes and JS syntax.

<!-- rpi:task id=P03-T02 -->
#### [ ] P03-T02: Commit and independently Review once

Resolve gh api user and use authenticated repository-local noreply identity
for author/committer. Commit implementation plus original RPI evidence, perform
one independent Review, retain its original outcome and route findings without
repeating Review. Commit final evidence locally. Stop as requested.
The sole reviewer must refresh Web Interface Guidelines and assess all changed
web files with file:line findings and explicit retrieval/check limitations.
Blocking in-scope findings mean an incomplete/blocked outcome, never a complete
fix claim; preserve them and route to an explicitly identified later correction.
Nonblocking/unrelated findings may be deferred with reasons.

## Test Ownership and Change Budget

* Canonical parser tests: src/core/tests/test_ai_statement_sources.py; expand two
  existing matrices and add at most two methods. API store integration retained.
* Canonical helper tests: src/api/tests/test_workspace_scripts.py; add at most
  one law VM method and expand existing loader fixtures.
* Browser: src/api/checks/loading_briefing_browser_check.py; add at most one law
  helper case function, parameterized by failure mode.
* Removals: none. Generated targets: external logs/screenshots/axe output only.
* Semantic coverage: exact complete statement objects and actual helper methods.
  Regression coverage: both supplied failures, sibling interfaces and terminators.
* No pinned source is targeted; validate existing hashes without repinning unrelated files.

## Dependencies

P01/P02 depend on completed research; P03 depends on both. /tmp/mv tools and
browser/axe availability govern validation, not source behavior.

## Critique Disposition

Exactly one critique executed; original verdict Revise is preserved in the
critique artifact. No repeated critique.

| Finding | Disposition | Evidence / response |
| --- | --- | --- |
| PC-001 High | Partially applied; incompatible advice rejected | Explicit blocking/nonblocking outcome rule added. Advice to re-enter implementation after Review conflicts with the active one-pass RPI contract; route later work and report incomplete if blocking, rather than silently claiming completion. |
| PC-002 Medium | Resolved directly | Pre-edit loaded skill/current rules required in P01; fresh retrieval, complete changed-file scope and file:line output required in sole P03 Review. |

## Follow-Up Items

* Human/hosted/live acceptance and publication are outside this local correction.

## Handoff

Ready after critique disposition. Changes:
.copilot-tracking/changes/2026-10-29/loading-briefing-review-correction-531-changes.md.
Implementation and requested strict/full/browser validation complete.
P03-T02 owns candidate commit, the parent-owned single Review and final evidence
only; no source implementation or validation blocker remains.
