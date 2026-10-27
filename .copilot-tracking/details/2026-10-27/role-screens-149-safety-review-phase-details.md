---
title: Role-screen safety review phase details
ms.date: 2026-10-27
---

Task ID: 496-r4391306128. Status: Ready after one critique, direct PC-001-PC-003 dispositions.
Execution reconciliation: P01/P02 complete. Exact production delta, executable
regression, actual-browser checks, full initial API/core results and final-base
focused reruns are recorded in the changes artifact. P03 remains pending;
source implementation is review-ready, not yet publication-ready.

## P01: Restore context and prove regression

### P01-T01

C1-C4 establish exact presentation and optional projection boundary. Execute the
actual roleScreensView with controlled h/api/show globals and real workSummary
in Node, supplied through unittest subprocess without third-party dependencies.
Exercise two distinct clocks, a task owner different from follow-up owners,
Unknown times, an ordinary work row and omitted/null work. Assert marker count,
every field, native href and current selection/page. Observe the missing-context
failure before applying the surgical host change. Do not weaken existing tests.

### P01-T02

C6-C7 show parent has no installed module. Browser-only register one read-only
test module for the authenticated role, exercise actual loopback staff rows,
then a separate actual contractor context. Inspect actual projected clocks and
assert their fields in the rendered link, Unknown retention and no-work/privacy
behavior; ensure no POST after login. Retain parent empty-registry assertion.
No production screen is registered by tests. Document restoration and the
unchanged no-work contract in the existing Specialist screen README section.

## P02: Validate and reconcile

### P02-T01

Set W to the absolute current worktree. From src/api run:

```bash
PYTHONPATH=$W/src/api/src:$W/src/core/src:$W/src/agents/src:../core/tests:../agents/tests python3 -m unittest discover -s tests -q
```

Use the same explicit roots from src/core, with tests on PYTHONPATH. Missing
dependencies permit pip installation only after the actual missing result;
use an external venv to keep candidate inputs clean. No uv or private dataset.
Record initial failures. If source hash stale, regenerate with repository
authoring tool or a surgical exact hash update, never reclassify coverage.

### P02-T02

Run parent role browser check with worktree roots; review changed JS against
fresh Web Interface Guidelines, local Fluent/plain-language baseline and all
applicable fetched rules. Syntax-check JS and run repository Ruff/mypy selectors
for edited Python. Preserve lack of human/AT acceptance.

Before Review/commit/gate, compare docs/reference/log.md at old parent
4140ebbf34174f2bdc9f6e980533797e92410ca9 and reviewed main
ad34164a8ab01fdca96776a62c536a3bfc4ec88d against the final candidate
(superseding initial 0ee2ac2f after the authorized second rebase).
Every pre-existing line/entry must survive verbatim in relative order, counting
shared history once. Record both SHAs and skipped bot commits 17b60576/4140ebbf.
Any discrepancy blocks Review/publication until reconciled without rewriting
historical entries.

## P03: Review, gate and draft publication

### P03-T01

Reconcile checklist/details/changes/test results before independent Review.
Original Review occurs once and is immutable; any findings route to follow-up.
Any unresolved in-scope safety/access/privacy/evidence-integrity/engineering
finding blocks parent publication even if the scoped gate passes. Inherited
child/combined-head or human/AT/Fluent limitations remain explicit residuals.
Use authenticated gh user id/login to configure local privacy-safe author and
committer. Conventional Commit with Refs #149, Refs #496 and required trailer.

### P03-T02

Fetch current main before the single gate; inspect changed-path selection.
Commit all original dated artifacts before invoking:

```bash
python3 tools/rpi-checks.py --changed --jobs 3 --base <current-main-sha> --out <new-external-path>
```

Verify receipt with --required-scope partial against freshly fetched main. No
--all, no retry after a candidate mutation, no cloud fallback, no false full
claim. If main moves or tools/evidence mutate, record a blocker instead of
silently exceeding the one-gate budget. Inventory all ignored/untracked outputs;
preserve and relocate exact owned paths externally rather than discard them.
Final-head review is read-only and retained exclusively at the external session
files/role-screens-149-safety-review/final-head-review.md through all publication.
Verify immediately before exact-head assessment and again immediately before
push. No candidate file, including ignored output, may change in between.
Adverse assessment blocks publication. Do not erase or revise original Review.

### P03-T03

Expected remote old head: 4140ebbf34174f2bdc9f6e980533797e92410ca9, subject to
fresh verification. If remote moved unexpectedly, explicit lease must refuse;
do not overwrite shared changes. Keep parent/children drafts; no merge/closure.
Push only feat/role-screens-149, verify remote SHA/isDraft and post thread reply
with changed behavior and test evidence. Record final SHA and external receipt
path in final-head evidence without changing the gated commit.
After the final remote write, retain a local copy at
.copilot-tracking/reviews/logs/2026-10-27/role-screens-149-safety-review-final-head.md.
This intentionally creates a post-publication untracked evidence input; the
receipt no longer verifies that working copy until it is preserved externally
again. Do not commit it, claim current clean verification, or push a later head.
