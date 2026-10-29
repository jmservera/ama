<!-- markdownlint-disable-file -->
# RPI Phase Details: loading-briefing-review-correction-531

## Metadata

* Task ID: 531-review-correction-2026-10-29
* Task slug: loading-briefing-review-correction-531
* Related plan: .copilot-tracking/plans/2026-10-29/loading-briefing-review-correction-531-plan.md
* Evidence: .copilot-tracking/research/2026-10-29/loading-briefing-review-correction-531-research.md

## Phase Index

| Phase ID | Name | Status | Detail sections |
| --- | --- | --- | --- |
| P01 | Helper recovery | Complete; browser passed | P01-T01 |
| P02 | Punctuation ownership | Complete | P02-T01 |
| P03 | Validation/local delivery | Validation complete; commit/Review finalization pending | P03-T01, P03-T02 |

<!-- rpi:phase id=P01 -->
## P01: Helper readiness and recovery

<!-- rpi:task id=P01-T01 -->
### P01-T01: Complete dependency readiness

Context C1-C4/C7: law handler bindings throw before first read; app's handler-only
gate permits unusable feedback/run. Add regression first and record original
failure. Apply loaded web-design-guidelines/current successfully retrieved rules
before source edits. Check non-null callable methods actually used by each page before any
dependency use. Law's terminal path must use native DOM listeners, a live
status and reload; disabled search/all controls prevent a dead form submission.
No replacement helper implementation or auto-reinjection in law. Preserve app's
two-attempt bounded recovery and lexical execution safety.

Browser expectations: block helper, empty script and partial interface; assert
no sources/search reads, no uncaught page errors, non-stuck status, native
keyboard reload and full recovery of initial read, All sources, source/detail/
provision handlers and search. Construct endpoint fixtures, not a law database.
Node VM expectations: execute whole law script for missing/null/empty/
non-callable/partial exports; prove no helper-dependent binding or fetch and
invoke reload. Extend app mocks with full valid interface, parameterize failures.

Completed: native terminal path and full workspace interface predicate; actual
VM fails before edits (law ReferenceError, null app helper TypeError), then
79 targeted helper/loading/parser/API tests pass. Browser regression added;
execution tracked under P03, not inferred from source.
P03 browser execution now passed for all five law failures and all seven
workspace helper bootstrap cases, with keyboard recovery and no page errors.

Completion evidence: actual new regression fails before source edit, passes
after; browser run passes if admitted or is explicitly recorded blocked.

<!-- rpi:phase id=P02 -->
## P02: Complete punctuation ownership

<!-- rpi:task id=P02-T01 -->
### P02-T01: Shared terminator and exact goldens

Context C5-C6: citation relocation inserts whitespace before only the final
punctuation; splitting turns that into a separate cited punctuation fragment.
Unicode ellipsis does not split at all. Extend the single shared pattern to
one-or-more terminators plus existing closing delimiters, with Unicode ellipsis
also normalized in analyse. Preserve marker protection and abbreviation logic.
Expand existing full-object matrices for terminator runs, nested closers,
before/after/uncited placements, whitespace, valid/unknown adjacent references.
Add literal Still waiting... and ?! supplied goldens; no custom tokenizer.

Completion evidence: goldens fail on original parser and pass after correction;
existing parser and API AI-task suites remain passing.

Completed: shared full-run terminator including Unicode ellipsis and matching
normalization; punctuation/closers can interleave after the first terminator.
Supplied literal goldens fail in all five cases before edits, then complete
full-object matrices and all 79 targeted tests pass. Extra interleaved-closer
counterexample also reproduced before the shared-pattern refinement.

<!-- rpi:phase id=P03 -->
## P03: Validation and local delivery

<!-- rpi:task id=P03-T01 -->
### P03-T01: Required validation

Use PYTHONDONTWRITEBYTECODE=1 and absolute paths to this worktree's src/api/src,
src/core/src, src/agents/src and owning test folders. Nonblocking flock owns
full suites and editable pip setup. Busy admission means record actual holder,
do not mutate shared venv or poll, and run scoped tests and read-only strict
tools only. Existing package mypy configuration is authoritative, no exemption.
Run API/core mypy, ruff check . and ruff format --check ., JS syntax and diff.
Run relevant browser with verified pinned axe only if admitted. Preserve
manifest pins (C8); none of those four source files is targeted. Update API
README for native law recovery and punctuation runs, not broad product claims.

Completed under admitted nonblocking lock: current packages installed editable;
API/core mypy, Ruff lint/format, browser and full units all pass. Core 1463
tests/190 explicit skips; API 1219/316 skips; Chromium 156.0.8078.4 and four axe
states/zero violations. Scenario integrity 11 tests and all four SHA-256 pins
pass. See changes for exact commands, external logs and preserved failed
attempts. No full publication receipt or human/hosted/live acceptance claimed.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Local commits and one Review

Keep stable identity and artifacts; retain original critique/review outcomes.
Use Conventional Commit and required Copilot trailer; no closing keywords.
Implementation commit precedes original independent Review, then final evidence
commit. No remote writes or complete publication gate because publication is
forbidden; do not imply local tests satisfy hosted/human/publication gates.
Route any residual Review findings as later work without another Review.
Distinguish blocking in-scope defects (outcome incomplete/blocked, later correction
required) from nonblocking/unrelated follow-ups (defer with reasons). No blanket
completion claim while a material finding is open; no implementation/Review loop.
The sole reviewer refreshes current Web Interface Guidelines and assesses every
changed web file; record file:line findings and missing/partial checks.
