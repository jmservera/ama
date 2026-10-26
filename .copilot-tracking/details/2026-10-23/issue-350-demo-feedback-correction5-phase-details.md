---
title: Issue 350 feedback checker correction 5 phase details
description: Bounded implementation and validation contract for JSON number fixes
ms.date: 2026-10-23
---

Task ID: issue-350-demo-feedback-correction5.
Plan: .copilot-tracking/plans/2026-10-23/issue-350-demo-feedback-correction5-plan.md.
Research C1-C5 is sufficient; no unresolved design choice.

## P01-T01: Red-first serialized regressions

Extend InputSafety using real bundle builders and raw JSON tokens. Inject
1e999, -1e999 and 1.0e999 into latency_ms, AI item rank and an unchecked
list/dict payload under the programme body. Assert a unique replacement.
Build reports with a runtime loader that raises AssertionError if invoked:
invalid JSON must block before evidence checks. Verify invalid JSON and
non-finite diagnostic in every measurable CHECK, gaps NOT-RUN,
offline_only true and acceptance not-accepted.
Schema matrix: true, false, 1.0, 2 must block with schema diagnostic;
supported integer 1 retains ai_evidence PASS and loader acceptance.
Finite matrix: 1.25, 1e308, 1e-999, -1.25; rank is not a validated field
and remains accepted, latency rejects only the negative. Keep ordinary
finite/type controls separate from the red regression selection.
Record red failures before editing checker source.
Executed: two selected methods produced 13 failing subtests before checker
edits; nine overflow and True/1.0 reached the runtime sentinel, while False/2
failed the strengthened diagnostic assertion. See changes for exact command.

## P01-T02: Loader-boundary correction

Introduce a small typed parse_float callback: convert str using float, reject
unless math.isfinite, return finite float. Wire it into json.loads alongside
the retained parse_constant. Let existing ValueError handling report invalid
JSON BLOCKED. No decoded-tree recursion, integer float conversion, component
rank constraint or latency-policy change.
Store schema_version once, require type(value) is int and exact supported
value before continuing. Diagnostic states integer requirement explicitly.
Executed without deviation: typed decoder callback and exact int guard only;
module documentation updated to state the constraints.

## P02-T01: Green and local checks

Run entire focused module under installed /tmp/fh350-venv with bytecode
disabled. Run pinned existing Ruff lint plus format/whitespace checks on both
tools; use formatter if required. Inspect diff and ignored status. Record red
and green counts and commands in changes artifact. No full-gate invocation:
coordinator owns it after the final local commit. Do not modify earlier
receipt, tooling, tests outside this module or any other worktree.
Executed: final 77-test suite, Ruff 0.17.1 lint, formatter check and whitespace
all pass. One ordinary formatter correction applied before final validation.
No ignored inputs; no dependency installation or other source edits.

## P03-T01: One Review

Activate rpi-review after reconciling plan markers, details and changes.
Review corrected loader, exact regression coverage, validation outputs and
evidence boundaries once. Record execution separately from outcome. The
local RPI review does not substitute for coordinator independent exact-head
assessment or required human/hosted acceptance. Route any residual findings
outside scope to later work, without another implementation/review cycle.
PC-001: local completion requires no unresolved in-scope acceptance finding;
if Review exposes one, preserve its outcome and mark the handoff blocked
rather than asserting completion. No repeat Review.
Executed once: Complete, outcome Conformant within local scope. No in-scope
defect or new decision/evidence gap. RV-001 routes out-of-scope publication
validation to coordinator. This does not certify independent acceptance.
PC-002 rejected: worker-local /tmp prohibition does not govern this primary;
preserve established test tempfile behavior without new scratch directories
in the candidate or changes to helpers/ignore rules.

## P03-T02: Local commit and stop

After passing local checks and a Review with no unresolved in-scope findings,
gh api user supplies id/login; configure local
privacy-safe noreply email and use it for author and committer. Stage only
the two named tools and correction5 artifacts. Inspect staged diff, commit
using Conventional Commits, Refs #350 and required Copilot coauthor trailer.
Keep issue #350 open/all original criteria unticked, PR #436 draft. No push,
amend, merge, full gate or publication. State may record commit as the intended
atomic closeout action; do not introduce a postcommit evidence commit that
would invalidate later exact-head evidence.
Prepared: gh api user returned id 8036360/login jmservera; local email set to
8036360+jmservera@users.noreply.github.com. Use this address explicitly for both
author and committer. Final artifacts carry the atomic closeout state;
successful containing commit and clean final worktree are the commit evidence.
No get_changed_files tool is exposed by this host. Staged content inspection
uses bounded git diff --cached as the available local equivalent, rather than
inventing a tool result or skipping content verification. Commit message uses
Conventional Commits, Refs #350 and required Copilot coauthor trailer.
